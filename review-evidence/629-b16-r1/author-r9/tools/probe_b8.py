#!/usr/bin/env python3
"""Direction B probe: does a known signal reach the reference peer's talker channels?
(this host; the caller holds the bench lock)

usage: probe_b8.py <name> <raw_root> [seconds]

Lane B7's probe_b7.py. Lane B8 changes: the controller staging directory (/tmp/a521) and
the agent (b8_ctl.py); and step 2 keeps the recording. In lane B8 a known tone is played into
the peer's talker inputs (tone_play_b8.sh), and this probe is the proof that it arrives:
McASP0's capture of the DUT's TDM output (8 channels, S32_LE, 48 kHz, <seconds>, default 10)
is sent over the board link to a receiver on this host, which writes it to
<raw_root>/<name>/mcasp-all.raw; nothing is written to the board's /tmp. The board-side
statistics of lane B6 are no longer computed; b8_proof.py grades the recording on this host.

The peer's AAF talker carries its own inputs. Whether a known signal is on them is
established from the levels of what it sends, with no wiring or instrument change:

 1. Controller: read the as-found state; binding rule (owner) for the peer's
    STREAM_OUTPUT 0 -> the DUT's STREAM_INPUT 0: read both formats; if they differ, set
    the LISTENER's (the DUT's) to the talker's and read it back; a listener that does not
    take it is a STOP. Then four identity mappings on the DUT's STREAM_PORT_INPUT 0
    (stream channel c -> cluster c, rendered on TDM slot c), read back, and CONNECT_RX.
 2. SoC board: record 2 s of McASP0 capture (the DUT's TDM output) into /tmp and reduce it
    there to per-channel statistics (non-zero words, minimum, maximum, mean square, distinct values
    among the first 4,096); only those lines leave the board.
 3. Teardown, always: unbind; mappings removed and read back empty; the DUT's STREAM_INPUT 0
    format restored and read back; the recording removed.

Environment (private): SOC_CONSOLE, DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, ECM_HOST.
"""
import json
import os
import socket
import subprocess
import threading
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
SOC, DUT = os.environ["SOC_CONSOLE"], os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
DUT_EID = "020000fffe000001"
EID = {"dut": DUT_EID, "peer": PEER_EID}
HOST = os.environ["ECM_HOST"]
name, raw_root = sys.argv[1], sys.argv[2]
SECS = int(sys.argv[3]) if len(sys.argv) > 3 else 10
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def soc(tag, limit, cmd):
    r = subprocess.run(["python3", "-B", str(TOOLS / "soccon_net.py"), SOC, str(dest / f"soc-{tag}.log"), str(limit), cmd],
                       timeout=limit + 45, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
             f"cd /tmp/a521 && sudo -n timeout 600 python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / "agent-stderr.txt", "w"),
            text=True, bufsize=1)
        self.log = open(dest / "ctl.jsonl", "a", buffering=1)
        line = ""
        for _ in range(3):
            line = self.readline()
            if '"agent-ready"' in line:
                break
        assert '"agent-ready"' in line, line

    def readline(self):
        line = self.p.stdout.readline()
        if not line:
            raise SystemExit("controller agent ended")
        self.log.write(json.dumps(dict(local_rx=round(time.time(), 6), line=json.loads(line))) + "\n")
        return line

    def cmd(self, **q):
        self.log.write(json.dumps(dict(local_tx=round(time.time(), 6), req=q)) + "\n")
        self.p.stdin.write(json.dumps(q) + "\n")
        self.p.stdin.flush()
        out = []
        while True:
            line = json.loads(self.readline())
            if line.get("type") == "done":
                return out
            if line.get("type") not in ("req",):
                out.append(line)

    def quit(self):
        try:
            self.p.stdin.write(json.dumps(dict(op="quit")) + "\n")
            self.p.stdin.flush()
            self.p.wait(15)
        except Exception:
            self.p.terminate()
            self.p.wait(10)
        event("agent-exit", rc=self.p.returncode)


def fmt_of(rows):
    for r in rows:
        if r.get("status") == "SUCCESS" and r.get("cmd") in ("GET_STREAM_FORMAT", "SET_STREAM_FORMAT"):
            return r["payload"][8:24]
    return None


def clk_of(rows, who):
    for r in rows:
        if r.get("what") == f"clock-{who}" and r.get("status") == "SUCCESS":
            return int(r["payload"][8:12], 16)
    return None


TALKER, LISTENER = ("peer", 0), ("dut", 0)
class Rx(threading.Thread):
    """Receives McASP0's capture over the board link into one file."""

    def __init__(self):
        super().__init__(daemon=True)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, 0))
        self.s.listen(1)
        self.s.settimeout(1.0)
        self.port = self.s.getsockname()[1]
        self.bytes = 0
        self.stop = False

    def run(self):
        with open(raw / "mcasp-all.raw", "wb") as f:
            while not self.stop:
                try:
                    c, _ = self.s.accept()
                except socket.timeout:
                    continue
                c.settimeout(1.0)
                while not self.stop:
                    try:
                        d = c.recv(1 << 16)
                    except socket.timeout:
                        continue
                    if not d:
                        break
                    f.write(d)
                    self.bytes += len(d)
                c.close()
                break


ag = None
found = {}
fmt_set = mapped = bound = False
try:
    ag = Agent()
    found["fmt-dut-in-0"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
    found["fmt-peer-out-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0))
    found["clk-dut"] = clk_of(ag.cmd(op="clk", who="dut"), "dut")
    found["clk-peer"] = clk_of(ag.cmd(op="clk", who="peer"), "peer")
    rows = ag.cmd(op="rx", who="dut", idx=0)
    found["rx-dut-0"] = {k: rows[0].get(k) for k in ("status", "conn_count", "stream_id")} if rows else None
    rows = ag.cmd(op="map", act="get", dtype=0x000E, didx=0)
    found["map-dut-in"] = rows[-1].get("payload") if rows else None
    event("as-found", **found)
    if (found["rx-dut-0"] or {}).get("conn_count"):
        raise SystemExit("the DUT's STREAM_INPUT 0 is already bound: not this lane's state, nothing changed")
    # binding rule: the listener (the DUT) adapts
    t, l0 = found["fmt-peer-out-0"], found["fmt-dut-in-0"]
    rec = dict(talker="peer-out-0", listener="dut-in-0", talker_fmt=t, listener_fmt=l0, set=None, listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        fmt_set = True
        s = ag.cmd(op="setfmt", who="dut", idx=0, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s], echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)
    mapped = True
    rows = ag.cmd(op="map", act="add", dtype=0x000E, didx=0, n=4)
    event("map-add", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
    rows = ag.cmd(op="bind", t=PEER_EID, tu=0, l=DUT_EID, lu=0)
    main = next((r for r in rows if r.get("what") == "bind"), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    bound = main.get("status") == 0
    event("bind", status=main.get("status"), conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
    if not bound:
        raise SystemExit(f"bind failed: {main}")
    time.sleep(3.0)
    ag.cmd(op="counters", who="dut", dtype=5, idx=0)
    rx = Rx()
    rx.start()
    soc("record", 60 + SECS, f"cat /proc/uptime; arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {SECS} "
                             f"> /dev/tcp/{HOST}/{rx.port}; echo arecord_rc=$?; cat /proc/uptime")
    time.sleep(2.0)
    rx.stop = True
    rx.join(5)
    event("recording", bytes=rx.bytes, frames=rx.bytes // 32)
    ag.cmd(op="counters", who="dut", dtype=5, idx=0)
finally:
    event("teardown")
    if ag is not None:
        try:
            if True:  # DISCONNECT_RX on an unbound listener changes nothing
                rows = ag.cmd(op="unbind", t=PEER_EID, tu=0, l=DUT_EID, lu=0)
                main = next((r for r in rows if r.get("what") == "unbind"), {})
                after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
                event("unbind", status=main.get("status"), conn_count=after.get("conn_count"))
            time.sleep(1.0)
            if mapped:
                rows = ag.cmd(op="map", act="remove", dtype=0x000E, didx=0, n=4)
                event("map-remove", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
                rows = ag.cmd(op="map", act="get", dtype=0x000E, didx=0)
                event("map-final", readback=rows[-1].get("payload") if rows else None, as_found=found.get("map-dut-in"))
            if fmt_set and found.get("fmt-dut-in-0"):
                s = ag.cmd(op="setfmt", who="dut", idx=0, fmt=found["fmt-dut-in-0"])
                event("format-restore", fmt=found["fmt-dut-in-0"], status=[r.get("status") for r in s])
            back = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
            event("format-final", fmt=back, equal_to_found=back == found.get("fmt-dut-in-0"))
            for who in ("peer", "dut"):
                event("clock-final", who=who, source=clk_of(ag.cmd(op="clk", who=who), who), as_found=found.get(f"clk-{who}"))
            ag.cmd(op="rx", who="dut", idx=0)
        except BaseException as e:
            event("teardown-error", error=repr(e))
        ag.quit()
    event("end")

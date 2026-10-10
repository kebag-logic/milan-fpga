#!/usr/bin/env python3
"""Lane B15 (new; its controller agent and Agent class are lane B10's probe_b10.py, unchanged): the
four-point capture of the known tone, the caller holding the bench lock.

usage: points_b15.py <name> <raw_root> [seconds] [control|dira]

While the tone plays into the reference peer's talker inputs (tone_play_b15.sh), four points are
captured at the same time for <seconds> (default 10):
  (a) the reference peer's link, from its tap: the peer's own talker stream (STREAM_OUTPUT 0);
  (b) the DUT's link, from its tap: the same stream as it arrives at the DUT;
  (c) the DUT's TDM output, recorded by McASP0 on the SoC board (8 x S32_LE, 48 kHz);
  (d) the external capture (the peer's digital output), as a control.

Controller steps (lane B8's agent, b8_ctl.py, on the controller host):
 1. As-found reads: the formats of the peer's STREAM_OUTPUT 0 and STREAM_INPUT 0 and the DUT's
    STREAM_INPUT 0, both GET_CLOCK_SOURCE, the rx states of the DUT's STREAM_INPUT 0 and the peer's
    STREAM_INPUT 0, the DUT's STREAM_PORT_INPUT 0 map.
 2. The peer's STREAM_OUTPUT 0 -> the DUT's STREAM_INPUT 0 under the binding rule (the owner's): read
    both formats; if they differ, set the LISTENER's (the DUT's) to the talker's, read back; then bind.
    The as-found map must hold the four identity mappings (stream channel c -> cluster c), else STOP:
    this tool never edits a map.
 3. With `control`, (d) is made a control of the peer's talker independent of the DUT: the peer's
    STREAM_INPUT 0, as found bound to the DUT's AAF talker, is unbound and bound to the peer's own
    STREAM_OUTPUT 0 under the binding rule (the peer's STREAM_INPUT 0 is the listener and adapts).
    The peer's CLOCK_DOMAIN follows its CRF input (STREAM_INPUT 8), which this tool does not touch.
    (Added after run pts1: a switch never sends a frame back out of its ingress port, so the peer's
    listener cannot receive its own talker this way; pts1's (d) read exact zero with the peer's
    STREAM_INPUT 0 counters at 0. The mode is kept as run.)
 3b. With `dira` (added after pts1), (d) is a positive control of the whole observation chain: the
    peer's STREAM_INPUT 0 stays bound to the DUT's AAF talker as found (no bind or unbind of it), and
    McASP0 plays lane B6's tone loop (b6_tone.py: 997 Hz on channel 0, 9,973 Hz on channel 1, -1 dBFS,
    eight channels S32_LE) into the DUT's TDM input while it records the DUT's TDM output. The DUT's
    as-found STREAM_PORT_OUTPUT 0 map (eight identity mappings, checked, not edited) puts the tone on
    the DUT's AAF talker, which both taps see (port 3 on the DUT's link, port 2 on the peer's) and the
    peer's listener renders to its digital output, (d). The loop is copied to the board, its SHA-256
    checked there, and removed at the end.
 4. Counters (GET_COUNTERS) of the DUT's STREAM_INPUT 0 and the peer's STREAM_INPUT 0, before and after.
 5. Captures: both taps on the tap host (tcpdump, AVTP only, 28-byte record header), the external
    capture on this host, McASP0 over SSH to the SoC board (its to-host bridge leg stopped by the
    caller first); all started together, (c) last, each for its own duration around <seconds>.
 6. Teardown, always: every bind this tool made is unbound, the formats it set are restored and read
    back, the peer's STREAM_INPUT 0 is bound back to its as-found talker (if it was bound), and every
    rx state, format and clock source is read back against the as-found reads. The tap files are
    copied to <raw_root>/<name>/ and removed from the tap host.

Environment (private): CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, SOC_SSH, TAP_HOST, TAP_PEER_IF,
TAP_DUT_IF, CAP_CARD, CAP_NCH, CAP_FMT.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
E = os.environ
CTL, IFACE = E["CTL_HOST"], E["CTL_IFACE"]
PEER_EID, PEER_MAC = E["PEER_EID"], E["PEER_MAC"]
DUT_EID = "020000fffe000001"
name, raw_root = sys.argv[1], sys.argv[2]
SECS = int(sys.argv[3]) if len(sys.argv) > 3 else 10
CONTROL = len(sys.argv) > 4 and sys.argv[4] == "control"
DIRA = len(sys.argv) > 4 and sys.argv[4] == "dira"
IDENT8 = "000f" + "0000" + "0000" + "0001" + "0008" + "0000" + "".join("0000%04x%04x0000" % (c, c) for c in range(8))
BOARD_LOOP = "/tmp/a588-loop.raw"
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
TAPF = "ether[40:2]=0x22f0 or ether[44:2]=0x22f0"
IDENT4 = "000e000000000001000400000000000000000000000000010001000000000002000200000000000300030000"


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
             f"cd /tmp/a588 && sudo -n timeout 600 python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
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


def rxs(rows):
    return {k: rows[0].get(k) for k in ("status", "conn_count", "stream_id", "talker", "talker_uid", "flags")} if rows else None


def counters(ag, tag):
    for who, dt, idx in (("dut", 5, 0), ("peer", 5, 0)):
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=idx)
        r = rows[-1] if rows else {}
        event("counters", tag=tag, who=who, dtype=dt, idx=idx, status=r.get("status"), payload=r.get("payload"))


def bind_rule(ag, talker, listener, sets):
    """The owner's binding rule: the listener adapts. talker/listener = (who, idx)."""
    t = fmt_of(ag.cmd(op="fmt", who=talker[0], dir="out", idx=talker[1]))
    l0 = fmt_of(ag.cmd(op="fmt", who=listener[0], dir="in", idx=listener[1]))
    rec = dict(talker=f"{talker[0]}-out-{talker[1]}", listener=f"{listener[0]}-in-{listener[1]}", talker_fmt=t,
               listener_fmt=l0, set=None, listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        s = ag.cmd(op="setfmt", who=listener[0], idx=listener[1], fmt=t)
        sets.append((listener, l0))
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s], echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who=listener[0], dir="in", idx=listener[1]))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)
    eid = {"dut": DUT_EID, "peer": PEER_EID}
    rows = ag.cmd(op="bind", t=eid[talker[0]], tu=talker[1], l=eid[listener[0]], lu=listener[1])
    main = next((r for r in rows if r.get("what") == "bind"), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event("bind", talker=rec["talker"], listener=rec["listener"], status=main.get("status"),
          conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
    if main.get("status") != 0:
        raise SystemExit(f"bind failed: {main}")


def unbind(ag, talker_eid, tu, listener, tag):
    eid = {"dut": DUT_EID, "peer": PEER_EID}
    rows = ag.cmd(op="unbind", t=talker_eid, tu=tu, l=eid[listener[0]], lu=listener[1])
    main = next((r for r in rows if r.get("what") == "unbind"), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event("unbind", tag=tag, talker=talker_eid, tu=tu, listener=f"{listener[0]}-in-{listener[1]}",
          status=main.get("status"), conn_count=after.get("conn_count"))
    return main.get("status")


def start_captures():
    procs = {}
    tap = (f"sudo -n timeout {SECS + 14} tcpdump -i {E['TAP_PEER_IF']} -w /tmp/b15-{name}-peer.pcap '{TAPF}' 2> /tmp/b15-{name}-peer.err & "
           f"sudo -n timeout {SECS + 14} tcpdump -i {E['TAP_DUT_IF']} -w /tmp/b15-{name}-dut.pcap '{TAPF}' 2> /tmp/b15-{name}-dut.err & "
           f"wait; tail -2 /tmp/b15-{name}-peer.err /tmp/b15-{name}-dut.err; ls -l /tmp/b15-{name}-*.pcap")
    procs["tap"] = (subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", E["TAP_HOST"], tap],
                                     stdout=open(dest / "tap.txt", "w"), stderr=subprocess.STDOUT), time.time())
    time.sleep(2.0)
    procs["extcap"] = (subprocess.Popen(["sudo", "-n", "arecord", "-D", f"hw:{E['CAP_CARD']},0", "-f", E["CAP_FMT"], "-r", "48000",
                                         "-c", E["CAP_NCH"], "-t", "raw", "-d", str(SECS + 6), str(raw / "extcap.raw")],
                                        stdout=open(dest / "extcap.txt", "w"), stderr=subprocess.STDOUT), time.time())
    time.sleep(2.0)
    soc = (f"cat /proc/uptime 1>&2; arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {SECS}; "
           f"echo arecord_rc=$? 1>&2; cat /proc/uptime 1>&2")
    if DIRA:
        # lane B6's McASP0 playback of the loop, started 2 s before the recording, ending by itself
        soc = (f"cat /proc/uptime 1>&2; {{ while cat {BOARD_LOOP}; do :; done | aplay -D hw:0,0 -t raw -c 8 -f S32_LE "
               f"-r 48000 -d {SECS + 6}; echo aplay_rc=$?; }} > /tmp/a588-aplay.log 2>&1 < /dev/null & AP=$!; sleep 2; "
               f"grep -E '^(state|hw_ptr)' /proc/asound/card0/pcm0p/sub0/status 1>&2; "
               f"arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {SECS}; echo arecord_rc=$? 1>&2; "
               f"wait $AP; cat /tmp/a588-aplay.log 1>&2; cat /proc/uptime 1>&2")
    procs["mcasp"] = (subprocess.Popen(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", E["SOC_SSH"], soc],
                                       stdout=open(raw / "mcasp-all.raw", "wb"), stderr=open(dest / "soc-record.log", "w")), time.time())
    event("captures-started", started={k: round(v[1], 3) for k, v in procs.items()})
    return procs


def wait_captures(procs):
    for k in ("mcasp", "extcap", "tap"):
        p, t0 = procs[k]
        try:
            rc = p.wait(timeout=SECS + 60)
        except subprocess.TimeoutExpired:
            p.terminate()
            rc = p.wait(10)
        event("capture-done", what=k, rc=rc, seconds=round(time.time() - t0, 3))


def fetch_taps():
    got = {}
    for side in ("peer", "dut"):
        src = f"/tmp/b15-{name}-{side}.pcap"
        dst = raw / f"tap-{side}.pcap"
        r = subprocess.run(["scp", "-q", f"{E['TAP_HOST']}:{src}", str(dst)], timeout=120)
        got[side] = dict(rc=r.returncode, bytes=dst.stat().st_size if dst.exists() else None,
                         sha256=sha(dst) if dst.exists() else None)
    r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", E["TAP_HOST"],
                        f"sudo -n rm -f /tmp/b15-{name}-peer.pcap /tmp/b15-{name}-dut.pcap /tmp/b15-{name}-peer.err "
                        f"/tmp/b15-{name}-dut.err; ls /tmp/b15-* 2>&1"], capture_output=True, text=True, timeout=60)
    event("taps-fetched", files=got, tap_host_after=r.stdout.strip(), rm_rc=r.returncode)


ag = None
found = {}
sets = []
binds = []
procs = None
try:
    ag = Agent()
    found["fmt-dut-in-0"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
    found["fmt-peer-out-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0))
    found["fmt-peer-in-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=0))
    found["clk-dut"] = clk_of(ag.cmd(op="clk", who="dut"), "dut")
    found["clk-peer"] = clk_of(ag.cmd(op="clk", who="peer"), "peer")
    found["rx-dut-0"] = rxs(ag.cmd(op="rx", who="dut", idx=0))
    found["rx-peer-0"] = rxs(ag.cmd(op="rx", who="peer", idx=0))
    rows = ag.cmd(op="map", act="get", dtype=0x000E, didx=0)
    found["map-dut-in"] = rows[-1].get("payload") if rows else None
    event("as-found", **found)
    if (found["rx-dut-0"] or {}).get("conn_count"):
        raise SystemExit("the DUT's STREAM_INPUT 0 is already bound: not this lane's as-found state, nothing changed")
    if (found["map-dut-in"] or "")[:len(IDENT4)] != IDENT4:
        raise SystemExit("STOP: the DUT's STREAM_PORT_INPUT 0 does not hold the four identity mappings; this tool edits no map")
    if DIRA:
        rows = ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
        found["map-dut-out"] = rows[-1].get("payload") if rows else None
        pr = found["rx-peer-0"] or {}
        event("dira-check", map_dut_out=found["map-dut-out"], peer_in_0=pr)
        if (found["map-dut-out"] or "")[:len(IDENT8)] != IDENT8 or pr.get("talker") != DUT_EID or pr.get("conn_count") != 1:
            raise SystemExit("STOP: dira needs the as-found eight identity mappings on the DUT's STREAM_PORT_OUTPUT 0 and the "
                             "peer's STREAM_INPUT 0 bound to the DUT's AAF talker; nothing changed")
        loop = raw / "b6-loop.raw"
        r = subprocess.run(["python3", "-B", str(TOOLS / "b6_tone.py"), str(loop)], capture_output=True, text=True, timeout=60)
        lsha = sha(loop)
        r2 = subprocess.run(["scp", "-q", str(loop), f"{E['SOC_SSH']}:{BOARD_LOOP}"], timeout=60)
        r3 = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", E["SOC_SSH"], f"sha256sum {BOARD_LOOP}"],
                            capture_output=True, text=True, timeout=30)
        event("loop-staged", tone_rc=r.returncode, bytes=loop.stat().st_size, sha256=lsha, scp_rc=r2.returncode,
              board=r3.stdout.strip())
        if not r3.stdout.startswith(lsha):
            raise SystemExit("the loop on the board does not match")
    bind_rule(ag, ("peer", 0), ("dut", 0), sets)
    binds.append((PEER_EID, 0, ("dut", 0)))
    if CONTROL:
        pr = found["rx-peer-0"] or {}
        if pr.get("conn_count"):
            unbind(ag, pr["talker"], int(pr["talker_uid"]), ("peer", 0), "control-unbind-as-found")
        bind_rule(ag, ("peer", 0), ("peer", 0), sets)
        binds.append((PEER_EID, 0, ("peer", 0)))
    time.sleep(3.0)
    counters(ag, "before")
    procs = start_captures()
    wait_captures(procs)
    counters(ag, "after")
finally:
    event("teardown")
    if ag is not None:
        try:
            for t_eid, tu, lis in reversed(binds):
                unbind(ag, t_eid, tu, lis, "teardown")
            time.sleep(1.0)
            for lis, f0 in reversed(sets):
                s = ag.cmd(op="setfmt", who=lis[0], idx=lis[1], fmt=f0)
                event("format-restore", listener=f"{lis[0]}-in-{lis[1]}", fmt=f0, status=[r.get("status") for r in s])
            pr = found.get("rx-peer-0") or {}
            if CONTROL and pr.get("conn_count"):
                t_eid, tu = pr["talker"], int(pr["talker_uid"])
                tf = fmt_of(ag.cmd(op="fmt", who="dut" if t_eid == DUT_EID else "peer", dir="out", idx=tu))
                lf = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=0))
                event("format-check", ok=tf == lf, talker=f"{t_eid}-out-{tu}", listener="peer-in-0", talker_fmt=tf,
                      listener_fmt=lf, set=None, note="the as-found bind, restored")
                rows = ag.cmd(op="bind", t=t_eid, tu=tu, l=PEER_EID, lu=0)
                main = next((r for r in rows if r.get("what") == "bind"), {})
                after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
                event("rebind-as-found", status=main.get("status"), conn_count=after.get("conn_count"), stream_id=after.get("stream_id"))
            fin = {}
            fin["fmt-dut-in-0"] = fmt_of(ag.cmd(op="fmt", who="dut", dir="in", idx=0))
            fin["fmt-peer-out-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="out", idx=0))
            fin["fmt-peer-in-0"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=0))
            fin["clk-dut"] = clk_of(ag.cmd(op="clk", who="dut"), "dut")
            fin["clk-peer"] = clk_of(ag.cmd(op="clk", who="peer"), "peer")
            fin["rx-dut-0"] = rxs(ag.cmd(op="rx", who="dut", idx=0))
            fin["rx-peer-0"] = rxs(ag.cmd(op="rx", who="peer", idx=0))
            rows = ag.cmd(op="map", act="get", dtype=0x000E, didx=0)
            fin["map-dut-in"] = rows[-1].get("payload") if rows else None
            diff = [k for k in fin if json.dumps(fin[k], sort_keys=True) != json.dumps(found.get(k), sort_keys=True)]
            event("final", equal_to_found=not diff, differ=diff, **fin)
        except BaseException as e:
            event("teardown-error", error=repr(e))
        ag.quit()
    if procs is not None:
        try:
            fetch_taps()
        except BaseException as e:
            event("fetch-error", error=repr(e))
    if DIRA:
        try:
            r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", E["SOC_SSH"],
                                f"rm -f {BOARD_LOOP} /tmp/a588-aplay.log; ls /tmp; ps -o pid,args | grep -E '[a]play|[a]record'; "
                                f"grep -E '^(state|closed)' /proc/asound/card0/pcm0p/sub0/status"],
                               capture_output=True, text=True, timeout=30)
            event("board-cleanup", rc=r.returncode, out=r.stdout.strip())
        except BaseException as e:
            event("board-cleanup-error", error=repr(e))
    for f in sorted(raw.glob("*")):
        event("raw", file=f.name, bytes=f.stat().st_size, sha256=sha(f))
    event("end")

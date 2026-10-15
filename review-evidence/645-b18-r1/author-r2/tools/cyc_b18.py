#!/usr/bin/env python3
# Lane B18 (#645 acceptance after PR #742): lane B17's cyc_b17.py with three changes only: the raw directory
# /tmp/645-b18/raw, the controller staging /tmp/a622 and the capture name 645-b18-cNN.pcap. Its notes follow.
"""Lane B17 (#645, ruling 6099627217 and the resume ruling 6186940255): one bind cycle of the reference
peer's AAF talker to the DUT's STREAM_INPUT 0 at INTERNAL, polled every 0.5 s.

usage: cyc_b17.py <cycle_number>
The caller holds the bench lock for the whole invocation (run_locked_b17.sh), one cycle per invocation.

Lane B14's sw_b14.py classes, reduced to this probe: the controller agent (b8_ctl.py beside avdecc_ro.py on
the controller host), B8's console poll (console_poll_b8.py, unchanged: MCSRV_STAT, AAFM_STAT/AAFM_RATE,
SLIP_LB, SLIP_TDM, RENDER_STAT, CRF_CTRL, CRF_RATE every 0.5 s), the binding rule (read both formats; if they
differ set the LISTENER's to the talker's and read it back; stop if it does not take it) and B14's tap
capture on the DUT's link, here with a 96-byte snap length so the AAF and CRF headers are kept.

The as-found state is the probe state: the DUT on CLOCK_SOURCE 0 (INTERNAL) and its STREAM_INPUT 0 bound to
the peer's STREAM_OUTPUT 0. A cycle checks that state (nothing is changed if it does not hold), starts the
capture and the poll, unbinds at +2 s, applies the binding rule and re-binds 6 s after the unbind (so the poll
runs at least 8 s before the bind), holds 32 s, reads the end state and stops: it ends bound as found. No
clock source, map or register is written; the peer's clock source is read, never set.

Environment (private): DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, TAP_HOST, TAP_IFACE.
"""
import hashlib
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
DUT = os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
TAP, TAP_IF = os.environ["TAP_HOST"], os.environ["TAP_IFACE"]
DUT_EID = "020000fffe000001"
EID = {"dut": DUT_EID, "peer": PEER_EID}
RAW = Path("/tmp/645-b18/raw")
CTL_DIR = "/tmp/a622"
SSH = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10"]
# lane B14's filter: AVTP behind the tap's 28-byte record header, untagged or VLAN-tagged
TAP_FILTER = "ether[40:2]=0x22f0 or (ether[40:2]=0x8100 and ether[44:2]=0x22f0)"
CAP_S, SNAP = 50, 96
PRE_UNBIND_S, UNBIND_TO_BIND_S, HOLD_S = 2.0, 6.0, 32.0
TALKER, LISTENER = ("peer", 0), ("dut", 0)
# GET_COUNTERS at the cycle's start and end: the DUT's STREAM_INPUT 0 and AVB_INTERFACE 0, the peer's talker
CTR = [("dut", 0x0005, 0), ("dut", 0x0009, 0), ("peer", 0x0006, 0)]
RAWT, MONO_RAW = time.clock_gettime_ns, time.CLOCK_MONOTONIC_RAW


def _term(signum, frame):
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
cyc = int(sys.argv[1])
tag = f"c{cyc:02d}"
raw = RAW / tag
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "cycles" / tag
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), mono_raw_ns=RAWT(MONO_RAW), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


class Poll:
    """B8's console poll for the whole cycle, stopped through its stop file."""

    def __init__(self, max_s):
        self.file, self.stopf = dest / "poll.jsonl", raw / "poll.stop"
        self.p = subprocess.Popen(["python3", "-B", str(TOOLS / "console_poll_b8.py"), DUT, str(self.file),
                                   str(max_s), "0.5", f"file:{self.stopf}"])
        event("poll-start", max_s=max_s, period_s=0.5)

    def stop(self):
        self.stopf.touch()
        try:
            self.p.wait(15)
        except subprocess.TimeoutExpired:
            self.p.kill()
            self.p.wait(5)
        n = sum(1 for line in open(self.file) if line.startswith("{")) if self.file.exists() else 0
        event("poll-end", rc=self.p.returncode, polls=n)


class Agent:
    def __init__(self, life_s):
        self.p = subprocess.Popen(
            SSH + [CTL, f"cd {CTL_DIR} && sudo -n timeout {life_s} python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(raw / "agent-stderr.txt", "w"), text=True, bufsize=1)
        self.log = open(raw / "ctl.jsonl", "a", buffering=1)
        self.n = 0
        self.offset_s = None
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

    def sync(self, k=5):
        best = None
        for _ in range(k):
            self.n += 1
            t0 = time.time()
            self.p.stdin.write(json.dumps(dict(op="sync", n=self.n)) + "\n")
            self.p.stdin.flush()
            line = json.loads(self.readline())
            t1 = time.time()
            assert line.get("type") == "sync" and line.get("n") == self.n, line
            s = dict(n=self.n, rtt_ms=round((t1 - t0) * 1e3, 3), offset_ms=round((line["rt"] - (t0 + t1) / 2) * 1e3, 3))
            if best is None or s["rtt_ms"] < best["rtt_ms"]:
                best = s
        self.offset_s = best["offset_ms"] / 1e3
        event("sync", **best)

    def quit(self):
        try:
            self.p.stdin.write(json.dumps(dict(op="quit")) + "\n")
            self.p.stdin.flush()
            self.p.wait(15)
        except Exception:
            self.p.terminate()
            self.p.wait(10)
        event("agent-exit", rc=self.p.returncode)


class Capture:
    """One tap capture of fixed length on the tap host, lane B14's command form."""

    def __init__(self):
        self.name = f"645-b18-{tag}.pcap"
        self.path = "/tmp/" + self.name
        cmd = shlex.join(["sudo", "-n", "timeout", str(CAP_S), "tcpdump", "-i", TAP_IF, "-s", str(SNAP), "-U", "-w",
                          self.path, TAP_FILTER])
        self.p = subprocess.Popen(["timeout", "-k", "3", str(CAP_S + 20)] + SSH + [TAP, cmd + " 2>&1"],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.buf = b""
        end = time.monotonic() + 12
        while time.monotonic() < end:
            b = os.read(self.p.stdout.fileno(), 4096)
            if not b:
                break
            self.buf += b
            if b"listening on" in self.buf:
                break
        self.ok = b"listening on" in self.buf
        event("capture-start", file=self.name, ok=self.ok, seconds=CAP_S, snaplen=SNAP)
        if not self.ok:
            raise SystemExit("tap capture did not start")

    def finish(self):
        out, _ = self.p.communicate(timeout=CAP_S + 25)
        self.buf += out or b""
        summary = [s for s in self.buf.decode(errors="replace").splitlines() if "packet" in s]
        try:
            remote = subprocess.run(SSH + [TAP, f"sha256sum {self.path}; stat -c %s {self.path}"], timeout=35,
                                    capture_output=True, text=True)
            rh, rsize = remote.stdout.split()[0], int(remote.stdout.split()[-1])
            local = RAW.parent / "pcap" / self.name
            local.parent.mkdir(exist_ok=True)
            subprocess.run(["scp", "-q", "-o", "BatchMode=yes", f"{TAP}:{self.path}", str(local)], timeout=125)
            hsh = hashlib.sha256()
            with open(local, "rb") as f:
                for blk in iter(lambda: f.read(1 << 22), b""):
                    hsh.update(blk)
            h = hsh.hexdigest()
            if h == rh:
                subprocess.run(SSH + [TAP, f"sudo -n rm -- {self.path}"], timeout=25)
            left = subprocess.run(SSH + [TAP, f"ls {self.path} 2>&1"], timeout=25, capture_output=True, text=True)
            event("capture-end", file=self.name, rc=self.p.returncode, summary=summary, bytes=rsize, sha256=h,
                  remote_equal=h == rh, removed_from_tap="No such file" in left.stdout)
        except Exception as e:
            event("capture-end", file=self.name, rc=self.p.returncode, summary=summary, error=repr(e))


def fmt_of(rows):
    for r in rows:
        if r.get("status") == "SUCCESS" and r.get("cmd") in ("GET_STREAM_FORMAT", "SET_STREAM_FORMAT"):
            return r["payload"][8:24]
    return None


def clk(ag, who):
    for r in ag.cmd(op="clk", who=who):
        if r.get("what") == f"clock-{who}" and r.get("status") == "SUCCESS":
            return int(r["payload"][8:12], 16)
    return None


def rx_row(ag, who, i):
    rows = ag.cmd(op="rx", who=who, idx=i)
    r = rows[0] if rows else {}
    t = r.get("talker")
    return dict(conn_count=r.get("conn_count"), talker={DUT_EID: "dut", PEER_EID: "peer"}.get(t, t),
                talker_uid=r.get("talker_uid"), flags=r.get("flags"), status=r.get("status"))


def counters(ag, when):
    got = {}
    for who, dt, i in CTR:
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=i)
        r = rows[0] if rows else {}
        got[f"{who}-{dt:#06x}-{i}"] = r.get("payload") if r.get("status") == "SUCCESS" else r.get("status")
    event("counters", when=when, payloads=got)


def state(ag, when):
    s = dict(clk_dut=clk(ag, "dut"), clk_peer=clk(ag, "peer"), rx_dut_0=rx_row(ag, "dut", 0))
    event("state", when=when, **s)
    return s


def binding_rule(ag):
    (tw, ti), (lw, li) = TALKER, LISTENER
    t = fmt_of(ag.cmd(op="fmt", who=tw, dir="out", idx=ti))
    l0 = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
    rec = dict(talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", talker_fmt=t, listener_fmt=l0, set=None,
               listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        s = ag.cmd(op="setfmt", who=lw, idx=li, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s])
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)


def acmp(ag, op):
    (tw, ti), (lw, li) = TALKER, LISTENER
    t_local = time.time()
    rows = ag.cmd(op=op, t=EID[tw], tu=ti, l=EID[lw], lu=li)
    main = next((r for r in rows if r.get("what") == op), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    # the controller host's send and receive times, on this host's clock through the agent's sync offset
    ctl_tx = main.get("t_tx")
    ctl_rx = main.get("t_rx")
    loc = (lambda x: None if x is None or ag.offset_s is None else round(x - ag.offset_s, 6))
    event(op, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", status=main.get("status"),
          conn_count=after.get("conn_count"), flags=after.get("flags"), t_local_send=round(t_local, 6),
          t_cmd_local=loc(ctl_tx), t_resp_local=loc(ctl_rx), rtt_ms=main.get("rtt_ms"))
    t_cmd = loc(ctl_tx)
    return main.get("status") == 0, t_cmd if t_cmd is not None else round(t_local, 6)


def sleep_until(t):
    while time.time() < t:
        time.sleep(0.05)


event("start", cycle=cyc, pre_unbind_s=PRE_UNBIND_S, unbind_to_bind_s=UNBIND_TO_BIND_S, hold_s=HOLD_S,
      tool_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      poller_sha256=hashlib.sha256((TOOLS / "console_poll_b8.py").read_bytes()).hexdigest())
ag = pl = cap = None
unbound = False
try:
    ag = Agent(150)
    ag.sync(5)
    s0 = state(ag, "start")
    r0 = s0["rx_dut_0"]
    if s0["clk_dut"] != 0:
        raise SystemExit(f"the DUT's clock source is {s0['clk_dut']}, not INTERNAL: nothing changed")
    if (r0["conn_count"], r0["talker"], r0["talker_uid"]) != (1, "peer", 0):
        raise SystemExit(f"the DUT's STREAM_INPUT 0 is not bound to the peer's STREAM_OUTPUT 0 ({r0}): nothing changed")
    counters(ag, "start")
    cap = Capture()
    pl = Poll(CAP_S + 30)
    t_poll0 = time.time()
    sleep_until(t_poll0 + PRE_UNBIND_S)
    ag.sync(3)
    unbound = True
    ok, t_unbind = acmp(ag, "unbind")
    if not ok:
        raise SystemExit("the unbind failed")
    sleep_until(t_unbind + UNBIND_TO_BIND_S - 1.0)
    binding_rule(ag)
    ag.sync(3)
    sleep_until(t_unbind + UNBIND_TO_BIND_S)
    ok, t_bind = acmp(ag, "bind")
    if not ok:
        time.sleep(2.0)
        ok, t_bind = acmp(ag, "bind")
        event("bind-retry", ok=ok)
        if not ok:
            raise SystemExit("STOP: the re-bind failed twice")
    unbound = False
    event("bind-time", t_bind_local=t_bind, poll_before_bind_s=round(t_bind - t_poll0, 3))
    sleep_until(t_bind + HOLD_S)
    ag.sync(3)
    s1 = state(ag, "end")
    counters(ag, "end")
    event("cycle-check", clk_dut_end=s1["clk_dut"], clk_peer_same=s1["clk_peer"] == s0["clk_peer"],
          bound_as_found=(s1["rx_dut_0"]["conn_count"], s1["rx_dut_0"]["talker"], s1["rx_dut_0"]["talker_uid"]) == (1, "peer", 0))
finally:
    if pl is not None:
        pl.stop()
    if unbound and ag is not None:
        # never leave the as-found bind removed: one re-bind attempt on any failure after the unbind
        try:
            event("finally-rebind", ok=acmp(ag, "bind")[0])
        except BaseException as e:
            event("finally-rebind", error=repr(e))
    if ag is not None:
        ag.quit()
    if cap is not None:
        cap.finish()
    for f in sorted(raw.rglob("*")):
        if f.is_file():
            event("raw-file", file=str(f.relative_to(raw)), bytes=f.stat().st_size,
                  sha256=hashlib.sha256(f.read_bytes()).hexdigest())
    event("end")

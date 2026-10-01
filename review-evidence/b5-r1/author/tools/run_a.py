#!/usr/bin/env python3
"""Direction A for lane B5 (this host; the caller holds the bench lock for the whole run).

usage: run_a.py <name> <continuity_s> <cycles> <play_s> <raw_root>

With <continuity_s> and <cycles> both 0 it is a diagnostic run: all <capture-channel-count> capture channels
are kept for the whole run, the bind is held 15 s with the peer's STREAM_INPUT 0
counters read every 5 s, and the run then tears down as below.

The #451 first-light DIN method, with the reference peer as the listener and an
external, hardware-clocked audio capture on this host as the observation point.

 1. SoC board: build one 65,536-frame period of the first-light pattern in /tmp and
    check its SHA-256 against the period computed here from the rule (as lane B3).
 2. Controller: start the b5_ctl.py agent; DUT STREAM_PORT_OUTPUT 0 gets eight
    identity mappings (stream channel c <- cluster c), read back.
 3. This host: start the capture (all <capture-channel-count> channels, S24_3LE, 48 kHz). The reader keeps
    channels CAP_L and CAP_R in the raw file, stamps every read with this host's
    clocks, and tracks frame validity online. Ten seconds of all channels are kept
    once the stream is valid, for the channel identification.
 4. SoC board: play the period in a loop into McASP0 for <play_s> s, in the
    background on the board (aplay ends by itself at its duration).
 5. Binding rule before every bind: read the talker's (DUT STREAM_OUTPUT 0) and the
    listener's (peer STREAM_INPUT 0) stream formats; if they differ, set the
    listener's to the talker's and read it back; then CONNECT_RX.
 6. Initial bind; wait for valid audio; <continuity_s> s bound and untouched.
 7. <cycles> unbind/rebind cycles: DISCONNECT_RX, 2 s hold, binding rule, CONNECT_RX,
    first valid run (30 s cap), 3 s more. Clock-offset pings to the controller host
    bracket every ACMP command.
 8. Unbind; the peer's input format back to its as-found value; DUT mappings removed
    and read back empty; aplay stopped by PID if still running; period file removed.

Every ACMP/AECP exchange, ping, console read and SoC step is logged. Grading is
offline (grade_a.py); the online tracker only paces the run.

Environment: SOC_CONSOLE, DUT_CONSOLE, CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, CAP_CARD.
"""
import array
import hashlib
import json
import os
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
SOC, DUT = os.environ["SOC_CONSOLE"], os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
CARD = os.environ["CAP_CARD"]
CAP_PERIOD = int(os.environ.get("CAP_PERIOD", "480"))  # capture period and buffer, frames
CAP_BUFFER = int(os.environ.get("CAP_BUFFER", "24000"))
DUT_EID = "020000fffe000001"
TALKER_UID, LISTENER_UID = 0, 0
NCH, CAP_L, CAP_R = <capture-channel-count>, <capture-channel-index>, <capture-channel-index>  # the peer's output pair, identified by content in the diagnostic run diag1
FS = 48000
HOLD_S, AFTER_S, CAP_S = 2.0, 3.0, 30.0
MIN_RUN = 480  # 10 ms of consecutive valid frames starts a valid run
DUT_READS = ["milan_status", "mem_read 0x90000660 20", "mem_read 0x90000694 8", "mem_read 0x900006cc 12",
             "mem_read 0x900008d4 12"]
PERIOD = "/tmp/a472-din.raw"
PLAYLOG = "/tmp/a472-play.log"
AWK = ("awk 'BEGIN{for(n=0;n<65536;n++){h=sprintf(\"00%02x%02x\",n%256,int(n/256));s=\"\";"
       "for(c=1;c<=8;c++)s=s h sprintf(\"%02x\",c);print s}}' | xxd -r -p > " + PERIOD)

name, cont_s, ncycles, play_s, raw_root = (sys.argv[1], float(sys.argv[2]), int(sys.argv[3]),
                                           int(sys.argv[4]), sys.argv[5])
DIAG = cont_s == 0 and ncycles == 0
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
aplay_line = f"aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {play_s}"


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(args, timeout=limit + 5, **kw)


def dut(tag):
    r = run(["python3", "-B", str(TOOLS / "console_read.py"), DUT, str(dest / f"dut-{tag}.txt"), *DUT_READS], 60,
            capture_output=True, text=True)
    event("dut", tag=tag, rc=r.returncode)


def soc(tag, limit, cmd):
    r = run(["python3", "-B", str(TOOLS / "soccon.py"), SOC, str(dest / f"soc-{tag}.log"), str(limit), cmd],
            limit + 30, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


class Reader(threading.Thread):
    """Reads the capture pipe; writes the two graded channels; tracks validity."""

    def __init__(self, proc):
        super().__init__(daemon=True)
        self.proc = proc
        self.out = open(raw / "cap-lr.raw", "wb")
        self.ts = open(raw / "cap-ts.bin", "wb")  # <q frames_after_read, d realtime, q monotonic_ns>
        self.full = None
        self.full_left = 0
        self.lock = threading.Lock()
        self.total = 0
        self.run_start = None  # start of the current run of valid frames
        self.segments = []  # closed valid runs [start, end)
        self.tags = None
        self.err = None

    def keep_full(self, seconds):
        with self.lock:
            if self.full is None:
                self.full = open(raw / "cap-all-<n>ch.raw", "wb")
                self.full_left = int(seconds * FS)
                event("full-snippet", start_frame=self.total, frames=self.full_left)

    def run(self):
        fd = self.proc.stdout.fileno()
        rem = b""
        fb = NCH * 3
        try:
            while True:
                d = os.read(fd, 1 << 16)
                if not d:
                    break
                t_rt, t_mono = time.time(), time.monotonic_ns()
                d = rem + d
                n = len(d) // fb
                rem = d[n * fb:]
                if n == 0:
                    continue
                a = np.frombuffer(d[:n * fb], dtype=np.uint8).reshape(n, NCH, 3)
                lr = np.ascontiguousarray(a[:, [CAP_L, CAP_R], :])
                self.out.write(lr.tobytes())
                v = lr[:, :, 0].astype(np.int32) | (lr[:, :, 1].astype(np.int32) << 8) | (lr[:, :, 2].astype(np.int32) << 16)
                ok = ((v[:, 0] >> 16) == 1) & ((v[:, 1] >> 16) == 2) & ((v[:, 0] & 0xFFFF) == (v[:, 1] & 0xFFFF))
                with self.lock:
                    base = self.total
                    if self.full is not None and self.full_left > 0:
                        k = min(n, self.full_left)
                        self.full.write(d[:k * fb])
                        self.full_left -= k
                        if self.full_left == 0:
                            self.full.close()
                    # run tracking on frame validity: transitions against the previous state
                    prev = 1 if self.run_start is not None else 0
                    steps = np.diff(np.concatenate(([prev], ok.astype(np.int8))))
                    for i in np.flatnonzero(steps):
                        if steps[i] > 0:
                            self.run_start = base + int(i)
                        else:
                            self.segments.append((self.run_start, base + int(i)))
                            self.run_start = None
                    self.total = base + n
                self.ts.write(struct.pack("<qdq", self.total, t_rt, t_mono))
        except Exception as e:  # recorded, never raised into the run
            self.err = repr(e)
        finally:
            self.out.close()
            self.ts.close()

    def state(self):
        with self.lock:
            return self.total, self.run_start

    def valid_between(self, a, b):
        with self.lock:
            segs = list(self.segments) + ([(self.run_start, self.total)] if self.run_start is not None else [])
        return sum(max(0, min(e, b) - max(s, a)) for s, e in segs)


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
             f"cd /tmp/a472 && sudo -n timeout {play_s + 600} python3 -B b5_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / "agent-stderr.txt", "w"),
            text=True, bufsize=1)
        self.log = open(dest / "ctl.jsonl", "a", buffering=1)
        self.n = 0
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

    def sync(self, k=3):
        best = None
        for _ in range(k):
            self.n += 1
            t0 = time.time()
            self.p.stdin.write(json.dumps(dict(op="sync", n=self.n)) + "\n")
            self.p.stdin.flush()
            line = json.loads(self.readline())
            t1 = time.time()
            assert line.get("type") == "sync" and line.get("n") == self.n, line
            s = dict(n=self.n, t0=round(t0, 6), t1=round(t1, 6), rt=line["rt"], rtt_ms=round((t1 - t0) * 1e3, 3),
                     offset_ms=round((line["rt"] - (t0 + t1) / 2) * 1e3, 3))
            if best is None or s["rtt_ms"] < best["rtt_ms"]:
                best = s
        event("sync", **best)
        return best

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


def binding_rule(ag, tag):
    """Read both formats; if they differ, set the listener's to the talker's; read back."""
    t = fmt_of(ag.cmd(op="fmt", who="dut", dir="out", idx=TALKER_UID))
    l0 = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=LISTENER_UID))
    rec = dict(tag=tag, talker=t, listener=l0, set=None, listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        s = ag.cmd(op="setfmt", who="peer", idx=LISTENER_UID, fmt=t)
        st = [r.get("status") for r in s]
        rec["set"] = dict(fmt=t, status=st, echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=LISTENER_UID))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)
    return rec


def acmp(ag, op):
    rows = ag.cmd(op=op, t=DUT_EID, tu=TALKER_UID, l=PEER_EID, lu=LISTENER_UID)
    main = next((r for r in rows if r.get("what") == op), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event(op, status=main.get("status"), t_tx=main.get("t_tx"), t_rx=main.get("t_rx"),
          conn_count=after.get("conn_count"), stream_id=after.get("stream_id"), flags=after.get("flags"))
    return main, after


def frames_now(rd):
    return rd.state()[0]


def wait_valid(rd, f0, cap_s):
    """First valid run (>= MIN_RUN frames) starting at or after frame f0; None on timeout."""
    end = time.monotonic() + cap_s
    while time.monotonic() < end:
        total, rs = rd.state()
        if rs is not None and rs >= f0 and total - rs >= MIN_RUN:
            return rs
        time.sleep(0.01)
    return None


def stream_flowing(rd, window=FS // 2):
    total, rs = rd.state()
    return rs is not None and total - rs >= window


period = array.array("I", [(((c + 1) << 16) | n) << 8 for n in range(65536) for c in range(8)])
if sys.byteorder != "little":
    period.byteswap()
digest = hashlib.sha256(period.tobytes()).hexdigest()
event("pattern-period", frames=65536, bytes=len(period) * 4, sha256=digest)
event("start", name=name, continuity_s=cont_s, cycles=ncycles, play_s=play_s, cap_period=CAP_PERIOD,
      cap_buffer=CAP_BUFFER)

ag = rd = cap = None
built = mapped = played = False
peer_fmt_found = None
bound = False
try:
    rc = soc("build", 180, f"cat /proc/uptime; {AWK}; echo build_rc=$?; cat /proc/uptime; "
                           f"wc -c < {PERIOD}; echo '{digest}  {PERIOD}' | sha256sum -c")
    built = True
    if rc != 0:
        raise SystemExit(f"period build or check failed on the SoC board (rc {rc})")
    ag = Agent()
    ag.sync(5)
    peer_fmt_found = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=LISTENER_UID))
    event("peer-format-found", fmt=peer_fmt_found)
    ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
    mapped = True
    rows = ag.cmd(op="map", act="add", dtype=0x000F, didx=0, n=8)
    event("map-add", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
    for who, dt, i in (("dut", 6, 0), ("peer", 5, 0)):
        ag.cmd(op="counters", who=who, dtype=dt, idx=i)
    cap = subprocess.Popen(["timeout", "-s", "INT", str(play_s + 300), "arecord", "-D", f"hw:{CARD},0", "-f", "S24_3LE",
                            "-r", str(FS), "-c", str(NCH), "-t", "raw", f"--period-size={CAP_PERIOD}", f"--buffer-size={CAP_BUFFER}",
                            "-v", "-"], stdout=subprocess.PIPE, stderr=open(raw / "arecord.log", "w"))
    rd = Reader(cap)
    rd.start()
    if DIAG:
        rd.keep_full(play_s)
    event("capture-started", diag=DIAG)
    time.sleep(2.0)
    rc = soc("play-start", 30, f"cat /proc/uptime; grep dma-controller /proc/interrupts; "
                               f"nohup sh -c 'while cat {PERIOD}; do :; done | {aplay_line}; echo aplay_rc=$?' "
                               f"> {PLAYLOG} 2>&1 < /dev/null & sleep 1; ps -o pid,args | grep -E '[a]play|[c]at {PERIOD}'; "
                               f"cat /proc/uptime")
    played = True
    if rc != 0:
        raise SystemExit(f"playback start failed (rc {rc})")
    dut("before-bind")
    time.sleep(1.0)
    # initial bind
    binding_rule(ag, "initial")
    ag.sync(3)
    f0 = frames_now(rd)
    main, after = acmp(ag, "bind")
    bound = main.get("status") == 0
    ag.sync(3)
    if not bound:
        raise SystemExit(f"initial bind failed: {main}")
    if DIAG:
        for k in range(3):
            time.sleep(5.0)
            ag.cmd(op="counters", who="peer", dtype=5, idx=0)
            ag.cmd(op="counters", who="dut", dtype=6, idx=0)
        dut("diag-bound")
        event("diag-done", frame=frames_now(rd))
        raise SystemExit(0)
    rs = wait_valid(rd, f0, CAP_S)
    event("initial-valid", frame=rs, f0=f0)
    if rs is None:
        raise SystemExit("no valid audio within 30 s of the initial bind")
    rd.keep_full(10.0)
    # continuity window
    t_c0 = time.monotonic()
    event("continuity-start", frame=frames_now(rd))
    marks = [10, cont_s / 2, cont_s - 10]
    k = 0
    while time.monotonic() - t_c0 < cont_s:
        el = time.monotonic() - t_c0
        if k < len(marks) and el >= marks[k]:
            dut(f"cont-{k}")
            ag.cmd(op="counters", who="peer", dtype=5, idx=0)
            ag.sync(3)
            k += 1
        time.sleep(0.5)
    event("continuity-end", frame=frames_now(rd))
    soc("mid-status", 20, f"cat /proc/uptime; ps -o pid,args | grep -E '[a]play|[c]at {PERIOD}'; "
                          f"for s in /proc/asound/card0/pcm0p/sub0/status; do head -8 $s; done")
    for who, dt, i in (("dut", 6, 0), ("peer", 5, 0)):
        ag.cmd(op="counters", who=who, dtype=dt, idx=i)
    # restart cycles
    for c in range(1, ncycles + 1):
        flowing = stream_flowing(rd)
        ag.sync(3)
        fu0 = frames_now(rd)
        main, after = acmp(ag, "unbind")
        fu1 = frames_now(rd)
        bound = False
        time.sleep(HOLD_S)
        rule = binding_rule(ag, f"cycle-{c}")
        ag.sync(3)
        fb0 = frames_now(rd)
        main, after = acmp(ag, "bind")
        bound = main.get("status") == 0
        ag.sync(3)
        held = rd.valid_between(fu1 + FS // 2, fb0)
        rs = wait_valid(rd, fb0, CAP_S) if bound else None
        event("cycle", cycle=c, flowing_before=flowing, unbind_frames=[fu0, fu1], bind_frame=fb0,
              valid_frames_in_hold=held, first_valid_run=rs, bind_status=main.get("status"))
        if not bound:
            raise SystemExit(f"rebind failed in cycle {c}: {main}")
        time.sleep(AFTER_S)
    dut("after-cycles")
    for who, dt, i in (("dut", 6, 0), ("peer", 5, 0)):
        ag.cmd(op="counters", who=who, dtype=dt, idx=i)
finally:
    event("teardown")
    if ag is not None:
        try:
            # always unbind: DISCONNECT_RX on an unbound listener changes nothing
            ag.sync(3)
            acmp(ag, "unbind")
            time.sleep(2.0)
            if peer_fmt_found is not None:
                cur = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=LISTENER_UID))
                if cur != peer_fmt_found:
                    s = ag.cmd(op="setfmt", who="peer", idx=LISTENER_UID, fmt=peer_fmt_found)
                    event("peer-format-restore", fmt=peer_fmt_found, status=[r.get("status") for r in s])
                back = fmt_of(ag.cmd(op="fmt", who="peer", dir="in", idx=LISTENER_UID))
                event("peer-format-final", fmt=back, equal_to_found=back == peer_fmt_found)
            if mapped:
                rows = ag.cmd(op="map", act="remove", dtype=0x000F, didx=0, n=8)
                event("map-remove", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
                rows = ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
                event("map-final", readback=rows[-1].get("payload") if rows else None)
            ag.cmd(op="rx", who="peer", idx=LISTENER_UID)
            ag.cmd(op="tx", who="dut", idx=TALKER_UID)
            ag.sync(3)
        except BaseException as e:
            event("teardown-error", error=repr(e))
        ag.quit()
    if played:
        soc("play-stop", 40, f"cat /proc/uptime; P=$(ps -o pid,args | grep '[a]play -v -D hw:0,0' | awk '{{print $1}}'); "
                             f"for p in $P; do A=$(tr '\\0' ' ' < /proc/$p/cmdline); echo \"$p: $A\"; "
                             f"if [ \"$A\" = '{aplay_line} ' ]; then kill $p; echo KILLED $p; else echo MISMATCH $p; fi; done; "
                             f"sleep 2; ps -o pid,args | grep -E '[a]play|[c]at {PERIOD}'; echo PS_RC=$?; cat {PLAYLOG}; "
                             f"for s in /proc/asound/card0/pcm0p/sub0/status; do head -3 $s; done")
    time.sleep(1.0)
    if cap is not None:
        # SIGINT to the timeout wrapper is passed on to arecord, which closes cleanly
        cap.send_signal(2)
        try:
            cap.wait(10)
        except subprocess.TimeoutExpired:
            cap.kill()
            cap.wait(5)
        event("capture-exit", rc=cap.returncode)
    if rd is not None:
        rd.join(10)
        event("reader", frames=rd.total, error=rd.err, segments=len(rd.segments))
    dut("final")
    if built:
        soc("cleanup", 30, f"rm -f {PERIOD} {PLAYLOG}; ls /tmp")
    for f in sorted(raw.iterdir()):
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for blk in iter(lambda: fh.read(1 << 22), b""):
                h.update(blk)
        event("raw-file", file=f.name, bytes=f.stat().st_size, sha256=h.hexdigest())
    event("end")

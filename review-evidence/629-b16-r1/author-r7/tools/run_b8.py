#!/usr/bin/env python3
"""One lane B8 case (this host; the caller holds the bench lock for the whole case).

usage: run_b8.py <name> <case> <durations> <raw_root>
  case SW:    durations "h1,h2,h3": the holds after each servo LOCKED, in seconds (item 2)
  case CRFLL: durations "w": the graded window, in seconds (item 3)

Lane B7's run_b7.py, unchanged in method (the B6 tone loop played into McASP0 on the SoC
board, the DUT's AAF talker to the peer's listener, the external capture of the peer's output,
the McASP0 timing sampler, the binding rule, the clock-source rule and the restore). Lane B8
changes:
  * the capture's channel count, the tone pair's channels and the sample format come from the
    private environment (CAP_NCH, CAP_L, CAP_R, CAP_FMT), so this file names none of them;
  * one console poll (console_poll_b8.py, every 0.5 s: servo, AAF meter, SLIP_LB, SLIP_TDM,
    RENDER_STAT, CRF lock and rate) runs from just before the case's binds to after the
    clock-source restore; the run waits for LOCKED by reading it. The console is used by
    nothing else meanwhile, so the 30 s DUT reads of lane B7 are not taken (the poll carries
    their media-clock and slip words) and the full DUT read runs before the binds and at the end;
  * case SW (assignment item 2): both of the peer's talkers bound (its CRF to the DUT's
    STREAM_INPUT 1, its AAF to STREAM_INPUT 0, as lane B7's B0), then the DUT's CLOCK_DOMAIN set
    to CLOCK_SOURCE 2 (AAF, from INTERNAL), 1 (CRF) and 2 (AAF) again, each read back, each held
    for its duration after the servo reads LOCKED; GET_COUNTERS and GET_CLOCK_SOURCE before each
    set, at its LOCKED, mid-hold and at the hold's end;
  * case CRFLL (assignment item 3): lane B7's B-CRF (the peer's CRF talker to the DUT's
    STREAM_INPUT 1, CLOCK_SOURCE 1) with its window, then lane B7's lock-loss observation with
    the CRF talker in place of the AAF one: counters and GET_CLOCK_SOURCE, unbind, 11 s of
    holdover, counters, rebind under the binding rule, LOCKED and 10 s on, counters;
  * board files are /tmp/a521-*, the controller staging /tmp/a521 and the agent b8_ctl.py.

Teardown, always: poll kept running through the clock-source restore and the unbinds, then
stopped; sampler, capture and playback stopped by PID (command lines checked); the DUT's clock
source restored as found and read back; every bind unbound; every listener format this case set
restored and read back; DUT mappings removed and read back empty; board files removed.

Grading is offline (grade_b8.py, b8_events.py). Environment (private): SOC_CONSOLE, DUT_CONSOLE,
CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, CAP_CARD, ECM_HOST, CAP_NCH, CAP_L, CAP_R, CAP_FMT.
"""
import hashlib
import json
import os
import signal
import socket
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parent
PACKET = TOOLS.parent
sys.path.insert(0, str(TOOLS))
import b6_tone as T  # noqa: E402
import hostsrv  # noqa: E402

SOC, DUT = os.environ["SOC_CONSOLE"], os.environ["DUT_CONSOLE"]
CTL, IFACE = os.environ["CTL_HOST"], os.environ["CTL_IFACE"]
PEER_EID, PEER_MAC = os.environ["PEER_EID"], os.environ["PEER_MAC"]
CARD, HOST = os.environ["CAP_CARD"], os.environ["ECM_HOST"]
NCH, CAP_L, CAP_R = int(os.environ["CAP_NCH"]), int(os.environ["CAP_L"]), int(os.environ["CAP_R"])
CAP_FMT = os.environ["CAP_FMT"]
<capture-format-check>
DUT_EID = "020000fffe000001"
FS = 48000
CAP_PERIOD, CAP_BUFFER = 480, 24000
MIN_RUN = 480
SETTLE_S = 20.0
DUT_READS = ["milan_status", "milan_nvm", "mem_read 0x90000738 4", "mem_read 0x90000748 8", "mem_read 0x900008d4 12",
             "mem_read 0x900008f8 8", "mem_read 0x900008e0 8", "mem_read 0x90000660 20", "mem_read 0x90000694 8",
             "mem_read 0x900006cc 12"]
DUT_WORDS = (("0x900008f8", 8), ("0x900008e0", 8), ("0x90000738", 4), ("0x90000748", 8), ("0x900008d4", 12))
TONE = "/tmp/a521-tone.raw"
SAMPLER = "/tmp/a521-sampler.sh"
PLAYLOG = "/tmp/a521-play.log"
CAPLOG = "/tmp/a521-cap.log"
RAWT = time.clock_gettime_ns
MONO_RAW = time.CLOCK_MONOTONIC_RAW
STATE = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}


def _term(signum, frame):
    # a deadline's SIGTERM runs the teardown below rather than ending the process mid-case
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
name, case, durations, raw_root = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
assert case in ("SW", "CRFLL"), case
DUR = [float(x) for x in durations.split(",")]
assert len(DUR) == (3 if case == "SW" else 1), DUR
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
# playback long enough for every hold or window plus set-up, lock waits and the lock-loss observation
PLAY_S = int(sum(DUR) + 420)
SAMPLES = int((sum(DUR) + 320) * 5)
aplay_line = f"aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {PLAY_S}"
arec_line = f"arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {PLAY_S}"
POLL_FILE = raw / "poll-run.jsonl"   # about 0.4 KB per poll: kept outside the packet
POLL_STOP = raw / "poll.stop"


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), mono_raw_ns=RAWT(MONO_RAW), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


def run(args, limit, **kw):
    return subprocess.run(args, timeout=limit + 5, **kw)


def dut(tag):
    r = run(["python3", "-B", str(TOOLS / "console_read.py"), DUT, str(dest / f"dut-{tag}.txt"), *DUT_READS], 60,
            capture_output=True, text=True)
    words = {}
    try:
        txt = (dest / f"dut-{tag}.txt").read_text(errors="replace")
        for addr, n in DUT_WORDS:
            i = txt.index(f"cmd='mem_read {addr} {n}'")
            line = txt[i:].split("Memory dump:\n", 1)[1].splitlines()[0].split()
            b = bytes(int(h, 16) for h in line[1:1 + n])
            base = int(addr, 16)
            for k in range(0, n, 4):
                words[f"{base + k - 0x90000000:#05x}"] = f"{struct.unpack('<I', b[k:k + 4])[0]:08x}"
    except (ValueError, IndexError):
        pass
    event("dut", tag=tag, rc=r.returncode, words=words)
    return words


class Poll:
    """The one console poll of the case (console_poll_b8.py), read back here as it grows."""

    def __init__(self, max_s):
        self.p = subprocess.Popen(["python3", "-B", str(TOOLS / "console_poll_b8.py"), DUT, str(POLL_FILE),
                                   str(max_s), "0.5", f"file:{POLL_STOP}"])
        event("poll-start", file=POLL_FILE.name, max_s=max_s, period_s=0.5)
        self.rows = []
        self.fh = None
        self.buf = ""

    def refresh(self):
        if self.fh is None:
            if not POLL_FILE.exists():
                return
            self.fh = open(POLL_FILE)
        self.buf += self.fh.read()
        while "\n" in self.buf:
            line, self.buf = self.buf.split("\n", 1)
            if line.startswith("{"):
                self.rows.append(json.loads(line))

    def wait_state(self, state, since_raw, max_s, tag):
        """First poll that started after since_raw and reads `state`; the interval from the poll
        before it is the resolution. Returns seconds (lo, hi) after since_raw, or None."""
        end = time.monotonic() + max_s
        while time.monotonic() < end:
            self.refresh()
            prev = None
            for r in self.rows:
                if r["raw0"] < since_raw:
                    continue
                if r.get("servo_state") == state:
                    lo = (prev["raw1"] - since_raw) / 1e9 if prev else 0.0
                    hi = (r["raw1"] - since_raw) / 1e9
                    event("servo-state", tag=tag, state=STATE[state], s_lo=round(lo, 3), s_hi=round(hi, 3), poll_n=r["n"])
                    return lo, hi
                prev = r
            if self.p.poll() is not None:
                break
            time.sleep(0.2)
        event("servo-state", tag=tag, state=STATE[state], s_lo=None, s_hi=None, timeout_s=max_s)
        return None

    def stop(self):
        POLL_STOP.touch()
        try:
            self.p.wait(15)
        except subprocess.TimeoutExpired:
            self.p.kill()
            self.p.wait(5)
        self.refresh()
        event("poll-end", rc=self.p.returncode, polls=len(self.rows))


def soc(tag, limit, cmd):
    r = run(["python3", "-B", str(TOOLS / "soccon_net.py"), SOC, str(dest / f"soc-{tag}.log"), str(limit), cmd],
            limit + 40, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


class Reader(threading.Thread):
    """Reads the capture pipe; keeps the tone pair; stamps reads; decodes the tone online."""

    def __init__(self, proc):
        super().__init__(daemon=True)
        self.proc = proc
        self.out = open(raw / "cap-lr.raw", "wb")
        self.ts = open(raw / "cap-ts.bin", "wb")  # <q frames_after_read, d realtime, q monotonic_raw_ns>
        self.full = None
        self.full_left = 0
        self.lock = threading.Lock()
        self.total = 0
        self.run_start = None
        self.tab = T.table()
        self.err = None

    def keep_full(self, seconds):
        with self.lock:
            if self.full is None:
                self.full = open(raw / "cap-all.raw", "wb")
                self.full_left = int(seconds * FS)
                event("full-snippet", start_frame=self.total, frames=self.full_left)

    def run(self):
        fd = self.proc.stdout.fileno()
        rem = b""
        fb = NCH * 3
        last_ord = None
        try:
            while True:
                d = os.read(fd, 1 << 16)
                if not d:
                    break
                t_raw, t_rt = RAWT(MONO_RAW), time.time()
                d = rem + d
                n = len(d) // fb
                rem = d[n * fb:]
                if n == 0:
                    continue
                a = np.frombuffer(d[:n * fb], dtype=np.uint8).reshape(n, NCH, 3)
                lr = np.ascontiguousarray(a[:, [CAP_L, CAP_R], :])
                self.out.write(lr.tobytes())
                v = lr[:, :, 0].astype(np.int64) | (lr[:, :, 1].astype(np.int64) << 8) | (lr[:, :, 2].astype(np.int64) << 16)
                v = np.where(v >= 1 << 23, v - (1 << 24), v)
                o = T.decode(v[:, 0], v[:, 1], self.tab)
                # online: a frame is good when it decodes and follows its predecessor in order
                prev = np.concatenate(([-2 if last_ord is None else last_ord], o[:-1]))
                good = (o >= 0) & (prev >= 0) & (((o - prev) % T.N) == 1)
                last_ord = int(o[-1])
                with self.lock:
                    base = self.total
                    if self.full is not None and self.full_left > 0:
                        k = min(n, self.full_left)
                        self.full.write(d[:k * fb])
                        self.full_left -= k
                        if self.full_left == 0:
                            self.full.close()
                    p = 1 if self.run_start is not None else 0
                    st = np.diff(np.concatenate(([p], good.astype(np.int8))))
                    for i in np.flatnonzero(st):
                        self.run_start = base + int(i) if st[i] > 0 else None
                    self.total = base + n
                self.ts.write(struct.pack("<qdq", self.total, t_rt, t_raw))
        except Exception as e:  # recorded, never raised into the run
            self.err = repr(e)
        finally:
            self.out.close()
            self.ts.close()

    def state(self):
        with self.lock:
            return self.total, self.run_start


class SampleRx(threading.Thread):
    """Receives the board's timing sample lines; stamps each chunk on CLOCK_MONOTONIC_RAW."""

    def __init__(self):
        super().__init__(daemon=True)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((HOST, 0))
        self.s.listen(1)
        self.s.settimeout(1.0)
        self.port = self.s.getsockname()[1]
        self.f = open(raw / "samples.txt", "w")
        self.lines = 0
        self.stop = False
        self.conns = 0

    def run(self):
        while not self.stop:
            try:
                c, peer = self.s.accept()
            except socket.timeout:
                continue
            self.conns += 1
            c.settimeout(1.0)
            buf = b""
            while not self.stop:
                try:
                    d = c.recv(4096)
                except socket.timeout:
                    continue
                t = RAWT(MONO_RAW)
                if not d:
                    break
                buf += d
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    self.f.write(f"{t}\t{line.decode(errors='replace')}\n")
                    self.lines += 1
                self.f.flush()
            c.close()
        self.f.close()


class Agent:
    def __init__(self):
        self.p = subprocess.Popen(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", CTL,
             f"cd /tmp/a521 && sudo -n timeout {PLAY_S + 600} python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(dest / "agent-stderr.txt", "w"),
            text=True, bufsize=1)
        self.log = open(dest / "ctl.jsonl", "a", buffering=1)
        self.n = 0
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


def clk_of(rows, what):
    # GET_CLOCK_SOURCE response payload: descriptor_type, descriptor_index, clock_source_index
    for r in rows:
        if r.get("what") == what and r.get("status") == "SUCCESS":
            return int(r["payload"][8:12], 16)
    return None


EID = {"dut": DUT_EID, "peer": PEER_EID}
fmt_set = []        # (who, idx, as_found) listener formats this case set


def binding_rule(ag, talker, listener, tag):
    """Owner rule: read both formats; if they differ, set the LISTENER's to the talker's; read back."""
    (tw, ti), (lw, li) = talker, listener
    t = fmt_of(ag.cmd(op="fmt", who=tw, dir="out", idx=ti))
    l0 = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
    rec = dict(tag=tag, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", talker_fmt=t, listener_fmt=l0,
               set=None, listener_after=l0)
    if t is None or l0 is None:
        event("format-check", ok=False, **rec)
        raise SystemExit("format read failed")
    if t != l0:
        if not any(w == lw and i == li for w, i, _ in fmt_set):
            fmt_set.append((lw, li, l0))
        s = ag.cmd(op="setfmt", who=lw, idx=li, fmt=t)
        rec["set"] = dict(fmt=t, status=[r.get("status") for r in s], echoed=fmt_of(s))
        rec["listener_after"] = fmt_of(ag.cmd(op="fmt", who=lw, dir="in", idx=li))
        if rec["listener_after"] != t:
            event("format-check", ok=False, **rec)
            raise SystemExit("STOP: the listener did not take the talker's format")
    event("format-check", ok=True, **rec)
    return rec


def acmp(ag, op, talker, listener):
    (tw, ti), (lw, li) = talker, listener
    rows = ag.cmd(op=op, t=EID[tw], tu=ti, l=EID[lw], lu=li)
    main = next((r for r in rows if r.get("what") == op), {})
    after = next((r for r in rows if r.get("what") == "rx-state-after"), {})
    event(op, talker=f"{tw}-out-{ti}", listener=f"{lw}-in-{li}", status=main.get("status"),
          conn_count=after.get("conn_count"), stream_id=after.get("stream_id"), flags=after.get("flags"))
    return main.get("status") == 0


def setclk(ag, who, src, tag):
    rows = ag.cmd(op="setclk", who=who, src=src)
    st = next((r.get("status") for r in rows if r.get("cmd") == "SET_CLOCK_SOURCE"), None)
    back = clk_of(rows, f"clock-{who}")
    event("set-clock", tag=tag, who=who, src=src, status=st, readback=back, ok=back == src)
    return st, back


def counters(ag, tag, items):
    """GET_COUNTERS (read-only) on (who, dtype, idx) items; the payloads are kept in ctl.jsonl."""
    got = {}
    for who, dt, i in items:
        rows = ag.cmd(op="counters", who=who, dtype=dt, idx=i)
        r = rows[0] if rows else {}
        got[f"{who}-{dt:#06x}-{i}"] = r.get("payload") if r.get("status") == "SUCCESS" else r.get("status")
    event("counters", tag=tag, payloads=got)
    return got


def clock_read(ag, tag):
    src = clk_of(ag.cmd(op="clk", who="dut"), "clock-dut")
    event("clock-read", tag=tag, source=src)
    return src


def wait_valid(rd, f0, cap_s):
    end = time.monotonic() + cap_s
    while time.monotonic() < end:
        total, rs = rd.state()
        if rs is not None and rs >= f0 and total - rs >= MIN_RUN:
            return rs
        time.sleep(0.05)
    return None


def frames_now(rd):
    return rd.state()[0]


def sleep_until(t_mono):
    while time.monotonic() < t_mono:
        time.sleep(0.2)


SAMPLER_SH = r"""#!/bin/bash
# Lane B8 timing sampler (lane B6's): McASP0 playback and capture PCM status (@SAMPLES@ samples, 5 per second).
exec 3>/dev/tcp/@HOST@/PORT || exit 1
n=0
while [ $n -lt @SAMPLES@ ]; do
  sp=none; hp=-1; sc=none; hc=-1; gp=-1; gc=-1
  # whole-file reads (a line-by-line read re-seeks this file and can lose lines)
  t0=$EPOCHREALTIME
  IFS= read -r -d '' x < /proc/asound/card0/pcm0p/sub0/status
  t1=$EPOCHREALTIME
  IFS= read -r -d '' y < /proc/asound/card0/pcm0c/sub0/status
  t2=$EPOCHREALTIME
  [[ $x =~ state:\ ([A-Z_]+) ]] && sp=${BASH_REMATCH[1]}
  [[ $x =~ hw_ptr\ *:\ ([0-9]+) ]] && hp=${BASH_REMATCH[1]}
  [[ $x =~ trigger_time:\ ([0-9.]+) ]] && gp=${BASH_REMATCH[1]}
  [[ $y =~ state:\ ([A-Z_]+) ]] && sc=${BASH_REMATCH[1]}
  [[ $y =~ hw_ptr\ *:\ ([0-9]+) ]] && hc=${BASH_REMATCH[1]}
  [[ $y =~ trigger_time:\ ([0-9.]+) ]] && gc=${BASH_REMATCH[1]}
  printf 'S %d %s %s %s %s %s %s %s %s %s\n' $n $t0 $t1 $t2 $sp $hp $sc $hc $gp $gc >&3 || exit 2
  n=$((n+1))
  sleep 0.2
done
printf 'END %d\n' $n >&3
""".replace("@SAMPLES@", str(SAMPLES)).replace("@HOST@", HOST)

T_LOOP = T.raw_bytes()
tone_sha = hashlib.sha256(T_LOOP).hexdigest()
serve = raw / "serve"
serve.mkdir()
(serve / "tone.raw").write_bytes(T_LOOP)
event("start", name=name, case=case, durations=DUR, play_s=PLAY_S, samples=SAMPLES, tone_sha256=tone_sha,
      tone_frames=T.N, settle_s=SETTLE_S)

# GET_COUNTERS items read at every mark: the DUT's CLOCK_DOMAIN, both talkers and both listeners,
# and the peer's listener of the DUT's AAF stream
CTR = [("dut", 0x0024, 0), ("dut", 0x0006, 0), ("dut", 0x0006, 1), ("peer", 0x0005, 0),
       ("dut", 0x0005, 0), ("dut", 0x0005, 1)]

ag = rd = cap = srv = srx = pl = None
fetched = mapped = played = sampling = False
found = {}
binds = []          # (talker, listener) bound by this case
clk_changed = []    # (who, as_found)
try:
    srx = SampleRx()
    srx.start()
    (serve / "sampler.sh").write_text(SAMPLER_SH.replace("PORT", str(srx.port)))
    samp_sha = hashlib.sha256((serve / "sampler.sh").read_bytes()).hexdigest()
    srv = hostsrv.FileServer(serve, 0)
    hport = srv.srv.server_address[1]
    rc = soc("fetch", 120, f"cat /proc/uptime; wget -q -O {TONE} http://{HOST}:{hport}/tone.raw; echo wget_rc=$?; "
                           f"wget -q -O {SAMPLER} http://{HOST}:{hport}/sampler.sh; echo wget2_rc=$?; "
                           f"wc -c < {TONE}; df -k /tmp | tail -1; echo '{tone_sha}  {TONE}' | sha256sum -c && "
                           f"echo '{samp_sha}  {SAMPLER}' | sha256sum -c")
    fetched = True
    if rc != 0:
        raise SystemExit(f"tone or sampler fetch/check failed on the SoC board (rc {rc})")
    ag = Agent()
    ag.sync(5)
    # as-found state
    for who, d, i in (("peer", "in", 0), ("dut", "in", 0), ("dut", "in", 1),
                      ("dut", "out", 0), ("dut", "out", 1), ("peer", "out", 0), ("peer", "out", 2)):
        found[f"fmt-{who}-{d}-{i}"] = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=i))
    for who in ("peer", "dut"):
        found[f"clk-{who}"] = clk_of(ag.cmd(op="clk", who=who), f"clock-{who}")
    for who, i in (("peer", 0), ("dut", 0), ("dut", 1)):
        rows = ag.cmd(op="rx", who=who, idx=i)
        found[f"rx-{who}-{i}"] = {k: rows[0].get(k) for k in ("status", "conn_count", "stream_id")} if rows else None
    event("as-found", **found)
    if any((found.get(f"rx-{w}-{i}") or {}).get("conn_count") for w, i in (("peer", 0), ("dut", 0), ("dut", 1))):
        raise SystemExit("a listener this case uses is already bound: not this lane's state, nothing changed")
    if found["clk-peer"] != 0 or found["clk-dut"] != 0:
        raise SystemExit(f"clock sources not as recorded at the start (peer {found['clk-peer']}, dut {found['clk-dut']})")
    ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
    mapped = True
    rows = ag.cmd(op="map", act="add", dtype=0x000F, didx=0, n=8)
    event("map-add", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
    counters(ag, "before-bind", CTR)
    cap = subprocess.Popen(["timeout", "-s", "INT", str(PLAY_S + 300), "arecord", "-D", f"hw:{CARD},0", "-f", CAP_FMT,
                            "-r", str(FS), "-c", str(NCH), "-t", "raw", f"--period-size={CAP_PERIOD}",
                            f"--buffer-size={CAP_BUFFER}", "-v", "-"],
                           stdout=subprocess.PIPE, stderr=open(raw / "arecord.log", "w"))
    rd = Reader(cap)
    rd.start()
    event("capture-started")
    time.sleep(2.0)
    rc = soc("play-start", 40, f"cat /proc/uptime; "
                               f"nohup sh -c 'while cat {TONE}; do :; done | {aplay_line}; echo aplay_rc=$?' "
                               f"> {PLAYLOG} 2>&1 < /dev/null & "
                               f"nohup sh -c '{arec_line} > /dev/null; echo arecord_rc=$?' > {CAPLOG} 2>&1 < /dev/null & "
                               f"sleep 1; ps -o pid,args | grep -E '[a]play|[a]record|[c]at {TONE}'; cat /proc/uptime")
    played = True
    if rc != 0:
        raise SystemExit(f"playback start failed (rc {rc})")
    rc = soc("sampler-start", 30, f"nohup bash {SAMPLER} > /dev/null 2>&1 < /dev/null & sleep 1; "
                                  f"ps -o pid,args | grep '[b]ash {SAMPLER}'")
    sampling = True
    dut("before-bind")
    # AAF bind, DUT talker -> peer listener (the tone path)
    aaf = (("dut", 0), ("peer", 0))
    binding_rule(ag, *aaf, "aaf")
    ag.sync(3)
    f0 = frames_now(rd)
    if not acmp(ag, "bind", *aaf):
        raise SystemExit("AAF bind failed")
    binds.append(aaf)
    ag.sync(3)
    rs = wait_valid(rd, f0, 30.0)
    event("initial-valid", frame=rs, f0=f0)
    if rs is None:
        raise SystemExit("no valid tone within 30 s of the AAF bind")
    rd.keep_full(10.0)
    # the one console poll of the case, from before the case's binds
    pl = Poll(PLAY_S + 200)
    time.sleep(3.0)
    extra = {"SW": [(("peer", 2), ("dut", 1), "crf"), (("peer", 0), ("dut", 0), "peer-aaf")],
             "CRFLL": [(("peer", 2), ("dut", 1), "crf")]}[case]
    event("binds-begin", frame=frames_now(rd))
    for talker, listener, tag in extra:
        binding_rule(ag, talker, listener, tag)
        if not acmp(ag, "bind", talker, listener):
            raise SystemExit(f"{tag} bind failed")
        binds.append((talker, listener))
    event("binds-end", frame=frames_now(rd))
    time.sleep(2.0)
    counters(ag, "after-binds", CTR)
    if case == "SW":
        phases = [("aaf1", 2, DUR[0]), ("crf", 1, DUR[1]), ("aaf2", 2, DUR[2])]
        for k, (tag, src, hold) in enumerate(phases):
            counters(ag, f"{tag}-before-set", CTR)
            clock_read(ag, f"{tag}-before-set")
            ag.sync(3)
            event("switch", tag=tag, src=src, frame=frames_now(rd))
            if k == 0:
                clk_changed.append(("dut", found["clk-dut"]))
            t_set = RAWT(MONO_RAW)
            t_set_mono = time.monotonic()
            st, back = setclk(ag, "dut", src, tag)
            if back != src:
                raise SystemExit(f"clock source set refused or not read back ({st}, {back})")
            lk = pl.wait_state(4, t_set, 120.0, tag)
            t_lock = time.monotonic()
            event("phase-locked", tag=tag, frame=frames_now(rd))
            if lk is None:
                raise SystemExit(f"{tag}: the DUT's media-clock servo did not read LOCKED within 120 s")
            counters(ag, f"{tag}-locked", CTR)
            clock_read(ag, f"{tag}-locked")
            if k == 0:
                # the graded span starts SETTLE_S after the first set and LOCKED (lane B7's window start)
                sleep_until(max(t_set_mono + SETTLE_S, t_lock))
                event("window-start", frame=frames_now(rd), samples=srx.lines)
            sleep_until(t_lock + hold / 2)
            counters(ag, f"{tag}-mid", CTR)
            clock_read(ag, f"{tag}-mid")
            sleep_until(t_lock + hold - 5)
            counters(ag, f"{tag}-end", CTR)
            clock_read(ag, f"{tag}-end")
            ag.sync(3)
            sleep_until(t_lock + hold)
            event("phase-end", tag=tag, frame=frames_now(rd))
        event("window-end", frame=frames_now(rd), samples=srx.lines)
    else:
        ag.sync(3)
        event("switch", tag="crf", src=1, frame=frames_now(rd))
        clk_changed.append(("dut", found["clk-dut"]))
        t_set = RAWT(MONO_RAW)
        t_set_mono = time.monotonic()
        st, back = setclk(ag, "dut", 1, "case")
        if back != 1:
            raise SystemExit(f"clock source set refused or not read back ({st}, {back})")
        lk = pl.wait_state(4, t_set, 120.0, "crf")
        if lk is None:
            raise SystemExit("the DUT's media-clock servo did not read LOCKED within 120 s")
        sleep_until(t_set_mono + SETTLE_S)
        counters(ag, "window-mark-0", CTR)
        clock_read(ag, "window-mark-0")
        t_c0 = time.monotonic()
        event("window-start", frame=frames_now(rd), samples=srx.lines)
        W = DUR[0]
        for k, m in enumerate((W / 2, W - 15)):
            sleep_until(t_c0 + m)
            counters(ag, f"window-mark-{k + 1}", CTR)
            clock_read(ag, f"window-mark-{k + 1}")
            ag.sync(3)
        sleep_until(t_c0 + W)
        event("window-end", frame=frames_now(rd), samples=srx.lines)
        # assignment item 3: lock loss of the followed CRF talker, after the graded window
        peer_crf = (("peer", 2), ("dut", 1))
        event("lockloss-begin", frame=frames_now(rd))
        counters(ag, "ll-before", CTR)
        clock_read(ag, "ll-before")
        ag.sync(3)
        time.sleep(1.5)
        event("ll-unbind", frame=frames_now(rd))
        t_unb = RAWT(MONO_RAW)
        t_unb_mono = time.monotonic()
        acmp(ag, "unbind", *peer_crf)
        binds.remove(peer_crf)
        pl.wait_state(5, t_unb, 10.0, "ll-holdover")
        sleep_until(t_unb_mono + 9.5)
        counters(ag, "ll-holdover", CTR)
        clock_read(ag, "ll-holdover")
        binding_rule(ag, *peer_crf, "peer-crf-rebind")
        ag.sync(3)
        sleep_until(t_unb_mono + 11.0)
        event("ll-rebind", frame=frames_now(rd))
        t_reb = RAWT(MONO_RAW)
        ok = acmp(ag, "bind", *peer_crf)
        if ok:
            binds.append(peer_crf)
        lk = pl.wait_state(4, t_reb, 90.0, "ll-return")
        t_ret = time.monotonic()
        sleep_until(t_ret + 10.0)
        counters(ag, "ll-after", CTR)
        clock_read(ag, "ll-after")
        event("lockloss-end", frame=frames_now(rd))
finally:
    event("teardown")
    if ag is not None:
        try:
            ag.sync(3)
            # the DUT's clock source first, read back; the poll still runs and records the return
            for w, src0 in clk_changed:
                if src0 is not None:
                    setclk(ag, w, src0, "restore")
            for who in ("peer", "dut"):
                event("clock-final", who=who, source=clk_of(ag.cmd(op="clk", who=who), f"clock-{who}"),
                      as_found=found.get(f"clk-{who}"))
            for tl in reversed(binds):
                acmp(ag, "unbind", *tl)
            binds.clear()
            time.sleep(2.0)
        except BaseException as e:
            event("teardown-error", stage="clock-unbind", error=repr(e))
    if pl is not None:
        time.sleep(3.0)
        pl.stop()
    if sampling or played:
        soc("stop", 60, f"cat /proc/uptime; for pat in '[b]ash {SAMPLER}' '[a]record -D hw:0,0' '[a]play -v -D hw:0,0'; do "
                        f"for p in $(ps -o pid,args | grep \"$pat\" | awk '{{print $1}}'); do "
                        f"A=$(tr '\\0' ' ' < /proc/$p/cmdline); echo \"$p: $A\"; "
                        f"if [ \"$A\" = 'bash {SAMPLER} ' ] || [ \"$A\" = '{arec_line} ' ] || [ \"$A\" = '{aplay_line} ' ]; "
                        f"then kill $p; echo KILLED $p; else echo MISMATCH $p; fi; done; done; sleep 2; "
                        f"ps -o pid,args | grep -E '[a]play|[a]record|[c]at {TONE}|[a]521-sampler'; echo PS_RC=$?; "
                        f"cat {PLAYLOG} {CAPLOG}; for s in /proc/asound/card0/pcm0*/sub0/status; do head -2 $s; done")
    if ag is not None:
        try:
            for who, i, f in fmt_set:
                s = ag.cmd(op="setfmt", who=who, idx=i, fmt=f)
                event("format-restore", who=who, idx=i, fmt=f, status=[r.get("status") for r in s])
            for key in ("fmt-peer-in-0", "fmt-dut-in-0", "fmt-dut-in-1"):
                _, who, d, i = key.split("-")
                back = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=int(i)))
                event("format-final", key=key, fmt=back, equal_to_found=back == found.get(key))
            if mapped:
                rows = ag.cmd(op="map", act="remove", dtype=0x000F, didx=0, n=8)
                event("map-remove", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
                rows = ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
                event("map-final", readback=rows[-1].get("payload") if rows else None)
            for who, i in (("peer", 0), ("dut", 0), ("dut", 1)):
                rows = ag.cmd(op="rx", who=who, idx=i)
                event("rx-final", who=who, idx=i, conn_count=rows[0].get("conn_count") if rows else None)
            ag.cmd(op="tx", who="dut", idx=0)
            ag.cmd(op="tx", who="dut", idx=1)
            ag.cmd(op="tx", who="peer", idx=0)
            ag.cmd(op="tx", who="peer", idx=2)
            counters(ag, "final", CTR)
            ag.sync(3)
        except BaseException as e:
            event("teardown-error", stage="formats-maps", error=repr(e))
        ag.quit()
    time.sleep(1.0)
    if cap is not None:
        cap.send_signal(2)
        try:
            cap.wait(10)
        except subprocess.TimeoutExpired:
            cap.kill()
            cap.wait(5)
        event("capture-exit", rc=cap.returncode)
    if rd is not None:
        rd.join(10)
        event("reader", frames=rd.total, error=rd.err)
    if srx is not None:
        srx.stop = True
        srx.join(5)
        event("samples", lines=srx.lines, connections=srx.conns)
    dut("final")
    if fetched:
        soc("cleanup", 30, f"rm -f {TONE} {SAMPLER} {PLAYLOG} {CAPLOG}; ls /tmp")
    if srv is not None:
        srv.close()
    for f in sorted(raw.rglob("*")):
        if f.is_file():
            h = hashlib.sha256()
            with open(f, "rb") as fh:
                for blk in iter(lambda: fh.read(1 << 22), b""):
                    h.update(blk)
            event("raw-file", file=str(f.relative_to(raw)), bytes=f.stat().st_size, sha256=h.hexdigest())
    event("end")

#!/usr/bin/env python3
"""One lane B9 case (this host; the caller holds the bench lock for the whole case).

usage: run_b9.py <name> <case> <window_s> <raw_root>
  case B0:   the DUT on INTERNAL (control)
  case BCRF: the DUT's CLOCK_DOMAIN set to CLOCK_SOURCE 1, the peer's CRF stream
  case BAAF: the DUT's CLOCK_DOMAIN set to CLOCK_SOURCE 2, the peer's AAF stream

Lane B8's run_b8.py (lane B7's run_b7.py with the console poll), unchanged in method: the B6
tone loop played into McASP0 on the SoC board, the DUT's AAF talker to the peer's listener, the
external capture of the peer's output, the McASP0 timing sampler, the binding rule, the
clock-source rule, the console poll every 0.5 s, the GET_COUNTERS marks and the restore. Lane B9
changes:
  * the cases are lane B7's B0, B-CRF and B-AAF, with one set of binds for all three: the
    DUT's AAF talker to the peer's STREAM_INPUT 0 (the Direction A tone path, for lane B7's
    frame-rate ratio), the peer's CRF talker to the DUT's STREAM_INPUT 1 and the peer's AAF
    talker to the DUT's STREAM_INPUT 0, each under the binding rule; the cases differ only in
    the DUT's clock source (lane B7: B-CRF bound the CRF only, B-AAF the AAF only);
  * four identity mappings on the DUT's STREAM_PORT_INPUT 0 (lane B7's probe), so the peer's
    talker channels, which carry the Direction B tone, are rendered on TDM slots 0 to 3;
  * McASP0's capture of the DUT's TDM output (the board's arecord, which lanes B6 to B8 sent to
    /dev/null) streams over the board link to a receiver here (McaspRx): it keeps channels 0 to
    3 (mcasp-ch0-3.raw), the first 10 s of all eight after the binds (mcasp-all-10s.raw), the
    non-zero word count of channels 4 to 7 over the whole stream, the stream's SHA-256 and each
    read's arrival time (mcasp-ts.bin); arecord asks for a 1 s buffer (-B 1000000);
  * the tone source's playback status is read from /proc every 0.2 s through the case
    (tone-status.jsonl; passive), so a playback restart, which would put a discontinuity into
    the tone before the peer, is timed; the case refuses to start unless the tone plays;
  * the external capture's two tone channels are identified by content once the tone is valid,
    as lane B6 did (the 997 Hz loop's values on one, the 9,973 Hz loop's on the other, the pair
    decoding); the indices go to the private directory (B9_PRIV), not to the events;
  * the window: from SETTLE_S after the last bind (B0) or after the set (B-CRF, B-AAF), and not
    before the servo reads LOCKED, for <window_s>; GET_COUNTERS and GET_CLOCK_SOURCE at its
    start, middle and 15 s before its end (lane B8's CRF window);
  * board files are /tmp/a526-*, the controller staging /tmp/a526, the agent b8_ctl.py.

Teardown, always: as lane B8, with both DUT maps removed and read back.

Grading is offline (grade_b9.py: the Direction A tone path, lane B7's; b9_thdn.py: the
Direction B tone). Environment (private): SOC_CONSOLE, DUT_CONSOLE, CTL_HOST, CTL_IFACE,
PEER_EID, PEER_MAC, CAP_CARD, ECM_HOST, CAP_NCH, CAP_FMT, TONE_PROC, B9_PRIV.
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
NCH, CAP_FMT = int(os.environ["CAP_NCH"]), os.environ["CAP_FMT"]
TONE_PROC, PRIV = os.environ["TONE_PROC"], Path(os.environ["B9_PRIV"])
BPS = 3  # the Reader decodes three-byte little-endian samples (the decode is generic, not masked)
DUT_EID = "020000fffe000001"
FS = 48000
CAP_PERIOD, CAP_BUFFER = 480, 24000
MIN_RUN = 480
SETTLE_S = 20.0
DUT_READS = ["milan_status", "milan_nvm", "mem_read 0x90000738 4", "mem_read 0x90000748 8", "mem_read 0x900008d4 12",
             "mem_read 0x900008f8 8", "mem_read 0x900008e0 8", "mem_read 0x90000660 20", "mem_read 0x90000694 8",
             "mem_read 0x900006cc 12"]
DUT_WORDS = (("0x900008f8", 8), ("0x900008e0", 8), ("0x90000738", 4), ("0x90000748", 8), ("0x900008d4", 12))
TONE = "/tmp/a526-tone.raw"
SAMPLER = "/tmp/a526-sampler.sh"
PLAYLOG = "/tmp/a526-play.log"
CAPLOG = "/tmp/a526-cap.log"
RAWT = time.clock_gettime_ns
MONO_RAW = time.CLOCK_MONOTONIC_RAW
STATE = {0: "IDLE", 1: "VERIFY", 2: "REPAIR", 3: "ACQUIRE", 4: "LOCKED", 5: "HOLDOVER", 6: "FAULT"}
SRC = {"B0": None, "BCRF": 1, "BAAF": 2}


def _term(signum, frame):
    # a deadline's SIGTERM runs the teardown below rather than ending the process mid-case
    raise SystemExit(f"signal {signum}")


signal.signal(signal.SIGTERM, _term)
name, case, window_s, raw_root = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
assert case in SRC, case
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
# playback and capture long enough for the window plus set-up, the lock wait and the teardown
PLAY_S = int(window_s + 200)
SAMPLES = int((window_s + 150) * 5)
aplay_line = f"aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {PLAY_S}"
arec_line = f"arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -B 1000000 -d {PLAY_S}"
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


def words24(a):
    v = a[..., 0].astype(np.int64) | (a[..., 1].astype(np.int64) << 8) | (a[..., 2].astype(np.int64) << 16)
    return np.where(v >= 1 << 23, v - (1 << 24), v)


class Reader(threading.Thread):
    """Reads the external capture's pipe; finds the tone pair's two channels by content (lane B6);
    keeps the pair; stamps reads; decodes the tone online."""

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
        lp = T.loop()
        self.sets = (np.unique(lp[:, 0]), np.unique(lp[:, 1]))
        self.pair = None
        self.pending = []   # all-channel chunks held until the pair is identified
        self.since_try = 0
        self.err = None

    def keep_full(self, seconds):
        with self.lock:
            if self.full is None:
                self.full = open(raw / "cap-all.raw", "wb")
                self.full_left = int(seconds * FS)
                event("full-snippet", start_frame=self.total, frames=self.full_left)

    def identify(self):
        """The tone pair from the last 4,800 frames held: each channel's share of each loop's values."""
        a = np.concatenate(self.pending[-12:])
        if len(a) < 4800:
            return None
        v = words24(a[-4800:])
        share = [[float(np.isin(v[:, c], s).mean()) if np.any(v[:, c]) else 0.0 for c in range(NCH)]
                 for s in self.sets]
        c0, c1 = int(np.argmax(share[0])), int(np.argmax(share[1]))
        if share[0][c0] < 0.99 or share[1][c1] < 0.99 or c0 == c1:
            return None
        if (T.decode(v[:, c0], v[:, c1], self.tab) >= 0).mean() < 0.99:
            return None
        return c0, c1

    def run(self):
        fd = self.proc.stdout.fileno()
        rem = b""
        fb = NCH * BPS
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
                a = np.frombuffer(d[:n * fb], dtype=np.uint8).reshape(n, NCH, BPS)
                if self.pair is None:
                    self.pending.append(a)
                    self.since_try += n
                    got = None
                    if self.since_try >= 9600:   # one attempt per 0.2 s of audio
                        self.since_try = 0
                        got = self.identify()
                    if got is None:
                        with self.lock:
                            self.total += n
                        self.ts.write(struct.pack("<qdq", self.total, t_rt, t_raw))
                        continue
                    self.pair = got
                    (PRIV / f"{name}-capture-pair.json").write_text(json.dumps(dict(pair=got, at_frame=self.total)))
                    event("capture-identified", at_frame=self.total)
                    if len(self.pending) > 1:
                        held = np.concatenate(self.pending[:-1])
                        self.out.write(np.ascontiguousarray(held[:, list(got), :]).tobytes())
                    self.pending = None
                lr = np.ascontiguousarray(a[:, list(self.pair), :])
                self.out.write(lr.tobytes())
                v = words24(lr)
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
            if self.pair is None:
                self.err = (self.err or "") + " the tone pair was never identified"
            self.out.close()
            self.ts.close()

    def state(self):
        with self.lock:
            return self.total, self.run_start


class McaspRx(threading.Thread):
    """Receives McASP0's capture of the DUT's TDM output (8 channels, S32_LE) over the board link."""

    def __init__(self):
        super().__init__(daemon=True)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8 << 20)
        self.s.bind((HOST, 0))
        self.s.listen(1)
        self.s.settimeout(1.0)
        self.port = self.s.getsockname()[1]
        self.lock = threading.Lock()
        self.total = 0
        self.bytes = 0
        self.nz47 = np.zeros(4, dtype=np.int64)
        self.sha = hashlib.sha256()
        self.full = None
        self.full_left = 0
        self.stop = False
        self.conns = 0
        self.err = None

    def keep_full(self, seconds):
        with self.lock:
            if self.full is None:
                self.full = open(raw / "mcasp-all-10s.raw", "wb")
                self.full_left = int(seconds * FS)
                event("mcasp-full-snippet", start_frame=self.total, frames=self.full_left)

    def run(self):
        out = open(raw / "mcasp-ch0-3.raw", "wb")
        ts = open(raw / "mcasp-ts.bin", "wb")  # <q frames_after_read, q monotonic_raw_ns>
        try:
            while not self.stop:
                try:
                    c, _ = self.s.accept()
                except socket.timeout:
                    continue
                self.conns += 1
                c.settimeout(1.0)
                rem = b""
                while not self.stop:
                    try:
                        d = c.recv(1 << 18)
                    except socket.timeout:
                        continue
                    t = RAWT(MONO_RAW)
                    if not d:
                        break
                    self.sha.update(d)
                    self.bytes += len(d)
                    d = rem + d
                    n = len(d) // 32
                    rem = d[n * 32:]
                    if n == 0:
                        continue
                    w = np.frombuffer(d[:n * 32], dtype="<i4").reshape(n, 8)
                    out.write(np.ascontiguousarray(w[:, :4]).tobytes())
                    with self.lock:
                        self.nz47 += np.count_nonzero(w[:, 4:], axis=0)
                        if self.full is not None and self.full_left > 0:
                            k = min(n, self.full_left)
                            self.full.write(d[:k * 32])
                            self.full_left -= k
                            if self.full_left == 0:
                                self.full.close()
                        self.total += n
                    ts.write(struct.pack("<qq", self.total, t))
                c.close()
                break
        except Exception as e:  # recorded, never raised into the run
            self.err = repr(e)
        finally:
            out.close()
            ts.close()
            if self.full is not None and not self.full.closed:
                self.full.close()

    def frames(self):
        with self.lock:
            return self.total


class ToneMon(threading.Thread):
    """The tone source's playback substream status every 0.2 s (read from /proc, passive)."""

    def __init__(self):
        super().__init__(daemon=True)
        self.f = open(raw / "tone-status.jsonl", "w")
        self.stop = False
        self.last = None

    def read(self):
        try:
            txt = open(TONE_PROC).read()
        except OSError as e:
            return dict(error=repr(e))
        r = {}
        for line in txt.splitlines():
            k, _, v = line.partition(":")
            if k.strip() in ("state", "trigger_time", "hw_ptr"):
                r[k.strip()] = v.strip()
        if not r:
            r["state"] = txt.strip()
        return r

    def run(self):
        while not self.stop:
            r = self.read()
            r["mono_raw_ns"] = RAWT(MONO_RAW)
            self.last = r
            self.f.write(json.dumps(r) + "\n")
            time.sleep(0.2)
        self.f.close()


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
             f"cd /tmp/a526 && sudo -n timeout {PLAY_S + 600} python3 -B b8_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
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


def marks():
    return dict(frame=frames_now(rd), mcasp_frame=mrx.frames(), samples=srx.lines)


def sleep_until(t_mono):
    while time.monotonic() < t_mono:
        time.sleep(0.2)


SAMPLER_SH = r"""#!/bin/bash
# Lane B9 timing sampler (lane B6's): McASP0 playback and capture PCM status (@SAMPLES@ samples, 5 per second).
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
event("start", name=name, case=case, window_s=window_s, play_s=PLAY_S, samples=SAMPLES, tone_sha256=tone_sha,
      tone_frames=T.N, settle_s=SETTLE_S)

# GET_COUNTERS items read at every mark: the DUT's CLOCK_DOMAIN, both talkers and both listeners,
# and the peer's listener of the DUT's AAF stream
CTR = [("dut", 0x0024, 0), ("dut", 0x0006, 0), ("dut", 0x0006, 1), ("peer", 0x0005, 0),
       ("dut", 0x0005, 0), ("dut", 0x0005, 1)]

ag = rd = cap = srv = srx = pl = mrx = tm = None
fetched = mapped_out = mapped_in = played = sampling = False
found = {}
binds = []          # (talker, listener) bound by this case
clk_changed = []    # (who, as_found)
try:
    # the Direction B tone must be playing before anything changes
    tm = ToneMon()
    tm.start()
    time.sleep(1.2)
    tone0 = dict(tm.last or {})
    time.sleep(1.0)
    tone1 = dict(tm.last or {})
    playing = (tone0.get("state") == "RUNNING" and tone1.get("state") == "RUNNING"
               and tone0.get("trigger_time") == tone1.get("trigger_time")
               and tone0.get("hw_ptr") != tone1.get("hw_ptr"))
    event("tone-check", playing=playing, state=tone1.get("state"))
    if not playing:
        raise SystemExit("the Direction B tone is not playing: nothing changed")
    srx = SampleRx()
    srx.start()
    mrx = McaspRx()
    mrx.start()
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
    for dt in (0x000F, 0x000E):
        rows = ag.cmd(op="map", act="get", dtype=dt, didx=0)
        found[f"map-{dt:#06x}"] = rows[-1].get("payload") if rows else None
    event("as-found", **found)
    if any((found.get(f"rx-{w}-{i}") or {}).get("conn_count") for w, i in (("peer", 0), ("dut", 0), ("dut", 1))):
        raise SystemExit("a listener this case uses is already bound: not this lane's state, nothing changed")
    if found["clk-peer"] != 0 or found["clk-dut"] != 0:
        raise SystemExit(f"clock sources not as recorded at the start (peer {found['clk-peer']}, dut {found['clk-dut']})")
    mapped_out = True
    rows = ag.cmd(op="map", act="add", dtype=0x000F, didx=0, n=8)
    event("map-add", dtype="0x000f", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
    mapped_in = True
    rows = ag.cmd(op="map", act="add", dtype=0x000E, didx=0, n=4)
    event("map-add", dtype="0x000e", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
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
                               f"nohup bash -c '{arec_line} > /dev/tcp/{HOST}/{mrx.port}; echo arecord_rc=$?' "
                               f"> {CAPLOG} 2>&1 < /dev/null & "
                               f"sleep 1; ps -o pid,args | grep -E '[a]play|[a]record|[c]at {TONE}'; cat /proc/uptime")
    played = True
    if rc != 0:
        raise SystemExit(f"playback start failed (rc {rc})")
    rc = soc("sampler-start", 30, f"nohup bash {SAMPLER} > /dev/null 2>&1 < /dev/null & sleep 1; "
                                  f"ps -o pid,args | grep '[b]ash {SAMPLER}'")
    sampling = True
    dut("before-bind")
    # AAF bind, DUT talker -> peer listener (the Direction A tone path)
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
    # the one console poll of the case, from before the peer's binds
    pl = Poll(PLAY_S + 200)
    time.sleep(3.0)
    event("binds-begin", **marks())
    for talker, listener, tag in ((("peer", 2), ("dut", 1), "crf"), (("peer", 0), ("dut", 0), "peer-aaf")):
        binding_rule(ag, talker, listener, tag)
        if not acmp(ag, "bind", talker, listener):
            raise SystemExit(f"{tag} bind failed")
        binds.append((talker, listener))
    event("binds-end", **marks())
    mrx.keep_full(10.0)
    t_ref_mono = time.monotonic()
    time.sleep(2.0)
    counters(ag, "after-binds", CTR)
    src = SRC[case]
    if src is not None:
        ag.sync(3)
        event("switch", tag=case.lower(), src=src, **marks())
        clk_changed.append(("dut", found["clk-dut"]))
        t_set = RAWT(MONO_RAW)
        t_ref_mono = time.monotonic()
        st, back = setclk(ag, "dut", src, "case")
        if back != src:
            raise SystemExit(f"clock source set refused or not read back ({st}, {back})")
        lk = pl.wait_state(4, t_set, 60.0, case.lower())
        if lk is None:
            raise SystemExit("the DUT's media-clock servo did not read LOCKED within 60 s")
    sleep_until(t_ref_mono + SETTLE_S)
    counters(ag, "window-mark-0", CTR)
    clock_read(ag, "window-mark-0")
    t_c0 = time.monotonic()
    event("window-start", **marks())
    for k, m in enumerate((window_s / 2, window_s - 15)):
        sleep_until(t_c0 + m)
        counters(ag, f"window-mark-{k + 1}", CTR)
        clock_read(ag, f"window-mark-{k + 1}")
        ag.sync(3)
    sleep_until(t_c0 + window_s)
    event("window-end", **marks())
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
                        f"ps -o pid,args | grep -E '[a]play|[a]record|[c]at {TONE}|[a]526-sampler'; echo PS_RC=$?; "
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
            for dt, n_, flag in ((0x000F, 8, mapped_out), (0x000E, 4, mapped_in)):
                if flag:
                    rows = ag.cmd(op="map", act="remove", dtype=dt, didx=0, n=n_)
                    event("map-remove", dtype=f"{dt:#06x}", status=[r.get("status") for r in rows],
                          readback=rows[-1].get("payload") if rows else None)
                rows = ag.cmd(op="map", act="get", dtype=dt, didx=0)
                back = rows[-1].get("payload") if rows else None
                event("map-final", dtype=f"{dt:#06x}", readback=back, equal_to_found=back == found.get(f"map-{dt:#06x}"))
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
        event("reader", frames=rd.total, error=rd.err, identified=rd.pair is not None)
    if mrx is not None:
        mrx.stop = True
        mrx.join(5)
        event("mcasp", frames=mrx.total, bytes=mrx.bytes, sha256=mrx.sha.hexdigest(), connections=mrx.conns,
              nonzero_words_ch4_7=[int(x) for x in mrx.nz47], error=mrx.err)
    if srx is not None:
        srx.stop = True
        srx.join(5)
        event("samples", lines=srx.lines, connections=srx.conns)
    if tm is not None:
        tm.stop = True
        tm.join(5)
        event("tone-status-end", state=(tm.last or {}).get("state"))
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

#!/usr/bin/env python3
"""One lane B6 case (this host; the caller holds the bench lock for the whole case).

usage: run_b6.py <name> <case> <window_s> <raw_root>
  case: A0 | A1 | A2 | BINT | BCRF

Lane B5's run_a.py method, with the B6 tone and the clock-source steps:

 1. SoC board: fetch the tone loop (b6_tone.py, 48,000 frames) from this host over the
    board link and check its SHA-256; fetch the timing sampler script the same way.
 2. Controller: start the b6_ctl.py agent; read the as-found state (formats, clock
    sources, RX states); DUT STREAM_PORT_OUTPUT 0 gets eight identity mappings, read back.
 3. This host: start the external capture (<capture-channels> channels, <capture-format>, 48 kHz). The reader keeps
    the <capture-input> pair (<tone-channels>, identified by content in lane B5 and checked
    again here from ten seconds of all channels), stamps every read with this host's
    CLOCK_MONOTONIC_RAW and realtime, and decodes the tone online to pace the run.
 4. SoC board: play the loop into McASP0 for the whole case (aplay ends at its duration),
    and hold McASP0 capture of the DUT's TDM output running into /dev/null.
 5. Binding rule before every bind (owner): read the talker's and the listener's current
    stream formats; if they differ, set the LISTENER's to the talker's and read it back;
    a listener that does not take it is a STOP. Then CONNECT_RX.
      all cases: DUT STREAM_OUTPUT 0 (AAF) -> peer STREAM_INPUT 0
      A2:        DUT STREAM_OUTPUT 1 (CRF) -> peer STREAM_INPUT 8
      BINT/BCRF: peer STREAM_OUTPUT 2 (CRF) -> DUT STREAM_INPUT 1
 6. Clock source (owner rule: only on the LISTENER's CLOCK_DOMAIN, read back):
      A0: peer as found; A1: peer -> the source located on STREAM_INPUT 0;
      A2: peer -> the source located on STREAM_INPUT 8; BINT: DUT as found (INTERNAL);
      BCRF: DUT -> the source located on STREAM_INPUT 1 (CRF), then wait for the DUT's
      media-clock servo to read LOCKED.
 7. SoC board: the timing sampler reads McASP0's playback and capture PCM status
    (hw_ptr, which the read itself brings up to date) five times a second with the board's
    clock before and after each read, and sends each sample line over the board link to a
    receiver here that stamps its arrival on CLOCK_MONOTONIC_RAW. No audio leaves the board.
 8. Window: <window_s> s untouched after a settle period, DUT reads (CRF sink, servo, slip
    counters) and peer counters at its start, middle and end.
 9. Teardown, always: sampler, capture and playback stopped by PID (command lines
    checked); clock sources restored as found, the peer's first and then the DUT's, each
    read back; every bind unbound; the peer's STREAM_INPUT 0 format restored and read
    back; DUT mappings removed and read back empty; board files removed.

Grading is offline (grade_b6.py). Environment (private): SOC_CONSOLE, DUT_CONSOLE,
CTL_HOST, CTL_IFACE, PEER_EID, PEER_MAC, CAP_CARD, ECM_HOST.
"""
import hashlib
import json
import os
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
DUT_EID = "020000fffe000001"
NCH, CAP_L, CAP_R = <capture-channels>, <tone-channel-a>, <tone-channel-b>
FS = 48000
CAP_PERIOD, CAP_BUFFER = 480, 24000
MIN_RUN = 480
SETTLE_S = 20.0
DUT_READS = ["milan_status", "mem_read 0x90000738 4", "mem_read 0x90000748 8", "mem_read 0x900008d4 12",
             "mem_read 0x900008f8 8", "mem_read 0x90000660 20", "mem_read 0x90000694 8", "mem_read 0x900006cc 12"]
TONE = "/tmp/a477-tone.raw"
SAMPLER = "/tmp/a477-sampler.sh"
PLAYLOG = "/tmp/a477-play.log"
CAPLOG = "/tmp/a477-cap.log"
RAWT = time.clock_gettime_ns
MONO_RAW = time.CLOCK_MONOTONIC_RAW

name, case, window_s, raw_root = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
assert case in ("A0", "A1", "A2", "BINT", "BCRF"), case
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
dest = PACKET / "runs" / name
dest.mkdir(parents=True, exist_ok=False)
events = open(dest / "events.jsonl", "a", buffering=1)
PLAY_S = int(window_s + 300)
SAMPLES = int((window_s + 200) * 5)
aplay_line = f"aplay -v -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {PLAY_S}"
arec_line = f"arecord -D hw:0,0 -t raw -c 8 -f S32_LE -r 48000 -d {PLAY_S}"


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
        for addr, n in (("0x900008f8", 8), ("0x90000738", 4), ("0x90000748", 8), ("0x900008d4", 12)):
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


def soc(tag, limit, cmd):
    r = run(["python3", "-B", str(TOOLS / "soccon_net.py"), SOC, str(dest / f"soc-{tag}.log"), str(limit), cmd],
            limit + 40, capture_output=True, text=True)
    event("soc", tag=tag, rc=r.returncode)
    return r.returncode


class Reader(threading.Thread):
    """Reads the capture pipe; keeps the <capture-input> pair; stamps reads; decodes the tone online."""

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
                self.full = open(raw / "cap-all-20ch.raw", "wb")
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
             f"cd /tmp/a477 && sudo -n timeout {PLAY_S + 600} python3 -B b6_ctl.py agent {IFACE} {PEER_EID} {PEER_MAC}"],
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


SAMPLER_SH = r"""#!/bin/bash
# Lane B6 timing sampler: McASP0 playback and capture PCM status (@SAMPLES@ samples, 5 per second).
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

ag = rd = cap = srv = srx = None
fetched = mapped = played = sampling = False
found = {}
binds = []          # (talker, listener) bound by this case
clk_changed = []    # (who, as_found)
peer_fmt_set = False
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
    for who, d, i in (("peer", "in", 0), ("peer", "in", 8), ("dut", "in", 0), ("dut", "in", 1),
                      ("dut", "out", 0), ("dut", "out", 1), ("peer", "out", 2)):
        found[f"fmt-{who}-{d}-{i}"] = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=i))
    for who in ("peer", "dut"):
        found[f"clk-{who}"] = clk_of(ag.cmd(op="clk", who=who), f"clock-{who}")
    for who, i in (("peer", 0), ("peer", 8), ("dut", 0), ("dut", 1)):
        rows = ag.cmd(op="rx", who=who, idx=i)
        found[f"rx-{who}-{i}"] = {k: rows[0].get(k) for k in ("status", "conn_count", "stream_id")} if rows else None
    event("as-found", **found)
    if any((found.get(f"rx-{w}-{i}") or {}).get("conn_count") for w, i in (("peer", 0), ("peer", 8), ("dut", 0), ("dut", 1))):
        raise SystemExit("a listener this case uses is already bound: not this lane's state, nothing changed")
    if found["clk-peer"] != 0 or found["clk-dut"] != 0:
        raise SystemExit(f"clock sources not as recorded at the start (peer {found['clk-peer']}, dut {found['clk-dut']})")
    ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
    mapped = True
    rows = ag.cmd(op="map", act="add", dtype=0x000F, didx=0, n=8)
    event("map-add", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
    for who, dt, i in (("dut", 6, 0), ("peer", 5, 0)):
        ag.cmd(op="counters", who=who, dtype=dt, idx=i)
    cap = subprocess.Popen(["timeout", "-s", "INT", str(PLAY_S + 300), "arecord", "-D", f"hw:{CARD},0", "-f", "<capture-format>",
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
    # AAF bind, DUT talker -> peer listener
    aaf = (("dut", 0), ("peer", 0))
    rule = binding_rule(ag, *aaf, "aaf")
    peer_fmt_set = rule["set"] is not None
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
    # case-specific
    if case == "A2":
        crf = (("dut", 1), ("peer", 8))
        binding_rule(ag, *crf, "crf")
        if not acmp(ag, "bind", *crf):
            raise SystemExit("CRF bind failed")
        binds.append(crf)
    if case in ("BINT", "BCRF"):
        crf = (("peer", 2), ("dut", 1))
        binding_rule(ag, *crf, "crf")
        if not acmp(ag, "bind", *crf):
            raise SystemExit("CRF bind failed")
        binds.append(crf)
    target = {"A1": ("peer", 3), "A2": ("peer", 1), "BCRF": ("dut", 1)}.get(case)
    if target:
        who, src = target
        clk_changed.append((who, found[f"clk-{who}"]))
        st, back = setclk(ag, who, src, "case")
        if back != src:
            raise SystemExit(f"clock source set refused or not read back ({st}, {back})")
    ag.sync(3)
    t_set = time.monotonic()
    if case == "BCRF":
        lock_t = None
        while time.monotonic() - t_set < 180:
            w = dut("servo-wait")
            s = int(w.get("0x8f8", "0"), 16) if w else 0
            if s & 7 == 4:
                lock_t = time.monotonic() - t_set
                break
            time.sleep(3.0)
        event("servo-lock", seconds=lock_t)
        if lock_t is None:
            raise SystemExit("the DUT's media-clock servo did not read LOCKED within 180 s")
    while time.monotonic() - t_set < SETTLE_S:
        time.sleep(0.5)
    ag.cmd(op="counters", who="peer", dtype=5, idx=0)
    t_c0 = time.monotonic()
    event("window-start", frame=frames_now(rd), samples=srx.lines)
    marks = [5, window_s / 2, window_s - 15]
    k = 0
    while time.monotonic() - t_c0 < window_s:
        el = time.monotonic() - t_c0
        if k < len(marks) and el >= marks[k]:
            dut(f"window-{k}")
            ag.cmd(op="counters", who="peer", dtype=5, idx=0)
            if case == "A2":
                ag.cmd(op="counters", who="peer", dtype=5, idx=8)
            if case in ("BINT", "BCRF"):
                ag.cmd(op="counters", who="dut", dtype=5, idx=1)
            ag.cmd(op="clk", who="peer")
            ag.cmd(op="clk", who="dut")
            ag.sync(3)
            k += 1
        time.sleep(0.5)
    event("window-end", frame=frames_now(rd), samples=srx.lines)
finally:
    event("teardown")
    if sampling or played:
        soc("stop", 60, f"cat /proc/uptime; for pat in '[b]ash {SAMPLER}' '[a]record -D hw:0,0' '[a]play -v -D hw:0,0'; do "
                        f"for p in $(ps -o pid,args | grep \"$pat\" | awk '{{print $1}}'); do "
                        f"A=$(tr '\\0' ' ' < /proc/$p/cmdline); echo \"$p: $A\"; "
                        f"if [ \"$A\" = 'bash {SAMPLER} ' ] || [ \"$A\" = '{arec_line} ' ] || [ \"$A\" = '{aplay_line} ' ]; "
                        f"then kill $p; echo KILLED $p; else echo MISMATCH $p; fi; done; done; sleep 2; "
                        f"ps -o pid,args | grep -E '[a]play|[a]record|[c]at {TONE}|[a]477-sampler'; echo PS_RC=$?; "
                        f"cat {PLAYLOG} {CAPLOG}; for s in /proc/asound/card0/pcm0*/sub0/status; do head -2 $s; done")
    if ag is not None:
        try:
            ag.sync(3)
            # clock sources first, the peer's and then the DUT's, each read back
            for who in ("peer", "dut"):
                for w, src0 in clk_changed:
                    if w == who and src0 is not None:
                        setclk(ag, who, src0, "restore")
            for who in ("peer", "dut"):
                event("clock-final", who=who, source=clk_of(ag.cmd(op="clk", who=who), f"clock-{who}"),
                      as_found=found.get(f"clk-{who}"))
            for tl in reversed(binds):
                acmp(ag, "unbind", *tl)
            time.sleep(2.0)
            if peer_fmt_set and found.get("fmt-peer-in-0"):
                s = ag.cmd(op="setfmt", who="peer", idx=0, fmt=found["fmt-peer-in-0"])
                event("peer-format-restore", fmt=found["fmt-peer-in-0"], status=[r.get("status") for r in s])
            for key in ("fmt-peer-in-0", "fmt-peer-in-8", "fmt-dut-in-0", "fmt-dut-in-1"):
                _, who, d, i = key.split("-")
                back = fmt_of(ag.cmd(op="fmt", who=who, dir=d, idx=int(i)))
                event("format-final", key=key, fmt=back, equal_to_found=back == found.get(key))
            if mapped:
                rows = ag.cmd(op="map", act="remove", dtype=0x000F, didx=0, n=8)
                event("map-remove", status=[r.get("status") for r in rows], readback=rows[-1].get("payload") if rows else None)
                rows = ag.cmd(op="map", act="get", dtype=0x000F, didx=0)
                event("map-final", readback=rows[-1].get("payload") if rows else None)
            for who, i in (("peer", 0), ("peer", 8), ("dut", 0), ("dut", 1)):
                ag.cmd(op="rx", who=who, idx=i)
            ag.cmd(op="tx", who="dut", idx=0)
            ag.cmd(op="tx", who="dut", idx=1)
            ag.cmd(op="tx", who="peer", idx=2)
            ag.sync(3)
        except BaseException as e:
            event("teardown-error", error=repr(e))
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

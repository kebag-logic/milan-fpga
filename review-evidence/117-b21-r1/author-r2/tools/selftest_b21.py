#!/usr/bin/env python3
"""Lane B21 step 1: capture-path self-test, deficit-only (this host; the caller holds the bench lock).

usage: selftest_b21.py <name> <seconds> <raw_root>

No DUT, peer, SoC board or controller action: the external capture runs alone, with lane B5's
reader (run_a.py's Reader, copied unchanged but for the module globals it reads) and its arecord
command line (hw:<CAP_CARD>,0, S24_3LE, 48 kHz, 20 channels, period 480, buffer 24,000 frames).
The capture's input is whatever it receives as found; the self-test reads only the per-read
timing record and the delivery deficit, which reveal loss inside the capture path independent of
content.

Alongside, a host-evidence sampler (host_sampler_b21.py, its own process) reads /proc/stat,
/proc/interrupts and /proc/loadavg at 20 Hz, so each stall can be placed against steal time,
interrupt counts and load. Snapshots of the process table (cumulative CPU), timers and the kernel
log are taken before and after.

Environment: CAP_CARD.
"""
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
CARD = os.environ["CAP_CARD"]
CAP_PERIOD, CAP_BUFFER = 480, 24000
NCH, CAP_L, CAP_R = 20, 10, 11  # lane B5's AES pair
FS = 48000

name, secs, raw_root = sys.argv[1], float(sys.argv[2]), sys.argv[3]
raw = Path(raw_root) / name
raw.mkdir(parents=True, exist_ok=False)
events = open(raw / "events.jsonl", "a", buffering=1)


def event(kind, **kw):
    r = dict(t=round(time.time(), 6), kind=kind, **kw)
    events.write(json.dumps(r) + "\n")
    print(json.dumps(r), flush=True)


class Reader(threading.Thread):
    """run_a.py's Reader: reads the capture pipe; writes the two AES channels; stamps every read."""

    def __init__(self, proc):
        super().__init__(daemon=True)
        self.proc = proc
        self.out = open(raw / "cap-lr.raw", "wb")
        self.ts = open(raw / "cap-ts.bin", "wb")  # <q frames_after_read, d realtime, q monotonic_ns>
        self.lock = threading.Lock()
        self.total = 0
        self.err = None

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
                with self.lock:
                    self.total += n
                self.ts.write(struct.pack("<qdq", self.total, t_rt, t_mono))
        except Exception as e:  # recorded, never raised into the run
            self.err = repr(e)
        finally:
            self.out.close()
            self.ts.close()


def snap(tag):
    cmds = {
        "ps": ["ps", "-eo", "pid,ppid,cls,rtprio,ni,pri,psr,time,etimes,comm,args", "--sort=-time"],
        "timers": ["systemctl", "list-timers", "--all", "--no-pager"],
        "uptime": ["cat", "/proc/uptime", "/proc/loadavg"],
        "dmesg": ["sh", "-c", "dmesg 2>&1 | tail -40"],
        "interrupts": ["cat", "/proc/interrupts"],
        "asound": ["sh", "-c", "cat /proc/asound/cards; for s in /proc/asound/card*/pcm*/sub0/status; do echo \"$s: $(head -1 $s)\"; done"],
    }
    for k, c in cmds.items():
        with open(raw / f"host-{tag}-{k}.txt", "w") as f:
            r = subprocess.run(c, stdout=f, stderr=subprocess.STDOUT, timeout=30)
        event("snapshot", tag=tag, what=k, rc=r.returncode)


event("start", name=name, seconds=secs, card=CARD, period=CAP_PERIOD, buffer=CAP_BUFFER, channels=NCH,
      tool_sha256=hashlib.sha256(open(__file__, "rb").read()).hexdigest())
snap("before")
smp = subprocess.Popen(["timeout", "-s", "INT", str(int(secs) + 60), "python3", "-B", str(TOOLS / "host_sampler_b21.py"),
                        str(raw / "host-samples.bin"), "20"], stderr=open(raw / "sampler.log", "w"))
cap = subprocess.Popen(["timeout", "-s", "INT", str(int(secs) + 30), "arecord", "-D", f"hw:{CARD},0", "-f", "S24_3LE",
                        "-r", str(FS), "-c", str(NCH), "-t", "raw", f"--period-size={CAP_PERIOD}",
                        f"--buffer-size={CAP_BUFFER}", "-v", "-"], stdout=subprocess.PIPE,
                       stderr=open(raw / "arecord.log", "w"))
rd = Reader(cap)
rd.start()
event("capture-started")
t0 = time.monotonic()
try:
    while time.monotonic() - t0 < secs:
        time.sleep(1.0)
        if cap.poll() is not None:
            event("capture-ended-early", rc=cap.returncode)
            break
finally:
    if cap.poll() is None:
        cap.send_signal(2)
        try:
            cap.wait(10)
        except subprocess.TimeoutExpired:
            cap.kill()
            cap.wait(5)
    event("capture-exit", rc=cap.returncode)
    rd.join(10)
    event("reader", frames=rd.total, error=rd.err)
    if smp.poll() is None:
        smp.send_signal(2)
        try:
            smp.wait(10)
        except subprocess.TimeoutExpired:
            smp.kill()
            smp.wait(5)
    event("sampler-exit", rc=smp.returncode)
    snap("after")
    for f in sorted(raw.iterdir()):
        if f.name == "events.jsonl":
            continue
        h = hashlib.sha256()
        with open(f, "rb") as fh:
            for blk in iter(lambda: fh.read(1 << 22), b""):
                h.update(blk)
        event("raw-file", file=f.name, bytes=f.stat().st_size, sha256=h.hexdigest())
    event("end")

#!/usr/bin/env python3
"""Fault-injection probe of the packet's grade_a.py: synthesize a run (capture pair,
read-time records, events) with known torn, invalid, repeat, skip, backward and zero
frames and a known restart, grade it with the packet's tool, compare every count.
usage: grade_a_fault_probe.py <packet author dir> <scratch dir>"""
import json, subprocess, sys
from pathlib import Path
import numpy as np

A, S = Path(sys.argv[1]), Path(sys.argv[2])
FS = 48000
run, raw = S / "run", S / "raw"
run.mkdir(parents=True, exist_ok=True); raw.mkdir(parents=True, exist_ok=True)

PRE = 4800                      # zero frames before the first valid sample
N = 20 * FS                     # frames of pattern
ords = list(range(N))
L = [(1 << 16) | (n & 0xFFFF) for n in ords]
R = [(2 << 16) | (n & 0xFFFF) for n in ords]
exp = dict(repeats=0, skips={}, torn=0, invalid=0, zero=0, backward=0)
def at(k): return k
# inject (positions in pattern frames, chosen far apart)
# repeat at 100000: frame k+1 equals frame k
k = 100000; L[k + 1], R[k + 1] = L[k], R[k]; exp["repeats"] += 1
for j in range(k + 2, N): L[j] = (1 << 16) | ((ords[j] - 1) & 0xFFFF); R[j] = (2 << 16) | ((ords[j] - 1) & 0xFFFF)
def skip(k, d):
    for j in range(k, N):
        L[j] = (1 << 16) | (((L[j] & 0xFFFF) + d) & 0xFFFF); R[j] = (2 << 16) | (((R[j] & 0xFFFF) + d) & 0xFFFF)
    exp["skips"][d] = exp["skips"].get(d, 0) + 1
skip(200000, 1); skip(300000, 6); skip(400000, 100)
# backward jump of 50 at 500000
for j in range(500000, N):
    L[j] = (1 << 16) | (((L[j] & 0xFFFF) - 50) & 0xFFFF); R[j] = (2 << 16) | (((R[j] & 0xFFFF) - 50) & 0xFFFF)
exp["backward"] += 1
# torn frame at 600000 (isolated: neighbours valid, so the steps around it are not counted)
R[600000] = (2 << 16) | (((R[600000] & 0xFFFF) + 3) & 0xFFFF); exp["torn"] += 1
# invalid non-zero (wrong tag) at 700000 and a one-bit flip in the tag at 700500
L[700000] = (3 << 16) | (L[700000] & 0xFFFF); exp["invalid"] += 1
R[700500] = R[700500] ^ (1 << 20); exp["invalid"] += 1
# zero frames: one at 800000, a run of 5 at 850000
for j in [800000] + list(range(850000, 850005)):
    L[j] = 0; R[j] = 0; exp["zero"] += 1
exp["torn_counted_invalid"] = exp["torn"]  # a torn frame is also not valid
Lw = np.array([0] * PRE + L, dtype=np.int64); Rw = np.array([0] * PRE + R, dtype=np.int64)
NF = len(Lw)
b = np.zeros((NF, 2, 3), dtype=np.uint8)
for c, w in ((0, Lw), (1, Rw)):
    b[:, c, 0] = w & 0xFF; b[:, c, 1] = (w >> 8) & 0xFF; b[:, c, 2] = (w >> 16) & 0xFF
b.tofile(raw / "cap-lr.raw")
# read records every 480 frames; host time = T0 + frames / FS + 1 ms latency
T0 = 1_000_000.0
f = np.arange(480, NF + 1, 480, dtype=np.int64)
ts = np.zeros(len(f), dtype=np.dtype([("f", "<i8"), ("rt", "<f8"), ("mono", "<i8")]))
ts["f"] = f; ts["rt"] = T0 + f / FS + 0.001; ts["mono"] = (ts["rt"] * 1e9).astype(np.int64)
ts.tofile(raw / "cap-ts.bin")
# controller clock = host clock + 1.5 s; bind response at host time T0 + 0.05 s; the first valid
# frame (PRE) reaches the host at T0 + PRE/FS + 1 ms - its delivery lag; expected restart:
OFF = 1.5
t_rx_local = T0 + 0.05
first_valid_host = T0 + (PRE // 480 + 1) * 480 / FS + 0.001 - ((PRE // 480 + 1) * 480 - PRE) / FS
events = [
    dict(kind="sync", t0=T0 - 1, t1=T0 - 1 + 1e-4, rtt_ms=0.1, offset_ms=OFF * 1e3),
    dict(kind="bind", t=T0 + 0.04, t_tx=T0 + 0.042 + OFF, t_rx=t_rx_local + OFF, status=0),
    dict(kind="initial-valid", frame=PRE),
    dict(kind="sync", t0=T0 + 1, t1=T0 + 1 + 1e-4, rtt_ms=0.2, offset_ms=OFF * 1e3),
    dict(kind="continuity-start", frame=PRE + 10),
    dict(kind="continuity-end", frame=NF - 10),
]
with open(run / "events.jsonl", "w") as fh:
    for e in events: fh.write(json.dumps(e) + "\n")
(run / "ctl.jsonl").write_text("")
out = S / "grade.json"
r = subprocess.run([sys.executable, "-I", str(A / "tools/grade_a.py"), str(run), str(raw), str(out)],
                   capture_output=True, text=True)
if r.returncode:
    print(r.stderr); sys.exit(2)
g = json.load(open(out)); c = g["continuity"]
checks = [
    ("repeats", c["repeats"], exp["repeats"]),
    ("skip histogram", c["skip_size_histogram"], {str(k): v for k, v in sorted(exp["skips"].items())}),
    ("backward", c["backward"], exp["backward"]),
    ("torn", c["torn"], exp["torn"]),
    ("invalid_nonzero (torn + wrong tag + bit flip)", c["invalid_nonzero"], exp["torn"] + exp["invalid"]),
    ("zero_frames", c["zero_frames"], exp["zero"]),
    ("silent stretches", [s["frames"] for s in c["silent_stretches"]], [1, 5]),
    ("valid", c["valid"], (NF - PRE - 20) - exp["torn"] - exp["invalid"] - exp["zero"]),
]
ib = g["initial_bind"]
checks.append(("initial first_valid_frame", ib["first_valid_frame"], PRE))
checks.append(("initial restart_s (upper bound by 1 ms read latency)", round(ib["restart_s"], 4),
               round(first_valid_host - t_rx_local, 4)))
bad = 0
for name, got, want in checks:
    ok = (got == want) if not isinstance(got, dict) else (json.loads(json.dumps(got)) == want)
    bad += not ok
    print(("OK  " if ok else "BAD ") + f"{name}: got {got} want {want}")
print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)

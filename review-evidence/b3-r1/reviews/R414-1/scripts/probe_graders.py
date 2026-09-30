#!/usr/bin/env python3
"""Fault probes of the lane's published grading tools (offline, synthetic data).
usage: probe_graders.py <packet-author-tools-dir> <scratch-dir>

DIN (grade_617.py): builds AAF pcaps of the first-light pattern and checks that
  A clean stream with whole-frame repeats every 93,990 frames -> 0 torn, repeats counted, identical in all channels
  B first-light tear shapes (pairs 1..3 one frame older, the three #451 states) -> every such frame counted torn
  C a single skipped TDM frame -> reported as a +2 step (not hidden)
  D the first-light stop-tail shape (pair 0 zero, pairs 1..3 last ordinal) -> NOT counted by the ordinal rule (documents the limit)
USB (grade_usb.py): builds S32_LE captures and checks
  E an exact in-order capture -> passes the strict rule
  F a capture shifted by k whole words -> strict 0, classified rot<k>
  G a linearly interpolated capture (half-sample phase) -> strict 0, low bytes non-zero, still in order
"""
import json, os, struct, subprocess, sys

tools, scratch = sys.argv[1], sys.argv[2]
os.makedirs(scratch, exist_ok=True)
SID = bytes.fromhex("0200000000010000")

def word(t, n):
    return ((t << 16) | (n & 0xFFFF)) << 8

def pcap(path, frames):
    out = [struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)]
    seq = 0
    for p in range(0, len(frames) - len(frames) % 6, 6):
        hdr = bytes(12) + b"\x22\xf0"
        avtp = bytes([0x02, 0x81, seq & 0xFF, 0]) + SID + bytes(4) + bytes([0x02, 0x50, 0x08, 32]) + struct.pack(">HH", 192, 0)
        payload = b"".join(struct.pack(">8I", *frames[p + k]) for k in range(6))
        fr = hdr + avtp + payload
        out.append(struct.pack("<IIII", p // 6, 0, len(fr), len(fr)) + fr)
        seq += 1
    open(path, "wb").write(b"".join(out))

def grade617(frames, name):
    p = os.path.join(scratch, name + ".pcap")
    pcap(p, frames)
    r = subprocess.run([sys.executable, os.path.join(tools, "grade_617.py"), p, SID.hex()], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)

res = {}
N = 199998  # a whole number of 6-frame PDUs
# A: ordinal stream with a repeat every 93,990 frames
ords, n = [], 1000
for i in range(N):
    ords.append(n)
    if i % 93990 != 93989:
        n += 1
A = [[word(c + 1, o) for c in range(8)] for o in ords]
g = grade617([[0xFFFFFF00] * 8] * 12 + A + [[0] * 8] * 12, "A")
res["A"] = dict(torn=g["torn_frames_whole_recording"], steps=g["channel0_non_unit_steps"], same=g["steps_identical_in_all_channels"],
                ok=g["torn_frames_whole_recording"] == 0 and g["channel0_non_unit_steps"] == {"0": 2} and g["steps_identical_in_all_channels"])
# B: first-light tear states
B, torn_expected = [], 0
for i in range(N):
    o = 1000 + i
    st = (i // 1000) % 4  # 0 coherent, 1: pair3 older, 2: pairs 2,3 older, 3: pairs 1..3 older
    w = []
    for c in range(8):
        p = c // 2
        older = (st == 1 and p == 3) or (st == 2 and p >= 2) or (st == 3 and p >= 1)
        w.append(word(c + 1, o - 1 if older else o))
    torn_expected += st != 0
    B.append(w)
g = grade617(B, "B")
res["B"] = dict(torn=g["torn_frames_in_region"], expected=torn_expected, offsets=g["pair_offset_vs_pair0"],
                ok=g["torn_frames_in_region"] == torn_expected)
# C: one skipped TDM frame
C = [[word(c + 1, 1000 + i + (1 if i >= 5000 else 0)) for c in range(8)] for i in range(20000)]
g = grade617(C, "C")
res["C"] = dict(steps=g["channel0_non_unit_steps"], torn=g["torn_frames_whole_recording"], ok=g["channel0_non_unit_steps"] == {"2": 1})
# D: first-light stop-tail torn shape just after the region
D = [[word(c + 1, 1000 + i) for c in range(8)] for i in range(12000)]
last = 1000 + 11999
D.append([0, 0] + [word(c + 1, last) for c in range(2, 8)])
D += [[0] * 8] * 11
g = grade617(D, "D")
res["D"] = dict(torn_whole=g["torn_frames_whole_recording"], edge_after=g["edge_frames"].get(str(12000)),
                note="ordinal rule does not count a zero/pattern mix; the page covers it through the edge-frame listing",
                ok=g["torn_frames_whole_recording"] == 0)

def grade_usb(words, name):
    p = os.path.join(scratch, name + ".raw")
    open(p, "wb").write(struct.pack("<%dI" % len(words), *words))
    r = subprocess.run([sys.executable, os.path.join(tools, "grade_usb.py"), p], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)

M = 60000
flat = [word(c + 1, i) for i in range(M + 2) for c in range(8)]
g = grade_usb(flat[:M * 8], "E")
res["E"] = dict(strict=g["strict"], classes=g["frame_classes"], ok=g["strict"]["valid_frames"] == M and g["strict"]["torn_valid_frames"] == 0)
for k in (1, 3):
    g = grade_usb(flat[k:k + M * 8], "F%d" % k)
    res["F%d" % k] = dict(strict=g["strict"]["valid_frames"], classes=g["frame_classes"],
                         steps=g["within_segment_steps"], ok=g["strict"]["valid_frames"] == 0 and g["frame_classes"].get("rot%d" % k, 0) == M)
interp = []
for i in range(M):
    for c in range(8):
        a, b = word(c + 1, i), word(c + 1, i + 1)
        interp.append((a + b) // 2)
g = grade_usb(interp, "G")
res["G"] = dict(strict=g["strict"]["valid_frames"], low=g["low_byte_histogram"], classes=g["frame_classes"],
                ok=g["strict"]["valid_frames"] == 0 and g["frame_classes"].get("aligned", 0) >= M - 2)
print(json.dumps(res, indent=1))
print("ALL PROBES AS EXPECTED" if all(v["ok"] for v in res.values()) else "PROBE MISMATCH")

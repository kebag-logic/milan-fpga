#!/usr/bin/env python3
"""Fault probes for the lane's graders (grade_617.py, grade_usb.py,
decode_capture.py): synthetic inputs with known defects, so each count the
pages rest on is shown able to go non-zero.

usage: probe_graders.py <packet-tools-dir> <scratch-dir>
"""
import json, os, struct, subprocess, sys
tools, scratch = sys.argv[1], sys.argv[2]
os.makedirs(scratch, exist_ok=True)
SID = bytes.fromhex("0200000000010000")
fails = 0
def chk(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(f"{'OK  ' if ok else 'FAIL'} {name}: got {got!r} want {want!r}")

def word(t, n):
    return ((t << 16) | (n & 0xFFFF)) << 8

def pcap(path, frames):
    """frames: list of 8-word tuples; six per AAF PDU, as the DUT talker sends."""
    out = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
    seq = 0
    for i in range(0, len(frames) - len(frames) % 6, 6):
        eth = b"\x91\xe0\xf0\x00\x00\x01" + b"\x02\x00\x00\x00\x00\x01" + b"\x22\xf0"
        hdr = bytes([0x02, 0x81, seq & 0xFF, 0x00]) + SID + b"\x00" * 4 + bytes([0x02, 0x50, 0x08, 32]) + struct.pack(">H", 192) + b"\x00\x00"
        data = b"".join(struct.pack(">8I", *frames[i + k]) for k in range(6))
        fr = eth + hdr + data
        out += struct.pack("<IIII", i // 6, 0, len(fr), len(fr)) + fr
        seq += 1
    open(path, "wb").write(out)

def run(tool, *args):
    r = subprocess.run([sys.executable, os.path.join(tools, tool), *args], capture_output=True, text=True)
    if r.returncode:
        print(r.stderr)
    return r.returncode

IDLE = (0xFFFFFF00,) * 8
def din(n_frames, tear_at=(), lr_at=(), repeat_at=()):
    fr = [IDLE] * 600
    n = 0
    for i in range(n_frames):
        if i in repeat_at:
            n -= 1
        w = [word(c + 1, n) for c in range(8)]
        if i in tear_at:           # pairs 1..3 one TDM frame older: the #451 first-light shape
            for c in range(2, 8):
                w[c] = word(c + 1, n - 1)
        if i in lr_at:             # right channel of pair 2 older
            w[5] = word(6, n - 1)
        fr.append(tuple(w))
        n += 1
    fr += [(0,) * 8] * 12 + [IDLE] * 594
    return fr

cases = [
    ("clean", din(12000, repeat_at=(3000, 9000)), dict(torn=0, rep=2, states={"[0, 0, 0]": 12000})),
    ("torn-first-light-shape", din(12000, tear_at=set(range(4000, 4100)) | {7000}), dict(torn=101, rep=None, states=None)),
    ("torn-left-right", din(12000, lr_at={5000, 5001, 5002}), dict(torn=3, rep=None, states=None)),
]
# Limit probe: first light's torn stop-tail frame (pair 0 zero, pairs 1..3 still
# at the last ordinal) carries ONE ordinal among its valid words, so the rule
# "valid words carry more than one ordinal" cannot count it. Expected torn 0.
tail = din(12000)
last = 600 + 12000 - 1
tail[last + 1] = (0, 0) + tuple(word(c + 1, 11999) for c in range(2, 8))
cases.append(("limit-first-light-stop-tail", tail, dict(torn=0, rep=0, states={"[0, 0, 0]": 12000})))
for name, frames, want in cases:
    p = os.path.join(scratch, f"din-{name}.pcap"); j = p + ".json"
    pcap(p, frames)
    chk(f"grade_617 {name} rc", run("grade_617.py", p, SID.hex(), j), 0)
    g = json.load(open(j))
    chk(f"grade_617 {name} torn in region", g["torn_frames_in_region"], want["torn"])
    chk(f"grade_617 {name} torn whole", g["torn_frames_whole_recording"], want["torn"])
    if want["rep"] is not None:
        chk(f"grade_617 {name} whole-frame repeats", g["channel0_non_unit_steps"], {"0": want["rep"]} if want["rep"] else {})
        chk(f"grade_617 {name} steps identical", g["steps_identical_in_all_channels"], True)
    if want["states"] is not None:
        chk(f"grade_617 {name} pair states", g["pair_offset_vs_pair0"], want["states"])
    else:
        chk(f"grade_617 {name} pair states not all coherent", len(g["pair_offset_vs_pair0"]) > 1 or any(g["left_right_mismatch_per_pair"]), True)

def raw(path, frames):
    open(path, "wb").write(b"".join(struct.pack("<8I", *f) for f in frames))

N = 5000
exact = [tuple(word(c + 1, n) for c in range(8)) for n in range(N)]
flat = [v for f in exact for v in f]
rot3 = [tuple(flat[i * 8 + 3:(i + 1) * 8 + 3]) for i in range(N - 1)]   # frame boundary lost by 3 words
interp = [tuple((v + 0x40) & 0xFFFFFFFF for v in f) for f in exact]      # low byte non-zero, order kept
for name, frames, want in (("exact", exact, dict(strict=N, aligned=N, rot=0)),
                           ("rot3", rot3, dict(strict=0, aligned=0, rot=N - 1)),
                           ("interp", interp, dict(strict=0, aligned=N, rot=0))):
    p = os.path.join(scratch, f"usb-{name}.raw"); j = p + ".json"
    raw(p, frames)
    chk(f"grade_usb {name} rc", run("grade_usb.py", p, j), 0)
    u = json.load(open(j))
    chk(f"grade_usb {name} strict valid", u["strict"]["valid_frames"], want["strict"])
    chk(f"grade_usb {name} aligned", u["frame_classes"].get("aligned", 0), want["aligned"])
    chk(f"grade_usb {name} rot3", u["frame_classes"].get("rot3", 0), want["rot"])
    j2 = p + ".dc.json"
    chk(f"decode_capture {name} rc", run("decode_capture.py", p, j2), 0)
    dc = json.load(open(j2))
    chk(f"decode_capture {name} torn-or-invalid frames", dc["torn_frames"] > 0, want["strict"] == 0)
print("RESULT", "PASS" if fails == 0 else f"FAIL ({fails})")
sys.exit(1 if fails else 0)

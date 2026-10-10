#!/usr/bin/env python3
"""R595-1 disposable probes of the lane B15 decoders (offline, synthetic data only).

usage: probes_r595.py <tools_dir> <work_dir>

<tools_dir> is a copy of the published lane B15 tools in which the two redacted
identity placeholders of tone_points_b15.py are replaced by neutral values (the
decoders' logic does not depend on them). Every probe prints one JSON line with
its expectation and its result; the exit status is 0 when every probe behaved
as the expectation says.
"""
import hashlib
import json
import os
import struct
import sys

import numpy as np

TOOLS, WORK = sys.argv[1], sys.argv[2]
sys.path.insert(0, TOOLS)
import align_b15 as AL  # noqa: E402
import b6_thdn as A  # noqa: E402
import b6_tone as T6  # noqa: E402
import tone_points_b15 as TP  # noqa: E402

FS = 48000
SID = "0200000000aa0000"
ok_all = True


def report(name, expect, got, ok):
    global ok_all
    ok_all &= bool(ok)
    print(json.dumps(dict(probe=name, expect=expect, got=got, result="AS EXPECTED" if ok else "UNEXPECTED")))


def floor_stream(n, seed=1):
    """A floor shaped like the recorded one: channels 0/1 in -2..+1, channels 2/3 in -1..0."""
    rng = np.random.default_rng(seed)
    x = np.zeros((n, 4), dtype=np.int64)
    x[:, 0] = rng.choice([-2, -1, 0, 1], size=n, p=[0.05, 0.40, 0.50, 0.05])
    x[:, 1] = rng.choice([-2, -1, 0], size=n, p=[0.05, 0.45, 0.50])
    x[:, 2] = rng.choice([-1, 0], size=n)
    x[:, 3] = rng.choice([-1, 0], size=n)
    return x


def write_pcap(path, x, port=2):
    cpf = x.shape[1]
    words = ((x << 8) & 0xFFFFFFFF)
    out = bytearray(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 262144, 1))
    for pdu in range(len(x) // 6):
        pay = words[pdu * 6:(pdu + 1) * 6].astype(">u4").tobytes()
        avtp = bytes([0x02, 0x81, pdu & 0xFF, 0]) + bytes.fromhex(SID) + struct.pack(">I", (pdu * 125000) & 0xFFFFFFFF) + \
            bytes([0x02, 0x50 | (cpf >> 8), cpf & 0xFF, 32]) + struct.pack(">H", len(pay)) + b"\x10\x00" + pay
        eth = bytes.fromhex("91e0f000fe00") + bytes.fromhex("0200000000aa") + b"\x81\x00\x60\x02\x22\xf0" + avtp
        rec = struct.pack("<IIIIII", 6, 0x110, port, 0, 0, len(eth)) + struct.pack("<I", len(eth)) + eth
        out += struct.pack("<IIII", pdu // 8000, (pdu % 8000) * 125, len(rec), len(rec)) + rec
    open(path, "wb").write(out)


# ---- alignment (align_b15.py) ----
N = 191842 * 6  # pts1's stream length at (b)
s = floor_stream(N)
pcap = os.path.join(WORK, "floor.pcap")
write_pcap(pcap, s)
dec, info = AL.load(pcap, SID, 2, 4)
report("A0 synthetic floor decodes exactly", "equal, 0 gaps", dict(equal=bool(np.array_equal(dec, s)), gaps=info["seq_gaps"]),
       np.array_equal(dec, s) and info["seq_gaps"] == 0)

rc = AL.controls(pcap, SID, 2, os.path.join(WORK, "align-controls.json"))
report("A1 align_b15 planted controls on a synthetic floor", "5 of 5 PASS (rc 0)", rc, rc == 0)

off = 182213
m = s[off:off + 480000].copy()
r = AL.compare(s, m, 4, 0)
report("A2 exact slice", "SAMPLE-EXACT, 480,000 equal", [r["verdict"], r["compared_equal"], r["matches_of_first_window"]],
       r["verdict"] == "SAMPLE-EXACT" and r["compared_equal"] == 480000)

m2 = m.copy()
m2[123456, 1] += 256
r = AL.compare(s, m2, 4, 0)
report("A3 one sample +256 LSB (outside the key's 8-bit lane)", "missed: the frame key keeps 8 bits per channel",
       [r["verdict"], r["frames_differing"]], r["verdict"] == "SAMPLE-EXACT")

m3 = m.copy()
m3[123456, 1] += 1
r = AL.compare(s, m3, 4, 0)
report("A4 one sample +1 LSB", "DIFFERENT, 1 differing frame", [r["verdict"], r["frames_differing"]],
       r["verdict"] == "DIFFERENT" and r["frames_differing"] == 1)

m4 = m[:, [0, 1, 3, 2]].copy()
r = AL.compare(s, m4, 4, 0)
report("A5 channels 2 and 3 swapped", "not SAMPLE-EXACT", r["verdict"], r["verdict"] != "SAMPLE-EXACT")

m5 = m[:, [1, 0, 2, 3]].copy()
r = AL.compare(s, m5, 4, 0)
report("A6 channels 0 and 1 swapped", "not SAMPLE-EXACT", r["verdict"], r["verdict"] != "SAMPLE-EXACT")

m6 = s[N - 300000:N].copy()
m6 = np.concatenate([m6, floor_stream(180000, seed=7)])
r = AL.compare(s, m6, 4, 0)
report("A7 recording runs past the end of the stream", "not SAMPLE-EXACT, or fewer than 480,000 compared",
       [r["verdict"], r.get("compared_equal"), r.get("covered_recording_frames")],
       r["verdict"] != "SAMPLE-EXACT" or r.get("compared_equal", 0) < 480000)

m7 = m.copy()
m7[300000:300050] = m7[300000]
r = AL.compare(s, m7, 4, 0)
report("A8 a 50-frame held value", "DIFFERENT", [r["verdict"], r["frames_differing"], r["slips"][:3]], r["verdict"] == "DIFFERENT")

# the recorded ranges keep every value inside the key's lossless lane [-128, 127]
report("A9 recorded (b) and (c) ranges inside the key's lossless lane", "-2..+1 within -128..127", [-2, 1],
       -128 <= -2 and 1 <= 127)

# ---- presence rule (tone_points_b15.channel_rows / verdict) ----
k = np.arange(10 * FS)


def tone_at(dbfs, f, ph):
    return np.round(10 ** (dbfs / 20) * np.sqrt(2) * 2 ** 23 * np.sin(2 * np.pi * f * k / FS + ph))


fl = floor_stream(10 * FS, seed=3).astype(np.float64)
rows = TP.channel_rows(fl)
sh = [r["share_997"] for r in rows] + [r["share_9973"] for r in rows]
report("T1 the recorded-shape floor alone", "TONE ABSENT, shares ~0.0004 (10 Hz of 24 kHz)",
       [TP.verdict(rows)[1], round(min(sh), 6), round(max(sh), 6)],
       TP.verdict(rows)[1] == "TONE ABSENT" and max(sh) < 0.001)
for lvl in (-20.0, -38.5, -45.0, -100.0):
    x = fl.copy()
    x[:, 0] += tone_at(lvl, 997, 0.7)
    x[:, 1] += tone_at(lvl, 9973, 2.1)
    rows = TP.channel_rows(x)
    v = TP.verdict(rows)[1]
    want = "TONE PRESENT" if lvl > -40 else "TONE ABSENT"
    report(f"T2 two tones at {lvl} dBFS RMS over the floor", f"{want} by the -40 dBFS level rule; share on 0/1",
           [v, rows[0]["share_997"], rows[1]["share_9973"], rows[0]["rms_dbfs"]], v == want)

# ---- the positive control's floor (b6 loop) ----
lp = T6.loop()
raw = os.path.join(WORK, "b6-loop.raw")
open(raw, "wb").write(T6.raw_bytes())
h = hashlib.sha256(open(raw, "rb").read()).hexdigest()
report("L1 regenerated lane B6 loop", "SHA-256 566d3dfa... and 1,536,000 bytes", [h[:16], os.path.getsize(raw)],
       h.startswith("566d3dfa") and os.path.getsize(raw) == 1536000)
base = [A.block_metrics(lp[:, c].astype(np.float64), f) for c, f in ((0, 997), (1, 9973))]
got = [[round(b["level_dbfs"], 2), round(b["f_hz"], 4), round(b["snr_db"], 4), round(b["thdn_db"], 4)] for b in base]
report("L2 the loop's own floor", "ch0 -1.00 dBFS 997 Hz SNR 146.0671 THD+N -146.0647; ch1 SNR 145.9933 THD+N -145.9933",
       got, got[0][3] == -146.0647 and got[0][2] == 146.0671 and got[1][3] == -145.9933)
rot = np.roll(lp[:, 0].astype(np.float64), 12345)
b = A.block_metrics(rot, 997)
report("L3 any one-second window of the loop (a rotation)", "the same THD+N to 4 decimals", round(b["thdn_db"], 4),
       round(b["thdn_db"], 4) == -146.0647)
for err in (1, 2, 8):
    y = rot.copy()
    y[24000] += err
    b = A.block_metrics(y, 997)
    report(f"L4 one sample off by {err} LSB in a block", "THD+N moves at or above the 4th decimal",
           [round(b["thdn_db"], 4), round(b["thdn_db"] + 146.0647, 4)], round(b["thdn_db"], 4) != -146.0647)
y = np.delete(rot, 24000)[:47999]
y = np.concatenate([y, rot[:1]])
b = A.block_metrics(y, 997)
report("L5 one frame dropped in a block", "THD+N far above the floor", round(b["thdn_db"], 2), b["thdn_db"] > -100)

print(json.dumps(dict(all_as_expected=bool(ok_all))))
sys.exit(0 if ok_all else 1)

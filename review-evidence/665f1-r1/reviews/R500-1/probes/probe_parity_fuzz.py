#!/usr/bin/env python3
# R500-1 probe P: section 6.2 verdict parity between the reviewed C codec (as
# the store judges a slot at boot) and scripts/nvm_klj2.py klj2_decode, over
# seeded structured mutations of accepted containers. The reference is given
# exactly the bytes the slot holds up to the IMG_LEN the header names (the
# slot is the blob followed by erased bytes), which is what rule 4 reads.
from __future__ import annotations

import random
import struct
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor

from r500_common import bench

STEM = sys.argv[1] if len(sys.argv) > 1 else "endstation_ax7101_1x1_tdm8"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
JOBS = int(sys.argv[3]) if len(sys.argv) > 3 else 12
SLOT = 65536
b = bench(STEM, "reviewed")
rng = random.Random(0x5001)
rids = sorted(b.frames)
erased = b.erased_frames()


def reseal(blob: bytes) -> bytes:
    return blob[:-4] + struct.pack("<I", zlib.crc32(blob[:-4]) & 0xFFFFFFFF)


def with_len(blob: bytes) -> bytes:
    """Rewrite IMG_LEN to the blob's length and reseal."""
    return reseal(blob[:16] + struct.pack("<I", len(blob)) + blob[20:])


def base_frames():
    k = rng.randrange(3)
    if k == 0:
        return dict(b.frames)
    if k == 1:
        return dict(erased)
    return {r: (erased[r] if rng.random() < 0.5 else b.frames[r]) for r in rids}


def area(frames):
    body = b"".join(frames[r] for r in sorted(frames))
    return body + bytes((-len(body)) % 4)


def build(frames, seq=3, nrec=None):
    a = area(frames)
    hdr = struct.pack("<10I", 0x324A4C4B, 0x00020000, seq, len(frames) if nrec is None else nrec,
                      40 + len(a) + 4, b.ident.entity_id & 0xFFFFFFFF, b.ident.entity_id >> 32,
                      b.ident.model_id & 0xFFFFFFFF, b.ident.model_id >> 32, b.donor.layout)
    return reseal(hdr + a + bytes(4))


def mutate() -> tuple[str, bytes]:
    fr = base_frames()
    kind = rng.randrange(11)
    if kind == 0:   # one header byte, resealed or not
        blob = bytearray(build(fr))
        blob[rng.randrange(40)] ^= 1 << rng.randrange(8)
        return "hdr_byte", reseal(bytes(blob)) if rng.random() < 0.8 else bytes(blob)
    if kind == 1:   # one byte inside a record header, resealed
        blob = bytearray(build(fr))
        r = rng.choice(rids)
        off = 40 + sum(len(fr[x]) for x in rids if x < r) + rng.randrange(8)
        blob[off] = rng.choice([0x00, 0xFF, blob[off] ^ 0x01, rng.randrange(256)])
        return "rec_hdr_byte", reseal(bytes(blob))
    if kind == 2:   # drop, duplicate or swap records
        items = [(r, fr[r]) for r in rids]
        op = rng.randrange(3)
        i = rng.randrange(len(items))
        if op == 0:
            del items[i]
        elif op == 1:
            items.insert(i, items[i])
        else:
            j = rng.randrange(len(items))
            items[i], items[j] = items[j], items[i]
        body = b"".join(x for _, x in items)
        body += bytes((-len(body)) % 4)
        blob = bytearray(build(fr))
        blob = bytes(blob[:40]) + body + bytes(4)
        hdr = blob[:12] + struct.pack("<I", len(items)) + blob[16:40]
        return "reorder", with_len(hdr + blob[40:])
    if kind == 3:   # N_REC off by a little, or reserved bits set
        blob = build(fr)
        n = len(fr) + rng.choice([-2, -1, 1, 2, 0x10000, 0x80000000])
        return "nrec", reseal(blob[:12] + struct.pack("<I", n & 0xFFFFFFFF) + blob[16:])
    if kind == 4:   # IMG_LEN moved, the blob cut or grown to match or not
        blob = build(fr)
        d = rng.choice([-8, -4, -1, 1, 3, 4, 8, 64, 300])
        if d < 0:
            nb = blob[:d - 4] + blob[-4:]
        else:
            nb = blob[:-4] + bytes(rng.randrange(256) for _ in range(d)) + blob[-4:]
        return "img_len", with_len(nb) if rng.random() < 0.7 else reseal(nb)
    if kind == 5:   # a nonzero pad byte, resealed
        blob = bytearray(build(fr))
        raw = 40 + sum(len(fr[x]) for x in rids)
        if raw % 4 == 0:
            blob[raw - 1] ^= 0x40
        else:
            blob[raw] = 0x5A
        return "pad", reseal(bytes(blob))
    if kind == 6:   # an erased header over a framed payload, or the reverse
        r = rng.choice(rids)
        f2 = dict(fr)
        pl = len(b.frames[r]) - 8
        if rng.random() < 0.5:
            f2[r] = b"\xff" * 8 + b.frames[r][8:]
        else:
            f2[r] = b.frames[r][:8] + b"\xff" * pl
        return "erased_face", build(f2)
    if kind == 7:   # one more record after the shape's last, framed or erased
        extra = bytes([0x17, 0x22, b.donor.layout, rng.choice([0xFF, max(rids) + 1, rids[-1]]), 0, 4])
        body = area(fr)[: 40 + sum(len(fr[x]) for x in rids) - 40]
        rec = extra + bytes(2) + bytes(4) if rng.random() < 0.5 else b"\xff" * 12
        body = body + rec
        body += bytes((-len(body)) % 4)
        blob = build(fr)
        hdr = blob[:12] + struct.pack("<I", len(fr) + 1) + blob[16:40]
        return "extra", with_len(hdr + body + bytes(4))
    if kind == 8:   # identity or layout words
        blob = build(fr)
        w = rng.choice([5, 6, 7, 8, 9])
        v = struct.unpack_from("<I", blob, w * 4)[0] ^ (1 << rng.randrange(32))
        return "ident", reseal(blob[: w * 4] + struct.pack("<I", v) + blob[w * 4 + 4:])
    if kind == 9:   # a framed record's payload_length rewritten with its crc16 recomputed
        r = rng.choice(rids)
        f2 = dict(fr)
        pay = b.frames[r][8:]
        newlen = rng.choice([0, 1, max(len(pay) - 1, 0), len(pay) + 1, 0x4000, 0xFFFF])
        h = b.frames[r][:4] + struct.pack(">H", newlen)
        from nvm_klj2 import crc16_ccitt
        f2[r] = h + struct.pack(">H", crc16_ccitt(h + pay)) + pay
        return "plen", build(f2)
    # kind 10: random bit flips anywhere, resealed (a CRC-clean corruption)
    blob = bytearray(build(fr))
    for _ in range(rng.randrange(1, 4)):
        blob[rng.randrange(40, len(blob) - 4)] ^= 1 << rng.randrange(8)
    return "flips", reseal(bytes(blob))


def reference(blob: bytes) -> int:
    slot = blob[:SLOT] + b"\xff" * (SLOT - min(len(blob), SLOT))
    if len(blob) >= 20:
        n = struct.unpack_from("<I", blob, 16)[0]
        if 44 <= n <= SLOT:
            return b.decode(slot[:n])[0]
    return b.decode(blob)[0]


cases = [mutate() for _ in range(N)]


def one(i: int):
    label, blob = cases[i]
    if len(blob) > SLOT:
        return None
    path = b.file(f"fz{i}.bin", blob)
    r = b.run("--slot-a", path, "--boot")
    want = reference(blob)
    return (i, label, r.s["vd_a"], want)


mism, kinds, verdicts = [], {}, {}
with ThreadPoolExecutor(JOBS) as ex:
    for res in ex.map(one, range(N)):
        if res is None:
            continue
        i, label, got, want = res
        kinds[label] = kinds.get(label, 0) + 1
        verdicts[want] = verdicts.get(want, 0) + 1
        if got != want:
            mism.append(res)
print(f"PARITY-FUZZ shape={STEM} cases={sum(kinds.values())} mismatches={len(mism)}")
print("kinds", dict(sorted(kinds.items())))
print("reference verdicts", dict(sorted(verdicts.items())))
for m in mism[:20]:
    print("MISMATCH case=%d kind=%s store=%d reference=%d" % m)

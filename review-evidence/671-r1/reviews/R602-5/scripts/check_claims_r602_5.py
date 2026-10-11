#!/usr/bin/env python3
"""R602-5 reviewer arithmetic checks for #671 / PR #715 round 5.

Usage: check_claims_r602_5.py TREE

1. The CRC-32 residue: for any container whose little-endian CRC-32 trailer
   closes it, zlib's CRC-32 over the whole container is 0x2144df1c, so the
   round-4 refusal digest is one constant over every such container; the
   round-5 comparison (CRC-32 over all but the last four bytes, and the last
   four whole) separates them.
2. The detection claims in BAREMETAL_FIRMWARE.md: every 1-bit, 2-bit and
   <=32-bit-burst difference between two equal-length reads up to the 64 KiB
   slot changes the round-5 comparison (2-bit pairs sampled, bursts sampled).
3. Check 13's case counts per shape from the tree's own generator: total
   generated, inside the detection limit, restart and cold split, and the
   R603-4 class coverage (every sequence of every sealed group, both
   orientations, both entry paths).
"""
import random
import sys
import zlib
from pathlib import Path


def sealed(prefix: bytes) -> bytes:
    return prefix + zlib.crc32(prefix).to_bytes(4, "little")


def cmp_key(read: bytes) -> tuple:
    return (len(read), zlib.crc32(read[:-4]), read[-4:])


def main() -> int:
    tree = Path(sys.argv[1])
    rng = random.Random(6715)
    # 1. residue
    res = set()
    keys = set()
    for n in (40, 44, 3336, 13256, 65536):
        for _ in range(20):
            c = sealed(bytes(rng.randrange(256) for _ in range(n - 4)))
            res.add(zlib.crc32(c))
            keys.add(cmp_key(c))
    print(f"residue values over 100 random sealed containers: {sorted(hex(r) for r in res)}")
    print(f"round-5 comparison keys distinct: {len(keys)} of 100")
    # 2. detection claims, on a 64 KiB read
    n = 65536
    base = bytes(rng.randrange(256) for _ in range(n))
    k0 = cmp_key(base)
    nbits = n * 8
    miss = 0
    trials = 0
    for _ in range(4000):                       # single bits
        b = bytearray(base); i = rng.randrange(nbits); b[i // 8] ^= 1 << (i % 8)
        trials += 1; miss += cmp_key(bytes(b)) == k0
    for _ in range(4000):                       # two bits anywhere
        b = bytearray(base)
        i, j = rng.sample(range(nbits), 2)
        for x in (i, j):
            b[x // 8] ^= 1 << (x % 8)
        trials += 1; miss += cmp_key(bytes(b)) == k0
    for _ in range(4000):                       # bursts of <= 32 bits
        b = bytearray(base); L = rng.randrange(1, 33); s = rng.randrange(nbits - L)
        pat = (1 | (rng.getrandbits(L - 1) << 1) | (1 << (L - 1))) if L > 1 else 1
        for t in range(L):
            if pat >> t & 1:
                b[(s + t) // 8] ^= 1 << ((s + t) % 8)
        trials += 1; miss += cmp_key(bytes(b)) == k0
    print(f"1-bit, 2-bit and <=32-bit burst differences on a 64 KiB read: {miss} undetected of {trials}")
    # 3. check 13's counts
    sys.path.insert(0, str(tree / "sw/firmware/nvm_hosttest"))
    import read_fault_cases as rfc
    from collections import Counter
    for shape, img_len in (("arty_4x4", 4808), ("1x1_tdm8", 3336), ("8x8", 13256)):
        body = 40 + (img_len - 40 - 4) // 2
        cases = rfc.fault_cases(body)
        total = 0
        for restart in (True, False):
            for older, faulted, manners, seqs in rfc.GROUPS:
                for turn, valid in enumerate("ab"):
                    total += len(rfc.windows(rfc.BOOT_READ_BOUND - int(restart))) * len(manners)
        cls = [c for c in cases if c.fault[0] == "--read-sealed" and c.count == 2
               and rfc.expect(c).judgement["ab".index(rfc.faulted_slot(
                   "valid" if c.fault[1][0] == c.valid else "other", c.valid))] == "ffc"]
        combos = Counter((c.older, c.fault[1][0] == c.valid, c.valid, c.restart, c.seq) for c in cls)
        want = {(older, fv, v, r, s) for older, faulted, manners, seqs in rfc.GROUPS
                if any(m in rfc.SEALED for m in manners)
                for fv in [faulted == "valid"] for v in "ab" for r in (True, False) for s in seqs}
        print(f"{shape}: windowed cases generated={total} run={len(cases)} "
              f"restart={sum(c.restart for c in cases)} cold={sum(not c.restart for c in cases)} "
              f"distinct={len(set(cases))}; R603-4 class cases={len(cls)}, "
              f"group x orientation x path x sequence combinations covered="
              f"{len(set(combos) & want)} of {len(want)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

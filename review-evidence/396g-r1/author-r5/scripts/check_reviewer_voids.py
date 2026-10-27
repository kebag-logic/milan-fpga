#!/usr/bin/env python3
"""Do the not-FAIL placements of the reviewer's arm-corruption sweep equal the two stated voids exactly?

Usage: python3 -I check_reviewer_voids.py <tb/tools dir> <r4_arm_corruption_sweep.log>

The sweep (F = 16384, d = -64..64, every channel, eight masks, the reviewer's
arms) prints one NOTFAIL line per placement that is not FAIL with every arm
found. This script predicts each placement's class from the bytes alone with
classify_arm.predict, the same predicate as the self-test's sweep, and
compares: the predicted voids (void-position, void-flip) must be exactly the
NOTFAIL placements, each NOT RUN for that arm. Exit status 0.
"""
import json
import sys
from pathlib import Path

sys.argv, log = [sys.argv[0], sys.argv[1]], sys.argv[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from classify_arm import predict  # noqa: E402
from arm_d4 import arms  # noqa: E402

F = 16384
MASKS = (0x100, 0x200, 0x1E00, 0x40000, 0x80000, 0x80100, 0x100000, 0x01000000)
notfail = {}
for line in open(log, encoding="utf-8"):
    if line.startswith("NOTFAIL"):
        row = json.loads(line[8:])
        notfail[(row["arm"], row["d"], row["ch"], int(row["mask"], 16))] = row
predicted = set()
for ai, (cls, at, size, channel) in enumerate(arms(F)):
    for d in range(-64, 65):
        for ch in range(4):
            for mask in MASKS:
                if predict(F, ai, d, ch, mask) in ("X1", "X2"):
                    predicted.add((at, d, ch, mask))
print("not FAIL", len(notfail), "predicted voids", len(predicted))
print("not FAIL but not a stated void:", sorted(set(notfail) - predicted))
print("stated void but FAIL:", sorted(predicted - set(notfail)))
print("every not-FAIL is NOT RUN with only its arm missed:",
      all(r["verdict"] == "NOT RUN" and r["missed"] == [{"class": c, "index": a, **({"mask": s, "channel": ch}
          if c == "bit-flip" else {"n": s})} for c, a, s, ch in arms(F) if a == k[0]] for k, r in notfail.items()))

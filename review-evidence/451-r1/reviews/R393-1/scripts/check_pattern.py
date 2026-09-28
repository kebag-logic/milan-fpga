#!/usr/bin/env python3
"""Check the DIN pattern source: formula, 65,536-frame periodicity, period hash.
Usage: check_pattern.py <din-pattern.raw>"""
import hashlib, json, sys
import numpy as np
b = open(sys.argv[1], "rb").read()
w = np.frombuffer(b, dtype="<u4").reshape(-1, 8)
n = np.arange(w.shape[0], dtype=np.uint64)
exp = ((((np.arange(8, dtype=np.uint64) + 1)[None, :] << 16) | (n[:, None] & 0xFFFF)) << 8).astype(np.uint32)
P = 65536
per = b[:P * 32]
periodic = all(b[i:i + len(per)] == per[:len(b) - i] for i in range(0, len(b), len(per)))
print(json.dumps({"bytes": len(b), "frames": int(w.shape[0]), "seconds": w.shape[0] / 48000,
                  "matches_formula_all_words": bool(np.array_equal(w, exp)),
                  "periodic_65536_frames": periodic,
                  "first_period_bytes": len(per), "first_period_sha256": hashlib.sha256(per).hexdigest()}, indent=1))

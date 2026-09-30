#!/usr/bin/env python3
"""Regenerate the DIN pattern period independently: 65,536 frames x 8 channels
of S32_LE, word ((t << 16) | n) << 8 for tag t = c + 1, and print its SHA-256."""
import hashlib, struct
b = b"".join(struct.pack("<8I", *[(((c + 1) << 16) | n) << 8 for c in range(8)]) for n in range(65536))
print(len(b), hashlib.sha256(b).hexdigest())

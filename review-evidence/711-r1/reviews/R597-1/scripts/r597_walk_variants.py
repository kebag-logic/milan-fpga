#!/usr/bin/env python3
"""Probe copies only: rewrite srp_latency.cpp's MVRP walk or the lwSRP pin check.

Usage: python3 -I r597_walk_variants.py <checkout> <variant> [<variant>...]
Variants: oldwalk (the base walk, keeping the new end assertion), oldwalk-noassert
(the exact base walk), vecsize (vector size n/3 instead of (n+2)/3), noendskip
(drop the Message EndMark skip), pinold (LWSRP_REV = 9197193e).
"""
import sys
from pathlib import Path
root = Path(sys.argv[1])
lat = root / "sw/firmware/ctrl/test/srp_latency.cpp"
arms = root / "sw/firmware/ctrl/test/ctrl_arms.py"
NEW_WALK = """                else { // 802.1Q-2018 10.8.1.2: a Message holds vectors up to its EndMark.
                       while(off+2<=f->len && (f->bytes[off] || f->bytes[off+1])) {
                           const unsigned n=wire_be16(f->bytes+off)&8191u;
                           off+=2+width+(n+2)/3;
                       }
                       off+=2; }
"""
OLD_WALK = """                else { const unsigned n=wire_be16(f->bytes+off)&8191u;
                       off+=2+width+(n+2)/3+2; }
"""
ASSERT = """            ASSERT_TRUE(off+2<=f->len && !f->bytes[off] && !f->bytes[off+1])
                <<"walk must end on the MRPDU EndMark";
"""
def sub(path, old, new):
    t = path.read_text(); assert t.count(old) == 1, (path, old[:40]); path.write_text(t.replace(old, new))
for v in sys.argv[2:]:
    if v == "oldwalk": sub(lat, NEW_WALK, OLD_WALK)
    elif v == "oldwalk-noassert": sub(lat, NEW_WALK, OLD_WALK); sub(lat, ASSERT, "")
    elif v == "vecsize": sub(lat, "off+=2+width+(n+2)/3;", "off+=2+width+n/3;")
    elif v == "noendskip": sub(lat, "                       off+=2; }\n", "                       }\n")
    elif v == "pinold": sub(arms, 'LWSRP_REV = "08ee86e812a0eb5e1dc6cd61b494d8baf3491348"',
                            'LWSRP_REV = "9197193e47a6bb1c45a56d90a18c1784123aba44"')
    else: raise SystemExit(f"unknown variant {v}")
    print("applied", v, "to", root)

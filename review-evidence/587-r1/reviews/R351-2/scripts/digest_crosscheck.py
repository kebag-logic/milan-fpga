#!/usr/bin/env python3
"""Cross-check: the new committed digest names the same generated Verilog as round 1.

Usage: digest_crosscheck.py VERILOG CHECKOUT_ROOT
Hashes the export's Verilog after comment stripping with the checkout root replaced by
(a) $REPO (the ce654301 rule), (b) $BUILD (the 55079500 rule as written, round-1 value 1f7c01e2...),
(c) the executor's published checkout path (round-1 committed value 3d371f2d...), and
(d) a one-byte non-comment mutation under rule (a) (must differ: sensitivity control).
"""
import hashlib, re, sys
text = open(sys.argv[1], encoding="utf-8", newline="").read()
root = sys.argv[2]
def norm(t, token):
    t = t.replace(root, token)
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.DOTALL)
    t = re.sub(r"//[^\n]*", "", t)
    return hashlib.sha256(t.encode()).hexdigest()
print("a  checkout -> $REPO                     ", norm(text, "$REPO"))
print("b  checkout -> $BUILD (old rule)          ", norm(text, "$BUILD"))
print("c  checkout -> executor published lane    ", norm(text, "$LANES/587-8x8-baseline-50mhz"))
i = text.index("CLK_HZ_P")
mut = text.replace("PP_UCODE_HEX_P", "PP_UCODE_HEX_Q", 1)
print("d  mutation (one identifier byte), rule a ", norm(mut, "$REPO"))

#!/usr/bin/env python3
"""Replace the place(E_SINFO, [...]) block of a gen_ucode.py (and any asserts that
directly follow it) with the same block of another gen_ucode.py.

Usage: splice_sinfo.py TARGET_GEN_UCODE SOURCE_GEN_UCODE
Each block must be found exactly once in each file; the script refuses otherwise.
"""
import re
import sys

PAT = re.compile(r"^place\(E_SINFO, \[\n.*?^\]\)\n(?:assert rom\[E_SINFO[^\n]*\n)*", re.S | re.M)


def block(text: str, what: str) -> re.Match:
    found = list(PAT.finditer(text))
    if len(found) != 1:
        raise SystemExit(f"{what}: {len(found)} E_SINFO blocks, expected exactly 1")
    return found[0]


target, source = sys.argv[1], sys.argv[2]
t = open(target).read()
s = open(source).read()
mt, ms = block(t, target), block(s, source)
open(target, "w").write(t[:mt.start()] + ms.group(0) + t[mt.end():])
print(f"spliced {len(ms.group(0).splitlines())} lines over {len(mt.group(0).splitlines())}")

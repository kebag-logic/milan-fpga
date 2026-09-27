#!/usr/bin/env python3
"""Write two disposable mutant packers derived from the head packer.

Usage: make_mutants.py <head gen_desc_image.py> <out dir>

M1 deletes the body/key agreement check (PR #124).  The four body/key probe
rows must flip to MISMATCH and nothing else.
M2 adds the L10 offset/count/length and L6 identity-list refusals that the
document says are NOT enforced.  The six "not enforced" rows must flip; the
L10 eight-entry boundary and every control must still pass.
"""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)

check = "        if (body_type, body_index) != (typ, idx):\n"
assert src.count(check) == 1
m1 = src.replace(check, "        if False:\n")
(out / "mutant_M1_no_body_key.py").write_text(m1, encoding="utf-8")

anchor = "        nidx = _u(desc.get(\"name_index\", NAME_NONE))\n"
assert src.count(anchor) == 1
inject = '''        if typ == 0x0002:
            off = int.from_bytes(body[140:142], "big")
            cnt = int.from_bytes(body[142:144], "big")
            if off != 144 or cnt > 8 or len(body) != 144 + 4 * cnt:
                raise ImageError("L10 mutant refusal")
        if typ == 0x0024:
            cnt = int.from_bytes(body[74:76], "big")
            lst = [int.from_bytes(body[76 + 2 * i:78 + 2 * i], "big")
                   for i in range(cnt)]
            if lst != list(range(cnt)) or len(body) != 76 + 2 * cnt:
                raise ImageError("L6 mutant refusal")
'''
m2 = src.replace(anchor, inject + anchor)
(out / "mutant_M2_l6_l10.py").write_text(m2, encoding="utf-8")
print("wrote", out / "mutant_M1_no_body_key.py", out / "mutant_M2_l6_l10.py")

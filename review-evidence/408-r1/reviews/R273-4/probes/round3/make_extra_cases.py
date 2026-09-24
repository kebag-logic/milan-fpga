#!/usr/bin/env python3
"""Extra hostile shapes for R273-3: a splice and a paste inside the AEM
verifier (outside the six boot-path bodies, where the bans are retired onto
the resolver), and a header-supplied concatenation macro forging the
identity sample inside milan_init() (a paste no firmware #define carries).

usage: make_extra_cases.py <repo-root> <out.json>
"""
import json
from pathlib import Path
import sys


def once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new, 1)


def main():
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    fw = (root / "sw/firmware/milan_baremetal/milan_baremetal.c").read_text(
        encoding="utf-8")
    magic_check = "\tif (src[0] != 'A' || src[1] != 'E'"
    guard = "\tif (id != MILAN_ID_MAGIC) {"
    anchor = "#define MILAN_PTP_SNAPSHOT   0x4u\n"
    cases = [
        {"label": "X1 verifier returns 1 before the CRC through a "
                  "token-joining splice of `return`",
         "firmware": once(fw, magic_check, "\tret\\\nurn 1;\n" + magic_check)},
        {"label": "X2 verifier returns 1 before the CRC through a ## paste "
                  "of `return`",
         "firmware": once(once(fw, magic_check,
                               "\tMILAN_R(ret, urn) 1;\n" + magic_check),
                          anchor, anchor + "#define MILAN_R(a, b) a##b\n")},
        {"label": "X3 control: verifier returns 1 before the CRC, spelled "
                  "plainly",
         "firmware": once(fw, magic_check, "\treturn 1;\n" + magic_check)},
        {"label": "X4 identity sample forged through the libc header's "
                  "__CONCAT paste (no firmware #define)",
         "firmware": once(fw, guard,
                          "\t__CONCAT(i, d) = MILAN_ID_MAGIC;\n" + guard)},
    ]
    out.write_text(json.dumps(cases, indent=1) + "\n", encoding="utf-8")
    print(f"{len(cases)} cases -> {out}")


if __name__ == "__main__":
    main()

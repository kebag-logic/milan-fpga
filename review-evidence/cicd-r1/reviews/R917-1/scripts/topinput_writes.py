#!/usr/bin/env python3
"""Detect the #996 mechanism in generated code: model code assigning a top-level input.

usage: topinput_writes.py OBJDIR [OBJDIR ...]
Top-level inputs are the VL_IN*/VL_INW declarations of the model's root header.
Any generated statement `vlSelfRef.<input> = ...` / `vlSelf-><input> = ...` other
than the constructor's random/zero reset is reported. Exit 0 = none, 1 = found.
"""
import re
import sys
from pathlib import Path

DECL = re.compile(r"VL_IN(?:8|16|64|W)?\(&?([A-Za-z0-9_]+)\s*,")


def main() -> int:
    found = 0
    for arg in sys.argv[1:]:
        obj = Path(arg)
        header = "".join(p.read_text() for p in obj.glob("*___024root.h"))
        inputs = sorted(set(DECL.findall(header)))
        hits = []
        for cpp in sorted(obj.glob("*___024root*.cpp")):
            for n, line in enumerate(cpp.read_text().splitlines(), 1):
                for name in inputs:
                    if re.search(r"vlSelf(?:Ref\.|->)" + re.escape(name) + r"\s*=(?!=)", line) \
                            and "RAND_RESET" not in line:
                        hits.append(f"{cpp.name}:{n}: {line.strip()}")
        print(f"{obj.parent.name}/{obj.name}: {len(inputs)} top inputs; model writes to a top input: {hits or 'none'}")
        found += bool(hits)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Compare Yosys `write_verilog -noattr` netlists, base vs head, modulo private names.

usage: canon_net.py OUTDIR TOP...   (env NET_SUFFIX selects the netlist, default .net.v)
Yosys private names, and escaped names derived from them, carry the lowered file's line (`$eq$all.v:123$45`) and a global
counter; both move when unrelated source lines move. Each escaped name holding a `$` is
replaced by its order of first appearance, so two netlists compare equal exactly
when they are the same structure with the same public names.
Exit 0 = every TOP canonicalizes identically.
"""
import hashlib
import os
import re
import sys
from pathlib import Path

PRIVATE = re.compile(r"\\\S*\$\S*")


def canon(text: str) -> str:
    """Rename every private escaped identifier by first appearance."""
    seen: dict[str, str] = {}

    def sub(found: re.Match[str]) -> str:
        """The stable stand-in for one private name."""
        return seen.setdefault(found.group(0), f"\\$p{len(seen)}")
    return PRIVATE.sub(sub, text)


def main() -> int:
    """Print one IDENTICAL or DIFFERS line per top."""
    out, tops = Path(sys.argv[1]), sys.argv[2:]
    rc = 0
    for top in tops:
        digests = [hashlib.sha256(canon((out / side / (top + os.environ.get("NET_SUFFIX", ".net.v"))).read_text()).encode())
                   .hexdigest() for side in ("base", "head")]
        same = digests[0] == digests[1]
        rc |= not same
        print(f"{'IDENTICAL' if same else 'DIFFERS  '} {top} base {digests[0]} head {digests[1]}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())

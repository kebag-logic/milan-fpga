#!/usr/bin/env python3
"""Replace the reviewer host's home directory prefix with the literal `$HOME`
in every receipt, in place, and report how many substitutions each file got.

The prefix reaches the receipts only through the census compiler selector
(`$HOME/br-milan-rv32/host/bin/riscv32-linux-gcc`), which gate 1b derives from
the home directory. Nothing else in any receipt is changed.
Usage: redact_home.py <receipts-dir> <home-prefix>"""
import sys
from pathlib import Path


def main() -> int:
    root, prefix = Path(sys.argv[1]), sys.argv[2]
    assert prefix.startswith("/") and len(prefix) > 1, prefix
    total = 0
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        data = path.read_bytes()
        count = data.count(prefix.encode())
        if count:
            path.write_bytes(data.replace(prefix.encode(), b"$HOME"))
            total += count
            print(f"{count:6d}  {path.relative_to(root)}")
    print(f"{total} substitution(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

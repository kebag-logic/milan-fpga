#!/usr/bin/env python3
"""Compare probe logs of two heads, file by file.

Usage: python3 -I compare_probe_logs.py <base dir> <head dir>

Each *.log and *.rc in the base directory is compared with the file of the same
name in the head directory: byte-identical, identical once the missed-arm void
reason of the head is written as the base's, or different. Exit 1 when any file
differs or is missing.
"""
import sys
from pathlib import Path

OLD = "void: a planted arm was missed"
NEW = ("void: a planted arm was missed; the source may not have planted it, or a DUT "
       "event at its sample may have masked it")


def main() -> int:
    base, head = Path(sys.argv[1]), Path(sys.argv[2])
    bad = 0
    for path in sorted(base.iterdir()):
        if path.suffix not in (".log", ".rc"):
            continue
        other = head / path.name
        if not other.exists():
            print(f"MISSING  {path.name}")
            bad += 1
            continue
        a, b = path.read_bytes(), other.read_bytes()
        if a == b:
            print(f"IDENTICAL {path.name}")
        elif a == b.replace(NEW.encode(), OLD.encode()):
            print(f"IDENTICAL-BUT-REASON {path.name} ({b.count(NEW.encode())} reason(s) rewritten)")
        else:
            print(f"DIFFERENT {path.name}")
            bad += 1
    print(f"{'PASS' if not bad else 'FAIL'}: {bad} file(s) differ or are missing")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

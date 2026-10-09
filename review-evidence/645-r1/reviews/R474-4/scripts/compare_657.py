#!/usr/bin/env python3
"""Compare two tdm8render-mutants transcripts line set by line set (R474-4).

Usage: compare_657.py DEV_LOG HEAD_LOG

Reads every line starting "[PASS]" or "[FAIL]". Prints the counts, the FAIL
lines of each, the lines only in one of them, and exits 0 when every dev
outcome line appears unchanged in the head transcript and the head's FAIL
lines equal dev's (the #657 comparison the round-2e assignment asks for).
"""
import sys
from pathlib import Path


def outcomes(path: Path) -> list[str]:
    return [ln.rstrip() for ln in path.read_text(errors="replace").splitlines()
            if ln.startswith("[PASS]") or ln.startswith("[FAIL]")]


def main() -> int:
    dev, head = (outcomes(Path(p)) for p in sys.argv[1:3])
    dfail = [x for x in dev if x.startswith("[FAIL]")]
    hfail = [x for x in head if x.startswith("[FAIL]")]
    print(f"dev: {len(dev) - len(dfail)}/{len(dev)} pass; head: {len(head) - len(hfail)}/{len(head)} pass")
    print("dev FAIL lines:", *dfail, sep="\n  ")
    print("head FAIL lines:", *hfail, sep="\n  ")
    only_dev = [x for x in dev if x not in head]
    only_head = [x for x in head if x not in dev]
    print("only in dev:", *only_dev, sep="\n  ")
    print("only in head:", *only_head, sep="\n  ")
    ok = not only_dev and sorted(dfail) == sorted(hfail)
    print("COMPARISON:", "MATCH (no regression against dev)" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

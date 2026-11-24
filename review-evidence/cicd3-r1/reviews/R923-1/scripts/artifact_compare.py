#!/usr/bin/env python3
"""Compare two hosted suite-logs artifacts (base and head) of one worker.

usage: python3 -I artifact_compare.py BASE_DIR HEAD_DIR

Receipts (cases/*.json) are compared field by field with only `head` and
`tree` allowed to differ. Suite logs (*.log) are compared line by line after
masking timing figures, temporary names and the staging directory names, and
the differing line count is printed per log. The preflight/ directory is
listed for each side.
"""

import json
import re
import sys
from pathlib import Path

MASK = (
    (re.compile(r"\d+(\.\d+)?\s*(s|ms|sec|seconds|min)\b"), "<T>"),
    (re.compile(r"/tmp/\S+"), "<TMP>"),
    (re.compile(r"milan-mutant-stage-\d+/"), ""),
    (re.compile(r"(?<=[-_])[a-z0-9_]{8}(?=[/\s:'\"]|$)"), "<RAND>"),
    (re.compile(r"\b\d{2}:\d{2}:\d{2}\b"), "<CLOCK>"),
    (re.compile(r"pid[ =]\d+|\bPID \d+"), "<PID>"),
)
DROP = re.compile(r"^(- V e r i l a t i o n|- Verilator:|%Warning|make(\[\d+\])?:|ccache)")


def normal(path: Path) -> list[str]:
    out = []
    for line in path.read_text(errors="replace").splitlines():
        if DROP.match(line):
            continue
        for pattern, repl in MASK:
            line = pattern.sub(repl, line)
        out.append(line.rstrip())
    return out


def main() -> int:
    base, head = Path(sys.argv[1]), Path(sys.argv[2])
    for receipt in sorted((base / "cases").glob("*.json")):
        b = json.loads(receipt.read_text())
        h = json.loads((head / "cases" / receipt.name).read_text())
        keys = sorted((set(b) | set(h)) - {"head", "tree"})
        same = all(b.get(k) == h.get(k) for k in keys)
        print(f"receipt {receipt.name}: {'IDENTICAL' if same else 'DIFFER'} outside head/tree "
              f"({len(b.get('results', []))} cases; head {b.get('head', '')[:8]} -> {h.get('head', '')[:8]})")
    for log in sorted(base.glob("*.log")):
        other = head / log.name
        if not other.exists():
            print(f"log {log.name}: MISSING at head")
            continue
        a, b = normal(log), normal(other)
        diff = sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))
        print(f"log {log.name}: {len(a)} vs {len(b)} normalised lines, {diff} differing")
    for side, root in (("base", base), ("head", head)):
        pre = root / "preflight"
        names = sorted(p.name for p in pre.iterdir()) if pre.is_dir() else []
        print(f"{side} preflight/: {names if names else 'absent or empty'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

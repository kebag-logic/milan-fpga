#!/usr/bin/env python3
"""Compare mutation-driver transcripts between arms.

usage: mutcompare.py DIR

DIR holds <suite>-<driver>-<arm>-<cold|warm>.{log,rc} files. Every arm's log is
compared with base-cold after masking host text only: scratch and staging
directory names (the thing the change under review moves), Verilator's own
statistics and warnings, make chatter and compiler echoes. Every remaining
line, including every check, verdict and figure, must match. Drivers that
print results as parallel arms finish are nondeterministic in ORDER at the
base too, so the multiset of lines is compared as well as the sequence, and
both answers are printed.
"""

import collections
import re
import sys
from pathlib import Path

MASKS = (
    (re.compile(r"/\S*/scratch/tmp-g?(base|head)/\S*"), "<TMP>"),
    (re.compile(r"/\S*/scratch/g?(base|head)/"), "<TREE>/"),
    (re.compile(r"milan-mutant-stage-\d+/"), ""),
    (re.compile(r"(?<=[-_])[a-z0-9_]{8}(?=[/\s:'\"]|$)"), "<RAND>"),
    (re.compile(r"(?<=[-_])\d(?=[/\s:'\"]|$)"), "<RAND>"),
)
DROP = re.compile(
    r"^(- V e r i l a t i o n|- Verilator:|%Warning|\s*:\s*\.\.\.|make(\[\d+\])?:|ccache|g\+\+ |"
    r"\s*\^|\s+\|)")


def normal(text: str) -> list[str]:
    """Lines with host text masked and host-only lines dropped."""
    lines = []
    for line in text.splitlines():
        if DROP.match(line):
            continue
        for pattern, repl in MASKS:
            line = pattern.sub(repl, line)
        lines.append(line.rstrip())
    return lines


VERDICT = re.compile(r"PASS|FAIL|caught|named|rejection|checks|survived|killed|mutant", re.I)


def main() -> int:
    directory = Path(sys.argv[1])
    groups = collections.defaultdict(dict)
    for log in sorted(directory.glob("*.log")):
        stem = log.stem
        m = re.match(r"(.+)-(base|head)-(cold|warm)$", stem)
        if not m:
            continue
        rc_file = log.with_suffix(".rc")
        rc = rc_file.read_text().split()[0] if rc_file.exists() else "rc=MISSING"
        groups[m.group(1)][f"{m.group(2)}-{m.group(3)}"] = (normal(log.read_text()), rc)
    bad = 0
    for name, arms in sorted(groups.items()):
        ref = arms.get("base-cold")
        if ref is None:
            print(f"{name}: base-cold MISSING")
            bad += 1
            continue
        verdicts = sum(1 for line in ref[0] if VERDICT.search(line))
        for arm in ("base-warm", "head-cold", "head-warm"):
            if arm not in arms:
                print(f"{name}: {arm} MISSING")
                bad += 1
                continue
            lines, rc = arms[arm]
            seq = lines == ref[0]
            bag = collections.Counter(lines) == collections.Counter(ref[0])
            same_rc = rc == ref[1]
            verdict = ("IDENTICAL" if seq else "IDENTICAL-AS-MULTISET" if bag else "DIFFER")
            if not (bag and same_rc):
                bad += 1
            print(f"{name}: base-cold vs {arm}: {verdict}, {rc} vs {ref[1]} "
                  f"({len(ref[0])} normalised lines, {verdicts} verdict lines)")
            if not bag:
                missing = collections.Counter(ref[0]) - collections.Counter(lines)
                extra = collections.Counter(lines) - collections.Counter(ref[0])
                for line in list(missing.elements())[:10]:
                    print(f"    - {line}")
                for line in list(extra.elements())[:10]:
                    print(f"    + {line}")
    print(f"groups: {len(groups)}, differing or missing comparisons: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

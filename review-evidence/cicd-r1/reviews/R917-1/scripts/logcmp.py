#!/usr/bin/env python3
"""Compare a suite log at the base with the same suite's log at the head.

usage: logcmp.py BASE.log BASE_TREE HEAD.log HEAD_TREE [--multiset]

Only host-dependent text is removed; every other byte must match:
  * the tree's absolute path (each log's own tree) -> <TREE>; the reviewer's
    scripts directory -> <SCRIPTS>;
  * Verilator's build-statistics lines ("- V e r i l a t i o n   R e p o r t",
    "- Verilator: Built from ...", "- Verilator: Walltime ...": timing and the
    byte size of the inputs, which the probes.vlt file itself changes);
  * make's "Entering/Leaving directory" chatter;
  * temporary directory names (tempfile suffixes) -> <TMP>;
  * the one intended difference: on a Verilator command echo line, the base's
    `--public-flat-rw` is rewritten to `probes.vlt` (so the rest of that command
    line is still compared byte for byte).
Exit 0 = identical after normalisation, 1 = differs (a unified diff is printed).
"""
import difflib
import re
import sys
from collections import Counter

DROP = re.compile(r"^(- V e r i l a t i o n   R e p o r t|- Verilator: (Built from|Walltime)|make(\[\d+\])?: (Entering|Leaving) directory)")
TMP = re.compile(r"(/tmp/[A-Za-z0-9_.-]*?)[A-Za-z0-9_]{8}(?=/|\b)")
SCRIPTS = "$REVIEWS/cicd-r917-1-packet/scripts"


def normalise(path: str, tree: str, base: bool) -> tuple[list[str], Counter]:
    out, dropped = [], Counter()
    for raw in open(path, encoding="utf-8", errors="replace").read().splitlines():
        line = raw.replace(tree, "<TREE>").replace(SCRIPTS, "<SCRIPTS>")
        if DROP.match(line):
            dropped[DROP.match(line).group(0)[:30]] += 1
            continue
        line = TMP.sub(r"\1<TMP>", line)
        is_verilator_cmd = line.startswith("<SCRIPTS>/vwrap.sh ") or line.startswith("verilator ")
        if base and is_verilator_cmd and "--public-flat-rw" in line:
            line = line.replace("--public-flat-rw", "probes.vlt")
            dropped["(rewritten) --public-flat-rw -> probes.vlt"] += 1
        out.append(line)
    return out, dropped


def main() -> int:
    b, bt, h, ht = sys.argv[1:5]
    multiset = "--multiset" in sys.argv
    bl, bd = normalise(b, bt, True)
    hl, hd = normalise(h, ht, False)
    print(f"base {len(bl)} compared lines, removed/rewritten {dict(bd)}")
    print(f"head {len(hl)} compared lines, removed {dict(hd)}")
    same = (Counter(bl) == Counter(hl)) if multiset else (bl == hl)
    if same:
        print("IDENTICAL" + (" (as a multiset of lines)" if multiset else ""))
        return 0
    print("DIFFERENT")
    for line in difflib.unified_diff(bl, hl, "base", "head", n=1, lineterm=""):
        print(line[:300])
    return 1


if __name__ == "__main__":
    sys.exit(main())

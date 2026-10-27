#!/usr/bin/env python3
"""From a par_mutants.py output directory and a list of check names, map
every listed check to the controls whose run failed it, and re-apply the
tree's own named-check rule (mutants.py named_verdict) per control.

Usage: kill_map.py <mut-outdir> <check-names.txt> <out.json>
Prints the unkilled names and the controls that break the tree's rule.
"""
import json
import re
import sys
from pathlib import Path

P1 = "p1 255 "
STRICT = ("#82 ", "#84 ", "#85 ", "#89 ", "#90 ", "#91 ", P1)


def failed_names(lines):
    out = set()
    for line in lines:
        body = line[len("FAIL "):]
        m = re.match(r"(.*?)\s+got [0-9a-f]+ exp [0-9a-f]+$", body)
        out.add((m.group(1) if m else body).rstrip())
    return out


def main() -> int:
    outdir, names_file, out_json = map(Path, sys.argv[1:4])
    summary = json.loads((outdir / "summary.json").read_text())
    names = [n for n in names_file.read_text().splitlines() if n]
    kills = {n: [] for n in names}
    rule_breaks = []
    for c in summary["controls"]:
        lines = c.get("fail_lines", [])
        fn = failed_names(lines)
        for n in names:
            if n in fn:
                kills[n].append(c["index"])
        breaks = " | ".join(c["breaks"])
        if c.get("answer") != "caught":
            rule_breaks.append((c["index"], c["name"], c.get("answer")))
            continue
        if breaks.startswith("slew:"):
            if not any(breaks in l and not l.startswith("FAIL " + P1)
                       for l in lines):
                rule_breaks.append((c["index"], c["name"], "slew name missed"))
        elif breaks.startswith(STRICT):
            for want in c["breaks"]:
                mine = want.startswith(P1)
                if not any(want in l and l.startswith("FAIL " + P1) == mine
                           for l in lines):
                    rule_breaks.append((c["index"], c["name"],
                                        f"missed {want}"))
    unkilled = [n for n, k in kills.items() if not k]
    Path(out_json).write_text(json.dumps(
        {"controls": summary["total"], "caught": summary["caught"],
         "clean": summary["clean"], "names": len(names),
         "unkilled": unkilled, "rule_breaks": rule_breaks,
         "kills": kills}, indent=1))
    print(f"clean={summary['clean']} controls={summary['total']} "
          f"caught={summary['caught']} names={len(names)} "
          f"unkilled={len(unkilled)} rule_breaks={len(rule_breaks)}")
    for n in unkilled:
        print("UNKILLED", n)
    for r in rule_breaks:
        print("RULE", *r)
    return 0


if __name__ == "__main__":
    sys.exit(main())

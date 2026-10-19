"""usage: r3_oldrows.py <receipts-dir>
For each kept failure-set comparison, check its detailed rows (DIFFER, HEAD ONLY, BASE
ONLY) against the round-3 comparison: the names must be the changed, added and removed
mutants plus any baseline the old script listed as a mutant, and each row's failure IDs
must equal the round-3 multiset. rc 1 on any disagreement."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r3_supersedes import PAIRS  # noqa: E402

ROW = re.compile(r"^(DIFFER|HEAD ONLY|BASE ONLY) (\S+): (?:base )?(\d+): ?(.*)$")
HEADROW = re.compile(r"^\s+head (\d+): ?(.*)$")


def expand(text: str) -> list[str]:
    """The round-3 'ID xN' list as a sorted multiset."""
    out = []
    for item in filter(None, (s.strip() for s in text.split(","))):
        name, _, n = item.partition(" x")
        out += [name] * (int(n) if n else 1)
    return sorted(out)


def main() -> int:
    root = Path(sys.argv[1])
    bad = 0
    for old, new in PAIRS:
        if not old:
            continue
        s = json.loads((root / f"{new}.json").read_text())
        rows, last = {}, None
        for line in (root / old).read_text().splitlines():
            if m := ROW.match(line):
                last = m.group(2)
                rows[last] = {"kind": m.group(1), "ids": sorted(filter(None, (x.strip() for x in m.group(4).split(","))))}
            elif (m := HEADROW.match(line)) and last:
                rows[last]["head"] = sorted(filter(None, (x.strip() for x in m.group(2).split(","))))
        text = (root / f"{new}.txt").read_text()
        want = set(s["mutants"]["changed"]) | set(s["mutants"]["added"]) | set(s["mutants"]["removed"])
        baseline_rows = {n for n in rows if f"  baseline {n}:" in text}
        names_ok = set(rows) - baseline_rows == want
        ids_ok = True
        for n in want & set(rows):
            r = rows[n]
            if r["kind"] == "DIFFER":
                m = re.search(rf"CHANGED {re.escape(n)}: base \d+: (.*)\n\s+head \d+: (.*)", text)
                ids_ok &= bool(m) and expand(m.group(1)) == r["ids"] and expand(m.group(2)) == r["head"]
            else:
                tag = "ADDED" if r["kind"] == "HEAD ONLY" else "REMOVED"
                m = re.search(rf"{tag} {re.escape(n)} \(\w+\): \d+: (.*)", text)
                ids_ok &= bool(m) and expand(m.group(1)) == r["ids"]
        ok = names_ok and ids_ok
        bad += not ok
        print(f"{'AGREE' if ok else 'DISAGREE'} {old}: {len(rows)} rows = {len(want)} changed/added/removed "
              f"mutants + {len(baseline_rows)} baselines listed as mutants"
              + (f" ({', '.join(sorted(baseline_rows))})" if baseline_rows else "")
              + ("" if ids_ok else "; failure IDs differ"))
    print(f"{bad} disagreements")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

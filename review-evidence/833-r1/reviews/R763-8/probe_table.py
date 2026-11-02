"""Cross-check the cleanup table in docs/testing/TESTING.md against MUTANTS.

Usage: python3 -I probe_table.py <clone>
Prints: mutants named in no row, names in rows that are not mutants, names in more than one row, and for
each row whether each named mutant's control is named in that row's 'Pinned by' cell.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import process_test_support as s  # noqa: E402

text = (root / "docs/testing/TESTING.md").read_text()
rows = [line for line in text.splitlines()
        if line.startswith("| ") and line.count(" | ") >= 2 and "Stated cleanup behaviour" not in line]
rows = [r for r in rows if "owner_" in r]
seen = {}
bad = []
for row in rows:
    cells = [c.strip() for c in row.strip("|").split(" | ")]
    behaviour, pinned, mutants = cells[0], cells[1], cells[2]
    names = re.findall(r"`([^`]+)`", mutants)
    controls = set(re.findall(r"`(owner_[a-z_]+)`", pinned))
    for name in names:
        seen.setdefault(name, []).append(behaviour[:50])
        if name not in s.MUTANTS:
            bad.append(f"not a mutant: {name}")
            continue
        control = s.MUTANTS[name][0]
        if control and control not in controls:
            bad.append(f"{name}: control {control} not named in its row '{behaviour[:50]}'")
unnamed = sorted(n for n in s.MUTANTS if n != "none" and n not in seen)
multi = {n: r for n, r in seen.items() if len(r) > 1}
print(f"rows {len(rows)} mutants {len(s.MUTANTS) - ('none' in s.MUTANTS)} named {len(seen)}")
print(f"unnamed: {unnamed}")
print(f"in more than one row: {multi}")
print("problems:" if bad else "problems: none")
for line in bad:
    print("  " + line)
no_control = sorted(n for n, v in s.MUTANTS.items() if n != "none" and not v[0])
print(f"no control: {no_control}")

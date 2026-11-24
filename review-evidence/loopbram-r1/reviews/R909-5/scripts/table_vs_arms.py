#!/usr/bin/env python3
"""Cross-check the CI policy's suite-budget table against run_all_suites.sh.

Usage: python3 -I table_vs_arms.py <repo-root>

Checks, at the checkout given:
  1. every named suite_timeout arm appears in the table with the same seconds;
  2. every table row naming a suite matches the arm the driver gives it
     (named arm, or the '*' default arm);
  3. the 'every other default suite' row equals the '*' arm, and every
     discovered suite under tb/verilator without a table row gets the '*' arm;
  4. PROVISIONAL_SUITES in scripts/suite_shards.py equals the set of rows whose
     basis says 'provisional'.
Exit 0 when all hold, 1 otherwise.
"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
driver = (root / "scripts/run_all_suites.sh").read_text()
policy = (root / "docs/testing/CI_WORKFLOWS.md").read_text()
selector = (root / "scripts/suite_shards.py").read_text()

body = re.search(r"suite_timeout\(\) \{\n  case \"\$1\" in\n(.*?)\n  esac", driver, re.S).group(1)
arms = {}
for m in re.finditer(r"^\s*(\S+)\)\s+printf '%s\\n' \"\$\{SUITE_TIMEOUT:-(\d+)\}\"", body, re.M):
    arms[m.group(1)] = int(m.group(2))
default = arms.pop("*")

start = policy.index("| Suite | Budget | Basis |")
rows = []
for line in policy[start:].splitlines()[2:]:
    if not line.startswith("|"):
        break
    cells = [c.strip() for c in line.strip("|").split("|")]
    rows.append(cells)

bad = 0
named = {}
other = None
provisional_rows = set()
for suite_cell, budget, basis in (r[:3] for r in rows):
    secs = int(re.match(r"(\d+) s", budget).group(1))
    names = re.findall(r"`([a-z0-9_]+)`", suite_cell)
    if suite_cell.startswith("every other default suite"):
        other = secs
        continue
    for n in names:
        named[n] = secs
        if basis.startswith("provisional"):
            provisional_rows.add(n)

print(f"driver named arms: {sorted(arms.items())}; '*' arm {default} s")
print(f"table rows: {sorted(named.items())}; 'every other' {other} s")
for s, v in sorted(arms.items()):
    ok = named.get(s) == v
    bad += not ok
    print(f"arm {s} {v} s -> table {named.get(s)} : {'OK' if ok else 'MISMATCH'}")
for s, v in sorted(named.items()):
    want = arms.get(s, default)
    ok = v == want
    bad += not ok
    print(f"row {s} {v} s -> driver gives {want} s : {'OK' if ok else 'MISMATCH'}")
ok = other == default
bad += not ok
print(f"'every other default suite' {other} s vs '*' {default} s : {'OK' if ok else 'MISMATCH'}")
suites = sorted(p.parent.name for p in (root / "tb/verilator").glob("*/Makefile"))
unlisted = [s for s in suites if s not in named]
wrong = [s for s in unlisted if arms.get(s, default) != other]
bad += bool(wrong)
print(f"discovered suites {len(suites)}; without a row {len(unlisted)}; of those not at {other} s: {wrong}")
prov = set(re.findall(r'"([a-z0-9_]+)"', re.search(r"PROVISIONAL_SUITES[^=]*=\s*frozenset\(\{([^}]*)\}", selector).group(1)))
ok = prov == provisional_rows
bad += not ok
print(f"PROVISIONAL_SUITES {sorted(prov)} vs provisional rows {sorted(provisional_rows)} : {'OK' if ok else 'MISMATCH'}")
print("RESULT", "PASS" if not bad else f"FAIL ({bad})")
sys.exit(1 if bad else 0)

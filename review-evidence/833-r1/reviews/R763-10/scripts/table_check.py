import re, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from process_test_support import MUTANTS
doc = open(sys.argv[1] + "/docs/testing/TESTING.md").read().splitlines()
rows = [l for l in doc if l.startswith("| ") and l.count("|") >= 4 and "`" in l.split("|")[-2]]
names = {}
for i, l in enumerate(rows):
    for n in re.findall(r"`([^`]+)`", l.split("|")[-2]):
        names.setdefault(n, []).append(i)
missing = [n for n, v in MUTANTS.items() if v[0] and n not in names]
nocontrol_named = [n for n, v in MUTANTS.items() if not v[0] and n != "none" and n in names]
unknown = [n for n in names if n not in MUTANTS]
multi = [n for n, r in names.items() if len(r) > 1]
ctrl_missing = []
for n, v in MUTANTS.items():
    if v[0] and n in names:
        for r in names[n]:
            if v[0] not in rows[r].split("|")[-3]:
                ctrl_missing.append((n, v[0]))
print("mutants", len(MUTANTS) - 1, "with control", sum(bool(v[0]) for v in MUTANTS.values()))
print("with control but in no row:", missing)
print("without control but named:", nocontrol_named)
print("named but not a mutant:", unknown)
print("named in more than one row:", multi)
print("row lacks its mutant's control:", ctrl_missing)

#!/usr/bin/env python3
"""Derive the #545 campaign inventories from source and compare them with the prose.

Usage: python3 derive_counts.py <repo-root>
Reads only; evaluates no repository code. Exit 0 when every count agrees,
1 when any stated count disagrees with its source inventory.
"""

import ast
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve "
    "thirteen fourteen fifteen sixteen".split())}
bad = 0


def say(ok: bool, text: str) -> None:
    global bad
    bad += 0 if ok else 1
    print(f"[{'OK' if ok else 'MISMATCH'}] {text}")


# gmstep_mutants.py: CONTROLS as a literal list of Control(...) calls.
gm = ast.parse((ROOT / "tb/verilator/milan_dp/gmstep_mutants.py").read_text())
controls = next(n.value for n in gm.body if isinstance(n, ast.Assign)
                and any(getattr(t, "id", "") == "CONTROLS" for t in n.targets))
rows = []
for call in controls.elts:
    name = call.args[0].value
    acceptance = call.args[5].value
    leg = call.args[6].value if len(call.args) > 6 else "gmstep"
    rows.append((name, acceptance, leg))
total = len(rows)
accept = sum(1 for r in rows if r[1])
optoff = sum(1 for r in rows if r[2] == "option-off")
slew = sum(1 for r in rows if r[0].startswith("the policy level"))
print(f"gmstep CONTROLS: total={total} acceptance={accept} option-off={optoff} "
      f"slew(--slew)={slew} gmstep-leg={total - optoff}")

readme = (ROOT / "tb/verilator/milan_dp/README.md").read_text().splitlines()
start = next(i for i, l in enumerate(readme) if l.startswith("| Control | Planted in |"))
table = []
for l in readme[start + 2:]:
    if not l.startswith("|"):
        break
    table.append(l)
say(len(table) == total - slew, f"README control table rows={len(table)}, CONTROLS minus --slew={total - slew}")
tab_names = {re.sub(r"`|\s*\(ruling [0-9]+ item [0-9]+\)", "", t.split("|")[1]).strip() for t in table}
src_names = {r[0] for r in rows if not r[0].startswith("the policy level")}
say(tab_names == src_names, f"README table names equal the non-slew CONTROLS names "
    f"(only-in-table={sorted(tab_names - src_names)}, only-in-source={sorted(src_names - tab_names)})")
sweep_rows = sum(1 for t in table if t.rstrip("| ").endswith("the sweep"))
say(sweep_rows == accept, f"README table 'the sweep' rows={sweep_rows}, acceptance controls={accept}")
off_rows = sum(1 for t in table if "option-off leg" in t)
say(off_rows == optoff, f"README table option-off rows={off_rows}, option-off controls={optoff}")

# Every sentence in the README that states a gmstep-mutants control count.
for i, l in enumerate(readme, 1):
    for m in re.finditer(r"(?:all|the sweep carries the|plus) (\w+)(?: #545)? controls?|all (\w+) \((?:two on the option-off leg|the explicit-campaign rule)|the (\w+) tabulated above", l, re.I):
        word = next(g for g in m.groups() if g).lower()
        if word not in WORDS:
            continue
        n = WORDS[word]
        text = m.group(0)
        # "tabulated": the table; "plus": the --slew additions; "the sweep
        # carries": the acceptance controls; any "all N": make gmstep-mutants.
        if "tabulated" in text:
            want, what = len(table), "table rows"
        elif text.lower().startswith("plus"):
            want, what = slew, "--slew controls"
        elif text.lower().startswith("the sweep"):
            want, what = accept, "acceptance controls"
        else:
            want, what = total, "make gmstep-mutants (--all) controls"
        say(n == want, f"README:{i}: '{text}' states {n}; source {what} = {want}")

testing = (ROOT / "docs/testing/TESTING.md").read_text().splitlines()
for i, l in enumerate(testing, 1):
    m = re.search(r"(\w+) gmstep controls and (\w+) option-off controls", l)
    if m:
        a, b = WORDS[m.group(1)], WORDS[m.group(2)]
        say((a, b) == (total - optoff, optoff), f"TESTING.md:{i}: {a} gmstep + {b} option-off; source {total - optoff} + {optoff}")
    m = re.search(r"#545 servo slew: (\w+) defects", l)
    if m:
        slew_n = WORDS[m.group(1)]
        testing_slew = (i, slew_n)

# slew_mutants.py: MUTANTS + STREAK_MUTANTS literal tuples.
sm = ast.parse((ROOT / "tb/verilator/mmcm_servo/slew_mutants.py").read_text())
defects = []
for n in sm.body:
    if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") in ("MUTANTS", "STREAK_MUTANTS"):
        defects += [e.elts[0].value for e in n.value.elts]
print(f"slew_mutants defects={len(defects)}: {', '.join(defects)}")
say(testing_slew[1] == len(defects), f"TESTING.md:{testing_slew[0]}: {testing_slew[1]} defects; source {len(defects)}")

mte = ast.parse((ROOT / "scripts/measure_test_evidence.py").read_text())
disp = next(n.value for n in mte.body if isinstance(n, ast.Assign)
            and getattr(n.targets[0], "id", "") == "DUT_READER_DISPOSITIONS")
text = next(v.value for k, v in zip(disp.keys, disp.values)
            if k.value == "tb/verilator/mmcm_servo/slew_mutants.py")
body = text.split("failures for ", 1)[1].split(";")[0]
classes = [c.strip() for c in re.split(r",\s*(?:and\s+)?|\s+and\s+", body) if c.strip()]
print(f"disposition classes={len(classes)}: {classes}")
say(len(classes) == len(defects), f"disposition names {len(classes)} classes for {len(defects)} defects")

print(f"RESULT: {'PASS' if bad == 0 else f'{bad} MISMATCH(ES)'}")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""cmp_counts.py TREE CAMPLOG ARMS: pair each selected MUTANTS row (in campaign order) with
its result line, then compare its failure count with the count each README table row
records for that arm and suite (tb/srp_encoder/README.md for srp_encoder rows,
tb/srp_top/README.md for srp_top rows; the table row naming the arm in backticks, the row
of the arm's group when there are several)."""
import re, sys
tree, camplog, arms = sys.argv[1], sys.argv[2], set(sys.argv[3].split(','))
src = open(f"{tree}/tb/srp_top/mutants.py").read()
rows = re.findall(r"\(\s*'([a-z0-9-]+)',\s*'([a-z_]+)',\s*'([a-z]*)',", src)
sel = [r for r in rows if r[0] in arms]
res = [l for l in open(camplog) if re.match(r"^[a-z0-9-]+: rc=", l)]
assert len(sel) == len(res), (len(sel), len(res))
readme = {s: open(f"{tree}/tb/{s}/README.md").read().splitlines() for s in ("srp_encoder", "srp_top")}
def recorded(arm, suite, group):
    rows = [l for l in readme[suite] if l.startswith('|') and f"`{arm}`" in l.split('|')[1]]
    # a srp_top row names its group in the second column: prefer the row of this group
    same = [l for l in rows if group and len(l.split('|')) > 2 and l.split('|')[2].strip() == group]
    for line in same or rows:
            cells = [c.strip() for c in line.split('|')]
            for c in cells[2:]:
                m = re.match(r"^(\d+)( FAIL)?\b", c)
                if m: return int(m.group(1)), line[:110]
    return None, None
bad = 0
for (arm, suite, group), l in zip(sel, res):
    assert l.startswith(arm + ":"), (arm, l)
    got = int(re.search(r"failures=(\d+)", l).group(1))
    rec, line = recorded(arm, suite, group)
    flag = "" if rec is None or rec == got else "  <-- DIFFERS"
    bad += bool(flag)
    print(f"{arm:38s} {suite:12s} {group:10s} measured {got:3d} recorded {rec}{flag}")
print(f"differing: {bad}")

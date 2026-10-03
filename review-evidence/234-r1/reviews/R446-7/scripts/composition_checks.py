#!/usr/bin/env python3
"""Composition checks for issue #234 / PR #638 on the merge-train candidate.

Run from a clone holding the candidate, dev tip, PR head and merge base:
    python3 composition_checks.py <candidate> <dev> <pr_head> <merge_base> <pr634_excerpt>
1. docs/findings/README.md: every row once, both parents' row orders kept,
   the union of both parents' rows, every link target present.
2. The route-1x1 baseline recorded by the PR against the shipping image of
   the candidate's dev side as PR #634's public body measured it, judged by
   the policy table the PR records (AREA_BUDGET.md).
"""
import json, os, re, subprocess, sys

cand, dev, pr, base, excerpt = sys.argv[1:6]

def show(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True,
                          text=True, check=True).stdout

def rows(rev):
    out = []
    for line in show(rev, "docs/findings/README.md").splitlines():
        m = re.match(r"\| \[[^\]]+\]\(([^)]+)\)", line)
        if m:
            out.append(m.group(1))
    return out

c, d, p, b = rows(cand), rows(dev), rows(pr), rows(base)
print("1. findings index")
print(f"   rows: candidate {len(c)}, dev {len(d)}, pr {len(p)}, base {len(b)}")
print(f"   duplicates: {sorted({x for x in c if c.count(x) > 1})}")
print(f"   dev order kept: {[x for x in c if x in d] == d}")
print(f"   pr order kept: {[x for x in c if x in p] == p}")
print(f"   candidate rows == dev rows | pr rows: {set(c) == set(d) | set(p)}")
print(f"   added by pr: {[x for x in p if x not in b]}")
print(f"   row text changed by dev: {[x for x in d if x in b and [l for l in show(dev,'docs/findings/README.md').splitlines() if '('+x+')' in l] != [l for l in show(base,'docs/findings/README.md').splitlines() if '('+x+')' in l]]}")
tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", cand, "docs/"],
                      capture_output=True, text=True, check=True).stdout.split()
missing = [x for x in c if os.path.normpath(os.path.join("docs/findings", x)) not in tree]
print(f"   link targets missing in candidate tree: {missing}")

print("2. route-1x1 baseline against the candidate's shipping image (PR #634 body)")
base_json = json.loads(show(cand, "syn/ooc/pp_resource_baseline.json"))
route = base_json["endpoints"]["route-1x1"]
fig = route["record"]["figures"]
pol = {k: v for k, v in route.items() if k != "record"}
text = open(excerpt).read()
num = lambda s: float(s.replace(",", ""))
meas = {
    "LUT": num(re.search(r"\| Slice LUTs \| ([\d,]+)", text).group(1)),
    "FF": num(re.search(r"\| Slice Registers \| ([\d,]+)", text).group(1)),
    "SLICE": num(re.search(r"\| Slices \| ([\d,]+) of", text).group(1)),
    "WNS_ns": float(re.search(r"\*\*WNS \+([\d.]+) ns", text).group(1)),
    "WHS_ns": float(re.search(r"WHS \+([\d.]+) ns", text).group(1)),
}
print(f"   recorded policy fields: {json.dumps(pol, sort_keys=True)}")
budget = show(cand, "docs/design/AREA_BUDGET.md")
row = next(l for l in budget.splitlines() if l.startswith("| `route-1x1` |"))
cells = [x.strip() for x in row.strip("|").split("|")]
tol = {"LUT": num(cells[1].lstrip("+")), "FF": num(cells[2].lstrip("+")),
       "SLICE": num(cells[3].lstrip("+"))}
for k in ("LUT", "FF", "SLICE"):
    delta = meas[k] - fig[k]
    print(f"   {k}: recorded {fig[k]:g}, #634 image {meas[k]:g}, growth {delta:+g}, "
          f"tolerance +{tol[k]:g}: {'EXCEEDS' if delta > tol[k] else 'within'}")
for k in ("WNS_ns", "WHS_ns"):
    print(f"   {k}: recorded {fig[k]}, #634 image {meas[k]}, change {meas[k]-fig[k]:+.3f}")

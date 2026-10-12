#!/usr/bin/env python3
"""Check each Mark II lane section (M2, M5, M6) of docs/design/MARK_II_AREA_PLAN.md
against both route-1x1 records it names: #645/#647's record (the gate record at
dev e8454e27) and #696's re-record (the record at the candidate head).

For each "Base route at dev `<sha>`" row: does it equal the e8454e27 record in
every gated figure it states? For each "M<n> route at `<sha>`" row: the
growth-only verdict (tolerance, absolute floor) against each record. Also prints
the sentence after each lane table that names the comparison record.
Read-only; uses `git show`.

usage: lane_vs_both_records.py <repo> <candidate rev> <old-record rev>
"""
import json
import re
import subprocess
import sys

FIG = ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "WNS_ns", "WHS_ns")


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def record(repo, rev):
    ep = json.loads(show(repo, rev, "syn/ooc/pp_resource_baseline.json"))["endpoints"]["route-1x1"]
    return ep["record"]["figures"], ep["tolerance"], ep["floor"]


def num(text):
    return float(text.replace(",", "").replace("+", ""))


def verdict(fig, rec, tol, floor):
    bad = []
    for k in ("LUT", "FF", "SLICE", "RAMB36", "RAMB18"):
        if fig[k] - rec[k] > tol[k]:
            bad.append(f"{k} +{fig[k] - rec[k]:g} > {tol[k]:g}")
    for k in ("WNS_ns", "WHS_ns"):
        if rec[k] - fig[k] > tol[k] + 1e-9:
            bad.append(f"{k} fall {rec[k] - fig[k]:.3f} > {tol[k]}")
        if fig[k] < floor[k] - 1e-9:
            bad.append(f"{k} {fig[k]} below floor {floor[k]}")
    return "PASS" if not bad else "FAIL: " + "; ".join(bad)


def main():
    repo, cand, old = sys.argv[1:4]
    records = {f"#696 record at {cand[:9]}": record(repo, cand),
               f"#645/#647 record at {old[:9]}": record(repo, old)}
    old_fig = records[f"#645/#647 record at {old[:9]}"][0]
    plan = show(repo, cand, "docs/design/MARK_II_AREA_PLAN.md").splitlines()
    pat = re.compile(r"^\| (Base route at dev `\w+`|M[0-9] route at `\w+`) \| ([\d,]+) \| ([\d,]+) \| "
                     r"([\d,]+) \| (\d+) / (\d+) \| ([+-][\d.]+) / ([+-][\d.]+) \|$")
    fail = 0
    for i, line in enumerate(plan, 1):
        m = pat.match(line)
        if not m:
            continue
        fig = dict(zip(FIG, (num(v) for v in m.groups()[1:])))
        name = m.group(1)
        if name.startswith("Base"):
            diff = [k for k in FIG if abs(fig[k] - old_fig[k]) > 1e-9]
            print(f":{i} {name}: equals the {old[:9]} record: {'YES' if not diff else 'NO ' + ','.join(diff)}")
            fail |= bool(diff)
            continue
        for label, (rec, tol, floor) in records.items():
            v = verdict(fig, rec, tol, floor)
            print(f":{i} {name} against {label} (LUT {rec['LUT']}): {v}")
            fail |= v != "PASS"
        for j in range(i, min(i + 6, len(plan))):
            if re.search(r"^Against .*record", plan[j]):
                print(f"   :{j + 1} {plan[j]}")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()

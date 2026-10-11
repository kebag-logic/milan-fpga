#!/usr/bin/env python3
"""Compare the Mark II M2/M6 lane routes against the route-1x1 record a tree holds.

For a repository revision, reads syn/ooc/pp_resource_baseline.json (record,
tolerance, floor) and the "Base route" / "M2 route" / "M6 route" rows of
docs/design/MARK_II_AREA_PLAN.md, then reports:
  * whether the plan's base row equals the record in every gated figure it
    states (LUT, FF, SLICE, RAMB36, RAMB18, WNS, WHS), as :695 claims;
  * each lane route's growth-only verdict against that record (tolerance,
    absolute floor), the same arithmetic the gate's check applies.
Also cross-checks the plan's current-inventory route column against the
record's scopes. Read-only; uses `git show`.

usage: record_vs_lane_routes.py <repo> <rev> [<rev> ...]
"""
import json
import re
import subprocess
import sys

FIG = ("LUT", "FF", "SLICE", "RAMB36", "RAMB18", "WNS_ns", "WHS_ns")


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True,
                          capture_output=True, text=True).stdout


def num(text):
    return float(text.replace(",", "").replace("+", ""))


def rows(plan):
    out = {}
    pat = re.compile(r"^\| (Base route at dev `\w+`|M[26] route at `\w+`) \| ([\d,]+) \| ([\d,]+) \| "
                     r"([\d,]+) \| (\d+) / (\d+) \| ([+-][\d.]+) / ([+-][\d.]+) \|$", re.M)
    for m in pat.finditer(plan):
        name = m.group(1)
        vals = [num(v) for v in m.groups()[1:]]
        out.setdefault(name, []).append(dict(zip(FIG, vals)))
    return out


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
    repo = sys.argv[1]
    for rev in sys.argv[2:]:
        ep = json.loads(show(repo, rev, "syn/ooc/pp_resource_baseline.json"))["endpoints"]["route-1x1"]
        rec, tol, floor = ep["record"]["figures"], ep["tolerance"], ep["floor"]
        plan = show(repo, rev, "docs/design/MARK_II_AREA_PLAN.md")
        print(f"== {rev}: route-1x1 record LUT {rec['LUT']} FF {rec['FF']} SLICE {rec['SLICE']} "
              f"RAMB {rec['RAMB36']}/{rec['RAMB18']} WNS {rec['WNS_ns']} WHS {rec['WHS_ns']}")
        print(f"   measured: {ep['measured'][:110]}...")
        found = rows(plan)
        if not found:
            print("   no M2/M6 lane rows in the plan at this revision")
        for name, figs in found.items():
            for fig in figs:
                if name.startswith("Base"):
                    diff = [k for k in FIG if abs(fig[k] - rec[k]) > 1e-9]
                    print(f"   {name}: equals the record in every stated gated figure: "
                          f"{'YES' if not diff else 'NO, differs in ' + ', '.join(diff)}")
                else:
                    print(f"   {name} against the record: {verdict(fig, rec, tol, floor)}")
        scopes = ep["record"]["scopes"]
        section = plan.split("### Current processor inventory", 1)[-1].split("\n## ", 1)[0]
        inv = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|", section, re.M)
        mism = [(s, int(r.replace(',', '')), scopes.get(s, {}).get("LUT")) for s, r, _, _ in inv
                if s in scopes and int(r.replace(',', '')) != scopes[s]["LUT"]]
        print(f"   current-inventory route column vs record scopes: {len(inv)} rows, "
              f"{len(mism)} differ {mism if mism else ''}")


if __name__ == "__main__":
    main()

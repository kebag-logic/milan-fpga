#!/usr/bin/env python3
"""Compare the Mark II plan's current processor inventory with the recorded file.

Usage: plan_vs_record.py <repo> [<rev>]
Reads docs/design/MARK_II_AREA_PLAN.md and syn/ooc/pp_resource_baseline.json at
<rev> (default HEAD) through git show, so the checkout is never modified.
Prints one line per row and figure, then a summary; exit 0 only when every
figure in the inventory equals the recorded LUT scope figure.
"""
import json
import re
import subprocess
import sys


def show(repo, rev, path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                          check=True, capture_output=True, text=True).stdout


def main():
    repo = sys.argv[1]
    rev = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    plan = show(repo, rev, "docs/design/MARK_II_AREA_PLAN.md")
    rec = json.loads(show(repo, rev, "syn/ooc/pp_resource_baseline.json"))
    start = plan.index("### Current processor inventory")
    end = plan.index("\n## ", start)
    rows = re.findall(r"^\| `([^`]+)` \| ([\d,]+) \| ([\d,]+) \| ([\d,]+) \|",
                      plan[start:end], re.M)
    eps = ("route-1x1", "ooc-1x1", "ooc-8x8")
    diffs = 0
    figures = 0
    for scope, *vals in rows:
        for ep, val in zip(eps, vals):
            figures += 1
            got = int(val.replace(",", ""))
            want = rec["endpoints"][ep]["record"]["scopes"].get(scope, {}).get("LUT")
            ok = got == want
            diffs += not ok
            print(f"{'ok  ' if ok else 'DIFF'} {scope:28s} {ep:9s} plan={got} record={want}")
    print(f"rev={rev} rows={len(rows)} figures={figures} differences={diffs}")
    return 0 if rows and diffs == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

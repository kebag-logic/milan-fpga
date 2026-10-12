#!/usr/bin/env python3
"""R624-9: R624-8's html-block-edge probe, round 8's published receipt against the rerun on round 9's check.
usage: compare_r624_8.py <round 8 receipt.json> <round 9 rerun.json> <out.json>"""
import json
import sys
a, b = (json.load(open(f)) for f in sys.argv[1:3])
B = {r["case"]: r for r in b}
out = []
for r in a:
    s = B[r["case"]]
    out.append(dict(case=r["case"], r8=[r["rc"], r["verdict"]], r9=[s["rc"], s["verdict"]],
                    same=[r["rc"], r["verdict"]] == [s["rc"], s["verdict"]], r9_markup=s["markup"][:2]))
    print(f'{r["case"]:55s} r8={r["rc"]},{r["verdict"]:9s} r9={s["rc"]},{s["verdict"]:9s} {"SAME" if out[-1]["same"] else "CHANGED"}')
json.dump(out, open(sys.argv[3], "w"), indent=1)

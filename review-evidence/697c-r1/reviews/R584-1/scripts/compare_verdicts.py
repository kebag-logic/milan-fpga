#!/usr/bin/env python3
"""Compare every [ok]/[ESCAPED] line (plant verdicts) and campaign tallies between dev and head gate logs.
usage: compare_verdicts.py DEVLOG... -- HEADLOG..."""
import re, sys
i = sys.argv.index("--")
def read(paths):
    v, t = {}, []
    for p in paths:
        for line in open(p, errors="replace"):
            m = re.match(r"^\[(ok|ESCAPED)\] (.*?)(?::|$)", line.rstrip())
            if m:
                v[m.group(2).strip()] = m.group(1)
            if re.search(r"(\d+) of (\d+) caught|caught: \d+|escaped", line):
                t.append(line.strip())
    return v, t
dv, dt = read(sys.argv[1:i]); hv, ht = read(sys.argv[i + 1:])
print(f"dev verdict lines {len(dv)} (ok {sum(x == 'ok' for x in dv.values())}); "
      f"head {len(hv)} (ok {sum(x == 'ok' for x in hv.values())})")
only_d = sorted(set(dv) - set(hv)); only_h = sorted(set(hv) - set(dv))
diff = sorted(k for k in set(dv) & set(hv) if dv[k] != hv[k])
for k in only_d: print("ONLY-DEV", dv[k], k)
for k in only_h: print("ONLY-HEAD", hv[k], k)
for k in diff: print("VERDICT-DIFFERS", k, dv[k], hv[k])
print("dev tallies:"); [print("  ", x) for x in dt]
print("head tallies:"); [print("  ", x) for x in ht]

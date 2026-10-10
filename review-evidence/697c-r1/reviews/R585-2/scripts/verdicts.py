#!/usr/bin/env python3
"""Compare the verdict lines ([ok]/[FAIL]/[ESCAPED]... name) of two test_ctrl_firmware.py logs by name, and print
the summary lines (mutants/caught/arms). Usage: verdicts.py <dev.log> <head.log>"""
import re, sys
def read(p):
    v = {}
    summary = []
    for ln in open(p, errors="replace"):
        m = re.match(r"^\[(ok|FAIL|ESCAPED|ERROR|MISSED|SURVIVED|[A-Za-z ]+)\] (.+?)(?::|$)", ln.rstrip())
        if m:
            v.setdefault(m[2].strip(), []).append(m[1])
        if re.search(r"caught|arms|PASS$|FAIL$|tsn-c-stack at", ln) and not ln.startswith("["):
            summary.append(ln.rstrip())
    return v, summary
d, ds = read(sys.argv[1]); h, hs = read(sys.argv[2])
print("dev verdict names:", len(d), "lines:", sum(map(len, d.values())), " head:", len(h), sum(map(len, h.values())))
print("non-ok at dev:", sorted(k for k, x in d.items() if set(x) != {"ok"})[:10])
print("non-ok at head:", sorted(k for k, x in h.items() if set(x) != {"ok"})[:10])
only_d = sorted(set(d) - set(h)); only_h = sorted(set(h) - set(d))
print("only at dev:", len(only_d), only_d[:20]); print("only at head:", len(only_h), only_h[:20])
diff = sorted(k for k in set(d) & set(h) if d[k] != h[k]); print("different verdicts:", len(diff), diff[:20])
print("-- dev summary"); print("\n".join(ds[-12:])); print("-- head summary"); print("\n".join(hs[-12:]))

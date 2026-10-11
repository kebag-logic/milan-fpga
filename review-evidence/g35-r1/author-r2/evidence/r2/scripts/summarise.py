"""Group per-position rows into byte ranges with identical base/head results.
Usage: summarise.py <base.tsv> <head.tsv>"""
import csv, sys
def load(path):
    with open(path) as f:
        return {(r["type"], int(r["byte"])): r for r in csv.DictReader(f, delimiter="\t")}
base, head = load(sys.argv[1]), load(sys.argv[2])
assert base.keys() == head.keys()
names = {"sync": "Sync", "fu": "Follow_Up", "pdreq": "Pdelay_Req", "pdresp": "Pdelay_Resp", "ann": "Announce (no PathTrace)"}
def cell(r):
    return f"+{r['drops']} / {r['events']} / {r['before']}-{r['on']}-{r['after']}"
check = {"head_all_one_drop": True, "head_no_event": True, "head_none_after": True}
for t in names:
    keys = sorted(k for k in head if k[0] == t)
    n = len(keys)
    print(f"\n{names[t]} ({n} bytes)\n")
    print("| flagged byte | base drops / events / writes before-on-after | head drops / events / writes before-on-after |")
    print("|---|---|---|")
    run = []
    def flush():
        a, b = run[0][1], run[-1][1]
        rng = f"{a}" if a == b else f"{a}-{b}"
        if b == n - 1: rng += " (eof)"
        print(f"| {rng} | {cell(base[run[0]])} | {cell(head[run[0]])} |")
    for k in keys:
        sig = lambda r: (r["drops"], r["events"], r["before"], r["on"], r["after"])
        if run and (sig(base[k]), sig(head[k])) != (sig(base[run[-1]]), sig(head[run[-1]])):
            flush(); run = []
        run.append(k)
        h = head[k]
        check["head_all_one_drop"] &= h["drops"] == "1"
        check["head_no_event"] &= h["events"] == "0"
        check["head_none_after"] &= h["after"] == "0"
    flush()
print("\n", check)

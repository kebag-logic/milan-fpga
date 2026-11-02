#!/usr/bin/env python3
"""usage: kills.py <trace jsonl> ...  Scratch only. From per-pass traces: how long after its SIGKILL each pid stayed live, and
how long the root shell took from RESUME to gone; states seen; re-parent race count."""
import json, sys
for path in sys.argv[1:]:
    tr = [json.loads(l) for l in open(path)]
    kill, root, dmax, states, race, lateresume = [], [], {}, {}, 0, 0
    for t in tr:
        sent = {}
        for at, pid, what in t["sent"]:
            if what == 9: sent.setdefault(str(pid), at)
        resume = next((at for at, _p, w in t["sent"] if w == "RESUME"), None)
        termed = {str(p) for _a, p, w in t["sent"] if w == 15}
        first = t["passes"][0][2] if t["passes"] else {}
        # a process listed live at the first census, not the root, that never got TERM and was later SIGKILLed
        if t["notified"] and any(p != str(t["root"]) and p not in termed and v and v[1] != "Z" and p in sent for p, v in first.items()):
            race += 1
        if resume is not None and resume >= 2.9: lateresume += 1
        for pid, at in sent.items():
            live_after = [p[0] + p[1] for p in t["passes"] if p[0] >= at and p[2].get(pid) and p[2][pid][1] != "Z"]
            kill.append(round(max(live_after) - at, 3) if live_after else 0.0)
        if resume is not None and t["outcome"] == "clean":
            root.append(round(t["elapsed"] - resume, 3))
        prev = {}
        for at, took, st in t["passes"]:
            for p, v in st.items():
                if v:
                    states[v[1]] = states.get(v[1], 0) + 1
                    if v[1] == "D":
                        w = v[3]
                        dmax.setdefault(w, [0, 0.0])
                        dmax[w][0] += 1
    kill.sort(); root.sort()
    q = lambda a, f: a[min(len(a) - 1, int(f * len(a)))] if a else None
    print(path.rsplit("/", 1)[1], "cleanups", len(tr), "failed", sum(t["outcome"] != "clean" for t in tr), "elapsed max", max(t["elapsed"] for t in tr))
    print("  SIGKILL->not live s: n", len(kill), "p50", q(kill, .5), "p99", q(kill, .99), "max", kill[-1] if kill else None)
    print("  RESUME->clean s:     n", len(root), "p50", q(root, .5), "p99", q(root, .99), "max", root[-1] if root else None)
    print("  never-TERMed race:", race, " resumed>=2.9s:", lateresume, " states", states, " D wchans", {k: v[0] for k, v in dmax.items()})

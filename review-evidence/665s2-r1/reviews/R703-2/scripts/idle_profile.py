#!/usr/bin/env python3
"""Function-level CPU-cycle profile of whole idle passes from a committed-PC trace.
Usage: idle_profile.py TRACE_LOG FUNCTIONS_JSON PASS_FUNCTION
Each commit's cycles (to the next commit) are charged to the function holding its PC;
a pass runs from one commit of PASS_FUNCTION's entry to the next."""
import bisect, json, sys
lines = [l.split() for l in open(sys.argv[1]) if l.startswith('PC ')]
funcs = json.load(open(sys.argv[2]))
starts = [f[1] for f in funcs]
entry = [f[1] for f in funcs if f[0] == sys.argv[3]][0]
def name(pc):
    i = bisect.bisect_right(starts, pc) - 1
    return funcs[i][0] if i >= 0 and pc < funcs[i][1] + funcs[i][2] else '?'
trace = [(int(c), int(pc, 16)) for _, c, pc in lines]
bounds = [k for k, (_, pc) in enumerate(trace) if pc == entry]
for a, b in zip(bounds, bounds[1:]):
    prof = {}
    for (c0, pc), (c1, _) in zip(trace[a:b], trace[a + 1:b + 1]):
        prof[name(pc)] = prof.get(name(pc), 0) + c1 - c0
    total = trace[b][0] - trace[a][0]
    top = sorted(prof.items(), key=lambda kv: -kv[1])[:6]
    print(f'pass {total} CPU cycles:', ', '.join(f'{k} {v}' for k, v in top))

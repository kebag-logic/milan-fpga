#!/usr/bin/env python3
"""For a merge-file output AUTO (conflict markers) and the recorded MERGED file,
check that each conflict side's lines occur in MERGED as an in-order
subsequence, and that the non-conflict text is identical once conflict regions
are removed from both. Prints lines that fail."""
import sys
auto = open(sys.argv[1]).read().split('\n')
merged = open(sys.argv[2]).read().split('\n')
sides = []; ctx = []
i = 0
while i < len(auto):
    if auto[i].startswith('<<<<<<< '):
        o, t = [], []; i += 1
        while not auto[i].startswith('======='): o.append(auto[i]); i += 1
        i += 1
        while not auto[i].startswith('>>>>>>> '): t.append(auto[i]); i += 1
        sides.append((o, t))
    else:
        ctx.append(auto[i])
    i += 1
def subseq(needle, hay):
    j = 0; miss = []
    for l in needle:
        k = j
        while k < len(hay) and hay[k] != l: k += 1
        if k == len(hay): miss.append(l)
        else: j = k + 1
    return miss
for n, (o, t) in enumerate(sides):
    mo = subseq(o, merged); mt = subseq(t, merged)
    print(f'conflict {n}: lane {len(o)} lines (missing in order: {len(mo)}), main {len(t)} lines (missing in order: {len(mt)})')
    for l in mo: print('  lane-missing:', l)
    for l in mt: print('  main-missing:', l)
mc = subseq(ctx, merged)
print(f'context {len(ctx)} lines, missing in order: {len(mc)}')
for l in mc: print('  ctx-missing:', l)
print(f'merged {len(merged)} lines = context {len(ctx)} + resolution {len(merged)-len(ctx)}; sides total {sum(len(o)+len(t) for o,t in sides)}')

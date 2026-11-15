"""One traced span's cycles as a call tree, each node its inclusive cycles and commits, from a committed-PC trace
(sim_main.cpp's PC lines, BUDGET_TRACE_AFTER / BUDGET_TRACE_PCS). Calls are followed as spanprof.py follows them: a
commit at a function's first instruction is a call returning to the instruction after the previous commit, and the
call ends at the first commit of that address. Each commit's cycles are those to the next commit.

Prints every node of at least MIN cycles, to DEPTH frames below the span's function, and writes the tree as JSON.

usage: python3 -I calltree.py FUNCTIONS.json TRACE START CYCLES OUT.json [MIN [DEPTH]]"""
import bisect
import collections
import json
import re
import sys

functions, trace, start, cycles, out = sys.argv[1:6]
start, cycles = int(start), int(cycles)
least = int(sys.argv[6]) if len(sys.argv) > 6 else 100
depth = int(sys.argv[7]) if len(sys.argv) > 7 else 12
raw = json.load(open(functions))
seen = collections.Counter(name for name, _, _ in raw)
funcs = sorted((addr, size, name if seen[name] == 1 else f'{name}@{addr:x}') for name, addr, size in raw)
starts = [a for a, _, _ in funcs]
entry = {a: n for a, _, n in funcs}


def func(pc: int) -> str:
    k = bisect.bisect_right(starts, pc) - 1
    return funcs[k][2] if k >= 0 and pc < funcs[k][0] + funcs[k][1] else '?'


pcs = []
for ln in open(trace, errors='replace'):
    if ln.startswith('PC '):
        _, c, p = ln.split()
        c = int(c)
        if start <= c <= start + cycles:
            pcs.append((c, int(p, 16)))
        elif c > start + cycles:
            break
root = func(pcs[0][1])
stack = [(root, None)]
incl = collections.Counter()
count = collections.Counter()
for k in range(len(pcs) - 1):
    cpu, pc = pcs[k]
    if k > 0:
        prev = pcs[k - 1][1]
        back = next((i for i in range(len(stack) - 1, 0, -1) if stack[i][1] == pc), None)
        if back is not None:
            del stack[back:]
        elif pc in entry and func(prev) != entry[pc]:
            stack.append((entry[pc], prev + 4))
    c = pcs[k + 1][0] - cpu
    names = [f for f, _ in stack]
    for i in range(1, len(names) + 1):
        key = tuple(names[:i])
        incl[key] += c
        if i == len(names):
            count[key] += 1
# calls: a node entered anew (its commits at the first instruction of the function)
tree = sorted(incl.items())
json.dump(dict(root=root, start=start, cycles=pcs[-1][0] - pcs[0][0], commits=len(pcs) - 1,
               nodes=[[list(k), v, count[k]] for k, v in tree]), open(out, 'w'), indent=0)
print(f'# span {root} from CPU cycle {start}: {pcs[-1][0] - pcs[0][0]} cycles, {len(pcs) - 1} commits')


def show(prefix, level):
    kids = sorted((k for k in incl if len(k) == len(prefix) + 1 and k[:len(prefix)] == prefix),
                  key=lambda k: -incl[k])
    for k in kids:
        if incl[k] < least or level > depth:
            continue
        print(f"{incl[k]:7d} {count[k]:6d}  {'  ' * level}{re.sub(r'@.*', '', k[-1])}")
        show(k, level + 1)


print(f"{incl[(root,)]:7d} {count[(root,)]:6d}  {root}")
show((root,), 1)

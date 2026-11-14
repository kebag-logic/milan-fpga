"""One traced span's cycles, by function and by source line, from a committed-PC trace (sim_main.cpp's PC lines,
BUDGET_TRACE_AFTER / BUDGET_TRACE_PCS).

The span is the commits from CPU cycle START (its SPAN line's second field, the commit of its entry) to START +
CYCLES (the commit of its return). Each commit's cycles are those to the next commit: the instruction's own and its
fetch and data stalls. Calls are followed as sim_main.cpp follows a traced one: a commit at a function's first
instruction is a call returning to the instruction after the previous commit, and the call ends at the first commit
of that address.

Reported:
- self: each function's cycles and commits;
- path: cycles by call path from the span's function, to DEPTH frames;
- lines: for FOCUS (a function in the span), each cycle charged to one of its source lines: its own instructions'
  lines (the outermost of an inline chain, from addr2line -i on a -g build of the same code), and each callee's
  cycles to the line of its call;
- passes: those lines summed over PASSES, a JSON list of [name, first_line, last_line].

usage: python3 -I spanprof.py FUNCTIONS.json TRACE START CYCLES ADDR2LINE ELF_G FOCUS PASSES.json OUT.json [DEPTH]"""
import bisect
import collections
import json
import subprocess
import sys

functions, trace, start, cycles, a2l, elf_g, focus, passes_path, out = sys.argv[1:10]
start, cycles = int(start), int(cycles)
depth = int(sys.argv[10]) if len(sys.argv) > 10 else 3
raw = json.load(open(functions))
seen = collections.Counter(name for name, _, _ in raw)
funcs = sorted((addr, size, name if seen[name] == 1 else f'{name}@{addr:x}') for name, addr, size in raw)
starts = [a for a, _, _ in funcs]
entry = {a: n for a, _, n in funcs}


def func(pc: int) -> str:
    k = bisect.bisect_right(starts, pc) - 1
    if k >= 0 and pc < funcs[k][0] + funcs[k][1]:
        return funcs[k][2]
    return f'?{pc:08x}'


pcs, fetches = [], []
for line in open(trace, errors='replace'):
    if line.startswith('PC '):
        _, cpu, pc = line.split()
        cpu = int(cpu)
        if start <= cpu <= start + cycles:
            pcs.append((cpu, int(pc, 16)))
        elif cpu > start + cycles:
            break
    elif line.startswith('FETCH '):
        _, cpu, _ = line.split()
        if start <= int(cpu) < start + cycles:
            fetches.append(int(cpu))
if not pcs or pcs[0][0] != start or pcs[-1][0] != start + cycles:
    sys.exit(f'the trace does not hold the span: first {pcs[0] if pcs else None}, last {pcs[-1] if pcs else None}')

# the call stack: (function, return pc, call-site pc in the caller)
root = func(pcs[0][1])
stack = [(root, None, None)]
selfc, selfn, pathc = collections.Counter(), collections.Counter(), collections.Counter()
focus_at = {}  # commit index -> the focus pc it is charged to
charged = []  # (focus pc to charge, cycles): the focus's own pc, or the call site of the callee in the focus
for k in range(len(pcs) - 1):
    cpu, pc = pcs[k]
    if k > 0:
        prev = pcs[k - 1][1]
        # a return ends its frame and every frame above it (a tail call's frame returns with its caller's)
        back = next((i for i in range(len(stack) - 1, 0, -1) if stack[i][1] == pc), None)
        if back is not None:
            del stack[back:]
        elif pc in entry and func(prev) != entry[pc]:
            stack.append((entry[pc], prev + 4, prev))
    c = pcs[k + 1][0] - cpu
    name = func(pc)
    selfc[name] += c
    selfn[name] += 1
    pathc[' > '.join(f for f, _, _ in stack[:depth + 1])] += c
    for i, (f, _, _) in enumerate(stack):
        if f == focus:
            charged.append((pc if i == len(stack) - 1 else stack[i + 1][2], c))
            focus_at[k] = charged[-1][0]
            break
total = pcs[-1][0] - pcs[0][0]
# each instruction-fetch refill started while a function's commit was the last: the function it is charged to
at = [c for c, _ in pcs]
refills = collections.Counter(func(pcs[max(bisect.bisect_right(at, f) - 1, 0)][1]) for f in fetches)

# the focus's lines: addr2line -i, the outermost (last) frame of each inline chain
addrs = sorted({pc for pc, _ in charged})
lines = {}
if addrs:
    # one block per address (-a marks each): pairs of (function, file:line), the inline chain innermost first
    r = subprocess.run([a2l, '-a', '-i', '-f', '-e', elf_g, *(f'{a:x}' for a in addrs)], capture_output=True,
                       text=True, check=True)
    block, cur = {}, None
    for ln in r.stdout.splitlines():
        if ln.startswith('0x'):
            cur = int(ln, 16)
            block[cur] = []
        else:
            block[cur].append(ln)
    for a, b in block.items():
        pairs = list(zip(b[0::2], b[1::2]))
        fn, where = pairs[-1]
        lineno = where.rsplit(':', 1)[-1].split()[0]
        lines[a] = (fn, int(lineno) if lineno.isdigit() else 0)
byline = collections.Counter()
for pc, c in charged:
    fn, ln = lines.get(pc, ('?', 0))
    byline[ln] += c
passes = json.load(open(passes_path))
bypass, passrefills = collections.Counter(), collections.Counter()


def pass_of(ln):
    return next((p for p, a, b in passes if a <= ln <= b), f'other (line {ln})')


for ln, c in byline.items():
    bypass[pass_of(ln)] += c
for f in fetches:
    k = max(bisect.bisect_right(at, f) - 1, 0)
    if k in focus_at:
        passrefills[pass_of(lines.get(focus_at[k], ('?', 0))[1])] += 1
result = dict(root=root, start=start, cycles=total, commits=len(pcs) - 1, refills=len(fetches),
              self=[[n, selfc[n], selfn[n], refills[n]] for n, _ in selfc.most_common()],
              paths=[[p, c] for p, c in pathc.most_common()],
              focus=focus, focus_cycles=sum(c for _, c in charged),
              lines=sorted([ln, c] for ln, c in byline.items()),
              passes=[[p, bypass[p], passrefills[p]] for p, _, _ in passes] +
              [[p, c, passrefills[p]] for p, c in bypass.items() if p not in {q for q, _, _ in passes}])
json.dump(result, open(out, 'w'), indent=1)
print(f'# span {root} from CPU cycle {start}: {total} cycles, {len(pcs) - 1} commits, {len(fetches)} fetch refills')
print(f"{'function (self)':34s} {'cycles':>7s} {'commits':>7s} {'refills':>7s}")
for n, c, i, f in result['self'][:25]:
    print(f'{n:34s} {c:7d} {i:7d} {f:7d}')
print(f'\n# by call path (depth {depth})')
for p, c in result['paths'][:30]:
    print(f'{c:7d}  {p}')
print(f'\n# {focus}: {result["focus_cycles"]} cycles by pass (callees charged to the line of their call)')
for p, c, f in result['passes']:
    print(f'{c:7d} {f:4d} refills  {p}')

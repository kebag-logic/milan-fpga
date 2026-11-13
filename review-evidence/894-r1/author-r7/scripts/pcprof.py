"""A per-function profile of one pass's polls from a committed-PC trace (sim_main.cpp's PC and FETCH lines,
BUDGET_TRACE_AFTER / BUDGET_TRACE_PCS): from the first commit inside adp_mbx's on_poll at or after bus cycle FROM to the
last commit inside ctrl_app_srp's deliver before the next entry of the pass's first poll, each function's committed
instructions, its CPU cycles (each commit's cycles to the next commit, the instruction's own and its fetch stalls), and
the fetch refills started while it ran.

usage: python3 -I pcprof.py FUNCTIONS.json TRACE FROM_SYS [TOP]"""
import bisect
import collections
import json
import sys

raw = json.load(open(sys.argv[1]))
seen = collections.Counter(name for name, _, _ in raw)
# a static function's name in several modules is told apart by its address
funcs = sorted((addr, size, name if seen[name] == 1 else f'{name}@{addr:x}') for name, addr, size in raw)
starts = [a for a, _, _ in funcs]
want_from, top = int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 40


def func(pc: int) -> str:
    k = bisect.bisect_right(starts, pc) - 1
    if k >= 0 and pc < funcs[k][0] + funcs[k][1]:
        return funcs[k][2]
    return f'?{pc:08x}'


pcs, fetches, ms_sys = [], [], []
for line in open(sys.argv[2], errors='replace'):
    if line.startswith('PC '):
        _, cpu, pc = line.split()
        pcs.append((int(cpu), int(pc, 16)))
    elif line.startswith('FETCH '):
        _, cpu, addr = line.split()
        fetches.append(int(cpu))
# the bus and CPU clocks are one (100 MHz each) and the CPU's count trails the bus's by 64 cycles at boot
first_poll = [k for k, (cpu, pc) in enumerate(pcs) if func(pc).startswith('on_poll') and cpu >= want_from - 64]
if not first_poll:
    sys.exit('no adp on_poll commit after FROM in the trace')
a = first_poll[0]
names = [func(pc) for _, pc in pcs]
b = a
poll0 = names[a]
while b + 1 < len(pcs) and not (names[b + 1] == poll0 and names[b] != poll0 and b > a + 50):
    b += 1
last_deliver = max(k for k in range(a, b + 1) if names[k].startswith('deliver'))
cyc, ins, ref = collections.Counter(), collections.Counter(), collections.Counter()
for k in range(a, last_deliver):
    cyc[names[k]] += pcs[k + 1][0] - pcs[k][0]
    ins[names[k]] += 1
fi = bisect.bisect_left(fetches, pcs[a][0])
for f in fetches[fi:bisect.bisect_left(fetches, pcs[last_deliver][0])]:
    k = bisect.bisect_right([c for c, _ in pcs[a:last_deliver + 1]], f) - 1 + a
    ref[names[max(k, a)]] += 1
total = pcs[last_deliver][0] - pcs[a][0]
print(f'# polls from CPU cycle {pcs[a][0]} to {pcs[last_deliver][0]}: {total} cycles, {last_deliver - a} commits, '
      f'{sum(ref.values())} fetch refills')
print(f"{'function':32s} {'cycles':>7s} {'instr':>6s} {'refills':>7s}")
for name, c in cyc.most_common(top):
    print(f'{name:32s} {c:7d} {ins[name]:6d} {ref[name]:7d}')

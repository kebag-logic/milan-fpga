#!/usr/bin/env python3
"""Check the fewer-reservations rows of docs/design/MARK_II_STREAM_ENGINES.md and
try to falsify the figure NFR-LAT-03 calls the largest reached.

Independent of the published model except where it is named: Part A replays each
row's words under the page's phase rule, then asks the published model's recursion
and 8.6.8.2 simulation. Part B searches contents per phase, best first, and accepts
a case only after an operation-level replay of starts and stops under the rule, at
most 16 AAF streams and one CRF on the port. No timing here is a measurement.
Usage: python3 -I probe_r8_delta.py <path to mixed_stagger.py>
"""
import importlib.util, itertools, sys
from fractions import Fraction as Fr

spec = importlib.util.spec_from_file_location("published_model", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

NS = {48: 6, 96: 12, 192: 24}
FIXED = {48: Fr(40325, 1000), 96: Fr(32491, 1000), 192: Fr(18093, 1000)}
FMT = (1, 2, 4, 6, 8)
CRF_BITS = 704
def L(r, n): return 704 if n == 'c' else 8 * (max(24 + NS[r] * 4 * n + 22, 68) + 20)
def RES(r, n):
    return 704 if n == 'c' else 8 * (max(24 + NS[r] * 4 * n + 1 + 22, 68) + 20)
def tie(P):
    if P == 6: return [0, 3, 1, 4, 2, 5]
    o, k = [], 1
    while len(o) < P:
        for j in range(k):
            p = j * P // k
            if p not in o: o.append(p)
        k *= 2
    return o
def choose(r, ph, T):
    return min(T, key=lambda q: (sum(L(r, x) for x in ph[q]), T.index(q)))
def order(r, q):
    """Smaller frames first, the CRF last in its phase."""
    return sorted(q, key=lambda x: (x == 'c', L(r, x)))
def wait(r, ph):
    P = NS[r]
    a = Fr(sum(RES(r, x) for q in ph for x in q), 125)
    if not a: return Fr(0)
    free, worst = None, Fr(0)
    for c in range(4):
        for p in range(P):
            for x in order(r, ph[p]):
                t = Fr(125 * p, P) + 125 * c
                s = t if free is None else max(t, free)
                free = s + Fr(L(r, x)) / a
                if x != 'c' and c >= 2: worst = max(worst, s - t)
    return worst
def f3(x): return f"{float(x):.3f}"

print("== A. each second-table row, replayed from its own words under the page's rule")
def play(r, ops):
    P = NS[r]; T = tie(P); ph = [[] for _ in range(P)]; peak = 0; where = []
    for op in ops:
        if op[0] == 's':
            q = choose(r, ph, T); ph[q].append(op[1]); where.append(q)
        elif op[0] == 'stop_fmt':
            for q in ph:
                while op[1] in q: q.remove(op[1])
        else:
            ph[op[1]].remove(op[2])
        peak = max(peak, sum(map(len, ph)))
    return ph, peak, where
S = lambda n, k=1: [('s', n)] * k
ROWS = [("48 kHz six one-channel", 48, S(1)+S(8,5)+S(1,2)+S(8,5)+S(1,3)+[('stop_fmt',8)], {0:[1]*6}, "103.022", "143.347"),
        ("48 kHz eight then one", 48, S(8)+S(1,2)+[('x',3,1)], {0:[8],1:[1]}, "71.310", "111.635"),
        ("96 kHz four one-channel", 96, S(1)+S(8,11)+S(1,3)+[('stop_fmt',8)], {0:[1]*4}, "92.935", "125.426"),
        ("192 kHz six then one", 192, S(1,5)+S(6)+[('x',0,1),('x',3,1),('x',6,1),('x',18,1)], {9:[6],12:[1]}, "83.941", "102.034")]
bad = 0
for name, r, ops, want, w_, t_ in ROWS:
    ph, peak, where = play(r, ops)
    got = {i: q for i, q in enumerate(ph) if q}
    w = wait(r, ph); rate = m.Rate(r)
    fifo = m.lindley_wait(rate, ph, None); ev = m.cbs_sim(rate, ph, None)
    ok = got == want and f3(w) == w_ and f3(fifo) == w_ and f3(ev) == w_ and f3(w + FIXED[r]) == t_ and peak <= 16
    bad += not ok
    print(f"{name}: placed {where}; peak {peak}; final {got}; mine {f3(w)}; model recursion {f3(fifo)}; "
          f"8.6.8.2 sim {f3(ev)}; total {f3(w + FIXED[r])}; page {w_} / {t_}; {'AGREES' if ok else 'DIFFERS'}")
print("result:", "ALL AGREE" if not bad else f"{bad} DIFFER")

print("\n== B. reach test: rebuild eight-channel helpers before each join, then replay")
def try_reach(r, target, cap=16):
    """target: {phase: [formats]}. Join order search with memo; returns ops or None."""
    P = NS[r]; T = tie(P)
    joins = sorted(((p, x) for p, q in target.items() for x in q), key=str)
    def need(have, p):
        ph = [list(q) for q in have]; helpers = []
        while True:
            c = choose(r, ph, T)
            if c == p: return helpers
            ph[c].append(8); helpers.append(c)
            if len(helpers) > cap: return None
    seen = set()
    def dfs(have, rest):
        if not rest: return []
        key = tuple(sorted(rest, key=str))
        if key in seen: return None
        for i, (p, x) in enumerate(rest):
            if rest.index((p, x)) != i: continue
            h = need(have, p)
            if h is None: continue
            aaf = sum(1 for q in have for y in q if y != 'c') + (x != 'c') + len(h)
            if aaf > cap: continue
            nh = [list(q) for q in have]; nh[p].append(x)
            tail = dfs(nh, rest[:i] + rest[i+1:])
            if tail is not None: return [(p, x, len(h))] + tail
        seen.add(key)
        return None
    return dfs([[] for _ in range(P)], joins)
def replay(r, target, plan, cap=16):
    """Operation-level check of a plan: every start goes where the rule sends it."""
    P = NS[r]; T = tie(P); ph = [[] for _ in range(P)]; words = []
    for p, x, nh in plan:
        for k in range(nh):
            c = choose(r, ph, T); ph[c].append('h')
        assert choose(r, ph, T) == p, (p, x, ph)
        ph[p].append(x)
        assert sum(1 for q in ph for y in q if y != 'c') <= cap
        for q in ph:
            while 'h' in q: q.remove('h')
    return {i: order(r, q) for i, q in enumerate(ph) if q} == {i: order(r, q) for i, q in target.items()}
_oL = L
def L(r, n):
    return _oL(r, 8) if n == 'h' else _oL(r, n)

def multisets(r, limit, withcrf):
    out = []
    bits = [L(r, n) for n in FMT]
    def go(i, cur, load):
        if i == len(FMT):
            out.append(tuple(cur)); return
        k = 0
        while load + k * bits[i] <= limit:
            go(i + 1, cur + [FMT[i]] * k, load + k * bits[i]); k += 1
    go(0, [], 0)
    return out

def quick(r, win):
    """Worst AAF wait of a burst window, phases consecutive, nothing else running."""
    tph = 125 / NS[r]
    a = sum(RES(r, x) for q in win for x in q) / 125
    if not a: return 0.0
    free, worst = 0.0, 0.0
    for i, q in enumerate(win):
        t = i * tph
        for x in q:
            s = max(t, free)
            if x != 'c': worst = max(worst, s - t)
            free = s + L(r, x) / a
    return worst

LIM = {48: 6192, 96: 7200}
WIDTH = {48: 2, 96: 3}
res = {}
for r in (48, 96):
    base = multisets(r, LIM[r], False)
    cands = []
    for w in range(1, WIDTH[r] + 1):
        for win in itertools.product(base, repeat=w):
            if not win[0] or not win[-1] or sum(map(len, win)) > 16: continue
            if r == 96 and w == 3 and sum(map(len, win)) > 7: continue
            for crf in [None] + list(range(w)):
                full = [list(q) + (['c'] if crf == i else []) for i, q in enumerate(win)]
                v = quick(r, full)
                if v > 60: cands.append((v, crf, win))
    cands.sort(key=lambda c: -c[0])
    print(f"{r} kHz: {len(cands)} window contents above 60 us scanned, best first")
    found = []
    for v, crf, win in cands:
        if len(found) >= 6: break
        hit = None
        for s in tie(NS[r]):
            target = {(s + i) % NS[r]: list(q) + (['c'] if crf == i else []) for i, q in enumerate(win) if q or crf == i}
            plan = try_reach(r, target)
            if plan is not None and replay(r, target, plan):
                hit = (s, target, plan); break
        if hit:
            ph = [[] for _ in range(NS[r])]
            for p, q in hit[1].items(): ph[p] = list(q)
            exact = wait(r, ph)
            found.append(exact)
            print(f"  reached: {hit[1]} wait {f3(exact)} total {f3(exact + FIXED[r])}; peak helpers {max(x[2] for x in hit[2])}")
    res[r] = found

print("\n== C. 192 kHz: every start finds an empty phase, so one stream per phase within the first 17 tie phases")
r = 192; T = tie(24); F = set(T[:17]); rate = m.Rate(192)
print("first 17 tie phases:", T[:17])
best = []
for h in sorted(F):
    for d in range(1, 7):
        win = [(h - d + i) % 24 for i in range(d + 1)]
        if win[0] not in F: continue
        ahead = [q for q in win[:-1] if q in F]
        for combo in itertools.product((None,) + FMT, repeat=len(ahead)):
            if combo[0] is None: continue
            for last in FMT:
                ph = {q: [n] for q, n in zip(ahead, combo) if n}; ph[h] = [last]
                a = sum(RES(r, q[0]) for q in ph.values()) / 125
                if a > 750: continue
                free, worst = 0.0, 0.0
                for i, q in enumerate(win):
                    if q in ph:
                        t = i * 125 / 24; s = max(t, free); worst = max(worst, s - t); free = s + L(r, ph[q][0]) / a
                best.append((worst, sorted(ph.items())))
best.sort(key=lambda b: -b[0])
shown, seen = 0, set()
def phases_of(items):
    ph = [[] for _ in range(24)]
    for q, n in items: ph[q] = list(n)
    return ph
def tandem(rate, target, other):
    """The model's shared packetizer queue with a different placement per port;
    target on port 1, built after port 0 in each phase. Returns wait incl. queue."""
    cyc = {n: m.build_cycles(rate.ns, n) for n in FMT}
    a = {0: Fr(sum(RES(192, x) for q in other for x in q), 125) or Fr(1), 1: Fr(sum(RES(192, x) for q in target for x in q), 125)}
    pk = None; ready = {0: [], 1: []}
    for c in range(4):
        for p in range(24):
            for port, ph in ((0, other), (1, target)):
                for n in ph[p]:
                    t = Fr(125 * p, 24) + 125 * c
                    st = t if pk is None else max(t, pk)
                    pk = st + cyc[n] * m.CYCLE_US
                    ready[port].append((pk, t, L(192, n), c))
    prev = None; worst = Fr(0)
    for rd, t, bits, c in sorted(ready[1], key=lambda x: x[0]):
        s = rd if prev is None else max(rd, prev)
        prev = s + Fr(bits) / a[1]
        if c >= 2: worst = max(worst, s - t)
    return worst
top_total = Fr(0)
for w, items in best:
    k = tuple((q, tuple(n)) for q, n in items)
    if k in seen: continue
    seen.add(k); shown += 1
    if shown > 8: break
    ph = phases_of(items)
    exact = wait(192, ph)
    same = m.tandem_192(rate, ph, None)
    heavy = [[8] if q in T[:14] else [] for q in range(24)]
    alone = tandem(rate, ph, [[] for _ in range(24)])
    busy = tandem(rate, ph, heavy)
    tot_busy = busy + FIXED[192]
    top_total = max(top_total, same, tot_busy)
    print(f"  {items}: wait {f3(exact)}; before packetizer {f3(exact + FIXED[192])}; published tandem, same placement both ports {f3(same)}; "
          f"with the other port at 14 eight-channel {f3(tot_busy)}")
print("largest 192 kHz total above, packetizer queue included:", f3(top_total))
ph = phases_of([(0,[6]),(1,[1])])
print("six-channel in phase 0, one-channel in phase 1, no eight-channel stream: wait", f3(wait(192, ph)), "before packetizer", f3(wait(192, ph) + FIXED[192]))
rt = m.Rate(192); print("  model recursion", f3(m.lindley_wait(rt, ph, None)), "8.6.8.2 sim", f3(m.cbs_sim(rt, ph, None)))
p2 = [[] for _ in range(24)]; order_seen = []
p2[0].append(6)
for _ in range(8):
    q = choose(192, p2, T); p2[q].append(1); order_seen.append(q)
print("  witness: start one six-channel, eight one-channel; placed", order_seen, "; stop all but phase 1's")

print("\n== D. figure the requirement quotes")
overall = {r: max(res[r]) + FIXED[r] for r in res}
print({k: f3(v) for k, v in overall.items()}, "192 kHz with packetizer queue:", f3(top_total))
print("143.347 survives as the largest found:", all(v <= Fr(143348, 1000) for v in overall.values()) and top_total <= Fr(143348, 1000))

print("\n== E. largest cases found, replayed operation by operation, then asked of the published model")
def run_ops(r, ops):
    T = tie(NS[r]); ph = [[] for _ in range(NS[r])]; placed = []
    for x in ops:
        q = choose(r, ph, T); ph[q].append(x); placed.append(q)
        assert sum(RES(r, y) for z in ph for y in z) / 125 <= 750
        assert sum(1 for z in ph for y in z if y != 'c') <= 16
    return ph, placed
ph, placed = run_ops(192, [8] + [1] * 7 + [8] + [1] * 6 + ['c', 1])
print("192 kHz: start eight-channel, seven one-channel, eight-channel, six one-channel, a CRF, one one-channel; placed", placed)
final = [[] for _ in range(24)]; final[0] = [8]; final[1] = [8]; final[2] = [1]
assert ph[0] == [8] and ph[1] == [8] and ph[2] == [1]
rt = m.Rate(192)
print("  stop all but phases 0, 1, 2: mine", f3(wait(192, final)), "model recursion", f3(m.lindley_wait(rt, final, None)),
      "8.6.8.2 sim", f3(m.cbs_sim(rt, final, None)), "before packetizer", f3(wait(192, final) + FIXED[192]), "published tandem", f3(m.tandem_192(rt, final, None)))
ph = [[] for _ in range(12)]; ph[0] = [8, 8]; ph[1] = [1, 1, 1, 1]
rt = m.Rate(96)
print("96 kHz {0: [8, 8], 1: [1, 1, 1, 1]}: mine", f3(wait(96, ph)), "model recursion", f3(m.lindley_wait(rt, ph, None)),
      "8.6.8.2 sim", f3(m.cbs_sim(rt, ph, None)), "total", f3(wait(96, ph) + FIXED[96]))
print("a window of d extra phases loses d phase intervals, so it stays under 125 - d x interval:")
print("  48 kHz, 3 or more phases: under", f3(Fr(125) - Fr(125, 6) * 2), "; 96 kHz, 3 or more phases: under", f3(Fr(125) - Fr(125, 12) * 2),
      "; a 96 kHz case above 143.347 needs a wait above", f3(Fr(143347, 1000) - FIXED[96]))

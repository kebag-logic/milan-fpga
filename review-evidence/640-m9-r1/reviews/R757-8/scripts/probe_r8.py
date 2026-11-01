#!/usr/bin/env python3
"""Round 8 probe of the fewer-reservations tables on the stream-engine page.

Own implementation of the page's phase rule, Table 4.4 frames and an event-level
8.6.8.2 credit simulation, compared with the published model's greedy_add,
lindley_wait and cbs_sim. Replays each row's starts and stops as the page words
them, then searches for reached cases above the page's figures. No timing here
is a measurement.
Usage: python3 -I probe_r8.py <mixed_stagger.py> [seed]
"""
import importlib.util, random, sys
from fractions import Fraction as Fr

spec = importlib.util.spec_from_file_location("published_model", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 640
SAMPLES = {48: 6, 96: 12, 192: 24}
PHASES = SAMPLES
FIXED = {48: Fr(40325, 1000), 96: Fr(32491, 1000), 192: Fr(18093, 1000)}
FORMATS = (1, 2, 4, 6, 8)

def bits(r, n): return 8 * (max(24 + SAMPLES[r] * 4 * n + 22, 68) + 20)
def res(r, n): return 8 * (max(24 + SAMPLES[r] * 4 * n + 1 + 22, 68) + 20)

def tie_order(p):
    if p == 6: return [0, 3, 1, 4, 2, 5]
    out, gap = [0], p
    while len(out) < p:          # "the order halves the gaps"
        gap_points = sorted({j * p // (2 * len(out)) for j in range(2 * len(out))})
        out += [x for x in gap_points if x not in out]
    return out

class Port:
    def __init__(s, r):
        s.r, s.ph, s.tie, s.peak = r, [[] for _ in range(PHASES[r])], tie_order(PHASES[r]), 0
    def start(s, n):
        p = min(s.tie, key=lambda q: (sum(bits(s.r, x) for x in s.ph[q]), s.tie.index(q)))
        s.ph[p].append(n); s.peak = max(s.peak, sum(map(len, s.ph))); return p
    def stop(s, p, n): s.ph[p].remove(n)
    def stop_format(s, n):
        for q in s.ph:
            while n in q: q.remove(n)
    def placed(s): return {i: sorted(q) for i, q in enumerate(s.ph) if q}

def frames(r, ph):
    out = []
    for i, q in enumerate(ph):
        for n in sorted(q):     # "smaller frames are built first"
            out.append((Fr(125 * i, PHASES[r]), bits(r, n)))
    return out

def event_wait(r, ph, cycles=6):
    """8.6.8.2 credit, stepped between events; no interfering traffic."""
    slope = Fr(sum(res(r, n) for q in ph for n in q), 125)
    if not slope: return Fr(0)
    send = slope - 1000
    credit, now, worst = Fr(0), Fr(0), Fr(0)
    for c in range(cycles):
        for rel, b in frames(r, ph):
            t = rel + 125 * c
            if t > now:             # idle: credit recovers to zero, not above
                credit = min(Fr(0), credit + slope * (t - now)); now = t
            start = now
            if credit < 0:
                start = now + (-credit) / slope; credit = Fr(0)
            dur = Fr(b, 1000)
            credit += send * dur
            now = start + dur
            if c >= cycles - 2: worst = max(worst, start - t)
    return worst

def model_wait(r, ph):
    rate = m.Rate(r); return m.lindley_wait(rate, ph, None), m.cbs_sim(rate, ph, None)

def row(name, r, seq, want_placed, want_wait, want_total):
    p = Port(r)
    for op, *a in seq:
        if op == "s":
            for _ in range(a[1]): p.start(a[0])
        elif op == "x": p.stop(*a)
        else: p.stop_format(a[0])
    # the published model places the same starts identically
    q = [[] for _ in range(PHASES[r])]; rate = m.Rate(r)
    for op, *a in seq:
        if op == "s":
            for _ in range(a[1]): m.greedy_add(rate, q, a[0])
        elif op == "x": q[a[0]].remove(a[1])
        else:
            for x in q:
                while a[0] in x: x.remove(a[0])
    own = event_wait(r, p.ph); f, e = model_wait(r, p.ph)
    tot = f + FIXED[r]
    ok = (p.placed() == want_placed and p.placed() == {i: sorted(x) for i, x in enumerate(q) if x}
          and all(f"{float(v):.3f}" == want_wait for v in (own, f, e)) and f"{float(tot):.3f}" == want_total
          and p.peak <= 16)
    print(f"{name}: {r} kHz final {p.placed()} peak {p.peak}; own event {float(own):.3f}; model fifo {float(f):.3f}; "
          f"model 8.6.8.2 {float(e):.3f}; page wait {want_wait}; total {float(tot):.3f}; page {want_total}; {'REPRODUCED' if ok else 'DIFFERS'}")
    return ok

print("== tie order vs model:", all(tie_order(P) == m.spread_order(P) for P in (6, 12, 24)))
print("== the second table, starts and stops as the page words them")
ok = True
ok &= row("row 1", 48, [("s",1,1),("s",8,5),("s",1,2),("s",8,5),("s",1,3),("X",8)], {0:[1]*6}, "103.022", "143.347")
ok &= row("row 2", 48, [("s",8,1),("s",1,2),("x",3,1)], {0:[8],1:[1]}, "71.310", "111.635")
ok &= row("row 3", 96, [("s",1,1),("s",8,11),("s",1,3),("X",8)], {0:[1]*4}, "92.935", "125.426")
ok &= row("row 4", 192, [("s",1,5),("s",6,1),("x",0,1),("x",3,1),("x",6,1),("x",18,1)], {9:[6],12:[1]}, "83.941", "102.034")
print("all rows reproduce:", ok)

print("== k co-phased equal frames against (k-1)x125/k")
for r, n, k in ((48,8,2),(48,8,3),(48,1,6),(96,1,4)):
    ph = [[] for _ in range(PHASES[r])]; ph[0] = [n]*k
    print(f"{r} kHz N={n} k={k}: wait {float(model_wait(r, ph)[0]):.3f}; form {(k-1)*125/k:.3f}")

print("== 192 kHz adjacent-phase pairs, reached by starts and stops")
def pair192(first, second, q):
    p = Port(192); a = p.start(first); assert a == 0
    placed = [p.start(second) for _ in range(8)]
    assert placed[-1] == 1, placed
    for ph_, n_ in zip(placed[:-1], [second]*7): p.stop(ph_, n_)
    own = event_wait(192, p.ph); f, e = model_wait(192, p.ph)
    print(f"{first}-channel then eight {second}-channel; stop all but phase 1: final {p.placed()} peak {p.peak}; "
          f"own event {float(own):.3f}; model fifo {float(f):.3f}; model 8.6.8.2 {float(e):.3f}; "
          f"before the packetizer term {float(f + FIXED[192]):.3f}; with tandem/packetizer model "
          f"{float(m.tandem_192(m.Rate(192), p.ph, None)) if hasattr(m,'tandem_192') else 'n/a'}")
    return f + FIXED[192]
top192 = max(pair192(6, 1, 1), pair192(8, 1, 1), pair192(4, 1, 1), pair192(6, 2, 1), pair192(8, 2, 1))
print("largest of those, before the packetizer term: %.3f; page row 102.034; R758-7 S1 106.927" % float(top192))
print("adding the page's whole 24.827 us mixed packetizer allowance: %.3f (page's largest reached 143.347)" % float(top192 + Fr(24827, 1000)))

print("== search for a reached case above the page's figures (random walk, stops pruned, per rate)")
rng = random.Random(seed)
def prune(r, ph):
    best = model_wait_fast(r, ph)
    improved = True
    while improved:
        improved = False
        for i, q in enumerate(ph):
            for n in sorted(set(q)):
                q.remove(n); w = model_wait_fast(r, ph)
                if w > best: best, improved = w, True; break
                q.append(n)
            if improved: break
    return best
def model_wait_fast(r, ph):
    a = Fr(sum(res(r, n) for q in ph for n in q), 125)
    if not a: return Fr(0)
    fr = frames(r, ph); free, worst = None, Fr(0)
    for c in range(3):
        for rel, b in fr:
            t = rel + 125 * c
            s = t if free is None else max(t, free)
            free = s + Fr(b) / a
            if c: worst = max(worst, s - t)
    return worst
TRIALS = {48: 4000, 96: 4000, 192: 4000}
for r in (48, 96, 192):
    top, arg = Fr(0), None
    for t in range(TRIALS[r]):
        p = Port(r); weights = rng.choice(((1,1,1,1,1),(5,0,0,0,5),(5,1,0,1,5),(1,0,0,3,3)))
        for step in range(rng.randint(2, 40)):
            cnt = sum(map(len, p.ph))
            if cnt and (cnt >= 16 or rng.random() < .25):
                occ = [(i, n) for i, q in enumerate(p.ph) for n in q]
                i, n = rng.choice(occ); p.stop(i, n)
            else:
                p.start(rng.choices(FORMATS, weights)[0])
        ph = [list(q) for q in p.ph]
        w = prune(r, ph)
        if w > top: top, arg = w, {i: sorted(q) for i, q in enumerate(ph) if q}
    print(f"{r} kHz: largest wait found {float(top):.3f}, total {float(top + FIXED[r]):.3f}"
          f"{' before the packetizer term' if r == 192 else ''}: {arg}")

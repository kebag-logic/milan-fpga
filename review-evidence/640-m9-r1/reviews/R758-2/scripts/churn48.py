#!/usr/bin/env python3
"""Independent falsification attempt of the 48 kHz mixed-format bound.
Rule under test (stream-engine page, The phase rule): a starting stream takes the
phase with the least wire time (running frames, CRF included), ties 0,3,1,4,2,5,
never moved; within a phase smaller frames first, CRF last. Random start/stop
walks (at most 16 AAF per port, optional CRF placed by the same rule), each
16-stream state scored with a FIFO start recursion written here; the best states
are re-scored with the event-level 8.6.8.2 simulator of cbs_model.py.
Usage: churn48.py <seed> <seconds>"""
import os, random, sys, time
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cbs_model as cm
TIE = [0, 3, 1, 4, 2, 5]
RANK = {p: i for i, p in enumerate(TIE)}
def L(n): return 8 * (max(24 + 24 * n + 22, 68) + 20)
def RES(n): return 8 * (max(24 + 24 * n + 1 + 22, 68) + 20)
CRF = 704
def place(ph, crf):
    loads = [sum(L(n) for n in ph[q]) + (CRF if crf == q else 0) for q in range(6)]
    return min(range(6), key=lambda q: (loads[q], RANK[q]))
def wait(ph, crf):
    a = F(sum(RES(n) for x in ph for n in x) + (CRF if crf is not None else 0), 125)  # bits/us
    fr = []
    for p in range(6):
        for n in sorted(ph[p], key=L):
            fr.append((F(125 * p, 6), L(n), True))
        if crf == p:
            fr.append((F(125 * p, 6), CRF, False))
    prev = None; worst = F(0)
    for c in range(4):
        for rel, bits, aaf in fr:
            r = rel + 125 * c
            s = r if prev is None else max(r, prev)
            prev = s + F(bits) / a
            if aaf and c >= 2:
                worst = max(worst, s - r)
    return worst
seed, secs = int(sys.argv[1]), float(sys.argv[2])
rnd = random.Random(seed); t0 = time.time(); best = []; n_states = 0
while time.time() - t0 < secs:
    ph = [[] for _ in range(6)]
    crf = None
    for step in range(rnd.randint(20, 120)):
        tot = sum(map(len, ph))
        r = rnd.random()
        if r < 0.03:
            crf = place(ph, None) if crf is None else None
        elif tot < 16 and (r < 0.62 or tot == 0):
            n = rnd.choice((1, 1, 1, 2, 2, 4, 6, 8, 8, 8))
            ph[place(ph, crf)].append(n)
        else:
            q = rnd.choice([q for q in range(6) if ph[q]])
            ph[q].pop(rnd.randrange(len(ph[q])))
        if sum(map(len, ph)) == 16:
            res = sum(RES(n) for x in ph for n in x) + (CRF if crf is not None else 0)
            if F(res, 125) > 750:
                continue
            n_states += 1
            w = wait(ph, crf)
            best.append((w, [sorted(x) for x in ph], crf))
            if len(best) > 400:
                best.sort(key=lambda b: -b[0]); best = best[:20]
best.sort(key=lambda b: -b[0])
uniq = []
for b in best:
    if b[1:] not in [u[1:] for u in uniq]:
        uniq.append(b)
print(f"seed {seed}: 16-stream states scored {n_states}")
for w, ph, crf in uniq[:3]:
    fr = [[L(n) for n in sorted(x)] for x in ph]
    sl = F(sum(RES(n) for x in ph for n in x) * 8000) + (cm.BW_CRF if crf is not None else 0)
    if crf is not None:
        fr[crf].append(CRF)
    ev, _ = cm.simulate(fr, sl, periods=14)
    print(f"  recursion {float(w):.3f} us, event sim {cm.us(ev):.3f} us, phases {ph}, crf {crf}")

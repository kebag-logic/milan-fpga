"""192 kHz: every occupancy that starts and stops reach at 16 AAF streams per
port under the least-wire-time rule, with the CRF at any reachable tie rank or
absent. With at most 17 entities and 24 phases a start always finds an empty
phase, so it takes the lowest-rank empty phase; the occupied set therefore lies
in the first 17 tie ranks. For each placement: (a) the one-format total with
the packetizer as a queue (the model's tandem_192), (b) the worst mixed shaper
wait by the model's own window objective (exact_192b's search), plus the
model's fixed terms. Usage: python3 -I probe192_placements.py <model-dir>"""
import itertools
import sys
sys.path.insert(0, sys.argv[1])
import mixed_stagger as m
from fractions import Fraction as Fr

r = m.Rate(192)
first17 = r.tie[:17]
cases = []
for k in range(17):                      # CRF at rank k, AAF at the other 16
    occ = [q for q in first17 if q != r.tie[k]]
    cases.append((f"crf rank {k}", occ, r.tie[k]))
    cases.append((f"crf stopped after rank {k}", occ, None))
cases.append(("no crf, first 16", r.tie[:16], None))

def mixed_worst(occ, crf):
    occ = set(occ)
    best = None
    for h in sorted(occ):
        for d in range(r.P):
            win = [(h - d + i) % r.P for i in range(d + 1)]
            ahead = [q for q in win[:-1] if q in occ]
            crf_ahead = crf is not None and crf in win[:-1]
            outside = m.NMAX - len(ahead) - 1
            for combo in itertools.combinations_with_replacement(m.FORMATS, len(ahead)):
                num = sum(r.L[n] for n in combo) + (m.CRF_L if crf_ahead else 0)
                res = (sum(r.res[n] for n in combo) + r.res[1] + outside * r.resmin
                       + (m.CRF_RES if crf is not None else 0))
                if Fr(res, m.INTERVAL) > m.CAP:
                    continue
                v = Fr(num * m.INTERVAL, res) - d * r.tph
                if best is None or v > best[0]:
                    best = (v, h, d, combo, crf_ahead)
    return best

uni_worst = mix_worst = None
for name, occ, crf in cases:
    u = None
    for n in m.FORMATS:
        ph = [[] for _ in range(r.P)]
        for q in occ:
            ph[q] = [n]
        if m.idle_slope(r, ph, crf) > m.CAP:
            continue
        t = m.tandem_192(r, ph, crf)
        u = (t, n) if u is None or t > u[0] else u
    w = mixed_worst(occ, crf)
    tot = w[0] + r.t_pin + m.T_CDC + m.T_MAC + m.I_1522
    print(f"{name:28s} one-format worst {m.fmt(u[0])} us (N={u[1]}); mixed shaper {m.fmt(w[0])} us, total before packetizer {m.fmt(tot)} us")
    if uni_worst is None or u[0] > uni_worst[0]:
        uni_worst = (u[0], name, u[1])
    if mix_worst is None or tot > mix_worst[0]:
        mix_worst = (tot, name)
print("WORST one-format:", m.fmt(uni_worst[0]), uni_worst[1:], " WORST mixed before packetizer:", m.fmt(mix_worst[0]), mix_worst[1])

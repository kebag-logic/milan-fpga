import sys
sys.path.insert(0, '.')
import mixed_stagger as m
r = m.Rate(192)
for n in m.FORMATS:
    ph = [[] for _ in range(r.P)]
    for q in r.tie[1:17]: ph[q] = [n]
    c = r.tie[0]
    if m.idle_slope(r, ph, c) > m.CAP: print(n, 'above cap'); continue
    print(n, 'crf first', m.fmt(m.tandem_192(r, ph, c)))

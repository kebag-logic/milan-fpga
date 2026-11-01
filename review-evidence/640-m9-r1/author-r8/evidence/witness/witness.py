"""Check each round-8 witness sequence under the page's exact phase rule, through the
reviewer's arithmetic restated here and through the published model's greedy_add,
lindley_wait and cbs_sim. Usage: python3 -I witness.py <mixed_stagger.py>"""
import importlib.util, sys
from fractions import Fraction as Fr
spec = importlib.util.spec_from_file_location("published_model", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FIXED = {48: Fr(40325, 1000), 96: Fr(32491, 1000), 192: Fr(18093, 1000)}

def run(name, khz, seq, want_wait, want_total, want_phases):
    """seq: ('s', n) starts an n-channel stream; ('x', phase, n) stops one."""
    r = m.Rate(khz); ph = [[] for _ in range({48: 6, 96: 12, 192: 24}[khz])]
    peak = 0; placed = []
    for op in seq:
        if op[0] == 's':
            before = [list(p) for p in ph]
            m.greedy_add(r, ph, op[1])
            q = next(i for i in range(len(ph)) if len(ph[i]) != len(before[i]))
            placed.append(q)
        else:
            ph[op[1]].remove(op[2])
        peak = max(peak, sum(map(len, ph)))
    assert peak <= 16, peak
    f = m.lindley_wait(r, ph, None); e = m.cbs_sim(r, ph, None); idle = m.idle_slope(r, ph, None)
    tot = Fr(f) + FIXED[khz]
    ok = (f"{float(f):.3f}" == want_wait and f"{float(e):.3f}" == want_wait and f"{float(tot):.3f}" == want_total
          and {i: sorted(p) for i, p in enumerate(ph) if p} == want_phases)
    print(f"{name}: {khz} kHz start phases {placed}; peak {peak} streams; final "
          f"{ {i: p for i, p in enumerate(ph) if p} }; idleSlope {float(idle):.3f} Mb/s; fifo {float(f):.3f}; "
          f"event-exact {float(e):.3f}; with interference {float(f)+12.336:.3f}; total {float(tot):.3f}; {'AGREES' if ok else 'DIFFERS'}")
    return ok

S = lambda n, k=1: [('s', n)] * k
ok = True
ok &= run("A six one-channel", 48, S(1)+S(8,5)+S(1,2)+S(8,5)+S(1,3)+[('x',p,8) for p in (3,1,4,2,5)]*2, "103.022", "143.347", {0:[1]*6})
ok &= run("B eight then one", 48, S(8)+S(1)+S(1)+[('x',3,1)], "71.310", "111.635", {0:[8],1:[1]})
ok &= run("C four one-channel", 96, S(1)+S(8,11)+S(1,3)+[('x',p,8) for p in range(1,12)], "92.935", "125.426", {0:[1]*4})
ok &= run("D six then one", 192, S(1,5)+S(6)+[('x',p,1) for p in (0,6,18,3)], "83.941", "102.034", {9:[6],12:[1]})
# R758-7 S1's larger 192 kHz case, for the handoff only
r = m.Rate(192); ph=[[] for _ in range(24)]; ph[3]=[8]; ph[6]=[1]
print("R758-7 S1, 192 kHz, 8 in phase 3, 1 in phase 6: fifo %.3f; total before packetizer %.3f" % (float(m.lindley_wait(r,ph,None)), float(Fr(m.lindley_wait(r,ph,None))+FIXED[192])))
print("ALL AGREE" if ok else "SOME DIFFER"); sys.exit(0 if ok else 1)

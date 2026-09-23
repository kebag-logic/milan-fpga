#!/usr/bin/env python3
"""Integer model of the #68 servo leg driving an ideal PHC, one 125 ms Sync
interval per step. Independent of the ROM: it restates the documented rule.

  step  iff  first synchronization  and  |offset| > 1 s
  slew  otherwise: PI on the offset saturated at +-20 us, integrator +-200 ppm

Prints, per clock, the largest trim the slew can program (in ppm) and how a
first-sync 900 ms offset converges when the master runs at +140 ppm (the
engine suite's closed-loop master), at nominal rate, and at -140 ppm: the
"about 33 to 83 minutes, about 47 against a nominal master" of the #68
DECISION.
"""
import sys

def gains(clk):
    return round((1 << 24) * 64 * 8 / clk), round(200 * (1 << 24) * 1000 / clk)

def run(clk, off0_ns, master_ppm=140.0, intervals=60000):
    m, ilim = gains(clk)
    ticks = clk // 8                      # ticks per 125 ms interval
    ns_per_unit = ticks / (1 << 24)       # phase moved per addend unit/interval
    e = float(off0_ns)                    # local minus master, ns
    intg, trim, first, steps = 0, 0, True, 0
    peak_trim = 0
    hist = []
    for k in range(intervals):
        off = int(round(e))
        if first and abs(off) > 1_000_000_000:
            e -= off; steps += 1; trim = -intg
        else:
            s = max(-20000, min(20000, off))
            t = (s * m) >> 6
            intg = max(-ilim, min(ilim, intg + (t >> 2)))
            trim = -((t - (t >> 2)) + intg)
        first = False
        peak_trim = max(peak_trim, abs(trim))
        # one interval of free run: our rate trim against the master's rate
        e += trim * ns_per_unit - master_ppm * 1e-6 * 125e6
        hist.append(e)
    return hist, steps, peak_trim, ns_per_unit

for clk in (100_000_000, 2_000_000):
    m, ilim = gains(clk)
    for master_ppm in (140.0, 0.0, -140.0):
        hist, steps, peak, npu = run(clk, 900_000_000, master_ppm)
        ppm = peak * npu / 125e6 * 1e6
        lock = next((k for k in range(len(hist)) if all(abs(x) < 200 for x in hist[k:k+80])), None)
        sign_flip = next((k for k in range(len(hist)) if hist[k] < 0), None)
        under = min(hist[sign_flip:]) if sign_flip is not None else 0.0
        print(f"clk {clk}, master {master_ppm:+.0f} ppm: gain_m {m} ilim {ilim}; "
              f"peak slew trim {peak} units = {ppm:.1f} ppm; "
              f"steps {steps}; first zero crossing after {sign_flip} intervals "
              f"({(sign_flip or 0) * 0.125 / 60:.1f} min); worst overshoot {under:.0f} ns; "
              f"|e|<200 ns held from interval {lock} ({(lock or 0) * 0.125 / 60:.1f} min)")
    h2, s2, _, _ = run(clk, 1_100_000_000)
    print(f"   first-sync 1.1 s: steps {s2}; |e| after 24 intervals {abs(h2[23]):.0f} ns")
sys.exit(0)

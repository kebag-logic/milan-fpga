#!/usr/bin/env python3
"""Probe: the cross-port conversion error bound and its effect on the merge.

Usage: python3 -I probe_conversion_error.py <dir-of-merge_model.py>

Part 1, arithmetic. The talker adds its latched PHC offset at stamp time;
the listener subtracts its own latched offset at the copy's arrival. The
offset (PHC1 - PHC0) drifts at the two grandmasters' frequency difference,
at most 200 ppm (IEEE 802.1AS-2020 B.1.1, 100 ppm each). So the two
offsets are evaluated at instants that differ by the latch ages AND by the
interval from stamping to arrival, which is up to the class A transit.
The page counts only the latch ages (2 x 125 us).

Part 2, effect. The author's merge model (unchanged) is re-run with its
injected error raised from 2.210 us to the corrected bound and to 10 us,
to show whether the merge verdicts depend on the figure.
"""
import sys

sys.path.insert(0, sys.argv[1])
import merge_model as mm  # noqa: E402

PPM = 200e-6
SYNC = 2 * 1.0            # us, one per network (B.3), as the page takes it
GRAN = 4 * 0.040          # us, four PHC reads (B.1.2)
LATCH = 125.0             # us, latch period
page = SYNC + 2 * LATCH * PPM + GRAN
print(f"page's bound: {SYNC:.3f} + {2 * LATCH * PPM:.3f} + {GRAN:.3f} = {page:.3f} us")
for label, transit in (("talker latency 0.1 ms + transit 2 ms (class A)", 2100.0),
                       ("the 2.667 ms render span as the separation", 2666.667)):
    sep = transit + LATCH          # stamp-to-arrival plus the older latch age
    drift = sep * PPM
    print(f"{label}: offsets {sep:.0f} us apart, drift {drift:.3f} us; "
          f"bound {SYNC:.3f} + {drift:.3f} + {GRAN:.3f} = {SYNC + drift + GRAN:.3f} us")

ok_all = True
for ex in (2.210, 2.715, 10.0):
    mm.E_X = ex
    fails = [name for name, case, want in mm.CASES if not mm.judge(mm.run(case), want)]
    ok_all &= not fails
    print(f"merge model with injected error +-{ex:.3f} us: {len(mm.CASES) - len(fails)} of "
          f"{len(mm.CASES)} cases pass{'; failing: ' + str(fails) if fails else ''}")
print("MERGE VERDICTS UNCHANGED" if ok_all else "MERGE VERDICTS CHANGE")
sys.exit(0 if ok_all else 1)

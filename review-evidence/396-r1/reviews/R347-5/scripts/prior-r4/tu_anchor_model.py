#!/usr/bin/env python3
"""R347-3 cycle model of KL_ptp_clock_validity's tu holdover.

Usage: python3 -B tu_anchor_model.py

Transcribes hdl/ieee8021as/ptp_timestamp/KL_ptp_clock_validity.sv:152-211 at
the reviewed head: free-running quarter-tick prescaler (qdiv_r, qtick_w),
hold_r reloaded to HOLD_QTICK_P (2) on EVERY discontinuity pulse (:199) and
decremented on qtick (:200), and ts_uncertain_o = ~sync_ok | hold | disc_p
(:211). The prescaler is scaled to QTICK cycles per 0.25 s; the timing ratios
are exact because the RTL is a pure cycle counter.

Scenario: a grandmaster change (gm_id edge) at t=0, followed by a PHC step
d seconds later, as the #117 silicon evidence records (adoption, then the
PHC step; docs/findings/117_GPTP_SILICON_EVIDENCE.md:351). sync_ok stays 1.
The script reports when tu clears, measured from the first recorded event
(the GM change the interval begins with) and from the last one (the step).
"""
from __future__ import annotations

QTICK = 1000            # cycles per 0.25 s quarter tick (scaled QTICK_CYC_P)
HOLD = 2                # HOLD_QTICK_P at the reviewed head
CPS = 4 * QTICK         # cycles per second


def clear_time(phase_cycles: int, pulses: list[int]) -> int:
    """Cycle at which ts_uncertain_o first returns to 0 after the first pulse."""
    qdiv = phase_cycles % QTICK
    hold = 0
    t = 0
    seen = False
    while True:
        qtick = qdiv == QTICK - 1
        disc = t in pulses
        tu = hold != 0 or disc          # sync_ok held at 1
        if seen and not tu:
            return t
        seen = seen or tu
        # registered updates (:160-162, :193-201)
        if disc:
            hold = HOLD
        elif qtick and hold:
            hold -= 1
        qdiv = 0 if qtick else qdiv + 1
        t += 1


def main() -> int:
    print("tu clear time after a GM change at t=0 with a PHC step at t=d "
          "(seconds; worst case over the prescaler phase)")
    print(f"{'d':>6} {'from GM change min..max':>26} {'from step min..max':>22} "
          f"{'> 0.5 s from GM change':>24}")
    for d_ms in (0, 20, 50, 100, 125, 200):
        d = d_ms * CPS // 1000
        from_first = []
        from_last = []
        for phase in range(0, QTICK, 7):
            c = clear_time(phase, [0, d] if d else [0])
            from_first.append(c / CPS)
            from_last.append((c - d) / CPS)
        over = max(from_first) > 0.5
        print(f"{d_ms / 1000:6.3f} {min(from_first):12.3f}..{max(from_first):<12.3f}"
              f"{min(from_last):10.3f}..{max(from_last):<10.3f} {str(over):>24}")
    print("Single event (d=0): clears 0.25..0.5 s after it, the implemented holdover.")
    print("Chained events: clears 0.25..0.5 s after the LAST pulse, so up to d+0.5 s")
    print("after the GM change. The head's rule measures from the discontinuity the")
    print("interval begins with; at fine observation resolution a correct design fails.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

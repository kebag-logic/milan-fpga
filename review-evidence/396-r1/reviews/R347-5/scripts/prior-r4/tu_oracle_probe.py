#!/usr/bin/env python3
"""R347-4 probe of check_release_tu against the implemented tu holdover.

Usage: python3 -B tu_oracle_probe.py <repo-root>

Imports tb/tools/torture_campaign.py from the reviewed tree read-only and
reuses the unchanged R347-3 cycle model (tu_anchor_model.clear_time, a
transcription of KL_ptp_clock_validity.sv:152-211, where tu rises in the
same cycle as the discontinuity pulse, :211).

Part A: DUT-side interval. For a GM edge at t=0 and a step at t=d, every
prescaler phase's clear time is graded with the interval starting exactly at
the first pulse. Expect PASS everywhere (the round-4 anchor honors the RTL).

Part B: wire-observed interval. tu is visible only on transmitted AVTPDUs, so
the first tu=1 packet follows the pulse by 0 < lag <= one packet period, and
the clear is observed at the first tu=0 packet. The event timestamp is the
pulse instant. With a lone discontinuity, the oracle's containment test
(start <= event < clear) excludes the event and the interval is graded as
uncorrelated, although the lag is far below the stated resolution.
"""
from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from tu_anchor_model import CPS, QTICK, clear_time  # noqa: E402


def load(repo: Path):
    spec = importlib.util.spec_from_file_location(
        "tc", repo / "tb/tools/torture_campaign.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tc"] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    tc = load(Path(sys.argv[1]))
    bound = tc.build_plan(["soak"])[0].args["tu_holdover_bound_s"]
    res = 0.001
    ok = True
    print(f"bound={bound} resolution={res}")
    print("Part A: DUT-side interval, GM edge at 0 plus step at d")
    for d_ms in (0, 20, 50, 100, 125, 200):
        d = d_ms * CPS // 1000
        verdicts = set()
        worst = 0.0
        for phase in range(0, QTICK, 7):
            c = clear_time(phase, [0, d] if d else [0]) / CPS
            worst = max(worst, c)
            events = [0.0, d / CPS] if d else [0.0]
            verdicts.add(tc.check_release_tu((0.0, c), events, holdover_bound_s=bound,
                                             observation_resolution_s=res,
                                             capture_complete=True)[0])
        print(f"  d={d_ms / 1000:.3f} worst_clear={worst:.3f} verdicts={sorted(verdicts)}")
        ok &= verdicts == {"PASS"}
    print("Part B: wire-observed interval, lone discontinuity at t_e")
    for period in (125e-6, 1e-3):
        for lag_frac in (0.01, 0.5, 1.0):
            t_e = 10.0
            start = t_e + lag_frac * period
            c = t_e + clear_time(0, [0]) / CPS
            clear = math.ceil(c / period) * period
            v, ev = tc.check_release_tu((start, clear), [t_e], holdover_bound_s=bound,
                                        observation_resolution_s=res, capture_complete=True)
            print(f"  period={period * 1e6:.0f}us lag={lag_frac * period * 1e6:.2f}us "
                  f"start-event={start - t_e:.6f}s <= res: {start - t_e <= res} -> {v} {ev}")
    print("Part B': same lag, GM edge before start and step inside")
    v, ev = tc.check_release_tu((10.0000625, 10.45), [10.0, 10.2], holdover_bound_s=bound,
                                observation_resolution_s=res, capture_complete=True)
    print(f"  -> {v} {ev}")
    print("Part C: event recorded exactly at the observed start (self-test shape)")
    v, ev = tc.check_release_tu((10.0, 10.45), [10.0], holdover_bound_s=bound,
                                observation_resolution_s=res, capture_complete=True)
    print(f"  -> {v} {ev}")
    print("Part D: tu raised long before its only discontinuity")
    v, ev = tc.check_release_tu((0.0, 10.4), [10.0], holdover_bound_s=bound,
                                observation_resolution_s=res, capture_complete=True)
    print(f"  -> {v} {ev}")
    print("Part A all PASS:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

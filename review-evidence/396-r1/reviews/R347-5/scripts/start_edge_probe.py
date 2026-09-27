#!/usr/bin/env python3
"""R347-5 probe of the round-5 start-edge allowance in check_release_tu.

Usage: python3 -B start_edge_probe.py <repo-root>

Imports tb/tools/torture_campaign.py from the reviewed tree read-only.

Part 1: the decision's arms at the self-test's origin (observed start 0).
Part 2: the same arms translated to realistic absolute capture times, where
  the event, the observed start and the resolution are all binary floats.
  Reports any case whose verdict differs from the exact-arithmetic verdict
  computed with fractions.Fraction on the same float inputs, and separately
  any case where a lag entered as exactly the resolution is excluded because
  start - resolution rounds above the event.
Part 3: symmetry with the clear edge (clear exactly at deadline).
Part 4: multi-event and ordering shapes around the start edge.
Part 5: tu raised long before its only discontinuity (decided behavior).
"""
from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path


def load(repo: Path):
    spec = importlib.util.spec_from_file_location("tc", repo / "tb/tools/torture_campaign.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["tc"] = mod
    spec.loader.exec_module(mod)
    return mod


def grade(tc, start, clear, events, res, bound=0.5):
    return tc.check_release_tu((start, clear), events, holdover_bound_s=bound,
                               observation_resolution_s=res, capture_complete=True)


def exact(start, clear, events, res, bound=0.5):
    """Same rule, exact arithmetic on the same float inputs."""
    s, c, r, b = (Fraction(x) for x in (start, clear, res, bound))
    inside = [Fraction(e) for e in events if s - r <= Fraction(e) < c]
    if not inside:
        return "FAIL"
    return "PASS" if c <= max(inside) + b + r else "FAIL"


def main() -> int:
    tc = load(Path(sys.argv[1]))
    ok = True
    print("Part 1: decision arms, observed interval (0, 0.4), bound 0.5")
    arms = ((-0.0005, 0.001, "PASS", "0.5x resolution before start"),
            (-0.002, 0.001, "FAIL", "2x resolution before start"),
            (0.0, 0.001, "PASS", "exactly at start"),
            (0.0, 0.0, "PASS", "exactly at start, zero resolution"),
            (-0.1, 0.001, "FAIL", "-0.1 s arm"),
            (-1e-9, 0.0, "FAIL", "1 ns before start, zero resolution"),
            (0.4, 0.001, "FAIL", "exactly at clear"))
    for event, res, want, label in arms:
        got, ev = grade(tc, 0.0, 0.4, [event], res)
        ok &= got == want
        print(f"  {label:38s} event={event:+.6f} res={res} -> {got} (want {want})")

    print("Part 2: absolute capture times, lag in {0.5x, 1x, 2x} resolution")
    flips = 0
    exact_lag_excluded = 0
    cases = 0
    for res in (0.001, 0.0001, 0.00025, 1e-6):
        for k in range(1, 20001):
            t_e = k * 0.0137 + 3.3
            for frac, want in ((0.5, "PASS"), (1.0, "PASS"), (2.0, "FAIL")):
                start = t_e + frac * res
                clear = t_e + 0.45
                got = grade(tc, start, clear, [t_e], res)[0]
                cases += 1
                if got != exact(start, clear, [t_e], res):
                    flips += 1
                if frac == 1.0 and got == "FAIL":
                    exact_lag_excluded += 1
                if frac != 1.0 and got != want:
                    ok = False
    print(f"  cases={cases} verdicts differing from exact arithmetic on the same inputs={flips}")
    print(f"  lag entered as exactly 1x resolution but excluded by rounding={exact_lag_excluded}")
    print("  (0.5x and 2x arms all as decided)" if ok else "  0.5x/2x arm mismatch")

    print("Part 3: clear edge symmetry, clear exactly at event + bound + resolution")
    clear_flips = 0
    for k in range(1, 20001):
        t_e = k * 0.0137 + 3.3
        clear = t_e + 0.5 + 0.001
        got = grade(tc, t_e, clear, [t_e], 0.001)[0]
        if got != "PASS":
            clear_flips += 1
    print(f"  clear entered as exactly the deadline but failed by rounding={clear_flips} of 20000")

    print("Part 4: multi-event shapes")
    shapes = (("GM edge 0.5x res before start, step at +0.2, clear +0.69", 10.0005, 10.69,
               [10.0, 10.2], 0.001, "PASS"),
              ("GM edge 0.5x res before start, step at +0.2, clear +0.71", 10.0005, 10.71,
               [10.0, 10.2], 0.001, "FAIL"),
              ("pre-window event ignored, in-window event anchors", 10.0, 10.45,
               [9.0, 10.0], 0.001, "PASS"),
              ("only event after clear", 10.0, 10.45, [10.46], 0.001, "FAIL"),
              ("empty event list", 10.0, 10.45, [], 0.001, "FAIL"))
    for label, s, c, evs, res, want in shapes:
        got, ev = grade(tc, s, c, evs, res)
        ok &= got == want
        print(f"  {label:58s} -> {got} (want {want})")

    print("Part 5: tu raised 10 s before its only discontinuity (decided, disclosed)")
    got, ev = grade(tc, 0.0, 10.4, [10.0], 0.001)
    print(f"  -> {got} {ev}")
    print("DECISION ARMS OK:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

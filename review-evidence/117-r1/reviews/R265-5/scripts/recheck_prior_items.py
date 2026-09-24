#!/usr/bin/env python3
"""Re-derive the step 3 dark window and both holdover spans from raw files.

Usage: recheck_prior_items.py <bench-a202/bench directory>

Dark window: the last tap record (either direction) before the outage and the
first after it, with the direction of the last one. Holdover: CLKV_STAT bit 3
episodes after the outlet-off command, as (first set sample, first clear
sample, sample count).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import recompute_step3 as r3  # noqa: E402


def main():
    base = Path(sys.argv[1])
    for n in range(1, 7):
        cdir = base / f"cycle{n}"
        off = r3.offsets(cdir)
        ps = (cdir / "powerstrip.txt").read_text()
        t_off = float(re.search(r"T_OFF_CMD (\S+)", ps).group(1)) - off["pi"]
        recs, _ = r3.tap(cdir, n)
        bb = [(s - off["ubuntu-server"] - t_off, p, k) for s, p, k in recs]
        before = max((t, p, k) for t, p, k in bb if t < 10)
        after = min(t for t, p, k in bb if t > 10)
        cs = r3.console(cdir)
        eps, cur = [], None
        for c in cs:
            t = c["t"] - t_off
            if t < 0:
                continue
            h = int(c["clkv"], 16) >> 3 & 1
            if h and cur is None:
                cur = [t, None, 0]
            if h:
                cur[2] += 1
            if not h and cur is not None:
                cur[1] = t
                eps.append(cur)
                cur = None
        print(f"cycle {n}: last record {before[0]:.2f} s (tap port {before[1]}, {before[2]}); "
              f"first after {after:.2f} s; holdover episodes "
              + "; ".join(f"set {a:.2f} clear {b:.2f} span {b - a:.2f} s, {k} samples" for a, b, k in eps[:3]))


if __name__ == "__main__":
    main()

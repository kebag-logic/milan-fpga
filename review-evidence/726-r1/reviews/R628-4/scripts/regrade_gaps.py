#!/usr/bin/env python3
"""Independently re-grade the #726 corrected cadence criterion from a stream
counter run log (NOTE/SERVICE/GAPS lines printed by stream_counters.hpp).

Criterion (issue #726 comment 6132483068):
  spacing: consecutive notifications for one descriptor and recipient are
           >= 1000 ms apart;
  refresh: every consecutive gap is <= 1000 ms + measured service delay.
Also checks the final wait (end - last) against the same bound, re-derives the
fixture's own GAPS line, and evaluates both verdicts for measurement starts
shifted through one second (every cycle; 1000 cycles = 1 ms).

Usage: regrade_gaps.py <run.log> [--quiet]
Exit 0 when every row passes both conditions and agrees with the fixture's
GAPS line; 1 otherwise.
"""
import sys
from collections import defaultdict

MS = 1000
SECOND = 1000 * MS


def main(path, quiet):
    notes = defaultdict(list)
    service = {}
    gaps_line = {}
    shape = None
    for line in open(path, errors="replace"):
        p = line.strip().split(",")
        if p[0] == "NOTE" and len(p) == 5:
            notes[(int(p[1]), int(p[2]), int(p[3]))].append(int(p[4]))
        elif p[0] == "SERVICE" and len(p) == 3:
            service[int(p[1])] = int(p[2])
        elif p[0] == "GAPS" and len(p) == 11:
            shape = int(p[1])
            key = (int(p[2]), int(p[3]), int(p[4]))
            gaps_line[key] = dict(start=int(p[5]), count=int(p[6]),
                                  min=float(p[7]), max=float(p[8]),
                                  tail=float(p[9]), service=float(p[10]))
    if shape is None:
        print("no GAPS rows"); return 1
    ok = True
    total_gaps = 0
    allmin, allmax, svcmax = 10**12, 0, 0
    for key, g in sorted(gaps_line.items()):
        ty, s, r = key
        slot = (0 if ty == 5 else shape + 1) + s
        svc = service[slot]
        times = sorted(notes.get(key, []))
        end = (times[-1] if times else 0) + round(g["tail"] * MS)

        def grade(start):
            sel = [t for t in times if start <= t < end]
            d = [b - a for a, b in zip(sel, sel[1:])]
            last = sel[-1] if sel else start
            spacing = all(x >= SECOND for x in d)
            refresh = (len(sel) >= 2 and all(x <= SECOND + svc for x in d)
                       and end - last <= SECOND + svc)
            return sel, d, spacing, refresh

        sel, d, spacing, refresh = grade(0)
        total_gaps += len(d)
        if d:
            allmin = min(allmin, min(d)); allmax = max(allmax, max(d))
        svcmax = max(svcmax, svc)
        agree = (len(sel) == g["count"] and abs(svc / MS - g["service"]) < 1e-3
                 and (not d or (abs(min(d) / MS - g["min"]) < 1e-3
                                and abs(max(d) / MS - g["max"]) < 1e-3)))
        # Shift probe through one second. grade(start) is piecewise constant
        # between notification instants (selection changes only when start
        # passes a timestamp), so evaluating 0, SECOND and every t, t+1 inside
        # [0, SECOND] covers every cycle start exactly.
        stable = True
        starts = {0, SECOND} | {x for t in times for x in (t, t + 1) if 0 <= x <= SECOND}
        for start in sorted(starts):
            _, _, sp, rf = grade(start)
            if sp != spacing or rf != refresh:
                stable = False
                break
        row_ok = spacing and refresh and agree and stable
        ok &= row_ok
        if not quiet or not row_ok:
            print(f"ROW type={ty} index={s} recipient={r} n={len(sel)} "
                  f"gaps_ms={[x / MS for x in d]} tail_ms={(end - (sel[-1] if sel else 0)) / MS:.3f} "
                  f"service_ms={svc / MS:.3f} spacing={spacing} refresh={refresh} "
                  f"agrees_with_fixture={agree} shift_stable={stable}")
    print(f"SUMMARY shape={shape} rows={len(gaps_line)} gaps={total_gaps} "
          f"min_gap_ms={allmin / MS:.3f} max_gap_ms={allmax / MS:.3f} "
          f"max_service_ms={svcmax / MS:.3f} verdict={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--quiet" in sys.argv))

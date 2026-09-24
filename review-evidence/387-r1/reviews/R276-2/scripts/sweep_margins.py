#!/usr/bin/env python3
"""Summarise a gmstep feed-delay sweep: per delay, the counted render
re-base and the first mr toggle relative to the plane's step pulse, the
tu hold, the talker's longest pause and interval, and the tally; then the
ranges against the leg's own windows (500 cycles for the re-base, two
talker intervals for the toggle, four intervals for a pause).

Usage: sweep_margins.py <logdir>   (files named delay-<n>.log)
"""
import pathlib
import re
import sys

PAT = {
    "rebase": re.compile(r"RENDER: counted recentre at cycle \d+ \(step pulse ([+-]\d+)\)"),
    "toggle": re.compile(r"RESTART: mr toggle first sent at cycle \d+ \(step pulse ([+-]\d+)\)"),
    "interval": re.compile(r"TALKER: baseline interval ([\d.]+) cycles"),
    "held": re.compile(r"TU: held (\d+) cycles"),
    "pause": re.compile(r"longest pause (\d+),"),
    "tally": re.compile(r"== gmstep: checks: (\d+)\s+failures: (\d+) =="),
}


def main() -> int:
    logs = sorted(pathlib.Path(sys.argv[1]).glob("delay-*.log"),
                  key=lambda p: int(p.stem.split("-")[1]))
    rows = []
    for log in logs:
        text = log.read_text()
        row = {"delay": int(log.stem.split("-")[1])}
        for key, pat in PAT.items():
            row[key] = pat.findall(text)
        rows.append(row)
        print(f"delay={row['delay']} rebase={row['rebase']} toggle={row['toggle']} "
              f"interval={row['interval']} held={row['held']} pause={row['pause']} "
              f"tally={row['tally']}")
    rebases = [int(v) for r in rows for v in r["rebase"]]
    toggles = [int(v) for r in rows for v in r["toggle"]]
    intervals = [float(v) for r in rows for v in r["interval"]]
    pauses = [int(v) for r in rows for v in r["pause"]]
    print(f"runs={len(rows)}")
    if rebases:
        print(f"re-base offset after the step pulse: {min(rebases)}..{max(rebases)} "
              f"(window 1..500), {len(rebases)} re-bases")
    if toggles and intervals:
        print(f"first mr toggle offset: {min(toggles)}..{max(toggles)} "
              f"(window 1..{2 * min(intervals):.0f}), {len(toggles)} toggles")
    if pauses and intervals:
        print(f"longest talker pause: {min(pauses)}..{max(pauses)} "
              f"(limit {4 * min(intervals):.0f}); interval {min(intervals)}..{max(intervals)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

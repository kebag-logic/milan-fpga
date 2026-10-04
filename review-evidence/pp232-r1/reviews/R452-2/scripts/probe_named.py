#!/usr/bin/env python3
"""Summarize clear_cycle_probe.sh logs: for each planted control, the named committed
checks it fails in tb/aecp_notify and the tb/pp_top tally.

Usage: probe_named.py PROBE_DIR CONTROL...
Prints one line per control and exits 1 if any control fails no named check.
"""
import re
import sys
from pathlib import Path

FAIL = re.compile(r"^\s*FAIL: ([A-Z]+[0-9]*[a-z]?):", re.M)
BUILD = re.compile(r"^\[build (\w+)\] (\d+) checks, (\d+) failures", re.M)
TALLY = re.compile(r"(\d+) checks: (\d+) PASS, (\d+) FAIL")


def main() -> int:
    d = Path(sys.argv[1])
    uncaught = 0
    for c in sys.argv[2:]:
        an = (d / f"{c}-aecp_notify.log").read_text(errors="replace")
        pt = (d / f"{c}-pp_top.log").read_text(errors="replace")
        names = sorted(set(FAIL.findall(an)), key=lambda s: (re.sub(r"\d.*", "", s), s))
        builds = "; ".join(f"{b} {n} checks {f} failing" for b, n, f in BUILD.findall(an))
        t = TALLY.findall(pt)
        pp = f"{t[-1][0]} checks, {t[-1][2]} FAIL" if t else "no final tally (make stopped after a build with failing checks)"
        pp_fail = sorted(set(re.findall(r"^\s*FAIL: ([^:\n]{1,40})", pt, re.M)))[:6]
        caught = bool(names)
        uncaught += 0 if caught else 1
        print(f"{c}: tb/aecp_notify fails {', '.join(names) if names else 'NOTHING'} [{builds}];"
              f" tb/pp_top {pp}{(' first fails: ' + ' | '.join(pp_fail)) if pp_fail else ''}")
    print(f"controls failing a named committed check: {len(sys.argv) - 2 - uncaught} of {len(sys.argv) - 2}")
    return 1 if uncaught else 0


if __name__ == "__main__":
    sys.exit(main())

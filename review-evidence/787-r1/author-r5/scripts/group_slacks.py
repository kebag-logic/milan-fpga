"""group_slacks.py <label=run-dir>...: per routed run, the worst setup slack of each intra-clock path group over the two
slow signoff corners, read from the Intra Clock Table of `*_signoff_Slow_0C_timing.rpt` and `*_Slow_85C_timing.rpt`
(WNS per clock), so the deciding group and the distance of every other group from it are visible. Host paths are not
printed."""
import re
import sys
from pathlib import Path

for arg in sys.argv[1:]:
    label, run = arg.split("=", 1)
    worst = {}
    for corner in ("Slow_0C", "Slow_85C"):
        text = sorted(Path(run).glob(f"*_signoff_{corner}_timing.rpt"))[0].read_text(errors="replace")
        table = text.split("Intra Clock Table", 1)[1].split("Inter Clock Table", 1)[0]
        for line in table.splitlines():
            m = re.match(r"^\s*(\S+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(\d+)\s+(\d+)\s+(-?\d+\.\d+|\s)", line)
            if m and m.group(1) not in ("Clock", "-----"):
                worst[m.group(1)] = min(worst.get(m.group(1), 99.0), float(m.group(2)))
    best = min(worst.values())
    print(f"== {label}: worst setup slack per clock over the slow corners (WNS, ns; distance from the run's worst)")
    for clock, slack in sorted(worst.items(), key=lambda kv: kv[1]):
        print(f"  {clock:32s} {slack:+.3f}  (+{slack - best:.3f})")

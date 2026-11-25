#!/usr/bin/env python3
"""Grade one CPU budget harness run: harness_grade.py RUN_LOG RESULTS_DIR.

Prints the run's own summary line, the longest work pass over every group log (`PASS <n> <a> <b> <cycles>`), the
worst MRPDU row of results/table.md (its measured and bound columns), the MISS rows, and the worst queued notice
commit the run log reports. Mirrors round 1's extractions.
"""
import re
import sys
from pathlib import Path

run, results = Path(sys.argv[1]), Path(sys.argv[2])
text = run.read_text(errors="replace")
summary = [l for l in text.splitlines() if "groups graded" in l]
print(run.name, "summary:", summary[-1] if summary else "MISSING")
longest = 0
for f in results.glob("*.log"):
    for m in re.finditer(r"^PASS \d+ \d+ \d+ (\d+)", f.read_text(errors="replace"), re.M):
        longest = max(longest, int(m.group(1)))
print(f"  longest pass {longest:,} cycles (THE SHARE 200,000)")
table = results / "table.md"
rows = table.read_text().splitlines() if table.exists() else []
probes, inside = [], False
for row in rows:
    if row.startswith("| Path | Probe |"):
        inside = True
        continue
    if inside and not row.startswith("|"):
        inside = False
    cells = [c.strip() for c in row.split("|")]
    if inside and len(cells) > 8 and not row.startswith("|---"):
        try:
            probes.append({"path": cells[1], "probe": cells[2], "ms": float(cells[4]), "budget": cells[5],
                           "ceiling": cells[6], "verdict": cells[7]})
        except ValueError:
            pass
mrpdu = [r for r in probes if "MRPDU" in r["path"]]
if mrpdu:
    worst = max(mrpdu, key=lambda r: r["ms"])
    print(f"  MRPDU probes {len(mrpdu)}; worst {worst['ms']} ms, budget {worst['budget']} ms, "
          f"ceiling {worst['ceiling']} ms, {worst['verdict']} ({worst['probe']})")
for r in mrpdu:
    if "leaveall" in (r["path"] + r["probe"]).lower():
        print(f"  own-LeaveAll MRPDU probe {r['probe']}: {r['ms']} ms, budget {r['budget']} ms, {r['verdict']}")
misses = [r for r in probes if r["verdict"].upper().startswith("MISS")]
print(f"  probes {len(probes)}; MISS {len(misses)}")
for r in misses:
    print(f"    MISS {r['probe']}: {r['ms']} ms, budget {r['budget']}, ceiling {r['ceiling']} ({r['path'][:70]})")
notices = [float(m.group(1)) for m in re.finditer(r"committed ([0-9.]+) ms after its port's answer", text)]
if notices:
    print(f"  notice commits {len(notices)}; worst {max(notices)} ms")
queued = [float(m.group(1)) for m in re.finditer(r"last queued notice[^\n]*?([0-9]+\.[0-9]+) ms", text)]
if queued:
    print(f"  last queued notice worst {max(queued)} ms")

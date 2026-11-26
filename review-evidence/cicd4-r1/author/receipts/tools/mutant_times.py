"""Per-mutant hosted seconds from a serial campaign log, and the interleaved deal's leg sums."""
import re, sys, datetime
from pathlib import Path
log, legs = Path(sys.argv[1]), int(sys.argv[2])
pat = re.compile(r"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d+)Z (\[(?:ok|ESCAPED)\] (?:mutant|defect) (\S+).*|toolchain: .*|tsn-c-stack at .*)")
prev, rows, start = None, [], None
for line in log.read_text(encoding="utf-8-sig").splitlines():
    m = pat.search(line)
    if not m:
        continue
    t = datetime.datetime.fromisoformat(m.group(1)[:26])
    if m.group(3) is None:
        prev = t if prev is None else prev
        start = start or t
        if m.group(2).startswith("tsn-c-stack"):
            prev = t
        continue
    rows.append((m.group(3), (t - prev).total_seconds()))
    prev = t
total = sum(s for _, s in rows)
print(f"{len(rows)} items, {total:.0f} s after setup; first {rows[0][0]} {rows[0][1]:.0f} s")
for leg in range(legs):
    part = rows[leg::legs]
    print(f"leg {leg}/{legs}: {len(part)} items {sum(s for _, s in part):.0f} s, first {part[0][1]:.0f} s")
top = sorted(rows, key=lambda r: -r[1])[:6]
print("slowest:", ", ".join(f"{n} {s:.0f}" for n, s in top))

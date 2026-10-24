"""Hosted shard windows from `gh run view --log` worker logs (read-only receipt)."""
import re, sys
from datetime import datetime
LINE = re.compile(r"^[^\t]*\t[^\t]*\t\ufeff?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?)Z (.*)$")
def t(s):
    whole, _, frac = s.partition(".")
    return datetime.strptime(whole, "%Y-%m-%dT%H:%M:%S").timestamp() + float("0." + (frac or "0"))
for path in sys.argv[1:]:
    rows = [(t(m[1]), m[2]) for l in open(path, encoding="utf-8") if (m := LINE.match(l))]
    first, last = rows[0][0], rows[-1][0]
    start = next(ts for ts, msg in rows if msg.startswith("shard: "))
    print(f"== {path.rsplit('/',1)[-1]}")
    print(f"  job log first line -> last line: {last-first:.1f} s")
    print(f"  setup (first line -> shard line): {start-first:.1f} s")
    prev = start
    for ts, msg in rows:
        m = re.fullmatch(r"(PASS|FAIL|TIMEOUT) +(\S+).*", msg)
        if m and ts >= start:
            print(f"  {m[1]:8} {m[2]:16} window {ts-prev:8.1f} s")
            prev = ts
        if msg.startswith("suites: "):
            print(f"  tail (last verdict -> last line): {last-prev:.1f} s")

#!/usr/bin/env python3
"""Independent re-derivation of per-suite windows from `gh run view --log`
worker logs (no import of the candidate selector).  Usage:
  independent_measure.py LOG... > out.json
For each log: shard line, every result line (PASS/FAIL/TIMEOUT), window from
the previous result (or shard line) to this one in exact decimal seconds, the
log span, and span minus the windows (the overhead)."""
import json, re, sys
from decimal import Decimal, ROUND_CEILING
from datetime import datetime, timezone

STAMP = re.compile(r"^[^\t]*\t[^\t]*\t\ufeff?(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?)Z (.*)$")

def secs(stamp):
    whole, _, frac = stamp.partition(".")
    t = datetime.strptime(whole, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    return Decimal(int(t.timestamp())) + (Decimal("0." + frac) if frac else 0)

out = {}
for path in sys.argv[1:]:
    rows = []
    for line in open(path, encoding="utf-8"):
        m = STAMP.match(line.rstrip("\n"))
        if m:
            rows.append((secs(m.group(1)), m.group(2)))
    shard = next((r for r in rows if re.fullmatch(r"shard: \d+/\d+ +selected suites: \d+", r[1])), None)
    i = rows.index(shard)
    results, summary = [], None
    for t, msg in rows[i + 1:]:
        if summary is None and msg.startswith("suites: "):
            summary = (t, msg)
            break
        m = re.fullmatch(r"(PASS|FAIL|TIMEOUT) +(\S+).*", msg)
        if m:
            results.append((t, m.group(1), m.group(2)))
    prev, win = shard[0], {}
    for t, verdict, suite in results:
        win[suite] = {"verdict": verdict, "exact": str(t - prev),
                      "ceil": int((t - prev).to_integral_value(ROUND_CEILING))}
        prev = t
    span = rows[-1][0] - rows[0][0]
    out[path.rsplit("/", 1)[-1]] = {
        "shard": shard[1], "summary": summary and summary[1],
        "first": str(rows[0][0]), "last": str(rows[-1][0]),
        "span": str(span), "setup_before_shard": str(shard[0] - rows[0][0]),
        "after_last_result": str(rows[-1][0] - prev),
        "overhead_ceil": int((span - (prev - shard[0])).to_integral_value(ROUND_CEILING)),
        "windows": win}
json.dump(out, sys.stdout, indent=1, sort_keys=True)

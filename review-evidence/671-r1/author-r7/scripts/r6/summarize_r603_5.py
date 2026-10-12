"""Summarise R603-5 probe_comparison.py's comparison.json: per shape and
variant, the standing findings and how many carry the trailer class's own
words, a lost change or lost other records.
Usage: summarize_r603_5.py COMPARISON.JSON"""
import json
import sys
from pathlib import Path

for row in json.loads(Path(sys.argv[1]).read_text()):
    standing = row["standing_findings"]
    if standing is None:
        continue
    named = sum("which differ only in their trailer" in f for f in standing)
    generic = sum("on reads that returned different bytes" in f for f in standing)
    lost = sum("was lost on the clean reboot" in f for f in standing)
    others = sum("did not survive" in f for f in standing)
    print(f"{row['shape']} {row['variant']}: standing findings {len(standing)}, naming the trailer class {named}, "
          f"'on reads that returned different bytes' {generic}, change lost {lost}, other records lost {others}")
    print(f"  first: {standing[0][:240]}")

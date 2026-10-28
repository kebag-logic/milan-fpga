"""Map each round-3 check to the controls whose verdict printed it as failed,
from the mutation arm's own log. usage: coverage.py <04b-log> <out.md>"""
import re
import sys
from pathlib import Path

NEW = [
    "p1 255 #89 gmPresent: a priority1 255 grandmaster's usable Sync raises sync-ok",
    "p1 255 #89 gmPresent: when its Sync stops, sync-ok clears within syncReceiptTimeout and the peer stays elected",
    "#84 takeover: the queued receipt timeout commits after it",
]
lines = Path(sys.argv[1]).read_text().splitlines()
fails, hits, verdicts = [], {n: [] for n in NEW}, []
for line in lines:
    if line.startswith("FAIL "):
        fails.append(line[5:])
        continue
    m = re.match(r"\[(PASS|FAIL)\] (?:mutant caught: (.*?) - breaks|mutant SURVIVED: (.*?)\. |mutant '(.*?)' |mutation '(.*?)')", line)
    if m:
        name = next(g for g in m.groups()[1:] if g)
        verdicts.append((name, m.group(1)))
        for n in NEW:
            if any(f.startswith(n) for f in fails):
                hits[n].append(name)
        fails = []
out = ["# Round-3 check coverage", "", "Generated from the mutation arm's log: each named check, and every control",
       "whose verdict printed that check as failed.", "", "| Check | Controls that fail it |", "|---|---|"]
for n in NEW:
    out.append(f"| {n} | {'<br>'.join(hits[n]) or '**none**'} |")
caught = sum(v == 'PASS' for _, v in verdicts)
out += ["", f"Controls in the log: {len(verdicts)}; caught: {caught}."]
Path(sys.argv[2]).write_text("\n".join(out) + "\n")
print("\n".join(out))

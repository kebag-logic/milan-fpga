"""Map each round-2 check to the controls whose verdict printed it as failed,
from the mutation arm's own log. usage: coverage.py <04b-log> <out.md>"""
import re
import sys
from pathlib import Path

NEW = [
    "#89 takeover: the queued receipt timeout leaves the port aged",
    "#89 a lone pair heard as master: a later Announce elects nothing",
    "#89 a lone pair heard as master: an Announce inside its watch elects the grandmaster",
    "#89 Announce lapse: a sync receipt timeout after mastership ages the next Announce",
    "#89 parked Sync: a Follow_Up 200 ms after it pairs with nothing",
    "#89 parked Sync: a Follow_Up 60 ms after it, after the takeover, is heard",
    "p1 255 #89 gmPresent: a priority1 1 Announce on the aged port elects nothing",
    "p1 255 #89 gmPresent: the aged port elects a priority1 255 grandmaster",
    "p1 255 #89 gmPresent: a priority1 255 grandmaster without Sync stays elected",
    "p1 255 #89 gmPresent: a priority1 1 Announce on the aged port makes this plane master",
    "#82 Pdelay loss: Announces from the incapable port elect nothing",
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
out = ["# Round-2 check coverage", "", "Generated from the mutation arm's log: each named check, and every control",
       "whose verdict printed that check as failed.", "", "| Check | Controls that fail it |", "|---|---|"]
for n in NEW:
    out.append(f"| {n} | {'<br>'.join(hits[n]) or '**none**'} |")
caught = sum(v == 'PASS' for _, v in verdicts)
out += ["", f"Controls in the log: {len(verdicts)}; caught: {caught}."]
Path(sys.argv[2]).write_text("\n".join(out) + "\n")
print("\n".join(out))

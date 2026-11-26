"""Compare the union of a campaign's leg logs with the hosted serial run's verdict lines.

A verdict is a line starting "[ok]" or "[ESCAPED]" with the line after it when that is a "    first:" line.
The serial lines come from the reference job log; the legs' from their timestamped local logs."""
import collections, re, sys
from pathlib import Path
ref, legs = Path(sys.argv[1]), [Path(p) for p in sys.argv[2:]]
def verdicts(lines):
    out = []
    for i, x in enumerate(lines):
        if re.match(r"\[(ok|ESCAPED|BAD)\] ", x):
            nxt = lines[i + 1] if i + 1 < len(lines) and lines[i + 1].startswith("    first:") else ""
            out.append(x + ("\n" + nxt if nxt else ""))
    return out
serial = []
for line in ref.read_text(encoding="utf-8-sig").splitlines():
    m = re.match(r"﻿?\d{4}-\d\d-\d\dT[\d:.]+Z (.*)$", line.split("\t", 2)[-1])
    # stderr is unbuffered on the runner and lands between a verdict and its detail; the legs' stderr is in .time
    if m and not m.group(1).startswith("[endstation_builder] WARNING"):
        serial.append(m.group(1))
s = verdicts(serial)
u = [v for leg in legs for v in verdicts([x.split(" ", 1)[1] if " " in x else "" for x in leg.read_text().splitlines()])]
cs, cu = collections.Counter(s), collections.Counter(u)
print(f"serial verdicts {len(s)}, legs' verdicts {len(u)} ({', '.join(str(len(verdicts([x.split(' ', 1)[1] if ' ' in x else '' for x in l.read_text().splitlines()]))) for l in legs)})")
print("identical multisets:", cs == cu, "| bad in legs:", sum(v.startswith(("[ESCAPED]", "[BAD]")) for v in u))
for label, d in (("only serial", cs - cu), ("only legs", cu - cs)):
    for v in list(d.elements())[:3]:
        print(f"  {label}: {v[:220]}")
summ = [x for x in serial if re.match(r"(mutants|defects|aecp|srp)\S*: |test_ctrl_firmware: ", x)]
print("serial summaries:", summ[-4:])
for leg in legs:
    body = [x.split(" ", 1)[1] for x in leg.read_text().splitlines() if " " in x]
    print(f"{leg.name}:", [x for x in body if re.match(r"(mutants|defects|aecp|srp)\S*: |test_ctrl_firmware: ", x)][-3:])

"""Compare the census legs' and judge's verdict lines with the hosted serial run's, line for line.

The serial run's lines are its step's output, the runner timestamp removed. Lines carrying a duration differ by
design and are compared with the figure masked."""
import re, sys
from pathlib import Path
ref, local = Path(sys.argv[1]), Path(sys.argv[2])
lines = []
for line in ref.read_text(encoding="utf-8-sig").splitlines():
    part = line.split("\t", 2)[-1]
    m = re.match(r"﻿?\d{4}-\d\d-\d\dT[\d:.]+Z (.*)$", part)
    if m:
        lines.append(m.group(1))
start = next(i for i, x in enumerate(lines) if x.startswith("publication census: elaborating"))
end = next(i for i, x in enumerate(lines) if x.startswith("mutations: "))
serial = lines[start:end + 1]
mask = lambda x: re.sub(r"in \d+ s at --jobs \d+", "in N s at --jobs J", x)
def body(path):
    return [x.split(" ", 1)[1] if " " in x else "" for x in path.read_text().splitlines()]
check = body(local / "leg0.log")
check = check[next(i for i, x in enumerate(check) if x.startswith("publication census: elaborating")):]
union = (local / "union.log").read_text().splitlines()
cut = next(i for i, x in enumerate(serial) if x.startswith("publication census: ") and "shape(s) elaborated" in x)
s_check, s_self = serial[:cut + 1], serial[cut + 1:]
print("serial check lines", len(s_check), "leg 0 lines", len(check), "identical (durations masked):",
      [mask(x) for x in s_check] == [mask(x) for x in check])
s_arms = [x for x in s_self if not x.startswith("selftest: ")]
u_arms = [x for x in union if not x.startswith("selftest: ")]
hexmask = lambda x: re.sub(r"\$0x[0-9a-f]+:", "$0xADDR:", x)       # a Yosys cell name holds a heap address
print("serial self-test lines", len(s_arms), "judge lines", len(u_arms), "identical:", s_arms == u_arms,
      "identical with Yosys heap addresses masked:", [hexmask(x) for x in s_arms] == [hexmask(x) for x in u_arms],
      "lines differing only by address:", sum(a != b for a, b in zip(s_arms, u_arms)))
print("serial summary:", next(x for x in s_self if x.startswith("selftest: ")))
print("judge summary: ", next(x for x in union if x.startswith("selftest: ")))
for a, b in zip(s_arms, u_arms):
    if hexmask(a) != hexmask(b):
        print("first difference:\n  serial:", a[:200], "\n  judge: ", b[:200]); break

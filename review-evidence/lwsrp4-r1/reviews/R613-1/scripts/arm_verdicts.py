# SPDX-License-Identifier: Apache-2.0
"""Extract per-arm verdict lines from parent firmware harness logs and compare them."""
import re, sys
from pathlib import Path
def arms(path):
    out, arm = {}, None
    for line in Path(path).read_text().splitlines():
        m = re.match(r"^\[(ok|FAIL|skip\w*)\] arm (\S+)", line)
        if m:
            arm = m.group(2); out[arm] = [m.group(1)]
        elif arm and "verdict:" in line:
            out[arm].append(line.strip())
    return out
logs = {Path(p).stem: arms(p) for p in sys.argv[1:]}
names = sorted(set().union(*logs.values()))
srp = [n for n in names if n == "lwsrp" or n.startswith("srp")]
for k, v in logs.items():
    print(k, "arms:", len(v), "srp-set:", sum(1 for n in srp if n in v))
first = next(iter(logs.values()))
diff = [n for n in names if len({str(l.get(n)) for l in logs.values()}) != 1]
print("arms with differing verdict lines:", diff or "none")
cases = {k: sum(int(m.group(1)) for n in srp for s in v.get(n, [])[1:] for m in [re.search(r"\((\d+) tests", s)] if m) for k, v in logs.items()}
print("srp-set test cases:", cases)

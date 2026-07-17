# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Line-coverage gate over verilator_coverage --annotate output.
# A coverage-point line starts with a 6-digit hit count (covered) or with
# '%' (below --annotate-min = uncovered). Gates the KL_ modules at ARGV[2] %.
import re
import sys
from pathlib import Path

ann_dir, threshold = Path(sys.argv[1]), float(sys.argv[2])
gated = ("KL_avtp_rx_monitor.sv", "KL_aaf_rx_depacketizer.sv")
fail = False
seen = set()
for f in sorted(ann_dir.glob("*.sv")) + sorted(ann_dir.glob("*.v")):
    cov = unc = 0
    for line in f.read_text(errors="replace").splitlines():
        if re.match(r"^%\d{6}", line):
            unc += 1
        elif re.match(r"^\s*\d{6}", line):
            cov += 1
    total = cov + unc
    if total == 0:
        continue
    pct = 100.0 * cov / total
    gate = f.name in gated
    if gate:
        seen.add(f.name)
    verdict = ""
    if gate:
        verdict = "PASS" if pct >= threshold else "FAIL <<<"
        if pct < threshold:
            fail = True
    print(f"  {f.name:32s} line {pct:5.1f}% ({cov}/{total}) {verdict}")
for g in gated:
    if g not in seen:
        print(f"  {g:32s} MISSING from coverage data FAIL <<<")
        fail = True
print(f"coverage gate ({threshold:.0f}% on KL_ modules): "
      + ("FAIL" if fail else "PASS"))
sys.exit(1 if fail else 0)

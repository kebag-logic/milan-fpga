#!/usr/bin/env python3
"""R363-3: removal mutants for the checks behind the boundary survivors.
Usage: removal_probe.py <repo>. KILLED = unchanged self-test rc 1 with a named FAIL/ERROR."""
import re, subprocess, sys, tempfile
from pathlib import Path
src = (Path(sys.argv[1]) / "tb/tools/torture_campaign.py").read_text(encoding="utf-8")
MUT = (
    ("R1 PDU timestamp-order check removed",
     '                or current["timestamp_s"] < previous["timestamp_s"]):',
     '                or False):'),
    ("R2 capture start<end term removed",
     "if (capture_start_s >= capture_end_s or capture_start_s > required_start_s",
     "if (False or capture_start_s > required_start_s"),
    ("R3 negative PDU index check removed",
     ' or pdu["pdu_index"] < 0\n', '\n'),
    ("R4 history zero-length guard removed",
     "if clear_s <= start_s or (intervals and start_s <= intervals[-1][1]):",
     "if (intervals and start_s <= intervals[-1][1]):"),
)
for name, old, new in MUT:
    assert src.count(old) == 1, name
    with tempfile.TemporaryDirectory(prefix="r363rm-") as d:
        p = Path(d) / "torture_campaign.py"; p.write_text(src.replace(old, new), encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", str(p), "--self-test"], capture_output=True, text=True, timeout=600)
        failed = sorted(set(re.findall(r"^(?:FAIL|ERROR): (test_\w+)", r.stderr, re.M)))
        print(("KILLED" if r.returncode and failed else "SURVIVED" if r.returncode == 0 else f"CRASH rc={r.returncode}"), name, failed)

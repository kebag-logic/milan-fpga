#!/usr/bin/env python3
"""Reviewer's own mutants of gate 1h's reader on a disposable copy; each must turn the gate red.

usage: own_mutants.py <copy root>
"""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); path = root / "sw/builder/test_builder.py"; shipped = path.read_text()
MUTANTS = [
 ("the build's defines dropped", '*(f"-D{define}" for define in record["define"]),', ''),
 ("the build's include directories dropped", '*(arg for incdir in record["incdir"] for arg in ("-I", incdir)),', ''),
 ("the shipped datapath read, not the planted text", 'str(planted) if Path(src).resolve() == datapath else src', 'src'),
 ("the earlier macro's guard read as the datapath's own",
  'modules = re.findall(r"^\\s*module\\s+milan_datapath\\b.*?^\\s*endmodule\\b",', 'modules = re.findall(r"^\\s*module\\s+\\w+\\b.*?^\\s*endmodule\\b",'),
]
wrong = 0
try:
    for name, old, new in MUTANTS:
        assert shipped.count(old) == 1, old
        path.write_text(shipped.replace(old, new))
        out = subprocess.run([sys.executable, "sw/builder/test_builder.py", "--gates",
                              "test_gptp_datapath_carries_the_launch_shape"],
                             cwd=root, capture_output=True, text=True)
        why = next((l for l in (out.stdout + out.stderr).splitlines() if l.startswith("AssertionError")), "")
        wrong += out.returncode == 0
        print(f"{'ok ' if out.returncode else 'BAD'} rc={out.returncode} {name}: {why[:170]}", flush=True)
finally:
    path.write_text(shipped)
print(f"mutants: {len(MUTANTS)} not red: {wrong}")
sys.exit(1 if wrong else 0)

#!/usr/bin/env python3
"""Mutate gate 1h's reader on a disposable clone: each mutant must turn the gate red, by name.

usage: gate1h_reader_mutants.py <clone>
"""
import subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]); path = root / "sw/builder/test_builder.py"; shipped = path.read_text()
MUTANTS = [
 ("the datapath alone, no earlier source", "             *sources],", "             str(planted)],"),
 ("the datapath first, not in its place", "             *sources],",
  "             str(planted), *(s for s in sources if s != str(planted))],"),
 ("the whole output, not the datapath's module", 'return modules[0], ""', 'return read.stdout, ""'),
 ("the first of many datapath modules", "if len(modules) != 1:", "if not modules:"),
 ("a macro no earlier source defines", 'DATAPATH_EARLIER_MACRO = "ETHERNET_PACKET_PKG_SV"', 'DATAPATH_EARLIER_MACRO = "NO_SOURCE_DEFINES_THIS"'),
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

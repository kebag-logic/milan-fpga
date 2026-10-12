"""Scratch (round 7): the firmware gate's verdict lines from a fullcap log: every [ok]/[ESCAPED]/[FAIL] line, the
mutants line and the gate's verdict, between the RV32 self-test's rc line and the firmware gate's.

usage: verdicts.py <fullcap log> <out>
"""
import re
import sys
from pathlib import Path

lines = Path(sys.argv[1]).read_text(encoding="utf-8", errors="replace").splitlines()
start = next(i for i, ln in enumerate(lines) if ln.startswith("rc=") and "fw_rv32_selftest.py" in ln)
end = next(i for i, ln in enumerate(lines) if ln.startswith("rc=") and "test_ctrl_firmware.py" in ln)
keep = [ln for ln in lines[start + 1:end]
        if re.match(r"^\[(ok|ESCAPED|FAIL)\]", ln) or ln.startswith(("mutants: ", "test_ctrl_firmware: "))]
Path(sys.argv[2]).write_text("".join(ln + "\n" for ln in keep), encoding="utf-8")
print(len(keep), sum(ln.startswith("[ok]") for ln in keep))

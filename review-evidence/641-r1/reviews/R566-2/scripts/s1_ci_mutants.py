#!/usr/bin/env python3
"""S1 probe: the CI contract must refuse a removed or neutralised guard self-test step.

Run from a disposable copy of the reviewed tree. Each mutant edits
.github/workflows/rtl-fast.yml, runs `scripts/ci_events.py --check`, and the
file is restored byte-for-byte afterwards.
"""
import pathlib
import subprocess
import sys

WF = pathlib.Path(".github/workflows/rtl-fast.yml")
ORIG = WF.read_bytes()
STEP = ("      - name: Prove both synthesis flows refuse active elaboration guards\n"
        "        run: python3 syn/yosys/guard_selftest.py\n\n")
RUN = "        run: python3 syn/yosys/guard_selftest.py\n"
text = ORIG.decode()
assert text.count(STEP) == 1, "step not found exactly once"
MUTANTS = {
    "step removed": text.replace(STEP, ""),
    "step neutralised with || true": text.replace(RUN, RUN.rstrip("\n") + " || true\n"),
    "step continue-on-error": text.replace(RUN, RUN + "        continue-on-error: true\n"),
    "step moved to a different job (firmware-unit tail)": None,
}
failures = 0
try:
    for name, body in MUTANTS.items():
        if body is None:
            continue
        WF.write_text(body)
        p = subprocess.run([sys.executable, "scripts/ci_events.py", "--check"],
                           capture_output=True, text=True, check=False)
        refused = p.returncode != 0
        failures += not refused
        last = (p.stdout + p.stderr).strip().splitlines()
        hint = next((l for l in last if "guard" in l or "yosys-elaboration" in l), last[-1] if last else "")
        print(f"{'REFUSED' if refused else 'ACCEPTED'} rc={p.returncode} {name}: {hint[:180]}")
finally:
    WF.write_bytes(ORIG)
print("restored" if WF.read_bytes() == ORIG else "RESTORE FAILED")
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Composition probes for scripts/check_baremetal_only.py on the candidate.

Run from a disposable copy of the candidate. Each probe removes ONE side's
file-pinned mask from the merged mask tables and requires `--check` to refuse
that side's file, proving the composed gate still reads both lanes' entries
and both lanes' files. The file is restored after every probe.
"""
import pathlib
import subprocess
import sys

GATE = pathlib.Path("scripts/check_baremetal_only.py")
PROBES = [
    ("predecessor-owned-process-mask",
     '    "scripts/owned_process.py": re.compile(r\'(?<=^PROC = Path\\(")/proc(?="\\)$)\'),\n',
     "scripts/owned_process.py"),
    ("predecessor-process-test-support-mask",
     '    "scripts/process_test_support.py": re.compile(r\'(?<=^PROC = Path\\(")/proc(?="\\)$)\'),\n',
     "scripts/process_test_support.py"),
    ("pr-installer-term-mask",
     '    "scripts/ci_rv32_sdk.py": re.compile(\n        SDK_IDENTITY_MASK + r\'|\\("Linux", "x86_64"\\)\'),\n',
     "scripts/ci_rv32_sdk.py"),
    ("pr-fixture-term-mask",
     '    "scripts/ci_rv32_sdk_selftest.py": re.compile(SDK_IDENTITY_MASK),\n',
     "scripts/ci_rv32_sdk_selftest.py"),
]


def main():
    pristine = GATE.read_bytes()
    failures = 0
    try:
        for name, anchor, victim in PROBES:
            text = pristine.decode()
            if text.count(anchor) != 1:
                print(f"{name}: ANCHOR-NOT-UNIQUE ({text.count(anchor)})")
                failures += 1
                continue
            GATE.write_text(text.replace(anchor, "", 1))
            proc = subprocess.run([sys.executable, "-B", str(GATE), "--check"],
                                  capture_output=True, text=True)
            out = proc.stdout + proc.stderr
            hits = [l for l in out.splitlines() if victim in l]
            killed = proc.returncode != 0 and bool(hits)
            print(f"{name}: exit={proc.returncode} "
                  f"{'KILLED' if killed else 'SURVIVED'} ({len(hits)} finding line(s) on {victim})")
            for l in hits[:3]:
                print("    " + l.strip())
            failures += 0 if killed else 1
            GATE.write_bytes(pristine)
    finally:
        GATE.write_bytes(pristine)
    print("PROBES:", "all KILLED" if failures == 0 else f"{failures} not killed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

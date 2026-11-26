#!/usr/bin/env python3
"""Focused binding/verify controls, using temporary storage only in SCRATCH.

Usage: probe_grade.py SOURCE SCRATCH
"""
import contextlib
from pathlib import Path
import sys
import tempfile

source, scratch = map(lambda s: Path(s).resolve(), sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
tempfile.tempdir = str(scratch)
sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
sys.path.insert(0, str(source / 'scripts'))
import selftest
import selftest_bind
import selftest_mutants_bind
import grade

checks = selftest_bind.bind_checks(selftest)
failed = [name for name, ok, detail in checks if not ok]
print(f'Focused binding/verify controls: {len(checks)} checks, {len(failed)} failures')
assert not failed, failed
for name, factory in selftest_mutants_bind.MUTANTS.items():
    with contextlib.ExitStack() as stack:
        for patch in factory():
            stack.enter_context(patch)
        try:
            failures = [n for n, ok, detail in selftest_bind.bind_checks(selftest) if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failures = [type(error).__name__]
    assert failures, name
    print(f'CAUGHT {name}')
print(f'PASS {len(selftest_mutants_bind.MUTANTS)} planted defects caught; no source mutation')

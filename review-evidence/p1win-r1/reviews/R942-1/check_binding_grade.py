#!/usr/bin/env python3
"""Focused binding grader controls, its 26 mutations, and independent byte-coverage probes."""
import contextlib
import struct
import sys
import zlib
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import selftest as support
import selftest_bind as checks
import selftest_mutants_bind as mutants
import grade
import save_burst

failures = 0
normal = checks.bind_checks(support)
for name, ok, detail in normal:
    print('PASS' if ok else 'FAIL', name, '' if ok else detail)
    failures += not ok
print('BASELINE', len(normal), 'checks', failures, 'failures')
for name, patches in mutants.MUTANTS.items():
    with contextlib.ExitStack() as stack:
        for patch in patches():
            stack.enter_context(patch)
        try:
            failed = [label for label, ok, _ in checks.bind_checks(support) if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [type(error).__name__ + ': ' + str(error)]
    print('CAUGHT' if failed else 'ESCAPED', name, failed[:1])
    failures += not bool(failed)
print('MUTATIONS', len(mutants.MUTANTS))

size, base = 128, 0xe40000
blob = struct.pack('<10I', 0x334a4c4b, 0x00030000, 7, 0, size, 0, 0, 0, 0, 3)
blob = blob.ljust(size - 4, b'\xff')
blob += struct.pack('<I', zlib.crc32(blob))
cases = {
    'no post-program reads': ([], None),
    'only first four bytes after program': ([(40, 50, base, 4)], None),
    'same half twice': ([(40, 50, base, 64), (60, 70, base, 64)], None),
    'overlap leaves final byte missing': ([(40, 50, base, 64), (60, 70, base + 63, 64)], None),
    'two halves complete': ([(40, 50, base, 64), (60, 70, base + 64, 64)], 70),
    'complete in reverse address order': ([(40, 50, base + 64, 64), (60, 70, base, 64)], 70),
    'reads straddle programming': ([(20, 50, base, 128)], 'REFUSED'),
}
for name, (reads, expected) in cases.items():
    log = grade.Log(100000000, 100000000,
                    flash_ops=[(10, grade.FLASH_ERASE, base, 0), (30, grade.FLASH_PROGRAM, base, size)],
                    programmed=[(30, base, blob)], reads=[(15, 19, base, size), *reads])
    try:
        actual = save_burst.saves(log, size)[0]['durable']
    except grade.Refusal:
        actual = 'REFUSED'
    ok = actual == expected
    print('PASS' if ok else 'FAIL', name, 'expected', expected, 'observed', actual)
    failures += not ok
print('RESULT', 'PASS' if not failures else 'FAIL', 'failures', failures)
sys.exit(bool(failures))

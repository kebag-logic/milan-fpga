#!/usr/bin/env python3
"""Probe the census extractor's part limit at its shipped value, and whether its self-test binds the reader's limit.

1. At the shipped PART_LIMIT a part of exactly that size, alone and as a first part, is written by parts() and read
   back under READ_LIMIT (the value case() passes); the same part is refused at a limit of PART_LIMIT (the round-3
   defect's value), and an overlong line is refused without an unbounded write.
2. With READ_LIMIT set back to PART_LIMIT in the loaded module (the round-3 defect re-planted), --selftest still passes.

usage: python3 -B probe_extract_limit.py SOURCE SCRATCH
"""
import sys
import tempfile
from pathlib import Path


def main(source: Path, scratch: Path) -> int:
    sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
    import census_extract as ce
    import receipt_regrade as rr
    limit = ce.PART_LIMIT
    line = b'x' * 99 + b'\n'
    exact = line * (limit // 100)
    assert len(exact) == limit
    ok = True
    with tempfile.TemporaryDirectory(dir=scratch) as tmp:
        work = Path(tmp)
        for name, data, sizes in (('exact', exact, [limit]), ('first-exact', exact + b'tail\n', [limit, 5])):
            record = ce.parts(work / name, 'observations.log', data)
            got = [p['bytes'] for p in record['parts']]
            back = rr.read_parts(work / name, record, ce.READ_LIMIT) == data
            try:
                rr.read_parts(work / name, record, ce.PART_LIMIT)
                refused = False
            except ValueError as error:
                refused = True
                reason = str(error)
            print(f'{name}: parts {got} (expected {sizes}); reads back under READ_LIMIT={ce.READ_LIMIT}: {back}; '
                  f'refused under the exclusive limit {ce.PART_LIMIT}: {refused}' + (f' ({reason})' if refused else ''))
            ok = ok and got == sizes and back and refused
        for name, data in (('overlong', b'x' * limit + b'\n'), ('overlong-later', exact + b'y' * limit + b'\n')):
            try:
                ce.parts(work / name, 'observations.log', data)
                print(f'{name}: NOT refused')
                ok = False
            except ValueError as error:
                emitted = sorted(p.name for p in (work / name).iterdir())
                print(f'{name}: refused ({error}); files left: {emitted}')
                ok = ok and len(emitted) <= 1
    print('SHIPPED LIMIT PAIRING:', 'PASS' if ok else 'FAIL')
    print('--- mutant: READ_LIMIT = PART_LIMIT (the round-3 defect) in the loaded module, then --selftest')
    shipped = ce.READ_LIMIT
    ce.READ_LIMIT = ce.PART_LIMIT
    status = ce.selftest()
    ce.READ_LIMIT = shipped
    print(f'MUTANT read-limit-exclusive: selftest exit {status}:', 'SURVIVES (not detected)' if status == 0 else 'KILLED')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))

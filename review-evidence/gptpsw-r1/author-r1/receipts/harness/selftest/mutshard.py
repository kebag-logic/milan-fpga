"""mutshard.py <k> <n>: the harness self-test's mutants k, k+n, ... (selftest.MUTANTS order), each graded by the same
checks() under mutated(name) that selftest.main runs; prints 'MUTANT caught|ESCAPED: <name>'. Scratch, not committed."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path('tb/verilator/ctrl_service_budget').resolve()))
import selftest, selftest_mutants
k, n = int(sys.argv[1]), int(sys.argv[2])
for i, name in enumerate(selftest_mutants.MUTANTS):
    if i % n != k:
        continue
    with selftest.mutated(name):
        try:
            failed = [c for c, ok, _ in selftest.checks() if not ok]
        except (selftest.grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as exc:  # as main
            failed = [f'raised {type(exc).__name__}']
    print(f"MUTANT {'caught' if failed else 'ESCAPED'}: {name}" + (f": {failed[0]}" if failed else ''), flush=True)

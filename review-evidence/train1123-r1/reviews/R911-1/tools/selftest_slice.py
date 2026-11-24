"""Run a slice of run.py --self-test's mutants (selftest_mutants.MUTANTS[start:end]) exactly as selftest.main does:
each mutant applied in memory through selftest.mutated, every check run, the mutant caught when one check fails.

usage: python3 -I -B selftest_slice.py <repo-root> <start> <end>
Exit 0 = every mutant in the slice caught; 1 = one escaped.
"""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import selftest  # noqa: E402
import selftest_mutants  # noqa: E402

start, end = int(sys.argv[2]), int(sys.argv[3])
names = list(selftest_mutants.MUTANTS)[start:end]
escaped = 0
for name in names:
    with selftest.mutated(name):
        try:
            failed = [(n, d) for n, ok, d in selftest.checks() if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [(f'refused: {error}', '')]
    if failed:
        print(f'MUTANT caught: {name}: {failed[0][0]}', flush=True)
    else:
        print(f'MUTANT ESCAPED: {name}', flush=True)
        escaped += 1
print(f'slice {start}:{end} of {len(selftest_mutants.MUTANTS)}: {len(names)} mutants, {escaped} escaped')
sys.exit(1 if escaped else 0)

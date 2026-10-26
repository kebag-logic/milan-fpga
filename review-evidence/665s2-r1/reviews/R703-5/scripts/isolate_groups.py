"""For named mutants, run every self-test check group separately, so a refusal in one group
cannot mask the others, and print which named checks fail in each.
Usage: python3 -I isolate_groups.py <tree>/tb/verilator/ctrl_service_budget [mutant-substring ...]"""
import sys, io, contextlib
sys.path.insert(0, sys.argv[1])
sys.dont_write_bytecode = True
import selftest, selftest_mutants, grade
groups = [n for n in ('fixture_checks', 'marker_checks', 'notify_checks', 'composition_checks', 'maximum_checks',
                      'window_checks', 'load_checks', 'path_checks', 'fanout_checks', 'run_checks', 'reuse_checks')]
subs = sys.argv[2:]
for name in selftest_mutants.MUTANTS:
    if subs and not any(s in name for s in subs):
        continue
    print('MUTANT', name)
    for g in groups:
        with selftest.mutated(name):
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    res = getattr(selftest, g)()
                fails = [n for n, ok, _ in res if not ok]
                print(f'  {g}: {len(res)} checks, failed: {fails}')
            except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as e:
                print(f'  {g}: RAISED {type(e).__name__}: {str(e)[:140]}')

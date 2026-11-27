"""Run tb/verilator/ctrl_service_budget/run.py --self-test's work in parallel, with its own verdict rule:
model_counts.main(), selftest.checks() unmutated (each must pass), then every selftest_mutants.MUTANTS entry
(each must make some check fail or refuse). Usage: python3 -I budget_selftest_parallel.py <checkout> <jobs>."""
import multiprocessing as mp
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
HERE = ROOT / 'tb/verilator/ctrl_service_budget'


def setup():
    sys.path.insert(0, str(HERE))
    import os
    os.chdir(HERE)


def base(_):
    setup()
    import contextlib, io, model_counts, selftest
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        mc = model_counts.main()
        res = [(n, ok, d[:300] if not ok else '') for n, ok, d in selftest.checks()]
    return mc, res, buf.getvalue()


def mutant(name):
    setup()
    import contextlib, io, grade, selftest
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), selftest.mutated(name):
        try:
            failed = [(n, d) for n, ok, d in selftest.checks() if not ok]
        except (grade.Refusal, KeyError, ValueError, IndexError, TypeError, RuntimeError) as error:
            failed = [(f'refused: {error}', '')]
    return name, (failed[0][0][:200] if failed else None)


if __name__ == '__main__':
    jobs = int(sys.argv[2])
    setup()
    import selftest_mutants
    names = list(selftest_mutants.MUTANTS)
    ctx = mp.get_context('fork')
    with ctx.Pool(jobs) as pool:
        b = pool.apply_async(base, (0,))
        results = pool.map(mutant, names, chunksize=1)
        mc, res, out = b.get()
    print(out.splitlines()[0] if out else '')
    print(out.splitlines()[1] if len(out.splitlines()) > 1 else '')
    failures = int(bool(mc))
    for n, ok, d in res:
        print(f'{"PASS" if ok else "FAIL"}: {n}' + ('' if ok else f': {d}'))
        failures += not ok
    for name, caught in results:
        print(f'MUTANT caught: {name}: {caught}' if caught else f'MUTANT ESCAPED: {name}')
        failures += caught is None
    print(f'model_counts rc={mc}; checks {len(res)}; mutants {len(names)}; self-test: {failures} failures')
    sys.exit(1 if failures else 0)

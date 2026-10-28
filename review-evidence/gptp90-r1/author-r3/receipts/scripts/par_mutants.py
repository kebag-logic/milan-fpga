"""Run selected controls of a lane's engine mutation arm in parallel, through
the arm's own stage/build/run_mutant functions. Not a gate: the recorded gate
is `make -C tb/verilator/engine mutants`.
usage: par_mutants.py <lane> <work> <jobs> [name-substring ...]"""
import contextlib, io, multiprocessing as mp, sys
from pathlib import Path
lane, work, jobs = Path(sys.argv[1]), Path(sys.argv[2]), int(sys.argv[3])
want = sys.argv[4:]
sys.path.insert(0, str(lane / "tb/verilator/engine")); sys.path.insert(0, str(lane / "tb/verilator"))
import mutants
CLEAN = None

def one(m):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = mutants.run_mutant(work, CLEAN, m)
    return m[0], ok, buf.getvalue()

if __name__ == "__main__":
    work.mkdir(parents=True, exist_ok=True)
    src = mutants.stage(work, "clean")
    CLEAN = mutants.build(src, work, "clean")
    assert CLEAN is not None and mutants.generate_image(src, work / "run_clean")
    sel = [m for m in mutants.MUTATIONS if not want or any(w in m[0] for w in want)]
    print("clean:", mutants.verdict(*mutants.run_harness(CLEAN, work / "run_clean")), "selected", len(sel), flush=True)
    with mp.get_context("fork").Pool(jobs) as pool:
        res = pool.map(one, sel, chunksize=1)
    bad = 0
    for name, ok, out in res:
        print(out, end="")
        bad += not ok
    print(f"\n{len(res)} controls: {len(res) - bad} caught, {bad} not")

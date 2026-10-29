"""Run chosen engine-arm mutants in parallel through the arm's own code.

usage: run_some_mutants.py <engine tb dir> <workers> <name> [<name> ...]
A name of "PORT" selects every entry of port_mutants.PORT_MUTATIONS.
Each mutant's printed verdict is collected and printed in order, with the
FAIL lines its run produced.
"""
import contextlib
import io
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

tb = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tb))
import mutants  # noqa: E402
import port_mutants  # noqa: E402

workers = int(sys.argv[2])
names = sys.argv[3:]
chosen = [m for m in mutants.MUTATIONS
          if m[0] in names or ("PORT" in names and m in port_mutants.PORT_MUTATIONS)]
work = Path(sys.argv[0]).resolve().parent.parent / "tmp" / "mut-explore"


def one(args):
    idx, mutation = args
    w = work / f"m{idx}"
    w.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        src = mutants.stage(w, "clean")
        exe = mutants.build(src, w, "clean")
        ok = exe is not None and mutants.run_mutant(w, exe, mutation)
    return mutation[0], ok, buf.getvalue()


if __name__ == "__main__":
    work.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for name, ok, out in ex.map(one, list(enumerate(chosen))):
            print(f"===== {name}: {'CAUGHT' if ok else 'NOT CAUGHT'}")
            print(out)

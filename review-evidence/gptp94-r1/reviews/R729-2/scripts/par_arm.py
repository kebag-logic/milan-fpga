#!/usr/bin/env python3
"""Run tb/verilator/engine/mutants.py's arm with a thread pool.

Imports the arm module of the tree given as argv[1] and calls its own
stage/build/generate_image/run_harness/run_mutant functions, unchanged, for
the clean control and every entry of MUTATIONS. Only the scheduling differs:
mutants run concurrently, builds are limited by a semaphore, and each
mutant's printed verdict is captured and printed in MUTATIONS order.

usage: par_arm.py <tree> <workers> <concurrent-builds>
"""
import contextlib
import io
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
workers = int(sys.argv[2])
nbuild = int(sys.argv[3])
eng = tree / "tb/verilator/engine"
sys.path.insert(0, str(eng))
import mutants as M  # noqa: E402

sem = threading.Semaphore(nbuild)
_orig_build = M.build


def _build(*a, **k):
    with sem:
        return _orig_build(*a, **k)


M.build = _build
# one compile job per build, so workers bound the job count
M.VFLAGS[M.VFLAGS.index("-j") + 1] = "1"

# per-thread stdout capture
_local = threading.local()
_real_stdout = sys.stdout


class _Router(io.TextIOBase):
    def write(self, s):
        buf = getattr(_local, "buf", None)
        return (buf if buf is not None else _real_stdout).write(s)


sys.stdout = _Router()


def one(work, clean_exe, mut):
    _local.buf = io.StringIO()
    try:
        ok = M.run_mutant(work, clean_exe, mut)
    except Exception as e:  # report, never hide
        print(f"[FAIL] mutation {mut[0]!r} raised {e!r}")
        ok = False
    return ok, _local.buf.getvalue()


def main():
    passes = fails = 0
    with tempfile.TemporaryDirectory(prefix="engine-mutants-",
                                     dir=sys.argv[4] if len(sys.argv) > 4
                                     else None) as td:
        work = Path(td)
        clean_src = M.stage(work, "clean")
        clean_run = work / "run_clean"
        clean_exe = M.build(clean_src, work, "clean")
        if clean_exe is None or not M.generate_image(clean_src, clean_run):
            _real_stdout.write("[FAIL] clean did not build\n")
            return 1
        ans = M.verdict(*M.run_harness(clean_exe, clean_run))
        if ans == "pass":
            passes += 1
            _real_stdout.write("[PASS] the unmutated engine still passes the harness\n")
        else:
            fails += 1
            _real_stdout.write(f"[FAIL] the unmutated engine does NOT pass ({ans})\n")
        _real_stdout.flush()
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(one, work, clean_exe, m) for m in M.MUTATIONS]
            for f in futs:
                ok, out = f.result()
                _real_stdout.write(out)
                _real_stdout.flush()
                if ok:
                    passes += 1
                else:
                    fails += 1
    total = passes + fails
    _real_stdout.write(f"\n{total} checks: {passes} PASS, {fails} FAIL\n")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

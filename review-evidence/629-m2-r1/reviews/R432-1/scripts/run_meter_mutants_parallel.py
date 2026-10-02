#!/usr/bin/env python3
"""Re-run tb/verilator/aaf_clock_meter/mutants.py's campaign in parallel.

Imports the suite's own MUTANTS table, mutate(), build() and run_case()
unchanged, so the kill criterion (build succeeds, harness exits 1, the NAMED
check is among the failures) is the suite's own. Only the scheduling differs:
N mutants at a time in separate processes, each in its own temporary
directory under --work.

usage: run_meter_mutants_parallel.py <tree>/tb/verilator/aaf_clock_meter \
           --work DIR [--jobs 8] [--only NAME ...]
env:   VERILATOR (the pinned 5.050 wrapper), VERILATOR_JOBS
"""
import argparse
import contextlib
import io
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

SUITE = None
WORK = None


def _init(suite: str, work: str) -> None:
    global SUITE, WORK
    SUITE, WORK = suite, work
    sys.path.insert(0, suite)


def one(t):
    import mutants as m  # the suite's own campaign module
    name, rtl, edits, target, failure = t
    buf = io.StringIO()
    with tempfile.TemporaryDirectory(dir=WORK, prefix=f"{name}-") as d, \
            contextlib.redirect_stdout(buf):
        src = m.mutate(m.RTL[rtl].read_text(), edits)
        if src is None:
            print(f"FAIL {name}: anchor not unique")
            ok = False
        else:
            exe = m.build(Path(d), name, rtl, src, target)
            ok = exe is not None and m.run_case(exe, name, target, failure)
    return name, ok, buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    suite = str(Path(a.suite).resolve())
    sys.path.insert(0, suite)
    import mutants as m
    todo = [t for t in m.MUTANTS if not a.only or t[0] in a.only]
    with ProcessPoolExecutor(a.jobs, initializer=_init,
                             initargs=(suite, a.work)) as ex:
        res = list(ex.map(one, todo))
    for name, ok, out in res:
        print(f"===== {name}: {'KILLED as named' if ok else 'NOT KILLED / ERROR'}")
        print(out.strip()[-1500:])
    bad = [n for n, ok, _ in res if not ok]
    print(f"SUMMARY: {len(res) - len(bad)}/{len(res)} killed by their named "
          f"check; escaped: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())

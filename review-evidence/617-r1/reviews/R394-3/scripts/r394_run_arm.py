#!/usr/bin/env python3
"""Run the committed capture_coherence mutation arm (mutants.py) in parallel.

Imports the suite's own mutants.py and calls its clean_control() and
grade_mutant() unchanged, one thread per leg control and per mutant, so each
verdict is the committed arm's own; only the schedule differs (the committed
driver runs them one after another, past this session's per-command limit).

  python3 r394_run_arm.py <suite-dir> [--jobs N]
"""

import argparse
import concurrent.futures as cf
import importlib.util
import sys
import tempfile
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("suite")
    ap.add_argument("--jobs", type=int, default=7)
    a = ap.parse_args()
    suite = Path(a.suite).resolve()
    spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
    m = importlib.util.module_from_spec(spec)
    sys.argv = [str(suite / "mutants.py")]
    spec.loader.exec_module(m)
    with tempfile.TemporaryDirectory(prefix="r394-arm-") as td:
        work = Path(td)
        tasks = [("control", leg, None, None) for leg in m.LEGS]
        tasks += [("mutant", leg, (name, edits), breaks) for leg, name, edits, breaks in m.MUTATIONS]

        def run(t):
            kind, leg, ne, breaks = t
            if kind == "control":
                return m.clean_control(leg, work)
            return m.grade_mutant(leg, work, ne[0], ne[1], breaks)

        with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
            results = list(ex.map(run, tasks))
    passes = sum(1 for r in results if r)
    print(f"\n{len(results)} checks: {passes} PASS, {len(results) - passes} FAIL")
    return 0 if passes == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())

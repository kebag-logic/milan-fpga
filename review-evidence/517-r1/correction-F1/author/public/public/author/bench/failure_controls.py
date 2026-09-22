#!/usr/bin/env python3
"""Run CLI-based runner tests against deliberate faulty runner copies.

Usage: python3 failure_controls.py LANE OUTPUT_DIRECTORY
Run under an external 120-second guard. An external timeout is UNKNOWN,
never a caught fault. Copies live outside the source lane. This script
does not run builds, containers, remote operations, or other suites.
"""
import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

MUTANTS = (
    ("no-exclusivity", "group_busy = any(leg.exclusive for leg in running)", "group_busy = False",
     "arm_shared_group_is_exclusive_ordered_and_allows_independent_overlap"),
    ("masked-child-exit", "return 0 if passed else 1", "return 0",
     "arm_a_failing_leg_fails_the_run_and_stops_later_starts"),
    ("lost-output", "shutil.copyfileobj(capture, self.out)",
     "self.out.write(capture.read(16))", "arm_every_byte_is_replayed_in_recipe_order"),
    ("three-workers", "MAX_JOBS = 2", "MAX_JOBS = 3", "arm_never_more_than_two_legs_alive"),
    ("parallel-frame-writers", "frame_dump = FRAME_DUMP_VAR in os.environ", "frame_dump = False",
     "arm_the_frame_dump_variable_runs_one_leg_at_a_time"),
    ("unreaped-orphans", 'active = {leg.proc.pid for leg in running}',
     'return\n    active = {leg.proc.pid for leg in running}',
     "arm_an_interrupt_kills_every_leg_and_what_it_spawned"),
)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("lane", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    suite = args.lane.resolve() / "tb/verilator/milan_dp"
    source = (suite / "sim_pool.py").read_text()
    spec = importlib.util.spec_from_file_location("test_sim_pool", suite / "test_sim_pool.py")
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
    records = []
    for name, before, after, arm in MUTANTS:
        if source.count(before) != 1:
            raise RuntimeError(f"{name}: mutation site missing or ambiguous")
        runner = args.output / f"{name}.py"
        runner.write_text(source.replace(before, after))
        tests.RUNNER = runner.resolve()
        started = time.monotonic()
        try:
            getattr(tests, arm)()
        except AssertionError as error:
            result = dict(name=name, caught=True, assertion=str(error), arm=arm)
        else:
            result = dict(name=name, caught=False, arm=arm)
        result.update(elapsed_s=time.monotonic() - started, sha256=hashlib.sha256(runner.read_bytes()).hexdigest())
        records.append(result)
        print(json.dumps(result), flush=True)
        (args.output / "receipts.json").write_text(json.dumps(records, indent=2) + "\n")
    return int(not all(r["caught"] for r in records))


if __name__ == "__main__":
    sys.exit(main())

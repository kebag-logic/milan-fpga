#!/usr/bin/env python3
"""R636-5 union plants for gptp_tables. Run from a checkout: python3 probe_union.py <checkout>.

Builds the collector self-test's synthetic fixture over the real driver
inventory, then plants gptp_tables missing, moved to worker 0, and duplicated
on worker 0; the collector must accept the control and refuse each plant.
"""
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / "scripts"))
from ci_suite_collect import collect  # noqa: E402
from ci_suite_collect_selftest import fixture  # noqa: E402
from ci_suite_pieces import expand_suites  # noqa: E402
from suite_shards import ROOT, balance, sweep_suites, WORKER_OVERHEAD_SECONDS  # noqa: E402

owners, _ = balance(expand_suites(sweep_suites(ROOT / "tb/verilator")), len(WORKER_OVERHEAD_SECONDS))
home = owners["gptp_tables"]
print(f"gptp_tables owner worker {home}/{len(WORKER_OVERHEAD_SECONDS)}")


def run(label, plant):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        workers, unions, _ = fixture(root)
        log = workers / f"suite-logs-{home}" / "gptp_tables.log"
        plant(workers, log)
        try:
            collect(workers, unions, root / "out", "a" * 40)
            print(f"{label}: ACCEPTED")
        except (OSError, ValueError, KeyError) as exc:
            print(f"{label}: REFUSED ({exc})")


run("control", lambda w, log: None)
run("gptp_tables log missing", lambda w, log: log.unlink())
run("gptp_tables moved to worker 0", lambda w, log: shutil.move(log, w / "suite-logs-0" / log.name))
run("gptp_tables duplicated on worker 0", lambda w, log: shutil.copyfile(log, w / "suite-logs-0" / log.name))

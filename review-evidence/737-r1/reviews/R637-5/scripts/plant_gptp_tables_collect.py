#!/usr/bin/env python3
"""Plant gptp_tables ownership defects against the production collector.

Usage: python3 plant_gptp_tables_collect.py <checkout>
Builds the checkout's own synthetic real-inventory fixture, then checks that
scripts/ci_suite_collect.collect accepts it and refuses gptp_tables' log
missing, moved off its owner, or duplicated on another worker."""
import shutil
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
from ci_suite_collect import collect  # noqa: E402
from ci_suite_collect_selftest import fixture  # noqa: E402
from ci_suite_pieces import expand_suites  # noqa: E402
from suite_shards import WORKER_OVERHEAD_SECONDS, balance, sweep_suites  # noqa: E402

suite = "gptp_tables"
owners, _ = balance(expand_suites(sweep_suites(root / "tb/verilator")), len(WORKER_OVERHEAD_SECONDS))
owner = owners[suite]
print(f"{suite} owner worker {owner}")
bad = 0
with tempfile.TemporaryDirectory() as d:
    d = Path(d)
    workers, unions, physical = fixture(d)
    assert suite in physical
    collect(workers, unions, d / "positive", "a" * 40)
    print("accepted: positive fixture; gptp_tables.log collected:", (d / "positive" / f"{suite}.log").is_file())
    log = workers / f"suite-logs-{owner}" / f"{suite}.log"
    other = workers / f"suite-logs-{0 if owner else 1}" / f"{suite}.log"
    data = log.read_bytes()

    def expect_refusal(label):
        global bad
        try:
            collect(workers, unions, d / label, "a" * 40)
        except (ValueError, OSError, KeyError) as exc:
            print(f"refused: {label}: {type(exc).__name__}: {str(exc)[:160]}")
        else:
            print(f"ACCEPTED (defect not caught): {label}")
            bad += 1

    log.unlink(); expect_refusal("missing")
    other.write_bytes(data); expect_refusal("moved-to-other-worker")
    log.write_bytes(data); expect_refusal("duplicated-on-other-worker")
    other.unlink()
    log.write_bytes(b"1 checks: 0 PASS, 1 FAIL\n")
    try:
        collect(workers, unions, d / "failing", "a" * 40)
        print("collector passes a FAIL log through (tally judges verdicts)")
    except (ValueError, OSError, KeyError) as exc:
        print(f"refused: failing-log: {type(exc).__name__}")
    log.write_bytes(data)
    collect(workers, unions, d / "restored", "a" * 40)
    print("accepted: restored fixture")
sys.exit(1 if bad else 0)

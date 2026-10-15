#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise physical log collection, exact worker ownership and union byte binding."""

import json
from pathlib import Path
import tempfile

from ci_suite_collect import collect
from ci_suite_pieces import PIECE_SECONDS, expand_suites, inventory, union
from ci_suite_pieces_selftest import write_leg
from suite_shards import ROOT, WORKER_OVERHEAD_SECONDS, balance, sweep_suites


def fixture(root: Path) -> tuple[Path, Path, list[str]]:
    """Populate real source inventories with synthetic completed observations."""
    physical = sweep_suites(ROOT / "tb/verilator")
    pieces = expand_suites(physical)
    total = len(WORKER_OVERHEAD_SECONDS)
    owners, _ = balance(pieces, total)
    workers, unions = root / "workers", root / "unions"
    workers.mkdir()
    unions.mkdir()
    for leg in range(total):
        path = workers / ("suite-logs-" + str(leg))
        path.mkdir()
        path.joinpath("TARGET_SHA").write_text("a" * 40 + "\n")
    for name in physical:
        if name not in PIECE_SECONDS:
            path = workers / ("suite-logs-" + str(owners[name])) / (name + ".log")
            path.write_text("1 checks: 1 PASS, 0 FAIL\n")
    for suite, lengths in PIECE_SECONDS.items():
        names = inventory(suite)
        for leg in range(len(lengths)):
            write_leg(workers / ("suite-logs-" + str(owners[f"{suite}__{leg}"])), suite, leg, names)
        union(suite, sorted(workers.iterdir()), unions / ("suite-union-" + suite), "a" * 40, "b" * 40)
    return workers, unions, physical


def main() -> int:
    """A final tally receives exactly the original physical suite population."""
    with tempfile.TemporaryDirectory(prefix="suite-collection-") as directory:
        root = Path(directory)
        workers, unions, physical = fixture(root)
        collect(workers, unions, root / "positive", "a" * 40)
        assert {path.stem for path in (root / "positive").glob("*.log")} == set(physical)
        def refused(label: str) -> None:
            """Each damaged artifact is checked by the final production collector."""
            try:
                collect(workers, unions, root / label, "a" * 40)
            except (ValueError, OSError, KeyError):
                print("collection refused:", label)
            else:
                raise AssertionError("accepted " + label)
        extra = workers / "suite-logs-extra"
        extra.mkdir()
        refused("extra-worker")
        extra.rmdir()
        worker = workers / "suite-logs-0"
        sha = worker / "TARGET_SHA"
        sha.write_text("c" * 40 + "\n")
        refused("wrong-worker-head")
        sha.write_text("a" * 40 + "\n")
        log = next(worker.glob("*.log"))
        data = log.read_bytes()
        log.unlink()
        refused("missing-owned-log")
        log.write_bytes(data)
        union_root = unions / ("suite-union-" + next(iter(PIECE_SECONDS)))
        receipt = union_root / "union.json"
        original = receipt.read_bytes()
        value = json.loads(original)
        value["verdicts_sha256"] = "c" * 64
        receipt.write_text(json.dumps(value))
        refused("forged-union-verdicts")
        receipt.write_bytes(original)
        log = next(union_root.glob("*.log"))
        log.write_bytes(log.read_bytes() + b"unobserved output\n")
        refused("changed-union-log")
    print("physical suite collection: all controls PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

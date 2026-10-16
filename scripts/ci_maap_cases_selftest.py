#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check MAAP receipt observations and inventory selection without changing predicates."""

import hashlib
import importlib.util
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from ci_case_receipts import partition, verify

ROOT = Path(__file__).resolve().parents[1]


class Records:
    """Retain exactly what the driver observed before transport or comparison."""

    def __init__(self) -> None:
        self.rows = []

    def record(self, name: str, outcome: str, rc: int, output: str) -> None:
        """The observer has no authority over the driver's own boolean verdict."""
        self.rows.append((name, outcome, rc, output))


def main() -> int:
    """Drive the production selection, observer and union with planted omissions."""
    spec = importlib.util.spec_from_file_location("maap_cases", ROOT / "tb/verilator/maap/mutants.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    names = driver.run_inventory(True)
    assert names[1:] == driver.run_inventory()
    assert len(names) == len(set(names))
    observed = []
    def run_case(work: Path, name: str, source: str, failure: str | None,
                 integration: bool = False, receipt: Records | None = None) -> bool:
        """Observe scheduling arguments while the real campaign applies its anchors."""
        observed.append((name, source, failure, integration))
        return True
    def standalone(receipt: Records) -> bool:
        """Keep the separate default Makefile harness in the scheduling inventory."""
        observed.append(("standalone", None, None, False))
        return True
    with tempfile.TemporaryDirectory(prefix="maap-receipt-controls-") as td:
        work = Path(td)
        with patch.object(driver, "run_case", run_case), patch.object(driver, "standalone", standalone):
            full = driver.campaign(work, names, Records())
            reference = observed[:]
            assert all(full) and [row[0] for row in reference] == names
            observed.clear()
            for index in range(4):
                assert all(driver.campaign(work, partition(names, f"{index}/4"), Records()))
            assert sorted(observed) == sorted(reference)
        for rc, output, failure, expected in (
                (0, " 0 failures\nchecked value: 17\n", None, "pass"),
                (1, "[FAIL] named check\nchecked value: 23\n", "named check", "caught"),
                (0, "[FAIL] named check\n", "named check", "failed"),
                (1, "[FAIL] different check\n", "named check", "failed"),
                (-9, "", "named check", "failed")):
            receipt = Records()
            runs = [subprocess.CompletedProcess([], 0, "compiler", ""),
                    subprocess.CompletedProcess([], rc, output, "")]
            with patch.object(driver.subprocess, "run", side_effect=runs):
                passed = driver.run_case(work, "fixture", "source", failure, receipt=receipt)
            assert passed == (expected in ("pass", "caught"))
            assert receipt.rows == [("fixture", expected, rc, output)]
        print("MAAP observation controls: raw status and checked output preserved")
    receipts = []
    for index in range(4):
        shard = f"{index}/4"
        rows = [{"case": name, "outcome": "pass", "returncode": 0,
                 "output_sha256": hashlib.sha256(name.encode()).hexdigest()}
                for name in partition(names, shard)]
        receipts.append({"schema": 1, "suite": "maap", "head": "a" * 40, "tree": "b" * 40,
                         "inventory": names[:], "shard": shard, "results": rows})
    assert set(verify(names, receipts, "maap", "a" * 40, "b" * 40)) == set(names)
    dropped = names[-1]
    for receipt in receipts:
        receipt["inventory"].remove(dropped)
        receipt["results"] = [row for row in receipt["results"] if row["case"] != dropped]
    try:
        verify(names, receipts, "maap", "a" * 40, "b" * 40)
    except ValueError:
        print("MAAP dropped-everywhere control: refused against the driver inventory")
    else:
        raise AssertionError("missing real mutant accepted")
    print(f"MAAP scheduling controls: {len(names)} cases retain their source and checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

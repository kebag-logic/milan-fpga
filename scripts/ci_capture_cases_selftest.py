#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Prove capture campaign scheduling and thread-local checked-output observations."""

import importlib.util
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

from ci_case_receipts import partition

ROOT = Path(__file__).resolve().parents[1]


class Records:
    """Keep the production scheduler's completed records for direct comparison."""

    def __init__(self) -> None:
        self.rows = []

    def record(self, name: str, outcome: str, rc: int, output: str) -> None:
        """Record without interpreting or changing a driver's returned verdict."""
        self.rows.append((name, outcome, rc, output))


def main() -> int:
    """Exercise inventory, concurrent observation isolation and failure preservation."""
    spec = importlib.util.spec_from_file_location("capture_cases", ROOT / "tb/verilator/capture_coherence/mutants.py")
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    with tempfile.TemporaryDirectory(prefix="capture-case-controls-") as td:
        work = Path(td)
        units = driver.arm_units(work, True)
        names = [unit.name for unit in units]
        assert names[2:] == [unit.name for unit in driver.arm_units(work)]
        assert len(names) == len(set(names))
        assert len(units) == 4 + len(driver.control_groups()) + len(driver.MUTATIONS)
        observed = []
        def fake(check: object, *args: object) -> object:
            """Retain the original registered function and complete argument tuple."""
            observed.append((check, args))
            return lambda: [(True, ["[PASS] fixture"])]
        with patch.object(driver, "one", fake), patch.object(driver, "partial", fake):
            driver.arm_units(work, True)
        assert len(observed) == len(units)
        assert sum(check is driver.mutant_result for check, _ in observed) == len(driver.MUTATIONS)
        def fixture(name: str, passed: bool) -> object:
            """One unit emits its checked values and keeps its own success decision."""
            def run() -> list:
                """Return the fixture verdict after observing its distinct harness output."""
                driver.run_harness("junction", work / name)
                return [(passed, [str(work / name) + " checked 23"])]
            return driver.Unit(name, run, False)
        fixtures = [fixture("first", True), fixture("second", False), fixture("third", True)]
        def run_child(command: list, **kwargs: object) -> tuple[int, str]:
            """Distinct outputs expose accidental sharing between concurrent workers."""
            return 1, "[FAIL] caught check for " + Path(command[0]).name + "\n"
        full = Records()
        with patch.object(driver, "run_child", run_child):
            verdicts = driver.run_units(fixtures, 2, full, work)
            assert verdicts == [True, False, True]
            sharded = Records()
            for index in range(2):
                owned = partition([unit.name for unit in fixtures], f"{index}/2")
                driver.run_units([unit for unit in fixtures if unit.name in owned], 1, sharded, work)
        assert sorted(full.rows) == sorted(sharded.rows)
        assert [row[1] for row in full.rows] == ["pass", "failed", "pass"]
        for name, _outcome, _rc, output in full.rows:
            data = json.loads(output)
            assert data["harnesses"] == [{"leg": "junction", "returncode": 1,
                                          "output": "[FAIL] caught check for " + name + "\n"}]
            assert data["results"][0][1] == ["<case-work>/" + name + " checked 23"]
        assert driver.OBSERVATIONS.get() is None
    print(f"capture scheduling controls: {len(names)} units, unchanged registration arguments")
    print("capture observations: full/sharded values match; failed unit remains failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

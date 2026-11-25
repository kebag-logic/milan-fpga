#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The Makefile case runner refuses failed builds and absent or masked verdicts."""

from pathlib import Path
import tempfile

import ci_make_cases
from ci_make_cases import build, execute, execute_all, inventory, receipt_forms


def start_order_controls(root: Path) -> None:
    """Cases start longest first by measured cost, ties and unmeasured cases in driver
    order, and their results come back in driver order whatever the start order."""
    names = ["short", "long", "tie_a", "unmeasured", "tie_b", "longest"]
    recipe = "".join(f"exec-{name}:\n\t@echo {name} >> started\n"
                     f"\t@printf '{name} checks: 1   failures: 0\\n'\n" for name in names)
    (root / "Makefile").write_text(recipe)
    saved = dict(ci_make_cases.CASE_SECONDS)
    ci_make_cases.CASE_SECONDS.clear()
    ci_make_cases.CASE_SECONDS["controls"] = {"short": 5, "long": 50, "tie_a": 20, "tie_b": 20,
                                              "longest": 90}
    try:
        for jobs in (1, 3):
            (root / "started").unlink(missing_ok=True)
            results = execute_all(root, "controls", names, dict.fromkeys(names, "tally"), jobs)
            assert [output.split()[0] for _, _, output in results] == names, results
            assert all(outcome == "pass" for outcome, _, _ in results), results
            started = (root / "started").read_text().split()
            assert sorted(started) == sorted(names), started
            if jobs == 1:
                # One worker starts each case only after the previous one ends.
                assert started == ["longest", "long", "tie_a", "tie_b", "short", "unmeasured"], started
            print(f"make case start order control, {jobs} job(s): results in driver order")
        ci_make_cases.CASE_SECONDS.clear()
        (root / "started").unlink()
        execute_all(root, "controls", names, dict.fromkeys(names, "tally"), 1)
        assert (root / "started").read_text().split() == names
        print("make case start order control: an unmeasured suite keeps driver order")
    finally:
        ci_make_cases.CASE_SECONDS.clear()
        ci_make_cases.CASE_SECONDS.update(saved)


def main() -> int:
    """Run every control through actual make processes and the production grader."""
    with tempfile.TemporaryDirectory(prefix="make-case-controls-") as directory:
        root = Path(directory)
        recipe = """CASES = good failing masked empty uncounted buildfail
all: $(addprefix exec-,$(CASES))
ci-list:
	@printf '%s\\n' $(CASES)
ci-receipts:
	@$(foreach case,$(CASES),printf '%s\\ttally\\n' '$(case)';)
build-%:
	@true
build-buildfail:
	@false
exec-good:
	@printf 'checks: 1   failures: 0\\nRESULT: PASS\\n'
exec-failing:
	@printf 'checks: 1   failures: 1\\nRESULT: FAIL\\n'
	@exit 1
exec-masked:
	@printf 'checks: 1   failures: 1\\nRESULT: FAIL\\n'
exec-empty:
	@true
exec-uncounted:
	@printf 'checks: 0   failures: 0\\nRESULT: PASS\\n'
exec-buildfail:
	@printf 'checks: 1   failures: 0\\nRESULT: PASS\\n'
"""
        (root / "Makefile").write_text(recipe)
        cases = inventory(root)
        assert cases == ["good", "failing", "masked", "empty", "uncounted", "buildfail"]
        for name in cases:
            rc = build(root, name)
            outcome, _, _ = execute(root, name) if rc == 0 else ("build-failed", rc, "")
            assert (outcome == "pass") == (name == "good"), (name, outcome)
            print(f"make case control: {name}: {outcome}")
        assert receipt_forms(root, cases) == dict.fromkeys(cases, "tally")
        for output in ("RESULT: PASS", "RESULT: FAIL", "", "RESULT: PASS\\nRESULT: PASS"):
            extra = recipe + "\nexec-result:\n\t@printf '" + output + "\\n'\n"
            (root / "Makefile").write_text(extra)
            outcome, _, observed = execute(root, "result", "result-stdout")
            assert (outcome == "pass") == (output == "RESULT: PASS"), (output, outcome)
            assert observed == output.replace("\\n", "\n") + "\n"
            if output == "RESULT: PASS":
                assert execute(root, "result")[0] == "failed"
        for rows in ("good\\ttally", "good\\tunknown", "good\\ttally\\ngood\\ttally"):
            (root / "Makefile").write_text(recipe.split("ci-receipts:")[0] +
                                         "ci-receipts:\n\t@printf '" + rows + "\\n'\n")
            try:
                receipt_forms(root, cases)
            except ValueError:
                print("make receipt form control: invalid registration refused")
            else:
                raise AssertionError("invalid receipt registration accepted")
        for changed in ("good good", "", "../outside"):
            (root / "Makefile").write_text(recipe.replace("CASES = " + " ".join(cases), "CASES = " + changed))
            try:
                inventory(root)
            except ValueError:
                print(f"make inventory control: {changed!r} refused")
            else:
                raise AssertionError(f"invalid inventory accepted: {changed!r}")
        start_order_controls(root)
    for suite, cost in ci_make_cases.CASE_SECONDS.items():
        # A misspelt case would silently cost 0; every measured name is a live case.
        live = inventory(ci_make_cases.ROOT / "tb/verilator" / suite)
        assert set(cost) <= set(live), (suite, sorted(set(cost) - set(live)))
        print(f"make case start order: {suite}'s {len(cost)} measured costs name live cases")
    print("make case runner: all controls pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The Makefile case runner refuses failed builds and absent or masked verdicts."""

from pathlib import Path
import tempfile

from ci_make_cases import execute, inventory


def main() -> int:
    """Run every control through actual make processes and the production grader."""
    with tempfile.TemporaryDirectory(prefix="make-case-controls-") as directory:
        root = Path(directory)
        recipe = """CASES = good failing masked empty uncounted buildfail
all: $(addprefix exec-,$(CASES))
ci-list:
	@printf '%s\\n' $(CASES)
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
            outcome, _, _ = execute(root, name)
            assert (outcome == "pass") == (name == "good"), (name, outcome)
            print(f"make case control: {name}: {outcome}")
        for changed in ("good good", "", "../outside"):
            (root / "Makefile").write_text(recipe.replace("CASES = " + " ".join(cases), "CASES = " + changed))
            try:
                inventory(root)
            except ValueError:
                print(f"make inventory control: {changed!r} refused")
            else:
                raise AssertionError(f"invalid inventory accepted: {changed!r}")
    print("make case runner: all controls pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

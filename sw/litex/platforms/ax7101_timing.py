# SPDX-License-Identifier: CERN-OHL-W-2.0
"""AX7101 release operating grade, shared by implementation and checkpoint reports.

Issue #395's owner decision limits the dev-board release to commercial Tj.
Artix-7 uses fixed Slow/Fast speed models, not temperature-prorated delays.
The junction setting records the power condition; both timing models must
retain both setup and hold analysis (UG835 config_timing_corners).
"""

from pathlib import Path


TIMING_GRADE = {
    "part": "xc7a100t-fgg484-2",
    "grade": "commercial",
    "junction_min_c": 0,
    "junction_max_c": 85,
    "corners": ("Slow", "Fast"),
}


def tcl_word(value: str | Path) -> str:
    """Quote a literal path or declaration word without Tcl substitution."""
    text = str(value)
    if any(char in text for char in "{}\\\n\r"):
        raise ValueError(f"unsupported Tcl literal: {text!r}")
    return "{" + text + "}"


def configure_commands() -> list[str]:
    """Derive the pre-placement and read-only checkpoint setup from one declaration."""
    script = Path(__file__).resolve().parents[1] / "timing_grade.tcl"
    if not script.is_file():
        raise FileNotFoundError(f"missing timing grade hook: {script}")
    grade = TIMING_GRADE
    return [
        f"source {tcl_word(script)}",
        "kl_timing_grade_configure " + " ".join(tcl_word(str(value)) for value in (
            grade["part"], grade["grade"], grade["junction_min_c"],
            grade["junction_max_c"], " ".join(grade["corners"]))),
    ]

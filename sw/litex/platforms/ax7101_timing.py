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

#: The dies this board is built for (#911). The XC7A200T variant is the same
#: board in the pin-compatible FBG484 footprint, so it keeps the release grade,
#: Tj range, corners and speed grade above and differs only in the part.
BOARD_PARTS = ("xc7a100t-fgg484-2", "xc7a200t-fbg484-2")


def board_part(part: str | None = None) -> str:
    """The die a build targets: `part`, or the declaration's own when None."""
    if part is None or part == TIMING_GRADE["part"]:
        return TIMING_GRADE["part"]
    if part not in BOARD_PARTS:
        raise ValueError(f"part {part!r} is not one of {BOARD_PARTS}")
    return part


def tcl_word(value: str | Path) -> str:
    """Quote a literal path or declaration word without Tcl substitution."""
    text = str(value)
    if any(char in text for char in "{}\\\n\r"):
        raise ValueError(f"unsupported Tcl literal: {text!r}")
    return "{" + text + "}"


def configure_commands(part: str | None = None) -> list[str]:
    """Derive the pre-placement and read-only checkpoint setup from one declaration.

    `part` is the die the build targets, one of BOARD_PARTS; None is the
    declaration's own part, read when called.
    """
    script = Path(__file__).resolve().parents[1] / "timing_grade.tcl"
    if not script.is_file():
        raise FileNotFoundError(f"missing timing grade hook: {script}")
    grade = dict(TIMING_GRADE, part=board_part(part))
    return [
        f"source {tcl_word(script)}",
        "kl_timing_grade_configure " + " ".join(tcl_word(str(value)) for value in (
            grade["part"], grade["grade"], grade["junction_min_c"],
            grade["junction_max_c"], " ".join(grade["corners"]))),
    ]

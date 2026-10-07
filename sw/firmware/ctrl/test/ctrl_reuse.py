# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_reuse.py - the processor's ADP and ACMP stimulus, cut out of the pinned submodule.

adp_walk.cpp includes pp_adp_reuse.inc and acmp_walk.cpp includes
pp_acmp_reuse.inc, pp_disc_reuse.inc and pp_talker_reuse.inc. This module
writes them, at build time, from the processor's own suites, after proving
that the submodule is checked out at the superproject's gitlink and that each
file's bytes are the blob that pin records: the walks reuse the processor's
own constants, frame builders, Table 5.51 transcription (tb/adp_engine), its
F05.3 matrix model of Milan Table 5.30 (tb/acmp_listener), its Table 5.54
transcription (tb/adp_engine) and its F05.11 constants (tb/acmp_talker),
never a copy of them. A marker that is missing or repeated refuses the run,
so a reshaped harness is noticed rather than half-cut.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from ctrl_build import PP, PP_ADP_SIM, ROOT, Refusal

#: The processor's ADP stimulus this gate reuses: (what, first line, end marker,
#: whether the end marker's line is part of the slice).
REUSE_SLICES = (
    ("the fixed entity configuration and the model_frame builder",
     "// ---- fixed configuration driven into the DUT", "// ---- independent 393-bit pp_txn_t codec", False),
    ("the Table 5.51 transcription ADV", "enum AdvCol {", "constexpr AdvCell ADV[N_AROW][N_ACOL] = {", True),
)

#: Every file cut, and the slices each output takes from it: (output, the
#: suite's file, its slices).
REUSE = (
    ("pp_adp_reuse.inc", PP_ADP_SIM, REUSE_SLICES),
    ("pp_acmp_reuse.inc", "tb/acmp_listener/sim_main.cpp", (
        ("the doc's constants, the ACMPDU and record transcriptions, the stimulus and the F05.3 matrix model",
         "// ---- constants shared with the doc (not with the RTL)",
         "// Harness: cycle-exact emulation of the landed faces + collectors", False),)),
    ("pp_disc_reuse.inc", PP_ADP_SIM, (
        ("the Table 5.54 transcription DISC", "// The listener's discovery SM, one per sink", "namespace {", False),)),
    ("pp_talker_reuse.inc", "tb/acmp_talker/sim_main.cpp", (
        ("the F05.11 constants", "// ---- 05 §3 / F05.11 constants (the document, not the DUT)",
         "// the RX-slot model backing", False),)),
)


def git(*args: str, cwd: Path = ROOT) -> str:
    """One git answer, with replace refs ignored; a failure refuses."""
    if cwd.resolve() != ROOT.resolve() and args != ("rev-parse", "--show-toplevel"):
        if Path(git("rev-parse", "--show-toplevel", cwd=cwd)).resolve() != cwd.resolve():
            raise Refusal("dependency directory is not its own checkout")
    res = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False,
                         env={**os.environ, "GIT_NO_REPLACE_OBJECTS": "1"})
    if res.returncode != 0:
        raise Refusal(f"git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout.strip()


def prove_pin(path: str = PP_ADP_SIM) -> tuple[str, str]:
    """The processor's gitlink, its checkout at that commit, and the reused file's blob."""
    record = git("ls-files", "-s", "--", "protocol-processor").split()
    if len(record) != 4 or record[0] != "160000" or record[2] != "0":
        raise Refusal(f"protocol-processor is not one stage-0 gitlink: {record}")
    pin = record[1]
    if Path(git("rev-parse", "--show-toplevel", cwd=PP)).resolve() != PP.resolve():
        raise Refusal("protocol-processor is not its own checkout")
    if git("rev-parse", "HEAD", cwd=PP) != pin:
        raise Refusal(f"protocol-processor is not at its pin {pin}")
    blob = git("ls-tree", pin, path, cwd=PP).split()
    if len(blob) < 3 or git("hash-object", path, cwd=PP) != blob[2]:
        raise Refusal(f"{path} differs from the blob the pin records")
    return pin, blob[2]


def cut(lines: list[str], what: str, first: str, end: str, inclusive: bool) -> list[str]:
    """One slice of the processor's harness; each marker must occur exactly once."""
    starts = [i for i, ln in enumerate(lines) if ln.startswith(first)]
    ends = [i for i, ln in enumerate(lines) if ln.startswith(end)]
    if len(starts) != 1 or len(ends) != 1 or ends[0] < starts[0]:
        raise Refusal(f"{what}: markers {first!r} / {end!r} found {len(starts)} / {len(ends)} times")
    stop = ends[0]
    if inclusive:
        closing = [i for i in range(stop, len(lines)) if lines[i] == "};"]
        if not closing:
            raise Refusal(f"{what}: no closing '}};' after {end!r}")
        stop = closing[0] + 1
    return lines[starts[0]:stop]


def cut_reuse(dest: Path) -> Path:
    """Write every reused slice, each from its pinned file; returns pp_adp_reuse.inc."""
    dest.mkdir(parents=True, exist_ok=True)
    for name, path, slices in REUSE:
        pin, blob = prove_pin(path)
        lines = (PP / path).read_text(encoding="utf-8").splitlines()
        out = [f"// CUT by sw/firmware/ctrl/test/test_ctrl_firmware.py from protocol-processor/{path}",
               f"// at the pin {pin} (blob {blob}); DO NOT EDIT, it is rewritten on every run."]
        for what, first, end, inclusive in slices:
            out += ["", f"// ---- {what}"] + cut(lines, what, first, end, inclusive)
        (dest / name).write_text("\n".join(out) + "\n", encoding="utf-8")
    return dest / "pp_adp_reuse.inc"

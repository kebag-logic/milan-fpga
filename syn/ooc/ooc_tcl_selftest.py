#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive the two OOC .tcl recipes' pre-synthesis refusals, automatically.

pp_shadow_ooc.tcl refuses to synthesize when a `$readmemh` image is missing or
empty, and it takes the source generator's exit status. Both refusals had
manual evidence and no test ([R0] on PR #240): deleting either one left every
hosted check green, which is the definition of a defense that rots.

milan_datapath_ooc.tcl (#246) derives its read set from dp_srcs.py, finds its
geometry packages IN that record, reads each geometry number from the ONE
live declaration (comments stripped, name boundary-anchored), GENERATES all
three images into fresh temp targets, validates their exact geometry, and publishes
by rename only after validation. Stale+no-op, one-token, truncated and
malformed images, commented-out or duplicated declarations, and a record
without the packages are all refusals before anything is read ([R-parallel]
and [R0] on PR #264 closed those survivors, round by round).

WHAT IT RUNS IS THE REAL .TCL, not a copy of its logic. `tclsh` sources the
tracked file with the Vivado-only commands stubbed. `read_verilog` RETURNS
(it does not exit) and RECORDS every file it is handed; the sentinel prints
at `synth_design`, whose stub is the observation point for the synthesis
safeguards:

  - every `-generic *_HEX_P=...` it receives must be quoted, absolute, an
    existing non-empty file, carry the CANONICAL basename for its parameter
    (PP_UCODE_HEX_P -> ucode.hex, PP_TROM_HEX_P -> ltn_rom.hex,
    GPTP_UCODE_HEX_P -> gptp_ucode.hex), and hold
    that ROM's geometry, or the stub errors -- an existing-but-wrong file
    opens cleanly, so Synth 8-4445 never protects that case;
  - `set_msg_config` is MODELLED, not transcribed: the stub keeps the final
    severity per message id, and the positive arm requires the EFFECTIVE
    severity of Synth 8-4445 at synth_design to be ERROR -- a downgrade
    applied after the promotion is the same defect as never promoting;
  - the recorded read set is written out and the positive arm requires it to
    EQUAL what dp_srcs.py derives, so a hand-written list cannot stand in
    for the record while the suite stays green.

Mutation copies of the recipe prove every one of those detectors can fail.

`tclsh` is the interpreter Vivado embeds, so the guard is exercised by the
language it is written in rather than reimplemented in Python. What tclsh
cannot prove is Vivado's own semantics; the real-Vivado negative control for
the promotion (a missing image at synthesis with the preflight removed must
abort, not warn) is recorded on the PR that lands a change.

    python3 syn/ooc/ooc_tcl_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/dp_srcs.py --selftest.
Needs the protocol-processor and verilog-axis submodules and sv2v, because
the datapath recipe derives its read set before anything else, so every arm
pays one dp_srcs.py run (~5 minutes total).
"""
import shutil
import sys
from pathlib import Path

from ooc_tcl_arms import ARMS, run_all
from ooc_tcl_harness import REPO, TCL, SelfTestPrereq, Suite, derived_record

#: Arm failures, held module-level so a prerequisite failure part-way through
#: still reports what ran before it rather than discarding the lot.
_PROBLEMS = []


def selftest() -> tuple[list[str], int]:
    """What the arms failed to prove, and how many of them ran.

    The ran count is returned, not just printed, because the arm total is
    itself an assertion: a suite that quietly stops running arms exits green,
    which is the false green this file exists to close.
    """
    suite = Suite(_PROBLEMS)
    problems = suite.problems
    del problems[:]
    if not shutil.which("tclsh"):
        # NOT a skip. A skip here is the false green this file exists to close;
        # the workflow installs tclsh for exactly this reason.
        return ["tclsh is not on PATH, so %s cannot be exercised. Install tcl "
                "(the interpreter Vivado embeds) rather than skipping: an "
                "unexercised refusal is the defect this file tests for."
                % Path(TCL).relative_to(REPO)], 0

    # Derived FIRST, for the same reason the recipe derives first: if the
    # record is unavailable, nothing below proves anything. Reaching it here
    # turns a raw CalledProcessError traceback -- which used to unwind past
    # the problem report and discard every arm already run -- into a named
    # refusal at arm zero.
    try:
        derived_record()
    except SelfTestPrereq as exc:
        return ["SELF-TEST PREREQUISITE UNAVAILABLE: %s" % exc], 0

    run_all(suite)

    if suite.ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), this "
                        "file declares %d." % (suite.ran, ARMS))
    return problems, suite.ran


def main() -> int:
    """The gate's exit status: 0 only when every declared arm proved its refusal."""
    try:
        bad, ran = selftest()
    except SelfTestPrereq as exc:
        # Named, and with the arms already run still reported: an aborted
        # suite must not look like a suite that found nothing.
        bad, ran = _PROBLEMS + ["SELF-TEST ABORTED: %s" % exc], 0
    for b in bad:
        print("  -", b, file=sys.stderr)
    if bad:
        return 2
    print("OOC .tcl refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())

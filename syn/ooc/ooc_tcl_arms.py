#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The arms of the OOC .tcl self-test: one planted refusal each.

Every function here takes the `Suite` and runs a group of arms against the
real pp_shadow_ooc.tcl and milan_datapath_ooc.tcl, using the stubs and the
machinery in `ooc_tcl_harness.py`. The groups are named for what they hold the
recipes to; `run_all` is the order they run in, and `ARMS` is how many arms
that comes to - a deleted arm is a self-test that still prints a pass, so the
count is asserted by the caller in `ooc_tcl_selftest.py`.
"""
import os
import shutil
import tempfile
from pathlib import Path

from ooc_tcl_harness import (
    Arm, DP_TCL, EFFECTIVE_OK, GEN_GPTP, GEN_LTN, GEN_UCODE, READ_LIST,
    REAL_PYTHON, Suite, _mutant, _read_text, _write, derived_sources,
    dp_positive, fires, images, pkg_mutant, unpublished)

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 58


def _arms_pp_shadow_images(suite):
    """Arms 1-5: pp_shadow_ooc.tcl REQUIRES its two images and does not generate
    them, and it takes the read-set generator's exit status."""
    arm = suite.run

    # ---- pp_shadow_ooc.tcl: requires, does not generate ------------------

    # Arm 1. Neither image. The first one named is the one reported.
    arm(Arm("no-images", "ltn_rom.hex is missing or empty", False))

    # Arm 2. The image the finding document used to name on its own.
    arm(Arm("ucode-missing", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex")))

    # Arm 3. Present and zero bytes: `file exists` alone would pass this, and
    # Vivado reads an empty image exactly as it reads an absent one.
    arm(Arm("ucode-empty", "ucode.hex is missing or empty", False,
        images("ltn_rom.hex", "ucode.hex!")))

    # Arm 4. ANTI-VACUITY. Both images present and non-empty must reach
    # synthesis. Without this arm a guard that always fires passes arms 1-3.
    arm(Arm("both-images-present", None, True, images("ltn_rom.hex", "ucode.hex")))

    # Arm 5. The .tcl must take the generator's exit status (dp_srcs.py here:
    # the read-set generator is the first exec this recipe runs).
    stub = tempfile.mkdtemp(prefix="dp-srcs-fails-")
    fake = Path(stub) / "python3"
    fake.write_text("#!/bin/sh\necho 'dp_srcs: planted generator failure' >&2\n"
                    "exit 2\n")
    fake.chmod(0o755)
    # `stub` stays `str`: the next thing it does is become part of PATH.
    arm(Arm("generator-failure-propagates", "planted generator failure", False,
        images("ltn_rom.hex", "ucode.hex"),
        env={"PATH": stub + os.pathsep + os.environ.get("PATH", "")}))
    shutil.rmtree(stub, ignore_errors=True)


def _arms_datapath_generators(suite):
    """Arms 6-14: milan_datapath_ooc.tcl's own generators - a dead one, and every
    way the microcode and transition-ROM images can come back the wrong
    shape, each refused before anything is read."""
    dp_arm = suite.dp_arm

    # ---- milan_datapath_ooc.tcl: derives, generates, validates -----------

    # Arm 6. A dead microcode generator aborts the script: its exit status
    # is taken by `exec`, never discarded.
    def no_temp_left(d: str, log: str) -> str | None:
        """Name the generator temps a refused run left in the run directory,
        so near-copies of the ROMs cannot accumulate unnoticed."""
        left = sorted(f.name for f in Path(d).iterdir() if ".gen." in f.name)
        if left:
            return ("the generator temp survived the refusal: %s. It is "
                    "cleaned on the validation path, so it must be cleaned "
                    "here too or near-copies of the ROMs accumulate"
                    % ", ".join(left))
        return None

    dp_arm(Arm("dp-ucode-generator-fail", "planted ucode generator failure",
               check=no_temp_left),
           "gen_ucode.py",
           "echo 'planted ucode generator failure' >&2\n  exit 3")

    # Arm 7. A generator that exits 0 leaving an empty image: zero words is
    # not the ROM's geometry.
    dp_arm(Arm("dp-ucode-empty", "0 words, expected exactly 2048"),
           "gen_ucode.py",
           ": > \"$out\"\n  exit 0")

    # Arm 8. ONE syntactically valid word ([R-parallel]'s exact plant): it
    # is non-empty, and $readmemh would load it and leave 2,047 words X.
    dp_arm(Arm("dp-ucode-one-word", "1 words, expected exactly 2048"),
           "gen_ucode.py",
           "printf '000000000000\\n' > \"$out\"\n  exit 0")

    # Arm 9. Truncated: right words, too few of them.
    dp_arm(Arm("dp-ucode-truncated", "1000 words, expected exactly 2048"),
           "gen_ucode.py",
           "%s %s -o \"$out.full\" > /dev/null && "
           "head -1000 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
           "  exit 0" % (REAL_PYTHON, GEN_UCODE))

    # Arm 10. Malformed word: full depth, one word the wrong shape. `Z` is
    # $readmemh-legal and loads as Z, which is exactly why it is refused.
    dp_arm(Arm("dp-ucode-malformed", "not exactly 12 hex digits",
               check=unpublished('ucode.hex')),
           "gen_ucode.py",
           "%s %s -o \"$out\" > /dev/null && "
           "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
           % (REAL_PYTHON, GEN_UCODE))

    # Arm 11. STALE image + no-op generator ([R-parallel]'s exact plant):
    # the pre-created file must not survive to be measured; the no-op leaves
    # no temp file, which is the refusal, and the stale image is deleted.
    def stale_gone(d: str, log: str) -> str | None:
        """Name the pre-created ucode.hex when the refusal left it standing to
        be measured by a later run."""
        if (Path(d) / "ucode.hex").exists():
            return "the stale ucode.hex survived the refusal"
        return None
    dp_arm(Arm("dp-ucode-stale-noop", "leaving no file",
               setup=lambda d: _write(d, "ucode.hex", "STALE\n"),
               check=stale_gone),
           "gen_ucode.py",
           "exit 0")

    # Arm 12. The transition ROM gets the identical geometry contract.
    dp_arm(Arm("dp-ltn-one-word", "1 words, expected exactly 128"),
           "gen_ltn_rom.py",
           "printf '00000000\\n' > \"$out\"\n  exit 0")

    # Arm 13. ...and the identical width contract.
    dp_arm(Arm("dp-ltn-malformed", "not exactly 8 hex digits",
               check=unpublished('ltn_rom.hex')),
           "gen_ltn_rom.py",
           "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
           "  exit 0" % (REAL_PYTHON, GEN_LTN))

    # Arm 14. ...and its generator's exit status.
    dp_arm(Arm("dp-ltn-generator-fail", "planted ltn generator failure"),
           "gen_ltn_rom.py",
           "echo 'planted ltn generator failure' >&2\n  exit 3")


def _arms_synth_design_call(suite):
    """Arm 15, the ANTI-VACUITY arm and the observation point for every synthesis
    safeguard, and arms 16-21, the mutations that prove each safeguard's
    detector can fail: the promotion, and each ROM generic."""
    arm = suite.run

    # Arm 15. ANTI-VACUITY, and the observation point for every synthesis
    # safeguard: from an EMPTY directory the real generators run, both
    # validated images land in the run directory, synth_design receives BOTH
    # canonical absolute ROM generics (the stub has rechecked basename and
    # geometry), the EFFECTIVE severity of Synth 8-4445 there is ERROR, and
    # the read set the stubs recorded EQUALS what dp_srcs.py derives.
    arm(Arm("dp-empty-dir-generates-and-passes", None, True, tcl=DP_TCL,
        check=dp_positive))

    # Arm 16. MUTATION: the promotion deleted. The detector must distinguish,
    # or arm 15's effective-severity assertion is vacuous.
    mut = _mutant(r"set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n",
                  "", "promotion-deleted")
    try:
        arm(Arm("dp-mut-promotion-deleted", None, True, tcl=mut,
            check=lambda d, log: None if EFFECTIVE_OK not in log
            else "the mutant still shows an ERROR effective severity"))
    finally:
        os.unlink(mut)

    # Arm 17. MUTATION: the promotion followed by a DOWNGRADE of the same id
    # ([R0]'s exact plant). Historical text still contains the ERROR
    # spelling; only the effective-severity model can tell them apart.
    mut = _mutant(r"(set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n)",
                  "\\1set_msg_config -id {Synth 8-4445} -new_severity "
                  "{CRITICAL WARNING}\n", "promotion-downgraded-after")
    try:
        def downgraded(d: str, log: str) -> str | None:
            """Name how the effective-severity model read the downgrade: it
            must no longer say ERROR, and it must have RECORDED the CRITICAL
            WARNING that replaced it rather than lost the id entirely."""
            if EFFECTIVE_OK in log:
                return "the downgrade-after-promotion mutant still reads as " \
                       "an ERROR effective severity"
            if "OOC-EFFECTIVE-SEV: {Synth 8-4445} = CRITICAL WARNING" not in log:
                return "the effective-severity model did not record the " \
                       "downgrade"
            return None
        arm(Arm("dp-mut-promotion-downgraded-after", None, True, tcl=mut,
            check=downgraded))
    finally:
        os.unlink(mut)

    # Arm 18. MUTATION: the ucode generic deleted from synth_design's call.
    mut = _mutant(r" -generic \$UCODE_GENERIC", "", "ucode-generic-deleted")
    try:
        arm(Arm("dp-mut-ucode-generic-deleted", None, True, tcl=mut,
            check=lambda d, log: None
            if "OOC-GENERIC-OK: PP_UCODE_HEX_P" not in log
            else "the mutant still shows the ucode generic"))
    finally:
        os.unlink(mut)

    # Arm 19. MUTATION: the ucode generic redirected at a MISSING image.
    mut = _mutant(r'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"\[file normalize '
                  r'ucode\.hex\]\\""',
                  'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"[file normalize '
                  'missing-ucode.hex]\\""', "ucode-generic-redirected")
    try:
        arm(Arm("dp-mut-ucode-generic-redirected", "SYNTH-GENERIC-IMAGE-MISSING",
            False, tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 20. MUTATION: the ucode generic CROSS-WIRED at the OTHER image
    # ([R0]'s exact plant). The file exists and opens, so Synth 8-4445 never
    # fires; only the canonical-basename binding refuses it.
    mut = _mutant(r'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"\[file normalize '
                  r'ucode\.hex\]\\""',
                  'set UCODE_GENERIC "PP_UCODE_HEX_P=\\"[file normalize '
                  'ltn_rom.hex]\\""', "ucode-cross-wired")
    try:
        arm(Arm("dp-mut-ucode-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 21. MUTATION: the transition-ROM generic cross-wired the other way.
    mut = _mutant(r'set TROM_GENERIC  "PP_TROM_HEX_P=\\"\[file normalize '
                  r'ltn_rom\.hex\]\\""',
                  'set TROM_GENERIC  "PP_TROM_HEX_P=\\"[file normalize '
                  'ucode.hex]\\""', "trom-cross-wired")
    try:
        arm(Arm("dp-mut-trom-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut))
    finally:
        os.unlink(mut)


def _arms_geometry_parser(suite):
    """Arms 22-25f: the geometry read out of the ONE live declaration - comments,
    prefixes, duplicates, absences and non-nibble widths."""
    arm = suite.run

    # ---- the geometry parser ([R0] round three, finding 2) ---------------

    # Arm 22. [R0]'s exact plant: a stale value in a line comment above a
    # live declaration of 52. The LIVE value must win; with 52 the real
    # 48-bit generator output no longer fits, and THAT refusal is the proof
    # the comment did not win (had it won, the run would have passed).
    pkg, mut = pkg_mutant(
        "// stale example: UCODE_W_C = 48\n"
        "localparam int unsigned UCODE_W_C = 52;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-comment-shadow")
    try:
        arm(Arm("dp-pkg-comment-shadow-live-wins", "not exactly 13 hex digits",
            False, tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 23. Block comments are stripped and prefixed identifiers do not
    # match: a /* UCODE_W_C = 40; */ and an XUCODE_W_C = 99 beside the live
    # 48/11 must leave the run WELL-FORMED (the real image fits 48).
    pkg, mut = pkg_mutant(
        "/* stale block:\n   localparam int unsigned UCODE_W_C = 40;\n*/\n"
        "localparam int unsigned XUCODE_W_C = 99;\n"
        "localparam int unsigned UCODE_W_C  = 48;\n"
        "localparam int unsigned UPC_W_C    = 11;\n", "pkg-block-and-prefix")
    try:
        arm(Arm("dp-pkg-block-comment-and-prefix", None, True, tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 24. TWO live declarations: a refusal, never a pick.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UCODE_W_C = 52;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-duplicate")
    try:
        arm(Arm("dp-pkg-duplicate", "expected exactly one live declaration",
            False, tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 25. ZERO live declarations (only a commented one): same refusal.
    pkg, mut = pkg_mutant(
        "// localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UPC_W_C = 11;\n", "pkg-missing")
    try:
        arm(Arm("dp-pkg-missing", "expected exactly one live declaration", False,
            tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arms 25a-25f. NON-NIBBLE widths refuse outright ([R-parallel] round
    # three): 50/4 truncates to 12 digits and the exact probe showed the
    # stale 2,048x48 image satisfying a declared width of 50. Widths 49-51
    # (microcode) and 33-35 (transition ROM) must each refuse BEFORE any
    # image can validate; the supported widths keep their behavior (48/32
    # pristine in arm 15, and 52 correctly demanding 13 digits in arm 22).
    for w in (49, 50, 51):
        pkg, mut = pkg_mutant(
            "localparam int unsigned UCODE_W_C = %d;\n"
            "localparam int unsigned UPC_W_C = 11;\n" % w,
            "pkg-width-%d" % w)
        try:
            arm(Arm("dp-pkg-width-%d-not-nibble" % w,
                "not a positive nibble-aligned", False, tcl=mut))
        finally:
            os.unlink(mut)
            os.unlink(pkg)
    for w in (33, 34, 35):
        pkg, mut = pkg_mutant(
            "localparam int unsigned TROM_W_C = %d;\n"
            "localparam int unsigned TROM_DEPTH_C = 128;\n" % w,
            "pkg-trom-width-%d" % w, which="acmp")
        try:
            arm(Arm("dp-pkg-trom-width-%d-not-nibble" % w,
                "not a positive nibble-aligned", False, tcl=mut))
        finally:
            os.unlink(mut)
            os.unlink(pkg)


def _arms_derived_source_connection(suite):
    """Arms 26-27: the read set is dp_srcs.py's record, so a hand list cannot
    stand in for it and an empty record is a refusal the recipe authors."""
    arm = suite.run

    # ---- the derived-source connection ([R0] round three, finding 5) -----

    # Arm 26. MUTATION: dp_srcs.py's record replaced by [R0]'s exact plant, a
    # hand list of the two packages. Geometry still resolves and the run
    # still reaches synthesis, which is exactly why the read-set-equality
    # detector exists: it must distinguish, or arm 15 is vacuous. The plant's
    # paths are COMPOSED here, not spelled: the contiguous submodule-source
    # path exists only in the untracked mutant, which is the planted defect
    # under test -- a tracked spelling would rightly trip
    # scripts/pp_srcs.py --check, and that trip is itself part of what this
    # plant is shown to hit on the real tree (PR #264 evidence).
    pp_root = "$REPO/protocol-processor" + "/hdl"
    gp_root = "$REPO/gptp-processor" + "/hdl"
    mut = _mutant(
        r"exec python3 \$DP_SRCS --top \$TOP --record 2>\$REC_ERR",
        'set _ "top=milan_datapath\\ndefine=SYNTHESIS'
        '\\nincdir=$REPO/configs/generated/endstation_arty_current'
        '\\nsrc=%s/aecp/ucpu_pkg.sv\\nsrc=%s/acmp/pp_acmp_pkg.sv'
        '\\nsrc=%s/ucpu/gptp_ucpu_pkg.sv"'
        % (pp_root, pp_root, gp_root),
        "srcs-hand-list")
    try:
        def hand_list_detected(d: str, log: str) -> str | None:
            """Name the hand-list plant as indistinguishable when the read set
            it produced still equals dp_srcs.py's record -- that equality is
            the whole detector arm 15 leans on."""
            rl = Path(d) / READ_LIST
            if not rl.is_file():
                return "the stubs recorded no read set"
            got = sorted(l.strip() for l in _read_text(rl).splitlines()
                         if l.strip())
            if got == derived_sources():
                return "the hand-list mutant read set equals the record: " \
                       "the detector cannot distinguish"
            return None
        arm(Arm("dp-mut-srcs-hand-list", None, True, tcl=mut,
            check=hand_list_detected))
    finally:
        os.unlink(mut)

    # Arm 27. MUTATION: the record comes back EMPTY. Nothing downstream may
    # quietly supply a list, and the refusal must be one the recipe AUTHORS:
    # the old spelling asserted the bare substring "SRC_LINES", which Tcl's
    # own undefined-variable error satisfied by echoing the source line.
    mut = _mutant(r"exec python3 \$DP_SRCS --top \$TOP --record 2>\$REC_ERR",
                  'set _ ""', "srcs-empty-record")
    try:
        arm(Arm("dp-mut-srcs-empty-record",
            "expected exactly one top and that top to be", False, tcl=mut))
    finally:
        os.unlink(mut)


def _arms_gptp_image(suite):
    """Arms 28-34: the integrated gPTP engine's image gets the identical
    contract - generator status, geometry, generic binding and width."""
    arm, dp_arm = suite.run, suite.dp_arm

    # ---- the integrated gPTP engine's image (#116: default-on fabric) ----

    # Arms 28-31. The third $readmemh image gets the identical contract:
    # generator exit status taken, zero/one-word/malformed images refused
    # against the geometry derived from gptp_ucpu_pkg.sv (1,024x48 at the
    # pin), before anything is read.
    dp_arm(Arm("dp-gptp-generator-fail", "planted gptp generator failure"),
           "gen_gptp_ucode.py",
           "echo 'planted gptp generator failure' >&2\n  exit 3")
    dp_arm(Arm("dp-gptp-empty", "0 words, expected exactly 1024"),
           "gen_gptp_ucode.py",
           ": > \"$out\"\n  exit 0")
    dp_arm(Arm("dp-gptp-one-word", "1 words, expected exactly 1024"),
           "gen_gptp_ucode.py",
           "printf '000000000000\\n' > \"$out\"\n  exit 0")
    dp_arm(Arm("dp-gptp-malformed", "not exactly 12 hex digits",
               check=unpublished('gptp_ucode.hex')),
           "gen_gptp_ucode.py",
           "%s %s -o \"$out\" > /dev/null && "
           "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
           % (REAL_PYTHON, GEN_GPTP))

    # Arm 32. MUTATION: the gptp generic deleted from synth_design's call.
    mut = _mutant(r" \\\n  -generic \$GUCODE_GENERIC", "",
                  "gptp-generic-deleted")
    try:
        arm(Arm("dp-mut-gptp-generic-deleted", None, True, tcl=mut,
            check=lambda d, log: None
            if "OOC-GENERIC-OK: GPTP_UCODE_HEX_P" not in log
            else "the mutant still shows the gptp generic"))
    finally:
        os.unlink(mut)

    # Arm 33. MUTATION: the gptp generic cross-wired at the AECP image. It
    # exists and opens, so Synth 8-4445 never fires. (The basename binding
    # and the geometry check BOTH refuse it today, because 8- and 12-digit
    # words are mutually exclusive; the basename guard only becomes the sole
    # detector if two ROMs ever share a geometry.)
    mut = _mutant(r'set GUCODE_GENERIC "GPTP_UCODE_HEX_P=\\"\[file normalize '
                  r'gptp_ucode\.hex\]\\""',
                  'set GUCODE_GENERIC "GPTP_UCODE_HEX_P=\\"[file normalize '
                  'ucode.hex]\\""', "gptp-cross-wired")
    try:
        arm(Arm("dp-mut-gptp-cross-wired", "SYNTH-GENERIC-WRONG-IMAGE", False,
            tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 34. The gptp package width gets the same non-nibble refusal.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 50;\n"
        "localparam int unsigned UPC_W_C = 10;\n", "pkg-gptp-width-50",
        which="gptp")
    try:
        arm(Arm("dp-pkg-gptp-width-50-not-nibble",
            "not a positive nibble-aligned", False, tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)


def _arms_what_the_tool_is_handed(suite):
    """Arms 35-39: everything else on the synth_design line - the include path's
    ORDER, the top, the defines, -sv and the part - each mutated, and each
    required to be caught by the detector this arm names."""
    arm = suite.run

    # ---- what the recipe hands the TOOL (post-merge review of PR #264) ----
    #
    # The stub used to inspect only -generic, so every other argument of the
    # synth_design line was unobserved -- and that is exactly where the recipe
    # was wrong: it spelled -include_dirs by hand, in an order that selected a
    # different elaboration shape than the portability gate, and dropped the
    # record's define. Each mutation below is caught by dp_positive; the arm
    # passes when the detector fires.

    # Arm 35. The include path ROTATED so the shape config dir lands LAST --
    # the pre-fix spelling, byte-for-byte in effect. Both orders elaborate
    # cleanly; only the order decides which adp_shape_defaults.svh wins.
    mut = _mutant(
        r"foreach d \$DEFINES \{ lappend DEFARGS -verilog_define \$d \}",
        "foreach d $DEFINES { lappend DEFARGS -verilog_define $d }\n"
        "set INCS [concat [lrange $INCS 1 end] [list [lindex $INCS 0]]]",
        "incdirs-reordered")
    try:
        arm(Arm("dp-mut-incdirs-reordered", None, True, tcl=mut,
            check=fires("include path is not the record's", 'reordered include path')))
    finally:
        os.unlink(mut)

    # Arm 36. The top cross-wired at the plane -- a plausible copy-paste from
    # pp_shadow_ooc.tcl, which this file calls "the same instrument". It would
    # report the PLANE's utilization as the assembled datapath's.
    mut = _mutant(r"out_of_context -top \$TOP",
                  "out_of_context -top KL_pp_shadow", "top-cross-wired")
    try:
        arm(Arm("dp-mut-top-cross-wired", None, True, tcl=mut,
            check=fires("not given the record's own top", 'cross-wired top')))
    finally:
        os.unlink(mut)

    # Arm 37. The record's defines dropped. KL_gptp_engine.sv gates
    # simulation-only $error blocks on `ifndef SYNTHESIS.
    mut = _mutant(r" \{\*\}\$DEFARGS", "", "defines-dropped")
    try:
        arm(Arm("dp-mut-defines-dropped", None, True, tcl=mut,
            check=fires("defines are not the record's", 'dropped defines')))
    finally:
        os.unlink(mut)

    # Arm 38. -sv dropped: the SystemVerilog half parsed as Verilog-2001.
    mut = _mutant(r"read_verilog -sv \$batch", "read_verilog $batch",
                  "sv-dropped")
    try:
        arm(Arm("dp-mut-sv-flag-dropped", None, True, tcl=mut,
            check=fires('read as SystemVerilog', 'dropped -sv flag')))
    finally:
        os.unlink(mut)

    # Arm 39. The part changed: an area figure is only a figure for a device.
    mut = _mutant(r"-part xc7a100tfgg484-2", "-part xc7z020clg400-1",
                  "part-changed")
    try:
        arm(Arm("dp-mut-part-changed", None, True, tcl=mut,
            check=fires('not given the ship part', 'changed part')))
    finally:
        os.unlink(mut)


def _arms_unguarded_constants(suite):
    """Arms 40-44: the geometry constants that used to reach `expr` unguarded,
    the one_source refusal, the renamed clock port, and the reports a
    refused run must not leave standing."""
    arm, dp_arm = suite.run, suite.dp_arm

    # ---- the two guards that had no arm at all ---------------------------

    # Arm 40. UPC_W_C = 0 asks for a ONE-WORD ucode image -- "the same lie as
    # an absent one" by the recipe's own contract, admitted through the single
    # geometry constant that used to reach `expr` with no guard.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UPC_W_C = 0;\n", "pkg-upc-zero")
    try:
        arm(Arm("dp-pkg-upc-zero", "not a positive ROM address width", False,
            tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 41. A zero depth would let an empty transition ROM validate.
    pkg, mut = pkg_mutant(
        "localparam int unsigned TROM_W_C = 32;\n"
        "localparam int unsigned TROM_DEPTH_C = 0;\n", "pkg-trom-depth-zero",
        which="acmp")
    try:
        arm(Arm("dp-pkg-trom-depth-zero", "not a positive ROM depth", False,
            tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 42. one_source: a record that no longer carries the geometry source
    # is a refusal, never a guessed path. No arm reached this guard before --
    # every package arm replaced the one_source call itself.
    mut = _mutant(r"one_source \$SRC_LINES ucpu_pkg\.sv",
                  "one_source $SRC_LINES no_such_pkg.sv", "one-source-missing")
    try:
        arm(Arm("dp-mut-one-source-missing", "expected exactly one no_such_pkg.sv",
            False, tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 43. The clock port renamed out from under create_clock. -quiet
    # would hand it an empty object list and define a VIRTUAL clock, so
    # timing_$TAG.rpt would report an essentially unconstrained design at
    # rc=0. The refusal is the only honest outcome.
    mut = _mutant(r"set CLK_NAME axis_clk", "set CLK_NAME renamed_clk",
                  "clock-port-renamed")
    try:
        arm(Arm("dp-mut-clock-port-renamed", "A virtual clock would report an",
            False, tcl=mut, post_synth=True))
    finally:
        os.unlink(mut)

    # Arm 44. The $TAG reports are invalidated before the FIRST refusal can
    # fire, not beside synth_design: a refused run must not leave the
    # previous run's numbers standing under the same names. The generator
    # refusal used here is upstream of synth_design, which is exactly the
    # placement the original fix got wrong and no arm observed.
    def plant_reports(d: str) -> None:
        """Stand the previous run's three $TAG reports up in the run
        directory, so a refusal that fails to invalidate them is visible."""
        for r in ("util_hier_base.rpt", "util_base.rpt", "timing_base.rpt"):
            _write(d, r, "STALE NUMBERS FROM A PREVIOUS RUN\n")

    def reports_gone(d: str, log: str) -> str | None:
        """Name whichever planted reports the refused run left standing."""
        left = sorted(r for r in ("util_hier_base.rpt", "util_base.rpt",
                                  "timing_base.rpt")
                      if (Path(d) / r).exists())
        if left:
            return ("a refused run left %s standing: the reports are the one "
                    "artifact read by hand, and nothing invalidated them"
                    % ", ".join(left))
        return None

    dp_arm(Arm("dp-refusal-invalidates-reports",
               "planted ucode generator failure",
               setup=plant_reports, check=reports_gone),
           "gen_ucode.py",
           "echo 'planted ucode generator failure' >&2\n  exit 3")


def _arms_record_and_generator_manners(suite):
    """Arms 45-49: an unrecognized record key, a severity downgrade spelled
    -suppress, a generator that warns and succeeds, and the two shapes a
    legitimate image is allowed to have."""
    arm, dp_arm = suite.run, suite.dp_arm

    # ---- guards this PR ADDED, each with an arm of its own ---------------

    # Arm 45. An unrecognized record key is a refusal: half-consuming a
    # record is how a consumer stops consuming the half that matters.
    mut = _mutant(r"exec python3 \$DP_SRCS --top \$TOP --record 2>\$REC_ERR",
                  'set _ "top=milan_datapath\\ndefine=SYNTHESIS'
                  '\\nincdir=$REPO/hdl/common\\nsrc=$REPO/x.sv\\nwat=1"',
                  "record-unknown-key")
    try:
        arm(Arm("dp-mut-record-unknown-key", "unrecognized record line", False,
            tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 46. -suppress is a downgrade that carries no -new_severity. The
    # two-option whitelist this file used to model could not see it.
    mut = _mutant(r"(set_msg_config -id \{Synth 8-4445\} -new_severity ERROR\n)",
                  "\\1set_msg_config -id {Synth 8-4445} -suppress\n",
                  "promotion-then-suppress")
    try:
        arm(Arm("dp-mut-promotion-then-suppress", None, True, tcl=mut,
            check=lambda d, log: None if EFFECTIVE_OK not in log
            else "a -suppress after the promotion still reads as ERROR"))
    finally:
        os.unlink(mut)

    # Arm 47. A generator that writes a PERFECT image, exits 0 and emits one
    # warning must not abort the run. Bare `exec` treats any stderr byte as
    # an error, which refused a good image and deleted the target first.
    dp_arm(Arm("dp-ucode-generator-warns-but-succeeds", None, expect_rc0=True),
           "gen_ucode.py",
           "%s %s -o \"$out\" > /dev/null && "
           "echo 'DeprecationWarning: planted, harmless' >&2\n  exit 0"
           % (REAL_PYTHON, GEN_UCODE))

    # Arm 48. A leading zero is DECIMAL in SystemVerilog and octal to Tcl's
    # expr. 011 must mean 11 (2,048 words), not 9 (512).
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UPC_W_C = 011;\n", "pkg-upc-octal")
    try:
        arm(Arm("dp-pkg-upc-leading-zero-is-decimal", None, True, tcl=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 49. $readmemh accepts a /* */ banner; refusing one is a false
    # refusal of a legitimate generator.
    dp_arm(Arm("dp-ucode-block-comment-banner", None, expect_rc0=True),
           "gen_ucode.py",
           "%s %s -o \"$out.b\" > /dev/null && "
           "{ printf '/* generated banner\\n   second line */\\n'; "
           "cat \"$out.b\"; } > \"$out\" && rm -f \"$out.b\"\n  exit 0"
           % (REAL_PYTHON, GEN_UCODE))


def _arms_generic_hygiene_and_order(suite):
    """Arms 56-58: an unmodelled generic, a duplicated one, and a read set
    reordered into a different compilation-unit sequence."""
    arm = suite.run

    # Arm 56. [R8]'s exact plant: a generic that structurally removes the
    # gPTP plane, passed alongside the three the model knows. The stub used
    # to `continue` past any name outside its ROM regex, so the whole suite
    # stayed green while the synthesized design changed.
    mut = _mutant(r" -generic \$GUCODE_GENERIC",
                  " -generic $GUCODE_GENERIC -generic GPTP_PLANE_EN_P=0",
                  "generic-unmodelled")
    try:
        arm(Arm("dp-mut-generic-unmodelled", "SYNTH-GENERIC-UNMODELLED", False,
            tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 57. The same generic passed twice: one value is silently the
    # winner, and which one is Vivado's business, not this recipe's.
    mut = _mutant(r" -generic \$GUCODE_GENERIC",
                  " -generic $GUCODE_GENERIC -generic $GUCODE_GENERIC",
                  "generic-duplicated")
    try:
        arm(Arm("dp-mut-generic-duplicated", "SYNTH-GENERIC-DUPLICATE", False,
            tcl=mut))
    finally:
        os.unlink(mut)

    # Arm 58. The old partition restored: every .sv first, then every .v.
    # The record is 54 .sv / 4 .v / 46 .sv and Vivado compiles in read_*
    # order, so this is a different compilation unit sequence -- invisible
    # to a set comparison, which is why the check is ordered.
    mut = _mutant(
        r"foreach f \[concat \$SRC_LINES \{\{\}\}\] \{",
        "set _sv {}; set _v {}\n"
        "foreach f $SRC_LINES {\n"
        "  if {[string match \"*.sv\" $f]} { lappend _sv $f } "
        "else { lappend _v $f }\n}\n"
        "foreach f [concat $_sv $_v {{}}] {",
        "srcs-reordered")
    try:
        arm(Arm("dp-mut-srcs-reordered", None, True, tcl=mut,
            check=fires("DIFFERENT ORDER", "reordered read set")))
    finally:
        os.unlink(mut)


def run_all(suite: Suite) -> None:
    """Every arm, in the order the review rounds built them."""
    _arms_pp_shadow_images(suite)
    _arms_datapath_generators(suite)
    _arms_synth_design_call(suite)
    _arms_geometry_parser(suite)
    _arms_derived_source_connection(suite)
    _arms_gptp_image(suite)
    _arms_what_the_tool_is_handed(suite)
    _arms_unguarded_constants(suite)
    _arms_record_and_generator_manners(suite)
    _arms_generic_hygiene_and_order(suite)

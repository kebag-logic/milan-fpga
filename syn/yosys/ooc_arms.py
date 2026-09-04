#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The arms of the ooc.sh self-test: one planted failure each.

Every function here takes the `Suite` and runs a group of arms against the
real syn/yosys/ooc.sh, using the models and the machinery in `ooc_harness.py`.
The groups are named for what they hold ooc.sh to; `run_all` is the order they
run in, and `ARMS` is how many arms that comes to - a deleted arm is a
self-test that still prints a pass, so the count is asserted by the caller in
`ooc_selftest.py`.
"""
import os
import tempfile

from ooc_harness import (
    AWK_FAIL_REPORT, Arm, CHMOD_FAIL, CHMOD_FAIL_DIRLOCK, FULL_ROW, GEN_GPTP,
    GEN_LTN, GEN_UCODE, GIT_STALE_GPTP_HEAD, GIT_STALE_HEAD, REAL_PYTHON, REPO,
    SV2V_ENV, SV2V_FAIL, SV2V_OK, Suite, YOSYS_CORRUPT_MIDRUN,
    YOSYS_EMPTY_JSON, YOSYS_ENV, YOSYS_FAIL, YOSYS_FAIL_TCAM, YOSYS_OK,
    YOSYS_TRANSIENT_SWAP, YOSYS_TWO_BLOCKS, _mutant, _mutant2,
    _preloadable_library, _processor_pins, _read_text, _run, _stub, _track,
    _write, ledger, pp_population, row_of, sv2v_plant)

#: How many arms run. A deleted arm is a self-test that still prints a pass.
ARMS = 75


def _arms_generation_and_microcode(suite):
    """Arms 1-8: the full-column positive row, the two front ends' exit status,
    and every way the microcode image can come back the wrong shape."""
    arm = suite.run

    # ---- generation, geometry, content, staging --------------------------

    # Arm 1. ANTI-VACUITY, full-width: every column of the printed row must
    # equal the model's stat block (no zeroed accumulator, no manufactured
    # row), all three ROMs generated and digest-verified into the run's own tmp
    # dir, nothing in the caller's directory.
    def clean_checks(log, ooc_tmp, home):
        row = row_of(log)
        if row is None:
            return "no row printed for the requested top"
        if row[1:] != FULL_ROW:
            return "row is not the model's stat block: got %s, want %s" \
                   % (row[1:], FULL_ROW)
        for img in ("ltn_rom.hex", "ucode.hex", "gptp_ucode.hex"):
            p = os.path.join(ooc_tmp, img)
            if not os.path.isfile(p) or os.path.getsize(p) == 0:
                return "%s was not generated into the run's tmp dir" % img
        for name in os.listdir(ooc_tmp):
            if ".run." in name:
                return "the exclusive run dir %s survived its top" % name
        return None
    arm(Arm("clean-full-columns", "tcam", None, True, check=clean_checks))

    # Arm 2. A yosys failure fails the SCRIPT, naming the top and the error.
    arm(Arm("yosys-fail", "tcam", "planted yosys elaboration failure", False,
        yosys=YOSYS_FAIL,
        check=lambda log, t, h: None if "yosys FAIL" in log
        else "the failure branch did not name the phase"))

    # Arm 3. Same for the sv2v front end.
    arm(Arm("sv2v-fail", "tcam", "planted sv2v failure", False, sv2v=SV2V_FAIL,
        check=lambda log, t, h: None if "sv2v FAIL" in log
        else "the failure branch did not name the phase"))

    # Arm 4. The microcode generator's exit status is taken, not `|| true`d.
    arm(Arm("ucode-generator-fail", "tcam", "ROM generator failed", False,
        py=("gen_ucode.py",
            "echo 'planted ucode generator failure' >&2\n  exit 3"),
        check=lambda log, t, h: None if row_of(log) is None
        else "a top was priced after the generator failed"))

    # Arms 5-8. Shape mutations for the microcode image.
    arm(Arm("ucode-empty", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", ": > \"$out\"\n  exit 0")))
    arm(Arm("ucode-one-word", "tcam", "1 words, expected exactly 2048", False,
        py=("gen_ucode.py", "printf '000000000000\\n' > \"$out\"\n  exit 0")))
    arm(Arm("ucode-truncated", "tcam", "1000 words, expected exactly 2048", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -1000 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_UCODE))))
    arm(Arm("ucode-malformed", "tcam", "not exactly 12 hex digits", False,
        py=("gen_ucode.py",
            "%s %s -o \"$out\" > /dev/null && "
            "sed -i '5s/.*/00000000000Z/' \"$out\"\n  exit 0"
            % (REAL_PYTHON, GEN_UCODE))))


def _arms_rom_content(suite):
    """Arms 9-17: a stale, a no-op-generated and a correctly shaped but
    WRONG-CONTENT image, for each of the three ROMs in turn."""
    arm = suite.run

    # Arm 9. STALE image + no-op generator; the stale image must be GONE.
    def stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ucode.hex")):
            return "the stale ucode.hex survived the refusal"
        return None
    arm(Arm("ucode-stale-noop", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", "exit 0"),
        setup=lambda t: _write(t, "ucode.hex", "STALE\n"), check=stale_gone))

    # Arm 10. [R0] round two's BLOCKER plant: a correctly SHAPED corrupt
    # image - 2,048 valid all-zero words from a "successful" generator. It
    # passes every shape gate and once priced KL_pp_shadow 4,045 LUT_TOT
    # low; only the pin-keyed content digest refuses it.
    arm(Arm("ucode-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_ucode.py",
            "%s -c \"print('\\\\n'.join(['0'*12]*2048))\" > \"$out\"\n"
            "  exit 0" % REAL_PYTHON),
        check=lambda log, t, h: None if row_of(log) is None
        else "a top was priced from a corrupt-content ROM"))

    # Arms 11-17. The transition ROM gets the SAME set, symmetrically.
    arm(Arm("ltn-generator-fail", "tcam", "ROM generator failed", False,
        py=("gen_ltn_rom.py",
            "echo 'planted ltn generator failure' >&2\n  exit 3")))
    arm(Arm("ltn-one-word", "tcam", "1 words, expected exactly 128", False,
        py=("gen_ltn_rom.py", "printf '00000000\\n' > \"$out\"\n  exit 0")))
    arm(Arm("ltn-malformed", "tcam", "not exactly 8 hex digits", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out\" > /dev/null && sed -i '2s/.*/123/' \"$out\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_LTN))))
    # 63, not 64: the generator's first line is a `//` header that rom_check
    # strips, which is exactly the kind of detail an unpinned count hides.
    arm(Arm("ltn-truncated", "tcam", "63 words, expected exactly 128", False,
        py=("gen_ltn_rom.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -64 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_LTN))))
    arm(Arm("ltn-empty", "tcam", "ltn_rom.hex is malformed", False,
        py=("gen_ltn_rom.py", ": > \"$out\"\n  exit 0")))
    def ltn_stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ltn_rom.hex")):
            return "the stale ltn_rom.hex survived the refusal"
        return None
    arm(Arm("ltn-stale-noop", "tcam", "ltn_rom.hex is malformed", False,
        py=("gen_ltn_rom.py", "exit 0"),
        setup=lambda t: _write(t, "ltn_rom.hex", "STALE\n"),
        check=ltn_stale_gone))
    arm(Arm("ltn-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_ltn_rom.py",
            "%s -c \"print('\\\\n'.join(['0'*8]*128))\" > \"$out\"\n"
            "  exit 0" % REAL_PYTHON)))

    # The gPTP microcode is independently generated, shaped and keyed to the
    # gptp-processor pin. Give it the same fail-closed generator boundary.
    arm(Arm("gptp-generator-fail", "tcam", "ROM generator failed", False,
        py=("gen_gptp_ucode.py",
            "echo 'planted gptp generator failure' >&2\n  exit 3")))
    arm(Arm("gptp-one-word", "tcam", "1 words, expected exactly 1024", False,
        py=("gen_gptp_ucode.py",
            "printf '000000000000\\n' > \"$out\"\n  exit 0")))
    arm(Arm("gptp-malformed", "tcam", "not exactly 12 hex digits", False,
        py=("gen_gptp_ucode.py",
            "%s %s -o \"$out\" > /dev/null && "
            "sed -i '2s/.*/00000000000Z/' \"$out\"\n  exit 0"
            % (REAL_PYTHON, GEN_GPTP))))
    arm(Arm("gptp-truncated", "tcam", "500 words, expected exactly 1024", False,
        py=("gen_gptp_ucode.py",
            "%s %s -o \"$out.full\" > /dev/null && "
            "head -500 \"$out.full\" > \"$out\" && rm -f \"$out.full\"\n"
            "  exit 0" % (REAL_PYTHON, GEN_GPTP))))
    arm(Arm("gptp-empty", "tcam", "gptp_ucode.hex is malformed", False,
        py=("gen_gptp_ucode.py", ": > \"$out\"\n  exit 0")))

    def gptp_stale_gone(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "gptp_ucode.hex")):
            return "the stale gptp_ucode.hex survived the refusal"
        return None

    arm(Arm("gptp-stale-noop", "tcam", "gptp_ucode.hex is malformed", False,
        py=("gen_gptp_ucode.py", "exit 0"),
        setup=lambda t: _write(t, "gptp_ucode.hex", "STALE\n"),
        check=gptp_stale_gone))
    arm(Arm("gptp-content-corrupt", "tcam", "content digest mismatch", False,
        py=("gen_gptp_ucode.py",
            "%s -c \"print('\\\\n'.join(['0'*12]*1024))\" > \"$out\"\n"
            "  exit 0" % REAL_PYTHON)))


def _arms_staging_and_ledger(suite):
    """Arms 18-22: an unknown top, the publish targets squatted, and the
    pin-keyed digest ledger (missing rows, and the record mode's round trip)."""
    problems, arm = suite.problems, suite.run

    # Arm 18. A requested top the list does not carry refuses.
    arm(Arm("unknown-top", "laneA_no_such_top", "unknown top", False))

    # Arm 19. A directory squatting the publish target: cleanup must be
    # CHECKED, not assumed ([R0] round two).
    arm(Arm("target-dir-squat", "tcam", "cannot remove the previous ucode.hex",
        False, setup=lambda t: os.makedirs(os.path.join(t, "ucode.hex"))))

    # Arm 20. [R0] round two's staging plant: files squatting predictable
    # staging names plus a no-op generator. mktemp's exclusive random name
    # ignores them; the empty stage refuses; nothing stale is published.
    def preplant_stages(t):
        _write(t, "ucode.hex.gen.%d" % os.getpid(), "STALE-STAGE\n")
        _write(t, "ucode.hex.stage.AAAAAAAA", "STALE-STAGE\n")
    def no_stale_published(log, ooc_tmp, home):
        if os.path.exists(os.path.join(ooc_tmp, "ucode.hex")):
            return "a stale staging file was published as ucode.hex"
        return None
    arm(Arm("stale-stage-preplant", "tcam", "ucode.hex is malformed", False,
        py=("gen_ucode.py", "exit 0"), setup=preplant_stages,
        check=no_stale_published))

    # Arm 21. The ledger without this pin's rows: refuse, do not guess.
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/planted-empty-ledger.tsv"',
                  "digest-ledger-detached")
    try:
        arm(Arm("digest-unrecorded-pin", "tcam", "no recorded content digest",
            False, script=mut,
            setup=lambda t: _write(t, "planted-empty-ledger.tsv", "# empty\n")))
    finally:
        os.unlink(mut)

    # Arm 22. The record mode round-trips: --record-rom-digests writes this
    # pin's rows into the (detached, scratch) ledger, and the very next run
    # against that ledger passes. Proves the pin-bump procedure works and
    # that arm 21's refusal is about the ledger's CONTENT, not a broken mode.
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "digest-ledger-scratch")
    try:
        suite.ran += 1
        with tempfile.TemporaryDirectory() as d:
            home = os.path.join(d, "home")
            rundir = os.path.join(d, "run")
            ooc_tmp = os.path.join(d, "ooc_tmp")
            bindir = os.path.join(home, ".local", "bin")
            os.makedirs(bindir)
            os.makedirs(rundir)
            os.makedirs(ooc_tmp)
            _write(ooc_tmp, "scratch-ledger.tsv", "# scratch\n")
            _stub(bindir, "sv2v", SV2V_OK)
            _stub(bindir, "yosys", YOSYS_OK)
            rc1, log1 = _run(mut, ["--record-rom-digests"], home, rundir,
                             ooc_tmp)
            rows = [l for l in _read_text(
                        os.path.join(ooc_tmp, "scratch-ledger.tsv")).splitlines()
                    if l.strip() and not l.startswith("#")]
            rc2, log2 = _run(mut, ["tcam"], home, rundir, ooc_tmp)
            if rc1 != 0 or len(rows) != 3 or rc2 != 0 \
                    or row_of(log2) is None:
                problems.append("SELF-TEST FAILED [record-mode-roundtrip]: "
                                "record rc=%d rows=%d, rerun rc=%d\n%s\n%s"
                                % (rc1, len(rows), rc2, log1.strip(),
                                   log2.strip()))
    finally:
        os.unlink(mut)


def _arms_report_phase(suite):
    """Arms 23-29: the row itself - a dead awk, a missing stat block, an
    unmapped one, the JSON artifact, two blocks, and the sticky exit."""
    arm = suite.run

    # ---- the report phase ------------------------------------------------

    # Arm 23. A dead report awk is a failed top, not a missing row.
    arm(Arm("report-awk-fail", "tcam", "planted awk report failure", False,
        awk=AWK_FAIL_REPORT,
        check=lambda log, t, h: None if "report FAIL" in log
        else "the report phase did not name itself"))

    # Arm 24. Both stat sources dropped from ooc.sh's yosys command.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten; stat;",
                  " ", "no-stat-source")
    try:
        arm(Arm("mut-no-stat-block", "tcam", "no stat block", False, script=mut))
    finally:
        os.unlink(mut)

    # Arm 25. synth_xilinx dropped, stat kept: an unmapped stat block maps
    # to zero xc7 cells, and a zero row is never a measurement.
    mut = _mutant(r" synth_xilinx -family xc7\$nodsp -top \$top -flatten;",
                  " ", "no-synth")
    try:
        arm(Arm("mut-unmapped-stat", "tcam", "zero xc7 cells", False, script=mut))
    finally:
        os.unlink(mut)

    # Arm 26. write_json dropped: the artifact must exist.
    mut = _mutant(r"; write_json \$TMP/\$top\.ooc\.json", "", "no-json")
    try:
        arm(Arm("mut-no-json", "tcam", "JSON netlist artifact", False,
            script=mut))
    finally:
        os.unlink(mut)

    # Arm 27. The artifact written EMPTY: `-e` would pass it; the run must
    # refuse ([R0] round two weakened `-s` to `-e` behind green arms).
    arm(Arm("empty-json", "tcam", "JSON netlist artifact", False,
        yosys=YOSYS_EMPTY_JSON))

    # Arm 28. TWO top blocks with different counts: last wins, no sum.
    def last_block_wins(log, ooc_tmp, home):
        row = row_of(log)
        if row is None:
            return "no row printed"
        if row[1] != "16" or row[4] != "4":
            return "row is not the last stat block (got %s)" % (row,)
        return None
    arm(Arm("two-blocks-last-wins", "tcam", None, True, yosys=YOSYS_TWO_BLOCKS,
        check=last_block_wins))

    # Arm 29. STICKY EXIT across tops ([R0] round two): the first top fails,
    # the second passes and prints its row, and the script still exits
    # non-zero. A later success must never launder an earlier failure.
    def both_outcomes(log, ooc_tmp, home):
        if "planted tcam-only failure" not in log:
            return "the failing top did not fail"
        if row_of(log, "KL_pcm_lpf") is None:
            return "the passing top printed no row"
        return None
    arm(Arm("multi-top-fail-then-pass", ["tcam", "KL_pcm_lpf"],
        "planted tcam-only failure", False, yosys=YOSYS_FAIL_TCAM,
        check=both_outcomes))


def _arms_authoritative_inputs(suite):
    """Arms 30-32: the affected tops consume the derived population, from the
    directory ooc.sh says they do."""
    arm = suite.run

    # ---- the affected tops consume the authoritative inputs ([R0] r2) ----

    # Arm 30. POSITIVE KL_pp_shadow: the sv2v model recorded exactly the
    # authoritative processor population (pp_srcs.py's own answer) plus the
    # parent's named files; the yosys model already refused to run outside
    # $OOC_TMP or without both canonical regular images in its cwd.
    def population_ok(log, ooc_tmp, home):
        rec = os.path.join(home, "sv2v-args.txt")
        if not os.path.isfile(rec):
            return "the sv2v model recorded no arguments"
        got = sorted(a for a in _read_text(rec).split()
                     if a.endswith(".sv") or a.endswith(".v"))
        if got != pp_population():
            return ("KL_pp_shadow's source set (%d files) is not the "
                    "authoritative population (%d files)"
                    % (len(got), len(pp_population())))
        if row_of(log, "KL_pp_shadow") is None:
            return "no row printed"
        return None
    arm(Arm("pp-shadow-population", "KL_pp_shadow", None, True,
        check=population_ok))

    # Arm 31. [R0] round two's plant: the derived population replaced by a
    # hand list of the two geometry packages. Geometry still resolves; the
    # population detector must distinguish, or arm 30 is vacuous. (On the
    # real tree this plant ALSO trips scripts/pp_srcs.py --check, since no
    # PROSE_OK exemption exists any more; the paths here are composed so
    # THIS tracked file is not the plant.)
    dollar_pp = "$" + "PP"
    mut = _mutant(
        r'PP_DERIVED="\$\(python3 "\$R/scripts/pp_srcs\.py" --prefix "\$PP"\)" \|\| exit 2',
        'PP_DERIVED="%s/aecp/ucpu_pkg.sv %s/acmp/pp_acmp_pkg.sv"'
        % (dollar_pp, dollar_pp), "hand-population")
    try:
        def hand_pop_detected(log, ooc_tmp, home):
            rec = os.path.join(home, "sv2v-args.txt")
            if not os.path.isfile(rec):
                return "the sv2v model recorded no arguments"
            got = sorted(a for a in _read_text(rec).split()
                         if a.endswith(".sv") or a.endswith(".v"))
            if got == pp_population():
                return "the hand-population mutant equals the record: the " \
                       "detector cannot distinguish"
            planted = sorted([
                os.path.join(REPO, "third_party", "verilog-axis", "rtl",
                             "axis_fifo.v"),
                os.path.join(REPO, "protocol-processor", "hdl", "aecp",
                             "ucpu_pkg.sv"),
                os.path.join(REPO, "protocol-processor", "hdl", "acmp",
                             "pp_acmp_pkg.sv"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_shadow.sv"),
                os.path.join(REPO, "hdl", "milan", "KL_pp_maap_shim.sv")])
            if got != planted:
                return ("the mutant's source set is neither the record nor "
                        "the planted hand list (%d files) - the arm proves "
                        "nothing about the population detector" % len(got))
            return None
        arm(Arm("mut-hand-population", "KL_pp_shadow", None, True, script=mut,
            check=hand_pop_detected))
    finally:
        os.unlink(mut)

    # Arm 32. [R0] round two's plant: cd "$rundir" -> cd "$R", restoring the
    # launch-directory dependency #245 exists to kill. The yosys model
    # refuses to run anywhere but an exclusive per-top dir under $OOC_TMP.
    # The anchor tracks ooc.sh's text and moved when the allocator preload was
    # applied inside this subshell (#290). The mutation is unchanged in meaning:
    # it still runs the synthesis somewhere other than the exclusive per-top
    # directory, and must still be caught.
    mut = _mutant(r'\(cd "\$rundir" && apply_malloc_env',
                  '(cd "$R" && apply_malloc_env', "cwd-escape")
    try:
        arm(Arm("mut-cwd-escape", "tcam", "YOSYS-WRONG-CWD", False, script=mut))
    finally:
        os.unlink(mut)


def _arms_geometry_parser(suite):
    """Arms 33-37: the microcode geometry read out of the ONE live declaration -
    comments, prefixes, duplicates, expressions and non-nibble widths."""
    arm = suite.run

    # ---- the geometry parser ([R0] round two, finding 3) -----------------

    def pkg_mutant(pkg_text, label):
        fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
        _track(pkg)
        with os.fdopen(fd, "w") as fh:
            fh.write(pkg_text)
        mut = _mutant(
            r'UCODE_W=\$\(pkg_num "\$UCPU_PKG" UCODE_W_C\)  \|\| exit 2',
            'UCODE_W=$(pkg_num "%s" UCODE_W_C)  || exit 2' % pkg, label)
        return pkg, mut

    # Arm 33. [R0]'s plant: a stale value in a comment above a live 52. The
    # LIVE value must win; with 52 the real 48-bit image no longer fits, and
    # THAT refusal proves the comment lost.
    pkg, mut = pkg_mutant(
        "// stale example: UCODE_W_C = 48\n"
        "localparam int unsigned UCODE_W_C = 52;\n", "pkg-comment-shadow")
    try:
        arm(Arm("pkg-comment-shadow-live-wins", "tcam",
            "not exactly 13 hex digits", False, script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 34. Block comments stripped and prefixed identifiers ignored: the
    # run stays WELL-FORMED at the live 48.
    pkg, mut = pkg_mutant(
        "/* stale block:\n   localparam int unsigned UCODE_W_C = 40;\n*/\n"
        "localparam int unsigned XUCODE_W_C = 99;\n"
        "localparam int unsigned UCODE_W_C  = 48;\n", "pkg-block-and-prefix")
    try:
        arm(Arm("pkg-block-comment-and-prefix", "tcam", None, True, script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 35. TWO live declarations: a refusal, never a pick.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 48;\n"
        "localparam int unsigned UCODE_W_C = 52;\n", "pkg-duplicate")
    try:
        arm(Arm("pkg-duplicate", "tcam", "exactly one live declaration", False,
            script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 36. An EXPRESSION initialiser is unsupported: refuse, not guess.
    pkg, mut = pkg_mutant(
        "localparam int unsigned OTHER_C = 12;\n"
        "localparam int unsigned UCODE_W_C = OTHER_C * 4;\n",
        "pkg-expression")
    try:
        arm(Arm("pkg-expression", "tcam", "exactly one live declaration", False,
            script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # Arm 37. A NON-NIBBLE width refuses outright ([R-parallel] round three
    # on PR #264; this script shared the truncating digit arithmetic): a
    # declared 50 would truncate to 12 digits and accept the stale 48-bit
    # image. Same guard, both scripts.
    pkg, mut = pkg_mutant(
        "localparam int unsigned UCODE_W_C = 50;\n", "pkg-width-50")
    try:
        arm(Arm("pkg-width-50-not-nibble", "tcam", "not a positive nibble-aligned",
            False, script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)


def _arms_geometry_other_roms(suite):
    """Arm 38 and the gPTP width: each ROM's geometry comes from its own owning
    package, and a changed live width invalidates the current image."""
    arm = suite.run

    # Arm 38. The transition ROM's width gets the identical guard (34 would
    # truncate to 8 digits and accept the stale 32-bit image).
    fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-pkg-")
    _track(pkg)
    with os.fdopen(fd, "w") as fh:
        fh.write("localparam int unsigned TROM_W_C = 34;\n"
                 "localparam int unsigned TROM_DEPTH_C = 128;\n")
    mut = _mutant(r'ACMP_PKG=\$\(one_pp_source pp_acmp_pkg\.sv\)  \|\| exit 2',
                  'ACMP_PKG="%s"' % pkg, "acmp-pkg-width-34")
    try:
        arm(Arm("ltn-width-34-not-nibble", "tcam", "not a positive nibble-aligned",
            False, script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)

    # The gPTP ROM geometry is independently sourced from its owning package.
    # A changed live width must invalidate the current 48-bit image.
    fd, pkg = tempfile.mkstemp(suffix=".sv", prefix=".ooc-gptp-pkg-")
    _track(pkg)
    with os.fdopen(fd, "w") as fh:
        fh.write("localparam int unsigned UCODE_W_C = 52;\n"
                 "localparam int unsigned UPC_W_C = 10;\n")
    mut = _mutant(
        r'GPTP_UCODE_W=\$\(pkg_num "\$GPTP_UCPU_PKG" UCODE_W_C\) \|\| exit 2',
        'GPTP_UCODE_W=$(pkg_num "%s" UCODE_W_C) || exit 2' % pkg,
        "gptp-pkg-width-52")
    try:
        arm(Arm("gptp-width-live-package", "tcam", "not exactly 13 hex digits",
            False, script=mut))
    finally:
        os.unlink(mut)
        os.unlink(pkg)


def _arms_consumption_custody(suite):
    """Arms 39-50: what yosys is allowed to consume - the exclusive run
    directory, the read-only copies, and the hashes on both sides of the run."""
    arm = suite.run

    # ---- consumption custody ([R0] round four) ---------------------------

    PLANTS = [
        ("ucode.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/ucode.hex"',
         "ucode.hex changed after publication"),
        ("ucode.hex", "delete", 'rm -f "$OOC_TMP/ucode.hex"',
         "ucode.hex is gone from"),
        ("ltn_rom.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/ltn_rom.hex"',
         "ltn_rom.hex changed after publication"),
        ("ltn_rom.hex", "delete", 'rm -f "$OOC_TMP/ltn_rom.hex"',
         "ltn_rom.hex is gone from"),
        ("gptp_ucode.hex", "swap",
         'printf \'SWAPPED\\n\' > "$OOC_TMP/gptp_ucode.hex"',
         "gptp_ucode.hex changed after publication"),
        ("gptp_ucode.hex", "delete", 'rm -f "$OOC_TMP/gptp_ucode.hex"',
         "gptp_ucode.hex is gone from"),
    ]

    # Arms 39-42. The published image swapped or deleted immediately AFTER
    # publication (sv2v runs between publication and the first consumption:
    # the reviewer's exact seam). The consuming copy's re-hash must refuse,
    # and no row may print.
    for img, mode, act, want in PLANTS:
        arm(Arm("%s-%s-after-publication" % (img.split(".")[0], mode), "tcam",
            want, False, sv2v=sv2v_plant("tcam", act),
            check=lambda log, t, h: None if row_of(log) is None
            else "a row was priced from unvouched bytes"))

    # Arms 43-46. The same four plants BETWEEN two requested tops: the
    # first, unaffected top prices and keeps its row; the second must
    # refuse rather than consume the changed/missing image.
    def between_check(log, ooc_tmp, home):
        if row_of(log, "tcam") is None:
            return "the first (unaffected) top printed no row"
        if row_of(log, "KL_pcm_lpf") is not None:
            return "the second top was priced from unvouched bytes"
        return None
    for img, mode, act, want in PLANTS:
        arm(Arm("%s-%s-between-tops" % (img.split(".")[0], mode),
            ["tcam", "KL_pcm_lpf"], want, False,
            sv2v=sv2v_plant("KL_pcm_lpf", act), check=between_check))

    # Arm 47. The consuming copy corrupted DURING the run (the model's own
    # exit trap): the post-run re-hash must discard whatever was measured.
    arm(Arm("ucode-corrupt-mid-run", "tcam", "changed under", False,
        yosys=YOSYS_CORRUPT_MIDRUN,
        check=lambda log, t, h: None if row_of(log) is None
        else "a row survived a mid-run byte change"))

    # Arm 48. Consumption moved back to the SHARED published directory
    # (cd "$rundir" -> cd "$TMP"): the yosys model refuses $OOC_TMP itself,
    # so the exclusive-run-dir contract cannot silently regress.
    # Same anchor move as arm 47 (#290); the mutation is unchanged in meaning.
    mut = _mutant(r'\(cd "\$rundir" && apply_malloc_env',
                  '(cd "$TMP" && apply_malloc_env', "consume-shared-dir")
    try:
        arm(Arm("mut-consume-shared-dir", "tcam", "YOSYS-WRONG-CWD", False,
            script=mut))
    finally:
        os.unlink(mut)

    # Arm 49. BOTH script-side re-hashes blinded (copy_matches always
    # true) plus the swap plant: the model's exact-byte ledger oracle is
    # the last line of defense and must go red on its own.
    mut = _mutant(r'\[ "\$got" = "\$\{ROM_SHA\[\$2\]\}" \]', "true",
                  "blind-copy-hash")
    try:
        arm(Arm("mut-blind-copy-hash", "tcam", "YOSYS-IMAGE-BYTES", False,
            script=mut,
            sv2v=sv2v_plant("tcam",
                            'printf \'SWAPPED\\n\' > "$OOC_TMP/ucode.hex"'),
            check=lambda log, t, h: None if row_of(log) is None
            else "a row was priced from unvouched bytes"))
    finally:
        os.unlink(mut)

    # Arm 50. chmod a-w dropped: the model refuses a writable consuming
    # copy, so immutability is held by an oracle, not a habit.
    mut = _mutant(r'chmod a-w "\$rundir/\$img"', ":", "writable-copy")
    try:
        arm(Arm("mut-writable-copy", "tcam", "YOSYS-IMAGE-WRITABLE", False,
            script=mut))
    finally:
        os.unlink(mut)


def _arms_read_interval(suite):
    """Arms 51-52: the transient swap, blocked on the shipping script and
    demonstrated on the mutant that forgets the directory lock."""
    arm = suite.run

    # ---- the read-interval and the pin authority ([R0] round five) -------

    # Arm 51. The transient swap on the SHIPPING script: the locked run
    # directory must refuse the rename outright, and nothing may price.
    def swap_blocked(log, ooc_tmp, home):
        if row_of(log) is not None:
            return "a row was priced around a transient-swap attempt"
        if os.path.exists(os.path.join(ooc_tmp, "transient-swap-succeeded")):
            return "the reviewed image was moved aside despite the lock"
        return None
    arm(Arm("transient-swap-blocked", "tcam", "YOSYS-TRANSIENT-SWAP-BLOCKED",
        False, yosys=YOSYS_TRANSIENT_SWAP, check=swap_blocked))

    # Arm 52. The same swap on a mutant that FORGETS the directory lock:
    # the exploit must fully succeed - reviewed bytes moved aside, wrong
    # bytes priced, reviewed bytes restored, both script hashes green, rc
    # 0. This is the reviewer's reproduction as a permanent fixture: it
    # proves arm 51's refusal is the lock's doing, not the stub's.
    mut = _mutant(r'chmod u-w "\$rundir"', "true", "no-dir-lock-swap")
    try:
        def swap_succeeded(log, ooc_tmp, home):
            if row_of(log) is None:
                return "the unlocked mutant did not price the swapped bytes"
            if not os.path.exists(os.path.join(ooc_tmp,
                                               "transient-swap-succeeded")):
                return "the swap never happened, so this arm proves nothing"
            return None
        arm(Arm("mut-no-dir-lock-transient-swap", "tcam", None, True,
            yosys=YOSYS_TRANSIENT_SWAP, script=mut, check=swap_succeeded))
    finally:
        os.unlink(mut)


def _arms_pin_authority(suite):
    """Arms 53-56: the ledger pin is the superproject gitlink, in normal and in
    record mode, for both processors."""
    arm = suite.run

    # Arm 53. The same mutant under the honest model: every green arm's
    # oracle includes the writability refusal, so forgetting the lock is
    # red even when nobody attempts a swap.
    mut = _mutant(r'chmod u-w "\$rundir"', "true", "no-dir-lock-model")
    try:
        arm(Arm("mut-no-dir-lock", "tcam", "YOSYS-RUNDIR-WRITABLE", False,
            script=mut))
    finally:
        os.unlink(mut)

    # Arms 54-55. Every chmod status is TAKEN, guard by guard: a chmod that
    # fails must be a named FATAL, never an ignored hardening. `read-only`
    # alone matched three different messages (both ooc.sh guards and the
    # yosys model's own writability refusal), so dropping the a-w status
    # still left the arm green on the u-w guard's message.
    arm(Arm("chmod-a-w-status-taken", "tcam",
        "consuming copy of ucode.hex read-only", False, chmod=CHMOD_FAIL,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced with an unenforced permission"))
    arm(Arm("chmod-u-w-status-taken", "tcam", "run directory read-only", False,
        chmod=CHMOD_FAIL_DIRLOCK,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced with an unlocked run directory"))

    # Arms 55-56. A stale submodule checkout (the dispatching git answers a
    # planted HEAD) refuses against the superproject gitlink, in normal AND
    # record mode; record mode must leave the ledger untouched.
    arm(Arm("stale-checkout-refused", "tcam",
        "disagrees with the superproject pin", False, git=GIT_STALE_HEAD,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced from a stale checkout"))
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "stale-record-ledger")
    try:
        def ledger_untouched(log, ooc_tmp, home):
            with open(os.path.join(ooc_tmp, "scratch-ledger.tsv")) as fh:
                if fh.read() != "# scratch\n":
                    return "record mode wrote rows for a stale checkout"
            return None
        arm(Arm("stale-checkout-record-refused", ["--record-rom-digests"],
            "disagrees with the superproject pin", False, script=mut,
            git=GIT_STALE_HEAD,
            setup=lambda t2: _write(t2, "scratch-ledger.tsv", "# scratch\n"),
            check=ledger_untouched))
    finally:
        os.unlink(mut)

    # The independently pinned gPTP processor has the identical authority:
    # neither normal nor record mode may certify a stale checkout.
    arm(Arm("stale-gptp-checkout-refused", "tcam",
        "gptp-processor checkout", False, git=GIT_STALE_GPTP_HEAD,
        check=lambda log, t2, h: None if row_of(log) is None
        else "a top was priced from a stale gPTP checkout"))
    mut = _mutant(r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
                  'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
                  "stale-gptp-record-ledger")
    try:
        def gptp_ledger_untouched(log, ooc_tmp, home):
            with open(os.path.join(ooc_tmp, "scratch-ledger.tsv")) as fh:
                if fh.read() != "# scratch\n":
                    return "record mode wrote rows for a stale gPTP checkout"
            return None
        arm(Arm("stale-gptp-checkout-record-refused",
            ["--record-rom-digests"], "gptp-processor checkout", False,
            script=mut, git=GIT_STALE_GPTP_HEAD,
            setup=lambda t2: _write(t2, "scratch-ledger.tsv", "# scratch\n"),
            check=gptp_ledger_untouched))
    finally:
        os.unlink(mut)


def _arms_stale_pin_false_green(suite):
    """Arm 57: the round-five false green as a fixture - a pin taken from the
    checkout prices a stale tree with every digest green."""
    arm = suite.run

    # Arm 57. The round-five false green as a fixture: pin taken from the
    # CHECKOUT (the pre-round-five spelling) plus a ledger carrying rows
    # for the stale revision - the run prices a wrong processor tree with
    # every digest green. Proves the gitlink comparison is what stands
    # between a stale checkout and a valid-looking figure.
    stale_pin = "b2effce9" * 5
    gptp_pin = _processor_pins()["gptp-processor"]
    mut = _mutant2(
        r'PP_PIN=\$\(pp_pin_of_record\) \|\| exit 2',
        'PP_PIN=$(git -C "$R/protocol-processor" rev-parse HEAD) || exit 2',
        r'DIGESTS="\$R/syn/yosys/rom_digests\.tsv"',
        'DIGESTS="${OOC_TMP}/scratch-ledger.tsv"',
        "pin-from-checkout")
    try:
        def stale_priced(log, ooc_tmp, home):
            if row_of(log) is None:
                return "the checkout-keyed mutant did not price, so this " \
                       "arm proves nothing about the gitlink comparison"
            return None
        arm(Arm("mut-pin-from-checkout-false-green", "tcam", None, True,
            script=mut, git=GIT_STALE_HEAD,
            setup=lambda t2: _write(
                t2, "scratch-ledger.tsv",
                "".join("%s\t%s\t%s\n" %
                        (gptp_pin if img == "gptp_ucode.hex" else stale_pin,
                         img, sha)
                        for img, sha in sorted(ledger().items()))),
            check=stale_priced))
    finally:
        os.unlink(mut)


def _arms_allocator_scoping(suite):
    """Arms 73-75: the allocator preload reaches yosys and nothing else, and
    YOSYS_MALLOC=none clears an inherited one for the yosys child only."""
    arm = suite.run

    # ---- allocator scoping (#290) ------------------------------------------
    # Arms 73-75. The preload is applied INSIDE the per-top yosys subshell so
    # it reaches yosys (and the abc it spawns) and nothing else; sv2v and the
    # ROM generators keep the caller's environment, and YOSYS_MALLOC=none
    # UNSETS an inherited LD_PRELOAD for the yosys child. Review [R1] proved
    # both properties by hand with a shim and then showed that a one-line
    # regression - exporting the preload once, for every child - passed
    # every arm here and the allocator self-test. These arms are that shim,
    # without a compiler: the yosys and sv2v models record the LD_PRELOAD they
    # ran under, and the fixture library is libc, which every dynamically
    # linked process already maps, so the loader takes it anywhere.
    lib = _preloadable_library()

    def _env_lines(home, name):
        try:
            with open(os.path.join(home, name)) as fh:
                return [ln.strip() for ln in fh if ln.strip()]
        except OSError:
            return []

    def scoped_to_yosys(log, ooc_tmp, home):
        y = _env_lines(home, "yosys-env.txt")
        v = _env_lines(home, "sv2v-env.txt")
        if not y or not v:
            return "the models did not run (yosys %d, sv2v %d records)" \
                   % (len(y), len(v))
        if any(x != lib for x in y):
            return "yosys ran under %s, not the selected %s" % (y, lib)
        if any(x != "<unset>" for x in v):
            return "the preload leaked to sv2v: %s" % v
        if "yosys allocator: " + lib not in log:
            return "the header does not name the selected library"
        return None

    def none_clears_child(log, ooc_tmp, home):
        y = _env_lines(home, "yosys-env.txt")
        v = _env_lines(home, "sv2v-env.txt")
        if not y or not v:
            return "the models did not run (yosys %d, sv2v %d records)" \
                   % (len(y), len(v))
        if any(x != "<unset>" for x in y):
            return "YOSYS_MALLOC=none left the inherited preload on yosys: %s" % y
        if any(x != lib for x in v):
            return "sv2v lost the caller's own environment: %s" % v
        if "yosys allocator: system" not in log:
            return "the header does not say system"
        return None

    if lib is None:
        for name in ("alloc-scoped-to-yosys", "alloc-none-clears-child",
                     "mut-alloc-exported-once"):
            print("  SKIPPED [%s]: no preloadable library on this machine "
                  "(libc.so.6 not found, or the loader refused it)" % name)
            suite.ran += 1
    else:
        # Arm 73. An explicit library reaches the yosys model and only it.
        arm(Arm("alloc-scoped-to-yosys", "tcam", None, True,
            yosys=YOSYS_ENV, sv2v=SV2V_ENV,
            env={"YOSYS_MALLOC": lib, "LD_PRELOAD": None},
            check=scoped_to_yosys))
        # Arm 74. `none` unsets an inherited preload for yosys, and for yosys
        # only: sv2v still sees what the caller exported.
        arm(Arm("alloc-none-clears-child", "tcam", None, True,
            yosys=YOSYS_ENV, sv2v=SV2V_ENV,
            env={"YOSYS_MALLOC": "none", "LD_PRELOAD": lib},
            check=none_clears_child))
        # Arm 75. The regression review planted: the preload exported once,
        # at top level, for every child. The subshell text is untouched, so
        # the cwd arms cannot see it; arm 73's check must.
        mut = _mutant(r'MALLOC_LIB="\$\(select_malloc\)" \|\| exit 2\n',
                      'MALLOC_LIB="$(select_malloc)" || exit 2\n'
                      'apply_malloc_env "$MALLOC_LIB"\n',
                      "alloc-exported-once")
        try:
            arm(Arm("mut-alloc-exported-once", "tcam", None, True, script=mut,
                yosys=YOSYS_ENV, sv2v=SV2V_ENV,
                env={"YOSYS_MALLOC": lib, "LD_PRELOAD": None},
                check=lambda log, t, h: None
                if scoped_to_yosys(log, t, h) else
                "the mutant that exports the preload for every child was "
                "not caught: sv2v ran under it unnoticed"))
        finally:
            os.unlink(mut)


def run_all(suite: Suite) -> None:
    """Every arm, in the order the review rounds built them."""
    _arms_generation_and_microcode(suite)
    _arms_rom_content(suite)
    _arms_staging_and_ledger(suite)
    _arms_report_phase(suite)
    _arms_authoritative_inputs(suite)
    _arms_geometry_parser(suite)
    _arms_geometry_other_roms(suite)
    _arms_consumption_custody(suite)
    _arms_read_interval(suite)
    _arms_pin_authority(suite)
    _arms_stale_pin_false_green(suite)
    _arms_allocator_scoping(suite)

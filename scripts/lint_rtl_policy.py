#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""lint_rtl_policy.py - what the RTL lint sweep asks for, and what it refuses
to count, with the reason and the record for every entry.

These are the POLICY TABLES of `scripts/lint_rtl.py`: the two warning codes the
sweep adds to Verilator's default set, the rules it waives whole or narrows by
predicate, the `lint_off` pragmas it accepts as justified, the files it leaves
out of the sweep, and the coded diagnostics that mean the sweep itself failed.
They are data, not machinery - nothing here reads a file, runs a tool or has an
opinion about how the sweep works - which is why they live in their own module:
a reviewer arguing about a waiver never has to read the gate, and the gate is
1000 lines shorter for it.

The tables are RE-EXPORTED by `lint_rtl`, which is where the rest of the tree
imports them from: `scripts/check_sv_idiom.py`, `scripts/check_port_contracts.py`,
`scripts/check_todo_ownership.py` and `scripts/measure_fail_fast.py` all take
`LINT_EXCLUDE` from there so that no two gates can disagree about which files
this repository is responsible for.

The rules for adding an entry are with each table. All of them come to the same
thing: a reason with no record is an opinion, and the next reader cannot check
it.
"""

#: Verilator's `--lint-only` default set is already correctness-shaped, so the
#: gate takes it whole and then adds two codes by name.  Both are cheap here
#: and neither is a style opinion:
EXTRA_WARNINGS = [
    # a signal used as BOTH an async reset and an ordinary flopped input is a
    # reset-domain question, not a style one, and this project resets
    # synchronously by house rule (CONTRIBUTING.md §1) - so every hit is a
    # deviation from the rule, and there are only five (4 in ieee1722, 1 on
    # milan_datapath's axis_resetn).
    #
    # INVESTIGATED 2026-07-27, all five, and none was fixed THEN: the finding
    # was true but the selection is an artifact, so a bulk fix looked like a
    # synthesis change bought with no evidence. THE EVIDENCE ARRIVED 2026-08-03
    # and the bulk fix LANDED - see the reset-partition note below. Kept in the
    # ratchet (NOT waived: an async reset really is a house-rule deviation, and
    # "we know it is fine" is what the ratchet is for, not RULE_WAIVERS).
    # What was found:
    #
    #  * `posedge clk_i or negedge rst_n` was NOT rare here - it was 44
    #    always_ff blocks across the then-current srp/aecp/acmp trees plus
    #    crf/aaf/common (the first three are deleted now). SYNCASYNCNET
    #    fires on 4 of them and not the other 40, purely because those 4 ALSO
    #    carry a 2-FF reset bridge into an audio/bclk domain
    #    (`xrst_n_r <= {xrst_n_r[0], rst_n}` in aaf_talker_i2s:95,
    #    KL_aaf_capture_i2s:71, KL_tdm_capture:109/120, KL_crf_tx:102). So the
    #    rule does not select "the modules with a reset problem"; it selects
    #    "the modules that also cross a clock domain".
    #
    #  * THE RESET PARTITION (2026-08-03, the missing evidence). On a 7-series
    #    SLICE the SR line is shared by all 8 FFs and its sync/async mode is a
    #    SLICE-WIDE property, so an async-reset FF can NEVER share a slice with
    #    a sync-reset one. Post-place on the AX7101 8x8 rv32 build that split
    #    was 13,040 async vs 41,253 sync registers, and the design sat at
    #    99.96 % SLICE occupancy (15,844/15,850) with LUTs at only 83.65 % -
    #    i.e. it was slice-bound, not LUT-bound, and the async/sync partition
    #    was buying that. 39 of the 44 blocks were converted to the house
    #    synchronous form; the 5 left are exactly the dual-clock modules above,
    #    where the async assert still carries the reset into a second domain
    #    whose clock can be stopped. The conversion is safe because milan_rst
    #    is AsyncResetSynchronizer-generated (async assert, SYNCHRONOUS
    #    release): the release is >= 2 clocked cycles wide, and a synchronous
    #    reset needs exactly one edge.
    #  * Both halves are individually correct for how the reset is GENERATED.
    #    axis_resetn is `~ResetSignal(cd_milan)` (sw/litex/milan_soc.py:528)
    #    and LiteX's S7PLL.create_clkout installs an AsyncResetSynchronizer:
    #    async assert, SYNCHRONOUS deassert. `negedge rst_n` is exactly the
    #    right sensitivity for that, and a 2-FF bridge is exactly the right
    #    way to carry an async-asserted reset into clk_audio/tdm_bclk.
    #  * The asymmetry that would be a defect - a dual-clock FIFO whose two
    #    sides leave reset at different times - was checked and is benign: the
    #    cdc_pair_fifo pointers are both cleared to 0, so the <=2-clock window
    #    where one side is still running only writes into a RAM that is empty
    #    by pointer comparison at both ends of it.
    #  * milan_datapath's axis_resetn hit is INHERITED, not its own: the file
    #    contains no `negedge` at all. Proved by mutation - deleting every
    #    `posedge clk_i or negedge rst_n` in hdl/ drops milan_datapath from
    #    194 findings to 193, the missing one being exactly this.
    "SYNCASYNCNET",
    # filename == module name is load-bearing here, not cosmetic: this sweep
    # (and syn/yosys/run.sh) resolve children through Verilator's `-y` library
    # search, which finds a module only by its filename.
    "DECLFILENAME",
]

# ---- RULE WAIVERS -----------------------------------------------------------
# One entry per rule that is switched OFF for the whole sweep, or narrowed:
#
#   CODE: (predicate-or-None, why this cannot be a real defect, where recorded)
#
# `predicate` is None for a whole-code waiver, or a callable
# (violation) -> bool selecting the narrow subset that is waived; anything the
# predicate does not select still counts.  The third field is the point: a
# reason with no record is an opinion, and the next reader cannot check it.
#
# Rules for adding one:
#   * the finding must be structurally impossible to be a defect - "we know it
#     is fine" is what the ratchet is for, not this table;
#   * prefer a NARROW predicate over a whole-code waiver, so the code stays
#     live everywhere else;
#   * the record must be a real file (ideally a line) a reviewer can open.


def _waive_axis_if_pins(v):
    """PINMISSING on an `axi_stream_if` instance's dead clk/rst_n ports."""
    return v.pin in ("clk", "rst_n") and "axi_stream_if" in v.source


RULE_WAIVERS = {
    "TIMESCALEMOD": (
        None,
        "a lint-only artifact, not a property of the RTL: exactly two files in "
        "hdl/ carry a `timescale (axis_mux_rr_2in_1out.sv and KL_pp_shadow.sv), "
        "and Verilator then flags all the "
        "others for not matching. A timescale has no synthesis meaning and "
        "every Verilator harness sets its own on the command line, so the 106 "
        "hits say nothing about the design",
        "hdl/common/axis_mux_rr_2in_1out.sv:7 and hdl/milan/KL_pp_shadow.sv:156 "
        "are the only two `timescale lines in hdl/; tb/verilator/*/Makefile "
        "carry the harness timescales",
    ),
    "PINMISSING": (
        _waive_axis_if_pins,
        "axi_stream_if declares clk/rst_n ports that NOTHING reads: the "
        "interface is used purely as a signal bundle, neither modport carries "
        "clk or rst_n, and no `.clk`/`.rst_n` member select of an interface "
        "instance exists anywhere in hdl/ or tb/ (grep -rnoE "
        "'[a-z_][a-z0-9_]*\\.(clk|rst_n)' returns nothing). All 53 instances "
        "are written `axi_stream_if #(...) name();` on purpose. PINMISSING "
        "stays live for every OTHER instance",
        "hdl/common/axi_stream_if.sv:14-15 (the ports) and :28-29 (the modports "
        "that omit them)",
    ),
}

# ---- PRAGMA WAIVERS ---------------------------------------------------------
# Every `verilator lint_off` that survives in the tree needs a justification for
# the same reason a tied-off input does: an unexplained suppression and an
# unexplained tie are the same defect class - a decision with no reader.
# Keyed `<path>|<CODE>`, same three fields as above.  `--pragmas` FAILS on a
# `lint_off` with no entry here, and on an entry naming a pragma that is gone.
#
# EMPTY IS A LEGITIMATE STATE (2026-08-13). Every entry this table ever held
# was an `hdl/ieee17221/aecp/**` waiver plus the milan_datapath one that
# justified the AEM_DYNMAP taps lifted off KL_aecp_top. The 1722.1/SRP control
# plane is deleted and the protocol processor stands in its place, so those
# files - and the milan_datapath pragma that pointed at them - are gone with
# it. The table is not "unused": the `--pragmas` gate below still demands a
# justification for every `lint_off` in the tree, and rejects an entry naming a
# pragma that no longer exists, so an empty table means exactly one thing -
# no file under hdl/ currently silences a Verilator warning.
PRAGMA_WAIVERS = {}

#: `hdl/` files deliberately outside the lint sweep, with the reason.  Only
#: whole FILES, never whole directories - a directory exclusion is how a scan
#: gets silently capped.
LINT_EXCLUDE = {}

#: Coded diagnostics that mean the SWEEP failed, not that the code is dirty:
#: a module the tool could not find is a setup problem, and grandfathering it
#: into a count would let the sweep quietly stop covering things.  Everything
#: else Verilator codes - including the ones it rates as errors, e.g. ENUMVALUE
#: - is a finding about the source and goes through the ratchet like any other.
ELAB_BLOCKERS = {"MODMISSING", "PKGNODECL"}

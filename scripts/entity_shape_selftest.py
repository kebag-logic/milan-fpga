#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
entity_shape_selftest.py - the mutation proof behind check_entity_shape.py.

A gate that only ever reports PASS proves nothing about the defect it was
written for. Every arm of scripts/check_entity_shape.py therefore has at
least one PLANTED WORLD here in which it must go red: a shape header beside
its includer, a build prerequisite left at the header's old path, a builder
that forgets the CRF uid, a tracked shape that is a different config's than
the one being built, a milan_csr that grows a write arm back, a config that
declares its own firmware_version.

WHY IT IS ITS OWN MODULE. The mutations and the checks they exercise are two
different subjects with two different readers, and together they made one
1338-line file. The gate module is what a build and a CI job run; this one is
read when someone asks "does that arm actually catch anything". Nothing else
imports it: `check_entity_shape.py --self-test` is the only entry.

The proofs are grouped by WHAT EACH GROUP PLANTS:

  _prove_include_ambiguity     a second copy of the header, reachable two ways
  _prove_dead_prerequisite     a consumer pointing at a path that is not there
  _prove_unresolvable_make     make expressions no static reader can settle
  _prove_frozen_expansion      immediate `:=` and rule-line expansion evasions
  _prove_builder_shape_lies    a builder computing a shape it does not emit
  _prove_tracked_shape_drift   the tracked header against the config built
  _prove_rtl_regressions       the RTL taking the shape back into its own hands
  _prove_config_defects        a config that re-declares or under-declares

Each one runs against the REAL tree, restores what it touched in a `finally`,
and requires expect_fail() to see a rejection that NAMES the arm's own
subject - a mutation caught by an unrelated check is not evidence.
"""

import os
import re
import shutil
import tempfile

import check_entity_shape as gate


def mutate(text, old, new):
    if old not in text:
        raise SystemExit(f"SELF-TEST SETUP: {old!r} not in the source")
    return text.replace(old, new, 1)


def adp_shape_of(builder, cfg):
    """This config's talker_stream_sources - read through the builder so the
    self-test never restates a count the gate exists to keep singular."""
    return builder.adp_shape(cfg)["talker_stream_sources"]


def expect_fail(label, fn, required=()):
    """Run a mutated world and require the pipeline to REJECT it.

    A rejection counts whether it comes from this gate's own comparisons or
    from the builder refusing to load the config - both stop the build.
    When required strings are supplied, the rejection must also name each
    one; a mutation caught by an unrelated check is not evidence for the arm
    it claims to exercise."""
    tally = gate.TALLY
    saved_f, saved_c, saved_q = tally.fails, tally.checks, tally.quiet
    tally.fails, tally.checks, tally.quiet = [], 0, True
    try:
        fn()
    except Exception as e:                            # noqa: BLE001
        tally.fails.append(f"{type(e).__name__}: {e}")
    if isinstance(required, str):
        required = (required,)
    reasons = "\n".join(tally.fails)
    missing = [token for token in required if token not in reasons]
    caught = bool(tally.fails) and not missing
    if missing:
        why = "rejection did not name " + ", ".join(repr(s) for s in missing)
    else:
        why = tally.fails[0] if tally.fails else ""
    tally.fails, tally.checks, tally.quiet = saved_f, saved_c, saved_q
    gate.ck(f"MUTATION rejected: {label}", caught, True)
    if caught:
        print(f"         (rejected by: {why})")


def with_rtl(dp_text=None, csr_text=None):
    """Context-manager-ish helper: swap in mutated sources for one call."""
    keep = (gate.RTL.datapath, gate.RTL.csr)
    td = tempfile.mkdtemp()
    if dp_text is not None:
        gate.RTL.datapath = os.path.join(td, "milan_datapath.sv")
        gate.write_text(gate.RTL.datapath, dp_text)
    if csr_text is not None:
        gate.RTL.csr = os.path.join(td, "milan_csr.sv")
        gate.write_text(gate.RTL.csr, csr_text)

    def restore():
        gate.RTL.datapath, gate.RTL.csr = keep
        shutil.rmtree(td, ignore_errors=True)
    return restore


def _prove_include_ambiguity(builder):
    """A byte-identical copy of the header, reachable two ways (arm H)."""
    # 0. THE AMBIGUITY CASE (arm H). Put a copy of the shape header back
    #    beside milan_csr.sv, exactly where it used to live. Nothing about
    #    the CONTENT is wrong -- the copy is byte-identical to the tracked
    #    one -- and every existing arm still passes. What is wrong is that
    #    the file is now reachable two ways, so Verilator binds the include
    #    path's copy while Vivado, yosys and sv2v bind this one, and a
    #    +incdir shape override reaches only half the design.
    adjacent = os.path.join(gate.ROOT, "hdl", "common", "csr", "gen",
                            os.path.basename(builder.ADP_SHAPE_REL))
    os.makedirs(os.path.dirname(adjacent), exist_ok=True)
    shutil.copyfile(os.path.join(gate.ROOT, builder.ADP_SHAPE_REL), adjacent)
    try:
        expect_fail("a shape header beside its includer is ambiguous",
                    gate.check_include_ambiguity)
    finally:
        os.unlink(adjacent)


def _prove_dead_prerequisite(original, stale):
    """A consumer left pointing at a path the header no longer occupies.

    Three spellings of the same defect (arm I): the plain relative path,
    the same path reached through a make FUNCTION, and a prefix that walks
    above the repository before coming back down into an existing hdl/
    tail. `original` is the untouched Makefile text, restored after each.
    """
    # 0b. THE STALE-CONSUMER CASE (arm I). Point a build prerequisite at the
    #     header's old home. Nothing about the RTL is wrong and every
    #     source-level gate stays green -- only the consumer inventory sees
    #     that the named file is gone.
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original.replace(
            "$(RTL_DIR)/common/gen/adp_shape_defaults.svh",
            "$(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh", 1))
    try:
        expect_fail("a build prerequisite left at the header's old path",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile",
                     "hdl/common/csr/gen/adp_shape_defaults.svh"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

    # 0c. [R8]'s plant on PR #310: the same stale prerequisite, reached
    #     through a make FUNCTION. The make-engine resolver expands it the
    #     way the build does -- $(shell pwd) runs -- so the verdict is the
    #     truthful one: resolved to the stale path, which is not tracked.
    shell_expr = mutate(
        original,
        "RTL_DIR    = ../../../hdl",
        "RTL_DIR    = $(shell pwd)/../../../hdl")
    shell_expr = mutate(
        shell_expr,
        "$(RTL_DIR)/common/gen/adp_shape_defaults.svh",
        "$(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(shell_expr)
    try:
        expect_fail("a make-function expression naming a dead path",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile",
                     "hdl/common/csr/gen/adp_shape_defaults.svh"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

    # 0d. [R8]'s second plant: CURDIR is a standard make variable, but this
    #     spelling walks one directory above the repository before returning
    #     to hdl/. Make resolves it exactly there, and a path outside the
    #     repository is refused whatever its tail spells.
    curdir_expr = mutate(
        original,
        "$(RTL_DIR)/common/gen/adp_shape_defaults.svh",
        "$(CURDIR)/../../../../hdl/common/gen/adp_shape_defaults.svh")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(curdir_expr)
    try:
        expect_fail("an above-repository prefix with an existing hdl tail",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)


def _prove_unresolvable_make(original, stale):
    """Make expressions that settle to no single path in the repository.

    [R8-2]'s three recurrences (arm I): an append that splits the
    prerequisite into two words, an immediate `:=` fed by a definition that
    arrives later in the same file, and an `include` that overrides the
    prefix outright. "Could not tell" must never read as "fine".
    """
    # 0e. [R8-2]'s first recurrence: `+=` after the good assignment. Make
    #     appends with a separating space, the prerequisite becomes two
    #     words, and no single path exists to bank -- the resolver must
    #     refuse rather than keep the pre-append value.
    if "RTL_DIR    = ../../../hdl" not in original:
        raise SystemExit("SELF-TEST SETUP: RTL_DIR spelling moved")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + "\nRTL_DIR += /junk\n")
    try:
        expect_fail("a += append that splits the prerequisite",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "cannot be resolved"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

    # 0f. [R8-2]'s second recurrence: an immediate := through a variable
    #     defined only LATER. Make froze the empty value at the := line, so
    #     the frozen-variable probe and the final-state text probe disagree
    #     and the reference is refused.
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + (
            "\nSHAPE_LATE := $(LATE_DIR)/common/gen/adp_shape_defaults.svh"
            "\nLATE_DIR := ../../../hdl\n"))
    try:
        expect_fail("an immediate assignment through a later definition",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "cannot be resolved"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

    # 0g. [R8-2]'s third recurrence: an include overriding the prefix.
    #     Make reads the include; the final value points nowhere inside
    #     the repository, and the resolver reports exactly that.
    shadow_mk = os.path.join(gate.ROOT, "tb/verilator/csr/shape_paths.mk")
    with open(shadow_mk, "w", encoding="utf-8") as handle:
        handle.write("RTL_DIR = /nonexistent\n")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + "\ninclude shape_paths.mk\n")
    try:
        expect_fail("an include that overrides the prefix",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)
        os.unlink(shadow_mk)


def _prove_frozen_expansion(original, stale):
    """Evasions that only make's own frozen state can catch.

    [R8-3] and [R8-4] (arm I): the late definition arrives through an
    `include` or wears an `export` prefix, so no same-file scan sees it;
    and the reference sits on a RULE line, an immediate-expansion context
    that no assignment scan or per-reference probe models at all.
    """
    # 0h. [R8-3]'s first evasion: the late definition arrives through an
    #     include, so no same-file scan can see it. The frozen-variable
    #     cross-check does: SHAPE_LATE froze the empty prefix, the text
    #     probe reads the include's final value, and they disagree.
    late_mk = os.path.join(gate.ROOT, "tb/verilator/csr/late_dir.mk")
    with open(late_mk, "w", encoding="utf-8") as handle:
        handle.write("LATE_DIR := ../../../hdl\n")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + (
            "\nSHAPE_LATE := $(LATE_DIR)/common/gen/adp_shape_defaults.svh"
            "\ninclude late_dir.mk\n"))
    try:
        expect_fail("an immediate assignment fed by an include",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "cannot be resolved"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)
        os.unlink(late_mk)

    # 0i. [R8-3]'s second evasion: the later definition wears an `export`
    #     prefix. The assignment-line pattern admits the prefix, and the
    #     frozen-variable cross-check refuses the disagreement.
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + (
            "\nSHAPE_LATE := $(LATE_DIR)/common/gen/adp_shape_defaults.svh"
            "\nexport LATE_DIR = ../../../hdl\n"))
    try:
        expect_fail("an immediate assignment fed by an exported definition",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "cannot be resolved"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)
    # 0j. [R8-4]'s evasion: the reference sits on a RULE line, an
    #     immediate-expansion context no assignment scan or reference
    #     probe models -- make froze the empty prefix into the
    #     prerequisite at parse time. The database sweep reads exactly
    #     that frozen prerequisite and refuses it.
    rule_expr = mutate(
        original,
        "obj_dir/Vcsr_sim: $(SRCS) $(GEN_CSR) $(SHAPE_DEF) sim_main.cpp",
        "obj_dir/Vcsr_sim: $(SRCS) $(GEN_CSR) "
        "$(LATE_DIR)/common/gen/adp_shape_defaults.svh sim_main.cpp")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(rule_expr + "\nLATE_DIR := ../../../hdl\n")
    try:
        expect_fail("a frozen rule prerequisite through a later definition",
                    gate.check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)


def _prove_builder_shape_lies(builder, src_cfg):
    """A builder whose computed shape contradicts the model it emits.

    The bench's own defect at the layer that now owns it (arms A-C): the
    CRF uid dropped from the talker count, the CRF sink dropped from the
    listener count, and a capability bit claimed with nothing behind it.
    """
    # 1. THE CRF CASE the bench found, at the layer that now owns it: the
    #    builder computes a talker count that excludes the CRF Media Clock
    #    Output while the AEM overlay still emits its STREAM_OUTPUT. The
    #    entity would advertise 8 sources and hold 9 descriptors, and uid 8
    #    would be un-reachable - CRF on the wire, invisible to ATDECC.
    real_shape = builder.adp_shape

    def crf_blind(cfg):
        r = dict(real_shape(cfg))
        r["talker_stream_sources"] = len(cfg["talkers"])
        return r
    builder.adp_shape = crf_blind
    try:
        expect_fail("builder's talker count excludes the CRF uid",
                    lambda: gate.check_config(builder, src_cfg))
    finally:
        builder.adp_shape = real_shape

    # 2. the CRF SINK dropped the same way (the max(N,2) asymmetry, now
    #    expressed where the shape is actually decided)
    def sink_blind(cfg):
        r = dict(real_shape(cfg))
        r["listener_stream_sinks"] = len(cfg["listeners"])
        return r
    builder.adp_shape = sink_blind
    try:
        expect_fail("builder's sink count excludes the CRF sink",
                    lambda: gate.check_config(builder, src_cfg))
    finally:
        builder.adp_shape = real_shape

    # 3. a capability with nothing behind it: MEDIA_CLOCK_SOURCE claimed by a
    #    config that has no CRF output (what the boot script did for years)
    def caps_lie(cfg):
        r = dict(real_shape(cfg))
        r["talker_capabilities"] |= 0x0800
        return r
    builder.adp_shape = caps_lie
    try:
        expect_fail("MEDIA_CLOCK_SOURCE claimed without a CRF output",
                    lambda: gate.check_config(
                        builder,
                        os.path.join(gate.CONFIG_DIR,
                                     "endstation_arty_current.yaml")))
    finally:
        builder.adp_shape = real_shape


def _prove_tracked_shape_drift(builder):
    """The tracked header against the config being built, and against its
    own declared owner (arms D and E)."""
    # 4. THE SHAPE-DRIFT DEFECT ITSELF, restated for the one artifact that is
    #    left: the tracked shape include carries config A's counts while the
    #    build is config B's. That is exactly "an 8x8 gateware shipping a 1x1
    #    shape", and it is still entirely possible - adp_shape_defaults.svh is
    #    a tracked, last-writer-wins file and `--write-rtl` hands it to
    #    whichever config it is called with.
    #
    #    (This mutation replaces the old "tracked ROM is a DIFFERENT config's
    #    than the shape" one. That mutation's subject - a second tracked
    #    entity artifact to disagree WITH - no longer exists: the AEM ROM has
    #    no RTL destination since hdl/ieee17221/aecp was deleted.)
    keep = builder.ADP_SHAPE_REL
    with tempfile.TemporaryDirectory() as td:
        other = builder.load_config(os.path.join(gate.CONFIG_DIR,
                                                 "endstation_arty_4x4.yaml"))
        adp4 = os.path.join(td, "adp_shape_defaults.svh")
        gate.write_text(adp4, builder.emit_adp_shape_svh(other))
        builder.ADP_SHAPE_REL = os.path.relpath(adp4, gate.ROOT)
        try:
            expect_fail(
                "the tree carries a DIFFERENT config's shape than the one "
                "being built",
                lambda: gate.check_built_config(
                    builder,
                    os.path.join(gate.CONFIG_DIR,
                                 "endstation_ax7101_8x8.yaml")))
        finally:
            builder.ADP_SHAPE_REL = keep

    # 4b. and the same file left STALE against its own declared owner: the
    #     `Source :` marker still names config X while the body is no longer
    #     what X generates. A shape include that lies about being current is
    #     worse than one that names nobody.
    with tempfile.TemporaryDirectory() as td:
        owner = gate.tracked_owner_cfg(builder, gate.all_configs())
        if owner is None:
            raise SystemExit("SELF-TEST SETUP: the tracked shape has no owner")
        stale = os.path.join(td, "adp_shape_defaults.svh")
        gate.write_text(stale, mutate(
            builder.emit_adp_shape_svh(owner),
            f"ADP_TALKER_SRC_C    = {adp_shape_of(builder, owner)};",
            f"ADP_TALKER_SRC_C    = {adp_shape_of(builder, owner) + 1};"))
        builder.ADP_SHAPE_REL = os.path.relpath(stale, gate.ROOT)
        try:
            expect_fail("tracked shape is STALE against the config it names",
                        lambda: gate.check_tracked_shape(builder,
                                                         gate.all_configs()))
        finally:
            builder.ADP_SHAPE_REL = keep


def _prove_rtl_regressions(builder, base_dp, base_csr):
    """The RTL taking the entity shape or the version back into its own
    hands (arms F and G)."""
    # 5. milan_csr regains a write arm for 0x618
    restore = with_rtl(csr_text=mutate(
        base_csr,
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;",
        "          A_ADP_TALK:   adp_ccaps <= s_axi_wdata;\n"
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;"))
    try:
        expect_fail("milan_csr regained a write arm for 0x618",
                    gate.check_rtl_wiring)
    finally:
        restore()

    # 6. milan_datapath stops sizing its ACMP arrays from the generated
    #    shape and computes its own again - RTL deciding the entity shape,
    #    which is how the advertised and addressable ranges drift apart
    restore = with_rtl(dp_text=mutate(
        base_dp, "localparam int ACMP_SRC_C = ADP_TALKER_SRC_C;",
        "localparam int ACMP_SRC_C = (N_STREAMS > 1) ? N_STREAMS + 1 : 1;"))
    try:
        expect_fail("milan_datapath recomputes the talker context count",
                    gate.check_rtl_wiring)
    finally:
        restore()

    # 7. THE VERSION DEFECT ITSELF: the gateware's VERSION moves and the
    #    descriptor keeps telling controllers the old number. Read the current
    #    literal out of the RTL rather than naming it - naming it here would
    #    be a second copy of exactly the constant this gate exists to keep
    #    singular. The mutation makes the VERSION arm G reads disagree with
    #    the one the model derived its firmware_version from, which is the
    #    same divergence in the same field.
    cur = re.search(r"(parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h)"
                    r"([0-9A-Fa-f_]+)", base_csr)
    if not cur:
        raise SystemExit("SELF-TEST SETUP: no VERSION parameter in milan_csr")
    restore = with_rtl(csr_text=mutate(
        base_csr, cur.group(0), cur.group(1) + "0002_0003"))
    try:
        expect_fail("milan_csr VERSION moved out from under the entity model",
                    lambda: gate.check_firmware_version(builder))
    finally:
        restore()


def _prove_config_defects(builder, base_cfg):
    """A config that answers a question it does not own, or under-declares
    the shape its gateware was built for (arms A-D and G)."""
    # 8. REMOVED, not weakened (2026-08-12): "TB golden not regenerated with
    #    the AEM ROM". It flipped one octet inside the firmware_version field
    #    of tb/verilator/aecp/aem_golden.h to prove arm G caught a stale
    #    golden. That file and the aecp Verilator suite that consumed it are
    #    DELETED, and so is the tracked ROM it was compared against - there is
    #    no second on-disk copy of the descriptor bytes left to go stale, so
    #    the mutation has no subject. Faking one (writing a golden nothing
    #    reads, just to flip a byte in it) would be a check that proves only
    #    that this file can write a file.

    # 9. a config declaring its own firmware_version - the second answer to
    #    "what version is this", which is the one controllers got for months
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "declared_fw.yaml")
        gate.write_text(p, mutate(
            base_cfg, '  serial_number: "AX7101-0001"',
            '  firmware_version: "0.1.0"\n  serial_number: "AX7101-0001"'))
        expect_fail("a config declares its own firmware_version",
                    lambda: builder.load_config(p))

    # 10. and the config itself losing a STREAM_INPUT while N_STREAMS holds
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "short_listener.yaml")
        gate.write_text(p, mutate(
            base_cfg,
            # no `formats` list since the Milan 6.4 family became derived
            # (endstation_builder.base_format_complete) rather than spelled
            # out per stream row
            '    - { name: "Stream In 7", channels: 8, map_mode: dynamic }\n',
            ""))
        # the model stays self-consistent; what breaks is the per-config
        # tracked copy on disk, which is how a config edit without a builder
        # run gets caught
        expect_fail("config edited without regenerating its shape include",
                    lambda: gate.check_config(builder, p))


def self_test():
    """Mutation proof: every planted shape disagreement must FAIL."""
    print("\n== self-test: a disagreeing shape must be REJECTED ==")
    builder = gate.load_builder()
    _prove_include_ambiguity(builder)
    stale = os.path.join(gate.ROOT, "tb/verilator/csr/Makefile")
    with open(stale, encoding="utf-8") as handle:
        original = handle.read()
    _prove_dead_prerequisite(original, stale)
    _prove_unresolvable_make(original, stale)
    _prove_frozen_expansion(original, stale)
    src_cfg = os.path.join(gate.CONFIG_DIR, "endstation_ax7101_8x8.yaml")
    base_cfg = gate.read_text(src_cfg)
    base_dp = gate.read_text(gate.RTL.datapath)
    base_csr = gate.read_text(gate.RTL.csr)
    _prove_builder_shape_lies(builder, src_cfg)
    _prove_tracked_shape_drift(builder)
    _prove_rtl_regressions(builder, base_dp, base_csr)
    _prove_config_defects(builder, base_cfg)

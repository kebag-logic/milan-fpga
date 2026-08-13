#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
lint_rtl.py - the whole-of-`hdl/` RTL lint gate (Verilator --lint-only).

WHY THIS EXISTS.  `scripts/run-verilator-lint.sh` linted the nine AECP modules
and nothing else, ran nowhere in CI and was documented nowhere, so nothing ran
it and nothing told a contributor to.  This replaces it with a sweep over every
module in `hdl/`, wired into the `rtl` workflow next to the suites.

WHY VERILATOR AND NOT VERIBLE/svlint - measured, not asserted.  The `rtl`
workflow already builds and caches a pinned Verilator 5.050 at /opt/verilator
for the suite sweep, so `--lint-only` costs one cache restore and ~10 s of
runner time: nothing extra to install, nothing extra to cache, and exactly the
version the harnesses are gated against, so a lint verdict and a suite verdict
can never disagree about what the source means.

Verible v0.0-4084 was then actually run over the same 89 files (2026-07-27):

    Verilator --lint-only     188 findings, 155 of them width (WIDTHTRUNC 74 +
                              WIDTHEXPAND 81) - the correctness meat
    Verible default rules    1004 findings, ZERO width. It has no elaborator,
                              so every one of those 155 is invisible to it

and of Verible's 1004, 916 are pure style - the largest single rule being 356
`parameter-name-style`, whose default pattern
`(([A-Z0-9]+[a-z0-9]*)+(_[0-9]+)?)` rejects essentially every parameter in the
tree because CONTRIBUTING.md §1 mandates the `_C`/`_P` suffix convention.
Adopting Verible's defaults would mean mass-renaming to its taste or waiving
its biggest rule on day one.  Turning off everything that fights the house
style leaves exactly THREE useful rules and FIFTEEN findings:
undersized-binary-literal 9, posix-eof 4, case-missing-default 2 (Verilator's
CASEINCOMPLETE already reports 1 of those 2).  Fifteen findings do not buy a
16.4 MB second toolchain, a second cache entry and a second version pin that
has to be kept in step with the suites.  Revisit if the tree adopts Verible's
naming conventions, or if a formatter (verible-verilog-format) is wanted -
that is a different job from this gate.

THE RULE THAT SHAPES THIS FILE.  A gate that only warns is worse than no gate:
`check_tied_inputs.sh` printed four warnings for months, three of them
expected, and the fourth - a tied-off `i_mac_events` that silently zeroed all
of RMON - survived precisely because a report whose warnings are mostly
expected is a report nobody reads.  So nothing here is advisory:

  * a malformed / unbalanced / unjustified `lint_off`, and a module that will
    not ELABORATE, are HARD failures, never ratcheted - see ELAB_BLOCKERS;
  * a violation COUNT above the committed per-directory ratchet
    (`scripts/lint.budget`) is a failure, and the offending violations are
    printed in full;
  * a waiver is a table entry naming the reason AND where the reason is
    recorded - the `check_tied_inputs.sh` shape - never a blanket `-Wno-`.

THE RATCHET.  Today's tree is not lint-clean and this round does not try to
make it so: rewriting RTL to please a linter is how deliberate truncations
become bugs.  `scripts/lint.budget` records the per-directory violation count
this tree is allowed to carry.  `--check` FAILS when a directory exceeds its
entry, so a NEW violation breaks the build from day one; a normal run only ever
LOWERS an entry, so paying the debt down is one commit with no argument.  The
outstanding count and its per-directory / per-code breakdown are printed on
every run: the size of the debt is never something you have to go and measure.

METHOD.  Every module declared under `hdl/` (excluding `**/doc/**`) is linted
as its own top, with the WHOLE source list on the command line each time.  The
obvious cheaper spelling - `-y hdl/...` library search - is wrong here and was
measured to be wrong: Verilator does not honour a compilation-unit-scope
`import <pkg>::*;` in a file it found through `-y`, so linting milan_datapath
that way produced 60+ bogus "Can't find definition of variable" errors out of
the then-current SRP registrar and friends, which put their import above the
module (house style; those files are deleted, the failure mode is not).
Passing the sources explicitly costs ~2 s per top and is correct.
Consequences worth knowing:

  * a module is elaborated at its DEFAULT parameters, which is why ALL 20
    SELRANGE used to be one bug: a 64-bit `s_axis.tdata` select against
    axi_stream_if's own `TDATA_WIDTH_P = 32` default (the then-current ADP
    parser 14, ptp_ts_core 5, KL_avtp_common_parser 1).  CLOSED 2026-07-27 by
    defaulting the interface to 64 - the width every one of its 53
    instantiations already passes explicitly, so no elaboration moved - which
    took the sweep from 188 to 150: SELRANGE 20 -> 0 plus 18 width findings
    that were themselves artifacts of the narrow elaboration.  It also retired
    two `lint_off SELRANGE` pragmas in the (since-deleted) AECP tree whose
    recorded justification ("the parameter default is 32") had been false since
    those modules moved to flat `input wire [63:0] s_axis_tdata` ports: they
    suppressed nothing, and removing them left the count at 150.  NOTE the hole
    that let a dead pragma sit there - this gate checks that a `lint_off` is
    well-formed, balanced and justified, but not that it still SUPPRESSES
    anything.
  * an %Error-rated code MASKS the findings behind it, so a count can go UP
    when a defect is fixed and that is not a regression.  Measured on the ADP
    parser of the day: with its uncast enum assignment in place Verilator stops
    after the ENUMVALUE error and reports 0 CASEINCOMPLETE for that file; with
    the cast it runs the later passes and reports 1 (`case (adp_state)`, no
    default).  The adp directory still fell 20 -> 6 because 15 findings went
    away, but a reviewer seeing a NEW code appear next to a fix should suspect
    unmasking before suspecting the fix.
  * a file that is `` `include ``-d by another (ethernet_packet_pkg.sv) is NOT
    also passed on the command line - that is a MODDUP, not a finding.
  * package/interface-only files declare no module, so they are linted as part
    of every run rather than as a top; `--check` FAILS if an interface file is
    instantiated by nothing (see `coverage_gaps`), so nothing escapes the sweep
    silently.
  * third_party/verilog-axis is on the `-y` path for RESOLUTION ONLY.  It is
    upstream code (alexforencich), we do not patch it, and diagnostics whose
    file lands under third_party/ are counted nowhere and waived nowhere - but
    they ARE printed, with their codes, so "excluded" never quietly becomes
    "unknown" (17 today: WIDTHTRUNC 10, WIDTHEXPAND 4, SELRANGE 3).

Run:
    scripts/lint_rtl.py                # sweep, print census, lower the ratchet
    scripts/lint_rtl.py --check        # CI gate: fail on regression, write nothing
    scripts/lint_rtl.py --pragmas      # just the `lint_off` well-formedness gate
    scripts/lint_rtl.py --self-test    # + prove a malformed pragma is rejected
    scripts/lint_rtl.py --verbose      # list every surviving violation

Exit 0 = at or under ratchet, 1 = regression / hard error, 2 = usage or setup.
"""

import argparse
import collections
import concurrent.futures
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HDL = os.path.join(ROOT, "hdl")
BUDGET = os.path.join(ROOT, "scripts", "lint.budget")
THIRD_PARTY = "third_party/"

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
        "a lint-only artifact, not a property of the RTL: exactly two of the 95 "
        "files in hdl/ carry a `timescale (axis_mux_rr_2in_1out.sv and the "
        "Zynq-only milan_dma_wrapper.v), and Verilator then flags all the "
        "others for not matching. A timescale has no synthesis meaning and "
        "every Verilator harness sets its own on the command line, so the 106 "
        "hits say nothing about the design",
        "hdl/common/axis_mux_rr_2in_1out.sv:7 and hdl/milan/milan_dma_wrapper.v:18 "
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
        "stays live for every OTHER instance - the 116 hits in milan_top.sv "
        "are counted, not waived",
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
LINT_EXCLUDE = {
    "hdl/milan/milan_dma_wrapper.v": (
        "Verilog-2001 shim around the Xilinx AXI DMA PS primitives; it is part "
        "of the Zynq flow only, no fabric build compiles it, and the `milan_dma` "
        "IP core it instantiates is not in this repository at all",
        "sw/litex/milan_soc.py:640 - 'Zynq-only milan_top.sv / "
        "milan_dma_wrapper.v are excluded from the fabric build'",
    ),
    "hdl/milan/milan_top.sv": (
        "the Zynq top. It cannot ELABORATE here, not merely lint dirty: it "
        "instantiates eth_mac_1g_rgmii_fifo, which lives in the `external/` "
        "submodule (an SSH remote CI does not and cannot fetch), and milan_dma, "
        "which is Xilinx IP absent from the tree. It is in no build: "
        "syn/yosys/run.sh's tops end at milan_datapath and the fabric flow "
        "excludes it by name. NOTE for whoever revives it - the 2026-07 reading, "
        "linting it against a checked-out external/, was 116 PINMISSING (91 on "
        "its milan_csr instance, 24 on the AECP top it wired, 1 on ptp_ts_top). "
        "That AECP top no longer exists, so the drift is now strictly worse than "
        "that number: it wires a control plane this repository deleted",
        "sw/litex/milan_soc.py:640 and .gitmodules (submodule 'external' = "
        "git@github.com:kebag-logic/fpga-avb-ethernet.git)",
    ),
}

#: Coded diagnostics that mean the SWEEP failed, not that the code is dirty:
#: a module the tool could not find is a setup problem, and grandfathering it
#: into a count would let the sweep quietly stop covering things.  Everything
#: else Verilator codes - including the ones it rates as errors, e.g. ENUMVALUE
#: - is a finding about the source and goes through the ratchet like any other.
ELAB_BLOCKERS = {"MODMISSING", "PKGNODECL"}

# ---- pragma well-formedness -------------------------------------------------
# The 2026 scar this gate must be able to catch: a trailing `//` comment after
# the waiver code
#
#     // verilator lint_off SELRANGE  // prose about why
#
# is TOLERATED by 5.050 and REJECTED by 5.020, and it made four suites
# unbuildable.  A lint gate that cannot catch a broken lint pragma has an
# obvious hole, so this is a HARD failure and never ratcheted: it breaks
# builds on other Verilator versions, which no violation count can express.
PRAGMA_RE = re.compile(r"verilator\s+lint_(off|on|save|restore)\b")
#: the ONLY accepted shapes.  Note `lint_on  UNUSED` (extra spaces) is fine;
#: anything after the code is not.
PRAGMA_OK_RE = re.compile(
    r"^\s*(?://|/\*)\s*verilator\s+lint_(?:off|on)\s+([A-Z][A-Z0-9_]*)\s*(?:\*/)?\s*$"
)
PRAGMA_BARE_RE = re.compile(r"^\s*(?://|/\*)\s*verilator\s+lint_(?:save|restore)\s*(?:\*/)?\s*$")


class Violation(object):
    """One deduplicated Verilator diagnostic."""

    __slots__ = ("code", "path", "line", "col", "msg", "source", "pin")

    def __init__(self, code, path, line, col, msg, source):
        self.code = code
        self.path = path
        self.line = line
        self.col = col
        self.msg = msg
        self.source = source
        m = re.search(r"missing pin: '(\w+)'", msg)
        self.pin = m.group(1) if m else ""

    @property
    def key(self):
        return (self.path, self.line, self.col, self.code)

    @property
    def bucket(self):
        """Ratchet bucket = the directory the offending file lives in."""
        return os.path.dirname(self.path)

    def __str__(self):
        return "%s:%s:%s: %s  %s" % (self.path, self.line, self.col,
                                     self.code, self.msg)


def hdl_files(exts=(".sv",)):
    """Every `hdl/` source of the given extensions, doc/ trees excluded."""
    out = []
    for base, dirs, files in os.walk(HDL):
        dirs[:] = [d for d in dirs if d != "doc"]
        for f in sorted(files):
            if f.endswith(exts):
                out.append(os.path.relpath(os.path.join(base, f), ROOT))
    return sorted(out)


def submodule_sources():
    """The protocol-processor submodule's RTL, as SOURCES only.

    `hdl/milan/KL_pp_shadow.sv` instantiates `protocol_processor_top`, which
    lives in the submodule and therefore is not in `hdl_files()`. Without it
    every sweep reported a hard MODMISSING for that top - an %Error-rated code,
    so it also MASKED whatever findings sat behind it in that file.

    These are appended as sources and NEVER added to the lint task list: the
    submodule is linted by its own gate at its own ratchet, and re-linting it
    here would import another repository's debt into this one's budget.
    Packages first, for the same compilation-unit reason as above.
    """
    root = os.path.join(ROOT, "protocol-processor", "hdl")
    if not os.path.isdir(root):
        return []                     # submodule not initialised: not our gate
    pkg, mod = [], []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ("doc", "rom")]
        for f in sorted(files):
            if not f.endswith(".sv"):
                continue
            rel = os.path.relpath(os.path.join(base, f), ROOT)
            (pkg if f.endswith("_pkg.sv") else mod).append(rel)
    return sorted(pkg) + sorted(mod)


def include_dirs():
    """`-I` roots for `` `include ``: every hdl directory.

    The ENTITY SHAPE comes first. Lint elaborates every module at its DEFAULT
    parameters, and milan_datapath defaults to N_STREAMS = 1, so it must see
    the 1x1 entity definition - not whichever config was last written into
    hdl/common/csr/gen/ by `endstation_builder.py --write-rtl`. Regenerating
    the tree for the 8x8 ship shape otherwise lints a 1-stream datapath
    against a 9-source entity, which milan_datapath's elaboration guard
    correctly rejects (and which, before that guard existed, showed up only
    as UNDRIVEN talker DMAC/VID bits). Same rule as the testbenches: name the
    shape you are elaborating, and put it ahead of hdl/common/csr.
    """
    dirs = [os.path.join("configs", "generated", "endstation_arty_current")]
    for base, sub, _ in os.walk(HDL):
        sub[:] = [d for d in sub if d != "doc"]
        dirs.append(os.path.relpath(base, ROOT))
    return dirs[:1] + sorted(dirs[1:])


def axis_lib():
    """verilog-axis `-y` root - RESOLUTION ONLY, never linted (see module doc)."""
    axis = os.path.join(ROOT, "third_party", "verilog-axis", "rtl")
    return os.path.relpath(axis, ROOT) if os.path.isdir(axis) else None


INCLUDE_RE = re.compile(r'^\s*`include\s+"([^"]+)"', re.M)


def included(files):
    """Basenames pulled in by `` `include `` - passing them on the command line
    as well would define their modules twice (MODDUP)."""
    out = set()
    for rel in files:
        for inc in INCLUDE_RE.findall(open(os.path.join(ROOT, rel)).read()):
            out.add(os.path.basename(inc))
    return out


DECL_RE = re.compile(r"^\s*(module|package|interface)\s+([A-Za-z_]\w*)", re.M)


def declarations():
    """(file -> [(kind, name), ...]) for every linted `hdl/` source."""
    out = {}
    for rel in hdl_files((".sv",)):
        if rel in LINT_EXCLUDE:
            continue
        text = open(os.path.join(ROOT, rel)).read()
        # Strip comments before the declaration search.  A banner line that
        # happens to begin with the word "module" is prose, not a design unit,
        # and handing its next word to --top-module fails elaboration outright
        # ("module at all" in KL_chan_map_capture's queue banner did exactly
        # that).  docs/traceability/gen_module_matrix.py carries the same guard
        # for the same reason.
        scan = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        scan = re.sub(r"//.*", "", scan)
        out[rel] = DECL_RE.findall(scan)
    return out


def packages(decls):
    """Package-only files.  Verilator's `-y` library search resolves MODULES
    and INTERFACES by filename but NOT `import <pkg>::*`, so every package is
    handed to every lint run explicitly - which also means the packages
    themselves are linted rather than merely parsed."""
    return sorted(rel for rel, ds in decls.items()
                  if ds and all(k == "package" for k, _ in ds))


def coverage_gaps(decls):
    """Files that no lint run would reach.  A module file is linted directly, a
    package file is preloaded into every run; an INTERFACE file is pulled in
    only by `-y` when something instantiates it, so prove something does.
    Without this, an unreferenced file could sit in the tree completely
    unlinted while the sweep still reported success - a silently capped scan."""
    bodies = {rel: open(os.path.join(ROOT, rel)).read() for rel in decls}
    pkgs = set(packages(decls))
    gaps = []
    for rel, ds in sorted(decls.items()):
        if any(k == "module" for k, _ in ds) or rel in pkgs:
            continue
        if not ds:
            gaps.append((rel, "declares no module, package or interface"))
            continue
        for kind, name in ds:
            users = [o for o, b in bodies.items()
                     if o != rel and re.search(r"\b%s\b" % re.escape(name), b)]
            if not users:
                gaps.append((rel, "%s %s is instantiated by nothing" % (kind, name)))
    return gaps


DIAG_RE = re.compile(r"^%(Warning|Error)-([A-Z][A-Z0-9_]*): (\S+?):(\d+):(\d+): (.*)$")
HARD_RE = re.compile(r"^%Error(?!: Exiting due to)")


def lint_one(mod, incdirs, sources, verilator):
    """Lint `mod` as a top; return (raw stdout, [Violation], [hard error])."""
    cmd = [verilator, "--lint-only", "--sv", "--top-module", mod]
    for w in EXTRA_WARNINGS:
        cmd.append("-Wwarn-" + w)
    for d in incdirs:
        cmd.append("-I" + d)
    axis = axis_lib()
    if axis:
        cmd += ["-y", axis]
    cmd += sources
    p = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, universal_newlines=True)
    lines = p.stdout.split("\n")
    vios, hard = [], []
    for i, ln in enumerate(lines):
        m = DIAG_RE.match(ln)
        if m:
            kind, code, path, line, col, msg = m.groups()
            # the offending SOURCE line, which Verilator echoes as `NNN | text`
            # a line or three below - MULTIDRIVEN and friends slip a
            # `... note: In instance` line in between. Waiver predicates read
            # this, so take the first real echo, not merely the next line.
            src = ""
            for ln2 in lines[i + 1:i + 5]:
                m2 = re.match(r"^\s*\d+\s*\|\s?(.*)$", ln2)
                if m2:
                    src = m2.group(1).strip()
                    break
            v = Violation(code, path, line, col, msg, src)
            # Findings inside the protocol-processor submodule are NOT this
            # tree's debt: it is linted by its own gate at its own ratchet, and
            # counting it here would move this budget every time that pin
            # advances. Its sources are on the command line only so our tops
            # can find `protocol_processor_top` (see submodule_sources).
            if v.path.startswith("protocol-processor/"):
                continue
            if code in ELAB_BLOCKERS:
                hard.append("%s (linting %s)" % (v, mod))
            else:
                vios.append(v)
        elif HARD_RE.match(ln):
            hard.append("%s (linting %s)" % (ln.strip(), mod))
    return p.stdout, vios, hard


def sweep(verilator, jobs):
    """Lint every module as its own top, in parallel.

    Returns (declarations, deduped violations, hard errors, n_lints).  The
    dedup key is (file, line, col, code): a leaf module is elaborated both on
    its own and inside every parent, so the same finding arrives many times and
    must be counted once or the ratchet would move with the hierarchy."""
    decls = declarations()
    incdirs = include_dirs()
    inc = included(decls)
    pkgs = packages(decls)
    # packages first: a compilation-unit `import` must see them declared
    sources = ([p for p in pkgs if os.path.basename(p) not in inc]
               + [r for r in sorted(decls)
                  if r not in pkgs and os.path.basename(r) not in inc]
               + submodule_sources())
    tasks = [name for rel, ds in sorted(decls.items())
             for kind, name in ds if kind == "module"]
    vios, hard = {}, []
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = {ex.submit(lint_one, m, incdirs, sources, verilator): m
                for m in tasks}
        for f in concurrent.futures.as_completed(futs):
            _, vv, hh = f.result()
            hard += hh
            for v in vv:
                vios.setdefault(v.key, v)
    return decls, list(vios.values()), sorted(set(hard)), len(tasks)


def apply_waivers(vios):
    """Split into (counted, waived, external) - external being third_party."""
    counted, waived, external = [], [], []
    for v in vios:
        if v.path.startswith(THIRD_PARTY) or "/third_party/" in v.path:
            external.append(v)            # upstream code, not ours to lint
            continue
        rule = RULE_WAIVERS.get(v.code)
        if rule is not None:
            pred = rule[0]
            if pred is None or pred(v):
                waived.append(v)
                continue
        counted.append(v)
    return counted, waived, external


# ---- pragma gate ------------------------------------------------------------

def known_codes(verilator, codes):
    """Codes Verilator 5.050 actually knows (asked, never assumed)."""
    bad = []
    for c in sorted(codes):
        p = subprocess.run([verilator, "--lint-only", "-Wno-" + c, "--version"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           universal_newlines=True)
        if "Unknown warning" in p.stdout:
            bad.append(c)
    return bad


def check_pragmas(verilator, files=None, root=None):
    """Well-formedness + balance + justification of every in-tree lint pragma.

    Returns (findings, seen) where `seen` is the set of `<path>|<CODE>` keys."""
    root = root or ROOT
    files = files if files is not None else hdl_files((".sv", ".svh", ".v"))
    findings, seen, codes = [], set(), set()
    for rel in files:
        depth = collections.Counter()
        for n, ln in enumerate(open(os.path.join(root, rel)), 1):
            if not PRAGMA_RE.search(ln):
                continue
            if PRAGMA_BARE_RE.match(ln):
                continue
            m = PRAGMA_OK_RE.match(ln)
            if not m:
                findings.append(
                    "%s:%d: MALFORMED lint pragma - the waiver code must be the "
                    "LAST token on the line (5.050 tolerates trailing prose, "
                    "5.020 rejects it and the file stops building):\n"
                    "        %s" % (rel, n, ln.rstrip()))
                continue
            code = m.group(1)
            codes.add(code)
            if "lint_off" in ln:
                depth[code] += 1
                key = "%s|%s" % (rel, code)
                seen.add(key)
                if key not in PRAGMA_WAIVERS:
                    findings.append(
                        "%s:%d: UNJUSTIFIED `lint_off %s` - add a "
                        "PRAGMA_WAIVERS entry (why | where the reason is "
                        "recorded) in %s, or delete the pragma."
                        % (rel, n, code, os.path.relpath(__file__, root)))
            else:
                depth[code] -= 1
                if depth[code] < 0:
                    findings.append("%s:%d: `lint_on %s` with no open lint_off"
                                    % (rel, n, code))
        for code, d in sorted(depth.items()):
            if d > 0:
                findings.append(
                    "%s: `lint_off %s` never closed - it leaks to the end of "
                    "the file and silences code nobody looked at" % (rel, code))
    for key in sorted(PRAGMA_WAIVERS):
        if key not in seen:
            findings.append("STALE PRAGMA_WAIVERS entry '%s': that file no "
                            "longer carries that lint_off" % key)
    if codes:
        bad = known_codes(verilator, codes)
        for c in bad:
            findings.append("unknown warning code '%s' in a lint pragma - "
                            "Verilator does not know it, so the pragma "
                            "silences nothing" % c)
    return findings, seen


# ---- ratchet ----------------------------------------------------------------

BUDGET_HDR = [
    "# GENERATED by scripts/lint_rtl.py - the RTL lint ratchet: the largest",
    "# number of Verilator --lint-only violations each hdl/ directory may",
    "# carry. A normal run only ever LOWERS an entry; --check FAILS when a",
    "# directory exceeds it, so a NEW violation breaks the build even though",
    "# today's backlog is grandfathered. Lowering one is a normal commit:",
    "#     scripts/lint_rtl.py && git add scripts/lint.budget",
    "# Waived rules and the reasons are the tables in scripts/lint_rtl.py.",
]


def read_budget():
    """{directory: allowance}, or None when the file is missing."""
    if not os.path.exists(BUDGET):
        return None
    out = {}
    for line in open(BUDGET):
        s = line.split("#", 1)[0].strip()
        if not s:
            continue
        d, n = s.rsplit(None, 1)
        out[d] = int(n)
    return out


def write_budget(counts, per_code=None):
    width = max([len(d) for d in counts] or [1])
    #: the debt is legible from the committed file alone - a reader should
    #: never have to run the sweep to find out how big the backlog is or what
    #: it is made of.
    tail = ["#", "# total %d across %d director(y/ies)"
            % (sum(counts.values()), len([1 for n in counts.values() if n]))]
    if per_code:
        tail.append("# by rule: " + ", ".join("%s %d" % (c, n)
                                              for c, n in ranked(per_code)))
    body = ["%-*s  %d" % (width, d, n) for d, n in sorted(counts.items())]
    content = "\n".join(BUDGET_HDR + tail + [""] + body) + "\n"
    cur = open(BUDGET).read() if os.path.exists(BUDGET) else None
    if cur != content:
        open(BUDGET, "w").write(content)
    return cur != content


# ---- self-test --------------------------------------------------------------

SELF_TEST_CASES = [
    # (filename, body, must-be-rejected, what it proves)
    ("bad_trailing.sv",
     "// verilator lint_off SELRANGE  // prose Verilator 5.020 chokes on\n"
     "// verilator lint_on  SELRANGE\n",
     True, "the 5.020 trailing-prose scar"),
    ("bad_block.sv",
     "/* verilator lint_off UNUSED */ wire x;\n"
     "/* verilator lint_on  UNUSED */\n",
     True, "a block comment with code after the pragma"),
    ("bad_unclosed.sv",
     "// verilator lint_off WIDTHTRUNC\n",
     True, "a lint_off that leaks to end of file"),
    ("bad_unknown.sv",
     "// verilator lint_off NOTACODE\n"
     "// verilator lint_on  NOTACODE\n",
     True, "a waiver code Verilator does not know"),
    ("bad_orphan_on.sv",
     "// verilator lint_on  UNUSED\n",
     True, "a lint_on with no matching lint_off"),
    ("good.sv",
     "// verilator lint_off UNUSED\n"
     "wire unused = 1'b0;\n"
     "// verilator lint_on  UNUSED\n",
     False, "the well-formed shape the tree already uses"),
]


def self_test(verilator):
    """Mutation-prove the pragma gate: malformed pragmas MUST be rejected."""
    import tempfile
    rc = 0
    with tempfile.TemporaryDirectory() as td:
        for name, body, must_fail, what in SELF_TEST_CASES:
            open(os.path.join(td, name), "w").write(body)
            saved = dict(PRAGMA_WAIVERS)
            # the good case needs its justification, exactly like the tree does
            PRAGMA_WAIVERS["good.sv|UNUSED"] = ("self-test fixture", "this file")
            try:
                found, _ = check_pragmas(verilator, files=[name], root=td)
            finally:
                PRAGMA_WAIVERS.clear()
                PRAGMA_WAIVERS.update(saved)
            found = [f for f in found if not f.startswith("STALE")]
            ok = bool(found) == must_fail
            print("  [self-test] %-16s %-8s %s (%s)"
                  % (name, "REJECT" if must_fail else "ACCEPT",
                     "OK" if ok else "FAILED", what))
            if not ok:
                rc = 1
                for f in found:
                    print("        unexpected: %s" % f.replace("\n", " "))
    return rc


# ---- reporting --------------------------------------------------------------

def ranked(counter):
    """Counter -> [(key, n)] sorted by count then key.  `most_common()` keeps
    INSERTION order for ties, and the sweep is threaded, so using it would make
    the `by rule` line in the committed budget file reorder itself at random -
    a spurious diff on a generated artifact."""
    return sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))


def census(vios):
    per_dir = collections.Counter(v.bucket for v in vios)
    per_code = collections.Counter(v.code for v in vios)
    return per_dir, per_code


def print_census(counted, waived, external, budget, n_lints):
    per_dir, per_code = census(counted)
    print("== hdl/ Verilator lint census (%d module elaborations) ==" % n_lints)
    width = max([len(d) for d in per_dir] or [24])
    for d, n in sorted(per_dir.items()):
        b = budget.get(d) if budget else None
        tag = "" if b is None else ("  <= ratchet %d" % b if n <= b
                                    else "  > RATCHET %d" % b)
        print("  %-*s %4d%s" % (width, d, n, tag))
    clean = sorted(set(budget or {}) - set(per_dir))
    for d in clean:
        print("  %-*s %4d  (was %d)" % (width, d, 0, budget[d]))
    print("  %-*s %4d" % (width, "TOTAL", len(counted)))
    print("  by rule: " + ", ".join("%s %d" % (c, n)
                                    for c, n in ranked(per_code)))
    if waived:
        wd = collections.Counter(v.code for v in waived)
        print("  waived (RULE_WAIVERS, reasons in %s): %s"
              % (os.path.relpath(__file__, ROOT),
                 ", ".join("%s %d" % (c, n) for c, n in ranked(wd))))
    if external:
        ed = collections.Counter(v.code for v in external)
        print("  third_party (upstream verilog-axis - resolved, never linted, "
              "not ours to fix): %s"
              % ", ".join("%s %d" % (c, n) for c, n in ranked(ed)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1],
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="CI gate: fail on regression, never write the budget")
    ap.add_argument("--pragmas", action="store_true",
                    help="only the lint_off well-formedness / justification gate")
    ap.add_argument("--self-test", action="store_true",
                    help="prove the pragma gate rejects a malformed pragma")
    ap.add_argument("--verbose", "-v", action="store_true",
                    help="list every surviving violation")
    ap.add_argument("--jobs", "-j", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--verilator", default=os.environ.get("VERILATOR", "verilator"))
    a = ap.parse_args()

    verilator = shutil.which(a.verilator) or a.verilator
    if not shutil.which(a.verilator):
        print("lint_rtl: no verilator on PATH (VERILATOR=<path> overrides)",
              file=sys.stderr)
        return 2

    rc = 0
    if a.self_test:
        rc |= self_test(verilator)

    print("== lint pragma gate (well-formed · balanced · justified) ==")
    findings, seen = check_pragmas(verilator)
    for f in findings:
        print("  [FAIL] " + f)
    if findings:
        print("PRAGMA GATE: FAIL - %d finding(s). Never ratcheted: a malformed "
              "pragma stops OTHER Verilator versions building the file (which "
              "no violation count can express), and an unexplained lint_off is "
              "the same defect class as an unexplained tied-off input."
              % len(findings))
        rc = 1
    else:
        print("PRAGMA GATE: PASS (%d justified lint_off, %d excluded file(s))"
              % (len(seen), len(LINT_EXCLUDE)))
    # --self-test composes with --check (that is how CI runs it); on its own it
    # is the fast pragma-only mode.
    if a.pragmas or (a.self_test and not a.check):
        return rc

    decls = declarations()
    gaps = coverage_gaps(decls)
    for rel, why in gaps:
        print("  [FAIL] %s: %s - it would be linted by nobody" % (rel, why))
    if gaps:
        print("LINT COVERAGE: FAIL - %d file(s) reachable by no lint run." % len(gaps))
        rc = 1

    decls, vios, hard, n_lints = sweep(verilator, a.jobs)
    counted, waived, external = apply_waivers(vios)
    for h in hard:
        print("  [ERROR] " + h)
    if hard:
        print("ELABORATION: FAIL - %d Verilator error(s). Never ratcheted: a "
              "module that will not elaborate is a broken build, not a lint "
              "finding." % len(hard))
        rc = 1

    budget = read_budget()
    print_census(counted, waived, external, budget or {}, n_lints)
    per_dir, _ = census(counted)

    # The backlog is printed IN FULL on every gated run. A ratchet that hides
    # what it is grandfathering is a silent cap, and a reader of this log must
    # be able to see the whole debt without going and running the sweep.
    if counted and (a.verbose or a.check):
        over = {d for d, n in per_dir.items() if n > (budget or {}).get(d, 0)}
        print("-- outstanding backlog: %d violation(s) --" % len(counted))
        for v in sorted(counted, key=lambda v: (v.path, int(v.line))):
            print("  %s%s" % ("NEW " if v.bucket in over else "", v))

    if a.check:
        if budget is None:
            print("LINT GATE: FAIL - %s is missing; run scripts/lint_rtl.py "
                  "once to record the baseline." % os.path.relpath(BUDGET, ROOT))
            return 1
        bad = sorted(d for d, n in per_dir.items() if n > budget.get(d, 0))
        if bad:
            for d in bad:
                print("LINT REGRESSION: %s has %d violation(s), ratchet allows %d"
                      % (d, per_dir[d], budget.get(d, 0)))
            print("  Fix it, or - if the finding is structurally impossible to")
            print("  be a defect - add a RULE_WAIVERS entry naming the reason")
            print("  AND where the reason is recorded. Raising the ratchet is")
            print("  not an option: it only ever goes down.")
            return 1
        low = sorted(d for d in budget if per_dir.get(d, 0) < budget[d])
        tot = sum(budget.values())
        print("LINT GATE: PASS (%d violation(s) <= ratchet %d; %d waived, "
              "%d justified lint_off)" % (len(counted), tot, len(waived), len(seen)))
        if low:
            print("  ratchet can be tightened in: %s  (run scripts/lint_rtl.py)"
                  % ", ".join(sorted(set(low))))
        return rc

    _, per_code = census(counted)
    if rc:
        return rc
    if budget is None:
        write_budget(per_dir, per_code)
        print("lint ratchet recorded: %d violation(s) across %d director(y/ies)"
              % (len(counted), len(per_dir)))
        return 0
    # A normal run only ever LOWERS an entry. A directory over its allowance is
    # reported and left alone: raising the ratchet is not something a tool gets
    # to do quietly, and --check will fail on it until someone deals with it.
    new, tightened, over = dict(budget), [], []
    for d in sorted(set(budget) | set(per_dir)):
        n, cur = per_dir.get(d, 0), budget.get(d, 0)
        if n < cur:
            tightened.append("%s %d -> %d" % (d, cur, n))
        elif n > cur:
            over.append("%s %d > %d" % (d, n, cur))
        new[d] = min(n, cur) if d in budget else 0
    for o in over:
        print("WARNING: %s violation(s) exceeds the ratchet - --check will FAIL" % o)
    if over:
        return 1
    # always rewrite when the CONTENT moved: the by-rule line in the header is
    # part of what makes the debt readable from the committed file alone, so it
    # must not go stale just because no directory count happened to change.
    rewrote = write_budget(new, per_code)
    if tightened:
        print("lint ratchet tightened: " + "; ".join(tightened))
    elif rewrote:
        print("lint ratchet unchanged (%d violation(s) <= %d); budget header "
              "refreshed" % (len(counted), sum(budget.values())))
    else:
        print("lint ratchet unchanged (%d violation(s) <= %d)"
              % (len(counted), sum(budget.values())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

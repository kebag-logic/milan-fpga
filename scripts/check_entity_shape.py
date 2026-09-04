#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""
check_entity_shape.py - the advertised-shape gate.

WHY THIS EXISTS.  An end station tells every controller on the segment how many
streams it has in exactly three places, and all three have to be the same
number:

  1. the ADPDU it broadcasts - talker_stream_sources / listener_stream_sinks,
     served by milan_csr at 0x618 / 0x61C;
  2. its AEM descriptor set - the STREAM_OUTPUT / STREAM_INPUT descriptors a
     controller can actually READ_DESCRIPTOR and bind;
  3. the gateware that was built - the ACMP source/sink contexts that answer
     CONNECT_TX / BIND_RX, sized by N_STREAMS at elaboration.

On 2026-07-27 they were three different numbers.  0x618 and 0x61C were plain
RW registers resetting to ZERO, so the advertised counts came from two
hand-typed lines in a boot script:

    w 0x618 0x48010001   # 1 implemented stream (honest count, Milan strict)
    w 0x61C 0x48010002   # 2 STREAM_INPUTs (media + CRF desc)

That comment was true at 1x1 and became false the day the board went 8x8.  The
flashed AX7101 - built N_STREAMS = 8 - advertised 1 talker source and 2
listener sinks next to a reference device advertising 4/10 and a peer host
advertising 8/8, so every controller on the segment could see and bind ONE of
its eight streams.  The register faithfully held what was written, so nothing
looked broken anywhere.

The CRF Media Clock Output is the sharpest case: it is a bindable ACMP talker
source at talker_unique_id = N_STREAMS, its PDUs were on the wire every 2 ms,
and it was invisible to ATDECC because uid 8 sat outside an advertised range
of 1.  (That is NOT the same gap as M-CLK-2, which is about the CRF stream not
holding an SRP class-A reservation.  This gate is only about discoverability.)

THE SHAPE IS SOFTWARE-DEFINED, NOT SOFTWARE-WRITABLE.  The fix is not to move
the number into the RTL - RTL choosing the entity shape is the same mistake
one layer down.  configs/endstation_*.yaml is the single declarative
definition and it drives the gateware, the AEM model and lwSRP alike, so
sw/builder/endstation_builder.py emits this shape's
hdl/common/gen/adp_shape_defaults.svh (which milan_csr and milan_datapath
`include) in one pass from one config.  This gate is what makes "one pass,
one config" checkable.

WHAT MOVED, 2026-08-12.  Two of this gate's three original comparands are
DELETED with the IEEE 1722.1 control-plane RTL: hdl/ieee17221/aecp/gen/
aecp_aem_rom.svh (the descriptor set the gateware served) and
tb/verilator/aecp/aem_golden.h (the TB's byte-exact image of it).  The
protocol-processor submodule is the control plane now. Its AECP uCPU serves a
descriptor image loaded through the external descriptor-memory interface, so
there is no legacy RTL ROM or matching testbench golden to keep in step.

THE GATE STAYS, AND IS STILL THE SAME GATE.  The defect it was written for -
an 8x8 gateware shipping a 1x1 shape - is entirely possible today, because
adp_shape_defaults.svh is STILL a tracked, last-writer-wins artifact that
`--write-rtl <cfg>` overwrites for whichever config it is handed, and it now
sizes the protocol processor's source/sink arrays as well as the ADPDU words.
What it compares is the config's declared shape against the two places that
copy of it lives on disk.

WHAT IT CHECKS, per end-station config:

  A  generated svh    the shape include the builder emits for this config
                      carries the counts adp_shape() computes from it, and
                      names the config it came from
  B  AEM model        this config's AEM overlay declares the same
                      STREAM_OUTPUT / STREAM_INPUT counts, and its
                      entity_counts agree with its descriptor_counts
  C  entity model     the descriptor ROM the builder generates for this
                      config has that many STREAM_OUTPUT / STREAM_INPUT
                      descriptors.  NOTE what this is now: a self-consistency
                      check of the DECLARATIVE model, generated in memory.
                      The processor serves the resulting descriptor image
                      through its external store. It is kept because the ADP
                      counts in arm A are DERIVED from that same model, so a
                      model that disagrees with itself is a shape count nobody
                      should trust
  D  per-config copy  configs/generated/<name>/gen/adp_shape_defaults.svh on
                      disk is byte-identical to the freshly generated text
                      (harnesses and builds select a shape by include path),
                      and that `gen/` holds NO leftover aecp_aem_rom.svh - a
                      build artifact in an include dir is a build artifact
                      something eventually compiles
  E  tracked shape    hdl/common/gen/adp_shape_defaults.svh names a
                      source config that exists and is EXACTLY what that
                      config generates - so "which shape is in the tree" is
                      always answerable and always current
  F  RTL consumption  milan_csr builds 0x618/0x61C from the generated
                      constants and has a defaults arm, NO write arm and NO
                      is_plain_rw entry for either; milan_datapath sizes its
                      source/sink context arrays from the SAME constants, so
                      the advertised range is the addressable range
  G  firmware version the ENTITY descriptor's firmware_version (1722.1-2021
                      7.2.1, offset 116) names the gateware's OWN VERSION
                      parameter, and no config declares one of its own

THE SAME DEFECT, ONE FIELD OVER (G, 2026-07-28).  All three configs hardcoded
`firmware_version: "0.1.0"` while hdl/common/csr/milan_csr.sv said
32'h0001_0016, and the AEM generator stamped the config's string into the
descriptor - so every board we ship told Hive, la_avdecc and every other
controller on the segment that it ran firmware 0.1.0.  Every gate was green,
because every gate compared that declaration against another declaration.
The version is DERIVED from the parameter (major.minor.rev =
VERSION[31:16].VERSION[15:0].entity.firmware_rev, so 0x0001_0016 -> "1.22.0")
and arm G reads it back out of the descriptor BYTES.  Those bytes are now
GENERATED IN MEMORY rather than read from the tracked ROM and the TB golden,
both of which are deleted; the arm therefore proves the derivation reaches
offset 116, and no longer proves any artifact is fresh (there is no longer an
artifact to be stale).  The two mutations that tested exactly that staleness
are removed from the self-test, by name and with the reason.

WHERE THE REST OF THIS GATE LIVES.  Two subjects were lifted out of this
file, each into a module named for what it produces, and nothing else
imports either:

  scripts/shape_consumer_inventory.py   what a build expression naming
                                        gen/adp_shape_defaults.svh resolves
                                        to - make expansion, frozen `:=`
                                        values, rule prerequisites (arm I)
  scripts/entity_shape_selftest.py      the planted worlds every arm above
                                        must go red in (--self-test)

Usage:
    check_entity_shape.py                 # every configs/endstation_*.yaml
    check_entity_shape.py --self-test     # + prove disagreeing shapes FAIL
    check_entity_shape.py --built-config configs/endstation_ax7101_8x8.yaml
                                          # pre-build: the tracked entity
                                          # definition IS this config's
                                          # (what sweep.sh/build.sh call)

Exit 0 = agree, 1 = drift (offending values printed), 2 = usage/setup.
Needs pyyaml (same dependency as sw/builder/test_builder.py).
"""

import argparse
import subprocess
import re
import sys
from collections.abc import Sequence
from pathlib import Path
from types import ModuleType

#: Arm I's resolver: everything that turns a build expression naming
#: gen/adp_shape_defaults.svh into the repository path it actually reaches.
#: sys.path[0] is this directory when the gate runs as a script, and
#: sw/builder/test_builder.py puts scripts/ on the path before importing it.
from shape_consumer_inventory import (GATE_SOURCES,  # noqa: E402
                                      dangling_consumers)

ROOT = Path(__file__).resolve().parent.parent
#: Where arms F and G read the RTL from when nothing has redirected them.
#: The self-test points RTL (below) at mutated copies for one call; these
#: two names always spell the tree's own sources.
DATAPATH = ROOT / "hdl/milan/milan_datapath.sv"
CSR = ROOT / "hdl/common/csr/milan_csr.sv"
CONFIG_DIR = ROOT / "configs"
#: What a per-config `gen/` include dir may hold. adp_shape_defaults.svh is
#: the ONE generated entity artifact any RTL still compiles; aecp_aem_rom.svh
#: used to sit beside it for KL_aecp_aem_store, and that module is deleted.
#: Arm D refuses a leftover, because a +incdir that finds a ROM nobody
#: regenerates is how a stale descriptor set gets compiled by accident.
GEN_DIR_FORBIDDEN = ("aecp_aem_rom.svh",)

# IEEE 1722.1-2021 Table 7.1 descriptor types
ENTITY = 0x0000
STREAM_INPUT, STREAM_OUTPUT = 0x0005, 0x0006

#: IEEE 1722.1-2021 7.2.1 Table 7-2: the ENTITY descriptor's firmware_version
#: field sits at offset 116 and is 64 octets - "64-octet UTF-8 string
#: containing the firmware version of the ATDECC Entity".
FW_OFFSET, FW_LEN = 116, 64

class Tally:
    """Every ck() result: how many comparisons ran, and which ones failed.

    ONE module-level instance, MUTATED and never rebound, so no function
    here reaches for `global` and no importer can end up holding a second
    answer to "did this run pass".  The self-test swaps a planted
    mutation's result set in and out by assigning these attributes around
    one call (entity_shape_selftest.expect_fail).
    """

    def __init__(self):
        self.fails = []
        self.checks = 0
        #! set while a self-test mutation is being run: the failure it
        #! plants is the expected outcome, so it is collected, not printed
        self.quiet = False


class RtlSources:
    """The two RTL files arms F and G read, as one mutable pair.

    Same reason as Tally: the self-test redirects these at mutated copies
    for the length of one call and puts them back, which used to be two
    `global` rebinds in a helper and its nested restore.
    """

    def __init__(self, datapath, csr):
        self.datapath = datapath
        self.csr = csr


TALLY = Tally()
RTL = RtlSources(DATAPATH, CSR)


# The three file helpers take `str | Path` rather than `Path`, because the
# mutation proofs (scripts/entity_shape_selftest.py) hand them temp-directory
# paths they build with their own spelling. Everything this module computes
# for itself is a Path.
def read_text(path: str | Path) -> str:
    """A whole file, read through a managed handle."""
    with open(path) as handle:
        return handle.read()


def read_utf8(path: str | Path) -> str:
    """A whole file as UTF-8 text, undecodable bytes replaced."""
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def write_text(path: str | Path, text: str) -> None:
    """Replace a file's contents, through a managed handle."""
    with open(path, "w") as handle:
        handle.write(text)


def ck(what: str, got: object, exp: object) -> None:
    """Record one comparison in the module tally, and say so out loud.

    Every arm of this gate reduces to a value the tree produces and the
    value it has to be, so this is the only place a result is decided.  A
    failure is collected even while quiet, which is what lets a planted
    mutation prove an arm goes red without printing a failure a reader
    would have to learn to ignore.
    """
    TALLY.checks += 1
    if got != exp:
        TALLY.fails.append(f"{what}: got {got!r}, expected {exp!r}")
        if not TALLY.quiet:
            print(f"  [FAIL] {what}: got {got!r}, expected {exp!r}")
    elif not TALLY.quiet:
        print(f"  [ok]   {what} = {got!r}")


# -------------------------------------------------- consumer inventory --
def check_shape_consumers() -> None:
    """I: every declared consumer of the TRACKED shape header resolves.

    The header is a tracked build artifact whose consumers live in
    Makefiles, scripts and prose. Relocating it and updating only the
    consumers an extension-filtered grep happens to match is how three
    Verilator suites came to depend on a deleted prerequisite while every
    source-level gate stayed green -- Makefiles carry no extension, so
    `--include=*.sv` and friends never see them. This check is deliberately
    file-type blind.

    It is also FAIL CLOSED, with make's own engine as the resolver for
    make consumers. An earlier spelling skipped any reference whose
    variables it could not expand, and `RTL_DIR = $(shell pwd)/../../../hdl`
    -- ordinary make -- walked a stale prerequisite straight through it;
    the hand-rolled model that replaced it then mis-resolved `+=`, a later
    `:=` definition and an `include` override, banking confidently wrong
    resolutions as clean. A Makefile reference is now expanded by make
    itself (finals, includes, functions), cross-checked against the frozen
    value of every variable assigned from it -- the two probes must agree,
    which is what an immediate `:=` fed by any later definition (same
    file, `include`, `export`, `override`) can never do -- and otherwise
    either resolves to a tracked path or is listed in
    CLASSIFIED_CONSUMERS with a reason.
    A textual suffix is not evidence that the build expression in front of
    it resolves to the repository. Nothing else passes.
    """
    tracked = set(tracked_files())
    dangling = []
    for name in sorted(tracked):
        if name in GATE_SOURCES:
            continue
        path = ROOT / name
        if not path.is_file():
            continue
        try:
            text = read_utf8(path)
        except OSError:
            continue
        dangling.extend(dangling_consumers(name, text, tracked))
    ck("I every shape-header consumer resolves", sorted(dangling), [])


# --------------------------------------------------- include ambiguity --
INCLUDE_RE = re.compile(r'^\s*`include\s+"([^"]+)"', re.M)


def tracked_files() -> list[str]:
    """Every path git records, which is what "in the tree" means to this gate.

    An untracked copy of a header is invisible here on purpose: it cannot be
    what a build compiles for anyone but the person who has it.
    """
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True,
                         capture_output=True, text=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


def check_include_ambiguity() -> None:
    """H: no `include may resolve two ways.

    A quoted `include is searched in the INCLUDING FILE'S OWN DIRECTORY before
    the include path by Vivado, yosys and sv2v -- but NOT by Verilator, which
    searches -I/+incdir and the CWD only.  So when an includer has a copy of
    its own target sitting beside it AND another copy is reachable on the
    include path, the two front ends bind different files and the same source
    tree elaborates as two different designs, silently.

    That is not hypothetical: milan_csr.sv and milan_datapath.sv both
    `include "gen/adp_shape_defaults.svh", only milan_csr.sv had a copy next
    door, and the shape override (`+incdir` at configs/generated/<cfg>/)
    therefore reached only half the design on every front end except
    Verilator.  See the PR that added this check.

    The rule enforced here is front-end independent, which is the point: an
    includer may not have its target adjacent while a competing copy of the
    same relative path exists anywhere else in the tree.  Then precedence
    cannot decide anything, and every tool agrees by construction.
    """
    tracked = tracked_files()
    rtl = [f for f in tracked
           if f.endswith((".sv", ".svh", ".v", ".vh"))
           and (f.startswith("hdl/") or f.startswith("configs/"))]
    ambiguous = []
    for f in rtl:
        try:
            text = read_utf8(ROOT / f)
        except OSError:
            continue
        own_dir = Path(f).parent
        for rel in set(INCLUDE_RE.findall(text)):
            if rel.startswith("/") or ".." in rel.split("/"):
                continue
            # STRING, not Path: `adjacent` is compared against git ls-files
            # output and printed in the finding, and the `..`-free guard above
            # is what makes the plain join equal to the old normpath.
            adjacent = str(own_dir / rel)
            if not (ROOT / adjacent).is_file():
                continue
            others = [o for o in tracked
                      if o.endswith("/" + rel) and o != adjacent]
            if others:
                ambiguous.append(
                    "%s `include \"%s\" resolves to %s beside it, and to %s "
                    "on the include path" % (f, rel, adjacent,
                                             ", ".join(sorted(others))))
    ck("H include resolution is unambiguous", sorted(ambiguous), [])


# ------------------------------------------------------ RTL consumption --
def check_rtl_wiring() -> None:
    """F: the RTL CONSUMES the generated shape and serves it read-only.

    Nothing here recomputes a count - that is the point. It checks that the
    two modules take their numbers from gen/adp_shape_defaults.svh and that
    no path exists for software to overwrite them."""
    print("== RTL: the shape is included from the config, and is read-only ==")
    dp = read_text(RTL.datapath)
    ck("milan_datapath includes the generated shape",
       '`include "gen/adp_shape_defaults.svh"' in dp, True)
    ck("ACMP talker contexts sized by ADP_TALKER_SRC_C",
       bool(re.search(r"localparam\s+int\s+ACMP_SRC_C\s*=\s*ADP_TALKER_SRC_C\s*;",
                      dp)), True)
    ck("ACMP sink contexts sized by ADP_LISTENER_SINK_C",
       bool(re.search(r"localparam\s+int\s+ACMP_SINKS_C\s*=\s*ADP_LISTENER_SINK_C\s*;",
                      dp)), True)
    # the shape must NOT be threaded through the instantiation any more: a
    # second copy is a second thing to get wrong
    inst = re.search(r"milan_csr\s*#\((.*?)\)\s*csr\s*\(", dp, re.S)
    if not inst:
        raise SystemExit("SETUP: no milan_csr instantiation in milan_datapath")
    ck("no ADP shape threaded through the milan_csr port map",
       "N_TALKER_SRC_P" in inst.group(1) or "N_LISTENER_SINK_P" in inst.group(1),
       False)

    csr = read_text(RTL.csr)
    ck("milan_csr includes the generated shape",
       '`include "gen/adp_shape_defaults.svh"' in csr, True)
    ck("0x618 word is built from ADP_TALKER_SRC_C",
       bool(re.search(r"ADP_TALK_C\s*=\s*\{[^}]*ADP_TALKER_SRC_C", csr, re.S)),
       True)
    ck("0x61C word is built from ADP_LISTENER_SINK_C",
       bool(re.search(r"ADP_LIST_C\s*=\s*\{[^}]*ADP_LISTENER_SINK_C", csr,
                      re.S)), True)
    ck("0x618 has a defaults-ROM arm",
       bool(re.search(r"A_ADP_TALK\[10:0\]:\s*csr_default\s*=\s*ADP_TALK_C",
                      csr)), True)
    ck("0x61C has a defaults-ROM arm",
       bool(re.search(r"A_ADP_LIST\[10:0\]:\s*csr_default\s*=\s*ADP_LIST_C",
                      csr)), True)
    # RO means: no write arm and no shadow-write entry. Either one coming back
    # restores the exact defect - a register that faithfully holds a lie.
    ck("0x618 has NO write arm",
       bool(re.search(r"A_ADP_TALK:\s*\w+\s*<=", csr)), False)
    ck("0x61C has NO write arm",
       bool(re.search(r"A_ADP_LIST:\s*\w+\s*<=", csr)), False)
    rw = re.search(r"function automatic logic is_plain_rw.*?endfunction", csr,
                   re.S)
    if not rw:
        raise SystemExit("SETUP: no is_plain_rw function in milan_csr")
    body = re.sub(r"//[^\n]*", "", rw.group(0))     # comments name them
    ck("0x618 is NOT plain-RW", "A_ADP_TALK" in body, False)
    ck("0x61C is NOT plain-RW", "A_ADP_LIST" in body, False)


# ------------------------------------------------------------ AEM ROM read --
def svh_shape(text: str, where: str) -> dict[str, int]:
    """Read the four constants back out of a generated shape include."""
    def one(name: str, pat: str) -> str:
        """The one constant's literal, or a setup refusal naming the include."""
        m = re.search(name + r"\s*=\s*" + pat + r"\s*;", text)
        if not m:
            raise SystemExit(f"SETUP: no {name} in {where}")
        return m.group(1)
    return dict(
        talker_stream_sources=int(one("ADP_TALKER_SRC_C", r"(\d+)")),
        listener_stream_sinks=int(one("ADP_LISTENER_SINK_C", r"(\d+)")),
        talker_capabilities=int(one("ADP_TALKER_CAPS_C", r"16'h([0-9A-Fa-f]{4})"),
                                16),
        listener_capabilities=int(
            one("ADP_LISTENER_CAPS_C", r"16'h([0-9A-Fa-f]{4})"), 16))


def svh_source(text: str) -> str | None:
    """The `Source :` header line every builder-generated include carries."""
    m = re.search(r"//\s*Source\s*:\s*(\S+)", text)
    return m.group(1) if m else None


def tracked_owner(builder: ModuleType, adp_text: str | None = None,
                  configs: Sequence[str | Path] | None = None
                  ) -> tuple[str | None, dict[str, object] | None]:
    """WHICH CONFIG OWNS the tracked entity definition - asked of the TREE.

    `endstation_builder.py --write-rtl <cfg>` installs the tracked shape
    include for WHICHEVER config it is handed, so the owner is not a constant
    a gate may assume: it is a fact the tree records.  The shape include's
    `Source :` line is the ONE place the answer lives - and this is the ONE
    reader of it, shared with sw/builder/test_builder.py gates 10/17/24d.
    Two answers to "who owns the tracked shape" is exactly how a gate comes
    to assume a config: gate 10 hardcoded endstation_arty_current and went
    red for every other owner, blocking any other shape from being written
    into the tree at all.

    adp_text overrides the tracked shape include, so a caller can ask the
    question of a CANDIDATE pair without installing it in the tree.
    Returns (source-path string or None, config dict or None).
    """
    if adp_text is None:
        adp_text = read_text(ROOT / builder.ADP_SHAPE_REL)
    src = svh_source(adp_text)
    for path in (all_configs() if configs is None else configs):
        cfg = builder.load_config(path)
        if cfg["source"] == src:
            return src, cfg
    return src, None


def rom_descriptor_counts(path: str) -> dict[int, int]:
    """Count descriptors by type in a generated aecp_aem_rom.svh directory."""
    text = path if "\n" in path else read_text(path)
    body = re.search(r"AEM_DIR_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\};", text, re.S)
    if not body:
        raise SystemExit("SETUP: no AEM_DIR_C directory in the ROM text")
    counts = {}
    for row in re.findall(r"64'h([0-9A-Fa-f_]{4})_", body.group(1)):
        t = int(row.replace("_", ""), 16)
        counts[t] = counts.get(t, 0) + 1
    return counts


# -------------------------------------------------------------- the checks --
def check_config(builder: ModuleType,
                 path: str | Path) -> tuple[dict[str, object], str]:
    """A-D: this config -> its generated shape include -> its AEM ROM."""
    cfg = builder.load_config(path)
    name = cfg["name"]
    L, T = len(cfg["listeners"]), len(cfg["talkers"])
    print(f"\n== {name}  ({L}x{T}) ==")

    want = builder.adp_shape(cfg)
    adp_svh = builder.emit_adp_shape_svh(cfg)
    got = svh_shape(adp_svh, f"{name} generated shape")

    # A: the generated include says what the config says
    ck(f"{name}: svh talker_stream_sources",
       got["talker_stream_sources"], want["talker_stream_sources"])
    ck(f"{name}: svh listener_stream_sinks",
       got["listener_stream_sinks"], want["listener_stream_sinks"])
    ck(f"{name}: svh talker_capabilities",
       f"0x{got['talker_capabilities']:04X}",
       f"0x{want['talker_capabilities']:04X}")
    ck(f"{name}: svh listener_capabilities",
       f"0x{got['listener_capabilities']:04X}",
       f"0x{want['listener_capabilities']:04X}")
    ck(f"{name}: svh names its source config", svh_source(adp_svh),
       cfg["source"])

    # B: the AEM overlay agrees (1722.1-2021 6.2.1.9/6.2.1.11 - the ADPDU
    # counts ARE the STREAM_OUTPUT/STREAM_INPUT descriptor counts)
    ovl = builder.emit_aem_overlay(cfg)
    dc, ec = ovl["descriptor_counts"], ovl["entity_counts"]
    ck(f"{name}: overlay entity_counts.talker == STREAM_OUTPUT",
       ec["talker_stream_sources"], dc["STREAM_OUTPUT"])
    ck(f"{name}: overlay entity_counts.listener == STREAM_INPUT",
       ec["listener_stream_sinks"], dc["STREAM_INPUT"])
    ck(f"{name}: advertised talker sources == STREAM_OUTPUT count",
       got["talker_stream_sources"], dc["STREAM_OUTPUT"])
    ck(f"{name}: advertised listener sinks == STREAM_INPUT count",
       got["listener_stream_sinks"], dc["STREAM_INPUT"])

    # C: and the DESCRIPTOR SET this config generates really has that many.
    # The ROM is generated IN MEMORY and compiled by nothing (the AECP plane
    # that served it is deleted) - this is a self-consistency check of the
    # DECLARATIVE MODEL, and it earns its place because the counts checked in
    # arm A are derived from that same model. A model that disagrees with
    # itself produces an ADP count nobody should trust.
    rom = rom_descriptor_counts(builder.emit_aem_rom_svh(cfg, ovl))
    ck(f"{name}: generated ROM STREAM_OUTPUT descriptors",
       rom.get(STREAM_OUTPUT, 0), got["talker_stream_sources"])
    ck(f"{name}: generated ROM STREAM_INPUT descriptors",
       rom.get(STREAM_INPUT, 0), got["listener_stream_sinks"])

    # the CRF contexts are WHY the counts are N+1: name the uid, so a reader
    # sees which slot the extra one is
    if cfg["clocking"]["crf_output"]:
        ck(f"{name}: CRF talker uid {T} is inside the advertised range",
           got["talker_stream_sources"] > T, True)
        ck(f"{name}: talker_capabilities claims MEDIA_CLOCK_SOURCE",
           bool(got["talker_capabilities"] & 0x0800), True)
    else:
        ck(f"{name}: no CRF output -> no MEDIA_CLOCK_SOURCE claim",
           bool(got["talker_capabilities"] & 0x0800), False)
    if cfg["clocking"]["crf_sink"]:
        ck(f"{name}: CRF sink uid {L} is inside the advertised range",
           got["listener_stream_sinks"] > L, True)

    # D: the tracked per-config copy on disk is what the builder emits now,
    # and its `gen/` holds nothing else an +incdir could pick up. The ROM
    # used to live there for KL_aecp_aem_store; that module is deleted, and a
    # leftover copy in an include dir is a stale descriptor set waiting to be
    # compiled by the next harness that points at this directory.
    p_gen = ROOT / builder.GEN_CONFIG_DIR / name / "gen"
    p_cfg = p_gen / "adp_shape_defaults.svh"
    ck(f"{name}: configs/generated copy is current",
       p_cfg.exists() and read_text(p_cfg) == adp_svh, True)
    left = sorted(f for f in GEN_DIR_FORBIDDEN if (p_gen / f).exists())
    ck(f"{name}: no deleted-plane artifact left in its gen/ include dir",
       left, [])
    return cfg, adp_svh


# ------------------------------------------------ firmware version (7.2.1) --
def _dir_entries(text, pat):
    return [(int(t, 16), int(i, 16), int(b, 16), int(l, 16))
            for t, i, b, l in re.findall(pat, text)]


def svh_rom(text: str) -> tuple[bytes, list[tuple[int, int, int, int]]]:
    """(rom bytes, directory) out of a tracked aecp_aem_rom.svh."""
    body = re.search(r"AEM_ROM_INIT_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\n\};",
                     text, re.S)
    dirb = re.search(r"AEM_DIR_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\n\};", text, re.S)
    if not body or not dirb:
        raise SystemExit("SETUP: no AEM_ROM_INIT_C / AEM_DIR_C in the ROM text")
    rom = bytes(int(b, 16)
                for b in re.findall(r"8'h([0-9A-Fa-f]{2})", body.group(1)))
    return rom, _dir_entries(
        dirb.group(1),
        r"64'h([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})_"
        r"([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})")


# golden_rom() is GONE (2026-08-12): it parsed tb/verilator/aecp/aem_golden.h,
# the image the aecp Verilator suite byte-compared the RTL against. That suite
# and the RTL it exercised are both deleted, so there is no golden to read and
# no staleness for arm G to catch there.


def entity_fw_field(rom: bytes, directory: Sequence[tuple[int, int, int, int]],
                    what: str) -> bytes:
    """The raw 64 octets a controller gets back at ENTITY[0] + 116."""
    base = [b for (t, i, b, _l) in directory if (t, i) == (ENTITY, 0)]
    if not base:
        raise SystemExit(f"SETUP: no ENTITY[0] in the {what} directory")
    return rom[base[0] + FW_OFFSET: base[0] + FW_OFFSET + FW_LEN]


def check_firmware_version(builder: ModuleType) -> None:
    """G: the firmware version a controller READS is the version this
    gateware IS.

    Roadmap item 00 again, at the field a validation tool looks at first.
    The gateware's version exists in exactly one place - `parameter logic
    [31:0] VERSION` behind the read-only 0x004 register in milan_csr.sv,
    whose `//!` comment is the gateware changelog - and the ENTITY
    descriptor's firmware_version is how every controller on the segment
    reads it.  Nothing connected the two: all three endstation configs
    hardcoded `firmware_version: "0.1.0"` and the AEM generator stamped that
    into the descriptor, so on 2026-07-27 a board running 0x0001_0016 told
    Hive, la_avdecc and every other controller that it ran firmware 0.1.0.
    Every gate in the tree was green, because every gate compared that
    declaration against another declaration.

    So this one does not re-derive anything.  It reads the parameter out of
    the RTL and the string out of the DESCRIPTOR BYTES.

    WHAT THOSE BYTES ARE NOW (2026-08-12).  They used to be the TRACKED ROM
    the gateware compiled plus the golden image the aecp TB byte-compared
    against, which made "VERSION bumped, artifacts not regenerated" a build
    failure.  Both files are deleted with the AECP plane, so the bytes are
    GENERATED IN MEMORY from the tracked shape's owning config.  The arm
    therefore still proves the derivation reaches offset 116 in the encoding
    the clause specifies - but it can no longer prove any artifact is fresh,
    because there is no longer an artifact that could go stale.  Said plainly
    here rather than left for a reader to infer from a passing check.

    Encoding is checked too, because the field is fixed-size: IEEE
    1722.1-2021 7.2.1 Table 7-2 places it at offset 116 for 64 octets, and
    7.2 says "The 64-octet strings do not include the NULL terminator when
    they are 64-octets long.  If the string is shorter than 64-octets then
    the remainder of the field shall be zero (0) padded."
    """
    print("\n== firmware version (1722.1-2021 7.2.1, ENTITY + 116) ==")
    g = load_aem_store()
    major, minor = g.rtl_version(RTL.csr)
    print(f"  milan_csr VERSION: 0x{major:04X}_{minor:04X} "
          f"-> major {major}, minor {minor}")

    # 1. no config re-declares it. An agreeing copy is still a second answer
    #    to "what version is this", and it is the copy controllers get.
    for p in all_configs():
        cfg = builder.load_config(p)
        raw = builder.yaml.safe_load(read_text(p))["entity"]
        ck(f"{cfg['name']}: config declares no firmware_version",
           "firmware_version" in raw, False)
        ck(f"{cfg['name']}: emitted firmware_version",
           cfg["entity"]["firmware_version"],
           g.firmware_version_string(cfg["entity"]["firmware_rev"], RTL.csr))

    # 2. the DESCRIPTOR BYTES the tracked shape's owner generates. Generated
    #    in memory: the tracked ROM and the TB golden are deleted, so there
    #    is no on-disk descriptor image left to read (or to go stale).
    owner = tracked_owner_cfg(builder, all_configs())
    if owner is None:
        ck("tracked shape names an owning config whose descriptors can be "
           "generated", False, True)
        return
    want = g.firmware_version_string(owner["entity"]["firmware_rev"], RTL.csr)
    rom_o, dir_o = svh_rom(builder.emit_aem_rom_svh(
        owner, builder.emit_aem_overlay(owner)))
    what = f"generated ROM ({owner['name']})"
    fld = entity_fw_field(rom_o, dir_o, what)
    ck(f"{what}: firmware_version field is {FW_LEN} octets", len(fld), FW_LEN)
    # 7.2: zero padded after the string, and no interior NUL
    s = fld.split(b"\x00", 1)[0]
    ck(f"{what}: firmware_version is zero padded past the string (7.2)",
       fld[len(s):] == bytes(FW_LEN - len(s)), True)
    ck(f"{what}: firmware_version decodes as UTF-8 (7.2.1)", _utf8(s), True)
    ck(f"{what}: firmware_version == the gateware's VERSION",
       s.decode("utf-8", "replace"), want)


def _utf8(b):
    try:
        b.decode("utf-8")
        return True
    except UnicodeDecodeError:
        return False


def load_aem_store() -> ModuleType:
    """avdecc/gen_aem_store.py, which owns the VERSION -> version-string rule.

    Imported here rather than at the top so the shape arms still run on a
    tree where avdecc/ is absent, and refused loudly rather than skipped
    when arm G needs it and it is not there.
    """
    sys.path.insert(0, str(ROOT / "avdecc"))
    try:
        import gen_aem_store as g
    except ImportError as e:                          # pragma: no cover
        raise SystemExit(f"SETUP: cannot import gen_aem_store ({e})")
    return g


def tracked_owner_cfg(builder: ModuleType,
                      configs: Sequence[str | Path]
                      ) -> dict[str, object] | None:
    """The config the tracked entity definition was generated from.

    Returns the CONFIG DICT. Distinct from tracked_owner() above, which
    returns a (source, config) pair and accepts an adp_text override so a
    caller can ask the question of a CANDIDATE pair. Two functions with one
    name shadowed each other across a merge and broke every tuple-unpacking
    caller at import time - hence the rename rather than a second alias."""
    src = svh_source(read_text(ROOT / builder.ADP_SHAPE_REL))
    for path in configs:
        cfg = builder.load_config(path)
        if cfg["source"] == src:
            return cfg
    return None


def check_tracked_shape(builder: ModuleType,
                        configs: Sequence[str | Path]) -> None:
    """E: the tracked entity definition is ONE config's, and is current.

    hdl/common/gen/adp_shape_defaults.svh is what a build `include-s -
    the whole of it now that the AEM ROM has no RTL destination. It must name
    a source config that exists AND be exactly what that config generates,
    otherwise the gateware advertises (and elaborates) a shape nobody chose,
    which is the 2026-07-27 defect with the layers swapped.

    The descriptor counts are checked against the model that owner GENERATES,
    which keeps arm C's question askable of the tracked owner specifically:
    the tracked shape and the entity model it was derived from cannot drift
    apart without one of them being regenerated alone."""
    print("\n== tracked entity definition (what a build includes) ==")
    adp = read_text(ROOT / builder.ADP_SHAPE_REL)
    src, owner = tracked_owner(builder, adp_text=adp, configs=configs)
    print(f"  tracked shape source: {src}")
    ck("tracked ADP shape names a source config", src is not None, True)
    ck(f"tracked shape's source config exists ({src})", owner is not None, True)
    if owner is None:
        return
    ck("tracked ADP shape == what that config generates",
       adp == builder.emit_adp_shape_svh(owner), True)
    got = svh_shape(adp, "tracked shape")
    rc = rom_descriptor_counts(
        builder.emit_aem_rom_svh(owner, builder.emit_aem_overlay(owner)))
    ck("owner's STREAM_OUTPUT descriptors == tracked advertised sources",
       rc.get(STREAM_OUTPUT, 0), got["talker_stream_sources"])
    ck("owner's STREAM_INPUT descriptors == tracked advertised sinks",
       rc.get(STREAM_INPUT, 0), got["listener_stream_sinks"])


def check_built_config(builder: ModuleType, path: str | Path) -> None:
    """Pre-build gate: the tracked entity definition IS the config being
    built. Without this a `build.sh ax8x8` silently inherits whatever shape
    was last committed - exactly how an 8x8 gateware came to carry a 1x1
    descriptor set. The fix is one command, and the message says it."""
    cfg = builder.load_config(path)
    print(f"\n== pre-build: tracked definition vs {cfg['name']} ==")
    adp = read_text(ROOT / builder.ADP_SHAPE_REL)
    ok_adp = adp == builder.emit_adp_shape_svh(cfg)
    ck(f"tracked ADP shape is {cfg['name']}'s", ok_adp, True)
    if not ok_adp:
        print(f"  the tree currently carries {svh_source(adp)}. Fix:\n"
              f"    python3 sw/builder/endstation_builder.py {path} "
              f"--write-rtl")


def load_builder() -> ModuleType:
    """sw/builder/endstation_builder.py - the ONE derivation this gate judges.

    Nothing here recomputes a shape; every expected value comes from the
    builder a real build runs, so the gate cannot agree with itself while
    disagreeing with what gets flashed.
    """
    sys.path.insert(0, str(ROOT / "sw/builder"))
    try:
        import endstation_builder as b
    except ImportError as e:                          # pragma: no cover
        raise SystemExit(f"SETUP: cannot import endstation_builder ({e})")
    return b


def all_configs() -> list[Path]:
    """Every configs/endstation_*.yaml, discovered rather than listed.

    A gate that names its configs stops checking the one added after it.
    One directory, so sorting the Paths is the order sorting their strings
    gave: the parent is identical and only the file name decides.
    """
    return sorted(CONFIG_DIR.glob("endstation_*.yaml"))


def run() -> None:
    """Arms A-I over every config, in the order a defect is cheapest to read."""
    builder = load_builder()
    check_shape_consumers()
    check_include_ambiguity()
    check_rtl_wiring()
    cfgs = all_configs()
    for p in cfgs:
        check_config(builder, p)
    check_tracked_shape(builder, cfgs)
    check_firmware_version(builder)


def main() -> int:
    """The gate's exit status: 0 when every arm agreed, 1 on any drift."""
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--self-test", action="store_true",
                    help="additionally prove that disagreeing shapes FAIL")
    ap.add_argument("--built-config", default=None,
                    help="pre-build check: the tracked entity definition must "
                         "be THIS config's (sweep.sh / build.sh call this)")
    args = ap.parse_args()
    if args.built_config:
        check_built_config(load_builder(), args.built_config)
    else:
        run()
        if args.self_test:
            # Imported here, not at the top: the mutation proofs import this
            # module back (they mutate its RTL sources and read its tally),
            # and nothing but this one flag needs them.
            import entity_shape_selftest
            entity_shape_selftest.self_test()
    print("-" * 70)
    print(f"checks: {TALLY.checks}   failures: {len(TALLY.fails)}")
    for f in TALLY.fails:
        print(f"  {f}")
    print(f"RESULT: {'FAIL' if TALLY.fails else 'PASS'}")
    return 1 if TALLY.fails else 0


if __name__ == "__main__":
    # Run as a script this module is `__main__`, so the self-test's
    # `import check_entity_shape` would load a SECOND copy with its own
    # TALLY and its own RTL paths - the mutations would then be counted in
    # a tally nothing prints. Publish the running module under its import
    # name first; when it was imported normally (sw/builder/test_builder.py)
    # the name is already bound to this same object and nothing changes.
    sys.modules.setdefault("check_entity_shape", sys.modules[__name__])
    sys.exit(main())

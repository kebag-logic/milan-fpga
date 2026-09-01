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
are removed from the self-test below, by name and with the reason.

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
import os
import subprocess
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAPATH = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
CSR = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
CONFIG_DIR = os.path.join(ROOT, "configs")
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

fails = []
checks = 0
quiet = False          #! set while a self-test mutation is being run


def ck(what, got, exp):
    global checks
    checks += 1
    if got != exp:
        fails.append(f"{what}: got {got!r}, expected {exp!r}")
        if not quiet:
            print(f"  [FAIL] {what}: got {got!r}, expected {exp!r}")
    elif not quiet:
        print(f"  [ok]   {what} = {got!r}")


# -------------------------------------------------- consumer inventory --
#: Any literal that names the shape header, with or without a build variable
#: in front of it ($(RTL_DIR)/..., ../../hdl/..., configs/generated/...).
CONSUMER_RE = re.compile(r"[\w$(){}./\\-]*gen/adp_shape_defaults\.svh")


ASSIGN_RE = re.compile(r"^\s*(\w+)\s*[:?]?=\s*(\S+)\s*$", re.MULTILINE)
VARIABLE_RE = re.compile(r"\$[({]?(\w+)[)}]?")
SHAPE_BASENAME = "adp_shape_defaults.svh"

#: References to the shape header that no static expansion can settle, each
#: classified with the reason it is not a tracked-header consumer. This set
#: is the ONLY way past the inventory: an unresolvable reference that is not
#: listed here is a finding, because "could not tell" must not read as "fine".
CLASSIFIED_CONSUMERS = {
    ("sw/litex/sweep.sh", "$CFG_GEN/gen/adp_shape_defaults.svh"):
        "a per-config copy chosen at build time under configs/generated/",
    ("tb/verilator/milan_dp/Makefile",
     "gen_divergent/gen/adp_shape_defaults.svh"):
        "written by gen_divergent_shape.py during the suite, never tracked",
    ("tb/verilator/milan_dp/gen_divergent_shape.py",
     "gen_divergent/gen/adp_shape_defaults.svh"):
        "the same generated file, named by the script that writes it",
}

#: Repo-root-anchored prefixes: a reference starting with one of these is
#: relative to the repository, not to the file quoting it.
ROOT_PREFIXES = ("hdl/", "configs/", "scripts/", "sw/", "syn/", "tb/",
                 "docs/", "bd/", "avdecc/")


def resolve_reference(reference, name, text):
    """Static expansion for script and prose consumers: the repo-relative
    path a reference names, or None when substituting the same-file
    assignments does not settle it. Makefile references never come here --
    make's own engine expands those (resolve_make_reference), because only
    make applies +=, includes and $(shell ...) the way the build does.
    None is NOT a pass -- see the classification below."""
    assignments = dict(ASSIGN_RE.findall(text))
    resolved = reference.lstrip("(")
    for _ in range(4):
        expanded = VARIABLE_RE.sub(
            lambda m: assignments.get(m.group(1), m.group(0)), resolved)
        if expanded == resolved:
            break
        resolved = expanded
    if "$" in resolved:
        return None
    if resolved.startswith(ROOT_PREFIXES):
        return os.path.normpath(resolved)
    return os.path.normpath(os.path.join(os.path.dirname(name), resolved))


MAKE_PROBE_TARGET = "__shape_probe__"

#: An assignment line, however it is spelled: optional `export`/`override`
#: prefixes, any of make's assignment operators. The frozen-value cross
#: check below keys on the VARIABLE being assigned, so a spelling the
#: pattern missed would only ever ADD a probe, never remove one.
ASSIGN_LINE_RE = re.compile(
    r"^[ \t]*(?:export[ \t]+|override[ \t]+)*"
    r"(?P<var>\w+)[ \t]*[:+?]{0,2}=(?P<rhs>.*)$", re.MULTILINE)


def probe_make(directory, makefile, expression):
    """One expression expanded by make itself in the consumer's own
    directory: final variable state, includes read, `+=`, `$(shell ...)`
    and every assignment applied exactly as a build applies them. Returns
    make's expansion, or None when make errors out."""
    probe = "%s: ; @printf '%%s' \"%s\"" % (MAKE_PROBE_TARGET, expression)
    env = dict(os.environ, MAKEFLAGS="", MFLAGS="")
    try:
        run = subprocess.run(
            ["make", "-s", "--no-print-directory", "-f", makefile,
             "--eval", probe, MAKE_PROBE_TARGET],
            cwd=directory, env=env, capture_output=True, text=True,
            timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if run.returncode != 0 or not run.stdout.strip():
        return None
    return run.stdout.strip()


def shape_prereqs_from_database(directory, makefile):
    """Every prerequisite naming the shape header, exactly as make FROZE
    it at parse time. Rule prerequisites are immediate-expansion contexts
    -- a variable defined after the rule line never reaches them however
    the final state reads -- and make's post-parse database records them
    frozen, so it is their ground truth. Returns (ok, tokens); not-ok
    means the database could not be read and nothing is verified."""
    env = dict(os.environ, MAKEFLAGS="", MFLAGS="")
    try:
        run = subprocess.run(["make", "-pqrR", "-f", makefile],
                             cwd=directory, env=env, capture_output=True,
                             text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return False, []
    if "# Files" not in run.stdout:
        return False, []
    tokens = set()
    for line in run.stdout.splitlines():
        if not line or line.startswith(("#", "\t", " ")):
            continue
        idx = line.find(":")
        if idx <= 0 or line[idx + 1:idx + 2] == "=":
            continue
        for token in line[idx + 1:].lstrip(":").split():
            if "$" not in token and token.endswith("/" + SHAPE_BASENAME) \
                    and token.endswith("gen/" + SHAPE_BASENAME):
                tokens.add(token)
    return True, sorted(tokens)


def resolve_make_reference(reference, name, text):
    """The reference expanded by make itself, cross-checked against every
    variable whose assignment carries it. The text probe alone reads the
    FINAL variable state, which an immediate `:=` does not honor -- make
    froze that value at its line, whatever `include`, `export` or a later
    definition did afterwards -- so for each assignment line containing
    the reference, the frozen variable is probed too and the text result
    must appear among its words. Any disagreement, any expansion make
    cannot settle to one word, any make error: None, and None is NOT a
    pass."""
    raw = reference.lstrip("(")
    directory = os.path.join(ROOT, os.path.dirname(name))
    makefile = os.path.basename(name)
    text_out = probe_make(directory, makefile, "$(abspath %s)" % raw)
    if text_out is None or any(c.isspace() for c in text_out):
        return None
    for m in ASSIGN_LINE_RE.finditer(text):
        if reference not in m.group("rhs"):
            continue
        var_out = probe_make(directory, makefile,
                             "$(abspath $(%s))" % m.group("var"))
        if var_out is None or text_out not in var_out.split():
            return None
    return os.path.normpath(os.path.relpath(text_out, ROOT))


def check_shape_consumers():
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
        # The gate's own source carries the CONSUMER_RE pattern and the
        # deliberately-stale path arm I plants. Neither is a consumer.
        if name == "scripts/check_entity_shape.py":
            continue
        path = os.path.join(ROOT, name)
        if not os.path.isfile(path):
            continue
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        is_make = name.endswith("Makefile") or name.endswith(".mk")
        seen_targets = set()

        def judge(reference, target):
            if target is None:
                dangling.append(
                    f"{name}: {reference} cannot be resolved and is not "
                    f"classified in CLASSIFIED_CONSUMERS")
                return
            if target.startswith("configs/generated/"):
                return            # per-config copies are arm D's
            if target in seen_targets:
                return            # one report per resolved defect
            if not target.startswith("hdl/"):
                seen_targets.add(target)
                dangling.append(
                    f"{name}: {reference} -> {target} is outside the "
                    f"tracked tree and is not classified")
                return
            if target not in tracked:
                seen_targets.add(target)
                dangling.append(f"{name}: {reference} -> {target}")

        references = sorted(set(CONSUMER_RE.findall(text)))
        for reference in references:
            # A bare `gen/...` is an `include directive: the compiler
            # resolves it through the search path, not against the file's
            # own directory. Whether it can bind two ways is arm H's
            # subject. A build prerequisite always carries a prefix.
            if reference.lstrip("(") == "gen/" + SHAPE_BASENAME:
                continue
            if (name, reference) in CLASSIFIED_CONSUMERS:
                continue          # the ONLY way past the inventory
            if is_make:
                target = resolve_make_reference(reference, name, text)
            else:
                target = resolve_reference(reference, name, text)
            judge(reference, target)
        if is_make and references:
            # Second source: the frozen prerequisites from make's own
            # database, catching an immediate-expansion RULE line the
            # per-reference probes cannot see ([R8-4]).
            directory = os.path.join(ROOT, os.path.dirname(name))
            ok, prereqs = shape_prereqs_from_database(
                directory, os.path.basename(name))
            if not ok:
                dangling.append(
                    f"{name}: make database unreadable; frozen shape "
                    f"prerequisites cannot be verified")
            for token in prereqs:
                if token.lstrip("(") == "gen/" + SHAPE_BASENAME:
                    continue
                if (name, token) in CLASSIFIED_CONSUMERS:
                    continue
                if os.path.isabs(token):
                    target = os.path.normpath(os.path.relpath(token, ROOT))
                else:
                    target = os.path.normpath(
                        os.path.join(os.path.dirname(name), token))
                judge(token, target)
    ck("I every shape-header consumer resolves", sorted(dangling), [])


# --------------------------------------------------- include ambiguity --
INCLUDE_RE = re.compile(r'^\s*`include\s+"([^"]+)"', re.M)


def tracked_files():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True,
                         capture_output=True, text=True)
    return [l for l in out.stdout.splitlines() if l.strip()]


def check_include_ambiguity():
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
            text = open(os.path.join(ROOT, f), encoding="utf-8",
                        errors="replace").read()
        except OSError:
            continue
        own_dir = os.path.dirname(f)
        for rel in set(INCLUDE_RE.findall(text)):
            if rel.startswith("/") or ".." in rel.split("/"):
                continue
            adjacent = os.path.normpath(os.path.join(own_dir, rel))
            if not os.path.isfile(os.path.join(ROOT, adjacent)):
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
def check_rtl_wiring():
    """F: the RTL CONSUMES the generated shape and serves it read-only.

    Nothing here recomputes a count - that is the point. It checks that the
    two modules take their numbers from gen/adp_shape_defaults.svh and that
    no path exists for software to overwrite them."""
    print("== RTL: the shape is included from the config, and is read-only ==")
    dp = open(DATAPATH).read()
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

    csr = open(CSR).read()
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
def svh_shape(text, where):
    """Read the four constants back out of a generated shape include."""
    def one(name, pat):
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


def svh_source(text):
    """The `Source :` header line every builder-generated include carries."""
    m = re.search(r"//\s*Source\s*:\s*(\S+)", text)
    return m.group(1) if m else None


def tracked_owner(builder, adp_text=None, configs=None):
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
        adp_text = open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read()
    src = svh_source(adp_text)
    for path in (all_configs() if configs is None else configs):
        cfg = builder.load_config(path)
        if cfg["source"] == src:
            return src, cfg
    return src, None


def rom_descriptor_counts(path):
    """Count descriptors by type in a generated aecp_aem_rom.svh directory."""
    text = path if "\n" in path else open(path).read()
    body = re.search(r"AEM_DIR_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\};", text, re.S)
    if not body:
        raise SystemExit("SETUP: no AEM_DIR_C directory in the ROM text")
    counts = {}
    for row in re.findall(r"64'h([0-9A-Fa-f_]{4})_", body.group(1)):
        t = int(row.replace("_", ""), 16)
        counts[t] = counts.get(t, 0) + 1
    return counts


# -------------------------------------------------------------- the checks --
def check_config(builder, path):
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
    p_gen = os.path.join(ROOT, builder.GEN_CONFIG_DIR, name, "gen")
    p_cfg = os.path.join(p_gen, "adp_shape_defaults.svh")
    ck(f"{name}: configs/generated copy is current",
       os.path.exists(p_cfg) and open(p_cfg).read() == adp_svh, True)
    left = sorted(f for f in GEN_DIR_FORBIDDEN
                  if os.path.exists(os.path.join(p_gen, f)))
    ck(f"{name}: no deleted-plane artifact left in its gen/ include dir",
       left, [])
    return cfg, adp_svh


# ------------------------------------------------ firmware version (7.2.1) --
def _dir_entries(text, pat):
    return [(int(t, 16), int(i, 16), int(b, 16), int(l, 16))
            for t, i, b, l in re.findall(pat, text)]


def svh_rom(text):
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


def entity_fw_field(rom, directory, what):
    """The raw 64 octets a controller gets back at ENTITY[0] + 116."""
    base = [b for (t, i, b, _l) in directory if (t, i) == (ENTITY, 0)]
    if not base:
        raise SystemExit(f"SETUP: no ENTITY[0] in the {what} directory")
    return rom[base[0] + FW_OFFSET: base[0] + FW_OFFSET + FW_LEN]


def check_firmware_version(builder):
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
    major, minor = g.rtl_version(CSR)
    print(f"  milan_csr VERSION: 0x{major:04X}_{minor:04X} "
          f"-> major {major}, minor {minor}")

    # 1. no config re-declares it. An agreeing copy is still a second answer
    #    to "what version is this", and it is the copy controllers get.
    for p in all_configs():
        cfg = builder.load_config(p)
        raw = builder.yaml.safe_load(open(p))["entity"]
        ck(f"{cfg['name']}: config declares no firmware_version",
           "firmware_version" in raw, False)
        ck(f"{cfg['name']}: emitted firmware_version",
           cfg["entity"]["firmware_version"],
           g.firmware_version_string(cfg["entity"]["firmware_rev"], CSR))

    # 2. the DESCRIPTOR BYTES the tracked shape's owner generates. Generated
    #    in memory: the tracked ROM and the TB golden are deleted, so there
    #    is no on-disk descriptor image left to read (or to go stale).
    owner = tracked_owner_cfg(builder, all_configs())
    if owner is None:
        ck("tracked shape names an owning config whose descriptors can be "
           "generated", False, True)
        return
    want = g.firmware_version_string(owner["entity"]["firmware_rev"], CSR)
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


def load_aem_store():
    sys.path.insert(0, os.path.join(ROOT, "avdecc"))
    try:
        import gen_aem_store as g
    except ImportError as e:                          # pragma: no cover
        raise SystemExit(f"SETUP: cannot import gen_aem_store ({e})")
    return g


def tracked_owner_cfg(builder, configs):
    """The config the tracked entity definition was generated from.

    Returns the CONFIG DICT. Distinct from tracked_owner() above, which
    returns a (source, config) pair and accepts an adp_text override so a
    caller can ask the question of a CANDIDATE pair. Two functions with one
    name shadowed each other across a merge and broke every tuple-unpacking
    caller at import time - hence the rename rather than a second alias."""
    src = svh_source(open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read())
    for path in configs:
        cfg = builder.load_config(path)
        if cfg["source"] == src:
            return cfg
    return None


def check_tracked_shape(builder, configs):
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
    adp = open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read()
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


def check_built_config(builder, path):
    """Pre-build gate: the tracked entity definition IS the config being
    built. Without this a `build.sh ax8x8` silently inherits whatever shape
    was last committed - exactly how an 8x8 gateware came to carry a 1x1
    descriptor set. The fix is one command, and the message says it."""
    cfg = builder.load_config(path)
    print(f"\n== pre-build: tracked definition vs {cfg['name']} ==")
    adp = open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read()
    ok_adp = adp == builder.emit_adp_shape_svh(cfg)
    ck(f"tracked ADP shape is {cfg['name']}'s", ok_adp, True)
    if not ok_adp:
        print(f"  the tree currently carries {svh_source(adp)}. Fix:\n"
              f"    python3 sw/builder/endstation_builder.py {path} "
              f"--write-rtl")


def load_builder():
    sys.path.insert(0, os.path.join(ROOT, "sw/builder"))
    try:
        import endstation_builder as b
    except ImportError as e:                          # pragma: no cover
        raise SystemExit(f"SETUP: cannot import endstation_builder ({e})")
    return b


def all_configs():
    return sorted(os.path.join(CONFIG_DIR, f) for f in os.listdir(CONFIG_DIR)
                  if f.startswith("endstation_") and f.endswith(".yaml"))


def run():
    builder = load_builder()
    check_shape_consumers()
    check_include_ambiguity()
    check_rtl_wiring()
    cfgs = all_configs()
    for p in cfgs:
        check_config(builder, p)
    check_tracked_shape(builder, cfgs)
    check_firmware_version(builder)


# ---------------------------------------------------------------- self-test --
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
    global fails, checks, quiet
    saved_f, saved_c, saved_q = fails, checks, quiet
    fails, checks, quiet = [], 0, True
    try:
        fn()
    except Exception as e:                            # noqa: BLE001
        fails.append(f"{type(e).__name__}: {e}")
    if isinstance(required, str):
        required = (required,)
    reasons = "\n".join(fails)
    missing = [token for token in required if token not in reasons]
    caught = bool(fails) and not missing
    if missing:
        why = "rejection did not name " + ", ".join(repr(s) for s in missing)
    else:
        why = fails[0] if fails else ""
    fails, checks, quiet = saved_f, saved_c, saved_q
    ck(f"MUTATION rejected: {label}", caught, True)
    if caught:
        print(f"         (rejected by: {why})")


def with_rtl(dp_text=None, csr_text=None):
    """Context-manager-ish helper: swap in mutated sources for one call."""
    global DATAPATH, CSR
    keep = (DATAPATH, CSR)
    td = tempfile.mkdtemp()
    if dp_text is not None:
        DATAPATH = os.path.join(td, "milan_datapath.sv")
        open(DATAPATH, "w").write(dp_text)
    if csr_text is not None:
        CSR = os.path.join(td, "milan_csr.sv")
        open(CSR, "w").write(csr_text)

    def restore():
        global DATAPATH, CSR
        DATAPATH, CSR = keep
        shutil.rmtree(td, ignore_errors=True)
    return restore


def self_test():
    """Mutation proof: every planted shape disagreement must FAIL."""
    print("\n== self-test: a disagreeing shape must be REJECTED ==")
    builder = load_builder()

    # 0. THE AMBIGUITY CASE (arm H). Put a copy of the shape header back
    #    beside milan_csr.sv, exactly where it used to live. Nothing about
    #    the CONTENT is wrong -- the copy is byte-identical to the tracked
    #    one -- and every existing arm still passes. What is wrong is that
    #    the file is now reachable two ways, so Verilator binds the include
    #    path's copy while Vivado, yosys and sv2v bind this one, and a
    #    +incdir shape override reaches only half the design.
    adjacent = os.path.join(ROOT, "hdl", "common", "csr", "gen",
                            os.path.basename(builder.ADP_SHAPE_REL))
    os.makedirs(os.path.dirname(adjacent), exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, builder.ADP_SHAPE_REL), adjacent)
    try:
        expect_fail("a shape header beside its includer is ambiguous",
                    check_include_ambiguity)
    finally:
        os.unlink(adjacent)

    # 0b. THE STALE-CONSUMER CASE (arm I). Point a build prerequisite at the
    #     header's old home. Nothing about the RTL is wrong and every
    #     source-level gate stays green -- only the consumer inventory sees
    #     that the named file is gone.
    stale = os.path.join(ROOT, "tb/verilator/csr/Makefile")
    original = open(stale, encoding="utf-8").read()
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original.replace(
            "$(RTL_DIR)/common/gen/adp_shape_defaults.svh",
            "$(RTL_DIR)/common/csr/gen/adp_shape_defaults.svh", 1))
    try:
        expect_fail("a build prerequisite left at the header's old path",
                    check_shape_consumers,
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
                    check_shape_consumers,
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
                    check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

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
                    check_shape_consumers,
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
                    check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "cannot be resolved"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)

    # 0g. [R8-2]'s third recurrence: an include overriding the prefix.
    #     Make reads the include; the final value points nowhere inside
    #     the repository, and the resolver reports exactly that.
    shadow_mk = os.path.join(ROOT, "tb/verilator/csr/shape_paths.mk")
    with open(shadow_mk, "w", encoding="utf-8") as handle:
        handle.write("RTL_DIR = /nonexistent\n")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + "\ninclude shape_paths.mk\n")
    try:
        expect_fail("an include that overrides the prefix",
                    check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)
        os.unlink(shadow_mk)
    # 0h. [R8-3]'s first evasion: the late definition arrives through an
    #     include, so no same-file scan can see it. The frozen-variable
    #     cross-check does: SHAPE_LATE froze the empty prefix, the text
    #     probe reads the include's final value, and they disagree.
    late_mk = os.path.join(ROOT, "tb/verilator/csr/late_dir.mk")
    with open(late_mk, "w", encoding="utf-8") as handle:
        handle.write("LATE_DIR := ../../../hdl\n")
    with open(stale, "w", encoding="utf-8") as handle:
        handle.write(original + (
            "\nSHAPE_LATE := $(LATE_DIR)/common/gen/adp_shape_defaults.svh"
            "\ninclude late_dir.mk\n"))
    try:
        expect_fail("an immediate assignment fed by an include",
                    check_shape_consumers,
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
                    check_shape_consumers,
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
                    check_shape_consumers,
                    ("tb/verilator/csr/Makefile", "outside the tracked tree"))
    finally:
        with open(stale, "w", encoding="utf-8") as handle:
            handle.write(original)
    src_cfg = os.path.join(CONFIG_DIR, "endstation_ax7101_8x8.yaml")
    base_cfg = open(src_cfg).read()
    base_dp = open(DATAPATH).read()
    base_csr = open(CSR).read()

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
                    lambda: check_config(builder, src_cfg))
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
                    lambda: check_config(builder, src_cfg))
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
                    lambda: check_config(
                        builder,
                        os.path.join(CONFIG_DIR,
                                     "endstation_arty_current.yaml")))
    finally:
        builder.adp_shape = real_shape

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
        other = builder.load_config(os.path.join(CONFIG_DIR,
                                                 "endstation_arty_4x4.yaml"))
        adp4 = os.path.join(td, "adp_shape_defaults.svh")
        open(adp4, "w").write(builder.emit_adp_shape_svh(other))
        builder.ADP_SHAPE_REL = os.path.relpath(adp4, ROOT)
        try:
            expect_fail(
                "the tree carries a DIFFERENT config's shape than the one "
                "being built",
                lambda: check_built_config(
                    builder,
                    os.path.join(CONFIG_DIR, "endstation_ax7101_8x8.yaml")))
        finally:
            builder.ADP_SHAPE_REL = keep

    # 4b. and the same file left STALE against its own declared owner: the
    #     `Source :` marker still names config X while the body is no longer
    #     what X generates. A shape include that lies about being current is
    #     worse than one that names nobody.
    with tempfile.TemporaryDirectory() as td:
        owner = tracked_owner_cfg(builder, all_configs())
        if owner is None:
            raise SystemExit("SELF-TEST SETUP: the tracked shape has no owner")
        stale = os.path.join(td, "adp_shape_defaults.svh")
        open(stale, "w").write(mutate(
            builder.emit_adp_shape_svh(owner),
            f"ADP_TALKER_SRC_C    = {adp_shape_of(builder, owner)};",
            f"ADP_TALKER_SRC_C    = {adp_shape_of(builder, owner) + 1};"))
        builder.ADP_SHAPE_REL = os.path.relpath(stale, ROOT)
        try:
            expect_fail("tracked shape is STALE against the config it names",
                        lambda: check_tracked_shape(builder, all_configs()))
        finally:
            builder.ADP_SHAPE_REL = keep

    # 5. milan_csr regains a write arm for 0x618
    restore = with_rtl(csr_text=mutate(
        base_csr,
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;",
        "          A_ADP_TALK:   adp_ccaps <= s_axi_wdata;\n"
        "          A_ADP_CCAPS:  adp_ccaps <= s_axi_wdata;"))
    try:
        expect_fail("milan_csr regained a write arm for 0x618",
                    check_rtl_wiring)
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
                    check_rtl_wiring)
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
                    lambda: check_firmware_version(builder))
    finally:
        restore()

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
        open(p, "w").write(mutate(
            base_cfg, '  serial_number: "AX7101-0001"',
            '  firmware_version: "0.1.0"\n  serial_number: "AX7101-0001"'))
        expect_fail("a config declares its own firmware_version",
                    lambda: builder.load_config(p))

    # 10. and the config itself losing a STREAM_INPUT while N_STREAMS holds
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "short_listener.yaml")
        open(p, "w").write(mutate(
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
                    lambda: check_config(builder, p))


def main():
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
            self_test()
    print("-" * 70)
    print(f"checks: {checks}   failures: {len(fails)}")
    for f in fails:
        print(f"  {f}")
    print(f"RESULT: {'FAIL' if fails else 'PASS'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

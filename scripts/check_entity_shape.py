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
sw/builder/endstation_builder.py emits BOTH this shape's
hdl/common/csr/gen/adp_shape_defaults.svh (which milan_csr and milan_datapath
`include) AND this shape's hdl/ieee17221/aecp/gen/aecp_aem_rom.svh, in one
pass from one config.  This gate is what makes "one pass, one config" checkable.

WHAT IT CHECKS, per end-station config:

  A  generated svh    the shape include the builder emits for this config
                      carries the counts adp_shape() computes from it, and
                      names the config it came from
  B  AEM model        this config's AEM overlay declares the same
                      STREAM_OUTPUT / STREAM_INPUT counts, and its
                      entity_counts agree with its descriptor_counts
  C  AEM ROM          the ROM the builder generates for this config has that
                      many STREAM_OUTPUT / STREAM_INPUT descriptors - the
                      descriptor set a controller enumerates
  D  per-config copy  configs/generated/<name>/gen/adp_shape_defaults.svh on
                      disk is byte-identical to the freshly generated text
                      (harnesses and builds select a shape by include path)
  E  tracked pair     hdl/common/csr/gen/adp_shape_defaults.svh and
                      hdl/ieee17221/aecp/gen/aecp_aem_rom.svh both name the
                      SAME source config and match what it generates - a
                      gateware cannot carry one shape's counts and another
                      shape's descriptors
  F  RTL consumption  milan_csr builds 0x618/0x61C from the generated
                      constants and has a defaults arm, NO write arm and NO
                      is_plain_rw entry for either; milan_datapath sizes its
                      ACMP context arrays from the SAME constants, so the
                      advertised range is the addressable range
  G  firmware version the ENTITY descriptor's firmware_version (1722.1-2021
                      7.2.1, offset 116) names the gateware's OWN VERSION
                      parameter, in the tracked ROM and in the TB golden
                      alike, and no config declares one of its own

THE SAME DEFECT, ONE FIELD OVER (G, 2026-07-28).  All three configs hardcoded
`firmware_version: "0.1.0"` while hdl/common/csr/milan_csr.sv said
32'h0001_0016, and the AEM generator stamped the config's string into the
descriptor - so every board we ship told Hive, la_avdecc and every other
controller on the segment that it ran firmware 0.1.0.  Every gate was green,
because every gate compared that declaration against another declaration.
The version is now DERIVED from the parameter (major.minor.rev =
VERSION[31:16].VERSION[15:0].entity.firmware_rev, so 0x0001_0016 -> "1.22.0")
and arm G reads it back out of the shipped descriptor BYTES.  Note the TB
golden is checked here and not by the aecp suite: that sweep deliberately
EXCLUDES the ENTITY descriptor from its byte-exact compare because it carries
live overlays, so a golden that is stale only inside ENTITY passes there.

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
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAPATH = os.path.join(ROOT, "hdl/milan/milan_datapath.sv")
CSR = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")
AEM_ROM = os.path.join(ROOT, "hdl/ieee17221/aecp/gen/aecp_aem_rom.svh")
AEM_GOLDEN = os.path.join(ROOT, "tb/verilator/aecp/aem_golden.h")
CONFIG_DIR = os.path.join(ROOT, "configs")

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

    `endstation_builder.py --write-rtl <cfg>` installs the tracked pair for
    WHICHEVER config it is handed, so the owner is not a constant a gate may
    assume: it is a fact the tree records.  The AEM ROM carries no marker of
    its own (its header names avdecc/gen_aem_store.py, the generator, not the
    config), so the shape include's `Source :` line is the ONE place the
    answer lives - and this is the ONE reader of it, shared with
    sw/builder/test_builder.py gate 10.  Two answers to "who owns the tracked
    ROM" is exactly how a gate comes to assume a config: gate 10 hardcoded
    endstation_arty_current and went red for every other owner, blocking any
    other shape from being written into the tree at all.

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
    # This is the arm that would have caught an 8x8 build shipping the 1x1
    # ROM: the counts and the descriptors come from one pass or not at all.
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

    # D: the tracked per-config copy on disk is what the builder emits now
    p_cfg = os.path.join(ROOT, builder.GEN_CONFIG_DIR, name, "gen",
                         "adp_shape_defaults.svh")
    ck(f"{name}: configs/generated copy is current",
       os.path.exists(p_cfg) and open(p_cfg).read() == adp_svh, True)
    return cfg, adp_svh, builder.emit_aem_rom_svh(cfg, ovl)


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


def golden_rom(text):
    """(rom bytes, directory) out of tb/verilator/aecp/aem_golden.h - the
    image the aecp TB byte-compares the RTL against."""
    body = re.search(r"AEM_ROM\[\]\s*=\s*\{(.*?)\n\};", text, re.S)
    dirb = re.search(r"AEM_DIR\[\]\s*=\s*\{(.*?)\n\};", text, re.S)
    if not body or not dirb:
        raise SystemExit("SETUP: no AEM_ROM / AEM_DIR in the golden header")
    rom = bytes(int(b, 16)
                for b in re.findall(r"0x([0-9A-Fa-f]{2})", body.group(1)))
    return rom, _dir_entries(
        dirb.group(1), r"\{\s*0x([0-9A-Fa-f]{4})\s*,\s*(\d+)\s*,"
                       r"\s*(\d+)\s*,\s*(\d+)\s*\}")


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
    the RTL and the string out of the TRACKED DESCRIPTOR BYTES - the ROM the
    gateware compiles and the golden image the aecp TB byte-compares the RTL
    against - which makes "VERSION bumped, artifacts not regenerated" a
    build failure instead of a wrong answer on the wire.

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

    # 2. the DESCRIPTOR BYTES a build serves, and the ones the TB pins.
    tracked = open(AEM_ROM).read()
    golden = open(AEM_GOLDEN).read()
    rom_t, dir_t = svh_rom(tracked)
    rom_g, dir_g = golden_rom(golden)
    owner = tracked_owner_cfg(builder, all_configs())
    want = (g.firmware_version_string(owner["entity"]["firmware_rev"], CSR)
            if owner else None)

    for what, rom, drc in (("tracked ROM", rom_t, dir_t),
                           ("TB golden", rom_g, dir_g)):
        fld = entity_fw_field(rom, drc, what)
        ck(f"{what}: firmware_version field is {FW_LEN} octets",
           len(fld), FW_LEN)
        # 7.2: zero padded after the string, and no interior NUL
        s = fld.split(b"\x00", 1)[0]
        ck(f"{what}: firmware_version is zero padded past the string (7.2)",
           fld[len(s):] == bytes(FW_LEN - len(s)), True)
        ck(f"{what}: firmware_version decodes as UTF-8 (7.2.1)",
           _utf8(s), True)
        ck(f"{what}: firmware_version == the gateware's VERSION",
           s.decode("utf-8", "replace"), want)

    # 3. and the golden is THIS ROM's, not a previous one's. Regenerating the
    #    ROM without regenerating the golden produces N byte-exact aecp
    #    failures at the changed offset and nothing else; catching it here
    #    names the cause instead of leaving it to a suite diff.
    ck("TB golden image == the tracked AEM ROM", rom_g == rom_t, True)


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


def check_tracked_pair(builder, configs):
    """E: the tracked entity definition is ONE config's, whole.

    hdl/common/csr/gen/adp_shape_defaults.svh and
    hdl/ieee17221/aecp/gen/aecp_aem_rom.svh are what a build `include-s. They
    must name the same source config AND be exactly what that config
    generates - otherwise the gateware advertises one shape and enumerates
    another, which is the 2026-07-27 defect with the layers swapped."""
    print("\n== tracked entity definition (what a build includes) ==")
    adp = open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read()
    rom = open(os.path.join(ROOT, builder.AEM_ROM_REL)).read()
    src, owner = tracked_owner(builder, adp_text=adp, configs=configs)
    print(f"  tracked shape source: {src}")
    ck("tracked ADP shape names a source config", src is not None, True)
    ck(f"tracked shape's source config exists ({src})", owner is not None, True)
    if owner is None:
        return
    ovl = builder.emit_aem_overlay(owner)
    ck("tracked ADP shape == what that config generates",
       adp == builder.emit_adp_shape_svh(owner), True)
    ck("tracked AEM ROM == what that config generates",
       rom == builder.emit_aem_rom_svh(owner, ovl), True)
    got = svh_shape(adp, "tracked shape")
    rc = rom_descriptor_counts(rom)
    ck("tracked ROM STREAM_OUTPUT == tracked advertised sources",
       rc.get(STREAM_OUTPUT, 0), got["talker_stream_sources"])
    ck("tracked ROM STREAM_INPUT == tracked advertised sinks",
       rc.get(STREAM_INPUT, 0), got["listener_stream_sinks"])


def check_built_config(builder, path):
    """Pre-build gate: the tracked entity definition IS the config being
    built. Without this a `build.sh ax8x8` silently inherits whatever shape
    was last committed - exactly how an 8x8 gateware came to carry a 1x1
    descriptor set. The fix is one command, and the message says it."""
    cfg = builder.load_config(path)
    print(f"\n== pre-build: tracked definition vs {cfg['name']} ==")
    adp = open(os.path.join(ROOT, builder.ADP_SHAPE_REL)).read()
    rom = open(os.path.join(ROOT, builder.AEM_ROM_REL)).read()
    ovl = builder.emit_aem_overlay(cfg)
    ok_adp = adp == builder.emit_adp_shape_svh(cfg)
    ok_rom = rom == builder.emit_aem_rom_svh(cfg, ovl)
    ck(f"tracked ADP shape is {cfg['name']}'s", ok_adp, True)
    ck(f"tracked AEM ROM is {cfg['name']}'s", ok_rom, True)
    if not (ok_adp and ok_rom):
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
    check_rtl_wiring()
    cfgs = all_configs()
    for p in cfgs:
        check_config(builder, p)
    check_tracked_pair(builder, cfgs)
    check_firmware_version(builder)


# ---------------------------------------------------------------- self-test --
def mutate(text, old, new):
    if old not in text:
        raise SystemExit(f"SELF-TEST SETUP: {old!r} not in the source")
    return text.replace(old, new, 1)


def expect_fail(label, fn):
    """Run a mutated world and require the pipeline to REJECT it.

    A rejection counts whether it comes from this gate's own comparisons or
    from the builder refusing to load the config - both stop the build."""
    global fails, checks, quiet
    saved_f, saved_c, saved_q = fails, checks, quiet
    fails, checks, quiet = [], 0, True
    try:
        fn()
    except Exception as e:                            # noqa: BLE001
        fails.append(f"{type(e).__name__}: {e}")
    caught, why = bool(fails), (fails[0] if fails else "")
    fails, checks, quiet = saved_f, saved_c, saved_q
    ck(f"MUTATION rejected: {label}", caught, True)
    if caught:
        print(f"         (rejected by: {why})")


def with_rtl(dp_text=None, csr_text=None, golden_text=None):
    """Context-manager-ish helper: swap in mutated sources for one call."""
    global DATAPATH, CSR, AEM_GOLDEN
    keep = (DATAPATH, CSR, AEM_GOLDEN)
    td = tempfile.mkdtemp()
    if dp_text is not None:
        DATAPATH = os.path.join(td, "milan_datapath.sv")
        open(DATAPATH, "w").write(dp_text)
    if csr_text is not None:
        CSR = os.path.join(td, "milan_csr.sv")
        open(CSR, "w").write(csr_text)
    if golden_text is not None:
        AEM_GOLDEN = os.path.join(td, "aem_golden.h")
        open(AEM_GOLDEN, "w").write(golden_text)

    def restore():
        global DATAPATH, CSR, AEM_GOLDEN
        DATAPATH, CSR, AEM_GOLDEN = keep
        shutil.rmtree(td, ignore_errors=True)
    return restore


def self_test():
    """Mutation proof: six ways the shape can disagree, each must FAIL."""
    print("\n== self-test: a disagreeing shape must be REJECTED ==")
    builder = load_builder()
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

    # 4. the tracked entity definition split in half: the shape include from
    #    one config, the descriptor ROM from another. This is the 8x8-build-
    #    with-a-1x1-ROM defect stated exactly.
    keep = builder.AEM_ROM_REL
    with tempfile.TemporaryDirectory() as td:
        other = builder.load_config(os.path.join(CONFIG_DIR,
                                                 "endstation_arty_4x4.yaml"))
        rom4 = os.path.join(td, "rom.svh")
        open(rom4, "w").write(builder.emit_aem_rom_svh(
            other, builder.emit_aem_overlay(other)))
        builder.AEM_ROM_REL = os.path.relpath(rom4, ROOT)
        try:
            expect_fail("tracked ROM is a DIFFERENT config's than the shape",
                        lambda: check_tracked_pair(builder, all_configs()))
        finally:
            builder.AEM_ROM_REL = keep

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
    #    entity definition is not regenerated, so the descriptor keeps
    #    telling controllers the old number. Read the current literal out of
    #    the RTL rather than naming it - naming it here would be a second
    #    copy of exactly the constant this gate exists to keep singular.
    cur = re.search(r"(parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*32'h)"
                    r"([0-9A-Fa-f_]+)", base_csr)
    if not cur:
        raise SystemExit("SELF-TEST SETUP: no VERSION parameter in milan_csr")
    restore = with_rtl(csr_text=mutate(
        base_csr, cur.group(0), cur.group(1) + "0002_0003"))
    try:
        expect_fail("milan_csr VERSION bumped, entity NOT regenerated",
                    lambda: check_firmware_version(builder))
    finally:
        restore()

    # 8. the stale-golden trap, stated: the ROM is regenerated and the TB
    #    golden is not. Flip one octet INSIDE the firmware_version field.
    base_gold = open(AEM_GOLDEN).read()
    rom_g, dir_g = golden_rom(base_gold)
    stale = entity_fw_field(rom_g, dir_g, "TB golden")[:1].hex().upper()
    restore = with_rtl(golden_text=mutate(
        base_gold, f"0x{stale}", "0x30"))            # '1' -> '0': "0.22.0"
    try:
        expect_fail("TB golden not regenerated with the AEM ROM",
                    lambda: check_firmware_version(builder))
    finally:
        restore()

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
            '    - { name: "Stream In 7", channels: 8, map_mode: dynamic, '
            'formats: ["0x0205022002006000", "0x0215022002006000"] }\n', ""))
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

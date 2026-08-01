# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
# BDD steps for the ENTITY descriptor's firmware_version field.
# Spec refs: IEEE 1722.1-2021 7.2.1 Table 7-2 (offset 116, 64 octets) and 7.2
# (zero padding); Milan end-station Validation Test plan v1.9 test macro 3.
#
# These steps read the ENTITY descriptor out of the artifacts a build actually
# ships - hdl/ieee17221/aecp/gen/aecp_aem_rom.svh, the ROM the gateware
# compiles, and tb/verilator/aecp/aem_golden.h, the image the aecp TB pins -
# and compare the field against hdl/common/csr/milan_csr.sv's VERSION
# parameter. Nothing here re-derives the version: a controller cannot see a
# builder, it sees these bytes.

import os
import re

from behave import given, when, then

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

AEM_ROM_SVH = os.path.join(ROOT, "hdl/ieee17221/aecp/gen/aecp_aem_rom.svh")
AEM_GOLDEN_H = os.path.join(ROOT, "tb/verilator/aecp/aem_golden.h")
#: the shape the golden's consumer (the aecp harness) actually compiles
HARNESS_ROM_SVH = os.path.join(
    ROOT, "configs/generated/endstation_arty_current/gen/aecp_aem_rom.svh")
MILAN_CSR_SV = os.path.join(ROOT, "hdl/common/csr/milan_csr.sv")

ENTITY_DESC = 0x0000
FW_OFFSET, FW_LEN = 116, 64          # 1722.1-2021 Table 7-2


def _rom_from_svh(text):
    body = re.search(r"AEM_ROM_INIT_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\n\};",
                     text, re.S)
    dirb = re.search(r"AEM_DIR_C\s*\[[^\]]*\]\s*=\s*'\{(.*?)\n\};", text, re.S)
    assert body and dirb, "aecp_aem_rom.svh has no ROM / directory block"
    rom = bytes(int(b, 16)
                for b in re.findall(r"8'h([0-9A-Fa-f]{2})", body.group(1)))
    dirs = [(int(t, 16), int(i, 16), int(b, 16), int(ln, 16))
            for t, i, b, ln in re.findall(
                r"64'h([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})_"
                r"([0-9A-Fa-f]{4})_([0-9A-Fa-f]{4})", dirb.group(1))]
    return rom, dirs


def _rom_from_golden(text):
    body = re.search(r"AEM_ROM\[\]\s*=\s*\{(.*?)\n\};", text, re.S)
    dirb = re.search(r"AEM_DIR\[\]\s*=\s*\{(.*?)\n\};", text, re.S)
    assert body and dirb, "aem_golden.h has no ROM / directory block"
    rom = bytes(int(b, 16)
                for b in re.findall(r"0x([0-9A-Fa-f]{2})", body.group(1)))
    dirs = [(int(t, 16), int(i), int(b), int(ln))
            for t, i, b, ln in re.findall(
                r"\{\s*0x([0-9A-Fa-f]{4})\s*,\s*(\d+)\s*,\s*(\d+)\s*,"
                r"\s*(\d+)\s*\}", dirb.group(1))]
    return rom, dirs


def _descriptor(rom, dirs, dtype, index):
    hit = [(b, ln) for (t, i, b, ln) in dirs if t == dtype and i == index]
    assert hit, f"descriptor 0x{dtype:04X}[{index}] is not in the directory"
    b, ln = hit[0]
    return rom[b:b + ln]


def _rtl_version():
    m = re.search(r"parameter\s+logic\s*\[31:0\]\s+VERSION\s*=\s*"
                  r"32'h([0-9A-Fa-f_]+)", open(MILAN_CSR_SV).read())
    assert m, "milan_csr.sv has no VERSION parameter"
    v = int(m.group(1).replace("_", ""), 16)
    return (v >> 16) & 0xFFFF, v & 0xFFFF


# --------------------------------------------------------------------------
@given('the entity definition this gateware serves')
def step_load_entity(context):
    rom, dirs = _rom_from_svh(open(AEM_ROM_SVH).read())
    context.aem_rom, context.aem_dir = rom, dirs
    context.fw_major, context.fw_minor = _rtl_version()


@given('the entity definition still declares firmware_version "{value}"')
def step_stale_entity(context, value):
    """The pre-2026-07-28 world, byte for byte: an ENTITY descriptor whose
    firmware_version is a hand-typed constant instead of the gateware's."""
    rom, dirs = _rom_from_svh(open(AEM_ROM_SVH).read())
    base = [b for (t, i, b, _l) in dirs if (t, i) == (ENTITY_DESC, 0)][0]
    padded = value.encode() + bytes(FW_LEN - len(value.encode()))
    rom = (rom[:base + FW_OFFSET] + padded
           + rom[base + FW_OFFSET + FW_LEN:])
    context.aem_rom, context.aem_dir = rom, dirs
    context.fw_major, context.fw_minor = _rtl_version()


@when('a controller READ_DESCRIPTORs the ENTITY descriptor')
def step_read_entity(context):
    context.entity_desc = _descriptor(context.aem_rom, context.aem_dir,
                                      ENTITY_DESC, 0)


@then('the firmware_version field is {n:d} octets at offset {off:d}')
def step_field_geometry(context, n, off):
    assert len(context.entity_desc) >= off + n, (
        f"ENTITY descriptor is {len(context.entity_desc)} B - too short to "
        f"hold a {n}-octet field at offset {off}")
    context.fw_field = context.entity_desc[off:off + n]
    assert len(context.fw_field) == n


@then('the firmware_version is a NUL-terminated UTF-8 string, zero padded')
def step_field_encoding(context):
    s = context.fw_field.split(b"\x00", 1)[0]
    assert context.fw_field[len(s):] == bytes(len(context.fw_field) - len(s)), (
        "1722.1-2021 7.2: the remainder of a short 64-octet string field "
        "shall be zero (0) padded")
    context.fw_string = s.decode("utf-8")     # raises if not valid UTF-8


@then('the firmware_version names the gateware VERSION register')
def step_field_matches_rtl(context):
    want = f"{context.fw_major}.{context.fw_minor}.0"
    assert context.fw_string == want, (
        f"the entity tells controllers it runs firmware "
        f"{context.fw_string!r} while milan_csr VERSION says "
        f"0x{context.fw_major:04X}_{context.fw_minor:04X} = {want!r}")


@then('the firmware_version contradicts the gateware VERSION register')
def step_field_contradicts_rtl(context):
    want = f"{context.fw_major}.{context.fw_minor}.0"
    assert context.fw_string != want, (
        "the negative control did not contradict anything - this scenario "
        "cannot prove the positive one can fail")


@then('the TB golden image serves the same ENTITY descriptor')
def step_golden_agrees(context):
    # The golden's identity follows its CONSUMER (the aecp harness compiles
    # configs/generated/endstation_arty_current), NOT the tracked pair,
    # whose owner is whichever config last ran --write-rtl (the ax7101_8x8
    # ship since 08-01). What this pins is staleness: a VERSION bump that
    # regenerates the shape but not the golden.
    h_rom, h_dir = _rom_from_svh(open(HARNESS_ROM_SVH).read())
    g_rom, g_dir = _rom_from_golden(open(AEM_GOLDEN_H).read())
    assert (_descriptor(g_rom, g_dir, ENTITY_DESC, 0)
            == _descriptor(h_rom, h_dir, ENTITY_DESC, 0)), (
        "tb/verilator/aecp/aem_golden.h is not the harness shape's: the "
        "aecp TB EXCLUDES the ENTITY descriptor from its byte-exact sweep "
        "(it carries live overlays), so a stale golden is silent there")
    # and the golden's firmware_version is the SAME derived string the
    # tracked entity serves - one VERSION register, however many shapes
    base = [b for (t, i, b, _l) in g_dir if (t, i) == (ENTITY_DESC, 0)][0]
    fld = g_rom[base + FW_OFFSET:base + FW_OFFSET + FW_LEN]
    want = f"{context.fw_major}.{context.fw_minor}.0"
    assert fld.split(b"\x00", 1)[0].decode() == want, (
        f"golden firmware_version != gateware VERSION {want}")

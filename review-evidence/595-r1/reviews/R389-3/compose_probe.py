#!/usr/bin/env python3
"""Composition probe: stricter declaration parsing (#595) against the shipping
image check (#577) in one builder. Run from a repository root; writes only
temporary files.

Checks:
 A. each tracked config loads, and _entity_model_image() invokes
    validate_shipping_image() exactly once and accepts;
 B. non-string MAC / vendor_oui / entity_capabilities and scalar formats are
    refused by load_config() with the #595 message, and the image check is
    never reached (parse refusal is not masked by, nor masks, the image check);
 C. quoted spellings of the same fields load and reach the image check, which
    accepts them;
 D. with a quoted declaration present, a damaged packed image is still
    refused by the image check under its own aem_desc.bin prefix.
"""
import copy
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402

calls = []
real_check = eb.aem_image_checks.validate_shipping_image


def counting_check(blob):
    calls.append(len(blob))
    return real_check(blob)


QUOTE = "quote the hexadecimal value as a YAML string"
failures = []


def expect(cond, msg):
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        failures.append(msg)


def image(cfg):
    return eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]


with patch.object(eb.aem_image_checks, "validate_shipping_image", counting_check), \
        tempfile.TemporaryDirectory(prefix="compose-probe.") as tmp:
    tmp = Path(tmp)
    # A
    for config in sorted((ROOT / "configs").glob("endstation_*.yaml")):
        cfg = eb.load_config(str(config))
        before = len(calls)
        image(cfg)
        expect(len(calls) == before + 1, f"A {config.name}: image check ran once and accepted")

    base_text = (ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text()
    base = yaml.safe_load(base_text)

    def variant(keys, token):
        doc = copy.deepcopy(base)
        node = doc
        for k in keys[:-1]:
            node = node[k]
        node[keys[-1]] = "SLOT__"
        text = yaml.safe_dump(doc).replace("SLOT__", token)
        path = tmp / "v.yaml"
        path.write_text(text)
        return path

    # B
    talker_formats = None
    for i, t in enumerate(base.get("streams", {}).get("talkers", [])):
        talker_formats = ("streams", "talkers", i, "formats")
        break
    refusals = [
        (("platform", "mac_address"), "020000000002", f"platform.mac_address: {QUOTE}"),
        (("platform", "mac_address"), "10:20:30:40:50:02", f"platform.mac_address: {QUOTE}"),
        (("entity", "vendor_oui"), "0x001BC5", f"entity.vendor_oui: {QUOTE}"),
        (("entity", "vendor_oui"), "true", f"entity.vendor_oui: {QUOTE}"),
        (("entity", "entity_capabilities"), "0x8", f"entity.entity_capabilities: {QUOTE}"),
        (("entity", "entity_capabilities"), "null", f"entity.entity_capabilities: {QUOTE}"),
    ]
    for keys, token, message in refusals:
        before = len(calls)
        try:
            eb.load_config(str(variant(keys, token)))
        except eb.ConfigError as exc:
            got = str(exc)
        else:
            got = "ACCEPTED"
        expect(got == message and len(calls) == before,
               f"B {'.'.join(map(str, keys))}={token}: refused '{got}', image check not reached")
    if talker_formats:
        for token in ('"0x0205022002006000"', "0x0205022002006000", "7"):
            before = len(calls)
            try:
                eb.load_config(str(variant(talker_formats, token)))
            except eb.ConfigError as exc:
                got = str(exc)
            else:
                got = "ACCEPTED"
            expect("formats: must be a list of quoted hexadecimal strings" in got and len(calls) == before,
                   f"B talker formats scalar {token}: refused '{got}'")

    # C
    oui = f"0x{eb.MODEL_ID_OUI:06X}"
    caps = f"0x{eb._aemi().adp_entity_capabilities():08X}" if hasattr(eb, "_aemi") else None
    accepted = [(("platform", "mac_address"), '"02-00-00-00-00-02"'),
                (("entity", "vendor_oui"), f'"{oui}"')]
    for keys, token in accepted:
        cfg = eb.load_config(str(variant(keys, token)))
        before = len(calls)
        image(cfg)
        expect(len(calls) == before + 1, f"C {'.'.join(keys)}={token}: loaded, image checked and accepted")

    # D: damaged packing after a quoted declaration still refuses at the image check
    import gen_desc_image as packer
    cfg = eb.load_config(str(variant(("entity", "vendor_oui"), f'"{oui}"')))
    real_build = packer.build

    def damaged(document, *a, **k):
        blob, report = real_build(document, *a, **k)
        return blob[:-4] + bytes(4) if len(blob) > 64 else blob, report

    rows = []

    def corrupt_l10(document, *a, **k):
        import struct
        doc = copy.deepcopy(document)
        for row in doc["descriptors"]:
            if row["type"] == 0x0002:
                body = bytearray.fromhex(row["bytes"])
                struct.pack_into(">H", body, 140, 143)
                row["bytes"] = body.hex()
                rows.append(row["index"])
        return real_build(doc, *a, **k)

    with patch.object(packer, "build", side_effect=corrupt_l10):
        try:
            image(cfg)
        except eb.ConfigError as exc:
            got = str(exc)
        else:
            got = "ACCEPTED"
    expect(got.startswith("aem_desc.bin: L10_OFFSET") and rows,
           f"D quoted OUI + damaged AUDIO_UNIT rate offset: refused '{got[:80]}'")

print(f"image-check invocations: {len(calls)}; failures: {len(failures)}")
sys.exit(1 if failures else 0)

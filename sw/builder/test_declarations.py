# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Executable declaration contracts for #400 and #403 (builder gate 40)."""
import copy
from pathlib import Path
import re
import struct
import sys
import tempfile
from unittest.mock import patch

import yaml
import endstation_builder as eb

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from pp_srcs import pp_sources  # noqa: E402

sys.path.insert(0, str(ROOT / "sw/litex"))
from boot_policy import fabric_constants  # noqa: E402


def _load(raw, directory):
    path = directory / "case.yaml"
    path.write_text(yaml.safe_dump(raw))
    return eb.load_config(path)



def _refused(raw, directory, field, rule):
    """Require the owning refusal, never an unrelated exception or guard."""
    try:
        _load(raw, directory)
    except eb.ConfigError as exc:
        assert field in str(exc) and rule in str(exc), (field, rule, str(exc))
    else:
        raise AssertionError(f"accepted invalid {field}: {rule}")


def test_model_id_contract() -> None:
    """Milan 5.3.3.1/5.6.2 endpoints; Table 7-2 ENTITY and ADP identity equality."""
    import gen_aemi_image as join

    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="model-id-contract.") as tmp:
        directory = Path(tmp)
        for key in ("entity_model_id", "model_id_pin"):
            raw = copy.deepcopy(base)
            raw["entity"].pop("model_id_pin", None)
            # Independent EUI-64 endpoints and adjacent legal values, per
            # Milan 5.3.3.1 (ENTITY) and 5.6.2 (ADPDU). Importing the guard's bounds would hide drift.
            for value in ("0x0000000000000001", "0xFFFFFFFFFFFFFFFE", "0x001BC50AC1000005"):
                raw["entity"][key] = value
                cfg = _load(raw, directory)
                assert cfg["entity"]["entity_model_id"] == value
                overlay = eb.emit_aem_overlay(cfg)
                document = join.model_to_document(
                    join.aem.build_model(join.aem.spec_from_overlay(overlay)),
                    join.identity_from_overlay(overlay))
                blob, _ = join.image.build(document, 576)
                row = int.from_bytes(blob[12:16], "big")
                assert blob[row:row + 4] == bytes(4), "first row must be ENTITY[0]"
                offset = int.from_bytes(blob[row + 8:row + 12], "big")
                assert blob[offset + 12:offset + 20] == int(value, 16).to_bytes(8, "big")
                constants = fabric_constants(overlay, eb.emit_lwsrp_table(cfg))
                assert (constants["MILAN_MODEL_ID_HI"] << 32
                        | constants["MILAN_MODEL_ID_LO"]) == int(value, 16)
            for value in ("0x0000000000000000", "0xFFFFFFFFFFFFFFFF"):
                raw["entity"][key] = value
                _refused(raw, directory, f"entity.{key}", "must not be zero or all ones")
    print("[F1] literal/pinned legal IDs, ENTITY/ADP equality, four endpoint refusals")


def test_model_id_resolution_contract() -> None:
    """Shadowed literals and derived IDs share validity rules."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="model-id-resolution.") as tmp:
        directory = Path(tmp)
        raw = copy.deepcopy(base)
        raw["entity"].update(model_id_pin="0x001BC50AC1000005")
        for value in ("0x0000000000000000", "0xFFFFFFFFFFFFFFFF"):
            raw["entity"]["entity_model_id"] = value
            _refused(raw, directory, "entity.entity_model_id", "must not be zero or all ones")
        raw["entity"]["entity_model_id"] = "0x001BC50000000001"
        assert _load(raw, directory)["entity"]["entity_model_id"] == "0x001BC50AC1000005"
        raw["entity"].pop("model_id_pin")
        raw["entity"]["entity_model_id"] = "hash-derived"
        for value in (0, 0xFFFFFFFFFFFFFFFF):
            with patch.object(eb, "derive_model_id", return_value=value):
                _refused(raw, directory, "entity.entity_model_id", "must not be zero or all ones")
        with patch.object(eb, "derive_model_id", return_value=0x001BC50000000001):
            assert _load(raw, directory)["entity"]["entity_model_id"] == "0x001BC50000000001"
    print("[F1] shadowed literals and derived endpoints refused")


#: (key path, field, legal value, width in bits) of every quoted 64- and 48-bit
#: hex field. The widths are the fields' own: EUI-64 identities and 1722.1
#: stream format words are 64 bits, and the stream DMAC is a MAC-48.
HEX_FIELDS = (
    (("entity", "entity_model_id"), "entity.entity_model_id", "0x001BC50AC1000005", 64),
    (("entity", "model_id_pin"), "entity.model_id_pin", "0x001BC50AC1000005", 64),
    (("entity", "entity_id"), "entity.entity_id", "0x001BC50AC1000005", 64),
    (("srp", "stream_dmac_base"), "srp.stream_dmac_base", "0x91E0F000FE01", 48),
    (("streams", "talkers", 0, "formats", 0), "streams.talkers[0].formats",
     "0x0205022000806000", 64),
    (("streams", "listeners", 0, "formats", 0), "streams.listeners[0].formats",
     "0x0205022000806000", 64),
    (("clocking", "crf_format"), "clocking.crf_format", "0x041060010000BB80", 64),
    (("clocking", "crf_output", "format"), "clocking.crf_output.format",
     "0x041060010000BB80", 64),
)


def _hex_field_base() -> dict:
    """arty_4x4 with one explicit format per direction and no pin or OUI, so
    every HEX_FIELDS value is the only one deciding its field."""
    raw = yaml.safe_load((ROOT / "configs/endstation_arty_4x4.yaml").read_text())
    raw["entity"].pop("model_id_pin", None)
    raw["entity"].pop("vendor_oui", None)
    for direction in ("talkers", "listeners"):
        raw["streams"][direction][0]["formats"] = ["0x0205022000806000"]
    return raw


def test_hex_scalar_contract() -> None:
    """Preserve hex string digits; reject YAML numbers before field semantics."""
    with tempfile.TemporaryDirectory(prefix="hex-scalar-contract.") as tmp:
        path = Path(tmp) / "scalar.yaml"
        for keys, field, legal, _bits in HEX_FIELDS:
            # The shared parser's result is independent of MAC width or family.
            # Those later rules cannot accept an arbitrary legal 64-bit number.
            for spelling in ("0x001BC50AC1000005", "1234567890123456",
                             "0012345670123456", "0x001B_C50A_C100_0005"):
                value = yaml.safe_load(f'"{spelling}"')
                assert eb._eui64(value, field) == int(spelling, 16)
                assert eb._fmt64(value, field) == f"0x{int(spelling, 16):016X}"
            raw = _hex_field_base()
            node = raw
            for key in keys[:-1]:
                node = node[key]
            node[keys[-1]] = "HEX_SLOT"
            template = yaml.safe_dump(raw)
            assert template.count("HEX_SLOT") == 1
            for spelling in (legal, legal.removeprefix("0x")):
                path.write_text(template.replace("HEX_SLOT", f'"{spelling}"'))
                cfg = eb.load_config(path)
                if keys[0] == "entity":
                    resolved = "entity_id" if keys[-1] == "entity_id" else "entity_model_id"
                    assert cfg["entity"][resolved] == legal
            if keys[0] == "entity":
                path.write_text(template.replace("HEX_SLOT", '"1234567890123456"'))
                assert eb.load_config(path)["entity"][resolved] == "0x1234567890123456"
            for spelling in (legal, "1234567890123456", "0012345670123456",
                             "0", "18446744073709551615", "true", "null", "1.5", "[]", "{}"):
                path.write_text(template.replace("HEX_SLOT", spelling))
                try:
                    eb.load_config(path)
                except eb.ConfigError as exc:
                    assert field in str(exc) and "quote" in str(exc), (field, spelling, str(exc))
                else:
                    raise AssertionError(f"accepted non-string {field}: {spelling}")
    print("[F1] eight hex fields: strings preserve digits; non-strings receive named quote refusals")


def test_aem_u32_contract() -> None:
    """Every AEM u32 preserves legal values and refuses unsigned overflow."""
    from aem_descriptors import be32

    for value in (0, 1, 2126000, 0xFFFFFFFF):
        assert be32(value) == value.to_bytes(4, "big")
    for value in (-1, -(1 << 32), 1 << 32, (1 << 32) + 2125999, 1 << 64):
        try:
            be32(value)
        except struct.error:
            pass
        else:
            raise AssertionError(f"AEM u32 silently truncated {value}")
    print("[u32] zero/maximum pack unchanged; negative and overflowing fields refuse")


def _yaml_template(raw, keys):
    """Keep the tested token's YAML spelling intact through the loader."""
    document = copy.deepcopy(raw)
    node = document
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = "YAML_SLOT"
    template = yaml.safe_dump(document)
    assert template.count("YAML_SLOT") == 1
    return template


def _yaml_refused(path, template, spelling, message):
    """An exact named refusal must replace acceptance or incidental errors."""
    path.write_text(template.replace("YAML_SLOT", spelling))
    try:
        eb.load_config(path)
    except eb.ConfigError as exc:
        assert str(exc) == message, (spelling, message, str(exc))
    else:
        raise AssertionError(f"accepted {spelling}: expected {message}")


def test_station_mac_string_contract() -> None:
    """Quoted station addresses preserve digits; YAML scalar coercion refuses."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    template = _yaml_template(base, ("platform", "mac_address"))
    field = "platform.mac_address"
    with tempfile.TemporaryDirectory(prefix="mac-string-contract.") as tmp:
        path = Path(tmp) / "case.yaml"
        for spelling, expected in (
                ("0x020000000002", 0x020000000002),
                ("020000000002", 0x020000000002),
                ("02:00:00:00:00:02", 0x020000000002),
                ("02-00-00-00-00-02", 0x020000000002),
                ("0x0200_0000_0002", 0x020000000002),
                ("123456789012", 0x123456789012),
                ("0x000000F42402", 0x000000F42402),
                ("10:20:30:40:50:02", 0x102030405002),
                ("0X020000000002", 0x020000000002),
                ("0200_0000_0002", 0x020000000002),
                ("02_00_00_00_00_02", 0x020000000002),
                ("0a-1B-2c-3D-4e-5F", 0x0A1B2C3D4E5F)):
            path.write_text(template.replace("YAML_SLOT", f'"{spelling}"'))
            cfg = eb.load_config(path)
            assert eb._mac48(spelling, field) == expected, spelling
            resolved = int(cfg["platform"]["mac_address"].replace(":", ""), 16)
            assert resolved == expected, (spelling, resolved, expected)
        for spelling in ("0x000000F42402", "0x020000000002", "020000000002",
                         "123456789012", "10:20:30:40:50:02", "0", "true", "false",
                         "null", "", "1.5", "[]", "{}"):
            assert not isinstance(yaml.safe_load(spelling), str), spelling
            _yaml_refused(path, template, spelling,
                          f"{field}: quote the hexadecimal value as a YAML string")
        omitted = copy.deepcopy(base)
        del omitted["platform"]["mac_address"]
        _refused(omitted, Path(tmp), field, "is required")
        for spelling, rule in (("000000000000", "is the all-zero MAC-48"),
                               ("00:00:00:00:00:00", "is the all-zero MAC-48"),
                               ("010000000001", "I/G bit"), ("xyz", "not a MAC-48")):
            base["platform"]["mac_address"] = spelling
            _refused(base, Path(tmp), field, rule)
    print("[595 MAC] twelve quoted values preserved; non-strings receive exact quote refusals")


#: #495 (disposition 5882165062): quoted MAC spellings refused by their shape,
#: under the rule each breaks. Every one is a YAML string, and the first of
#: each rule differs from a legal unicast MAC only by that fault.
MAC_SHAPE_REFUSALS = (
    ("sign", ("+020000000002", "-020000000002", "+02:00:00:00:00:02", "-2")),
    ("leading or trailing whitespace",
     (" 020000000002", "020000000002 ", "\t02:00:00:00:00:02", "02-00-00-00-00-02\n")),
    ("fewer than twelve digits", ("02000000002", "2", "0", "0x2")),
    ("more than twelve digits", ("0200000000002", "1000000000000", "0x0200_0000_0000_2")),
    ("short or unpadded octet",
     ("2:000:00:00:00:02", "0:2", "2:0:0:0:0:2", "02:00:00:00:02", "02:00:00:00:00:00:02")),
    ("mixed separators", ("02:00-00:00:00:02", "02-00:00:00:00:02")),
    ("separator next to an underscore",
     ("02:_00:00:00:00:02", "02_:00:00:00:00:02", "02-00-00-00-00_-02")),
    ("leading, trailing or doubled underscore",
     ("_020000000002", "020000000002_", "0200__00000002", "0x_020000000002")),
    ("prefix on octets", ("0x02:00:00:00:00:02",)),
)


def _set(raw: dict, keys: tuple, value: object) -> dict:
    """A copy of `raw` with the value at `keys` replaced."""
    document = copy.deepcopy(raw)
    node = document
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value
    return document


def _shape_refused(raw: dict, keys: tuple, spelling: str, directory: Path, prefix: str,
                   rule: str) -> None:
    """The loader refuses the quoted `spelling` with a message led by `prefix`."""
    assert yaml.safe_load(yaml.safe_dump(spelling)) == spelling, spelling
    try:
        _load(_set(raw, keys, spelling), directory)
    except eb.ConfigError as exc:
        assert str(exc).startswith(prefix), (rule, spelling, str(exc))
    else:
        raise AssertionError(f"accepted {spelling!r}: {rule}")


def test_mac_shape_contract() -> None:
    """#495: each refused MAC shape is named and refused before its value."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    keys, field = ("platform", "mac_address"), "platform.mac_address"
    with tempfile.TemporaryDirectory(prefix="mac-shape-contract.") as tmp:
        for rule, spellings in MAC_SHAPE_REFUSALS:
            for spelling in spellings:
                _shape_refused(base, keys, spelling, Path(tmp),
                               f"{field}: {spelling!r} is not a MAC-48 (", rule)
    count = sum(len(spellings) for _, spellings in MAC_SHAPE_REFUSALS)
    print(f"[495 MAC] {len(MAC_SHAPE_REFUSALS)} named shape rules, {count} spellings refused")


def _hex_shape_refusals(legal: str) -> tuple[tuple[str, str], ...]:
    """(rule, spelling) pairs of a `0x` legal value, each breaking one hex rule."""
    digits = legal.removeprefix("0x")
    first = next(c for c in digits if c.isdigit())
    return (
        ("sign", "+" + legal), ("sign", "+" + digits), ("sign", "-" + digits),
        ("leading whitespace", " " + legal), ("leading whitespace", "\t" + digits),
        ("trailing whitespace", legal + " "), ("trailing whitespace", digits + "\n"),
        ("leading underscore", "_" + digits), ("leading underscore", "0x_" + digits),
        ("trailing underscore", digits + "_"),
        ("doubled underscore", f"{digits[:2]}__{digits[2:]}"),
        ("non-ASCII digit", digits.replace(first, chr(0x0660 + int(first)), 1)),
        ("no digits", "0x"),
    )


def _assert_hex_shape(raw: dict, keys: tuple, field: str, legal: str, bits: int,
                      directory: Path) -> None:
    """#495: one field refuses every named hex shape, and a digit past its
    width even as a leading zero; the 0X prefix and grouping are accepted."""
    digits = legal.removeprefix("0x")
    assert len(digits) * 4 == bits, (field, legal, bits)
    for rule, spelling in _hex_shape_refusals(legal):
        _shape_refused(raw, keys, spelling, directory, f"{field}: {spelling!r} is not ", rule)
    for spelling in ("0x0" + digits, "0" + digits):
        _shape_refused(raw, keys, spelling, directory,
                       f"{field}: {spelling!r} is outside {bits} bits (", "digits past the width")
    for spelling in ("0X" + digits, f"0x{digits[:2]}_{digits[2:]}"):
        _load(_set(raw, keys, spelling), directory)


def test_hex_shape_contract() -> None:
    """#495: every quoted hex field refuses each named shape and its width."""
    oui_base = yaml.safe_load((ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
    fields = [(_hex_field_base(), *field) for field in HEX_FIELDS] + [
        (oui_base, ("entity", "vendor_oui"), "entity.vendor_oui", "0x123456", 24),
        (oui_base, ("entity", "entity_capabilities"), "entity.entity_capabilities",
         f"0x{_adp_caps():08X}", 32)]
    with tempfile.TemporaryDirectory(prefix="hex-shape-contract.") as tmp:
        for raw, keys, field, legal, bits in fields:
            _assert_hex_shape(raw, keys, field, legal, bits, Path(tmp))
    rules = {rule for rule, _ in _hex_shape_refusals("0x10")}
    print(f"[495 hex] {len(fields)} hex fields: {len(rules)} named shape rules and the width refused")


def _adp_caps() -> int:
    """ADP_ENTITY_CAPS_C as pp_adp_pkg declares it in the derived processor sources."""
    # Find the authority by its package declaration so source moves stay valid.
    sources = [(ROOT / path).read_text() for path in pp_sources()]
    packages = [source for source in sources
                if re.search(r"^\s*package\s+pp_adp_pkg\s*;", source, re.M)]
    assert len(packages) == 1, "expected one pp_adp_pkg in derived processor sources"
    matches = re.findall(r"ADP_ENTITY_CAPS_C\s*=\s*32'h([0-9A-Fa-f_]+)", packages[0])
    assert len(matches) == 1
    return int(matches[0], 16)


def test_declared_hex_string_contract() -> None:
    """Both declared unsigned callers require strings, including explicit nulls."""
    base = yaml.safe_load((ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
    caps = _adp_caps()
    with tempfile.TemporaryDirectory(prefix="declared-hex-contract.") as tmp:
        path = Path(tmp) / "case.yaml"
        for key, bits, expected in (("vendor_oui", 24, 0x123456),
                                    ("entity_capabilities", 32, caps)):
            field = f"entity.{key}"
            template = _yaml_template(base, ("entity", key))
            digits = f"{expected:0{bits // 4}X}"
            for spelling in (f"0x{digits}", digits, f"0x{digits[:2]}_{digits[2:]}"):
                path.write_text(template.replace("YAML_SLOT", f'"{spelling}"'))
                cfg = eb.load_config(path)
                assert eb._declared_uint(spelling, bits, field) == expected, spelling
                if key == "vendor_oui":
                    resolved = int(cfg["entity"]["entity_model_id"], 16) >> 40
                else:
                    blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
                    row = int.from_bytes(blob[12:16], "big")
                    assert blob[row:row + 4] == bytes(4), "first row must be ENTITY[0]"
                    offset = int.from_bytes(blob[row + 8:row + 12], "big")
                    resolved = int.from_bytes(blob[offset + 20:offset + 24], "big")
                assert resolved == expected, (field, spelling, resolved, expected)
            # Numeric-looking hex strings have their literal value even where
            # later capability/OUI semantics would refuse that particular value.
            for spelling, number in (("123456", 0x123456), ("001234", 0x001234),
                                      ("10_20", 0x1020), ("0", 0),
                                      (f"{(1 << bits) - 1:X}", (1 << bits) - 1)):
                assert eb._declared_uint(spelling, bits, field) == number, (field, spelling)
            for spelling in (f"0x{digits}", str(expected), "123456", "001234", "10:20:30",
                             "0", "true", "false", "null", "", "1.5", "[]", "{}"):
                assert not isinstance(yaml.safe_load(spelling), str), spelling
                _yaml_refused(path, template, spelling,
                              f"{field}: quote the hexadecimal value as a YAML string")
            for spelling in (f"{1 << bits:X}", f"0{digits}"):
                raw = copy.deepcopy(base)
                raw["entity"][key] = spelling
                _refused(raw, Path(tmp), field, f"outside {bits} bits")
            assert key not in base["entity"]
            _load(base, Path(tmp))
    print("[595 uint] OUI and capabilities strings preserve values; all non-strings refuse")


def test_formats_list_contract() -> None:
    """Every stream requires a list; empty or omitted lists keep defaults."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_4x4.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="formats-list-contract.") as tmp:
        path = Path(tmp) / "case.yaml"
        default = _load(base, Path(tmp))
        for direction in ("talkers", "listeners"):
            for index in range(len(base["streams"][direction])):
                keys = ("streams", direction, index, "formats")
                field = f"streams.{direction}[{index}].formats"
                template = _yaml_template(base, keys)
                for spelling in ('"0205022000806000"', '"0x0205022000806000"',
                                 "0x0205022000806000", "0205022000806000", "123456",
                                 "10:20:30", "0", "true", "false", "null", "", '""',
                                 "1.5", "{}", '{"0x0205022000806000": 1}'):
                    _yaml_refused(path, template, spelling,
                                  f"{field}: must be a list of quoted hexadecimal strings")
                for spelling in ("0x0205022000806000", "0205022000806000",
                                 "0x0205_0220_0080_6000"):
                    path.write_text(template.replace("YAML_SLOT", f'["{spelling}"]'))
                    cfg = eb.load_config(path)
                    assert cfg[direction][index]["formats"][0] == "0x0205022000806000", field
                _yaml_refused(path, template, "[0x0205022000806000]",
                              f"{field}: quote the hexadecimal value as a YAML string")
                raw = copy.deepcopy(base)
                stream = raw["streams"][direction][index]
                stream.pop("formats", None)
                omitted = _load(raw, Path(tmp))[direction][index]["formats"]
                stream["formats"] = []
                empty = _load(raw, Path(tmp))[direction][index]["formats"]
                assert omitted == empty == default[direction][index]["formats"], field
    print("[595 formats] all stream indices: list type, exact quoted values, defaults and element refusals")


def test_listener_buffer_contract() -> None:
    """Milan 5.3.3.4 floor and Table 7-8 width survive descriptor packing."""
    import gen_aemi_image as join

    base = yaml.safe_load((ROOT / "configs/endstation_ax7101_8x8.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="listener-buffer-contract.") as tmp:
        directory = Path(tmp)
        for index in range(len(base["streams"]["listeners"])):
            raw = copy.deepcopy(base)
            stream = raw["streams"]["listeners"][index]
            # Independent clause boundary, not the implementation's constant.
            for value in (2126000, 2126001, 0xFFFFFFFF):
                stream["buffer_length_ns"] = value
                cfg = _load(raw, directory)
                assert cfg["listeners"][index]["buffer_length_ns"] == value
                overlay = eb.emit_aem_overlay(cfg)
                assert overlay["stream_inputs"][index]["buffer_length_ns"] == value
                document = join.model_to_document(
                    join.aem.build_model(join.aem.spec_from_overlay(overlay)),
                    join.identity_from_overlay(overlay))
                blob, _ = join.image.build(document, 576)
                # Read the packed image directory and the independent Table 7-8
                # field at offset 128, rather than the overlay's declared value.
                start = int.from_bytes(blob[12:16], "big")
                entries = int.from_bytes(blob[8:10], "big")
                for row in range(start, start + 16 * entries, 16):
                    if blob[row:row + 4] == b"\x00\x00\x00\x05":
                        assert int.from_bytes(blob[row + 4:row + 6], "big") > index
                        stride = int.from_bytes(blob[row + 14:row + 16], "big")
                        offset = int.from_bytes(blob[row + 8:row + 12], "big") + index * stride
                        assert int.from_bytes(blob[offset + 128:offset + 132], "big") == value
                        break
                else:
                    raise AssertionError(f"missing packed STREAM_INPUT[{index}]")
            for value in (2125999, 0, -1, 2126000.5, "2126000", True):
                stream["buffer_length_ns"] = value
                _refused(raw, directory, f"streams.listeners[{index}].buffer_length_ns",
                         "listener buffer floor")
            for value in (1 << 32, (1 << 32) + 2125999):
                stream["buffer_length_ns"] = value
                _refused(raw, directory, f"streams.listeners[{index}].buffer_length_ns",
                         "listener buffer width")
        for value in (0, -5, 1 << 32, "unused"):
            raw = copy.deepcopy(base)
            raw["streams"]["talkers"][0]["buffer_length_ns"] = value
            cfg = _load(raw, directory)
            assert "buffer_length_ns" not in eb.emit_aem_overlay(cfg)["stream_outputs"][0]
    print("[F2] eight listeners: floor/uint32 maximum pack equal; underflow/overflow refused")


def test_stream_format_contract() -> None:
    """Table 7-8 count after Milan 6.4 completion; 5.3.3.4 family separation."""
    import gen_aemi_image as join

    base = yaml.safe_load((ROOT / "configs/endstation_arty_4x4.yaml").read_text())
    # Independent format strings and cap from AVTP I.2.4 and Table 7-8.
    aaf = "0x0205022000806000"
    crf = "0x041060010000BB80"
    with tempfile.TemporaryDirectory(prefix="stream-format-contract.") as tmp:
        directory = Path(tmp)
        for direction in ("listeners", "talkers"):
            for index in range(len(base["streams"][direction])):
                raw = copy.deepcopy(base)
                stream = raw["streams"][direction][index]
                field = f"streams.{direction}[{index}].formats"
                derived = int(direction == "listeners")
                for count in (1, 46 - derived):
                    stream["formats"] = [aaf] * count
                    cfg = _load(raw, directory)
                    assert len(cfg[direction][index]["formats"]) == count + derived
                    if count + derived == 46:
                        overlay = eb.emit_aem_overlay(cfg)
                        document = join.model_to_document(
                            join.aem.build_model(join.aem.spec_from_overlay(overlay)),
                            join.identity_from_overlay(overlay))
                        join.image.build(document, 576)
                        dtype = 0x0005 if direction == "listeners" else 0x0006
                        row = next(r for r in document["descriptors"]
                                   if r["type"] == dtype and r["index"] == index)
                        body = bytes.fromhex(row["bytes"])
                        assert int.from_bytes(body[82:84], "big") == 138
                        assert int.from_bytes(body[84:86], "big") == 46
                        assert len(body) == 506 and len(body) <= 508
                for count in (47 - derived, 48 - derived, 48):
                    stream["formats"] = [aaf] * count
                    _refused(raw, directory, field, "format count")
                for formats in ([aaf, crf], [crf, aaf], [crf],
                                [aaf, "0x0000000000000000"], ["0x8205022000806000"]):
                    stream["formats"] = formats
                    _refused(raw, directory, field, "must contain only AAF formats")
    print("[F3] each AAF input/output: 46 final entries accepted; count/family refusals")


def test_crf_format_contract() -> None:
    """Milan 7.3.2 Table 7.1 independently fixes both CRF direction words."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_4x4.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="crf-format-contract.") as tmp:
        directory = Path(tmp)
        for output in (False, True):
            raw = copy.deepcopy(base)
            node = raw["clocking"]["crf_output"] if output else raw["clocking"]
            key = "format" if output else "crf_format"
            field = "clocking.crf_output.format" if output else "clocking.crf_format"
            node[key] = "0x041060010000bb80"
            cfg = _load(raw, directory)
            resolved = "crf_output_format" if output else "crf_format"
            assert cfg["clocking"][resolved] == "0x041060010000BB80"
            node[key] = "0x041060010000BB81"
            _refused(raw, directory, field, "CRF format must be")
            for value in ("0x0205022000806000", "0x0000000000000000", "0x841060010000BB80"):
                node[key] = value
                _refused(raw, directory, field, "must contain only CRF formats")
    print("[F3] both CRF directions: Milan word accepted; altered word/wrong family refused")


def test_output_clock_source_contract() -> None:
    """Milan 5.3.3.6: AAF and CRF outputs independently require INTERNAL."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="output-clock-contract.") as tmp:
        directory = Path(tmp)
        for crf_output in (False, True):
            raw = copy.deepcopy(base)
            raw["clocking"]["crf_output"] = dict(enabled=crf_output)
            for default in ("internal", "crf"):
                raw["clocking"].update(media_clock_sources=["internal", "crf"],
                                       default_source=default)
                cfg = _load(raw, directory)
                overlay = eb.emit_aem_overlay(cfg)
                assert [s["type"] for s in overlay["clock_sources"]] == ["internal", "crf"]
                assert len(overlay["stream_outputs"]) == 1 + int(crf_output)
            raw["clocking"].update(media_clock_sources=["crf"], default_source="crf")
            _refused(raw, directory, "clocking.media_clock_sources", "requires INTERNAL")
            if crf_output:
                # Exercise the CRF-only output arm directly: no talker guard
                # exists here to detect its removal through refusal precedence.
                clocking = eb._load_clocking(raw, "CRF-only output control")
                try:
                    eb._validate_output_clock_sources([], clocking)
                except eb.ConfigError as exc:
                    assert "requires INTERNAL" in str(exc), str(exc)
                else:
                    raise AssertionError("CRF output accepted without INTERNAL")
                raw["streams"]["talkers"] = []
                _refused(raw, directory, "clocking.media_clock_sources", "requires INTERNAL")
        # Input-only clock loading already supports CRF-only. Keep this narrow
        # boundary; the complete YAML loader still requires an AAF talker.
        raw["clocking"]["crf_output"]["enabled"] = False
        clocking = eb._load_clocking(raw, "input-only control")
        assert clocking["media_clock_sources"] == ["crf"]
        eb._validate_output_clock_sources([], clocking)
        _refused(raw, directory, "streams.talkers", "needs at least one talker stream")
        raw = copy.deepcopy(base)
        raw["clocking"].update(media_clock_sources=["internal"], default_source="internal",
                               crf_sink=False, crf_output={"enabled": False})
        assert _load(raw, directory)["clocking"]["media_clock_sources"] == ["internal"]
        raw["clocking"]["media_clock_sources"] = []
        _refused(raw, directory, "clocking.media_clock_sources", "L6 requires at least one source")
        raw["clocking"].pop("default_source")
        _refused(raw, directory, "clocking.media_clock_sources", "L6 requires at least one source")
    print("[F4] INTERNAL+CRF accepted; AAF/CRF outputs refused without INTERNAL; input-only unchanged")


def _code(text):
    return re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)


def assert_bindings(dp: str, wrapper: str, top: str, csr: str) -> None:
    """Each expression belongs to its actual instance, never a comment."""
    for source, module, instance, expression in (
        (dp, "KL_pp_shadow", "pp_shadow", ".SRP_DOM_DEF_VID_P(ADP_SRP_DOM_DEF_VID_C)"),
        (wrapper, "protocol_processor_top", "u_pp", ".SRP_DOM_DEF_VID_P(SRP_DOM_DEF_VID_P)"),
        (top, "KL_srp_top", "u_srp", ".DOM_DEF_VID_P(SRP_DOM_DEF_VID_P)"),
    ):
        match = re.search(r"\b" + module + r"\s*#\((.*?)\)\s*" + instance + r"\s*\(",
                          _code(source), re.S)
        assert match, f"missing actual {module} {instance}"
        compact = re.sub(r"\s+", "", match[1])
        assert expression in compact, f"broken generated VID binding: {module}"
    compact = re.sub(r"\s+", "", _code(dp))
    assert "?pp_aecp_pt_offset_w[32*k+:32]:ADP_STROUT_PRES_NS_C[k]" in compact, \
        "presentation row/default precedence binding"
    for reg, symbol, addr in (("aaf_ctrl", "AAF_CTRL_RST_C", "A_AAF_CTRL"),
                               ("maap_ctrl", "MAAP_CTRL_RST_C", "A_MAAP_CTRL")):
        compact = re.sub(r"\s+", "", _code(csr))
        assert f"localparamlogic[31:0]{symbol}=32'd0;" in compact, symbol
        assert f"{reg}<={symbol};" in compact, f"{reg} real reset"
        assert f"{addr}[10:0]:csr_default={symbol};" in compact, f"{reg} readback"


def assert_header(header: str, n: int) -> None:
    """Check each emitted factory row and the supported startup value."""
    text = _code(header)
    assert re.search(r"ADP_SRP_DOM_DEF_VID_C\s*=\s*16'd2;", text), "generated startup VID"
    match = re.search(r"ADP_STROUT_PRES_NS_C\s*\[0:(\d+)\]\s*=\s*'\{([^}]+)\};", text)
    assert match and int(match[1]) == n - 1, "generated output row shape"
    assert re.findall(r"32'd(\d+)", match[2]) == ["2000000"] * n, "factory offset rows"


def test_declaration_contracts() -> None:
    """Declaration refusals, generated rows, real bindings and mutation controls."""
    test_model_id_contract()
    test_model_id_resolution_contract()
    test_hex_scalar_contract()
    test_station_mac_string_contract()
    test_mac_shape_contract()
    test_declared_hex_string_contract()
    test_hex_shape_contract()
    test_formats_list_contract()
    test_aem_u32_contract()
    test_listener_buffer_contract()
    test_stream_format_contract()
    test_crf_format_contract()
    test_output_clock_source_contract()
    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="declarations.") as tmp:
        directory = Path(tmp)
        default = _load(base, directory)
        omitted_srp = copy.deepcopy(base)
        omitted_srp.pop("srp")
        assert _load(omitted_srp, directory)["srp"]["tspec_policy"] == "derived"
        explicit = copy.deepcopy(base)
        explicit["streams"]["talkers"][0]["presentation_time_offset_ns"] = 2000000
        explicit.setdefault("clocking", {}).setdefault("crf_output", {})[
            "presentation_time_offset_ns"] = 2000000
        explicit["platform"]["rx_address_filter"] = "promiscuous"
        same = _load(explicit, directory)
        assert eb.emit_adp_shape_svh(default) == eb.emit_adp_shape_svh(same)
        cases = []
        for key, values in (("vid", (1, 3, 4094)),
                            ("bandwidth_limit_pct", (0, 76, 100))):
            for value in values:
                cases.append((f"srp.{key}", lambda c, key=key, value=value:
                              c["srp"].update({key: value})))
        for leaf, value in (("join", 201), ("join", 200.5), ("leave", 600), ("leaveall", 15000)):
            cases.append((f"srp.timers_ms.{leaf}", lambda c, leaf=leaf, value=value:
                          c["srp"]["timers_ms"].update({leaf: value})))
        cases += [
            ("srp.tspec.policy", lambda c: c["srp"]["tspec"].update(policy="pinned")),
            ("srp.tspec.interval_frames", lambda c: c["srp"]["tspec"].update(interval_frames=2)),
            ("platform.rx_address_filter", lambda c: c["platform"].update(rx_address_filter="hardware")),
            ("board.features.maap", lambda c: c["board"].setdefault("features", {}).update(maap=False)),
        ]
        for value in (0, 1000000, 2000001, 0x7fffffff, True):
            cases.append(("5.3.7.6", lambda c, value=value: c["streams"]["talkers"][0].update(
                presentation_time_offset_ns=value)))
            cases.append(("5.3.7.6", lambda c, value=value: c["clocking"].setdefault(
                "crf_output", {}).update(enabled=True, presentation_time_offset_ns=value)))
        for value in (1000000, 2000000):
            cases.append(("streams.listeners[0].presentation_time_offset_ns",
                          lambda c, value=value: c["streams"]["listeners"][0].update(
                              presentation_time_offset_ns=value)))
        for reason, change in cases:
            raw = copy.deepcopy(base)
            change(raw)
            try:
                _load(raw, directory)
            except eb.ConfigError as exc:
                assert reason in str(exc), (reason, str(exc))
            else:
                raise AssertionError(f"accepted unsupported {reason}")
        for bits in range(4):
            raw = copy.deepcopy(base)
            raw["srp"].update(enable_at_reset=bool(bits & 1),
                              talker_declare_at_reset=bool(bits & 2))
            cfg = _load(raw, directory)
            assert eb.srp_reset_words(cfg)["LWSRP_CTRL"] & 3 == bits
        for path in sorted((ROOT / "configs").glob("endstation_*.yaml")):
            cfg = eb.load_config(path)
            header = eb.emit_adp_shape_svh(cfg)
            outputs = eb._overlay_streams(cfg)[1]
            n = len(cfg["talkers"]) + int(cfg["clocking"]["crf_output"])
            assert len(outputs) == n
            assert [o["presentation_time_offset_ns"] for o in outputs] == [2000000] * n
            assert_header(header, n)
            for old, new in (("16'd2;", "16'd3;"),
                             ("32'd2000000", "32'd1000000"),
                             (f"ADP_STROUT_PRES_NS_C [0:{n - 1}]", f"ADP_STROUT_PRES_NS_C [0:{n}]")):
                mutant = header.replace(old, new, 1) + "\n// " + old
                assert mutant != header
                try:
                    assert_header(mutant, n)
                except AssertionError:
                    pass
                else:
                    raise AssertionError(f"undetected generated header mutant {old}")
            print(f"[gate 40] {path.name}: {n} output factory rows, VID 2, promiscuous")
    _binding_controls()
    print(f"[gate 40] {len(cases)} refusals; 3 header mutants per config")


def _binding_controls() -> None:
    """Read exact consumers and prove every binding/reset assertion can fail."""
    paths = ("hdl/milan/milan_datapath.sv", "hdl/milan/KL_pp_shadow.sv",
             "protocol-processor/hdl/top/protocol_processor_top.sv", "hdl/common/csr/milan_csr.sv")
    texts = [ (ROOT / path).read_text() for path in paths ]
    assert_bindings(*texts)
    plants = (
        (0, ".SRP_DOM_DEF_VID_P (ADP_SRP_DOM_DEF_VID_C)", ".SRP_DOM_DEF_VID_P (16'd2)"),
        (1, ".SRP_DOM_DEF_VID_P (SRP_DOM_DEF_VID_P)", ".SRP_DOM_DEF_VID_P (16'd2)"),
        (2, ".DOM_DEF_VID_P    (SRP_DOM_DEF_VID_P)", ".DOM_DEF_VID_P    (16'd2)"),
        (0, "ADP_STROUT_PRES_NS_C[k]", "ADP_STROUT_PRES_NS_C[0]"),
        (0, "? pp_aecp_pt_offset_w[32*k +: 32]", "? ADP_STROUT_PRES_NS_C[k]"),
        (3, "aaf_ctrl <= AAF_CTRL_RST_C;", "aaf_ctrl <= 32'h0002_0000;"),
        (3, "maap_ctrl  <= MAAP_CTRL_RST_C;", "maap_ctrl  <= 32'h0000_0800;"),
        (3, "csr_default = AAF_CTRL_RST_C;", "csr_default = 32'h0002_0000;"),
        (3, "csr_default = MAAP_CTRL_RST_C;", "csr_default = 32'h0000_0800;"),
    )
    for i, old, new in plants:
        assert texts[i].count(old) == 1, old
        mutant = list(texts)
        mutant[i] = mutant[i].replace(old, new) + "\n// " + old
        try:
            assert_bindings(*mutant)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"undetected binding/reset mutant {old}")
    srp = _code((ROOT / "protocol-processor/hdl/srp/KL_srp_top.sv").read_text())
    for key, value in (("JOIN_MS_P", 200), ("PERIODIC_MS_P", 1000), ("LEAVE_MS_P", 5000)):
        assert re.search(r"\b" + key + r"\s*=\s*" + str(value) + r"\b", srp), key
    prng = _code((ROOT / "protocol-processor/hdl/common/KL_pp_prng.sv").read_text())
    assert re.search(r"3'd3:.*?limit_w\s*=\s*16'd5000;\s*base_w\s*=\s*16'd10000;", prng, re.S)
    print(f"[gate 40] {len(plants)} binding/reset mutants; donor timer profile")


if __name__ == "__main__":
    test_declaration_contracts()

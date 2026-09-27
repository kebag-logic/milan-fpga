# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Executable declaration contracts for #400 and #403 (builder gate 40)."""
import copy
from pathlib import Path
import re
import sys
import tempfile
from unittest.mock import patch

import yaml
import endstation_builder as eb

ROOT = Path(__file__).resolve().parents[2]
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


def test_hex_scalar_contract() -> None:
    """Preserve hex string digits; reject YAML numbers before field semantics."""
    base = yaml.safe_load((ROOT / "configs/endstation_arty_4x4.yaml").read_text())
    cases = (
        (("entity", "entity_model_id"), "entity.entity_model_id", "0x001BC50AC1000005"),
        (("entity", "model_id_pin"), "entity.model_id_pin", "0x001BC50AC1000005"),
        (("entity", "entity_id"), "entity.entity_id", "0x001BC50AC1000005"),
        (("srp", "stream_dmac_base"), "srp.stream_dmac_base", "0x91E0F000FE01"),
        (("streams", "talkers", 0, "formats", 0), "streams.talkers[0].formats",
         "0x0205022000806000"),
        (("streams", "listeners", 0, "formats", 0), "streams.listeners[0].formats",
         "0x0205022000806000"),
        (("clocking", "crf_format"), "clocking.crf_format", "0x041060010000BB80"),
        (("clocking", "crf_output", "format"), "clocking.crf_output.format",
         "0x041060010000BB80"),
    )
    with tempfile.TemporaryDirectory(prefix="hex-scalar-contract.") as tmp:
        path = Path(tmp) / "scalar.yaml"
        for keys, field, legal in cases:
            # The shared parser's result is independent of MAC width or family.
            # Those later rules cannot accept an arbitrary legal 64-bit number.
            for spelling in ("0x001BC50AC1000005", "1234567890123456",
                             "0012345670123456", "0x001B_C50A_C100_0005"):
                value = yaml.safe_load(f'"{spelling}"')
                assert eb._eui64(value, field) == int(spelling, 16)
                assert eb._fmt64(value, field) == f"0x{int(spelling, 16):016X}"
            raw = copy.deepcopy(base)
            raw["entity"].pop("model_id_pin", None)
            raw["entity"].pop("vendor_oui", None)
            for direction in ("talkers", "listeners"):
                raw["streams"][direction][0]["formats"] = ["0x0205022000806000"]
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

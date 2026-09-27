# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Executable declaration contracts for #400 and #403 (builder gate 40)."""
import copy
from pathlib import Path
import re
import sys
import tempfile

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
    """Milan 5.3.1 endpoints; Table 7-2 ENTITY and ADP identity equality."""
    import gen_aemi_image as join

    base = yaml.safe_load((ROOT / "configs/endstation_arty_current.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="model-id-contract.") as tmp:
        directory = Path(tmp)
        for key in ("entity_model_id", "model_id_pin"):
            raw = copy.deepcopy(base)
            raw["entity"].pop("model_id_pin", None)
            # Independent EUI-64 endpoints and adjacent legal values, per
            # Milan 5.3.1. Importing the guard's bounds would hide drift.
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


def test_listener_buffer_contract() -> None:
    """Milan 5.3.3.4: every listener, including nonzero indices, meets the floor."""
    base = yaml.safe_load((ROOT / "configs/endstation_ax7101_8x8.yaml").read_text())
    with tempfile.TemporaryDirectory(prefix="listener-buffer-contract.") as tmp:
        directory = Path(tmp)
        for index in range(len(base["streams"]["listeners"])):
            raw = copy.deepcopy(base)
            stream = raw["streams"]["listeners"][index]
            # Independent clause boundary, not the implementation's constant.
            for value in (2126000, 2126001):
                stream["buffer_length_ns"] = value
                cfg = _load(raw, directory)
                assert cfg["listeners"][index]["buffer_length_ns"] == value
                overlay = eb.emit_aem_overlay(cfg)
                assert overlay["stream_inputs"][index]["buffer_length_ns"] == value
            for value in (2125999, 0, -1, 2126000.5, "2126000", True):
                stream["buffer_length_ns"] = value
                _refused(raw, directory, f"streams.listeners[{index}].buffer_length_ns",
                         "listener buffer floor")
    print("[F2] eight listener indices: floor/above accepted, below/noninteger refused")


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
    test_listener_buffer_contract()
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

# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Approved #979 topology, source identities and default-off image identity."""
import copy
from pathlib import Path
import sys
import tempfile

import yaml
import endstation_builder as eb

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "avdecc"), str(ROOT / "protocol-processor/hdl/aecp/desc")]
import aem_assemble
import aem_specs
import gen_aem_store
import gen_aemi_image
import gen_desc_image


def image(overlay: dict) -> bytes:
    """The shipping descriptor image, including identity and writable names."""
    model = gen_aem_store.build_model(gen_aem_store.spec_from_overlay(overlay))
    document = gen_aemi_image.model_to_document(model, gen_aemi_image.identity_from_overlay(overlay))
    return gen_desc_image.build(document, 576)[0]


def test_input_loopback_contract() -> None:
    """Nine clusters/page crossing, 64-key ceiling, independent physical key, and source bucket 6."""
    with tempfile.TemporaryDirectory(prefix="input-loopback-builder-") as tmp:
        directory = Path(tmp)
        for name, widths, first, channels in (
                ("endstation_ax7101_1x1_tdm8", [16], 8, 8),
                ("endstation_ax7101_8x8", [9, 8, 8, 8, 8, 8, 8, 7], 1, 63)):
            raw = yaml.safe_load((ROOT / "configs" / (name + ".yaml")).read_text())
            path = directory / (name + ".yaml")

            def derive(value: dict) -> eb.BuildArtifacts:
                """Regenerate all artifacts from the same config pathname."""
                path.write_text(yaml.safe_dump(value))
                return eb._derive_artifacts(path)

            original = derive(raw)
            disabled = copy.deepcopy(raw)
            disabled["audio_interface"]["cluster_mapping"]["fabric"]["input_loopback_lane"] = False
            off = derive(disabled)
            # Every artifact field, including argv, model ID and emitted ROM.
            assert original == off, name
            assert image(original.overlay) == image(off.overlay), name
            enabled = copy.deepcopy(raw)
            enabled["audio_interface"]["cluster_mapping"]["fabric"].update(
                input_loopback_lane=True, loopback_lane=False)
            on = derive(enabled)
            assert on.aem_rom_why is None, on.aem_rom_why
            assert on.overlay["model_id"] != off.overlay["model_id"]
            assert image(on.overlay) != image(off.overlay)
            assert "--input-loopback-lane" in on.argv
            assert "--input-loopback-lane" not in off.argv
            ports = on.overlay["stream_ports"]
            assert [p["clusters"] for p in ports["input"]] == widths
            assert sum(widths) == first + channels
            assert [p["base_cluster"] for p in ports["input"]] == [sum(widths[:i]) for i in range(len(widths))]
            physical = [(p["index"], g["offset"] + n) for p in ports["input"]
                        for g in p["pool"] if g["role"] == "physical" for n in range(g["width"])]
            assert physical == [(0, n) for n in range(first)], physical
            destinations = [g["first"] + n for p in ports["input"] for g in p["pool"]
                            if g["role"] == "input_loopback" for n in range(g["width"])]
            assert destinations == list(range(channels))
            addresses = []
            for j, p in enumerate(ports["output"]):
                for source in aem_specs._out_cluster_sources(on.overlay, j, p):
                    if source["src"] == 6:
                        assert source["valid"]
                        addresses.append(8 * source["idxh"] + 2 * source["idx"] + source["half"])
            assert addresses == list(range(channels)), addresses
            spec = gen_aem_store.spec_from_overlay(on.overlay)
            table = aem_assemble._dynmap_tables(spec)
            assert table["KEYS"] == first + channels and table["PAGE"] == 8
            assert table["PNMAPS"] == ([2] if channels == 8 else [2, 1, 1, 1, 1, 1, 1, 1])
            if channels == 63:
                assert eb.aem_name_count(on.overlay) == 234
                try:
                    eb._adp_name_entries(on.overlay, "all-fabric")
                except eb.ConfigError as error:
                    assert "128 NAME records" in str(error)
                else:
                    raise AssertionError("all-fabric NAME ceiling moved")
                too_many = copy.deepcopy(spec)
                too_many["ports_in"][-1]["clusters"] += 1
                try:
                    aem_assemble._dynmap_tables(too_many)
                except ValueError as error:
                    assert "65 dynamic cluster keys exceeds the 64-key" in str(error)
                else:
                    raise AssertionError("65 keys accepted")
            for value in ("true", 1):
                invalid = copy.deepcopy(enabled)
                invalid["audio_interface"]["cluster_mapping"]["fabric"]["input_loopback_lane"] = value
                try:
                    derive(invalid)
                except eb.ConfigError as error:
                    assert "input_loopback_lane must be bool" in str(error)
                else:
                    raise AssertionError("non-boolean option accepted")
    print("  input loopback: 1x1/16 keys, 8x8/64 keys, page crossing, source addresses, "
          "NAME/key bounds, off identity PASS")


if __name__ == "__main__":
    test_input_loopback_contract()

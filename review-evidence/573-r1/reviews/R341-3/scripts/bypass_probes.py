"""Reviewer bypass/boundary probes for the F1-F4 refusals.

Run from <tree>/sw/builder:  python3 -B bypass_probes.py <tree>
Prints one JSON object per probe: the loader verdict and, where the loader
accepts, what the generated overlay/image carries.
"""
import copy
import json
from pathlib import Path
import sys
import tempfile

import yaml

TREE = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(TREE / "sw/builder"))
import endstation_builder as eb  # noqa: E402
import gen_aemi_image as join  # noqa: E402

AAF48 = "0x0205022000806000"


def base(name):
    return yaml.safe_load((TREE / "configs" / name).read_text())


def load(raw, text=None):
    with tempfile.TemporaryDirectory(prefix="r341-probe.") as tmp:
        path = Path(tmp) / "case.yaml"
        path.write_text(text if text is not None else yaml.safe_dump(raw))
        return eb.load_config(path)


def image_stream_inputs(cfg):
    """Build the packed descriptor document and flat image; return STREAM_INPUT fields."""
    overlay = eb.emit_aem_overlay(cfg)
    document = join.model_to_document(
        join.aem.build_model(join.aem.spec_from_overlay(overlay)),
        join.identity_from_overlay(overlay))
    join.image.build(document, 576)          # the image packer accepts it too
    rows = []
    for row in document["descriptors"]:
        if row["type"] == 0x0005:            # STREAM_INPUT, IEEE 1722.1-2021 Table 7-8
            body = bytes.fromhex(row["bytes"])
            rows.append(dict(index=row["index"],
                             buffer_length=int.from_bytes(body[128:132], "big"),
                             number_of_formats=int.from_bytes(body[84:86], "big")))
    return overlay, rows


def probe(label, fn):
    try:
        result = fn()
        print(json.dumps(dict(probe=label, verdict="ACCEPTED", detail=result)))
    except eb.ConfigError as exc:
        print(json.dumps(dict(probe=label, verdict="REFUSED", detail=str(exc)[:240])))
    except Exception as exc:  # an unnamed failure is itself a result
        print(json.dumps(dict(probe=label, verdict=f"UNNAMED {type(exc).__name__}",
                              detail=str(exc)[:240])))


def listener_buffer(value):
    def run():
        raw = base("endstation_arty_4x4.yaml")
        raw["streams"]["listeners"][0]["buffer_length_ns"] = value
        cfg = load(raw)
        overlay, rows = image_stream_inputs(cfg)
        return dict(declared=value, overlay=overlay["stream_inputs"][0]["buffer_length_ns"],
                    image_stream_inputs=rows[:1])
    return run


def listener_formats(formats):
    def run():
        raw = base("endstation_arty_4x4.yaml")
        raw["streams"]["listeners"][0]["formats"] = formats
        cfg = load(raw)
        overlay, rows = image_stream_inputs(cfg)
        return dict(declared=len(formats), final=len(cfg["listeners"][0]["formats"]),
                    image_stream_inputs=rows[:1])
    return run


def talker_buffer(value):
    def run():
        raw = base("endstation_arty_4x4.yaml")
        raw["streams"]["talkers"][0]["buffer_length_ns"] = value
        return dict(loaded=load(raw)["talkers"][0]["buffer_length_ns"])
    return run


def model_literal_text(text_value):
    def run():
        text = (TREE / "configs/endstation_arty_current.yaml").read_text()
        raw = yaml.safe_load(text)
        raw["entity"].pop("model_id_pin", None)
        dumped = yaml.safe_dump(raw)
        lines = [ln for ln in dumped.splitlines()]
        out = []
        for ln in lines:
            if ln.startswith("  entity_model_id:"):
                ln = f"  entity_model_id: {text_value}"
            out.append(ln)
        cfg = load(None, "\n".join(out) + "\n")
        return dict(yaml_text=text_value, resolved=cfg["entity"]["entity_model_id"])
    return run


def crf_sink_off_altered_word():
    raw = base("endstation_arty_4x4.yaml")
    raw["clocking"]["crf_sink"] = False
    raw["clocking"]["media_clock_sources"] = ["internal"]
    raw["clocking"]["default_source"] = "internal"
    raw["clocking"]["crf_format"] = "0x041060010000BB81"
    return dict(loaded=load(raw)["clocking"]["crf_format"])


def default_sources_with_outputs():
    raw = base("endstation_arty_4x4.yaml")
    raw["clocking"].pop("media_clock_sources", None)
    raw["clocking"].pop("default_source", None)
    return dict(sources=load(raw)["clocking"]["media_clock_sources"])


def reversed_sources_with_outputs():
    raw = base("endstation_arty_4x4.yaml")
    raw["clocking"].update(media_clock_sources=["crf", "internal"], default_source="crf")
    cfg = load(raw)
    return dict(sources=[s["type"] for s in eb.emit_aem_overlay(cfg)["clock_sources"]])


for value in (2126000, 2125999, 2**32 - 1, 2**32, 2**32 + 1000, 2**32 + 2126000, 2**33):
    probe(f"F2 listener buffer_length_ns={value}", listener_buffer(value))
for value in (0, 1, -5, 2**32 + 1000):
    probe(f"F2 talker buffer_length_ns={value} (talkers unaffected)", talker_buffer(value))
for count in (45, 46, 47):
    probe(f"F3 listener {count} declared AAF 48k 8ch formats", listener_formats([AAF48] * count))
probe("F3 CRF sink disabled, altered crf_format", crf_sink_off_altered_word)
probe("F4 sources omitted (default) with outputs", default_sources_with_outputs)
probe("F4 sources [crf, internal] with outputs", reversed_sources_with_outputs)
for text_value in ("0x0000000000000000", "0xFFFFFFFFFFFFFFFF", "0", "0x001BC50AC1000005", "'0x001BC50AC1000005'"):
    probe(f"F1 unquoted YAML entity_model_id {text_value}", model_literal_text(text_value))

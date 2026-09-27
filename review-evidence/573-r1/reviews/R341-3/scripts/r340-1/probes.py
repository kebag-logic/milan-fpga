"""Reviewer probes of the F1-F4 refusals: boundaries, alternate spellings,
defaults and paths around each check. Records loader outcome per case.

Usage: python3 probes.py <tree root> <output json>
"""
import copy
import json
from pathlib import Path
import sys
import tempfile

import yaml

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "sw/builder"))
import endstation_builder as eb  # noqa: E402

AAF = "0x0205022000806000"
CRF = "0x041060010000BB80"


def base(name):
    return yaml.safe_load((ROOT / f"configs/endstation_{name}.yaml").read_text())


def run(label, name, mutate, directory, pack=False):
    raw = base(name)
    mutate(raw)
    path = directory / "case.yaml"
    path.write_text(yaml.safe_dump(raw))
    row = dict(case=label, config=name)
    try:
        cfg = eb.load_config(path)
    except eb.ConfigError as exc:
        row.update(loader="refused", reason=str(exc)[:240])
        return row
    except Exception as exc:  # noqa: BLE001 - classify unnamed failures
        row.update(loader=f"crashed:{type(exc).__name__}", reason=str(exc)[:240])
        return row
    row["loader"] = "accepted"
    row["entity_model_id"] = cfg["entity"]["entity_model_id"]
    if pack:
        import gen_aemi_image as join
        try:
            overlay = eb.emit_aem_overlay(cfg)
            document = join.model_to_document(
                join.aem.build_model(join.aem.spec_from_overlay(overlay)),
                join.identity_from_overlay(overlay))
            blob, _ = join.image.build(document, 576)
            row.update(image="accepted", image_bytes=len(blob),
                       stream_inputs=[dict(buffer=s.get("buffer_length_ns"), n=len(s["formats"]))
                                      for s in overlay["stream_inputs"]])
        except Exception as exc:  # noqa: BLE001
            row.update(image=f"refused:{type(exc).__name__}", image_reason=str(exc)[:240])
    return row


def ent(**kw):
    def f(c):
        c["entity"].pop("model_id_pin", None)
        c["entity"].update(kw)
    return f


def lst(index, **kw):
    return lambda c: c["streams"]["listeners"][index].update(kw)


def tlk(index, **kw):
    return lambda c: c["streams"]["talkers"][index].update(kw)


def clk(**kw):
    return lambda c: c["clocking"].update(kw)


def crf_out(**kw):
    return lambda c: c["clocking"].setdefault("crf_output", {}).update(kw)


def seq(*fs):
    def f(c):
        for g in fs:
            g(c)
    return f


CASES = [
    # F1 model identity
    ("F1 control unchanged arty_current", "arty_current", lambda c: None),
    ("F1 literal YAML int 0", "arty_current", ent(entity_model_id=0)),
    ("F1 literal YAML int all-ones", "arty_current", ent(entity_model_id=(1 << 64) - 1)),
    ("F1 literal short '0x0'", "arty_current", ent(entity_model_id="0x0")),
    ("F1 literal lowercase all-ones", "arty_current", ent(entity_model_id="0xffffffffffffffff")),
    ("F1 pin YAML int 0", "arty_current", ent(entity_model_id="hash-derived", model_id_pin=0)),
    ("F1 pin decimal string all-ones", "arty_current",
     ent(entity_model_id="hash-derived", model_id_pin="18446744073709551615")),
    ("F1 zero literal shadowed by legal pin", "arty_current",
     lambda c: c["entity"].update(entity_model_id="0x0000000000000000",
                                  model_id_pin="0x001BC50AC1000005")),
    ("F1 hash-derived with vendor_oui 0", "arty_4x4",
     lambda c: c["entity"].update(entity_model_id="hash-derived", vendor_oui="0x000000")),
    ("F1 literal legal 1", "arty_current", ent(entity_model_id="0x0000000000000001")),
    # F2 listener buffer
    ("F2 default omitted", "ax7101_8x8",
     lambda c: [s.pop("buffer_length_ns", None) for s in c["streams"]["listeners"]]),
    ("F2 last listener 2125999", "ax7101_8x8", lst(7, buffer_length_ns=2125999)),
    ("F2 null", "ax7101_8x8", lst(0, buffer_length_ns=None)),
    ("F2 float 2126000.0", "ax7101_8x8", lst(0, buffer_length_ns=2126000.0)),
    ("F2 2**32 (field is 32-bit)", "ax7101_8x8", lst(0, buffer_length_ns=1 << 32)),
    ("F2 2**32+2125999 wraps below floor if truncated", "ax7101_8x8",
     lst(0, buffer_length_ns=(1 << 32) + 2125999)),
    ("F2 talker 1 ns (talker unaffected)", "ax7101_8x8", tlk(0, buffer_length_ns=1)),
    ("F2 talker string (talker unaffected)", "ax7101_8x8", tlk(0, buffer_length_ns="x")),
    # F3 formats
    ("F3 listener 46 declared (47 final)", "arty_4x4", lst(0, formats=[AAF] * 46)),
    ("F3 listener 47 declared (48 final)", "arty_4x4", lst(0, formats=[AAF] * 47)),
    ("F3 talker 47", "arty_4x4", tlk(0, formats=[AAF] * 47)),
    ("F3 talker 48", "arty_4x4", tlk(0, formats=[AAF] * 48)),
    ("F3 last talker mixed", "ax7101_8x8", tlk(-1, formats=[AAF, CRF])),
    ("F3 last listener mixed", "ax7101_8x8", lst(-1, formats=[AAF, CRF])),
    ("F3 listener empty list (default)", "arty_4x4", lst(0, formats=[])),
    ("F3 CRF input YAML int word", "arty_4x4", clk(crf_format=int(CRF, 16))),
    ("F3 CRF input altered word, sink disabled", "arty_4x4",
     clk(crf_format="0x041060010000BB81", crf_sink=False, media_clock_sources=["internal"],
         default_source="internal")),
    ("F3 CRF output altered word, output disabled", "arty_current",
     crf_out(enabled=False, format="0x041060010000BB81")),
    ("F3 CRF output altered word, output enabled", "arty_current",
     crf_out(enabled=True, format="0x041060020000BB80")),
    ("F3 CRF output plural 'formats' key (alternate key)", "arty_current",
     crf_out(enabled=True, formats=["0x041060010000BB81"])),
    # F4 clock sources
    ("F4 [internal] only, sink off, outputs", "arty_current",
     clk(media_clock_sources=["internal"], default_source="internal", crf_sink=False)),
    ("F4 reversed [crf, internal]", "arty_current",
     clk(media_clock_sources=["crf", "internal"], default_source="crf")),
    ("F4 [crf] default omitted", "arty_current", clk(media_clock_sources=["crf"])),
    ("F4 [crf] + CRF output enabled", "arty_current",
     seq(clk(media_clock_sources=["crf"], default_source="crf"), crf_out(enabled=True))),
    ("F4 empty sources, default omitted", "arty_current", clk(media_clock_sources=[])),
    ("F4 empty sources, default internal", "arty_current",
     clk(media_clock_sources=[], default_source="internal")),
    ("F4 [crf] on 8x8", "ax7101_8x8", clk(media_clock_sources=["crf"], default_source="crf")),
]


def main() -> None:
    rows = []
    with tempfile.TemporaryDirectory(prefix="r340-probes-") as tmp:
        for label, name, mutate in CASES:
            pack = label.startswith(("F2 2**32", "F2 float", "F1 zero literal", "F1 hash"))
            rows.append(run(label, name, mutate, Path(tmp), pack))
    for r in rows:
        extra = r.get("reason") or r.get("image_reason") or r.get("entity_model_id") or ""
        print(f"{r['case']:52} {r['loader']:22} {r.get('image', ''):22} {extra[:150]}")
    Path(sys.argv[2]).write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main()

"""Round-3 decision matrix: every _eui64/_fmt64 key requires a quoted YAML string.

Run: python3 -B hex_rule_probe.py <tree>
For each field, writes spellings into arty_4x4 (pin removed) through a text slot
so YAML typing is exactly what a user file gets, and prints the loader result:
the resolved value on acceptance, or the refusal text. Accepted identity values
are followed into the emitted overlay.
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

BASE = yaml.safe_load((TREE / "configs/endstation_arty_4x4.yaml").read_text())
AAF = "0x0205022000806000"
CRF = "0x041060010000BB80"
FIELDS = (
    (("entity", "entity_model_id"), "0x001BC50AC1000005"),
    (("entity", "model_id_pin"), "0x001BC50AC1000005"),
    (("entity", "entity_id"), "0x001BC50AC1000005"),
    (("srp", "stream_dmac_base"), "0x91E0F000FE01"),
    (("streams", "talkers", 0, "formats", 0), AAF),
    (("streams", "listeners", 0, "formats", 0), AAF),
    (("clocking", "crf_format"), CRF),
    (("clocking", "crf_output", "format"), CRF),
)
UNQUOTED = ("{legal}", "1234567890123456", "0012345670123456", "0", "null", "", "true",
            "1.5", "[]", "{{}}", "18446744073709551615", "0x_1")
QUOTED = ("{legal}", "{bare}", "1234567890123456", "0x001B_C50A_C100_0005", "zz")


def resolved(cfg, keys):
    if keys[0] == "entity":
        name = "entity_id" if keys[-1] == "entity_id" else "entity_model_id"
        over = eb.emit_aem_overlay(cfg)["entity"][name]
        return dict(cfg=cfg["entity"][name], overlay=over)
    if keys[0] == "srp":
        return dict(cfg=cfg["srp"]["stream_dmac_base"])
    if keys[0] == "streams":
        side = "talkers" if keys[1] == "talkers" else "listeners"
        return dict(cfg=cfg[side][0]["formats"][0])
    clk = cfg["clocking"]
    return dict(cfg=clk.get("crf_format") if keys[-1] == "crf_format" else clk.get("crf_output_format"))


def run(keys, text):
    raw = copy.deepcopy(BASE)
    raw["entity"].pop("model_id_pin", None)
    raw["entity"].pop("vendor_oui", None)
    for d in ("talkers", "listeners"):
        raw["streams"][d][0]["formats"] = [AAF]
    node = raw
    for k in keys[:-1]:
        node = node[k]
    node[keys[-1]] = "HEX_SLOT"
    tpl = yaml.safe_dump(raw)
    assert tpl.count("HEX_SLOT") == 1
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "c.yaml"
        path.write_text(tpl.replace("HEX_SLOT", text))
        loaded = yaml.safe_load(path.read_text())
        node = loaded
        for k in keys:
            node = node[k]
        kind = type(node).__name__
        try:
            cfg = eb.load_config(path)
        except eb.ConfigError as exc:
            return kind, dict(refused=str(exc))
        except Exception as exc:  # a crash is a result, not a refusal
            return kind, dict(crashed=f"{type(exc).__name__}: {exc}")
    return kind, dict(accepted=resolved(cfg, keys))


for keys, legal in FIELDS:
    field = ".".join(str(k) for k in keys)
    bare = legal.removeprefix("0x")
    for form, texts in (("quoted", QUOTED), ("unquoted", UNQUOTED)):
        for t in texts:
            spelled = t.format(legal=legal, bare=bare)
            text = f'"{spelled}"' if form == "quoted" else spelled
            kind, res = run(keys, text)
            print(json.dumps(dict(field=field, form=form, text=text, yaml_type=kind, **res)))
# selectors and the pin presence rule
for keys, text in ((("entity", "entity_model_id"), "hash-derived"),
                   (("entity", "entity_model_id"), '"hash-derived"'),
                   (("entity", "entity_id"), "mac-derived"),
                   (("srp", "stream_dmac_base"), "maap"),
                   (("srp", "stream_dmac_base"), '" MAAP "'),
                   (("entity", "model_id_pin"), "null"),
                   (("entity", "model_id_pin"), "")):
    kind, res = run(keys, text)
    print(json.dumps(dict(field=".".join(keys), form="selector/presence", text=text, yaml_type=kind, **res)))

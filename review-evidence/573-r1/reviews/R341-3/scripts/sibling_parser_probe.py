"""Sibling hex parsers outside the #573 round-3 decision: quoted versus unquoted.

Run: python3 -B sibling_parser_probe.py <tree>
Writes platform.mac_address and entity.vendor_oui once quoted and once unquoted
into arty_4x4 (hash-derived model ID, no pin) and prints the resolved value.
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


def resolve(section, field, text):
    raw = copy.deepcopy(BASE)
    raw["entity"].pop("model_id_pin", None)
    raw[section][field] = "SLOT"
    template = yaml.safe_dump(raw)
    assert template.count("SLOT") == 1
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "case.yaml"
        path.write_text(template.replace("SLOT", text))
        kind = type(yaml.safe_load(path.read_text())[section][field]).__name__
        try:
            cfg = eb.load_config(path)
        except eb.ConfigError as exc:
            return kind, "REFUSED: " + str(exc)
    if field == "mac_address":
        return kind, cfg["entity"]["entity_id"] if False else f"0x{eb._mac48(cfg['platform']['mac_address'], 'x'):012X}" if isinstance(cfg.get("platform", {}).get("mac_address"), (int, str)) else repr(cfg.get("platform"))
    return kind, cfg["model_id"]["hash"]


for section, field, spellings in (
        ("platform", "mac_address", ("0x020000000002", "020000000002", "200000000002")),
        ("entity", "vendor_oui", ("0x001BC5", "001BC5", "123456"))):
    for s in spellings:
        qk, q = resolve(section, field, f'"{s}"')
        uk, u = resolve(section, field, s)
        print(json.dumps(dict(field=f"{section}.{field}", text=s, quoted=q,
                              unquoted_yaml_type=uk, unquoted=u, equal=q == u)))

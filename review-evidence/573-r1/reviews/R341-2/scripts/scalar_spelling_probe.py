"""EUI-64 YAML scalar spellings: quoted versus unquoted, per field.

Run: python3 -B scalar_spelling_probe.py <tree>
For each spelling, the same text is written once quoted and once unquoted into
an otherwise unchanged arty_current configuration, and the value the loader
resolves is printed. The builder's documented hex parser reads a quoted string
as hexadecimal, so a quoted/unquoted mismatch is a silent reinterpretation.
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

BASE = yaml.safe_load((TREE / "configs/endstation_arty_current.yaml").read_text())


def resolve(field, text):
    raw = copy.deepcopy(BASE)
    raw["entity"].pop("vendor_oui", None)
    if field == "entity_model_id":
        raw["entity"].pop("model_id_pin", None)
    raw["entity"][field] = "SCALAR_SLOT"
    template = yaml.safe_dump(raw)
    assert template.count("SCALAR_SLOT") == 1
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "case.yaml"
        path.write_text(template.replace("SCALAR_SLOT", text))
        yaml_type = type(yaml.safe_load(path.read_text())["entity"][field]).__name__
        try:
            cfg = eb.load_config(path)
        except eb.ConfigError as exc:
            return yaml_type, "REFUSED: " + str(exc)
    key = "entity_model_id" if field in ("entity_model_id", "model_id_pin") else field
    return yaml_type, cfg["entity"][key]


for field in ("model_id_pin", "entity_model_id", "entity_id"):
    for spelling in ("0x001BC50AC1000005", "001BC50AC1000005", "1000000000000005",
                     "0010000000000001", "10"):
        q_type, quoted = resolve(field, f'"{spelling}"')
        u_type, unquoted = resolve(field, spelling)
        print(json.dumps(dict(field=field, text=spelling, quoted=quoted,
                              unquoted_yaml_type=u_type, unquoted=unquoted,
                              equal=quoted == unquoted)))

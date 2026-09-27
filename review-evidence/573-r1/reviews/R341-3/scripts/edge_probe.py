"""Edge spellings around the round-3 string rule (formats as a scalar, whitespace/sign text).

Run: python3 -B edge_probe.py <tree>
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


def run(path_keys, text):
    raw = copy.deepcopy(BASE)
    raw["entity"].pop("model_id_pin", None)
    raw["entity"].pop("vendor_oui", None)
    node = raw
    for k in path_keys[:-1]:
        node = node[k]
    node[path_keys[-1]] = "SLOT"
    tpl = yaml.safe_dump(raw)
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "c.yaml"
        p.write_text(tpl.replace("SLOT", text))
        try:
            cfg = eb.load_config(p)
        except eb.ConfigError as exc:
            return dict(refused=str(exc))
        except Exception as exc:
            return dict(crashed=f"{type(exc).__name__}: {exc}")
    return dict(accepted=dict(entity_id=cfg["entity"]["entity_id"],
                              talker0_formats=cfg["talkers"][0]["formats"]))


for keys, text in ((("streams", "talkers", 0, "formats"), '"0x0205022000806000"'),
                   (("streams", "talkers", 0, "formats"), '"0205022000806000"'),
                   (("streams", "talkers", 0, "formats"), "[]"),
                   (("entity", "entity_id"), '" 0x001BC50AC1000005 "'),
                   (("entity", "entity_id"), '"+0x001BC50AC1000005"'),
                   (("entity", "entity_id"), '"-0x1"'),
                   (("entity", "entity_id"), '""'),
                   (("entity", "entity_id"), '"0x1_0000_0000_0000_0000"')):
    print(json.dumps(dict(field=".".join(map(str, keys)), text=text, **run(keys, text))))

#!/usr/bin/env python3
"""Load arty_4x4 / ax7101_1x1_tdm8 with one field re-spelled (raw YAML text)
and print the loader's outcome. Usage: edge_probe.py <tree>"""
import copy, sys, tempfile
from pathlib import Path
import yaml
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb

def template(cfg, keys):
    doc = yaml.safe_load((tree / "configs" / cfg).read_text())
    node = doc
    for k in keys[:-1]:
        node = node[k]
    node[keys[-1]] = "SLOT"
    t = yaml.safe_dump(doc); assert t.count("SLOT") == 1
    return t

CASES = [
    ("endstation_arty_4x4.yaml", ("platform", "mac_address"),
     ["yes", "on", "off", "2026-09-28", "!!binary AgAAAAAC", ".inf", "1:30.5", "~",
      "0b10", "02:00:00:00:00:02", "'02:00:00:00:00:02'", '"0x02:00:00:00:00:02"',
      '"-2"', '"0:2"', '" 020000000002 "', '"2"', "0205022000806000"]),
    ("endstation_ax7101_1x1_tdm8.yaml", ("entity", "vendor_oui"),
     ["yes", "2026-09-28", "001BC5", '"001BC5"', '"0x00_1B_C5"', '"+1BC5"', '" 1BC5"', "[]"]),
    ("endstation_ax7101_1x1_tdm8.yaml", ("entity", "entity_capabilities"),
     ["yes", "0000C588", '"0000C588"', '"0x0000_C588"', "0x0000C588", "50568"]),
    ("endstation_arty_4x4.yaml", ("streams", "listeners", 0, "formats"),
     ["[null]", "[[\"0x0205022000806000\"]]", "[0205022000806000]", "[true]",
      "!!set {a: null}", "yes", "2026-09-28", '["0205022000806000", "0x0205022000806000"]']),
]
with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "case.yaml"
    for cfg, keys, spellings in CASES:
        t = template(cfg, keys)
        for s in spellings:
            path.write_text(t.replace("SLOT", s))
            try:
                c = eb.load_config(path)
                node = c
                if keys[0] == "platform":
                    got = c["platform"]["mac_address"]
                elif keys[-1] == "vendor_oui":
                    got = c["entity"]["entity_model_id"]
                elif keys[-1] == "formats":
                    got = c["listeners"][0]["formats"][:2]
                else:
                    got = "accepted"
                print(f"ACCEPT {'.'.join(map(str, keys))} {s!r} -> {got}")
            except eb.ConfigError as e:
                print(f"REFUSE {'.'.join(map(str, keys))} {s!r} -> {str(e)[:140]}")
            except Exception as e:
                print(f"CRASH  {'.'.join(map(str, keys))} {s!r} -> {type(e).__name__}: {str(e)[:140]}")

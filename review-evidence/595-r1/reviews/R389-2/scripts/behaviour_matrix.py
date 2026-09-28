#!/usr/bin/env python3
"""Load one tracked config with a single key replaced by a raw YAML spelling
and print the loader's outcome. Usage: behaviour_matrix.py <tree> <label>.
Run it once against the base tree and once against the head tree."""
import copy, sys, tempfile
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
import yaml
import endstation_builder as eb

SPELLINGS = ["020000000002", '"020000000002"', "10:20:30:40:50:02", '"10:20:30:40:50:02"',
             "02:00:00:00:00:02", '"02-00-00-00-00-02"', "0x020000000002", "0b101",
             "yes", "no", "on", "off", "true", "1:30.5", ".inf", "1.5", "~", "", "[]", "{}",
             "!!str 020000000002", "!!binary AAECAwQF", "2002-12-14", "08", "123456",
             '"123456"', '"0x123456"', "0x123456", '"001BC5"', "001BC5", "[1, 2]"]
FORMATS = ['"0x0205022000806000"', "0x0205022000806000", "yes", "~", "", "[]",
           '["0x0205022000806000"]', "[0x0205022000806000]", "!!set {a}", "{}", "0"]

def slot(doc, keys):
    d = copy.deepcopy(doc); n = d
    for k in keys[:-1]:
        n = n[k]
    n[keys[-1]] = "YAML_SLOT"
    t = yaml.safe_dump(d); assert t.count("YAML_SLOT") == 1
    return t

def outcome(path, text):
    path.write_text(text)
    try:
        cfg = eb.load_config(path)
    except eb.ConfigError as e:
        return f"REFUSED {e}"
    except Exception as e:  # noqa: BLE001
        return f"CRASH {type(e).__name__}: {e}"
    return cfg

def main():
    arty = yaml.safe_load((tree / "configs/endstation_arty_current.yaml").read_text())
    ax = yaml.safe_load((tree / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "c.yaml"
        t = slot(arty, ("platform", "mac_address"))
        for s in SPELLINGS:
            r = outcome(path, t.replace("YAML_SLOT", s))
            r = r if isinstance(r, str) else "ACCEPTED mac=" + r["platform"]["mac_address"]
            print(f"platform.mac_address\t{s}\t{r[:160]}")
        t = slot(ax, ("entity", "vendor_oui"))
        for s in SPELLINGS:
            r = outcome(path, t.replace("YAML_SLOT", s))
            r = r if isinstance(r, str) else "ACCEPTED oui=0x%06X" % (int(r["entity"]["entity_model_id"], 16) >> 40)
            print(f"entity.vendor_oui\t{s}\t{r[:160]}")
        t = slot(ax, ("entity", "entity_capabilities"))
        for s in ["~", "", "true", "1.5", "0", '"0"', "[]"]:
            r = outcome(path, t.replace("YAML_SLOT", s))
            r = r if isinstance(r, str) else "ACCEPTED"
            print(f"entity.entity_capabilities\t{s}\t{r[:160]}")
        t = slot(arty, ("streams", "talkers", 0, "formats"))
        for s in FORMATS:
            r = outcome(path, t.replace("YAML_SLOT", s))
            r = r if isinstance(r, str) else "ACCEPTED formats=" + ",".join(r["talkers"][0]["formats"])
            print(f"streams.talkers[0].formats\t{s}\t{r[:160]}")
        t = slot(arty, ("streams", "listeners", 0, "formats"))
        for s in FORMATS:
            r = outcome(path, t.replace("YAML_SLOT", s))
            r = r if isinstance(r, str) else "ACCEPTED n=%d first=%s" % (len(r["listeners"][0]["formats"]), r["listeners"][0]["formats"][0])
            print(f"streams.listeners[0].formats\t{s}\t{r[:160]}")

main()

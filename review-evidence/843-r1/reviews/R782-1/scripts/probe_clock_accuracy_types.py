#!/usr/bin/env python3
"""Load the AX7101 1x1 config with gptp.clock_accuracy replaced by each
probe value and report what the builder of <checkout> does with it.

usage: probe_clock_accuracy_types.py <checkout> <tmpdir>
"""
import pathlib
import sys

import yaml

root = pathlib.Path(sys.argv[1]).resolve()
tmp = pathlib.Path(sys.argv[2])
sys.path.insert(0, str(root / "sw" / "builder"))
import endstation_builder as eb  # noqa: E402

src = root / "configs" / "endstation_ax7101_1x1_tdm8.yaml"
base = yaml.safe_load(src.read_text())
PROBES = [("int 0x22", 0x22), ("int 0xFE", 0xFE), ("omitted", None),
          ("int 0x31", 0x31), ("int 0x1F", 0x1F), ("int 0xFF", 0xFF),
          ("string '0x22'", "0x22"), ("string '34'", "34"),
          ("bool true", True), ("float 34.7", 34.7), ("null", "NULL")]
for label, value in PROBES:
    cfg = yaml.safe_load(src.read_text())
    if value is None:
        cfg["gptp"].pop("clock_accuracy", None)
    elif value == "NULL":
        cfg["gptp"]["clock_accuracy"] = None
    else:
        cfg["gptp"]["clock_accuracy"] = value
    p = tmp / "probe.yaml"
    # keep the include-relative paths valid: write next to the original
    p = src.parent / f".probe_{abs(hash(label))}.yaml"
    p.write_text(yaml.safe_dump(cfg, sort_keys=False))
    try:
        got = eb.load_config(str(p))["gptp"]["clock_accuracy"]
        print(f"{label:16s}: accepted, resolves to 0x{got:02X}")
    except eb.ConfigError as e:
        print(f"{label:16s}: ConfigError: {str(e)[:110]}")
    except Exception as e:  # noqa: BLE001 - the probe reports the class
        print(f"{label:16s}: UNNAMED {type(e).__name__}: {str(e)[:110]}")
    finally:
        p.unlink()

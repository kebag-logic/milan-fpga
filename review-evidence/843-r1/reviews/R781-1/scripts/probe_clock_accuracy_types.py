#!/usr/bin/env python3
"""Load the AX7101 1x1 config with gptp.clock_accuracy replaced by values of
several YAML types and report what the builder resolves or raises.
usage: probe_clock_accuracy_types.py <repo> <scratch dir>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(root / "sw/builder"))
import endstation_builder as eb
src = (root / "configs/endstation_ax7101_1x1_tdm8.yaml").read_text()
for label, lit in [("int 0x22", "0x22"), ("int 34", "34"), ("float 34.9", "34.9"),
                   ("string '0x22'", "'0x22'"), ("bool true", "true"),
                   ("null", "null"), ("int 0x20 low end", "0x20"),
                   ("int 0x31 high end", "0x31"), ("int 0xFE", "0xFE"),
                   ("int 0x21 (valid, not the board's)", "0x21"),
                   ("negative -1", "-1")]:
    text, n = re.subn(r"(?m)^  clock_accuracy: 0x22$", f"  clock_accuracy: {lit}", src)
    assert n == 1
    p = out / "probe.yaml"; p.write_text(text)
    try:
        c = eb.load_config(str(p))
        print(f"{label:38s} -> accepted, resolved 0x{c['gptp']['clock_accuracy']:02X}, "
              f"args {eb.gptp_ucode_args(c)[-2:]}")
    except eb.ConfigError as e:
        print(f"{label:38s} -> ConfigError: {str(e)[:90]}")
    except Exception as e:
        print(f"{label:38s} -> {type(e).__name__} (not ConfigError): {str(e)[:90]}")

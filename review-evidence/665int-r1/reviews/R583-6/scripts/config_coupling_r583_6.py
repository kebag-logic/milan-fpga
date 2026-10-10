#!/usr/bin/env python3
"""R583-6 probe: does gate 23m hold every shape the census elaborates?

Adds configs/endstation_probe_r5836.yaml (a renamed copy of
endstation_arty_4x4.yaml) to a DISPOSABLE tree, then prints the shapes the
census would elaborate (census_elab.shapes()) and the configurations gate 23m
iterates (test_builder.CONFIGS), and removes the file again.

    config_coupling_r583_6.py TREE
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
src = (tree / "configs/endstation_arty_4x4.yaml").read_text(encoding="utf-8")
probe = tree / "configs/endstation_probe_r5836.yaml"
probe.write_text(re.sub(r"(?m)^name:\s*\S+", "name: endstation_probe_r5836", src, count=1), encoding="utf-8")
try:
    sys.path.insert(0, str(tree / "sw/mailbox"))
    import census_elab as ce
    census = [s.name for s in ce.shapes()]
    text = (tree / "sw/builder/test_builder.py").read_text(encoding="utf-8")
    block = re.search(r"^CONFIGS = \{(.*?)^\}", text, re.S | re.M).group(1)
    gate = sorted(Path(p).stem for p in re.findall(r'"(configs/[^"]+\.yaml)"', block))
    print("census shapes:", census)
    print("gate 23m configs (test_builder.CONFIGS):", gate)
    missing = sorted(set(census) - {"recipe"} - set(gate))
    print("elaborated by the census but not held by gate 23m:", missing or "none")
finally:
    probe.unlink()

#!/usr/bin/env python3
"""Test-only fixture: arty_current with clocking.crf_output.enabled=true,
headers emitted by the builder itself. usage: make-crfon-fixture.py <tree> <out>"""
import copy, pathlib, sys, yaml
tree, out = map(pathlib.Path, sys.argv[1:3])
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
raw = yaml.safe_load((tree / "configs/endstation_arty_current.yaml").read_text())
raw.setdefault("clocking", {}).setdefault("crf_output", {})["enabled"] = True
(out / "config.yaml").write_text(yaml.safe_dump(raw, sort_keys=False))
cfg = eb.load_config(out / "config.yaml")
(out / "gen").mkdir(exist_ok=True)
(out / "gen/adp_shape_defaults.svh").write_text(eb.emit_adp_shape_svh(cfg))
(out / "gen/lwsrp_csr_defaults.svh").write_text(eb.emit_csr_defaults_svh(cfg))
print("outputs", len(cfg["talkers"]) + int(cfg["clocking"]["crf_output"]))

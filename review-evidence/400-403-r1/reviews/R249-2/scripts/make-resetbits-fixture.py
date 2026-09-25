#!/usr/bin/env python3
"""Test-only fixture: arty_current with srp.enable_at_reset and
srp.talker_declare_at_reset both true; headers emitted by the builder.
usage: make-resetbits-fixture.py <tree> <out>"""
import pathlib, sys, yaml
tree, out = map(pathlib.Path, sys.argv[1:3])
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
raw = yaml.safe_load((tree / "configs/endstation_arty_current.yaml").read_text())
raw.setdefault("srp", {}).update(enable_at_reset=True, talker_declare_at_reset=True, rtl_table=False)
(out / "gen").mkdir(parents=True, exist_ok=True)
(out / "config.yaml").write_text(yaml.safe_dump(raw, sort_keys=False))
cfg = eb.load_config(out / "config.yaml")
(out / "gen/adp_shape_defaults.svh").write_text(eb.emit_adp_shape_svh(cfg))
(out / "gen/lwsrp_csr_defaults.svh").write_text(eb.emit_csr_defaults_svh(cfg))
print("LWSRP_CTRL reset", eb.srp_reset_words(cfg)["LWSRP_CTRL"])

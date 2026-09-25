#!/usr/bin/env python3
"""Every committed generated shape header equals the builder's emission, and
the tracked hdl/ copies equal the rtl_table config's. usage: <tree>"""
import pathlib, sys
tree = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(tree / "sw/builder"))
import endstation_builder as eb
bad = 0
owners = []
for path in sorted((tree / "configs").glob("endstation_*.yaml")):
    cfg = eb.load_config(path)
    emitted = eb.emit_adp_shape_svh(cfg)
    committed = (tree / "configs/generated" / path.stem / "gen/adp_shape_defaults.svh").read_text()
    ok = emitted == committed
    bad += not ok
    print(f"{path.stem}: generated adp_shape_defaults.svh {'==' if ok else '!='} emission")
    if cfg["srp"].get("rtl_table"):
        ok = (tree / "hdl/common/csr/gen/lwsrp_csr_defaults.svh").read_text() == eb.emit_csr_defaults_svh(cfg)
        bad += not ok
        print(f"  rtl_table owner {path.stem}: hdl/common/csr/gen/lwsrp_csr_defaults.svh {'==' if ok else '!='} emission")
    if (tree / "hdl/common/gen/adp_shape_defaults.svh").read_text() == emitted:
        owners.append(path.stem)
        print(f"  hdl/common/gen/adp_shape_defaults.svh == {path.stem} emission")
bad += len(owners) != 1
print('tracked hdl/common/gen shape owner:', owners)
sys.exit(1 if bad else 0)

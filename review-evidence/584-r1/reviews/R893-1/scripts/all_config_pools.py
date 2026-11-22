"""Every tracked configuration's STREAM_PORT_INPUT pools, cluster names, input map counts and output cluster counts as
the builder resolves them. Run from the repository root: python3 -I all_config_pools.py"""
import glob
import sys
sys.path.insert(0, "sw/builder")
import endstation_builder as eb
for f in sorted(glob.glob("configs/endstation_*.yaml")):
    cfg = eb.load_config(f)
    ins = [(p["clusters"], [g["role"] for g in p["pool"]]) for p in cfg["ports_in"]]
    print(f, "in", ins, "out", [p["clusters"] for p in cfg["ports_out"]], "maps_in", [p["maps"] for p in cfg["ports_in"]])
    print("   names", [eb.cluster_names(cfg, p, "input") for p in cfg["ports_in"]])
    print("   model_id", eb.emit_aem_overlay(cfg)["model_id"]["value"])

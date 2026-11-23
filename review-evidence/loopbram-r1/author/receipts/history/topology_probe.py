#!/usr/bin/env python3
"""Read-only reproduction of the input-map geometry boundary at #979's base."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(root / "sw/builder"), str(root / "avdecc")]
import endstation_builder as builder
import aem_assemble
from aem_specs import builtin_spec

result = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
          "scope": "Input-map table construction only; no full candidate generation, RTL or area measurement.",
          "base_shapes": [], "geometry_probes": []}
for shape, config in (("1x1/1if", "endstation_ax7101_1x1_tdm8"),
                      ("8x8/1if", "endstation_ax7101_8x8")):
    cfg = builder.load_config(str(root / "configs" / (config + ".yaml")))
    result["base_shapes"].append({"shape": shape,
        "input_cluster_counts": [p["clusters"] for p in cfg["ports_in"]],
        "input_pools": [p["pool"] for p in cfg["ports_in"]],
        "legacy_loopback_enabled": cfg["interface"]["cluster_fabric"]["loopback_lane"],
        "output_cluster_counts": [p["clusters"] for p in cfg["ports_out"]]})

cases = (("selected B: physical plus eight on port 0, seven on port 7", [9] + [8]*6 + [7], 64, True), ("minimal: physical plus one loop per port", [2] + [1]*7, 9, True),
         ("63 separate loop channels plus physical", [8]*8, 64, True),
         ("64 loop channels, first sharing the physical mapping", [8]*8, 64, True),
         ("64 separate loop channels plus physical", [9] + [8]*7, 65, False),
         ("1x1: eight physical plus eight separate loop", [16], 16, True))
for name, widths, expected_keys, expected_pass in cases:
    spec = copy.deepcopy(builtin_spec())
    spec["ports_in"] = []
    base = 0
    for width in widths:
        spec["ports_in"].append(dict(base_cluster=base, clusters=width,
                                     map_mode="dynamic", maps=0))
        base += width
    assert base == expected_keys
    try:
        table = aem_assemble._dynmap_tables(spec)
        assert expected_pass, name
        assert table["KEYS"] == expected_keys
        row = {"case": name, "keys": base, "result": "accepted geometry",
               "page_size": table["PAGE"], "pages_per_port": table["PNMAPS"]}
    except ValueError as exc:
        assert not expected_pass, (name, str(exc))
        assert str(exc) == "65 dynamic cluster keys exceeds the 64-key render map address space (chmap64)"
        row = {"case": name, "keys": base, "result": "refused as expected", "reason": str(exc)}
    result["geometry_probes"].append(row)
result["source_sha256"] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
    for name in ("avdecc/aem_assemble.py", "sw/builder/endstation_builder.py",
                 "hdl/ieee1722/aaf/KL_render_queue.sv", "hdl/milan/milan_datapath.sv",
                 "hdl/ieee1722/aaf/KL_chan_map_capture.sv")}
print(json.dumps(result, indent=2))

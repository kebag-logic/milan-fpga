#!/usr/bin/env python3
"""Run the named gates of sw/builder/test_builder.py, and print the launch shape per config.
usage: builder_focus.py <tree>"""
import importlib, sys, traceback
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / "sw/builder"))
t = importlib.import_module("test_builder")
names = ["test_gptp_launch_observer_seam", "test_gptp_launch_shape_follows_the_phy",
         "test_reboot_egress_statement", "test_reboot_egress_statement_gate_bites",
         "test_datapath_params_match_the_instance"]
bad = 0
for name in names:
    try:
        getattr(t, name)(); print("PASS", name)
    except Exception:
        bad += 1; print("FAIL", name); traceback.print_exc()
eb = t.eb if hasattr(t, "eb") else importlib.import_module("endstation_builder")
for path in sorted((tree / "configs").glob("endstation_*.yaml")):
    try:
        cfg = eb.load_config(path)
        params = eb.datapath_params(cfg)
        print(path.name, cfg["board_target"], {k: v for k, v in params.items() if k.startswith("GPTP_ETH") or k == "REBOOT_MAC_MIN_MBPS_P"}, "RXFILT_P" in params and params["RXFILT_P"])
    except Exception as exc:
        print(path.name, "skipped:", type(exc).__name__, str(exc)[:100])
print("RESULT", "FAIL" if bad else "PASS")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""Run the unchanged round-2 make_probe_tree_r2.py (probe C) against the round-3 head.

make_probe_tree_r2.py pins its export revision in the module constant HEAD.
The script bytes are not edited: this driver loads it as a module, rebinds HEAD
to the reviewed head, and calls its main() with the same arguments.

Usage: python3 run_probe_c_at_head.py <clone> <out-dir>
"""
import importlib.util
import sys
from pathlib import Path

HEAD = "3face0914efd9d5e71f36da7e30108cfe09c837d"

spec = importlib.util.spec_from_file_location(
    "make_probe_tree_r2", Path(__file__).with_name("make_probe_tree_r2.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.HEAD = HEAD
sys.exit(mod.main())

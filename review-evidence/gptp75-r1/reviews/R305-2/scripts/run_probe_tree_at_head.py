#!/usr/bin/env python3
"""Run the unchanged round-1 make_probe_tree.py against the round-2 head.

make_probe_tree.py pins its export revision in the module constant HEAD. The
script bytes are not edited: this driver loads it as a module, rebinds HEAD to
the reviewed head, and calls its main() with the same arguments.

Usage: python3 run_probe_tree_at_head.py <clone> <out-dir>
"""
import importlib.util
import sys
from pathlib import Path

HEAD = "4a897e44243d39945df763d00b96049363a58e78"

spec = importlib.util.spec_from_file_location(
    "make_probe_tree", Path(__file__).with_name("make_probe_tree.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.HEAD = HEAD
sys.exit(mod.main())

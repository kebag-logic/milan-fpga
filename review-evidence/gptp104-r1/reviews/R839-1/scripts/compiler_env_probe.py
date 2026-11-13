#!/usr/bin/env python3
"""Print what an engine arm's compiler_env() returns for OBJCACHE/CCACHE_*.

usage: compiler_env_probe.py <tree>/tb/verilator/engine/mutants.py
Imports the arm from its own file; builds nothing.
"""
import importlib.util
import sys

spec = importlib.util.spec_from_file_location("arm", sys.argv[1])
arm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(arm)
env = arm.compiler_env()
for key in sorted(k for k in env if k == "OBJCACHE" or k.startswith("CCACHE_")):
    print(f"  compiler_env: {key}=[{env[key]}]")

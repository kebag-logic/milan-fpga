"""Run <tree>/scripts/act_ci.py --selftest with os.cpu_count stubbed to N (a hosted 4-vCPU runner, a 1-CPU host).

Usage (inside a disposable boundary, cwd = tree root): python3 -I cpu_stub_selftest.py N
"""
import os
import runpy
import sys

count = int(sys.argv[1])
os.cpu_count = lambda: count
sys.argv = ["scripts/act_ci.py", "--selftest"]
runpy.run_path("scripts/act_ci.py", run_name="__main__")

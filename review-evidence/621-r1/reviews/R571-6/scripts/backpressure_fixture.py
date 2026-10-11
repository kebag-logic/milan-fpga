#!/usr/bin/env python3
"""Exercise unchanged backpressure tests with the required relative recipe input.
This supplies a fixture location only; it does not repair the default #720 path.
"""
import pathlib, sys, tempfile
root = pathlib.Path(sys.argv[1]).resolve()
packet = pathlib.Path(sys.argv[2]).resolve()
fixtures = pathlib.Path(tempfile.mkdtemp(prefix="backpressure-fixtures-", dir=packet / "scratch"))
recipe = fixtures / "nvm_capture_cpu/recipe.py"
recipe.parent.mkdir(exist_ok=True)
recipe.write_bytes((root / "tb/verilator/nvm_capture_cpu/recipe.py").read_bytes())
sys.path.insert(0, str(root / "tb/verilator/milan_dp"))
import test_sim_pool_backpressure as tests
raise SystemExit(tests.run(fixtures))

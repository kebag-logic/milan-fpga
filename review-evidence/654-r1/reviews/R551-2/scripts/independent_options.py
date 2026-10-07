#!/usr/bin/env python3
"""Independent CLI boundary and mutation observations; no source-file writes."""
import argparse
import contextlib
import io
import json
from pathlib import Path
import sys
import types
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "sw/litex"))
source = (root / "sw/litex/milan_soc.py").read_text()
from litex.soc.cores.cpu.naxriscv import NaxRiscv
from litex.soc.cores.cpu.vexiiriscv import VexiiRiscv

class SetupStarted(Exception):
    pass

def module(text):
    mod = types.ModuleType("independent_options_target")
    mod.__file__ = str(root / "sw/litex/milan_soc.py")
    sys.modules[mod.__name__] = mod
    exec(compile(text, mod.__file__, "exec"), mod.__dict__)
    return mod

def cli(mod, token):
    argv = [mod.__file__, "--no-milan", "--sys-clk-freq=50000000"]
    if token is not None:
        argv.append("--l2-bytes=" + token)
    stream = io.StringIO()
    with patch.object(sys, "argv", argv), contextlib.redirect_stderr(stream), \
         patch.object(mod.board_audio_routing, "assert_front_end_routed", side_effect=SetupStarted), \
         patch.object(mod.alinx_ax7101, "Platform", side_effect=AssertionError("platform started")):
        try:
            mod.main()
        except SetupStarted:
            return {"kind": "setup"}
        except SystemExit as exc:
            return {"kind": "exit", "rc": exc.code, "reason": stream.getvalue().splitlines()[-1]}
    raise AssertionError("unexpected completion")

mod = module(source)
rows = []
invalid = ["1e-400", "-1e-400", "1e-1000000", "-1e-1000000", "0.5", "-1", "nan", "sNaN",
           "Infinity", "-Infinity", "1.00000000000000000000000000001", "invalid", "1e999999999999999999999"]
zero = [None, "0", "-0", "+0", "0.0", "-0.0", "0e-400", "-0e-1000000"]
for token in invalid + zero + ["8192", "8192.0", "8.192e3", "1e1000000"]:
    row = {"token": token, **cli(mod, token)}
    if token in zero:
        assert row["kind"] == "setup", row
    else:
        assert row["kind"] == "exit" and row["rc"] == 2, row
        assert ("whole number" if token in invalid else "without a data cache") in row["reason"], row
    rows.append(row)
anchor = "default=None, type=_parse_l2_bytes,"
assert source.count(anchor) == 1
mutant = module(source.replace(anchor, "default=None, type=float,"))
controls = []
for token in ("1e-400", "-1e-400"):
    observation = cli(mutant, token)
    assert observation["kind"] == "setup", observation
    controls.append({"mutation": "restore float parser", "token": token, "observation": observation,
                     "control": "killed by expected refusal"})

def constructor(target, cpu, size):
    with patch.object(NaxRiscv, "args_read", side_effect=SetupStarted), \
         patch.object(VexiiRiscv, "args_read", side_effect=SetupStarted), \
         patch.object(target.SoCCore, "__init__", side_effect=AssertionError("SoC started")):
        try:
            target.MilanSoC(None, 50000000, cpu=cpu, l2_bytes=size, with_milan=False)
        except SetupStarted:
            return "setup"
        except ValueError as exc:
            return str(exc)
    raise AssertionError("unexpected completion")

constructor_rows = []
for cpu in ("NaxRiscv", "unknown", "", None):
    for size in (None, 0):
        outcome = constructor(mod, cpu, size)
        assert "unsupported CPU" in outcome, outcome
        constructor_rows.append({"cpu": cpu, "l2_bytes": size, "reason": outcome})
anchor = 'if cpu not in ("vexiiriscv", "naxriscv"):'
assert source.count(anchor) == 1
mutant = module(source.replace(anchor, "if False:"))
assert constructor(mutant, "NaxRiscv", 0) == "setup"
controls.append({"mutation": "remove unknown CPU guard", "observation": "setup",
                 "control": "killed by expected refusal"})
print(json.dumps({"cli": rows, "constructors": constructor_rows, "controls": controls}, indent=2))
print("PASS: exact CLI tokens, genuine zeros, setup boundaries and three independent controls")

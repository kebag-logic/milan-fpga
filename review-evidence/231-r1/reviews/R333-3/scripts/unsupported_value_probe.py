#!/usr/bin/env python3
"""Show what dropping the unsupported-log-value refusal admits.
usage: unsupported_value_probe.py <pp_baseline.py>
Feeds wrapper_parameters() a log whose only override uses a value format the
parser does not model (hex), with pristine and mutant helpers."""
import importlib.util, sys, tempfile
from pathlib import Path
src = Path(sys.argv[1]).read_text()
old = '            raise ValueError(f"unsupported parameter value: {name}={raw}")\n'
assert src.count(old) == 1
log = ("INFO: synthesizing module 'KL_pp_shadow' [w.sv:1]\n"
       "\tParameter N_STREAM_IN_P bound to: 32'h2\n"
       "\tParameter RX_FIFO_BYTES_P bound to: 32'b1000000000000\nINFO: end\n")
wrapper = "parameter int unsigned N_STREAM_IN_P = 8,\nparameter int unsigned RX_FIFO_BYTES_P = 4096,\n"
for name, text in (("pristine", src), ("mutant", src.replace(old, "            continue\n"))):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "pp_baseline.py"
        f.write_text(text)
        spec = importlib.util.spec_from_file_location(name, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        try:
            print(f"{name}: accepted {mod.wrapper_parameters(log, wrapper)} (elaborated N_STREAM_IN_P is 2)")
        except ValueError as error:
            print(f"{name}: refused: {error}")

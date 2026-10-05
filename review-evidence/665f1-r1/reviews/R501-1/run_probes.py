#!/usr/bin/env python3
"""Build fault probes against the exact checkout, writing only below scratch."""
import os
from pathlib import Path
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
work = out / "scratch" / "probes"
work.mkdir(parents=True, exist_ok=True)
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True
sys.path.insert(0, str(repo / "sw/firmware/ctrl_nvm/test"))
import nvm_bench as b
inputs = b.shape_inputs(repo / "configs/endstation_ax7101_1x1_tdm8.yaml", work)
gen = work / "gen"
gen.mkdir(exist_ok=True)
(gen / "nvm_shape_gen.h").write_text(b.shape_header(inputs.shape, inputs.donor, inputs.ident))
cmd = ["gcc", *b.CFLAGS, "-I"+str(gen), "-I"+str(b.TREE / "host/stubs"), "-I"+str(b.TREE / "test"),
       *(str(b.TREE / src) for src in b.SOURCES[:-1]), str(out / "probe_store.c"), "-o", str(work / "probe_store")]
subprocess.run(cmd, check=True, timeout=60)
subprocess.run([str(work / "probe_store")], check=True, timeout=20)

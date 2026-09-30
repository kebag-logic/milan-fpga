#!/usr/bin/env python3
"""Wrap rv32_image() to save every -no-pie linked ELF the gate reads for the
shipping firmware, then stop after the baseline. Independent receipt: the raw
image the pins are decided on, for readelf."""
import os, sys, importlib.util
from pathlib import Path
tree = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]); out.mkdir(exist_ok=True)
sys.argv = [str(tree/"sw/builder/test_builder.py"), "--require-rv32"]
sys.path.insert(0, str(tree/"sw/builder"))
spec = importlib.util.spec_from_file_location("test_builder", sys.argv[0])
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
orig = mod.rv32_image; n = [0]
def wrap(elf, *a, **k):
    (out/f"unit_{n[0]}.elf").write_bytes(elf); n[0]+=1
    return orig(elf, *a, **k)
mod.rv32_image = wrap
os.environ["R413_STOP_AFTER_BASELINE"]="1"
try: mod.test_baremetal_profile_contract()
except SystemExit: pass
print("saved", n[0], "elf(s) to", out)

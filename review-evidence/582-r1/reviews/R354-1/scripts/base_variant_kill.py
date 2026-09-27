#!/usr/bin/env python3
"""R354-1: in a disposable extraction of the source base 9e9954e9, show that
the removed gate-1b "fabric clock" variant (milan_clk_hz 80 MHz, ROM must
differ from the shipping-AX ROM) detects a builder that stops forwarding
--clk-hz to the gPTP ROM generator.

Usage: base_variant_kill.py <base-tree>   (the tree's builder file is mutated
and restored in place; the tree must be a disposable copy)
"""
import copy
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

TREE = Path(sys.argv[1]).resolve()
BUILDER = TREE / "sw/builder/endstation_builder.py"
OLD = '             "--clk-hz", str(cfg["constraints"]["milan_clk_hz"])],'
NEW = '             ],'
PROBE = r'''
import copy, hashlib, sys, tempfile, yaml
from pathlib import Path
sys.path.insert(0, "sw/builder")
import endstation_builder as eb
raw = yaml.safe_load(Path("configs/endstation_ax7101_1x1_tdm8.yaml").read_text())
def rom(r, td, tag):
    p = td / f"{tag}.yaml"; p.write_text(yaml.safe_dump(r))
    return Path(eb.build(p, td / tag, write_fragment=False)["paths"]["gptp_ucode"]).read_bytes()
with tempfile.TemporaryDirectory() as t:
    td = Path(t); base = rom(raw, td, "base")
    v = copy.deepcopy(raw); v["board"]["constraints"]["milan_clk_hz"] = 80_000_000
    var = rom(v, td, "v80")
    print("base ROM", hashlib.sha256(base).hexdigest()[:16], "80MHz ROM", hashlib.sha256(var).hexdigest()[:16])
    print("removed variant assertion (image != base_ucode):", "PASS" if var != base else "FAIL -> mutant killed")
'''


def run(label: str) -> None:
    r = subprocess.run([sys.executable, "-c", PROBE], cwd=TREE, capture_output=True, text=True)
    print(f"[{label}] rc={r.returncode}")
    print((r.stdout + r.stderr).strip())


text = BUILDER.read_text()
assert text.count(OLD) == 1
run("base builder")
BUILDER.write_text(text.replace(OLD, NEW))
try:
    run("base builder, --clk-hz not forwarded")
finally:
    BUILDER.write_text(text)
assert BUILDER.read_text() == text

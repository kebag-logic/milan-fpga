#!/usr/bin/env python3
"""Export one shipped config's gateware (no vendor tool, no firmware) from a tree.

Usage: default_build_probe.py TREE CONFIG_STEM OUTDIR [extra milan_soc args...]

Runs the builder to obtain the config's milan_soc.py argv, then runs the
tree's own milan_soc.py with --no-compile-software --no-compile-gateware into
OUTDIR. Compare two OUTDIRs with normalise_compare.py.
"""
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    tree, stem, out = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3]).resolve()
    extra = sys.argv[4:]
    py = sys.executable
    cfg = tree / "configs" / f"{stem}.yaml"
    gen = (
        "import sys; sys.path.insert(0, 'sw/builder'); import endstation_builder as eb; "
        f"eb.build(__import__('pathlib').Path('{cfg}'), __import__('pathlib').Path('{tree}/sw/builder/out'))"
    )
    res = subprocess.run([py, "-c", gen], cwd=tree, capture_output=True, text=True)
    if res.returncode != 0:
        print(res.stdout[-4000:], res.stderr[-4000:])
        return 2
    argv = json.loads((tree / "sw/builder/out" / stem / "soc_params.json").read_text())["argv"]
    argv += ["--entity-gen-dir", str(tree / "configs/generated" / stem),
             "--no-compile-software", "--no-compile-gateware", "--output-dir", str(out / "soc"), *extra]
    res = subprocess.run([py, str(tree / "sw/litex/milan_soc.py"), *argv], cwd=tree / "sw/litex",
                         capture_output=True, text=True)
    (out / "soc.log").write_text(res.stdout + res.stderr)
    print(f"milan_soc rc={res.returncode} argv={' '.join(argv)}")
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())

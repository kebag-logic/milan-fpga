#!/usr/bin/env python3
"""[R383] Regenerate the AX7101 1x1 TDM8 sweep build inputs without a vendor run
and compare them with the retained round-1 sweep inputs.

For each tree and each place directive, run milan_soc.py with the published
sweep argv (soc_params.json argv + directives + 16 threads) but with
--no-compile-software --no-compile-gateware in place of --build, then compare
alinx_ax7101.{tcl,xdc,v} byte-for-byte with the retained sweep directory after
replacing the tree root and output directory with fixed tokens.
Usage: regen_sweep_inputs.py <python> <retained work dir> <retained lane root>
                             <out dir> <label=tree>...
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

py, work, lane, out = sys.argv[1], Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]).resolve()
trees = dict(a.split("=", 1) for a in sys.argv[5:])
SEEDS = [("asl", "AltSpreadLogic_high"), ("eto", "ExtraTimingOpt"),
         ("eppo", "ExtraPostPlacementOpt")]
CFG = "endstation_ax7101_1x1_tdm8"
env = dict(os.environ, PYTHONHASHSEED="0")


def norm(text, root, outdir):
    return text.replace(str(outdir), "<OUT>").replace(str(root), "<ROOT>")


def h(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


bad = 0
for label, tree in trees.items():
    tree = Path(tree).resolve()
    subprocess.run([py, "sw/builder/endstation_builder.py", f"configs/{CFG}.yaml"], cwd=tree,
                   env=env, check=True, capture_output=True, timeout=300)
    argv = json.loads((tree / "sw/builder/out" / CFG / "soc_params.json").read_text())["argv"]
    for seed, directive in SEEDS:
        dest = out / f"{label}-{seed}"
        cmd = [py, str(tree / "sw/litex/milan_soc.py"), *argv,
               "--entity-gen-dir", str(tree / "configs/generated" / CFG),
               "--synth-directive", "AreaOptimized_high", "--opt-directive", "ExploreArea",
               "--place-directive", directive, "--vivado-max-threads", "16",
               "--no-compile-software", "--no-compile-gateware", "--output-dir", str(dest)]
        r = subprocess.run(cmd, cwd=tree / "sw/litex", env=env, capture_output=True, text=True,
                           timeout=900)
        if r.returncode:
            print(f"{label} {seed}: ELABORATION rc={r.returncode}\n{r.stderr[-2000:]}")
            bad += 1
            continue
        retained = work / f"build_ax7101_{seed}_350af5dcf"
        for name in ("alinx_ax7101.tcl", "alinx_ax7101.xdc", "alinx_ax7101.v"):
            new = norm((dest / "gateware" / name).read_text(), tree, dest)
            old = norm((retained / "gateware" / name).read_text(), lane, retained)
            same = new == old
            bad += not same
            print(f"{label} {seed} {name}: {'IDENTICAL' if same else 'DIFFERENT'} "
                  f"regen={h(new)} retained={h(old)} lines={len(new.splitlines())}")
            if not same:
                import difflib
                diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                                 "retained", "regen", n=0, lineterm=""))
                print("\n".join(diff[:40]))
        bits = sorted(p.name for p in (dest / "gateware").glob("*.bit*"))
        print(f"{label} {seed}: bitstream-like files after elaboration: {bits or 'none'}")
print(f"differences={bad}")
sys.exit(1 if bad else 0)

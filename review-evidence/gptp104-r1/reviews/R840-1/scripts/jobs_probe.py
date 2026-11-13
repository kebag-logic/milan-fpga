#!/usr/bin/env python3
"""Sensitivity probes for tb/mutation_jobs_test.py on a reduced arm.

usage: jobs_probe.py <head-tree> <scratch-dir> <out-dir> <variant>

Copies the head tree to <scratch-dir>/jobs-<variant>, cuts the copy's
MUTATIONS down to SUBSET (real mutants: two RTL, one generator-only), plants
the variant's defect, and runs the copy's own mutation_jobs_test.py against
the copy's mutants.py with --out. The head tree is never edited.

variants:
  baseline      no defect; the test must pass
  abs-paths     build() hands Verilator absolute staged paths again, so the
                temporary directory reaches the model C++ and the cache key;
                the warm checks must fail
  objcache-on   compiler_env() forces OBJCACHE=ccache even when the caller
                set it empty; the off runs' "wrote nothing" checks must fail
"""
import shutil
import subprocess
import sys
from pathlib import Path

head, scratch, out = (Path(a).resolve() for a in sys.argv[1:4])
variant = sys.argv[4]
ARM = "tb/verilator/engine/mutants.py"
SUBSET = (
    "slew level tied low",                 # RTL, top/KL_gptp_engine.sv
    "slew clears at the first in-band pair",  # generator only
    "the path-count refusal restored",     # RTL, wire/KL_gptp_rx_parser.sv, pair list
)
CUT = ("\n\ndef edits_of(",
       "\n\n# REVIEW PROBE: reduced arm\nMUTATIONS = [m for m in MUTATIONS if m[0] in "
       + repr(SUBSET) + "]\n\n\ndef edits_of(")
DEFECTS = {
    "baseline": [],
    "abs-paths": [(
        "         *RTL_SOURCES, str(HERE / \"sim_main.cpp\"), \"-o\", exe_name],\n"
        "        cwd=str(srcdir), env=compiler_env(), capture_output=True, text=True)\n",
        "         *[str(srcdir / s) for s in RTL_SOURCES],\n"
        "         str(HERE / \"sim_main.cpp\"), \"-o\", exe_name],\n"
        "        env=compiler_env(), capture_output=True, text=True)\n")],
    "objcache-on": [(
        "    env.setdefault(\"OBJCACHE\", \"ccache\" if shutil.which(\"ccache\") else \"\")\n",
        "    env[\"OBJCACHE\"] = \"ccache\"\n")],
}

tree = scratch / f"jobs-{variant}"
if tree.exists():
    shutil.rmtree(tree)
shutil.copytree(head, tree)
arm = tree / ARM
text = arm.read_text(encoding="utf-8")
for old, new in [CUT] + DEFECTS[variant]:
    assert text.count(old) == 1, (variant, old)
    text = text.replace(old, new)
arm.write_text(text, encoding="utf-8")
dest = out / variant
dest.mkdir(parents=True, exist_ok=True)
res = subprocess.run(
    [sys.executable, str(tree / "tb/mutation_jobs_test.py"), str(arm), "--out", str(dest / "runs")],
    cwd=str(tree / "tb/verilator/engine"), capture_output=True, text=True)
(dest / "jobs-test.log").write_text(res.stdout + res.stderr, encoding="utf-8")
(dest / "rc").write_text(f"rc={res.returncode}\n", encoding="utf-8")
print(f"{variant}: rc {res.returncode}")
print(res.stdout[-4000:], res.stderr[-2000:])

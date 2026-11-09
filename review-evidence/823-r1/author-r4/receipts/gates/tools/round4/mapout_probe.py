"""Compile nvm_klj2.c with MAPOUT_0 = 65536 and the MAPOUT width assert removed; print the compiler's errors."""
import shutil, subprocess, sys
from pathlib import Path
root = Path(sys.argv[1]).resolve(); work = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl_nvm/test"))
import test_ctrl_nvm as t, nvm_bench as nb
shutil.rmtree(work, ignore_errors=True)
tree = work / "tree"; shutil.copytree(nb.TREE, tree, ignore=shutil.ignore_patterns("__pycache__", "test"))
h = tree / "nvm_shape.h"; s = h.read_text(); line = t.WIDTHS[1][3]; assert s.count(line) == 1
h.write_text(s.replace(line, ""))
inputs = nb.shape_inputs(root / "configs/endstation_ax7101_1x1_tdm8.yaml", work / "inputs")
gen = work / "gen"; nb.write_headers(gen, nb.doctor(nb.shape_header(inputs), (("MILAN_NVM3_MAPOUT_ENTRIES_0", 65536),)), inputs.clock_hz)
cmd = ["cc", *nb.CFLAGS, "-Wno-overflow", *nb.includes(tree, gen), "-c", str(tree / "nvm_klj2.c"), "-o", str(work / "o.o")]
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode)
print("\n".join(l for l in r.stderr.splitlines() if "error" in l))

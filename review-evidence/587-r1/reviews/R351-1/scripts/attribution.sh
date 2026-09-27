#!/bin/bash
# Recipe attribution variant: separate export directory, --attribution-only preparation, same synthesis command.
set -u
S=$REVIEWS/587-r351-1-packet/scratch
export REPO=$REVIEWS/r351-1-587 WORK=$S/work-attr LITEX_PYTHON=$S/pybin/python3 SDK=$S/sdk 
export PATH="$HOME/Xilinx/2026.1/Vivado/bin:$SDK/bin:$S/pybin:/usr/bin:/bin" PYTHONHASHSEED=0 LITEX_ENV_CC_TRIPLE=riscv32-linux
mkdir -p $WORK; cp $S/work/ax8x8-dry-run.log $WORK/
cd $REPO
/usr/bin/python3 - <<'PY'
import json, os, shlex, subprocess
from pathlib import Path
root = Path(os.environ["REPO"]); work = Path(os.environ["WORK"]); python = os.environ["LITEX_PYTHON"]
preview = (work / "ax8x8-dry-run.log").read_text()
lines = [l for l in preview.splitlines() if "exec python3 milan_soc.py " in l]
assert len(lines) == 1
argv = shlex.split(lines[0].split("exec python3 ", 1)[1]); argv.remove("--build")
argv[argv.index("--output-dir") + 1] = str(work / "ax8x8")
(work / "ax8x8-argv.json").write_text(json.dumps(argv, indent=2))
with (work / "ax8x8-elaboration.log").open("w") as log:
    subprocess.run([python, *argv], cwd=root / "sw/litex", stdout=log, stderr=subprocess.STDOUT, check=True)
PY
echo "export rc=$?" > $WORK/attr.rc
python3 $REPO/syn/ooc/pp_baseline.py $WORK/ax8x8/gateware --synthesis-only --attribution-only > $WORK/prepare.log 2>&1; echo "prepare rc=$?" >> $WORK/attr.rc
cd $WORK/ax8x8/gateware && vivado -mode batch -source baseline_integrated.tcl -nojournal -log baseline.log > vivado.stdout 2>&1; echo "synthesis rc=$?" >> $WORK/attr.rc

#!/usr/bin/env bash
# ax_export.sh <tree> <out>: elaborate the AX7101 1x1 shipping build without Vivado and keep the top Verilog.
set -u
tree=$1 W=$2; mkdir -p "$W"; cd "$tree" || exit 3
PY=${MILAN_LITEX_PYTHON:-$HOME/litex-milan/venv/bin/python3}
export PATH=$(dirname "$PY"):$PATH PYTHONHASHSEED=0
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml --write-rtl > "$W/writertl.log" 2>&1 || { echo write-rtl failed; exit 5; }
(cd sw/litex && TAG=r762 ./build.sh ax7101 --dry-run) > "$W/dry-run.log" 2>&1 || { echo dry-run failed; exit 6; }
line=$(grep "exec python3 milan_soc.py " "$W/dry-run.log" | head -1)
python3 -c "
import shlex,sys,json
a=shlex.split(sys.argv[1].split('exec python3 ',1)[1]); a.remove('--build')
a[a.index('--output-dir')+1]=sys.argv[2]
print(json.dumps(a))" "$line" "$W/out" > "$W/argv.json"
python3 -c "
import json,subprocess,sys
a=json.load(open(sys.argv[1])); r=subprocess.run([sys.argv[2],*a],cwd='sw/litex',stdout=open(sys.argv[3],'w'),stderr=subprocess.STDOUT)
sys.exit(r.returncode)" "$W/argv.json" "$PY" "$W/elaboration.log"; rc=$?
echo "elaboration rc=$rc"; exit $rc

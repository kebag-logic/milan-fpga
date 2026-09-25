#!/bin/sh
# [R325] R325-3 disposable probes of scripts/check_nvm_capture.py against REAL
# source edits (not its in-memory controls), plus the receipt-edit residual.
# Usage: r325_gate_input_probes.sh <clean clone at b02af048> <scratch dir>
set -u
CLONE=$1; SCRATCH=$2; M=$SCRATCH/gatemut
rm -rf "$M"; cp -a "$CLONE" "$M"; cd "$M"
test "$(git rev-parse HEAD)" = b02af0480d3a3061df24683d522799d1759f7c33
Y8=configs/endstation_ax7101_8x8.yaml
J=tb/verilator/nvm_capture_cpu/measurements.json
export PYTHONDONTWRITEBYTECODE=1
clean() { git checkout -q -- .; find . -name __pycache__ -type d -prune -exec rm -rf {} + ; }
run() { out=$(python3 -B scripts/check_nvm_capture.py 2>&1); rc=$?; echo "ARM $1 expect=$2 rc=$rc :: $(echo "$out" | grep -E '^(FAIL|PASS)|Error|error' | tail -2 | cut -c1-260)"; clean; }
clean
run baseline pass
sed -i 's/^    milan_clk_hz: 100000000          # single fast domain (AX timing CLOSED)$/    milan_clk_hz: 50000000/' $Y8; git diff --quiet $Y8 && echo "edit failed"; run yaml-8x8-cpu-clock-50MHz fail
sed -i 's/^    sys_clk_hz: 100000000            # milan_soc.py default (sweep passes none)$/    sys_clk_hz: 125000000/' $Y8; git diff --quiet $Y8 && echo "edit failed"; run yaml-8x8-sys-clock fail
sed -i 's/^CPU_HZ = 50_000_000$/CPU_HZ = 40_000_000/' tb/verilator/nvm_capture_cpu/recipe.py; run recipe-cpu-40MHz fail
sed -i 's/^    "SUID": 8,  /    "SUID": 9,  /' scripts/nvm_contract.py; git diff --quiet scripts/nvm_contract.py && echo "edit failed"; run contract-suid-payload+1 fail
sed -i 's/^    - { name: "Stream Out 7", channels: 8, map_mode: dynamic, clusters: 2 }$/    - { name: "Stream Out 7", channels: 8, map_mode: static, clusters: 2 }/' $Y8; git diff --quiet $Y8 && echo "edit failed"; run yaml-8x8-talker7-static-map fail
printf '\n' >> sw/firmware/milan_baremetal/milan_baremetal.c; run firmware-trailing-newline fail
printf '\n' >> tb/verilator/nvm_capture_cpu/soc.py; run harness-soc-edit fail
# Residual 1: a clock edit plus a receipt edit, with no new measurement.
sed -i 's/^    milan_clk_hz: 100000000          # single fast domain (AX timing CLOSED)$/    milan_clk_hz: 40000000/' $Y8
python3 - <<'PY'
import json; p='tb/verilator/nvm_capture_cpu/measurements.json'; r=json.load(open(p))
r['measured_for']['endstation_ax7101_8x8']['configured_cpu_hz']=40000000
for a in r['measurements']:
    if a['shape']=='endstation_ax7101_8x8': a['configured_cpu_hz']=40000000
open(p,'w').write(json.dumps(r, indent=2)+'\n')
PY
run RESIDUAL-yaml-clock-40MHz-plus-receipt-edit residual-pass
# Residual 2: census growth plus run.py expectation, hashes and receipt edits.
sed -i 's/^    "SUID": 8,  /    "SUID": 9,  /' scripts/nvm_contract.py
sed -i 's/expected = (12634, 156) if/expected = (12635, 156) if/; s/else (3218, 53)/else (3219, 53)/' tb/verilator/nvm_capture_cpu/run.py
python3 - <<'PY'
import json, hashlib, pathlib; p='tb/verilator/nvm_capture_cpu/measurements.json'; r=json.load(open(p))
for s in r['measured_for'].values(): s['raw_bytes'] += 1
for a in r['measurements']:
    for row in a['rows']: row['raw'] += 1
h=pathlib.Path('tb/verilator/nvm_capture_cpu')
r['harness_sha256']={f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in h.iterdir() if f.suffix in ('.py','.cpp')}
open(p,'w').write(json.dumps(r, indent=2)+'\n')
PY
run RESIDUAL-census-growth-plus-harness-and-receipt-edit residual-pass
# Ungated by design: product RTL / SoC integration on the measured path.
printf '// probe\n' >> hdl/milan/KL_pp_shadow.sv; run UNGATED-rtl-pp-shadow-edit pass
printf '# probe\n' >> sw/litex/milan_soc.py; run UNGATED-soc-integration-edit pass
printf '# probe\n' >> scripts/nvm_shape.py; run UNGATED-nvm_shape-edit pass
test -z "$(git status --porcelain --untracked-files=no)" && echo "probe copy restored clean"

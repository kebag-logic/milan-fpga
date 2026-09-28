#!/usr/bin/env bash
# Usage: inventory_probe.sh <processor-clone> <scratch-parent-dir> <out-dir>
# Runs only the parent's scripts/measure_test_evidence.py --check on a scratch
# parent (kebag-logic/milan-fpga c0723222) whose protocol-processor tree is:
#  head       exact candidate 0404675d
#  prev       00b5c6c9 (round-2 head)
#  no-ci      0404675d with the hdl.yml mutation step removed (Makefile target kept)
#  no-target  0404675d with the Makefile mutants target removed (hdl.yml step kept)
set -u
pp=$(cd "$1" && pwd); s=$2; out=$(mkdir -p "$3" && cd "$3" && pwd)
PARENT=c07232228c12b72805dd20e6852bf93f25794da0; GPTP=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
cd "$s" && git checkout -q $PARENT
git submodule init protocol-processor gptp-processor >/dev/null
if [ ! -d gptp-processor/.git ]; then rm -rf gptp-processor; git clone -q https://github.com/Mister-M-alt/FPGA-gPTP.git gptp-processor; fi
git -C gptp-processor checkout -q $GPTP
for v in head prev no-ci no-target; do
  rm -rf protocol-processor; git clone -q "$pp" protocol-processor
  case $v in prev) git -C protocol-processor checkout -q 00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c;;
             *) git -C protocol-processor checkout -q 0404675dcd8788d29cb15a831a8c182438bf1c92;; esac
  case $v in
    no-ci) python3 - protocol-processor/.github/workflows/hdl.yml <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
blk='      - name: SRP LeaveAll mutation campaign\n        run: |\n          export PATH="$HOME/verilator/bin:$PATH"\n          make -C tb/srp_top mutants\n'
assert blk in t; open(p,'w').write(t.replace(blk,''))
PY
    ;;
    no-target) python3 - protocol-processor/tb/srp_top/Makefile <<'PY'
import sys; p=sys.argv[1]; t=open(p).read()
blk='mutants:\n\tpython3 mutants.py --output "$(MUTANT_OUTPUT)"\n\n'
assert blk in t; open(p,'w').write(t.replace(blk,''))
PY
    ;;
  esac
  git update-index --cacheinfo 160000,$(git -C protocol-processor rev-parse HEAD),protocol-processor
  git submodule status -- protocol-processor gptp-processor
  git -C protocol-processor diff --stat
  python3 scripts/measure_test_evidence.py --check > "$out/inventory-$v.log" 2>&1; echo "rc=$?" >> "$out/inventory-$v.log"
  echo "== $v: $(head -1 "$out/inventory-$v.log") | srp_top armed: $(grep -c 'protocol-processor/tb/srp_top: ' "$out/inventory-$v.log") | $(tail -1 "$out/inventory-$v.log")"
done
git -C protocol-processor checkout -q -- .; git reset -q; git status --short | head

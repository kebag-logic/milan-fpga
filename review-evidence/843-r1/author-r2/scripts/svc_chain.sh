#!/usr/bin/env bash
# svc_chain.sh <rev>: the fw_service_budget re-measure at <rev> (README "Regenerate the fixture through its generator"):
# a clean clone, svc_driver.sh (round 1's driver, unchanged steps), then gen_oracle.py in the clone and its self-test.
set -u
rev=$1; here=$(cd "$(dirname "$0")" && pwd)
S=$VALIDATION_STORAGE/scratch/843-a737b/svc; C=$S/clone
mkdir -p "$S"
echo "== CLONE $(date -Is)"
bash "$here/make_clone.sh" "$C" "$rev" || { echo "CLONE FAILED"; exit 2; }
echo "== DRIVER $(date -Is)"
bash "$here/svc_driver.sh" "$C" "$S"
for f in "$S"/run-*.log; do echo "$f: $(tail -c 300 "$f" | tail -2 | tr '\n' ' ')"; done
grep -h "^END" "$S"/chain-*.log
if grep -h "^END" "$S"/chain-*.log | grep -qv "rc=0"; then echo "A RUN FAILED"; exit 3; fi
echo "== GEN_ORACLE $(date -Is)"
cd "$C" || exit 2
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 LITEX_ENV_CC_TRIPLE=riscv32-linux
export PATH="/usr/local/bin:/usr/bin:/bin:$HOME/litex-milan/venv/bin:$HOME/br-milan-rv32/host/bin"
export TMPDIR="$S/tmp"
"$HOME/litex-milan/venv/bin/python" -B tb/verilator/fw_service_budget/gen_oracle.py \
  --small-build "$S/fw-1x1" --large-build "$S/fw-8x8" > "$S/gen_oracle.log" 2>&1
echo "gen_oracle rc=$?"
make -C tb/verilator/fw_service_budget --no-print-directory > "$S/make-fw_service_budget.log" 2>&1
echo "make fw_service_budget rc=$?"
git -C "$C" status --short
echo "== SVC-CHAIN-COMPLETE $(date -Is)"

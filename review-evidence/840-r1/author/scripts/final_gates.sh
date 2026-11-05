#!/usr/bin/env bash
# The firmware, builder, behave and whitespace gates this change touches, one log and
# one rc per gate, never piped, each group on its own clean clone of <head>:
#   main  - whitespace, em dash, the firmware self-test and PHY peer, coverage,
#           RV32, saved-state suites, capture census, torture self-test, behave
#   ctrlK - the control-plane firmware suites, shard K of 4 (they write ignored
#           outputs into the checkout, so each shard has its own clone)
#   build - sw/builder/test_builder.py --require-rv32
# Usage: final_gates.sh <head> <scratch>
set -u
H=$1; S=$2; G=$S/logs
here=$(dirname "$(readlink -f "$0")")
mkdir -p "$G" "$S/tmp"
BASE=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
VENV=$VALIDATION_STORAGE/840-a732/gates/venv/bin
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp MAKEFLAGS="-j4 --no-print-directory" CI_CAMPAIGN_JOBS=4 PYTHONHASHSEED=0
P=$BASE
clone() { [ -d "$S/$1" ] || "$here/clone_at.sh" "$H" "$S/$1" > "$G/clone-$1.log" 2>&1; }
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc $(date -Is)"; }
for d in wt wt-ctrl0 wt-ctrl1 wt-ctrl2 wt-ctrl3 wt-build; do clone $d || { echo "clone $d failed"; exit 3; }; done
for d in wt wt-ctrl0 wt-ctrl1 wt-ctrl2 wt-ctrl3 wt-build; do test "$(git -C "$S/$d" rev-parse HEAD)" = "$H" || exit 4; done
main() {
  cd "$S/wt" || exit 3
  run diffcheck "git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD"
  run em_dash "$VENV/python3 scripts/check_em_dash.py --base 604899c08ff1cd1830e1dd08b733109ef852400c"
  run phy_firmware "python3 sw/firmware/nvm_hosttest/test_phy_firmware.py"
  run firmware_selftest "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test"
  run fw_coverage_selftest "python3 sw/firmware/gtest/fw_coverage.py --selftest"
  run fw_coverage_check "python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8"
  run fw_rv32_selftest "python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32"
  run ctrl_nvm "python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 8"
  run nvm_capture "python3 scripts/check_nvm_capture.py"
  run torture_selftest "python3 tb/tools/torture_campaign.py --self-test"
  P=$VENV:$BASE
  run behave "cd tests && behave"
  git status --porcelain > "$G/tree-after-main.txt"
}
ctrl() {
  cd "$S/wt-ctrl$1" || exit 3
  run ctrl_firmware_$1 "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $1/4"
  git status --porcelain > "$G/tree-after-ctrl$1.txt"
}
build() {
  cd "$S/wt-build" || exit 3
  run builder "python3 sw/builder/test_builder.py --require-rv32"
  git status --porcelain > "$G/tree-after-build.txt"
}
main & ctrl 0 & ctrl 1 & ctrl 2 & ctrl 3 & build &
wait
echo done > "$G/DONE"

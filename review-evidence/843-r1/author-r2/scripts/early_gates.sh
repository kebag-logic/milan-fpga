#!/usr/bin/env bash
# early_gates.sh <sha>: the builder bank, behave and the firmware self-test at an intermediate commit, to find a merge
# breakage before the final head; never the final evidence (final_gates.sh is).
set -u
H=$1; S=$VALIDATION_STORAGE/scratch/843-a737b; W=$S/clone-early-${H:0:8}; O=$S/early-gates-${H:0:8}
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O" "$S/tmp-early"
[ -d "$W" ] || bash "$here/make_clone.sh" "$W" "$H" > "$O/clone.log" 2>&1 || exit 3
cd "$W" || exit 3
SDK=$VALIDATION_STORAGE/scratch/803-a693/sdk/br-milan-rv32/host
export HOME=$HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/tmp-early MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c
export PATH=$S/venv-ci/bin:$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:$SDK/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
run() { id=$1; shift; s=$(date +%s); { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s) - s ))" > "$O/$id.rc"; echo "$id rc=$rc"; }
run behave "cd tests && behave"
run fw_selftest "python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test"
run builder "python3 sw/builder/test_builder.py --require-rv32"
git status --porcelain > "$O/tree-after.txt"
echo done > "$O/DONE"

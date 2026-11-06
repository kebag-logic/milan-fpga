#!/usr/bin/env bash
# The lane's own gates, one log and one rc per gate, never piped, on a clean clone of the head.
set -u
H=3e475161e528baa655a5ba84d6a38d78f8c64f3b; W=$VALIDATION_STORAGE/833-a726l/gates/lane-wt; O=$VALIDATION_STORAGE/833-a726l/gates/lane-out
mkdir -p "$O" $VALIDATION_STORAGE/833-a726l/gates/tmp $VALIDATION_STORAGE/833-a726l/gates/lane-home
if [ ! -d "$W" ]; then
  git clone -q --no-checkout $LANES/833-owned-process "$W" && git -C "$W" -c advice.detachedHead=false checkout -q --detach "$H" || exit 2
  for sub in protocol-processor gptp-processor; do git -C "$W" config submodule.$sub.url $LANES/833-owned-process/$sub; done
  git -C "$W" -c protocol.file.allow=always submodule update -q --init protocol-processor gptp-processor || exit 2
  git -C "$W" remote set-url origin https://github.com/kebag-logic/milan-fpga.git
fi
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$VALIDATION_STORAGE/833-a726l/gates/lane-home VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$VALIDATION_STORAGE/833-a726l/gates/tmp MAKEFLAGS="-j4 --no-print-directory" PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
export PATH=$VALIDATION_STORAGE/scratch/a662/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
run() { id=$1; shift; { echo "# head $H gate $id: $*"; grep SigIgn /proc/self/status; bash -c "$*"; } > "$O/$id.log" 2>&1; rc=$?; echo $rc > "$O/$id.rc"; echo "$id rc=$rc"; }
for g in "$@"; do
  case $g in
    diffcheck) run diffcheck "git diff --check cc204c6fd2349b543d73f15c97162a2c4434c86e HEAD" ;;
    mergebase) run mergebase "git merge-base --all HEAD cc204c6fd2349b543d73f15c97162a2c4434c86e" ;;
    invcheck) run inventory_check "python3 scripts/docs_inventory.py --check" ;;
    invself) run inventory_selftest "python3 scripts/docs_inventory.py --selftest" ;;
    suite) run test_suite_cancellation "python3 scripts/test_suite_cancellation.py" ;;
    mutants) run mutants "python3 scripts/test_suite_cancellation.py --mutants --jobs 4" ;;
    lifecycle) run lifecycle "make --no-print-directory -C tb/verilator/gptp_shadow lifecycle" ;;
    behave) PATH=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin:$PATH run behave "cd tests && behave --no-capture -f plain" ;;
  esac
done
git status --short --ignored > "$O/tree-after.txt"

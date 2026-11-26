#!/bin/sh
# bg.sh NAME CMD...: run CMD detached from $CLONE; its log and exit code in $PKT/scratch/runs/NAME.{log,rc}.
# Needs CLONE and PKT set (env.sh). The R941-1 runs, each from the clone at the exact head:
#   store      $LPY -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
#   hst        $LPY -B tb/verilator/ctrl_service_budget/run.py --self-test
#   stst       $LPY -B tb/verilator/nvm_split_target/run.py --self-test
#   st-<pt>    $LPY -B tb/verilator/nvm_split_target/run.py --point <1x1|8x8> --build-dir $PKT/scratch/target-<pt> --jobs 3
#   sb-<pt>    $LPY -B tb/verilator/ctrl_service_budget/run.py --point <1x1|8x8-1if> --build-dir $PKT/scratch/budget-<pt>
#              --groups save-bind,save-bind-burst,save-bind-in-{capture,seal,erase,erase-late,blank,blank-late,
#              program,program-late,verify,verify-late} --jobs 4
#   xc-<pt>    the same build, --reuse-build --out $PKT/scratch/budget-<pt>/xcheck
#              --groups save,save-flight,save-burst,backlog-owed --jobs 4 --record-budget-findings
#   cov        $LPY -B sw/firmware/gtest/fw_coverage.py --check --lwsrp $CLONE/third_party/lwSRP --jobs 4
#   plat       $LPY -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $PKT/scratch/plat
. "$(dirname "$0")/env.sh"
n=$1; shift
mkdir -p "$PKT/scratch/runs"
rm -f "$PKT/scratch/runs/$n.rc"
nohup sh -c 'cd "$CLONE" && echo "== $0 HEAD $(git rev-parse HEAD) dirty $(git status --porcelain --untracked-files=no | wc -l) start $(date +%T)"; "$@"; r=$?; echo "== $0 END rc=$r $(date +%T)"; echo $r > "$PKT/scratch/runs/$0.rc"' "$n" "$@" > "$PKT/scratch/runs/$n.log" 2>&1 < /dev/null &

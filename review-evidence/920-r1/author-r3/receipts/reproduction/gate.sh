#!/bin/bash
set -u
root=<scratch>
kind=$1
head=81c9a1a0c84bbb1da633db641d623d253dcb092a
export TMPDIR=$root/tmp PYTHONUNBUFFERED=1 PYTHONHASHSEED=0 MAKEFLAGS=-j16
export PATH=<home>/litex-milan/venv/bin:<home>/br-milan-rv32/host/bin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
export WF_VENV=<other-scratch>/gates/venv/bin
exec > "$root/logs/$kind.log" 2>&1
run_gate() {
  if [ "$kind" = docs ]; then
    for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do
      /usr/bin/python3 "$root/scripts/run_wf.py" docs.yml "$head" "$job" "$root/docs" || return $?
    done
    /usr/bin/python3 "$root/scripts/verify_wf.py" "$head" "$root/docs" docs.yml > "$root/logs/docs-verify.md"
    return $?
  fi
  /usr/bin/python3 "$root/scripts/clone.py" "$head" "$root/$kind-clone" || return $?
  cd "$root/$kind-clone" || return 2
  case $kind in
    store) /usr/bin/python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8 ;;
    coverage) /usr/bin/python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8 ;;
    images)
      export B1=<lane-scratch>/build/r2-1x1
      export B8=<lane-scratch>/build/r2-8x8-1if
      /usr/bin/python3 "$root/scripts/clone.py" bd252db1d73511307c0ecb78470f0d15d0c3ea9b "$root/baseline-clone" || return $?
      bash <lane-scratch>/scripts/qimg.sh "$root/baseline-clone" "$root/baseline-images" || return $?
      bash <lane-scratch>/scripts/qimg.sh "$PWD" "$root/images" || return $?
      /usr/bin/python3 "$root/scripts/compare-images.py" || return $?
      /usr/bin/python3 tb/verilator/ctrl_service_budget/load_grade.py --check > "$root/logs/load-grade.log"
      ;;
  esac
  rc=$?
  git status --porcelain --untracked-files=all
  return "$rc"
}
run_gate
rc=$?
printf '%s\n' "$rc" > "$root/logs/$kind.rc"
echo "FINAL rc=$rc"
exit "$rc"

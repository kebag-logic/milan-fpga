#!/usr/bin/env bash
# wf_all.sh <head> <base> <root> <group>: every job a pull_request to dev runs in <group>'s workflow(s), each on its
# own fresh clone (run_wf.py), one after another; each runner's output to <root>/runner/<job>.log, its exit status to
# <root>/runner/<job>.rc. Every job runs whatever the previous one returned. Nothing is piped.
set -u
H=$1; B=$2; R=$3; GROUP=$4
here=$(cd "$(dirname "$0")" && pwd)
PY=<scratch>/venv-ci/bin/python3
mkdir -p "$R/runner"
run_job() { # workflow job [k=v ...]
  local wf=$1 job=$2; shift 2
  local tag="${wf}__${job}"; for kv in "$@"; do tag="${tag}__${kv/=/}"; done
  echo "== START $tag $(date -Iseconds)" >> "$R/runner/progress.txt"
  "$PY" "$here/run_wf.py" "$wf" "$job" "$H" "$B" "$R" "$@" > "$R/runner/$tag.log" 2>&1
  echo $? > "$R/runner/$tag.rc"
  echo "== DONE $tag rc=$(cat "$R/runner/$tag.rc") $(date -Iseconds)" >> "$R/runner/progress.txt"
}
case $GROUP in
  fast-a)
    for job in changes verilator-lint bdd-conformance yosys-elaboration publication-census rtl-fast; do run_job rtl-fast $job; done ;;
  fast-yosys)
    # the one rtl-fast job that reads syn/ooc/pp_resource_baseline.json (its resource gate selftest, mutants and
    # check-baseline), re-run after a change to that file's notes
    run_job rtl-fast yosys-elaboration ;;
  fast-fw1)
    for job in firmware-unit firmware-boundary firmware-verilator; do run_job rtl-fast $job; done ;;
  fast-fw2)
    for job in firmware-control-mutants; do run_job rtl-fast $job; done ;;
  fast-fw3)
    for job in firmware-aecp-mutants firmware-srp-mutants; do run_job rtl-fast $job; done ;;
  rtl)
    run_job rtl full-ci-gate
    for k in 0 1 2 3; do run_job rtl yosys-shards shard=$k total=4; done
    run_job rtl yosys-portability ;;
  rtl-yosys-redo)
    for k in 0 1 2; do run_job rtl yosys-shards shard=$k total=4; done
    run_job rtl yosys-portability ;;
  builder-litex)
    # the same, with the LiteX interpreter, so the builder's LiteX-chain gates run instead of reporting NOT RUN
    W="$R/work/builder-litex/wt"
    mkdir -p "$(dirname "$W")" "$R/logs"
    bash <scratch>/scripts/make_clone.sh "$W" "$H" > "$R/logs/builder-litex__clone.log" 2>&1
    ( cd "$W" && source <scratch>/scripts/env.sh && export HOME=<scratch>/home-ci \
        MILAN_RV32_CC=<scratch>/home-ci/br-milan-rv32/host/bin/riscv32-linux-gcc \
        MILAN_LITEX_PYTHON=<litex>/venv/bin/python3 PATH=<scratch>/venv-ci/bin:$PATH && \
      echo "# head $H: MILAN_LITEX_PYTHON=<litex>/bin/python3 python3 sw/builder/test_builder.py --require-rv32" && \
      python3 sw/builder/test_builder.py --require-rv32 ) > "$R/logs/builder-litex__test_builder.log" 2>&1
    echo $? > "$R/logs/builder-litex__test_builder.rc"
    git -C "$W" status --porcelain > "$R/logs/builder-litex__tree-after.txt" ;;
  rtl-gate)
    run_job rtl full-ci-gate ;;
  docs)
    for job in wire-accountability docs-check-no-git docs-gates-0 docs-gates-1 docs-gates-2; do run_job docs $job; done ;;
  elab)
    for k in 0 1 2 3 4; do run_job elaborate elaborate-gates-$k; done ;;
  builder)
    # the assignment's named gate in one invocation, on its own fresh clone of the head (the CI legs run it in two)
    W="$R/work/builder/wt"
    mkdir -p "$(dirname "$W")" "$R/logs"
    bash <scratch>/scripts/make_clone.sh "$W" "$H" > "$R/logs/builder__clone.log" 2>&1
    ( cd "$W" && source <scratch>/scripts/env.sh && export HOME=<scratch>/home-ci \
        MILAN_RV32_CC=<scratch>/home-ci/br-milan-rv32/host/bin/riscv32-linux-gcc \
        PATH=<scratch>/venv-ci/bin:$PATH && \
      echo "# head $H: python3 sw/builder/test_builder.py --require-rv32" && \
      python3 sw/builder/test_builder.py --require-rv32 ) > "$R/logs/builder__test_builder.log" 2>&1
    echo $? > "$R/logs/builder__test_builder.rc"
    git -C "$W" status --porcelain > "$R/logs/builder__tree-after.txt" ;;
esac
echo "GROUP $GROUP DONE $(date -Iseconds)" >> "$R/runner/progress.txt"
echo done > "$R/runner/$GROUP.DONE"

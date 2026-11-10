#!/usr/bin/env bash
# gates.sh <head> <which...>: the standalone gates of [A757] (#867), each group on its own clean clone of <head>
# under gates/<which>, each log gates/<name>.log ending in rc=N. The scratch HOME holds the pinned RV32 SDK,
# installed and verified by scripts/ci_rv32_sdk.py. which: srptx split builder budget diffcheck
set -uo pipefail
H=$1; shift
S=/data-2/milan/tmp/665s7-a757b; G=$S/gates
LITEX=$WORKSPACE_HOME/litex-milan/venv/bin
V=$VALIDATION_TOOLS/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator
export PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
# git's settings as environment (git-config(1) GIT_CONFIG_COUNT): no config file is written
export GIT_CONFIG_COUNT=2 GIT_CONFIG_KEY_0=protocol.file.allow GIT_CONFIG_VALUE_0=always \
  GIT_CONFIG_KEY_1=safe.directory GIT_CONFIG_VALUE_1='*'
mkdir -p "$G" "$TMPDIR"
fresh() { rm -rf "$G/$1"; bash $S/bin/clone.sh "$G/$1" "$2" > "$G/$1-clone.log" 2>&1; }
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }
for which in "$@"; do
  case $which in
    srptx)
      fresh srptx "$H"; D=$G/srptx
      gate make-twin "$D" make -C tb/verilator/milan_dp -j8 twin
      gate make-twin-plants "$D" make -C tb/verilator/milan_dp -j8 twin-plants
      gate make-srptx "$D" make -C tb/verilator/milan_dp -j8 srptx
      gate make-srptx-plants "$D" make -C tb/verilator/milan_dp -j8 srptx-plants
      gate make-srptx-mutants "$D" make -C tb/verilator/milan_dp -j8 srptx-mutants
      ;;
    split)
      fresh split "$H"; D=$G/split
      gate make-split "$D" make -C tb/verilator/milan_dp -j8 split
      gate make-split-mutants "$D" make -C tb/verilator/milan_dp -j8 split-mutants
      gate make-split-cdc "$D" make -C tb/verilator/milan_dp split-cdc
      gate split-parallel "$D" python3 tb/verilator/milan_dp/split_parallel.py --selftest
      ;;
    builder)
      fresh builder "$H"
      PATH=$LITEX:$PATH gate test-builder "$G/builder" python3 sw/builder/test_builder.py --require-rv32
      ;;
    budget)
      fresh budget "$H"; D=$G/budget
      PATH=$LITEX:$PATH gate budget-selftest "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
      PATH=$LITEX:$PATH gate budget-1x1 "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $S/tmp/budget-1x1 --record-budget-findings
      PATH=$LITEX:$PATH gate budget-8x8 "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/tmp/budget-8x8 --record-budget-findings
      ;;
    diffcheck)
      fresh diffcheck "$H"
      gate diff-check "$G/diffcheck" git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 "$H"
      ;;
  esac
done
echo "$(date +%T) gates.sh done: $*"

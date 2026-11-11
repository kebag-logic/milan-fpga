#!/usr/bin/env bash
# gates.sh <head> <which...>: the standalone gates of [A760] (#870), each group on its own clean clone of <head>
# under gates/<which>, each log gates/<name>.log ending in rc=N. which: builder budget diffcheck boot memory identity
set -uo pipefail
H=$1; shift
S=<scratch>; G=$S/gates
LITEX=<home>/litex-milan/venv/bin
V=<tools>/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
export GIT_ALLOW_PROTOCOL=file:https
# the pinned RV32 SDK, installed and verified by scripts/ci_rv32_sdk.py under the scratch HOME
SDK=$HOME/br-milan-rv32/host/bin
mkdir -p "$G" "$TMPDIR" "$HOME"
fresh() { rm -rf "$G/$1"; bash $S/tools/clone.sh "$G/$1" "$2" > "$G/$1-clone.log" 2>&1; }
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }
for which in "$@"; do
  case $which in
    builder)
      fresh builder "$H"
      PATH=$LITEX:$SDK:$PATH gate test-builder "$G/builder" python3 sw/builder/test_builder.py --require-rv32
      ;;
    budget)
      fresh budget "$H"; D=$G/budget
      PATH=$LITEX:$PATH:$SDK gate budget-selftest "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
      PATH=$LITEX:$PATH:$SDK gate budget-1x1 "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $S/tmp/budget-1x1 --record-budget-findings
      PATH=$LITEX:$PATH:$SDK gate budget-8x8 "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/tmp/budget-8x8 --record-budget-findings
      ;;
    boot)
      fresh boot "$H"; D=$G/boot
      PATH=$LITEX:$PATH:$SDK gate split-boot-1x1 "$D" python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/tmp/boot-1x1
      PATH=$LITEX:$PATH:$SDK gate split-boot-8x8 "$D" python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/tmp/boot-8x8 --shape endstation_ax7101_8x8
      ;;
    memory)
      fresh memory "$H"; D=$G/memory
      PATH=$LITEX:$SDK:$PATH gate test-ctrl-memory "$D" python3 -B sw/litex/test_ctrl_memory.py
      ;;
    endpoint)
      # the all-fabric exports of both AX7101 shapes at the gate's flow, against the base's (endpoint-flow/base-*)
      fresh endpoint "$H"
      # each shape's own flow flags (sw/litex/build.sh cfg_ax7101 and cfg_ax8x8), as the base exports used
      for stem in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
        rm -rf "$G/endpoint-$stem"
        place=ExtraPostPlacementOpt; [ $stem = endstation_ax7101_8x8 ] && place=AltSpreadLogic_high
        PATH=$LITEX:$PATH FLOW="--synth-directive AreaOptimized_high --opt-directive ExploreArea --place-directive $place --vivado-max-threads 32" \
          gate endpoint-export-$stem "$G/endpoint" bash $S/tools/endpoint_export.sh "$G/endpoint" $stem "$G/endpoint-$stem"
        gate endpoint-compare-$stem "$G/endpoint" python3 $S/tools/endpoint_compare.py $S/base $S/endpoint-flow/base-$stem "$G/endpoint" "$G/endpoint-$stem"
      done
      ;;
    diffcheck)
      fresh diffcheck "$H"
      gate diff-check "$G/diffcheck" git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 "$H"
      ;;
  esac
done
echo "$(date +%T) gates.sh done: $*"

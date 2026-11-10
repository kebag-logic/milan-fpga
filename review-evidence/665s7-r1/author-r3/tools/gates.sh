#!/usr/bin/env bash
# gates.sh <head> <which...>: the standalone gates of [A757] (#867) round 3, each group on its own clean clone of
# <head> under gates/<which>, each log gates/<name>.log ending in rc=N. The scratch HOME gets the pinned RV32 SDK,
# installed from the pinned archive and verified by scripts/ci_rv32_sdk.py (sdk). which: sdk builder budget split
# diffcheck
set -uo pipefail
H=$1; shift
S=/data-2/milan/tmp/665s7-a757c; G=$S/gates; T=$MANAGEMENT/2026-09-23/665s7-a757c/tools
LITEX=$WORKSPACE_HOME/litex-milan/venv/bin
V=$VALIDATION_TOOLS/pinned-verilator-5.050
BASE=1d6bf5556ae28764361d85012b86394eb467d294
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator MAKEFLAGS=-j16
export PATH=$V:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
# git's settings as environment, no config file written, no GIT_CONFIG_* (a suite guard refuses those)
export GIT_ALLOW_PROTOCOL=file:https GIT_AUTHOR_NAME=gate GIT_AUTHOR_EMAIL=gate@invalid GIT_COMMITTER_NAME=gate \
  GIT_COMMITTER_EMAIL=gate@invalid
mkdir -p "$G" "$TMPDIR" "$HOME"
fresh() { rm -rf "$G/$1"; bash $T/clone.sh "$G/$1" "$2" > "$G/$1-clone.log" 2>&1; }
gate() { local name=$1 dir=$2; shift 2; (cd "$dir" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")"; }
for which in "$@"; do
  case $which in
    sdk)
      fresh sdk "$H"
      rm -rf "$HOME/br-milan-rv32"
      gate rv32-sdk "$G/sdk" python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host" \
        --archive $VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1.tar.xz
      gate rv32-sdk-verify "$G/sdk" python3 scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host" --verify-only
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
      gate budget-clean "$D" git status --porcelain --ignored=no
      ;;
    budget8x8)
      # after the host restart killed budget-8x8 mid-run: 8x8 alone, on its own fresh clone
      fresh budget8x8 "$H"; D=$G/budget8x8
      rm -rf $S/tmp/budget-8x8
      PATH=$LITEX:$PATH gate budget-8x8 "$D" python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $S/tmp/budget-8x8 --record-budget-findings
      gate budget8x8-clean "$D" git status --porcelain --ignored=no
      ;;
    split)
      fresh split "$H"; D=$G/split
      gate make-split "$D" make --no-print-directory -C tb/verilator/milan_dp split
      gate make-split-mutants "$D" make --no-print-directory -C tb/verilator/milan_dp split-mutants
      gate make-split-cdc "$D" make --no-print-directory -C tb/verilator/milan_dp split-cdc
      gate split-parallel "$D" python3 tb/verilator/milan_dp/split_parallel.py --selftest
      gate split-clean "$D" git status --porcelain --ignored=no
      ;;
    diffcheck)
      fresh diffcheck "$H"
      gate diff-check "$G/diffcheck" git diff --check $BASE "$H"
      gate diff-check-r2 "$G/diffcheck" git diff --check 2131eff48066da1e3bbeb6b417ea0655fa7c7741 "$H"
      ;;
  esac
done
echo "$(date +%T) gates.sh done: $*"

#!/usr/bin/env bash
# budget-points.sh: S2's harness (tb/verilator/ctrl_service_budget/run.py) at 1x1 (one interface) and 8x8 (two),
# on the clean clone gates/budget of the head whose --self-test passed there (rc 0, 16:06:31); each log ends rc=N
set -uo pipefail
S=<scratch>; G=$S/gates; D=$G/budget
LITEX=<home>/litex-milan/venv/bin; V=<tools>/pinned-verilator-5.050
export HOME=$S/home TMPDIR=$S/tmp VERILATOR=$V/verilator PYTHONHASHSEED=0
export PATH=$V:<tools>/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c GIT_ALLOW_PROTOCOL=file:https
SDK=$HOME/br-milan-rv32/host/bin
test "$(git -C $D rev-parse HEAD)" = ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa || exit 3
test -z "$(git -C $D status --porcelain --untracked-files=no)" || exit 4
gate() { local name=$1; shift; (cd "$D" && "$@") > "$G/$name.log" 2>&1; echo "rc=$?" >> "$G/$name.log"; echo "$(date +%T) $name $(tail -n 1 "$G/$name.log")" >> $S/gates-run.log; }
for p in 1x1 8x8; do
  rm -rf $S/tmp/budget-$p
  PATH=$LITEX:$PATH:$SDK gate budget-$p python3 -B tb/verilator/ctrl_service_budget/run.py --point $p --build-dir $S/tmp/budget-$p --record-budget-findings --jobs 8
done

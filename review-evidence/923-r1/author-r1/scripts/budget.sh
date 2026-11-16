#!/usr/bin/env bash
# budget.sh <clone> <point> <build-dir> <jobs> [run.py args...]: the CPU budget harness at one point on a clone, the
# S2 recipe's environment; rc and elapsed at the end of its output.
set -u
C=$1; P=$2; D=$3; J=$4; shift 4
T=/data-2/milan/tmp/923-a789
. $T/env.sh
export HOME=$T/home TMPDIR=$T/tmp/budget-$P-$(basename "$D") MAKEFLAGS="-j$J --no-print-directory"
mkdir -p "$TMPDIR" "$HOME"
[ -e "$HOME/br-milan-rv32" ] || ln -s $WORKSPACE_HOME/br-milan-rv32 "$HOME/br-milan-rv32"
cd "$C" || exit 3
echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=all | wc -l) point $P jobs $J args $* start $(date +%T)"
start=$(date +%s)
python3 -B tb/verilator/ctrl_service_budget/run.py --point "$P" --build-dir "$D" --jobs "$J" --record-budget-findings --record-share-findings "$@"
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc end $(date +%T) DIRTY-after $(git status --porcelain --untracked-files=all | wc -l)"
exit $rc

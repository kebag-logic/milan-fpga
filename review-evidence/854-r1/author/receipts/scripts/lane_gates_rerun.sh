#!/usr/bin/env bash
# lane_gates_rerun.sh <head> <gate>...: re-run named gates of lane_gates.sh after an environment fix
# (run 1 kept as <gate>-run1.*). test_builder: the pinned SDK at $HOME/br-milan-rv32/host, as CI provisions it.
# behave: PyYAML beside behave, as the hosted runner's Python carries it.
set -u
H=$1; shift; S=$VALIDATION_STORAGE/scratch/854-a756; W=$S/gclone; G=$S/gates/lane
here=$(cd "$(dirname "$0")" && pwd)
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
source "$here/env.sh"
export MAKEFLAGS="-j8 --no-print-directory" CI_CAMPAIGN_JOBS=8 HOME=$S/home-gates
BASEP=$PATH
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
for g in "$@"; do
  case $g in
    test_builder) P=$BASEP; run test_builder "python3 sw/builder/test_builder.py --require-rv32" ;;
    behave) P=$S/venv-behave/bin:$BASEP; run behave "cd tests && behave --no-capture -f plain" ;;
  esac
done
git status --short --ignored > "$G/tree-after-rerun.txt"
echo done > "$G/RERUN-DONE"

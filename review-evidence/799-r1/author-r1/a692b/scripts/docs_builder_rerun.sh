#!/usr/bin/env bash
# #799: re-run the docs workflow's two end-station builder legs, and leg 1 again with the LiteX interpreter, at <rev>
# in the same docs clone, with $HOME holding a fresh `scripts/ci_rv32_sdk.py --archive` install of the pinned RV32
# SDK, verified (the first run's $HOME held a relocated copy of an earlier install).
# usage: docs_builder_rerun.sh <rev>
set -u
rev=$1; h=${rev:0:8}; R7=$(cd "$(dirname "$0")" && pwd); B=$VALIDATION_STORAGE/scratch/799-a692b/docs; C=$B/clone-docs-$h; O=$B/docs-$h
PY=$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3
for g in gate_25_0 gate_25_1; do
  DOCS_ONLY=$g $PY "$R7/docs_steps.py" "$O/rerun-$g" "$C" > "$O/rerun-$g.out" 2>&1; echo $? > "$O/rerun-$g.rc"
done
DOCS_ONLY=gate_25_1 DOCS_EXTRA_ENV="MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3" \
  $PY "$R7/docs_steps.py" "$O/rerun-leg1-litex" "$C" > "$O/rerun-leg1-litex.out" 2>&1; echo $? > "$O/rerun-leg1-litex.rc"
git -C "$C" status --porcelain --untracked-files=no > "$O/rerun-clone-status-after.txt"
echo DOCS-BUILDER-RERUN-DONE > "$O/rerun-done"

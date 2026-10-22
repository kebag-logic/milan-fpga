#!/usr/bin/env bash
# docs_replica.sh OUTDIR: the docs workflow's gate step bodies, literally, at the
# committed head (docs_steps.py from round 1b, unchanged), then builder leg 1
# again with the LiteX interpreter, as round 1b did.
set -u
out="$1"; mkdir -p "$out"
cd $VALIDATION_STORAGE/771-a662-r2 || exit 2
python3 $VALIDATION_STORAGE/scratch/a662/docs_steps.py "$out/all" > "$out/all.out" 2>&1
echo $? > "$out/all.rc"
DOCS_ONLY=gate_25_1 DOCS_EXTRA_ENV="MILAN_LITEX_PYTHON=$WORKSPACE_HOME/litex-milan/venv/bin/python3" \
    python3 $VALIDATION_STORAGE/scratch/a662/docs_steps.py "$out/leg1-litex" > "$out/leg1-litex.out" 2>&1
echo $? > "$out/leg1-litex.rc"
date -Is > "$out/done"

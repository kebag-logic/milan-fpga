#!/usr/bin/env bash
# Run the PR's own mutation campaign from the head scratch copy with the pinned tool.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); export PATH=$PK/tools:$PATH
export TMPDIR=$PK/scratch/tmp; mkdir -p $TMPDIR
python3 $PK/scratch/head/tb/pp_top/name_wr_mutant.py --output $PK/receipts/04-shipped-mutation
echo "campaign rc=$?"

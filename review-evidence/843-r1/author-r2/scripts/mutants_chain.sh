#!/usr/bin/env bash
# mutants_chain.sh <sha>: round 1's planted mutants (mutants.py, unchanged checks and anchors) on a clean clone of <sha>.
set -u
H=$1; S=$VALIDATION_STORAGE/scratch/843-a737b; C=$S/clone-mutants-${H:0:8}; here=$(cd "$(dirname "$0")" && pwd)
export TMPDIR=$S/tmp-mutants HOME=$HOME TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c PYTHONHASHSEED=0
mkdir -p "$TMPDIR"
bash "$here/make_clone.sh" "$C" "$H" || exit 2
python3 -I "$here/mutants.py" "$C" "$S/mutants-${H:0:8}"
echo "mutants rc=$?"
git -C "$C" status --porcelain

#!/usr/bin/env bash
set -euo pipefail
src=${1:?source clone}
packet=${2:?packet directory}
work="$packet/scratch/docs-tree"
mkdir -p "$packet/receipts" "$packet/scratch/tmp"
export TMPDIR="$packet/scratch/tmp"
git clone --shared --no-checkout "$src" "$work"
git -C "$work" checkout --detach 66d1b501f4879402fe76485095aef7c6e07c32af
python3 -m venv "$packet/scratch/docs-venv"
"$packet/scratch/docs-venv/bin/python" -m pip install wavedrom
export PATH="$packet/scratch/docs-venv/bin:$PATH"
cd "$work"
set +e
make -j16 check > "$packet/receipts/docs-check.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$packet/receipts/docs-check.rc"
cat "$packet/receipts/docs-check.log"
python3 scripts/gen_matrix.py --check > "$packet/receipts/matrix-check.log" 2>&1
matrix_rc=$?
printf '%s\n' "$matrix_rc" > "$packet/receipts/matrix-check.rc"
cat "$packet/receipts/matrix-check.log"
exit $((rc || matrix_rc))

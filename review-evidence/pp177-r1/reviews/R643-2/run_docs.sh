#!/usr/bin/env bash
set -euo pipefail
# Usage: bash run_docs.sh CHECKOUT PACKET
repo=$(realpath "$1")
packet=$(realpath "$2")
mkdir -p "$packet/scratch/tmp"
python3 -m venv "$packet/scratch/docs-venv"
"$packet/scratch/docs-venv/bin/python" -m pip install 'wavedrom==2.0.3.post3'
export PATH="$packet/scratch/docs-venv/bin:$PATH"
export TMPDIR="$packet/scratch/tmp"
export PYTHONDONTWRITEBYTECODE=1
cd "$repo"
set +e
make -j16 check > "$packet/docs-check.log" 2>&1
rc=$?
printf '%s\n' "$rc" > "$packet/docs-check.rc"
exit "$rc"

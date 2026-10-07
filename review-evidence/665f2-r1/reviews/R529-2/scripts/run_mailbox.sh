#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$1" && pwd)
packet=$(cd "$2" && pwd)
: "${VERILATOR:?Select the verified pinned simulator}"
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$packet/scratch/tmp"
mkdir -p "$packet/scratch/mailbox-tree"
git -C "$repo" archive HEAD --output "$packet/scratch/head.tar"
tar -xf "$packet/scratch/head.tar" -C "$packet/scratch/mailbox-tree"
make -C "$packet/scratch/mailbox-tree/tb/verilator/mbx" -j16 VBUILD_JOBS=4 run-wb run-axil

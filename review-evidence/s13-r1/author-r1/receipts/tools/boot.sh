#!/usr/bin/env bash
# boot.sh <clone> <build-dir> [shape]: the split boot simulation (#665 S3) from a clean clone, to ready.
set -u
L=$1; D=$2; SH=${3:-endstation_ax7101_1x1_tdm8}
source <scratch>/bin/env.sh
cd "$L" || exit 3
echo "# head $(git rev-parse HEAD) status: $(git status --porcelain | tr '\n' ' ')"; date -Iseconds
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir "$D" --shape "$SH"
rc=$?; date -Iseconds; echo "rc=$rc"; exit $rc

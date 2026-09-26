#!/usr/bin/env bash
# Focused NW run at head: build the pp_top bench and run --name-writes-only.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); export PATH=$PK/tools:$PATH
cd $PK/scratch/head/tb/pp_top
make gsi-build > $PK/receipts/03-head-build.log 2>&1; echo "build rc=$?"
./obj_dir/Vpp_top_sim --name-writes-only > $PK/receipts/03-head-name-writes.log 2>&1; echo "run rc=$?"
tail -2 $PK/receipts/03-head-name-writes.log

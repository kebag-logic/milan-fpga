#!/bin/bash
# In a recorded run's own clone, moved to the lane's head: regrade the logs already recorded, on the reused build
# (every input's digest checked). usage: regrade_head.sh CLONE BUILD POINT LOG [run.py options...]
set -u
. $MANAGEMENT/2026-09-23/665s5-a702/scripts/env.sh
C=$1 B=$2 P=$3 L=$4; shift 4
git -C "$C" fetch -q $LANES/665-s5-hooks 665-s5-hooks && git -C "$C" checkout -q FETCH_HEAD
cd "$C"
{ echo "HEAD $(git rev-parse HEAD)"; echo "\$ python3 -B tb/verilator/ctrl_service_hooks/run.py --point $P $* --build-dir <build> --regrade --record-findings"; } > "$L"
python3 -B tb/verilator/ctrl_service_hooks/run.py --point "$P" "$@" --build-dir "$B" --regrade --record-findings >> "$L" 2>&1
echo "rc=$?" >> "$L"
echo "tree: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s)" >> "$L"

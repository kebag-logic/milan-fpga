#!/bin/bash
# In a recorded run's own clone, moved to the lane's head: rerun named groups on the reused build, then regrade every
# group. usage: rerun_regrade.sh CLONE BUILD POINT GROUPS LOG [run.py options...]
set -u
. $MANAGEMENT/2026-09-23/665s5-a702/scripts/env.sh
C=$1 B=$2 P=$3 G=$4 L=$5; shift 5
git -C "$C" fetch -q $LANES/665-s5-hooks 665-s5-hooks && git -C "$C" checkout -q FETCH_HEAD
cd "$C"
{ echo "HEAD $(git rev-parse HEAD)"; echo "\$ python3 -B tb/verilator/ctrl_service_hooks/run.py --point $P $* --build-dir <build> --reuse-build --groups $G --record-findings"; } > "$L"
python3 -B tb/verilator/ctrl_service_hooks/run.py --point "$P" "$@" --build-dir "$B" --reuse-build --groups "$G" --record-findings --jobs 2 >> "$L" 2>&1
echo "rerun rc=$?" >> "$L"
echo "\$ python3 -B tb/verilator/ctrl_service_hooks/run.py --point $P $* --build-dir <build> --regrade --record-findings" >> "$L"
python3 -B tb/verilator/ctrl_service_hooks/run.py --point "$P" "$@" --build-dir "$B" --regrade --record-findings >> "$L" 2>&1
echo "regrade rc=$?" >> "$L"
echo "tree: $(git status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s)" >> "$L"

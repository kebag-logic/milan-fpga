#!/bin/bash
# The final gate pass at a head, once: the sweep as four native-shards units (shard 2, capture_coherence, on four
# CPUs), and the queue of every workflow job and the lane's gates and the harness's head regrade for the dispatcher.
# usage: final30.sh HEAD SHARD0 SHARD1 SHARD2 SHARD3
set -u
H=$1; shift
T=/data-2/milan/tmp/665s2b-a683zo
G=$T/gates-run
mkdir -p $G $T/logs $T/gates-out
SRC=$G/src-sweep
[ -d $SRC ] || bash $T/scripts/clone.sh $SRC $H > $T/logs/final-src.log 2>&1
test "$(git -C $SRC rev-parse HEAD)" = "$H" || { echo "sweep source not at $H"; exit 4; }
test -z "$(git -C $SRC status --porcelain --untracked-files=all)" || { echo "sweep source dirty"; exit 4; }
mkdir -p $G/tmp-sweep
cat > $T/665s2b-a683zo-sweep-spec.json <<SPEC
{"cwd": "$SRC", "head": "$H", "base": "0fb66211b7", "commands": [["env", "PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin", "VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator", "TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c", "TMPDIR=$G/tmp-sweep", "MAKEFLAGS=-j4 --no-print-directory", "bash", "scripts/run_all_suites.sh", "$G/sweep/logs", "--wait"]]}
SPEC
python3 $MANAGEMENT/2026-09-23/native-shards.py 665s2b-a683zo $T/665s2b-a683zo-sweep-spec.json $G/sweep 4 "$@" > $T/logs/final-sweep-launch.log 2>&1
echo "sweep launch rc=$? $(date +%T)" >> $T/logs/final-sweep-launch.log

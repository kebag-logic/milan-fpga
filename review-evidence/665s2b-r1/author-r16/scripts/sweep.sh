#!/bin/bash
# The full sweep at a head as four native-shards units (one clone and unit each, MemoryMax 10G, -j4), the shard that
# holds capture_coherence (2/4) on four CPUs as every shard is. usage: sweep.sh HEAD OUT CPUS-0 CPUS-1 CPUS-2 CPUS-3
set -u
H=$1 OUT=$2; shift 2
T=$VALIDATION_STORAGE/665s2b-a683u
SPEC=$T/sweep-spec-${H:0:8}.json
cat > "$SPEC" <<JSON
{
 "cwd": "$LANES/665-s2b-cycles",
 "head": "$H",
 "base": "a68536fa",
 "commands": [
  ["env", "PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
   "VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator",
   "TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c",
   "TMPDIR=$T/tmp-sweep", "MAKEFLAGS=-j4 --no-print-directory",
   "bash", "scripts/run_all_suites.sh", "$OUT/logs", "--wait"]
 ]
}
JSON
mkdir -p "$T/tmp-sweep"
python3 $MANAGEMENT/2026-09-23/native-shards.py 665s2b-r "$SPEC" "$OUT" 4 "$@"

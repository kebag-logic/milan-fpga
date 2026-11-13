#!/bin/bash
# The final sweep, each of its four shards started as soon as a CPU range is free and MemAvailable is above 20 GB
# (native-shard-one.py, native-shards.py's steps for one shard): shard 2, whose capture_coherence builds one datapath a
# CPU, on the first four CPUs of its range, the others on a whole 8-CPU range. The source clone and spec as final30.sh
# makes them. Checks every 20 s; a line per launch. usage: launch_sweep34b.sh HEAD
set -u
H=$1 T=/data-2/milan/tmp/665s2b-a683zo L=$T/logs/launch-sweep34.txt G=$T/gates-run
mkdir -p $G $T/gates-out
SRC=$G/src-sweep
[ -d $SRC ] || bash $T/scripts/clone.sh $SRC $H > $T/logs/final-src.log 2>&1
test "$(git -C $SRC rev-parse HEAD)" = "$H" || { echo "sweep source not at $H" >> $L; exit 4; }
test -z "$(git -C $SRC status --porcelain --untracked-files=all)" || { echo "sweep source dirty" >> $L; exit 4; }
mkdir -p $G/tmp-sweep
SPEC=$T/665s2b-a683zo-sweep-spec.json
python3 - "$SRC" "$H" "$G" "$SPEC" <<'PY'
import json, sys
src, head, g, spec = sys.argv[1:5]
env = ['env', 'PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
       'VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',
       'TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c', f'TMPDIR={g}/tmp-sweep',
       'MAKEFLAGS=-j4 --no-print-directory']
open(spec, 'w').write(json.dumps({'cwd': src, 'head': head, 'base': '0fb66211b7',
                                  'commands': [env + ['bash', 'scripts/run_all_suites.sh', f'{g}/sweep/logs', '--wait']]}) + '\n')
PY
for k in 2 0 1 3; do
    while true; do
        free=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick 2>/dev/null)
        mem=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
        if [ -n "$free" ] && [ "$mem" -gt 20 ]; then
            lo=${free%-*}
            if [ $k = 2 ]; then cpus="$lo-$((lo + 3))"; else cpus=$free; fi
            echo "$(date +%T) shard $k on $cpus (MemAvailable $mem GB)" >> $L
            python3 $T/scripts/native-shard-one.py 665s2b-a683zo $SPEC $G/sweep 4 $k $cpus >> $L 2>&1
            echo "$(date +%T) shard $k launch rc=$?" >> $L
            sleep 30
            break
        fi
        sleep 20
    done
done
echo "$(date +%T) every shard launched" >> $L

#!/bin/bash
# The final pass's full Verilator sweep (round 2's launch_sweep2.sh without its pool fallback): each of the four shards
# is started on its own CPU range, the one cpu_ranges.py picks at that moment (checked before each launch), once
# MemAvailable is above 30 GB; a shard waits for a range, never the session pool (round 3's assignment). Shard 2
# (capture_coherence, one datapath a CPU) runs on the first four CPUs of its booked range. The source is a clean clone
# at the head (native-shard-one.py: native-shards.py's steps for one shard). Checks every 20 s; a line per launch.
# usage: launch_sweep3.sh HEAD [SHARD...]  (default 2 0 1 3)
set -u
H=$1; shift; SHARDS=${*:-2 0 1 3}; T=/data-2/milan/tmp/897-a776 G=/data-2/milan/tmp/897-a776/r3
L=$G/logs/launch-sweep-${H:0:8}.txt
mkdir -p $G/logs
SRC=$G/sweep-src-${H:0:8}
[ -d $SRC ] || bash $T/scripts/clone.sh $SRC $H > $G/logs/sweep-src.log 2>&1
test "$(git -C $SRC rev-parse HEAD)" = "$H" || { echo "sweep source not at $H" >> $L; exit 4; }
test -z "$(git -C $SRC status --porcelain --untracked-files=all)" || { echo "sweep source dirty" >> $L; exit 4; }
mkdir -p $G/tmp-sweep
SPEC=$G/sweep-spec-${H:0:8}.json
python3 - "$SRC" "$H" "$G" "$SPEC" <<'PY'
import json, sys
src, head, g, spec = sys.argv[1:5]
env = ['env', 'PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin',
       'VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator',
       'TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c', f'TMPDIR={g}/tmp-sweep',
       'MAKEFLAGS=-j4 --no-print-directory']
open(spec, 'w').write(json.dumps({'cwd': src, 'head': head, 'base': '5b264bf264',
                                  'commands': [env + ['bash', 'scripts/run_all_suites.sh', f'{g}/sweep-{head[:8]}/logs', '--wait']]}) + '\n')
PY
for k in $SHARDS; do
    while true; do
        # one pick at a time across this lane's launchers (the dispatcher's too), held until the shard is visible
        exec 9>>$G/pick.lock; flock 9
        free=$(python3 $MANAGEMENT/2026-09-23/cpu_ranges.py pick 2>/dev/null)
        mem=$(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo)
        if [ -z "$free" ] || [ "$mem" -le 30 ]; then flock -u 9; fi
        if [ -n "$free" ] && [ "$mem" -gt 30 ]; then
            lo=${free%-*}
            if [ $k = 2 ]; then cpus="$lo-$((lo + 3))"; else cpus=$free; fi
            echo "$(date +%T) shard $k on $cpus, booked $free (MemAvailable $mem GB)" >> $L
            python3 $T/scripts/r3/native-shard-one.py 897-a776-r3 $SPEC $G/sweep-${H:0:8} 4 $k $cpus >> $L 2>&1
            echo "$(date +%T) shard $k launch rc=$?" >> $L
            sleep 5; flock -u 9
            sleep 25
            break
        fi
        sleep 20
    done
done
echo "$(date +%T) every shard launched" >> $L

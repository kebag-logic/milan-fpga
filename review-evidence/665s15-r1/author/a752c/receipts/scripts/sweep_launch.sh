#!/bin/bash
# The full sweep as four native-shards units on a clean clone of a commit: reserve four booked ranges with placeholder
# units of this lane, release them and hand them to native-shards.py at once; shard 2, which holds capture_coherence,
# gets four CPUs of its range (its mutant driver builds one datapath a CPU). Waits while MemAvailable is under 30 GB,
# and gives up (rc 3, every placeholder released) after TRIES tries a minute apart.
# usage: sweep_launch.sh COMMIT LABEL OUT [TRIES]
set -u
H=$1 LABEL=$2 OUT=$3 TRIES=${4:-8}
T=$SCRATCH
M=$MGMT
C=$T/src-$LABEL
mkdir -p $T/logs
[ -d "$C" ] || bash $T/scripts/clone.sh "$C" "$H" > $T/logs/clone-$LABEL.log 2>&1
test "$(git -C "$C" rev-parse HEAD)" = "$H" || exit 4
test -z "$(git -C "$C" status --porcelain --untracked-files=all)" || exit 5
ranges=()
tries=0
while [ ${#ranges[@]} -lt 4 ]; do
    avail=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    exec 8> "$T/pick.lock"; flock 8
    if [ "$avail" -gt 31457280 ] && r=$(python3 $M/cpu_ranges.py pick); then
        k=${#ranges[@]}
        systemd-run --user --unit="milan-665s15-a752c-hold$k" --collect /usr/bin/taskset -c "$r" /usr/bin/sleep 36000 > /dev/null 2>&1
        ranges+=("$r"); echo "$(date +%T) reserved $r (MemAvailable ${avail} kB)" >> $T/logs/$LABEL.txt; sleep 5; flock -u 8
    else
        flock -u 8
        tries=$((tries + 1))
        if [ "$tries" -ge "$TRIES" ]; then
            for k in 0 1 2 3; do systemctl --user stop "milan-665s15-a752c-hold$k.service" 2>/dev/null; done
            echo "$(date +%T) gave up after $tries tries with ${#ranges[@]} ranges" >> $T/logs/$LABEL.txt
            exit 3
        fi
        sleep 60
    fi
done
first=${ranges[2]%-*}
ranges[2]="$first-$((first + 3))"
cat > $T/$LABEL-spec.json <<JSON
{"cwd": "$C", "head": "$H", "base": "1d6bf5556a",
 "commands": [["env", "PATH=$DATA/tools/pinned-verilator-5.050:$DATA/tools/sv2v-v0.0.12:$DATA/scratch/a662/make43/bin:$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
               "VERILATOR=$DATA/tools/pinned-verilator-5.050/verilator",
               "TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c",
               "TMPDIR=$T/tmp-$LABEL", "MAKEFLAGS=-j4 --no-print-directory",
               "bash", "scripts/run_all_suites.sh", "$OUT/logs", "--wait"]]}
JSON
mkdir -p $T/tmp-$LABEL
for k in 0 1 2 3; do systemctl --user stop "milan-665s15-a752c-hold$k.service"; done
echo "$(date +%T) launching on ${ranges[*]}" >> $T/logs/$LABEL.txt
python3 $M/native-shards.py $LABEL $T/$LABEL-spec.json $OUT 4 "${ranges[@]}" >> $T/logs/$LABEL.txt 2>&1
echo "$(date +%T) native-shards rc=$?" >> $T/logs/$LABEL.txt

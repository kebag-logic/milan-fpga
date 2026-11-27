#!/usr/bin/env bash
# unit5home.sh (HOME=<home>, MemoryMax 12G) <name> <cpus> <cwd> <cmd...>: start <cmd> in its own transient user unit milan-977-a825e-<name> (MemoryMax 10G)
# pinned to <cpus>, without waiting; output to units/<name>.log, status to units/<name>.rc (poll with poll5.sh).
set -u
name=$1; cpus=$2; cwd=$3; shift 3
U=<scratch>/units
envf=<scratch>/bin/env.sh
echo "[unit milan-977-a825e-$name cpus $cpus start $(date +%T)]" > "$U/$name.log"
rm -f "$U/$name.rc"
systemd-run --user --quiet --unit="milan-977-a825e-$name" --collect \
  --property=MemoryMax=12G --working-directory="$cwd" \
  --setenv=HOME=<home> \
  /usr/bin/taskset -c "$cpus" /bin/bash -c ". $envf; \"\$@\" >> $U/$name.log 2>&1; echo \$? > $U/$name.rc; echo \"[unit end \$(date +%T) rc \$(cat $U/$name.rc)]\" >> $U/$name.log" bash "$@"
echo "started milan-977-a825e-$name"

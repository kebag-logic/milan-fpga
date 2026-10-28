#!/bin/bash
# Launch one command as its own systemd user unit on CPUs <cpus> with a memory
# cap, logging to <out>/<name>.log and its exit status to <out>/<name>.rc.
# usage: unit.sh <name> <cpus> <memmax> <cwd> <out> <cmd> [args...]
name=$1 cpus=$2 mem=$3 cwd=$4 out=$5; shift 5
mkdir -p "$out"
rm -f "$out/$name.rc"
printf '%q ' "$@" > "$out/$name.cmd"; echo >> "$out/$name.cmd"
exec systemd-run --user --unit="milan-gptp90-a688c-$name" --collect \
  --property=MemoryMax="$mem" --working-directory="$cwd" \
  --setenv=HOME=<home> \
  --setenv=PATH=<pinned-verilator>:<pinned-sv2v>:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  --setenv=VERILATOR_ROOT=<pinned-verilator-root>/usr/share/verilator \
  --setenv=TMPDIR=<scratch>/tmp \
  --setenv=PYTHON_CPU_COUNT=8 --setenv=VERILATOR_JOBS=8 --setenv=MAKEFLAGS=-j8 \
  /usr/bin/taskset -c "$cpus" /bin/bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$out/$name" "$@"

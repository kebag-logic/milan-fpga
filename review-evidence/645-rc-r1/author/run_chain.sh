#!/usr/bin/env bash
# usage: run_chain.sh <cpus> <name:dir:target-args> ...   (scratch orchestration, outside the tree)
# Each step: taskset -c <cpus> env -u MAKEFLAGS make -C <dir> <args>, logged with rc and wall seconds.
set -u
ROOT=$LANES/645-bind-recentre
OUT=/tmp/a620/suites
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
cpus=$1; shift
for step in "$@"; do
  name=${step%%:*}; rest=${step#*:}; dir=${rest%%:*}; args=${rest#*:}
  start=$(date +%s.%N)
  ( cd "$ROOT" && env -u MAKEFLAGS taskset -c "$cpus" make -C "$dir" $args ) > "$OUT/$name.log" 2>&1
  rc=$?
  end=$(date +%s.%N)
  echo "$rc" > "$OUT/$name.rc"
  python3 -c "print(f'{$end - $start:.3f}')" > "$OUT/$name.secs"
  echo "$(date +%T) $name rc=$rc secs=$(cat $OUT/$name.secs)" >> "$OUT/chain.log"
done

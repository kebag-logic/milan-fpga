#!/bin/bash
# casecost.sh TREE CPUS SUITE [CASE...]: build every listed case of SUITE in r3/wt/TREE on all of CPUS, then execute each
# case alone, one case per physical core: the first logical CPU of each sibling pair in CPUS (2k, 2k+1 on this host;
# the other sibling stays booked and idle). Per case: user/sys/wall (time) and counters (perf). Untimed builds use the
# host ccache. Output: r3/cost/TREE/{build.log,<case>.time,<case>.perf,<case>.out}
set -u
T=$1; C=$2; S=$3; shift 3
W=/data-2/milan/tmp/cicd-a839/r3/wt/$T
O=/data-2/milan/tmp/cicd-a839/r3/cost/$T
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
export CI_BUILD_JOBS=8 CI_TOOL_BUILD_JOBS=8 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=8 SIM_JOBS=4 MAKEFLAGS='-j1 --no-print-directory'
export OBJCACHE=ccache
mkdir -p "$O"; cd "$W" || exit 99
D=tb/verilator/$S
if [ "$#" -eq 0 ]; then mapfile -t cases < <(python3 -c 'import json,sys; print("\n".join(json.load(sys.stdin)))' \
  < <(python3 scripts/ci_make_cases.py --suite "$S" --list)); else cases=("$@"); fi
make -s -C "$D" ci-prepare > "$O/build.log" 2>&1
for c in "${cases[@]}"; do
  echo "== build $c $(date +%T)" >> "$O/build.log"
  taskset -c "$C" make -s -C "$D" "build-$c" >> "$O/build.log" 2>&1 || echo "BUILD FAILED $c" >> "$O/build.log"
done
echo "== builds done $(date +%T)" >> "$O/build.log"
[ -n "${BUILD_ONLY:-}" ] && exit 0
# one CPU per physical core
mapfile -t cores < <(python3 -c '
import sys
cpus=set()
for p in sys.argv[1].split(","):
    a,_,b=p.partition("-"); cpus|=set(range(int(a),int(b or a)+1))
print("\n".join(str(c) for c in sorted(cpus) if c%2==0 and c+1 in cpus))' "$C")
run1() {  # case cpu
  taskset -c "$2" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$1.time" \
    perf stat -x, -o "$O/$1.perf" -e task-clock,cycles:u,instructions:u -- \
    make -s --no-print-directory -C "$D" "exec-$1" > "$O/$1.out" 2>&1
  echo "rc=$?" >> "$O/$1.time"
}
declare -A pid
for c in "${cases[@]}"; do
  while :; do
    free=""
    for k in "${cores[@]}"; do
      if [ -z "${pid[$k]:-}" ] || ! kill -0 "${pid[$k]}" 2>/dev/null; then free=$k; break; fi
    done
    [ -n "$free" ] && break
    wait -n
  done
  run1 "$c" "$free" &
  pid[$free]=$!
done
wait
echo "== execs done $(date +%T)" >> "$O/build.log"

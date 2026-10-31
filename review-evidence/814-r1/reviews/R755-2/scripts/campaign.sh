#!/usr/bin/env bash
# Reviewer campaign: one job per line of <jobs> ("<name>\t<command>"), up to 16 at once, each with its
# own log and rc file under <out>. Usage: campaign.sh <jobs> <out> <litex-sw-dir>
jobs=$1 out=$2 dir=$3
run_one() {
  name=$1; shift
  ( cd "$dir" && /usr/bin/time -f "TIME maxrss %M kB, %U s user, %e s wall" timeout -k 10 1500 bash -c "$*" ) \
    > "$out/$name.log" 2>&1
  echo $? > "$out/$name.rc"
}
export -f run_one; export out dir
awk -F'\t' '{printf "%s\0%s\0", $1, $2}' "$jobs" | xargs -0 -n2 -P16 bash -c 'run_one "$0" "$1"'
echo done > "$out/ALL.done"

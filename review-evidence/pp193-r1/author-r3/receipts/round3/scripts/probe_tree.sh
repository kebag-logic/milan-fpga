#!/usr/bin/env bash
# usage: probe_tree.sh <out dir> <rtl tree> <probe.py> [patch]: export the
# tree's tracked files (plus its working-tree RTL/tests), insert the probe into
# the copy's stream-FSM suite, plant the optional patch, build and run the
# suite; <out>/log and <out>/rc.
set -u
out=$1; tree=$2; probe=$3; patch=${4:-}
. <scratch>/r3/scripts/env.sh
rm -rf "$out"; mkdir -p "$out/tree"
(cd "$tree" && git ls-files -z | xargs -0 tar -c) | tar -x -C "$out/tree"
[ -n "$patch" ] && (cd "$out/tree" && git apply "$patch" 2>&1 || patch -s -p1 < "$patch")
python3 -I "$probe" "$out/tree/tb/srp_stream_fsms/sim_main.cpp" || { echo 9 > "$out/rc"; exit 9; }
( cd "$out/tree/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/log" 2>&1; echo $? > "$out/rc" )
grep -E "^PROBE|checks:" "$out/log"
echo "rc $(cat "$out/rc")"

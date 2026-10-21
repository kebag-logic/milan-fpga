#!/usr/bin/env bash
# usage: tests_on_rtl.sh <out dir> <tests tree> <rtl tree> [patch]: the tests
# tree's tracked files with the RTL tree's hdl/, the optional patch planted,
# then the stream-FSM suite; <out>/log and <out>/rc.
set -u
out=$1; tt=$2; rt=$3; patch=${4:-}
. <scratch>/r3/scripts/env.sh
rm -rf "$out"; mkdir -p "$out/tree"
(cd "$tt" && git ls-files -z | xargs -0 tar -c) | tar -x -C "$out/tree"
rm -rf "$out/tree/hdl"; (cd "$rt" && git ls-files -z hdl | xargs -0 tar -c) | tar -x -C "$out/tree"
[ -n "$patch" ] && (cd "$out/tree" && git apply "$patch")
( cd "$out/tree/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/log" 2>&1; echo $? > "$out/rc" )
grep -E "^FAIL|checks:" "$out/log"
echo "rc $(cat "$out/rc")"

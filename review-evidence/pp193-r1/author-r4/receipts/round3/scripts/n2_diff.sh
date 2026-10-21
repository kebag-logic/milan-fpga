#!/usr/bin/env bash
# usage: n2_diff.sh <out dir> <dev tree> <pre-S2 listener .sv>: the stream-FSM
# suite built with the wrapper at two streams (-GN_STREAMS_P=2), once with the
# dev listener and once with the pre-S2 listener; the two outputs are diffed.
set -u
out=$1; dev=$2; pre=$3
. <scratch>/r3/scripts/env.sh
rm -rf "$out"; mkdir -p "$out"
for v in s2 pre; do
  mkdir -p "$out/$v"
  (cd "$dev" && git ls-files -z hdl tb/common tb/srp_stream_fsms | xargs -0 tar -c) | tar -x -C "$out/$v"
  [ $v = pre ] && cp "$pre" "$out/$v/hdl/srp/KL_srp_listener_fsm.sv"
  sed -i 's/--top-module $(TOP) \\/--top-module $(TOP) -GN_STREAMS_P=2 \\/' "$out/$v/tb/srp_stream_fsms/Makefile"
done
( cd "$out/s2/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/s2.log" 2>&1; echo $? > "$out/s2.rc" ) &
( cd "$out/pre/tb/srp_stream_fsms" && make RUN_ARGS=suite > "$out/pre.log" 2>&1; echo $? > "$out/pre.rc" ) &
wait
grep -E "^FAIL|^PASS|checks:" "$out/s2.log" > "$out/s2.lines"
grep -E "^FAIL|^PASS|checks:" "$out/pre.log" > "$out/pre.lines"
grep -c "GN_STREAMS_P=2" "$out/s2.log" "$out/pre.log"
diff "$out/pre.lines" "$out/s2.lines" > "$out/diff.txt"; echo "diff rc $?" | tee "$out/diff.rc"
tail -1 "$out/s2.lines"; tail -1 "$out/pre.lines"

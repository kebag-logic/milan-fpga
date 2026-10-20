#!/usr/bin/env bash
# The stream suite alone with listener-csid-ram-ignores-park planted, at the
# round-2 head (the campaign keeps one receipt per label and this arm's label
# is shared with the walk runs). Fresh export, never the lane's working tree.
set -u
. <scratch>/scripts/env.sh
S=<scratch>
HEAD_SHA=$(cat $S/head2.sha)
W=$S/r2rec/csid-ram-suite
rm -rf "$W"; mkdir -p "$W"
git -C <lane> archive "$HEAD_SHA" hdl tb/common tb/srp_stream_fsms tb/srp_top/mutations | tar -x -C "$W"
echo "$HEAD_SHA" > "$W.sha"
cd "$W" && git apply tb/srp_top/mutations/listener-csid-ram-ignores-park.patch > "$W.apply.log" 2>&1
echo $? > "$W.apply.rc"
cd "$W/tb/srp_stream_fsms" || exit 2
make RUN_ARGS=suite VERILATOR="$VERILATOR" > "$W.log" 2>&1; echo $? > "$W.rc"

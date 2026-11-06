#!/bin/sh
# Usage: probes.sh <disposable clone at 6162885> <receipts dir> <verilator>
# M1: listener_is's split q starts at -1 and must still be compared with fp:
#     replace "q == fp" by "q != fp" in listener_is -> AS rows must fail.
# M2: PS12's sink_b must name sink 3: set it to 2 -> PS12 must fail.
# Each probe edits one line, rebuilds, runs, and restores the clone.
C=$1; R=$2; V=$3
cd "$C" || exit 2
sed -i 's/return listener_value(f, sid, e, q) \&\& e == ev \&\& q == fp;/return listener_value(f, sid, e, q) \&\& e == ev \&\& q != fp;/' tb/pp_top/sim_main.cpp
git diff --stat > "$R/probe-M1.diff"; git diff >> "$R/probe-M1.diff"
sed -i 's/^  const int sink_b = 3;/  const int sink_b = 2;/' tb/srp_stream_fsms/sim_main.cpp
git diff -- tb/srp_stream_fsms > "$R/probe-M2.diff"
( cd tb/pp_top && eval "$(make -s -n run VERILATOR=$V 2>/dev/null | grep "^$V --cc" | head -1)" > "$R/probe-M1.build.log" 2>&1 && ./obj_dir/Vpp_top_sim --acmp-only > "$R/probe-M1.log" 2>&1; echo $? > "$R/probe-M1.rc" ) &
( cd tb/srp_stream_fsms && make run VERILATOR=$V > "$R/probe-M2.log" 2>&1; echo $? > "$R/probe-M2.rc" ) &
wait
git checkout -q -- tb/pp_top/sim_main.cpp tb/srp_stream_fsms/sim_main.cpp
git status --porcelain --untracked-files=no > "$R/probe-restore.status"

#!/bin/sh
# Phase 1 probes: head suites, head benches on ebb1f001 RTL, reviewer-owned mutants.
# Run on a host with headroom: eleven concurrent Verilator builds.
# usage: run_phase1.sh <packet dir> <verilator>
# Each job writes receipts/<job>.log and receipts/<job>.rc; jobs run concurrently.
set -u
P=$1
V=$2
T=$P/scratch/trees
R=$P/receipts
mkdir -p "$R"
job() { # name dir make-args...
  name=$1; dir=$2; shift 2
  ( cd "$dir" && make VERILATOR="$V" "$@" > "$R/$name.log" 2>&1; echo $? > "$R/$name.rc" ) &
}
job head-acmp_talker        "$T/head/tb/acmp_talker" run
job head-srp_stream_fsms    "$T/head/tb/srp_stream_fsms" all
job head-pp_top-maap        "$T/head/tb/pp_top" maap-internal
job oldrtl-acmp_talker      "$T/oldrtl/tb/acmp_talker" run
job oldrtl-srp_stream_fsms  "$T/oldrtl/tb/srp_stream_fsms" all
job oldrtl-pp_top-maap      "$T/oldrtl/tb/pp_top" maap-internal
for m in none_sticky record_holds_new_id epoch_never_ticks; do
  job "m_$m-acmp_talker" "$T/m_$m/tb/acmp_talker" run
done
for m in parked_txla_sends_new_value join_never_follows_leave; do
  job "m_$m-srp_stream_fsms" "$T/m_$m/tb/srp_stream_fsms" all
done
wait

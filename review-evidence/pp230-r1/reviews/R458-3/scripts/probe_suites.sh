#!/usr/bin/env bash
# Run one reviewer probe against the committed suites that build the SRP stream FSMs / top.
# usage: probe_suites.sh <probe name>   (tree: scratch/pt/<probe>, hdl/srp from scratch/probes/<probe>)
set -u
P=$REVIEWS/pp230-r458-3-packet; S=$P/scratch; pr=$1; T=$S/pt/$pr
rm -rf $T; mkdir -p $T/tb
cp -r $S/head/hdl $T/hdl; rm -rf $T/hdl/srp; cp -r $S/probes/$pr $T/hdl/srp
for d in common srp_stream_fsms srp_top; do cp -r $S/head/tb/$d $T/tb/$d; rm -rf $T/tb/$d/obj_*; done
for d in srp_stream_fsms srp_top; do
  (cd $T/tb/$d && make > $T/$d.log 2>&1); rc=$?
  fails=$(grep -c '^FAIL' $T/$d.log)
  echo "PROBE $pr suite=$d rc=$rc FAIL_lines=$fails tallies: $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' $T/$d.log | tr '\n' ';')"
  grep '^FAIL' $T/$d.log | head -5
done

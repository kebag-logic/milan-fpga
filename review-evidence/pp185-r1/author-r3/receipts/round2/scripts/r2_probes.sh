#!/usr/bin/env bash
# round 2: the reviewers' probes on exports of the head, unpiped, each with log and rc.
# claim and mr carry the base bench (b0f6f9c3) with the probe, as the reviewers' drivers
# build it; vendor is probe_rdc.py's vendor variant on the head bench.
W2=$VALIDATION_STORAGE/pp185-a647/r2/work/probes-head2
W=$VALIDATION_STORAGE/pp185-a647/r2/work/probes-head
R=$VALIDATION_STORAGE/pp185-a647/r2/rec/probes-head
mkdir -p $R; export PATH=$VALIDATION_STORAGE/pp185-a647/bin:$PATH
(cd $W2/claim/tb/aecp_notify && make run) > $R/probe-claim.log 2>&1; echo $? > $R/probe-claim.rc
(cd $W2/mr/tb/aecp_notify && make run) > $R/probe-midround.log 2>&1; echo $? > $R/probe-midround.rc
(cd $W/vendor/tb/pp_top && make aecp-dispatch) > $R/probe-vendor.log 2>&1; echo $? > $R/probe-vendor.rc
echo done > $R/probes.done

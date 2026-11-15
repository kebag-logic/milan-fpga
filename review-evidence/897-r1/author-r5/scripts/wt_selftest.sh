#!/bin/bash
# The CPU budget harness's self-test on the worktree's uncommitted harness edits (round 5, before their commit).
set -u
. /data-2/milan/tmp/897-a776/scripts/env.sh
export TMPDIR=/data-2/milan/tmp/897-a776/r4/tmp/wt-selftest; mkdir -p $TMPDIR
cd $LANES/897-aspath && python3 -B tb/verilator/ctrl_service_budget/run.py --self-test > /data-2/milan/tmp/897-a776/r4/logs/wt-selftest.log 2>&1
echo "rc=$?" >> /data-2/milan/tmp/897-a776/r4/logs/wt-selftest.log

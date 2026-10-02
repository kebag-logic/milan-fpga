#!/bin/bash
# Reproduce the disclosed sweep-relaunch deviation: the suite-cancellation
# self-test plain, then under nohup. Usage: cancel_nohup.sh <clone> <outdir>
set -u
C=$1; O=$2; cd "$C"
timeout 300 python3 scripts/test_suite_cancellation.py > "$O/cancel_plain.log" 2>&1; echo "plain rc=$?" > "$O/cancel.rc"
timeout 300 nohup python3 scripts/test_suite_cancellation.py > "$O/cancel_nohup.log" 2>&1; echo "nohup rc=$?" >> "$O/cancel.rc"

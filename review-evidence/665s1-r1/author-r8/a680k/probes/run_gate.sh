#!/bin/bash
# Run one gate command from the lane checkout, its output and then "rc=N elapsed=Ns" into a log.
#   $1 the log   $2... the command (run from the checkout, the current directory)
log=$1
shift
start=$(date +%s)
"$@" > "$log" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s) - start ))s" >> "$log"
exit $rc

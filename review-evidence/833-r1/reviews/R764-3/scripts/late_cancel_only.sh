#!/usr/bin/env bash
# usage: late_cancel_only.sh <checkout> <log> <rc>
# Runs only owner_late_cancel from <checkout>'s scripts/test_suite_cancellation.py,
# inside its own user+PID namespace, and prints its wall time. Writes <log> and <rc>.
d=$1; log=$2; rcf=$3
cd "$d" && timeout -k 5 120 unshare --user --map-current-user --pid --fork --kill-child --mount-proc python3 -c "
import sys, time; sys.path.insert(0, 'scripts'); import test_suite_cancellation as t
b=time.monotonic(); t.owner_late_cancel(); print(f'owner_late_cancel {time.monotonic()-b:.2f} s')" > "$log" 2>&1
echo $? > "$rcf"

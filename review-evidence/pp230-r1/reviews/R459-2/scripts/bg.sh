#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# bg.sh LOGBASE CMD...   run CMD detached; LOGBASE.log gets its output and
# LOGBASE.rc its exit status once it ends (so a waiter polls for the .rc).
L=$1; shift
rm -f "$L.rc"
setsid nohup bash -c '"$@" > "$0.log" 2>&1; echo $? > "$0.rc"' "$L" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $L pid $!"

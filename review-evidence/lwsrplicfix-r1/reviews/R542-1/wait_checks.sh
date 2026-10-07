#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Wait up to <seconds> for <out-dir>/<name>.rc files, then print each status.
# Usage: wait_checks.sh <out-dir> <seconds> <name>...
set -eu
out=$1; limit=$2; shift 2
start=$(date +%s)
while :; do
    missing=0
    for n in "$@"; do [ -f "$out/$n.rc" ] || missing=1; done
    [ "$missing" -eq 0 ] && break
    [ $(( $(date +%s) - start )) -ge "$limit" ] && break
    sleep 5
done
for n in "$@"; do
    if [ -f "$out/$n.rc" ]; then echo "$n rc=$(cat "$out/$n.rc")"; else echo "$n RUNNING"; fi
done

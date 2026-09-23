#!/usr/bin/env bash
# rec.sh NAME CMD... : run CMD in the lane, keep stdout+stderr and the exit code.
set -u
OUT=$MANAGEMENT/2026-09-23/437-a184/receipts
name=$1; shift
cd $LANES/437-container-paragraph-scopes || exit 99
start=$(date -u +%FT%TZ)
"$@" >"$OUT/$name.log" 2>&1
rc=$?
printf '%s\t%s\t%s\t%s\t%s\n' "$name" "$rc" "$(git rev-parse HEAD)" "$start" "$*" >>"$OUT/exits.tsv"
echo "$name exit=$rc"
exit $rc

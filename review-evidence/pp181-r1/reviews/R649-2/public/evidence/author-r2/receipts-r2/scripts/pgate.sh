#!/usr/bin/env bash
# usage: pgate.sh <record-dir> <name> <workdir> <command...>  (unpiped; log, rc, seconds)
rec="$1"; name="$2"; wd="$3"; shift 3
mkdir -p "$rec"
export PATH="<data>/tmp/pp181-a635/bin-parent:$PATH"
export LC_ALL=C.UTF-8
start=$(date +%s)
( cd "$wd" && "$@" ) > "$rec/$name.log" 2>&1
rc=$?
echo "$rc" > "$rec/$name.rc"
echo "$name rc=$rc secs=$(( $(date +%s) - start ))" >> "$rec/summary.txt"

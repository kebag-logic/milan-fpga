#!/usr/bin/env bash
# Usage: bg.sh <name> <dir> <cmd...>: run detached; log to $R/<name>.log, rc to $R/<name>.rc
name=$1 dir=$2; shift 2
setsid bash -c 'cd "$1"; shift; s=$(date +%s); "$@" > "$R/$N.log" 2>&1; rc=$?; echo $(( $(date +%s)-s )) > "$R/$N.seconds"; echo $rc > "$R/$N.rc"' _ "$dir" "$@" </dev/null >/dev/null 2>&1 &

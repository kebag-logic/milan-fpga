#!/usr/bin/env bash
# bg.sh <receipt-name> <bin-dir> <workdir> <command...>
# Runs the command detached with <bin-dir> first on PATH; writes
# receipts/<name>.{cmd,log,rc,secs}. The .rc file appears only at the end.
set -u
P="$(cd "$(dirname "$0")/.." && pwd)"
name=$1 bin=$2 wd=$3; shift 3
R=$P/receipts; mkdir -p "$R"; rm -f "$R/$name.rc"
printf 'cd %q && PATH=%q:$PATH' "$wd" "$bin" > "$R/$name.cmd"; printf ' %q' "$@" >> "$R/$name.cmd"; echo >> "$R/$name.cmd"
( start=$(date +%s); cd "$wd" && PATH="$bin:$PATH" "$@" > "$R/$name.log" 2>&1 </dev/null; rc=$?
  echo $(( $(date +%s) - start )) > "$R/$name.secs"; echo $rc > "$R/$name.rc" ) </dev/null >/dev/null 2>&1 &
disown

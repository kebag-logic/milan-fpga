#!/usr/bin/env bash
# Start one detached campaign with its own log, rc and resource record.
# usage: launch.sh NAME BINDIR WORKDIR -- command args...
#   NAME     receipt stem under $PACKET/receipts
#   BINDIR   directory prepended to PATH (verilator, sv2v, yosys links)
#   WORKDIR  directory the command runs in
# Env: PACKET (default: this script's parent dir), TMPDIR is set to $PACKET/scratch/tmp.
set -euo pipefail
name=$1 bindir=$2 workdir=$3; shift 3
[ "$1" = "--" ] && shift
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
rec=$PACKET/receipts
mkdir -p "$rec" "$PACKET/scratch/tmp"
printf '%q ' "$@" > "$rec/$name.cmd"; echo >> "$rec/$name.cmd"
{
  echo "workdir=${workdir/#$PACKET/<packet>}"
  echo "path_prefix=${bindir/#$PACKET/<packet>}"
  for t in verilator sv2v yosys; do
    p=$(PATH="$bindir:$PATH" command -v $t || true)
    [ -n "$p" ] && echo "$t=$(PATH="$bindir:$PATH" $t --version 2>&1 | head -1)"
  done
  echo "started=$(date -u +%FT%TZ)"
} > "$rec/$name.env"
rm -f "$rec/$name.rc"
BINDIR=$bindir TMPD=$PACKET/scratch/tmp REC=$rec/$name \
  setsid nohup bash -c '
  cd "$1"; shift
  export PATH="$BINDIR:$PATH" TMPDIR="$TMPD"
  /usr/bin/time -v -o "$REC.time" "$@" > "$REC.log" 2>&1
  echo $? > "$REC.rc"
' launch "$workdir" "$@" </dev/null >/dev/null 2>&1 &
echo "launched $name pid $!"

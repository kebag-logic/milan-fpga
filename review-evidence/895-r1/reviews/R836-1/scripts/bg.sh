#!/bin/bash
# usage: CLONE=<review checkout> TOOLS=<pinned tools> bg.sh NAME CMD...
# Runs CMD detached from CLONE with the reviewer environment; its log and rc go to <packet>/receipts/run/NAME.{log,rc}.
P=$(cd "$(dirname "$0")/.." && pwd)
: "${CLONE:?set CLONE to the review checkout}"
name=$1; shift
mkdir -p "$P/receipts/run" "$P/scratch/tmp/$name"
( source "$P/scripts/env.sh"; export TMPDIR="$P/scratch/tmp/$name"; cd "$CLONE";
  echo "== $name start $(date -u +%FT%TZ) :: $*"; "$@"; r=$?; echo "== $name rc $r $(date -u +%FT%TZ)"; echo $r > "$P/receipts/run/$name.rc" ) > "$P/receipts/run/$name.log" 2>&1 < /dev/null &
echo "started $name pid $!"

#!/bin/sh
# Usage: launch.sh <name> <workdir> <command...>; writes logs/<name>.log and logs/<name>.rc
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
export TMPDIR=$P/scratch/tmp
: "${VERILATOR:?set VERILATOR to the pinned 5.050 executable}"; export VERILATOR
( cd "$dir" && { date -u +%FT%TZ; echo "+ $*"; } > "$P/logs/$name.log" && "$@" >> "$P/logs/$name.log" 2>&1; echo $? > "$P/logs/$name.rc"; date -u +%FT%TZ >> "$P/logs/$name.log" ) &

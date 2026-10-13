#!/usr/bin/env bash
# Launch one named review run detached, with its own log and rc file.
# Usage: launch.sh NAME CWD -- COMMAND...
set -u
name="$1"; cwd="$2"; shift 3
packet="$(cd "$(dirname "$0")/.." && pwd)"
runs="$packet/runs"
mkdir -p "$runs" "$packet/scratch/tmp/$name"
rm -f "$runs/$name.rc"
(
  cd "$cwd" || exit 97
  export TMPDIR="$packet/scratch/tmp/$name" PYTHONDONTWRITEBYTECODE=1
  export VERILATOR="${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}"
  date -u +"start %FT%TZ" > "$runs/$name.time"
  printf '%q ' "$@" > "$runs/$name.cmd"; echo >> "$runs/$name.cmd"
  "$@" > "$runs/$name.log" 2>&1
  echo $? > "$runs/$name.rc"
  date -u +"end %FT%TZ" >> "$runs/$name.time"
) </dev/null >/dev/null 2>&1 &
disown
echo "launched $name"

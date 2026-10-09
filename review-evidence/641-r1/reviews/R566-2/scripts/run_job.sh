#!/usr/bin/env bash
# Usage: run_job.sh <name> <dir> <command...>
# Runs one command in <dir>; writes receipts/<name>.log and receipts/<name>.rc.
set -u
P="$(cd "$(dirname "$0")/.." && pwd)"
name=$1; dir=$2; shift 2
cd "$dir" || exit 2
{
  echo "# job $name  dir=$(basename "$dir")  head=$(git rev-parse HEAD)  start=$(date -u +%FT%TZ)"
  echo "# cmd: $*"
} > "$P/receipts/$name.log"
"$@" >> "$P/receipts/$name.log" 2>&1
rc=$?
echo "# end=$(date -u +%FT%TZ) rc=$rc" >> "$P/receipts/$name.log"
echo "$rc" > "$P/receipts/$name.rc"

#!/usr/bin/env bash
# Start one campaign detached, with its own log and rc file under $P/scratch/runs.
# Usage: P=<packet> TOOLS=<toolchains> bg.sh <name> <dir> <command...>
export P TOOLS; name=$1; dir=$2; shift 2
mkdir -p $P/scratch/runs; rm -f $P/scratch/runs/$name.rc
setsid nohup bash -c 'cd "$1"; shift; . "$P"/scripts/env.sh; start=$(date +%s); "$@"; rc=$?; echo "$rc $(( $(date +%s) - start ))s" > "$P/scratch/runs/'"$name"'.rc"' _ "$dir" "$@" > $P/scratch/runs/$name.log 2>&1 < /dev/null &
echo "started $name"

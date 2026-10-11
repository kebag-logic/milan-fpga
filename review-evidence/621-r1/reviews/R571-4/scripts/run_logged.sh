#!/bin/bash
# Usage: run_logged.sh <name> <workdir> <command...>
# Runs the command in <workdir> with the pinned simulator first on PATH,
# writing receipts/<name>.log, receipts/<name>.rc and receipts/<name>.time.
set -u
PACKET="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
name=$1; dir=$2; shift 2
export PATH="$PACKET/scratch/bin:$PATH"
cd "$dir" || exit 2
start=$(date +%s.%N)
"$@" > "$PACKET/receipts/$name.log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "$rc" > "$PACKET/receipts/$name.rc"
python3 -c "print(f'{$end-$start:.1f} s wall')" > "$PACKET/receipts/$name.time"

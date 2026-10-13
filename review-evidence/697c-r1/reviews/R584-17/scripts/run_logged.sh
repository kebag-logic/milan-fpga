#!/bin/bash
# run_logged.sh NAME CMD... : run CMD from the clone root, log to receipts/NAME.log, exit status to receipts/NAME.rc
set -u
. "$(dirname "$0")/env.sh"
name=$1; shift
cd "$CLONE"
start=$(date +%s)
{ echo "# cmd: $*"; echo "# head: $(git rev-parse HEAD)"; echo "# python: $(command -v python3) $(python3 --version 2>&1)"; "$@"; } > "$PACKET/receipts/$name.log" 2>&1
rc=$?
echo "$rc $(( $(date +%s) - start ))s" > "$PACKET/receipts/$name.rc"

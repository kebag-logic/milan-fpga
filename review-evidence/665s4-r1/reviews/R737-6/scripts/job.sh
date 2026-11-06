#!/bin/bash
# job.sh NAME DIR COMMAND...: run COMMAND in DIR with the probe environment; receipts/NAME.log and receipts/NAME.rc.
P=$(cd "$(dirname "$0")/.." && pwd); export P; . "$P/scripts/env.sh"
n=$1; d=$2; shift 2; cd "$d" || exit 9
{ echo "# $n: $*"; echo "# head $(git rev-parse HEAD)"; echo "# start $(date -u +%FT%TZ)"; "$@"; rc=$?; echo "# end $(date -u +%FT%TZ) rc=$rc"; echo $rc > "$P/receipts/$n.rc"; } > "$P/receipts/$n.log" 2>&1

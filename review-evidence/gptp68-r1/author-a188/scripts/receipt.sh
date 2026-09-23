#!/bin/sh
# One receipt of reproduce.sh, run on its own (one foreground call each):
# receipts/<name>.log (command, start, output, end, exit) and <name>.exit.
# Usage: receipt.sh <name> <command...>
set -u
. $REVIEWS/gptp68-a188-packet/scripts/env.sh
R=$A188_PACKET/receipts
cd "$A188_LANE" || exit 2
n=$1; shift
{ echo "# command: $*"; echo "# start: $(date -Is)"; } > "$R/$n.log"
"$@" >> "$R/$n.log" 2>&1
rc=$?
{ echo "# end: $(date -Is)"; echo "# exit: $rc"; } >> "$R/$n.log"
echo "$rc" > "$R/$n.exit"
echo "$n exit=$rc"
exit $rc

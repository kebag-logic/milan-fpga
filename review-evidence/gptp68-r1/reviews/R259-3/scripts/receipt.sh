#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# receipt.sh NAME CMD...: run CMD in the foreground, write receipts/NAME.log
# (stdout+stderr, host paths replaced by $HOME / $DATA) and receipts/NAME.exit.
set -u
. "$(dirname "$0")/env.sh"
name=$1; shift
log="$PACKET/receipts/$name.log"
mkdir -p "$(dirname "$log")"
{ echo "# receipt $name"; echo "# command: $*"; echo "# started $(date -u +%Y-%m-%dT%H:%M:%SZ)"; } > "$log.raw"
"$@" >> "$log.raw" 2>&1
rc=$?
echo "# finished $(date -u +%Y-%m-%dT%H:%M:%SZ) exit $rc" >> "$log.raw"
sed -e "s#$DATA#\$DATA#g" -e "s#$HOME#\$HOME#g" "$log.raw" > "$log"
rm -f "$log.raw"
echo "$rc" > "$PACKET/receipts/$name.exit"
exit $rc

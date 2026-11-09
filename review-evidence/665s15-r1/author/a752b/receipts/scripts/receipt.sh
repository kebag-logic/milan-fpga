#!/bin/bash
# Copy files into the output directory's receipts, host paths replaced by placeholders.
# usage: receipt.sh SUBDIR FILE [NAME]
set -eu
O=$MGMT/665s15-a752b/receipts/$1
mkdir -p "$O"
sed -e 's#$SCRATCH#$SCRATCH#g' -e 's#$LANE#$LANE#g' \
    -e 's#$MGMT#$MGMT#g' -e 's#$HOME/#$HOME/#g' -e 's#$HOME#$HOME#g' \
    -e 's#$DATA/#$DATA/#g' "$2" > "$O/${3:-$(basename "$2")}"

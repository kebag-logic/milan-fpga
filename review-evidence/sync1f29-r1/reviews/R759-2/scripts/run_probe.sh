#!/bin/bash
# run_probe.sh NAME TREE CMD...: run one harness command in a scratch tree, with its own log and rc file
P=${PACKET:?}; name=$1; tree=$2; shift 2
export TOOLS=$VALIDATION_TOOLS
. "$P/scripts/env.sh"
cd "$tree" || exit 9
"$@" > "$P/receipts/$name.log" 2>&1
echo $? > "$P/receipts/$name.rc"

#!/bin/bash
# usage: run_bg.sh NAME WORKDIR CMD... ; writes $PACKET/receipts/NAME.log and NAME.rc
. "$(dirname "$0")/env.sh"
name=$1; dir=$2; shift 2
cd "$dir" || exit 2
( "$@" > "$PACKET/receipts/$name.log" 2>&1; echo $? > "$PACKET/receipts/$name.rc" ) &

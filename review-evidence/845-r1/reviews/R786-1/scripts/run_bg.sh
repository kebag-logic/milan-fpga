#!/bin/bash
# usage: run_bg.sh <name> <workdir> <cmd...>; writes ../receipts/<name>.log and .rc
P=$(cd "$(dirname "$0")/.." && pwd)
n=$1; d=$2; shift 2
( cd "$d" && "$@" ) > "$P/receipts/$n.log" 2>&1
echo $? > "$P/receipts/$n.rc"

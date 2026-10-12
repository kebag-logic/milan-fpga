#!/bin/sh
# bg.sh <name> <command...>: run a command detached; log to receipts/<name>.log
# and its exit status to receipts/<name>.rc, beside this script.
P=$(cd "$(dirname "$0")" && pwd)
name=$1; shift
rm -f "$P/receipts/$name.rc"
( "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) &

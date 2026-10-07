#!/bin/sh
# Usage: launch.sh NAME CMD...  -- detached run with log and rc file under receipts/jobs
PKT=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}; N=$1; shift
mkdir -p $PKT/receipts/jobs
setsid nohup sh -c '"$@" > '"$PKT/receipts/jobs/$N.log"' 2>&1; echo $? > '"$PKT/receipts/jobs/$N.rc" sh "$@" < /dev/null > /dev/null 2>&1 &

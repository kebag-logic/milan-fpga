#!/usr/bin/env bash
# Usage: waitrc.sh SECONDS NAME...  waits (foreground, bounded) for each NAME.rc, prints status
P=$REVIEWS/pp168-r552-1-packet
lim=$1; shift; t=0
while :; do
  all=1; for n in "$@"; do [ -f "$P/receipts/$n.rc" ] || all=0; done
  [ $all = 1 ] && break
  [ $t -ge $lim ] && break
  sleep 15; t=$((t+15))
done
for n in "$@"; do if [ -f "$P/receipts/$n.rc" ]; then echo "$n rc=$(cat $P/receipts/$n.rc)"; else echo "$n RUNNING"; fi; done
free -g | sed -n 2p

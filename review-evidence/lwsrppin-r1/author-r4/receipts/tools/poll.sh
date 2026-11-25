#!/bin/bash
# poll.sh SECONDS: wait up to SECONDS, stopping early when the count of finished runs changes; then one status line.
H=/data-2/milan/tmp/lwsrppin-a834/r4/harness; end=$(( $(date +%s) + $1 )); n0=$(ls $H/rc-* 2>/dev/null | wc -l)
while [ $(date +%s) -lt $end ]; do [ $(ls $H/rc-* 2>/dev/null | wc -l) -ne $n0 ] && break; sleep 15; done
s="$(date +%H:%M)"; for n in 1x1 8x8-1if 1x1-every 8x8-1if-every 1x1-later 8x8-1if-later selftest; do s="$s $n=$(cat $H/rc-$n 2>/dev/null || echo -)"; done
echo "$s avail=$(free -g | awk 'NR==2{print $7}')G"

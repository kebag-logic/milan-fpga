#!/bin/bash
# waitev.sh <root> <minutes>: return when a driver or lane group finishes, a step rc is not 0, or the time is up
R=$1; B=<scratch>/bg; end=$(( $(date +%s) + $2 * 60 ))
state() { echo "$(ls $B/*.rc $R/logs/standalone*.rc 2>/dev/null | wc -l) $(grep -l 'DRIVER DONE' $R/drivers/*.log 2>/dev/null | wc -l) $(grep -Lx 0 $R/logs/*.rc $R/docs/logs/*.rc $R/lane/*.rc 2>/dev/null | wc -l)"; }
s0=$(state)
while [ "$(state)" = "$s0" ] && [ $(date +%s) -lt $end ]; do sleep 20; done
date +%T; cat $B/lane*.log | sort
for d in A B C D E; do [ -e $R/drivers/$d.log ] && echo "$d: $(grep -c 'rc=0$' $R/drivers/$d.log) ok; $(tail -n1 $R/drivers/$d.log)"; done
echo "bad: $(grep -Lx 0 $R/logs/*.rc $R/docs/logs/*.rc $R/lane/*.rc 2>/dev/null)"
systemctl --user show milan-665s11-a761b.service -p MemoryCurrent | cat; free -g | sed -n 2p; uptime

#!/bin/bash
# g19try3.sh: a third run of elaborate-gates-1 gate_19 at this head, on a free CPU range when one is picked, else on
# the shared pool once this lane's other gate jobs have ended and the one-minute load is under 64
G=<scratch>/gates; H=bc939bc72735e14969799347ed3bda325df1d3fb; R=$G/pass3; B=<scratch>/bg
while :; do
  r=$(/usr/bin/python3 <management>/2026-09-23/cpu_ranges.py pick)
  [ -n "$r" ] && break
  load=$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)
  if [ -e $B/drvA.rc ] && grep -q "LANE s2 DONE" $B/lanes2.log && [ "$load" -lt 64 ]; then r=96-127; break; fi
  sleep 60
done
echo "$(date +%T) gate_19 try 3 on $r (load $(cut -d' ' -f1 /proc/loadavg))" >> $R/logs/elaborate.elaborate-gates-1__gate_19.rerun-note
systemd-run --user --unit=milan-665s11-a761-g19c --collect -p MemoryMax=10G /usr/bin/taskset -c $r /bin/bash -c \
  "$G/venv/bin/python3 $G/tools/wf/run_wf.py elaborate $H elaborate-gates-1 $R gate_19 > $B/g19c.log 2>&1; echo \$? > $B/g19c.rc"

#!/usr/bin/env bash
# poll up to 540 s (or until file $1 exists); SIGSTOP the rtl-fast replica's process group above 10.5 GB unit memory
CG=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-780-a670b.service; X=$VALIDATION_STORAGE/scratch/780-a670; mx=0
for i in $(seq 1 54); do
  a=$(( $(cat $CG/memory.current) / 1048576 )); [ $a -gt $mx ] && mx=$a
  if [ $a -gt 10500 ]; then p=$(pgrep -f 'rtl_fast_steps.py' | head -1); [ -n "$p" ] && kill -STOP -- -$(ps -o pgid= -p $p | tr -d ' ') && echo "PAUSED rtl-fast at $a MB"; break; fi
  [ -n "${1:-}" ] && [ -e "$1" ] && break
  sleep 10
done
echo "max unit memory ${mx}MB; MemAvailable $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) GB"
echo "rtl-fast fw: rc=$(cat $X/r/rtlfast-25f05752-fw.rc 2>/dev/null || echo running); $(tail -1 $X/r/rtlfast-25f05752-fw.out)"
echo "firmware: $(tail -1 $X/r/firmware/table.txt | cut -c1-100)"

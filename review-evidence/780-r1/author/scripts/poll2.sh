#!/usr/bin/env bash
# poll for up to 540 s (or until file $1 exists): this unit's memory, rtl-fast and firmware progress
X=$VALIDATION_STORAGE/scratch/780-a670
cg=$(sed 's/^0:://' /proc/self/cgroup | sed 's#/app.slice/.*#/app.slice/milan-780-a670b.service#'); mx=0
for i in $(seq 1 18); do
  a=$(( $(cat /sys/fs/cgroup$cg/memory.current) / 1048576 )); [ $a -gt $mx ] && mx=$a
  [ -n "${1:-}" ] && [ -e "$1" ] && break
  sleep 30
done
echo "max unit memory ${mx}MB; MemAvailable $(awk '/MemAvailable/{print int($2/1048576)}' /proc/meminfo) GB"
echo "rtl-fast: rc=$(cat $X/r/rtlfast-25f05752.rc 2>/dev/null || echo running); $(tail -1 $X/r/rtlfast-25f05752.out)"
echo "firmware: $(tail -1 $X/r/firmware/table.txt | cut -c1-100)"

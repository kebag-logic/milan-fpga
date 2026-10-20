#!/usr/bin/env bash
S=<scratch>
for j in B H G P; do printf '%-3s %s\n' "$j" "$(tail -1 $S/jobs/$j.out 2>/dev/null)"; done
for t in base/campaigns head4/campaigns head4/gates parent-base parent-head; do
  for r in $S/rec/$t/*.log; do [ -e "$r" ] || continue; n=$(basename $r .log); rc=$S/rec/$t/$n.rc
    [ -f "$rc" ] || printf '%-16s %-18s running | %s\n' "$t" "$n" "$(tail -1 $r | cut -c1-90)"; done; done
U=$(sed -n 's#^0::/##p' /proc/self/cgroup); D=/sys/fs/cgroup/$U
awk -v c=$(cat $D/memory.current) -v a=$(awk '$1=="anon"{print $2}' $D/memory.stat) 'BEGIN{printf "mem %.2f GB anon %.2f GB  ", c/1e9, a/1e9}'
tail -n 400 $S/memlog.txt | sort -k2 -n | tail -1 | awk '{printf "peak(last100min) %.2f GB  ", $2/1e9}'
uptime | sed 's/.*load/load/'; df -h /data | tail -1 | awk '{print "disk free " $4}'; tail -2 $S/memguard.log 2>/dev/null

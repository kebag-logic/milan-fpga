#!/bin/bash
S=/data-2/milan/tmp/665s2b-a683zo
date +%T
for n in GA8 GA1 GN8 GN1 GB1; do d=$S/builds/$n/results; [ -d $d ] || { echo "$n: not started"; continue; }
  echo "$n: $(grep -l SUMMARY $d/*.log 2>/dev/null | wc -l) done / $(ls $d/*.txt 2>/dev/null | wc -l) started rc=$(cat $S/logs/$n.log.rc 2>/dev/null || echo -)"; done
for m in srp-compared-by-memcmp notice-fan-out-as-it-was polls-rebuild-in-the-base polls-rebuild-twice; do f=$S/logs/ctl-$m-9e6f0141.log; [ -f $f ] && echo "$m: rc=$(cat $f.rc 2>/dev/null || echo -) $(grep '^CONTROL' $f | cut -c1-160)"; done
tail -2 $S/logs/dispatch30.txt; cat $S/logs/diskguard.txt 2>/dev/null | tail -1; df -h /data-2 | tail -1 | awk '{print "data-2 free", $4}'; grep MemAvailable /proc/meminfo

#!/bin/bash
# status.sh: one compact line per driver and lane, memory, and the sweeps
S=<scratch>; R=$S/gates/pass1
echo "$(date +%T) $(tail -n 1 $R/phase/log)"
for f in $R/drivers/*.log; do echo -n "$(basename $f .log):$(grep -c 'rc=0' $f)ok/$(grep 'rc=' $f | grep -vc 'rc=0')bad$(grep -q 'DRIVER DONE' $f && echo '(done)') "; done; echo
for f in $R/lane/*.rc; do echo -n "$(basename $f .rc)=$(cat $f) "; done; echo
grep 'rc=' $R/drivers/*.log | grep -v 'rc=0' | sed 's#.*/##' | head -5
echo "unit $(( $(systemctl --user show milan-665s11-a761d.service -p MemoryCurrent --value)/1048576 ))MB avail $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)MB; sweep1: $(systemctl --user list-units --plain --no-legend 'milan-665s11-a761c-sw*' | wc -l) units; sweep2: $(tail -n 1 $S/gates/sweep/launch2.txt | cut -c1-90)"
for f in r821 r822; do echo -n "$f=$(cat $S/probes/$f.rc 2>/dev/null) "; done; cat $S/probes/final.txt 2>/dev/null; echo
C=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice
echo "anon: session $(awk '/^anon /{print int($2/1048576)}' $C/milan-665s11-a761d.service/memory.stat)MB census $(awk '/^anon /{print int($2/1048576)}' $C/milan-665s11-a761c-census.service/memory.stat 2>/dev/null)MB; census rc=$(cat $S/logs/census.rc 2>/dev/null); timing-cuts rc=$(cat $S/gates/pass1/logs/elaborate.elaborate-gates-1__gate_19.standalone-test_soc_timing_cuts.rc 2>/dev/null); sweep2 units $(systemctl --user list-units --plain --no-legend 'milan-665s11-a761c-sx*' | wc -l)"

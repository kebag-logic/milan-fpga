#!/usr/bin/env bash
# Round 7c: wait up to <seconds> (default 540) or until a watched rc/done file
# appears that was not there at the start, then print every job's state.
# Keeps the unit's MemoryCurrent under 9 GB (page cache counts in it).
set -u
S=$VALIDATION_STORAGE/scratch/632-a659/r7; B7=$VALIDATION_STORAGE/scratch/632-a659/r7b; B=$VALIDATION_STORAGE/scratch/632-a659/r7c; h=c2c996fa
limit=${1:-540}
watch() { ls $S/camp/gmstep-$h/rc $B/fw-$h/ctrl_boundary.rc $B7/docs-$h/end $B/sweep-$h/DONE 2>/dev/null | sort; }
before=$(watch); t0=$SECONDS
cg=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-632-a659n.service
trim() { [ "$(cat $cg/memory.current)" -gt 8589934592 ] && echo 3G > $cg/memory.reclaim 2>/dev/null; true; }
until [ "$(watch)" != "$before" ] || [ $((SECONDS - t0)) -ge "$limit" ]; do trim; sleep 15; done
trim
date -u +%T
echo "current $(( $(cat $cg/memory.current) / 1048576 )) MB; anon $(( $(awk '/^anon /{print $2}' $cg/memory.stat) / 1048576 )) MB; $(grep oom_kill $cg/memory.events); $(cut -d' ' -f1-3 /proc/loadavg)"
f=$S/camp/gmstep-$h/log
echo "gmstep: $(grep -c '\[PASS\]' $f 2>/dev/null) PASS $(grep -c '\[FAIL\]' $f 2>/dev/null) FAIL rc=$(cat $S/camp/gmstep-$h/rc 2>/dev/null)"
echo "fwb: $(tail -1 $B/fw-$h/progress.txt 2>/dev/null | cut -c1-140)"
echo "docs: $(tail -1 $B7/docs-$h/all.out 2>/dev/null | cut -c1-120) | all.rc=$(cat $B7/docs-$h/all.rc 2>/dev/null) end=$(cat $B7/docs-$h/end 2>/dev/null)"
[ -d $B/sweep-$h ] && echo "sweep: $(ls $B/sweep-$h | tr '\n' ' ')"
true

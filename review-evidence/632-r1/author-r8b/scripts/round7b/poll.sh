#!/usr/bin/env bash
# Round 7b: wait up to <seconds> (default 540) or until a watched rc/done file
# appears that was not there at the start, then print every job's state.
set -u
S=$VALIDATION_STORAGE/scratch/632-a659/r7; B=$VALIDATION_STORAGE/scratch/632-a659/r7b; h=d835ba12
limit=${1:-540}
watch() { ls $S/camp/tdm8m-$h/rc $S/camp/gmstep-$h/rc $S/camp/pullin-$h/rc $B/fw-$h/done-* $B/yosys-$h.rc \
  $B/docs-$h/end $B/builder-$h/builder.rc $B/sweep-$h/DONE $B/fwb-$h/done-* 2>/dev/null | sort; }
before=$(watch); t0=$SECONDS
cg=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-632-a659m.service
# keep MemoryCurrent under 9 GB: the page cache counts in it and the kernel only trims it at the 12 GB cap
trim() { [ "$(cat $cg/memory.current)" -gt 8589934592 ] && echo 3G > $cg/memory.reclaim 2>/dev/null; true; }
until [ "$(watch)" != "$before" ] || [ $((SECONDS - t0)) -ge "$limit" ]; do trim; sleep 15; done
trim
date -u +%T
cg=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/milan-632-a659m.service
echo "current $(( $(cat $cg/memory.current) / 1048576 )) MB; anon $(( $(awk '/^anon /{print $2}' $cg/memory.stat) / 1048576 )) MB; $(grep oom_kill $cg/memory.events); $(cut -d' ' -f1-3 /proc/loadavg)"
for n in tdm8m gmstep; do
  f=$S/camp/$n-$h/log
  echo "$n: $(grep -c '\[PASS\]' $f 2>/dev/null) PASS $(grep -c '\[FAIL\]' $f 2>/dev/null) FAIL rc=$(cat $S/camp/$n-$h/rc 2>/dev/null)"
done
echo "pullin: $(ls $S/camp/pullin-$h 2>/dev/null | grep -c '^pullin_.*log$') logs rc=$(cat $S/camp/pullin-$h/rc 2>/dev/null)"
echo "fw: $(tail -1 $B/fw-$h/progress.txt 2>/dev/null | cut -c1-140)"
echo "yosys: $(grep -c '\[PASS\]' $B/yosys-$h.log 2>/dev/null) PASS $(grep -c '\[FAIL\]' $B/yosys-$h.log 2>/dev/null) FAIL rc=$(cat $B/yosys-$h.rc 2>/dev/null)"
echo "docs: $(tail -1 $B/docs-$h/all.out 2>/dev/null | cut -c1-120) | all.rc=$(cat $B/docs-$h/all.rc 2>/dev/null) end=$(cat $B/docs-$h/end 2>/dev/null)"
echo "builder: rc=$(cat $B/builder-$h/builder.rc 2>/dev/null) $(tail -1 $B/builder-$h/builder.log 2>/dev/null | cut -c1-120)"
[ -d $B/sweep-$h ] && echo "sweep: $(ls $B/sweep-$h | tr '\n' ' ')"
[ -d $B/fwb-$h ] && echo "fwb: $(tail -1 $B/fwb-$h/progress.txt 2>/dev/null | cut -c1-140)"
true

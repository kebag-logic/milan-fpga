#!/usr/bin/env bash
# After the head campaigns: the R665-1 probes and the R666-1 reproduction at
# the exact round-2 head (a fresh export of it, never the lane's working tree).
set -u
S=<scratch>
HEAD_SHA=$(cat $S/head2.sha)
# (resume: no wait on the campaigns; the export is independent of them)
X=$S/rec2/probes/export
rm -rf $S/rec2/probes; mkdir -p $X
git -C <lane> archive "$HEAD_SHA" | tar -x -C $X
echo "$HEAD_SHA" > $S/rec2/probes/export.sha
bash $S/scripts/r2/run_r665_probes.sh $X $S/rec2/probes/r665
W=$S/rec2/probes/r666
mkdir -p $W/tb
cp -r $X/hdl $W/
for d in common pp_top srp_stream_fsms; do cp -r $X/tb/$d $W/tb/; done
( cd $W && patch -p1 --no-backup-if-mismatch < $S/review-packets/R666-1/receipts/reviewer-probes.patch > $W.apply.log 2>&1; echo $? > $W.apply.rc )
rm -f $W/tb/pp_top/sim_main.cpp.rej
python3 -I - "$W/tb/pp_top/sim_main.cpp" <<'PY' >> $W.apply.log 2>&1
import sys
p = sys.argv[1]
t = open(p).read()
old = "    as_in_place_swap_follows_the_registered_type();\n    as_coalesced_swaps_follow_the_last_type();\n"
new = "    as_in_place_swap_follows_the_registered_type();\n    review_stalled_swaps();\n    as_coalesced_swaps_follow_the_last_type();\n"
assert t.count(old) == 1
open(p, "w").write(t.replace(old, new))
print("hunk 1 (the call) placed by hand after as_in_place_swap_follows_the_registered_type()")
PY
bash $S/scripts/r2/run_r666_repro.sh $W
echo done > $S/rec2/probes/ALL.done

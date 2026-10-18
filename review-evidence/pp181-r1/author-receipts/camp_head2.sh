#!/usr/bin/env bash
# resume of camp_head.sh after the 10:57 crash: acmp (its run was cut mid-way, no rc line),
# then the two campaigns that refuse an existing output (never started at head).
S=<data>/tmp/pp181-a635; T=<data>/lanes/pp181-cut
out=$S/camp/head
. $S/env.sh
export TMPDIR=$S/tmp; mkdir -p "$TMPDIR"
cd "$T" || exit 9
echo "resume $(git rev-parse HEAD)" >> "$out/rc-b.txt"
t0=$SECONDS rc=0
rm -rf "$out/acmp"; mkdir -p "$out/acmp"
python3 tb/pp_top/acmp_mutants.py --output "$out/acmp" --jobs 4 > "$out/acmp.log" 2>&1 || rc=$?
echo "acmp rc=$rc ($((SECONDS - t0))s)" >> "$out/rc-b.txt"
echo DONE >> "$out/rc-b.txt"
$S/campaigns2.sh $T head
echo CAMP-HEAD-DONE > $S/camp/head/done.txt

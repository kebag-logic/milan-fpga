#!/bin/bash
# all_diffs.sh: imgdiff.py and relink_cmp.py over every image pair, base clone against head clone: the CPU budget
# harness's twelve, the target platform's four and the size fixture's four. Writes cmp/all/<name>.{imgdiff,relink}.txt
# and cmp/all/SUMMARY.txt.
set -u
S=<scratch>; . $S/bin/env.sh
O=$S/cmp/all; mkdir -p $O; : > $O/SUMMARY.txt
pairs=()
for p in 1x1 8x8-1if 8x8; do for a in none answering-every-port answering-ports valid-destinations; do
  pairs+=("budget-$p-$a $S/img/budget-base/$p/$a/image $S/img/budget-head/$p/$a/image $S/clones/base $S/clones/head"); done; done
for p in 1x1-if1 1x1-if2 8x8-if1 8x8-if2; do
  pairs+=("platform-$p $S/img/plat-base/plat/$p $S/img/plat-head/plat/$p $S/clones/base-plat $S/clones/head-plat")
  pairs+=("fixture-$p $S/img/plat-base/fixture-$p $S/img/plat-head/fixture-$p $S/clones/base-plat $S/clones/head-plat"); done
for row in "${pairs[@]}"; do
  set -- $row; n=$1 b=$2 h=$3 bc=$4 hc=$5
  python3 -I $S/bin/imgdiff.py $b $h > $O/$n.imgdiff.txt 2>&1
  rm -rf $S/cmp/relink/$n; python3 -I $S/bin/relink_cmp.py $bc $b $hc $h $S/cmp/relink/$n > $O/$n.relink.txt 2>&1; rc=$?
  inputs=$(grep -m1 '^inputs that differ' $O/$n.imgdiff.txt | sed 's/^inputs that differ by sha256: //')
  sized=$(grep -m1 '^input sections whose size differs' $O/$n.imgdiff.txt | sed 's/^input sections whose size differs: //')
  canon=$(grep -m1 '^canonical listings' $O/$n.relink.txt | sed 's/^canonical listings: //')
  eq=$(grep -c 'loadable bytes EQUAL to the built image' $O/$n.relink.txt)
  ins=$(grep -E '^[-+]\s' $O/$n.relink.txt | tr -s '\t ' ' ' | tr '\n' ';')
  echo "$n | inputs differing: $inputs | sized: $sized | relinks equal to built: $eq/2 | canonical: $canon | lines: $ins | rc $rc" >> $O/SUMMARY.txt
done
cat $O/SUMMARY.txt

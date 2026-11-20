#!/bin/bash
# collect7.sh: the attribution experiment's receipts into r7attr/receipts (collect5.py copies them to round5's
# receipts/attr): per image, its head and edit, then each repeat's run summary and survey (srp-talker-held; the notice
# leg's ordinary and long views), the images' comparison, the projections and the tools. One file per image and leg.
set -u
T=<scratch>; A=$T/r7attr; O=$A/receipts; mkdir -p $O/tools
declare -A CL=([A]=r7-A [B]=r7-B [C]=r7-C [D]=r7-D [E]=r7-E)
for I in A B C D E; do
  C=$T/clones/${CL[$I]}
  for leg in $I notice-$I; do
    [ -d $A/$leg ] || continue
    f=$O/$leg.txt
    { echo "# image $I, leg $leg: head $(git -C $C rev-parse HEAD), $(git -C $C status --porcelain | wc -l) file(s) edited"
      git -C $C diff
      echo "## build"; cat $A/$leg/build.log | grep -E '^(BUILD|BUILT)'
      echo "ctrl_app.elf sha256 $(sha256sum $A/$leg/build/image/ctrl_app.elf | cut -d' ' -f1)"
      for k in 1 2 3; do
        echo "## repeat $k: run.py rc $(cat $A/$leg/rep$k.rc 2>/dev/null)"
        grep -hE 'groups graded|^STEPS|^JOINS|^SAVE|^SHARE|^CLOCK' $A/$leg/rep$k.log | cut -c1-400
        for v in ordinary long; do
          d=$A/out/$leg-rep$k/survey/$v-costs
          [ -f $d/costs.txt ] && { echo "### survey, $v view: costs.txt"; cat $d/costs.txt; echo "### aecp.txt"; cat $d/aecp.txt; }
        done
        [ -f $A/out/$leg-rep$k/survey/compare-long.txt ] && { echo "### compare-long.txt"; cat $A/out/$leg-rep$k/survey/compare-long.txt; }
      done
    } > $f
  done
done
cp $A/images.txt $A/project-*.txt $A/table7.md $O/ 2>/dev/null
cp $A/attr.sh $A/notice.sh $A/analyse7.sh $A/table7.py $A/collect7.sh $A/images.sh $O/tools/ 2>/dev/null
ls -la $O $O/tools | awk '{print $5, $NF}'

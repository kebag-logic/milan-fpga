#!/bin/bash
# fab_exports.sh <label> <commit> [patch]: the all-fabric shipping exports (1x1 and 8x8) of <commit>, with <patch>
# applied when given, from one fixed clone path into one fixed output path, then moved to exports/<label>-<cfg>,
# so two runs differ only in what the commit changes
set -eu
S=<scratch>; LANE=<lane>
label=$1; commit=$2; patch=${3:-}
wt=$S/fab/wt
if [ ! -d $wt ]; then
  git clone -q --shared --no-checkout $LANE $wt
fi
git -C $wt fetch -q $LANE $commit 2>/dev/null || true
git -C $wt reset -q --hard; git -C $wt clean -qfdx -e configs/generated -e sw/builder/out
git -C $wt -c advice.detachedHead=false checkout -q --detach $commit
for dep in $(git -C $wt config --file $wt/.gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}'); do
  [ "$dep" = external ] && continue; [ -e $LANE/$dep/.git ] && git -C $wt config submodule.$dep.url $LANE/$dep
done
git -C $wt -c protocol.file.allow=always submodule update -q --init --force $(git -C $wt config --file $wt/.gitmodules --get-regexp '^submodule\..*\.path$' | awk '{print $2}' | grep -v '^external$')
[ -n "$patch" ] && git -C $wt apply $patch
git -C $wt rev-parse HEAD > $S/exports/$label.commit
git -C $wt status --porcelain > $S/exports/$label.status
for cfg in ax7101_1x1_tdm8 ax7101_8x8; do
  rm -rf $S/fab/out
  (cd $wt && python3 -B $S/scripts/export_fabric.py . $cfg $S/fab/out > $S/exports/$label-$cfg.log 2>&1)
  rm -rf $S/exports/$label-$cfg; mv $S/fab/out $S/exports/$label-$cfg
done
echo done

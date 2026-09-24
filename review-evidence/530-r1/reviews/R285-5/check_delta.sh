#!/usr/bin/env bash
# Delta checks for PR #549 round 4 (f814d37d..8ffd6c61). usage: check_delta.sh <repo>
set -u
R=${1:?repo}
D=$(cd "$(dirname "$0")" && pwd)
BASE=50e78097564244c124e1ec30dd8821f83951ab06
PREV=f814d37d94e17435f3b6dcc424f8b2b606cdd3e9
HEAD_=8ffd6c616840b161891e2eb714a7ddbbb72c7a0d
SIL=c593cbeff
DEV=3d2f3e3131c9db5898e1db9dd3e2a35149843109
g() { git -C "$R" "$@"; }
echo "== identity"; g rev-parse HEAD 'HEAD^{tree}'
echo "== stripped datapath"
python3 "$D/strip_sv_comments.py" "$R" hdl/milan/milan_datapath.sv $BASE $SIL $PREV 6556effc8 77068c9ad $HEAD_
echo "== hdl/ files differing c593cbef..head"; g diff --name-only $SIL $HEAD_ -- hdl
echo "== non-tb/scripts/hdl paths changed f814..head (non-doc?)"
g diff --name-only $PREV $HEAD_ | grep -v -E '\.md$' || echo "(only .md + listed above)"
echo "== tb/ scripts/ syn/ tests/ features/ changed f814..head"
g diff --name-only $PREV $HEAD_ -- tb scripts syn tests features || true
echo "== added/removed hdl lines f814..head that are not // comments"
g diff -U0 $PREV $HEAD_ -- hdl | grep -E '^[+-][^+-]' | grep -v -E '^[+-]\s*//' || echo "(none)"
echo "== metacomment tokens in changed hdl lines"
g diff -U0 $PREV $HEAD_ -- hdl | grep -E '^[+-][^+-]' | grep -i -E 'verilator|synopsys|pragma|lint_off|translate_' || echo "(none)"
echo "== gitlinks head"; g ls-tree $HEAD_ | awk '$2=="commit"'
echo "== modes of changed files f814..head"; g diff --raw $PREV $HEAD_ | awk '{print $1,$2,$6}'
echo "== merge-tree recompute of 6556effc"
MT=$(g merge-tree --write-tree --name-only $PREV $DEV | head -1); echo "auto tree $MT"
g merge-tree --write-tree --name-only $PREV $DEV | sed -n '2,$p'
echo "-- recorded merge vs auto tree (paths)"; g diff --name-status $MT 6556effc8
echo "-- FR-CONN row at head equals PR side; FR-MVU row equals dev side"
for id in 'FR-MVU-01..03' 'FR-CONN-01/02'; do
  for rev in $PREV $DEV 6556effc8 $HEAD_; do
    printf '%s %s ' "$id" "${rev:0:8}"
    g show $rev:docs/reference/FR_NFR.md | grep -F "| **$id**" | sha256sum | cut -c1-16
  done
done
echo "== diff --check f814..head and dev..head"; g diff --check $PREV $HEAD_ && echo clean1; g diff --check $DEV $HEAD_ && echo clean2
echo "== is dev tip ancestor of head"; g merge-base --is-ancestor $DEV $HEAD_ && echo yes

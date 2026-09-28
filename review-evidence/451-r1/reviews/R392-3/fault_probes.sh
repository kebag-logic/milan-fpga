#!/usr/bin/env bash
# R392-3 disposable fault probes. Usage: fault_probes.sh <repo> <scratch-dir> <python>
# Clones <repo> at the exact head into <scratch-dir>/probe, applies one fault at a
# time, runs the gate expected to catch it, and restores the file from Git.
set -u
REPO=${1:?repo}; SCR=${2:?scratch}; PY=${3:?python}
HEAD_EXP=0e5ae9c82bbdb5abc3feba84f07d0e6481254906
DEV=7390b43627032c71c470e2aa8d0845eb5b740663
P="$SCR/probe"; rm -rf "$P"
git clone -q --shared --no-checkout "$REPO" "$P" && git -C "$P" checkout -q --detach "$HEAD_EXP" || exit 2
cd "$P" || exit 2
export PYTHONDONTWRITEBYTECODE=1
IDX=docs/findings/README.md; CD=docs/litex/CLOCK_DOMAINS.md; MX=docs/reference/MILAN_COMPLIANCE_MATRIX.md
probe(){ # name expect(fail|pass) cmd...
  local n=$1 e=$2; shift 2; "$@" > "$SCR/probe_$n.log" 2>&1; local rc=$?
  local got=pass; [ $rc -ne 0 ] && got=fail
  printf '%-34s rc=%-3s probe-expect=%-4s %s\n' "$n" "$rc" "$e" "$([ $got = $e ] && echo AS-EXPECTED || { [ $got = pass ] && echo GATE-BLIND || echo UNEXPECTED-FAIL; })"
  git checkout -q -- . ; }
rowcheck(){ # index row invariants on the working copy: union of both sides, no dup, no marker
  local w; w=$(grep '^| \[' $IDX)
  [ "$(grep -cE '^(<<<<<<<|=======|>>>>>>>)' $IDX)" = 0 ] || return 1
  [ "$(printf '%s\n' "$w" | sort | uniq -d | wc -l)" = 0 ] || return 1
  [ "$( (git show 335e55c41:$IDX; git show $DEV:$IDX) | grep '^| \[' | sort -u | sha256sum)" = "$(printf '%s\n' "$w" | sort | sha256sum)" ] || return 1; }

probe baseline_rowcheck pass rowcheck
probe baseline_docs_check pass $PY scripts/docs_check.py
# F1 conflict markers left in the index
sed -i '11i <<<<<<< ours' $IDX; sed -i '13i =======' $IDX; sed -i '17i >>>>>>> theirs' $IDX
cp $IDX "$SCR/f1.md"; probe F1_marker_rowcheck fail rowcheck
cp "$SCR/f1.md" $IDX; probe F1_marker_docs_check fail $PY scripts/docs_check.py
cp "$SCR/f1.md" $IDX; probe F1_marker_gen_toc fail $PY scripts/gen_toc.py --check
cp "$SCR/f1.md" $IDX; git -c user.name=p -c user.email=p@p commit -q -am probe
probe F1_marker_git_diff_check fail git diff --check $DEV HEAD
git reset -q --hard "$HEAD_EXP"
# F2 duplicate row
sed -i '12p' $IDX; probe F2_duplicate_row_rowcheck fail rowcheck
sed -i '12p' $IDX; probe F2_duplicate_row_docs_check fail $PY scripts/docs_check.py
# F3 lost dev row (#397)
sed -i '/397_SERVICE_BUDGET/d' $IDX; probe F3_lost_row_rowcheck fail rowcheck
# F4 CLOCK_DOMAINS reworded into one long sentence
sed -i '140s/.*/- The example configuration exposes capture and physical TDM rendering, which TDM8 first light carried on hardware (#451)./' $CD
probe F4_long_sentence_doc_style fail $PY scripts/check_doc_style.py
# F5 em dash in the reworded matrix row
sed -i '207s/clocked on the shipping/clocked \xe2\x80\x94 on the shipping/' $MX
git -c user.name=p -c user.email=p@p commit -q -am probe
probe F5_em_dash fail $PY scripts/check_em_dash.py --base $DEV
git reset -q --hard "$HEAD_EXP"
# F6 broken link target in the reworded CLOCK_DOMAINS line
sed -i '140s/451_TDM8_FIRST_LIGHT.md/451_TDM8_FIRST_LIGHT_X.md/' $CD
probe F6_broken_link_docs_check fail $PY scripts/docs_check.py
sed -i '140s/451_TDM8_FIRST_LIGHT.md/451_TDM8_FIRST_LIGHT_X.md/' $CD
probe F6_broken_link_doc_paths fail $PY scripts/check_doc_paths.py
# F7 extra cell in the matrix row
sed -i '207s/ (#447), and / (#447) | and /' $MX
probe F7_extra_cell_docs_check fail $PY scripts/docs_check.py
echo "final head $(git rev-parse HEAD) status [$(git status --porcelain | wc -l) lines]"

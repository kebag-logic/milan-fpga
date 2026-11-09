#!/usr/bin/env bash
# Lane steps on a fresh clean clone of the head: inventory, style, behave, diff --check, gate-read readers, census.
set -u
H=$1; S=$VALIDATION_STORAGE/640-a720q; G=$S/gates; L=$LANES/640-mark2-charter
W=$G/extra/wt; LOGS=$G/logs; E=$HOME/milan-fpga-management/2026-09-23/640-a720l/evidence/census
DEV=$(git -C $L rev-parse ac0a01e3); OLD=$(git -C $L rev-parse 0a75aa77); R6=$(git -C $L rev-parse 72816d26)
rm -rf $G/extra; mkdir -p $G/extra $G/extra/tmp $G/extra/runner_temp
git clone -q --shared --no-checkout $L $W
git -C $W fetch -q $L $H
git -C $W -c advice.detachedHead=false checkout -q --detach $H
git -C $W remote set-url origin https://github.com/kebag-logic/milan-fpga.git
SRC=$G/docs-gates-0/wt
for p in gptp-processor protocol-processor third_party/tsn-c-stack third_party/verilog-axis; do
  name=$(git -C $W config -f .gitmodules --get-regexp '^submodule\..*\.path$' | awk -v p="$p" '$2==p{sub(/^submodule\./,"",$1); sub(/\.path$/,"",$1); print $1}')
  url=$(git -C $W config -f .gitmodules submodule."$name".url)
  git -C $W config submodule."$name".url "file://$SRC/.git/modules/$p"
  git -C $W -c protocol.file.allow=always submodule update -q --init -- "$p"
  test -e "$W/$p/.git" || { echo "submodule $p missing"; exit 3; }
  git -C $W/$p remote set-url origin "$url"
  git -C $W config submodule."$name".url "$url"
  printf '%s\t%s\t%s\n' "$p" "$(git -C $W/$p rev-parse HEAD)" "$(git -C $W/$p remote get-url origin)"
done > $LOGS/extra__submodules.txt
test "$(git -C $W rev-parse HEAD)" = "$H" || exit 4
test -z "$(git -C $W status --porcelain)" || exit 5
export PATH="$S/venv/bin:/usr/local/bin:/usr/bin:/bin" HOME=$S/home TMPDIR=$G/extra/tmp RUNNER_TEMP=$G/extra/runner_temp
cd $W
run() { local id="$1"; shift; { echo "# head $H lane step $id: $*"; ( set -o pipefail; timeout 900 bash -c "$*" ); } > $LOGS/lane__$id.log 2>&1; local rc=$?; echo $rc > $LOGS/lane__$id.rc; printf 'lane__%s\trc=%s\t%s\n' $id $rc "$(tail -1 $LOGS/lane__$id.log | cut -c1-140)"; }
DEVPAGES=$(git diff --name-only $R6 $H -- '*.md' | tr '\n' ' ')
BRPAGES=$(git diff --name-only $DEV $H -- '*.md' | tr '\n' ' ')
echo "$DEVPAGES" > $LOGS/lane__pages_merge_vs_r6.txt; echo "$BRPAGES" > $LOGS/lane__pages_merge_vs_dev.txt
run inventory_check "python3 scripts/docs_inventory.py --check"
run doc_style "python3 scripts/check_doc_style.py"
run style_blocks_vs_dev "python3 -I $S/tools/style_touched.py $W $DEV $BRPAGES"
run style_merge_new "python3 -I $S/tools/merge_style_probe.py $W $H"
run style_merge_new_control "! python3 -I $S/tools/merge_style_probe.py $W $H --control"
run behave "export PATH=$S/venv-behave/bin:\$PATH; cd tests && behave --no-capture -f plain"
run diffcheck_mergebase "git diff --check $DEV HEAD"
run diffcheck_oldbase "git diff --check $OLD HEAD"
run em_dash_mergebase "python3 scripts/check_em_dash.py --base $DEV"
run reader_check_baseline "python3 syn/ooc/pp_resource_gate.py check-baseline"
run reader_service_bounds "rm -rf $G/extra/sb_out && python3 -I $S/tools/service_bounds_arm.py $W $G/extra/sb_out"
run census_coverage "python3 -I $E/census_coverage.py $W $E/basis_soc_hierarchy.txt $E/basis_csr.csv $E/basis_place_top_excerpt.rpt"
C=$G/extra/control_r1; rm -rf $C; mkdir -p $C/docs/design $C/sw/litex
git show 3f8ed303:docs/design/MARK_II_AREA_PLAN.md > $C/docs/design/MARK_II_AREA_PLAN.md
cp sw/litex/milan_soc.py $C/sw/litex/
run census_coverage_control "! python3 -I $E/census_coverage.py $C $E/basis_soc_hierarchy.txt $E/basis_csr.csv $E/basis_place_top_excerpt.rpt"
git status --porcelain > $LOGS/lane__tree-after.txt
echo done > $LOGS/lane__DONE

#!/usr/bin/env bash
# Every docs-workflow step on the clean clone, sequentially (no parallel sweeps).
G=$VALIDATION_STORAGE/640-a720o/gates
echo $$ > $G/run_all.pid
date -Is > $G/run_all.start
cd $G
bash run_gates.sh a
bash run_gates.sh b
bash run_gates.sh c
bash run_gates.sh nogit
cd $G/wt
V=$VALIDATION_STORAGE/818-mdvenv/bin/python3
for step in "md818_docs_check:$V scripts/docs_check.py" "md818_em_dash:$V scripts/check_em_dash.py --base 503bc97cd4f24ad07596c17e7188f2024617972d" "md818_doc_style:$V scripts/check_doc_style.py" "md818_toc:$V scripts/gen_toc.py --selftest && $V scripts/gen_toc.py --verify-anchors && $V scripts/gen_toc.py --check" "diff_check:git diff --check 503bc97cd4f24ad07596c17e7188f2024617972d HEAD" "style_touched:python3 -I $VALIDATION_STORAGE/640-a720o/style_touched.py . 503bc97cd4f24ad07596c17e7188f2024617972d docs/design/MARK_II_AREA_PLAN.md docs/design/AREA_BUDGET.md docs/design/MAILBOX_SPLIT.md docs/findings/README.md && python3 -I $VALIDATION_STORAGE/640-a720o/style_touched.py . 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2 docs/design/MARK_II_AREA_PLAN.md"; do
  id=${step%%:*}; cmd=${step#*:}
  bash -c "$cmd" > $G/logs/$id.log 2>&1; rc=$?; echo $rc > $G/logs/$id.rc
  printf '%s\trc=%s\t%s\n' $id $rc "$(tail -1 $G/logs/$id.log | cut -c1-140)"
done
cd $G
STEP_TIMEOUT=900 bash run_gates.sh e_sdk
STEP_TIMEOUT=1500 bash run_gates.sh e_fw
STEP_TIMEOUT=2400 bash run_gates.sh e_b0
STEP_TIMEOUT=1500 bash run_gates.sh e_b1
git -C $G/wt status --short > $G/logs/final_status.txt
git -C $G/wt submodule status > $G/logs/final_submodules.txt
date -Is > $G/run_all.end
echo ALL_DONE

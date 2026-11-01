#!/usr/bin/env bash
# every docs-workflow step on the clean clone, sequentially
G=$VALIDATION_STORAGE/640-a720e/gates
cd $G
bash run_gates.sh a
bash run_gates.sh b
bash run_gates.sh c
bash run_gates.sh nogit
cd $G/wt
V=$VALIDATION_STORAGE/818-mdvenv/bin/python3
for step in "md818_docs_check:$V scripts/docs_check.py" "md818_em_dash:$V scripts/check_em_dash.py --base 1f29f189279f9fc0132f4918e47342b87d22f33a" "md818_doc_style:$V scripts/check_doc_style.py" "md818_toc:$V scripts/gen_toc.py --selftest && $V scripts/gen_toc.py --verify-anchors && $V scripts/gen_toc.py --check" "diff_check:git diff --check 1f29f189279f9fc0132f4918e47342b87d22f33a HEAD"; do
  id=${step%%:*}; cmd=${step#*:}
  bash -c "$cmd" > $G/logs/$id.log 2>&1; rc=$?; echo $rc > $G/logs/$id.rc
  printf '%s\trc=%s\t%s\n' $id $rc "$(tail -1 $G/logs/$id.log | cut -c1-140)"
done
cd $G
STEP_TIMEOUT=900 bash run_gates.sh e_sdk
STEP_TIMEOUT=1500 bash run_gates.sh e_fw
STEP_TIMEOUT=2400 bash run_gates.sh e_b0
STEP_TIMEOUT=1500 bash run_gates.sh e_b1
echo ALL_DONE

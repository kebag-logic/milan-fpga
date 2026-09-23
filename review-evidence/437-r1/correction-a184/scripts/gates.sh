#!/usr/bin/env bash
# Focused gates at the lane HEAD; each via rec.sh (log + exit row). At most 8 parallel.
set -u
OUT=$MANAGEMENT/2026-09-23/437-a184
cd $LANES/437-container-paragraph-scopes || exit 99
MB=$(git merge-base origin/dev HEAD)
cat > "$OUT/work/gates.list" <<LIST
toc-selftest python3 -B scripts/gen_toc.py --selftest
toc-check python3 -B scripts/gen_toc.py --check
toc-anchors python3 -B scripts/gen_toc.py --verify-anchors
toc-sites python3 -B scripts/gen_toc.py --sites
emdash-selftest python3 -B scripts/check_em_dash.py --selftest
emdash-base-mergebase python3 -B scripts/check_em_dash.py --base $MB
emdash-base-original python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896
docs-check python3 -B scripts/docs_check.py
docs-check-selftest python3 -B scripts/docs_check.py --selftest
doc-style python3 -B scripts/check_doc_style.py
doc-style-selftest python3 -B scripts/check_doc_style.py --selftest
doc-paths python3 -B scripts/check_doc_paths.py
py-idiom python3 -B scripts/check_py_idiom.py
py-idiom-selftest python3 -B scripts/check_py_idiom.py --selftest
hygiene python3 -B scripts/check_hygiene.py --check
hygiene-selftest python3 -B scripts/check_hygiene.py --selftest
naming python3 -B scripts/measure_naming.py --check
naming-selftest python3 -B scripts/measure_naming.py --selftest
fail-fast python3 -B scripts/measure_fail_fast.py --check
fail-fast-selftest python3 -B scripts/measure_fail_fast.py --selftest
test-evidence python3 -B scripts/measure_test_evidence.py --check
test-evidence-selftest python3 -B scripts/measure_test_evidence.py --selftest
control-flow-selftest python3 -B scripts/measure_control_flow.py --selftest
cohesion-selftest python3 -B scripts/measure_cohesion.py --selftest
todo-ownership python3 -B scripts/check_todo_ownership.py
todo-ownership-selftest python3 -B scripts/check_todo_ownership.py --selftest
ci-events python3 -B scripts/ci_events.py --check
ci-events-selftest python3 -B scripts/ci_events.py --selftest
feature-status python3 -B scripts/check_feature_status.py
solution-docs python3 -B scripts/check_solution_docs.py
submodule-docs python3 -B scripts/check_submodule_docs.py
gptp-docs python3 -B scripts/check_gptp_docs.py
archive python3 -B scripts/check_archive.py
LIST
xargs -P 8 -L 1 "$OUT/scripts/rec.sh" < "$OUT/work/gates.list"

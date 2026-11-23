#!/usr/bin/env bash
# The 24 docs and quality gates of round 2, run from the repo root given as $1.
# The em-dash gate runs under the scratch venv holding the pinned renderer ($2).
set -u
cd "$1"; venv_py=$2; base=854bd7236792ce1adbd10c43b13a6a5002ad3bb6; fail=0
run() { out=$("$@" 2>&1); rc=$?; [ $rc -ne 0 ] && fail=1; echo "== rc=$rc $* :: $(printf '%s' "$out" | tail -3 | tr '\n' ' ' | cut -c1-400)"; }
export PYTHONDONTWRITEBYTECODE=1
run python3 scripts/docs_check.py
run "$venv_py" scripts/check_em_dash.py --base $base
run python3 scripts/check_doc_style.py
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_baremetal_only.py --selftest
run python3 scripts/check_py_idiom.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_hygiene.py --check
run python3 scripts/measure_naming.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_feature_status.py
run python3 docs/traceability/gen_module_matrix.py --check
run python3 scripts/check_doc_paths.py
run python3 scripts/check_solution_docs.py
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_entity_shape.py
run python3 scripts/check_wire_accountability.py
run python3 scripts/check_nvm_record_space.py
run python3 scripts/check_nvm_klj3.py
run python3 scripts/check_sweep_shape.py
run "$venv_py" scripts/gen_toc.py --check
echo "DOCS GATES fail=$fail"; exit $fail

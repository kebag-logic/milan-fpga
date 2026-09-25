#!/usr/bin/env bash
# Composition gates for issue 559 / PR 564 candidate. Usage: run_gates.sh <repo> <outdir>
# Each gate runs in the foreground; its combined output goes to <outdir>/<name>.log
# and "<name> rc=<n>" is appended to <outdir>/SUMMARY.txt.
set -u
repo=$(cd "$1" && pwd); out=$2; mkdir -p "$out"; : > "$out/SUMMARY.txt"
cd "$repo"
parent=$(git rev-parse HEAD^1)
g() { name=$1; shift; ( "$@" ) > "$out/$name.log" 2>&1; rc=$?; echo "$name rc=$rc" | tee -a "$out/SUMMARY.txt"; }
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree}) parent1=$parent" > "$out/HEAD.txt"
g ci_events_check        python3 scripts/ci_events.py --check
g ci_events_selftest     python3 scripts/ci_events.py --selftest
g nvm_capture            python3 scripts/check_nvm_capture.py
g nvm_record_space       python3 scripts/check_nvm_record_space.py
g docs_check_git         python3 -B scripts/docs_check.py
g docs_check_gitdir_null env GIT_DIR=/dev/null python3 -B scripts/docs_check.py
g em_dash_parent         python3 scripts/check_em_dash.py --base "$parent"
g em_dash_srcbase        python3 scripts/check_em_dash.py --base "$(git merge-base HEAD^1 HEAD^2)"
g doc_style              python3 scripts/check_doc_style.py
g doc_style_selftest     python3 scripts/check_doc_style.py --selftest
g gen_toc_check          python3 scripts/gen_toc.py --check
g gen_toc_anchors        python3 scripts/gen_toc.py --verify-anchors
g gen_toc_selftest       python3 scripts/gen_toc.py --selftest
g doc_paths              python3 scripts/check_doc_paths.py
g doc_map                python3 docs/DOC_MAP.gen.py --check
g module_matrix          python3 docs/traceability/gen_module_matrix.py --check
g baremetal_check        python3 scripts/check_baremetal_only.py --check
g baremetal_selftest     python3 scripts/check_baremetal_only.py --selftest
g test_evidence_check    python3 scripts/measure_test_evidence.py --check
g test_evidence_selftest python3 scripts/measure_test_evidence.py --selftest
g naming_check           python3 scripts/measure_naming.py --check
g hygiene_check          python3 scripts/check_hygiene.py --check
g todo_ownership         python3 scripts/check_todo_ownership.py
g py_idiom               python3 scripts/check_py_idiom.py
g cpp_idiom              python3 scripts/check_cpp_idiom.py
g sh_idiom               python3 scripts/check_sh_idiom.py
g fail_fast_check        python3 scripts/measure_fail_fast.py --check
g sweep_shape            python3 scripts/check_sweep_shape.py --self-test
g diff_check_parent      git diff --check "$parent" HEAD

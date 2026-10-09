#!/usr/bin/env bash
# Reviewer subset of the documentation/script gates touching the changed files.
# usage: doc_subset.sh TREE MD_PYTHON OUTDIR BASE
set -u
tree=$1; md=$2; out=$3; base=$4
mkdir -p "$out"; cd "$tree" || exit 2
run() { name=$1; shift; "$@" > "$out/$name.log" 2>&1; echo "$name $?" | tee -a "$out/results.txt"; }
: > "$out/results.txt"
run em-dash "$md" scripts/check_em_dash.py --base "$base"
run doc-style "$md" scripts/check_doc_style.py
run doc-paths "$md" scripts/check_doc_paths.py
run toc-check "$md" scripts/gen_toc.py --check
run toc-anchors "$md" scripts/gen_toc.py --verify-anchors
run docs-check "$md" scripts/docs_check.py
run py-idiom python3 scripts/check_py_idiom.py
run sh-idiom python3 scripts/check_sh_idiom.py
run hygiene python3 scripts/check_hygiene.py --check
run todo-ownership python3 scripts/check_todo_ownership.py
run test-evidence python3 scripts/measure_test_evidence.py --check
run naming python3 scripts/measure_naming.py --check
run fail-fast python3 scripts/measure_fail_fast.py --check
run ci-events-check python3 scripts/ci_events.py --check
run pp-srcs-check python3 scripts/pp_srcs.py --check
run rtl-source-lists python3 scripts/check_rtl_source_lists.py
run cpp-idiom python3 scripts/check_cpp_idiom.py
git status --porcelain --untracked-files=no > "$out/git-status-after.txt"

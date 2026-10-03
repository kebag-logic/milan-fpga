#!/bin/bash
# gates.sh <tag>: the light gates at the lane head, from the physical /data
# worktree path, each to its own log, never piped; one "rc label" line each.
# Markdown gates with the pinned md venv; ratchets with the host python3.
set -u
tag=${1:-head}
R=$VALIDATION_STORAGE/629-a517/gates
MD=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python
mkdir -p "$R"
cd $LANES/629-m2-impl || exit 2
head=$(git rev-parse HEAD)
sum="$R/${tag}_gates.txt"
echo "head $head $(date -Is)" > "$sum"
gate() {  # gate <label> <command...>
  local label=$1; shift
  "$@" > "$R/${tag}_${label}.log" 2>&1
  echo "$? $label" >> "$sum"
}
gate md_docs_check            "$MD" scripts/docs_check.py
gate md_doc_style             "$MD" scripts/check_doc_style.py
gate md_toc_check             "$MD" scripts/gen_toc.py --check
gate md_toc_anchors           "$MD" scripts/gen_toc.py --verify-anchors
gate md_em_dash_1269cdaf      "$MD" scripts/check_em_dash.py --base 1269cdafb4bb964c757baae0f0c5a932d43f540b
gate md_em_dash_cdf49d1a      "$MD" scripts/check_em_dash.py --base cdf49d1a28527562888f0a903de51b6b15b1244f
gate md_em_dash_c1288648      "$MD" scripts/check_em_dash.py --base c12886486c1e4acf2003bfaba25db2a307446428
gate md_doc_paths             "$MD" scripts/check_doc_paths.py
gate diff_check_worktree      git diff --check
gate diff_check_c1288648      git diff --check c12886486c1e4acf2003bfaba25db2a307446428 HEAD
gate diff_check_1269cdaf      git diff --check 1269cdafb4bb964c757baae0f0c5a932d43f540b HEAD
gate diff_check_cdf49d1a      git diff --check cdf49d1a28527562888f0a903de51b6b15b1244f HEAD
gate test_evidence            python3 scripts/measure_test_evidence.py --check
gate hygiene                  python3 scripts/check_hygiene.py --check
gate py_idiom                 python3 scripts/check_py_idiom.py
gate sh_idiom                 python3 scripts/check_sh_idiom.py
gate cpp_idiom                python3 scripts/check_cpp_idiom.py
gate sv_idiom                 python3 scripts/check_sv_idiom.py
gate lint                     python3 scripts/lint_rtl.py --check
gate naming                   python3 scripts/measure_naming.py --check
gate port_contracts           python3 scripts/check_port_contracts.py
gate fail_fast                python3 scripts/measure_fail_fast.py --check
gate todo_ownership           python3 scripts/check_todo_ownership.py
gate rtl_source_lists         python3 scripts/check_rtl_source_lists.py
gate submodule_docs           python3 scripts/check_submodule_docs.py
gate boundaries               python3 docs/diagrams/submodule_boundaries.gen.py --check
gate baremetal_only           python3 scripts/check_baremetal_only.py --check
gate nvm_capture              python3 scripts/check_nvm_capture.py
gate ci_scope_selftest        python3 scripts/ci_scope.py --selftest
gate pp_srcs                  python3 scripts/pp_srcs.py --check --selftest
gate feature_status           python3 scripts/check_feature_status.py --self-test
echo "end $(date -Is) porcelain=$(git status --porcelain | wc -l)" >> "$sum"

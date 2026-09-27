#!/bin/sh
# Repository gates at the reviewed head, in a disposable clean copy.
# Usage: r329_gates.sh <clean-copy> <venv-python>   (base 831f94f4)
cd "$1" || exit 2
V=$2; B=831f94f4146cc45ec476f8c8dcf5afac7cd8eacf
run() { echo "### $*"; "$@" 2>&1 | grep -v 'frozen site'; echo "### rc=$? :: $*"; }
# note: rc printed is grep's when piped; record the real rc instead
run2() { echo "### $*"; out=$("$@" 2>&1); rc=$?; printf '%s\n' "$out" | grep -v 'frozen site' | tail -n 15; echo "### rc=$rc :: $*"; }
run2 git diff --check $B HEAD
run2 git diff --check 104c8a54b183cd9215ed1e3a2e1be1634f48d33d HEAD
run2 python3 -B scripts/docs_check.py
run2 $V scripts/check_em_dash.py --base $B
run2 python3 scripts/check_doc_style.py
run2 $V scripts/gen_toc.py --check
run2 $V scripts/gen_toc.py --verify-anchors
run2 python3 scripts/check_doc_paths.py
run2 $V docs/traceability/gen_module_matrix.py --check
run2 python3 scripts/check_rtl_source_lists.py
run2 python3 scripts/check_sv_idiom.py
run2 python3 scripts/lint_rtl.py --check
run2 python3 scripts/check_cpp_idiom.py
run2 python3 scripts/check_py_idiom.py
run2 python3 scripts/check_port_contracts.py
run2 python3 scripts/measure_naming.py --check
run2 python3 scripts/measure_test_evidence.py --check
run2 python3 scripts/ci_events.py --check
run2 python3 scripts/xvlog_gate.py --check
run2 python3 scripts/check_submodule_docs.py
run2 python3 scripts/check_diagram_pngs.py
run2 python3 docs/diagrams/submodule_boundaries.gen.py --check
run2 python3 scripts/check_nvm_capture.py

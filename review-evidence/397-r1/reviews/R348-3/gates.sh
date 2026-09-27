#!/bin/sh
# Composition gates for #397 on the merge-train candidate. Usage: gates.sh <clone> <receipt-dir>
# Runs each gate in the foreground and records rc plus full output.
set -u
R=$1; O=$2; mkdir -p "$O"; cd "$R" || exit 2
PARENT=10a5bf59a6a73e9b6487d9ea6f42669ce142ae25
SRCBASE=ac18b50968b12efe4d15c0a06301264b35656b31
: > "$O/summary.tsv"
g() { name=$1; shift; "$@" > "$O/$name.log" 2>&1; rc=$?; printf '%s\t%s\t%s\n' "$rc" "$name" "$*" >> "$O/summary.tsv"; }
g head git rev-parse HEAD HEAD^{tree}
g tool-python python3 -c 'import sys;print(sys.version)'
g tool-verilator verilator --version
g fsb-make make -C tb/verilator/fw_service_budget
g fsb-selftest python3 -B tb/verilator/fw_service_budget/run.py --self-test
g nvm-hosttest python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
g check-nvm-capture python3 -B scripts/check_nvm_capture.py
g feature-status python3 -B scripts/check_feature_status.py
g feature-status-self python3 -B scripts/check_feature_status.py --self-test
g pp-srcs python3 -B scripts/pp_srcs.py --check --selftest
g baremetal-only python3 -B scripts/check_baremetal_only.py --check
g baremetal-only-self python3 -B scripts/check_baremetal_only.py --selftest
g entity-shape-self python3 -B scripts/check_entity_shape.py --self-test
g docs-check python3 -B scripts/docs_check.py
g doc-paths python3 -B scripts/check_doc_paths.py
g doc-style python3 -B scripts/check_doc_style.py
g archive python3 -B scripts/check_archive.py
g toc-check python3 -B scripts/gen_toc.py --check
g toc-anchors python3 -B scripts/gen_toc.py --verify-anchors
g em-dash-parent python3 -B scripts/check_em_dash.py --base $PARENT
g em-dash-srcbase python3 -B scripts/check_em_dash.py --base $SRCBASE
g em-dash-self python3 -B scripts/check_em_dash.py --selftest
g solution-docs python3 -B scripts/check_solution_docs.py
g submodule-docs python3 -B scripts/check_submodule_docs.py
g todo-ownership python3 -B scripts/check_todo_ownership.py
g py-idiom python3 -B scripts/check_py_idiom.py
g cpp-idiom python3 -B scripts/check_cpp_idiom.py
g sh-idiom python3 -B scripts/check_sh_idiom.py
g hygiene python3 -B scripts/check_hygiene.py --check
g naming python3 -B scripts/measure_naming.py --check
g fail-fast python3 -B scripts/measure_fail_fast.py --check
g test-evidence python3 -B scripts/measure_test_evidence.py --check
g suite-shards-self python3 -B scripts/suite_shards.py --selftest
g ci-events-check python3 -B scripts/ci_events.py --check
g ci-events-self python3 -B scripts/ci_events.py --selftest
g ci-scope-self python3 -B scripts/ci_scope.py --selftest
g diff-check-parent git diff --check $PARENT HEAD
g diff-check-srcbase git diff --check $SRCBASE HEAD
g status git status --porcelain --untracked-files=all

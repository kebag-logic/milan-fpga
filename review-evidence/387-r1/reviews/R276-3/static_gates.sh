#!/usr/bin/env bash
# Composition static gates for #387 / PR #540 round R276-3.
# Usage: static_gates.sh <clone> <out-log>
# Runs, in the clone, the repository gates that read the files this
# composition changes (docs, TOC/anchors, em dash, gPTP docs, pins, diagrams,
# evidence/ratchet readers, CI event map). Each command's exit code is logged.
set -u
clone=${1:?clone}; out=${2:?log}
parent=5c51569bd269b73a82ab767290fea92c134e5d02
dev=50e78097564244c124e1ec30dd8821f83951ab06
srcbase=759da623072358afdb0e9d570a7b4b6a788492c9
cd "$clone" || exit 2
: > "$out"
fails=0
run() {
  printf '### %s\n' "$*" >> "$out"
  "$@" >> "$out" 2>&1
  rc=$?
  printf '### exit=%d :: %s\n\n' "$rc" "$*" >> "$out"
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  printf '%-4s %s\n' "$rc" "$*"
}
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')" | tee -a "$out"
run python3 -B scripts/docs_check.py
run python3 scripts/check_em_dash.py --base "$parent"
run python3 scripts/check_em_dash.py --base "$dev"
run python3 scripts/check_em_dash.py --base "$srcbase"
run python3 scripts/check_em_dash.py --selftest
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run python3 scripts/check_gptp_docs.py
run python3 scripts/check_gptp_docs.py --with-submodule
run python3 scripts/check_gptp_docs.py --selftest
run python3 docs/DOC_MAP.gen.py --check
run python3 docs/DOC_MAP.gen.py --selftest
run python3 docs/diagrams/timesync_chain.gen.py --check
run python3 docs/diagrams/timesync_chain.gen.py --selftest
run python3 docs/diagrams/submodule_boundaries.gen.py --check
run python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run python3 scripts/check_solution_docs.py
run python3 scripts/check_submodule_docs.py
run python3 scripts/check_submodule_docs.py --selftest
run python3 scripts/check_diagram_pngs.py
run python3 scripts/check_diagram_pngs.py --selftest
run python3 scripts/gen_toc.py --selftest
run python3 scripts/gen_toc.py --verify-anchors
run python3 scripts/gen_toc.py --check
run python3 scripts/check_feature_status.py
run python3 scripts/check_doc_paths.py
run python3 scripts/measure_test_evidence.py --check
run python3 scripts/check_rtl_source_lists.py
run python3 scripts/check_port_contracts.py
run python3 scripts/check_cpp_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/measure_naming.py --check
run python3 scripts/measure_fail_fast.py --check
run python3 scripts/check_baremetal_only.py --check
run python3 scripts/check_archive.py
run python3 scripts/ci_events.py --check
run python3 scripts/ci_events.py --selftest
run git diff --check "$parent" HEAD
run git diff --check "$dev" HEAD
echo "FAILED_GATES=$fails" | tee -a "$out"

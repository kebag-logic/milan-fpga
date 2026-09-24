#!/usr/bin/env bash
# Run the documentation gates named by PR #537 at the checked-out head.
# Usage: run_doc_gates.sh <repo-root> <receipt-dir>
# Each gate's stdout+stderr goes to <receipt-dir>/gate_<n>.txt with its exit code
# appended; a summary line per gate goes to <receipt-dir>/gates_summary.txt.
set -u
repo=$1
out=$2
mkdir -p "$out"
cd "$repo" || exit 2
summary="$out/gates_summary.txt"
: > "$summary"
printf 'head %s tree %s\n' "$(git rev-parse HEAD)" "$(git rev-parse 'HEAD^{tree}')" >> "$summary"

run() {
  local name=$1
  shift
  local log="$out/gate_${name}.txt"
  printf '$ %s\n' "$*" > "$log"
  timeout 1200 "$@" >> "$log" 2>&1
  local rc=$?
  printf 'exit=%s\n' "$rc" >> "$log"
  printf '%-28s exit=%-3s %s\n' "$name" "$rc" "$(grep -v '^exit=' "$log" | tail -n 1 | cut -c1-150)" >> "$summary"
}

run docs_check            python3 -B scripts/docs_check.py
run em_dash_base          python3 -B scripts/check_em_dash.py --base 759da623072358afdb0e9d570a7b4b6a788492c9
run em_dash_round         python3 -B scripts/check_em_dash.py --base 64bcf768d28b4b9763fbe5917a734bcefa2a66e0
run em_dash_selftest      python3 -B scripts/check_em_dash.py --selftest
run feature_status        python3 -B scripts/check_feature_status.py --self-test
run baremetal_only        python3 -B scripts/check_baremetal_only.py --check
run module_matrix         python3 -B docs/traceability/gen_module_matrix.py --check
run gptp_docs             python3 -B scripts/check_gptp_docs.py --with-submodule
run doc_style             python3 -B scripts/check_doc_style.py
run toc_check             python3 -B scripts/gen_toc.py --check
run toc_anchors           python3 -B scripts/gen_toc.py --verify-anchors
run doc_paths             python3 -B scripts/check_doc_paths.py
run submodule_docs        python3 -B scripts/check_submodule_docs.py
run solution_docs         python3 -B scripts/check_solution_docs.py
run wire_accountability   python3 -B scripts/check_wire_accountability.py
run diff_check_base       git diff --check 759da623072358afdb0e9d570a7b4b6a788492c9 HEAD
run diff_check_round      git diff --check 64bcf768d28b4b9763fbe5917a734bcefa2a66e0 HEAD
# Remaining documentation-workflow gates and self-tests
run doc_style_selftest     python3 -B scripts/check_doc_style.py --selftest
run gptp_docs_plain        python3 -B scripts/check_gptp_docs.py
run gptp_docs_selftest     python3 -B scripts/check_gptp_docs.py --selftest
run doc_map                python3 -B docs/DOC_MAP.gen.py --check
run timesync_diagram       python3 -B docs/diagrams/timesync_chain.gen.py --check
run solution_docs_selftest python3 -B scripts/check_solution_docs.py --selftest
run submodule_diagram      python3 -B docs/diagrams/submodule_boundaries.gen.py --check
run submodule_docs_selftest python3 -B scripts/check_submodule_docs.py --selftest
run diagram_pngs           python3 -B scripts/check_diagram_pngs.py
run baremetal_selftest     python3 -B scripts/check_baremetal_only.py --selftest

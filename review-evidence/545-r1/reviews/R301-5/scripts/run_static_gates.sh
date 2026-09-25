#!/usr/bin/env bash
# Run the static/documentation gates that read the files this candidate
# composes, against one checkout. Each gate's output goes to its own log; the
# summary TSV records gate name, exit status and wall seconds.
#
# usage: run_static_gates.sh <repo> <out-dir>
#   TOOLBIN (optional) is prepended to PATH: python3 with the pinned
#   Markdown lock, and the pinned verilator wrapper.
#   PARENT (default: HEAD^1) and DEV (optional) are the em-dash bases.
set -uo pipefail
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
[ -n "${TOOLBIN:-}" ] && export PATH="$TOOLBIN:$PATH"
cd "$repo" || exit 2
parent=${PARENT:-$(git rev-parse HEAD^1)}
summary="$out/summary.tsv"
printf 'gate\texit\tseconds\n' > "$summary"

run() { # <name> <command...>
  local name=$1; shift
  local t0 t1 rc
  t0=$(date +%s)
  "$@" > "$out/$name.log" 2>&1
  rc=$?
  t1=$(date +%s)
  printf '%s\t%s\t%s\n' "$name" "$rc" "$((t1 - t0))" >> "$summary"
  printf '%-44s exit %s (%ss)\n' "$name" "$rc" "$((t1 - t0))"
}

{
  echo "repo: $repo"
  echo "head: $(git rev-parse HEAD) tree: $(git rev-parse HEAD^{tree})"
  echo "parent base: $parent"
  echo "dev base: ${DEV:-unset}"
  echo "python3: $(command -v python3) $(python3 --version 2>&1)"
  echo "verilator: $(command -v verilator) $(verilator --version 2>&1)"
} > "$out/environment.txt"

run docs_check                python3 scripts/docs_check.py
run em_dash_parent            python3 scripts/check_em_dash.py --base "$parent"
[ -n "${DEV:-}" ] && run em_dash_dev python3 scripts/check_em_dash.py --base "$DEV"
run em_dash_selftest          python3 scripts/check_em_dash.py --selftest
run doc_style                 python3 scripts/check_doc_style.py
run doc_style_selftest        python3 scripts/check_doc_style.py --selftest
run gptp_docs                 python3 scripts/check_gptp_docs.py
run gptp_docs_selftest        python3 scripts/check_gptp_docs.py --selftest
run doc_map_check             python3 docs/DOC_MAP.gen.py --check
run timesync_chain_check      python3 docs/diagrams/timesync_chain.gen.py --check
run timesync_chain_selftest   python3 docs/diagrams/timesync_chain.gen.py --selftest
run submodule_diag_check      python3 docs/diagrams/submodule_boundaries.gen.py --check
run submodule_diag_selftest   python3 docs/diagrams/submodule_boundaries.gen.py --selftest
run submodule_docs            python3 scripts/check_submodule_docs.py
run submodule_docs_selftest   python3 scripts/check_submodule_docs.py --selftest
run diagram_pngs              python3 scripts/check_diagram_pngs.py
run diagram_pngs_selftest     python3 scripts/check_diagram_pngs.py --selftest
run feature_status            python3 scripts/check_feature_status.py
run feature_status_selftest   python3 scripts/check_feature_status.py --self-test
run module_matrix_check       python3 docs/traceability/gen_module_matrix.py --check
run solution_docs             python3 scripts/check_solution_docs.py
run nvm_capture               python3 scripts/check_nvm_capture.py
run rtl_source_lists          python3 scripts/check_rtl_source_lists.py
run port_contracts            python3 scripts/check_port_contracts.py
run naming_check              python3 scripts/measure_naming.py --check
run fail_fast_check           python3 scripts/measure_fail_fast.py --check
run todo_ownership            python3 scripts/check_todo_ownership.py
run test_evidence_check       python3 scripts/measure_test_evidence.py --check
run test_evidence_selftest    python3 scripts/measure_test_evidence.py --selftest
run hygiene_check             python3 scripts/check_hygiene.py --check
run sv_idiom                  python3 scripts/check_sv_idiom.py
run cpp_idiom                 python3 scripts/check_cpp_idiom.py
run py_idiom                  python3 scripts/check_py_idiom.py
run sh_idiom                  python3 scripts/check_sh_idiom.py
run ci_events_check           python3 scripts/ci_events.py --check
run ci_events_selftest        python3 scripts/ci_events.py --selftest
run doc_paths                 python3 scripts/check_doc_paths.py
run archive                   python3 scripts/check_archive.py
run gen_toc_selftest          python3 scripts/gen_toc.py --selftest
run gen_toc_verify_anchors    python3 scripts/gen_toc.py --verify-anchors
run gen_toc_check             python3 scripts/gen_toc.py --check
run pp_srcs_check             python3 scripts/pp_srcs.py --check
run lint_rtl_check            python3 scripts/lint_rtl.py --check
run lint_rtl_pragmas          python3 scripts/lint_rtl.py --pragmas
run xvlog_gate_check          python3 scripts/xvlog_gate.py --check

#!/usr/bin/env bash
# Run the parent's static/documentation gates that read processor files, each
# in the foreground, one receipt per gate, rc recorded. No gate is piped.
# Usage: parent_gates.sh <clone> <packet>
set -u
CLONE="$1"; PKT="$2"
OUT="$PKT/receipts/gates"; mkdir -p "$OUT"
export PATH="$PKT/scratch/bin:$PATH"
cd "$CLONE" || exit 2
SUMMARY="$OUT/SUMMARY.txt"; : > "$SUMMARY"
run() { # <name> <cmd...>
  local name="$1"; shift
  local t0=$SECONDS
  "$@" > "$OUT/$name.log" 2>&1
  local rc=$?
  printf '%-34s rc=%s  %ss  %s\n' "$name" "$rc" "$((SECONDS - t0))" "$*" >> "$SUMMARY"
}
run pp_srcs_check            python3 -B scripts/pp_srcs.py --check
run pp_srcs_selftest         python3 -B scripts/pp_srcs.py --selftest
run rtl_source_lists         python3 -B scripts/check_rtl_source_lists.py
run xvlog_gate_check         python3 -B scripts/xvlog_gate.py --check
run lint_rtl_check           python3 -B scripts/lint_rtl.py --check
run sv_idiom                 python3 -B scripts/check_sv_idiom.py
run cpp_idiom                python3 -B scripts/check_cpp_idiom.py
run py_idiom                 python3 -B scripts/check_py_idiom.py
run sh_idiom                 python3 -B scripts/check_sh_idiom.py
run port_contracts           python3 -B scripts/check_port_contracts.py
run measure_naming           python3 -B scripts/measure_naming.py --check
run measure_test_evidence    python3 -B scripts/measure_test_evidence.py --check
run todo_ownership           python3 -B scripts/check_todo_ownership.py
run hygiene                  python3 -B scripts/check_hygiene.py
run soc_sources              python3 -B scripts/check_soc_sources.py
run module_matrix            python3 -B docs/traceability/gen_module_matrix.py --check
run submodule_docs           python3 -B scripts/check_submodule_docs.py
run submodule_diagram        python3 -B docs/diagrams/submodule_boundaries.gen.py --check
run diagram_pngs             python3 -B scripts/check_diagram_pngs.py
run pp_integrator_params     python3 -B protocol-processor/scripts/check-integrator-params.py
run docs_check_git           python3 -B scripts/docs_check.py
run em_dash                  python3 -B scripts/check_em_dash.py --base 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a
run doc_style                python3 -B scripts/check_doc_style.py
run toc_check                python3 -B scripts/gen_toc.py --check
run toc_anchors              python3 -B scripts/gen_toc.py --verify-anchors
run doc_paths                python3 -B scripts/check_doc_paths.py
run ci_events                python3 -B scripts/ci_events.py --check
run diff_check_range         git diff --check 7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a HEAD
# metadata-free filesystem mode of the docs gate: archive export of HEAD
EXP="$PKT/scratch/export"; rm -rf "$EXP"; mkdir -p "$EXP"
git archive HEAD | tar -x -C "$EXP"
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  git -C "$s" archive HEAD | tar -x -C "$EXP/$s"
done
( cd "$EXP" && python3 -B scripts/docs_check.py ) > "$OUT/docs_check_nogit.log" 2>&1
printf '%-34s rc=%s  %s\n' docs_check_nogit "$?" "(archive export of HEAD, no .git)" >> "$SUMMARY"
cat "$SUMMARY"

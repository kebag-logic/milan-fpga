#!/usr/bin/env bash
# Run the static gates that read the files this PR and its predecessors both
# touch (and the docs-check steps generally) on the candidate tree, in
# parallel, one log and one rc file per gate.
# Usage: gates.sh <repo> <outdir> <base-for-em-dash> [python]
set -u
repo=$1; out=$2; base=$3; py=${4:-python3}
mkdir -p "$out"
cd "$repo" || exit 2
run() { # name, command...
  local name=$1; shift
  while [ "$(jobs -rp | wc -l)" -ge 16 ]; do wait -n; done
  ( "$@" >"$out/$name.log" 2>&1; echo $? >"$out/$name.rc" ) &
}
run docs_check            $py scripts/docs_check.py
run em_dash               $py scripts/check_em_dash.py --base "$base"
run doc_style             $py scripts/check_doc_style.py
run doc_style_self        $py scripts/check_doc_style.py --selftest
run gptp_docs             $py scripts/check_gptp_docs.py
run gptp_docs_self        $py scripts/check_gptp_docs.py --selftest
run gptp_docs_sub         $py scripts/check_gptp_docs.py --with-submodule
run doc_map               $py docs/DOC_MAP.gen.py --check
run doc_map_self          $py docs/DOC_MAP.gen.py --selftest
run timesync_chain        $py docs/diagrams/timesync_chain.gen.py --check
run timesync_chain_self   $py docs/diagrams/timesync_chain.gen.py --selftest
run solution_docs         $py scripts/check_solution_docs.py
run solution_docs_self    $py scripts/check_solution_docs.py --selftest
run submod_diag           $py docs/diagrams/submodule_boundaries.gen.py --check
run submod_diag_self      $py docs/diagrams/submodule_boundaries.gen.py --selftest
run submod_docs           $py scripts/check_submodule_docs.py
run submod_docs_self      $py scripts/check_submodule_docs.py --selftest
run diagram_pngs          $py scripts/check_diagram_pngs.py
run diagram_pngs_self     $py scripts/check_diagram_pngs.py --selftest
run feature_status        $py scripts/check_feature_status.py --self-test
run trace_matrix          $py docs/traceability/gen_module_matrix.py --check
run baremetal             $py scripts/check_baremetal_only.py --check
run baremetal_self        $py scripts/check_baremetal_only.py --selftest
run nvm_record_space      $py scripts/check_nvm_record_space.py
run nvm_record_space_self $py scripts/check_nvm_record_space.py --self-test
run nvm_capture           $py scripts/check_nvm_capture.py
run test_evidence         $py scripts/measure_test_evidence.py --check
run test_evidence_self    $py scripts/measure_test_evidence.py --selftest
run hygiene               $py scripts/check_hygiene.py --check
run hygiene_self          $py scripts/check_hygiene.py --selftest
run cpp_idiom             $py scripts/check_cpp_idiom.py
run cpp_idiom_self        $py scripts/check_cpp_idiom.py --selftest
run py_idiom              $py scripts/check_py_idiom.py
run py_idiom_self         $py scripts/check_py_idiom.py --selftest
run sh_idiom              $py scripts/check_sh_idiom.py
run sh_idiom_self         $py scripts/check_sh_idiom.py --selftest
run ci_events             $py scripts/ci_events.py --check
run ci_events_self        $py scripts/ci_events.py --selftest
run doc_paths             $py scripts/check_doc_paths.py
run toc_self              $py scripts/gen_toc.py --selftest
run toc_anchors           $py scripts/gen_toc.py --verify-anchors
run toc_check             $py scripts/gen_toc.py --check
run suite_shards_self     $py scripts/suite_shards.py --selftest
run diff_check            git diff --check "$base" HEAD
wait
for f in "$out"/*.rc; do printf '%s %s\n' "$(cat "$f")" "$(basename "$f" .rc)"; done | sort -k2 >"$out/SUMMARY.txt"
cat "$out/SUMMARY.txt"

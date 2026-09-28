#!/usr/bin/env bash
# Usage: static_gates.sh  (env: REPO, PKT). Runs the docs-workflow static gates,
# the ratchets, the CI event checker and the Markdown gates with the pinned
# Markdown environment ($PKT/scratch/mdenv), one at a time.
set -u
: "${REPO:?}" "${PKT:?}"
S=$PKT/scratch; R=$PKT/receipts/static
export PATH="$S/toolbin:$S/mdenv/bin:/usr/local/bin:/usr/bin" REPO
PARENT=1a3c716f6e9fbc1c3227bce0a287ac943944fcbb
SRCBASE=0eff6d2ee3818a6d2b1f1fdcd0084d81b28f247a
g() { "$PKT/scripts/run_gate.sh" "$R" "$@"; }
g diff_check_parent        300 git diff --check $PARENT HEAD
g em_dash_parent           900 python3 scripts/check_em_dash.py --base $PARENT
g em_dash_srcbase          900 python3 scripts/check_em_dash.py --base $SRCBASE
g em_dash_selftest         900 python3 scripts/check_em_dash.py --selftest
g docs_check               900 python3 scripts/docs_check.py
g feature_status           900 python3 scripts/check_feature_status.py
g gen_toc_verify_anchors   900 python3 scripts/gen_toc.py --verify-anchors
g gen_toc_check            900 python3 scripts/gen_toc.py --check
g gen_toc_selftest        1800 python3 scripts/gen_toc.py --selftest
g doc_style                600 python3 scripts/check_doc_style.py
g doc_style_selftest       600 python3 scripts/check_doc_style.py --selftest
g doc_paths                600 python3 scripts/check_doc_paths.py
g gptp_docs                600 python3 scripts/check_gptp_docs.py
g doc_map_check            600 python3 docs/DOC_MAP.gen.py --check
g timesync_chain_check     600 python3 docs/diagrams/timesync_chain.gen.py --check
g solution_docs            600 python3 scripts/check_solution_docs.py
g submodule_boundaries     600 python3 docs/diagrams/submodule_boundaries.gen.py --check
g submodule_docs           600 python3 scripts/check_submodule_docs.py
g diagram_pngs             600 python3 scripts/check_diagram_pngs.py
g baremetal_only_check     900 python3 scripts/check_baremetal_only.py --check
g baremetal_only_selftest  900 python3 scripts/check_baremetal_only.py --selftest
g nvm_record_space         600 python3 scripts/check_nvm_record_space.py
g soc_sources              600 python3 scripts/check_soc_sources.py
g rtl_source_lists         600 python3 scripts/check_rtl_source_lists.py
g pp_srcs_check            600 python3 scripts/pp_srcs.py --check
g naming_check             900 python3 scripts/measure_naming.py --check
g port_contracts           900 python3 scripts/check_port_contracts.py
g fail_fast_check          900 python3 scripts/measure_fail_fast.py --check
g todo_ownership           600 python3 scripts/check_todo_ownership.py
g test_evidence_check      900 python3 scripts/measure_test_evidence.py --check
g test_evidence_selftest   900 python3 scripts/measure_test_evidence.py --selftest
g hygiene_check            900 python3 scripts/check_hygiene.py --check
g sv_idiom                 900 python3 scripts/check_sv_idiom.py
g cpp_idiom                900 python3 scripts/check_cpp_idiom.py
g py_idiom                 900 python3 scripts/check_py_idiom.py
g sh_idiom                 900 python3 scripts/check_sh_idiom.py
g ci_events_check          900 python3 scripts/ci_events.py --check
g ci_events_selftest      3000 python3 scripts/ci_events.py --selftest
g ci_scope_selftest        900 python3 scripts/ci_scope.py --selftest
g archive_check            600 python3 scripts/check_archive.py
g lint_rtl_check          1800 python3 scripts/lint_rtl.py --check --jobs 2
g wire_accountability_st   900 python3 scripts/check_wire_accountability.py --self-test

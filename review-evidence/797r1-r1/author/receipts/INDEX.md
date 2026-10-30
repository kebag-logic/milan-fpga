# Receipts index

Generated from the files present; regenerate after adding a receipt.

| File | Bytes | sha256 | First line |
|---|---|---|---|
| `behave/counters_contract_milan.txt` | 31596 | `50bd8363472f0ced` | USING RUNNER: behave.runner:Runner |
| `behave/full-suite.txt` | 394 | `2ce6f2aec92dca80` | behave --no-capture -f plain (from tests/), full bdd-conformance suite at a8bcfba9426db350 |
| `command-table/walk-step-final-head.txt` | 289 | `81b5c604851564f6` | head a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| `command-table/walk-step-negative-control.txt` | 3068 | `665e6977dc17acaf` | Traceback (most recent call last): |
| `compare-old.txt` | 350 | `b483fc41a06cb6e7` | compared 227 old rows; 5 disagree |
| `export/aem_desc.json` | 266 | `ba08511e11780706` | { |
| `export/csr.csv` | 9035 | `d1ee95171613829b` | #-------------------------------------------------------------------------------- |
| `gates/00-build-the-validated-hdl-reference.txt` | 952 | `b6b824438915d406` | $ set -euo pipefail |
| `gates/04-link-health-wording-dead-reference-and-local-info-gate.txt` | 181 | `8842051f14b729cc` | $ python3 scripts/docs_check.py |
| `gates/05-added-line-em-dash-gate.txt` | 331 | `cb60656134f8288e` | $ python3 scripts/check_em_dash.py --base 1e80128f0a467b58bf884b7d9bf62e013a2fb141 |
| `gates/06-concise-audience-documentation-gate.txt` | 353 | `ee3496831264e8d0` | $ python3 scripts/check_doc_style.py |
| `gates/07-audience-diagram-no-drift-gate.txt` | 448 | `d29419a5075cf2eb` | $ python3 docs/DOC_MAP.gen.py --check |
| `gates/08-product-solution-source-fact-gate.txt` | 259 | `4193fa2c41ab3df3` | $ python3 scripts/check_solution_docs.py |
| `gates/09-verified-submodule-documentation-gate.txt` | 461 | `89335c351c63e012` | $ python3 docs/diagrams/submodule_boundaries.gen.py --check |
| `gates/10-hdl-timing-diagram-no-drift-gate.txt` | 595 | `53b712b22f455ae5` | $ python3 scripts/gen_wavedrom.py --selftest |
| `gates/11-published-diagram-png-gate.txt` | 236 | `168675d9bec83090` | $ python3 scripts/check_diagram_pngs.py |
| `gates/12-milan-feature-status-consistency-gate.txt` | 1575 | `9d1eb263cc86d943` | $ python3 scripts/check_feature_status.py --self-test |
| `gates/13-traceability-matrix-no-drift-gate.txt` | 196 | `616a77e63d121a1f` | $ python3 docs/traceability/gen_module_matrix.py --check |
| `gates/15-imported-gptp-documentation-gate.txt` | 2797 | `8a55bae14d47a05c` | $ python3 scripts/check_gptp_docs.py --with-submodule |
| `gates/16-code-quality-measurement-self-tests.txt` | 3415 | `b6a3b739240897eb` | $ python3 scripts/measure_control_flow.py --selftest |
| `gates/18-bare-metal-scope-gate.txt` | 239 | `108a6d774dd00d47` | $ python3 scripts/check_baremetal_only.py --check |
| `gates/19-install-and-verify-the-pinned-rv32-sdk.txt` | 7326 | `065e7b3b5122ecff` | $ set -euo pipefail |
| `gates/20-compiler-absent-firmware-controls.txt` | 50896 | `d9769472ce13ad4e` | $ set -euo pipefail |
| `gates/21-end-station-builder-gates.txt` | 120352 | `c25113932fa96bde` | $ python3 sw/builder/test_builder.py --require-rv32 |
| `gates/22-nvm-record-space-gate.txt` | 9897 | `5d858b609924f302` | $ python3 scripts/check_nvm_record_space.py |
| `gates/23-capture-measurement-census-and-clock-gate.txt` | 458 | `eecc456d5ae199f9` | $ python3 scripts/check_nvm_capture.py |
| `gates/24-saved-state-writer-gate.txt` | 23394 | `e14c06abc1434e1f` | $ python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test |
| `gates/25-soc-source-list-gate-vivado-would-fail-40-min-in-without-thi.txt` | 5056 | `d1419a182a418b75` | $ python3 scripts/check_soc_sources.py |
| `gates/26-rtl-source-list-drift-gate.txt` | 3572 | `bd74ed5669ad8c66` | $ python3 scripts/check_rtl_source_lists.py |
| `gates/27-boundary-unit-naming-ratchet.txt` | 40710 | `2f5465b55613de0c` | $ python3 scripts/measure_naming.py --check |
| `gates/28-port-contract-gate.txt` | 5155 | `99a0f31d50ce6996` | $ python3 scripts/check_port_contracts.py |
| `gates/29-fail-fast-ratchet.txt` | 12551 | `4ea6a5801dbd3e72` | $ python3 scripts/measure_fail_fast.py --check |
| `gates/30-todo-ownership-gate.txt` | 2860 | `758194c23e4b5ed1` | $ python3 scripts/check_todo_ownership.py |
| `gates/31-test-evidence-ratchet.txt` | 27662 | `11a5f5bf07942e66` | $ python3 scripts/measure_test_evidence.py --check |
| `gates/32-mechanical-hygiene-ratchet.txt` | 4081 | `18dcba367a0f439b` | $ python3 scripts/check_hygiene.py --check |
| `gates/33-systemverilog-idiom-gate.txt` | 3276 | `b346ce8d9e696918` | $ python3 scripts/check_sv_idiom.py |
| `gates/34-c-and-c-idiom-gate.txt` | 4014 | `b2da7238d555d7f7` | $ python3 scripts/check_cpp_idiom.py |
| `gates/35-python-idiom-gate.txt` | 3096 | `3b9f980fa02211cd` | $ python3 scripts/check_py_idiom.py |
| `gates/36-shell-idiom-gate.txt` | 2799 | `d6efa97f7bff894f` | $ python3 scripts/check_sh_idiom.py |
| `gates/37-ci-event-and-sha-contract-gate.txt` | 2835 | `07a8d1ec0c9995d4` | output too large for the receipt directory: 338439 bytes, sha256 a0796b39c56ee20d58f077c4b |
| `gates/38-local-act-runner-contract-gate.txt` | 123867 | `d8a96974340f4681` | $ python3 scripts/act_ci.py --selftest |
| `gates/39-doc-cited-path-gate.txt` | 159 | `e69cf796764de305` | $ python3 scripts/check_doc_paths.py |
| `gates/40-archive-integrity-gate.txt` | 229 | `0c4eb7604aee39aa` | $ python3 scripts/check_archive.py |
| `gates/41-per-page-contents-gate.txt` | 338 | `1d590322b8f81d8f` | $ python3 scripts/gen_toc.py --selftest |
| `gates/42-aem-store-generator-self-test.txt` | 3663 | `a16753235c793599` | $ python3 avdecc/gen_aem_store.py --self-test |
| `gates/43-sweep-build-shape-gate.txt` | 19663 | `e3bc66b686ad04ad` | $ python3 scripts/check_sweep_shape.py --self-test |
| `gates/44-deploy-shape-gate.txt` | 9297 | `67738e6405b8ca2b` | $ python3 scripts/check_deploy_shape.py --self-test |
| `gates/45-entity-shape-gate.txt` | 27737 | `d08406681cdfc11d` | $ python3 scripts/check_entity_shape.py --self-test |
| `gates/46-register-reference-freshness-gate.txt` | 1183 | `9a1831ccdb49a62f` | $ python3 scripts/gen_register_reference.py --check |
| `gates/47-ci-scheduling-and-evidence-controls.txt` | 135982 | `57febab262229464` | $ python3 scripts/ci_gate_workflows.py --check |
| `gates/49-advertised-vs-emitted-gate-green-since-2026-07-28-item-00.txt` | 5197 | `b1ec928845016d45` | $ python3 -m pip install --quiet pyyaml |
| `gates/50-strip-git-metadata-then-run-the-docs-gate.txt` | 334 | `bb228182042e574f` | $ test ! -e .git |
| `gates/HEAD.txt` | 41 | `c83ede0fb81820ac` | a8bcfba9426db350018c9cee95f4905fb364d8f0 |
| `gates/summary.tsv` | 2849 | `9d0f1d95e5edff70` | 0	docs-check	Build the validated HDL reference	rc=0	2s |
| `mutants/page-hand-edit.txt` | 377 | `9c09e7f28bfbfd81` | # mutant: page-hand-edit |
| `mutants/reset-value-change.txt` | 467 | `9ba187f952413e61` | # mutant: reset-value-change |
| `mutants/rtl-field-rename.txt` | 460 | `56bf0d7b85ee4495` | # mutant: rtl-field-rename |
| `mutants/soc-from-check.txt` | 385 | `52d90b877e7bcb69` | # SoC extract against the shipping export (fresh), then against an export copy with one ba |
| `mutants/unknown-field-description.txt` | 552 | `dcedc7039ea69fdb` | # mutant: unknown-field-description |
| `pages.txt` | 381 | `806a490eaa087003` | old page: git show 1e80128f:docs/reference/REGISTER_MAP.md |
| `submodules.txt` | 501 | `13c511195c8c341b` |  efeb541ae5fe1e078332d8462dca2fc2d9cb8db5 external (heads/main) |
| `survival.txt` | 1657 | `2f074c34d4890747` | fragments: 1612; present on the new page: 1600; missing: 12 |

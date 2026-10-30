# Receipts index

Generated from the files present; sha256 truncated to 16 hex digits.

| File | Bytes | sha256 | First line |
|---|---|---|---|
| `builder-bank/full-bank-attempt.txt` | 1206 | `73164aa8d99b8a77` | head 1548e659b6 (the lane's first commit; the builder and its tests are unchanged since ba |
| `builder-bank/leg-receipt.json` | 4642 | `f6281f4d74303e16` | {"inventory": ["test_soc_option_refusals", "test_commercial_timing_grade", "test_baremetal |
| `builder-bank/leg.log` | 3359 | `53d9a94054cf87ab` | head cb07597bc33106933c708a45f92c91f17a7a3e61 |
| `ci-inventory/01-head.log` | 211 | `4d2d1542b6615675` | $ CI_IMAGE_SHFMT=<scratch>/shfmt python3 scripts/ci_tool_inventory.py --check   (committed |
| `ci-inventory/02-base-drift.txt` | 467 | `b11147c4c9e545d3` | head cb07597bc33106933c708a45f92c91f17a7a3e61 |
| `ci-inventory/03-neutralised.log` | 280 | `4ffbc4424b1503f6` | $ CI_IMAGE_SHFMT=<scratch>/shfmt python3 scripts/ci_tool_inventory.py --check   (dev's own |
| `ci-inventory/04-without-pin-endstation_definition.gen.py.log` | 263 | `19b555e16609b197` | $ CI_IMAGE_SHFMT=<scratch>/shfmt python3 scripts/ci_tool_inventory.py --check   (as 03, wi |
| `ci-inventory/04-without-pin-gen_key_reference.py.log` | 241 | `8cbb901e9e368286` | $ CI_IMAGE_SHFMT=<scratch>/shfmt python3 scripts/ci_tool_inventory.py --check   (as 03, wi |
| `example/00-head.txt` | 46 | `964469b22274ae6a` | head cb07597bc33106933c708a45f92c91f17a7a3e61 |
| `example/00-snippet.yaml` | 259 | `bd041e2ed25d7a96` | streams: |
| `example/01-copy.log` | 79 | `3bc8b83a3872b662` | $ cp configs/endstation_ax7101_1x1_tdm8.yaml /tmp/endstation_try_2x2.yaml |
| `example/01-endstation_try_2x2.yaml` | 10980 | `606111fbf91d206b` | # SPDX-FileCopyrightText: 2026 Kebag Logic |
| `example/02-artifacts-2x2.sha256` | 880 | `75109ef9dbe158c6` | 3e4faba8c7ff0e11a82d3f4f81a0808ea4347e00505fc638ebd735945ec2ded7 8458 adp_shape_defaults.s |
| `example/02-build-2x2.log` | 916 | `778b5480840be0e9` | $ python3 sw/builder/endstation_builder.py /tmp/endstation_try_2x2.yaml -o /tmp/try |
| `example/02-build_plan-2x2.md` | 11882 | `2e45bc59281ba507` | # Build plan - endstation_try_2x2 |
| `example/03-build-8x8-refused.log` | 424 | `b1198acb65c96fa0` | $ python3 sw/builder/endstation_builder.py /tmp/endstation_try_8x8.yaml -o /tmp/try |
| `example/04-build-1x1-4ch.log` | 969 | `46c53db496148e98` | $ python3 sw/builder/endstation_builder.py /tmp/endstation_try_1x1_4ch.yaml -o /tmp/try |
| `example/04-build_plan-1x1-4ch.md` | 10814 | `0c25e03910cdd5e8` | # Build plan - endstation_try_1x1_4ch |
| `example/04-channels-edit.txt` | 133 | `4ad805c0c885e06b` | 220:    - { name: "Stream In 0", channels: 4, map_mode: dynamic } |
| `example/05-build_plan-1x1.md` | 10825 | `7b464617c041fa0d` | # Build plan - endstation_ax7101_1x1_tdm8 |
| `example/05-return-build.log` | 1156 | `681c705f8b18d527` | $ python3 sw/builder/endstation_builder.py configs/endstation_ax7101_1x1_tdm8.yaml --write |
| `example/05-return-git-status.log` | 26 | `c16209b5124835a7` | $ git status --short |
| `example/05-return-rm.log` | 51 | `1a4a645f3fd89bb5` | $ rm -r /tmp/endstation_try_2x2.yaml /tmp/try |
| `example/06-git-status-after.log` | 88 | `5d0e0806bf781975` | $ git status --short --ignored configs/generated sw/builder/out |
| `gates/00-summary.tsv` | 3481 | `e7854d005d844f81` | # head cb07597bc33106933c708a45f92c91f17a7a3e61; tree before run: clean |
| `gates/01-docs_check.log` | 165 | `c747c4a5c74e83cb` | $ python3 scripts/docs_check.py |
| `gates/02-docs_check-selftest.log` | 104 | `6779cf4f84c0e953` | $ python3 scripts/docs_check.py --selftest |
| `gates/03-check_doc_style.log` | 89 | `b761c578f473feee` | $ python3 scripts/check_doc_style.py |
| `gates/04-check_doc_style-selftest.log` | 86 | `a72faa1baf95c9fb` | $ python3 scripts/check_doc_style.py --selftest |
| `gates/05-check_em_dash.log` | 228 | `3f7f68da7b0362e2` | $ python3 scripts/check_em_dash.py --base 1e80128f0a467b58bf884b7d9bf62e013a2fb141 |
| `gates/06-check_em_dash-selftest.log` | 93 | `9b347bb51b52924b` | $ python3 scripts/check_em_dash.py --selftest |
| `gates/07-check_doc_paths.log` | 143 | `9f92448f2667a591` | $ python3 scripts/check_doc_paths.py |
| `gates/08-gen_toc-selftest.log` | 83 | `8dbd7115fd6e9656` | $ python3 scripts/gen_toc.py --selftest |
| `gates/09-gen_toc-verify-anchors.log` | 115 | `3bbf49832e67e187` | $ python3 scripts/gen_toc.py --verify-anchors |
| `gates/10-gen_toc-check.log` | 136 | `d02db4b640187a29` | $ python3 scripts/gen_toc.py --check |
| `gates/11-check_baremetal_only-check.log` | 127 | `f3899e21f281e832` | $ python3 scripts/check_baremetal_only.py --check |
| `gates/12-check_baremetal_only-selftest.log` | 101 | `b6cbdc60f11e11cf` | $ python3 scripts/check_baremetal_only.py --selftest |
| `gates/13-check_archive.log` | 133 | `4513c1119b50774c` | $ python3 scripts/check_archive.py |
| `gates/14-check_archive-selftest.log` | 86 | `9971acee3b1a2233` | $ python3 scripts/check_archive.py --selftest |
| `gates/15-check_diagram_pngs.log` | 111 | `81a4064508f65af5` | $ python3 scripts/check_diagram_pngs.py |
| `gates/16-check_diagram_pngs-selftest.log` | 115 | `0cef6e0e22f16f02` | $ python3 scripts/check_diagram_pngs.py --selftest |
| `gates/17-check_feature_status.log` | 76 | `e0f7494ad83fd972` | $ python3 scripts/check_feature_status.py |
| `gates/18-check_feature_status-selftest.log` | 1559 | `d602d175f1cf081e` | $ python3 scripts/check_feature_status.py --self-test |
| `gates/19-check_gptp_docs.log` | 83 | `7c2462101bdaefef` | $ python3 scripts/check_gptp_docs.py |
| `gates/20-check_gptp_docs-selftest.log` | 99 | `5f5492933a457390` | $ python3 scripts/check_gptp_docs.py --selftest |
| `gates/21-check_solution_docs.log` | 133 | `36cb0be7bd7e7820` | $ python3 scripts/check_solution_docs.py |
| `gates/22-check_solution_docs-selftest.log` | 116 | `f025b8a00d4114ad` | $ python3 scripts/check_solution_docs.py --selftest |
| `gates/23-DOC_MAP-check.log` | 104 | `7eb9d41d4add0ec9` | $ python3 docs/DOC_MAP.gen.py --check |
| `gates/24-DOC_MAP-selftest.log` | 106 | `b673d0a3a5e91376` | $ python3 docs/DOC_MAP.gen.py --selftest |
| `gates/25-timesync_chain-check.log` | 119 | `37b82cad6552b7bc` | $ python3 docs/diagrams/timesync_chain.gen.py --check |
| `gates/26-submodule_boundaries-check.log` | 119 | `5049c5e551ae6b76` | $ python3 docs/diagrams/submodule_boundaries.gen.py --check |
| `gates/27-check_submodule_docs.log` | 94 | `44f268a901fd0aa1` | $ python3 scripts/check_submodule_docs.py |
| `gates/28-gen_module_matrix-check.log` | 180 | `5bb831487e7201d2` | $ python3 docs/traceability/gen_module_matrix.py --check |
| `gates/29-gen_key_reference-check.log` | 100 | `cd5e2c8bf418c491` | $ python3 sw/builder/gen_key_reference.py --check |
| `gates/30-gen_key_reference-selftest.log` | 135 | `0488b09da3b25fa3` | $ python3 sw/builder/gen_key_reference.py --selftest |
| `gates/31-endstation_definition-check.log` | 122 | `780969c8ab2cb335` | $ python3 docs/diagrams/endstation_definition.gen.py --check |
| `gates/32-endstation_definition-selftest.log` | 147 | `f87e77cd1ae14142` | $ python3 docs/diagrams/endstation_definition.gen.py --selftest |
| `gates/33-check_entity_shape-selftest.log` | 27713 | `f6338eeea9d2ffbe` | $ python3 scripts/check_entity_shape.py --self-test |
| `gates/34-ci_gate_workflows-check.log` | 52 | `3eacd54ae4043c35` | $ python3 scripts/ci_gate_workflows.py --check |
| `gates/35-ci_gate_workflows_selftest.log` | 22449 | `872411742ff764c5` | $ python3 scripts/ci_gate_workflows_selftest.py |
| `gates/36-ci_events-check.log` | 211 | `826c3c3de095d613` | $ python3 scripts/ci_events.py --check |
| `gates/37-ci_events-selftest.log` | 12782 | `4ecc9b1a51872d64` | $ python3 scripts/ci_events.py --selftest |
| `gates/38-generate_ci_evidence_pins-check.log` | 60 | `1707eb94c36c78b9` | $ python3 scripts/generate_ci_evidence_pins.py --check |
| `gates/39-check_py_idiom.log` | 502 | `08e96767902137c9` | $ python3 scripts/check_py_idiom.py |
| `gates/40-check_py_idiom-selftest.log` | 2583 | `77d9f2dc3f8548f2` | $ python3 scripts/check_py_idiom.py --selftest |
| `gates/41-check_hygiene-check.log` | 2173 | `df0c5f30fe856b3a` | $ python3 scripts/check_hygiene.py --check |
| `gates/42-measure_naming-check.log` | 36622 | `260a5b9b3f0caaaa` | $ python3 scripts/measure_naming.py --check |
| `gates/43-measure_fail_fast-check.log` | 5889 | `0f7090d486499d8a` | $ python3 scripts/measure_fail_fast.py --check |
| `gates/44-measure_test_evidence-check.log` | 21697 | `14fb8d4c0c766752` | $ python3 scripts/measure_test_evidence.py --check |
| `gates/45-check_todo_ownership.log` | 208 | `dce5204687ca66a0` | $ python3 scripts/check_todo_ownership.py |
| `gates/46-nogit-docs_check.log` | 290 | `1fe0988e11cba8e6` | $ python3 scripts/docs_check.py   (in a git-free export of HEAD, no .git, no submodules) |
| `gates/47-nogit-check_feature_status.log` | 133 | `496054a8373b9a0f` | $ python3 scripts/check_feature_status.py   (in a git-free export of HEAD, no .git, no sub |
| `mutants/00-head.txt` | 41 | `772081a671f0c911` | cb07597bc33106933c708a45f92c91f17a7a3e61 |
| `mutants/00-summary.tsv` | 385 | `6667b062326b90ff` | mutant	rc	expected	verdict |
| `mutants/01-key-stale-page.log` | 771 | `653dd50bf6dcb1fe` | planted in sw/builder/README-parameters.md: |
| `mutants/02-key-builder-default-changed.log` | 339 | `f61b985b53f59246` | planted in sw/builder/endstation_builder.py: |
| `mutants/03-key-builder-limit-changed.log` | 401 | `93188690e9646dc3` | planted in sw/builder/endstation_builder.py: |
| `mutants/04-key-builder-message-changed.log` | 868 | `b6163c3c6a83ab50` | planted in sw/builder/endstation_builder.py: |
| `mutants/05-key-builder-new-key-without-entry.log` | 394 | `3e70fb2497c28773` | planted in sw/builder/endstation_builder.py: |
| `mutants/06-guide-stale-page.log` | 556 | `fc8338401576fb47` | planted in docs/guides/DEFINING_THE_END_STATION.md: |
| `mutants/07-guide-builder-threshold-changed.log` | 373 | `0ebe94e4f82fee10` | planted in sw/builder/endstation_builder.py: |
| `mutants/08-guide-consumer-renamed.log` | 301 | `d00fd4ebff2ba448` | planted in sw/litex/milan_soc.py: |
| `mutants/09-guide-model-table-row-dropped.log` | 328 | `b9f3068b9abcb048` | planted in docs/guides/DEFINING_THE_END_STATION.md: |
| `mutants/10-guide-cost-table-changed.log` | 407 | `cee69f20f20d1781` | planted in sw/builder/endstation_builder.py: |

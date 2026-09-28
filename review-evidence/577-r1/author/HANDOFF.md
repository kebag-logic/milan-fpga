# Issue #577 author handoff

Author: [A410]. Internal reviewer: [R384]. External reviewer: [R385].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/577#issuecomment-5865331676
Branch: `577-image-l6-l10`.
Base: `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
Head: `a53682ed38720de758006602a19f78c8e40d69da`.
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`.
Processor root verified before its Git read; pin: `16be6768f710e79450aace277abacd6c2c3336e5`.
Status: author work complete and ready for independent review; local commit only.

## Change list

| File:line | Change |
|---|---|
| `sw/builder/endstation_builder.py:2310` | Validate the completed packed blob before returning any image artifacts; translate named image errors to ConfigError. |
| `sw/builder/aem_image_checks.py:20` | Derive sampling-rate walk offset and bound from read-only microprogram assignments. |
| `sw/builder/aem_image_checks.py:39` | L10 offset, count, complete-word and exact-extent refusals. |
| `sw/builder/aem_image_checks.py:60` | L6 list bounds and distinct duplicate/gap/order refusals. |
| `sw/builder/aem_image_checks.py:82` | Read actual AEMI index rows, descriptor extents and every member. |
| `sw/builder/test_builder.py:27233` | Independent boundary/refusal fixture table. |
| `sw/builder/test_builder.py:27279` | Inject after successful loading; prove bytes survive packing; grade the emitter's exact reason. |
| `sw/builder/test_builder.py:27313` | Gate 36b: all five shipping images, four accepted controls and 13 negative cases. |
| `sw/builder/test_builder.py:27333` | Ten descriptor targets across two synthetic configurations, same-length stride members and repeated unequal-length runs. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89` | Updated L6 matrix row. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:93` | Updated L10 matrix row. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:181` | Image-boundary derivation and named refusal evidence. |
| `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:318` | F6 enforcement and remaining processor scope. |

## Image boundary and derivation

`_entity_model_image` calls the validator immediately after `gen_desc_image.build` returns.
The exact checked `blob` becomes `aem_desc.bin`. No expected value comes from
`_load_clocking`, `_validate_output_clock_sources`, YAML, overlay or packer report.
Both loader functions are AST-identical to the base. Their scope is unchanged.

| Measured field | Source and derivation |
|---|---|
| Image version | Big-endian header field at byte 4; accepts AEMI v1. |
| Index count/location | Header bytes 8 and 12; no fixed row count or location. |
| Configuration/type/count/length/base/stride | Each emitted 16-byte index row; walk every row and member. |
| Descriptor location | Row base plus member number times row stride. |
| Actual descriptor length | Row elem_len; slices exclude alignment padding. |
| Rate offset/count | Big-endian body fields at 140/142, IEEE 1722.1-2021 7.2.3. |
| Required rate offset/bound | Literal SSR_LIST_OFF/SSR_WALK_MAX assignments read from the pinned SET_SAMPLING_RATE microprogram. AST parsing never executes it. No copied builder maximum is used. |
| Full-word rate extent | Divide measured unpadded length minus the consumer's list start by sizeof big-endian u32. Partial remainder, missing words and extra words have distinct reasons. Pull bits remain part of each word. |
| Source offset/count | Big-endian body fields at 72/74, IEEE 1722.1-2021 7.2.32. |
| Source list | Exactly count u16 entries at the served offset, bounded by the actual descriptor length. |
| Required identity list | range(served count), independent of constructor contents. Classify duplicates, gaps and order separately. |

The image contains enough structure, so the assignment's STOP condition does not apply.
The generic packer remains responsible for generic integrity. The checker does not
claim every L1-L10 rule, source construction, runtime rate support, model evolution
or multi-configuration product support. Synthetic fixtures prove the reader's walk.
Processor issue 89 remains separate defence-in-depth work.

## Boundary and refusal cases

All cases use a successfully loaded shipping configuration. The test substitutes
a descriptor while the real packer runs, verifies its exact packed bytes, then
requires the builder's post-packing validator to produce the named result.

| Case | Packed fields / mutation | Result |
|---|---|---|
| One rate | offset 144, count 1, length 148 | accepted |
| Eight rates | offset 144, count 8, length 176; includes pull-bearing word 0x2000BB80 | accepted structurally |
| Identity sources | [0,1] | accepted |
| One source | [0] | accepted |
| Wrong offset | offset 143 with otherwise valid one-rate body | L10_OFFSET |
| Ninth rate | count 9, nine distinct complete words, length 180 | L10_COUNT |
| Count/extent mismatch | count 2, one complete word, length 148 | L10_COUNT_EXTENT |
| One byte short | count 1, length 147 | L10_PARTIAL_WORD |
| One word extra | count 1, length 152 | L10_EXTRA_WORDS |
| Reversed list | [1,0] | L6_ORDER |
| Gapped list | [0,2] | L6_GAP |
| Duplicate list | [0,0] | L6_DUPLICATE |
| Short audio header | length 143 | L10_HEADER |
| Short domain header | length 75 | L6_HEADER |
| Empty list | count 0 | L6_EMPTY |
| Short source list | final source is missing one byte | L6_EXTENT |
| List inside header | source offset 70 | L6_EXTENT |

The eight-rate fixture bypasses only model construction, never the new check.
It does not widen #478's loader scope or downstream supported-rate restrictions.

## Removed-check mutant table

`check_mutants.py` creates disposable single-module mutants outside the worktree.
It deletes exactly one named raising statement per mutant, then calls the same
committed `test_shipping_image_contract`. Each required-class mutant wrongly
accepts its invalid input and therefore fails the test. Additional defensive
mutants fail if their named reason falls through to a generic structural error.
No mutant changes the worktree or the processor sources.

| Removed check | Verdict | Test failure |
|---|---|---|
| L10_OFFSET | killed | gate 36b: wrong offset accepted; missing L10_OFFSET |
| L10_COUNT | killed | gate 36b: ninth rate accepted; missing L10_COUNT |
| L10_COUNT_EXTENT | killed | gate 36b: count exceeds extent accepted; missing L10_COUNT_EXTENT |
| L10_PARTIAL_WORD | killed | gate 36b: one byte short accepted; missing L10_PARTIAL_WORD |
| L10_EXTRA_WORDS | killed | gate 36b: one word extra accepted; missing L10_EXTRA_WORDS |
| L6_ORDER | killed | gate 36b: reversed sources accepted; missing L6_ORDER |
| L6_GAP | killed | gate 36b: source gap accepted; missing L6_GAP |
| L6_DUPLICATE | killed | gate 36b: duplicate source accepted; missing L6_DUPLICATE |
| L10_HEADER | killed | short audio header: wrong refusal aem_desc.bin: IMAGE_STRUCTURE: truncated packed field: unpack_from requires a buffer of at least 144 bytes for unpacking 4 bytes at offset 140 (actual buffer size is 143) |
| L6_HEADER | killed | short domain header: wrong refusal aem_desc.bin: IMAGE_STRUCTURE: truncated packed field: unpack_from requires a buffer of at least 76 bytes for unpacking 4 bytes at offset 72 (actual buffer size is 75) |
| L6_EMPTY | killed | gate 36b: empty sources accepted; missing L6_EMPTY |
| L6_EXTENT | killed | short source list: wrong refusal aem_desc.bin: IMAGE_STRUCTURE: truncated packed field: unpack_from requires a buffer of at least 80 bytes for unpacking 4 bytes at offset 76 (actual buffer size is 79) |
| emitter hook removed | killed | gate 36b: wrong offset accepted; missing L10_OFFSET |

## Five-configuration results

`check_images.py` loads the assigned base's builder source in memory without
creating another checkout. The unchanged producers and source configurations
are shared; it compares each complete base image with the checked head image.
No binary images or tree exports are retained here.

| Configuration | Image bytes | Rate offset/count/length | Sources | Compared with base | SHA-256 |
|---|---:|---|---|---|---|
| arty_current | 5792 | 144/3/156 | [0, 1] | identical | `ac833c3ccde42a2d9a78b517d660b9f7da03c4b3d31227aa65dcaf9e8def6192` |
| arty_4x4 | 10112 | 144/1/148 | [0, 1] | identical | `1b288e13ccbf03410c593a53bc22f4a68e3d289eef8a7f907e63bc98a51415ff` |
| arty_8ch | 15360 | 144/1/148 | [0, 1] | identical | `2b5c008cf3a2ff1eca11ef5e24c5a2e391e97f25435854430e563758de516b9b` |
| ax7101_8x8 | 18288 | 144/1/148 | [0, 1] | identical | `193bf18736d23256c1b25d9af1bddb0721d95780fb36a14cf5f91476aff1a2d4` |
| ax7101_1x1_tdm8 | 7352 | 144/1/148 | [0, 1] | identical | `9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404` |

Every CLOCK_DOMAIN has source offset/count/length 76/2/80.
arty_current retains 48000/96000/192000; the other four retain 48000.

## Gate table

Commands run in the foreground from `$LANES/577-image-l6-l10`.
`run_gates.py` records each command, head, exit status, elapsed time, log size
and SHA-256. Commands are never piped. Each has a 7200-second timeout.
`/tmp/milan-577-venv/bin/python` is Python 3.14 with the repository's hash-locked
Markdown and HDL parser dependencies; no environment or installed packages
live in this output directory. Full logs over 200000 bytes are represented
by size/hash and a bounded tail only.

Only successful final-head receipts below count as evidence. Superseded or
setup-refused attempts remain separately recorded and do not count as passes.

| Receipt | Exact command | rc | Log |
|---|---|---:|---|
| builder-01 | `/tmp/milan-577-venv/bin/python -u sw/builder/test_builder.py --require-rv32` | 0 | builder-01.log |
| builder-02 | `/tmp/milan-577-venv/bin/python -u sw/builder/test_firmware_compiler.py --selftest` | 0 | builder-02.log |
| builder-03 | `/tmp/milan-577-venv/bin/python -u sw/builder/test_firmware_compiler.py --absent --audit /tmp/milan-577-absent.jsonl` | 0 | builder-03.log |
| docs-01 | `/tmp/milan-577-venv/bin/python -u scripts/docs_check.py` | 0 | docs-01.log |
| docs-02 | `GIT_DIR=/dev/null /tmp/milan-577-venv/bin/python -u scripts/docs_check.py` | 0 | docs-02.log |
| docs-03 | `/tmp/milan-577-venv/bin/python -u scripts/check_em_dash.py --base 54ce877371ee6e8878cf67294e86c2a8481b62f6` | 0 | docs-03.log |
| docs-04 | `/tmp/milan-577-venv/bin/python -u scripts/check_doc_style.py` | 0 | docs-04.log |
| docs-05 | `/tmp/milan-577-venv/bin/python -u scripts/check_doc_style.py --selftest` | 0 | docs-05.log |
| docs-06 | `/tmp/milan-577-venv/bin/python -u scripts/gen_toc.py --check` | 0 | docs-06.log |
| docs-07 | `/tmp/milan-577-venv/bin/python -u scripts/gen_toc.py --verify-anchors` | 0 | docs-07.log |
| docs-08 | `/tmp/milan-577-venv/bin/python -u scripts/gen_toc.py --selftest` | 0 | docs-08.log |
| docs-09 | `/tmp/milan-577-venv/bin/python -u scripts/check_doc_paths.py` | 0 | docs-09.log |
| docs-10 | `/tmp/milan-577-venv/bin/python -u scripts/check_feature_status.py --self-test` | 0 | docs-10.log |
| docs-11 | `/tmp/milan-577-venv/bin/python -u docs/traceability/gen_module_matrix.py --check` | 0 | docs-11.log |
| docs-12 | `/tmp/milan-577-venv/bin/python -u scripts/check_gptp_docs.py --with-submodule` | 0 | docs-12.log |
| docs-13 | `/tmp/milan-577-venv/bin/python -u scripts/check_gptp_docs.py --selftest` | 0 | docs-13.log |
| docs-14 | `/tmp/milan-577-venv/bin/python -u scripts/check_solution_docs.py` | 0 | docs-14.log |
| docs-15 | `/tmp/milan-577-venv/bin/python -u scripts/check_solution_docs.py --selftest` | 0 | docs-15.log |
| docs-16 | `/tmp/milan-577-venv/bin/python -u scripts/check_submodule_docs.py` | 0 | docs-16.log |
| docs-17 | `/tmp/milan-577-venv/bin/python -u scripts/check_submodule_docs.py --selftest` | 0 | docs-17.log |
| docs-18 | `/tmp/milan-577-venv/bin/python -u scripts/check_archive.py` | 0 | docs-18.log |
| docs-19 | `/tmp/milan-577-venv/bin/python -u scripts/check_archive.py --selftest` | 0 | docs-19.log |
| docs-20 | `/tmp/milan-577-venv/bin/python -u scripts/ci_events.py --check` | 0 | docs-20.log |
| docs-21 | `/tmp/milan-577-venv/bin/python -u scripts/ci_events.py --selftest` | 0 | docs-21.log |
| docs-22 | `/tmp/milan-577-venv/bin/python -u scripts/check_py_idiom.py` | 0 | docs-22.log |
| docs-23 | `/tmp/milan-577-venv/bin/python -u scripts/check_py_idiom.py --selftest` | 0 | docs-23.log |
| docs-24 | `/tmp/milan-577-venv/bin/python -u scripts/check_baremetal_only.py --check` | 0 | docs-24.log |
| docs-25 | `/tmp/milan-577-venv/bin/python -u scripts/check_baremetal_only.py --selftest` | 0 | docs-25.log |
| docs-26 | `/tmp/milan-577-venv/bin/python -u scripts/check_rtl_source_lists.py` | 0 | docs-26.log |
| docs-27 | `/tmp/milan-577-venv/bin/python -u scripts/check_rtl_source_lists.py --selftest` | 0 | docs-27.log |
| docs-28 | `/tmp/milan-577-venv/bin/python -u scripts/check_port_contracts.py` | 0 | docs-28.log |
| docs-29 | `/tmp/milan-577-venv/bin/python -u scripts/check_port_contracts.py --selftest` | 0 | docs-29.log |
| docs-30 | `/tmp/milan-577-venv/bin/python -u scripts/measure_naming.py --check` | 0 | docs-30.log |
| docs-31 | `/tmp/milan-577-venv/bin/python -u scripts/measure_naming.py --selftest` | 0 | docs-31.log |
| docs-32 | `/tmp/milan-577-venv/bin/python -u scripts/measure_fail_fast.py --check` | 0 | docs-32.log |
| docs-33 | `/tmp/milan-577-venv/bin/python -u scripts/measure_fail_fast.py --selftest` | 0 | docs-33.log |
| docs-34 | `/tmp/milan-577-venv/bin/python -u scripts/check_todo_ownership.py` | 0 | docs-34.log |
| docs-35 | `/tmp/milan-577-venv/bin/python -u scripts/check_todo_ownership.py --selftest` | 0 | docs-35.log |
| docs-36 | `/tmp/milan-577-venv/bin/python -u scripts/measure_test_evidence.py --check` | 0 | docs-36.log |
| docs-37 | `/tmp/milan-577-venv/bin/python -u scripts/measure_test_evidence.py --selftest` | 0 | docs-37.log |
| docs-38 | `/tmp/milan-577-venv/bin/python -u scripts/check_hygiene.py --check` | 0 | docs-38.log |
| docs-39 | `/tmp/milan-577-venv/bin/python -u scripts/check_hygiene.py --selftest` | 0 | docs-39.log |
| docs-40 | `/tmp/milan-577-venv/bin/python -u scripts/check_sv_idiom.py` | 0 | docs-40.log |
| docs-41 | `/tmp/milan-577-venv/bin/python -u scripts/check_sv_idiom.py --selftest` | 0 | docs-41.log |
| docs-42 | `/tmp/milan-577-venv/bin/python -u scripts/check_cpp_idiom.py` | 0 | docs-42.log |
| docs-43 | `/tmp/milan-577-venv/bin/python -u scripts/check_cpp_idiom.py --selftest` | 0 | docs-43.log |
| docs-44 | `/tmp/milan-577-venv/bin/python -u scripts/measure_control_flow.py --selftest` | 0 | docs-44.log |
| docs-45 | `/tmp/milan-577-venv/bin/python -u scripts/measure_cohesion.py --selftest` | 0 | docs-45.log |
| docs-46 | `/tmp/milan-577-venv/bin/python -u avdecc/gen_aem_store.py --self-test` | 0 | docs-46.log |
| docs-47 | `/tmp/milan-577-venv/bin/python -u scripts/check_entity_shape.py --self-test` | 0 | docs-47.log |
| docs-48 | `/tmp/milan-577-venv/bin/python -u scripts/check_wire_accountability.py --self-test` | 0 | docs-48.log |
| diagrams-01 | `/tmp/milan-577-venv/bin/python -u docs/DOC_MAP.gen.py --check` | 0 | diagrams-01.log |
| diagrams-02 | `/tmp/milan-577-venv/bin/python -u docs/DOC_MAP.gen.py --selftest` | 0 | diagrams-02.log |
| diagrams-03 | `/tmp/milan-577-venv/bin/python -u docs/diagrams/timesync_chain.gen.py --check` | 0 | diagrams-03.log |
| diagrams-04 | `/tmp/milan-577-venv/bin/python -u docs/diagrams/timesync_chain.gen.py --selftest` | 0 | diagrams-04.log |
| diagrams-05 | `/tmp/milan-577-venv/bin/python -u docs/diagrams/submodule_boundaries.gen.py --check` | 0 | diagrams-05.log |
| diagrams-06 | `/tmp/milan-577-venv/bin/python -u docs/diagrams/submodule_boundaries.gen.py --selftest` | 0 | diagrams-06.log |
| diagrams-07 | `/tmp/milan-577-venv/bin/python -u scripts/gen_wavedrom.py --selftest` | 0 | diagrams-07.log |
| diagrams-08 | `/tmp/milan-577-venv/bin/python -u scripts/gen_wavedrom.py docs/diagrams/wd_axis_backpressure.json --background=white --check` | 0 | diagrams-08.log |
| diagrams-09 | `/tmp/milan-577-venv/bin/python -u scripts/gen_wavedrom.py docs/diagrams/wd_cdc_handshake.json --background=white --check` | 0 | diagrams-09.log |
| diagrams-10 | `/tmp/milan-577-venv/bin/python -u scripts/gen_wavedrom.py docs/diagrams/wd_gptp_pdelay.json --background=white --check` | 0 | diagrams-10.log |
| diagrams-11 | `/tmp/milan-577-venv/bin/python -u scripts/check_diagram_pngs.py` | 0 | diagrams-11.log |
| diagrams-12 | `/tmp/milan-577-venv/bin/python -u scripts/check_diagram_pngs.py --selftest` | 0 | diagrams-12.log |
| parser-01 | `/tmp/milan-577-venv/bin/python -u scripts/gen_hdl_reference.py --selftest` | 0 | setup-retries/parser-01.log |
| diagrams-14 | `/tmp/milan-577-venv/bin/python -u scripts/check_sh_idiom.py` | 0 | diagrams-14.log |
| diagrams-15 | `/tmp/milan-577-venv/bin/python -u scripts/check_sh_idiom.py --selftest` | 0 | diagrams-15.log |
| reference-01 | `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.commitGraph GIT_CONFIG_VALUE_0=false /tmp/milan-577-venv/bin/python -u scripts/gen_hdl_reference.py --output /tmp/milan-577-hdl-reference` | 0 | reference-01.log |
| focused-01 | `/tmp/milan-577-venv/bin/python -u $MANAGEMENT/2026-09-23/577-a410/check_mutants.py` | 0 | focused-01.log |
| focused-02 | `/tmp/milan-577-venv/bin/python -u $MANAGEMENT/2026-09-23/577-a410/check_images.py` | 0 | focused-02.log |

## Evidence limits and reruns

The first head's wording gate rejected a generic processor phrase. The final
head names SET_SAMPLING_RATE precisely. The interrupted old-head builder runs
and old documentation receipts are under `superseded-head`; none clear a gate.
The HDL parser self-test initially refused its missing pinned package. After
installing the lock outside this output directory, the self-test passed.
HDL reference generation initially interpreted Git's missing commit-graph
warning as a dirty-tree signal. Its successful rerun disables that optional
Git acceleration through per-command configuration, without changing Git data
or repository files. Setup attempts are recorded under `setup-retries`.

All 69 final-head command receipts return rc 0. The complete builder reports
ALL GATES PASS EXCEPT 1 NOT RUN: gate 11 needs the absent placement calibration
report. Its compiler-backed instruments ran. The deliberately compiler-absent
run also returns 0 and records its three compiler-dependent instruments as one
NOT RUN arm, with zero actual firmware compiler invocations. That absence is
not counted as evidence of those instruments. No-Git documentation mode reports
its expected inventory-parity skip. Neither exclusion is new F6 evidence.

The final worktree is clean. `integrity.json` records the four changed files,
unchanged gitlinks and whitespace gate. `processor-integrity.json` proves the
read-only walk source matches its pin. The commit subject has no body or trailers.
The public REVIEW READY handoff names this exact head. No independent review
verdict is claimed by the author.
Independent review, publication, hosted/candidate validation and merge remain
outside this author's assignment. No push, PR operation, merge, hardware,
firmware, processor source, gitlink or RTL change was made.

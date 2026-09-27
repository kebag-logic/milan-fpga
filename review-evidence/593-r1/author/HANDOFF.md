# [A377] Issue #593 handoff

Status: implementation complete; ready for independent review.
Head: `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`
Commit subject: Enforce recorded mr causes and tu hold timing in release soak
Branch: `593-mr-tu-soak`
Base: `6d5ebd7357c1e468e446f18a61527c5be6118a04`
Origin verified: `https://github.com/kebag-logic/milan-fpga.git`
Working directory: `$LANES/593-mr-tu-soak`
Executor: [A377]. Internal reviewer: [R362]. External reviewer: [R363].

## Public contract

- [Issue #593](https://github.com/kebag-logic/milan-fpga/issues/593)
- [Assignment](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5858876858)
- [Original decision, superseded](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857762351)
- [Corrected governing decision](https://github.com/kebag-logic/milan-fpga/issues/396#issuecomment-5857765949)
- [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/593#issuecomment-5858887833)

Only the assigned desk work is complete. Physical release qualification
still requires the recorded campaigns. Independent review remains pending.

## Change list

| File:line | Change |
|---|---|
| `REQUIREMENTS.md:262` | Recorded mr causes, per-stream hold and MEDIA_RESET correlation |
| `REQUIREMENTS.md:288` | Resolution-aware GM minimum and corrected decision |
| `docs/testing/TESTING.md:915` | Soak assertions and evidence schema |
| `docs/testing/TESTING.md:945` | Derived timestamp and counter-update windows |
| `docs/testing/TESTING.md:990` | Explicit GM history and tu timing verdict |
| `tb/tools/torture_campaign.py:3388` | Mandatory mr assertion in every soak plan |
| `tb/tools/torture_campaign.py:3553` | tu containment, last-event deadline and GM minimum |
| `tb/tools/torture_campaign.py:3593` | Record validation and per-stream packet checks |
| `tb/tools/torture_campaign.py:3634` | Distinct caused toggles back MEDIA_RESET increments |
| `tb/tools/torture_campaign.py:3657` | Public mr evidence oracle |
| `tb/tools/torture_campaign.py:3694` | Plan requires packet, cause, counter and GM evidence |
| `tb/tools/torture_campaign.py:4096` | NOT RUN is counted and prevents a successful exit |
| `tb/tools/torture_campaign.py:5402` | Twelve new self-test methods |
| `tb/tools/torture_release_mutants.py:99` | Nineteen new mutation controls; prior twenty-five retained |
| `tests/steps/torture_release_steps.py:115` | Expanded evidence contract |
| `tests/steps/torture_release_steps.py:269` | Explicit accepted discontinuities and GM history |

## Rule-to-check map

| Rule and clause | Executable check and boundary |
|---|---|
| mr causes: IEEE 1722-2016 4.4.4.3; corrected #396 decision | `_release_mr_toggles`: recorded source change, CRF disruption, or received CRF mr toggle mapped to the affected stream |
| GM alone cannot excuse mr: corrected #396 decision; Milan v1.2 Annex B.1.2 | Allowed-cause filter excludes GM identity and PHC step events; B.1.2's conditional media-lock rule is not restated as an unconditional lock rule |
| Eight AVTPDUs: IEEE 1722-2016 4.4.4.3 | Consecutive, unwrapped indices of the toggling stream; next toggle index minus previous toggle index must be at least eight; terminal tail needs eight observed PDUs |
| MEDIA_RESET intervals: Milan v1.2 Tables 5.4/5.6 | `_release_media_resets`: each increment consumes a distinct cause-correlated wire toggle; several toggles can share one update interval |
| Cause coincidence: #593 assignment | R is recorded relative event/capture uncertainty, including launch latency; match in `[toggle - R, toggle + R]` |
| Deferred counter update: Milan Tables 5.4/5.6 | Adjacent-read matching window is `[before - 1 - R, after + R]`; one second comes from the device observation-interval ceiling, not periodic polling |
| tu event containment: IEEE 1722-2016 4.4.4.7; #396 rounds 4/5 | GM identity, GM time-source change, or another detected gPTP discontinuity must fall in `[observed_start - R, clear)` |
| tu upper bound: corrected #396 decision | Clear no later than last contained discontinuity + 0.5 s + R |
| tu GM minimum: Milan v1.2 Annex B.1.1; corrected #396 decision | Clear + R must reach latest preceding GM change + 0.25 s; later PHC steps affect the upper-bound anchor |
| Missing evidence: #593 assignment | NOT RUN; explicit empty complete histories differ from absent histories; resolution appears in verdict detail |

Timestamp comparisons use decimal representations to preserve inclusive decimal
boundaries. PDU indices and counter arithmetic remain integers. Counter reads
are evaluated separately for each descriptor; unsigned 32-bit wrap is decoded.
The caller's completeness attestation covers capture gaps, counter windows,
source mapping, common clock correlation, the baseline and the hold tail.
The oracle does not infer provenance from periodic healthy samples.

The cited PDF locations were read directly: IEEE PDF pages 36-37
(printed pages 24-25), Milan PDF page 141 (printed page 134), and
MEDIA_RESET rows on PDF pages 40 and 44 (Tables 5.4/5.6).
No standard extracts are copied into the deliverables.

## Self-test arm table

All 66 planner self-tests pass at the head above.
The twelve added methods contain independent positive, negative and boundary arms.

| Method | File:line | Arm purpose | Result |
|---|---|---|---|
| `test_release_mr_allowed_causes` | `tb/tools/torture_campaign.py:5420` | Each allowed clock cause independently explains a toggle and reset. | PASS |
| `test_release_mr_no_cause` | `tb/tools/torture_campaign.py:5430` | A complete empty cause history cannot excuse an observed toggle. | PASS |
| `test_release_mr_gm_only` | `tb/tools/torture_campaign.py:5434` | A GM edge or PHC step alone is not a media-clock-source change. | PASS |
| `test_release_mr_resolution` | `tb/tools/torture_campaign.py:5440` | A measured relative timestamp bound controls both matching edges. | PASS |
| `test_release_mr_stream_scope` | `tb/tools/torture_campaign.py:5453` | Neither another stream's cause nor its PDUs can satisfy this stream. | PASS |
| `test_release_mr_eight_pdus` | `tb/tools/torture_campaign.py:5465` | Seven PDUs fails; exactly eight passes, including a falling toggle. | PASS |
| `test_release_media_reset_no_cause` | `tb/tools/torture_campaign.py:5475` | A counter increase without a caused wire toggle must fail. | PASS |
| `test_release_media_reset_intervals` | `tb/tools/torture_campaign.py:5483` | Counts are per device interval, with bounded deferred updates. | PASS |
| `test_release_mr_missing_evidence` | `tb/tools/torture_campaign.py:5499` | Missing records, incomplete capture and invalid resolution never pass. | PASS |
| `test_release_tu_gm_minimum` | `tb/tools/torture_campaign.py:5518` | The latest GM edge requires 0.25 s, allowing recorded resolution. | PASS |
| `test_release_tu_missing_gm_history` | `tb/tools/torture_campaign.py:5538` | An omitted GM history cannot silently bypass the minimum check. | PASS |
| `test_release_mr_plan_contract` | `tb/tools/torture_campaign.py:5546` | The emitted soak contract requires all inputs used by the checks. | PASS |

The retained tu controls also exercise the latest-discontinuity anchor,
uncorrelated intervals, early/late containment and missing resolution.
The feature gate passes 86 scenarios and 353 steps.

## Mutant table

All 44 mutations fail their named behavioral self-test. M01-M25 are retained;
M26-M44 are new. The runner requires a clean baseline and rc 1 with the
named assertion failure. Parser failures and timeouts do not count as kills.
Only a disposable planner file changes, outside the output directory.

| ID | Mutation | Killing method | Result |
|---|---|---|---|
| M01 | restore eligibility check removed | `test_release_eligibility_boundaries` | KILLED |
| M02 | restore ceiling relaxed | `test_release_eligibility_boundaries` | KILLED |
| M03 | power-off hold hardcoded | `test_release_timing_and_snapshot_contract` | KILLED |
| M04 | power-off CLI value discarded | `test_release_cli_parameters` | KILLED |
| M05 | ADP window charged for pre-cut time | `test_release_timing_and_snapshot_contract` | KILLED |
| M06 | missing ADP evidence skipped | `test_release_timing_and_snapshot_contract` | KILLED |
| M07 | tu bound uses media-clock holdover | `test_release_tu_contract` | KILLED |
| M08 | uncorrelated tu ignored | `test_release_tu_contract` | KILLED |
| M09 | boot evidence ends before the next cut | `test_release_boot_negative_control` | KILLED |
| M10 | tu anchor uses the first discontinuity | `test_release_tu_chained_discontinuities` | KILLED |
| M11 | tu clearing deadline ignores observation resolution | `test_release_tu_chained_discontinuities` | KILLED |
| M12 | tu oracle accepts an uncorrelated interval | `test_release_tu_chained_discontinuities` | KILLED |
| M13 | tu plan uses the first discontinuity | `test_release_tu_contract` | KILLED |
| M14 | tu plan drops capture resolution | `test_release_tu_contract` | KILLED |
| M15 | tu assertion allows five seconds | `test_release_assertion_text` | KILLED |
| M16 | tu assertion drops uncorrelated failure | `test_release_assertion_text` | KILLED |
| M17 | ADP assertion uses the pre-cut anchor | `test_release_assertion_text` | KILLED |
| M18 | ADP assertion charges the off time | `test_release_assertion_text` | KILLED |
| M19 | CLI power hold default changes | `test_release_cli_power_hold_default` | KILLED |
| M20 | tu containment drops the start allowance | `test_release_tu_start_resolution` | KILLED |
| M21 | tu containment doubles the start allowance | `test_release_tu_start_resolution` | KILLED |
| M22 | tu containment excludes its inclusive start | `test_release_tu_start_resolution` | KILLED |
| M23 | tu containment includes the clear instant | `test_release_tu_start_resolution` | KILLED |
| M24 | tu assertion drops the event window | `test_release_assertion_text` | KILLED |
| M25 | tu plan drops the start allowance | `test_release_tu_contract` | KILLED |
| M26 | mr clock-source cause removed | `test_release_mr_allowed_causes` | KILLED |
| M27 | mr CRF disruption cause removed | `test_release_mr_allowed_causes` | KILLED |
| M28 | mr received CRF toggle cause removed | `test_release_mr_allowed_causes` | KILLED |
| M29 | mr uncorrelated toggle accepted | `test_release_mr_no_cause` | KILLED |
| M30 | mr GM-only toggle accepted | `test_release_mr_gm_only` | KILLED |
| M31 | mr cause time window removed | `test_release_mr_resolution` | KILLED |
| M32 | mr foreign-stream cause accepted | `test_release_mr_stream_scope` | KILLED |
| M33 | mr eight-PDU minimum removed | `test_release_mr_eight_pdus` | KILLED |
| M34 | mr terminal hold evidence ignored | `test_release_mr_eight_pdus` | KILLED |
| M35 | MEDIA_RESET cause check removed | `test_release_media_reset_no_cause` | KILLED |
| M36 | MEDIA_RESET reuses a toggle for two increments | `test_release_media_reset_intervals` | KILLED |
| M37 | MEDIA_RESET interval update allowance removed | `test_release_media_reset_intervals` | KILLED |
| M38 | tu GM minimum removed | `test_release_tu_gm_minimum` | KILLED |
| M39 | tu GM minimum anchored at the first GM change | `test_release_tu_gm_minimum` | KILLED |
| M40 | tu GM minimum drops recorded resolution | `test_release_tu_gm_minimum` | KILLED |
| M41 | tu missing GM history accepted | `test_release_tu_missing_gm_history` | KILLED |
| M42 | mr missing evidence accepted | `test_release_mr_missing_evidence` | KILLED |
| M43 | mr plan hold weakened | `test_release_mr_plan_contract` | KILLED |
| M44 | tu plan GM minimum removed | `test_release_mr_plan_contract` | KILLED |

## Gate table

Every command below returned zero at `95bea7cf82fcf7cf034c156ef7aa6800ee769e05`.
Every command ran in the foreground, without a pipeline, from the physical
working directory above. The gate timeout was 1800 seconds per command.
`PYTHONPATH=/tmp/milan-593-markdown` supplied the hash-locked Markdown dependencies.
Dependencies were installed outside the output directory using
`python3 -m pip install --target /tmp/milan-593-markdown --require-hashes -r tools/markdown/requirements.txt`.
No dependency or checkout was copied into this output directory.

| Exact command | rc | Evidence |
|---|---|---|
| `rtk proxy python3 -B tb/tools/torture_campaign.py --self-test` | 0 | behavior-01.log |
| `rtk proxy python3 -B tb/tools/torture_release_mutants.py` | 0 | behavior-02.log |
| `rtk proxy python3 -B -m behave tests/features/torture_campaign_plan.feature -f progress` | 0 | behavior-03.log |
| `rtk proxy python3 scripts/ci_scope.py --selftest` | 0 | behavior-04.log |
| `rtk proxy python3 scripts/check_baremetal_only.py --check` | 0 | behavior-05.log |
| `rtk proxy python3 scripts/check_baremetal_only.py --selftest` | 0 | behavior-06.log |
| `rtk proxy git diff --check` | 0 | behavior-07.log |
| `rtk proxy git diff 6d5ebd7357c1e468e446f18a61527c5be6118a04 HEAD --check` | 0 | behavior-08.log |
| `rtk proxy python3 scripts/docs_check.py` | 0 | docs-01.log |
| `rtk proxy python3 scripts/check_em_dash.py --base 6d5ebd7357c1e468e446f18a61527c5be6118a04` | 0 | docs-02.log |
| `rtk proxy python3 scripts/check_em_dash.py --selftest` | 0 | docs-03.log |
| `rtk proxy python3 scripts/check_doc_style.py` | 0 | docs-04.log |
| `rtk proxy python3 scripts/check_doc_style.py --selftest` | 0 | docs-05.log |
| `rtk proxy python3 scripts/check_feature_status.py --self-test` | 0 | docs-06.log |
| `rtk proxy python3 scripts/check_doc_paths.py` | 0 | docs-07.log |
| `rtk proxy python3 scripts/check_archive.py` | 0 | docs-08.log |
| `rtk proxy python3 scripts/check_archive.py --selftest` | 0 | docs-09.log |
| `rtk proxy python3 scripts/gen_toc.py --selftest` | 0 | docs-10.log |
| `rtk proxy python3 scripts/gen_toc.py --verify-anchors` | 0 | docs-11.log |
| `rtk proxy python3 scripts/gen_toc.py --check` | 0 | docs-12.log |
| `rtk proxy python3 scripts/check_gptp_docs.py --with-submodule` | 0 | contracts-01.log |
| `rtk proxy python3 scripts/check_gptp_docs.py --selftest` | 0 | contracts-02.log |
| `rtk proxy python3 scripts/check_solution_docs.py` | 0 | contracts-03.log |
| `rtk proxy python3 scripts/check_solution_docs.py --selftest` | 0 | contracts-04.log |
| `rtk proxy python3 scripts/check_submodule_docs.py` | 0 | contracts-05.log |
| `rtk proxy python3 scripts/check_submodule_docs.py --selftest` | 0 | contracts-06.log |
| `rtk proxy python3 docs/traceability/gen_module_matrix.py --check` | 0 | contracts-07.log |
| `rtk proxy python3 scripts/check_py_idiom.py` | 0 | contracts-08.log |
| `rtk proxy python3 scripts/check_py_idiom.py --selftest` | 0 | contracts-09.log |
| `rtk proxy python3 scripts/check_hygiene.py --check` | 0 | contracts-10.log |
| `rtk proxy python3 scripts/check_hygiene.py --selftest` | 0 | contracts-11.log |
| `rtk proxy python3 scripts/check_todo_ownership.py` | 0 | contracts-12.log |
| `rtk proxy python3 scripts/check_todo_ownership.py --selftest` | 0 | contracts-13.log |

The three `*-gates.json` files record each command, physical working directory,
full head, duration, log size and SHA-256. `artifact-manifest.json` records
sizes and SHA-256 values for changed files, the renderer lock and the standards.
It substitutes for copies of large files. All output artifacts are below 200 KB.

## Scope and remaining review

Reviewers should inspect the correlation contract and independent controls.
The current design documentation records mr on a PHC step in
`docs/design/GM_LOSS_RECOVERY.md:155`. Such an observation needs a separately
recorded permitted media-clock cause to pass this release gate. This desk
change makes no physical conformance claim; talker behavior remains with #74.

No push, PR operation, merge, other checkout, hardware operation, firmware,
RTL or builder edit was performed. The local commit and PR-BODY.md are ready
for the next authorized review step. REVIEW READY publication is the final action.

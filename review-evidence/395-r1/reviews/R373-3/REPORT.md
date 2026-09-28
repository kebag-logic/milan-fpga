[R373] POSITIVE - exact head 3b5603e3d16a164c35329efeb633800fe4fe9f95

# R373-3: external review of PR #605 for #395 items 1, 2 and 5

- Head `3b5603e3d16a164c35329efeb633800fe4fe9f95`, tree `f4dd44c07795673e8434e145d7e40b355d370ae5`.
- Source base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`. Round-3 delta: `3a0cb4cf..3b5603e3`, one commit, 7 files, +48/-15.
- Context loaded, in this order:
  - AGENTS.md, CONTRIBUTING.md sections 3 and 6, and docs/README.
  - The #395 body.
  - The owner decision (5789765635), the round-1 assignment (5859935504), the margin decision (5860418611), its correction (5860783553) and the round-3 assignment (5860820812).
  - #607.
  - The full diff `8bc97021..3b5603e3` and the round-3 delta.
  - Public evidence on `395-review-evidence`: the author-r2 packet at `fa9b0b53` and the author-r3 packet at `5b4579a6`.
  - Exact-head hosted check runs.
- I read prior review findings only after my own pass over the diff and my own probes were complete.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. All five lenses are covered clean. Four new SUGGESTIONs follow, and they do not affect coverage.

## Assignment items verified at this head

1. **Round-2 BLOCKER: the bare-metal scope gate. Resolved.**
   - `scripts/check_baremetal_only.py --check` returns rc 0: "0 findings across 919 tracked first-party file(s)". `--selftest` returns rc 0 with 700 arms. Receipts: `receipts/baremetal_check.txt`, `receipts/baremetal_selftest.txt`.
   - The gate is not weakened:
     - Its blob `1d85befd` is identical at the base and at the head.
     - The PR diff touches nothing under `scripts/`.
     - The gate has no mask naming `docs/findings/`.
   - The reworded `COMMERCIAL_TIMING_395.md:117` reads "Ethernet-to-system crossings remain **unbounded false paths**, in both directions". It keeps the meaning of the former "Ethernet/sys" line, and the table at `:126-127` spells out both directions.
   - Planted-fault probe (`receipts/probe_baremetal.txt`, script `probe_baremetal.sh`):
     - The unmodified control passes.
     - Restoring the round-2 wording fails the gate at `:117` (`'/sys'`).
     - A planted `/sys` line appended to each of the 12 files the PR changes fails the gate every time, so every changed file is inside the gate's scan set.
     - The clone was clean afterwards.
   - Hosted `docs-check` at the exact head: step 23 "Bare-metal scope gate" is `success` (`receipts/hosted_docs_check_steps.txt`, snapshot 2026-09-28T00:22Z).
2. **R372-2 S1: MultiReg and AsyncResetSynchronizer attribution. Resolved.**
   - Record `:118-137` names both generic false paths. Shipping `alinx_ax7101.xdc:566` targets `mr_ff` cells, and `:568` targets `ars_ff1`/`ars_ff2` PRE pins. The shipping XDC confirms both (`receipts/shipping_xdc_excerpt.txt`; the XDC and checkpoint hashes equal record `:24-27`).
   - The per-crossing table at `:124-129` matches the author-r3 receipt (`crossings-r2-results.txt`, which is byte-identical by SHA-256 to the cited `r2-v1-crossings-r2-results.txt`).
   - I reproduced it independently: my own structural and path probe on a scratch copy of the read-only checkpoint (`classify_crossings.tcl`, `receipts/classify_crossings_results.txt`, rc 0) gives the counts below.

     | Crossing | Endpoints | Treatment under the shipping constraints |
     |---|---|---|
     | Ethernet to sys | 13 `mr_ff:D` | all False Path |
     | Sys to Ethernet | 12 `mr_ff:D` and 4 `ars:PRE` | all False Path |
     | Ethernet to milan | 50 untagged D | timed |
     | Milan to Ethernet | 6 untagged D | timed; its 8 `ars:PRE` fan-in endpoints return no timed path |

   - `crg_clkout0` matches 0 clocks.
   - #607 is linked with the reset-assertion decision (`:136-137`).
3. **S2: the standalone PLL control. Resolved.**
   - `sw/builder/test_timing_grade.py:190` calls `test_pll_grade` from `__main__`.
   - The standalone entry with the LiteX interpreter returns rc 0 and prints all three arms (`receipts/standalone_timing_grade.txt`).
   - Planted fault (`receipts/probe_pll.txt`): restoring `S7PLL(speedgrade=-2)` makes the standalone entry fail with `AssertionError: call(speedgrade=-2)`. The unmodified control passes.
   - The builder arm `test_commercial_timing_grade` returns rc 0 with all three arms executed (`receipts/focused_builder_timing_grade.txt`).
4. **S3: older wording aligned with the margin rule. Resolved.**
   - What R372-2 S3 asked for the `milan_soc.py:206-207` comment was to drop the stale "speedgrade -2" literal. `milan_soc.py:207-208` now reads "speed grade derived from the declared part", which matches the code at `:216`.
   - The BUILDING gate row `:72` reads "AX7101 WNS >= +0.03 ns; WHS >= 0". Its automatic column says "**no**: thresholds are not automatically enforced; read the reports and select the sweep seed manually".
   - BUILDING also carries the rule at:
     - `:33` (Contents);
     - `:49` (flowchart);
     - `:536-542` (the correction is cited: `sweep.sh` launches three directives and the seed pick is manual);
     - `:626-629`.
   - `RUNNING_TESTS.md:155-160` states the rule, manual seed selection, and "**not automatically enforced**", with the correction linked. `LITEX_SOC.md:161-163` says the same.
   - Those statements agree with `sw/litex/sweep.sh:1-5`, where the pick is by WNS and by hand.
5. **S4: public locator and findings index. Resolved.**
   - Record `:143-146` links `crossings.tcl` and `reports/crossings-results.txt` at `fa9b0b5373ab`.
   - Both paths exist at that commit, and `fa9b0b53` is an ancestor of the live `395-review-evidence` tip `5b4579a6`.
   - `docs/findings/README.md:11` lists the record, and its status cell is accurate.

Scope boundaries:
- Items 3 and 4 remain open. The PR body says "Relates to #395", and `closingIssuesReferences` is empty.
- There is no timing or constraint fix. The full-PR diff under `hdl/`, `sw/firmware/`, `syn/` and `*.xdc` is empty, and `milan_soc.py` changes only the comment at `:207-208` and the derivation at `:216`.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### R373-3-S1 - SUGGESTION - Docs - a README diagram still labels the build gate "WNS >= 0"
- **Where:** `docs/BUILD_FLASH_BOOT.gen.py:26`, which reads `("GATE: WNS ≥ 0", 0)`. The rendered `.svg`/`.png`/`.drawio` is embedded at `README.md:279`.
- **Authority:** margin decision 5860418611: WNS >= +0.03 ns and WHS >= 0 at every corner. AGENTS section 6, Docs lens.
- **Impact:** the integrator-facing picture of the AX7101 build shows a weaker gate than BUILDING section 5. The wording predates this PR, and the file is outside item 5's three pages and the S3 list, so this is a follow-up rather than a defect of this lane.
- **Required outcome (optional):** a follow-up regenerates the diagram with the recorded rule. The enforcement follow-up named in the correction is a natural home.
- **Verification:** the diagram no-drift gates pass after regeneration, and the label matches BUILDING `:72`.

### R373-3-S2 - SUGGESTION - Docs, RTL - the reset endpoints overlap between the two Ethernet crossings
- **Where:** `docs/findings/COMMERCIAL_TIMING_395.md:124-133`.
- **Evidence:** in `receipts/classify_crossings_results.txt`, the PRE pins of `FDPE_12`..`FDPE_15` have fan-in from both `milansoc_crg_clkout0` and `milansoc_crg_clkout1`. The 4 sys-to-Ethernet reset endpoints are therefore a subset of the 8 milan-to-Ethernet ones: 8 unique PRE pins, not 12. The per-crossing counts in the record are correct.
- **Impact:** #607 might size its reset-assertion decision as 12 endpoints.
- **Required outcome (optional):** a sentence in the record, or a note relayed to #607, that the reset endpoints are 8 unique pins.
- **Verification:** re-read against the receipt's `cells:` lines.

### R373-3-S3 - SUGGESTION - Docs - cited receipt named without a locator
- **Where:** record `:121-122` cites `r2-v1-crossings-r2-results.txt` by filename and links only the review comment.
- **Evidence:** a byte-identical copy is published at `5b4579a6:review-evidence/395-r1/author-r3/reports/crossings-r2-results.txt`.
- **Required outcome (optional):** link one of the two published copies, as `:145-146` does.

### R373-3-S4 - SUGGESTION - Tests, Robustness - the standalone entry skips two arms silently without an argument
- **Where:** `sw/builder/test_timing_grade.py:186-190`.
- **Evidence:** with no argument, the entry runs only the contract arm and prints nothing about the platform and PLL arms (`receipts/standalone_timing_grade_noarg.txt`). The builder arm records a skip, and no documentation cites the standalone entry.
- **Required outcome (optional):** print a visible stand-down line when the interpreter argument is absent.

## Prior public findings at this head (read after my own pass)

| Finding | Status at `3b5603e3` | Evidence |
|---|---|---|
| R372-2-F1 = R373-2 R2-F1 (BLOCKER; Tests, Docs): the record trips the bare-metal gate | **Resolved** | Item 1 above. Local `--check`/`--selftest` return rc 0, and the hosted step 23 is `success`. The author-r3 `gates/baremetal-check.log` and `baremetal-selftest.log` are in the author's gate list. The hosted builder step is still pending with the manager. |
| R372-2 S1 (ARS false path at xdc:568) | Resolved | Item 2 |
| R372-2 S2 = R373-2 S-F (standalone PLL) | Resolved | Item 3 |
| R372-2 S3 = R373-2 S-E (older gate wording, non-enforcement) | Resolved | Item 4 |
| R372-2 S4 (crossings locator) | Resolved | Item 5 |
| R372-1 S4 (findings index) | Resolved | `docs/findings/README.md:11` |
| R372-1 S1 (UG835 wording, record `:57`), S2 (power Tj fixed at 85 C), S3 (reporter argument edges) | Retained as suggestions | `:57` is unchanged, and `timing_grade.tcl` and `report_timing_grade.py` have an empty diff since `3a0cb4cf` |
| R373-2 S-A (`timing_grade.tcl:73` post-restore check mutant) | Retained as a suggestion | File unchanged since `3a0cb4cf` |
| R373-2 S-B (shared LiteX skip text, `test_builder.py:27561`) | Retained as a suggestion | Unchanged |
| R373-2 S-C (power report is worst-case at 85 C, unstated) | Retained as a suggestion | No power-report sentence in the record or in BUILDING section 5 |
| R373-2 S-D (`report_timing_grade.py` creates the directory before refusing) | Retained as a suggestion | Unchanged |
| Round-1 findings (R372-1 F1-F3, R373-1 F1), resolved at `3a0cb4cf` | Still resolved | The delta changes none of the lines those resolutions rest on. Record `:80-112` (census, rejected exceptions, #607) and `:153-170` are unchanged, and the lines at `:61-70` were only extended. |

## Reviewer-owned ledger

| Lens | Result | Examined artifacts (at head) | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #395 body, owner decision 5789765635, margin decision 5860418611, correction 5860783553 and round-3 assignment 5860820812, checked against record `:61-70` and `:114-146`, BUILDING `:33`, `:49`, `:72`, `:536-542` and `:626-629`, RUNNING_TESTS `:155-172`, LITEX_SOC `:145-167` and findings README `:11`. Corner rows at record `:44-48` against the author-r3 per-corner summaries (identical, 0.123/0.101 and 1.429/0.036). Items 3 and 4 open (`closingIssuesReferences` empty). No timing or constraint fix (full-PR diff under hdl/, sw/firmware/, syn/ and *.xdc is empty). | R373-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| RTL | CLEAN | Shipping `alinx_ax7101.xdc:566`, `:568` and `:583-595` (`receipts/shipping_xdc_excerpt.txt`, hashes equal record `:24-27`). An independent structural and timing-path classification of the four Ethernet crossings on the read-only checkpoint (`classify_crossings.tcl`, `receipts/classify_crossings_results.txt`), checked against record `:117-137`. `milan_soc.py:205-216` comment and PLL derivation. No HDL in the diff. Only S2 (a suggestion) was raised. | R373-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Robustness | CLEAN | Gate reach: restored wording and a `/sys` plant in each of the 12 changed files all fail, the control passes, and the gate blob equals the base (`receipts/probe_baremetal.txt`). The PLL literal fault is killed through the standalone entry (`receipts/probe_pll.txt`). The standalone entry without an argument (`receipts/standalone_timing_grade_noarg.txt`; S4). `timing_grade.tcl` and `report_timing_grade.py` have an empty diff since `3a0cb4cf`. | R373-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Tests | CLEAN | `sw/builder/test_timing_grade.py:186-190` standalone (rc 0, three arms). `test_builder.test_commercial_timing_grade` focused (rc 0, three arms). The planted PLL literal fails. `check_baremetal_only.py --check`/`--selftest` rc 0. `ci_scope.py --selftest` rc 0 (`receipts/doc_gates.txt`). Only S4 (a suggestion) was raised. | R373-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |
| Docs | CLEAN | Delta wording in the record, BUILDING, RUNNING_TESTS, LITEX_SOC and the findings README, read against the decisions and `sweep.sh:1-5`. These gates return rc 0 (`receipts/doc_gates.txt`, `receipts/doc_gates_renderer.txt`): `docs_check.py`, `check_doc_paths.py`, `gen_toc.py --check`, `check_em_dash.py --base 8bc97021` (306 added lines) and `--base 3a0cb4cf` (45 lines), `check_feature_status.py`, `check_doc_style.py`, `check_solution_docs.py`, `check_py_idiom.py`, and `git diff --check`. Record links resolve to the cited comments and evidence commits. S1 and S3 are suggestions. | R373-3 | 3b5603e3d16a164c35329efeb633800fe4fe9f95 |

## Real limits

- **Banks not run.** I did not run the full builder bank or the parent, protocol-processor, gPTP or Yosys banks, as the assignment excludes them. My builder coverage is the focused `test_commercial_timing_grade` arm and the standalone entry. The manager's full static/builder and native banks at this head are the public source evidence for the rest.
- **Corner reports not regenerated.** I did not regenerate the corner reports. The checkpoint hash is unchanged, and `timing_grade.tcl`, `report_timing_grade.py` and `ax7101_timing.py` have an empty diff since round 2. I cross-checked the record against the author-r3 retained summaries instead.
- **Classification probe method.** My crossing classification uses combinational fan-in start-point clocks and `get_timing_paths -nworst 1 -max_paths 5000` per direction. It confirms the endpoint classes and exception attribution. It does not re-measure the intended 8 ns bound, which is unchanged in this delta.
- **Verilator not used.** There is no RTL in the diff.
- **Hosted runs incomplete at the snapshot.** At 2026-09-28T00:22Z these were `in_progress`: `docs-check` (the "End-station builder gates" step and later steps), `elaborate`, and Verilator shards 0, 1, 2 and 4. `Physical gPTP` is `skipped`, which is a skipped context, not an executed job.
- **No physical evidence.** Physical calibration was NOT RUN. No hardware was touched, and field skips are not hardware proof.
- **Source head only.** This verdict is on the source head. It is not a verdict on the current-dev merge candidate.

## Pending manager duties

- Hosted and act acceptance at the exact head. This includes the `docs-check` job completing with "End-station builder gates" executed, and `elaborate` and all Verilator shards completing.
- The final current-dev candidate. The source base is `8bc97021`, live dev is `63de19bd`, and candidate-merge validation and post-merge containment follow.
- Opening the public follow-up that the margin correction names ("Enforcing it automatically is a separate follow-up"). No issue number for it is public yet. It could also carry S1.
- Optionally relaying S2's unique-pin count to #607.
- Items 3 and 4 remain open on #395.

R373-3 FINISHED

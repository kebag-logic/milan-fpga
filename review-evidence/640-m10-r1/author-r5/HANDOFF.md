# HANDOFF - [A720o] issue #640, PR #835 round 5 (docs only)

Status: REVIEW READY (2026-11-02). All 55 rc files read 0. Head d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73 (tree 7117c798eca686f6023287b32a07af72baf81c0f), on 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2 and dev 503bc97cd4f24ad07596c17e7188f2024617972d. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 545ac9cb (640-a720n's head, PR #835's round 4 head). `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Round 4 reviews: R765-4 NEGATIVE (PR #835 issuecomment-6584004136); R766-4 NEGATIVE (issuecomment-6582620684). Both on the same MINOR. Their probes came from the public evidence branch `640-m10-review-evidence` at 781cfb93 (`reviews/R765-4/scripts/anchor_probe.py`, `reviews/R766-4/scripts/fix_probe.py`), read before running.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6585325093 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6586744550 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720o (gate clone, venv copied from 640-a720n, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- Page changed this round: docs/design/MARK_II_AREA_PLAN.md (AP) only, 5 lines (5+, 5-), five commits. No RTL, firmware, generator, gate or configuration file. AP is not gate-read; the two gate-read pages are unchanged, and their readers were run again anyway.

## Read this first

1. **No STOP.** F1 takes R766-4-F1's exact text unsplit; it passes check_doc_style (table cells are exempt from the prose limits, and the changed-block probe finds 0).
2. **Afterwards neither the stage table nor the census says stage 3 removes no generated FIFO.** Every FIFO mention on AP was re-read (`grep -n -i fifo`): the census note AP:339-340 already limits itself to "the 29 generated FIFO RAMB36"; AP:322 and :330 keep their stage 3 rows; AP:387 is the 47-RAMB36 bound.
3. **R765-4-S1 taken** (reason below). It changes only link text.
4. The three residues take their published exact wording, one commit each.

## Commits (one-line subjects, no body, no trailers)

Commits 1 to 14 (640-a720j to 640-a720n) are unchanged; this round adds five:

| # | SHA | Subject |
|---|---|---|
| 15 | 5878a5effb45cdae63086ad311bd9c6ce341298f | Name the FIFOs of stage 3 blocks among stage 3's removals and limit the earlier leaving to the 29 generated FIFO RAMB36 (#640) |
| 16 | fda074559e5bfbae5fbbb7a886e4b9c9956c762f | Make both regions, not the BIOS, what ctrl_memory's banks hold until stage 3 (#640) |
| 17 | 8a093ae904c20bbf8a716456a72ccc23f6b8e0f1 | Say the 128-byte console buffer comes from taking 10 ms as the gap (#640) |
| 18 | 189accced658daae4bc0709f64ab74bd88d31753 | Say rom is filled from the flash copy from stage 1 on, not already (#640) |
| 19 | d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73 | Name the M8a-1 link's target as the Mark I ledger (#640) |

## Findings and changes (AP line numbers at head)

| IDs | Severity, lenses | Where | Was | Now | Commit |
|---|---|---|---|---|---|
| R765-4-F1 / R766-4-F1 | MINOR; Conformance, Docs | AP:233, stage 3 "Removes" | "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block ([census](#litex-block-census))" | "Wishbone and CSR-bank glue; the FIFOs of stage 3 blocks. The 29 generated FIFO RAMB36 leave earlier, each with its block ([census](#litex-block-census))" (R766-4-F1's exact fix, not split) | 15 |
| R766-3-RESIDUE-2 / R765-3-R1 | RESIDUE; Docs | AP:239, note under the stage table | "`ctrl_memory`'s `rom` and `sram` banks hold them until stage 3." | "Until stage 3, `ctrl_memory`'s banks hold both regions." | 16 |
| R765-2-RESIDUE-1 | RESIDUE; Docs | AP:368, console UART text | "Under 10 ms, the buffer would be 128 bytes." | "Taking 10 ms as the gap gives 128 bytes." | 17 |
| R765-2-RESIDUE-2 | RESIDUE; Docs | AP:336, census, split build `ctrl_memory` row, fate cell | "... Stage 1 already fills `rom` from the flash copy, not the configuration image" | "... From stage 1, `rom` is filled from the flash copy, not the configuration image" | 18 |
| R765-4-S1 | SUGGESTION; Docs | AP:231, stage 1 "Removes" | "already left at the switch-over ([M8a-1](#firmware-and-block-ram-ledger))" | "already left at the switch-over (M8a-1, [Mark I ledger](#firmware-and-block-ram-ledger))" | 19 |

### R765-4-S1: taken, and why

- The anchor lands on `### Firmware and block RAM ledger` (AP:1260), under `## Mark I plan history` (AP:476). The page's current section is `## Mark II Block RAM ledger` (AP:382).
- M8a-1's -18 RAMB36 row (AP:1302) exists only in the history ledger, so the target stays. Only the label changes, to say which ledger it is.
- Cost: link text only, in a table cell; no figure or booking moves. The anchor probe still resolves it, and its mutant control still fails.
- Not taken: pointing it at `SPLIT_CONTROL_MEMORY.md#5-fit` instead. That page reports M8a-1's mapping, not the -18 ledger row the cell cites.

### Checks on the change

| Check | Result | Evidence |
|---|---|---|
| R765-4's `anchor_probe.py` on AP:233 (clean clone at head) | `#litex-block-census RESOLVES`; control `#firmware-and-block-ram-ledgerx MISSING`; rc 0 | evidence/gates/logs/anchor_probe_233.log, .rc |
| Same probe on AP:231, 233, 236 (lane at head) | 6 fragments resolve, control missing, rc 0 | evidence/anchor_probe_head.out |
| `census_coverage.py` (640-a720l's, as the reviewers ran it) at head | RESULT: PASS; output byte-identical to round 4's `census_coverage_worktree.out` | evidence/census_coverage_head.out; gates/logs/census_coverage.log |
| Census control against the round 1 page | RESULT: FAIL, as it must (rc of the negated step 0) | gates/logs/census_coverage_control.log |
| Planted style controls (R766-4's `fix_probe.py`, in memory) | 12-word sentences in place of AP:239 and AP:368 are caught (sentence and paragraph limits) | evidence/style_control.out |
| Changed-block style probe, 4 pages against 503bc97c and AP against 545ac9cb | 0 findings | gates/logs/style_touched.log |
| FIFO re-read of AP | No line says stage 3 removes no generated FIFO | `grep -n -i fifo docs/design/MARK_II_AREA_PLAN.md` (Read this first, 2) |

## Gate table

All 55 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/`, `scripts/`, `sw/`, `syn/` or `hdl/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720o/gates/wt: a fresh clone of the lane at d85da3297f0b664ac4f2b63eac3c5fd36ed4eb73 (tree 7117c798, evidence/gates/clone_head.txt), with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720n's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720n's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720o/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run 2026-11-02T19:46:28+01:00 to 2026-11-02T20:40:32+01:00. Step list: evidence/gates/run_gates.sh, run_all.sh, run_extra.sh (run_both.sh runs the last two in order). The table is round 4's rows with this round's rc and last log line (evidence/gate_table.py).

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720o/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | gPTP documentation selftest: OK (30 controls) |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py`, `timesync_chain.gen.py` `--check`/`--selftest` | 0 | time-sync diagram selftest: OK (source, status, XML, raster) |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | solution documentation selftest: OK (45 mutation controls) |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py`, `check_submodule_docs.py` | 0 | submodule documentation selftest: OK (table and diagram controls) |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and three `--check` | 0 | WaveDrom current: docs/diagrams/wd_gptp_pdelay.json |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | diagram PNG selftest: OK (6 rasters, 28 mutation controls) |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | traceability matrix up to date (80 modules, 0 untested <= ratchet 0, 0 archived) |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | source evidence selftest: PASS (7 arms) |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py`, `measure_cohesion.py` `--selftest` | 0 | 18 checks: 18 PASS, 0 FAIL |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check`/`--selftest` | 0 | baremetal-only selftest: PASS (867 arm(s)) |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN; 0 actual firmware compiler invocations |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persisted record has a unique id inside record_id[7:0], every group is inside its block, every payload fits MAX_PAYLOAD_P, every image fits one erase block, the allocation is the donor's own F07.8 rule and its floor fits the namespace at every shipped shape, the worst-case commit fits T-NVM-COMMIT-TIMEOUT with 2x margin, every record round trips through a KLJ2 image, an empty user name survives it, and a CRC-clean image missing any mandatory record is refused with zero records applied |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS: capture census, clocks, both timing arms and receipt agree |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | saved-state writer gate: OK across 5 shape(s), and every planted defect reddened |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | iob_pack_selftest: 22 arms, 21 mutants, 0 failure(s) |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 checks: 50 PASS, 0 FAIL |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check`/`--selftest` | 0 | 66 checks: 66 PASS, 0 FAIL |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 checks: 82 PASS, 0 FAIL |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check`/`--selftest` | 0 | 106 checks: 106 PASS, 0 FAIL |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 checks: 45 PASS, 0 FAIL |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check`/`--selftest` | 0 | 105 checks: 105 PASS, 0 FAIL |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check`/`--selftest` | 0 | 35 checks: 35 PASS, 0 FAIL |
| docs-gates-0 | gate_37 SV idiom | `check_sv_idiom.py` (+ `--selftest`) | 0 | 55 checks: 55 PASS, 0 FAIL |
| docs-gates-0 | gate_38 C++ idiom | `check_cpp_idiom.py` (+ `--selftest`) | 0 | 75 checks: 75 PASS, 0 FAIL |
| docs-gates-0 | gate_39 Python idiom | `check_py_idiom.py` (+ `--selftest`) | 0 | 54 checks: 54 PASS, 0 FAIL |
| docs-gates-0 | gate_40 shell idiom | `check_sh_idiom.py` (+ `--selftest`) | 0 | 48 checks: 48 PASS, 0 FAIL |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | doc path gate: OK (1084 cited paths all resolve, 2 allowlisted; 10 line anchor(s) within their file) |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | archive selftest: OK (24 controls) |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| docs-gates-0 | gate_46 AEM store | `gen_aem_store.py --self-test` | 0 | gen_aem_store self-test: PASS |
| docs-gates-0 | gate_47 sweep shape | `check_sweep_shape.py --self-test` | 0 |   [self-test] OK: 1 drift(s) reported |
| docs-gates-0 | gate_48 deploy shape | `check_deploy_shape.py --self-test` | 0 |   [selftest] OK: 1 drift(s) reported |
| docs-gates-0 | gate_49 entity shape | `check_entity_shape.py --self-test` | 0 | RESULT: PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | manifest comparison controls: PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check`/`--selftest` | 0 | selftest: PASS (2199 contract items, 5258 arms) |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | selftest: PASS |
| (lane) | Markdown gates, pinned venv | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's page against 545ac9cb | 0 | docs/design/MARK_II_AREA_PLAN.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | census coverage | `census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts | 0 | RESULT: PASS |
| (lane) | census coverage control | `! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must | 0 | RESULT: FAIL |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- check_em_dash still counts 231 added lines: this round edits lines the branch already adds.
- The clean clone's `git status --short` was empty after both runs (logs/final_status.txt, final_status_extra.txt).
- Large logs are listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read. Unchanged.
3. The console buffer still rests on S2b's 2.0 ms share; the page gives 128 bytes under 10 ms. When PR #810 merges or the share changes, the buffer is derived again. Unchanged.
4. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
5. The census keeps today's `PSCLK` and PHY reset behaviour. If the owner wants either changed, that is a new decision. Unchanged.
6. For the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3). Unchanged.
7. Not taken, optional: R765-3-S1 (where stage 1's loader runs and how `rom` becomes writable); R765-2-S1 / R766-2-S1, R766-2-S2, R766-2-S3, R765-2-S4. Unchanged.
8. Closed this round, pending re-review: R765-4-F1 / R766-4-F1, R766-3-RESIDUE-2 / R765-3-R1, R765-2-RESIDUE-1, R765-2-RESIDUE-2, R765-4-S1. R766-4's optional PR-body suggestion ("none of the 29 RAMB36") is taken in PR-BODY.md's round 4 row.
9. Live dev is at e61a4afa (fetched 2026-11-02), 18 commits past 503bc97c; it changes `sw/litex/milan_soc.py` (26+, 7-), which the census reads, and not AP. The candidate merge must be validated on current dev, with the census check re-run there (manager duty, R765-4 and R766-4).
10. Observation, unchanged: the switch-over's Block RAM ledger (AP:1297-1305) credits no removal for the 8 processor memory-path crossing RAMB36 that the census books to the switch-over. An omitted credit, not a double booking; it belongs to the switch-over lane's ledger.
11. Coverage: this round's changes are in Conformance and Docs scope; RTL, Robustness and Tests artifacts are untouched. Conformance and Docs must be covered again at d85da329.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| round5.diff | `git diff 545ac9cb HEAD` |
| census_coverage_head.out | The census coverage check at the lane head (PASS, identical to round 4's) |
| anchor_probe_head.out | R765-4's anchor probe on AP:231, 233, 236 |
| style_control.out | Two planted style controls, both caught |
| style_touched.py | The changed-block style probe |
| make_pr_body.py | Builds PR-BODY.md from round 4's |
| gate_table.py, gate_table.md | Builds the gate table from round 4's rows and this round's logs |
| gates/ | Every step's log and rc, run_all.out, run_extra.out, the run scripts, setup_clone.sh, service_bounds_arm.py, clone_head.txt, the anchor probe on :233; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.

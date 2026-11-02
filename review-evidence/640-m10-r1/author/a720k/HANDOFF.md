# HANDOFF - [A720k] issue #640 Mark II charter follow-up, second pass (docs only)

Status: REVIEW READY (2026-11-02). All 54 rc files read 0. git diff --check 503bc97c HEAD rc 0. Head 3f8ed303e01285f1bad0641f4ebc05764f162467 (tree 580d876cd9f7f973d1407d3da5759a23822a24d0). Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 7aa996e3 (640-a720j's head) on dev 503bc97c; `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d, and origin/dev is still 503bc97c.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Source of both items: #640 issuecomment-6575277828 ([A10], 2026-11-02 10:50 UTC), the manager's answer to 640-a720j's open points 1 and 2.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6575884690 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6576935771 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720k (gate clone, venv copied from 640-a720j, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- One page changes in this pass: docs/design/MARK_II_AREA_PLAN.md (AP). No RTL, firmware, generator, gate or configuration file. docs/integration/QSPI_FLASHBOOT.md not edited. No generated page reads AP; DOC_MAP and the TOC gate pass unchanged.

## Read this first

1. **D21 is a new decision row, a manager decision.** The assignment said to move open decision 4 into the decisions table, so I numbered it D21, after D20. Its outcome text follows the comment's bullets; the offset and budget are left to the stage 1 lane (`FLASHBOOT_LAYOUT` and the generated layout page).
2. **The census held no layout statement.** The census (AP:287-320) never said the layout stays or lacks a slot. The statements were in the stage table row (AP:231), the stage 1 text (AP:264-273), the D18 consequence (AP:381), lane 2's dependency (AP:398) and open decision 4. All are gone; `grep -n -i "open decision 4\|stay as is\|layout is unchanged\|no firmware slot"` on AP finds nothing.
3. **One contents line changed with item 2.** AP:20 now reads "Owner and manager rulings, 2026-10-31 and 2026-11-02.", since the table now holds a manager row. "The owner and manager rulings of ..." broke the 10-word sentence limit.
4. **Line numbers in 640-a720j's HANDOFF shift.** Add 8 to its AP line numbers 266 to 375, and 9 to 376 to 431. Its 432 to 441 (open decision 4) are gone; from 442 on, subtract 1.

## Commits (one-line subjects, no body, no trailers)

640-a720j's five commits (1 to 5) are unchanged; this pass adds:

| # | SHA | Subject |
|---|---|---|
| 6 | a0080e09b9c23219752d072468d40bda07ff0343 | Link the owner's 2026-11-02 decisions D18 to D20 to the comment on #640 that records them (#640) |
| 7 | 3f8ed303e01285f1bad0641f4ebc05764f162467 | Record the manager's decision that the copied firmware image gets its own erase-aligned flash slot, and drop open decision 4 and the unchanged-layout statements (#640) |

## 1. D18 to D20 links (commit 6)

| Where (at head) | Change |
|---|---|
| AP:381 | D18 link: `issues/640` -> `issues/640#issuecomment-6575277828` |
| AP:382 | D19 link: the same |
| AP:383 | D20 link: the same |

No other link the first pass made for these decisions points at #640: the census and UART rows link to the D18 to D20 anchors on the page (AP:289, :306, :315, :324), not to the issue. The other bare `issues/640` links in the branch (AP:3, MAILBOX_SPLIT.md:27, AREA_BUDGET.md) are not about D18 to D20.

## 2. Open decision 4 -> D21, manager decision (commit 7)

| Where (at head) | Before | After |
|---|---|---|
| AP:20 | "The owner rulings of 2026-10-31 and 2026-11-02." | "Owner and manager rulings, 2026-10-31 and 2026-11-02." |
| AP:231 (stage table, stage 1) | "the flash layout is unchanged" | "the image has its own flash slot ([D21](#mark-ii-decisions))" |
| AP:264-273 (stage 1 boot and bus) | "The layout in QSPI_FLASHBOOT.md stays unchanged. That layout has no firmware slot (open decision 4)." | Own slot (D21); free, erase-aligned, never reserved or used; bitstream and AEM keep offsets and budgets; no image in the bitstream slot's tail; the stage 1 lane states offset and budget in `FLASHBOOT_LAYOUT` and the generated layout page; until then QSPI_FLASHBOOT.md describes the shipping layout |
| AP:381 (D18 consequence) | "where the image sits in flash is open decision 4" | "the image sits in its own flash slot (D21)" |
| AP:384 (new D21 row) | - | "[Manager, 2026-11-02](...#issuecomment-6575277828)": own slot sized for the image, free erase-aligned range, neither reserved (`journal`, `user`) nor used; bitstream and AEM keep offsets and budgets; not in the bitstream slot's tail, which would tie the offset to the bitstream's size. Consequence: the stage 1 lane adds the slot to `FLASHBOOT_LAYOUT` and the generated layout page, and states its offset and budget there |
| AP:398 (lane 2) | Scope without the slot; depends on "Lane 1; open decision 4" | Scope adds "the firmware's own flash slot (D21)"; depends on "Lane 1" |
| AP:417-441 (open list) | Items 1 to 4 | Items 1 to 3; item 4 (nine bullets: the no-slot premise, AEM 64 KiB, rom 96,624 B, bitstream 3,825,992 B, 368,312 B tail, the two choices) removed |

Not chosen: the slot's offset and budget. Not edited: docs/integration/QSPI_FLASHBOOT.md, sw/litex/milan_soc.py (`FLASHBOOT_LAYOUT`), docs/diagrams/flash_layout.gen.py.

## Gate table

All 54 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/` or `scripts/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720k/gates/wt: a fresh clone of the lane at 3f8ed303e01285f1bad0641f4ebc05764f162467, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720j's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720j's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720k/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run 2026-11-02T12:24:18+01:00 to 2026-11-02T13:16:28+01:00. Step list: evidence/gates/run_gates.sh, run_all.sh.

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720k/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 194 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
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
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 finding(s) across 5 config(s): the inventory's (group, index) key set is exactly the set the shape requires with no key claimed twice, every persist |
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
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 194 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages | 0 | docs/findings/README.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | style on this pass's changed blocks | check_doc_style's `analyze()` on AP's changed blocks against 7aa996e3 | 0 | docs/design/MARK_II_AREA_PLAN.md: 0 finding(s) in changed blocks |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- The readers of AREA_BUDGET.md and MAILBOX_SPLIT.md re-ran at this head though this pass does not touch those pages.
- Clone status after the run: empty (evidence/gates/logs/final_status.txt).
- gate_41's log is 337,511 B, listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open points for the manager (as they now stand)

1. ~~Post the owner's 2026-11-02 decisions on #640.~~ Done by the manager (issuecomment-6575277828); D18 to D20 link to it.
2. ~~Open owner decision 4.~~ Decided by the manager; recorded as D21. The slot's offset and budget remain for the stage 1 lane.
3. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j, Read this first, 3). Unchanged.
4. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read (640-a720j, Read this first, 4). Unchanged.
5. The UART buffer rests on the 2.0 ms per-pass share, S2b's unmerged rule (640-a720j, section 3). Unchanged.
6. Coverage: every touched scope is Conformance and Docs. No RTL, firmware, generator, gate or configuration file changed.
7. New: D21 is numbered by me (Read this first, 1); the reviewer may prefer another label.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| style_touched.py | check_doc_style's analyze() over every changed block of a page against a base |
| service_bounds_arm.py | Runs MAILBOX_SPLIT.md's gate reader on the clone |
| write_handoff.py, make_pr_body.py | Build this file and PR-BODY.md |
| gates/ | Every step's log and rc, run_all.out, run_all.sh, run_gates.sh, setup_clone.sh; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.

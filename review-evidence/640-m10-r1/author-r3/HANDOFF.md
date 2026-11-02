# HANDOFF - [A720m] issue #640, PR #835 round 3 (docs only)

Status: REVIEW READY (2026-11-02). All 55 rc files read 0. Head d52e966bb7258184e33702a9edd9ca11b4b1362c (tree 4f12d77661d545c8bd5676ceaa1654328d79ce94), on 30eb4834 and dev 503bc97c. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at 30eb4834 (640-a720l's head, PR #835's round 2 head). `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d; origin/dev is still 503bc97c (fetched at start).
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Round 2 reviews: R765-2 POSITIVE (PR #835 issuecomment-6579373754); R766-2 NEGATIVE on one MINOR, R766-2-F1 (issuecomment-6579449561).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6579495587 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6580708443 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720m (gate clone, venv copied from 640-a720l, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- Page changed this round: docs/design/MARK_II_AREA_PLAN.md (AP) only, 10 lines added and 5 removed. No RTL, firmware, generator, gate or configuration file. AP is not gate-read; both gate-read pages of the PR are unchanged this round, and their readers were run again anyway.

## Read this first

1. **No STOP.** The fix rests on the code and D18: `ctrl_memory.py:128-129` defines `rom` and `sram` at the BIOS regions' origins; `milan_soc.py:3005-3014` builds them and refuses other origins; `milan_soc.py:3168-3176` builds no integrated ROM or SRAM under `--ctrl-mailbox`.
2. **The stage table's stage 1 cells are unchanged.** "Drop DDR3 and the BIOS ROM" is the owner's stage 1 heading (#640 issuecomment-6545999204), and R766-2 read the note as reconciling them. The note now says so ("Stage 1's row keeps the owner's words") and states the switch-over, the holder and stage 1's work in the same terms as the census rows and lane 2.
3. **"No fate below is a LiteX block" (AP:311) still holds.** The BIOS fates name `ctrl_memory`'s LiteX banks only as the holder until stage 3; the end state is first-party Block RAM, as the `ctrl_memory` row (AP:336) says.
4. **Suggestions R766-2-S1, S2, S3 are not taken.** The brief limits the round to F1; each is listed in the open list.

## Commits (one-line subjects, no body, no trailers)

Commits 1 to 12 (640-a720j, 640-a720k, 640-a720l) are unchanged; this round adds one:

| # | SHA | Subject |
|---|---|---|
| 13 | d52e966bb7258184e33702a9edd9ca11b4b1362c | Say the switch-over removes the BIOS and its ROM and SRAM, that ctrl_memory's rom and sram banks hold those regions until stage 3 and that stage 1 fills rom from flash, and drop the BIOS ROM from lane 2's scope (#640) |

## Finding R766-2-F1 (Conformance, Docs; MINOR)

| Where (at head) | Was | Now |
|---|---|---|
| AP:333, BIOS ROM fate | "Removed, nothing in its place: the split build runs no BIOS. From stage 1 the first-party boot loader fills the firmware's memory (D18)" | "Removed at the switch-over: the split build runs no BIOS and builds no integrated ROM. `ctrl_memory`'s `rom` banks hold the region and the reset entry until stage 3, then first-party Block RAM (the `ctrl_memory` row). From stage 1 the boot loader fills `rom` from the flash copy (D18)" |
| AP:334, BIOS SRAM fate | "Removed, nothing in its place: the split build builds none" | "Removed at the switch-over: the split build builds no integrated SRAM. `ctrl_memory`'s `sram` banks hold the region until stage 3, then first-party Block RAM (the `ctrl_memory` row)" |
| AP:432, lane 2 scope | "Drop DDR3 and the BIOS ROM; a boot loader copying the firmware from QSPI flash; ..." | "Drop DDR3 (lane 1 already drops the BIOS memory); a boot loader filling `rom` from the firmware's QSPI flash copy (D18); ..." |
| AP:235-241, note under the stage table | "Lane 1's split build already drops the BIOS memory. The census places it at the switch-over." | "Stage 1's row keeps the owner's words. The census places the BIOS at the switch-over." / "The switch-over removes the BIOS and its ROM and SRAM. `ctrl_memory`'s `rom` and `sram` banks hold them until stage 3." / "Stage 1 drops DDR3 and fills `rom` from flash (D18)." |

Block cells and stages are unchanged, so the census coverage check maps the same 165 objects to the same rows (PASS; output identical to round 2's).

### Every statement of who removes the BIOS memory (all touched pages, at head)

Search: `grep -n -i bios` and `\bROM\b`, `rom`, `sram`, `ctrl_memory`, `boot loader` over the four pages this PR touches (AP, AREA_BUDGET.md, MAILBOX_SPLIT.md, docs/findings/README.md), plus AP's stage 1 section.

| Where | Statement | Agrees? |
|---|---|---|
| AP:112 | Basis row disposition: "The switch-over and LiteX stages 1 to 3; its 47 RAMB36 are 29 generated FIFOs and 18 BIOS ROM and SRAM" | Yes, unchanged |
| AP:231 | Stage table, stage 1: "Drop DDR3 and the BIOS ROM ... / BIOS ROM and SRAM, 18 RAMB36 measured" | Owner's stage wording, unchanged; reconciled by the note (Read this first, 2) |
| AP:235-241 | Note under the stage table | Changed this round |
| AP:269-270 | Stage 1 section: "Stage 1's loader copies the firmware image from QSPI flash. It copies it into Block RAM, then starts it (D18)." | Yes, unchanged |
| AP:299 | Census lead: "D19 removes every LiteX block, beyond DDR3 and the BIOS." | Yes, scope of D19; unchanged |
| AP:333-334 | Census BIOS ROM and SRAM rows | Changed this round |
| AP:336 | Census `ctrl_memory` row: stage 3, first-party Block RAM; "Stage 1 already fills `rom` from the flash copy" | Yes, unchanged |
| AP:354 | Console loss row, "no BIOS" (the probe image's condition) | Not a removal statement |
| AP:387-388 | Block RAM ledger: "18 BIOS memory. All 47 are gone once LiteX stage 3 ends." | Yes, unchanged |
| AP:415-416 | D18 consequence "LiteX stage 1's boot loader"; D19 "not only DDR3 and the BIOS" | Yes, unchanged |
| AP:432 | Lane 2 scope | Changed this round |
| AP:802 | SoC side table, basis `@own` contents include "the BIOS ROM and SRAM" | Describes the basis; not a removal statement |
| AP:1302, 1309-1312, 1335 | M8a-1: "BIOS ROM and SRAM not built in the split"; "The split builds neither BIOS memory"; "Keeping the BIOS ROM and SRAM would add 18" | Yes, unchanged |
| AREA_BUDGET.md:301, 306-310 | M8a-1's row and text: "The split builds neither BIOS memory"; "Keeping the BIOS memories would add 18" | Yes, unchanged |
| MAILBOX_SPLIT.md:1151-1154 | "Since #640 M8a-1 the switch ... builds no BIOS ROM or BIOS SRAM, and builds `rom` and `sram` block RAM from that image" | Yes, unchanged |
| docs/findings/README.md | No BIOS statement | - |

## Gate table

All 55 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/` or `scripts/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720m/gates/wt: a fresh clone of the lane at d52e966bb7258184e33702a9edd9ca11b4b1362c, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720l's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720l's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720m/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run 2026-11-02T15:22:54+01:00 to 2026-11-02T16:14:02+01:00. Step list: evidence/gates/run_gates.sh, run_all.sh; readers and census steps: evidence/gates/run_extra.sh.

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720m/gates/runner_temp/milan-hdl-reference/index.html |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | docs_check: 0 finding(s) across 213 md files + 1436 scrubbed text files, scrub self-test 23/23, routing arms 4/4 [git ls-files] |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 230 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
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
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 230 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's page against 30eb4834 | 0 | docs/design/MARK_II_AREA_PLAN.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | census coverage | `census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts | 0 | RESULT: PASS |
| (lane) | census coverage control | `! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must | 0 | RESULT: FAIL |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- `style_touched` checks the four branch pages against 503bc97c and this round's page against 30eb4834. Its planted control (an 11-word sentence in the new note) was caught, rc 1, then restored (evidence/style_control.out).
- Large logs are listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read. Unchanged.
3. The console buffer still rests on S2b's 2.0 ms share; the page gives 128 bytes under 10 ms. When PR #810 merges or the share changes, the buffer is derived again. Unchanged.
4. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
5. The census keeps today's `PSCLK` and PHY reset behaviour. If the owner wants either changed, that is a new decision. Unchanged.
6. For the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3). Unchanged.
7. New, not taken this round: R766-2-S1 (T_svc = 20 ms is an approved owner decision of 2026-10-29; a pass over the share under 20 ms would give 231 characters and a 256-byte buffer), R766-2-S2 (the stage 1 probe figures are Arty A7-100T measurements), R766-2-S3 (`MilanMAC`'s first-party Migen glue, `milan_soc.py:1712-1760` and the AX42 patch, must be carried to the stage 2 MAC).
8. Coverage: this round's change is in Conformance and Docs scope (R766-2-F1's lenses); RTL, Robustness and Tests artifacts are untouched.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| round3.diff | `git diff 30eb4834 HEAD` |
| census_coverage.out | The census coverage check at the working tree before commit (PASS, identical to round 2's output) |
| style_control.out | The style probe's planted control and the clean rerun |
| style_touched.py, make_pr_body.py | The changed-block style probe; builds PR-BODY.md from round 2's |
| write_handoff.py, handoff_body.md | Build this file |
| gates/ | Every step's log and rc, run_all.out, run_all.sh, run_gates.sh, run_extra.sh, setup_clone.sh, service_bounds_arm.py; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.

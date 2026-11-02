# HANDOFF - [A720n] issue #640, PR #835 round 4 (docs only)

Status: REVIEW READY (2026-11-02). All 55 rc files read 0. Head 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2 (tree 94e8b7052d4f4d03b578891691a3df96d2273043), on d52e966bb7258184e33702a9edd9ca11b4b1362c and dev 503bc97cd4f24ad07596c17e7188f2024617972d. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-charter-followup. Started at d52e966b (640-a720m's head, PR #835's round 3 head). `git merge-base HEAD origin/dev` is 503bc97cd4f24ad07596c17e7188f2024617972d.
- **Live dev moved:** origin/dev was e61a4afa at start (fetched). Every diff and gate here is against the briefed base 503bc97c. R765-3 already flags this for the manager: the merge candidate must be validated on current dev, and the census check re-run there (it reads `sw/litex/milan_soc.py`, which those commits change).
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Round 3 reviews: R766-3 POSITIVE (PR #835 issuecomment-6580971431); R765-3 NEGATIVE on one MINOR, R765-3-F1 (issuecomment-6580969269).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6581002965 (text: evidence/taken.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6582338387 (text: evidence/review_ready.md)
- Scratch: $VALIDATION_STORAGE/640-a720n (gate clone, venv copied from 640-a720m, fresh scratch HOME with a freshly installed pinned SDK). Evidence: ./evidence/.
- Page changed this round: docs/design/MARK_II_AREA_PLAN.md (AP) only, 3 lines changed (3+, 3-). No RTL, firmware, generator, gate or configuration file. AP is not gate-read; the two gate-read pages are unchanged, and their readers were run again anyway.

## Read this first

1. **No STOP.** The fix follows R765-3-F1's required outcome exactly, and moves no figure: the 18 RAMB36 stay as measured and are booked where M8a-1 books them.
2. **One more double booking was found and fixed the same way: stage 3's "the generated FIFOs".** The census (AP:339-340) says each leaves with its block. By the basis build's synthesis mapping (evidence/fifo_owners.txt), none of the 29 belongs to a stage 3 row: 16 DDR3 (stage 1), 5 Ethernet (stage 2), 8 processor memory-path crossings (switch-over). Public text gives no per-stage split, only "leave earlier, each with its block".
3. **The owner's "Change" wording stays** ("Drop DDR3 and the BIOS ROM ... This also frees Block RAM", #640 issuecomment-6545999204). Stage 1 still frees Block RAM: DDR3's 16 FIFO RAMB36.
4. **R765-3-R1 and R765-3-S1 are not taken.** The brief limits the round to F1 and says touch nothing else; both are on the open list.

## Commits (one-line subjects, no body, no trailers)

Commits 1 to 13 (640-a720j to 640-a720m) are unchanged; this round adds one:

| # | SHA | Subject |
|---|---|---|
| 14 | 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2 | Stop crediting stage 1 with the BIOS ROM and SRAM's 18 RAMB36 and stage 3 with the generated FIFOs, which leave at the switch-over and with their own blocks, and name stage 1's Change cell as the one keeping the owner's words (#640) |

## Finding R765-3-F1 (Conformance, Docs; MINOR)

| Where (at head) | Was | Now |
|---|---|---|
| AP:231, stage table, stage 1 "Removes" | "LiteDRAM controller and PHY; BIOS ROM and SRAM, 18 RAMB36 measured" | "LiteDRAM controller and PHY. The BIOS ROM and SRAM, 18 RAMB36 measured, already left at the switch-over ([M8a-1](#firmware-and-block-ram-ledger))" |
| AP:233, stage table, stage 3 "Removes" (same cause, found on the re-read) | "Wishbone and CSR-bank glue; the generated FIFOs" | "Wishbone and CSR-bank glue. The generated FIFOs leave earlier, each with its block ([census](#litex-block-census))" |
| AP:235, note under the stage table | "Stage 1's row keeps the owner's words." | "Stage 1's Change cell keeps the owner's words." |

Stage 1's "Change" cell (AP:231) is unchanged: it keeps the owner's words, and the note names it.

### Every per-stage RAMB36 or LUT credit, re-read for the same double booking (AP at head unless named)

| Where | Credit | Booked elsewhere? | Result |
|---|---|---|---|
| AP:231 stage 1 Removes | BIOS ROM and SRAM, 18 RAMB36 | Yes: AP:238, :333-334, :432, :1302; AREA_BUDGET.md:301 at the switch-over | **Fixed** (F1) |
| AP:231 stage 1 Credited as | Lever 1, ~1.0k LUTs | Lever 1 is "Drop DDR3, on-chip main memory" (AP:190), no BIOS LUTs; lane 2 ~1.0k (AP:432) | Agrees |
| AP:232 stage 2 Removes / Credited | LiteEth MAC and LiteSPI; part of the -1.75k | -1.75k is "LiteX stages 2 and 3 beyond levers 1 and 2" (AP:211); lane 4 (AP:434). STREAM_ENGINES.md:911 debits the new MAC's crossing FIFOs at stage 2 | Agrees |
| AP:233 stage 3 Removes | "the generated FIFOs" (29 RAMB36, AP:112, :387) | Yes: AP:339-340, each leaves with its block; DDR3 row (stage 1), Ethernet row (stage 2), processor memory paths (switch-over); none at stage 3 (evidence/fifo_owners.txt) | **Fixed** (same cause) |
| AP:233 stage 3 Credited as | Lever 2, ~1.0k, and the rest of the -1.75k | Lever 2 (AP:191, :461-466) and -1.75k exclusive by AP:211; lane 5 (AP:435) | Agrees |
| AP:112 basis row | 47 RAMB36 = 29 FIFOs + 18 BIOS; "the switch-over and LiteX stages 1 to 3" | Spans stages, credits none | Agrees |
| AP:387-388 | "All 47 are gone once LiteX stage 3 ends" | A bound, not a stage credit | Agrees |
| AP:431 lane 1 | Basis to ~31.0k | The chain (AP:146-153) subtracts no BIOS or FIFO LUTs | Agrees |
| AP:1297-1305 ledger | M8a-1 -18 at the switch-over; no generated-FIFO credit | Only booking of the 18 | Agrees |
| AREA_BUDGET.md:301 | M8a-1 -18 | Same as the ledger | Agrees |

The census coverage check (`census_coverage.py`, R765's run of 640-a720l's script) maps the same objects to the same rows: PASS, output byte-identical to round 3's.

## Gate table

All 55 rc files read 0.

Every run step of `.github/workflows/docs.yml` at 503bc97c (no `.github/` or `scripts/` diff on the branch), as its jobs run it, sequentially, on $VALIDATION_STORAGE/640-a720n/gates/wt: a fresh clone of the lane at 545ac9cb4a4b6981094e4cf6ad1dfffd6a9169f2, with gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77 and verilog-axis 48ff7a7e (depth 1 from 640-a720m's clone, each origin its .gitmodules URL; the same pins as HEAD's gitlinks). Venv: 640-a720m's, copied. RV32 SDK: installed fresh into $VALIDATION_STORAGE/640-a720n/home; the shared SDK was not touched. TMPDIR and RUNNER_TEMP point into scratch. Run 2026-11-02T16:31:25+01:00 to 2026-11-02T17:24:11+01:00. Step list: evidence/gates/run_gates.sh, run_all.sh, run_extra.sh (run_both.sh runs the last two in order).

| Job | Step | Command | rc | Last line |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD`, no .git | 0 | feature_status: 0 finding(s) |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | Wrote: $VALIDATION_STORAGE/640-a720n/gates/runner_temp/milan-hdl-reference/index.html |
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
| (lane) | Markdown gates, pinned venv | `check_em_dash.py --base 503bc97c` | 0 | check_em_dash: 0 finding(s) over 231 added line(s) in 4 changed Markdown page(s), 0 mirrored label(s) exempt, arms 339/339 [503bc97c..HEAD] |
| (lane) | Markdown gates, pinned venv | `check_doc_style.py` | 0 | documentation style: OK (23 current documents) |
| (lane) | Markdown gates, pinned venv | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | TOC gate: OK (152 page(s) carry an annotated contents list, 18 below the 3-section threshold) |
| (lane) | whitespace | `git diff --check 503bc97c HEAD` | 0 |  |
| (lane) | style on changed blocks | check_doc_style's `analyze()` on every changed block of the 4 pages against 503bc97c, and of this round's page against d52e966b | 0 | docs/design/MARK_II_AREA_PLAN.md: 0 finding(s) in changed blocks |
| (reader) | AREA_BUDGET.md's gate reader (rtl-fast) | `syn/ooc/pp_resource_gate.py check-baseline` | 0 | baseline PASS: 3 endpoints |
| (reader) | MAILBOX_SPLIT.md's gate reader (rtl-fast firmware-unit) | `ctrl_service_bounds.arm_service_bounds` via `service_bounds_arm.py` | 0 | rc 0 |
| (lane) | census coverage | `census_coverage.py` over the basis hierarchy, CSR map and placed rows, and the split-only parts | 0 | RESULT: PASS |
| (lane) | census coverage control | `! census_coverage.py` against the round 1 page (3f8ed303): rc 0 means the check failed there, as it must | 0 | RESULT: FAIL |

Notes:
- docs-check's "Require every gate exactly once" verifies uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. Not run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Builder leg 1's 16 NOT RUN arms need migen, LiteX and an Arty report, which the docs workflow never installs; the leg's rc is what counts.
- `style_touched` checks the four branch pages against 503bc97c and this round's page against d52e966b. Its planted control (a 12-word sentence in the note) was caught, rc 1, then restored (evidence/style_control.out). The stage table rows are table cells, which the style rules exempt.
- The clean clone's `git status --short` was empty after both runs (logs/final_status.txt, final_status_extra.txt).
- Large logs are listed in evidence/gates/LARGE_LOGS.txt by sha256 and size, not copied.

## Open list (as it now stands)

1. #640's body still shows 34.2k, 26.9k and 20.7k (640-a720j). Unchanged.
2. Exact-head long gates apply when the PR is ready: AREA_BUDGET.md and MAILBOX_SPLIT.md are gate-read. Unchanged.
3. The console buffer still rests on S2b's 2.0 ms share; the page gives 128 bytes under 10 ms. When PR #810 merges or the share changes, the buffer is derived again. Unchanged.
4. D21's slot offset and budget wait for the stage 1 lane. Unchanged.
5. The census keeps today's `PSCLK` and PHY reset behaviour. If the owner wants either changed, that is a new decision. Unchanged.
6. For the stage 1 lane: the probe's AX7101 -3,758 LUT figure includes the failing route (R766-1-S3). Unchanged.
7. Not taken: R766-2-S1, S2, S3 (round 3's list). Unchanged.
8. New, not taken this round: R765-3-R1 (AP:239 "hold them" takes the BIOS as its object; exact fix "hold those regions until stage 3"), R765-3-S1 (say where stage 1's loader runs, since `rom` is read-only and holds the reset entry). Carried residue: R765-2-RESIDUE-1 (AP:368) and R765-2-RESIDUE-2 (AP:336).
9. Live dev is at e61a4afa, 18 commits past 503bc97c (R765-3's pending manager duty). The candidate merge must be validated on current dev, with the census check re-run there.
10. Observation, not changed (outside F1): the switch-over's Block RAM ledger (AP:1297-1305) credits no removal for the 8 processor memory-path crossing RAMB36 that the census books to the switch-over. That is an omitted credit, not a double booking; any change belongs to the switch-over lane's ledger.
11. Coverage: this round's change is in Conformance and Docs scope (R765-3-F1's lenses); RTL, Robustness and Tests artifacts are untouched.

## Evidence (./evidence)

| File | What |
|---|---|
| taken.md, taken_url.txt | The TAKEN text as posted, and its URL |
| review_ready.md, review_ready_url.txt | The REVIEW READY text as posted, and its URL |
| round4.diff | `git diff d52e966b HEAD` |
| census_coverage_worktree.out | The census coverage check at the working tree before commit (PASS, identical to round 3's) |
| fifo_owners.txt | The LiteX top's Block RAM rows from the basis synthesis mapping, each memory's owner and census row, and the reconciliation to 47 RAMB36 (log digests recorded) |
| style_control.out | The style probe's planted control and the clean rerun |
| make_pr_body.py | Builds PR-BODY.md from round 3's |
| gates/ | Every step's log and rc, run_all.out, run_extra.out, the run scripts, setup_clone.sh, service_bounds_arm.py; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR creation or edit, merge, rebase, sub-agent, bench, flashing or Vivado. No existing comment edited. Only TAKEN and REVIEW READY posted on #640.

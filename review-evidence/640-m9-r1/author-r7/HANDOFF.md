# HANDOFF - [A720g] issue #640 Mark II charter, round 7 (docs only)

Status: REVIEW READY at head e7310e94fff7188c5800a94c03a3f0e4c7c1c024 (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-6 head 3f5fea241e8dacd976798ca817c67e55096cf1aa (PR #828). Round-7 head e7310e94fff7188c5800a94c03a3f0e4c7c1c024, tree 0a9f7f6a5b8d385fc43116ba0035d384b125b8c7.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (re-fetched after the gates, unchanged); merge base 1f29f189. Round 7 adds 24 lines and removes 24 on 3 pages (3f5fea24..HEAD); against 1f29f189 the PR adds 1,754 and removes 112 over 7 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Owner decision: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558021030 (2026-11-01 13:35), read in full.
- Reviews answered: R757-6 and R758-6 (both POSITIVE at 3f5fea24), read for their residue and suggestions.
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558056220 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558619691 (text: evidence/review_ready_posted.md)
- Scratch: $VALIDATION_STORAGE/640-a720g. Evidence (small files): ./evidence/.

## Commits (one-line subjects, no body, no trailers)

| # | SHA | Files | Group |
|---|---|---|---|
| 1 | 7b3121d234c019ebb596d57e653bcad889cc051a | FR, SE, AP | Owner decision, items 1 to 3 |
| 2 | e7310e94fff7188c5800a94c03a3f0e4c7c1c024 | SE | R757-6 RR11 and R758-6-R1 |

`FR` = docs/reference/FR_NFR.md, `SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md. No rebase, no amend, nothing pushed.

## Changes (file:line at e7310e94)

| Change, file:line | Source |
|---|---|
| FR:306 "SHOULD be below 65 µs, and as short as possible" | Owner decision 2026-11-01; assignment item 1 |
| FR:306 cites the decision: "makes 65 µs a target that does not bind every legal stream setup" | Owner decision, its first bullet |
| FR:306 "Those derived bounds are accepted and published, and no connection is refused because of them." replaces "not met by the design ... open owner question" | Owner decision; assignment item 1 |
| FR:306 "The bench measures against the target and reports each case; a case above 65 µs that stays inside its published bound is not a failure." | Assignment item 1, as written |
| FR:306 priority column M to S | The file's legend, FR:19-21: S=SHOULD. A SHOULD row marked M would contradict it |
| SE:224 "sets a 65 µs target" | Owner decision |
| SE:227-234 the decision, stated once on the page, in the talker budget's opening | Owner decision; assignment item 2 |
| SE:389 "Mixed formats do not; the [owner's decision](#talker-latency-budget) accepts their bounds." | Assignment item 2, pointer "around line 380" |
| SE:1225-1248 question 1 removed; the remaining six numbered 1 to 6 | Assignment item 2 |
| AP:60 target row: "Target: below 65 µs ..., as short as possible"; "whose bounds the owner accepted"; the link to `#open-questions` is gone | Assignment item 3 |
| AP:255 D14: "[owner, 2026-11-01]: 65 µs is a target"; "those bounds are accepted and published, and no connection is refused because of them" | Assignment item 3 |
| SE:636-637 "Both copies' margins under about 125 µs lapse every head." "The threshold carries the conversion error, so it is approximate." | R757-6 RR11; R758-6-R1 |
| SE:639-640 the "Interleaved copies" line moved into the pointer's paragraph; both sentences unchanged | The two-sentence paragraph limit; "that case" still names the interleaving |
| SE:1183 item 3: "A margin under about 125 µs on both networks lapses the head before the next packet"; "The threshold carries the conversion error: within that error of 125 µs, only some packets lapse." | R757-6 RR11; R758-6-R1 |
| PR body, known limitations, Status, talker results, Round 7 section | Assignment item 5 |

Unchanged: the bounds tables and every figure, the "Against 65 µs" columns, `SE_TLAT_OVER`, the merge rules, every register, every other page. Open owner decisions 1 to 3 in the area plan and the other design questions stay open, as the owner states.

## Decisions taken inside the assignment

- **The pointer "around line 1142" is not changed.** The assignment names it as a pointer to question 1. It is not one: SE:1151-1152 follows "A burst beyond S1 ..." and points to the save burst question. That stays open, now as question 1 on the same list, and the link still resolves. Rewording it would touch an open owner decision. This is the one place the round departs from the assignment's text.
- **Priority S at FR:306.** The assignment says "the file's own requirement wording" and keep the rest of the row. The legend ties the column to the keyword, so it follows the keyword.
- **The "Against 65 µs" columns keep "Met" and "Not met".** They read a figure against the target. No line there presents the result as awaiting the owner, and the assignment keeps the tables.
- **The verification row SE:1159 is unchanged.** It names what the bench runs, not a pass condition; FR:306 carries what the bench records.
- **FR:306 states nothing for a case above its published bound.** The assignment and the decision do not. The bounds are upper limits, so such a measurement would contradict the analysis; the row does not call it a failure in words.
- **RR11 and R758-6-R1 give different exact texts.** The assignment asks for both points, with "about 125 µs". SE:636 is RR11's sentence with "about", rewritten to stay at 10 words. R758-6-R1's "within the conversion error of 125 µs, only some packets lapse" is kept at SE:1183, where tables allow it. Its "well under" and "first-copy" wording is not used.
- **History rows annotated in the PR body.** Rows that would read as current now carry a note: commit `872ff20e`, the Round 6 closure, R757-2 RR1 and the Round 5 suggestions. This is round 6's own precedent, and R757-5 RR10's reasoning.

## Derived numbers

None new. Round 7 changes no figure.

| Text | Basis |
|---|---|
| "about 125 µs", "within that error of 125 µs" | R758-6-R1 arm A: margins of 122.3 to 124.9 µs give 1,595 to 1,660 anchors of 2,000, 125.1 to 127.6 µs give 260 to 335, 127.8 to 130 µs give 1. The page's conversion error bound is 2.744 µs, so 125 ± 2.744 µs covers those bands |
| "both networks" | R757-6 RR11, section C of its receipt: one network at 150 to 200 µs and the other at 10 to 50 µs gives 1 anchor and 0 shifts |

## Finding closure

| Item | Closed by | Verification |
|---|---|---|
| Owner: 65 µs is a target | FR:306, SE:224-234, AP:60, AP:255 | Read against the decision; `git grep` finds no "MUST be below 65", no "open owner question" on latency, and no link to `#open-questions` outside SE:27 and SE:1152 |
| Owner: requirement text approved | PR body Status | "needs owner approval" no longer appears in PR-BODY.md |
| Open question 1 | SE:1225-1248 | No reference by number remained on the pages; the PR body's "(open questions 1 and 7)" is updated |
| R757-6 RR11 | SE:636, SE:1183, PR limitation | All three say both networks or both copies |
| R758-6-R1 | SE:636-637, SE:1183, PR limitation | All three say about 125 µs and that the threshold carries the conversion error |

### Suggestions

R757-6 S14 to S16 and R758-6 S1 to S4 are not taken: the assignment says touch nothing else. All are optional.

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720g/gates/wt at e7310e94fff7188c5800a94c03a3f0e4c7c1c024 (tree 0a9f7f6a), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, their module directories copied from round 6's scratch clone, each origin its .gitmodules URL). Gate venv: round 6's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME ("SDK fresh installation: verified"); the shared SDK was not touched. TMPDIR pointed at scratch. dev is unchanged since round 6's base (1f29f189), so the workflow is too. After the run the clone's status was empty and its gitlinks unchanged. All 50 rc files read 0. Logs and rc files: ./evidence/gates/.

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 213 md + 1436 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 1f29f189` (merge base with live dev) | 0 | 0 findings over 1754 added lines in 7 pages |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | OK; 30 controls |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py --check/--selftest`, `timesync_chain.gen.py --check/--selftest` | 0 | OK |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | 45 controls |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and the three `--check` runs | 0 | current |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | 6 rasters, 28 controls |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | 0 findings |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | up to date, 80 modules |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | PASS |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 | 18 PASS |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check` and `--selftest` | 0 | 0 findings over 1434 files; 867 arms |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK fresh installation: verified |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (690 s) |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 findings, 5 configs |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | OK, 5 shapes |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | 22 arms |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 PASS |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check/--selftest` | 0 | 66 PASS |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 PASS |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check/--selftest` | 0 | 106 PASS |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 PASS |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check/--selftest` | 0 | 105 PASS |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check/--selftest` | 0 | 35 PASS |
| docs-gates-0 | gate_37 to 40 idioms | `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest` each) | 0 | 55, 75, 54, 48 PASS |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | 1084 paths resolve |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | OK, 24 controls |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 152 pages |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1156 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base 1f29f189`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output, in the clone and rerun in the lane |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over every changed block of the 7 pages against 1f29f189 | 0 | 0 findings |

Notes:
- The 16 NOT RUN arms of leg 1 are round 6's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Each leg's rc is 0.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- /tmp: TMPDIR pointed at scratch. `find /tmp -maxdepth 2 -user alex -newer run_all.start` lists only other sessions' working-directory markers. None is this lane's.

## Evidence (./evidence)

| File | What |
|---|---|
| taken_posted.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| edit1.py, edit2.py | The exact-text edits behind the two commits (commit 1 also took one follow-up edit, for the sentence limit, at SE:227) |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 7 touched pages against 1f29f189 |
| make_pr_body.py | Builds PR-BODY.md from round 6's by exact-text replacement |
| gates/ | Every gate step's log and rc at e7310e94, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt holds the one log over 200 KB by digest and size |
| SHA256SUMS | Digests of every file above |

## Open points for the reviewers and the manager

- SE:1151-1152 left unchanged, against the assignment's text: see "Decisions taken inside the assignment".
- R757-5 S9 stays as round 6 left it: not covered by item 3, and "the pair loses no samples" is unchanged.
- PR #828's live body and head are still round 6's until the manager pushes this round.

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. The shared RV32 SDK in the home directory was not touched.

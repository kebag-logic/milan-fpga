# HANDOFF - [A720h] issue #640 Mark II charter, round 8 (docs only)

Status: REVIEW READY at head 20933ef48a9b174e58a9d17ddd59078a072024af (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-7 head e7310e94fff7188c5800a94c03a3f0e4c7c1c024 (PR #828). Round-8 head 20933ef48a9b174e58a9d17ddd59078a072024af, tree 2299420e70cea4ce2dcb0450c5ff0fbb56bbf9f0.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (re-fetched after the gates, unchanged); merge base 1f29f189. Round 8 adds 45 lines and removes 7 on 3 pages (e7310e94..HEAD); against 1f29f189 the PR adds 1,792 and removes 112 over 7 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Reviews answered: R757-7 NEGATIVE (https://github.com/kebag-logic/milan-fpga/pull/828#issuecomment-6558867513, F1) and R758-7 POSITIVE (https://github.com/kebag-logic/milan-fpga/pull/828#issuecomment-6558924964, R1), both read in full. Their probes read and re-run: R757-7 `probe_fewer_bound.py` (seed 640) and `crosscheck_published_model.py` reproduce the published outputs byte for byte (evidence/witness/).
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6558948950 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6559623221 (text: evidence/review_ready_posted.md)
- Scratch: $VALIDATION_STORAGE/640-a720h. Evidence (small files): ./evidence/.

## Commits (one-line subjects, no body, no trailers)

| # | SHA | Files | Group |
|---|---|---|---|
| 1 | 210c3eb6a68381886d11601c2bb106c6d6f437f0 | FR, SE, AP | Manager's rules 1 to 3 |
| 2 | 20933ef48a9b174e58a9d17ddd59078a072024af | SE | Sentence limit at SE:445, and the probe pointer's verb at SE:447 |

`FR` = docs/reference/FR_NFR.md, `SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md. No rebase, no amend, nothing pushed.

Why a second commit: my first edit script stopped on an ambiguous match, and the command chain committed anyway, so commit 1 carries one 11-word sentence. Commit 2 fixes it; the head has none. The gates ran on the head only.

## Changes (file:line at 20933ef4)

| Change, file:line | Source |
|---|---|
| FR:306 "123.337 µs with three co-phased eight-channel streams" removed from the row | Rule 1: remove wording presenting it as the worst case |
| FR:306 "Those 16-reservation bounds are accepted and published." | Rule 1: no such wording for a class with no bound. The bounds it names are the two figures before it, both in the 16-reservation table |
| FR:306 "With fewer reservations no maximum is derived, and the stream-engine lane owes that derivation." | Rule 1; rule 2's open item; F1 outcome (b) "name who derives it" |
| FR:306 "The largest figure reached there is 143.347 µs, with six co-phased one-channel streams at 48 kHz; it is quoted as reached, not as a limit." | Rule 1 |
| FR:306 "No connection is refused because of any of these figures." | Rule 1; owner decision |
| FR:306 "The bench measures every case against the target and reports it; a case above 65 µs is reported, not failed." | Rule 1 |
| FR:306 "A case is graded against a bound only where one is derived, which is the 16-reservation table; there, a measurement above its bound contradicts the analysis and is a finding." | Rule 1; closes R758-7 S2 as a side effect |
| SE:230-243 the decision's statement says the same in short sentences | F1 names SE:230-231; rule 1 |
| SE:423 "k co-phased equal frames"; SE:425-426 "That form gives no largest k." "It does not cover unequal frames." | Rule 2; F1's text at SE:414 |
| SE:428-436 second table: four cases reached under the exact phase rule, each with its starts and stops | Rule 2; F1's probe table |
| SE:438-439 "The rows of both tables are examples." "None is a maximum." | Rule 2 |
| SE:441-445 fixed terms stated as estimates, with the 96 and 192 kHz values already on the page | F1 "Real limits" |
| SE:447-451 pointer to the published probe and output; the 192 kHz search left out eight-channel streams | Rule 2; F1 "Real limits" |
| SE:1221 open design item 4, requirement and verification | Rule 2 |
| AP:60, AP:255 | Rule 3 |
| AP:276 "Talker latency taps on all talker streams, measured against the 65 µs target" | Rule 3; R758-7-R1; R757-7 RR12 |
| PR body: Fewer reservations line, Status, Known limitations, Round 8 section, annotated round 7 rows | Rule 3 |

Unchanged: the 16-reservation table and the first fewer-reservations table (hashes in evidence/delta_check.txt), every other figure, `SE_TLAT_OVER`, every register, every other page.

## Figures added to the pages

No new derivation. Every figure is R757-7's, and each reproduces.

| Figure | Basis | Check |
|---|---|---|
| 143.347 µs, wait 103.022 µs | F1; 103.022 + 40.325 | witness.py: model queue recursion and event-exact simulation agree |
| 111.635 µs, wait 71.310 µs | F1; 71.310 + 40.325 | Same |
| 125.426 µs, wait 92.935 µs | F1; 92.935 + 32.491 | Same |
| At least 102.034 µs, wait 83.941 µs | F1; 83.941 + 18.093, before the packetizer term | Same |

## Decisions taken inside the assignment

- **A second table, not extra rows in the first.** The first table's header says eight-channel at 48 kHz and has no witness column. Leaving it alone keeps its hash, so a reviewer can see no old figure moved.
- **The columns are the reviewer's: wait and total.** idleSlope and "with interference" would add figures the assignment does not need.
- **Two witness sequences are mine.** The probe's random walks print only the final placement, so rows 2 and 4 needed a sequence. Row 2: start eight-channel (phase 0), one-channel (phase 3), one-channel (phase 1); stop the phase 3 stream. Row 4: start five one-channel (phases 0, 12, 6, 18, 3), one six-channel (phase 9); stop phases 0, 3, 6, 18. The published model's `greedy_add` reaches each stated phase (evidence/witness/witness.out). Rows 1 and 3 are the reviewer's sequences.
- **SE states the grading rule as well as FR.** F1 outcome (b) names SE:230-231 for what the bench does. FR stays the authority.
- **The decision's wording.** The owner's text says bounds "for fewer reservations are accepted". The pages no longer say that, by rule 1. The PR body records that the decision was taken on 123.337 µs. The acceptance and no-refusal decisions are not reopened.

## Open points for the manager

- **192 kHz row is not the largest known figure at that rate.** R758-7 S1 reaches at least 106.927 µs (eight-channel in phase 3, one-channel in phase 6, wait 88.834 µs); witness.py reproduces both figures. The rule names R757-7's "at least 102.034 µs" and "no other figure changes", so no page carries 106.927. The page calls its row an example that may be low, and item 4 covers eight-channel at 192 kHz. The PR body's Round 8 section states this. 143.347 µs remains the largest overall.
- **"The manager has told the owner" rests on your instruction.** The PR body says so as ruled. No comment on #640 or #828 records it when this was written, and this lane cannot verify it.
- **The owner's decision text still says bounds for fewer reservations "are accepted".** A cold reader meets that on #640, next to pages saying no such bound exists. R757-7 RR13 (issue body) is the manager's, as is any note on this.
- **Reviewer labels.** SE:447 links review evidence by pinned commit, as SE:1220 and SE:1260-1261 already do.
- The R757 and R758 ledgers must be re-covered at this head: the delta touches the scope of every lens they named for F1. This commit changes no RTL.

## Finding closure

| Item | Closed by | Verification |
|---|---|---|
| R757-7-F1 | FR:306; SE:230-243, SE:423-451, SE:1221; AP:60, AP:255; PR body. Outcome (b) | Re-run probes: every witness is covered by the stated rule for a case with no bound. `git grep 123.337` finds only the unchanged SE:416 row |
| R758-7-R1, R757-7 RR12 | AP:276 | Read against FR:306 |

Not taken: R758-7 S1 (a ceiling; that is item 4), S3; R757-7-S2; R757-6 S14 to S16; R758-6 S1 to S4. R757-7 RR13 is the manager's. R757-7-S1 enters only through item 4's verification.

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720h/gates/wt at 20933ef48a9b174e58a9d17ddd59078a072024af (tree 2299420e), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, copied from round 7's scratch clone, each origin its .gitmodules URL). Gate venv: round 7's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME ("SDK fresh installation: verified"); the shared SDK was not touched. TMPDIR pointed at scratch. dev is unchanged since round 7's base (1f29f189), so the workflow is too. After the run the clone's status was empty and its gitlinks unchanged. All 50 rc files read 0. Logs and rc files: ./evidence/gates/.

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 213 md + 1436 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 1f29f189` (merge base with live dev) | 0 | 0 findings over 1792 added lines in 7 pages |
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
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (710 s) |
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
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1171 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base 1f29f189`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output, in the clone and rerun in the lane |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over every changed block of the 7 pages against 1f29f189 | 0 | 0 findings |

Notes:
- The 16 NOT RUN arms of leg 1 are the same as round 7's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Each leg's rc is 0.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- /tmp: TMPDIR pointed at scratch. `find /tmp -maxdepth 2 -user alex -newer run_all.start` lists only /tmp/milan-bench.lock. This lane's scripts and logs do not name it, and this lane ran no bench.
- Another lane's sweep ran on the host at the same time. This lane ran no parallel sweep.

## Evidence (./evidence)

| File | What |
|---|---|
| taken_posted.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| edit1.py, edit2.py | The exact-text edits behind the two commits |
| delta_check.txt | Table hashes across both heads, name-status, modes, remaining 123.337 and "accepted and published" hits |
| witness/witness.py, witness.out | Each row's sequence through the published model's phase rule and both wait calculations, plus R758-7 S1's 192 kHz case |
| witness/rerun_*.out | The reviewer's two probes re-run; each equals its published output |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 7 touched pages against 1f29f189: 0 findings |
| make_pr_body.py | Builds PR-BODY.md from round 7's by exact-text replacement |
| gates/ | Every gate step's log and rc at the head, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt holds the one log over 200 KB by digest and size |
| SHA256SUMS | Digests of every file above |

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. Every figure here is derived or a probe's output; none is a measurement.

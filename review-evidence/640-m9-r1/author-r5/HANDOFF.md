# HANDOFF - [A720e] issue #640 Mark II charter, round 5 (docs only)

Status: REVIEW READY at head 270866ecb95155ef48428ec3a049c357f7eae946 (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check 1f29f189 HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-4 head 22f3cedb420992b7b776c5a842b0b210ac4191d3 (PR #828). Round-5 head 270866ecb95155ef48428ec3a049c357f7eae946, tree 6d63bab078834cb3112d3002665f1c2efd9051ca.
- Base: live dev 1f29f189279f9fc0132f4918e47342b87d22f33a (fetched 09:34 CET, unchanged, 0 commits ahead); merge base 1f29f189. Round 5 adds 75 lines and removes 105 over 2 pages (22f3cedb..270866ec); against 1f29f189 the PR adds 1,748 and removes 112 over 7 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6555599350 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6556148840 (text: evidence/review_ready_posted.md)
- Reviews answered: R757-4 (PR #828 issuecomment-6555468647) and R758-4 (issuecomment-6555558017), both read in full.
- Manager ruling applied: reduce, do not patch; no new mechanism.
- Decisions re-read: #640, #665 and #823 bodies and comments fetched 09:34 CET. No owner comment after 2026-10-31. The 2026-11-01 comments are lane TAKEN, STOP and REVIEW READY posts, two manager rulings on #665 about the dev-soft-core sync, the daily area measurement and the LiteX stage 1 probe; none touches this round.
- Scratch: $VALIDATION_STORAGE/640-a720e (standards text, gate clone, gate venv copied from round 4, a fresh scratch HOME for the pinned SDK). Evidence (small files): ./evidence/.

## Commits (one per finding group, one-line subjects, no body, no trailers)

| # | SHA | Files | Finding group |
|---|---|---|---|
| 1 | d22e071d2fdd5c72dee2fb7d6933d19940520026 | SE, AP | R757-4-N6, N7, RR5; R758-4-F1, F2, R2 |
| 2 | 7906c586eb939fd233615fcae7a311c8927315f6 | SE | R757-4 RR6, RR7 |
| 3 | 270866ecb95155ef48428ec3a049c357f7eae946 | SE | Group 1 follow-up: TU-2 says a clean copy renders as the rules place it (a discarded duplicate would otherwise read as breaking it); case B takes the model's 60 to 180 µs latency |

`SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md. No rebase, no amend, nothing pushed. docs/reference/FR_NFR.md does not change, see below.

## What left the page and what stayed (file:line at 270866ec)

| Change, file:line | Source |
|---|---|
| SE:611-617 "Copies with tu set" keeps only IEEE 1722-2016 4.4.4.7's meaning and a pointer: "This page fixes no merge mechanism for those copies." The count, the reference and rule 4's span check left | Manager ruling |
| SE:632-635 the rules take clean copies; rule 1's format check also takes every tu copy (Milan v1.2 4.4.2.2 has no tu exception); item 2 owns tu copies past that check | Manager ruling; Milan v1.2 4.4.2.2 |
| SE:637-646 six rules: stream checks, no valid head, more than 21 packets from the head, newer, older, duplicate. Round 4's rules 2 and 4 and rule 5's `ANCHOR_TU` branch left; the rest renumbered | Manager ruling |
| SE:648 "The head takes its copy's own time."; the tu head's advance by count left | Same |
| SE:654-655 Annex D.2: "The merge keeps that external behaviour for clean copies." D.2: "implementation can be different as long as the external behavior is the same". "Clean partner data is a non-empty buffer there" left with rule 2 | Milan v1.2 Annex D.2, read this round |
| SE:657-663 unpaired stream and pairing paragraphs moved out of upkeep, before "Head upkeep"; SE:659-660 "Milan v1.2 Annex D.3 covers losing one network. While the other stays clean, the pair loses no samples." The tu sentences left | Milan v1.2 Annex D.3 |
| SE:665-674 "Reference upkeep" is now "Head upkeep"; its tu reference sentences left; SE:670 the sweep clears a stale `HEAD_VALID` | Manager ruling |
| "tu on both networks" section (round-4 SE:700-738) removed whole | R757-4-N6, R758-4-F1 |
| SE:744-746 `SE_MERGE_DUP` is merge rule 6, `SE_MERGE_SEC` rules 2 to 5, both of clean copies; `SE_MERGE_TU` left; 0x038-0x03C reserved | Manager ruling: tu-only registers |
| SE:816-818 `LCTX_STATE`: SEQ keeps its Milan v1.2 5.3.8.10 `SEQ_NUM_MISMATCH` use with the tu reference text gone; `ANCHOR_TU`, `SEQ_VALID`, `CLEAN_VALID`, `LAST_TU` left; 31:9 reserved | Same |
| SE:819 `LCTX_LAST_PT` loses "a tu head advances by count"; SE:833 `LCTX_SEQ_PT` and `LCTX_CLEAN_PT` left, 0x48-0x7C reserved | Same |
| SE:1148 verification row "Listener merge, clean copies": every clean case kept, every tu case moved to item 2; mutations are the exact compare and own-time placement | Manager ruling |
| SE:1149 row "Copies with tu set" points to item 2 | Same |
| SE:1167 open design item 2 replaces round 4's "Restart during tu": one item, owned by lane 6 per SE:1161 | Manager ruling |
| SE:1169-1207 item 2's requirements, loss table, named cases, model pointer | Below |
| AP:276 lane 6's evidence column gains the open design items | Makes the ownership readable from the plan; no figure changes |

Stayed, unchanged: the 62.5 µs window and neighbour argument (SE:600-609), the 2.744 µs bound (SE:530-577), the pairing (SE:489-505), the duplicate count of clean copies, the render span (SE:449-485), open design item 1 (SE:1166). Every latency, save, area and Block RAM figure.

## Requirements in item 2 (SE:1176-1180), each cited, read in the standards this round

| Id | Manager's | Clause read | Verification named |
|---|---|---|---|
| TU-1 | (a) | IEEE 1722-2016 4.4.4.7: "may stop attempting to correlate AVTP Presentation Time to gPTP time"; Milan v1.2 4.4.2.3: "should continue to let its media clock free-wheel for an appropriate amount of time" | Cases A to D; fails if a tu copy's skew alone changes which samples render or where they land, apart from an anchor TU-4 states; a servo simulation fails if the media clock adjusts inside the stated free-wheel time |
| TU-2 | (b) | Milan v1.2 Annex D.2: "it renders one or the other, depending what is available"; IEEE 1722-2016 4.4.4.7: "to prevent unacceptable disturbances" | Case E; fails if a tu copy overwrites clean data or keeps a clean copy from rendering |
| TU-3 | (c), plus round 4's restart requirement, which no finding disputes (R757-4 focus 5; R758-4 S2 calls it right and verifiable) | Milan v1.2 4.4.2.1 and 5.3.8.10; IEEE 1722-2016 4.4.4.6: "may start at any value for the first AVTPDU" | Cases K and L; every write checked against the render point |
| TU-4 | (d) | IEEE 1722-2016 4.4.4.6: "may join a stream at any time"; 4.4.4.7 | Case G; fails if a stream receiving every packet renders only isolated packets |
| TU-5 | (e) | Milan v1.2 Annex D.3: "limited to the loss of connectivity"; GM_LOSS_RECOVERY.md:218 and :333 (one 1.5 s step), :190 (tu held at least 0.25 s) | Every case, in model and on bench; loss table SE:1184-1186 reads "To be set by lane 6" |

## Named cases (SE:1193-1204): where each reviewer's probe went

| Case | Reviewer's source |
|---|---|
| A | R757-4-N6 rows 1 to 4; 1.5 s added under the manager's (e) |
| B | R757-4-N6 row 5; R758-4-F1(a) first part. The model's primary latency is 60 to 180 µs (`merge_model.py:195`), so the reviews' "primary's latency" and "60 to 180 µs" are one setup |
| C | R758-4-F1(a) default latencies; round 4's plus and minus 5 and 200 µs |
| D | R757-4-N6 row 6 |
| E | Round 4's one-network tu rows; R758-4-R2's 1 % loss; the bench row "a grandmaster change on one network with both up" moved from SE:1219 |
| F | R757-4-N6 row 7; round 4's cut then grandmaster change |
| G | R757-4-N7 Arm B; R758-4-F2 |
| H | R758-4-F1(b) |
| I | R758-4-F1(c); round 4's clear-together time step |
| J | Round 4's onsets and short periods; the bench row "tu on both by one talker" moved from SE:1219, its "no lost samples" removed |
| K | R757-4 RR5; round 4's plus and minus 40 jumps |
| L | Round 4's open design item 2; R758-4 S2 (a clean partner losing frames) |

The model pointer (SE:1206-1207) links the merge model of rounds 4 and 3 and both reviewers' probes at commit-pinned public evidence paths, commit b250a616 (tip of the public evidence branch, 2 ahead of the reviews' 993a5bb5, 0 behind). docs/testing/ASSERTIONS.md:153 and TESTING.md:326 use the same link form. Nothing of the model enters the repository.

## Finding closure

| Finding | Closed by | Verification |
|---|---|---|
| R757-4-N6, R758-4-F1 | No no-loss or gap statement about tu remains (round-4 SE:695, :711-712, :721, :723-738, :1219 bench); rule 1 no longer reads a tu copy's time (SE:632); TU-1 and TU-5; cases A to D, F, H, I | evidence/claims_grep.txt: every removed phrase and tu-only name counts 0 on SE, AP, FR and the split page. Its one "loses no sample" hit is SE:660, clean copies under Annex D.3 |
| R757-4-N7, R758-4-F2 | The sentence "A tu copy with no valid reference cannot make one" left with the reference; TU-4 requires the render and has the lane state how; case G | claims_grep.txt "cannot make one" 0; SE:1179, SE:1199 |
| R757-4-N8, R758-4-R1 | PR body Round 4 row "Merge model" reads "removing rule 4 fails 7". Round-4 handoff stays as published | evidence/model/mutation_count.txt: re-run of the unchanged model prints `no_rule4: caught by 7`, as published `merge_model.out:39`. The re-run output equals the published file but for its appended `rc=0` line |
| R758-4-R2 | SE:650 reads "Past rule 1, a packet's only clean copy always renders." as written. The second sentence ("Rule 2 and rule 4 drop only tu copies.") is not applied because those rules are gone; TU-2 carries what remains | Text compare with the finding |
| R757-4 RR5 | Round-4 SE:730, :735-736 are gone; case K names a jump on both networks | claims_grep.txt |
| R757-4 RR6 | SE:975 as written | Text compare |
| R757-4 RR7 | SE:937 as written | Text compare |

FR_NFR.md: `grep -n` for `tu`, "listener merge" and "timestamp uncertain" finds nothing in it (claims_grep.txt), so there is no matching claim to remove and the file does not change.

PR body: the Round 4 rows R758-3-F1, R758-3-F2, Merge model and RR4 are restated as history; the Round 3 and Round 4 intros say round 5 removed the tu text; known limitations state no loss figure for tu; the models line calls the merge model a known-failing starting point. `grep -n "loses no sample"` on PR-BODY.md: no hit.

### Suggestions

| Item | Taken? | Reason |
|---|---|---|
| R758-4 S2 | Part | The clean partner losing frames is in case L. Naming candidates for the restart signal is not taken: TU-3 leaves it to the lane, under "add no new mechanism" |
| R757-4 S4 | Not taken | Optional; this round only reduces |
| R757-4 S5, R758-4 S1 | Not taken | Both ask for one clause in NFR-REL-03 ("A reported flash fault is outside this bound"). That is requirement text, so it is for the owner's approval. Both reviewers accept the reading |
| R757-4 S6, R758-4 S3 | Not taken | Optional; a rule for a persistently failing header or a full old slot adds save-path text |
| R757-4 S7 | Not taken | The PR body keeps it as a known limitation |

## Derived numbers

- 56 octets (SE:1172): the listener context is 128 octets; 0x48 to 0x7C inclusive is 128 - 72 = 56.
- 1.5 s (SE:1180, :1186): GM_LOSS_RECOVERY.md:218, "drives one 1.5 s grandmaster step". TIME_SYNC.md's step policy has no upper bound, so this is the largest step the page grades.
- Removed registers change no ledger row: listener contexts stay 32 x 128 octets, 1.0 tile.
- No tu figure stands on the page. Case parameters (skews, latencies) are inputs.

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720e/gates/wt at 270866ecb95155ef48428ec3a049c357f7eae946 (tree 6d63bab0), a fresh clean clone of the lane with the four submodules the jobs fetch (gptp-processor 135afd04, protocol-processor a9e84b66, tsn-c-stack 70936b77, verilog-axis 48ff7a7e, cloned from round 4's scratch clone, each origin set to its .gitmodules URL). Gate venv: round 4's, copied. The pinned RV32 SDK was installed fresh into this lane's scratch HOME ("SDK fresh installation: verified"); the shared SDK was not touched. TMPDIR pointed at scratch for this run. dev's workflow is unchanged from round 4's base. After the run the clone's status was empty and its gitlinks unchanged. All 50 rc files read 0. Logs and rc files: ./evidence/gates/.

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 213 md + 1436 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base 1f29f189` (merge base with live dev) | 0 | 0 findings over 1748 added lines in 7 pages |
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
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (681 s) |
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
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 152 pages; 580 cross-page links reproduced |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1139 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base 1f29f189`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check 1f29f189 HEAD` | 0 | no output |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over every changed block of the 7 pages against 1f29f189 | 0 | 0 findings |

Notes:
- The 16 NOT RUN arms of leg 1 are the same as round 4's: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. Each leg's rc is 0; the verdict is judged on the union of the legs.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- Setup: protocol-processor's scratch source is shallow, so `--reference` refused it; it was cloned with `--depth 1` over `file://`. Its commit is the pinned gitlink. The lane's own origin was not touched.
- /tmp: `find /tmp -maxdepth 2 -user alex -newer run_all.sh` lists only the shell's working-directory markers, nothing of this lane's gates.

## Evidence (./evidence)

| File | What |
|---|---|
| claims_grep.txt | Removed phrases and tu-only names, counted on the four pages; tu claims in FR_NFR.md |
| model/mutation_count.txt, model/merge_model_rerun.out | The round-4 merge model re-run unchanged, in scratch; its mutation counts |
| style_touched.py, style_touched.log | check_doc_style's analyze() over every changed block of the 7 touched pages against 1f29f189 |
| taken_posted.md, review_ready_posted.md | The TAKEN and REVIEW READY texts as posted |
| gates/ | Every gate step's log and rc at 270866ec, run_all.out, run_all.sh, run_gates.sh; LARGE_LOGS.txt |
| SHA256SUMS | Digests of every file above |

## Open points for the reviewers

- TU-4 and TU-1: a stream that starts with tu has no clean time, so an anchor by its own time may be the lane's choice. TU-1's test excepts "an anchor TU-4 states" for that reason.
- The named cases keep the reviewers' parameters. The expected results stay out on purpose: the manager's ruling makes them lane 6's output.
- Round 4's mutations (`no_rule2`, `r3_rule2`, `no_rule4`) left the verification row with the rules they test.

## Not done / not allowed

No push, PR edit, merge to dev, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. No reviewer finding argued; none reopened. The shared RV32 SDK in the home directory was not touched.

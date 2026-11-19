[R872] POSITIVE - exact head a16899b1fb2a0c731ebf18476d1a38627254ea4e

External independent review R872-2, PR #953, issues #943 and #665. Tree: `4a56ad08834166f69a5ef066b727978485ac0188`. All five lenses were applied to the delta and its dependencies. No open BLOCKER, MAJOR or MINOR remains within this review's scope. This is a source-review verdict, not completion of the train's validation or authorization to merge.

The independent pass examined the full `0839453f..a16899b1` diff and history, concentrating on `502b041c..a16899b1`: commits `106c7203` and `a16899b1`, eight changed files. Production firmware, HDL, mailbox contract, dependency pins, bounds and cost statements do not change in this round. Existing behavior outside the delta retains its prior verdict. After recording my independent assessment and ledger, I read the prior public finding sections and reconciled every named item below. I did not read the other reviewer's report or private author material.

Authorities: AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md section 1, docs/reference/FR_NFR.md sections 3.4.1/3.4.2, aecp.h's brief-observation contract, aecp_face.c:162, and the scoped Milan/IEEE clauses recorded on #943. Public scope and decisions are captured in public-scope.json, including [the original scope ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7007273447) and [the subsequent margin ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-7018568112).

**Prior findings, independently resolved**

| Prior item | Disposition at this head | Evidence and cause-level check |
|---|---|---|
| R872-1-F1, MAJOR; Conformance, RTL, Robustness, Tests | RESOLVED | declaring_outputs.py:69 preserves brief and supplies declaring flags; its bridge-source entry is instrumented. :124 builds the five groups, :246 checks record execution, :261 checks answered/refused paths and completion in THE RETRY. record_classes.py:192 holds completion-running records and :264 requires completed paths. Published normal and planted runs cover both required points. |
| R872-1-F2, MINOR; Tests, Docs | RESOLVED | The fixture saves/restores brief across memset. The published bridge probe returns brief=1 with zero source calls, then a whole observation with one source call and the expected destination. Map/long-command records count zero completions. The live PR and #943 comment 7018504570 explicitly withdraw 325/1,920 us from the old experiment and reject its placement-only explanation. |
| R872-1-R1, RESIDUE; Docs | RESOLVED | live-pr.json records base flip-train-1117, step 13, filled internal/external roles, and conditional future retargeting. |
| R871-F1, MINOR; Tests | RESOLVED | test_aecp.cpp:900 registers a matching stream on the wrong interface first; :914 checks the whole flags word under Ready, Ready Failed and Asking Failed. aecp_output_mutants.py:44 and :66 plant unwanted MSRP_FAILURE_VALID and either-interface registration. The published 1x1/2if receipt catches both by their intended assertion words; all 17 rows are caught at that campaign shape. |
| R871-S1, SUGGESTION; Tests | IMPLEMENTED; margin disposition below | The maintained arm registers output 0's Listener and grades completed paths at both points. Its original experimental figures are superseded, not reused as placement proof. The public ruling requires separate margin recovery and final-image measurement. |
| R871-S2, SUGGESTION; Docs | RESOLVED | Current receipts cover 17 rows at 1x1/1if, 1x1/2if and 8x8/1if. The live PR explicitly supersedes round one's intermediate receipts. At one interface, the two interface-selection plants are equivalent and are identified as such, not counted as successful kills. |

**Completion coverage and measurements**

The completion marker is on the bridge's ACMP source callback, before the original source query. Inside the measured AECP handler or retry-round span it witnesses completion work, rather than merely observing a response field. The ordinary command groups remain present. The added group exercises GET_STREAM_INFO for every output, SET_STREAM_INFO refused NOT_SUPPORTED and ENTITY_LOCKED after whole observation, an accepted SET_STREAM_INFO whose fan-out exceeds ring room behind held egress, the GET queued behind it, and the declared Talker's unsolicited notice in THE RETRY. Response checks and fan-out recipients remain in the ordinary service grader.

| Published declaring-arm result | 1x1/1if | 8x8/1if |
|---|---:|---:|
| Groups / budget misses / refusals | 5 / 0 / 0 | 5 / 0 / 0 |
| Probe instances | 57 | 62 |
| Completions in aecp-outputs records | 6 in 6 records | 13 in 13 records |
| Completions in retry rounds | 1 | 1 |
| Output GET_STREAM_INFO responses/notices examined | 19 | 26 |
| Declared notice to final recipient | 1.337 ms | 1.615 ms |
| Held SET's final notice / held GET response | 9.104 / 4.068 ms | 9.138 / 4.103 ms |
| Dearest held completed record | 23,330 cycles; 245/245 us | 20,707 cycles; 220/265 us |
| Work passes over 2 ms share | 0/839 | 2/845 |

The two 8x8 share exceedances are in aecp-largest-notice, whose records do not run completion. The recorded peak is 2.284 ms, within the prior arm-B observed range 2.224–2.321 ms. They are recorded exceedances, not passing share measurements. No new service-budget miss or stated retry-round-cost miss appears in the receipts. round_grade.py:59 still charges the complete round against cold-start, notice and refused-attempt costs; the new arm uses the existing grading path in run.py:931 and :987.

The three negative controls discriminate the intended causes at both points: completion-unexecuted produces 7/14 missing-completion findings; brief-completed produces three offending command-record findings at each point; completion-dearer produces 7/14 held-record overruns, including 525 us against 245 us. All six receipts say caught with zero refusals. Removing the declaring leg makes each record-class pass fail for its three missing completed paths. These are execution/measurement failures, not compile failures or unrelated refusals. Combined class passes include all 99/98 arm-A groups and the required answering arms.

**Margin judgment**

The risk is real and must not be presented as final-image margin. The declaring fixture counts zero completions in records measuring 30,226 cycles (320 us by rule, statement 310) and 167,522 cycles (1,760 us, statement 1,720). Unlike the withdrawn experiment, this fixture preserves brief. These observations support placement sensitivity, not a quantitative estimate of the production completion's isolated cost.

My independent margin-probe.txt confirms that a 320 us paced statement makes the 1x1 last-queued-notice row 141.47 ms against 140 ms; 325 gives 141.54 ms. At 340 us, that row is 141.77 ms and ACMP is 32.75 ms against 30 ms. The held SET record has only three cycles before the rounding threshold: 23,333 still gives 245 us; 23,334 gives 250 us.

I accept #943's correction and maintained completion proof as a train component. I do not accept carrying these numbers unchanged into final-image qualification. The scoped measurement contract holds the newly exercised completed records; non-completion commands remain measured in established arms, and alternate placement is explicitly reported. No new production or statement change hides the variation in this delta. The subsequent public ruling does not waive the risk: it requires margin-recovery work before final measurement, including worse-case projections and no borrowing statements from a luckier image. That ordered work and the final candidate's own measurements remain mandatory. This verdict does not convert a failed final-image bound into an accepted limitation.

**New items**

**R872-2-R1 — RESIDUE — Docs — tb/verilator/ctrl_service_budget/declaring_outputs.py:296 — reviewer identity in a source explanation.**

Authority/evidence: the owner's source-comment rule prohibits reviewer IDs and review-round labels; the new docstring names R872-1-F2.
Impact: source-history wording only; no behavior, measurement, assertion, figure or clause claim changes.
Exact required outcome: replace `(a brief observation that leaves it cleared is completed, R872-1-F2)` with `(a brief observation that leaves it cleared is completed; #943)`.
Verification: inspect the added docstring and confirm the behavior/reason remains while the reviewer reference is gone. This residue does not unclean a lens.

**R872-2-S1 — SUGGESTION — Docs — PR #953 Status and How to validate; author-r2/PR-BODY.md:33 — distinguish docs gates from SDK setup verification.**

Authority/evidence: the body summarizes docs gate steps as rc 0. The handoff, issue comment and author-r2/receipts/docs/docs-gate-steps-a16899b1.txt explicitly disclose three SDK verification setup failures, alongside setup/recorder skips. The summary can be read as including those steps.
Impact: readers may mistake a gate-only summary for completely successful workflow reproduction. The underlying results are already disclosed; no new execution failure is alleged.
Suggested outcome: use “Executed docs gate checks returned 0; the three SDK provenance verification steps refused, and the receipt lists setup/recorder skips.” Retain the separate firmware-boundary refusal and unchecked completion items.
Verification: compare with the three rc=1 entries and published handoff. No source rerun or verdict change is requested by this clarification.

**Reviewer-owned lens ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts and basis | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | declaring_outputs.py:124, test_aecp.cpp:900, FR_NFR 3.4.1/3.4.2; required completed response/notice paths, frozen bounds and scope rulings | R872-2 | a16899b1fb2a0c731ebf18476d1a38627254ea4e |
| RTL | CLEAN | build.py:239, declaring_outputs.py:69, ctrl_app_aecp.c:49, aecp_face.c:162, round_grade.py:59; fixture/bridge boundary, span accounting, fan-out and costs; full diff has no HDL/mailbox/pin changes | R872-2 | a16899b1fb2a0c731ebf18476d1a38627254ea4e |
| Robustness | CLEAN | declaring_outputs.py:159, :246, record_classes.py:192; successful/refused/backpressured responses, retry execution, omitted completion and brief controls; unchanged reset/withdrawal behavior retained | R872-2 | a16899b1fb2a0c731ebf18476d1a38627254ea4e |
| Tests | CLEAN | test_aecp.cpp:900, aecp_output_mutants.py:44, declaring_outputs.py:351, record_classes.py:264; two formerly surviving plants, six cost/execution plant runs, independent controls and row calculations | R872-2 | a16899b1fb2a0c731ebf18476d1a38627254ea4e |
| Docs | CLEAN | SPLIT_CONTROL_MEMORY.md:3000, harness README declaring-arm section, live PR, corrected #943 comment, published receipts; causal correction and limits checked; residue and suggestion above | R872-2 | a16899b1fb2a0c731ebf18476d1a38627254ea4e |

Paths in the ledger are within tb/verilator/ctrl_service_budget unless another location is named: test_aecp.cpp and aecp_output_mutants.py are under sw/firmware/ctrl/test; ctrl_app_aecp.c under sw/firmware/ctrl/app; aecp_face.c under sw/firmware/ctrl/aecp; SPLIT_CONTROL_MEMORY.md under docs/design.

**Evidence, limits and manager duties**

archive-verification.txt verifies all 112 published author files against the publication manifest at archive f9f1e85d91749fbba4506b54236e63f3eeba7ca6. No reviewer reports were extracted. This establishes byte integrity against the published manifest. The archive commit reports no cryptographic signature; no separate signed packet was located in the designated archive, so signer authentication is not claimed. Published receipts are excerpts, some accompanied by hashes of larger logs; those unavailable larger logs were not independently regraded. published-receipt-excerpts.txt identifies the receipt lines inspected.

Author source-head evidence: all four firmware shards report PASS, with 383 AECP plants and 17 output rows; coverage reports PASS for 40 files. The published harness self-test reports zero failures. The docs receipt records the setup failures/skips above. Firmware-boundary still refuses two named pre-existing unclassified files; it is not claimed green. Twin, memory, platform ledger, release-image identity and unchanged answering-arm results carry from round one only for unchanged inputs. No manager source bank exists at this head, and none is inferred.

Independent executions: both flip checks returned 0 (flip-1x1.log, flip-8x8.log); controls.log records 41 maintained record-class/declaring checks plus independent record/retry span containment at a 2:1 clock ratio and successful/refused/brief fault checks; margin-probe.txt records the projections above. A broader harness self-test was started, then stopped with rc -15 when its default temporary-directory use was noticed. Its partial log is retained as harness-selftest-interrupted.log and is not a pass. The portable runner now directs temporary work into packet scratch; the complete harness verdict cited here is the author's published result. No compiler or simulator campaign was rerun. No hardware, hosted/act acceptance, full parent/processor/synthesis/builder bank, source fix, commit, push, or GitHub write was performed.

source-integrity.txt verifies every tracked parent blob's bytes and mode, the index tree, and the five required initialized submodules' gitlinks, heads, indexes and tracked bytes/modes. Parent HEAD/tree remain exactly as assigned and status is clean. No tracked restoration was necessary. The uninitialized external gitlink was recorded, not used.

The manager still owns the separately ordered margin-recovery step and reviews; final-image costs and held bounds; current-dev candidate construction and full builder/native banks with receipts; hosted executed-versus-skipped context acceptance and local replica acceptance; existing boundary/setup obligations; review completion, authorized merge and containment; issue/project completion; and disposition of the separately scoped GET_TX_STATE report. Candidate evidence must name the actual live-dev base and composed tree; source base 0839453f is not that proof. Physical calibration remains NOT RUN, and field skips are not hardware proof. This source verdict clears none of those duties.

Publish only REPORT.md and files listed in MANIFEST.sha256. Scratch is excluded.

R872-2 FINISHED

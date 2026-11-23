[R894] POSITIVE - exact head 3cda030c174b325e36c26af6420487ff91346d15

External independent review R894-4, issue #584 / PR #975. Tree f6050855ee84658b4d907cf8bac69deee39bb893. This independent verdict and ledger were written before consulting prior review reports. Final public-finding reconciliation follows below.

The delta from 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e replaces six lines in three documentation files. It changes no implementation, generated artifact, test, interface or requirement. The owner approved port 0's TDM32 slot 0, ports 1-7's Unrouted clusters, and no input loopback backing in [#584 comment 7092564847](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7092564847). D8, the changelog and descriptor ownership reflect that decision. Three wording residues remain below. No BLOCKER, MAJOR or MINOR was found.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #584 body and decisions 5857155362, 7077045073, 7092564847; CHANGELOG.md:64-82; docs/ENDSTATION_BUILDER.md:759-777; docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:163-173; configs/endstation_ax7101_8x8.yaml:204,222,263 | R894-4 delta; R894-3 unchanged implementation carried | 3cda030c174b325e36c26af6420487ff91346d15 |
| RTL | CLEAN | delta.diff: only three Markdown files; hdl/ieee1722/aaf/KL_tdm_render_master.sv bus/lane contract; no RTL/configuration/gitlink change from 599c79af | R894-4 delta; R894-3 unchanged implementation carried | 3cda030c174b325e36c26af6420487ff91346d15 |
| Robustness | CLEAN | delta.diff; public-receipts/rtl/ship8-mutants.txt: projection, zero-tail, epoch-mask, REMOVE and stale-event controls unchanged | R894-4 delta; R894-3 unchanged implementation carried | 3cda030c174b325e36c26af6420487ff91346d15 |
| Tests | CLEAN | docs-check.log, toc-check.log, anchors.log, em-dash.log; public-receipts/gates/builder-union.txt and rtl/ship8-mutants.txt; no test-source delta | R894-4 delta; R894-3 unchanged tests carried | 3cda030c174b325e36c26af6420487ff91346d15 |
| Docs | CLEAN | Three changed pages, docs/ENDSTATION_BUILDER.md:886-890, PR body, owner approval, documentation gates | R894-4, with non-blocking wording residue | 3cda030c174b325e36c26af6420487ff91346d15 |

R894-4-R1 | RESIDUE | Docs | docs/ENDSTATION_BUILDER.md:888-890.
Authority/evidence: D10 still says these backing choices await the owner's disposition; comment 7092564847 explicitly approves them.
Impact: contradictory approval-status prose beside corrected D8.
Required outcome / exact fix: replace the final sentence with "On the 8x8, the owner approved ports 1-7's Unrouted clusters and TDM32 Out 0 as the first TDM channel on 2026-11-23 (#584, D8)."
Verification: read D8 and D10 together; no pending/await wording for this decision.

R894-4-R2 | RESIDUE | Docs | PR #975, Known limitations / out of scope, first bullet.
Authority/evidence: it says the loopback posture and TDM32 interpretation remain pending, although Description records the approval and claims D8 and D10 agree.
Impact: contradictory PR status prose.
Required outcome / exact fix: replace "remain pending the owner's disposition (Description)" with "were approved by the owner on 2026-11-23 (Description)". Resolve R1 so D10 agrees.
Verification: search the live PR body for pending/await in this decision's context.

R894-4-R3 | RESIDUE | Docs | PR #975, How to get into the same state.
Authority/evidence: both checkout and HEAD assertion still name 599c79af9cfe242bc3d60dd1c80f3e8d57cca12e; Status names 3cda030c.
Impact: reproduction instructions retrieve preceding documentation wording; all executable inputs are identical.
Required outcome / exact fix: replace both old hashes in that section with 3cda030c174b325e36c26af6420487ff91346d15.
Verification: both commands identify the reviewed head.

These residues change only prose or PR text, with no change to measurements, figures, verdicts, tests, code, generated artifacts, conformance/clause claims or privacy. Under the owner's residue rule they do not unclean a lens. No source comment was added in this delta.

All four focused documentation checks pass. docs_check: zero findings over 223 Markdown and 1919 text files; generated contents: 160 pages; anchors: 756 reproduced cross-page links; em-dash gate: six added lines, three pages, 339/339 controls. The initial dependency refusal was resolved with a disposable environment installed from the repository's hash-pinned Markdown lock.

The public evidence audit verifies 270 author files against the published manifest and all 159 round-3 index rows, including complete receipt coverage. Raw tracked bytes, executable modes and index entries match the head: 1944 parent blobs, six gitlinks. The four required initialized submodules match their pins and raw blobs/index (115, 868, 100 and 214 files respectively). No tracked source was changed.

Public findings reconciled after the independent verdict and ledger

The prior reports were read only after the independent pass and the above verdict/ledger were written. Their public bodies are preserved in prior-public-findings.json. The original source-base history/inventory from dd163e41438acb86e0c4d4e76df90f3f91ace1c0 was examined for context; this round judges only the complete 599c79af..3cda030c delta and its dependencies, as instructed.

| Prior finding | Disposition at this head and cause evidence |
|---|---|
| R894-1-F1 / R893-1-F1 (Conformance, Docs) | CLOSED, owner-disposed. Comment 7092564847 expressly approves the actual unchanged topology. D8:759-777, ownership:171-173 and CHANGELOG:79-82 record approval. The remaining D10/PR stale status is R1/R2 wording residue, not an unapproved topology. |
| R894/R893 F2; R894 F2-R2 / R893 F6 (Conformance, Robustness, Tests, Docs) | CLOSED as established by R894-3. No harness, parameter, RTL or dependency change. Public round-3 ship8-mutants records 11/11 including both named B3/Z3 recovery replay failures, projection, zero-tail, epoch-mask, REMOVE and bus controls. This round authenticates those receipts; it does not rerun the campaign. |
| R894/R893 F3 (Docs) | CLOSED, carried. SPLIT_CONTROL_MEMORY.md and its measured per-image accounting are untouched. PR still distinguishes +1336/+1344 ROM and +1744/+1808 SRAM by image. |
| R894 F4 (Docs) | CLOSED, carried. Ownership L1:86 names STREAM_PORT_CLUSTER_MINIMUM and no waiver; builder row 45:1158 names no tracked waiver. Saved-state census authority is untouched. |
| R894 F5 / F5-R2; R893 F7 (Tests, Docs) | CLOSED. Current 159-row index and historical 80-/16-row replacements independently match public bytes. Original historical indexes remain superseded; no claim that those old originals were rewritten. |
| R893 R1-R3 (Docs) | CLOSED, carried: "an 8x8 talker", first-port physical ownership and loopback-on obj_nxn8 description have no delta. |
| R894 R4 / R893 R4 (Docs) | CLOSED, carried. Builder plan generator unchanged; authenticated comparison still records 153/155 identical outputs and only the two 17-byte 8x8 plan-name additions. |
| R894 R5 / R893 RS2 (Docs) | Prior summary clarification retained; the approval sentence is now intentionally updated. CHANGELOG:79-82 names all three approved points; zero slots and unrouted ports remain distinct at :86-87. |
| R894 R6 (Docs) | CLOSED, carried. Final receipt explanations and their corrected indexes are unchanged and authenticated. |
| R893 RS1 (Docs) | CLOSED, carried. TESTING.md's timing paragraph has no delta. |
| R893 RS3; R894 R9-R3 (Docs) | Retain wording residue below; source banner and tap title are unchanged. |
| R893 S3 (Tests) | CLOSED, carried. Zero-tail, epoch-mask and REMOVE plants remain banked and caught in the authenticated campaign receipt. |
| R894 R7-R3, R8-R3; R893 S1/S2 | Retain unchanged, detailed below. |

Carried open items, with their original IDs

R7-R3 | RESIDUE | Docs | CHANGELOG.md:88-89.
Authority/evidence: the detailed recovery contract permits pre-loss audio until epoch closure; the short summary omits that qualifier. This is unchanged from R894-3.
Impact: abbreviated prose obscures the existing interval, without changing the measured behavior or executable expectation.
Exact fix: "One record spans loss/reset through recovery after rebind." and "Pre-loss audio ends at epoch closure; rebind requires freshness."
Verification: compare those bullets with the unchanged recovery banner and the published clean record. Preserve test expectations and results.

R8-R3 | RESIDUE | Docs | tb/verilator/milan_dp_render/sim_ship8_render.cpp:45.
Authority/evidence: the owner's source-comment rule requires behavior and reason rather than a bench phase label; the existing sentence uses P2.
Impact: comment-maintenance residue, inherited unchanged.
Exact fix: replace "graded in P2 against the ids the bench's own answers carried" with "checked during listener binding against the IDs carried by the generated responses."
Verification: preserve executable bytes and #584 authority; remove only the phase label from the comment.

R9-R3 | RESIDUE | Docs | tb/verilator/milan_dp_render/sim_ship8_render.cpp:42,411.
Authority/evidence: "timestamp and counter sources only" conflicts with the already enumerated masks and stream IDs.
Impact: contradictory labels, unchanged; accessors and pin-only sample decoder are correctly described by the full enumeration.
Exact fix: banner "Internal taps supply timestamps, counters, masks and stream IDs"; title "Taps: timestamps, counters and stream state".
Verification: labels agree with the unchanged accessors; no oracle, clause claim or test changes.

S1 (R893-2) | SUGGESTION | Tests, Docs | scripts/suite_shards.py:122; tb/verilator/milan_dp_render/Makefile:47-62; docs/testing/TESTING.md:433-437.
Authority/evidence: aggregate timing predates ship8; its piece estimate is explicitly scaled local timing.
Impact: optional scheduling refinement when actual hosted timing is available.
Desired outcome: update aggregate and piece estimates using the manager's measured hosted window.
Verification: distinguish executed hosted pieces from serial default-suite timing; no new timing measurement is claimed here.

S2 (R893-2) | SUGGESTION | Tests, Robustness | tb/verilator/milan_dp_render/ship8_params.py.
Authority/evidence: flags outside recognized/refused prefixes remain intentionally ignored.
Impact: a future relevant flag outside those prefixes might escape the guard; no current delta introduces one.
Desired outcome: optionally inventory intentional ignored flags.
Verification: a future unsupported render-relevant flag is refused by name, with deliberate control/clock differences documented.

Reproduction, evidence and limits

- Run `python3 verify-evidence.py <checkout>` from this packet. It checks immutable public blobs, all current receipt-index rows, both historical corrections and exact parent/required-submodule bytes/modes/index. The publication commit must already be fetched. No source edits or restoration are needed.
- For the documentation gates, create a disposable environment under scratch/, install `tools/markdown/requirements.txt` with `--require-hashes`, then run `<environment-python> run-doc-gates.py <checkout>`. The four checks execute concurrently and are joined by the foreground process. Per-command logs and exit files are included. No job remains running.
- The changed owner-decision link resolves to the exact public approval; the retained November decision link resolves to comment 7077045073. The processor #122 disposition also resolves and retains the cluster minimum. The local D8 link and 755 other cross-page fragments pass the anchor gate. The PR body's approval links match those checked URLs; stale status is explicitly reported rather than hidden by a green link check.
- Publication faacf4dfb277313f6cbe7804a995dbbd5227a12c is UNSIGNED: the public commit API reports verified=false, reason=unsigned, and there is no detached signature in this packet. Its manifest is a hash inventory. Immutable identity and published hashes were verified; signer authentication is not claimed. This existing limitation is not a newly introduced defect.
- Source execution evidence is the author's published round-3 evidence, carried because executable inputs are identical. The builder union reports 113 gates exactly once, with two existing NOT RUN arms. Physical calibration was NOT RUN. The full published docs workflow records 99/103 commands, with four hosted-environment commands failing locally. The four focused docs checks here are fresh at 3cda030c; they are not a claim that all 103 workflow commands ran here.
- No manager source bank ran at this exact head; none is inferred. No full parent/processor/builder/synthesis bank, simulation campaign, routing, container workflow or hardware operation was performed in this round. Physical calibration NOT RUN and field skips provide no hardware proof. No exact-head hosted jobs were inspected or certified here.
- The required four submodule gitlinks and checkout bytes were verified. The other two gitlink index entries are exact; the legacy external module is uninitialized and not needed for these checks. No source mutation, commit, push, GitHub write, author contact or sub-agent was used.
- This is source-review approval, not merge authorization or whole-product conformance. R894-3's unchanged-source verdicts stand. The manager must carry all six residues and two suggestions, finish the required independent review bar, obtain exact-head hosted/local-replica acceptance and the owed hosted timing, and publish the final current-dev candidate's builder/native receipts at the merge turn.
- Source base dd163e41438acb86e0c4d4e76df90f3f91ace1c0, reviewed source head 3cda030c174b325e36c26af6420487ff91346d15 and supplied live dev e275d7950ef3385753e6a15d2e191ba855b171ed are distinct. No future merge candidate has been validated by this report. Merge requires explicit maintainer authorization, followed by containment, Issue closure and Project completion.

Only REPORT.md and files listed in MANIFEST.sha256 are publishable. Scratch contents are excluded.

R894-4 FINISHED

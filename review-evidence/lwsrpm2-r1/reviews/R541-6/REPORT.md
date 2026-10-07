[R541] POSITIVE - exact head 14c8b364863be49bc222f4913830b79d23dcf173

External independent delta review of [issue #10](https://github.com/kebag-logic/lwSRP/issues/10) and [PR #12](https://github.com/kebag-logic/lwSRP/pull/12), round R541-6.
Tree: `0d2f7e8cfb5f1e2886c7cfabde530b7cf1ed3921`.
The [round-seven assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6036261356) covers one commit after `a29f8d13ff4869e54997d9adf05d83a4ace4b8bd`.

Both assigned findings are resolved. No BLOCKER, MAJOR, MINOR, or RESIDUE remains open in this review.
Two previously acknowledged test suggestions remain below.

I judge the retained-Flush mechanism complete across the supported paths that can touch pending storage.
The owned snapshot survives local declarations, immediate and deferred cross-port replay, receive retry, repeated Flush, timer processing, and opposite-Talker replacement.
Completion clears pending state, and reclamation cannot free an outstanding LV withdrawal.
No further mechanism defect was found, so the manager’s conditional switch to atomic refusal is not triggered.
This judgment assumes the documented serialized, non-reentrant API and supported value sizes; it is not exhaustive protocol proof.

**Reconstruction and independence**

I read the supplied instruction reference, contributor rules, README, and reader guides first.
Next came frozen acceptance, public manager scope decisions, linked issues, and interface authorities.
I then inspected the [source-base diff](receipts/source-base.diff), history, and [round-seven delta](receipts/round7.diff).
The source base is `1401654530ce7d9275de9b901e67df47e5bbc536`.
The [independent source-pass record](receipts/independent-pass.md) precedes extraction of prior public findings.
Public finding extracts were used for reconciliation after that pass.
No private author material or current-round reviewer report was consulted.
The [independent verdict and ledger](receipts/independent-verdict.md) records this review’s judgment separately.

The [initial evidence pin](https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1) contains only the first-round author packet.
The public [round-seven packet](https://github.com/kebag-logic/milan-fpga/tree/271ee8152e1b1ed7f7ab2ca60d1076d3ab037684/review-evidence/lwsrpm2-r1/author-r7) was retrieved separately at that immutable revision.
Its receipts identify this exact source head.
[Evidence assessment](receipts/evidence-assessment.json) records provenance and separates supplied validation from reviewer executions.

**Assigned findings**

**R541-5-F1 — MAJOR — Conformance, Robustness, Tests, Docs — RESOLVED.**
Artifacts: [snapshot storage and selection](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/src/core/mrp_mad.c#L642), [capture guard](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/src/core/mrp_mad.c#L651), and [cross-port regressions](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/unit/review_test.c#L990).
Authority: round-seven item 1 and the [public ownership contract](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/src/include/shish_lan/mrp.h#L277).
The former defect withdrew newer Applicant parameters instead of the originally registered value.
The required outcome was an immutable owed value, without suppressing legitimate Applicant updates or ordinary LV recovery.
The first failed Flush now captures aligned storage; later failures preserve it.
Reservation copies, indication, and policy use that saved value.
Verification: the unchanged prior probe passes all 48 cases and 2,188 checks per profile, with zero value mismatches.
See [default](receipts/OFF-cross-port.log) and [enabled](receipts/ON-cross-port.log) traces.
All four published snapshot reversals compile and fail their required named tests in both profiles.
Independent storage checks also inspect the full saved and queued value, including Talker Failed fields.

**R540-5-01 — MINOR — Tests — RESOLVED.**
Artifact: [timer-completion regression](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/unit/review_test.c#L1008).
Authority: issue acceptance 2 and the [public finding](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036255540).
The former coverage gap allowed pending state to remain after timer completion, causing extra Leave/Join pairs on subsequent refreshes.
The required outcome was a timer-only completion test followed by repeated unchanged registrations and a discriminating reversal.
The new test covers all three stream types, IN/LV, every reservation fault, three refreshes, and later ticking.
The exact `flush-timer-completion` mutation compiles and fails `timer_completed_flush_keeps_unchanged_registrations_quiet` in the [default results](receipts/OFF-reversal-results.json).
The [enabled results](receipts/ON-reversal-results.json) independently confirm the same named failure.

**Pending-storage path audit**

| Path and exact-head artifact | Result and evidence |
| --- | --- |
| First and repeated failed Flush, `src/core/mrp_mad.c:651` | One capture until successful Leave; repeated failures retain the full value. Repository local-declaration matrix and independent lifecycle cases pass. |
| Local Join/New, `src/core/mrp_mad.c:467`, `:955` | Refreshes Applicant storage while preserving the owed snapshot. Independent mutation freezing Applicant updates is detected. |
| Immediate/deferred propagation, `src/core/mrp_mad.c:590` | Replay reaches ordinary local declaration storage. Retained source output delays replay correctly; accepting output preserves the snapshot. |
| Source receive, `src/core/mrp_mad.c:1002` | Completes saved Leave before refreshing the attribute. The public probe covers all six event kinds, changed/unchanged values, both initial states, and repeated reservation failures. |
| Opposite-Talker replacement, `src/core/mrp_mad.c:1029` | Pending old withdrawal uses its saved value before replacement. Both directions and faults 0–9 pass the independent lifecycle probe. |
| Timer, repeated Flush, received/transmitted LeaveAll, Re-declare | LV retains the pending obligation; first available retry completes it. Subsequent unchanged registrations remain quiet. |
| Reservation, indication, policy, `src/core/mrp_mad.c:642` | All select the saved value. The independent queue-copy mutation fails an owned-byte assertion after successful compilation. |
| Completion, `src/core/mrp_mad.c:670` | Timer, receive, and explicit Flush clear the flag; later independent Flush captures a fresh value. |
| Reclaim/destroy, `src/core/mrp_mad.c:1103`, `:919` | Pending LV is not reclaimed. Destruction releases pending attributes and queues; later global ticks remain safe. |

The [lifecycle probe](scripts/storage_probe.c) drives public operations and uses internal readback only to inspect ownership bytes.
It covers 281 cases and 10,081 checks per profile, with [default](receipts/OFF-storage.log), [enabled](receipts/ON-storage.log), and instrumented results.
The separate prior [public-interface probe](scripts/prior_cross_port_probe.c) retains production propagation policy.

**Reviewer executions**

| Check | Exact-head result |
| --- | --- |
| Host configure/build, configured tests | Both profiles return 0; 1/1 configured target passes. |
| [Default unit runner](receipts/OFF-units.log) | Eight suites, 86 tests, 19,885 assertions; rc 0. |
| [Enabled unit runner](receipts/ON-units.log) | Eight suites, 86 tests, 19,873 assertions; rc 0. |
| Scenarios | Each profile: one feature, three scenarios, ten steps; rc 0. Dry run only checks matching. |
| Prior cross-port probe | Each profile: 48 cases, 2,188 checks, zero value mismatches; rc 0. |
| [Broader prior probe](receipts/OFF-broad-probe.log) | Each profile: 489 cases, 21,780 checks, zero value mismatches; rc 0. |
| Independent lifecycle probe | Each profile: 281 cases, 10,081 checks; normal and memory/undefined-behavior instrumented runs return 0. |
| Published reversal sample | 22 of 93 cases per profile; all compile and fail required named checks. Restored builds and suites return 0. |
| Independent mutations | Four per profile: partial snapshot, wrong queue-copy value, frozen Applicant refresh, and skipped pending replacement. All compile and fail the independent oracle. |
| Embedded source-list boundary | Both profile links and dispatch executions pass. Only runner build parallelism changes in the disposable copy. |
| Freestanding boundary | Both profile dependency checks return 0. |
| Documentation | 975 fragments; zero long sentences or detected unlinked references; 79 reference self-tests pass. |
| Links | 354 local links and 20 external URLs pass; repository requests are authenticated. |
| Graphs and anchors | All 27 graphs render. Changed eight-node retry graph visually checked; all 43 source anchors checked. |
| Integrity | All 60 tracked blobs, file modes, and index entries match the assigned head. No library submodule gitlinks exist. |

[Execution records](receipts/executions.jsonl) retain commands, return codes, and log names.
[Published sample results](receipts/OFF-reversal-results.json) and [independent mutation results](receipts/OFF-own-mutations.json) distinguish intentional failures from baseline passes; matching enabled receipts are included.
The public author packet independently records all 93 reversals per profile, including required failure names and restored passing builds.
Those complete campaigns were inspected, not rerun here.

Independent campaigns ran concurrently within their foreground drivers, with explicit job limits and separate logs and return-code files.
Builds used 16-way parallelism; disposable sources and dependencies stayed under packet scratch.
The [portable reproduction entry](scripts/reproduce.sh) requires an exact-head checkout and a fresh packet scratch directory.
No source fixes, commits, pushes, remote writes, or hardware actions were made.

**Earlier public findings at this head**

These are explicit current-head dispositions, supported by source inspection, passing suites, the sampled reversals, and the published full campaign.
They do not claim that every historical probe was independently rerun.

| Prior finding | Disposition | Current evidence |
| --- | --- | --- |
| R541-1-F1 | RESOLVED | Complete decode validation and checked vector arithmetic; range tests pass; sampled decode-error reversal fails. |
| R541-1-F2 / R540-1-01 | RESOLVED | Later-version unknown messages/events are skipped at the correct boundaries; current-version strictness tests pass. |
| R541-1-F3 | RESOLVED | Domain explanation and manager matrix include clause 35.2.2.9. |
| R541-1-F4 / R540-1-07 | RESOLVED | Previously changed guards and new delta guards satisfy the braces rule. |
| R541-1-F5 / R540-1-02 | RESOLVED | Both source lists include switch dispatch; both embedded link probes pass; bare-metal recipe names it. |
| R541-1-F6 / R540-1-03 | RESOLVED | Owned FIFO survives retained output and replays after acceptance; retention reversal fails. |
| R541-1-F7 / R540-1-04 | RESOLVED | Local/omitted/reserved LeaveAll, Listener subtype, timer bounds, and LO reclamation are covered by current tests and published reversals. |
| R541-1-S1 / R540-1-06 / parent R532-1 S2 | RESOLVED | Unchanged LV recovery cancels aging without duplicate Join; sampled recovery-indication reversal fails. |
| R541-1-S2 / R540-1-05 | RESOLVED | Profile Re-declare/LeaveAll scope and participant restart regressions pass; full published campaign detects their reversals. |
| Parent R532-1 S1 | RESOLVED | Receive LeaveAll is type- and port-scoped; isolation tests pass. |
| R540-2-01 | RESOLVED | Changed IN/LV values indicate and propagate after either LeaveAll route; sampled IN-only reversal fails. |
| R540-2-02 | RESOLVED | Unknown stream messages use AttributeListLength; sampled list-boundary reversal fails. |
| R541-2-F1 / R540-2-03 | RESOLVED | Reservation-before-indication, rollback, error reporting, replay, and teardown fault tests pass; full published campaign detects named reversals. |
| R541-2-F2 | RESOLVED | Host indication precedes policy; sampled callback-order reversal fails. |
| R541-2-F3 | RESOLVED | Integrator table and runner agree on eight suites. |
| R541-2-R1 / R540-2-R1 / R538-2-R2 | RESOLVED | Exact licence-and-notice sentence is present in `doc/tools/README.md:31`. |
| R541-2-R2 / R540-2-R2 / R538-2-R3 | RESOLVED | Both requested historical licence sentences are present in `doc/manager.md:91`. |
| R541-3-F1 / R540-3-01 | RESOLVED | Failed topology withdrawal is retained and retried, now with a protected snapshot. |
| R540-3-02 | RESOLVED | Replacement stops before new Join when old Leave reservation fails; both-direction fault cases pass. |
| R540-3-03 | RESOLVED | Receive stopping, selected policy masks, and allocation-free no-policy behavior have named tests and reversals. |
| R541-4-F1 / R540-4-S2 | RESOLVED | Incoming registration cannot cancel pending Flush; saved Leave precedes new registration. |
| R541-4-F2 | RESOLVED | First-tick recovery and reached failures are asserted; sampled two-tick reversal fails. |
| R540-4-01 | RESOLVED | Failed IN→LV transition is observed; continuity probe and sampled observer reversal pass/fail as required. |
| R540-4-02 | RESOLVED | Replacement begins in received-LeaveAll LV; both directions/faults covered; both sampled reversals fail. |
| R540-4-03 | RESOLVED | Fault position 1 is included; dropping the source-error stop guard fails its named regression. |
| R540-4-S1 | RESOLVED by documentation | Retry contract states later LeaveAll can apply during a failed payload; identical retry converges. |
| R541-5-F1 / R540-5-01 | RESOLVED | Exact-head evidence detailed above. |
| R540-5-S1 / R540-4-S3 | RETAINED as SUGGESTION | Repository-only gaps described below. |

**Retained suggestions**

**R540-5-S1 — SUGGESTION — Tests.**
Artifact: `tests/unit/review_test.c:758`; replacement condition at `src/core/mrp_mad.c:1030`.
Authority: [prior public suggestion](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036255540), acknowledged in the PR body.
The repository suite still passes a mutation that skips an opposite Talker whose Flush is pending.
The independent lifecycle probe detects it; the unmodified head passes both replacement directions and faults 0–9.
Impact: this specific interaction could regress without the repository suite detecting it.
Suggested outcome: add a repository pending-Flush replacement case and named reversal.
Verification: require the compiled mutation to fail that named case in both profiles.
See [default unit survival](receipts/OFF-suggestion-pending-replacement.log), [enabled survival](receipts/ON-suggestion-pending-replacement.log), and [independent detection](receipts/OFF-own-replacement-ignores-pending.log).
This is retained optional coverage advice, not a newly found mechanism defect.

**R540-4-S3 — SUGGESTION — Tests.**
Artifact: inherited Flush-triggered LeaveAll request at `src/core/mrp_mad.c:1140`.
Authority: the [prior public suggestion](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452), retained and acknowledged in later rounds.
Removing that request still passes the repository unit suite in both profiles.
Impact: the inherited request lacks a discriminating repository regression.
Suggested outcome: pin the resulting LeaveAll transmission with a named reversal.
Verification: the compiled removal must fail that regression, while the unmodified head passes.
See [default](receipts/OFF-suggestion-flush-leaveall.log) and [enabled](receipts/ON-suggestion-flush-leaveall.log) receipts.
No current behavior defect is alleged.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
| --- | --- | --- | --- | --- |
| Conformance | CLEAN | Frozen acceptance; manager scope; public interfaces; Registrar/Applicant tables; snapshot and ordering probes; prior-finding reconciliation | R541-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| RTL | CLEAN | Complete changed-file inventory; no HDL/constraints; embedded source lists and dispatch; freestanding checks; public parent pool/mailbox boundary | R541-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Robustness | CLEAN | Snapshot writes/readers; allocation failures; immediate/deferred replay; receive/timer/replacement interactions; reclamation/destruction; instrumented lifecycle probes | R541-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Tests | CLEAN | Both 86-test profiles; prior 48/489-case probes; independent 281-case probe; 22 sampled and four independent mutations per profile; restored suites | R541-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |
| Docs | CLEAN | README and four guides; interface/PR claims; measured counts; sentence/reference/link checks; graph inspection; source anchors; explicit integration limits | R541-6 | 14c8b364863be49bc222f4913830b79d23dcf173 |

**Limits and pending manager duties**

This is a source delta review, not a complete standards certification or exhaustive state-space exploration.
Normative allocation-exhaustion behavior is not inferred from the standard: the snapshot obligation comes from accepted scope and the published interface.
The [RTL boundary assessment](receipts/boundary-assessment.md) distinguishes host linking and native interface inspection from target evidence.
The supplied manager source static/build and native-bank passes were not independently rerun.
Source validation against `1401654530ce7d9275de9b901e67df47e5bbc536` is distinct from the final candidate against live dev `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c`.
The manager must build and accept that current-dev candidate at merge time, confirm required parent gitlinks, and obtain both independent positive reviews.

[Exact-head hosted queries](receipts/hosted-runs.json) return zero workflow runs, zero check runs, and zero status contexts.
There are no executed hosted jobs in that response to count as passes, and no skipped context is treated as coverage.
Hosted and local workflow acceptance remain manager-owned.
Physical calibration: **NOT RUN**. Field skips do not prove hardware behavior.
Target execution, pool sizing on the final target, and network interoperability remain unverified here.
The separately tracked scenario-state assertion limitation remains disclosed in [issue #4](https://github.com/kebag-logic/lwSRP/issues/4).

The [integrity receipt](receipts/integrity.json) verifies exact tracked bytes, modes, index, and the empty library gitlink set after probes.
[MANIFEST.sha256](MANIFEST.sha256) identifies the publishable packet; scratch is excluded.
The manager owns publication and any merge. No remote write was performed by this review.

R541-6 FINISHED

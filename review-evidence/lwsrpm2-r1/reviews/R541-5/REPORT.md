[R541] NEGATIVE - exact head a29f8d13ff4869e54997d9adf05d83a4ace4b8bd
<!-- SPDX-License-Identifier: Apache-2.0 -->

External independent review of [issue #10][issue] and [PR #12][pr], round R541-5.
The reviewed tree is `dfff72e82034986739d9f8641a820a0d76ea6dd1`.
One MAJOR saved-value defect remains open.
The five assigned corrections pass their direct reproducers and discriminating reversals.
Cross-port propagation still corrupts the value owed by a pending Flush.

The [public start][start] fixes the reviewed head.
The [full diff](receipts/full.diff), [round-six delta](receipts/round6.diff), and [history](receipts/history.txt) were inspected.
The delta is one commit on `0a45695db537badb8d7e9cbf578925fe5b89d647`.

Reconstruction began with the supplied instructions, [contribution rules][contributing], [README][readme], and four reader guides.
Frozen acceptance, public manager decisions, and interface authorities preceded the independent source pass.
The [independent verdict and ledger](receipts/independent-verdict.md) were written before reading prior public finding bodies.
The initial comment inventory exposed prior report headings and short lead-ins.
Detailed findings were read only after the independent verdict.
Supplemental parent-boundary checks followed the independent pass.
No private author material, unrelated checkout, private management material, or current parallel review was consulted.
No source fix, commit, remote write, delegated work, or hardware action occurred.

**R541-5-F1 — MAJOR — Conformance, Robustness, Tests, Docs — OPEN**

**A propagated update overwrites the value owed by a failed Flush.**

Artifacts: [pending flag, source line 647][pending], [receive protection, line 995][receive], and [unconditional value refresh, line 478][refresh].
The bypass runs through [propagation replay, line 597][replay] and [local declaration, line 948][local].
Withdrawal later uses that mutable value at [line 674][leave].
The [public interface][interface] and [integration contract][contract] promise withdrawal with the saved value.
The [developer guide][developer] makes the same claim.

Authority: [round-six item 1][assignment] requires preserved pending withdrawal across receive dispatch, with aligned interfaces, documentation, tests, and reversal evidence.
The [frozen acceptance][issue] requires regressions for new behavior.
Conformance attribution concerns these accepted requirements and public contracts, without assuming a standards-defined allocation-exhaustion policy.

The new receive guard protects only the attribute on the incoming port.
The refresh helper is inherited; the new pending mechanism does not protect its saved-value obligation from that path.
A valid receive on another port publishes a propagated Join to the pending source port.
That Join refreshes the shared attribute storage without completing the pending withdrawal or preserving its old value.
The flag survives, but the later Leave reports parameters that were never registered through the source port's host indication.

The [independent probe](scripts/probe.c) retains the production propagation callbacks unchanged.
It uses three ports, copied indication values, serialized public calls, and the repository's fault allocation port.
It has no retained source output or callback reentry.
A representative Talker sequence is:

| Operation | Observed result |
| --- | --- |
| Receive on port 0, frame size 100 | Host receives Join with 100. |
| Flush port 0, fail a reservation | No Leave yet; withdrawal remains pending. |
| Receive same identity on port 1, frame size 200 | Propagation changes port 0's stored value to 200. |
| Tick, or receive port 0 with frame size 300 | Leave carries 200, instead of the saved 100. |
| Receive completion variant | Join with 300 follows the incorrect Leave. |

The [default trace](receipts/OFF-cross-port.log) and [enabled trace](receipts/ON-cross-port.log) each execute 48 cases and 2188 checks.
Twelve no-fault controls preserve the original value.
All 36 faulted cases report the wrong withdrawal value.
Coverage includes both Talker types, Listener, initial IN/LV, all three reservation faults, and timer/receive completion.
Listener routing uses registered Talkers; its pending subtype changes from 2 to 1 before withdrawal.
Both [instrumented default](receipts/OFF-san-cross-port.log) and [instrumented enabled](receipts/ON-san-cross-port.log) runs reproduce the same mismatches without memory diagnostics.
Every case destroys its application and checks zero live allocations.

Impact: the host receives withdrawal data inconsistent with its original registration.
Value-dependent host accounting or propagation policy cannot reliably reconcile that registration.
This affects the library's supported multiport use; the probe does not establish a single-port product failure.
The defect changes observable callback values and violates the documented retention contract; it is not wording-only residue.

Required outcome: preserve the original withdrawal value until indication and propagation complete.
Cover every path that can refresh pending storage, including local declarations and propagation from other ingress ports.
Preserve legitimate subsequent Applicant updates and ordinary unchanged LV recovery.
Add named regressions with a reversal that restores this bypass, and align the interface and guides with the resulting behavior.

Verification: all 48 cross-port cases must preserve original Leave values in both profiles.
Keep successful recovery on the first tick, observer continuity, replacement ordering, source-error stopping, and the existing passing suites.
A compiled bypass mutation must fail the new named regression.

**Round-six disposition**

| Assigned item | Disposition at this head | Evidence |
| --- | --- | --- |
| R541-4-F1 | Direct cancellation RESOLVED; saved-value guarantee RETAINED through F1 above | Pending flag and receive-before-refresh tests pass. Cross-port update bypass remains. |
| R541-4-F2 | RESOLVED | [Two-tick default mutation](receipts/OFF-flush-deadline.log) and [enabled mutation](receipts/ON-flush-deadline.log) fail the named next-tick regression. |
| R540-4-01 | RESOLVED | [Observer mutation](receipts/OFF-flush-observer.log) fails its named continuity test. Independent continuity checks pass both profiles and fail the reversal. |
| R540-4-02 | RESOLVED | LV replacement starts after received LeaveAll, both directions, all nine fault positions. [IN-only](receipts/ON-replacement-lv.log) and [omitted-timer](receipts/ON-replacement-leave-timer.log) plants fail. |
| R540-4-03 | RESOLVED | Fault position 1 is checked. [Source-error guard removal](receipts/ON-receive-instance-stop.log) fails the named test and independent probe. |

The [independent passing probe](receipts/OFF-final-probe.log) covers 489 cases and 21780 checks per profile.
It checks all six incoming events, both starting states, changed/unchanged values, all Flush reservation faults, and receive-with-LeaveAll interleavings.
It also checks ordinary LV recovery, repeated exhaustion, observer continuity, replacement faults, source-error stopping, and teardown.
The [enabled result](receipts/ON-final-probe.log) has identical counts.
A [selective JoinMt bypass](receipts/ON-own-joinmt.log) fails the repository regression and [independent oracle](receipts/ON-own-joinmt-probe.log).
Independent replacement and source-error probes also reject their respective plants in both profiles.

**Earlier public findings**

The [previous internal findings][previous-internal] and [previous external findings][previous-external] were read after the independent verdict.
Earlier finding headings and disposition chains were checked for completeness.
Unchanged dispositions below use current source inspection, passing current suites, and the public round-six reversal records.
Only the explicitly stated reversal sample was rerun independently.

| Prior finding | Disposition at this head | Current evidence |
| --- | --- | --- |
| R541-3-F1 / R540-3-01 | Original lost-Flush reproducer RESOLVED; broader saved-value retention remains F1 | First-tick and repeated-fault probes pass; cross-port values fail. |
| R540-3-02 | RESOLVED | Both replacement directions and IN/LV fault sweeps pass; ordering reversals fail. |
| R540-3-03 | RESOLVED | Stop, policy-mask, and no-policy tests pass; published corresponding reversals fail. Coverage text remains accurate for those tests. |
| R540-2-01 | RESOLVED | Changed values after received/transmitted LeaveAll pass; unchanged recovery remains quiet. Published IN-only reversal is detected. |
| R540-2-02 | RESOLVED | Opaque stream extensions use advertised list boundaries; generic applications retain vector skipping. Current parser tests pass. |
| R541-2-F1 | Reported receive-allocation loss RESOLVED; withdrawal-value issue remains F1 | Reservation rollback tests pass; shared pending storage remains vulnerable. |
| R541-2-F2 | RESOLVED | Indications precede policy selection; [callback-order reversal](receipts/OFF-callback-order.log) fails its named test. |
| R541-2-F3 | RESOLVED | Eight suites execute in both profiles, matching the integration guide. |
| R540-2-03 | RESOLVED | Fault-port rollback, replay, error reporting, allocation, and teardown tests pass; published named reversals are detected. |
| R541-1-F1 | RESOLVED | Atomic application validation and overflow tests pass; validation paths remain unchanged in this delta. |
| R541-1-F2 / R540-1-01 | RESOLVED | Higher-version skipping and current-version rejection remain covered across all applications. |
| R541-1-F3 | RESOLVED | The [Domain explanation][domain] and [manager matrix][matrix] cite the Domain clause. |
| R541-1-F4 / R540-1-07 | RESOLVED | Changed guards inspected in the full diff and round-six delta are braced. |
| R541-1-F5 / R540-1-02 | RESOLVED | Both source lists include switch dispatch; [embedded link and execution](receipts/embedded.log) pass. The bare-metal guide includes it. |
| R541-1-F6 / R540-1-03 | Original retained-output loss RESOLVED | FIFO ownership and replay remain tested; [retention reversal](receipts/ON-propagation-retention.log) is detected. |
| R541-1-F7 / R540-1-04 | RESOLVED | Local/omitted/reserved LeaveAll, Listener subtype, timer bound, and reclamation tests pass. Published named reversals are detected. |
| R541-1-S1 / R540-1-06 / parent R532-1 S2 | RESOLVED | Ordinary unchanged LV recovery remains quiet and cancels aging. [Recovery-indication reversal](receipts/OFF-registrar-recovery-indication.log) fails. |
| R541-1-S2 / R540-1-05 | RESOLVED | Profile scope, transmitted LeaveAll, and participant timer restart tests pass. Their published reversals are detected. |
| Parent R532-1 S1 | RESOLVED | Type/port LeaveAll isolation tests pass; the receive handler remains type-scoped. |
| R540-2-R1 / R541-2-R1 / R538-2-R2 | RESOLVED | The exact licence-and-notice sentence remains in the [documentation-check guide][doc-tools]. |
| R540-2-R2 / R541-2-R2 / R538-2-R3 | RESOLVED | Both exact historical licence sentences remain in the [manager guide][licence]. |
| R540-4-S1 | RESOLVED by documentation | The [retry contract][contract] explicitly allows later LeaveAll processing during a failed payload. |
| R540-4-S2 | Direct cancellation RESOLVED | Pending withdrawal precedes direct incoming registration; the separate value defect is F1. |
| R540-4-S3 | RETAINED as SUGGESTION | The pre-existing Flush-triggered LeaveAll request still lacks a discriminating regression. |

No RESIDUE remains open.
Previously classified equivalent mutations remain equivalent; they are not counted as newly detected defects or independently rerun here.

Retained **R540-4-S3 — SUGGESTION — Tests** concerns [topology dispatch, source line 1132][topology].
Authority and evidence are the [previous public finding][previous-internal] and unchanged dispatch code.
Impact: an inherited LeaveAll request can regress without a named failing test.
Suggested outcome: add a focused regression when this inherited topology behavior is next changed.
Verification: removing that request should fail the named test after successful compilation.
This suggestion does not change the verdict or leave a lens unclean.

**Executed evidence and documentation**

| Check | Result |
| --- | --- |
| Host unit suites | 81 tests, eight suites per profile; [default](receipts/OFF-units.log): 16314 assertions; [enabled](receipts/ON-units.log): 16302. Both pass. |
| Configured targets | [Default](receipts/OFF-ctest.log) and [enabled](receipts/ON-ctest.log): 1/1 passes. |
| Scenarios | [Default](receipts/OFF-scenarios.log) and [enabled](receipts/ON-scenarios.log): one feature, three scenarios, ten steps pass. |
| Published reversal sample | 16 of 88 cases per profile; all compile and fail required named checks. |
| Reviewer mutation | Selective JoinMt bypass fails both repository and independent checks in both profiles. |
| Restored copies | Both [default](receipts/OFF-edges-restored-ctest.log) and [enabled](receipts/ON-edges-restored-ctest.log) checks pass after plants. |
| Instrumented execution | Both [default units](receipts/OFF-san-units.log) and [enabled units](receipts/ON-san-units.log) pass. Independent passing probes retain their normal counts. |
| Embedded boundary | Both profile source-list links and dispatch executions [pass](receipts/embedded.log). |
| Freestanding boundary | [Default](receipts/freestanding-OFF.log) and [enabled](receipts/freestanding-ON.log) checks pass. |
| Documentation mechanics | [960 fragments](receipts/sentences.log), zero long sentences; [zero unlinked references](receipts/references.log); [79 self-tests](receipts/references-self.log). |
| Links | [354 local links and 20 external URLs](receipts/links.log) pass; repository checks use authenticated access. |
| Graphs and anchors | [All 27 graphs render](receipts/graphs.log); [43 anchors](receipts/source-anchors.txt) identify intended source. The changed graph received [visual inspection](receipts/graph-review.md). |
| Integrity | [All 60 tracked blobs](receipts/integrity.json) match exact bytes and modes; index/tree match; worktree clean; zero required gitlinks. |

The [execution ledger](receipts/execution-ledger.json) records result codes and receipt hashes.
Every named execution has separate output and return-code receipts.
The [portable driver](scripts/reproduce.sh) builds dependencies and disposable copies under scratch.
The [sample campaign](scripts/campaign.py) and [additional campaign](scripts/final_campaign.py) accept bounded job counts.
Independent profiles and checks ran concurrently under foreground orchestration, within sixteen parallel jobs.
No heavy parent or implementation build ran.

The initial probe's observer indexed one identity per type.
Its later two-identity stop case required disabling that separate continuity oracle; the corrected stop test checks identity presence and callback order directly.
This was a reviewer-harness correction, with no repository source change.

**Public evidence and limits**

The [supplied snapshot][initial-evidence] contains the initial author packet.
The public branch supplied [round-six evidence][author-evidence] at immutable commit `efd32b2a79d19f1e6dc672049b4dbcf3f25ff73b`.
[Retrieval provenance](receipts/author-provenance.json) records the inspected files and hashes.
The public results identify this exact source head and report all 88 reversals detected per profile, with restored passes.
Development failures in the public command history were not treated as final passes.
The independent review reran 16 cases per profile, as authorized; it did not rerun the full 88-case banks.

The [parent requirements][requirements], [reservation requirements][frnfr], and [mailbox contract][mailbox] retain hardware admission, transport, and scheduling responsibilities outside this library.
The [boundary assessment](receipts/boundary-assessment.md) distinguishes these interfaces from host execution.
No HDL or constraints changed, so no simulator was needed or used.
The embedded check establishes host linking and dispatch, not complete target linking or target execution.

The [exact-head queries](receipts/evidence-assessment.md) returned zero [workflow runs](receipts/hosted-runs.json), [check runs](receipts/hosted-checks.json), and [statuses](receipts/hosted-status.json).
No executed hosted job or skipped context was counted as passing evidence.
The manager's full source static, builder, and native success is supplied by the assignment; those banks were not rerun here.
Separate executable manager receipts were not located in the inspected issue and PR comments.

Standards assessment uses frozen public decisions, state tables, and interfaces.
Publisher landing pages do not supply the complete normative texts; this review makes no broader certification claim.
The known [scenario assertion limitation][issue4] remains outside this delta.
Unchanged graphs were rendered again, but only the changed graph received fresh visual inspection.
No hardware or network interoperability was tested.
Physical calibration is NOT RUN; field skips are not hardware proof.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN — F1 | Frozen acceptance, round-six scope, interface contracts, state tables, receive/Flush semantics, parent boundaries, independent probes | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| RTL | CLEAN | Complete changed-file inventory; no HDL/constraints; C source lists; host embedded dispatch; freestanding boundary | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Robustness | UNCLEAN — F1 | Pending state/value ownership, reservation faults, propagation replay, receive/timer interleavings, observer continuity, instrumented execution, teardown | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Tests | UNCLEAN — F1 | Both profiles, 16 sampled reversals, independent JoinMt mutation, replacement/source-error plants, passing probes, cross-port controls and failures | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |
| Docs | UNCLEAN — F1 | Reader guides, contribution rules, public interface, saved-value promises, PR claims, counts, sentence/reference/link checks, graph and anchor review | R541-5 | a29f8d13ff4869e54997d9adf05d83a4ace4b8bd |

The [manifest](MANIFEST.sha256) lists every publishable script and receipt.
Scratch contains only disposable material and is excluded from publication.
Repository bytecode created by an import was removed before the final exact-byte audit.
All source mutations occurred in disposable copies; tracked checkout content was never changed.

The manager must obtain correction and independent re-review of F1 before merge acceptance.
The source base remains `1401654530ce7d9275de9b901e67df47e5bbc536`.
The final candidate against live development `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` requires separate merge-turn validation.
Hosted/local acceptance, dependency pins, issue closure, publication, and post-merge containment remain manager duties.

[issue]: https://github.com/kebag-logic/lwSRP/issues/10
[pr]: https://github.com/kebag-logic/lwSRP/pull/12
[start]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035920200
[assignment]: https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6035585910
[contributing]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/CONTRIBUTING.md
[readme]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/README.md
[pending]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L647
[receive]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L995
[refresh]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L478
[replay]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L597
[local]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L948
[leave]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L674
[topology]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/core/mrp_mad.c#L1132
[interface]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/include/shish_lan/mrp.h#L278
[contract]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/integrator.md#transmit-and-retry
[developer]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/developer.md#deferred-propagation
[domain]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/developer.md#stream-values-and-bounded-interests
[matrix]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/manager.md#implementation-status
[licence]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/manager.md#licence-and-contributions
[doc-tools]: https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/tools/README.md#L31
[previous-internal]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452
[previous-external]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962
[initial-evidence]: https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1
[author-evidence]: https://github.com/kebag-logic/milan-fpga/tree/efd32b2a79d19f1e6dc672049b4dbcf3f25ff73b/review-evidence/lwsrpm2-r1/author-r6
[requirements]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/REQUIREMENTS.md
[frnfr]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/reference/FR_NFR.md
[mailbox]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/design/MAILBOX_SPLIT.md
[issue4]: https://github.com/kebag-logic/lwSRP/issues/4

R541-5 FINISHED

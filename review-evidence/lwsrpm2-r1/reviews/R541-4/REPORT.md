[R541] NEGATIVE - exact head 0a45695db537badb8d7e9cbf578925fe5b89d647

External independent review of [issue #10][issue10] and [PR #12][pr], round R541-4.
The reviewed tree is `6d663f9b08d92b1e1b7202ce159b9e8e391d5f56`.
The [public start][start] pins this head.
One MAJOR withdrawal-loss defect and one MINOR regression-coverage defect remain open.
Replacement ordering and the three previously surviving policy/error plants are resolved.

The [contribution rules][contributing], [README][readme], reader guides, frozen acceptance, assignment, and public interfaces informed the independent source pass.
There is no tracked repository instruction file.
The [full diff](receipts/full.diff), [one-commit delta](receipts/round5.diff), and [history](receipts/history.txt) were examined.
The delta is one commit on `82422d6ffe38d430576cd9d874a45b9e124e6c63`.
The [independent verdict and ledger](receipts/independent-verdict.md) were written before reading prior public findings.
Earlier executable probe sources were replayed without reading their report conclusions first.
Supplemental parent-authority checks followed that independent pass.

The parent [requirements][requirements], [reservation requirements][frnfr], and [mailbox interface][mailbox] retain transport, admission, and hardware ownership outside this library.
The [boundary receipt](receipts/interface-boundary.txt) records that assessment.
No private author material, management workspace, or other checkout was read.
No source fix, commit, remote write, delegated review, or hardware action occurred.

**R541-4-F1 — MAJOR — Conformance, Robustness, Tests, Docs — OPEN**

**A received Join can cancel a failed topology Flush before its retry.**

Artifacts: the [failure handler, source line 644][flush-handler], [Registrar Join rows, source line 350][join-rows], and [topology interface][topology-api].
Related promises appear in the [integration contract][retry-contract], [developer retry graph][retry-guide], and [manager matrix][matrix].

Authority: [round-five item 1][assignment] requires allocation failure never to silently lose topology withdrawal.
The [public interface][topology-api] promises retained work and subsequent retry.
The [Registrar Flush row][flush-row] requires a Leave indication for a registered attribute.
Conformance attribution concerns frozen acceptance and the public interface; it does not assert a standards-defined allocation-exhaustion policy.

On reservation failure, Flush sets LV and arms a one-centisecond timer.
Before that tick, a valid received Join changes LV to IN and stops the same timer.
No independent pending-Flush state remains.
An unchanged Join also produces no replacement registration indication.
Both public calls complete without exposing the lost operation.

This is a permitted serialized sequence.
The integration contract requires deferring topology changes during retained output; these probes have no retained source output.
The parent [event-loop contract][mailbox-loop] also permits topology dispatch followed by receive processing before another tick.

The [interleaving probe](scripts/probe_r4.c) covers all three stream registration types, initial IN/LV, unchanged/changed Joins, and every reservation fault.
Each profile runs 48 cases: 12 controls and 36 faulted cases.
All faulted cases lose the Leave; unchanged Joins additionally lose the fresh Join indication.
The [default](receipts/probe_r4-OFF.log) and [enabled](receipts/probe_r4-ON.log) receipts each contain 54 failed assertions and zero live allocations.
Both builds succeed; both executions return one without a memory-instrumentation error.

A [second probe](scripts/probe_r4_native.c) uses the production stream propagation policy unchanged.
It covers both Talker types, initial IN/LV, and allocation positions zero through three.
All four controls pass; all twelve faulted cases lose the Leave-before-Join sequence in each profile.
See the [default trace](receipts/native-OFF.log) and [enabled trace](receipts/native-ON.log).
Each faulted trace remains empty through 32 tick/poll/receive cycles, while the Registrar remains IN.

| Sequence, both profiles | Leave indications | Fresh Join indication |
| --- | --- | --- |
| Successful Flush, then unchanged Join | One | Present |
| Failed Flush, tick, then unchanged Join | One | Present |
| Failed Flush, unchanged Join, then tick | Zero | Absent |

Impact: temporary exhaustion silently removes a requested withdrawal from the event sequence.
Host state and propagated declarations can retain registration across a topology change without the required withdrawal notification.
Continuing ticks and polls does not recover the lost Flush while unchanged Joins keep arriving.

Required outcome: preserve the pending withdrawal across receive dispatch, or expose a reliable failure-and-retry contract.
A pending Flush must complete before accepting a subsequent registration that would cancel it.
Keep ordinary unchanged LV recovery behavior intact.
Update the interface and guides together, and add named fault-port regressions with a discriminating reversal.

Verification: both interleaving probes must preserve exactly one Leave before the subsequent Join at every fault position.
If the API instead refuses intervening input, document that result and prove its retry reaches the same sequence.
Retain the passing replacement, timer, queue, teardown, and profile tests.

**R541-4-F2 — MINOR — Conformance, Tests, Docs — OPEN**

**The named next-tick regression accepts a two-tick initial Flush retry.**

Artifacts: the [Flush regression, test line 646][flush-test], especially its repeated-failure sequence at [line 663][flush-test-sequence].
The [tester guide][tester-faults] claims repeated-exhaustion coverage; the [integration contract][retry-contract] promises next-tick retry.
Authority: [issue acceptance 2][issue10] requires a failing regression for each new behavior.
The [round-five assignment][assignment] requires allocation-position regressions and a named reversal for retained Flush withdrawal.

The independent `own-flush-two-tick-delay` mutation changes only the initial Flush timer from one centisecond to two.
Its definition is in the [sample runner](scripts/run_reversals.py).
Both mutated builds succeed, and all 75 repository unit tests still pass with normal assertion totals.
See the [default](receipts/reversals-OFF/own-flush-two-tick-delay.log) and [enabled](receipts/reversals-ON/own-flush-two-tick-delay.log) unit receipts.

The named regression always injects another failure before its first tick.
It expects no withdrawal then, without establishing that the timer fired and attempted allocation.
It clears allocation failure before the second tick, allowing the delayed mutant to satisfy every assertion.

This mutation is behaviorally distinct.
The [confirmation runner](scripts/check_deadline_mutation.py) compiles it against [the earlier root probe](scripts/probe_r3.c).
That probe observes withdrawal after two ticks and fails its one-tick check at all three reservation faults.
Both [default](receipts/deadline-plant-probe-OFF.log) and [enabled](receipts/deadline-plant-probe-ON.log) runs fail exactly those three checks.
The unmodified head passes [that probe](receipts/probe_r3-OFF.log).

Impact: the repository test misses a regression in the documented deadline and can mistake an unattempted retry for repeated exhaustion.
The current implementation meets the isolated deadline; this finding concerns regression coverage, not an additional current timer defect.

Required outcome: independently check successful recovery on the first tick and repeated allocation failure on successive ticks.
Verify that each intended fault is actually reached.
Add the two-tick mutation to a named regression requirement, and align the coverage statement with the executed cases.
Verification: the unmodified head passes; the two-tick mutation compiles and fails the named repository test in both profiles.
Keep the existing repeated-exhaustion and teardown assertions.

**Prior public findings at this head**

The [first internal][r540-1], [first external][r541-1], [second internal][r540-2], [second external][r541-2], [third internal][r540-3], and [third external][r541-3] findings were reconciled.
The table distinguishes resolved reported reproducers from the broader remaining Flush guarantee.
Current root evidence includes [receive probes](receipts/probe_rx-OFF.log), [fault sweeps](receipts/probe_fault-ON.log), and the [named reversal ledger](receipts/reversal-ledger.json).

| Prior finding | Disposition at this head | Current evidence |
| --- | --- | --- |
| R541-3-F1 / R540-3-01 | RETAINED through F1; original tick-before-receive reproducer resolved | Earlier [Flush probe](receipts/probe_flush-OFF.log) passes; receive-before-tick probes fail. |
| R540-3-02 | RESOLVED | [Replacement regression][replacement-test] sweeps all nine allocations in both directions. [Root probe](receipts/probe_r3-ON.log) preserves Leave before Join. Its reversal fails the named test. |
| R540-3-03 | RESOLVED | [y01](receipts/plants-OFF/y01-no-map-error-stop-unit.log), [y02](receipts/plants-OFF/y02-publish-ignores-policy-unit.log), and [y07](receipts/plants-ON/y07-no-policy-still-reserves-unit.log) fail their named tests. The [coverage table][tester-coverage] separates masks from future topology filtering. |
| R540-2-01 | RESOLVED | Both LeaveAll paths preserve changed Listener/Talker indications and propagation. Unchanged recovery stays quiet; the IN-only reversal fails both named tests. |
| R540-2-02 | RESOLVED | Opaque later-version stream messages use their list boundary; receive probes pass and the boundary reversal fails. |
| R541-2-F1 | Reported receive-value loss RESOLVED; broader withdrawal guarantee remains F1 | All reservation positions preserve changed values for retry; the allocation sweep passes. |
| R541-2-F2 | RESOLVED | Host indications precede policy selection; the callback-order reversal fails its named test. |
| R541-2-F3 | RESOLVED | The [integration table][integrator] states eight suites; both executions run eight. |
| R540-2-03 | RESOLVED | Reservation atomicity, rollback, error reporting, poll/commit replay, teardown, changed propagation, and zero-length reversals fail. |
| R541-1-F1 | RESOLVED | Atomic application validation and overflow tests pass; decode, stream, VLAN, MAC, and Domain reversals fail. |
| R541-1-F2 / R540-1-01 | RESOLVED | Higher-version type/event skipping and current-version strictness pass across applications; selected reversals fail. |
| R541-1-F3 | RESOLVED | The [Domain explanation][domain-guide] and [matrix][matrix] cite the Domain clause. |
| R541-1-F4 / R540-1-07 | RESOLVED | Changed guards are braced; the [full-range guard audit](receipts/guard-candidates.txt) has no candidate violations. |
| R541-1-F5 / R540-1-02 | RESOLVED | Both actual embedded source-list links and dispatch probes [pass](receipts/embedded.log). The [bare-metal list][baremetal] includes switch dispatch. |
| R541-1-F6 / R540-1-03 | Original retained-output loss RESOLVED | FIFO order, copied values, reclamation, and accepted-output replay tests pass; reversals fail. |
| R541-1-F7 / R540-1-04 | RESOLVED | All six earlier reversals fail: local/omitted/reserved LeaveAll, Listener subtype, timer upper bound, and leaving-observer reclamation. |
| R541-1-S1 / R540-1-06 / parent R532-1 S2 | RESOLVED | Ordinary unchanged LV recovery stops aging without duplicate indication; its reversal fails. F1 requires distinguishing pending Flush work. |
| R541-1-S2 / R540-1-05 | RESOLVED | Re-declare scope, transmitted LeaveAll scope, and received LeaveAll restart reversals fail named tests. |
| Parent R532-1 S1 | RESOLVED | Type/port LeaveAll isolation passes; widening its scope fails the sampled reversal. |
| R540-2-R1 / R541-2-R1 / R538-2-R2 | RESOLVED | The exact required licence-and-notice sentence appears in the [documentation-check guide][doc-tools]. |
| R540-2-R2 / R541-2-R2 / R538-2-R3 | RESOLVED | Both exact historical licence sentences appear in the [manager guide][manager-licence]. |

No wording-only residue remains open.
The [public plant campaign](scripts/plants_r3.py) still has one equivalent survivor, `y03`, in each profile.
Only transmit events set the pending transmit message, and those events do not allocate indication reservations.
Removing rollback of that unchanged field therefore does not alter failure behavior.

**Executed evidence**

| Check | Result and receipts |
| --- | --- |
| Host units | Eight suites and 75 tests per profile; [default](receipts/unit-OFF.log): 4745 assertions; [enabled](receipts/unit-ON.log): 4733; both exit zero. |
| Configured targets | [Default](receipts/ctest-OFF.log) and [enabled](receipts/ctest-ON.log): 1/1 passes; both builds succeed. |
| Scenarios | [Default](receipts/scenario-OFF.log) and [enabled](receipts/scenario-ON.log): one feature, three scenarios, ten steps pass. |
| Isolated codec | [Nine tests, 1690 assertions](receipts/codec.log); exit zero. |
| Earlier public probes | Receive probes and [root allocation/replacement probe](receipts/probe_r3-OFF.log) pass in both profiles. |
| Allocation sweep | [2289 checks](receipts/probe_fault-OFF.log) per profile; 54 changed-value cases, 12 unchanged LV cases, repeated timer exhaustion, retained FIFO replay; zero failures/live allocations. |
| Earlier Flush probe | [532 checks](receipts/probe_flush-ON.log) per profile; controls and reservation faults pass. |
| Instrumented units | [Default](receipts/sanitized-unit-OFF.log) and [enabled](receipts/sanitized-unit-ON.log) pass with normal totals and address, undefined-behavior, and leak checking. |
| Published reversal sample | 42 of 80 cases per profile; each sampled behavior compiles and fails its required named tests. |
| Independent reversals | Three per profile: shortened restoration and omitted destination are killed; the two-tick Flush delay survives, as F2 details. |
| Combined sample | [90 executions](receipts/reversal-ledger.json), 90 successful builds, 88 expected test failures, two timing survivors. Both [restored](receipts/reversals-OFF/restored-check.log) [checks](receipts/reversals-ON/restored-check.log) pass. |
| Earlier plant campaign | [Default](receipts/plants-OFF/campaign.log) and [enabled](receipts/plants-ON/campaign.log): 13 of 14 killed; only equivalent y03 survives. |
| Embedded/freestanding | [Both source-list executions](receipts/embedded.log) pass. [Default](receipts/freestanding-OFF.log) and [enabled](receipts/freestanding-ON.log) strict seven-source checks pass. |
| Documentation mechanics | [941 fragments](receipts/docs-sentences.log), zero long sentences; [zero unlinked references](receipts/docs-references.log); [79 reference self-tests](receipts/docs-references-selftest.log). |
| Links and graphs | [352 local links and 20 external URLs](receipts/docs-links.log) pass; repository checks authenticated. [All 27 graphs](receipts/docs-graphs.log) render. |
| Manual documentation | [43 anchors](receipts/source-anchors.txt) identify intended code; the new retry graph was [visually inspected](receipts/graph-review.md). |
| New defect probes | Both interleaving probes fail in both profiles; controls pass. Timing confirmation fails only the three first-tick assertions. |

The original [evidence snapshot][initial-evidence] contains the earlier author packet.
The retrieved [follow-up snapshot][author-r5] supplies round-five records.
The [evidence inventory](receipts/public-evidence.json) records immutable provenance and hashes.
Those published records report all 80 reversals per profile and restored passes.
This review independently ran the stated sample; it does not substitute that sample for the full published campaign.

The [portable reproduction driver](scripts/reproduce.py) uses a fresh packet and keeps dependencies, probe trees, and generated images under scratch.
Supporting scripts record results and complete output.
Published paths are normalized to `$SOURCE` and `$PACKET`; diagnostic content and exit codes are retained.
Initial dependency configuration failed because of a compatibility minimum; the explicit-minimum retry, build, and local installation succeeded.
The [failed configuration](receipts/dependency-configure.log) and [successful retry](receipts/dependency-configure-retry.log) are retained.
No shared installation was changed.

Independent campaigns ran concurrently under foreground orchestration, within sixteen concurrent build slots.
Host and dependency builds used sixteen-job builds; published mutation drivers retained their smaller per-build limits.
No heavy implementation build ran.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN — F1, F2 | Frozen acceptance, public scope, contribution rules, interfaces, Registrar/parser delta, profiles, parent boundaries, root probes | R541-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| RTL | CLEAN | Full changed-file inventory; no RTL/constraints; C source lists; mailbox/hardware ownership; embedded source-list execution | R541-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Robustness | UNCLEAN — F1 | Reservation rollback, replacement ordering, FIFO ownership/replay, timers, interleaving, fault positions, instrumentation, teardown | R541-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Tests | UNCLEAN — F1, F2 | Both profiles, scenarios, codec, fault port, earlier probes, 90 reversal executions, 28 earlier plants, new controls/deadline confirmation | R541-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |
| Docs | UNCLEAN — F1, F2 | Reader guides, README, PR body, retry contract, coverage claims, checks, anchors, graph rendering, exact residue replacements | R541-4 | 0a45695db537badb8d7e9cbf578925fe5b89d647 |

The [integrity receipt](receipts/integrity.json) verifies all 60 tracked blob bytes, modes, and index entries against the assigned head.
The tree and worktree are clean; every tracked file carries the licence identifier.
This repository has zero submodule gitlinks; none required restoration.
All mutations occurred in disposable copies.
The [manifest](MANIFEST.sha256) lists publishable scripts and receipts; scratch is excluded.

**Limits and pending manager duties**

This is source and host-execution evidence, without target execution or network interoperability.
The embedded source-list probe is a host link check, not a complete target build.
The known [scenario assertion limitation][issue4] remains disclosed and outside this delta.
Standards assessment uses frozen public decisions and interface authorities; full normative documents were not reread this round.
Unchanged graph shapes were rendered again; only the new diagram received fresh visual inspection.

The manager reports full source static, builder, and native banks passing at this head.
Those banks were not rerun here, as assigned.
Their source base is `1401654530ce7d9275de9b901e67df47e5bbc536`.
The final candidate against live development head `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` remains separate merge-turn work.

The [exact-head hosted query](receipts/hosted-evidence.json) returned zero workflow runs and zero check runs.
No executed hosted job or skipped context was counted as passing evidence.
Hosted and local acceptance remain manager duties.
Physical calibration is NOT RUN; field skips provide no hardware proof.

The manager must obtain corrections and independent re-review of F1 and F2 before merge acceptance.
Final candidate validation, dependency pins, issue closure, publication, and post-merge containment remain manager duties.
This review performs none of those writes.

[issue10]: https://github.com/kebag-logic/lwSRP/issues/10
[pr]: https://github.com/kebag-logic/lwSRP/pull/12
[start]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035129064
[assignment]: https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6034815912
[contributing]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/CONTRIBUTING.md
[readme]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md
[flush-handler]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/core/mrp_mad.c#L644
[join-rows]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/core/mrp_mad.c#L350
[flush-row]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/core/mrp_mad.c#L378
[topology-api]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/include/shish_lan/mrp.h#L343
[retry-contract]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md#transmit-and-retry
[retry-guide]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/developer.md#deferred-propagation
[matrix]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/manager.md#implementation-status
[flush-test]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c#L646
[flush-test-sequence]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c#L663
[replacement-test]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c#L736
[tester-faults]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L34
[tester-coverage]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#coverage
[integrator]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md#build-choices
[domain-guide]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/developer.md#stream-values-and-bounded-interests
[baremetal]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md#embedded-module-and-bare-metal
[doc-tools]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L31
[manager-licence]: https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/manager.md#licence-and-contributions
[requirements]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/REQUIREMENTS.md
[frnfr]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/reference/FR_NFR.md
[mailbox]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/design/MAILBOX_SPLIT.md
[mailbox-loop]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/design/MAILBOX_SPLIT.md#L294
[initial-evidence]: https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1
[author-r5]: https://github.com/kebag-logic/milan-fpga/tree/0c6326966d964ea5400b3ac790614c873d311b19/review-evidence/lwsrpm2-r1/author-r5
[r540-1]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319
[r541-1]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033216570
[r540-2]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033931109
[r541-2]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033978356
[r540-3]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034569438
[r541-3]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034811505
[issue4]: https://github.com/kebag-logic/lwSRP/issues/4

R541-4 FINISHED

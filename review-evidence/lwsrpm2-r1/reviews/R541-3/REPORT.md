[R541] NEGATIVE - exact head 82422d6ffe38d430576cd9d874a45b9e124e6c63
<!-- SPDX-License-Identifier: Apache-2.0 -->

The reported round-four cases are corrected, but one allocation-failure path still loses a required withdrawal.
A topology Flush has neither an error result nor automatic recovery after propagation reservation fails.
One MAJOR finding remains open.

Tree: `02fda6f08254fc7dd5c259c996cfbb31e76682d7`.
The reviewed change is one commit above `a9cd5ef58a2478cb2ce4899b31aa02d5c2072646`.
The complete PR comparison starts at `1401654530ce7d9275de9b901e67df47e5bbc536`.

**Reconstruction and independence**

I read the supplied repository instructions, [contribution rules][contributing], [readme][readme], and all reader guides first.
I then reconstructed [frozen acceptance][issue10], the [round-four assignment][assignment], and earlier manager scope decisions.
The linked [destination][issue6], [LeaveAll][issue7], and [profile][issue11] requirements remained in scope.
The [documentation ownership rules][issue1] also remained binding.

Interface review covered [application callbacks][header], the [allocation port][alloc], [timer port][timer], and [integration contract][integrator].
Parent context included [product ownership][requirements], [functional and service requirements][frnfr], and the [mailbox boundary][mailbox].
These preserve fabric ownership of framing, timestamps, media, and time synchronization.

I inspected the complete comparison, history, and [round-four delta](receipts/round4.diff) before opening prior public findings.
The [independent-pass receipt](receipts/independent-pass.txt) records that ordering.
No other reviewer's report file or private author material was read.
Earlier findings were read from permitted public PR comments after that pass.
No source edits, commits, pushes, remote writes, or delegated reviews occurred.
The [public review start][review-start] pins the assigned source head and review boundary.

The [initial public evidence snapshot][initial-evidence] contains the original author packet.
The later [public author packet][author-r4] supplies round-four command and reversal records.
Its retrieved evidence tree was `46780a0e1351b17df5db2c3726f5691ed5cb7950`.
The [evidence summary](receipts/public-evidence.json) distinguishes published records from this review's executions.

**Open finding**

**R541-3-F1 — MAJOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifacts: [src/core/mrp_mad.c:642][failure-handler], [src/core/mrp_mad.c:737][discarded-result], and [src/core/mrp_mad.c:1095][topology].
The [public topology interface][topology-api] returns no status.
The [Registrar guide][registrar-guide] displays Flush transitions to MT and claims agreement with the default table.

Authority: [round-four item 3][assignment] requires propagation to survive allocation failure through retention or atomic refusal.
The [public interface][topology-api] identifies Flush as the requested topology operation.
Its [Registrar table][registrar-table] requires withdrawal and MT for a registered attribute.
The normative reference is [IEEE 802.1Q-2018, Table 10-4 and clause 10.7.5.2][ieee].
[Issue acceptance 2][issue10] also requires discriminating regression coverage.

When reservation fails, the Registrar returns to its previous state.
Retry is armed only for Leave-timer expiry.
The topology broadcast discards the returned error, and the public caller receives no failure indication.
No pending Flush remains for later dispatch.

The independent [Flush probe](scripts/probe_flush.c) registers a Talker on port zero and propagates it to two destinations.
It fails each of the three reservation allocations separately, then resumes allocation immediately.
Every port is polled while an unchanged peer Join continues for thirty ticks.
The probe uses valid configured timer values and serialized callbacks.

| Case, in both profiles | Immediately after Flush | After continued dispatch |
| --- | --- | --- |
| No allocation failure | MT; one Leave indication | One Leave, two Joins, three policy calls |
| Failure at reservation 1, 2, or 3 | IN; no Leave indication | Zero Leaves, one Join, one policy call |

The faulted paths never publish the withdrawal or its propagation.
Unchanged redeclarations cannot recover the lost operation.
Both [default](receipts/flush-run-OFF.log) and [enabled](receipts/flush-run-ON.log) executions return 1 with six failed assertions.
Both compilations return zero; memory instrumentation reports no memory error or leak.
Each execution finishes with zero live allocations.

This defect also exists at the previous PR head.
The [historical default](receipts/flush-previous-run-OFF.log) and [historical enabled](receipts/flush-previous-run-ON.log) probes reproduce missed withdrawals at failure slots one and two.
Their additional ordering failures belong to the previously reported callback defect.
This finding is newly identified within the PR, rather than introduced by its final commit.

Impact: temporary allocation exhaustion silently suppresses a topology withdrawal and leaves host registration state stale.
The caller cannot follow a failure-and-retry contract because the operation returns no result.
Passing receive and timer allocation tests do not cover this entry point.
The documented Flush transition needs a matching failure-handling contract and implementation.

Required outcome: retain and retry the failed topology operation, or expose an explicit failure contract permitting reliable caller retry.
Preserve withdrawal ordering and eventual propagation after memory becomes available.
Add a fault-port regression and a named reversal for this path.
Update the affected interface and guide together.

Verification: the [Flush runner](scripts/run_flush.py) must return zero in both profiles for the control and every failure slot.
The withdrawal must occur exactly once, and subsequent registration must be indicated correctly.
Retain the currently passing receive, timer, callback-order, queue, and teardown checks.

**Prior public findings at this head**

The [first internal findings][r540-1], [first external findings][r541-1], [second internal findings][r540-2], and [second external findings][r541-2] were reconciled individually.
“Resolved” below applies to each reported reproducer and required correction.
The broader allocation-loss guarantee remains incomplete because of R541-3-F1.

| Finding | Disposition and current evidence |
| --- | --- |
| R540-2-01 | RESOLVED. Both LeaveAll paths preserve changed Listener and Talker indications and propagation. Unchanged recovery emits no duplicate indication. |
| R540-2-02 | RESOLVED. Opaque later-version stream messages use their advertised list boundary. Generic VLAN/MAC traversal and current-version rejection remain covered. |
| R541-2-F1 | Reported changed-value loss RESOLVED. All reservation positions preserve old values and state; identical receive retries deliver the update. |
| R541-2-F2 | RESOLVED. Host indications precede policy selection for Join and Leave. The ordering reversal fails its named regression. |
| R541-2-F3 | RESOLVED. The integration table says eight suites; eight execute in each profile. |
| R540-2-03 | Reported gaps RESOLVED. Reservation, rollback, error reporting, poll/commit replay, teardown, changed propagation, and zero-length checks have failing reversals. |
| R540-2-R1 / R541-2-R1 / R538-2-R2 | RESOLVED. The [documentation-check guide][doc-tools] contains the exact required licence-and-notice sentence. |
| R540-2-R2 / R541-2-R2 / R538-2-R3 | RESOLVED. The [manager guide][manager] contains both exact historical licence sentences. |
| R541-1-F1 | RESOLVED. Atomic application-range and vector-overflow regressions pass. Selected decode, stream, VLAN, MAC, and Domain reversals fail. |
| R541-1-F2 / R540-1-01 | RESOLVED. Later-version type/event skipping and current-version strictness pass, including opaque stream extensions. |
| R541-1-F3 | RESOLVED. The [Domain description][domain-guide] cites clause 35.2.2.9. |
| R541-1-F4 / R540-1-07 | RESOLVED. Reported changed guards have braces; the current delta introduces no unbraced guard body. |
| R541-1-F5 / R540-1-02 | RESOLVED. Both embedded source-list links and dispatch executions pass. The [bare-metal list][baremetal] names switch dispatch. |
| R541-1-F6 / R540-1-03 | Original retained-output loss RESOLVED. Queue ownership, order, reclamation, and accepted-output replay regressions pass. |
| R541-1-F7 / R540-1-04 | RESOLVED. All six reported surviving behavioral reversals now fail named checks in both profiles. |
| R541-1-S1 / R540-1-06 / parent R532-1 S2 | RESOLVED. Unchanged LV recovery cancels aging without extra indication; its reversal fails. Changed recovery is independently covered. |
| R541-1-S2 / R540-1-05 | RESOLVED. Re-declare scope, transmitted LeaveAll scope, and received LeaveAll restart reversals fail named checks. |
| Parent R532-1 S1 | Remains RESOLVED. Type-and-port isolation passes; widening LeaveAll delivery fails the multi-type regressions. |

Root receipts are the [receive probes](receipts/probe-rx-OFF.log), [fault sweep](receipts/fault-OFF.log), and [complete sampled reversal ledger](receipts/reversal-ledger.json).
Corresponding enabled-profile receipts are included in the manifest.
No wording residue remains open.

**Executed evidence**

| Check | Result |
| --- | --- |
| Default host suite | Eight suites, 70 tests, 4215 assertions; [exit 0](receipts/unit-OFF.log) |
| Enabled host suite | Eight suites, 70 tests, 4203 assertions; [exit 0](receipts/unit-ON.log) |
| Configured test target | 1/1 passes in each profile; all configuration and build commands return zero |
| Scenarios | One feature, three scenarios, ten steps pass per profile; dry run only validates matching |
| Isolated codec | Nine tests, 1690 assertions; [exit 0](receipts/codec.log) |
| Required receive probes | p1a–p1d and p2–p2c pass in [default](receipts/probe-rx-OFF.log) and [enabled](receipts/probe-rx-ON.log) profiles |
| Independent allocation sweep | 54 changed-value cases, 12 unchanged LV cases, repeated timer exhaustion, and retained FIFO replay per profile |
| Sweep assertions | 2289 checks per profile; zero failures, zero live allocations; [default](receipts/fault-OFF.log), [enabled](receipts/fault-ON.log) |
| Instrumented complete suites | Both profiles pass with normal assertion totals; address, undefined-behavior, and leak checks enabled |
| Reversals | 37 published cases plus two independent faults detected per profile; 78 successful builds followed by expected test failures |
| Restored reversal trees | Both restored builds and test targets pass; originals were never mutated |
| Embedded and freestanding | Both profiles pass source-list execution and strict seven-source compilation/dependency checks |
| Documentation | 925 fragments; zero long sentences; zero unlinked references; 79 reference self-tests pass |
| Links and graphs | 347 local links, 20 external URLs, 26 graph renders; all pass; maximum 12 nodes |
| Manual documentation checks | All 43 source anchors inspected; both changed receive diagrams viewed; exact residue replacements confirmed |
| New Flush probe | Compiles successfully; fails behavior assertions in both profiles, as detailed in F1 |

The independent reversals truncate saved-value restoration and omit the last possible propagation destination.
Both fail required named regressions after successful compilation.
Every sampled behavioral reversal has build and test receipts, including observed failed test names.
The public author record contains 75 reversals per profile; this review independently executes the stated sample.

Campaigns ran concurrently under foreground orchestration.
Host builds used sixteen build jobs with a shared build lock.
Concurrent reversal campaigns each used two build jobs.
No heavy implementation build ran.
The [portable reproduction script](scripts/reproduce.sh) recreates dependencies and disposable products under packet scratch.
Run it with the checkout path in a fresh packet containing these scripts.
Its final failing exit currently reproduces F1.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN | Frozen scope, interfaces, Registrar/parser changes, profiles, LV recovery, extensions, allocation and Flush probes; F1 | R541-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| RTL | CLEAN | Changed-file inventory, C/module boundaries, parent ownership requirements, embedded links; no RTL or constraint changes | R541-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Robustness | UNCLEAN | Queues, rollback, retry, timers, teardown, instrumented suites, repeated allocation failures, topology failure propagation; F1 | R541-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Tests | UNCLEAN | Eight suites, scenarios, codec, fault port, 78 reversal executions, controls and missing Flush regression; F1 | R541-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |
| Docs | UNCLEAN | Reader guides, PR body, checks, links, anchors, graphs, residues, allocation contract and unsupported Flush guarantee; F1 | R541-3 | 82422d6ffe38d430576cd9d874a45b9e124e6c63 |

The [integrity receipt](receipts/integrity.json) verifies all 60 tracked blob bytes, Git modes, and index entries against the assigned head.
The worktree is clean; every tracked file carries its licence identifier.
This repository contains zero submodule gitlinks; none required restoration.
The [interface-boundary receipt](receipts/interface-boundary.txt) records the RTL scope assessment.

**Limits and pending manager duties**

This is source and host-execution evidence, without target execution, physical calibration, network interoperability, or hardware proof.
The source-list probe is not a complete target-platform build.
The [known scenario assertion limitation][issue4] remains disclosed and outside this delta.
Standards assessment uses frozen public decisions, linked authorities, and interface contracts; full normative texts were not downloaded this round.

The manager reports full source static, builder, and native banks passing at this head.
Those banks were not rerun here, as assigned.
Their source base is `1401654530ce7d9275de9b901e67df47e5bbc536`.
The final candidate against live development head `d51b373ad7e8e8381af2797be3ebb8ee45c62e3c` remains a separate merge-turn obligation.

The exact upstream head returned zero hosted workflow runs and zero check runs in the queried public interfaces.
No executed hosted job or skipped context was counted as passing evidence here.
Hosted-context acceptance remains with the manager.
Physical calibration is NOT RUN; field skips establish no hardware result.

The manager must obtain a correction and independent re-review of F1 before relying on this packet for merge approval.
Final candidate validation, required dependency pins, issue closure, publication, and post-merge containment remain manager duties.
This review performs none of those writes.

[contributing]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/CONTRIBUTING.md
[readme]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/README.md
[issue10]: https://github.com/kebag-logic/lwSRP/issues/10
[assignment]: https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033982129
[review-start]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034322813
[issue1]: https://github.com/kebag-logic/lwSRP/issues/1
[issue4]: https://github.com/kebag-logic/lwSRP/issues/4
[issue6]: https://github.com/kebag-logic/lwSRP/issues/6
[issue7]: https://github.com/kebag-logic/lwSRP/issues/7
[issue11]: https://github.com/kebag-logic/lwSRP/issues/11
[header]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/include/shish_lan/mrp.h
[alloc]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/ports/alloc.h
[timer]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/ports/timer.h
[integrator]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/integrator.md
[requirements]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/REQUIREMENTS.md
[frnfr]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/reference/FR_NFR.md
[mailbox]: https://github.com/kebag-logic/milan-fpga/blob/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/docs/design/MAILBOX_SPLIT.md
[initial-evidence]: https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1
[author-r4]: https://github.com/kebag-logic/milan-fpga/tree/a07d7c63a66a5149392ddb999a67710d8ef53f5d/review-evidence/lwsrpm2-r1/author-r4
[failure-handler]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_mad.c#L642
[discarded-result]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_mad.c#L737
[topology]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_mad.c#L1095
[topology-api]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/include/shish_lan/mrp.h#L340
[registrar-table]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_mad.c#L378
[registrar-guide]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/developer.md#registrar
[domain-guide]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/developer.md#stream-values-and-bounded-interests
[baremetal]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/integrator.md#embedded-module-and-bare-metal
[doc-tools]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/tools/README.md
[manager]: https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/manager.md
[ieee]: https://standards.ieee.org/ieee/802.1Q/6844/
[r540-1]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319
[r541-1]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033216570
[r540-2]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033931109
[r541-2]: https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033978356

R541-3 FINISHED

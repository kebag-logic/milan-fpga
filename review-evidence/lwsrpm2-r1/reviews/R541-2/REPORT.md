[R541] NEGATIVE - exact head a9cd5ef58a2478cb2ce4899b31aa02d5c2072646
<!-- SPDX-License-Identifier: Apache-2.0 -->

The original receive, extension, embedded-link, retained-propagation, and recovery findings are resolved for their reported stimuli.
Two propagation regressions and one inaccurate suite count remain open.
Two carried licence wording residues also remain.
All five lenses were applied independently at this head.

**Scope and authorities**

The verified tree is bc5b80a60d923ce869647e3f3ba95276456864d1.
The source base is 1401654530ce7d9275de9b901e67df47e5bbc536.
The delta is the single commit after 23d9a817.
That parent's tree equals the previously reviewed 86a5f74c tree, 7cf49d0d499d21227764282b9d64c8de86f83758.
The [byte audit](receipts/final-source-audit.json) verifies all 58 tracked blobs, modes, index entries, head, and tree.
This repository has no submodule gitlinks.

Reconstruction followed the contribution rules, reader guides, frozen issue scope, linked authorities, interfaces, diff, history, and public evidence.
No repository instruction file exists in the reviewed tree.
The [independent pass receipt](receipts/independent-pass.txt) preceded reading prior public findings.
The operative scope is the [issue acceptance](https://github.com/kebag-logic/lwSRP/issues/10) and [round-three assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033222017).
The [contribution rules](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/CONTRIBUTING.md), [documentation acceptance](https://github.com/kebag-logic/lwSRP/issues/1), and [profile acceptance](https://github.com/kebag-logic/lwSRP/issues/11) also apply.

The local normative documents were checked directly, without republishing their text.
Comparisons covered [IEEE 802.1Q-2018, Table 10-4 and clauses 10.8.3.5, 35.2.2.8, and 35.2.2.9](https://standards.ieee.org/ieee/802.1Q/6844/).
The profile comparison covered [Milan v1.2, clause 4.2.7.2.2](https://milanav.com/milan-faqs/).

**R541-2-F1 — MAJOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifact: [src/core/mrp_mad.c:959](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_mad.c#L959), especially the changed-value path at [line 997](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_mad.c#L997).
Authority: the [round-three propagation requirement](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033222017) and [queue reservation contract](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/developer.md#deferred-propagation).

A changed Join updates the stored source value and issues its indication before reserving propagation work.
If that allocation fails, receive returns a memory error, but the new source value remains installed.
Retrying the identical PDU clears the error and succeeds without queuing the update.
The equality check now treats the changed value as unchanged.
The destination consequently keeps its old declaration.

The independent probe uses the normal stream propagation policy and two ports.
It changes a Talker's maximum frame size from 100 to 200 and fails exactly the next allocation.
Both profiles return -12, then return zero on retry, while the destination remains at 100 after 100 ticks and transmit polls.
The source holds 200.
The no-failure control propagates 200 successfully.
Evidence: [default failure](receipts/probe-allocation-OFF.log), [enabled failure](receipts/probe-allocation-ON.log), and [control](receipts/probe-allocation-control-OFF.log).
The probes run with memory and undefined-behavior instrumentation.

Impact: temporary pool exhaustion permanently loses a registration update despite a successful retry.
The published suites pass without detecting this failure.
The documented reservation-before-indication guarantee also does not hold on this path.

Required outcome: preserve pending propagation, or preserve enough previous state for a retry to deliver the update reliably.
Reserve work consistently before publishing the corresponding indication.
Add a named allocation-failure regression and a reversal that fails it.
Verification: both allocation probe modes must pass, and every destination must eventually hold 200 without an additional changed advertisement.

**R541-2-F2 — MINOR — Conformance, Robustness, Tests, Docs — OPEN**

Artifact: [src/core/mrp_mad.c:631](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_mad.c#L631), preceding the indications at [line 650](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_mad.c#L650).
Authority: the [public callback ordering contract](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/include/shish_lan/mrp.h#L158).
It places propagation policy after the corresponding host indication.

The new Registrar path evaluates policy before notifying the host.
A conforming policy can therefore inspect stale host state and choose the wrong destination mask.
The independent probe's host indication enables propagation to port 1.
At this head, receive succeeds and indicates registration, but policy observes the old state and port 1 receives nothing.
The complete exported parent tree selects port 1 correctly.
Evidence: [default](receipts/probe-order-OFF.log), [enabled](receipts/probe-order-ON.log), and [parent control](receipts/probe-order-parent-control.log).

Impact: existing custom applications can silently stop propagating registrations or apply stale withdrawal policy.
The [changed receive graph](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/architecture.md#receive-path) describes the new order while the public header retains the original guarantee.
This changes interface behavior and is not wording-only residue.

Required outcome: preserve the published callback ordering while retaining queued propagation guarantees.
Keep the interface, graphs, and implementation consistent.
Add a named callback-order regression with a discriminating reversal.
Verification: the order probe must produce one destination instance and observe the completed indication in both profiles.

**R541-2-F3 — MINOR — Conformance, Docs — OPEN**

Artifact: [doc/integrator.md:19](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/integrator.md#L19).
Authority: [issue acceptance 3](https://github.com/kebag-logic/lwSRP/issues/10) requires coherent documentation for changed behavior.

The build table still says the unit runner contains seven suites.
The [runner](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/unit/main.c) now registers eight, confirmed by both [default](receipts/unit-OFF.log) and [enabled](receipts/unit-ON.log) execution.
Impact: the integration guide reports an incorrect test inventory and disagrees with the other reader guides.
Required outcome: replace “seven suites” with “eight suites.”
Verification: compare the corrected table with the eight registered and executed suites.
This changes a numerical test inventory, so the wording-only residue exception does not apply.

**R541-2-R1 — RESIDUE — Docs — OPEN**

Artifact: [doc/tools/README.md:31](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/tools/README.md#L31).
Authority: the [manager's carried wording correction](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033473193), inherited identifier R538-2-R2.
The requested replacement remains unapplied; the current sentence still describes a combined tree.
Impact is limited to prose about files that already exist.
Required exact replacement:

~~~markdown
The [licence](../../LICENSE) and [notice](../../NOTICE) links are required and must resolve.
~~~

Verification: inspect the replacement and rerun the documentation checks.
This residue does not dirty a lens or determine the verdict.

**R541-2-R2 — RESIDUE — Docs — OPEN**

Artifact: [doc/manager.md:91](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/manager.md#L91) and its following sentence.
Authority: the [manager's carried wording correction](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033473193), inherited identifier R538-2-R3.
The present-tense separate-licence wording remains after the licence merge.
Impact is limited to stale release prose; both licence files are present.
Required exact replacements:

~~~markdown
The [release issue](https://github.com/kebag-logic/lwSRP/issues/1) required the licence and documentation before publication.
The [licence issue](https://github.com/kebag-logic/lwSRP/issues/8) added both files.
~~~

Verification: inspect both replacements and rerun the documentation checks.
This residue does not dirty a lens or determine the verdict.

**Prior finding reconciliation**

The [prior external findings](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033216570) and [prior internal findings](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319) were reconciled after the independent diff pass.
Each disposition below applies to the exact assigned head.

| Prior finding | Disposition and root evidence |
| --- | --- |
| R541-1-F1 | RESOLVED. Invalid final Domain values cause zero attribute or LeaveAll callbacks. All three stream types reject identity wrap and accept legal maxima. See [atomic](receipts/probe-atomic-OFF.log), [overflow](receipts/probe-overflow-ON.log), and [range reversals](receipts/mutation-ledger.tsv). |
| R541-1-F2 / R540-1-01 | RESOLVED. Structural skipping preserves following declarations for VLAN, MAC, and stream applications. The independent unknown value contains zero bytes and multiple packed events. See [extension probes](receipts/probe-extensions-OFF.log) and [named extension reversals](receipts/mutation-ledger.tsv). |
| R541-1-F3 | RESOLVED. The [Domain increment citation](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/developer.md#L290) names [clause 35.2.2.9](https://standards.ieee.org/ieee/802.1Q/6844/). The [manager matrix](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/manager.md#L32) includes it. |
| R541-1-F4 / R540-1-07 | RESOLVED. The reported changed guards now have braces. Manual inspection and the [statement audit](receipts/guard-audit.txt) found no changed unbraced guard bodies. |
| R541-1-F5 / R540-1-02 | RESOLVED. The actual embedded source list links all switch entry points in both profiles. See [embedded execution](receipts/embedded.log) and the [bare-metal list](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/integrator.md#L367). Removing dispatch fails the link. |
| R541-1-F6 / R540-1-03 | Original retained-port loss RESOLVED. The [three-port probe](receipts/probe-retention-ON.log) preserves retry bytes, copied updates, source reclamation, and withdrawal order. New queue-allocation loss remains in F1. |
| R541-1-F7 / R540-1-04 | RESOLVED for every named reversal. Local LeaveAll, omitted-value events, reserved events, Listener subtype, timer upper bound, and leaving-observer preservation each fail named checks. See the [complete mutation ledger](receipts/mutation-ledger.tsv). |
| R541-1-S1 / R540-1-06 / parent R532-1 S2 | RESOLVED. [Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/) requires timer cancellation and IN without another Join indication. Both Join variants pass the [independent recovery probe](receipts/probe-recovery-ON.log); their reversal fails the named regression. |
| R541-1-S2 / R540-1-05 | RESOLVED. Re-declare, transmitted LeaveAll, and received LeaveAll restart each have a failing reversal in the [ledger](receipts/mutation-ledger.tsv). |
| Parent R532-1 S1 | Remains RESOLVED. Type-and-port isolation tests pass; the all-types reversal fails both supported multi-type application regressions. |

**Executed evidence and lens assessment**

| Check | Result at this head |
| --- | --- |
| Host profiles | Both configure and build successfully. Each test target passes. [Default](receipts/unit-OFF.log): 60 tests, 3896 assertions. [Enabled](receipts/unit-ON.log): 60 tests, 3884 assertions. |
| Scenarios | [Default](receipts/behave-OFF.log) and [enabled](receipts/behave-ON.log): one feature, three scenarios, ten steps; rc 0. The [dry run](receipts/behave-dry.log) remains separate. |
| Published reversals | All 60 detected in each profile, exceeding the requested sample. Both [default](receipts/reversals-OFF.log) and [enabled](receipts/reversals-ON.log) campaigns restore passing builds and checks. |
| Independent plants | Wrong Domain byte order, omitted destination increment, and suppressed destination replay each compile and fail named tests in both profiles. See [mutation ledger](receipts/mutation-ledger.tsv). |
| Instrumentation | The [enabled unit suite](receipts/sanitize-unit.log) passes all 60 tests and 3884 assertions with memory, undefined-behavior, and leak checks. Independent probes use instrumentation in both profiles. |
| Embedded and freestanding | [Embedded dispatch](receipts/embedded.log) and strict [default](receipts/freestanding-OFF.log) / [enabled](receipts/freestanding-ON.log) checks pass. Seven translation units are checked per profile. |
| Documentation | [Sentence](receipts/sentences.log): 904 fragments, none over 25 words. [References](receipts/references.log): zero unlinked references. [Self-tests](receipts/reference-selftest.log): 79 pass. |
| Links and diagrams | [Links](receipts/links.log): 345 local links and 19 external URLs pass. [Rendering](receipts/graphs.log): 26 graphs pass, maximum 11 nodes. Repository URLs use authenticated access. |
| Manual documentation review | Both changed diagrams are readable. All [43 source anchors](receipts/source-anchors.txt) identify their intended code. See [visual scope](receipts/graph-review.md). F2 and F3 remain despite mechanical passes. |
| Repository integrity | [Final audit](receipts/final-source-audit.json): 58 tracked files match exact blobs and modes; index and working tree are clean. No required gitlinks exist. |

Conformance was assessed against frozen scope, the normative clauses, interface contracts, parser boundaries, Registrar actions, and the declaration updates.
The received-Leave option retains its single-cell scope; both published profile fault reversals remain discriminating.
The remaining conformance defects are the propagation contracts and documentation accuracy recorded above.

RTL was assessed independently through the complete changed-file inventory, both build branches, and embedded dispatch execution.
There is no RTL implementation or hardware change in this standalone library.
RTL is clean as not applicable; the host link probe establishes no target execution claim.

Robustness review covered receive atomicity, value arithmetic, copied queue storage, refusal ownership, source reclamation, timer recovery, allocation failure, and callback ordering.
The normal paths pass; F1 and F2 demonstrate failures outside the published regression coverage.

Tests review distinguished successful builds, executed assertions, expected failing mutations, restoration checks, and scenario limitations.
All 126 profile-specific mutation executions were detected.
The [scenario limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains disclosed: its assertions repeat operations instead of independently reading port state.
Passing those scenarios is not protocol or hardware proof.

Docs review covered every reader guide, the changed graphs, interface comments, clause citations, anchors, licence prose, and the public PR body.
The Domain authority and embedded recipe are corrected.
The callback contradiction, suite inventory, and two carried residues remain as identified above.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN — F1, F2, F3 | Frozen acceptance, normative clauses, callback interface, parser, Registrar, queue, literal-wire and failure probes. | R541-2; prior findings reconciled | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| RTL | CLEAN — not applicable | Complete diff inventory, standalone source tree, host and embedded build lists, dispatch link probe. | R541-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Robustness | UNCLEAN — F1, F2 | Decode ranges, overflow, FIFO lifetime, retained bytes, three-port replay, allocation and ordering controls, instrumentation. | R541-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Tests | UNCLEAN — F1, F2 | Eight suites, both profiles, scenarios, 120 published reversal executions, six independent plants, named failures and restored checks. | R541-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |
| Docs | UNCLEAN — F1, F2, F3 | Four reader guides, interface contracts, public PR body, clause matrix, 26 renders, changed diagrams, 43 anchors, documentation checks. | R541-2 | a9cd5ef58a2478cb2ce4899b31aa02d5c2072646 |

**Public evidence, limits, and pending manager duties**

The [initial public archive](https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1) supplies historical evidence.
The [round-three archive](https://github.com/kebag-logic/milan-fpga/tree/de6b34ba0418aea03f065fe691b2ebe0f0f91c8a/review-evidence/lwsrpm2-r1/author-r3) supplies the updated author packet.
Its six selected files match the [published hashes](receipts/public-archive-inventory.json).
Its final published-command inventory records 27 successful commands; its earlier exploratory failures remain visible in the [evidence summary](receipts/public-evidence-summary.txt).
Those public claims are distinguished from the independent executions above.

The [exact-head hosted snapshot](receipts/hosted-contexts.json) has zero workflow runs, check runs, and commit statuses.
There are no executed or skipped jobs to count as acceptance evidence.
The manager's source-bank success is supplied by the assignment; it is distinct from final candidate validation.
No corresponding exact-head source-bank receipt appeared in the examined issue or PR comments.

The manager must obtain fixes and renewed independent positive reviews before accepting this head.
Carry R1 and R2 to the residue checklist.
The manager owns publication, closing issues, hosted acceptance, and final current-dev candidate construction at merge time.
The supplied live-dev baseline is d51b373ad7e8e8381af2797be3ebb8ee45c62e3c; this review did not construct that candidate.

Physical calibration was NOT RUN.
Field skips and host results are not hardware proof.
No parent, processor, timing-protocol, synthesis, builder-bank, container, or hardware campaign ran here.
No simulator was needed for this source-only delta.
No source fixes, commits, pushes, remote writes, author contact, or delegation occurred.
No target build, network interoperability, exhaustive state coverage, or bounded target memory budget is claimed.

The remaining 24 diagrams received rendering checks; their visual evidence is carried from the public packet.
Temporary dependencies, exported trees, builds, original transcripts, and graph images remain in unpublished scratch.
Published receipts preserve process output with location prefixes replaced by portable aliases.
All foreground campaign drivers completed before this report was finalized.
The [portable reproduction instructions](REPRODUCE.md) and [manifest](MANIFEST.sha256) identify the publishable packet.

R541-2 FINISHED

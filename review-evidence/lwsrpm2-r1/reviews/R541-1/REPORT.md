[R541] NEGATIVE - exact head 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9
<!-- SPDX-License-Identifier: Apache-2.0 -->

Two MAJOR receive-conformance defects and five MINOR acceptance defects remain open.
The required baseline suites pass, including the new Milan withdrawal behavior.
Passing regressions do not cover the independently reproduced receive cases below.

**Scope and independence**

This review covers [PR #12](https://github.com/kebag-logic/lwSRP/pull/12), from base `1a1d6cbe4f971d2d346b948dd2e9716421f211e9` to the exact head above.
The head tree is `7cf49d0d499d21227764282b9d64c8de86f83758`.
The [public start](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032743680) fixes this review round.

I reconstructed the repository instructions, guides, [frozen acceptance](https://github.com/kebag-logic/lwSRP/issues/10), and [merge assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634).
The [second assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032515334) adds the [Milan requirement](https://github.com/kebag-logic/lwSRP/issues/11).
The [destination](https://github.com/kebag-logic/lwSRP/issues/6), [LeaveAll](https://github.com/kebag-logic/lwSRP/issues/7), and [owner documentation rules](https://github.com/kebag-logic/lwSRP/issues/1) also govern acceptance.
I read the local normative editions of [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/) and [Milan v1.2](https://milanav.com/milan-faqs/).
The latter link provides publisher access guidance.
No standard text is redistributed.

The linked [parent assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6030279477) supplies integration context.
I also examined its [requirements](https://github.com/kebag-logic/milan-fpga/blob/50d492c12789e1d80bf11f547e7fe53e02b4bdb9/REQUIREMENTS.md), [timing register](https://github.com/kebag-logic/milan-fpga/blob/50d492c12789e1d80bf11f547e7fe53e02b4bdb9/docs/reference/FR_NFR.md), [mailbox contract discussion](https://github.com/kebag-logic/milan-fpga/blob/50d492c12789e1d80bf11f547e7fe53e02b4bdb9/docs/design/MAILBOX_SPLIT.md), and [adapter contract](https://github.com/kebag-logic/milan-fpga/blob/50d492c12789e1d80bf11f547e7fe53e02b4bdb9/sw/firmware/ctrl/srp/README.md).
Those establish transport, static allocation, serialized dispatch, and parent timing responsibilities; they do not prove library conformance.

The independent diff pass preceded reading the [public author evidence](https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1/author).
An independent verdict and five-lens ledger were saved before reading any other reviewer report.
The subsequently published R540 report was read only after that independent verdict and ledger were written.
No private author material, management material, or unpublished reviewer packet was read.
No source fix, commit, remote write, delegation, shared installation, or hardware operation occurred.

**R541-1-F1 — MAJOR — Conformance, Robustness, Tests**

**Invalid application values bypass atomic validation, and vector arithmetic wraps a stream identity.**

- Location: [receive validation, lines 173–190](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_pdu.c#L173-L190); [stream arithmetic and decoding, lines 284–333](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/modules/msrp.c#L284-L333).
- Authority: [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), 10.8.2.8(d), 10.8.3.3, 35.2.2.8.2, and 35.2.2.9.
  Vector increments must remain within the permitted value range; malformed PDUs require discard under the default profile.
  [Milan v1.2](https://milanav.com/milan-faqs/), 4.2.7.1.2, permits retaining an earlier valid prefix, but forbids processing information after the invalid field.
- Evidence: [overflow receipts](receipts/edge-default-overflow.log) show a two-value Listener vector starting at unique ID 65535 registers IDs 65535 and 0.
  An overflowing Domain priority vector also applies its first value instead of rejecting the default-profile PDU.
  [A second probe](receipts/edge-default-invalid-then-valid.log) puts an invalid priority of 8 before a valid Listener message.
  Reception returns zero and indicates that later Listener.
  This also fails the Milan relaxation.
  Results reproduce in [Milan](receipts/edge-milan-invalid-then-valid.log) and [instrumented execution](receipts/edge-sanitized-invalid-then-valid.log).
  [Legal boundary controls](receipts/edge-default-controls.log) all pass.
- Impact: malformed input can register an unintended stream and produce state changes beyond an invalid field.
  The prevalidation pass cannot prevent these effects because decoding errors are ignored, while arithmetic overflow is not reported.
- Required outcome: validate application ranges and complete vector increments before default-profile state changes.
  Reject overflowing stream IDs and destination addresses without wrapping.
  Do not resume processing later values or messages after an invalid application field.
- Verification: add the literal cases from [the independent probes](scripts/edge_probes.c) to upstream tests, including legal maxima and malformed later messages.
  Require zero indications and unchanged state for default-profile malformed PDUs.
  Exercise both profiles and plant separate range-check and decode-error-handling reversals.

**R541-1-F2 — MAJOR — Conformance, Robustness, Tests, Docs**

**Higher-version extensions cause valid following declarations to be discarded.**

- Location: [type and length validation, lines 133–139](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_pdu.c#L133-L139); [event validation, lines 165–168](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_pdu.c#L165-L168).
- Authority: [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), 10.8.3.5(c)(1–2).
  With a higher protocol version, an unknown type discards its message; an unknown event discards its vector.
  Processing continues with subsequent supported content.
- Evidence: [version probes](receipts/edge-default-versions.log) first confirm that a higher-version ordinary VLAN declaration succeeds.
  An unknown MVRP type followed by that declaration returns -22, with no registration.
  The corresponding MMRP case also returns -22.
  An unknown event followed by a valid vector likewise discards everything.
  [Both-profile](receipts/edge-milan-versions.log) and [instrumented](receipts/edge-sanitized-versions.log) runs reproduce the results.
- Impact: future peers lose otherwise supported registrations merely by including an extension in the same PDU.
  The [existing higher-version regression](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/integration_test.c#L378) covers only an unknown MSRP message.
  The [integrator statement about later versions](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/integrator.md#L154) and [manager receive row](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/manager.md#L29) omit this limitation.
- Required outcome: make version handling distinguish extensions from malformed current-version input.
  Skip the specified message or vector and continue processing supported following content.
  Make the guide and matrix accurately describe the resulting receive contract.
- Verification: add all three failing cases and retain the passing higher-version control.
  Test unknown types in all supported applications, unknown events, and current-version malformed-input rejection.
  Plant reversals against those named tests.

**R541-1-F3 — MINOR — Conformance, Docs**

**The Domain increment explanation cites the stream-reservation clause instead of the Domain clause.**

- Location: [developer guide, lines 278–282](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/developer.md#L278-L282); [manager matrix, line 32](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/manager.md#L32).
- Authority: [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), 35.2.2.8 covers stream reservations; 35.2.2.9 defines Domain discovery and its increments.
- Evidence and impact: the stated Domain behavior is correct for valid values, but its supplied authority does not define that behavior.
  The manager row groups Domain offsets under the same incomplete clause list.
- Required outcome: cite both 35.2.2.8 and 35.2.2.9, or split the Domain explanation and cite 35.2.2.9 directly.
  Add the Domain authority to the manager row.
- Verification: compare the revised sentences and matrix with both clauses, then rerun reference and link checks.
  This is a clause-attribution defect, not wording-only residue.

**R541-1-F4 — MINOR — Conformance**

**Seventeen changed guard lines violate the repository braces rule.**

- Location: examples include [declaration allocation, line 837](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L837) and [codec bounds, line 27](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_pdu.c#L27).
- Authority: [contribution rules, lines 10–12](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/CONTRIBUTING.md#L10-L12) explicitly require braces on new and changed lines.
- Evidence: [the changed-line receipt](receipts/changed-guards.log) lists 17 modified unbraced guards across the core and three applications.
- Impact: the imported delta does not satisfy the applicable contribution rule.
  No runtime failure is attributed to this formatting alone.
- Required outcome: brace those changed guard bodies; unchanged legacy lines need no unrelated cleanup.
- Verification: inspect the base-to-head added lines and rerun the existing compilation and suites.

**R541-1-F5 — MINOR — Robustness, Docs**

**The embedded source list omits the implementation of the public switch entry points.**

- Location: [embedded build list, lines 6–14](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/CMakeLists.txt#L6-L14), [switch declarations](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/include/shish_lan/switch.h#L27), and [bare-metal recipe](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/integrator.md#L341).
- Authority: [issue #10](https://github.com/kebag-logic/lwSRP/issues/10) includes the bare-metal integration contract.
  The [adapter guide](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/integrator.md#L294) directs callers through these entry points.
- Evidence: a new [independent link probe](scripts/module_probe.c), compiled against exactly the module's listed sources, produces [four undefined symbols](receipts/module-list-link.log).
  Including `src/core/switch.c` in the disposable [control link](receipts/module-list-control.log) resolves all four, and [execution succeeds](receipts/module-list-control-run.log).
  The header changed from inline wrappers to external declarations in this delta.
- Impact: an embedded adapter using the documented switch interface cannot link with the advertised source list.
- Required outcome: include the switch implementation in the module and bare-metal recipe, or preserve equivalent inline entry points where appropriate.
- Verification: the unmodified module-list probe must link and execute successfully, and the recipe must include every required source.
  This independently confirms and retains public finding R540-1-02.

**R541-1-F6 — MINOR — Conformance, Robustness, Tests, Docs**

**Internal propagation is silently lost while a destination port retains refused output.**

- Location: [propagation calls, lines 527–549](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L527-L549), [retention guards, lines 830 and 847](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L830), and [retention contract](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/integrator.md#L195).
- Authority: [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), 35.2.4, and the library's documented propagation and retry behavior.
  Propagation is part of the implemented bridge path; internal callbacks cannot be retried by the host's queue of incoming operations.
- Evidence: an independent [two-port probe](scripts/map_probe.c) registers and withdraws a Talker on port 0 while port 1 retains a refused Domain PDU.
  In [default execution](receipts/map-default.log), the Join control yields one target Talker and five messages over 300 centiseconds.
  The retained case yields no target Talker and no message after acceptance resumes.
  The withdrawal control ends in VO; the retained case remains QA and sends four further Talker messages.
  [Milan execution](receipts/map-milan.log) reproduces both failures.
  The helpers ignore the target operation's negative result; no deferred propagation is recorded.
- Impact: transient backpressure can permanently lose a declaration or leave a stale propagated declaration after withdrawal.
  These probes exercise the multiport path; they do not imply a single-port failure.
- Required outcome: preserve and replay internal propagation during retention, with an explicit lifetime and ordering contract.
  Cover both registration and timer-driven withdrawal and update the integration guide.
- Verification: the retained cases must reach the same final state as their controls after output resumes.
  Add a named multiport regression and a reversal that removes propagation preservation.
  This independently confirms and retains public finding R540-1-03.

**R541-1-F7 — MINOR — Tests**

**Six new-behavior regressions survive the unit suite.**

- Location: [transmit tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/transmit_test.c), [timing tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/integration_test.c#L200), and [reversal inventory](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/check_reversals.py).
- Authority: [issue #10 acceptance](https://github.com/kebag-logic/lwSRP/issues/10) requires a failing test for each reverted new behavior.
- Evidence: the independent [reconciliation campaign](scripts/survivors.py) builds each fault separately in the default profile.
  All six faults below pass all 45 tests and 2659 assertions; [the summary](receipts/survivors-summary.log) records build and test return codes.

| Surviving fault | Changed artifact | Missing observation |
| --- | --- | --- |
| Remove committed local rLA | `src/core/mrp_mad.c:1284` | Local event after accepted LeaveAll, required by 10.7.6.6. |
| Remove omitted-value txLAF | `src/core/mrp_mad.c:1265` | Omitted Applicant transitions when a LeaveAll PDU is full. |
| Accept reserved LeaveAll values | `src/core/mrp_pdu.c:157` | Rejection of LeaveAllEvent encodings 2–7. |
| Always transmit Listener Ready | `src/core/mrp_mad.c:1168` | Actual subtype bytes after an Asking Failed declaration. |
| Permit the upper LeaveAll boundary | `src/core/mrp_mad.c:663` | A seed that reaches the forbidden upper boundary or exceeds it. |
| Reclaim LO | `src/core/mrp_mad.c:965` | Preservation of a leaving Applicant with pending work. |

- Impact: the published reversal inventory does not establish the frozen coverage requirement for these behaviors.
  A coarser widening toward twice the configured interval does fail the timing test; the near-boundary reversal still survives.
- Required outcome: add a discriminating test and named reversal for each row.
- Verification: each single fault must compile and fail its named assertion, while the restored tree passes.
  This independently confirms and retains public finding R540-1-04.

**R541-1-S1 — SUGGESTION — Conformance, Tests**

**Retain the inherited extra Join indication as a separate follow-up.**

- Location: [Registrar Join rows, lines 338–350](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L338-L350).
- Authority: [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), Table 10-4, requires stopping the Leave timer and returning to IN for received Join in LV.
  It does not issue another Join indication.
- Evidence: [the independent recovery probe](receipts/edge-default-rejoin.log) observes two Join callbacks and two propagation calls over registration, Leave, and Join recovery.
  The table requires only the initial indication.
  Both received Join variants use the same extra action.
- Impact: the state transition and timer recovery are correct, but host callbacks and bridge propagation run redundantly.
  This is an actual IEEE deviation inherited from before this delta.
  The [developer comparison](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/developer.md#L190-L193) and [manager matrix](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/manager.md#L23) now disclose it correctly.
- Suggested outcome: track and correct the extra action separately, with callback-count and propagation-count regressions.
- Verification: registration followed by Leave and Join recovery returns IN, cancels aging, and produces no additional Join or propagation callback.
  This retains parent suggestion R532-1 S2 without expanding this merge into an inherited-behavior repair.

**R541-1-S2 — SUGGESTION — Tests**

**Pin the remaining Milan event boundaries and received LeaveAll timer restart.**

- Location: [Milan transition selector](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L558), [receive LeaveAll handler](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L922), and [Milan tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/milan_test.c).
- Authority: [Milan v1.2](https://milanav.com/milan-faqs/), 4.2.7.2.2, changes one Registrar cell; other events retain the IEEE table.
  The [developer guide](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/developer.md#L221) documents the inherited received-LeaveAll timer restart.
- Evidence and impact: [the campaign](receipts/survivors-summary.log) independently reproduces surviving faults that apply rapid withdrawal to Re-declare or txLA, and omit that timer restart.
  Current code handles those paths correctly, but tests do not pin them.
- Suggested outcome: add state-and-deadline assertions and matching reversals for these paths.
- Verification: each of the three faults fails its corresponding new test.
  This retains public suggestion R540-1-05 without changing the stated issue #11 acceptance result.

**Acceptance and lens evidence**

| Area | Independent result and evidence |
| --- | --- |
| Merge and history | The merge has base `1a1d6cbe` and lane tip `ef8a28b9` as parents. The 20-commit lane ancestry is retained. Licence history is shared. |
| Conflict resolutions | The required dependency, empty-suite guard, reporter cleanup, scenario bindings, and four-reader guides remain. Differences from the lane protocol sources at the merge are explanatory comments. |
| Receive validation | Truncations, complete implicit ends, malformed later messages, reserved packed values, Listener Ignore, and unknown MSRP messages have working regressions. F1 and F2 identify missing cases. |
| LeaveAll scope | [MSRP and MMRP tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/integration_test.c#L70) cover every supported type and both ports. Both Applicant and Registrar isolation are asserted. Widening delivery fails both named tests in [the receipt](receipts/mutations/leaveall-scope.log). Parent R532-1 S1 is resolved. |
| Transmit and splitting | [Transmit tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/transmit_test.c) exercise accepted commits, refusal retention, exact retry bytes, Join spacing, omitted-value fairness, and quiet Listener redeclaration. Published reversals fail; F6 identifies propagation loss and F7 records additional surviving faults. |
| Aging and storage | Timer unlinking, live Registrar aging during refusal, retained withdrawal values, receive interests, and reclamation pass their named regressions and reversals. Serialized lifetime restrictions are explicit. |
| Domain and destinations | Valid Domain encoding and offsets pass. Every application destination is pinned, and each wrong-address reversal fails. MSRP uses 01-80-C2-00-00-0E. F1 concerns invalid ranges; F3 concerns authority attribution. |
| Milan opt-in | [The profile suite](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/milan_test.c) tests both Talker types and Listener withdrawal before receive returns. Default timing, constructor selection, MVRP/MMRP scope, duplicate withdrawal, and LV deadlines pass. |
| Independent Milan reversals | [Delayed IN withdrawal](receipts/mutations/milan-delayed-in-leave.log) fails both immediate tests, without failing the LV deadline test. [Restarted LV timing](receipts/mutations/milan-restarted-lv-deadline.log) fails the deadline test, without failing either immediate test. |
| Freestanding interface | Six protocol translation units pass strict compilation and header-dependency checks in [default](receipts/freestanding-default.log) and [Milan](receipts/freestanding-milan.log) profiles. Hosted-header mutations fail. F5 independently demonstrates incomplete embedded source-list linking with a host compiler. |
| RTL | Not applicable. This is a standalone C11 library. The complete delta and both build lists contain no RTL implementation or hardware change. |
| Documentation | Four reader guides retain the required structure. [Sentence](receipts/sentences.log), [reference](receipts/references.log), and [link](receipts/links.log) checks pass. F2, F3, F5 and F6 remain despite those mechanical passes. |
| Graphs and anchors | All 25 graphs render, with at most 11 nodes. [Visual inspection](receipts/graph-review.md) found readable labels and no unrelated node crossings. All [43 source anchors](receipts/anchors.log) point to the intended definitions or rows. |
| Public hygiene | All 55 tracked files have the Apache-2.0 identifier. No private path or account residue was found. Licence and notice changes add metadata only. [Final byte and index audit](receipts/final-source-audit.log) verifies the frozen tree. |

The disclosed changed-Listener callback sequence remains different from the replacement sequence in [IEEE 802.1Q-2018](https://standards.ieee.org/ieee/802.1Q/6844/), 35.2.6.
It emits an updated Join without a preceding Leave.
The guides state that limitation; this review does not certify complete bridge behavior.

**Executed checks**

| Check | Result |
| --- | --- |
| [Default unit execution](receipts/ctest-default.log) | 45 tests; 2659 assertions; 1/1 test target; rc 0. |
| [Milan unit execution](receipts/ctest-milan.log) | 45 tests; 2647 assertions; 1/1 test target; rc 0. |
| [Default scenarios](receipts/behave-default.log), [Milan scenarios](receipts/behave-milan.log) | Each: one feature, three scenarios, ten steps; rc 0. |
| [Isolated codec](receipts/codec.log) | Nine tests; 1690 assertions; rc 0. |
| [Instrumented Milan suite](receipts/ctest-sanitized.log) | 45 tests; 2647 assertions; address, undefined-behavior and leak checks enabled; rc 0. |
| [Reversal campaign](receipts/mutations.log) | All 39 published reversals and three independent mutations detected; campaign rc 0. |
| [Named mutation ledger](receipts/mutation-ledger.md) | 39 behavioral/layout builds succeed and fail assertions. Three intentional compile/dependency regressions fail their dedicated checks. |
| [Restoration after mutations](receipts/mutation-restoration.log) | Copied source bytes restored; final build and unit run pass. |
| Independent edge probes | Legal controls pass. F1, F2 and the inherited S1 reproduce in both profiles and instrumented execution. |
| [Public-finding probes](receipts/reconcile-probes.log) | Four module-list link errors; added-source control passes. Registration and withdrawal propagation fail in both profiles, with passing controls. |
| [Coverage reconciliation](receipts/survivors-summary.log) | Ten separate builds succeed. Six acceptance faults and three suggestions survive; a coarser timing fault fails. Restored byte comparison, build and unit suite pass. |
| Documentation checks | 860 sentence fragments, zero over limit; zero unlinked references; 79 reference self-tests; 331 local links and 19 external URLs. |

The three independent faults reverse Domain byte order, duplicate Milan Leave indications, and commit a refused transmission.
Each fails its expected named test after successful compilation.
The campaign is broad regression evidence, not exhaustive state or input coverage.

The [scenario assertions](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/features/steps/switch_steps.py#L27-L37) repeat operations and check return codes.
They do not independently observe port state, as [issue #4](https://github.com/kebag-logic/lwSRP/issues/4) and the guides disclose.
A dry run is recorded separately and supplies no protocol execution evidence.

**Public finding reconciliation**

After saving my independent verdict and ledger, the first public snapshot contained only two review-start notices.
A later snapshot included the [published R540 report](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319).
I read that report after my full independent report had been written, then ran the additional reconciliation probes above.
Submitted reviews and inline comments remained empty.

| Public finding | Disposition at the exact reviewed head |
| --- | --- |
| R540-1-01 | RETAINED in F2. Independent probes already covered both unknown application types and unknown events. F2 is MAJOR because supported registrations are lost; it is broader than the prior unknown-type finding. |
| R540-1-02 | RETAINED in F5. New independent source-list link failure and added-source control confirm it. |
| R540-1-03 | RETAINED in F6. New independent registration and withdrawal controls reproduce loss in both profiles. |
| R540-1-04 | RETAINED in F7. Six independently constructed faults compile and survive. |
| R540-1-05 | RETAINED as S2. All three suggested coverage gaps independently reproduce. |
| R540-1-06 | RETAINED as S1, also parent R532-1 S2. The independent callback-count probe preceded the public report. The inherited table comment also overstates the IEEE action. |
| R540-1-07 | RETAINED in F4 with independently assessed MINOR severity. The repository expressly applies its braces rule to changed lines; lack of runtime impact does not waive that contribution requirement. |

Parent R532-1 S1 is resolved by the new type-and-port isolation regressions and the independently killed all-types reversal.
Parent R532-1 S2 remains as the nonblocking inherited deviation documented above.
The upstream link-condition test gap also has new regressions; both guard reversals now fail.
The parent Milan finding is addressed at the library boundary by the optional transition and constructor tests.
Parent adapter selection, integration wiring, and candidate acceptance remain separate duties.

The [public archive](https://github.com/kebag-logic/milan-fpga/tree/eb9c5a65ef3cab26831bff8924c3ec91a5844e30/review-evidence/lwsrpm2-r1) and [command summary](receipts/public-evidence.log) were inspected.
Its final published-command inventory has 25 successful records; its 39-reversal inventory distinguishes expected failing checks from successful builds.
My executed receipts independently reproduce those principal library results.

**Reviewer-owned ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
| --- | --- | --- | --- | --- |
| Conformance | UNCLEAN — F1–F4, F6 | Frozen acceptance, local normative clauses, parser, state tables, stream codec, contribution rules, literal edge and propagation probes. | R541-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| RTL | CLEAN — not applicable | Complete changed-file list, standalone C11 sources, host and embedded build lists. | R541-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Robustness | UNCLEAN — F1, F2, F5, F6 | Range validation, receive effects, timer lifetime, refusal ownership, bounded interests, instrumented runs, module link and multiport probes. | R541-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Tests | UNCLEAN — F1, F2, F6, F7 | Seven suites, both profiles, scenarios, 42 detected reversals, ten reconciliation faults, named failure receipts, independent boundary and propagation probes. | R541-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |
| Docs | UNCLEAN — F2, F3, F5, F6 | All reader guides, clause matrix, PR body, 25 graph renders, visual views, 43 source anchors, documentation checks, embedded recipe and retention contract. | R541-1 | 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9 |

**Limits and pending manager duties**

- Fix and re-review F1–F7 before accepting this head. No wording-only residue is recorded.
- Obtain both independent positive reviews and enforce the remaining publication and merge requirements.
- The exact-head hosted snapshot contains zero workflow runs, zero check runs, and zero commit statuses. Empty contexts are neither executed nor skipped jobs.
- The supplied manager source-bank results are distinct from validation of the final current-dev candidate. This review did not run those banks.
- At the merge turn, the manager owns candidate construction and acceptance against live dev `09f1841bd2c6a9dea8eb1994d887f7386ca4f62d`.
- Physical calibration was NOT RUN. Field skips and host assertions provide no hardware proof.
- No parent, processor, synthesis, builder, container, or hardware campaign ran here. The embedded source list was linked with a host compiler; no target build or execution is claimed. Network interoperability and complete state-table coverage remain unproved.
- All disposable trees and original local transcripts remain in unpublished scratch. Published receipts redact location prefixes only.
- The original clone was never mutated. Final verification covers every tracked blob, executable mode, index entry, head, and tree. This standalone repository has no required submodule gitlinks.

[Reproduction instructions](REPRODUCE.md), portable scripts, rendered graph receipts, and raw process results accompany this report.
Only manifest-listed files and this report are publishable.

R541-1 FINISHED

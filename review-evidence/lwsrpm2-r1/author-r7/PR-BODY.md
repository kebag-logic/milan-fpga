[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support while preserving the test harness, licence, and four reader guides.
The [original assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the merge scope.
The library supports transactional output, receive validation, Domain values, bounded interests, fair splitting, and serialized dispatch.
Destination addressing and received LeaveAll isolation are corrected.
The [optional stream profile](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/doc/integrator.md#milan-received-leave) enables immediate received withdrawal from IN.
LV retains its deadline; VLAN and MAC timing remains unchanged.

## Round 7

Addresses the [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6036261356), [internal finding](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036255540), and [external finding](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036243067).

A failed Flush now owns a value snapshot until its Leave succeeds.
Later local declarations and cross-port propagation can update Applicant storage without changing the owed withdrawal.
Leave indication and propagation use the snapshot.
Repeated failures preserve it; a later independent Flush captures a fresh value.
Receive completes the withdrawal before applying a subsequent registration.
The [interface](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/src/include/shish_lan/mrp.h) and [integration contract](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/doc/integrator.md#transmit-and-retry) describe ownership and retry behavior.

The [new regressions](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/unit/review_test.c) cover all 48 cross-port cases per profile with production propagation policy.
They cover both Talker types, Listener, IN and LV, every reservation fault, and timer or receive completion.
Another 48 cases cover local declarations, repeated failure, Applicant updates, and subsequent Flush snapshots.
The timer-completion regression receives three unchanged registrations and requires exactly one Leave and one Join.
Five new [named reversals](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/check_reversals.py) detect snapshot bypass, replacement, indication, policy, and timer-completion defects.

Validation at [the local head](https://github.com/kebag-logic/lwSRP/commit/14c8b364863be49bc222f4913830b79d23dcf173):

- [Unit runner](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/unit/main.c): eight suites, 86 tests per profile; 19885 default assertions and 19873 enabled assertions; rc 0.
- [Configured tests](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 target per profile; rc 0.
- [Scenarios](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, ten steps per profile; rc 0.
- All 93 [reversals](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/check_reversals.py) detected per profile; restored builds and checks pass; drivers return 0.
- The external cross-port probe passes 48 cases and 2188 checks per profile with zero value mismatches.
- Its broader probe passes 489 cases and 21780 checks per profile. The internal probe passes 243 checks per profile.
- The internal reviewer's exact timer-only mutation fails the new named regression in both profiles; builds return 0 and unit runs return 1.
- Instrumented suites, all retained reviewer probes, [embedded dispatch](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/check_embedded.py), and [freestanding checks](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/tests/check_freestanding.py) pass; rc 0.
- All 27 [published commands](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/doc/tester.md) return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/14c8b364863be49bc222f4913830b79d23dcf173/doc/tools/README.md): 975 fragments; zero long sentences; zero unlinked references; 79 self-tests pass.
- All 354 local links and 20 external URLs pass. Repository links use authenticated access.
- All 27 graphs render; maximum 12 nodes. The changed eight-node retry graph passes visual inspection.
- All 43 source anchors were checked. All 60 tracked files retain the licence identifier.

The [internal review's remaining suggestions](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6036255540) concern pending opposite-Talker replacement coverage and the inherited Flush-triggered LeaveAll test gap.
Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains explicit.
Review roles: integration author, internal reviewer, and external reviewer.

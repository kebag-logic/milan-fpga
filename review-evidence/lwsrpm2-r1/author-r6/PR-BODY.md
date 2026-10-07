[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support while preserving the test harness, licence, and four reader guides.
The [original assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the merge scope.
The library supports transactional output, receive validation, Domain values, bounded interests, fair splitting, and serialized dispatch.
Destination addressing and received LeaveAll isolation are corrected.
The [optional stream profile](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/integrator.md#milan-received-leave) enables immediate received withdrawal from IN.
LV retains its deadline; VLAN and MAC timing remains unchanged.

## Round 6

Addresses the [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6035585910), [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452), and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962).

A pending Flush flag now preserves withdrawal when a registration arrives before the retry tick.
Receive completes the saved-value Leave before applying the incoming registration.
Repeated allocation failure preserves the pending operation and returns an error for payload retry.
Observers receive the retained IN-to-LV transition during the original Flush call.
Ordinary unchanged LV recovery keeps its existing behavior.
The [interface and integration contract](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/integrator.md#transmit-and-retry) explain indication order, retry, polling, and observer behavior.

The [fault regressions](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c) cover all three stream registration types, IN and LV, changed values, and unchanged values.
They check first-tick recovery, repeated failures, receive-before-tick ordering, saved values, observer continuity, and teardown.
Replacement tests start in received-LeaveAll LV, in both directions, at all nine allocation positions.
Receive-stop tests include source-instance allocation failure.
Each change has a required named [reversal](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py).

Validation:

- [Unit runner](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/main.c): eight suites and 81 tests per profile; 16314 default assertions and 16302 enabled assertions; rc 0.
- [Configured tests](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 target per profile; rc 0.
- [Scenarios](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, ten steps per profile; rc 0.
- All 88 [reversals](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py) detected per profile; restored builds and tests pass; driver rc 0.
- Both reviewers' probes pass in both profiles. The internal probe reports 5934 checks and zero observer gaps.
- The external interleaving probe passes 6576 checks per profile. Its production-policy probe preserves Leave before Join in all 16 cases.
- Both LV replacement plants and the source-error guard plant fail their required named tests in both profiles.
- The independent two-tick mutation now fails the next-tick regression in both profiles.
- Instrumented suites, [embedded dispatch](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_embedded.py), and [freestanding checks](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_freestanding.py) pass; rc 0.
- All 27 [published commands](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/tester.md) return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/tools/README.md): 960 fragments; zero long sentences; zero unlinked references; 79 self-tests pass.
- All 354 local links and 20 external URLs pass. Repository links use authenticated access.
- All 27 graphs render; maximum 12 nodes. The changed eight-node retry graph passes visual inspection.
- All 43 source anchors were checked. All 60 tracked files retain the licence identifier.

The reviewer-classified equivalent plants remain documented in the [internal](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) and [external](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962) reviews.
The internal review's pre-existing Flush-to-LeaveAll mutation remains a coverage gap outside the five assigned corrections.
Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains explicit.
Review roles: integration author, internal reviewer, and external reviewer.

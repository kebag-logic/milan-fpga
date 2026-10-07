[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support while preserving the harness, licence, and four reader guides.
The [original assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the merge scope.
The library supports transactional output, receive validation, Domain values, bounded interests, fair splitting, and serialized integration.
Destination addressing and received LeaveAll isolation are corrected.
The [optional stream profile](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md#milan-received-leave) enables immediate received withdrawal from IN.
LV retains its deadline; VLAN and MAC timing remains unchanged.

Range checks reject invalid application values before indications.
Higher protocol versions skip unknown stream messages by list length and unknown VLAN/MAC messages by vector boundaries.
Changed Listener and Talker values indicate and propagate in IN and LV.
The [propagation queues](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/core/mrp_mad.c) own copied values and preserve order across retained output and temporary exhaustion.
Unchanged LV recovery follows [IEEE 802.1Q-2018, Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).

## Round 5

Addresses the [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6034815912), [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034569438), and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034811505).

A failed Flush reservation now retains withdrawal in LV with a one-centisecond Leave timer.
Repeated allocation failures retry on subsequent ticks.
A failed Talker replacement stops before the new Join.
An identical receive retry delivers the old Leave before the new Join.
Later attributes wait after a reservation failure.
The [integration contract](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md#transmit-and-retry) explains these paths and their dispatch requirements.

Five [named regressions](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) cover Flush retry, ordered replacement, receive stopping, policy masks, and allocation-free operation without policy.
Flush tests sweep all three reservations from IN and LV, including repeated exhaustion.
Replacement tests sweep all nine allocations in both directions.
Each regression has a matching [reversal](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py).

Validation:

- [Unit runner](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/main.c): eight suites and 75 tests per profile; 4745 default assertions and 4733 enabled assertions; rc 0.
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 target per profile; rc 0.
- [behave](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, ten steps per profile; rc 0.
- All 80 [reversals](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) detected per profile; restored builds and checks pass; rc 0.
- Both reviewers' required probes pass in both profiles. All three reported surviving plants now fail their named tests.
- The external allocation sweep passes 2289 checks per profile; the Flush probe passes 532; rc 0 and zero live allocations.
- Instrumented suites pass with address, undefined-behavior, and leak checks; rc 0.
- [Embedded](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_embedded.py) and [freestanding](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_freestanding.py) checks pass in both profiles; rc 0.
- All 27 [published commands](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md) return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md): 941 sentence fragments; zero long sentences; zero unlinked references; 79 self-tests pass.
- All 352 local links and 20 external URLs pass. Repository links use authenticated access.
- All 27 graphs render; maximum 12 nodes. The new retry diagram passes visual inspection.
- All 43 source anchors were checked. All 60 tracked files carry the licence identifier.

The reviewer classified one surviving rollback plant as equivalent in the [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034569438).
Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains explicit.
Review roles: integration author, internal reviewer, and external reviewer.

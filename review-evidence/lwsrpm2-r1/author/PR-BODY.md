[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support through the required merge.
The [integration assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the scope.
The licence, required test dependencies, empty-suite guard, and scenario bindings remain coherent.
The stack validates complete payloads before indications.
It supports Domain values, bounded receive interests, fair PDU splitting, and transactional send retry.
Refused output retains exact bytes while Registrar timers continue.
The documentation defines serialized dispatch, buffer ownership, callback restrictions, and timer teardown.

All application destinations have independent regressions.
Received LeaveAll is isolated by type and ingress port.
The implementation matches [IEEE 802.1Q-2018, clause 10.7.5.20](https://standards.ieee.org/ieee/802.1Q/6844/).
Both former deviation notes are removed.

## Round 2

The [round-2 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032515334) adds an opt-in application setting for immediate received withdrawal.
[MSRP builds](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/CMakeLists.txt) enable it through [LWSRP_MILAN](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/include/shish_lan/msrp.h), which defaults off.
Custom applications select [milan_rapid_leave](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/include/shish_lan/mrp.h) before creation.
With that option, received Leave in IN issues a Leave indication and enters MT immediately.
A received Leave in LV preserves its original deadline.
Default MSRP, VLAN, and MAC timing remains unchanged.
Rebuild the library and consumers because the public operations structure grew.

This implements [Milan v1.2, clause 4.2.7.2.2](https://milanav.com/milan-faqs/).
The specification link opens the publisher's access guidance.
The comparison uses consolidated revision 1.2 and [IEEE 802.1Q-2018, Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
The option does not imply complete Milan conformance.

Validation:

- [Unit tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/main.c): 45 tests; 2659 default assertions or 2647 enabled assertions; both configurations return 0.
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 passes in both profiles; rc 0.
- [behave](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, and ten steps pass in both profiles; rc 0.
- [Profile tests](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/milan_test.c) cover both Talker types, Listener indications, repeated withdrawals, unchanged VLAN/MAC timing, and the original LV deadline.
- [Planted reversals](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/check_reversals.py): all 39 detected; restored build and tests pass; rc 0.
- Delaying withdrawal fails both immediate-indication tests. Restarting LeaveTime fails the separate deadline test. Each leaves the other's tests passing.
- [Sanitizers](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html): enabled profile passes all 45 tests with leak detection; rc 0.
- [Freestanding checks](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/check_freestanding.py): six sources pass in each profile; all compiler commands return 0.
- Isolated codec suite: nine tests and 1690 assertions; rc 0.
- All 25 published commands return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/doc/tools/README.md): 860 sentence fragments; none over 25 words; zero unlinked references; 79 reference self-tests pass.
- All 331 local links and 19 external URLs pass. Repository URL checks use authenticated access.
- All 25 graphs render; maximum 11 nodes; rc 0. Both new graphs pass native and page-width visual review.
- All 55 repository files carry the [SPDX](https://spdx.dev/) identifier. No generated assets or private paths are included.

The four reader guides follow the [documentation rules](https://github.com/kebag-logic/lwSRP/issues/1).
All 43 source anchors were reviewed against their targets.
[Scenario coverage limitations](https://github.com/kebag-logic/lwSRP/issues/4) remain explicit.
Target execution and network interoperability remain unverified.

Review roles: integration author, internal reviewer, and external reviewer.

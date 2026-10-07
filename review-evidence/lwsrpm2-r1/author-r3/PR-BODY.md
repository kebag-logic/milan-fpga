[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support while preserving the test harness, licence, and four reader guides.
The [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the merge scope.
The library supports transactional output, Domain values, bounded receive interests, fair splitting, and serialized integration.
Destination and LeaveAll isolation regressions cover every supported application.

## Round 2

The [profile assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032515334) adds optional immediate received MSRP withdrawal.
The [build option](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/CMakeLists.txt) defaults off.
With it enabled, received Leave in IN indicates withdrawal and enters MT immediately.
LV keeps its original deadline; VLAN and MAC timing remains unchanged.
This implements [Milan v1.2, clause 4.2.7.2.2](https://milanav.com/milan-faqs/).
The specification link provides publisher access guidance.

## Round 3

The [Round 3 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033222017) accepts the [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319) and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033216570).
All findings and suggestions are addressed.

The [parser](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_pdu.c) rejects decoded range errors and vector overflow before any indication.
Higher versions skip unknown message types and event vectors while preserving supported following declarations.
Current-version rejection stays strict.
The [embedded source list](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/CMakeLists.txt) includes switch dispatch.
The [propagation queue](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/src/core/mrp_mad.c) owns value copies and replays retained-port operations in order after output acceptance.

Registrar recovery from LV now stops aging without duplicate Join or propagation callbacks.
This matches [IEEE 802.1Q-2018, Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
The [developer guide](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/developer.md) cites the Domain increment authority separately.
Changed guards follow the [contribution rules](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/CONTRIBUTING.md).

Validation:

- [Unit suites](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/unit/main.c): 60 tests; 3896 default assertions or 3884 enabled assertions; rc 0.
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 target in both profiles; rc 0.
- [behave](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, ten steps in both profiles; rc 0.
- [Reversals](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/check_reversals.py): all 60 detected in each profile; restored builds and tests pass; rc 0.
- [Boundary regressions](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/unit/review_test.c) pin invalid values, extension handling, retained propagation, recovery, LeaveAll behavior, and leaving-state preservation.
- [Profile regressions](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/unit/milan_test.c) also pin Re-declare and transmitted LeaveAll deadlines.
- [Embedded source-list probe](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/check_embedded.py): both profiles link and execute switch dispatch; rc 0.
- [Freestanding checks](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/check_freestanding.py): seven sources per profile; all compiler invocations return 0.
- Enabled [sanitizer checks](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html), including leak detection, pass all 60 tests; rc 0.
- Independent reviewer receive and propagation probes pass in both profiles; rc 0.
- All 27 published commands return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/tools/README.md): 904 sentence fragments; none over 25 words; zero unlinked references; 79 self-tests pass.
- All 345 local links and 19 external URLs pass. Repository links use authenticated access.
- All 26 graphs render; maximum 11 nodes; visual inspection passes; rc 0.
- All 43 source anchors were reviewed. All 58 repository files carry the licence identifier.

The [retention contract](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/doc/integrator.md) states queue lifetime, ordering, and allocation requirements.
Target execution and network interoperability remain unverified.
The [scenario coverage limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains explicit.
Review roles: integration author, internal reviewer, and external reviewer.

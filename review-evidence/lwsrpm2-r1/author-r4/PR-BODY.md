[A563]

[Closes #10](https://github.com/kebag-logic/lwSRP/issues/10).
[Closes #6](https://github.com/kebag-logic/lwSRP/issues/6).
[Closes #7](https://github.com/kebag-logic/lwSRP/issues/7).
[Closes #11](https://github.com/kebag-logic/lwSRP/issues/11).

Integrates bare-metal and end-station support while preserving the harness, licence, and four reader guides.
The [original assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634) defines the merge scope.
The library supports transactional output, Domain values, bounded receive interests, fair splitting, and serialized integration.
Destination and LeaveAll isolation tests cover every supported application.

## Round 2

The [profile assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032515334) adds optional immediate received stream withdrawal.
The [build option](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/CMakeLists.txt) defaults off.
When enabled, received Leave in IN indicates withdrawal and enters MT immediately.
LV keeps its original deadline; VLAN and MAC timing remains unchanged.
This implements [Milan v1.2, clause 4.2.7.2.2](https://milanav.com/milan-faqs/).

## Round 3

The [earlier assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033222017) adds atomic range validation, overflow checks, embedded switch dispatch, and deferred propagation.
Unchanged LV Join recovery stops aging without another indication, matching [IEEE 802.1Q-2018, Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
The [propagation queues](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_mad.c) own copied values and preserve event order after retained output commits.

## Round 4

The [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033982129) accepts the [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033931109) and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033978356).
All findings and wording residues are addressed.

Changed Listener and Talker values in LV now indicate and propagate after received or transmitted LeaveAll.
Unchanged values retain normal recovery behavior.
The [parser](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/src/core/mrp_pdu.c) skips unknown later-version stream messages by their advertised list length.
VLAN and MAC retain vector traversal through the EndMark.
Current-version rejection stays strict.
These boundaries follow [IEEE 802.1Q-2018, clauses 10.8.3.5 and 35.2.2.6](https://standards.ieee.org/ieee/802.1Q/6844/).

Propagation reserves memory before notifying the host and evaluates policy afterwards.
Failed reservation preserves the source value and state for an identical receive retry.
Timer withdrawal retries on the next tick.
Failed destination allocation retains queued work for later polls.
The [integration contract](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/integrator.md#transmit-and-retry) documents ordering, lifetime, and capacity for up to 32 temporary target entries.
The [fault allocation port](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/fault_alloc.c) makes exhaustion and teardown checks reproducible.

Validation:

- [Unit runner](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/main.c): eight suites, 70 tests, 4215 default assertions or 4203 enabled assertions; rc 0.
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html): 1/1 target in both profiles; rc 0.
- [behave](https://behave.readthedocs.io/en/stable/): one feature, three scenarios, ten steps in both profiles; rc 0.
- [Reversals](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py): all 75 detected in each profile; restored checks pass; rc 0.
- [Boundary regressions](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) pin changed values, allocation rollback, callback order, error reporting, retry, and teardown.
- Both reviewers' receive, allocation, and ordering probes pass in both profiles with [instrumentation](https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html); rc 0.
- Instrumented unit suites pass in both profiles, including leak checks; rc 0.
- [Embedded](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_embedded.py) and [freestanding](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_freestanding.py) checks pass in both profiles; rc 0.
- All 27 published commands return 0.
- [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/tools/README.md): 925 sentence fragments; zero over 25 words; zero unlinked references; 79 self-tests pass.
- All 347 local links and 20 external URLs pass. Repository links use authenticated access.
- All 26 graphs render; maximum 12 nodes; changed diagrams pass visual inspection.
- All 43 source anchors were checked. All 60 repository files carry the licence identifier.

Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains explicit.
Review roles: integration author, internal reviewer, and external reviewer.

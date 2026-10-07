[A560]

# Local dependency stack

Relates to #665. All branches are local; publication and upstream reviews are owed.
Final parent pin: `ef8a28b9f991ad2f6a466b377c25c2f7bcb310da` on `zephyr-api-docs`.
The branches form one ancestry stack; publish prerequisites before dependent heads.

| Branch | Commit | Unit tests | Assertions | Behavior suite |
|---|---|---:|---:|---|
| `apache-2.0` | `fed1a0d0a08e1f9682ce1fca3bb4b9985d846e5b` | 9 | 1690 | Baseline setup failure; fixed by `test-entrypoints` |
| test-entrypoints | 58ed80ee13d6bc708d0017e8ec87a19b11b267b0 | 9 | 1690 | 3 scenarios / 10 steps |
| timer-lifetime | 9c7ee482888c57dd95599233756337f90303c935 | 11 | 1704 | 3 scenarios / 10 steps |
| msrp-wire-values | d8d10b58fb513465cc746bd07307f84d35a7c1c9 | 12 | 1725 | 3 scenarios / 10 steps |
| mrp-receive-validation | 7e81da9c6ad03090f380e17fbf84b3cb5016434a | 13 | 1777 | 3 scenarios / 10 steps |
| mrp-transmit | 33651955c213d0d6e03155e718e9e64508850f78 | 15 | 1803 | 3 scenarios / 10 steps |
| freestanding-headers | d11a55281d6aaae42e3995821e85b0c073decac8 | 15 | 1803 | 3 scenarios / 10 steps |
| mrp-transmit-retry | 5724550c0f96c65c4cd5e5d42f699a67fb14d2f0 | 16 | 1818 | 3 scenarios / 10 steps |
| mrp-registration-updates | 7d72af7a6c8cf0c35472de415d5b3a096897f5e0 | 17 | 1829 | 3 scenarios / 10 steps |
| parser-vector-reads | c09d91299f65575835b78b7e1653cd981d35b0a1 | 17 | 1829 | 3 scenarios / 10 steps |
| mrp-transmit-opportunities | 96b323fa43f98b0d8329212d81335982873ec67a | 18 | 1837 | 3 scenarios / 10 steps |
| mrp-bounded-storage | bb35392c2c75f0a8e874dd1a5bd816cd9eef6c92 | 19 | 1845 | 3 scenarios / 10 steps |
| mrp-pdu-segmentation | 4d09ed27f57958eb9e2625ae18200593308b79f7 | 20 | 1895 | 3 scenarios / 10 steps |
| mrp-withdrawal-value | f8fb5528eff0a1f1519b4e896bbd0f235762815b | 21 | 1900 | 3 scenarios / 10 steps |
| msrp-context-compatibility | 4c6a0fe3ca5ab02de804d99408ba957dd673ee9b | 22 | 1902 | 3 scenarios / 10 steps |
| msrp-talker-replacement | 8e6ecc885495c0cf3b13689ad5203091a9c52d30 | 23 | 1909 | 3 scenarios / 10 steps |
| bare-metal-api-docs | f5e244eb2f5bbe8f207ac6e5770ba45fcfd6d156 | 23 | 1909 | 3 scenarios / 10 steps |
| msrp-listener-new | a832b2813671037a2027a683a110767aa07995ae | 24 | 1914 | 3 scenarios / 10 steps |
| zephyr-api-docs | ef8a28b9f991ad2f6a466b377c25c2f7bcb310da | 24 | 1914 | 3 scenarios / 10 steps |

Part A adds the full official Apache-2.0 licence, NOTICE, SPDX labels and the company-contribution statement. The ownership decision is in the assignment. No conflicting copyright/licence notice was found. The original queue credits an algorithm; it carries no separate code licence.

Every Part B row was rebuilt at that exact local branch head with CMake, CTest and behave. All four commands returned zero. The final row only updates Zephyr help; the compiled source tree equals its predecessor.

## Upstream file map

Paths in this table are relative to the separate lwSRP clone at the final pin. Every changed source, header, test and build entry also carries its Apache-2.0 identifier.

| File:line | Change |
|---|---|
| `CMakeLists.txt:35` | Build exported entry points and the added cgreen regression suites. |
| `Kconfig.zephyr:6` | Describe the actual centisecond timer and asynchronous transmit integration. |
| `LICENSE:1` | Full Apache-2.0 licence text. |
| `NOTICE:1` | Required project notice. |
| `README.md:61` | Document contributions, bounded storage, timer/TX ownership and bare-metal integration. |
| `behave.ini:1` | Add the Apache-2.0 SPDX identifier. |
| `build.sh:2` | Add the Apache-2.0 SPDX identifier. |
| `src/core/mrp_mad.c:13` | Bound registration storage; manage timers and state; validate receive before mutation; retain transactional output and segment PDUs. |
| `src/core/mrp_pdu.c:13` | Correct wire parsing, vector bounds, lengths and checked encoding. |
| `src/core/switch.c:1` | Export switch entry points for the existing behavior harness. |
| `src/core/switch_ctrl.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/error.h:1` | Provide stable freestanding API error values without hosted errno state. |
| `src/include/shish_lan/mmrp.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/mrp.h:231` | Expose bounded port configuration, receive filtering, visitation, reclaim and committed TX hooks. |
| `src/include/shish_lan/mrp_pdu.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/msrp.h:33` | Expose context compatibility, Talker registration replacement and Listener subtype updates. |
| `src/include/shish_lan/mvrp.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/include/shish_lan/switch.h:27` | Declare exported switch entry points. |
| `src/include/shish_lan/switch_ctrl.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/modules/mmrp.c:10` | Use freestanding error values and remove hosted allocation headers. |
| `src/modules/msrp.c:22` | Correct wire values, registration updates, Talker replacement and Listener New redeclaration. |
| `src/modules/mvrp.c:9` | Use freestanding error values and remove hosted allocation headers. |
| `src/modules/sim_adapter.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/modules/sim_adapter.h:1` | Add the Apache-2.0 SPDX identifier. |
| `src/ports/alloc.c:1` | Add the Apache-2.0 SPDX identifier. |
| `src/ports/alloc.h:5` | Use the freestanding size declaration. |
| `src/ports/timer.c:36` | Unlink destroyed timers and prevent stale or duplicate timer ownership. |
| `src/ports/timer.h:42` | Declare timer finalization. |
| `tests/features/environment.py:9` | Load the explicitly built shared library for each branch gate. |
| `tests/features/steps/switch_steps.py:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/features/switch.feature:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/unit/mrp_pdu_test.c:1` | Add the Apache-2.0 SPDX identifier. |
| `tests/unit/msrp_values_test.c:1` | Check independent MSRP wire values and context compatibility. |
| `tests/unit/placeholder.c:13` | Register all new cgreen suites. |
| `tests/unit/receive_test.c:1` | Check malformed input, registration replacement, resource limits and subtype changes. |
| `tests/unit/timer_test.c:1` | Check destruction, callback order and timer lifetime. |
| `tests/unit/transmit_test.c:1` | Check refusal retry, opportunities, segmented output and retained withdrawal values. |
| `zephyr/module.yml:1` | Add the Apache-2.0 SPDX identifier. |


## Upstream test sensitivity

The fifteen added cgreen cases each reject a separately planted source defect at the final upstream pin. Every faulty source compiled, every run returned 1 and named the intended failed test; sources were restored after each plant. The restored suite returns 0 (24 cases, 1,914 assertions). The existing nine cases and three behavior scenarios also pass at every Part B branch head.

| Test and source | Planted defect | Observed result |
|---|---|---|
| `tests/unit/timer_test.c:15` `remove_head_middle_tail_and_reinitialize` | Fire expiry during removal instead of cancelling silently. | 1; named test fails |
| `tests/unit/timer_test.c:38` `destroy_with_live_attribute_timers_then_tick` | Leave a freed port LeaveAll timer linked. | 1; named test fails |
| `tests/unit/msrp_values_test.c:8` `domain_and_vector_offsets_match_wire_fields` | Drop the Domain class vector offset. | 1; named test fails |
| `tests/unit/msrp_values_test.c:44` `domain_callback_preserves_existing_member_order` | Insert a field before the existing first callback. | 1; named test fails |
| `tests/unit/receive_test.c:18` `truncation_respects_complete_vectors_and_pdu_end` | Deliver receive callbacks before whole-PDU validation. | 1; named test fails |
| `tests/unit/receive_test.c:57` `changed_registered_listener_notifies_without_duplicate_join` | Suppress changed Listener notification while already registered. | 1; named test fails |
| `tests/unit/receive_test.c:83` `uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | Ignore the receive-interest filter and allocate uninteresting streams. | 1; named test fails |
| `tests/unit/receive_test.c:108` `withdrawal_does_not_replace_the_registered_declaration` | Overwrite the registered value with a withdrawal subtype. | 1; named test fails |
| `tests/unit/receive_test.c:129` `talker_join_replaces_the_other_type_on_the_same_port` | Skip same-port replacement of the opposite Talker attribute type. | 1; named test fails |
| `tests/unit/transmit_test.c:39` `fresh_ladder_and_refusal_are_transactional` | Encode New as JoinMt. | 1; named test fails |
| `tests/unit/transmit_test.c:66` `leaveall_then_withdrawal_retains_until_leave_expiry` | Halve the configured LeaveTime. | 1; named test fails |
| `tests/unit/transmit_test.c:83` `refused_pdu_survives_timers_without_aging_unsent_leaveall` | Discard owed TX when a new receive arrives. | 1; named test fails |
| `tests/unit/transmit_test.c:112` `receive_redeclare_requests_transmission_without_periodic_wait` | Clear the requested Applicant transmit opportunity. | 1; named test fails |
| `tests/unit/transmit_test.c:143` `a_full_pdu_retries_omitted_attributes_before_repeats` | Always visit normal order instead of deferred attributes first. | 1; named test fails |
| `tests/unit/transmit_test.c:163` `changed_listener_redeclares_from_a_quiet_applicant` | Use Join for a changed Listener instead of New. | 1; named test fails |


# Integration handoff

Status: Round 4 REVIEW READY. Local head 82422d6ffe38d430576cd9d874a45b9e124e6c63; clean tree; one commit ahead; unpushed.
Starting head: a9cd5ef58a2478cb2ce4899b31aa02d5c2072646, already published by the manager.
The sections before Round 2 retain the previous merge evidence.

## Baseline and scope

- Branch: mark2-port, initially clean.
- Origin: https://github.com/kebag-logic/lwSRP.git, verified; rc 0.
- Starting HEAD: 1a1d6cbe4f971d2d346b948dd2e9716421f211e9, verified; rc 0.
- Merge parent: ef8a28b9f991ad2f6a466b377c25c2f7bcb310da, verified; rc 0.
- Read the exact [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634).
- Read the bodies and all comments for [issue 10](https://github.com/kebag-logic/lwSRP/issues/10), [issue 1](https://github.com/kebag-logic/lwSRP/issues/1), [issue 6](https://github.com/kebag-logic/lwSRP/issues/6), and [issue 7](https://github.com/kebag-logic/lwSRP/issues/7).
- [TAKEN](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032201369) posted; rc 0.
- Protocol behavior is the incoming stack. Integration changes cover harness composition, regression tests, documentation, and licence identifiers.
- No push, PR creation/edit, comment modification/deletion, rebase, amend, or delegation occurred.

## Conflicts and resolutions

- CMakeLists.txt: retain the required dependency lookup and empty-suite rejection from the base; add all four incoming suites and the internal include path. This preserves the harness protection and new coverage.
- tests/unit/placeholder.c (modify/delete): retain the deletion. Register the incoming suites in tests/unit/main.c, preserving its reporter and suite cleanup. One executable has one entry point.
- README.md: retain the owner-approved four-reader structure and exact licence paragraph. Move incoming integration details into the relevant guides and update the quick start after testing.
- Nonconflicting overlap: retain the exported switch operations and existing scenario bindings. Update stale inline-wrapper comments. Retain SHLAN_LIBRARY for external builds.
- Licence commit fed1a0d is common history; no duplicate licence application is needed.
- Merge invocation rc 1 reports these expected conflicts; all conflicts resolved in the final merge commit.


## Licence

Every current repository file has SPDX-License-Identifier: Apache-2.0.
The first audit found missing identifiers in LICENSE and NOTICE (rc 1).
Added metadata lines to both files without changing their terms or notice text.
The final audit inspected 54 files and found no missing identifier, private residue, generated asset, conflict marker, or file over 200 KB (rc 0).
The duplicate licence commit is already an ancestor of the starting base (rc 0).

## Validation totals

- Initial merge: ctest 1/1; 24 unit tests; 1914 assertions; rc 0.
- Final published ctest: 1/1; 37 unit tests; 2278 assertions; rc 0.
- Suite assertions: codec 1690; timers 14; stream values 23; receive 83; transmit 104; integration 364.
- Final published behave: one feature, three scenarios, ten steps; rc 0.
- Dry run: three scenarios and ten steps untested by design; rc 0.
- Isolated codec executable: nine tests, 1690 assertions; rc 0.
- Address/undefined-behavior sanitizers with leak detection: ctest 1/1, 37 tests, 2278 assertions; rc 0.
- Strict freestanding source checks: six sources, twelve compiler commands; each rc 0.
- Optimized bounded-header compilation with warnings as errors: rc 0.
- Planted reversals: 35 detected; final restored build and ctest rc 0.
- Published commands: all 19 executed individually; each rc 0. No check was piped.
- Final whitespace check: rc 0.

## Behavioural fixes, tests, and planted reversals

The committed reversal runner changes one scratch copy at a time.
The original checkout is never mutated by that runner.
All 32 behavioral/layout mutation builds returned 0 and each failing ctest returned 8.
The two hosted-header checks and the optimized initialization check returned 1 as expected.
The baseline and restored configure/build/test checks returned 0.
Each row names the failing assertion or dedicated check observed in the final run.

| Fix / reversal label | Planted change | Check that failed | rc |
| --- | --- | --- | --- |
| timer-unlink | `    if (t->cs && t->link && t->link->cs) { return; }     struct shlan_timer **at = &g_head;` | `timer_suite -> remove_head_middle_tail_and_reinitialize` | 8 |
| msrp-address | `{ 0x91u, 0xE0u, 0xF0u, 0x00u, 0x0Eu, 0x80u }` | `integration_suite -> every_application_uses_its_standard_destination`; `msrp_values_suite -> domain_and_vector_offsets_match_wire_fields` | 8 |
| mmrp-address | `0x00u, 0x21u` | `integration_suite -> every_application_uses_its_standard_destination` | 8 |
| mvrp-address | `0x00u, 0x20u` | `integration_suite -> every_application_uses_its_standard_destination` | 8 |
| domain-offset | `d->class_id = buf[0];` | `msrp_values_suite -> domain_and_vector_offsets_match_wire_fields` | 8 |
| talker-offset | `increment_stream(t->stream_id.bytes + 6, 2, 0);` | `msrp_values_suite -> domain_and_vector_offsets_match_wire_fields` | 8 |
| listener-offset | `increment_stream((uint8_t *)attr_val_out + 6, 2, 0);` | `msrp_values_suite -> domain_and_vector_offsets_match_wire_fields` | 8 |
| wire-prevalidation | `int r = 0;` | `integration_suite -> a_malformed_later_message_has_no_earlier_indications`; `receive_suite -> truncation_respects_complete_vectors_and_pdu_end` | 8 |
| pdu-endmark | `if (false && vector_seen && off == len)` | `receive_suite -> truncation_respects_complete_vectors_and_pdu_end` | 8 |
| leaveall-scope | `if (a->attr_type == attr_type \|\| a->attr_type != attr_type)` | `integration_suite -> mmrp_leaveall_changes_only_the_message_type_and_port`; `integration_suite -> msrp_leaveall_changes_only_the_message_type_and_port` | 8 |
| local-registration | `if (ev == MRP_EVENT_NEW) { ev = MRP_EVENT_RNEW; }     const struct reg_entry *e = &reg_table[ev][ai->reg];` | `transmit_suite -> fresh_ladder_and_refusal_are_transactional`; `transmit_suite -> refused_pdu_survives_timers_without_aging_unsent_leaveall` | 8 |
| registrar-condition | `false && ai->reg != MRP_REG_STATE_IN)` | `transmit_suite -> fresh_ladder_and_refusal_are_transactional` | 8 |
| periodic-interval | `&ps->pt_timer, 20u` | `integration_suite -> periodic_is_one_second_independent_of_join_time`; `transmit_suite -> receive_redeclare_requests_transmission_without_periodic_wait` | 8 |
| leaveall-randomization | `return ps->leaveall_cs;` | `integration_suite -> leaveall_draws_are_inside_the_required_interval` | 8 |
| refused-storage | `if (r != 0) {         ps->prepared_pdu = NULL;         return r;` | `transmit_suite -> refused_pdu_survives_timers_without_aging_unsent_leaveall` | 8 |
| registrar-during-refusal | `struct mrp_attr_timer_arg *a = (struct mrp_attr_timer_arg *)arg;     if (priv_of(a->app)->ports[a->port_id].prepared_pdu) { return; }` | `integration_suite -> registrar_ages_while_a_transmission_is_retained` | 8 |
| changed-listener-indication | `if (false && changed_in && (ev == MRP_EVENT_RJOININ` | `receive_suite -> changed_registered_listener_notifies_without_duplicate_join` | 8 |
| receive-opportunity | `// Reversal: omit receive-driven requests.     switch (MRP_APPL_STATE_QA)` | `transmit_suite -> receive_redeclare_requests_transmission_without_periodic_wait` | 8 |
| receive-interest | `if (false && priv->filter && !priv->filter(` | `receive_suite -> uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | 8 |
| reclaim | `if (false && a->reg == MRP_REG_STATE_MT &&` | `receive_suite -> uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | 8 |
| split-fairness | `a->tx_deferred != (priority != 0)` | `transmit_suite -> a_full_pdu_retries_omitted_attributes_before_repeats` | 8 |
| received-withdrawal-value | `previous && !declares && false ? previous :` | `receive_suite -> withdrawal_does_not_replace_the_registered_declaration` | 8 |
| local-withdrawal-value | `*ai   = get_or_create_attr(app, ps, port_id, attr_type, attr_val);` | `integration_suite -> local_withdrawal_keeps_the_registered_listener_value` | 8 |
| talker-replacement | `rc->app->ops->attr_replaces && false) {` | `receive_suite -> talker_join_replaces_the_other_type_on_the_same_port` | 8 |
| listener-redeclaration | `MSRP_ATTR_TYPE_LISTENER, val, false);` | `transmit_suite -> changed_listener_redeclares_from_a_quiet_applicant` | 8 |
| domain-member-order | `struct msrp_ctx {     void (*inserted_before_existing_members)(void);` | `msrp_values_suite -> domain_callback_preserves_existing_member_order` | 8 |
| hosted-allocation-header | `#include <stddef.h> #include <stdlib.h>` | `hosted header dependency check` | 1 |
| hosted-error-header | `#include "shish_lan/error.h" #include <errno.h>` | `hosted header dependency check` | 1 |
| point-to-point-condition | `if ((false && p2p && ev == MRP_EVENT_RJOININ &&` | `integration_suite -> applicant_receive_conditions_follow_link_mode` | 8 |
| shared-in-condition | `(false && !p2p && ev == MRP_EVENT_RIN)` | `integration_suite -> applicant_receive_conditions_follow_link_mode` | 8 |
| withdrawal-transition | `_S(TX_MSG_LEAVE, MRP_APPL_STATE_LO), _X, _X,` | `integration_suite -> applicant_declaration_recovery_and_withdrawal_follow_the_table` | 8 |
| periodic-passive | `_X, _X, _X,     },     /* LEAVETIMER:` | `integration_suite -> applicant_declaration_recovery_and_withdrawal_follow_the_table` | 8 |
| leaveall-all-types | `for (unsigned type = 1; type < last; ++type)` | `integration_suite -> transmitted_leaveall_includes_every_supported_type` | 8 |
| unknown-stream-message | `if (false && !expected && msrp)` | `integration_suite -> later_versions_skip_unknown_stream_messages` | 8 |
| bounded-header-initialization | `uint16_t vh;` | `optimized compilation: maybe-uninitialized` | 1 |

Additional assertions cover Domain callback delivery and timer destruction/recreation.
The imported registered-value tests cover LeaveAll aging without restarting an existing Leave timer.
The state-path tests cover local Join/New, withdrawal, recovery, periodic passive states, and link conditions.
The source list preserves every incoming protocol file and every incoming suite.
No new protocol defect was patched outside the incoming stack.

The first exploratory timer reversal could loop and required its test processes to be stopped.
That exploratory result is not relied upon for delivery.
The final mutation retains an armed linked timer and produces two explicit assertion failures without a stall.
The runner also gives each ctest target a ten-second timeout.

## Published commands

Environment: LWSRP_BUILD is an external build directory; CGREEN_PREFIX and CMAKE_PREFIX_PATH select the supplied dependency installation.
LD_LIBRARY_PATH selects its library directory; CPATH and LIBRARY_PATH support the isolated compiler command.
REVERSAL_SCRATCH is a fresh external directory; DOC_SCRATCH contains rendered graphs.
PYTHONDONTWRITEBYTECODE prevents generated caches in the checkout.
The same Linux host commands were run from the repository root.

| Page and line | Exact command or block | rc |
| --- | --- | --- |
| README.md:39 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug` | 0 |
| README.md:40 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| README.md:41 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| README.md:42 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:18 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug` | 0 |
| doc/tester.md:19 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| doc/tester.md:20 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| doc/tester.md:21 | `"$LWSRP_BUILD/unit_tests"` | 0 |
| doc/tester.md:22 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:23 | `behave --dry-run` | 0 |
| doc/tester.md:48 | `cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$LWSRP_BUILD/mrp_pdu_tests" <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` | 0 |
| doc/tester.md:56 | `"$LWSRP_BUILD/mrp_pdu_tests"` | 0 |
| doc/tester.md:133 | `python3 tests/check_freestanding.py` | 0 |
| doc/tester.md:134 | `python3 tests/check_reversals.py --work-dir "$REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX"` | 0 |
| doc/tools/README.md:14 | `python3 doc/tools/check_sentences.py` | 0 |
| doc/tools/README.md:15 | `python3 doc/tools/check_references.py` | 0 |
| doc/tools/README.md:16 | `python3 doc/tools/check_references.py --self-test` | 0 |
| doc/tools/README.md:17 | `python3 doc/tools/check_links.py --github-auth` | 0 |
| doc/tools/README.md:18 | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | 0 |

The heredoc compiler invocation is one command, including its complete embedded source.
The contribution C example and scenario example are syntax examples, not shell commands.
The scenario example is also exercised by the existing scenario suite.

## Documentation changes and checks

| Page | Change | Final check results |
| --- | --- | --- |
| README.md | Current scope, external build commands, suite counts, four reader links. | Sentences 0; references 0; links 0; graph 0. |
| doc/architecture.md | Atomic receive validation, interest filtering, allocation, transactional output, retry and splitting. | Sentences 0; references 0; links 0; all three graphs 0. |
| doc/developer.md | Current tables, storage, timers, Domain, offsets, interests, replacement and remaining deviations. | Sentences 0; references 0; links 0; all eight graphs 0. |
| doc/integrator.md | Port configuration, receive, persistent output buffers, deferred input, timer teardown, serialization, bare-metal source list. | Sentences 0; references 0; links 0; all seven graphs 0. |
| doc/manager.md | Clause matrix, implemented scope, remaining gaps, test counts, issue status. | Sentences 0; references 0; links 0; graph 0. |
| doc/tester.md | Six suites, external build, regressions, reversals, strict headers, explicit scenario limits. | Sentences 0; references 0; links 0; both graphs 0. |
| doc/tools/README.md | Licence links now resolve in the combined tree. | Sentences 0; references 0; links 0. |
| Public headers and stream destination comment | Domain type, bounded PDU contract, exact address clause and table. | Compiler and whitespace checks 0; source review complete. |
| LICENSE and NOTICE | Add required identifiers. | SPDX audit 0. |

Global results: 795 sentences/fragments, zero over 25 words, zero prose exemptions.
The reference check reports zero bare references; its self-test passes 79 cases.
There are 309 local links and 17 external URLs; all checks pass.
Repository links were checked with authenticated access; other external URLs used anonymous requests.
All 42 source-line references were printed and reviewed against their target definitions or rows.
The obsolete line ranges were replaced with current function/table anchors.

The inherited ISO catalogue URL returned HTTP 403 in all tried official variants.
The final pages link the committee's public C11 draft, which returns HTTP 200.
This keeps the language reference public and explicit about draft status.
The initial transmit sequence used a reserved participant identifier; rendering failed with rc 1.
Renaming it resolved the error. Shortened sequence labels improved page-width readability.
All final documentation checks return 0; no broken link is exempted.

## Graph review

All 23 graphs rendered in scratch; every render returned 0.
Maximum size: 11 nodes. No rendered asset was copied into the repository or output directory.
Reviewed the rasterized graphs for clipping, label overlap, and edges crossing nodes.
The sequence graphs were also inspected at 80% scale for page-width readability.
Other graphs fit within 800 pixels at native size.
Sequence arrows crossing participant lifelines are intentional; no arrow crosses a participant box.

| Graph | Nodes | Render rc | Visual result |
| --- | --- | --- | --- |
| CONTRIBUTING.md:48 | 5 | 0 | Clear labels; no clipping or node crossing. |
| README.md:15 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/architecture.md:10 | 11 | 0 | Clear labels; no clipping or node crossing. |
| doc/architecture.md:35 | 10 | 0 | Clear labels; no clipping or node crossing. |
| doc/architecture.md:60 | 8 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:29 | 10 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:81 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:114 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:143 | 7 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:170 | 3 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:205 | 2 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:232 | 2 | 0 | Clear labels; no clipping or node crossing. |
| doc/developer.md:275 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:49 | 4 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:89 | 4 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:137 | 3 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:185 | 3 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:218 | 3 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:248 | 2 | 0 | Clear labels; no clipping or node crossing. |
| doc/integrator.md:279 | 4 | 0 | Clear labels; no clipping or node crossing. |
| doc/manager.md:45 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/tester.md:65 | 6 | 0 | Clear labels; no clipping or node crossing. |
| doc/tester.md:95 | 9 | 0 | Clear labels; no clipping or node crossing. |

The six state graphs were compared with the local IEEE 802.1Q-2018 tables 10-3 through 10-6.
Their displayed transitions match the selected standard paths.
The guides distinguish selected graphs from exhaustive conformance evidence.
The Registrar extra Join indication and periodic-disable timer action remain documented.
The standard was converted only in scratch; no standard copy or extended quotation enters the deliverables.

## Issue status and remaining limits

- Issue 6: fixed. MSRP uses 01-80-C2-00-00-0E. The exact code comment cites 35.2.2.1 and Table 8-1. Every application's destination is pinned; three planted wrong addresses fail. The deviation notes are removed.
- Issue 7: fixed. The local standard's 10.7.5.20 limits received LeaveAll to the message's Attribute Type and ingress port. The handler follows that rule. The shared participant timer still restarts. Tests cover all four MSRP types and both MMRP types on two ports. Both Applicant and Registrar states of every other type stay unchanged. All-types delivery fails those tests. The deviation notes are removed.
- Both issues remain open remotely until the manager publishes and merges the change; the prepared PR body closes them with issue 10.
- Issue 4 remains open. Existing scenarios do not independently observe port state. A wrongly redirected disable operation remains outside their coverage.
- Additional participant modes, full bridge policy, resource admission, and target/interoperability testing remain outside this integration.
- Changed Listener registrations notify without a separate Leave callback. Opposite Talker Join registrations are replaced. Conflicting New registrations require host precedence policy.

## Delivery

Local merge commit: 12a0b77f4c4853028466f1ce608feb59598bb3a3.
Parents: 1a1d6cbe4f971d2d346b948dd2e9716421f211e9 and ef8a28b9f991ad2f6a466b377c25c2f7bcb310da.
The parent check, one-line subject check, origin check, and clean-tree check returned 0.
The final committed build, ctest, and behave runs returned 0.
Final ctest: 1/1; 37 tests; 2278 assertions. Final behave: 1 feature; 3 scenarios; 10 steps.
Final status payload: [A563] REVIEW READY 12a0b77f4c4853028466f1ce608feb59598bb3a3.
The manager owns push and PR publication. The prepared PR body uses neutral role labels.
[COMMANDS.json](COMMANDS.json) records primary command returns, published commands, mutation command returns, and graph-render commands.
All paths in that record use environment aliases for portability.

Final status comment posted: [[A563] REVIEW READY 12a0b77f4c4853028466f1ce608feb59598bb3a3](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032502747); rc 0.

## Round 2

Status: REVIEW READY. Local head `86a5f74c028dedec2a0f5bc1c5a258bbd83746b9`. Working tree clean. Branch unpushed.
Parent: `12a0b77f4c4853028466f1ce608feb59598bb3a3`.
Origin and branch were confirmed at resume and after commit; all checks returned 0.
The original starting head is retained as the first parent of the prior merge.

Read the exact [round-2 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032515334) and [issue 11](https://github.com/kebag-logic/lwSRP/issues/11).
Re-read the original [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634), [integration issue](https://github.com/kebag-logic/lwSRP/issues/10), and [documentation rules](https://github.com/kebag-logic/lwSRP/issues/1).
Re-read the [destination issue](https://github.com/kebag-logic/lwSRP/issues/6) and [LeaveAll issue](https://github.com/kebag-logic/lwSRP/issues/7), including all comments.
Authenticated issue and comment reads returned 0.
An initial connector read returned HTTP 404; the authenticated command-line reads succeeded.
No TAKEN comment was repeated.

### Changes and conflicts

No new merge or conflict occurred in this round.
The earlier merge resolutions remain unchanged.
The source change is limited to the explicitly authorized profile behavior.

The appended application option is [milan_rapid_leave](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/include/shish_lan/mrp.h).
Zero-initialized operations preserve the default rule.
The [Registrar handler](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/core/mrp_mad.c#L554) changes only received Leave in IN when the option is enabled.
It enters MT and issues the existing Leave indication and propagation action without starting LeaveTime.
The LV state retains its original deadline.
Other Registrar events retain the generic table.
The [MSRP constructor](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/src/modules/msrp.c) selects the option through the default-off build setting.
Both host and embedded module build branches wire the setting.
Direct builds can define the same header setting when compiling the stream application.
Default VLAN and MAC constructors keep generic timing.
The public structure grew; the integration guide requires rebuilding the library and consumers.

The local consolidated specification and local bridge standard were read from scratch text exports.
The comparison uses [Milan v1.2, clause 4.2.7.2.2](https://milanav.com/milan-faqs/) and [IEEE 802.1Q-2018, Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
Only the received-Leave cell for IN changes.
No standard file or long quotation was added to the checkout or output directory.

### Behavioral tests and reversals

The new [profile suite](https://github.com/kebag-logic/lwSRP/blob/86a5f74c028dedec2a0f5bc1c5a258bbd83746b9/tests/unit/milan_test.c) has eight tests.
Literal received payloads exercise Talker Advertise, Talker Failed, and Listener registrations.
The tests require the indication and MT state before receive returns, without a tick.
They check retained Listener values and no duplicate indication after repeated Leave or later ticks.
The LV test receives LeaveAll, waits 200 centiseconds, then receives Leave.
It checks LV at 499 centiseconds and withdrawal at the original 500-centisecond deadline.
Default application timing, constructor selection, VLAN and MAC aging, and local withdrawal are also checked.

| Behavioral contract | Planted reversal | Dedicated failed check | Build rc | Check rc |
| --- | --- | --- | --- | --- |
| Immediate opted-in withdrawal | Disable the profile branch. | talker_leave_in_is_immediate and listener_leave_in_is_immediate. | 0 | 8 |
| Existing LV deadline | Select the timer-starting IN row for an LV received Leave. | leave_in_lv_keeps_the_original_deadline. | 0 | 8 |
| Build-profile selection | Invert the constructor flag. | msrp_constructor_selects_the_build_profile. | 0 | 8 |
| Application opt-in scope | Remove the option condition. | disabled_application_option_preserves_ieee_timing, mvrp_keeps_ieee_leave_timing, and mmrp_keeps_ieee_leave_timing. | 0 | 8 |

The delayed-IN reversal leaves the deadline test passing.
The restarted-LV reversal leaves both immediate tests passing.
The runner enforces these independent failure requirements.
All 39 reversals were detected in the final published run; runner rc 0.
All 36 behavioral/layout mutation builds returned 0; their test runs returned 8.
The two hosted-header checks and optimized initialization check returned 1 as expected.
Baseline and restored configure/build/test checks returned 0.
The source checkout was never mutated by the reversal runner.

### Validation

| Check | Counts | rc |
| --- | --- | --- |
| Default configure and build | Seven suites. | 0 each |
| Default ctest | 1/1; 45 tests; 2659 assertions. | 0 |
| Default unit executable | 45 tests; 2659 assertions. | 0 |
| Enabled configure and build | Seven suites. | 0 each |
| Enabled ctest | 1/1; 45 tests; 2647 assertions. | 0 |
| Enabled unit executable | 45 tests; 2647 assertions. | 0 |
| Default and enabled behave | One feature; three scenarios; ten steps per run. | 0 each |
| Scenario dry run | Three scenarios; ten steps untested by design. | 0 |
| Isolated codec | Nine tests; 1690 assertions. | 0 |
| Address/undefined-behavior sanitizers with leak detection | Enabled build; 1/1; 45 tests; 2647 assertions. | 0 |
| Strict freestanding checks | Six sources and twelve compiler commands per profile. | 0 each |
| Reversal runner | 39 detected; restored build and tests pass. | 0 |
| Whitespace and staged whitespace | No errors. | 0 each |
| Public content and SPDX audit | 55 files; no residue, generated assets, conflict markers, or oversize files. | 0 |
| Committed-state audit | Parent, branch, origin, clean tree, one-line message, and configured identity. | 0 each |

The base six suites retain 2278 assertions.
The new suite contributes 381 default assertions or 369 enabled assertions.
The constructor paths account for the difference.
No test or published command was piped.
Every process ran in the foreground with a timeout; no background work remains.

### Published commands

All 25 published commands were executed individually and returned 0 in the final replay.
Builds, reversal copies, logs, and rendered graphs stayed in scratch.
The environment supplies LWSRP_BUILD, LWSRP_MILAN_BUILD, CGREEN_PREFIX, CMAKE_PREFIX_PATH, LD_LIBRARY_PATH, CPATH, LIBRARY_PATH, REVERSAL_SCRATCH, and DOC_SCRATCH.
No environment values are embedded in public content.

| Page and line | Exact command or block | rc |
| --- | --- | --- |
| README.md:39 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF` | 0 |
| README.md:40 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| README.md:41 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| README.md:42 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:18 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF` | 0 |
| doc/tester.md:19 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| doc/tester.md:20 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| doc/tester.md:21 | `"$LWSRP_BUILD/unit_tests"` | 0 |
| doc/tester.md:22 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:23 | `behave --dry-run` | 0 |
| doc/tester.md:46 | `cmake -S . -B "$LWSRP_MILAN_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=ON` | 0 |
| doc/tester.md:47 | `cmake --build "$LWSRP_MILAN_BUILD" --parallel 2` | 0 |
| doc/tester.md:48 | `ctest --test-dir "$LWSRP_MILAN_BUILD" --output-on-failure` | 0 |
| doc/tester.md:49 | `"$LWSRP_MILAN_BUILD/unit_tests"` | 0 |
| doc/tester.md:50 | `SHLAN_LIBRARY="$LWSRP_MILAN_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:72 | `cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$LWSRP_BUILD/mrp_pdu_tests" <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` | 0 |
| doc/tester.md:80 | `"$LWSRP_BUILD/mrp_pdu_tests"` | 0 |
| doc/tester.md:158 | `python3 tests/check_freestanding.py` | 0 |
| doc/tester.md:159 | `CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py` | 0 |
| doc/tester.md:160 | `python3 tests/check_reversals.py --work-dir "$REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX"` | 0 |
| doc/tools/README.md:14 | `python3 doc/tools/check_sentences.py` | 0 |
| doc/tools/README.md:15 | `python3 doc/tools/check_references.py` | 0 |
| doc/tools/README.md:16 | `python3 doc/tools/check_references.py --self-test` | 0 |
| doc/tools/README.md:17 | `python3 doc/tools/check_links.py --github-auth` | 0 |
| doc/tools/README.md:18 | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | 0 |

### Documentation pages and results

| Page | Round-2 changes | Checks |
| --- | --- | --- |
| README.md | Explicit default profile, current counts, integration link. | Sentences 0; references 0; links 0; graph 0. |
| doc/architecture.md | Application option in receive path, suite count, current anchors. | Sentences 0; references 0; links 0; three graphs 0. |
| doc/developer.md | Optional Registrar transition, deadline rule, separate profile graph, current anchors. | Sentences 0; references 0; links 0; nine graphs 0. |
| doc/integrator.md | Build switch, direct build definition, application option, callback sequence, rebuild requirement, timer guidance. | Sentences 0; references 0; links 0; eight graphs 0. |
| doc/manager.md | Profile matrix row, current evidence, issue scope, current anchors. | Sentences 0; references 0; links 0; graph 0. |
| doc/tester.md | Both profile commands, counts, regression coverage, independent reversal requirements, both freestanding modes. | Sentences 0; references 0; links 0; two graphs 0. |

Global checks: 860 sentences/fragments; zero over 25 words; zero prose exemptions.
References: zero unlinked references; all 79 self-tests pass.
Links: 331 local links and 19 external URLs pass.
Repository links use authenticated access; other links use anonymous requests.
All 43 source anchors were mapped and reviewed against their target definitions or rows.

The first link replay returned 1 because the original publisher homepage returned HTTP 403 with a browser challenge.
The publisher's specification page and other site URLs had the same result.
The final links use the official Milan site's specification-access guidance, which returns HTTP 200.
The developer guide identifies that destination as access guidance and states the compared revision.
No failure was exempted and the link checker was not weakened.

All 25 graphs render; each command returns 0; maximum 11 nodes.
The original 23 graph sources are identical to the previously inspected versions.
Both new graphs were inspected at native size and reduced page width.
The first profile state graph had overlapping labels despite render rc 0.
Left-to-right layout and shorter action labels fixed the overlap.
The final new graphs have readable labels and no edge crossing a node.
All documentation checks were repeated after that layout change; all returned 0.

| Graph | Nodes | Render rc | Visual status |
| --- | --- | --- | --- |
| CONTRIBUTING.md:48 | 5 | 0 | Unchanged source; prior visual inspection retained. |
| README.md:15 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/architecture.md:10 | 11 | 0 | Unchanged source; prior visual inspection retained. |
| doc/architecture.md:35 | 10 | 0 | Unchanged source; prior visual inspection retained. |
| doc/architecture.md:62 | 8 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:29 | 10 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:81 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:114 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:143 | 7 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:170 | 3 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:201 | 3 | 0 | New; native and page-width inspection passed. |
| doc/developer.md:229 | 2 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:256 | 2 | 0 | Unchanged source; prior visual inspection retained. |
| doc/developer.md:299 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:44 | 2 | 0 | New; native and page-width inspection passed. |
| doc/integrator.md:81 | 4 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:121 | 4 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:169 | 3 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:217 | 3 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:251 | 3 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:281 | 2 | 0 | Unchanged source; prior visual inspection retained. |
| doc/integrator.md:312 | 4 | 0 | Unchanged source; prior visual inspection retained. |
| doc/manager.md:46 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/tester.md:89 | 6 | 0 | Unchanged source; prior visual inspection retained. |
| doc/tester.md:119 | 9 | 0 | Unchanged source; prior visual inspection retained. |

### Issue status and delivery

[Issue 6](https://github.com/kebag-logic/lwSRP/issues/6) remains fixed by the local branch.
Every destination regression passes; planted wrong addresses fail their checks.
[Issue 7](https://github.com/kebag-logic/lwSRP/issues/7) remains fixed by the local branch.
The receive handler limits LeaveAll to the message type and ingress port.
The unchanged scope matches [IEEE 802.1Q-2018, clause 10.7.5.20](https://standards.ieee.org/ieee/802.1Q/6844/).
Both isolation tests pass; the all-types reversal fails them.
Both issues remain open remotely until the manager publishes and merges the prepared closing references.
[Issue 11](https://github.com/kebag-logic/lwSRP/issues/11) is implemented and tested; its closing reference is included.

Local commit: `86a5f74c028dedec2a0f5bc1c5a258bbd83746b9`.
Subject: Add opt-in Milan MSRP rapid withdrawal.
The commit uses the configured identity, one subject line, no body, and no trailers.
No push, PR creation/edit, rebase, amend, comment edit/delete, or delegation occurred.
The manager owns publication.
Target execution and network interoperability remain unverified.
The option implements the specified transition; it does not claim full Milan conformance.

[ROUND2-COMMANDS.json](ROUND2-COMMANDS.json) records commands and return codes with portable path aliases.
[PR-BODY.md](PR-BODY.md) contains the final prepared body, including the required Round 2 section.
Final status payload: [A563] REVIEW READY 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9.

Final status comment posted: [REVIEW READY](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032727963); rc 0.
Final delivery audit returned 0. No required work remains.

## Round 3

Status: REVIEW READY; final status comment posted.
Starting head: 23d9a8173b07503a0ee6e8528f922fceab4e67f0.
Origin is the required repository; verification rc 0.
Branch was clean; verification rc 0.
The starting tree and prior head both resolve to 7cf49d0d499d21227764282b9d64c8de86f83758; verification rc 0.
The earlier sections preserve historical receipts from before the owner rewrote history.
The owner authorized these source changes in the [Round 3 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033222017).
The exact issue bodies, owner rules, assignment comments, and both cited reviews were read.
The public review probes and mutation scripts were read from the evidence branch.
The [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6032999319) and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033216570) are addressed below.
No new TAKEN comment was posted.

### Conflicts and decisions

No merge or conflict was introduced in Round 3.
The earlier conflict resolutions remain intact because the rewritten starting tree was identical.
The local standard was read from the existing scratch text conversion.
No standard document or long quotation enters the tree or output packet.

| Finding | Resolution and reason | Regression evidence |
| --- | --- | --- |
| External F1 | Decoding errors reject the full payload before indications. Stream, destination, VLAN, and MAC increments reject overflow. | Atomic error, vector boundary, and legal-maximum tests; separate decoder and range reversals. |
| External F2; internal 01 | Higher versions skip unknown messages using advertised value lengths and vector boundaries. Unknown events skip their vectors. Current-version rejection remains strict. | VLAN, MAC, and stream cases preserve following supported declarations; type, event, and version reversals. |
| External F3 | Domain increments cite the Domain discovery clause. The manager matrix includes both stream and Domain authorities. | Compared with the local standard; references and links pass. |
| External F4; internal 07 | All 17 reviewed changed guards use braces. | Base-to-head added-guard review, compilation, and suites pass. |
| External F5; internal 02 | Embedded and bare-metal source lists include switch dispatch. | Actual module list links and executes all four switch entry points in both profiles. Removing the source fails linking. |
| External F6; internal 03 | Owned FIFO entries preserve internal propagation per destination during refusal. Acceptance commits the retained frame before ordered replay. | Join and timer-driven Leave match controls. Source reclamation, copied values, and operation order have regressions and reversals. |
| External F7; internal 04 | All six surviving faults have discriminating tests. | Named failures for local rLA, omitted txLAF, reserved LeaveAll, Listener subtype, upper timer boundary, and LO preservation. |
| External S1; internal 06 | Remove the extra Join indication for both received Join variants in LV. | Table 10-4 requires timer cancellation and IN without another indication. Callback and propagation counts remain one. The reversal fails the recovery test. |
| External S2; internal 05 | Pin Re-declare, transmitted LeaveAll, and received LeaveAll timer restart. | All three named tests fail their separate reversals. |

The propagation queue owns copied values until replay or destruction.
Operations on each destination remain in event order, independent of source buffer changes or reclamation.
Destination allocation failure preserves the queued operation for a later transmit poll.
Queue reservation errors are reported through receive; timer-driven withdrawal retries reservation on the next tick.
Allocation capacity must cover propagated traffic during prolonged refusal.
The host still queues its incoming payloads and local operations for a retained port.
The tested contract remains serialized and forbids reentrant callbacks.

### Behavioral fixes and planted reversals

The [reversal runner](https://github.com/kebag-logic/lwSRP/blob/a9cd5ef58a2478cb2ce4899b31aa02d5c2072646/tests/check_reversals.py) tests all 60 reversals in each profile.
Every behavioral mutation builds successfully and fails a named assertion.
Each profile has 56 successful mutation builds followed by ctest rc 8.
Two dependency checks, one optimized warning check, and one embedded link check fail intentionally with rc 1.
Baseline and restored builds and tests return 0 in both profiles.
The delayed-IN and restarted-LV reversals still fail independently.
Neither reversal fails the other's required test.
The original source checkout is never mutated by the runner.

| Reversal | Observed failing test or check | Build rc | Check rc, default / enabled |
| --- | --- | --- | --- |
| timer-unlink | `remove_head_middle_tail_and_reinitialize` | 0 | 8 / 8 |
| msrp-address | `domain_and_vector_offsets_match_wire_fields`; `every_application_uses_its_standard_destination` | 0 | 8 / 8 |
| mmrp-address | `every_application_uses_its_standard_destination` | 0 | 8 / 8 |
| mvrp-address | `every_application_uses_its_standard_destination` | 0 | 8 / 8 |
| domain-offset | `domain_and_vector_offsets_match_wire_fields` | 0 | 8 / 8 |
| talker-offset | `domain_and_vector_offsets_match_wire_fields`; `stream_vectors_cannot_wrap_identity_or_destination` | 0 | 8 / 8 |
| listener-offset | `domain_and_vector_offsets_match_wire_fields`; `stream_vectors_cannot_wrap_identity_or_destination` | 0 | 8 / 8 |
| wire-prevalidation | `a_malformed_later_message_has_no_earlier_indications`; `application_errors_reject_the_whole_pdu`; `reserved_leaveall_events_are_rejected_atomically`; `stream_vectors_cannot_wrap_identity_or_destination`; `truncation_respects_complete_vectors_and_pdu_end`; `vlan_and_mac_vector_ranges_are_atomic` | 0 | 8 / 8 |
| pdu-endmark | `truncation_respects_complete_vectors_and_pdu_end` | 0 | 8 / 8 |
| leaveall-scope | `mmrp_leaveall_changes_only_the_message_type_and_port`; `msrp_leaveall_changes_only_the_message_type_and_port` | 0 | 8 / 8 |
| local-registration | `fresh_ladder_and_refusal_are_transactional`; `refused_pdu_survives_timers_without_aging_unsent_leaveall` | 0 | 8 / 8 |
| registrar-condition | `fresh_ladder_and_refusal_are_transactional` | 0 | 8 / 8 |
| periodic-interval | `periodic_is_one_second_independent_of_join_time`; `receive_redeclare_requests_transmission_without_periodic_wait` | 0 | 8 / 8 |
| leaveall-randomization | `leaveall_draws_are_inside_the_required_interval` | 0 | 8 / 8 |
| refused-storage | `refused_pdu_survives_timers_without_aging_unsent_leaveall`; `retained_ports_replay_propagated_join_and_timer_leave_in_order` | 0 | 8 / 8 |
| registrar-during-refusal | `registrar_ages_while_a_transmission_is_retained` | 0 | 8 / 8 |
| changed-listener-indication | `changed_registered_listener_notifies_without_duplicate_join` | 0 | 8 / 8 |
| receive-opportunity | `leaving_observer_is_retained_until_its_pending_transmission`; `receive_redeclare_requests_transmission_without_periodic_wait` | 0 | 8 / 8 |
| receive-interest | `uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | 0 | 8 / 8 |
| reclaim | `leaving_observer_is_retained_until_its_pending_transmission`; `queued_propagation_owns_values_and_survives_source_reclamation`; `retained_ports_replay_propagated_join_and_timer_leave_in_order`; `uninteresting_values_do_not_allocate_and_empty_state_is_reclaimed` | 0 | 8 / 8 |
| split-fairness | `a_full_pdu_retries_omitted_attributes_before_repeats` | 0 | 8 / 8 |
| received-withdrawal-value | `disabled_application_option_preserves_ieee_timing`; `leave_in_lv_keeps_the_original_deadline`; `listener_leave_in_is_immediate`; `msrp_constructor_selects_the_build_profile`; `withdrawal_does_not_replace_the_registered_declaration` | 0 | 8 / 8 |
| local-withdrawal-value | `local_withdrawal_keeps_the_registered_listener_value` | 0 | 8 / 8 |
| talker-replacement | `talker_join_replaces_the_other_type_on_the_same_port` | 0 | 8 / 8 |
| listener-redeclaration | `changed_listener_redeclares_from_a_quiet_applicant` | 0 | 8 / 8 |
| domain-member-order | `domain_callback_preserves_existing_member_order` | 0 | 8 / 8 |
| hosted-allocation-header | Hosted header rejection | Dedicated check | 1 / 1 |
| hosted-error-header | Hosted header rejection | Dedicated check | 1 / 1 |
| point-to-point-condition | `applicant_receive_conditions_follow_link_mode` | 0 | 8 / 8 |
| shared-in-condition | `applicant_receive_conditions_follow_link_mode` | 0 | 8 / 8 |
| withdrawal-transition | `applicant_declaration_recovery_and_withdrawal_follow_the_table`; `retained_ports_replay_propagated_join_and_timer_leave_in_order` | 0 | 8 / 8 |
| periodic-passive | `applicant_declaration_recovery_and_withdrawal_follow_the_table` | 0 | 8 / 8 |
| leaveall-all-types | `transmitted_leaveall_includes_every_supported_type` | 0 | 8 / 8 |
| unknown-stream-message | `later_versions_skip_unknown_messages_in_every_application`; `later_versions_skip_unknown_stream_messages` | 0 | 8 / 8 |
| bounded-header-initialization | Optimized uninitialized-header warning | Dedicated check | 1 / 1 |
| milan-delayed-in-leave | `talker_leave_in_is_immediate`; `listener_leave_in_is_immediate` | 0 | 8 / 8 |
| milan-restarted-lv-deadline | `leave_in_lv_keeps_the_original_deadline` | 0 | 8 / 8 |
| milan-profile-selection | `msrp_constructor_selects_the_build_profile` | 0 | 8 / 8 |
| milan-option-scope | `mvrp_keeps_ieee_leave_timing`; `mmrp_keeps_ieee_leave_timing`; `disabled_application_option_preserves_ieee_timing` | 0 | 8 / 8 |
| application-decode-error | `application_errors_reject_the_whole_pdu` | 0 | 8 / 8 |
| stream-increment-overflow | `stream_vectors_cannot_wrap_identity_or_destination` | 0 | 8 / 8 |
| domain-priority-range | `application_errors_reject_the_whole_pdu` | 0 | 8 / 8 |
| domain-class-range | `application_errors_reject_the_whole_pdu` | 0 | 8 / 8 |
| vlan-range | `vlan_and_mac_vector_ranges_are_atomic` | 0 | 8 / 8 |
| mac-increment-overflow | `vlan_and_mac_vector_ranges_are_atomic` | 0 | 8 / 8 |
| unknown-event-extension | `later_versions_skip_unknown_events_but_current_versions_reject_them` | 0 | 8 / 8 |
| current-version-extension | `later_versions_skip_unknown_messages_in_every_application` | 0 | 8 / 8 |
| propagation-retention | `retained_ports_replay_propagated_join_and_timer_leave_in_order` | 0 | 8 / 8 |
| propagation-order | `queued_propagation_owns_values_and_survives_source_reclamation` | 0 | 8 / 8 |
| registrar-recovery-indication | `registrar_recovery_stops_aging_without_duplicate_join_or_map` | 0 | 8 / 8 |
| committed-local-leaveall | `full_leaveall_reports_each_required_transition` | 0 | 8 / 8 |
| omitted-leaveall-event | `full_leaveall_reports_each_required_transition` | 0 | 8 / 8 |
| reserved-leaveall-event | `reserved_leaveall_events_are_rejected_atomically` | 0 | 8 / 8 |
| listener-subtype | `changed_listener_redeclares_from_a_quiet_applicant` | 0 | 8 / 8 |
| leaveall-upper-bound | `leaveall_draws_are_inside_the_required_interval` | 0 | 8 / 8 |
| reclaim-leaving-observer | `leaving_observer_is_retained_until_its_pending_transmission` | 0 | 8 / 8 |
| milan-redeclare-scope | `redeclare_keeps_the_ieee_deadline` | 0 | 8 / 8 |
| milan-transmitted-leaveall-scope | `transmitted_leaveall_keeps_the_ieee_deadline` | 0 | 8 / 8 |
| received-leaveall-restart | `received_leaveall_restarts_the_participant_deadline` | 0 | 8 / 8 |
| embedded-switch-source | Missing switch dispatch symbols | Dedicated check | 1 / 1 |

The six new-behavior coverage faults and all three scope suggestions fail their required named tests.
The near-upper-bound timer reversal is caught with seed 168.
Literal payload regressions include invalid earlier and later messages and legal maximum values.
The queue regression verifies the original retained output bytes are unchanged.

### Validation

| Check | Final result | rc |
| --- | --- | --- |
| Default configure and build | Eight suites. | 0 each |
| Default unit run | 60 tests; 3896 assertions. | 0 |
| Enabled configure and build | Eight suites. | 0 each |
| Enabled unit run | 60 tests; 3884 assertions. | 0 |
| ctest, both profiles | 1/1 target in each profile. | 0 each |
| behave, both profiles | One feature, three scenarios, ten steps in each profile. | 0 each |
| Scenario dry run | Three scenarios and ten steps untested by design. | 0 |
| Isolated codec | Nine tests; 1690 assertions. | 0 |
| Enabled address/undefined-behavior sanitizers with leak detection | 1/1 target; 60 tests; 3884 assertions. | 0 |
| Strict freestanding checks | Seven sources; fourteen compiler invocations per profile. | 0 each |
| Actual embedded module list | Both profiles link and exercise all four public switch entry points. | 0 each |
| Reversal campaigns | 60/60 in each profile; both restored checks pass. | 0 each |
| Independent reviewer edge probes | Version, overflow, legal controls, invalid-first message, and Join recovery pass in both profiles. | 0 each |
| Independent reviewer multiport probes | Both profiles match controls: one Talker and five messages for Join; VO and one message after withdrawal. | 0 each |
| Whitespace and public-content audits | No errors; 58 tracked or proposed files carry the identifier. | 0 each |

The original six suites now contribute 2287 assertions.
The profile suite contributes 442 default assertions or 430 enabled assertions.
The boundary suite contributes 1167 assertions.
All processes ran in the foreground with explicit timeouts.
No check was piped.

### Published commands

Every command below was executed individually on the final implementation.
All 27 returned 0.
After the last documentation edit, all five documentation commands were rerun; each returned 0.
Environment variables select scratch directories and the dependency installation.
The embedded compiler, reversal runner, and graph renderer record each child return code.

| Page and line | Exact command or block | rc |
| --- | --- | --- |
| README.md:39 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF` | 0 |
| README.md:40 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| README.md:41 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| README.md:42 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:18 | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF` | 0 |
| doc/tester.md:19 | `cmake --build "$LWSRP_BUILD" --parallel 2` | 0 |
| doc/tester.md:20 | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | 0 |
| doc/tester.md:21 | `"$LWSRP_BUILD/unit_tests"` | 0 |
| doc/tester.md:22 | `SHLAN_LIBRARY="$LWSRP_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:23 | `behave --dry-run` | 0 |
| doc/tester.md:46 | `cmake -S . -B "$LWSRP_MILAN_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=ON` | 0 |
| doc/tester.md:47 | `cmake --build "$LWSRP_MILAN_BUILD" --parallel 2` | 0 |
| doc/tester.md:48 | `ctest --test-dir "$LWSRP_MILAN_BUILD" --output-on-failure` | 0 |
| doc/tester.md:49 | `"$LWSRP_MILAN_BUILD/unit_tests"` | 0 |
| doc/tester.md:50 | `SHLAN_LIBRARY="$LWSRP_MILAN_BUILD/libshlan.so" behave` | 0 |
| doc/tester.md:73 | `cc -std=c11 -Isrc/include tests/unit/mrp_pdu_test.c src/core/mrp_pdu.c -xc - -lcgreen -o "$LWSRP_BUILD/mrp_pdu_tests" <<'C'<br>#include <cgreen/cgreen.h><br>TestSuite *mrp_pdu_suite(void);<br>int main(void)<br>{<br>    return run_test_suite(mrp_pdu_suite(), create_text_reporter());<br>}<br>C` | 0 |
| doc/tester.md:81 | `"$LWSRP_BUILD/mrp_pdu_tests"` | 0 |
| doc/tester.md:161 | `python3 tests/check_embedded.py --work-dir "$EMBEDDED_SCRATCH"` | 0 |
| doc/tester.md:162 | `python3 tests/check_freestanding.py` | 0 |
| doc/tester.md:163 | `CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py` | 0 |
| doc/tester.md:164 | `python3 tests/check_reversals.py --work-dir "$REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX"` | 0 |
| doc/tester.md:165 | `python3 tests/check_reversals.py --work-dir "$MILAN_REVERSAL_SCRATCH" --prefix "$CGREEN_PREFIX" --milan ON` | 0 |
| doc/tools/README.md:14 | `python3 doc/tools/check_sentences.py` | 0 |
| doc/tools/README.md:15 | `python3 doc/tools/check_references.py` | 0 |
| doc/tools/README.md:16 | `python3 doc/tools/check_references.py --self-test` | 0 |
| doc/tools/README.md:17 | `python3 doc/tools/check_links.py --github-auth` | 0 |
| doc/tools/README.md:18 | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | 0 |

### Documentation pages and checks

| Page | Changes | Final results |
| --- | --- | --- |
| README.md | Current test counts and four-reader entry points retained. | Sentences 0; references 0; links 0; graph 0. |
| doc/architecture.md | Atomic ranges, extension handling, owned queues, updated receive order, eight suites, current anchors. | Sentences 0; references 0; links 0; three graphs 0. |
| doc/developer.md | Correct Registrar recovery, deferred queue lifetime, Domain authority, vector limits, current anchors. | Sentences 0; references 0; links 0; nine graphs 0. |
| doc/integrator.md | Receive version contract, FIFO retention sequence, allocation and lifetime, embedded source completeness, current anchors. | Sentences 0; references 0; links 0; nine graphs 0. |
| doc/manager.md | Correct recovery, receive, Domain, and propagation matrix entries; current evidence and anchors. | Sentences 0; references 0; links 0; graph 0. |
| doc/tester.md | Boundary coverage, embedded link command, both reversal profiles, current counts. | Sentences 0; references 0; links 0; two graphs 0. |
| Public MRP header | Queue ownership, replay order, lifetime, and destination-allocation retry. | Both profiles compile; strict checks 0; whitespace 0. |

Final checks: 904 sentence fragments; zero over 25 words; zero prose exceptions.
There are zero unlinked references; all 79 reference self-tests pass.
All 345 local links and 19 external URLs pass.
Repository URL checks use authenticated access; other external URLs are anonymous.
All 43 source-line anchors were refreshed and inspected against their intended definitions or rows.
All 26 graphs render; maximum 11 nodes; every render returns 0.
All graphs were viewed in page-width sheets.
The changed receive flow and new retention sequence were also viewed at native size.
No label clipping, overlap, or edge crossing an unrelated node was found.
The displayed state paths retain the previous normative comparison; corrected Registrar actions now match Table 10-4 as well.

| Graph | Nodes | Render rc | Visual result |
| --- | --- | --- | --- |
| CONTRIBUTING.md:48 | 5 | 0 | Clear labels; no clipping or unrelated node crossings. |
| README.md:15 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/architecture.md:10 | 11 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/architecture.md:35 | 11 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/architecture.md:67 | 8 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:29 | 10 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:81 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:114 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:143 | 7 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:170 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:202 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:230 | 2 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:257 | 2 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/developer.md:313 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:44 | 2 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:81 | 4 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:121 | 4 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:172 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:215 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:242 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:276 | 3 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:306 | 2 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/integrator.md:337 | 4 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/manager.md:46 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/tester.md:90 | 6 | 0 | Clear labels; no clipping or unrelated node crossings. |
| doc/tester.md:120 | 9 | 0 | Clear labels; no clipping or unrelated node crossings. |

### Exploratory failures and recovery

The first new unit run returned 1 because a test incorrectly expected a quiescent source to resist reclamation.
The corrected test requires reclamation, exercising the queued value's independent lifetime.
Its final run returns 0; both propagation reversals fail named tests.
Two optional raster-view commands returned 1 because the installed browser module used a different layout.
Resolving the installed module path fixed both view commands; final raster generation returns 0.
These were scratch-only visualization helpers; all graph-render checks returned 0.
The first connector reads returned unavailable; authenticated repository reads succeeded and supplied the exact assignments and reviews.
No failed required check is waived.

### Issue status and delivery

[issue 6](https://github.com/kebag-logic/lwSRP/issues/6) remains fixed: the destination and cited address authority were rechecked against the local standard.
All application destination tests and wrong-address reversals pass their expected checks.
[issue 7](https://github.com/kebag-logic/lwSRP/issues/7) remains fixed: received LeaveAll reaches only its message type on the ingress port.
This matches [IEEE 802.1Q-2018, clause 10.7.5.20](https://standards.ieee.org/ieee/802.1Q/6844/).
Both multi-type isolation tests pass; widened delivery fails them.
[issue 11](https://github.com/kebag-logic/lwSRP/issues/11) remains implemented and independently tested in both profiles.
The remote issues remain open pending publication and merge by the manager.

Local head: a9cd5ef58a2478cb2ce4899b31aa02d5c2072646.
The commit uses the configured identity and a single-line subject without a body or trailers.
No push, PR creation/edit, rebase, amend, comment edit/delete, or delegation occurred.
Target execution and network interoperability remain unverified.
The queue requires memory sized for retained traffic; the host tests do not establish a target resource budget.
The [command ledger](ROUND3-COMMANDS.json) and [reversal ledger](ROUND3-REVERSALS.json) use portable path aliases.
The prepared [PR body](PR-BODY.md) includes this round and the required closing links.

Committed-state audit: rc 0. Parent, origin, branch, clean tree, configured identity, and one-line message verified.
Subject: Fix atomic receive validation and retained propagation.
Final status payload: [A563] REVIEW READY a9cd5ef58a2478cb2ce4899b31aa02d5c2072646.

Final delivery audit: rc 0.
Final [REVIEW READY comment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033629484) posted; rc 0.
No required Round 3 work remains. Branch remains unpushed.

## Round 4

The [assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6033982129) accepts the [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033931109) and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6033978356).
Both packets were read on the public evidence branch.
This includes the internal candidate diff, receive probe, allocation probe, and mutation script.
The external ordering and allocation probes were read and executed.
The candidate diff was used as a reference.
The allocation and ordering fixes required a unified indication path.

Origin and assigned starting head were confirmed; both checks returned 0.
The branch was clean at the start.
No merge conflicts occurred in this round.
The earlier merge resolutions remain recorded above.
No push, PR mutation, comment edit, rebase, amend, identity change, or delegation occurred.
No second TAKEN message was posted.

### Findings and decisions

- R540-2-01: changed Listener and Talker registrations indicate and propagate in IN and LV.
  Tests cover JoinIn and JoinMt after received and transmitted LeaveAll.
  Unchanged values retain the normal recovery cell.
- R540-2-02: unknown later-version stream messages skip to their list boundary without decoding unknown vector layouts.
  VLAN and MAC retain vector-based traversal.
  Current-version rejection stays strict.
  A non-generic unknown message followed by a valid Listener is pinned.
- R541-2-F1: failed propagation reservation restores the old source value, Registrar state, and Applicant state.
  The corresponding host indication is withheld.
  An identical payload retry delivers the update to every selected target.
  Earlier completed events may remain applied.
- R541-2-F2: reserve all possible target entries before indication, then call propagation policy after the host indication.
  Policy may depend on the newly indicated host state.
  Unselected entries are released.
  This requires temporary capacity for one entry per possible target, capped at 32.
- R541-2-F3: the integration table now says eight suites.
- R540-2-03: a replacement allocation port injects failures and counts live allocations.
  Tests pin reservation, rollback, error reporting, timer retry, poll replay, commit replay, changed propagation, and teardown.
  The zero-length generic attribute rejection also has a discriminating test.
- Both pairs of licence residues use the exact requested wording.
  Relative licence links remain relative to the documentation page.

### Behavioural fixes and reversals

All 75 reversals are detected in each profile.
Every behavioral mutation compiles successfully before failing its required check.
The 71 behavioral/layout checks return 8 through the test driver.
The three strict/header checks and embedded link reversal return 1 as expected.
Both restored builds and test runs return 0.
The [complete reversal ledger](ROUND4-REVERSALS.json) records both profiles, every plant, and the observed failing names.
The following additional cases close this round's findings.
All listed test failures occur in both profiles, with rc 8.

| Reversal | Discriminating regression |
| --- | --- |
| [changed-in-only](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [changed_values_after_received_leaveall_are_indicated_and_propagated](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c), [changed_values_after_transmitted_leaveall_are_indicated_and_propagated](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [stream-list-boundary](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [unknown_stream_layout_uses_attribute_list_length](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [changed-value-rollback](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [changed_value_allocation_failure_preserves_retry](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [registrar-rollback](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [timer_allocation_failure_rolls_back_and_retries](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c), [reservation_failure_is_reported_without_partial_publication](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [applicant-rollback](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [reservation_failure_is_reported_without_partial_publication](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [leave-timer-retry](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [timer_allocation_failure_rolls_back_and_retries](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [receive-map-error](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [reservation_failure_is_reported_without_partial_publication](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [reservation-atomicity](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [reservation_failure_is_reported_without_partial_publication](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [poll-replay](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [failed_commit_replay_is_retried_by_the_next_poll](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [commit-replay](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [retained_ports_replay_propagated_join_and_timer_leave_in_order](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [queue-teardown](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [destroy_releases_all_queued_allocations](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [zero-attribute-length](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [unknown_generic_messages_reject_zero_attribute_length](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [changed-value-propagation](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [changed_values_after_received_leaveall_are_indicated_and_propagated](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c), [changed_values_after_transmitted_leaveall_are_indicated_and_propagated](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [replay-error-retention](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [failed_commit_replay_is_retried_by_the_next_poll](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |
| [callback-order](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/check_reversals.py) | [propagation_policy_observes_completed_host_indications](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/tests/unit/review_test.c) |

The internal review's 17 plants were rerun in both profiles.
All 15 non-equivalent plants fail; the two documented equivalent plants remain successful.
The required x02–x07, x12, and x16 failures name the new regressions.
The x16 source target was adapted to the unified publication block.
Its meaning remains suppression of changed-value propagation.
Every other mutation remains unchanged.
The x10 timer callback is harmless after recovery to IN; x17 still encounters the public retention guard.
Those two were explicitly classified as equivalent by the review.

### Final checks

| Check | Default profile | Enabled profile | rc |
| --- | --- | --- | --- |
| Configure and build | Passed | Passed | 0 |
| Unit runner | 70 tests; 4215 assertions | 70 tests; 4203 assertions | 0 |
| Test driver | 1/1 target | 1/1 target | 0 |
| Scenarios | 1 feature; 3 scenarios; 10 steps | 1 feature; 3 scenarios; 10 steps | 0 |
| Reversal driver | 75 detected; restored checks pass | 75 detected; restored checks pass | 0 |
| Instrumented suites | 70 tests; 4215 assertions | 70 tests; 4203 assertions | 0 |
| Embedded source-list link and execution | Passed | Passed | 0 |
| Freestanding source checks | Seven sources; 14 compiler commands | Seven sources; 14 compiler commands | 0 |
| Independent receive and allocation probes | All passed | All passed | 0 |

Instrumented execution checks address errors, undefined behavior, and leaks.
Six independent probe compilations and twenty probe executions return 0.
The external allocation-failure and no-failure controls both deliver the final value to every target.
The callback-order probe observes the completed host indication and creates the destination instance.
The scenario dry run reports one feature, three scenarios, and ten steps untested; rc 0.
The isolated codec run passes nine tests and 1690 assertions; rc 0.
All 27 published commands were executed separately and return 0 in the final run.
No check was piped.
Every campaign completed in the foreground.

The [command receipt](ROUND4-COMMANDS.json) records commands and return codes with portable location aliases.
The [result receipt](ROUND4-RESULTS.txt) retains final check output and named reviewer-plant failures.
Dependencies, binaries, normative text, and rendered images remain in scratch.
No output file exceeds 200 KB.

### Documentation

| Page | Change | Result |
| --- | --- | --- |
| [Readme](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/README.md) | Current test totals. | All applicable documentation checks pass. |
| [Developer](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/developer.md) | Changed values in LV, reservation rollback, ordering, and anchors. | All applicable documentation checks pass. |
| [Integrator](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/integrator.md) | Eight suites, stream skipping, callback sequence, and allocation contract. | All applicable documentation checks pass. |
| [Manager](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/manager.md) | Receive and replacement matrix rows, test totals, and licence residue. | All applicable documentation checks pass. |
| [Tester](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/tester.md) | Allocation port, coverage, totals, and 75 reversals. | All applicable documentation checks pass. |
| [Architecture](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/architecture.md) | Correct callback order and distinct extension boundaries. | All applicable documentation checks pass. |
| [Documentation checks](https://github.com/kebag-logic/lwSRP/blob/82422d6ffe38d430576cd9d874a45b9e124e6c63/doc/tools/README.md) | Exact required licence wording. | All applicable documentation checks pass. |

Sentence check: 925 fragments, zero over 25 words, no prose exemptions; rc 0.
Reference check: zero unlinked references; rc 0.
Reference self-test: 79 cases pass; rc 0.
Links: 347 local links and 20 external URLs pass; rc 0.
Repository URLs use authenticated access.
All 26 graphs render; maximum 12 nodes; every render returns 0.
Both changed diagrams were inspected visually and remain readable.
All 43 source anchors identify their intended code.
The unchanged diagrams retain their prior visual review and were rendered again.
The file audit checks 60 files: licence identifiers present, no private residue, no oversized files, and no generated assets; rc 0.
Whitespace and changed-control-statement brace checks pass; rc 0.

### Issue status and limits

The [destination issue](https://github.com/kebag-logic/lwSRP/issues/6) remains fixed and covered by all-application address tests and wrong-address reversals.
The [LeaveAll issue](https://github.com/kebag-logic/lwSRP/issues/7) remains fixed and covered by multi-type, multi-port isolation tests and the all-types reversal.
The local [IEEE 802.1Q-2018 standard](https://standards.ieee.org/ieee/802.1Q/6844/) was checked directly.
The relevant authorities are Table 10-4 and clauses 10.7.5.20, 10.8.3.5, 35.2.2.1, and 35.2.2.6.
No standard text is included in the repository or output packet.
Both issues close through merge, not this local work.
The existing profile issue remains covered in both builds.
Target execution, hardware validation, and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains disclosed.

### Exploratory failures

The first build returned 2 because a test used the wrong enum spelling; this was corrected.
The attempted runner before that build completed returned 1 because the executable did not exist.
The first executable run returned 1 because a test configured its port after registration; setup was corrected.
The first reversal run and first published run returned 1 because the Applicant rollback stimulus left its state unchanged.
The final stimulus uses JoinIn on a shared link and detects that reversal.
The final full published run, both reversal profiles, and instrumented suites all pass.
Earlier failures remain visible in the command receipt.

Final commit: `82422d6ffe38d430576cd9d874a45b9e124e6c63`.
The subject is one line, without body or trailers.
The configured identity was used.
The final tree is clean and one commit ahead of the published branch.
[REVIEW READY](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6034308037) posted with the final head; rc 0.
All foreground work is complete. No push was performed.
Draft source links target the local commit and resolve remotely after the manager publishes it.

## Round 5

Status: implementation and validation complete. Ready for independent review.
Final local head: [0a45695db537badb8d7e9cbf578925fe5b89d647](https://github.com/kebag-logic/lwSRP/commit/0a45695db537badb8d7e9cbf578925fe5b89d647).
The branch is one commit ahead of its published tracking branch. No push occurred.
The configured identity was used. The commit has one subject line and no body or trailers.
The initial remote URL, branch, clean status, and expected resume head were confirmed; each command returned 0.
The resume head was `82422d6ffe38d430576cd9d874a45b9e124e6c63`.

The [round-5 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6034815912) accepts the [internal review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034569438) and [external review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6034811505).
Their public packets were read from the evidence branch at [the frozen evidence head](https://github.com/kebag-logic/milan-fpga/tree/e5bd1a7ca91b4b55ee04ffc62790951d603c54d7/review-evidence/lwsrpm2-r1/reviews).
Both reports, both probe sources, the external Flush runner, and the internal plant script were read before correction.
The original assignment, issue body, documentation rules and owner comments, destination issue, and LeaveAll issue were also read.

### Conflicts and implementation decisions

There was no merge in this round and no conflict.
The earlier merge conflicts and their resolutions remain recorded above.
Only the assigned source fixes, their tests, reversal cases, and affected documentation changed.

The topology interface retains its existing return type.
A failed Flush reservation now enters LV and arms a one-centisecond Leave timer.
The existing timer retry handles repeated reservation failure and publishes withdrawal when allocation succeeds.
This avoids an unreported, discarded topology operation while retaining the serialized dispatch contract.
The host continues global ticks and destination polls.

Talker replacement now checks both old-registration withdrawal events.
A failure returns before delivering the new event and restores an existing replacement value when needed.
An identical receive retry then delivers the old Leave before the new Join.
A failed rapid Leave also stops before attempting the old Leave-timer event.

The receive rule remains: stop later attributes after reservation failure.
Policy publication keeps only selected destinations.
Applications without the corresponding policy reserve no propagation entries.
These three existing rules now have discriminating tests and named reversals.

### Behavioral fixes, regressions, and reversals

All named tests are in [the boundary suite](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c).
All named plants are in [the reversal runner](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py).
Every new behavioral reversal builds with rc 0 and fails its required named test in both profiles; the test target returns 8.
The complete reversal drivers return 0 after verifying expected failures and passing restored checks.

| Finding | Regression | Named reversal | Result in both profiles |
| --- | --- | --- | --- |
| Failed topology withdrawal | [flush_allocation_failures_retry_withdrawal_on_the_next_tick](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) | [flush-retry](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) | IN and LV; control and all three reservation positions; repeated exhaustion; exactly one Leave; later Join restored. |
| Replacement indication order | [replacement_allocation_failures_keep_leave_before_join](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) | [replacement-order](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) | Both Talker replacement directions; control and all nine allocation positions; Leave before Join; destination recovery. |
| Receive stop; y01 | [reservation_failure_stops_later_receive_messages](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) | [receive-stop](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) | Every first-message reservation position; no later-message state or indication before retry. |
| Policy masks; y02 | [propagation_obeys_talker_and_listener_policy_masks](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) | [policy-mask](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) | Talker excludes ingress; Listener selects its Talker port and excludes unrelated ports. |
| No-policy allocation; y07 | [applications_without_policy_do_not_reserve_propagation](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/unit/review_test.c) | [no-policy-reservation](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/tests/check_reversals.py) | VLAN Join allocates only its source instance; Flush allocates no propagation work. |

The initial regression run returned 1 and exposed both source defects.
That development run also found an observer-state test assumption and a still-armed fault injection after a failed assertion.
The test setup was corrected before final validation.
No baseline crash or compilation failure was counted as a successful reversal.
The final named reversals fail assertions after successful builds.

### Executed validation

| Check | Default | Enabled | Return code |
| --- | --- | --- | --- |
| Configure and build | Pass | Pass | 0 each |
| Configured test target | 1/1 | 1/1 | 0 each |
| Unit runner | Eight suites; 75 tests; 4745 assertions | Eight suites; 75 tests; 4733 assertions | 0 each |
| Scenarios | One feature; three scenarios; ten steps | One feature; three scenarios; ten steps | 0 each |
| Scenario dry run | Step matching passes | Published once | 0 |
| Isolated codec | Nine tests; 1690 assertions | Published once | 0 |
| Complete reversals | 80/80 detected | 80/80 detected | Driver 0 each |
| Restored reversal build and test | Pass | Pass | 0 each |
| Embedded source-list link and dispatch | Pass | Pass | 0 each |
| Freestanding compilation and dependencies | Seven sources | Seven sources | 0 each |
| Instrumented unit and configured tests | Pass; normal assertion count | Pass; normal assertion count | 0 each |
| Internal allocation and order probe | All f1, f2, f3 cases pass | All f1, f2, f3 cases pass | Build 0; run 0 each |
| Internal surviving-plant probe | All q1–q4 checks pass | All q1–q4 checks pass | Build 0; run 0 each |
| External Flush runner | 532 checks; no failures or live allocations | 532 checks; no failures or live allocations | Build 0; run 0 each |
| External allocation sweep | 2289 checks; no failures or live allocations | 2289 checks; no failures or live allocations | Build 0; run 0 each |
| Reviewer plants | 13 detected; one equivalent survives | 13 detected; one equivalent survives | Builds 0; detected tests 1; equivalent 0 |

The reviewer plants were run from the unmodified public script in scratch.
A foreground wrapper recorded every configure, build, and test return code.
The script's failing-name extractor returned empty lists; the receipts additionally extract actual assertion names from each unit log.
The y01, y02, and y07 plants fail exactly their matching named regressions in both profiles.
The surviving y03 plant removes pending-transmit rollback; the reviewer classifies it as equivalent because indicating events never set pending transmit.
No reported non-equivalent plant survives.

The external allocation runner initially lacked its expected dependency-prefix location, so its final unit compilation returned 1.
Its independent fault sweeps already passed.
After linking the existing dependency installation into scratch, the unchanged runner passed all builds and executions with rc 0.
The first-run receipts remain preserved; no dependency was installed into the checkout or output directory.
Address, undefined-behavior, and leak instrumentation reports no error on the restored source.
All allocation tests end with zero live allocations.

### Documentation and standards

The local standard was converted to text in scratch; conversion returned 0. No standard text was copied into the repository.
The retry behavior was checked against [IEEE 802.1Q-2018, clause 10.7.5.2 and Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
Resource exhaustion is an implementation recovery contract; it does not change the normal Flush table transition.

| Page or interface | Change | Check result |
| --- | --- | --- |
| [README.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md) | Updated unit counts. | Passed applicable checks; rc 0. |
| [doc/architecture.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/architecture.md) | Refreshed transmit source anchors. | Passed applicable checks; rc 0. |
| [doc/developer.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/developer.md) | Documented Flush retry, replacement order, and receive stopping; added the retry graph; refreshed source anchors. | Passed applicable checks; rc 0. |
| [doc/integrator.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/integrator.md) | Documented failed Flush retention, ticks and polling, receive retry boundaries, and replacement indication order. | Passed applicable checks; rc 0. |
| [doc/manager.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/manager.md) | Updated assertion counts and the Registrar recovery claim; refreshed source anchors. | Passed applicable checks; rc 0. |
| [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md) | Updated counts and reversal totals; described allocation sweeps; separated covered policy masks from future topology filtering. | Passed applicable checks; rc 0. |
| [src/include/shish_lan/mrp.h](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/include/shish_lan/mrp.h) | Updated the topology and retention contracts without an API signature change. | Passed applicable checks; rc 0. |

All five documentation commands pass with rc 0.
There are 941 sentence fragments, none over 25 words, and zero unlinked references.
All 79 reference self-tests pass.
All 352 local links and 20 external URLs pass.
Repository URLs use authenticated access; other URLs use anonymous access.
All 27 graphs render, with a maximum of 12 nodes.
The new Flush graph has seven actual nodes and was viewed at its native page-sized rendering.
Its labels are readable, and no edge crosses a node.
Other graph sources are unchanged and were rendered again.
All 43 source anchors were mapped to the same named source lines after the edits and manually inspected.
All 60 tracked files retain their licence identifiers.
The complete pull-request range has zero unbraced added control statements.
Whitespace, conflict-marker, generated-artifact, size, and private-residue audits pass; rc 0.

[Issue #6](https://github.com/kebag-logic/lwSRP/issues/6) remains fixed: the [stream destination](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/modules/msrp.c) uses the Nearest Bridge address.
The authority is [IEEE 802.1Q-2018, clause 35.2.2.1 and Table 8-1](https://standards.ieee.org/ieee/802.1Q/6844/).
[Issue #7](https://github.com/kebag-logic/lwSRP/issues/7) remains fixed: [received LeaveAll](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/src/core/mrp_mad.c#L1047) reaches only its message type on the ingress port.
The local [IEEE 802.1Q-2018, clause 10.7.5.20](https://standards.ieee.org/ieee/802.1Q/6844/) confirms that scope.
Address and LeaveAll isolation tests pass, and their wrong-address and all-types reversals fail in both profiles.
Both issues are still open remotely; the draft retains their closing links for the manager’s merge.

### Published commands and receipts

Every published shell command was executed in the foreground, without a pipeline.
All 27 returned 0.
Their exact published text and return codes are preserved in [the command ledger](ROUND5-COMMANDS.json).
Builds, rendered graphs, compiler products, dependency references, and standard text remain in scratch.
No generated image or file over 200 KB is in the checkout or output directory.

| Entry | Published location | Return code |
| --- | --- | --- |
| published-01 | [README.md:39](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md#L39) | 0 |
| published-02 | [README.md:40](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md#L40) | 0 |
| published-03 | [README.md:41](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md#L41) | 0 |
| published-04 | [README.md:42](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/README.md#L42) | 0 |
| published-05 | [doc/tester.md:18](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L18) | 0 |
| published-06 | [doc/tester.md:19](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L19) | 0 |
| published-07 | [doc/tester.md:20](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L20) | 0 |
| published-08 | [doc/tester.md:21](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L21) | 0 |
| published-09 | [doc/tester.md:22](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L22) | 0 |
| published-10 | [doc/tester.md:23](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L23) | 0 |
| published-11 | [doc/tester.md:54](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L54) | 0 |
| published-12 | [doc/tester.md:55](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L55) | 0 |
| published-13 | [doc/tester.md:56](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L56) | 0 |
| published-14 | [doc/tester.md:57](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L57) | 0 |
| published-15 | [doc/tester.md:58](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L58) | 0 |
| published-16 | [doc/tester.md:81](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L81) | 0 |
| published-17 | [doc/tester.md:89](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L89) | 0 |
| published-18 | [doc/tester.md:170](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L170) | 0 |
| published-19 | [doc/tester.md:171](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L171) | 0 |
| published-20 | [doc/tester.md:172](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L172) | 0 |
| published-21 | [doc/tester.md:173](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L173) | 0 |
| published-22 | [doc/tester.md:174](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tester.md#L174) | 0 |
| published-23 | [doc/tools/README.md:14](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L14) | 0 |
| published-24 | [doc/tools/README.md:15](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L15) | 0 |
| published-25 | [doc/tools/README.md:16](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L16) | 0 |
| published-26 | [doc/tools/README.md:17](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L17) | 0 |
| published-27 | [doc/tools/README.md:18](https://github.com/kebag-logic/lwSRP/blob/0a45695db537badb8d7e9cbf578925fe5b89d647/doc/tools/README.md#L18) | 0 |

Receipts:

- [Commands, published commands, probes, and instrumentation](ROUND5-COMMANDS.json).
- [Default reversal commands and named failures](ROUND5-REVERSALS-OFF.json).
- [Enabled reversal commands and named failures](ROUND5-REVERSALS-ON.json).
- [Default reviewer plants and return codes](ROUND5-PLANTS-OFF.json).
- [Enabled reviewer plants and return codes](ROUND5-PLANTS-ON.json).
- [Detailed results, links, graph renders, and source anchors](ROUND5-RESULTS.txt).
- [Current pull-request draft](PR-BODY.md).

Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains disclosed.
The manager owns publication, independent review, pull-request updates, issue closure, and merge validation.
No existing issue or pull-request comment was edited or deleted.
No push, pull-request write, history rewrite, identity change, or delegated work occurred.
The final status comment is the only remote write in this round.

Final integrity audit: rc 0. The committed head and parent match; the worktree is clean, including ignored files.
The one-line commit uses the configured identity. Portable receipts and output sizes pass the final audit.
[REVIEW READY](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6035110842) posted with the final head; rc 0.
No push was performed. Draft source links become remotely available after the manager publishes the commit.

## Round 6

Status: REVIEW READY. Checks complete; committed locally and unpushed.
Starting head: `0a45695db537badb8d7e9cbf578925fe5b89d647`.
Final head: `a29f8d13ff4869e54997d9adf05d83a4ace4b8bd`.
The origin is the assigned public repository, and the branch is the assigned integration branch.
The starting worktree was clean.
No merge conflicts occurred in this round.
The earlier conflict ledger remains applicable; no earlier resolution was changed.

### Scope and findings

Read the [round-6 assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6035585910), [original assignment](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6032186634), and [issue body](https://github.com/kebag-logic/lwSRP/issues/10).
Also read the [documentation rules](https://github.com/kebag-logic/lwSRP/issues/1), [destination issue](https://github.com/kebag-logic/lwSRP/issues/6), and [LeaveAll issue](https://github.com/kebag-logic/lwSRP/issues/7).
Read the [internal delta review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) and [external delta review](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962), including their probe sources and plants.
The [provenance receipt](ROUND6-PROVENANCE.json) pins the evidence branch commit and hashes every copied review script.
All scripts and generated artifacts stayed in scratch.

All five assigned findings are addressed:

| Finding | Change and reason | Regression and reversal |
| --- | --- | --- |
| [R541-4-F1](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962) | A pending flag preserves the failed Flush across receive dispatch. The saved-value Leave completes before the incoming value is applied. Failed retries return the allocation error and stop later attributes. | [pending_flush_precedes_received_registration](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L916); [pending-flush](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py), [flush-before-refresh](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py), and [flush-completion](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |
| [R541-4-F1](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962) | Repeated receive failures preserve values, event order, and owned allocations. Ordinary LV recovery remains unchanged. | [pending_flush_talker_receive_failures_preserve_order_and_values](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L920); [pending_flush_failed_talker_receive_failures_preserve_order_and_values](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L925); [pending_flush_listener_receive_failures_preserve_order_and_values](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L929); [pending-flush](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |
| [R541-4-F2](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035579962) | Independent first-tick recovery and repeated-failure cases reject a two-tick initial delay. The fault port reports whether each intended failure occurred. | [flush_allocation_failures_retry_withdrawal_on_the_next_tick](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L646); [flush-deadline](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |
| [R540-4-01](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) | The error path reports retained IN-to-LV transitions after restoring Applicant state. This preserves the observer contract. | [failed_flush_reports_continuous_observer_transitions](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L955); [flush-observer](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |
| [R540-4-02](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) | Replacement tests start in received-LeaveAll LV, in both directions, at every allocation position. | [replacement_from_lv_keeps_leave_before_join_at_every_allocation](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L803); [replacement-lv](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py) and [replacement-leave-timer](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |
| [R540-4-03](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) | The stop regression now includes the source-instance allocation. Its new reversal removes only the source-error guard. | [reservation_failure_stops_later_receive_messages](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/unit/review_test.c#L987); [receive-instance-stop](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/tests/check_reversals.py). |

The pending-withdrawal matrix runs 144 receive interleavings per profile.
It covers all three stream registration types, IN and LV, changed and unchanged values, New, JoinIn, JoinMt, and all three Flush reservation faults.
The receive-failure matrix adds 216 cases per profile, across all six Leave and Join reservations.
Every case repeats refusal, verifies old Leave values and new registration values, checks subsequent unchanged Join, and destroys the application without live allocations.
The timer matrix has 24 cases, with zero, one, or two additional failed ticks.
Observer continuity covers all three faults and both timer and receive recovery.
The existing IN replacement sweep remains; a separate 20-case LV sweep covers both directions and all nine allocations.
The source-stop sweep covers positions one through four.

The [internal suggestions](https://github.com/kebag-logic/lwSRP/pull/12#issuecomment-6035484452) are also tracked.
The guides now disclose that later LeaveAll events can apply during a failed payload; identical replay restores the final state.
The receive-before-tick suggestion is resolved by the pending flag.
The pre-existing Flush-to-LeaveAll plant remains a coverage gap; it was not among the five assigned corrections.

### Validation

| Check | Default profile | Enabled profile | Return codes |
| --- | --- | --- | --- |
| Configure and build | Pass | Pass | 0 each |
| Configured test target | 1/1 | 1/1 | 0 each |
| Unit runner | Eight suites; 81 tests; 16314 assertions | Eight suites; 81 tests; 16302 assertions | 0 each |
| Scenarios | One feature; three scenarios; ten steps | One feature; three scenarios; ten steps | 0 each |
| Scenario dry run | Step matching passes | Published once | 0 |
| Isolated codec | Nine tests; 1690 assertions | Published once | Build 0; execution 0 |
| All repository reversals | 88/88 detected | 88/88 detected | Driver 0; restored build and test 0 |
| Instrumented suites | Pass with normal totals | Pass with normal totals | Configure, build, unit, and configured check 0 |
| Embedded source-list dispatch | Pass | Pass | 0 |
| Freestanding compilation | Seven sources | Seven sources | 0 each |
| Internal independent probe | 5934 checks; zero failures; zero observer gaps | Same | Build 0; execution 0 |
| External receive and replacement probes | Pass | Pass | Build 0; execution 0 each |
| External allocation sweep | 2289 checks; zero failures/live allocations | Same | Build 0; execution 0 |
| External original Flush probe | 532 checks; zero failures/live allocations | Same | Build 0; execution 0 |
| External interleaving probe | 48 cases; 6576 checks; zero failures/live allocations | Same | Build 0; execution 0 |
| External production-policy interleaving | 16 cases; Leave precedes Join throughout | Same | Build 0; execution 0 |
| External independent mutations | All three detected, including the two-tick delay | Same | Builds 0; checks 8; restored checks 0 |

Every new repository reversal compiles and fails its required named test in both profiles.
The complete campaigns also retain the address, LeaveAll scope, ordinary LV recovery, timer, queue, teardown, and profile reversals.
Return code 8 denotes the expected failing configured test for a planted behavioral defect.
Structural and compile-time reversals retain their documented expected failures.
No instrumentation error occurs on the unmodified source.

The internal plant campaign ran all 21 definitions per profile, unchanged.
It detects 35 of 42 executions.
The formerly surviving LV plants and source-error guard plant fail their required named tests in both profiles.
The reviewer-classified equivalent survivors remain: unguarded replacement timer in default mode, omitted redundant error assignment, and omitted transient value restoration.
The remaining two survivors omit the pre-existing Flush-to-LeaveAll request, a disclosed coverage gap.
The external campaign detects 13 of 14 plants per profile.
Its sole survivor removes rollback of an unchanged pending-transmit field, which the reviewer classified as equivalent.
The external script's name extractor returns empty lists; the receipts separately extract actual failing test names from its logs.
All plant configure, build, unit, and independent-probe return codes are recorded.

The three external independent mutation definitions were replayed unchanged.
Their original wrapper requires exactly 80 repository cases; a scratch wrapper bypassed that obsolete count assertion.
The full current 88-case campaign ran separately in both profiles.
No review packet or repository mutation definition was weakened.

Initial expanded execution exceeded the unit framework's assertion-message limit in one large test; rc 1.
Splitting that matrix by registration type preserved every case and resolved the harness limit.
A preliminary 87-case default campaign passed before the completed-flag reversal was added.
Both final 88-case campaigns pass.
The first full-range brace audit flagged the closing condition of a correctly braced do loop; rc 1.
Manual inspection confirmed the false positive. Correcting the scratch auditor produced rc 0 without changing repository source.
Generated import bytecode was removed before final integrity validation.

### Documentation, standards, and issue status

The local standard was converted to scratch text; rc 0.
No standard text was copied into the repository or output packet.
The normal Flush, LV recovery, and received LeaveAll behavior was checked against [IEEE 802.1Q-2018, clauses 10.7.5.2, 10.7.5.20, and Table 10-4](https://standards.ieee.org/ieee/802.1Q/6844/).
The pending flag is an allocation-recovery contract; it does not redefine ordinary table transitions.

| Page or interface | Change | Checks |
| --- | --- | --- |
| [README.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/README.md) | Updated unit counts. | All applicable checks pass; rc 0. |
| [doc/architecture.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/architecture.md) | Updated transmit source anchors. | All applicable checks pass; rc 0. |
| [doc/developer.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/developer.md) | Documented pending Flush, saved-value receive retry, observer continuity, and ordinary LV recovery. Updated the retry graph and source anchors. | All applicable checks pass; rc 0. |
| [doc/integrator.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/integrator.md) | Documented receive retry, indication order, observer reporting, and later LeaveAll behavior. | All applicable checks pass; rc 0. |
| [doc/manager.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/manager.md) | Updated Registrar and replacement claims, source anchors, and assertion counts. | All applicable checks pass; rc 0. |
| [doc/tester.md](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/doc/tester.md) | Updated fault matrices, observer coverage, counts, and reversal totals. | All applicable checks pass; rc 0. |
| [src/include/shish_lan/mrp.h](https://github.com/kebag-logic/lwSRP/blob/a29f8d13ff4869e54997d9adf05d83a4ace4b8bd/src/include/shish_lan/mrp.h) | Updated retained withdrawal and receive retry contracts without changing public signatures. | All applicable checks pass; rc 0. |

All five documentation commands pass.
There are 960 sentence fragments, zero long sentences, zero unlinked references, and 79 passing reference self-tests.
All 354 local links and 20 external URLs pass.
Repository links use authenticated access; other external links use anonymous access.
All 27 graphs render; the largest has 12 nodes.
The changed retry graph has eight actual nodes and was inspected at native size and page width.
Its labels are readable, no edge crosses a node, and its successful path clears pending state before the Leave indication.
All other graph sources are unchanged and were rendered again.
All 43 source anchors were mapped to the same named code lines and manually checked.
All 60 tracked files retain the licence identifier.
Whitespace, full-range braces, conflict markers, generated artifacts, file sizes, and private-residue checks pass; rc 0.

[Issue #6](https://github.com/kebag-logic/lwSRP/issues/6) remains fixed: the stream destination is the Nearest Bridge group address.
The authority is [IEEE 802.1Q-2018, clause 35.2.2.1 and Table 8-1](https://standards.ieee.org/ieee/802.1Q/6844/).
[Issue #7](https://github.com/kebag-logic/lwSRP/issues/7) remains fixed: received LeaveAll reaches only its message type on the ingress port.
The local standard check confirms that scope.
Their tests pass, and their address and all-types delivery reversals fail in both profiles.
Both issues remain open remotely; their closing links remain in the pull-request draft.

### Published commands and receipts

Every published shell command ran in the foreground, without a pipeline.
All 27 returned 0.
The exact command text, published location, and individual return codes appear in the command ledger.
No toolchain, package installation, virtual environment, rendered image, or file over 200 KB is in the checkout or output directory.

- [Commands, published commands, independent probes, and instrumentation](ROUND6-COMMANDS.json).
- [Default reversals, commands, and required failures](ROUND6-REVERSALS-OFF.json).
- [Enabled reversals, commands, and required failures](ROUND6-REVERSALS-ON.json).
- [Internal plants and individual return codes](ROUND6-PLANTS-INTERNAL-both.json).
- [External default plants and individual return codes](ROUND6-PLANTS-EXTERNAL-OFF.json).
- [External enabled plants and individual return codes](ROUND6-PLANTS-EXTERNAL-ON.json).
- [Detailed execution results, graphs, and source anchors](ROUND6-RESULTS.txt).
- [Evidence provenance](ROUND6-PROVENANCE.json).
- [Pull-request draft](PR-BODY.md).

Target execution and network interoperability remain unverified.
The [scenario assertion limitation](https://github.com/kebag-logic/lwSRP/issues/4) remains disclosed.
Review roles remain integration author, internal reviewer, and external reviewer.
The manager owns publication, independent review, pull-request updates, issue closure, and merge validation.
No existing issue or pull-request comment was edited or deleted.
No push, pull-request write, history rewrite, identity change, or delegated work occurred.
The final status comment is this round's only remote write.

Final integrity audit: rc 0. Parent, configured identity, one-line subject, and exact validated file contents match.
The worktree is clean, including ignored files.
No push was performed. New source links become available after manager publication.

[REVIEW READY](https://github.com/kebag-logic/lwSRP/issues/10#issuecomment-6035908183) posted with `a29f8d13ff4869e54997d9adf05d83a4ace4b8bd`; rc 0.

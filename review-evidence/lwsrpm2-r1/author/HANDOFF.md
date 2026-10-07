# Integration handoff

Status: Round 2 REVIEW READY. Local head 86a5f74c028dedec2a0f5bc1c5a258bbd83746b9; working tree clean; branch unpushed.
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

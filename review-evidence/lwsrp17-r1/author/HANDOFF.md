# [A584] lwsrp17 handoff — group same-type VectorAttributes into one Message per MRPDU

Status: REVIEW READY at the head below. Every acceptance item of #17 is met; all lwSRP gates rc 0; parent arms, documentation set and SRP plant campaign run at this head (findings for the pin bump below).

- Repository: https://github.com/kebag-logic/lwSRP, issue #17, assignment comment 6094124382.
- Branch: `lwsrp17-group` from main `9197193e` (local only: push and PR are not allowed in this lane).
- Head: `a44eeedf9abb0549b473acfb46eb910e99f397e1`
- Commits (configured identity, one-line subjects, no bodies or trailers):
  - `7674c28` Group same-type VectorAttributes into one Message per MRPDU
  - `04394a0` Add grouped-encoding goldens, an independent decoder and four planted defects
  - `2bf7b5a` Check decoded-event equivalence of every existing transmit opportunity
  - `aafcdd5` Document the grouped MRPDU layout, its checks and the new counts
  - `a44eeed` Pin the 65535-octet stream PDU bound with a test and a reversal
- 16 files changed, 1411 insertions, 66 deletions (`git diff --stat 9197193e..a44eeed`).

Clause references are IEEE 802.1Q-2018 (read from the local copy; no standard text is copied into the repository).

## Changes (file:line, clause)

| File:line | Change | Clause |
| --- | --- | --- |
| `src/core/mrp_mad.c:1290` `tx_header_len` | Message header: AttributeType + AttributeLength, plus the two-octet AttributeListLength for MSRP. | 10.8.1.2 c, 10.8.2.2–10.8.2.4, 35.2.2.6 |
| `src/core/mrp_mad.c:1296` `tx_vector_len` | One VectorAttribute: NumberOfValues 1 (one ThreePacked octet, plus one FourPacked octet for Listener) or 0 for the LeaveAll-only vector. Sizes identical to the old `tx_vector`. | 10.8.2.8 a/b/f, 10.8.2.10.1, 10.8.2.10.2, 35.2.2.7.2 |
| `src/core/mrp_mad.c:1303` `struct tx_types`, `:1308` `tx_type_in`, `:1313` `tx_type_add` | Two 256-bit stack bitmaps (64 octets): types with an open Message; types flagged LeaveAll. No heap, no new callback. | 10.8.2.2 (types 0–255) |
| `src/core/mrp_mad.c:1318` `tx_open`, `:1326` `tx_close` | Write the Message header; close the AttributeList with its EndMark and back-fill the MSRP AttributeListLength (list including its EndMark, as before). | 10.8.1.2 c/d, 10.8.2.9, 35.2.2.6 |
| `src/core/mrp_mad.c:1351` `tx_message` | One Message per AttributeType: the LeaveAll vector first when due (`:1359`: LeaveAll, NumberOfValues 0, zero FirstValue, unchanged form), then one single-value vector per selected value, placed in ascending FirstValue order (`:1379`: in-place adjacent swaps, `memcmp` over the FirstValue octets as an unsigned binary number). ThreePacked/FourPacked padding stays 0. | 10.8.1.2 d/e, 10.8.2.6, 10.8.2.7, 10.8.2.8 f, 10.8.2.10.1, 10.8.2.10.2, 35.2.2.7.2 |
| `src/core/mrp_mad.c:1388` `tx_assemble` | ProtocolVersion, then the Messages in ascending AttributeType order (`:1394`), then one MRPDU EndMark (`:1405`). | 10.8.1.2 a/b |
| `src/core/mrp_mad.c:1410` `mrp_transmit` (selection `:1425`–`:1491`) | Selection keeps its order and rules: LeaveAll preamble for types 1..last, then omitted values, then repeats, in list order; a value that does not fit is deferred and `full` stops repeats. Only the cost changes: the first vector of a type pays its Message header and EndMark (`:1464`). Nothing is written until selection ends. MSRP storage is clamped to 65535 octets (`:1430`) so no AttributeListLength can wrap. | 10.8.3.1 a/b; 10.7.5.7–10.7.5.9 (tx!, txLA!, txLAF! unchanged); 10.8.2.4 |
| `src/include/shish_lan/mrp.h:258` | `mrp_transmit` contract: grouped layout, buffer sizing, 65535-octet MSRP reach. | 10.8.1.2, 10.8.2.4 |
| `CMakeLists.txt:71` | Unit target adds `grouping_test.c` and `mrpdu_decoder.c`. | — |
| `tests/unit/main.c` | Runs `grouping_suite` (nine suites). | — |
| `tests/unit/mrpdu_decoder.{c,h}` | Test-side decoder from 10.8.1.2/10.8.2; no code or header shared with `src/core/mrp_pdu.c`. Its only application facts: MSRP carries AttributeListLength and FourPacked on type 3 (35.2.2.6, 35.2.2.7.2). Rejects reserved LeaveAllEvent (10.8.2.6), events above 5 (10.8.2.5), incomplete vectors (10.8.3.4 b), zero type or length, empty AttributeLists (10.8.1.2 d); counts explicit EndMarks and trailing octets. | 10.8.1.2, 10.8.2.5–10.8.2.10, 10.8.3.4 |
| `tests/unit/grouping_test.c` | 15 tests (below). | — |
| `tests/unit/transmit_trace.c` | Preloadable trace: wraps `mrp_transmit` and the host send callback, decodes each offered PDU with the test-side decoder, keys records by the running unit-test name. | — |
| `tests/check_equivalence.py` | Builds the base revision's own unit suite against base sources and against this checkout's sources, runs both under the trace, compares every opportunity, and checks the grouped form. | — |
| `tests/check_reversals.py` | Five grouping reversals with named required failures (99 cases). | — |
| `README.md`, `doc/*.md` | Layout section and graph (developer), sizing (integrator), status row (manager), grouping and equivalence sections, counts (tester), anchors `mrp_mad.c#L1323` → `#L1410`. | — |

Design notes for review:
- Event and state-machine semantics are untouched: `appl_table`, `reg_table`, `appl_event`, `reg_event`, the commit loop (tx!, txLA!, txLAF!, local rLA!, owed periodic, join timer) and the retained-PDU retry path are the same code. Only the layout of the selected vectors and the room each one costs changed.
- Grouping saves the header and EndMark of every further value of a type (6 octets for MSRP, 4 for MVRP/MMRP), so more values can fit at a boundary: a 1500-octet MSRP PDU holds 124 Listener vectors, 83 before. No existing scenario reaches a boundary where this changes the selected set (equivalence table).
- An `encode_attr` length error now surfaces after selection instead of mid-selection; it still returns `-SHLAN_ERROR_INVALID` and commits nothing. Unreachable for the three built-in applications (unknown types have `attr_len` 0 and are deferred before encoding).
- LeaveAll keeps today's form: its own NumberOfValues-0 vector per type (all types 1..last), now first inside that type's Message rather than a Message of its own. Per type, LeaveAll still precedes that type's values (10.8 NOTE 2). Across types, a receiver now meets LeaveAll(type n+1) after type n's values; LeaveAll applies only to its own type (10.8.2.6), so decoded events per type are unchanged.
- Ordering is an in-place insertion: O(n²) octet swaps in the worst case (about 92 000 for 124 Listener values in descending list order), no scratch buffer, no `memmove`.
- Order follows the wire FirstValue (Domain: SRclassID first, so class B (5) precedes class A (6)).
- MSRP storage above 65535 octets is no longer used (previously such a buffer could produce a PDU above 65535 octets; never reachable in an Ethernet frame).

## Tests and the planted defect each catches

`tests/unit/grouping_test.c` (102 tests in the runner, was 87):

| Test | What it pins |
| --- | --- |
| `two_listener_values_share_one_message` | Golden G1 (33 octets): two Listener New/Ready values in one Message, ascending. |
| `domain_classes_share_one_message_in_ascending_order` | Golden G2 (23 octets): Domain class B then class A, JoinMt, one Message. |
| `talker_and_listener_messages_follow_attribute_type_order` | Golden G3 (95 octets): interleaved declarations become a Talker Advertise Message (2 vectors) then a Listener Message (2 vectors). |
| `leaveall_flags_every_stream_type_including_empty_ones` | Golden G4 (118 octets): LeaveAll on types 1–4; types 1, 2 and 4 empty; type 3 has its LeaveAll vector then the Listener value. |
| `vlan_leaveall_message_carries_the_declared_vectors` | Golden G5 (21 octets, MVRP): LeaveAll vector, then VID 2 and VID 3 (Mt) in one Message, no AttributeListLength. |
| `a_message_that_fits_exactly_is_not_split` | G1 at capacity exactly 33: one MRPDU (the per-value form needed 39). |
| `one_octet_short_moves_a_vector_to_a_second_pdu` | Goldens G6/G7 (21 octets each): at capacity 32 the newest value goes first and the omitted one leads the next MRPDU. |
| `an_ethernet_mtu_carries_124_listener_vectors_in_one_message` | Golden G8 (1497 octets, built in the test from the 10.8 layout): 125 Listener values at capacity 1500 give 124 vectors (uids 2–125) in one Message; uid 1 leads the next PDU (124 vectors, graded). |
| `stream_pdus_stop_at_the_attribute_list_length_reach` | 2400 Talker values at capacity 131072: one PDU of 65529 octets, AttributeListLength 65522, 2340 ascending vectors, EndMarks; one more vector would need 65557. |
| `every_stream_pdu_keeps_one_ordered_message_per_type` | Sweep: MSRP (Talker Advertise, Talker Failed, Listener, Domain, withdrawals), capacities 1500/200/140/120, 160 opportunities over two LeaveAll periods; each PDU graded by the decoder (one Message per type, ascending types, LeaveAll first and on all types or none, NumberOfValues 1 otherwise, strictly ascending FirstValue, EndMarks = Messages + 1, no trailing octets). |
| `every_vlan_and_mac_pdu_keeps_one_ordered_message_per_type` | The same sweep for MVRP and MMRP. |
| `received_values_in_separate_messages_register` | Receive path, one Message per value (MSRP Listener ×2 and Domain ×2; MVRP VID ×2). |
| `received_values_grouped_in_one_message_register` | Receive path, grouped form. |
| `received_values_packed_in_one_vector_register` | Receive path, "+k" packed (NumberOfValues 2: Listener uid +1, Domain class and priority +1 (35.2.2.8, 35.2.2.9), VID +1). |
| `test_decoder_reads_the_three_forms_and_rejects_bad_ones` | Decoder self-check: all three forms, packed events and FourPacked types, implicit final EndMark (10.8.1.2 f), rejection of event 216, reserved LeaveAllEvent, a truncated vector and an empty AttributeList. |

Planted defects (`tests/check_reversals.py`; each must compile, fail CTest and fail its named tests). Counts are from the final campaigns; both profiles identical.

| Case | Plant | Required named tests | Tests it fails |
| --- | --- | --- | --- |
| `grouped-message-split` (split Message) | close and reopen the Message after every vector | `two_listener_values_share_one_message`, `every_stream_pdu_keeps_one_ordered_message_per_type` | 11 |
| `grouped-endmark-count` (wrong EndMark count) | omit the MRPDU EndMark (still parses, 10.8.1.2 f) | `two_listener_values_share_one_message`, `every_vlan_and_mac_pdu_keeps_one_ordered_message_per_type` | 11 |
| `grouped-vector-order` (wrong vector order) | `> 0` → `< 0` in the FirstValue insertion | `two_listener_values_share_one_message`, `domain_classes_share_one_message_in_ascending_order` | 9 |
| `grouped-dropped-vector` (dropped vector) | skip the list-tail value while still committing it | `two_listener_values_share_one_message`, `an_ethernet_mtu_carries_124_listener_vectors_in_one_message` | 13 (3 of them existing transmit tests) |
| `grouped-list-length-reach` (extra) | remove the 65535-octet clamp | `stream_pdus_stop_at_the_attribute_list_length_reach` | 1 |

## Decoded-equivalence table per scenario

`tests/check_equivalence.py` (base `9197193e`): the base revision's own unit suite, once with base sources and once with this head's sources, both under the trace. Same table with `--milan OFF` and `--milan ON`, at `2bf7b5a` and at the head, and under CPython 3.12.3.

| Scenario | Opportunities | PDUs | Byte-identical | Layout-only | Different |
| --- | --- | --- | --- | --- | --- |
| fresh_ladder_and_refusal_are_transactional | 7 | 4 | 4 | 0 | 0 |
| refused_pdu_survives_timers_without_aging_unsent_leaveall | 4 | 4 | 3 | 1 | 0 |
| receive_redeclare_requests_transmission_without_periodic_wait | 5 | 4 | 4 | 0 | 0 |
| a_full_pdu_retries_omitted_attributes_before_repeats | 5 | 5 | 0 | 5 | 0 |
| changed_listener_redeclares_from_a_quiet_applicant | 4 | 4 | 4 | 0 | 0 |
| periodic_is_one_second_independent_of_join_time | 7 | 4 | 4 | 0 | 0 |
| registrar_ages_while_a_transmission_is_retained | 2 | 2 | 2 | 0 | 0 |
| applicant_declaration_recovery_and_withdrawal_follow_the_table | 3 | 3 | 3 | 0 | 0 |
| applicant_receive_conditions_follow_link_mode | 2 | 2 | 2 | 0 | 0 |
| transmitted_leaveall_includes_every_supported_type | 1 | 1 | 1 | 0 | 0 |
| transmitted_leaveall_keeps_the_ieee_deadline | 1 | 1 | 1 | 0 | 0 |
| retained_ports_replay_propagated_join_and_timer_leave_in_order | 8 | 8 | 7 | 1 | 0 |
| queued_propagation_owns_values_and_survives_source_reclamation | 2 | 2 | 2 | 0 | 0 |
| committed_leaveall_delivers_local_receive_and_omitted_events | 3 | 3 | 0 | 3 | 0 |
| full_leaveall_reports_each_required_transition | 3 | 3 | 0 | 3 | 0 |
| leaving_observer_is_retained_until_its_pending_transmission | 1 | 1 | 1 | 0 | 0 |
| changed_values_after_transmitted_leaveall_are_indicated_and_propagated | 4 | 4 | 4 | 0 | 0 |
| reservation_failure_is_reported_without_partial_publication | 2 | 0 | 0 | 0 | 0 |
| failed_commit_replay_is_retried_by_the_next_poll | 3 | 2 | 2 | 0 | 0 |
| destroy_releases_all_queued_allocations | 1 | 1 | 1 | 0 | 0 |
| replacement_allocation_failures_keep_leave_before_join | 40 | 40 | 40 | 0 | 0 |
| replacement_from_lv_keeps_leave_before_join_at_every_allocation | 40 | 40 | 40 | 0 | 0 |
| **Total (22 scenarios)** | **148** | **138** | **125** | **13** | **0** |

"Different" compares the multiset of decoded events (LeaveAll per type; type, FirstValue, offset, AttributeEvent and FourPackedType per value) and the send result. Every opportunity also has the same `mrp_transmit` result and number of sends, and every new PDU passes the grouped-form check. The other 65 base unit tests make no transmit call. The three behave scenarios make none either (run under the trace: no record). The two boundary scenarios that matter (`a_full_pdu_…`, 80-octet buffer; `committed_leaveall_…`/`full_leaveall_…`, 20-octet buffer under LeaveAll) select the same values with grouped costs, so their decoded events match.

Negative controls (scratch copies, not committed): with the `grouped-dropped-vector` plant the check reports 40 different and 35 not-grouped opportunities (rc 1); with the `grouped-message-split` plant 132 and 132 (rc 1).

## Goldens

| Id | Test | Octets | Content |
| --- | --- | --- | --- |
| G1 | `two_listener_values_share_one_message`, `a_message_that_fits_exactly_is_not_split` | 33 | `00` · `03 08 00 1a` · `00 01 <sid …00:00> 00 80` · `00 01 <sid …00:01> 00 80` · `00 00` · `00 00` |
| G2 | `domain_classes_share_one_message_in_ascending_order` | 23 | `00` · `04 04 00 10` · `00 01 05 02 00 02 6c` · `00 01 06 03 00 02 6c` · `00 00` · `00 00` |
| G3 | `talker_and_listener_messages_follow_attribute_type_order` | 95 | `01 19 00 3a` + 2 × 28-octet Talker vectors (uid 0, 1) + `00 00`, then `03 08 00 1a` + 2 Listener vectors (uid 0, 1) + `00 00`, then `00 00` |
| G4 | `leaveall_flags_every_stream_type_including_empty_ones` | 118 | `01 19 00 1d 20 00 0×25 00 00` · `02 22 00 26 20 00 0×34 00 00` · `03 08 00 18 20 00 0×8 00 01 <sid> 00 80 00 00` · `04 04 00 08 20 00 0×4 00 00` · `00 00` |
| G5 | `vlan_leaveall_message_carries_the_declared_vectors` | 21 | `00` · `01 02` · `20 00 00 00` · `00 01 00 02 90` · `00 01 00 03 90` · `00 00` · `00 00` |
| G6, G7 | `one_octet_short_moves_a_vector_to_a_second_pdu` | 21 each | capacity 32: `00 03 08 00 0e 00 01 <sid …00:01> 00 80 00 00 00 00`, then the same with `<sid …00:00>` |
| G8 | `an_ethernet_mtu_carries_124_listener_vectors_in_one_message` | 1497 | `00 03 08 05 d2`, 124 × `00 01 02 00 00 00 00 20 <uid> 00 80` (uids 2–125), `00 00 00 00` |
| G9 | `stream_pdus_stop_at_the_attribute_list_length_reach` (structural) | 65529 | `00 01 19 ff f2`, 2340 × Talker vectors (uids 0–2339 ascending), `00 00 00 00` |

Stream identities are locally administered (`02:00:00:00:00:xx`); no device-specific values.

## Gates (lwSRP, at `a44eeed`)

Toolchain: GCC 16.2.1, CMake 4.4.4, cgreen 1.7.0 (scratch prefix), Python 3.14.7 and CPython 3.12.3, behave from the user environment, Mermaid CLI.

| Gate | Command (scratch paths elided) | Result |
| --- | --- | --- |
| Configure/build, default | `cmake -S . -B "$LWSRP_BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=OFF`, `cmake --build "$LWSRP_BUILD" --parallel 2` | rc 0, 0 warnings |
| CTest, default | `ctest --test-dir "$LWSRP_BUILD" --output-on-failure` | rc 0, 1/1 |
| Unit runner, default | `"$LWSRP_BUILD/unit_tests"` | rc 0, 102 tests, 26658 assertions, 0 failures |
| Configure/build/CTest/unit, Milan | same with `-DLWSRP_MILAN=ON` | rc 0 each, 0 warnings, 26646 assertions |
| Scenarios, both builds | `SHLAN_LIBRARY=… behave` | rc 0, 3 scenarios / 10 steps passed |
| Scenario dry run | `behave --dry-run` | rc 0 |
| Freestanding | `python3 tests/check_freestanding.py`; `CC="cc -DLWSRP_MILAN=1" python3 tests/check_freestanding.py` | rc 0, 7 sources, 0 failures (each) |
| Embedded | `python3 tests/check_embedded.py --work-dir "$EMBEDDED_SCRATCH"` | rc 0 |
| Reversals, default | `python3 tests/check_reversals.py --work-dir … --prefix "$CGREEN_PREFIX"` | rc 0, 99 reversals, 0 failures |
| Reversals, Milan | same with `--milan ON` | rc 0, 99 reversals, 0 failures |
| Equivalence, both profiles | `python3 tests/check_equivalence.py --work-dir … --prefix "$CGREEN_PREFIX" [--milan ON]` | rc 0, 0 different, 0 problems |
| Equivalence, CPython 3.12.3 | same, default profile | rc 0 |
| Sentences / references / self-test | `python3 doc/tools/check_sentences.py`, `check_references.py`, `check_references.py --self-test` | rc 0 (1012 sentences; 0 unlinked; 79 cases); also rc 0 under 3.12.3 |
| Links | `python3 doc/tools/check_links.py --github-auth` | rc 0, 366 local, 21 external, 0 failures |
| Graphs | `python3 doc/tools/render_mermaid.py --output "$DOC_SCRATCH/graphs"` | rc 0, 28 graphs; new layout graph reviewed as PNG |
| Strict compile | `gcc`/`clang -O2 -std=c11 -Wall -Wextra -Wpedantic -Werror -c src/core/mrp_mad.c` | rc 0 each |

Size and stack (RV32, from the parent's `srp-rv32` arm objects): `mrp_mad.o` text 12709 → 13309 octets (+600), data 140 and bss 0 unchanged; `mrp_transmit` static frame 96 → 192 octets (helpers inlined, includes the 64-octet bitmaps; the old `tx_vector` frame of 80 is gone); the largest static frame of the SRP set is unchanged at 256 octets; all frames remain `static`. Host x86-64 `-O2`: `mrp_transmit` 176 (dynamic, bounded) → 304 (static).

## Parent consumer (milan-fpga `dev` `554e61d2`, gitlink at this head)

Scratch clone, submodules initialised (`external` `efeb541a`, `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845`, `third_party/verilog-axis` `48ff7a7e`). `third_party/lwSRP` was fetched from the local branch and checked out at `a44eeed` (toplevel verified before each submodule git command); the gitlink is staged in the scratch index only. Nothing was committed or pushed.

Runs (`python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4`, local RV32 SDK, system GoogleTest 1.18):

| Run | lwSRP | Arms | GoogleTest cases | Failures | Result |
| --- | --- | --- | --- | --- | --- |
| Baseline | `9197193e` (pin) | 59 ok | 1191 | 0 | PASS |
| Candidate | `aafcdd5` (same `src/` as the head) | 59 ok | 1191 | 0 | PASS |
| Final | `a44eeed` | 59 ok | 1191 | 0 | PASS (per-arm verdicts identical to baseline) |

The F4 SRP set inside those 59: `lwsrp`; `srp_mbx`, `debug`, `srp_rx_retry`, `srp_app`, `test_acmp_mbx` (SRP), `srp_latency` and `srp_walk` (processor wire comparison) at one and two interfaces; `srp_shape` and `srp-rv32` for all five shipped shapes at one and two interfaces: 35 arms, 291 cases, 0 failures, unchanged. The candidate needed one scratch edit to run at all: `ctrl_arms.LWSRP_REV` (without it the pin check refuses: "lwSRP at … is not the pinned 9197193e…").

Documentation set (14 gates: `docs_check.py`, `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py`, `DOC_MAP.gen.py --check`, `timesync_chain.gen.py --check`, `check_solution_docs.py`, `submodule_boundaries.gen.py --check`, `check_submodule_docs.py` (+ `--selftest`), `check_diagram_pngs.py`, `check_feature_status.py --self-test`, `gen_module_matrix.py --check`, `check_doc_paths.py`):

| Run | Result |
| --- | --- |
| Baseline (pin) | 14/14 rc 0 |
| Head, gitlink only | 12/14: `submodule_boundaries.gen.py --check` ("diagram stale") and `check_submodule_docs.py` ("documented pin differs from Git") rc 1 |
| Head, gitlink + `SUBMODULES.md` row + regenerated diagram | 14/14 rc 0 |

### Byte-level SRP expectations in milan-fpga (input to the pin bump)

| File:line (at `554e61d2`) | Expectation | At `9197193e` | At this head | Pin-bump action |
| --- | --- | --- | --- | --- |
| `sw/firmware/ctrl/test/srp_latency.cpp:68-77` (skip at `:76-77`) | The LeaveAll detector walks an MVRP Message by skipping `2 + width + ⌈n/3⌉ + 2` octets, i.e. assumes exactly one VectorAttribute per MVRP Message. | Exact: LeaveAll and each VID were separate Messages. | Grouped MVRP Messages hold the LeaveAll vector and the VIDs together. The walk reads the second vector's FirstValue as a type-0 Message (NumberOfValues 4096/3072) and runs past the frame end. With the arm's single VID the verdict is still right, by accident (the arm passes). With two VIDs in a non-LeaveAll PDU, a JoinMt octet (`0x6c`) is read as a LeaveAll flag: a false LeaveAll. Reproduced in scratch on real lwSRP output for 1 and 2 VIDs. | Walk every VectorAttribute up to the AttributeList EndMark (diff below). Tested in scratch at the head: `srp_latency` arm passes at one and two interfaces; the fixed walk ends exactly on the MRPDU EndMark for both layouts and gives the right verdict in all three reproduced PDUs. |
| `sw/firmware/ctrl/test/srp_latency.cpp:72`, `:74-75` (MSRP branch) | Skips a Message by AttributeListLength; LeaveAll read on each Message's first vector. | Exact. | Exact (LeaveAll vector is still first in each Message). | None. |
| `sw/firmware/ctrl/test/srp_fixture.hpp:76-128` `capture()` | Generic decoder: walks every vector to the EndMark, uses AttributeListLength, applies "+k". | Exact. | Exact (exercised by the passing `srp_mbx`, `srp_feedback`/`test_acmp_mbx`, `srp_walk` arms). | None. |
| `sw/firmware/ctrl/srp/srp_mbx.c:521` | Licences a VID from the committed MVRP PDU with lwSRP's own `mrpdu_parse`. | Exact. | Exact (the parser accepts every 10.8 form). | None. |
| `sw/firmware/ctrl/srp/srp_mbx.c:800` | Transmit storage `sizeof(m->frame) - 14`. | 83 Listener values per 1500-octet PDU. | 124 per 1500-octet PDU; no shipped shape comes near either bound. | None. |
| `sw/firmware/ctrl/test/ctrl_arms.py:362` (and comment `:359`) | `LWSRP_REV` pin. | — | Refusal until updated. | Set to the new SHA. |
| `docs/reference/SUBMODULES.md:26` | Documented pin. | — | `check_submodule_docs.py`: documented pin differs from Git. | Set to the new SHA. |
| `docs/diagrams/submodule_boundaries.svg:72` (+ `.drawio`, `.png`, `docs/diagrams/PNG_MANIFEST.json`) | Generated pin label `pin 9197193e47a6`. | — | `submodule_boundaries.gen.py --check`: stale. | Regenerate with `python3 docs/diagrams/submodule_boundaries.gen.py` (at this head: svg label `pin a44eeedf9abb`, two manifest hashes change, PNG 380516 → 380194 octets, sha256 `a3ddf7ab087a47a0ca73d33986a1f75bf81f97aa5ff36d9aa726e36fd15e3b1b`). |
| `sw/firmware/ctrl/README.md:340`, `sw/firmware/ctrl/srp/README.md:292`, `:343`, `docs/design/MAILBOX_SPLIT.md:295` | Prose pin mentions. | — | Not gated. | Update with the pin. |
| `sw/firmware/ctrl/srp/README.md:75-76` | Permalinks `doc/integrator.md#L321-L323` and `src/include/shish_lan/mrp.h#L288-L290` at `9197193e`. | — | Still valid (old SHA). If moved to the new SHA the same text is at `doc/integrator.md#L324-L326` and `src/include/shish_lan/mrp.h#L292-L294`. | Optional. |

No other parent test or document hard-codes transmitted MSRP/MVRP octets. The processor's own SRP encoder (`protocol-processor`) is not affected.

Proposed `srp_latency.cpp` change (tested in scratch, not committed):

```diff
                 if(!mvrp) off=end;
-                else { const unsigned n=wire_be16(f->bytes+off)&8191u;
-                       off+=2+width+(n+2)/3+2; }
+                else { // 802.1Q 10.8.1.2 d: every vector up to the EndMark.
+                       while(off+2<=f->len && (f->bytes[off] || f->bytes[off+1])) {
+                           const unsigned n=wire_be16(f->bytes+off)&8191u;
+                           off+=2+width+(n+2)/3;
+                       }
+                       off+=2; }
```

### Parent SRP plant campaign

The SRP part of the parent's `--self-test`, run at `a44eeed` with the parent's own `srp_mutants.campaign` and `ctrl_mutants.lwsrp_pin_arms` (scratch driver, same calls and subset filter as `test_ctrl_firmware.py`; the ADP/ACMP/MAAP/AECP campaigns do not involve lwSRP and were not run):

| Part | Defects | Caught | Escaped |
| --- | --- | --- | --- |
| Full SRP table, two interfaces | 169 | 169 | 0 |
| One-interface subset (four-way, binding, feedback, r10, p11, bound, term, poll/send extra) | 68 | 68 | 0 |
| Pin refusal: one compiled source edited; another revision checked out | 2 | 2 | 0 |

Verdict: `srp campaign: PASS`, rc 0.

## Open points

- Push, PR creation and the parent pin bump are outside this lane; PR-BODY.md is ready.
- The parent's `srp_latency.cpp` walker should change with the pin bump (above); it passes today only because the arm declares one VID.
- LeaveAll keeps the separate NumberOfValues-0 vector per type ("as today"). If the interoperability baseline is later found to flag LeaveAll on the first declared vector instead, that is a separate, decoded-equivalent change.

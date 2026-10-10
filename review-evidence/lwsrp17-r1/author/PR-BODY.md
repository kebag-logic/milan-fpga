[A584] Group same-type VectorAttributes into one Message per MRPDU

Closes #17

## What changes

`mrp_transmit` now writes one Message per AttributeType in each MRPDU (IEEE 802.1Q-2018 10.8.1.2):

- Messages follow ascending AttributeType order. Each ends with one EndMark, and one more ends the PDU.
- Inside a Message, a due LeaveAll keeps today's form and is flagged per type (its own NumberOfValues-0 vector, first). One single-value VectorAttribute per declaration follows, in ascending FirstValue order (10.8.2.7).
- NumberOfValues stays 1 and there is no "+k" packing. Event and state-machine semantics are unchanged: the Applicant and Registrar tables, the commit loop (tx!, txLA!, txLAF!, local rLA!) and the retained-PDU retry path are the same code.
- Selection keeps its order and rules (LeaveAll preamble, omitted values, then repeats). Only the room a value costs changes: the first vector of a type pays the Message header and EndMark, so a value moves to a second MRPDU only when it no longer fits.
- Bare metal: no heap and no new callbacks; 64 octets of stack bitmaps and an in-place insertion for the order. MSRP storage is capped at 65535 octets so AttributeListLength cannot wrap.

MSRP, MVRP and MMRP share the writer. The receive parser is unchanged.

## Evidence

- Byte-exact goldens (`tests/unit/grouping_test.c`): two Listener values in one Message; Domain class B and class A together; mixed Talker Advertise and Listener; empty types under LeaveAll and a VLAN Message under LeaveAll; a capacity that fits exactly (no split), one octet short (a second MRPDU), a 1500-octet PDU with 124 Listener vectors, and the 65535-octet bound.
- Sweeps grade every PDU of all three applications over four capacities and two LeaveAll periods. The grader is a test-side decoder written from 10.8.1.2 and 10.8.2 (`tests/unit/mrpdu_decoder.c`); it shares no code with `src/core/mrp_pdu.c`.
- The receive path accepts all three valid encodings (one Message per value, grouped, and "+k" packed), one named test each.
- Decoded equivalence (`tests/check_equivalence.py`): the base `9197193e` unit suite runs against the base and the new sources under a trace that decodes every offered PDU. 22 transmitting scenarios, 148 opportunities and 138 PDUs: 125 byte-identical, 13 layout-only, 0 with different decoded events, in both Registrar profiles.
- Planted defects in `tests/check_reversals.py`, each failing its named tests: a split Message, a wrong EndMark count, a wrong vector order and a dropped vector, plus the removed 65535-octet bound.

| Check | Default profile | Milan profile |
| --- | --- | --- |
| Configure, build (no warnings), CTest | 0 | 0 |
| Unit runner, 102 tests | 0; 26658 assertions | 0; 26646 assertions |
| Scenarios (3 scenarios, 10 steps) | 0 | 0 |
| Scenario dry run | 0 | — |
| Equivalence check | 0; 0 different | 0; 0 different |
| Reversals (99) | 0; 0 survived | 0; 0 survived |
| Freestanding check | 0 | 0 |
| Embedded check (both profiles) | 0 | — |
| Documentation checks (sentences, references, self-test, links, graphs) | 0 | — |

## Downstream

The parent firmware pins this library. Its firmware arms (including every SRP arm and the processor wire comparison) and its documentation set were run against this head; nothing was committed there.

- Arms: 59 of 59 pass with 1191 cases, the same verdicts as at the current pin.
- Its SRP planted-defect campaign catches all 237 defects, and both pin-refusal checks pass.
- The documentation set passes once the pin bump updates its submodule table and regenerates the boundary diagram.
- One parent test helper walks MVRP Messages as if each held a single vector. It still passes with one VLAN, but grouped Messages need a vector walk; a tested replacement is ready for the pin bump.

# Proposed implementation tickets

Draft work contracts from the #500 design lane, revised by A152 after the
R217 and R218 round-one reviews, by A153 after their round-two reviews and
by A154 after their round-three reviews. They authorize no implementation.

| Draft | Destination | State |
|---|---|---|
| T1 processor stage 1 | processor repository, not filed | opens after the #500 contract and its amendment are accepted, on T8 and T9; its roll-back resets the dynamic-state store AND the descriptor store; declared shippable only after #502 |
| T2 processor stage 2 | processor repository, not filed | after T1 (whose roll-back already resets the descriptor store); declared shippable only after #502 |
| T3 processor stage 3 | processor repository, not filed | BLOCKED on #501; the pending-and-skip rule is containment, not persistence |
| T4 parent, per stage | kebag-logic/milan-fpga, not filed | the release conditions of each stage, and the firmware changes |
| T5 output-map capacity | kebag-logic/milan-fpga #501 | open; blocks stage 3 |
| T6 pending from the live write | kebag-logic/milan-fpga #502 | open; blocks every stage declared shippable |
| T7 area table refresh | kebag-logic/milan-fpga #495 checklist | documentation |
| T8 port cause, bounded binding walk and the listener's admission | processor repository, a new issue referencing issues 15 and 20, not filed | PREREQUISITE of stage 1 and of every shippable stage (seams S1, S3, S4); closes and amends neither issue; claims no reuse of a port whose device never answers |
| T9 descriptor memory response isolation | processor repository, a new issue, not filed | PREREQUISITE of stage 1 and of every shippable stage (seam S2); also closes a pre-existing exposure of ordinary AECP service |

The executable evidence these drafts cite is the commit the design page
names; a later commit that edits only these drafts changes no measured
source, result or digest.

# Proposed implementation tickets

Draft work contracts from the #500 design lane, revised by A152 after the
R217 and R218 round-one reviews. They authorize no implementation.

| Draft | Destination | State |
|---|---|---|
| T1 processor stage 1 | processor repository, not filed | opens after the #500 contract and its amendment are accepted; declared shippable only after #502 |
| T2 processor stage 2 | processor repository, not filed | after T1; declared shippable only after #502 |
| T3 processor stage 3 | processor repository, not filed | BLOCKED on #501; the pending-and-skip rule is containment, not persistence |
| T4 parent, per stage | kebag-logic/milan-fpga, not filed | the release conditions of each stage, and the firmware changes |
| T5 output-map capacity | kebag-logic/milan-fpga #501 | open; blocks stage 3 |
| T6 pending from the live write | kebag-logic/milan-fpga #502 | open; blocks every stage declared shippable |
| T7 area table refresh | kebag-logic/milan-fpga #495 checklist | documentation |
| T8 port deadline | processor issue 15, as an addendum | bounds the binding walk; not needed for the D3 containment |

The executable evidence these drafts cite is the commit the design page
names; a later commit that edits only these drafts changes no measured
source, result or digest.

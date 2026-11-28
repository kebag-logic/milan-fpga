Status: REVIEW READY for the round-8 ledger and inventory change. Local head `701f294405d47a81eed1079d32b54e1eea4a4f31`.

The new USB-network ledger point follows the [ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7234489667); existing points and owner bounds are unchanged. All 159 retained traces across eight images regrade identically, and the new point's ledger qualification passes without a new or larger miss. The seven known held-egress service-budget misses remain recorded.

| Check | Result | Bound or figure |
|---|---:|---:|
| Load | 0.501397114035 | 0.70 |
| ACMP | 29.84000 ms | 30 ms |
| txL | 48.90000 ms | 49 ms |
| Last notice | 117.58000 ms | 140 ms |
| THE SHARE | 1.7923875 ms | 2 ms |
| Complete wire egress | 644.980750 us | 1000 us |
| USB held AECP last delivery | 62.03635 ms | 62.14 ms |

The 62.03635-versus-61.99 failure is preserved at the original Arty point. One cycle above 62.14 fails at the USB point; the exact figure passes. The ledger self-test catches all 25 mutations. Fourteen focused final-head gates pass, including documentation, contents and generated-inventory checks. The inventory regeneration is a separate commit.

Arty and both ALINX ELF/map-header identities remain exact at #1004's same pins. Firmware, RTL, queue model and scheduling costs are unchanged. All other thirteen dependency files remain byte-identical. Full receipt bindings, controls and boundaries are in [HANDOFF-r8.md](HANDOFF-r8.md) and [receipts](receipts/INDEX.md).

This is executor evidence for the requested desk scope, not an independent review verdict or whole-issue completion. Physical-route, attachment and board acceptance remain open. Nothing was pushed, posted, flashed or run on the bench.

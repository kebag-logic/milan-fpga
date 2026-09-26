[A328] BASELINE REFERENCE — #231

Measured RTL: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`; committed baseline: `af6d19c553ad8c445a80528344baf2273b41ad46`.

Baseline page: [resource and timing baseline](https://github.com/kebag-logic/milan-fpga/blob/af6d19c553ad8c445a80528344baf2273b41ad46/docs/findings/PP_SHADOW_BASELINE.md). Recipe: [reproduction commands](https://github.com/kebag-logic/milan-fpga/blob/af6d19c553ad8c445a80528344baf2273b41ad46/docs/testing/PP_SHADOW_BASELINE_RECIPE.md). Inputs: [parameters and image hashes](https://github.com/kebag-logic/milan-fpga/blob/af6d19c553ad8c445a80528344baf2273b41ad46/docs/findings/PP_SHADOW_BASELINE_INPUTS.json).

The commit is local under the assignment's no-push instruction; those file links become available when the maintainer publishes it. The measured reference values are public here now:

| Measurement | LUT | FF | RAMB36 / RAMB18 | DSP | CARRY4 | WNS ns |
|---|---:|---:|---:|---:|---:|---:|
| Vivado OOC product 1x1, 100 MHz | 22,350 | 24,533 | 21 / 3 | 5 | 1,415 | -6.180 |
| Vivado OOC product 8x8, 100 MHz | 28,992 | 32,984 | 26 / 5 | 5 | 1,775 | -10.987 |
| Vivado shipping 1x1 route, whole SoC | 48,618 | 57,854 | 79 / 27 | 11 | 3,203 | +0.013 |
| Vivado shipping 1x1 route, wrapper | 22,441 | 23,493 | 21 / 3 | 5 | 1,361 | +0.013 |
| Vivado integrated 8x8 synthesis, whole SoC | 68,136 | 70,835 | 80 / 29 | 11 | 3,916 | -11.331 |
| Vivado integrated 8x8 synthesis, wrapper | 37,809 | 31,391 | 26 / 5 | 5 | 1,803 | -10.594 |
| Yosys OOC product 1x1 | 47,230 | 23,041 | 15 / 4 | 5 | 1,813 | Not measured |
| Yosys OOC product 8x8 | 71,860 | 32,615 | 16 / 4 | 7 | 2,108 | Not measured |

Product labels count audio streams; the processor includes CRF and therefore has 2/2 or 9/9 stream contexts. The integrated clocks are 50 MHz and 100 MHz. All 20 standalone parameters and 120 source reads match the corresponding integrated export. Vivado is 2026.1 build 6511674; Yosys reports 0.66 / 86f2ddebc-dirty with sv2v 0.0.13.

SRP drives most standalone scaling: 4,296 to 8,302 LUTs. AECP is 4,663 / 5,053 LUTs standalone, while integrated 8x8 AECP is 15,199 LUTs; these synthesis contexts must remain distinct. The baseline records complete hierarchy resources and scoped internal timing, and explains notification RAM replication, the full 5.5/10.5 BRAM-tile mapping difference and the extra 8x8 address multipliers.

All synthesis, routing and equivalent-geometry mapping commands returned rc 0. Every ROM input was present and geometry checked; all four synthesis logs contain zero Synth 8-4445 diagnostics. The shipping route has no route errors, setup/hold/pulse-width failures, or active-port IOB failures. Its +0.013/+0.014 ns setup/hold margins describe the existing constraints: unmatched-clock/conditional-XDC warnings and 46/87 ports without input/output delays remain recorded limitations. No board-interface signoff or hardware claim is made.

The three placement directives all return rc 0 with zero final setup/hold failures. Shipping `ExtraPostPlacementOpt` gives +0.013 ns WNS at 48,618 LUT; `AltSpreadLogic_high` gives the best WNS, +0.123 ns at 48,972 LUT; `ExtraTimingOpt` gives +0.106 ns at 48,893 LUT. All use 32 threads, the default seed, the same synthesis checkpoint and the existing shipping constraints.

The retired substitution comparison remains historical: `eff99a9c`, 56,779 to 55,466 LUTs, 109 to 135 BRAM tiles, failed placement. The later exact-head datapath correction is 38,879 LUTs at `b3507ddd` against 34,215 at `04b55dad`. No RTL or donor change is included in this baseline.

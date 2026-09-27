# Commercial-grade timing measurement for issue 395

Measured 2026-09-27 for #395 items 1, 2 and 5.
The [assignment](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5859935504)
names the shipping AX7101 1x1 TDM8 candidate from `9e9954e9`.
The release declares commercial grade, 0 to 85 C junction.
Items 3 and 4 remain open; this record contains no physical measurements.

## Contents

- **[Candidate identity and recipe](#candidate-identity-and-recipe)** -- Input hashes, speed file and original implementation directives.
- **[Corner results](#corner-results)** -- Setup and hold results for each fixed model and recorded temperature endpoint.
- **[Report findings and limits](#report-findings-and-limits)** -- CDC diagnostics, clock-pair classifications and missing I/O constraints.

## Candidate identity and recipe

The input is `build_ax7101_eto_tdm8dev9e9954e9`, read without modification.
The routed checkpoint is in `Physopt postRoute` state.
The part is `xc7a100tfgg484-2`; the timing engine is Vivado 2026.1,
build 6511674, with production speed file 1.23 dated 2018-06-13.

| Input | Bytes | SHA-256 |
|---|---:|---|
| Routed checkpoint | 115715651 | `5f7a442b6a9327ad5d41aa0b10e18c84d9ca4c0aacd573d2ad25d444f5b2f5d1` |
| Bitstream | 3825992 | `1696d1ea7568b2cf3cd536b1d34488e1ce7702e4a79e7cf3aca2c6ed6a54d2c7` |
| Implementation Tcl | 30654 | `a6827b1388c04ad08a0c08f255d39d941fe22fb9a019abb0ab9c4cf7a1bc895e` |
| Constraints | 20700 | `c94fe242303759d9b800eacd719c5d7e51504b51533247746607b58f4b716d49` |

The retained implementation Tcl records `AreaOptimized_high` synthesis,
`ExploreArea` optimization, `ExtraTimingOpt` placement, and `AggressiveExplore`
for both physical-optimization passes and routing. It specifies no explicit
placement seed. Its source paths identify the 1x1 TDM8 generated configuration
at `9e9954e96bf5`; the clock report shows 100 MHz system and 50 MHz fabric.
The original build used 32 threads; this read-only analysis uses 16.
No synthesis, placement or routing was repeated.

## Corner results

The report recipe is [BUILDING section 5](../integration/BUILDING.md#5-gates-before-a-build-is-good).
It derives its conditions from the same declaration as new candidates.

| Timing model | Recorded junction endpoint C | WNS ns | TNS ns | WHS ns | THS ns |
|---|---:|---:|---:|---:|---:|
| Slow | 0 | 0.123 | 0.000 | 0.101 | 0.000 |
| Slow | 85 | 0.123 | 0.000 | 0.101 | 0.000 |
| Fast | 0 | 1.429 | 0.000 | 0.036 | 0.000 |
| Fast | 85 | 1.429 | 0.000 | 0.036 | 0.000 |
| Both models | 85 | 0.123 | 0.000 | 0.036 | 0.000 |

Both setup and hold were enabled for each selected model.
Each report counts 175907 setup and hold endpoints, with zero failing endpoints.
Worst pulse-width slack is 0.264 ns, with zero failing pulse-width endpoints.
The explicit negative-slack reports contain no paths.

These are two fixed timing models, repeated at the power-estimation endpoints.
They are not four temperature-specific timing models.
UG835 documents that operating-condition temperature is not used for timing;
UG906 requires both min and max analysis at both speed corners.
[DS181](https://docs.amd.com/v/u/en-US/ds181_Artix_7_Data_Sheet)
specifies the device operating ranges and speed characteristics.
The result clears the existing WNS >= 0 rule, without inventing a new margin.

## Report findings and limits

Clock interaction reports 16 active clock pairs: eight Clean, six Ignored,
and two No Common Clock. The two latter pairs connect `eth_clocks0_rx` and
`milansoc_crg_clkout1` in opposite directions; their constraint classifications
are `Timed (unsafe)` and `Partial False Path (unsafe)`.
Their slacks are positive, but that does not establish CDC correctness.

| CDC rule | Severity | Count |
|---|---|---:|
| CDC-2, missing ASYNC_REG on one-bit synchronizers | Warning | 11 |
| CDC-3, one-bit synchronizers with ASYNC_REG | Info | 21 |
| CDC-5, missing ASYNC_REG on multibit synchronizers | Warning | 4 |
| CDC-6, multibit synchronizers with ASYNC_REG | Warning | 56 |
| CDC-9, synchronized asynchronous reset | Info | 1 |
| CDC-10, combinational logic before synchronizer | Critical | 6 |
| CDC-12, multiple clocks feeding synchronizer | Critical | 4 |
| CDC-15, clock-enable-controlled crossing | Warning | 249 |
| CDC-26, possible LUTRAM read/write collision | Warning | 183 |

The report retains ten Critical diagnostics, 503 Warning diagnostics and
22 Info diagnostics. They have not been waived or repaired by this work.

`check_timing` finds zero unclocked registers, unconstrained internal endpoints,
multiple-clock pins, generated-clock problems or loops. It also finds **46
inputs without input delays and 87 outputs without output delays**.
These include memory, Ethernet, audio, serial and flash ports.
The unconstrained-path report preserves their detail.
CDC analysis skips unconstrained inputs; its report is not complete I/O coverage.

Positive constrained-path slack does not sign off those missing external
constraints, CDC diagnostics, die-temperature telemetry or oscillator bounds.
The assignment forbids timing fixes; these findings remain visible for review.

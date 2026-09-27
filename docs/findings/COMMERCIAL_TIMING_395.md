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
The [margin decision](https://github.com/kebag-logic/milan-fpga/issues/395#issuecomment-5860418611)
requires WNS >= +0.03 ns and WHS >= 0.
Both thresholds apply at every declared corner.
This formalizes BUILDING's AX7101 QSPI flashboot margin caveat.
Every row meets both thresholds for the applied constraints.
Worst WNS exceeds the required margin by 0.093 ns.
Worst WHS is +0.036 ns; TNS and THS remain zero.
Missing constraints still limit item 2's timing evidence, as below.

## Report findings and limits

Clock interaction reports 16 active clock pairs: eight Clean, six Ignored,
and two No Common Clock. The two latter pairs connect `eth_clocks0_rx` and
`milansoc_crg_clkout1` in opposite directions; their constraint classifications
are `Timed (unsafe)` and `Partial False Path (unsafe)`.
Their slacks are positive, but that does not establish CDC correctness.

The shipping build rejected its intended clock-crossing exceptions.
Its `alinx_ax7101.xdc:583-591` uses incomplete clock names.
`crg_clkout0/1` should match `milansoc_crg_clkout0/1`; they match nothing.
The audio clock group has the same missing prefix.
The source is `sw/litex/milan_soc.py:1520-1534` at `66001a30`.
Lines 1499-1509 explain the prior warm-die RX/ARP failure.
That failure motivated the intended 8 ns crossing bound.

The retained `vivado.log` census identifies each rejected exception:

| Shipping XDC line | Intended constraint | Diagnostic | Build log lines |
|---|---|---|---|
| 583 | Ethernet to sys/milan hold false path | 12-4739 | 1705, 4118 |
| 585 | Ethernet to sys/milan 8 ns maximum delay | 12-4739 | 4123 |
| 587 | Sys/milan to Ethernet hold false path | 12-4739 | 1710, 4128 |
| 589 | Sys/milan to Ethernet 8 ns maximum delay | 12-4739 | 4133 |
| 591 | Asynchronous Ethernet/audio clock groups | 12-4739; 12-5201 | 1719, 1721, 1723; 4142, 4144, 4146 |
| 595 | Quasi-static multicycle setup/hold relaxation | 20-1307 | 1724, 4147 |

`Vivado 12-4739` reports no valid constraint objects.
`12-5201` reports only one nonempty clock group.
`Designutils 20-1307` rejects `if` inside the XDC file.
That construct comes from `sw/litex/milan_soc.py:1550-1556` at `66001a30`.
Its 112 tagged cells therefore lack the multicycle relaxation.
That omission makes their analysis stricter.

The log contains **14 emitted CRITICAL WARNING diagnostics**:
ten 12-4739, two 12-5201 and two 20-1307.
A substring search returns fifteen matches, including line 6400.
That line echoes source text; it emits no diagnostic.
The retained census preserves diagnostic text and original line numbers.
The full log has 832920 bytes and SHA-256
`4519c33a0dddc5967a4ac37c5f58324a3517315996ddd7291476726d32e160a6`.

These rejections explain both unsafe Ethernet/milan clock-pair classifications.
Ethernet to milan is timed against a 4 ns relationship.
The reverse pair remains partially false-pathed.
Ethernet/sys crossings remain **unbounded false paths**, in both directions.
The generic LiteX MultiReg false path overrides maximum-delay constraints.
Correcting clock names alone would not restore that bound.
[Issue #607](https://github.com/kebag-logic/milan-fpga/issues/607) owns the constraint fix
and build refusal on these warnings.

The [internal review](https://github.com/kebag-logic/milan-fpga/pull/605#issuecomment-5860399025)
measured the intended bound on the read-only checkpoint.
Its receipts are `v2-probe-results.txt` and `v3-crossings-results.txt`.
Round 2 repeats its reset-based probe across all four directions.
The retained script and receipt are `crossings.tcl` and `crossings-results.txt`.
The probe clears timing constraints only in memory.
It recreates the 200 MHz and Ethernet primary clocks.
Generated sys/milan clocks propagate from the existing clock primitives.
It then applies the intended 8 ns datapath-only bound.
This exposes crossings hidden by the original false paths.

| Crossing | Slow maximum datapath ns | Slow worst slack ns | Fast maximum datapath ns | Fast worst slack ns |
|---|---:|---:|---:|---:|
| Ethernet to sys | 2.179 | 5.746 | 1.240 | 6.717 |
| Sys to Ethernet | 3.395 | 4.313 | 1.979 | 5.895 |
| Ethernet to milan | 5.373 | 2.560 | 3.092 | 4.823 |
| Milan to Ethernet | 3.652 | 4.056 | 1.996 | 5.878 |

Slack includes endpoint checks; it is not simply 8 minus delay.
Removing all false paths exposes fourteen milan-to-Ethernet endpoints.
The worst endpoint is the reset input `FDPE_18/PRE`.
The review's narrower measurement retained generic false paths there.
Its six visible endpoints gave Slow/Fast slack +7.066/+7.538 ns.
Their maximum datapath delays were 0.875/0.432 ns, respectively.
The other three directions reproduce the review's numbers exactly.
Both models meet the intended bound for this placement.
This diagnostic does not repair the shipping constraint set.
It neither proves CDC correctness nor protects future sweep seeds.
No timing or constraint fix is included in this lane.

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

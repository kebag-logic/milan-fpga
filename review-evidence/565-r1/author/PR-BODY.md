[A344]

Closes #565

## Status

Local implementation ready for independent review.

## Description

The 8x8 shape now declares a 50 MHz Milan/CPU target. Its note cites the cacheless build contract and #565 without claiming timing closure. The system declaration remains 100 MHz, sampling remains 48 kHz, and the audio PLL declaration remains 24.576 MHz. No other clock declaration carried a CLOSED claim.

The [build contract](docs/integration/BAREMETAL_FIRMWARE.md#build-contract) and [capture evidence](docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost) now describe the reconciled configuration.

## Consumer check

| Consumer | Before | After |
|---|---|---|
| Configuration loader | Milan 100 MHz <= system 100 MHz | Milan 50 MHz <= system 100 MHz |
| soc_params.json and generated sweep argument | --milan-clk-freq 100e6 | --milan-clk-freq 50e6 |
| lwsrp_table.json and lwsrp_table.svh | Clock parameters 100000000 | Clock parameters 50000000 |
| build_plan.md | Milan 100e6 | Milan 50e6 |
| gptp_ucode.hex generation | --clk-hz 100000000; gain 86, limit 33554 | --clk-hz 50000000; gain 172, limit 67109 |
| Main PLL and CPU clock input | Divider 16; 100 MHz | Divider 32; 50 MHz |
| CPU clock selection and MAC domain | Separate CPU clock enabled; Milan domain selected | Same selection and CDC; selected domain now 50 MHz |
| Datapath clock parameter and microsecond timer divisor | 100000000; 100 | 50000000; 50 |
| Quarter-second / diagnostic intervals | 25000000 / 100000000 cycles | 12500000 / 50000000 cycles |
| PHC reset increment | 167772160 Q8.24 ns, 10 ns per tick | 335544320 Q8.24 ns, 20 ns per tick |
| MAAP, media NCO, CRF receiver, grid alignment and AVTP receive monitor clock inputs | 100000000 each | 50000000 each |
| MMCM servo, optional I2S playback, render setpoint and both processor shadow clock inputs | 100000000 each | 50000000 each; feature pruning unchanged |
| MCLK divider exponent / source-settle error / latency-tap guard | 3 / 32 / 50000 cycles | 2 / 16 / 25000 cycles |
| Memory-bridge watchdogs | 3072 system cycles; 12-bit counters | 6144 system cycles; 13-bit counters |
| Optional PPS width | 100000 cycles if enabled | 50000 cycles if enabled; disabled in this shape |
| Generated XDC | 21076 bytes | Byte-identical; derived clock follows PLL divider |
| System timer and firmware clock constant | 100000000 | Unchanged |
| Shape-reading simulation suites | Descriptor geometry; independently specified test clocks | Headers and inventories byte-identical; default csr, milan_dp, nvm_backend and nvm_cosim exercised |
| Capture input gate | configured_cpu_hz=100000000 for 8x8 | configured_cpu_hz=50000000; six arms remeasured |
| Documentation | Stale 8x8 reconciliation and board-wide clock wording | Contract target, refreshed section 18, shape-derived consumer wording |

The configuration-specific gPTP image changes from `21e846a7e1989091e555486bbb571b6967eb014925f768dbca7d41124d1d3748` to `78c8418a00b35cdae75c459c5269ca3892355507c4dc8af9eb2c29d81b87673b`; both contain 13312 bytes. The 100 MHz comparison retains the selected configuration ROM and establishes capture timing only.

## Other configurations

Every generated file was compared directly before and after, including the generated sweep fragment.

| Configuration | Files compared | Result |
|---|---:|---|
| endstation_arty_4x4 | 11 | byte-identical |
| endstation_arty_8ch | 11 | byte-identical |
| endstation_arty_current | 11 | byte-identical |
| endstation_ax7101_1x1_tdm8 | 11 | byte-identical |

## Capture measurements

Each arm contains 16 captures with aligned rising edges. The system timer runs at 100 MHz. Both 50 MHz shapes use the contract clock; the 100 MHz 8x8 point is a non-contract comparison.

| Shape | CPU MHz | Traffic | Minimum ms | Maximum ms | 49 ms / maximum |
|---|---:|---|---:|---:|---:|
| 8x8 | 50 | ON | 24.29290 | 24.30246 | 2.0163x |
| 8x8 | 50 | OFF | 24.25794 | 24.26154 | 2.0197x |
| 1x1 | 50 | ON | 6.59814 | 6.60642 | 7.4170x |
| 1x1 | 50 | OFF | 6.58554 | 6.58857 | 7.4371x |
| 8x8 | 100 | ON | 18.99012 | 19.00433 | 2.5784x |
| 8x8 | 100 | OFF | 19.78694 | 19.79024 | 2.4760x |

The 8x8 contract maximum is 24.30246 ms, 0.19754 ms below the 24.5 ms limit. The nominal hold remains 50 ms with a guaranteed 49 ms floor. All 96 captures pass byte, ownership, attestation and traffic checks. The receipt records refreshed input hashes, rows and maxima. The labelled 100 MHz point remains required by the unchanged gate.

## ROM ledger

All three default processor images match the existing pin-keyed ledger. No re-recording was needed. Those images use generator defaults, independently of the configuration-specific gPTP image.

## Issue #231 report

The [baseline at ae729bbf](https://github.com/kebag-logic/milan-fpga/blob/ae729bbfd90934f4d56d3b02f1ffc652496b414d/docs/findings/PP_SHADOW_BASELINE.md) uses 100 MHz for the 8x8 timer and integrated Milan/CPU domain. Its clock-derived parameters, ROM and measured timing/area describe that recipe. The 68136-LUT, -11.331 ns integrated synthesis result cannot be presented as a 50 MHz result. The standalone 10 ns constraint is separately fixed, while its timer parameters still belong to the recorded configuration. The baseline was inspected without edits; geometry and historical results retain their original meaning.

## How to reproduce

Generate all five configurations from their sources and compare every artifact. Follow the capture recipe for both shapes at 50 MHz, traffic ON and OFF, and the labelled 8x8 100 MHz comparison, with 16 captures per arm.

## How to validate

| Required command group | Result |
|---|---|
| Full builder, compiler present and absent | rc 0 each |
| Documentation checks in repository and filesystem inventory modes; punctuation, style, TOC, anchors and paths | rc 0 each |
| Capture input and timing gate | rc 0 |
| RTL lint and default ROM-ledger check | rc 0 each |
| Default sweep chunks 1/5, 3/5 and 4/5 | rc 0 each |
| Whitespace diff check | rc 0 |

The existing historical calibration arm is unavailable in both builder modes. Compiler-dependent instruments intentionally do not run in the absent mode. Four optional external field-campaign/freshness arms are declared skipped by chunk 1/5. The filesystem inventory mode also omits its repository-parity self-test. These omissions contribute no evidence.

## DoD

The declared clock, consumer audit, artifact identity, capture threshold, ROM-ledger check and baseline report are complete. Independent reviews remain pending.

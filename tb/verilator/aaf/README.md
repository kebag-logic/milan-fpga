<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# AAF talker checks

`make` runs both existing talker legs and startup checks.

## Contents

- **[Startup boundary](#startup-boundary)** -- Defines the exercised contract and sweep.
- **[Defect controls](#defect-controls)** -- Names each planted defect and detecting assertion.
- **[Running](#running)** -- Gives reproducible commands and expected results.
- **[Limits](#limits)** -- Separates boundary simulation from bench measurements.

## Startup boundary

Issue #667 concerns retained timestamps after stream enable.

The shape has one talker and eight wire channels.

Four pair slots form each sample; six samples form packets.

IEEE 1722-2016 7.5 associates timestamps with the first sample.

Sections 4.3.2 and 4.4.4.9 define presentation time and encoding.

Milan v1.2 5.3.8.10, Table 5.6 defines EARLY/LATE_TIMESTAMP counters.

| Sweep dimension | Values |
|---|---|
| Fabric period | 20 ns |
| Sample periods | 1041, 1042, 1042 cycles, repeated |
| Pair spacing | 1, 26, 260 fabric cycles |
| Enable phase | 0, 1, each later pair and following cycle, 1040 |
| PHC origin | 0, 1000000000, 0xffe00000 ns |
| Disabled interval | Cold start, 500000000 ns, 3800000000 ns |
| Restart | Disable/re-enable; reset with enable held high |
| Output stalls | Five cycles in seventeen during reset-start cases |
| Initial sequence | 248, crossing modulo-256 wrap |

The Cartesian sweep grades 486 starts and 4860 PDUs.

Repeated phases in the compact-spacing case remain separate cases.

Every first-to-second timestamp step must equal the steady step.

Six rational sample periods equal exactly 125000 ns here.

The tolerance is therefore zero, including modulo-2^32 wrap.

Every timestamp independently matches its payload sample plus offset.

Payload checks require complete, ordered eight-channel sample frames.

Bounded loops require all ten PDUs, preventing vacuous success.

Each case prints its first ten headers and sweep result.

## Defect controls

| Planted defect | Required failing assertion |
|---|---|
| Restore admission before pair zero | Startup step equals steady |
| Retain admission across disable | Startup step equals steady |
| Retain admission across reset | Startup step equals steady |
| Omit presentation offset | Sample plus offset |
| Clear normal-mode timestamp validity | Valid normal timestamp |
| Hold sequence number | Consecutive sequence |
| Never publish a completed bank | Bounded first ten |
| Corrupt left sample bits | Complete sample rows |

Each source fragment must occur exactly once before mutation.

Every mutant requires exit 1 and its named failing assertion.

Compilation failures and crashes fail the campaign.

## Running

```sh
make -j16 -C tb/verilator/aaf
make -j16 -C tb/verilator/aaf startup
make -j16 -C tb/verilator/aaf startup-mutants START_JOBS=4
```

The startup leg passes 34020 checks.

All eight mutations must be caught; commands return zero.

`START_MDIR` selects the startup build directory.

`TMPDIR` selects temporary storage for the mutation campaign.

## Limits

The boundary receives the post-bind enable, not ACMP traffic.

The pair source models three legal delivery spacings.

It does not instantiate the TDM capture or capture-map engines.

Disabled clocks are elided while PHC time advances.

This exposes retained state without simulating seconds of silence.

Whole-datapath regressions exercise integration separately.

The manager repeats the bench binds after merge and flashing.

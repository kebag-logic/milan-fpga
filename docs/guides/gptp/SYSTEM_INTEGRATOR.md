<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP system-integrator guide

Use this page for parent wiring.

## Contents

- **[Configure](#configure)** — Build one matching engine image.
- **[Connect](#connect)** — Preserve every integration seam.
- **[Observe](#observe)** — Read coherent health and diagnostics.
- **[Verify](#verify)** — Exercise real parent boundaries.

## Configure

Product configurations set `fabric_gptp: true`.

The builder rejects false product values.

Every configuration needs one `gptp` section.

| Input | Purpose |
|---|---|
| Station MAC | Clock identity generation |
| Priority one | Announce priority vector |
| Datapath frequency | Timers and servo scaling |

The builder emits one absolute ROM path.

Keep that ROM with its generated bitstream.

## Connect

All engine logic uses `axis_clk`.

Reset stays synchronous and active-low.

| Seam | Integration duty |
|---|---|
| RX tap | Present accepted MAC receive beats |
| TX leg | Preserve valid-ready backpressure |
| TX stamper | Observe actual MAC-boundary acceptance |
| PHC | Apply rate levels and phase pulses |
| Publication | Consume only committed generations |

Never drive receive readiness from this observer.

Return both timestamp tag fields.

Sequence identifiers alone remain ambiguous.

Read the [engine interface guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/bacf812178ea0e0ca843b5c332dd62414f701fad/docs/INTEGRATION.md).

## Observe

Sample public state after commit.

| Surface | Meaning |
|---|---|
| GM and parent CSRs | Selected time hierarchy |
| `CLKV_STAT` | Synchronization, holdover, `asCapable`, `tu` |
| `GET_AVB_INFO` | Coherent selected-owner summary |
| `GET_AS_PATH` | Coherent selected PathTrace |
| Drop counters | Tap, parser, and queue refusals |

Zero PathTrace count means no published trace.

It never implies one hidden identity.

## Verify

- Run the imported engine suite.
- Run `gptp_shadow` for transport wiring.
- Run `gptp_plane` for PHC steering.
- Run `milan_dp` for product consumers.
- Stall transmit traffic deliberately.
- Reset during active exchanges.
- Withhold timestamp returns.
- Exercise option-off safe values.

Read the [parent seam contract](../../design/GPTP_PLANE.md).

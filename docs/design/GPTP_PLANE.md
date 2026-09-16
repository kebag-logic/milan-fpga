<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP plane

Fabric gPTP owns product time synchronization.

This page defines parent integration.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gptp.fabric-product-owner` | `implemented` | - |
<!-- milan-feature-status:end -->

![Fabric gPTP integration](../diagrams/timesync_chain.svg)

## Contents

- **[Choose a reader](#choose-a-reader)** — Follow responsibility-specific guidance.
- **[Ownership](#ownership)** — Identify the only product time owner.
- **[Integration seams](#integration-seams)** — Connect receive, transmit, PHC, and publication.
- **[Timestamp boundaries](#timestamp-boundaries)** — Preserve frame and timestamp pairing.
- **[Configuration](#configuration)** — Generate one matching engine image.
- **[Diagnostics](#diagnostics)** — Distinguish silence from internal refusal.
- **[Verification](#verification)** — Reproduce donor and parent evidence.

## Choose a reader

| Reader | Parent guide | Engine guide |
|---|---|---|
| Project manager | [Manager](../guides/gptp/MANAGER.md) | [`MANAGER.md`](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/MANAGER.md) |
| System integrator | [Integrator](../guides/gptp/SYSTEM_INTEGRATOR.md) | [`INTEGRATION.md`](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/INTEGRATION.md) |
| HDL developer | [HDL developer](../guides/gptp/HDL_DEVELOPER.md) | [`HDL_DEVELOPER.md`](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/HDL_DEVELOPER.md) |
| Test developer | [Test developer](../guides/gptp/TEST_DEVELOPER.md) | [`TEST_DEVELOPER.md`](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/TEST_DEVELOPER.md) |

Parent guides own integration behavior.

Engine guides own imported behavior.

## Ownership

- Product configurations enable `GPTP_PLANE_EN_P`.
- The builder rejects product configurations without it.
- `KL_gptp_shadow` wraps the imported engine.
- The engine owns protocol decisions and servo arithmetic.
- The parent owns transport, PHC, and public consumers.
- One atomic bank supplies every public consumer.
- Option-off elaboration exists only for verification.
- That elaboration publishes safe failure values.

Normative behavior remains in [`REQUIREMENTS.md`](../../REQUIREMENTS.md).

## Integration seams

| Seam | Parent boundary | Contract |
|---|---|---|
| RX | Accepted MAC receive beats | Observe only; classify `0x88F7`; never backpressure |
| TX | Dedicated control-lane input | Hold complete frames through downstream stalls |
| Launch records | The MAC's own transmit stream | One ordered record per launched frame, plus the echo that re-bases the position |
| Recovery | The link guard's episode evidence | Resolve a fenced epoch only after a qualified episode completes |
| PHC | `timestamp_counter` controls | Apply engine rate and phase changes |
| Publication | CSR and protocol consumers | Sample one committed generation |

Every functional engine block uses `axis_clk`.

Reset is synchronous and active-low.

### Receive

- A beat transfers when valid and ready coincide.
- The tap never changes receive readiness.
- Accepted gPTP frames enter one frame FIFO.
- First-beat PHC timestamps use a side FIFO.
- Frame commits push exactly one timestamp.
- Full timestamp storage sheds complete frames.

### Transmit

- Engine bytes become one wide control stream.
- Downstream readiness controls every accepted beat.
- The accepted end-of-frame beat allocates one ledger entry.
- Nothing is timed there.
- `KL_gptp_gmii_launch` observes the MAC's own transmit stream.
- It reports one record per launched frame, in order.
- Identity is position, not a tag lookup.
- Generation and frame tags cross-check that position.

### PHC and publication

- Engine rate writes become the PHC adjustment level.
- Engine phase writes remain single-cycle pulses.
- `pub_commit_o` exposes one complete state generation.
- `pub_disc_o` exposes pre-commit health discontinuities.
- Consumers never combine different publication generations.

## Timestamp boundaries

| Direction | Reference point | Pairing key | Root evidence |
|---|---|---|---|
| Ingress | First accepted tap beat | Delivered-frame position | `gptp_shadow` suite |
| Egress | The frame's LAUNCH, observed one register stage before the pads | Ledger position, cross-checked by generation and tags | `gptp_txts` closed loop |

The egress time is reconstructed, not captured:

```text
t1 = PHC at the accepted record
     - (TXTS_DELTA_EXP_P + OBS_LAT_E_CYC_P) x ETH_TICK_NS_P
     - CDC_LAT_D_CYC_P x DP_TICK
     - DP_TICK / 2
```

The shipping shape makes that **426 ns**.

Its terms are 45 transmit cycles and four register stages.

No term is an allowance for queueing.

The queue sits between the ledger entry and the launch.

The reconstructed interval never crosses it.

The published digital bound is +/-11.2 ns.

`tb/verilator/gptp_txts` grades every frame against a pad oracle.

That oracle is independent of the design under test.

A launch that cannot be reconstructed is an explicit loss.

`GPTP_DROPE[31:16]` counts those, and no substitute time is published.

No ingress correction is applied today.

`KL_gptp_shadow` stores the raw PHC value at `FW_HEAD0`.

`PTP_INGRESS_LAT` (`0x540`) is readable, inert scratch. It is a plain RW word
with no timestamp consumer.

A future ingress correction belongs at the tap boundary.

Physical calibration remains tracked by issue #64.

Both seams stamp per frame.

The shadow pushes one stamp per committed `0x88F7` frame.

The ledger returns one result per admitted frame.

Each result is a measurement or a counted loss.

No live PHC value enters the engine.

### After a reset

A reset invalidates the association between entries and positions.

The plane fences its own egress and seals the ledger.

It then asks the link guard for a recovery episode.

Only a completed episode discharges that demand.

An aborted, refused or masked episode discharges nothing.

The seal lifts only on the observer's echo.

That echo carries the observer's own position.

`GPTP_DROPE[31:16]` counts what the fenced epoch could not time.

## Configuration

The builder requires one `gptp` configuration section.

It generates one ROM per hardware configuration.

Inputs include these values:

- Station MAC address.
- Announced priority one.
- Actual datapath clock frequency.

`GPTP_UCODE_HEX_P` names the generated ROM.

`CLK_HZ_P` must match `axis_clk`.

## Diagnostics

| Counter | Owner | Public register |
|---|---|---|
| Tap drops | `KL_gptp_shadow` | `0x7E8[31:16]` |
| Parser drops | `KL_gptp_engine` | `0x7E8[15:0]` |
| Event drops | `KL_gptp_engine` | `0x7EC[15:0]` |
| Lost egress timestamps | `KL_gptp_txret` | `0x7EC[31:16]` |

Counters wrap naturally.

Read deltas between observations.

Option-off elaboration reports zeros.

## Verification

| Boundary | Command | Main evidence |
|---|---|---|
| Imported engine | `make -C gptp-processor` | Protocol, servo, parser, serialization |
| Parent transport | `make -C tb/verilator/gptp_shadow` | RX, TX, pairing, publication, ledger laws, recovery |
| Egress launch | `make -C tb/verilator/gptp_txts` | The launch reference over the product's own converted MAC |
| Converted MAC | `python3 sw/litex/test_gptp_tx_timestamp.py` | That conversion behaves like the migen source |
| Closed-loop PHC | `make -C tb/verilator/gptp_plane` | Servo controls real counter |
| Product integration | `make -C tb/verilator/milan_dp` | MAC, CSR, protocol consumers |
| Wire models | `make -C tb/verilator/tsn_fuzz ptp` | Message fields and state campaigns |

Read the [traceability table](../traceability/ieee8021as.md).

Historical integration detail remains [archived](../history/v1/design/GPTP_PLANE.md).

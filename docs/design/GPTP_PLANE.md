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
     - CDC_LAT_D_CYC_P x DP_TICK_NS_P
     - DP_TICK_NS_P / 2
```

The shipping shape makes that **426 ns**.

Its terms are 45 transmit cycles and four register stages.

No term is an allowance for queueing.

The queue sits between the ledger entry and the launch.

The reconstructed interval never crosses it.

The published digital bound is +/-11.2 ns.

These are its terms.

| Term | Bound | Basis |
|---|---|---|
| Clock-domain transfer: the crossing's sampling phase, mean corrected | +/-10.00 ns | half of `DP_TICK_NS_P` = 20 ns. The dominant term, and a direct consequence of the adopted 50 MHz PHC. The correction above subtracts the mean of that phase, so what remains is its spread |
| PHC integer truncation | +/-1.00 ns | `timestamp_out` is the integer field of a Q(64).24 accumulator, so with a non-zero adjustment the reported value trails the accumulator by up to one integer nanosecond |
| Transmit clock against PHC, relative frequency over the 426 ns window | +/-0.09 ns | 426 ns x `RECON_REL_PPM_P` = 200 ppm, rounded up |
| Applied PHC rate correction over the same window | +/-0.09 ns | the same product, enforced rather than assumed: a record whose `adj_abs_w` exceeds `PHC_ADJ_MAX_C` is returned as a loss |
| Digital observation point: reference edge and `delta` quantisation | 0.00 ns | `delta` is an exact transmit-clock cycle count, and any value other than `TXTS_DELTA_EXP_P` aborts the record instead of reconstructing from it |
| PHC discontinuity inside the window | not a bound | invalidated and returned as counted loss, never absorbed |
| **Total** | **+/-11.18 ns, published as +/-11.2 ns** | sum of magnitudes, rounded up and never down |

The assumptions are declared, not inherited.

`RECON_REL_PPM_P` is a design constraint the bench sweeps.

It is not a claim about this board's oscillators.

The total is insensitive to it.

At 1000 ppm those two terms reach 0.85 ns.

The total would then be 11.9 ns.

Every term above is digital.

No term is a measured physical latency.

This is a component bound, not the system obligation.

[NFR-TIME-01](../reference/FR_NFR.md) requires 1 us to the grandmaster.

This bound is one contributor to that.

Through `t1` alone it contributes at most +/-5.6 ns.

The physical terms are not in this table.

PHY latency, pad clock-to-out and cable belong elsewhere.

`tb/verilator/gptp_txts` grades every frame against a pad oracle.

Its `kBoundNs` is 11 ns.

That is never looser than the figure published here.

That oracle is independent of the design under test.

A launch that cannot be reconstructed is an explicit loss.

`GPTP_DROPE[31:16]` counts those, and no substitute time is published.

### The board's own latency corrections

Two per-board constants correct what the digital terms cannot reach.

`INGRESS_LAT_NS_P` is SUBTRACTED from the arrival stamp at `FW_HEAD0`.

`EGRESS_LAT_NS_P` is ADDED to the reconstructed launch.

The plane is their only consumer.

They are declared per board in the configuration's `gptp:` section.

The builder carries them into elaboration parameters.

`GPTP_LAT` (`0x7F0`) publishes the applied pair, read-only.

So a controller host reads what is applied.

`PTP_INGRESS_LAT` (`0x540`) stays readable, inert scratch.

So does `PTP_EGRESS_LAT` (`0x544`).

Neither has a timestamp consumer.

One owner cannot be two.

A correction two layers each apply is applied twice.

The builder REFUSES a board that omits either key.

A generated default looks exactly like a measured zero.

#### What is measured, and what is assigned

The SUM is measured. The SPLIT is not.

An inline tap on the link measures the sum.

It compares the wire's Pdelay turnaround against the claimed `t3 - t2`.

A Milan-validated reference peer gives the instrument's zero.

On 2026-09-20 this board showed **875 ns** of error.

Its uncertainty is about 25 ns.

The method needs no new instrument.

[BOARD_PORTING_AX7101.md](../integration/BOARD_PORTING_AX7101.md) states it for a new port.

The digital distance INSIDE `milan_datapath` is measured, and it is zero.

`tb/verilator/milan_dp`'s gPTP legs count it both ways.

They print it as cycles and grade it.

Receive is 0 cycles, MAC beat to stamp.

`rx_mac_filter` passes combinationally.

The tap latches on that same edge.

Transmit already lands on the observed launch.

`tb/verilator/gptp_txts` grades that against a pad oracle inside 11 ns.

A pipeline change moving either stamp point fails those checks.

That is what forces these constants to be measured again.

So the whole 875 ns lies OUTSIDE this module.

It is not all analog.

From the GMII pins the receive path crosses LiteEth.

That is framing, width conversion and two clock-domain crossings.

This repository converts that chain for TRANSMIT only.

`sw/litex/gen_mac_tx_model.py` is the converter.

So the receive chain's distance cannot be counted here.

The split is therefore ASSIGNED, not derived.

The board reference's PHY datasheet states no 1000BASE-T latency.

It states only the RGMII clock-skew straps.

This board is strapped GMII and does not use them.

No figure exists elsewhere in this repository.

The default applies: 3:1 receive to transmit.

The 1000BASE-T receive DSP dominates.

That is **656 ns ingress and 219 ns egress**.

They sum to the measured 875 ns.

| Quantity | Value | How it is known |
|---|---|---|
| Total stamp error | 875 ns, +/-25 ns | measured, inline tap, 40 exchanges per direction |
| Digital receive, inside `milan_datapath` | 0 ns | counted and graded in `tb/verilator/milan_dp` |
| Digital transmit, beyond the 426 ns already corrected | 0 ns, bounded +/-11 ns | the `tb/verilator/gptp_txts` pad oracle |
| Remainder: PHY plus the LiteEth receive chain | 875 ns | the measured sum, less a proved zero |
| Assigned ingress | 656 ns | 3:1 default, no datasheet figure |
| Assigned egress | 219 ns | 3:1 default, no datasheet figure |

#### The open bound on the split

Nothing measured here bounds the split error.

A one-way error of `e` leaves the SUM right.

The two constants are then wrong by `+e` and `-e`.

Both published stamps move the SAME way, late by `e`.

An ingress stamp under-corrected by `e` is late by `e`.

An egress stamp over-corrected by `e` is late by `e` as well.

**It does not move the peer delay.**

Mean link delay is `((t4 - t1) - (t3 - t2)) / 2`.

Both corrections enter that with the same sign.

So only their sum appears.

A common shift of both stamps cancels.

The 800 ns bound is met by the sum alone.

That is the measured quantity.

**It moves the synchronized offset by the whole split error.**

A Sync arrives on the ingress path only.

The ingress constant alone corrects it.

Its receive stamp is left late by `e`.

The mean link delay does not move.

So it absorbs none of that.

So the computed offset from the grandmaster carries `e`, not `e/2`.

The LiteEth receive chain is the largest known contributor to `e`.

Counting it as PHY assigns too little ingress.

Closing that needs the second instrument of issue #488.

The physical calibration itself remains issue #64.

Both seams stamp per frame.

The shadow pushes one stamp per committed `0x88F7` frame.

The ledger returns one result per admitted frame.

Each result is a measurement or a counted loss.

No live PHC value enters the engine.

### Propagation asymmetry is not modelled

This record settles the design boundary of issue #511.

The [owner decision](https://github.com/kebag-logic/milan-fpga/issues/511#issuecomment-5789766257) excludes delayAsymmetry for v1.2.

It cites REQ-PTP-06's constants and the single cabled port.

| Question | v1.2 answer | Authority |
|---|---|---|
| Is delayAsymmetry modelled? | No. Its value is zero. | IEEE 802.1AS-2011 8.3 does not require measuring it; 10.2.4.8 makes an unmodelled value zero |
| Where would it enter? | ClockSlaveSync `syncReceiptTime` and `setMDSyncReceive()` `upstreamTxTime`. At zero both terms vanish. It never enters the Pdelay mean. | IEEE 802.1AS-2011 10.2.12, 11.2.13.2.1 and 11.2.15.2.4 |
| Is it managed? | No managed object, CSR or configuration key carries it. | IEEE 802.1AS-2011 14.6.9 lists it read-write and recommended |
| Can a configuration set it? | No. The builder refuses every `gptp` key it does not know (`_known_gp`). | [`endstation_builder.py`](../../sw/builder/endstation_builder.py) |
| Does the engine take it? | No. The pinned gPTP processor has no asymmetry input. | Outside its historic prototype pages the pinned tree never names it ([donor issue 58](https://github.com/Mister-M-alt/FPGA-gPTP/issues/58)) |
| What corrects timestamps? | The two per-board elaboration constants, applied once in `KL_gptp_shadow`. | REQ-PTP-06; IEEE 802.1AS-2011 8.4.3 `ingressLatency` and `egressLatency` |
| What fixes a one-way split error? | Re-measured constants (#64, #488). Never a second asymmetry term. | REQ-PTP-06 names one owner |
| Is live tuning allowed? | No. The donor's UART Y/I/E tuner stays donor-bench-only. | REQ-PTP-06 constants; REQ-PTP-09 |
| Does Milan ask for it? | No. Milan v1.2 never mentions asymmetry. | Milan v1.2 Section 4.2.6 defers to 802.1AS |

Two donor citations disagree with the 2011 text.

The clauses above were checked against that text.

| Donor citation | IEEE 802.1AS-2011 text |
|---|---|
| Issue 58: 11.2.15 | The MDPdelayReq machine; `computePropTime()` has no asymmetry term |
| Prototype pages: 10.2.4.5 | That clause is `syncInterval`; delayAsymmetry is 10.2.4.8 |

#### Revisit trigger

Revisit when a profile adds a second cabled port.

Section 8 redundancy under #394 is one such profile.

A runtime correction first needs a REQ-PTP-06 amendment.

#### What an adoption must define

| Item | Required answer |
|---|---|
| Requirement | A public REQ-PTP amendment naming one owner, before any RTL lane |
| Sign | Positive when responder-to-initiator is longer (8.3) |
| Units | `scaledNs` in the grandmaster time base (10.2.4.8, 14.6.9) |
| Default and reset | Zero, which is today's behavior |
| Range | Declared in the configuration schema; the builder refuses values outside it |
| Configuration owner | One key per port, carried to one engine input |
| Application point | 10.2.12 and 11.2.13.2.1 only; never `computePropTime()` |
| Update | An elaboration constant, unless REQ-PTP-06 is amended first |
| Double compensation | Never folded into `INGRESS_LAT_NS_P` or `EGRESS_LAT_NS_P` |

#### What an adoption must prove

No result is claimed here: nothing is implemented.

| Arm | Expected evidence |
|---|---|
| Zero | Offset and PHC trajectory identical to today's build |
| Positive and negative | The offset moves by the configured value, in opposite directions |
| Sign | A sign-swapped mutation fails the suite |
| Limits | Out-of-range values are refused by the builder |
| Reset and update | Reset restores zero; no live change without an amendment |
| Peer delay | `neighborPropDelay` is unchanged by every value |
| Double correction | The I/E constants and `GPTP_LAT` are unchanged |
| Configuration to engine | The configured value reaches the engine input exactly |

An adoption is one bounded lane, tracked under issue #110.

It owes a reviewed durable donor pin and regenerated ROM.

It also owes donor `make`, `gptp_shadow` and root integration.

Every CONTRIBUTING gate runs at that candidate.

| Party | Owns |
|---|---|
| Parent | The product contract, REQ-PTP-06 constants, the builder refusal and this record |
| gPTP processor | Any asymmetry input and its arithmetic, under donor issue 58 |
| Donor bench | The UART Y/I/E tuner, never pinned into a product image |
| Issues #64 and #488 | Physical measurement of the split |
| Issue #110 | Integration tracking of any adopted donor pin |

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

`gptp.ingress_latency_ns` and `gptp.egress_latency_ns` are REQUIRED of every
board and reach `INGRESS_LAT_NS_P` / `EGRESS_LAT_NS_P`.

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

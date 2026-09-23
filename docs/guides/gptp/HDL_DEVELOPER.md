<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP HDL-developer guide

Use this page for parent RTL changes.

## Contents

- **[Find ownership](#find-ownership)** — Change the correct repository and module.
- **[Preserve timing](#preserve-timing)** — Maintain transfer and commit ordering.
- **[Handle failures](#handle-failures)** — Keep refusal paths observable and bounded.
- **[Finish changes](#finish-changes)** — Update tests, diagrams, and evidence.

## Find ownership

| Concern | Owner |
|---|---|
| Protocol state | `gptp-processor/` |
| Parent transport | `KL_gptp_shadow` |
| Egress identity | `KL_gptp_txticket` allocates one ledger entry per admitted frame |
| Egress launch | `KL_gptp_gmii_launch` observes the MAC's own transmit stream |
| Egress reconstruction | `KL_gptp_txret` owns the ledger, the fence and the recovery demand |
| PHC arithmetic | `timestamp_counter` |
| PHC clock domain | `milan_soc.py` ties `gtx_clk` to `axis_clk` at the `milan_datapath` instantiation |
| Time validity | `KL_ptp_clock_validity` |
| Public ABI | `milan_csr` and processor wrapper |

Never patch imported behavior inside the parent lane.

Land donor changes before advancing its pin.

Read the [engine HDL guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/HDL_DEVELOPER.md).

## Preserve timing

![RX acceptance timing](https://raw.githubusercontent.com/Mister-M-alt/FPGA-gPTP/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/diagrams/wavedrom/rx_accept.svg)

![TX backpressure timing](https://raw.githubusercontent.com/Mister-M-alt/FPGA-gPTP/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/diagrams/wavedrom/tx_backpressure.svg)

![Parent Pdelay timestamp ownership](../../diagrams/wd_gptp_pdelay.svg)

The parent chronogram proves the egress and ingress orderings:

- The accepted EOF beat allocates the entry.
- Nothing is timed at that beat.
- The queue after it is drawn, never corrected for.
- Reference octet to tag octets is 45 transmit cycles.
- The record crosses in two fabric cycles.
- The tuple returns on the record's own cycle.
- Ingress commit follows nine accepted beats.
- Engine SOF follows the commit by three cycles.

Clock-domain precondition:

- The PHC counts on `gtx_clk`.
- The shadow samples `phc_ns_i` on `axis_clk`.
- Every real instantiation ties `gtx_clk` to `axis_clk`, and
  `sw/builder/test_builder.py` gate 1d refuses a build that does not.
- The egress reconstruction subtracts whole PHC ticks.
- A bench may run the counter at another rate.
- It must then declare `GPTP_PHC_TICK_NS_P`.
- `KL_gptp_txret` refuses that mismatch at elaboration.
- The launch observer runs in `maceth_tx`.
- It takes the MAC's own transmit reset.
- It owns both record crossings itself.
- `ptp_csr_sync` crosses CSR commands only.

Timing rules:

- RX acceptance requires a real parent transfer.
- RX timestamps remain paired through frame commit.
- TX payload stays stable during every stall.
- TX state advances only after acceptance.
- Publication fields stage before commit.
- Discontinuity reaches validity before registered publication.

The [parent architecture](../../design/GPTP_PLANE.md) explains each seam.

## Handle failures

- Drop complete RX frames after storage exhaustion.
- Count every confirmed gPTP tap refusal.
- Reject malformed frames inside the parser.
- Preserve event snapshots through queueing.
- Match egress timestamps using both tags.
- Keep option-off outputs structurally safe.
- Test reset during every outstanding transaction.

Never convert a refused frame into partial data.

## Finish changes

- Add a failing focused regression first.
- Exercise negative and boundary paths.
- Update WaveDrom after timing changes.
- Update Draw.io after structural changes.
- Run donor and parent suites.
- Run lint and portability gates.
- Record exact-head evidence publicly.

Start with the [source ledger](https://github.com/Mister-M-alt/FPGA-gPTP/blob/e5dcea6e351abff18a27a00f8e345f3251bdbd8f/docs/SOURCE_EVIDENCE.md).

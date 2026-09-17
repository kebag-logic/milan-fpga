# Milan FPGA product changelog

This file records current bare-metal product revisions.

Older campaigns remain available in Git history.

The [archived throughput record](docs/history/v1/findings/PERFORMANCE_GOAL.md) preserves closed campaign measurements.

## Contents

- **[Unreleased - gPTP egress launch time](#unreleased---gptp-egress-launch-time)** -- The queue leaves t1.
- **[Release 0x0002_0059 - PPS output](#release-0x0002_0059---pps-output)** -- Six CSR words, one metrology pin.
- **[Release 0x0002_0058 - slip counters readable](#release-0x0002_0058---slip-counters-readable)** -- Two RO words, prefill retired.
- **[Release 0x0002_0057 — live media-clock selection](#release-0x0002_0057--live-media-clock-selection)** -- CRF selection steers the grids.
- **[Release 0x0002_0056 — ownerless gPTP verification form](#release-0x0002_0056--ownerless-gptp-verification-form)** -- Verification only.
- **[Release 0x0002_0055 — fabric gPTP product ownership](#release-0x0002_0055--fabric-gptp-product-ownership)** -- Shipping time owner.
- **[Release 0x0002_0054 — generated names](#release-0x0002_0054--generated-names)** -- Serves generated names and writable overlays.
- **[Release 0x0002_0053 — stream setters](#release-0x0002_0053--stream-setters)** -- Adds supported stream setters.

## Unreleased - gPTP egress launch time

- The egress timestamp was the first accepted MAC-boundary beat.
- Two crossings and a store-and-forward buffer follow that beat.
- That queue entered t1 and biased the peer delay (#360).
- t1 is now the frame's launch.
- It is observed one register stage before the pads.
- `KL_gptp_gmii_launch` reports one ordered record per frame.
- `KL_gptp_txticket` allocates one entry per admitted frame.
- `KL_gptp_txret` owns the ledger and the correction.
- It also owns the fence and the recovery demand.
- Identity is position; generation and tags cross-check it.
- The correction is 426 ns of register stages.
- No term of it is a queue allowance.
- An unreconstructable launch is a counted loss.
- `GPTP_DROPE[31:16]` publishes that count.
- The word's low half is unchanged.
- VERSION is unchanged; the release step owns the bump.
- `tb/verilator/gptp_txts` closes the loop over the converted MAC.
- `sw/litex/test_gptp_tx_timestamp.py` proves that conversion behaves.

## Release 0x0002_0059 - PPS output

- The PHC can drive a pulse-per-second pin (#260).
- Six words land at `0x548`-`0x55C`.
- `PTP_PPS_CTRL` holds the enable, the arm strobe and a built bit.
- `PTP_PPS_TGT_{LO,HI}` carries the second boundary to arm.
- `PTP_PPS_RD_{LO,HI}` reads the live target back.
- It advances by exactly `1e9` per pulse, so drift is measurable.
- `PTP_PPS_WIDTH` publishes the elaborated width in PHC cycles.
- `PPS_CTRL[16]` reads 0 when the comparator was never built.
- Arm and enable can go in one word.
- That write emits no pulse before the boundary.
- The comparator is gated on having been armed.
- The output is off by default and needs `--pps` to exist.
- On the AX7101 it is J11 pin 35, ball `C17`.
- No existing CSR address moves.

## Release 0x0002_0058 - slip counters readable

- `SLIP_LB` (`0x8D4`) and `SLIP_TDM` (`0x8D8`) expose the media-boundary slip counters (#390).
- `SLIP_LB` counts the loopback ring; `SLIP_TDM` counts the TDM junction.
- Each word is live RO, `{skip[31:16], dup[15:0]}`, saturating.
- Read twice and difference for a rate below the ceiling.
- A starved fed pair counts one dup per tick.
- A half at `0xFFFF` is spent until reset.
- `SLIP_LB` is a structural zero without the loopback lane.
- The true-ratio leg feeds the ring at the physical rate.
- At INTERNAL each fed pair dups once per beat period.
- Under CRF the same window shows zero: one grid.
- The `PB_PREFILL_C` bench override is retired.
- Every suite grades the shipped prefill.
- No existing CSR address moves.

## Release 0x0002_0057 — live media-clock selection

- The stored `SET_CLOCK_SOURCE` index reaches the media plane (#74).
- One registered resolve compares it against the generated CRF index.
- A CRF-less shape resolves structurally false through the `16'hFFFF` fold.
- The verdict arms the MMCM servo, the align chain, and `mr`.
- `KL_media_grid_align` holds the packet grid on the physical fsync grid.
- The chain runs CRF, MMCM, fsync, then tick.
- The MMCM status slice belongs to the MMCM alone.
- INTERNAL remains bit-exact free-run with slips accepted and now counted. Since 0x0002_0058 they read at `SLIP_LB`/`SLIP_TDM` (`0x8D4`/`0x8D8`).
- `KL_chan_map_capture` gains TDM junction slip counters.
- The true-ratio leg proves the INTERNAL drift.
- The same leg proves its close under CRF.
- Received toggles and source changes both fire `mr`.
- The 10.4.3 scoping negative holds at INTERNAL.
- The CLOCK_SOURCE shape constants join `adp_shape_defaults.svh`, derived.
- Every shape carries its own CRF index.
- The 8-listener shapes read index 9.
- No CSR addresses move.

The bench probe stays open on issue #74.

## Release 0x0002_0056 — ownerless gPTP verification form

- The fabric gPTP plane remains the sole shipping time owner.
- It owns protocol, servo, and publication state.
- `GPTP_PLANE_EN_P=0` remains buildable only for verification.
- Its GM, parent, PathTrace, and peer-delay publications remain zero.
- Sync and asCapable remain zero.
- `tu` remains one.
- Compatibility writes remain inert.
- Bare-metal UART status exposes the complete timing record.
- The smoke grader validates every published field.
- The bare-metal gate rejects superseded runtime surfaces.
- Mutation controls cover every tracked path class.
- `milan_datapath` no longer instantiates classifier or queue stages.
- It also omits credit shaping and record stamping.
- Their only packet source left under #259.
- Product sources already join the downstream trunk.
- CSR addresses remain stable.
- Retained classifier and shaping registers are scratch.
- Retired capability and diagnostic bits read structural zero.
- The builder drops `--cbs-queues-mask`.
- Standalone suites and Yosys tops retain block coverage.
- Fabric credit shaping remains separately scoped.
- `milan_datapath` shrinks by 180,840 Yosys cells.
- Issue #259 removes 163 files and 57,135 lines.
- Commit `59ba6ffb` preserves them in Git history.
- Removed surfaces include campaign and vendor-build infrastructure.
- They also include superseded audio staging and benches.
- Target-era findings, logs, product pages, tests, and diagrams left.
- The archive lost only material covered by #259.
- The bare-metal scanner guards future reintroduction.
- General archives retain visibly labelled obsolete evidence.
- Issue #259 keeps target-only material solely in Git history.
- Other protocol records remain in the general archive.
- Current authorities replace stale status pages.

Physical closure still requires #70 and #117 evidence.

## Release 0x0002_0055 — fabric gPTP product ownership

- Product configurations select the integrated fabric gPTP engine.
- One atomic bank publishes GM, parent, and PathTrace.
- It also publishes delay, sync, asCapable, and AVTP `tu`.
- Fabric publication writes cannot be forged through CSRs.

## Release 0x0002_0054 — generated names

- `SET_NAME` and `GET_NAME` serve generated AEM names.
- Responses and `READ_DESCRIPTOR` share one writable overlay.

## Release 0x0002_0053 — stream setters

- Stream-format setters apply descriptor-specific validation.
- Supported stream-info setters apply equivalent validation.
- Accepted presentation offsets reach their fabric consumers.
- Accepted stream formats reach their fabric consumers.

Earlier revisions remain in this file's Git history.

The CSR RTL history provides the version source.

<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The fabric gPTP plane

The time-sync plane of epic #110: the `gptp-processor` submodule's
micro-coded 802.1AS engine spliced into the datapath as the product's
time owner. The default image does not start `ptp4l`, `phc2sys`, or the
`milan-statd` GM/path/CLKV mirror chain. This page is the integration
architecture of record for #114 and #116; the donor
repo's own pages under `gptp-processor/docs/` (the resource-validation
record) carry the engine's internals and measured cost.

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `gptp.fabric-product-owner` | `implemented` | - |
<!-- milan-feature-status:end -->

Normative edition: the plane's wire formats and state machines follow the
Milan v1.2 profile (section 4.2.6) of IEEE 802.1AS-2011 with Cor1-2013 and
Cor2-2015, so a clause cited on this page or in the donor's pages is
802.1AS-2011 unless marked otherwise. The controlField is the 11.4.2.7 /
Table 11-7 value per message (Sync 0x0, Follow_Up 0x2, Announce and the
three Pdelay messages 0x5), not the 0 of 802.1AS-2020 10.6.2.2.13; receivers
ignore the byte in both editions (IEEE 1588-2008 13.3.2.10, IEEE 1588-2019
13.3.2.13). The hardware-assist scope (PHC, timestamping planes) keeps its
802.1AS-2020 references in [REQUIREMENTS.md](../../REQUIREMENTS.md) section 2
and the [802.1AS traceability table](../traceability/ieee8021as.md); the
decision is recorded on #139.

## Contents

- **[The shape](#the-shape)** -- one option, four seams
- **[Timestamps](#timestamps)** -- where stamps are born and how they travel
- **[The ownership boundary](#the-ownership-boundary)** -- default fabric owner and explicit software comparison
- **[Verification map](#verification-map)** -- which bench proves what

## The shape

`GPTP_PLANE_EN_P` (milan_datapath parameter, **default ON**) elaborates
`KL_gptp_shadow` with four seams. The builder emits the same value into every
real build/sweep/deploy instance. The supported comparison is explicit
`fabric_gptp: false`; it selects the software-owner ABI and causes the rootfs
fragment to carry `/etc/milan-gptp-software-owner`. Invalid owner/profile
pairings are refused rather than silently producing two PHC owners.

The option also carries `GPTP_UCODE_HEX_P`. In a shipping SoC build this is an
absolute path to the builder's per-config 1,024-word image, generated from the
same YAML station MAC, priority1 and Milan clock as the rest of the station.
Self-contained benches retain the relative `gptp_ucode.hex` default.

The plane has four seams:

1. **RX**: the same `rx_axis_to_dma` tap every plane uses -- input
   only, a beat is real when `tvalid && tready` (the gh #65 rule). The
   tap classifies EtherType 0x88F7 at the aligned lanes into a frame
   FIFO (drops counted via the FIFO's overflow strobe -- with
   DROP_WHEN_FULL the input stays ready, so a ready-based counter is
   blind) and feeds the engine 1 byte/clk.
2. **TX**: the engine's byte stream gears up to one wide, frame-held
   lane that joins the control TX AFTER the min-IFG gasket (the CRF
   rationale: time-critical frames must not queue 512 cycles per
   control burst) through its own staggered merge -- ctl 2^15, this
   merge 2^16, the MAC boundary 2^17; arbiter diagnostics lane 4.
   HONEST BOUND: bypassing the gasket means a plane frame can reach
   the MAC back-to-back behind another frame -- the exact class the
   512-cycle gasket exists for (the MilanMAC cut-through eater). The
   plane's own exchange pairs are self-spaced by the 1 B/clk gearbox,
   and #117's silicon rounds own the wire answer before #116 flips
   the option on.
3. **PHC**: the plane owns `timestamp_counter`'s adjfine (a
   pulse-to-level latch lives in the shadow) and adjtime when enabled;
   settime stays with the CSR face -- boot sets the epoch. Off, both
   knobs constant-fold to the CSR-driven wires.
4. **Publish**: the grandmaster identity every fabric consumer reads
   (the protocol processor's ADPDU/GET_AVB_INFO/AS_PATH face, the
   Milan-info answers, the recentre latch) follows the plane's publish
   bank when the option is on.

## Timestamps

- **Ingress**: latched from the live counter at each frame's first tap
  beat, pushed into a side FIFO on the frame FIFO's commit pulse --
  exactly once per DELIVERED frame, so drops can never desync stamps
  from frames -- and popped at the byte stream's sof. The constant
  MAC-to-tap pipeline offset belongs to the ingress-latency correction;
  #117 measures it on silicon. The side FIFO is 32 deep, smaller than
  the frame FIFO, so a back-to-back burst could commit more frames than
  it holds; the **shed rule** (issue #122) keeps it from lapping a
  still-live stamp: at a frame's first tap beat, if the ring is already
  spoken for, the WHOLE frame is shed before it enters the frame FIFO,
  and the shed is counted in `dbg_tap_drop_o` only once its EtherType
  verdict confirms 0x88F7.

  "Spoken for" is two terms, and both are load-bearing. The ring's own
  occupancy (write minus read pointer) is exact but **lags**: the push
  happens on the frame FIFO's commit, so frames already taken at the tap
  are invisible and the guard would shed too late (measured: 38 frames
  into a 32-entry ring). Counting at the tap and releasing on pop closes
  that gap but **leaks**: a frame the FIFO itself discards -- oversize,
  or arriving full -- never commits, so it never pushes and never pops,
  and after 32 such frames the guard wedges shut and the plane goes
  permanently deaf. So the second term counts frames that have entered
  the frame FIFO and are not yet **resolved** by it. A frame resolves
  exactly once, as good (a future push), bad, or overflow (no push), so
  the count can neither leak nor underflow whatever the FIFO does with
  it. The sum is the entries the ring holds plus the pushes it may still
  be owed, so shedding at 32 means it is never asked to hold a 33rd.
  Take the pointer difference in its own width before widening it to the
  sum: casting `wp - rp` straight to the wider type evaluates the
  subtraction at that width and throws the wrap-safe bit away, which
  reads a wrapped ring as almost-full and sheds frames there was room
  for. A frame that is a single beat and arrives while the ring is full
  is shed without being counted -- its EtherType verdict never lands, so
  it is indistinguishable from the runts the tap already reclaims.
- **Egress**: the control lane does not traverse `ptp_ts_top`'s TX
  stamper (only the shaped data path does), so `KL_gptp_txstamp`
  observes the TRUE MAC boundary: armed by the plane's lane sof, it
  latches the counter at an 0x88F7 frame's first beat and returns
  {ts, sequenceId, messageType} for the engine's pending exchange.
  BOTH tags travel, since #214: a Pdelay_Req carries our own request
  counter and a Pdelay_Resp echoes the peer's, so the 16-bit sequence
  alone cannot say which leg a stamp belongs to, and on a link where
  both ends run this plane the two counters start equal at boot and
  advance together at 1 Hz. Two frames of one messageType are never
  outstanding at once, so the pair separates them. The engine consumes
  both halves at its boundary (`KL_gptp_shadow`'s `txts_type_i`, mirrored
  on `dbg_txts_type_o`) and credits only the exact transmitter claim;
  this is the parent integration of Mister-M-alt/FPGA-gPTP#28.
  Observer-pure (`check_tap_purity` holds). One gPTP stack per port is
  the operating assumption -- two transmitting stacks is itself
  invalid, and the A/B bring-up keeps exactly one talking.
- **Inside the engine**, the ingress stamp ping-pongs with the message
  bank (stage at sof, commit at eof, length-qualified) -- the fabric
  bench found the single-register race this retires; the pinned donor's
  engine record carries the story.

## The ownership boundary

With the product-default option on, the fabric publication bank is the single
source for `ADP_GM` 0x624/0x628, `GPTP_PDELAY` 0x6E4, the parent at
0x730/0x734, GET_AVB_INFO, GET_AS_PATH, clock validity/asCapable and AVTP
`tu`. GM and parent are each snapshotted as one 64-bit value across either
two-half CSR read order. A GM/sync discontinuity asserts `tu` on that same
edge, then the committed bank becomes visible; no consumer can see a new
identity with an old-valid timestamp verdict. Software writes to the legacy
publication and CLKV registers cannot manufacture live fabric health.

With the option off, the legacy software contract remains intact: LO stages
and HI commits each identity, `CLKV_CTRL` renews the compatibility lease, and
the marked rootfs image starts linuxptp plus the full publisher. This is a
comparison/bring-up shape, not the product default. VERSION `0x0002_0055`
records the ownership change without allocating new CSR addresses.

## Verification map

| bench | faces | proves |
|---|---|---|
| gptp-processor `tb/verilator/*` | byte, model counter | the 802.1AS state machines, servo math, and the donor's planted-mutation ladder; its count lives in the donor's engine bench README under `gptp-processor/tb/verilator/engine/` at the pinned SHA and is not mirrored here, where it would drift at every repin |
| `tb/verilator/gptp_plane` | byte, REAL counter | the engine steers the parent's `timestamp_counter` closed-loop, and its transmitted Follow_Up carries a live timestamp while the two-step Sync body stays zero (Table 11-8). It does NOT observe the engine's own `phc_ns_i`: at the current submodule pin that input has no reader, so a tie-off there passes this bench ([#211](https://github.com/kebag-logic/milan-fpga/issues/211)). The slice's `timestamp_counter` wire is a different signal and IS covered, by `tb/verilator/gptp_shadow` |
| `tb/verilator/gptp_shadow` | WIDE, real counter + boundary stamper | the fabric slice with no harness-provided timestamps; classify/transport/gearbox/stamper, positional pairing for all six transmitted types, and the two equal-sequence cross-type collisions proved by delaying/replaying complete real boundary tuples (Req vs Resp and Sync vs Resp). The same gate holds a response return while two same-type peer requests cross the production tap and a start/mid-frame-stalled wide lane; two valid Signaling chasers then reuse both donor message banks, proving the queued request's event snapshot preserves its requester identity, port and exact ingress `requestReceiptTimestamp` through bank churn. Independent request/Sync warm-reset phases prove the cadence and receipt-timer bootstrap. The 158-check run goes red when the engine's type input is tied off, donor matching is reduced to sequence-only, same-type response ownership or the whole queued-request snapshot is removed, only its saved timestamp is bypassed, stale timer ownership survives reset, the receipt timer is not bootstrapped, or the return-order gate is bypassed |
| `tb/verilator/milan_dp` obj_gptp | the whole datapath | option-ON elaborates at the shipping 1x1 ENTITY shape (the leg's own -G set, 2 MHz clock -- not the obj_ax1x1 argv); the boot Pdelay_Req reaches the real MAC boundary; NO Announce without asCapable |
| `tb/verilator/milan_dp` default legs | the whole datapath | the [GPTP-OPT] tripwire: with the option OFF, CSR adjfine and adjtime still reach `timestamp_counter` through the eff muxes (a polarity swap goes red) |
| `tb/verilator/tsn_fuzz` (`fuzz_ptp.py`) | byte, the tsn-gen 802.1AS models at the CI pin | the plane's own Announce / Sync / Follow_Up / Pdelay field-by-field against the Milan v1.2 profile of 802.1AS-2011 (the Table 11-7 control byte among them), parser drop/ignore gates, BTCA under fuzz, the two-sided asCapable canary; the tally and the tracked gaps live in the generated [`hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`](../../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md) |

The option-ON verdict from #114's old Linux/sound-card shape was RED: the
baseline alone synthesized at 93.84% LUT and failed default placement. #120
re-runs the required three-directive AX7101 sweep with one cacheless RV32I
bare-metal hart and the sound-card surface absent. The final placed resource
and timing record lives in
[BAREMETAL_FIRMWARE.md](../integration/BAREMETAL_FIRMWARE.md), not in the
builder's pre-Vivado estimate.

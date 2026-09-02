<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The fabric gPTP plane

The time-sync plane of epic #110: the `gptp-processor` submodule's
micro-coded 802.1AS engine spliced into the datapath as the product's
time owner. Every product image has exactly this one GM/path/CLKV publication
owner; the verification-only option-off elaboration has none and publishes
the defined fail-safe zeros. This page is the integration
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
- **[The ownership boundary](#the-ownership-boundary)** -- one product owner and an ownerless verification elaboration
- **[Drop diagnostics](#drop-diagnostics)** -- the three refusal counters and their CSR words
- **[Verification map](#verification-map)** -- which bench proves what

## The shape

`GPTP_PLANE_EN_P` (milan_datapath parameter, **default ON**) elaborates
`KL_gptp_shadow` with four seams. The builder emits the same value into every
real build/sweep/deploy instance. `fabric_gptp: false` is refused for product
configurations because they require the fabric publication owner; the option-off ABI remains
reachable only through a direct `milan_soc.py` run as verification-only
hardware with zero gPTP owners, and its artifacts are not flashable.

The option also carries `GPTP_UCODE_HEX_P`. In a shipping SoC build this is an
absolute path to the builder's per-config 1,024-word image, generated from the
same YAML station MAC, priority1 and Milan clock as the rest of the station.
Self-contained benches retain the relative `gptp_ucode.hex` default. The Yosys
and Vivado whole-datapath manifests expand all eight donor/parent gPTP sources;
their recognizer rejects residual shell variables and missing files before
emitting a list. All OOC flows generate and validate the gPTP image (beside the
two protocol-processor ROMs) and fail if a generator is missing, fails, or
emits an empty file.

The plane has four seams:

1. **RX**: the live `rx_axis_fabric` observer seam -- input
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
- **Egress**: there is no in-line TX stamper in the trunk (the
  `ptp_ts_top` record stampers left with the general-data chain in
  `0x0002_0056`), so `KL_gptp_txstamp`
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
  engine record carries the story. The engine has no free-running PHC
  nanosecond input since Mister-M-alt/FPGA-gPTP#47: only event-specific
  ingress/egress stamps enter it, while its PHC face is control-only. The
  parent counter still feeds the shadow's ingress capture and the separate
  MAC-boundary stamper.

The parent-side synthesis comparison for #211 used
`syn/yosys/run.sh --top KL_gptp_shadow` at base
`5b680542a94523d1de2b5e66068ef0a751977fbf` and implementation
`2faca833f25268abc49a76cb0d296ae5dd6a9fd2`. The reported total cell count
fell from 204,045 to 203,960 (-85); both runs passed the tied-input and tap
purity gates. The donor's Vivado out-of-context record, including the
flattened engine and standalone uCPU results, lives with FPGA-gPTP #47.

## The ownership boundary

With the product-default option on, the fabric publication bank is the single
source for `ADP_GM` 0x624/0x628, `GPTP_PDELAY` 0x6E4, the parent at
0x730/0x734, GET_AVB_INFO, GET_AS_PATH, clock validity/asCapable and AVTP
`tu`. GM and parent are each snapshotted as one 64-bit value across either
two-half CSR read order. A GM/sync discontinuity asserts `tu` on that same
edge, then the committed bank becomes visible; no consumer can see a new
identity with an old-valid timestamp verdict. Software writes to the legacy
publication and CLKV registers cannot manufacture live fabric health.
`GET_AS_PATH` therefore serves no entries without a GM or when the selected
Announce carried no PathTrace TLV. A present TLV is the complete bounded
sequence: GM followed by up to seven tail identities. The donor stages a
candidate's full path, publishes it only when that candidate is actually taken,
clears inactive slots on shorter paths, and commits count/tail with the scalar
bank. The parent preserves raw count zero, clamps the public count, and clears
inactive tails. Its generation and Table 5.22 edge compare exactly
`(count ? GM : 0, count, active tails)`: fabric 0 <-> 1 is a real change, while
GM A->B with both counts zero leaves the served empty sequence unchanged. The
0x7DC address group remains readable compatibility state but cannot alter this
fabric-owned path or its live 0x7E4 generation.
The donor's peer-delay arithmetic stays signed: a small negative symmetric
measurement remains acceptable and does not tear down asCapable. At the parent
publication commit, that value is clamped to zero before entering the unsigned
CSR/GET_AVB_INFO contract, so a legal -1 ns sample can never appear as
`0xFFFF_FFFF` ns.

With the option off, the address map remains buildable but ownerless. GM,
parent, path and peer-delay publications are zero, sync/asCapable are zero, and
`tu` is one. Legacy writes are acknowledged and ignored: they cannot publish a
path, create clock health, or renew a lease. The verification map below proves
that attempted writes leave the fail-safe outputs unchanged. VERSION
`0x0002_0056` records removal of the final compatibility owner without
allocating new CSR addresses.

## Drop diagnostics

A field failure must distinguish silence on the link from traffic the
plane refused inside (issue #207). Three 16-bit free-running counters
answer it, each owned by the stage that drops:

- **tap** (`dbg_tap_drop_o`, `KL_gptp_shadow`): whole frames shed at the
  tap seam -- the frame FIFO overflow, a stalled forward beat, and the
  issue-#122 shed rule above, counted only once the EtherType verdict
  confirms 0x88F7.
- **parser** (`dbg_rx_drop_o`, the donor engine's `drop_cnt_o`): frames
  the 802.1AS parser refused -- wrong domain, wrong version, a declared
  length the frame does not carry, a malformed TLV chain.
- **event queue** (`dbg_ev_drop_o`): dispatch events the queue refused -
  it was full when they arrived, or an announce arrived without its
  frozen capture context (the engine folds both refusals into this one
  count).

Software reads them at CSR `0x7E8` (`{tap, parser}` in one coherent
access) and `0x7EC` (event count, zero-extended); the words are live,
read-only, write-inert, never cleared by access, and they wrap -- deltas
are the interface. Option OFF reads defined zeros from the CSR's own
parameter gate, so an absent plane is explicit, never a floating count.
Semantics, reset and rollover live in
[`REGISTER_MAP.md`](../reference/REGISTER_MAP.md).

## Verification map

| bench | faces | proves |
|---|---|---|
| gptp-processor `tb/verilator/*` | byte, model counter | the 802.1AS state machines, servo math, and the donor's planted-mutation ladder; its count lives in the donor's engine bench README under `gptp-processor/tb/verilator/engine/` at the pinned SHA and is not mirrored here, where it would drift at every repin |
| `tb/verilator/gptp_plane` | byte, REAL counter | the engine steers the parent's `timestamp_counter` closed-loop through its PHC control outputs, and its transmitted Follow_Up carries an event-specific egress timestamp while the two-step Sync body stays zero (Table 11-8). The donor removed the unread free-running engine input in Mister-M-alt/FPGA-gPTP#47 ([#211](https://github.com/kebag-logic/milan-fpga/issues/211)); the slice's live counter feeds remain separately covered by `tb/verilator/gptp_shadow` |
| `tb/verilator/gptp_shadow` | WIDE, real counter + boundary stamper | the fabric slice with no harness-provided timestamps; classify/transport/gearbox/stamper, positional pairing for all six transmitted types, and the two equal-sequence cross-type collisions proved by delaying/replaying complete real boundary tuples (Req vs Resp and Sync vs Resp). The same gate holds a response return while two same-type peer requests cross the production tap and a start/mid-frame-stalled wide lane; two valid Signaling chasers then reuse both donor message banks, proving the queued request's event snapshot preserves its requester identity, port and exact ingress `requestReceiptTimestamp` through bank churn. Independent request/Sync warm-reset phases prove the cadence and receipt-timer bootstrap. The same run also drives an accepted -40 ns exchange, requires public zero with asCapable retained, then restores a positive delay. It goes red when the public sign clamp, engine type input, donor type match, same-type ownership/snapshot, timer repairs, or return-order proof is removed |
| `tb/verilator/milan_dp` obj_gptp | the whole datapath | option-ON elaborates at the shipping 1x1 ENTITY shape (the leg's own -G set, 2 MHz clock -- not the obj_ax1x1 argv); the boot Pdelay_Req reaches the real MAC boundary; NO Announce without asCapable; live positive and negative peer-delay exchanges reach CSR/clock validity; GET_AVB_INFO carries the negative sample as byte-exact unsigned zero; and a four-identity Announce survives as an exact 74-byte GET_AS_PATH response. Fabric 0x7E4 ownership, software-staging isolation, one tail-only Table 5.22 push and identical-refresh silence are graded in the same leg |
| `tb/verilator/milan_dp` default legs | the whole datapath | the [GPTP-OPT] tripwire: with the option OFF, CSR adjfine and adjtime still reach `timestamp_counter` through the eff muxes (a polarity swap goes red) |
| `tb/verilator/tsn_fuzz` (`fuzz_ptp.py`) | byte, the tsn-gen 802.1AS models at the CI pin | the plane's own Announce / Sync / Follow_Up / Pdelay field-by-field against the Milan v1.2 profile of 802.1AS-2011 (the Table 11-7 control byte among them), parser drop/ignore gates, BTCA under fuzz, the two-sided asCapable canary; the tally and the tracked gaps live in the generated [`hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md`](../../hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md) |

The option-ON verdict from #114's earlier high-resource shape was RED: the
baseline alone synthesized at 93.84% LUT and failed default placement. #120
re-runs the required three-directive AX7101 sweep with one cacheless RV32I
bare-metal hart and fabric I2S/TDM endpoints. The final placed resource
and timing record lives in
[BAREMETAL_FIRMWARE.md](../integration/BAREMETAL_FIRMWARE.md), not in the
builder's pre-Vivado estimate.

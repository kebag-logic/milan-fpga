<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The fabric gPTP plane

The time-sync plane of epic #110: the `gptp-processor` submodule's
micro-coded 802.1AS engine spliced into the datapath as fabric, on the
way to retiring `ptp4l`/`phc2sys`/the `milan-statd` mirror chain. This
page is the integration architecture of record for #114; the donor
repo's own pages under `gptp-processor/docs/` (the resource-validation
record) carry the engine's internals and measured cost.

## Contents

- **[The shape](#the-shape)** -- one option, four seams
- **[Timestamps](#timestamps)** -- where stamps are born and how they travel
- **[What stays software until #116](#what-stays-software-until-116)** -- the flip boundary
- **[Verification map](#verification-map)** -- which bench proves what

## The shape

`GPTP_PLANE_EN_P` (milan_datapath parameter, DEFAULT OFF) elaborates
`KL_gptp_shadow` with four seams. #120's shipping AX7101 configuration opts in
explicitly after its bare-metal and sound-card area buy-back; other builds
remain bit-identical until they make the same product choice. #116 still owns
the default flip and CSR compatibility transition.

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
  {ts, sequenceId} for the engine's pending exchange. Observer-pure
  (`check_tap_purity` holds). One gPTP stack per port is the operating
  assumption -- two transmitting stacks is itself invalid, and the A/B
  bring-up keeps exactly one talking.
- **Inside the engine**, the ingress stamp ping-pongs with the message
  bank (stage at sof, commit at eof, length-qualified) -- the fabric
  bench found the single-register race this retires; the donor's
  engine v3 record carries the story.

## What stays software until #116

The CSR readback words (`ADP_GM` 0x624/8, `GPTP_PDELAY` 0x6E4, the
0x730 AS_PATH group), the `tu` bit's CLKV lease, and the rootfs
daemons. The #116 flip re-points them at the plane and carries the
VERSION story; the splice changes no CSR-visible behavior, which is
why it carries no VERSION bump.

## Verification map

| bench | faces | proves |
|---|---|---|
| gptp-processor `tb/verilator/*` | byte, model counter | the 802.1AS state machines, servo math, 34 mutations |
| `tb/verilator/gptp_plane` | byte, REAL counter | the engine steers the parent's `timestamp_counter` closed-loop; the phc_ns_i observing check |
| `tb/verilator/gptp_shadow` | WIDE, real counter + boundary stamper | the fabric slice with no harness timestamps at all; classify/transport/gearbox/stamper; 5 mutations |
| `tb/verilator/milan_dp` obj_gptp | the whole datapath | option-ON elaborates at the shipping 1x1 ENTITY shape (the leg's own -G set, 2 MHz clock -- not the obj_ax1x1 argv); the boot Pdelay_Req reaches the real MAC boundary; NO Announce without asCapable |
| `tb/verilator/milan_dp` default legs | the whole datapath | the [GPTP-OPT] tripwire: with the option OFF, CSR adjfine and adjtime still reach `timestamp_counter` through the eff muxes (a polarity swap goes red) |

The option-ON verdict from #114's old Linux/sound-card shape was RED: the
baseline alone synthesized at 93.84% LUT and failed default placement. #120
re-runs the required three-directive AX7101 sweep with one cacheless RV32I
bare-metal hart and the sound-card surface absent. The final placed resource
and timing record lives in
[BAREMETAL_FIRMWARE.md](../integration/BAREMETAL_FIRMWARE.md), not in the
builder's pre-Vivado estimate.

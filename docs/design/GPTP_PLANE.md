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

`GPTP_PLANE_EN_P` (milan_datapath parameter, DEFAULT OFF -- the shipped
shape is bit-identical until #116 flips it behind #120's baremetal
buy-back) elaborates `KL_gptp_shadow` with four seams:

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
  #117 measures it on silicon.
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
| gptp-processor `tb/verilator/*` | byte, model counter | the 802.1AS state machines, servo math, 33 mutations |
| `tb/verilator/gptp_plane` | byte, REAL counter | the engine steers the parent's `timestamp_counter` closed-loop; the phc_ns_i observing check |
| `tb/verilator/gptp_shadow` | WIDE, real counter + boundary stamper | the fabric slice with no harness timestamps at all; classify/transport/gearbox/stamper; 5 mutations |
| `tb/verilator/milan_dp` obj_gptp | the whole datapath | option-ON elaborates at the shipping 1x1 ENTITY shape (the leg's own -G set, 2 MHz clock -- not the obj_ax1x1 argv); the boot Pdelay_Req reaches the real MAC boundary; NO Announce without asCapable |
| `tb/verilator/milan_dp` default legs | the whole datapath | the [GPTP-OPT] tripwire: with the option OFF, CSR adjfine and adjtime still reach `timestamp_counter` through the eff muxes (a polarity swap goes red) |

The area verdict for option-ON is RED at the current shipping shape
(measured: the baseline alone synthesizes at 93.84% and fails default
placement); it resolves through #120's baremetal downgrade and
sound-card removal, where the verdict re-runs against the downgraded
SoC.

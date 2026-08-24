<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# gptp_shadow -- the fabric slice, wide faces, loop closed in fabric

The whole slice the #114 splice instantiates: `KL_gptp_shadow` (the
0x88F7 tap, frame FIFO, byte serializer, the gptp-processor engine, the
adjfine latch, the TX gearbox and lane) beside the real
`timestamp_counter` and `KL_gptp_txstamp` observing the TX lane as the
stand-in MAC boundary. Unlike `tb/verilator/gptp_plane` (byte faces,
exact-integer model), this bench drives the WIDE faces and NO timestamp
ever enters from the harness: ingress stamps ride the tap's
commit-pulse side FIFO, egress stamps come from the boundary observer,
and delay/offset checks are range assertions around harness-recorded
fabric time.

| phase | claim |
|---|---|
| 1 | boot Pdelay_Req byte-exact through the gearbox; the boundary stamper supplies t1 by itself, and its extracted tags, sequenceId AND messageType, are that frame's (#214) |
| 2, 3 | a fabric-timed exchange lands on the harness-records expectation; asCapable at the second exchange, not the first |
| 4 | adopt; offset in range; a short closed loop locks the REAL counter against a +100 ppm master |
| 4b | #214: a peer Pdelay_Req reusing OUR outstanding sequenceId draws our Pdelay_Resp and its Pdelay_Resp_Follow_Up, and the two returning stamps are told apart by messageType alone (0x3 and 0xA), in emission order, one stamp per frame. That collision is the systematic one on a two-board link, where both request counters start at zero and advance at 1 Hz |
| 13 | #214: with no announce refreshed the receipt timeout expires and the plane becomes grandmaster, so Announce, Sync and Follow_Up join the lane. Then every stamp of the whole run is paired with the frame it belongs to, positionally, and checked against that frame's own messageType and sequenceId, so the tag is proved for all SIX types the plane transmits rather than the three a slave-only run emits. Last in the run, because a plane that is its own grandmaster stops consuming the peer syncs the earlier phases need |
| 5 | an AVTP-ethertype frame between gPTP ones is invisible; a runt drops harmlessly and costs no drop count |
| 6 | an OVERSIZE frame dropped inside the tap FIFO cannot skew the next sync's ingress stamp (falsifies an accept-time ts push -- the commit-pulse transport pairs stamps with DELIVERED frames only) |
| 7 | a back-to-back burst overflows the tap FIFO: drops are COUNTED via the FIFO's overflow strobe (DROP_WHEN_FULL keeps s_ready high, so a ready-based counter is blind), and the plane keeps working afterwards |
| all | #211: the slice wires the steered counter into the engine's `phc_ns_i`, and that connection is checked. The engine reads the port nowhere, so nothing behavioural can see it: `dbg_eng_phc_o` is read hierarchically at `u_shadow.u_engine` and must equal the counter every cycle, and must move |

The `all` row closes a blind spot this bench had for its whole life,
and the measurement is the argument: tying the ENGINE's connection
inside `KL_gptp_shadow.sv` to `64'd0` -- a mis-wire of the shipped
slice, not of a harness -- left the run at 59 checks, 59 PASS. An input
no program reads accepts any wiring in silence, so connectivity is the
only contract left to hold, and it is the one silicon breaks. With the
gate the same tie-off gives 61 checks, 59 PASS, 2 FAIL. The two checks
prove the CONNECTION and never that the engine uses the value; the
proposal that it should not, and the amendment it needs from
[#211](https://github.com/kebag-logic/milan-fpga/issues/211), are in
[`docs/design/GPTP_PLANE.md`](../../../docs/design/GPTP_PLANE.md).

This bench found the engine's ingress-stamp race (a chaser's sof
overwrote the previous frame's stamp before its event dispatched --
every pdelay skewed +half the inter-frame gap), fixed in the donor as
the per-bank eof-committed stamp; phase 2 is red under any engine
without it. Five planted mutations (a deaf classifier lane, an
accept-time ts push, shifted stamper sequence lanes, an eof-timed arm,
the single-register engine revert) turn the run red, and five more on
the #214 type tag: dropped, read from the transportSpecific nibble
beside it, frozen at a constant, and never latched at all each turn six
checks red, while one that is correct for every type EXCEPT Announce
turns exactly one, the whole-run pairing check, which is the reason
that check and phase 13 exist. A sixth, re-registering the slice's
type port instead of passing it through, turns the sample-cycle skew
check red: the engine samples the txts face combinationally on the
valid pulse, so a register there would hand it the previous stamp's
type.

```sh
git submodule update --init gptp-processor   # once
make        # regenerates gptp_ucode.hex from the submodule, builds, runs
```

Exit 0 = PASS; the tally line is the record.

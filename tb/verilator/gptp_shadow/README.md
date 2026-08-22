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
| 5 | an AVTP-ethertype frame between gPTP ones is invisible; a runt drops harmlessly and costs no drop count |
| 6 | an OVERSIZE frame dropped inside the tap FIFO cannot skew the next sync's ingress stamp (falsifies an accept-time ts push -- the commit-pulse transport pairs stamps with DELIVERED frames only) |
| 7 | a back-to-back burst overflows the tap FIFO: drops are COUNTED via the FIFO's overflow strobe (DROP_WHEN_FULL keeps s_ready high, so a ready-based counter is blind), and the plane keeps working afterwards |

This bench found the engine's ingress-stamp race (a chaser's sof
overwrote the previous frame's stamp before its event dispatched --
every pdelay skewed +half the inter-frame gap), fixed in the donor as
the per-bank eof-committed stamp; phase 2 is red under any engine
without it. Five planted mutations (a deaf classifier lane, an
accept-time ts push, shifted stamper sequence lanes, an eof-timed arm,
the single-register engine revert) turn the run red, and four more on
the #214 type tag (dropped, read from the transportSpecific nibble
beside it, frozen at a constant, never re-latched) each turn exactly
the five type checks red.

```sh
git submodule update --init gptp-processor   # once
make        # regenerates gptp_ucode.hex from the submodule, builds, runs
```

Exit 0 = PASS; the tally line is the record.

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
fabric time. The two collision phases may DELAY one complete real
boundary tuple and replay that exact tuple after later raw returns; the
harness still supplies no timestamp or tag. The one-slot test gate lets
later returns pass and releases only on an idle raw cycle, so it does not
exercise the separate one-open-return limitation of donor #31.

| phase | claim |
|---|---|
| 1 | boot Pdelay_Req byte-exact through the gearbox; the boundary stamper supplies t1 by itself, and its extracted tags, sequenceId AND messageType, are that frame's (#214) |
| 1c | #214: hold the boot Pdelay_Req's real boundary tuple, inject a peer request with that same sequenceId, and let the response and its unclaimed Follow_Up stamps arrive first. The response stamp builds the response's own Follow_Up, the type-A stamp consumes no claim, and releasing the original type-2 tuple preserves the measured peer delay. Sequence-only credit goes red. |
| 2, 3 | a fabric-timed exchange lands on the harness-records expectation; asCapable at the second exchange, not the first |
| 4 | adopt; offset in range; a short closed loop locks the REAL counter against a +100 ppm master |
| 13 | #214: after the receipt timeout makes the plane grandmaster, let its Announce stamp dispatch, then hold the next real Sync tuple and inject a peer request with the same sequenceId. The response stamp must build Resp_FU, its type-A stamp must leave Sync pending, and only the released type-0 tuple may build Sync Follow_Up with that exact boundary time. Engine-face order is exactly `3,A,0`, with zero gate conflicts/event drops; Announce, Sync and Follow_Up also complete the positional all-six-type tag proof. |
| 5 | an AVTP-ethertype frame between gPTP ones is invisible; a runt drops harmlessly and costs no drop count |
| 6 | an OVERSIZE frame dropped inside the tap FIFO cannot skew the next sync's ingress stamp (falsifies an accept-time ts push -- the commit-pulse transport pairs stamps with DELIVERED frames only) |
| 7 | a back-to-back burst overflows the tap FIFO: drops are COUNTED via the FIFO's overflow strobe (DROP_WHEN_FULL keeps s_ready high, so a ready-based counter is blind), and the plane keeps working afterwards |

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
type. At this pin, tying the engine's newly consumed `txts_type_i` to
zero turns the run red with 20 failures (50 PASS of 70 checks reached),
starting at the response-first collision and cascading through the
deliberately uncompleted pdelay ladder. Swapping type 2 and type 3 only
at the engine face turns 22 of 70 reached checks red while the raw
boundary extraction stays unchanged. Masking messageType out of both
event and claim comparisons (the donor's sequence-only mutation) turns
13 of 91 reached checks red, while bypassing the test-only return-order
gate turns 4 of 85 reached checks red. The restored integration is
99/99.

```sh
git submodule update --init gptp-processor   # once
make        # regenerates gptp_ucode.hex from the submodule, builds, runs
```

Exit 0 = PASS; the tally line is the record.

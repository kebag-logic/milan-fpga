<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# gptp_plane -- the time-sync plane against the real PHC

Integration bench for issue #110: the `gptp-processor` submodule's
`KL_gptp_engine` married to the PARENT's real
`hdl/ieee8021as/ptp_timestamp/timestamp_counter.sv` -- the exact pairing
the datapath splice will instantiate, proven closed-loop before any
fabric is committed. The donor repo's own engine suite proves the
802.1AS protocol details against a MODEL of the counter; here the model
is replaced by the counter itself (Q8.24 accumulator, 8.0 ns increment,
the 125 MHz shape), and the wrap carries the one piece of fabric the
splice adds beyond wires: the adjfine latch (the engine pulses an
addend, the counter wants a level).

What it proves:

| phase | claim |
|---|---|
| 1 | the plane boots beside the ticking counter; one pdelay exchange measures 600 ns and does not raise asCapable |
| 2 | a live auto-answering peer raises asCapable at the second exchange |
| 3 | a better announce is adopted; the publish bank carries the GM identity and role flags |
| 4 | closed loop vs a +100 ppm master 1 ms ahead in counter time: ONE adjtime re-base near +1 ms (the correction negates the offset), the latched adjfine level lands at the +100 ppm ideal (13,421 Q8.24 units, within 15%), the measured offset locks under 150 ns, and the REAL counter's advance tracks the master's within 100 ns over the last four sync intervals |
| 5 | announce silence rides to grandmaster; the two-step Sync's ten reserved octets are zero (802.1AS-2011 Table 11-8) and its paired Follow_Up carries a plausible event-specific egress timestamp |

| 6 | FPGA-gPTP #109: the link delay verdict, to the nanosecond, against the real counter. The peer's clock is this one plus a constant, so the neighborRateRatio is exactly 1 and the residence sets the delay. -3, -80, -81, -263, -800, -801 and -5,000,000 ns keep asCapable, publish the delay floored at -800 ns, and are subtracted exactly by the next Follow_Up with no PHC step; 800 ns keeps asCapable; 801 ns clears it, its next Follow_Up is not used, and an ordinary exchange requalifies the port. The engine's word is signed here: the public clamp to 0 is `gptp_shadow`'s and `milan_dp`'s |

`make link-delay` (part of the default target) plants eight defects in the
pinned generator, one image each, on the binary `run` built: the old -80 ns
window, no floor, the used value clamped to 0, a floor at 0, a floor at
-799 ns, publication before the floor, 801 ns good and 800 ns bad. Each must
fail the checks `link_delay.py` names, and the unplanted image passes them all.

Mister-M-alt/FPGA-gPTP#47 resolves the blind spot found in PR #113's review by
removing the engine's unread free-running nanosecond input, its dispatch
preload, and its gather leg. This direct-engine wrapper therefore connects the
real counter only to the engine's PHC adjustment outputs; ingress and egress
timestamps enter through `rx_ts_i` and `txts_ns_i` for their specific events.

That removal does not apply to the fabric slice's live counter wire. It is read by
`KL_gptp_shadow.sv`'s `ts_arr_r <= phc_ns_i` and, on the egress side since
[#360](https://github.com/kebag-logic/milan-fpga/issues/360), by
`KL_gptp_txret.sv`, which captures the PHC when a launch record crosses into
the plane's domain and reconstructs the frame's launch from it. The
first-beat stamper that used to read the counter here was retired with that
change: it took its time at the datapath's MAC boundary, upstream of the
MAC's queueing. The wire remains covered: tying the slice's counter consumers
in `tb/verilator/gptp_shadow`'s wrapper to
`64'd0` turns that bench red across its delay, capability, publication, servo,
and timestamp-ring checks. So a mis-wire of the counter into the shipped slice
is still caught. The distinction and removal decision are tracked by
[#211](https://github.com/kebag-logic/milan-fpga/issues/211).

The harness derives every injected egress return's `sequenceId` and
`messageType` from the selected transmitted frame and grades both fields,
including a nonzero Pdelay sequence and a Sync. This is interface regression
coverage only: the bench injects timestamps directly into the engine and has
no boundary stamper, so it proves neither boundary extraction nor
equal-sequence claim routing. Those integration properties belong to
`tb/verilator/gptp_shadow`.

Timescale note: the bench clock is 2 MHz while the counter keeps its
8.0 ns/tick shape, so counter time runs 62.5x slower than the bench
timer's millisecond. That is deliberate and self-consistent -- the
µcode's servo gain is generated for the bench's ticks-per-sync-interval
(`--clk-hz 2000000`, one sync per 250k ticks), and every timestamp in
the harness is counter-time ns.

```sh
git submodule update --init gptp-processor   # once
make        # regenerates gptp_ucode.hex from the submodule, builds, runs
```

Exit 0 = PASS; the tally line is the record.

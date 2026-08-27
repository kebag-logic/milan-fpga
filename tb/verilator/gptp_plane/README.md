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

Mister-M-alt/FPGA-gPTP#47 resolves the blind spot found in PR #113's review by
removing the engine's unread free-running nanosecond input, its dispatch
preload, and its gather leg. This direct-engine wrapper therefore connects the
real counter only to the engine's PHC adjustment outputs; ingress and egress
timestamps enter through `rx_ts_i` and `txts_ns_i` for their specific events.

That removal does not apply to the fabric slice's live counter wire. It is read by
`KL_gptp_shadow.sv`'s `ts_arr_r <= phc_ns_i` and `KL_gptp_txstamp.sv`'s
first-beat `ts_r <= phc_ns_i` and remains covered:
tying both slice consumers in `tb/verilator/gptp_shadow`'s wrapper to
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

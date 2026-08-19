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

Known blind spot, on purpose: `phc_ns_i` (the engine's live-clock
snapshot input) is dispatch metadata in the current µcode -- no handler
consumes it yet -- so a mis-wire of that one input is invisible to these
checks. The loop closes through the ingress/egress timestamps. Its first
functional consumer is a donor-side µcode revision; the splice round
carries the observing check.

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

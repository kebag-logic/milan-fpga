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
| 5 | announce silence rides to grandmaster; the two-step Sync's ten reserved octets are zero (802.1AS-2011 Table 11-8) and its paired Follow_Up carries a plausible live timestamp. It does NOT observe `phc_ns_i`: see the note below |

The `phc_ns_i` blind spot from PR #113's review is RE-OPENED at the
current submodule pin for the ENGINE's port, and this bench does not
close it. Measured: tying `.phc_ns_i` to `64'd0` in
`gptp_plane_wrap.sv` leaves the run at 18 checks, 18 PASS; on `dev` at
the old pin `5c330fc8` the same tie failed `origin is the real
counter`. `KL_gptp_engine`'s input has no reader at this pin: the
microcode generator emits no `GATH` (FPGA-gPTP #10 removed the one that
gathered the Sync body's origin), and `RTS1`, the register `phc_ns_i`
feeds through `disp_ts1_r`, is read by no program. The Follow_Up's
preciseOriginTimestamp comes from the TX timestamp instead, which this
bench drives itself, so no assertion here can restore observability
while the input is unread.

Scope that carefully, because the same name means two things. What is
unread is the ENGINE port, which is what this wrapper instantiates.
The SLICE's `timestamp_counter` wire is read by
`KL_gptp_shadow.sv:197` and `KL_gptp_txstamp.sv:95` and IS covered:
tying both slice consumers in `tb/verilator/gptp_shadow`'s wrapper to
`64'd0` turns that bench red, 40 checks with 31 PASS and 9 FAIL. So a
mis-wire of the counter into the shipped slice is caught; only the
engine's own port is invisible. Tracked as
[#211](https://github.com/kebag-logic/milan-fpga/issues/211), which
asks the real question: should the engine consume `phc_ns_i`, or is
that port vestigial at this pin?

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

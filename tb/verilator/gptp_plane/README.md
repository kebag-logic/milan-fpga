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
| 5 | announce silence rides to grandmaster; the two-step Sync's ten reserved octets are zero (802.1AS-2011 Table 11-8) and its paired Follow_Up carries a plausible live timestamp. It does NOT observe `phc_ns_i`: phase 6 is why |
| 6 | the ENGINE's `phc_ns_i` port carries the steered counter, cycle for cycle, and moves. A WIRING gate, not an observation: it proves the connection, never that the engine uses the value |

Phase 6 is the answer this branch PROPOSES to
[#211](https://github.com/kebag-logic/milan-fpga/issues/211), and the
reasoning matters more than the two checks. `KL_gptp_engine`'s
`phc_ns_i` has no reader in the shipped microprogram: the generator
emits no `GATH` and `RTS1`, the register the port feeds through
`disp_ts1_r`, is read by no program. #211 records two outcomes and
both need `gptp-processor` edits this repository cannot make, so PR
#243 asked #211 for a third one, RETAIN UNREAD AND GATE THE WIRING;
until a maintainer amends #211 that outcome is proposed, not decided.
The argument for it is that no 802.1AS field can carry a free-running
clock read.
Every timestamp on the wire is an event message's ingress or egress
stamp -- the Follow_Up's preciseOriginTimestamp is the Sync's egress
time (11.4.4.2.1), the pdelay legs carry the exchange's own stamps --
and the two-step Sync's own ten octets are reserved and transmitted as
zero (Table 11-8). The one consumer the port ever had, a `GATH` filling
that Sync body, was a Table 11-8 violation, and FPGA-gPTP #10 removed
it. So no behavioural check here can observe the port, and one written
anyway would be observing the harness: the TX timestamp this bench
drives itself.

What an unread input still owes is its wiring, and that is what was
silently unchecked. Measured on this bench before phase 6, at pin
`c33fb1af`: tying `.phc_ns_i` to `64'd0` in `gptp_plane_wrap.sv` left
the run at 18 checks, 18 PASS, and so did `64'd123456789`. The gate is
`tap_eng_phc_o`, read hierarchically from inside the engine instance so
that the tie-off is visible to it; a tap on the wrapper's own
`phc_ns_o` would have stayed green under exactly that tie-off, which is
measured too. With phase 6 the same tie-off gives 20 checks, 18 PASS,
2 FAIL, and a live-but-wrong connection (`phc_ns_o + 64'd1`) gives 19
PASS, 1 FAIL.

Scope that carefully, because the same name means two things. What is
unread is the ENGINE port, which is what this wrapper instantiates.
The SLICE's `timestamp_counter` wire is read by
`KL_gptp_shadow.sv`'s `ts_arr_r <= phc_ns_i` and `KL_gptp_txstamp.sv`'s
first-beat `ts_r <= phc_ns_i` and IS covered:
tying both slice consumers in `tb/verilator/gptp_shadow`'s wrapper to
`64'd0` turns that bench red, 61 checks with 45 PASS and 16 FAIL. The
slice's own connection to the ENGINE port is a third thing again, and
it was invisible until `gptp_shadow` grew the same wiring gate.

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

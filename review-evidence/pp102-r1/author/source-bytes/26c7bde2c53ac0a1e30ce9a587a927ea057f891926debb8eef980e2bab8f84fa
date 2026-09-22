<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# side_port — KL_pp_side_port + KL_pp_trace_ring suite

Proves the management side-port ([02 §7](../../docs/architecture/02_interfaces.md)
class E, [07 §5.5](../../docs/architecture/07_memory_maps.md) window map) and the
P-TRACE-RING debug ring (F01.5: 256 × 128 b) behind window 0x40000: `make` =
build + run, exit 0 = PASS, 368 checks.

The C++ harness is an independent model, never DUT logic: five window-backend
stubs with programmable wait states and deterministic per-address data, an
independent 256 × 4-lane ring model with its own mod-2^16 counter, and a host
that holds `req_valid` until `rvalid` (F02.7 pready semantics). The top is
`side_port_tb_wrap.sv`: side-port **A** (`EN_FW_ASSIST_P = 1`, all six windows
live) with the REAL trace ring wired behind window 0x40000, plus side-port
**B** at the F01.5 default (`EN_FW_ASSIST_P = 0`, auto-acked backends) proving
window 0x50000 vanishes when the parameter is off.

Covered: window decode exact at every boundary word (first/last of all six
windows, the 0x300FF control-window top, and five unmapped addresses:
0x30100, 0x3FFFF, 0x60000, 0x70000, 0xFFFFF → err, nothing forwarded); RO
writes (dbg/snap/trace) refused with `err_o` and never forwarded; the 07 §2
rule — image writes forwarded byte-exact pre-enable, refused post-enable,
reads always allowed; RW writes (ctrl/fw) forwarded byte-exact through 3/4
backend wait states with exactly one response; error responses single-cycle
with `rdata = 0`; single-outstanding acceptance (a held request accepted once;
a mid-wait address change fires nothing). Ring: 5-record fill read back
bit-exact per 32-bit lane via the window path (lane 0 = record bits [127:96],
class-A MSB-first); 300 writes wrap — counter 300 via both the port and the
window, index 44 the oldest survivor, all 256 records bit-exact vs the model;
read-during-write of the SAME record returns the OLD record (read-first) while
the counter advances, and a different-record read during a write is
undisturbed.

TB glue (an integration choice — 07 §5.5 does not pin the in-window layout):
trace-window offset bit 10 clear = ring records addressed
{record[7:0], lane[1:0]}; bit 10 set = the 16-bit write counter. The C++
model mirrors the same map.

Mutation-proven 2026-08-11 (backup → sed → run red → restore → rerun green):

| # | Mutation | Result |
|---|---|---|
| 1 | `KL_pp_side_port` dbg window loses its RO refusal (`fwd_ok_w = !we_i` → `1'b1`) | 4 of 368 fail: both dbg RO-write refusals + both not-forwarded checks |
| 2 | `KL_pp_trace_ring` counter step `16'd1` → `16'd2` | fails count-5, count-300, and every other record readback (records land on even indices only) |
| 3 | `KL_pp_trace_ring` lane mux flipped LSB-first (`(LANES_C-1-l)*32` → `l*32`) | every multi-lane readback fails with lanes 0↔3 / 1↔2 swapped |

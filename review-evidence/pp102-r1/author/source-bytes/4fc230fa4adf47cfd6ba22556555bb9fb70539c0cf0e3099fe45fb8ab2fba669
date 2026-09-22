<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# syn/ooc — the µCPU area experiment

The gate experiment of
[`docs/10_RESOURCE_AND_EFFORT.md` §6](../../docs/10_RESOURCE_AND_EFFORT.md):
out-of-context Vivado synthesis of the µCPU skeleton at the reference
platform's ship part, using the same instrument as every anchor in that
document (post-synthesis hierarchical utilization). This directory is
deliberately device-specific — it prices this architecture against one real
die; the RTL itself stays vendor-neutral (`hdl/README.md` rule 1).

```sh
cd <workdir>
python3 <repo>/hdl/aecp/ucode/gen_ucode.py -o ucode.hex   # ROM image for $readmemh
vivado -mode batch -source <repo>/syn/ooc/ucpu_ooc.tcl -nojournal -log ooc.log
```

## Result of record — 2026-08-11, Vivado 2026.1, xc7a100t-fgg484-2

| Metric | Value |
|---|---|
| Slice LUTs | **1,068** (936 logic + 132 as distributed RAM) |
| Registers | 491 |
| Block RAM | 3 × RAMB36 (the 2048 × 48 µcode ROM) |
| DSP | 0 |
| WNS at 100 MHz (`P-CLK-HZ`), OOC | **+2.541 ns** (0 failing endpoints) |

Sanity held: the register file inferred as distributed RAM (not the +894-LUT
flop-mirror failure mode), the ROM as block RAM (its contents cannot be
constant-folded into the decode), and the only synthesis warnings are the two
constant-1 strobe bits that are true by construction. The functional suite
(`tb/ucpu/`, mutation-proven; 92 checks at that date, and it has grown since —
run the suite rather than trusting this number) ran green on the same RTL and
the same ROM image before synthesis.

## Re-measured 2026-08-13 — after the flow-controlled response buffer

The response-buffer face gained `rb_ready` when the buffer moved into main
memory ([03 §7.1](../../docs/architecture/03_packet_engine.md)), so the number
above was re-taken on the same instrument, same part, same ROM image:

| Metric | 2026-08-11 | 2026-08-13 |
|---|---|---|
| Slice LUTs | 1,068 (936 + 132 distributed RAM) | **1,070** (938 + 132) |
| Registers | 491 | 491 |
| Block RAM | 3 × RAMB36 | 3 × RAMB36 |
| WNS at 100 MHz, OOC | +2.541 ns | **+2.586 ns** |

Two LUTs for a stall arm the whole µISA needed anyway. The reason it is that
cheap is the one design decision in `KL_aecp_resp_buf`: its `wr_ready_o` is a
REGISTER, so nothing in the µCPU's stall path reaches into the buffer's address
arithmetic and back. Driven combinationally from the write address instead, the
same feature cost ~1 ns of WNS on the whole processor.

The number is a **skeleton** measurement: dispatch handshake, hazard-key
extraction and the deadline/abort arm will grow it. The bracket it collapses
(+1,200…+2,500 ESTIMATE) survives a 2× growth allowance.

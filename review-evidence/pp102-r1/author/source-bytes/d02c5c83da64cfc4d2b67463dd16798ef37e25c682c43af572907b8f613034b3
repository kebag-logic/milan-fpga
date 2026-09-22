<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# resp_buf — KL_aecp_resp_buf suite

Proves the [03 §7](../../docs/architecture/03_packet_engine.md) AECP response
buffer now that it lives in the integrator's **main memory** instead of the
fabric: `make` = build + run, exit 0 = PASS, **64 checks**.

## Why the block exists

The response an AECP command builds is up to 592 bytes (the 07 §3.2 worst-case
descriptor plus the 06 §8 header record and the 4-byte prefix). Held as fabric
state inside `KL_aecp_engine` it measured **5,079 flip-flops and 3,495 LUTs**
on the reference part (xc7a100t, Vivado 2026.1, post-synthesis out-of-context
at the 1-stream shape) — and those were the instances the placer could not pack
on a die whose 135 block-RAM tiles were already 100 % used. It is not a cache,
it is never read while it is written, and only the frame builder reads it: it
belongs behind a memory port.

## What the harness is

Two models, neither of them a copy of DUT logic:

1. **A latency-injecting memory BFM with both channels.** Read latency **29
   clocks and write latency 23 BY DEFAULT — never zero**: the reference SoC
   measures ~1424 ns on a miss to main memory, and a buffer tested only against
   zero-latency memory is untested against the thing that makes it hard. The
   same BFM plays a bridge that never accepts anything (`off`), one that fails
   every write (`werr`), and one that answers a chosen beat with `rsp_err`.
2. **A contract model of the memory image** — bytes below 12 dropped, bytes at
   or past `RESP_BYTES_P` dropped, the *m* strobed bytes of a write laid out
   BIG-ENDIAN from `wr_addr` upward, a byte whose strobe is 0 left alone. Every
   payload check compares the DUT's *streamed bytes* **and** the BFM's memory
   image against that model, so a buffer that agrees only with itself fails.

`MEM_TIMEOUT_CYC_P` is compressed to 96 so the "no bridge at all" arm runs in a
few hundred clocks; the BFM's latencies stay well inside it.

## What it proves

| Check | The property |
|---|---|
| R1 | a whole response round-trips: the streamed bytes and the memory image both equal the contract model, in **one** read burst and exactly the lane writes the write pattern implies |
| R2 | the 06 §8 header record is **dropped**, and bytes 8..11 — which share lane 1 with byte 12 — are never clobbered |
| R3 | a 4-byte field that **straddles a lane boundary** survives on both sides (the one-byte-per-cycle absorb is what makes this need no special case) |
| R3b | a GET_DYNAMIC_INFO status byte can patch an earlier record-header lane, then resume forward, without corrupting either pass |
| R4 | the write face is **flow controlled**: a lane-closing write is held for at least the write latency, one inside the open lane is not, and back-pressure does not change a byte |
| R5 | latency is not a correctness parameter — fast, default and slow memory give identical payloads |
| R6 | `rsp_ready` is real back-pressure: a builder taking a byte every six cycles still gets every byte, in order, exactly once |
| R7 | beats past the emitted length are **drained**, never left on the bridge |
| R8 | a zero-length response costs no read burst at all |
| R9 | a **tied-off master** degrades: the write face goes permanently ready rather than parking the µCPU, the fault is raised, and no byte is ever offered |
| R10 | it heals on the next response with no reset |
| R11 | a bridge that reports a write error voids the response (fault 2) |
| R12 | a bridge that reports a read error voids it mid-stream (fault 4) |
| R13 | a write past the capacity is dropped, never wrapped to the start |
| R14 | back-to-back responses of different lengths do not bleed into each other |

The system-level proof that none of this changed the wire lives in
[`tb/pp_top`](../pp_top/README.md) section B: byte-exact `READ_DESCRIPTOR`
responses through a latency-injecting response memory, the payload compared
against the memory image itself, and the measured cost of the response path in
clocks against the IEEE 1722.1 §9.2.1.1 100 ms budget.

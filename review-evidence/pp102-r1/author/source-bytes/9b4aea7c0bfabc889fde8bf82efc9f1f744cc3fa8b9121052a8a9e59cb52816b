<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# rx_slots — KL_pp_rx_slots suite

Proves the RX slot pool (`hdl/packet_engine/KL_pp_rx_slots.sv`, the "RX slot
RAM" row of [03 §2](../../docs/architecture/03_packet_engine.md) and the
drop6/rx_overrun gate of 03 §3): `make` = build + run, exit 0 = PASS,
130 checks.

The C++ harness is an independent model of the pool CONTRACT, never DUT
logic: 4 slots × 576 bytes (F01.5), a saturating 16-bit refused-while-full
counter, wr_last closes the stream, commit latches the accepted-byte count,
abort/free return slots. It deliberately assumes NO grant policy — the
granted index is an opaque handle, only required to have been free in the
model — so the lowest-free encoder is implementation, not contract, and the
suite survives a different encoder. Combinational outputs (grant, slot,
slots_free, slot_len) are sampled pre-edge; the sync-read rd_data_o is
sampled post-edge, one cycle after rd_en, as the port contract states.

Covered: reset state; all four slots filled with distinct generator
patterns at lengths 60 / 82 / 536 (max command PDU) / 576 (full slot) with
byte-exact readback and latched lengths, in BOTH commit forms (commit
coincident with the last byte, and one cycle later — the same-cycle byte
must count); 5th alloc refused + counted; a held request counting per
cycle; abort mid-frame returning the slot for immediate realloc with the
old bytes unreadable and the neighbor slot undisturbed; 3 full
free/realloc walks of the whole pool with zero leaks; interleaved
write-one-slot-while-reading-another with every read byte-exact; bytes
after wr_last dropped (length stops at last); writes past 576 dropped
(length clamps, first 576 bytes intact); free of a free slot a no-op;
alloc refused mid-write WITHOUT an overrun count while slots remain free
(a frame-serial refusal is not a drop); and the overrun counter saturating
at 0xFFFF over a 70,000-cycle full-pool soak — no wrap.

Mutation-proven 2026-08-11 (each applied to a copy-backed original,
restored + rerun green after):

| # | Mutation (sed on the RTL) | Fails |
|---|---|---|
| M1 | overrun saturation guard removed (`ovr_cnt_r != OVR_MAX_C` → `1'b1`): counter wraps | 2 of 130 (T8 saturated / no wrap) |
| M2 | commit length drops the same-cycle final byte (`wr_len_now_w` → `wr_ptr_r`) | 8 of 130 (every same-cycle-commit length in T2/T5) |
| M3 | abort leaks the slot (`writing_r[cur_slot_r] <= 1'b0` removed from the abort arm) | 19 (pool leaks: T4 abort/realloc, all three T5 walks, T10 grant; exit 1) |

All three mutants change behavior (no equivalent mutants). M3's fail count
is against 118 reached checks — with the pool leaked, bad-handle guards
short-circuit some per-slot loops rather than crash the harness.

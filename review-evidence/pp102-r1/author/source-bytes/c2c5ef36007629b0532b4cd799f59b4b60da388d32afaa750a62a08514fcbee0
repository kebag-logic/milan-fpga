<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# tx_slots — KL_pp_tx_slots suite

Proves the TX slot pool (`hdl/packet_engine/KL_pp_tx_slots.sv`) implements the
[03 §7](../../docs/architecture/03_packet_engine.md) response-buffer and
[03 §8](../../docs/architecture/03_packet_engine.md) serialize contract at the
F01.5 shape "P-TX 4x576 + 1600": `make` = build + run, exit 0 = PASS, 95 checks.

The C++ harness is an independent contract model, never DUT logic: it keeps its
own slot lifecycle (FREE/ALLOC/READY/STREAM), its own per-slot byte images, and
its own free/ready accounting — no pipeline, no skid, no address math shared
with the RTL. Serialize outputs are sampled pre-edge, exactly what the TX
arbiter's registers would see.

Covered: allocation policy — plain allocation walks 0..3 lowest-first and never
returns the oversize slot even when it is the only one free; an oversize
allocation (the Δ8 READ_DESCRIPTOR class, Milan §5.4.1) is granted slot 4 only
and waits for it while 0..3 sit free; the grant is a one-cycle pulse.
Release aligned with the first serializer-request edge wins before acceptance,
emits no byte, and frees the slot. Release aligned with the final beat is also
lossless and returns the slot directly to FREE.
Byte-exact write/commit/serialize on all five slots with header-after-payload
random-access writes (payload offsets first, header offsets last, plus an
overwrite); random ser_ready_i drops (55–80%) with an explicit hold check —
a stalled byte and its ser_last must persist unchanged, the stream stalls and
never skips; full-ready streaming moves exactly one byte per cycle; ser_last
rides the final byte; the slot auto-frees on the last consumed byte and is
immediately reusable (re-alloc returns the freed index, new content streams
byte-exact); two committed slots are serviced strictly one at a time with the
second request held throughout the first stream; a serialize request against
an uncommitted slot is ignored without state damage; a write after commit is
discarded (the queued frame is immune to its builder); 1-byte, full-576 and
full-1600 length boundaries; a zero-length commit is freed on service without
emitting a byte; quiescence (no spurious grants or bytes when idle).

Mutation-proven 2026-08-11 (each applied to a copy-backed original via sed,
run red, restored, rerun green — 81/81):

| # | Mutation | Result |
|---|---|---|
| M1 | ser_last off-by-one: `fetch_idx_r == cur_len_w - 1` → `== cur_len_w` (last never fires) | fails 41 of 81 |
| M2 | serializer read-enable stall gate `(!out_valid_r \|\| ser_ready_i)` removed — prefetch overruns the output register under backpressure | fails 18 of 81 |
| M3 | auto-free on eof removed (`done_w` no longer returns the slot to FREE) | fails 27 of 81 |
| M4 | plain-alloc picker loop widened into the oversize slot (policy break: plain alloc may return 4) | fails 2 of 81 |

M5, added 2026-08-19 at the current 95-check shape, removes release priority
from the first serializer-request edge. It fails 1 of 95 because the canceled
frame emits bytes. Restoring release priority passes 95 of 95.

The original four are behavior-changing mutants (no equivalent mutants recorded); M2 is
invisible to full-ready streams by construction and is caught by the
random-backpressure frames, which is exactly the class of defect it plants.

<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# dispatch — KL_pp_normalizer + KL_pp_dispatch suite

Proves the normalized-transaction path of
[03 §4](../../docs/architecture/03_packet_engine.md) (the one 393-bit record,
F03.3 ALLOC → DECODED → DISPATCHED) and 03 §5 (four producers RX / TIMER /
SELF / MGMT into per-engine dispatch queues), through the two DUTs wired
end-to-end in `tb_dispatch_top.sv`: `make` = build + run, exit 0 = PASS,
179 checks.

The C++ harness is an independent model of the RECORD CONTRACT, never DUT
logic: `Rec` re-encodes pp_txn_t from the 03 §4 declared widths alone
(packed struct, first field = MSB; the field-offset table in `sim_main.cpp`
sums to 393), and every popped record is compared word-for-word — one
flipped bit anywhere in normalize → enqueue → pop fails a check. Per-queue
`std::deque`s carry the expected pop order. Registered outputs are sampled
pre-edge; accept strobes (`*_ready_o`) are combinational and sampled
pre-edge in the same cycle they fire.

Covered: reset state (no heads, zero levels, zero counters, no strobes);
the dispatch-ROM seam mirroring the presented beat (hz_valid/protocol/
opcode) with the class/key answer folded into the record; one RX beat per
protocol ADP / ACMP / AEM / MVU / AA with full-record integrity — origin +
arrival stamping, per-class budget selection (ADP/ACMP/AECP budgets all
distinct), hazard class+key, tx_slot = NULL, ADP+ACMP → multicast
disposition vs AECP → unicast — and routing to exactly one queue (leak
checks on the other two); deadline ms rollover (arrival 0xFFFFFFF0 + 50 →
0x22); TIMER/SELF/MGMT records passing through bit-exact (xorshift-filled,
every field non-trivial); all four producers presented in the SAME cycle
accepted in the fixed 03 §5 order RX > TIMER > SELF > MGMT, exactly one
accept strobe per cycle, records popped in that order; queue-full = STALL
never drop (capacity DEPTH+1 in the queue proper, +1 in the normalizer
stage; the next producer request holds for 6 observed cycles without an
accept, then is delivered intact after the drain — nothing lost, nothing
reordered); the stall-cycle counter cycle-exact (+5 over 5 stalled edges)
and frozen once the stall ends, other queues' counters untouched;
independence (ADP and ACMP flow while AECP is full); head bit-stable
across a pop stall with the level unchanged; and a 12-record cross-queue
interleave from all four producers keeping per-queue FIFO order.

Full policy note: 03 §5 does not state an explicit drop-vs-stall rule for
the dispatch FIFOs — but F03.2 marks the RX slot pool as the LAST drop
gate, F03.3 has no drop arc after ALLOC, and 03 §6 (e) forbids silent
drops, so the implementation backpressures (producers stall) and the
per-queue "overflow" counters count stalled cycles, not lost records. The
producer priority is likewise implemented in the 03 §5 listed order 1–4;
the doc numbers the producers but does not spell out an arbitration rule.

Mutation-proven 2026-08-11 (each applied to a copy-backed original,
restored + rerun green after):

| # | Mutation (sed on the RTL) | Fails |
|---|---|---|
| M1 | normalizer: TIMER accept strobe drops the `!rx_valid_i` term — TIMER no longer yields to RX | 1 of 179 (T6 "exactly one accept got 2") |
| M2 | normalizer: deadline loses the budget term (`now_ms_i + budget` → `now_ms_i`) | 12 of 179 (every RX record compare in T2/T3/T6/T8/T10 + both T4 rollover checks) |
| M3 | dispatch FIFO: full-detect off-by-one (`cnt_r == DEPTH_P` → `cnt_r > DEPTH_P`) — a push at DEPTH wraps the write pointer over the oldest entry | 8 of 179 (T7 stall never observed, drain corrupt seq 28673→28677, T10 order corrupt, residue at end) |

All three mutants change behavior (no equivalent mutants). M3 is the
load-bearing one: it converts the documented stall-never-drop contract into
silent overwrite, and the suite sees both the missing stall and the
corrupted records.

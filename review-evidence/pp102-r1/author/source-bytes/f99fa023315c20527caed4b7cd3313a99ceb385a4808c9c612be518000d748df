<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# tx_arbiter — KL_pp_tx_arbiter suite

Proves the TX arbiter (`hdl/packet_engine/KL_pp_tx_arbiter.sv`) implements the
[03 §8](../../docs/architecture/03_packet_engine.md) frame-atomic priority
merge with the [08 §2](../../docs/architecture/08_timing.md) T-TX-AGING
starvation guard: `make` = build + run, exit 0 = PASS, 66 checks.

The harness (`tx_arbiter_harness.sv`) wires the arbiter to the REAL
`KL_pp_tx_slots` pool with nothing in between — the ser_* port match is
proven by elaboration, and every streamed byte crosses the actual
pool-serializer contract. The C++ reference model re-implements only the
arbitration POLICY from the doc (priority map, solicited mask, aging rule,
pacing rule) — no FSM, no serializer, no memory shared with the RTL. The
merged tx_* stream is sampled pre-edge and compared byte-for-byte against
the model's own frame images.

Covered: strict priority when fresh over all four doc classes (ACMP >
AECP-solicited/self-CA > unsolicited/SRP > ADP; lowest index breaks ties;
sequence 2,0,5,1,4 over five simultaneous requesters incl. the oversize
slot); a lone lowest-priority requester is served; frame atomicity — an
ACMP request arriving mid-ADP-frame produces no grant until ser_last and
the in-flight frame is byte-exact and uninterrupted; aging promotion with
compressed tick_ms bursts — ADP starves behind back-to-back ACMP while
un-aged, and a 12-tick burst (threshold 10 = T-TX-AGING) flips the next
arbitration to the aged ADP over a fresh native ACMP; pacing outranks
aging — three aged non-solicited requesters against a continuously
re-armed ACMP yield the strict alternation 1,2,4,2,3,2, never two
non-solicited frames back-to-back while solicited traffic waits;
per-requester grant counters exact against the model; a PP_SLOT_NULL_C
handle is never granted and cannot hang the plane; a request withdrawn
after registered qualification is not granted from the stale bit;
selection remains abortable until the slot pool accepts its serializer start,
with no grant, frame, or slot damage on a pre-start withdrawal;
randomized contention
(1000+ frames, random lengths 1..64, random ready 40..100%, sparse random
ticks, oversize mixed in) with EVERY grant matched to the model's
decision, every frame byte-exact with sof/eof placement, grants one-hot
single-cycle, never mid-frame, no arbitration stall with work pending,
and the pool fully drained at the end.

Directed phases freeze the stream (tx_ready = 0) while arming mid-frame
contenders, so the schedules are exact regardless of prep length — the
pool's stall-never-skip skid (proven in `tb/tx_slots`) is what makes the
freeze legal.

Mutation-proven, restored, and rerun green at the current 66-check shape:

| # | Mutation | Result |
|---|---|---|
| M1 | aging never promotes: selection key `{~aged_w[i], class}` → `{1'b1, class}` | fails 12 of 60 (aged-ADP and pacing sequences collapse; 102 model mismatches) |
| M2 | pacing dropped: eligibility mask condition `pace_nonsol_r && sol_pend_w` → `1'b0` | fails 6 of 60 (alternation becomes 1,4,3,..; 17 random-phase grant mismatches) |
| M3 | priority inverted: best-key compare `<` → `>` | fails 21 of 60 (strict-priority sequences reversed; 311 model mismatches) |
| M4 | frame atomicity broken: `eof_w = consume_w && ser_last_i` → `consume_w` (arbiter re-arbitrates after the first byte) | fails 27 of 60 (4 mid-frame grants, 55 byte errors, stalls, pool corruption) |
| M5 | pre-start abort ignored and serializer request left asserted | fails 3 of 66 (canceled grant, frame start, and slot lifecycle) |

All five are behavior-changing mutants (no equivalent mutants recorded).
M2 is exactly the class of defect the aged-flood pacing phase plants: with
strict priority alone it is invisible, because solicited classes natively
outrank the unsolicited ones — only an AGED non-solicited flood can take
back-to-back frames, and only the pacing mask stops it.

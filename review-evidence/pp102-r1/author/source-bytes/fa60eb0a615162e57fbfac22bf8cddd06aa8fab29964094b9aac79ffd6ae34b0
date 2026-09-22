<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# scoreboard — KL_pp_scoreboard suite

Proves the cross-engine admission scoreboard
(`hdl/packet_engine/KL_pp_scoreboard.sv`, the F03.7 hazard matrix + ordering
rules (a)/(e) of [03 §6](../../docs/architecture/03_packet_engine.md)):
`make` = build + run, exit 0 = PASS, 3705 checks.

The C++ model is an independent transcription of the F03.7 matrix as a
LITERAL 9x9 table of {NEVER, SAMEKEY, ALWAYS} — a different formulation from
the RTL's precedence-rule chain, so either side diverging from the doc fails
the run. Grant ids are treated as opaque handles (no allocation-policy
assumption beyond uniqueness), so a different free-entry encoder survives the
suite. Combinational outputs (gnt, id, kill_ack) are sampled pre-edge;
registered state (holds mask, full, barrier_pend) is compared post-edge.

Matrix as encoded (both sides, from the doc): CFG_BARRIER = ALWAYS vs
everything itself included; RO x RO = NEVER, RO x any write = SAMEKEY;
LOCK_OP = ALWAYS vs the F06.14 lock-protected set (CFG, STREAM, MAP, CLOCK,
NAME, IDENTIFY) + itself, NEVER vs REGISTRY_OP; same class = ALWAYS for
REGISTRY_OP/IDENTIFY (single resource), SAMEKEY for STREAM/MAP/CLOCK/NAME;
STREAM_CFG x MAP_CFG = ALWAYS (the "referenced streams" cross-lock is
class-wide here — the single-{class,key} admission port cannot carry a key
set, so the RTL over-serializes rather than under-locks; see the RTL banner).

Covered: reset state; same-key serializes / release reopens; distinct keys
parallel with distinct ids; RO_SNAPSHOT admitting concurrently with itself on
the SAME key; the full 9x9 class-pair sweep in both key relations (162
ordered pairs, second admission checked against the literal matrix, table
drained and verified empty after each); rule (e) — the deadline-kill refused
while response-queued is low (key still serialized after the refusal),
honored once it is high, and refused for a no-longer-held id; grant/release
ordering — a same-cycle release + conflicting request does NOT admit (grants
evaluate against the pre-release hold set) and admits the next cycle; release
of a non-held id a no-op; holds-table full (8 parallel RO holds) refusing a
conflict-free request until one release; the CFG_BARRIER drain — refused
barrier latches barrier_pend, non-barrier admission then blocked while
holders drain, barrier granted exactly on the empty table clearing the latch,
everything excluded while the barrier is HELD, normal admission after its
release; and 2600 randomized ops (1417 requests / 811 releases / 372 kills at
seed 7) with every grant/refusal checked for exact equivalence against the
model (a lost grant and a duplicated grant both fail), plus periodic
holds/full/pend state compares and a drained end state.

Mutation-proven 2026-08-11 (each applied to a copy-backed original,
restored + rerun green after; totals differ per mutant because some checks
are conditional on grants):

| # | Mutation (sed on the RTL) | Fails |
|---|---|---|
| M1 | key compare dropped (`same_key_v = (a_key == b_key)` → `1'b1`): every SAMEKEY cell becomes ALWAYS | 245 of 3600 (distinct-keys-parallel: T2, T3 diff-key arms, T8) |
| M2 | rule (e) guard dropped (`kill_resp_queued_i` removed from `kill_ack_o`): kill honored before the response is queued | 128 of 3781 (T4 early-kill acked; T8 respq=0 kills + downstream grants) |
| M3 | barrier drain-block dropped (`(adm_is_barrier_w \|\| !barrier_pend_r)` → `1'b1`) | 122 of 3741 (T7 drain blocking; T8 admissions during pend) |
| M4 | STREAM x MAP cross-lock dropped (arm returns `1'b0`) | 60 of 3732 (T3 STR-MAP arms both key relations; T8) |

All four mutants change behavior (no equivalent mutants).

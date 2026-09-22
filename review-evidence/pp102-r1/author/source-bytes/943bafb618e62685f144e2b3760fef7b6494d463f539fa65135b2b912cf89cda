<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# event_router — KL_pp_event_router suite

Proves the sticky-event fan-in/fan-out
(`hdl/packet_engine/KL_pp_event_router.sv` — the
[03 §2](../../docs/architecture/03_packet_engine.md) F03.1 "Event router" row
with the class-C semantics of
[02 §5](../../docs/architecture/02_interfaces.md) / F02.6): `make` = build +
run, exit 0 = PASS, 81 checks, at the shipping shape (N_SRC_P = 16,
PAYLOAD_W_P = 16 — no `-G` overrides).

The C++ harness is an independent model, never DUT logic: it implements the
documented policy itself — per-source sticky latch holding the FIRST payload
until ack ("evt holds with its arg until evt_ack", F02.6), re-fire before ack
= coalesced flag + one saturating lost tick, ack + re-fire on the same cycle
= a NEW event with nothing lost, and a round-robin presentation whose base
advances past each delivered source. Every cycle the DUT outputs are compared
pre-edge against the model (lockstep), the lost-counter read port is
spot-read on a rotating index, and every delivery is matched.

Covered: single event delivered exactly once (2-cycle strobe→valid latency,
sticky over un-acked cycles, no re-delivery); re-strobe before ack — FIRST
payload held, `evt_lost_o` raised, counter exact and cumulative across acks;
coalescing on a queued-but-not-presented source; the ack+strobe same-cycle
race (old event delivered, new payload latched, NO lost tick); 16
simultaneous strobes → 16 deliveries in 16 cycles, round-robin order from
the pointer, each exactly once; directed pointer-wrap order (13 before 1
with the pointer at 12); ack-while-idle no-op; full saturation (all strobes
+ ack held) → one delivery per cycle rotating by exactly one; lost-counter
exactness at 100, saturation at 255, no wrap at 315; a randomized soak of
≥ 2200 deliveries with zero lockstep mismatches, no starved source, and the
per-source conservation law closed after drain:
strobes = delivered + lost — the "an event is NEVER silently dropped
without the counter ticking" contract as arithmetic (16 checks).

What the model cannot catch: it mirrors the documented arbitration policy,
so an implementation and model that both deviated identically from 02 §5
would pass — the directed phases (A–I) pin the DUT outputs against
constants for exactly this reason.

Mutation-proven 2026-08-11 (backup/sed/run/restore, all reverted):
- **M1** RR pointer frozen (`ptr_r <= ptr_r` on delivery) — fails 3 of 81
  (G3, J2 lockstep first-diverges on `src`, J3).
- **M2** lost-counter saturation removed (wraps at 256) — fails 19 of 81
  (H3 reads 59 after 315 re-fires, G3, J3, all 16 J7 final-counter reads).
- **M3** payload re-latched on every re-fire (FIRST-payload rule broken) —
  fails 3 of 81 (B1, B5, J2 lockstep first-diverges on `payload`).

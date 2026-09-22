<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# srp_stream_fsms — KL_srp_talker_fsm + KL_srp_listener_fsm suite

Proves the per-stream SRP FSMs (`hdl/srp/KL_srp_talker_fsm.sv`, M = 8
sources, and `hdl/srp/KL_srp_listener_fsm.sv`, N = 8 sinks) against
[10 §4/§5/§6.3/§6.4/§6.5](../../docs/architecture/10_srp_engine.md) with the
802.1Q-2018 §10.7 tables as the normative core: `make` = build + run,
exit 0 = PASS, 1005 checks.

The C++ model transcribes **Table 10-3 (applicant) and Table 10-4
(registrar) independently as data matrices** — never DUT logic — including
notes 4/5 (`operPointToPointMAC` via the `p2p_i` level), note 8 (tx! in AN
against the registrar), and the Milan **Δ13** deviation (rLv = immediate
IN→MT on the withdrawing frame; the LeaveAll cycle is the only LV path,
aged by a per-stream `T-MRP-LEAVE` slot). The wrap binds both modules the
way the engine integrates them: one decoder event bus and one cadence fan
to both; encoder-intake, VLAN-user and timer-arm faces stay separate for
observation (integration muxes them — ops are single-cycle and the timer
slot blocks are disjoint: talker 16..23/owner `0x40`+s, listener
24..31/owner `0x60`+k).

Covered:

- **Full Table 10-3 rx walk, both modules**: every rx event {rNew, rJoinIn,
  rIn, rJoinMt, rMt, rLv, rLA} × all 12 states × both p2p arms, driven
  through real ports (state-landing recipes use gate/settle ops, decoder
  events and join ticks; every recipe is cross-checked model-vs-DUT), on
  the talker's Talker-Advertise attribute AND the listener's Listener
  attribute — the two transcriptions of the table in the two modules are
  deliberately duplicated, and this walk is what keeps them identical.
- **Every tx!/txLA! row with its message**, both modules: transition plus
  the exact encoder push (sN=New, sJ=JoinMt, sL=Lv, s=Empty — the
  same-attribute registrar of a declared attribute never registers at an
  endpoint, so the reg_in=1 encodings and note 8's QA arm are
  unreachable-by-construction; optional `[s]`/`[sJ]`/`[sL]` are never
  sent, periodic! carries the re-join). Talker FirstValue checked
  byte-exact (stream_id/DA/VLAN/TSpec/prio/rank), Listener FirstValue +
  FourPacked lane likewise.
- **Δ13 + the LeaveAll-cycle exception**, both registrars: rLv on IN drops
  to MT on the frame (event strobes fire, NO leavetimer op); LeaveAll →
  LV with ARM(slot, owner, now+5000) observed on the timer face, the
  registration stays published through LV, a re-join CANCELs and returns
  to IN silently, an injected expiry ages LV→MT with the unregister
  event; foreign expiry slots are ignored.
- **F10.4 talker walk**: gate open → VLAN user++ + ADVERTISE; Ready and
  ReadyFailed (not AskingFailed) × `sr_admitted_i` ⇒ ACTIVE; admission
  loss → in-place swap to Talker Failed (tk_decl FAILED, fail code 1 +
  own-MAC system id published, New of the 34-byte Failed FirstValue on
  the next tick); admission return swaps back; gate close → Lv + VLAN
  user--.
- **F10.5 listener walk**: settle arms the exact {stream_id, DA, VLAN}
  matcher (near-misses on each field never match); Advertise registers →
  EVT_TK_REGISTERED + acc_latency latch + Ready declared; the in-place
  Advertise↔Failed swap BOTH directions (strobe, no unregistration,
  failure info latched/gated, declaration follows Ready↔AskingFailed);
  Δ13 unregister withdraws the declaration; teardown A8 fires NO events,
  drops VLAN, disarms the matcher.
- **Per-application isolation**: MVRP-application events with matching
  bytes (including the MVRP-VID/Talker-Advertise type-1 collision) never
  reach a registrar or applicant.
- **acc_latency latch**: initial latch, silent refresh re-latch, Failed
  also carries it.
- **VLAN user handshakes**: ops held under back-pressure, exactly-once
  consumption, close-before-join collapse to net zero.

Known model limits (recorded honestly): the harness drives the timer and
VLAN faces itself, so it proves the *contract* (op/slot/owner/deadline,
hold-until-ready), not KL_pp_timer_service/KL_srp_vlan integration; own
LeaveAll ages registrars at the `leaveall_own_i` strobe rather than at the
txLA! opportunity (≤ one T-MRP-JOIN early on a ≥ 4.5 s timer).

Mutation-proven 2026-08-11 (backup/sed/run/restore):

| Mutation | Result |
|---|---|
| Δ13 removed: listener rLv takes the IEEE LV+leavetimer path | 2 of 1005 FAIL (Δ13 unregister, no-leavetimer) |
| Talker applicant table cell QO→AO (rJoinMt!/rMt!) removed | 4 of 1005 FAIL (exactly the QO × {rJoinMt!, rMt!} × p2p walk cells) |
| Listener exact-match DA compare disabled | 2 of 1005 FAIL (near-miss + isolation) |

All three restored; suite back to 1005/1005 PASS.

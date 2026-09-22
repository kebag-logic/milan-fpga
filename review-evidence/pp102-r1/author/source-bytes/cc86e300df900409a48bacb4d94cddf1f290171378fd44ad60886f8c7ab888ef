<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# srp_top — KL_srp_admission + KL_srp_top end-to-end engine suite

Proves the assembled SRP engine (`hdl/srp/KL_srp_top.sv` wiring
KL_srp_decoder → {Domain, VLAN, talker/listener FSMs} → KL_srp_encoder,
with `hdl/srp/KL_srp_admission.sv` feeding the talker plane) against
[10 §1/§2/§3/§6/§7/§9](../../docs/architecture/10_srp_engine.md) and the
[02 §4.1](../../docs/architecture/02_interfaces.md) `srp` contract —
**through the REAL shared blocks**: frames are pulled byte-by-byte off a
real `KL_pp_tx_slots` serialize face (the C++ side plays the 03 §8 TX
arbiter), cadence and registrar-leave timers run on a real
`KL_pp_timer_service` (time-compressed: 1 ms = 40 clk, 32 slots), and the
T-MRP-LEAVEALL draws come from a real `KL_pp_prng` (kind 3, 10–15 s).
`make` = build + run, exit 0 = PASS, **230 checks**.

Expectations are independent: an MRPDU builder/parser written here from
802.1Q §10.8.1.2 / §35.2.2, a Σ-slope model transcribing the Milan v1.2
§4.3.3.2 recipe from the silicon-measured reference
(`milan-fpga/hdl/ieee8021q/srp/KL_lwsrp_bw_gate.sv`: F = MaxFrameSize+22,
min-68 clamp, W = F+20, slope = W·MaxIntervalFrames·8000·8) with the
greedy stream-index-order walk against the 75 % port-rate ceiling, and
the Table 10-3 fresh-declaration ladder (New, New, JoinMt) cited from the
standard — never DUT logic.

Covered end to end:

- **Bring-up**: link-up → Domain default declaration `{6, 3, 2}` New on
  the wire, byte-exact, at the first T-MRP-JOIN drain; class-D defaults.
- **Class-B service port** (02 §4.1 template): GET_DOMAIN {prio, VID}
  (class A only — class 5 FAILs), unknown op UNSUPPORTED, out-of-range
  indices FAIL; single-outstanding request/response contract throughout.
- **DECLARE_TALKER → admission → wire**: granted_slope_bps / sr_admitted /
  Σ / over_limit against the independent model; Talker Advertise New
  byte-exact (25 B FirstValue: stream_id, DA, VID, TSpec, prio/rank from
  the Domain + cfg, accumulated latency), the declaration ladder, and the
  MVRP VID New the membership join emits — all through the real slot pool.
- **Over-ceiling refusal (10 §6.3)**: a TSpec that pushes Σ past 75 % is
  refused → granted 0, over_limit, `tk_decl_state` FAILED, fail code 1 +
  own-MAC system id in class-D, and **Talker Failed code 1 byte-exact on
  the wire** (34 B FirstValue, §35.2.2.8.7 end-station MAC). Withdrawal of
  the blocking stream re-admits it: Advertise New replaces the Failed in
  place, over_limit clears.
- **Listener end-to-end**: DECLARE_LISTENER arms the exact matcher; a fed
  Talker Advertise MRPDU registers (TK_ATTR_REGISTERED, acc_latency
  latch) and the engine answers with a byte-exact Listener Ready New
  (FourPacked lane); the in-place Advertise↔Failed swap both ways
  (REGISTERED strobe, no unregister, failure info latched/gated,
  declaration follows Ready↔AskingFailed).
- **Certified two-class Domain arrival**: FirstValue `{5, 2, VID 5}`,
  NumberOfValues 2 — class A arrives as value 1 (802.1Q §35.2.2.9) —
  adopts (DOMAIN_CHANGE, class-D update, GET_DOMAIN agrees) and
  re-declares end-to-end: one Domain message, Lv `{6,3,2}` + New
  `{6,3,5}`, byte-exact.
- **LeaveAll per application (10 §6.5)**: the own MSRP leavealltimer
  (PRNG-drawn) emits a LeaveAllEvent PDU whose cycle re-declares Domain
  JoinIn + Listener Ready; registrations stay published through LV and a
  peer re-join keeps them (no unregister). A received MSRP LeaveAll ages
  the registrar over a real 5 s T-MRP-LEAVE to TK_ATTR_UNREGISTERED and
  the Listener Lv reaches the wire — while MVRP membership is untouched.
  The MVRP participant runs its own LeaveAll (flagged PDU, VID re-join,
  never an Lv flap).
- **Admission sweep**: 30 randomized declare/withdraw rounds across all 8
  sources vs the model — admitted vector, per-source granted slopes, Σ
  and over_limit, exercising the greedy order and capacity reuse.

Known limits (recorded honestly): the C++ side emulates the TX arbiter
and the processor-top header strip (both out of scope here — 03 §8 / 03
§5 own them); the PRNG face assumes this engine is the only draw client
(true in the wrap; the full processor routes draws); the byte-exact
checks align actions into clean 200 ms slots because T-MRP-PERIODIC
re-joins legitimately aggregate into the same MRPDU at boundary ticks —
aggregation itself is checked structurally by the parser, and the ladder
is covered by set-checks wherever bundling can occur.

Mutation-proven 2026-08-11 (backup/sed/run/restore):

| Mutation | Result |
|---|---|
| Admission ceiling widened to the full port rate (75 % term removed) | 33 of 230 FAIL (refusal phase C: admitted/over_limit/FAILED/wire Failed; the whole G sweep) |
| granted_slope_bps published ungated (raw slope instead of admitted-gated) | 31 of 230 FAIL (C "granted 0 while refused" + every G slope compare) |
| Admission verdict into the talker FSMs tied 1 (top wiring cut) | 5 of 230 FAIL (C: FAILED state, fail code/bridge, Talker Failed byte-exact; C2 swap-back) |

All three restored; suite back to 230/230 PASS.

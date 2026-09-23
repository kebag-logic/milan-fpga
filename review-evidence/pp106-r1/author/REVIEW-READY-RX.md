[A206] REVIEW READY (both halves): branch `106-leaveall-scope`, two commits on main `fbc1f715`. Nothing is pushed and no PR is open. The PR body (`Closes #106`), handoff and receipts are in the review packet.

- `9370f8ab` Signal LeaveAll for every registered MSRP attribute type (transmit, reviewed above: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5798150193)
- `fc155c3c` Route a received LeaveAll to its own attribute type, once per MRPDU (receive, per the scope decision: https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/106#issuecomment-5798176959)

**The rule, IEEE 802.1Q-2014**
- §10.7.5.20 NOTE: "The LeaveAll state machine operates on a per-application (not per-Attribute Type) basis, but the LeaveAll message operates on a per-Attribute Type basis. Hence, when the LeaveAll state machine issues a LeaveAll, it must generate a LeaveAll Attribute for each Attribute Type supported by the application concerned."
- §10.7.5.20 b) 2): rLA! occurs for a state machine only when "The PDU contains a Message in which the Attribute Type is the type associated with the state machine."

**Receive half**
- `KL_srp_decoder` no longer strobes a whole-application rLA! per VectorHeader. It strobes one lane per Attribute Type (`la_msrp_o[type − 1]`, `la_mvrp_o`), **once per MRPDU**, at the first VectorHeader of that type carrying LeaveAllEvent.
- `KL_srp_top` routes each lane to that type's state machines only:
  - Talker Advertise/Failed: the talker applicant of that variant, and the listener registrar holding that type.
  - Listener: the listener applicants and the talker registrars.
  - Domain: the Domain participant, which re-declares.
  - MVRP VID: VLAN, unchanged.
- An own LeaveAll still ages every registrar (§10.7.9). The MRP state machine tables, Δ13 and the leave timers are unchanged; only the strobe feeding each machine's rLA! changed.
- **Order.** The lane fires at the VectorHeader, which precedes its FirstValue and Vector (§10.8.1.2). §10.8: "A given MRP Participant shall process MRPDUs in the order in which they are received, and shall process the MRP Messages in a PDU in the order in which they were put into the Data Link Service Data Unit (DLSDU)." So a type's LeaveAll is applied before the events of its own VectorAttribute and all later ones. A conformant sender puts the LeaveAll first (§10.6, §10.8 NOTE 2), so for its MRPDUs the lane precedes all of that MRPDU's events of the type.
- Docs 10 §6.5 and the `KL_srp_top` and `KL_srp_decoder` banners state this with the clauses, replacing the per-application text.

**Three points for the reviewers**
1. **Timer clause.** The scope decision keeps the no-restart behaviour "as the standard's timer rules require". I kept the behaviour, but the clauses say the opposite:
   - Table 10-5 (§10.7.9) maps rLA! to "Start leavealltimer" and Passive in both states.
   - §10.6: "Reception of a LeaveAll message from another Participant causes the timer to be restarted without generating a message".
   - Milan v1.2 Table 4.3 only sets the range.

   I found no clause that permits no-restart, so §6.5 records it as an open deviation with these clauses rather than citing a justification.
2. **Applicants are routed per type too.** The decision names registrars; §10.7.5.20 b)2) scopes applicants the same way.
3. **One layout is handled in DLSDU order, not LeaveAll-first.** It is a type-T vector without LeaveAll ahead of the first flagged type-T vector in the same MRPDU. The streaming decoder has already emitted those events; making them follow the LeaveAll would need the whole MRPDU buffered. Our encoder never sends this layout, and none of the switch's 9 LeaveAll MRPDUs in Run B has it.

**Tests: each of (a), (b), (c) in the decoder, the talker FSM and end to end**
- (a) Run B shape `[Listener LA JoinMt][Domain LA][TalkerAdvertise LA n=0][TalkerFailed LA n=0]`:
  - The decoder takes the capture's 109 bytes; its strobe timeline is exactly `L3 E3 L4 E4 E4 L1 L2`.
  - In the talker FSM the Listener registration ends IN, and its ARM is cancelled by the re-declaration.
  - In `srp_top` it stays IN past T-MRP-LEAVE and the source stays ACTIVE.
- (b) Domain-only LeaveAll: only the Domain lane fires. No Listener registrar ages in the FSM or end to end, and our Domain re-declares.
- (c) Listener-only LeaveAll: IN → LV with T-MRP-LEAVE armed and Ready still published, then MT without any re-declaration; ACTIVE drops.
- A routing matrix covers every lane against every plane, plus a once-per-MRPDU test.
- Counts: srp_decoder 113 → 150, srp_stream_fsms 1005 → 1068, srp_top 236 → 252. srp_encoder is unchanged at 556 (the first commit's tests pass).
- Existing checks are all kept. Two `srp_top` stimuli (F2, F4) flagged LeaveAll on one type while expecting another type to age or re-declare, and 5 of their checks failed under the new routing. Both now flag every MSRP type, as a conformant peer does.
- 15 failing arms, each shown failing and restored under a SHA-256 check:
  - the previous decoder: 19 FAIL;
  - the previous receive side end to end: 5 FAIL (F5a, F5b, F5c);
  - decoder lanes, gate and re-arm: 21, 8, 18, 11;
  - talker FSM: 13, 16, 6, 2;
  - listener FSM: 6, 2, 3;
  - top routing: 5, 1.

**Gates at `fc155c3c`, CI simulator pin 5.050**
- Repository:
  - make check: OK.
  - lint: 37 OK.
  - run_suites: 30/30 suites, 15,436 checks, 0 failing.
  - gen_matrix --check: OK.
  - yosys: 32 OK plus Xilinx.
- Parent consumer: a disposable clone at `574c29fa` with the gitlink staged at `fc155c3c`:
  - check_cpp_idiom: 0 ≤ 0.
  - check_py_idiom: OK.
  - xvlog_gate --check: PASS, 4 = ratchet, pinned @fc155c3c, none in SRP.
  - pp_srcs --check --selftest: OK.
  - pp_shadow: 371 checks, 0 failures.
  - Also OK: check_sv_idiom, check_hygiene.
- The #530 end-to-end harness was not rerun at `fc155c3c`.

**Open, for the owner**
- The timer deviation above. `docs/10_RESOURCE_AND_EFFORT.md` still implies this spec restarts the timer.
- #530 item 2 is unchanged.
- Pin `fc155c3c` only after review.

[A206] REVIEW READY: branch `106-leaveall-scope`, one commit `9370f8ab` on main `fbc1f715`. Nothing is pushed, and no PR is open. The PR body, handoff and receipts are in the review packet.

**The change**
- An own LeaveAll MRPDU flags LeaveAllEvent on the first VectorAttribute of every attribute type the participant registers: MSRP Talker Advertise, Talker Failed, Listener and Domain, and MVRP VID.
- A registered type with nothing declared gets a LeaveAll-only message after the drained ones:
  - NumberOfValues 0;
  - a zero FirstValue of the full AttributeLength;
  - no packed events;
  - AttributeListLength = AttributeLength + 4.

  These are the bench switch's own bytes and order.
- When every type is already declared, only the flag bits change and no octet is added.
- MRPDUs without LeaveAll, and the MVRP LeaveAll MRPDU, are byte-identical to before.
- One edge case changes: a LeaveAll requested while a drain is writing now goes whole into the next MRPDU. Before, it was dropped.
- The MRP state machines and the receive side are unchanged.

**The standard**, IEEE 802.1Q-2014:
- §10.7.5.20 NOTE: "the LeaveAll message operates on a per-Attribute Type basis. Hence, when the LeaveAll state machine issues a LeaveAll, it must generate a LeaveAll Attribute for each Attribute Type supported by the application concerned".
- §10.8.1.2: `VectorAttribute ::= VectorHeader, FirstValue {, Vector}`.
- §10.8.2.8 f: "If the number of AttributeEvent values is zero, FirstValue is ignored ... However, FirstValue is still present, and of the correct length". §10.8.2.8 g: NullLeaveAllEvent requires a nonzero count.
- The docs' "§10.7.1" citation for LeaveAll scope was wrong. That clause is notational conventions. It is fixed in docs 10 §6.5 and both banners.

**Tests**
- srp_encoder: 180 → 556 checks. It covers all 15 declared-type combinations, each compared with the same drain sent without LeaveAll; the all-types case adds 0 octets. It also checks the NumberOfValues-0 bytes against the switch's wire bytes, and covers repeated types, MVRP unchanged, mid-drain requests and start-cycle requests.
- srp_top: 235 → 236 checks. The real own-LeaveAll MRPDU flags every type once.
- Ten failing arms were each shown to fail: the base encoder (146 FAIL), then 128, 115, 81, 50, 128, 3, 2, 2 and 2.

**Gates**, all under Verilator 5.050, the CI pin:
- make check: OK.
- lint: 37 OK.
- run_suites: 30/30 suites, 15,320 checks. Only srp_encoder and srp_top changed.
- gen_matrix --check: OK.
- yosys portability: OK.
- Parent consumer, in a disposable clone at `574c29fa` with the gitlink staged at `9370f8ab`:
  - check_cpp_idiom: 0 ≤ 0.
  - check_py_idiom: OK.
  - xvlog_gate --check: PASS, 4 findings = ratchet, none in SRP.
  - pp_srcs --check --selftest: OK.
  - pp_shadow: 371 checks, 0 failures.
  - Also run, both OK: check_sv_idiom and check_hygiene.

**End to end**, using the #530 harness at AX7101 1x1 TDM8:
- Type-scoped bridge:
  - The base encoder loses the registration 5 s after each DUT LeaveAll. The log is byte-identical to the #530 packet's.
  - With this change there is no loss in 60 s.
- Bridge sending LeaveAll in the bench switch's exact layout, 9.99 s after each DUT LeaveAll:
  - With this change, streaming is continuous for 300 s (22 cycles).
  - The base encoder reproduces the silicon burst ends.

**Open, for the owner: the receive side (correcting my DECISION)**
- The DECISION called this an interpretation question. It is a conformance defect: §10.8.2.6 reads "The LeaveAllEvent is interpreted on receipt as a MAD Leave All event to be applied to the state machines for all Attributes of the type defined by the AttributeType field".
- `KL_srp_decoder` instead raises an application-wide rLA! at every flagged VectorAttribute. That is why Run B burst 2 ended 5.000 s after the switch's own LeaveAll.
- With this change alone, the exposure closes only if our next LeaveAll lands within 5 s of the switch's. That fails for a LeaveAll interval within about 10 ms of 15 s: about 2 % of cycles by arithmetic, and 0 of 22 in simulation.
- With a fixed 12.5 s switch period, simulation shows the registration dropping 5.00 s after a switch LeaveAll.
- Recommendation: fix the receive routing before the #530 silicon rerun is judged. Also noted: our own leavealltimer does not restart on a received LeaveAll (802.1Q Table 10-5).

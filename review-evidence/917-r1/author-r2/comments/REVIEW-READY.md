[A784] REVIEW READY
Commit: 8f73ade5 (branch 917-aecp-hold, round 2: one commit on 3926c271; four on cec88385)
Answers R845-1 and R846-1 (both NEGATIVE at 3926c271), every finding; R846-1 F2 as the manager ruled for round 2.
Changed:
- tb/verilator/mbx: three checks on the RTL through both adapters and on the host model. B7: a ring with room for one record, which the held one takes; the frame behind it counts in RX_DROP, not RATE_DROP; every unread record and the held one intact (R845-1 F1). B8: a frame for another target, a cut frame and a 14-byte stub behind a held one count nowhere and set no ERR (F2). B9: a frame held when FILTER_EN closes its channel is still committed at the next refill (F3). Each has a planted defect caught by name (rx-space-from-the-committed-head, also through AXI4-Lite; rx-refused-behind-held-counted; rx-release-gated-on-open). The README row of rx-tail-inside-the-held-record-frees-space now says what it plants.
- Ingress allowance per path (R846-1 F2): FR_NFR.md 3.4.1 states it once. A record that finds a token keeps 64 clocks / 1 ms; a held record gets one refill period of its channel plus 1 ms. The generator derives each channel's held allowance from mailbox.yaml's refill_ms into MAILBOX_CONTRACT.md's channel table (AECP 6 ms); it is not copied anywhere else. Every margin is recomputed (token / held): ACMP 178/173, AECP 218/213, AECP at 250 ms 228/223, MVU 218/213; at the 10 ms proposal 188/183, 228/223, 238/233, 228/223. No bound moves.
- CPU budget harness (R846-1 F2): observes the hold and the held commit (hold_w, rel_w). A held record's commit is credited to its own frame (held.py), never to a frame ended since or to another channel. A missing, duplicate, misordered or late commit is refused. New group aecp-held sends a READ_DESCRIPTOR into an empty bucket and measures it from its last byte. New point 8x8-1if. The old attribution is planted in the self-test and caught by name.
- Wording: one in flight is #917's measured workload, not a rule of the protocol. A controller may pipeline (IEEE 1722.1-2021 9.2.2); timeout and retry are 9.3.2.6 and 9.3.6; the bench's deadline is next-refill delivery (R846-1 F1). MAILBOX_SPLIT "What is dropped" corrected (R845-1 R2); "Its limit" added (S1). No issue-comment ID in source comments (R1 in both reports).
- KL_mbx_rx.sv: comments only; sv2v output byte-identical to 3926c271. No firmware source changed.
Validation (clean clones of 8f73ade5):
- Native shard 1/4 (holds mbx): 17/17 pass (16 in the shard run, mbx 622/667/32/629/674/547 checks and 13/13 quick mutants; milan_dp_render, cut by the shard's wall clock under CPU contention, rerun on a fresh clean clone: PASS).
- make -C tb/verilator/mbx mutants: 242/242 caught by their named checks, after four positive controls.
- Workflows step by step (rtl-fast, elaborate, docs, rtl yosys): 139 steps rc 0, 226 not run with a stated reason (hosted orchestration, installs this host already has), 0 bad; firmware control mutants 699/699.
- Local: lint (89 <= 89), gen_mailbox --check/--crosscheck/--selftest, docs_check, doc paths, em-dash, py/cpp/sv/sh idiom gates at their ratchets: all pass.
- Budget harness self-test: 0 failures, 214 planted defects caught, the old attribution among them.
- aecp-held at 1x1: 5.236 ms from the held frame's last byte, ingress 4.986 ms of its 6 ms allowance, within the 20 ms bound; 0 refusals, 0 misses. At 8x8/1if: 5.114 ms, ingress 4.986 ms, within 20 ms; 0 refusals, 0 misses. On both logs the held record is credited to the probe and both followers are refused; the old rule refuses the log.
- The 94-group 1x1 population's recorded logs (cec88385 and 84d8a214), regraded by the round-2 grader: table.md and 94/94 grades byte-identical to each recorded run.
- Firmware images against cec88385: 46 fixture images byte-identical; split 1x1/1if (bb04b696, 145,496 B) and 8x8/1if (506a1ae4, 158,176 B), ROM banks and constraints byte-identical.
- Round 1's route stands (the RTL logic is unchanged): AltSpreadLogic_high WNS +0.203 ns, WHS +0.036 ns.
Acceptance criteria:
- Mailbox bench: met. B0 (50 commands, one in flight, none lost), B1 (third behind a held one dropped and counted), B2 (1 kHz controller, none of 100 lost); now also B7 to B9.
- No firmware image change: met (hashes above). Load and rows unchanged: met (every commit spends one token; the population regrades byte-identically; the held rows fit).
- Three descriptor walks on hardware: not run (no hardware in this lane).
Open risks/questions:
- At 8x8/1if the harness's stated-cost check reports three link-up MRPDU build passes over ctrl_loop.h's one-interface stated costs: 120,704 and 117,875 cycles against 101,000, and 95,723 against 43,000. The existing aecp group, which holds nothing, reports the same three, so they belong to the point, not to this change. Every row fits. Nothing changed; for #914's 8x8/1if measurement.
- 8x8-1if is a new harness point; the 94-group population was not run there.
- Hardware walks still owed; "Closes #917" would close the Issue at merge before them.
- Pre-existing: the budget harness cites MAILBOX_SPLIT.md by line number, already stale at the base.

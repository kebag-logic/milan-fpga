# HANDOFF r10c: [A825] #977 (part of #665), round 10c

Status: **STOP** (11:42 CET 2026-11-27) under the ruling's item 5 (#977 comment 7212897415): at 8x8/1if the polls base and the tier-2 slice checks fail, with the numbers below. The ceiling (0.77), the pins (80 of 80 ELFs identical across each move), the delivery bound, S14/S14b, the three groups and the fourth window are committed at e62e1936. Nothing is pushed or posted.
ETA: none until the decision; after it, about 9 h (the final relearn, every arm at both points, routes, gates, ledger, packet).

Inputs read in full: the OWNER DECISION, #977 comment 7213594113 (8x8/1if ceiling 0.77; every other bound unchanged; margin recovery is #1025, not this PR); the RULING, #977 comment 7212897415; the manager's round 10c instruction.

Order: (a) the ceiling to 0.77 with its control; (b) the pins lwSRP e27b34c9 and tsn-c-stack 5a07d9b7, each product ELF byte-identical across each move; (1) the delivery bound (ruling item 2) with tests, plants and the wire consequence; (2) S14 at 8x8/1if (ruling item 6, the 2026-11-27 ruling item 3, #1023), the three groups, the granted fourth window (kept, its 0.6 % recorded), the JoinIn-of-both-kinds record against 2 ms; (3) the full re-measure at both points; STOP per ruling item 5 with numbers.

## STOP (ruling 7212897415, item 5): base and slice checks fail at 8x8/1if

Measured at `e62e1936`, the delivery bound in, on the 8x8/1if images of the none and answering-ports arms, every registering group (`receipts/stop10c/registering-8x8-1if-e62e1936.txt`). No pass exceeds 2 ms: the longest is 1.454 ms (swap). 0 work passes are over THE SHARE in every group.

| Group | Polls base (stated 300 us = 30,000 cycles) | Tier-2 slice of SRP's records (stated 1,475 us = 147,500) | Other |
|---|---:|---:|---|
| `srp-register-swap` | **33,137** / **31,554** | **149,057** / **151,656** | a walk item 14,270 / 12,082 over its stated 12,000 |
| `srp-register-both` (every input's JoinIn of both kinds) | within | **171,911** / **174,819** (1.72-1.75 ms, under 2 ms) | |
| `srp-register-lv` | **30,760** / **30,008** | within | |
| `srp-register-leavetime` | **30,760** / **30,008** | within | |
| `srp-register`, `-burst`, `-population`, `-leaveall`, `-messages` | within | within | rc 0 |

(answering-ports / none.)

- **What the delivery bound did.** Before it, at 25ed2bb0's images, the leave-timer group's run-out pass had a base of 31,215 / 31,081 cycles. Its SRP delivery was 11,837 cycles: one binding change (6,322 to 6,480 alone) and one loss completion in one pass. One of the two a delivery (`e62e1936`) brings it to 30,760 / 30,008, still over 30,000 by up to 2.5 %. The swap's over-base pass spends 14,403 cycles in SRP's delivery with one binding change.
- **The slices are records THE DRAIN takes alone.** The swap record charges 18 values (2,625 us) and the JoinIn of both kinds 18 (2,625 us), both over the 1,475 us slice by design: THE DRAIN takes such a record alone (the 2026-11-27 ruling's item 2 already states 1,500 us due at 8x8/1if). The grader holds every tier-2 slice to the stated slice, so a record alone over it fails the slice check. Splitting a record is refused (the 2026-11-27 ruling, item 1). A cheaper record is #1025's, not this PR's.
- **The load passes at 0.77.** The registration cost restated by the rule over every registering group at `e62e1936` is 195 us at 8x8/1if (the JoinIn of both kinds: apply 162,757 and settle 37,848 cycles over its V of 9, 18,123 a Talker). With it the 8x8/1if load is 0.763, and `flip_grade --check --point 8x8/1if` passes against 0.77. At the stated 135 us it is 0.757. (`receipts/stop10c/load-flip-e62e1936.txt`, `regcost-8x8-1if-e62e1936.txt`.)

**1x1/1if** at `e62e1936` passes. Every registering group passes in both arms, 18 of 18 runs with rc 0 and no stated cost exceeded, the swap included (its polls base is within 225 us with the delivery bound). The longest pass is 0.993 ms. The restated registration cost is 185 us (the JoinIn of both kinds, 17,532 cycles a Talker over its two sinks), so the load is 0.523 of 0.70. (`receipts/stop10c/registering-1x1-e62e1936.txt`, `regcost-1x1-e62e1936.txt`.)

**Decision needed** (facts, not a choice):

- **The slice check for a record taken alone:** either hold such a record to its charge rather than the slice, or move the 8x8/1if slice statement. The ruling keeps the slices as stated.
- **The 8x8/1if polls base:** it is over by up to 2.5 % in the loss passes and 10 % in the swap's binding-change pass. Options: restate the base, which the ruling refuses; spread the delivery further (for example, a binding change only on a pass that took no record and no other heavy item); or #1025's cuts.

**Done this round** (committed, `e62e1936`):

- the ceiling 0.77 with its control;
- the idiom-gate fixes;
- both pins, 80 of 80 ELFs byte-identical across each move;
- the delivery bound, as one of a binding change and a loss completion a delivery, with D1-D5 and seven plants, all caught;
- S14 and S14b, with three plants, all caught;
- the three groups;
- the fourth hot-list window, relearned at `ec9dc4be`. At `e62e1936` the list is that relearn's: the delivery change came after it, and a relearn at a STOP head was not run.

Gate shard 0 passes at `ec9dc4be`. The composition suite passes at `e62e1936` (1x1/1if, 1x1/2if, 8x8/1if), and platsinks at `760d341c`.

**Not done** (the STOP):

- every arm at both points;
- the routes;
- the full gate at the head;
- the final relearn;
- the memory ledger statement.

## Log
(Times from `date` and the commit times.)
- 09:31 owner decision read. Found at the committed head a35b092f: the Python idiom gate failed (run.py 1,003 and grade.py 1,001 lines over the 1,000 ratchet, 11 lines over 120 columns, 2 undocumented nested helpers), all from #977's own lines; fixed in fd126873 (no behaviour change: the gate passes, flip and load self-tests pass).
- 09:35 2d57e46e: FLIP 8x8/1if 0.77 (flip_grade, load_grade comment, FR_NFR 3.4.1, SPLIT_CONTROL_MEMORY), a new control "8x8/1if: 0.761 refused or 0.771 passed" (flip self-test 617 of 617; it catches the ceiling planted at 0.76 and at 0.78); load_grade/flip_grade --check PASS.
- 09:36 f5552daf + cdb35fc7: lwSRP gitlink 73007b48 -> e27b34c9 (squash merge of lwSRP PR #22; src delta is comments and the LWSRP_LEAN_COPY=0 restore macro), ctrl_arms.LWSRP_REV, SUBMODULES.md, the READMEs, MAILBOX_SPLIT.md, the diagram regenerated; doc style, submodule docs and diagram checks pass.
- 09:37 9380ff82: tsn-c-stack gitlink 0f72ca69 -> 5a07d9b7 (PR #41's merge; tree 6095ea25 equal to 0f72ca69's), every full-SHA link, SUBMODULES.md, the diagram.
- 09:38 identity builds id10-A (2d57e46e), id10-B (cdb35fc7), id10-C (9380ff82): plat_ledger's platform images and the 24 harness images each.
- 09:45 rm (logged before it runs): <scratch>/r10/fwb (the gate's build dir of the exploratory arms run, rebuilt)
- 09:58 pin identity: 80 of 80 ELFs byte-identical across lwSRP 73007b48 -> e27b34c9 and across tsn-c-stack 0f72ca69 -> 5a07d9b7 (receipts/pins/elf-identity.txt).
- 10:06 f6b44e99: the delivery bound (ctrl_app_srp.c deliver: one binding change and, outside THE SETTLE, one loss completion a delivery, each the first owed from its turn; the rest pending, keeping the loop awake; THE SETTLE unchanged), tests D1-D5 (srp_binding.hpp), ParkedReplacementRetiresThePreviouslyAcceptedBinding's expectation changed (one parked retirement a delivery, the other owed), srp/README.md; six plants (srp_deliver_mutants.py) each caught at 1x1/1if (deliver-owed-loss-sleeps first escaped D3, since each loss also owes an unbind; D5 holds a loss with no change owed). Composition suite passes at 1x1/1if, 1x1/2if, 8x8/1if.
- 10:06 760d341c: S14 at each shape (the keep min(SRP_KEPT_TALKERS, V - bound): within it the original checks, past it nothing declared before the Talker's next declaration, then in THE TRANSMIT's next MRPDU), S14b (one input unbound, the original checks); plants early-keep-bound-uncounted (S14, 8x8) and early-keep-room-short (S14b, 8x8), early-talker-ignored's 8x8 S14 needle moved to S14b; all caught by hand-planting (plantsink10.py; the control campaign refuses a partial table). platsinks passes at both shapes.
- 10:06 c80f1e91: groups srp-register-lv, srp-register-leavetime (900 ms past the Lv: LeaveTime 60 cs), srp-register-both.
- 10:10 note: commit 25ed2bb0 (S14b's needle) also carries ctrl_split_hot.txt's procedure header for the granted fourth window (#977's ruling on round 9's STOP, item 3), taken in by commit -a; no list entry changed there; not amended.
- 10:11 maps10-8x8 first launched on 32-47, which another job held (my error, cpu_ranges listed it busy); stopped within a minute and relaunched on 48-63. rm (logged before it runs): <scratch>/r10/maps/8x8 (its partial first build).
- 10:33 rm (logged before it runs): <scratch>/r10/b/8x8-1if (step 0's window builds at a35b092f, superseded; the final build was started over it and stopped at once)
- 10:33 ec9dc4be: hot list relearned with the fourth window (four windows on the 1x1/1if default arm at 25ed2bb0: 204,832 / 273,408 / 900,000 / 900,000 PCs; 295 learned, the same five dropped, 290 listed; ctrl_split_delivered.isra.0 new; 72 of 72 maps clean). Final builds b10 started at ec9dc4be; gate shards 0 (PASS at 10:48) and 1 started.
- 10:42 early registering groups (pool early10, at 25ed2bb0's images): at 8x8/1if srp-register-leavetime's run-out pass has a polls base of 31,215 cycles (answering-ports) and 31,081 (none), over the stated 300 us (30,000). Its SRP delivery is 11,837 cycles: one binding change (6,322 to 6,480 alone) and one loss completion in the same pass. (8x8/2if's registering findings are outside #977's scope: its rows are reported, not held, and its registrations are not measured.)
- 10:55 e62e1936: a delivery makes one of a binding change and a loss completion, the kind the last did not where both are owed. The ruling allows each at most one a delivery and each owed within 2 x CTRL_SRP_SINKS deliveries; this takes one of the two and keeps that bound. D3 now holds one of the two a delivery and every loss within 2 x n_sinks; plant deliver-binds-beside-a-loss caught; all seven delivery plants caught; the composition suite passes at 1x1/1if, 1x1/2if, 8x8/1if. The b10 builds and shard 1 at ec9dc4be no longer stand (stopped).
- 10:58 check: the registering groups at 8x8/1if on e62e1936's images (chk10), and the relearn images for e62e1936 (maps11).
- 11:10 early10 stopped (its images were 25ed2bb0's, superseded); relearn windows hot11-w1..4 on e62e1936's 1x1/1if default arm image.
- 11:21 STOP conditions met at 8x8/1if on e62e1936 (chk10): polls base and tier-2 slices over their statements (numbers in the STOP section). Relearn windows hot11 stopped (not needed for a STOP). 1x1/1if registering groups run on e62e1936's images (chk10-1x1) for the report.
- 11:40 1x1/1if registering groups at e62e1936: 18 of 18 pass; the restated cost 185 us, the load 0.523. STOP written.

STOP: ruling item 5 at e62e1936, 8x8/1if: the polls base over its 300 us (srp-register-swap 33,137 cycles, srp-register-lv/-leavetime 30,760) and the tier-2 slice over its 1,475 us for records THE DRAIN takes alone (srp-register-both 174,819 cycles, srp-register-swap 151,656); no pass over 2 ms (longest 1.454 ms); the load 0.763 passes against 0.77 at the cost restated by the rule (195 us); 1x1/1if passes

# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 10, [A781]

Status: STOP to the maintainer at `db6bc954` (comment text `STOP-COMMENT.md`, posted once on #894 as issuecomment-6934654949): the fix reaches
every cost target at both points and every row the CPU decides holds, but one held-egress row at 8x8/1if,
backlog-owed.service.aecp.last.if0, measures 62.04905 ms against its ledger figure 61.94 (by phase, not cost), and a
ledger figure moves only by ruling. PR text `PR-BODY.md`. Nothing pushed; no PR created or edited. Host stops during
the round: 15:40 (power cycle), 18:46 (crash), 19:39 (maintenance).

- Start head: cd7d92ad (round 9's STOP, #894 issuecomment-6917926838), tree clean, 15:13 CET. Only the session's own
  unit running.
- Assignment: the manager's ruling on round 9's STOP, #894 issuecomment-6918853411, and issue #930 (both read in full;
  saved at the scratch's r10/ruling-r10.md and r10/issue-930.md). Items: (1) commit the restatements as the patch
  states them; (2) the fix in the split SRP adapter (srp_mbx and the registrar walk; lwSRP and tsn-c-stack unchanged):
  a licence published and the declarations updated only when the licence changes, and a walk of only the Listeners
  whose registration changed; callback order and arguments identical, by a differential unit test over random record
  sequences at both shapes, a planted defect per mark site caught by name, coverage 100 %; (3) the targets: 1x1/1if
  SRP record <= 280 us by the rule and the last queued notice <= 140 ms by every source; 8x8/1if load <= 0.75 at the
  pin; every row within its bound at both points including srp-talker-held; (4) the tsn-c-stack#32 column; (5) STOP
  with the measured best if the fix cannot reach the targets. Then the final gates on a clean clone, REVIEW READY on
  #894, this file and PR-BODY.md. At most 4 heavy units at once. Push nothing.
- Host restart: power-cycled at 15:40 CET (memory upgrade, 82 GiB). At the cut the tree held the fix and the restated
  walk test uncommitted (kept); no round-10 unit had been started, so none was cut.

## Items

1. The restatements. — DONE `d9335d1f`, as round 9's patch states them (SRP unit 290 and 450, record.srp 290 and
   OWN 450, the polls at 8x8/1if, 1x1/1if's apply 285).
2. The fix. — `51e50436` and `705f6fa4`:
   - srp_mbx.c: a Listener's indication copies its declaration (listener, as before) and no longer marks the walk;
     the transition observer copies its presence (listener_moved); a Registrar change no longer marks the walk at
     all, since each change of what the walk copies comes with an indication (IEEE 802.1Q-2018 Table 10-4; lwSRP
     indicates a value changed while it registers): a walk now follows a Talker's indication, a binding, one of the
     adapter's own declarations or a participant's creation. lwSRP and tsn-c-stack unchanged. `moved` kept a function
     of its own (CTRL_CC_NOINLINE), as the split link script's hot list places it.
   - The licence: already published only when it changes (poll: `active != i->active[s]`); the record itself
     publishes nothing and declares nothing.
   - srp_listeners.cpp, the differential: srp_mbx.c built with lwSRP's msrp_app_create and mrp_set_observer renamed
     to the suite's seams, which restore #665's walk schedule (every Listener indication and every Registrar change
     owing the walk) in the reference run; random record sequences (Listener, Talker, Domain and MVRP records with
     LeaveAll, bindings, time, link changes, allocation refusals, records with no poll after them) through both from
     one seed; every mailbox write but the transmit ring's words (the frames are compared from the model instead,
     the ring's records carrying the driver's commit count since its start), every licence call and the state the
     loop, ACMP and THE TRANSMIT read, after every step; each settled step of the copied run against a walk of the
     registrar. Two seeds x 3,000 steps, at 1x1/1if and 8x8/1if (srp_arms.listener_arms), and in the coverage run.
   - srp_listener_mutants.py: five defects, one at each copy and mark site (the Talker indication's mark, the
     Listener's declaration copy, its presence copy, presence's MT test, the observer's dispatch), each caught by
     name at 1x1/1if, 8x8/1if (a new one-interface campaign at the 8x8 entity) and 8x8/2if.
   - Existing tests under #930's contract: srp_mbx.cpp ARecordThatChangesNoRegistrationCostsNoWalk now holds that a
     Listener record walks nothing and a Talker record walks once; the composition test
     AcmpMailbox.F3bListenerRegistrationControlsItsOwnGate binds a sink while Asking Failed registers, so a walk
     copies the Listener again (four-way-f3b-asking-failed-excluded, planted in the walk, escaped without it);
     four-way-f3b-withdrawal-stale's plant moves from the walk's reset of listener_present, which no longer decides a
     withdrawal, to the copy that does (listener_moved), the same test and words.
3. The targets. — The restatement on the fixed image (`1d4244a6`, `db6bc954`): the SRP units 280 (1x1/1if) and 365
   (8x8/1if), record.srp 280 at 1x1/1if in both columns, 8x8/1if's own record.srp dropped for NEAREST's 365, the
   retained retry 280 and 345, 8x8/1if's reclaim 35 to 40. The measurement on 46cf2a7d's image (29 legs, every rc 0, no
   STATED line; receipts/harness/legs-46cf2a7d/):
   - 1x1/1if: SRP's record 23,503 cycles, 250 us by the rule (<= 280); the last queued notice by every source 136.65 ms
     (<= 140; flip check); every measured row within (gate_r10.py PASS, 118 groups, 1,290 instances); the survey: 0
     statements exceeded.
   - 8x8/1if: the load 0.735 at the pin (<= 0.75; 0.694 in the second column); every row the CPU decides within (117
     groups, 1,762 instances); the survey: the reclaim alone over (restated); the record classes PASS at both points.
   - NOT MET: backlog-owed.service.aecp.last.if0 at 8x8/1if, 62.04905 ms against its ledger figure 61.94 (62.16 by the
     rule at this measurement); the other six held rows 0.22-0.37 ms under. Cause (receipts/harness/aecp-last-phase.txt):
     the composed window opens 290 us earlier on the fixed image, so the release falls 237.5 us past a millisecond
     (527.5 before), no AECP frame is queued at it, and the first pass after it commits ACMP's owed frame first.
4. The tsn-c-stack#32 column. — The pin 715589c1 is the merge of tsn-c-stack PR #34 (closing #32); its src/ and
   include/ are byte-identical to 9043b926, the donor commit STATED_US_DONOR was measured with, and #32's head a530eca
   is in it. So "at the pin" includes #32, and both columns state one image's costs: the pin's also holds what images
   built before the pin moved measured for the five costs #32's walk moves (WALK), since a statement never goes down;
   the donor's holds only measurements of images carrying #32. Explained in load_grade.py's docstring; the ceiling is
   read at the pin's column, as flip_grade.py does.
5. STOP. — Posted once on #894 with the measured best; the final gates not run, by the STOP (their scripts:
   mkqueueR10.sh, lane_gates_r10.sh, vshard.sh). Quick checks on a clean clone of db6bc954: 20 of 20.

## Run history (CET)

- 15:13 resume; head cd7d92ad, clean. 15:2x item 1, commit d9335d1f. 15:3x the cost's analysis (the dearest 8x8/1if
  record, R9-H8: srp_mbx:receive 42,663 cycles, its registrar walk 9,714 of them, after mrp_rx).
- 15:40 the host's power cycle; 16:38 resume.
- 16:4x-17:1x the fix, the differential, the defects; dev arms (srp_mbx 74, srp_walk 5, srp_talker 12, srp_rx_retry
  21, srp_app 8, srp_latency 5, test_acmp_mbx 76 at one and two interfaces, srp_listeners at 1x1/1if, 8x8/1if and
  1x1/2if); 34 defects near the change planted at one and two interfaces, all caught; commit 51e50436.
- 17:14 the probe (srp-talker-held alone at both points, clean clone of 51e50436): refused at the image's link, the
  hot list's `srp_mbx moved` no section once moved was inlined; moved kept a function of its own, all 8 images link
  (qimg on the tree), commit 705f6fa4; 17:18 the probe again on a clean clone of 705f6fa4; 17:19 fw_coverage --check
  on that clone: PASS, 39 files, srp_mbx.c 746 of 746 lines; 17:30-17:48 test_ctrl_firmware's suites there: PASS,
  82 arms.
- 18:09 the 1x1/1if probe ended rc 0: SRP's record 23,503 cycles (27,170 before), its apply 23,144 (26,925), 250
  and 245 us by the rule; every other cost within its statement (costs_r5.sh). The 8x8/1if probe's Listener Readies
  measured at most 32,936 (42,663 before), 350 us.
- 18:46 the host's hard reset; 19:06 reboot; 19:08 resume. The 8x8/1if probe was cut in its held save (no rc): its
  output removed, not re-run alone, since the measurement's valid-destinations leg at 8x8/1if runs the same group on
  the measured image. At the cut its records outside the Listener Readies were at most 20,860 cycles (not evidence).
- 19:0x the restatement on the tree (the SRP units 280 and 365, 1x1/1if's record.srp 280 in both columns, 8x8/1if's
  own record.srp dropped for NEAREST's 365, the retained retry 280 and 345): load 0.730 at the pin at 8x8/1if, 1x1/1if's
  last queued notice 136.65 ms, every grader's self-test PASS; commits 11a9b4bf (the #32 column), 1d4244a6 (the
  restatement), 46cf2a7d (the design note). qimg on a clean clone of 46cf2a7d: all 8 images link.
- 19:11 the measurement on that clone (mkqueueM10.sh, 15 legs, at most 4 at once, on the session's CPUs, every range
  booked); the first launcher stopped by its unit before any leg started, to put the 8x8/1if valid-destinations leg
  first.
- 19:12-19:13 the first four legs started (M8-VD, M8-A0..A2); 19:39 the host's maintenance shutdown cut them all (no
  rc): their output removed. 19:44 resume; 19:4x the measurement again in shorter legs, so a stop cuts less
  (mkqueueM10b.sh: 29 legs, arm A in eight parts, the answering-every-port arm in two, each valid-destinations group
  its own, srp-talker-held first at both points), at most 4 at once, on free 8-wide ranges or the session's CPUs.
- 21:27 both srp-talker-held legs rc 0, no STATED line, no budget miss; the survey: every statement holds but
  8x8/1if's reclaim, 3,446 cycles, 40 us by the rule against 35 (a grader's statement, not the image's).
- 23:3x arm A at 8x8/1if complete (eight parts, rc 0, no STATED line); gate_r10.py over it and srp-talker-held: every
  row the CPU decides within its ruling, six held-egress rows within the ledger, and
  backlog-owed.service.aecp.last.if0 62.04905 ms over its ledger figure 61.94 by 0.10905 ms (the composed image's
  61.75319). The cause, read from both traces: the hold releases 6,005,361 cycles after the composed window opens on
  both images, and on this one the window opens 29,006 cycles (290 us) earlier (the settle before it shorter, its SRP
  records cheaper), so the release falls 237.5 us past a millisecond instead of 527.5 us; the first pass after it
  (+51.9 us, 42,336 cycles) commits ACMP's owed frame ahead of AECP's, which round 8's first pass (+170 us) committed
  first. AECP's last service moves 0.296 ms later, ACMP's and the five owed frames' 0.09 to 0.16 ms earlier. A ledger
  figure moves only by ruling, so this is a row over its bound: a STOP, after the rest of the measurement.
- 01:29 the last 8x8/1if leg ended; 01:54 the last 1x1/1if leg (29 of 29 rc 0, none with a STATED line). 01:4x-02:1x
  the gates and surveys over both points (gate_r10.py, survey_r5.py, survey_point.py: 1x1/1if's first survey ran twice
  over itself, a detached attempt not dead when its unit began, so it was discarded and run alone); the record classes;
  8x8/1if's rows by every source; the reclaim restated, commit db6bc954 (a grader only; the images are 46cf2a7d's);
  quick checks on a clean clone of db6bc954, 20 of 20; at db6bc954 the 34 nearby defects at one and two interfaces and
  the five new ones at 8x8/1if, 73 plantings, all caught; the phase receipt from both traces.
- 02:1x receipts, INDEX.md, STOP-COMMENT.md, PR-BODY.md; the STOP posted once on #894 (issuecomment-6934654949),
  its text the file's. Nothing pushed; no PR created or edited.

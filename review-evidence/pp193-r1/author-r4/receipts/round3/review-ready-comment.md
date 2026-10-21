[A661] REVIEW READY
Head: processor `193-shared-listener-leave` = 324ac9a7aafe7090428a15c53d5b61eac69f1257. That is six new commits on the PR #198 head 7b424cdf; not pushed, no rebase, no amend.

Round 3 (the [A10] assignment on PR #198, answering R679-2 and R680-2). The RTL change is in `KL_srp_listener_fsm` only, with no new register; no port, parameter or register-map change.
- F1: each applicant now has one transmit opportunity per walk, of the walk's kind (tx! or txLA!), whichever slot holds it.
  - The walk marks every slot it passes, and a handover still carries the applicant's mark.
  - A walk ends only when every slot holds the mark. A slot handed an applicant after the walk passed it, from a slot the walk had not reached, makes the walk go round again from slot 0 and serve it in that walk. In R679-2's case that is the LeaveAll walk's JoinMt.
  - Why this form: an owed txLA! carried to the passed slot needs a flip-flop per sink and is still a tick late. Serving at the giver's slot fails when the giver leaves the group in that clock (an A15 handover, a parked takeover).
  - Banner, 10 §6.4 and the PR text no longer claim a delay.
- Found in this round, the same class: the walk sent the last declarer's Lv, then a rider ahead of the walk declared, and that walk sent New beside the Lv for the StreamID. The walk now marks every member of a group whose applicant it serves (round 2 did so for a retired park only), so the New waits for the next tx!.
- New checks, each KILLED by a named control:
  - SH18: txLA! handover into a passed slot, holders 5 and 7, clocks 1-3. One JoinMt in the LeaveAll walk. Control `listener-walk-ends-owing-a-transmit`, which also kills SH16, SH19 and SH20.
  - SH19: the tx! form. SH20: the A15 handover form (LA to LO, then Empty, not Lv).
  - SH21: a rider declaring after the last Lv. Control `listener-walk-marks-group-only-on-retire`.
  - SH22: a rider settling after its stream's transmit lets the walk end. Control `listener-walk-marks-only-served-slots`.
  - SH16 now expects the New in the walk that serves the takeover.
- F2: SH17 is R679-2's re-park case, with the edit it names as its control `listener-repark-takes-matcher-pairs`: KILLED.
- R1: applied as written. Commit 6 then adds this round's checks to that row and to six other count rows.
- S3: the PR body gives the listener FSM alone at one sink beside "no 1x1 figure": main 2,898 LUT / 454 FF, head 2,786 / 455.
- S1: applied. SH23, two parks through an own LeaveAll, with control `listener-two-parks-grouped`.
- S2: measured, not kept. At 2 Stream Inputs `KL_pp_shadow` was +99 LUT / -128 FF, so commit 5 takes it out.
- R680-2-S1: applied.
- One existing control changes its named check: `listener-rider-not-quiet` now must fail SH14. SH1's rider sits above the owner, and the new group mark keeps that rider's Empty from going out. The control fails 12 checks.
- R679-2's probes on the head:
  - `s2_probe.py`: MATCH in all 20 rows (both holders, tx! and txLA!, clocks 1-3, both controls). On 7b424cdf the six txLA! handover rows read DIFF, as reported.
  - `repark_probe.py`: MATCH. With its planted edit the suite now fails SH17.
  - Its control campaign now kills its re-park and both-parked arms in the stream-FSM suite.

Records, base 7b424cdf (round 2's head records, same executable inputs) vs head, all rc 0:
- run_suites: 1,030,367 -> 1,030,375 (only srp_stream_fsms +8).
- lint, make check, matrix, portability elaboration and guards: identical but for `make check`'s five new patch files.
- srp_top campaign: 203/203 -> 208/208, coverage 124/124 -> 131/131. 174 arm runs keep their verdict and tags. Nine gain tags of the new checks, and one fails one more line of the same checks. `listener-rider-not-quiet` moves from SH1 to SH14, as above. Five arm runs are new.
- Every other campaign that builds the listener FSM (acmp, notify, d3, aecp, dispatch, ctr, gsi, name_wr, name_state, elab guards) is identical at the head.
- Gates ran at 65d39b0c. Commit 6 changes only `tb/srp_top/README.md` and one required tag in `tb/srp_top/mutants.py`; the gates that read the docs ran again at 324ac9a7 and are identical. Every campaign ran at 324ac9a7.

Area, 8x8 `KL_pp_shadow` (module defaults), the scratch parent of round 2 (dev 78ca9bdf + the four adoption patches): main 56,743 LUT / 26,331 FF (re-measured, unchanged), head 58,046 / 26,949. That is +1,303 LUT and +618 FF against main, inside the accepted +1,335 / +618. Round 3 is -32 LUT and 0 FF against 7b424cdf. LUTRAM, BRAM, DSP and carry are unchanged. No 1x1 figure of `KL_pp_shadow` was measured.

Consumer gates: not run, per the assignment (the manager runs them).

Evidence: lane receipts (HANDOFF Round 3, PR body Round 3, receipts/round3 with its index).

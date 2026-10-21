[A661] REVIEW READY
Head: processor `193-shared-listener-leave` = 4f57e22006ca727abace93a0cb8585484a377352. That is three new commits on the PR #198 head 47434635; not pushed, no rebase, no amend.

Round 4 (the [A10] assignment on PR #198, answering R679-3 and R680-3). This round changes tests and docs only. The RTL logic is unchanged: one commit edits comment lines of `KL_srp_listener_fsm.sv`, and sv2v gives byte-identical Verilog for the listener at 47434635 and at the head. STOP condition not hit: the new check exposes no defect.

- R679-3-F1: new check SH24, which requires every Listener push of a walk to come before its done strobe.
  - Setup: sink 4 takes sink 7's applicant over at clock 1-12 of a tx! walk (AN) or an own LeaveAll's walk (QA). The handover lands ahead of the walk, behind it (the second pass needs more than 2 clocks to reach sink 4), or after it ended.
  - Each walk must send one message for the stream, the model's, before the strobe, and nothing in the 60 clocks after it.
  - Control `listener-walk-done-before-second-pass` is the named edit, `txop_done_o <= 1'b1` in W_DONE with the second pass kept. It is KILLED on SH24 ("tx! walk, clock 3: strobe at clock 9, before it '', after it '0/2'", and the same for txLA! with '3/2').
  - R679-3's `order_probe.py`, unchanged: LATE 0 of 72 at the head; LATE 32 with the control planted; LATE 32 with R679-3's own arm.
- R679-3-R1: applied as written (the srp_top README row).
- R679-3-R2 and R680-3-R1: applied as written in the PR text. The opening now also lists the merge of main 859b537b.
- R679-3-S1: the banner and 10 §6.4 state the group mark's LA/LO exception.
- R679-3-S2: SH1's received-LeaveAll check now runs one more tick, as suggested. With `listener-rider-not-quiet` planted, that alone still passes.
  - Measured: the rider above the owner goes to LO and stays there for 8 ticks, and its Empty never goes out, because the owner's transmit marks the group in every walk.
  - So SH1 also requires the rider to stay VO after those ticks. With the edit planted, SH1 fails again ("rider LO").
  - The control stays required to fail SH14 and now fails 15 checks.

Records, base 47434635 vs head, each in a clean clone, all rc 0:
- run_suites: 1,030,395 -> 1,030,399 (only srp_stream_fsms, 1,418 -> 1,422).
- req-tags, lint, matrix, portability elaboration and guards: identical. make check: identical but for the new patch file.
- srp_top campaign: 208/208 at 324ac9a7 (the merge of main changes nothing it builds) -> 209/209, coverage 131/131 -> 132/132.
  - 182 arm runs keep their verdict and tags.
  - Six controls fail more checks (SH24, and SH1 for three), and the README counts match.
  - The new arm is KILLED on SH24.
- Not run, per the assignment (the manager runs the banks): the pp_top, name_state and elab-guard campaigns and the consumer gates. They build the listener, whose change is comments only.
- Area: not re-measured, because the netlist input is unchanged. Round 3's figures stand: +1,303 LUT / +618 FF at 8x8.

Evidence: lane receipts (HANDOFF Round 4, PR body Round 4, receipts/round4 with its index).

[A666] REVIEW READY
Commit: c2a080aef7cd9a4ee2cd1bb4f8214b529bfd8c83 (branch 775-offformat-seq-advance, round 2 of PR #777: three new commits on c7e87c8c, no rebase or amend, still on dev a032c6d6; not pushed, the manager pushes)
Changed (answering R685-1 per the round-2 assignment on PR #777):
- F1, tests (50275e29): tb/verilator/avtp_rxmon/sim_main_nx.cpp adds two AAF [SQ] arms.
  - [SQ4], :1066-1085: an off-format PDU first in a fresh era, on an unlocked stream. The stream stays unlocked and MEDIA_LOCKED does not move at the reject; MEDIA_LOCKED +1 at the first accepted PDU after it.
  - [SQ5], :1092-1119: an off-format PDU inside the settle window with one PDU of it left. A gap at that PDU counts nothing (not shortened), and the next gap counts SEQ_NUM_MISMATCH +1 (not restarted).
  - Each arm keeps the existing counter checks. [SQ0]-[SQ3] are unchanged; [SQ] is split into three phases to stay under the 100-line function ratchet.
- F1, mutants (50275e29): format_mutants.py gains two arms, lock set and settle step (the review's lock_set and settle_dec), each the defect in the engine and in the same line of the lockstep reference.
- F1, docs (3f5cebd0): docs/testing/TESTING.md:617 states exactly what [SQ] grades at each of the three points, that the mr reference and seed are graded through MEDIA_RESET, and that the 100 ms silence watchdog across a reject is not graded.
- F2, comments only (c2a080ae): KL_avtp_rx_monitor_ctx.sv:96-100 carries the review's exact delta text for #775, and :19-23 no longer places #775 inside the flat module's contract. The file is identical after comment stripping (verilator -E -P, 804 lines, same SHA-256), so no RTL line changed and route-1x1 was not rerun.
- F3: out of scope, per the assignment.
Validation (clean clones at c2a080ae, pinned Verilator 5.050):
- make -C tb/verilator/avtp_rxmon: rc 0. Flat 97/0, NX 194/0, lockstep N=1 116/0 and N=8 119/0, lockstep_mutants.py 14/14, format_mutants.py 11/11.
- Planted controls, engine and reference together:
  - lock set fails [SQ4f] MEDIA_LOCKED +1 at the first accepted PDU (got 0), and [SQ4c].
  - settle step fails [SQ5c] a gap at the window's last PDU counts no SEQ_NUM_MISMATCH (got 1), and [SQ5d] and [SQ5g].
- The review's probe_lock_settle.py from the archived packet: with both copies planted, NX now fails those named [SQ] checks, while the lockstep still passes (116/0, 119/0). The review's probe_mutants.py: 12 of 13 caught (10 at c7e87c8c). The survivor is F3.
- Full sweep as 4 parallel shard units: rc 0, 64/64 suites, 2,189,642 checks, 0 failures (+27 over round 1: NX +25, format_mutants +2).
- lint_rtl.py --check: rc 0 (89 <= 89). The 30 static gates: rc 0.
- Docs workflow gates under GNU Make 4.3: 42 run, rc 0, builder legs included. Not run, as in round 1: gate_42 and the no-git step.
Acceptance criteria: met. The issue's acceptance items are unchanged since round 1, where the review found all of them met; R685-1 F1 and F2 are now closed by the evidence above.
Open risks/questions:
- F3, a reject that refreshes the 100 ms silence watchdog, is ungraded and predates #775. It is left to the manager as a possible new issue.
- The flat test instrument KL_avtp_rx_monitor keeps its old reject path, as in round 1.
- No bench run here.

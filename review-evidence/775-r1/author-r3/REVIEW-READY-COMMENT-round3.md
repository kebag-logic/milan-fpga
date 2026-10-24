[A666] REVIEW READY
Commit: 220b51f2eb50c32f830e0b5a8ee1ce138b218bb6 (branch 775-offformat-seq-advance, round 3 of PR #777: four new commits on c2a080ae, no rebase or amend, still on dev a032c6d6; not pushed, the manager pushes)
Changed (answering R685-2 and R686-2 per the round-3 assignment on PR #777; tests, docs and one comment rewrap, no RTL line):
- R686-2-F1 and R685-2-S1 (a8ddb31a): format_mutants.py's two-copy arms now write both planted copies and build both. The N=4 stack is built from the planted engine (it compiles no reference) and must fail the arm's named [SQ] check. The lockstep leg at N=1 and N=8 is built from the planted engine and the planted reference, and its result is printed as measured, not graded. Each arm prints its two planted file names and the lockstep result on the pair.
- R685-2-F1 (a8ddb31a), the review's option (b). tb/verilator/avtp_rxmon/sim_main_nx.cpp adds two arms:
  - [SQ6], :1124-1148: a reject on a freshly bound stream, then the era's first accepted PDU with mr = 1, which counts no MEDIA_RESET.
  - [SQ7], :1150-1181: a reject on a seeded stream (mr reference 0), then an accepted PDU with mr = 1, which counts MEDIA_RESET once.
  - format_mutants.py also gains two two-copy arms, mr seed set and mr seed clear (the review's mr_seed_set and mr_seed_clear, byte for byte).
- Docs (de094b8a): docs/testing/TESTING.md:617 states the two seed arms. It says a reject that sets the seed, clears it, or writes its own mr into the reference is graded through MEDIA_RESET, and it says what the two-copy arms build and grade.
- R685-2-R1, comments only (db5d9d27): the banner rewrap at KL_avtp_rx_monitor_ctx.sv:18-22, same words. The file at c2a080ae and 220b51f2 is identical after comment stripping by verilator -E -P (804 lines, 026a45f4...) and by the review's strip_sv_comments.py (804 lines, 7c744642...). No route was run.
- Tally fix (220b51f2): the lockstep result on a planted pair is printed as "N=1 116/0, N=8 119/0 (checks/failures)". At db5d9d27 it was printed as the harness's own tally lines, and the sweep's tally (scripts/suite_tally.py) read the first tally on each of those 4 lines, so it counted 464 checks of mutant pairs as checks of the tree. A failing pair would also have failed the suite. The db5d9d27 runs are kept under receipts/round3/superseded-db5d9d27; every gate was rerun at 220b51f2.
Validation (clean clones at 220b51f2, pinned Verilator 5.050):
- make -C tb/verilator/avtp_rxmon: rc 0. Flat 97/0, NX 218/0, lockstep N=1 116/0 and N=8 119/0, lockstep_mutants.py 14/14, format_mutants.py 13/13. The sweep's tally reads its log as 577 checks (97+218+116+119+14+13).
- Two-copy arms. Each fails its named check in the N=4 stack; the lockstep on each planted pair, as measured, gives rc 0 at N=1 116/0 and N=8 119/0:
  - lock set fails [SQ4f], and also [SQ4c].
  - settle step fails [SQ5c], and also [SQ5d] and [SQ5g].
  - mr seed set fails [SQ6e] ...and counts no MEDIA_RESET: it seeds the reference (got 1), and also [SQ6c] and [SQ6i].
  - mr seed clear fails [SQ7d] MEDIA_RESET +1 at the toggled PDU after the reject (got 0), and also [SQ7c] and [SQ7e].
- The review's probe_sq_claims.py from the archived packet catches 6 of 6 (4 of 6 at c2a080ae). Its probe_lock_settle.py gives the round-2 result.
- cd tests && behave --no-capture -f plain: rc 0, 14 features, 406 scenarios, 1977 steps, 0 failed.
- Full sweep as 4 parallel shard units: rc 0, 64/64 suites, 2,189,668 checks, 0 failures (+26 over round 2: NX +24, format_mutants +2).
- lint_rtl.py --check: rc 0 (89 <= 89). The 30 static gates: rc 0.
- Docs workflow gates under GNU Make 4.3: 42 run, rc 0, builder legs included. Not run, as in rounds 1 and 2: gate_42 and the no-git step.
- The new arms pass on the shipping RTL, so no arm shows the RTL wrong and no STOP.
Acceptance criteria: met. The issue's acceptance items are unchanged since round 1. R685-2 F1 and R1 and R686-2 F1 are answered by the evidence above.
Open risks/questions:
- R685-1-F3, a reject that refreshes the 100 ms silence watchdog, is still ungraded and disclosed. It is left to the manager.
- The flat test instrument KL_avtp_rx_monitor keeps its old reject path, as in round 1.
- No bench run here.

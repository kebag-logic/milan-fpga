[A726e] REVIEW READY
Commit: a67eaf66c99b6b07c7ef206ad3489cb9555e00ca
Changed: round 5 on top of round 4 head c1b2961777809403bd2de833ec1fa00c75394d6c, 5 one-line commits, tests and docs only; scripts/owned_process.py is byte-identical.
- R764-4-F1 (MINOR, Tests and Docs): owner_shell_window's trap now ends with 0.3 s of builtins and no child (read -t on a FIFO), then an observable last step. A guard that spares a resumed shell for one pass or 1 s is red: "the resumed shell was killed inside its own window, with no child to spare it". TESTING.md:274.
- The class: all 131 mutants published for this PR (R763-1..4, R764-1..4, round 1's table, round 3's own) reduce to 43 distinct ones. All ran at round 4's head and at this one through one driver, against every owner control and the whole test. The 10 that were green everywhere at c1b29617 now have controls, and nothing was narrowed:
  - new owner_stated_seconds: production constants on an owner whose every census pass stalls; grace, 14 s, the window and 20 s checked pass by pass;
  - new owner_reused_identity;
  - owner_reparented: SIGTERM in that pass;
  - owner_late_cancel: the collected shell still listed in that pass.
  One mutant is equivalent and is listed with its reason.
- MUTANTS in scripts/process_test_support.py lists every mutant with the control it must fail and its words. python3 scripts/test_suite_cancellation.py --mutants [--matrix] runs it beside the preflight, as an explicit campaign. TESTING.md:281 states that a stated cleanup behaviour is one some control pins.
- R764-4-S1: derived, not widened. The child is held until census pass 61, so the resume is at least 1.22 s on the owner's clock however the owner stalls.
- Residue R764-3-R1: the exact fix at :683.
- A fifth commit rewords one comment that the bare-metal scope gate refused.
Validation, all rc 0 at this head, one log and rc each:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (43 mutants, 42 with a control that must fail); --matrix: 506 runs PASS;
- R764-4's own matrix.py and repeat_control.py: only its two shell-window rows change, both now red 3/3 and 16/16, with none green 16/16;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: unchanged from round 4; product code untouched; every stated cleanup behaviour some published mutant broke is now pinned by a named control.
Open risks/questions: the preflight grows by about 1.5 s (the shell-window control takes 4.7 s against 3.3 s; the two new controls 0.1 s). The PR body's Round 5 section is ready for the manager to apply; this lane does not edit the PR.

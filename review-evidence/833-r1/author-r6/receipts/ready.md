[A726f] REVIEW READY
Commit: a987b601a0c10049321c18847504c4a94a862e04
Changed: round 6 on top of round 5 head a67eaf66c99b6b07c7ef206ad3489cb9555e00ca, 6 one-line commits, tests and docs only; scripts/owned_process.py is byte-identical. In the ruling's order (issuecomment-6582585294):
- R763-5-F3 (MAJOR): owner_shell_window's hold is bounded on both sides. A 40.5 s reap stage puts the verdict at 40.9 s of owner clock, past the child's 61 census passes, which are at most 30.5 s at the 0.5 s cap, however slow each pass is. The resume stays past grace + 1 s.
- The table: docs/testing/TESTING.md:255-289 states every cleanup behaviour as a row, 16 rows. Each row names the control that pins it and the MUTANTS that prove it. A short "Not pinned by a control" list gives three reasons only the product's comments state, each with why. Every cleanup statement of the earlier prose and control list is a row, so nothing was narrowed. TESTING.md:285 says: "A stated cleanup behaviour is a row of this table; one that no control pins is on the list above, with the reason."
- The five gaps, all pinned, none moved:
  - R764-5-F1, the signal through the handle (`signal-by-number`): owner_reused_identity has the number change hands right after the recheck. A blocked SIGTERM makes a by-number signal visible at once.
  - R764-5-F1 and R763-5-F1, the stubborn parent's SIGKILL at 4 s: `parent-spared-past-kill-all`, `parents-killed-at-grace`.
  - R764-5-F1, the vanishing listing's 10 s and no later: `vanishing-waits-30s-more`.
  - R763-5-F2, the report's current parent and age: `report-without-current-parent`, `report-age-in-ticks`.
- One more mutant of the lane's own for each of the 16 rows. Each is red on its control with its words, and each is in MUTANTS. One of them, `resume-unless-reaped-now`, was green at first: owner_late_cancel modelled only a shell collected in the cancel's own pass, and it now covers a later pass too.
- R764-5-R1, the exact fix. R763-4-X1 is merged into the table's second-stage row. R763-5-S1 is taken: under a launcher that ignores SIGHUP, the campaign's runs get it at its default.
- A sixth commit, disclosed: item 3's report control paused after its sleep check, and was red 3 of 160 unmutated at 16 jobs. The pause now comes first: 0 of 160.
- Every round 5 reviewer mutant is in MUTANTS: 15 published, 13 distinct, matched by hash. MUTANTS has 74 mutants and none, all distinct.
Validation, all rc 0 at this head, one log and rc each:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (74 mutants, 70 with a control that must fail), also at every item's commit; --matrix 825 runs PASS: none green on all 11, the 4 with no control green on all 11;
- the reviewers' own probes, unchanged:
  - slow_census_probe.py PASS at 0.15, 0.2, 0.3 and 0.5 s (and at 1.0 and 1.75 s);
  - kill_all_probe.py and report_probe.py: rc 0 here, rc 1 on each mutant;
  - probe_mutants.py: its three F1 mutants red;
  - probe_effect.py: the head row as R764-5's own;
- owner_shell_window green 24/24 unmutated, and all its listed mutants red 6/6 with their words;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: unchanged from round 5; product code untouched; every stated cleanup behaviour is a row of TESTING.md's table, pinned by its control and proved by its mutants, and no behaviour was moved to the not-pinned list.
Open risks/questions: none. The preflight grows by about 0.2 s: the report control's 0.1 s pause, and the reused-identity control's second process. The PR body's Round 6 section is ready for the manager to apply; it is 60,430 characters, because two superseded tables now point to their copies on 833-review-evidence. This lane does not edit the PR.

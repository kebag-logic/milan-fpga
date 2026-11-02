[A726g] REVIEW READY
Commit: 887fdd53b013cc8796c1d595644a2a9f0b8c27a5
Changed: round 7 on top of round 6 head a987b601a0c10049321c18847504c4a94a862e04, 5 one-line commits, one per item of the manager's round 7 ruling (issuecomment-6585868556), tests and docs only; scripts/owned_process.py is byte-identical. Pinned, never narrowed:
- R764-6-F1, row 1: owner_reused_identity hands the number over for SIGTERM and again for SIGKILL, with a stale-start check for both. The process that takes the number blocks SIGTERM and SIGCONT, and a SIGKILL stays pending until it is collected, so any signal _send sends by number is pending at once. rv6-sigkill-by-number and rv6-sigcont-by-number are red with "a census entry was signalled by its number" and named in row 1.
- R764-6-F2, row 5, and R763-6-F1, rows 6 and 8: owner_stated_seconds resumes the cancelled shell in its first pass, with nothing else live, inside grace. Its trap's command, listed from the next pass, gets no SIGTERM and no SIGKILL until 10 s after the resume. A second listing has a survivor's trap start a cleanup command with no shell resumed, and it gets no SIGTERM either.
  - rv6-resume-not-before-grace, rv6-resume-not-first-pass, sigterm-to-new and rv6-sigterm-trap-commands are red with "a first-pass resume's stated seconds were not kept". The lane's sigterm-to-new-before-resume is red with "a new descendant's stated seconds were not kept".
  - They are named in rows 5, 6 and 2. Not-pinned item 2 is gone: all of it is pinned.
- R764-6-S2: each row's "Pinned by" cell names the domain of each control, and each domain equals its row.
  - Where one fell short, the control was widened. owner_stated_seconds now lands a tick (2^-20 s) short of every stated time and then on it.
  - Its passes run from a tick to an hour.
  - It resumes in the first pass, at 3 s, at 5.5 s, a tick before 14 s, and never.
  - Every verdict must report its live child's wall time since that child's first SIGKILL. That was a survivor: the lane's own row-16 edge mutant survived every control before.
- Item 4: one mutant of the lane's own at the edge of each row's domain, 18 for 16 rows, each red on its control with its words and named in its row.
- R764-6-R1, R2, R3: the exact fixes. For R3, owner_shell_window is dropped from row 10. R763-6-S1 is taken: rv6-return-before-confirm is red on owner_vanishing, row 12. R764-6-S1 is not taken: it predates this PR and is outside #833, so it is suggested as a new Issue.
- MUTANTS: 99 mutants, 96 with a control, all named in the table; the 3 with no control are in no row.
Validation at this head, one log and rc each, SIGHUP at its default; every gate rc 0:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (99 mutants, 96 with a control that must fail), also at every item's commit;
- --matrix in 4 parts, 1100 runs, each PASS:
  - none green on all 11;
  - each mutant with a control red on it and on the whole test;
  - the 3 with no control green on all 11;
- the reviewers' probes, unchanged:
  - row_mutants.py: no survivor among its 10;
  - grace_resume_probe.py: PASS 3/3 here, FAIL 3/3 on each of its 3 mutants;
  - sigcont_pending.py: rc 0;
  - both table checks: R764-6's rc 0, R763-6's flags only windows-2s, which it accepted;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: unchanged from round 6, product code untouched. Every row of TESTING.md's cleanup table states the domain its controls cover, equal to what it states, and every row has a mutant at that domain's edge.
Open risks/questions:
- Under host load near 100, two existing mutants of the unchanged real-time owner_shell_window sometimes fail their own check:
  - trap-commands-1s went green, twice;
  - shell-window-one-pass was red, but with the trap command's words instead of its own, once.
- Above about 0.75 s a census pass, a 1 s window cannot be told from 10 s against the trap's real 1.5 s command. Both mutants are red 8 of 8 at load 25 to 42, and the gates here passed.
- Both are also red, with no timing, on owner_stated_seconds. Naming that control instead is a manager decision, outside this round's items.
- The preflight is unchanged in time: each control within 0.06 s, the whole test 63.5 s at both heads.

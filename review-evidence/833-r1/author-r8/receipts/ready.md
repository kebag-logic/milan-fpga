[A726h] REVIEW READY
Commit: 5b6d38a3542119ad77d352ea992e3cc41d121620
Changed: round 8 on top of round 7 head 887fdd53b013cc8796c1d595644a2a9f0b8c27a5, 5 one-line commits, one per item of the manager's round 8 ruling (issuecomment-6588568293), tests and docs only; scripts/owned_process.py is byte-identical. Pinned, never narrowed:
- R763-7-F1 = R764-7-F1, ruling item 1: owner_stated_seconds has a resume-timing matrix. It resumes the cancelled shell in each class of pass, at its earliest and its latest pass:
  - the first pass, inside grace;
  - a later pass inside grace: pass 2, a tick in, and the last pass before 2 s;
  - the first pass past grace, at 2 s;
  - a later pass past grace: the next pass, a tick after 2 s, and the last before 14 s.
  - In each cell the shell is then alone, or its trap starts a command, listed from the pass after the resume. Each cell's whole event list is asserted to a tick: rows 2, 3, 5, 6, 7 and 8 as they apply.
  - "First pass past grace" is read as the first pass at or past 2 s, since the first pass of cleanup is always inside grace. The PR body and the guide say so.
  - R764-7's feasibility listing, a resume at 1 s, is beside the matrix, as published.
- R763-7-F2: R763-7's feasibility listing, as published: a descendant new since the first census, listed inside grace while the cancelled shell stays stopped.
- Ruling item 2: every reviewer mutant published at round 7 is in MUTANTS under a behaviour name, with the published edit byte for byte. That is nine names in eight edits, since two are the same edit. Each is red on a named control with its words and named in its row. The PR body lists each with both reviewers' names.
- Ruling item 3: the testing guide tables the matrix's cells with each listing's words. Rows 2 to 8 name the cells they cover, and no row claims a cell that no listing exercises.
- Ruling item 4: twelve edge mutants, one per cell at its class's earliest or latest pass. Run with every listing checked, each is red on its own cell's listing and on no other.
- RESIDUE: R763-7-R1, R2 and R764-7-R1 take the exact fixes. R763-7-R3 and R764-7-R2 are resolved by the matrix: the notes and the docstring name the resumes the control makes.
- SUGGESTION:
  - R763-7-S1 and R764-7-S1 taken: the rv6-* names are renamed by behaviour.
  - R763-7-S2 taken: the corrected grace probe is the one quoted.
  - R764-7-S2 taken: trap-commands-1s and shell-window-one-pass name owner_stated_seconds, where they are red with no timing.
  - R764-6-S1 not taken, as in round 7.
- The starved owner's clock moved unchanged to scripts/process_test_support.py, so the test module stays under the 1000-line ratchet at 965 lines.
- MUTANTS: 119 mutants, 116 with a control, all named in the table.
Validation at this head, one log and rc each, SIGHUP at its default; every gate rc 0:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (119 mutants, 116 with a control that must fail), also at every item's commit;
- --matrix in 4 parts, 1353 runs, each PASS:
  - none green on all 11;
  - each mutant with a control red on it and on the whole test;
  - the 3 with no control green on all 11;
- the reviewers' probes, unchanged:
  - row_mutants.py, r7_mutants.py and rv7_mutants.py: no survivor;
  - grace_resume_probe.py: PASS 5/5;
  - grace_resume_probe2.py: PASS 3/3 here, FAIL 3/3 on each of 4 mutants;
  - both feasibility probes: as published;
  - slow shell-window campaign: PASS, 45 runs;
  - sigcont_pending.py: rc 0;
  - table checks: all pass, except R763-6's, which flags only windows-2s, as it accepted;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: unchanged from round 7, product code untouched. Every cell of the resume-timing matrix has a listing and an edge mutant red on it alone, every round 7 reviewer mutant is red with its words, and every row's domain note names the cells it covers.
Open risks/questions:
- R764-7's whole-test mode (RV7_WHOLE=1) stops at its own report line on its first red result, since it joins None. That first run was red; --matrix gives the whole-test column for all four.
- The preflight is unchanged in time: owner_stated_seconds takes 0.16 to 0.21 s at both heads, and the whole test 60.6 s at round 7 against 60.4 s here.

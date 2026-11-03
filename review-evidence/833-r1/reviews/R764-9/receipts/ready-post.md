[A726i] REVIEW READY
Commit: e803d94b3a11921a293cf036a8eda333d23828f9
Changed: round 9 on top of round 8 head 5b6d38a3542119ad77d352ea992e3cc41d121620, 4 one-line commits, one per item of the manager's round 9 ruling (issuecomment-6590477473), tests and docs only; scripts/owned_process.py is byte-identical. Pinned, never narrowed:
- Ruling item 1, the liveness axis. In owner_stated_seconds a real process, which the product sees as live, stands for a live descendant new since the first census. Its listings:
  - R763-8-F1: beside a stopped shell before any resume. The child's trap starts it as the child exits, it alone holds the shell, and the shell is resumed only once it is gone, at 3 s.
  - R764-8-F1: with no cancelled shell. A survivor's trap starts it, and the survivor is spared to 4 s while it lives.
  - R764-8-F1: as the trap's command after a resume in pass 1 and pass 2, inside grace. Beyond the ruling, it is also live in every other matrix cell with a trap command, so liveness crosses every class of resume.
  - R763-8-F2: late in grace. Read as the trap's command, live or not, first listed in the last pass before 2 s after a resume a pass earlier, since a live command is listed only from the pass after its resume. A zombie the stopped shell has not collected, sent SIGKILL at 2 s, puts that pass a tick before 2 s.
  - Each listing asserts its whole event list, to a tick, so its rows' behaviour.
- Ruling item 2: all 13 reviewer mutants published at round 8 are in MUTANTS, each with its published edit byte for byte, red on owner_stated_seconds with its words, and named in its row. The PR body lists each with both reviewers' IDs. R764-8's two interior mutants, green at round 8, turn red on a lone resume at 1 s and one at 10 s.
- Ruling item 3: the guide's matrix has a live column, and the liveness cells are tabled beside it. Rows 2 to 8 name them. Ten edge mutants, one per new cell, each red on its own cell's listing alone.
- Ruling item 4, RESIDUE: R763-8-R1, R2 (= R764-8-R1) and R3 take their exact fixes.
- SUGGESTION: R764-8-S1 is taken: the guide says once that a cell's domain is its listed resume, the reading the ruling and the review use; no row's claim changes. R764-6-S1 is not taken, as in rounds 7 and 8.
- window and the matrix's classes moved unchanged to scripts/process_test_support.py. So owner_stated_seconds is 87 lines and the test module 997, under the 100 and 1000 limits.
- MUTANTS: 142 mutants, 139 with a control, all named in the table.
Validation at this head, one log and rc each, SIGHUP at its default; every gate rc 0:
- every run: step of .github/workflows/docs.yml: verifier 64 steps rc 0, 31 not run with round 1's reasons, 0 bad; builder legs EXCEPT 1 / EXCEPT 16 NOT RUN;
- python3 scripts/test_suite_cancellation.py: PASS;
- --mutants: PASS (142 mutants, 139 with a control that must fail), also at every item's commit;
- --matrix in 4 parts, 1606 runs, each PASS:
  - none green on all 11;
  - each mutant with a control red on it with its words and red on the whole test;
  - the 3 with no control green on all 11;
- every reviewer probe from rounds 6, 7 and 8, unchanged: no survivor;
  - R764-8's boundary and liveness probes: all red, the two interior ones included;
  - R763-8's two mutants and its every-listing sweep over 47 mutants: all red;
  - both round 8 feasibility probes: as published;
  - the round 6 and 7 mutant probes: no survivor;
  - grace_resume_probe2.py: FAIL 3/3 on sigterm-to-live-new with a real trap command;
  - every table check passes, except R763-6's, which flags only windows-2s, as it accepted;
- make -C tb/verilator/gptp_shadow lifecycle: PASS;
- cd tests && behave: 508 scenarios passed;
- git diff --check 1f29f189 HEAD: silent.
Full sweep not rerun: only files round 1 changed.
Acceptance criteria: unchanged from round 8, product code untouched. Every new liveness cell has a listing and an edge mutant red on it alone, and every round 8 reviewer mutant is red with its words. The domain notes name the liveness cells. The preflight grows by about 11 ms (owner_stated_seconds 29 to 40 ms in-process; the whole test a mean of 60.9 s at both heads).
Open risks/questions:
- Outside this round: the unmodified owner_report control was red in 4 of 1152 repeated runs at load about 42, 16 at once: 1 of 512 at round 8's head, 3 of 640 here. Each red read state R of a child that sleeps 20 ms a loop, after the control had seen it asleep. So it is the control's own race between that wait and the report; the report itself was right. owner_report and _describe are unchanged in round 9, and every gate run was green. It is disclosed for a ruling and not changed.
- R764-7's whole-test mode stops at its own report line on the first red result, as in round 8; --matrix has every whole-test column.


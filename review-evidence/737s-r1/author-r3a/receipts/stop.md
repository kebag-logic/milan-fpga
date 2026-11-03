[A727d] STOP
Head: ae7412eb293c6a52d64f86b57e69835c7d20121a (branch 737-elab-split, 4 commits over the round 2 head e180ba30, one per round 3 item; local lane, not pushed)
Reason: applied to attempt 3 of run 41678609075, round 3 item 1 (bounds from component maxima) needs a decision no issue settles. Attempt 3 finished after item 1 was committed from attempts 1 and 2.

Evidence, from the jobs API and job logs of run 41678609075 attempt 3, at e180ba30: all five workers succeeded and every simulation ran once and passed.
- Setup (job span less gate step and Verilator build) on workers 0 to 4: 362, 399, 442, 485 and 398 s. Attempt 1's largest was 255.
  - The excess is the full-history checkout (99 to 208 s), "Install LiteX at the pinned revisions" (89 to 143 s; the LiteX workers carry no pip cache since option (B)) and the VexiiRiscv placement (36 to 59 s).
- Members: `test_soc_timing_cuts` 510 s (largest before 369), `test_gptp_tx_timestamp` 462 (461), `test_ctrl_memory` 284 (280).
- The `elaborate` aggregate was cancelled again at its 3-minute limit ("The job has exceeded the maximum execution time of 3m0s"), 149 s into the full-history checkout that ae7412eb removes.

With the ruling's rule (setup 485, cold Verilator 431, the 338 s allowance, the 3 s self-test):
1. `LEG_BUDGET` = 1800 - 338 - 485 - 431 - 3 = 543 s.
   - The members' largest seconds total 1704, so no three-leg partition fits: the bound is 568, and the best fullest leg found by exhaustive search is 620.
   - The current legs hold 462 / 448 / 794. Four legs fit (510).
   - A fourth LiteX worker is one more concurrent runner per head, which round 2's queueing decision kept at three.
2. Builder worker 0 projects at 485 + 1130 = 1615 s, so the elaborate workflow projects at 1953 s, above #737 acceptance 1's 30 minutes (1885 even at the former 270 s allowance).
   - That holds whatever the LiteX legs do. No ruling covers dividing builder leg 0 (one gate) or a projection above 30 minutes.

Options (the decision is the manager's):
(a) a fourth LiteX leg;
(b) cut the setup:
  - shallower worker checkouts: the scope step needs only the head's parent on hosted runs, but the checkout contract in `scripts/ci_events.py`, in the act trust set, admits only `fetch-depth: 0`;
  - a pip cache on the LiteX workers, reversing that part of option (B);
(c) bound setup by a stated figure, or exclude a hosted-latency outlier from the maxima;
(d) accept a projection above 30 minutes and keep acceptance 1 open.

Done at this head (gates below):
- item 1 (f66312c4), committed from attempts 1 and 2; attempt 3 breaks its figures (above).
  - `LARGEST` holds each member's largest verdict row, and the legs (from `SECONDS`) must fit `LEG_BUDGET` at it.
  - Every projection is a sum of component maxima.
  - `CI_WORKFLOWS.md` states the re-measurement rule once.
- item 2 (a174e9e5), R767-2-F1 / R768-2-F2:
  - Builder leg 1 runs every `--require-elaboration` gate and generates the CPU metadata. A local cold run of gate 23g alone wrote it.
  - Builder leg 0 elaborates nothing: it saved the key empty at a cold key.
  - LiteX generates whatever it lacks, so no worker reads the metadata without generating it.
  - Only `elaborate-gates-1` now carries the metadata cache and the step that fills it; generation refuses any other arrangement.
- item 3 (e4d52a12), R767-2-F3 / R768-2-F3:
  - The elaborate aggregate checks out the head alone; it reads only the head's tree.
  - Its 3-minute limit stays, against a 44 s projection (largest depth-one checkout 19 s plus largest span less checkout 25 s).
  - `Collect CI manifest` keeps its full fetch, because it reads the merge base, and took at most 149 s of 15 minutes. The act sandbox validation accepts the workflow.
- item 4 (ae7412eb):
  - R768-2-S1: literal names in the self-test; its mutant now fails the self-test.
  - R768-2-S2: 1883 / 2307 / 2825 s. R768-2-RS1 is in the PR body text.
  - R767-2-R1 and S1 were answered by item 1.
  - Declined, with reasons in the handoff: R768-2-S3's placement copy.
Gates at ae7412eb, each rc 0:
- `ci_gate_workflows.py --check`;
- `ci_events.py --check`, and `--selftest` (5489 arms);
- `run_litex_sims.sh --selftest`;
- the gate workflow and LiteX leg self-tests;
- `ci_scope.py --selftest`;
- behave (508);
- `git diff --check e61a4afa`;
- the act sandbox validation;
- the docs workflow steps that read the changed files.
Controls and mutants:
- The `union` over round 2's real leg receipts passes. Dropping `test_pp_boot_bus_freeze` refuses with "LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze", and restoring it passes.
- Mutants of the metadata removal, the head-only checkout and the cache names each fail the self-test.
Not run: the three local LiteX leg commands, since the decision may change the legs.
Known defect: item 3's new paragraph in `docs/testing/CI_WORKFLOWS.md` (about line 3273) runs into the receipts paragraph after it. The fix is recorded for the next round.

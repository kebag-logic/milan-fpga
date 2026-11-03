[A727e] REVIEW READY
Commit: 3b323864232fa430ec3a185f33ad7b30fbf1156b (branch 737-elab-split, five commits over ae7412eb; local lane, not pushed; PR #836 is at e180ba30)
Changed:
- Item 1, under the STOP ruling (d), commits 4f6cf352 and e2426156:
  - `scripts/ci_litex_legs.py` derives `LEG_BUDGET` from named constants: `JOB_LIMIT` 2700 - `HEADROOM` 600 - `SETUP` 485 - `COLD_VERILATOR` 431 - `SELFTEST` 3 = 1181 s.
  - `LARGEST` includes run 41678609075 attempt 3 (`test_soc_timing_cuts` 510, `test_gptp_tx_timestamp` 462, `test_ctrl_memory` 284). The legs hold 462 / 448 / 794 at `LARGEST` and fit, so three legs stay.
  - The LiteX leg self-test requires each LiteX worker's generated limit to equal 2700 s.
  - Every elaborate worker is projected as the sum of its component maxima against 2700 s: builder workers 1615 / 1604 (margins 1085 / 1096); LiteX cold 1381 / 1367 / 1713 (1319 / 1333 / 987); LiteX with Verilator restored 950 / 936 / 1282.
  - The re-measurement rule is stated once, in `docs/testing/CI_WORKFLOWS.md`.
- Item 2, commits 4dc72137 and 3b323864: the elaborate workflow figure is stated as a measurement against #737 acceptance 1, which stays open, not as a bound.
  - It is 2013 s with Verilator restored and 2111 s cold. The allowance is 398 s, because attempt 3's aggregate spent 85 s outside its checkout, 82 of them before its first step. The 1953 s figure used the earlier 338 s allowance.
  - The shallower worker checkout and a LiteX pip cache are recorded as candidates for acceptance 1, not taken here.
- Item 3, commit d153844b: the metadata cache on the generating builder leg only, and the aggregate's head-only checkout, stand as committed at ae7412eb. The aggregate's 3-minute limit now carries a 104 s projection (margin 76 s). Its docs paragraph no longer runs into the receipts paragraph.
- Item 4: every residue and suggestion of R767-2 and R768-2 was already dispositioned at ae7412eb. Nothing is left, so there is no commit.
Validation, at 3b323864232fa430ec3a185f33ad7b30fbf1156b with 16 CPUs, each rc 0:
- `ci_gate_workflows.py --check`;
- `ci_events.py --check`, and `--selftest` (2199 items, 5489 arms);
- `run_litex_sims.sh --selftest` (16);
- the gate workflow and LiteX leg self-tests;
- `ci_scope.py --selftest`;
- behave (508);
- `git diff --check e61a4afa`;
- the act sandbox validation of the elaborate workflow;
- the docs workflow run steps that read the changed files;
- the three LiteX leg commands, 571 / 410 / 661 s, with each simulation PASS once: gptp 570; cpu 92, gmii 0, boot 31, mem 15, retained 272; ctrl 84, soc 576;
- `union` over those receipts, and the aggregate verifier over them.
Controls:
- Dropping `test_pp_boot_bus_freeze` from leg 1's receipt is refused by both, with "LiteX leg 1 did not run its selection exactly once: test_pp_boot_bus_freeze". Both pass again once it is restored.
- A mutant that sets a LiteX worker's limit to 44 minutes fails the LiteX leg self-test.
Acceptance criteria:
- Round 3 items 1 to 4 and the STOP ruling's items 1 to 4 are met locally.
- Ruling item 4 (hosted proof: a green exact-head `elaborate` run with the union, and a non-empty metadata restore on the second attempt) needs the manager's runs after the push.
- #737 acceptance 1 is not met and stays open.
Open risks/questions:
- The figures are hosted maxima up to run 41678609075 attempt 3. A later larger value replaces a figure by the stated rule.
- Candidate Issues, not taken here:
  - the docs-check aggregate's full fetch under its 3-minute limit;
  - the package-downloads cache tar failure;
  - artifacts unavailable after a re-run.

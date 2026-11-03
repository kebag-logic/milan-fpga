[A727f] REVIEW READY
Commit: 9104a8fc68979a7a8795859e8704aef27ea0634d (branch 737-elab-split, three commits over 3b323864; local lane, not pushed; PR #836 is at 3b323864)
Changed:
- Ruling item 1, the last re-measurement (f3a49b93). Run 41705989293 attempts 1 and 2 join the cited runs, and every component is recomputed from the jobs API over the whole set.
  - Components: setup 739 (worker 1, a2), `test_gptp_tx_timestamp` 477, self-test 4 (leg step less its rows, 481 - 477, a2 leg 0), collector 183, tail 29, depth-one checkout 26.
  - `LEG_BUDGET` = 2700 - 600 - 739 - 431 - 4 = 926 s. The legs hold 477 / 448 / 794 and fit, so the partition is unchanged.
  - Projections against 2700 s: builders 1869 / 1858 (margins 831 / 842); LiteX cold 1651 / 1622 / 1968 (1049 / 1078 / 732); with Verilator restored 1220 / 1191 / 1537.
  - Aggregate 26 + 85 = 111 s (margin 69). Allowance 111 + 183 + 120 + 29 = 443.
  - Workflow figure, a measurement against acceptance 1: 2312 s warm and 2411 s cold.
  - `scripts/ci_litex_legs.py` is re-pinned in `ci/image/command-table.json`. `scripts/ci_gate_workflows.py` changes in a comment only. `docs/testing/CI_WORKFLOWS.md` carries every figure.
- Ruling items 2 and 3 (56e6021a). `CI_WORKFLOWS.md` freezes the cited runs, and the re-measurement rule now applies to the next re-measurement under #737 acceptance 1. Beside it is the merge bar for later hosted runs: a job at its timeout, an elaborate worker's span above 2100 s, a LiteX simulation unrun, run twice or unreported, or the union verifier refusing. The PR body says so in one sentence, linking the ruling.
- Item 3 (9104a8fc), with each exact text: R767-3-R1, R767-3-R2 (docs; the PR body half too), R768-3-RS1 and R768-3-S2 (rewrap). R767-3-S2 is in the PR body: round 2's derived table and workflow paragraph now sit under "Superseded (round 2)". R767-3-S1 (#837), R768-3-S1 and the observations were declined by the ruling and not taken.
Where the arithmetic differs:
- Allowance 443, as R767-3, not R768-3's 436. R768-3 kept the 19 s depth-one checkout; the rule's component rose to 26 s (`Cancel late CI failures`, a1).
- `LEG_BUDGET` 926, not the ruling's 927. Round 3's self-test method (leg step less rows, whole seconds) gives 4 s at a2 leg 0. The log shows 480.6 s against a 477 s row. Keeping 3 would leave a stated maximum the frozen set exceeds. The partition still fits, and worker 4 cold is 132 s inside 2100.
Validation at 9104a8fc68979a7a8795859e8704aef27ea0634d with 16 CPUs, each rc 0:
- `ci_gate_workflows.py --check` and `ci_gate_workflows_selftest.py`;
- `ci_litex_legs.py legs` and `ci_litex_legs_selftest.py`;
- `ci_events.py --check`, and `--selftest` (2199 items, 5489 arms);
- `run_litex_sims.sh --selftest` (16);
- `ci_scope.py --selftest`;
- behave (508);
- `git diff --check e61a4afa`;
- the act sandbox validation of elaborate;
- the docs workflow run steps that read the changed files;
- the three LiteX leg commands, 518 / 410 / 643 s, each simulation PASS once: gptp 518; cpu 90, gmii 0, boot 29, mem 15, retained 276; ctrl 73, soc 570;
- `union` and the aggregate verifier over those receipts.
Controls:
- `LARGEST` `test_gptp_tx_timestamp` at 927 is refused with "a LiteX leg holds 927 measured seconds at its largest, above its 926; re-derive the legs or add a leg". It is accepted at 926, and after the restore byte-equal to the head.
- A dropped `test_pp_boot_bus_freeze` is refused by `union` and by the verifier, and both pass once it is restored.
- A 44-minute LiteX worker limit fails `ci_gate_workflows_selftest.py` with ('elaborate', 2, 44), while the LiteX leg self-test alone passes. Restored; the tree equals HEAD.
Acceptance criteria:
- Ruling items 1 to 3 and the round 4 residues are met locally.
- The hosted run at the pushed head is judged by the merge bar only, under ruling item 3.
- #737 acceptance 1 is not met and stays open.
Open risks/questions:
- `LEG_BUDGET` is 926 against the ruling's quoted 927, for the reason above.
- The merge bar names "an elaborate worker's span" where the ruling says "a job's". The 120-minute watcher ran 2299 s at 3b323864, and the 2700 s parenthetical only fits the 45-minute workers.

[A683k] TAKEN

Branch: `665-s2b-cycles` (local, not pushed), on round 8's final head `59038a1d7c8ec65417fc74d7fb64804d7075e3fe`, whose commits stay. The lane base is `origin/dev-soft-core` `e76a755a`: checked as an ancestor, not dev. The PR targets `dev-soft-core`.

Authoritative references:
- the owner's decision of 2026-10-29 12:40 and the round-9 assignment, issuecomment-6495692075;
- round 8's STOP, issuecomment-6495801236;
- FR_NFR 3.4.1 and NFR-SCOUT-03 (`docs/reference/FR_NFR.md`), with the clauses the bound table cites: IEEE 802.1Q-2018 10.7.11 and Milan v1.2 Table 4.3 (SRP/MRP), Milan v1.2 5.5.2.3 and Table 5.26 (ACMP), IEEE 1722.1-2021 9.3.2.6 and 7.5.2 (AECP, notifications), 7.5.1 (identification), IEEE 1722-2016 B.3.4.2 (MAAP), Milan v1.2 5.6.3.5.2 (ADP);
- S2's harness (`tb/verilator/ctrl_service_budget/`), `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, `docs/design/MAILBOX_SPLIT.md`.

Interpreted scope:
1. **Make the decision normative.** FR_NFR 3.4.1 gets `T_svc = 20 ms`, approved by the owner on 2026-10-29. It also gets the rule that grades each moved path against `min(T_svc, family ceiling)` (plus a normative wait W where the path has one), and the resulting bound table: SRP/MRP 18 ms; ACMP and discovery-to-connection 20; AECP and notifications 20; MAAP and ADP 20; optional identification 15, not enabled. The three paragraphs that assumed 10 ms are rewritten. `T_ingress + T_svc + T_egress + T_network < timeout` is shown, with its margin, for each numeric response deadline. The NFR-SCOUT-03 row is updated. `docs/history` is not touched.
2. **Change the harness.** `T_SVC_MS = 20.0`. The grader's verdict uses `min(T_SVC_MS, CEILING_MS[family])`. `selftest.py` pins both values. New planted defects, at least: SRP graded against T_svc alone, which fails on an 18 to 20 ms SRP instance; and a stale 10 ms pin. Calibrated checks move to the new bounds. The oracle changes only through its generator, on the committed trace.
3. **Re-measure at the final head.** Every composed row at 100 MHz, at 1x1/1if and 8x8/2if, on both arms, with and without both drafts (lwSRP's receive path, the TSN stack's wire halves). Each row is graded against its own bound, and any row over it is bold. SPLIT_CONTROL_MEMORY section 13 and MAILBOX_SPLIT move to the approved budget.

Not in this round: the block-RAM ledger, the egress-held rows (tsn-c-stack #26), the drafts' repository reviews. No RTL changes.

Validation plan (round 8's gate set, at the final head, all rc 0):
- the firmware self-test (`--require-rv32 --self-test`, four shards) with every firmware mutant driver;
- `fw_coverage.py --check` and `fw_rv32_selftest.py --require-rv32`;
- S2's harness, its self-test, and the eight legs at both points and both arms;
- `test_builder.py --require-rv32` and `test_soc_options.py`;
- `gen_mailbox.py --check --crosscheck --selftest` and the publication census;
- the mailbox suite, `lint_rtl.py --check` and `xvlog_gate.py --check`;
- rtl-fast's `firmware-boundary` and `firmware-verilator`;
- the linked images, and the docs, idiom and bare-metal gates;
- `cd tests && behave`.

No full sweep is planned, because no RTL changes.

Blockers: none. STOP if any row the CPU decides misses its bound at either point with both drafts staged.

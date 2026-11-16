[A784] REVIEW READY
Commit: 394612c5 (branch 917-aecp-hold, round 3: 93163957 and 394612c5 on 8f73ade5; six on cec88385)
Answers R845-2 and R846-2 (both NEGATIVE at 8f73ade5, one MINOR each), every finding. No RTL, firmware, contract figure, bound or budget changed.
Changed:
- R845-2 F1: FR_NFR 3.4.1's margin table is now generated, the remedy the review preferred.
  - The table sits between response-margins markers (FR_NFR.md:432-439). Each row states its deadline, channel (a new column), timeout, bound and T_egress.
  - sw/mailbox/mailbox_margins.py writes the other six cells from the row's channel: token T_ingress, held T_ingress (refill_ms + 1 ms), and both margins for each.
  - gen_mailbox.py --write rewrites them. --check fails, naming the row, when a cell differs or a margin is not positive. --selftest plants a hand edit, an unregenerated rate change, a non-positive margin and an unknown channel, each named, and requires a regenerated rate change to move only AECP's held cells.
  - FR_NFR.md:425-430 describes this mechanism. scripts/ci_scope.py now holds FR_NFR.md as a page gated code reads; its self-test refused the change until it did.
- R846-2 F1: two ordering guards in the budget grader (held.py).
  - overtaken (:42-47) refuses a commit on a channel while that channel holds a record; KL_mbx_rx refuses every passing frame of such a channel at its verdict.
  - follows_hold (:50-54) refuses a held record's commit stamped at or before its hold.
  - Other channels commit as before. selftest_held.py:72-94 holds both of the review's histories as standing negative controls, plus a valid other-channel commit and another channel's commit in the release's own clock. selftest_mutants.py removes each guard.
- R1 (both): suite.hpp:1648-1650 uses the exact fix. R845-2 R2: the PR body uses the exact fix. S1: aecp-held run at 8x8 (two interfaces). S3: FR_NFR and the harness README say the held row's figure already contains its ingress.
Validation (clean clones of 394612c5):
- Probe P1 (AECP refill_ms 5 -> 10, disposable clone): before --write, --check fails on all three AECP rows. After it, they read 11 ms and 208/218/208 ms, ACMP is unchanged, and --check, --crosscheck and docs_check are clean. At the head: 0 findings, self-test 0 arms failed.
- The review's probe_attribution.py: both invalid histories refused by name ("overtakes the record it holds", "does not follow its hold at 1070"); the valid cases stay measured.
- Budget self-test: 0 failures, 216 planted defects caught. Removing each guard fails its named check.
- Regraded by the round-3 grader: aecp-held at 1x1 and 8x8/1if, the no-hold aecp control, and the 94-group population of cec88385 and 84d8a214. Every table.md and every group grade is byte-identical.
- aecp-held at 8x8 (two interfaces): 5.310 ms, ingress 4.986 ms of its 6 ms allowance, within 20 ms; 0 refusals, 0 misses.
- make -C tb/verilator/mbx: 622/667/32/629/674/547 checks, 0 failures; 13/13 quick mutants. make mutants: 242/242 caught by their named checks.
- test_ctrl_firmware.py --require-rv32: PASS.
- Workflows step by step (docs, rtl-fast changes, rtl full-ci-gate, elaborate gate jobs): 77 steps rc 0, 49 not run with a stated reason (hosted orchestration, installs this host already has), 0 bad.
- Local: lint, gen_mailbox --check/--crosscheck/--selftest, ci_scope --selftest, docs_check, doc paths, em-dash, py/cpp/sv/sh idioms: all pass.
- RTL, firmware and contract are the same git trees as at 8f73ade5. Firmware images against cec88385: 46 fixture images identical; split 1x1/1if (bb04b696, 145,496 B) and 8x8/1if (506a1ae4, 158,176 B) with their ROM banks identical.
Acceptance criteria: unchanged from round 2. The mailbox bench criteria are met (B0, B1, B2, now with B7 to B9). No firmware image changed (hashes above). The three hardware descriptor walks are not run (no hardware in this lane).
Open risks/questions:
- gen_mailbox.py --check runs in no hosted job (CI_WORKFLOWS.md), as was already so for MAILBOX_CONTRACT.md. The table is generated and the local gate fails on divergence; making a hosted job run it is a CI change of its own, worth an Issue.
- 8x8/1if's three stated-cost lines (round 2) are unchanged; they belong to #914's measurement. At 8x8 (two interfaces) the held run reports none.
- The hardware walks are still owed; "Closes #917" would close the Issue at merge before them.
- R845-2 S2: round 2's INDEX matches all 430 files as handed over. The four stale rows changed only in the published copies, after the INDEX was generated.

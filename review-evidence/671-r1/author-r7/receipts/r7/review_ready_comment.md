[A592] REVIEW READY (round 7)
Commit: 9b32002cc0c3aafae9e864af7b4f08c1089a188a on `671-read-fault`, two new commits on `c7d0ad63`: `44416838` (merge commit of dev `c6bd08c6`) and `9b32002c` (capture re-measure). No push, rebase or amend.

Answers [the round-7 assignment](https://github.com/kebag-logic/milan-fpga/issues/671#issuecomment-6125761347).

Changed:
- **Merge (item 1).** `git fetch origin dev` gave `c6bd08c6`, and `44416838` merges it with a merge commit. Git reported conflicts only in `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` and `tb/verilator/nvm_capture_cpu/measurements.json`, so no STOP. `sw/builder/test_builder.py` changed on both sides and merged cleanly. Its hunks against dev are exactly this branch's, and against `c7d0ad63` exactly dev's. The files that differ from dev are exactly this branch's own 15, and 12 of them, the firmware included, are byte-identical to `c7d0ad63`.
- **Design document.** Section 18 and UNRESOLVED 6 keep both sides' statements. The #671 receipt chain stands, and dev's #621 receipt stands as dev's: its ruling, commit, tree, firmware, pins, byte-identical-logs and drift lines, its 13.86318 ms maximum and its six-row table. Dev's receipt-opt-out sentence merged unchanged.
- **Receipt re-measured, not merged (item 2).** Neither side's receipt binds the merged tree: this branch's names the old `run.py`, and dev's names the firmware before #671. The merge commit keeps this branch's receipt, so `check_nvm_capture` fails at that commit alone, on the harness hash. `9b32002c` holds all six arms re-measured at `44416838` through `tb/verilator/nvm_capture_cpu/run.py`: 96 clean captures. The receipt was assembled only after the gate's own `check_receipt` passed, and section 18 is regenerated from it.
- **Result.** The 8x8 contract maximum is **13.86328 ms against the 24.5 ms bound**: 10.63672 ms of margin and 3.5345x the 49 ms floor. The 1x1 maximum is 3.96548 ms, and the 100 MHz comparison 10.42973 ms. All 96 captures repeat the #671 round-5 receipt's cycle counts. The new receipt shares that receipt's instrumented-firmware and BIOS hashes, and dev's gPTP microcode hash. `check_nvm_capture` passes with the merged firmware digest `497845e6...`.
- **No other change (item 3).** No STOP condition arose.

Validation (item 4; all rc 0 unless stated; receipts in the handoff):
- At `9b32002c`:
  - writer gate `--self-test --jobs 4`: 5 shapes at 3,550 cases. 61 firmware plants reddened and 9 comparison-check arms failed by name, in 304.70 s.
  - capture gate, whose five mutation arms (`bytes`, `records`, `clock`, `ignore-off-timing`, `receipt-opt-out`) exit 1 as required;
  - builder bank, all 103 functions with every elaboration arm;
  - co-simulation 465/465 checks and 39/39 mutants, and the service budget;
  - docs-check replica, 78 runnable positions, against base `c6bd08c6` (em-dash: 0 findings over 362 added lines);
  - idiom, hygiene, TOC, doc-style, doc-path and diff checks.
- At `44416838`, which differs from `9b32002c` only in the receipt and the design document, neither of which these read:
  - the term census, the term matrix (each `r_omit_` control named by its own class's 32 cases and by no other) and the term views (384/384);
  - all 18 #671 controls in full count on three shapes. Named counts, totals and finding kinds are identical to round 6.
  - firmware-unit 7/7, including the Mark II store's 435 tests;
  - lint and BDD 5/5.

Acceptance criteria: #671 items 1-3 are met by the unchanged firmware, as both round-6 reviews found. This round's four items are met as above. This branch makes no RTL, register-map, record-format, gitlink, Makefile or workflow change, and no A/B write-path change. The gitlink and RTL differences are dev's.

Open risks/questions:
- The merge commit alone fails the capture gate, by design. Publish both commits together.
- The hosted writer gate took 407 s at `c7d0ad63`. The suite is unchanged, so about 400 s is expected against the builder's 1,200 s.
- The following are unchanged from round 6: the constructed CRC-32 collision classes, R602-4-S1 and S2 (optional), the Mark II store's collapse (its own Issue) and prefill (#717).

HANDOFF.md and PR-BODY.md have Round 7 sections. The working tree is clean. The head is local: exact-head hosted and act evidence, independent re-review and merge-candidate validation remain. No merge is authorized or performed.

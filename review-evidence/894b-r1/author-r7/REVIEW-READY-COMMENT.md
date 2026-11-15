[A781] REVIEW READY
Commit: d539f162 (lane 894b, PR #914; round 7, three commits on round 6's af2c4d7a, where R844-3 is POSITIVE and R843-3 NEGATIVE on two MINORs)

Changed:
- **R843-3-F1 (d0fea5f0).** Section 13 states 8x8/1if's gate as measured on the head's image.
  - That is round 5's measurement of a15345f7's image, which the head carries byte-identical: 114 groups and 1,717 instances.
  - The rows: AECP 4.860, ACMP 7.231, ADP 6.014, MAAP 6.255, SRP 10.474, MRPDU 4.114 and the notices 2.168 ms; the first and last queued notice 2.812 and 26.636; the largest command 2.547.
  - Joins are 187.397 to 190.147 ms. The slices are 142,809, 138,906 and 92,744 cycles. THE RETRY's 2,453,084 rounds are none over their statement.
  - The load is 0.711 and 0.673 everywhere it is stated.
  - The every-source rows (R5 126.36, the last 325.90, txL 134.96 ms, the largest command's record 1,510 us) and the load with every command the largest (0.969) are as the head derives them, linked to their receipt.
  - Round 3's figures stay as labelled history. FR_NFR 3.4.1 cites the gate.
  - d539f162 gives that receipt link its archive commit's short ID.
- **R843-3-F2 (d2fd8975).** record_classes.py holds a pass complete at every point it runs any leg at, as #902's 647d5c4a held 1x1/1if.
  - A point with legs and no arm A leg is refused by name. An 8x8/1if-only pass still runs.
  - R843-3's mixed-point probe input now gives the two findings 647d5c4a gives: "the pass runs no arm A leg at 1x1/1if" and the missing arm B SET_CONFIGURATION at 1x1/1if.
  - It is a planted control (14 of 14), and on af2c4d7a's rule it escapes.
- **Residue, with the reports' exact fixes:**
  - R843-3-R1 and R844-3-R2, together: MAILBOX_SPLIT.md's slice is "stated for each shape (THE SHAPES): the slice rule's choice at 1x1/1if, 0.95 ms, 1.475 ms at 8x8/1if, and 1.3 ms at two interfaces".
  - R843-3-R2: FR_NFR's ledger citation is linked.
  - R844-3-R1: record_classes.py's point_name says "#894's 8x8/1if shape".
  - R844-3-R3: section 13's round-3 load record and reported rows are labelled, with the current receipt linked.
  - R844-3-R4: the PR body's survey bullet reads "every measurement within its statement".
  - R843-3-S1 is not taken: section 13 states it, it is the stricter apply check, and the survey holds it (316.40 us measured, 335 by the rule, against 345). S2 stays retained.

Validation (a clean clone of the head; receipts and their index in the round 7 packet):
- **Images.** All eight at d539f162 are byte-identical by ELF and loadable sha256 to af2c4d7a's. There is no firmware or image change, so no sweep.
- **Lane gates of what changed (part r):** 45 as required, the four by design `_exits_1`, and the clone clean after.
  - The comment scans (over the whole delta, and over af2c4d7a..d539f162) and R844-1's audit find 0 lines.
  - py idiom and docs_check pass.
  - The harness self-test has 0 failures. Its PASS lines are round 6's plus the new control.
  - load 28 of 28 and --check pass, the record classes 14 of 14, and the shape-cost, ledger, flip and rows gates.
- **The docs workflow's jobs** (docs-gates-0, 1 and 2, wire-accountability, docs-check-no-git, docs-check): 61 steps run rc 0, 34 not run with a stated reason, 0 bad.
- **The probe and the measurement.**
  - R843-3's probe through a gate: PASS at the head, exit 1 on af2c4d7a's module.
  - 8x8/1if's measurement legs graded by the changed module: PASS, identical to round 5's receipt.
- **F1's figures.** Each of the 36 figures section 13 now states for 8x8/1if's gate, load and every-source rows equals its receipt, and 0.671 and 154,850 stand only as round 3's. The same check finds 37 of its 38 lines bad on af2c4d7a's section 13.

Acceptance criteria (the manager's round 7, items 1 to 4): met as above, and the PR body's finding-by-finding table records each finding.

Open risks/questions:
- R843-3's re-review of d539f162 is due, on Conformance, Docs, Tests and Robustness. No firmware changed.
- #902's heads since 4ae887a1 are not merged here: 26898c05, 41ca9f87 and 07ed787e, where 894-tiers now is. They are comments, docstrings and documents, and a merge conflicts in FR_NFR.md and aecp_mbx.h's comments, so the next sync takes them.
- The rows by every source at 8x8/1if stay reported, owed to #872. valid-destinations is #895's arm. Mailbox.ARoundFillsWhatItsPassHasLeft at 8x8/1if, and 1x1/1if's SRP record figure, stay for new Issues.

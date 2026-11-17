[A781] REVIEW READY
Commit: e1ecce20 (lane 894b, PR #914; round 14, two commits on round 13's d0a2a160, answering R843-6 and R844-5; under the owner's batch rule the last delta before #914 freezes)

Changed:
- **FR_NFR 3.4.1's 8x8/1if hold-off (R843-6-F1; 60389719).** The report's text: 2,027 cs at 8x8/1if, whose `CTRL_LOOP_TX_MS` is its own tx row's 74.26 ms rounded up, 75 ms, held to that row by `flip_grade.py --check` (`tx_held`). The 2,026 cs at 70 ms is marked historical. A sweep of the tree for 69.84, 2,026, 2026 cs, `li a3,2026` and 70 ms beside 8x8/1if or THE TRANSMIT finds every remaining occurrence historical, a plant or refusal, or unrelated. Section 13's composed-image immediate now names its image.
- **`--check` held to calling `tx_held` (R843-6-S1; e1ecce20).**
  - The new flip control `CHECK_HELD_CONTROL` runs `main` as `--check --point 8x8/1if` does. It plants 8x8/1if's figure at 70 ms only in the text `tx_held` reads, and requires exit 1 naming the figure. The flip self-test now has 616 controls.
  - The new harness mutant `flip: --check does not call tx_held, ...` runs `main` with `tx_held` finding nothing for its duration. Under it the three earlier controls stay refused, and only the new control's check fails, by name. The harness now has 260 mutants.
  - `--check`'s wiring is unchanged.
- **The wording residues, by their exact fixes:**
  - `flip_grade.py`'s comment on the planted figures (R843-6-R1);
  - `srp_mbx.c`'s guard, on the same two lines (R2);
  - `srp_talker.cpp:53`'s hold-off, with 8x8/1if's 20,270 ms (R3);
  - section 13's refusal sentence (R4);
  - the PR body's status, base `dev-soft-core` and fetch prerequisite (R843-6-R5, R844-5-R1).

Validation, on fresh clean clones of e1ecce20:
- **Images:** all eight are byte-identical to d0a2a160's, by ELF and loadable sha256, both 8x8/1if images among them.
- **The flip gate:** `--check` passes at 1x1/1if and at 8x8/1if, with its HELD line; `--selftest` refuses 616 of 616. 8x8/2if's check exits 1, by design.
- **The new mutant, by name:** caught by `the flip check refuses --check --point 8x8/1if with 8x8/1if's CTRL_LOOP_TX_MS planted at 70 ms` alone.
- **The harness self-test:** 932 checks pass and 260 mutants are caught, 0 failures.
- **Quick checks:** 22 rc 0, and 8x8/2if's flip check rc 1 by design. They cover the graders' checks and self-tests, docs_check, the Python and C++ idiom gates, the comment scans over round 14's delta and R844-1's audit (0 lines), and the diff checks.
- **The docs jobs** (`docs.yml`, six jobs): 61 steps rc 0, 34 not run with a stated reason, 0 bad.
- **Not re-run, by the round's brief:** campaigns and legs. Round 14 changes no firmware byte; round 13's results at d0a2a160 stand.

Acceptance criteria:
- **#930: met, as ruled; unchanged.** The PR body closes #930.
- **R843-6-F1, S1 and R1 to R5, and R844-5-R1:** answered as above; each disposition is in the PR body.

Open risks/questions:
- **`twin` and `twin-plants`** fail on the base's `split-talker-failed` row until PR #935 lands.
- **The every-source rows at 8x8/1if** stay owed to #872, as ruled: R4 21.39 ms against 20, and tx 74.26 against the MRPDU's 49 ms.
- **The timing floor** is #818's. No route ran.
- **Reviews:** R843-6 was NEGATIVE and R844-5 POSITIVE at d0a2a160, so a re-review of this head is owed.

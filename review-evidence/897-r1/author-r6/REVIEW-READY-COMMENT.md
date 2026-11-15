[A776] REVIEW READY
Commit: `b15da60a` (round 6, on round 5's `eca1b9ca`, #902's round-13 head `234bc149`; it answers R833-5's NEGATIVE at `eca1b9ca`)

Round 6, the manager's assignment on R833-5 (PR #898). No firmware and no RTL change. Not pushed.

Changed:
- `b15da60a` (`record_classes.py`, `selftest_mutants.py`, the harness README, section 13):
  - **F1, the guard holds the answered read.** Each record carries its response's control_data_length, read from the frame `read_leg` already parses. A pass is refused unless its answering-ports leg at 1x1/1if answered a GET_AS_PATH SUCCESS at 80 (16 B, and 8 B for each of `arm_path.ENTRIES`, IEEE 1722.1-2021 7.4.41.2). Every GET_AS_PATH that arm answers SUCCESS at another length is refused by name.
  - **The planted control.** "a GET_AS_PATH answered SUCCESS with no entries" is refused.
  - **The port is pinned.** `port_findings()` requires `build.VARIANTS['answering-ports']` to carry `arm_path.B_PATH` as the face's `path` port, reading the count and each entry through the window. It is a harness self-test check and fails `record_classes.py --selftest`. A mutant restoring the earlier port, "build: arm B's path port answers no entries at once, reading no window (earlier rule)", is caught by it.
  - **RES1-RES3**, with R833-5's exact wording; and section 13's statement of what the guard refuses.
- **F2.** Round 6's receipts list every AECP record of the head's legs and the measurement legs, with each GET_AS_PATH response frame decoded. No source change.
- **RES5.** Round 5's REVIEW READY (issuecomment-6894799910) is edited in place, that phrase only: "as built at 1x1/1if R4 and last (the first queued notice at its 20 ms bound)".
- **RES4.** The PR body names R833-5.

Validation:
- **F1 on real legs at this head** (the same figures on `eca1b9ca`'s legs, whose images are this head's):
  - arm B's GET_AS_PATH is SUCCESS at control_data_length 80: 16,208 cycles at 1x1/1if, 16,397 and 15,966 at 8x8/2if;
  - arm A's refused responses are at 16;
  - `record_classes.py` over every one-interface leg and the 8x8 legs: RESULT PASS.
- **The stub on a real leg.** A scratch arm-B leg built with the earlier port (never committed) answers SUCCESS at 16, 10,019 cycles. Beside every leg it is refused: "a GET_AS_PATH answered SUCCESS with control_data_length 16, not the 80 of the 8 entries the arm's path port reads and answers". In place of arm B's leg, "the pass is missing arm B's GET_AS_PATH ... with its 8 entries (control_data_length 80)" refuses it as well.
- **F2's figures as receipted:**

  | Figure | Receipt line |
  |---|---|
  | 1x1/1if arm B | `16,208 cycles 175 us command GET_AS_PATH status 0 control_data_length 80`; the response `count 8, control_data_length 80 (16 + 8 x 8 = 80), frame 106 B`, its eight ClockIdentities |
  | 1x1/1if arm A | `10,948 cycles 115 us ... status 10 control_data_length 16`, `count 0` |
  | 8x8/2if interface 1 | `15,966 cycles 170 us ... status 0 control_data_length 80`, the response on port 1, `count 8` |

- **One pass at `b15da60a`**, each part on its own fresh clean clone:

  - **Docs workflow:** every job and `run:` step. 61 ran, 34 not run with a stated reason, 0 bad.
  - **Lane gates:** 24 gates. 20 at 0, and the 4 that exit 1 by design, each output byte-identical to `eca1b9ca`'s.
    - the harness self-test: 0 failures, 250 of 250 mutants, the new one caught by the port check;
    - `record_classes.py --selftest`: 14 of 14 and the port check;
    - `rows_tiers`; `load_grade` and `flip_grade`, self-tests and checks; `tier_grid` (950 us);
    - `plat_ledger`, the fixtures and `test_ctrl_memory`;
    - `docs_check` 0 findings, the em-dash gate against `cec88385` and `234bc149`, both idiom ratchets.
  - **R833-5's probe (`probe_stub_path.sh`) at this head:** refused by name in both suites. `run.py --self-test` FAILs "the answering-ports arm's path port is arm_path.py's, which reads the window", and `record_classes.py --selftest` exits 1 on the same finding. `build.py` is restored.
  - **Harness legs, one a point and arm:** every leg exits 0. `record_classes.py` at this head over them and round 5's one-interface legs: RESULT PASS.
  - **Images:** all 14 byte-identical to `eca1b9ca`'s (the six harness arms, and the size fixture and the platform at the four points). So round 5's full pass at `eca1b9ca` (workflows, campaigns, the 65-suite sweep) stands for every image.

Acceptance criteria (the round-6 assignment):
- **Item 1 (F1) met.** The guard holds the answered 8-entry read by its control_data_length. A SUCCESS with no entries fails by name, as a planted control and on a real leg. `record_classes.py --selftest` and `run.py --self-test` pass at the head, and R833-5's probe fails by name there.
- **Item 2 (F2) met.** Every focus figure is in a published, indexed receipt.
- **Item 3 met.** RES1-RES3 use the exact fixes, RES4 is in the PR body, and RES5 is edited in place.
- **Item 4 met** (above).

Open risks/questions:
- **#902 moved again**, to `41ca9f87` (11 commits past `234bc149`: docs and comments, `CTRL_LOOP_TX_MS` at two interfaces, `aecp_mbx.h`'s comment). This branch stays on `234bc149`. A scratch trial merge into `b15da60a`, never committed, conflicts in `SPLIT_CONTROL_MEMORY.md` and FR_NFR 3.4.1, both docs. #902's text states the paced class at 300 us; this branch restates it at 305 at 1x1/1if.
- **Carried from round 5:**
  - the 8x8/2if datapath event costs over their statement (reported, not held);
  - one AVB_INTERFACE an image at two interfaces (raised for a decision);
  - the composed #901 + #898 image against 133,120 B (ruling item 3);
  - the 64-entry path's control_data_length.

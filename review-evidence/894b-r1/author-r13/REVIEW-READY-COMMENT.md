[A781] REVIEW READY
Commit: d0a2a160 (lane 894b, PR #914; round 13, three commits on round 12's 8883d499, answering R843-5 and R844-4; under the freeze rule #914's last change)

Changed:
- **THE TRANSMIT's figure at 8x8/1if is held in the tree (R843-5-F1, option (a); a840c14d).** `rows_grade` holds 8x8/1if's own entry, and each point's polls and notices are read at its own shape, so the tree derives 8x8/1if's tx row itself: 74.26 ms. `flip_grade.py --check` runs `rows_tiers.tx_statements` at 8x8/1if through `tx_held`. That check is separate from 8x8/1if's reported rows; the point's other grading is unchanged. The self-test plants the figure at 60, 69 and 74 ms, and each is refused by name: 615 controls, from 612.
- **`CTRL_LOOP_TX_MS` 75 ms at 8x8/1if (R844-4-F1; 32a9242f)**, its tx row rounded up. The withdrawn Talker's hold-off there is 2,027 cs, from 2,026. That keeps IEEE 802.1Q-2018 35.2.2.8's two LeaveAllTime periods after the Leave's latest departure: 20,005.74 ms remain. `ctrl_loop.h`, `srp_mbx.c`'s comment and the SRP README name the guard.
- **Each figure stated with its image or derivation (R844-4-F2; d0a2a160).** Section 13, MAILBOX_SPLIT (1x1/1if's slice 0.9 ms) and FR_NFR 3.4.1 (R843-4-R1's exact fix, R843-5's wording). It also takes `load_grade.py`'s header (R843-5-R1) and the harness README. The packet index names its round (R843-5-R2).

Validation:
- **Images**, on a clean clone of d0a2a160:
  - the six images at 1x1/1if, 1x1/2if and 8x8/2if are byte-identical to 8883d499's, by ELF and loadable sha256;
  - each 8x8/1if image differs in one instruction, `li a3,2026` to `li a3,2027`, with every other byte of every section the same.
- **The 8x8/1if legs on that image** ran on a clean clone of 32a9242f, whose images are d0a2a160's:
  - `srp-talker-held`, `srp-talker` and `srp-talker-loss` and the `transmit-aged` control each exit 0 with no STATED line;
  - every group's simulation log is byte-identical to round 10's on 46cf2a7d's image;
  - the gate holds every measured row within its bound, and its only findings are the seven held-egress ledger rows, which these groups do not measure;
  - the control is caught in 8 of 8 groups.
- **The reviewers' probes** at d0a2a160:
  - R844-4's `transmit_contract_probe.py`: `tx_statements` empty, `MODEL ENVELOPE CHECK: PASS`;
  - R843-5's `tx_plant_probe.sh` (its plant pointed at the head's 75u): 60 ms refused by name at 8x8/1if, and 70 ms too;
  - the three new controls refused by name.
- **Quick checks**, 20 rc 0, and 8x8/2if's flip check rc 1 by design:
  - the shape table and the flip self-test, 615 refused;
  - the flip check at 1x1/1if and at 8x8/1if, with its HELD line;
  - rows_tiers (1,033), the load gate (28 refused, and `--check`), the record classes (14), the mixed-point probe, the ledger's 15 mutants;
  - docs_check and the idiom gates;
  - the comment scans and R844-1's audit, 0 lines;
  - the diff checks.

  Every grader's output matches 8883d499's but the figure, the HELD line, the control count and the header.
- **The harness self-test** (`run.py --self-test`): 931 checks pass and 259 mutants are caught, 0 failures.
- **The docs jobs** (`docs.yml`, six jobs): 61 steps rc 0, 34 not run with a stated reason, 0 bad.
- **The SRP campaign** (`firmware-srp-mutants`): 436 caught, 0 escaped, the Talker hold-off plants among them.
- **The firmware suites and coverage** (`firmware-unit`) pass. The arms include `srp_talker.cpp` at 1x1/1if and 8x8/2if and `srp_listeners.cpp` at 8x8/1if; coverage covers 39 files, `srp_mbx.c` 746 of 746 lines.
- **Not re-run:** the control and AECP campaigns, the boundary and simulation jobs, the shards and the lane gates; the PR body says why.

Acceptance criteria:
- **#930: met, as the ruling on round 10's STOP confirms; unchanged by this round.** The PR body closes #930.
- **R843-5-F1, R844-4-F1 and F2, R843-5-R1 and R2, R843-4-R1:** answered as above; each disposition is in the PR body.

Open risks/questions:
- **`twin` and `twin-plants`** fail on the base's `split-talker-failed` row until PR #935 lands.
- **The every-source rows at 8x8/1if** stay owed to #872, as ruled: R4 21.39 ms against 20, and tx 74.26 against the MRPDU's 49 ms. Only THE TRANSMIT's figure is held there.
- **The timing floor** is #818's: +0.030 ns setup and 0 ns hold, on the best of the three directives. No route ran.
- **Reviews:** R843-5 and R844-4 were NEGATIVE at 8883d499, so a re-review of this head is owed.

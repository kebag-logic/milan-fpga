[A825] REVIEW READY: round 11 of #977, milan-fpga `pf-977-1` at `3181a3ec372b6473175cc1c842ada8133a96b127` (round 11b). tsn-c-stack is at `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` and lwSRP at `main` `e27b34c9231abaa862bdb73f807238b330aa4c51`, both unchanged. Nothing is pushed or posted.

This round answers both re-reviews of round 10d: PR #993 comments 7226275798 (internal R957-2) and 7226304210 (external R958-2). For R957-2-F1 the manager decided option (a). The 8x8/1if load ceiling of 0.78 is behind the owner's answer. It is one droppable commit, `9976b94f`. The only commit after it, `3181a3ec`, touches none of its files, so `git revert 9976b94f` alone still drops it.

**1. What changed** (8 commits past `25ff0632`)

| Finding | Commit | Fix |
|---|---|---|
| R957-2-F1 MAJOR | `71503e5a` | A sourced load term, `deliveries`: the binding changes and loss completions a registering record defers, V a record at the registration rate. It is costed by the rule against the median ordinary pass's base: 125 us at 8x8/1if and 190 us at 1x1/1if, with the dearest-before figures 80 and 130 us recorded beside it. The premise is stated in `load_grade.py`'s header and the design document's load section, with four planted controls, each refused (the term left out, at half its rate, at no cost, under its dearest-before figure). |
| Ceiling (manager's instruction) | `e8618e0c` + `9976b94f` (droppable) | 8x8/1if flip ceiling 0.78, owner decision pending, with a control that 0.780 passes and 0.781 fails. The first form, `9dd2c076`, carried a review label in a comment, so it is restored to 0.77 and made again cleanly. |
| R957-2-S1 | `bdf8c0cc` | D8 (the loss turn), D9 (both owed after a loss: the change goes first) and D10 (a record's pass takes no turn). Four planted defects, each caught at its shapes. |
| R958-2-F1 MINOR | `0acbb717` | `SPLIT_CONTROL_MEMORY.md:172`: the platform's refusal thresholds are 65.5 and 61.5, as the executable boundary cases hold them. |
| R957-2-R1, R958-2-R1 | `8ffdea83` | Every #977 citation of 2026-11-27 names its ruling ("on the delivery bound", "on the population bound"). The B25, B26 and B27 comment prefixes are removed. |
| R957-2-R2, R958-2-R3 | `8ffdea83` | The 79.49 ms row (79.48 at the ruling's 415 us SETTLE) and a link to the owner's approval of 80 ms, in `ctrl_loop.h`, `FR_NFR.md` and the design document. |
| R957-2-R3, R958-2-R2, R958-2-R3 (packet and PR body) | `PR-BODY.md`; `round10/receipts/INDEX.md` | Run counts: 285 exit 0, plus 4 single kept/bound runs refused for pairing that pass as the 2 pairs. The lwSRP Pins row now reads "used by the default-option shapes; the published ELF comparisons cover those images too". The reviewers are named. A dated supersession note is appended to round 10's index, whose other bytes are kept. |
| R958-2-S1 | `71503e5a` | The design document explains why the load counts no pass's base while the rows charge it: base 300 instead of 350 us gives the tx row 77.89 instead of 79.49 ms and leaves the load unchanged. |
| Builder step 43 (round 11b) | `3181a3ec` | The merge-train candidate failed the whitespace gate (`git diff --check`) on `srp_binding.hpp`'s blank line at EOF. The line is removed. `git diff --check` over the whole PR delta now reports no hit, against both the merge base `71bad8c0` and the dev-soft-core tip `0b594023` that the builder uses. That line was the only hit. |

**2. Results**

| Item | Result |
|---|---|
| Every product ELF against `25ff0632`'s | **80 of 80 byte-identical** at `9976b94f` and again at `3181a3ec` (plat_ledger's platform images and the harness's 72). Round 10d's measurement (578 runs + 4 pairs) and both routes stand. No arm was re-run. |
| 8x8/1if load at the pin | **0.77864** with the deliveries term (0.76614 without it, 0.77414 at the dearest-before cost), within 0.78 and over 0.77. Without `9976b94f`, `flip_grade --check --point 8x8/1if` fails. |
| 1x1/1if load | 0.5321 at the pin (0.5290 graded), against 0.70 |
| `load_grade --check` / `--selftest` | PASS / 32 of 32 |
| `flip_grade --check`, both points / `--selftest` | PASS, PASS / 628 of 628 |
| New plants | `deliver-loss-turn-from-the-first`, `deliver-loss-turn-never-advanced` and `deliver-loss-always-first` caught at 1x1/2if. `srp-977-deliver-loss-in-a-records-pass` caught at 1x1/1if and 8x8/1if. 448 SRP defects, each at one site. |
| Composition suites mbx1, mbx2, mbx8 | PASS |
| Firmware gate, 4 shards with `--self-test` (`9976b94f`) | PASS |
| `fw_coverage --check`, `test_ctrl_memory`, `plat_ledger --self-test`, `ctrl_hot` both, twin (`9976b94f`) | PASS |
| Harness self-tests, Python and C++ idiom gates (`9976b94f`) | PASS: `run.py --self-test` 0 failures, `load_grade` 32/32, `flip_grade` 628/628, `shape_costs` 25/25, `kept_grade` 33; idiom gates PASS |
| Docs workflow (`9976b94f`) | 100 of 100 steps |
| The manager's builder, all 49 steps (`manager-builder.json`), in a clean clone at `3181a3ec` | Every step exits 0. Step 43 (`git diff --check`) is clean. Step 32, the xvlog gate, PASSes, run through vivado-slot.sh. Step 47 reports "ALL GATES PASS EXCEPT 1 NOT RUN", as the manager's run of the candidate did: gate 11 needs a calibration build report that is not on disk. Steps 32 and 47 ran again under the real HOME, because a scratch HOME hid xvlog and litex. |

**3. Open for the owner and the reviewers**

- **The 8x8/1if load ceiling, 0.77 to 0.78.** The manager is asking the owner. If it is refused, revert `9976b94f`, and 8x8/1if waits for #1025's margin recovery.
- **The deliveries term's baseline.** It is the manager's choice, the median ordinary pass's base. Against the dearest base before each record the 8x8/1if load would be 0.774.

The receipts are under `receipts/`, indexed in `receipts/INDEX.md`.

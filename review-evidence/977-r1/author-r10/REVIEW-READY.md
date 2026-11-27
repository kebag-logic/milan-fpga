[A825] REVIEW READY: round 10d of #977, milan-fpga `pf-977-1` at `25ff0632c4ed312d57cad78783474308c92dd21f`. The tsn-c-stack pin is `main` `5a07d9b7d87298f04b15aa28f0304ec88b0aef81` and the lwSRP pin `main` `e27b34c9231abaa862bdb73f807238b330aa4c51`, both unchanged in this round. Nothing is pushed or posted.

This round implements [the ruling on round 10c's STOP](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7216582862). Item 5 is the owner's question. It is one droppable commit, `70468e2a`, and `git revert 70468e2a` applies cleanly at the head.

**1. What changed** (15 commits past `e62e1936`; detail in `PR-BODY.md`)

| Item | Commits | What |
|---|---|---|
| 1, pass alone | `d8e12c16`, `25824442`, `25ff0632` | `CTRL_LOOP_ALONE_US` per shape, by the rule over every group of every arm, at most 1,935 us. It is 1,840 us at 8x8/1if (171,622 cycles measured) and 925 us at 1x1/1if (87,826, under its 950 us slice). A pass of one SRP record is held to max(slice, pass alone), and every row opens on that figure. |
| 2, base | `7e7f59af` | 8x8/1if polls base 350 us, walk 150 us. |
| 3, SETTLE term | `d8e12c16`, `25824442` | One a row: 105 us at 1x1/1if. At 8x8/1if it is 425 us, the ruling's 415 restated by the rule for the 40,049 cycles measured, which puts the tx row at 79.49 ms. |
| 4, no binding change in a record's pass | `55bd7f41`, `e59cf6ea` | The guard in `deliver`'s bind loop (`settles`). D6 holds it per shape, its plant runs in the one-interface campaigns, and the new group is `srp-register-both-owed`. |
| 5, THE TRANSMIT 80 ms | `70468e2a` (droppable) | 77 and 80 ms builds: 80 of 80 product ELFs byte-identical, including the 8x8/1if platform image. The hold-off stays 8 cs. |
| Restatements | `25824442` | `REGISTRATION_US` 185 us (1x1/1if) and 190 us (8x8/1if) by the rule over every registering group. |
| Relearn | `c63e9d58` | Four windows, 290 entries, the same five dropped, 72 of 72 maps clean. |
| Ledger | `4352900b`, `4e595c85` | The platform's 8x8/1if image needs 147,712 B of `rom`, 256 B past 60.5. Its entry is 61.0 by the owner's rule of 2026-11-15, as ROM debt owed to the hybrid XIP lane's issue. **This is a ledger move a reviewer should confirm.** |
| Gate fixes | `2e466ae9`, `8c30e241`, `8765bfd5`, `dfda4df4` | Five SRP plants whose lines round 10c's delivery bound rewrote are re-pointed, and the withdrawal plant compiles again. D7 covers e62e1936's untested `bind = n` line, which coverage found, and comes with its plant. |

**2. Results**

| Item | Result |
|---|---|
| Every group of every arm, both points (`e59cf6ea`'s images; the head's 80 ELFs byte-identical to them) | 578 runs + 4 srp-kept/srp-bound pairs, all exit 0 (the single kept/bound runs refused only for kept_grade's pairing). 0 stated misses. |
| Longest pass (STOP at 2 ms) | 1.557 ms at 1x1/1if, and 1.930 ms at 8x8/1if (the JoinIn of both kinds, 193,036 cycles, 3.5 % under THE SHARE) |
| THE TRANSMIT's row at 8x8/1if (STOP at 80 ms) | 79.49 ms (79.48 at the ruling's 415 us SETTLE) |
| Loads | 1x1/1if 0.524 (0.70); 8x8/1if 0.766 (0.77) |
| 1x1/1if rows | ACMP 29.51 (30), txL 48.08 (49), last notice 133.91 (135): all held |
| Post-swap delivering passes at the registration rate (the reviewer question) | +0.0019 over the dearest base before the record; **+0.0136 over the median base, which would put the 8x8/1if load at about 0.780**. Not a load term today. |
| Routes | 1x1/1if: WNS +0.159 / WHS +0.036 ns, 0 routing errors, 82 BRAM. 8x8/1if: WNS +0.092 / WHS +0.036 ns, 0 routing errors, 100.5 BRAM. The images are the head's, byte for byte. |
| Firmware gate, 4 shards with `--self-test` (`25ff0632`) | PASS |
| `fw_coverage.py --check`, `test_ctrl_memory.py`, `plat_ledger.py` and `--self-test`, `ctrl_hot.py` both, the twin (`25ff0632`) | PASS |
| Harness self-tests (`25ff0632`) | PASS: `run.py --self-test` 0 failures, `load_grade` 28/28, `flip_grade` 628/628, `shape_costs` 25/25, `kept_grade` 33 |
| Docs workflow (`25ff0632`) | 100 of 100 steps |

**3. Open for the owner and the reviewers**

- **Item 5**, the owner's answer. If it is refused, revert `70468e2a`, and 8x8/1if waits for #1025.
- **The post-swap delivering passes:** is a pass's binding change a load term at the registration rate?
- **The 8x8/1if platform ledger at 61.0** under the owner's rule of 2026-11-15.

The receipts are under `receipts/r10d/`, indexed in `receipts/INDEX.md`.

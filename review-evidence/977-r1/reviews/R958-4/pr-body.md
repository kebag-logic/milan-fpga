Register Talkers at the MRP state machines' rate within THE SHARE (#977)

[A825]

## Contents

- **[Status](#status)**: round 12 of #977. The deferred deliveries are costed against the ordinary passes after the delivery window, the 8x8/1if ceiling of 0.79 sits behind the owner's answer, and both reviews' findings and residues are fixed.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, the executor and the independent reviewers.
- **[Description](#description)**: what changed and why.
- **[Authoritative references](#authoritative-references)**: requirement and specification clauses, and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout and dependency commands.
- **[How to validate](#how-to-validate)**: the exact commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this does not do, and why.
- **[Definition of Done](#definition-of-done)**: the merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**Ready for review at `3256d1d2`, with the 8x8/1if load ceiling of 0.79 behind the owner's answer.** This round answers both re-reviews of round 11, [the internal review](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7229653191) and [the external review](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7229617575), and follows [the manager's decision on #977](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7229657853).

- **internal review F1, the baseline.** The deliveries term is now costed against the ordinary passes after the delivery window, the decision's accepted baseline, by the rule, over both arms at both points.
  - The window is the delivery bound's own: the record's pass and the 2 x n_sinks deliveries after it. The baseline is the median polls base of the ordinary passes in the 50 ms after the window, since those passes carry none of the deferred work.
  - The cost is 160 us at 8x8/1if (the answering-ports arm's swap, 15,104 cycles a sink) and 200 us at 1x1/1if (18,778 cycles a sink).
  - The 50 ms and 500 ms pre-record medians are recorded beside it, not graded: 125 and 145 us at 8x8/1if, 190 and 200 us at 1x1/1if.
  - The measured figure is the gate's floor (`DELIVERY_MEASURED`), and a control refuses a lower one.
- **The 8x8/1if load** at the pin is 0.78214 with the term (0.76614 without it), at least the 0.7806 the reviewer derived. It is under 0.79 and over the owner's 0.77.
  - So the 0.78 raise is reverted (`feefd047`) and replaced by one droppable commit, `3256d1d2`, which raises the ceiling to 0.79 and cites "owner decision pending". Its control holds 0.790 within the ceiling and 0.791 over it.
  - Without it the 8x8/1if flip check fails. If the owner refuses, 8x8/1if waits for #1025.
- **external review F1, the adapters.** `flip_grade.flip_checks()` and `load_grade.ceiling_checks()` now report every failed control. The control names are built from the ruled figures, so `controls()` and `CONTROLS` cannot drift, and either adapter fails an escape it does not name. The focused mutation (8x8/2if at 0.71) fails through both paths.
- **1x1/1if** is 0.53254 against 0.70.
- **No product byte moves.** Every product ELF at the head is byte-identical to `25ff0632`'s, 80 of 80 (`receipts/elf-identity-3256d1d2.txt`), so round 10d's measurement and both routes stand.

`pf-977-1` -> `dev-soft-core`. Both dependencies are pinned at their PRs' merge commits:

- **lwSRP** at `main` `e27b34c9`, the squash merge of [lwSRP PR #22](https://github.com/kebag-logic/lwSRP/pull/22).
- **tsn-c-stack** at `main` `5a07d9b7`, the merge of [tsn-c-stack PR #41](https://github.com/kebag-logic/tsn-c-stack/pull/41).

## Linked Issue / roles

Closes #977
Relates to #665, #969, #1023, #1025

Executor: `[A825]`
Internal cleared-context reviewer: `[R957]`
External reviewer: `[R958]`

## Description

Round 12 follows both re-reviews of round 11 and the manager's decision on #977 (comment 7229657853). Rounds 11, 10d and 10 are in the tables after this one.

| Piece | What and why |
|---|---|
| The ceiling held at 0.77 again (`feefd047`) | Reverts round 11's 0.78 raise, so the owner is asked for one figure, 0.79. |
| The adapters (`0a71ca6b`) | external review F1. `RULED_FLIP` and `EDGE_1IF` state the ruled ceilings and the edge loads. The ceilings control and the edge control are named from them, in `controls()` and in `CONTROLS` alike. `flip_checks()` and `load_grade.ceiling_checks()` each add a failing check for any escape they do not name. `selftest_mutants.py` plants 8x8/2if at 0.71 and an unnamed escape, and `flip_grade --selftest` refuses 628 of 628. |
| The deliveries baseline (`ddf5c568`) | internal review F1 and the decision's item 2. `DELIVERY_US` is 160 us at 8x8/1if and 200 us at 1x1/1if. That is the dearest record over every registering group of both arms on images byte-identical to the head's, by the rule, against the median polls base of the ordinary passes in the 50 ms after the delivery window. At 8x8/1if the answering-ports swap is 135,935 cycles over its after-median of 12,089, 15,104 a sink. At 1x1/1if the answering-ports JoinIn of both kinds with a change owed is 18,778 a sink. `DELIVERY_MEASURED` holds those cycles, and `delivery_findings` refuses a `DELIVERY_US` under their figure by the rule (the control "the deliveries cost stated under its measurement by the rule"). `DELIVERY_BESIDE` records the 50 ms and 500 ms pre-record medians' figures. The window and the reason are stated in `load_grade.py` and in the design document's section 13, which links the decision. Also: internal review R1 (the comment describes the method rather than naming a tool), internal review R2 (the README's pass-cost sentence names the `deliveries` exception), and S1 (`srp_deliver_mutants.py` says the unprefixed plants run in the two-interface campaign). |
| The 0.79 ceiling (`3256d1d2`, droppable) | The 8x8/1if flip ceiling is 0.79, owner decision pending. The manager amends the citation when the owner answers, and the PR does not merge with "pending". The control holds 0.790 within it and 0.791 over, and `flip_grade --selftest` refuses 628 of 628. `FR_NFR.md` and the design document follow. It is the last commit, so `git revert 3256d1d2` alone drops it. |

### Round 11 (`71503e5a` to `3181a3ec`)

| Piece | What and why |
|---|---|
| The deliveries term (`71503e5a`) | internal review F1, option (a). The term is `load_grade.deliveries`: DELIVERY_US x V x 3 / (1.5 x 180 ms), at 1x1/1if and 8x8/1if. DELIVERY_US is measured over every registering group of both arms, on images byte-identical to the head's. For each record, the window is the delivery bound's own: the record's pass and the 2 x n_sinks deliveries after it. Its polls base over the median ordinary pass's in the 50 ms before the record is summed, and divided by the sinks (superseded in round 12 by the after-window baseline). The dearest record, by the rule, gives 125 us at 8x8/1if (the answering-ports arm's swap, 104,157 cycles over its median 14,942) and 190 us at 1x1/1if (18,076 cycles a sink). `DELIVERY_US_DEAREST` (80, 130 us) reports the dearest-before baseline. `load_grade.py`'s premise, its term list and the design document's load section (premise and term table) state the change. `load_deliveries.py` holds the four controls, and `load_grade --selftest` refuses 32 of 32. The design document also explains why the load counts no pass's base while the rows charge it: the 8x8/1if base at 300 us instead of 350 leaves the load as it is and the tx row at 77.89 instead of 79.49 ms (external review S1). |
| The 0.78 ceiling (`9976b94f`, reverted in round 12 by `feefd047`; `e8618e0c` held 0.77 again first) | The 8x8/1if flip ceiling was 0.78, owner decision pending. The manager updates the citation when the owner answers. The control holds 0.780 within it and 0.781 over, and `flip_grade --selftest` refuses 628 of 628. `FR_NFR.md` and the design document follow. The first form of this commit carried a review label in a comment, so `e8618e0c` restores 0.77 and `9976b94f` makes the raise again. Nothing after it touches its lines. |
| The loss turn and the alternation (`bdf8c0cc`) | internal review S1. D8: a sink's loss waits at most n_sinks deliveries whatever another sink loses again. D9: with both owed after a loss completion, the delivery makes the binding change. D10: a record's pass takes no turn. Four planted defects are caught: the loss turn from the first sink, never advanced, a loss always first (all three at two interfaces), and a record's pass taking a loss's turn (at 1x1/1if and 8x8/1if). All 448 SRP defects plant at one site. |
| The refusal threshold (`0acbb717`) | external review F1. The platform's one-interface image is refused at 61.5 RAMB36, half a tile past its 61.0 entry, as `ctrl_memory_ledger.py`'s boundary cases hold it. |
| Residues (`8ffdea83`) | internal review R1 and external review R1: every #977 citation of 2026-11-27 now names its ruling ("on the delivery bound", "on the population bound"), and the B-number comment prefixes in `test_plat_boot.cpp` are gone. internal review R2 and external review R3: `ctrl_loop.h`, `FR_NFR.md` and the design document state the 79.49 ms row (79.48 at the ruling's 415 us SETTLE) and link the owner's approval of 80 ms. |
| Whitespace (`3181a3ec`) | The merge-train builder's step 43 (`git diff --check`) refused `srp_binding.hpp`'s blank line at EOF. It is removed after the ceiling commit, whose files it does not touch. `git diff --check` over the PR delta is now clean against the merge base and against dev-soft-core's tip. Every step of the manager's builder exits 0 at `3181a3ec`. Step 47 leaves gate 11 not run, as on the candidate, since it needs a calibration build report. |

### Round 10d (`d8e12c16` to `25ff0632`)

| Piece | What and why |
|---|---|
| The alone records (`d8e12c16`, `25824442`, `25ff0632`) | Item 1. `CTRL_LOOP_ALONE_US` states each shape's pass of a record THE DRAIN takes alone, from the pass's start to the record's end, by the rule over every group of every arm, at most 1,935 us (`shape_costs.ALONE_MOST_US`, with a plant). It is 1,840 us at 8x8/1if (171,622 cycles measured) and 925 us at 1x1/1if (87,826 cycles, over every group), under its 950 us slice. The two-interface shapes take their slice. `slice_grade.py` holds a pass of one SRP record to the larger of the two, and a pass of more to the slice. The self-test adds checks at both points and two mutants. |
| The rows (`d8e12c16`, `25824442`) | Items 1 and 3. Every row by every source opens on the larger of the slice and the pass alone, with THE SETTLE of that record a term beside it (`rows_grade.ROW_COSTS`). That term is 105 us at 1x1/1if, and 425 us at 8x8/1if: the ruling's 415 restated by the rule for the 40,049 cycles measured in the swap. A row without its SETTLE is a new plant (rows_tiers 1,055 controls refused). `long_counted` moved to `paced_rows.py`, which keeps `rows_tiers.py` within its 1,000 lines. |
| The base (`7e7f59af`) | Item 2. 8x8/1if's polls base is 350 us and its walk 150 us, by the rule over 33,137 and 14,270 cycles (the swap at `e62e1936`). No finer split. |
| A record's pass makes no binding change (`55bd7f41`, `e59cf6ea`) | Item 4. `deliver`'s bind loop takes no change in a pass that carries a record alone (`settles`, the one-interface shapes). The change stays pending, owed to the next delivery of a pass that took no SRP record. D6 holds it per shape, and its plant runs in the one-interface campaigns. The new group `srp-register-both-owed` sends two inputs' UNBIND_RX just ahead of the both-kinds record, so a change is owed in the record's pass. The srp README states the bound as "deliveries of passes that took no SRP record". |
| THE TRANSMIT's figure (`70468e2a`) | Item 5, [approved by the owner](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7217388999): 80 ms at 8x8/1if, the cap. The hold-off stays 8 cs. `flip_grade --check --point 8x8/1if` holds the figure at or over its row. |
| The registration cost (`25824442`) | Restated by the rule over every registering group of both arms: 190 us at 8x8/1if (17,921 cycles a Talker, the JoinIn of both kinds) and 185 us at 1x1/1if (17,578). |
| Hot list (`c63e9d58`) | The final relearn: four windows on the 1x1/1if default arm, of 206,393, 274,149, 900,000 and 900,000 PCs. 295 entries are learned, the same five are dropped by the ruled filter over all 72 link maps, and 290 are listed, all 72 maps clean. |
| Memory ledger (`4352900b`, `4e595c85`) | The platform's 8x8/1if image plans 147,712 B of `rom`, 256 B past the 147,456 B that 60.5 holds. Its entry is 61.0 by the owner's rule of 2026-11-15, as ROM debt of 5.0 RAMB36 owed to the hybrid XIP lane's issue. The memory gate's ledger cases follow it. Every other image is within its entry. |
| Gate fixes (`2e466ae9`, `8c30e241`, `8765bfd5`, `dfda4df4`) | Round 10c's delivery bound rewrote the lines five SRP plants planted at, so the gate refused them for want of a site. Each is re-pointed at its line, and all 443 SRP defects plant at one site. The withdrawal plant now compiles. D7 covers the case coverage found untested: with a binding change and a loss both owed after a binding change, the delivery completes the loss. It comes with its plant. |
| Docs (`235a48c8`, `dcd1dc58`) | FR_NFR 3.4.1's shapes clause, `SPLIT_CONTROL_MEMORY.md`'s alone-records paragraph and the ledger. |

### Round 10's earlier pieces

Committed in round 10 before the ruling (at `e62e1936`), each re-measured at this head:

| Piece | What and why |
|---|---|
| The ceiling (`2d57e46e`) | 8x8/1if's flip ceiling 0.77 by [the owner's decision of 2026-11-27](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7213594113), 0.76 before by its decision of 2026-11-25; a control holds 0.761 within it and 0.771 over (the flip self-test refuses 617 of 617). FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY.md follow. |
| The idiom gate (`fd126873`) | #977's own Python had pushed `run.py` and `grade.py` past the 1,000-line ratchet and 11 lines past 120 columns, with 2 undocumented nested helpers; rewrapped, no behaviour change. |
| Pins (`f5552daf`, `cdb35fc7`, `9380ff82`) | lwSRP `e27b34c9`: its source delta past `73007b48` is comments and the `LWSRP_LEAN_COPY` 0 restore arm, used by the default-option shapes; the published ELF comparisons cover those images too. tsn-c-stack `5a07d9b7`: its tree is `0f72ca69`'s. All 80 product ELFs are byte-identical across each move: plat_ledger's platform images and the harness's 72 (8 arms at 1x1, 8x8/1if and 8x8/2if, each image and its plan's stand-in and mapped images). |
| The delivery bound (`f6b44e99`, `e62e1936`) | [The ruling's item 2](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7212897415). A delivery makes at most one binding change and, outside THE SETTLE, at most one loss completion, each the first owed from its turn. Where both are owed it makes only the kind the last one did not, so each owed waits at most 2 x `n_sinks` deliveries. The rest stay pending and keep the loop awake. THE SETTLE still completes every loss it owes, and THE TRANSMIT waits on none of them. Tests D1-D5 hold each rule, D7 since this round the case coverage found untested; eight planted defects, each caught. `ParkedReplacementRetiresThePreviouslyAcceptedBinding` now expects one retirement a delivery, the other owed. |
| S14 (`760d341c`, `25ed2bb0`) | The ruling's item 6, the 2026-11-27 ruling's item 3, #1023. Within the keep, min(`SRP_KEPT_TALKERS`, V less the bound sinks), the original checks hold. Past it, as at 8x8/1if with every input bound, nothing is declared before the Talker's next declaration, and then it is declared in THE TRANSMIT's next MRPDU. S14b leaves one input unbound and holds the original checks at every shape. Three planted defects, each caught. |
| The new groups (`c80f1e91`) | The ruling's item 4: every input's Lv alone (`srp-register-lv`), the same left until its leave timers run out in one centisecond (`srp-register-leavetime`), and every input's JoinIn of both kinds in one MRPDU (`srp-register-both`). |
| The fourth window (`ec9dc4be`) | The ruling's item 3: `srp-register-swap` on the 1x1/1if default arm, from 300,000 bus cycles before its swap record, 900,000 PCs, appended. The list is 290 entries, the same five dropped, all 72 maps clean. It moved the swap's cost by 0.6 % at 8x8/1if. |

- **Round 12's checks at `3256d1d2`:**
  - `load_grade --check` PASS, `--selftest` 32 of 32, and `load_deliveries.py` refuses every deliveries control;
  - `flip_grade --check` at 1x1/1if and at 8x8/1if PASS, `--selftest` 628 of 628;
  - the harness self-tests: `run.py --self-test` 0 failures, `kept_grade` 33 checks, `shape_costs` 25 of 25 and `--check`;
  - the Python and C++ idiom gates, and the docs workflow (100 of 100, the em-dash base dev-soft-core `0b594023`);
  - `git diff --check` over the whole delta, against the merge base `71bad8c0` and against `0b594023`: no hit;
  - every product ELF, 80 of 80, byte-identical to `25ff0632`'s, and `plat_ledger.py` PASS.

  All pass. `srp_deliver_mutants.py`'s change is a docstring sentence only, so the firmware gate was not re-run; round 11's run at `9976b94f` stands for its plants.

- **Round 11's checks at `9976b94f`:**
  - the firmware gate's four shards with `--self-test`;
  - `fw_coverage.py --check` (40 files), `test_ctrl_memory.py`, `plat_ledger.py` and `--self-test`, `ctrl_hot.py` both, and the twin;
  - the harness self-tests: `run.py --self-test` 0 failures, `load_grade` 32 of 32, `flip_grade` 628 of 628, `shape_costs` 25 of 25, `kept_grade` 33;
  - `load_grade --check` and `flip_grade --check` at both points;
  - the Python and C++ idiom gates, and the docs workflow (100 of 100).

  All pass.

## Measured (round 10d, standing at this head)

Every group of every arm at 1x1/1if and 8x8/1if: 578 group runs, one group a run, plus srp-kept with srp-bound in one run in each of their four arms. The images are `e59cf6ea`'s. The final head's 80 product ELFs are byte-identical to them, so the pools and both routes stand for `25ff0632`.

| | 1x1/1if | 8x8/1if |
|---|---|---|
| Group runs | 289 + 2 pairs: 285 exit 0, and the 4 single srp-kept and srp-bound runs are refused by `kept_grade`'s pairing and pass as the 2 pairs | the same |
| Stated misses (polls, slices, rounds, passes given whole) | 0 | 0 |
| Longest pass, against THE SHARE's 200,000 cycles | 155,676 (1.557 ms, `answering-every-port` `notice-burst-5`) | 193,036 (1.930 ms, the JoinIn of both kinds, none arm; 3.5 % under) |
| Heaviest polls base, against its statement | 19,847 of 22,500 | 33,565 of 35,000 (the swap) |
| Heaviest registrar walk | 3,260 of 3,500 | 14,108 of 15,000 (the swap) |
| Longest pass of one SRP record, against max(slice, pass alone) | 87,826 (925 us by the rule) of 95,000 | 171,622 (1,805 us) of 184,000 |
| Longest SRP slice of more records, against the slice | 80,021 of 95,000 | 123,248 of 147,500 |
| THE SETTLE at most, against its row term | 8,663 (105 us) | 40,049 (425 us) |
| A Talker's registration all in, by the rule | 17,578, 185 us | 17,921, 190 us |
| Load, against the ceiling (round 12, with the deliveries term against the after-window baseline) | 0.533 of 0.70 | 0.782 of 0.79 (0.766 without the term, against 0.77) |

- **Routes:**
  - 1x1/1if (image `2e3b1fe8`): WNS +0.159 ns, WHS +0.036 ns, 0 routing errors, 82 BRAM tiles.
  - 8x8/1if (image `f36a050a`): WNS +0.092 ns, WHS +0.036 ns, 0 routing errors, 45,672 LUT, 100.5 BRAM tiles.
  - Both meet the #818 floor at every corner.
- **`plat_ledger.py` at `25ff0632`:** PASS. 1x1: 132,576 and 133,248 B of `rom` (46.5, 47.5). 8x8: 147,712 and 147,312 B (61.0, 65.0).
- **Gates at `25ff0632`:** the firmware gate's four shards with `--self-test` pass. So do `fw_coverage.py --check` (40 files), `test_ctrl_memory.py`, `plat_ledger.py --self-test`, `ctrl_hot.py --check` and `--self-test`, and the twin. The harness self-tests pass: `run.py --self-test` with 0 failures, `kept_grade` 33 checks, `load_grade` 28 of 28 and `--check`, `flip_grade` 628 of 628 and `--check` at both points, and `shape_costs` 25 of 25 and `--check`. The Python and C++ idiom gates pass. The plants added or re-pointed this round are refused: at two interfaces all eight delivery plants, and at 1x1/1if the D6 plant and the six re-pointed SRP plants.
- **The docs workflow at `25ff0632`:** 100 of 100 steps pass.
- **THE TRANSMIT's figure:** at `e59cf6ea` the 77 and 80 ms builds are byte-identical, 80 of 80, including the 8x8/1if platform image. `git revert 70468e2a` applies cleanly at the head.

## Authoritative references

- IEEE 802.1Q-2018 10.7.11 (three MRPDUs in 1.5 x JoinTime), 10.7.4.1 (withdrawal), 35.2.6 (kind replacement).
- Milan v1.2 Table 4.3 (JoinTime).
- `sw/firmware/ctrl/loop/ctrl_loop.h` (THE SHAPES, `CTRL_LOOP_ALONE_US`, THE DRAIN, THE SETTLE), `sw/firmware/ctrl/app/ctrl_app_srp.c` (`deliver`), `sw/firmware/ctrl/srp/README.md`, `docs/reference/FR_NFR.md` 3.4.1, `docs/design/SPLIT_CONTROL_MEMORY.md`.

## How to get into the same state

```sh
git fetch origin pf-977-1 && git checkout pf-977-1
git submodule update --init third_party/lwSRP third_party/tsn-c-stack protocol-processor gptp-processor third_party/verilog-axis
git -C third_party/lwSRP rev-parse HEAD        # e27b34c9231abaa862bdb73f807238b330aa4c51 (lwSRP main, PR #22's merge)
git -C third_party/tsn-c-stack rev-parse HEAD  # 5a07d9b7d87298f04b15aa28f0304ec88b0aef81 (tsn-c-stack main, PR #41's merge)
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/litex/test_ctrl_memory.py
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <new dir>
python3 tb/verilator/ctrl_service_budget/run.py --self-test
python3 tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir <new dir> --variant none --groups srp-register-both,srp-register-both-owed,srp-register-swap --record-budget-findings --record-share-findings   # and --point 1x1
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # and --point 8x8/1if
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
```

Expected: every command passes. The 8x8/1if flip check needs both `70468e2a` (without it 77 ms is under the 79.49 ms row) and `3256d1d2` (without it the load of 0.782 is over 0.77). `python3 tb/verilator/ctrl_service_budget/load_grade.py --selftest` refuses 32 of 32, among them the deliveries term left out.

## Known limitations / out of scope

- **The 8x8/1if ceiling of 0.79** waits on the owner's answer. If it is refused, `3256d1d2` is reverted, the 8x8/1if flip check fails at 0.782, and 8x8/1if waits for #1025's margin recovery.
- **The deliveries term** is stated against the ordinary passes after the delivery window, the baseline the manager's decision accepts. Against the 50 ms and 500 ms pre-record medians the 8x8/1if load would be 0.779 and 0.781; they are recorded, not graded.
- **#1025**: THE SETTLE's one-entry completion, the margin recovery, is its own issue.
- **#1023**: its design text remains its own; S14's expectation is taken here.
- **The platform's 8x8/1if entry** is 61.0 RAMB36 under the owner's rule of 2026-11-15, as ROM debt owed to the hybrid XIP lane's issue.
- **The second hart.** The owner ruled no second hart for this image.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the 8x8/1if ceiling of 0.79 behind the owner's answer)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


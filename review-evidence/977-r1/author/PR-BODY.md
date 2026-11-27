[A825]

## Contents

- **[Status](#status)**: round 8 of #977: the integration with `dev-soft-core` and tsn-c-stack `main`, measured, under the owner's decision on round 7's ADP bound.
- **[Linked Issue / roles](#linked-issue--roles)**: the public task, the executor and the independent reviewers.
- **[Description](#description)**: what changed and why.
- **[Authoritative references](#authoritative-references)**: requirement and specification clauses, and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: checkout and dependency commands.
- **[How to validate](#how-to-validate)**: the exact commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this does not do, and why.
- **[Definition of Done](#definition-of-done)**: the merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Ready for review. Round 7 merged `dev-soft-core` `4df125b8` and tsn-c-stack `main` `c3bff8f3` (PR 40). Round 8 applies the owner's decision on the one open item, and measures the merged image:

- **ADP's LINK_UP bound** is stated at 12 mailbox accesses (option (a)): PR 40's seed reads `NOW_MS` once on each transition out of DOWN. The lines are #1015's, word for word, so the two PRs merge in `adp_mbx.h`, `MAILBOX_SPLIT.md`, `ctrl_mutants.py` and `scenario.py`.
- **Every CPU budget harness arm** at both points exits 0 on the merged image (below). `kept_grade.py` and `egress_ledger.py` pass.
- **The ruling's figures are unchanged** (`flip_grade.py --check` at both points). 1x1/1if: last 132.95 ms (135), ACMP 29.40 ms (30, margin 0.60 ms), txL 47.98 ms (49). 8x8/1if: load 0.757 (0.76), THE TRANSMIT 76.86 of 77 ms. 1x1/1if's load is 0.518 (0.70).
- **The 1x1/1if AECP notice item** measures 15,544 CPU cycles at most against its stated 165 us. The registrations term holds at 135 us (8x8/1if, at most 12,806 cycles a Talker) and 120 us (1x1/1if, 11,172).
- **The harness waited too briefly for ADP's LINK_UP draw** (`ea52ec11`). A link raised after enable draws over 0 to 4 s (Milan v1.2 5.6.3.5.3, Table 5.50), not the startup's 0 to 2 s. PR 40's seed draws 3.48 s at 1x1/1if, so the 2.2 s window refused `adp-advertise` there (the negative control). The window is now 4.2 s.
- **Both routes** meet the #818 floor at every corner.
- **The firmware gate** passes all four shards, catching 851 of 851 planted defects. `fw_coverage.py --check`, `plat_ledger.py`, the docs workflow and the harness self-tests pass.
- **tsn-c-stack** passes its quality job (28 of 28 gates, 512 planted defects caught) and its bare-metal job, and merges with `dev-linux` without conflict.

`pf-977-1` -> `dev-soft-core`. lwSRP is pinned at `opt-exec-3` (its own PR against lwSRP `main`). tsn-c-stack is pinned at `977-settle` `5d03517f`: the two commits on `main` `a795471c`, with `main` `c3bff8f3` merged in (its own PR, `PR-BODY-tsn.md`). By the ruling's item 4 the pin is for now: it moves to that PR's merge commit once it lands, and never stays on the branch.

## Linked Issue / roles

Closes #977
Relates to #665

Executor: `[A825]`
Internal cleared-context reviewer: to be named by the manager
External reviewer: to be named by the manager

## Description

Round 6 follows [the owner's ruling of 2026-11-26](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7180135694). Every bound is unchanged: the 1x1/1if load ceiling stays 0.70 and the 8x8/1if one 0.76, the last notice stays within 140 ms, ACMP within 30 ms, txL within 49 ms and THE SHARE within 2 ms.

| Piece | What and why |
|---|---|
| The join timer (`f36f4820`) | #1002's fix (`5baf3476`) with its test and planted control. `transmit_aged` holds while a centisecond is owed to the loop or a TICK is posted and not yet dispatched (`mbx_tick_pending`, a scan that consumes nothing). So lwSRP's join timer is never armed one centisecond early. This is the ruling's item 2. |
| Its tests (`655555db`, `3b944823`) | With the fix, four SRP planted defects and two reboot-silence ones escaped. The tests encoded the old early arming. #1002's own test follow-ups for exactly those tests (`12b1cab9`: `srp_mbx.cpp`, `srp_talker.cpp`; `7e8f4ddb`: `test_plat_boot.cpp`) are cherry-picked. They are tests only, and no MAAP commit was taken. This goes beyond "the fix with its test and planted control": it is the test half of the same fix, recorded here as a deviation. |
| The AECP item (`c0871493`) | The ruling's item 1. At 1x1/1if, `aecp-fanout`'s AECP notice item is stated at 165 us (15,464 CPU cycles measured). `CTRL_LOOP_QUEUED_MS` goes 130 -> 135 ms by the recorded rule (`poll_grade`, `load_grade`, `ctrl_loop.h`'s 1x1 shape, `notice_window`'s self-test, the harness README). Graded at 1x1/1if: last 132.95 ms (135), ACMP 29.40 ms (30; margin 0.60 ms), txL 47.98 ms (49). `FR_NFR.md` 3.4.1 records the 0.75 second-hart trigger met at 0.757 on 2026-11-25, with the study running and the owner's ruling of no second hart for this image (item 3). |
| tsn-c-stack `175cf9e0` (`47aa051f`) | `977-settle` rebased onto `main` `a795471c`. That includes PR 38: ADP discovery refuses a `control_data_length` under 56 and reads a longer one by its first 56 octets (IEEE 1722.1-2021 6.2.7.1.3). `SUBMODULES.md`, the submodule diagram and the stack's links follow the pin. |
| Hot list (`fda89791`) | Relearned at that pin by the procedure `plat/ctrl_split_hot.txt` records. There are three windows on the 1x1/1if split image, arm A, each from 300,000 bus cycles before the image's own first record commit (205,700, 273,797 and 900,000 PCs). The ruled filter over all 72 link maps drops the same five functions as round 5, so the list keeps 279 of 284; `mbx_tick_pending` is the one new entry. This is the measured image. |
| ADP adapter test (`f57cfa0d`) | The firmware test that held the old exact-56 rule is split in two. A short length is refused, with `valid_time` bits never lengthening it, and a long one restarts advertising through the mailbox. Two planted defects are re-anchored and one is added (`<` -> `!=`, caught by the long test), for 849 plants. The image is unchanged. |
| Load (`812afc24`) | `load_grade.REGISTRATION_US` is restated from both registering arms on this image by the recorded rule. At 1x1/1if it is 120 us: 11,150 CPU cycles a Talker all in, the answering-ports arm's (round 5: 10,826, 115 us). At 8x8/1if it stays 135 us: 12,712 cycles (round 5: 12,519), and THE SETTLE is at most 4,111 cycles a sink. The 1x1/1if load moves by under 0.001. |
| Docs (`0e820a90`) | `SPLIT_CONTROL_MEMORY.md`: the relearn at the new pin, and every image's fit within its ledger entry (about 160 B more `rom` an image; `plat_ledger.py`). |
| tsn-c-stack `5d03517f` | `977-settle` merges `main` `c3bff8f3` (PR 40: ADP's delay generator seeded on each transition out of DOWN from the sum of the MAC address and the local clock, IEEE 1722.1-2021 6.2.4.2.2). It is a merge commit, not a rebase. `CHANGELOG.md` keeps both unreleased entries. |
| Merge (`163e467f`) | `dev-soft-core` `4df125b8` merged. The tsn-c-stack gitlink is `5d03517f`, which contains `a795471c` and `c3bff8f3`; `gptp-processor` is the base's `3ce71b76`. `test_adp.cpp` is the base's (`941bc2d9`, whose long-discovery test covers `f57cfa0d`'s), and `ctrl_mutants.py` takes the base's four ADP discovery plants. The pin's links, `SUBMODULES.md` (#1013's PR 38 section kept, #977's restated) and the submodule diagram follow the gitlinks. |
| ADP's LINK_UP bound (`b9c01152`, `6e2c9116`) | `ADP_MBX_LAT_LINK` 11 -> 12 in `adp_mbx.h`, and the `LINK_UP / LINK_DOWN` row of `MAILBOX_SPLIT.md`'s ADP table 12 / 9. These are #1015's lines, word for word; the C0 check passes at 12, and `latency-extra-read` is still caught at 13. #1015's `adp_mbx_set_clock` and its THE DRAW comment are that PR's own change and are not taken, so the image is unchanged (16 of 16 images byte-identical). `seed-left-at-zero` is wrapped as #1015 wraps it, the same plant. |
| The harness's LINK_UP window (`ea52ec11`, `2fe50d53`, `09599524`) | `scenario.advertised()` waits 4,200 ms for each interface's ENTITY_AVAILABLE, not 2,200: the link is raised after enable, so the draw is LINK_UP's 0 to 4 s (Milan v1.2 5.6.3.5.3, Table 5.50; tsn-c-stack `ADP_DELAY_MAX_MS`; the firmware's own G1 test draws over it). The five groups that take it (`adp-link`, `adp-gm`, `adp-discover`, `adp-advertise`, `control`) run 2 s longer, and LINK_UP's model accesses read 12. The latent defect dates from `d58c8e22`: round 6's draw fell under 2.2 s, and PR 40's seed draws 3.48 s at 1x1/1if. With the old window that run is refused (`adp.tmr_delay.if0`: no TMR_DELAY expiry in the window); with the new one it passes. `2fe50d53` keeps `scenario.py` at the 1,000-line module ratchet (the docstring on one line). #1015 makes the same fix; `09599524` takes its words and its `fixture.link_up` at 12 model accesses, so the two PRs merge here. |
| Plants (`8000dae1`) | The firmware gate's `seed-left-at-zero` and `link-up-draws-startup-kind` re-anchored on the lines PR 40 rewrote: the generator's zero guard in `leave_down`, and LINK_UP's draw out of DOWN. They are the same defects and tests as the stack's own campaign, and both are caught. |

### Ablation (the ruling's item 2)

8x8/1if talker-notices with the grader unchanged:

| Image | Exit | Late run-outs | Joins |
|---|---|---:|---|
| `4003865a` + `5baf3476` (`f36f4820`) | 0 | 0 | 187.745 to 190.091 ms, within Milan v1.2 Table 4.3 |
| `4003865a` (the negative control) | 1 | 10 (groups 1 to 5, periodic and join, 60.25 to 60.35 ms past the opportunity) | |

### Every arm

Every arm on the merge's image (built at `163e467f`; `ea52ec11`'s images and models are the same, its builds in a clean clone; `run.py --regrade` at `ea52ec11`). Round 7's run takes every group from one queue, longest first, one group a run. The five groups `ea52ec11` rescripts were run again at `ea52ec11`, in both arms that have them.

| Point | Arm | Groups | Budget misses | Passes over THE SHARE | Exit |
|---|---|---:|---|---:|---|
| 1x1 | none | 103 | the 7 ledgered `backlog-owed` rows | 0 of 179,032 | 0 |
| 1x1 | answering-ports | 104 | the same 7 | 0 of 163,371 | 0 |
| 1x1 | answering-every-port, answering-later, declaring-outputs, shutdown-entry, talker-notices, valid-destinations | 16, 8, 5, 2, 8, 3 | 0 | 0 | 0 |
| 8x8/1if | none | 103 | the 7 ledgered rows | 0 of 312,803 | 0 |
| 8x8/1if | answering-ports | 104 | the same 7 | 0 of 295,955 | 0 |
| 8x8/1if | answering-every-port, answering-later, declaring-outputs, shutdown-entry, talker-notices, valid-destinations | 16, 8, 5, 2, 8, 3 | 0 | 0 | 0 |

- The 1x1/1if AECP notice item (`aecp-fanout`'s dearest `aecp` poll item, stated 165 us, 16,500 CPU cycles) measures 15,544 cycles in answering-ports, 15,408 in declaring-outputs and 13,746 in none.
- The registrations term (`regcost2.py`, both registering arms): at 8x8/1if at most 12,806 cycles a Talker all in, 135 us by the rule (stated 135), THE SETTLE at most 4,136 a sink. At 1x1/1if at most 11,172 cycles, 120 us by the rule (stated 120).
- `kept_grade.py` PASS at both points (nothing owed).
- `egress_ledger.py --point 8x8-1if` PASS: all seven rows measured and within their figures, by 0.11 to 0.21 ms; `--selftest` 18 mutants PASS.
- Routes of the merge's platform images (`plat_ledger.py` at `8000dae1`), worst corner:
  - 1x1/1if: WNS +0.234 ns and WHS +0.036 ns; 32,693 LUT, 42,793 FF, 82 BRAM (round 6: +0.231 / +0.035 ns; 32,553 LUT, 42,798 FF).
  - 8x8/1if: WNS +0.098 ns and WHS +0.036 ns; 45,704 LUT, 53,348 FF, 100.5 BRAM, round 6's exactly.
  - 0 routing errors in either.

## Authoritative references

- IEEE 802.1Q-2018 10.7.4.1 (the transmit opportunity), 10.7.11 (three MRPDUs in 1.5 x JoinTime), 35.2.6 (kind replacement).
- IEEE 1722.1-2021 6.2.7.1.3 (ADP's `control_data_length`).
- Milan v1.2 Table 4.3 (JoinTime), 5.5.3.5 (ACMP's listener state machine).
- `sw/firmware/ctrl/loop/ctrl_loop.h` (THE TIERS, THE SETTLE, THE SHAPES), `sw/firmware/ctrl/plat/ctrl_split_hot.txt`, `docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md` 3.4.1, `tb/verilator/ctrl_service_budget/README.md`.

## How to get into the same state

```sh
git fetch origin pf-977-1 && git checkout pf-977-1
git submodule update --init third_party/lwSRP third_party/tsn-c-stack protocol-processor gptp-processor third_party/verilog-axis
git -C third_party/lwSRP rev-parse HEAD        # 73007b4807977517045e8aa485c61ebb8f5ee843 (lwSRP opt-exec-3)
git -C third_party/tsn-c-stack rev-parse HEAD  # 5d03517f2ab42416654a8f2be2f71cfc51d82440 (tsn-c-stack 977-settle)
```

## How to validate

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4, 2/4, 3/4
python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
python3 sw/firmware/ctrl/test/ctrl_hot.py --check && python3 sw/firmware/ctrl/test/ctrl_hot.py --self-test
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <new dir> --self-test
python3 sw/litex/test_ctrl_memory.py
make -C tb/verilator/milan_dp twin twin-plants twin-maps twin-maps-plants
python3 tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <new dir> --record-budget-findings --record-share-findings   # and --point 8x8-1if, and each --variant
python3 -I tb/verilator/ctrl_service_budget/kept_grade.py <build dir> --results <its results>
python3 -I tb/verilator/ctrl_service_budget/egress_ledger.py --point 8x8-1if <8x8-1if arm A results>   # and --selftest
python3 -I tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # and --point 8x8/1if
```

Expected result:

- Every command passes.
- `run.py` reports `backlog-owed`'s seven rows past their 20 ms at both points, as the base does (the scenario's 60 ms egress hold). `--record-budget-findings` records them, and `egress_ledger.py` holds them.
- The firmware gate's control campaign catches 851 of 851 planted defects.
- The gate table and receipts are in the round's comment.

## Known limitations / out of scope

- **#1015 and this PR** state ADP's LINK_UP bound in the same words, and make the same harness fix; they merge in `adp_mbx.h`, `MAILBOX_SPLIT.md`, `ctrl_mutants.py` and `scenario.py` (a trial merge with #1015's branch `35d29eb7`). They still conflict in the tsn-c-stack pin's docs and diagram (#1015 pins `c3bff8f3`, this PR `5d03517f`), which the PR that lands second regenerates.
- **The adapter's seed** answers PR 40's `seed` port with `NOW_MS`, the mailbox's only clock. #1015 adds a microsecond clock for it (`adp_mbx_set_clock`); that is its own change and is not taken here.
- **The hot list is not relearned at `5d03517f`.** This round is integration only. `ctrl_hot.py --check` passes (279 entries, in the recorded order). PR 40's `leave_down` and `mix` run only on a transition out of DOWN, and they are not on the list.
- **The second hart.** The 0.75 trigger is met (0.757 on 2026-11-25) and the study runs. The owner ruled no second hart for this image.
- **The pin is a branch head for now.** PR #1016 (stack `a795471c`) has landed. Once tsn-c-stack's PR merges, the pin moves to its merge commit, and the image is rebuilt and re-measured there.
- **The size fixture's 8x8/2if entry** stays at 62.5 RAMB36 (owner's rule of 2026-11-15; ROM debt owed to S14).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md) (`dev-soft-core` `4df125b8` merged at `163e467f`; the gates above on the head)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

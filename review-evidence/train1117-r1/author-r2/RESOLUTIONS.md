# RESOLUTIONS: the flip train's composition, round 2 (#665)

Round 2 continues round 1's branch at `7431b6ba` under #665's ruling of 2026-11-17 (issuecomment-6950343235):
decision 1 (the ledger: #931's `own_point`), decision 2 (THE STEP: the PHY poll against the store's pace) and
decision 3 (the 1x1/1if rows: attribute now, cut at the final head). Conventions are round 1's: one row per conflicted
file per step; "Train" is the branch before the step, "PR" the frozen head merged; every merge is
`git merge --no-ff <frozen head>`, checked against its PR's GitHub head immediately before (`headcheck.sh`, receipts).
A figure both sides restated is recomputed at the step from the composed tree by its tool: the ROM ledger by
`plat_ledger.py` (the platform's image at the four points) and by the CPU budget harness's 8x8/2if build in every arm
(the size fixture's), each entry at its measured tiles by the owner's rule of 2026-11-15 (S14 debt). The coverage
ratchet comes only from `fw_coverage.py --write`.

## Step 7: #931 `d06ded5a` (map edits through the EDIT window; #923, #924); merge `6a8126e4`

Merge base `16ba667d`. The same 15 files as round 1's scratch attempt. Seven take round 1's scratch resolutions,
carried onto the recomposed tip by `git merge-file` (the hunks equal round 1's but for their labels; the three
documents' other lines differ by #914's new head only, no conflict). The ledger files are resolved by decision 1.

| File | Train's intent | #931's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/aecp/aecp.h` | REBOOT's due and acceptance (#871) | the EDIT port, `aecp_restore_commit` | both | independent declarations |
| `sw/firmware/ctrl/aecp/aecp_face.h` | "random is the platform's"; `(mbx_win_read, mbx_win_ask)` | the EDIT port's lines | both, word for word | disjoint edits |
| `sw/firmware/ctrl/test/test_aecp.cpp` | GSI kind 2 answered by `path()` (#897) | the EDIT window's transaction (`edit()`) | one fixture `answer`: kind 2 the train's path, EDIT #931's transaction, every other window `word()`; both test sets | each window its own answer |
| `tb/verilator/ctrl_service_budget/edit_rows.py` | 1x1/1if SET_CONFIGURATION 305 (#871, #897); 8x8/1if row 335 / 685 (#914) | one-row edit 295 at 1x1/1if and 355 at 8x8/2if (#923's commit) | 1x1/1if {295, 305}, 8x8/2if {355, 595}, 8x8/1if {335, 685}; both histories | each side's move; 8x8/1if's one-row edit with #923's commit is unmeasured, owed at the final head |
| `docs/design/MAILBOX_SPLIT.md`, `docs/reference/FR_NFR.md`, the harness README | the train's rows and figures | #923's | word-level merges (round 1's) | disjoint edits |
| `sw/litex/ctrl_memory.py` (5) | `product_point`, the `product` flag, entries 59.5 / 61.0 / 56.5 | `own_point`, entries 59.5 / 61.0 / 56.5 | **ruled (decision 1)**: `own_point`; `product_point` and `Ledgered.product` removed; entries at the measured composition: the fixture 60.0, the platform's two-interface image 62.0 (`ctrl_plat` 20,672 B), its one-interface image 57.5 (18,496 B); both histories in each entry's `owed` and in the comment | the ruling; the tools' measurement |
| `sw/litex/milan_soc.py` | `add_ctrl_memory` by `product_point` | by `own_point` | #931's | ruled |
| `sw/firmware/ctrl/test/ctrl_plat_image.py` (auto-merged) | the link without `--ledgered-point` by `product_point` | named point only | by `own_point` | the product build's rule, as #933 had its link follow it; `product_point` is gone |
| `sw/litex/ctrl_memory_ledger.py` (8) | `PLATFORM_1` and `PRODUCT = {PLATFORM_1}`; HELD with the flag; `product_facts`; 13 plants | `PRODUCT` the one-interface name; HELD without it; 9 plants | #931's names and HELD; REFUSED: #931's rows (a superset of the train's) and the train's unheld-name row beside #931's; `product_facts` kept for the product image (planned at its entry, refused half a tile past and with another `ctrl_plat`), its loop naming no point for the two two-interface images removed; plants: the union of distinct edits (the train's one-interface "at 57.0" and "without ctrl_plat" are #931's same edits, kept once; the train's "at the two-interface ctrl_plat" kept) | **ruled removal**: #933's refusals of the two 8x8 two-interface images and its flag plants (the platform's two-interface entry made a product entry; the size fixture's made one). The ruling names two; #933's third, "the one-interface entry not a product entry", plants the same removed flag and goes with it; the one-interface image's planning is held by #931's facts and plants |
| `sw/litex/test_ctrl_memory.py` (6) | the SoC build plans only the product entry and refuses the others' (#933); `soc_plan`; 4 `product_point` mutants | each entry planned at its own entry through `add_ctrl_memory`; an unledgered 8x8 image refused at 56.5 two ways; 3 `own_point` mutants | both arms' loops (`product_facts`, #931's own-entry loop); #931's `add_ctrl_memory` rows; the train's rows refusing the two-interface images removed (ruled); #933's 4 `product_point` mutants and their property removed with their target; the case writer moves four tiles to `.text` so a case reaches 63.0 | ruled; #931's own-entry mutants (no entry, staging buffer alone, names alone) hold `own_point`; the platform's 62.5 refusal needs a 62.5 case |
| `tb/verilator/ctrl_split_boot/plat_ledger.py` (3) | `ONE8`; `product-override-not-taken`; an unlinked override at a size no image has | `TWO1`; an unlinked override at the 1x1 two-interface `ctrl_plat` | both names; both unlinked-override controls (#933's as `override-unlinked-no-image`): 9 controls | each control a distinct case |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (8) | sections 3 and 5 by `product_point`; 13 planted ledgers; "At #901's head, merged as `70f4056f`" | by `own_point`; 9 planted ledgers; "#901's review head `16ba667d`" | `own_point`; both histories; the measured entries and a section 5 table for the composed train; 10 planted ledgers; the head named both ways (`16ba667d` merged as `70f4056f`, firmware identical) | ruled; measured |
| `sw/firmware/ctrl/plat/README.md` (2), `tb/verilator/ctrl_split_boot/README.md` | product entry; 61.0 / 56.5 | own entry; 61.0 / 56.5 | `own_point`; the measured 62.0 / 57.5; the README's control list nine | ruled; measured |
| `sw/firmware/gtest/coverage.ratchet` (2) | | | the train's lines at this commit | its generator refuses here: the gate fails on B12 (F4, decision 2); regenerated at `03c92617` |

**Measured at step 7** (`plat_ledger.py --self-test`, receipts/ledger/s7-plat-ledger2.log; the harness build,
receipts/ledger/s7-fixture-summary.txt): `ctrl_plat` 17,856 / 19,392 / 18,496 / 20,672 B, the same as at the round-1 tip
`7431b6ba` (whose own `plat_ledger` run fails on round 1's provisional figures, receipts/ledger/pl-tip.log): #923's
commit adds no `ctrl_plat` byte here, only 2,168 B of `rom` at every point. The platform images plan 44.5, 45.5, 57.5
and 62.0 RAMB36 (44.0, 45.0, 57.0, 61.5 at the tip); the fixture plans 60.0 in all six arms, 129,920 to 130,424 B of
`rom`, past the 129,024 B that 59.5 holds. `plat_ledger` PASS at all four points, 9 of 9 controls; `test_ctrl_memory`
PASS.

**Fix `b1af3b54`**: the union put `aecp_mutants.py` at 1,010 lines and `test_ctrl_memory.py` at 1,011, past the idiom
gate's 1,000 with its ratchet full. The five SET_STREAM_INFO defects move to `aecp_stream_info_mutants.py`, spread back
in place (the defect table identical: 361 defects, same names, files, edits, checks and order); three items of
`test_ctrl_memory.py`'s docstring are rewrapped, words unchanged.

## THE STEP by decision 2: `03c92617`, fixes `45708d9e` and `afbbde54`

The store's centisecond step keeps its first place; a call that owes no centisecond step takes an owed PHY frame and
the store takes no extra (#920) step in it; no call carries a save's step and a frame.

- `nvm_store.h`/`.c`: `nvm_store_owed()`, true while a centisecond's step is owed. The header's #920 paragraph states
  the exception and that the slowest pace and every worst case stand (not restated).
- `ctrl_plat_phy.c`: `owes()` (a poll in progress, a poll due or a probe that missed); `ctrl_plat_phy_store_step`
  gives a call with no centisecond step owed and a frame owed to the frame alone, else is #933's.
- `ctrl_plat_phy.h`, `ctrl_loop.h` (THE STEP), the plat README: restated to the rule, with its reasons (IEEE 802.3
  22.2.4.2.13, IEEE 802.1AS-2011 10.2.4.11, Milan v1.2 4.2.6.2.5).
- `test_plat_boot.cpp`: B12 keeps every assertion and gains two, "B12 the yielding call leaves the store's step count
  unchanged" and "B12 a call with no frame owed takes the extra step". L5 (a save in flight 500 ms, four poll
  periods: a loss and a return each published within one period, the save in flight across both, then complete) and L6
  (a PHY that never answers: a frame owed in every call; the save durable within (CTRL_LOOP_STEP_AGE + 1) centiseconds
  a step, its stated slowest pace).
- `plat_mutants.py`: the two ruled plants, `plat-phy-frame-yields-to-the-extra-step` (caught by L5 "a loss during a
  save is published within one poll period") and `plat-phy-frame-beside-the-extra-step` (caught by B12 "the yielding
  call leaves the store's step count unchanged"); and two more, since every test of `test_plat_boot.cpp` must be named
  by a plant (`SOURCES`) and B12's second new assertion must be shown to fail:
  `plat-phy-frame-before-the-centisecond-step` (L6 "the save is durable while every probe misses") and
  `plat-phy-extra-step-never-taken` (B12 "a call with no frame owed takes the extra step"). 117 + 4 = 121 defects;
  the control campaign 793 + 4 = 797.
- The coverage ratchet regenerated by `fw_coverage.py --write` (the gate passes in coverage mode).
- `45708d9e` rewraps two of those plant rows (AST-identical); `afbbde54` moves the four into their own function,
  spliced in place (`phy_mutants` was 105 lines, past 100; the table identical, 121 rows, same order).
- `6ad5c259`: `plat-phy-extra-step-never-taken` as first written (`if (!nvm_store_owed()) {`) left the static
  `owes()` unused, so `-Werror` refused its build and it escaped at `03c92617` (796 of 797, "0 check(s) failed"). Its
  condition now keeps `owes()` referenced (`!nvm_store_owed() && (owes(ctx) || true)`); planted alone
  (`--slice 614/797`) it is caught, and the control campaign at the tip catches 797 of 797.

## Step 8: #932 `0fdfdba7` (the latest Talker registration decides; #925); merge `31304b74`, fix `eafe4a16`

Merge base `70f4056f`. 7 files conflicted.

| File | Train's intent | #932's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/litex/ctrl_memory.py` (3) | own_point ledger, 62.0 / 20,672 | platform 61.0, `ctrl_plat` 21,248 with #925's StreamIDs (`sram` a 57th granule) | the train's structure, entries measured: the platform's two-interface image 62.5 (`ctrl_plat` 21,504 B), its one-interface 57.5 (18,944 B), the fixture 60.0; #925's history added | measured |
| `sw/litex/ctrl_memory_ledger.py` (8), `test_ctrl_memory.py` (4) | the step-7 cases, plants and docstring | #925's figures | the train's, restated to 62.5 / 63.0 and the measured `ctrl_plat` sizes 17,984 / 19,712 / 18,944 / 21,504 | measured; the case writer's 63.0 reaches the platform's refusal |
| `sw/firmware/ctrl/test/srp_mutants.py` (2) | `srp_listener_mutants` (#930) | `srp_kind_mutants` (#925) | both imports and both spreads | independent tables |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (5), plat README (2), split-boot README | the step-7 figures | #925's | both histories; the measured figures; section 5's table with steps 6, 7 and 8 | measured |
| `sw/firmware/gtest/coverage.ratchet` (1) | | | regenerated at `eafe4a16` | the gate fails at `31304b74` (below) |

**Measured at step 8** (receipts/ledger/s8-plat-ledger2.log, s8-fixture-summary.txt): `ctrl_plat` 17,984 / 19,712 /
18,944 / 21,504 B; the platform images plan 44.5, 45.5, 57.5 and 62.5 RAMB36, the last with its `sram` 115,440 B, 752 B
past 56 granules, as at #925's own head; the fixture 60.0 in all six arms, 130,472 to 130,968 B of `rom`.
`plat_ledger` PASS, 9 of 9 controls; `test_ctrl_memory` PASS.

**Fix `eafe4a16`** (a semantic composition, no textual conflict): #930's `srp_listeners.cpp` checks each settled step
of the copied run against a registrar walk, its expected Listener declaration by the rule before #925 (Failed whenever
both kinds are registered). #925 (ruled on #925, POSITIVE) makes the latest registered kind decide (`listener_kind`).
At `31304b74` the two Listener-copy suites fail only that check, at 1x1/1if and 8x8/1if (95 and 149 steps); the
copied-against-reference differential passes, so the code's behaviours agree and only the oracle is stale. The oracle
now derives the expected declaration by #925's rule from the walked kinds and the sink's `latest_kind`; every other
comparison is unchanged. The coverage ratchet is regenerated there.

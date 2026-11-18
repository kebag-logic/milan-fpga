# RESOLUTIONS: the flip train's composition, round 1 (#665)

One row per conflicted file per step. "Train" is the branch before the step (dev-soft-core `cb96336d` and the steps
before it); "PR" is the frozen head merged. Every merge is `git merge --no-ff <frozen head>`; each head was checked
against its PR's GitHub head immediately before its merge. A figure both sides restated is recomputed from the composed
tree after step 7 (section "Restated at the composed tree" below), by its tool or by the rule; a per-step resolution of
such a figure takes the side that moved it from the merge base, the larger where both did, and is marked
*provisional*.

## Step 1: #881 `d3e61e37` (AECP REBOOT on the split CPU, #871); merge `43b954e6`

Merge base `41ca9f87`. 18 files conflicted, the plan's 18. The #881 lane's own sync of `cb96336d` (its local
reference branch, `59fe35b5`) resolved the same merge with the parents swapped; every hunk below was read against it
(ours / base / theirs / its resolution) and checked to keep both sides. The composed tree equals that reference
merge's tree exactly (`5cf4989c`), and every auto-merged file equals it too.

| File | Train's intent | #881's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/aecp/aecp_mbx.h` | `AECP_QUEUED_MS` 140 at 1x1/1if (#895's ruling, row 135.43 ms) | 135 (its row 134.74 ms with REBOOT) | 140, both histories in the comment | the queued rule (`queued_bound.py`) at the composed tree: the row is 137.89 ms, so 140; `flip_grade --check --point 1x1/1if` holds it |
| `sw/firmware/ctrl/loop/ctrl_loop.h` | comment: AECP_QUEUED_MS's 140 | comment: 135 | the train's (140) | the composed figure, above |
| `sw/firmware/ctrl/aecp/README.md` | 140 ms and its ruling | 135 ms and REBOOT's row | 140, with REBOOT's 135 as history | the composed figure |
| `sw/firmware/ctrl/plat/README.md` (2 hunks) | SRP Talker gate, GET_AS_PATH through the face, `platboot` B11 GET_AS_PATH; 42 plat defects | REBOOT's reset port, `platboot` B11..B23; 62 defects | both sections; GET_AS_PATH's test renumbered B24; 64 defects | REBOOT took B11..B23 on its side; the count is the composed campaign's (42 + 62 - 40 at the base) |
| `sw/firmware/ctrl/test/test_plat_boot.cpp` (2) | `B11GetAsPathAnswersTheDatapathsSequence` | REBOOT tests B11..B23 | all; GET_AS_PATH's test renamed `B24...`, its messages "B24" | two tests cannot share B11; no stale B11 GET_AS_PATH reference remains (git grep) |
| `sw/firmware/ctrl/test/plat_mutants.py` | `plat-as-path-unavailable` caught by B11 | `reboot_mutants` | both; the AS_PATH mutant names B24 | its test's new name |
| `sw/litex/ctrl_memory.py` (3) | 8x8 fixture entry 59.5, platform 60.5 (#897) | platform 61.0 cap / entry 60.5 (#871) | both histories; ctrl_plat 20,416 | *provisional*: restated at the composed image by `plat_ledger.py` after step 7 |
| `sw/litex/ctrl_memory_ledger.py` (4) | PLAT sizes +64 B at three points; fixture 59.5 | +128 B at every point | #881's sizes, the train's 59.5 | *provisional* (as above) |
| `sw/litex/test_ctrl_memory.py` (2) | 59.5 / 60.5 | 59.0 / 60.5 | 59.5 / 60.5 | the entries above |
| `tb/verilator/ctrl_service_budget/build.py` | answering-ports: path port is arm_path's (#897); valid-destinations arm (#895) | answering-ports gives AECP a reset port (#871) | both arms' text | independent additions |
| `.../edit_rows.py` | paced SET_CONFIGURATION 305 (28,752) | 305 (28,750) | 305, both measurements | equal |
| `.../load_grade.py` (2) | the cost table's #895/#897 restatements | REBOOT's: SRP 285, AECP 240, events_none 40, retained 285 | each cost the side's that moved it from `41ca9f87`, the larger where both did (AECP 245, events_none 40) | *provisional* |
| `.../poll_grade.py` | base 225 | retained 285 | base 225, retained 285 | each side's move, *provisional* |
| `.../record_classes.py` (7) | GET_AS_PATH held and required (#897) | REBOOT accepted and refused required (#871) | union of docstring, constants, findings, controls and the synthetic pass | independent checks; self-test 17 of 17 |
| `.../selftest_notice.py` | (140, 62) | (135, 62) | (140, 62) | the composed figure |
| `.../README.md` (3) | 140 ms, GET_AS_PATH's record class | 135 ms, REBOOT's record class | both | |
| `.../poll_grade.py`, `load_grade.py` comments | | | both histories | |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (6) | #897 rows, entries, history | #871 rows, entries, history | both histories; the train's "at this head" figures | *provisional* figures, restated after step 7 |
| `docs/reference/FR_NFR.md` | 140 ms and #895's composition | 135 ms with REBOOT | 140 with REBOOT's 135 as history | the composed figure |

Checks at `43b954e6` (receipts/steps/s1/): docs gates, em-dash (297 added lines, 0 findings), hygiene, idioms, harness
self-test (0 failures), `rows_tiers` 1033/1033, `record_classes` 17/17, load gate PASS and 26/26, flip check at
1x1/1if PASS (last 137.89 within 140), flip self-test 585/585, `test_ctrl_memory` PASS. The all-points flip check
fails on the 8x8/2if rows only, the same eleven findings as the base `cb96336d` (reported, not held, by the owner's
decision of 2026-11-12). Firmware suites and the control campaign: section below.

## Step 2: #914 `8883d499` (the 8x8/1if tier rows, THE RETRY keyed on the shape; closes #930); merge `136e64ce`

Merge base `70f4056f`. 12 files conflicted (the plan's alone-on-live 9, plus `notice_window.py`, `poll_grade.py` and
`sw/firmware/ctrl/aecp/README.md`, which step 1 touched).

| File | Train's intent | #914's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/loop/ctrl_loop.h` (3) | `CTRL_LOOP_SRP_UNIT_US (MBX_N_IF == 1u ? 285u : 365u)` (#871: SRP's record 285); `CTRL_LOOP_TX_MS (... ? 35u : 105u)` (#897, tx row 34.20) | THE SHAPES: one table keyed on (interfaces, sources, sinks); 1x1/1if's row carries 280 and 34; 8x8/1if's own row | #914's table, its 1x1/1if row at SRP unit **285** and TX **35**; its comments name both moves | the train moved both 1x1/1if figures from `70f4056f`, #914 moved neither; `load_grade.py` (record.srp 285 at 1x1/1if) refuses any other unit; `SRP_REDECLARE_CS` stays 2,023 cs at 1x1/1if (ceil(35/10) = ceil(34/10)) |
| `tb/verilator/ctrl_service_budget/rows_tiers.py` (2) | the TX control's literal figure 35 | the control plants one under each point's figure read from the table | #914's | its code reads the composed table, so it holds the train's 35 |
| `.../flip_grade.py` (2) | same, literal 35 | same, from the table | #914's | as above |
| `.../notice_window.py` | `queued_ms(interfaces)` regexes the old macro; docstring names REBOOT's 135 | `queued_ms(at)` reads THE SHAPES | #914's function, the train's history in its docstring | the old macro form no longer exists after the merge (`AECP_QUEUED_MS CTRL_LOOP_QUEUED_MS`) |
| `.../edit_rows.py` | paced SET_CONFIGURATION 305 at 1x1/1if (#871, #897) | `PACED['8x8/1if']` 335 / 685 | both: 1x1/1if 305, 8x8/1if's row | independent points |
| `.../poll_grade.py` (2) | ONE.retained 285 (#871) | ONE / TWO / EIGHT_ONE keyed on the shape | #914's structure, ONE.retained **285**, both comments | the train moved it, #914 did not; *provisional* |
| `.../record_classes.py` (4) | 1x1/1if completeness also needs REBOOT accepted and refused (#871) and the answered GET_AS_PATH (#897); any answering-ports GET_AS_PATH at another length refused | completeness held per point over COMPLETE (1x1/1if, 8x8/1if), each at its own statements | #914's per-point loop; inside it, at 1x1/1if (`REBOOT_PATH_POINT`), the train's REBOOT and GET_AS_PATH checks; the any-point length check as the train had it; both control lists | each side's behaviour exactly: neither PR holds REBOOT or GET_AS_PATH completeness at 8x8/1if, so the composition does not either (noted for the composition review); self-test 20 of 20 (17 + 3) |
| `.../README.md` | record classes: REBOOT and GET_AS_PATH | record classes per point | one paragraph carrying both, controls listed from both | |
| `sw/firmware/ctrl/aecp/README.md` | REBOOT's 135 as history | descriptors' count by shape; 130 at 8x8/1if | word-level merge, both edits | disjoint edits in one paragraph |
| `sw/firmware/ctrl/srp/README.md` | TX 35 at 1x1/1if (#897) | the hold-off at 8x8/1if 2,026 cs, THE SHAPES; #930's Listener copy | word-level merge, both edits | disjoint edits |
| `docs/reference/FR_NFR.md` (2) | REBOOT's 135 history; TX 35 | 8x8/1if keeps 130 by its shape | word-level merge | disjoint edits |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | sections "GET_AS_PATH through the face", "GET_AS_PATH on SRP's Talker declarations (#897)" | section "THE SHAPES and 8x8/1if" | both, the train's first (their chronological order) | both appended at the same point |

Checks at `136e64ce` (receipts/steps/s2/): as step 1, plus `shape_costs --check` PASS and `--selftest` 25/25,
`egress_ledger --selftest` 15 mutants 0 failures, `record_classes` 20/20; the 1x1/1if model is unchanged from step 1;
the all-points flip check's findings equal the base's.

## Step 3: #918 `394612c5` (hold an AECP command its channel has no token for until the next refill, #917); merge `874bd403`

Merge base `cec88385`. 7 files conflicted, the plan's alone-on-live 7.

| File | Train's intent | #918's intent | Resolution | Why |
|---|---|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py` | module docstring reflowed to 120 columns | the same docstring reflowed, one line break elsewhere | the train's | the same words |
| `.../grade.py` | `import join_grade` (#894) | `import held` (#917) | both, `held` then `join_grade` | independent imports, alphabetical |
| `.../selftest_mutants.py` | `import join_grade` | `import held` | both, alphabetical | as above |
| `.../run.py` | `POINTS` with `8x8-1if` | the same `POINTS`, with a comment naming the point | #918's | the same table; the comment kept |
| `.../selftest.py` | the ledgered-point check with `8x8-1if: None` | the same check, wrapped over three lines | the train's | the same expression |
| `.../scenario.py` | the group list with REBOOT's, the datapath window's and the long notice's groups | the group list with `held.groups(p)` | the train's list, `held.groups(p)` last | both sides' groups, each once |
| `docs/design/MAILBOX_SPLIT.md` | the face row: GET_AS_PATH through each interface's window (#897) | the planted-defects row: thirteen default arms, the held frame's among them | word-level merge, both edits | disjoint edits in two table rows |

Composition fix `d7941d4d`: each side left `build.py` at exactly 1,000 lines and `grade.parse` at 100 and 98, the idiom
gate's limits (`LONG_MODULE_LINES`, `LONG_FUNCTION_LINES`); the union is 1,004 and 101, so `check_py_idiom.py` fails
(long function 10 > 9, long module 11 > 10). The ratchet is not raised: three comment blocks of `build.py` (lines
390, 640, 877) are rewrapped to 120 columns and one `grade.parse` comment moves onto its `elif` line, words unchanged;
both files' ASTs are identical before and after.

Checks at `874bd403` and `d7941d4d` (receipts/steps/s3/): see the HANDOFF's step table.

## Step 4: #935 `37255683` (split gates at the base, #929); merge `d21f7aab`

Merge base `70f4056f`. 2 files conflicted.

| File | Train's intent | #935's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/test/srp_arms.py` | `listener_arms` (#930: the Listener copies against the reference walk at 1x1/1if and 8x8/1if) | `mbx_entity_arms` (#929: `srp_mbx.cpp` at the 8x8 entity, both interface counts) | both functions | independent arms |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py` | calls `listener_arms` in the suite run and in the coverage run | calls `mbx_entity_arms` in the suite run | both calls in the suite run; the coverage run as the train had it | each side's call sites as it wrote them |

## Step 5: #933 `1a1e6665` (poll the PHY link after boot, advertise 1000BASE-T only, #919); merge `89eea108`

Merge base `70f4056f`. 13 files conflicted. Resolved first in a throwaway worktree on `d21f7aab`; the lane's merge
reproduced its tree exactly (`b94388eb`), so the firmware runs there carry.

| File | Train's intent | #933's intent | Resolution | Why |
|---|---|---|---|---|
| `sw/firmware/ctrl/plat/ctrl_plat.c` | `ctrl_plat_step`: a READY loop stops for the REBOOT's departure (#871) | a refused stage's console turn also gives the PHY a frame (#919) | the PHY frame in the refused-stage branch, then the REBOOT branches and the loop, each as written | in READY the PHY runs through THE STEP inside the loop, which the departure stops by design |
| `.../ctrl_plat.h` | `uintptr_t reboot` in the environment | `struct ctrl_plat_phy_bus phy` | both fields | |
| `.../ctrl_plat_main.c` | `.reboot = CTRL_PLAT_REBOOT` | `.phy = {...}` | both | |
| `.../ctrl_plat_gen.py` (2) | `ctrl_reboot_req` a required row; docstring | the PHY's three rows, all or none; docstring | both rows sets, one docstring | |
| `sw/firmware/ctrl/test/ctrl_plat_csr.csv` | `ctrl_reboot_req` at 0xf0001800 | the PHY rows at 0xf0002004.. | both, in address order | a hand-kept fixture at placeholder addresses |
| `.../plat_mutants.py` (2) | GET_AS_PATH's and REBOOT's defects | the PHY's and the advertisement's | both tables; `mutants()` is #933's (it adds `phy_mutants`) | 117 defects: the train's 64 plus #933's 53 (41 at their base) |
| `.../test_plat_boot.cpp` (5) | REBOOT tests `Boot.B11..B23`, GET_AS_PATH `Boot.B24`; the fixture's GSI path window; `SetUp` through `fabric_from_reset` | PHY tests in a `Phy` fixture (`Phy.B11`, `Phy.B12`, `Phy.L1..L4`); the fixture's CTR counters window; `counters` reset in `SetUp` | both test sets, names as written (distinct fixtures); one `answer` serving GSI kind 2 and, once served, the CTR counters; `SetUp` calls `fabric_from_reset()` then resets `counters`; a two-line heading for the PHY entries in the index comment | each window answers as on its own side |
| `sw/firmware/gtest/coverage.ratchet` | per-file lines and branches | the same, its tree | regenerated by `fw_coverage.py --write` on the composed tree | a generated file; the train's figures were already behind its composed firmware (aecp.c 615 to 629 lines, srp_mbx.c 741 to 746), the tool records the whole tree |
| `sw/litex/ctrl_memory.py` (3) | the fixture's entry 59.5 (#897); REBOOT's history (#871) | the platform's two-interface entry 61.0, a new product entry `platform-8x8-one-interface` 56.5 (#919, #923's ruling) | #933's entries and `product_point`, the train's 59.5, both histories; the new entry's `ctrl_plat` at the ledger's 18,304 | `held == ledgers.HELD` needs both files to agree; sizes *provisional* |
| `.../ctrl_memory_ledger.py` (5) | FIXTURE rows at 59.5; sizes +128/+64/+64/+64 (#881) | PLATFORM rows at 61.0, PLATFORM_1, the product flag | #933's file with the train's FIXTURE moves; sizes the larger at each point, 17,664 / 19,136 / 18,304 / 20,416 | *provisional* |
| `.../test_ctrl_memory.py` (2) | 59.5 | #933's generic text, 61.0 and the product entry | #933's, at 59.5 | |
| `sw/firmware/ctrl/plat/README.md` (6) | REBOOT's port and tests, 64 defects | PHY rows, tests, 94 defects, the 8x8 images' entries | both; 117 defects; the 8x8 two-interface paragraph names every feature and both sides' measurements | prose; image figures restated after step 7 |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (4) | #897's and #871's history of the entries | #919's 61.0 and the product entry | both, chronological | prose; figures restated after step 7 |

## Step 6: #938 `81c9a1a0` (pending marks over the whole name id space, paced saves, #920); merge `13da58de`, fix `47f77284`

Merge base `70f4056f`. 5 files conflicted. Resolved and checked first in a throwaway worktree on `89eea108`; the lane's
merge and fix reproduce its trees exactly (`6542cb3b`, `81c3f39f`).

| File | Train's intent | #938's intent | Resolution | Why |
|---|---|---|---|---|
| `tb/verilator/ctrl_service_budget/grade.py` | `grade(..., interfaces, shape)` (#894, THE SHAPES) | `grade(..., interfaces, journal)` and `programmed()` (#920) | the merge: both parameters and `programmed()`; then the fix below | |
| `.../run.py` | passes `shape` | passes the group's journal | both arguments | |
| `sw/litex/ctrl_memory.py` (2) | the platform's two-interface entry 61.0 (#919), the product entry | `ctrl_plat` 128 B more (#920) | 61.0 at `ctrl_plat` 20,480; both histories | sizes *provisional* |
| `.../ctrl_memory_ledger.py` (2) | sizes 17,664 / 19,136 / 18,304 / 20,416 | 17,664 / 19,200 / 18,304 / 20,480 | the larger at each point, 17,664 / 19,200 / 18,304 / 20,480; docstring names #920 | *provisional* |
| `docs/design/SPLIT_CONTROL_MEMORY.md` (3) | the entries table at 59.5 / 61.0 / 56.5 | `ctrl_plat` of 20,480 | the table at the provisional sizes; two hunks word-merged | |

Composition fix `47f77284` (one commit after the merge): `grade.grade` would take seven parameters, one past
`check_py_idiom.py`'s `MAX_PARAMETERS` with its ratchet already full; `interfaces` and `shape` are read only as
`stated_at = shape or interfaces`, so they fold into one, `at`, and the four callers that gave both pass `shape or
interfaces` (`run.py`, `selftest_round.py` x3). `aecp_mutants.py` (1,002 lines) and `selftest_mutants.py` (1,005)
return to the 1,000-line limit by one rewrapped comment and five dict entries joined onto one line each; both ASTs are
identical before and after.

## Step 7: #931 `d06ded5a` (map edits through the EDIT window; SET_CONFIGURATION and SET_STREAM_INFO, #923, #924)

**STOPPED** (#665 issuecomment-6942842392): #933's `product_point` and #931's `own_point` require opposite behaviour of
`milan_soc.add_ctrl_memory` for the size fixture's and the platform's 8x8 two-interface images, and their memory tests
pin both. Merge base `16ba667d`; 15 files conflict on step 6. Resolved in scratch, waiting only on the decision:
`aecp.h` (both declarations), `aecp_face.h` (#931's EDIT port with the train's "random is the platform's"),
`test_aecp.cpp` (one fixture `answer`: GSI kind 2 the train's path, EDIT #931's transaction, every other window
`word()`; both test sets), `edit_rows.py` (#931's 1x1/1if and 8x8/2if one-row figures 295 and 355, the train's 305 and
8x8/1if row, *provisional* at 8x8/1if), `MAILBOX_SPLIT.md`, `FR_NFR.md` and the harness README (word-level merges).
Waiting on the decision: `milan_soc.py`, `ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`,
`plat_ledger.py`, section 5 of `SPLIT_CONTROL_MEMORY.md` and the plat README; `coverage.ratchet` comes from
`fw_coverage.py --write` at the merge.

## The recomposition on #914's new head `e1ecce20` (steps 2' to 6')

#914's two reviews at `8883d499` were NEGATIVE; its head moved to `d0a2a160` (R843-6 NEGATIVE) and then to `e1ecce20`
(R843-7 POSITIVE; R844-5 POSITIVE at its ancestor `d0a2a160`, whose later delta R843-7 covers). The first composition
is kept under `refs/ref/compose-on-914-8883d499` (`47f77284`); the branch went back to step 1 (`43b954e6`) and #914's new
head was merged as step 2'. #914 changed, between `8883d499` and `e1ecce20`, `ctrl_loop.h` (8x8/1if's
`CTRL_LOOP_TX_MS` 70 to 75 ms), `srp_mbx.c`, `srp_talker.cpp`, the harness's `flip_grade.py` (`tx_held`),
`load_grade.py`, `rows_grade.py`, `rows_tiers.py`, `selftest_mutants.py` (+13 lines) and four documents.

| Step | Conflicts | How resolved |
|---|---|---|
| 2' (#914 `e1ecce20`), merge `877c99e4` | the same 12 files | `git rerere` replayed 5 (`aecp/README.md`, `srp/README.md`, `edit_rows.py`, `notice_window.py`, `poll_grade.py`); `record_classes.py` is unchanged on #914's side, so step 2's resolution is taken whole; `ctrl_loop.h` composed as in step 2 on #914's new text (its 8x8/1if row at 75 ms; 1x1/1if at SRP unit 285 and TX 35); `rows_tiers.py`, `flip_grade.py` #914's as before; the harness README's record-classes paragraph is step 2's (both sides of that hunk unchanged); `FR_NFR.md`, `SPLIT_CONTROL_MEMORY.md` and the harness README's other hunk word-merged. Each recomposed file differs from step 2's resolution only by #914's own new changes (word diffs checked). |
| 3' (#918), 4' (#935) | as steps 3 and 4 | replayed by rerere, none left; step 3's fix `d7941d4d` applies unchanged |
| 5' (#933) | as step 5 | replayed by rerere; the plat README's defect count corrected again to 117 (rerere had recorded it before the correction); the coverage ratchet regenerated by `fw_coverage.py --write` on this tree, identical to step 5's |
| 6' (#938) | as step 6 | rerere replayed 4; `SPLIT_CONTROL_MEMORY.md` by `git merge-file` of step 6's resolved file with #914's new delta, no conflict |

Step 6''s fix differs from `47f77284`: #914 now adds 13 lines to `selftest_mutants.py`, so the union is 1,018 lines and
layout alone cannot bring it to 1,000. #938's five burst mutants and their one helper move to a new
`selftest_mutants_burst.py`, spread back into `MUTANTS` at the same place. The table's keys, order and values, and the
helper, are AST-identical before and after (272 entries). The five line-joins are dropped as no longer needed; the
`grade.grade` fold and the `aecp_mutants.py` rewrap stay.

# [A683zo] #665 lane S2b, round 30 (HANDOFF)

**Status: REVIEW READY** at `5bea2597ec514f0cde306e538261c6ddee66b456` (`665-s2b-cycles`), round 30 finished as ruled on the third STOP (#665 issuecomment-6842347916, section 11).
- **The rulings in the round:**
  - on round 29 (sections 1 to 7);
  - the first STOP, the fixture at 58.5 (section 8);
  - the second, the record mover's port (section 9);
  - the third, the stated costs (sections 10 and 11).
- **The firmware's stated costs** restated as ruled: `AECP_ROUND_COLD_US` 185 us at 8x8/2if (the margin exception, expiring at the 8x8/2if flip), and 1,010 / 430 us at 1x1/1if. The four triggers did not fire.
- **The re-grade:** 8x8/2if on fresh builds at `6c284a97`; 1x1/1if graded after the byte-compare; the tables from every leg's full tally.
- **The load:** 1x1/1if at 0.501 / 0.499 within 0.70. The flip check exits 1, as designed: 8x8/2if 0.822, and 1x1/1if R4 74.83 ms (#894).
- **The full pass, once at this head, on clean clones, every gate rc 0** but the flip check (section 11's table).
- Nothing pushed; no rebase, force or amend.
- REVIEW READY: #665 issuecomment-6848807388 (`REVIEW-READY-COMMENT.md`), 2026-11-13 10:2x CET.

The third STOP's status, as it stood:

**Status: STOP (third)** at `525375d649132fe82eb6e18ccdaad7cdb2c8982a` (`665-s2b-cycles`), after the ruling on the second STOP (section 9) and section 10's work.
- At the composed tree, two firmware-stated costs are under their measurement: `AECP_ROUND_COLD_US` at 8x8/2if (most measured 180.16 us against 165) and `CTRL_LOOP_BUILD_ONE_PASS_US` at 1x1/1if (40,700 cycles against 40,500).
- The firmware's own rule (heaviest plus 5 %, rounded up to 5 us) puts the cold cost at 190 us. There THE RETRY's search fails "the first notice at 2 interface(s): 28 ms over AECP_QUEUED_FIRST_MS", a bound round 30's item 5 holds unchanged.
- The legs ran at `da1869a3`, after two harness fixes that the merge's KLJ3 made necessary.
- Posted as #665 issuecomment-6838551181 (`STOP3-COMMENT.md`), 2026-11-13 00:1x CET; the receipts are `receipts/stop3-stated-costs/`.

The second STOP's status follows, unchanged:

**Status: STOP (second)** at `a4faefd46e6e41285077a0dbe90115ac416d0794` (`665-s2b-cycles`). The manager ruled on the first STOP: ledger the size fixture's 8x8/2if point at 58.5 (#665 issuecomment-6831583372). That is `a4faefd4`.

**The second STOP: the composed tree does not boot** (section 8). In the harness, no group boots at either point. The split boot simulation reports "mailbox contract mismatch". It passes at `dev-soft-core` `0fb66211` and at PR #892's `8bc1dfc0`.
- `0fb66211`'s `3ba76ae7` made `KL_mbx` ack a register read two cycles after the request.
- This branch's record mover, `KL_mbx_dma.sv`, still pairs the host port's ack with the request one cycle before.
- The fix is an RTL change, which this lane may not make.
- So the re-grade, the four cost controls and the full pass did not run.

The first STOP's status follows, unchanged:

**Status: STOP** at `187eeed89235d5ab7ce68bcd4953c7ef118e9245` (`665-s2b-cycles`). Items 1 to 3 are done and committed. Item 4's merge is done: one merge commit of PR #892's round 4 head `8bc1dfc0`, which carries live `dev-soft-core` `0fb66211`.

**The merge blocks the re-measure.** In the composed tree, the size fixture's 8x8 image with two interfaces plans **58.5 RAMB36**. The ruling holds that point at 58.0, and the owner's decision refuses it at 58.5 (finding F-FIX, section 6). So the CPU budget harness cannot build at 8x8/2if, and the re-grade, the cost controls and the full gate pass did not run at this head. That needs a decision; it is not mine to make.

Nothing was rebased, forced, amended or pushed. tsn-c-stack stays at `715589c`. No change to tsn-c-stack, lwSRP or any donor. I made no RTL or mailbox-contract change: the merge brings `dev-soft-core`'s own (`KL_mbx.sv`, `KL_mbx_rx.sv`).

- Authority:
  - the ruling on round 29 (#665 issuecomment-6828629878), items 1 to 6;
  - the owner decision of 2026-11-12 14:26 (#665 issuecomment-6824896581);
  - R711-8 (#810 issuecomment-6828561870) and R712-8 (#810 issuecomment-6828619213).
- TAKEN: #665 issuecomment-6828675905 (`TAKEN-COMMENT.md`), 2026-11-12 17:00 CET.
- STOP: #665 issuecomment-6831529450 (`STOP-COMMENT.md`), 2026-11-12 18:47 CET.
- The ruling on that STOP: #665 issuecomment-6831583372 (18:55 CET). The resumed session started at 20:42 CET, after the host's power-off at 19:20.
- The second STOP: #665 issuecomment-6834998091 (`STOP2-COMMENT.md`), 2026-11-12 21:2x CET.
- Base: `b2d39235ab9bba85d7e560b5f5f78fb4be528960` (round 29).
- Pin move head merged: `8bc1dfc0bbaa0d7a541a2e75951eff6d12fa6ea3`, from its REVIEW READY of 17:36 CET (#665 issuecomment-6829628610). I fetched it from the pin lane's checkout by its full SHA.
- **Output directory (a deviation).** This round writes to `665s2b-a683zo`, the session's own directory. The brief named `665s2b-a683zn`, which holds round 29's handoff and receipts, and both reviews cite them. Writing there would have overwritten them.

| Commit | Subject (short) |
|---|---|
| `cd87c3b2` | item 1: the platform entry at 60.0, refused at 60.5; the ledger's cases; the gate `plat_ledger.py` |
| `ef913ca4` | item 2: the SRP record cut's control held to this image's unplanted record, 5 % margin |
| `39b2968c` | item 3a: rule windows off the 2 ms grid; the "W less two records" control |
| `ab6325c8` | item 3c: `load_grade.py --check` refuses a column bound to the other's table |
| `267b9a14` | item 3b: driver test T7 and its plant |
| `a45f80ae` | item 3d: the ACMP expiry row names the pin move's kill through `also` |
| `e27a4540` | docs for items 1 to 3 |
| `86f60f8b` | item 3c: the binding controls planted from the gate's own tables (a planted one-column gate is refused, not raised) |
| `70e30d7b` | docs: section 13's control paragraph |
| `187eeed8` | item 4: the merge (parents `70e30d7b`, `8bc1dfc0`) |
| `a4faefd4` | the first STOP: the size fixture's 8x8/2if entry at 58.5, as ruled |
| `420d44e4` | the second STOP: the record mover holds its CPU request until `KL_mbx` answers it; the bench's two-cycle model, D11 and three plants |
| `9e6f0141` | the split boot links and plans the platform's 8x8/2if image under its own override |
| `cdc2742e` | docs: the host-port rule, the bench, D11, the split boot as a gate at every sync |
| `da1869a3` | the harness's flash device held to the flash map's journal (KLJ3 at `0xe40000`), with the flash test's set-span cases |
| `3e67f9ca` | a save held to KLJ3's container (its stage less the 10-byte record header `ctrl_nvm` names); the save bounds at 8x8 restated |
| `525375d6` | docs: the save's worst case on KLJ3's container in section 13 |
| `6c284a97` | the third STOP: `AECP_ROUND_COLD_US` 185 us at 8x8/2if with its margin exception; 1,010 / 430 us at 1x1/1if |
| `16eb95fc` | the AECP firm cap's test with room for one notice past the cap |
| `5bea2597` | the tables from every leg's full tally; section 13's re-grade, load and rows |

## 1. Outcome against the ruling

| Item | Outcome |
|---|---|
| 1. F1 (F-PLAT) | **Done.** The ledger entry is 60.0, refused at 60.5, stated as ROM debt owed to S14; the fixture stays 58.0 (refused at 58.5). Section 5 states the owner's decision with its link, in place of the superseded criterion and the "waits for a ruling" text. The new gate `tb/verilator/ctrl_split_boot/plat_ledger.py` links the platform image at all four points, each against its ledger: PASS at the head. Its seven planted ledgers are graded as required (7 of 7), and two plants fail the gate end to end (rc 1): round 29's 59.0 and a stale key |
| 2. F2 (F-CTL) | **Done, option (c).** One run measures `notice-every-2` on the planted build and on this tree's unplanted image. The control is caught only where the planted heaviest SRP record apply is more than 5 % dearer. Caught: 35,908 against 32,866 cycles (+9.3 %), rc 0. The table rule is unchanged and no stated cost is lowered. The README passage (round 29's `:1409-1413`, now `:1422-1427`) and section 13's (round 29's `:2168`, now `:2275`) are rewritten, and true of round 29's image |
| 3. Suggestions | **Done.** S1: rule windows at each solved row's W and either side of the refill at R4's bound plus its record; the "W less two records" plant is refused by a rule finding. R712-8 S2: T7 and its plant (caught). S5: `--check` itself refuses swapped columns (rc 1 end to end). S7: `also` names the pin move's kill test, at the words it fails on at the composed tree (C9's, not C5's: section 6) |
| 4. Sync | **The merge is done; the re-measure is blocked.** PR #892's head moved to `8bc1dfc0` and its REVIEW READY was posted at 17:36. I merged it at about 17:50 with one merge commit; eleven conflicts, each resolved from the composed tree (section 2). `ctrl_plat` was re-measured at the four points (unchanged: 17,472 / 19,008 / 18,112 / 20,288 B) and the platform plans 59.5, within 60.0. **The fixture's 8x8/2if image plans 58.5** (F-FIX): **STOP** |
| 5. Unchanged | Unchanged: the bounds, the every-source rule, the tiers, THE DRAIN and `RETAINED_ROWS` |
| 6. Elsewhere | Not mine: S3/S4 go to #894; F-HOOKS and R711-7 S2 get issues; S6 is the manager's |

## 2. Changes (file:line at the head, reason)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `cd87c3b2` | `sw/litex/ctrl_memory.py:243-262` | `LEDGERED["platform-8x8-two-interfaces"]` at 60.0. Its `owed` names the decision and the 4.0 RAMB36 owed to S14. The comment above states both caps (58.5 and 60.5) and names the gate | item 1 |
| `cd87c3b2` | `sw/litex/ctrl_memory_ledger.py:6-12`, `:49-52`, `:64-72`, `:127-129` | `OWN`, `HELD`, `REFUSED` and `planted()` at 60.0 / 60.5 (the fixture's plant at "the platform's 60.0") | item 1: the ledger's own cases move with the entry |
| `cd87c3b2` | `sw/litex/test_ctrl_memory.py:232-238` | `ledger_elf`: two tiles of `.text` more and of `.bss` less, so a case reaches 61.0 | The 60.5 case did not fit the 56-tile `sram` region ("outside regions"): 35 failures before, PASS after (`receipts/item1-platform-ledger/test_ctrl_memory-1.log`, `-2.log`) |
| `cd87c3b2` | `tb/verilator/ctrl_split_boot/plat_ledger.py` (new, 295 lines) | `POINTS` (`:61`); `build`/`link`/`maps` (`:80-110`); `grade_point` LINK/KEY/TILES apart (`:123-154`); `grade` with LEDGER (`:157-174`); `CONTROLS` (`:218-238`); `--self-test`, `--controls`, `--regrade` | item 1: the gate, with its planted controls |
| `cd87c3b2` | `sw/firmware/ctrl/test/ctrl_configs.py:179-183` | `OUTSIDE` entry for `plat_ledger.py` | The firmware-boundary gate refuses an unclassified program that names the firmware's tree |
| `ef913ca4` | `tb/verilator/ctrl_service_budget/poll_items.py:120-137` | `CONTROLS` without the SRP cut; `REFERENCE_CONTROLS`; `REFERENCE_MARGIN_PERCENT = 5` | item 2 |
| `ef913ca4` | `build.py:117-119` | `REFERENCE_CONTROLS` | item 2 |
| `ef913ca4` | `run.py:593-645`, `:761-762` | `reference_run`: the control's group on this tree's unplanted image, built (or reused, checked) in `<build-dir>/reference`. `reference_verdict` (4 parameters): caught past the margin, with no refusal in either run | item 2 |
| `ef913ca4` | `selftest_polls.py:135-190`; `selftest_mutants.py:796-810` | four checks and six grader mutants | item 2: each mutant caught by its named check (`receipts/interim/harness_selftest-i1.summary.txt`) |
| `39b2968c` | `rows_grade.py:338-354`, `:364` | `BOUNDARY_US`, `rule_windows` (RULE_WINDOWS, each solved row's W, 20 ms + R4's record ± 1 us) | item 3, S1 |
| `39b2968c` | `flip_grade.py:162-183`, `:233-235` | the control "SRP's arrivals cut by two records of AECP", refused by name, no movement required (`None`) | item 3, S1: it moves no row at this head |
| `ab6325c8`, `86f60f8b` | `load_grade.py:174`, `:344-354`, `:363`, `:511-529` | `BOUND`; `unbound()` in `findings()` (so in `--check`); `binding_controls()` planting from the constants | item 3, S5; R711-8's one-column probe raised `IndexError` before `86f60f8b` |
| `267b9a14` | `sw/firmware/ctrl/test/test_mbx_dma_driver.cpp:45-49`, `:443-468` | T7 | item 3, R712-8 S2 (IEEE 1722.1-2021 7.5.2; `aecp.h` REFUSED) |
| `267b9a14` | `sw/firmware/ctrl/test/mbx_dma_mutants.py:56-62` | `mover-fan-end-refuses-before-the-last-frame-is-committed` | item 3: T7 must fail it |
| `a45f80ae` | `sw/firmware/ctrl/test/acmp_mutants.py:783-785` | `also` with `AcmpMailbox.C5ToC9TimerPathsAreServedInThePassThatTakesTheExpiry` on "C9 TMR_NO_TK, the run's first draw -> TMR_DELAY armed" | item 3, S7 |
| `e27a4540`, `70e30d7b` | `docs/design/SPLIT_CONTROL_MEMORY.md`: section 3 `:132`, `:140-142`; section 5 `:263-272` (the decision); `:345` (round 29's head); section 6 `:487`, `:501-507`; section 13 `:2227` (rules), `:2275` (the control), `:2287` (T7), `:2291` (the re-grade paragraph) | the decision; the gate; the control; the windows; T7 | items 1 to 3 |
| `e27a4540` | `tb/verilator/ctrl_service_budget/README.md:132`, `:152`, `:1137`, `:1336-1341`, `:1422-1427`, `:1428-1429` | `--check`'s binding; `rule_windows`; the reference control and its self-test checks and mutants; the controls lists | items 2, 3 |
| `e27a4540` | `tb/verilator/ctrl_split_boot/README.md:124-145` (new section, Contents); `sw/firmware/ctrl/plat/README.md:136`; `sw/firmware/ctrl/README.md:482` | the gate; the platform at 59.5 within 60.0; T7 | items 1, 3 |
| `187eeed8` (merge) | `sw/firmware/ctrl_nvm/nvm_store.c:881-890` | `nvm_mark(id)`: S2b's mark by id with no walk (`nvm_rec_id_of`, `nvm_rec_id_known`), on KLJ3's counted open set (`nvm_open_set(&nvm.dirty, id)`) | the composed tree: both sides' behaviour |
| `187eeed8` | `sw/firmware/ctrl_nvm/test/nvm_mutants.py:396-397` | `budget_rearmed_by_change` anchored on the composed line | the composed tree |
| `187eeed8` | `sw/firmware/ctrl/plat/ctrl_split_hot.txt`, `ctrl_split.ld` | `nvm_store nvm_any` dropped from both | KLJ3's `nvm_any` is `v->count != 0u`, which the compiler inlines. The composed image's link refused the name ("hot-list name ... is no section"). `ctrl_hot.py --check`: 206 entries |
| `187eeed8` | `sw/litex/ctrl_memory.py:251-258`; `ctrl_memory_ledger.py:31`, `:35` | both entries keyed on `nvm_stage` 13,594 B (KLJ3); `ctrl_plat` 20,288 B; platform 60.0, fixture 58.0; `STAGE_*` 3,454 / 13,594; `PLAT_*` unchanged | measured at the four points on the composed tree (`receipts/merge/plat_ledger-merge.log`). The fixture's `owed` carries the decision without a new comment ID |
| `187eeed8` | `sw/firmware/gtest/coverage.ratchet` | through `fw_coverage.py --write` on the composed tree (39 files) | the generator (`receipts/merge/fw_coverage-write-merge.log`) |
| `187eeed8` | `tb/verilator/ctrl_service_budget/split_soc.py:480-493` | the docstring: #791's region pieces and S2b's clock domain | both sides' facts |
| `187eeed8` | `sw/firmware/gtest/README.md:324-328`; `sw/firmware/ctrl_nvm/README.md:261-262`; `tb/verilator/ctrl_service_budget/README.md:1451` | S2b's SRP row and KLJ3's store rows (both mark entry points); KLJ3's multi-block erase with S2b's 128-byte read-back (`NVM_READ_BYTES`, the composed code); `as-built` with dev's words | both sides' facts, each against the composed code |
| `187eeed8` | `docs/design/SPLIT_CONTROL_MEMORY.md:38-40`, `:137-138`, `:288` (both sides' paragraphs), `:441-470`, `:546-547` | the split has no `main_ram` and its flash window is uncached and not executable (both true of the composed `milan_soc.py:3518-3537`, `:3686-3689`). The table keyed on 13,594 B. S2b's face-writer ledger and KLJ3's paragraph, both. The pin branch's own measurements labelled as that branch's. **This head's table and F-FIX** (`:456-467`) | the composed tree |

## 3. New checks, planted mutants and failing words

| Check | Planted defect | Refused with |
|---|---|---|
| `plat_ledger.py` (gate) | `stale-key` (ctrl_plat 64 B short) | `KEY 8x8-if2: ... lists {... 'ctrl_plat': 20224}, the image carries {... 20288}` and `LINK` |
| | `past-its-tiles` (tiles half a tile under the plan) | `TILES 8x8-if2: 59.5 RAMB36 past the 59 its override ledgers` and `LINK` |
| | `stale-key-past-its-tiles` (both) | `KEY`, `TILES` and `LINK`: the stale key does not hide the overrun |
| | `stale-record` (`PLAT_1X1_1` − 64) | `KEY 1x1-if1: ctrl_memory_ledger.PLAT_1X1_1 records 17,408 B, the image carries 17472` |
| | `budget-under-a-point` | `TILES 8x8-if1: 53 RAMB36 past the 52.5 budget` |
| | `override-not-taken` | `LINK`, `TILES 8x8-if2 ... past the 56 budget` and `LEDGER: ['platform-8x8-two-interfaces'] ... linked at no point` |
| | `override-unlinked` | `LEDGER: ['platform-8x8-one-interface'] ... linked at no point` |
| | end to end: `ctrl_memory.py` at round 29's 59.0 | rc 1, `plat_ledger: FAIL (2 finding(s))`, `TILES 8x8-if2: 59.5 RAMB36 past the 59` |
| | end to end: the entry's `ctrl_plat` at 20,224 | rc 1, `KEY 8x8-if2: ...` |
| `run.reference_verdict` (harness self-test) | `polls: a reference control held to no margin` | "the SRP record cut's control is held to this image's unplanted SRP record, not to a stated cost, with a margin of 5 %" |
| | `... read against its own planted run` | "a reference control is caught by a planted record more than its margin dearer than the unplanted one, and escapes at the margin, at the same cost and cheaper" |
| | `... refusals ignored` | "a reference control escapes with a refusal in either run, or without its group in either" |
| | `... other run without its variant`; `... in the planted build's place` | "a reference control's other run is its group alone on this point's unplanted image, at its variant and core, in the build directory's reference" |
| | `polls: the SRP record cut's control held to its stated cost` | the first check, by name |
| the control itself | `srp-compared-by-memcmp` on round 29's image | `CONTROL srp-compared-by-memcmp caught: notice-every-2's heaviest record 35,908 CPU cycles planted against 32,866 on this image unplanted, more than 5 % dearer`, rc 0 |
| `rows_grade.rule_findings` (flip self-test, 132 of 132) | `SRP's arrivals cut by two records of AECP` | `1x1/1if R4: 41 SRP records ahead in 20.206 ms, not the 42 ...` (and 8x8/2if at 20.266 ms); 1x1/1if's R4 stays 66.12 |
| `load_grade.py --check` | end to end: `COLUMNS` swapped | rc 1, `OVER a column's name bound to the other's table, or a column not the gate's: [('at the pin', 'STATED_US_DONOR'), ...]`, `RESULT: FAIL` |
| `binding_controls` (load self-test, 25 of 25) | swapped, the donor's column dropped, an equal copy of the donor's table | each refused by `findings()` |
| T7 | `mover-fan-end-refuses-before-the-last-frame-is-committed` | "T7 the last frame is committed before REFUSED, and no completion is kept" (1 of 1, also at the merge head) |
| `acmp-expiry-reads-the-clock-twice` with `also` | (the existing plant) | `AcmpCore.TimerPortBudgets` "timer clock budget for state PRB_W_DELAY" and `AcmpMailbox.C5ToC9...` "C9 TMR_NO_TK, the run's first draw -> TMR_DELAY armed" (1 of 1, also at the merge head) |

The reviewers' probes, re-run at the merge head (`receipts/item3-suggestions/`):
- R711-8's `probe_rules.py`: "srp window less two records ... rule_findings 1"; the swapped columns are refused by `--check`; the one-column plant is refused, not raised.
- R712-8's `rule_probes.py`: every plant REFUSED except "retries not capped by passes". Both reviewers called that one equivalent: passes exceed floor(W/10)+2 at every window.
- R712-8's `columns_probe.py`: every wrong binding is refused.

## 4. Measurement at the merge head

Both images were built alike on a clean clone of `187eeed8`, one runtime and each shape's own split export (`receipts/item1-platform-ledger/plat_ledger-head.log`, `receipts/merge/fixtures-head/`):

| Point | Fixture `rom` / `sram`, B | Fixture RAMB36 | Platform `rom` / `sram`, B | Platform RAMB36 | `ctrl_plat`, B |
|---|---:|---:|---:|---:|---:|
| 1x1/1if | 108,600 / 45,920 | 38.5 | 113,672 / 46,880 | 39.5 | 17,472 |
| 1x1/2if | 110,304 / 57,312 | 41.0 | 115,400 / 58,336 | 43.0 | 19,008 |
| 8x8/1if | 122,136 / 87,008 | 51.5 | 127,256 / 87,984 | 53.0 | 18,112 |
| 8x8/2if | 123,808 / 113,168 | **58.5, refused at its 58.0** | 128,960 / 114,160 | 59.5, within 60.0 | 20,288 |

The harness's own 8x8 build refuses at the same plan (`receipts/merge/harness-8x8-build-head.log`): "REFUSED: allocation over budget: 58.5 RAMB36 (rom 123808 bytes in 124928, sram 113168 bytes in 114688) exceeds the 58-RAMB36 budget ledgered for 8x8, two interfaces".

**The legs were not re-graded.** The merge does move measured costs: `dev-soft-core`'s mailbox RTL "Answer[s] a mailbox register read a cycle later" (`3ba76ae7`), and KLJ3 changes the store and its stage. A re-grade at both points is owed once the fixture's 8x8/2if point builds. The load gate at this head still reads round 29's tables: 0.486 / 0.483 at 1x1/1if, rc 0 (`receipts/item3-suggestions/head-load_check.log`). These are round 29's costs, not this image's.

## 5. Gates run (STOP: the full pass was not run)

| Gate | Where | Result |
|---|---|---|
| `plat_ledger.py --self-test` | clean clone of `187eeed8` | rc 0; 4 of 4 points PASS; 7 of 7 controls as required |
| the fixture at the four points | clean clone of `187eeed8` | 3 linked; 8x8/2if refused at 58.5 (F-FIX) |
| `test_ctrl_memory.py` | clean clone of `187eeed8` | `RESULT: PASS` |
| `load_grade.py --check`, `--selftest`; `flip_grade.py --selftest` | clean clone of `187eeed8` | rc 0: PASS 0.486 / 0.483; 25 of 25; 132 of 132 |
| `ctrl_service_hooks/run.py --self-test` | clean clone of `187eeed8` | 28 of 28 checks, 96 of 96 mutants |
| the round's plants (`acmp-expiry...`, T6's, T7's) | clean clone of `187eeed8` | 3 of 3 caught |
| `test_ctrl_firmware.py --require-rv32` | the merge's working tree | `test_ctrl_firmware: PASS` |
| `test_ctrl_nvm.py --require-rv32` | the merge's working tree | "OK across 5 shape(s), 526 tests" |
| `ctrl_hot.py --check`; idiom gates; `check_baremetal_only.py`; `docs_check.py` | the merge's tree | rc 0; 206 entries; 0 findings |
| `run.py --self-test` (harness) | clean clone of `e27a4540` (items 1 to 3) | `self-test: 0 failures`, 213 mutants caught |
| `fw_coverage.py --check` | clean clone of `e27a4540` | `firmware coverage: PASS (39 files)` |
| `run.py --self-test` (harness) | clean clone of `187eeed8` | `self-test: 0 failures`, 213 mutants caught (`receipts/merge/head-harness_selftest.summary.txt`) |
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | clean clone of `187eeed8` | "OK across 5 shape(s), 526 tests, and all 144 planted defects reddened", the re-anchored `budget_rearmed_by_change` among them |
| Not run, owing to the STOP | | the workflow jobs, the full mutant campaigns, the legs at both points, the four cost controls at the merge head, `test_builder.py`, `behave`, the split boot runs, the sweep |

## 6. Findings, deviations and open questions

- **F-FIX, the blocker (from the merge, not from either side alone).** The composed size fixture's 8x8/2if image plans 58.5 RAMB36: `rom` 123,808 B in 124,928 and `sram` 113,168 B in 114,688. The ruling holds it at 58.0, and the owner's decision caps it at 58.5, which the ledger refuses.
  - S2b's `rom` already took 61 granules at round 29 (123,112 B), with its `sram` 64 B under 55 granules (112,576 in 112,640).
  - KLJ3's stage and open bits add about 590 B of `sram` (#823's own table: +576 B at that point), so `sram` takes a 56th granule.
  - The pin branch's own composed fixture is at 58.0 because its `rom` (121,064 B) takes one granule fewer.
  - **Ways back to 58.0:** cut 928 B of `rom` (to 122,880) or 528 B of `sram` (to 112,640). Either is a firmware change outside this round's scope. The other way is a ledger decision past the owner's cap.
  - The tree states the overrun (section 5, `:467`). The entry stays 58.0 and the image is refused by name.
- **The legs and costs at the merge.** `dev-soft-core`'s mailbox answers a register read a cycle later, and KLJ3 changes the store, so the merge moves measured costs. The re-grade at both points is owed after F-FIX. So are the four cost controls at the merge head, including the SRP control's re-run.
  - Section 13 says the SRP control is caught on round 29's image (`ef913ca4`), and that this head's 8x8/2if builds are refused.
- **The C5 needle (S7).** At the composed tree, the expiry plant fails #892's kill test at its C9 line, not C5's: C5 reads "35 accesses (bound 35)" under the plant (`receipts/item3-suggestions/plant-arm-acmp.log`). So the `also` row names the test at C9's words. A row with C5's words escaped (`plant-acmp-expiry.log`, rc 1) and was not committed.
- **S1, exactly.** No solved row's W sees the one-record error alone at this head. At 1x1/1if's R4 (66.12 ms), W less one record and W less two both hold 32 SRP refills (65.915 and 65.71 ms over 2 ms). So the boundary windows, a microsecond either side of 20 ms plus R4's record, are what refuse it. Both are in `rule_windows`, beside each solved W.
- **R712-8's "retries not capped by passes"** still escapes: an equivalent plant, as both reviewers found.
- **Deviation: the output directory** (see the status).
- **Deviation: a cache directory removed.** `sw/firmware/ctrl/test/__pycache__` in the lane checkout (git-ignored) held my runs' bytecode and earlier files from 04:56. I removed it whole after listing it; it is regenerated on import.
- **Placement.** Every CPU range was booked all round (`cpu_ranges.py`: "busy 128 cpus"), so everything ran on the session pool 96-127. MemAvailable stayed above 45 GB.

## 7. Run history (CET)

- 16:58 start; origin and head `b2d39235` verified; the handoff, R711-8, R712-8, the ruling and the decision read.
- 17:00 TAKEN posted (#665 issuecomment-6828675905).
- 17:00 to 17:12 item 1, with the gate's first run (83 s, 4 of 4 PASS, 7 of 7 controls).
- 17:12 to 17:18 item 2; `cd87c3b2`, `ef913ca4`; the control launched on a clean clone.
- 17:18 to 17:31 item 3: `39b2968c`, `ab6325c8`, `267b9a14`, `a45f80ae`, and the docs `e27a4540`. The harness self-test and the coverage check started on a clean clone of `e27a4540`.
- 17:33 to 17:44 the reviewers' probes; `86f60f8b`; the control caught (17:44); `70e30d7b`.
- 17:46 PR #892's head `8bc1dfc0` and its REVIEW READY (17:36) found; `0fb66211`'s RTL, store and harness changes read.
- 17:48 to 18:05 the merge: eleven conflicts resolved; the ratchet through its generator; the hot list's `nvm_any`; the platform at four points; the fixture at 58.5 (F-FIX).
- 18:05 to 18:15 the store gate, the firmware test, the memory test; the merge committed (`187eeed8`).
- 18:15 to 18:30 the clean-clone evidence at `187eeed8`, the end-to-end plants, the receipts; this file, `PR-BODY.md` and the STOP comment.
- 18:26 the harness self-test at `187eeed8`: 0 failures; 18:45 the store self-test there: 144 of 144. The receipts scrubbed and indexed; STOP posted.

## 8. The resumed session (after the ruling on the first STOP)

**The ruling** (#665 issuecomment-6831583372): ledger the size fixture's 8x8/2if point at 58.5, within the owner's cap, as ROM debt owed to S14; section 5 states it with the link, and says the cap is fully used. Then finish round 30: the re-grade at both points, the four cost controls, the full pass, REVIEW READY. PR #892 has a round 5 head since, `6eacd76d`, a documentation commit on `8bc1dfc0`. It is not merged here: the ruling names round 4's head, and the brief allows no other merge.

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `a4faefd4` | `sw/litex/ctrl_memory.py:244-258` | the fixture's entry at 58.5; its `owed` gives the half tile as ROM debt owed to S14 on top of the 58.0 allowance, 528 B of `sram` past 55 granules; the comment gives each image's refusal (59.0 and 60.5) | the ruling |
| `a4faefd4` | `sw/litex/ctrl_memory_ledger.py:7`, `:49-51`, `:57-63`, `:76`; `test_ctrl_memory.py:21`, `:334` | the fixture's cases at 58.5, refused at 59.0 | the ledger's own cases move with the entry |
| `a4faefd4` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 3 (`:137`, `:142-143`), section 5 (the ledger line, the arm's granule, this head's table, the F-FIX paragraph), section 6; `tb/verilator/ctrl_service_budget/README.md:49`, `:245`; `sw/firmware/ctrl/plat/README.md:110` | the ruling with its link; "the cap is now fully used: any further growth at that point ... is a STOP"; the platform's 59.5 | the ruling |

Checks at `a4faefd4`:
- `test_ctrl_memory.py`: PASS, "the 8x8-two-interfaces override plans its own point's image: 58.5 RAMB36".
- The fixture links at the four points: 38.5 / 41.0 / 51.5 / 58.5, all rc 0 (`receipts/resume-mover-ack/fixtures-585/`).
- `fw_coverage.py --check`: PASS, 39 files, on a clean clone.
- The docs check: 0 findings.

**The re-grade and the controls (stopped).**
- I launched on clean clones of `a4faefd4`, on booked ranges (0-63), at about 20:47:
  - GA8 and GA1, every group of arm A, 14 jobs each;
  - GN8 and GN1, the `answering-every-port` arm;
  - GB8 then GB1, arm B's `aecp` group;
  - the four cost controls.
- Three builds failed in seconds as they started together. Two collided in the CPU generator's sbt server, and one read a half-written netlist. Each was cleared and restarted alone.
- **No group booted.** At about 21:12, every running group was still at the PC after `main` returns (`receipts/resume-mover-ack/harness-groups-at-a4faefd4.txt`). I stopped all the units. Round 29's GB8 took 250 s in all.

**The cause** (`receipts/resume-mover-ack/rtl-excerpts.txt`, `boot-*.log`):
- The split boot simulation at 1x1:
  - at `a4faefd4`: FAIL, "Milan split: mailbox contract mismatch; entity disabled";
  - at `dev-soft-core` `0fb66211`: PASS;
  - at PR #892's `8bc1dfc0`: PASS;
  - at round 29's head it passed (round 29's lane gates).
- The fixture's `main` returns from `ctrl_app_open` → `ctrl_loop_open` → `mbx_open`, whose `caps_match` of the ID and CAPS reads fails. `_start`'s `jal main` is followed by `j 5c`, and every log's PC sample sits at `0x5c`.
- `dev-soft-core`'s `3ba76ae7` (it arrives with PR #889's merge `38967e26`; it is not in round 29's tree) changed `KL_mbx`'s host port: a register read now acks two cycles after its request, any other access one.
- `KL_mbx_dma.sv`, the record mover on that port between `KL_mbx_wb` and `KL_mbx`, exists only on this branch. It still pairs an ack with the CPU by the request one cycle before: `ack_cpu_r <= cpu_issue_w`, `cpu_ack_o = host_ack_i && ack_cpu_r`.
- No gate saw it:
  - the mover's own bench (`tb/verilator/mbx` `run-dma`) drives a model host port;
  - the mailbox co-simulation has no mover;
  - the pin move has no mover, and its round 4 did not run the harness or the split boot;
  - this branch's merge commit ran neither before the re-grade started.
- **The fix is an RTL change**: `KL_mbx_dma.sv` holding an outstanding register read until its ack, with a bench case for a two-cycle register read and its plant. The lane's brief forbids RTL changes, and the fix would bring the RTL gates and the sweep into the round: STOP.

**Run history (CET, resumed):**
- 20:42 resumed; the tree clean at `187eeed8`; the ruling read.
- 20:44 `a4faefd4`.
- 20:47 the legs, controls and coverage check launched.
- 20:50 to 20:58 the three failed builds restarted one at a time.
- 20:55 coverage PASS.
- 21:05 to 21:12 no group finished; the logs read; the units stopped.
- 21:12 to 21:22 the diagnosis: the split boot at three heads; the RTL and firmware read.
- 21:2x this section, the receipts, `STOP2-COMMENT.md`.

## 9. After the ruling on the second STOP (the record mover's port)

**The ruling** (#665 issuecomment-6835550732, 21:48 CET): the fix stays in this lane.
1. The mover tracks an outstanding CPU request until its ack, for one- and two-cycle answers alike, with the rule derived from `KL_mbx`'s port as merged.
2. The mover's bench gets a two-cycle register-read case, and a plant restoring the one-cycle routing must fail it.
3. A new gate: the split boot at both points, at every sync.
4. The RTL gates the change touches.

Then round 30 finishes as ruled.

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `420d44e4` | `hdl/milan/mailbox/KL_mbx_dma.sv:78`, `:158`, `:185-193`, `:200-201`, `:212`, `:240`, `:271`, `:404-407` | `ack_cpu_r` (the port's request last cycle was the CPU's) becomes `cpu_wait_r`, "a CPU request is with KL_mbx: issued, its answer not yet taken", updated `cpu_issue_w \|\| (cpu_wait_r && !host_ack_i)`. `cpu_ack_o = host_ack_i && cpu_wait_r`, and the mover's requests and beats (`fill_req_w`, `beat_w`, `mover_w`, `axi_rready_o`) wait while it is set, the answer's cycle included | item 1. `KL_mbx`'s port as merged: "a host access this cycle, none until its answer", answered "1 cycle after host_req_i, 2 for a register read". No latency is coded: the bit ends at the ack, however long it takes. The mover's own requests are ring reads and writes, which that port answers the cycle after. The flop count is unchanged (the same one flop, its next state one AND-OR more) |
| `420d44e4` | `tb/verilator/mbx/dma_main.cpp:4-11`, `:53-59`, `:75-87`, `:120-124`, `:210-246`, `two_cycle()` | the host model follows the merged port: a read outside the event ring and the bench's two rings is a register read, answered two cycles after its request, everything else the cycle after. Every request is checked against the port's rule, none while one awaits its answer, the answer's cycle included. D11: a CPU register read answered at two cycles with its own word, alone, held behind a transfer and in the cycle a transfer starts; a ring read at one cycle | item 2. The bench's CPU accesses (words 2 to 7) are register reads, so D4, D8 and D10 take the two-cycle path too |
| `420d44e4` | `tb/verilator/mbx/dma_mutants.py` | `ack-misrouted` and `fill-during-cpu-answer` re-anchored on `cpu_wait_r`. New: `cpu-answer-one-cycle` (the one-cycle routing: `cpu_wait_r <= cpu_issue_w;`), `beat-during-cpu-answer`, `mover-during-cpu-answer` | item 2: 24 of 24 caught |
| `420d44e4` | `tb/verilator/mbx/Makefile:155-159` | `DMA_VFLAGS` drops `-GBENCH_P=1` | the merge's `VFLAGS` carry `0fb66211`'s `tb_mbx_top` parameter, so `make run-dma`, and the suite's `dma-mutants`, refused to build at the merge ("Parameters from the command line were not found in the design: BENCH_P") |
| `9e6f0141` | `tb/verilator/ctrl_split_boot/boot_soc.py` (`PLATFORM_LEDGERED`, the plan under `split_soc.ledgered_plan`), `run.py:195-206` | the boot links the platform's 8x8/2if image with `--ledgered-point platform-8x8-two-interfaces` and plans its SoC to that override's tiles; every other point takes none | item 3: the boot runs at both points |
| `cdc2742e` | `tb/verilator/mbx/README.md:27-41`, `docs/design/MAILBOX_SPLIT.md:299-311`, `docs/design/SPLIT_CONTROL_MEMORY.md:1133-1135`, `tb/verilator/ctrl_split_boot/README.md` ("A gate at every sync") | the port rule, the bench's model and D11, and the gate | docs |

**Checks at the fix:**
- The mover's bench at `420d44e4`: `checks: 520041 failures: 0`.
- `make dma-mutants`: 24 of 24. The one-cycle plant fails nine checks, among them "D11 a CPU register read is answered two cycles after its request, with its own word", "D11 no request reaches the port while one awaits its answer", "D4 a CPU access is answered" and "D8 after a reset the port is the CPU's".
- `lint_rtl.py --check`: PASS (89 <= ratchet 89).
- The interim mailbox suite at `cdc2742e`: every arm PASS, cosim 32 checks, Wishbone 553, AXI4-Lite 598, host model 490; the mover's plants 24 of 24, the mailbox's 12 of 12.
- The split boot on a clean clone of `9e6f0141`: PASS at 1x1/1if (ready at 26.370 ms), 8x8/1if (66.017 ms) and 8x8/2if (68.371 ms).
- Arm B's `aecp` group at 8x8 boots and grades: GB8, 0 refusals, 0 of 39 misses.

**Note on the last line above.** That GB8 ran at `9e6f0141`. Arm B's `aecp` group saves nothing, so it did not reach the journal check of section 10. GB8 ran again at `da1869a3`: 0 refusals, 0 of 39 misses, rc 0.

## 10. The re-grade at the merge: two harness fixes, then the third STOP

**The legs at `9e6f0141` were invalid.** Every group that saves failed "FAIL: flash write escaped the journal" (`receipts/rtl-fix/journal-bound/at-9e6f0141-GA1-*.tail.txt`).
- The budget harness's flash device (`tb/verilator/fw_service_budget/flash.hpp`, shared with the older harness) took writes only in `0xee0000..0xf00000`, KLJ2's journal.
- The merge's KLJ3 store (#823) writes `journal_klj3`, 640 KiB at `0xe40000` (`sw/litex/milan_soc.py:184`), and only reads KLJ2's two headers.
- `build.py` already wrote the flash map's journal into `budget_config.hpp` (`journal_offset`, `journal_size`). The device's check and the journal-read trace (`sim_main.cpp`, `journal_base`/`journal_end`) still held the old constants.

I stopped queue 31's units (the legs, the controls, the dispatcher) and fixed the harness. Then I relaunched everything on clean clones of the fix (queue 32).

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `da1869a3` | `tb/verilator/fw_service_budget/flash.hpp:75`, `:113-121`, `:136-137` | The write check reads `journal_lo_`/`journal_hi_`. `journal(offset, size)` sets them, refusing a span that is not whole erase blocks inside the medium. The default stays KLJ2's window, which this older harness's media lay out | The split store's journal is KLJ3's. The older harness keeps its own layout, unchanged |
| `da1869a3` | `tb/verilator/ctrl_service_budget/sim_main.cpp:86-88`, `:270-271`, the removed `journal_base`/`journal_end` | `Bench` sets the device's journal from `budget_config.hpp`; the `FLASHRD` read runs are the reads inside it | The flash map is the one source of the journal |
| `da1869a3` | `tb/verilator/fw_service_budget/flash_test.cpp:67-93` | A set journal takes its last page and refuses the bytes past and before it, and a span off an erase block is refused | The new span's own test |
| `da1869a3` | `tb/verilator/ctrl_service_budget/README.md:115` | The journal is the flash map's; the refusal's words | docs |
| `3e67f9ca` | `tb/verilator/ctrl_service_budget/save_window.py:80-98` | `rec_hdr()` reads `NVM_REC_HDR` from `nvm_shape.h` through the name it defines (`NVM3_REC_HDR`, 10, `nvm_layout3.h`), refusing a name defined other than once. `container()` subtracts it in place of the constant 8 | KLJ2's header was 8 bytes, KLJ3's is 10. A 1x1 save programmed 3,444 bytes and was refused against 3,446 |
| `3e67f9ca` | `tb/verilator/ctrl_service_budget/selftest_share.py:394-396` | A check that the header read is 10 | so a changed header restates the container, and a plant of 8 fails |
| `3e67f9ca` | `tb/verilator/ctrl_service_budget/README.md:108-109`, `:112` | The save bounds on KLJ3's containers: 12,470 ms at 8x8 (382 steps of 13,584 B), 4,070 ms at 1x1 (102 of 3,444); in flight 22,870 ms (380 and 382) and 6,070 ms | `save_window.bound_ms` at the build's containers |
| `525375d6` | `docs/design/SPLIT_CONTROL_MEMORY.md:1609-1610`, `:1822` | The same in section 13: S = 1 + 3 + 54 + 2 + 107 + 108 + 107 = 382 | docs |

The groups' scripts do not change: the step count at both points is the same under either header, so the legs' recorded scripts stay valid for a re-grade.

**New checks, their plants and failing words.**

| Check | Plant | Failing words |
|---|---|---|
| `flash_test.cpp`'s set-span cases (run by `fw_service_budget/run.py --self-test`) | the device's check back on `0xee0000`/`0xf00000` | "[FAIL] last page of a set journal taken", "[FAIL] last page of a set journal programmed got=0xff exp=0xa5", "[FAIL] write past a set journal refused" (3 of 19) |
| the harness end to end | `9e6f0141`, without the device's span | "FAIL: flash write escaped the journal" in every saving group (`receipts/rtl-fix/journal-bound/`) |
| `selftest_share.py`'s header check | `NVM3_REC_HDR 8u` in a copy of the tree | "FAIL a save's container is its stage, nvm_stage, less the record header ... got 8" (`receipts/rtl-fix/journal-bound/plant-rec-hdr-8.txt`) |
| `save_grade.save_time`, end to end | `da1869a3`'s grader, KLJ2's 8 | "REFUSED save-second: the save programmed 3444 bytes, its image is 3446" (`V32-at-da1869a3-*`) |

**The record mover's area** (ruling on the second STOP: "if the fix moves area or timing beyond its own few flops, state it"):
- `KL_mbx_dma` alone through `synth_xilinx -family xc7`, at `187eeed8` (before the fix) and `da1869a3`: flops 704 and 704, LUTs 484 to 487, MUXF7 16 to 13, MUXF8 5, CARRY4 34 (`receipts/rtl-fix/area/`).
- No route was run, so there is no timing figure. The one flop's next state takes one AND-OR more, and it gates the mover's request and ready.

**Gates run in this session** (each rc 0 unless stated, never piped):

| Gate | Tree | Result |
|---|---|---|
| `flash_test.cpp` | working tree on `cdc2742e` | 19 checks, 0 failures |
| `fw_service_budget/run.py --self-test` | the same | `checks: 55 failures: 0` |
| `ctrl_service_budget/run.py --self-test` | the same, then with `3e67f9ca`'s change | `self-test: 0 failures` both times |
| `check_cpp_idiom.py`, `check_py_idiom.py` | the same | PASS |
| `docs_check.py` | before each commit | 0 findings |
| verification, 1x1, `acmp-notk` and `save-second` | the working tree of `da1869a3` | both run to the end without a journal refusal; rc 1 on "the save programmed 3444 bytes, its image is 3446" and three STATED lines (fixed at `3e67f9ca`, and the third STOP) |

**The legs at `da1869a3`** (queue 32; GA8 and GA1 with helpers on the same build, `scripts/a683zo_helper.py`):
- GN8, GN1: 16 of 16 groups each, rc 1, on STATED lines only.
- GB8: rc 0. GB1: rc 1, on one STATED line.
- The four controls: all caught.
- GA8 and GA1: running when the STOP was posted.
- `receipts/stop3-stated-costs/README.md` tabulates every cost over.

**The STOP.** In short:
- `ctrl_loop.h` and `aecp_mbx.h` state the costs by their own rule, heaviest measured plus 5 %.
- Round 29's table rule keeps them, a measurement over them being a finding.
- The rule's figure for the AECP round's cold cost at 8x8/2if, 190 us, makes THE RETRY's search put the first queued notice at 28 ms against `AECP_QUEUED_FIRST_MS`, 22 ms. Item 5 holds that bound unchanged.
- That is a decision, not mine (AGENTS.md section 2).

**Run history (CET, 2026-11-12 to 13):**
- 22:20 the journal check traced.
- 22:22 queue 31 stopped.
- 22:23 the verification run started.
- 22:41 `da1869a3`.
- 22:42 queue 32.
- 23:04 the verification run ended, the header refusal found.
- 23:20 `3e67f9ca`.
- 23:41 the helpers started.
- 23:50 to 00:07 the STATED tally, the search on a copy, `525375d6`.
- 00:10 the STOP.

## 11. After the ruling on the third STOP (the stated costs)

**The ruling** (#665 issuecomment-6842347916, option (b) amended, a maintainer-delegated decision):
- `AECP_ROUND_COLD_US` at 8x8/2if: 165 to 185 us, the most the retry search holds; 186 fails it.
- `CTRL_LOOP_BUILD_ONE_PASS_US` at 1x1/1if: 405 to 430 us, by the rule.
- `CTRL_LOOP_BUILD_PASS_US` at 1x1/1if: 900 to 1,010 us, by the rule.
- The margin exception is stated in `aecp_mbx.h`, `FR_NFR.md` 3.4.1 and `SPLIT_CONTROL_MEMORY.md`. It expires at the 8x8/2if flip.
- The tables take every leg's full tally.
- Four STOP triggers.
- Then the fresh 8x8 build and its legs, the four controls, the 1x1 grading after a byte-compare, the tables, the load gate, the full pass, and REVIEW READY.

**The resume.** The session was cut during the STOP; on resume the tree was clean at `525375d6`. The old GA8 at `da1869a3` was still grading, and its unit ended at 03:56.

**Trigger 1, before building** (`receipts/ruling3/trigger1-rounds-by-n-k.txt`; `tools/tally_rounds.py`, through the harness's own `round_grade.rounds`). I tallied every round of every leg at `da1869a3` by notices n and refusals k.
- No implied cold cost (round - 365n - 34k) exceeds 183.1 us. The dearest is GN8's n=0 k=2, 24,816 cycles, implying 180.16 us.
- GA8 has only k=0 and k=1 rounds, the dearest implying 81.41 us. So there is no k=0 or k=1 round over the stated line.
- At 1x1/1if every round is under its stated 85 us. The dearest is GN1's n=0 k=1, at 58.62 us.

**Trigger 3.** I tallied every STATED line of every leg's own run and its helpers'. The firmware-stated costs over are the three ruled, and no other:
- the build pass, 96,033 cycles (GA1 `srp`);
- the build-one pass, 40,700 (GB1 `aecp`);
- the rounds at 8x8/2if (GN8).

`ctrl_retry_search.py` passes at 1,010, 430 and 185 together, and fails at 186 (`receipts/ruling3/retry-search-what-if-cold-186.txt`).

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `6c284a97` | `sw/firmware/ctrl/aecp/aecp_mbx.h:21-29` | `AECP_ROUND_COLD_US` 2-IF 185. The exception: 2.7 % over the most measured, 180.16 us, because 186 fails the search's binding pass (185 + 5 x 34 + 1,215 + 365 + 65 = 2,000 us, THE SHARE). It expires at the 8x8/2if flip, when #890 closes with a measured cold cost of at most 176.1 us or on a new owner decision | the ruling |
| `6c284a97` | `sw/firmware/ctrl/loop/ctrl_loop.h:270-271` | `CTRL_LOOP_BUILD_PASS_US` 1-IF 1,010; `CTRL_LOOP_BUILD_ONE_PASS_US` 1-IF 430 | the ruling, by the rule. Only the search and the harness read them, so the 1x1 image is unchanged |
| `6c284a97` | `docs/reference/FR_NFR.md` 3.4.1 (after "Each stated cost of a notice ...") | the exception with its link, its reason and its expiry | the ruling |
| `6c284a97` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 ("The queued notices at stated costs") | the exception; the pass costs at 1,010 / 430, with the merged image's 96,033 and 40,700 cycles | the ruling |
| `6c284a97` | `tb/verilator/ctrl_service_budget/poll_grade.py:55`, `:61`; `load_grade.py:150-155` | an owed MRPDU at a build of one's 430 us at 1x1/1if; the graded column's builds at the headers' | an owed MRPDU is stated at a build of one's cost, and the graded column is at least the pin's (`load_grade.py --check` refused it otherwise) |
| `16eb95fc` | `sw/firmware/ctrl/test/test_aecp.cpp:2468-2473` | "firm, it stops at its cap beside records" gives the round room for one notice past the cap: `AECP_ROUND_COLD_US + (AECP_ROUND_FIRM_NOTICES + 1) x AECP_NOTICE_US`, in place of `CTRL_LOOP_SHARE_US` | at the 185 us cold start a share holds 4.97 notices at 8x8/2if, so the share alone no longer tells the cap of 4 from the pass's room. The plant `retry-firm-uncapped` escaped the firmware-aecp-mutants job at `6c284a97` (`receipts/ruling3/aecp-mutants-shard2-at-6c284a97.txt`) |
| `5bea2597` | `tb/verilator/ctrl_service_budget/load_grade.py:102-170`, `poll_grade.py:51-66` | the tables by `tools/apply_tables.py` from `tools/tables30.py`, and their provenance | the ruling: every leg's full tally |
| `5bea2597` | `docs/design/SPLIT_CONTROL_MEMORY.md` section 13 | round 30's re-grade paragraph; the rows (1x1/1if R4 74.83 ms); the "less two records" plant now refused at R5's W, 38.25 ms (50 SRP records ahead against 51); the two columns' table; the load table and its paragraph; the levers; "What is left" | the docs' figures at this head |

**New check, its plant and its failing words:**
- **Check:** `Mailbox.ARoundFillsWhatItsPassHasLeft`, "firm, it stops at its cap beside records", with room for the cap plus one.
- **Plant:** `retry-firm-uncapped` (`aecp_retry_mutants.py`), the cap taken off.
- **Result:** caught with the fix ("[ok] retry-firm-uncapped", shard 2/4 PASS). At `6c284a97` it was "[ESCAPED] retry-firm-uncapped: Mailbox.ARoundFillsWhatItsPassHasLeft".

**The legs.**
- **8x8/2if, on fresh builds at `6c284a97`**, each on its own clean clone:
  - GA8, every group of arm A, with helpers and stealers on the same build (`scripts/a683zo_helper.py`, `a683zo_steal.py`), its runs merged (`merge_leg.py`), 93 groups;
  - GN8, the `answering-every-port` arm;
  - GB8, arm B's `aecp` group;
  - the four cost controls.
- **1x1/1if.** Each leg's build at `6c284a97` (S-GA1, S-GN1, S-GB1) has an image identical to `da1869a3`'s: the ELF, `objcopy -O binary`, and one sample group's log byte for byte. Every recorded group of the `da1869a3` legs is graded on it.

**Trigger 2.** The re-grade at `6c284a97` checks every round and every pass given whole on the fresh 8x8 build against its stated cost, and none is over. The only STATED lines are grader tables (the polls base, the rebuild item), and the tables restate them.

**Trigger 4.** After the tables, `load_grade.py --check`: 1x1/1if 0.501 at the pin and 0.499 with tsn-c-stack#32, PASS.

The re-grade at the merge:

| | 8x8/2if | 1x1/1if |
|---|---|---|
| refusals | 0 | 0 |
| misses (arm A) | 7 of 996 (4 of 136 paths), round 29's owed rows, 62.68 to 65.05 ms | 7 of 945 (4 of 87), 61.95 to 63.59 ms |
| misses (answering-every-port / arm B) | 0 of 736 / 0 of 39 | 0 of 280 / 0 of 25 |
| work passes over the share | 0 of 257,719; heaviest 183,244 cycles (`notice-burst-2`) | 0 of 166,045; heaviest 166,127 (`notice-every-6`) |
| saves | `save-second` 22,829.6 of 22,870 ms; `save-starved` 12,447.0 of 12,470 | 6,030.3 of 6,070; 4,048.8 of 4,070 |
| least row margin | 8.162 ms (`backlog-adp@program-aged2-7`) | 9.992 ms (`backlog-adp@verify-aged2-5`) |

The tables (`tools/tables30.py`, round 29's rule; the polls' rebuild and withdrawal items restated by the same rule as its other items):
- `poll_grade.py`: the polls base 155 to 205 us at 1x1/1if and 280 to 325 at 8x8/2if; the walk 20 to 35 at 1x1/1if; the rebuild 630 to 690 at 8x8/2if.
- `load_grade.py` at 1x1/1if, both columns: SRP record and its retained retry 260 to 280, centisecond 130 to 150, AECP timer slot 60 to 65, TICK 40 to 45, grandmaster event 35 to 40. With #32: the polls base 155 to 205, the walk 20 to 35, ACMP's owed frame 120 to 125.
- `load_grade.py` at 8x8/2if: AECP timer slot 100 to 110 in both columns; TICK 40 to 85 at the pin and 75 to 85 with #32. With #32: the polls base 285 to 325.

The four controls at `6c284a97` are all caught:

| Control | Planted | Stated |
|---|---|---|
| `notice-fan-out-as-it-was` | an AECP item of 31,933 cycles | 27,000 |
| `polls-rebuild-in-the-base` | a polls base of 74,295 | 28,000; 32,500 restated |
| `polls-rebuild-twice` | a rebuild item of 109,171 | 63,000; 69,000 restated |
| `srp-compared-by-memcmp` | 34,551, against 30,989 unplanted (+11.5 %) | — |

The load and rows at this head:
- `flip_grade.py --check` exits 1, as designed: 8x8/2if at 0.822 at the pin.
- 1x1/1if R4 by every source is 74.83 ms against tier 1's 20; it was 66.12 ms at round 29.
- 8x8/2if R4 377.98, R5 148.68, R6 139.23 ms.
- The rows by every source are #894's.

**The cause is not separated.** The merge brings the two-cycle register read (`3ba76ae7`), KLJ3, and a hot list without `nvm_any`.

**The owner decision of 2026-11-13 06:47** (#665 issuecomment-6845315282), posted after the ruling: "8x8 is a must, 2if parts an option, but keep it going."
- The flip needs at least 8x8/1if, and a 2if-only blocker may be deferred to #890.
- #810 is not re-scoped, so this round changes nothing for it.
- Holding the rows at 8x8/1if is #894's next step; this head's flip check is unchanged.

**The full pass, once, at `5bea2597ec514f0cde306e538261c6ddee66b456`.** Each gate ran on a clean clone and was never piped. Receipts are in `receipts/final-5bea2597/`.

| Gate | Result | Receipt |
|---|---|---|
| Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml`, each job on its own fresh clone (`gates/run_wf.py`) | **139 steps rc 0; 226 not run, each with its reason; 0 bad** (`verify_wf.py`, rc 0). Every job's tree is clean after it. `docs-check-no-git` removes `.git`, so the runner's tree check after it cannot run, as in round 29 | `workflows/verify-table.md`, `workflows/rc/`, `workflows/drivers/` |
| rtl-fast: `bdd-conformance` | 508 scenarios and 2,330 steps passed | `workflows/logs/` |
| rtl-fast: `firmware-unit` | `test_ctrl_firmware: PASS`; the saved-state store's coverage run PASS; `fw_coverage.py --check` PASS over 39 files | |
| rtl-fast: the firmware mutant jobs | control mutants 698 of 698 caught; AECP mutants 227 `[ok]`, `retry-firm-uncapped` among them; SRP mutants 340 `[ok]` | |
| rtl-fast: `firmware-boundary`, `firmware-verilator` | `ctrl_boundary: PASS` | |
| rtl-fast: `split-cdc` | 13 checks, 0 failures | |
| rtl-fast: the other jobs | `yosys-elaboration`, `verilator-lint`, `yosys-tool`, `publication-census`, `changes`: rc 0 | |
| rtl.yml | `full-ci-gate`, `yosys-tool`, `yosys-shards` 0/4 to 3/4: rc 0 | |
| elaborate.yml | `elaborate-gates-0`, `elaborate`, `elaborate-gates-1`: rc 0 | |
| docs.yml | `wire-accountability`, `docs-check-no-git`, `docs-check`, `docs-gates-0` to `-2`: rc 0 | |
| The full sweep, `scripts/run_all_suites.sh`, four shard units on clean clones (`scripts/native-shard-one.py`, the manager's `native-shards.py` steps for one shard; shard 2, holding `capture_coherence`, on four CPUs) | **65 suites passed, 0 failed, 0 timed out; 2,713,040 checks, 0 in-suite failures**; every shard's preflight passes and every runner exits 0. `mbx`: the record mover's mutants 24 of 24, the mailbox's 12 of 12. In shard 3 the `tsn_fuzz` campaign rewrites the date stamp of two `TEST_RESULTS.md` files in place, as before | `sweep/` |
| The lane's own gates, part a | `git diff --check` against the merge base and round 29's head; the Python and C/C++ idiom gates; `check_baremetal_only.py --check`; `docs_check.py` 0 findings; `ctrl_hot.py --self-test` and `--check`; the harness self-test (0 failures); `load_grade.py --selftest` (25 of 25) and `--check` (PASS, 0.501 and 0.499); `flip_grade.py --selftest` (132 of 132); the rows' re-derivation; R711-8's and R712-8's rule, column and fan probes; `attribute_grep`; the hooks and target self-tests; `gen_mailbox.py --check --crosscheck` and `--selftest`; `lint_rtl.py --check`; `test_soc_options.py`; `test_ctrl_memory.py`; `cd tests && behave`; `make -C tb/verilator/milan_dp twin`: each rc 0 | `lane/summary.txt` |
| The flip check | `flip_grade.py --check`, `--point 1x1/1if` and `--point 8x8/2if` each exit 1, by design (1x1/1if R4 74.83 ms, #894; 8x8/2if, #890) | `lane/flip_check_*.log` |
| The lane's own gates, part b | `test_builder.py --require-rv32`: rc 0 | `lane/test_builder.log` |
| The lane's own gates, part c | `plat_ledger.py --self-test` (four points, 7 of 7); the fixtures at four points; `test_ctrl_nvm.py --require-rv32 --self-test` (526 tests, 144 planted defects reddened); the split boot at 1x1/1if (ready at 26.370 ms), 8x8/1if (66.017) and 8x8/2if (68.371, run after the part on its clone, `boot_8x8_if2`); its native controls; its plants: each rc 0 | `lane/boot_*.log` |
| The harness at this head, the six legs (`scripts/sample33.sh`) | Each leg is built fresh with one sample group, and every image and every sample log is byte-identical to the leg's build. Every recorded group is then regraded: GA8 93 groups, GN8 16, GB8 1, GA1 94, GN1 16, GB1 1; 0 refusals; the 14 recorded misses; no STATED line; each rc 0 | `harness/` |
| The four cost controls at this head | all caught: 31,933 against 27,000; 74,295 against 32,500; 109,171 against 69,000; 34,551 against 30,989 | `harness/controls/` |

**Run history (CET, 2026-11-13):**
- 03:51 resumed; the ruling read.
- 03:56 the old GA8 ended.
- 03:58 trigger 1 tallied.
- 04:02 `6c284a97`.
- 04:04 queue 33: the fresh 8x8 legs, the controls, the 1x1 samples.
- 04:21 to 05:39 helpers and stealers on GA8.
- 06:00 to 06:15 the early firmware jobs; the AECP plant escaped.
- 06:17 `16eb95fc`.
- 07:21 GA8's `save-second` finished.
- 07:23 to 07:40 the merge, trigger 2, the costs, the tables, the docs.
- 07:41 `5bea2597`.
- 07:47 the full pass.
- 08:22 to 08:24 the four shards.
- 10:03 the lane's part c.
- 10:10 `boot_8x8_if2`.
- 10:12 `verify_wf.py` rc 0.

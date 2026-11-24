# HANDOFF r1: [A828], the post-flip composition lane (pf-train-1123 -> dev-soft-core)

**Status: STOP (23:40 CET).** The composition is done and every gate passes. The routes meet #818's floor at both
shapes, and the formal CPU budget measurement is complete at 1x1/1if and 8x8/1if (490 groups). The two statements the
manager's ruling named are **within** on the composed images, so neither is raised. One other statement is over and is
raised by the rule with every owner bound held.

**The STOP:** at 8x8/1if **two of #969's owner-ruled conditions break**: kept <= bound in arm A, and a build pass within
its stated cost in `answering-ports`. The lane can't restate either, because one is an owner ruling's condition and the
other is the firmware's tier-2 slice constant. Details are [below](#the-stop-two-of-969s-conditions-break-at-8x81if).

Final head **`f5a1585e601cc627824b590c7f50351e3c8da18f`**, branch `pf-train-1123`, committed locally. Nothing is pushed
and nothing is posted (no REVIEW READY on #665, because of the STOP). The final-head gate reruns are listed in the gate
table.

Base `078c60fb` (the #958 sync: PR #958 `1825ba4e` + PR #961 `287ca1ee` + dev-soft-core `854bd723`; dev-soft-core still
`854bd723` when fetched). The tsn-c-stack pin is unchanged at `715589c1`. Every PR head fetched matches the manager's SHA.

## The STOP: two of #969's conditions break at 8x8/1if

The owner's ruling on #969 (2026-11-22) owes the kept Talkers' registration records to #977 while `kept_grade.py`'s
conditions hold. `kept_grade` on the formal measurement's legs (receipts `budget/kept-grade-*`):

| Point / arm | kept <= bound (kept Failed against the bound record, CPU cycles) | build passes within their statements | kept_grade |
|---|---|---|---|
| 1x1/1if arm A | 36,631 <= 38,739 | yes (build-one 53,182 of 73,500) | PASS, 4 owed |
| 1x1/1if answering-ports | 35,435 <= 38,746 | yes (53,605 of 73,500) | PASS, 4 owed |
| **8x8/1if arm A** | **142,582 > 142,137: broken** | yes (103,782 of 147,500) | **FAIL**, 5 owed |
| **8x8/1if answering-ports** | 134,143 <= 138,016 | **srp-bound's build of one 171,645 > 147,500: broken** | **FAIL**, 5 owed |

- **kept <= bound (8x8/1if, arm A).** At #969's head (its 5dba2089 images) the kept Failed record was 142,909 and the
  bound record 153,208. On the composed image the kept record barely moves (142,582) but the bound record is about
  11,000 cycles cheaper (142,137). So the comparison #969's ruling rests on now fails by 445 cycles (0.3 %). The
  composition caused it by making the other side of the comparison cheaper. #969's code didn't change.
- **The build pass (8x8/1if, answering-ports).** `srp-bound`'s build of one MRPDU is a single pass of 171,645 cycles.
  The limit is `CTRL_LOOP_BUILD_ONE_PASS_US` 1,475 us (147,500 cycles), tier 2's slice at shape (1, 9, 9)
  (`sw/firmware/ctrl/loop/ctrl_loop.h:373`). Arm A's same group builds at 103,782. #969's rounds graded arm A only, so
  this arm's figure has no earlier measurement to compare with.
- Neither is a statement that ruling item 4 can raise. The first is an owner ruling's condition. The second is a
  firmware constant that sets the scheduler's slice: raising it changes the image and THE TRANSMIT's model. So, per the
  manager's item 2 ("if an owner bound would break, STOP with the figures"), the lane stops here.
- **Needed to clear:** an owner decision on #969's conditions at 8x8/1if. Options include accepting kept <= bound
  within a margin, or comparing kept with the bound path's measurement at #969's head, and deciding on the srp-bound
  build-one pass (owed to #977 with the rest, or a slice restatement). Then a re-grade of the same legs. The logs are
  kept in the scratch tree, and `kept_grade.py` grades them without re-simulating.

## Merges (one merge commit each, in the manager's order)

| # | PR (issue) | Branch at head | Merge commit | Conflicted files |
|---|---|---|---|---|
| 1 | #959 (#948) | `948-rx-fanout` `64117b77` | `ee58b499` | none (7 files auto-merged, both sides read) |
| 2 | #975 (#584) | `584-input-port-clusters` `3cda030c` | `8fac1fd2` | `aecp_mutants.py`, `ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `SPLIT_CONTROL_MEMORY.md` |
| 3 | #971 (#969) | `969-srp-kept-talkers` `c113018d` | `23ee9529` | `sink_mutants.py`, `test_plat_sinks.cpp`, `ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, `SPLIT_CONTROL_MEMORY.md`, `plat/README.md`, `ctrl_split_boot/README.md` |
| 4 | #978 (#973) | `973-srp-link-carried` `87b2fc0f` | `b04610c2` | `CHANGELOG.md`, `srp_mutants.py`, `test_ctrl_firmware.py` |
| 5 | #974 (#972) | `972-link-once` `77a74b2f` | `d6c398c8` | `CHANGELOG.md` |

Then, on the code head `d6c398c8`:

| Commit | What and why |
|---|---|
| `c2b2ba1a` | The ledger at the composed images' measured figures (below). **Images and every image-dependent gate ran here.** |
| `0ad0bf2d` | A gate fix: `ctrl_configs.OUTSIDE` classifies `sw/litex/mac_link_status.py` (finding 1 below) |
| `b6b2e603` | The firmware page's pin control count as measured, 185 -> 192 (finding 2) |
| `cfd99726` | The resolved texts held to the idiom gate (two lines past 120 columns; `test_ctrl_memory.py` back to 1,000 lines) and the SRP page's bare reference made a link (the early docs run's findings) |
| `f5a1585e` | 8x8/1if `poll_grade.EIGHT_ONE['aecp_long']` 320 -> 325 us by the rule, and section 13's record of the formal measurement. **Final head.** |

Every commit after `c2b2ba1a` changes no image input. `plat_ledger` at `f5a1585e` gives all 24 image hashes identical
to `c2b2ba1a`'s (`ledger/plat-ledger-f5a1585e.txt`). The changes are text, `ctrl_configs.OUTSIDE` (read by the
boundary gate alone), and a grader's statement.

## Conflicts and their resolution (every one keeps both sides)

1. `sw/firmware/ctrl/test/aecp_mutants.py` (`DEFECTS`): the train's registration (#957) and again (#950) rows and
   #584's input rows both appended after the configuration rows. All four tables are kept, and both imports. The file
   is 997 lines, under the idiom gate's 1,000.
2. `sw/firmware/ctrl/test/sink_mutants.py` and `test_plat_sinks.cpp`: #950/#954's `Streams` fixture (S13, S14, T1) and
   #969's `Early` fixture (S13, S14) each add tests at the same place. Both fixtures are kept whole. The gtest names
   differ by fixture. The two colliding Python constants are renamed `EARLY_S13` and `EARLY_S14` for #969's rows, and
   its one plant row is updated to them. The header comment gets an "Early" heading. 36 rows (35 + 1, counted from
   `sink_mutants.mutants`), stated in `plat/README.md`. `platsinks` runs 17 tests a shape (12 + 3 + 2).
3. `srp_mutants.py` and `test_ctrl_firmware.py`: #969's `srp_early_mutants` and #973's `srp_link_mutants` are both
   imported and appended. The 8x8/1if SRP campaign's filter carries both prefixes. The 1x1 if1 filter carries #973's,
   as on #973's branch.
4. `CHANGELOG.md` (twice): every entry and its contents line is kept, newest merge first.
5. The ledger (`ctrl_memory.py`, `ctrl_memory_ledger.py`, `test_ctrl_memory.py`, the design page's sections 3 and 5,
   the platform, SRP and split-boot READMEs): each PR's own text is kept as the history of its own base. The figures
   were provisional at the merges and are **re-derived from measurement in `c2b2ba1a`**, never added from the PRs'
   figures.
6. The plat README's "ACMP's asking-failed source flag reads false" bullet appeared only in #969's side of a conflict.
   It is the base's text, which #954 (on the train) removed by implementing the flag, so it stays removed.

Receipt: `merge/merges-and-resolution.txt` (each merge's parents, files both sides changed, and the combined diff of
every conflicted file).

## Two gate findings on the composed head, and their fixes

1. **`ctrl_boundary.py --require-rv32 --selftest` refused `sw/litex/mac_link_status.py`** (fixed in `0ad0bf2d`). The
   file names the firmware's tree (`sw/firmware/ctrl/plat/ctrl_plat_phy.h` in its docstring), has a `__main__` block,
   and is in none of `BUILDERS`, `PART_OF`, `OUTSIDE` or `SUITES`. It came from PR #974 (#972) and is byte-identical
   at #974's head `77a74b2f`. There, `ctrl_configs.py` differs from the composed one only by #973's own `OUTSIDE` line
   (`f90ede10`). So **PR #974's own head fails this gate the same way**, and the composition did not make it. The fix
   is of the same kind as #973's `f90ede10`: one `OUTSIDE` entry beside `milan_soc.py`.
2. **The firmware page's pin control count** (fixed in `b6b2e603`). The self-test's only remaining finding was "gives
   the pin controls as 185, where the self-test has 192". Every PR head and dev-soft-core state 185. The 7 more are
   #948's `milan_dp` targets: `twin-fanout`, `twin-fanout-plants`, `build-twin8-sp`, `twin8-fw`, `fan-stop-plants`,
   `fan-stop-plant-shared` and `fan-stop-plant-one-index`, each a pin control in the run's log
   (`firmware/ctrl-boundary-0ad0bf2d-makefile-pin-controls.txt`).

## The composed figures (measured at `d6c398c8`; ledgered in `c2b2ba1a`)

`plat_ledger.py`: FAIL at `d6c398c8` before the figures (11 findings), PASS at `c2b2ba1a` and `f5a1585e` (0 findings):

| Point | rom / sram, B | RAMB36 | ctrl_plat, B | Entry |
|---|---:|---:|---:|---|
| 1x1/1if | 127,512 / 56,736 | 45.5 | 18,048 | within 56 |
| 1x1/2if | 129,296 / 59,168 | 46.5 | 19,840 | within 56 |
| 8x8/1if (product) | 141,616 / 100,096 | 59.5 | 19,136 | raised 59.0 -> 59.5, S14 debt 3.5 |
| 8x8/2if | 143,368 / 117,632 | 64.5 | 21,888 | raised 64.0 -> 64.5, S14 debt 8.5 |

- `ctrl_plat` is 64 B larger than with #969 alone at 1x1/2if and both 8x8 points. That is the composition, as measured.
- **The size fixture.** Linked for every labelled CPU-budget arm, every `nvm_split_target` arm and every planted
  mutation at both 8x8 points (#584's `variant_sizes.py`), plus each mutation that needs a variant, built with it:
  - 8x8/1if: `declaring-outputs` plans 57.5 (133,128 B of rom), and so does `completion-dearer` on it (133,168 B).
    Every other image plans 57.0. The entry is raised from 57.0 to 57.5 (S14 debt 1.5).
  - 8x8/2if: every image plans 61.5, its entry.
- `test_ctrl_memory.py`'s synthetic ledger image now reaches 65.0 with seven tiles of `.text` (six reached 64.5), so
  the platform's 65.0 refusal is graded. It PASSes with 0 failures.

## The formal CPU budget measurement (images of `c2b2ba1a` = `f5a1585e`)

Every arm and every group at 1x1/1if and 8x8/1if:
- The arms: arm A, `answering-ports`, `answering-every-port`, `answering-later`, `shutdown-entry`,
  `valid-destinations`, `talker-notices` and `declaring-outputs`.
- 245 groups a point, 24 legs, at most 4 at once, each built once and run as `run.py` builds it with
  `--record-budget-findings --record-share-findings`.
- Graded by the statement survey (round 28's tools, with `srp-kept`/`srp-bound` left to `kept_grade.py`),
  `record_classes.py` and `kept_grade.py`.
- Receipts: `budget/cpu-1x1-1if-formal-c2b2ba1a.md` and `budget/cpu-8x8-1if-formal-c2b2ba1a.md`.

- **Refusals and misses.** No group is refused at either point. The only budget misses are the 7 known held-egress
  `backlog-owed` rows, in arm A and in `answering-ports`, as on every base. Passes over THE SHARE: 0 of 420,473 at
  1x1/1if, and at 8x8/1if 2 of 737,682, both `srp-bound`'s, owed to #977.
- **The manager's two statements: within, so not raised.**
  - 1x1/1if `edit_rows.PACED`: held paced 28,733 cycles, 305 us, of 315 (`answering-ports` `aecp-fanout`, an
    accepted SET_CONFIGURATION; the one-row edit is below it; 28,947 reported in `declaring-outputs`).
  - 8x8/1if `rows_tiers.LONG_RECORD_US`: 85,310 cycles, 900 us, of 1,720 (arm A `aecp-largest-notice`; 85,968
    reported in `declaring-outputs`).
  - The sync's 30,044 and 167,199 were measured on #958's image.
- **Why the 8x8/1if long record halved.** With #584's AUDIO_CLUSTER on every 8x8 STREAM_PORT_INPUT, the input map
  can change at 8x8, so `long_notice.groups` edits the input map. Before #584 it edited the output map (input map
  capacity 0). A **scratch probe (not committed)** of the output map's 63-mapping edit on the same image:
  - 8x8/1if: 136,201 cycles, 1,435 us, **within** 1,720.
  - 1x1/1if: 176,099 cycles, 1,850 us, past the 975 that the input map's edit states. The harness has never
    measured the output map at 1x1/1if (#894's design), so this is pre-existing and not the composition's. It is a
    candidate new Issue (`budget/probe-output-map-largest-command-NOT-COMMITTED.txt`).
- **One other statement exceeded, raised by the rule** (`f5a1585e`): 8x8/1if `poll_grade.EIGHT_ONE['aecp_long']`
  320 -> 325 us, 30,948 cycles (`declaring-outputs` `aecp-largest-notice`; arm A 30,912).
- **Every owner bound held at the raised statement** (`load_grade --check`, `flip_grade --check` at both points,
  `shape_costs --check`):
  - loads: 0.512 of 0.70 (1x1/1if) and 0.744 of 0.75 (8x8/1if);
  - 1x1/1if: last queued notice 127.43 of 130 ms (and of the owner's 140), ACMP 29.15 of 30, txL 47.98 of 49;
  - 8x8/1if: THE TRANSMIT 76.86 of 77 ms;
  - THE SHARE: as above.
- 1x1/1if: 0 statements exceeded. `record_classes` PASS: long 935 of 975 (955 reported), other 240 of 255, paced 305
  of 315.
- 8x8/1if: `record_classes` PASS: long 900 of 1,720, other 265 of 265, paced 590 of 685 (605 reported). The survey
  gives `aecp_long` (raised) and `srp-kept`'s own record (owed to #977).
- `kept_grade`: see [the STOP](#the-stop-two-of-969s-conditions-break-at-8x81if).

## Gate table

| Gate | Head | Result | Receipt |
|---|---|---|---|
| plat_ledger | `d6c398c8` | FAIL before the figures (11 findings: ctrl_plat +64 B, 8x8 at 59.5 and 64.5) | `ledger/plat-ledger-d6c398c8.txt` |
| plat_ledger | `c2b2ba1a`, `f5a1585e` | PASS, 0 findings. The 24 image hashes are identical at the two heads | `ledger/plat-ledger-c2b2ba1a.txt`, `-f5a1585e.txt` |
| Size fixture, every arm and plant | `d6c398c8`, `c2b2ba1a` | 8x8/1if worst 57.5 (declaring-outputs, completion-dearer on it); 8x8/2if 61.5 | `ledger/fixture-sizes-*.txt` |
| test_ctrl_memory.py | `c2b2ba1a` (working tree) | PASS, 0 failures (again at `f5a1585e` in the tree checks) | `ledger/test-ctrl-memory-c2b2ba1a.txt` |
| Firmware gate, 4 shards, with plants | `c2b2ba1a` | **PASS** all four: 2,003 live invocations, shards 96/845/399/663; 96 + 844 + 398 + 664 `[ok]`, 0 escaped | `firmware/fw-gate-c2b2ba1a-s0..3.txt` |
| Firmware gate, 4 shards, with plants | `f5a1585e` | **PASS** all four: 2,003 live invocations, shards 96/845/399/663; 96 + 844 + 398 + 664 `[ok]`, 0 escaped | `firmware/fw-gate-f5a1585e-s0..3.txt` |
| fw_coverage --selftest, --check | `c2b2ba1a` | **PASS** (40 files) | `firmware/fw-coverage-c2b2ba1a.txt` |
| ctrl_boundary --require-rv32 --selftest | `c2b2ba1a` | FAIL: `mac_link_status.py` unclassified (#974's own head too) | `firmware/ctrl-boundary-c2b2ba1a.txt` |
| ctrl_boundary --require-rv32 --selftest | `0ad0bf2d` | FAIL: the README's 185 pin controls against 192 | `firmware/ctrl-boundary-0ad0bf2d.txt` |
| ctrl_boundary --require-rv32 --selftest | `b6b2e603` | **PASS**: 0 findings, 117 boundary, 192 pin, 4 figure controls, 0 misbehaved | `firmware/ctrl-boundary-b6b2e603.txt` |
| ctrl_boundary --require-rv32 --selftest | `f5a1585e` | **PASS**: 0 findings, 117 boundary, 192 pin and 4 figure controls, 0 misbehaved | `firmware/ctrl-boundary-f5a1585e.txt` |
| Builder legs 0 and 1 and their union (docs) | `c2b2ba1a` | **PASS**: 113 gates exactly once | `firmware/builder-*.txt/json` |
| Twin, twin-plants, twin-maps, twin-maps-plants | `c2b2ba1a` | **PASS** (rc 0 each) | `twin/twin-c2b2ba1a.txt` |
| Suites: milan_dp | `c2b2ba1a` | **PASS**, 14,379 checks, 0 failures | `rtl/suites-A-c2b2ba1a.txt` |
| Suites: milan_dp_render, tdm_render, avtp_rxmon, milan_dp_mclk, aaf_audio_loop | `c2b2ba1a` | **PASS**, 3,626 checks, 0 failures | `rtl/suites-B-c2b2ba1a.txt` |
| Suites: nvm_backend, fw_service_budget | `c2b2ba1a` | **PASS** (849 checks). ctrl_split_boot, nvm_capture_cpu and nvm_split_target have no Makefile and are run by their run.py below | `rtl/suites-C-c2b2ba1a.txt` |
| Split boot: 1x1, 8x8, 8x8 --interfaces 2, placement and native controls, --self-test | `c2b2ba1a` | **PASS** (rc 0 each) | `rtl/split-boot-c2b2ba1a.txt` |
| nvm_split_target --self-test, --point 1x1, 8x8; check_nvm_capture.py | `c2b2ba1a` | **PASS** | `rtl/nvm-split-target-c2b2ba1a.txt` |
| Route 8x8/1if (recipe, ExtraPostPlacementOpt) | `c2b2ba1a` | **#818's floor met** at every corner: Slow WNS +0.105 / WHS +0.102, Fast +1.636 / +0.036 ns; 46,621 LUT, 53,338 FF, 98.5 BRAM tiles; identity PASS | `route/8x8-ExtraPostPlacementOpt/` |
| Route 1x1/1if (ExtraPostPlacementOpt) | `c2b2ba1a` | floor NOT met: Slow WNS +0.019 ns (`KL_mbx` rx, 24 levels, a path no PR touched) | `route/1x1-ExtraPostPlacementOpt/` |
| Route 1x1/1if (ExtraTimingOpt) | `c2b2ba1a` | **#818's floor met** at every corner: Slow +0.384 / +0.102, Fast +1.636 / +0.036 ns; 32,680 LUT, 80.5 BRAM tiles; identity PASS | `route/1x1-ExtraTimingOpt/` |
| CPU budget, the formal measurement (every arm and group) | `c2b2ba1a` | 1x1/1if: 0 statements exceeded, record_classes PASS, kept_grade PASS. 8x8/1if: aecp_long over (raised), record_classes PASS, **kept_grade FAIL in two arms (the STOP)** | `budget/` |
| Harness tree checks and self-tests (load/flip/shape --check, record_classes/flip/kept/load/shape --selftest, run.py --self-test, test_ctrl_memory) | `f5a1585e` | **PASS**: load_grade, flip_grade (both points) and shape_costs `--check` PASS; the five `--selftest` rc 0; `run.py --self-test` 0 failures (360 MUTANT caught lines); test_ctrl_memory 0 failures | `budget/tree-checks-f5a1585e.txt` |
| Docs workflow steps (wire-accountability, docs-check-no-git, docs-gates-0..2) | `b6b2e603` (early) | 2 real findings (a bare reference, 2 over-long lines and a 1,002-line module), fixed in `cfd99726`; 3 SDK install-verify refusals (environment, as on the bases) | `docs/docs-workflow-steps-b6b2e603.txt` |
| Docs workflow steps | `f5a1585e` | 56 steps rc 0, 24 SKIP (installs and hosted recorders); the 3 RV32 SDK install-verify steps refuse ("missing regular SDK provenance receipt", the environment, as on the bases); docs_check 0 findings, em-dash 0 over 801 added lines, every idiom gate PASS; tree clean after | `docs/docs-workflow-steps-f5a1585e.txt` |

## Notes

- **The first route attempt.** It ran on the session pool with 16 threads and was OOM-killed at 08:34 at its 12 GB
  cap. It was restarted at 10:01 on a booked range with 8 threads and a 16 GB cap
  (`route/chain-first-attempt-oom.log`).
- **Scratch and units.** Scratch is `$VALIDATION_STORAGE/train1123-a828` (clones, the measurement's logs, about 12 GB).
  Units are `milan-train1123-a828-*`, each with MemoryMax 10 to 16 GB. The CPU legs ran on booked 8-CPU ranges or on
  the session pool when none was bookable.
- **Receipts.** Under `receipts/`, with `INDEX.md` generated from the files present. Tools are copied with host paths
  replaced. No file is over 200 KB.

STOP: at 8x8/1if two of #969's owner-ruled kept_grade conditions break on the composed image (kept Talker Failed 142,582 > bound 142,137 CPU cycles in arm A; srp-bound's build of one 171,645 > CTRL_LOOP_BUILD_ONE_PASS_US 147,500 in answering-ports), which the composition cannot restate; everything else passes at f5a1585e

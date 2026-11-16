# [A786] #920 round 1: the split's saved-state store saves a burst of acknowledged name changes in time

Lane: `920-save-burst`, base `dev-soft-core` `659d7687` (verified, submodules initialised).
TAKEN: #920 issuecomment-6899873919.

Status: STOP (one condition): the 8x8/1if split platform image misses the timing floor at all three directives,
as the base's own image does at the recipe's (section 4). Every other gate is in section 4. The STOP text is
`STOP-r1.md`, posted as #920 issuecomment-6908928237.

## 1. The cause (proved before any fix)

**A lost mark, not the step rate.** `sw/firmware/ctrl/aecp/aecp_nvm.h` held the AECP owner's pending bits in
`uint32_t pending[8]` (256 ids), a size from layout 2's 8-bit record_id. Layout 3 (#823, `nvm_layout3.h`) puts the
NAME block after every other block: its base is id 222, so name ordinal k is id 222 + k, and every name from ordinal
34 on has an id of 256 or more. `aecp_nvm.c` `mark()` then wrote `pending[id / 32]` past the array, and
`aecp_nvm_poll()` scans only the 8 words, so those marks never reached the store: never dirty, no window, never saved,
however long the wait.

- **The five names lost on the bench are exactly ordinals 34 to 38** of the 1x1 names table
  (`AECP_ENTITY_NAMES` 39): AUDIO_CLUSTER 22, 23, 24, CONTROL 0, CLOCK_DOMAIN 0, ids 256 to 260
  (receipt `cause/names-table-1x1.txt`).
- **Unit proof at the base** (`cause/unit-burst-before-fix.txt`): a new test sets every one of the 39 names over AECP,
  saves through the real store and power-cycles: `delivered` 34 of 39, the store's `n_dirty` 34 of 39, and exactly
  names 34 to 38 come back as their defaults. Nothing is in flight, no attempt fails and no time limit is involved.
- **The capture refutes the timing lead** (`cause/rehearsal-setname-pacing.txt`, from the rehearsal's own capture of
  the persistence run): the 39 SET_NAMEs were all answered SUCCESS within 877.6 ms; AUDIO_CLUSTER 24 and 23 were
  answered at 573.96 and 576.89 ms, early in the burst, yet were lost, while clusters 21 to 8 answered later were
  saved. So the loss follows the id, not the time.
- **Impact at 8x8** (107 names): ordinals 34 to 65 set bits in the word after the array (`released` and its padding),
  ordinals 66 to 97 in `struct ctrl_plat`'s next member, `binding.acmp` (the ACMP persistence wrapper's pointer), and
  98 to 106 in `binding.bind_group`: 73 names never saved and the binding wrapper corrupted by a SET_NAME.
- **The other leads, checked:** a failed attempt inside the back-off, or attempts exhausted, would leave `stale`,
  `alarm` or a failed verdict; the rehearsal's console status after the run read PP_STAT `5b000444` (backed 1,
  img_valid 1, dirty 0, pend 0, stale 0, verdict 0): the store held nothing dirty or pending, as a mark that never
  arrived predicts. The flash part's erase/program time cannot select names by id. The `taken` rule walks ascending id
  (`nvm_rec_next`), so a change at or past the cursor is taken; it loses nothing.
- Harness replay (a) and bench replay (b): see section 5.

## 2. The fix (file:line, reason)

Commits (one-line subjects): `945a1217` the pending bits; `c1a24c18` the store's three mechanisms; `80e9a7ac`
`1734de1e` `3d9cd3e0` `9646113b` `c6373ea4` the harness; `9e28059b` the rule docs; `0fa7f2ed` `104f85cc` tests and
coverage rows; `11860de2` the ledger; `339d0224` the join's plant removed (section 3); `542281d0` the harness code held to the
Python idiom gate's ratchets (no behaviour change, below).

1. **The lost mark, fixed as that defect** (ruling item 1: "a failed attempt or a lost mark is fixed as that defect").
   - `sw/firmware/ctrl/aecp/aecp_nvm.h:10,20-21`: `AECP_NVM_WORDS` = layout 3's id space (`NVM3_ID_SPACE`, 1,129 ids,
     36 words) and `pending_count`. Reason: every record id `nvm_rec_id_of` returns must have its bit.
   - `aecp_nvm.c:128`: static assert, every id of the shape below `32 * AECP_NVM_WORDS`.
   - `aecp_nvm.c:138`: a bit counted only when it was clear (a record queued twice is delivered once).
   - `aecp_nvm.c:165,179`: a poll with nothing pending tests no word; the poll uncounts the bit it clears.
2. **The ruling's three allowed mechanisms**, `sw/firmware/ctrl_nvm/nvm_store.c`:
   - joins: `nvm_mark` (:934) joins a change to the running capture when the capture will take it: on its first
     walk a record at or past its cursor, and at any walk a record no capture holds; `nvm_takes` (:636) and
     `nvm_joined_behind` (:642) make the capture (:655) walk again from the first record for such a record, taking only
     records no capture holds, so it takes each record once and ends. `rewound` (:98).
   - next save at the first idle step: a change the save in flight cannot take sets `next_now` (:99, :934), and
     `nvm_idle` (:548) starts the next capture at the first idle step with no window; `nvm_capture_begin` (:532)
     clears it. A first change keeps DR2a's window; a failed attempt keeps DR2c's back-off (`nvm_busy` false then).
   - more than one step a centisecond: `nvm_busy` (:896), a save in flight (`nvm_in_flight`, :527) or a change it
     left outside a back-off; `nvm_store_step` (:912) takes a step in any pass it is called in while busy, with
     `NVM_STEP_US` left; a step not owed that finds no room returns false (the age does not run). The loop calls it
     once a pass, only in a pass that took no input; on the split image `mbx_hal_wait()` returns at once.
   - Not changed (ruling's refused list): `NVM_STEP_US`, `CTRL_LOOP_STEP_AGE`, the tiers, the pace, the two-slot
     sequence, the blank check, the verify, the format, DR2a's window for a first change. No RTL, no mailbox
     contract, no budget bound.
3. **The ledger** (`sw/litex/ctrl_memory.py:262`): `platform-8x8-two-interfaces` at 60.5 RAMB36 (its cap), its
   `ctrl_plat` 20,416 B; `ctrl_memory_ledger.py` and `test_ctrl_memory.py` restated (ROM 131,224 B; S14 debt).
4. **The harness** (`tb/verilator/ctrl_service_budget/`): `save_burst.py` (`schedule` :103, `held` :123, `burst`
   :154, `flight` :181, the grade :247-362); `sim_main.cpp:311` FLASHDATA; `grade.py` `programmed` (FLASHDATA, read beside
   `parse`) and the group's grade; `run.py` the journal file, the BURST line (`print_bursts`), the misses and the
   table; `save_window.py` the plants (`PLANTS`, merged into `build.MUTATIONS`, `build.SAVE_CONTROLS`), the groups at
   one-interface points (`groups`), the windows at a step a pass and the in-flight bound with no window of its own;
   `build.py` plants under `ctrl_nvm/`; the self-test
   (`selftest_burst.py`, five grader mutants, the restated checks).
5. **Docs**: `nvm_store.h` (the step and a change's worst case), `ctrl_loop.h` (a client may step in every pass that
   calls it), `ctrl_nvm/README.md` (THE STEP, DR2a, the figures), `ARCHITECTURE_HW_SW_SPLIT.md`,
   `nvm_split_target/README.md`, the harness README, `gtest/README.md` (two exclusion rows), and
   `SPLIT_CONTROL_MEMORY.md` (section 3's ledger row, section 13's new subsection and summary bullet).

## 3. New checks, planted mutants, failing words

**Firmware units (GoogleTest).** AECP arm (`sw/firmware/ctrl/test/test_aecp.cpp`, `aecp_mutants.py`):

| Check | Planted defect | Its failing words |
|---|---|---|
| `Nvm.EveryAcknowledgedNameSurvivesTheRealStorePowerCycle` (new: every name set over AECP, saved, power-cycled) | `nvm-ids-past-256-dropped` (ids past 255 never marked) | "every name's mark reaches the store, once"; "survives the power cycle" |
| same | `nvm-pending-counted-twice` | "the pending count follows its bits" |
| same; `Nvm.EveryChangeQueuesOnlyItsOwnedRecords` | `nvm-pending-count-kept` | "the pending count follows its bits"; `owner.pending_count` |

Store suite (`sw/firmware/ctrl_nvm/test/test_nvm_write.cpp`, `test_nvm_more.cpp`, `nvm_mutants.py`; `--self-test`
plants every defect and requires each named test to fail):

| Check | Planted defects (caught by) |
|---|---|
| `capture_joins` (new) | `join_never_walks_again`, `join_walk_takes_inflight`, `join_walk_joins_inflight`, `taken_while_capturing`, `taken_after_last_latch`, `taken_off_by_one` (the last now by "a first change after the retry: erase ... want 1,000 to 1,050 ms"), `next_save_waits_a_window` |
| `busy_steps` (new) | `busy_never_steps` ("the save ran a step a pass with no centisecond"), `busy_in_backoff` ("a failed attempt's backoff waits for the centisecond, its passes take no step"), `busy_without_room_owes` ("a pass of a save with less than NVM_STEP_US left takes no step and owes none"), `idle_counted_in_flight`, `next_save_waits_a_window` |
| `debounce` (its last case restated: a change during the seal is the next save's, no window) | `quiet_period`, `no_debounce`, `capture_leaves_window_armed`, `next_save_waits_a_window`, `idle_counted_in_flight` |
| `capture_window_edges` (restated: a change to a taken record is the next save's at the first idle step; one after the last latch joins) | `join_never_walks_again`, `taken_while_capturing`, `next_save_waits_a_window` |
| `step_room`, `dr2c_unchanged_set` (unchanged) | `step_untaken_when_not_owed`, `budget_rearmed_by_change` (seams restated) |

**Save harness** (`build.SAVE_CONTROLS`, `run.py --mutation`, caught when the group is named among the late saves):

| Control | Point | Group | Result |
|---|---|---|---|
| `store-names-past-256-lost` | 1x1/1if | `save-burst` | `CONTROL store-names-past-256-lost caught: 10 save(s) not durable within their stated worst case (save-burst, ...)`; names 34 to 38 never durable |
| `store-next-save-waits` | 1x1/1if | `save-flight` | `CONTROL store-next-save-waits caught: 1 save(s) not durable ... (save-flight)`; `112 steps to the next save's erase (want 19) OVER` |
| `store-step-only-owed` | 8x8/1if | `save-burst` | `CONTROL store-step-only-owed caught: 67 save(s) not durable ... (save-burst, ...)`; `the latest durable 8021.164 ms after its response (name 48; target 5,000 ms), 2 save(s) ... OVER` |

Receipts `tests/controls/` (each run's CONTROL, BURST and summary lines; the plants at `c6373ea4`, built on the RV32
image, so each plant compiles with every function referenced).

**The join has no harness control, by measurement.** A fourth plant, `store-join-dropped` (`if (0 &&
nvm_joined_behind())`), ran at 8x8/1if and printed `CONTROL store-join-dropped ESCAPED: 0 save(s) not durable within
their stated worst case (none)`. With the join left out, a change behind the cursor goes to the next save, and that save
starts at the first idle step. The burst was then `7 save(s)` where the join makes 6, the latest name `1366.653 ms`
after its response, `0 name(s) missing within` (`tests/controls/ctl-store-join-dropped-8x8-1if.txt`). At 1x1/1if the
burst ends inside its first window, so its one save takes every name and no join happens. So no group's 5 s target can
see the join. A control that cannot fail is no control, so the plant is removed (`build.py`, with the reason in its
comment and in the harness README). The store's units hold the join: `capture_joins` kills `join_never_walks_again`,
`join_walk_takes_inflight` and `join_walk_joins_inflight` (above).

Grader self-test (`run.py --self-test`): `selftest_burst.py`'s 11 checks (a name missing, late, refused or
unanswered; a container whose CRC does not close; the cut's older slot; no journal; the next save's steps) and five
grader mutants (`burst: a container is accepted whatever its CRC`, `burst: the cut is not read`, `burst: the cut reads
slot A whatever the sequences`, `burst: a SET_NAME's status is not read`, `flight: the next save's steps are not
counted`); at `9646113b` **0 failures, 251 of 251 mutants caught** (`tests/budget-selftest-9646113b.txt`).

Coverage: `nvm_store.c` 100 % lines and branches after its exclusions, `aecp_nvm.c` 100 % (two rows: `nvm_idle`'s
window-not-armed arc, arc 6 of 8, and `aecp_nvm_poll`'s scan-exhausted arc with its `return false;`; validated
offline against the kept measurement, no finding).

## 3b. The fix measured so far (exploratory, not the gate runs)

1x1/1if, fix at `9e28059b` (firmware equal to the head's; `logs/fix1-1x1`): the re-staged save windows
(`backlog-adp@{blank,program,verify}-{0,7}`, `blank-aged2-0`, `verify-aged2-7`) all open inside their phases, 0 budget
misses, 0 of 86,452 passes over the share; `save` 1,078.7 ms from the change to durable (2,018.6 at the base),
`save-held` 1,087.5, `save-starved` 4,048.2 of 4,070, `save-second` 6,030.5 of 6,070; the longest pass carrying a
step 98,909 cycles (0.989 ms), the longest step 78,820 (0.788 ms). `save-flight` (graded on the changed name since
`3d9cd3e0`): durable 158.5 ms after its response, its next save 19 steps (want 19), 6.4 ms, after the first's verify.

8x8/1if, fix at `9e28059b` (`logs/fix2-8x8-1if`, receipts `fix/burst-8x8-1if/`): `save-burst` 107 names, 214
frames in 2,777 ms, 0 refusals; every name durable, the latest 1,367.5 ms after its response (least 332.7, median
601.5), 6 saves of 306 to 318 ms each, the cut's authoritative container sequence 6 with no name missing;
`save-flight` durable 657.7 ms after its response, its next save 59 steps (want 59). 0 budget misses, 0 of 6,263
passes over the share. The base there traps in the burst and its change in flight takes 7,049.8 ms (section 5).

**8x8/1if's stated-cost lines are the base's, owed to #914** (`fix/8x8-1if-stated-triage.txt`). Both runs exit 1 on
STATED lines (run.py: at `--mutation none` a stated cost exceeded fails the run as a late line), and no row is over
its bound in either. On this base 8x8/1if takes 1x1/1if's statements, since `ctrl_loop.h` keys them on the interface
count: a build of one 735 us (73,500 cycles), the slice 950 us (95,000), the polls base 205 us (20,500), and an SRP
record's apply 280 us (28,000). `ctrl_loop.h:279-281` already records that one MRPDU's build at 8x8/1if measured
1,019 us, over both. #914, which is open and not on this base, gives 8x8/1if its own figures (slice and build of one
1,475 us).
- At the base (replay2, `659d7687`'s image), `save-flight` at 8x8/1if already prints 17 build-one passes (92,100 to
  94,668 cycles), 2 polls bases (21,531 and 21,774) and 1 SRP apply (30,063), so these kinds are not new.
- Fix, `save-flight`: 16 build-one passes (92,628 to 96,241); of those, 12 are also over the slice, the base's longest
  being 94,668. Each such slice is `srp_mbx:build_mrpdu` plus two `mrp_reclaim`s: SRP's MRPDU build, which this lane
  does not touch. At the same instant (4,061 ms) the build takes 90,675 cycles at the base and 91,512 at the fix
  (+0.9 %); the image's code and data moved by the 304 B of `rom` and 64 B of `ctrl_plat`. The CPU is cacheless here.
- Fix, `save-burst` (no base figure, since the base traps there): the longest slice is 109,408 cycles at 14,621.9 ms,
  `build_mrpdu` 104,680. That is 1.8 s after the burst's last save, with the store idle. It is within #914's 147,500.
- The polls base: the heaviest base is the same pass in both runs, the entity's SET_NAME delivered at about 2,715.7 ms,
  21,774 cycles at the base and 23,251 at the fix. Of the +1,477, `ctrl_app_aecp:deliver` (which runs
  `aecp_nvm_poll` -> `nvm_mark`, now with the join's checks) accounts for +731. The rest is spread over SRP's, ADP's
  and AECP's transmit spans, which this lane does not change.
- So this lane moves the 8x8/1if figures but does not create the condition. Against 8x8/1if's own statements on
  #914's head `d539f162` (`poll_grade.EIGHT_ONE`: base 235 us, retained 345 us; `ctrl_loop.h`'s (1, 9, 9) block:
  slice and build of one 1,475 us), every STATED line of these two runs is within: the polls base 23,251 of 23,500,
  the apply 30,494 of 34,500, the build 109,408 of 147,500. The polls base has 249 cycles of margin there, which the
  sync onto #914 re-measures on the merged image.

Images (`img/`, `qimg.sh`, base -> head): ROM +296 B (the size fixture's 1x1/1if) to +304 B, +304 B every platform image; SRAM +64 to +144 B; `struct ctrl_plat` +64 B at
1if, +128 B at 2if. platform 8x8/2if ROM 131,224 B, past its ledgered 60.0 RAMB36: raised to 60.5 (the owner's cap),
S14 debt (`11860de2`). Fixture 1x1/2if 41.5 -> 42.0 and 8x8/1if 54.0 -> 54.5 tiles (sram banks; not ledgered).

## 4. Gates (clean clone of the final head)

Final head `54280c94`: a docs-only commit over `f1f7c3e8`, whose firmware jobs below carry. The harness legs ran on `11860de2`'s image. From there to the head the firmware source is
unchanged; only tests, the harness plants, `save_burst.saves`' erase-count bound and the idiom refactor changed. The
image ELF in every harness build is `1ae81a2c` at 1x1/1if (`full1` and `full1b` alike). The head's grader re-grades
`full1`'s 1x1 `save-burst`, `save-flight` and `save-second` logs to the same lines.

| Gate | Command | rc | Receipt |
|---|---|---|---|
| CPU budget harness, 1x1/1if, every group | `run.py --point 1x1 ... --record-budget-findings --record-share-findings`, as four legs on one build, graded together by `--regrade` | 0 | `harness/regrade-1x1.txt`, `table-1x1.md`, `sources-1x1.json`, `run-*-1x1.txt` |
| CPU budget harness, 8x8/1if, every group | the same at `8x8-1if` | 1, on STATED lines only | `harness/regrade-8x8-1if.txt`, `table-8x8-1if.md`, `8x8-1if-stated-against-914.txt` |
| Save controls | `run.py --mutation <plant> --groups <group>` | 0 each (caught) | `tests/controls/` |
| Saved-state store suite with its planted defects | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | 0 at `54280c94`: 546 tests at 5 shapes, all 152 planted defects caught | `tests/store-suite-selftest-54280c94.txt` |
| Harness self-test | `run.py --self-test` | 0 at `54280c94` (and at `542281d0`): 875 checks, 0 failing, 251 of 251 mutants caught | `tests/budget-selftest-*.txt` |
| Split saved-state target, 1x1 and 8x8 | `tb/verilator/nvm_split_target` | 0, 0 at `104f85cc` (store and target unchanged since) | `tests/nvm-split-target-*.txt` |
| Load gate | `load_grade.py --check` | 0: 1x1/1if 0.516 of 0.70 (0.512 with tsn-c-stack #32) | `gates/` |
| Memory ledger | `sw/litex/test_ctrl_memory.py` | 0 | `gates/` |
| Python idiom, docs, doc style, doc paths | `check_py_idiom.py` (and `--selftest`), `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py` | 0 | `gates/` |
| rtl-fast firmware jobs | `run_wf.py` replica: firmware-unit (with `fw_coverage --check`: PASS, 39 files), -aecp-mutants, -control-mutants, -srp-mutants, -verilator at `f1f7c3e8`; -boundary (the LiteX venv) at `54280c94` | 0 failed steps in each | `workflows/` |
| docs jobs | `run_wf.py` replica at `54280c94`: wire-accountability, docs-check-no-git, docs-gates-0, -1, -2 | 0 failed steps in each; `verify_wf`: 61 steps ran, 34 not run with a reason, 0 bad | `workflows/54280c94/`, `verify-docs-54280c94.md` |
| elaborate jobs | `run_wf.py` replica at `54280c94`: elaborate-gates-0, -1 (the LiteX venv), elaborate | 0 failed steps in each; 8 of 8 LiteX simulations; `verify_wf`: 10 ran, 36 not run with a reason, 0 bad | `workflows/54280c94/`, `verify-elaborate-54280c94.md` |
| rtl-fast, every step | `verify_wf` | 0 bad at `f1f7c3e8` (21 ran, 86 not run with a reason) and at `54280c94` (3 ran, 104 not run) | `verify-rtl-fast-*.md`, `not_run*.json` |
| verilator-suites, every suite | the whole sweep serially, one unit on one range from 07:47, on its own clean clone of `54280c94`: four ranges with MemAvailable over 30 GB never stood together | INCOMPLETE at the record's close (13:23): 44 of 65 suites PASS, 18 not yet run. `gptp_shadow` FAILs on its mutant-lifecycle step alone (a 12 s subprocess timeout under a host load average of about 400; the suite's own 325 checks pass). `media_phase` and `milan_dp` TIMEOUT on the sweep's wall clock (1,400 s and 4,800 s, under loads of 300 to 800): result unknown, with `milan_dp`'s finished shapes passing (`milan_datapath` 233 checks, 0 failures). No suite reads anything this change touches. The sweep runs on, and the three suites are queued to run alone after it (`sweep/rerun-54280c94` in the lane's scratch) | `sweep/` |
| Split platform image 1x1/1if | S9's recipe, three directives | 0, met; best ExtraTimingOpt: WNS +0.133, WHS +0.036 | `image/1x1-*.txt` |
| Split platform image 8x8/1if | S9's recipe, three directives | **MISS at all three** (below) | `image/8x8-*.txt` |

**The harness at 1x1/1if** (98 groups):
- 0 refusals and 0 of 142,535 work passes over the share.
- Every BURST and SAVE line reads `within`; there is no STATED line.
- The 7 budget misses are the seven held-egress rows of `backlog-owed` (61.8 to 63.6 ms, behind the scenario's 60 ms
  egress hold). The design page records them as misses at the base, owed to tsn-c-stack #26.
- The longest tier-2 slices: SRP's 81,257, the build's 69,452 and the round's 8,750 cycles, against 95,000.
- Joins 187.8 to 190.1 ms. The aged windows' least margin is 9.976 ms.
- The longest pass carrying a step is 0.989 ms; the longest step is 0.788 ms.

**At 8x8/1if** (97 groups):
- 0 refusals, 0 of 251,469 passes over the share, and every BURST and SAVE line `within`.
- The same seven held-egress rows miss (61.8 to 64.4 ms).
- The aged windows' least margin is 8.876 ms.
- The run exits 1 on STATED lines across ten kinds, against 1x1/1if's statements, which this base keys on the
  interface count (section 3b). Each kind's most measured instance is within #914's own 8x8/1if statement; the tightest
  is the polls base, 23,251 of 23,500.

**ROM per image** at the head, by `qimg.sh` (`image/rom-per-image-*.txt`): every image links.
- size fixture: 1x1/1if 111,320 B (+296), 1x1/2if 112,616 (+304), 8x8/1if 124,832 (+304), 8x8/2if 126,096 (+304);
- platform: 1x1/1if 116,376 (+304), 1x1/2if 117,688 (+304), 8x8/1if 129,928 (+304), 8x8/2if 131,224 (+304).

Only the platform's 8x8/2if image passes a tile: 60.0 -> 60.5, its ledger entry raised to the cap as S14 debt.
The fixture's 1x1/2if (41.5 -> 42.0) and 8x8/1if (54.0 -> 54.5) are not ledgered points.

**8x8/1if's split image misses the ruling's timing floor at every directive** (a STOP condition):

| Directive | WNS (Slow) | WHS (Fast) | Floors |
|---|---|---|---|
| ExtraPostPlacementOpt (the recipe's) | +0.011 | +0.034 | WNS misses +0.030 |
| ExtraTimingOpt | +0.171 | +0.014 | WHS misses +0.030 |
| AltSpreadLogic_high | +0.215 | +0.014 | WHS misses +0.030 |

The two hold misses are one path, `milan_datapath/g_aaf_meter.aaf_clock_meter/s2_ts_r_reg[6]` ->
`grp_ts0_r_reg[6]/D` (milansoc_crg_clkout1). The setup miss is `KL_mbx_cdc/u_edit/rq_r_reg[80]` ->
`milan_datapath/amap_edit_oclaim_expect_r_reg[599]/CE`. Every build has 0 failing endpoints, meets the issue's floors
(WNS >= +0.030, WHS >= 0) in two of the three, and passes the identity gate. This lane changes no RTL: the image differs
from the base only in its firmware's bytes, 129,928 B of `rom` where the base has 129,624, in the same 56.0 RAMB36
(`img/base.txt`, `img/head.txt`). **The base misses identically.** The base's own 8x8/1if image (`659d7687`, its firmware), built at the recipe's
directive, gives the same figures on the same paths: WNS +0.011 on `KL_mbx_cdc/u_edit/rq_r_reg[80]` -> `amap_edit_oclaim_expect_r_reg[599]/CE`,
WHS +0.034 and +0.070 on the same MAC converter path, identity rc 0 (`image/base-659d7687-8x8-ExtraPostPlacementOpt.txt`). The route
does not see the firmware's bytes, so the miss is the base's at that directive.

## 5. Bench

**(b) The burst on the board, on its current image (no reflash), 2026-11-15 20:35-20:38Z** (`bench/`). Under the
bench lock, the in-house harness's own persistence scenario as the rehearsal left it: its harness at `ff474d45` with
only the rehearsal's recorded `power.sh` boot-line patch (a copy in this lane's scratch, since the shared clone had
since gained another lane's uncommitted format-step change), its settings file (`bench.env.a783`, only the power log
directory re-pathed), the rehearsal's per-feature settings (`CERT_POWER_APPROVED=1 CERT_POWER_OFF_S=8
CERT_BOOT_S=17`). The runner only checks the test machine (AVB stack stopped, the owner-approved PHY setting, link up)
and stops rather than change it; `con_poll.py` sent `milan_status` once a second from the run's start to the cut and
decoded PP_STAT's store bits (`milan_csr.sv` A_PP_STAT; the split drives them from the store, `milan_datapath.sv`
`i_ctl_nvm`). HUPCL was already off.
- The burst: 39 SET_NAMEs, every one SUCCESS, the last answered 880.6 ms after the first (`persist-1.setname-pacing.txt`,
  from the harness's own capture; 3 commands the AECP limiter refused were resent after 250 ms).
- The store, read before the cut (`persist-1.console.txt`): clean at 20:36:22.78Z, **dirty 1** at 23.81Z (the burst
  marked), **pend 1** at 24.84Z (the save in flight), then from 25.87Z through ten readings to the cut at 35.24Z
  **backed 1, dirty 0, pend 0, stale 0, img_valid 1, verdict 0 (OK), alarm 0**: a verified save, nothing dirty, no
  failed attempt, no attempts exhausted, nothing in flight, about 10 s before the cut.
- After the cold cycle the same five names were their defaults: AUDIO_CLUSTER 22, 23, 24, CLOCK_DOMAIN 0, CONTROL 0
  (`persist-1.summary.txt`, the run's result in this lane's words; the raw run log is not kept). The scenario's own
  restore set the names back after the second cycle.
- So on the board too the store finished in time and believed it held every change: the five marks never reached it.

**(a) The burst in the save harness, at the base firmware** (the `replay` tree: `659d7687` with only the harness
commits, its burst pacing at `3d9cd3e0`'s; receipts `cause/harness-replay-1x1/`): `save-burst` at 1x1/1if, every
name set and read back as the controller does (78 frames in 850 ms, three 250 ms resends, as the bench's 877.6 ms),
under the held load, cut 10 s after the last frame: **one save; names 34 to 38 never durable and missing from the
authoritative container at the cut (sequence 1)**; the other 34 durable 1,489 to 2,338 ms after their responses.
`save-flight` at the base: the change in flight durable 2,020.4 ms after its response, its next save after 36 steps
(its window), not the 19 of its capture and seal.
At 8x8/1if the base firmware **traps** during the burst (`cause/harness-replay-8x8-1if/trap.txt`): 8 load access faults
(cause 5) at PC `0x1c98`, `deliver` in `ctrl_app_aecp.c`, from 0.28 s after the burst's first SET_NAME. In the harness's
fixture image `image_state.pending[9]` and `[10]` are the AECP bridge's first two words, its `app` and `aecp` pointers:
the names of ordinals 66 to 106 (ids 288 to 328), which the descending burst marks first, set bits in them. The base's
change in flight there took 7,049.8 ms from its response to durable, over the 5 s target, at a step a centisecond.

## 6. Open items

- Item 4 of the ruling: this lane syncs onto #919's review head; at the start #919 had no review head (its branch at
  the base). No pass of this lane's carries a PHY poll slice, since none exists yet.
- The decision the STOP asks for (8x8/1if's image timing). Until it is made, no REVIEW READY is posted.
- The suite sweep at `54280c94` was unfinished when this record closed (section 4): 18 suites not yet run, and
  `gptp_shadow`, `media_phase` and `milan_dp` to be judged alone. The next round's head will need its own sweep in
  any case (the sync onto #919).
- The sync onto #914: 8x8/1if's stated-cost lines are within #914's statements. The tightest is the polls base,
  23,251 of 23,500 cycles. Of the rise over #914's own measurement (21,995), 731 cycles in the pass that delivers a name
  are this change's `nvm_mark`. The sync re-measures it on the merged image, and the rule (measurement + 5 %) may move
  that statement.
- The verify table of the workflow replica lists the rtl-fast jobs outside this lane's gates (verilator-lint, the
  yosys jobs, publication-census, split-cdc, bdd-conformance) as not run: this change has no RTL, tooling or census
  input.
- The `docs-check-no-git` job's own steps pass (rc 0 each). The replica's after-job `git status` cannot run once that
  job strips `.git`, which it does by design.
- Scratch: build trees, image builds and clones stay in the lane's scratch until the next round (13 GB, under the 20 GB
  cap).

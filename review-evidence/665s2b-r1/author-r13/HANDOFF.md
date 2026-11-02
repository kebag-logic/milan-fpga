# [A683p] #665 lane S2b, round 13 (HANDOFF)

**Status: REVIEW READY** at `4f58214f457e963243a1fe6b86c6af161e97f26f` (2026-11-02); every gate rc 0 there (section 6). Start head `c954b8a91e720f87d2dfa9294c8501058dc55df3` on `665-s2b-cycles`; commits are added on top, no rebase, no force, no merge. PR target `dev-soft-core` (`a68536fa`, not moved). Nothing pushed by this lane.

- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked); the head contains `origin/dev-soft-core` `a68536fa` (checked).
- Authority: the round 13 assignment (issuecomment-6573625213); the round 12 reviews R711-2 (PR #810 issuecomment-6573244887) and R712-2 (issuecomment-6573608668); earlier assignments and the owner decisions of 2026-10-31.
- TAKEN: issuecomment-6576862729 (`TAKEN-COMMENT.md`).
- REVIEW READY: issuecomment-6588508497 (`REVIEW-READY-COMMENT.md`).

## Contents

1. Outcome against the assignment
2. Changes (file:line, reason)
3. New checks, planted mutants and failing words
4. Method
5. Measurement
6. Gates
7. Findings, decisions for the manager
8. Run history

## 1. Outcome against the assignment

Every measured row the CPU decides and every pass fits at 100 MHz, at both points, in both arms, with the two drafts staged and without them, a save in progress and both links changing at once included. No store phase needed an amendment of the share, so this is REVIEW READY, not STOP.

| Item | Outcome | Where |
|---|---|---|
| 1. A save in a composed window | Met. THE STEP: the step only in a pass that took no input, only while 1.0 ms of the share is left, owed once. R711-2's x-save and y-save windows reproduce exactly at `c954b8a9` (2.388 and 2.716 ms) and fit at this head (1.628 and 1.978 ms). Each store phase's flash cost measured at both points (section 5). `backlog-adp`'s window in each flash phase (blank check, program, verify) at 8 tick phases, both points, both arms, with and without the drafts: 0 of 99,289 passes over, graded by `grade.pass_share`. The planted store step: `CONTROL store-step-unbounded caught`, 5 windows over the share with every row within its bound. The save from the change to durable at 8x8: 4,697.1 ms before, 4,697.4 ms after; #823's 0.5 s not claimed, and said so in the docs and the PR body | `ctrl_loop.h` THE SHARE and THE STEP; `SPLIT_CONTROL_MEMORY.md` section 13, "A save in a composed window, and both links at once" |
| 2. A joint link change | Met. One interface built a pass. `y-links` 1.761 / 1.817 ms and `x-links-same` 1.543 / 1.560 ms, arm A / arm B, 0 over. The plant `joint-reset-builds-both` fails `Srp.JointLinkChangeBuildsOneInterfaceAPass` ("a pass builds one interface at most") | `srp_mbx.c`, `srp_bounds.h` |
| 3. The boot simulation's flash window | Met. The boot SoC calls `milan_soc.ctrl_uncached_flash` and refuses any other window; `PLANT flash-window-cached: caught`; `run.py` at both shapes; README figures restated from the runs at the code head | `tb/verilator/ctrl_split_boot/` |
| 4. Stale statements | Met. The three F4 lines (SRP README share 2.0 ms, AECP README 20 ms bound, the store README's cadence), the platform README's 58.5 tiles; the gPTP additions from the table's units, each a mean or a bound, and their effect on the 8x8/2if margins | `SPLIT_CONTROL_MEMORY.md` section 14, "gPTP's share, an assumption" |
| 5. Residue | Met. R711-2-R1: the save time in absolute terms in the PR body and at `SPLIT_CONTROL_MEMORY.md:1304`; R712-2 RESIDUE-1: the harness README's arm B line; S1: the interface reset clears `listener_present` | as named |
| Exit | Every measured row and pass fits at 100 MHz, a save in progress included. The 32x32 estimate is restated, since its figures moved | section 5 |

## 2. Changes

Commits on `c954b8a9` (one-line subjects, no body, no trailers):

| Commit | Subject (short) |
|---|---|
| `8164850e` | The store's flash step only in a pass with 1.0 ms of the share left (THE STEP); `ctrl_plat` ledgered |
| `e9cb4b46` | One interface built a pass; `listener_present` cleared by the reset |
| `5a1b5eee` | The harness: every pass held to the share, idle ones too; a save's windows; the planted store step |
| `8ec54db5` | The split boot simulation on the product's uncached flash window |
| `800a056c` | A save's windows' save inside the wait for MAAP; a window outside its flash phase refused |
| `091308ba` | Three planted defects kept compiling under `-Werror` |
| `ebde56f0` | The boot SoC plant as the call made a no-op in the export's own process |
| `73285c9e` | The coverage ratchet, through its generator |
| `83709d3f` | The store's step only in a pass that took no input; the harness plant takes it in every pass |
| `4625be27` | A save's flash phase read off what came before its window |
| `8918536e` | The skipped-recreate SRP plant re-anchored at the comment the one-build pass left |
| `3e0de521` | The coverage ratchet for the step's pass that takes no input |
| `c13ef319` | The phase checks' helper documented (idiom gate) |
| `5688b627` | A save's flash phases told apart by its pages alone |
| `dd025320` | `save_window.py` registered with the boundary gate |
| `b49a001d` | The planted store step judged per window: a pass over the share with every row of that window within its bound |
| `b2fd8d49` | The step's measured cost in the loop's and the store's comments (comments only) |
| `6ecd1806` | The SRP, AECP and platform READMEs' stale lines |
| `e15f1350` | THE STEP in `MAILBOX_SPLIT.md`, the port arm's row, the store README's step costs and save time |
| `fb923f25` | The boot README's figures on the uncached window |
| `8684e8db` | `SPLIT_CONTROL_MEMORY.md`: the ledger and fit at this head, the round's subsection, the gPTP additions, the 32x32 estimate |
| `6abf30e1` | The harness README: a save's phase read off its page programs alone |
| `4f58214f` | The store README's step costs linked to their section (docs gate) |

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/loop/ctrl_loop.h:66`, `:79-81`, `:83-97`, `:135`, `:153-156`, `:191-194` | THE STEP: one deferrable client at the end of a pass; `CTRL_LOOP_SHARE_US` 2000; THE SHARE's slices name the store's step and SRP's one build a pass | Item 1: a store step beside the heaviest pass took it to 2.39 ms (x-save) and 2.72 ms (y-save) |
| `sw/firmware/ctrl/loop/ctrl_loop.c:66`, `:158`, `:170-171` | `ctrl_loop_set_step`; the deadline read once as the pass starts; the step called after every poll of a pass that took no event and no record (`work == 0u`), its owed result keeping the loop passing | The pass knows its own time, so the step can be held out of a pass that has no room; and a step in a pass that takes records lengthens every record still waiting: with the room gate alone the last SRP record of a save's 8x8 window took 18.21 ms (first attempts) |
| `sw/firmware/ctrl/test/test_plat_boot.cpp` B10 | Two passes a tick: the one that takes the tick, then one that takes nothing | The store's step is taken by the pass after the tick |
| `sw/firmware/ctrl_nvm/nvm_store.h:68-74` | `NVM_STEP_US` 1000: a step's stated cost, the program's issue (95,386 cycles with the store's own, 0.95 ms, measured) being the longest | The step is admitted only while that much of the share is left |
| `sw/firmware/ctrl_nvm/nvm_store.c:789`, `:798`, `:811` | `nvm_store_tick` owes one step (not counted), `nvm_store_step` takes it only with `NVM_STEP_US` before the deadline, `nvm_store_clock` the port's microseconds | The centisecond pacing stays; a deferred step is taken by the next pass with room, and the passes it waited through owe it once |
| `sw/firmware/ctrl/plat/ctrl_plat.c:260-261`, `ctrl/test/ctrl_aecp_image.c:133-134`, `ctrl/test/rv32_image/image_main.c:207-208`, `:219-220` | Each binding: the tick as the centisecond consumer, the step and its clock as THE STEP | Every image that runs the store |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:223`, `ctrl_plat_image.py:45` | The required symbols name `nvm_store_tick` and `nvm_store_step` | The step inlines the service, so `nvm_store_service` is no longer what an image must hold |
| `sw/litex/ctrl_memory.py:217`, `ctrl_memory_ledger.py:26` | `ctrl_plat` 19,960 B, and 17,160 / 18,664 / 17,808 at the other points | The loop's four new fields; the ledger names the struct's size so a change refuses until measured again |
| `sw/firmware/ctrl/srp/srp_mbx.c:837-841`, `:867-872`, `:876-877`; `srp_mbx.h:95` | `builds_first`, the deferral of a second build, `build_turn` | Item 2: both links changing together built both interfaces in one pass, 2.08 ms (y-links) |
| `sw/firmware/ctrl/srp/srp_mbx.c:791` | The reset clears `listener_present` | Item 5, R711-2-S1 |
| `sw/firmware/ctrl/srp/srp_bounds.h:16-20` | The build bound restated | Item 2 |
| `tb/verilator/ctrl_service_budget/grade.py:827` (`pass_share`) | Every pass, those with no mailbox write too (each idle run's longest) | A deferred step can be all such a pass does, and a pass with no mailbox write was never graded |
| `grade.py:805` (`save_phase`, by pages alone since `5688b627`), `:789`, `:657` (`defined_load` through `save_window.row`) | A save's window must open inside its flash phase of the first save | The windows' timing is checked, not assumed |
| `tb/verilator/ctrl_service_budget/save_window.py` (new) | `backlog-adp`'s window at eight tick phases of each flash phase of a save; `save`, the save alone | Item 1's staged groups and the save's duration |
| `tb/verilator/ctrl_service_budget/sim_main.cpp:386-391`, `:237` | `wait flash erase|program N`, `wait flash idle CYCLES` | A phase starts at the save's own flash event |
| `tb/verilator/ctrl_service_budget/build.py:46`, `:72-77`; `run.py:334-350` (`verdict`) | `store-step-unbounded`, a share control | Item 1's planted store step |
| `tb/verilator/ctrl_split_boot/boot_soc.py:93`, `:112-113` | `ctrl_uncached_flash`, and a refusal of any other window | Item 3 |
| `tb/verilator/ctrl_split_boot/run.py:99`, `:415`, `:438` (`SOC_PLANT`, `soc_plant`) | The SoC plant: `boot_soc.py` without the call, whose export must be refused | Item 3 |
| `sw/firmware/ctrl/srp/srp_mbx.c:791` and `ctrl/test/srp_mutants.py` `reset-skips-recreate` | The plant re-anchored at `// A failed recreate` | The one-build pass moved the anchor; the same defect is planted (`8918536e`) |
| `sw/firmware/gtest/coverage.ratchet` | Regenerated through `fw_coverage.py` | Every touched file still whole (`73285c9e`, `3e0de521`) |
| `sw/firmware/ctrl/test/ctrl_configs.py` `OUTSIDE` | `save_window.py` | The boundary gate's register of modules that name the firmware tree and compile nothing (`dd025320`) |
| `docs/design/SPLIT_CONTROL_MEMORY.md:26`, `:105` (ledger), `:257-266` (fit), `:1304`, `:1313-1426`, `:1428-1437`, section 14 | The round's subsection; the save's time before; the margin and a save's progress in "What is left"; the 32x32 estimate, the idle pass and the gPTP additions restated; the one-CPU table dated to `c954b8a9` | Items 1, 4, 5 and the exit's restatement |
| `docs/design/MAILBOX_SPLIT.md:323-336` | THE STEP in the loop's pass order | Item 1 |
| `sw/firmware/ctrl_nvm/README.md:239-262` (`:247` linked in `4f58214f`) | THE STEP, the step costs at both points, the save to durable, #823 not claimed | Items 1 and 4 |
| `sw/firmware/ctrl/srp/README.md:152-157`, `:221`; `aecp/README.md:310`; `plat/README.md:95`, `:117`; `ctrl/README.md:480` | The F4 lines, the one-build paragraph, 58.5 tiles, the port arm's checks | Items 2, 4 and 5 |
| `tb/verilator/ctrl_split_boot/README.md:42-43`, `:69`, `:79-86`, `:103` | The SoC's uncached window, the SoC control, the figures at the code head | Item 3 |
| `tb/verilator/ctrl_service_budget/README.md` | Idle passes held to the share; a save's windows; the store-step control; RESIDUE-1 | Items 1 and 5 |

## 3. New checks, planted mutants and failing words

| Check | Planted | Failing words |
|---|---|---|
| `LoopBring.L10StepBindingRefusals` | `step-binds-twice`, `step-binds-no-function`, `step-binds-no-clock` | "L10 a second step is refused"; "L10 a step with no function is refused"; "L10 a step with no clock is refused" |
| `Loop.L11StepLastWithTheDeadlineReadAtTheStart` | `step-before-the-polls`, `step-deadline-read-at-the-end`, `step-deadline-without-the-share`, `step-owed-lets-it-sleep` | "L11 after every poll"; "L11 the deadline is the share past the clock read as"; same; "L11 a step still owed asks for the next pass at once" |
| `Loop.L12StepOnlyInAPassThatTakesNoInput` | `step-beside-input` | "L12 a pass that takes a record does not take the step" |
| `NvmBoth.step_room` | `step_ignores_room`, `step_needs_more_room`, `step_owed_once_each`, `step_owed_lost_without_room`, `step_not_owed_after_a_short_pass`, `step_untaken_when_not_owed` | "a pass with less than NVM_STEP_US left takes no step"; "a pass with NVM_STEP_US left takes the owed step"; "the passes a step waited through owe it once" |
| `Boot.B10ABindAfterReadyIsWrittenBackThroughTheLoop` | `plat-store-tick-unbound`, `plat-store-step-unbound` (was `plat-store-service-unbound`) | "B10 the bind is written back by the store's service on the loop's tick" |
| `Srp.JointLinkChangeBuildsOneInterfaceAPass` (two interfaces) | `joint-reset-builds-both`, `build-turn-ignored`, `build-turn-not-moved`, `build-waits-beside-a-withdrawal` | "a pass builds one interface at most"; "the interface whose turn it is is built first" (two); "an interface due beside one still withdrawing is built at once" |
| `Srp.InterfaceResetClearsListenerPresent` | `reset-keeps-listener-present` | "the interface reset clears listener_present" |
| Harness: "a pass that writes nothing to the mailbox is held to the share too..." | `share: a pass with no mailbox write is not held to it` | The check's name |
| Harness: "each flash phase of a save is staged at eight tick phases..." | `save: four tick phases a flash phase`, `save: the program phase spread across one tick, not its step's two`, `save: the blank check staged after the first page program`, `save: the verify staged while the pages are programmed` | The check's name |
| Harness: "a save's window carries backlog-adp's defined load" | `save: a save's window carries no defined load` | Caught first as a refusal: "no defined composed load" |
| Harness: "a save's window is refused unless it opens inside its flash phase of the first save..." | `save: a window outside its flash phase is graded`, `save: the phase read off the last save, not the first` | The check's name |
| Harness: "the planted store step is caught by a pass over the share with every row within its budget..." | `share: the planted store step is judged as a budget control` | The check's name |
| Native control `--mutation store-step-unbounded` | the step taken in every pass, its deadline `+ 0x40000000u` | `CONTROL store-step-unbounded caught` (section 5) |
| Boot self-test: the SoC plant | `flash-window-cached` | `PLANT flash-window-cached: caught` |

## 4. Method

- **Reproduction.** The round 12 review's probe patch (`receipts/measure/P0-A8/probe-groups.patch`) on a clean clone of `c954b8a9`, 8x8/2if, arm A; its image is round 12's `6d8c4931`. The same build ran its lone save to 5.2 s (`z-save`'s wait lengthened) for the save's duration before this round.
- **Legs.** `tb/verilator/ctrl_service_budget/run.py` on clean clones (`scripts/clone.sh`), each a build, its groups, `--record-budget-findings --record-share-findings`, the CPU on `sys` at 100 MHz:
  - arm A every group at both points (`N-A1`, `N-A8`);
  - arm B (`--variant answering-ports`), and both drafts staged in each arm (lwSRP `fc06e7c0`, tsn-c-stack `6532c3b0`, `receipts/drafts-staged.patch`, gitlinks staged in the scratch clone only), on the four backlog rows, the 24 save windows and the lone save (`N-B1`, `N-B8`, `D-A1`, `D-B1`, `D-A8`, `D-B8`);
  - the planted store step at 8x8, arm A (`CTL-A8`);
  - R711-2's probe groups on this lane's code at 8x8: the x-save and y-save windows, `y-links` and `x-links-same` in arm A, the two link groups in arm B (`X-A8`, `X-B8`, `probe-groups.patch` in each);
  - the labelled 8x8/1if point for section 14's S column (`P81-A8`, `receipts/point-8x8-1if.patch`);
  - measurement only, a clone that prints every journal read and every pass that runs the flash port (`read-backs.patch` in each): the lone save at both points (`R-A1`, `R-A8`), for each step's cost and the time to durable, and the 24 save windows at 8x8, arm A (`R-W8`), for how long a step waits for a pass that takes it.
- **Heads.** Each leg's `run.log` names the head it started at. Legs started at `83709d3f`, `4625be27`, `5688b627` or `b49a001d`; no firmware, store or loop source changed between them, and the images agree: `N-A8` (`83709d3f`), `X-A8` (`5688b627`) and `R-A8` (`b49a001d`) built `2c677934`, `N-A1` and `R-A1` `0e8e1527`, `N-B8` and `X-B8` `e109fce8`. A leg whose grader changed after it started was regraded from its own clone with the later grader (its `regrade.log`). The final head adds documentation and two comments; its images are rebuilt and compared (section 6).
- Legs on this lane's unit and on units of their own on free CPU ranges (`cpu_ranges.py`).
- `scripts/rows13.py` and `scripts/fig13.py` build every row and share cell from the legs' `results.json`; `scripts/savewin.py`, `scripts/savephases.py`, `scripts/readback.py` and `scripts/stepwait.py` read the windows' and the lone save's passes off the logs; `scripts/estimate13.py` restates section 14; `scripts/fit.py` the fit table.

## 5. Measurement

The CPU on `sys` at 100 MHz in every leg; receipts under `receipts/measure/<leg>/` (`label.txt`, `run.log` with the start head, `build.json`, `image.txt`, `results.json.gz`, `table.md`, and the leg's analyses).

| Leg | Point, arm | Groups | Start head | Image | Result (its `run.log`) |
|---|---|---|---|---|---|
| `P0-A8` | 8x8/2if, A, at `c954b8a9` | R711-2's probe groups, `z-save` to 5.2 s | `c954b8a9` + probe patch | `6d8c4931` | x-save 3 of 6 over (2.388 ms), y-save 7 of 8 over (2.716 ms), y-links 2.081 ms, x-links-same 2.004 ms; save durable at +4,697.1 ms |
| `N-A1` | 1x1/1if, A | every group, 43 | `83709d3f` | `0e8e1527` | 0 refusals, 6 egress-held misses, 0 of 19,927 over |
| `N-B1` | 1x1/1if, B | backlog, 24 windows, save | `b49a001d` | `1168bf74` | 0 refusals, 0 of 10,496 over |
| `D-A1`, `D-B1` | 1x1/1if, A and B, drafts | backlog, 24 windows, save | `b49a001d` | `0ba1e0d6`, `4b8bcd06` | 0 refusals, 0 of 13,012 and 0 of 10,483 over |
| `N-A8` | 8x8/2if, A | every group, 42 | `83709d3f` | `2c677934` | 0 refusals, 0 of 27,214 over |
| `N-B8` | 8x8/2if, B | backlog, 24 windows, save | `b49a001d` | `e109fce8` | 0 refusals, 0 of 13,648 over |
| `D-A8`, `D-B8` | 8x8/2if, A and B, drafts | backlog, 24 windows, save | `83709d3f`, `4625be27` | `e2a1300b`, `a0230f91` | 0 refusals, 0 of 20,045 and 0 of 13,645 over (`D-A8` regraded with `5688b627`'s grader) |
| `X-A8`, `X-B8` | 8x8/2if, A; B | R711-2's probe groups; the link groups | `5688b627`, `b49a001d` + probe patch | `2c677934`, `e109fce8` | 0 over; x-save 1.628, y-save 1.978, y-links 1.761 / 1.817, x-links-same 1.543 / 1.560 ms; SRP last at most 16.62 ms |
| `CTL-A8` | 8x8/2if, A, `--mutation store-step-unbounded` | 24 windows | `4625be27` | `c4fd3cf8` | regraded with `b49a001d`'s verdict: `CONTROL store-step-unbounded caught: 5 group(s) with a pass over the per-pass share and every row within its budget, 10 with a row over its budget as well, 1 with a row over and no pass over, 0 refusal(s)`; 15 of 18,256 passes over, the longest 270,522 cycles |
| `P81-A8` | 8x8/1if, A (labelled point) | backlog | `b49a001d` + point patch | `e0b9a7bc` | 0 refusals, 0 of 1,271 over |
| `R-A1`, `R-A8` | 1x1/1if and 8x8/2if, A, measurement only | the lone save | `b49a001d` + read-back patch | `0e8e1527`, `2c677934` | each step's cost; durable at +2,018.4 and +4,697.4 ms |
| `R-W8` | 8x8/2if, A, measurement only | 24 windows | `b49a001d` + read-back patch | `2c677934` | 0 of 559,355 passes over; a step waits at most 16.95 ms (`step-waits.txt`), its pass at most 101,796 cycles |
| `first-attempts/room-only-8x8` | 8x8/2if, A, the room gate alone | 14 windows then finished | `800a056c` | | every pass within the share; SRP last 18.02 to 18.21 ms in four blank-check windows: superseded by `83709d3f` |

Figures (tables in `receipts/tables/section13.md` and `section14.md`, built by `scripts/fig13.py` and `scripts/estimate13.py`):

- **The share.** 0 passes over in every leg; over a save's 24 windows 0 of 99,289. The longest pass at 8x8 is 1.98 ms (`N-B8`, `backlog-adp@blank-7`), and it carries no step; a pass carrying a step is at most 1.02 ms at 8x8 (`R-W8`) and 1.22 ms at 1x1.
- **The rows.** Every row the CPU decides fits, a save in progress included. The least margin is 0.71 ms, the 8x8 last SRP record in a save's window, 17.29 ms in arm B (16.99 in arm A, 15.79 / 15.46 with the drafts). In the four backlog windows the 8x8 last SRP record is 16.56 / 16.46 ms, 15.88 / 15.96 at `c954b8a9`: each drain pass runs 68 more instructions but about 3,300 more cycles, half of them fetch waits from the moved code layout (the same pass at each head, `backlog-adp`, arm A, 11.1 ms into the window).
- **The store's steps** (`R-A1`, `R-A8`, flash port and store, CPU cycles): erase issue 5,051 / 5,112; busy poll 3,994 / 4,710; blank-check read-back 73,491 / 72,841; page program issue 95,373 / 95,386; verify read-back 76,234 / 76,737 (1x1 / 8x8).
- **A save to durable**, one save alone, no flash busy time: 8x8 4,697.1 ms at `c954b8a9`, 4,697.4 ms at this head; 1x1 2,018.4 ms. The other legs' `save-alone.txt` count read-backs off idle runs and agree at 8x8 (+4,697.3 to +4,698.2 ms); at 1x1 they see 26 of 27, an idle run holding two, which is why `R-*` were run.
- **The 32x32 estimate**, restated: the last SRP record 31.4 / 37.1 / 66.2 ms under S / L / U, the last AECP record 28.1 / 35.8 / 63.9 ms, the longest pass 3.5 / 4.9 / 7.9 ms.
- **gPTP**: at 8x8/2if the mean leaves 0.26 ms (0.39 ms over at the range's top), the bound 7.29 ms over; the longest pass 3.58 ms under the pass bound; at 32x32 5.1 / 9.5 ms, Pdelay 10.2 ms (fits) / 18.9 ms (does not).
- **The boot**, at the code head (`c13ef319`, lane pre-check): 25.515 ms / 64.885 ms to ready; the final head's runs are in section 6.
- **Fit** (`receipts/fit/fit.txt`): the platform image 58.5 tiles and the fixture 57.0 at 8x8 with two interfaces, within the ledgered 59.0 and 57.5.

## 6. Gates

Every gate on a clean clone of the final head `4f58214f457e963243a1fe6b86c6af161e97f26f`, each its own log and rc, never piped; receipts under `receipts/gates/`.

| Gate | Command (from the clone's root) | rc | Result | Receipt |
|---|---|---:|---|---|
| docs.yml, every `run:` step | `scripts/run_docs_yml.py` per job, `scripts/verify_docs_yml.py` (from 829-a725c) | 0 | 64 steps ran, all rc 0; 31 hosted-only steps not run, each with its reason; 0 bad | `gates/docs/verify.md`, `gates/docs/logs/` |
| The full sweep, 4 native shards | `native-shards.py` over `scripts/run_all_suites.sh --wait --shard k/4`, `MAKEFLAGS=-j4 --no-print-directory` | 0 ×4 | 65 of 65 suites (15, 17, 17, 16), 2,613,655 checks, 0 failures, 0 timed out | `gates/sweep/shard-k/spec/01.log` |
| Firmware self-test, 4 shards | `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard k/4` | 0 ×4 | `test_ctrl_firmware: PASS` each; shard 1's mutants 612 of 612 caught | `gates/firmware/fwshard-k.log` |
| The store's gate and its plants | `python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` | 0 | 5 shapes, 445 tests, all 116 planted defects reddened | `gates/firmware/nvmself.log` |
| Firmware coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8` | 0 | PASS (38 files) | `gates/lane/fw_coverage.log` |
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | 0 failures; the share control caught | `gates/lane/harness_selftest.log` |
| Boot simulation, both shapes | `python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir … [--shape endstation_ax7101_8x8]` | 0, 0 | PASS; 25.515 and 64.885 ms to ready, the README's figures exactly | `gates/lane/boot_1x1.log`, `boot_8x8.log` |
| Boot native controls and self-test | `… run.py --native-controls`; `… run.py --self-test` | 0, 0 | 6 of 6; 3 of 3 plants caught, `flash-window-cached` among them | `gates/lane/boot_native.log`, `boot_plants.log` |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 2 NOT RUN: gate 1b's `MAKEFLAGS += -e` mutation (this make), gate 11's calibration report (no mf48 build tree on this host); the same two at every earlier head | `gates/lane/test_builder.log` |
| behave | `cd tests && behave --no-capture -f plain` | 0 | 14 features, 508 scenarios, 2,330 steps passed | `gates/lane/behave.log` |
| `git diff --check` | against `a68536fa`, the merge base with `dev-soft-core`, and against `f4c9ad4f`, the base earlier rounds used | 0, 0 | clean | `gates/lane/diffcheck*.log` |
| Idiom, mailbox, census, lint, SoC, memory, boundary | `check_py_idiom.py`, `check_cpp_idiom.py`, `gen_mailbox.py --check --crosscheck` and `--selftest`, `publication_census.py --check --selftest`, `lint_rtl.py --check`, `test_soc_options.py`, `test_ctrl_memory.py`, `ctrl_boundary.py --require-rv32 --selftest` both halves, `fw_rv32_selftest.py --require-rv32` | 0 each | as their logs end | `gates/lane/` |
| Image identity | `scripts/imgcheck.py`: the harness's `build.firmware()` at the final head | 0 | 5 of 5 images the same as the legs' (`N-A1`, `N-B1`, `N-A8`, `N-B8`, `CTL-A8`) | `gates/image-identity.log` |

- The sweep's first attempt at this head stopped in every shard's preflight (`test_suite_cancellation.py`, `cancel-command-SIGINT`: "CLEANUP FAILED: owned descendants remain"); the script alone passed, and the second attempt is the row above. Both are kept (`gates/sweep-first-attempt/`).
- No gptp_shadow lifecycle failure (#833) occurred.
- The working tree after the lane gates is clean (`gates/lane/tree-after.txt`, empty).

## 7. Findings, decisions for the manager

- **The margin is thin.** The least margin of any row is 0.71 ms (8x8 last SRP record in a save's window, arm B), and the heaviest 8x8 pass is 1.98 ms of the 2.0 ms share; that pass carries no step and was 1.97 ms at round 12's head. gPTP's assumed bound (8.0 ms on a row, 1.6 ms on a pass) does not fit either; its mean (0.45 ms) fits the row.
- **The 8x8 last SRP record rose 0.5 to 0.7 ms in the backlog windows** (15.88 / 15.96 to 16.56 / 16.46 ms). Measured cause: 68 more instructions a drain pass (the clock read as each pass starts), about 3,300 more cycles, half of them instruction-fetch waits from the moved code layout. It fits; it is recorded in section 13.
- **A save's progress is not bounded.** The store steps only in a pass that took no input. In the heaviest window a step waited at most 16.95 ms and the window cost the save one tick; nothing bounds the wait under input that never leaves a pass empty. Recorded under "What is left"; no owner decision is asked here.
- **The step's room.** The longest step, a page program's issue, is 95,386 cycles (0.954 ms) of the 1.0 ms `NVM_STEP_US`; the margin is 0.046 ms. A slower flash port must restate the constant; `NvmBoth.step_room` and its plants hold the rule, not the figure.
- **Durable time at 1x1 needed a measurement-only build.** The harness gives passes with no mailbox write only as their run's longest, so a run can hide a read-back; `R-A1` and `R-A8` print every pass that runs the flash port. The scaffold is a receipt (`read-backs.patch`), not on the branch.
- **Not run:** any hardware or bench step (none assigned); a Vivado route (none needed). docs.yml's hosted-only steps are listed with their reasons in `receipts/gates/docs/verify.md`.
- No open question blocks REVIEW READY.

## 8. Run history

- 2026-11-02 13:09 CET start; 13:12 TAKEN.
- 13:17 the head's reproduction, R711-2's patch on a clean clone: x-save 183,886 / 201,045 / 210,688 / 238,763 / 155,896 / 155,896 cycles, 3 of 6 over; y-save 7 of 8 over, the longest 271,599 (2.716 ms); y-links 208,096 (2.081 ms); identical to R711-2's.
- 13:20 to 14:13 the step, the joint link change, the harness's save windows, the boot window; the firmware suite, the store's suite, the harness self-test and coverage on the working tree, each rc 0.
- 14:00 the dev leg's blank-check windows at 8x8: 0 passes over, the longest 1.90 ms.
- 14:13 the code head `800a056c`; the legs start. 14:25 a pre-check of the new plants alone, through their own campaigns: three escaped as compile failures under `-Werror` (`091308ba`); the boot SoC plant escaped, its copy unable to import the budget SoC (`ebde56f0`).
- 14:55 the ratchet (`73285c9e`); the sweep starts as four units at that head; 15:22 firmware shard 1 there: 611 of 611.
- 15:55 regrading the 8x8 leg's finished save windows: every pass within the share, but the last SRP record 18.02 to 18.21 ms in four blank-check windows, and one program window refused by the phase guard although inside its phase. The legs stop.
- 16:00 `83709d3f`: the step only in a pass that took no input; the firmware suite and the affected plants pass; the legs restart at that head on fresh clones, the 8x8 draft legs and the firmware shards as units.
- 16:20 `4625be27`: the phase guard reads a save's phase off what came before the window; the clones move to it before any leg grades.
- 16:20 to 17:57 `5688b627` (a save's phases by pages alone), `c13ef319`, `dd025320`; the lane pre-check at `c13ef319`, every gate rc 0 but the boundary gate (fixed by `dd025320`).
- 17:45 `b49a001d`: the planted store step judged per window; `CTL-A8` regraded: caught.
- 18:11 to 19:29 the legs finish and are kept: `X-B8`, `P81-A8`, `N-A1`, `D-A1`, `N-B8`, `N-A8`, `D-B1`, `N-B1`.
- 18:16 to 18:39 `R-A1`, `R-A8`: the lone save on a clone that prints every pass running the flash port; durable at +2,018.4 and +4,697.4 ms.
- 18:59 to 19:48 `R-W8`: the 24 windows on that clone; a step waits at most 16.95 ms.
- 19:49 the docs and two comments (`b2fd8d49` to `8684e8db`); the gates start there, and stop at 19:51 when the harness README's `save_phase` line is found stale; `6abf30e1` fixes it and every gate restarts at that head.
- 20:15 docs.yml's `docs_check` at `6abf30e1` finds `sw/firmware/ctrl_nvm/README.md:247` naming `SPLIT_CONTROL_MEMORY.md` without a link; the gates stop, the text gates pass on the working tree with the link, `4f58214f` commits it, and every gate restarts at that head, the sweep on 48-63, freed meanwhile.
- 20:17 the sweep's first attempt at `4f58214f`: every shard stopped in its preflight, `test_suite_cancellation.py`'s `cancel-command-SIGINT` case reporting "CLEANUP FAILED: owned descendants remain" (`receipts/gates/sweep-first-attempt/`). The same script run alone in shard 0's clone at 20:33 passes; no script changed since `6abf30e1`, where all four shards' preflights passed. 20:35 the second attempt: every shard's preflight passes; its results are section 6's.
- 22:07 every gate at `4f58214f` rc 0; receipts collected and indexed; REVIEW READY.

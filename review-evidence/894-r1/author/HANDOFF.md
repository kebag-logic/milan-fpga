# 894-a773: #894 round 2 (build the 1x1/1if tier design), HANDOFF

**Status: REVIEW READY.** Head `12180198b087d4cfdd531d0de5d3753211b35616` (`8cc3e5d3`, C3: every cost measured on the image under the tiers, the larger stated, and the slice the rule picks at those costs, 1,200 us at 1x1/1if; then the docs restated). The full gate pass ran once on it (section 4); the 1x1/1if legs measure `8cc3e5d3`'s image and the 8x8/2if legs `9afbbbe2`'s, each leg's run image byte-identical at the head and each leg regraded there (head-gate method, as #810 round 28's).

- Lane: branch `894-tiers`, base `f9442a10ff7e673c6e65874ca7629b49201c589d` (round 1 head; two commits on #810 round 28 head `66f71326`). Nothing is pushed.
- TAKEN: #894 issuecomment-6813962419 (`TAKEN-COMMENT.md`). REVIEW READY: #894 issuecomment-6839788052 (`REVIEW-READY-COMMENT.md`).
- Ruling: #894 issuecomment-6813855717 (round 1 STOP ruling; the aecp_ready change decided under (a)-(d); the slice = largest least relative margin at 1x1/1if; 8x8/2if measured, not gated).
- Measured firmware: `9afbbbe2`, the head, at both points: legs L1A and L1N on a clean clone of it, L8A and L8N on a clone of it whose ledger plans 58.0 RAMB36 for measurement only (F1), started 07:57 CET. Earlier legs on `3f469cef` and `b7611ca4` were stopped or set aside when the image changed (section 6); the 8x8/2if figures of F2 and C1 come from `3f469cef`'s leg, whose SRP and AECP code paths in question `9afbbbe2` changes only as C1 states.

## 1. Changes (file:line, reason) — firmware (`3f469cef`)

- `loop/ctrl_loop.c` `service_rx` (`rx_left`): each take records whether it ended on its limit (records may remain) or on an empty ring / module not ready. The tier-1 test reads this, so an ordinary pass makes **no extra mailbox read** (the ADP/ACMP per-path access bounds, `ADP_MBX_LAT_*`, `ACMP_MBX_LAT_*`, are unchanged).
- `ctrl_loop.c` ordinary pass: tier 1's first channel (`first_ch`, AECP) past its cap to `CTRL_LOOP_DRAIN_RECORDS` while the pass has spent at most `CTRL_LOOP_DRAIN_US`; every other tier-1 channel only once the first's take left none (AECP first); then tier 2, THE DRAIN's channel (SRP), only once tier 1's takes left none (`tier1_done`), in a slice ending `CTRL_LOOP_SLICE_US` after the pass started, a record started only while the slice holds `CTRL_LOOP_SRP_UNIT_US` (the load gate's `record.srp`); `drained` when SRP's take left none.
- `ctrl_loop.c` passes given whole: THE TRANSMIT's build and THE RETRY's round are tier-2 slices from the pass's start, taken after an ordinary pass that left tier 1 holding nothing (or, after a pass given whole, while `tier1_holds()` finds none — the only extra reads, and only with a tier-2 client bound); the round only once SRP is drained too (SRP first); a queue's first notice is tier 1's: a round of one beside held work (`round_one`, `retry_first`). THE STEP's aged pass stands as built. Rounds are told what their slice has left (`round_of(l, end)`, `slice_end()` capped at the pass's deadline).
- `ctrl_loop.h`: `CTRL_LOOP_SLICE_US 1300u`, `CTRL_LOOP_SRP_UNIT_US`, `CTRL_LOOP_BUILD_MOST`, fields `first_ch`, `retry_first`, `round_one`, `tier1_done`, `drained`, `rx_left`; THE TIERS replaces THE DRAIN's text; THE TRANSMIT's and THE DRAIN's as-built pass-count derivations (`CTRL_LOOP_TX_*`, `CTRL_LOOP_SRP_*`, `CTRL_LOOP_DRAIN_TAKES`) removed: they describe the loop before the tiers.
- `ctrl_transmit_fn(void *ctx, unsigned most)`: the loop tells THE TRANSMIT's client how many MRPDUs its slice holds (`CTRL_LOOP_BUILD_MOST`: 2 at 1x1/1if, 1 at 8x8/2if).
- `srp/srp_mbx.c` `transmit`: makes at most `most` MRPDUs, resumes at the next participant (`tx_resume`) with its declarations already made, reclaims at the slice boundary as the next build would (else a record between the slices finds no room: found by `SrpRetry.OversizedValid...` at 2 interfaces), and `reset_interface` ends a build it was resuming.
- `aecp/aecp.c`, `aecp.h`: the owed-notice queue (`struct aecp_owed`, `cfg.owed`/`owed_slots`, `owed_head`/`owed_count`/`owed_recipient`). A command whose notice fits a slot (`AECP_OWED_BYTES` 128) has its response committed in the record's turn and its notice queued (`owe`), so AECP takes its next record; the poll sends the queue's oldest notice, one a poll, before the response buffer's own (`notices`); a longer notice stays in the response buffer as before, after the queue. `aecp_ready` is false while the queue is full. THE RETRY waits while the queue holds notices (`round_waits`). `fan_out` takes its frame, requester and cursor.
- `aecp/aecp_mbx.c`: AECP is tier 1's first channel; a round beside held work is a queue's first notice alone; `retry_first` kept. `aecp_mbx.h`: `AECP_MBX_OWED_SLOTS` (16 at 1x1/1if = the AECP burst; 0 at 8x8/2if, whose sram has 144 to 208 B left under its ledger); `AECP_QUEUED_FIRST_MS`/`AECP_QUEUED_MS` = decision D's 20/125 ms at 1x1/1if, the stated 22/62 ms at 8x8/2if; `AECP_QUEUED_PASSES`, `AECP_QUEUED_CEILING_MS` and the loop search (`ctrl_retry_search.py`, deleted) retired: the queued notices are the tier model's rows.
- `plat/ctrl_plat.c`, `test/ctrl_aecp_image.c`: the queue's storage at 1x1/1if.

## 1b. Changes at `b7611ca4` (file:line, reason)

- `loop/ctrl_loop.h:261-268` `CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 1050u : 1300u)`: the ruling's rule (largest least relative margin over the five rows at 1x1/1if) at the datapath events' measured costs picks 1,050 us on the 50 us grid (0.2835; 1,300 us gives 0.271); 8x8/2if keeps 1,300 us (I5).
- `tb/verilator/ctrl_service_budget/rows_tiers.py:72-73` `DATAPATH_US`: each datapath event at its measured cost (section 3) where it assumed `event.AECP`'s 60/95 us; `:228-249` `Design.slice_us == 0` is the tree's slice at each point (`at_point`), `BUILT = Design(0, ...)`; `:308-345` `aecp_passes` and `tier1_records` split out of `tiered` (the idiom gate's 100-line function rule; output byte-identical across every model and design); the module docstring restated (it is now the flip check's rows).
- `slice_grade.py` (new): round 23 item 1's gate, every tier-2 slice held to its point's `CTRL_LOOP_SLICE_US`; wired into `grade.grade` (`passes.slices`) and `run.stated_misses` (`STATED`, fails the run), a `SLICES` line (`run.print_slices`).
- `grade.py:192-194`: the testbench's `DATAPATH` pulse lines are parsed as pads (they were refused: the `datapath-events` group could not be graded at `3f469cef`).
- `datapath_window.py` (new): the `datapath-events` group, moved out of `scenario.py` (the idiom gate's 1,000-line module rule), each recorded script byte-identical.
- `sim_main.cpp:600`: the pulse kinds' table as `std::array` (the C++ idiom gate read the C array's initializer as a multi-declarator); no warning added.
- `selftest_round.py`: `slice_checks` (each kind at the length and a cycle over, at each point, SRP's from its pass's start, a build pass's round its slice's, named and failing the run) and `datapath_checks` (a pulse line graded, the group's posts), run from `round_checks`; `selftest_mutants.py`: 8 slice plants.
- Docs: `SPLIT_CONTROL_MEMORY.md` section 13 (THE TIERS: the measured costs, the slice, the rows at each point; the queued-notice table; the flip paragraph), `FR_NFR.md` 3.4.1 (the harness's checks stated, not its results), `MAILBOX_SPLIT.md`, the AECP, SRP and harness READMEs, `tests/README.md`; `whole_grade.py`, `round_grade.py` and `selftest_share.py` docstrings (the retired search).
- Lines over 120 columns wrapped in the mutant drivers, `poll_items.py`, `rows_tiers.py` and the behave steps (the idiom gate); the plant lists are unchanged (compared).

## 1c. Changes after `b7611ca4` (file:line, reason)

- `9afbbbe2`: sw/firmware/ctrl/aecp/aecp.c:384 `transmit(a, drains)`; sw/firmware/ctrl/aecp/aecp.c:889 the poll sends the response and the notices first, inside AECP's send, as before the queue (C1); `aecp_owed_mutants.py` and the behave steps re-anchored; the docs' figures at the measured costs and each point's slice.
- `46d051c3`: sw/firmware/ctrl/test/test_port_loop.cpp:1706 `Loop.L27`'s deadline case from the constants (C2).
- `0cab1e04`: the coverage checks and their six plants (section 2); `sw/firmware/gtest/coverage.ratchet`, the five files' grown counts as `--write` renders them; `Srp.RefusedPeerDomainDoesNotSurviveLinkRestart` held at the reset; `srp_transmit_mutants.py` transmit-built-by-the-poll; `ctrl_service_hooks/hooks.py` H-NOTIFY's plants; the behave steps' annotations (C2).
- `51c0e04a`: sw/firmware/ctrl/test/ctrl_configs.py:227 `rows_tiers.py` in `OUTSIDE`; `whole_grade.py`'s entry reworded; `SPLIT_CONTROL_MEMORY.md` section 13's image figures at the head.
- `19247413`: sw/firmware/ctrl/test/ctrl_configs.py:231 and sw/firmware/ctrl/test/ctrl_configs.py:260: `slice_grade.py` and the steps in `OUTSIDE`.
- `ee35f22b`: sw/firmware/ctrl/loop/ctrl_loop.h:308 `CTRL_LOOP_BUILD_PASS_US` 955 us at 1x1/1if (the build pass measured 90,543 cycles under the tiers; `CTRL_LOOP_BUILD_MOST` stays 2, the image unchanged); tb/verilator/ctrl_service_budget/load_grade.py:152 tsn-c-stack#32's column the same; the rows it moves in the docs.
- `8cc3e5d3` (C3): every cost measured again at the image under the tiers, by #665 round 28's cost tools unchanged (`parts.py`, `eventcost.py`, `costs24.py`, `aecp_kinds.py`) over every leg at each point; each cost the larger of that and the committed table's, the gate's rule. tb/verilator/ctrl_service_budget/load_grade.py:120-131 and :150-160, both columns: at 1x1/1if an AECP record 205 to 235 us (22,256 cycles, every `notice-every` group: the record's turn now commits the response and queues the notice), ADP's timer slot 110 to 115, the TICK 40 to 45, a pass's events' fixed part 25 to 30; at 8x8/2if AECP's timer slot 95 to 105 and a notice 270 to 275 (the 58.0-plan image, F1). tb/verilator/ctrl_service_budget/poll_grade.py:58-63: the polls' base 155 to 160 at 1x1/1if; ACMP's owed frame 185 to 195 and a notice 270 to 275 at 8x8/2if. tb/verilator/ctrl_service_budget/rows_tiers.py:75 `DATAPATH_US` at 1x1/1if 35, 30 and 25 us (29.66, 25.37 and 20.74 measured at `9afbbbe2`'s image). At these costs the slice rule's choice is no longer 1,050 us: the last queued notice binds and 1,200 us has the largest least margin (0.2673; 1,050 us 0.2610, 1,250 us 0.2669, 1,300 us 0.2650), so sw/firmware/ctrl/loop/ctrl_loop.h:261-268 `CTRL_LOOP_SLICE_US` is 1,200 us at 1x1/1if (`rows_tiers --selftest`'s "the built design's slice not the rule's" refused the tree's 1,050 at the new costs, 508 of 509, until it moved). The 8x8/2if image is unchanged (the expression's 8x8/2if arm); the 1x1/1if image changes, so its three legs run again on it (M1A, M1N, M1B).

## 2. New checks, planted mutants and failing words

Each planted defect is run by its driver (`test_ctrl_firmware.py --self-test`), and is caught only when its named test fails on its words. The firmware suite's own run at the final head is in section 4.

**THE TIERS, `loop_step_mutants.tier_mutants` (16 plants, `ctrl_loop.c`):**

| Plant | Kill test | Failing words |
|---|---|---|
| tier1-others-beside-the-first | `Loop.L26TierOnesFirstChannelGoesFirst` | L26 and no other tier-1 channel's record while it holds one it would take |
| tier1-first-to-its-cap | `Loop.L26...` | L26 with a clock it goes past its cap while the pass has room |
| tier1-first-past-its-time | `Loop.L26...` | L26 and stops once the pass has spent CTRL_LOOP_DRAIN_US |
| tier1-held-by-a-module-not-ready | `Loop.L26...` | L26 a first channel whose module is not ready holds the others back no longer |
| tier1-held-by-an-empty-ring | `Loop.L20AnOwedBuildIsAPassOfItsOwn` | L20 the next pass calls the transmit though input waits, then an aged round |
| tier2-beside-tier1 | `Loop.L26...` | L26 tier 2 takes nothing while the first channel's take stopped at its limit |
| whole-beside-tier1 | `Loop.L20...` | L20 and the pass after it serves tier 1, not the build |
| whole-row-beside-tier1 | `Loop.L22PassesGivenWholeStandApartAsInputWaits` | L22 and none follows another while a tier-1 record is held |
| round-before-the-drain | `Loop.L27TierTwoRoundsComeAfterTheDrainInSlices` | L27 a round waits while THE DRAIN's channel was left a record (SRP first) |
| drained-beside-the-drain | `Loop.L27...` | L27 a pass that takes THE DRAIN's cap leaves a record of its channel |
| first-notice-not-tier1 | `Loop.L22...` | L22 a queue's first notice after that pass, though a record waits |
| round-one-never-told | `Loop.L22...` | L22 told it stands beside held tier-1 work |
| round-slice-is-the-share | `Loop.L27...` | L27 a round in a pass given whole has a slice from the pass's start |
| slice-end-past-the-deadline | `Loop.L27...` | L27 a round in a pass that took nothing has a slice from its start, and never past the pass's deadline |
| slice-starts-at-the-cap | `Loop.L23TheDrainIsTierTwoInASlice` | L23 and starts none once its slice has no room for a record's stated cost |
| transmit-told-a-whole-build | `Loop.L20...` | L20 told the MRPDUs its slice holds |

Re-anchored for the tiers, same intent: the RETRY/BUILD/drain plants in `loop_step_mutants.py`, `ctrl_mutants.py` rx-pass-unbounded, `acmp_mutants.py` rx-one-record-per-pass, `aecp_retry_mutants.py` retry-yield-ignored, `srp_mutants.py` srp-term-poll-frames-uncapped, `srp_transmit_mutants.py` transmit-reentry-unguarded and second-interface-starved.

**The owed-notice queue, conditions (a) to (c), `aecp_owed_mutants.py` (14 plants, run by `aecp_mutants.py`):**

| Plant | Condition | Kill test | Failing words |
|---|---|---|---|
| owed-newest-first | (a) | `Queued.BackToBackCommandsOfTwoControllersOweTheirNoticesInOrder` | (a) in the order their commands were taken |
| owed-requester-forgotten | (a) | `Queued.BackToBack...` | (a) two notices, each to the two registered controllers not its requester |
| owed-walk-restarts | (a) | `Queued.AQueuedNoticeResumesAtItsRecipient` | (a) the walk resumes at the recipient it stopped at |
| owed-long-notice-before-the-queue | (a) | `Queued.ALongerNoticeWaitsInTheResponseBufferBehindTheQueue` | (a) the queue's notice first, then the long one |
| owed-notice-before-its-response | (b) | `Queued.BackToBack...` | (b) each response is committed in its record's turn, and no notice yet |
| owed-drained-in-the-records-turn | (b) | `Queued.BackToBack...` | (b) each response is committed in its record's turn, and no notice yet |
| owed-ready-while-full | (c) | `Queued.TheOwedQueueIsBoundedAndHoldsTheNextRecordWhileFull` | (c) AECP is not ready while the queue is full |
| owed-slot-never-freed | (c) | `Queued.TheOwedQueue...` | (c) its slot free, AECP is ready again |
| owed-never-ready-without-slots | (c), 8x8/2if | `Core.WithNoOwedSlotsTheNextRecordWaitsForTheNotice` | command produces a response |
| owed-long-notice-queued | bound | `Queued.ALongerNotice...` | its response waits for the poll, as every notice's did |
| owed-not-queued | the change | `Queued.BackToBack...` | (c) a command's notice owed in the queue does not hold the next record |
| retry-first-never-cleared | first notice tier 1 | `Mailbox.ARoundBesideHeldWorkIsAQueuesFirstNoticeAlone` | and the queue's next is no longer its first |
| retry-round-one-ignored | first notice tier 1 | `Mailbox.ARound...` | a round beside held work builds a queue's first notice alone |
| retry-first-never-set | first notice tier 1 | `Mailbox.ARound...` | a queue's first notice is tier 1's from the attach |

`aecp_fan_mutants.py`: new notice-to-the-one-that-asked (`r->controller == ~requester`), killed by `Core.ANoticeIsAddressedToEachRecipientAlone`; the fan plants re-anchored on `fan_out`'s new signature.

Condition (d): `Queued.*` (4 tests, two controllers' back-to-back state-changing commands, `test_aecp.cpp`) and `tests/features/aecp_owed_notices.feature` (3 scenarios, its model's rules pinned to `aecp.c`/`aecp.h`/`aecp_mbx.h` text: a rule dropped from the source fails the scenario that states it).

**The resumed build, `srp_transmit_mutants.py`:**

| Plant | Kill test | Failing words |
|---|---|---|
| build-resumed-from-the-first-participant | `Srp.ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole` | a build resumed across slices sends the frames of the build made whole |
| build-whole-in-any-slice | `Srp.ABuildResumed...` | a slice that holds one MRPDU makes one |
| build-reclaim-left-to-the-next-slice | `SrpRetry.OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding` | adapter.received |
| build-resumed-past-a-reset | `Srp.ABuildResumed...` | a reset ends the build it was resuming: its new participants build whole, MSRP first |

`Srp.ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole` compares, byte for byte, the MRPDUs of a build made across slices (one MRPDU a slice) with those of the same build made whole (round 23 item 2's comparison against an unsliced build).

**Coverage checks and their plants (C2):**

| Plant | Kill test | Failing words |
|---|---|---|
| owed-tail-overwrites-the-head (`aecp_owed_mutants.py`) | `Queued.TheOwedQueueIsBoundedAndHoldsTheNextRecordWhileFull` | the queue's tail wraps to its freed first slot, its notices in their order |
| owed-depth-unbounded | `Queued.AQueueTooDeepOrWithNoStorageIsRefused` | (c) a queue deeper than its 8-bit counts |
| owed-slots-without-storage | `Queued.AQueueTooDeepOrWithNoStorageIsRefused` | (c) slots with no storage |
| owed-round-beside-the-queue | `Core.HeldRetryWaitsForTheRoundAndTheRoundForAnOwedResponse` | the round waits while the owed-notice queue holds a notice |
| owed-fan-over-the-held-notice | `Queued.BesideALongerNoticeTheQueuesGoesFrameByFrame` | the queue's frame by frame, the long notice's two through the fan port |
| holds-a-module-not-ready (`loop_step_mutants.py`) | `Loop.L22PassesGivenWholeStandApartAsInputWaits` | L22 a tier-1 record whose module is not ready holds none back (THE TIERS) |

**The slice gate (round 23 item 1), `slice_grade.py`, new:** every tier-2 slice (SRP's records from the pass's start, a pass given whole to a build with its round, every other round) held to `CTRL_LOOP_SLICE_US`; a slice over it prints `STATED` and fails the run. Self-test `selftest_round.slice_checks` (9 checks: each kind at the length fits and a cycle over is refused; SRP's slice from the pass's start, not its first record; a build pass's round is that slice's; named and failing the run). Seven grader plants in `selftest_mutants.py`, each caught by a check:

| Plant | Caught by |
|---|---|
| slice: no slice is held to its length | a slice of SRP's records at the stated length fits it and one a cycle over does not |
| slice: the stated length doubled | the slice is ctrl_loop.h's stated length, at every point |
| slice: SRP's records are not a slice | a slice of SRP's records at the stated length fits it and one a cycle over does not |
| slice: SRP's slice from its first record | (same) |
| slice: a build pass is not a slice | a slice of THE TRANSMIT's build at the stated length fits it and one a cycle over does not |
| slice: a build pass's round a slice of its own | (same) |
| slice: in bus cycles, not CPU time | a slice of SRP's records at the stated length fits it and one a cycle over does not |

**The built design in the flip check:** `flip_grade.py --design built` (default) reads `rows_tiers.BUILT`; `flip_grade.built_controls`: each row at each point against a bound 0.01 ms under its W (refused) and over it (passes), each counted source dropped (must shorten W), `rows_tiers.broken`, the default design not the built one; `AECP_QUEUED_MS` planted at 1250 must be refused. `selftest_mutants.py` "rows: the built design's rows by every source not held". `rows_tiers.py --selftest`: the built controls (the slice not the rule's: a slice other than `slice_choice`'s; the owed-notice queue's depth not counted).

## 3. Measurement

**The datapath events' sink cost** (assignment item 3), the `datapath-events` group (`datapath_window.py`: each event pulsed alone on every interface, eight times, 2 ms apart), measured on `3f469cef`'s builds (the firmware sinks are unchanged by `b7611ca4`): from the `mbx_event_take` that took the record to the next take, the take and every sink (ADP, ACMP, MAAP, AECP, the AECP application, SRP), the most of the group's records:

| Event | 1x1/1if: `3f469cef`, `9afbbbe2`, `8cc3e5d3` | stated (the most x1.05, up to 5 us) | 8x8/2if: `3f469cef`, `9afbbbe2` | stated |
|---|---:|---:|---:|---:|
| AVB_INFO_CHANGED | 27.08, 29.66, 29.66 us | 35 | 33.13, 31.51 us | 35 |
| AS_PATH_CHANGED | 26.10, 25.37, 25.37 us | 30 | 30.32, 29.59 us | 35 |
| AMAP_LIVE_WRITE | 15.41, 20.74, 20.74 us | 25 | 20.54, 20.73 us | 25 |

(The 8x8/2if image is the same at `8cc3e5d3`; C3: the 1x1/1if stated costs were 30, 30 and 20 us until `9afbbbe2`'s image was measured.)

`rows_tiers.py` assumed `event.AECP`'s 60 and 95 us. Receipts: `receipts/measure/datapath-*.json`. Every other cost, measured again on the image under the tiers (C3): `receipts/measure/costs-9afbbbe2-*.txt` (both points) and `costs-8cc3e5d3-1x1.txt` (the 1,200 us image: no cost above `9afbbbe2`'s, so the table and the slice rule's choice stand).

**Rows by every source at the built design** (`rows_tiers.py`, at the head):

| Point | Slice | R4 (20) | R5 (90) | R6 (90) | First (20) | Last (125) | MRPDU, reported (20) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1/1if | 1,200 us | 12.71 | 54.59 | 52.85 | 14.60 | 91.59 | 29.00 |
| 8x8/2if | 1,300 us | 42.47 | 187.97 | 178.28 | 20.25 | 647.23 | 89.01 |

`flip_grade.py --check --point 1x1/1if`: `RESULT: PASS`, rc 0. **The 1x1/1if long-window load** (`load_grade.py --check`): 0.470 at the pin, 0.457 with tsn-c-stack#32, ceiling 0.70 (8x8/2if 0.821 and 0.722, reported).

**The legs.** Six configurations. At 1x1/1if on `8cc3e5d3`'s image (the 1,200 us slice; byte-identical at the head, section 4): arm A every group (M1A, 95 groups: 38 before the power-off and 57 re-run on its build, merged) and the `answering-every-port` arm (M1N, 16 groups); at 8x8/2if on `9afbbbe2`'s, which `8cc3e5d3` and the head leave byte-identical: at 8x8/2if arm A's stress groups (L8A, 11 groups: the four backlog windows, the three save windows, `aecp`, `aecp-fanout`, `srp`, `datapath-events`) and the `answering-every-port` arm (L8N, 16 groups); arm B's `aecp` group at both points (M1B, L8B). Each regraded at the head (`receipts/legs/rg-*-summary.txt`, tables `*-table.md`).

**8x8/2if stress, every source at its contract rate.** The `backlog*` windows stage every channel's admitted burst at once (AECP 16, ACMP 12, ADP 8, MAAP 7, SRP 32 records) with a grandmaster change every 2 ms (15), a bound sink and 16 registrations; `notice-burst-<k>` adds the composed burst 6 ms after a queue of 40 notices' port answers, and the save windows hold a save in flight through it (`scenario.backlog_groups`, `notice_window.every_groups`, `save_window`).

**1x1/1if, by measurement** (3 legs)

| Tier | Row | Longest, ms | Bound, ms | Margin | Group |
|---|---|---:|---:|---:|---|
| SRP | srp | 9.044 | 90 | 0.900 | backlog-adp@program-aged2-5 |
| mrpdu | srp | 1.052 | 20 | 0.947 | notice-every-6 |
| tier 1 | acmp | 6.562 | 20 | 0.672 | notice-burst-3 |
| tier 1 | adp | 5.652 | 20 | 0.717 | notice-burst-5 |
| tier 1 | aecp | 4.605 | 20 | 0.770 | notice-every-6 |
| tier 1 | maap | 5.677 | 20 | 0.716 | notice-every-6 |
| queued notices | the first of a queue, the latest | 5.947 | 20 | | 16 queues |
| queued notices | every one, the latest of 192 | 17.228 | 125 | 0.862 | |
| egress held (tsn-c-stack #26) | backlog-owed.service.aecp.last | 61.505 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed | 62.413 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed_behind | 360.329 | 20 | | backlog-owed |

Heaviest work pass 156,127 CPU cycles (1.561 ms, THE SHARE 2.000 ms), notice-burst-2.
Longest tier-2 slices: build 90,543 cycles (srp), round 80,832 cycles (notice-every-5), srp 103,874 cycles (notice-every-1), against the slice's 120,000.

**8x8/2if, by measurement** (3 legs)

| Tier | Row | Longest, ms | Bound, ms | Margin | Group |
|---|---|---:|---:|---:|---|
| SRP | srp | 13.937 | 90 | 0.845 | notice-every-7 |
| mrpdu | srp | 5.572 | 20 | 0.721 | save-starved |
| tier 1 | acmp | 9.605 | 20 | 0.520 | notice-burst-1 |
| tier 1 | adp | 8.344 | 20 | 0.583 | notice-burst-1 |
| tier 1 | aecp | 5.648 | 20 | 0.718 | notice-every-0 |
| tier 1 | maap | 7.746 | 20 | 0.613 | notice-burst-1 |
| queued notices | the first of a queue, the latest | 3.572 | 22 | | 16 queues |
| queued notices | every one, the latest of 640 | 53.336 | 62 | 0.140 | |
| egress held (tsn-c-stack #26) | backlog-owed.service.aecp.last | 61.997 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed | 64.014 | 20 | | backlog-owed |
| egress held (tsn-c-stack #26) | backlog.owed_behind | 360.585 | 20 | | backlog-owed |

Heaviest work pass 228,022 CPU cycles (2.280 ms, THE SHARE 2.000 ms), notice-every-0.
Longest tier-2 slices: build 157,971 cycles (srp), round 73,427 cycles (notice-burst-6), srp 121,720 cycles (notice-every-5).

Least row margin per tier, by measurement: at 1x1/1if tier 1 0.672 (ACMP, 6.562 ms), SRP 0.900 (9.044 ms), the queued notices 0.862 (17.228 of 125 ms; the first of a queue at most 5.947 of 20 ms); at 8x8/2if tier 1 0.520 (ACMP, 9.605 ms), SRP 0.845 (13.937 ms), the queued notices 0.140 (53.336 of the stated 62 ms; the first at most 3.572 of 22 ms). The MRPDU rows (`mrpdu_grade.py`) are at most 1.052 ms at 1x1/1if and 5.572 ms at 8x8/2if, against 20. The three egress-held paths of tsn-c-stack #26 miss as round 28 recorded (6 instances of 945 at 1x1/1if and of 131 at 8x8/2if, 3 paths each).

Tallies at the head: M1A 0 refusals, 6 budget misses (the egress-held paths), 0 of 162,514 work passes over THE SHARE, 4 saves durable within their bound, no stated-cost finding; M1N 0 refusals, 0 of 280 probe instances missed, 0 of 24,583 passes over the share, 192 queued notices within; L8A 0 refusals, the 6 egress-held misses, 0 of 167,463 passes over the share, 3 saves durable, F2's four stated-cost lines; L8N 0 refusals, 0 of 736, 11 of 16,874 passes over the share (F3), 640 notices within; M1B 0 of 25, L8B 0 of 39.

## 4. Gates

The full gate pass ran once on the head, `12180198b087d4cfdd531d0de5d3753211b35616`, each workflow job and gate part on a fresh clean clone of it (`receipts/gates/`: `workflows-verify.md` the step table, `lane-summary.txt`, `gate-logs.sha256` every log's digest, `sweep-shard<k>.txt`, `dispatch.txt`). Earlier passes at `9afbbbe2`, `46d051c3`, `0cab1e04`, `51c0e04a` and `19247413` were stopped at their first failures (section 6), and the complete pass at `ee35f22b` is superseded by C3 (`receipts/gates-ee35f22b/`, `receipts/legs-ee35f22b/`); none is gate evidence. The runner and verifier are #810 round 28's (`run_wf.py`, `verify_wf.py`), pointed at this lane; their runner home links the pinned RV32 SDK as #810's did.

| Gate | Where | Result | Receipt |
|---|---|---|---|
| Every `run:` step of `rtl-fast.yml`, `rtl.yml`, `elaborate.yml` and `docs.yml` (the four a pull request to `dev-soft-core` triggers) | each job its own clone (`run_wf.py`) | **139 steps ran, 226 not run with a reason**; one step's verdict UNKNOWN: `elaborate-gates-1` gate_19 exit 92, `test_soc_timing_cuts` killed by its 900 s wall clock on the loaded pool (the other seven PASS). Run again alone in that job's clean clone with its environment and `LITEX_SIM_TIMEOUT=1800`: 8 of 8 PASS, rc 0. With it, every step rc 0 or not run with a reason; every job's tree clean after | `workflows-verify.md`, `wf-rerun/` |
| `firmware-unit` | its job | every step rc 0: `test_ctrl_firmware.py --require-rv32 --self-test` (shard 0) PASS, the saved-state store gate, `fw_coverage.py --check` PASS (39 files, `aecp.c` 532/532 and `ctrl_loop.c` 216/216 branches) | `gate-logs.sha256` |
| `firmware-control-mutants`, `-aecp-mutants`, `-srp-mutants` | their jobs | **697 of 697 caught**; 243 `[ok]`; 344 `[ok]`; 0 escaped; `test_ctrl_firmware: PASS` each | |
| `firmware-boundary`, `firmware-verilator` | their jobs | `ctrl_boundary: PASS` each | |
| docs.yml (6 jobs), elaborate.yml (3), rtl.yml (`full-ci-gate`, `yosys-tool`, `yosys-shards` 0 to 3), rtl-fast.yml's other 8 | their jobs | every step rc 0 | |
| `git diff --check` against the merge base `1d6bf555`, round 1's `f9442a10` and #810's `66f71326` | lane clone a | rc 0, no output | `lane-summary.txt` |
| `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`, `docs_check.py`, `ctrl_hot.py --self-test`/`--check` | lane clone a | rc 0 each | |
| The harness self-test (`run.py --self-test`) | lane clone a | `self-test: 0 failures`, 210 `MUTANT caught` | |
| `rows_tiers.py --selftest`; `--terms` | lane clone a | 509 of 509 controls refused; `--terms` rc 1 by design (8x8/2if's rows) | |
| `load_grade.py --selftest`, `--check` | lane clone a | 24 of 24; `RESULT: PASS`, 1x1/1if 0.463 at the pin, 0.450 with tsn-c-stack#32 | |
| `flip_grade.py --selftest`, `--check --point 1x1/1if`; `--check`, `--point 8x8/2if`, `--point 1x1/1if --design as-built` | lane clone a | 319 of 319; **rc 0, `RESULT: PASS`**; each of the other three rc 1 by design (8x8/2if; the loop before the tiers at R4) | |
| R711-6's and R712-6's probes, `git grep __attribute__`, hooks and target self-tests, `gen_mailbox.py --check --crosscheck`/`--selftest`, `lint_rtl.py --check`, `test_soc_options.py`, `test_ctrl_memory.py`, `make -C tb/verilator/milan_dp twin` | lane clone a | rc 0 each; hooks 28 of 28 checks, 96 of 96 plants | |
| `cd tests && behave` | lane clone a | 15 features, 511 scenarios, 2,346 steps passed | |
| `test_builder.py --require-rv32` | lane clone b | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN` (the two arms #810's rounds record, each with the tool's reason) | |
| `test_ctrl_nvm.py --require-rv32 --self-test`; `ctrl_split_boot` at 1x1, 8x8, `--native-controls`, `--self-test` | lane clone c | 455 tests, all 121 plants reddened; PASS (0 findings) at both shapes; 6 of 6 native controls; 3 of 3 plants | |
| The full sweep (`scripts/run_all_suites.sh` as four `native-shards.py` units on the session pool) | four shard clones of the head | 62 of 65 suites PASS, 0 in-suite failures; shards 2 and 3 exit 0. Three were killed by the wall clock on the loaded pool: `milan_dp` (4,800 s), `milan_dp_gm_steps` and `milan_dp_render` (1,800 s). Each was re-run alone in its shard's clean clone, as the sweep runs it (`rerun_suite.sh`: its make, then `suite_tally.py --verdict`), the wall clock doubled as the sweep's message directs: each make rc 0 and verdict rc 0 (`milan_dp` 35 min, `milan_dp_gm_steps` 17 min, `milan_dp_render` 14 min). All 65 PASS | `sweep-shard<k>.txt`, `sweep-rerun/` |
| The CPU budget harness at both points (S2's harness) | each leg's image built again at the head (`rg`, `rg8` clones) | each leg's run image (`build.json`'s ELF) byte-identical to the leg's (ELF and `objcopy -O binary`), and each sample group's log byte-identical (`compare_builds.py`, `head-build-<leg>.txt`); at 1x1/1if every image. At 8x8/2if the split SoC's two one-interface images, built only to export the flash port's CSR map (`build.py`, `flash_map`), differ in `CTRL_LOOP_SLICE_US`'s one-interface arm alone (12 instruction lines), and the map they export is identical. Every leg regraded at the head from its merged logs: 1x1/1if rc 0 (M1A, M1N, M1B: the egress-held paths only, no pass over the share, no stated-cost finding); 8x8/2if L8N, L8B rc 0, L8A rc 1 by F2 alone | `receipts/legs/` |
| The 8x8/2if harness build at a clean clone of the head, the committed ledger | `rg` | refused by F1, as stated | `harness-8x8-clean-head-build.txt` |

## 5. Findings, interpretations, open questions

- **F1: the 8x8/2if fixture image is over its 57.5-RAMB36 ledger**: at the head 664 B of rom (123,544 B against 122,880; `3f469cef` 808 B; round 1's head had 440 B to spare at 122,440). The harness's 8x8/2if build at a clean clone of the head refuses: `allocation over budget: 58 RAMB36 (rom 123544 bytes in 124928, sram 112432 bytes in 112640) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces` (`receipts/gates/harness-8x8-clean-head-build.txt`). `SPLIT_CONTROL_MEMORY.md` section 13 still states `3f469cef`'s figures (808 B, about 1,250 B larger); at the head the 8x8/2if image is 1,104 B larger than round 1's. The change adds 1,248 B of text at both points; at 8x8/2if, by symbol: `fan_out` +848 (now a function of its own, called for the queue's notice and the response buffer's) against `transmit` -712, `ctrl_loop_service` +340 (the tiers), `aecp_poll` +272, `respond` +196 (new), `aecp_rx` +120, `retry` +52, the rest 4 to 24 each. The queue's own code, dead at 8x8/2if (no slots, I2), is a few hundred bytes, short of 808, so compiling it out there would not recover the ledger alone. **Effect on the gates:** the CPU budget harness's 8x8/2if build plans the size fixture against the ledger (`build.py`, `LEDGERED_POINTS`), so on a clean clone of this head it refuses to build at 8x8/2if; no workflow job builds that image (the firmware suite's arms and `ctrl_memory_ledger.py` pass). The 8x8/2if legs run on a scratch clone whose ledger plans 58.0 RAMB36 for measurement only, never committed: the ledger is the owner's (#665 decision D3, owed to lane S14's hybrid XIP), and 8x8/2if is neither gated nor relaxed here. Needs an owner decision: the ledger at 8x8/2if, or 808 B of code out of that image.
- **I1: the slice.** The rule (largest least relative margin over the five rows at 1x1/1if) on the 50 us grid of round 1's sweep gives 1,300 us (0.2610; 1,250 us 0.2398). A 5 us search gives 1,275 us (0.2620) only with zero time between the events' fixed part and tier 2's first record; any tier-1 empty-ring read there takes the fifth SRP record out of the slice (0.2397). 1,300 us kept.
- **I2: 8x8/2if has no owed-notice slots** (sram ledger), so AECP keeps the tree's rule there; the model counts each point's depth.
- **F2: at 8x8/2if a Domain adoption's first build slice is 1.58 ms.** At 8x8/2if a slice holds one MRPDU, so a build resumed across slices makes every interface's declarations and its first MRPDU in the first slice. In the `srp` group (a Domain adopted at both interfaces) that pass is 158,096 CPU cycles, and another 131,518, over `CTRL_LOOP_BUILD_ONE_PASS_US` (1,215 us) and over the 1.3 ms slice; every other 8x8/2if group's heaviest build pass is 94,739 to 95,260. `whole_grade.py` and the slice gate refuse both, so the harness's 8x8/2if run fails `STATED` there (receipt `receipts/measure/`). 1x1/1if makes its whole build in one slice (`CTRL_LOOP_BUILD_MOST` 2) and is not affected. The remedies are each an owner question at a point the ruling leaves ungated: a longer 8x8/2if slice (1,700 us would hold the measured 1,665 us stated cost, but lets an ordinary pass's SRP slice run to 1.7 ms before the polls, against THE SHARE's 2.0 ms), the declarations in a slice of their own (Milan v1.2 4.3.2's licence then follows the VLAN's MRPDU one slice later, as I3), or more rom on an image already over its ledger (F1).
- **F3: at 8x8/2if one pass of each notice group is over THE SHARE**, 2.088 to 2.280 ms against 2.0 ms (11 of 16,874 work passes, L8N; recorded with `--record-share-findings`): the composed burst's pass, AECP's records taken past their cap until the pass has spent `CTRL_LOOP_DRAIN_US` (about 13,000 cycles each at 8x8/2if), then the other tier-1 channels' due (ACMP's two, 37,939 cycles), then the polls. 8x8/2if is measured, not gated.
- **C1 (corrected before review): the poll's sends.** `3f469cef` and `b7611ca4` answered a waiting command before the poll's notices and sent the poll's notices outside `transmit`. The harness charged them to the polls' base (13 passes of `aecp-fanout` at 8x8/2if over the base's 28,000 cycles, `aecp_mbx:poll` 29,110 cycles with no `aecp:transmit` span), and the order was a protocol change beyond `aecp_ready`. The poll now calls `transmit(a, true)` first, as the tree did before the queue, so the queue's notices and the response buffer's go before a waiting command's conclusion and inside AECP's send item.
- **C2 (corrected before review): checks a first gate pass found.** At `46d051c3` the gate pass found, each fixed in the next head:
  - the coverage ratchet: six arcs of the new code no test took (`aecp.c` `aecp_init`'s two refusals, `owe`'s tail wrap, `fan_out` with no scratch beside a held notice, `round_waits` on the queue alone; `ctrl_loop.c` `holds` on a module not ready). Each now has a check and a plant (section 2);
  - `srp_mutants.py` reset-keeps-owed-domain escaped at two interfaces: a build resumed across slices made its declarations, adopting the refused Domain legitimately, before the link-down was taken, so the plant had nothing to keep. `Srp.RefusedPeerDomainDoesNotSurviveLinkRestart` now holds the state at the old link's reset itself (neither owed nor adopted), whatever build ran before it; caught at both shapes;
  - `srp_transmit_mutants.py` transmit-built-by-the-poll planted the old one-argument `transmit` call (did not compile);
  - `ctrl_service_hooks/hooks.py` H-NOTIFY's two plants were anchored on the old fan-out cursor and the old `transmit` (the hooks self-test refused them); re-anchored, 28 of 28 checks, 96 of 96 plants;
  - the behave steps' functions lacked the annotations and docstrings the Python idiom gate requires of public functions, and one line passed 120 columns (the gate had not read the untracked files before);
  - `Loop.L27`'s expected figure held only at a 1,300 us slice (`46d051c3` itself).
- **I4: the polls' heavy items are not sliced.** #665's round 23 ruling lists them in tier 2; this round's assignment names SRP's records, THE TRANSMIT's build and THE RETRY's round as the sliced work, and the polls run as before, in every ordinary pass after SRP's slice, each heavy item doing its work only once its source posted it (`poll_grade.py`). The tier model charges each by its own source in every pass that may carry it (round 1's model), and each is held to its stated cost by the harness.
- **I5: the slice per point.** The rule at 1x1/1if with the measured datapath costs gives 1,050 us, and 1,200 us once every cost is measured on the image under the tiers (C3). One slice at both points could not take it: 8x8/2if's build of one MRPDU is 1,215 us (`CTRL_LOOP_BUILD_ONE_PASS_US`), which the build cannot divide and `ctrl_loop.c` asserts fits a slice; a single slice could only be 1,250 or 1,300 us on the grid (0.2735 and 0.271 at 1x1/1if). The ruling chooses the slice at 1x1/1if and no slice at 8x8/2if, whose rows miss at every slice, so 8x8/2if keeps 1,300 us, as built and measured. (The rule applied at 8x8/2if on what it can take gives 1,250 us, least margin -4.0166 against 1,300 us's -4.0170: every row misses either way.) The ruling expected 1,300 us at 1x1/1if; that was round 1's figure with the datapath events at `event.AECP`'s cost.
- **I3: at 8x8/2if a slice holds one MRPDU**, so an interface's MSRP and MVRP MRPDUs leave in two slices; a Domain adopted in the first is published before its VLAN's MRPDU leaves in the second (the licence still follows the VLAN's send, Milan v1.2 4.3.2, one slice later). At 1x1/1if the slice holds the whole build.
- **C3 (corrected before review): the costs on the image under the tiers.** The load gate's stated costs and the polls' were the ones measured before the tiers; only the datapath events' and the 1x1/1if build pass had been measured on this round's image. Measured again by #665 round 28's tools over every leg at both points (`receipts/measure/costs-9afbbbe2-*.txt`), eight costs were over their stated ones (section 1c), the AECP record at 1x1/1if by 30 us in every `notice-every` group (its turn commits the response and queues the notice), and AMAP_LIVE_WRITE at 1x1/1if at 20.74 us against 20. Each is stated at the larger, the gate's rule. At those costs the last queued notice binds at 1x1/1if, and the rule's slice is 1,200 us (0.2673), not 1,050 (0.2610): `CTRL_LOOP_SLICE_US` moved, the 1x1/1if legs ran again on it, and their costs were measured again (section 3). The 1x1/1if load is 0.470 at the pin and 0.457 with tsn-c-stack #32; 8x8/2if's 0.821 and 0.722, reported.

## 6. Run history

- 2026-11-12 04:51 CET start; head `f9442a10` verified; round 1 handoff, STOP and ruling read.
- 05:1x TAKEN posted (issuecomment-6813962419).
- 05:08-05:22 the firmware suite at `f9442a10` (baseline): PASS.
- 05:20-06:40 firmware, tests, mutant re-anchors; quick images (1x1/1if rom 108,480 B, sram 48,480 B; 8x8/2if over its ledger).
- 06:4x the firmware suite on a snapshot of the change: PASS; harness self-test 0 failures; `3f469cef` committed.
- 06:45 legs started on `3f469cef` (session pool: no range was bookable, `cpu_ranges.py show`: busy 128).
- 07:10-07:25 docs restated; the slice gate (`slice_grade.py`) built; the datapath group run alone at both points: the grader refused its `DATAPATH` lines (fixed in `grade.py`); the costs measured (section 3).
- 07:3x the slice rule at the measured costs picks 1,050 us at 1x1/1if (I5): the 1x1/1if legs stopped, the slice made per point; the idiom gates fixed (long lines, two long functions, two modules at 1,000 lines, a C++ table); `b7611ca4` committed; the 1x1/1if legs and the firmware shards restarted on it.
- 07:5x the 8x8/2if leg's finished groups graded with the new graders: F2 and C1.
- 08:32 the gate pass at `9afbbbe2`: `firmware-unit` failed, `Loop.L27` ("... and never past the pass's deadline": its step put the slice past the deadline only at a 1,300 us slice, so at 1,050 us the cap was not exercised and the expected figure was another's). The test restated from the constants (a slice from the round's own start, and one that would end past the deadline ends at it), both of its plants still caught; `46d051c3` committed; that gate pass and the sweep stopped and restarted on it (the logs of the first are kept in scratch, not as gate evidence).
- 09:15-10:10 the gate pass at `46d051c3` found C2's items, and three failures from the scratch volume filling for a few minutes (another lane shares it: `test_builder`'s NVM host test "cannot write", the NVM self-test "No space left on device", the control campaign's copy) and one from the runner's home (the elaborate gate's SDK selector: #810's runner home linked `br-milan-rv32` to the pinned SDK this host has; mine now does too). The same few minutes damaged twelve leg logs, lines cut and run together (`SPANSPAN ...`, `5708CALL`): L1N's notice-burst-0 to -3, L1A's acmp-notk, backlog-adp@verify-0 to -6 and save-second, and L8A's save-held, save-second and save-starved, each refused by the grader (backlog-adp@verify-5's damage is in a traced line, which only the full grader reads), each re-run from its leg's build (L1N-re, L1A-re) and merged before the regrade; every other finished log parses (the scan, section 4). Each C2 item fixed and checked (the suites at both shapes, each new and re-anchored plant caught, the coverage at 100 %, the ratchet's grown counts recorded as `--write` renders them); `0cab1e04` committed; the gate pass and the sweep restarted on it at 10:15.
- 10:15-12:58 the gate pass at `0cab1e04`: every job and lane gate as expected but `firmware-boundary` (`ctrl_boundary` refused `rows_tiers.py`, round 1's module, a program naming the firmware's tree that the registry did not list: now in `ctrl_configs.OUTSIDE`), and the sweep's wall-clock timeouts on the loaded pool (`milan_dp`, `media_phase`, `mmcm_servo`, `reboot_ctrl`: UNKNOWN, not failures). L8A's three save groups were damaged in the same disk-full window (re-run, L8A-re). `51c0e04a` committed with the registry entry and the doc's image figures at the head; the gate pass and the sweep restarted on it at 13:02, and the head builds of every leg remade there.
- 13:02-13:28 the gate pass at `51c0e04a`: `firmware-boundary` refused two more files that name the firmware's tree and compile nothing, `slice_grade.py` and the owed-notice feature's steps (a module's rule, beside the program's that refused `rows_tiers.py`; the earlier log line was cut where I read it). Both registered in `ctrl_configs.OUTSIDE`, the registry checked to leave only the five builders that compile in the capture; `19247413` committed; the gate pass, the sweep and the head builds restarted on it at 13:31.
- 13:34-15:05 L1A finished; merged with its re-runs and regraded at `19247413`: 0 refusals, the 6 budget misses round 28 recorded (the three egress-held paths of tsn-c-stack #26), no pass over THE SHARE, and two stated-cost findings. One was damage the grader had not seen: `backlog-adp@verify-7`'s polls base of 1,537,791 cycles; a strict check of every trace line's shape (`linecheck.py`) found its 9 cut lines, and found every other merged log clean; it was re-run (L1A-re3). The other was real: in the `srp` group (run at 12:57-13:12, after the window) a pass given whole to the build of both of an interface's MRPDUs took 90,543 cycles against `CTRL_LOOP_BUILD_PASS_US` 900 us, the tier check before a pass given whole now in it. Restated at 955 us at 1x1/1if (the measurement plus 5 %; `CTRL_LOOP_BUILD_MOST` stays 2, so the image is unchanged), and in tsn-c-stack#32's column, which the load gate holds at or above the pin where #32 moves nothing; the slice rule still picks 1,050 us, the load stays 0.463 and 0.450, every 1x1/1if row still fits (R5 53.01, R6 49.28, the last notice 86.96, the MRPDU row 27.26). `ee35f22b` committed; the gate pass, the sweep and the head builds restarted on it at 15:08. C1 fixed, `9afbbbe2` committed; every leg restarted on it (L8N on 56-63, `cpu_ranges.py pick`); the gate pass started: the workflow jobs and the lane's gates through a dispatcher (5 at once, MemAvailable floor 25 GB, the session pool), the full sweep as four `native-shards.py` units on the session pool's four 8-CPU blocks (no 0-95 range was free; as #810 round 28's D4).
- 15:08-17:40 the gate pass at `ee35f22b`: every workflow job and lane gate as expected (`verify_wf.py`: 139 ran, 226 not run with a reason, 0 bad), the sweep's 60 of 65 and its five wall-clock kills each PASS alone, and the six head builds byte-identical with each leg regraded. That pass is superseded by C3 (below), and the gate pass runs again on the final head.
- 17:40-18:05 C3: the 1x1/1if datapath receipt at `9afbbbe2`'s image put AMAP_LIVE_WRITE at 20.74 us, over its stated 20, so every cost was measured again at the image under the tiers by round 28's cost tools over every leg at each point (`receipts/measure/costs-9afbbbe2-*.txt`). Eight costs measured above their stated ones (section 1c). At those costs the slice rule picks 1,200 us at 1x1/1if, and `rows_tiers --selftest` refused the tree's 1,050. `8cc3e5d3` committed (the larger costs, the slice 1,200 us at 1x1/1if); the firmware suite, the harness, the tier model's and the flip check's self-tests passed on it; the load at 1x1/1if is 0.470 at the pin and 0.457 with #32.
- 18:10 the 1x1/1if legs restarted on a clean clone of `8cc3e5d3` (M1A 12 jobs, M1N 6, M1B 1, on the session's CPUs: `cpu_ranges.py pick` found none free, busy 128); `fw_coverage.py --check` on it.
- 18:17-19:20 M1N (16 groups) and M1B (1) finished on `8cc3e5d3`: rc 0, 0 refusals, 0 budget misses, no pass over THE SHARE, every tier-2 slice within 120,000 cycles. A partial cost measurement over the groups finished then moved no stated cost (only THE RETRY's round span, which the round grade and the slice gate hold, not a stated cost). `fw_coverage.py --check` PASS at `8cc3e5d3`. The docs restated at the new costs and slice (uncommitted).
- 19:20 the host was powered off at the owner's request, with M1A at 38 of 95 groups; 20:38 the host back. Every log that had ended (38 of M1A's, M1N's 16, M1B's 1) passed the strict line check (`linecheck.py`, 0 bad lines). 20:45 M1A's 57 unfinished groups re-run on its own build from the same clean clone (`--reuse-build --groups`, into `M1A-re`), to be merged with the 38.
- 22:07-22:20 M1A's re-run ended rc 0 (57 groups: the 6 egress-held misses, nothing else); merged with its 38 (`results-merged`, 95 logs, 0 bad lines) and regraded on its build: rc 0. Every cost measured on M1A, M1N and M1B (`receipts/measure/costs-8cc3e5d3-1x1.txt`): none above `9afbbbe2`'s, the TICK lower, so the table and the slice stand; the datapath events identical (29.66, 25.37 and 20.74 us). The docs at those figures; `12180198` committed (docs only).
- 22:30-01:11 the gate pass at `12180198`: the dispatcher's 25 units (workflow jobs, lane gate parts, the seven head builds), the sweep's four shards, then the regrades and the three suites and one LiteX step the loaded pool's wall clock killed, each run again alone (section 4). Every gate as expected.

- 01:2x REVIEW READY posted on #894 (issuecomment-6839788052, `REVIEW-READY-COMMENT.md`).

[A683u]

## Contents

- **[Status](#status)** — REVIEW READY at the head below: round 16 takes SRP's MRPDU build out of every pass that takes a record, gives every pass class a measured worst case at least 6,490 cycles under the share, re-measures every row, and restates the figures. `665-s2b-cycles` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Checkout, submodules and environment.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What is left, and the decisions for the owner.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY at `d930ea98f75be96f1062217d62bccd24dd291265`. This is round 16 of lane S2b, on round 15's second continuation `d0eef1cb`: eleven commits added on top, with no rebase, no force and no merge. `dev-soft-core` is still `a68536fa`, which the head contains.

SRP's MRPDU build is now a pass class of its own (THE TRANSMIT): no pass that takes a record carries one, and a build held past its age takes a pass of its own, so every participant's MRPDU is sent within 44 ms of its hold, inside the 200 ms JoinTime. A pass that dispatches a centisecond takes one record of a channel (THE TICK's cap). With that, the composed burst under input that leaves no pass empty, round 15's residual, fits: its last SRP record is 16.48 to 17.11 ms at 8x8/2if against 18 (19.05 to 19.67 before), and no pass is over the share. Every pass class has a stated worst case in cycles, the heaviest of each measured at least 9,580 cycles under the 2.0 ms share at both points, at the head's layout and with the new fields at their structs' ends. Every row, pass and save window was measured again at both points, in both arms, with and without the drafts: 0 refusals, 0 of 1,489,645 work passes over the share, every row the CPU decides within its bound, the least margin 0.235 ms ([Round 16](#round-16)).

One statement is for the manager: SRP's 18 ms is THE SHARE's nine passes, and the composed burst's 32 SRP records at 8x8/2if take sixteen, so that row fits by its passes' measured cost, not by the constants ([Known limitations](#known-limitations--out-of-scope)).

The 32x32 figures are an estimate, restated from this head, and they miss: the last AECP and SRP records and the per-pass share under every reading, the last ACMP record under two of three (section 14 of `SPLIT_CONTROL_MEMORY.md`).

## Linked Issue / roles

Relates to #665

Executor: `[A683u]`
Internal cleared-context reviewer: `[R711]`
External reviewer: `[R712]`

## Description

### Round 16

The ruling on round 15's STOP (#665 issuecomment-6634982529) put the composed burst in the SRP row's scope and asked for the layout's cycles back: a pass that fits by less than the 6,490 cycles data layout alone moved it fits by chance. Its four items, at `d930ea98f75be96f1062217d62bccd24dd291265`:

| Ruling item | Change | Evidence |
|---|---|---|
| 1. The SRP lever, by pass class, its bound from the constants, stated in ms beside `CTRL_LOOP_STEP_AGE` and `CTRL_LOOP_RETRY_MS` | THE TRANSMIT (`ctrl_loop.h`, `ctrl_loop.c`, `srp_mbx.c`). The attribution of round 15's residual: the 32 SRP records of the burst's first instant are taken by sixteen passes, and five of them carried an MRPDU build a centisecond's join timers started, about 2.4 to 2.9 ms, which put the last past 18 ms; the heaviest pass was one of them. So the loop marks a pass that took no record, at most one event and no centisecond (`tx_pass`, before its polls) and calls SRP's build after the polls, before THE RETRY and THE STEP. SRP's poll builds and declares nothing, and reports a held build owed. Once a build is held more than `CTRL_LOOP_TX_AGE` (two) centiseconds, counted on SRP's own tick, the next pass after one not given whole is the build's alone, before any input, with THE RETRY's round after it. A frame a build left owed stays the poll's (A3). THE TICK's cap (`CTRL_LOOP_RX_PER_TICK_PASS`): with THE TRANSMIT alone the heaviest pass was the one that dispatches the 10 ms centisecond beside the burst's first records, 195,756 cycles, so such a pass takes one record of a channel. Stated beside the constants: `CTRL_LOOP_TX_MS`, (2 + 1) x 10 + 7 x 2 = 44 ms from a hold to its build under any input, so every participant's MRPDU is sent within 2 x `MBX_N_IF` x 44 = 176 ms, inside the 200 ms JoinTime (IEEE 802.1Q Table 10-7); and `CTRL_LOOP_SRP_MS`, 18 ms, THE SHARE's nine passes, with what THE TRANSMIT gives SRP's records by pass class: at most one aged build among any record's wait, since two stand 20 ms apart; `srp_mbx.c` holds both at compile time | 8x8/2if, the composed burst's last SRP record: 16.48 to 17.11 ms (19.05 to 19.67 at `d0eef1cb`), with both drafts 15.98 to 16.46; the last AECP record 15.76 to 16.43 ms (19.66). 1x1/1if: 10.74 to 10.88 and 10.23 to 10.42 ms. Every other channel within its own bound. `--mutation transmit-beside-records` (THE TRANSMIT's pass every pass): `CONTROL transmit-beside-records caught`, every group 19.59 to 20.11 ms. `LoopBring.L18TransmitBindingRefusals`, `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord`, `Loop.L20AnAgedTransmitIsAPassOfItsOwn`, `Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel`, `Srp.TransmitWaitsForAPassThatTakesNoRecord`, `Srp.AHeldBuildTakesAPassOfItsOwnPastItsAge`, `Srp.AnOwedFrameComesBeforeTheBuild`, with 46 new plants (24 and 3 in the loop, 19 in SRP's adapter) and `rx-pass-unbounded` re-planted, each failing its named test on its words; two grader mutants for the new control |
| 2. The share by construction: every pass class's worst case in cycles, each at least 6,490 under the share, at both points, at the head's layout and the struct-ends layout | `ctrl_loop.h`, THE SHARE: seven classes, each with its heaviest measured pass at 8x8/2if and 1x1/1if; the one no group stages, a pass given whole to an aged build, by composition | Least 9,580 cycles under, a pass that takes a record at 8x8/2if (190,420 cycles); with the new fields at their structs' ends, 10,844 (189,156). Every other class at least 28,649 under. No further record cap was needed |
| 3. Every row, pass and save window again, both points, both arms, with and without the drafts, as round 15 item 1 staged them, plus the notice groups | Twelve legs and the struct-ends and 8x8/1if legs, on clean clones of `12e5ec56`, whose firmware the head's is (the head's images are the legs' byte for byte, 9 of 9) | 0 refusals; 0 of 1,489,645 work passes over the share, the longest 1.904 ms; every row the CPU decides within its bound, the three egress-held rows over as before. Least margin 0.235 ms, 8x8 arm A, a save's verify window opened one short of the age limit, last SRP record 17.765 ms (0.020 at `d0eef1cb`, 0.101 at `65251a2f`). Every save durable within its stated worst case: `save-starved` 12,087.0 of 12,110 ms and `save-second` 22,110.1 of 22,150 at 8x8/2if; 4,048.1 of 4,070 and 6,029.8 of 6,070 at 1x1/1if. The controls `retry-ageless` (8 of 8 notices late at both points) and `store-step-aged-heavier` (8 of 8 windows over) are caught |
| 4. Restate `ctrl_loop.h`, `aecp.h` and sections 13 and 14 | `ctrl_loop.h` (the heaviest pass, the least margin, a build-carrying pass, every class, SRP's bound); `aecp.h` (the retried notice measured from its port's answer: 12.30 to 13.20 ms at 1x1/1if, 12.47 to 13.51 at 8x8/2if); section 13's new subsection with every table; section 14's estimate, its misses, the idle pass and the gPTP paragraph | `SPLIT_CONTROL_MEMORY.md` sections 13 and 14 |

Also fixed on the way: the harness control as first committed did not build under `-Werror` (its plant left two locals unused), found when it first ran; and SRP's README named a binding among what holds a build, where its test asserts a binding holds none.

### Round 15

Both round 14 reviews were NEGATIVE: R711-4 (MAJOR F1, F2) and R712-4 (MINOR F1, F2). The age limit itself was confirmed at its cause. What did not hold was what the round stated about it: that no aged step lands among a window's records, with the least margin 0.77 ms, and that 12,110 ms is a change's worst case at 8x8/2if. The test of the limit also could not tell centiseconds from dispatches.

Round 15 staged the windows opened at the step's worst age and stopped at `bc4685ec` (#665 issuecomment-6620336528): one 8x8 pass, 2.021 ms, held an AECP change-notice retry beside the burst's records and a centisecond. The ruling (issuecomment-6620376502) made the retry the product's, kept the share, and asked for the retry to be kept out of the burst's pass by construction. The first continuation did that at `65251a2f` (issuecomment-6630201662). The ruling on it (issuecomment-6630265194) found that a retry held for a pass that takes nothing could wait up to 30 ms under input that leaves no pass empty, past its notice's 20 ms, and asked for the bound back by construction. The second continuation, at the head above, does that, and stops on what its new row found.

#### Round 15 continued (2): THE RETRY's age limit, and the STOP

| Ruling item | Change | Evidence |
|---|---|---|
| 1. The bound by construction, by pass class, stated in ms beside `CTRL_LOOP_STEP_AGE`; `aecp.h` corrected | THE RETRY's age limit (`ctrl_loop.h`). Once AECP reports a held retry `CTRL_LOOP_RETRY_AGE_MS` (4 ms) past its time, read on AECP's own millisecond clock from the earliest held retry (`aecp_retry_aged`, `aecp.retry_since`), the next pass is the round's alone. It calls the round before it takes any input and returns one, as an aged step's pass does. An aged step's pass, read first, takes the round after the step instead. The age is not reported while anything waits ahead of the round (a response or notice owed, a command waiting on its apply, a START/STOP pending). The retry stays out of every pass that takes input or dispatches a centisecond. The bound beside `CTRL_LOOP_STEP_AGE`, `CTRL_LOOP_RETRY_MS`: the age, then the pass running when it is reached, the pass that takes the round, and the pass that sends what it built, each within THE SHARE, 4 + 3 x 2 = 10 ms. With AECP's 8 ms spacing, a retried notice is built and committed within 18 ms of its port's answer, inside `AECP_NOTICE_MS` (20 ms), and `aecp_mbx.c` asserts that sum at compile time. No two passes given whole to aged work run back to back, and THE BOUND names their cost to a waiting input | `ctrl_loop.h`, `ctrl_loop.c`, `aecp.h`, `aecp.c`, `aecp_mbx.c`; the two new per-pass functions in the hot list after `ctrl_loop_service` (`ctrl_hot.py --check`) |
| 2. A harness row, graded from the port's answer against 20 ms; a grader mutant and a firmware mutant, each caught by name | `notice_window.py`, in the labelled `answering-later` arm. The face block's stream observation stays unanswered until an attempt at or after NOW_MS 3,150 fails. That attempt marks the answer (an `ENTRY`), so the next retry is a whole 8 ms backoff away. The notice is a BIND_RX's GET_STREAM_INFO, fanned out to 16 registrations an interface, under `save-starved`'s input (every receive channel at its refill rate with its bursts, a grandmaster change as every pass starts) with a save in flight, at eight phases. A late notice fails the run whatever its options record. Each channel's longest record under that load is a row too | 1x1: 12.364 to 12.450 ms, 16 recipients; 8x8: 12.519 to 13.010 ms, 32 recipients; every group within 20 ms. `--mutation retry-ageless` (the age removed): `CONTROL retry-ageless caught`, 8 of 8 groups late, 30.619 to 30.872 ms at 8x8; at 1x1, 8 of 8, 30.307 to 30.392 ms. The same groups on `65251a2f`'s firmware: 30.68 to 30.72 ms. Grader mutants "notice: a retried notice later than its bound is a budget finding only" and "notice: a retried notice is held to its ceiling, not its bound" each fail "a retried notice later than its bound fails the run whatever the options record, and one within it passes"; 149 grader mutants caught, 0 failures. Firmware plants: 8 new in the loop and 8 new in AECP, 4 re-anchored, each failing its named test on its words (`Loop.L17AnAgedRetryIsAPassOfItsOwn`, `Core.HeldRetryAgesFromItsEarliestTimeWhenTheRoundCouldTakeIt`, `Mailbox.AgedRetryTakesAPassOfItsOwn`) |
| 3. Every row, pass and save window again | Started at the code head `49f268ed`; stopped at the residual below | Begun at the code head `49f268ed`, and stopped at the residual below. As far as it ran, at 8x8: the four backlog windows and every aged window at the limit in arm A, arm B's 16 verify aged windows, and 59, 51 and 52 groups of N-A8's, N-B8's and D-A8's own runs. Every one has 0 refusals and 0 passes over the share, and only the three egress-held rows are over their bounds. The least margin is 0.020 ms, arm A's `verify-aged2-6` (last SRP record 17.980 ms), whose records hold one aged retry pass (9,973 cycles) beside its aged step's. Arm B's thinnest set (0.101 ms at `65251a2f`) is now 0.445 ms at the limit. `backlog-adp`'s heaviest pass fell to 189,736 cycles (199,112). `save-starved` is durable 12,086.7 ms after its change (12,110) |
| 4. Restate `ctrl_loop.h`, `aecp.h` and sections 13 and 14 from this head's figures | `aecp.h` restated with the bound by construction. The figure restatement of `ctrl_loop.h` and sections 13 and 14 is held back: it depends on the decision below | |

**Why STOP.** The exit is a pass over the share, or a row that does not fit. The new row's groups are the first to stage a composed burst under input that leaves no pass empty. At the load's first instant, every channel's bucket burst comes at once while the grandmaster flood runs. At 8x8/2if both exits occur there:

- **A row that does not fit.** Every group's longest held SRP record is 19.047 to 19.666 ms against its 18 ms. It is the last of the load's first SRP burst. Its 21 passes hold the composed burst's ACMP, AECP and SRP records, and two aged retry rounds of about 13,000 cycles each (about 0.26 ms). The same groups on `65251a2f`'s firmware, which has no age limit, give 18.975 to 19.421 ms. With one registration an interface they give 18.175 to 18.823 ms, and with AECP's first burst one refill period late, as `save-starved` stages it, 18.624 to 19.339 ms. So the overrun predates the age limit: this staging is new, and no earlier group combined a composed burst with the flood. With both drafts staged it is 18.030 to 18.626 ms.
- **A pass over the share.** `notice-retried-4` has one pass of 201,540 CPU cycles (2.015 ms), the burst's third, which takes ADP, ACMP, AECP, MAAP and SRP records and holds no round. With the age removed (`retry-ageless`, otherwise this head's image) it is 202,048 cycles. On `65251a2f`'s firmware it is 195,897. Each of these groups' heavy burst passes is about 5,000 cycles heavier at this head than on `65251a2f`'s firmware, with the same records and fewer fetch refills (470 against 480). The extra cycles fall mainly in `ctrl_app_srp` and `ctrl_app_aecp`, which this change does not touch. That points to the image's layout (the two new hot-list functions, and the fields added to `struct ctrl_loop` and `struct aecp`), not to the round's work. Not tested further here.

**For the manager:**
- Whether a composed burst under input that leaves no pass empty is in the SRP row's scope. If it is, the 8x8 last SRP record needs a lever outside THE RETRY, since it misses on `65251a2f` too.
- Whether the layout's 5,000 cycles are to be recovered here (the ruling allows a re-trace of the hot list when item 1 takes a margin below zero), or the share's margin is accepted as it stands in the staged windows.

**Round 15 item 1's staging at this head, as far as it ran** (8x8/2if; least margin to the bound, ms; passes over the 2.0 ms share):

| Groups | Arm | Least margin, row | Passes over the share |
|---|---|---:|---|
| The four backlog windows, the 24 aged windows at the limit | A | 0.020, `verify-aged2-6` (17.980) | 0 of 28,829 |
| The 16 verify aged windows | B | 0.308, `verify-aged1-3` (17.692); at the limit 0.445 | 0 of 13,411 |
| 59 groups of N-A8's own run | A | 0.165, `program-aged1-3` (17.835) | 0 of 115,278 |
| 51 groups of N-B8's own run | B | 0.705, `blank-aged1-6` (17.295) | 0 of 88,840 |
| 52 groups of D-A8's own run | A, both drafts | 1.620, `verify-aged2-5` (16.380) | 0 of 110,260 |

The three egress-held rows miss as before. N-A1 (9 groups) fits with 6.4 ms or more. Not run: D-B8, N-B1, D-A1, D-B1, AH-A8, P81-A8.

#### Round 15 continued (1), at `65251a2f`

| Item | Change | Evidence |
|---|---|---|
| Ruling 1. The retry kept out of the burst's pass, with its bound | THE RETRY (`ctrl_loop.h`): the loop calls AECP's round (`aecp_retry`) only in a pass that took no input and dispatched no centisecond, after its polls and before THE STEP, whose deadline counts the round's time, or after the step in the pass given whole to an aged step. The loop decides from what the pass took and dispatched; there is no cycle estimate. AECP's poll and its timer's sink hold a due retry, arm no timer for it and report it owed (`aecp.retry_hold`) | No pass over the share in any leg at `65251a2f`. The residual window's heaviest pass was 197,193 cycles (1.972 ms), with no round in it (202,116 before) |
| Ruling 2. A test and a named mutant | `Loop.L16TheRetryOnlyInAPassThatTakesNothing`, `LoopBring.L15RetryBindingRefusals`, `Mailbox.RetryWaitsForAPassThatTakesNothing`, `Core.HeldRetryWaitsForTheRoundAndTheRoundForAnOwedResponse` | 25 plants, 11 in the loop and 14 in AECP, each failing its named test on its words |
| Ruling 3. Every row, pass and save window again | Ten legs at the code head `5e2651d5` | 0 refusals, 0 of 1,281,000 work passes over the share, every row within its bound (the three egress-held rows miss as before). Least margin 0.101 ms (8x8, arm B, `verify-aged2-2`, last SRP record 17.899 ms) |
| Ruling 4. The held-back restatement from that head's figures | `ctrl_loop.h`'s reason for N and section 13's and 14's figures at `65251a2f` | `SPLIT_CONTROL_MEMORY.md` sections 13 and 14 |
| Round 15's items 2 to 4 | Stand as met: a change while a save is in flight, 22,150 ms at 8x8/2if and 6,070 ms at 1x1; `Loop.L14TheAgeCountsCentisecondsNotDispatches`; the residues | `nvm_store.h`, `test_port_loop.cpp`, the store's README |

That continuation's open question, a retried notice's timing behind a backlog or under input that leaves no pass empty, is what the second continuation answers above. Its other findings stand: the scan placed in the hot list, `aged=` on an aged step's `PASS` line, the coverage of the round's guard, and THE RETRY's AECP plants in a table of their own.

### Round 14

Both round 13 reviews were NEGATIVE on one MAJOR (R711-3-F1 = R712-3-F1): since THE STEP, a save advanced only through passes that took no input, and nothing bounded how long input could keep them from coming. The manager's decision: bound it by a mechanism, state the worst case, and test it under the contract's load.

| Item | Change | Evidence |
|---|---|---|
| 1. The mechanism | THE STEP's age limit (`ctrl_loop.h`): once more than `CTRL_LOOP_STEP_AGE` centiseconds, two, have been dispatched since the step last ran or owed nothing, the next pass is the step's alone, before any input, with the deadline read as it starts; it returns one, so the input it held off is taken by the next pass, one step later | `Loop.L13AnAgedStepIsAPassOfItsOwn` and ten planted defects. N measured: in every window the harness stages, at both points, in both arms, with and without the drafts, at most two centiseconds were posted between two passes that carried a step (one at 1x1), so no aged step lands among the records of a window opened from idle (restated in round 15: one opened at the age limit takes one, and the least margin is 0.148 ms) |
| 2. The bound | A save is durable at most 1,000 ms (DR2a) + S × 3 ticks + 10 ms after its change with no save in flight (restated in round 15: a change marked while a save is in flight, 22,150 ms at 8x8/2if, 6,070 ms at 1x1); S is its steps after the first-dirty window. A SET_NAME of the entity marks both its names: at 8x8/2if S = 370 and the worst case is 12,110 ms, at 1x1 S = 102 and 4,070 ms, with no flash busy time (`nvm_store.h`, `save_window.bound_ms`). `save-held` holds every receive channel at its contract refill rate with its bursts through a whole save; `save-starved` adds a grandmaster change as every pass starts, so no pass takes nothing | 8x8/2if, arm A / arm B, without and with the drafts: `save-starved` durable 12,087.0 / 12,087.0 and 12,087.1 / 12,088.0 ms after its change, within 12,110; `save-held` 4,696.9 / 4,696.7 and 4,697.0 / 4,731.1 ms; 0 passes over the share in either group; each channel's longest record within its bound, SRP at most 14.81 ms against 18. 1x1: `save-starved` 4,049.0 / 4,048.1 and 4,047.9 / 4,048.0 ms within 4,070. The plant with the age limit removed: `CONTROL store-step-ageless caught`, the save not durable 12,618.4 ms after its change |
| 3. One build a pass either way (R711-3-F2) | The poll reads whether the interface with the turn builds before it visits either (`turn_builds`) | `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal`, the mirrored case, fails on the plant `build-turn-read-after-its-visit`, the old reading; the review's link groups at 8x8: `y-links` 1.741 / 1.809 ms (arm A / arm B), `x-links-same` 1.531 / 1.556 ms, no pass over |
| 4. Every pass that carries a step (R711-3-F3 = R712-3-F2) | The harness prints every pass that enters the store's step, idle or work, with the store's own CPU time | Over every group of every leg: the longest pass that carries a step is 1.22 / 1.23 ms at 1x1 and 1.29 / 1.27 ms at 8x8 (arm A / arm B, without the drafts), 1.18 / 1.18 and 1.25 / 1.25 ms with them; the longest step's own time 0.97 ms, within `NVM_STEP_US`; each step kind's cost at both points in section 13. Round 13's sentence now gives the lone save's 1.21 and 1.26 ms on one basis |
| 5. The verify phase bounded (R711-3-F4) | `grade.save_phase` refuses a verify window that opens after the save's read-backs have read back every programmed byte, read off the journal reads | The self-test's phase check holds the case and its mutant; the mutant `save: a verify window is graded after its read-backs read back the container` is caught; every leg's 24 windows graded with 0 refusals |
| 6. Residue | R712-3 RESIDUE-1 and R711-3 RESIDUE-1 (section 14's S slope is arm A's at both ends), R712-3 RESIDUE-2 (the read-back step's cost in `nvm_store.h`), with their exact texts; S1 (the room rule at exactly `NVM_STEP_US`) | `SPLIT_CONTROL_MEMORY.md` section 14's S bullet (both texts, with this head's 10.04 ms); `nvm_store.h`'s `NVM_READ_BYTES` comment; `NvmBoth.step_room` with exactly `NVM_STEP_US` left, on the model port, and the plant `step_needs_room_past_its_cost`; R712-3 SUGGESTION-2, the unrounded 1.116 ms in section 14 |

**Found and fixed on the way.** The first held runs showed two things. Their SET_NAME took one of AECP's tokens, so the channel's first burst lost a record: AECP's bursts now start one refill period after the change, and a held group that commits fewer records than it offered is refused by name. And at 8x8 one pass was over the share, 2.135 ms, 1 ms after the change: AECP's mark of the SET_NAME's two names walked the store's records twice, 22,088 cycles, in the pass that drained the first bursts. A record is now marked by its id without the walk (`nvm_rec_id_of`, `nvm_store_changed_id`), with host tests and planted defects, and that pass is 1.711 ms. Every leg ran again at that head. A SET_NAME of the entity marks both its names, which the stated worst case counts. The `srp-poll-extra-read` plant had no site once the poll read every link before its visits; it is re-anchored at those reads and caught.

**A save from its change to durable** against its stated worst case (ms, arm A / arm B):

| Save | Worst case, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| `save`, alone | 4,070; 12,110 | 2,019.2 / 2,018.4 | 2,018.3 / 2,018.3 | 4,697.4 / 4,697.4 | 4,697.4 / 4,698.3 |
| `save-held` | 4,070; 12,110 | 2,019.0 / 2,018.1 | 2,018.1 / 2,018.1 | 4,696.9 / 4,696.7 | 4,697.0 / 4,731.1 |
| `save-starved` | 4,070; 12,110 | 4,049.0 / 4,048.1 | 4,047.9 / 4,048.0 | 12,087.0 / 12,087.0 | 12,087.1 / 12,088.0 |
| `save-starved`, longest gap between flash steps | | 30.98 / 30.97 | 31.08 / 31.05 | 31.33 / 31.25 | 31.48 / 31.42 |

**The rows and the share at this head**, every leg at `21d0e0f6`, whose images the head's equal, and arm A's every group again at the head (below), each family against min(T_svc = 20 ms, its 10 % ceiling):

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.77 | 0.72 / 0.71 | 1.32 / 1.32 | 1.23 / 1.23 |
| ADP record, first | 20 | 0.82 / 0.81 | 0.76 / 0.75 | 1.36 / 1.37 | 1.28 / 1.27 |
| MAAP record, first | 20 | 0.80 / 0.80 | 0.75 / 0.73 | 1.34 / 1.35 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.81 / 0.81 | 0.76 / 0.74 | 1.35 / 1.36 | 1.27 / 1.27 |
| SRP record, first | 18 | 2.87 / 2.85 | 2.69 / 2.65 | 5.45 / 5.43 | 5.05 / 5.06 |
| ACMP record, last | 20 | 5.11 / 5.16 | 4.53 / 4.61 | 7.87 / 8.51 | 7.34 / 7.72 |
| ADP record, last | 20 | 3.58 / 3.67 | 3.28 / 3.29 | 5.85 / 6.07 | 5.44 / 5.56 |
| MAAP record, last | 20 | 3.57 / 3.70 | 3.26 / 3.33 | 5.83 / 6.10 | 5.43 / 5.59 |
| AECP record, last | 20 | 10.04 / 10.37 | 9.07 / 9.67 | 14.83 / 15.93 | 13.49 / 14.33 |
| SRP record, last | 18 | 10.67 / 10.59 | 9.88 / 9.64 | 16.35 / 15.90 | 15.58 / 14.87 |
| an ACMP command behind a full acmp ring | 20 | 3.57 / 3.54 | 3.27 / 3.22 | 6.64 / 6.70 | 6.37 / 6.29 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.83 / 2.80 | 2.54 / 2.52 | 3.62 / 4.63 | 3.31 / 4.27 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.14 / 0.12 | 0.08 / 0.11 | 0.11 / 0.19 | 0.08 / 0.22 |
| an event behind 15 others | 20 | 0.92 / 0.92 | 0.87 / 0.85 | 1.47 / 1.48 | 1.39 / 1.38 |
| AECP record, last, in the owed window | 20 | **62.93** / **62.95** | **62.93** / **62.85** | **65.13** / **65.13** | **65.13** / **65.04** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **62.10** | **62.06** / **62.01** | **63.78** / **63.77** | **63.76** / **63.69** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows (`save_window.py`), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.43 / 1.44 | 1.42 / 1.32 | 1.96 / 1.91 | 1.84 / 1.69 |
| ADP record, first | 20 | 1.42 / 1.43 | 1.41 / 1.31 | 1.95 / 1.90 | 1.83 / 1.68 |
| MAAP record, first | 20 | 1.46 / 1.47 | 1.44 / 1.35 | 1.99 / 1.93 | 1.86 / 1.71 |
| AECP record, first | 20 | 1.47 / 1.48 | 1.45 / 1.36 | 2.00 / 1.94 | 1.87 / 1.72 |
| SRP record, first | 18 | 2.73 / 2.58 | 2.45 / 2.35 | 4.37 / 4.21 | 4.09 / 3.99 |
| ACMP record, last | 20 | 5.95 / 5.89 | 5.43 / 5.29 | 9.02 / 9.23 | 8.30 / 8.32 |
| ADP record, last | 20 | 4.43 / 4.40 | 4.08 / 3.97 | 6.57 / 6.79 | 6.08 / 6.15 |
| MAAP record, last | 20 | 4.46 / 4.43 | 4.11 / 4.01 | 6.61 / 6.82 | 6.12 / 6.18 |
| AECP record, last | 20 | 10.91 / 10.92 | 9.87 / 10.34 | 15.96 / 16.56 | 14.86 / 15.31 |
| SRP record, last | 18 | 11.46 / 11.22 | 10.51 / 10.32 | 17.23 / 16.91 | 16.48 / 15.56 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.55 / 3.53 | 3.31 / 3.21 | 5.42 / 5.35 | 5.03 / 4.87 |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.76 / 2.73 | 2.28 / 2.26 | 4.78 / 4.80 | 4.43 / 4.44 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.39 / 4.32 | 3.66 / 3.63 | 8.11 / 8.17 | 7.17 / 7.09 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.57 / 5.41 | 5.04 / 4.96 | 10.92 / 11.00 | 9.82 / 9.76 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.82 / 3.01 | 2.27 / 2.54 | 5.30 / 5.33 | 4.84 / 4.85 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.09 / 8.01 | 7.07 / 7.09 | 14.12 / 14.20 | 13.42 / 13.38 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.85 / 2.82 | 2.37 / 2.35 | 4.86 / 4.88 | 4.51 / 4.53 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.55 / 4.47 | 3.82 / 3.85 | 8.27 / 8.50 | 7.32 / 7.28 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.10 / 6.09 | 5.60 / 5.54 | 11.49 / 11.35 | 10.36 / 10.35 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.94 / 2.89 | 2.37 / 2.40 | 5.41 / 5.61 | 4.95 / 4.97 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.67 / 8.69 | 7.65 / 7.68 | 14.60 / 14.81 | 13.88 / 13.89 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1264, 1.11 / 0 of 1251, 1.10 | 0 of 1285, 1.01 / 0 of 1250, 1.01 | 0 of 1311, 1.97 / 0 of 1285, 1.92 | 0 of 1313, 1.89 / 0 of 1287, 1.77 |
| A save's windows | 0 of 10748, 1.22 / 0 of 8643, 1.23 | 0 of 11112, 1.18 / 0 of 8633, 1.17 | 0 of 18324, 1.96 / 0 of 11744, 1.95 | 0 of 17871, 1.86 / 0 of 11737, 1.85 |
| save-held | 0 of 3411, 1.03 / 0 of 3395, 1.03 | 0 of 3405, 1.04 / 0 of 3421, 1.03 | 0 of 8474, 1.69 / 0 of 8489, 1.69 | 0 of 8504, 1.63 / 0 of 8499, 1.63 |
| save-starved | 0 of 44390, 0.97 / 0 of 43629, 0.97 | 0 of 39664, 0.97 / 0 of 43670, 0.97 | 0 of 52488, 1.71 / 0 of 52090, 1.72 | 0 of 52624, 1.66 / 0 of 53926, 1.66 |
| Every group run | 0 of 66819, 1.22 / 0 of 57520, 1.23 | 0 of 56068, 1.18 / 0 of 57576, 1.18 | 0 of 88204, 1.97 / 0 of 74225, 1.95 | 0 of 80929, 1.89 / 0 of 76066, 1.85 |

Every row the CPU decides fits; the tightest is the 8x8 last SRP record in a save's window, 17.23 ms in arm A, 0.77 ms under 18. The three egress-held rows miss as before. No pass is over the share in any group of any leg; the longest, 1.97 ms, carries no step.

**32x32, an estimate, restated at this head:** the last SRP record 31.0 / 35.8 / 65.4 ms under S / L / U, the last AECP record 28.3 / 35.0 / 63.7 ms, the longest pass 3.6 / 4.9 / 7.9 ms (section 14 of `SPLIT_CONTROL_MEMORY.md`). gPTP's assumed mean leaves the 8x8 last SRP record 0.32 ms; at the top of its range, 1.116 ms, it is 0.35 ms over; its bound puts it 7.23 ms over.

### Round 13

Both round 12 reviews found passes over the 2.0 ms share that no group staged: a save's flash step beside a composed window's heaviest work, 2.39 and 2.72 ms at 8x8/2if, and both links changing together, 2.08 ms. The share is not amended; each is fixed in code, and each stale statement in text.

| Item | Change | Evidence |
|---|---|---|
| 1. A save in a composed window | THE STEP (`ctrl_loop.h`): the store's centisecond consumer only owes a step; the loop reads the store's clock as a pass starts and, after the polls of a pass that took no event and no record, hands the step the clock's value at which the pass has spent the share. The step is taken only while 1.0 ms (`NVM_STEP_US`) is left; otherwise it stays owed, once. THE SHARE names it | At round 12's head the review's windows reproduce exactly (x-save 2.388 ms, y-save 2.716 ms, y-links 2.081 ms). At this head `backlog-adp`'s window in each flash phase of a save at eight tick phases, both points, both arms, with and without the drafts: 0 of 99,289 passes over the share; a pass carrying a step at most 1.02 ms at 8x8 and 1.22 ms at 1x1. The planted store step (`--mutation store-step-unbounded`, 8x8, arm A): 15 of 24 windows over the share, the longest 2.71 ms, 5 of them with every row within its bound; `CONTROL store-step-unbounded caught` |
| 2. A joint link change | A poll builds one interface at most; the other on the next pass, and it goes first after that | `y-links` 1.76 / 1.82 ms (arm A / arm B), `x-links-same` 1.54 / 1.56 ms, no pass over. `Srp.JointLinkChangeBuildsOneInterfaceAPass` fails on the plant `joint-reset-builds-both` |
| 3. The boot simulation's flash window | The boot SoC on the product's uncached window (`milan_soc.ctrl_uncached_flash`); an export with another is refused; the self-test plants the call's removal | 1x1 25.515 ms, 8x8 64.885 ms to ready (24.660 and 64.271 ms through the cached window at `c954b8a9`, 25.413 and 65.026 ms with the window alone); `PLANT flash-window-cached: caught`, 3 of 3 plants caught |
| 4. Stale statements | The SRP README's share (2.0 ms), the AECP README's 20 ms service bound, the store README's cadence; the platform image's 58.5 tiles; the gPTP additions restated from the table's own units, each a mean or a bound | Section 14 of `SPLIT_CONTROL_MEMORY.md` |
| 5. Residue | A save's time to durable in absolute terms (here and in section 13); the harness README's arm B backlog rows; the interface reset clears `listener_present` (S1, accepted) | `Srp.InterfaceResetClearsListenerPresent`, plant `reset-keeps-listener-present` |

**The first fix was not enough, and its result is kept.** With the room gate alone every pass of the 14 save windows then graded fit, but at 8x8 the deferred read-backs landed in the passes that drain SRP's full ring, and the last SRP record took 18.02 to 18.21 ms against 18 in four blank-check windows. The step now waits for a pass that takes no input, so no record waits on it beyond the pass running when the record arrives.

**The store's steps,** one save with no other load, CPU cycles at 100 MHz, the flash port's and the store's in the step's pass, from a measurement-only build that prints every pass running the flash port (not on this branch):

| Step | 1x1/1if | 8x8/2if |
|---|---:|---:|
| Erase issue | 5,051 | 5,112 |
| Busy poll | 3,994 | 4,710 |
| Blank-check read-back, 128 bytes | 73,491 | 72,841 |
| Page program issue | 95,373 | 95,386 |
| Verify read-back, 128 bytes | 76,234 | 76,737 |

The longest, a page program's issue, is 0.954 ms, within the 1.0 ms the step is given.

**A save from the change to durable,** from the SET_NAME to the end of the step that reads back the container's last bytes, one save with no other load, on the harness's flash model, which has no busy time: at 8x8 4,697.1 ms at round 12's head and 4,697.4 ms at this head; at 1x1 2,018.4 ms. The blank check and the verify read back 128 bytes a tick, 104 ticks each at 8x8, 2.08 s of ticks where a whole page a step took 1.04 s before round 12. The owner's 0.5 s (#823) belongs to the append-only design in Mark II, not to this image, and this PR does not claim it.

**A save's progress.** The store steps only in a pass that took no input. In `backlog-adp`'s window at 8x8 a step owed as the window opened waited until its records had drained, at most 16.95 ms past its tick, and the ticks meanwhile owed it once, so a window delays a save by about a tick. Nothing here bounds that wait under input that never leaves a pass empty.

**The rows with a save in progress** (`backlog-adp`'s window in a save's flash phases; ms, arm A / arm B, bold over the bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.48 / 1.46 | 1.41 / 1.37 | 1.85 / 1.87 | 1.71 / 1.81 |
| ADP record, first | 20 | 1.47 / 1.45 | 1.40 / 1.36 | 1.84 / 1.86 | 1.70 / 1.80 |
| MAAP record, first | 20 | 1.51 / 1.49 | 1.43 / 1.39 | 1.88 / 1.89 | 1.73 / 1.84 |
| AECP record, first | 20 | 1.52 / 1.50 | 1.44 / 1.40 | 1.89 / 1.90 | 1.74 / 1.85 |
| SRP record, first | 18 | 2.68 / 2.59 | 2.44 / 2.41 | 4.39 / 4.38 | 4.08 / 4.01 |
| ACMP record, last | 20 | 5.95 / 5.92 | 5.47 / 5.33 | 8.89 / 9.30 | 8.20 / 8.39 |
| ADP record, last | 20 | 4.44 / 4.42 | 4.10 / 4.02 | 6.44 / 6.85 | 5.94 / 6.24 |
| MAAP record, last | 20 | 4.47 / 4.46 | 4.14 / 4.06 | 6.48 / 6.89 | 5.96 / 6.28 |
| AECP record, last | 20 | 10.86 / 11.15 | 10.22 / 10.34 | 15.86 / 16.79 | 14.51 / 15.38 |
| SRP record, last | 18 | 11.17 / 11.14 | 10.60 / 10.31 | 16.99 / 17.29 | 15.79 / 15.46 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.57 / 3.55 | 3.32 / 3.26 | 5.29 / 5.40 | 4.87 / 4.96 |

The tightest is the 8x8 last SRP record, 17.29 ms against 18, arm B: 0.43 and 0.83 ms more, arm A and arm B, than `backlog-adp`'s window with no save, since a step can be running when the window's records arrive.

**The rows of the four backlog windows at this head:**

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.79 | 0.71 / 0.72 | 1.32 / 1.39 | 1.23 / 1.24 |
| ADP record, first | 20 | 0.82 / 0.83 | 0.75 / 0.76 | 1.37 / 1.43 | 1.28 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.81 | 0.73 / 0.74 | 1.35 / 1.41 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.82 | 0.74 / 0.75 | 1.36 / 1.42 | 1.27 / 1.28 |
| SRP record, first | 18 | 2.88 / 2.92 | 2.68 / 2.70 | 5.42 / 5.61 | 5.06 / 5.06 |
| ACMP record, last | 20 | 5.06 / 5.18 | 4.79 / 4.60 | 7.85 / 8.31 | 7.28 / 7.37 |
| ADP record, last | 20 | 3.52 / 3.68 | 3.38 / 3.30 | 5.85 / 6.07 | 5.38 / 5.35 |
| MAAP record, last | 20 | 3.54 / 3.72 | 3.42 / 3.33 | 5.84 / 6.06 | 5.36 / 5.33 |
| AECP record, last | 20 | 9.68 / 10.17 | 9.44 / 9.60 | 14.69 / 15.96 | 13.58 / 14.35 |
| SRP record, last | 18 | 10.58 / 10.47 | 9.74 / 9.58 | 16.56 / 16.46 | 15.33 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.59 / 3.63 | 3.27 / 3.28 | 6.59 / 7.01 | 6.36 / 6.37 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.81 / 2.81 | 2.54 / 2.53 | 3.60 / 4.42 | 3.29 / 3.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.10 | 0.13 / 0.06 | 0.12 / 0.12 | 0.19 / 0.25 |
| an event behind 15 others | 20 | 0.92 / 0.93 | 0.85 / 0.88 | 1.47 / 1.54 | 1.38 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.90** / **63.01** | **62.90** / **62.87** | **65.10** / **65.31** | **65.12** / **65.14** |
| a response with 7 frames owed ahead of it | 20 | **62.05** / **62.14** | **62.03** / **62.02** | **63.75** / **64.19** | **63.75** / **63.76** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Against round 12's head the 8x8 last SRP record rose from 15.88 / 15.96 to 16.56 / 16.46 ms: a pass of SRP's drain runs 68 more instructions, the clock read as each pass starts, but about 3,300 more CPU cycles, half of them instruction-fetch waits from the moved code layout, and the record waits sixteen passes.

**The per-pass share,** passes over it of the work passes, those that write nothing to the mailbox counted by their run's longest, and the longest in ms (arm A / arm B):

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1280, 1.10 / 0 of 1251, 1.10 | 0 of 1276, 1.01 / 0 of 1250, 1.01 | 0 of 1314, 1.96 / 0 of 1286, 1.95 | 0 of 1317, 1.86 / 0 of 1286, 1.82 |
| A save's 24 windows | 0 of 11195, 1.22 / 0 of 8643, 1.21 | 0 of 11134, 1.18 / 0 of 8631, 1.16 | 0 of 18088, 1.95 / 0 of 11745, 1.98 | 0 of 18111, 1.86 / 0 of 11742, 1.83 |
| Every group the leg ran | 0 of 19927, 1.22 / 0 of 10496, 1.21 | 0 of 13012, 1.18 / 0 of 10483, 1.16 | 0 of 27214, 1.96 / 0 of 13648, 1.98 | 0 of 20045, 1.86 / 0 of 13645, 1.83 |

**32x32, an estimate, restated at this head.** No such shape exists. U is the assigned four times 8x8/2if; L the line through 1x1/1if and 8x8/2if; S the slope at one interface, from a labelled scratch point.

| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.79 | 1.17 | 1.39 | 5.5 | 3.4 | 2.7 |
| ADP record, first | 20 | 0.83 | 1.21 | 1.43 | 5.7 | 3.5 | 2.8 |
| MAAP record, first | 20 | 0.81 | 1.20 | 1.41 | 5.6 | 3.5 | 2.8 |
| AECP record, first | 20 | 0.82 | 1.21 | 1.42 | 5.7 | 3.5 | 2.8 |
| SRP record, first | 18 | 2.92 | 4.68 | 5.61 | **22.5** (+4.5) | 14.9 | 11.8 |
| ACMP record, last | 20 | 5.18 | 7.25 | 8.31 | **33.3** (+13.3) | 19.1 | 15.8 |
| ADP record, last | 20 | 3.68 | 5.01 | 6.07 | **24.3** (+4.3) | 14.3 | 11.2 |
| MAAP record, last | 20 | 3.72 | 5.00 | 6.06 | **24.2** (+4.2) | 14.1 | 11.0 |
| AECP record, last | 20 | 10.17 | 13.21 | 15.96 | **63.9** (+43.9) | **35.8** (+15.8) | **28.1** (+8.1) |
| SRP record, last | 18 | 10.58 | 14.91 | 16.56 | **66.2** (+48.2) | **37.1** (+19.1) | **31.4** (+13.4) |
| An ACMP command behind a full ACMP ring | 20 | 3.63 | 5.80 | 7.01 | **28.0** (+8.0) | 18.6 | 14.6 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.81 | 3.90 | 4.42 | 17.7 | 9.9 | 8.2 |
| An event behind 15 others | 20 | 0.93 | 1.32 | 1.54 | 6.1 | 3.6 | 2.9 |
| The longest work pass | 2 | 1.10 | 1.56 | 1.96 | **7.9** (+5.9) | **4.9** (+2.9) | **3.5** (+1.5) |

The rows that would not fit: the last AECP record under S, L and U by 8.1, 15.8 and 43.9 ms; the last SRP record by 13.4, 19.1 and 48.2 ms; the longest work pass at 3.5, 4.9 and 7.9 ms, over the share by 1.5, 2.9 and 5.9 ms; under U alone the first SRP record by 4.5 ms, the last ACMP, ADP and MAAP records by 13.3, 4.3 and 4.2 ms, an ACMP command behind a full ACMP ring by 8.0 ms.

**gPTP, a labelled assumption,** restated from the table's own units, a frame or a servo run each, 0.4 ms at 40,000 cycles: on a row 1.1 units, 0.45 ms, as a mean (62 units a second over 18 ms); 20 units, 8.0 ms, as a bound, all that can fall in 18 ms on two ports; on a pass 4 units, 1.6 ms, as a bound (two records a channel a pass). At 8x8/2if the last SRP record, 17.29 ms at its worst, keeps 0.26 ms under the mean and is 0.39 ms over at the range's top, 1.1 ms; the bound puts it 7.29 ms over. The longest pass, 1.98 ms, becomes 3.58 ms under the pass bound. So F6's records need their own room in the pass. At 32x32 the longest pass becomes 5.1 ms under S and 9.5 ms under U, and a Pdelay response, two passes, takes 10.2 ms under S, within Milan v1.2 4.2.6.2.6's 15 ms, and 18.9 ms under U, past it. Not measured: no gPTP firmware is linked here.

### Round 12

| Piece | Change | Why |
|---|---|---|
| Merge | `dev-soft-core` `a68536fa`, contract 2.4 and dev's #806, #814, #818, #787 | Assigned. Three semantic conflicts follow below; each is its own commit |
| Split CPU clock | `milan_soc.CTRL_CPU_CD` `sys`, `ctrl_cpu_domain` refuses any other, no CPU clock of its own, no crossing | The owner's decision of 2026-10-30. The all-fabric CPU and the Milan datapath clock do not change |
| CPU budget harness | Built through `ctrl_cpu_cd`; `build.json` records `cpu_cd`, `cpu_hz`, `sys_hz`; a CPU anywhere else is refused, built or reused; the `--cpu-hz` option is retired | One clock, and no figure at another presented as the product's |
| Split boot simulation | The merged S3 harness still drove the CPU from the Milan clock: now `ctrl_cpu_cd`, the boot graded against the approved T_svc = 20 ms | Merge conflict in meaning: boot at 1x1 24.660 ms, 8x8 64.271 ms |
| Platform image | `ctrl_plat_image.py` built RV32I against the split link: now the split hart's flags and audits, with the record mover and the word-wide primitives; `ctrl_memory.LEDGERED`'s `ctrl_plat` size re-measured, 19,944 B, 58.0 RAMB36 within the ledgered 59.0 | Merge conflict in meaning: it no longer linked |
| SRP link change | `reset_interface` withdraws and destroys in the pass that takes it; the next pass's poll builds; SRP's receive waits; a pass of link edges builds once | It was the one 8x8 pass over the 2.0 ms share, 2.21 and 2.22 ms. Events a pass do not set it (labelled experiments: six 2.207 ms, four 2.108 ms) |
| Saved-state read-back | Blank check and verify read 128 bytes a step (`NVM_READ_BYTES`) | A whole page through the product's uncached window and lwSRP's periodic work in one tick put an 8x8 pass at 2.26 ms. A save's read-back takes twice as many ticks: at 8x8 the blank check and the verify are 2.08 s of ticks, and a save takes 4,697.1 ms from the change to durable (measured in round 13 at `c954b8a9`) |
| Harness flash window | Uncached and not executable but in the hybrid-XIP arm, refused otherwise | The cached window read the flash through the data cache, which the product never does: 12.39 ms at 8x8 and 4.07 ms at 1x1 for one pass in each save |
| Harness AECP pacing | Each frame waits a refill period of the channel's token bucket | At 100 MHz the groups outran the refill and the filter refused the frames past its burst: 3 refused probes at 1x1, 15 at 8x8 |
| The two refused windows | Each backlog window opens on a drained event ring; its table and any refusal give the records held at its opening | The window's definition was wrong, not the firmware: it named a population only a drained ring can take, and waited a fixed time for one. With k records held only 16 - k + 1 of the fifteen grandmaster changes commit |
| Docs | `ARCHITECTURE_HW_SW_SPLIT.md`, `SPLIT_CONTROL_MEMORY.md` sections 5, 11 to 13 and new 14, both harness READMEs, `MAILBOX_SPLIT.md`'s access bounds, the SRP, store and platform READMEs | Every figure names its clock. The bare-metal all-fabric image keeps its own clock contract |

The rows at round 12's head, `c954b8a9`, each family against min(T_svc = 20 ms, its 10 % ceiling); round 13 restates them above.

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

| Row | Bound, ms | 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 / 0.75 | 0.65 / 0.67 | 1.30 / 1.31 | 1.21 / 1.22 |
| ADP record, first | 20 | 0.79 / 0.80 | 0.70 / 0.71 | 1.34 / 1.35 | 1.25 / 1.26 |
| MAAP record, first | 20 | 0.77 / 0.78 | 0.68 / 0.69 | 1.33 / 1.33 | 1.24 / 1.24 |
| AECP record, first | 20 | 0.78 / 0.79 | 0.69 / 0.70 | 1.34 / 1.34 | 1.25 / 1.25 |
| SRP record, first | 18 | 2.79 / 2.80 | 2.50 / 2.56 | 5.35 / 5.29 | 4.99 / 5.00 |
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| ADP record, last | 20 | 3.65 / 3.59 | 3.18 / 3.22 | 5.81 / 5.85 | 5.26 / 5.08 |
| MAAP record, last | 20 | 3.68 / 3.63 | 3.22 / 3.26 | 5.80 / 5.84 | 5.30 / 5.12 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| an ACMP command behind a full acmp ring | 20 | 3.45 / 3.47 | 3.03 / 3.11 | 6.51 / 6.73 | 6.19 / 6.21 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.73 / 2.74 | 2.42 / 2.45 | 3.53 / 4.19 | 3.95 / 4.11 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.12 / 0.12 | 0.11 / 0.10 | 0.25 / 0.23 | 0.23 / 0.09 |
| an event behind 15 others | 20 | 0.88 / 0.89 | 0.78 / 0.80 | 1.44 / 1.45 | 1.35 / 1.35 |
| AECP record, last, in the owed window | 20 | **62.66** / **62.73** | **62.75** / **62.77** | **64.99** / **64.95** | **64.94** / **65.01** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **61.93** | **61.94** / **61.95** | **63.68** / **63.93** | **63.91** / **63.68** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The share is 2.0 ms. Passes over it of the work passes run, longest in ms, arm A / arm B:

| 1x1/1if | 1x1/1if, both drafts | 8x8/2if | 8x8/2if, both drafts |
|---:|---:|---:|---:|
| 0 of 1277, 1.07 / 0 of 1250, 1.07 | 0 of 1279, 0.98 / 0 of 1250, 0.98 | 0 of 1319, 1.97 / 0 of 1286, 1.92 | 0 of 1310, 1.77 / 0 of 1302, 1.77 |



Out of context, the split CPU on `sys` closes at 100 MHz, WNS +1.605 ns, WHS +0.070 ns, 3,543 LUTs, 5,643 FFs, 9.5 tiles: 405 LUTs, 1,236 FFs and 5 tiles fewer than behind the crossing. The routed split image is lane S9's.

**The 1x1, 4 KiB windows.** At the CPU's 100 MHz, on a drained ring, all four commit their fifteen grandmaster changes with no record held. The composed maximum covers all four, so it is no longer partial: at least 40.25 ms, a lower bound while the two bound-talker windows close with SRP records unreleased.

**32x32 and gPTP** are restated at round 13's head above.

**One CPU, measured** at round 12's head. As built, the split placement already has one hart. The figures below are the split firmware on that hart, and on the SoC core as it ships, cacheless, on `sys` at 100 MHz, arm A. The cacheless core does not fit 8x8.

| Row | Bound, ms | Split CPU, 1x1 | Cacheless RV32IM, 1x1 | Cacheless RV32I, 1x1 | Split CPU, 8x8 | Cacheless RV32IM, 8x8 | Cacheless RV32I, 8x8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.56 | 1.58 | 1.30 | 2.90 | 2.93 |
| ADP record, first | 20 | 0.79 | 1.60 | 1.62 | 1.34 | 2.94 | 2.98 |
| MAAP record, first | 20 | 0.77 | 1.58 | 1.60 | 1.33 | 2.92 | 2.96 |
| AECP record, first | 20 | 0.78 | 1.59 | 1.61 | 1.34 | 2.93 | 2.97 |
| SRP record, first | 18 | 2.79 | 5.44 | 5.63 | 5.35 | 11.37 | 11.72 |
| ACMP record, last | 20 | 5.16 | 9.98 | 10.45 | 7.76 | 16.08 | 16.09 |
| ADP record, last | 20 | 3.65 | 7.14 | 7.78 | 5.81 | 11.70 | 11.77 |
| MAAP record, last | 20 | 3.68 | 7.18 | 7.81 | 5.80 | 11.71 | 11.75 |
| AECP record, last | 20 | 9.67 | 17.34 | 19.76 | 14.41 | **26.83** | **28.51** |
| SRP record, last | 18 | 9.95 | 17.98 | **21.63** | 15.88 | **30.26** | **34.52** |
| An ACMP command behind a full ACMP ring | 20 | 3.45 | 6.87 | 7.06 | 6.51 | 14.29 | 14.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.73 | 5.50 | 5.94 | 3.53 | 8.75 | 7.78 |
| An event behind 15 others | 20 | 0.88 | 1.82 | 1.84 | 1.44 | 3.16 | 3.20 |
| Passes over the 2.0 ms share, longest ms | 2 | 0 of 1277, 1.07 | **3 of 1267, 2.14** | **3 of 1270, 2.35** | 0 of 1319, 1.97 | **62 of 1314, 3.61** | **64 of 1315, 3.85** |

## Authoritative references

- #665 and #640, "Updated 2026-10-31" and their 2026-10-31 and 2026-11-01 comments. The round 16 ruling (#665 issuecomment-6634982529) and the STOP it answers (issuecomment-6634926714). The ruling on the first continuation (#665 issuecomment-6630265194) and the REVIEW READY it answers (issuecomment-6630201662). The ruling on round 15's STOP (issuecomment-6620376502) and the STOP it answers (issuecomment-6620336528). The round 15 assignment (issuecomment-6611588032) and the round 14 reviews it answers (this PR's issuecomment-6611420126 and issuecomment-6611570890). The round 14 assignment (#665 issuecomment-6589337173) and the round 13 reviews it answers (issuecomment-6589042666 and issuecomment-6589327842). The round 13 assignment (issuecomment-6573625213); the round 12 assignment (issuecomment-6514866239); the 20 ms decision (issuecomment-6495692075); #823's 0.5 s, the append-only design's.
- `docs/design/SAVED_STATE_FASTCONNECT.md` section 9.4, the flash part's datasheet maximum (tSE, tPP).
- `docs/reference/FR_NFR.md` 3.4.1 (a notification's 20 ms; "No extra budget is granted at timer arm, expiry or retry") and 3.4.2, NFR-SCOUT-01 and -03; `sw/firmware/ctrl/loop/ctrl_loop.h`, THE SHARE with every pass class's worst case, THE STEP, THE RETRY with its age limit, THE TRANSMIT, THE TICK's cap and `CTRL_LOOP_SRP_MS`; `sw/firmware/ctrl/aecp/aecp.h`, the retry's backoff and the notice's bound.
- IEEE 1722.1-2021 7.5.2 and 9.3.2.6, Milan v1.2 5.4.5.2 and Table 5.22 (the notices a retry builds).
- PR #828's `MARK_II_AREA_PLAN.md` and `MARK_II_STREAM_ENGINES.md`, read only.
- IEEE 802.1AS-2011 with Cor1 and Cor2, as Milan v1.2 profiles it; Milan v1.2 4.2.6.2.6 and 4.3.2; IEEE 802.1Q-2018 10.7.11 and Table 10-7 (JoinTime).

## How to get into the same state

```sh
git fetch origin
git checkout d930ea98f75be96f1062217d62bccd24dd291265
git submodule update --init protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
```

The harness's prerequisites are in `tb/verilator/ctrl_service_budget/README.md`: the product LiteX tree, the pinned RV32 SDK and Verilator, with `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8-notice --variant answering-later --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-transmit --variant answering-later --mutation transmit-beside-records
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings --record-share-findings
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --shard 0/4
python3 sw/firmware/ctrl/test/ctrl_hot.py --check
python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP
```

Expected result at this head:
- The self-tests report 0 failures and every planted defect caught; the firmware self-test runs as shards 0/4 to 3/4.
- The 8x8 and 1x1 runs: 0 refusals, no pass over the share, every row within its bound but the three egress-held paths (`backlog.owed`, `backlog.owed_behind0` to `3`, `backlog-owed.service.aecp.last`), which the record options list.
- The 8x8 notice run: every retried notice within 20 ms, every held row within its bound, the longest held SRP record at most 17.11 ms.
- The build-beside-records plant prints `CONTROL transmit-beside-records caught`.

Evidence at `d930ea98f75be96f1062217d62bccd24dd291265`, each gate on a clean clone, never piped, each rc 0:

- Every `run:` step of `.github/workflows/docs.yml`, each job on its own fresh clone: 64 steps ran, 0 bad; the 31 hosted-only steps were not run, each with its reason recorded. The first run of docs-gates-0 failed one step, the HDL timing diagram no-drift gate, because the local gate environment lacked `wavedrom==2.0.3.post3`, which docs.yml's diagram dependency step installs and the local runner does not run. With that package installed, the job ran again on a fresh clone, rc 0.
- `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0 to 3, each shard its own unit on four CPUs, `MAKEFLAGS="-j4 --no-print-directory"`: 65 of 65 suites, 2,613,655 checks, 0 failures; each shard's counts equal round 15's; `capture_coherence`'s shard built on 4 workers. No preflight failure.
- `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard k/4`, k = 0 to 3: `test_ctrl_firmware: PASS` in each. Shard 1 caught 669 of 669 mutants, including THE TRANSMIT's 24 loop plants and THE TICK cap's 3. Shards 2 and 3 caught every AECP and SRP campaign plant, including THE RETRY's 26 and THE TRANSMIT's 19 in SRP's adapter.
- `python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4`: 455 tests, all 121 planted defects reddened.
- `python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8`: PASS (38 files).
- `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 0 failures, 151 of 151 grader mutants caught.
- `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <b> --record-budget-findings --record-share-findings`: 94 groups, 0 refusals, 0 of 199,801 passes over the share, only the three egress-held paths over budget; the saves 2,018.4 / 2,018.2 / 4,048.1 ms (alone / held / starved) against 4,070 and `save-second` 6,029.8 ms against 6,070. Its table is byte for byte the measured 1x1 arm A leg's.
- The same at `--point 8x8`: 93 groups, 0 refusals, 0 of 286,852 passes over, only the three egress-held paths over budget; the saves 4,697.3 / 4,696.9 / 12,087.0 ms against 12,110 and `save-second` 22,110.1 ms against 22,150; the longest step-carrying pass 1.302 ms, the longest step 0.960 ms; the least margin 0.235 ms (the last SRP record of a verify window opened one short of the age limit, 17.765 ms). Its table is byte for byte the measured 8x8 arm A leg's.
- `python3 sw/builder/test_builder.py --require-rv32`: "ALL GATES PASS EXCEPT 2 NOT RUN", the same two arms that need another host as before.
- `cd tests && behave --no-capture -f plain`: 508 scenarios passed, 0 failed.
- `git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD`: clean.
- Also rc 0: the boot simulation at both shapes (25.590 and 64.661 ms to ready), its native controls (6 of 6) and its self-test (3 of 3 plants caught); the Python and C++ idiom gates; the bare-metal scope check; `gen_mailbox.py --check --crosscheck` and `--selftest`; the publication census; `lint_rtl.py --check` (89, within its ratchet); `test_soc_options.py` and `test_ctrl_memory.py`; both halves of `ctrl_boundary.py`; `ctrl_hot.py --self-test` and `--check` (207 entries, in the recorded order).
- The nine measured images (both arms, both points, the notice legs and the three controls), rebuilt at the head through the harness's own build, are the legs' (9 of 9).

## Known limitations / out of scope

- **SRP's 18 ms for the composed burst is met by measurement, not derived from the constants** (for the manager). THE SHARE's 2.0 ms is 18 ms over nine passes, with the A3 row of seven owed frames as its deepest admitted wait. The composed burst's 32 SRP records at 8x8/2if, and the backlog windows' full SRP ring, two a pass under D4(b), take sixteen passes, which the constants bound at about 34 ms. The row fits by those passes' measured cost: 16.48 to 17.11 ms in the notice groups, 17.765 ms at worst over every window. THE TRANSMIT made those passes lighter and bounds what stands among them by pass class (at most one aged build, one aged step and the aged retries; a build only in a pass that took no record because an event posted during it held SRP's records back). A bound from the constants alone would need more than two SRP records a pass or a stated cost for an SRP drain pass. `CTRL_LOOP_SRP_MS` and section 13 say so.
- **The margins:** 0.235 ms on the 8x8 last SRP record, and 9,580 cycles on the share. A change that grows the hot code ahead of SRP's drain, or adds fields to the loop's or a module's structs, must measure them again.
- **The struct-ends layout ran a subset:** the 8x8 notice groups and arm A's backlog, save and aged windows. The classes whose heaviest falls in other groups sit 28,649 cycles or more under the share.
- **THE TICK's cap moves the other channels' last records later** (ACMP 8.90 ms against 8.54 at 8x8/2if), each within its 20 ms; at 32x32 the last ACMP record now misses under the measured line too.
- **A pass given whole to an aged build** is staged by no group; its worst case is stated by composition (one build and one round, 183,922 cycles at 8x8/2if).
- **A retried notice behind other notices:** each notice owed ahead of it costs it its own round and the pass that sends it, and while a command waits on its apply or a START/STOP is pending no notice is built (`aecp.h`). The 18 ms is a single notice's, with nothing ahead of its round.
- **The idle pass** carries THE TRANSMIT's and THE RETRY's calls and their ages, about 8,700 CPU cycles at 1x1/1if and 15,400 at 8x8/2if.
- **The aged windows sample, they do not sweep:** eight delays across the tick, three flash phases, two ages; with the drafts, the limit only.
- **A change's worst case is this image's, not #823's.** 12,110 ms at 8x8/2if for a SET_NAME of the entity with no save in flight, 22,150 ms beside another's save in flight, on a flash with no busy time; on the part at its datasheet maximum, 15,370 and 28,670 ms. #823's 0.5 s applies to the append-only design's writer through this same step, and this image does not meet it.
- **The step's room:** the longest step is 0.962 ms (96,212 cycles, 1x1/1if) of the 1.0 ms `NVM_STEP_US` gives it; no gate holds the figure yet.
- **The three egress-held rows** stay with tsn-c-stack #26.
- **The drafts** (lwSRP, tsn-c-stack) are measured staged and are not pinned here.
- **The platform image's hot list:** four entries name the size fixture's callbacks and place nothing in that image.
- **No fabric option outlives the switch-over:** nothing here adds one.
- The hybrid-XIP arm still misses T_svc on every path, so D3's rule stands.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (#665 stays open: this lane is one part of it)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes (Evidence above)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains (SRP's composed-burst fit is stated as measured, for the manager)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

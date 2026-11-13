[A773]

## Contents

- **[Status](#status)**: the built tiers, their head, and `894-tiers` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)**: #894, its executor and reviewers.
- **[Description](#description)**: what the firmware, the harness and the model now do.
- **[Authoritative references](#authoritative-references)**: the rulings and clauses.
- **[How to get into the same state](#how-to-get-into-the-same-state)**: the commands to check out the branch.
- **[How to validate](#how-to-validate)**: the reviewer's commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)**: what this round leaves to the owner.
- **[Definition of Done](#definition-of-done)**: the merge bar.

## Status

**GREEN at 1x1/1if; 8x8/2if measured, not gated (owner questions F1 to F3 below).** Head `12180198b087d4cfdd531d0de5d3753211b35616`, ordinary commits on round 1's `f9442a10`. `894-tiers` -> `dev-soft-core` (after #810 merges).

- Every 1x1/1if row fits by every source at the built slice, and the flip check passes there: `flip_grade.py --check --point 1x1/1if` rc 0. The 1x1/1if long-window load is 0.470 at the pin and 0.457 with tsn-c-stack #32, against 0.70, every cost the larger of its measurement on the image under the tiers and the committed table's.
- Measured on the CPU budget harness, every 1x1/1if row fits with room: tier 1 at most 6.562 ms of 20, SRP 9.044 of 90, the last queued notice 17.228 of 125. The only misses are round 28's three egress-held paths of tsn-c-stack #26.
- The clean-clone gate pass ran once on the head. Every `run:` step of the four workflows a pull request triggers passes or is not run with a stated reason (139 ran, 226 not run); one, the standalone LiteX aggregate, passed 8 of 8 on an uncontended re-run after the loaded pool's wall clock killed one of its simulations. The firmware self-test and every mutant driver catch every plant, with 0 escaped. `fw_coverage.py --check` passes at 100 % for the changed files. `test_builder.py --require-rv32`, behave (511 scenarios) and `git diff --check` pass. All 65 sweep suites pass: 62 in the sweep, and `milan_dp`, `milan_dp_gm_steps` and `milan_dp_render` on an uncontended re-run with the wall clock doubled, after the loaded pool's clock killed them.

## Linked Issue / roles

Relates to #894, #665, #810 and #890.

Executor: `[A773]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

#894's round 2 builds the design round 1's model found to fit every row at 1x1/1if, as the ruling of 2026-11-12 decided it.

| Piece | What changed |
|---|---|
| `sw/firmware/ctrl/loop/ctrl_loop.c`, `ctrl_loop.h` | **THE TIERS.** Tier 1 (AECP first, past its cap while the pass has spent at most `CTRL_LOOP_DRAIN_US`, then ACMP, ADP and MAAP, each once the one before left no record it would take) before any tier-2 work. Tier 2 only once tier 1's takes left none: SRP's records in a slice ending `CTRL_LOOP_SLICE_US` after the pass started, each record started only while the slice holds its stated cost; THE TRANSMIT's build and THE RETRY's round each a slice of a pass given whole, after a pass that served tier 1, the round only once SRP is served too. A queue's first notice is tier 1's. Which take ended on its limit is recorded as it is taken (`rx_left`), so tier 1 is checked with no extra mailbox read. THE STEP's aged pass stands as built. |
| `CTRL_LOOP_SLICE_US` | The ruling's rule at the costs measured on the image under the tiers: **1,200 us at 1x1/1if** (the largest least relative margin over the five rows, 0.2673, the last queued notice binding, on a 50 us grid; 1,050 us gives 0.2610 and 1,300 us 0.2650). **1,300 us at 8x8/2if**, which the ruling leaves unchosen and which holds one MRPDU's build there. |
| `sw/firmware/ctrl/srp/srp_mbx.c` | **The build resumes across slices.** It makes at most the MRPDUs its slice holds (`CTRL_LOOP_BUILD_MOST`: 2 at 1x1/1if, so the whole build; 1 at 8x8/2if), reclaims as the next build would, and resumes at the next participant with its declarations made. An interface reset ends a build it was resuming. |
| `sw/firmware/ctrl/aecp/aecp.c`, `aecp_mbx.*` | **AECP's owed-notice queue** (`aecp_ready`, the ruling's conditions (a) to (d)). A command whose notice fits a slot commits its response in its record's turn and queues the notice, so AECP takes its next record. The poll sends the queue's oldest, one a poll, after any response and before the response buffer's own, inside AECP's send (`transmit`), as the tree sent its notices before. AECP is not ready while the queue is full. `AECP_MBX_OWED_SLOTS` is the AECP burst at 1x1/1if and 0 at 8x8/2if, whose sram has no room. The queued-notice bounds at 1x1/1if are decision D's 20 and 125 ms. |
| `tb/verilator/ctrl_service_budget/` | **The datapath change pads** and the `datapath-events` group measure the three coalesced datapath events' sink cost. The grader reads the pulse lines. **`slice_grade.py`** (#665 round 23, item 1) fails a run on any tier-2 slice over its point's `CTRL_LOOP_SLICE_US`. |
| `rows_tiers.py`, `flip_grade.py` | **The built design** (`rows_tiers.BUILT`, the tree's slice at each point, AECP first, SRP first, the queue at each point's depth) is the flip check's rows (`--design built`, the default). The loop before the tiers stays available (`--design as-built`). The datapath events are at their measured cost. `rows_grade.py` is unchanged. |
| Tests | `Loop.L26`, `Loop.L27` and the restated `L16`, `L17`, `L20`, `L22` and `L23`; `Queued.*` (two controllers' back-to-back state-changing commands, the queue's bound, a longer notice behind the queue, a walk resumed at its recipient); `Srp.ABuildResumedAcrossSlicesSendsTheFramesOfTheBuildMadeWhole` (the MRPDU bytes of a sliced build against the same build made whole); `tests/features/aecp_owed_notices.feature`; the harness's slice and datapath checks. |
| Planted defects | 17 for the tiers (`loop_step_mutants.py`), 19 for the queue and the first notice (`aecp_owed_mutants.py`), 4 for the resumed build (`srp_transmit_mutants.py`), 1 new fan-out plant, 8 for the slice gate, 1 for the built rows. Each fails its named test on its own words. |
| Docs | `SPLIT_CONTROL_MEMORY.md` section 13 (THE TIERS), `FR_NFR.md` 3.4.1, `MAILBOX_SPLIT.md`, the AECP, SRP and harness READMEs, `tests/README.md`. The loop search `ctrl_retry_search.py` is retired: the queued notices are tier rows now. |

**Rows by every source at the built design** (`rows_tiers.py`):

| Point | Slice | R4 (20 ms) | R5 (90 ms) | R6 (90 ms) | First queued notice (20 ms) | Last queued notice (125 ms) | MRPDU, reported |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1/1if | 1,200 us | 12.71 | 54.59 | 52.85 | 14.60 | 91.59 | 29.00 |
| 8x8/2if | 1,300 us | 42.47 | 187.97 | 178.28 | 20.25 | 647.23 | 89.01 |

**The datapath events' sink cost** (assignment item 3), the most measured on the images under the tiers plus 5 %, rounded up to 5 us: 35, 30 and 25 us at 1x1/1if (at most 29.66, 26.10 and 20.74 measured), and 35, 35 and 25 us at 8x8/2if (at most 33.13, 30.32 and 20.73 measured), for AVB_INFO_CHANGED, AS_PATH_CHANGED and AMAP_LIVE_WRITE. The rows had assumed `event.AECP`'s 60 and 95 us.

**Every cost measured again on the image under the tiers** (#665 round 28's cost tools over every leg at each point), each the larger of that and the committed table's: at 1x1/1if an AECP record 205 to 235 us (its turn now commits the response and queues the notice), ADP's timer slot 110 to 115, the TICK 40 to 45, a pass's events' fixed part 25 to 30 and the polls' base 155 to 160; at 8x8/2if AECP's timer slot 95 to 105, a notice 270 to 275 and ACMP's owed frame 185 to 195. At those costs the slice rule's choice moved from 1,050 us to 1,200 us at 1x1/1if.

**Measured on the CPU budget harness.** The 1x1/1if legs ran on `8cc3e5d3`'s image (the 1,200 us slice) and the 8x8/2if legs on `9afbbbe2`'s, which `8cc3e5d3` leaves unchanged. Each is byte-identical at the head (ELF and binary), each leg's sample group log is byte-identical too, and each leg is regraded at the head.

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

The 8x8/2if stress has every source at its contract rate. The `backlog*` windows stage every channel's admitted burst at once (AECP 16, ACMP 12, ADP 8, MAAP 7 and SRP 32 records), a grandmaster change every 2 ms (15), a bound sink and 16 registrations. `notice-burst-<k>` adds a queue of 40 notices whose ports answer 6 ms before the composed burst. The save windows hold a save in flight through it.

## Authoritative references

- #894's ruling of 2026-11-12 (issuecomment-6813855717): the `aecp_ready` change under conditions (a) to (d), the slice by the largest least relative margin at 1x1/1if, 8x8/2if measured and not gated.
- #665's round 23 ruling (issuecomment-6732443213): the two tiers, slices with tier 1 between them, a gate on the slice, builds and rounds resumable with the same bytes.
- #665 decision D (issuecomment-6759183115): tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms; the 0.70 long-window ceiling.
- IEEE 1722.1-2021 7.5.2, 9.3.5.2.6 and 9.3.5.4 (Figure 9-3); Milan v1.2 5.4.5.1, 5.4.5.2 and 4.3.2.
- `docs/reference/FR_NFR.md` 3.4.1; `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, THE TIERS.

## How to get into the same state

```sh
git fetch origin 894-tiers
git checkout 894-tiers
git rev-parse HEAD   # 12180198b087d4cfdd531d0de5d3753211b35616
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

## How to validate

```sh
# the model and the flip check (seconds)
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --terms            # exits 1: 8x8/2if's rows miss by every source
python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest         # 509 of 509 controls refused
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if   # RESULT: PASS
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest         # 319 of 319
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check            # 0.470 and 0.457 at 1x1/1if, PASS
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test               # self-test: 0 failures, 210 plants caught
# the firmware, its plants and coverage (minutes)
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard K/4   # K = 0..3
python3 sw/firmware/gtest/fw_coverage.py --check
cd tests && behave
git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD
```

Expected result / pass criteria:
- `rows_tiers.py --terms` prints the table in the Description and exits 1, on 8x8/2if's rows only.
- Every self-test and gate above exits 0.
- The four firmware shards catch every plant: the control campaign 697 of 697, the AECP campaign 243 and the SRP campaign 344, with 0 escaped.
- The CPU budget harness at 1x1/1if (`run.py --point 1x1 --build-dir <dir> --record-budget-findings --record-share-findings`) exits 0. Its only budget misses are the three egress-held paths, and no pass exceeds THE SHARE.

## Known limitations / out of scope

- **The MRPDU row.** By every source a timer's MRPDU now waits for tier 1's records: 29.00 ms at 1x1/1if and 89.01 ms at 8x8/2if, over the 20 ms the loop before the tiers held it to by construction. It is reported, not held. Which bound holds it under the tiers is an open decision on #894.
- **8x8/2if is measured, not gated** (the ruling). Its rows by every source miss under the tiers.
- **F1: the 8x8/2if size fixture's image is 664 B of rom over its 57.5-RAMB36 ledger** (123,544 B; 1,104 B more than before the tiers). The harness's 8x8/2if build plans that image against the ledger, so it refuses on a clean clone. The 8x8/2if measurement used a plan of 58.0 RAMB36 that is not committed. This needs an owner decision on the ledger, or 808 B of code out of that image.
- **F2: at 8x8/2if a Domain adoption's first build slice is 1.58 ms.** That is over the 1.3 ms slice and over `CTRL_LOOP_BUILD_ONE_PASS_US`, and the slice gate refuses it. The remedies are each an owner question: a longer 8x8/2if slice, against THE SHARE; the declarations in a slice of their own; or more rom.
- **F3: at 8x8/2if one pass of each notice group is over THE SHARE**, 2.088 to 2.280 ms against 2.0. It is the composed burst's pass: AECP's records taken past their cap to `CTRL_LOOP_DRAIN_US`, then ACMP's two, then the polls. 11 of 16,874 work passes.
- **Interpretations, each published:** the slice per point (1x1/1if by the rule, 8x8/2if kept at 1,300 us); the 50 us grid; no owed-notice slots at 8x8/2if; one MRPDU a slice at 8x8/2if, so the VLAN's licence follows its send one slice later (Milan v1.2 4.3.2); the polls' heavy items not sliced; MAAP counted in tier 1.
- **Not changed:** the bounds (tier 1 20 ms, SRP 90 ms, the last queued notice 125 ms), the every-source rule, the load ceilings, `rows_grade.py`, tsn-c-stack, lwSRP and every donor.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

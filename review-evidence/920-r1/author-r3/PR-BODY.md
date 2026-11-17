[A786]

## Contents

- **[Status](#status)** - Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** - Public task, executor, and independent reviewers.
- **[Description](#description)** - What changed and why.
- **[Authoritative references](#authoritative-references)** - Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** - Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** - Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** - What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** - The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Ready for independent re-review at `81c9a1a0`. Round 3 local gates pass;
all eight firmware images are byte-identical to `bd252db1`.
`920-save-burst` -> `dev-soft-core`.

## Linked Issue / roles

Closes #920
Relates to #665, #890, #914, #919, #927

Executor: `[A786]`
Internal cleared-context reviewer: `[R857]` (R857-1 negative; re-review pending)
External reviewer: `[R858]` (R858-1 positive at `bd252db1`)

## Description

**The cause: a lost mark.** The AECP owner held its saved-state marks in `uint32_t pending[8]`, 256 ids, a size from
layout 2's 8-bit record_id. Layout 3 (#823) puts the NAME block after every other block, at id 222, so every name from
ordinal 34 on has an id of 256 or more: `mark()` wrote past the array and `aecp_nvm_poll()` never delivered it. At
1x1/1if those are ordinals 34 to 38, AUDIO_CLUSTER 22 to 24, CONTROL 0 and CLOCK_DOMAIN 0: exactly the five names the
rehearsal lost. At 8x8 it is 73 names, and the bits land in `struct ctrl_plat`'s next member, the ACMP persistence
wrapper. Shown three ways before any fix (receipts):

- the unit test this PR adds, at the base: 34 of 39 marks reach the store, names 34 to 38 come back as defaults;
- the save harness at the base, the burst paced as the rehearsal's controller sent it: one save, names 34 to 38 never
  durable and missing at the cut;
- the board, on its current image: the store read over the console before the cut held nothing dirty, nothing
  pending, no failed attempt, verdict OK, about 10 s before the cut, and the same five names came back as defaults.

The step rate was not the cause: in the rehearsal's own capture AUDIO_CLUSTER 24 was answered 574 ms into an 878 ms
burst and lost, while the clusters answered after it were saved.

| Piece | Change |
|---|---|
| `sw/firmware/ctrl/aecp/aecp_nvm.{c,h}` | One pending bit per layout 3 id (36 words) and a count of the bits set; a static assert that every id of the shape has its bit. The lost-mark defect, fixed as that defect. |
| `sw/firmware/ctrl_nvm/nvm_store.c` | The ruling's three allowed mechanisms (#665 issuecomment-6899740728, item 1): a change marked during a running capture joins it (the capture walks again from the first record for one behind its cursor that no capture holds); a change the save in flight cannot take is the next save's, which starts at the first idle step after it; and while a save is in flight every pass that took no input and has `NVM_STEP_US` left takes a step, one a pass. |
| `sw/litex/ctrl_memory*.py` | The target platform's 8x8 two-interface image ledgered at 60.5 RAMB36, its cap, `ctrl_plat` 20,480 B: S14 debt. |
| `tb/verilator/ctrl_service_budget/` | `save-burst` and `save-flight` at the one-interface points; each save's container read off the log; three planted save controls, each caught by its group's name; the save windows staged at a step a pass. The capture's join has no harness control: the removed plant remains within 5 s (7 saves instead of 6 at 8x8/1if); its omitted change is written by the next save that a later change starts, so the store's units hold it. |

Nothing changes the step's length, the age limit, the tiers, the pace, the two-slot sequence, the blank check, the
verify, the format, or a first change's first-dirty window. No RTL, mailbox contract or budget bound changes.

**The merge of `dev-soft-core` `70f4056f`** (#901, SRP's Talker declarations, #895) is one `--no-ff` merge, with both
sides kept:
- `aecp_nvm.h`: this branch's pending-bit words, with #901's name runs.
- `ctrl_memory*.py` and section 3: both sides raised the platform's 8x8/2if entry to 60.5. #895's reason stands,
  and #920's is added within that cap.
- `ctrl_plat` is measured on the merge at 17,664, 19,200, 18,304 and 20,480 B.
- Every image is #901's plus 296 to 304 B; the 8x8/2if platform image is 132,040 B in its 60.5 RAMB36.

The merge carries no gateware change.

Round 3 adds two store tests and named plants. `first_change_after_flight`
requires the full first-dirty window after an immediate follow-up save;
`next_now_not_reset` removes that flag's reset. `retry_after_rewind` requires
an in-flight record changed during retry backoff to survive a power cut;
`rewound_not_reset` removes the capture flag's reset. Case 4's wording now
claims only the record ahead of the rewound cursor that it exercises.
Firmware and gateware are unchanged from `bd252db1`.

**Load acceptance, amended by [the ruling on F-2](https://github.com/kebag-logic/milan-fpga/issues/920#issuecomment-6935243271):**
"the load within 0.70 at 1x1/1if, and within 0.75 at 8x8/1if by #914's gate at the composition; 8x8/2if's load is owed to #890".

- 1x1/1if: **0.517 of 0.70** at this head.
- 8x8/1if: graded by **#914's gate at the composition**. Its measurement is
  **0.735 of 0.75 at #914's head**, per [the recorded measurement](https://github.com/kebag-logic/milan-fpga/issues/894#issuecomment-6934688411).
  That is prior evidence for #914, not a composition result for this head.
- 8x8/2if: **0.798** at the pin, identical at `70f4056f`. This is the base's
  figure, owed to **#890**; this PR moves no load term.

Round 3 coverage passes across 39 files; all eight firmware image comparisons pass.
The store gate passes 566 tests across five shapes and catches all 154 plants.
All five local docs jobs pass; the verifier records 61 executed steps, 34 declared NOT RUN reasons, and zero bad steps. Composition grading and bench qualification remain outstanding.

## Authoritative references

- Milan v1.2 5.3.13 (the names saved in non-volatile memory and restored after a power cycle)
- #665 issuecomment-6899519003 (the rehearsal's finding) and issuecomment-6899740728 (the ruling, items 1 and 4)
- #920 issuecomment-6910219988 (the ruling on this PR's timing STOP: the 8x8/1if routes miss at the base, owed to #927)
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, [A burst of names and a change in flight (#920)](../docs/design/SPLIT_CONTROL_MEMORY.md#a-burst-of-names-and-a-change-in-flight-920)
- `sw/firmware/ctrl_nvm/nvm_store.h` (a change's worst case), `sw/firmware/ctrl/loop/ctrl_loop.h` (THE STEP)

## How to get into the same state

```sh
git fetch origin && git checkout 920-save-burst && git submodule update --init
```

## How to validate

Round 3 ran the store suite with all named plants, `fw_coverage --check`,
and the docs jobs on clean clones. Firmware images are rebuilt at `bd252db1`
and `81c9a1a0` with identical inputs and compared byte for byte. All sixteen comparisons (eight ELFs and eight loadable binaries) match.
The harness, routes and full sweep carry. The prior measurements
below describe round 2, not new round 3 harness executions.

```sh
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output /tmp/aecp-nvm --nvm --filter 'Nvm.*'
python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8
python3 -B sw/firmware/gtest/fw_coverage.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/b1x1 --jobs 8 --record-budget-findings --record-share-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir /tmp/b81 --jobs 8 --record-budget-findings --record-share-findings
# the save controls, each its group alone
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/c1 --jobs 2 --record-budget-findings --record-share-findings --mutation store-names-past-256-lost --groups save-burst
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/c2 --jobs 2 --record-budget-findings --record-share-findings --mutation store-next-save-waits --groups save-flight
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir /tmp/c3 --jobs 2 --record-budget-findings --record-share-findings --mutation store-step-only-owed --groups save-burst
```

Expected result / pass criteria:

- the AECP arm's `Nvm.*` tests pass, `EveryAcknowledgedNameSurvivesTheRealStorePowerCycle` among them; the store's
  suite passes at every shape and its self-test catches every mutant; `fw_coverage --check` reports no finding;
- the harness self-test reports `0 failures`;
- at 1x1 the run exits 0. Every row the CPU decides is within its budget, no pass is over the share, every `SAVE` and
  `BURST` line reads `within`, and no `STATED` line is printed. The seven held-egress rows of `backlog-owed`, behind the
  scenario's 60 ms egress hold, are recorded misses, as at the base. The burst's 39 names are durable in one save, the
  latest 1,107.8 ms after its response. The change in flight is durable in 165.0 ms, its next save 19 steps on (want 19);
- at 8x8/1if every row the CPU decides is within its budget, no pass is over the share, and every `SAVE` and `BURST`
  line reads `within`, with the same seven held-egress rows recorded. The burst's 107 names are durable in 6 saves, the
  latest 1,370.3 ms after its response. The change in flight is durable in 663.1 ms, 59 steps on (want 59). The run
  exits 1 only on `STATED` lines (Known limitations);
- each control prints `CONTROL <name> caught` and exits 0.

## Known limitations / out of scope

- R857-1's F-1 tests and F-2 load disposition are addressed for re-review.
  The prior wording residues remain on the manager's residue checklist.
- Final composition grading, the #919 sync, fixed-image bench qualification,
  hosted acceptance and independent re-review remain outstanding.

- **The 8x8/1if split platform image's routes miss at the base, owed to #927** (#920 issuecomment-6910219988):
  - the recipe's ExtraPostPlacementOpt: WNS +0.011, WHS +0.034;
  - ExtraTimingOpt: WNS +0.171, WHS +0.014;
  - AltSpreadLogic_high: WNS +0.215, WHS +0.014.

  The base's own 8x8/1if image gives the same at the recipe's directive, on the same paths. 1x1/1if meets at all
  three; the best is ExtraTimingOpt, WNS +0.133 and WHS +0.036. No further route is run: the merge brings no gateware
  change, so a route of it would differ only in the ROM's bytes.
- **8x8/1if's stated-cost lines are #914's per-shape statements, recorded as such** (the same ruling). On this base one
  interface takes 1x1/1if's statements at every shape. On the merge the lines are:
  - the polls base: 90 lines in 78 groups, the most 25,015 cycles against 22,500, in the pass that delivers a name;
    this change's `nvm_mark` takes 731 cycles of that pass;
  - an ACMP item: 7,277 against 5,500;
  - a declined ACMP offer: 2,338 against 2,000.

  Every row the CPU decides is within its bound; the seven held-egress misses are recorded above.
- **Item 4 of the ruling, the sync onto #919's review head, waits for #919's REVIEW READY** (the train puts #919
  first). No pass here carries a PHY poll slice, since none exists on this base.
- The starved worst cases and the product part's stay above 10 s at 8x8 (15,740 and 29,410 ms on the product part).
  They are stated, not gated (the ruling, item 1). The append-only design (#823) closes them.
- The target platform's 8x8 two-interface image is ledgered at 60.5 RAMB36, the cap, as S14 debt (#895's raise, with
  #920's 296 B within it).

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

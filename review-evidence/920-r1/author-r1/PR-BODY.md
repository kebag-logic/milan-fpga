[A786]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

BLOCKED (a timing decision): the 8x8/1if split platform image misses the timing floor at all three directives; every other gate below. `920-save-burst` -> `dev-soft-core`

## Linked Issue / roles

Closes #920
Relates to #665

Executor: `[A786]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

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
| `sw/litex/ctrl_memory*.py` | The target platform's 8x8 two-interface image ledgered at 60.5 RAMB36, its cap, `ctrl_plat` 20,416 B: S14 debt. |
| `tb/verilator/ctrl_service_budget/` | `save-burst` and `save-flight` at the one-interface points; each save's container read off the log; three planted save controls, each caught by its group's name; the save windows staged at a step a pass. The capture's join has no harness control: without it the burst is still durable within 5 s (7 saves instead of 6 at 8x8/1if), so the store's units hold it. |

Nothing changes the step's length, the age limit, the tiers, the pace, the two-slot sequence, the blank check, the
verify, the format, or a first change's first-dirty window. No RTL, mailbox contract or budget bound changes.

## Authoritative references

- Milan v1.2 5.3.13 (the names saved in non-volatile memory and restored after a power cycle)
- #665 issuecomment-6899519003 (the rehearsal's finding) and issuecomment-6899740728 (the ruling, items 1 and 4)
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 13, [A burst of names and a change in flight (#920)](../docs/design/SPLIT_CONTROL_MEMORY.md#a-burst-of-names-and-a-change-in-flight-920)
- `sw/firmware/ctrl_nvm/nvm_store.h` (a change's worst case), `sw/firmware/ctrl/loop/ctrl_loop.h` (THE STEP)

## How to get into the same state

```sh
git fetch origin && git checkout 920-save-burst && git submodule update --init
```

## How to validate

```sh
python3 -B sw/firmware/ctrl/test/aecp_arms.py --output /tmp/aecp-nvm --nvm --filter 'Nvm.*'
python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 16
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
- at 1x1 the run exits 0. Every row the CPU decides is within its budget, no pass is over the share, and every `SAVE`
  and `BURST` line reads `within`. The seven held-egress rows of `backlog-owed` (behind the scenario's 60 ms egress hold)
  are recorded misses, as at the base. In the groups: the burst's 39 names are durable in one save, the latest 1,101.7 ms after its response, and the
  change in flight in 158.5 ms, its next save 19 steps on (want 19);
- at 8x8/1if every row the CPU decides is within its budget, no pass is over the share, and every `SAVE` and `BURST`
  line reads `within`, with the same seven held-egress rows recorded. In the groups: the burst's 107 names in 6 saves, the latest 1,367.5 ms after its response, and the change in flight in
  657.7 ms, 59 steps on (want 59). The run exits 1 only on `STATED` lines, as at the base (Known limitations);
- each control prints `CONTROL <name> caught` and exits 0.

## Known limitations / out of scope

- **The 8x8/1if split platform image misses the timing floor (WNS and WHS >= +0.030 ns) at all three directives**,
  and the decision is posted on #920. The figures:
  - the recipe's ExtraPostPlacementOpt: WNS +0.011, WHS +0.034;
  - ExtraTimingOpt: WNS +0.171, WHS +0.014;
  - AltSpreadLogic_high: WNS +0.215, WHS +0.014.

  Every build has 0 failing endpoints and passes the identity gate, and two meet the issue's floors (WHS >= 0). The
  change has no RTL; the image differs from the base only in its firmware's bytes, in the same 56.0 RAMB36. 1x1/1if
  meets at all three; the best is ExtraTimingOpt, WNS +0.133 and WHS +0.036. The base's own 8x8/1if image, built at
  the recipe's directive, gives the same figures on the same paths (WNS +0.011, WHS +0.034): the route does not see the
  firmware's bytes.
- **8x8/1if exits 1 on stated-cost lines, at the base as here.** On this base one interface takes 1x1/1if's
  statements (`ctrl_loop.h`'s build of one and slice, `poll_grade.py`'s polls base), and SRP's build of one MRPDU at
  8x8/1if is over them (`ctrl_loop.h` records 1,019 us). In the base's `save-flight` the longest build-one pass is
  94,668 cycles and the polls base 21,774; here they are 96,241 and 23,251. The polls base grows by 731 cycles, which
  is this change's `nvm_mark` in the delivery of a name. SRP's spans move by a few hundred cycles because the image's
  layout shifted. The burst's longest build is 109,408 cycles, 1.8 s after its last save. No row is over its bound at
  either point. #914 gives 8x8/1if its own statements (polls base 235 us, build of one and slice 1,475 us), and every
  such line here is within them; the polls base has the least margin, 249 cycles.
- **Item 4 of the ruling (the sync onto #919's review head) is open.** #919 had no review head when this lane started.
  No pass here carries a PHY poll slice, since none exists on this base.
- The starved worst cases and the product part's stay above 10 s at 8x8 (15,740 and 29,410 ms on the product part).
  They are stated, not gated (the ruling, item 1). The append-only design (#823) closes them.
- The target platform's 8x8 two-interface image is ledgered at 60.5 RAMB36, the cap, as S14 debt.

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

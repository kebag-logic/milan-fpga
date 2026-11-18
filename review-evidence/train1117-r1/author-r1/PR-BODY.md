[A794] The flip train, composed: seven frozen PRs merged in train order onto dev-soft-core, each conflict resolved keeping both sides, and the composed image measured once

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**BLOCKED (draft): STOP at step 7** (#665 issuecomment-6942842392). Steps 1 to 6 are composed and checked on #914's frozen head `e1ecce20` (recomposed after its head moved from `8883d499`). Step 7, #931, waits for a decision on what the product SoC build plans past 56 RAMB36, where #933 and #931 require opposite behaviour. A measurement of the composed image at 1x1/1if (a probe with step 7) puts three rows over their bounds once the costs are restated by the rule; that also needs a decision. The last three train members (#934, #932, #936) come in round 2. `flip-train-1117` -> `dev-soft-core`.

## Linked Issue / roles

Relates to #665
Relates to #871
Relates to #894
Closes #917
Closes #929
Closes #919
Closes #920
Closes #923
Closes #924
Closes #930

Executor: `[A794]`
Internal cleared-context reviewer: the composition review, by both reviewers (#665 issuecomment-6939574513, item 3)
External reviewer: the same composition review

## Description

One train branch on dev-soft-core `cb96336d`, by the owner's rules for the flip train (#665 issuecomment-6939460730, option B; issuecomment-6939574513, freeze and compose once). Each frozen PR head is merged with `git merge --no-ff`, so each becomes an ancestor and GitHub marks it merged when the train lands. There is no rebase, squash or cherry-pick. Before each merge the head was checked against the PR's GitHub head.

| Step | PR | Frozen head | Its reviews | Merge | Conflicts |
|---|---|---|---|---|---|
| 1 | #881 (#871, AECP REBOOT and the reset port) | `d3e61e37` | R821 POSITIVE at the head; R822 POSITIVE at its ancestor `d3566d44` | `43b954e6` | 18 |
| 2 | #914 (#930, #894: the 8x8/1if tier rows, THE RETRY keyed on the shape) | `e1ecce20` | R843-7 POSITIVE at the head; R844-5 POSITIVE at its ancestor `d0a2a160` | `877c99e4` | 12 |
| 3 | #918 (#917, the AECP command held to the next refill) | `394612c5` | R846, R845 POSITIVE at the head | `9c0e1974` | 7 |
| 4 | #935 (#929, the split gates at the base) | `37255683` | R856, R855 POSITIVE at the head | `22a82038` | 2 |
| 5 | #933 (#919, the PHY poll and 1000BASE-T only) | `1a1e6665` | R852, R851 POSITIVE at the head | `2078c438` | 13 |
| 6 | #938 (#920, a name burst durable within 5 s) | `81c9a1a0` | R857 POSITIVE at the head; R858 POSITIVE at its ancestor `bd252db1` | `7c28f53f` | 5 |
| 7 | #931 (#923, #924, map edits through the EDIT window) | `d06ded5a` | R847, R848 POSITIVE at the head | STOP | 15 |

Every conflicted file has a resolution row (both sides' intent, the resolution, why) in the lane's RESOLUTIONS table, attached to the composition review.

Composition fixes. Each fixes only what the union broke, never a PR's own change:

| Commit | What | Why |
|---|---|---|
| `6fef44b8` | Three comments in the harness's `build.py` rewrapped, and one comment in `grade.parse` moved; words and AST unchanged. | Each side left `build.py` at the Python idiom gate's 1,000-line limit and `grade.parse` within 100 lines; the union broke the ratchet, which may not be raised. |
| `7431b6ba` | `grade.grade`'s `interfaces` and `shape` folded into one parameter, with its four callers; one comment rewrapped; #938's five burst mutants and their helper moved to `selftest_mutants_burst.py`, the mutant table unchanged (AST-identical, 272 entries). | #914's `shape` and #938's `journal` gave the function seven parameters, one past the gate's six; the union put `aecp_mutants.py` and `selftest_mutants.py` past the 1,000-line module limit. |

Figures two PRs both restate (AECP_QUEUED_MS, `CTRL_LOOP_SRP_UNIT_US`, `CTRL_LOOP_TX_MS`, the polls' and records' stated costs, the paced records, the ROM ledger's `ctrl_plat` sizes and entries) are carried through the merges at the side that moved them, the larger where both did. They are restated from the composed image after the last merge, by their tools (`queued_bound.py`, `rows_tiers.py`, `plat_ledger.py`) or by the rule: stated cost = measurement + 5 %, rounded up to 5 us, never below the measurement. A ROM entry goes to its measured size by the owner's rule of 2026-11-15, as S14 debt. The coverage ratchet is regenerated by `fw_coverage.py --write`.

Composed figures (owed at the final head): the CPU service-budget harness at 1x1/1if and 8x8/1if, the record classes, the statement survey, the ROM ledger at every point and both split routes.

**Release image:** at the first composition's step 5 (`89eea108`), against `cb96336d`. `bios.bin` and the AEM blob are byte-identical, `bios.elf` is identical with debug sections stripped, and the gateware export is equal outside the top Verilog's comments. To be repeated at the final head.

## Authoritative references

- #665 issuecomment-6939460730 (option B, one train candidate) and issuecomment-6939574513 (freeze, compose once, one composition review, one merge).
- Each composed PR's own rulings, cited in its row of the resolution table: #894's shape, retry-cost and held-egress rulings; #895's rulings of 2026-11-14 and 2026-11-15; #897's ruling of 2026-11-15; #923's ruling of 2026-11-16; the owner's rule of 2026-11-15 on control-memory ROM as S14 debt.
- [FR_NFR.md 3.4.1](docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing), [SPLIT_CONTROL_MEMORY.md](docs/design/SPLIT_CONTROL_MEMORY.md) sections 5 and 13, [MAILBOX_SPLIT.md](docs/design/MAILBOX_SPLIT.md).

## How to get into the same state

```sh
git fetch origin flip-train-1117 dev-soft-core
git checkout --detach origin/flip-train-1117
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP
# each frozen head is an ancestor:
for h in d3e61e37 e1ecce20 394612c5 37255683 1a1e6665 81c9a1a0; do git merge-base --is-ancestor $h HEAD && echo "$h in"; done
```

## How to validate

```sh
python3 scripts/docs_check.py && python3 scripts/check_py_idiom.py && python3 scripts/check_hygiene.py --check
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check
python3 -I tb/verilator/ctrl_service_budget/record_classes.py --selftest
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4   # and 1/4 to 3/4
python3 sw/firmware/gtest/fw_coverage.py --check
```

Expected result / pass criteria: every command exits 0. `flip_grade.py --check` without `--point` fails only on the 8x8/2if rows, the base `cb96336d`'s same eleven findings, reported, not held, by the owner's decision of 2026-11-12.

## Known limitations / out of scope

- Step 7 (#931) is not composed: see Status.
- The composed image at 1x1/1if, measured on a probe with step 7 and restated by the rule: the largest legal command's record 1,045 us against 975; `event.AECP` 80 against 75, `event.MAAP` 170 against 165, `AS_PATH_CHANGED` and `AVB_INFO_CHANGED` 40 against 35. With those, three rows by every source pass their bounds: the last queued notice 142.44 ms (140), ACMP 32.89 (30), txL 49.66 (49). Not fixed here: a bound or the rule cannot move in this lane.
- #934 (the dev sync), #932 (#925) and #936 are composed in round 2 on the heads the manager names.
- A firmware campaign leaves two untracked `dispatch-build/keys/*.yaml` files in its checkout (pre-existing, before #935).

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

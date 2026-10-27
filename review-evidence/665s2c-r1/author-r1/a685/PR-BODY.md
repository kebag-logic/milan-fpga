[A685]

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

**The split CPU gets a 4 KiB instruction cache; it roughly halves the split firmware's service times but does not close T_svc = 10 ms at either point.**

- Composed maximum: 14.81 -> 8.60 ms at 1x1 with one interface, 27.84 -> 14.03 ms at 8x8 with two. Paths missing T_svc: 22 -> 13 of 81 at 1x1, 60 -> 34 of 129 at 8x8.
- The cost is 1.5 block RAM tiles, -9 LUTs and +173 FF on the product split CPU, out of context; the route closes at the shipping clocks.
- The all-fabric CPU and every shipped config's export are unchanged.
- Every gate rc 0, each at the head or at an earlier head whose later commits it does not read, except the docs workflow's `check_baremetal_only.py`, which fails on S2's own line (Known limitations): the self-test (86 checks, 57 of 57 mutants), the builder bank, behave (406 scenarios), 68 of 69 docs gates, the all-fabric export digest, and the four-shard Verilator sweep (64 of 64 suites, 2,190,531 checks).

`665-s2c-icache` -> `dev-soft-core`, head `2a7b0df53951cf00695b177b26c660ebe49a0f1a`, on S2's round 3 (`f8876638`, PR #792). It merges after #792.

## Linked Issue / roles

Relates to #665 (lane S2c). The cache alone does not close T_svc (acceptance item 4 asks for the residual, given below), and the requirement NFR-SCOUT-01 needs the owner's amendment (Known limitations).
Relates to #791 (the region decode, unchanged by the cache) and #397.

Executor: `[A685]`
Internal cleared-context reviewer: `[R713]`
External reviewer: `[R714]`

## Description

The assignment is [issuecomment-6421463860](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860), the owner's decision of 2026-10-26: an instruction cache is the first approach to the soft core's CPU budget.

| Piece | What changed |
|---|---|
| `sw/litex/milan_soc.py` | `CTRL_FETCH_L1 = (64, 1)` and `ctrl_cpu_args()`: under `--ctrl-mailbox` only, the CPU's generator options gain `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, the pinned VexiiRiscv's own fetch L1. No data cache. |
| `sw/builder/test_soc_options.py` | The constructor probe records the generator options; a new check requires the all-fabric CPU to keep exactly its arguments and the split CPU to add exactly the cache, and kills three planted defects (the split without its cache, the all-fabric with it, a data cache with it). |
| `tb/verilator/ctrl_service_budget/` | `--fetch-l1 split\|none\|SETSxWAYS` builds the split CPU, the cacheless core or a sweep point through the same function; the fetch observers follow the cache's refill bus, with the line read off the netlist; a reused build must be the selected cache and arm. `--xip` is a labelled hybrid-XIP arm: the image's own objects relinked with every function but the reset entry and F1's flash driver in the flash window. Five new self-test checks, five mutants. |
| `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 | The cache's parameters and reasons, the region decode, its block RAM and logic, and the requirement conflict. |
| `docs/design/MARK_II_AREA_PLAN.md` | The cache's 1.5 tiles debited in the block RAM ledger: 115.5 tiles (117.5 at 56 firmware tiles), against the 121.5 ceiling. |
| `tb/verilator/ctrl_service_budget/README.md` | The section "The instruction cache": the sweep, every arm, the backlog rows, the fan-out, the paths still missing, the XIP arm, block RAM and logic, the T_svc gap and the controls. |

**Parameters.** 4 KiB, direct-mapped, 64-byte lines (the generator's fixed line), one refill at a time, no prefetch. The sweep's knee: 2 KiB is 4 to 5 % slower and leaves three more paths missing; 8 and 16 KiB, one way or two, are 2 to 5 % faster for one to three more tiles. **No data cache:** with the DMA port an LSU L1 makes the generator build its coherent interconnect and hub instead of patch 0005's non-coherent fabric, and the measured data-side cost is mostly byte-loop stores, which S2b removes first.

| Instruction cache | Tiles, out of context (difference) | 1x1: composed maximum, ms | 1x1: under an unreleased load, at least | 1x1: paths (instances) missing T_svc | 8x8: composed maximum, ms | 8x8: under an unreleased load, at least | 8x8: paths (instances) missing T_svc |
|---|---:|---:|---:|---:|---:|---:|---:|
| none (S2) | 4.5 (+0) | 14.81 | 31.32 | 22 of 81 (58 of 141) | 27.84 | 44.19 | 60 of 129 (102 of 182) |
| 2 KiB, 1 way | 5.5 (+1) | 8.99 | 18.82 | 16 of 81 (41 of 141) | 14.58 | 29.73 | 37 of 129 (65 of 182) |
| 4 KiB, 1 way (split) | 6 (+1.5) | 8.60 | 19.32 | 13 of 81 (34 of 141) | 14.03 | 29.12 | 34 of 129 (66 of 182) |
| 8 KiB, 1 way | 7 (+2.5) | 8.40 | 18.96 | 13 of 81 (34 of 141) | 13.76 | 28.79 | 31 of 129 (59 of 182) |
| 8 KiB, 2 ways | 7.5 (+3) | 8.19 | 18.01 | 12 of 81 (33 of 141) | 13.63 | 28.35 | 29 of 129 (61 of 182) |
| 16 KiB, 1 way | 9 (+4.5) | 8.17 | 17.98 | 12 of 81 (33 of 141) | 13.53 | 28.17 | 29 of 129 (61 of 182) |

**The region decode (#791).** Every executable region is cacheable, so the cache's own region term is constant, and its region check is the cacheless fetch's expression. The decode is identical with and without the cache for the as-built regions, the harness's cover and the product split export. #791's non-power-of-two decode is therefore unchanged by the cache and stays #791's; the `as-built` control faults at the same call with the cache.

**The residual for S2b and the owner.** With the cache, the composed maximum is `memset` and `memcpy` 40 to 42 % (byte loops), the mailbox driver 12 to 21 %, AECP, ACMP and lwSRP's `mrp_mad` 15 to 21 %, and software multiply, divide and shift 7 %. In arm A, AECP's change-notice retry every millisecond sets every worst pass. Loads and stores now wait 39 to 40 % of the cycles. S2b's firmware items (word-wide copies, zeroing only what is sent, the retry backoff, the per-pass cap) address the first three; the M extension, a data cache and the clock remain the owner's.

**Hybrid XIP (D3 / S14).** A labelled arm runs every function but the reset entry and F1's flash driver from the flash window behind the cache. A refill from flash costs 2,100 to 2,160 CPU cycles against 42 from block RAM. Behind 4 KiB, 71 of 78 paths (1x1) and 111 of 125 (8x8) miss T_svc; behind 32 KiB (13 tiles), 19 of 81 and 50 of 129, with composed maxima of 23.42 and 30.99 ms. No path inside T_svc holds from flash, so D3's rule stands. Moving the code would free 20.5 tiles at 1x1 and 21 at 8x8 with two interfaces, planned. F1's flash driver must stay in block RAM: with it in flash the CPU stalled behind the command master's chip select and trapped (cause 2).

## Authoritative references

- The S2c assignment (issuecomment-6421463860); S2's result (issuecomment-6413711129) and round 3 (PR #792, `f8876638`); decisions D3 and D4 (issuecomment-6409738976); the branch policy (issuecomment-6409455089); the owner's all-fabric clarification (issuecomment-6410301079).
- `docs/reference/FR_NFR.md` 3.4.1 (T_svc = 10 ms) and NFR-SCOUT-01 (one cacheless RV32I control hart: see Known limitations).
- `docs/design/SPLIT_CONTROL_MEMORY.md` (the 56-tile allocation) and `docs/design/MARK_II_AREA_PLAN.md` (the block RAM ledger, the L11b core-pricing recipe).
- `sw/litex/patches/0004` and `0005` (the cacheless VexiiRiscv series); the pinned generator's `FetchL1Plugin` (64-byte line) and `Soc.scala` (the coherent interconnect an LSU L1 selects with DMA).
- #791 (the region decode); #397 (the one-hart rule).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2c-icache
git submodule update --init third_party/tsn-c-stack third_party/lwSRP
```

Use the capture prerequisites (`tb/verilator/nvm_capture_cpu/README.md#run`): the product LiteX tree and its virtual environment first on `PATH`, the pinned RV32 SDK, Verilator, `LITEX_ENV_CC_TRIPLE`, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`. Keep build directories outside the checkout.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 sw/builder/test_soc_options.py
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/s2c-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/s2c-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/s2c-1x1-none --fetch-l1 none --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/s2c-1x1-xip --xip --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/s2c-as-built --cpu-regions as-built
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/s2c-slow-adp --mutation slow-adp-rx
cd tests && behave
```

Expected result / pass criteria:

- The self-test prints `self-test: 0 failures`, with 57 `MUTANT caught` lines, rc 0.
- `test_soc_options.py` prints `Split placement CPU: the instruction cache on the split CPU only, 3 killed controls` and `RESULT: PASS`.
- The 1x1 run prints `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, rc 0; the 8x8 run `17 groups graded, 0 refusals, 66 T_svc misses (66 of 182 probe instances, 34 of 129 paths)`, rc 0. Each figure repeats to the cycle.
- The cacheless run (`--fetch-l1 none`) prints S2's round-3 figures: `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`.
- The XIP run prints `18 groups graded, 3 refusals, 120 T_svc misses (120 of 138 probe instances, 71 of 78 paths)`, rc 1: the refusals are probes whose bounded waits expired, a result of the arm.
- The controls print `CONTROL as-built caught: an instruction access fault (cause 1)` and `CONTROL slow-adp-rx caught: every control path missed T_svc`, rc 0.
- behave: 14 features, 406 scenarios, 1977 steps passed.

## Known limitations / out of scope

- **A requirement conflict, for the owner.** `docs/reference/FR_NFR.md` NFR-SCOUT-01 requires "one cacheless RV32I control hart", and `docs/ARCHITECTURE_HW_SW_SPLIT.md` repeats it. The owner's decision gives the split hart an instruction cache. This PR does not edit the requirement; the amendment needs the owner's text. The design doc records the conflict.
- The cache does not close T_svc; S2b's firmware work and the owner's core options follow.
- The docs workflow's `check_baremetal_only.py --check` fails on S2's `tb/verilator/ctrl_service_budget/scenario.py:805` comment ("the TX ring filled"), added at `cd3525c3` and present at S2's head `f8876638`. It is S2's line; this PR leaves it for S2's next round.
- Arm A's AECP change-notice retry makes some one-phase ACMP samples longer with the cache (an input lands in the next, shorter pass); their pass bounds and arm B show the cache's effect.
- The XIP arm is a labelled test arm; the real hybrid layout is S14's. The model's flash erase and program waits are zero.
- The cache's tiles are an out-of-context figure; the integrated route is M8a-2's.
- No hardware or bench evidence.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (NFR-SCOUT-01 awaits the owner's amendment)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

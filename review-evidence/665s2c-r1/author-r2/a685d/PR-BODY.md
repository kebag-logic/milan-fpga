[A685d]

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

**The split CPU gets a 4 KiB instruction cache. It cuts the split firmware's longest passes by a third to a half, but it does not close T_svc = 10 ms at either point.**

- Composed maximum over every backlog window: at least 31.32 -> at least 19.32 ms at 1x1 with one interface, and at least 44.19 -> at least 29.12 ms at 8x8 with two.
  - Both are lower bounds, with the cache and without it, because the two bound-talker windows never release SRP's 32 records.
  - Over the windows that released their whole load, the same windows with and without the cache: 14.81 -> 8.60 ms and 27.84 -> 14.03 ms.
- Paths missing T_svc: 22 -> 13 of 81 at 1x1, and 60 -> 34 of 129 at 8x8.
- The cost is 1.5 block RAM tiles, -9 LUTs and +173 FF on the product split CPU, out of context. The route closes at the shipping clocks.
- The all-fabric CPU and every shipped config's export are unchanged.
- **NFR-SCOUT-01 is amended.** The owner amended it on 2026-10-27 for this cache, and this PR applies the amendment: one RV32I control hart, with a 4 KiB direct-mapped instruction cache and no data cache in the split placement, and cacheless in the all-fabric placement. There is no open requirement conflict.
- Round 2 answers R713-1 and R714-1 (both NEGATIVE, MINOR findings only). It adds no measurement and changes no measured cycle count. It changes only the harness README, its self-test, the CPU option test, two source comments and two sentences of the area plan. Its last commit applies the amendment to four documents and changes nothing else.
- Gates at the head, rc 0 each:
  - the harness self-test: 93 checks, 70 of 70 mutants;
  - the CPU option test, with 6 killed controls on the split cache;
  - the split control memory test, which reads the amended design document;
  - the bare-metal scope gate;
  - the docs workflow's gates;
  - behave: 406 scenarios.
- The builder bank passed at the commit before the amendment (`de91db59`), with its one registered NOT RUN. The amendment changes four Markdown pages, which the bank does not read.
- Reruns at the head for this round's evidence:
  - the README's cacheless `slow-adp-rx` control measures the 24.614 ms printed beside it;
  - the README's fixture regeneration reproduces the committed `fixture.log` and `oracle.json` byte for byte;
  - the reviewers' planted mutants for R713-1-F4 and R714-1-F1 are all killed.

`665-s2c-icache` -> `dev-soft-core`, head `e0bb857a9f4b8e9d29736970a1135afde03260c5`. That is thirteen commits on S2's final head `f58d049b` (PR #792, both reviews POSITIVE): round 1's six and seven from this round. It merges after #792.

## Linked Issue / roles

Relates to #665 (lane S2c).
- The cache alone does not close T_svc. Acceptance item 4 asks for the residual, which is given below.
- NFR-SCOUT-01 is amended as the owner decided ([issuecomment-6434741232](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434741232) and its correction [issuecomment-6434744436](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434744436)).

Relates to #791 (the region decode, unchanged by the cache) and #397.

Executor: `[A685d]`, continuing `[A685]`, `[A685b]` and `[A685c]`'s lane
Internal cleared-context reviewer: `[R713]`
External reviewer: `[R714]`

## Description

The assignment is [issuecomment-6421463860](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860), the owner's decision of 2026-10-26: an instruction cache is the first approach to the soft core's CPU budget.
[issuecomment-6431653823](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6431653823) re-based the lane onto S2's final harness.
This round is [issuecomment-6433542516](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6433542516).

**The NFR-SCOUT-01 amendment.** The owner amended NFR-SCOUT-01 on 2026-10-27 ([issuecomment-6434741232](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434741232)), following the 2026-10-26 decision that the cache is the first approach. Its correction ([issuecomment-6434744436](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434744436)) keeps the all-fabric placement's hart cacheless, and its wording governs. Any change to the cache's geometry, or a data cache, needs the owner again. `docs/history/` is an archive and is not edited.

| Document | What changed |
|---|---|
| `docs/reference/FR_NFR.md:321` | NFR-SCOUT-01's first sentence: "The release architecture MUST use one RV32I control hart: in the split placement it has a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it stays cacheless." The rest of the row is unchanged. |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:62` | Its one repetition of "cacheless" for the control hart, in the same wording. The page uses no uppercase requirement keywords, so the sentence says "uses". |
| `docs/design/MARK_II_AREA_PLAN.md:383` | The control hart's row: "NFR-SCOUT-01: one RV32I hart, 4 KiB instruction cache, no data cache". |
| `docs/design/SPLIT_CONTROL_MEMORY.md:243-247` | The open-conflict paragraph is now a record of the amendment: its date, the decision and its correction, the old and new text, and that any change of geometry or a data cache needs the owner again. |

**Round 2: R713-1 and R714-1.**

| Finding | What changed | Evidence |
|---|---|---|
| R713-1-F1 (Conformance, Docs) | The six rows of the two "Paths that still miss T_svc" tables whose worst instance was never answered or never released now read "at least X, **never answered**" or "at least X, **never released**" in both ms columns, with the cycles cell marked the same way. A note above the tables states they are lower bounds and do not measure what the cache saves. | All 47 rows checked against the archived regrades of the 1x1 and 8x8 arms, with and without the cache: 0 mismatches. |
| R713-1-F2, R714-1-F2 (Docs) | The README states the measured rate: in Vivado, one tile for each 4 KiB of data and half a tile of tags for each way. | Every row of the README's Vivado table satisfies 4.5 + size / 4 KiB + 0.5 x ways. |
| R713-1-F3 (Docs, Tests) | S2's reproduction commands select `--fetch-l1 none`: the Results block (new), the controls, and the fixture regeneration, which now gives the run that records the fixture. The page says what the default commands give: the split cache's arms. The cache section's controls name their command, with `--fetch-l1 64x1`. | The documented cacheless `slow-adp-rx` control, rerun at the head, measures 24.614 ms. The documented fixture regeneration reproduces both committed files byte for byte. |
| R713-1-F4 (Tests) | Two self-test checks drive `run.main()` on temporary files, with the build's toolchain steps replaced. One builds and checks what `build.json` records for `fetch_l1` and `xip`. The other refuses a reused build of another fetch L1 or arm, reuses the selected one, and reuses a build that records no fetch L1 as cacheless. They replace the earlier check, which compared `built_as()` with `selected()` only. Three new mutants. | The reviewer's source mutants, replayed on a copy of the head, are killed: `run.py:317`'s condition set to `False`, and `build.py:520` recording `xip = False`. So is a third one, which builds with the default cache whatever the selection. |
| R714-1-F1 (Tests) | `test_soc_options.py` restates the split CPU's options, `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1` (4 KiB, one way, no LSU L1), and requires them exactly, not a pattern read back from the module under test. Three new killed controls: 128 sets, two ways, 32 sets. | R714-1's geometry probe at the head: the control passes, and 128 sets, two ways and 32 sets each fail. |
| Residue (R714-1 RES1, R713-1 RS1) | `build.py`'s XIP comment names no lane: "(#665, decision D3)" and "the saved-state flash driver (nvm_flash_litespi.c)". The check and mutant names say "the flash driver". | No lane or review label on any source line added since S2. |
| Residue (R714-1 RES2) | The XIP conclusion is worded to what was measured: the T_svc service paths stay in block RAM, as D3 rules. | README "The hybrid-XIP arm" |
| Residue (R713-1 RS2 to RS4) | The area plan's "All four" and "None of these numbers"; this Status sentence; "a CPU of 13 tiles". | |

The two residue texts for `build.py:149` differ. RES1's "(#665, decision D3)" is applied, keeping the D3 citation at `:153`. RS1's "(#665, the hybrid-XIP decision)" is not.

| Piece | What changed |
|---|---|
| `sw/litex/milan_soc.py` | `CTRL_FETCH_L1 = (64, 1)` and `ctrl_cpu_args()`. Under `--ctrl-mailbox` only, the CPU's generator options gain `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, the pinned VexiiRiscv's own fetch L1. No data cache. |
| `sw/builder/test_soc_options.py` | The constructor probe records the generator options. The split-cache check requires the all-fabric CPU to keep exactly `--xlen=32`, and the split CPU to have exactly `--xlen=32 --fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1`, restated in the test. It kills six planted defects: the split without its cache, the all-fabric with it, a data cache with it, 128 sets, two ways, and 32 sets. |
| `tb/verilator/ctrl_service_budget/` | `--fetch-l1 split\|none\|SETSxWAYS` builds the split CPU, the cacheless core or a sweep point through the same function. The fetch observers follow the cache's refill bus, with the line read off the netlist. A reused build must be the selected cache and arm. `--xip` is a labelled hybrid-XIP arm: the image's own objects are relinked with every function but the reset entry and the saved-state flash driver in the flash window. Six self-test checks and eight mutants. |
| `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 | The cache's parameters and reasons, the region decode, its block RAM and logic, and the record of the NFR-SCOUT-01 amendment. |
| `docs/design/MARK_II_AREA_PLAN.md` | The cache's 1.5 tiles, debited in the block RAM ledger: 115.5 tiles (117.5 at 56 firmware tiles), against the 121.5 ceiling. The control hart's row cites the amended NFR-SCOUT-01. |
| `docs/reference/FR_NFR.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md` | NFR-SCOUT-01 as amended, and the architecture's repetition of it. |
| `tb/verilator/ctrl_service_budget/README.md` | The section "The instruction cache": the sweep, the backlog windows one by one, every arm, the backlog rows, the fan-out, the paths still missing, the XIP arm, block RAM and logic, the T_svc gap and the controls. |

**Parameters.** 4 KiB, direct-mapped, 64-byte lines (the generator's fixed line), one refill at a time, no prefetch.
- The sweep's knee, on the windows that released their load: 2 KiB is 4 to 5 % slower and leaves three more paths missing. 8 and 16 KiB, with one way or two, are 2 to 5 % faster for one to three more tiles.
- The composed maximum is a lower bound at every size, so it does not rank the sizes.
- **No data cache:** with the DMA port, an LSU L1 makes the generator build its coherent interconnect and hub instead of patch 0005's non-coherent fabric. The measured data-side cost is mostly byte-loop stores, which S2b removes first.

| Instruction cache | Tiles, out of context (difference) | 1x1: composed maximum, every backlog window, ms | 1x1: over the windows that released their whole load only, ms | 1x1: paths (instances) missing T_svc | 8x8: composed maximum, every backlog window, ms | 8x8: over the windows that released their whole load only, ms | 8x8: paths (instances) missing T_svc |
|---|---:|---:|---:|---:|---:|---:|---:|
| none (S2) | 4.5 (+0) | at least 31.32 | 14.81 | 22 of 81 (58 of 141) | at least 44.19 | 27.84 | 60 of 129 (102 of 182) |
| 2 KiB, 1 way | 5.5 (+1) | at least 18.82 | 8.99 | 16 of 81 (41 of 141) | at least 29.73 | 14.58 | 37 of 129 (65 of 182) |
| 4 KiB, 1 way (split) | 6 (+1.5) | at least 19.32 | 8.60 | 13 of 81 (34 of 141) | at least 29.12 | 14.03 | 34 of 129 (66 of 182) |
| 8 KiB, 1 way | 7 (+2.5) | at least 18.96 | 8.40 | 13 of 81 (34 of 141) | at least 28.79 | 13.76 | 31 of 129 (59 of 182) |
| 8 KiB, 2 ways | 7.5 (+3) | at least 18.01 | 8.19 | 12 of 81 (33 of 141) | at least 28.35 | 13.63 | 29 of 129 (61 of 182) |
| 16 KiB, 1 way | 9 (+4.5) | at least 17.98 | 8.17 | 12 of 81 (33 of 141) | at least 28.17 | 13.53 | 29 of 129 (61 of 182) |

Arm B runs three of the four backlog rows, as S2's arm B does. Its figure is partial, over 3 of 4 windows: 8.61 ms at 1x1 and 14.07 ms at 8x8, against S2's 14.81 and 27.84 ms.

**Notification fan-out, whole.** With the cache, over every fan-out measured, on every interface and in both arms:
- a recipient costs 7,054 to 15,334 CPU cycles (7,144 to 13,114 in arm A), against S2's 11,786 to 22,030;
- the 16 recipients at 1x1 take 4.42 to 8.70 ms, and every fan-out fits T_svc there;
- the 32 at 8x8 take 8.25 to 18.19 ms. 5 of arm A's 13 fan-outs and 10 of arm B's 22 still miss, and none is over the 24 ms ceiling.

**The region decode (#791).** Every executable region is cacheable, so the cache's own region term is constant, and its region check is the cacheless fetch's expression.
- The decode is identical with and without the cache for the as-built regions, the harness's cover and the product split export.
- So #791's non-power-of-two decode is unchanged by the cache and stays #791's. With the cache, the `as-built` control faults at the same call.

**The residual for S2b and the owner.** In arm A, AECP's change-notice retry every millisecond sets every worst pass and the composed maximum at both points.
- The composed maximum's pass is:
  - `memset` and `memcpy` (byte loops), 65 % at 1x1 and 43 % at 8x8;
  - AECP, ACMP and lwSRP's `mrp_mad`, 18 % and 39 %;
  - the mailbox driver, 7 % and 6 %;
  - software multiply, divide and shift, 3 %.
- The longest pass of the windows that released their load is:
  - `memset` and `memcpy`, 40 to 42 %;
  - the mailbox driver, 12 to 21 %;
  - AECP, ACMP and `mrp_mad`, 15 to 21 %;
  - software arithmetic, 7 %.
- Loads and stores now wait 39 to 40 % of the cycles.
- S2b's firmware items address the first three: word-wide copies, zeroing only what is sent, the retry backoff and the per-pass cap. The M extension, a data cache and the clock remain the owner's.

**Hybrid XIP (D3 / S14).** A labelled arm runs every function but the reset entry and the saved-state flash driver from the flash window, behind the cache.
- A refill from flash costs 2,100 to 2,160 CPU cycles, against 42 from block RAM.
- Behind 4 KiB, 71 of 78 paths (1x1) and 111 of 125 (8x8) miss T_svc.
- Behind 32 KiB (a CPU of 13 tiles), 19 of 81 and 50 of 129 miss. Over the windows that released their load, the longest pass is 23.42 and 30.99 ms, against the cacheless core's 14.81 and 27.84.
- With every function but the reset entry and the flash driver in flash, more paths miss T_svc (19 of 81 and 50 of 129 behind 32 KiB, against 13 and 34 with the code in block RAM), so the T_svc service paths stay in block RAM, as D3 rules. Moving the code would free 20.5 tiles at 1x1 and 21 at 8x8 with two interfaces, planned.
- The saved-state flash driver must stay in block RAM. With it in flash, the CPU stalled behind the command master's chip select and trapped (cause 2).

## Authoritative references

- The S2c assignment (issuecomment-6421463860), the re-base round (issuecomment-6431653823) and this round (issuecomment-6433542516).
- The owner's NFR-SCOUT-01 amendment (issuecomment-6434741232) and its correction (issuecomment-6434744436).
- R713-1 (PR #796, issuecomment-6433539808) and R714-1 (PR #796, issuecomment-6433362127).
- S2's result (issuecomment-6413711129) and S2's final head (PR #792, `f58d049b`).
- Decisions D3 and D4 (issuecomment-6409738976), the branch policy (issuecomment-6409455089) and the owner's all-fabric clarification (issuecomment-6410301079).
- `docs/reference/FR_NFR.md` 3.4.1 (T_svc = 10 ms) and NFR-SCOUT-01, as amended (one RV32I control hart, with this instruction cache in the split placement).
- `docs/design/SPLIT_CONTROL_MEMORY.md` (the 56-tile allocation) and `docs/design/MARK_II_AREA_PLAN.md` (the block RAM ledger and the L11b core-pricing recipe).
- `sw/litex/patches/0004` and `0005` (the cacheless VexiiRiscv series).
- The pinned generator's `FetchL1Plugin` (its 64-byte line) and `Soc.scala` (the coherent interconnect an LSU L1 selects with DMA).
- #791 (the region decode) and #397 (the one-hart rule).

## How to get into the same state

```sh
git fetch origin
git checkout 665-s2c-icache
git submodule update --init third_party/tsn-c-stack third_party/lwSRP
```

Use the capture prerequisites (`tb/verilator/nvm_capture_cpu/README.md#run`):
- the product LiteX tree, with its virtual environment first on `PATH`;
- the pinned RV32 SDK and Verilator;
- `LITEX_ENV_CC_TRIPLE`, `PYTHONHASHSEED=0`, `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.

Keep build directories outside the checkout.

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 scripts/check_baremetal_only.py --check
python3 sw/builder/test_soc_options.py
python3 sw/litex/test_ctrl_memory.py
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir ../s2c-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-1x1-none --fetch-l1 none --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-1x1-xip --xip --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-as-built --cpu-regions as-built
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir ../s2c-slow-adp-none --fetch-l1 none --mutation slow-adp-rx
cd tests && behave
```

Expected result / pass criteria:

- The self-test prints `self-test: 0 failures`, with 93 `PASS` and 70 `MUTANT caught` lines, rc 0. Among them are `PASS: the run builds and records the fetch L1 and the arm it selected` and `PASS: the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless`.
- `check_baremetal_only.py --check` prints `baremetal-only: OK`, rc 0.
- `test_ctrl_memory.py` ends `RESULT: PASS`, rc 0.
- `test_soc_options.py` prints `Split placement CPU: the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls` and `RESULT: PASS`.
- The 1x1 run prints `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, rc 0. Its `table.md` prints `Composed maximum over the 4 backlog windows: at least 966,218 CPU cycles (19.324 ms), backlog-adp-refill, a lower bound (load unreleased in backlog-adp, backlog-adp-refill).`
- The 8x8 run prints `17 groups graded, 0 refusals, 66 T_svc misses (66 of 182 probe instances, 34 of 129 paths)`, rc 0. Each figure repeats to the cycle.
- The cacheless run (`--fetch-l1 none`) prints S2's figures, `18 groups graded, 0 refusals, 58 T_svc misses (58 of 141 probe instances, 22 of 81 paths)`, and its `table.md` equals S2's final A1 table.
- The XIP run prints `18 groups graded, 3 refusals, 120 T_svc misses (120 of 138 probe instances, 71 of 78 paths)`, rc 1. The refusals are probes whose bounded waits expired, a result of the arm.
- The controls print `CONTROL as-built caught: an instruction access fault (cause 1)` and `CONTROL slow-adp-rx caught: every control path missed T_svc`, rc 0. The planted path measures `BUDGET control.discover.if0: 16.556 ms over T_svc 10 ms` on the split cache, and `24.614 ms` on the cacheless core, as the README gives both.
- behave: 14 features, 406 scenarios and 1977 steps passed.

## Known limitations / out of scope

- **The amendment's listed edits, and two sentences it does not list.** This PR makes the four edits the owner listed and no others. Two places are left as they are, for the owner or a reviewer to decide:
  - `docs/reference/FR_NFR.md:6`, the page's introduction, still says "The release uses one cacheless RV32I control hart". The amendment names only NFR-SCOUT-01's row on that page.
  - `docs/design/MARK_II_AREA_PLAN.md:383` now carries the owner's text. That row's figures (3,522 LUT, 4,736 FF) are the hart of the routed image in the plan's historical inventory at `e6172750`, before the split: the all-fabric hart, which stays cacheless.
  - The area plan's D5 lines (`:610`, `:1302`, `:1357`) and the cacheless patch series name the 2026-08 decision and the cacheless cores as priced, and are not repetitions of NFR-SCOUT-01.
- The cache does not close T_svc. S2b's firmware work, which now runs on the cached core, and the owner's core options follow.
- Arm A's AECP change-notice retry makes some one-phase ACMP samples longer with the cache, because an input lands in the next, shorter pass. Their pass bounds and arm B show the cache's effect.
- The XIP arm is a labelled test arm; the real hybrid layout is S14's. The model's flash erase and program waits are zero.
- The self-test's build check stands a recorder in for the SoC export, which needs LiteX. `split_soc.build`'s own record of its selection is attested by each run's `build.json`, not by the portable self-test.
- The reviewers' optional suggestions are not taken this round: comparing the resolved geometry on reuse, refusing `--xip --fetch-l1 none`, and a synthetic refill trace for `sim_main.cpp`, with `xip_offset()`'s coverage. R713-1's other source probes (the flash image hand-off, `split_soc`'s geometry and the native model's refill accounting) still survive the portable self-test.
- The cache's tiles are an out-of-context figure; the integrated route is M8a-2's.
- No hardware or bench evidence.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains (NFR-SCOUT-01 is amended as the owner decided; `FR_NFR.md:6`'s introduction, outside the amendment's listed edits, still says cacheless)
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

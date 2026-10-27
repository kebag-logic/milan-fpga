# [A685] #665 lane S2c: an L1 instruction cache on the split SoC's soft core (HANDOFF)

Status: **REVIEW READY**, 2026-10-27.

- Branch `665-s2c-icache`, local, not pushed. Head: see section 5.
  - The lane started on S2's round-2 head `cd3525c3` on `dev-soft-core` `e76a755a`. Verified: the merge base with `origin/dev-soft-core` is `e76a755a`, not dev. `origin/dev-soft-core` has since moved to `9220f9b3`, a dev sync for #784.
  - S2's round 3 (`f8876638`, PR #792, REVIEW READY 2026-10-26 17:06) landed during the lane. The lane's commits were re-based onto it, as the lane's brief directs ("re-base onto its later rounds when they land"). The pre-rebase head is kept as the local ref `s2c-before-r3` (`179228603b`).
  - Commits: one-line subjects, no body, no trailers.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). Each submodule's toplevel and origin were verified before any git command used it.
- Assignment: issuecomment-6421463860. TAKEN: issuecomment-6421656283 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6431631510 (`REVIEW-READY-COMMENT.md`).
- Nothing pushed. No PR, no issue or comment edit. No bench, no hardware, no flashing.
- Vivado ran only under `$VIVADO_LOCK`, out of context on CPU netlists (no SoC route), with MemAvailable above 38 GB and no sweep running.

## Contents

1. Result
2. Acceptance
3. Changes, file:line and reason
4. New checks, planted mutants and failing words
5. Gate table
6. Run history and reproducibility
7. Findings, decisions and open questions

## 1. Result

**The 4 KiB instruction cache roughly halves the split firmware's service times, but does not close T_svc at either point.**

| Figure (S2's harness at round 3, arm A) | 1x1, none | 1x1, 4 KiB | 8x8, none | 8x8, 4 KiB |
|---|---:|---:|---:|---:|
| Composed maximum (a window that released its load) | 14.81 ms | **8.60 ms** | 27.84 ms | **14.03 ms** |
| Longest pass under a load left unreleased (lower bound) | 31.32 ms | 19.32 ms | 44.19 ms | 29.12 ms |
| Worst pass | 31.32 ms | 19.32 ms | 59.79 ms | 37.89 ms |
| Paths (instances) missing T_svc | 22 of 81 (58 of 141) | 13 of 81 (34 of 141) | 60 of 129 (102 of 182) | 34 of 129 (66 of 182) |
| CPU cycles per instruction | 9.52 | 5.83 | 9.49 | 5.65 |
| Data-side waits / cycles | 0.226 | 0.390 | 0.233 | 0.403 |

- Parameters: 4 KiB, 64 sets, 1 way, 64-byte line (fixed by the pinned generator), one refill at a time, no prefetch, no data cache. `milan_soc.CTRL_FETCH_L1 = (64, 1)`.
- Sweep (composed maximum, 1x1 / 8x8): none 14.81 / 27.84; 2 KiB 8.99 / 14.58; 4 KiB 8.60 / 14.03; 8 KiB 8.40 / 13.76; 8 KiB 2-way 8.19 / 13.63; 16 KiB 8.17 / 13.53 ms. 4 KiB is the knee.
- Block RAM: +1.5 tiles out of context on the product split CPU (4.5 -> 6.0: +1 RAMB36, +1 RAMB18); LUT 3,091 -> 3,082, FF 5,017 -> 5,190; routed at 20 / 10 ns with WNS +0.607 ns, WHS +0.003 ns. Outside the 56-tile firmware allocation; debited in the plan's ledger: 114 -> 115.5 tiles (116 -> 117.5 at 56 firmware tiles).
- The residual is the data side's: `memset`/`memcpy` 40 to 42 % of the composed maximum, the mailbox driver 12 to 21 %, AECP/ACMP/`mrp_mad` 15 to 21 %, software arithmetic 7 %; in arm A AECP's 1 ms change-notice retry sets every worst pass (`memset` 49 to 63 % of it).
- Hybrid XIP: no path inside T_svc holds with the code in flash, behind 4 KiB or 32 KiB; moving it would free 20.5 / 21 tiles (section 7).
- Arms B, SHUTDOWN and the three controls: see the README section and section 4.

## 2. Acceptance

| Item (issuecomment-6421463860) | Status | Evidence |
|---|---|---|
| 1. L1 instruction cache through the generator's own options, no hand-edited netlist; parameters with reasons | met | `milan_soc.py:2815-2833`, `:2900-2903`; `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 |
| 1. All-fabric CPU byte-identical | met | export proof, five shipped configs, normalised digest identical per config; all-fabric CPU netlist `VexiiRiscvLitex_f5f08b17` at base and head; `test_soc_options.py` split-cache test |
| 1. Split region decode exact; #791 where the cache's region settings touch it | met as scoped: the cache's own region term is constant (every executable region is cacheable), and its region check is the cacheless fetch's expression; `pma_compare.py` finds the decode identical with and without the cache for the as-built regions, the harness cover and the product split export. #791's non-power-of-two decode is unchanged and stays #791's | `receipts/pma/` |
| 2. S2's harness at both points with the cache against S2's no-cache tables: worst pass, composed maximum, every backlog row, fan-out, cycles per path | met | README "The instruction cache"; every arm's `table.md` and `results.json` in `receipts/runs/`; `receipts/report.md` |
| 2. At least two sizes, the curve | met: 2, 4, 8, 8 (2-way), 16 KiB at both points | README "The sweep" |
| 2. Block RAM and LUT/FF from Yosys and the OOC run, against the 56-tile ledger and the area plan | met | README "Block RAM and logic"; design doc section 7; `MARK_II_AREA_PLAN.md` ledger row |
| 3. Hybrid XIP: paths with hot code in flash behind the cache; whether they hold; BRAM freed | met: they do not hold (4 KiB and 32 KiB); 20.5 / 21 tiles freed, planned | README "The hybrid-XIP arm"; section 7 |
| 4. Tables with the remaining T_svc gap at each point; residual for S2b and the owner's options | met: the cache alone does not close T_svc | README "The T_svc gap" |
| 5. Firmware behaviour and tests, mailbox contract unchanged | met: no firmware, test-fixture or contract file changed | `git diff f8876638..HEAD --stat` |

The PR body says "Relates to #665": T_svc is not closed, and the requirement text NFR-SCOUT-01 conflicts (section 7).

## 3. Changes, file:line and reason

Line numbers are at the head.

| File:line | What | Reason |
|---|---|---|
| `sw/litex/milan_soc.py:2815-2833` | `CTRL_FETCH_L1 = (64, 1)` and `ctrl_cpu_args()`, the generator options `--fetch-l1 --fetch-l1-sets=64 --fetch-l1-ways=1` | The owner's decision; one statement of the split CPU's cache, used by the SoC and the harness |
| `sw/litex/milan_soc.py:2900-2903` | Under `ctrl_mailbox` only, the options join `vexii_args` | The split CPU gains the cache; the all-fabric arguments, netlist and export stay byte-identical |
| `sw/litex/milan_soc.py:2878-2879` | Comment: the product gate accepts only RV32 VexiiRiscv, cacheless except the split's instruction cache | The comment said "cacheless" only |
| `sw/builder/test_soc_options.py:44-50`, `:75`, `:88`, `:217-248`, `:294` | The constructor probe records the generator options; `test_split_cache` checks the all-fabric CPU keeps exactly `--xlen=32` and the split adds exactly `ctrl_cpu_args`, with three killed controls | A self-checking test for the changed behaviour, run by `test_builder.py` |
| `tb/verilator/ctrl_service_budget/split_soc.py:257-271` | `fetch_l1_geometry`: `split`, `none` or `SETSxWAYS` | The sweep runs the split's cache, the cacheless core and test-only sizes through the same generator option |
| `split_soc.py:322-330`, `:353` | The CPU's `extra_scala_args` carry `milan_soc.ctrl_cpu_args(geometry)`; `soc.json` records the selection | The harness CPU is the split CPU's, by the same function |
| `tb/verilator/ctrl_service_budget/build.py:335-353` | `fetch_bus`: the fetch observers read the fetch L1's refill bus when the CPU has one; a refill's beats are read off the netlist's line-aligned refill address | The cacheless fetch bus does not exist in a cached netlist; the line is derived, never restated |
| `build.py:397-406` | `budget_config.hpp` gets `fetch_beats` and, with the cache, id accessors that read 0 | The cache has one refill in flight and no id |
| `build.py:149-210` | `XIP_TEXT`, `xip_offset`, `xip_script`, `xip_image`: the labelled hybrid-XIP arm relinks the image's own objects through `ctrl_srp_image.link` with every function in the flash window except the reset entry and F1's flash driver; rom is built from the relinked ELF without its flash code; the flash device is preloaded at the first erase block past the AEM slot | Item 3, test code only; the driver stays in block RAM as D3 requires (section 7) |
| `build.py:494-520` | `Core(cpu_regions, fetch_l1, xip)` and `build(..., core=...)` | The build's CPU and code placement as one parameter (the idiom gate's parameter limit) |
| `tb/verilator/ctrl_service_budget/run.py:146-151` | `--fetch-l1` and `--xip` | The selections |
| `run.py:245-254`, `:276-281` | `selected` and `built_as`: a reused build must be the selected point, regions, mutation, variant, fetch L1 and arm; a build recording no fetch L1 is cacheless | Reuse never mixes CPUs |
| `run.py:290` | A group runs with the build's flash image | The XIP arm's code is in the flash device |
| `tb/verilator/ctrl_service_budget/sim_main.cpp:266-287`, `:474` | A fetch command carries `fetch_beats` words; its wait runs to its last beat or its error, once; the code-coverage marks cover the whole line | One sampling path for both fetch buses; the cacheless arms reproduce S2 byte for byte |
| `tb/verilator/ctrl_service_budget/observe.vlt:2-4`, `:17-21` | `public_flat_rd` on the fetch L1's refill bus | Passive observation of the cached CPU |
| `selftest.py:637-679`, `:682` | `cache_checks`, five checks (section 4) | Self-protection of the new rules |
| `selftest_mutants.py:249-268`, `:352-361` | Five mutants (section 4) | Each new rule must fail a named check when broken |
| `tb/verilator/ctrl_service_budget/README.md` | Lead, run options, the test SoC's CPU, fetch counting, the section "The instruction cache", the new checks, mutants and limits | Documents the cache arms and their results |
| `docs/design/SPLIT_CONTROL_MEMORY.md` section 7 | Parameters and reasons, the decode, the product OOC table, the ledger, the requirement conflict | The authoritative statement of the split CPU's cache |
| `docs/design/MARK_II_AREA_PLAN.md` ledger | +1.5 tiles: 115.5 (116.5 with every bank in block RAM; 117.5 at 56 firmware tiles) | The cache's block RAM debited in the split only |

## 4. New checks, planted mutants and failing words

Self-test: `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` prints `self-test: 0 failures`, with 86 `PASS` checks and 57 `MUTANT caught` lines (round 3's 81 and 52 plus this lane's 5 and 5).

| New check (as printed) | Planted mutant (`selftest_mutants.py`) | Failing words |
|---|---|---|
| the fetch observers follow the CPU's fetch plugin | fetch bus: the cacheless observers on a cached CPU | `MUTANT caught: fetch bus: the cacheless observers on a cached CPU: the fetch observers follow the CPU's fetch plugin` |
| a refill's beats are read off the netlist | fetch bus: one beat a refill | `MUTANT caught: fetch bus: one beat a refill: a refill's beats are read off the netlist ((1, 1))` |
| a cached netlist without its line-aligned refill address is refused | (the refusal is the check) | `FAIL: a cached netlist without its line-aligned refill address is refused: accepted` if it ever passes one |
| a reused build of another fetch L1 or arm is refused; a build with no fetch L1 is cacheless | reuse: the fetch L1 and the arm are not compared | `MUTANT caught: reuse: the fetch L1 and the arm are not compared: a reused build of another fetch L1 or arm is refused; ...` |
| the XIP arm keeps the reset entry and F1's flash driver in rom and moves the other code to flash | xip: the reset entry moves to flash with the other code; xip: F1's flash driver moves to flash with the other code | `MUTANT caught: xip: ...: the XIP arm keeps the reset entry and F1's flash driver in rom ...` |

`sw/builder/test_soc_options.py` `test_split_cache` prints `Split placement CPU: the instruction cache on the split CPU only, 3 killed controls`:

| Planted control (source mutation of `milan_soc.py`) | Failing words |
|---|---|
| the split CPU without its cache | `killed: the split CPU without its cache` |
| the all-fabric CPU with the cache | `killed: the all-fabric CPU with the cache` |
| a data cache with it (`--lsu-l1` appended) | `killed: a data cache with it` |

Full-harness controls on the cached CPU (`--fetch-l1 64x1`), each rc 0:

| Control | Measured | Words |
|---|---|---|
| `slow-adp-rx` | `BUDGET control.discover.if0: 16.556 ms over T_svc 10 ms` (unplanted 0.513 ms) | `CONTROL slow-adp-rx caught: every control path missed T_svc` |
| `slow-adp-shutdown` (shutdown-entry) | `BUDGET control.shutdown.if0: 16.328 ms` (unplanted 0.333 ms) | `CONTROL slow-adp-shutdown caught: every control path missed T_svc` |
| `as-built` | `TRAP 151504 0 1 00006880` repeated | `CONTROL as-built caught: an instruction access fault (cause 1)` |

## 5. Gate table

Head `2a7b0df53951cf00695b177b26c660ebe49a0f1a` (`665-s2c-icache`, five commits on S2's round 3 `f8876638`). Every gate ran in the foreground or as a polled background job, unpiped, with its rc on its log's last line in `receipts/gates/` unless named otherwise. A gate run at an earlier head is named with it; nothing it reads changed after that head (the commits after `f3c71e42` touch only the harness README, and after `7e1124be` only the harness's XIP link script, self-test, README and two design documents).

| Gate | Command | Head | Result |
|---|---|---|---|
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | `2a7b0df5` | rc 0: 86 checks, 57 of 57 mutants caught, `self-test: 0 failures` |
| CPU option test | `python3 sw/builder/test_soc_options.py` | `2a7b0df5` | rc 0: 52 constructor and 18 CLI cases, 9 killed controls; split cache, 3 killed controls; `RESULT: PASS` |
| Builder bank | `python3 sw/builder/test_builder.py --require-rv32` | `7e1124be` | rc 0: `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a local Arty build report, as in S1); 1,896 s |
| BDD conformance (rtl-fast) | `cd tests && behave` | `2a7b0df5` (tree) | rc 0: 14 features, 406 scenarios, 1977 steps |
| Docs gates (the docs workflow's 69 commands, pinned renderer and HDL parser) | `scripts/docs_gates.sh` | `2a7b0df5` (tree) | 68 of 69 rc 0. `check_baremetal_only.py --check` rc 1 on `tb/verilator/ctrl_service_budget/scenario.py:805` ("TX ring"), a line S2 added at `cd3525c3`; it fails the same way at S2's head `f8876638`, and passes at `e76a755a` (section 7) |
| Python idiom, self-test | `python3 scripts/check_py_idiom.py`, `--selftest` | `2a7b0df5` | rc 0, rc 0 |
| C++ idiom, self-test | `python3 scripts/check_cpp_idiom.py`, `--selftest` | `2a7b0df5` | rc 0, rc 0 |
| Hygiene, TODO ownership, SoC sources, RTL source lists | `check_hygiene.py --check`, `check_todo_ownership.py`, `check_soc_sources.py`, `check_rtl_source_lists.py` | `2a7b0df5` | rc 0 each |
| Whitespace | `git diff --check f8876638 HEAD` | `2a7b0df5` | rc 0 |
| All-fabric export digest, five shipped configs | `scripts/export_compare.sh` (S1's method) | base `e76a755a`, head `f3c71e42` | rc 0: normalised digest identical per config; 3,856 of 3,876 files byte-identical, the other 20 run stamps, archive member times, the hierarchy comment's order and the log's interleaving. All-fabric CPU netlist `VexiiRiscvLitex_f5f08b17` at both, sha256 `c208df0b...`, the netlist `MARK_II_AREA_PLAN.md` L11b records. The split export differs only in the CPU netlist's name (3 files) |
| Region decode | `pma_compare.py` | netlists | identical with and without the cache: as-built regions, the harness cover, the product split export |
| Four-shard Verilator sweep | `native-shards.py` (pinned Verilator 5.050, sv2v 0.0.12) | `f3c71e42` | rc 0 per shard: 64 of 64 suites (15 + 17 + 16 + 16), 2,190,531 checks, 0 in-suite failures, 0 timed out; `tsn_fuzz` declares its field campaigns skipped (tsn-gen absent). Shards 0, 1 and 3 in booked units (`MAKEFLAGS=-j4`); shard 2 in the lane's unit with `MAKEFLAGS=-j1 VERILATOR_JOBS=4`, the hosted runners' settings, after four OOM kills at the shard unit's 10 GB (section 6) |
| Head regrade, every arm | `scripts/regrade_head.sh` | `2a7b0df5` | every table byte-identical to its run's; rc 0 except the two 4 KiB XIP arms (rc 1: their refused probes, as the run gave) |
| Harness arms | `run.py --point P --build-dir B [--fetch-l1 G] [--variant V] [--mutation M] [--xip] [--record-budget-findings]` | built at `5fa7e956` to `f3c71e42`, regraded at `2a7b0df5` | section 6 |
| Yosys pricing | `price_yosys.py` (`synth_xilinx -family xc7 -flatten`, Yosys 0.66) | netlists | 11 netlists, rc 0 |
| Vivado out of context | `ooc_cpu.sh` under `$VIVADO_LOCK` | netlists | 11 runs, rc 0 each; synthesis, place and route at 20 / 10 ns, every WNS and WHS positive |

## 6. Run history and reproducibility

- **Reproduction of S2.** The cacheless arms at this lane's harness reproduce S2 byte for byte: at round 2, both points' `table.md` equal S2's round-2 A1 and A8 tables and five logs compared equal; under round 3, both equal S2's round-3 A1 and A8 tables.
- **Round 2 to round 3.** The first arms ran S2's round-2 scenario. After the re-base, `complete_r3.sh` ran the two groups round 3 changed or added (`backlog-owed`, `aecp-fanout`) on each arm's attested build and regraded every group with round 3's grader; arm B got `aecp-fanout` the same way. Round 3 changes no build input, so the builds stayed valid.
- **Two driver faults, no measurement effect.** The first completion chain used a shell variable named `GROUPS`, which bash reserves; it ran nothing and was redone. The two 2 KiB legs were running when the re-base replaced the grader under them; their simulations completed and only their grading failed, and the completion regraded them.
- **The XIP arm, twice.** The first XIP run put F1's flash driver in flash too and trapped (section 7); the arm was changed to keep the driver in block RAM, and all four XIP legs ran again. The first run's table and a trap excerpt are in `receipts/allflash-xip/`.
- **The sweep.** A serial sweep in the lane's unit was started first: under `nohup` the preflight's hang-up control could not stop its child and the preflight aborted; it was stopped and replaced by the four-shard sweep. Shard 2 was OOM-killed four times at its unit's 10 GB cap while building `capture_coherence`'s `milan_datapath` model (Verilator `-j 0` twice, then 4, then 2, each with `MAKEFLAGS=-j4`); it was then run in the lane's own unit with the hosted runners' settings, `MAKEFLAGS=-j1` and `VERILATOR_JOBS=4`. One retry was launched on a range that had been booked in the meantime and was stopped within a minute.
- **Head regrade.** Every arm was regraded at the head on its attested build; every `table.md` is byte-identical (`receipts/head-regrade/`).
- **Determinism.** Each arm's build records every input's digest; reuse and regrade refuse a changed one. The builds are not committed; `receipts/builds/` holds every `build.json` and `soc.json`, and `receipts/netlists/` every CPU netlist's size and sha256.

## 7. Findings, decisions and open questions

1. **Requirement conflict, for the owner.** `docs/reference/FR_NFR.md` NFR-SCOUT-01: "The release architecture MUST use one cacheless RV32I control hart." `docs/ARCHITECTURE_HW_SW_SPLIT.md` repeats it. The owner's decision gives the split hart an instruction cache. AGENTS section 2: published, not chosen privately; the requirement text is not edited. A possible amendment for the owner: "one RV32I control hart; the split placement's hart fetches through an L1 instruction cache sized in `SPLIT_CONTROL_MEMORY.md`, and its data side is cacheless."
2. **The cache does not close T_svc.** 1x1: composed maximum 8.60 ms, but 13 of 81 paths miss and the worst pass is 19.32 ms (#397's one-hart rule fails). 8x8: composed maximum 14.03 ms, 34 of 129 paths miss, worst pass 37.89 ms. The residual is the data side's (section 1); S2b's firmware items and the owner's options (M extension, a data cache with the coherent interconnect it needs, the clock) remain. S2b's STOP (issuecomment-6422817781, on the cacheless core and S2's round-1 harness) brings the composed maximum to 4.75 / 8.74 ms in firmware alone; the two were not measured together.
3. **Hybrid XIP.** With the code in flash, a refill costs 2,100 to 2,160 CPU cycles against 42. At 4 KiB: CPI 34 / 22, 71 of 78 and 111 of 125 paths miss, three and four probes' bounded waits expire. At 32 KiB (13 tiles): CPI 10 / 9, 19 of 81 and 50 of 129 paths miss, composed maxima 23.42 / 30.99 ms, against 8.60 / 14.03 with 4 KiB in block RAM. Moving the code frees 20.5 tiles (1x1) and 21 (8x8 two interfaces), planned. D3's rule holds: no path inside T_svc can run from the flash, even behind 32 KiB.
4. **F1's flash driver cannot run from flash.** With the driver in flash, the CPU stalled in `ls_window` (`0x2041effc`) with the command master holding the chip select and then took an illegal-instruction trap (cause 2) in the three 1x1 ACMP groups that read saved state. That is D3's requirement that the erase and program path stay in block RAM; S14 needs it as a linker section.
5. **#791 unchanged.** The cache neither fixes nor worsens the non-power-of-two decode; the `as-built` control with the cache faults at the same call (`0x6880`, cause 1). #791 stays with S3.
6. **Inherited gate finding.** `check_baremetal_only.py --check` fails on S2's `scenario.py:805` comment ("the TX ring filled"), introduced at `cd3525c3` and present at `f8876638`. Not changed here (S2's file and lane); S2's next round or the manager should reword it.
7. **One-phase samples.** In arm A's ACMP groups the AECP retry makes passes 14 to 21 ms with the cache; seven 8x8 ACMP inputs then span two passes instead of one and measure longer than without the cache (their pass bounds rise 5 to 20 ms). Arm B, without the retry, shows the cache's effect alone.
8. **Not done.** The integrated route of the split image (M8a-2); hardware or bench evidence; a data cache measurement (an owner option, a generator path the product patches do not cover). The self-test is still not run by a CI job (S2's open point).

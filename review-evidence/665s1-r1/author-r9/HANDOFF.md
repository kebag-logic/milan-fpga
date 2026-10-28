STATUS: REVIEW READY (merge round 2, executor [A680l]): head `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1`; every gate rc 0

# #665 lane S1 ([A680l]): merge round 2 on PR #795

- Branch `665-s1-faces` (`origin` is `kebag-logic/milan-fpga`), from `dev-soft-core` `e76a755a`. Nothing pushed.
  Four commits on R701-8's `614635b7` (one-line subjects, no body, no trailers):
  - `c6ab3432` merge of `origin/dev-soft-core` `05439833` (parents `614635b7`, `05439833`);
  - `8669b9f4` README: R701-8-W2 as written;
  - `b198a2e1` README: two claims about the cached core;
  - `c3ba2b26` the ledgered plan moved to `build.build` (Python idiom gate).
- Assignment: #665 issuecomment-6474448163. TAKEN: issuecomment-6474478339 (text in `TAKEN-COMMENT.md`); REVIEW READY:
  issuecomment-6477269918 (text in `REVIEW-READY-COMMENT.md`). `PR-BODY.md` follows the template; "Relates to #665".
- Review answered: R701-8 (PR #795 issuecomment-6466412104, POSITIVE at `614635b7`), W1 and W2.
- Rulings still in force: 6461128613 (round 8), 6461910715 (option (c)), 6463964028, 6412739248, 6425357821, 6421238472.

## Work list

- [x] 1. Merge `origin/dev-soft-core` `05439833` as a merge commit (no rebase): `c6ab3432`
- [x] 2. R701-8-W1 (`PR-BODY.md`, Known limitations, the `as-built` bullet) and W2 (`8669b9f4`)
- [x] 3. Gates (table below), real harness builds at both points, arm A, one group, cache on: all rc 0
- [x] PR-BODY.md, REVIEW READY (text in `REVIEW-READY-COMMENT.md`)

## The merge (`c6ab3432`)

Since the branch's first merge (`6660a1a0`) the sides changed 11 files in common. Auto-merged: `docs/ARCHITECTURE_HW_SW_SPLIT.md`,
`docs/design/SPLIT_CONTROL_MEMORY.md`, `docs/reference/FR_NFR.md`, `sw/firmware/ctrl/test/ctrl_configs.py`,
`sw/litex/milan_soc.py`, `tb/verilator/ctrl_service_budget/run.py`. Conflicted and resolved (both sides kept):

| File:line at `c6ab3432` | Conflict | Resolution and reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/build.py:560-561` | the `split_soc.build` call: S1's `ledgered_point(shape, n_if)` vs S2c's `rom_elf`, `core.cpu_regions`, `core.fetch_l1` | all of them (S1's ledgered point at S2c's XIP-aware rom image; the planner's override checks symbols the relink keeps) |
| `split_soc.py:423-441` | signature/docstring: `ledgered` vs `fetch_l1` | both; `ledgered_plan` kept |
| `selftest.py:754-917` | S1 `build_checks` vs S2c `cache_checks`, `cache_build_checks`; `checks()` list | all three; S2c's stub `soc.build` given S1's extra parameter |
| `selftest_mutants.py:464-487` | S1's two `build:` mutants vs S2c's eight | all ten |
| `README.md:223-242` | Results opening: S1's firmware provenance vs S2c's cacheless commands | both; provenance extended to "The instruction cache" (no firmware source changed on dev-soft-core since `e76a755a`: `git diff --stat e76a755a 05439833 -- sw/firmware hdl sw/mailbox` is `ctrl_configs.py` and a README line) and to `:52` |
| `README.md` self-test list, mutant table | appended rows on both sides | all rows |

Checks (`receipts/merge-checks.txt`, `receipts/merge-combined-diff.txt`): files differing from `614635b7` are exactly
`6660a1a0..05439833`'s 21; from `05439833` exactly `6660a1a0..614635b7`'s 66; every one-sided file equals its side.
The harness self-test after the resolution: 97 PASS, 76 mutants caught (91/68 + S2c's 6/8).

## Changes after the merge

| File:line at `c3ba2b26` | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_budget/README.md:994` (`8669b9f4`) | R701-8-W2's exact text: the `lw` at 0x24; the trap line's last field is the last committed PC, the `bgeu` before it | R701-8-W2 |
| `README.md:850-851` (`b198a2e1`) | after S2c's "cached CPU takes ... cause 1, at the same call (`0x6880`)": at this head the cached CPU is caught with cause 5 at the start code's first `.data` copy load | S2c's line is the firmware of `e76a755a`; measured at this head, `runs/C-asbuilt-split` |
| `README.md:1033-1034` (`b198a2e1`) | "On this core it measures the same" -> "On the cacheless core ..."; "That comparison has not been run on the split's cache." | the default core is now the cache; the comparison was A680j's, cacheless |
| `build.py:560-561` (`c3ba2b26`) | `with split_soc.ledgered_plan(ledgered_point(shape, n_if)): spec = split_soc.build(... core.fetch_l1)` | merged `split_soc.build` had 7 parameters; `check_py_idiom.py` failed "FAIL: too many parameters 8 > ratchet 7" in the first docs-gates run, at `b198a2e1` (that log was overwritten by the rerun at `c3ba2b26`; `receipts/gates/idiom-params-by-revision.txt`, the gate's own `scan` per revision, shows `split_soc.py:432` "build takes 7" at `c6ab3432` and none at either parent or at `c3ba2b26`) |
| `split_soc.py:423-433`, `:459` | `split_soc.build` back to S2c's six parameters; `add_ctrl_memory` unwrapped; `ledgered_plan` docstring says `build.build` applies it | same; `ctrl_memory.plan`'s one call in the flow is `add_ctrl_memory` (`milan_soc.py:2807`) |
| `selftest.py:849-857` | S2c's stub `split_soc` back to six parameters, plus `ledgered_plan` returning a null context; docstring | the stub stands in for the module `build.build` now calls twice |
| `build.py:137` | comment: the SoC plan is `split_soc.ledgered_plan` | accuracy |

No new check or planted mutant: the change is a call-site move; the real 8x8 build is its test (57.5 ledgered, tables
byte-identical before and after: `runs/A8-8669b9f4` vs `runs/A8`).

## Gate table

Head `c3ba2b2647aee7fdfe220cac6634827cf5a47ec1` for every row (each receipt's `.head` or first line names it, `DIRTY 0`),
except where a row says otherwise. Units on this session's CPUs 0-15 (no free range: `cpu_ranges.py show` gave none).

| Gate | Result | Receipt (`receipts/`) |
|---|---|---|
| real harness build, arm A, `aecp`, 1x1/1if, split cache (`run.py --point 1x1 --groups aecp --record-budget-findings`) | rc 0, 174 s: 25 of 25, 0 refusals, 0 T_svc misses; `soc.json` `fetch_l1 split` `[64, 1]`, netlist `VexiiRiscvLitex_2c4bb987...` (S2c's), plan 37.0, no ledgered name; ELF `fe939fff...` (= the linked image) | `runs/A1` |
| the same, 8x8/2if | rc 0, 300 s: 39 of 39, 0 refusals, 0 misses; plan 57.5, `ledgered: 8x8-two-interfaces`; ELF `654921b6...`; PINMISSING only the CPU's `dma_bus_awregion`/`arregion` (no mailbox pin) | `runs/A8` |
| both at `8669b9f4` (before `c3ba2b26`) | the same verdicts; `table.md` byte-identical to `c3ba2b26`'s at each point | `runs/A1-8669b9f4`, `runs/A8-8669b9f4` |
| comparison with S2c's cached runs (`665s2c-a685` `P1-64x1`, `P8-64x1`) and this lane's cacheless runs (`665s1-a680j` `A1`, `A8`) | 1x1: +0.042 to +0.358 ms vs S2c (this lane's face commits), -0.751 to -2.791 ms vs cacheless; 8x8: -1.801 to +1.562 vs S2c (phase), -1.203 to -5.424 vs cacheless | `compare/*.md` |
| the `as-built` control, 1x1, cacheless (`--fetch-l1 none --cpu-regions as-built`) | rc 0: `TRAP 166 0 5 00000020` x3, `CONTROL as-built caught` | `runs/C-asbuilt-none` |
| the `as-built` control, 1x1, split cache (`--cpu-regions as-built`) | rc 0: `TRAP 195 0 5 00000020` x3, `CONTROL as-built caught` (S2c's README said cause 1 at 0x6880 on its firmware) | `runs/C-asbuilt-split` |
| harness self-test `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | rc 0: 97 PASS, 76 MUTANT caught, 0 ESCAPED, `self-test: 0 failures` | `gates/harness-selftest.txt` |
| `sw/litex/test_ctrl_memory.py` (LiteX's interpreter) | rc 0, 0 failures; the default `add_ctrl_memory` refuses the ledgered image (`:48`) | `gates/test-ctrl-memory.txt` |
| `sw/builder/test_soc_options.py` (LiteX's interpreter; S2c's file, `milan_soc.py` merged) | rc 0: "the 4 KiB direct-mapped instruction cache on the split CPU only, 6 killed controls", RESULT: PASS | `gates/test-soc-options.txt` |
| docs workflow, 69 commands (`probes/docs_gates.sh`: `check_em_dash.py --base`, `check_py_idiom.py`, `check_cpp_idiom.py`, `check_baremetal_only.py --check`/`--selftest`, ...) | 69 of 69 rc 0, 275 s. First run at `b198a2e1`: 68 of 69, `check_py_idiom.py` "FAIL: too many parameters 8 > ratchet 7", fixed by `c3ba2b26` | `gates/docs-gates.txt`, `gates/idiom-params-by-revision.txt` |
| docs CI self-tests (`probes/docs_ci_selftests.sh`, 16; `ci_gate_workflows_selftest.py` runs S2c's `ci_fast_tool_selftest.py`) | 16 of 16 rc 0 | `gates/docs-ci-selftests-summary.txt` (full log by size and sha256) |
| `cd tests && behave --no-capture -f plain` | rc 0: 14 features, 406 scenarios, 1,977 steps | `gates/behave.txt` |
| rtl-fast `firmware-boundary` steps (`probes/boundary_unit.sh`: SDK self-test, the pinned archive into a new destination and verified, `ctrl_boundary.py --require-rv32 --selftest --without verilator`) | rc 0, 1,466 s: `ctrl_boundary: PASS`, 2,864 compiled sources of 3,094 invocations (as before); 0 changed paths after | `gates/firmware-boundary.txt` |
| `ctrl_boundary.py --require-rv32 --selftest --only verilator` (pinned Verilator 5.050 first on PATH) | rc 0, 1,006 s: PASS, 775 of 885 (as before) | `gates/ctrl-boundary-only-verilator.txt` |
| `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard k/4`, four units | rc 0 each (478, 1,584, 670, 1,009 s); `[ok]` 61, 528, 137, 280 (as before) | `fw/shard-*.txt` |
| `fw_coverage.py --check --jobs 4` | rc 0, 307 s: PASS, 31 files at 100 % lines and branches | `gates/fw-coverage-check.txt` |
| `test_ctrl_nvm.py --require-rv32 --jobs 4` | rc 0, 125 s: OK across 5 shapes, 435 tests | `gates/test-ctrl-nvm.txt` |
| `test_builder.py --require-rv32` (without `MILAN_RV32_CC`) | rc 0, 2,161 s: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11: no local Arty build report, as before) | `gates/test-builder.txt` |
| `gen_mailbox.py --check` | rc 0, 0 findings | `gates/gen-mailbox-check.txt` |
| linked images, four points (`probes/images_unit.sh`, `image_points.sh ... ledgered`, `-fno-stack-protector` runtime) | rc 0: 37.0, 40.5, 50.5 within 56; 8x8/2if 57.5 with `--ledgered-point`, refused without (rc 2); the override refused on the other three (rc 2). ELFs byte-identical to rounds 6-8 (`fe939fff`, `18c5055b`, `d92a7f96`, `654921b6`) | `images/` |
| four-shard Verilator sweep (`native-shards.py`, pinned Verilator 5.050 and sv2v 0.0.12, CPUs 0-3, 4-7, 8-11, 12-15) | rc 0 each (5,672, 4,653, 5,632, 4,107 s, on 4 CPUs each, beside the other gates): shards 0 to 3 pass 15, 17, 16 and 16 suites (64 of 64), 250,913 + 1,536,446 + 380,086 + 23,679 = 2,191,124 checks, 0 in-suite failures, 0 timed out; declared skips only `tsn_fuzz`'s two field campaigns (tsn-gen absent). Suites and checks equal `614635b7`'s | `sweep/sweep-c3ba2b26/` |

Not run this round, receipts stand (neither merge nor this round changes a file they read): `aecp_arms.py`,
`aecp_mutants.py` (`424b1489`), `gen_mailbox.py --check --crosscheck`/`--selftest`, the census, `lint_rtl.py`,
`KL_mbx` OOC (rounds 4-5; no `hdl/`, `sw/mailbox/`, `syn/` or generated file changes). Not run again although the
merge changes the harness they run in (S2c's fetch-L1 selection and observers, `build.py`, `sim_main.cpp`): arm B
legs and `slow-adp-rx` (cacheless figures from `0eda061a`; S2c recorded S2's cacheless figures again with
`--fetch-l1 none`, and at this head the cacheless `as-built` control's trap lines equal round 8's).
`slow-adp-shutdown` has never run at this lane's heads. Not run at all: arm B and the controls
`slow-adp-*` on the split's cache; the one-cycle acknowledgement comparison on the cache (a scratch worktree for the
plant was refused by the permission mode, so the README now limits that claim to the cacheless core). No Vivado.

## Process notes

- Scratch: `$VALIDATION_STORAGE/scratch/665s1-a680l-work/` (builds, logs, tmp, sweep, SDK destination `sdk`, PR body
  generator `pr/edit.py`). Sweep clones `$LANES/665s1-a680l-shard{0..3}` (made by `native-shards.py`).
- Units: each gate in its own transient unit (`probes/unit.sh`, `unit_bg.sh`), MemoryMax 2-8 G; legs peaked about
  1.3 G, the sweep's four shards about 4 G together. MemAvailable fell to about 20 GB during the sweep from another
  lane's unit (16 GB); nothing was started then.
- `probes/`: `env.sh`, `leg.sh`, `unit.sh`, `unit_bg.sh`, `gate_unit.sh`, `run_gate.sh`, `docs_unit.sh`,
  `docs_gates.sh`, `docs_ci_unit.sh`, `docs_ci_selftests.sh`, `boundary_unit.sh`, `firmware_boundary.sh`,
  `behave_unit.sh`, `images_unit.sh`, `image_points.sh`, `compare_rows.py`, `idiom_params_probe.py`,
  `collect_receipts.py` (receipts index; host paths replaced; files over 200 KB in `receipts/large-files.txt`).

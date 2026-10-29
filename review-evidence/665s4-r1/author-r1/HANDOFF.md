# [A698] #665 Mark II split, lane S4: the F1 flash and saved-state ports on the target

STATUS: STOP (decision needed: the capture bound). Everything else in the scope is done and passes at both points.

- Checkout `$LANES/665-s4-f1-target`, local branch `s4-f1-target`. The assignment names `665-s4-f1-target`; the worktree's branch was created as `s4-f1-target` before this session and is not renamed.
- Base `origin/dev-soft-core` `f4c9ad4f06f185378fd2646298aab51dd108e86f`. `origin` is `https://github.com/kebag-logic/milan-fpga.git`, and HEAD equalled the base at the start.
- Head `9c2f12a80494b9ee95441ca7f9c606ee6cfe617f`: five commits on the base. The fifth (Python idiom: two docstrings and four line wraps) follows `19d79844`, where the long gates ran. Nothing is pushed.
- Assignment: [A10] issuecomment-6493622258 on #665, and section S4 of the plan (`665-a678/PLAN.md`).
- TAKEN: issuecomment-6493949387. STOP: issuecomment-6500265323 (`STOP-COMMENT.md`), posted with head `9c2f12a8`.
- Parallel lanes: S2b (`665-s2b-cycles`) and S3 (`665-s3-platform`). Shared files are listed below.

## The finding that stops the lane

The capture misses the 24.5 ms bound at both points, by any reading of "the capture".

| Point | Records, container | Capture, CPU cycles | ms | Fixed cost per step | Cost per payload byte | Idle step |
|---|---|---:|---:|---:|---:|---:|
| 1x1 | 54, 3,336 B | 1,361,143 | 27.223 | 11,062 | 263.7 | 9,486 |
| 8x8 | 164, 13,256 B | 5,161,328 | 103.227 | 16,500 | 205.5 | 9,389 |

- Every record is dirty, and each is latched from its real owner. The fixed and per-byte costs are the least-squares line through the latch steps.
- At 8x8 the payload bytes alone, 11,898 B, cost 48.9 ms: twice the bound, even with no fixed cost.
- The shipping writer copies 13,210 B in 13.86 ms.
- Every step is within T_svc. The longest is 2.639 ms at 8x8, a capture step; at 1x1 it is 2.022 ms, a page program.
- Options and the recommendation (a) are in `STOP-COMMENT.md`.

## Scope as interpreted (TAKEN-COMMENT.md)

- **The flash port's map** is generated from the split SoC's `csr.csv`, with the field offsets from the same export's LiteX `csr.h`.
- **The state port** stays bound to the owners the image composes: `acmp_nvm` over `aecp_nvm`. It is proven on the target CPU.
- **The guard** is bound to the SoC's journal. It is checked against the record-space slot geometry and every image slot, and proven on the target.
- **The capture** is the store's capture phase for a full work set: Σ CPU cycles, graded against 24.5 ms. Each step is graded against T_svc.

## Changes (file:line, reason), at `19d79844` (the fifth commit moves `target_grade.py` and `target_cases.py` lines by one or two)

| Where | What, and why |
|---|---|
| `sw/firmware/ctrl_nvm/plat/gen_flash_port.py:1-58` (new) | **The generator** reads a split SoC export and writes the port's `generated/csr.h`, `generated/mem.h` and `flash_port.json`, so the port never compiles against a hand-written address (S4 scope item 1). |
| `gen_flash_port.py:174-310` | **The eight rules**: data width, registers, header, fields, flash window, journal, slots, clock. The journal rule (`:256`) and the slots rule (`:286`) are the region guard's static half (S4 scope item 3). |
| `gen_flash_port.py:327-363` | **The headers it writes.** The accessors cast through `uintptr_t`. |
| `gen_flash_port.py:383-612` | **The self-test**: 33 checks, each planted defect refused by its own rule and by no other. |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:55-64` | `flash_port()` puts `--flash-map` ahead of the RV32 stand-ins, and refuses a map whose clock is not the shape's: `timer0` counts the SoC's clock. |
| `ctrl_srp_image.py:66-82`, `:121-124`, `:143-144`, `:153-154`, `:160-161` | `--nvm-source` lets a planted copy of the store be built. Both options default to today's behaviour. `--flash-map` without `--with-aecp` is refused. |
| `tb/verilator/ctrl_service_budget/build.py:110-153` | `Plant`, `Variant` and `label` let a client pass its own planted defect or arm. |
| `build.py:156-183` | `mutated_source` copies the tree the plant names (`ctrl` or `ctrl_nvm`) and returns the image's option for it. |
| `build.py:187-214` | `firmware()` takes `flash_map`. |
| `build.py:217-256` | `soc_export`, `port_map` and `flash_map` export the split SoC with the point's one-interface image, generate the map, and export again with the image linked against the map. Two different maps are refused. |
| `build.py:469-510` | `SPAN_SYMBOLS`, `CALL_SYMBOLS`, `traced` and `trace_lines` generate the testbench's trace tables. A static function is resolved by its module. |
| `build.py:546-547` | The journal's bounds go into `budget_config.hpp`. |
| `build.py:661-668` | The flash map's files are attested inputs. |
| `build.py:692`, `:701` | `build()` makes and records the map. |
| `tb/verilator/ctrl_service_budget/split_soc.py:55`, `:76-111` | `FLASH_MAP`, `fixture_addresses(flash_map)` and `map_deviations` read the device addresses from the map and compare the test SoC's own `csr.csv` with it. |
| `split_soc.py:331-347` | `FlashBoundary` holds the PHY's two CSRs, so the bank is laid out as the split SoC's. |
| `split_soc.py:353-376` | `add_devices` builds `add_spi_flash`'s LiteSPI in the split SoC's `spiflash` and `timer0` banks. |
| `split_soc.py:477-479` | The build is refused on a deviation. |
| `tb/verilator/ctrl_service_budget/sim_main.cpp:84`, `:151-156` | Journal preload and dump (`BUDGET_JOURNAL_IN` and `_OUT`). |
| `sim_main.cpp:264`, `:326-341`, `:519-520` | Passive SPAN and CALL tracing (`trace_commit`). |
| `tb/verilator/ctrl_service_budget/grade.py:95`, `:158-160` | The parser accepts SPAN and CALL lines into `Log.traced` and grades nothing from them. |
| `tb/verilator/ctrl_service_budget/selftest.py:708-743`, `:860-868` | The reuse checks gain the flash map's files and "reuse refuses the flash port's map". The build stub gains `flash_map`. |
| `tb/verilator/ctrl_service_budget/README.md` | The test SoC's devices and address table, the traced lines, finding 2 and the limits. |
| `tb/verilator/nvm_split_target/target_cases.py` (new) | **The cases**: the two arms (`capture-all`, `guard-probe`), the three plants, the scripts, and the journals derived by the reference codec. |
| `tb/verilator/nvm_split_target/target_grade.py` (new) | **The grading**: step phases from the traced calls, `capture`, `decomposed`, `fits`, `lengthened`, the apply order, the answers, the guard, the commit, and the per-case verdicts. |
| `tb/verilator/nvm_split_target/run.py` (new) | **The driver**: per-arm builds, the commit first, the other cases in parallel, the bound's control on the measured commit, `--regrade`. |
| `tb/verilator/nvm_split_target/target_selftest.py` (new) | **The portable self-test**: 29 checks and 7 grader mutants. |
| `tb/verilator/nvm_split_target/README.md` (new) | The harness, its rules and the results at both points. |
| `sw/firmware/ctrl/test/ctrl_configs.py:166-169`, `:197-200`, `:209-215` | The boundary gate's OUTSIDE list gains the two new files that name the firmware tree. The two harness reasons are updated. |
| `sw/firmware/ctrl_nvm/README.md` | The generated map, the owners on the split CPU, the measured CPU time (it replaces "CPU time, not measured"), and "What this does not prove". |
| `docs/ARCHITECTURE_HW_SW_SPLIT.md:211-213` | Section 5: F1's ports on the target, and the capture finding. |

No firmware function changed, so the Mark II unit-test rule adds no units. `fw_coverage.py --check` holds the ratchet.

## New checks: planted mutant and failing words

| Check | Planted defect | Failing words |
|---|---|---|
| target `reorder-settle` (1x1 and 8x8) | `nvm_store.c`: the D3 walk's test before the first name is removed (`if (0 && ...)`) | 1x1: `apply order: entry 4 is aecp_value_restore, the container needs aecp_restore_settle (44 entries, 44 wanted)`; 8x8: entry 25 of 133 |
| target `reorder-bindings` | `nvm_store.c`: the binding walk runs after the D3 walk | `apply order: entry 0 is aecp_map_restore, the container needs acmp_restore_binding` |
| target `guard-removed` | `nvm_flash_litespi.c` `ls_in_journal` returns 1; `guard-probe` arm | `flash write escaped the journal` (the flash model) |
| target `capture-one-page-past` | the measured capture lengthened to exactly the bound, then one page of its own cost past it | 1x1: `at the bound 24.5000 ms fits; one page (104,453 cycles) past it, 26.5891 ms, is over`; 8x8: 99,676 cycles, 26.4935 ms |
| `gen_flash_port.py --self-test` | 17 planted exports, 6 doctored reserved journals and a published image over the journal, each refused by its named rule and by no other | for example `REFUSED registers: spiflash_master_cs is in csr.csv more than once` |
| `nvm_split_target` self-test mutants (7) | strictly below the bound; the bound as the whole floor; the closing step dropped; the page not added; settle last regardless; only the first entry compared; any sequence_id | each names the check that fails, for example `a capture at exactly its bound fits` |
| harness self-test | the flash map's `flash_port.json` changed after a build | `reuse refuses the flash port's map` |

## Measurements, at `19d79844`

- The capture: the table above.
- The commit's phases, longest step in ms at 1x1 and 8x8:
  - capture: 0.815 and 2.639;
  - seal: 0.688 and 0.697;
  - erase: 0.248 and 0.252;
  - poll: 0.237 and 0.246;
  - program: 2.022 and 2.032;
  - read: 1.907 and 1.920;
  - idle: 0.200 and 0.207.
- The commit: one erase, and 14 or 52 pages.
- `nvm_store_boot`, CPU cycles (ms):
  - 1x1: valid 5,027,209 (100.5), absent 506,631 (10.1), torn 8,255,898 (165.1), version 504,698 (10.1);
  - 8x8: valid 24,423,878 (488.5), absent 1,746,898 (34.9), torn 37,255,159 (745.1), version 1,744,933 (34.9).
- The stage against the ledger: `nvm_stage` is 3,344 B and 13,264 B. The plans are 37.0 tiles at 1x1 and 57.5 at 8x8 with two interfaces. Both equal `SPLIT_CONTROL_MEMORY.md` section 5; the map moves no planned byte.
- The S2 harness at 1x1 on the generated map: `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`.

## Gates

The runner is `scripts/gates_s4.py`: one log per gate, the tree checked clean before and after each. Receipts are in `receipts/gates-9c2f12a8/` and `receipts/gates-19d79844/`, with their `summary.md`.

| Gate set | Head | Result |
|---|---|---|
| 99 gates: the docs workflow's check-mode commands, the bare-metal scope gate, the idiom, naming, evidence and hygiene gates, `git diff --check`, behave (406 scenarios), `hdl_reference`, `firmware_compiler_absent`, the generator, target and harness self-tests, and rtl-fast's `firmware-boundary` in both modes | `9c2f12a8` | `0 of 99 gates nonzero or left the tree dirty` |
| `builder_require_rv32` | `19d79844` | rc 0, `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11's calibration report, which needs a vendor build tree, as in earlier lanes) |
| `ctrl_nvm`: `test_ctrl_nvm.py --require-rv32 --self-test` | `19d79844` | rc 0, `OK across 5 shape(s), 435 tests, and all 109 planted defects reddened` |
| `ctrl_firmware`: `test_ctrl_firmware.py --require-rv32 --self-test` (the control, ACMP, MAAP, AECP and SRP campaigns) | `19d79844` | rc 0, 1,006 `[ok]` plants, none escaped |
| `fw_coverage.py --selftest` and `--check` | `19d79844` | rc 0, 100 % lines and branches |
| `nvm_cosim`: `make` and `make lint` | `19d79844` | rc 0, `465 checks: 465 PASS`, `39 of 39 mutant(s) killed by their named check` |
| `publication_census`, `ctrl_memory` | `19d79844` | rc 0 |
| the first run's `firmware_compiler_absent` and `py_idiom` | `19d79844` | rc 1: the runner's scratch directory was missing (an invocation error), and the idiom finding the fifth commit fixes. Both rc 0 at `9c2f12a8`. |

The nine gates run only at `19d79844` read none of the files the fifth commit changes: two docstrings in `gen_flash_port.py`'s self-test helpers, and line wraps in three `nvm_split_target` modules (`receipts/scope/diff-19d79844-to-head.patch`).

| Run | Head | Result |
|---|---|---|
| `nvm_split_target/run.py --point 1x1` and `--point 8x8` | `9c2f12a8`, and `19d79844` before it, identical | `RC=1` at each point, on the commit's capture bound alone; every other case passes and every control is caught (`receipts/target-*`) |
| `ctrl_service_budget/run.py --point 1x1` | `19d79844` | `18 groups graded, 0 refusals, 34 T_svc misses (34 of 141 probe instances, 13 of 81 paths)`, `RC=0` |
| `ctrl_service_budget/run.py --point 8x8` | `19d79844` | `17 groups graded, 0 refusals, 62 T_svc misses (62 of 182 probe instances, 30 of 129 paths)`, `RC=0` |
| `nvm_capture_cpu/run.py`, 8x8 at 50 MHz, 16 captures, traffic on and off | `19d79844` | `RC=0` each; 13.848 to 13.863 ms, and 13.675 to 13.690 ms |
| `nvm_capture_cpu` controls `skip-copy` and `no-traffic`, 1x1 | `19d79844` | `RC=0`, each `caught by destination-byte or concurrent-traffic oracle` |

Environments, outside the checkout and the output directory:

- the product LiteX venv and the pinned RV32 SDK (`LITEX_ENV_CC_TRIPLE`, `COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`, `PYTHONHASHSEED=0`);
- the pinned Markdown renderer's venv;
- a scratch venv with `tools/hdl_reference/requirements.txt` (hash-pinned);
- a scratch venv with behave, as CI installs it;
- for `nvm_capture_cpu`, a scratch `bin` holding only a link to the system `meson`, ahead of the SDK's `meson` shim, which cannot import `mesonbuild` under the venv's Python.

Not run: the four-shard full sweep (no RTL change), Vivado (no route needed), and the 1x1 and 100 MHz arms of `nvm_capture_cpu`, whose firmware and harness are unchanged.

Observation, not this lane's: `tb/verilator/nvm_cosim/README.md` says 469 checks; the suite prints 465 at this head.

## Shared files touched

- `sw/firmware/ctrl/test/ctrl_srp_image.py` (S2b also edits).
- `sw/firmware/ctrl/test/ctrl_configs.py` (S2b also edits).
- The S2 harness: `build.py`, `split_soc.py`, `selftest.py` and `README.md`, all of which S2b also edits (the expected conflicts are in `fixture_addresses` and `add_devices`). This lane alone edits `sim_main.cpp` and `grade.py`.
- `docs/ARCHITECTURE_HW_SW_SPLIT.md` section 5, one line.

## Open questions and assumptions

- The capture bound: decision requested (STOP).
- "The journal region that `check_nvm_record_space.py` names": the record-space check names the slot geometry (check 5). The offset is `milan_soc.py`'s `FLASHBOOT_RESERVED` journal, which the SoC publishes in `csr.csv`.
- The product split SoC export needs the builder's own ignored outputs (`sw/builder/out/<cfg>`, `configs/generated/<cfg>`), as `test_ctrl_memory.py` does.

[A594]

## Contents

- **[Status](#status)** -- M8a-1 review-ready; gates; `640-m8a` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- The split placement's memory map and block RAM, the fit at four points, the ledger, the controls.
- **[Authoritative references](#authoritative-references)** -- Rulings, plan sections and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and their expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What waits for M8a-2, and the open risks.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

REVIEW READY for M8a-1, head `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14` (four commits on `dev` `e8454e27`). `640-m8a` -> `dev`.

Every gate the change touches passes locally; the gate table is below. M8a-2 (boot, service checks, route) follows F-INT PR 2.

## Linked Issue / roles

Relates to #640

Executor: `[A594]`
Internal cleared-context reviewer: `[R606]`
External reviewer: `[R607]`

Assignment: #640 comment 6100371426. Round-1 STOP: #640 comment 6101473717. Ruling: #640 comment 6101485877 (this PR is its step M8a-1).

## Description

In the split placement (`--ctrl-mailbox`) the control firmware now owns the CPU's reset entry and runs from block RAM sized from its own linked image. No BIOS ROM or BIOS SRAM is built there. The all-fabric default is digest-identical.

| Piece | What it does |
|---|---|
| `sw/litex/ctrl_memory.py` | The one statement of the split map: `rom` at the reset address `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB; the bank plan; the named refusals `reset entry`, `memory map`, `memory-map overlap`, `allocation over budget` (56 RAMB36) and `staging buffer` |
| `sw/litex/milan_soc.py` | `CtrlMemory` builds a region from power-of-two banks of RAMB18 granules, largest first, each a LiteX `wishbone.SRAM`, and answers `err` past the last bank. `add_ctrl_memory` builds `rom` (initialised) and `sram` from `--ctrl-firmware`. Under `--ctrl-mailbox` no BIOS ROM or SRAM is built and no BIOS is compiled |
| `sw/firmware/ctrl/plat/ctrl_split.ld`, `ctrl_split_start.S` | The split link and the reset entry: stack, `.data` copied from `rom`, `.bss` cleared, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` | `--layout split` links the full F0-F5/F1 composition into that map and reports the bank plan; the flat layout is unchanged |
| `sw/litex/test_ctrl_memory.py` | 33 checks: banks against an independent oracle, the refusals on ELFs from an independent writer, the three planted controls, the real `CtrlMemory` in simulation with planted defects, a probe linked through the real script |
| `syn/ooc/ctrl_memory_ooc.py` | Emits both regions of each image as the SoC builds them, and the out-of-context Vivado script |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | The split placement's memory contract, refusals, boot console and diagnostics, and fit |

**Linked spans** (`ctrl_srp_image.py --with-aecp --layout split`, pinned RV32 SDK, 8 KiB stack), bytes:

| Point | `rom` need | `sram` need | Sum | Flat span (unchanged) |
|---|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 95,032 | 45,520 | 140,552 | 140,400 |
| 1x1, two interfaces | 96,320 | 56,880 | 153,200 | 153,056 |
| 8x8, one interface | 108,680 | 86,080 | 194,760 | 194,224 |
| 8x8, two interfaces (largest) | 110,056 | 112,208 | 222,264 | 221,728 |

The split adds the reset entry (88 B), the second copy of `.data` and alignment. The spans hold the descriptor image (7,512 / 19,520 B), the shape's `nvm_stage` (3,344 / 13,264 B) and the lwSRP pool.

**Block RAM as mapped** (`syn/ooc/ctrl_memory_ooc.py`: Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`, out of context):

| Point | Planned RAMB36 equivalents | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT / FF | Byte floor |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 35.0 | 33 / 2 | 34.0 | 212 / 32 | 35 |
| 1x1, two interfaces | 38.0 | 37 / 1 | 37.5 | 89 / 7 | 38 |
| 8x8, one interface | 48.5 | 46 / 2 | 47.0 | 307 / 33 | 48 |
| 8x8, two interfaces (largest) | 54.5 | 52 / 2 | 53.0 | 328 / 40 | 55 |

- **Planned:** every bank in block RAM.
- **Byte floor:** the flat linked span at 4,096 B per RAMB36, rounded up.
- **Budget:** every point is within 56 RAMB36.
- **`sram`:** maps exactly as planned.
- **`rom`:** maps below plan. Vivado trims ROM bit columns that are constant across a bank, and puts one small or sparse ROM bank in logic: 231 of the largest point's 328 LUTs.

Before, the base BIOS ROM took 16 RAMB36 and its SRAM 2. One LiteX SRAM of the largest image took 64 RAMB36 (round 1).

**Ledger** (`MARK_II_AREA_PLAN.md`, mirrored in `AREA_BUDGET.md`):

- the BIOS ROM and SRAM are not built: -18 RAMB36, 0 RAMB18, measured at `e8454e27`;
- the firmware allocation as mapped at 8x8 with two interfaces: +52 RAMB36, +2 RAMB18, +53 tiles;
- totals: `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`, then 113 after the split's conditional release (8.5 below 121.5, reserve untouched);
- with every bank in block RAM: 125.5 and 114.5.

**Planted controls, through the real SoC build** (each refused before any export):

- allocation over budget: the largest image with a 16 KiB stack, `allocation over budget: 56.5 RAMB36 ... exceeds the 56-RAMB36 budget`;
- memory-map overlap: `.bss` linked at `.data`'s address (GNU ld accepts it), `memory-map overlap: .bss at 0x10000000 lies inside .data [0x10000000, 0x10000038)`;
- staging buffer for another shape: the 1x1 image in an 8x8 build, `staging buffer: nvm_stage is 3344 bytes; the endstation_ax7101_8x8 shape stages 13264`.

**Boot console and diagnostics.** The split image loses the LiteX BIOS and its console, the BIOS DDR3 initialisation and the shipping firmware's UART commands. It keeps the UART, `timer0`, `ctrl`, the identifier memory, the `ppmem` observer and every Milan CSR. Its CSR map equals the base `--ctrl-mailbox` export's; only the `rom` and `sram` region sizes differ.

**DDR3 at this base.** `KL_pp_shadow` is still instantiated, so DDR3 stays under `--ctrl-mailbox`. With no BIOS, `pp_mem_gate` never opens and the processor's three memory masters stay refused, as before training. F-INT PR 2 removes the wrapper; M8a-2 routes the split without DDR3.

**All-fabric default.** Both AX7101 shipping exports, base `milan_soc.py` against head: 22 files each, 0 differ after normalizing timestamps, the export directory and LiteX's comment-only hierarchy tree. Normalized `alinx_ax7101.v`: `40e5304a...` (1x1) and `fea8757e...` (8x8), equal at base and head.

## Authoritative references

- #640 ruling 6101485877: 224 KB binding, up to 56 RAMB36 as mapped; conditional release; no power-of-two waste; firmware owns the reset entry; M8a-1 and M8a-2.
- #640 assignment 6100371426; owner decisions 5991591637 (D4) and 6081706413 (224 KB).
- `docs/design/MARK_II_AREA_PLAN.md`: L11 The SoC side; Firmware and block RAM ledger.
- `docs/design/AREA_BUDGET.md`: the memory ledger mirror.
- `docs/design/MAILBOX_SPLIT.md`: Default build (the `--ctrl-mailbox` switch).
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the export recipe used for the digest proof.

## How to get into the same state

```sh
git fetch origin
git switch 640-m8a
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
```

`$SDK` is the pinned RV32 SDK directory; `MILAN_RV32_CC` may name its `riscv32-linux-gcc`.

## How to validate

```sh
python3 sw/litex/test_ctrl_memory.py
scripts/run_litex_sims.sh "$LOGS"
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" \
  --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$RUNTIME"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
```

Expected result / pass criteria:

- `test_ctrl_memory: 0 failure(s)` and `RESULT: PASS` (with an RV32 compiler); the aggregate passes 6 of 6;
- the plan prints 54.5 RAMB36 for the largest point, and `--stage-bytes 3344` refuses it with `staging buffer`;
- `ctrl_memory_ooc.tsv` lists `s8i2_rom` 25 / 1 and `s8i2_sram` 27 / 1 (RAMB36 / RAMB18);
- a shipping export with `--ctrl-mailbox --ctrl-firmware "$OUT/ctrl_app.elf"` elaborates with no BIOS; the default export is digest-identical to `dev`.

Local gate results (each unpiped, rc 0 unless stated):

| Gate | Head | Result |
|---|---|---|
| `test_ctrl_memory.py`; `run_litex_sims.sh --selftest` and the aggregate | `a475ab5a` | 33 checks PASS; 6 of 6 PASS |
| `check_py_idiom.py` (CPython 3.12.3) and `--selftest`; hygiene, TODO, fail-fast and test-evidence ratchets | `a475ab5a` | PASS |
| `docs_check.py`, `check_em_dash.py --base e8454e27`, `gen_toc.py --verify-anchors`/`--check`, `check_doc_paths.py`, `check_doc_style.py`, `ci_events.py --check` | `5d532e9d` | PASS |
| `test_builder.py --require-elaboration --require-rv32` | `c20ed894` and `a475ab5a` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a bench build tree; recorded reason) |
| `check_soc_sources.py`, `iob_pack_selftest.py`, sweep/deploy/entity shape self-tests, the `syn/ooc` self-tests | `c20ed894` | PASS |
| `ctrl_image_selftest.py --require-rv32`; `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `c20ed894` | PASS |
| `scripts/run_all_suites.sh` | `94190c36` | 61 of 61 suites, 2,185,848 checks, 0 failures (4 declared `tsn_fuzz` skips: tsn-gen absent) |
| `syn/yosys/run.sh` | `94190c36` | 58 of 58 tops PASS |
| Default exports, base vs head, both AX7101 configs | head `milan_soc.py` | 22 files each, 0 differ |
| Planted controls through the SoC build | head `milan_soc.py` | each refused by name (rc 1, expected) |
| Out-of-context mapping | images of `94190c36` | Vivado rc 0; table above |

`94190c36` to `5d532e9d` is documentation only. `c20ed894` to `94190c36` adds two docstrings.

## Known limitations / out of scope

- M8a-2, after F-INT PR 2: the split-image simulation boot to the control application's ready state, `check_nvm_capture.py` 8x8, `nvm_cosim`, `nvm_capture_cpu`, and the integrated route through the M0s recipe against its split figure (LUT, FF, RAMB deltas; WNS).
- The image linked here is the size fixture in the split layout; the reset entry is checked by layout, not by a CPU simulation.
- The bank decode sits on the CPU bus path; its timing is measured only by M8a-2's route.
- Headroom at the largest point is 1.5 RAMB36 (6 KiB); growth beyond it is refused by name.
- The split build uses its own VexiiRiscv netlist, one for both shapes.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (M8a-1 part; M8a-2 follows)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

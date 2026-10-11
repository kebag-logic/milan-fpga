[A594]

## Contents

- **[Status](#status)** -- M8a-1 round 2 review-ready; the head and the dev merge it carries; `640-m8a` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Round 2](#round-2)** -- Each R606-1 and R607-1 finding and the change that answers it.
- **[Description](#description)** -- The split placement's memory map and block RAM, the rules, the fit at four points, the ledger.
- **[Authoritative references](#authoritative-references)** -- Rulings, plan sections and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands, their expected results and the gate table.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What waits for M8a-2, and the open risks.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

REVIEW READY for M8a-1 round 2, head `76605880a20005cbc2acad1b23ba2ccebde64ca8`. `640-m8a` -> `dev`.

- Round 2 adds three commits on `08b90b6859b0a7d7f172c7ae29745248895d9aa9`: `be431eec` (code, test, rule table), `516d7fb8` (ledger and fit docs) and `76605880` (one sentence of the rule section).
- `08b90b68` is the round-1 head `5d532e9d` plus a merge of dev `ac2c5e77` (M2, PR #710). That merge conflicted only in `docs/testing/TESTING.md` and kept both suite paragraphs.
- The LiteX aggregate passes 7 of 7 at the head (M2's `test_retained_cdc_storage` arrived with the merge).

Every gate the change touches passes locally; the gate table is below. M8a-2 (boot, service checks, route) follows F-INT PR 2.

## Linked Issue / roles

Relates to #640

Executor: `[A594]`
Internal cleared-context reviewer: `[R606]`
External reviewer: `[R607]`

Assignment: #640 comment 6100371426. Round-1 STOP: #640 comment 6101473717. Ruling: #640 comment 6101485877 (this PR is its step M8a-1). Round 2: #640 comment 6105011666, answering R606-1 (#721 comment 6104999232) and R607-1 (#721 comment 6105008317).

## Round 2

| Finding | Change |
|---|---|
| R606-1-F1: writable initialised data running in `rom` accepted | New rule `writable in rom` under `memory map`; unit arm, and the link plant `} > sram AT > rom` to `} > rom` |
| R606-1-F2, R607-1-F1: the hole graded at one address; five of twelve mutants survive | The simulation runs at the largest image's sram banks (64, 32, 8, 4 and 2 KiB) in both regions. It samples 47 addresses past the last bank up to word `0xFFFF`, the 256 KiB window the SoC decodes, so past 224 KiB. Each must answer err alone, and no aliased cell may change. A read presented on the cycle after an err must ack with its own data |
| R607-1-F1: budget boundary and three refusals without an arm | 56.0 RAMB36 accepted and 56.5 refused; arms for a NOBITS section in rom, a shared load address and no bytes at the reset address |
| Round 2 item 1: one list and a standing mutation check | `ctrl_memory.RULES` registers 16 rules; a refusal names its rule. The test requires `SPLIT_CONTROL_MEMORY.md` section 3 to list exactly those rules, and every rule to have a refusal arm and a mutant. 40 mutants each rebuild one function or class from its own source with one edit; each must be killed by a named FAIL |
| R606-1-F3, R607-1-S1: the SoC hookup untested | A SoC arm runs `milan_soc.py`'s own `main()` on the shipping 1x1 config's argv, exporting without Vivado or software. It requires: the three controls refused by rule before any Verilog; both lone flags refused; and the split export holding the image's banks and no BIOS ROM or SRAM, with rom initialised to the image and no BIOS or shipping firmware built. R606-1's `main()`-stage mutant turns it red |
| R607-1-S2 (round 2 item 3): truncated ELF unnamed | Rule `elf truncated` under `memory map`: every header, table, symbol, name and load segment read is bounds-checked |
| R606-1-F4, R607-1-F2: the 56-tile sentences and `AREA_BUDGET.md:382` | 116 tiles, 5.5 below the ceiling, in both ledgers; the ruled limit, up to 56 RAMB36 as mapped, with M8a-1's 53 out of context; the plan's lane row names the ruled 56-tile allocation |
| R606-1-F5: the 231-LUT attribution | 231 LUT cells is the `rom` region: the bank in logic plus the bank decode and read multiplexer. The basis is LUT primitives; `report_utilization` gives 220 Slice LUTs |
| R607-1-F3: this body | It names the round-2 head, `08b90b68` and the dev merge, and the aggregate's 7 of 7 |
| R607-1-R1, R607-1-R2 | The exact texts, in `SPLIT_CONTROL_MEMORY.md` and the plan |

The Python idiom gate's exec inventory gains one entry for the test, with its guard. The edit must match its source exactly once, and the result must parse to exactly that one definition, run in its module's namespace.

## Description

In the split placement (`--ctrl-mailbox`) the control firmware owns the CPU's reset entry and runs from block RAM sized from its own linked image. No BIOS ROM or BIOS SRAM is built there. The all-fabric default is digest-identical.

| Piece | What it does |
|---|---|
| `sw/litex/ctrl_memory.py` | The one statement of the split map: `rom` at the reset address `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB; the bank plan; `RULES`, the 16 refusal rules under the checks `reset entry`, `memory map`, `memory-map overlap`, `allocation over budget` (56 RAMB36) and `staging buffer` |
| `sw/litex/milan_soc.py` | `CtrlMemory` builds a region from power-of-two banks of RAMB18 granules, largest first, each a LiteX `wishbone.SRAM`, and answers `err` past the last bank. `add_ctrl_memory` builds `rom` (initialised) and `sram` from `--ctrl-firmware`. Under `--ctrl-mailbox` no BIOS ROM or SRAM is built and no BIOS is compiled |
| `sw/firmware/ctrl/plat/ctrl_split.ld`, `ctrl_split_start.S` | The split link and the reset entry: stack, `.data` copied from `rom`, `.bss` cleared, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` | `--layout split` links the full F0-F5/F1 composition into that map and reports the bank plan; the flat layout is unchanged |
| `sw/litex/test_ctrl_memory.py` | Banks against an independent oracle; a planted defect per rule on ELFs from an independent writer; the real `CtrlMemory` in simulation across the decoded window; a probe linked through the real script; the SoC build through `main()`; the rule register; 40 mutants |
| `syn/ooc/ctrl_memory_ooc.py` | Emits both regions of each image as the SoC builds them, and the out-of-context Vivado script |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | The split placement's memory contract, the rule table, boot console and diagnostics, and fit |

**Linked spans** (`ctrl_srp_image.py --with-aecp --layout split`, pinned RV32 SDK, 8 KiB stack), bytes:

| Point | `rom` need | `sram` need | Sum | Flat span (unchanged) |
|---|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 95,032 | 45,520 | 140,552 | 140,400 |
| 1x1, two interfaces | 96,320 | 56,880 | 153,200 | 153,056 |
| 8x8, one interface | 108,680 | 86,080 | 194,760 | 194,224 |
| 8x8, two interfaces (largest) | 110,056 | 112,208 | 222,264 | 221,728 |

The split adds the reset entry (88 B), the second copy of `.data` and alignment. The spans hold the descriptor image (7,512 / 19,520 B), the shape's `nvm_stage` (3,344 / 13,264 B) and the lwSRP pool.

**Block RAM as mapped** (`syn/ooc/ctrl_memory_ooc.py`: Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`, out of context; unchanged in round 2):

| Point | Planned RAMB36 equivalents | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT cells / FF | Byte floor |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 35.0 | 33 / 2 | 34.0 | 212 / 32 | 35 |
| 1x1, two interfaces | 38.0 | 37 / 1 | 37.5 | 89 / 7 | 38 |
| 8x8, one interface | 48.5 | 46 / 2 | 47.0 | 307 / 33 | 48 |
| 8x8, two interfaces (largest) | 54.5 | 52 / 2 | 53.0 | 328 / 40 | 55 |

- **Planned:** every bank in block RAM.
- **Byte floor:** the flat linked span at 4,096 B per RAMB36, rounded up.
- **Budget:** every point is within 56 RAMB36. The largest leaves 3 tiles as mapped; the budget check reads the planned 54.5, so its image can grow 6 KiB (1.5 tiles) before it is refused.
- **`sram`:** maps exactly as planned.
- **`rom`:** maps below plan. Vivado trims ROM bit columns that are constant across a bank, and puts one small or sparse ROM bank in logic. With the region's bank decode and read multiplexer, the `rom` region takes 231 of the largest point's 328 LUT cells (220 Slice LUTs).

Before, the base BIOS ROM took 16 RAMB36 and its SRAM 2. One LiteX SRAM of the largest image took 64 RAMB36 (round 1).

**Ledger** (`MARK_II_AREA_PLAN.md`, mirrored in `AREA_BUDGET.md`):

- the BIOS ROM and SRAM are not built: -18 RAMB36, 0 RAMB18, measured at `e8454e27`;
- the firmware allocation as mapped at 8x8 with two interfaces: +52 RAMB36, +2 RAMB18, +53 tiles;
- totals: `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`, then 113 after the split's conditional release (8.5 below 121.5, reserve untouched);
- with every bank in block RAM: 125.5 and 114.5;
- at the ruled 56 firmware tiles: 116, leaving 5.5.

**Planted controls.** Through `milan_soc.py`'s `main()` in the test, each refused by its rule before any Verilog is written:

- an allocation over budget, 58 RAMB36: `allocation over budget`, rule `budget`;
- a memory-map overlap, `.bss` at `.data`'s address: `memory-map overlap`, rule `addresses`;
- a staging buffer of another shape, the 8x8 stage in the 1x1 build: `staging buffer`, rule `stage size`.

Round 1 ran the same three once on the linked firmware through the SoC build (the 8x8 two-interface image with a 16 KiB stack, 56.5 RAMB36; `.bss` linked at `.data`; the 1x1 image in an 8x8 build).

**Boot console and diagnostics.** The split image loses the LiteX BIOS and its console, the BIOS DDR3 initialisation and the shipping firmware's UART commands. It keeps the UART, `timer0`, `ctrl`, the identifier memory, the `ppmem` observer and every Milan CSR. Its CSR map equals the base `--ctrl-mailbox` export's; only the `rom` and `sram` region sizes differ.

**DDR3 at this base.** `KL_pp_shadow` is still instantiated, so DDR3 stays under `--ctrl-mailbox`. With no BIOS, `pp_mem_gate` never opens and the processor's three memory masters stay refused, as before training. F-INT PR 2 removes the wrapper; M8a-2 routes the split without DDR3.

**All-fabric default.** Both AX7101 shipping exports are digest-identical to the base: 22 files each, 0 differ after normalizing timestamps, the export directory and LiteX's comment-only hierarchy tree. Round 2 re-proved it against `08b90b68`, whose default export R606-1 had matched to dev `ac2c5e77`: both default exports are identical (22 files each, 0 differ), and so are both split exports (24 and 23 files, 0 differ).

## Authoritative references

- #640 ruling 6101485877: 224 KB binding, up to 56 RAMB36 as mapped; conditional release; no power-of-two waste; firmware owns the reset entry; M8a-1 and M8a-2.
- #640 round-2 assignment 6105011666; assignment 6100371426; owner decisions 5991591637 (D4) and 6081706413 (224 KB).
- `docs/design/MARK_II_AREA_PLAN.md`: L11 The SoC side; Firmware and block RAM ledger.
- `docs/design/AREA_BUDGET.md`: the memory ledger mirror.
- `docs/design/SPLIT_CONTROL_MEMORY.md`: the rule table (section 3) and fit (section 5).
- `docs/design/MAILBOX_SPLIT.md`: Default build (the `--ctrl-mailbox` switch).
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the export recipe used for the digest proof.

## How to get into the same state

```sh
git fetch origin
git switch 640-m8a
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 -m pip install pyyaml
python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
```

`$SDK` is the pinned RV32 SDK directory; `MILAN_RV32_CC` may name its `riscv32-linux-gcc`. The SoC arm needs the end-station builder's PyYAML and the VexiiRiscv generator that `elaborate.yml` installs.

## How to validate

```sh
python3 sw/litex/test_ctrl_memory.py
scripts/run_litex_sims.sh "$LOGS"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
```

Expected result / pass criteria:

- `test_ctrl_memory: 0 failure(s)` and `RESULT: PASS` (with an RV32 compiler), every one of the 40 `MUTANT` lines `[ok  ]`;
- the aggregate passes 7 of 7 at the head;
- R607-1's `mutants.py <tree> <out> <litex-python>`: all twelve mutants KILLED, each with named FAIL lines;
- the plan prints 54.5 RAMB36 for the largest point, and `--stage-bytes 3344` refuses it with `staging buffer`.

Local gate results, round 2 (each unpiped, rc 0 unless stated). `be431eec` to `516d7fb8` changes `docs/design/` only, outside the rule table the test reads; `516d7fb8` to `76605880` changes one prose line of that section.

| Gate | Head | Result |
|---|---|---|
| `test_ctrl_memory.py` (with the pinned RV32 SDK) | `be431eec`, `76605880` | 109 checks, 0 failures, `RESULT: PASS`; 40 of 40 mutants caught by a named failure |
| `run_litex_sims.sh --selftest` and the aggregate (pinned Verilator 5.050) | `516d7fb8` | 10 checks PASS; 7 of 7 PASS, 0 skipped |
| R607-1's `mutants.py`, unmodified | `be431eec` | 12 of 12 KILLED by named FAIL lines |
| R606-1's `probe_writable_rom.py` and `probe_region_top.py`; R607-1's `probe_malformed.py` and `probe_ctrlmem_sim.py` | `516d7fb8` | `.data` in rom refused `memory map`; every malformed input refused `memory map`; both simulation probes PASS |
| `ctrl_memory.py plan` under CPython 3.12.3, largest image | `516d7fb8` | 54.5; the 1x1 stage refused `staging buffer` (rc 2) |
| `ctrl_srp_image.py`, four points, split and flat | `516d7fb8` | eight ELFs byte-identical to round 1's; plans identical |
| `ctrl_memory_ooc.py`, four points, emission only | `516d7fb8` | inputs identical to those mapped in round 1, apart from date stamps |
| Default and split exports, `08b90b68` against head | `516d7fb8` | 22, 22, 24 and 23 files, 0 differ |
| `test_builder.py --require-elaboration --require-rv32` | `516d7fb8` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a bench build tree; recorded reason, as in round 1) |
| `syn/yosys/run.sh` | `516d7fb8` | 58 of 58 tops PASS; TAP-PURITY PASS |
| `check_soc_sources.py` and `--selftest`; `iob_pack_selftest.py` | `516d7fb8` | PASS |
| `check_py_idiom.py` (CPython 3.12.3) and `--selftest`; hygiene, TODO, fail-fast, test-evidence and shell-idiom ratchets | `76605880` | PASS, at ratchet |
| `docs_check.py`, `check_em_dash.py --base 08b90b68`, `gen_toc.py --check`/`--verify-anchors`, `check_doc_paths.py`, `check_doc_style.py`, `ci_events.py --check`, their self-tests, `git diff --check` | `76605880` | PASS |
| `scripts/run_all_suites.sh` | `76605880` | 61 of 61 suites, 2,185,848 checks, 0 failures (4 declared `tsn_fuzz` skips: tsn-gen absent) |

Round 1's gates (at `c20ed894` to `5d532e9d`) are unchanged in meaning: the out-of-context Vivado mapping at the images of `94190c36`, and the firmware host tests at `c20ed894`. Round 2 changes no firmware source.

## Known limitations / out of scope

- M8a-2, after F-INT PR 2: the split-image simulation boot to the control application's ready state, `check_nvm_capture.py` 8x8, `nvm_cosim`, `nvm_capture_cpu`, and the integrated route through the M0s recipe against its split figure (LUT, FF, RAMB deltas; WNS).
- The image linked here is the size fixture in the split layout; the reset entry is checked by layout, not by a CPU simulation.
- The bank decode sits on the CPU bus path; its timing is measured only by M8a-2's route.
- Headroom at the largest point is 1.5 RAMB36 (6 KiB) by the plan; growth beyond it is refused by name.
- The split build uses its own VexiiRiscv netlist, one for both shapes; on a cold metadata cache the hosted job pays one more Scala run for it.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained.
- The SoC arm exports with `--no-compile-software`, so it reads the Builder's BIOS decision from the flag the Builder reads rather than from a compiled BIOS.

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

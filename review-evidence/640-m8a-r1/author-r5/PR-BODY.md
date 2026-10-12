[A594]

## Contents

- **[Status](#status)** -- M8a-1 round 5 review-ready; the head and the commit on round 4's merge; `640-m8a` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Round 5](#round-5)** -- The fit re-measured on the firmware merged from dev, answering R606-4 and R607-4.
- **[Round 3](#round-3)** -- Each R606-2 and R607-2 finding and the change that answers it.
- **[Round 2](#round-2)** -- Each R606-1 and R607-1 finding and the change that answers it.
- **[Description](#description)** -- The split placement's memory map and block RAM, the rules, the fit at four points, the ledger.
- **[Authoritative references](#authoritative-references)** -- Rulings, plan sections and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands, their expected results and the gate table.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What waits for M8a-2, and the open risks.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

REVIEW READY for M8a-1 round 5, head `42678ae2f77fbbef056f7fb99859e0193181e6d7`. `640-m8a` -> `dev`.

- Round 5 adds one commit, `42678ae2` (documentation only), on round 4's head `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d`. It re-measures the fit on the merged firmware and carries it into both ledgers.
- Round 3 adds five commits on the round-2 head `76605880a20005cbc2acad1b23ba2ccebde64ca8`: `22caf735` (the gate-read page), `087df144` (the SoC arm in the `elaborate` interpreter), `4a2608cd` (ROM bytes only from validated load data), `4a57b41d` (the partial-placement ledger figures) and `ce10328c` (residue wording).
- Round 2 added `be431eec`, `516d7fb8` and `76605880` on `08b90b68`, which is the round-1 head `5d532e9d` plus a merge of dev `ac2c5e77` (M2, PR #710). Round 4's head `8ab2b5399ecc725ff0ad4421c0e64ef03b89d28d` merges dev `c6bd08c6` into `ce10328c`, keeping both sentences in `docs/ARCHITECTURE_HW_SW_SPLIT.md`; the manager validates the current-dev merge candidate at the merge turn.
- `scripts/ci_scope.py --selftest` passes at the head, and the LiteX aggregate passes 7 of 7 in an interpreter that installs `sw/litex/litex_pins.txt` and nothing else.

Every gate the round-5 change touches passes locally at the head; the gate tables are below. M8a-2 (boot, service checks, route) follows F-INT PR 2.

## Linked Issue / roles

Relates to #640

Executor: `[A594]`
Internal cleared-context reviewer: `[R606]`
External reviewer: `[R607]`

Assignment: #640 comment 6100371426. Round-1 STOP: #640 comment 6101473717. Ruling: #640 comment 6101485877 (this PR is its step M8a-1). Round 2: #640 comment 6105011666, answering R606-1 (#721 comment 6104999232) and R607-1 (#721 comment 6105008317). Round 3: #640 comment 6107088105, answering R606-2 (#721 comment 6107064124) and R607-2 (#721 comment 6107065061). Round 5: #640 comment 6118560882, answering R606-4 (#721 comment 6118557490) and R607-4 (#721 comment 6118122865).

## Round 5

R606-4-F1 = R607-4-F1 (MINOR): dev `c6bd08c6` (F-INT's publication writers, lwSRP `08ee86e8`) grew all four linked images, so the documented fit was that of the images of `ce10328c`.

| Item | Result |
|---|---|
| Re-link the four points | `ctrl_srp_image.py --with-aecp --layout split` (and flat) at `8ab2b539`, both shapes, one and two interfaces: all rc 0. Planned 35.5 / 38.0 / 48.5 / 55.0 RAMB36, each within 56. With the same runtime, `ce10328c` still links round 1's four split ELFs byte for byte |
| Map them out of context | `syn/ooc/ctrl_memory_ooc.py` and its Vivado script on the four new images: rc 0, every ROM image read. As mapped 35.0 / 37.5 / 47.0 / 54.0 tiles |
| Reconcile the documents | `SPLIT_CONTROL_MEMORY.md` section 5: fit table, bank fill, headroom (1.0 tile, 4 KiB; 5,064 B with the bank slack), which ROM bank Vivado puts in logic, the LUT figures. It names the revision it links and keeps the `ce10328c` figures with their source. Both ledgers: +54 tiles, 125 before and 114 after the release, 126 and 115 with every bank in block RAM, 131 for the partial placement |
| Limits | 55.0 of 56 planned; flat span 223,776 of 229,376 B (224 KiB). Nothing exceeded |
| Runtime | Built with R607-4's `runtime_probe.py`, which adds only `-fno-stack-protector` to the runtime recipe's compiles, as both reviewers did; the recipe's fix is #723 |
| Reviewers' probes | R607-4 `run_fit.py` (head and `previous-`) and `compare_fit.py`: PASS. R606-4 `link_points.sh` on both trees and `fit_summary.py`: the same figures, 5,064 B headroom at the largest |
| R606-4-R1 (residue) | The Status bullet carries R606-4-R1's exact sentence |

The shipping image's `rom` drops from five banks to two (64 + 32 KiB) and no longer has a bank in logic. At the largest point the 1,024-word bank is now full and in block RAM, and the new 512-word bank is in logic.

## Round 3

| Finding | Change |
|---|---|
| R606-2-F1: the rule table's page is read by a gated test but not registered, so `ci_scope.py --selftest` fails and every hosted classifier step is red | `docs/design/SPLIT_CONTROL_MEMORY.md` joins `GATE_READ_DOCS`, with a classification case. `CI_WORKFLOWS.md` lists seven gate-read pages and names `sw/litex/test_ctrl_memory.py` as this one's reader. `ci_scope.py --selftest` passes, and `ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` prints `true` |
| R606-2-F2: the SoC arm resolves LiteX's firmware data packages, which the `elaborate` install lacks | The SoC child refuses every `pythondata_software_*` import in every interpreter, and writes LiteX's headers without the firmware make inputs, as `sw/builder/test_shipping_clock_constraints.py` does. The arm compiles nothing, and the gateware, its init files and `csr.csv` read neither package. Provisioning the packages would widen the shared pins and job for something no gate here uses. A mutant is graded only against an arm that passed unmutated in the same run, so an environment failure never counts as a kill. In a `litex_pins.txt`-only interpreter the test passes, the aggregate is 7 of 7, and every SoC mutant is killed by its own check: `main() staging check removed` by the stage-size control, which now exports, and `shipping firmware linked` by `the split build adds no shipping firmware` |
| R607-2-F1: the reset-byte rule read section metadata, while ROM is programmed from the load segments' file bytes | New rule `load coverage` (`memory map`): every section with initial bytes must be carried by the load segments' file bytes. `entry bytes` also requires those bytes to carry the first word at the reset address. Regressions: the test's ELFs (reset segment emptied, reset section moved, reset segment cut to one word, `.data`'s segment emptied); the genuinely linked probe (emptied, cut, `.data`'s emptied), whose rom words must also equal the toolchain's `objcopy -O binary`; and the real split SoC build, refused before any Verilog or init file. There are four new mutants, 44 in all, and the register has 17 rules. The four shipped split images plan and program byte-identically |
| R606-2-F3: the partial-placement figure and the give-way basis | Both documents: the partial placement keeps AECP's six tiles, `124 + 6 = 130`, 8.5 over 121.5 at the measured 53. The give-way text names the ruled 56-tile firmware allocation |
| R606-1-R1 (residue) | The two exact texts, in `AREA_BUDGET.md` and the plan |

R607-2's `probe_load_soc.py`, run unmodified, no longer reproduces: the export is refused (`reset entry: no load segment carries the first word at the reset address 0x00000000, so rom would hold none there`) and writes no Verilog. Its `probe_elf_loads.py` reports the empty reset segment refused by `entry bytes` and the short one by `load coverage`.

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
| `sw/litex/ctrl_memory.py` | The one statement of the split map: `rom` at the reset address `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB; the bank plan; `RULES`, the 17 refusal rules under the checks `reset entry`, `memory map`, `memory-map overlap`, `allocation over budget` (56 RAMB36) and `staging buffer` |
| `sw/litex/milan_soc.py` | `CtrlMemory` builds a region from power-of-two banks of RAMB18 granules, largest first, each a LiteX `wishbone.SRAM`, and answers `err` past the last bank. `add_ctrl_memory` builds `rom` (initialised) and `sram` from `--ctrl-firmware`. Under `--ctrl-mailbox` no BIOS ROM or SRAM is built and no BIOS is compiled |
| `sw/firmware/ctrl/plat/ctrl_split.ld`, `ctrl_split_start.S` | The split link and the reset entry: stack, `.data` copied from `rom`, `.bss` cleared, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py` | `--layout split` links the full F0-F5/F1 composition into that map and reports the bank plan; the flat layout is unchanged |
| `sw/litex/test_ctrl_memory.py` | Banks against an independent oracle; a planted defect per rule on ELFs from an independent writer; the real `CtrlMemory` in simulation across the decoded window; a probe linked through the real script, with its load segments planted; the SoC build through `main()`; the rule register; 44 mutants |
| `syn/ooc/ctrl_memory_ooc.py` | Emits both regions of each image as the SoC builds them, and the out-of-context Vivado script |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | The split placement's memory contract, the rule table, boot console and diagnostics, and fit |

**Linked spans** (`ctrl_srp_image.py --with-aecp --layout split`, pinned RV32 SDK, 8 KiB stack), bytes, firmware of `8ab2b539` (dev `c6bd08c6`):

| Point | `rom` need | `sram` need | Sum | Flat span |
|---|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 96,624 | 45,776 | 142,400 | 142,256 |
| 1x1, two interfaces | 98,056 | 57,152 | 155,208 | 155,056 |
| 8x8, one interface | 110,344 | 86,336 | 196,680 | 196,144 |
| 8x8, two interfaces (largest) | 111,848 | 112,464 | 224,312 | 223,776 |

The split adds the reset entry (88 B), the second copy of `.data` and alignment. The spans hold the descriptor image (7,512 / 19,520 B), the shape's `nvm_stage` (3,344 / 13,264 B) and the lwSRP pool.

**Block RAM as mapped** (`syn/ooc/ctrl_memory_ooc.py`: Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`, out of context; re-mapped in round 5 on the images above):

| Point | Planned RAMB36 equivalents | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT cells / FF | Byte floor |
|---|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 35.5 | 34 / 2 | 35.0 | 128 / 8 | 35 |
| 1x1, two interfaces | 38.0 | 37 / 1 | 37.5 | 89 / 7 | 38 |
| 8x8, one interface | 48.5 | 46 / 2 | 47.0 | 417 / 42 | 48 |
| 8x8, two interfaces (largest) | 55.0 | 53 / 2 | 54.0 | 266 / 34 | 55 |

- **Planned:** every bank in block RAM.
- **Byte floor:** the flat linked span at 4,096 B per RAMB36, rounded up.
- **Budget:** every point is within 56 RAMB36. The largest leaves 2 tiles as mapped; the budget check reads the planned 55.0, so its banks can grow 4 KiB (1.0 tile) before it is refused, 5,064 B with the unused bytes inside them.
- **`sram`:** maps exactly as planned.
- **`rom`:** maps below plan. Vivado trims ROM bit columns that are constant across a bank. At 8x8 it also puts one small or sparse ROM bank in logic (1,024 words with one interface, 512 with two); at 1x1 every bank is in block RAM. With the region's bank decode and read multiplexer, the `rom` region takes 169 of the largest point's 266 LUT cells (161 Slice LUTs).
- **Earlier:** the firmware of `ce10328c` planned 35.0 / 38.0 / 48.5 / 54.5 and mapped 34.0 / 37.5 / 47.0 / 53.0 tiles (rounds 1 to 3).

Before, the base BIOS ROM took 16 RAMB36 and its SRAM 2 (`e8454e27`). One LiteX SRAM of that revision's largest image took 64 RAMB36 (round 1).

**Ledger** (`MARK_II_AREA_PLAN.md`, mirrored in `AREA_BUDGET.md`):

- the BIOS ROM and SRAM are not built: -18 RAMB36, 0 RAMB18, measured at `e8454e27`;
- the firmware allocation as mapped at 8x8 with two interfaces: +53 RAMB36, +2 RAMB18, +54 tiles;
- totals: `87.5 - 6.5 + 6 - 18 + 54 + 2 = 125`, then 114 after the split's conditional release (7.5 below 121.5, reserve untouched);
- with every bank in block RAM: 126 and 115;
- at the ruled 56 firmware tiles: 116, leaving 5.5.

**Planted controls.** Through `milan_soc.py`'s `main()` in the test, each refused by its rule before any Verilog or init file is written:

- an allocation over budget, 58 RAMB36: `allocation over budget`, rule `budget`;
- a memory-map overlap, `.bss` at `.data`'s address: `memory-map overlap`, rule `addresses`;
- a staging buffer of another shape, the 8x8 stage in the 1x1 build: `staging buffer`, rule `stage size`;
- since round 3, the reset segment's file bytes emptied with its section kept: `reset entry`, rule `entry bytes`.

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

`$SDK` is the pinned RV32 SDK directory; `MILAN_RV32_CC` may name its `riscv32-linux-gcc`. The SoC arm needs the end-station builder's PyYAML and the VexiiRiscv generator that `elaborate.yml` installs. It needs no LiteX firmware data package: it refuses them in any interpreter.

## How to validate

```sh
python3 sw/litex/test_ctrl_memory.py
scripts/run_litex_sims.sh "$LOGS"
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
```

`$RUNTIME` holds the archives of `sw/firmware/ctrl/test/ctrl_image_runtime.py`. With the pinned SDK they link only if the runtime is compiled with `-fno-stack-protector` (#723); round 5 added that flag as both reviewers did.

Expected result / pass criteria:

- `test_ctrl_memory: 0 failure(s)` and `RESULT: PASS` (with an RV32 compiler), every one of the 44 `MUTANT` lines `[ok  ]`, in an interpreter that installs `sw/litex/litex_pins.txt` alone and in one that also has LiteX's firmware data packages;
- the aggregate passes 7 of 7 at the head;
- `python3 scripts/ci_scope.py --selftest` passes, and `python3 scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` prints `true`;
- R607-2's `probe_load_soc.py` no longer reproduces (its assertion fails on a refused build), and its `probe_elf_loads.py` reports every load variant refused by name;
- R607-1's `mutants.py <tree> <out> <litex-python>`: all twelve mutants KILLED, each with named FAIL lines (round 2);
- the plan prints 55.0 RAMB36 for the largest point, and `--stage-bytes 3344` refuses it with `staging buffer`;
- `ctrl_memory_ooc.tsv` maps `s8i2_rom` to 26 RAMB36 and 1 RAMB18 and `s8i2_sram` to 27 and 1: 54.0 tiles.

Local gate results, round 5, at the committed head `42678ae2` (each unpiped, rc 0):

| Gate | Environment | Result |
|---|---|---|
| `ctrl_srp_image.py --with-aecp`, four points, split and flat, then `ctrl_memory.py plan` | pinned RV32 SDK; runtime built with `-fno-stack-protector` added (#723) | at `8ab2b539` (the head's firmware): the figures above. At `ce10328c`, same runtime: round 1's four split ELFs, byte for byte |
| `syn/ooc/ctrl_memory_ooc.py` and its Vivado script | LiteX interpreter; Vivado 2026.1 out of context | 8 of 8 tops; every ROM image read; no error or critical warning |
| Both reviewers' fit probes (`run_fit.py`, `compare_fit.py`; `link_points.sh`, `fit_summary.py`) | as above | PASS; the same figures |
| `docs.yml`: every `docs-check` command in order (80), `wire-accountability`, and `docs-check-no-git` on the tree exported without `.git` | CPython 3.12.3 with the job's installs only; pinned sv2v v0.0.12; GNU make 4.3; a HOME holding only the pinned RV32 SDK; no LiteX; em-dash base `c6bd08c6` | 83 of 83 rc 0; `check_em_dash.py` 0 findings over 324 added lines; `ci_events.py` OK, 1,821 contract items, selftest 2,530 arms; `test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 17 NOT RUN` (15 LiteX arms that job has no interpreter for, gate 11, and gate 1b's mutation, which make 4.3 does not honour) |
| `scripts/run_litex_sims.sh --selftest` and the aggregate | `litex_pins.txt` alone (plus PyYAML), the patch series; pinned Verilator 5.050 | 10 checks PASS; 7 of 7 PASS; `test_ctrl_memory`: `RESULT: PASS`, 44 of 44 mutants caught, the section-3 rule table equal to `ctrl_memory.RULES` |
| `scripts/ci_scope.py --selftest`; the three changed pages | CPython 3.12.3 | PASS; `SPLIT_CONTROL_MEMORY.md` and `AREA_BUDGET.md` relevant, the plan documentation only |
| `syn/ooc/pp_resource_gate.py check-baseline` | CPython 3.12.3 | `baseline PASS: 3 endpoints` |

Not run in round 5: the suite sweep, Yosys, the elaboration gate and the firmware host suites, since `42678ae2` changes three pages under `docs/design/` and nothing they read. The merge `8ab2b539` is validated with the current-dev merge candidate at the merge turn. The local Actions replica needs the pushed head.

Local gate results, round 3, at the committed head `ce10328c` (each unpiped, rc 0 unless stated):

| Gate | Environment | Result |
|---|---|---|
| `docs.yml`: every `docs-check` command in order (80), `wire-accountability`, and `docs-check-no-git` on the tree exported without `.git` | CPython 3.12.3 with the job's installs only (hash-locked parser and Markdown renderer, PyYAML, wavedrom); pinned sv2v v0.0.12; GNU make 4.3; a HOME holding only the pinned RV32 SDK, installed fresh and verified; no LiteX; em-dash base the merge base with `dev` `ac2c5e77` | 83 of 83 rc 0; `test_builder.py --require-rv32`: `ALL GATES PASS EXCEPT 14 NOT RUN` (the LiteX arms that job has no interpreter for, and gate 11) |
| `scripts/ci_scope.py --selftest`; `scripts/ci_scope.py docs/design/SPLIT_CONTROL_MEMORY.md` | CPython 3.12.3 | PASS; `true` |
| `scripts/ci_events.py --check` and `--selftest` | CPython 3.12.3 with PyYAML | OK, 1,749 contract items; PASS, 2,374 arms |
| `scripts/run_litex_sims.sh --selftest` and the aggregate | `litex_pins.txt` alone (plus PyYAML), `ci_litex_env.py` and the patch series as `elaborate.yml` runs them; pinned Verilator 5.050 | 10 checks PASS; 7 of 7 PASS; `test_ctrl_memory`: 123 checks, `RESULT: PASS`, 44 of 44 mutants caught |
| `sw/builder/test_builder.py --require-elaboration --require-rv32` | as the aggregate | `ALL GATES PASS EXCEPT 1 NOT RUN` (gate 11 needs a bench build tree, as before) |
| `test_ctrl_memory.py` | an interpreter that also has LiteX's firmware data packages | `RESULT: PASS`, the same log line for line once temporary names are normalised |
| Control: that run with the include hook removed | as above | rc 1 as planted: the split export fails by name, and all six SoC mutants report `not graded` |
| Per commit: classifier, event, Python idiom and ratchet gates, docs gates, `pp_resource_gate.py check-baseline` (after the `AREA_BUDGET.md` edits), `check_em_dash.py --base 76605880`, `git diff --check` | as above | PASS |

Not rerun in round 3: the suite sweep and Yosys, since no file under `hdl/`, `tb/` or `syn/` and no gitlink changed since `76605880`, where they passed. Vivado was not rerun either: nothing it maps changed, and the four shipped split images plan and program identically. The local Actions replica needs the pushed head.


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
- Headroom at the largest point is 1.0 RAMB36 (4 KiB) by the plan, 5,064 B with the slack inside its banks; growth beyond it is refused by name. One dev merge (`c6bd08c6`) took 0.5 RAMB36 of it.
- The split build uses its own VexiiRiscv netlist, one for both shapes; on a cold metadata cache the hosted job pays one more Scala run for it.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained.
- The SoC arm exports with `--no-compile-software`, so it reads the Builder's BIOS decision from the flag the Builder reads rather than from a compiled BIOS.
- The SoC arm writes LiteX's headers without the firmware make inputs, and refuses the firmware data packages, through LiteX's `Builder._generate_includes`, as `sw/builder/test_shipping_clock_constraints.py` does. A LiteX that renamed it would fail the arm by name. Compiling software for the split image is M8a-2's boot.
- Two optional review suggestions stay open: an `sram` section outside the startup copy's linker ranges, and unnamed errors for out-of-range ELF table indices (fail-closed).

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

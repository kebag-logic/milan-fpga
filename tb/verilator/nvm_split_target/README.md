# Saved-state store on the split CPU

This harness boots the split image's saved-state store (F1, [`ctrl_nvm`](../../../sw/firmware/ctrl_nvm/README.md)) on the split placement's CPU, memory and flash.
Its contract is the [S4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258) on #665.
It runs on the [CPU budget harness's](../ctrl_service_budget/README.md) test SoC: the shipping VexiiRiscv at 50 MHz with the split's instruction cache, `CtrlMemory`, LiteSPI and its native flash model.
The image is `ctrl_srp_image.py --with-aecp --layout split`, whose flash port compiles against the split SoC's own map ([the flash port's map](#the-flash-ports-map)).
Every figure is a measured clock count, never an estimate.

## Contents

- **[Run](#run)** -- Prerequisites, the two points, reuse and the regrade.
- **[The flash port's map](#the-flash-ports-map)** -- What is generated from the split SoC's `csr.csv`, and how the test SoC is held to it.
- **[The cases](#the-cases)** -- Each boot's image, journal and stimulus, and what it must show.
- **[Grading](#grading)** -- The traced calls, the step phases, the capture's bound and the apply order.
- **[Results](#results)** -- The capture and the commit's steps, and every case, at both points.
- **[Controls and self-test](#controls-and-self-test)** -- The planted defects, the bound's control and the grader mutants.
- **[Limits](#limits)** -- What is not measured, and why.

## Run

The prerequisites are the CPU budget harness's ([Run and reproduce](../ctrl_service_budget/README.md#run-and-reproduce)): the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator.
Keep build directories outside the checkout.
The portable self-test needs Python and PyYAML only:

```sh
python3 -B tb/verilator/nvm_split_target/run.py --self-test
```

Each point builds one image per arm and plant, then runs every case:

```sh
python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1
python3 -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir /tmp/nvm-target-8x8
```

`1x1` is `endstation_ax7101_1x1_tdm8` with one AVB interface, and `8x8` is `endstation_ax7101_8x8` with two, the CPU budget harness's two points.
`--cases` selects cases; the `commit` case always runs, because the others boot the journal it writes.
`--jobs` sets how many boots run at once.
`--reuse-build` reuses each arm's build when every input its `build.json` records still attests (`build.reused`).
`--regrade` grades the runs recorded in `--out` on reused builds, and refuses a case whose recorded script or journal is not the one the run would use.
A step over T_svc fails the run unless `--record-budget-findings` is given.

The directory has no Makefile on purpose: the serial sweep discovers every Makefile, and `scripts/suite_shards.py` must then register the suite.

## The flash port's map

`nvm_flash_litespi.c` reaches the LiteSPI command master, `timer0` and the memory-mapped flash window.
On the target their addresses are the split SoC's: `milan_soc.py --ctrl-mailbox --ctrl-firmware`, exported for the point's config.
[`gen_flash_port.py`](../../../sw/firmware/ctrl_nvm/plat/gen_flash_port.py) reads them from that export's `csr.csv` and writes `generated/csr.h` and `generated/mem.h`, which `ctrl_srp_image.py --flash-map` puts ahead of the RV32 stand-ins.
`csr.csv` carries no field offsets, so the generator reads those from the same export's LiteX `csr.h` and refuses any address on which the two files differ.
LiteX's own `csr.h` cannot be compiled into the image: it includes libbase's headers.

`build.flash_map` exports the split SoC with the point's one-interface image on the stand-ins, generates the map, then exports it again with that image linked against the map.
It refuses the build unless the two maps are the same, so the CSR map does not depend on the image.
The product SoC build plans no ledgered point, so the export uses the one-interface image at 8x8 too.

The test SoC places the flash and `timer0` from the map.
Its LiteSPI is `add_spi_flash`'s, with its command master, in the split SoC's `spiflash` bank: the PHY's two CSRs, the memory-mapped reader's two, then the master's five.
After the export, `split_soc.map_deviations` compares the test SoC's own `csr.csv` with the split SoC's map for every register the port uses and for the flash window, and refuses any difference.
At both points they are:

| Device | The split SoC, and the test SoC | The RV32 stand-ins (`ctrl_nvm/test/rv32/generated`) |
|---|---|---|
| `spiflash_master_cs` to `_status` | `0xf000_2810` to `0xf000_281c` | `0xf000_3000` to `0xf000_300c` |
| `timer0_load` to `_value` | `0xf000_3000` to `0xf000_3010` | `0xf000_3800` to `0xf000_3810` |
| flash window | `0x0100_0000`, 16 MiB | `0x2000_0000`, 16 MiB |
| journal (`milan_flash_journal_*`) | `0x00ee_0000`, 128 KiB | (the store's build constants, the same) |

The mailbox stays at the fixture's placeholder (`ctrl_build.py`, `CTRL_MBX_BASE`); the target platform firmware owns that address.

The generator's rules are its docstring's.
The journal it accepts is `milan_soc.py`'s `FLASHBOOT_RESERVED` journal, which the store is built with (`nvm_bench.py` reads the same literal).
It is two slots, each one 64 KiB erase block: the A/B geometry `scripts/check_nvm_record_space.py` sizes every container against (its check 5).
It must be aligned, inside the device, and clear of every image slot (`FLASHBOOT_LAYOUT`: the bitstream and the AEM), the user slot, and every image the SoC publishes.
The port's own guard (`ls_in_journal`) refuses a program or an erase outside `MILAN_FLASH_JOURNAL_OFFSET` and `_SIZE`, so these rules bind that guard to the journal of the SoC the image runs on.

## The cases

Each case boots one image with one journal in the flash and runs one script ([`target_cases.py`](target_cases.py)).
The testbench loads the journal over the erased flash (`BUDGET_JOURNAL_IN`) and writes the journal it leaves at the end (`BUDGET_JOURNAL_OUT`).
After booting and raising every link, each case but the planted guard asks two questions, each answered from the owner the store restores:

- READ_DESCRIPTOR of the ENTITY, for its `entity_name` (IEEE 1722.1-2021 7.4.5, the descriptor's 7.2.1 layout);
- GET_RX_STATE of sink 0, for its talker (IEEE 1722.1-2021 8.2.1; Milan v1.2 5.5.3.5, the fast connect of a saved binding).

| Case | Image | Journal | Must show |
|---|---|---|---|
| `commit` | `capture-all` | blank | Every record of the shape is marked changed once the boot releases. SET_NAME renames the entity and BIND_RX binds sink 0 to a talker. The store captures every record from its owners and commits: one erase and the container's pages. The journal it leaves decodes, by the reference codec, with the saved name and sink 0's binding; both questions answer them. |
| `valid` | fixture | the commit's | Both questions answer the saved values, the apply order is the container's, and nothing is written. |
| `absent` | fixture | blank | No owner applies anything, the name is not a saved one, sink 0 is unbound, and nothing is written. |
| `torn` | fixture | the commit's container in slot A; in slot B the next sequence renaming the entity, its last page never programmed | Slot A's values are applied in its order, the newer torn slot is refused, and nothing is written. |
| `version` | fixture | the commit's container under the next major version in slot A, slot B blank | The slot is refused for its version: no owner applies anything, the name is not a saved one, sink 0 is unbound, and nothing is written, the refused slot included. |
| `guard` | `guard-probe` | blank | After the boot the port is asked to erase four blocks outside the journal (the bitstream's first block, the block below the journal, the block above it and the one beyond) and to program three pages outside it. Every call reaches the port and is refused before the command master is touched. One erase inside the journal reaches the device, which sees it and nothing else. Then the boot opens the mailbox. |

`capture-all` and `guard-probe` are labelled test-code arms: edits of the size fixture in a scratch copy (`build.Variant`), never the formal image.
The planted defects are in [Controls and self-test](#controls-and-self-test).

## Grading

[`target_grade.py`](target_grade.py) reads each log through the CPU budget harness's parser.
The testbench traces calls passively ([`sim_main.cpp`](../ctrl_service_budget/sim_main.cpp), `trace_commit`):

- a SPAN line for every call of `nvm_store_boot` and `nvm_store_service`, from the commit of the function's entry to the commit of its return address (the call's PC plus 4), in CPU cycles;
- a CALL line for every entry of the owners' apply and latch functions (`acmp_restore_binding`, `aecp_value_restore`, `aecp_map_restore`, `aecp_restore_settle`, `acmp_nvm.c`'s and `aecp_nvm.c`'s `latch`) and of the flash port's `ls_read`, `ls_program`, `ls_erase` and `ls_busy` (`build.CALL_SYMBOLS`).

A service step's phase is the first of its calls in this order: the owners' latch (capture), `nvm_crc32_update` (seal), `ls_erase`, `ls_program`, `ls_read` (the blank check or the verify) and `ls_busy` (a poll).
The step after the last latch, which ends the capture and seals the header (`nvm_seal_begin`), is the capture's.

**The capture** is the store's capture phase for one work set with every record of the shape dirty: the sum of its steps' CPU cycles.
It must latch exactly the shape's records, one a step, and take at most 24.5 ms: half the shipping writer's guaranteed 49 ms hold floor, the bound `check_nvm_capture.py` holds the shipping capture to (`nvm_capture_cpu/recipe.py`, `HOLD_FLOOR_MS`).
The store latches one record per 10 ms TICK (`tick_ms`, `sw/mailbox/mailbox.yaml`), so the capture's elapsed time is paced by the loop: it is reported, not held to the bound.
Each step's CPU time is held to T_svc = 10 ms ([FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)).

**The apply order** is read inside the one `nvm_store_boot` span.
The owners' apply entries in order must be exactly the booted container's (`expected_applies`):

1. every binding, `acmp_restore_binding`;
2. every other non-erased record in ascending id: `aecp_value_restore` for a value, `aecp_map_restore` for a map;
3. `aecp_restore_settle` once, before the first name, or last when the container has none;
4. the names, `aecp_value_restore`.

That is D3's order: bindings, then formats, maps, the settle step and names ([ARCHITECTURE_HW_SW_SPLIT.md section 2](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#2-boot-sequence); [`ctrl_nvm/README.md`](../../../sw/firmware/ctrl_nvm/README.md#boot), "Boot" items 5 to 7).
An erased record applies nothing, and SUID and MCR are applied by no owner (`aecp_nvm.c`).

Every case also fails on a trap, a bus error, a failed testbench check or a wait that timed out.

## Results

The results are pending the measurement at this head.

## Controls and self-test

Each planted defect is a scratch copy of the saved-state store's tree (`build.Plant`), built and booted like the cases:

| Control | Planted defect | Journal | Caught by |
|---|---|---|---|
| `reorder-settle` | the D3 walk's settle step runs after the names (`nvm_store.c`, its test before the first name removed) | the commit's | the apply order |
| `reorder-bindings` | the binding walk runs after the D3 walk | the commit's | the apply order |
| `guard-removed` | `ls_in_journal` passes every address, in the `guard-probe` arm | blank | the flash model, which refuses a write outside the journal: `flash write escaped the journal` |
| `capture-one-page-past` | the measured commit's capture lengthened to exactly its bound, then by one page of its own measured cost past it (`target_grade.lengthened`) | - | at the bound it fits; one page past it is over |

The capture's control is planted in the measured commit itself: a page's cost is the capture's cycles per byte of the shape's container, times 256.

The self-test ([`target_selftest.py`](target_selftest.py)) runs the graders on synthetic logs and the journal builder on the 1x1 shape.
It requires a capture at exactly its bound to fit, one a page past it to be caught, a missing record to be refused and every step to be classified by its calls.
It requires the container's own apply order to pass, and each of these to be caught: the settle after the names, a binding after the D3 walk, a name before a map, one apply missing, one too many and two boots.
It requires the derived journals to be judged by the reference codec as the cases need them, and every arm and planted defect to apply to the checkout's sources.
Then it replaces each grading rule in turn with a weaker one, and a named check must fail:

| Mutant | Caught by |
|---|---|
| capture: strictly below the bound | a capture at exactly its bound fits |
| capture: the bound is the whole hold floor | a capture one page of its own cost past its bound is caught |
| capture: the closing step is not the capture's | a capture at exactly its bound fits |
| capture: the planted page is not added | a capture one page of its own cost past its bound is caught |
| order: settle last whatever the names | the bindings first, then the D3 records in ascending id, settle before the first name |
| order: only the first entry compared | the settle after the names is caught |
| answers: any sequence_id | the answers are read by sequence_id: the name and the talker |

## Limits

- The flash model's erase and program waits are zero (`fw_service_budget/flash.hpp`), so the commit's elapsed time is the store's step pacing, not a part's.
- One phase of each boot is run; the boot path's host suite covers the faults on every read ([`ctrl_nvm/README.md`](../../../sw/firmware/ctrl_nvm/README.md#the-host-suite)).
- The mailbox's datapath is held idle as the CPU budget harness holds it, so the face block's windows are never answered.
- The capture's records come from the fixture's owners as composed; the target platform's own `main` is a later image.

# Saved-state store on the split CPU

This harness boots the split image's saved-state store (F1, [`ctrl_nvm`](../../../sw/firmware/ctrl_nvm/README.md)) on the split placement's CPU, memory and flash.
Its contract is the [S4 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258) on #665, with the capture's timing as the [owner decided on 2026-10-29](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6504551000) (option (c), [The capture's timing](#the-captures-timing)).
It runs on the [CPU budget harness's](../ctrl_service_budget/README.md) test SoC: the shipping VexiiRiscv at 50 MHz with the split's instruction cache, `CtrlMemory`, LiteSPI and its native flash model.
The image is `ctrl_srp_image.py --with-aecp --layout split`, whose flash port compiles against the split SoC's own map ([the flash port's map](#the-flash-ports-map)).
Every figure is a measured clock count, never an estimate.

## Contents

- **[Run](#run)** -- Prerequisites, the two points, reuse and the regrade.
- **[The flash port's map](#the-flash-ports-map)** -- What is generated from the split SoC's `csr.csv`, and how the test SoC is held to it.
- **[The cases](#the-cases)** -- Each boot's image, journal and stimulus, and what it must show.
- **[Grading](#grading)** -- The traced calls, the step phases, T_svc, the capture's measurement and the apply order.
- **[Results](#results)** -- The capture and the commit's steps, and every case, at both points.
- **[Controls and self-test](#controls-and-self-test)** -- The planted defects, the step control, D5's check on the current flash writer and the grader mutants.
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
A service step over T_svc fails its case, and so the run.

Each run writes `results.json` and `table.md` to `--out`.
`results.json` holds the point, its shape, T_svc and every case's result, and the CPU and bus clocks every figure was converted and graded at (`cpu_hz`, `sys_hz`).
Those clocks are the ones every arm's `build.json` records, from the shape's constraints; builds that record different clocks are refused (`run.clocks`).
`table.md` names the same clocks, in MHz and in hertz, on the line above each of its tables.
The run is refused, exit 2 and no `table.md`, when the record lacks a clock, when a figure in it is not its CPU cycles at the record's CPU clock, or when its clocks are not its builds' (`run.provenance`, `run.against_build`).

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

**Every step** of the store, in every phase and in every case, is held to T_svc of CPU time ([FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing)).
A step over it is a finding of its case (`over_t_svc`), naming the step and its phase.
The bound is the CPU budget harness's `scenario.T_SVC_MS`.
At this harness's base that is the 10 ms proposal.
The owner approved `T_svc` = 20 ms on 2026-10-29, graded per family as `min(T_svc, ceiling)` ([#665](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075)); `scenario.py` takes that value with the change that makes it normative.
10 ms is under every family's bound, the 18 ms of SRP's included, so a step within it is within each.
The boot is not a service step: it runs once, before the loop, and is measured, not held to T_svc.

**The capture** is the store's capture phase for one work set with every record of the shape dirty.
It must latch exactly the shape's records, one a step, and the step that ends it.
It is measured and recorded, not graded against a bound:

- its CPU time, the sum of its steps' CPU cycles;
- its elapsed time, from its first step's start to its last step's end.

The store latches one record per 10 ms TICK (`tick_ms`, `sw/mailbox/mailbox.yaml`), so the elapsed time is the loop's pacing.

**The apply order** is read inside the one `nvm_store_boot` span.
The owners' apply entries in order must be exactly the booted container's (`expected_applies`):

1. every binding, `acmp_restore_binding`;
2. every other non-erased record in ascending id: `aecp_value_restore` for a value, `aecp_map_restore` for a map;
3. `aecp_restore_settle` once, before the first name, or last when the container has none;
4. the names, `aecp_value_restore`.

That is D3's order: bindings, then formats, maps, the settle step and names ([ARCHITECTURE_HW_SW_SPLIT.md section 2](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#2-boot-sequence); [`ctrl_nvm/README.md`](../../../sw/firmware/ctrl_nvm/README.md#boot), "Boot" items 5 to 7).
An erased record applies nothing, and SUID and MCR are applied by no owner (`aecp_nvm.c`).

Every case also fails on a trap, a bus error, a failed testbench check or a wait that timed out.

### The capture's timing

The owner's decision of 2026-10-29 19:05 on #665, option (c), restates the first acceptance item of S4:

- **The split writer F1 is not held to D5's 24.5 ms capture bound.** F1 holds no owner while it captures, and a change behind its cursor opens its own window (DR2a). So the hold the bound protects does not exist in the split.
- **Each F1 step stays bounded by T_svc**, under FR_NFR 3.4.1 as amended (20 ms, graded per family). The cases grade it as described above.
- **The total capture time has no bound of its own.** It is measured and recorded at both points ([Results](#results)). A power loss inside it loses at most the unsaved change, because the previous slot stays valid (the `torn` case).
- **D5 on the current flash writer is unchanged.** The 24.5 ms bound covers the current flash writer's capture only: half that writer's guaranteed 49 ms hold floor (`nvm_capture_cpu/recipe.py`, `HOLD_FLOOR_MS`). `scripts/check_nvm_capture.py` keeps it, and its 8x8 maximum of 13.863 ms stays gated. This harness's self-test fails if that writer's grader stops refusing a capture over 24.5 ms ([Controls and self-test](#controls-and-self-test)).

## Results

Measured at the head this harness lands with, on the split's 4 KiB instruction cache.
Every figure below is at the clocks both points' builds recorded: the CPU at 50 MHz (50,000,000 Hz) and the bus at 100 MHz (100,000,000 Hz).
Each run's `results.json` and `table.md` carry them.

```sh
python3 -B tb/verilator/nvm_split_target/run.py --point 1x1 --build-dir /tmp/nvm-target-1x1
python3 -B tb/verilator/nvm_split_target/run.py --point 8x8 --build-dir /tmp/nvm-target-8x8
```

Both runs exit 0: every case passes, no step is over T_svc, and every control is caught.

### The capture

Recorded, not bounded ([The capture's timing](#the-captures-timing)); CPU 50 MHz, bus 100 MHz:

| Point | Records, container | Capture steps | CPU time, cycles | CPU time, ms | Elapsed, ms | Longest step, ms | Fixed a step, cycles | A payload byte, cycles | Idle step, cycles |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | 54, 3,336 B (2,858 B of payload) | 55 | 1,361,143 | 27.223 | 534.905 | 0.815 | 11,062 | 263.7 | 9,486 |
| 8x8 | 164, 13,256 B (11,898 B of payload) | 165 | 5,161,328 | 103.227 | 1,638.061 | 2.639 | 16,500 | 205.5 | 9,389 |

The fixed cost and the cost a byte are the least-squares line through the latch steps' CPU cycles against the payload of the record each latched.
An idle step, which every step pays too, is mostly the flash port's 64-bit clock conversion (`ls_now_us`).
The elapsed time is the loop's pacing, one record a 10 ms tick; the CPU time is spread over it, at most 2.639 ms in any one step.
For comparison, the current flash writer's capture copies 13,210 bytes at 8x8 in 13.86 ms (`nvm_capture_cpu/measurements.json`), about 52 cycles a byte, holding its owners while it does.

### The commit's steps

CPU 50 MHz, bus 100 MHz:

| Phase | 1x1: steps, longest CPU cycles (ms) | 8x8: steps, longest CPU cycles (ms) |
|---|---|---|
| capture | 55, 40,771 (0.815) | 165, 131,929 (2.639) |
| seal | 14, 34,384 (0.688) | 52, 34,839 (0.697) |
| erase | 1, 12,416 (0.248) | 1, 12,595 (0.252) |
| poll | 15, 11,851 (0.237) | 53, 12,321 (0.246) |
| program | 14, 101,098 (2.022) | 52, 101,577 (2.032) |
| read (blank check and verify) | 28, 95,354 (1.907) | 104, 95,984 (1.920) |
| idle | 203, 10,022 (0.200) | 215, 10,358 (0.207) |

Every step is within T_svc at both points; the longest, 2.639 ms, is a capture step at 8x8.
The commit erased one block and programmed 14 pages at 1x1 and 52 at 8x8, and the journal it left decodes by the reference codec with the saved name and sink 0's binding.

### The boots

CPU 50 MHz, bus 100 MHz:

| Case | 1x1: apply entries, `nvm_store_boot` CPU cycles (ms) | 8x8 |
|---|---|---|
| `valid` | 44, 5,027,209 (100.5) | 133, 24,423,878 (488.5) |
| `absent` | 0, 506,631 (10.1) | 0, 1,746,898 (34.9) |
| `torn` | 44, 8,255,898 (165.1) | 133, 37,255,159 (745.1) |
| `version` | 0, 504,698 (10.1) | 0, 1,744,933 (34.9) |

Each passes at both points: the answers are the saved values where a slot is accepted and the defaults where none is, the apply order is the container's, and nothing is written.
Every service step of these cases is within T_svc too: the longest is 0.196 ms at 8x8.
The `guard` case passes at both points: seven calls outside the journal reached the port and were refused, and the device saw only the erase inside it.
The boot runs before the loop.
A refusal stands only on two reads of the same bytes ([`ctrl_nvm/README.md`](../../../sw/firmware/ctrl_nvm/README.md#boot), "Boot" item 3), so the `torn` boot reads its refused slot twice, beside the accepted slot and its re-stage.

### The controls

CPU 50 MHz, bus 100 MHz:

| Control | 1x1 | 8x8 |
|---|---|---|
| `reorder-settle` | caught: entry 4 is `aecp_value_restore`, the container needs `aecp_restore_settle` | caught: entry 25 is `aecp_value_restore`, the container needs `aecp_restore_settle` |
| `reorder-bindings` | caught: entry 0 is `aecp_map_restore`, the container needs `acmp_restore_binding` | caught: entry 0 is `aecp_map_restore`, the container needs `acmp_restore_binding` |
| `guard-removed` | caught: `flash write escaped the journal` | caught: `flash write escaped the journal` |
| `slow-step` | caught: `step 0 (idle) takes 30.2216 ms of CPU time, over T_svc 10.0 ms` | caught: `step 0 (idle) takes 30.2139 ms of CPU time, over T_svc 10.0 ms` |
| `step-over-t-svc` | caught in every phase: capture, erase, idle, poll, program, read, seal (T_svc = 500,000 cycles) | caught in every phase: capture, erase, idle, poll, program, read, seal (T_svc = 500,000 cycles) |

## Controls and self-test

Each planted defect is a scratch copy of the saved-state store's tree (`build.Plant`), built and booted like the cases:

| Control | Planted defect | Journal | Caught by |
|---|---|---|---|
| `reorder-settle` | the D3 walk's settle step runs after the names (`nvm_store.c`, its test before the first name removed) | the commit's | the apply order |
| `reorder-bindings` | the binding walk runs after the D3 walk | the commit's | the apply order |
| `guard-removed` | `ls_in_journal` passes every address, in the `guard-probe` arm | blank | the flash model, which refuses a write outside the journal: `flash write escaped the journal` |
| `slow-step` | the store's first service step spins on its own clock until 30 ms past its start (`nvm_store.c`, `nvm_store_service`), in the fixture | blank | T_svc: the step's finding, `step 0 (idle) takes ... over T_svc` |
| `step-over-t-svc` | each phase's longest step of the measured commit stretched to exactly T_svc, then one CPU cycle past it (`target_grade.stretched`) | - | at T_svc no finding is added; one cycle past it adds exactly one, naming that step and its phase |

The step control is planted in the measured commit itself, phase by phase, so it shows that every phase the commit runs is graded.
`slow-step` shows the same of a real step: the firmware's own step, traced as the cases trace every step.

The self-test ([`target_selftest.py`](target_selftest.py)) runs the graders on synthetic logs and the journal builder on the 1x1 shape.
It requires:

- the capture's CPU time to be its steps' cycles and its elapsed time its first step's start to its last step's end;
- a capture of twice 24.5 ms of CPU time, every step within T_svc, to be no finding;
- a missing record to be refused, and every step to be classified by its calls;
- a step of exactly T_svc to pass, and one CPU cycle over it to be a finding naming it and its phase, in every phase;
- that finding to fail its case, and the step control to be caught in every phase;
- the run's report to grade every step against T_svc and give the capture no bound;
- the run's clocks to travel with its results. A synthetic commit at CPU 62.5 MHz and bus 125 MHz:
  - `results.json` must carry those clocks, through JSON;
  - the report must name them beside every table, and none at 50 MHz;
  - its figures must be its cycles at 62.5 MHz;
- a record to be refused when it lacks either clock, when a clock is not a whole positive number of hertz, when it names a CPU clock its figures were not converted at, or when its clocks are not its builds';
- builds that disagree on their clocks, lack one or are none, to be refused;
- `run.py`'s own `main`, on builds recording the 62.5 MHz clocks, to write them to `results.json` and beside every table of `table.md`. It must refuse, with exit 2 and no `table.md`:
  - results graded at another CPU clock than their record names;
  - a run whose clocks are not its builds';
- the container's own apply order to pass, and each of these to be caught: the settle after the names, a binding after the D3 walk, a name before a map, one apply missing, one too many and two boots;
- the derived journals to be judged by the reference codec as the cases need them, and every arm and planted defect to apply to the checkout's sources.

It also holds D5 on the current flash writer.
It runs that writer's own grader, `grade_rows` in [`nvm_capture_cpu/run.py`](../nvm_capture_cpu/run.py), the one `check_nvm_capture.py` regrades its receipt through.
A capture of exactly 24.5 ms must pass, and one system tick more must be refused.

Then it replaces each grading rule in turn with a weaker one, and a named check must fail:

| Mutant | Caught by |
|---|---|
| steps: strictly below T_svc | a step of exactly T_svc passes, in the capture, seal, erase, poll, program and read phases |
| steps: only the capture's steps graded | a step one CPU cycle over T_svc is a finding naming it and its phase, in the capture, seal, erase, poll, program and read phases |
| steps: the idle step not graded | any one step stretched one cycle over T_svc, the idle step among them, is that step alone, its phase kept |
| steps: no step graded against T_svc | a service step over T_svc fails its case, one at T_svc does not |
| step control: the planted cycle not added | the step control: each phase's longest step at T_svc passes and one cycle past it is caught |
| capture: the closing step is not the capture's | the capture's CPU time is its steps' cycles, its elapsed time its first step's start to its last step's end |
| capture: the elapsed time is its CPU time | the same check |
| capture: the current writer's 24.5 ms bound imposed on F1 | a capture of twice 24.5 ms of CPU time, every step within T_svc, is no finding |
| order: settle last whatever the names | the bindings first, then the D3 records in ascending id, settle before the first name |
| order: only the first entry compared | the settle after the names is caught |
| answers: any sequence_id | the answers are read by sequence_id: the name and the talker |
| clocks: the report names the product clocks whatever it was given | a run at other clocks is reported at them: its clocks named, its figures converted at its CPU clock |
| clocks: the last table without its clock line | every table of the report has the clocks beside it |
| clocks: results.json without its clocks | the results record carries the clocks its builds recorded, through JSON |
| clocks: a missing clock not refused | a record without its sys_hz is refused |
| clocks: the figures not checked against the CPU clock | a record whose CPU clock is not the one its figures were converted at is refused |
| clocks: the record not compared with its builds' | run.py refuses a run whose clocks are not its builds', writing no table |
| clocks: the first build's clocks taken for all | builds that disagree on their clocks, lack one or are none are refused |
| clocks: an unconditional 50 MHz and 100 MHz for the run | run.py writes its builds' clocks to results.json and beside every table of table.md |
| the current flash writer: its 24.5 ms check removed from its grader | the current flash writer's capture is held to 24.5 ms: exactly 24.5 ms passes, one system tick more is refused |

The last mutant deletes the check's three lines from `grade_rows`'s source, writes the result to a scratch copy and imports it in place of the grader.
That writer's own gate fails on the same removal: `check_nvm_capture.py` stops at its boundary control, `OFF timing limit was ignored`.

## Limits

- The flash model's erase and program waits are zero (`fw_service_budget/flash.hpp`), so the commit's elapsed time is the store's step pacing, not a part's.
- One phase of each boot is run; the boot path's host suite covers the faults on every read ([`ctrl_nvm/README.md`](../../../sw/firmware/ctrl_nvm/README.md#the-host-suite)).
- The mailbox's datapath is held idle as the CPU budget harness holds it, so the face block's windows are never answered.
- The capture's records come from the fixture's owners as composed; the target platform's own `main` is a later image.

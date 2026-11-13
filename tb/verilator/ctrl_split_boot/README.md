<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Split boot simulation (#665 S3)

This simulation boots the split placement's platform image on the split CPU, from reset to its ready line.
It then compares the boot's CSR writes with `milan_baremetal.c`'s and answers the release grader's commands on the UART.
Its contract is S3's acceptance on [#665](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6493622258): a LiteX simulation boots the split SoC to the ready state, the UART banner and graded commands answer, and a register-write trace shows the CSR initialisation writes exactly what `milan_baremetal` writes for the same shape.

## Contents

- **[Run](#run)** -- The prerequisites, the command, and the regrade.
- **[The SoC and the testbench](#the-soc-and-the-testbench)** -- What is the CPU budget harness's, what this simulation adds, and what the testbench answers.
- **[What is graded](#what-is-graded)** -- The model's own verdict, the boot, the trace, each UART duty, the smoke grader's own checks, and the controls of each.
- **[Results](#results)** -- The two shapes' boot times, traces and UART duties, and the grader's verdicts.
- **[A gate at every sync](#a-gate-at-every-sync)** -- The boot at both points before any leg at every sync, and why.
- **[The platform image against the ledger](#the-platform-image-against-the-ledger)** -- The platform image linked at every point and graded against the memory ledger, and its planted ledgers.
- **[Limits](#limits)** -- What a simulation without the datapath cannot show.

## Run

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator, and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
Keep the build directory outside the checkout:

```sh
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1 --regrade
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-1x1 --placement-controls
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-native --native-controls
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/split-boot-plants --self-test
```

The run generates the shape's flash map with `ctrl_service_budget/build.flash_map` from the split SoC export.
Both platform links use that map, and both boot exports refuse any flash-device placement that differs from it.
The run builds the runtime archives, then links the platform image (`ctrl_plat_image.py`) twice.
The first link is against a provisional map, and the boot SoC's export with that image gives the SoC's own `csr.csv`.
The second link is against that `csr.csv`, and the run refuses it unless the second export's rows equal the first's: the map does not depend on the image.
It then builds the native model, runs it, and saves its exit status beside its log (`sim.status`).
`--regrade` grades the log and the status a run left in the build directory.
`--native-controls` grades the native controls, with no build ([What is graded](#what-is-graded)).
`--placement-controls` runs the placement controls on a finished run in the build directory, with one export for each that needs one.
`--self-test` grades the native controls, then builds and runs each planted control in a planted copy of the firmware's tree, and requires each to be graded a finding of its own kind. It ends with the placement controls, on one of those builds.
Exit 0 is a pass, 1 a finding and 2 a refusal.

## The SoC and the testbench

[`boot_soc.py`](boot_soc.py) builds the CPU budget harness's test SoC ([`split_soc.py`](../ctrl_service_budget/split_soc.py), imported read only):

- the shipping VexiiRiscv with the split placement's instruction and data caches, on the bus clock, `sys`, 100 MHz, with no clock of its own and no crossing (`milan_soc.CTRL_CPU_CD`; #665, owner decision 2026-10-30);
- the flash window uncached and not executable, as the product's split CPU has it (`milan_soc.ctrl_uncached_flash`; #665): an export whose window is another is refused, `its flash window's regions are [...], not ['r']`;
- `milan_soc.add_ctrl_memory` built from the linked image;
- `KL_mbx` behind `KL_mbx_wb`, its datapath on pads, each face commit acknowledged at the contract's bound;
- LiteSPI, its PHY staged as MilanSoC stages it (`milan_soc.stage_spi_phy`, #814), and `timer0` where F1's port addresses them.

The CPU generator is given the shipping split region list, each region as its aligned power-of-two pieces ([#791](https://github.com/kebag-logic/milan-fpga/issues/791)), and that harness refuses a list that is not its own power-of-two cover.
The results below were measured when the harness still widened each region to its cover.
This SoC adds the two devices the platform reaches beyond the mailbox:

- the Milan CSR window, a Wishbone slave at `milan_soc.MILAN_CSR_BASE` named `milan_csr`, whose bus the testbench answers;
- the UART, MilanSoC's own `sim` UART.

[`sim_main.cpp`](sim_main.cpp) drives the clocks and the flash as that harness's testbench does, with a blank flash.
The mailbox's datapath is idle with interface 0's link up.
The CSR window answers from a register file holding builder gate 35's seeded words, ID and VERSION as the datapath's reset values.
`TOD_RD_LO/HI` hold the simulated time of the last snapshot.
After the ready line the testbench types `milan_status`, then `milan_gettime`, waits one millisecond, and types `milan_gettime` again, as the smoke grader does.

## What is graded

[`run.py`](run.py) grades the testbench's log:

- **NATIVE**: the model's own verdict, which no observation before it discharges. Its saved exit status must be 0, and its checker's tally must have completed with no failure, read as the sweep reads a suite log (`scripts/suite_tally.py`). A regrade reads the same saved status, and a run that saved none is a finding.
- **BOOT**: the ready line, exactly one banner (the #396 plan counts boots by their banners), and the boot-to-ready time against the 20 s ADP valid time (Milan v1.2 5.6.2/5.6.3).
- **TRACE**: the window's writes before ready. The first fifteen must equal `configure_fabric()`'s for the same config, compiled on the host as builder gate 35 runs it on the same seeded file ([`plat_trace.py`](../../../sw/firmware/ctrl/test/plat_trace.py)). The next three must be MAAP's one-owner report. No write may set `ADP_CTRL[0]` or `PP_CTRL[0]`.
- **UART**: each command's span, its wait to the first response byte, and its longest gap between two response bytes, which bounds the loop pass that sends them. Each is compared with #397's 500 ms tick rule and the approved T_svc = 20 ms.
- **Native controls** (`--native-controls`, and first in `--self-test`): a stand-in for the model prints a valid boot's observations, then ends in one of six ways. A pass must pass. A nonzero exit, a failed tally, a missing tally, and a failed tally with a nonzero exit must each be a NATIVE finding, on the run and on its regrade. A run whose saved status is gone must pass, and be a NATIVE finding on its regrade.
- **Controls** (`--self-test`): the SoC exported with `milan_soc.ctrl_uncached_flash` made a no-op, as `boot_soc.py` without its call, must be refused by the flash window's check (`PLANT flash-window-cached`); a CSR write skipped (the `LWSRP_VID` write, out of `ctrl_plat_csr.c`) must be a TRACE finding; a console that spins 2,000,000 turns, about 0.55 s, before its `milan_status` response must be a UART finding, its span past #397's tick rule. Each must be found in a run the model completes, with no NATIVE finding, so its observations are a whole run's: the two `milan_gettime` answers do not spin, and the run ends inside its 2 s limit.
- **Placement controls** (`--placement-controls` on a finished run, and last in `--self-test`): `split_soc.map_deviations` must find nothing on the true flash map, and must name a moved register, a register the SoC lacks, a moved window and a resized window. `boot_soc.build` must refuse, in its own words, an export given the map with `spiflash_master_cs` moved four bytes. Each planted defect of that refusal must then let the same map through: the refusal taken out of the build (`guard-removed`), and a `map_deviations` that finds nothing (`deviations-empty`). They need the product LiteX tree, as the boot does, and no hosted job runs them.
- **GRADER**: `baremetal_uart_smoke.py`'s own `grade()` on the three answers. The firmware's checks (`aem-image`, `phc-advances`) must pass. `fabric-enabled` must fail, the listed difference. The checks whose words are the stand-in register file's are printed and never counted.

## Results

The platform image at this head, at the shipping shape and the largest that fits 56 tiles, from the two `run.py` commands above.
Every figure is simulated time, the split CPU and its bus on `sys`, at 100 MHz; the native model completed each run (NATIVE exit status 0, its tally `checks: 1   failures: 0`):

| Shape | Boot to ready | CPU cycles at 100 MHz | Trace | `milan_status` span / first byte / longest gap | `milan_gettime` (worst) |
|---|---:|---:|---|---|---|
| 1x1, one interface | 25.477 ms | 2,547,656 | 18 of 18 equal | 2.600 / 0.467 / 0.119 ms | 0.332 / 0.199 / 0.113 ms |
| 8x8, one interface | 64.584 ms | 6,458,406 | 18 of 18 equal | 4.161 / 0.544 / 0.196 ms | 0.487 / 0.276 / 0.216 ms |

The SoC reads the flash through the product's uncached window, as the split CPU does (#665, 2026-11-02).
At `c954b8a9`, the head before this change, this page recorded 24.660 and 64.271 ms to ready through a cached window, and the window alone moves them to 25.413 and 65.026 ms; the boot reads its slots' headers through it.
The window alone leaves every UART figure as it was.
At `4f58214f` the loop also read the store's clock as each pass starts and ran the store's owed step in a pass that took no input (THE STEP, `ctrl_loop.h`): 25.515 and 64.885 ms to ready, each longest gap 0.013 to 0.018 ms longer than that page's.
At this head the step also has its age limit, and a changed record is marked without walking the records (#665): the boot is 25.477 and 64.584 ms to ready, the 8x8 `milan_status` span 4.161 ms against 3.976 ms, and no verdict moves.

The boot's own figures before the CPU moved, with the platform image still built RV32I without the record mover or the word-wide primitives, and the CPU at 50 MHz, were measured after merging `dev-soft-core` `a68536fa` and giving both platform links and boot exports the generated map (#665, decision 6677095110).
The rows marked staged are the two `run.py` commands above, at `93c6e9a544`: `split_soc.add_devices` stages this SoC's LiteSPI PHY, as `MilanSoC.add_spi_flash` stages the product's (#814).
The rows marked none are the same tree with that one call removed, a control, at `1de390e104`.

| Shape | PHY stage | Boot to ready | CPU cycles at 50 MHz | Trace | `milan_status` span / first byte / longest gap | `milan_gettime` (worst) |
|---|---|---:|---:|---|---|---|
| 1x1, one interface | staged | 84.372 ms | 4,218,617 | 18 of 18 equal | 21.546 / 1.963 / 1.266 ms | 2.527 / 1.239 / 1.268 ms |
| 1x1, one interface | none | 84.362 ms | 4,218,076 | 18 of 18 equal | 21.547 / 1.963 / 1.267 ms | 2.526 / 1.239 / 1.267 ms |
| 8x8, one interface | staged | 184.622 ms | 9,231,088 | 18 of 18 equal | 40.224 / 2.856 / 2.207 ms | 4.053 / 2.132 / 1.858 ms |
| 8x8, one interface | none | 184.611 ms | 9,230,556 | 18 of 18 equal | 40.225 / 2.856 / 2.207 ms | 4.053 / 2.132 / 1.858 ms |

There the stage cost the boot 541 CPU cycles at 1x1 and 532 at 8x8, about 0.01 ms, and moved no UART figure by more than 0.001 ms, in either direction, and no verdict.
The prior measurements at `a68536fa`, on the stand-in flash addresses with the same PHY stage, reached ready at 84.393 and 184.658 ms.
Both boots at this head are within the 20 s ADP valid time.
Every UART duty is within 500 ms, and no response byte waits past T_svc on the one before it.
A response is sent at 16 bytes a pass, so a command's span is about 20 passes of the loop.
The 8x8 image with two interfaces plans 59.5 RAMB36, within the 60.0 the owner's [decision of 2026-11-12](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6824896581) ledgers by name for the flip, owed to lane S14.
At that point the simulation names the platform's override ([A gate at every sync](#a-gate-at-every-sync)).

The smoke grader's verdicts on the simulated UART:

| Check | Verdict | Reading |
|---|---|---|
| `aem-image` | PASS | the firmware's own CRC check of the AEM image |
| `phc-advances` | PASS | the firmware's snapshot read; the time is the testbench's |
| `fabric-enabled` | FAIL | **the listed difference**: the split never sets `ADP_CTRL[0]` or `PP_CTRL[0]`, so a split image fails this check on any board |
| `id-miln`, `version-gptp-publication` | PASS | not evidence: the testbench answers the datapath's reset values |
| `gptp-identities`, `gptp-path`, `gptp-pdelay`, `clkv-fabric-owner`, `gptp-locked` | PASS or FAIL | not evidence: the stand-in register file's words; they need the datapath and a gPTP peer |

## A gate at every sync

The boot runs at both of the lane's points, 1x1 with one interface and 8x8 with two, and at 8x8 with one, on every sync of the S2b branch onto its base (#665: the ruling on round 30's second STOP), before any harness leg starts:

```sh
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-1x1
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-8x8 --shape endstation_ax7101_8x8
python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir /tmp/boot-8x8-if2 --shape endstation_ax7101_8x8 --interfaces 2
```

The merge of `dev-soft-core` `0fb66211` built and linked at every point and passed the firmware's own gates, but its firmware stopped at boot with "mailbox contract mismatch; entity disabled": the record mover still answered a CPU request the cycle after it, and the mailbox now answers a register read two cycles after (#870).
At 8x8 with two interfaces the platform image is the ledgered point: its link names `--ledgered-point platform-8x8-two-interfaces` and the boot SoC plans it to that override's tiles (`boot_soc.PLATFORM_LEDGERED`), and every other point takes no override.
At this branch's head each boot reaches ready, at 26.370 ms (1x1, one interface), 66.017 ms (8x8, one) and 68.371 ms (8x8, two), within the 20 s ADP valid time.

## The platform image against the ledger

[`plat_ledger.py`](plat_ledger.py) links the platform image at the ledger's four points, 1x1 and 8x8 each with one and two interfaces, and grades each against `ctrl_memory.LEDGERED` ([SPLIT_CONTROL_MEMORY.md section 5](../../../docs/design/SPLIT_CONTROL_MEMORY.md#5-fit)).
Each shape's `csr.csv` and flash map are its split SoC export's, from the CPU budget harness's `build.flash_map`, and the runtime archives are this simulation's.
The 8x8 image with two interfaces is linked with `--ledgered-point platform-8x8-two-interfaces`, and every other image with no override.
Each image is graded on four checks, each apart, so that one finding does not hide another:

- `LINK`: `ctrl_plat_image.py` exits 0, and the image's plan with its point's override is accepted;
- `KEY`: the image's `ctrl_plat` is the size `ctrl_memory_ledger.py` records for its point, and at the override's point the image carries every symbol of that override at its listed size;
- `TILES`: the plan, read with no budget, is within its override's tiles, or the 56-RAMB36 budget;
- `LEDGER`: every override of the platform's image is linked at a point.

A stale `ctrl_plat` key refused that image by its key for three rounds of #665, and hid that its plan had passed the tiles its override then held.
So `--self-test` grades seven planted ledgers on the linked images, in its own process, and requires each to give exactly the findings it names: a stale key (`KEY`, `LINK`), a plan past its tiles (`TILES`, `LINK`), both at once (all three), a stale record in `ctrl_memory_ledger.py` (`KEY` at that point), the budget half a tile under the 8x8 one-interface plan (`TILES` there), the override not taken (`LINK`, `TILES`, `LEDGER`) and an override no point links (`LEDGER`).

```sh
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat-ledger --self-test
```

Exit 0 when every point passes and every planted ledger is graded as it requires; 1 for a finding; 2 when a build step is refused.

## Limits

- The datapath is not built: the CSR window is a register file, so the trace shows what the firmware writes, not what a datapath does with it.
- The flash is blank, so the boot's saved-state terminal is BLANK. Valid, torn and wrong-version slots are lane S4's.
- The UART is LiteX's `sim` stream, with no baud rate: a span is CPU and loop time. At 115,200 baud the 305-byte status line takes about 26.5 ms on the wire.
- `fabric-enabled` and the #396 campaign's one BIOS pass per cold cut cannot hold on a split image. The owner's ruling (#665, 6505997821) accepts both as listed differences, and the graders' split mode is owed to the bench lane (S12).

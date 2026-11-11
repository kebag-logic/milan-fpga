<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# REBOOT simulation (#871)

This simulation runs an AECP REBOOT on the split CPU, the end-station reset that follows, and the boot after it.
Its contract is [#871](https://github.com/kebag-logic/milan-fpga/issues/871)'s acceptance (#665 S11).
The firmware's AECP owner answers the REBOOT, and the platform's reset port starts the reset #787 chose ([REBOOT_RESET.md section 8](../../../docs/design/REBOOT_RESET.md#8-the-split-placement)).
The flash keeps its journal across the reset, as the configuration reload boots the same flash.

## Contents

- **[Run](#run)** -- The prerequisites, the command, and what the build shares between images.
- **[The SoC and the testbench](#the-soc-and-the-testbench)** -- The split boot simulation's SoC with two pad groups more, and the reset sequence the testbench stands for.
- **[The runs](#the-runs)** -- The four scripts, from a blank flash to the boot after the reset and the replay after a cut.
- **[What is graded](#what-is-graded)** -- Each grade, its acceptance item and its clause.
- **[Plants and controls](#plants-and-controls)** -- The five planted images and the seven grader controls, each caught by its own finding's words.
- **[Results](#results)** -- The order, the bound, the journal, the restore and the advertisement, as measured.
- **[Limits](#limits)** -- What the simulation does not model.

## Run

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator, and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
Keep the build directory outside the checkout:

```sh
python3 -B tb/verilator/ctrl_reboot/run.py --build-dir /tmp/reboot-1x1
python3 -B tb/verilator/ctrl_reboot/run.py --build-dir /tmp/reboot-plants --self-test --jobs 3
```

The point is the shipping shape, `endstation_ax7101_1x1_tdm8` with one AVB interface.
The build makes, once, the shape's flash map from the split SoC's export, the runtime archives, and the test SoC's `csr.csv` from an export with the checkout's image.
Each image is then the platform image (`ctrl_plat_image.py`) linked against that map, its own export and its native model.
The checkout's image is one; `--self-test` adds each planted image.
Every export runs with `PYTHONHASHSEED` 0, which `run.py` sets itself: LiteX builds the CPU's ISA string from a set, so exports with other seeds can differ in `csr.csv`, and the run refuses an image whose SoC map is not the shared one.
Exit 0 is a pass, 1 a finding and 2 a refusal.

## The SoC and the testbench

[`reboot_soc.py`](reboot_soc.py) builds the [split boot simulation](../ctrl_split_boot/README.md)'s SoC, `boot_soc.py`, imported read only.
Its devices come from `split_soc.add_devices`, which adds the split SoC's own reset port, `milan_soc.add_ctrl_reboot`.
This SoC adds two pad groups:

- `reboot`, the port's CSR level, where the product crosses it into `KL_reboot_ctrl`;
- `gsi`, the face block's GSI window. The split SoC's test mailbox holds every window answer idle, and the AECP owner then refuses SET_STREAM_FORMAT and SET_STREAM_INFO, which read the datapath through it.

[`sim_main.cpp`](sim_main.cpp) drives the clocks, the CSR window and the flash as the split boot simulation does.
The flash erases a sector in 20 ms and programs a page in 0.5 ms, so a journal write spans the loop's ticks.
The testbench drives the mailbox's datapath side from a script.
It answers the GSI window as a datapath whose stream runs no traffic would: every GET_STREAM_INFO word 0, and the format verdict 3, supported.
On the reset port's rise it runs `KL_reboot_ctrl`'s sequence ([`hdl/milan/KL_reboot_ctrl.sv`](../../../hdl/milan/KL_reboot_ctrl.sv)):

| Phase | Ends when | Here |
|---|---|---|
| DRAIN | F_NVM, as the firmware last committed it, says no live writer or nothing accepted outside a slot; else at 10,000 ms | also stopped at 1,000 ms; a write completes in about 400 ms |
| EGRESS | on a tick once the mailbox has sent nothing since the previous tick; else at 3 ms | as the RTL |
| HOLD | the PHY hold rises | 50 ms of the RTL's 3,500 ms, then the run ends at the reload and writes the journal |

## The runs

[`run.py`](run.py) writes four scripts, each a run of the same model:

| Run | Flash | Script |
|---|---|---|
| `reboot` | blank | A REBOOT of a short command, a STREAM_INPUT, a MEMORY_OBJECT and ENTITY 1, then GET_CONFIGURATION. A second controller registers for notifications. Every item is read, set away from its default, and read again. At the erase of the write that saves them, controller 1's REBOOT of ENTITY 0. Once its SUCCESS has left the mailbox, a GET_CONFIGURATION and a BIND_RX, inside the window before the port; a GET_CONFIGURATION and a BIND_RX once the port has fired |
| `after` | `reboot`'s | Every item read, then the first ENTITY_AVAILABLE awaited for 4,100 ms (Milan v1.2 Table 5.50's TMR_DELAY, 0 to 4 s) |
| `cut` | `reboot`'s | Two names set, then a cut after the first page program of the write that saves them |
| `replay` | `cut`'s | The two names read |

The items are the #396 release grader's: Milan v1.2's eight saved items and the binding (`tb/tools/torture_campaign.py`, `RELEASE_PERSISTED_ITEMS`).
The script sets the stream format (5.3.8.1), the presentation time offset (5.3.7.6), a channel mapping removed (5.3.9.1), the clock source (5.3.11.1), both entity names and an object name (5.3.13), and the binding (5.3.8.2).
The shape has one configuration and one AUDIO_UNIT rate, so those two are read and never graded.

## What is graded

| Grade | Acceptance item | What it requires |
|---|---|---|
| NATIVE | | each run's exit status and its checker's tally, read as the sweep reads a suite log |
| REFUSE | 5 | each refused REBOOT answered as IEEE 1722.1-2021 7.4.43 states (BAD_ARGUMENTS, NOT_SUPPORTED twice, NO_SUCH_DESCRIPTOR) at cdl 16, no notification, no reset, and GET_CONFIGURATION answered after them |
| ORDER | 2, 3 | the REBOOT of ENTITY 0 answered SUCCESS; that response, its one notification (7.5.2) and ENTITY_DEPARTING (Milan v1.2 5.6.3.3) leaving the mailbox before the reset port fires, in that order; the port firing at all. As the processor (REQ-FWX-001): the window's BIND_RX reaching the mailbox between the SUCCESS and the port, and neither it nor the window's AEM command answered; no frame but ADP's leaving after ENTITY_DEPARTING, and none after the port; no frame given after the port taken |
| JOURNAL | 4 | the REBOOT inside the write (after its erase, before its last page); the drain ended because the state was durable; after the reset every item reads back as before it; the cut's replay reads one whole snapshot, the saved one or the cut write's |
| RESTORE | 1 | `check_release_state_restored` over the six settable items and the binding; the other two read back unchanged |
| ADP | 1 | an ENTITY_AVAILABLE after the reset, and the REBOOT-to-advertisement time under 20,000 ms (valid_time 10, Milan v1.2 5.6.2) |
| BOUND | | the measured cycles from the REBOOT command's last byte to the reset port, and on to the PHY hold |

## Plants and controls

Each planted image is the platform image built from a copy of the firmware tree with one edit, driven by the `reboot` script.
Each must give a finding that carries its own words:

| Plant | Edit | Its finding |
|---|---|---|
| `reset-before-the-response` | the port written in the take that accepts the REBOOT, before its SUCCESS is handed to send | ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired |
| `request-ignored` | the port never written | ORDER: the reset port never fired |
| `write-torn` | the store not serviced once the loop stops | JOURNAL: the drain ended cap, not because the state was durable |
| `any-descriptor-type` | a REBOOT of any descriptor type taken | REFUSE: refuse-input answered status 0 at cdl 16, not 11 at cdl 16 |
| `frames-taken-after-the-success` | the platform's receive gate open | ORDER: a BIND_RX given after the REBOOT's SUCCESS had left was answered |

Each grader control plants one edit into a clean run's log and must give a finding that carries its words:

| Control | Edit | Its finding |
|---|---|---|
| `response-after-the-port` | the reset port's rise moved to the cycle after the REBOOT arrived | ORDER: the REBOOT's SUCCESS left the mailbox after the reset port fired |
| `frame-after-the-departing` | an ACMP frame one cycle after the first ENTITY_DEPARTING | ORDER: a frame other than ADP's left the mailbox after ENTITY_DEPARTING |
| `drain-at-its-cap` | the drain ended at its cap | JOURNAL: the drain ended cap |
| `no-advertisement` | the boot's ADP frames deleted | ADP: no ENTITY_AVAILABLE after the reset |
| `name-reverted` | the entity name read back changed | RESTORE: the #396 grader says FAIL, `entity_names` |
| `binding-lost` | the binding's talker zeroed | RESTORE: the #396 grader says FAIL, `stream_binding` |
| `replay-mixed` | the replay's object name read as the other snapshot's | JOURNAL: the cut's replay reads ..., a write half applied |

## Results

At the shipping shape, one interface, the split CPU at 50 MHz and its bus at 100 MHz; simulated time throughout:

| Grade | Result |
|---|---|
| REFUSE | BAD_ARGUMENTS, NOT_SUPPORTED, NOT_SUPPORTED, NO_SUCH_DESCRIPTOR, each at cdl 16; no notification, no reset, GET_CONFIGURATION answered |
| ORDER | from the REBOOT command's last byte: SUCCESS at 2.157 ms, its notification at 2.300 ms, ENTITY_DEPARTING at 4.199 ms, the reset port at 4.243 ms; the window's AEM command and BIND_RX reached the mailbox at 2.157 ms and 2.158 ms and neither was answered; no frame but ADP's after ENTITY_DEPARTING, none after the port, and nothing given after the port taken |
| BOUND | this scenario's measurement, not a bound: 424,271 bus cycles, 212,135 CPU cycles, from the command to the port; then 581.124 ms to the PHY hold, the drain ended durable and the egress wait quiet. The firmware stage has no bound while a ring is held ([REBOOT_RESET.md section 8](../../../docs/design/REBOOT_RESET.md#8-the-split-placement)) |
| JOURNAL | the write's erase 62 bus cycles before the REBOOT arrived, its 14 page programs after it; the drain durable; every item back after the reset; the cut's replay reads the saved snapshot whole |
| RESTORE | PASS over the stream format, the presentation time offset, the channel mappings, the clock source, the entity names, the object name and the binding; the configuration (0) and the rate (48,000) read the same and are not graded |
| ADP | 585.367 ms to the PHY hold, 3,500 ms of hold and 3 ms to the IPROG word, then 502.312 ms from the reset to the first ENTITY_AVAILABLE (159.297 ms to ready): 4,590.679 ms of 20,000 ms, 15,409.321 ms left for the configuration load |

The five plants and the seven controls are each caught by their own finding's words.

## Limits

- The datapath is not built. The mailbox's datapath side is the testbench, so "on the wire" is the mailbox's transmit face. From there the path to the MAC is cut-through, and `KL_reboot_ctrl`'s egress wait holds the PHY until every frame given to the MAC has left; `tb/verilator/reboot_ctrl` and `pp_shadow`'s `[RB]` grade it.
- The PHY hold runs 50 ms of its 3,500 ms, and the IPROG word and the configuration load are not simulated. The ADP grade adds the RTL's hold and 3 ms to the measured times, and states the margin left for the configuration load.
- The flash's erase and page times are shorter than the media's. A write spans fewer milliseconds than on the board, and the store's pace between pages is its own.
- The GSI window's answers are a quiet datapath's, not the processor's gather words; they make the two SETs that read the window possible, and nothing else is graded from them.
- One point, the shipping shape. The bench's REBOOT cycles are S12's (#396's `power` area).

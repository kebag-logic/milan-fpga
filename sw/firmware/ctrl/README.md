<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# ctrl: the bare-metal control-plane firmware (#665)

Portable C11 for the on-chip RISC-V, and for a hard core, behind the packet
mailbox ([design](../../../docs/design/MAILBOX_SPLIT.md),
[contract](../../../docs/reference/MAILBOX_CONTRACT.md)). No OS, no heap, no
threads: one event loop, static state, and a static pool behind lwSRP's
allocation port. Lane F0 carries the mailbox driver, the HAL, lwSRP's port
layer, the loop and the ADP slice; the other protocols follow in F1 to F5,
each as its own ports-and-adapters module.

`python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test`
is the gate: exit 0 = every arm passed and every planted defect was caught.

## Contents

- **[Layout](#layout)** -- One directory per layer: wire, driver and HAL, lwSRP's port layer, loop, ADP, the app, the MMIO platform, the host model, the tests.
- **[The host test](#the-host-test)** -- The seven arms, how the processor's ADP stimulus is cut from the pinned submodule and walked, and the planted defects.
- **[Run](#run)** -- The three invocations and what each needs.

## Layout

| Directory | What it holds |
|---|---|
| [`wire/`](wire) | the big-endian wire layer every protocol shares |
| [`mbx/`](mbx) | the generated contract header, the three-function bus port (`mbx_hal.h`), the ring lanes and the driver |
| [`port/`](port) | lwSRP's port layer: `shlan_malloc`/`calloc`/`free` on the static block pool, `shlan_printf` on the debug sink |
| [`loop/`](loop) | the event loop: bounded passes, the TICK fan-out, the bring-up order |
| [`adp/`](adp) | the ADP core (no mailbox), its mailbox adapter with the latency bounds, and `adp_entity.py` |
| [`app/`](app) | the static composition a platform starts |
| [`plat/`](plat) | `mbx_hal.h` on a memory-mapped window (`CTRL_MBX_BASE`, from the SoC's generated `mem.h`) |
| [`host/`](host) | the mailbox model and `mbx_hal.h` on it |
| [`test/`](test) | the host tests and their driver |

## The host test

The driver compiles the firmware for the host exactly as the target
compiles it (`-std=c11 -Wall -Wextra -Werror -pedantic`), into a temporary
directory, and runs these arms:

| Arm | Source | What it shows |
|---|---|---|
| `model` | `model_suite.cpp` | the mailbox suite's checks, which the RTL passes through both adapters, pass on the model too |
| `port` | `test_port_loop.c` | the pool, the debug sink, the driver on the model, the loop's order, bounds and tick fan-out |
| `adp` | `test_adp.c` | the ADP core over fake ports (deferred sends, strays, discards, the two draw kinds), the tag race, the latency bound of every path |
| `walk` | `adp_walk.cpp` | the processor's own ADP walk, reused: 36 cells of its Table 5.51 transcription and its frame builder, on the firmware and the model |
| `entity` | `entity_probe.c` | every shipped config's ADPDU fields, against the fabric's own sources |
| `rv32` | the portable set | a freestanding RV32I build whose only open symbols are C-library string and format functions and libgcc helpers |
| `lwsrp` | `lwsrp_port.c` | with `--lwsrp DIR`: lwSRP's own MRP core on the port layer, through the SRP channel, timed by the fabric's ticks |

### Reusing the processor's stimulus

`ctrl_reuse.py` cuts three things out of the pinned
`protocol-processor/tb/adp_engine/sim_main.cpp` at build time: the fixed
entity configuration, the independent 82-byte `model_frame` builder and the
`ADV` table of Milan v1.2 Table 5.51. It first proves the submodule is one
stage-0 gitlink, checked out at that commit, and that the file's bytes are the
blob the pin records; a marker that is missing or repeated refuses the run.

`adp_walk.cpp` drives the firmware into each cell's state through the
mailbox, applies the row's event as the fabric delivers it, and grades the
cell's end state, draws, arms, cancel rule, frame (byte for byte against
`model_frame`) and available_index. The processor's "DELAY, draw in flight"
column has no firmware counterpart (the firmware draws and arms in one call)
and is reported as not applicable. A stray ('S') is an expiry posted with a
tag the firmware did not issue.

### Planted defects

`--self-test` writes each defect of `ctrl_mutants.py` into a copy of this
tree and requires the arm it names to exit 1 with a `[FAIL]` naming the
check. 28 arms: ADP clause defects caught by the walk (one per walked row), adapter and latency
defects by `adp`, pool, sink, loop and driver defects by `port`, lane and
model defects by `model`, a wrong ADPDU field source by `entity`, and a heap
call by `rv32`.

## Run

```sh
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --lwsrp <lwSRP checkout>
```

Needs a host C and C++ compiler, PyYAML, and for `rv32` the pinned RV32 SDK
(`scripts/ci_rv32_sdk.py`). lwSRP is referenced, never vendored.

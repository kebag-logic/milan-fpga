<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Region-decode simulation (#791)

This simulation runs the split CPU the split SoC generates and probes the edges of its two control regions, `rom` and `sram`.
It is [#791](https://github.com/kebag-logic/milan-fpga/issues/791)'s test.
Each probe fetches or loads at the last word of a region, at each seam between the region's decode pieces, and one word past the region's end.
The probe also reads the CPU netlist's own fetch and load decode at every 32-bit address against the SoC's regions.
The fix it tests is in the [split control memory](../../../docs/design/SPLIT_CONTROL_MEMORY.md#the-cpus-region-decode).

## Contents

- **[Run](#run)** -- The prerequisites, the command, the regrade and the self-test.
- **[The SoC and the probe](#the-soc-and-the-probe)** -- What is the shipping split SoC's, the two things that differ, and what the probe does.
- **[What is graded](#what-is-graded)** -- Each named check, the static decode check, and the two planted decodes with the checks each must fail.
- **[Limits](#limits)** -- What this simulation does not show.

## Run

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator, and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
Keep the build directory outside the checkout:

```sh
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode --regrade
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode-single-mask --mutant single-mask
python3 -B tb/verilator/ctrl_region_decode/run.py --build-dir /tmp/region-decode-self --self-test
python3 tb/verilator/ctrl_region_decode/decode.py "$NETLIST" "$REGIONS"
```

The run links the probe image, exports the test SoC, builds its native model, runs it, and saves its exit status beside its log (`sim.status`).
`--regrade` grades the log and the status a run left in the build directory.
`--mutant` builds one planted decode instead of the shipping one.
`--self-test` builds the shipping decode and both planted decodes, each in its own directory under `--build-dir`.
The shipping decode must pass every check, and each planted decode must fail exactly the checks named for it, in a run that reached its end word.
`decode.py` reads one netlist against one region list (a `soc.json`'s `memory_regions` followed by its `cpu_devices`), with no build.
Exit 0 is a pass, 1 a finding and 2 a refusal.
The directory has no Makefile, for the CPU budget harness's reason: the serial sweep discovers every Makefile, and registering a suite is a CI change.

## The SoC and the probe

[`region_soc.py`](region_soc.py) builds its SoC from the [CPU budget harness's](../ctrl_service_budget/split_soc.py) parts, imported read only.
It uses MilanSoC's own VexiiRiscv path with the DMA port and the split placement's instruction cache, the CPU at the Milan clock and the bus at the system clock.
Its firmware memory is `milan_soc.add_ctrl_memory`, which hands the generator the split regions as their pieces.
The split SoC's other CPU-visible regions are slaves that answer `err`.
They sit at the shipping split SoC's places, in its order: the flash window where LiteX's allocator puts it, the Milan CSR window, then the mailbox.
So the generator is handed the shipping split SoC's region list.
Its single-mask netlist matches, line for line apart from its name, the CPU netlist of the split image that would not boot on the Arty ([#878](https://github.com/kebag-logic/milan-fpga/issues/878)).

Two things differ from the shipping SoC, so the test reads the CPU's decode and nothing else:

- the plan gives each region banks that fill its whole power-of-two window: its decode pieces, then the window's rest. So the region's last word is memory, and so is the word past its end, which the SoC's bus decodes to the same slave. Only the CPU's own decode can refuse that access. The shipping plan populates only the image's need and answers `err` past it; [`test_ctrl_memory.py`](../../../sw/litex/test_ctrl_memory.py) grades that hole;
- the devices the firmware drives are absent: the probe uses only `rom` and `sram`.

[`probe.S`](probe.S) runs the table `run.py` writes (`probe_data.S`), one probe at a time, in machine mode.
Every word probed inside a region is `ret`: `rom`'s are in the image, and the probe stores `sram`'s first.
A fetch calls its address; a load reads it.
Before each probe the program stores the probe's table address to `sram`'s first word, which divides the log into one segment per probe.
A trap of any cause stores `mcause`, `mtval` and `mepc`, then resumes after the probe, so every probe runs.

[`sim_main.cpp`](sim_main.cpp) drives only the clocks, the reset and the idle UART.
At each rising edge of the CPU's clock it prints the committed PC, each trap and its cause, each fetch command on the CPU's bus (an instruction-cache refill), and each data command and response.

## What is graded

[`run.py`](run.py) grades, for `rom` (0 to 0x3_8000) and `sram` (0x1000_0000 to 0x1003_8000):

| Check | Requires |
|---|---|
| a load at its last word reads its word from memory | the load reaches the bus, answers without `err`, reads `ret`, and no trap |
| a fetch at its last word executes it | the word commits, and no trap |
| a load at each seam of its decode pieces | the same, at 0x1_fffc, 0x2_0000, 0x2_fffc and 0x3_0000 from the origin |
| a fetch at each seam of its decode pieces | the same, at those four words |
| a load one word past its end | a load access fault, cause 5, whose `mtval` is that address, and no data command for it on the bus |
| a fetch one word past its end | an instruction access fault, cause 1, whose `mtval` and `mepc` are that address, and no fetch command for its line on the bus |

It also requires the probe to run every probe and store its end word, with the model's exit status 0.

**DECODE.** [`decode.py`](decode.py) reads the netlist's two fault terms: `FetchL1Plugin_logic_ctrl_pmaPort_rsp_fault` for a fetch, and `LsuCachelessPlugin_logic_onPma_port_rsp_fault` for a word load.
It reads every assign they use, inlined.
The address appears only masked by constants, so each term reads only those mask bits; a region's membership reads only the bits from the lowest set bit of `origin | size` up.
Evaluating every combination of the union of those bits decides each term at all 2^32 addresses.
The fetch term must admit exactly the regions with `x` in their mode, and the load term exactly the regions with `r`, the CPU's own CLINT and PLIC included.
Stores are not graded: at the pinned generator the data port admits a store wherever it admits a load, whatever the region's mode.

**Planted decodes.** Each must fail exactly these checks:

| Mutant | What the generator is handed | Must fail |
|---|---|---|
| `single-mask` | the whole regions (`split_soc.CpuPatches` `as-built`), the decode of #791 | `rom`'s seam load and seam fetch (0x1_fffc and 0x2_fffc have bit 15 set), DECODE fetch and DECODE load |
| `cover` | each region at its power-of-two cover, the boot harness's old workaround | the four past-the-end checks, DECODE fetch and DECODE load |

Under `single-mask`, `rom`'s last word, 0x3_7ffc, has bit 15 clear and is admitted.
The netlist's `sram` terms are exact, as `decode.py` shows.

## Limits

- The test SoC's banks are not the shipping plan's: the CPU's decode is generated from the region list and does not depend on them.
- Stores, and transfers other than a word, are not graded.
- No firmware of the product runs here; the [split boot simulation](../ctrl_split_boot/README.md) boots it on the same CPU.

# Split placement control memory

Status: **M8a-1 implemented** behind `--ctrl-mailbox` (#640 lane M8a, plan L11a).
The split image's boot, service checks and route are M8a-2, after F-INT PR 2 (#665).
The all-fabric shipping default is unchanged and keeps its BIOS.

In the split placement the control firmware owns the CPU's reset entry and runs from block RAM.
No BIOS ROM or BIOS SRAM is built there.
[`ctrl_memory.py`](../../sw/litex/ctrl_memory.py) is the one statement of the map, the bank plan and the checks.
[`milan_soc.py`](../../sw/litex/milan_soc.py) builds the memory from the linked image (`CtrlMemory`, `add_ctrl_memory`).

## Contents

- **[1. Memory map](#1-memory-map)** -- The two firmware regions, what each section of the image occupies, and why each region spans the whole budget.
- **[2. Block RAM from the image](#2-block-ram-from-the-image)** -- Power-of-two banks of RAMB18 granules, the error answer past the last bank, and the build switch.
- **[3. Named refusals](#3-named-refusals)** -- The checks every image passes before any block RAM is built, and the three planted controls.
- **[4. Boot console and diagnostics](#4-boot-console-and-diagnostics)** -- What the split image loses and keeps without a BIOS, and DDR3 until the wrapper is removed.
- **[5. Fit](#5-fit)** -- Linked spans and block RAM at the four points, mapped out of context, and the ledger rows.
- **[6. Reproduce](#6-reproduce)** -- The link, the plan, the mapping and the test.
- **[7. The CPU's instruction cache](#7-the-cpus-instruction-cache)** -- The split CPU's fetch L1: its parameters and why, its block RAM and logic against the ledger, the region decode, and the requirement it conflicts with.
- **[8. The CPU's multiply and divide](#8-the-cpus-multiply-and-divide)** -- The split CPU's RV32M, the image built and audited for it, its logic out of context, and the requirement amended for it.
- **[9. The CPU's data cache](#9-the-cpus-data-cache)** -- The split CPU's LSU L1: its size from the composed bursts, why it is coherent, the windows it never caches, its area against the ledger, and the requirement amended for it.

## 1. Memory map

| Region | Origin | Size | Holds |
|---|---|---:|---|
| `rom` | `0x0000_0000`, the CPU's reset address | 224 KiB | `.text` with the reset entry first, `.rodata`, the initial bytes of `.data` |
| `sram` | `0x1000_0000` | 224 KiB | `.data`, `.bss`, the 8 KiB stack |

Both origins are LiteX's VexiiRiscv `rom` and `sram` origins.
`add_ctrl_memory` refuses a CPU whose reset address or `sram` origin differs.
Every other region keeps its origin and size: `main_ram`, `spiflash`, `milan_csr`, `ctrl_mbx` and `csr`.
The split CPU sees `spiflash` uncached and not executable ([section 9](#9-the-cpus-data-cache)).

Each region spans the whole 224 KiB budget.
The VexiiRiscv netlist is generated from the region list, so it does not depend on the image.
Both shipped shapes elaborate the same CPU netlist.

[`ctrl_split.ld`](../../sw/firmware/ctrl/plat/ctrl_split.ld) links the firmware into these regions.
It includes `regions.ld`, which `ctrl_memory.py regions` writes.
[`ctrl_split_start.S`](../../sw/firmware/ctrl/plat/ctrl_split_start.S) is the reset entry.
It sets the stack, copies `.data` from its initial bytes in `rom` and clears `.bss`.
A CPU reset therefore re-enters with power-on state.

## 2. Block RAM from the image

`ctrl_memory.plan` reads the linked ELF.
The `rom` need runs to the last initial byte; the `sram` need runs to the top of the stack.
Each need is rounded up to 2,048-byte granules, one RAMB18 of 512 32-bit words.
The granule count's binary digits are the banks, largest first.

Each bank is LiteX's own `wishbone.SRAM` of power-of-two depth.
It maps to whole block RAMs with no rounding.
A region therefore wastes less than one granule.
Largest first keeps every bank aligned to its own size, so the bank decode is a compare of high address bits.
An address of the region past the last bank answers `err` at once instead of aliasing a bank.

`rom` is read-only and initialised with the image; `sram` is uninitialised.
The Builder then builds no BIOS: `add_ctrl_memory` sets LiteX's own `integrated_rom_initialized`.
`main()` does not add the shipping firmware library, which has no BIOS to link into.

`--ctrl-mailbox` requires `--ctrl-firmware <elf>`, and `--ctrl-firmware` alone is refused.
The default build passes neither, and its export is digest-identical to the base (section 5).

## 3. Named refusals

Every refusal raises `ctrl_memory.Refusal`, whose `check` names it and whose `rule` names the rule that refused.
`ctrl_memory.RULES` registers each rule, and this table lists the same rules in the same order:

| Check | Rule | Refuses |
|---|---|---|
| `reset entry` | `entry address` | An image entering anywhere but `rom`'s first byte |
| `reset entry` | `entry bytes` | An image with no initial bytes at the reset address |
| `reset entry` | `cpu origins` | A CPU whose reset address or `sram` origin is not this map's |
| `memory map` | `elf class` | A file that is not a little-endian ELF32 file |
| `memory map` | `elf machine` | An ELF32 file for a machine other than RISC-V |
| `memory map` | `elf truncated` | A header, table, name or load segment running past the end of the file |
| `memory map` | `outside regions` | A section outside both regions |
| `memory map` | `loads outside rom` | Initial bytes loading outside `rom`, the only region the bitstream initialises |
| `memory map` | `load coverage` | A section with initial bytes that the load segments' file bytes, which program `rom`, do not all carry |
| `memory map` | `nobits in rom` | A NOBITS section in `rom`, which the firmware cannot write |
| `memory map` | `writable in rom` | A writable section with initial bytes running in `rom`, which drops its writes |
| `memory-map overlap` | `regions` | The two regions sharing an address |
| `memory-map overlap` | `addresses` | Two sections sharing an address |
| `memory-map overlap` | `initial bytes` | Two sections sharing a load address |
| `allocation over budget` | `budget` | Banks totalling more than 56 RAMB36, a RAMB18 counting half |
| `staging buffer` | `stage symbol` | An image with no `nvm_stage` |
| `staging buffer` | `stage size` | An `nvm_stage` that is not the selected shape's stage: its KLJ2 container plus one record header |

The budget is the owner's 224 KB at 4,096 usable bytes per RAMB36 (#640 ruling 6101485877).
An allocation of exactly 56.0 RAMB36 is accepted; 56.5 is refused.
`rom`'s contents are the load segments' file bytes and nothing else.
So `entry bytes` reads them as well as the sections: the first word at the reset address must be in them.
`load coverage` requires them to carry every byte of every section with initial bytes.
`add_ctrl_memory` checks the CPU's origins, then reads and plans the image, which runs every other rule but the two staging rules.
`main()` runs the staging check before any export; the shape comes from `--entity-gen-dir`.

[`test_ctrl_memory.py`](../../sw/litex/test_ctrl_memory.py) plants a defect for every rule and requires that rule to refuse it.
It also requires this table to equal `ctrl_memory.RULES`.
For every rule it rebuilds the code with that rule removed or weakened, and requires a named failure.

The three planted controls fail by name in the test and in the SoC build itself.
The test drives `milan_soc.py`'s own `main()` on the shipping 1x1 config's argv, with ELFs it writes:

- an allocation over budget, 58 RAMB36, refused by `budget`;
- a memory-map overlap, `.bss` at `.data`'s address, refused by `addresses`;
- a staging buffer of another shape, the 8x8 stage in the 1x1 build, refused by `stage size`.

A fourth case empties the reset segment's file bytes and keeps its section, refused by `entry bytes`.
Each is refused before any Verilog or init file is written.
`--ctrl-mailbox` alone and `--ctrl-firmware` alone are each refused.
The passing split export holds the image's banks and no BIOS ROM or SRAM, and its `rom` banks hold the image.

The same three controls, on the firmware linked at `c20ed894`, were also run once through the SoC build:

- an allocation over budget: the 8x8 two-interface image with a 16 KiB stack, 56.5 RAMB36;
- a memory-map overlap: `.bss` linked at `.data`'s address, which GNU ld accepts;
- a staging buffer of another shape: the 1x1 image in an 8x8 build, 3,344 against 13,264 bytes.

## 4. Boot console and diagnostics

The split image loses:

- the LiteX BIOS and its console: banner, memory, flash, SDRAM and boot commands;
- the BIOS DDR3 initialisation (`sdram_init`);
- the shipping firmware's UART commands, because `libmilan_baremetal` is not linked.

It keeps the UART, `timer0`, `ctrl` (reset, scratch, bus errors) and the identifier memory.
It also keeps the `ppmem` observer and every Milan CSR.
Any console in the split image is the control firmware's.

The CSR map is unchanged: a split export's `csr.csv` equals the base `--ctrl-mailbox` export's.
Only the `rom` and `sram` region sizes differ.

DDR3 stays instantiated under `--ctrl-mailbox` at this base.
`KL_pp_shadow` is still instantiated, and its three processor memory masters reach the window in `main_ram`.
With no BIOS, the DFI never makes the 1 to 0 to 1 hand-back that `pp_mem_gate` waits for.
Those masters are therefore refused safely, as before DDR3 training.
F-INT PR 2 removes the wrapper in the split build; M8a-2 then routes the split without DDR3.

## 5. Fit

The image is the full F0-F5/F1 composition, linked by `ctrl_srp_image.py --with-aecp --layout split` with an 8 KiB stack.
It holds the descriptor image (7,512 / 19,520 B), the shape's `nvm_stage` (3,344 / 13,264 B) and the lwSRP pool.
The figures below link the firmware of `8ab2b539`, which carries dev `c6bd08c6`: F-INT's publication writers and lwSRP `08ee86e8`.
Mapped out of context by `syn/ooc/ctrl_memory_ooc.py`: Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`.

| Point | `rom` need, B | `sram` need, B | Planned RAMB36 equivalents | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT cells / FF | Byte floor |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 96,624 | 45,776 | 35.5 | 34 / 2 | 35.0 | 128 / 8 | 35 |
| 1x1, two interfaces | 98,056 | 57,152 | 38.0 | 37 / 1 | 37.5 | 89 / 7 | 38 |
| 8x8, one interface | 110,344 | 86,336 | 48.5 | 46 / 2 | 47.0 | 417 / 42 | 48 |
| 8x8, two interfaces (largest) | 111,848 | 112,464 | 55.0 | 53 / 2 | 54.0 | 266 / 34 | 55 |

"Planned" is `ctrl_memory.plan` with every bank in block RAM.
The banks hold 97.2 to 99.8 percent of their bytes.
The byte floor is the flat linked span at 4,096 B per RAMB36, rounded up.
Every point is within the 56-RAMB36 budget.
The largest leaves 2 tiles as mapped.
The budget check reads the planned 55.0, so its banks can grow 4 KiB (1.0 tile) before it is refused; with the unused bytes inside them, 5,064 B.

Two Vivado optimisations put the ROM below its plan:

- it trims a ROM bit column that is constant across a bank, so `16384x31` takes 15 RAMB36 and one RAMB18;
- it maps a small or sparse ROM bank into logic: the 1,024-word bank at 8x8 with one interface, and the 512-word bank at 8x8 with two interfaces.

At 1x1 every `rom` bank is in block RAM.
At 8x8 that logic, with the `rom` region's bank decode and read multiplexer, is most of each point's LUT cells: 327 of 417 with one interface, and 169 of the largest point's 266.
A LUT cell is one LUT primitive, as `ctrl_memory_ooc.py` counts them; `report_utilization` gives 161 Slice LUTs for the largest point's `rom` region.
The decode and multiplexer are not free: two `rom` banks with none in logic take 36 LUT cells, and the largest point's five `sram` banks 97.
The `sram` banks map exactly as planned, and their LUT cells are the bank decode and read multiplexer.
LiteX's memory emitter carries no `ROM_STYLE`, so the build keeps Vivado's default.
Forcing the logic bank into block RAM would recover only that bank's share of the 169, which this mapping does not separate.
M8a-2's route weighs that share against at most 1.0 tile.

The firmware of `ce10328c`, on dev `ac2c5e77`, planned 35.0 / 38.0 / 48.5 / 54.5 and mapped 34.0 / 37.5 / 47.0 / 53.0 tiles at the same points.
Dev `c6bd08c6` added 1,792 B of `.text` and 264 B of `.bss` at the largest point, and its `rom` gained a fifth bank.

Before: the base image's BIOS ROM took 16 RAMB36 and its SRAM 2, measured at `e8454e27`.
One LiteX SRAM of the whole need of that revision's largest image, 221,728 B, took 64 RAMB36.
The ledger rows are in the [plan](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger): 114 tiles after the split's release.

## 6. Reproduce

Link the image with the fixture, then plan it:

```sh
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
```

`ctrl_image_runtime.py` builds the runtime archives; see the [control firmware](../../sw/firmware/ctrl/README.md#linked-size).

Map the regions out of context with the LiteX interpreter and Vivado:

```sh
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
```

Build a split SoC by adding `--ctrl-mailbox --ctrl-firmware "$OUT/ctrl_app.elf"` to a shipping export.

The test runs in the LiteX aggregate:

```sh
python3 sw/litex/test_ctrl_memory.py
```

## 7. The CPU's instruction cache

The split placement's CPU fetches through an L1 instruction cache ([#665 S2c](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860), owner decision of 2026-10-26).
`milan_soc.ctrl_cpu_args` hands the pinned VexiiRiscv generator its own fetch L1 options, under `--ctrl-mailbox` only.
The all-fabric CPU's arguments are unchanged, so its netlist and every shipped config's export are too.
The [split service budget](../../tb/verilator/ctrl_service_budget/README.md#the-instruction-cache) measures it.

| Parameter | Value | Reason |
|---|---|---|
| Size | 4 KiB: 64 sets | The knee of the measured sweep: 8 KiB costs one more tile for about 2 % on the longest pass of the backlog windows that released their load; the composed maximum, a lower bound at every size, does not rank the sizes |
| Ways | 1, direct-mapped | Two ways cost half a tile more at the same size |
| Line | 64 bytes | The generator's fixed `FetchL1Plugin` line at the pinned revision; a refill is sixteen 32-bit beats on the CPU's peripheral bus |
| Refills | one at a time, no prefetch | The generator's defaults; the next-line prefetcher needs a second refill slot |
| Data cache | none when this cache was chosen; [section 9](#9-the-cpus-data-cache) adds one | With the DMA port, an LSU L1 makes the generator build its coherent interconnect and hub instead of [patch 0005](../../sw/litex/patches/0005-vexiiriscv-cacheless-litex.patch)'s non-coherent fabric. The data side's measured cost was mostly byte-loop stores to `sram`, which the firmware removed first. |

Every executable region is cacheable: `rom`, `sram` and, while DDR3 is built, `main_ram`.
The flash window was too, until the data cache made it neither cacheable nor executable for the split CPU ([section 9](#9-the-cpus-data-cache)).
So the cache never fetches uncached.
The cache adds no region and changes none.
Its region check is the cacheless fetch's expression, read at the cache's own fetch stage.
The non-power-of-two `rom` and `sram` decode of [#791](https://github.com/kebag-logic/milan-fpga/issues/791) is therefore the same with and without the cache, and stays #791's.

Out of context, Vivado 2026.1 with `AreaOptimized_high` on `xc7a100t-fgg484-2`, the product split CPU netlist the `--ctrl-mailbox` export reads:

| CPU | LUT | FF | RAMB36 / RAMB18 | Tiles | Routed WNS / WHS at 20 / 10 ns |
|---|---:|---:|---:|---:|---:|
| Split, cacheless (base `e76a755a`) | 3,091 | 5,017 | 2 / 5 | 4.5 | +0.305 / +0.064 ns |
| Split, 4 KiB instruction cache | 3,082 | 5,190 | 3 / 6 | 6.0 | +0.607 / +0.003 ns |
| Difference | -9 | +173 | +1 / +1 | +1.5 | |

The cache's tiles are the CPU's, outside `rom` and `sram`, so the 56-RAMB36 firmware allocation is unchanged.
They are debited in the [plan's ledger](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger): 1.5 tiles, in the split only.
The route closes at the shipping clocks, the CPU at 50 MHz and its bus at 100 MHz; the integrated route is M8a-2's.

The owner amended [NFR-SCOUT-01](../reference/FR_NFR.md#34-fabric-scale-out-and-future-ports) for this cache on 2026-10-27 ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434741232), [correction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6434744436)), following the 2026-10-26 decision that the cache is the first approach.
It had required "one cacheless RV32I control hart", which this cache contradicted.
It then required one RV32I control hart: in the split placement with a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement cacheless.
Section 8 records the later amendment for the split hart's multiply and divide.
Any change to the cache's geometry, or a data cache, needs the owner's decision again.

## 8. The CPU's multiply and divide

The split placement's CPU has RV32M ([#665 S2b round 3](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6445197853), owner decision of 2026-10-27).
`milan_soc.CTRL_MULDIV` adds the pinned VexiiRiscv generator's `--with-mul --with-div` to `ctrl_cpu_args`, under `--ctrl-mailbox` only: its `MulPlugin`, and its `DivPlugin` at the generator's defaults, a radix-2 divider built for area.
The ISA does not depend on the cache, so the harness's cacheless and sweep arms (`--fetch-l1 none`, `SETSxWAYS`) keep RV32M and run the same image.
The all-fabric CPU's arguments are unchanged, so its netlist is too; [`test_soc_options.py`](../../sw/builder/test_soc_options.py) proves both, with eleven planted controls.

The split image is built for it.
`ctrl_srp_image.py --layout split` compiles and links with `-march=rv32im` (`ctrl_build.SPLIT_RV32_FLAGS`).
It refuses an object without the RV32IM attribute, an object that calls a software multiply or divide helper (`fw_rv32.muldiv_findings`), and a linked ELF that is not RV32IM.
The flat layout and `ctrl_image.py` stay RV32I.
So every 32-bit multiply and divide of the split image is an instruction.
The saved-state store's clock (`ls_now_us`), lwSRP's `parse_pass` and LeaveAll draw, MAAP's and ADP's random draws, AECP's controller monitor and map commands, and the pool's index arithmetic no longer call `__udivsi3`, `__umodsi3` or `__mulsi3`, and SRP's `declare_sources` no longer calls `__muldi3`.
At the shipping 1x1 point the image calls one runtime helper still, `__lshrdi3`, at nine call sites: tsn-c-stack's `wire_put_be` (`include/wire.h`) shifts its value as 64 bits, in its five out-of-line copies and where the SRP glue inlines it.
Removing that shift is the stack's change, not this placement's.

Out of context, Vivado 2026.1 with `AreaOptimized_high` on `xc7a100t-fgg484-2`, the product split CPU netlist the `--ctrl-mailbox` export reads at the shipping 1x1 config, both netlists exported from the same image so that only the extension differs:

| CPU | LUT | FF | DSP48E1 | RAMB36 / RAMB18 | Tiles | Routed WNS / WHS at 20 / 10 ns |
|---|---:|---:|---:|---:|---:|---:|
| Split, 4 KiB instruction cache | 3,082 | 5,190 | 0 | 3 / 6 | 6.0 | +0.607 / +0.003 ns |
| Split, 4 KiB instruction cache and RV32M | 3,481 | 5,433 | 4 | 3 / 6 | 6.0 | +0.826 / +0.073 ns |
| Difference | +399 | +243 | +4 | 0 / 0 | 0 | |

The first row reproduces section 7's cached CPU exactly.
The extension adds no block RAM, so neither the 56-RAMB36 firmware allocation nor the [plan's ledger](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger) changes; its logic and its four DSP slices are the CPU's, in the split only.
Both routes complete with no routing error and close at the shipping clocks, the CPU at 50 MHz and its bus at 100 MHz; the integrated route is M8a-2's.

The owner amended [NFR-SCOUT-01](../reference/FR_NFR.md#34-fabric-scale-out-and-future-ports) for this extension on 2026-10-27 ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6445197853)).
It had required one RV32I control hart in both placements.
It then required one control hart: in the split placement it is RV32IM, with a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and no data cache; in the all-fabric placement it is RV32I and stays cacheless.
[The architecture](../ARCHITECTURE_HW_SW_SPLIT.md) repeated that wording.
Any other extension, or M on the all-fabric hart, needs the owner's decision again.
Section 9 records the later amendment for the data cache.

## 9. The CPU's data cache

The split placement's CPU has an L1 data cache ([#665 S2b round 4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6460942408), owner decision of 2026-10-28).
`milan_soc.CTRL_LSU_L1` adds the pinned VexiiRiscv generator's `--lsu-l1 --lsu-l1-sets=128 --lsu-l1-ways=1` to `ctrl_cpu_args`, with the instruction cache, under `--ctrl-mailbox` only.
The harness's cacheless arm (`--fetch-l1 none`) has neither cache.
The all-fabric CPU's arguments are unchanged, so its netlist is too; [`test_soc_options.py`](../../sw/builder/test_soc_options.py) proves both, with seventeen planted controls.

| Parameter | Value | Reason |
|---|---|---|
| Size | 8 KiB: 128 sets | The smallest size measured to drain the composed bursts within T_svc at a burst of 2; the owner kept it with today's bursts, below |
| Ways | 1, direct-mapped | At 4 KiB two ways gain 0.67 ms on the composed window; 8 KiB direct-mapped gains 1.35 ms |
| Line | 64 bytes | The generator's `LsuL1Plugin` line at the pinned revision |
| Coherency | the generator's hub, with the DMA port | Below |
| Uncached windows | `ctrl_mbx`, `milan_csr`, `csr`; `spiflash`, which is no longer executable either | Below |

### Coherent with the DMA port

The protocol-memory bridges reach LiteDRAM through the CPU's DMA slave.
With an LSU L1, patch 0005 keeps the generator's coherency (`lsuL1Coherency`), so the generator joins that slave, the fetch L1 and the data L1 in its coherent bus behind a hub (`Soc.scala`, `splited.wc`).
The hub probes the data cache before a DMA access completes: a DMA write cannot leave a stale line in the CPU, and a DMA read sees a line the CPU holds dirty.
That is the generator's own fabric, unchanged.

The non-coherent alternative is not this generator's.
Its non-coherent split fabric (`splited.nc`) attaches no DMA port, so the protocol-memory bridges would lose their path to LiteDRAM.
Keeping the DMA window uncached by region instead is refused too: with an LSU L1 the generator rejects an uncached memory-bus region (patch 0005's assertion).
Either would need further generator patches.
Coherency costs speed, not safety: through the hub the fetch L1's refills take longer.
Measured on contract 2.2's bursts at 1x1, the ACMP command behind a full ACMP ring took 10.82 ms on a coherent 4 KiB data cache, and 9.45 ms on the same cache without the DMA port, which is not a product CPU.

### The windows it never caches

- **`ctrl_mbx`, `milan_csr` and `csr`** are `rw` peripheral regions without the cacheable flag, as before.
  The data cache sends every access to them to its IO bus, one at a time and in program order, so every ring word, register and doorbell is read and written at the fabric.
- **`spiflash`** is the one region this cache changes.
  The saved-state store reads the flash through the window, then erases and programs it through the LiteSPI command master, which no cache sees ([`nvm_flash_litespi.c`](../../sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c)), and blank-checks and verifies it through the window again.
  A line the cache held before an erase would read stale after it.
  `milan_soc.ctrl_uncached_flash` therefore hands the generator the window without its cacheable flag (`r,p`), so every flash read is an IO access.
  LiteX's rule that a region outside its IO region is cached is a rule for CPUs whose caches follow the IO region alone; VexiiRiscv takes each region's cacheability from its region list.
  The window also stops being executable: the split image runs from `rom` ([`ctrl_split.ld`](../../sw/firmware/ctrl/plat/ctrl_split.ld)), so a fetch from flash faults instead of running uncached, and section 7's rule that every executable region is cacheable still holds.
  The harness's labelled hybrid-XIP arm executes from the flash on its own test SoC; an XIP placement would need the window cacheable for fetch, so it needs its own decision.
- **`rom`, `sram` and `main_ram`** are cached.
  Only the CPU writes `sram`, and nothing writes `rom`; `main_ram` is the DMA's target and is coherent through the hub.

### Size, from the composed bursts

The [CPU budget harness](../../tb/verilator/ctrl_service_budget/README.md#backlog-rows) offers every receive channel its admitted burst at once, with fifteen grandmaster changes.
At 8x8 with two interfaces the last record it releases is SRP's, which takes a record only once the window's events are taken.
On contract 2.2's bursts no size measured drains it within T_svc: with a 16 KiB cache the composed rows still miss at both points.
At the smaller bursts the harness measured for the owner's other 2026-10-28 decision, the last SRP record of the 8x8 composed window is released after:

| Bursts | Data cache | ms |
|---|---|---:|
| ADP, AECP and SRP 2; ACMP and MAAP 3 | 4 KiB | 11.58 |
| the same | 4 KiB, two ways | 10.91 |
| the same | 8 KiB | 10.23 |
| the same | 16 KiB | 9.89 |
| every channel 2 | 4 KiB | 10.59 |
| every channel 2 | 8 KiB | 9.45 |

8 KiB is the smallest size that fits, with every channel's burst at 2.
The owner did not adopt those bursts ([decision of 2026-10-28](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6474448683)): contract 2.2's admission stays, so nothing it admits today is dropped.
At a burst of 2 the harness's own command sequences were refused at ingress, 19 to 31 a run.
Among them were back-to-back AECP and ACMP commands and an ENTITY_DEPARTING of a bound talker, and 4 of 16 controllers missed their notification.
The same decision keeps this cache at 8 KiB with today's bursts.
There it takes 10 to 22 % off the composed rows that the CPU's work decides, and leaves the rest to the CPU clock.
The harness observes this CPU's loads and stores at its data cache's IO bus, which carries every mailbox access; cached accesses never reach a bus it observes.

### Area

Out of context, Vivado 2026.1 with `AreaOptimized_high` on `xc7a100t-fgg484-2`, the product split CPU netlist the `--ctrl-mailbox` export reads at the shipping 1x1 config:

| CPU | LUT | FF | DSP48E1 | RAMB36 / RAMB18 | Tiles | Routed WNS / WHS at 20 / 10 ns |
|---|---:|---:|---:|---:|---:|---:|
| Split, 4 KiB instruction cache and RV32M (section 8) | 3,481 | 5,433 | 4 | 3 / 6 | 6.0 | +0.826 / +0.073 ns |
| and a 4 KiB data cache, measured, not chosen | 4,511 | 7,321 | 4 | 5 / 11 | 10.5 | +0.443 / +0.075 ns |
| and the 8 KiB data cache | 4,544 | 7,321 | 4 | 6 / 11 | 11.5 | +0.291 / +0.066 ns |
| Difference, 8 KiB data cache | +1,063 | +1,888 | 0 | +3 / +5 | +5.5 | |

The data cache's own bank is two RAMB36.
Its coherent fabric adds the rest: a second clock-domain crossing from the CPU to the bus, one for the cached and one for the IO side, each a RAMB36 and a RAMB18, and the hub's RAMB18.
Both routes complete with no routing error and close at the shipping clocks, the CPU at 50 MHz and its bus at 100 MHz; the integrated route is M8a-2's.

The tiles are the CPU's, outside `rom` and `sram`, so the 56-RAMB36 firmware allocation is unchanged.
They are debited in the [plan's ledger](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger): 5.5 tiles, in the split only.
That leaves the ledger 0.5 tiles below its 121.5-tile ceiling after the conditional release, and over it with every bank in block RAM or at the full 56-tile allocation.

The owner amended [NFR-SCOUT-01](../reference/FR_NFR.md#34-fabric-scale-out-and-future-ports) for this cache on 2026-10-28 ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6460942408)).
It had required no data cache on the split hart.
It now requires one control hart: in the split placement it is RV32IM, with a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and an 8 KiB direct-mapped data cache (64-byte lines), coherent with the DMA port, with the mailbox, CSR and flash windows uncached; in the all-fabric placement it is RV32I and stays cacheless.
[The architecture](../ARCHITECTURE_HW_SW_SPLIT.md) repeats that wording.
Any other geometry, or a data cache on the all-fabric hart, needs the owner's decision again.

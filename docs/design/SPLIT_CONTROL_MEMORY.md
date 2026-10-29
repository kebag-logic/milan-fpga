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
- **[10. The CPU clock the composed rows need](#10-the-cpu-clock-the-composed-rows-need)** -- The composed rows measured against the CPU clock alone and with its bus, the rows no clock moves, timing out of context, and what is left at the highest clock that closes.
- **[11. The firmware's work on the record paths](#11-the-firmwares-work-on-the-record-paths)** -- What the AECP and SRP record paths executed, the indexed AECP scans, the SRP copies kept until they change, the hot code placed first, and the composed rows after them at 100 MHz and at 150 MHz.

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
There it takes 10 to 22 % off the composed rows that the CPU's work decides, and leaves the rest to the CPU clock ([section 10](#10-the-cpu-clock-the-composed-rows-need)).
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

## 10. The CPU clock the composed rows need

The owner kept this cache and contract 2.2's admission, and asked for the split CPU clock that brings every composed row within T_svc, measured before the product clock is set ([decision of 2026-10-28](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6474448683)).
The rows are the [CPU budget harness](../../tb/verilator/ctrl_service_budget/README.md#backlog-rows)'s four backlog groups, at 1x1/1if and 8x8/2if, in arms A and B, with both caches.
No clock brings them all within T_svc.
This section is the measurement; the product clocks are unchanged, the CPU at 50 MHz and its bus at 100 MHz.

### What a faster clock has to move

- `_CRG` drives the CPU's `cpu_clk` from `milan`, which the Milan datapath shares, and that datapath's time base is cycle arithmetic on the clock's frequency.
  A faster CPU alone therefore needs a PLL output of its own.
- `rom` and `sram` sit on the bus, `sys`, behind the generator's crossing, so every instruction and data line refill crosses it and waits on the bus clock.
  LiteDRAM's PHY runs at four times that clock (`sys4x`).
- That PLL has one output left, and every output is an exact division of its VCO.
  The VCO must also give the bus's 100 MHz, `milan`'s 50 MHz, the PHY's 400 MHz and the 200 MHz IODELAY reference, so it is 800, 1200 or 1600 MHz.
  Above 100 MHz that leaves 120, 150, 160 and 200 MHz; the 112.5, 125 and 140 MHz points below are measurements only.

### Method

The harness runs with three labelled test-only variants, none in the tree:

- the CPU's clock set apart from the config's `milan_clk_hz`, with the image and the bus unchanged;
- a sampler that also observes the CPU edges that no bus edge shares; at 100 MHz, where every CPU edge is a bus edge, its 1x1 arm A logs are byte-identical to the harness's;
- the bus clock moved with the CPU, with every script wait kept in milliseconds; at 100 MHz its scripts are identical.

The images and the CPU netlist are section 9's, so the clock is the only change, and the 50 MHz column is section 9's run.

### The rows against the clock

Each cell is the worst instance over the four groups in ms, arm A / arm B, bold where it misses T_svc (10 ms).
The owed window's last AECP record is a row of its own, because its response waits for the held egress.

| 1x1/1if: row | CPU 50 | CPU 100 | CPU 112.5 | CPU 150 | CPU and bus 112.5 | CPU and bus 150 |
|---|---:|---:|---:|---:|---:|---:|
| ACMP record, last | **14.23** / **14.10** | 9.72 / 8.55 | 8.45 / 8.48 | 7.90 / 7.04 | 8.13 / 7.60 | 5.78 / 5.97 |
| ADP record, last | **10.41** / 9.78 | 6.66 / 6.14 | 5.91 / 5.91 | 5.53 / 4.90 | 5.57 / 5.59 | 4.11 / 4.14 |
| MAAP record, last | **10.45** / 9.82 | 6.69 / 6.12 | 5.94 / 5.95 | 5.57 / 4.89 | 5.61 / 5.57 | 4.14 / 4.17 |
| AECP record, last | **29.26** / **29.09** | **20.07** / **18.78** | **18.23** / **18.17** | **16.09** / **15.94** | **17.19** / **16.70** | **12.75** / **12.94** |
| SRP record, last | **33.84** / **29.81** | **21.40** / **20.03** | **20.23** / **18.64** | **17.86** / **16.56** | **19.24** / **17.80** | **14.22** / **12.93** |
| AECP record, last, in the owed window | **68.27** / **68.24** | **65.76** / **65.76** | **65.34** / **65.37** | **64.69** / **64.91** | **65.06** / **65.09** | **63.69** / **63.78** |
| A response with 7 frames owed ahead of it | **65.75** / **66.36** | **64.06** / **64.03** | **63.74** / **63.74** | **63.63** / **63.45** | **63.55** / **63.56** | **62.56** / **62.63** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

| 8x8/2if: row | CPU 50 | CPU 100 | CPU 112.5 | CPU 150 | CPU and bus 112.5 | CPU and bus 150 |
|---|---:|---:|---:|---:|---:|---:|
| An ENTITY_AVAILABLE behind a full ADP ring | **12.13** / **12.12** | 7.91 / 7.42 | 7.34 / 6.66 | 6.35 / 5.86 | 7.03 / 6.40 | 5.64 / 4.39 |
| SRP record, first | **15.82** / **12.24** | 8.14 / 8.06 | 7.57 / 7.46 | 6.28 / 5.07 | 7.24 / 7.17 | 4.21 / 4.32 |
| ADP record, last | **16.09** / **16.08** | **10.60** / 9.89 | 9.85 / 9.15 | 8.71 / 7.94 | 9.63 / 8.80 | 7.59 / 6.86 |
| MAAP record, last | **16.07** / **16.12** | **10.64** / 9.91 | 9.90 / 9.13 | 8.75 / 7.93 | 9.67 / 8.78 | 7.62 / 6.85 |
| An ACMP command behind a full ACMP ring | **19.52** / **19.11** | **12.37** / **12.02** | **11.50** / **11.10** | **10.27** / 9.60 | **10.99** / **10.68** | 8.52 / 8.27 |
| ACMP record, last | **24.44** / **22.16** | **15.99** / **14.31** | **14.93** / **12.61** | **12.38** / **10.84** | **14.74** / **12.72** | **11.01** / 9.07 |
| AECP record, last | **53.03** / **46.75** | **33.42** / **30.52** | **30.84** / **27.16** | **26.77** / **24.11** | **31.06** / **26.63** | **23.14** / **19.64** |
| SRP record, last | **66.78** / **49.88** | **43.15** / **30.49** | **37.43** / **29.23** | **32.36** / **25.08** | **35.93** / **27.38** | **25.67** / **20.43** |
| AECP record, last, in the owed window | **77.50** / **77.05** | **71.55** / **70.91** | **70.41** / **69.96** | **69.24** / **68.75** | **70.01** / **69.51** | **67.55** / **67.15** |
| A response with 7 frames owed ahead of it | **72.54** / **72.14** | **68.32** / **67.73** | **68.11** / **67.02** | **66.39** / **65.99** | **67.14** / **67.38** | **65.40** / **65.03** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

The other composed rows fit at 50 MHz in both arms, at both points.

### Three rows no clock moves

- **A response with 7 frames owed ahead of it** includes the scenario's 60 ms egress hold, so it takes 62.6 to 72.5 ms at every clock.
- **An ACMP command behind the owed input** is never answered at any clock.
  The core owes at most `ACMP_OWED_MAX` (8) responses and drops the commands beyond them.
- **The owed window's last AECP record** is released 5.7 to 11.5 ms after the egress returns, at a 100 MHz CPU, so the hold sets it too.

### Why the CPU alone cannot close the rest

The harness counts each instruction line refill's wait at the CPU's fetch bus, and the bus clock sets that wait.
At a 100 MHz CPU, the windows that set the last AECP and SRP record rows spend 10.5 to 11.6 ms in refill waits alone at 1x1, and 10.9 to 14.2 ms at 8x8.
Fitting every instance to T = A/f + B over the four CPU clocks leaves B, the part no CPU clock removes.
In the bound-talker windows, B for those records is 8.3 to 9.9 ms at 1x1, which needs a CPU of 580 MHz or more.
At 8x8 it is 11.2 to 16.1 ms, more than T_svc, which no CPU clock closes.
At 8x8 the last ACMP record also needs 280 MHz in arm A and 182 MHz in arm B, and the ACMP command behind a full ring 153 and 138 MHz.

### The CPU and its bus together

With the bus moved too, the rows shrink almost in proportion to the clocks.
From 100 to 150 MHz the last AECP and SRP record rows take 0.60 to 0.69 times as long.
Scaled the same way from 150 MHz, the last SRP record needs about 215 MHz at 1x1 and 385 MHz at 8x8.

### Timing out of context

The product split CPU netlist (`VexiiRiscvLitex_796aec55cd5b8093ecb99c528d9a1284`, section 9's), with `rom` and `sram` built from the 1x1 image and its LiteDRAM crossing brought out to pins, is synthesized as in section 9 (`AreaOptimized_high`, `xc7a100t-fgg484-2`).
It is placed and routed with the CPU and bus clocks asynchronous, the generator's crossing between them.
Its bus side carries `rom`, `sram`, the crossings and the CSR bank; LiteDRAM, whose PHY clock is four times the bus's, is not in it.

| CPU clock | Bus clock | CPU WNS / WHS, ns | Bus WNS / WHS, ns | Closes |
|---:|---:|---:|---:|---|
| 100 MHz | 100 MHz | +0.952 / +0.041 | +2.440 / +0.070 | yes |
| 112.5 MHz | 100 MHz | +0.608 / +0.077 | +1.991 / +0.071 | yes |
| 120 MHz | 100 MHz | +0.581 / +0.074 | +2.239 / +0.072 | yes |
| 125 MHz | 100 MHz | +0.703 / +0.051 | +2.017 / +0.070 | yes |
| 140 MHz | 100 MHz | +0.205 / +0.003 | +2.305 / +0.070 | yes |
| 150 MHz | 100 MHz | +0.273 / +0.068 | +2.325 / +0.058 | yes |
| 160 MHz | 100 MHz | -0.139 / +0.041 (5 endpoints) | +2.081 / +0.071 | no |
| 112.5 MHz | 112.5 MHz | +0.706 / +0.031 | +1.476 / +0.072 | yes |
| 120 MHz | 120 MHz | +0.359 / +0.063 | +0.793 / +0.070 | yes |
| 125 MHz | 125 MHz | +0.648 / +0.031 | +0.994 / +0.070 | yes |
| 140 MHz | 140 MHz | +0.186 / +0.029 | +0.892 / +0.070 | yes |
| 150 MHz | 150 MHz | +0.310 / +0.040 | +0.807 / +0.070 | yes |
| 215 MHz | 215 MHz | -1.568 / +0.030 (1,340 endpoints) | -0.614 / +0.070 (258) | no |
| 431.6 MHz | 431.6 MHz | -3.931 / +0.045 (8,286 endpoints) | -2.805 / +0.071 (2,145) | no |

No route has a routing error.
The critical path at 160 MHz runs inside the CPU.
Out of context, with nothing else on the device, these are upper bounds; the integrated route is M8a-2's.

### What is left at the highest clock that closes

- **The CPU alone at 150 MHz**, the next step, 160 MHz, missing by 0.139 ns: at 1x1 the last AECP and SRP records still miss, 15.9 to 17.9 ms.
  At 8x8 so do the last ACMP record, 10.8 and 12.4 ms, the ACMP command behind a full ring in arm A, 10.27 ms, and the last AECP and SRP records, 24.1 to 32.4 ms.
- **The CPU and its bus at 150 MHz**: at 1x1 the last AECP and SRP records, 12.75 to 14.22 ms.
  At 8x8 the last ACMP record in arm A, 11.01 ms, and the last AECP and SRP records, 19.6 to 25.7 ms.
- **At every clock**, the three rows no clock moves.

So the CPU and its bus would both have to move, to about 215 MHz at 1x1 and 385 MHz at 8x8, and 215 MHz already fails out of context.
Setting the product clock is the owner's decision.
[Section 11](#11-the-firmwares-work-on-the-record-paths) measures the rows again after the firmware's own changes.

## 11. The firmware's work on the record paths

Before the product clock is chosen, the owner asked for the firmware work every clock needs on the AECP and SRP record paths ([assignment of 2026-10-29](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6486770462)).
This section is what those paths executed, the three changes, and the composed rows after them, at the 100 MHz CPU clock and with the CPU and its bus at 150 MHz.
No clock, cache geometry, admission, `ACMP_OWED_MAX` or scenario hold changed.

### What a window executed

The harness ran with a labelled, test-only profiling variant, not in the tree.
It charges each CPU cycle to the function of the last committed PC, each instruction line refill to the function that holds the line, and each data cache line refill and write-back to the running function.
A helper's cycles (`ctrl_mem`, the compiler runtime) are charged to the function that called it.
With its own lines removed, its 16 group logs at 100 MHz are byte-identical to section 10's.
Each window runs from the group's first loaded record's commit to the row's release, as in section 10.

At 100 MHz, before the changes:

- Instruction line refills took 6.1 to 16.8 ms of each window, 35 to 64 % of it outside the owed window.
  The windows' passes run 203 functions, some 46 KB of code, through the 4 KiB direct-mapped fetch L1.
  In the four windows traced, 35 to 55 % of the refills fetched a line the same pass had already fetched.
- In the 8x8 bound-talker windows, a data cache line refill was outstanding for 6.2 to 10.9 ms.
- In arm A's 8x8 `backlog-adp` window, the last SRP record's (40.66 ms):
  - AECP's event scans in `arm` and `aecp_poll` took 7.8 ms. Every call walked the events of all 124 descriptors, while the image's unanswered stream observations kept a few retrying.
  - The SRP adapter's registrar walks took 8.6 ms: `snapshot` through `mrp_attr_visit` and `registrations`, with the `memcmp` they call. It walked once before and once after every record, every poll and every tick, on each interface.
  - `mrp_reclaim` walked each participant's attributes twice a poll, 1.0 ms.

### The three changes

- **(a) AECP's scans walk an index** (`sw/firmware/ctrl/aecp/aecp.c`).
  The events holding a notice or a retry are linked in descriptor order through their rows (`aecp.live`), and `arm` and the notice scan of `aecp_poll` walk only them.
  A bit per registration (`aecp.used`) leaves the registry scans only the used ones.
  `aecp_open` relinks every row, as its rescan read every row.
  `aecp_find`, the descriptor lookup, is unchanged: on these rows it reads the ENTITY, the model's first descriptor, in 44 instructions a record.
- **(b) The SRP adapter keeps its copies until something they copy changes** (`sw/firmware/ctrl/srp/srp_mbx.c`).
  `snapshot` walks the registrar only after a Registrar state change (lwSRP's transition observer), an indication, a binding, or one of the adapter's own declarations, which rewrite the value of an attribute a registration may share.
  Otherwise it keeps the copies and runs each sink's capture, as a walk would.
  A record that changes no registration walks nothing; of the composed load's 32 Listener Ready records, only the first changes one.
  `mrp_reclaim` runs only after a transition or a receive, and stays owed while the participant holds the owed frame, which lwSRP never reclaims.
  lwSRP itself is unchanged.
- **(c) The service loop's hot code first** (`sw/firmware/ctrl/plat/ctrl_split.ld`).
  The 203 functions a service pass ran in the composed windows, 46,064 bytes, are placed ahead of the rest of `.text`, in the order a pass first ran them.
  The order comes from committed-PC traces of four windows, and a model of the fetch L1 (4 KiB, direct mapped, 64-byte lines) chose it.
  The model reads 4 to 8 % fewer refills than those windows measured.
  In it, packing the same functions in their linked order saves at most 5 % of the refills, and their run order 17 to 29 %; an order learned at one point holds at the other.
  In run order, a function a pass runs after another takes the next cache sets instead of evicting it.

Behaviour is unchanged apart from timing:

- The firmware self-test passes with its existing tests unchanged.
  Each change adds unit tests, with 100 % line and branch coverage on both files, and planted defects that those tests catch.
- In every group log, at both points, in both arms and at both clocks, each mailbox channel's egress frames, per interface and in order, are those before the changes.
  So is each mailbox register's own sequence of values, but for:
  - ADP at 8x8: which interface's first advertisement leaves first at boot, and in `backlog-owed` one periodic advertisement fewer in the shorter run;
  - MAAP's address, which the TSN stack seeds with the clock at start, so it follows boot timing;
  - the transmit records' `SEQ`, which counts frames across channels in send order;
  - the timer deadlines and the event ring's acknowledgements, which carry milliseconds.

### The rows after

Each cell is the worst instance over the four groups in ms, arm A / arm B, bold where it misses T_svc (10 ms).
The 150 MHz columns move the CPU and its bus together, with section 10's variants; their "before" is section 10's run.
| 1x1/1if: row | CPU 100, before | CPU 100, after | CPU and bus 150, before | CPU and bus 150, after |
|---|---:|---:|---:|---:|
| ACMP record, last | 9.72 / 8.55 | 6.99 / 7.20 | 5.78 / 5.97 | 4.88 / 4.76 |
| ADP record, last | 6.66 / 6.14 | 4.87 / 5.08 | 4.11 / 4.14 | 3.39 / 3.39 |
| MAAP record, last | 6.69 / 6.12 | 4.86 / 5.12 | 4.14 / 4.17 | 3.41 / 3.41 |
| AECP record, last | **20.07** / **18.78** | **13.95** / **14.62** | **12.75** / **12.94** | 9.26 / 9.64 |
| SRP record, last | **21.40** / **20.03** | **15.14** / **14.59** | **14.22** / **12.93** | 9.91 / 9.85 |
| AECP record, last, in the owed window | **65.76** / **65.76** | **64.20** / **64.19** | **63.69** / **63.78** | **62.74** / **62.78** |
| A response with 7 frames owed ahead of it | **64.06** / **64.03** | **62.92** / **62.91** | **62.56** / **62.63** | **62.13** / **61.96** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | 6.21 / 6.19 | 5.34 / 5.38 | 4.14 / 4.13 | 3.56 / 3.59 |
| An ENTITY_AVAILABLE behind a full ADP ring | 5.04 / 4.29 | 3.59 / 3.88 | 3.04 / 3.13 | 2.58 / 2.59 |
| An event behind 15 others | 1.82 / 1.80 | 1.54 / 1.55 | 1.21 / 1.20 | 1.03 / 1.03 |
| ACMP, ADP, AECP, MAAP record, first | 1.61 to 1.66 | 1.37 to 1.43 | 1.07 to 1.10 | 0.92 to 0.95 |
| SRP record, first | 3.31 / 3.23 | 2.77 / 2.79 | 2.16 / 2.15 | 1.85 / 1.86 |

| 8x8/2if: row | CPU 100, before | CPU 100, after | CPU and bus 150, before | CPU and bus 150, after |
|---|---:|---:|---:|---:|
| ACMP record, last | **15.99** / **14.31** | **11.30** / **10.72** | **11.01** / 9.07 | 7.47 / 7.26 |
| ADP record, last | **10.60** / 9.89 | 8.70 / 8.18 | 7.59 / 6.86 | 5.75 / 5.57 |
| MAAP record, last | **10.64** / 9.91 | 8.69 / 8.17 | 7.62 / 6.85 | 5.74 / 5.56 |
| AECP record, last | **33.42** / **30.52** | **19.50** / **19.60** | **23.14** / **19.64** | **13.23** / **13.61** |
| SRP record, last | **43.15** / **30.49** | **22.47** / **20.94** | **25.67** / **20.43** | **14.52** / **13.60** |
| AECP record, last, in the owed window | **71.55** / **70.91** | **66.89** / **66.41** | **67.55** / **67.15** | **64.59** / **64.47** |
| A response with 7 frames owed ahead of it | **68.32** / **67.73** | **64.99** / **65.03** | **65.40** / **65.03** | **63.33** / **63.27** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | **12.37** / **12.02** | **10.44** / 9.88 | 8.52 / 8.27 | 6.90 / 6.70 |
| An ENTITY_AVAILABLE behind a full ADP ring | 7.91 / 7.42 | 5.70 / 5.34 | 5.64 / 4.39 | 4.06 / 3.81 |
| An event behind 15 others | 3.09 / 3.13 | 2.74 / 2.68 | 2.06 / 2.09 | 1.83 / 1.79 |
| ACMP, ADP, AECP, MAAP record, first | 2.91 to 2.98 | 2.51 to 2.62 | 1.94 to 1.99 | 1.68 to 1.74 |
| SRP record, first | 8.14 / 8.06 | 5.60 / 5.42 | 4.21 / 4.32 | 3.70 / 3.61 |

The ENTITY_AVAILABLE behind the ADP ring with its bucket refilling, an observation, stays under 0.5 ms in every run.

### Instruction refills per window

The line refills of the work passes in each group's composed window, arm A / arm B, and their wait in ms.

| Window | CPU 100, before | CPU 100, after | CPU and bus 150, before | CPU and bus 150, after |
|---|---:|---:|---:|---:|
| 1x1 `backlog` | 7,215 / 7,282 (6.39 / 6.44) | 5,559 / 5,654 (4.92 / 4.99) | 7,000 / 7,064 (4.13 / 4.16) | 5,524 / 5,524 (3.26 / 3.25) |
| 1x1 `backlog-adp` | 13,180 / 13,889 (11.66 / 12.27) | 9,582 / 9,409 (8.58 / 8.35) | 13,474 / 13,439 (7.95 / 7.91) | 9,539 / 9,554 (5.70 / 5.66) |
| 1x1 `backlog-adp-refill` | 14,943 / 14,889 (13.22 / 13.15) | 11,450 / 10,113 (10.24 / 8.98) | 15,830 / 14,875 (9.33 / 8.76) | 11,521 / 10,216 (6.87 / 6.04) |
| 1x1 `backlog-owed` | 16,373 / 16,749 (14.48 / 14.79) | 11,340 / 11,555 (10.12 / 10.25) | 16,298 / 17,102 (9.61 / 10.07) | 11,304 / 11,521 (6.72 / 6.81) |
| 8x8 `backlog` | 12,742 / 12,176 (11.38 / 10.87) | 9,063 / 9,148 (8.10 / 8.17) | 12,481 / 11,914 (7.43 / 7.09) | 8,905 / 9,107 (5.31 / 5.42) |
| 8x8 `backlog-adp` | 15,990 / 13,711 (14.31 / 12.28) | 10,874 / 10,390 (9.74 / 9.25) | 14,955 / 13,860 (8.92 / 8.28) | 10,641 / 10,123 (6.36 / 6.01) |
| 8x8 `backlog-adp-refill` | 16,906 / 14,428 (15.13 / 12.93) | 11,523 / 10,925 (10.33 / 9.75) | 16,584 / 15,105 (9.89 / 9.03) | 12,044 / 10,992 (7.20 / 6.53) |
| 8x8 `backlog-owed` | 18,788 / 18,133 (16.80 / 16.31) | 12,526 / 12,588 (11.24 / 11.26) | 19,216 / 18,319 (11.45 / 10.99) | 12,740 / 12,506 (7.63 / 7.46) |

The changes take out 21 to 34 % of each window's refills.
(a) and (b) took out instructions and data cache refills, and (c) most of the instruction refills.
With (a) and (b) alone, the 1x1 `backlog` windows refilled more lines than before (7,661 / 7,415), their code having moved.

### What is left

- **At 100 MHz**:
  - at 1x1, the last AECP and SRP records, 13.95 to 15.14 ms;
  - at 8x8, the last ACMP record (11.30 / 10.72), arm A's ACMP command behind a full ring (10.44), and the last AECP and SRP records (19.50 to 22.47 ms).
- **With the CPU and its bus at 150 MHz**:
  - every composed row at 1x1 fits but section 10's three rows no clock moves;
  - at 8x8, the last AECP and SRP records still miss, 13.23 to 14.52 ms.
- **What the windows now run**:
  - the mailbox driver's record copies (`mbx_rx_take`, `mbx_tx_send`, `memcpy`, `memset`);
  - ACMP's core (`finish`, and `wire_put_be`'s 64-bit shifts through `__lshrdi3`);
  - lwSRP's receive (`rx_on_attr`, `parse_pass`).
  Instruction refills are still 4.9 to 11.3 ms of each window at 100 MHz.

Setting the product clock stays the owner's decision.

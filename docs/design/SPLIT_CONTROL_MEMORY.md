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
- **[3. Named refusals](#3-named-refusals)** -- The checks every image passes before any block RAM is built, the one ledgered point's named override, and the three planted controls.
- **[4. Boot console and diagnostics](#4-boot-console-and-diagnostics)** -- What the split image loses and keeps without a BIOS, and DDR3 until the wrapper is removed.
- **[5. Fit](#5-fit)** -- Linked spans and block RAM at the four points, mapped out of context, and the ledger rows, with the one point over budget owed to lane S14.
- **[6. Reproduce](#6-reproduce)** -- The link, the plan, the mapping and the test.

## 1. Memory map

| Region | Origin | Size | Holds |
|---|---|---:|---|
| `rom` | `0x0000_0000`, the CPU's reset address | 224 KiB | `.text` with the reset entry first, `.rodata`, the initial bytes of `.data` |
| `sram` | `0x1000_0000` | 224 KiB | `.data`, `.bss`, the 8 KiB stack |

Both origins are LiteX's VexiiRiscv `rom` and `sram` origins.
`add_ctrl_memory` refuses a CPU whose reset address or `sram` origin differs.
Every other region is unchanged: `main_ram`, `spiflash`, `milan_csr`, `ctrl_mbx` and `csr`.

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
| `allocation over budget` | `budget` | Banks totalling more than 56 RAMB36, a RAMB18 counting half, or more than a ledgered point's tiles; that point's override on any other image |
| `staging buffer` | `stage symbol` | An image with no `nvm_stage` |
| `staging buffer` | `stage size` | An `nvm_stage` that is not the selected shape's stage: its KLJ2 container plus one record header |

The budget is the owner's 224 KB at 4,096 usable bytes per RAMB36 (#640 ruling 6101485877).
An allocation of exactly 56.0 RAMB36 is accepted; 56.5 is refused.

One point may plan past the budget, and only by name (#665 rulings 6412739248 and 6425357821).
`ctrl_memory.LEDGERED` holds `8x8-two-interfaces`, the 8x8 image with two interfaces, at 57.5 RAMB36.
[Section 5](#5-fit) ledgers that tile and a half as owed to lane S14.
Only that point's measurement names the override, through `ctrl_memory.py plan --ledgered-point` or `ctrl_srp_image.py --ledgered-point`.
The product SoC build names none: `add_ctrl_memory` plans with no override, so every product SoC build is still held to 56 RAMB36.
The [CPU budget harness](../../tb/verilator/ctrl_service_budget/README.md) names it for that point only, for its image and its SoC plan (`build.py`, `LEDGERED_POINTS`).
The override recognises its image by the image's own symbols.
These are the 8x8 shape's `nvm_stage` of 13,264 bytes and the size fixture's `image_allocation`, 8 bytes per interface, so 16.
`budget` refuses the override on any other image, and refuses its point past 57.5 RAMB36.
`rom`'s contents are the load segments' file bytes and nothing else.
So `entry bytes` reads them as well as the sections: the first word at the reset address must be in them.
`load coverage` requires them to carry every byte of every section with initial bytes.
`add_ctrl_memory` checks the CPU's origins, then reads and plans the image, which runs every other rule but the two staging rules.
`main()` runs the staging check before any export; the shape comes from `--entity-gen-dir`.

[`test_ctrl_memory.py`](../../sw/litex/test_ctrl_memory.py) plants a defect for every rule and requires that rule to refuse it.
It plans the ledgered point at 57.5 RAMB36 by name, and requires `budget` to refuse that image in three cases: without the override, through `add_ctrl_memory`, and at 58.0 RAMB36.
It also plants the override on the 1x1 images with one and two interfaces, on the 8x8 image with one interface, and on an image without `image_allocation`, and requires `budget` to refuse each.
An override name the ledger does not hold is refused by `budget` too.
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

The ledger at lane S1's face writer (#665) is planned by `ctrl_memory.plan`.
It links the firmware of `e493dccd` against its base `e76a755a`, with one runtime for both:

| Point | `rom` need, B | `sram` need, B | Planned RAMB36 equivalents | Base `e76a755a` | Against the 56-RAMB36 budget |
|---|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 104,424 | 46,256 | 37.0 | 35.5 | within |
| 1x1, two interfaces | 106,008 | 57,648 | 40.5 | 38.5 | within |
| 8x8, one interface | 118,144 | 86,832 | 50.5 | 49.0 | within |
| 8x8, two interfaces (largest) | 119,800 | 112,992 | 57.5 | 56.0 | **over by 1.5 tiles, owed to lane S14** |

The face writer adds 6,496 to 6,592 B of `rom` and 336 B of `sram` at each point.
Its `applied` acknowledgement path, as `989c9f53` built it, accounts for 392 to 400 B of that `rom` and 16 B of that `sram`; at 8x8 with one interface it doubles `rom`'s last bank to 4 KiB, half a tile.
The model in which acknowledged state is the only truth a controller sees (#665, 6421238472) adds 1,056 B of `rom` and 224 B of `sram` at every point, against `989c9f53`, which did not have it:

- the record of the values a change overwrites, and its ten call sites;
- the swap that undoes and redoes the change;
- the held SUCCESS response, and the command's re-answer as a refusal;
- the wait's resolution, done or failed;
- the lock expiry's kept notification;
- the lock check's refusal while a change waits.

All 224 B of `sram` are the core's new state: the held response (`AECP_HELD_BYTES`, 122 B) with its interface, length and requester, the four recorded values, the noted change, the wait's deadline and its three flags.
Holding an expired lock by its owner until its release is applied, and refusing SET_SYSTEM_UNIQUE_ID as every change is while one waits, add 64 B more of `rom` and no `sram` at every point, against `6d2b77bb`.
The other three points keep their RAMB36 count: only at 8x8 with two interfaces do the added bytes cross a granule, in `rom`.
The shipping point has 24 B of `rom` left before its next granule would make it 37.5.
At 8x8 with two interfaces `rom`'s banks hold 119,800 B in 120,832 and `sram`'s 112,992 B in 114,688.
That is 57.5 RAMB36, a tile and a half over the budget, with 1,032 B of `rom` left before the next granule would make it 58.0.
Without this model the point had 104 B left at 57.0, so returning to 57.0 needs 1,016 B of `rom`.
RV32I has no compressed instructions. Two compactions were measured on throwaway edits at `4e3aab32`, and neither is taken:

- constant port tables in `aecp_face.c`, `aecp_mbx.c` and `ctrl_app_aecp.c`: 64 B of `rom`;
- IN_PROGRESS carrying the held SUCCESS body instead of re-answering the command: 64 B more.

Together they would leave 119,672 B, still 57.5.
The owner's decision D3 (#665, 6409738976) moves cold code and the descriptor image to QSPI flash in lane S14.
The rulings of 2026-10-26 ledger this point as owed to S14: one tile (#665, 6412739248), then a tile and a half (#665, 6425357821).
Only that point's measurement plans it, by name ([section 3](#3-named-refusals)), and every SoC build is still refused past 56.
The flip (S13) still requires 56 RAMB36 or fewer at every point, with S14 merged.
These figures are planned, not mapped.

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
  --interfaces 2 --with-aecp --layout split --ledgered-point 8x8-two-interfaces --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264 \
  --ledgered-point 8x8-two-interfaces
```

This is the ledgered point, so both commands name its override.
Without `--ledgered-point`, both refuse it at 57.5 RAMB36.
Every other point takes no override, and refuses one.

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

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
- **[3. Named refusals](#3-named-refusals)** -- The checks every image passes before any block RAM is built, the two ledgered images' named overrides, and the three planted controls.
- **[4. Boot console and diagnostics](#4-boot-console-and-diagnostics)** -- What the split image loses and keeps without a BIOS, and DDR3 until the wrapper is removed.
- **[5. Fit](#5-fit)** -- Linked spans and block RAM at the four points for the size fixture and the target platform, the platform's added bytes by part, mapped out of context, and the ledger rows, with the largest point over budget owed to lane S14.
- **[6. Reproduce](#6-reproduce)** -- The link, the plan, the mapping and the test.
- **[7. The CPU's instruction cache](#7-the-cpus-instruction-cache)** -- The split CPU's fetch L1: its parameters and why, its block RAM and logic against the ledger, the region decode, and the requirement it conflicts with.
- **[8. The CPU's multiply and divide](#8-the-cpus-multiply-and-divide)** -- The split CPU's RV32M, the image built and audited for it, its logic out of context, and the requirement amended for it.
- **[9. The CPU's data cache](#9-the-cpus-data-cache)** -- The split CPU's LSU L1: its size from the composed bursts, why it is coherent, the windows it never caches, its area against the ledger, and the requirement amended for it.
- **[10. The CPU clock the composed rows need](#10-the-cpu-clock-the-composed-rows-need)** -- The composed rows measured against the CPU clock alone and with its bus, the rows no clock moves, timing out of context, and what is left at the highest clock that closes.
- **[11. The firmware's work on the record paths](#11-the-firmwares-work-on-the-record-paths)** -- What the AECP and SRP record paths executed, the indexed AECP scans, the SRP copies kept until they change, the hot code placed first, and the composed rows after them at a 100 MHz test clock and at 150 MHz.
- **[12. The remaining firmware levers at the present clock](#12-the-remaining-firmware-levers-at-the-present-clock)** -- The indexed descriptor lookup, the hot list's gate, ACMP's wire packing as a TSN stack change, the record copies and lwSRP's receive checked, the composed rows after them at a 100 MHz test clock, what a larger fetch L1 would save by the model, and, with the CPU on `sys` at 100 MHz, a save in a composed window, its worst case, aged windows, THE RETRY, and THE TRANSMIT with every pass class.
- **[13. The larger fetch L1 and the record mover](#13-the-larger-fetch-l1-and-the-record-mover)** -- The 16 KiB two-way fetch L1 and its area and timing out of context, the bulk copies and fills, the mailbox's record mover, lwSRP's receive path as a change to lwSRP, the composed rows after them at a 100 MHz test clock, the rows again at the approved T_svc = 20 ms and with contract 2.3's face writer, the refills per window, what holds the 8x8 rows, every row and pass at the Milan clock of 2026-10-29, every row and pass with the CPU on `sys` at 100 MHz, a save in each flash phase and both links at once, with the store's step held to the pass's share, and a save's worst case under any input, with one build a pass either way.
- **[14. The 32x32 estimate](#14-the-32x32-estimate)** -- The service load per row at four times the 8x8 streams, an estimate against T_svc; one CPU, measured on the cacheless core at 100 MHz; gPTP's share, a labelled assumption; and what it leaves to the owner.

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
| `allocation over budget` | `budget` | Banks totalling more than 56 RAMB36, a RAMB18 counting half, or more than a ledgered point's tiles; that point's override on any other image |
| `staging buffer` | `stage symbol` | An image with no `nvm_stage` |
| `staging buffer` | `stage size` | An `nvm_stage` that is not the selected shape's stage: its KLJ2 container plus one record header |

The budget is the owner's 224 KB at 4,096 usable bytes per RAMB36 (#640 ruling 6101485877).
An allocation of exactly 56.0 RAMB36 is accepted; 56.5 is refused.

Two images may plan past the budget, each only by its own name (#665 rulings 6412739248, 6425357821 and 6505997821).
Both are 8x8 with two interfaces, and [section 5](#5-fit) ledgers both as owed to lane S14:

| Name in `ctrl_memory.LEDGERED` | Image | Its symbols | RAMB36 |
|---|---|---|---:|
| `8x8-two-interfaces` | the size fixture's | `nvm_stage` of 13,264 B, `image_allocation` of 16 B | 57.5 |
| `platform-8x8-two-interfaces` | the target platform's | `nvm_stage` of 13,264 B, `ctrl_plat` of 19,968 B | 59.0 |

Each override recognises its image by the image's own symbols.
`nvm_stage` is the 8x8 shape's staging buffer.
The second is the image's own object, sized by the two interfaces.
For the size fixture it is the per-interface table `image_allocation`, 8 bytes per interface.
For the platform it is its one static object, `struct ctrl_plat`, whose size follows the interface count and the shape's streams.
A change to that struct changes the size, so the override refuses the image until its entry is measured again.
Only a point's own measurement names its override, through `ctrl_memory.py plan --ledgered-point`, `ctrl_srp_image.py --ledgered-point` or `ctrl_plat_image.py --ledgered-point`.
The product SoC build names none: `add_ctrl_memory` plans with no override, so every product SoC build is still held to 56 RAMB36.
The [CPU budget harness](../../tb/verilator/ctrl_service_budget/README.md) names the size fixture's for that point only, for its image and its SoC plan (`build.py`, `LEDGERED_POINTS`).
`budget` refuses either override on any other image, the other override's image among them, and refuses its point past its tiles.
`rom`'s contents are the load segments' file bytes and nothing else.
So `entry bytes` reads them as well as the sections: the first word at the reset address must be in them.
`load coverage` requires them to carry every byte of every section with initial bytes.
`add_ctrl_memory` checks the CPU's origins, then reads and plans the image, which runs every other rule but the two staging rules.
`main()` runs the staging check before any export; the shape comes from `--entity-gen-dir`.

[`test_ctrl_memory.py`](../../sw/litex/test_ctrl_memory.py) plants a defect for every rule and requires that rule to refuse it.
It plans each ledgered point's image at its tiles by name; [`ctrl_memory_ledger.py`](../../sw/litex/ctrl_memory_ledger.py) holds the cases.
It requires `budget` to refuse that image in three cases: without the override, through `add_ctrl_memory`, and half a tile past its tiles.
It also plants each override on the same image's three other points, on the other override's image, and on an 8x8 image carrying one of its two symbols alone, and requires `budget` to refuse each.
An override name the ledger does not hold is refused by `budget` too.
Six planted ledgers each widen one entry to another point or image, or past its tiles.
The platform's entry loses its staging buffer or `ctrl_plat`, takes the 8x8 one-interface `ctrl_plat`, or plans 59.5.
The fixture's loses `image_allocation`, or plans 59.0.
Each must turn the test red with the ledger's own entries, which the test pins, set aside.
It also requires this table to equal `ctrl_memory.RULES`.
For every rule it rebuilds the code with that rule removed or weakened, and requires a named failure.
Three of those rebuilds let an override plan any image, any image carrying its symbols, or any image with its staging buffer.

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
The [target platform](../../sw/firmware/ctrl/plat/README.md#the-console) brings one, under decision D6 (#665): `milan_status` and `milan_gettime` in `milan_baremetal.c`'s lines, and one boot banner.
It also writes the CSR initialisation `milan_baremetal.c` writes for the same shape ([the CSR window](../../sw/firmware/ctrl/plat/README.md#the-csr-window)).

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

The ledger at lane S2b's merge of S1's face writer (#665, `dev-soft-core` `f4c9ad4f`) is planned the same way.
It links the merged firmware of `51fa5f18` against the branch before the merge, `bf1773c0`, with one runtime for both:

| Point | `rom` need, B | `sram` need, B | Planned RAMB36 equivalents | Before the merge, `bf1773c0` | Against the 56-RAMB36 budget |
|---|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 103,520 | 44,960 | 36.5 | 35.0 | within |
| 1x1, two interfaces | 104,968 | 56,352 | 40.0 | 38.5 | within |
| 8x8, one interface | 117,128 | 85,536 | 50.0 | 48.5 | within |
| 8x8, two interfaces (largest) | 118,584 | 111,696 | 56.5 | 55.0 | **over by half a tile**, within the 57.5 ledgered and owed to lane S14 |

The merge adds 6,264 to 6,376 B of `rom` and 336 B of `sram` at each point, the face writer's.
Each point plans half a tile under S1's own ledger above, and the largest a whole tile, because the branch's compactions (sections 11 to 13) are in both.
These figures are planned, not mapped.
The [target platform](../../sw/firmware/ctrl/plat/README.md)'s image (#665 S3) replaces the size fixture's `main` with the platform's, and links with `ctrl_plat_image.py`.
Planned by `ctrl_memory.plan` from the firmware of `b8628704`, beside the fixture at the same commit, both linked with the same runtime:

| Point | Platform `rom` / `sram` need, B | Platform RAMB36 | Fixture `rom` / `sram` need, B | Fixture RAMB36 | Platform minus fixture, B | Against the budget |
|---|---:|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 109,560 / 47,168 | 39.0 | 104,448 / 46,272 | 37.0 | +5,112 / +896 | within |
| 1x1, two interfaces | 111,200 / 58,592 | 42.0 | 106,032 / 57,648 | 40.5 | +5,168 / +944 | within |
| 8x8, one interface | 123,304 / 87,760 | 52.0 | 118,168 / 86,848 | 50.5 | +5,136 / +912 | within |
| 8x8, two interfaces (largest) | 125,048 / 113,936 | 59.0 | 119,824 / 113,008 | 57.5 | +5,224 / +928 | **over by 3.0 tiles, ledgered at 59.0, owed to lane S14** |

At 8x8 with two interfaces the platform's `rom` banks hold 125,048 B in 126,976 and its `sram` banks 113,936 B in 114,688.
That is 59.0 RAMB36, three tiles over the budget and a tile and a half over the fixture's 57.5.
It cannot reach 57.5 within the platform's files, because each region is planned in power-of-two banks of whole granules.
The fixture's own `sram` (113,008 B) already needs 28.0 tiles, so `rom` would have to fit 29.5 tiles (120,832 B).
That is a cut of 4,216 B from the platform's 5,224 B of `rom`.
The owner's ruling of 2026-10-29 (#665, 6505997821) ledgers that point at 59.0, owed to lane S14 under decision D3: the boot and the CSR policy are cold code, which D3 moves to flash.
It amends ruling 6425357821's 57.5 for this one image, and `ctrl_memory.LEDGERED` names it `platform-8x8-two-interfaces` ([section 3](#3-named-refusals)).
Every other point stays within 56 RAMB36.
The flip (S13) needs 56 RAMB36 or fewer at every point, with S14 merged.

At this branch's head the two images are built alike, RV32IM with the record mover and the word-wide primitives (`ctrl_plat_image.py` takes `ctrl_srp_image.py`'s split flags and audits), and the branch's compactions are in both:

| Point | Platform `rom` / `sram` need, B | Platform RAMB36 | Fixture `rom` / `sram` need, B | Fixture RAMB36 | Against the budget |
|---|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 109,152 / 45,920 | 38.5 | 104,048 / 45,008 | 36.5 | within |
| 1x1, two interfaces | 110,808 / 57,344 | 41.5 | 105,656 / 56,400 | 40.0 | within |
| 8x8, one interface | 122,792 / 86,496 | 51.5 | 117,656 / 85,584 | 50.0 | within |
| 8x8, two interfaces (largest) | 124,480 / 112,672 | 58.5 | 119,264 / 111,744 | 57.0 | **over by 2.5 tiles**, within the 59.0 and the 57.5 ledgered, owed to lane S14 |

These are planned, not mapped.
THE STEP (`ctrl_loop.h`, section 13) and SRP's one build a pass add 336 to 424 B of `rom` and 16 to 32 B of `sram` at each point; at 8x8 with two interfaces each image takes half a tile more than the round before's 58.0 and 56.5 (#665, 2026-11-02): the fixture's `rom`, 424 B more, one more 2 KiB bank, and the platform's `sram`, 32 B more than the 112,640 B its banks held exactly.
THE STEP's age limit, SRP's turn read before the poll's visits and the store's walk-free mark add 152 to 224 B of `rom` and up to 16 B of `sram` at each point (#665, 2026-11-03); only the platform's 1x1 two-interface image takes half a tile more, 41.5, its `rom` 216 B past the 110,592 B, 54 banks of 2 KiB, that it filled exactly.
`ctrl_plat` is 19,968 B at the largest point, 19,960 B before the age limit's two fields, 19,944 B before THE STEP's four fields and 21,240 B when the ledger above named it, so the ledger names the new size, as it requires when that struct changes.
The figures by part below are `b8628704`'s.

By part, from the two link maps, with one section per function and object, the platform's bytes minus the fixture's at each point (`rom` / `sram`, B):

| Part | 1x1, one interface | 1x1, two interfaces | 8x8, one interface | 8x8, two interfaces |
|---|---:|---:|---:|---:|
| The boot: `ctrl_plat_boot` with the composition, MAAP owner and SRP source set-up it inlines, `ctrl_plat_step` and the image hook; the three configurations it holds (`config`, `aecp_config`, `srp_config`) | +1,528 / +128 | +1,656 / +144 | +1,532 / +128 | +1,692 / +144 |
| The CSR policy: identity, the fifteen writes, status and time of day (`ctrl_plat_csr.c`) | +788 / 0 | +788 / 0 | +788 / 0 | +788 / 0 |
| The console (`ctrl_plat_console.c`, its digit table and its state) | +1,748 / +588 | +1,748 / +588 | +1,748 / +588 | +1,748 / +588 |
| The console's and the boot's strings, merged | +762 / 0 | +762 / 0 | +762 / 0 | +762 / 0 |
| MAAP's port: the window's two accesses, the allocation report and `maap_csr.c`, with its state | +916 / +32 | +916 / +32 | +916 / +32 | +916 / +32 |
| ACMP's talker sources: `source`, `locked`, `stream`, `notice` | +164 / 0 | +164 / 0 | +164 / 0 | +164 / 0 |
| SRP's licence port | +48 / 0 | +48 / 0 | +48 / 0 | +48 / 0 |
| AECP's observations: `random_value`, `path` | +12 / 0 | +12 / 0 | +12 / 0 | +12 / 0 |
| `main`, the generated policy and stream table, and `env` (`ctrl_plat_main.c`) | +168 / +56 | +168 / +56 | +224 / +56 | +224 / +56 |
| The bus port (`ctrl_plat_mmio.c`) | +16 / 0 | +16 / 0 | +16 / 0 | +16 / 0 |
| The rest of `struct ctrl_plat`, against the fixture's `image_allocation`, `image_licences` and two constant port tables | -80 / +114 | -80 / +128 | -80 / +107 | -80 / +114 |
| The size fixture's `main` and its callbacks, removed (`ctrl_aecp_image.c`) | -980 / 0 | -1,052 / 0 | -1,012 / 0 | -1,088 / 0 |
| Every other object: the same sources, built against the platform's bus map | +16 / 0 | +16 / 0 | +16 / 0 | +16 / 0 |
| Alignment | +6 / -22 | +6 / -4 | +2 / +1 | +6 / -6 |
| **The platform minus the fixture** | **+5,112 / +896** | **+5,168 / +944** | **+5,136 / +912** | **+5,224 / +928** |

The other members of `struct ctrl_plat` are the objects the fixture holds with the same types: the application, SRP, AECP, its bridge and face, ACMP's configuration, the saved state and the sources.
They are equal in both images, and so are the AEM image, its pools and lwSRP's pool.
The ports' rows are the platform's callbacks; the fixture's stand-ins for them are in its removed `main` row.
The rest of `struct ctrl_plat` is its stage, version, MAAP allocations, licences and drop count, and the ACMP and AECP port tables the fixture keeps constant in `rom`.
The five largest `.bss` objects at the shipping point are lwSRP's pool (9,920 B), the application (8,880 B), SRP (4,824 B), the descriptor image's values (4,527 B) and AECP (3,352 B).
At the largest point they are lwSRP's pool (48,064 B), F1's `nvm_stage` (13,264 B), the descriptor image's values (11,753 B), the application (10,064 B) and SRP (5,896 B).
The held open (`ctrl_app_open_held`) adds 24 B of `rom` and 16 B of `sram` to the fixture too; at the shipping point its `rom` then fills its last granule exactly, still 37.0.

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

Link the target platform's image at the same point, against the `csr.csv` of a split export of that shape (`$SOC`):

```sh
python3 sw/firmware/ctrl/test/ctrl_plat_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --ledgered-point platform-8x8-two-interfaces --csr-csv "$SOC/csr.csv" --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
```

It names the platform's own override, and is refused at 59.0 RAMB36 without it or with the fixture's.
Its report (`$OUT/size.json`) holds the plan and the five largest `.bss` objects, with `ctrl_plat` counted by member.

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
It then required one control hart: in the split placement it is RV32IM, with a 4 KiB direct-mapped instruction cache (64-byte lines, one refill at a time) and an 8 KiB direct-mapped data cache (64-byte lines), coherent with the DMA port, with the mailbox, CSR and flash windows uncached; in the all-fabric placement it is RV32I and stays cacheless.
[The architecture](../ARCHITECTURE_HW_SW_SPLIT.md) repeated that wording.
The owner amended it again on 2026-10-29 for a larger instruction cache ([section 13](#13-the-larger-fetch-l1-and-the-record-mover)).

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
This section is what those paths executed, the three changes, and the composed rows after them, at a 100 MHz CPU clock and with the CPU and its bus at 150 MHz.
Neither was the product's that day, when the product clocked the split CPU at 50 MHz and its bus at 100 MHz ([section 13](#at-the-milan-clock-and-the-per-pass-share)); the owner moved the CPU to `sys` at 100 MHz on 2026-10-30 ([section 13](#the-split-cpu-on-sys-at-100-mhz)).
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
  `aecp_find`, the descriptor lookup, is unchanged here: on these rows it reads the ENTITY, the model's first descriptor, in 44 instructions a record.
  Section 12 indexes it.
- **(b) The SRP adapter keeps its copies until something they copy changes** (`sw/firmware/ctrl/srp/srp_mbx.c`).
  `snapshot` walks the registrar only after a Registrar state change (lwSRP's transition observer), an indication, a binding, or one of the adapter's own declarations, which rewrite the value of an attribute a registration may share.
  Otherwise it keeps the copies and runs each sink's capture, as a walk would.
  A record that changes no registration walks nothing; of the composed load's 32 Listener Ready records, only the first changes one.
  `mrp_reclaim` runs only after a transition or a receive, and stays owed while the participant holds the owed frame, which lwSRP never reclaims.
  lwSRP itself is unchanged.
- **(c) The service loop's hot code first** (`sw/firmware/ctrl/plat/ctrl_split.ld`).
  The 203 functions a service pass ran in the composed windows, 46,064 bytes, are placed ahead of the rest of `.text`, in the order a pass first ran them.
  Since contract 2.3's face writer replaced the size fixture's stream observation, `ctrl_aecp_image a_stream`, 202 are listed, in the same order.
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

The owner kept the product's clocks on 2026-10-29, the CPU at 50 MHz and its bus at 100 MHz; section 12 takes the firmware levers left at them, and the decision of 2026-10-30 moved the CPU to `sys` ([section 13](#the-split-cpu-on-sys-at-100-mhz)).

## 12. The remaining firmware levers at the present clock

The owner kept the split CPU and its bus at their clocks on 2026-10-29 ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6488028169)), the CPU at 50 MHz and its bus at 100 MHz, and the [assignment of the same day](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6489248781) took the firmware levers left on the record paths.
Every figure here is at a 100 MHz CPU clock, then a test clock behind the crossing and not the product's 50 MHz of that day, measured with section 11's profiling variant.
[Section 13](#the-split-cpu-on-sys-at-100-mhz) measures the rows at the product's clock, `sys` at 100 MHz.
No clock, cache geometry, admission, `ACMP_OWED_MAX`, scenario hold or RTL changed.

### The changes

- **`aecp_find` answers from an index** (`sw/firmware/ctrl/aecp/aecp_commands.c`).
  `aecp_init` builds it from the model's keys (`aecp_index`, `aecp.runs`): for each configuration and each descriptor type of IEEE 1722.1-2021 Table 7-1, where its descriptors start and how many there are, each at the position of its index.
  A lookup is the run's start plus the index.
  A model `aecp_image_load` built is one run per key.
  A key outside the indexed configurations (the first; every shipped model has one) or types, or placed any other way, is scanned for as before, so every model is found as it was.
  The firmware never changes a key after `aecp_init`.
  The self-test's cases that do now rebuild the index with the change, and the fixture's teardown fails any case that leaves `aecp_find` answering differently from a scan of the model.
- **The hot list is gated** (`sw/firmware/ctrl/test/ctrl_hot.py`).
  `plat/ctrl_split_hot.txt` records section 11's order with the traces it came from.
  The script's list must be that one, entry for entry, and every entry must name a section of the linked image, read from its link map.
  `ctrl_srp_image.py` applies both rules to every split image it links, and the firmware self-test runs the gate's planted defects.
- **ACMP's 64-bit wire fields** are packed by the TSN stack's `wire_put_be` (`include/wire.h`).
  Its 64-bit shift by a variable count is a call to the compiler runtime's `__lshrdi3` for each byte.
  Packing in two 32-bit halves takes the call out, bit for bit.
  The stack is pinned (`ctrl_build.stack_pin` refuses any other tree), so this is a change to tsn-c-stack, drafted for that repository's own review and not in this branch.
  It is measured below with the pin moved in a scratch tree only.
  With it nothing calls `__lshrdi3`, so the runtime's hot-list entry goes with the pin move: the gate refuses the image until it does.
- **The mailbox driver's record copies** were checked and left as they are.
  - A received record is copied once, from its ring into the loop's frame, a word at a time, and every module reads it there.
  - A transmitted record is built once and copied once into its ring, a word at a time when the frame starts on a word.
    In the traced windows only MAAP's frames start elsewhere: its transmit queue sits at an unaligned offset of the stack's `struct maap`, seven frames a window.
  - The other copies are the stack's (ACMP's owed queue copies a frame it built on the stack) and the SRP adapter's retry, which copies a record only after lwSRP refused it storage.
- **lwSRP's receive path** (`parse_pass`, `rx_on_attr` and the attribute lookups, with the helpers they call) takes 2.3 to 4.4 ms of each window that carries SRP records, 13 to 31 %.
  It is the largest single path there, but it holds no row.
  Without any of it, the missing rows' worst instances would still be 11.0 to 11.7 ms at 1x1 and 16.1 to 17.7 ms at 8x8 (10.1 to 10.7 and 16.1 to 17.2 with the stack's change).
  lwSRP is unchanged.

### The rows

Each cell is the worst instance over the four groups in ms, arm A / arm B, bold where it misses T_svc (10 ms).
"Before" is section 11's "after"; "with the stack's change" adds the tsn-c-stack draft to this branch.

| 1x1/1if: row | before | after | with the stack's change |
|---|---:|---:|---:|
| ACMP record, last | 6.99 / 7.20 | 6.62 / 6.76 | 6.06 / 6.37 |
| ADP record, last | 4.87 / 5.08 | 4.94 / 5.06 | 4.27 / 4.50 |
| MAAP record, last | 4.86 / 5.12 | 4.93 / 5.09 | 4.31 / 4.54 |
| AECP record, last | **13.95** / **14.62** | **13.45** / **14.37** | **12.95** / **13.44** |
| SRP record, last | **15.14** / **14.59** | **15.30** / **14.84** | **14.28** / **13.91** |
| AECP record, last, in the owed window | **64.20** / **64.19** | **64.19** / **64.22** | **64.16** / **64.07** |
| A response with 7 frames owed ahead of it | **62.92** / **62.91** | **62.90** / **62.94** | **62.90** / **62.88** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | 5.34 / 5.38 | 5.44 / 5.40 | 4.89 / 4.86 |
| An ENTITY_AVAILABLE behind a full ADP ring | 3.59 / 3.88 | 3.63 / 3.86 | 3.18 / 3.42 |
| An event behind 15 others | 1.54 / 1.55 | 1.57 / 1.57 | 1.44 / 1.43 |
| ACMP, ADP, AECP, MAAP record, first | 1.37 to 1.43 | 1.40 to 1.44 | 1.27 to 1.32 |
| SRP record, first | 2.77 / 2.79 | 2.83 / 2.83 | 2.62 / 2.60 |

| 8x8/2if: row | before | after | with the stack's change |
|---|---:|---:|---:|
| ACMP record, last | **11.30** / **10.72** | **10.69** / **10.70** | **10.51** / **10.59** |
| ADP record, last | 8.70 / 8.18 | 8.13 / 8.14 | 8.01 / 8.06 |
| MAAP record, last | 8.69 / 8.17 | 8.12 / 8.13 | 8.00 / 8.04 |
| AECP record, last | **19.50** / **19.60** | **19.26** / **19.73** | **19.11** / **20.39** |
| SRP record, last | **22.47** / **20.94** | **21.76** / **21.07** | **21.30** / **20.86** |
| AECP record, last, in the owed window | **66.89** / **66.41** | **66.52** / **66.64** | **66.68** / **66.74** |
| A response with 7 frames owed ahead of it | **64.99** / **65.03** | **64.70** / **64.82** | **64.85** / **64.91** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | **10.44** / 9.88 | 9.85 / 9.86 | 9.66 / 9.73 |
| An ENTITY_AVAILABLE behind a full ADP ring | 5.70 / 5.34 | 5.45 / 5.34 | 5.24 / 5.43 |
| An event behind 15 others | 2.74 / 2.68 | 2.65 / 2.66 | 2.61 / 2.61 |
| ACMP, ADP, AECP, MAAP record, first | 2.51 to 2.62 | 2.48 to 2.53 | 2.44 to 2.48 |
| SRP record, first | 5.60 / 5.42 | 5.36 / 5.35 | 5.27 / 5.29 |

The ENTITY_AVAILABLE behind the ADP ring with its bucket refilling, an observation, stays under 0.5 ms in every run.
Arm A's 8x8 ACMP command behind a full ring now fits.
Some rows moved the other way (the 1x1 last SRP record in arm A, the 8x8 last AECP record in arm B): code that moves changes which lines the fetch L1 holds.

### Instruction refills per window

The line refills of the work passes in each group's composed window, arm A / arm B, and their wait in ms.

| Window | before | after | with the stack's change |
|---|---:|---:|---:|
| 1x1 `backlog` | 5,559 / 5,654 (4.92 / 4.99) | 5,551 / 5,539 (4.90 / 4.90) | 5,471 / 5,473 (4.84 / 4.84) |
| 1x1 `backlog-adp` | 9,582 / 9,409 (8.58 / 8.35) | 10,053 / 9,766 (8.92 / 8.63) | 9,655 / 9,354 (8.53 / 8.27) |
| 1x1 `backlog-adp-refill` | 11,450 / 10,113 (10.24 / 8.98) | 11,698 / 10,463 (10.38 / 9.25) | 11,260 / 10,064 (9.95 / 8.90) |
| 1x1 `backlog-owed` | 11,340 / 11,555 (10.12 / 10.25) | 11,629 / 11,627 (10.32 / 10.28) | 11,362 / 11,284 (10.03 / 9.96) |
| 8x8 `backlog` | 9,063 / 9,148 (8.10 / 8.17) | 9,029 / 9,087 (8.04 / 8.08) | 8,985 / 9,111 (7.96 / 8.07) |
| 8x8 `backlog-adp` | 10,874 / 10,390 (9.74 / 9.25) | 10,686 / 10,380 (9.53 / 9.26) | 10,575 / 10,215 (9.40 / 9.03) |
| 8x8 `backlog-adp-refill` | 11,523 / 10,925 (10.33 / 9.75) | 11,626 / 10,906 (10.35 / 9.71) | 11,608 / 10,713 (10.31 / 9.48) |
| 8x8 `backlog-owed` | 12,526 / 12,588 (11.24 / 11.26) | 12,331 / 12,592 (11.01 / 11.25) | 12,427 / 12,474 (11.05 / 11.06) |

The levers took out instructions, 3 to 10 % of a window's with the stack's change, and no refills: each window refills within 5 % of before.

### What holds the rows

In each window still over T_svc, instruction refills wait 43 to 61 % of the window (7.1 to 9.6 ms) and a data cache line refill is outstanding for 8 to 19 % (1.0 to 3.9 ms).
By function, the largest are the memory primitives' copies and fills (`ctrl_mem`'s `forward` and `memset`, 1.2 to 1.6 ms each at 8x8, called most from ACMP's views and records and from the AECP command bodies), the mailbox driver (`mbx_rx_take` and `mbx_tx_send`, about 1.0 to 1.2 ms each), lwSRP's receive path (above) and ACMP's core.
None of them alone would bring a missing row within T_svc.

### What a larger fetch L1 would save, by the model

Section 11's model of the fetch L1 (64-byte lines, a miss on each committed PC whose line is not held) takes its size and ways as parameters here, with least recently used replacement.
It ran on committed-PC traces of every window, arm A, at both points, of this branch and with the stack's change.
At the product's 4 KiB direct-mapped geometry it reads 3 to 8 % fewer refills than the traces measured.
Each window's measured refill wait is scaled by the fraction of refills the model removes; nothing else in the window moves.
The worst window of each row that misses, in ms, bold where it would still miss:

| Row | Geometry now | 4 KiB 2-way | 4 KiB 4-way | 8 KiB 1-way | 8 KiB 2-way | 16 KiB 1-way | 16 KiB 2-way | 16 KiB 4-way |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 AECP record, last | **13.46** | **13.16** | **13.14** | **11.85** | **10.98** | 9.93 | 8.96 | 8.75 |
| 1x1 SRP record, last | **15.34** | **14.98** | **14.97** | **13.42** | **12.30** | **11.11** | 9.91 | 9.58 |
| 8x8 ACMP record, last | **10.74** | **10.33** | **10.24** | 9.91 | 9.26 | 9.29 | 8.40 | 8.37 |
| 8x8 AECP record, last | **19.27** | **18.84** | **18.69** | **17.67** | **16.95** | **15.36** | **14.44** | **13.99** |
| 8x8 SRP record, last | **21.80** | **21.34** | **21.16** | **19.93** | **19.17** | **17.10** | **16.09** | **15.47** |
| 1x1 AECP record, last, with the stack's change | **12.96** | **12.87** | **12.81** | **11.13** | **10.32** | 9.34 | 8.34 | 8.23 |
| 1x1 SRP record, last, with the stack's change | **14.31** | **14.20** | **14.14** | **12.24** | **11.34** | **10.14** | 8.90 | 8.74 |
| 8x8 ACMP record, last, with the stack's change | **10.56** | 9.98 | 9.68 | 9.68 | 8.82 | 9.14 | 8.09 | 8.01 |
| 8x8 AECP record, last, with the stack's change | **19.12** | **18.70** | **18.38** | **17.49** | **16.41** | **15.41** | **14.29** | **13.96** |
| 8x8 SRP record, last, with the stack's change | **21.33** | **20.87** | **20.51** | **19.43** | **18.22** | **17.01** | **15.66** | **15.23** |

By the model, a 16 KiB two-way fetch L1 brings both 1x1 rows within T_svc, and 8 KiB direct-mapped the 8x8 last ACMP record.
At 8x8 no geometry up to 16 KiB four-way brings the last AECP or SRP record within T_svc: the instructions themselves, the data cache's refills and the mailbox's bus waits are left.
The geometry stays the owner's decision.

### What is left

- At 100 MHz the last AECP and SRP records still miss at both points, 12.95 to 15.30 ms at 1x1 and 19.11 to 21.76 ms at 8x8, and at 8x8 the last ACMP record, 10.51 to 10.70 ms.
- The stack's change reaches this branch only through tsn-c-stack's own review, then a pin move with the hot list's runtime entry removed.

## 13. The larger fetch L1 and the record mover

The owner took three of section 12's open items on 2026-10-29 ([decision and assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6492443864)):
- a 16 KiB two-way fetch L1 on the split hart;
- a firmware and bus-path round for the 8x8 rows: bulk copies and fills, a DMA for the mailbox driver's record transfers, and a change to lwSRP's receive path;
- the TSN stack's wire-halves change from section 12, measured staged as there.

Every figure in this section up to [At the Milan clock](#at-the-milan-clock-and-the-per-pass-share) is at a 100 MHz CPU clock with the bus at 100 MHz: section 11's profiling variant ran the split CPU at that clock (`CSB_CPU_HZ`), behind the generator's crossing, as a test clock.
That subsection has every row and every pass at the two clocks of its day, when the product clocked the split CPU from the Milan clock, 50 MHz, with its bus at 100 MHz.
The owner's decision of 2026-10-30 then put the CPU on `sys`, the bus clock, at 100 MHz, with no crossing, and [The split CPU on `sys`](#the-split-cpu-on-sys-at-100-mhz) has every row and pass there.

### The fetch L1

| Parameter | Value | Reason |
|---|---|---|
| Size | 16 KiB: 128 sets | The owner's decision; section 12's model put both 1x1 rows within the 10 ms T_svc then proposed at this size and ways |
| Ways | 2, least recently used | The pinned generator replaces by its pseudo-LRU, which at two ways is exact LRU |
| Line | 64 bytes | The generator's fixed line, as section 7 |
| Refills | One at a time, no prefetch | The generator's default, as section 7 |
| Region decode | Unchanged | Section 7's cover; only rom is executable |

`milan_soc.CTRL_FETCH_L1` holds it; `ctrl_cpu_args` hands it to the generator with the data cache and RV32M, and the all-fabric CPU keeps exactly `--xlen=32`.
`sw/builder/test_soc_options.py` restates the geometry and kills a larger and a smaller cache, a third way, one way, and the 4 KiB direct-mapped cache it replaces.

The owner amended [NFR-SCOUT-01](../reference/FR_NFR.md#34-fabric-scale-out-and-future-ports) for it on the same day.
It now requires one control hart: in the split placement it is RV32IM, with a 16 KiB two-way set-associative instruction cache (64-byte lines, LRU replacement, one refill at a time) and the coherent 8 KiB direct-mapped data cache (64-byte lines), coherent with the DMA port, with the mailbox, CSR and flash windows uncached; in the all-fabric placement it is RV32I and stays cacheless.
[The architecture](../ARCHITECTURE_HW_SW_SPLIT.md) repeats that wording.

**Out of context** (Vivado 2026.1, `AreaOptimized_high`, `xc7a100t-fgg484-2`), the split CPU and its firmware memory, the CPU clock and the bus at 10 ns, section 10's recipe:

| Split CPU | CPU WNS / WHS, ns | Bus WNS / WHS, ns | LUT | FF | The CPU's RAMB36 / RAMB18 | The CPU's tiles |
|---|---:|---:|---:|---:|---:|---:|
| 4 KiB direct-mapped fetch L1 (section 10) | +0.952 / +0.041 | +2.440 / +0.070 | 3,902 | 6,828 | 6 / 11 | 11.5 |
| 16 KiB two-way fetch L1 | +0.659 / +0.031 | +2.660 / +0.072 | 3,948 | 6,879 | 9 / 11 | 14.5 |

The route has no routing errors, and its worst CPU path is the generator's memory bridge into its read pipe (8.93 ns, 84 % route).
The cache's data takes four RAMB36 where the 4 KiB cache took one; its tags stay in the core's RAMB18.
That is CPU memory outside the 224 KB firmware allocation, so no image's plan changes with it.
[The area plan's ledger](MARK_II_AREA_PLAN.md) takes the 3 tiles: 124 after the conditional release, 2.5 over its 121.5-tile ceiling.

### The memory primitives

`plat/ctrl_mem.c`'s aligned copy and fill now move eight words a turn, then the rest by its bits, a step each: four words, two, one, a halfword, a byte.
Before, they moved four words a turn and the rest in a word loop and a byte loop.
Most calls on the record paths fill or copy a few tens of aligned bytes, so a call's fixed instructions weigh as much as its words.
In the 8x8 windows `memset` runs 15 % fewer instructions and `forward` 6 % fewer; their time is mostly the data cache's refills, which no primitive removes.
The host suite's every-alignment tests cover each new step, and six planted defects are caught.

### The record mover

[`KL_mbx_dma`](../../hdl/milan/mailbox/KL_mbx_dma.sv) sits on the mailbox's host port between `KL_mbx_wb` and `KL_mbx` and masters the CPU's coherent DMA port.
- A receive move reads a chunk of ring words into a 16-word buffer, then writes it to memory as one AXI4 burst.
- A transmit move reads a burst from memory and writes each beat to the ring.
- A burst never crosses a 64-byte line.

It adds nothing to the mailbox contract:
- it moves the ring words the driver's loop moved, in ring order;
- a transmit word's lanes past the length are zero, and a receive move leaves memory past the length untouched;
- the header words, counters and doorbells stay the driver's;
- while a move runs it owns the port, and an access of the CPU's waits for it.

Its four control registers are a CSR bank of their own (`milan_soc.CTRL_MBX_DMA_REGISTERS`), pinned below the mailbox's.
The driver (`plat/mbx_dma.h`) writes three of them and polls the fourth: four register accesses a record instead of one uncached access a word.
The split image moves every received payload and every transmitted payload on a word with it; any other build keeps the word loops.

Its word count is formed in 13 bits, so every length the 12-bit field allows, 4093 to 4095 included, is its whole words; in 12 bits those three wrapped to none, and a receive held the host port.
Out of context at 10 ns, with the mailbox's recipe, it takes 396 LUTs, 700 FFs and no block RAM, with 4.775 ns of setup and 0.189 ns of hold slack; before the 13-bit sum it took 395 LUTs.
Its bench checks it against a driver's word loop written from the contract, with a model of `KL_mbx`'s port and an AXI4 memory that stalls and errs, at every length to 96 bytes, the largest frame and the field's largest lengths; 21 planted defects are caught.
The driver's own use of it, the split image's record-mover arm, has a host test over a register model of the mover ([`test_mbx_dma_driver.cpp`](../../sw/firmware/ctrl/test/test_mbx_dma_driver.cpp)).

The CPU budget harness puts the same mover in its own test SoC and observes `KL_mbx`'s side of it.
Each request holds its fields through its answer, as `KL_mbx_wb`'s do, so the harness's observer and grader are unchanged.
With it, the driver runs half its instructions: `mbx_tx_send` takes 0.40 to 0.45 ms of an 8x8 window where it took 0.98 to 1.03, and `mbx_rx_take` 0.65 to 0.71 where it took 0.85 to 0.93.
What `mbx_rx_take` keeps is its poll and the data cache's refills of the frame the mover wrote.

### lwSRP's receive path, as a change to lwSRP

Two exact changes, drafted for lwSRP's own review and measured staged; the parent's pin stays:
- `mrp_reclaim` walks a port's attributes only after one was created or changed to a reclaimable state since the last walk, and frees the same attributes at the same calls.
  The SRP adapter calls it after every receive, and each call walked the whole list: 0.68 to 0.75 ms of an 8x8 SRP window, mostly data-cache refills, 0.18 ms with the change.
- `parse_pass` clears a decoded value only on the pass that delivers it; the validation pass cleared 64 bytes an attribute for nothing.

The adapter needs no change: its reclaim flag still saves the call.
Moving the pin is the gitlink and `ctrl_arms.LWSRP_REV` together.

### The rows

Each cell is the worst instance over the four groups in ms, arm A / arm B, bold over its own bound at the approved budget ([3.4.1](../reference/FR_NFR.md#341-control-service-budget-and-normative-timing)): min(T_svc = 20 ms, the family's ceiling), so 18 ms for the SRP rows and 20 ms for every other.
These are the figures round 8 published, graded then against the 10 ms proposed.
"Before" is section 12's "after"; "with the stack's change" adds section 12's TSN stack draft to it.
"After" is this branch: the fetch L1, the primitives and the mover.
"After, with both changes" adds the TSN stack draft and the lwSRP draft, staged.
"The fetch L1 alone" is section 12's firmware on the new CPU.

| 1x1/1if: row | before | with the stack's change | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 6.62 / 6.76 | 6.06 / 6.37 | 5.66 / 5.43 | 5.09 / 5.02 | 4.41 / 4.55 |
| ADP record, last | 4.94 / 5.06 | 4.27 / 4.50 | 4.02 / 3.88 | 3.77 / 3.56 | 3.22 / 3.24 |
| MAAP record, last | 4.93 / 5.09 | 4.31 / 4.54 | 4.06 / 3.92 | 3.81 / 3.60 | 3.25 / 3.27 |
| AECP record, last | 13.45 / 14.37 | 12.95 / 13.44 | 10.52 / 10.42 | 9.56 / 9.93 | 8.64 / 9.00 |
| SRP record, last | 15.30 / 14.84 | 14.28 / 13.91 | 11.03 / 10.71 | 10.41 / 9.91 | 9.11 / 9.26 |
| AECP record, last, in the owed window | **64.19** / **64.22** | **64.16** / **64.07** | **62.72** / **62.68** | **62.40** / **62.32** | **62.25** / **62.36** |
| A response with 7 frames owed ahead of it | **62.90** / **62.94** | **62.90** / **62.88** | **61.92** / **61.89** | **61.70** / **61.64** | **61.60** / **61.68** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | 5.44 / 5.40 | 4.89 / 4.86 | 4.19 / 4.14 | 3.91 / 3.69 | 3.44 / 3.44 |
| An ENTITY_AVAILABLE behind a full ADP ring | 3.63 / 3.86 | 3.18 / 3.42 | 3.04 / 2.97 | 2.88 / 2.72 | 2.46 / 2.48 |
| An event behind 15 others | 1.57 / 1.57 | 1.44 / 1.43 | 1.27 / 1.26 | 1.22 / 1.17 | 1.10 / 1.10 |

| 8x8/2if: row | before | with the stack's change | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 10.69 / 10.70 | 10.51 / 10.59 | 9.10 / 9.10 | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 8.13 / 8.14 | 8.01 / 8.06 | 6.91 / 6.91 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 8.12 / 8.13 | 8.00 / 8.04 | 6.89 / 6.89 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | 19.26 / 19.73 | 19.11 / **20.39** | 15.88 / 16.16 | 14.92 / 15.89 | 14.47 / 15.22 |
| SRP record, last | **21.76** / **21.07** | **21.30** / **20.86** | 16.89 / 16.64 | 16.30 / 16.39 | 15.81 / 15.19 |
| AECP record, last, in the owed window | **66.52** / **66.64** | **66.68** / **66.74** | **65.13** / **65.15** | **64.66** / **64.79** | **64.79** / **64.68** |
| A response with 7 frames owed ahead of it | **64.70** / **64.82** | **64.85** / **64.91** | **63.76** / **63.78** | **63.44** / **63.51** | **63.78** / **63.42** |
| An ACMP command behind the owed input | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |
| An ACMP command behind a full ACMP ring | 9.85 / 9.86 | 9.66 / 9.73 | 8.42 / 8.42 | 7.87 / 8.29 | 7.98 / 7.63 |
| An ENTITY_AVAILABLE behind a full ADP ring | 5.45 / 5.34 | 5.24 / 5.43 | 4.52 / 4.42 | 4.23 / 4.32 | 4.24 / 4.38 |
| An event behind 15 others | 2.65 / 2.66 | 2.61 / 2.61 | 2.19 / 2.19 | 2.15 / 2.20 | 2.15 / 2.12 |

The first records fit everywhere.
After this branch's changes every row the CPU decides fits its bound, at both points, with the drafts staged or not: at 8x8 the last AECP record takes at most 15.89 ms against 20, and the last SRP record at most 16.39 ms against 18.
Only the three rows the egress hold and `ACMP_OWED_MAX` decide miss ([What is left](#what-is-left)).

Behaviour is unchanged apart from timing, group by group, by section 12's comparison:
- this branch against the fetch L1 alone is identical in every part, at both points and arms;
- the fetch L1 alone against section 12's head differs only in MAAP's clock-seeded addresses at 1x1, as section 12 found;
- with both changes, the only other difference is the cross-channel SEQ of four transmit records in one 8x8 run, which follows the sends' timing; every egress frame is identical.

### At the approved budget

The owner approved T_svc = 20 ms on 2026-10-29 and kept 8x8 in the split's scope ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075)).
NFR-SCOUT-03 still requires every numeric normative timeout to hold with margin, so each path is graded against min(T_svc, its family's ceiling), and the CPU budget harness grades so (`grade.budget_ms`).
Every composed row was measured again at the branch's head, at the 100 MHz test clock, at both points, in both arms, with the two drafts staged and without them, as above.
Every group log and every linked image is byte-identical to the legs above: the firmware, the RTL and what the harness observes are unchanged, and only the grading moved.

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.09 / 5.02 | 4.41 / 4.55 | 8.51 / 8.94 | 8.62 / 8.28 |
| ADP record, last | 20 | 3.77 / 3.56 | 3.22 / 3.24 | 6.68 / 6.86 | 6.64 / 6.52 |
| MAAP record, last | 20 | 3.81 / 3.60 | 3.25 / 3.27 | 6.66 / 6.84 | 6.63 / 6.50 |
| AECP record, last | 20 | 9.56 / 9.93 | 8.64 / 9.00 | 14.92 / 15.89 | 14.47 / 15.22 |
| SRP record, last | 18 | 10.41 / 9.91 | 9.11 / 9.26 | 16.30 / 16.39 | 15.81 / 15.19 |
| An ACMP command behind a full ACMP ring | 20 | 3.91 / 3.69 | 3.44 / 3.44 | 7.87 / 8.29 | 7.98 / 7.63 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.88 / 2.72 | 2.46 / 2.48 | 4.23 / 4.32 | 4.24 / 4.38 |
| An event behind 15 others | 20 | 1.22 / 1.17 | 1.10 / 1.10 | 2.15 / 2.20 | 2.15 / 2.12 |
| AECP record, last, in the owed window | 20 | **62.40** / **62.32** | **62.25** / **62.36** | **64.66** / **64.79** | **64.79** / **64.68** |
| A response with 7 frames owed ahead of it | 20 | **61.70** / **61.64** | **61.60** / **61.68** | **63.44** / **63.51** | **63.78** / **63.42** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

At the 100 MHz test clock every row the CPU decides fits, at both points, in both arms, with the drafts staged or not.
The tightest is the 8x8 last SRP record: 1.61 ms under its 18 ms bound without the drafts, and 2.19 ms with them.
The 8x8 last AECP record keeps 4.11 ms without them and 4.78 ms with them.
The three bold rows are the egress's, at every clock and with every lever: the 60 ms egress hold sets the owed window's AECP record and the response with 7 frames owed ahead of it, and `ACMP_OWED_MAX` drops the command behind the owed input.

### With contract 2.3's face writer

This branch merged `dev-soft-core` `f4c9ad4f`, with lane S1's [PR #795](https://github.com/kebag-logic/milan-fpga/pull/795): contract 2.3's face block, the port census and the AECP owner's face writer (#665).
The image now commits the AECP owner's settings through the face block.
The CPU budget harness acknowledges each commit at the contract's bound, `FACE_ACK_CYCLES` bus cycles after `fw_send_o` rises ([the test SoC](../../tb/verilator/ctrl_service_budget/README.md#the-test-soc)).
The record mover, the fetch L1, the bulk primitives and the hot list stay as above.
The hot list lost one entry, the size fixture's `a_stream`, which the face's port replaced ([section 11](#11-the-firmwares-work-on-the-record-paths)).
The CPU's netlist is unchanged.
Every composed row was measured again at the merge, at the 100 MHz test clock, at both points, in both arms, with the two drafts staged and without them, graded as above:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.51 / 5.30 | 4.60 / 4.76 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 3.93 / 3.77 | 3.28 / 3.41 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 3.97 / 3.81 | 3.26 / 3.44 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 10.25 / 10.43 | 9.36 / 9.98 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 10.53 / 10.40 | 9.97 / 10.19 | 16.95 / 16.32 | 15.60 / 15.40 |
| An ACMP command behind a full ACMP ring | 20 | 4.07 / 4.04 | 3.64 / 3.70 | 8.13 / 8.15 | 7.64 / 7.45 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.02 / 2.87 | 2.58 / 2.60 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 1.24 / 1.23 | 1.14 / 1.15 | 2.09 / 2.10 | 2.01 / 2.02 |
| AECP record, last, in the owed window | 20 | **62.81** / **62.90** | **62.84** / **62.83** | **65.03** / **64.94** | **65.02** / **65.09** |
| A response with 7 frames owed ahead of it | 20 | **61.99** / **62.06** | **62.01** / **62.00** | **63.70** / **63.64** | **63.69** / **63.74** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

At the 100 MHz test clock every row the CPU decides still fits, at both points, in both arms, with the drafts staged or not.
The tightest is the 8x8 last SRP record: 1.05 ms under its 18 ms bound without the drafts, 0.56 ms less than before the merge, and 2.40 ms with them.
The 8x8 last AECP record keeps 4.16 ms without the drafts and 5.39 ms with them.
At 1x1 every such row keeps at least 7.47 ms: the last SRP record takes 10.53 ms against 18.
The first records take at most 5.12 ms, and the refilling bucket's row at most 0.23 ms.
The three bold rows are the egress's, as before.

No row here answers IN_PROGRESS.
Each commit is acknowledged within the contract's bound, so no change of face state waits.
The 12 ms bound FR_NFR 3.4.1 gives a command answered IN_PROGRESS has no measured row on the CPU.

### Instruction refills per window

The line refills of the work passes overlapping each group's composed window, with their wait, in ms, arm A / arm B:

| Window | before | the fetch L1 alone | after | after, with both changes |
|---|---:|---:|---:|---:|
| 1x1 `backlog` | 5,551 (4.90) / 5,539 (4.90) | 1,514 (1.34) / 1,497 (1.33) | 1,493 (1.32) / 1,488 (1.32) | 1,539 (1.36) / 1,529 (1.36) |
| 1x1 `backlog-adp` | 10,053 (8.92) / 9,766 (8.63) | 4,100 (3.63) / 3,877 (3.43) | 4,203 (3.71) / 4,176 (3.69) | 3,734 (3.30) / 3,697 (3.28) |
| 1x1 `backlog-adp-refill` | 11,698 (10.38) / 10,463 (9.25) | 4,216 (3.73) / 3,865 (3.42) | 4,488 (3.97) / 4,121 (3.64) | 3,995 (3.53) / 3,714 (3.29) |
| 1x1 `backlog-owed` | 11,629 (10.32) / 11,627 (10.28) | 3,856 (3.42) / 3,791 (3.36) | 4,049 (3.57) / 4,052 (3.58) | 3,642 (3.21) / 3,616 (3.22) |
| 8x8 `backlog` | 9,029 (8.04) / 9,087 (8.08) | 3,620 (3.27) / 3,569 (3.22) | 3,922 (3.48) / 3,936 (3.49) | 3,972 (3.55) / 4,021 (3.59) |
| 8x8 `backlog-adp` | 10,686 (9.53) / 10,380 (9.26) | 4,124 (3.73) / 4,000 (3.62) | 4,464 (4.01) / 4,376 (3.89) | 4,409 (3.96) / 4,473 (4.00) |
| 8x8 `backlog-adp-refill` | 11,626 (10.35) / 10,906 (9.71) | 4,314 (3.90) / 4,018 (3.63) | 4,642 (4.18) / 4,383 (3.90) | 4,522 (4.06) / 4,409 (3.94) |
| 8x8 `backlog-owed` | 12,331 (11.01) / 12,592 (11.25) | 3,847 (3.49) / 3,770 (3.42) | 4,170 (3.75) / 4,195 (3.73) | 4,002 (3.61) / 4,244 (3.79) |

The fetch L1 takes 60 to 70 % of the refills out of every window.
Section 12's model had predicted the refill count well, but not the rows: measured, they came out 0.8 to 1.6 ms above its figures, because the rest of each window did not stay as the model held it.

### What holds the 8x8 rows

With both changes, each 8x8 window whose last AECP or SRP record took 13.2 to 15.8 ms runs 266,000 to 311,000 instructions.
It waits on instruction refills for 3.0 to 4.0 ms and has a data-cache refill outstanding for 2.5 to 3.7 ms.
By module family it is spread: lwSRP 2.4 to 3.5 ms, ACMP's core 2.3 to 2.6, the memory primitives 2.0 to 2.5, AECP 1.1 to 2.0, the SRP adapter 1.4 to 2.0, the mailbox driver 1.3 to 1.7.
No single function holds 1.3 ms.
The levers this page has named are taken; what is left is the work itself at the composed 8x8 load.

### At the Milan clock, and the per-pass share

This subsection is the record of 2026-10-29, before the [owner's decision of 2026-10-30](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239): the product clocked the split CPU from the Milan clock, 50 MHz, with its bus at 100 MHz (`cpu_clk` from `ClockSignal("milan")`; `milan_clk_hz` in both ax7101 configurations, which the builder holds to the bare-metal build contract's clock).
The figures above in this section, and in sections 11 and 12, are at a 100 MHz CPU clock, or 150 MHz where section 11 says so: test clocks, not that day's product ([#665 correction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508196970)).
The owner's decisions of 2026-10-29, no clock increase and T_svc = 20 ms, were taken on those figures, and that decision of 2026-10-30 answered the clock question again.

The CPU budget harness then ran the split CPU at the Milan clock by default, and any other CPU clock only as a labelled option.
Every composed row was measured at both clocks, at both points, in both arms, with the two drafts staged and without them, graded as above.
The images are byte-identical to the merge's legs above, the CPU's netlist is the same, and at 100 MHz every probe's CPU cycles at 1x1 arm A equal those legs'.
The mover's word count now takes the length field's 4093 to 4095 without a wrap; no record has such a length, and the rows do not move.

With the CPU at that day's product clock, the Milan clock, 50 MHz, and the bus at 100 MHz (ms, arm A / arm B, bold over the row's own bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 8.65 / 8.90 | 7.64 / 7.46 | 14.37 / 14.72 | 13.79 / 13.80 |
| ADP record, last | 20 | 6.08 / 6.38 | 5.51 / 5.36 | 11.20 / 11.23 | 10.59 / 10.61 |
| MAAP record, last | 20 | 6.11 / 6.42 | 5.50 / 5.34 | 11.19 / 11.21 | 10.57 / 10.59 |
| AECP record, last | 20 | 15.95 / 17.05 | 14.87 / 15.76 | **25.02** / **25.61** | **24.02** / **24.11** |
| SRP record, last | 18 | 17.81 / 17.02 | 16.34 / 16.26 | **28.25** / **27.25** | **25.66** / **25.45** |
| An ACMP command behind a full ACMP ring | 20 | 6.83 / 6.78 | 6.01 / 6.09 | 13.57 / 13.60 | 12.71 / 12.72 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 4.55 / 4.88 | 4.38 / 4.26 | 7.63 / 7.87 | 7.32 / 7.23 |
| An event behind 15 others | 20 | 2.06 / 2.06 | 1.88 / 1.89 | 3.63 / 3.64 | 3.46 / 3.48 |
| AECP record, last, in the owed window | 20 | **64.73** / **64.67** | **64.66** / **64.65** | **68.53** / **68.46** | **68.71** / **68.75** |
| A response with 7 frames owed ahead of it | 20 | **63.41** / **63.33** | **63.35** / **63.33** | **66.26** / **66.20** | **66.41** / **66.45** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

With the CPU at that day's labelled 100 MHz option, behind the crossing, and the bus at 100 MHz, the same legs as the merge's above:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.51 / 5.30 | 4.60 / 4.76 | 8.79 / 8.82 | 8.30 / 8.12 |
| ADP record, last | 20 | 3.93 / 3.77 | 3.28 / 3.41 | 6.67 / 6.69 | 6.31 / 6.33 |
| MAAP record, last | 20 | 3.97 / 3.81 | 3.26 / 3.44 | 6.65 / 6.68 | 6.29 / 6.32 |
| AECP record, last | 20 | 10.25 / 10.43 | 9.36 / 9.98 | 15.10 / 15.84 | 13.74 / 14.61 |
| SRP record, last | 18 | 10.53 / 10.40 | 9.97 / 10.19 | 16.95 / 16.32 | 15.60 / 15.40 |
| An ACMP command behind a full ACMP ring | 20 | 4.07 / 4.04 | 3.64 / 3.70 | 8.13 / 8.15 | 7.64 / 7.45 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.02 / 2.87 | 2.58 / 2.60 | 4.13 / 4.32 | 3.33 / 4.03 |
| An event behind 15 others | 20 | 1.24 / 1.23 | 1.14 / 1.15 | 2.09 / 2.10 | 2.01 / 2.02 |
| AECP record, last, in the owed window | 20 | **62.81** / **62.90** | **62.84** / **62.83** | **65.03** / **64.94** | **65.02** / **65.09** |
| A response with 7 frames owed ahead of it | 20 | **61.99** / **62.06** | **62.01** / **62.00** | **63.70** / **63.64** | **63.69** / **63.74** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

At that day's 50 MHz:
- **At 1x1/1if every row the CPU decides fits**, in both arms, with the drafts staged or not.
  The tightest is the last SRP record, 17.81 ms against 18; the last AECP record takes at most 17.05 ms.
- **At 8x8/2if the last AECP record misses its bound**: 25.02 to 25.61 ms against 20, and 24.02 to 24.11 with both drafts.
- **At 8x8/2if the last SRP record misses its bound**: 27.25 to 28.25 ms against 18, and 25.45 to 25.66 with both drafts.
- Every other row the CPU decides fits at 8x8; the tightest of them is the last ACMP record, at most 14.72 ms against 20.

At the 100 MHz option every row the CPU decides fits at both points, as above.
The three egress-held rows miss at both clocks, as before.

**The per-pass share.**
A pass is the only opportunity to take an input, and the deepest admitted wait is seven owed frames, answered in pass 8 after the room returns, so nine passes must fit the smallest bound every input shares (`ctrl_loop.h`, THE SHARE).
That bound is SRP's 18 ms, so the share is 2.0 ms of CPU time: 100,000 CPU cycles at 50 MHz and 200,000 at 100 MHz.
The harness holds every work pass of every group to it, apart from the rows (`share.py`, `grade.pass_share`), and a pass over it fails the run unless `--record-share-findings` records it.

Each group's work passes against the share, over the four groups' runs (arm A / arm B: the passes over it of the passes run, and the longest pass in ms, bold where any is over):

| CPU clock | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 50 MHz (that day's product) | 0 of 1273, 1.89 / 0 of 1245, 1.89 | 0 of 1264, 1.71 / 0 of 1246, 1.72 | **32 of 1310, 3.46** / **30 of 1286, 3.47** | **24 of 1307, 3.28** / **23 of 1285, 3.30** |
| 100 MHz (option) | 0 of 1272, 1.14 / 0 of 1248, 1.14 | 0 of 1273, 1.04 / 0 of 1249, 1.06 | **1 of 1311, 2.29** / **2 of 1284, 2.30** | **1 of 1332, 2.20** / **1 of 1298, 2.20** |

- **At 1x1/1if every pass fits the share at both clocks**: the longest is 1.89 ms at 50 MHz.
- **At 8x8/2if, at 50 MHz, 23 to 32 of each run's passes are over it**, in two kinds:
  - in every group, three passes before any load, at about 172, 368 and 568 ms of the run: 101,111 to 120,378 cycles, 2.02 to 2.41 ms; lwSRP's MRP work for the two interfaces is about half of each (`mrp_mad`, 59,778 of the 119,836 cycles of the one the experiment below shows);
  - in every composed window, up to six of its first passes: 100,328 to 173,282 cycles, 2.01 to 3.47 ms, whose largest modules are the memory primitives, ACMP's core, lwSRP and the SRP adapter.
- **At 8x8/2if, at 100 MHz, one or two passes are over it**: the `backlog` window's first, 2.29 to 2.30 ms, and 2.20 ms with both drafts.

**A split by the loop's own constant does not bring them within it.**
In a labelled experiment, not on this branch, `CTRL_LOOP_RX_PER_PASS` took one record of a channel a pass instead of two (owner decision D4(b) set two), at 8x8/2if, arm A, without the drafts:

| 8x8/2if, arm A, without the drafts | Bound, ms | CPU 50 MHz (that day's product): two records a pass (the branch) | one (the experiment) | CPU 100 MHz (option): two | one |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 14.37 | 19.25 | 8.79 | 11.79 |
| ADP record, last | 20 | 11.20 | 13.99 | 6.67 | 8.32 |
| MAAP record, last | 20 | 11.19 | 12.64 | 6.65 | 7.50 |
| AECP record, last | 20 | **25.02** | **22.84** | 15.10 | 14.11 |
| SRP record, last | 18 | **28.25** | **34.87** | 16.95 | **20.86** |
| An ACMP command behind a full ACMP ring | 20 | 13.57 | 17.69 | 8.13 | 10.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 7.63 | 11.69 | 4.13 | 7.29 |
| An event behind 15 others | 20 | 3.63 | 3.02 | 2.09 | 1.77 |
| Work passes over the 2.0 ms share | 2.0 | **32 of 1310, longest 3.46 ms** | **18 of 1380, longest 2.84 ms** | **1 of 1311, longest 2.29 ms** | 0 of 1380, longest 1.67 ms |

At 50 MHz it shortens the composed windows' longest pass but leaves the passes before any load as they were, and it lengthens the last SRP and ACMP records, which take twice as many passes.
At 100 MHz every pass then fits the share, and the last SRP record misses its 18 ms bound.
No figure of records a pass serves both the share and the rows at 8x8, so the branch keeps two.
The passes before any load are lwSRP's MRP work, which a record count does not reach.
So at that day's clock the 8x8 last AECP and SRP records and the 8x8 passes missed, and the owner decided the split CPU's clock on 2026-10-30 ([below](#the-split-cpu-on-sys-at-100-mhz)).

### The split CPU on `sys` at 100 MHz

The [owner's decision of 2026-10-30](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239) moved the split CPU from the Milan clock to `sys`, the 100 MHz bus clock the mailbox, its record mover and the firmware memory run on.
`milan_soc.CTRL_CPU_CD` names that domain, and `MilanSoC` refuses any other for the split placement, the Milan clock among them.
The all-fabric CPU, the Milan datapath clock, the PHC, the media grids and every `MILAN_CLK_FREQ_HZ` derivation do not change.

The memory crossing is removed, not kept degenerate.
With the CPU on the bus's own clock the generator's `with_cpu_clk` is off and `cross_cpu_memory_ports` leaves the CPU alone, so no `StreamFifoCC` or `cpu_clk` port is built: a crossing between one clock's edges would cost its cycles and its area for nothing.
Every CPU-clock constant comes from the CPU's own clock: the mailbox's millisecond tick from `sys`, the loop's share as 200,000 CPU cycles, and the harness's `cpu_hz` from `MilanSoC.cpu_clk_freq`.
The CPU budget harness and the split boot simulation both build through `ctrl_cpu_cd` and refuse a CPU with a clock of its own; a CPU budget build that records its CPU anywhere else is refused, built or reused.

Out of context, the product split CPU netlist on `sys` (`VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f`) with `rom` and `sram` built from the 1x1 image, its LiteDRAM port brought out to pins, routed at 10 ns with the method of section 9:

| Split CPU | WNS / WHS, ns | LUT | FF | The CPU's RAMB36 / RAMB18 | The CPU's tiles | Route |
|---|---:|---:|---:|---:|---:|---|
| 16 KiB two-way fetch L1, behind the crossing at 100 MHz ([above](#the-fetch-l1)) | CPU +0.659 / +0.031, bus +2.660 / +0.072 | 3,948 | 6,879 | 9 / 11 | 14.5 | no routing error |
| 16 KiB two-way fetch L1, on `sys` at 100 MHz | +1.605 / +0.070 | 3,543 | 5,643 | 6 / 7 | 9.5 | no routing error |

Without the crossing the CPU is 405 LUTs, 1,236 FFs and 5 tiles smaller.
Its worst path runs from the generator's peripheral bridge into the interrupt controller's gateways, 8.015 ns, 76 % route.
Out of context, with nothing else on the device, this is an upper bound; the routed split image is lane S9's.

Every composed row was measured on the merged head, with the CPU on `sys` at 100 MHz and the bus on the same clock, at both points, in both arms, with the two drafts staged and without them, graded against min(T_svc, its family's ceiling) with T_svc = 20 ms (ms, arm A / arm B, bold over the row's own bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, last | 20 | 5.16 / 5.06 | 4.34 / 4.52 | 7.76 / 7.98 | 7.42 / 7.30 |
| ADP record, last | 20 | 3.65 / 3.59 | 3.18 / 3.22 | 5.81 / 5.85 | 5.26 / 5.08 |
| MAAP record, last | 20 | 3.68 / 3.63 | 3.22 / 3.26 | 5.80 / 5.84 | 5.30 / 5.12 |
| AECP record, last | 20 | 9.67 / 10.02 | 8.72 / 9.48 | 14.41 / 15.16 | 13.79 / 14.05 |
| SRP record, last | 18 | 9.95 / 10.00 | 9.49 / 9.68 | 15.88 / 15.96 | 14.84 / 14.81 |
| An ACMP command behind a full ACMP ring | 20 | 3.45 / 3.47 | 3.03 / 3.11 | 6.51 / 6.73 | 6.19 / 6.21 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.73 / 2.74 | 2.42 / 2.45 | 3.53 / 4.19 | 3.95 / 4.11 |
| An event behind 15 others | 20 | 0.88 / 0.89 | 0.78 / 0.80 | 1.44 / 1.45 | 1.35 / 1.35 |
| AECP record, last, in the owed window | 20 | **62.66** / **62.73** | **62.75** / **62.77** | **64.99** / **64.95** | **64.94** / **65.01** |
| A response with 7 frames owed ahead of it | 20 | **62.07** / **61.93** | **61.94** / **61.95** | **63.68** / **63.93** | **63.91** / **63.68** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Every row the CPU decides fits, at both points, in both arms, with the drafts staged or not.
The tightest is the 8x8 last SRP record, 15.96 ms against 18, 14.84 with both drafts; the 8x8 last AECP record takes at most 15.16 ms against 20.
At 1x1 they take 10.00 and 10.02 ms.
The three egress-held rows miss as before: they hold the egress for 60 ms, and stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).

The per-pass share, 2.0 ms, 200,000 CPU cycles: the passes over it of the work passes run over the four backlog groups, and the longest in ms (arm A / arm B):

| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---:|---:|---:|---:|
| 0 of 1277, 1.07 / 0 of 1250, 1.07 | 0 of 1279, 0.98 / 0 of 1250, 0.98 | 0 of 1319, 1.97 / 0 of 1286, 1.92 | 0 of 1310, 1.77 / 0 of 1302, 1.77 |

No pass is over the share in any leg, nor in any of the harness's other groups, which arm A also ran at both points.
Over every group the longest at 8x8 is 1.97 ms, at 1x1 1.21 ms.

**The pass that was over it.**
On the merged head before this change one 8x8 pass was over the share in each arm, 2.21 and 2.22 ms, in the `backlog` window, and in no other window.
It was the pass that took the row's own LINK event: SRP's `reset_interface` destroyed the interface's participants and built new ones in the event, about 110,000 CPU cycles at 8x8 of the 200,000.
The count of events a pass takes is not what sets it: at six events a pass that pass was 2.207 ms, and at four 2.108 ms, the LINK event arriving in a later pass with the same work (labelled experiments, not on this branch).
So a link change now takes two passes (`srp_bounds.h`): the pass that takes it withdraws and destroys, the next pass's poll builds, and SRP's receive waits until then, so no record meets an interface with no participants and neither pass also runs an SRP record.
Any number of link edges in a pass builds once, which a pass of eight used to do eight times.

**The other groups.**
Three things the composed rows do not reach showed only when every group ran at 100 MHz.
The flash window was cacheable in the test SoC, for the hybrid-XIP arm, so the saved-state store read flash through the data cache, which the product never does: its read and its buffer met at one cache index, and one pass in each save took 12.4 ms at 8x8 and 4.1 ms at 1x1 (a labelled control restores it).
The window is now the product's in every arm but hybrid-XIP's, and a build with another is refused.
An AECP group sent its next frame when the last settled, so at 100 MHz it outran the channel's refill of one frame every 5 ms, and the filter refused the frames past its burst; each frame now waits that period.
And through the product's uncached window a read of the store's whole page takes 1.40 ms, which with lwSRP's periodic work in the same tick put an 8x8 pass at 2.26 ms.
The store's blank check and verify now read back 128 bytes a step (`NVM_READ_BYTES`), so a save's read-back takes twice as many ticks: at 8x8 the blank check and the verify are 2.08 s of ticks, 1.04 s before, and a save there is 4,697.1 ms from the change to durable on a flash with no busy time (measured at that head on 2026-11-02, [below](#a-save-in-a-composed-window-and-both-links-at-once)).
The owner's 0.5 s ([#823](https://github.com/kebag-logic/milan-fpga/issues/823)) is the append-only design's, not this image's.

**The hybrid-XIP arm's two windows.**
At the CPU's old 50 MHz, the 1x1, 4 KiB arm's `backlog-adp` and `backlog-adp-refill` were refused: the fifteen grandmaster changes arrive 8 bus cycles apart and the source coalesces while its record waits, so with k records held only 16 - k + 1 commit, and those windows opened with 4 or 5 records held.
That was the window's definition, not the firmware's defect: it named a population only a drained ring can take, and waited a fixed time for one.
Every backlog window now opens on a drained ring (`scenario.OPEN_WINDOW`), its table gives the records held at its opening, and a refusal names them.
At 100 MHz all four windows take their fifteen, with no record held, so that arm's composed maximum covers all four ([the harness](../../tb/verilator/ctrl_service_budget/README.md#the-instruction-cache)).

### A save in a composed window, and both links at once

This subsection is the record of 2026-11-02 (#665); the one above is the record of `c954b8a9`, the head before it.
Two kinds of pass the groups above never staged were over the share at that head, measured with the probe groups published in the review of [PR #810](https://github.com/kebag-logic/milan-fpga/pull/810) (a labelled patch, not on this branch).
In a pass that also carried a composed window's heaviest work, the saved-state store's flash step took the pass to 2.39 ms in `backlog`'s window, 3 of 6 tick phases over, and to 2.72 ms in `backlog-adp`'s, 7 of 8 over.
With both links changing together SRP built both interfaces in one pass: 2.08 ms under `backlog-adp`'s load, 2.004 ms under `backlog`'s.
No row missed its bound in any of them; the closest was the last SRP record, 17.55 ms against 18.

**The store's steps on the product SoC.**
One save with no other load, the CPU on `sys` at 100 MHz, through the product's uncached flash window and its command master.
Each cell is the flash port's and the store's CPU cycles in the step's pass, the most of any step of its kind, from a measurement-only build that prints every pass running the flash port and every journal read (not on this branch):

| Step | 1x1/1if | 8x8/2if |
|---|---:|---:|
| Erase issue | 5,051 | 5,112 |
| Busy poll, the erase or the program not yet done | 3,994 | 4,710 |
| Blank-check read-back, 128 bytes | 73,491 | 72,841 |
| Page program issue | 95,373 | 95,386 |
| Verify read-back, 128 bytes, compared with the stage | 76,234 | 76,737 |

A read-back reads 128 bytes through the uncached window, each byte one SPI read; a program step issues one page through the command master a byte at a time.
The program's issue is the longest step, 95,386 cycles, within the 1.0 ms THE STEP gives it.

**THE STEP.**
The loop now owns the pass's time (`ctrl_loop.h`, THE STEP).
It reads the store's clock once as a pass starts, and after the polls of a pass that took no event and no record it hands the store's step the clock's value at which the pass has spent its share.
The store's centisecond consumer only owes a step, and the step is taken only while `NVM_STEP_US`, 1.0 ms, is left before that deadline: a pass that carries one has spent at most 1.0 ms before it and adds the step's own cost.
A step without room stays owed, and the centiseconds that pass meanwhile owe it once, so the store never takes two steps in one pass or catches up in a burst.
It waits for a pass that took no input because a step in a pass that took records delays the records behind them.
With the room gate alone every pass of the 14 save windows then graded fit, but at 8x8 the deferred read-backs fell in the passes that drain SRP's full ring, and the last SRP record took 18.02 to 18.21 ms against 18 in four blank-check windows (a labelled attempt, not on this branch).
The harness now holds every pass to the share, those that write nothing to the mailbox too, by their run's longest, since a deferred step can be all such a pass does.

**A save in each flash phase.**
`save_window.py` opens `backlog-adp`'s window, the heaviest the harness stages, during each flash phase of a save, at eight phases of that phase's heavy step: 1.25 ms apart across the 10 ms tick for the blank check and the verify, 2.5 ms apart across the program phase's 20 ms.
Each phase starts at a flash event of the save itself, and `grade.save_phase` refuses a window that did not open inside it.
The 24 windows ran at both points, in both arms, with the two drafts staged and without them: no pass is over the share in any of them, 0 of 99,289 passes.
Over the lone save, in a build that printed every pass running the flash port, a pass that carries a step is at most 1.21 ms at 1x1 (a blank-check read-back's) and 1.26 ms at 8x8 (a page program's issue), arm A without the drafts; over the 24 windows at 8x8, the same arm, it is at most 1.02 ms; arm B's windows and the drafted ones were bounded only by their longest pass, 1.98 ms at 8x8, which carries none ([the passes at the next head](#a-saves-worst-case-and-one-build-a-pass-either-way) are every one that carries a step).
Their rows (ms, arm A / arm B, bold over the row's own bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.48 / 1.46 | 1.41 / 1.37 | 1.85 / 1.87 | 1.71 / 1.81 |
| ADP record, first | 20 | 1.47 / 1.45 | 1.40 / 1.36 | 1.84 / 1.86 | 1.70 / 1.80 |
| MAAP record, first | 20 | 1.51 / 1.49 | 1.43 / 1.39 | 1.88 / 1.89 | 1.73 / 1.84 |
| AECP record, first | 20 | 1.52 / 1.50 | 1.44 / 1.40 | 1.89 / 1.90 | 1.74 / 1.85 |
| SRP record, first | 18 | 2.68 / 2.59 | 2.44 / 2.41 | 4.39 / 4.38 | 4.08 / 4.01 |
| ACMP record, last | 20 | 5.95 / 5.92 | 5.47 / 5.33 | 8.89 / 9.30 | 8.20 / 8.39 |
| ADP record, last | 20 | 4.44 / 4.42 | 4.10 / 4.02 | 6.44 / 6.85 | 5.94 / 6.24 |
| MAAP record, last | 20 | 4.47 / 4.46 | 4.14 / 4.06 | 6.48 / 6.89 | 5.96 / 6.28 |
| AECP record, last | 20 | 10.86 / 11.15 | 10.22 / 10.34 | 15.86 / 16.79 | 14.51 / 15.38 |
| SRP record, last | 18 | 11.17 / 11.14 | 10.60 / 10.31 | 16.99 / 17.29 | 15.79 / 15.46 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 3.57 / 3.55 | 3.32 / 3.26 | 5.29 / 5.40 | 4.87 / 4.96 |

Every row fits in every window, at both points, in both arms, with the drafts staged or not.
The tightest is the 8x8 last SRP record, 17.29 ms against 18 in arm B and 16.99 in arm A, 15.79 and 15.46 with both drafts; the last AECP record takes at most 16.79 ms against 20, and at 1x1 the two take at most 11.17 and 11.15 ms.
A save adds to them because its step can be running when the window's records arrive, and they wait for that pass: at 8x8 the last SRP record takes 0.43 and 0.83 ms more, arm A and arm B, than in `backlog-adp`'s window with no save, 16.56 and 16.46 ms.

**The planted store step.**
`--mutation store-step-unbounded` hands the step a deadline no pass reaches and takes it in every pass that owes it, as before THE STEP.
At 8x8, arm A, it puts 15 of the 24 windows over the share, the longest pass 2.71 ms.
In 5 of them every row fits its bound, so only the share catches it; in 10 the last SRP record is over 18 ms as well, 18.004 to 18.59, and in one it is over, 19.00 ms, with no pass over.
The run prints `CONTROL store-step-unbounded caught`, and a run in which every window with a pass over also had a row over would print `ESCAPED`.

**A save from the change to durable.**
From the SET_NAME to the end of the step that reads back the container's last bytes, which moves the authority, one save with no other load, on the harness's flash model, which has no busy time: at 8x8 4,697.1 ms at `c954b8a9` and 4,697.4 ms at this head; at 1x1 2,018.4 ms at this head.
The first 1,000 ms are DR2a's first-dirty window, then the capture and the seal; the blank check and the verify read back 128 bytes a step, one step a tick, 104 ticks each at 8x8 for 13,256 bytes, 27 at 1x1 for 3,336, where a whole page a step took half as many.
A real part's erase and page-program waits add to it; the store polls them, a step a tick.
The owner's 0.5 s ([#823](https://github.com/kebag-logic/milan-fpga/issues/823)) is the append-only design's in Mark II, not this image's, and this change does not claim it.

**Both links at once.**
A poll now builds one interface at most (`srp_bounds.h`): the other is built on the next pass, and the interface whose build waited goes first after that.
`Srp.JointLinkChangeBuildsOneInterfaceAPass` fails on an image that builds both in one pass.
At this head, at 8x8, the same probe groups put no pass over the share: both links dropping under `backlog-adp`'s load (`y-links`) take a longest pass of 1.76 / 1.82 ms (arm A / arm B), and under `backlog`'s (`x-links-same`) 1.54 / 1.56 ms.
With a save in progress, arm A, `backlog`'s window's longest pass is 1.63 ms and `backlog-adp`'s 1.98 ms, against 2.39 and 2.72 ms at `c954b8a9`.
Every row fits in them, the last SRP record at most 16.62 ms.

**The rows at this head.**
The four backlog windows, every leg rebuilt at this head (ms, arm A / arm B, bold over the row's own bound):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.79 | 0.71 / 0.72 | 1.32 / 1.39 | 1.23 / 1.24 |
| ADP record, first | 20 | 0.82 / 0.83 | 0.75 / 0.76 | 1.37 / 1.43 | 1.28 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.81 | 0.73 / 0.74 | 1.35 / 1.41 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.82 | 0.74 / 0.75 | 1.36 / 1.42 | 1.27 / 1.28 |
| SRP record, first | 18 | 2.88 / 2.92 | 2.68 / 2.70 | 5.42 / 5.61 | 5.06 / 5.06 |
| ACMP record, last | 20 | 5.06 / 5.18 | 4.79 / 4.60 | 7.85 / 8.31 | 7.28 / 7.37 |
| ADP record, last | 20 | 3.52 / 3.68 | 3.38 / 3.30 | 5.85 / 6.07 | 5.38 / 5.35 |
| MAAP record, last | 20 | 3.54 / 3.72 | 3.42 / 3.33 | 5.84 / 6.06 | 5.36 / 5.33 |
| AECP record, last | 20 | 9.68 / 10.17 | 9.44 / 9.60 | 14.69 / 15.96 | 13.58 / 14.35 |
| SRP record, last | 18 | 10.58 / 10.47 | 9.74 / 9.58 | 16.56 / 16.46 | 15.33 / 14.81 |
| An ACMP command behind a full ACMP ring | 20 | 3.59 / 3.63 | 3.27 / 3.28 | 6.59 / 7.01 | 6.36 / 6.37 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.81 / 2.81 | 2.54 / 2.53 | 3.60 / 4.42 | 3.29 / 3.95 |
| An ENTITY_AVAILABLE behind the ADP ring, its bucket refilling (observed) | 20 | 0.08 / 0.10 | 0.13 / 0.06 | 0.12 / 0.12 | 0.19 / 0.25 |
| An event behind 15 others | 20 | 0.92 / 0.93 | 0.85 / 0.88 | 1.47 / 1.54 | 1.38 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.90** / **63.01** | **62.90** / **62.87** | **65.10** / **65.31** | **65.12** / **65.14** |
| A response with 7 frames owed ahead of it | 20 | **62.05** / **62.14** | **62.03** / **62.02** | **63.75** / **64.19** | **63.75** / **63.76** |
| An ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

Every row the CPU decides fits, at both points, in both arms, with the drafts staged or not; the three egress-held rows miss as before, and stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).
Against `c954b8a9` the 8x8 last SRP record rose from 15.88 and 15.96 ms to 16.56 and 16.46.
A pass of SRP's drain now runs 68 more instructions, the clock read THE STEP makes as each pass starts, but takes about 3,300 more CPU cycles, about half of them waiting on instruction fetch because the code's layout moved (`backlog-adp`, arm A, the pass 11.1 ms into the window at each head); the record waits sixteen such passes.

The per-pass share, 2.0 ms: the passes over it, those that write nothing to the mailbox counted by their run's longest, of the work passes run, and the longest in ms (arm A / arm B):

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1280, 1.10 / 0 of 1251, 1.10 | 0 of 1276, 1.01 / 0 of 1250, 1.01 | 0 of 1314, 1.96 / 0 of 1286, 1.95 | 0 of 1317, 1.86 / 0 of 1286, 1.82 |
| A save's 24 windows | 0 of 11195, 1.22 / 0 of 8643, 1.21 | 0 of 11134, 1.18 / 0 of 8631, 1.16 | 0 of 18088, 1.95 / 0 of 11745, 1.98 | 0 of 18111, 1.86 / 0 of 11742, 1.83 |
| Every group the leg ran | 0 of 19927, 1.22 / 0 of 10496, 1.21 | 0 of 13012, 1.18 / 0 of 10483, 1.16 | 0 of 27214, 1.96 / 0 of 13648, 1.98 | 0 of 20045, 1.86 / 0 of 13645, 1.83 |

**The boot simulation's flash window.**
The split boot simulation now builds the product's uncached flash window, and refuses an export without it.
At `c954b8a9` the window alone moves the boot to ready from 24.660 to 25.413 ms at 1x1 and from 64.271 to 65.026 ms at 8x8; at that subsection's head it was 25.515 and 64.885 ms, and at the next subsection's 25.477 and 64.584 ms ([the boot simulation](../../tb/verilator/ctrl_split_boot/README.md#results)).

### A save's worst case, and one build a pass either way

This subsection is the record of 2026-11-03 (#665); the one above is the record of `4f58214f`, the head before it.
At that head a save advanced only through passes that took no input, and nothing bounded how long input could keep them from coming (the round 13 reviews of [PR #810](https://github.com/kebag-logic/milan-fpga/pull/810)).

**THE STEP's age limit.**
A step not run for more than `CTRL_LOOP_STEP_AGE` centiseconds, two, is the whole of the next pass: the loop calls it before it takes any input, with the deadline read as the pass starts, and returns one, so the input it held off is taken by the next pass (`ctrl_loop.h`, THE STEP).
The age is the centiseconds the loop has dispatched since the step last ran or owed nothing; a step it had no room for keeps its age.
Under input that leaves no pass empty the store then steps once every three ticks, and an input waits one step at most: the longest step's own CPU time is at most 0.966 ms (`NVM_STEP_US` gives it 1.0 ms), and a pass taken whole by an aged step is that step and the loop's clock read; from [the next subsection](#aged-windows-a-change-while-a-save-is-in-flight-and-the-retry)'s head on, also THE RETRY's round, so an input waits one step and one round.
`Loop.L13AnAgedStepIsAPassOfItsOwn` and its ten planted defects hold the rule.

**Why two.**
The limit decides how often a window takes an aged step, not whether: a window that opens with the step's age at the limit, after input that left no pass empty, takes one among its records at its next centisecond at any limit, and no window takes two, since none drains in two ticks.
The step's age counts the centiseconds dispatched since it last ran or owed nothing, and in every window the harness stages from idle, at both points, in both arms, with and without the drafts, at most two centiseconds were posted in TICK records between two passes that carried a step (one at 1x1): with the limit at two a window opened from idle takes no aged step, and with it at one it would take one at its second centisecond.
Every row fits with the aged step a window opened at the limit takes, at each placement measured: the least margin is 0.101 ms, against 0.77 ms stated here at first, which held for windows opened from idle only ([the next subsection](#aged-windows-a-change-while-a-save-is-in-flight-and-the-retry)).
At `a3f23bba` the heaviest windows held the step off longest: at 8x8 the longest gap between two passes that carried a step, in a save's verify windows, was 26.36 ms in arm A and 26.40 ms in arm B, with two centiseconds between them; at 1x1 it was 19.69 ms, with one.
In the starved saves, where every step comes through the limit, the longest gap is 31.3 to 31.5 ms at 8x8 and 31.0 to 31.1 ms at 1x1: three ticks and the passes that dispatch them.

**A save's worst case.**
The store owes a step each centisecond, and the loop takes one at least every three ticks under any input, so with no save in flight a change is durable at most

> T ≤ 1,000 ms + S × 3 × 10 ms + 10 ms

after its change.
1,000 ms is DR2a's first-dirty window; S is its steps from the first after that window to durable: the step that starts the capture, one for each changed record and one that finds none left, the seal's 256-byte stretches of the container less its trailer, the erase and its wait, the blank check's 128-byte read-backs, each page's issue and its wait, and the verify's read-backs; 10 ms covers the change's own pass and the passes between a tick and the aged step it triggers.
A SET_NAME of the entity marks both its names (`aecp_nvm.c` marks every name of the descriptor it names), so at 8x8/2if, a 13,256-byte container, S = 1 + 3 + 52 + 2 + 104 + 104 + 104 = 370 and T ≤ 12,110 ms; at 1x1, 3,336 bytes, S = 102 and T ≤ 4,070 ms; each further changed record adds one step, 30 ms (`nvm_store.h`, `save_window.bound_ms`).
A change marked while a save is in flight, once its capture has passed the change's record, waits for the rest of that save first, so a change's worst case is longer: 22,150 ms at 8x8/2if and 6,070 ms at 1x1 ([the next subsection](#aged-windows-a-change-while-a-save-is-in-flight-and-the-retry)).
That is on the harness's flash model, which has no busy time: a part's erase adds at most its erase time, and each page program at most its program time (the next subsection gives the product part's figure).
The owner's 0.5 s ([#823](https://github.com/kebag-logic/milan-fpga/issues/823)) applies to the firmware writer of the append-only design through this same step; this image states its own worst case and does not meet 0.5 s.

**A save under load.**
`save-held` holds every receive channel at its contract refill rate with its bursts from the save's change until its worst case has passed: admission's records at once, again every as many refill periods, each channel's bursts 0.2 ms apart, AECP's first one refill period after the change, since the SET_NAME takes one of its tokens.
`save-starved` adds a grandmaster change as every pass starts, an event source the contract coalesces but does not rate, so no pass takes nothing and the store steps only through the age limit.
Each is timed from the change to the read-back that completes its verify (`save_grade.save_time`), and a held group that commits fewer records than its load offered is refused:

| Save, ms from the change to durable (arm A / arm B) | Worst case, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| `save`, alone | 4,070; 12,110 | 2,019.2 / 2,018.4 | 2,018.3 / 2,018.3 | 4,697.4 / 4,697.4 | 4,697.4 / 4,698.3 |
| `save-held` | 4,070; 12,110 | 2,019.0 / 2,018.1 | 2,018.1 / 2,018.1 | 4,696.9 / 4,696.7 | 4,697.0 / 4,731.1 |
| `save-starved` | 4,070; 12,110 | 4,049.0 / 4,048.1 | 4,047.9 / 4,048.0 | 12,087.0 / 12,087.0 | 12,087.1 / 12,088.0 |
| `save-starved`, longest gap between flash steps | | 30.98 / 30.97 | 31.08 / 31.05 | 31.33 / 31.25 | 31.48 / 31.42 |

Every save is within its worst case at both points, in both arms, with the drafts staged or not, and no pass is over the share in either held group.
Under the held load alone a save takes what it takes alone, 4,696.7 to 4,731.1 ms at 8x8 against 4,697.4 to 4,698.3 ms, since the contract's records leave passes that take nothing: its longest gap between flash steps is 17.7 to 19.5 ms.
Starved, it steps through the limit, every 31.0 to 31.5 ms, and is durable 12,087.0 to 12,088.0 ms after its change at 8x8, 22 ms inside the worst case, and 4,047.9 to 4,049.0 ms at 1x1.
Each channel's longest record under the held load is within its bound: at 8x8 the SRP record at most 14.81 ms against 18 and the AECP record 11.49 ms against 20.
A read-back run in the log spans one step's reads, or two steps' within a millisecond of each other, as a step held off past a tick and the next one can be; the time to durable counts their bytes.

**The planted age limit's removal.**
`--mutation store-step-ageless` takes the step only in a pass that took no input, as before the age limit.
At 8x8, arm A, under `save-starved`'s load it never takes the step after the change: the save is not durable 12,618.4 ms after its change, past its 12,110 ms worst case, with no pass over the share, and the run prints `CONTROL store-step-ageless caught`.
The planted store step, `--mutation store-step-unbounded`, is caught at this head too: 13 of 18,918 passes over the share in the 24 windows, the longest 2.718 ms; in 5 windows every row fits its bound, so only the share catches it, in 8 the last SRP record is over 18 ms as well, 18.08 to 19.13 ms, and in 3 it is over with no pass over.

**A persisted change beside a full burst.**
In the first run of the held groups one 8x8 pass was over the share in both held groups, up to 2.135 ms in arm A and 2.085 ms in arm B, 1 ms after the change: AECP's mark of the SET_NAME's two names walked the records from the first, once to name the record and once more in the store, 22,088 CPU cycles in the pass that drained the first bursts.
A record is now marked by its id without the walk (`nvm_rec_id_of`, `nvm_store_changed_id`), so a mark costs the same in any pass, and the held channels but AECP burst at the change, so the marks fall among their first bursts' records.
At this head that pass is 1.711 ms in arm A, its marks within it, and no pass of either held group is over the share in any leg.

**Every pass that carries a step.**
The harness now prints each pass that enters the store's step, those that write nothing to the mailbox too, and gives the store's and its flash port's own CPU time in it.
Over every group a point runs, the longest pass that carries a step is 1.22 ms at 1x1 and 1.29 ms at 8x8, arm A without the drafts (1.23 and 1.27 ms in arm B, at most 1.18 and 1.25 ms with the drafts), and the longest step's own time 0.97 ms (96,579 cycles, a page program's issue), within the 1.0 ms `NVM_STEP_US` gives it.

The steps of one save with no other load, arm A, each kind's longest: the store's and its flash port's own CPU cycles, then the pass that carried it (at 8x8 an idle step's pass also carries the polls' periodic work):

| Step | 1x1/1if, own / pass | 8x8/2if, own / pass |
|---|---:|---:|
| Idle | 3,170 / 46,642 | 2,982 / 102,374 |
| Capture or seal, or idle in the first-dirty window | 35,645 / 46,508 | 34,700 / 66,886 |
| Erase issue | 4,741 / 12,477 | 5,451 / 22,889 |
| Busy poll | 3,775 / 11,506 | 5,013 / 22,451 |
| Blank-check read-back, 128 bytes | 76,495 / 120,202 | 75,869 / 121,069 |
| Page program issue | 95,184 / 102,986 | 95,525 / 126,870 |
| Verify read-back, 128 bytes | 76,048 / 83,867 | 76,917 / 122,059 |

**One build a pass either way.**
The poll now reads whether the interface with the turn builds before it visits either interface (`srp_mbx.c`, `turn_builds`).
Visited first, a withdrawing interface with the turn had spent its withdrawal by the time the other was examined, so interface 1 waited three passes behind interface 0's withdrawal where the rule allows one.
`Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` holds the mirrored case, and `build-turn-read-after-its-visit` plants the old reading.
The round 12 review's link groups at this head, at 8x8: both links dropping under `backlog-adp`'s load (`y-links`) take a longest pass of 1.741 / 1.809 ms (arm A / arm B), under `backlog`'s (`x-links-same`) 1.531 / 1.556 ms; with a save in progress, arm A, `backlog`'s window's longest pass is 1.640 ms and `backlog-adp`'s 1.977 ms (`x-save`, `y-save`).

**A save's verify phase, bounded.**
`grade.save_phase` now refuses a verify window that opens after the save's read-backs have read back every programmed byte, which the harness reads off its journal reads (`FLASHRD`), so a window graded as the verify's is the verify's.

**The rows at this head.**

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.78 / 0.77 | 0.72 / 0.71 | 1.32 / 1.32 | 1.23 / 1.23 |
| ADP record, first | 20 | 0.82 / 0.81 | 0.76 / 0.75 | 1.36 / 1.37 | 1.28 / 1.27 |
| MAAP record, first | 20 | 0.80 / 0.80 | 0.75 / 0.73 | 1.34 / 1.35 | 1.26 / 1.26 |
| AECP record, first | 20 | 0.81 / 0.81 | 0.76 / 0.74 | 1.35 / 1.36 | 1.27 / 1.27 |
| SRP record, first | 18 | 2.87 / 2.85 | 2.69 / 2.65 | 5.45 / 5.43 | 5.05 / 5.06 |
| ACMP record, last | 20 | 5.11 / 5.16 | 4.53 / 4.61 | 7.87 / 8.51 | 7.34 / 7.72 |
| ADP record, last | 20 | 3.58 / 3.67 | 3.28 / 3.29 | 5.85 / 6.07 | 5.44 / 5.56 |
| MAAP record, last | 20 | 3.57 / 3.70 | 3.26 / 3.33 | 5.83 / 6.10 | 5.43 / 5.59 |
| AECP record, last | 20 | 10.04 / 10.37 | 9.07 / 9.67 | 14.83 / 15.93 | 13.49 / 14.33 |
| SRP record, last | 18 | 10.67 / 10.59 | 9.88 / 9.64 | 16.35 / 15.90 | 15.58 / 14.87 |
| an ACMP command behind a full acmp ring | 20 | 3.57 / 3.54 | 3.27 / 3.22 | 6.64 / 6.70 | 6.37 / 6.29 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.83 / 2.80 | 2.54 / 2.52 | 3.62 / 4.63 | 3.31 / 4.27 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.14 / 0.12 | 0.08 / 0.11 | 0.11 / 0.19 | 0.08 / 0.22 |
| an event behind 15 others | 20 | 0.92 / 0.92 | 0.87 / 0.85 | 1.47 / 1.48 | 1.39 / 1.38 |
| AECP record, last, in the owed window | 20 | **62.93** / **62.95** | **62.93** / **62.85** | **65.13** / **65.13** | **65.13** / **65.04** |
| a response with 7 frames owed ahead of it | 20 | **62.07** / **62.10** | **62.06** / **62.01** | **63.78** / **63.77** | **63.76** / **63.69** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows (`save_window.py`), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.43 / 1.44 | 1.42 / 1.32 | 1.96 / 1.91 | 1.84 / 1.69 |
| ADP record, first | 20 | 1.42 / 1.43 | 1.41 / 1.31 | 1.95 / 1.90 | 1.83 / 1.68 |
| MAAP record, first | 20 | 1.46 / 1.47 | 1.44 / 1.35 | 1.99 / 1.93 | 1.86 / 1.71 |
| AECP record, first | 20 | 1.47 / 1.48 | 1.45 / 1.36 | 2.00 / 1.94 | 1.87 / 1.72 |
| SRP record, first | 18 | 2.73 / 2.58 | 2.45 / 2.35 | 4.37 / 4.21 | 4.09 / 3.99 |
| ACMP record, last | 20 | 5.95 / 5.89 | 5.43 / 5.29 | 9.02 / 9.23 | 8.30 / 8.32 |
| ADP record, last | 20 | 4.43 / 4.40 | 4.08 / 3.97 | 6.57 / 6.79 | 6.08 / 6.15 |
| MAAP record, last | 20 | 4.46 / 4.43 | 4.11 / 4.01 | 6.61 / 6.82 | 6.12 / 6.18 |
| AECP record, last | 20 | 10.91 / 10.92 | 9.87 / 10.34 | 15.96 / 16.56 | 14.86 / 15.31 |
| SRP record, last | 18 | 11.46 / 11.22 | 10.51 / 10.32 | 17.23 / 16.91 | 16.48 / 15.56 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.55 / 3.53 | 3.31 / 3.21 | 5.42 / 5.35 | 5.03 / 4.87 |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.76 / 2.73 | 2.28 / 2.26 | 4.78 / 4.80 | 4.43 / 4.44 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.39 / 4.32 | 3.66 / 3.63 | 8.11 / 8.17 | 7.17 / 7.09 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.57 / 5.41 | 5.04 / 4.96 | 10.92 / 11.00 | 9.82 / 9.76 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.82 / 3.01 | 2.27 / 2.54 | 5.30 / 5.33 | 4.84 / 4.85 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.09 / 8.01 | 7.07 / 7.09 | 14.12 / 14.20 | 13.42 / 13.38 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.85 / 2.82 | 2.37 / 2.35 | 4.86 / 4.88 | 4.51 / 4.53 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.55 / 4.47 | 3.82 / 3.85 | 8.27 / 8.50 | 7.32 / 7.28 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.10 / 6.09 | 5.60 / 5.54 | 11.49 / 11.35 | 10.36 / 10.35 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.94 / 2.89 | 2.37 / 2.40 | 5.41 / 5.61 | 4.95 / 4.97 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.67 / 8.69 | 7.65 / 7.68 | 14.60 / 14.81 | 13.88 / 13.89 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1264, 1.11 / 0 of 1251, 1.10 | 0 of 1285, 1.01 / 0 of 1250, 1.01 | 0 of 1311, 1.97 / 0 of 1285, 1.92 | 0 of 1313, 1.89 / 0 of 1287, 1.77 |
| A save's windows | 0 of 10748, 1.22 / 0 of 8643, 1.23 | 0 of 11112, 1.18 / 0 of 8633, 1.17 | 0 of 18324, 1.96 / 0 of 11744, 1.95 | 0 of 17871, 1.86 / 0 of 11737, 1.85 |
| save-held | 0 of 3411, 1.03 / 0 of 3395, 1.03 | 0 of 3405, 1.04 / 0 of 3421, 1.03 | 0 of 8474, 1.69 / 0 of 8489, 1.69 | 0 of 8504, 1.63 / 0 of 8499, 1.63 |
| save-starved | 0 of 44390, 0.97 / 0 of 43629, 0.97 | 0 of 39664, 0.97 / 0 of 43670, 0.97 | 0 of 52488, 1.71 / 0 of 52090, 1.72 | 0 of 52624, 1.66 / 0 of 53926, 1.66 |
| Every group run | 0 of 66819, 1.22 / 0 of 57520, 1.23 | 0 of 56068, 1.18 / 0 of 57576, 1.18 | 0 of 88204, 1.97 / 0 of 74225, 1.95 | 0 of 80929, 1.89 / 0 of 76066, 1.85 |

Every row the CPU decides fits, at both points, in both arms, with the drafts staged or not; the three egress-held rows miss as before, and stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).
The tightest is the 8x8 last SRP record in a save's window, 17.23 ms against 18 in arm A and 16.91 ms in arm B; in the backlog windows it is 16.35 and 15.90 ms.
No pass is over the share in any group of any leg; the longest, 1.97 ms at 8x8, carries no step.

### Aged windows, a change while a save is in flight, and THE RETRY

This subsection is the record of 2026-11-04 (#665) at `5e2651d5`; the one above is the record of `a3f23bba`, the head before it.
The round 14 reviews of [PR #810](https://github.com/kebag-logic/milan-fpga/pull/810) found two statements of that subsection the head does not hold: that no aged step lands among a window's records, and that 12,110 ms is a change's worst case at 8x8/2if.
Measuring windows opened at the step's worst age then put one pass over the share, which THE RETRY (below) keeps out.

**An aged step can land among a window's records.**
THE STEP's age counts the centiseconds dispatched since the step last ran or owed nothing, so only a pass that takes nothing, or the step, ends it (`ctrl_loop.h`).
Every window the harness staged opened after a pass that took nothing, at age zero.
Input that leaves no pass empty before a window, such as a grandmaster change as every pass starts, carries the age into it, and a window that opens with the age at its limit takes an aged step at its next centisecond, among its records, whatever the limit.
It takes one at most: a window's drain, from its opening to the release of its last record, is shorter than two ticks, and after that step the age starts again.
A window opened at age zero takes none at a limit of two, since its third centisecond comes 20 ms or more after it opens, at the worst tick phase just past 20 ms: the longest drain of any window opened from idle is 17.274 ms (8x8, arm A, `backlog-adp@verify-5`), 2.726 ms short. This restates the 3.6 ms of the subsection above, which held for the eight sampled tick phases only.
A step that is running as a window opens ends the age too, so such a window takes no aged step among its records either: the two costs do not meet in one window.

**The aged windows.**
`save_window.aged_window` opens `backlog-adp`'s window in each flash phase with the age at its limit, two, and one short of it, one: after the phase's flash event, a grandmaster change as every pass starts, two of the store's steps, which leave the phase's heavy step next (a blank-check read-back, a page program's issue, a verify read-back), the age's centiseconds in TICK records, then one of eight delays spread evenly across the whole tick, 0.625 to 9.375 ms, and the window opens as the flood stops.
`save_grade.aged_window` proves the age off the log, the centiseconds the TICK records carried since the last pass that carried a step, every pass between them a work pass, and refuses a window at the limit with no aged step taking its phase's heavy step in it, among its records or, where the window drains before its next centisecond, just after them.
Every aged window of every leg was graded with 0 refusals.
At the limit the aged step came among the window's records in 24 of 24 windows at 8x8 in every leg and at 1x1 without the drafts, and in 22 of 24 at 1x1 with the drafts, where the other two drain before their next centisecond and take it just after their last record. One short of it, 14 and 13 of 24 at 8x8 (arm A, arm B) took one among their records and 1 and 3 just after them; at 1x1, 1 of 24 among and 1 and 2 after.

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

A save's windows opened with the step's age at its limit, two (save_window.aged_window), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.13 / 1.12 | 1.05 / 0.92 | 1.31 / 1.30 | 1.24 / 1.57 |
| ADP record, first | 20 | 1.12 / 1.11 | 1.04 / 0.91 | 1.31 / 1.29 | 1.23 / 1.56 |
| MAAP record, first | 20 | 1.16 / 1.15 | 1.08 / 0.94 | 1.34 / 1.33 | 1.27 / 1.24 |
| AECP record, first | 20 | 1.17 / 1.16 | 1.09 / 0.95 | 1.35 / 1.34 | 1.28 / 1.25 |
| SRP record, first | 18 | 2.59 / 2.57 | 2.09 / 2.26 | 4.30 / 4.33 | 4.12 / 3.97 |
| ACMP record, last | 20 | 6.29 / 6.16 | 5.68 / 5.53 | 9.68 / 9.52 | 8.96 / 8.97 |
| ADP record, last | 20 | 4.74 / 4.65 | 4.30 / 4.20 | 7.18 / 7.02 | 6.72 / 6.77 |
| MAAP record, last | 20 | 4.78 / 4.68 | 4.34 / 4.23 | 7.22 / 7.05 | 6.76 / 6.58 |
| AECP record, last | 20 | 11.42 / 11.81 | 10.51 / 10.80 | 16.83 / 17.50 | 15.53 / 16.01 |
| SRP record, last | 18 | 11.97 / 11.79 | 11.11 / 11.10 | 17.74 / 17.90 | 16.41 / 16.58 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.86 / 3.76 | 3.51 / 3.42 | 5.73 / 5.58 | 5.40 / 5.56 |

The same one short of it, one, 24 at each leg that ran them (both arms, without the drafts):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.81 / 1.13 | - / - | 1.68 / 1.67 | - / - |
| ADP record, first | 20 | 0.80 / 1.12 | - / - | 1.67 / 1.66 | - / - |
| MAAP record, first | 20 | 0.84 / 0.84 | - / - | 1.34 / 1.33 | - / - |
| AECP record, first | 20 | 0.85 / 0.85 | - / - | 1.35 / 1.34 | - / - |
| SRP record, first | 18 | 2.91 / 2.29 | - / - | 4.30 / 4.34 | - / - |
| ACMP record, last | 20 | 6.07 / 6.03 | - / - | 8.90 / 8.67 | - / - |
| ADP record, last | 20 | 4.50 / 4.50 | - / - | 6.41 / 6.20 | - / - |
| MAAP record, last | 20 | 4.53 / 4.54 | - / - | 6.34 / 6.24 | - / - |
| AECP record, last | 20 | 10.98 / 11.38 | - / - | 16.79 / 17.47 | - / - |
| SRP record, last | 18 | 12.22 / 12.34 | - / - | 17.65 / 17.81 | - / - |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.28 / 3.61 | - / - | 5.07 / 5.03 | - / - |

Aged windows: the least margin and its row, the aged steps among their records (count, the longest aged pass, CPU cycles (ms), and the kinds), per age, arm A / arm B:

| Age | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 2 | 6.025 (11.975, blank-aged2-0); 24 aged in 24, longest 90,295 (0.903), issue/read-back / 6.212 (11.788, blank-aged2-0); 24 aged in 24, longest 83,823 (0.838), issue/read-back | 6.886 (11.114, blank-aged2-0); 22 aged in 24, longest 89,723 (0.897), issue/read-back / 6.900 (11.100, blank-aged2-0); 22 aged in 24, longest 91,818 (0.918), issue/read-back | 0.256 (17.744, program-aged2-1); 24 aged in 24, longest 92,022 (0.920), issue/read-back / 0.101 (17.899, verify-aged2-2); 24 aged in 24, longest 95,825 (0.958), issue/read-back | 1.591 (16.409, program-aged2-5); 24 aged in 24, longest 91,477 (0.915), issue/read-back / 1.419 (16.581, verify-aged2-4); 24 aged in 24, longest 92,887 (0.929), issue/read-back |
| 1 | 5.776 (12.224, blank-aged1-7); 1 aged in 24, longest 84,970 (0.850), read-back / 5.660 (12.340, blank-aged1-7); 1 aged in 24, longest 77,764 (0.778), read-back | - / - | 0.351 (17.649, verify-aged1-4); 14 aged in 24, longest 91,638 (0.916), issue/read-back / 0.187 (17.813, verify-aged1-6); 13 aged in 24, longest 84,324 (0.843), issue/read-back | - / - |

The least margin with an aged step at its worst placement measured is 0.101 ms, the 8x8 last SRP record at 17.899 ms in `backlog-adp@verify-aged2-2`, arm B; arm A's is 0.256 ms (`program-aged2-1`, 17.744 ms), and with the drafts 1.419 ms. The reviews' windows of round 14 ran on `a3f23bba`'s image (17.840 and 17.775 ms there); the staged windows are this head's.
The program phase's aged step is a page program's issue in every program window, and the blank check's and the verify's a 128-byte read-back, in every leg.

**Why two.**
The limit decides how often, not whether, a window takes an aged step: at any limit a window opened at the limit takes one at its next centisecond, and no window takes two.
At one, a window opened from idle would take one at its second centisecond too; at two it takes none, and every row fits with the one a window opened at the limit takes, at its worst placement measured.
Three would add a tick to every step of a save under such input, 4 ticks a step and 15,810 ms alone at 8x8/2if.

**The planted heavier aged step.**
`--mutation store-step-aged-heavier` holds the CPU 0.8 ms longer in the pass given whole to an aged step, by the step's own clock, about one read-back step more.
On the verify's eight aged windows at the limit, 8x8, arm A, every window's last SRP record is over 18 ms, 18.386 to 18.743 ms, with no pass over the share, and the run prints `CONTROL store-step-aged-heavier caught`.

**A change while a save is in flight.**
A change marked once the running capture has passed its record is not that capture's (`nvm_mark`): its record is dirty again and opens a first-dirty window of its own, and only an idle step starts a capture, so it waits for the rest of the save in flight before its own save starts.
The worst is a change marked just after the capture took the first record it names, two steps into that save: it waits for the save's other S<sub>f</sub> - 2 steps, or its own first-dirty window where that is longer, then its own S steps, so

> T ≤ max(1,000 ms, (S<sub>f</sub> - 2) × 3 × 10 ms) + S × 3 × 10 ms + 10 ms

after it. For a SET_NAME of the entity beside another's save in flight, S<sub>f</sub> = S = 370 at 8x8/2if and T ≤ 22,150 ms; 102 at 1x1 and T ≤ 6,070 ms; each further record of either save adds 30 ms (`nvm_store.h`, `save_window.bound_ms`).
`save-second` stages it: under a grandmaster change as every pass starts, a SET_NAME just after a step, then 1,035 ms later and one step on, once the capture has started and taken the entity's first name, a SET_NAME of the entity to another value.
`save_grade.save_time` times the second from its mark to durable in the save after the first, and refuses it unless it came after the first's first-dirty window and before the first save's erase:

Ms from the second change to durable against its stated worst case, arm A / arm B (steps; longest gap between flash steps, ms):

| Group | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| save-second | 6029.8 of 6,070 (102; 30.979) / 6029.8 of 6,070 (102; 30.94) | 6029.8 of 6,070 (102; 30.911) / 6029.9 of 6,070 (102; 30.922) | 22110.0 of 22,150 (370; 30.942) / - | - / - |

The review's 1x1 probe, its own plant on a clean clone of `a3f23bba` (a second SET_NAME 1,500 ms after the first under the same flood), gave, in round 15, the review's own analysis byte for byte: the second SET_NAME durable 5,608.954 ms after it, over the 4,070 ms then stated and within the 6,070 ms above. At this head `save-second` is durable within its worst case at both points, in both arms, with and without the drafts.

**On the product's flash part.**
The harness's flash model has no busy time.
The part of [section 9.4 of the fast-connect design](SAVED_STATE_FASTCONNECT.md#94-the-deadlines), the N25Q128 at its datasheet maximum, erases a 64 KiB sector in up to 3 s (tSE) and programs a page in up to 5 ms (tPP).
A wait's polls come one a step: the poll that finds the erase done is at most one step period after it ends, so the erase adds at most tSE to a save, and a page's wait at most tPP, since its first poll comes at the next tick or later and a second one more than a tick after its issue.
A save so adds at most tSE + pages × tPP: 3,260 ms at 8x8/2if (52 pages) and 3,070 ms at 1x1 (14).
A SET_NAME of the entity is then durable at most 15,370 ms after it alone and 28,670 ms beside another's save in flight at 8x8/2if, 7,140 and 12,210 ms at 1x1.

The owner's 0.5 s ([#823](https://github.com/kebag-logic/milan-fpga/issues/823)) applies to the firmware writer of the append-only design through this same step; this image states its own worst case and does not meet 0.5 s.

**A change-notice retry kept out of a burst's pass (THE RETRY).**
At `bc4685ec`, the head THE RETRY starts from, one pass was over the share: at 8x8/2if, arm A, `backlog-adp@blank-aged1-7`'s second pass, 202,116 CPU cycles, 2.021 ms.
It was the composed burst's heaviest pass, which takes the records and dispatches the centisecond posted 0.625 ms after the window opened, and it held 4,679 more cycles of AECP than the same pass of the window opened from idle: arm A's size fixture never answers the face block, so AECP's change notices after the grandmaster changes are retried with the backoff of `aecp.h` (1, 2, 4, then every 8 ms), and one came due in that pass.
The retry is the product's: a held or resetting datapath, or a slow answer, takes the same path, so the share holds it ([the ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6620376502)).
A burst's pass does not need a centisecond to be that heavy: at that head `backlog-adp@verify-aged1-2`'s second pass, 195,683 cycles, held a retry and dispatched none.
So a retry is now taken by no pass that takes an input or dispatches a centisecond (`ctrl_loop.h`, THE RETRY): AECP's poll and its timer's sink hold a due retry, arm no timer for it and report it owed (`aecp.retry_hold`), and only the loop calls its round (`aecp_retry`), in a pass that took no input and dispatched no centisecond, after its polls and before THE STEP, whose deadline counts the round's time, or after the step in the pass given whole to an aged step, the only pass free of input under input that leaves none empty.
The round tries every due notice, one observation-port call each, and builds the first its port answers.
`Loop.L16TheRetryOnlyInAPassThatTakesNothing`, `Mailbox.RetryWaitsForAPassThatTakesNothing` and `Core.HeldRetryWaitsForTheRoundAndTheRoundForAnOwedResponse` hold the rule, with 25 planted defects, 11 in the loop and 14 in AECP, `retry-in-the-bursts-pass` (the round released in any pass) among them.
Its bound, stated beside `CTRL_LOOP_STEP_AGE`: with nothing posted after it, a due retry waits through the passes that take the input posted before it and dispatch the centiseconds then owed, and the next pass takes it; under input that leaves no pass empty it waits for the next aged step's pass, at most three ticks.
A pass that takes it holds its polls' owed output, one round, and THE STEP only before its deadline; an aged step's pass holds the step and one round.
At this head no pass of any leg is over the share. `backlog-adp@blank-aged1-7`'s heaviest pass is 197,193 cycles (1.972 ms), with AECP's command cycles at the level of a pass that holds no round. The aged step's passes that hold a round, which re-arms AECP's timer and so writes to the mailbox, take at most 92,022 cycles (0.920 ms) at 8x8; the round, the loop's call and the re-arm are at most 9,770 cycles of that.

**The scan in the hot list, and the layout.**
The round shares AECP's event scan with the poll. When `ctrl_split_hot.txt` was traced, the scan was inlined in `aecp_poll`; with a second caller it is now a function of its own (`scan`). Linked after the hot region, it cost every pass that scans; the hot list now places it where its code ran, between `mbx_now_ms` and `arm`.
Even so, the code that grew ahead of SRP's drain moves its functions against the fetch L1. An 8x8 SRP drain pass now refills 216 to 222 fetch lines where it refilled 199 to 210 at `a3f23bba`'s image, about 2,000 cycles. It also runs 41 more instructions, `arm`'s held check for each live event. It now takes 69,300 to 71,100 cycles against 66,300 to 68,100.
Over SRP's drain that is about 0.3 ms. In arm B, which retries nothing, the tightest aged window's last SRP record moved from 17.563 to 17.899 ms. In arm A the retries no longer in the burst take about as much back: `verify-aged2-2` went from 17.852 to 17.530 ms.
The burst's heaviest pass holds no retry and is 199,112 cycles at 8x8 (`backlog-adp`, 1.991 ms), 888 cycles short of the share; it was 196,985. The hot list is not traced again here.
A notice whose port answers is built at its next retry, within 8 ms, and where no input waits in the pass after the one that takes the retry's timer, inside its 20 ms bound; behind a backlog it waits until the backlog is taken, and under input that leaves no pass empty until the next aged step, where it can come later than 20 ms after the port answers (`aecp.h`).

**The rows at this head.**

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.79 / 0.79 | 0.71 / 0.70 | 1.32 / 1.32 | 1.25 / 1.23 |
| ADP record, first | 20 | 0.83 / 0.83 | 0.75 / 0.75 | 1.36 / 1.36 | 1.29 / 1.28 |
| MAAP record, first | 20 | 0.81 / 0.82 | 0.73 / 0.73 | 1.34 / 1.34 | 1.27 / 1.26 |
| AECP record, first | 20 | 0.82 / 0.83 | 0.74 / 0.74 | 1.35 / 1.35 | 1.28 / 1.27 |
| SRP record, first | 18 | 2.87 / 2.88 | 2.64 / 2.63 | 5.42 / 5.43 | 5.12 / 5.08 |
| ACMP record, last | 20 | 5.32 / 5.22 | 4.51 / 4.62 | 7.95 / 8.54 | 7.94 / 7.55 |
| ADP record, last | 20 | 3.77 / 3.71 | 3.26 / 3.29 | 5.90 / 6.07 | 5.71 / 5.61 |
| MAAP record, last | 20 | 3.81 / 3.75 | 3.25 / 3.33 | 5.89 / 6.11 | 5.74 / 5.60 |
| AECP record, last | 20 | 10.32 / 10.64 | 9.25 / 9.65 | 14.88 / 15.92 | 14.20 / 14.64 |
| SRP record, last | 18 | 10.64 / 10.61 | 10.11 / 9.94 | 16.81 / 16.42 | 15.14 / 15.09 |
| an ACMP command behind a full acmp ring | 20 | 3.56 / 3.57 | 3.22 / 3.20 | 6.68 / 6.68 | 6.38 / 6.41 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.88 / 2.84 | 2.55 / 2.51 | 3.55 / 4.64 | 4.39 / 3.99 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.10 / 0.14 | 0.10 / 0.11 | 0.20 / 0.23 | 0.18 / 0.11 |
| an event behind 15 others | 20 | 0.93 / 0.94 | 0.85 / 0.85 | 1.47 / 1.47 | 1.40 / 1.39 |
| AECP record, last, in the owed window | 20 | **62.98** / **62.97** | **62.95** / **62.94** | **65.26** / **65.24** | **65.09** / **65.24** |
| a response with 7 frames owed ahead of it | 20 | **62.11** / **62.32** | **62.08** / **62.06** | **63.87** / **63.84** | **63.72** / **63.87** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows opened from idle (save_window.py), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.50 / 1.51 | 1.39 / 1.41 | 1.87 / 1.90 | 1.66 / 1.68 |
| ADP record, first | 20 | 1.49 / 1.50 | 1.38 / 1.40 | 1.86 / 1.89 | 1.66 / 1.68 |
| MAAP record, first | 20 | 1.52 / 1.54 | 1.41 / 1.44 | 1.89 / 1.92 | 1.69 / 1.71 |
| AECP record, first | 20 | 1.53 / 1.55 | 1.42 / 1.45 | 1.90 / 1.93 | 1.70 / 1.72 |
| SRP record, first | 18 | 2.91 / 2.66 | 2.43 / 2.44 | 4.42 / 4.37 | 4.39 / 3.96 |
| ACMP record, last | 20 | 6.05 / 6.01 | 5.46 / 5.41 | 8.94 / 9.26 | 8.16 / 8.40 |
| ADP record, last | 20 | 4.50 / 4.50 | 4.09 / 4.08 | 6.44 / 6.78 | 5.94 / 6.19 |
| MAAP record, last | 20 | 4.54 / 4.54 | 4.12 / 4.12 | 6.48 / 6.82 | 5.98 / 6.23 |
| AECP record, last | 20 | 10.89 / 11.43 | 10.30 / 10.46 | 16.24 / 16.87 | 14.70 / 15.41 |
| SRP record, last | 18 | 11.53 / 11.40 | 10.78 / 10.76 | 17.24 / 17.22 | 15.79 / 15.75 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.62 / 3.62 | 3.29 / 3.30 | 5.34 / 5.35 | 4.77 / 4.89 |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.77 / 2.79 | 2.28 / 2.27 | 4.83 / 4.80 | 4.60 / 4.48 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.38 / 4.42 | 3.68 / 3.65 | 8.23 / 7.84 | 7.19 / 7.24 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.68 / 5.80 | 5.18 / 5.21 | 11.37 / 11.34 | 10.02 / 10.06 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.83 / 2.85 | 2.65 / 2.60 | 5.37 / 5.33 | 4.92 / 4.90 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.21 / 8.53 | 7.51 / 7.48 | 14.53 / 14.83 | 13.62 / 13.65 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.85 / 2.87 | 2.38 / 2.35 | 4.90 / 5.16 | 4.58 / 4.58 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.53 / 4.57 | 3.87 / 3.82 | 8.55 / 8.51 | 7.40 / 7.43 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.20 / 6.30 | 5.81 / 5.85 | 11.66 / 11.66 | 10.63 / 10.70 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.94 / 2.96 | 2.86 / 2.77 | 5.63 / 5.60 | 5.04 / 5.04 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.73 / 9.09 | 8.10 / 8.13 | 15.11 / 15.08 | 14.13 / 14.19 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1289, 1.12 / 0 of 1249, 1.11 | 0 of 1292, 1.02 / 0 of 1252, 1.00 | 0 of 1328, 1.99 / 0 of 1288, 1.93 | 0 of 1334, 1.82 / 0 of 1285, 1.86 |
| A save's windows from idle | 0 of 12463, 1.23 / 0 of 8645, 1.24 | 0 of 12459, 1.24 / 0 of 8635, 1.21 | 0 of 21379, 1.98 / 0 of 11744, 1.95 | 0 of 22538, 1.88 / 0 of 11745, 1.87 |
| Aged windows at the limit | 0 of 25308, 1.23 / 0 of 21822, 1.23 | 0 of 24743, 1.22 / 0 of 22573, 1.20 | 0 of 28802, 1.97 / 0 of 18246, 1.95 | 0 of 29937, 1.88 / 0 of 18208, 1.86 |
| Aged windows one short of it | 0 of 22915, 1.40 / 0 of 19420, 1.47 | 0 of 0, 0.00 / 0 of 0, 0.00 | 0 of 27582, 1.97 / 0 of 17031, 1.96 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| save-held | 0 of 3392, 1.04 / 0 of 3354, 1.05 | 0 of 3405, 1.04 / 0 of 3403, 1.04 | 0 of 8417, 1.70 / 0 of 8476, 1.69 | 0 of 8490, 1.63 / 0 of 8486, 1.61 |
| save-starved | 0 of 42175, 0.97 / 0 of 40711, 0.98 | 0 of 40800, 0.97 / 0 of 43249, 0.97 | 0 of 52543, 1.75 / 0 of 51902, 1.72 | 0 of 53866, 1.66 / 0 of 52681, 1.65 |
| save-second | 0 of 80579, 0.96 / 0 of 77687, 0.97 | 0 of 76999, 0.96 / 0 of 81995, 0.96 | 0 of 120075, 1.37 / 0 of 0, 0.00 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| Every group run | 0 of 197118, 1.40 / 0 of 173490, 1.47 | 0 of 160300, 1.24 / 0 of 161709, 1.21 | 0 of 269272, 1.99 / 0 of 109304, 1.96 | 0 of 116785, 1.88 / 0 of 93022, 1.87 |

Saves, ms from the change to durable against the stated worst case, arm A / arm B (steps; longest gap between flash steps, ms):

| Group | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| save | 2018.3 of 4,070 (102; 10.844) / 2018.2 of 4,070 (102; 10.912) | 2018.3 of 4,070 (102; 10.888) / 2018.2 of 4,070 (102; 10.941) | 4697.3 of 12,110 (370; 12.542) / 4697.4 of 12,110 (370; 12.453) | 4698.4 of 12,110 (370; 12.612) / 4697.4 of 12,110 (370; 12.632) |
| save-held | 2018.1 of 4,070 (102; 14.528) / 2018.0 of 4,070 (102; 14.651) | 2018.1 of 4,070 (102; 14.021) / 2018.0 of 4,070 (102; 13.958) | 4696.9 of 12,110 (370; 20.085) / 4696.9 of 12,110 (370; 19.857) | 4731.3 of 12,110 (370; 17.748) / 4696.9 of 12,110 (370; 18.752) |
| save-starved | 4048.1 of 4,070 (102; 31.096) / 4048.0 of 4,070 (102; 30.993) | 4047.9 of 4,070 (102; 31.122) / 4048.0 of 4,070 (102; 31.107) | 12087.1 of 12,110 (370; 31.424) / 12087.0 of 12,110 (370; 31.314) | 12088.1 of 12,110 (370; 31.366) / 12086.8 of 12,110 (370; 31.242) |
| save-second | 6029.8 of 6,070 (102; 30.979) / 6029.8 of 6,070 (102; 30.94) | 6029.8 of 6,070 (102; 30.911) / 6029.9 of 6,070 (102; 30.922) | 22110.0 of 22,150 (370; 30.942) / - | - / - |

Passes that carry the store's step, every group: count, the longest pass and the longest step, CPU cycles (ms), arm A / arm B:

| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---:|---:|---:|---:|
| 30477: 123,345 (1.233); 96,082 (0.961) / 26876: 123,539 (1.235); 96,486 (0.965) | 19050: 123,503 (1.235); 95,835 (0.958) / 19050: 121,294 (1.213); 96,041 (0.960) | 40537: 131,058 (1.311); 96,423 (0.964) / 35701: 127,174 (1.272); 96,571 (0.966) | 25115: 126,044 (1.260); 96,278 (0.963) / 25120: 125,953 (1.260); 96,126 (0.961) |

### THE RETRY's age limit, THE TRANSMIT, THE TICK's cap and every pass class

This subsection is the record of 2026-11-05 (#665) at the code head `65a56d02`. Its legs ran on clean clones of `12e5ec56`, whose firmware is `65a56d02`'s; the commits after it change tests, plants, the harness's new control, comments, one named constant and the compile-time check that reads it, and documents, and the images they build are the legs' byte for byte. The subsection above is the record of `5e2651d5`.
Two of its statements no longer hold at this head. A retried notice is now inside its 20 ms under any input, by construction. And the least margin it states, 0.101 ms, was taken before a staging that composes every channel's burst under input that leaves no pass empty: that staging put the 8x8 last SRP record past its 18 ms and one pass over the share, from a cause that predates THE RETRY ([the ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6634982529)).

**THE RETRY's age limit.**
Under input that leaves no pass empty a held change-notice retry waited for the next aged step's pass, up to three ticks, on top of the 8 ms spacing, which put a retried notice past its 20 ms ([the ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6630265194)).
A held retry `CTRL_LOOP_RETRY_AGE_MS` (4 ms) past its time, on AECP's own millisecond clock from the earliest held retry, now takes the next pass whole, before any input (`aecp_retry_aged`, `ctrl_loop.h`).
So a retry's round is committed within `CTRL_LOOP_RETRY_MS`, 4 + 3 x 2 = 10 ms, of its time, and a retried notice within 8 + 10 = 18 ms of its port's answer; `aecp_mbx.c` holds the sum to `AECP_NOTICE_MS` at compile time.
`notice_window.py`'s groups time it from the port's answer, in the labelled `answering-later` arm, under `save-starved`'s input (every receive channel at its refill rate with its bursts, a grandmaster change as every pass starts) with a save in flight, at eight phases of the spacing, and each channel's longest record under that load is a row too:

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz; over the eight groups, the least to the most, ms, bold over the bound:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts | 8x8/2if, struct-ends layout |
|---|---:|---:|---:|---:|---:|---:|
| a retried notice, from its port's answer to its last recipient's commit | 20 | 12.30 to 12.41 | 12.32 to 13.20 | 12.54 to 12.99 | 12.47 to 13.51 | 12.77 to 12.84 |
| ACMP record, the longest held | 20 | 5.35 to 6.14 | 4.85 to 5.16 | 9.14 to 9.84 | 8.49 to 9.04 | 9.09 to 9.93 |
| ADP record, the longest held | 20 | 2.26 to 4.00 | 1.57 to 3.88 | 5.61 to 7.52 | 5.38 to 6.95 | 5.94 to 7.63 |
| MAAP record, the longest held | 20 | 2.60 to 3.40 | 2.38 to 3.28 | 5.02 to 5.72 | 4.79 to 5.17 | 4.93 to 5.78 |
| AECP record, the longest held | 20 | 10.03 to 10.81 | 9.39 to 9.77 | 15.76 to 16.43 | 14.77 to 15.53 | 15.75 to 16.45 |
| SRP record, the longest held | 18 | 10.74 to 10.88 | 10.23 to 10.42 | 16.48 to 17.11 | 15.98 to 16.46 | 16.58 to 17.10 |

With the age removed (`--mutation retry-ageless`, at this head's firmware) every group's notice is late, 30.29 to 30.32 ms at 1x1/1if and 30.66 to 30.88 ms at 8x8/2if, and the run prints `CONTROL retry-ageless caught` at both points.

**The composed burst under input that leaves no pass empty.**
The notice groups are the first to stage it: at the load's first instant every channel's bucket burst comes at once while a grandmaster change starts every pass, with a bound sink, 16 registrations an interface and a save in flight.
At `d0eef1cb`, at 8x8/2if, every group's last record of SRP's first burst was 19.047 to 19.666 ms after its commit, 18.975 to 19.421 ms on `65251a2f`'s firmware, and one pass was 201,540 cycles.
In `notice-retried-4` the 32 SRP records commit at +0.80 to +0.83 ms and the last is taken by the sixteenth pass that takes SRP's records, two a pass (D4(b)): 0.72 ms of the pass running, one pass of 1.23 ms that took no SRP record because a TICK record posted during it left the event level set at SRP's readiness check, the sixteen passes, 17.45 ms, and two aged retry rounds, 0.26 ms.
Five of the sixteen carry an MRPDU build a centisecond's join timers start, about 2.4 to 2.9 ms in all, and the last AECP record (19.657 ms against 20) waits behind the same passes.
So the lever that moves SRP, AECP and the heaviest pass together is to take the build out of every pass that takes a record.

**THE TRANSMIT.**
SRP's MRPDU build is now deferrable work of its own pass class (`ctrl_loop.h`, THE TRANSMIT; `srp_mbx.c`, `transmit`).
The loop marks a pass that took no record, at most `CTRL_LOOP_TX_EVENTS` (one) events and no centisecond before its polls (`tx_pass`), and calls the build after them, before THE RETRY and THE STEP, whose deadline counts its time.
SRP's poll builds nothing and declares nothing; the build's call makes the interface's declarations and then builds one MRPDU, the participants in turn, in the order the poll ran them before.
A centisecond, a received record, a walk that changes a binding's declaration, an unbinding that withdraws one, a Domain change or a new participant holds a build, and the poll reports a held build owed.
Once SRP's tick has counted more than `CTRL_LOOP_TX_AGE` (two) centiseconds while it is held, the next pass after one not given whole is the build's alone, before any input, with THE RETRY's round after it; no two passes given whole run back to back.
Its bound, `CTRL_LOOP_TX_MS`, from the hold to the end of the pass that takes it, under any input: three ticks, then seven passes of the share, 30 + 7 x 2 = 44 ms; every participant's owed MRPDU, one a call, within 2 x `MBX_N_IF` x 44 = 176 ms at two interfaces, inside the 200 ms JoinTime (IEEE 802.1Q Table 10-7).
A frame a build left owed stays the poll's (A3), one a pass, and a pass whose poll sent it builds no other.
Three of the head's behaviours are kept by where the work now stands, each found against the head's own trace on the way: a Domain adopted in a record's pass would have left its VID unlicensed to the next poll, so the declarations run in the build's call, as they ran beside the build before (Milan 4.3.2); a reclaim before the declarations gave a retained receive's room to an adoption the head refused, so the reclaim follows them; and in a pass whose build does not follow, the poll reclaims, so a record the next pass takes finds the room.
`LoopBring.L18TransmitBindingRefusals`, `Loop.L19TheTransmitOnlyInAPassThatTakesNoRecord`, `Loop.L20AnAgedTransmitIsAPassOfItsOwn`, `Srp.TransmitWaitsForAPassThatTakesNoRecord`, `Srp.AHeldBuildTakesAPassOfItsOwnPastItsAge` and `Srp.AnOwedFrameComesBeforeTheBuild` hold the rule, with 43 planted defects, 24 in the loop and 19 in SRP's adapter, each failing its named test on its words.

**SRP's bound, and what THE TRANSMIT gives its records.**
`CTRL_LOOP_SRP_MS` states SRP's bound beside `CTRL_LOOP_STEP_AGE`, `CTRL_LOOP_RETRY_MS` and `CTRL_LOOP_TX_MS`: min(T_svc = 20 ms, its ceiling), 18 ms, THE SHARE's nine passes ([FR_NFR.md 3.4.1](../reference/FR_NFR.md#341-control-service-budget-and-normative-timing)).
By pass class, no pass that takes a record carries a build.
Beside the passes a record of SRP's admitted burst waits stand at most one pass given whole to an aged build, since two stand `CTRL_LOOP_TX_AGE` ticks apart, more than 18 ms (`srp_mbx.c` holds the two to each other at compile time), at most one given whole to an aged step, three ticks apart, and the aged retries' passes, at least a millisecond and `CTRL_LOOP_RETRY_AGE_MS` apart.
That count does not reach the composed burst's own passes: its 32 SRP records at 8x8/2if, two a pass, are taken in sixteen, more than the nine THE SHARE counts, so that row fits by the measured cost of those sixteen passes, not by the constants.
At this head it fits: in the notice groups the last record of SRP's first burst is 16.48 to 17.11 ms after its commit at 8x8/2if, 15.98 to 16.46 ms with both drafts, and 10.23 to 10.88 ms at 1x1/1if; over every window staged, the last SRP record is at most 17.765 ms, a save's verify window opened one short of the age limit, arm A (the tables below).
A pass among those a record waits can still carry a build where it took no record at all: an event posted during it holds SRP's records back (`srp_mbx.c`, `rx_order_ready`), and no other channel's record waited. A frame SRP owes is sent in place of a build, and owed centiseconds are dispatched by a pass that builds none, so that is the one case, and the measured rows include it.
The same holds of the four backlog windows, whose SRP ring is full: the row has fitted by measurement since the backlog windows were first staged, and this head does not change how it is bounded.

**THE TICK's cap.**
With THE TRANSMIT alone the notice groups' last SRP record fell to 16.790 ms and the last AECP record to 16.266 ms, but one pass was 195,756 cycles, 4,244 under the share: the pass that dispatches the 10 ms centisecond beside the burst's first records, about 43,000 cycles of the centisecond's consumers (lwSRP's timers and the walks after them) beside two records a channel (a labelled pre-check on the code head's working tree before this cap, not this head's measurement).
So a pass that dispatches a centisecond takes one record of a channel, `CTRL_LOOP_RX_PER_TICK_PASS`, and the rest wait for the next pass; THE BOUND's passes grow by one for each such pass among them.
`Loop.L21APassThatDispatchesACentisecondTakesOneRecordOfAChannel` holds it, with three plants; `rx-pass-unbounded` now plants the receive loop's bound and the cap together, since either alone still stops a pass at two records.

**The first registration.**
The heaviest pass that takes a record at this head is 190,420 cycles, the third pass of `backlog-adp@verify-0`'s window (8x8/2if, arm A), with eight events and the burst's records.
In the notice groups the heaviest is the burst's first pass that takes SRP's first two records, which register a Listener new to the participant: 188,980 cycles (`notice-retried-3`).
Traced by committed PC (`BUDGET_TRACE_AFTER`, on the code head's working tree, whose pass is the same 188,980 cycles), it spends about 40,000 cycles more than a later burst pass with the same records: lwSRP's attribute searches (`memcmp` 12,663 against 992, `find_attr`, `mrp_attr_registered_ports`), the adapter's walk (`mrp_attr_visit`, `registrations`, `snapshot`) and a block from the pool.
`memcmp` is already word-wise (`ctrl_mem.c`); the count is lwSRP's linear searches, which no pass class moves.

**Every pass class.**
THE SHARE's reason is that no pass may run past 2.0 ms; the ruling asks each kind of pass to sit at least 6,490 cycles under it, the swing the data layout alone made on the same records ([the ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6634982529)).
A pass's class is read off its `PASS` line: what it wrote (an event's or a channel's tail) says what it took, and its modules say which callbacks ran.
The heaviest measured pass of each class, CPU cycles and its margin under the 200,000-cycle share, over every group of every leg at this head, both arms pooled (CPU 100 MHz on sys, bus 100 MHz):

| Class | What it holds | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts | 8x8/2if, struct-ends layout |
|---|---|---:|---:|---:|---:|---:|
| records | takes a record: its events, its records, two a channel (one in a pass that dispatches a centisecond), and the polls | 116,176 (83,824 under; backlog-adp@verify-5) | 105,756 (94,244 under; backlog-adp@verify-5) | 190,420 (9,580 under; backlog-adp@verify-0) | 182,362 (17,638 under; backlog-adp@blank-aged2-2) | 189,156 (10,844 under; notice-retried-3) |
| events | takes events and no record: the polls, and at most one event beside THE TRANSMIT's build | 52,247 (147,753 under; notice-retried-0) | 50,444 (149,556 under; notice-retried-0) | 140,363 (59,637 under; save-starved) | 134,776 (65,224 under; save-starved) | 137,715 (62,285 under; save-starved) |
| none | takes nothing and writes to the mailbox: the polls' owed output, THE TRANSMIT's build, THE RETRY's round, THE STEP before its deadline | 128,083 (71,917 under; backlog-adp@blank-aged1-7) | 115,948 (84,052 under; notice-retried-7) | 171,351 (28,649 under; srp) | 131,973 (68,027 under; save-held) | 135,904 (64,096 under; save-held) |
| whole-step | given whole to an aged step: the step and THE RETRY's round | 97,378 (102,622 under; save-starved) | 97,160 (102,840 under; save-starved) | 97,347 (102,653 under; save-starved) | 97,806 (102,194 under; save-starved) | 98,174 (101,826 under; save-starved) |
| whole | given whole to an aged retry: one round | 9,610 (190,390 under; notice-retried-0) | 9,378 (190,622 under; notice-retried-3) | 12,571 (187,429 under; notice-retried-0) | 12,419 (187,581 under; notice-retried-7) | 13,186 (186,814 under; notice-retried-0) |
| whole-transmit | given whole to an aged build: one build and one round | - | - | - | - | - |
| idle | writes nothing to the mailbox: the polls with nothing owed, or THE STEP before its deadline (a run's longest) | 106,887 (93,113 under; acmp-notk) | 106,401 (93,599 under; backlog-adp@verify-0) | 118,647 (81,353 under; acmp-notk) | 117,495 (82,505 under; save-held) | 117,708 (82,292 under; backlog-adp@verify-0) |
| build | of the above, one that carries THE TRANSMIT's build or the poll's owed SRP frame | 128,083 (71,917 under; backlog-adp@blank-aged1-7) | 115,948 (84,052 under; notice-retried-7) | 171,351 (28,649 under; srp) | 134,776 (65,224 under; save-starved) | 137,715 (62,285 under; save-starved) |
| step | of the above, one that carries the store's step | 128,083 (71,917 under; backlog-adp@blank-aged1-7) | 115,948 (84,052 under; notice-retried-7) | 130,212 (69,788 under; acmp-notk) | 127,428 (72,572 under; save-held) | 127,657 (72,343 under; save-held) |

Every class sits at least 9,580 cycles under the share at both points, at the head's layout and at the struct-ends layout: the closest is a pass that takes a record at 8x8/2if, 190,420 cycles, 3,090 cycles more than the ruling's 6,490 under.
No staged group holds a pass given whole to an aged build, since a pass that takes no record comes before a build ages in every staging; `Loop.L20AnAgedTransmitIsAPassOfItsOwn` and `Srp.AHeldBuildTakesAPassOfItsOwnPastItsAge` make one.
It holds one build and one round and no poll, so at most the heaviest pass that carries a build and the heaviest round: 171,351 + 12,571 = 183,922 cycles at 8x8/2if and 128,083 + 9,610 = 137,693 at 1x1/1if.
The struct-ends layout ran the 8x8 notice groups and arm A's backlog windows, a save's windows from idle, its aged windows at the limit and the three saves; the classes whose heaviest falls in groups outside them, a pass that takes nothing in `srp` (171,351 cycles), and one that writes nothing and one that carries the store's step in `acmp-notk` (118,647 and 130,212), sit 28,649 cycles or more under the share.
The struct-ends layout moves THE RETRY's and THE TRANSMIT's fields to the ends of their structs, so the image's other data keep the offsets they had before them (a labelled scratch layout, not on this branch).

**The controls.**

- `--mutation transmit-beside-records` gives THE TRANSMIT's pass to every pass, so the build follows the polls of a pass that takes the composed burst's records, as before THE TRANSMIT. At 8x8/2if, in the eight notice groups, every group's longest held SRP record is 19.59 to 20.11 ms, over its 18 ms, the longest AECP record 18.40 to 19.17 ms, with no pass over the share, and the run prints `CONTROL transmit-beside-records caught`.
- `--mutation retry-ageless`, above: `CONTROL retry-ageless caught` at both points.
- `--mutation store-step-aged-heavier` holds the CPU 0.8 ms longer in the pass given whole to an aged step. On the verify's eight aged windows at the limit, 8x8, arm A, every window's last SRP record is over 18 ms, 18.137 to 18.568 ms, with no pass over the share, and the run prints `CONTROL store-step-aged-heavier caught`.

**The rows at this head.**

CPU 100 MHz on sys (the product split CPU clock), bus 100 MHz. Cells are arm A / arm B, ms, bold over the bound.

The four backlog windows:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.82 / 0.79 | 0.73 / 0.73 | 1.34 / 1.35 | 1.25 / 1.32 |
| ADP record, first | 20 | 0.86 / 0.84 | 0.77 / 0.78 | 1.39 / 1.39 | 1.29 / 1.36 |
| MAAP record, first | 20 | 0.84 / 0.82 | 0.75 / 0.76 | 1.37 / 1.37 | 1.27 / 1.34 |
| AECP record, first | 20 | 0.86 / 0.83 | 0.77 / 0.77 | 1.38 / 1.38 | 1.28 / 1.36 |
| SRP record, first | 18 | 3.05 / 2.96 | 2.76 / 2.78 | 5.49 / 5.42 | 5.10 / 5.36 |
| ACMP record, last | 20 | 5.16 / 5.19 | 4.61 / 4.68 | 8.47 / 8.90 | 8.19 / 8.06 |
| ADP record, last | 20 | 3.66 / 3.70 | 3.32 / 3.35 | 6.58 / 6.77 | 6.16 / 6.33 |
| MAAP record, last | 20 | 3.65 / 3.74 | 3.31 / 3.39 | 5.49 / 5.43 | 5.11 / 5.36 |
| AECP record, last | 20 | 10.01 / 10.27 | 9.39 / 9.62 | 14.21 / 15.28 | 13.55 / 13.98 |
| SRP record, last | 18 | 10.81 / 10.55 | 10.18 / 9.89 | 16.45 / 15.72 | 14.68 / 15.15 |
| an ACMP command behind a full acmp ring | 20 | 3.78 / 3.66 | 3.38 / 3.40 | 7.11 / 6.81 | 6.33 / 6.89 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 2.94 / 2.85 | 2.61 / 2.58 | 4.69 / 5.49 | 5.01 / 4.95 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 20 | 0.08 / 0.14 | 0.09 / 0.05 | 0.09 / 0.18 | 0.08 / 0.09 |
| an event behind 15 others | 20 | 0.97 / 0.94 | 0.88 / 0.89 | 1.51 / 1.51 | 1.40 / 1.50 |
| AECP record, last, in the owed window | 20 | **63.03** / **62.97** | **62.91** / **63.00** | **64.81** / **64.87** | **64.78** / **64.96** |
| a response with 7 frames owed ahead of it | 20 | **62.16** / **62.13** | **62.07** / **62.13** | **63.55** / **63.62** | **63.56** / **63.66** |
| an ACMP command behind the owed input | 20 | **never** / **never** | **never** / **never** | **never** / **never** | **never** / **never** |

A save's windows opened from idle (save_window.py), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.52 / 1.45 | 1.44 / 1.42 | 1.86 / 1.83 | 1.77 / 1.87 |
| ADP record, first | 20 | 1.51 / 1.44 | 1.43 / 1.41 | 1.85 / 1.82 | 1.76 / 1.86 |
| MAAP record, first | 20 | 1.55 / 1.47 | 1.46 / 1.45 | 1.89 / 1.85 | 1.79 / 1.90 |
| AECP record, first | 20 | 1.56 / 1.48 | 1.47 / 1.46 | 1.90 / 1.86 | 1.80 / 1.91 |
| SRP record, first | 18 | 2.72 / 2.58 | 2.50 / 2.47 | 4.22 / 3.70 | 3.89 / 3.70 |
| ACMP record, last | 20 | 6.12 / 5.89 | 5.59 / 5.45 | 9.35 / 9.26 | 8.42 / 8.57 |
| ADP record, last | 20 | 4.68 / 4.41 | 4.17 / 4.12 | 7.02 / 7.13 | 6.45 / 6.62 |
| MAAP record, last | 20 | 4.61 / 4.44 | 4.21 / 4.16 | 6.41 / 6.63 | 6.08 / 6.41 |
| AECP record, last | 20 | 10.68 / 11.05 | 10.18 / 10.25 | 15.64 / 15.94 | 14.19 / 15.05 |
| SRP record, last | 18 | 11.59 / 11.26 | 11.05 / 10.74 | 17.52 / 16.44 | 15.08 / 15.53 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.88 / 3.55 | 3.38 / 3.34 | 5.76 / 5.86 | 5.30 / 5.45 |

A save's windows opened with the step's age at its limit, two (save_window.aged_window), 24 at each leg:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.17 / 0.79 | 1.02 / 1.09 | 1.28 / 1.65 | 1.52 / 1.62 |
| ADP record, first | 20 | 1.16 / 0.78 | 1.01 / 1.08 | 1.27 / 1.64 | 1.51 / 1.61 |
| MAAP record, first | 20 | 0.90 / 0.81 | 0.75 / 1.11 | 1.31 / 1.28 | 1.20 / 1.27 |
| AECP record, first | 20 | 0.91 / 0.82 | 0.76 / 1.12 | 1.32 / 1.29 | 1.21 / 1.28 |
| SRP record, first | 18 | 2.41 / 2.30 | 2.11 / 2.13 | 4.17 / 3.61 | 4.19 / 3.49 |
| ACMP record, last | 20 | 6.79 / 6.57 | 6.19 / 6.02 | 10.16 / 10.06 | 9.19 / 9.34 |
| ADP record, last | 20 | 5.37 / 5.20 | 4.87 / 4.78 | 7.97 / 7.92 | 7.40 / 7.39 |
| MAAP record, last | 20 | 4.53 / 4.37 | 4.11 / 4.03 | 6.51 / 6.41 | 6.04 / 6.16 |
| AECP record, last | 20 | 11.17 / 11.29 | 10.52 / 10.61 | 16.26 / 16.63 | 14.51 / 15.52 |
| SRP record, last | 18 | 11.92 / 11.62 | 11.22 / 11.20 | 17.66 / 17.29 | 15.68 / 16.31 |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 4.57 / 4.41 | 4.14 / 4.06 | 6.67 / 6.65 | 6.25 / 6.22 |

The same one short of it, one, 24 at each leg that ran them (both arms, without the drafts):

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 1.17 / 1.12 | - / - | 1.28 / 1.64 | - / - |
| ADP record, first | 20 | 1.16 / 1.11 | - / - | 1.27 / 1.63 | - / - |
| MAAP record, first | 20 | 0.86 / 0.83 | - / - | 1.30 / 1.28 | - / - |
| AECP record, first | 20 | 0.87 / 0.84 | - / - | 1.31 / 1.29 | - / - |
| SRP record, first | 18 | 3.12 / 2.16 | - / - | 5.03 / 3.58 | - / - |
| ACMP record, last | 20 | 6.01 / 5.93 | - / - | 9.30 / 9.08 | - / - |
| ADP record, last | 20 | 4.58 / 4.56 | - / - | 7.05 / 6.95 | - / - |
| MAAP record, last | 20 | 4.00 / 3.80 | - / - | 6.25 / 6.05 | - / - |
| AECP record, last | 20 | 10.42 / 10.54 | - / - | 16.28 / 16.56 | - / - |
| SRP record, last | 18 | 12.23 / 10.78 | - / - | 17.77 / 17.33 | - / - |
| an ENTITY_AVAILABLE behind a full adp ring | 20 | 3.78 / 3.78 | - / - | 5.74 / 5.67 | - / - |

save-held, every receive channel at its refill rate with its bursts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.78 / 2.72 | 2.29 / 2.28 | 4.65 / 4.61 | 4.25 / 4.42 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.33 / 4.25 | 3.68 / 3.64 | 8.18 / 7.46 | 6.96 / 7.70 |
| AECP record, every channel at its refill rate, the longest | 20 | 5.52 / 5.48 | 5.01 / 5.03 | 10.56 / 10.34 | 9.04 / 9.63 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.97 / 2.75 | 2.50 / 2.55 | 5.14 / 5.09 | 4.62 / 4.82 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.49 / 8.02 | 7.11 / 7.05 | 14.53 / 14.32 | 12.74 / 13.59 |

save-starved, the same and a grandmaster change as every pass starts:

| Row | Bound, ms | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|---:|
| ADP record, every channel at its refill rate, the longest | 20 | 2.86 / 2.81 | 2.37 / 2.60 | 4.74 / 4.70 | 4.34 / 4.63 |
| ACMP record, every channel at its refill rate, the longest | 20 | 4.48 / 4.42 | 3.82 / 4.04 | 8.39 / 7.65 | 6.98 / 7.91 |
| AECP record, every channel at its refill rate, the longest | 20 | 6.13 / 6.06 | 5.64 / 5.65 | 11.23 / 10.99 | 9.67 / 10.38 |
| MAAP record, every channel at its refill rate, the longest | 20 | 2.92 / 2.87 | 2.68 / 2.59 | 5.27 / 5.22 | 4.73 / 4.94 |
| SRP record, every channel at its refill rate, the longest | 18 | 8.65 / 8.61 | 8.00 / 7.94 | 15.08 / 14.90 | 13.59 / 14.26 |

The share is 2.0 ms. Passes over it, of the work passes run, and the longest in ms, arm A / arm B:

| Groups | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| The four backlog windows | 0 of 1315, 1.14 / 0 of 1272, 1.11 | 0 of 1318, 1.04 / 0 of 1273, 1.03 | 0 of 1355, 1.63 / 0 of 1311, 1.85 | 0 of 1362, 1.53 / 0 of 1312, 1.81 |
| A save's windows from idle | 0 of 12644, 1.16 / 0 of 8798, 1.12 | 0 of 12640, 1.13 / 0 of 8796, 1.12 | 0 of 22645, 1.90 / 0 of 11936, 1.86 | 0 of 22731, 1.77 / 0 of 11937, 1.81 |
| Aged windows at the limit | 0 of 25748, 1.15 / 0 of 22572, 1.12 | 0 of 25715, 1.13 / 0 of 22195, 1.12 | 0 of 29414, 1.90 / 0 of 19133, 1.87 | 0 of 30654, 1.78 / 0 of 18234, 1.82 |
| Aged windows one short of it | 0 of 23328, 1.28 / 0 of 20074, 1.20 | 0 of 0, 0.00 / 0 of 0, 0.00 | 0 of 28096, 1.90 / 0 of 17786, 1.87 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| save-held | 0 of 3426, 1.13 / 0 of 3429, 1.13 | 0 of 3439, 1.11 / 0 of 3433, 1.12 | 0 of 8623, 1.66 / 0 of 8638, 1.65 | 0 of 8678, 1.57 / 0 of 8665, 1.61 |
| save-starved | 0 of 42843, 0.97 / 0 of 42843, 0.97 | 0 of 43204, 0.97 / 0 of 41993, 0.97 | 0 of 57407, 1.69 / 0 of 58001, 1.67 | 0 of 58295, 1.60 / 0 of 52030, 1.64 |
| save-second | 0 of 81422, 0.96 / 0 of 81198, 0.97 | 0 of 81075, 0.97 / 0 of 78972, 0.96 | 0 of 129900, 1.31 / 0 of 0, 0.00 | 0 of 0, 0.00 / 0 of 0, 0.00 |
| Every group run | 0 of 199801, 1.28 / 0 of 180796, 1.20 | 0 of 168001, 1.13 / 0 of 157272, 1.12 | 0 of 286852, 1.90 / 0 of 117430, 1.87 | 0 of 122348, 1.78 / 0 of 92803, 1.82 |

Saves, ms from the change to durable against the stated worst case, arm A / arm B (steps; longest gap between flash steps, ms):

| Group | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| save | 2018.4 of 4,070 (102; 10.95) / 2018.5 of 4,070 (102; 10.988) | 2018.4 of 4,070 (102; 10.946) / 2018.5 of 4,070 (102; 10.843) | 4697.3 of 12,110 (370; 11.3) / 4698.2 of 12,110 (370; 11.367) | 4698.2 of 12,110 (370; 11.322) / 4697.3 of 12,110 (370; 11.28) |
| save-held | 2018.2 of 4,070 (102; 14.206) / 2018.3 of 4,070 (102; 14.275) | 2018.2 of 4,070 (102; 13.966) / 2018.3 of 4,070 (102; 13.935) | 4696.9 of 12,110 (370; 18.923) / 4730.9 of 12,110 (370; 18.217) | 4707.9 of 12,110 (370; 17.255) / 4696.9 of 12,110 (370; 18.348) |
| save-starved | 4048.1 of 4,070 (102; 31.043) / 4048.2 of 4,070 (102; 31.119) | 4048.1 of 4,070 (102; 30.893) / 4048.2 of 4,070 (102; 30.959) | 12087.0 of 12,110 (370; 31.092) / 12087.9 of 12,110 (370; 31.1) | 12087.9 of 12,110 (370; 31.115) / 12086.7 of 12,110 (370; 31.106) |
| save-second | 6029.8 of 6,070 (102; 30.948) / 6029.9 of 6,070 (102; 30.937) | 6029.9 of 6,070 (102; 30.895) / 6029.8 of 6,070 (102; 30.927) | 22110.1 of 22,150 (370; 31.041) / - | - / - |

Aged windows: the least margin and its row, the aged steps among their records (count, the longest aged pass, CPU cycles (ms), and the kinds), per age, arm A / arm B:

| Age | 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---|---:|---:|---:|---:|
| 2 | 6.077 (11.923, program-aged2-7); 24 aged in 24, longest 90,231 (0.902), issue/read-back / 6.380 (11.620, program-aged2-7); 24 aged in 24, longest 83,253 (0.833), issue/read-back | 6.776 (11.224, blank-aged2-7); 24 aged in 24, longest 89,359 (0.894), issue/read-back / 6.798 (11.202, blank-aged2-0); 24 aged in 24, longest 83,413 (0.834), issue/read-back | 0.335 (17.665, verify-aged2-4); 24 aged in 24, longest 85,164 (0.852), issue/read-back / 0.713 (17.287, verify-aged2-4); 24 aged in 24, longest 83,661 (0.837), issue/read-back | 2.318 (15.682, verify-aged2-7); 24 aged in 24, longest 85,683 (0.857), issue/read-back / 1.693 (16.307, verify-aged2-7); 24 aged in 24, longest 84,117 (0.841), issue/read-back |
| 1 | 5.771 (12.229, blank-aged1-7); 0 aged in 24 / 7.218 (10.782, blank-aged1-5); 0 aged in 24 | - / - | 0.235 (17.765, verify-aged1-7); 14 aged in 24, longest 84,053 (0.841), issue/read-back / 0.674 (17.326, verify-aged1-7); 13 aged in 24, longest 83,311 (0.833), issue/read-back | - / - |

Passes that carry the store's step, every group: count, the longest pass and the longest step, CPU cycles (ms), arm A / arm B:

| 1x1/1if | 1x1/1if, with both drafts | 8x8/2if | 8x8/2if, with both drafts |
|---:|---:|---:|---:|
| 30478: 128,083 (1.281); 96,212 (0.962) / 26876: 120,051 (1.201); 95,990 (0.960) | 19050: 113,084 (1.131); 96,078 (0.961) / 19050: 112,416 (1.124); 96,030 (0.960) | 40519: 130,212 (1.302); 95,999 (0.960) / 35688: 126,891 (1.269); 95,746 (0.957) | 25123: 125,743 (1.257); 95,873 (0.959) / 25120: 127,428 (1.274); 96,034 (0.960) |

A window opened from idle still takes no aged step among its records at this head: its longest drain, from its opening to the end of the pass that releases its last record, is 17.559 ms (8x8/2if, arm A, `backlog-adp@program-2`), 2.441 ms short of the two ticks before its third centisecond.

### What is left

- The owner kept 8x8 in the Mark II split's scope, approved T_svc = 20 ms ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075)) and put the split CPU on `sys` at 100 MHz ([decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239)).
- **With the CPU on `sys` at 100 MHz** every row the CPU decides and every pass fits at both points, a save in progress, both links changing at once and every receive channel held at its refill rate through a whole save, with no pass empty or not, included, a save's windows opened with the step's age at its limit, so an aged step among their records, included, and every channel's burst composed under input that leaves no pass empty included, with the least margin the 8x8 last SRP record's, 0.235 ms (17.765 ms, arm A, a save's verify window opened one short of the age limit) ([above](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)).
- The TSN stack's and lwSRP's changes reach this branch only through those repositories' reviews, then a pin move: the TSN stack's with the hot list's runtime entry removed, lwSRP's with `ctrl_arms.LWSRP_REV`.
- The three rows no CPU lever moves are unchanged: the 60 ms egress hold, `ACMP_OWED_MAX`, and the command behind the owed input. They stay with [tsn-c-stack #26](https://github.com/kebag-logic/tsn-c-stack/issues/26).
- The block-RAM ledger, 124 against 121.5 ([the area plan](MARK_II_AREA_PLAN.md)), is commissioned separately.
- **A save's progress** is bounded whatever the input: a step not run for more than two centiseconds is the next pass's alone, so a save advances at least one step every three ticks. A SET_NAME of the entity is durable at most 12,110 ms after it at 8x8/2if and 4,070 ms at 1x1 with no save in flight, and 22,150 ms and 6,070 ms when marked just after another's save in flight took its first record, on a flash with no busy time; on the product's flash part at its datasheet maximum, 15,370 and 28,670 ms at 8x8/2if, 7,140 and 12,210 ms at 1x1 ([above](#aged-windows-a-change-while-a-save-is-in-flight-and-the-retry)). The contract's buckets bound the records' rate, and with every receive channel at its refill rate with its bursts the step is never held off to the limit (`save-held`, durable as fast as alone); the event sources are coalesced but not rated, and a grandmaster change as every pass starts holds every step to it (`save-starved`, `save-second`). Such input before a window can open it at the age limit, and it then takes one aged step among its records; a window opened from idle takes none, since its longest drain, 17.559 ms, is shorter than the two ticks before its third centisecond. #823's 0.5 s is the append-only design's writer's, through this same step; this image does not meet it.
- **A change-notice retry** is taken only in a pass that took no input and dispatched no centisecond, after an aged step or an aged build, or, once held 4 ms past its time, in a pass of its own (THE RETRY in `ctrl_loop.h`), so no pass of a burst holds one, and a notice whose port answers is committed within 18 ms of the answer under any input, inside its 20 ms (`aecp.h`): 12.30 to 13.51 ms at both points under input that leaves no pass empty ([above](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)). Each notice owed ahead of it costs it its own round and the pass that sends it.
- **SRP's MRPDU build is a pass class of its own** (THE TRANSMIT in `ctrl_loop.h`), taken only in a pass that took no record, at most one event and no centisecond, or once held past its age in a pass of its own, within `CTRL_LOOP_TX_MS`, 44 ms, so every participant's MRPDU is sent within the 200 ms JoinTime. A pass that dispatches a centisecond takes one record of a channel (THE TICK's cap).
- **SRP's 18 ms, `CTRL_LOOP_SRP_MS`, is THE SHARE's nine passes, and the composed burst's 32 SRP records at 8x8/2if take sixteen:** that row fits by the measured cost of its passes, which hold no build except in a pass that took no record at all, not by the constants ([above](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)).
- **The margins at this head:** 0.235 ms on the 8x8 last SRP record (arm A), and 9,580 cycles on the share (a pass that takes a record, 1.904 ms at 8x8/2if); every pass class sits at least 6,490 cycles, the data layout's measured swing, under the share at both points, at the head's layout and at the struct-ends layout ([above](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)). A change that grows the hot code ahead of SRP's drain, or adds fields to the loop's or a module's structs, must measure them again.
- The platform image's four hot-list entries that name the size fixture's callbacks place nothing there, and its own callbacks are not on the list.
- The routed split image is lane S9's. [Section 14](#14-the-32x32-estimate) carries these figures to Mark II's shape.

## 14. The 32x32 estimate

Mark II's shape is 32x32: 16x16 logical streams, each redundant on both networks, on one TDM8 bus ([owner, 2026-10-31](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545621753)).
No such shape exists yet, so nothing here measures it.
The first table is a derivation from this branch's measurements, marked as an estimate, against T_svc = 20 ms and each family's ceiling; the one-CPU table is measured; the gPTP share is an assumption, labelled as one.

### The estimate

Each row's 8x8/2if measurement, with the CPU on `sys` at 100 MHz, is carried to 64 streams three ways, and the rings and buckets stay the contract's, so a window holds the same records:

- **U** is the assigned derivation: four times the 8x8/2if figure, every cycle taken to grow with the streams.
- **L** is the measured growth: the line through 1x1/1if (2 streams) and 8x8/2if (16), to 64.
- **S** is the streams' own growth: the 8x8/2if figure plus the slope from 1x1/1if to 8x8/1if, which holds the interfaces at one. Its slope uses arm A at both ends, since the 8x8/1if point ran in arm A only: section 13's arm A 1x1/1if figures (the last AECP record's 10.01 ms), not the 1x1/1if column below, which is the worst of the arms. The 8x8/1if point is a labelled scratch arm, not on this branch.

Worst of the arms measured at this head (2026-11-05, the code head `65a56d02`), over the four backlog windows, ms, over the bound in bold with the excess (estimates in the last three columns):

| Row | Bound, ms | 1x1/1if | 8x8/1if | 8x8/2if | U: 4 x 8x8/2if | L: the line, 1x1/1if to 8x8/2if | S: the streams alone |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.82 | 1.18 | 1.35 | 5.4 | 3.1 | 2.6 |
| ADP record, first | 20 | 0.86 | 1.22 | 1.39 | 5.6 | 3.2 | 2.6 |
| MAAP record, first | 20 | 0.84 | 1.21 | 1.37 | 5.5 | 3.2 | 2.6 |
| AECP record, first | 20 | 0.86 | 1.22 | 1.38 | 5.5 | 3.2 | 2.6 |
| SRP record, first | 18 | 3.05 | 4.76 | 5.49 | **21.9** (+3.9) | 13.8 | 11.4 |
| ACMP record, last | 20 | 5.19 | 7.81 | 8.90 | **35.6** (+15.6) | **21.6** (+1.6) | 18.0 |
| ADP record, last | 20 | 3.70 | 5.66 | 6.77 | **27.1** (+7.1) | 17.3 | 13.6 |
| MAAP record, last | 20 | 3.74 | 4.89 | 5.49 | **21.9** (+1.9) | 11.5 | 9.8 |
| AECP record, last | 20 | 10.27 | 13.17 | 15.28 | **61.1** (+41.1) | **32.5** (+12.5) | **26.1** (+6.1) |
| SRP record, last | 18 | 10.81 | 14.93 | 16.45 | **65.8** (+47.8) | **35.8** (+17.8) | **30.6** (+12.6) |
| An ACMP command behind a full ACMP ring | 20 | 3.78 | 5.88 | 7.11 | **28.4** (+8.4) | 18.5 | 14.3 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.94 | 3.82 | 5.49 | **22.0** (+2.0) | 14.2 | 8.5 |
| An event behind 15 others | 20 | 0.97 | 1.33 | 1.51 | 6.0 | 3.4 | 2.8 |
| The longest work pass | 2 | 1.14 | 1.59 | 1.85 | **7.4** (+5.4) | **4.3** (+2.3) | **3.4** (+1.4) |

The rows that would not fit, and by how much:

- **AECP record, last, under S, L and U:** over by 6.1, 12.5 and 41.1 ms.
- **SRP record, last, under S, L and U:** over by 12.6, 17.8 and 47.8 ms.
- **The longest work pass, under S, L and U:** 3.4, 4.3 and 7.4 ms, over the 2.0 ms share by 1.4, 2.3 and 5.4 ms.
- **ACMP record, last, under L and U:** over by 1.6 and 15.6 ms.
- **Under U alone:** SRP record, first by 3.9 ms, ADP record, last by 7.1 ms, MAAP record, last by 1.9 ms, an ACMP command behind a full ACMP ring by 8.4 ms, an ENTITY_AVAILABLE behind a full ADP ring by 2.0 ms.

So the last AECP and SRP records and the per-pass share miss whichever way the growth is read, the last ACMP record under two of the three readings, and the rest of U's misses depend on how much of each row grows with the streams.
Against `5e2651d5`'s estimate the longest pass is lower (1.85 ms at 8x8/2if against 1.99) and the other channels' last records are later (ACMP 8.90 ms against 8.54, ADP 6.77 against 6.07): THE TICK's cap gives a pass that dispatches a centisecond one record of a channel ([section 13](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)), so those records wait a pass more for each such pass.
The last SRP record waits for its channel's 32 records at two a pass, so its row is about sixteen passes, and every pass carries the polls' per-stream cost: an idle pass takes about 8,700 CPU cycles at 1x1/1if and 15,400 at 8x8/2if, where the loop calls THE TRANSMIT's and THE RETRY's clients in every pass that takes nothing (the commonest shortest pass of the four backlog windows' idle runs, arm A).
The derivation has limits a measurement would not: 8x8/2if already holds its streams per interface, so a 32x32 interface holds twice its streams where the entity holds four times, which makes U an upper reading for the per-interface work (SRP); nothing here knows the cost of 64-stream tables that were never linked, and the Block RAM they need binds first ([the area plan](MARK_II_AREA_PLAN.md)).

### One CPU, measured

The owner's lever order names one CPU, no second hart, as lever 4 ([#640](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6545540394)).
As built, the split placement has one hart already: `MilanSoC` gives its only CPU, `cpu_count` 1, the split options under `--ctrl-mailbox`, and the harness measures that one hart with the protocol firmware, its boot path and the saved-state store on it.
So the estimate's 3,948 LUTs of split CPU are added to an image that still counts the all-fabric CPU's 3,249, and lever 4's saving removes a second hart the code does not build.
What the lever can still ask is whether the firmware fits the SoC core as it ships: cacheless, without the split CPU's caches or RV32M.
Measured on `sys` at 100 MHz at `c954b8a9`, before THE STEP, the four backlog groups, arm A, the image rebuilt for each CPU (bold over the bound; the cacheless RV32I arm is a labelled scratch arm, not on this branch):

| Row | Bound, ms | Split CPU, 1x1 | Cacheless RV32IM, 1x1 | Cacheless RV32I, 1x1 | Split CPU, 8x8 | Cacheless RV32IM, 8x8 | Cacheless RV32I, 8x8 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ACMP record, first | 20 | 0.75 | 1.56 | 1.58 | 1.30 | 2.90 | 2.93 |
| ADP record, first | 20 | 0.79 | 1.60 | 1.62 | 1.34 | 2.94 | 2.98 |
| MAAP record, first | 20 | 0.77 | 1.58 | 1.60 | 1.33 | 2.92 | 2.96 |
| AECP record, first | 20 | 0.78 | 1.59 | 1.61 | 1.34 | 2.93 | 2.97 |
| SRP record, first | 18 | 2.79 | 5.44 | 5.63 | 5.35 | 11.37 | 11.72 |
| ACMP record, last | 20 | 5.16 | 9.98 | 10.45 | 7.76 | 16.08 | 16.09 |
| ADP record, last | 20 | 3.65 | 7.14 | 7.78 | 5.81 | 11.70 | 11.77 |
| MAAP record, last | 20 | 3.68 | 7.18 | 7.81 | 5.80 | 11.71 | 11.75 |
| AECP record, last | 20 | 9.67 | 17.34 | 19.76 | 14.41 | **26.83** | **28.51** |
| SRP record, last | 18 | 9.95 | 17.98 | **21.63** | 15.88 | **30.26** | **34.52** |
| An ACMP command behind a full ACMP ring | 20 | 3.45 | 6.87 | 7.06 | 6.51 | 14.29 | 14.42 |
| An ENTITY_AVAILABLE behind a full ADP ring | 20 | 2.73 | 5.50 | 5.94 | 3.53 | 8.75 | 7.78 |
| An event behind 15 others | 20 | 0.88 | 1.82 | 1.84 | 1.44 | 3.16 | 3.20 |
| Passes over the 2.0 ms share, longest ms | 2 | 0 of 1277, 1.07 | **3 of 1267, 2.14** | **3 of 1270, 2.35** | 0 of 1319, 1.97 | **62 of 1314, 3.61** | **64 of 1315, 3.85** |

The cacheless core does not fit 8x8: the last AECP and SRP records miss, and about 60 passes a run are over the share.
At 1x1 the RV32IM arm fits every row, the last SRP record by 0.02 ms, with three passes over the share; RV32I misses the last SRP record too.
Against those, the split CPU on `sys` costs 5 tiles of Block RAM (9.5 against 4.5) and about 300 LUTs (3,543 against 3,249) more than the shipping core, and at the head that measured these arms its image planned 56.5 tiles where RV32I's planned 57.0; at this head it plans 57.0 ([section 5](#5-fit)).
The quiet work load, work-pass cycles over elapsed cycles from `settled` to `composed`, is 1.14 % at 1x1/1if and 2.80 % at 8x8/2if on the split CPU, 6.22 % and 6.55 % on the two cacheless arms at 8x8/2if: load is not what binds, the burst is.
The estimate carries that quiet load to 5.9 to 11.2 % at 32x32.

### gPTP's share, an assumption

The protocol processor goes at the switch-over and gPTP moves to firmware at lane F6 ([owner, 2026-10-31](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6545457321)); the fabric keeps the timestamps on both ports.
None of this is measured, because no gPTP firmware is linked here.
The assumption, from Milan v1.2's intervals (Sync 125 ms, Announce and Pdelay 1 s) and the message set of IEEE 802.1AS-2011 with its Corrigenda 1 and 2:

| Quantity | Assumed | Basis |
|---|---:|---|
| Frames a second | 46 | 23 a port, two ports: Sync and Follow_Up 16, Announce 1, Pdelay 6 (requester and responder) |
| Servo runs a second | 16 | One per Sync, each port |
| CPU cycles a frame or servo run | 40,000 (20,000 to 100,000) | About twice a measured ACMP record; the surveyed stack [uses soft double math](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6551164172) |
| Sustained load | 2.48 % (1.24 to 6.2) | 62 units a second, a frame or a servo run each, x 40,000 cycles at 100 MHz |

Each unit, a frame or a servo run, is 0.4 ms at 40,000 cycles (0.2 to 1.0 ms over the range).
What that adds, from the same units (2026-11-02; the round before gave 1.6 ms on a row and 0.8 ms on a pass, from the frames alone):

| Addition | Units | ms | Mean or bound | Basis |
|---|---:|---:|---|---|
| To a row, mean | 1.1 | 0.45 (0.22 to 1.1) | Mean | 62 units a second over the row's bound, 18 ms for SRP |
| To a row, bound | 20 | 8.0 (4.0 to 20.0) | Bound | All that can fall in one 18 ms: on each port one Sync, its Follow_Up and the servo run they start (Sync is 125 ms), one Announce, and one Pdelay exchange each way, three frames each (Pdelay is 1 s) |
| To a pass, bound | 4 | 1.6 (0.8 to 4.0) | Bound | Two records a channel a pass (`CTRL_LOOP_RX_PER_PASS`), each a Follow_Up starting its servo run |

At 8x8/2if the last SRP record takes 17.77 ms against 18 at its worst, in a save's verify window opened one short of the age limit, arm A ([section 13](#the-retrys-age-limit-the-transmit-the-ticks-cap-and-every-pass-class)): the mean, 0.45 ms, puts it 0.21 ms over, and the bottom of its range, 0.22 ms, leaves it 0.01 ms under; the top, 62 x 0.018 x 1.0 ms = 1.116 ms, puts it 0.88 ms over, and the bound 7.77 ms over. At `5e2651d5`, 17.90 ms, the mean put it 0.35 ms over.
The longest pass, 1.90 ms, takes 3.50 ms under the pass's bound, 1.50 ms over the 2.0 ms share; so gPTP's records, when F6 links them, need their own room in the pass, which these figures do not give them.
So the sustained share is small, and the bursts are what it touches: the longest 32x32 pass becomes 5.0 ms under S and 9.0 ms under U.
A Pdelay response waits for the pass running when its request arrives, then its own, and Milan v1.2 4.2.6.2.6 allows 15 ms of turnaround: 10.0 ms under S fits, 18.0 ms under U does not.

**What would measure it:** F6's stack linked into this harness's image behind the HAL, the mailbox channel it takes in the contract, and a stimulus of these frames on both ports at their intervals, graded here for each frame's cost, the servo's, the pass and the Pdelay turnaround, at 8x8/2if first and at 32x32 when that shape exists.

### What the estimate leaves to the owner

These are not decided here.

- **The last AECP and SRP records and the per-pass share at 32x32.** The levers are the rings and buckets the contract admits, the two records a pass of the owner's D4(b), the 2.0 ms share itself, and the firmware's per-stream polls; which of them is the owner's.
- **Which CPU lever 4 means.** The split placement already has one hart. The cacheless core would save about 300 LUTs and 5 tiles, and does not fit 8x8.
- **The CPU clock past 100 MHz, or a second hart,** if the firmware's levers do not close 32x32. Each runs against the area target.

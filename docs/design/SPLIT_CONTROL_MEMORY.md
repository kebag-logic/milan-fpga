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

Every refusal raises `ctrl_memory.Refusal`, whose `check` names it.

| Check | Refuses |
|---|---|
| `reset entry` | An image entering anywhere but `rom`'s first byte, or with no initial bytes there |
| `memory map` | A section outside both regions, initial bytes outside `rom`, or a NOBITS section in `rom` |
| `memory-map overlap` | Two sections sharing an address or a load address, or the two regions overlapping |
| `allocation over budget` | Banks totalling more than 56 RAMB36, a RAMB18 counting half |
| `staging buffer` | An `nvm_stage` that is not the selected shape's stage: its KLJ2 container plus one record header |

The budget is the owner's 224 KB at 4,096 usable bytes per RAMB36 (#640 ruling 6101485877).
The SoC build runs the first four while it builds the memory.
`main()` runs the staging check before any export; the shape comes from `--entity-gen-dir`.

The three planted controls fail by name in [`test_ctrl_memory.py`](../../sw/litex/test_ctrl_memory.py) and in the SoC build itself:

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
Mapped out of context by `syn/ooc/ctrl_memory_ooc.py`: Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`.

| Point | `rom` need, B | `sram` need, B | Planned RAMB36 equivalents | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT / FF | Byte floor |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 95,032 | 45,520 | 35.0 | 33 / 2 | 34.0 | 212 / 32 | 35 |
| 1x1, two interfaces | 96,320 | 56,880 | 38.0 | 37 / 1 | 37.5 | 89 / 7 | 38 |
| 8x8, one interface | 108,680 | 86,080 | 48.5 | 46 / 2 | 47.0 | 307 / 33 | 48 |
| 8x8, two interfaces (largest) | 110,056 | 112,208 | 54.5 | 52 / 2 | 53.0 | 328 / 40 | 55 |

"Planned" is `ctrl_memory.plan` with every bank in block RAM.
The banks hold 96.6 to 99.6 percent of their bytes.
The byte floor is the flat linked span at 4,096 B per RAMB36, rounded up.
Every point is within the 56-RAMB36 budget, and the largest leaves 3 tiles.

Two Vivado optimisations put the ROM below its plan:

- it trims a ROM bit column that is constant across a bank, so `16384x31` takes 15 RAMB36 and one RAMB18;
- it maps a small or sparse ROM bank into logic: the 512-word bank at 1x1 with one interface, and the 1,024-word bank at 8x8.

That logic is most of each point's LUTs: 231 of the largest point's 328.
The `sram` banks map exactly as planned, and their LUTs are the bank decode and read multiplexer.
LiteX's memory emitter carries no `ROM_STYLE`, so this round keeps Vivado's default.
M8a-2's route weighs those LUTs against at most 1.5 tiles.

Before: the base image's BIOS ROM took 16 RAMB36 and its SRAM 2.
One LiteX SRAM of the largest image's whole need took 64 RAMB36.
The ledger rows are in the [plan](MARK_II_AREA_PLAN.md#firmware-and-block-ram-ledger): 113 tiles after the split's release.

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

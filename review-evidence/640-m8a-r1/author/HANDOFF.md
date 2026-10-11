# HANDOFF: lane M8a-1 for #640 (split placement's on-chip control memory)

Executor [A594]. Reviewers [R606] (internal), [R607] (external).
Branch `640-m8a` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (local, not pushed).
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100426002
STOP (round 1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101473717 (its handoff and PR body are kept in `stop-round/`)
Ruling: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877
REVIEW READY (M8a-1): https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6104411638

## Status

**REVIEW READY (M8a-1).** Head `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14`: four commits on dev `e8454e27`, local, not pushed.

- **Fit:** holds at all four points. As mapped, 34.0 / 37.5 / 47.0 / 53.0 tiles (RAMB36 + RAMB18/2) against the 56-RAMB36 budget, with no power-of-two waste.
- **Ledger:** 124 tiles before the split's conditional release, 113 after; 121.5 is the ceiling and the 13.5 reserve is untouched.
- **Planted controls:** all three fail by name, in the unit test and through the real SoC build.
- **Default:** the all-fabric default is digest-identical for both AX7101 shipping configs.
- **Gates:** every gate the change touches passed (section 11).
- **Open:** M8a-2 (boot, service checks, route) waits for F-INT PR 2.

## Contents

1. Scope of this round
2. Changes, with file:line
3. Memory map and instantiation
4. Linked spans at the four points
5. Primitive mapping, before and after
6. Ledger rows, measured
7. Planted controls, and the defect each test catches
8. Boot console and diagnostics; DDR3 at this base
9. All-fabric default: digest-identical
10. All-fabric image without DDR3 (measurement only)
11. Gate table
12. Not in this round, and open risks
13. Reproduction

## 1. Scope of this round

From the ruling (6101485877):

- the owner's 224 KB binds: up to 56 RAMB36 as mapped; the ledger takes the split's conditional release (-11 tiles) and stays at or under 121.5 with the 13.5 reserve untouched;
- no power-of-two waste; the four points at or near their floor; RAMB36 and RAMB18 reported as mapped;
- the firmware owns the reset entry in the split placement; no BIOS ROM or SRAM there; the all-fabric image keeps its BIOS;
- M8a-1 is the memory map and instantiation behind `--ctrl-mailbox`, the fit proof, the linked spans, the ledger rows, the three planted controls and the default digest-identical;
- M8a-2, after F-INT PR 2: the split-image simulation boot, `check_nvm_capture.py` 8x8, `nvm_cosim`, `nvm_capture_cpu` and the integrated route through the M0s recipe.

## 2. Changes, with file:line

Commits (one-line, no trailers):

- `c20ed894a3b577407588e30ff365480a7e7be26a` Build the split placement's firmware ROM and RAM from the linked image behind --ctrl-mailbox, in power-of-two banks with no BIOS (#640 M8a-1)
- `94190c36501cce6082b9fa93c916a8ecbaca0455` Give the split memory plan's and test's nested helpers the docstrings the Python idiom gate requires
- `a475ab5ab4e3eb75a1ab79f913cf9f6893f42d2b` Document the split placement's control memory and record M8a-1's measured firmware block RAM ledger rows (#640)
- `5d532e9dcd2bb8d19f8017cc0c2d6e02ec556d14` State the split ROM mapping default without process language, as the docs wording gate requires

18 files, +1,270 / -55.

| File:line | Change |
|---|---|
| `sw/litex/ctrl_memory.py:44-89` | New. The contract: 4,096 B per RAMB36, the 2,048 B RAMB18 granule, the 56-RAMB36 budget, `rom` at `0x0000_0000` and `sram` at `0x1000_0000`, each 224 KiB |
| `sw/litex/ctrl_memory.py:139` | `banks()`: the need in granules, its binary digits as banks, largest first |
| `sw/litex/ctrl_memory.py:151` | `read_elf()`: entry, allocated sections (address, load address, loaded or NOBITS), symbols, load segments of an RV32 ELF |
| `sw/litex/ctrl_memory.py:197` | `check_map()`: `reset entry`, `memory map` and `memory-map overlap` (sections, load addresses, regions) |
| `sw/litex/ctrl_memory.py:219` | `plan()`: the needs and banks; `allocation over budget` above 56 RAMB36 |
| `sw/litex/ctrl_memory.py:236` | `rom_words()`: the initial contents of `rom` |
| `sw/litex/ctrl_memory.py:245` | `stage_bytes()`: the shape's KLJ2 container (scripts' `inventory` and `klj2_assemble`) plus one record header, as `nvm_shape.h` derives `NVM_STAGE_BYTES` |
| `sw/litex/ctrl_memory.py:263` | `check_stage()`: `staging buffer` |
| `sw/litex/ctrl_memory.py:273, 281` | `regions_ld()` for the link; the CLI (`regions`, `plan`) |
| `sw/litex/milan_soc.py:44` | `import ctrl_memory` |
| `sw/litex/milan_soc.py:2578` | `CtrlMemory`: one region as banks of LiteX `wishbone.SRAM` behind a `wishbone.Decoder`; past the last bank, `err` at once |
| `sw/litex/milan_soc.py:2608` | `add_ctrl_memory()`: checks the CPU's reset address and `sram` origin, plans the image, adds `rom` (read-only, initialised) and `sram`, sets LiteX's `integrated_rom_initialized` so no BIOS is built |
| `sw/litex/milan_soc.py:2674, 2777-2781, 2808-2809` | `ctrl_firmware` parameter; under `ctrl_mailbox` no BIOS ROM or SRAM (`integrated_rom_size=0`, `integrated_sram_size=0`), then `add_ctrl_memory` right after `SoCCore.__init__` |
| `sw/litex/milan_soc.py:3683` | `--ctrl-firmware` |
| `sw/litex/milan_soc.py:3887` | `--ctrl-mailbox` and `--ctrl-firmware` refused apart |
| `sw/litex/milan_soc.py:4027` | passed to `MilanSoC` |
| `sw/litex/milan_soc.py:4066` | the split build adds no `libmilan_baremetal` (no BIOS to link into) |
| `sw/litex/milan_soc.py:4188` | the split build's staging check, before any export |
| `sw/firmware/ctrl/plat/ctrl_split.ld` | New. The split link: reset entry first in `rom`, `.data` in `sram` loaded from `rom`, `.bss`, 8 KiB stack |
| `sw/firmware/ctrl/plat/ctrl_split_start.S` | New. The reset entry: stack, `.data` copy, `.bss` clear, `main` |
| `sw/firmware/ctrl/test/ctrl_srp_image.py:66, 92, 180` | `link()` extracted; `--layout split` links with the split script and reports the bank plan; the flat layout is unchanged (same four spans) |
| `sw/litex/test_ctrl_memory.py` | New. 33 checks (section 7) |
| `syn/ooc/ctrl_memory_ooc.py` | New. Emits both regions of each image as `CtrlMemory` builds them, and the OOC Vivado script |
| `scripts/run_litex_sims.sh:101` | `test_ctrl_memory` in the pinned inventory |
| `docs/design/SPLIT_CONTROL_MEMORY.md` | New. The split placement's memory contract, refusals, boot and diagnostics, fit |
| `docs/design/MARK_II_AREA_PLAN.md`, `docs/design/AREA_BUDGET.md` | Ledger rows measured (section 6) |
| `docs/testing/TESTING.md`, `docs/testing/CI_WORKFLOWS.md`, `docs/design/MAILBOX_SPLIT.md`, `docs/ARCHITECTURE_HW_SW_SPLIT.md`, `docs/litex/LITEX_SOC.md`, `docs/README.md`, `sw/firmware/ctrl/README.md` | Cross-references |

## 3. Memory map and instantiation

| Region | Origin | Size | Holds | Built from |
|---|---|---:|---|---|
| `rom` | `0x0000_0000` (CPU reset address) | 224 KiB | reset entry, `.text`, `.rodata`, initial bytes of `.data` | banks of `wishbone.SRAM`, read-only, initialised from the ELF |
| `sram` | `0x1000_0000` | 224 KiB | `.data`, `.bss`, 8 KiB stack | banks of `wishbone.SRAM`, writable, uninitialised |

- Each region spans the whole budget, so the CPU netlist does not depend on the image: both split exports elaborate the same `VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`.
- Banks: the need rounded up to 2,048 B granules; the granule count's binary digits, largest first; each bank aligned to its own size; the decode compares high address bits (`slave_sel[0] = adr[15:14] == 0`, ... in the export).
- Past the last bank the region answers `err` in one cycle and writes nothing.
- Split vs base `--ctrl-mailbox` export (1x1): `csr.csv` differs only in `memory_region,rom` (131,072 to 229,376) and `memory_region,sram` (8,192 to 229,376). No CSR, CSR bank, interrupt or constant changes. `soc.h` identical except its timestamp; `mem.h` differs in `ROM_SIZE`/`SRAM_SIZE`.
- Split exports: `software/bios/` is empty (no `bios.bin`); the gateware carries `rom_bank0..4.init` (1x1) / `rom_bank0..3.init` (8x8) and the identifier's `mem.init`; no `sram.init`.

## 4. Linked spans at the four points

Linked at the lane head by `ctrl_srp_image.py --with-aecp --layout split` (pinned RV32 SDK `riscv32-ilp32d--glibc--stable-2025.08-1`, `-DNDEBUG`, `--gc-sections`, 8,192 B stack). Bytes:

| Point | .text | .rodata | .data | .bss | stack | `rom` need | `sram` need | Sum | Flat span (unchanged) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface (shipping) | 83,020 | 11,950 | 56 | 37,252 | 8,192 | 95,032 | 45,520 | 140,552 | 140,400 |
| 1x1, two interfaces | 84,308 | 11,950 | 56 | 48,620 | 8,192 | 96,320 | 56,880 | 153,200 | 153,056 |
| 8x8, one interface | 83,068 | 25,158 | 448 | 77,428 | 8,192 | 108,680 | 86,080 | 194,760 | 194,224 |
| 8x8, two interfaces (largest) | 84,444 | 25,158 | 448 | 103,556 | 8,192 | 110,056 | 112,208 | 222,264 | 221,728 |

- The split need exceeds the flat span by the reset entry (88 B of `.text`), the second copy of `.data` (56 / 448 B) and alignment (8 / 0 B).
- Inside the spans: descriptor image `aecp_entity_image` 7,512 / 19,520 B (rodata); `nvm_stage` 3,344 / 13,264 B (bss), equal to `ctrl_memory.stage_bytes` for the shape; lwSRP pool `image_arena` 9,920 / 19,840 / 24,032 / 48,064 B (bss), counted once.
- The largest point uses 222,264 of 229,376 bytes (224 KiB), and its banks 54.5 of 56 RAMB36: 1.5 RAMB36 (6 KiB) of headroom.

## 5. Primitive mapping, before and after

**After** (out of context, `syn/ooc/ctrl_memory_ooc.py`, Vivado 2026.1, `xc7a100t-fgg484-2`, `-mode out_of_context -directive AreaOptimized_high`, `Synth 8-4445` promoted to an error, every ROM `$readmem` read successfully; Vivado rc 0, run 2026-10-11 03:28 to its release under the exclusive lock). Per region:

| Top | Banks, bytes | Planned RAMB36 / RAMB18 | As mapped RAMB36 / RAMB18 | LUT | FF | LUTRAM |
|---|---|---:|---:|---:|---:|---:|
| `s1i1_rom` | 64K+16K+8K+4K+2K | 23 / 1 | 22 / 1 | 120 | 27 | 0 |
| `s1i1_sram` | 32K+8K+4K+2K | 11 / 1 | 11 / 1 | 92 | 5 | 0 |
| `s1i2_rom` | 64K+32K | 24 / 0 | 23 / 1 | 36 | 3 | 0 |
| `s1i2_sram` | 32K+16K+8K | 14 / 0 | 14 / 0 | 53 | 4 | 0 |
| `s8i1_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 217 | 28 | 0 |
| `s8i1_sram` | 64K+16K+4K+2K | 21 / 1 | 21 / 1 | 90 | 5 | 0 |
| `s8i2_rom` | 64K+32K+8K+4K | 27 / 0 | 25 / 1 | 231 | 34 | 0 |
| `s8i2_sram` | 64K+32K+8K+4K+2K | 27 / 1 | 27 / 1 | 97 | 6 | 0 |

Per point:

| Point | Linked need, B | Allocated bytes (banks) | Used | Planned tiles | As mapped RAMB36 / RAMB18 | As mapped tiles | LUT / FF | Byte floor (flat span / 4,096, up) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, one interface | 140,552 | 143,360 | 98.0% | 35.0 | 33 / 2 | **34.0** | 212 / 32 | 35 |
| 1x1, two interfaces | 153,200 | 155,648 | 98.4% | 38.0 | 37 / 1 | **37.5** | 89 / 7 | 38 |
| 8x8, one interface | 194,760 | 198,656 | 98.0% | 48.5 | 46 / 2 | **47.0** | 307 / 33 | 48 |
| 8x8, two interfaces | 222,264 | 223,232 | 99.6% | 54.5 | 52 / 2 | **53.0** | 328 / 40 | 55 |

- `sram` maps exactly as planned. Its LUTs are the bank decode and the read multiplexer.
- `rom` maps below plan for two reasons. Vivado trims a bit column constant across a bank (`16384x31` becomes 15 RAMB36 and one RAMB18). It also maps a small or sparse bank into logic: the 512-word bank at s1i1 (77 LUT6) and the 1,024-word bank at s8i1/s8i2, absent from the block-RAM mapping report (`util/*.rpt`, `map.vivado.log`).
- Most ROM LUTs come from that bank: 231 at the largest point. LiteX's memory emitter writes no `ROM_STYLE`, so this round reports Vivado's default. Forcing block RAM would cost at most the planned-minus-mapped difference, 1.0 / 0.5 / 1.5 / 1.5 tiles, and save most of those LUTs; M8a-2's route weighs it.

**Before:**

| Configuration | RAMB36 | RAMB18 | Source |
|---|---:|---:|---|
| All-fabric (and base `--ctrl-mailbox`) BIOS ROM, 13,279 x 32 | 16 | 0 | route census at `e8454e27` (round 1) |
| BIOS SRAM, 2,048 x 32 | 2 | 0 | same |
| Identifier memory (stays in both placements) | 0 | 1 | same |
| One LiteX `wishbone.SRAM` of the largest image's whole span (221,728 B) | 64 | 0 | round 1 OOC mapping |
| ROM + RAM, one `wishbone.SRAM` each, largest image | 64 | 0 | round 1 OOC mapping |

In the split, the BIOS ROM and SRAM are not built (-18 RAMB36), and the firmware takes 52 RAMB36 + 2 RAMB18 at the largest point.

## 6. Ledger rows, measured

Recorded in `docs/design/MARK_II_AREA_PLAN.md` (Firmware and block RAM ledger) and mirrored in `docs/design/AREA_BUDGET.md`:

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a-1: BIOS ROM and SRAM not built in the split, measured at `e8454e27` | -18 | 0 | -18 | 69 |
| M8a-1: firmware allocation as mapped, 8x8 with two interfaces | +52 | +2 | +53 | 122 |
| M2 maximum additional allocation | +2 | 0 | +2 | 124 |
| Conditional release of remaining wrapper storage, split only | -10 | -2 | -11 | 113 |

- `87.5 - 6.5 + 6 - 18 + 53 + 2 = 124`; after the release, 113: 8.5 below 121.5, reserve untouched.
- With every bank in block RAM (the plan bound 54.5): 125.5 and 114.5.
- At the shipping 1x1 with one interface (34.0): 105 and 94.
- The census's extra RAMB18 is the 49-byte identifier memory, which stays; the estimate row's -18.5 becomes -18.
- Keeping the BIOS memories would add 18: 142 and 131.

## 7. Planted controls, and the defect each test catches

**The three controls the assignment names, through the real SoC build** (`milan_soc.py` shipping export plus `--ctrl-mailbox --ctrl-firmware`, each refused before any export; logs in `evidence-m81/`):

| Control | Plant | Result |
|---|---|---|
| Allocation over budget | the 8x8 two-interface image linked from a scratch copy of the control tree whose `ctrl_split.ld` reserves a 16 KiB stack | rc 1, `allocation over budget: 56.5 RAMB36 (rom 110056 bytes in 110592, sram 120400 bytes in 120832) exceeds the 56-RAMB36 budget`; the fixture refuses the same image with the same words (rc 2) |
| Memory-map overlap | the 1x1 image linked from a copy whose `ctrl_split.ld` places `.bss` at `ADDR(.data)`; GNU ld accepts it | rc 1, `memory-map overlap: .bss at 0x10000000 lies inside .data [0x10000000, 0x10000038) (addresses)` |
| Staging buffer for another shape | the good 1x1 one-interface image in an 8x8 build | rc 1, `staging buffer: nvm_stage is 3344 bytes; the endstation_ax7101_8x8 shape stages 13264` |

Also refused (rc 2, by argparse): `--ctrl-mailbox` without `--ctrl-firmware`, and `--ctrl-firmware` without `--ctrl-mailbox`.

**`sw/litex/test_ctrl_memory.py`** (33 checks, RESULT: PASS; in `scripts/run_litex_sims.sh`):

| Arm | What it checks | Planted defect it catches |
|---|---|---|
| banks | 840 needs up to past the budget against an independent oracle (ceil(need/2,048) and its binary digits); zero need; RAMB18 counted half | any bank rounding or ordering change (the `banks smallest first` mutant turns 4 checks red) |
| checks | an ELF written by an independent writer: needs, `rom` contents at their load addresses, stage accepted | `the map check off` (5 red), `the budget check off` (1 red), `the staging check off` (2 red) |
| controls | over budget (215,000 B of .bss, 58 RAMB36, each region inside its own); overlap (.bss over .data; `sram` moved into `rom`); staging both ways (1x1 image vs 8x8 stage, 8x8 image vs 1x1 stage); entry at 0x100; .data's initial bytes in `sram`; a section at `0x4000_0000` | each must be refused by its named check |
| simulation | the real `milan_soc.CtrlMemory` in migen: `rom` reads its image at the first, second and last word of each of 3 banks; a write to `rom` changes nothing; `sram` byte lanes at every bank edge; past the last bank `err` at once in both regions; a hole write lands in no bank (each bank's aliasing cell read back) | `banks smallest first` (misaligned decode), `the hole answers nothing` (no `err`: 2 red), `a writable rom` (1 red) |
| link | a probe linked by the real `ctrl_split.ld` behind `ctrl_split_start.S` with the pinned SDK: entry 0 is `auipc sp`; `.data` runs in `sram` and its 7 loads from `rom`; the stack tops the `sram` need; `nvm_stage` passes | link-script plants: `.data` without `AT > rom` (refused `memory map`), `ENTRY(main)` (refused `reset entry`) |

Each mutant is a monkeypatch of the code under test for one arm; the arm must report at least one failure.

## 8. Boot console and diagnostics; DDR3 at this base

The split image loses: the LiteX BIOS and its console (banner, memory, flash, SDRAM and boot commands); the BIOS DDR3 initialisation (`sdram_init`); the shipping firmware's UART commands (`libmilan_baremetal` is not linked). It keeps the UART, `timer0`, `ctrl` (reset, scratch, bus errors), the identifier memory, the `ppmem` observer and every Milan CSR. Any console there is the control firmware's (F-INT PR 2). The all-fabric image keeps its BIOS (section 9).

DDR3 stays instantiated under `--ctrl-mailbox` at this base, because `KL_pp_shadow` (unconditional at `hdl/milan/milan_datapath.sv:8003`) and its three processor memory masters still reach the window in `main_ram`. With no BIOS the DFI never makes the 1 to 0 to 1 hand-back that `pp_mem_gate` (`sw/litex/milan_soc.py:2255`) waits for, so those masters stay refused (they answer errors, as before training). Removing DDR3 belongs with the wrapper's removal (F-INT PR 2) and is measured by M8a-2's route.

## 9. All-fabric default: digest-identical

Both AX7101 shipping configs exported (recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, no `--build`) with the base `milan_soc.py` (blob of `e8454e27`, swapped in and restored) and with the head. Normalization, and nothing else: LiteX timestamp lines, the export's own directory, the Verilog banner's Date line and LiteX's comment-only hierarchy tree.

| Config | Files compared | Differ | Normalized SHA-256 of `alinx_ax7101.v` |
|---|---:|---:|---|
| `ax7101` (1x1 TDM8) | 22 | 0 | `40e5304ae1fea35a02e5487f1096ed3c3bc4cdfa0732cd46e5332ce796586602` (base = head) |
| `ax8x8` | 22 | 0 | `fea8757e5546fa793dd76ac08800630fde4383ac8a289313f60b2b571b580e16` (base = head) |

The 22 files include the top `.v`, `.tcl`, `.xdc`, every `.init` (the BIOS ROM image among them), `bios.bin`, `csr.csv`, `csr.json`, the generated headers and `regions.ld`, the AEM image and manifest and `flashboot_layout.json`. Tables: `evidence-m81/digest-ax7101.txt`, `digest-ax8x8.txt`.

## 10. All-fabric image without DDR3 (measurement only)

Unchanged from round 1 (`stop-round/HANDOFF-stop.md` section 6): DDR3 holds only the processor window. Compacted, it is 14,792 B (4 RAMB36) at 1x1 and 46,640 B (12 RAMB36) at 8x8. Dropping DDR3 there would also need a compacted window and its constants, an on-chip memory on the CPU's DMA bus for the three processor masters, the removal of LiteDRAM, the PHY, `pp_mem_gate`'s DFI hold and the BIOS SDRAM init, and a pinned `spiflash` CSR location. Not done; the default flip decides it.

## 11. Gate table

Heads: `c20ed894` (first commit), `94190c36` (docstrings), `a475ab5a` (docs), `5d532e9d` (final, one doc line). Every gate unpiped, rc recorded (`evidence-m81/gates-*`).

| # | Gate | Head | rc | Result |
|---:|---|---|---:|---|
| 1 | `sw/litex/test_ctrl_memory.py` | `a475ab5a` | 0 | 33 checks, RESULT: PASS (link arm with the pinned SDK) |
| 2 | `scripts/run_litex_sims.sh --selftest` | `a475ab5a` | 0 | PASS |
| 3 | `scripts/run_litex_sims.sh <logs>` (pinned Verilator 5.050 on PATH) | `a475ab5a` | 0 | 6 of 6 PASS, 0 skipped |
| 4 | `ctrl_memory.py plan` on CPython 3.12.3 (largest image, `--stage-bytes 13264`) | `a475ab5a` | 0 | 54.5 planned |
| 5 | `check_py_idiom.py` and `--selftest` (CPython 3.12.3) | `a475ab5a` | 0, 0 | at ratchet (`c20ed894` was rc 1: two nested helpers without docstrings; fixed in `94190c36`) |
| 6 | `check_hygiene.py --check` and `--selftest`; `check_todo_ownership.py`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check` | `a475ab5a` | 0 each | PASS |
| 7 | `docs_check.py`; `check_em_dash.py --base e8454e27`; `gen_toc.py --verify-anchors`, `--check`; `check_doc_paths.py`; `check_doc_style.py`; `ci_events.py --check` | `5d532e9d` | 0 each | PASS (`a475ab5a`: `docs_check.py` rc 1, process wording, fixed in `5d532e9d`) |
| 8 | `gen_toc.py --selftest`; `check_doc_style.py --selftest`; `ci_events.py --selftest` | `a475ab5a` | 0 each | PASS |
| 9 | `sw/builder/test_builder.py --require-elaboration --require-rv32` | `c20ed894` and `a475ab5a` (the tree reached `5d532e9d`, one doc line, during the run) | 0, 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11: the bench build tree for its calibration is not on this host; recorded reason) |
| 10 | `check_soc_sources.py` and `--selftest`; `sw/litex/iob_pack_selftest.py` | `c20ed894` | 0 each | PASS |
| 11 | `check_sweep_shape.py --self-test`; `check_deploy_shape.py --self-test`; `check_entity_shape.py --self-test` | `c20ed894` | 0 each | PASS |
| 12 | `syn/ooc`: `dp_srcs.py --selftest`, `ooc_tcl_selftest.py`, `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `pp_resource_gate.py --selftest`, `pp_resource_gate_mutants.py`, `pp_resource_gate.py check-baseline` | `c20ed894` | 0 | PASS |
| 13 | `ctrl_image_selftest.py --require-rv32` | `c20ed894` | 0 | 33 checks PASS |
| 14 | `test_ctrl_firmware.py --require-rv32 --self-test --jobs 4` | `c20ed894` | 0 | `test_ctrl_firmware: PASS` |
| 15 | `scripts/run_all_suites.sh <logs>` (VERILATOR_JOBS=2, -j8) | `94190c36` | 0 | 61 of 61 suites, 2,185,848 checks, 0 failures; 4 declared `tsn_fuzz` skips (tsn-gen absent). Two earlier attempts (rc 2) aborted in the preflight's hard-HUP control because they ran under `nohup`; relaunched with `setsid` only |
| 16 | `syn/yosys/run.sh` | `94190c36` | 0 | 58 of 58 tops PASS; TAP-PURITY PASS |
| 17 | Fixture, four points, split and flat (`fit_final.sh`) | `94190c36` | 0 (12 runs) | flat spans unchanged; split ELFs byte-identical to the mapped ones |
| 18 | Default exports, base vs head, both AX7101 configs (section 9) | head `milan_soc.py` = `c20ed894` blob | 0 | 22 files each, 0 differ |
| 19 | Split exports, both configs (`--ctrl-mailbox --ctrl-firmware`) | same | 0 | elaborate; no BIOS; one CPU netlist |
| 20 | Planted controls through the SoC build (section 7) | same | 1 (expected) | each refused by name |
| 21 | OOC mapping (Vivado, exclusive lock) | images of `94190c36` | 0 | section 5 |

The diff from `94190c36` to `5d532e9d` touches documentation only (`docs/`, `sw/firmware/ctrl/README.md`), which neither the suites, Yosys nor the fixture read. The diff from `c20ed894` to `94190c36` adds two docstrings.

## 12. Not in this round, and open risks

- M8a-2: the split-image simulation boot to the control application's ready state, the service checks and the integrated route (LUT, FF, RAMB deltas against M0s's split figure, WNS) wait for F-INT PR 2.
- The image linked here is the size fixture in the split layout. Its reset entry is exercised by the linked probe's layout checks, not by a CPU simulation.
- The bank decode and its data multiplexer sit on the CPU's bus path; their timing is measured only by M8a-2's route.
- Headroom at the largest point is 1.5 RAMB36 (6 KiB) under 56. Growth beyond that is refused by name.
- The split build needs its own VexiiRiscv netlist (`VexiiRiscvLitex_dd10544c3ff1037f8a13f4ce3a3dd432`), generated once for both shapes.
- DDR3 under `--ctrl-mailbox` at this base is instantiated and untrained (section 8).
- Worktree leftovers, none committed: the export recipe's three scratch symlinks (`sw/builder/out`, untracked; `configs/generated/ltn_rom.hex` and `ucode.hex`, ignored) point into the scratch work directory, and the gates' ignored build outputs (`tb/verilator/*/obj_*`, `__pycache__`, `.run_all_suites.lock`) remain. Removing them was declined by the session's permissions; `git status` shows only `?? sw/builder/out`.

## 13. Reproduction

Environment: the pinned RV32 SDK (`scripts/ci_rv32_sdk.py --verify-only`), the LiteX stack of `sw/litex/litex_pins.txt` with `sw/litex/patches/`, Vivado 2026.1, PyYAML on the host Python. Runtime archives as in round 1 (`stop-round/HANDOFF-stop.md` section 8).

```sh
python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml \
  --interfaces 2 --with-aecp --layout split --output "$OUT" \
  --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a"
python3 sw/litex/ctrl_memory.py plan "$OUT/ctrl_app.elf" --stage-bytes 13264
python3 syn/ooc/ctrl_memory_ooc.py "$MAP" s8i2="$OUT/ctrl_app.elf"
cd "$MAP"
vivado -mode batch -nojournal -source ctrl_memory_ooc.tcl
python3 sw/litex/test_ctrl_memory.py
```

Default digest proof: the recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (export without `--build`), once with `e8454e27`'s `sw/litex/milan_soc.py` and once with the head's, compared by `evidence-m81/digest.py`. Split export: the same argv plus `--ctrl-mailbox --ctrl-firmware <elf>` (`evidence-m81/split-*-argv.json`). Scripts used: `evidence-m81/export.py`, `fit_final.sh`, `run_map.sh`, `gates_*.sh`.

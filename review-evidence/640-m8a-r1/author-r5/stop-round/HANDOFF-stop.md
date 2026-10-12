# HANDOFF: lane M8a for #640 (on-chip control memory for the split placement)

Executor [A594]. Reviewers [R606] (internal), [R607] (external).
Branch `640-m8a` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100371426
TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6100426002
STOP: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101473717

## Status

**STOP.** Lane head = base `e8454e2751d05b02ee8e5a571857589ab358ab86`. No commit, no tree change (`git status` clean before and after every run).

The assignment's own STOP condition fires: "A shape that does not fit is a STOP with the table."

- The largest supported shape at two interfaces links to a 221,728 B firmware span.
- 50 RAMB36 hold at most 204,800 B of byte-addressed storage (4,096 B each). The span is 16,928 B over that ceiling before any boot code, and needs at least 55 RAMB36.
- **As mapped** (LiteX's own `wishbone.SRAM`, Vivado synthesis at the shipping part and directive) it takes **64 RAMB36**, unified or split into ROM and RAM. Vivado's default inference rounds each memory to a power-of-two depth: a 204,800 B memory, the full 50-tile ceiling, itself maps to 64 RAMB36.
- As mapped, the 8x8 one-interface point also needs 64 RAMB36. It fits only at the 48-tile floor, which needs a 1K x 32-per-tile decomposition that default inference does not produce.
- The shipping 1x1 point fits as mapped at 48 RAMB36 (ROM 32 + RAM 16).

Two prerequisites the service and route proofs need are also absent at this base (section 1).
Nothing was implemented, so no all-fabric digest can change, and no route was run.

## Contents

1. Prerequisites at the base
2. Memory fit (the STOP table), floor and as mapped
3. BIOS ROM and SRAM reuse at the checkpoint
4. Ledger reconciliation (224 KB / 50 tiles)
5. Five largest static consumers and reduction options
6. All-fabric image without DDR3 (measurement only, as ruled)
7. Decisions needed
8. Reproduction
9. Gate table
10. Changes, tests, primitive mapping and route (none: STOP)

## 1. Prerequisites at the base

| Proof the assignment asks for | What it needs | State at `e8454e27` | Evidence |
|---|---|---|---|
| Split placement selected by its existing switch | A build in which firmware owns ADP, ACMP, MAAP, SRP (and AECP for the full split) | `--ctrl-mailbox` adds an idle mailbox only; the wrapper stays | `hdl/milan/milan_datapath.sv:8003` instantiates `KL_pp_shadow` unconditionally; `sw/litex/milan_soc.py:2548-2553` hold the mailbox's datapath ports idle |
| "A LiteX simulation boot of the split image to the control application's ready state" | An image that boots the control application (`sw/firmware/ctrl/app/ctrl_app.c`) | No SoC build compiles or links it | `sw/litex/milan_soc.py:3990-3993` links only `libmilan_baremetal`; `sw/firmware/ctrl/README.md:352-353` and `sw/firmware/ctrl/aecp/README.md:179-181`: the linked images are size fixtures, not board images |
| Route "through the M0s recipe, against M0s's split figure" | An M0s `f0-f4` or `full-split` route | None exists; M0s step 1 stopped for this prerequisite | `docs/design/MARK_II_AREA_PLAN.md:644-648` ("Not measured"); M0s STOP https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6087021702 |
| The same route's census | `f0-f4` requires ADP, both ACMP engines, SRP and both MAAP absent | A `--ctrl-mailbox` export keeps them, so the recipe errors after synthesis by design | `syn/ooc/pp_placement.py:41-48`, `:121-123` |

The build switch that removes the wrapper and connects the datapath is F-INT PR 2 (#665 ruling 6088423771: "PR 2 (after F5 merges): the build switch, the two-placement datapath simulation ... both images, the gates and the size"). PR 1 (#704) is open; PR 2 is not assigned.

`check_nvm_capture.py` grades the shipping firmware's `nvm_capture()` (`tb/verilator/nvm_capture_cpu/README.md`). In the split, the saved state belongs to the F1 store inside the control firmware, so that bench measures the all-fabric capture path, not the split's.

## 2. Memory fit (the STOP table), floor and as mapped

The firmware was linked at this base with the repository's own fixture, `sw/firmware/ctrl/test/ctrl_srp_image.py --with-aecp`. That is the full F0-F5/F1 composition, built with the pinned RV32 SDK (`riscv32-ilp32d--glibc--stable-2025.08-1`, verified), `-DNDEBUG`, `--gc-sections` and an 8,192-byte stack reservation.
The figures equal F5's published spans (https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6086832557: "140400 / 153056 / 194224 / 221728 bytes"), and a second run in this session reproduced them byte for byte.

The span already contains:

- the descriptor image: `aecp_entity_image` is 7,512 B at 1x1 and 19,520 B at 8x8 (rodata). Its CRC32 equals the fabric's own `aem_desc.bin` (`5ba355eb`, `2104c2d3`; section 6);
- the shape-sized stage: `nvm_stage` is 3,344 B and 13,264 B (bss);
- the lwSRP pool `image_arena`, in bss, counted once.

| Point | text | rodata | data | bss | stack | Linked span, B | Floor RAMB36 at 4,096 B | As mapped, ROM + RAM | As mapped, unified | vs 50 RAMB36 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1x1, one interface (shipping) | 82,932 | 11,950 | 56 | 37,252 | 8,192 | 140,400 | 35 | 32 + 16 = **48** | 64 | fits as ROM + RAM, 2 spare |
| 1x1, two interfaces | 84,220 | 11,950 | 56 | 48,620 | 8,192 | 153,056 | 38 | 32 + 16 = **48** | 64 | fits as ROM + RAM, 2 spare |
| 8x8, one interface | 82,980 | 25,158 | 448 | 77,428 | 8,192 | 194,224 | 48 | 32 + 32 = **64** | 64 | **over as mapped**; fits only at the floor |
| **8x8, two interfaces (largest)** | 84,356 | 25,158 | 448 | 103,556 | 8,192 | **221,728** | **55** | 32 + 32 = **64** | **64** | **over: 16,928 B past the 50-tile ceiling, 14 tiles as mapped** |

"Floor" counts 4,096 usable bytes per RAMB36: 32 data bits per word, because the 4 parity bits per word are not byte-addressable. It counts no boot code: the fixture has no reset entry.

### As mapped (Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high`, out of context)

Each memory is LiteX's own `wishbone.SRAM`, emitted by LiteX (`litex.gen.fhdl.verilog.convert`) and sized from the linked ELF (`evidence/gen_mem.py`).

- `rom_*` is read-only and holds the load image (.text, .rodata, .data), as LiteX's auto-sized ROM does. It is initialised with the real bytes from `objcopy -O binary`; Vivado reports `Synth 8-3876 $readmem data file ... read successfully` for all four.
- `ram_*` holds .data, .bss and the stack.
- `uni_*` is one writable memory holding the whole linked span.
- `cap50` is 50 x 4,096 B, the most a 50-RAMB36 allocation can expose.

Script `evidence/map.tcl`; results in `evidence/map-default.tsv`; Vivado exit 0.

| Memory | Bytes | Words x 32 | RAMB36 | RAMB18 | LUT | FF | Allocated bytes (4,096 per RAMB36) | Used / allocated |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cap50` | 204,800 | 51,200 | **64** | 0 | 29 | 1 | 262,144 | 78.1% |
| `rom_s1i1` | 94,944 | 23,736 | 32 | 0 | 1 | 1 | 131,072 | 72.4% |
| `ram_s1i1` | 45,500 | 11,375 | 16 | 0 | 5 | 1 | 65,536 | 69.4% |
| `rom_s1i2` | 96,232 | 24,058 | 32 | 0 | 1 | 1 | 131,072 | 73.4% |
| `ram_s1i2` | 56,868 | 14,217 | 16 | 0 | 5 | 1 | 65,536 | 86.8% |
| `rom_s8i1` | 108,592 | 27,148 | 32 | 0 | 1 | 1 | 131,072 | 82.8% |
| `ram_s8i1` | 86,068 | 21,517 | 32 | 0 | 5 | 1 | 131,072 | 65.7% |
| `rom_s8i2` | 109,968 | 27,492 | 32 | 0 | 1 | 1 | 131,072 | 83.9% |
| `ram_s8i2` | 112,196 | 28,049 | 32 | 0 | 5 | 1 | 131,072 | 85.6% |
| `uni_s1i1` | 140,400 | 35,100 | 64 | 0 | 29 | 1 | 262,144 | 53.6% |
| `uni_s1i2` | 153,056 | 38,264 | 64 | 0 | 29 | 1 | 262,144 | 58.4% |
| `uni_s8i1` | 194,224 | 48,556 | 64 | 0 | 29 | 1 | 262,144 | 74.1% |
| `uni_s8i2` | 221,728 | 55,432 | 64 | 0 | 29 | 1 | 262,144 | 84.6% |

Vivado's block-RAM mapping report gives the shape: `cap50 | mem_reg | 50 K x 32 ... | 0 | 64` and `uni_s8i2 | mem_reg | 54 K x 32 ... | 0 | 64`.
Every count equals 4,096 B x the next power-of-two word depth / 1,024. The base image's BIOS ROM follows the same rule (13,279 words -> 16 RAMB36, section 3).
The ROM + RAM split duplicates .data (56 / 448 B) in both memories, which changes no count.

Reaching the floor needs a decomposition into 1K x 32 tiles with an address decode, either written explicitly or requested from synthesis. A `ram_decomp = "power"` variant of the same thirteen memories was prepared but not run (section 9, row 11), so whether that attribute reaches the floor is unmeasured. Even at the floor, the largest shape needs 55.

## 3. BIOS ROM and SRAM reuse at the checkpoint

Source: the routed base image of `e8454e27` measured by sibling lane M2. Its checkout `HEAD` = `e8454e2751d0...`, clean apart from the recipe's `sw/builder/out` link, and its gate `check --endpoint route-1x1` passed.
Placed-cell census `baseline_cells.tsv` (8,301,796 B, sha256 `44dab163382b844407b0447593190b44bef051f5d1214dc88532879d49175fff`), RAMB cells outside `milan_datapath`:

| Memory | Emitted depth | Content | Mapped | Reusable for firmware |
|---|---|---|---|---|
| `rom` (BIOS with the shipping firmware linked in) | 13,279 x 32 (1x1); 13,319 x 32 (8x8 export) | 53,116 B (1x1), 53,276 B (8x8) | 16 RAMB36 (`rom_dat0_reg_0..15`) | yes |
| `sram` | 2,048 x 32 | 8,192 B | 2 RAMB36 (`sram_reg_0..1`) | yes |
| `mem` | 49 x 8 | the 49-byte SoC identifier string | 1 RAMB18 (`mem_dat0_reg`) | **no**: the identifier CSR stays in either placement |

**Confirmed reuse: 18 RAMB36, 0 RAMB18 = 18 tiles.** The ledger's 18 RAMB36 + 1 RAMB18 (18.5) counted the identifier memory.
The 16-RAMB36 ROM holds 53,116 B in 65,536 B of capacity: the power-of-two rounding measured in section 2.

If the control firmware is linked into the BIOS as the shipping firmware is today, the BIOS stays.

- The shipping ROM image is 53,116 B. The shipping firmware is 13.4 KB of it by the base `bios.elf` link map; its object is 15.6 KB before section collection (`milan_baremetal.o`: text 15,529, data 104).
- So the BIOS and its libraries are about 38-40 KB (9-10 tiles at the floor) of ROM, plus 2,160 B of BIOS bss.
- With the BIOS retained, both 8x8 points exceed 50 tiles. This is an estimate: 194,224 + ~38,000 + 2,160 is about 234,000 B at one interface, about 58 tiles at the floor. It counts the C runtime the BIOS and the fixture share twice, a few KB at most.

Without the BIOS, the firmware needs its own reset entry and runtime, which the fixture does not contain.

## 4. Ledger reconciliation (224 KB / 50 tiles)

| Item | Plan | Measured here |
|---|---|---|
| Firmware budget | 224 KB, "about 50 RAMB36 tiles" at 4.5 KB per tile | 50 RAMB36 expose 204,800 usable bytes at the floor; 224,000 B need 55 RAMB36 at 4,096 B (54.7). As mapped by default inference, a 204,800 B memory takes 64 RAMB36 |
| Largest shape, two interfaces | passes F5's 224,000-byte reading by 2,272 B | needs at least 55 RAMB36 bare (16,928 B over 50), 64 as mapped |
| BIOS ROM and SRAM reuse | -18 RAMB36, -1 RAMB18 (-18.5 tiles), historical | -18 RAMB36, 0 RAMB18 (-18 tiles) at `e8454e27` |
| Ledger line `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5` | 120.5 tiles | at the floor: `87.5 - 6.5 + 6 - 18 + 55 + 2 = 126` tiles; as mapped: `87.5 - 6.5 + 6 - 18 + 64 + 2 = 135` tiles. Both are over the 121.5 ceiling before the conditional 11-tile release (115 and 124 after it) |

The image's recorded RAM use (`route-1x1`, 74 RAMB36 + 27 RAMB18 = 87.5 tiles) is unchanged; nothing here is a routed figure.

## 5. Five largest static consumers and reduction options

At 8x8, two interfaces (bss unless marked):

| Object | Bytes | What it is | Reduction option (not implemented) |
|---|---:|---|---|
| `image_arena` | 48,064 | lwSRP attribute pool, `SRP_POOL_ARENA_BYTES` (24,032 per interface) | size the pool from a measured high-water mark under the entity's attribute bound instead of the worst case |
| `aecp_entity_image` (rodata) | 19,520 | the generated AEM descriptor image | serve READ_DESCRIPTOR from the image in SPI flash (memory-mapped LiteSPI, 25 MHz SCK) within the 240 ms response timeout |
| `nvm_stage` | 13,264 | the one container-sized saved-state stage (F1) | already shape-sized and single; share it with another transient buffer only by ownership proof |
| `image_values` | 11,753 | AECP descriptor value store (`AECP_ENTITY_VALUE_BYTES`) | narrow per-field storage to the entity model's used widths |
| `image_app` | 9,640 | the composed application (loop, ACMP state, MAAP, ADP) | ACMP's state is sized at the 16-sink/16-source/4-interface maxima; size it from the shape |

## 6. All-fabric image without DDR3 (measurement only, as ruled)

The shipping firmware already runs from the BIOS ROM and SRAM. DDR3 holds only the processor window (`sw/litex/milan_soc.py:2988-3041`), a 1 MiB reservation at `0x7F700000`:

| Object in DDR3 | 1x1 bytes | 8x8 bytes | Source |
|---|---:|---:|---|
| Descriptor image at `desc_base` | 7,512 | 19,520 | `aem_desc.bin`, through `build_desc_image`'s own calls (`evidence/desc_size.py`): CRC32 `5ba355eb` / `2104c2d3`, equal to the firmware's copy |
| AECP response buffer (last 4 KiB) | 592 | 592 | `milan_soc.py:3007-3013` |
| Saved-state live window (one 64 KiB block reserved) | 3,344 | 13,264 | container size, `nvm_stage` |
| Saved-state private stage (one 64 KiB block reserved) | 3,344 | 13,264 | container size |
| **Total, compacted** | **14,792** | **46,640** | |
| RAMB36 at the floor | 3.6 -> 4 | 11.4 -> 12 | |

What it would also need (not done):

- a compacted window replacing the 1 MiB `pp_mem` reservation: the `desc_base`/`resp_base` compile-time parameters, the `MILAN_NVM_*_BASE` firmware constants, the platform shape and the deploy manifest `aem_desc.json`;
- an on-chip memory on the CPU's DMA bus for the three 64-bit processor masters;
- removal of LiteDRAM, the A7DDRPHY, `pp_mem_gate`'s DFI hold and the BIOS SDRAM init;
- a pinned CSR location for `spiflash`, so that removing the `sdram` bank does not move it (`milan_soc.py:3301-3312` records that hazard).

Its LUT saving is the same unmeasured L11a figure.

Observation for a separate Issue (not acted on here): the comment at `sw/litex/milan_soc.py:3005-3006` says the largest descriptor image "is 23,216 bytes, at the 8x8 shape". At this base the 8x8 image is 19,520 B, so the comment is stale. Its collision argument still holds.

## 7. Decisions needed

1. **Memory fit (the STOP).** The largest shape at two interfaces needs at least 55 RAMB36 of firmware memory before boot code, and 64 as LiteX's memory maps today. Choose one or more:
   - raise the allocation (the ledger is then 126 tiles at the floor, 135 as mapped, before the conditional release);
   - reduce the firmware (section 5);
   - bound the largest shape's interface count.

   Whichever is chosen, reaching the floor also needs a 1K-x-32 decomposition, which LiteX's default inference does not produce.
2. **Boot organisation.** Keep the BIOS (about +10 tiles) or give the control firmware its own reset entry and runtime. The fixture measures neither.
3. **Sequencing.** The split-image boot, the M0s route and the split capture path need F-INT PR 2. M8a's memory instantiation can be written against `--ctrl-mailbox` now, but none of its service or route proofs can run until the split build exists.

## 8. Reproduction

```sh
python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only
python3 sw/firmware/ctrl/test/ctrl_image_runtime.py --picolibc "$PICOLIBC" \
  --compiler-rt "$COMPILER_RT" --litex-software "$LITEX_SOFTWARE" --output "$RUNTIME"
for shape in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  for ifs in 1 2; do
    python3 sw/firmware/ctrl/test/ctrl_srp_image.py --config "configs/$shape.yaml" \
      --interfaces "$ifs" --with-aecp --output "$FIT/img-$shape-if$ifs" \
      --libc "$RUNTIME/libc.a" --compiler-runtime "$RUNTIME/libcompiler_rt.a" \
      > "$FIT/img-$shape-if$ifs.log"
  done
done
```

`MILAN_RV32_CC` names the pinned SDK's `riscv32-linux-gcc` for the firmware link. For `ctrl_image_runtime.py` only, it names a wrapper that adds `-fno-stack-protector`, as F5's lane did: the SDK's compiler defaults to the stack protector, and `__umoddi3` otherwise references `__stack_chk_guard`, which no bare-metal runtime defines.
The firmware objects themselves already pass `-fno-stack-protector` (`sw/firmware/ctrl/test/ctrl_build.py:45`).
The runtime archives' bytes differ between runs (archive member metadata); the linked spans do not.

Mapping, with LiteX's `migen` and `litex` on `PYTHONPATH`:

```sh
python3 evidence/gen_mem.py "$FIT" "$MAP/v" "$SDK/bin/riscv32-linux-objcopy"
cd "$MAP/v"
vivado -mode batch -nojournal -source ../map.tcl -tclargs "cap50 rom_s1i1 ram_s1i1 rom_s1i2 ram_s1i2 rom_s8i1 ram_s8i1 rom_s8i2 ram_s8i2 uni_s1i1 uni_s1i2 uni_s8i1 uni_s8i2"
```

with `evidence/map.tcl` copied to `$MAP/map.tcl`; it writes `$MAP/map.tsv`.
Descriptor sizes: `python3 evidence/desc_size.py <repo> <builder-out>/<shape>/aem_overlay.json ...`.

## 9. Gate table

All at lane head `e8454e2751d05b02ee8e5a571857589ab358ab86`, worktree clean before and after, each run unpiped with its exit status recorded.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/ci_rv32_sdk.py --destination "$SDK" --verify-only` | 0 | `riscv32-ilp32d--glibc--stable-2025.08-1`, archive sha256 `d42680e9...`, gcc 14.3.0 |
| 2 | `python3 sw/firmware/ctrl/test/ctrl_image_runtime.py ...` | 0 | `libc.a` 5,542 B, `libcompiler_rt.a` 29,432 B |
| 3 | `ctrl_srp_image.py --config configs/endstation_ax7101_1x1_tdm8.yaml --interfaces 1 --with-aecp` | 0 | `ram_span` 140400 |
| 4 | same, `--interfaces 2` | 0 | `ram_span` 153056 |
| 5 | `ctrl_srp_image.py --config configs/endstation_ax7101_8x8.yaml --interfaces 1 --with-aecp` | 0 | `ram_span` 194224 |
| 6 | same, `--interfaces 2` | 0 | `ram_span` 221728 |
| 7 | `python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32` | 0 | `ctrl_image self-test: 33 checks PASS` |
| 8 | `python3 syn/ooc/pp_baseline.py --selftest` (runs the placement recipe controls of `pp_placement_selftest.py`) | 0 | `placement Tcl all-fabric / f0-f4 / full-split ... PASS`; `placement recipe: ... PASS`; `baseline export selftest ... PASS` |
| 9 | `python3 evidence/desc_size.py ...` (both shapes) | 0 | 7,512 B `5ba355eb`; 19,520 B `2104c2d3` |
| 10 | Vivado OOC mapping, 13 memories, default inference (`evidence/map.tcl`) under the exclusive lock | 0 | section 2 table; `evidence/map-default.tsv` |
| 11 | Vivado OOC mapping, the same 13 with `(* ram_decomp = "power" *)` | not run | queued under the exclusive lock behind other lanes' routes, cancelled before it acquired the lock; no result is claimed |

Row 11 is optional to the STOP: the floor column already bounds what any decomposition can reach, and 221,728 B exceeds 50 tiles at the floor.

Receipts (scratch, not copied): Vivado log `map.log` 346,142 B; the thirteen `util_*.rpt` and the run logs are listed by sha256 in `evidence/receipts.tsv`.

The fixtures' and recipe's gates are the only ones this STOP rests on. No tree file changed, so no Makefile, RTL, suite, builder or deploy gate is touched; none was run.

## 10. Changes, tests, primitive mapping and route (none: STOP)

- **Changes:** none. No file in the tree changed.
- **Tests and planted controls:** none were written or run. The assignment stops at a shape that does not fit, and the split build that the service, boot and route proofs need does not exist at this base. That includes the three named controls (allocation over budget, memory-map overlap, wrong-shape staging).
- **Primitive mapping before:** BIOS ROM 16 RAMB36, SRAM 2 RAMB36, identifier 1 RAMB18 (section 3). **After:** not implemented. The projected firmware memory is in section 2.
- **Resource and route before/after through the M0s recipe:** not run. M0s has no split figure to compare against (section 1), and no change exists to route.
- **All-fabric endpoint:** unchanged trivially, because no input changed.

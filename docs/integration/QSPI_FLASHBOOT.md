# QSPI flash-boot  -  skip the multi-minute serial upload

## Contents

- **[The device at a glance](#the-device-at-a-glance)** — The to-scale flash map, generated from the same `load_map()` that emits the kernel's `fixed-partitions` node — so map, device tree and picture cannot drift apart. The generator also re-runs the overlap/alignment check and prints the verdict *onto* the drawing, which is how a broken map becomes visible before flash time.
- **[Layout "full" — THE DEPLOYED TRUTH (2026-07-24, silicon-verified end-to-end)](#layout-full--the-deployed-truth-2026-07-24-silicon-verified-end-to-end)** — Start here. The current slot table, plus two traps that have each bitten twice: the `dtb` slot is a **decoy** — the kernel boots on the FDT embedded in OpenSBI — and LiteX CSR addresses shift whenever the gateware block set changes, so a stale DTB produces symptoms as oblique as a ptp4l tx-timestamp timeout. Ends with real boot timing: ~7 min cold to network-up, so probe windows need ≥ 8 min.
- **[Layout v3 — SUPERSEDED HISTORY (2026-07-12; offsets no longer deployed)](#layout-v3--superseded-history-2026-07-12-offsets-no-longer-deployed)** — Historical: these offsets are not what ships. Kept for the reasoning that is still true — why the kernel is flashed as `Image.xz` (there is no non-EFI self-extracting kernel on RISC-V), the xz stream rule the vendored decoder imposes, and the four cooperating pieces the whole feature is built from.
- **[The hard constraint: 16 MB flash vs 23 MB of images](#the-hard-constraint-16-mb-flash-vs-23-mb-of-images)** — Why there are two manifests at all: 16 MB of device against ~23 MB of images. Describes the older kernel-at-offset-0 arrangement, in which the bitstream is deliberately *not* in flash — read it against the deployed layout above, which now starts with the bitstream.
- **[How the boot works](#how-the-boot-works)** — The boot-method priority chain and what full vs partial each do. The reassuring part: every copy is CRC-checked from the FBI header, so an empty or half-written flash falls through to serialboot rather than bricking the boot.
- **[Usage](#usage)** — The four commands in order — apply the BIOS patch (re-run after every LiteX upgrade), build, flash, then the fast iteration loop that JTAG-loads gateware while the kernel stays in flash.
- **[Getting to zero-upload](#getting-to-zero-upload)** — The three steps that get a boot to upload nothing, and the size targets they have to hit. `flash-images` refuses an oversized image, so an un-slimmed kernel fails loudly instead of half-writing the layout.
- **[Caveats](#caveats)** — Six, and the first is the expensive one: `--coherent-dma` is mandatory and *not* implied by `--all-blocks` — without it RX skbs arrive all-zero and TX sends stale data the peer silently filters. The rest cover FBI endianness, flash addressing and why kernel-at-0 is safe with this loader.
- **[Validated](#validated)** — What was actually checked at the time, including the negative: the slot check correctly *rejects* a 14 MB kernel against the 8.5 MiB slot.
- **[2026-07-06: zero-upload ACHIEVED  -  the sizes that made "full" fit](#2026-07-06-zero-upload-achieved-----the-sizes-that-made-full-fit)** — Frozen record of the two rounds of slimming, with the before/after per lever. The kernel-config gotcha worth stealing: without `CONFIG_EXPERT=y` the VT/INPUT disables **silently fail**.
- **[Planned: boot-chain compression (BIOS-LZ4 kernel)  -  bitstream stays JTAG](#planned-boot-chain-compression-bios-lz4-kernel-----bitstream-stays-jtag)** — A proposal, not shipped. Argues the decompressor belongs in the LiteX BIOS rather than OpenSBI, prices the gain at ~3.4 MiB of freed flash, and records the decision that the bitstream stays JTAG-loaded even though the freed space would fit it.
- **[Field notes (2026-07-10 silicon session)](#field-notes-2026-07-10-silicon-session)** — Five things learned the hard way at the bench, including the one that looks like flaky hardware: the BIOS re-tunes the SPI divisor *upward* at boot, defeating the gateware clock cap, and marginal MB-scale reads showed up as one lucky boot in six. Also the manual `litex>` flashboot recovery and a scary-looking initramfs message that is benign.

## The device at a glance

![QSPI flash map](../diagrams/flash_layout.svg)

*What is at which offset, how much of the device each slot actually costs, and
which slots a reflash must never erase* — drawn **to scale**, and **generated**
by [`flash_layout.gen.py`](../diagrams/flash_layout.gen.py) from the one source
of truth (`FLASHBOOT_LAYOUT` + `FLASHBOOT_RESERVED` in `sw/litex/milan_soc.py`),
read through the very same `load_map()` that emits the kernel's
`fixed-partitions` node. The map, the device tree and this picture move
together or not at all. Regenerate with:

```
python3 docs/diagrams/flash_layout.gen.py docs/diagrams/flash_layout
rsvg-convert -w 1800 docs/diagrams/flash_layout.svg -o docs/diagrams/flash_layout.png
```

The generator also re-runs the map consistency check (overlap / erase-block
alignment / past-the-device) and prints the verdict on the drawing, so a broken
map is visible in the picture rather than only at flash time.

## Layout "full" — THE DEPLOYED TRUTH (2026-07-24, silicon-verified end-to-end)

The layout of record is the `--flashboot full` manifest baked into the
gateware BIOS (`flashboot_layout.json` in every build dir — ALWAYS read the
build's own copy; offsets below are the current AX/Arty builds'):

| slot      | offset      | budget    | measured (AX 07-24) | notes |
|-----------|-------------|-----------|---------------------|-------|
| bitstream | `0x00_0000` | 4 MiB     | 3.6 MiB (raw)       | AX: platform-pinned **SPIx4 / CONFIGRATE 50, UNCOMPRESSED** — cold-config silicon-proven (the x1/33/COMPRESS pin is the **Arty-only** override; the milan_soc.py comment says why). `openFPGALoader -f --verify`, NOT fbi-wrapped. |
| kernel    | `0x40_0000` | 3 MiB     | 2.52 MB             | Image.xz (`xz -9 --check=crc32`); BIOS xz_embedded decodes → DRAM |
| opensbi   | `0x70_0000` | 384 KiB   | 266,824 B           | fw_jump → 0x40F0_0000. **CARRIES THE KERNEL'S DTB (FW_FDT_PATH embed)** — see the decoy warning below |
| dtb       | `0x76_0000` | 128 KiB   | ~3 KB               | **A DECOY for the kernel**: the BIOS copies it, but the kernel boots on the *OpenSBI-embedded* FDT. Changing the DTB = rebuild opensbi (`fpga/boot/build_opensbi.sh`, always-clean rule) + flash the OPENSBI slot. Keep this slot in sync anyway (safety copy). |
| rootfs    | `0x78_0000` | **6.375 MiB** (was 8.5 MiB) | 8,898,244 B was the **2026-07-24** image, i.e. BEFORE the v4 shrink | rootfs.cpio + `xz -9 -e --check=crc32` **by hand** (NOT a buildroot target in this output tree: `rm images/rootfs.cpio*; make rootfs-cpio; xz …`) |

> **The budget column above is a snapshot; the picture is the source.** The v4
> map (2026-07-26) shrank `rootfs` from 8.5 MiB to `0x66_0000` = 6.375 MiB to
> make room for the `journal` and `user` slots, and the measured image in the
> "measured" column predates that change — an 8.49 MiB rootfs would no longer
> fit. `sw/litex/milan_soc.py` records 5.6 MiB for the current image, leaving
> ~0.775 MiB of slack. Read the live budget off the generated map above (or off
> the build's own `flashboot_layout.json`), and read the pre-flash size line
> `deploy.sh flash-images` prints before it writes anything.

All Linux images are FBI-wrapped (`python -m litex.soc.software.crcfbigen
<img> -f -l`) then written raw at their offsets
(`openFPGALoader -o <offset> --write-flash --file-type raw --verify`);
`deploy.sh flash-images` automates the set. `openFPGALoader --reset` pulses
PROGRAM_B = reboot from flash without a power cycle.

**Matched-image rule (the CSR-rot trap, bitten twice — 07-22 and 07-24):**
the kl-eth LiteX CSR block addresses (dma-ts, dma-pcm, …) are AUTO-ALLOCATED
and SHIFT whenever the gateware's block set changes (e.g. `--rx-queues 1`
dropped the RX1 queue CSRs and moved dma-ts 0x3100→0x308c, dma-pcm
0x3120→0x30ac). The DTB **must be regenerated from the build's `csr.csv`**
and re-embedded into opensbi with every gateware change that touches the
map — the symptom of a stale DTB is subtle (e.g. ptp4l "timed out while
polling for tx timestamp" while everything else works).

**Boot timing truth (07-24):** power-on → network-up ≈ **7 min** (FPGA
config and kernel are seconds; the rootfs init + S50milan devmem storm is
the bulk). Warm boots (link already negotiated) ≈ 2.5–3 min. **Reachability
probes need ≥ 8 min windows** — two false "cold-boot dead" verdicts were
probe timeouts.

## Layout v3 — SUPERSEDED HISTORY (2026-07-12; offsets no longer deployed)

The gateware lives in flash and the FPGA config-boots it (mode pins: Arty
JP1 -> QSPI, AX7101 boot switch -> QSPI); bitstreams are COMPRESSED (pinned:
COMPRESS + SPI x1 + 33 MHz configrate). The kernel is flashed as the kernel
build's own **Image.xz** (there is no non-EFI self-extracting kernel on
riscv — the config's self-extractor is EFI zboot, which our BIOS->OpenSBI
chain has no loader for; Image.xz is the artifact the kernel proposes for
bootloader decompression). The BIOS decompresses it with the vendored
xz_embedded decoder (patch 0003 + files/xz, 0BSD from linux lib/xz; 10.6 KB
of rv64 code; single-call mode — the destination buffer is the dictionary,
64 KB state arena; byte-identical decode host-proven on the real Image).

| slot      | offset     | budget   | measured | notes |
|-----------|------------|----------|----------|-------|
| bitstream | 0x00_0000  | 2.25 MiB | ~2.0-2.3 | raw config stream via `deploy.sh flash`; NOT fbi-wrapped |
| kernel    | 0x24_0000  | 3.5 MiB  | 2.52 MB  | Image.xz (xz -9 --check=crc32; deploy.sh auto-compresses a raw Image); BIOS stages @ +24 MB, decodes -> 0x4000_0000 |
| opensbi   | 0x5C_0000  | 384 KiB  | 261 KB   | fw_jump -> 0x40F0_0000 |
| dtb       | 0x62_0000  | 128 KiB  | ~10 KB   | -> 0x40EF_0000 |
| rootfs    | 0x64_0000  | 9.75 MiB | 5.6 MB   | CPIO-XZ -> 0x4100_0000 (4 MiB slack — no slimming pressure) |

xz stream rule: plain LZMA2, `--check=crc32` (or none) — the decoder builds
without CRC64/BCJ. The BIOS magic-sniffs the staged payload, so an
uncompressed Image keeps booting (transition-safe).

Rollout is atomic per board: flash the v3 bitstream AND the image set in one
session (a v3 BIOS with old-layout flash finds no kernel at 0x24_0000 and
vice versa). DRAM scratch during boot: staging at +24 MB, arena at +28 MB —
clear of kernel (8.1 MB @ +0), initrd (@ +16 MB), dtb/opensbi (@ ~+15 MB).
The pre-v3 sections below describe the kernel-at-0 layout.


Every boot of the fully-FPGA Linux SoC uploads four images over the 1.5 Mbaud LiteX UART  - 
the 14 MB kernel `Image`, the 8.7 MB `rootfs.cpio.gz`, OpenSBI and the DTB, ~23 MB total,
which takes **~4 minutes**. This is the "gain time" feature: stage the large, static images
in the board's QSPI flash so the BIOS copies them straight into DRAM (quad SPI, ~10 MB/s)
instead of trickling them over the wire.

It has three cooperating pieces plus a host boot-list, all opt-in behind
`milan_soc.py --with-spiflash` (included in `--all-blocks`):

| piece | where | what |
|-------|-------|------|
| **flash core** | `sw/litex/milan_soc.py`, `sw/litex/platforms/alinx_ax7101.py` | memory-maps the on-board flash; emits the `MILAN_FLASHBOOT_*` layout constants |
| **BIOS method** | `sw/litex/patches/0001-milan-linux-flashboot.patch` | `linux_flashboot` copies images flash→DRAM, boots (or pre-loads then defers to serialboot) |
| **flashing** | `sw/litex/deploy.sh flash-images` | wraps each image as a LiteX FBI and writes it at the compiled-in offset; refuses a `$DTB` whose `kl,dma-ether` windows mismatch the build’s `csr.csv` ([check_dtb_csr.py](../../sw/litex/check_dtb_csr.py), [TROUBLESHOOTING §20](../limitations/TROUBLESHOOTING.md)) |
| **host boot-list** | `the-private-test-repo/fpga/boot/boot_flashkernel.json` | serial upload of only the *non*-flashed images (partial mode) |

---

## The hard constraint: 16 MB flash vs 23 MB of images

The AX7101 flash is a **Micron N25Q128 = 128 Mbit = 16 MB** (confirmed from the Alinx repo,
`DATASHEET/QSPI FLASH/N25Q128.pdf`). The boot images total **~23 MB**:

| image | size | DRAM target |
|-------|------|-------------|
| kernel `Image` | ~14 MB | `0x4000_0000` |
| `rootfs.cpio.gz` | ~8.7 MB | `0x4100_0000` (initrd) |
| `opensbi.bin` (fw_jump) | ~0.26 MB | `0x40f0_0000` (**boot entry**, a0=hartid, a1=0) |
| `milan.dtb` | ~3 KB | `0x40ef_0000` |

So **not everything fits at once**. Two manifests (`--flashboot`):

* **`kernel` (default)  -  partial, works today.** Flash only the big, static 14 MB kernel.
  `linux_flashboot` pre-loads it to DRAM; serialboot then uploads only OpenSBI+dtb+rootfs
  (~9 MB). **~60 % faster** per boot, no image rebuild. The kernel + OpenSBI are the images
  that change *least*, so most iterations upload just the ~9 MB rest.
* **`full`  -  zero upload.** Flash every image; `linux_flashboot` boots OpenSBI directly with
  **no serial upload at all**. Fits once the kernel is slimmed to **≤ 8.5 MiB** with a
  cpio.xz rootfs ≤ 6.75 MiB — achieved 2026-07-06 with an 8.14 MB `-Os` kernel (see
  [Getting to zero-upload](#getting-to-zero-upload)); the deploy step refuses an oversized
  image rather than silently corrupt the layout.

Because the default kernel occupies flash offset 0, **the bitstream is *not* stored in flash**
in this layout  -  flash-boot builds are JTAG-`load`ed (`deploy.sh load`), which is the normal
iteration path anyway. (A bitstream + a 14 MB kernel cannot coexist in 16 MB.)

### Flash layout (`FLASHBOOT_LAYOUT` in `milan_soc.py`)

```
 offset      kernel manifest (default)        full manifest (slim kernel)
 0x00_0000   kernel  (≤ 16 MB)                kernel   (≤ 8.5 MiB)
 0x88_0000    -                                opensbi  (512 KB; fw_jump 261 KB + FBI)
 0x90_0000    -                                dtb      (256 KB)
 0x94_0000    -                                rootfs   (≤ 6.75 MiB → ends = 16 MiB)
```

The build writes `<build>/flashboot_layout.json` (the single source of truth); `deploy.sh
flash-images` reads it, so the gateware's compiled-in offsets and the flashing never drift.

---

## How the boot works

`define_boot_method(milan_flash, …, priority −10)` runs **before** serialboot (priority 0),
which stays as the fallback. The BIOS boot sequence tries methods in ascending priority:

```
 reset → BIOS → linux_flashboot (−10)  → serialboot (0) → …
                    │                        │
   copies flashed images DRAM←flash          uploads whatever linux_flashboot didn't,
                    │                         then jumps to the last json entry (OpenSBI)
        full? boot OpenSBI (no serial)
        partial? print + return  ─────────────┘
```

* **Full manifest:** `linux_flashboot` copies opensbi+dtb+kernel+rootfs, then
  `boot(0,0,0, 0x40f0_0000)`  -  the NaxRiscv `boot_helper` leaves `a0=hartid`, `a1=0`, exactly
  what the OpenSBI fw_jump expects (DTB is embedded via `FW_FDT_PATH`).
* **Partial manifest:** `linux_flashboot` copies only the kernel to `0x4000_0000`, prints a
  note and returns; serialboot then uploads OpenSBI+dtb+rootfs from `boot_flashkernel.json`
  (which omits `Image` and lists `opensbi.bin` **last**, so litex_term jumps there).

Each copy uses the BIOS's existing `copy_image_from_flash_to_ram`, which **CRC-checks** every
image (LiteX FBI = `[length][crc32][data]`, little-endian header). A CRC/length failure aborts
the copy and falls through to serialboot  -  an empty or mid-update flash **cannot brick the
boot**.

---

## Usage

### One-time: apply the BIOS patch

The `linux_flashboot` method lives in the LiteX BIOS source, shipped here as a patch:

```sh
sw/litex/patches/apply.sh        # idempotent; finds the LiteX tree from your Python env
```

Re-run it after any `pip install -U litex` (an upgrade resets the BIOS sources). Without it,
the `MILAN_FLASHBOOT_*` constants are inert and the build still works (serial boot only).

### Build a flash-boot bitstream

```sh
sw/litex/deploy.sh build            # --all-blocks already implies --with-spiflash --flashboot kernel
# or explicitly:
sw/litex/milan_soc.py --all-blocks --coherent-dma --milan-clk-freq 50e6 --with-spiflash --flashboot kernel --build
```

### Flash the kernel once (partial mode)

```sh
KERNEL=/path/to/images/Image  sw/litex/deploy.sh flash-images
```

`flash-images` reads the newest `flashboot_layout.json` (override `LAYOUT=`), wraps each
manifest image as an FBI (`crcfbigen -f -l`), size-checks it against its slot, and writes it
with `openFPGALoader -o <offset> --write-flash --file-type raw --verify`. Only the images in
the manifest need their env var (`KERNEL`/`OPENSBI`/`DTB`/`ROOTFS`); there are no
machine-specific defaults.

### Iterate (the fast loop)

```sh
sw/litex/deploy.sh load             # JTAG → SRAM (kernel stays in flash across reloads)
# then, in the-private-test-repo:
O=<buildroot-out> FLASH_KERNEL=1 fpga/boot/boot.sh   # uploads opensbi+dtb+rootfs only (~9 MB)
```

The kernel is already in flash; the BIOS pre-loads it and serialboot handles the rest.

---

## Getting to zero-upload

The 14 MB kernel was the blocker. Slim it below the 8.5 MiB slot (achieved: 8.14 MB,
see the 2026-07-06 section below) and switch the rootfs to cpio.xz, and the **full**
manifest fits  -  then a boot uploads *nothing*:

1. Trim the kernel `.config` (drop unused drivers/filesystems/debug; the Milan NIC needs only
   `kl-eth` + the litex UART/CLINT/PLIC). A lean RV64 buildroot kernel is ~4–6 MB.
2. Rebuild; confirm `Image` ≤ 8.5 MiB (the slot size) and the cpio.xz rootfs ≤ 6.75 MiB.
3. Build `--flashboot full`, flash all four images, boot with no serial step:
   ```sh
   sw/litex/milan_soc.py --all-blocks --coherent-dma --milan-clk-freq 50e6 --with-spiflash --flashboot full --build
   KERNEL=…/Image OPENSBI=…/opensbi.bin DTB=…/milan.dtb ROOTFS=…/rootfs.cpio.gz \
       sw/litex/deploy.sh flash-images
   sw/litex/deploy.sh load     # BIOS flash-boots directly; no boot.sh needed
   ```

`flash-images` errors out if the kernel (or rootfs) overflows its slot, so an un-slimmed
kernel fails loudly instead of half-writing.

---

## Caveats

* **`--coherent-dma` is mandatory and NOT implied by `--all-blocks`.** Without it the NIC's
  DMA masters bypass the NaxRiscv snooping `dma_bus`: RX data never becomes CPU-visible (the
  stack drops every frame  -  all-zero skbs) and TX reads stale skb data (garbage dst MAC that
  the peer NIC silently filters). Hardware-confirmed 2026-07-04; `deploy.sh` includes it.
* **No bitstream in flash (kernel layout).** The kernel sits at offset 0, so a power-cycle
  will not auto-configure the FPGA from flash  -  always JTAG-`load`. This is the normal dev
  flow. (`deploy.sh flash` writes a *bitstream* to offset 0 and is mutually exclusive with
  `flash-images` on 16 MB.)
* **Re-apply the patch after LiteX updates** (`apply.sh` is idempotent and errors clearly if
  LiteX has moved the patched lines  -  then refresh the `.patch`).
* **Endianness:** the FBI header is little-endian (`crcfbigen -l`), matching the BIOS's
  `MMPTR` reads on this RV64 core. `deploy.sh` uses `-l`; don't drop it.
* **Flash addressing:** the N25Q128 is 16 MB = 3-byte addressable, so the whole chip is
  reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ,
  so WP#/HOLD# are never left floating.
* **openFPGALoader offset 0** is only guarded on *Efinix* boards; the Xilinx SPI path (v1.1.1,
  verified) writes raw at any offset, so kernel-at-0 is fine here.

---

## Validated

* Gateware elaborates + generates `csr.json` (SPIFLASH region at `SPIFLASH_BASE`, litespi
  master CSRs) and emits the correct `MILAN_FLASHBOOT_*` constants for both manifests
  (`kernel`: kernel-only, no `COMPLETE`; `full`: all four + `COMPLETE`).
* The patched BIOS compiles; `linux_flashboot` and `milan_flash_boot_method` link into the
  boot-method section.
* `deploy.sh flash-images` wraps the real 14 MB `Image` into a 14 MB+8 B FBI, passes the
  slot check for the kernel manifest, and issues the correct `openFPGALoader` write; it
  correctly **rejects** the 14 MB kernel against the 8.5 MiB `full` slot.

See also [pipeline-telemetry.md](../fpga/pipeline-telemetry.md), [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md),
and [`sw/litex/patches/README.md`](../../sw/litex/patches/README.md).

---

## 2026-07-06: zero-upload ACHIEVED  -  the sizes that made "full" fit

The blockers fell in two rounds (fragment: `br2-external/board/milan_naxriscv/linux.fragment`):

| Item | Before | After | How |
|---|---|---|---|
| kernel `Image` | 11.9 MB | **8.14 MB** | `-Os` (CC_OPTIMIZE_FOR_SIZE, −25 % alone); SELinux/kexec off; `CONFIG_EXPERT=y` (without it the VT/INPUT disables **silently fail**  -  they need EXPERT); kallsyms off (~1 MB; oops decode moves offline via vmlinux); LOG_BUF 15. +THP added for the 300 Mbit/s plan. |
| rootfs | 9.13 MB (cpio.gz) | **5.59 MB** (cpio.xz) | `BR2_TARGET_ROOTFS_CPIO_XZ` + kernel `RD_XZ`  -  the BIOS only memcpys flash→DRAM; the *kernel* unpacks the initramfs, so xz costs nothing at the BIOS level. |

Final measured layout (total 14.3 of 16 MiB): kernel ≤8.5 MiB @0 · **opensbi 512 KB @0x88_0000**
(fw_jump is 261 KB + 8 B FBI wrapper  -  the original 256 KB slot was 4.7 KB short; `flash-images`'s
slot check caught it) · dtb 256 KB @0x90_0000 · rootfs ≤6.75 MiB @0x94_0000.

Flash: `LAYOUT=<build>/flashboot_layout.json KERNEL=… OPENSBI=… DTB=… ROOTFS=…
sw/litex/deploy.sh flash-images` (needs the litex venv on PATH for `crcfbigen`).

## Planned: boot-chain compression (BIOS-LZ4 kernel)  -  bitstream stays JTAG

Stock OpenSBI cannot decompress (`fw_jump` only jumps), and a RISC-V `Image` has no
self-extracting stub (unlike x86 bzImage). The right layer is the **LiteX BIOS**: our
patched `linux_flashboot` already does the flash→DRAM copy, so it gains an **LZ4-block
decompressor** (~200 lines of C, 50–100 MB/s on the 100 MHz core):

| | today | with BIOS-LZ4 |
|---|---|---|
| kernel in flash | 8.14 MB raw | ~4.8 MB lz4 (+~0.2 s boot) |
| free flash | 1.7 MiB | ~5.1 MiB (kernel-growth headroom) |

Rootfs is already maxed (cpio.**xz**, the kernel unpacks it). The freed space would even
fit the 3.83 MB bitstream for a fully standalone power-on box, but per the 2026-07-06
decision the **bitstream stays JTAG-loaded** for the iteration loop; only the
kernel slot gets compressed. Implementation = BIOS patch (lz4 decode into 0x40000000) +
`deploy.sh` compressing at flash time + a layout shrink  -  one reflash to adopt.

## Field notes (2026-07-10 silicon session)

1. **Never `-f` a bitstream to this flash.** The kernel lives at offset 0 (the
   table above); `openFPGALoader -f <bit>` overwrites its FBI. Symptom on the
   next flashboot: `Error: invalid image length 0xffffffff` at the kernel step
   (the bit-file's leading dummy words read as the length). Recovery: re-flash
   `kernel.fbi` raw at `-o 0` (crcfbigen `-f -l`), load bitstreams via **JTAG
   SRAM only**. Corollary: a power-cycle leaves the FPGA unconfigured (flash
   holds no bitstream)  -  the board needs one JTAG load per power-on by design.
2. **The BIOS boot-time SPI auto-calibration defeats the gateware clock cap.**
   liblitespi `spiflash_freq_init()` re-tunes the divisor UP from the gateware
   default while a short CRC block reads stably  -  silicon locked div=2 (50 MHz),
   where MB-scale reads are marginal (per-read-different CRCs; the hsq0-era
   failures). One lucky boot in ~6 was the tell. Fix (build_hsq3+):
   `add_constant("SPIFLASH_SKIP_FREQ_INIT")` next to `add_spi_flash(...,
   clk_freq=12.5e6)`  -  the BIOS then keeps the built-for divisor.
3. **Manual flashboot from `litex>`** (roulette recovery, no serial upload):
   `mem_write 0xf0005000 8` and `0xf0005008 8` (phy+mmap divisors → ~12.5 MHz),
   then per image `mem_read <hdr> 8` (FBI = LE [len][crc32]), `mem_copy <dst>
   <hdr+8> <ceil(len/4)>`, `crc <dst> <len>` == header crc (host-computed ⇒
   end-to-end, catches stale cache lines too), finally `boot 0x40f00000`.
   Scripted: scratchpad `manual_flashboot.sh`. Validated on silicon (all four
   images CRC-OK first try at div 8).
4. **`Initramfs unpacking failed: invalid magic at start of compressed archive`
   ~35 s into boot is benign**: the initrd reservation is 16 MB, the CPIO-XZ is
   5.3 MB  -  the kernel probes the trailing garbage for a concatenated archive
   and reports the miss AFTER the real archive already unpacked. Login works.
5. `rtk` humanizes/dedups tool output on this host  -  when forensics matter
   (byte counts, repeated log lines), read raw files or use `rtk proxy`.

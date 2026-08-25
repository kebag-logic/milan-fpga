# QSPI flash-boot  -  skip the multi-minute serial upload

## Contents

- **[The device at a glance](#the-device-at-a-glance)** — The to-scale flash map, generated from the same `load_map()` that emits the kernel's `fixed-partitions` node — so map, device tree and picture cannot drift apart. The generator also re-runs the overlap/alignment check and prints the verdict *onto* the drawing, which is how a broken map becomes visible before flash time.
- **[Layout "baremetal" - shipping AX7101](#layout-baremetal---shipping-ax7101)** — The two-slot bitstream plus raw AEM manifest, why it has no kernel or FBI wrapper, and the paired-image verification required before firmware enables ADP.
- **[Layout "full" — RETIRED LINUX BRING-UP HISTORY (#259; silicon-verified 2026-07-24)](#layout-full--retired-linux-bring-up-history-259-silicon-verified-2026-07-24)** — The measured five-slot Linux bring-up record, retired by #259: no tool flashes this manifest any more, and the section survives only as the silicon-verified history behind the bare-metal contract.
- **[Layout v3 — SUPERSEDED HISTORY (2026-07-12; offsets no longer deployed)](#layout-v3--superseded-history-2026-07-12-offsets-no-longer-deployed)** — Historical: these offsets are not what ships. Kept for the reasoning that is still true — why the kernel is flashed as `Image.xz` (there is no non-EFI self-extracting kernel on RISC-V), the xz stream rule the vendored decoder imposes, and the four cooperating pieces the whole feature is built from.
- **[The hard constraint: 16 MB flash vs 23 MB of images](#the-hard-constraint-16-mb-flash-vs-23-mb-of-images)** — Why there are two manifests at all: 16 MB of device against ~23 MB of un-slimmed images. Bannered — the arithmetic is permanent but the kernel-at-offset-0 arrangement it argued for is pre-v3 and has not shipped since 2026-07-12. The slot map inside is now read off `FLASHBOOT_LAYOUT` and starts with the bitstream, matching the deployed table above.
- **[How the boot works](#how-the-boot-works)** — The boot-method priority chain and what full vs partial each do. The reassuring part: every copy is CRC-checked from the FBI header, so an empty or half-written flash falls through to serialboot rather than bricking the boot.
- **[Usage](#usage)** — The four commands in order — apply the BIOS patch (re-run after every LiteX upgrade), build, flash, then the fast iteration loop that JTAG-loads gateware while the kernel stays in flash.
- **[Getting to zero-upload](#getting-to-zero-upload)** — The three steps that get a boot to upload nothing, and the size targets they have to hit. `flash-pair` prepares and budgets the whole set before writing, so an un-slimmed kernel fails without a partial update.
- **[Caveats](#caveats)** — Linux DMA coherency, FBI endianness, flash addressing and the profile-specific AEM path. Bare-metal has a raw AEM slot; Linux still loads the paired image from its rootfs on every boot.
- **[Validated](#validated)** — What was actually checked at the time, including the negative: the slot check correctly *rejects* a 14 MB kernel against the 8.5 MiB slot.
- **[2026-07-06: zero-upload ACHIEVED  -  the sizes that made "full" fit](#2026-07-06-zero-upload-achieved-----the-sizes-that-made-full-fit)** — Frozen record of the two rounds of slimming, with the before/after per lever. The kernel-config gotcha worth stealing: without `CONFIG_EXPERT=y` the VT/INPUT disables **silently fail**.
- **[Planned: boot-chain compression (BIOS-LZ4 kernel)  -  bitstream stays JTAG](#planned-boot-chain-compression-bios-lz4-kernel-----bitstream-stays-jtag)** — A proposal, not shipped. Argues the decompressor belongs in the LiteX BIOS rather than OpenSBI, prices the gain at ~3.4 MiB of freed flash, and records the decision that the bitstream stays JTAG-loaded even though the freed space would fit it.
- **[Field notes (2026-07-10 silicon session)](#field-notes-2026-07-10-silicon-session)** — Five things learned the hard way at the bench, including the one that looks like flaky hardware: the BIOS re-tunes the SPI divisor *upward* at boot, defeating the gateware clock cap, and marginal MB-scale reads showed up as one lucky boot in six. Also the manual `litex>` flashboot recovery and a scary-looking initramfs message that is benign.

## The device at a glance

The descriptor-read behavior described below is checked against the
[Milan feature status ledger](../reference/MILAN_FEATURE_STATUS.md):

<!-- milan-feature-status:start -->
| Feature ID | Status | Canonical value |
|---|---|---|
| `aem.served-command-set` | `implemented` | - |
| `soc.baremetal-profile` | `implemented` | - |
<!-- milan-feature-status:end -->

![QSPI flash map](../diagrams/flash_layout.svg)

*What is at which offset, how much of the device each slot actually costs, and
which slots a reflash must never erase* — drawn **to scale**, and **generated**
by [`flash_layout.gen.py`](../diagrams/flash_layout.gen.py) from the one source
of truth (`FLASHBOOT_LAYOUT` + `FLASHBOOT_RESERVED` in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py)),
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

## Layout "baremetal" - shipping AX7101

The shipping AX7101 build uses `--software-profile baremetal --flashboot
baremetal`. Firmware is linked into the FPGA ROM, so there is no kernel,
OpenSBI, DTB or rootfs boot image.

| slot | offset | budget | format | notes |
|---|---:|---:|---|---|
| bitstream | `0x00_0000` | 4 MiB | raw FPGA configuration | Written with `openFPGALoader -f --verify`; configuration logic reads it at power-on. |
| AEM | `0x40_0000` | 64 KiB | raw `aem_desc.bin` | Begins with `AEMI`; never FBI-wrapped. Firmware copies it into paired DRAM and verifies the generated length and CRC32 before enabling ADP/processor. |

The AEM slot deliberately aliases the Linux kernel offset because manifests
are mutually exclusive. The journal and user ranges remain reserved. Always
flash the AEM from the same build as the bitstream: its entity/model identity,
length, CRC and destination are compiled into that firmware.

```console
sw/litex/build.sh ax7101
INSTALLED_BUILD=<exact-current-build> \
    sw/litex/build.sh flash ax7101:<target-builddir>
```

`deploy.sh flash-pair` proves the live installed offset-zero payload, selects
`<target-builddir>/aem_desc.bin` by default, prepares/checks the whole target,
and uses verified writes. The one supported transition is the fabric-baremetal
refresh: AEM verifies first, the target bit commits last, and a retry
recognizes either source or target bit. Layouts naming the retired Linux boot
images or a non-fabric owner refuse before any programmer I/O (#259). See
[BAREMETAL_FIRMWARE.md](BAREMETAL_FIRMWARE.md) for boot ordering and UART
validation.

## Layout "full" — RETIRED LINUX BRING-UP HISTORY (#259; silicon-verified 2026-07-24)

> **Retired (#259, USER directive 2026-08-25).** The product is bare-metal
> only: the `full`/`kernel` manifests, the rootfs, OpenSBI, the DTB slot and
> the software gPTP owner are no longer flashable, and every tool below
> refuses them. This section is preserved as the measured bring-up record.

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
> fit. [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) records 5.6 MiB for the current image, leaving
> ~0.775 MiB of slack. Read the live budget off the generated map above (or off
> the build's own `flashboot_layout.json`), and read the pre-flash size line
> `deploy.sh flash-pair` prints while preparing the complete set, before it
> performs live readback or a write.

All Linux images are FBI-wrapped (`python -m litex.soc.software.crcfbigen
<img> -f -l`) then written raw at their offsets
(`openFPGALoader -o <offset> --write-flash --file-type raw --verify`);
`deploy.sh flash-pair` automates the set. `openFPGALoader --reset` pulses
PROGRAM_B = reboot from flash without a power cycle.

**Matched-image rule (the CSR-rot trap, bitten twice — 07-22 and 07-24):**
the kl-eth LiteX CSR block addresses (dma-ts, dma-pcm, …) are AUTO-ALLOCATED
and SHIFT whenever the gateware's block set changes (e.g. `--rx-queues 1`
dropped the RX1 queue CSRs and moved dma-ts 0x3100→0x308c, dma-pcm
0x3120→0x30ac). The DTB **must be regenerated from the build's `csr.csv`**
and re-embedded into opensbi with every gateware change that touches the
map — the symptom of a stale DTB is subtle (e.g. ptp4l "timed out while
polling for tx timestamp" while everything else works). The same preflight
passes the layout's compiled `cpu_xlen` to `check_dtb_csr.py`: an RV32 build
requires `riscv,isa = "rv32…"` and `mmu-type = "riscv,sv32"` in both the slot
DTB and the FDT embedded in OpenSBI, so an RV64/sv39 boot chain is refused even
when every CSR window happens to match.

**Matched-owner and installed-state rule (#116/#259):** every new
`flashboot_layout.json` carries the resolved `gptp_owner` enum and `cpu_xlen`
compiled into `soc.h`. The only flashable owner is `fabric` on the bare-metal
{bitstream, aem} manifest: `none`, the retired `software` owner, and any
layout naming a retired Linux boot image refuse before programmer I/O. A
completed Vivado build also records `bitstream_payload_sha256` over the
parsed configuration payload (the exact bytes openFPGALoader writes) and the
`.bit` header's `bitstream_fpga_part`; before any write, `deploy.sh
flash-pair` requires both bindings to match the supplied BIT - directory
adjacency is not artifact identity.

The transaction also requires `INSTALLED_LAYOUT` + `INSTALLED_BIT` (or the
named launcher's `INSTALLED_BUILD`). It verifies the layout SHA-256/part against
the parsed Xilinx `.bit` payload, then dumps
the same number of live bytes from QSPI offset zero on the serial-selected
board, and accepts exactly one match: the supplied installed artifact, or the
target artifact when resuming after its commit write. An owner string is not
installed-state evidence. Missing/unknown metadata, a
short/ambiguous/mismatched readback, a wrong build directory, a
missing/mismatched payload digest, a `.bit` FPGA part that differs from the
layout or selected programmer part, and a missing or oversized *last* image
all refuse before a write. A live target bit beside a stale AEM gets an
AEM-only repair, because the autonomous fabric commit bit owns gPTP
independently of AEM. `deploy.sh check-images` retains the read-only
target preflight.
Sweep fallback layouts reconstruct the enum and CPU width from the compiled
`MILAN_GPTP_OWNER` / `MILAN_CPU_XLEN` constants, then hash the explicitly
selected `.bit`; missing or ambiguous bit artifacts refuse reconstruction.

Write order is part of the invariant:

| installed → target | completed verified writes |
|---|---|
| fabric/baremetal → fabric/baremetal | raw AEM, then target fabric bit |
| anything naming a retired Linux artifact (#259) | refused before programmer I/O |
| owner `none` or the retired `software` owner | refused before programmer I/O |

At every accepted boundary the old or new fabric owner remains bootable.
A process/tool failure can be retried with the same installed reference. This
does not make a single flash slot electrically atomic: power loss *during*
offset-zero erase/program can tear the only bitstream. A/B or Xilinx MultiBoot
is required to remove that hardware boundary.

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
| bitstream | 0x00_0000  | 2.25 MiB | ~2.0-2.3 | raw config stream committed by `deploy.sh flash-pair`; NOT fbi-wrapped |
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

It has three cooperating pieces, all opt-in behind
`milan_soc.py --with-spiflash` (included in `--all-blocks`):

| piece | where | what |
|-------|-------|------|
| **flash core** | [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py), [`sw/litex/platforms/alinx_ax7101.py`](../../sw/litex/platforms/alinx_ax7101.py) | memory-maps the on-board flash; emits the `MILAN_FLASHBOOT_*` layout constants |
| **BIOS method** | [`sw/litex/patches/0001-milan-linux-flashboot.patch`](../../sw/litex/patches/0001-milan-linux-flashboot.patch) | `linux_flashboot` copies images flash→DRAM, boots (or pre-loads then defers to serialboot) |
| **flashing** | `sw/litex/deploy.sh check-images` / `flash-pair` | SHA-256/part-binds each layout to its parsed `.bit` payload and its compiled CPU width, requires the fabric owner on the bare-metal {bitstream, aem} manifest, refuses every retired Linux boot image and the retired software owner (#259) before programmer I/O, materializes every image, live-matches QSPI offset zero to the exact installed/target payload, then performs verified writes with the target bit last ([qspi_owner_transition.py](../../sw/litex/qspi_owner_transition.py), [check_gptp_owner_pair.py](../../sw/litex/check_gptp_owner_pair.py)) |

---

## The hard constraint: 16 MB flash vs 23 MB of images

> **PARTLY SUPERSEDED — read the arithmetic, not the offsets (bannered
> 2026-07-27).** The *constraint* below is permanent and is why the layout looks
> the way it does: 16 MB of device against ~23 MB of un-slimmed images. The
> *arrangement* it describes — kernel at offset 0, bitstream deliberately not in
> flash — is the **pre-v3** layout and has not been deployed since 2026-07-12.
> What ships puts the **bitstream at `0x00_0000` with a 4 MiB budget and the
> kernel at `0x40_0000`**; that is what
> [Layout "full"](#layout-full--linux-bring-up-truth-2026-07-24-silicon-verified-end-to-end)
> above describes, what `FLASHBOOT_LAYOUT` in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py) contains,
> and what a build's own `flashboot_layout.json` exports (re-verified against a
> build dir while flashing, 2026-07-27). Two things below are stale rather than
> merely dated — the *sizes* in the image table (the kernel is flashed as a
> ~2.5 MB `Image.xz`, not a ~14 MB raw `Image`) and the bitstream paragraph,
> which is bannered where it sits.

The AX7101 flash is a **Micron N25Q128 = 128 Mbit = 16 MB** (confirmed from the Alinx repo,
`DATASHEET/QSPI FLASH/N25Q128.pdf`). The boot images total **~23 MB**:

| image | size | DRAM target |
|-------|------|-------------|
| kernel `Image` | ~14 MB | `0x4000_0000` |
| `rootfs.cpio.gz` | ~8.7 MB | `0x4100_0000` (initrd) |
| `opensbi.bin` (fw_jump) | ~0.26 MB | `0x40f0_0000` (**boot entry**, a0=hartid, a1=0) |
| `milan.dtb` | ~3 KB | `0x40ef_0000` |

(Those are the *un-slimmed* sizes that created the problem. The kernel has since
been slimmed and is flashed compressed, which is what dissolved it — see
[Getting to zero-upload](#getting-to-zero-upload).)

So **not everything fits at once**. Two manifests (`--flashboot`):

* **`kernel` (the `--flashboot` default)  -  partial.** Flash only the big, static kernel (a ~14 MB raw `Image`
  at the time this was written; ~2.5 MB as `Image.xz` today).
  `linux_flashboot` pre-loads it to DRAM; serialboot then uploads only OpenSBI+dtb+rootfs
  (~9 MB). **~60 % faster** per boot, no image rebuild. The kernel + OpenSBI are the images
  that change *least*, so most iterations upload just the ~9 MB rest.
* **`full`  -  zero upload.** Flash every image; `linux_flashboot` boots OpenSBI directly with
  **no serial upload at all**. Fits once the kernel is slimmed to **≤ 8.5 MiB** with a
  cpio.xz rootfs ≤ 6.75 MiB — achieved 2026-07-06 with an 8.14 MB `-Os` kernel (see
  [Getting to zero-upload](#getting-to-zero-upload)); the deploy step refuses an oversized
  image rather than silently corrupt the layout.

> **NOT TRUE OF A CURRENT BUILD.** *"Because the default kernel occupies flash
> offset 0, the bitstream is not stored in flash in this layout — flash-boot
> builds are JTAG-`load`ed (`deploy.sh load`) … a bitstream + a 14 MB kernel
> cannot coexist in 16 MB."* Both halves were resolved rather than refuted: the
> kernel moved off offset 0 and the 14 MB `Image` became a ~2.5 MB `Image.xz`,
> which is exactly what made room for the bitstream. **The board now QSPI
> config-boots the bitstream from offset 0**, and `deploy.sh load` is the fast
> *iteration* path, not the only one.

### Flash layout (`FLASHBOOT_LAYOUT` in `milan_soc.py`)

The map below is read straight out of `FLASHBOOT_LAYOUT` + `FLASHBOOT_RESERVED`
in [`sw/litex/milan_soc.py`](../../sw/litex/milan_soc.py). It is the same map the
[Linux bring-up table](#layout-full--linux-bring-up-truth-2026-07-24-silicon-verified-end-to-end)
above renders slot by slot, and the same one the SVG at the top of this page is
generated from:

```
 offset      slot       budget      notes
 0x00_0000   bitstream  4 MiB       config-read by the FPGA, NOT fbi-wrapped
 0x40_0000   kernel     3 MiB       Image.xz, BIOS xz_embedded -> 0x4000_0000
 0x70_0000   opensbi    384 KiB     fw_jump -> 0x40F0_0000 (carries the kernel DTB)
 0x76_0000   dtb        128 KiB     decoy copy; the kernel boots on OpenSBI's FDT
 0x78_0000   rootfs     6.375 MiB   cpio.xz -> 0x4100_0000 (v4: was 8.5 MiB)
 0xDE_0000   journal    128 KiB     RESERVED, raw A/B - never erased by a reflash
 0xE0_0000   user       2 MiB       RESERVED, jffs2 -> /user
```

The two `RESERVED` slots are not boot images: the BIOS never copies them and a
reflash must not erase them. (The saved-state journal that used those slots was deleted 2026-08-13 with this repository's own AECP/AEM engine; the slots stay reserved in the flash map, and nothing writes or reads them today. Persistence is a genuine loss, not a relocation: the protocol processor's NVM face is answered by a blank-flash responder, so a restore walk always completes with zero records and nothing survives a power cycle.)

The manifests (`--flashboot`) select which *images* the BIOS copies, not where
they live: `kernel` (partial) pre-loads only the kernel and lets serialboot
supply the rest, `full` copies opensbi + dtb + kernel + rootfs for a zero-upload
boot. The bitstream is in neither manifest — the FPGA config logic reads it
before any BIOS runs.

The build writes `<build>/flashboot_layout.json` (the single source of truth);
`deploy.sh flash-pair` reads it, so the gateware's compiled-in offsets, gPTP
owner, CPU XLEN, rootfs lease and flashing never drift. A Vivado-produced copy
is deployable only when its parsed payload SHA-256 and FPGA part are present;
an elaboration-only JSON deliberately has no bit binding and fails closed.
**Read the build's own copy** — the numbers above are a snapshot of the tree, and
the `rootfs` budget in particular has already moved once (v4, 2026-07-26).

---

## How the boot works

For `baremetal`, the LiteX BIOS itself is the application. Its Milan init hook
loads and CRC-checks the raw AEM slot, programs fabric policy, and enables the
entity only on success. It does not invoke `linux_flashboot` or serialboot.

The Linux `kernel` and `full` manifests retain the boot-method sequence below.

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
* **Partial manifest:** `linux_flashboot` copies only the kernel to `0x4000_0000`,
  prints a note and returns. There is no active kernel-from-QSPI serialboot
  shortcut: the companion `boot.sh` always uploads and verifies the complete
  volatile kernel/OpenSBI/DTB/rootfs tuple. The partial layout remains only as
  an explicit non-atomic recovery primitive.

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

Shipping bare-metal:

```sh
sw/litex/build.sh ax7101
INSTALLED_BUILD=<exact-current-build> \
    sw/litex/build.sh flash ax7101:<target-build>
```

The AX8x8 full-Linux product profile keeps fabric ownership:

```sh
sw/litex/build.sh ax8x8
KERNEL=… OPENSBI=… DTB=… ROOTFS=… \
INSTALLED_BUILD=<exact-current-build> \
    sw/litex/build.sh flash ax8x8:<target-build>
```

For a direct transaction, replace `INSTALLED_BUILD` with the exact
`INSTALLED_LAYOUT` + `INSTALLED_BIT`, set the target `LAYOUT` + `BIT` and image
variables, then invoke `sw/litex/deploy.sh flash-pair`.

The software-owner option-OFF comparison is a generated config variant with
`board.features.fabric_gptp: false` and a positive v1 software-profile rootfs.
Moving between that
full-Linux image and the product fabric/full-Linux image requires the shipping
`ax7101` fabric/baremetal build as the two-transaction bridge described above.

### Recovery-only partial mode

Partial `kernel` layouts are not an autonomously bootable software-owner set
and are excluded from both the persistent owner guarantee and the supported
serialboot path. The direct primitive remains for lab recovery and therefore
requires an explicit escape:

```sh
ALLOW_NONATOMIC_FLASH=1 LAYOUT=<partial-build>/flashboot_layout.json \
KERNEL=/path/to/images/Image ROOTFS=/path/to/images/rootfs.cpio.xz \
    sw/litex/deploy.sh flash-images
```

The escape still runs the owner/DTB checks (and a direct bit recovery verifies
the layout's payload SHA-256/part), prepares the entire requested
subset and uses verified writes. It does **not** prove live installed state or
claim safe persistent ordering. Named `build.sh flash` never sets the escape.

### Iterate (the fast loop)

```sh
sw/litex/deploy.sh load             # JTAG → SRAM (volatile)
# then, in the-private-test-repo:
O=<buildroot-out> LAYOUT=<exact-layout> BIT=<exact-bit> \
DTB=<exact-dtb> OPENSBI=<exact-fw_jump> fpga/boot/boot.sh
```

The companion boot entry point verifies the owner/CPU/CSR tuple, loads the
exact volatile bit, and uploads the complete Linux tuple. It deliberately does
not trust a pre-existing QSPI kernel.

---

## Getting to zero-upload

The 14 MB kernel was the blocker. Slim it below the 8.5 MiB slot (achieved: 8.14 MB,
see the 2026-07-06 section below) and switch the rootfs to cpio.xz, and the **full**
   manifest fits  -  then a boot uploads *nothing*:

1. Trim the kernel `.config` (drop unused drivers/filesystems/debug; the Milan NIC needs only
   `kl-eth` + the litex UART/CLINT/PLIC). A lean RV64 buildroot kernel is ~4–6 MB.
2. Rebuild; confirm `Image` ≤ 8.5 MiB (the slot size) and the cpio.xz rootfs ≤ 6.75 MiB.
3. Build `--flashboot full`, transactionally flash the complete set, and boot
   with no serial step:
   ```sh
   TAG=<tag> sw/litex/build.sh ax8x8
   INSTALLED_LAYOUT=… INSTALLED_BIT=… LAYOUT=<build>/flashboot_layout.json \
   BIT=<build>/gateware/alinx_ax7101.bit KERNEL=…/Image \
   OPENSBI=…/opensbi.bin DTB=…/milan.dtb ROOTFS=…/rootfs.cpio.gz \
       sw/litex/deploy.sh flash-pair
   sw/litex/deploy.sh load     # BIOS flash-boots directly; no boot.sh needed
   ```

`flash-pair` materializes and budgets every image before live readback or a
write, so an un-slimmed kernel fails without partially updating QSPI.

---

## Caveats

* **`--coherent-dma` is mandatory and NOT implied by `--all-blocks`.** Without it the NIC's
  DMA masters bypass the NaxRiscv snooping `dma_bus`: RX data never becomes CPU-visible (the
  stack drops every frame  -  all-zero skbs) and TX reads stale skb data (garbage dst MAC that
  the peer NIC silently filters). Hardware-confirmed 2026-07-04; `deploy.sh` includes it.
* ~~**No bitstream in flash (kernel layout).**~~ **NO LONGER TRUE (since the v3
  layout, 2026-07-12).** This bullet described the pre-v3 arrangement, where the
  kernel sat at offset 0, a power-cycle left the FPGA unconfigured and every
  power-on needed a JTAG `load`. The deployed layout puts the **bitstream at
  offset 0** and the board config-boots it from flash. `flash-pair` owns both
  disjoint slot classes and orders them as one transaction; direct `flash` and
  `flash-images` are recovery-only escapes.
  JTAG `load` remains the *iteration* path because it skips the flash write, not
  because flash cannot hold a bitstream.
* **Re-apply the patch after LiteX updates** (`apply.sh` is idempotent and errors clearly if
  LiteX has moved the patched lines  -  then refresh the `.patch`).
* **Endianness:** the FBI header is little-endian (`crcfbigen -l`), matching the BIOS's
  `MMPTR` reads on this RV64 core. `deploy.sh` uses `-l`; don't drop it.
* **Flash addressing:** the N25Q128 is 16 MB = 3-byte addressable, so the whole chip is
  reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ,
  so WP#/HOLD# are never left floating.
* **openFPGALoader offset 0** is only guarded on *Efinix* boards; the Xilinx SPI path (v1.1.1,
  verified) writes raw at any offset, so writing offset 0 by hand is fine here
  (it is the bitstream slot in the deployed layout, and was the kernel slot
  pre-v3).
* **The AEM path is profile-specific.** Since 2026-08-13 the entity model is
  not a ROM in gateware:
  the protocol processor's descriptor store fetches it from **DRAM**, at a
  **compile-time** base (`PP_DESC_BASE_P`, derived by the SoC as the top 1 MiB
  of `main_ram` and reserved in the device tree — there is no base register to
  program). Under Linux it has no flash slot and software must write the paired
  rootfs image into DRAM on every boot before enabling the entity. Under the
  shipping bare-metal manifest, raw `aem_desc.bin` occupies the 64 KiB slot at
  `0x40_0000`; firmware copies and CRC-checks it before enabling
  `PP_CTRL[0]` and `ADP_CTRL[0]`. The
  end-station builder produces `aem_desc.bin`, `aem_desc.json`, and
  `aem_desc.map`. The tracked rootfs packages the paired artifacts under
  `/etc/milan-aem/`, and `aemi-load` verifies and writes the image before entity
  enable. A custom boot path must provide the equivalent step. An unloaded or
  corrupt image reports zero configurations, so every `READ_DESCRIPTOR` returns
  `BAD_ARGUMENTS`; the store watchdog prevents a stalled bus from hanging the
  command, and a late load heals without a reset. Bench walk-through:
  [Section 26 of ../limitations/TROUBLESHOOTING.md](../limitations/TROUBLESHOOTING.md#section-26-the-controller-finds-the-entity-and-enumerates-nothing---the-descriptor-image-was-never-loaded-into-dram).

---

## Validated

* Gateware elaborates + generates `csr.json` (SPIFLASH region at `SPIFLASH_BASE`, litespi
  master CSRs) and emits the correct `MILAN_FLASHBOOT_*` constants for both manifests
  (`kernel`: kernel-only, no `COMPLETE`; `full`: all four + `COMPLETE`).
* The patched BIOS compiles; `linux_flashboot` and `milan_flash_boot_method` link into the
  boot-method section.
* The RV32I bare-metal BIOS compiles and the generated `baremetal` layout
  contains only bitstream plus the 64 KiB raw AEM slot. The deployment path
  leaves the `AEMI` bytes unframed.
* The legacy `flash-images` materializer wraps the real 14 MB `Image` into a
  14 MB+8 B FBI and enforces slot budgets. The current `flash-pair` gate adds
  whole-set preparation, live `.bit` readback identity, verified direction
  ordering, 28 before/after-write failure prefixes and resumability.

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
(fw_jump is 261 KB + 8 B FBI wrapper  -  the original 256 KB slot was 4.7 KB short; the
image budget check caught it) · dtb 256 KB @0x90_0000 · rootfs ≤6.75 MiB @0x94_0000.

The command used in that 2026-07-06 session predates owner transactions. Use
the current `flash-pair` recipe in [Usage](#usage); it still needs the LiteX
environment for `crcfbigen`.

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

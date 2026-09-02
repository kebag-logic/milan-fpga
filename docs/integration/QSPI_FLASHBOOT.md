# QSPI flash-boot  -  skip the multi-minute serial upload

## Contents

- **[The device at a glance](#the-device-at-a-glance)** — The to-scale flash map, generated from `FLASHBOOT_LAYOUT` itself, so the picture cannot drift from the map the build compiles in. The generator also re-runs the overlap/alignment check and prints the verdict *onto* the drawing, which is how a broken map becomes visible before flash time.
- **[Layout "baremetal" - shipping AX7101](#layout-baremetal---shipping-ax7101)** — The only manifest that ships: bitstream plus raw AEM image, why the AEM bytes carry no FBI wrapper, the two reserved ranges a reflash must not erase, and the paired-image verification required before firmware enables ADP.
- **[How the boot works](#how-the-boot-works)** — Power-on to entity-enabled in one hop: config logic reads the bitstream, the BIOS is the application, and the AEM copy is length- and CRC-checked, so an empty or half-written slot leaves the entity disabled instead of bricking the boot.
- **[Usage](#usage)** — Build and flash the pair, the explicit non-atomic escape kept for lab recovery, and the JTAG iteration loop that skips the flash write.
- **[Caveats](#caveats)** — Flash addressing and the AEM path in full: the descriptor image lives in reserved memory at a compile-time base, so a custom boot path that skips the copy enumerates nothing.
- **[Validated](#validated)** — What was actually checked rather than assumed: the emitted constants, the bare-metal BIOS build, the unframed `AEMI` bytes, and what the `flash-pair` gate adds over the recovery-only materializer.
- **[Field notes (2026-07-10 silicon session)](#field-notes-2026-07-10-silicon-session)** — The bench lesson that looks like flaky hardware: the BIOS re-tunes the SPI divisor *upward* at boot, defeating the gateware clock cap, and marginal MB-scale reads showed up as one lucky boot in six.

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
read through its `load_map()`. The map and this picture move together or not at
all. Regenerate with:

```
python3 docs/diagrams/flash_layout.gen.py docs/diagrams/flash_layout
rsvg-convert -w 1800 docs/diagrams/flash_layout.svg -o docs/diagrams/flash_layout.png
```

The generator also re-runs the map consistency check (overlap / erase-block
alignment / past-the-device) and prints the verdict on the drawing, so a broken
map is visible in the picture rather than only at flash time.

## Layout "baremetal" - shipping AX7101

The shipping AX7101 build uses `--software-profile baremetal --flashboot
baremetal`. Firmware is linked into the FPGA ROM, so the flash carries no
second-stage boot image at all: two slots, and nothing to upload.

| slot | offset | budget | format | notes |
|---|---:|---:|---|---|
| bitstream | `0x00_0000` | 4 MiB | raw FPGA configuration | Written with `openFPGALoader -f --verify`; configuration logic reads it at power-on. |
| AEM | `0x40_0000` | 64 KiB | raw `aem_desc.bin` | Begins with `AEMI`; never FBI-wrapped. Firmware copies it into paired DRAM and verifies the generated length and CRC32 before enabling ADP/processor. |

The AEM slot sits at `0x40_0000`, immediately after the bitstream budget.
Always flash the AEM from the same build as the bitstream: its entity/model identity,
length, CRC and destination are compiled into that firmware.

The `journal` and `user` ranges are RESERVED: no manifest writes them and a
reflash must not erase them. The saved-state journal that used those slots
was deleted 2026-08-13 with this repository's own AECP/AEM engine, so nothing
writes or reads them today. Persistence is a genuine loss, not a relocation:
the protocol processor's NVM face is answered by a blank-flash responder, so a
restore walk always completes with zero records and nothing survives a power
cycle.

The build writes `<build>/flashboot_layout.json` (the single source of truth);
`deploy.sh flash-pair` reads it, so the gateware's compiled-in offsets, gPTP
owner, CPU XLEN and flashing never drift. A Vivado-produced copy is deployable
only when its parsed payload SHA-256 and FPGA part are present; an
elaboration-only JSON deliberately has no bit binding and fails closed. **Read
the build's own copy** rather than any number quoted in prose.

```console
sw/litex/build.sh ax7101
INSTALLED_BUILD=<exact-current-build> \
    sw/litex/build.sh flash ax7101:<target-builddir>
```

`deploy.sh flash-pair` proves the live installed offset-zero payload, selects
`<target-builddir>/aem_desc.bin` by default, prepares/checks the whole target,
and uses verified writes. The one supported transition is the fabric-baremetal
refresh: AEM verifies first, the target bit commits last, and a retry
recognizes either source or target bit. Layouts naming a retired boot image or
a non-fabric owner refuse before any programmer I/O (#259). See
[BAREMETAL_FIRMWARE.md](BAREMETAL_FIRMWARE.md) for boot ordering and UART
validation.

## How the boot works

The FPGA configuration logic reads the bitstream from offset 0 at power-on,
before any software runs. The LiteX BIOS is then the application itself: its
Milan init hook loads and CRC-checks the raw AEM slot, programs fabric policy,
and enables the entity only on success. There is no second-stage image, no
boot-method chain and no serial upload in the shipping path.

The AEM copy goes through the BIOS's `copy_image_from_flash_to_ram`, so the
slot's length and CRC32 are both checked before a byte is used. A failed check
abandons the copy and leaves the entity disabled rather than advertising a model
nobody can enumerate: an empty or half-written slot **cannot brick the boot**.

---

## Usage

### Build a flash-boot bitstream

Every named config produces the same {bitstream, AEM} pair;
`ax8x8` and `arty` differ from `ax7101` only in dataplane shape:

```sh
sw/litex/build.sh ax7101
INSTALLED_BUILD=<exact-current-build> \
    sw/litex/build.sh flash ax7101:<target-build>
```

For a direct transaction, replace `INSTALLED_BUILD` with the exact
`INSTALLED_LAYOUT` + `INSTALLED_BIT`, set the target `LAYOUT` + `BIT`, then
invoke `sw/litex/deploy.sh flash-pair`. A layout naming a retired boot image
or a non-fabric owner refuses before any programmer I/O.

The current CSR ABI is `VERSION=0x0002_0057`. Every flashable manifest selects
the sole fabric gPTP owner. The direct option-OFF elaboration is
verification-only and ownerless: GM identity, parent identity, path data and
pdelay are zero; `sync=0`, `asCapable=0`, and `time_uncertain=1`; every legacy
publication write is inert. Its artifacts are refused by the flash tools.

### Recovery-only partial mode

The direct primitives (`flash`, `flash-images`) remain for lab recovery of
the bare-metal pair only, behind an explicit escape:

```sh
ALLOW_NONATOMIC_FLASH=1 LAYOUT=<build>/flashboot_layout.json \
    sw/litex/deploy.sh flash-images
```

The escape still runs the owner checks (and a direct bit recovery verifies
the layout's payload SHA-256/part), prepares the entire requested subset and
uses verified writes. It does **not** prove live installed state or claim
safe persistent ordering, and a layout naming a retired image slot refuses.
Named `build.sh flash` never sets the escape.

### Iterate (the fast loop)

```sh
sw/litex/deploy.sh load             # JTAG → SRAM (volatile)
```

The flashed AEM slot pairs with the flashed bitstream, so after a volatile
JTAG load of a DIFFERENT build, provision the matching `aem_desc.bin` before
enabling the entity (see the AEM caveat below).

---

## Caveats

* **The bitstream is the offset-zero commit artifact.** The board config-boots
  it directly. `flash-pair` owns the bitstream and AEM slots and orders them as
  one transaction; direct `flash` and `flash-images` are recovery-only escapes.
  JTAG `load` remains the fast iteration path because it skips the flash write.
* **Flash addressing:** the N25Q128 is 16 MB = 3-byte addressable, so the whole chip is
  reachable with the standard quad read (`READ_1_1_4`, 0x6B). `mode="4x"` drives all four DQ,
  so WP#/HOLD# are never left floating.
* **Do not write offset zero by hand for a normal update.** The Xilinx SPI path
  can write it, but only `flash-pair` proves the installed/target artifacts and
  preserves the bitstream+AEM ordering contract.
* **The AEM path is profile-specific.** Since 2026-08-13 the entity model is
  not a ROM in gateware:
  the protocol processor's descriptor store fetches it from **DRAM**, at a
  **compile-time** base (`PP_DESC_BASE_P`, derived by the SoC as the top 1 MiB
  of `main_ram` and reserved for the firmware; there is no base register to
  program). Under the
  shipping bare-metal manifest, raw `aem_desc.bin` occupies the 64 KiB slot at
  `0x40_0000`; firmware copies and CRC-checks it before enabling
  `PP_CTRL[0]` and `ADP_CTRL[0]`. The
  end-station builder produces `aem_desc.bin`, `aem_desc.json`, and
  `aem_desc.map`. A custom boot path must provide the equivalent step. An unloaded or
  corrupt image reports zero configurations, so every `READ_DESCRIPTOR` returns
  `BAD_ARGUMENTS`; the store watchdog prevents a stalled bus from hanging the
  command, and a late load heals without a reset. Bench walk-through:
  [Section 26 of ../limitations/TROUBLESHOOTING.md](../limitations/TROUBLESHOOTING.md#section-26-the-controller-finds-the-entity-and-enumerates-nothing---the-descriptor-image-was-never-loaded-into-dram).

---

## Validated

* Gateware elaborates + generates `csr.json` (SPIFLASH region at `SPIFLASH_BASE`, litespi
  master CSRs) and emits the `MILAN_FLASHBOOT_*` constants the shipping manifest needs.
* The RV32I bare-metal BIOS compiles and the generated `baremetal` layout
  contains only bitstream plus the 64 KiB raw AEM slot. The deployment path
  leaves the `AEMI` bytes unframed.
* The recovery-only `flash-images` materializer FBI-wraps what it is given and
  enforces slot budgets. The `flash-pair` gate adds whole-set preparation, live
  `.bit` readback identity, verified direction ordering, 28 before/after-write
  failure prefixes and resumability.

See also [BOARD_PORTING_AX7101.md](BOARD_PORTING_AX7101.md) and
[`sw/litex/patches/README.md`](../../sw/litex/patches/README.md).

---

## Field notes (2026-07-10 silicon session)

1. **Use `flash-pair` for persistent updates.** It proves the live offset-zero
   payload, validates the target pair and writes the AEM image before the
   bitstream commit artifact. Use JTAG `load` for volatile iteration.
2. **The BIOS boot-time SPI auto-calibration defeats the gateware clock cap.**
   liblitespi `spiflash_freq_init()` re-tunes the divisor UP from the gateware
   default while a short CRC block reads stably  -  silicon locked div=2 (50 MHz),
   where MB-scale reads are marginal (per-read-different CRCs; the hsq0-era
   failures). One lucky boot in ~6 was the tell. Fix (build_hsq3+):
   `add_constant("SPIFLASH_SKIP_FREQ_INIT")` next to `add_spi_flash(...,
   clk_freq=12.5e6)`  -  the BIOS then keeps the built-for divisor.
3. **Grade every persistent update over UART from the bench workstation.** Run
   `python3 scripts/baremetal_uart_smoke.py --port /dev/serial/by-id/<adapter>`; it checks
   the image, identity, `0x0002_0056` publication ABI and advancing PHC.
4. **Use an external JTAG/CSR transport for evidence not exposed by the UART
   firmware.** The console deliberately provides only the documented
   `milan_status`, time and UTC commands; it is not a general register shell.

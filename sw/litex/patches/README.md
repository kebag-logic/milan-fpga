# LiteX-ecosystem patches

Small additions to the **LiteX / LiteEth / VexiiRiscv pythondata** source trees (vendored or pip-installed),
shipped here as patches and applied in place by `apply.sh` (idempotent; discovers each
tree from the active Python env; re-run after every LiteX/LiteEth update).

## Contents

- **[0002-liteeth-gmii-tx-clk-invert.patch — GMII TX clock phase option](#0002-liteeth-gmii-tx-clk-invertpatch--gmii-tx-clock-phase-option)** — Forwards `gtx_clk` 180° out of phase, and the measured verdict for the AX7101/RTL8211E: REQUIRED once the TX launch FFs are IOB-packed — 25-40 % corrupt frames edge-aligned vs 20/20 pings and zero CRC errors inverted. Also says what it is *not*: this was never the silence bug.
- **[0001-milan-linux-flashboot.patch — QSPI Linux flash-boot](#0001-milan-linux-flashbootpatch--qspi-linux-flash-boot)** — A BIOS boot method that copies the Linux images out of memory-mapped QSPI into DRAM instead of waiting on a serial upload. Names the three BIOS files it touches, and why it registers at priority -10 (ahead of serialboot, which stays as fallback) and compiles to nothing on non-Milan builds.
- **[0002-vexiiriscv-l2-depth-args.patch — VexiiRiscv L2 geometry args](#0002-vexiiriscv-l2-depth-argspatch--vexiiriscv-l2-geometry-args)** — The VexiiRiscv L2 arguments four of the five configs pass, so `apply.sh` applies it too as of 2026-08-21. Read this if you were confused by the duplicate `0002-` prefix: it targets a different tree.
- **[0004-vexiiriscv-baremetal-variant.patch](#0004-vexiiriscv-baremetal-variantpatch)** — Adds the one-hart RV32I plus `zicsr`/`zifencei` Vexii variant with machine mode only and no MMU, predictor, counters, FPU or L1 cache.
- **[0005-vexiiriscv-cacheless-litex.patch](#0005-vexiiriscv-cacheless-litexpatch)** — Replaces Vexii's L1 assumptions with a shared cacheless TileLink topology so CPU and non-coherent Milan DMA still reach peripherals and LiteDRAM.
- **[Usage](#usage)** — The `apply.sh` verbs (apply, `--reverse`, `PYTHON=` for a specific env), why you must re-run after every LiteX upgrade, and the copy-paste recipe for re-diffing a patch that no longer applies.

## `0002-liteeth-gmii-tx-clk-invert.patch` — GMII TX clock phase option

Adds `tx_clk_invert` to `LiteEthPHYGMII(CRG)`: forwards `gtx_clk` **180° out of phase**
with TXD via the ODDR. Default `False` = upstream edge-aligned behavior. Exposed as
`milan_soc.py --gtx-tx-invert`.

**Final measured verdict on the AX7101 (RTL8211E), 2026-07-04 — REQUIRED (with IOB-packed
TX FFs):** the phase was never the *silence* bug (that was the cut-through/starvation issue
+ missing `--coherent-dma` — see the retired MAC TX bring-up finding (#259, in git history)), but once the GMII TX launch
FFs are packed into the IOB (deterministic skew ≈ 0 vs the forwarded clock), edge-aligned
sampling is hold-marginal: measured 25–40 % corrupt frames (`rx_crc_errors` at the peer) vs
**20/20 pings + 0 CRC errors with the invert** (mid-bit sampling, ~4 ns/4 ns margins).
`deploy.sh` enables `--gtx-tx-invert` by default for this board.

## `0001-milan-linux-flashboot.patch` — QSPI Linux flash-boot

Adds a `linux_flashboot` BIOS boot method that copies the Linux boot images out of the
memory-mapped QSPI flash into DRAM, so a boot needs **no** (or, for the partial manifest,
much smaller) serial upload — the "gain time" path. See [`docs/integration/QSPI_FLASHBOOT.md`](../../../docs/integration/QSPI_FLASHBOOT.md).

Touches three BIOS files (all in `litex/soc/software/bios/`):

| file | change |
|------|--------|
| `boot.c`  | broaden the flash-image-helper guards to also compile under `MILAN_FLASHBOOT_ENTRY` (without setting `FLASH_BOOT_ADDRESS`, since the BIOS itself is *not* booted from flash), and add `linux_flashboot()` |
| `boot.h`  | declare `linux_flashboot(void)` |
| `main.c`  | register it with `define_boot_method(milan_flash, …, -10)` so it runs **before** serialboot (which stays as the fallback) |

It is driven entirely by the `MILAN_FLASHBOOT_*` constants that `milan_soc.py --with-spiflash`
emits into `generated/soc.h`. With no such constants the added code compiles to nothing, so
the patch is inert on non-Milan builds.

## `0002-vexiiriscv-l2-depth-args.patch` — VexiiRiscv L2 geometry args

Exposes VexiiRiscv L2 depth/geometry arguments used by the performance
campaign's L2 experiments (see [`CHANGELOG.md`](../../../CHANGELOG.md) / `docs/findings/`).
**Applied by `apply.sh` since 2026-08-21.** It used to say "not applied,
apply it by hand for a non-default L2", and that description outlived the
historical Linux performance campaign: four former configurations passed
`--scala-args=--l2-down-pending`. Those configurations and their shipping
claim are retired under #259; the patch remains in the reproducibility series
until #259 removes that compatibility code. It targets the Scala checkout
inside the pythondata package rather than a Python package, which is why
`apply.sh` resolves it separately. (Yes, the file shares the `0002-` prefix
with the LiteEth patch — they target different trees.)

## `0004-vexiiriscv-baremetal-variant.patch`

Adds the LiteX `baremetal` Vexii variant. It uses `ParamSimple` at XLEN 32 and
adds only RV32I, `zicsr` and `zifencei`; no M/F extension, supervisor mode,
MMU, branch predictor, counters or L1 cache is enabled. LiteX only publishes
`CPU_MMU` when supervisor mode is present.

## `0005-vexiiriscv-cacheless-litex.patch`

Upstream `Soc.scala` assumed the LSU L1 existed: it rejected uncached memory
regions, tied coherency to DMA presence, dereferenced the L1 diagnostics and
only built the split cached/non-cached fabric. This patch adds the cacheless
topology used by the RV32I variant:

- Vexii instruction and data buses share one address-decoded TileLink node.
- Main memory and the peripheral node are both downstream of that node.
- LiteX/Milan DMA masters join the same non-coherent node directly.
- Coherency and L1 diagnostics remain conditional on L1 actually existing.

The resulting SoC still gives CPU and DMA access to LiteDRAM, while removing
the cache hub and stale-copy problem by construction. `apply.sh` applies the
patch to `pythondata_cpu_vexiiriscv` and treats a reverse-applicable patch as
already installed.

## Usage

```sh
./apply.sh            # apply to the LiteX tree of the active Python env (idempotent)
./apply.sh --reverse  # undo
PYTHON=/path/to/venv/bin/python3 ./apply.sh   # target a specific env
```

The LiteX tree is found from the active Python environment (`import litex`), so there are no
machine-specific paths. **Re-run `apply.sh` after every `pip install -U litex` / LiteX update**
— an upgrade resets the BIOS sources. If LiteX has moved the patched lines, `apply.sh` stops
with an error; re-diff against the new tree and refresh the `.patch`:

```sh
# after hand-re-applying the three edits to the new BIOS sources:
git -C "$(python3 -c 'import litex,os;print(os.path.dirname(os.path.dirname(litex.__file__)))')" \
    diff -- litex/soc/software/bios/{boot.c,boot.h,main.c} > 0001-milan-linux-flashboot.patch
```

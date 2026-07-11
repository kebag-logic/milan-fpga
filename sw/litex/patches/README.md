# LiteX-ecosystem patches

Small additions to the **LiteX / LiteEth** source trees (vendored or pip-installed),
shipped here as patches and applied in place by `apply.sh` (idempotent; discovers each
tree from the active Python env; re-run after every LiteX/LiteEth update).

## `0002-liteeth-gmii-tx-clk-invert.patch` — GMII TX clock phase option

Adds `tx_clk_invert` to `LiteEthPHYGMII(CRG)`: forwards `gtx_clk` **180° out of phase**
with TXD via the ODDR. Default `False` = upstream edge-aligned behavior. Exposed as
`milan_soc.py --gtx-tx-invert`.

**Final measured verdict on the AX7101 (RTL8211E), 2026-07-04 — REQUIRED (with IOB-packed
TX FFs):** the phase was never the *silence* bug (that was the cut-through/starvation issue
+ missing `--coherent-dma` — see `docs/findings/kl-eth-tx-debug.md`), but once the GMII TX launch
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
campaign's L2 experiments (see `CHANGELOG.md` / `docs/findings/`). **Not
applied by `apply.sh`** — apply it manually (`patch -p1 -d <pythia/litex
tree>`) only when building VexiiRiscv with a non-default L2. (Yes, the file
shares the `0002-` prefix with the LiteEth patch — they target different
trees.)

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

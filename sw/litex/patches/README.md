# LiteX BIOS patches

Small additions to the **LiteX BIOS** that live in the LiteX source tree (vendored or
pip-installed), shipped here as patches and applied in place by `apply.sh`.

## `0001-milan-linux-flashboot.patch` — QSPI Linux flash-boot

Adds a `linux_flashboot` BIOS boot method that copies the Linux boot images out of the
memory-mapped QSPI flash into DRAM, so a boot needs **no** (or, for the partial manifest,
much smaller) serial upload — the "gain time" path. See [`../../docs/QSPI_FLASHBOOT.md`](../../docs/QSPI_FLASHBOOT.md).

Touches three BIOS files (all in `litex/soc/software/bios/`):

| file | change |
|------|--------|
| `boot.c`  | broaden the flash-image-helper guards to also compile under `MILAN_FLASHBOOT_ENTRY` (without setting `FLASH_BOOT_ADDRESS`, since the BIOS itself is *not* booted from flash), and add `linux_flashboot()` |
| `boot.h`  | declare `linux_flashboot(void)` |
| `main.c`  | register it with `define_boot_method(milan_flash, …, -10)` so it runs **before** serialboot (which stays as the fallback) |

It is driven entirely by the `MILAN_FLASHBOOT_*` constants that `milan_soc.py --with-spiflash`
emits into `generated/soc.h`. With no such constants the added code compiles to nothing, so
the patch is inert on non-Milan builds.

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

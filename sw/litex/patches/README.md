# LiteX ecosystem patches

`apply.sh` applies the small product-required deltas to the active LiteX
environment. It discovers each source tree through the selected Python
interpreter and is safe to run again after dependency updates.

The series contains:

- `0002-liteeth-gmii-tx-clk-invert.patch`: expose the AX7101 GMII transmit
  clock phase control used by `milan_soc.py --gtx-tx-invert`.
- `0004-vexiiriscv-baremetal-variant.patch`: add the cacheless, machine-mode
  RV32I Vexii variant and publish an MMU constant only when one exists.
- `0005-vexiiriscv-cacheless-litex.patch`: connect the cacheless instruction,
  data, and DMA paths to the LiteX bus fabric.

Usage:

```sh
./apply.sh
./apply.sh --reverse
PYTHON=/path/to/venv/bin/python3 ./apply.sh
```

If an upstream revision changes a patched hunk, `apply.sh` stops at that patch.
Refresh the diff against the newly pinned source tree, then rerun the builder's
toolchain-patch gate before committing it.

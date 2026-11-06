# Why every MDIO transaction doubled at dd764ed7, and the fix

Scratch evidence for F3 (#840 round 2). Nothing here is committed to the tree.

## Per-transaction probe

`probe-instrumentation.diff` adds two `printf` lines to a scratch copy of
`tb/verilator/fw_service_budget/phy.hpp`: one per completed MDIO transaction (op 6 read, op 5
write, register, start cycle, length in system cycles) and one per complete poll (retired
heartbeat entry to publication). The simulator is otherwise the harness's own build.

- `probe-dd764ed7-1x1.txt`: the round-1 1x1 service build (firmware of d62417f1, the same file as
  dd764ed7), the first 400 s of wall time of the `all` plan. Every transaction, reads included, takes
  16,855 to 16,957 cycles; the discovery poll is 246,869 cycles and a steady poll 88,839.
- `probe-inlined-1x1.txt`: the same plan on a scratch build of dd764ed7 with only the
  `always_inline` change of c06150b4, the first 420 s. Reads take 8,649 to 8,795 cycles, writes 9,464 to 9,474;
  the discovery poll is 131,480 cycles and a steady poll 46,470.

The base oracle's largest transaction is 8,793 cycles (8x8) and 8,789 (1x1), so the reads are
back at the base figure.

## Compiled code

Objects compiled by the BIOS build's own `Makefile` and flags (`-march=rv32i2p0`, the product
toolchain), disassembled; labels and comments stripped.

- `phy_mdio_read-604899c0.s`: the base. `phy_mdio_bit()` has one caller and is inlined; the
  preamble loop is six instructions (`sw`, `lw`, `sw`, `sw`, `addi`, `bnez`), one taken branch.
- `phy_mdio_read-dd764ed7.s`, `phy_mdio_bit-dd764ed7.s`, `phy_mdio_write-dd764ed7.s`: the new
  `phy_mdio_write()` is a second caller, so `phy_mdio_bit()` is no longer inlined. Each bit is a
  `jal` to an eleven-instruction function and its `ret`: three taken branches per bit. The core
  is cacheless (`sw/litex/milan_soc.py`, "the product gate below accepts only cacheless RV32
  VexiiRiscv"), so each taken branch refetches over the bus.
- `phy_mdio_read-inlined.s`, `phy_mdio_write-inlined.s`: with `always_inline`. The read is
  byte-identical to the base's 65 instructions (`cmp` exit 0).

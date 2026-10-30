# Sampling ledger: docs/integration/PORTING_GUIDE.md

Every numeric or normative statement, with the mechanical checks and the manual verdict.

| Line | Kind | Statement | Mechanical | Verdict |
|---:|---|---|---|---|
| 3 | sentence | Port the LiteX board shell around the vendor-neutral `milan_datapath`; do not fork the protocol/media RTL. | - | policy |
| 23 | row | \| audio I/O \| conceptually \| map I2S/TDM pins and clock ownership \| | - | policy: porting table |
| 24 | row | \| LiteX shell \| no \| clock/reset, DDR3, QSPI, UART, part, speed grade \| | - | policy: porting table |
| 28 | sentence | The Milan RTL uses SystemVerilog and vendor-recognized `ASYNC_REG` attributes, but no required Xilinx primitive. | - | ok: git grep of hdl/ (tb excluded) finds no MMCME2, PLLE2, BUFG, IDDR/ODDR, IBUFDS, xpm_ or RAMB instance; ASYNC_REG attributes are used (hdl/common/cdc_handshake.sv) |
| 28 | sentence | Replace those through the destination toolchain while retaining the same logical clocks, reset release, packet convention, and audio timing. | - | ok: git grep of hdl/ (tb excluded) finds no MMCME2, PLLE2, BUFG, IDDR/ODDR, IBUFDS, xpm_ or RAMB instance; ASYNC_REG attributes are used (hdl/common/cdc_handshake.sv) |
| 36 | sentence | Assert resets asynchronously only where the wrapper documents it and release them synchronously in each destination domain. | - | policy |
| 45 | sentence | Constrain every external and generated clock at its actual frequency. | - | policy |
| 58 | sentence | Keep reset synchronization registers together and exclude only the intended asynchronous assertion arcs. | - | policy |
| 63 | sentence | Translate every CDC exception to the destination syntax. | - | policy |
| 63 | sentence | A crossing is not safe because a tool failed to time it; the implementation primitive and the constraint must agree. | - | policy |
| 70 | sentence | A generic synthesis pass proves portable RTL structure, not board electrical correctness. | - | policy |
| 93 | item | Define clocks, resets, MAC byte order, audio pins, and flash layout. | - | policy |

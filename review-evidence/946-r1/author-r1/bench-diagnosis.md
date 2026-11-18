# #946 (F-G1) bench diagnosis, from the S12b gating lane [A783], 2026-11-18 18:18

Copied from `s12b-a783/gating/HANDOFF.md` section 11.5. The evidence receipt is
`s12b-a783/gating/receipts/8x8/fg1-bench-diagnosis/reachability.txt`. F-G1 itself (the cause, read from the RTL, with
file:line) is in the same section, just above.

**F-G1 bench diagnosis (#946, the manager's request of 18:3x): NOT RUN, because the bench cannot reach the window
without a new image.** Receipt: `receipts/8x8/fg1-bench-diagnosis/reachability.txt` (18:18, read only, nothing
written to the board). Requested: bind M's stream to input 1 alone; write input 1's context FMT_LO/FMT_HI by hand to
`0205022002006000`; check FRAMES_RX rises and UNSUPPORTED_FORMAT stops; then add input 0 and check F-G2. On the
installed 8x8/1if image (`0b3ea432...`, clone `73272666`):
- **The window is on the soft core's bus,** so it is the CPU that could write it. csr.csv:
  `memory_region,milan_csr,0x90000000,65536,io`. The per-stream window is `milan_csr.sv:1018-1030`:
  - `A_STRM_SEL` 0x800 (`[3:0]` index, `[8]` 0 = listener);
  - `A_STRMW_FMT_LO` 0x824 and `A_STRMW_FMT_HI` 0x828, "current stream format (LCTX w2/w3)";
  - `A_STRMW_CTRL` 0x810 (`[0]` en).

  The hand write would be: SEL = 0x001, then FMT_HI = 0x02050220 and FMT_LO = 0x02006000, at 0x90000800 / 0x90000828
  / 0x90000824. Writes are held until the engine accepts them (`milan_csr.sv:519-521`).
- **Nothing on the bench can make the CPU issue that write:**
  - **Console:** the split console runs exactly two commands, `milan_status` and `milan_gettime`, and refuses any
    other line (`sw/firmware/ctrl/plat/ctrl_plat_console.c:143-151`). There is no memory read or write command.
  - **Bus bridges:** none. The CSR blocks are ctrl, identifier_mem, milan_mac, spiflash, timer0, uart, ctrl_reboot,
    ctrl_mbx_dma and ctrl_mbx; no jtagbone, uartbone or etherbone.
  - **JTAG:** the soft core netlist (`VexiiRiscvLitex_191cc593...v`) has no JTAG or debug module, and the top level
    has no BSCANE2. The FPGA JTAG reaches only configuration and the flash, and a warm JTAG reload is excluded anyway.
  - **Firmware:** the only writer the CPU runs is the control firmware, and it never writes the window (no reference
    in `sw/firmware/ctrl`).
- **Not done, per the instruction:** no image built for it. F-G2's recheck depends on the same write, so it is not
  run either. The board was not touched (no bind, no write, no power cycle).
- **What a diagnostic image would need** (for the fix lane, not built here): any one of
  - a console write command for the `milan_csr` region;
  - a Wishbone bridge;
  - firmware that writes the three words above on a bind.

  The check would then be the one requested: input 1 alone, FRAMES_RX rising and UNSUPPORTED_FORMAT +0; then inputs 0
  and 1 together for F-G2.


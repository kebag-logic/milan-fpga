# REVIEW READY: usbnet (FPGA side), #1011 + #1018

Branch `1011-usbnet` in $LANES/usbnet-1011, from dev-soft-core c34e7d8b06, head
`cc49123d2db1e01e80859efa10f8da43a01344ef`, 8 commits, unpushed. Nothing posted.

Arty integration, local only: `1011-usbnet-arty-int`, head `660ed296780e3ff1e5cdc88b9b1ce32d08e94b49`, in
$VALIDATION_STORAGE/usbnet-a855/int. It is this branch merged onto the Arty split merge 49b534fc9 (A829's local merge of
PR #1004 with dev-soft-core).

The selected image is $VALIDATION_STORAGE/usbnet-a855/route/AltSpreadLogic_high-final2/:
- bitstream sha256 `ddddd0f03d79291b033662b6872e8cc99d92256780a7732d0a6ec1909f62e77f`;
- control firmware `18c9b4046214a60b0e7168e183473bb20fa950f52d999efeca47e664fbbf9771`, the Arty product with the
  LED code.

It was not flashed.

## What to review

| Area | Files |
|---|---|
| Rules, receive copy, transmit check and rate limit, injection arbiter, top, LEDs | `hdl/usbnet/KL_usbnet_{pkg,rx_copy,tx_inject,tx_arb,tap}.sv`, `hdl/usbnet/KL_status_leds.sv` |
| Arty SoC attachment (`--usb-net`; LEDs always on the Arty), pinned CSR page | `sw/litex/usbnet_soc.py`, 4 hook sites in `sw/litex/milan_soc.py` |
| Firmware LD2/LD3, compiled only with the register | `sw/firmware/ctrl/plat/ctrl_plat_leds.h`, `ctrl_plat_main.c`, `ctrl_plat_gen.py` |
| Firmware tests and defect rows | `test_aecp.cpp` (`Leds.*`), `aecp_arms.py` (Arty arm), `aecp_leds_mutants.py`, `aecp_mutants.py` |
| Benches and planted defects | `tb/verilator/usbnet/` |
| Contract for the USB device firmware | `docs/design/USB_NET_PATH.md` |

## Evidence (receipts/INDEX.md)

- **Benches.** The tap bench passes 9 cases; the LED bench passes. **43 of 43** RTL planted defects are caught,
  each by its named check, at the head.
- **Firmware.** The `Leds.*` tests pass on the shipping, dev-soft-core Arty and Arty split models. They set LD3's
  three cases over AECP SET_CLOCK_SOURCE. **8 of 8** firmware defect rows are caught, and the plant-table control
  passes. Every AECP arm passes, **26 of 26**. Taken at 7e4cdddc76; no firmware file changed after it.
- **Shaper suites.** CBS, shaping core and queues pass, unchanged.
- **ALINX identity at the head.** ax7101, ax8x8 and ax7a200t SoC exports are identical with and without the change,
  over 3837 to 3839 files and 136 RTL sources each, with a same-tree control. The 1x1 and 8x8 product firmware
  images and map headers are byte-identical.
- **Arty route.** AltSpreadLogic_high: WNS 0.601 ns, WHS 0.050 ns, every corner, 0 failures. ExtraTimingOpt also
  meets every corner (0.072 ns).
  - Cost against the same recipe without the change: +1221 LUT, +832 FF, +2 RAMB36. Of that, the tap is 1019 LUT,
    791 FF and 2 RAMB36.
  - The image identity gate passes.
- **Gates.** 17 repository gates pass at the head.

## Open owner decisions (in PR-BODY.md)

1. **The computer cannot reach this device itself.** The device's own frames never reach the copy, and the
   computer's frames never reach the device's receiver. Fixing that needs a local path both ways, beyond #1011's
   text.
2. **Bus threads.** All four threads of the 2-bit slave-FIFO address are already assigned in usb-audio's design.
3. **MVRP.** MVRP is 01-80-C2-00-00-21, outside the 0x block the issue names; the -2x block is excluded as well.

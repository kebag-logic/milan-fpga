# usbnet (FPGA side) A855: #1011 + #1018

**Status 10:35: REVIEW READY `cc49123d2db1e01e80859efa10f8da43a01344ef`. ETA: none, done. Desk only: no Arty, no
bench, no flash. Nothing pushed or posted.**

- **Branch.** `1011-usbnet` in $LANES/usbnet-1011, from dev-soft-core c34e7d8b06, 8 commits. It is a fresh
  clone; no earlier session had worked there.
- **Arty integration, local only.** `1011-usbnet-arty-int` at 660ed29678 in $VALIDATION_STORAGE/usbnet-a855/int: this
  branch merged onto A829's Arty split merge 49b534fc9. dev-soft-core's own Arty recipe no longer elaborates (its PLL
  has no configuration), so the routed Arty image is the split one.
- **Image.** $VALIDATION_STORAGE/usbnet-a855/route/AltSpreadLogic_high-final2/, bitstream ddddd0f0…, control firmware
  18c9b404… (the Arty product with the LED code). It was not flashed.

## Done

1. **#1011 tap** (`hdl/usbnet/`, Arty only behind `milan_soc.py --usb-net`, `sw/litex/usbnet_soc.py`).
   - **Receive copy.** Unicast to the computer, plus broadcast and multicast, with these excluded: AVTP stream
     subtypes (untagged or behind one tag), 01-80-C2-00-00-0x and -2x, two tags, and no computer attached.
   - **Transmit drops.** Another source than the computer's, a reserved destination, an AVTP stream subtype, two
     tags, a priority above 1, and a bad length.
   - **Injection.** Best effort only: injected at the MAC core input, strictly below every datapath frame, with at
     most one injected frame ahead of a datapath frame. 10 Mb/s token bucket. The REBOOT frame-end account excludes
     the computer's frames.
   - **Verification.** Benches with 43 of 43 planted defects caught. The existing shaper suites pass unchanged.
   - **Cost and timing.**
     - +1221 LUT, +832 FF, +2 RAMB36 for the whole change; of that, the tap is 1019 LUT, 791 FF and 2 RAMB36.
     - Every corner met: WNS 0.601 ns and WHS 0.050 ns with AltSpreadLogic_high. ExtraTimingOpt also meets every
       corner, at 0.072 ns. The pristine baseline is 0.433 / 0.050 ns.
2. **#1018 LEDs.**
   - **The LEDs.** LD0 is link with an activity blink (40 ms off, 60 ms hold). LD1 is the USB 3.0 path, from the
     tap. All four use the green channel at 16/256 duty.
   - **LD2 and LD3.** The status register `status_leds_ctrl`, written every 250 ms by the control firmware
     (`plat/ctrl_plat_leds.h`), from the AECP core's state. LD3 is checked over AECP SET_CLOCK_SOURCE in all three
     cases, on the shipping, dev-soft-core Arty and Arty split models. 8 of 8 firmware defect rows are caught, and
     26 of 26 AECP arms pass.
   - **LD1's signals for the USB device firmware lane** are in `docs/design/USB_NET_PATH.md` sections 4 and 5:
     - a HOST record (address plus a state word, bit 0 SuperSpeed) at every connection and every second;
     - a DETACH record on disconnection;
     - bus alive, from the slave-FIFO master.
3. **ALINX identity.**
   - All three ALINX recipes' SoC exports are identical, with every RTL source each Vivado script reads identical by
     content.
   - The 1x1 and 8x8 product firmware images are byte-identical.
   - The existing CSR addresses on the Arty are unchanged: rows are only added, and the LED bank is pinned to page 27.

## Not done, and why

- **Bench items.** #1011 acceptance 3 and #1018 acceptance 4 need the bench, so PR-BODY.md says "Relates to" for both
  issues.
- **Bus side.** It is terminated in this image: no slave-FIFO master is in this repository, so LD1 stays off until
  usb-audio's master is bound to `usbnet_bus`. The tap is DONT_TOUCH, so its cost is real.
- **Arty service census not re-run.** The firmware's LED tick is a new periodic task, and A829's 145-case census was
  not re-run with it. It is owed on the integration.

## Owner decisions needed (written up in PR-BODY.md)

1. **The computer cannot see or control this device itself, only its peers.** The device's own transmitted frames
   never reach the copy, and the computer's frames to the device never reach the device's receiver. #1011's text
   covers neither; a local path both ways is needed.
2. **GPIF threads.** usb-audio's design assigns all four threads of the 2-bit address. Two network threads need a
   third address line or shared threads. The FPGA side is thread-agnostic.
3. **MVRP and MMRP** use 01-80-C2-00-00-21 and -20, outside the 0x block the issue names. The -2x block is excluded
   too. The tagged-priority drop is also beyond the issue's literal text: it keeps the computer's frames in best
   effort at the next bridge.

## Notes for the next lane and the manager

- **Disk-cleanup log.** Several of this lane's own scratch removals under $VALIDATION_STORAGE/usbnet-a855 were made
  before being logged. They are recorded in disk-cleanup.log marked "LOGGED LATE". Later removals were logged first.
- **Observation, not this lane's.** The Arty split image drives the IDENTIFY LED (`user_led0`) with a constant 0.
  Synthesis warns about it in A829's round-5 image too.
- **A829's round-6 route.** Its ExtraTimingOpt route at 49b534fc9 appears to have died; its log stops at 07:59.
  This lane routed that same pristine head as its own baseline (receipts/arty-route-baseline*).
- **Bench warning.** The tap bench prints one width warning, from its `-G` override of the 64-bit rate parameter.
  It is benign and left as is.
- **Merging into dev-soft-core.** The merge will need `scripts/docs_inventory.py --write` re-run if the audit page
  conflicts; it auto-merged on the integration.

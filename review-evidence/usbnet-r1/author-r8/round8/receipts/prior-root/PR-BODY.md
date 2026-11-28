## Description

The FPGA side of the USB network path (#1011), with the Arty A7's status LEDs LD0 to LD3 (#1018), for the Arty build only.
The attached computer is its own station behind the device, as the owner decided on #1011: control traffic only, its
own locally administered address, no gPTP or MSRP mirroring. No AVTP stream frame crosses in either direction.

**Receive copy.** The frames the device itself takes are copied toward the computer. A frame is copied when it is
unicast to the computer, or when it is broadcast or multicast. AVTP stream subtypes are never copied (IEEE 1722-2016
Table 6: subtype bit 7 clear, untagged or behind one tag). Neither are 01-80-C2-00-00-0x and the MRP block
01-80-C2-00-00-2x. The issue names MVRP among the excluded protocols, and MVRP and MMRP use -21 and -20 (IEEE
802.1Q-2018 Table 10-1). The copy only observes: the device's reception is unchanged, and unicast to the device
stays with it. A frame that finds no room is dropped whole and counted.

**Transmit injection.**
- **Drops.** A frame from the computer is dropped whole when it has another source than the computer's address, a
  reserved destination, an AVTP stream subtype, two tags, a tag with priority above 1 (IEEE 802.1Q-2018 Table 8-5;
  best effort at the next bridge too), or a bad length.
- **Where it enters.** Frames enter at the MAC core's transmit input, after the datapath's store-and-forward FIFO.
  - The datapath wins every arbitration.
  - An injection is granted only with no datapath frame waiting and none in the MAC.
  - A datapath frame waits at most the one injected frame already granted: the lower-priority frame IEEE 802.1Q-2018
    Annex L and IEEE 802.1BA-2011 6.5 budget, 123.4 us at most on the Arty's 100 Mb/s link.
  - Without injection the datapath passes with no added clock.
- **Rate limit.** A 10 Mb/s token bucket on wire octets, with a 3200-octet burst.
- **The REBOOT account.** The AECP REBOOT sequence counts frame ends at the PHY. The arbiter leaves the computer's
  frames out of that count (IEEE 1722.1-2021 7.4.43; [REBOOT_RESET.md](docs/design/REBOOT_RESET.md)).

**Bus records.** Each record is a 16-bit length header with a 4-bit type: FRAME, HOST (the computer's address and
USB state, sent at every connection and every second) and DETACH. Records toward the computer end with `last`.
[USB_NET_PATH.md](docs/design/USB_NET_PATH.md) is the contract the USB device firmware works to. LD1's inputs are
there too: bus alive, address held, a HOST record at most 3 s old, SuperSpeed.

**LEDs.** Green channel only, PWM duty 16/256.
- **LD0.** Link up; each frame in either direction blinks it off for 40 ms, followed by a 60 ms hold.
- **LD1.** The USB 3.0 path, from the tap.
- **LD2 and LD3.** A status register the control firmware writes every 250 ms, from the AECP core's own state:
  - LD2: a STREAM_INPUT bound with its media locked, or a STREAM_OUTPUT with a registered Listener.
  - LD3: CLOCK_DOMAIN 0's source, as SET_CLOCK_SOURCE set it, is INTERNAL; or it is INPUT_STREAM, with that input
    bound and media-locked and the domain locked; or it is EXTERNAL with the domain locked.
- **Compiled only where it exists.** The firmware compiles the LED code only where the SoC has the register.

**Registers.** The LED bank is pinned to its own CSR page, and the tap's registers follow every other MAC register.
No existing address moves.

## Linked Issue / roles

Relates to #1011 (its bench item 3 is not done; desk only).
Relates to #1018 (its board item 4 is not done; desk only).
Relates to kebag-logic/usb-audio#5 (the USB device firmware side) and #878 (the Arty split image).

## Validation

- **USB network path Verilator suite: 9 cases PASS.**
  - Every receive class (26 frames, with and without a computer attached), the transmit drops (21 frames plus an
    unknown record), the host record and LD1's inputs, and a full buffer.
  - The rate limit: 799,973 b/s steady against 800,000 at the scaled clock.
  - Best effort only. 120 class A-like datapath frames run with the computer saturating its rate limit, with and
    without a stalling MAC:
    - the datapath wins every arbitration, including a directed contention case;
    - no injected frame shares the MAC with a datapath frame;
    - the worst datapath wait is 2314 / 2337 clocks, against a bound of one injected frame;
    - every datapath frame arrives intact and in order;
    - the frame-end toggle counts the 120 datapath frames only.
- **LED suite PASS:** each LED through each state, the blink and its hold, the duty.
- **Planted defects: 43 of 43 caught, each by its named check** (one per filter class, drop, rate rule, arbitration
  rule and LED rule).
- **Firmware.** The AECP arm's `Leds.*`: the clock source is set over AECP (SET_CLOCK_SOURCE) internal, following a
  flowing stream, and following a stopped stream, plus LD2's rules. They pass on the shipping model and on the Arty
  model. All 8 LED defect rows are caught, and the campaign's plant table claims every test. The full application
  arm passes (186 tests).
- **The stand-alone shaper suites** (credit-based shaper, shaping core, queues) pass unchanged.
- **The Arty split image with this change routes.** The recipe's argv, with `--usb-net`, through the Vivado slot
  wrapper. Two directives, both met; AltSpreadLogic_high is selected.
  - Every corner is met: WNS 0.601 ns (slow), WHS 0.050 ns (fast), 0 failing endpoints, 0 routing errors.
    ExtraTimingOpt also meets them, at WNS 0.072 ns.
  - Against the same recipe routed without this change (WNS 0.433 ns, WHS 0.050 ns): +1221 LUT, +832 FF,
    +2 RAMB36 (78 to 80 block-RAM tiles), +415 slices.
  - Of that, the tap is 1019 LUT, 791 FF and 2 RAMB36: receive copy 339/278/1, transmit check 585/479/1,
    arbiter 95/34/0. The LEDs, the registers and the glue are the remaining +202 LUT and +41 FF.
  - The control image with the LED code keeps the block-RAM plan, 44.5 of 56 tiles, and the same flash map. The
    image identity gate passes on the selected image.
- **ALINX identity.**
  - Every file the three ALINX recipes' SoC exports write is identical with and without this change. The comparison
    blanks date stamps and treats the generator's comment tree as a multiset; a same-tree control run shows that
    tree's order varies.
  - All 136 RTL sources the Vivado scripts read are identical by content.
  - The 1x1 and 8x8 product firmware images link byte-identical.
- **Repository gates pass:** SystemVerilog, Python and C++ idiom, port contracts, RTL lint, wire accountability,
  source lists, docs check and the documentation inventory.

## How to reproduce

- `make -C tb/verilator/usbnet` (both benches) and `make -C tb/verilator/usbnet mutants` (the planted defects).
- `python3 sw/firmware/ctrl/test/aecp_arms.py --output DIR --core --filter 'Leds.*' --config configs/<model>.yaml`.
- **The Arty image.** The Arty split recipe's argv (`endstation_builder.emit_soc_argv` of
  `configs/endstation_arty_split.yaml`, once #1004 is merged), plus `--usb-net`. The control image is linked
  against that SoC's `csr.csv` (`sw/firmware/ctrl/test/ctrl_plat_image.py`).

## Limitations and remaining work

- **The bus side is terminated in this image.** No slave-FIFO master is in this repository yet; the one in
  kebag-logic/usb-audio is to be bound to `usbnet_bus`. Until then, LD1 stays off. The tap carries DONT_TOUCH, so the
  stated cost is the whole path's.
- **Decision needed: the computer cannot reach the device itself.** As #1011 is written, the copy reads the device's
  receive stream and the injection goes to the wire. The device's own frames (its ADP advertisements, its AECP
  responses to the computer) never reach the computer, and the computer's frames to the device never reach the
  device's receiver. A controller on the computer therefore sees and controls the peers, but not this device.
  Closing that needs a local path both ways: the datapath's transmit stream through the same copy rule, and the
  computer's frames to the device, or to a group, merged into the device's receive stream. That is not in #1011's
  scope.
- **Decision needed: the bus threads.** The usb-audio design assigns all four threads of the 2-bit slave-FIFO address
  (capture, status, trace, playback), and the bring-up harness wires A0 and A1 only. The two network threads therefore
  need either a third address line or shared threads. The FPGA side carries no thread number.
- **Owed on the Arty integration.** The firmware's LED tick adds one periodic task. The Arty split image's service
  census (#878) has not been re-run with it.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied, including the bench items
- [x] Changed behavior has self-checking tests
- [ ] Full required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] Changed contracts are documented
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated
- [ ] Post-merge containment is checked before the Issue moves to Done

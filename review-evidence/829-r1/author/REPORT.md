# Arty gPTP at 100 Mb/s (#829): what the 1,509 ns is, and the runtime correction

**The Arty now syncs to the bench grandmaster and carries a stream from the reference peer, both through the inline tap.** asCapable and sync held for 10 min 40 s. That run used the tap compensation, so its synchronized offset is wrong by a known amount: about 233 ns, measured on the same capture.

**Two things stay open.** The check with the tap out needs a person at the bench, and the split between ingress and egress is assigned, not measured.

All figures below are from the final image at `829-bench` `b474b534`, unless a row says otherwise. The first image, `0a1928bd`, gave the same results: its rows are the `m-*` receipts.

## Results

| # | Question | Answer |
|---|---|---|
| a | Does the plane need a link event to start? | **No.** It measured by the first or second reading after each of 2 flashes and 4 resets. Not a third fault |
| b | Is any of the 1,509 ns a logic error? | **No term is.** The terms add to 1,524 to 1,544 ns. 15 to 35 ns stays unexplained, with the terms the larger |
| c | One image, runtime correction | Done behind `gptp.latency_writable`, off on the AX7101 |
| d | True pair, 1409/100 | Arty 894.8 ns, zero 890.6 ns, `PDELAY_NS` 888.2 ns. asCapable 0 under the tap, as expected |
| e | Tap compensation, 1409/581 | `PDELAY_NS` 650 to 654 ns, asCapable 1, sync 1, grandmaster the bench's. Stream connection passed |
| f | Owed with the tap out | Not run, see [What is still owed](#what-is-still-owed) |
| g | AX7101 route | Passes its record, rc 0. With the writable RTL present and the key off, the routed netlist is the same: all 126 checksums match |
| h | Bench as left | Tap compensation written; a reset restores 1409/100 |

## Before and after

Every row is the same method: `docs/integration/BOARD_PORTING_AX7101.md` section 6, on the tap, with the console polled over the same capture. "Sum" is Arty less zero, plus the pair applied. `PDELAY_NS` leaves out the two polls after a write.

| Setting | Tap | Exchanges | Arty, sd | Zero, sd | Arty - zero | Sum | PDELAY_NS mean (range) | GPTP_LAT | ASCAP | SYNC |
|---|---|---:|---:|---:|---:|---:|---|---|---|---|
| Uncalibrated fixed image (scratch probe build), measured before this lane | out | status only | | | | 1504 (2 x 752) | 748 to 756 | | 1 | 1 |
| The same image | in | 129 | 2368.4, 33.2 | 859.0, 22.7 | 1509.4 | 1509.4 | 1620 | | 0 | 0 |
| final image, written 0/0 (`f-01-pair-0-0`) | in | 128 | 2394.1, 28.0 | 889.5, 23.5 | 1504.6 | 1504.6 | 1645.3 (1626 to 1664) | `00000000` | 0 | 0 |
| 400/0, sum 400 (`f-02-pair-400-0`) | in | 69 | 1993.8, 33.3 | 886.7, 22.6 | 1107.1 | 1507.1 | 1446.8 (1436 to 1464) | `01900000` | 0 | 0 |
| 0/400, sum 400 (`f-03-pair-0-400`) | in | 69 | 1996.6, 25.6 | 893.3, 24.0 | 1103.3 | 1503.3 | 1451.7 (1426 to 1462) | `00000190` | 0 | 0 |
| 800/400, sum 1200 (`f-04-pair-800-400`) | in | 69 | 1192.0, 32.0 | 890.3, 24.2 | 301.7 | 1501.7 | 1048.2 (1034 to 1064) | `03200190` | 0 | 0 |
| reset value, right after the flash (`f-00-after-flash-reset-pair`) | in | 49 | 879.2, 32.2 | 888.3, 22.5 | -9.1 | 1499.9 | 897 (879 to 919) | `05810064` | 0 | 0 |
| pair from `f-01`'s capture, 1405/100 (`f-05-pair-from-math`) | in | 68 | 884.5, 30.6 | 890.3, 23.5 | -5.8 | 1499.2 | 896.7 (888 to 906) | `057d0064` | 0 | 0 |
| **true pair**, 1409/100, the reset value (`f-06-true-pair-reset-value`) | in | 88 | 894.8, 33.0 | 890.6, 23.7 | 4.2 | 1513.2 | 888.2 (874 to 904) | `05810064` | 0 | 0 |
| **tap compensation**, 1409/581 (`f-07-tap-comp`) | in | 68 | 402.7, 35.0 | 892.8, 21.9 | -490.1 | 1499.9 | 650.2 (631 to 665) | `05810245` | 1 | 1 |
| the same, first 5 min 20 s (`f-10-tap-comp-sync-a`) | in | 316 | 407.5, 29.7 | 890.7, 22.6 | -483.2 | 1506.8 | 654.0 (631 to 675) | `05810245` | 1 | 1 |
| the same, next 5 min 20 s (`f-11-tap-comp-sync-b`) | in | 316 | 403.9, 31.9 | 890.9, 22.1 | -487.0 | 1503.0 | 653.2 (639 to 667) | `05810245` | 1 | 1 |
| bench as left (`bench-left`) | in | 29 | 406.3, 30.3 | 891.8, 20.2 | -485.5 | 1504.5 | 664.2 (653 to 669) | `05810245` | 1 | 1 |

| Row against `f-01`, same link-up | X written | Arty moved, predicted -X | Sum | PDELAY_NS moved, predicted -X/2 |
|---|---:|---:|---:|---:|
| `f-02-pair-400-0` | 400 | -400.3 | 1507.1 | -198.5 |
| `f-03-pair-0-400` | 400 | -397.5 | 1503.3 | -193.6 |
| `f-04-pair-800-400` | 1200 | -1202.1 | 1501.7 | -597.1 |
| `f-05-pair-from-math` | 1505 | -1509.6 | 1499.2 | -748.6 |
| `f-06-true-pair-reset-value` | 1509 | -1499.3 | 1513.2 | -757.1 |
| `f-07-tap-comp` | 1990 | -1991.4 | 1499.9 | -995.1 |
| `f-10-tap-comp-sync-a` | 1990 | -1986.6 | 1506.8 | -991.3 |
| `f-11-tap-comp-sync-b` | 1990 | -1990.2 | 1503.0 | -992.1 |

| Link-up | Image | Pair | Arty | Zero | Sum |
|---|---|---|---:|---:|---:|
| 14:05 | scratch probe | none | 2368.4 | 859.0 | 1509.4 |
| 14:24, same link-up | scratch probe | none | 2373.8 | 855.9 | 1517.9 |
| 14:25, reset | scratch probe | none | 2415.2 | 932.0 | 1483.2 |
| 15:29, flash 1 | `0a1928bd` | 0/0 | 2396.2 | 924.6 | 1471.6 |
| 15:34, reset | `0a1928bd` | 0/0 | 2375.1 | 918.0 | 1457.1 |
| 15:35, reset | `0a1928bd` | 0/0 | 2397.0 | 890.6 | 1506.4 |
| 15:36, reset, measured at 16:01 | `0a1928bd` | 0/0 | 2385.6 | 877.2 | 1508.4 |
| 16:28, flash 2 | final | 0/0 | 2394.1 | 889.5 | 1504.6 |

**The response is linear.** On one link-up, every written correction moves the Arty's difference by the value written, and `PDELAY_NS` by half, inside the spread of about 30 ns per exchange and 3 to 5 ns per row. The ingress and egress words move it equally, one at a time.

**The written 0/0 row matches the uncalibrated one, within the link-up scatter.** Its sum is 1504.6 ns against 1509.4 ns. The Arty's and the zero's figures each moved, because the tap's transit moved. In simulation the writable build at 0/0 is exact: t2 is the PHC at the first beat, and t3 is 3770 ns below the record's PHC.

**The two uncalibrated rows came from a scratch probe image, not the plain fix.** That image had removed the peer delay clamp, and its `GPTP_LAT` read a probe word. That is why those status lines print `GPTP_LAT=b1b10000` on a build with no correction. The peer delay arithmetic is the same.

### A finding on the method: one zero does not cover both directions

**The sum moves by up to about 60 ns between link-ups, seven of them on three images.** On one link-up it holds still, inside about 14 ns, which is its spread per row.

The zero measures the tap's Arty-to-switch transit, while the Arty's difference carries the switch-to-Arty transit. Each link-up sets those two separately, so one link-up's sum is only good to about 30 ns either way.

The direct reading with the tap out, 2 x 752 = 1,504 ns, has no tap in it. So I kept 1,509 ns as the board's sum: it is the measurement of record, and it sits 5 ns from that reading. `docs/integration/BOARD_PORTING_AX7101.md` on `829-bench` now tells a port to measure several link-ups.

## a. Fault 3 is not a fault in the plane

**It starts without any special event.** On this link every start measured:

| Start | Image | First `PDELAY_NS` read | Receipt |
|---|---|---|---|
| Console reset | scratch probe | 0 at 9 s, 1,664 at 12 s | `fault3-reset-1` |
| Flash | `0a1928bd` | 873 | `m-00-after-flash-reset-pair` |
| Console reset, three times | `0a1928bd` | measured each time | `m-11`, `m-12`, `m-13` |
| Flash | final | 893 | `f-00-after-flash-reset-pair` |

Each of those resets is itself a link event: the switch's Pdelay_Req sequence restarts near 100 across one. But link events did not cure the earlier state either: the three flashes of a fixed image before 13:47 all read 0, and each flash restarts the switch's sequence the same way.

**What differed is the link the owner re-plugged at 13:47.** Before it, the MAC never received the frames:

| Before the tap, same image, 120 s window | Rate | With the tap | Rate |
|---|---:|---|---:|
| Pdelay_Resp events | 1.01/s | Pdelay_Resp events | 1.00/s |
| Pdelay_Resp_Follow_Up events | **0** | Pdelay_Resp_Follow_Up events | 1.00/s |
| Pdelay_Req events | 0.68/s | Pdelay_Req events | 1.00/s |
| Good frames at the MAC | 3.68/s | Good frames at the MAC | 5.31/s |
| FCS errors | 0 | FCS errors | 0 |

The preamble error lane stayed equal to the good-frame count, so no frame was silently dropped there either. A follow-up that never reaches the MAC cannot be the plane's fault, and with no follow-up there is no peer delay to publish.

**In simulation**, `make -C tb/verilator/milan_dp gptp` holds the link up from before reset is released, never toggles it, and publishes peer delay on the way to asCapable. The AX7101 runs the same plane.

**Still unexplained:** why that link delivered no follow-ups and two thirds of the requests. No capture exists of it, because the tap in use then was on another link. Only the owner knows whether the re-plug also changed the switch port or the cable. It has not recurred on this link.

## b. The 1,509 ns, term by term

| Term | ns | Side | Basis |
|---|---:|---|---|
| PHY receive, first bit of `J` to `RXD` | 240 | ingress | DP83848 T2.9.2, 24 bit times |
| `RXD` to the FPGA's sampling edge | 10 to 30 | ingress | 40 ns `RX_CLK` less T2.5.2 |
| Sampling edge to the preamble checker's first octet | 85 | ingress | simulation |
| Frame check buffer | 362 | ingress | simulation |
| Gathering the 64-bit beat | 600 | ingress | simulation |
| MAC core crossing into `sys` | 63 | ingress | simulation |
| `mac_rx_cdc`, to the edge the plane stamps | 64 | ingress | simulation |
| Launch edge to the PHY's sampling edge | 40 | egress | one `TX_CLK`, DP83848 note 4 |
| PHY transmit | 60 | egress | DP83848 T2.6.1, 6 bit times |
| **Sum of the terms** | **1,524 to 1,544** | | |
| **Measured** | **1,509** | | tap, and 1,504 tap out |

**The eight-octet figure in the brief is really two terms.** The 640 ns is the 600 ns beat here, which is seven more octets and a clock, and the frame check buffer adds 362 ns on top. Together with the crossings they make the "other 870 ns", and none of it is a fault.

**The launch stamp lands where it should.** `gptp_txts` grades t1 against the pads' launch of frame octet 0, found by the delimiter on the nibbles themselves. A launch one preamble away would move the sum by 640 ns, and the sum has no room for that. In simulation the reconstruction is exactly 3,770 ns below the record's PHC.

**This corrects a figure in the document.** `GPTP_PLANE.md` said 1,164 ns to `core.source`. Measured from the sampling edge at the 80 MHz clock it is 1,110 ns, and 1,174 ns at the edge the plane stamps. Corrected on `829-mii-gptp`.

**15 to 35 ns stays unexplained.** The datasheet figures are nominal, the crossings' phases spread by about 16 ns, and I modelled no clock tree delay.

## c. The runtime correction

| Point | Behaviour |
|---|---|
| Key | `gptp.latency_writable`, off unless stated, refused unless a YAML boolean. Set on `endstation_arty_current` only |
| Key off | The elaboration constants, no flop, and `0x540`/`0x544` stay inert scratch resetting to zero |
| Key on | `[15:0]` of `0x540` and `0x544` are the applied pair. The build's pair is their reset value |
| `GPTP_LAT` (`0x7F0`) | Reads the applied pair after every write |
| Arithmetic | The same subtractor and the same point, same sign. Ingress at the frame's first accepted beat, egress where the record resolves |
| Takes effect | Within two plane clocks of the bus write |
| Clock crossing | None. The flops, the CSR block and the plane are all `axis_clk`, so the census has no new row |
| Tearing | A stamp reads one register on one edge, so it carries the old value or the new one whole |
| A write mid-exchange | Spoils that exchange at most. The next exchange carries the new pair whole, tested with the write swept through the exchange at both link shapes. The neighbor rate ratio over the window across a write of X ns is off by X over that second, for that one window |

**The split rests on the DP83848 datasheet, and it is an assignment.** Egress takes the datasheet's transmit figure plus one MII clock, 100 ns. Ingress takes the rest of the measured sum, 1,409 ns. The unexplained 15 to 35 ns could lie on either side, and a split error moves the synchronized offset by its whole value. So the offset carries an open error of at least that size, and no tap can settle it.

**The AX7101 does not move.** Off is the default and the shipping image's configurations do not state the key. Its builder export is byte-identical apart from the order of a comment tree, and a second route of the 1x1 with the writable RTL present gives every figure to the digit, with all 126 implementation checksums matching, ending `200e845fc`. Against its record, both routes read LUT 51,994 (52,012), FF 54,101 (53,707), slice 15,841 (15,780), WNS +0.236 ns (+0.440), WHS +0.036 ns (+0.036).

**Setting the pair is math.** `setpair.py` reads a capture's row, computes zero and sum, and writes the registers. For the compensation it keeps the true pair and adds extra egress only, 2 x (zero - 650).

## e. Under the tap compensation

| Check | Clause | Result |
|---|---|---|
| asCapable, 64 polls over 10 min 40 s | IEEE 802.1AS-2020 11.2 | 1 at every poll |
| Sync to the bench grandmaster | IEEE 802.1AS-2020 10.2 | `SYNC=1 TU=0`, grandmaster and parent `3cc0c6fffefe0210`, path count 2 |
| Peer delay | Milan v1.2 4.2.6.1.1 | Means 654.0 and 653.2 ns, range 631 to 675 ns, against a 650 ns target |
| Announce and Sync on the capture | IEEE 802.1AS-2020 10.2 | 637 Announce at 1/s, 5,103 Sync and Follow_Up at 8/s |
| Offset from the grandmaster | | -234.9 and -231.5 ns, sd 30, flat over the run, **wrong by construction** |
| Stream connection | Milan v1.2 5.5 | CONNECT_RX to the Arty succeeded, peer stream output to the Arty's stream input, and the disconnect succeeded |
| Reservation | IEEE 802.1Q-2022 35 | Talker Advertise relayed by the switch, then the Arty's Listener declaration 66 ms later, on the capture |
| Stream frames | | 460,354 on the capture, 7,999.8/s over 57.6 s, no sequence break |
| Arty's counters | Milan v1.2 5.5 | `MEDIA_LOCKED` 1, `MEDIA_UNLOCKED` 1 at the disconnect, `FRAMES_RX` and `TIMESTAMP_VALID` 459,823; no mismatch, late, early or uncertain frame |

**The offset is the compensation's cost, and its size was predicted.** Extra egress of 481 ns brings the delay to 650 ns against a tap transit of about 890 ns, so the plane believes the grandmaster is nearer than it is. Zero less `PDELAY_NS` predicts -237 ns; the capture reads -233 ns. Under this setting the offset says nothing about the board's true offset.

**The listener format was restored afterwards** to `0x0205022000806000`, and the peer's configuration was not changed. The connection ran with the peer as talker, so nothing was written to the peer beyond the ACMP connection request the Arty sends it.

## What is still owed

**One check needs the owner, tap out:** write the true pair, or just reset, and read `PDELAY_NS` near zero, asCapable and sync. `PDELAY_NS` should read 0 to a few tens of ns, and its negative readings publish as 0. The engine's floor is -80 ns, so the pair leaves about 60 ns of margin there. I have not run this and do not claim it.

**The offset itself** has not been measured under the true pair, because the tap breaks the delay bound whenever it is in.

## Bench as left

| Item | State |
|---|---|
| Image | `829-bench` `b474b534`, flashed 16:26, all three flash steps rc 0 |
| Pair | Tap compensation, 1409/581, `GPTP_LAT=05810245` |
| A reset restores | 1409/100, the true pair. Under the tap that means asCapable 0 until compensation is written again |
| Writing it again | Recompute after any link event, since the zero moves: `tools/setpair.py` from a fresh row |
| State at the last read, 18:20 | `SYNC=1 ASCAPABLE=1 TU=0`, `PDELAY_NS` 649 to 663, grandmaster the bench's, 1 h 40 min after the compensation was written; `receipts/bench-left-final` |
| Stream | Disconnected; listener format as found |
| Tap | Stays where it is |
| Bench lock | Free; no process of mine on any other host; my remote directories removed |
| Host | `-hupcl` stays set on the Arty's console port |

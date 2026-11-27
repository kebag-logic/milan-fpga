# USB network path and Arty status LEDs (#1011, #1018)

Audience: FPGA and firmware developers, and the USB device firmware's developers (kebag-logic/usb-audio#5).

The attached computer is its own station behind the device, with a locally
administered address that the USB device firmware generates at every
connection. The path carries control traffic only: no gPTP or MSRP mirroring
(the owner's decisions on #1011, 2026-11-25), and no AVTP stream frame in either
direction. This page states the FPGA side: the filter rules, the injection
point, the bus records the USB device exchanges with it, and the four status
LEDs of the Arty A7 build.

It is built for the Arty only (`milan_soc.py --usb-net`, `sw/litex/usbnet_soc.py`).
No other board's build carries a line of it.

## Contents

- **[1. Where it sits](#1-where-it-sits)** -- The MAC attachment and local control receiver, including their buffering and clock boundaries.
- **[2. Receive copy (frames toward the computer)](#2-receive-copy-frames-toward-the-computer)** -- Which network and device transmissions are copied, and how full buffers drop frames.
- **[3. Transmit injection (frames from the computer)](#3-transmit-injection-frames-from-the-computer)** -- Frame validation, best-effort arbitration, rate accounting and reset recovery.
- **[4. The bus records](#4-the-bus-records)** -- The shared frame and station formats, address lifetime and detach handling.
- **[5. The signals for LD1 (the USB device firmware's side)](#5-the-signals-for-ld1-the-usb-device-firmwares-side)** -- The bus and station conditions that indicate a live USB 3.0 path.
- **[6. Status LEDs (#1018)](#6-status-leds-1018)** -- Link activity, stream connection and clock-source state, with blink and PWM behavior.
- **[7. Registers](#7-registers)** -- The status, address and counter fields visible to control firmware.
- **[8. Verification](#8-verification)** -- Runnable benches, planted defects, shaper regressions and the remaining physical checks.

## 1. Where it sits

```
           MAC core RX ──► rx_dp (to the datapath) ─────────────► datapath
                              │ accepted beats (valid and ready)
                              ▼
                        KL_usbnet_rx_copy ──► up: records toward the computer
 datapath ─► tx_sf (store-and-forward) ─► KL_usbnet_tx_arb ─► MAC core TX ─► PHY
                    │ accepted device TX beats
                    └────► second KL_usbnet_rx_copy ──► up record arbiter
                                              ▲   (strict priority to tx_sf)
                        KL_usbnet_tx_inject ──┘◄── dn: records from the computer
```

Everything runs on the SoC system clock in the MAC wrapper's reset domain
(`macsys`). The bus streams `up` and `dn` are on that clock; a slave-FIFO
master crosses them to its bus clock. Until one is attached, the image
terminates the bus side: nothing arrives from the computer, records toward it
are taken and discarded, and the bus reads as down (LD1 off).

### Local reception in the split placement

The computer also reaches the device's own control receiver.
Its checked transmissions are observed at their accepted MAC beats.
Unicast to the device, broadcast and multicast receive local copies.
The device's live station address crosses through a coherent handshake.
Another station's unicast receives no local copy.

`KL_usbnet_local_rx` owns an independent whole-frame buffer.
It serializes local copies into the split mailbox's byte input.
The mailbox applies its normal protocol filters to both sources.
Network control bytes win arbitration at each frame boundary.
A granted frame retains ownership through backpressure and its end.
A full local buffer drops whole copies and counts them.
If transmit-domain recovery cancels an injection before its last beat,
the local copy rolls back only that uncommitted frame.
Completed copies and a stalled receiver output retain their state.

The network MAC, timestamping and media receiver wiring stays unchanged.
Local copies cannot backpressure any of those paths.
Buffered control delivery can wait behind one local frame.
This queueing affects firmware delivery, not network ingress timestamps.
The attachment requires the split control mailbox.

At the Arty's 80 MHz system clock, the conservative additional wait is
`2 * 1515 + 16 = 3046` clocks, or 38.075 us.
This bounds the serializer's remaining bytes and the mailbox's finite
classification, drain and verdict states; ring capacity and token availability
decide admission, rather than waiting for firmware to release `ready`.
The production mailbox test exercises full rings and empty token buckets.
Its longest observed wait is 1707 clocks (21.3375 us).
Adding the conservative bound to #1004's 29.77 ms ACMP row gives
29.808075 ms, below 30 ms by 191.925 us.
The mailbox's channel limits and held-record refill allowances still apply.
This is the merger's additional wait, not a claim that every local copy is admitted.

## 2. Receive copy (frames toward the computer)

Two independent copies read the frames the device takes from the MAC and
the device's own accepted transmit frames. Both apply the same rule and
never push back. A record arbiter alternates complete records when both
wait; their length, kind and payload never interleave. The device's own reception is
unchanged, and unicast frames addressed to the device stay with it. Rules, in
order (`KL_usbnet_pkg::rx_rule`):

| Order | Frame | Verdict |
|---|---|---|
| 1 | no computer attached | not copied |
| 2 | shorter than its header, or two IEEE 802.1Q tags | not copied |
| 3 | AVTP (EtherType 0x22F0) with a stream subtype, untagged or behind one tag | not copied |
| 4 | individual destination equal to the computer's address | **copied** |
| 4 | any other individual destination, the device's own included | not copied |
| 5 | destination 01-80-C2-00-00-00 to -0F, or 01-80-C2-00-00-20 to -2F | not copied |
| 6 | any other broadcast or multicast | **copied** |

- **Stream subtypes.** IEEE 1722-2016 Table 6 places every stream data format
  at subtype 0x00 to 0x7F: 61883/IIDC, MMA, AAF, CVF, CRF, TSCF, SVF, RVF, AEF
  continuous, and vendor and experimental streams. Control and alternative
  formats are at 0x80 to 0xFF: NTSCF, ESCF, EECF, AEF discrete, ADP, AECP,
  ACMP, MAAP and experimental control. A stream frame is therefore an AVTP
  frame whose subtype has bit 7 clear. Reserved stream values fall on the same
  side. Rule 3 comes before rule 4, so no stream frame reaches the computer,
  even one addressed to it.
- **Reserved destinations.** 01-80-C2-00-00-0x is the block a bridge never
  forwards (IEEE 802.1Q-2018 8.6.3, Table 8-1): gPTP, MSRP and LLDP use it.
  #1011 and usb-audio#5 also name MVRP among the excluded protocols. MVRP and
  MMRP use 01-80-C2-00-00-21 and -20 (Table 10-1), so the MRP application
  block -20 to -2F is excluded too.
- **Room.** Each copy holds 4 KiB of frames (one RAMB36) and 16 frame lengths. A
  frame that would be copied but finds no room is dropped whole and counted.

## 3. Transmit injection (frames from the computer)

A frame from the computer is checked when its last word arrives, and dropped
whole if any rule refuses it (`KL_usbnet_pkg::tx_rule`, and the record header
check for the length):

| Refused | Why |
|---|---|
| a length below 14 octets (19 with a tag, 15 for AVTP) or above 1515 | not a frame the path carries |
| a source that is not the computer's address | #1011: the computer sends only as itself |
| a destination in 01-80-C2-00-00-0x or -2x | no gPTP, SRP, MVRP or LLDP from the computer |
| two IEEE 802.1Q tags | the rules cannot read the subtype |
| an AVTP stream subtype | no stream frame from the computer |
| one tag with priority above 1 | IEEE 802.1Q-2018 Table 8-5: only best effort (0) and background (1) |

The last rule keeps the computer's frames in best effort at the next bridge as
well. A priority-2 or priority-3 tag would place them in an SR class queue
there (IEEE 802.1Q-2018 34.5).

**Best effort only, at the device.** `KL_usbnet_tx_arb` sits at the MAC core's
transmit input, after the datapath's store-and-forward FIFO. That FIFO carries
every SR class frame and every frame of the device's own control plane.
- **Priority.** The datapath wins every arbitration, at frame boundaries.
- **When an injection is granted.** Only when no datapath frame is waiting and
  none is still in the MAC between this point and the PHY.
- **What a datapath frame can wait for.** At most the one injected frame
  already granted. That is the lower-priority interference IEEE 802.1Q-2018
  Annex L and IEEE 802.1BA-2011 6.5 already budget. On the Arty's 100 Mb/s link,
  the longest injected frame is 1539 octets on the wire, 123.2 us.
- **No second injected frame ahead.** None can be queued in front of a datapath
  frame, because the next grant again needs the MAC empty of datapath frames.
- **No added latency otherwise.** With no injection, the datapath passes
  straight through.

The product's TX trunk has no credit-based shaper (see the TX-trunk note in
`hdl/milan/milan_datapath.sv`). This arbiter is therefore the strict-priority
stage below the SR classes (IEEE 802.1Q-2018 8.6.8).

**Egress qualification remains open at 100 Mb/s.** The control row reserves
1 ms for egress: `49 = 240 - 190 - T_egress`, as `rows_tiers.py` derives it.
The injected frame's 123.2 us must fit inside that allowance together with
the existing egress path. It cannot simply be added outside the 49 ms bound.
The capacity proof in [FR_NFR 3.4.1](../reference/FR_NFR.md#341-control-service-budget)
uses 250 Mb/s of a gigabit link. That premise does not hold for this board.
The current five rings can hold 254 minimum records accepted by `KL_mbx_tx`.
Their predecessors alone occupy 1700.16 us at 100 Mb/s, before injection,
even without competing traffic. This is a counterexample to that capacity
argument, not evidence that the production firmware generates that backlog.
A tighter bound on reachable Arty traffic and arbitration is required.
Firmware identity and CPU census results do not establish it.

**Rate limit.** A token bucket in octets on the wire, refilled at 10 Mb/s (a
tenth of the Arty's link) with a 3200-octet burst. Each frame costs at least 60
octets, plus 24 for preamble, FCS and interframe gap. A frame waits until the
bucket holds its cost; no frame is dropped for rate.
The reserved cost stays outside the refill ceiling until the frame ends at the PHY.
Thus arbitration delays and MAC stalls cannot create another burst.

**The REBOOT account.** The AECP REBOOT sequence counts the datapath's frames
out of the MAC by a toggle that flips on each frame end at the PHY
(`KL_reboot_ctrl`, [REBOOT_RESET.md](REBOOT_RESET.md)). With this path the arbiter
produces that toggle and leaves the computer's frames out of it. It announces
each grant across to the transmit clock. The frame end that answers the
announcement is the injected frame, the only frame in the MAC since the grant.

**The MAC's RMON counters** count every frame the MAC sends, the computer's
included; the tap's own counters (section 7) separate them.

**The gPTP egress observer** attributes frames by their gPTP destination and
EtherType (`KL_gptp_gmii_launch`). The computer's frames can carry neither, so
the observer's frame ordinal is unchanged.

A reset of either arbiter clock domain starts a flush handshake.
Both domains must acknowledge and release it before traffic resumes.
The outstanding frame count resets; the frame-end toggle does not.
Both clocks must run for recovery.
Reset discards interrupted MAC frames, as the MAC reset contract specifies.

## 4. The bus records

The byte contract is [usb-audio PR #7, docs/NETWORK.md](https://github.com/kebag-logic/usb-audio/blob/da91f5999a31d0965872ff153194ee817d1106d1/docs/NETWORK.md),
adopted by the [interface amendment](https://github.com/kebag-logic/milan-fpga/issues/1011#issuecomment-7186353239).
Both streams carry 16-bit words, low octet first. An odd payload ends with
one zero pad octet. Each record starts with two words:

| Word | Field |
|---|---|
| 0 | payload length in octets, header and padding excluded |
| 1 | kind: 0x4E01 Ethernet frame, 0x4E02 station |

A frame toward the computer has 14 to 1514 octets without FCS. The merged
FX3 contract sends at most 1514 octets from the computer too. This FPGA
receiver retains its 1515-octet acceptance envelope, which that contract
explicitly records as a compatible superset. There is no general extra-byte
exception in the FX3 sender; its USB boundary workaround fits within 1514.
Each record toward the computer ends with `last` on its final word, for the
slave-FIFO master's PKTEND#. There is no incoming boundary signal.
Unknown kinds and wrong lengths are consumed by the full 16-bit length and
counted. A checked frame waits for whole-frame buffer room.

The station record has exactly 16 payload octets:

| Offset | Size | Field |
|---|---|---|
| 0 | 6 | computer MAC, first octet first |
| 6 | 2 | flags: bit 0 MAC_VALID, bit 1 CONFIGURED, bit 2 SUPERSPEED, bit 3 DATA_ACTIVE |
| 8 | 2 | CDC packet filter |
| 10 | 2 | sequence, incremented for each record |
| 12 | 2 | heartbeat period in milliseconds |
| 14 | 2 | low 16 bits of the configuration digest |

MAC_VALID clear detaches the station and clears its address. An invalid
address or zero heartbeat also clears it. A valid address is individual and
locally administered. The packet filter and digest words are consumed; the
FX3 owns the host's filter, and this thread-agnostic FPGA attachment does not
compare configuration digests. It sends no separate detach record.

The FX3 renews the MAC after USB bus or port reset, and clears MAC_VALID
on reset or disconnection. Configuration zero clears CONFIGURED while
retaining that enumeration's valid MAC; LD1 goes dark independently. The
FPGA follows the received fields and does not infer a new address lifetime
from CONFIGURED or DATA_ACTIVE. The sequence survives USB resets.

The sequence comparison accepts a forward delta of 1 through 32767,
including wrap. A duplicate or older record is counted and cannot renew
freshness or replace the current station. Reset or expiry permits the next
sequence to start afresh. Queued records do not establish their wall-clock
creation time; the freshness interval starts when a new record is received.

## 5. The signals for LD1 (the USB device firmware's side)

LD1 requires all of the following:

1. The slave-FIFO master reports PCLK running (`usbnet_bus.alive`).
2. A valid station address is held.
3. The last new station record arrived less than three of its heartbeat
   periods ago.
4. MAC_VALID, CONFIGURED and SUPERSPEED are all set.

DATA_ACTIVE is not an LD1 condition. At expiry both the address and LD1
clear. The FX3 sends a station record at every state change and each
heartbeat (100 ms in its example), including after disconnection with
MAC_VALID clear. No separate register-write control path is required.
The future slave-FIFO master must honor DATA_ACTIVE before waiting for the
FPGA-to-FX3 socket: that producer channel exists only at data alternate
setting 1. The station state exposes DATA_ACTIVE, but this image has no
attached slave-FIFO master.

## 6. Status LEDs (#1018)

LD0 to LD3 are the Arty's RGB LEDs, on the green channel only, at a PWM duty of
16/256 (6.25 %); red and blue are held dark. LD4 stays the IDENTIFY LED.

| LED | On | Source |
|---|---|---|
| LD0 | Ethernet link up; on a frame in either direction it goes off for 40 ms, then stays on for at least 60 ms | the MAC's link state (`milan_mac_link_status`) and its frame ends |
| LD1 | the USB 3.0 path works (section 5) | the tap |
| LD2 | any stream input media-locked, or any stream output transmit gate open | fabric levels |
| LD3 | internal clock, or the selected source locked | fabric levels |

The [ruling](https://github.com/kebag-logic/milan-fpga/pull/1020#issuecomment-7213370880)
replaces the firmware observer.
No firmware-written LED register remains.
No LED code enters the control image.
LD2 does not report a listener connection count.
It reports input media lock or output transmission permission.

LD3 ignores lock when the selected source is internal.
A stream source requires its own input media lock.
It also requires the existing media clock-domain lock.
An external source requires only that clock-domain lock.
Other inputs cannot satisfy a selected stream's requirement.

The datapath exports six existing levels on `axis_clk`.
`KL_status_led_truth` registers the two complete LED predicates there.
Each predicate crosses through two synchronizer stages into `sys`.
The independent display bits have no joint atomicity requirement.
Neither bit controls traffic or mailbox service.
Datapath reset clears both predicates before their crossings settle.
LD0 and LD1 already use the system clock.

| Level | Existing source | Clock |
|---|---|---|
| any input media lock | `avtp_rx_monitor.locked_sh_r`, reduced with `crf_locked_w` | datapath |
| any output transmit gate | `tkd_streaming_w`, including CRF where present | datapath |
| internal selection | `int_clk_selected_r` from the generated source table | datapath |
| stream selection | `follow_sel_r` | datapath |
| selected input media lock | indexed AAF lock, or `crf_locked_w` | datapath |
| media clock-domain lock | `ctr_mclk_lock_w` | datapath |

`usbnet_soc.fabric_ports` carries these into the Arty top.
`StatusLeds` connects them to `KL_status_led_truth`.
`led_stream_dp` and `led_clock_dp` cross to their `_sys` signals.
`KL_status_leds` drives the green channels from those synchronized levels.

## 7. Registers

| Register | Access | Content |
|---|---|---|
| `status_leds_state` | RO | bits 3:0 LD0 to LD3 as shown, before the PWM |
| `milan_mac_usbnet_host` | RO | the computer's address, octets 2 to 5 |
| `milan_mac_usbnet_host_hi` | RO | bits 15:0 octets 0 and 1; bit 16 an address is held; bit 17 LD1 |
| `milan_mac_usbnet_counts` | RO | 16-bit saturating counters from bit 0: copied, dropped for room, passed, dropped by a rule, records skipped, frames injected |

`milan_mac_usbnet_local_counts` reports local receive copies and overflows.
Each count saturates at 65,535; copies occupy the low half.

The LED bank is pinned to its own CSR page, below the REBOOT port's. The tap's
registers follow every other register of the MAC's bank. No address of an
image without them moves.

## 8. Verification

- `tb/verilator/usbnet` (`make`, `make mutants`):
  - **tap harness.** Every receive class, the transmit drops, the station record
    and LD1's inputs, a full buffer, and the rate limit. The best-effort-only
    injection is checked against a class A-like datapath stream with the
    computer's side saturating its rate limit, with and without a stalling MAC:
    - the datapath wins every arbitration;
    - no injected frame shares the MAC with a datapath frame;
    - a datapath frame waits at most one injected frame;
    - the datapath frames leave intact and in order;
    - the frame-end toggle counts the datapath frames only.
  - **Device transmit copy.** Unicast to the computer, broadcast and
    multicast pass; other unicast, stream subtypes, reserved destinations
    and oversized records do not. With USB draining or stalled, the device
    has identical transmit departure cycles and frame-end accounting.
  - **Local receiver harness.** Device unicast, broadcast and multicast;
    odd and maximum lengths; full-buffer recovery and byte-stream stalls.
    Network control traffic wins at boundaries and never interleaves.
  - **LED harness.** Each LED through each state, the blink and its hold, and
    the duty.
  - **planted defects.** One per rule, each required to fail its named check
    (`mutants.py`).
- **Fabric predicates.** The truth-table harness exhausts all six inputs.
  It checks reset and source-clock registration too.
  Each predicate rule has a named planted defect.
- **Production LED attachment.** The real attachment is generated with
  independent source and system clocks. Its 258 checks cover the complete
  predicates, source registration, both synchronizer stages and colour wiring.
- **Clock commands.** Real `SET_CLOCK_SOURCE` commands select internal,
  flowing stream, stopped stream and external sources in the unchanged AECP
  fixture, then exercise the fabric predicate with explicit lock inputs.
  This is a command-to-predicate seam test; it does not simulate the processor
  bus or media-clock acquisition.
- **Mailbox wait.** The local receiver drives the production mailbox byte
  input with even, odd and maximum lengths, full rings and empty buckets.
  A planted grant-release defect must fail the named wait check.
- **The stand-alone shaper suites** (`tb/verilator/cbs`, `shaper_core`,
  `queues`) are unchanged by this path and pass.

The sweep registers this suite with its provisional timeout.
Every harness reports executed checks and failures to the sweep tally.
Boundary tests cover both direction-specific maxima and following-frame recovery.
Record tests grade every accepted terminator, including stalled final words.
Held-injection tests independently sum wire octets over every departure interval.
They cover short and maximum frames, arbitration waits and MAC backpressure.
Reset tests cover each domain alone, both request parities and activity.
The control image must match its baseline at identical pins.
Both ELF and map-header bytes participate in that proof.
Scheduling qualification must name the pins it measured.
The local receive and transmit waits need separate fabric bounds.

Station records share the incoming queue with frame records.
A frame waiting for space can delay a later station update.
Freshness expires normally while waiting; it is not extended by congestion.

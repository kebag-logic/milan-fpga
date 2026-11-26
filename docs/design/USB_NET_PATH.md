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

## 1. Where it sits

```
           MAC core RX ──► rx_dp (to the datapath) ─────────────► datapath
                              │ accepted beats (valid and ready)
                              ▼
                        KL_usbnet_rx_copy ──► up: records toward the computer
 datapath ─► tx_sf (store-and-forward) ─► KL_usbnet_tx_arb ─► MAC core TX ─► PHY
                                              ▲   (strict priority to tx_sf)
                        KL_usbnet_tx_inject ──┘◄── dn: records from the computer
```

Everything runs on the SoC system clock in the MAC wrapper's reset domain
(`macsys`). The bus streams `up` and `dn` are on that clock; a slave-FIFO
master crosses them to its bus clock. Until one is attached, the image
terminates the bus side: nothing arrives from the computer, records toward it
are taken and discarded, and the bus reads as down (LD1 off).

## 2. Receive copy (frames toward the computer)

The copy reads the frames the device itself takes, after its MAC core and
before its datapath, and never pushes back. The device's own reception is
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
- **Room.** The copy holds 4 KiB of frames (one RAMB36) and 16 frame lengths. A
  frame that would be copied but finds no room is dropped whole and counted.

## 3. Transmit injection (frames from the computer)

A frame from the computer is checked when its last word arrives, and dropped
whole if any rule refuses it (`KL_usbnet_pkg::tx_rule`, and the record header
check for the length):

| Refused | Why |
|---|---|
| a length below 14 octets (19 with a tag, 15 for AVTP) or above 1518 | not a frame the path carries |
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
  the longest injected frame is 1542 octets on the wire, 123.4 us.
- **No second injected frame ahead.** None can be queued in front of a datapath
  frame, because the next grant again needs the MAC empty of datapath frames.
- **No added latency otherwise.** With no injection, the datapath passes
  straight through.

The product's TX trunk has no credit-based shaper (see the TX-trunk note in
`hdl/milan/milan_datapath.sv`). This arbiter is therefore the strict-priority
stage below the SR classes (IEEE 802.1Q-2018 8.6.8).

**Rate limit.** A token bucket in octets on the wire, refilled at 10 Mb/s (a
tenth of the Arty's link) with a 3200-octet burst. Each frame costs at least 60
octets, plus 24 for preamble, FCS and interframe gap. A frame waits until the
bucket holds its cost; no frame is dropped for rate.

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

## 4. The bus records

Both streams carry records of 16-bit words. The record's octets go two per
word, the first octet in bits 7:0, and an odd length is padded with a zero
octet. Each record starts with one header word:

| Bits | Field |
|---|---|
| 15:12 | type |
| 11:0 | length in octets, the header excluded |

| Type | Direction | Length | Payload |
|---|---|---|---|
| 0 FRAME | both | 14 to 1518 | an Ethernet frame without its FCS |
| 1 HOST | to the FPGA | 8 | the computer's address (6 octets, first octet first), then the USB state word (2 octets, low octet first) |
| 2 DETACH | to the FPGA | 0 | the computer left: the address is cleared |

- **The USB state word.** Bit 0: configured at SuperSpeed. Bit 1: the network
  function is active. Other bits are reserved and sent as 0.
- **When the USB device sends HOST.** At every connection, with the newly
  generated address, then at least once a second while connected. A HOST whose
  address is a group address, or is not locally administered, is refused,
  counted and treated as DETACH.
- **Unknown records.** Any other type, or a HOST or DETACH of another length,
  is skipped by its length and counted. The parser stays in step, because the
  length is the only framing the bus has.
- **Toward the computer.** Each record ends with `last` on its final word, so a
  slave-FIFO master can commit the USB transfer there (PKTEND#).
- **Backpressure.** From the computer, a frame whose header has arrived waits,
  backpressured, until the buffer holds the whole frame (4 KiB, one RAMB36), so
  a frame is never cut.

## 5. The signals for LD1 (the USB device firmware's side)

LD1 "the USB 3.0 path works" needs no wire beyond the slave-FIFO bus. It is on
while all of these hold:

1. **bus alive.** The slave-FIFO master reports its bus clock running
   (`usbnet_bus.alive`, a level from the master, with PCLK out of reset and its
   clock locked).
2. **address held.** A HOST record arrived and was not followed by a DETACH.
3. **fresh.** The last HOST record is at most 3 s old.
4. **SuperSpeed.** Bit 0 of the last HOST record's state word is set.

So the USB device firmware owes: a HOST record at every connection and at
least once a second, its state word kept current, and a DETACH on a
disconnection it can still report. A firmware that stops sending HOST records
turns LD1 off within 3 s.

## 6. Status LEDs (#1018)

LD0 to LD3 are the Arty's RGB LEDs, on the green channel only, at a PWM duty of
16/256 (6.25 %); red and blue are held dark. LD4 stays the IDENTIFY LED.

| LED | On | Source |
|---|---|---|
| LD0 | Ethernet link up; on a frame in either direction it goes off for 40 ms, then stays on for at least 60 ms | the MAC's link state (`milan_mac_link_status`) and its frame ends |
| LD1 | the USB 3.0 path works (section 5) | the tap |
| LD2 | a stream is connected | `status_leds_ctrl` bit 0, written by the control firmware |
| LD3 | the clock source is satisfied | `status_leds_ctrl` bit 1, written by the control firmware |

The control firmware writes LD2 and LD3 every 250 ms
(`sw/firmware/ctrl/plat/ctrl_plat_leds.h`), from the AECP core's own state:

- **LD2:**
  - some STREAM_INPUT is bound with its media locked (IEEE 1722.1-2021 7.4.42,
    STREAM_INPUT counters MEDIA_LOCKED and MEDIA_UNLOCKED); or
  - some STREAM_OUTPUT has a connected Listener. A Milan Talker keeps no ACMP
    connection_count, so the Listener's SRP registration for the stream
    (Milan v1.2 5.4.2.10.2) stands for a connection_count above zero.
- **LD3:** CLOCK_DOMAIN 0's clock source, as SET_CLOCK_SOURCE set it
  (IEEE 1722.1-2021 7.4.23), is:
  - INTERNAL; or
  - INPUT_STREAM (CRF or AAF), with its STREAM_INPUT bound, the input's media
    locked and the clock domain locked (CLOCK_DOMAIN counters LOCKED and
    UNLOCKED); or
  - EXTERNAL, with the clock domain locked.

A lock state is read from its two counters. Each counts edges into its state
from an unlocked reset, so the state is locked when LOCKED − UNLOCKED is odd;
the parity survives a wrap of either counter. The firmware compiles this code
only where the SoC has the register: `ctrl_plat_gen.py` emits `CTRL_PLAT_LEDS`
from the SoC's `csr.csv`.

## 7. Registers

| Register | Access | Content |
|---|---|---|
| `status_leds_ctrl` | RW | bit 0 LD2, bit 1 LD3; written by the firmware |
| `status_leds_state` | RO | bits 3:0 LD0 to LD3 as shown, before the PWM |
| `milan_mac_usbnet_host` | RO | the computer's address, octets 2 to 5 |
| `milan_mac_usbnet_host_hi` | RO | bits 15:0 octets 0 and 1; bit 16 an address is held; bit 17 LD1 |
| `milan_mac_usbnet_counts` | RO | 16-bit saturating counters from bit 0: copied, dropped for room, passed, dropped by a rule, records skipped, frames injected |

The LED bank is pinned to its own CSR page, below the REBOOT port's. The tap's
registers follow every other register of the MAC's bank. No address of an
image without them moves.

## 8. Verification

- `tb/verilator/usbnet` (`make`, `make mutants`):
  - **tap harness.** Every receive class, the transmit drops, the host record
    and LD1's inputs, a full buffer, and the rate limit. The best-effort-only
    injection is checked against a class A-like datapath stream with the
    computer's side saturating its rate limit, with and without a stalling MAC:
    - the datapath wins every arbitration;
    - no injected frame shares the MAC with a datapath frame;
    - a datapath frame waits at most one injected frame;
    - the datapath frames leave intact and in order;
    - the frame-end toggle counts the datapath frames only.
  - **LED harness.** Each LED through each state, the blink and its hold, and
    the duty.
  - **planted defects.** One per rule, each required to fail its named check
    (`mutants.py`).
- **Firmware.** The AECP arm's `Leds.*` tests set the clock source over AECP
  (SET_CLOCK_SOURCE) in the three cases: internal, following a flowing stream,
  and following a stopped stream. They also check LD2's rules. The tests run on
  the shipping model and on each Arty model. The campaign plants one defect per
  rule (`aecp_leds_mutants.py`).
- **The stand-alone shaper suites** (`tb/verilator/cbs`, `shaper_core`,
  `queues`) are unchanged by this path and pass.

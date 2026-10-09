<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Packet mailbox contract, generated reference

**GENERATED** by `sw/mailbox/gen_mailbox.py` from `sw/mailbox/mailbox.yaml`; do not hand-edit.
Regenerate with `python3 sw/mailbox/gen_mailbox.py --write`.

The design page is [MAILBOX_SPLIT.md](../design/MAILBOX_SPLIT.md).
This page is contract version 2.2.

## Byte order

- Every register, record header word and event word is one 32-bit value.
- A field sits at the bit positions below, whatever the host's byte order.
- Frame bytes travel four to a ring word, in little-endian lanes.
- Frame byte k is in ring word k/4, at bits 8*(k%4)+7 down to 8*(k%4).
- Wire fields inside a frame keep network (big-endian) order.
- The bus carries 32-bit accesses only; a partial write is refused.

## Registers

### Global registers

Byte offsets from the window base.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `ID` | ro | Contract identity. Firmware checks MAGIC and MAJOR before it opens a channel. |
| `0x004` | `CAPS` | ro | What this build elaborated. |
| `0x008` | `IRQ_STATUS` | rw1c | The interrupt causes. RX and EVT are levels: they stay set while the ring holds an unconsumed record and clear when the core advances its tail. ERR is sticky and cleared by writing 1. |
| `0x00C` | `IRQ_ENABLE` | rw | The interrupt line is the OR of IRQ_STATUS AND IRQ_ENABLE. Reset 0. |
| `0x010` | `NOW_MS` | ro | Free-running fabric millisecond counter, the time base of every timer deadline. |
| `0x014` | `LINK` | ro | Current link level per interface. |
| `0x018` | `TICK_CTL` | rw | The centisecond tick. Reset 0. While EN is set the fabric counts one tick every tick_ms milliseconds of NOW_MS and posts TICK events carrying the ticks elapsed since the previous TICK record, so the firmware calls its centisecond timer port (lwSRP's shlan_timer_tick) once per tick counted and loses none when it is late. Clearing EN drops the unposted count. |
| `0x020` | `OWN_EID_LO` | rw | The filter's entity_id, low word. Reset 0; firmware writes it before it opens a channel. |
| `0x024` | `OWN_EID_HI` | rw | The filter's entity_id, high word. |
| `0x028` | `FILTER_EN` | rw | Bit c opens channel c. Reset 0: every channel is closed and its frames are dropped uncounted until the firmware has written OWN_EID and opened it. |
| `0x02C` | `MAAP_BASE_LO` | rw | The MAAP range this entity probes or holds, low 32 bits of the first address. |
| `0x030` | `MAAP_BASE_HI` | rw | The MAAP range, high 16 bits of the first address. |
| `0x034` | `MAAP_COUNT` | rw | Addresses in the MAAP range. 0 means no range, and no MAAP frame passes. |
| `0x038` | `TMR_DEADLINE` | rw | The deadline the next TMR_CMD arm uses, in NOW_MS units. |
| `0x03C` | `TMR_CMD` | wo | A write arms or cancels one timer slot. An arm replaces whatever the slot held and drops its unposted expiry; a cancel disarms it and drops its unposted expiry. An expiry already in the event ring stays there and carries the tag of the arm it belongs to. Any other OP is refused and counted in BUS_ERR. |
| `0x060` | `EVT_HEAD` | ro | Words the fabric has written into the event ring, modulo 2^16. |
| `0x064` | `EVT_TAIL` | rw | Words the core has consumed from the event ring. Writing it releases the space. A value more than the ring behind EVT_HEAD, or ahead of it, leaves no free word: nothing posts until it is back in range. |
| `0x070` | `BUS_ERR` | ro | Host accesses refused, saturating. A write with a partial byte strobe and a bad TMR_CMD are refused. |
| `0x074` | `FILTER_MISMATCH` | ro | Untagged frames of a control EtherType that match no channel's tuple, saturating. A frame counts once, when it reaches byte 14 with an EtherType some tuple names and its destination MAC, EtherType and AVTP subtype together match no tuple of any channel; it also sets IRQ_STATUS.ERR. A frame that matches a tuple and fails its channel's identity term, a frame for a closed channel and a tagged frame never count, nor does a frame that ends before byte 14. |

`ID` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `MAGIC` | 0x4D42 |
| `[15:8]` | `MAJOR` | contract major version |
| `[7:0]` | `MINOR` | contract minor version |

`CAPS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[19:16]` | `EVT_WORDS_LOG2` | event ring size |
| `[15:8]` | `N_TIMERS` | timer slots |
| `[7:4]` | `N_IF` | interface count |
| `[3:0]` | `N_CH` | channel count |

`IRQ_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31]` | `ERR` | a drop or error counter moved (sticky |
| `[8]` | `EVT` | the event ring is not empty (level) |
| `[7:0]` | `RX` | bit c: channel c's receive ring is not empty (level) |

`IRQ_ENABLE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31]` | `ERR` | error enable |
| `[8]` | `EVT` | event ring enable |
| `[7:0]` | `RX` | per-channel enable |

`NOW_MS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `MS` | milliseconds since reset |

`LINK` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[3:0]` | `UP` | bit i: interface i link up |

`TICK_CTL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `EN` | post TICK events |

`OWN_EID_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `EID` | entity_id[31:0] |

`OWN_EID_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `EID` | entity_id[63:32] |

`FILTER_EN` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[7:0]` | `OPEN` | per-channel open |

`MAAP_BASE_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `ADDR` | first address[31:0] |

`MAAP_BASE_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `ADDR` | first address[47:32] |

`MAAP_COUNT` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | address count |

`TMR_DEADLINE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `MS` | absolute deadline |

`TMR_CMD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:30]` | `OP` | 1 arm, 2 cancel |
| `[23:8]` | `TAG` | firmware tag |
| `[7:0]` | `SLOT` | timer slot |

`EVT_HEAD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | producer count |

`EVT_TAIL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | consumer count |

`BUS_ERR` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | refusals |

`FILTER_MISMATCH` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | frames |

### Interface registers

Interface i's block starts at `0x040 + 0x10 * i`.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `GM_LO` | ro | Grandmaster identity, low word. Reading it snapshots GM_HI and DOMAIN, so the next two reads are coherent with it (the CSR window's convention). |
| `0x004` | `GM_HI` | ro | Grandmaster identity, high word, from the snapshot. |
| `0x008` | `DOMAIN` | ro | gPTP domain number, from the snapshot. |

`GM_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `ID` | gptp_grandmaster_id[31:0] |

`GM_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `ID` | gptp_grandmaster_id[63:32] |

`DOMAIN` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[7:0]` | `NUMBER` | gptp_domain_number |

### Interface filter registers

Interface i's filter block starts at `0x080 + 0x8 * i`.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `OWN_MAC_LO` | rw | This interface's own unicast MAC, low word. Reset 0; firmware writes it before it opens a channel. |
| `0x004` | `OWN_MAC_HI` | rw | This interface's own unicast MAC, high 16 bits. |

`OWN_MAC_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `MAC` | MAC[31:0], destination wire bytes 2 to 5 |

`OWN_MAC_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `MAC` | MAC[47:32], destination wire bytes 0 and 1 |

### Interface bound-talker registers

Interface i's bound-talker table starts at `0x200 + 0x100 * i`, and its entry e at `0x10 * e` inside it, for 16 entries (one per listener stream). An `eq_bound` term reads the table of the interface the frame arrived on.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `BOUND_EID_LO` | rw | An entry's talker_entity_id, low word. Reset 0. |
| `0x004` | `BOUND_EID_HI` | rw | An entry's talker_entity_id, high word. Reset 0. |
| `0x008` | `BOUND_EN` | rw | The entry holds a bound talker. Reset 0. The firmware clears EN before it rewrites the entry's BOUND_EID, so a half-written identity never matches. |

`BOUND_EID_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `EID` | talker_entity_id[31:0], ADPDU wire bytes 22 to 25 |

`BOUND_EID_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `EID` | talker_entity_id[63:32], ADPDU wire bytes 18 to 21 |

`BOUND_EN` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `EN` | the entry takes part in the eq_bound test |

### Interface publication registers

Interface i's publication block starts at `0x800 + 0x200 * i`. Bit s of a source field is source s, for 16 sources. The firmware owner writes each value before the response that promises it; the datapath reads interface i's block through `KL_mbx`'s `pub_*_o` ports.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `DA_GATE` | rw | The talker destination-address gate: bit s is set while MAAP holds a stream destination address for source s on this interface (IEEE 1722-2016 Annex B; the processor's acmp_declaring_o). The MAAP owner writes it before it reports the allocation, which a PROBE_TX_RESPONSE then promises (Milan v1.2 5.5.4.1). |
| `0x004` | `LICENCE` | rw | The SRP stream gate: bit s is set while source s holds its licence, an admitted Talker Advertise with a registered Listener Ready or Ready Failed after the stream VLAN's MVRP Join (Milan v1.2 5.3.7.3 and 4.3.2; the processor's srp_active_o AND srp_sr_admitted_o). The SRP owner writes it before it reports the licence. |
| `0x008` | `IDLE_SLOPE` | rw | The sum, in bits per second, of the bandwidth the SRP owner admitted for this interface's sources, Ethernet overhead included (the processor's srp_sum_slope_bps_o), written before the declarations it admitted are sent. |
| `0x00C` | `SR_DOMAIN` | rw | The SR class A Domain this interface's declarations carry (Milan v1.2 4.2.7.2.1). ADOPTED is set once a received Domain replaced the default {priority 3, VID 2}, until the link restarts (the processor's srp_domain_adopted_o, class_a_prio_o and class_a_vid_o). Written in one access, before the declarations that carry it. |

`DA_GATE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `OPEN` | bit s: source s may send to its destination address |

`LICENCE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `ACTIVE` | bit s: source s's stream may leave |

`IDLE_SLOPE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `BPS` | admitted bandwidth |

`SR_DOMAIN` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[24]` | `ADOPTED` | a received Domain was adopted |
| `[18:16]` | `PRIORITY` | the operational SR class A priority |
| `[11:0]` | `VID` | the operational SR class A VID |

### Interface publication sink registers

Sink k's entry starts at `0x100 + 0x10 * k` inside interface i's publication block, for 16 sinks (one per listener stream). A hole, a sink past the last and an interface the build does not have read 0 and take no write.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `SID_LO` | rw | Sink k's stream_id, low word, as last written. The datapath reads it while SID_VALID is set. |
| `0x004` | `SID_HI` | rw | Sink k's stream_id, high word, as last written. The datapath reads it while SID_VALID is set. |
| `0x008` | `BINDING` | rw | Sink k's binding. BOUND is the bound state (Milan v1.2 5.3.8.2; the processor's acmp_bound_o), written before the BIND_RX or UNBIND_RX response. SID_VALID says SID_LO and SID_HI hold the stream_id the sink settled on (5.5.3.5.18 step 4, 5.3.8.9; the processor's acmp_bound_sid_o); the datapath takes the stream_id only while it is set. The firmware clears SID_VALID before it rewrites SID_LO and SID_HI and sets it after, so a half-written stream_id never reaches the datapath. |

`SID_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `SID` | stream_id[31:0] |

`SID_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `SID` | stream_id[63:32] |

`BINDING` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[1]` | `SID_VALID` | SID_LO and SID_HI are the settled stream_id |
| `[0]` | `BOUND` | the sink is bound |

### Channel registers

Channel c's block starts at `0x100 + 0x20 * c`.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `RX_HEAD` | ro | Words the fabric has committed into the receive ring, modulo 2^16. |
| `0x004` | `RX_TAIL` | rw | Words the core has consumed. Writing it releases the space (the RX doorbell). A value more than the ring behind RX_HEAD, or ahead of it, leaves no free word: every frame counts in RX_DROP until it is back in range. |
| `0x008` | `TX_HEAD` | rw | Words the core has committed into the transmit ring. Writing it is the TX doorbell. A value more than the ring ahead of TX_TAIL is refused like a malformed record. |
| `0x00C` | `TX_TAIL` | ro | Words the fabric has consumed from the transmit ring. |
| `0x010` | `RX_DROP` | ro | Frames the channel accepted but could not store (ring full or over max_frame_bytes), saturating. |
| `0x014` | `RATE_DROP` | ro | Frames the channel's rate limiter refused, saturating. |
| `0x018` | `TX_ERR` | ro | TX records the fabric refused, saturating. A refused record flushes the ring to TX_HEAD. |
| `0x01C` | `RX_PASS` | ro | Frames committed into the receive ring, modulo 2^16. |

`RX_HEAD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | producer count |

`RX_TAIL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | consumer count |

`TX_HEAD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | producer count |

`TX_TAIL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `WORDS` | consumer count |

`RX_DROP` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | frames |

`RATE_DROP` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | frames |

`TX_ERR` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | records |

`RX_PASS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `COUNT` | frames |

## Records

One received frame, Ethernet header first, FCS stripped. The fabric writes the payload words, then the two header words, then advances RX_HEAD past the whole record, so the core never sees a partial record.

One frame to transmit, Ethernet header first, without FCS or padding. The core writes the whole record, then advances TX_HEAD past it. Records leave in commit order across every channel: of the records committed and not yet sent, the merge sends the one whose SEQ comes first modulo 2^16, so a response committed before the notification it causes leaves before it. Records with equal SEQ leave round-robin by channel.

One fabric event, four words. Sources are coalesced: a source that fires again before its record is posted posts once, with its state at posting time, so the ring never overflows and no current state is lost.

| Record | Word | Bits | Field | Meaning |
|---|---|---|---|---|
| RX frame | word 0 | `[31:28]` | `KIND` | 1 |
| RX frame | word 0 | `[19:16]` | `IF` | interface the frame arrived on |
| RX frame | word 0 | `[15:0]` | `LEN` | frame bytes |
| RX frame | word 1 | `[31:0]` | `ARRIVAL_MS` | NOW_MS when the frame's last byte arrived |
| TX frame | word 0 | `[31:28]` | `KIND` | 2 |
| TX frame | word 0 | `[19:16]` | `IF` | interface to send on |
| TX frame | word 0 | `[15:0]` | `LEN` | frame bytes |
| TX frame | word 1 | `[31:16]` | `RSVD` | must be 0; any other value refuses the record |
| TX frame | word 1 | `[15:0]` | `SEQ` | commit sequence: the core's count of TX records committed on every channel, modulo 2^16 |
| event | word 0 | `[31:16]` | `SEQ` | posting sequence |
| event | word 0 | `[11:8]` | `IF` | interface |
| event | word 0 | `[7:0]` | `TYPE` | event type |
| TIMER event | word 1 | `[23:16]` | `SLOT` | timer slot |
| TIMER event | word 1 | `[15:0]` | `TAG` | the tag of the arm that expired |
| TIMER event | word 2 | `[31:0]` | `DEADLINE_MS` | the armed deadline |
| TIMER event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |
| LINK event | word 1 | `[0]` | `UP` | link level at posting |
| LINK event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |
| GM event | word 1 | `[31:0]` | `ID_LO` | gptp_grandmaster_id[31:0] at posting |
| GM event | word 2 | `[31:0]` | `ID_HI` | gptp_grandmaster_id[63:32] at posting |
| GM event | word 3 | `[7:0]` | `DOMAIN` | gptp_domain_number at posting |
| TICK event | word 1 | `[15:0]` | `COUNT` | ticks since the previous TICK record |
| TICK event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |

An RX or TX record is the header words, then ceil(LEN/4) payload words.

| Event | TYPE | Meaning |
|---|---:|---|
| `TIMER` | 1 | A timer slot's deadline passed. |
| `LINK` | 2 | The interface's link level changed. |
| `GM` | 3 | The gPTP plane published a grandmaster change on the interface. |
| `TICK` | 4 | Centiseconds elapsed (TICK_CTL.EN set). COUNT is the ticks counted since the previous TICK record, at least 1 and saturating; the firmware calls its centisecond timer port COUNT times. |

## Channels and the ingress filter

A frame is classified when its byte 15 arrives, by its full tuple,
or at its last byte when it ends at byte 14.
A channel's tuple holds when the destination MAC is the tuple's address,
or, for an `own` tuple, `OWN_MAC` of the interface the frame arrived on;
the EtherType is the tuple's; the AVTP subtype is the tuple's where it names one;
and the message_type (the low nibble of byte 15, 0 when the frame ends
at byte 14) is one of the tuple's where it names some.
The frame passes when its channel is open and one accept term (the identity term) holds.
It must also fit max_frame_bytes and the free ring space.
Then the channel's token bucket must hold a token.

Untagged frames only, by construction: a VLAN tag's TPID (`0x8100`, `0x88A8`, `0x88E7`) sits where the
EtherType is read, and no tuple names one, so a tagged frame reaches no channel
and no counter. An untagged frame whose EtherType some tuple names, matching no tuple,
counts once in `FILTER_MISMATCH`. A frame failing its identity term is dropped uncounted.
A frame that ends before byte 14 is classified into nothing and counted nowhere.

| Channel | id | receive ring | transmit ring | Max frame | Rate |
|---|---:|---|---|---:|---|
| `adp` | 0 | `0x1000`, 256 words | `0x1400`, 128 words | 128 | burst 8, one token per 10 ms |
| `acmp` | 1 | `0x1800`, 256 words | `0x1C00`, 256 words | 128 | burst 16, one token per 5 ms |
| `aecp` | 2 | `0x2000`, 512 words | `0x2800`, 512 words | 1514 | burst 16, one token per 5 ms |
| `maap` | 3 | `0x3000`, 128 words | `0x3200`, 128 words | 64 | burst 8, one token per 20 ms |
| `srp` | 4 | `0x4000`, 1024 words | `0x5000`, 512 words | 1514 | burst 32, one token per 2 ms |

| Channel | Tuple | VLAN tag | Destination MAC | EtherType | AVTP subtype | message_type | Why |
|---|---:|---|---|---|---|---|---|
| `adp` | 0 | absent | `91:E0:F0:01:00:00` | `0x22F0` | `0xFA` | any | the ADP and ACMP multicast address (IEEE 1722.1-2021 Table B.1) |
| `acmp` | 0 | absent | `91:E0:F0:01:00:00` | `0x22F0` | `0xFC` | any | the ADP and ACMP multicast address (IEEE 1722.1-2021 Table B.1; 8.2.1 sends every ACMPDU to it) |
| `acmp` | 1 | absent | own MAC of the arrival interface (`OWN_MAC`) | `0x22F0` | `0xFC` | any | this interface's own unicast MAC, a receive tolerance the owner decision grants, not a normative transmission |
| `aecp` | 0 | absent | own MAC of the arrival interface (`OWN_MAC`) | `0x22F0` | `0xFB` | any | this interface's own unicast MAC (IEEE 1722.1-2021 9.2.2: commands and responses travel unicast) |
| `maap` | 0 | absent | `91:E0:F0:00:FF:00` | `0x22F0` | `0xFE` | any | the MAAP multicast address (IEEE 1722-2016 Table B.10; B.2.1 sends PROBE and ANNOUNCE to it) |
| `maap` | 1 | absent | own MAC of the arrival interface (`OWN_MAC`) | `0x22F0` | `0xFE` | 2 | a DEFEND to this interface's own unicast MAC (IEEE 1722-2016 B.2.1: the PROBE's source MAC) |
| `srp` | 0 | absent | `01:80:C2:00:00:0E` | `0x22EA` | not read | any | MSRP: the Nearest Bridge group address and the MSRP EtherType (IEEE 802.1Q-2018 35.2.2.1, 35.2.2.2) |
| `srp` | 1 | absent | `01:80:C2:00:00:21` | `0x88F5` | not read | any | MVRP: the Customer Bridge MVRP address and EtherType (IEEE 802.1Q-2018 11.2.3.1.3, Tables 10-1 and 10-2) |

`adp` accepts a frame when one term holds (IEEE 1722.1-2021 6.2; Milan v1.2 5.6.3.1 and 5.6.4.1):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_zero` | 18 | 2 | `entity_id` | ENTITY_DISCOVER for every entity (Milan v1.2 5.6.3.1 step 2) |
| 1 | `eq_own` | 18 | 2 | `entity_id` | ENTITY_DISCOVER for this entity (Milan v1.2 5.6.3.1 step 2) |
| 2 | `eq_bound` | 18 | 0, 1 | `entity_id` | ENTITY_AVAILABLE and ENTITY_DEPARTING of a talker bound on the receiving interface (Milan v1.2 5.6.4.1; #665, comment 6029368753) |

`acmp` accepts a frame when one term holds (IEEE 1722.1-2021 8.2.1.9 and 8.2.1.10):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_own` | 34 | any | `talker_entity_id` | a command or response addressed to this entity's talker |
| 1 | `eq_own` | 42 | any | `listener_entity_id` | a command or response addressed to this entity's listener |

`aecp` accepts a frame when one term holds (IEEE 1722.1-2021 9.2.2.4 (Table 9-1), 9.2.2.7 and 9.2.2.8; Milan v1.2 5.4.5.3):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_own` | 18 | 0, 2, 4, 6, 8, 10, 12, 14 | `target_entity_id` | a command addressed to this entity |
| 1 | `eq_own` | 26 | 1, 3, 5, 7, 9, 11, 13, 15 | `controller_entity_id` | a response to a command this entity sent as a controller, such as CONTROLLER_AVAILABLE (Milan v1.2 5.4.5.3) |

`maap` accepts a frame when one term holds (IEEE 1722-2016 B.2.1, B.2.5, B.2.6 and note b of Table B.7):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `range_overlap` | 26 | 1, 2, 3 | `requested_start_address` | a PROBE, DEFEND or ANNOUNCE whose requested range conflicts with this entity's range |

`srp` accepts a frame when one term holds (IEEE 802.1Q-2018 35.2.2 (MSRP address and EtherType) and 11.2 (MVRP)):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `any` | 0 | any | `MRPDU` | every MSRP and MVRP PDU; both are link-local to this port |

| Destination | Value | Holds when |
|---|---:|---|
| `none` | 0 | never (an unused tuple) |
| `mac` | 1 | the destination MAC is the tuple's address |
| `own` | 2 | the destination MAC is OWN_MAC of the interface the frame arrived on |

| Test | Value | Holds when |
|---|---:|---|
| `none` | 0 | never (an unused term) |
| `any` | 1 | always |
| `eq_own` | 2 | the 8-byte big-endian field equals OWN_EID |
| `eq_zero` | 3 | the 8-byte field is 0 |
| `range_overlap` | 4 | the 6-byte start and 2-byte count overlap [MAAP_BASE, MAAP_BASE + MAAP_COUNT - 1] |
| `eq_bound` | 5 | the 8-byte big-endian field equals an enabled entry (BOUND_EID, BOUND_EN) of the arrival interface's bound-talker table |

## Constants

Every constant below is `MBX_<name>` in C and `MBX_<name>_C` in SystemVerilog.
`gen_mailbox.py --selftest` reads this table back.

| Name | Value |
|---|---:|
| `MBX_VERSION_MAJOR` | `0x2` |
| `MBX_VERSION_MINOR` | `0x2` |
| `MBX_MAGIC` | `0x4d42` |
| `MBX_WINDOW_BYTES` | `0x8000` |
| `MBX_REGISTER_SPACE_BYTES` | `0x400` |
| `MBX_N_IF` | `0x1` |
| `MBX_N_TIMERS` | `0x10` |
| `MBX_N_BOUND` | `0x10` |
| `MBX_N_PUB_SOURCES` | `0x10` |
| `MBX_N_PUB_SINKS` | `0x10` |
| `MBX_TICK_MS` | `0xa` |
| `MBX_N_CH` | `0x5` |
| `MBX_INDEX_BITS` | `0x10` |
| `MBX_MAX_TERMS` | `0x3` |
| `MBX_MAX_TUPLES` | `0x2` |
| `MBX_TERM_FIELD_BYTES` | `0x8` |
| `MBX_DST_BYTE` | `0x0` |
| `MBX_ETHERTYPE_BYTE` | `0xc` |
| `MBX_SUBTYPE_BYTE` | `0xe` |
| `MBX_MSG_TYPE_BYTE` | `0xf` |
| `MBX_DST_NONE` | `0x0` |
| `MBX_DST_MAC` | `0x1` |
| `MBX_DST_OWN` | `0x2` |
| `MBX_TEST_NONE` | `0x0` |
| `MBX_TEST_ANY` | `0x1` |
| `MBX_TEST_EQ_OWN` | `0x2` |
| `MBX_TEST_EQ_ZERO` | `0x3` |
| `MBX_TEST_RANGE_OVERLAP` | `0x4` |
| `MBX_TEST_EQ_BOUND` | `0x5` |
| `MBX_TMR_OP_ARM` | `0x1` |
| `MBX_TMR_OP_CANCEL` | `0x2` |
| `MBX_REG_ID` | `0x0` |
| `MBX_ID_MINOR_LSB` | `0x0` |
| `MBX_ID_MINOR_WIDTH` | `0x8` |
| `MBX_ID_MAJOR_LSB` | `0x8` |
| `MBX_ID_MAJOR_WIDTH` | `0x8` |
| `MBX_ID_MAGIC_LSB` | `0x10` |
| `MBX_ID_MAGIC_WIDTH` | `0x10` |
| `MBX_REG_CAPS` | `0x4` |
| `MBX_CAPS_N_CH_LSB` | `0x0` |
| `MBX_CAPS_N_CH_WIDTH` | `0x4` |
| `MBX_CAPS_N_IF_LSB` | `0x4` |
| `MBX_CAPS_N_IF_WIDTH` | `0x4` |
| `MBX_CAPS_N_TIMERS_LSB` | `0x8` |
| `MBX_CAPS_N_TIMERS_WIDTH` | `0x8` |
| `MBX_CAPS_EVT_WORDS_LOG2_LSB` | `0x10` |
| `MBX_CAPS_EVT_WORDS_LOG2_WIDTH` | `0x4` |
| `MBX_REG_IRQ_STATUS` | `0x8` |
| `MBX_IRQ_STATUS_RX_LSB` | `0x0` |
| `MBX_IRQ_STATUS_RX_WIDTH` | `0x8` |
| `MBX_IRQ_STATUS_EVT_LSB` | `0x8` |
| `MBX_IRQ_STATUS_EVT_WIDTH` | `0x1` |
| `MBX_IRQ_STATUS_ERR_LSB` | `0x1f` |
| `MBX_IRQ_STATUS_ERR_WIDTH` | `0x1` |
| `MBX_REG_IRQ_ENABLE` | `0xc` |
| `MBX_IRQ_ENABLE_RX_LSB` | `0x0` |
| `MBX_IRQ_ENABLE_RX_WIDTH` | `0x8` |
| `MBX_IRQ_ENABLE_EVT_LSB` | `0x8` |
| `MBX_IRQ_ENABLE_EVT_WIDTH` | `0x1` |
| `MBX_IRQ_ENABLE_ERR_LSB` | `0x1f` |
| `MBX_IRQ_ENABLE_ERR_WIDTH` | `0x1` |
| `MBX_REG_NOW_MS` | `0x10` |
| `MBX_NOW_MS_MS_LSB` | `0x0` |
| `MBX_NOW_MS_MS_WIDTH` | `0x20` |
| `MBX_REG_LINK` | `0x14` |
| `MBX_LINK_UP_LSB` | `0x0` |
| `MBX_LINK_UP_WIDTH` | `0x4` |
| `MBX_REG_TICK_CTL` | `0x18` |
| `MBX_TICK_CTL_EN_LSB` | `0x0` |
| `MBX_TICK_CTL_EN_WIDTH` | `0x1` |
| `MBX_REG_OWN_EID_LO` | `0x20` |
| `MBX_OWN_EID_LO_EID_LSB` | `0x0` |
| `MBX_OWN_EID_LO_EID_WIDTH` | `0x20` |
| `MBX_REG_OWN_EID_HI` | `0x24` |
| `MBX_OWN_EID_HI_EID_LSB` | `0x0` |
| `MBX_OWN_EID_HI_EID_WIDTH` | `0x20` |
| `MBX_REG_FILTER_EN` | `0x28` |
| `MBX_FILTER_EN_OPEN_LSB` | `0x0` |
| `MBX_FILTER_EN_OPEN_WIDTH` | `0x8` |
| `MBX_REG_MAAP_BASE_LO` | `0x2c` |
| `MBX_MAAP_BASE_LO_ADDR_LSB` | `0x0` |
| `MBX_MAAP_BASE_LO_ADDR_WIDTH` | `0x20` |
| `MBX_REG_MAAP_BASE_HI` | `0x30` |
| `MBX_MAAP_BASE_HI_ADDR_LSB` | `0x0` |
| `MBX_MAAP_BASE_HI_ADDR_WIDTH` | `0x10` |
| `MBX_REG_MAAP_COUNT` | `0x34` |
| `MBX_MAAP_COUNT_COUNT_LSB` | `0x0` |
| `MBX_MAAP_COUNT_COUNT_WIDTH` | `0x10` |
| `MBX_REG_TMR_DEADLINE` | `0x38` |
| `MBX_TMR_DEADLINE_MS_LSB` | `0x0` |
| `MBX_TMR_DEADLINE_MS_WIDTH` | `0x20` |
| `MBX_REG_TMR_CMD` | `0x3c` |
| `MBX_TMR_CMD_SLOT_LSB` | `0x0` |
| `MBX_TMR_CMD_SLOT_WIDTH` | `0x8` |
| `MBX_TMR_CMD_TAG_LSB` | `0x8` |
| `MBX_TMR_CMD_TAG_WIDTH` | `0x10` |
| `MBX_TMR_CMD_OP_LSB` | `0x1e` |
| `MBX_TMR_CMD_OP_WIDTH` | `0x2` |
| `MBX_REG_EVT_HEAD` | `0x60` |
| `MBX_EVT_HEAD_WORDS_LSB` | `0x0` |
| `MBX_EVT_HEAD_WORDS_WIDTH` | `0x10` |
| `MBX_REG_EVT_TAIL` | `0x64` |
| `MBX_EVT_TAIL_WORDS_LSB` | `0x0` |
| `MBX_EVT_TAIL_WORDS_WIDTH` | `0x10` |
| `MBX_REG_BUS_ERR` | `0x70` |
| `MBX_BUS_ERR_COUNT_LSB` | `0x0` |
| `MBX_BUS_ERR_COUNT_WIDTH` | `0x10` |
| `MBX_REG_FILTER_MISMATCH` | `0x74` |
| `MBX_FILTER_MISMATCH_COUNT_LSB` | `0x0` |
| `MBX_FILTER_MISMATCH_COUNT_WIDTH` | `0x10` |
| `MBX_IF_BASE` | `0x40` |
| `MBX_IF_STRIDE` | `0x10` |
| `MBX_IF_REG_GM_LO` | `0x0` |
| `MBX_GM_LO_ID_LSB` | `0x0` |
| `MBX_GM_LO_ID_WIDTH` | `0x20` |
| `MBX_IF_REG_GM_HI` | `0x4` |
| `MBX_GM_HI_ID_LSB` | `0x0` |
| `MBX_GM_HI_ID_WIDTH` | `0x20` |
| `MBX_IF_REG_DOMAIN` | `0x8` |
| `MBX_DOMAIN_NUMBER_LSB` | `0x0` |
| `MBX_DOMAIN_NUMBER_WIDTH` | `0x8` |
| `MBX_IFF_BASE` | `0x80` |
| `MBX_IFF_STRIDE` | `0x8` |
| `MBX_IFF_REG_OWN_MAC_LO` | `0x0` |
| `MBX_OWN_MAC_LO_MAC_LSB` | `0x0` |
| `MBX_OWN_MAC_LO_MAC_WIDTH` | `0x20` |
| `MBX_IFF_REG_OWN_MAC_HI` | `0x4` |
| `MBX_OWN_MAC_HI_MAC_LSB` | `0x0` |
| `MBX_OWN_MAC_HI_MAC_WIDTH` | `0x10` |
| `MBX_BND_BASE` | `0x200` |
| `MBX_BND_STRIDE` | `0x100` |
| `MBX_BND_ENTRY_STRIDE` | `0x10` |
| `MBX_BND_REG_BOUND_EID_LO` | `0x0` |
| `MBX_BOUND_EID_LO_EID_LSB` | `0x0` |
| `MBX_BOUND_EID_LO_EID_WIDTH` | `0x20` |
| `MBX_BND_REG_BOUND_EID_HI` | `0x4` |
| `MBX_BOUND_EID_HI_EID_LSB` | `0x0` |
| `MBX_BOUND_EID_HI_EID_WIDTH` | `0x20` |
| `MBX_BND_REG_BOUND_EN` | `0x8` |
| `MBX_BOUND_EN_EN_LSB` | `0x0` |
| `MBX_BOUND_EN_EN_WIDTH` | `0x1` |
| `MBX_PUB_BASE` | `0x800` |
| `MBX_PUB_STRIDE` | `0x200` |
| `MBX_PUB_REG_DA_GATE` | `0x0` |
| `MBX_DA_GATE_OPEN_LSB` | `0x0` |
| `MBX_DA_GATE_OPEN_WIDTH` | `0x10` |
| `MBX_PUB_REG_LICENCE` | `0x4` |
| `MBX_LICENCE_ACTIVE_LSB` | `0x0` |
| `MBX_LICENCE_ACTIVE_WIDTH` | `0x10` |
| `MBX_PUB_REG_IDLE_SLOPE` | `0x8` |
| `MBX_IDLE_SLOPE_BPS_LSB` | `0x0` |
| `MBX_IDLE_SLOPE_BPS_WIDTH` | `0x20` |
| `MBX_PUB_REG_SR_DOMAIN` | `0xc` |
| `MBX_SR_DOMAIN_VID_LSB` | `0x0` |
| `MBX_SR_DOMAIN_VID_WIDTH` | `0xc` |
| `MBX_SR_DOMAIN_PRIORITY_LSB` | `0x10` |
| `MBX_SR_DOMAIN_PRIORITY_WIDTH` | `0x3` |
| `MBX_SR_DOMAIN_ADOPTED_LSB` | `0x18` |
| `MBX_SR_DOMAIN_ADOPTED_WIDTH` | `0x1` |
| `MBX_PUB_SINK_BASE` | `0x100` |
| `MBX_PUB_SINK_STRIDE` | `0x10` |
| `MBX_PUB_SINK_REG_SID_LO` | `0x0` |
| `MBX_SID_LO_SID_LSB` | `0x0` |
| `MBX_SID_LO_SID_WIDTH` | `0x20` |
| `MBX_PUB_SINK_REG_SID_HI` | `0x4` |
| `MBX_SID_HI_SID_LSB` | `0x0` |
| `MBX_SID_HI_SID_WIDTH` | `0x20` |
| `MBX_PUB_SINK_REG_BINDING` | `0x8` |
| `MBX_BINDING_BOUND_LSB` | `0x0` |
| `MBX_BINDING_BOUND_WIDTH` | `0x1` |
| `MBX_BINDING_SID_VALID_LSB` | `0x1` |
| `MBX_BINDING_SID_VALID_WIDTH` | `0x1` |
| `MBX_CH_BASE` | `0x100` |
| `MBX_CH_STRIDE` | `0x20` |
| `MBX_CH_REG_RX_HEAD` | `0x0` |
| `MBX_RX_HEAD_WORDS_LSB` | `0x0` |
| `MBX_RX_HEAD_WORDS_WIDTH` | `0x10` |
| `MBX_CH_REG_RX_TAIL` | `0x4` |
| `MBX_RX_TAIL_WORDS_LSB` | `0x0` |
| `MBX_RX_TAIL_WORDS_WIDTH` | `0x10` |
| `MBX_CH_REG_TX_HEAD` | `0x8` |
| `MBX_TX_HEAD_WORDS_LSB` | `0x0` |
| `MBX_TX_HEAD_WORDS_WIDTH` | `0x10` |
| `MBX_CH_REG_TX_TAIL` | `0xc` |
| `MBX_TX_TAIL_WORDS_LSB` | `0x0` |
| `MBX_TX_TAIL_WORDS_WIDTH` | `0x10` |
| `MBX_CH_REG_RX_DROP` | `0x10` |
| `MBX_RX_DROP_COUNT_LSB` | `0x0` |
| `MBX_RX_DROP_COUNT_WIDTH` | `0x10` |
| `MBX_CH_REG_RATE_DROP` | `0x14` |
| `MBX_RATE_DROP_COUNT_LSB` | `0x0` |
| `MBX_RATE_DROP_COUNT_WIDTH` | `0x10` |
| `MBX_CH_REG_TX_ERR` | `0x18` |
| `MBX_TX_ERR_COUNT_LSB` | `0x0` |
| `MBX_TX_ERR_COUNT_WIDTH` | `0x10` |
| `MBX_CH_REG_RX_PASS` | `0x1c` |
| `MBX_RX_PASS_COUNT_LSB` | `0x0` |
| `MBX_RX_PASS_COUNT_WIDTH` | `0x10` |
| `MBX_RX_KIND` | `0x1` |
| `MBX_RX_HDR_WORDS` | `0x2` |
| `MBX_TX_KIND` | `0x2` |
| `MBX_TX_HDR_WORDS` | `0x2` |
| `MBX_EV_WORDS` | `0x4` |
| `MBX_EVT_BASE` | `0x400` |
| `MBX_EVT_WORDS` | `0x40` |
| `MBX_RXREC_W0_LEN_LSB` | `0x0` |
| `MBX_RXREC_W0_LEN_WIDTH` | `0x10` |
| `MBX_RXREC_W0_IF_LSB` | `0x10` |
| `MBX_RXREC_W0_IF_WIDTH` | `0x4` |
| `MBX_RXREC_W0_KIND_LSB` | `0x1c` |
| `MBX_RXREC_W0_KIND_WIDTH` | `0x4` |
| `MBX_RXREC_W1_ARRIVAL_MS_LSB` | `0x0` |
| `MBX_RXREC_W1_ARRIVAL_MS_WIDTH` | `0x20` |
| `MBX_TXREC_W0_LEN_LSB` | `0x0` |
| `MBX_TXREC_W0_LEN_WIDTH` | `0x10` |
| `MBX_TXREC_W0_IF_LSB` | `0x10` |
| `MBX_TXREC_W0_IF_WIDTH` | `0x4` |
| `MBX_TXREC_W0_KIND_LSB` | `0x1c` |
| `MBX_TXREC_W0_KIND_WIDTH` | `0x4` |
| `MBX_TXREC_W1_SEQ_LSB` | `0x0` |
| `MBX_TXREC_W1_SEQ_WIDTH` | `0x10` |
| `MBX_TXREC_W1_RSVD_LSB` | `0x10` |
| `MBX_TXREC_W1_RSVD_WIDTH` | `0x10` |
| `MBX_EVREC_W0_TYPE_LSB` | `0x0` |
| `MBX_EVREC_W0_TYPE_WIDTH` | `0x8` |
| `MBX_EVREC_W0_IF_LSB` | `0x8` |
| `MBX_EVREC_W0_IF_WIDTH` | `0x4` |
| `MBX_EVREC_W0_SEQ_LSB` | `0x10` |
| `MBX_EVREC_W0_SEQ_WIDTH` | `0x10` |
| `MBX_EV_TYPE_TIMER` | `0x1` |
| `MBX_EV_TIMER_W1_TAG_LSB` | `0x0` |
| `MBX_EV_TIMER_W1_TAG_WIDTH` | `0x10` |
| `MBX_EV_TIMER_W1_SLOT_LSB` | `0x10` |
| `MBX_EV_TIMER_W1_SLOT_WIDTH` | `0x8` |
| `MBX_EV_TIMER_W2_DEADLINE_MS_LSB` | `0x0` |
| `MBX_EV_TIMER_W2_DEADLINE_MS_WIDTH` | `0x20` |
| `MBX_EV_TIMER_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_TIMER_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_EV_TYPE_LINK` | `0x2` |
| `MBX_EV_LINK_W1_UP_LSB` | `0x0` |
| `MBX_EV_LINK_W1_UP_WIDTH` | `0x1` |
| `MBX_EV_LINK_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_LINK_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_EV_TYPE_GM` | `0x3` |
| `MBX_EV_GM_W1_ID_LO_LSB` | `0x0` |
| `MBX_EV_GM_W1_ID_LO_WIDTH` | `0x20` |
| `MBX_EV_GM_W2_ID_HI_LSB` | `0x0` |
| `MBX_EV_GM_W2_ID_HI_WIDTH` | `0x20` |
| `MBX_EV_GM_W3_DOMAIN_LSB` | `0x0` |
| `MBX_EV_GM_W3_DOMAIN_WIDTH` | `0x8` |
| `MBX_EV_TYPE_TICK` | `0x4` |
| `MBX_EV_TICK_W1_COUNT_LSB` | `0x0` |
| `MBX_EV_TICK_W1_COUNT_WIDTH` | `0x10` |
| `MBX_EV_TICK_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_TICK_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_CH_ADP` | `0x0` |
| `MBX_CH_ADP_RX_BASE` | `0x1000` |
| `MBX_CH_ADP_RX_WORDS` | `0x100` |
| `MBX_CH_ADP_TX_BASE` | `0x1400` |
| `MBX_CH_ADP_TX_WORDS` | `0x80` |
| `MBX_CH_ADP_MAX_FRAME_BYTES` | `0x80` |
| `MBX_CH_ADP_RATE_BURST` | `0x8` |
| `MBX_CH_ADP_RATE_REFILL_MS` | `0xa` |
| `MBX_CH_ADP_M0_DST` | `0x1` |
| `MBX_CH_ADP_M0_DST_HI` | `0x91e0` |
| `MBX_CH_ADP_M0_DST_LO` | `0xf0010000` |
| `MBX_CH_ADP_M0_ETHERTYPE` | `0x22f0` |
| `MBX_CH_ADP_M0_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_ADP_M0_SUBTYPE` | `0xfa` |
| `MBX_CH_ADP_M0_MSG_MASK` | `0xffff` |
| `MBX_CH_ADP_M1_DST` | `0x0` |
| `MBX_CH_ADP_M1_DST_HI` | `0x0` |
| `MBX_CH_ADP_M1_DST_LO` | `0x0` |
| `MBX_CH_ADP_M1_ETHERTYPE` | `0x0` |
| `MBX_CH_ADP_M1_HAS_SUBTYPE` | `0x0` |
| `MBX_CH_ADP_M1_SUBTYPE` | `0x0` |
| `MBX_CH_ADP_M1_MSG_MASK` | `0x0` |
| `MBX_CH_ADP_T0_TEST` | `0x3` |
| `MBX_CH_ADP_T0_OFFSET` | `0x12` |
| `MBX_CH_ADP_T0_MSG_MASK` | `0x4` |
| `MBX_CH_ADP_T1_TEST` | `0x2` |
| `MBX_CH_ADP_T1_OFFSET` | `0x12` |
| `MBX_CH_ADP_T1_MSG_MASK` | `0x4` |
| `MBX_CH_ADP_T2_TEST` | `0x5` |
| `MBX_CH_ADP_T2_OFFSET` | `0x12` |
| `MBX_CH_ADP_T2_MSG_MASK` | `0x3` |
| `MBX_CH_ACMP` | `0x1` |
| `MBX_CH_ACMP_RX_BASE` | `0x1800` |
| `MBX_CH_ACMP_RX_WORDS` | `0x100` |
| `MBX_CH_ACMP_TX_BASE` | `0x1c00` |
| `MBX_CH_ACMP_TX_WORDS` | `0x100` |
| `MBX_CH_ACMP_MAX_FRAME_BYTES` | `0x80` |
| `MBX_CH_ACMP_RATE_BURST` | `0x10` |
| `MBX_CH_ACMP_RATE_REFILL_MS` | `0x5` |
| `MBX_CH_ACMP_M0_DST` | `0x1` |
| `MBX_CH_ACMP_M0_DST_HI` | `0x91e0` |
| `MBX_CH_ACMP_M0_DST_LO` | `0xf0010000` |
| `MBX_CH_ACMP_M0_ETHERTYPE` | `0x22f0` |
| `MBX_CH_ACMP_M0_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_ACMP_M0_SUBTYPE` | `0xfc` |
| `MBX_CH_ACMP_M0_MSG_MASK` | `0xffff` |
| `MBX_CH_ACMP_M1_DST` | `0x2` |
| `MBX_CH_ACMP_M1_DST_HI` | `0x0` |
| `MBX_CH_ACMP_M1_DST_LO` | `0x0` |
| `MBX_CH_ACMP_M1_ETHERTYPE` | `0x22f0` |
| `MBX_CH_ACMP_M1_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_ACMP_M1_SUBTYPE` | `0xfc` |
| `MBX_CH_ACMP_M1_MSG_MASK` | `0xffff` |
| `MBX_CH_ACMP_T0_TEST` | `0x2` |
| `MBX_CH_ACMP_T0_OFFSET` | `0x22` |
| `MBX_CH_ACMP_T0_MSG_MASK` | `0xffff` |
| `MBX_CH_ACMP_T1_TEST` | `0x2` |
| `MBX_CH_ACMP_T1_OFFSET` | `0x2a` |
| `MBX_CH_ACMP_T1_MSG_MASK` | `0xffff` |
| `MBX_CH_ACMP_T2_TEST` | `0x0` |
| `MBX_CH_ACMP_T2_OFFSET` | `0x0` |
| `MBX_CH_ACMP_T2_MSG_MASK` | `0x0` |
| `MBX_CH_AECP` | `0x2` |
| `MBX_CH_AECP_RX_BASE` | `0x2000` |
| `MBX_CH_AECP_RX_WORDS` | `0x200` |
| `MBX_CH_AECP_TX_BASE` | `0x2800` |
| `MBX_CH_AECP_TX_WORDS` | `0x200` |
| `MBX_CH_AECP_MAX_FRAME_BYTES` | `0x5ea` |
| `MBX_CH_AECP_RATE_BURST` | `0x10` |
| `MBX_CH_AECP_RATE_REFILL_MS` | `0x5` |
| `MBX_CH_AECP_M0_DST` | `0x2` |
| `MBX_CH_AECP_M0_DST_HI` | `0x0` |
| `MBX_CH_AECP_M0_DST_LO` | `0x0` |
| `MBX_CH_AECP_M0_ETHERTYPE` | `0x22f0` |
| `MBX_CH_AECP_M0_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_AECP_M0_SUBTYPE` | `0xfb` |
| `MBX_CH_AECP_M0_MSG_MASK` | `0xffff` |
| `MBX_CH_AECP_M1_DST` | `0x0` |
| `MBX_CH_AECP_M1_DST_HI` | `0x0` |
| `MBX_CH_AECP_M1_DST_LO` | `0x0` |
| `MBX_CH_AECP_M1_ETHERTYPE` | `0x0` |
| `MBX_CH_AECP_M1_HAS_SUBTYPE` | `0x0` |
| `MBX_CH_AECP_M1_SUBTYPE` | `0x0` |
| `MBX_CH_AECP_M1_MSG_MASK` | `0x0` |
| `MBX_CH_AECP_T0_TEST` | `0x2` |
| `MBX_CH_AECP_T0_OFFSET` | `0x12` |
| `MBX_CH_AECP_T0_MSG_MASK` | `0x5555` |
| `MBX_CH_AECP_T1_TEST` | `0x2` |
| `MBX_CH_AECP_T1_OFFSET` | `0x1a` |
| `MBX_CH_AECP_T1_MSG_MASK` | `0xaaaa` |
| `MBX_CH_AECP_T2_TEST` | `0x0` |
| `MBX_CH_AECP_T2_OFFSET` | `0x0` |
| `MBX_CH_AECP_T2_MSG_MASK` | `0x0` |
| `MBX_CH_MAAP` | `0x3` |
| `MBX_CH_MAAP_RX_BASE` | `0x3000` |
| `MBX_CH_MAAP_RX_WORDS` | `0x80` |
| `MBX_CH_MAAP_TX_BASE` | `0x3200` |
| `MBX_CH_MAAP_TX_WORDS` | `0x80` |
| `MBX_CH_MAAP_MAX_FRAME_BYTES` | `0x40` |
| `MBX_CH_MAAP_RATE_BURST` | `0x8` |
| `MBX_CH_MAAP_RATE_REFILL_MS` | `0x14` |
| `MBX_CH_MAAP_M0_DST` | `0x1` |
| `MBX_CH_MAAP_M0_DST_HI` | `0x91e0` |
| `MBX_CH_MAAP_M0_DST_LO` | `0xf000ff00` |
| `MBX_CH_MAAP_M0_ETHERTYPE` | `0x22f0` |
| `MBX_CH_MAAP_M0_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_MAAP_M0_SUBTYPE` | `0xfe` |
| `MBX_CH_MAAP_M0_MSG_MASK` | `0xffff` |
| `MBX_CH_MAAP_M1_DST` | `0x2` |
| `MBX_CH_MAAP_M1_DST_HI` | `0x0` |
| `MBX_CH_MAAP_M1_DST_LO` | `0x0` |
| `MBX_CH_MAAP_M1_ETHERTYPE` | `0x22f0` |
| `MBX_CH_MAAP_M1_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_MAAP_M1_SUBTYPE` | `0xfe` |
| `MBX_CH_MAAP_M1_MSG_MASK` | `0x4` |
| `MBX_CH_MAAP_T0_TEST` | `0x4` |
| `MBX_CH_MAAP_T0_OFFSET` | `0x1a` |
| `MBX_CH_MAAP_T0_MSG_MASK` | `0xe` |
| `MBX_CH_MAAP_T1_TEST` | `0x0` |
| `MBX_CH_MAAP_T1_OFFSET` | `0x0` |
| `MBX_CH_MAAP_T1_MSG_MASK` | `0x0` |
| `MBX_CH_MAAP_T2_TEST` | `0x0` |
| `MBX_CH_MAAP_T2_OFFSET` | `0x0` |
| `MBX_CH_MAAP_T2_MSG_MASK` | `0x0` |
| `MBX_CH_SRP` | `0x4` |
| `MBX_CH_SRP_RX_BASE` | `0x4000` |
| `MBX_CH_SRP_RX_WORDS` | `0x400` |
| `MBX_CH_SRP_TX_BASE` | `0x5000` |
| `MBX_CH_SRP_TX_WORDS` | `0x200` |
| `MBX_CH_SRP_MAX_FRAME_BYTES` | `0x5ea` |
| `MBX_CH_SRP_RATE_BURST` | `0x20` |
| `MBX_CH_SRP_RATE_REFILL_MS` | `0x2` |
| `MBX_CH_SRP_M0_DST` | `0x1` |
| `MBX_CH_SRP_M0_DST_HI` | `0x180` |
| `MBX_CH_SRP_M0_DST_LO` | `0xc200000e` |
| `MBX_CH_SRP_M0_ETHERTYPE` | `0x22ea` |
| `MBX_CH_SRP_M0_HAS_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_M0_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_M0_MSG_MASK` | `0xffff` |
| `MBX_CH_SRP_M1_DST` | `0x1` |
| `MBX_CH_SRP_M1_DST_HI` | `0x180` |
| `MBX_CH_SRP_M1_DST_LO` | `0xc2000021` |
| `MBX_CH_SRP_M1_ETHERTYPE` | `0x88f5` |
| `MBX_CH_SRP_M1_HAS_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_M1_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_M1_MSG_MASK` | `0xffff` |
| `MBX_CH_SRP_T0_TEST` | `0x1` |
| `MBX_CH_SRP_T0_OFFSET` | `0x0` |
| `MBX_CH_SRP_T0_MSG_MASK` | `0xffff` |
| `MBX_CH_SRP_T1_TEST` | `0x0` |
| `MBX_CH_SRP_T1_OFFSET` | `0x0` |
| `MBX_CH_SRP_T1_MSG_MASK` | `0x0` |
| `MBX_CH_SRP_T2_TEST` | `0x0` |
| `MBX_CH_SRP_T2_OFFSET` | `0x0` |
| `MBX_CH_SRP_T2_MSG_MASK` | `0x0` |
| `MBX_IF_W` | `0x1` |
| `MBX_CH_W` | `0x3` |
| `MBX_RING_AW` | `0xa` |
| `MBX_ADDR_W` | `0xd` |
| `MBX_FRAME_BYTES_MAX` | `0x5ea` |

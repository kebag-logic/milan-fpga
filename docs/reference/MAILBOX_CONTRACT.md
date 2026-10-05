<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Packet mailbox contract, generated reference

**GENERATED** by `sw/mailbox/gen_mailbox.py` from `sw/mailbox/mailbox.yaml`; do not hand-edit.
Regenerate with `python3 sw/mailbox/gen_mailbox.py --write`.

The design page is [MAILBOX_SPLIT.md](../design/MAILBOX_SPLIT.md).
This page is contract version 1.0.

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

A frame is classified by EtherType, and by AVTP subtype where the channel names one.
It passes when its channel is open and one accept term holds.
It must also fit max_frame_bytes and the free ring space.
Then the channel's token bucket must hold a token.

| Channel | id | receive ring | transmit ring | Max frame | Match | Rate |
|---|---:|---|---|---:|---|---|
| `adp` | 0 | `0x1000`, 256 words | `0x1400`, 128 words | 128 | `0x22F0`, subtype `0xFA` | burst 8, one token per 10 ms |
| `acmp` | 1 | `0x1800`, 256 words | `0x1C00`, 256 words | 128 | `0x22F0`, subtype `0xFC` | burst 16, one token per 5 ms |
| `aecp` | 2 | `0x2000`, 512 words | `0x2800`, 512 words | 1514 | `0x22F0`, subtype `0xFB` | burst 16, one token per 5 ms |
| `maap` | 3 | `0x3000`, 128 words | `0x3200`, 128 words | 64 | `0x22F0`, subtype `0xFE` | burst 8, one token per 20 ms |
| `srp` | 4 | `0x4000`, 1024 words | `0x5000`, 512 words | 1514 | `0x22EA` or `0x88F5` | burst 32, one token per 2 ms |

`adp` accepts a frame when one term holds (IEEE 1722.1-2021 6.2; Milan v1.2 5.6.3.1):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_zero` | 18 | 2 | `entity_id` | ENTITY_DISCOVER for every entity (Milan v1.2 5.6.3.1 step 2) |
| 1 | `eq_own` | 18 | 2 | `entity_id` | ENTITY_DISCOVER for this entity (Milan v1.2 5.6.3.1 step 2) |

`acmp` accepts a frame when one term holds (IEEE 1722.1-2021 8.2.1.9 and 8.2.1.10):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_own` | 34 | any | `talker_entity_id` | a command or response addressed to this entity's talker |
| 1 | `eq_own` | 42 | any | `listener_entity_id` | a command or response addressed to this entity's listener |

`aecp` accepts a frame when one term holds (IEEE 1722.1-2021 9.2.2.7 (target_entity_id)):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `eq_own` | 18 | any | `target_entity_id` | a command addressed to this entity |

`maap` accepts a frame when one term holds (IEEE 1722-2016 B.2.5, B.2.6 and note b of Table B.7):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `range_overlap` | 26 | 1, 2, 3 | `requested_start_address` | a PROBE, DEFEND or ANNOUNCE whose requested range conflicts with this entity's range |

`srp` accepts a frame when one term holds (IEEE 802.1Q-2018 35.2.2 (MSRP address and EtherType) and 11.2 (MVRP)):

| Term | Test | Wire byte | message_type | Field | Why |
|---|---|---:|---|---|---|
| 0 | `any` | 0 | any | `MRPDU` | every MSRP and MVRP PDU; both are link-local to this port |

| Test | Value | Holds when |
|---|---:|---|
| `none` | 0 | never (an unused term) |
| `any` | 1 | always |
| `eq_own` | 2 | the 8-byte big-endian field equals OWN_EID |
| `eq_zero` | 3 | the 8-byte field is 0 |
| `range_overlap` | 4 | the 6-byte start and 2-byte count overlap [MAAP_BASE, MAAP_BASE + MAAP_COUNT - 1] |

## Constants

Every constant below is `MBX_<name>` in C and `MBX_<name>_C` in SystemVerilog.
`gen_mailbox.py --selftest` reads this table back.

| Name | Value |
|---|---:|
| `MBX_VERSION_MAJOR` | `0x1` |
| `MBX_VERSION_MINOR` | `0x0` |
| `MBX_MAGIC` | `0x4d42` |
| `MBX_WINDOW_BYTES` | `0x8000` |
| `MBX_REGISTER_SPACE_BYTES` | `0x400` |
| `MBX_N_IF` | `0x1` |
| `MBX_N_TIMERS` | `0x10` |
| `MBX_TICK_MS` | `0xa` |
| `MBX_N_CH` | `0x5` |
| `MBX_INDEX_BITS` | `0x10` |
| `MBX_MAX_TERMS` | `0x2` |
| `MBX_TERM_FIELD_BYTES` | `0x8` |
| `MBX_ETHERTYPE_BYTE` | `0xc` |
| `MBX_SUBTYPE_BYTE` | `0xe` |
| `MBX_MSG_TYPE_BYTE` | `0xf` |
| `MBX_TEST_NONE` | `0x0` |
| `MBX_TEST_ANY` | `0x1` |
| `MBX_TEST_EQ_OWN` | `0x2` |
| `MBX_TEST_EQ_ZERO` | `0x3` |
| `MBX_TEST_RANGE_OVERLAP` | `0x4` |
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
| `MBX_CH_ADP_ETHERTYPE0` | `0x22f0` |
| `MBX_CH_ADP_ETHERTYPE1` | `0x22f0` |
| `MBX_CH_ADP_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_ADP_SUBTYPE` | `0xfa` |
| `MBX_CH_ADP_RATE_BURST` | `0x8` |
| `MBX_CH_ADP_RATE_REFILL_MS` | `0xa` |
| `MBX_CH_ADP_T0_TEST` | `0x3` |
| `MBX_CH_ADP_T0_OFFSET` | `0x12` |
| `MBX_CH_ADP_T0_MSG_MASK` | `0x4` |
| `MBX_CH_ADP_T1_TEST` | `0x2` |
| `MBX_CH_ADP_T1_OFFSET` | `0x12` |
| `MBX_CH_ADP_T1_MSG_MASK` | `0x4` |
| `MBX_CH_ACMP` | `0x1` |
| `MBX_CH_ACMP_RX_BASE` | `0x1800` |
| `MBX_CH_ACMP_RX_WORDS` | `0x100` |
| `MBX_CH_ACMP_TX_BASE` | `0x1c00` |
| `MBX_CH_ACMP_TX_WORDS` | `0x100` |
| `MBX_CH_ACMP_MAX_FRAME_BYTES` | `0x80` |
| `MBX_CH_ACMP_ETHERTYPE0` | `0x22f0` |
| `MBX_CH_ACMP_ETHERTYPE1` | `0x22f0` |
| `MBX_CH_ACMP_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_ACMP_SUBTYPE` | `0xfc` |
| `MBX_CH_ACMP_RATE_BURST` | `0x10` |
| `MBX_CH_ACMP_RATE_REFILL_MS` | `0x5` |
| `MBX_CH_ACMP_T0_TEST` | `0x2` |
| `MBX_CH_ACMP_T0_OFFSET` | `0x22` |
| `MBX_CH_ACMP_T0_MSG_MASK` | `0xffff` |
| `MBX_CH_ACMP_T1_TEST` | `0x2` |
| `MBX_CH_ACMP_T1_OFFSET` | `0x2a` |
| `MBX_CH_ACMP_T1_MSG_MASK` | `0xffff` |
| `MBX_CH_AECP` | `0x2` |
| `MBX_CH_AECP_RX_BASE` | `0x2000` |
| `MBX_CH_AECP_RX_WORDS` | `0x200` |
| `MBX_CH_AECP_TX_BASE` | `0x2800` |
| `MBX_CH_AECP_TX_WORDS` | `0x200` |
| `MBX_CH_AECP_MAX_FRAME_BYTES` | `0x5ea` |
| `MBX_CH_AECP_ETHERTYPE0` | `0x22f0` |
| `MBX_CH_AECP_ETHERTYPE1` | `0x22f0` |
| `MBX_CH_AECP_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_AECP_SUBTYPE` | `0xfb` |
| `MBX_CH_AECP_RATE_BURST` | `0x10` |
| `MBX_CH_AECP_RATE_REFILL_MS` | `0x5` |
| `MBX_CH_AECP_T0_TEST` | `0x2` |
| `MBX_CH_AECP_T0_OFFSET` | `0x12` |
| `MBX_CH_AECP_T0_MSG_MASK` | `0xffff` |
| `MBX_CH_AECP_T1_TEST` | `0x0` |
| `MBX_CH_AECP_T1_OFFSET` | `0x0` |
| `MBX_CH_AECP_T1_MSG_MASK` | `0x0` |
| `MBX_CH_MAAP` | `0x3` |
| `MBX_CH_MAAP_RX_BASE` | `0x3000` |
| `MBX_CH_MAAP_RX_WORDS` | `0x80` |
| `MBX_CH_MAAP_TX_BASE` | `0x3200` |
| `MBX_CH_MAAP_TX_WORDS` | `0x80` |
| `MBX_CH_MAAP_MAX_FRAME_BYTES` | `0x40` |
| `MBX_CH_MAAP_ETHERTYPE0` | `0x22f0` |
| `MBX_CH_MAAP_ETHERTYPE1` | `0x22f0` |
| `MBX_CH_MAAP_HAS_SUBTYPE` | `0x1` |
| `MBX_CH_MAAP_SUBTYPE` | `0xfe` |
| `MBX_CH_MAAP_RATE_BURST` | `0x8` |
| `MBX_CH_MAAP_RATE_REFILL_MS` | `0x14` |
| `MBX_CH_MAAP_T0_TEST` | `0x4` |
| `MBX_CH_MAAP_T0_OFFSET` | `0x1a` |
| `MBX_CH_MAAP_T0_MSG_MASK` | `0xe` |
| `MBX_CH_MAAP_T1_TEST` | `0x0` |
| `MBX_CH_MAAP_T1_OFFSET` | `0x0` |
| `MBX_CH_MAAP_T1_MSG_MASK` | `0x0` |
| `MBX_CH_SRP` | `0x4` |
| `MBX_CH_SRP_RX_BASE` | `0x4000` |
| `MBX_CH_SRP_RX_WORDS` | `0x400` |
| `MBX_CH_SRP_TX_BASE` | `0x5000` |
| `MBX_CH_SRP_TX_WORDS` | `0x200` |
| `MBX_CH_SRP_MAX_FRAME_BYTES` | `0x5ea` |
| `MBX_CH_SRP_ETHERTYPE0` | `0x22ea` |
| `MBX_CH_SRP_ETHERTYPE1` | `0x88f5` |
| `MBX_CH_SRP_HAS_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_SUBTYPE` | `0x0` |
| `MBX_CH_SRP_RATE_BURST` | `0x20` |
| `MBX_CH_SRP_RATE_REFILL_MS` | `0x2` |
| `MBX_CH_SRP_T0_TEST` | `0x1` |
| `MBX_CH_SRP_T0_OFFSET` | `0x0` |
| `MBX_CH_SRP_T0_MSG_MASK` | `0xffff` |
| `MBX_CH_SRP_T1_TEST` | `0x0` |
| `MBX_CH_SRP_T1_OFFSET` | `0x0` |
| `MBX_CH_SRP_T1_MSG_MASK` | `0x0` |
| `MBX_IF_W` | `0x1` |
| `MBX_CH_W` | `0x3` |
| `MBX_RING_AW` | `0xa` |
| `MBX_ADDR_W` | `0xd` |
| `MBX_FRAME_BYTES_MAX` | `0x5ea` |

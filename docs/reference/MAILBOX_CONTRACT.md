<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Packet mailbox contract, generated reference

**GENERATED** by `sw/mailbox/gen_mailbox.py` from `sw/mailbox/mailbox.yaml`; do not hand-edit.
Regenerate with `python3 sw/mailbox/gen_mailbox.py --write`.

The design page is [MAILBOX_SPLIT.md](../design/MAILBOX_SPLIT.md).
This page is contract version 2.4.

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
| `0x000` | `DA_GATE` | rw | The talker declaration gate: bit s is set when source s on this interface has a valid destination address and either an answered probe younger than T-SRP-DAFRESH (15000 ms) or a registered Listener (Milan v1.2 4.3.3.1). This is the processor's acmp_declaring_o predicate. The MAAP adapter publishes it before each allocation report and refreshes it after service, including idle service ticks. Invalid destinations, absent demand and expired probe demand close the gate. Any matching Listener counts, including Asking Failed; LICENCE remains separate. |
| `0x004` | `LICENCE` | rw | The SRP stream gate: bit s is set while source s holds its licence, an admitted Talker Advertise with a registered Listener Ready or Ready Failed after the stream VLAN's MVRP Join (Milan v1.2 5.3.7.3 and 4.3.2; the processor's srp_active_o AND srp_sr_admitted_o). The SRP owner writes it before it reports the licence. |
| `0x008` | `IDLE_SLOPE` | rw | The sum, in bits per second, of the bandwidth the SRP owner admitted for this interface's sources, Ethernet overhead included (the processor's srp_sum_slope_bps_o), written before the declarations it admitted are sent. |
| `0x00C` | `SR_DOMAIN` | rw | The SR class A Domain this interface's declarations carry (Milan v1.2 4.2.7.2.1). ADOPTED is set once a received Domain replaced the default {priority 3, VID 2}, until the link restarts (the processor's srp_domain_adopted_o, class_a_prio_o and class_a_vid_o). Written in one access, before the declarations that carry it. |
| `0x010` | `TALKER_DECL` | rw | The Talker declarations: bit s is set while source s's MSRP Talker attribute, a Talker Advertise or a Talker Failed, is declared on this interface (IEEE 802.1Q-2018 clause 35; the processor's srp_tk_decl_state_o other than NONE). The datapath tags a stream's frames only while its bit is set, because a bridge prunes a tagged stream that is not declared (802.1Q 35.1.2). The SRP owner sets a bit before the declaration it describes is sent, and clears it before the declaration is destroyed. |

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

`TALKER_DECL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `DECLARED` | bit s: source s has a Talker declaration |

### Interface publication source registers

Source s's entry starts at `0x80 + 0x8 * s` inside interface i's publication block, for 16 sources (one per talker stream). A source past the last reads 0 and takes no write.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `SRC_SID_LO` | rw | Source s's current stream_id, low word: the ID its Talker attribute declares and its stream data AVTPDUs carry (IEEE 1722-2016 4.4.4.8; Milan v1.2 5.3.7.5 Table 5.3; the processor's src_stream_id_o). The datapath stamps SRC_SID_HI:SRC_SID_LO on source s's frames. The owner writes both words while source s's DA_GATE bit is clear, before it opens the gate and before the declaration or the PROBE_TX response that carries the ID, so no frame carries a half-written stream_id; after a MAAP conflict the gate is closed until the new allocation (Milan v1.2 5.5.4.1; protocol-processor #202). |
| `0x004` | `SRC_SID_HI` | rw | Source s's current stream_id, high word, written with SRC_SID_LO. |

`SRC_SID_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `SID` | stream_id[31:0] |

`SRC_SID_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `SID` | stream_id[63:32] |

### Interface publication sink registers

Sink k's entry starts at `0x100 + 0x10 * k` inside interface i's publication block, for 16 sinks (one per listener stream). A hole, a sink past the last and an interface the build does not have read 0 and take no write.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `SID_LO` | rw | Sink k's stream_id, low word, as last written. The datapath reads it while SID_VALID is set. |
| `0x004` | `SID_HI` | rw | Sink k's stream_id, high word, as last written. The datapath reads it while SID_VALID is set. |
| `0x008` | `BINDING` | rw | Sink k's binding. BOUND is the bound state (Milan v1.2 5.3.8.2; the processor's acmp_bound_o), written before the BIND_RX or UNBIND_RX response. SID_VALID says SID_LO and SID_HI hold the stream_id the sink settled on (5.5.3.5.18 step 4, 5.3.8.9; the processor's acmp_bound_sid_o); the datapath takes the stream_id only while it is set. The firmware clears SID_VALID before it rewrites SID_LO and SID_HI and sets it after, so a half-written stream_id never reaches the datapath. STARTED is the started state (5.3.8.7; the processor wrapper's aecp_strm_started_o, which the ACMP binding record owns), 0 while the sink is unbound: the datapath discards the AVTPDUs of a sink that is bound and not started. The firmware writes it before the BIND_RX response that echoes STREAMING_WAIT and before a later START_STREAMING or STOP_STREAMING is reported, in one write that keeps SID_VALID. |

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
| `[2]` | `STARTED` | the bound sink is started |
| `[1]` | `SID_VALID` | SID_LO and SID_HI are the settled stream_id |
| `[0]` | `BOUND` | the sink is bound |

### Interface face registers

Interface i's face block starts at `0x6000 + 0x400 * i`. The firmware writes the `F_*` settings, then `F_COMMIT`: `KL_mbx`'s `fw_send_o` rises and every setting holds on its `fw_*_o` port until the datapath's acknowledgement `fw_ack_p_i`, within 64 cycles. A window's `CMD.GO` opens a request held on its ports with its tag until the answer carrying that tag, or the window's timeout. A write that would move a held value is refused and counted in `BUS_ERR`.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `F_CTRL` | rw | The control plane's ready level, in place of the processor's enable_i and restore_go_i (Milan v1.2 5.6.1): set once the saved state is applied and AECP is released, so the datapath sees no entity before the restored state. |
| `0x004` | `F_ENTITY` | rw | The entity's current configuration (IEEE 1722.1-2021 7.4.7; the processor's aecp_cur_config_o) and its IDENTIFY control value, 0 or 255 (Milan v1.2 5.4.2.12; aecp_identify_o). |
| `0x008` | `F_CLOCK` | rw | CLOCK_DOMAIN 0's clock_source_index as SET_CLOCK_SOURCE set it (IEEE 1722.1-2021 7.4.23; the processor's aecp_clk_src_index_o), which the media clock resolves. |
| `0x00C` | `F_AECP` | rw | LOCK_HELD is set while a LOCK_ENTITY is held (IEEE 1722.1-2021 7.4.2; Milan v1.2 5.4.2.27 and 5.4.2.28 forbid a local map change meanwhile; the processor's aecp_lock_held_o). DYN_DIRTY is set while a persisted setting moved and is not saved (aecp_dyn_dirty_o). |
| `0x010` | `F_RESTORE` | rw | The saved-state restore's status, as the processor's restore_*_o and rs_cause_o report it to the CSRs: the firmware's saved-state store writes it before AECP is released and again on every change. |
| `0x014` | `F_NVM` | rw | The saved-state store's status, as the processor's nvm_*_o report it to the CSRs: written before AECP is released and again on every change. |
| `0x018` | `F_COMMIT` | wo | Writing GO publishes every F_* value of this interface: fw_send_o rises and the values hold until the acknowledgement. Refused while F_STATUS.BUSY is set. |
| `0x01C` | `F_STATUS` | ro | The commit handshake. BUSY is set from a commit until its acknowledgement returns. |
| `0x040` | `CTR_REQ` | rw | The descriptor GET_COUNTERS asks about. |
| `0x044` | `CTR_WORD` | rw | The quadlet asked for, 0 to 31 a counters_block quadlet, 32 the counters_valid mask. |
| `0x048` | `CTR_CMD` | wo | Writing GO asks the datapath for the quadlet. Refused while CTR_STATUS.BUSY is set. |
| `0x04C` | `CTR_STATUS` | ro | The window's request, open or answered. |
| `0x050` | `CTR_DATA` | ro | The quadlet, in IEEE 1722.1 value order. |
| `0x060` | `AMAP_REQ` | rw | The Stream Port the read asks about. |
| `0x064` | `AMAP_PAGE` | rw | The word asked for. |
| `0x068` | `AMAP_CMD` | wo | Writing GO asks the datapath for the word. Refused while AMAP_STATUS.BUSY is set. |
| `0x06C` | `AMAP_STATUS` | ro | The window's request, open or answered. |
| `0x070` | `AMAP_DATA_LO` | ro | The word, low half. |
| `0x074` | `AMAP_DATA_HI` | ro | The word, high half (0 unless a mapping record). |
| `0x080` | `EDIT_REQ` | rw | The Stream Port the transaction edits. |
| `0x084` | `EDIT_BEAT` | rw | One beat of the transaction: PHASE 0 begins validation, 1 begins the commit, 2 finishes, 3 aborts, 4 validates record REC and 5 commits it; REMOVE names a REMOVE_AUDIO_MAPPINGS; COUNT the records. |
| `0x088` | `EDIT_RECORD_LO` | rw | The mapping record, low half (mapping_cluster_offset, mapping_cluster_channel). |
| `0x08C` | `EDIT_RECORD_HI` | rw | The mapping record, high half (mapping_stream_index, mapping_stream_channel). |
| `0x090` | `EDIT_VALUE_LO` | rw | The beat's value lane, low half (the processor's amap_edit_value_o). |
| `0x094` | `EDIT_VALUE_HI` | rw | The beat's value lane, high half. |
| `0x098` | `EDIT_CMD` | wo | Writing GO presents the beat. Refused while EDIT_STATUS.BUSY is set. |
| `0x09C` | `EDIT_STATUS` | ro | The window's request, open or answered. |
| `0x0A0` | `EDIT_DATA_LO` | ro | The beat's verdict, low half (bit 0 accepted, or for a finish a mapping changed). |
| `0x0A4` | `EDIT_DATA_HI` | ro | The beat's verdict, high half. |
| `0x0C0` | `GSI_REQ` | rw | The descriptor the word belongs to. |
| `0x0C4` | `GSI_SEL` | rw | The word asked for: KIND 0 GET_STREAM_INFO, 1 GET_AVB_INFO, 2 GET_AS_PATH; SEL the word within the kind (kind 0 selector 15 is SET_STREAM_FORMAT's verdict on GSI_PROP); ORD an array ordinal. |
| `0x0C8` | `GSI_PROP_LO` | rw | The proposed stream format kind 0 selector 15 judges, low half. |
| `0x0CC` | `GSI_PROP_HI` | rw | The proposed stream format, high half. |
| `0x0D0` | `GSI_CMD` | wo | Writing GO asks the datapath for the word. Refused while GSI_STATUS.BUSY is set. |
| `0x0D4` | `GSI_STATUS` | ro | The window's request, open or answered. |
| `0x0D8` | `GSI_DATA_LO` | ro | The word, low half. |
| `0x0DC` | `GSI_DATA_HI` | ro | The word, high half. |

`F_CTRL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `READY` | the firmware control plane is running |

`F_ENTITY` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[23:16]` | `IDENTIFY` | the IDENTIFY control's value |
| `[15:0]` | `CUR_CONFIG` | current_configuration |

`F_CLOCK` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:0]` | `SOURCE_INDEX` | clock_source_index |

`F_AECP` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[1]` | `DYN_DIRTY` | a persisted setting is not saved yet |
| `[0]` | `LOCK_HELD` | a LOCK_ENTITY is held |

`F_RESTORE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[13:12]` | `CAUSE` | the binding walk's cause: 1 torn, 2 device, 3 deadline |
| `[10:8]` | `RS_CAUSE` | the walk's abort cause: 1 torn, 2 device, 3 deadline, 5 passes disagree, 6 descriptor, 7 image |
| `[5]` | `RB` | the walk rolled back to the defaults |
| `[4]` | `CLOSED` | the walk ended CLOSED |
| `[3]` | `BLANK` | the completed walk validated no record |
| `[2]` | `FAIL` | the completed restore did not restore |
| `[1]` | `DONE` | the restore sequencing completed (not a verdict) |
| `[0]` | `BUSY` | the restore walk is running |

`F_NVM` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[11:8]` | `VERDICT` | the verdict on the last image offered |
| `[5]` | `IMG_VALID` | the image in the window was validated |
| `[4]` | `PEND` | accepted work no verified slot holds and DIRTY does not report |
| `[3]` | `STALE` | a writer loss not made good |
| `[2]` | `DIRTY` | committable work no slot holds |
| `[1]` | `ALARM` | a record producer exhausted its write attempts |
| `[0]` | `BACKED` | the store answers |

`F_COMMIT` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `GO` | publish |

`F_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `BUSY` | a commit waits for its acknowledgement |

`CTR_REQ` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `INDEX` | descriptor_index |
| `[15:0]` | `TYPE` | descriptor_type |

`CTR_WORD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[5:0]` | `WORD` | quadlet |

`CTR_CMD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `GO` | ask |

`CTR_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[11:8]` | `TAG` | the last request's tag |
| `[2]` | `TIMEOUT` | the last request had no answer within wait_cycles |
| `[1]` | `DONE` | the answer of the last request is in DATA |
| `[0]` | `BUSY` | the request is open |

`CTR_DATA` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | the quadlet |

`AMAP_REQ` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `INDEX` | descriptor_index |
| `[15:0]` | `TYPE` | descriptor_type |

`AMAP_PAGE` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:24]` | `REC` | the record's ordinal within the page |
| `[17:16]` | `SEL` | 0 number_of_maps, 1 the page's geometry, 2 a mapping record |
| `[15:0]` | `MAP_INDEX` | map_index |

`AMAP_CMD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `GO` | ask |

`AMAP_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[11:8]` | `TAG` | the last request's tag |
| `[2]` | `TIMEOUT` | the last request had no answer within wait_cycles |
| `[1]` | `DONE` | the answer of the last request is in DATA |
| `[0]` | `BUSY` | the request is open |

`AMAP_DATA_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | word[31:0] |

`AMAP_DATA_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | word[63:32] |

`EDIT_REQ` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `INDEX` | descriptor_index |
| `[15:0]` | `TYPE` | descriptor_type |

`EDIT_BEAT` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `COUNT` | number_of_mappings |
| `[15:8]` | `REC` | the record's ordinal |
| `[4]` | `REMOVE` | a REMOVE_AUDIO_MAPPINGS |
| `[2:0]` | `PHASE` | the beat's phase |

`EDIT_RECORD_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `RECORD` | record[31:0] |

`EDIT_RECORD_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `RECORD` | record[63:32] |

`EDIT_VALUE_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `VALUE` | value[31:0] |

`EDIT_VALUE_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `VALUE` | value[63:32] |

`EDIT_CMD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `GO` | present the beat |

`EDIT_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[11:8]` | `TAG` | the last request's tag |
| `[2]` | `TIMEOUT` | the last request had no answer within wait_cycles |
| `[1]` | `DONE` | the answer of the last request is in DATA |
| `[0]` | `BUSY` | the request is open |

`EDIT_DATA_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | verdict[31:0] |

`EDIT_DATA_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | verdict[63:32] |

`GSI_REQ` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:16]` | `INDEX` | descriptor_index |
| `[15:0]` | `TYPE` | descriptor_type |

`GSI_SEL` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[15:8]` | `ORD` | the array ordinal |
| `[7:4]` | `SEL` | the word selector |
| `[1:0]` | `KIND` | the command family |

`GSI_PROP_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | format[31:0] |

`GSI_PROP_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | format[63:32] |

`GSI_CMD` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `GO` | ask |

`GSI_STATUS` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[11:8]` | `TAG` | the last request's tag |
| `[2]` | `TIMEOUT` | the last request had no answer within wait_cycles |
| `[1]` | `DONE` | the answer of the last request is in DATA |
| `[0]` | `BUSY` | the request is open |

`GSI_DATA_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | word[31:0] |

`GSI_DATA_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `DATA` | word[63:32] |

### Interface face source registers

Source s's entry starts at `0x100 + 0x10 * s` inside interface i's face block, for 16 sources (one per talker stream).

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `F_PT_OFFSET` | rw | Source s's presentation time offset, nanoseconds, as SET_STREAM_INFO's msrp_accumulated_latency set it (Milan v1.2 5.4.2.9; the processor's aecp_pt_offset_o), taken while F_SRC_VALID.PT_OFFSET is set. |
| `0x004` | `F_FMT_OUT_LO` | rw | Source s's stream_format, low half (Milan v1.2 5.4.2.7; aecp_fmt_out_o). |
| `0x008` | `F_FMT_OUT_HI` | rw | Source s's stream_format, high half. |
| `0x00C` | `F_SRC_VALID` | rw | Which of source s's settings a controller set (aecp_pt_offset_v_o, aecp_fmt_out_v_o). |

`F_PT_OFFSET` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `NS` | presentation time offset |

`F_FMT_OUT_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | stream_format[31:0] |

`F_FMT_OUT_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | stream_format[63:32] |

`F_SRC_VALID` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[1]` | `FMT_OUT` | F_FMT_OUT holds a set value |
| `[0]` | `PT_OFFSET` | F_PT_OFFSET holds a set value |

### Interface face sink registers

Sink k's entry starts at `0x200 + 0x10 * k` inside interface i's face block, for 16 sinks (one per listener stream). A hole, an entry past the last and an interface the build does not have read 0 and take no write.

| Offset | Register | Access | Meaning |
|---|---|---|---|
| `0x000` | `F_FMT_IN_LO` | rw | Sink k's stream_format, low half (Milan v1.2 5.4.2.7; aecp_fmt_in_o). |
| `0x004` | `F_FMT_IN_HI` | rw | Sink k's stream_format, high half. |
| `0x008` | `F_SNK_VALID` | rw | Whether a controller set sink k's format (aecp_fmt_in_v_o). |

`F_FMT_IN_LO` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | stream_format[31:0] |

`F_FMT_IN_HI` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[31:0]` | `FMT` | stream_format[63:32] |

`F_SNK_VALID` fields:

| Bits | Field | Meaning |
|---|---|---|
| `[0]` | `FMT_IN` | F_FMT_IN holds a set value |

### Face windows

| Window | GO | Status | Request | Answer | Answered or timed out within |
|---|---|---|---|---|---:|
| `CTR` | `CTR_CMD` | `CTR_STATUS` | `CTR_REQ`, `CTR_WORD` | `CTR_DATA` | 64 cycles |
| `AMAP` | `AMAP_CMD` | `AMAP_STATUS` | `AMAP_REQ`, `AMAP_PAGE` | `AMAP_DATA_LO`, `AMAP_DATA_HI` | 64 cycles |
| `EDIT` | `EDIT_CMD` | `EDIT_STATUS` | `EDIT_REQ`, `EDIT_BEAT`, `EDIT_RECORD_LO`, `EDIT_RECORD_HI`, `EDIT_VALUE_LO`, `EDIT_VALUE_HI` | `EDIT_DATA_LO`, `EDIT_DATA_HI` | 64 cycles |
| `GSI` | `GSI_CMD` | `GSI_STATUS` | `GSI_REQ`, `GSI_SEL`, `GSI_PROP_LO`, `GSI_PROP_HI` | `GSI_DATA_LO`, `GSI_DATA_HI` | 64 cycles |

### COUNTERS_CHANGED descriptors

One pending bit per entry below, per interface; a change naming any other descriptor sets the ALL bit. A descriptor posts at most once in each 1000 ms epoch of `NOW_MS`.

| Family | descriptor_type | Entries |
|---|---|---:|
| `STREAM_INPUT` | `0x0005` | 16 |
| `STREAM_OUTPUT` | `0x0006` | 16 |
| `AVB_INTERFACE` | `0x0009` | 1 |
| `CLOCK_DOMAIN` | `0x0024` | 1 |

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
| COUNTERS_CHANGED event | word 1 | `[31:16]` | `INDEX` | descriptor_index (0 with ALL) |
| COUNTERS_CHANGED event | word 1 | `[15:0]` | `TYPE` | descriptor_type (0 with ALL) |
| COUNTERS_CHANGED event | word 2 | `[0]` | `ALL` | every served descriptor may have moved |
| COUNTERS_CHANGED event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |
| AVB_INFO_CHANGED event | word 1 | `[15:0]` | `COUNT` | changes since the previous record |
| AVB_INFO_CHANGED event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |
| AS_PATH_CHANGED event | word 1 | `[15:0]` | `COUNT` | changes since the previous record |
| AS_PATH_CHANGED event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |
| AMAP_LIVE_WRITE event | word 1 | `[15:0]` | `COUNT` | live writes since the previous record |
| AMAP_LIVE_WRITE event | word 3 | `[31:0]` | `NOW_MS` | NOW_MS at posting |

An RX or TX record is the header words, then ceil(LEN/4) payload words.

| Event | TYPE | Meaning |
|---|---:|---|
| `TIMER` | 1 | A timer slot's deadline passed. |
| `LINK` | 2 | The interface's link level changed. |
| `GM` | 3 | The gPTP plane published a grandmaster change on the interface. |
| `TICK` | 4 | Centiseconds elapsed (TICK_CTL.EN set). COUNT is the ticks counted since the previous TICK record, at least 1 and saturating; the firmware calls its centisecond timer port COUNT times. |
| `COUNTERS_CHANGED` | 5 | The counters of a descriptor the datapath serves moved (the processor's ctr_change face; Milan v1.2 Table 5.22 makes it a GET_COUNTERS notification, at most one per descriptor per second). A descriptor that moves again before its record is posted, or within holdoff_ms of its last record, posts once. ALL set: a change named a descriptor the source keeps no bit for, so every served descriptor may have moved. |
| `AVB_INFO_CHANGED` | 6 | A GET_AVB_INFO word the datapath serves changed on the interface (the processor's gsi_avb_chg_i; Milan v1.2 Table 5.22). COUNT is the changes since the previous record, at least 1 and saturating. |
| `AS_PATH_CHANGED` | 7 | The AS_PATH sequence the datapath serves changed on the interface (the processor's gsi_asp_chg_i; Milan v1.2 Table 5.22). COUNT as for AVB_INFO_CHANGED. |
| `AMAP_LIVE_WRITE` | 8 | An edit's commit beat changed the live audio map (the processor's amap_live_wr_i). COUNT is the live writes since the previous record, at least 1 and saturating. |

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
| `MBX_VERSION_MINOR` | `0x4` |
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
| `MBX_PUB_REG_TALKER_DECL` | `0x10` |
| `MBX_TALKER_DECL_DECLARED_LSB` | `0x0` |
| `MBX_TALKER_DECL_DECLARED_WIDTH` | `0x10` |
| `MBX_PUB_SRC_BASE` | `0x80` |
| `MBX_PUB_SRC_STRIDE` | `0x8` |
| `MBX_PUB_SRC_REG_SRC_SID_LO` | `0x0` |
| `MBX_SRC_SID_LO_SID_LSB` | `0x0` |
| `MBX_SRC_SID_LO_SID_WIDTH` | `0x20` |
| `MBX_PUB_SRC_REG_SRC_SID_HI` | `0x4` |
| `MBX_SRC_SID_HI_SID_LSB` | `0x0` |
| `MBX_SRC_SID_HI_SID_WIDTH` | `0x20` |
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
| `MBX_BINDING_STARTED_LSB` | `0x2` |
| `MBX_BINDING_STARTED_WIDTH` | `0x1` |
| `MBX_FACE_BASE` | `0x6000` |
| `MBX_FACE_STRIDE` | `0x400` |
| `MBX_FACE_ACK_CYCLES` | `0x40` |
| `MBX_FACE_REG_F_CTRL` | `0x0` |
| `MBX_F_CTRL_READY_LSB` | `0x0` |
| `MBX_F_CTRL_READY_WIDTH` | `0x1` |
| `MBX_FACE_REG_F_ENTITY` | `0x4` |
| `MBX_F_ENTITY_CUR_CONFIG_LSB` | `0x0` |
| `MBX_F_ENTITY_CUR_CONFIG_WIDTH` | `0x10` |
| `MBX_F_ENTITY_IDENTIFY_LSB` | `0x10` |
| `MBX_F_ENTITY_IDENTIFY_WIDTH` | `0x8` |
| `MBX_FACE_REG_F_CLOCK` | `0x8` |
| `MBX_F_CLOCK_SOURCE_INDEX_LSB` | `0x0` |
| `MBX_F_CLOCK_SOURCE_INDEX_WIDTH` | `0x10` |
| `MBX_FACE_REG_F_AECP` | `0xc` |
| `MBX_F_AECP_LOCK_HELD_LSB` | `0x0` |
| `MBX_F_AECP_LOCK_HELD_WIDTH` | `0x1` |
| `MBX_F_AECP_DYN_DIRTY_LSB` | `0x1` |
| `MBX_F_AECP_DYN_DIRTY_WIDTH` | `0x1` |
| `MBX_FACE_REG_F_RESTORE` | `0x10` |
| `MBX_F_RESTORE_BUSY_LSB` | `0x0` |
| `MBX_F_RESTORE_BUSY_WIDTH` | `0x1` |
| `MBX_F_RESTORE_DONE_LSB` | `0x1` |
| `MBX_F_RESTORE_DONE_WIDTH` | `0x1` |
| `MBX_F_RESTORE_FAIL_LSB` | `0x2` |
| `MBX_F_RESTORE_FAIL_WIDTH` | `0x1` |
| `MBX_F_RESTORE_BLANK_LSB` | `0x3` |
| `MBX_F_RESTORE_BLANK_WIDTH` | `0x1` |
| `MBX_F_RESTORE_CLOSED_LSB` | `0x4` |
| `MBX_F_RESTORE_CLOSED_WIDTH` | `0x1` |
| `MBX_F_RESTORE_RB_LSB` | `0x5` |
| `MBX_F_RESTORE_RB_WIDTH` | `0x1` |
| `MBX_F_RESTORE_RS_CAUSE_LSB` | `0x8` |
| `MBX_F_RESTORE_RS_CAUSE_WIDTH` | `0x3` |
| `MBX_F_RESTORE_CAUSE_LSB` | `0xc` |
| `MBX_F_RESTORE_CAUSE_WIDTH` | `0x2` |
| `MBX_FACE_REG_F_NVM` | `0x14` |
| `MBX_F_NVM_BACKED_LSB` | `0x0` |
| `MBX_F_NVM_BACKED_WIDTH` | `0x1` |
| `MBX_F_NVM_ALARM_LSB` | `0x1` |
| `MBX_F_NVM_ALARM_WIDTH` | `0x1` |
| `MBX_F_NVM_DIRTY_LSB` | `0x2` |
| `MBX_F_NVM_DIRTY_WIDTH` | `0x1` |
| `MBX_F_NVM_STALE_LSB` | `0x3` |
| `MBX_F_NVM_STALE_WIDTH` | `0x1` |
| `MBX_F_NVM_PEND_LSB` | `0x4` |
| `MBX_F_NVM_PEND_WIDTH` | `0x1` |
| `MBX_F_NVM_IMG_VALID_LSB` | `0x5` |
| `MBX_F_NVM_IMG_VALID_WIDTH` | `0x1` |
| `MBX_F_NVM_VERDICT_LSB` | `0x8` |
| `MBX_F_NVM_VERDICT_WIDTH` | `0x4` |
| `MBX_FACE_REG_F_COMMIT` | `0x18` |
| `MBX_F_COMMIT_GO_LSB` | `0x0` |
| `MBX_F_COMMIT_GO_WIDTH` | `0x1` |
| `MBX_FACE_REG_F_STATUS` | `0x1c` |
| `MBX_F_STATUS_BUSY_LSB` | `0x0` |
| `MBX_F_STATUS_BUSY_WIDTH` | `0x1` |
| `MBX_FACE_REG_CTR_REQ` | `0x40` |
| `MBX_CTR_REQ_TYPE_LSB` | `0x0` |
| `MBX_CTR_REQ_TYPE_WIDTH` | `0x10` |
| `MBX_CTR_REQ_INDEX_LSB` | `0x10` |
| `MBX_CTR_REQ_INDEX_WIDTH` | `0x10` |
| `MBX_FACE_REG_CTR_WORD` | `0x44` |
| `MBX_CTR_WORD_WORD_LSB` | `0x0` |
| `MBX_CTR_WORD_WORD_WIDTH` | `0x6` |
| `MBX_FACE_REG_CTR_CMD` | `0x48` |
| `MBX_CTR_CMD_GO_LSB` | `0x0` |
| `MBX_CTR_CMD_GO_WIDTH` | `0x1` |
| `MBX_FACE_REG_CTR_STATUS` | `0x4c` |
| `MBX_CTR_STATUS_BUSY_LSB` | `0x0` |
| `MBX_CTR_STATUS_BUSY_WIDTH` | `0x1` |
| `MBX_CTR_STATUS_DONE_LSB` | `0x1` |
| `MBX_CTR_STATUS_DONE_WIDTH` | `0x1` |
| `MBX_CTR_STATUS_TIMEOUT_LSB` | `0x2` |
| `MBX_CTR_STATUS_TIMEOUT_WIDTH` | `0x1` |
| `MBX_CTR_STATUS_TAG_LSB` | `0x8` |
| `MBX_CTR_STATUS_TAG_WIDTH` | `0x4` |
| `MBX_FACE_REG_CTR_DATA` | `0x50` |
| `MBX_CTR_DATA_DATA_LSB` | `0x0` |
| `MBX_CTR_DATA_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_AMAP_REQ` | `0x60` |
| `MBX_AMAP_REQ_TYPE_LSB` | `0x0` |
| `MBX_AMAP_REQ_TYPE_WIDTH` | `0x10` |
| `MBX_AMAP_REQ_INDEX_LSB` | `0x10` |
| `MBX_AMAP_REQ_INDEX_WIDTH` | `0x10` |
| `MBX_FACE_REG_AMAP_PAGE` | `0x64` |
| `MBX_AMAP_PAGE_MAP_INDEX_LSB` | `0x0` |
| `MBX_AMAP_PAGE_MAP_INDEX_WIDTH` | `0x10` |
| `MBX_AMAP_PAGE_SEL_LSB` | `0x10` |
| `MBX_AMAP_PAGE_SEL_WIDTH` | `0x2` |
| `MBX_AMAP_PAGE_REC_LSB` | `0x18` |
| `MBX_AMAP_PAGE_REC_WIDTH` | `0x8` |
| `MBX_FACE_REG_AMAP_CMD` | `0x68` |
| `MBX_AMAP_CMD_GO_LSB` | `0x0` |
| `MBX_AMAP_CMD_GO_WIDTH` | `0x1` |
| `MBX_FACE_REG_AMAP_STATUS` | `0x6c` |
| `MBX_AMAP_STATUS_BUSY_LSB` | `0x0` |
| `MBX_AMAP_STATUS_BUSY_WIDTH` | `0x1` |
| `MBX_AMAP_STATUS_DONE_LSB` | `0x1` |
| `MBX_AMAP_STATUS_DONE_WIDTH` | `0x1` |
| `MBX_AMAP_STATUS_TIMEOUT_LSB` | `0x2` |
| `MBX_AMAP_STATUS_TIMEOUT_WIDTH` | `0x1` |
| `MBX_AMAP_STATUS_TAG_LSB` | `0x8` |
| `MBX_AMAP_STATUS_TAG_WIDTH` | `0x4` |
| `MBX_FACE_REG_AMAP_DATA_LO` | `0x70` |
| `MBX_AMAP_DATA_LO_DATA_LSB` | `0x0` |
| `MBX_AMAP_DATA_LO_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_AMAP_DATA_HI` | `0x74` |
| `MBX_AMAP_DATA_HI_DATA_LSB` | `0x0` |
| `MBX_AMAP_DATA_HI_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_REQ` | `0x80` |
| `MBX_EDIT_REQ_TYPE_LSB` | `0x0` |
| `MBX_EDIT_REQ_TYPE_WIDTH` | `0x10` |
| `MBX_EDIT_REQ_INDEX_LSB` | `0x10` |
| `MBX_EDIT_REQ_INDEX_WIDTH` | `0x10` |
| `MBX_FACE_REG_EDIT_BEAT` | `0x84` |
| `MBX_EDIT_BEAT_PHASE_LSB` | `0x0` |
| `MBX_EDIT_BEAT_PHASE_WIDTH` | `0x3` |
| `MBX_EDIT_BEAT_REMOVE_LSB` | `0x4` |
| `MBX_EDIT_BEAT_REMOVE_WIDTH` | `0x1` |
| `MBX_EDIT_BEAT_REC_LSB` | `0x8` |
| `MBX_EDIT_BEAT_REC_WIDTH` | `0x8` |
| `MBX_EDIT_BEAT_COUNT_LSB` | `0x10` |
| `MBX_EDIT_BEAT_COUNT_WIDTH` | `0x10` |
| `MBX_FACE_REG_EDIT_RECORD_LO` | `0x88` |
| `MBX_EDIT_RECORD_LO_RECORD_LSB` | `0x0` |
| `MBX_EDIT_RECORD_LO_RECORD_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_RECORD_HI` | `0x8c` |
| `MBX_EDIT_RECORD_HI_RECORD_LSB` | `0x0` |
| `MBX_EDIT_RECORD_HI_RECORD_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_VALUE_LO` | `0x90` |
| `MBX_EDIT_VALUE_LO_VALUE_LSB` | `0x0` |
| `MBX_EDIT_VALUE_LO_VALUE_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_VALUE_HI` | `0x94` |
| `MBX_EDIT_VALUE_HI_VALUE_LSB` | `0x0` |
| `MBX_EDIT_VALUE_HI_VALUE_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_CMD` | `0x98` |
| `MBX_EDIT_CMD_GO_LSB` | `0x0` |
| `MBX_EDIT_CMD_GO_WIDTH` | `0x1` |
| `MBX_FACE_REG_EDIT_STATUS` | `0x9c` |
| `MBX_EDIT_STATUS_BUSY_LSB` | `0x0` |
| `MBX_EDIT_STATUS_BUSY_WIDTH` | `0x1` |
| `MBX_EDIT_STATUS_DONE_LSB` | `0x1` |
| `MBX_EDIT_STATUS_DONE_WIDTH` | `0x1` |
| `MBX_EDIT_STATUS_TIMEOUT_LSB` | `0x2` |
| `MBX_EDIT_STATUS_TIMEOUT_WIDTH` | `0x1` |
| `MBX_EDIT_STATUS_TAG_LSB` | `0x8` |
| `MBX_EDIT_STATUS_TAG_WIDTH` | `0x4` |
| `MBX_FACE_REG_EDIT_DATA_LO` | `0xa0` |
| `MBX_EDIT_DATA_LO_DATA_LSB` | `0x0` |
| `MBX_EDIT_DATA_LO_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_EDIT_DATA_HI` | `0xa4` |
| `MBX_EDIT_DATA_HI_DATA_LSB` | `0x0` |
| `MBX_EDIT_DATA_HI_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_GSI_REQ` | `0xc0` |
| `MBX_GSI_REQ_TYPE_LSB` | `0x0` |
| `MBX_GSI_REQ_TYPE_WIDTH` | `0x10` |
| `MBX_GSI_REQ_INDEX_LSB` | `0x10` |
| `MBX_GSI_REQ_INDEX_WIDTH` | `0x10` |
| `MBX_FACE_REG_GSI_SEL` | `0xc4` |
| `MBX_GSI_SEL_KIND_LSB` | `0x0` |
| `MBX_GSI_SEL_KIND_WIDTH` | `0x2` |
| `MBX_GSI_SEL_SEL_LSB` | `0x4` |
| `MBX_GSI_SEL_SEL_WIDTH` | `0x4` |
| `MBX_GSI_SEL_ORD_LSB` | `0x8` |
| `MBX_GSI_SEL_ORD_WIDTH` | `0x8` |
| `MBX_FACE_REG_GSI_PROP_LO` | `0xc8` |
| `MBX_GSI_PROP_LO_FMT_LSB` | `0x0` |
| `MBX_GSI_PROP_LO_FMT_WIDTH` | `0x20` |
| `MBX_FACE_REG_GSI_PROP_HI` | `0xcc` |
| `MBX_GSI_PROP_HI_FMT_LSB` | `0x0` |
| `MBX_GSI_PROP_HI_FMT_WIDTH` | `0x20` |
| `MBX_FACE_REG_GSI_CMD` | `0xd0` |
| `MBX_GSI_CMD_GO_LSB` | `0x0` |
| `MBX_GSI_CMD_GO_WIDTH` | `0x1` |
| `MBX_FACE_REG_GSI_STATUS` | `0xd4` |
| `MBX_GSI_STATUS_BUSY_LSB` | `0x0` |
| `MBX_GSI_STATUS_BUSY_WIDTH` | `0x1` |
| `MBX_GSI_STATUS_DONE_LSB` | `0x1` |
| `MBX_GSI_STATUS_DONE_WIDTH` | `0x1` |
| `MBX_GSI_STATUS_TIMEOUT_LSB` | `0x2` |
| `MBX_GSI_STATUS_TIMEOUT_WIDTH` | `0x1` |
| `MBX_GSI_STATUS_TAG_LSB` | `0x8` |
| `MBX_GSI_STATUS_TAG_WIDTH` | `0x4` |
| `MBX_FACE_REG_GSI_DATA_LO` | `0xd8` |
| `MBX_GSI_DATA_LO_DATA_LSB` | `0x0` |
| `MBX_GSI_DATA_LO_DATA_WIDTH` | `0x20` |
| `MBX_FACE_REG_GSI_DATA_HI` | `0xdc` |
| `MBX_GSI_DATA_HI_DATA_LSB` | `0x0` |
| `MBX_GSI_DATA_HI_DATA_WIDTH` | `0x20` |
| `MBX_FACE_SOURCE_BASE` | `0x100` |
| `MBX_FACE_SOURCE_STRIDE` | `0x10` |
| `MBX_FACE_SRC_REG_F_PT_OFFSET` | `0x0` |
| `MBX_F_PT_OFFSET_NS_LSB` | `0x0` |
| `MBX_F_PT_OFFSET_NS_WIDTH` | `0x20` |
| `MBX_FACE_SRC_REG_F_FMT_OUT_LO` | `0x4` |
| `MBX_F_FMT_OUT_LO_FMT_LSB` | `0x0` |
| `MBX_F_FMT_OUT_LO_FMT_WIDTH` | `0x20` |
| `MBX_FACE_SRC_REG_F_FMT_OUT_HI` | `0x8` |
| `MBX_F_FMT_OUT_HI_FMT_LSB` | `0x0` |
| `MBX_F_FMT_OUT_HI_FMT_WIDTH` | `0x20` |
| `MBX_FACE_SRC_REG_F_SRC_VALID` | `0xc` |
| `MBX_F_SRC_VALID_PT_OFFSET_LSB` | `0x0` |
| `MBX_F_SRC_VALID_PT_OFFSET_WIDTH` | `0x1` |
| `MBX_F_SRC_VALID_FMT_OUT_LSB` | `0x1` |
| `MBX_F_SRC_VALID_FMT_OUT_WIDTH` | `0x1` |
| `MBX_FACE_SINK_BASE` | `0x200` |
| `MBX_FACE_SINK_STRIDE` | `0x10` |
| `MBX_FACE_SNK_REG_F_FMT_IN_LO` | `0x0` |
| `MBX_F_FMT_IN_LO_FMT_LSB` | `0x0` |
| `MBX_F_FMT_IN_LO_FMT_WIDTH` | `0x20` |
| `MBX_FACE_SNK_REG_F_FMT_IN_HI` | `0x4` |
| `MBX_F_FMT_IN_HI_FMT_LSB` | `0x0` |
| `MBX_F_FMT_IN_HI_FMT_WIDTH` | `0x20` |
| `MBX_FACE_SNK_REG_F_SNK_VALID` | `0x8` |
| `MBX_F_SNK_VALID_FMT_IN_LSB` | `0x0` |
| `MBX_F_SNK_VALID_FMT_IN_WIDTH` | `0x1` |
| `MBX_WIN_CTR_WAIT_CYCLES` | `0x40` |
| `MBX_WIN_CTR_DATA_WORDS` | `0x1` |
| `MBX_WIN_AMAP_WAIT_CYCLES` | `0x40` |
| `MBX_WIN_AMAP_DATA_WORDS` | `0x2` |
| `MBX_WIN_EDIT_WAIT_CYCLES` | `0x40` |
| `MBX_WIN_EDIT_DATA_WORDS` | `0x2` |
| `MBX_WIN_GSI_WAIT_CYCLES` | `0x40` |
| `MBX_WIN_GSI_DATA_WORDS` | `0x2` |
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
| `MBX_CTRCHG_HOLDOFF_MS` | `0x3e8` |
| `MBX_CTRCHG_STREAM_INPUT_TYPE` | `0x5` |
| `MBX_CTRCHG_STREAM_INPUT_COUNT` | `0x10` |
| `MBX_CTRCHG_STREAM_INPUT_FIRST` | `0x0` |
| `MBX_CTRCHG_STREAM_OUTPUT_TYPE` | `0x6` |
| `MBX_CTRCHG_STREAM_OUTPUT_COUNT` | `0x10` |
| `MBX_CTRCHG_STREAM_OUTPUT_FIRST` | `0x10` |
| `MBX_CTRCHG_AVB_INTERFACE_TYPE` | `0x9` |
| `MBX_CTRCHG_AVB_INTERFACE_COUNT` | `0x1` |
| `MBX_CTRCHG_AVB_INTERFACE_FIRST` | `0x20` |
| `MBX_CTRCHG_CLOCK_DOMAIN_TYPE` | `0x24` |
| `MBX_CTRCHG_CLOCK_DOMAIN_COUNT` | `0x1` |
| `MBX_CTRCHG_CLOCK_DOMAIN_FIRST` | `0x21` |
| `MBX_CTRCHG_N_SRC` | `0x4` |
| `MBX_CTRCHG_ALL_BIT` | `0x22` |
| `MBX_CTRCHG_N_PEND` | `0x23` |
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
| `MBX_EV_TYPE_COUNTERS_CHANGED` | `0x5` |
| `MBX_EV_COUNTERS_CHANGED_W1_TYPE_LSB` | `0x0` |
| `MBX_EV_COUNTERS_CHANGED_W1_TYPE_WIDTH` | `0x10` |
| `MBX_EV_COUNTERS_CHANGED_W1_INDEX_LSB` | `0x10` |
| `MBX_EV_COUNTERS_CHANGED_W1_INDEX_WIDTH` | `0x10` |
| `MBX_EV_COUNTERS_CHANGED_W2_ALL_LSB` | `0x0` |
| `MBX_EV_COUNTERS_CHANGED_W2_ALL_WIDTH` | `0x1` |
| `MBX_EV_COUNTERS_CHANGED_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_COUNTERS_CHANGED_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_EV_TYPE_AVB_INFO_CHANGED` | `0x6` |
| `MBX_EV_AVB_INFO_CHANGED_W1_COUNT_LSB` | `0x0` |
| `MBX_EV_AVB_INFO_CHANGED_W1_COUNT_WIDTH` | `0x10` |
| `MBX_EV_AVB_INFO_CHANGED_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_AVB_INFO_CHANGED_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_EV_TYPE_AS_PATH_CHANGED` | `0x7` |
| `MBX_EV_AS_PATH_CHANGED_W1_COUNT_LSB` | `0x0` |
| `MBX_EV_AS_PATH_CHANGED_W1_COUNT_WIDTH` | `0x10` |
| `MBX_EV_AS_PATH_CHANGED_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_AS_PATH_CHANGED_W3_NOW_MS_WIDTH` | `0x20` |
| `MBX_EV_TYPE_AMAP_LIVE_WRITE` | `0x8` |
| `MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_LSB` | `0x0` |
| `MBX_EV_AMAP_LIVE_WRITE_W1_COUNT_WIDTH` | `0x10` |
| `MBX_EV_AMAP_LIVE_WRITE_W3_NOW_MS_LSB` | `0x0` |
| `MBX_EV_AMAP_LIVE_WRITE_W3_NOW_MS_WIDTH` | `0x20` |
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

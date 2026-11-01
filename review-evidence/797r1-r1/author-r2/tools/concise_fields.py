#!/usr/bin/env python3
"""One-off: bit meanings of the carried notes, as field rows of the descriptions file."""
import json, sys
p = sys.argv[1] + "/scripts/register_descriptions.json"
d = json.load(open(p))
R = d["registers"]
SZ = "**Structural zero.** "
SCRATCH = "Inert scratch: stores and reads back, reaches no logic. "

def fields(key, **kw):
    R[key].setdefault("fields", {}).update(kw)

def split(key, name, rows):
    R[key].setdefault("split", {})[name] = rows

def note(key, *texts):
    R[key].setdefault("notes", [])
    R[key]["notes"] = list(texts) + R[key]["notes"]

note("MAC_STATUS", "These bits mirror the LiteX `milan_mac_link_status` CSR.",
     "Its reset: link up, full duplex, gigabit on GMII. MII resets to 100 Mb/s.",
     "So this word reads `0x0000000D` on the AX7101 until firmware writes.",
     "Firmware writes it only while the saved-state writer runs.",
     "The word does not follow the link on its own.",
     "For the link, read `LINKG_STAT`, the link counters or BMSR.")
split("VERSION", "VERSION", [["31:16", "MAJOR", "Major: an entire redesign of blocks."],
                            ["15:0", "MINOR", "Minor: compliance fixes, flat across majors."]])
fields("IRQ_STATUS", EVT_RMON_ROLLOVER="RMON rollover latch; `i_evt_rmon_rollover` sets it.",
       EVT_LINK_CHANGE="Link change latch; `i_evt_link_change` sets it.")
note("IRQ_STATUS", "`[0]` was `tx_ts_ready`: a structural zero since `0x0056`.")
fields("IRQ_RAW", EVT_RMON_ROLLOVER="Same latch as `IRQ_STATUS[2]`.", EVT_LINK_CHANGE="Same latch as `IRQ_STATUS[1]`.")
fields("MAC_CTRL", MAC_TX_EN="Transmit enable.", MAC_RX_EN="Receive enable.", MAC_PROMISC="Promiscuous receive.",
       MAC_ALLMULTI="Accept all multicast.", MAC_IS_1G="Link rate is 1 Gb/s. Consulted only while `[5]` is set.",
       MAC_IS_1G_SELECT="speed_manual: 0 derives the rate from `MAC_STATUS` speed, 1 uses `[4]` (REQ-MAC-03).")
fields("MAC_ALO", MAC_ADDR="Station MAC, LSB-first: wire byte 0 in `[7:0]`, byte 3 in `[31:24]`.")
fields("MAC_AHI", MAC_ADDR="Station MAC: wire byte 4 in `[7:0]`, byte 5 in `[15:8]`.")
fields("STATS_CAP", STATS_CAP="Per-lane mask in `[8:0]`: lane n is the `STATn` word at `0x210 + 4n`. 1 is a real counter, "
       "0 structurally silent. Live, not snapshot-latched. `[31:9]` read 0.")
fields("STATS", STAT_SNAP="The snapshot of lane n, latched by `STATS_CTRL[0]`. Read `STATS_CAP` before believing a zero.")
split("CLS_CTRL", "CLS_CTRL", [
    ["31:3", "RESERVED", ""],
    ["2", "CTRL_CLASS", SCRATCH + "Was ctrl_class (REQ-CLS-10)."],
    ["1", "DMAC_CHECK", SCRATCH + "Was dmac_check (REQ-CLS-07)."],
    ["0", "USE_PCP", SCRATCH + "Was use_pcp: 1 classifies by the PCP table."]])
fields("CLS_DPCP", CLS_DPCP=SCRATCH + "Was the default PCP of untagged frames.")
fields("PTP_INCR", PTP_INCR="Nominal increment per tick, Q8.24 ns: `[31:24]` integer, `[23:0]` fraction. "
       "The reset is the PHC clock period from `MILAN_CLK_FREQ_HZ_P`.")
fields("PTP_TWLO", PTP_TOD_WR="Time to load, low half: `PTP_CMD[0]` applies it.")
fields("PTP_TWHI", PTP_TOD_WR="Time to load, high half.")
fields("PTP_OFLO", PTP_OFFSET="adjtime signed delta, low half.")
fields("PTP_OFHI", PTP_OFFSET="adjtime signed delta, high half.")
fields("PTP_TRLO", PTP_TOD_RD="Time latched by `PTP_CMD[2]`, low half.")
fields("PTP_TRHI", PTP_TOD_RD="Time latched by `PTP_CMD[2]`, high half.")
fields("PPS_CTRL", PPS_P="Built: 1 only when the gateware elaborated the comparator. Read it before believing `[0]`.",
       PPS_ARM="Arm: loads `PTP_PPS_TGT_{HI,LO}` into the live target.")
note("PPS_CTRL", "At `PPS_P` = 0, `[0]` reads 0 and reaches nothing.", "At `PPS_P` = 1, `[0]` is the R/W runtime enable.",
     "Setting `[1]` and `[0]` in one word emits no early pulse.")
fields("PPS_TGLO", PPS_TARGET_NS="Target to arm, low half, in ns. Write a TAI second boundary: the hardware does no modulo.")
fields("PPS_TGHI", PPS_TARGET_NS="Target to arm, high half.")
fields("PPS_RDLO", PPS_TARGET_RD_NS="Live target, low half, from the PHC domain. Advances by 1e9 on each pulse. "
       "Reads 0 when `PPS_CTRL[16]` is 0.")
fields("PPS_RDHI", PPS_TARGET_RD_NS="Live target, high half.")
fields("ADP_EIDLO", ADP_ENTITY_ID="entity_id, low half.")
fields("ADP_EIDHI", ADP_ENTITY_ID="entity_id, high half.")
fields("ADP_MIDLO", ADP_ENTITY_MODEL_ID="entity_model_id, low half.")
fields("ADP_MIDHI", ADP_ENTITY_MODEL_ID="entity_model_id, high half.")
split("ADP_TALK", "ADP_TALK", [["31:16", "TALKER_CAPS", "talker_capabilities, generated from the end-station config. "
      "Writes are ignored."], ["15:0", "TALKER_SOURCES", "talker_stream_sources: the STREAM_OUTPUT descriptor count."]])
split("ADP_LIST", "ADP_LIST", [["31:16", "LISTENER_CAPS", "listener_capabilities, generated from the end-station config. "
      "Writes are ignored."], ["15:0", "LISTENER_SINKS", "listener_stream_sinks: the STREAM_INPUT descriptor count."]])
snap = ("The first half read snapshots the live 64-bit identity; the other half reads that snapshot, in either order. ")
fields("ADP_GMLO", GPTP_GM_RD_SNAP="gptp_grandmaster_id, low half. " + snap + "Before a peer is elected it reads thisClock. "
       "With the gPTP plane off it reads 0. Writes are inert.")
fields("ADP_GMHI", GPTP_GM_RD_SNAP="gptp_grandmaster_id, high half. " + snap + "With the gPTP plane off it reads 0.")
fields("ADP_DOMAIN", ADP_DOMAIN="gptp_domain_number, ADPDU byte 48: a structural 0 in both builds. Writes are inert.")
fields("ADP_IDX1", ADP_INTERFACE_INDEX="interface_index.")
fields("ADP_ASLO", ADP_ASSOCIATION_ID="association_id, low half: inert scratch.")
fields("ADP_ASHI", ADP_ASSOCIATION_ID="association_id, high half: inert scratch.")
fields("ADP_CMD", ADP_ADVERTISE=SCRATCH + "Was advertise-now.", ADP_DEPART=SCRATCH + "Was depart.")
fields("ADP_STATUS", ADP_AVAILABLE_INDEX="available_index, live from the protocol processor; equal to the value on the wire.")
fields("AECP_STAT0", AECP_LOCKED="The processor's live `LOCK_ENTITY` level.",
       AECP_CMD_COUNT=SZ + "The processor command count is not exported.")
fields("AECP_STAT1", AECP_RESP_COUNT=SZ + "Was AECP responses sent.", AECP_CURRENT_CONFIG=SZ + "Was the current configuration index.")
fields("ACMP_STAT", ACMP_RESP_COUNT=SZ + "Was responses sent. Read `ACMPL_STATE[3]` and `ACMP_TALKER[1]` instead.",
       ACMP_CMD_COUNT=SZ + "Was commands accepted.")
fields("AAF_CTRL", AAF_ENABLE="Enable. Firmware boots the generated `MILAN_AAF_CTRL_BOOT` word.",
       AAF_BYPASS="Diagnostic bypass. Boot clears it.", AAF_VID="Startup VID 2. Domain adoption selects the tag on the wire.")
fields("AAF_DMLO", AAF_DEST_MAC="Destination MAC `[31:0]`; reset is `91:E0:F0:00:FE:01`. A fallback: with `MAAP_CTRL[0]` and "
       "`MAAP_STAT1[2]` set, the datapath uses the MAAP-claimed address.")
fields("AAF_DMHI", AAF_DEST_MAC="Destination MAC `[47:32]`.")
fields("ADP_DIAG", ADP_DEPART_SRC=SZ + "Was the last depart cause.", ADP_REARM_CNT=SZ + "Was dormancy re-arms.",
       ADP_DEPART_CNT=SZ + "Was depart events. Read `ADP_STATUS` across two reads instead.")
fields("ACMP_TALKER", ACMP_PROBE_ARMED=SZ + "The class-D face has no probe-window level.",
       ACMP_TALKER_ACTIVE="Live: the processor's `acmp_declaring_o`, set only after MAAP ALLOC_DA success.",
       ACMP_LOBS="Mirror of the `ACMP_LOBS[0]` manual override.", AAF_GATE="The composed gate the datapath admits frames on.")
fields("ADP_DIAG2", ADP_STATE=SZ + "Was the advertiser state.", ADP_LAST_MSG=SZ + "Was the last message_type.",
       ADP_DISC_SEEN_CNT=SZ + "Was ENTITY_DISCOVERs seen: it counts `i_adp_disc_seen_p`, whose source is deleted.",
       ADP_DISC_RX_CNT=SZ + "Was ENTITY_DISCOVERs accepted.", ADP_SENT_CNT=SZ + "Was ADPDUs egressed.")
fields("LWSRP_CTRL", LWSRP_ENABLE="Live admission enable. Firmware sets it for normal boot. It does not enable the SRP engine.",
       LWSRP_TALKER_EN="Live talker admission arm. Firmware sets it for normal boot.",
       LWSRP_DECL_BYPASS=SCRATCH + "Was declare-always.")
note("LWSRP_CTRL", "`[4:2]` is legacy queue-selection scratch, reset 4.")
fields("LWSRP_VID", LWSRP_VID="Diagnostic default VID; startup uses `srp.vid` = 2. Writes do not program the processor. "
       "The operational pair is at `LWSRP_DOM`.")
fields("LWSRP_DMLO", LWSRP_DEST_MAC=SCRATCH + "The processor takes its address from MAAP.")
fields("LWSRP_DMHI", LWSRP_DEST_MAC=SCRATCH + "The processor takes its address from MAAP.")
fields("LWSRP_TSPEC", LWSRP_INTERVAL=SCRATCH + "Was MaxIntervalFrames; the processor derives it from the SR class.",
       LWSRP_MAX_FRAME=SCRATCH + "Was MaxFrameSize; the fabric derives it from each framer (Milan v1.2 4.3.3.2 Table 4.4).")
split("LWSRP_STATUS", "LWSRP_STATUS", [
    ["31:24", "INGRESS_DROPS", SZ + "That ingress path is deleted; see `PP_DIAG[15:8]`."],
    ["23:16", "FAIL_CODE", "MSRP failure code."],
    ["15:12", "RESERVED", ""],
    ["11", "ROW_SHORTFALL", SZ + "No attribute-row table exists in this fabric."],
    ["10", "TALKER_FAILED", "TalkerFailed seen."],
    ["9", "ADMIT_VERDICT", "The OR of the processor's real admission grants. Status only."],
    ["8", "GATE_OPEN", "Source 0's ACTIVE and real grant (#551): the Milan v1.2 5.3.7.3 licence."],
    ["7", "OVER_LIMIT", "Over the 75 % gate: ceiling refusal."],
    ["6", "ACTIVE", "Raw reservation ACTIVE, ORed over sources, CRF output included."],
    ["5", "DOMAIN_OK", "Domain ok."],
    ["4", "TALKER_DECLARED", "Talker declared."],
    ["3", "LISTENER_READY", "`[1:0]` is ready or ready-failed (Milan v1.2 5.3.7.3)."],
    ["2", "LISTENER_REGISTERED", "`[1:0]` is not 0, asking-failed included."],
    ["1:0", "LISTENER_STATE", "The Listener registered on talker source 0, as 802.1Q 35.2.2.7.2 (Table 35-3) FourPackedEvents: "
     "0 none, 1 asking-failed, 2 ready, 3 ready-failed."]])
fields("LWSRP_CNT", LWSRP_CNT=SZ + "Was MRPDU counts. Reservations still form: read `LWSRP_STATUS` and `LWSRP_DOM`.")
split("ACMPL_STATE", "ACMPL_STATE", [
    ["31", "CRF_BOUND", "CRF sink bound."],
    ["30:28", "RESERVED", ""],
    ["27:16", "VLAN", "Stream VLAN from the bind record."],
    ["15", "TALKER_VISIBLE", SZ + "Was bound talker ADP-visible."],
    ["14:13", "PROBING", SZ + "Was probing status."],
    ["12:8", "ACMP_STATUS", SZ + "Was the last ACMP status."],
    ["7", "TALKER_FAILED", "Sink 0 carries an MSRP TalkerFailed code; same source as `ACMPL_TUID[23:16]`."],
    ["6", "TALKER_ADVERTISE", "Sink 0's registered Talker attribute is ADVERTISE."],
    ["5", "LISTENER_DECLARED", SZ + "Was Listener attribute declared."],
    ["4", "ACTIVE", "Stream active; follows bound."],
    ["3", "BOUND", "Bound: the truth for this sink."],
    ["2:0", "SM_STATE", SZ + "The probe ladder no longer exists here, so a reader waiting for SETTLED waits forever."]])
fields("ACMPL_TKLO", ACMPL_TALKER_LO=SZ + "Was the bound talker entity ID, low half.")
fields("ACMPL_TKHI", ACMPL_TALKER_HI=SZ + "Was the bound talker entity ID, high half.")
fields("ACMPL_CNT", ACMPL_CNT=SZ + "Was PROBE_TX commands sent and listener commands accepted.")
split("ACMPL_TUID", "ACMPL_TUID", [
    ["31:24", "RESERVED", ""],
    ["23:16", "TALKER_FAILED", "MSRP TalkerFailed code for the bound stream, live."],
    ["15:0", "TUID", SZ + "Was the bound talker unique ID."]])
split("AVTPRX_STAT", "AVTPRX_STAT", [
    ["31:24", "STREAM_INTERRUPTED", "Saturating view; the full count is at `STRMW_CNTn`."],
    ["23:16", "MEDIA_UNLOCKED", "Saturating view; the full count is at `STRMW_CNTn`."],
    ["15:8", "MEDIA_LOCKED", "Saturating view; the full count is at `STRMW_CNTn`."],
    ["7:1", "RESERVED", ""],
    ["0", "LOCKED_LEVEL", "Media-locked level."]])
note("AVTPRX_STAT", "`AVTPRX_STAT` bytes saturate: `0xFF` means at least 255.",
     "Counter clauses: IEEE 1722.1-2021 Table 7-156. Milan v1.2 Table 5.6.")
note("AVTPRX_ERR", "`AVTPRX_ERR` fields saturate: all ones means at least that many.")
split("AVTPRX_ERR", "AVTPRX_ERR", [
    ["31:16", "SEQ_NUM_MISMATCH", "Saturating: all ones means at least this many. The full count is at `0x83C`."],
    ["15:8", "UNSUPPORTED_FORMAT", "Saturating view."],
    ["7:0", "TIMESTAMP_UNCERTAIN", "Saturating view."]])
split("PCMRX_CNT", "PCMRX_CNT", [["31:16", "DROPPED", "Whole frames dropped: FIFO overflow."],
                                 ["15:0", "PDUS", "PDU payloads emitted to the fabric."]])
fields("MAAP_CTRL", MAAP_ENABLE="Enable.", MAAP_SEED_VALID="Seed valid.", MAAP_COUNT="Block count.", MAAP_SEED_OFFSET="Seed offset.")
note("MAAP_CTRL", "Firmware writes the generated `MILAN_MAAP_CTRL_BOOT` word.")
split("MAAP_STAT0", "MAAP_STAT0", [
    ["31:24", "CONFLICTS", "Conflicts: re-address events."], ["23:16", "DEFENDS", "DEFENDs sent."], ["15:0", "OFFSET", "Claimed offset."]])
split("MAAP_STAT1", "MAAP_STAT1", [
    ["31:3", "RESERVED", ""],
    ["2", "ADDR_VALID", "ANNOUNCE state: the address is valid."],
    ["1:0", "STATE", "0 idle, 1 probe, 2 announce."]])
fields("I2SPB_STAT", UNDERRUN="Underruns: silence frames. Saturates at `0xFFFF`. Any set bit written here restarts this "
       "whole half, not only the set bits. A zero write is inert.",
       OVERRUN="Overruns: pairs dropped. Saturates at `0xFFFF`. Any set bit written here restarts this whole half.")
split("I2SPB_TRIM", "I2SPB_TRIM", [["31:16", "NCO_TRIM", "Signed NCO trim, LSB about 15.3 ppm."], ["15:0", "FIFO_FILL", "FIFO fill, in pairs."]])
fields("TCAM_CTRL", TCAM_DEFAULT_PASS="1 accepts frames that miss the table.",
       TCAM_ADDR_FILT_EN="1 sends a miss to the 802.3 station address filter instead of `[0]` (REQ-MAC-02).")
fields("TCAM_KLO", TCAM_WR_KEY="Match key `[31:0]` (destination MAC).")
fields("TCAM_KHI", TCAM_WR_KEY="Match key `[47:32]`.")
fields("TCAM_MLO", TCAM_WR_MASK="Per-bit mask `[31:0]`.")
fields("TCAM_MHI", TCAM_WR_MASK="Per-bit mask `[47:32]`.")
fields("TCAM_ACT", TCAM_WR_ACTION="Entry action.")
fields("RST_EPOCH", RST_EPOCH="Datapath reset-release count. It has no reset clause, so the count survives reset. "
       "A live tick proves a real reset happened.")
for k in ("ENT_NAME_LO", "ENT_NAME_HI"):
    fields(k, ENTITY_NAME8_31_24="One character of the board-name overlay.", ENTITY_NAME8_23_16="One character.",
           ENTITY_NAME8_15_8="One character.",
           ENTITY_NAME8_7_0="First character of this word." if k == "ENT_NAME_LO" else "One character.")
note("ENT_NAME_LO", "All zero keeps the ROM name.")
fields("AS2_LO", GPTP_PARENT_RD_SNAP="Parent clockIdentity, low half. " + snap + "With the gPTP plane off it reads 0.")
fields("AS2_HI", GPTP_PARENT_RD_SNAP="Parent clockIdentity, high half. " + snap + "With the gPTP plane off it reads 0.")
split("CRF_STATUS", "CRF_STATUS", [["31:16", "PDUS", "PDUs accepted."],
      ["15:8", "FORMAT_ERRORS", "Format errors: subtype (#765) and the Milan v1.2 7.3.2 check."], ["7:0", "SEQ_ERRORS", "Sequence errors."]])
fields("CRF_SIDLO", CRF_SID="Followed stream_id, low half: the manual lever. A bind wins.")
fields("CRF_SIDHI", CRF_SID="Followed stream_id, high half.")
fields("CRFT_CTRL", CRFT_EN="Talker enable. Firmware boots `MILAN_CRF_TX_CTRL_BOOT` from the config.",
       CRFT_CLASS_A="Class-A declare and tag (Milan v1.2 7.3.3). Clear gives the untagged control-lane shape.")
split("CRFT_CTRL", "CRFT_STAT", [
    ["31:23", "RESERVED", ""],
    ["22:20", "PCP", "PCP on the frames."],
    ["19:8", "VID", "VID on the frames."],
    ["7", "LICENSED", "Emission licensed now: `[0]` and `[6]` while SRP policing is on."],
    ["6", "RESERVATION_ACTIVE", "This output's ACTIVE and real admission grant (#551)."],
    ["5", "TAGGED", "Frames leaving tagged."],
    ["4", "ROW_VALID", SZ + "There is no fabric row to provision."],
    ["3:2", "RESERVED", ""]])
fields("CRFT_SIDLO", CRFT_SID="stream_id, low half. Zero selects AUTO: `{station MAC, N_STREAMS}`. A non-zero pair wins.")
fields("CRFT_SIDHI", CRFT_SID="stream_id, high half.")
fields("CRFT_DMLO", CRFT_DEST_MAC="Destination MAC `[31:0]`. Zero selects AUTO: MAAP block slot `base + N_STREAMS`. A non-zero pair wins.")
fields("CRFT_DMHI", CRFT_DEST_MAC="Destination MAC `[47:32]`.")
fields("BDBG1", BDBG1=SZ + "Was AECP scan forensics.")
fields("BDBG2", BDBG2=SZ + "Was AECP scan forensics.")
split("LINKG_STAT", "LINKG_STAT", [
    ["31:16", "BOUNCE_CNT", "Link bounce count, saturating."], ["15:10", "RESERVED", ""],
    ["9", "FREEZE", "Freeze."], ["8", "DIS", "Disable."],
    ["7", "ACT_RECENT", "RX activity within the last 2^27 guard clock cycles."],
    ["6", "GUARD_RST", "Reinit held."], ["5:4", "STATE", "0 RUN, 1 HOLD, 2 SETTLE."], ["3", "RESERVED", ""],
    ["2", "ETH_RST", "Sequenced Ethernet-domain reset."], ["1", "TX_ALIVE", "TX alive."], ["0", "RX_ALIVE", "RX alive."]])
split("CLKV_STAT", "CLKV_STAT", [
    ["31:17", "RESERVED", ""],
    ["16", "AS_CAPABLE", "asCapable: the bit `GET_AVB_INFO` serves (IEEE 1722.1-2021 7.4.40.2 flags bit 0)."],
    ["15:4", "RESERVED", ""],
    ["3", "HOLDOVER", "Inside a discontinuity holdover."], ["2", "RESERVED", ""],
    ["1", "SYNC_OK", "Fabric sync_ok."], ["0", "TU", "`tu` as stamped on every outgoing stream frame."]])
split("TXARB_DIAG", "TXARB_DIAG", [
    ["31:24", "TAG", "Constant `0xA7`. Zero means the gateware predates this word."],
    ["23:16", "STALL_STICKY", "A presented beat was refused for the mux's watchdog window. Clears only on reset."],
    ["15:8", "ABORT_STICKY", "A granted source abandoned its frame; the arbiter closed it. Clears only on reset."],
    ["7:0", "LOCKED_NOW", "Lane holds the arbiter lock now."]])
note("TXARB_DIAG", "Lanes, LSB first: 0 `ctl_tx`, 1 `aaf_final`, 2 `crf_dp`, 3 `adp_tx`, 4 `gptp_ctl_mux`.",
     "Lane 1 is a structural zero since `0x0056`.", "Lane 4 is live with fabric gPTP only.")
split("LWSRP_DOM", "LWSRP_DOM", [
    ["31:25", "RESERVED", ""], ["24", "ADOPTED", "A network Domain declaration was adopted."],
    ["23:16", "PRIORITY", "Operational priority."], ["15:12", "RESERVED", ""], ["11:0", "VID", "Operational VID."]])
fields("REST_TKLO", ACMP_REST_TALKER="Dead port: talker ID, low half.")
fields("REST_TKHI", ACMP_REST_TALKER="Dead port: talker ID, high half.")
fields("REST_META", ACMP_REST_TUID="Dead port: talker_unique_id.")
fields("REST_CTLO", ACMP_REST_CTLR="Dead port: controller ID, low half.")
fields("REST_CTHI", ACMP_REST_CTLR="Dead port: controller ID, high half.")
fields("REST_CMD", REST_PEND="Dead port. Commit; read back as busy. The ack never asserts, so it stays busy.",
       REST_DONE="A commit completed since reset.", REST_FLAGS="Binding flags `[23:8]` of the commit word.",
       REST_STAT="Read: status of the last commit. Write: the low bits of the binding flags.",
       REST_IDX="Write: target sink index. Read: last committed index.")
fields("JNL_CTRL", JNL_START="Discarded: start a slot image.", JNL_END="Discarded: image complete.", JNL_ABORT="Discarded: abort.",
       JNL_STAT="`[31]` busy, `[30]` done; a structural zero.")
fields("JNL_STAT", JNL_STAT=SZ + "The bit list is kept in the design notes.")
fields("AEMP_FIELD", AEMP_WDATA="Discarded. `[2:0]` was the field: 0 stream format, 1 sampling rate, 2 clock source; 3 and 4 refused.")
fields("AEMP_CTRL", AEMP_COMMIT="Discarded: commit.", AEMP_ABORT="Discarded: abort.",
       AEMP_STAT=SZ + "The bit list is kept in the design notes.")
note("ETH_GUARD", "The readback is the guard flop itself.", "A refused write never reads back as accepted.")
split("GPTP_LAT", "GPTP_LAT_NS", [
    ["31:16", "INGRESS", "Ingress correction in ns, subtracted from every arrival timestamp."],
    ["15:0", "EGRESS", "Egress correction in ns, added to every reconstructed launch timestamp."]])
note("GPTP_LAT", "Elaboration constants: a write changes nothing. Option OFF reads 0.")
fields("STRM_SEL", STRM_LSN0="Listener-0 row select. With `[8]` at 0, 1 makes the window's SRP row sink 0's dedicated row. "
       "`[8]` and `[3:0]` still store and still gate the window. A read returns 0.",
       STRM_DIR="Direction: 0 listener, 1 talker.", STRM_IDX="Stream index.")
note("STRM_SEL", "`{dir=0, idx=0}` is the park state.", "Writing `SEL` invalidates the ACMP and SRP read snapshots.",
     "Until a re-poll lands, snapshot-served words read 0.")
fields("STRM_SNAP", SNAP_BUSY="Writing 1 latches the selected stream's `STATE`, `CNT0..9` and `PDUS` as one coherent block. "
       "Read: busy. Poll it to 0 before reading the latched words.")
fields("STRMW_CTRL", STRMW_CTRL_31_1="Listener: `[2]` is the render route, `[1]` reads 0. Talker index above 0: the context word.",
       STRMW_CTRL_0="Enable. Talker index 0: a hard alias of `AAF_CTRL[0]`. A write at index above 0 also commits the staged SRP record.")
fields("STRMW_SID_LO", STRMW_SID_LO="stream_id `[31:0]`. Writes stage the provisioning stream_id; listener writes also forward "
       "to the context. A talker's word is the ID it starts with, not its current one after a MAAP conflict.")
fields("STRMW_SID_HI", STRMW_SID_HI="stream_id `[63:32]`, as `STRMW_SID_LO`.")
fields("STRMW_DMAC_LO", STRMW_DMAC_LO="Stream DMAC `[31:0]`. Talker index 0: a hard alias of `AAF_DMLO`. Writes stage the provisioning DMAC.")
fields("STRMW_DMAC_HI", STRMW_DMAC_HI="DMAC `[47:32]` in `[15:0]`. Talker index 0: a hard alias of `AAF_DMHI`.")
fields("STRMW_FMT_LO", STRMW_FMT_LO="Listener: current stream format `[31:0]` from the context. Talker: writes are ignored.")
fields("STRMW_FMT_HI", STRMW_FMT_HI="Listener: current stream format `[63:32]`. Talker: writes are ignored.")
fields("STRMW_STATE", STRMW_STATE="The snapshot-latched pack. Listener: `[2:0]` ACMP state, `[4:3]` probing, `[9:5]` status, "
       "`[10]` media_locked, `[18:11]` wire_chans, `[27:19]` the low 9 bits of `STRMW_SRP`. Talker: `[0]` probe_armed, "
       "`[1]` talker_active, `[2]` lobs, `[3]` composed admission, `[27:19]` the SRP bits.")
fields("STRMW_CTLR_LO", ACMP_CTLR_Q=SZ + "Was the binding controller's ID, low half: `i_acmp_tbl_gnt` is tied low, so nothing loads it.")
fields("STRMW_CTLR_HI", ACMP_CTLR_Q=SZ + "Was the binding controller's ID, high half.")
fields("STRMW_RSVD_86C", STRMW_RSVD_86C="No word is defined here. It reads the not-backed poison while the selected stream exists.")
fields("LTAP_CTRL", LTAP_EN="Measure enable, reset 1.", LTAP_CLR="Clears all statistics.",
       LTAP_STATUS="`[8]` tx_active, `[11:9]` tx stage awaited, `[12]` rx_active, `[15:13]` rx stage awaited.")
fields("LTAP", LTAP_REGS="Per-stage latency statistics, in axis_clk cycles.")
fields("APRB", APRB_REGS="RX stream-parser probe words.")
split("SLIP_LB", "SLIP_LB", [["31:16", "SKIPS", "Loopback-ring skips: queue full at a push, the oldest event dropped."],
      ["15:0", "DUPS", "Loopback-ring dups: a media tick found a pair's queue empty, so the hold repeats the last event."]])
split("SLIP_TDM", "SLIP_TDM", [["31:16", "SKIPS", "TDM-junction skips: a frame close over an unread frame."],
      ["15:0", "DUPS", "TDM-junction dups: a walk snapshot with no frame closed since the last one."]])
split("MCSRV_STAT", "MCSRV_STAT", [
    ["31:16", "TRIM", "Signed applied frequency trim, in 1/16 ppm."],
    ["15:10", "DISCARDED", "Discarded rate windows, saturating at 63."],
    ["9", "PHASE_SETTLED", "Phase settled (#632): inside 5 % of a sample period for four full windows (IEEE 1722-2016 10.8)."],
    ["8", "DRP_TIMEOUT", "DRP relock-timeout fault."],
    ["7", "PS_FAULT", "PSDONE-watchdog fault, sticky."],
    ["6", "PS_BUSY", "Fine-PS actuator busy."],
    ["5", "MMCM_LOCKED", "MMCM LOCKED, synchronised."],
    ["4", "DRP_MISMATCH", "DRP config mismatch; repaired only when `MCSRV_CTRL[1]` is set."],
    ["3", "DRP_VERIFIED", "DRP config verified."],
    ["2:0", "STATE", "0 IDLE, 1 VERIFY, 2 REPAIR, 3 ACQUIRE, 4 LOCKED, 5 HOLDOVER, 6 FAULT."]])
note("MCSRV_STAT", "At INTERNAL it reads IDLE with trim 0. The servo then moves nothing.")
fields("MCSRV_CTRL", MCSRV_PS_INVERT="Flips the servo's fine-PS direction: a bench sign knob.",
       MCSRV_AUTO_REPAIR="1 allows the DRP divider repair path. 0, the reset, is verify-only.")
fields("CHMAP_WORD", CHMAP_WR_DATA="The map word `{EN[15], SRC[14:12], rsvd[11:9], HALF[8], IDX_HI[7:4], IDX_LO[3:0]}`. "
       "A read returns the last committed word, not the map RAM.")
fields("CHMAP_SNAP", CHMAP_SNAP_TAG="Constant `0xC5`. Zero means the gateware predates this word.",
       CMRD_SIDE="Side latched at the last arm.", CMRD_ADDR="Index latched at the last arm.",
       CHMAP_RDBK="Capability: `[8]` render port wired, `[9]` capture port wired with the loop mask.",
       CMRD_ARMED="A snapshot has been armed since reset.",
       CMRD_UNSUP="Unsupported: the last arm was refused because this side has no readback port.",
       CMRD_TO="Timeout: the last snapshot ended without the fabric answering.",
       CMRD_VALID="Valid: the last snapshot carries fabric data.",
       CMRD_BUSY="Writing 1 arms a readback of the entry `CHMAP_SEL` names; ignored while busy. Read: busy.")
fields("CHMAP_LOOP", MASK_VALID="`[18:16]` are a measurement: capture side only.", VALID="This word is a measurement.",
       CMRD_ADDR="Index of the measured entry.", SIDE="Side of the measured entry.",
       LOOP_SUSPECT="`mapped` and not `fed`: a slot the map advertises that no audio has reached.",
       LOOP_FLAGS="`[17]` fed, `[16]` mapped.", RAW="Raw fabric readback word. The entry packing differs from the `CHMAP_WORD` you write.")
note("CHMAP_LOOP", "`0xDEADDEAD` means no measurement stands behind this word.")
split("PP_STAT", "PP_NVM_VERDICT", [["15:12", "PP_NVM_VERDICT", "Verdict code of the last image offered."]]) if False else None
fields("PP_STAT", PP_PRESENT_TAG="Constant `0x5B`. A read of 0 means the gateware predates this group.",
       PP_RESTORE_CAUSE="The binding walk's cause: 1 torn, 2 device error, 3 deadline.",
       PP_RS_CAUSE="The D3 walk's first abort cause, valid with `[3]`: 1 torn, 2 device error, 3 deadline, 5 passes disagree, "
       "6 descriptor fault, 7 image not proven.",
       PP_RESTORE_RB="A pass-1 abort rolled the stores back to DEFAULTS.",
       PP_RESTORE_CLOSED="The D3 walk ended CLOSED: fail, never done, AECP held until reset.",
       PP_NVM_VERDICT="Verdict code of the last image offered.",
       PP_NVM_PEND="Accepted work no verified slot holds and `nvm_dirty` does not report. A durable reading needs it at 0.",
       PP_NVM_IMG_VALID="Firmware validated the image in the window.",
       PP_NVM_STALE="`nvm_backed` was true since reset and is now false, and the loss is not made good.",
       PP_NVM_DIRTY="The image holds committed changes no flash slot yet holds.",
       PP_NVM_BLANK="The completed restore validated zero records and none failed.",
       PP_NVM_BACKED="Live evidence: a writer answered within `T-NVM-WRITER-ALIVE` and no unrevoked failure is outstanding.",
       PP_ERR="The last side-port access returned an error.",
       PP_NVM_ALARM="A record producer exhausted its three write attempts. Reset-sticky.",
       PP_RESTORE_FAIL="A walk failed or ran blind, or the map restore rolled back to its reset set.",
       PP_RESTORE_DONE="Both boot walks sequenced to COMPLETE or DEFAULTS and the map restore ended. Not the same as succeeded.",
       PP_RESTORE_BUSY="A walk or the map restore is running.", PP_BUSY="A side-port access is outstanding.")
fields("PP_SPADDR", PP_SPADDR="Side-port word address. A read returns the armed address.")
split("PP_DIAG", "PP_RX_DROPS", [["15:8", "PP_RX_DROPS", "Control frames lost to a full ingress FIFO."]]) if False else None
fields("PP_DIAG", PP_TX_FRAMES="Control frames transmitted.", PP_RX_DROPS="Control frames lost to a full ingress FIFO.",
       PP_RX_FRAMES="Control frames received.")
fields("PP_NVM_SEL", PP_NVM_SEL="The backing store's word index the next `PP_NVM_DATA` access names. 0 image base, 1 image length, "
       "2 image sequence, 3 status and verdict, 4 strobes, 5 capture identity, 8 to 15 record ownership, `0x20` and `0x30` plus port the map tables.")
split("PP_NVM_STAT", "PP_NVM_CSR_RDATA", [
    ["31:24", "TAG", "Contract tag `0xC3`: read it first. 0 means the gateware predates the contract, and a writer must disable itself. A write here is the strobe word: `[0]` heartbeat, `[1]` commit acknowledged, `[2]` commit started, `[3]` ARM, `[4]` ATTEST, `[5]` RELEASE, `[6]` RELOAD."],
    ["23", "UNRES", "At least one record is open."], ["22", "NVM_PEND", "The same wire as `PP_STAT[11]`."],
    ["21", "ARM_REFUSED", "The last ARM was not accepted."], ["20", "ACK_REFUSED", "Ack refused."],
    ["19", "ATTESTED", "Attested."], ["18", "VALID", "No mutating grant since the arm."],
    ["17", "HOLD", "Mutating requests are being deferred."], ["16", "OPEN", "A capture is open."],
    ["15:12", "VERDICT", "Verdict of the last slot judged, or the writer's transaction verdict."],
    ["11", "RELOAD_REFUSED", "The last RELOAD strobe was refused."],
    ["10", "COMMIT_BUSY", "A commit is inside its `T-NVM-COMMIT-TIMEOUT` bracket."],
    ["9", "NVM_STALE", "See `PP_STAT[9]`."], ["8", "NVM_DIRTY", "Committable image work."], ["7", "IMG_VALID", "See `PP_STAT[10]`."],
    ["6", "NVM_BACKED", "See `PP_STAT[6]`."], ["5", "IMG_CFG", "An image length is set."],
    ["4", "DEV_BUSY", "A record operation is in flight on the device face."],
    ["3", "LOAD_PENDING", "A boot window load may still be accepted."],
    ["2", "LOAD_ACCEPTED", "A RELOAD has been accepted since reset. While 0 the backend arms no capture."],
    ["1:0", "RESERVED", ""]])
json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
open(p, "a").write("\n")

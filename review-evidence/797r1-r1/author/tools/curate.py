#!/usr/bin/env python3
"""Curate the drafted descriptions into scripts/register_descriptions.json:
names, purposes, D0 corrections, the A10 additions, array instance tables,
the memory-bridge rows moved to the LiteX CSRs, the split VERSION log."""
import json
import re
import sys
from pathlib import Path

DRAFT, OLDROWS, OUT = (Path(a) for a in sys.argv[1:4])
d = json.loads(DRAFT.read_text())
old = json.loads(OLDROWS.read_text())
R = d["registers"]

# ---- names and purposes (purpose: one sentence, ten words or fewer) -------
NP = {
    "ID": ("Identification", "Constant magic word that identifies the Milan CSR block."),
    "VERSION": ("Gateware version", "Major and minor version of this CSR block's ABI."),
    "CAP": ("Capabilities", "Constant capability flags and the queue-window geometry."),
    "SCRATCH": ("Scratch", "Read/write word for bus liveness tests."),
    "IRQ_STATUS": ("Interrupt status", "Latched interrupt events, cleared by writing 1."),
    "IRQ_MASK": ("Interrupt mask", "Enables each interrupt source onto the IRQ line."),
    "IRQ_RAW": ("Raw interrupt status", "Latched interrupt events before masking."),
    "MAC_CTRL": ("MAC control", "MAC enables, receive filtering modes and the link-rate override."),
    "MAC_IFG": ("MAC inter-frame gap", "Inter-frame gap in bytes."),
    "MAC_ALO": ("Station MAC address, low word", "Station MAC address bits 31 to 0."),
    "MAC_AHI": ("Station MAC address, high word", "Station MAC address bits 47 to 32."),
    "MAC_STATUS": ("MAC link status", "Link, speed and duplex as the SoC publishes them."),
    "MC_LO": ("Multicast hash, low word", "Multicast hash filter buckets 0 to 31."),
    "MC_HI": ("Multicast hash, high word", "Multicast hash filter buckets 32 to 63."),
    "PHY_RST": ("PHY reset (inert)", "Stored PHY reset bit that the shipping SoC leaves unconnected."),
    "STATS_CTRL": ("Statistics control", "Snapshot and reset strobes for the RMON counters."),
    "STATS_CAP": ("Statistics capability", "Marks which RMON counter lanes have a real source."),
    "STATS": ("RMON counter snapshot", "Snapshot of one RMON counter, latched by STATS_CTRL."),
    "CLS_CTRL": ("Classifier control (scratch)", "Retained classifier control word; no logic reads it."),
    "CLS_DPCP": ("Classifier default PCP (scratch)", "Retained default-priority word; no logic reads it."),
    "CLS_MAP": ("PCP to traffic-class map (scratch)", "Retained PCP to traffic-class map; no logic reads it."),
    "CLS_REGEN": ("Priority regeneration (scratch)", "Retained priority regeneration map; no logic reads it."),
    "CLS_TCQ": ("Traffic-class to queue map (scratch)", "Retained traffic-class to queue map; no logic reads it."),
    "CBS_IDLE": ("CBS idleSlope (scratch)", "Retained idleSlope word for one queue; nothing reads it."),
    "CBS_HI": ("CBS hiCredit (scratch)", "Retained hiCredit word for one queue; nothing reads it."),
    "CBS_LO": ("CBS loCredit (scratch)", "Retained loCredit word for one queue; nothing reads it."),
    "CBS_EN": ("CBS control (scratch)", "Retained shaping enable for one queue; nothing reads it."),
    "PTP_CTRL": ("PTP clock control", "Enables the PTP hardware clock counter."),
    "PTP_INCR": ("PTP increment", "Nominal clock increment per tick, Q8.24 nanoseconds."),
    "PTP_ADJ": ("PTP fine adjustment", "Signed addend applied on every tick."),
    "PTP_TWLO": ("PTP settime target, low word", "Time-of-day target for settime, bits 31 to 0."),
    "PTP_TWHI": ("PTP settime target, high word", "Time-of-day target for settime, bits 63 to 32."),
    "PTP_OFLO": ("PTP adjtime offset, low word", "Signed adjtime delta, bits 31 to 0."),
    "PTP_OFHI": ("PTP adjtime offset, high word", "Signed adjtime delta, bits 63 to 32."),
    "PTP_CMD": ("PTP command", "Strobes that apply settime, adjtime or a time snapshot."),
    "PTP_TRLO": ("PTP time snapshot, low word", "Time of day latched by the last snapshot, low word."),
    "PTP_TRHI": ("PTP time snapshot, high word", "Time of day latched by the last snapshot, high word."),
    "PTP_ILAT": ("Ingress latency (scratch)", "Readable inert scratch; corrections are published at GPTP_LAT."),
    "PTP_ELAT": ("Egress latency (scratch)", "Readable inert scratch; corrections are published at GPTP_LAT."),
    "PPS_CTRL": ("PPS alarm control", "PPS enable, arm strobe and the built capability bit."),
    "PPS_TGLO": ("PPS target, low word", "Absolute PPS target to arm, bits 31 to 0."),
    "PPS_TGHI": ("PPS target, high word", "Absolute PPS target to arm, bits 63 to 32."),
    "PPS_RDLO": ("PPS live target, low word", "Target the PHC publishes back, bits 31 to 0."),
    "PPS_RDHI": ("PPS live target, high word", "Target the PHC publishes back, bits 63 to 32."),
    "PPS_WIDTH": ("PPS pulse width", "PPS pulse width in PHC clock cycles."),
    "ADP_CTRL": ("ADP control", "Entity enable and the advertised valid time."),
    "ADP_EIDLO": ("Entity ID, low word", "entity_id bits 31 to 0."),
    "ADP_EIDHI": ("Entity ID, high word", "entity_id bits 63 to 32."),
    "ADP_MIDLO": ("Entity model ID, low word", "entity_model_id bits 31 to 0."),
    "ADP_MIDHI": ("Entity model ID, high word", "entity_model_id bits 63 to 32."),
    "ADP_ECAPS": ("Entity capabilities (scratch)", "Stored and read back; the processor supplies the ADPDU field."),
    "ADP_TALK": ("ADP talker shape", "Constant talker sources and capabilities from the build config."),
    "ADP_LIST": ("ADP listener shape", "Constant listener sinks and capabilities from the build config."),
    "ADP_CCAPS": ("Controller capabilities (scratch)", "Stored and read back; the processor supplies the ADPDU field."),
    "ADP_GMLO": ("gPTP grandmaster, low word", "Grandmaster identity bits 31 to 0, coherent with GMHI."),
    "ADP_GMHI": ("gPTP grandmaster, high word", "Grandmaster identity bits 63 to 32, coherent with GMLO."),
    "ADP_DOMAIN": ("gPTP domain", "The gPTP domain number, a structural zero."),
    "ADP_IDX0": ("ADP indices 0", "Current configuration and identify-control indices."),
    "ADP_IDX1": ("ADP indices 1 (scratch)", "Stored interface index; never reaches the wire."),
    "ADP_ASLO": ("Association ID, low word (scratch)", "Stored association_id bits 31 to 0; never reaches the wire."),
    "ADP_ASHI": ("Association ID, high word (scratch)", "Stored association_id bits 63 to 32; never reaches the wire."),
    "ADP_CMD": ("ADP command", "Advertise-now and depart strobes."),
    "ADP_STATUS": ("ADP status", "The available_index the processor advertises."),
    "AECP_STAT0": ("AECP status 0", "Entity lock level and a retired command count."),
    "AECP_STAT1": ("AECP status 1", "Retired AECP response count and configuration index."),
    "ACMP_STAT": ("ACMP status", "Retired ACMP command and response counts."),
    "AAF_CTRL": ("AAF talker control", "AAF talker enable, gate bypass and stream VID."),
    "AAF_DMLO": ("AAF destination MAC, low word", "AAF stream destination MAC bits 31 to 0."),
    "AAF_DMHI": ("AAF destination MAC, high word", "AAF stream destination MAC bits 47 to 32."),
    "AAF_FRAMES": ("AAF frames sent", "AAF frames the talker has sent."),
    "AAF_PAIRS": ("AAF pairs captured", "Audio sample pairs the talker front end captured."),
    "ADP_DIAG": ("ADP diagnostics", "Retired ADP depart and re-arm counters."),
    "ACMP_TALKER": ("ACMP talker state", "Talker probe, active, observed and gate bits."),
    "ACMP_LOBS": ("Listener-observed override", "Manual listener_observed override for the AAF gate."),
    "ADP_DIAG2": ("ADP liveness diagnostics", "Retired ADP liveness and discover counters."),
    "LWSRP_CTRL": ("SRP control", "SRP admission enable and talker admission arm."),
    "LWSRP_VID": ("SRP VID", "Software-owned default SR VID."),
    "LWSRP_DMLO": ("SRP destination MAC, low word (scratch)", "Retained stream destination MAC bits 31 to 0."),
    "LWSRP_DMHI": ("SRP destination MAC, high word (scratch)", "Retained stream destination MAC bits 47 to 32."),
    "LWSRP_TSPEC": ("SRP TSpec (scratch)", "Retained MaxFrameSize and MaxIntervalFrames words."),
    "LWSRP_STATUS": ("SRP status", "SRP registrar and declaration status from the processor."),
    "LWSRP_SLOPE": ("SRP granted slope", "Granted idleSlope summed across admitted sources."),
    "LWSRP_CNT": ("SRP PDU counts", "Retired MRPDU counters, a structural zero."),
    "LWSRP_LAT": ("SRP accumulated latency", "TalkerAdvertise AccumulatedLatency in nanoseconds."),
    "ACMPL_STATE": ("ACMP listener state", "Bound state of listener sink 0 and its SRP bits."),
    "ACMPL_TKLO": ("Bound talker, low word", "Retired bound talker entity ID, a structural zero."),
    "ACMPL_TKHI": ("Bound talker, high word", "Retired bound talker entity ID, a structural zero."),
    "ACMPL_CNT": ("ACMP listener counts", "Retired listener command counts, a structural zero."),
    "ACMPL_TUID": ("ACMP listener talker ID", "Retired talker unique ID and the live failure code."),
    "AVTPRX_STAT": ("AVTP RX status (saturating views)", "Stream Input 0 lock and interruption counters."),
    "AVTPRX_FRX": ("AVTP RX frames received", "Stream Input 0 FRAMES_RX, a full 32-bit counter."),
    "AVTPRX_ERR": ("AVTP RX errors (saturating views)", "Stream Input 0 sequence, format and timestamp counters."),
    "PCMRX_CNT": ("AAF RX depacketizer counts", "Frames dropped and payloads emitted by the depacketizer."),
    "PCMRX_TS": ("AAF RX last timestamp", "avtp_timestamp of the last depacketized PDU."),
    "MAAP_CTRL": ("MAAP control", "MAAP enable, seed and block count."),
    "MAAP_STAT0": ("MAAP status 0", "MAAP conflicts, defends and the claimed offset."),
    "MAAP_STAT1": ("MAAP status 1", "MAAP state and address-valid flag."),
    "I2SPB_STAT": ("I2S playback drift rails", "Underrun and overrun counts, each half cleared on write."),
    "TONE_CTRL": ("Pilot tone control", "Pilot tone enable and attenuation."),
    "I2SPB_TRIM": ("I2S playback trim", "Media-clock recovery trim and FIFO fill."),
    "GPTP_PDELAY": ("gPTP neighbor delay", "Measured gPTP neighbor propagation delay in nanoseconds."),
    "ACMPL_DBG": ("Listener walker forensics", "Retired listener walker counters, a structural zero."),
    "AVTPRX_TSD": ("AVTP RX timestamp delta", "Signed timestamp delta at the last accepted PDU."),
    "I2SPB_DBG": ("I2S DAC forensics", "Serial bits of the last left half-frame at the DAC."),
    "CTLR_DIAG": ("Controller diagnostics", "Retired controller counter, a structural zero."),
    "TCAM_CTRL": ("TCAM control", "Default pass and address-filter enable for the RX filter."),
    "TCAM_KLO": ("TCAM key, low word", "Match key bits 31 to 0 for the next commit."),
    "TCAM_KHI": ("TCAM key, high word", "Match key bits 47 to 32 for the next commit."),
    "TCAM_MLO": ("TCAM mask, low word", "Care mask bits 31 to 0 for the next commit."),
    "TCAM_MHI": ("TCAM mask, high word", "Care mask bits 47 to 32 for the next commit."),
    "TCAM_ACT": ("TCAM action", "Action byte for the next commit."),
    "TCAM_CMD": ("TCAM command", "Commits one TCAM entry: index, add or remove."),
    "LINK_CTRL": ("Link control", "Firmware link qualification and link-guard controls."),
    "RST_EPOCH": ("Reset epoch", "Count of datapath reset releases, the reset canary."),
    "ENT_NAME_LO": ("Entity name overlay, characters 0 to 3", "Board-name overlay characters 0 to 3."),
    "ENT_NAME_HI": ("Entity name overlay, characters 4 to 7", "Board-name overlay characters 4 to 7."),
    "LPF_CTRL": ("Playback filter control", "Enables the playback low-pass filter."),
    "AS2_LO": ("gPTP parent, low word", "Parent clockIdentity bits 31 to 0, coherent with AS2_HI."),
    "AS2_HI": ("gPTP parent, high word", "Parent clockIdentity bits 63 to 32, coherent with AS2_LO."),
    "CRF_CTRL": ("CRF sink control", "CRF sink enable and the locked flag."),
    "CRF_SIDLO": ("CRF sink stream ID, low word", "Followed CRF stream_id bits 31 to 0."),
    "CRF_SIDHI": ("CRF sink stream ID, high word", "Followed CRF stream_id bits 63 to 32."),
    "CRF_DELTA": ("CRF timestamp delta", "Signed crf_ts minus ptp_now at the last PDU."),
    "CRF_RATE": ("CRF rate", "Talker media clock rate measured against gPTP."),
    "CRF_STATUS": ("CRF status", "CRF PDUs accepted, format errors and sequence errors."),
    "CRFT_CTRL": ("CRF talker control", "CRF talker enable, class-A declare and live status."),
    "CRFT_SIDLO": ("CRF talker stream ID, low word", "CRF talker stream_id bits 31 to 0."),
    "CRFT_SIDHI": ("CRF talker stream ID, high word", "CRF talker stream_id bits 63 to 32."),
    "CRFT_DMLO": ("CRF talker destination MAC, low word", "CRF talker destination MAC bits 31 to 0."),
    "CRFT_DMHI": ("CRF talker destination MAC, high word", "CRF talker destination MAC bits 47 to 32."),
    "CRFT_COUNT": ("CRF talker PDU count", "CRF PDUs emitted since reset."),
    "BDBG0": ("Scan forensics 0", "Retired AECP scan forensics, a structural zero."),
    "BDBG1": ("Scan forensics 1", "Retired AECP scan forensics, a structural zero."),
    "BDBG2": ("Scan forensics 2", "Retired AECP scan forensics, a structural zero."),
    "LINKG_STAT": ("Link guard status", "Live link-guard state, flags and bounce count."),
    "CLKV_CTRL": ("Clock validity control (inert)", "Retained address; reads zero and writes change nothing."),
    "CLKV_STAT": ("Clock validity status", "The tu verdict and the fabric sync and asCapable state."),
    "CLKV_TUCNT": ("Timestamp-uncertain count", "Seconds in which the talkers stamped tu."),
    "TXARB_DIAG": ("TX arbiter diagnostics", "TX trunk arbiter lock supervision per lane."),
    "LWSRP_DOM": ("SRP operational domain", "Operational SR class-A VID and priority."),
    "REST_TKLO": ("Bind-restore talker, low word", "Saved talker_entity_id bits 31 to 0."),
    "REST_TKHI": ("Bind-restore talker, high word", "Saved talker_entity_id bits 63 to 32."),
    "REST_META": ("Bind-restore metadata", "Saved talker_unique_id and VLAN."),
    "REST_CTLO": ("Bind-restore controller, low word", "Saved controller_entity_id bits 31 to 0."),
    "REST_CTHI": ("Bind-restore controller, high word", "Saved controller_entity_id bits 63 to 32."),
    "REST_CMD": ("Bind-restore command", "Commit and status of the retired bind-restore port."),
    "JNL_CTRL": ("Journal ingest control", "Start, end and abort strobes of the retired journal ingest."),
    "JNL_DATA": ("Journal ingest data", "Next journal word for the retired journal ingest."),
    "JNL_STAT": ("Journal ingest status", "Retired journal engine status, a structural zero."),
    "JNL_SEQ": ("Journal ingest sequence", "Retired accepted-image sequence, a structural zero."),
    "AEMP_SEL": ("AEM patch select", "Descriptor selection for the retired AEM patch port."),
    "AEMP_FIELD": ("AEM patch field", "Field selection for the retired AEM patch port."),
    "AEMP_DATA": ("AEM patch data", "Payload word for the retired AEM patch port."),
    "AEMP_CTRL": ("AEM patch control", "Commit and abort strobes of the retired AEM patch port."),
    "ETH_GUARD": ("Ethernet guard", "Kill switch that refuses the CPU's Ethernet disruption levers."),
    "ASP_LO": ("AS_PATH staging, low word (retired)", "Retired AS_PATH address; reads zero."),
    "ASP_HI": ("AS_PATH staging, high word (retired)", "Retired AS_PATH address; reads zero."),
    "ASP_CMD": ("AS_PATH status", "Generation and length of the fabric's selected PathTrace."),
    "GPTP_DROPW": ("gPTP wire drops", "gPTP frames lost at the tap or the parser."),
    "GPTP_DROPE": ("gPTP event drops", "Lost launch records and refused gPTP events."),
    "GPTP_LAT": ("gPTP latency corrections", "Ingress and egress timestamp corrections the plane applies."),
    "STRM_SEL": ("Stream window select", "Selects the stream the 0x810 to 0x868 words view."),
    "STRM_SNAP": ("Stream window snapshot", "Latches the selected stream's state and counters."),
    "STRMW_CTRL": ("Stream window control", "Enable and route flags of the selected stream."),
    "STRMW_SID_LO": ("Stream window stream ID, low word", "stream_id bits 31 to 0 of the selected stream."),
    "STRMW_SID_HI": ("Stream window stream ID, high word", "stream_id bits 63 to 32 of the selected stream."),
    "STRMW_DMAC_LO": ("Stream window destination MAC, low word", "Destination MAC bits 31 to 0 of the selected stream."),
    "STRMW_DMAC_HI": ("Stream window destination MAC, high word", "Destination MAC bits 47 to 32 of the selected stream."),
    "STRMW_FMT_LO": ("Stream window format, low word", "Current stream format bits 31 to 0."),
    "STRMW_FMT_HI": ("Stream window format, high word", "Current stream format bits 63 to 32."),
    "STRMW_STATE": ("Stream window state", "Snapshot-latched state word of the selected stream."),
    "STRMW_CNT": ("Stream window counter", "One of the ten snapshot-latched Stream Input counters."),
    "STRMW_PDUS": ("Stream window PDU count", "Snapshot-latched PDU and drop counts of the selected stream."),
    "STRMW_SRP": ("Stream window SRP status", "SRP status of the selected stream."),
    "STRMW_CTLR_LO": ("Stream window controller, low word", "Retired binding controller ID, a structural zero."),
    "STRMW_CTLR_HI": ("Stream window controller, high word", "Retired binding controller ID, a structural zero."),
    "STRMW_BIND": ("Stream window binding", "Retired binding flags and talker ID, a structural zero."),
    "LTAP_CTRL": ("Latency tap control", "Latency tap enable, clear strobe and live status."),
    "LTAP": ("Latency tap readback", "One packed readback word of the AAF latency taps."),
    "APRB": ("Stream parser probe", "One readback word of the RX stream-parser probe."),
    "RSVD_GAP": ("Reserved compatibility word", "Retired telemetry word; reads zero and ignores writes."),
    "SLIP_LB": ("Loopback slip counters", "Loopback-ring duplicate and skip counts."),
    "SLIP_TDM": ("TDM slip counters", "TDM-junction duplicate and skip counts."),
    "RENDER_STAT": ("Render presentation state", "Presentation state of the selected listener."),
    "AAFM_STAT": ("AAF clock meter status", "AAF clock meter status and diagnostics."),
    "AAFM_RATE": ("AAF clock meter rate", "Signed AAF media rate in CRF_RATE units."),
    "MCSRV_STAT": ("Media-clock servo status", "MMCM DRP servo state, trim and flags."),
    "MCSRV_CTRL": ("Media-clock servo control", "Servo direction knob and repair enable."),
    "CHMAP_CTRL": ("Channel map control", "Arms the channel-map debug write window."),
    "CHMAP_SEL": ("Channel map select", "Map side and entry index for writes and readback."),
    "CHMAP_WORD": ("Channel map word", "Map word committed through the shared write port."),
    "CHMAP_STAT": ("Channel map status", "Committed and refused map-word writes."),
    "CHMAP_SNAP": ("Channel map snapshot", "Arms a map RAM readback and reports its status."),
    "CHMAP_LOOP": ("Channel map readback", "The map word the RAM holds, or 0xDEADDEAD."),
    "PP_CTRL": ("Processor control", "Entity enable and the restore-walk start."),
    "PP_STAT": ("Processor status", "Presence tag, saved-state verdict and side-port status."),
    "PP_SPADDR": ("Processor side-port address", "Side-port word address; a write posts a read."),
    "PP_SPDATA": ("Processor side-port data", "Posted read data; a write posts a side-port write."),
    "PP_DIAG": ("Processor frame diagnostics", "Control frames sent, received and dropped."),
    "PP_NVM_SEL": ("Saved-state window select", "Index of the backend word PP_NVM_DATA reads or writes."),
    "PP_NVM_DATA": ("Saved-state window data", "The backend word PP_NVM_SEL names."),
    "PP_NVM_STAT": ("Saved-state status and strobes", "Backend status word on read, strobe word on write."),
}
for label, (name, purpose) in NP.items():
    R[label]["name"] = name
    R[label]["purpose"] = purpose
missing = [k for k in R if not R[k]["purpose"]]
assert not missing, missing

# ---- acronyms: the documented ABI names --------------------------------
R["STATS"]["acronym"] = "STAT"
R["LTAP"]["acronym"] = "LTAP_W"
R["APRB"]["acronym"] = "APRB_W"
R["STRMW_CNT"]["acronym"] = "STRMW_CNT"
R["RSVD_GAP"]["acronym"] = "RSVD_GAP"
for k, v in R.items():
    v["acronym"] = v["acronym"].removeprefix("A_")
    if v["acronym"] == k:
        del v["acronym"]

# ---- array instance tables -----------------------------------------------
for label, extra in (("STATS", "Name"), ("LTAP", "Name"), ("APRB", "Name")):
    rows = [["n", "Offset", "Name", "Producer reset", "Description"]]
    for n, r in enumerate(x for x in old[label] if x["line"] < 2500):
        rows.append([str(n), f"`{r['offset']}`", r["name"], r["reset"], r["desc"]])
    R[label]["notes"] = [{"table": rows}]
    R[label]["fields"] = {}

# ---- the CBS rows that were the memory-bridge table ------------------------
bridge = {"desc_req": "ppmem_desc_req", "desc_fault": "ppmem_desc_fault",
          "resp_req": "ppmem_resp_req", "resp_fault": "ppmem_resp_fault"}
soc_regs = {}
for label in ("CBS_IDLE", "CBS_HI", "CBS_LO", "CBS_EN"):
    for r in old[label]:
        name = r["name"].strip("`")
        if name in bridge:
            soc_regs[bridge[name]] = r["desc"]
    R[label]["notes"] = [n for n in R[label]["notes"] if not any(
        n == r["desc"] for r in old[label] if r["name"].strip("`") in bridge)]
for grp in d["soc_notes"]:
    keep = []
    for item in grp["rows"]:
        if isinstance(item, dict) and "table" in item and item["table"][1][1] == "`stat`":
            soc_regs["ppmem_stat"] = item["table"][1][4]
            continue
        keep.append(item)
    grp["rows"] = keep

# ---- D0 corrections, quoted and rewritten ---------------------------------
def replace_everywhere(old_text, new_text, must=True):
    blob = json.dumps(d, ensure_ascii=False)
    count = blob.count(json.dumps(old_text, ensure_ascii=False)[1:-1])
    if must:
        assert count, old_text
    blob = blob.replace(json.dumps(old_text, ensure_ascii=False)[1:-1], json.dumps(new_text, ensure_ascii=False)[1:-1])
    d.clear()
    d.update(json.loads(blob))
    return count


replace_everywhere("802.1Q 35.2.2.7.4 FourPackedEvents", "802.1Q 35.2.2.7.2 (Table 35-3) FourPackedEvents")
replace_everywhere("Milan Table 7-156", "IEEE 1722.1-2021 Table 7-156, Milan v1.2 Table 5.6")
replace_everywhere("**Every Stream Output's presentation-time offset is pinned at the Milan 2 ms default** "
                   "(`SET_MAX_TRANSIT_TIME` is gone).",
                   "**Every Stream Output's presentation-time offset defaults to the Milan 2 ms value**, and "
                   "SET_STREAM_INFO sets each Stream Output's offset, which the framers apply "
                   "(`SET_MAX_TRANSIT_TIME` is gone).")
replace_everywhere("Physical switch-cycle acceptance remains on [#599](https://github.com/kebag-logic/milan-fpga/issues/599).",
                   "Physical switch-cycle acceptance is recorded in the [#599 link-cycle finding]"
                   "(../findings/599_394_E1_LINK_CYCLES.md).")
replace_everywhere("Bare-metal firmware publishes PHY state into LiteX `milan_mac.link_status`.",
                   "Bare-metal firmware publishes PHY state into LiteX `milan_mac.link_status`, but only while "
                   "the saved-state writer runs (`phy_link_tick()` runs inside `nvm_heartbeat_tick()`); "
                   "otherwise MAC_STATUS keeps its reset value: link up, 1000 Mb/s, full duplex.")
R = d["registers"]

# ---- the A10 additions and D0-014/015/017 ----------------------------------
R["ETH_GUARD"]["fields"] = {
    "ETH_GUARD": "1 = guarded: the reset state, armed at power-on. Software may re-arm it before risky work. "
                 "The link guard's own automatic recovery is not gated. The SoC exports the level "
                 "(`o_eth_guard`), but at this head nothing in `sw/litex/milan_soc.py` consumes it, so the LiteX "
                 "`milan_mac_phy_crg_reset` CSR is NOT gated.",
}
R["ETH_GUARD"]["notes"] = [
    "The readback is the guard flop itself, so a refused write never reads back as accepted. The RTL comments "
    "on the `o_eth_guard` port and on `A_ETH_GUARD` in `hdl/common/csr/milan_csr.sv` say the guard also gates "
    "the LiteX PHY reset chain; the SoC does not implement that gating at this head (issue #797 records the "
    "decision it needs)."]
R["PHY_RST"]["fields"]["PHY_RESET_N"] = (
    "Drives `o_phy_reset_n` (0 = reset asserted). The shipping SoC leaves that datapath output unconnected, so "
    "this bit resets nothing. The PHY reset that reaches the pin is the LiteX `milan_mac_phy_crg_reset` CSR "
    "(the PHY clock/reset block's `_reset` storage, `sw/litex/patches/0002-liteeth-gmii-tx-clk-invert.patch`), "
    "for the port the image is built for (`--eth-port`).")
R["MAC_STATUS"]["notes"] = [
    "The three bits mirror the LiteX `milan_mac_link_status` CSR, synchronised into the datapath clock "
    "(`sw/litex/milan_soc.py`, the `link_status` CSRStorage). Its reset value is link up, 1000 Mb/s on GMII "
    "(100 on MII) and full duplex, so this word reads `0x0000000D` on the AX7101 until firmware writes the CSR.",
    "Firmware writes that CSR from MDIO only while the saved-state writer runs; otherwise the reset value "
    "stays. The word does not follow the link on its own. For the link, read `LINKG_STAT` (0x774), the "
    "AVB_INTERFACE LINK_UP and LINK_DOWN counters, or the PHY's BMSR over MDIO."]
R["LINK_CTRL"]["notes"] = R["LINK_CTRL"].get("notes", [])

# ---- 0x600 and stream-count corrections -----------------------------------
replace_everywhere("**They both default to 1 in the RTL, and the shipping AX7101 shape is 8**",
                   "**They both default to 1 in the RTL, and the shipping AX7101 (`endstation_ax7101_1x1_tdm8`) "
                   "is the one-AAF-stream shape**; `endstation_ax7101_8x8.yaml` declares 8 of each")

# ---- saved state: D0-058 and D0-059 ----------------------------------------
n058 = replace_everywhere("**Nothing in this device persists a binding across a power cycle.**",
                          "**This CSR port persists nothing; bindings persist through the processor's restore "
                          "walk and `KL_nvm_backend` (see `PP_NVM_*` at 0x934 and `PP_STAT` at 0x924), and the "
                          "binding survives a cold power cycle on silicon since 2026-09-21 (#70).** The paragraph "
                          "below is the record from before that backend landed:")
n059 = replace_everywhere("is **not met by this build**.",
                          "is no longer served by this retired CSR face; the saved-state store serves it, with the "
                          "open physical items on #70.")
print("D0-058 hits", n058, "D0-059 hits", n059)

# ---- VERSION changelog: one row per minor -----------------------------------
ver = R["VERSION"]
blob = " ".join(n for n in ver["notes"] if isinstance(n, str))
cut = re.split(r"(?=(?:\*\*)?Prior: |(?<=, )0x00[0-9A-F]{2} )", blob)
rows = [["Entry", "Change"]]
for k, part in enumerate(p.strip(" ,") for p in cut if p.strip(" ,")):
    m = re.search(r"0x00[0-9A-F]{2}", part)
    rows.append([m.group(0) if m else f"note {k}", part])
ver["notes"] = [{"heading": "VERSION minor changelog (chronological landing record)",
                 "rows": [{"table": rows}]}]

# ---- module purposes --------------------------------------------------------
MP = {
    "ident": "Identification, capabilities and the interrupt registers.",
    "mac": "MAC control, link status and the inert PHY reset.",
    "stats": "RMON counter snapshot and its capability mask.",
    "cls": "Retained classifier words; no logic reads them.",
    "cbs": "Retained per-queue CBS words; nothing reads them.",
    "ptp": "PTP hardware clock control, time access and PPS alarm.",
    "adp": "ADP identity words, the advertise strobes and status.",
    "aecp": "AECP and ACMP status, and the flat AAF talker words.",
    "lwsrp": "SRP control and the processor's SRP status.",
    "acmpl": "Listener bind record, AVTP RX, MAAP and audio diagnostics.",
    "tcam": "RX destination-MAC filter programming.",
    "link": "Link guard controls and the reset canary.",
    "overlay": "Entity name overlay, playback filter and gPTP parent.",
    "crf": "CRF media-clock sink control and measurements.",
    "crft": "CRF media-clock talker control and counters.",
    "bdbg": "Retired scan forensics and the live link-guard status.",
    "clkv": "Clock validity, TX arbiter supervision and the SRP domain.",
    "rest": "Retired bind-restore port, kept as an ABI.",
    "jnl": "Retired journal ingest port, kept as an ABI.",
    "aemp": "Retired AEM patch port, kept as an ABI.",
    "guard": "The Ethernet guard kill switch.",
    "asp": "Retired AS_PATH addresses and the live PathTrace status.",
    "gptpd": "gPTP plane drop counters.",
    "gptpl": "The timestamp corrections the gPTP plane applies.",
    "strm": "Indexed window onto one stream's context.",
    "ltap": "AAF per-stage latency taps.",
    "aprb": "The RX stream parser's pre-match view.",
    "gap": "Retired telemetry words that read zero.",
    "slip": "Media-boundary slip counters.",
    "render": "Presentation state of the selected listener.",
    "aafm": "AAF media clock meter.",
    "mcsrv": "MMCM DRP media-clock servo.",
    "chmap": "Channel-map debug write port and map RAM readback.",
    "pp": "Protocol-processor control plane and the saved-state window.",
}
for m in d["modules"]:
    m["purpose"] = MP[m["key"]]

# ---- SoC side ---------------------------------------------------------------
d["regions"] = {
    "rom": "Boot ROM holding the bare-metal firmware image.",
    "sram": "On-chip SRAM: the firmware's stack and data.",
    "main_ram": "DDR3 main memory.",
    "spiflash": "Memory-mapped QSPI flash (read path).",
    "milan_csr": "The Milan CSR block this page documents.",
    "csr": "LiteX CSR banks.",
    "clint": "RISC-V core-local interruptor.",
    "plic": "RISC-V platform-level interrupt controller.",
    "milan_flashboot_aem": "Flash slot of the AEM entity image.",
    "milan_flash_journal": "Flash slots of the saved-state journal (A and B); a reflash must not erase it.",
    "milan_flash_user": "Reserved user flash range.",
    "pp_window": "The protocol processor's reserved main-memory window.",
    "pp_desc": "AEM descriptor image, read by the processor.",
    "pp_stage": "Saved-state private stage, written by the firmware only.",
    "pp_live": "Saved-state live window the backend reads and writes.",
    "pp_resp": "AECP response buffer, written by the processor.",
}
d["csr_banks"] = {
    "ctrl": "SoC control: reset, scratch, bus errors.",
    "ddrphy": "DDR3 PHY.",
    "identifier_mem": "SoC identifier string.",
    "milan_mac": "Milan MAC wrapper: PHY reset, MDIO, MAC counters, loopback, link status.",
    "sdram": "DDR3 controller software interface.",
    "spiflash": "QSPI flash controller.",
    "timer0": "Timer 0.",
    "uart": "UART.",
    "ppmem": "Protocol-processor memory-bridge observers, pinned to the last CSR page.",
}
soc_regs.update({
    "milan_mac_phy_crg_reset": "PHY reset of the port the image is built for (`--eth-port`): the PHY clock/reset "
                               "block's `_reset` storage, which drives the PHY reset pin. This is the PHY reset; "
                               "`PHY_RESET` (0x11C) is inert. `ETH_GUARD` does not gate it at this head.",
    "milan_mac_phy_mdio_w": "Software bit-bang MDIO write register (clock, output enable, data).",
    "milan_mac_phy_mdio_r": "Software bit-bang MDIO read register.",
    "milan_mac_core_preamble_crc": "LiteEth status, reset 1: the MAC core inserts and checks preamble and CRC.",
    "milan_mac_core_rx_datapath_preamble_errors": "LiteEth RX preamble error count.",
    "milan_mac_core_rx_datapath_crc_errors": "LiteEth RX CRC error count.",
    "milan_mac_loopback": "1 = internal MAC TX to MAC RX loopback.",
    "milan_mac_link_status": "Link, speed and duplex published by firmware; mirrored into `MAC_STATUS` (0x110). "
                             "Reset: link up, 1000 Mb/s on GMII (100 on MII), full duplex.",
})
d["soc_registers"] = soc_regs
d["cbs_classes"] = ["best effort", "control (MAAP/MSRP/MVRP, ADP/ACMP/AECP)", "gPTP",
                    "SR class B (CBS)", "SR class A (CBS)"]
d["page"]["reading_purpose"] = "Verdicts, history notes and how to read the tables."
# ---- an un-anchored section pointer that the old line break hid ------------
replace_everywhere("([`../limitations/TROUBLESHOOTING.md`](../limitations/TROUBLESHOOTING.md) Section 21)",
                   "([the troubleshooting guide's blocker section](../limitations/TROUBLESHOOTING.md#section-21-acmp-says-success-"
                   "the-listener-declares-itself-bound---and-not-one-frame-is-accepted-root-caused-and-fixed-"
                   "version-0x000f-mechanism-confirmed-on-silicon-2026-07-26))")

# ---- drop the carried feature-status table (the block is rendered from the ledger)
def drop_feature_tables(items):
    keep = []
    for item in items:
        if isinstance(item, dict) and "table" in item and item["table"][0][:2] == ["Feature ID", "Status"]:
            continue
        if isinstance(item, dict) and "rows" in item:
            item["rows"] = drop_feature_tables(item["rows"])
        keep.append(item)
    return keep


d["page"]["notes"] = drop_feature_tables(d["page"]["notes"])
replace_everywhere("<!-- milan-feature-value:gateware_version:historic --> VERSION `0x0002_0055` adds lane 4",
                   "minor `0x0055` adds lane 4")
blob = json.dumps(d, ensure_ascii=False)
assert "<!--" not in blob, blob[blob.index("<!--") - 80:blob.index("<!--") + 80]

# ---- link targets from the repository root, so the file reads the same anywhere
from pathlib import PurePosixPath


def repo_target(target: str) -> str:
    """A link target written relative to docs/reference/, as a repository path."""
    path, _, frag = target.partition("#")
    parts = []
    for part in (PurePosixPath("docs/reference") / path).parts:
        if part == "..":
            parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts) + ("#" + frag if frag else "")


def fix_links(text: str) -> str:
    return re.sub(r"\]\((?!https?:|#|/)([^)\s]+)\)", lambda m: "](" + repo_target(m.group(1)) + ")", text)


d = json.loads(fix_links(json.dumps(d, ensure_ascii=False)))
out = {"_comment": "Prose for the generated register reference (#797), keyed by RTL register and field "
                   "name. The generator refuses a key the RTL lacks. Regenerate the page after any edit.",
       "page": d["page"], "modules": d["modules"], "cbs_classes": d["cbs_classes"],
       "regions": d["regions"], "csr_banks": d["csr_banks"], "soc_registers": d["soc_registers"],
       "soc_notes": d["soc_notes"], "registers": d["registers"]}
text = json.dumps(out, indent=2, ensure_ascii=False) + "\n"
text = text.replace(" — ", " -- ").replace("—", "--")
OUT.write_text(text)
print("wrote", OUT, len(text))

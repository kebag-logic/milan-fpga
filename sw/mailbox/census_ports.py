# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_ports.py - every port of the processor wrapper cell, each in exactly one disposition class.

THE QUESTION. The split placement removes the whole KL_pp_shadow (#665), and
with it every face the datapath reads, not only the class-D outputs
publication_census.py follows. Which faces the mailbox must carry, and which
may go, is decided port by port here, from the netlist census_elab.py builds,
in every shape the builder builds (#665).

THE POPULATION is every port of the KL_pp_shadow module, as the elaborated
datapath's pp_shadow cell declares it: inputs and outputs alike, 219 at the
head this was written at. ``PORTS`` names each under one class (#665):

  C  class-D, already carried by contract 2.2's publication block and 2.4's
     source entries: exactly publication_census.CLASS_D_PORTS and the
     started level
  F  firmware-written: a setting or a status level the firmware writes into
     the face block (its carrier, a REGISTER.FIELD of contract 2.3)
  R  a request and answer window that keeps the datapath's answer logic
     unchanged (its carrier, the window's REGISTER.FIELD)
  E  an event record (its carrier, the event type, or EVENT.Wn.FIELD)
  M  a frame or event path the placement switch connects (its carrier, the
     KL_mbx port it reaches)
  G  gone with the wrapper, tied to its reset value, with its ruled reason

A row's carrier must be defined: an F or R carrier by the face block, an E
carrier by an event type, an M carrier by KL_mbx's port list. An F, R or E
carrier is as wide as its port, per source or per sink where the row says so,
in every shape, for no more streams than the contract's sources and sinks.

A G OUTPUT REACHES NOTHING THAT STAYS. Its cone is followed with
publication_census.flow() and step(), every cell and named net, and ends
only at three terminals, each named by cell and port (the ruling, item 2):

  csr       the processor-status inputs of the CSR cell ``csr`` that
            ``G_CSR`` lists, read back as a defined split value
  memory    the twenty memory-master outputs ``G_MEMORY`` lists one by one,
            the SoC's main-memory bridge
  shim      an input of the cell ``pp_maap_shim``, accepted only while each
            of its outputs reaches inputs of ``pp_shadow`` alone

and at the two exclusions below. Every other end, an input of any other
cell or port, a datapath output and a cell with no output, is the wire, and
a G output that reaches it fails.

THE EXCLUSION OWED TO THE PLACEMENT SWITCH (the ruling, item 1). The #637 map
record face (mrec_*) feeds the datapath's map writer and restore, block
amr_fsm (hdl/milan/milan_datapath.sv, its restore and hold path), which
drives the render channel map. That block goes with the wrapper: in the
split, the firmware's AECP owner applies the #637 restore (#637), so map
persistence keeps one owner. A G cone therefore stops at the nets
``REMOVED_WITH_WRAPPER`` names, and at the locals sv2v makes inside the block
(``amr_fsm.``). Each named net must be reached by a G cone of the
shape, and each must be a net of the map writer (``amr_``). ACCEPTANCE ITEM
OF THE PLACEMENT SWITCH: its split elaboration drops this exclusion, and
the census passes without it.

THE REBOOT EXCLUSION, ALSO OWED TO THE PLACEMENT SWITCH (ruling 6554243203).
The processor's AECP REBOOT request (reboot_req_o, #787) drives
KL_reboot_ctrl, which stays in the datapath and runs the drain, the egress
wait, the PHY hold and the configuration reload. In the split the
firmware's AECP owner takes REBOOT, and the split has no carrier for its
request yet (#665). A G cone therefore ends at the one cell input
``REBOOT_TERMINAL`` names, reboot_req_i of the cell reboot_ctrl, and at no
other input of that cell; a second consumer of the same net is still the
wire. ACCEPTANCE ITEM OF THE PLACEMENT SWITCH: it gives REBOOT its carrier,
drops this exclusion, and the census passes without it.

THE RULES are census_rules.py's ``port-*`` and ``g-*`` entries, each
enforced only where ``live()`` names it, each with a plant in
census_selftest.py.
"""

from __future__ import annotations

import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import mailbox_model
from census_rules import live

REPO = Path(__file__).resolve().parent.parent.parent
KL_MBX = REPO / "hdl/milan/mailbox/KL_mbx.sv"

CLASSES = ("C", "F", "R", "E", "M", "G")
#: The rules this module enforces, and no other module. Named one by one: the
#: class-D census's own port-connected and port-one-net share the prefix.
RULES = frozenset({"port-unmapped", "port-one-class", "port-stale", "port-class-d", "port-contract",
                   "port-width", "g-on-wire", "g-csr-terminal", "g-memory-terminal", "g-shim-terminal",
                   "g-exclusion-stale", "g-exclusion-amr"})
WRAPPER = "KL_pp_shadow"
WRAPPER_CELL = "pp_shadow"
CSR = "milan_csr"
CSR_CELL = "csr"
SHIM = "KL_pp_maap_shim"
SHIM_CELL = "pp_maap_shim"

#: The processor-status inputs of csr a G output may end at: the host window's
#: and the saved-state window's read-back, and the processor's frame counters.
G_CSR = frozenset({"i_pp_rdata", "i_pp_ack", "i_pp_err", "i_pp_nvm_csr_rdata", "i_pp_rx_frames",
                   "i_pp_tx_frames", "i_pp_rx_drops"})
#: The datapath outputs of the three memory masters, the SoC's main-memory bridge.
G_MEMORY = frozenset({
    "o_desc_mem_req_valid", "o_desc_mem_req_addr", "o_desc_mem_req_beats", "o_desc_mem_rsp_ready",
    "o_resp_mem_req_valid", "o_resp_mem_req_addr", "o_resp_mem_req_beats", "o_resp_mem_rsp_ready",
    "o_resp_mem_wr_valid", "o_resp_mem_wr_addr", "o_resp_mem_wr_data", "o_resp_mem_wr_strb",
    "o_nvm_mem_req_valid", "o_nvm_mem_req_addr", "o_nvm_mem_req_beats", "o_nvm_mem_rsp_ready",
    "o_nvm_mem_wr_valid", "o_nvm_mem_wr_addr", "o_nvm_mem_wr_data", "o_nvm_mem_wr_strb",
})
#: The map writer and restore's nets a G cone stops at (block amr_fsm, removed
#: with the wrapper; owed to the placement switch), and the scope of the
#: locals sv2v makes inside that block.
REMOVED_WITH_WRAPPER = (
    "amr_abort_r", "amr_bi_r", "amr_crc_nx_w", "amr_crc_r", "amr_dirty_r", "amr_e_b1_r", "amr_e_b3_r",
    "amr_e_b5_r", "amr_e_ff_r", "amr_e_z_r", "amr_ek_r", "amr_eu_r", "amr_gk_r", "amr_hcrc_r", "amr_hframe_r",
    "amr_hid_r", "amr_li_r", "amr_lo_r", "amr_malformed_r", "amr_prog_w", "amr_r_r", "amr_refuse_r",
    "amr_req_r", "amr_st_r", "amr_unused_r",
)
REMOVED_SCOPE = "amr_fsm."
#: What a map-writer net's name begins with.
REMOVED_PREFIX = "amr_"
#: The one cell input a G cone stops at for the REBOOT request (cell, module,
#: port): the split has no REBOOT carrier yet (#787, #665); owed to the
#: placement switch.
REBOOT_TERMINAL = ("reboot_ctrl", "KL_reboot_ctrl", "reboot_req_i")


@dataclass(frozen=True)
class Port:
    """How one port of the wrapper is disposed of."""

    carrier: tuple[str, ...] = ()   # REGISTER.FIELD, EVENT, EVENT.Wn.FIELD or a KL_mbx port
    per: str = ""                   # "source" or "sink": one carrier per stream; "" one in all
    why: str = ""


def _rows(why: str, names: str, per: str = "") -> dict[str, Port]:
    """Rows of one reason, no carrier: a class C or G group."""
    return {n: Port((), per, why) for n in names.split()}


_FW = "the firmware writes it in the face block (decision D1)"
_GSI = "GET_STREAM_INFO, GET_AVB_INFO and GET_AS_PATH"

#: class -> port -> its row. A port named under two classes, or under none, fails.
PORTS: dict[str, dict[str, Port]] = {
    "C": {
        **_rows("class-D: contract 2.2's publication block, publication_census.py",
                "srp_class_a_prio_o srp_class_a_vid_o srp_domain_adopted_o srp_domain_change_o srp_tk_decl_state_o "
                "srp_lstn_reg_state_o srp_active_o srp_sr_admitted_o srp_granted_slope_bps_o srp_src_fail_code_o "
                "srp_src_fail_bridge_o srp_sum_slope_bps_o srp_over_limit_o srp_tk_reg_state_o srp_lstn_decl_state_o "
                "srp_acc_latency_o srp_snk_fail_code_o acmp_declaring_o acmp_bound_o acmp_bound_eid_o "
                "acmp_bound_sid_o acmp_bound_dmac_o acmp_bound_vlan_o adp_next_avail_index_o aecp_strm_started_o"),
        **_rows("class-D: contract 2.4's source entries (SRC_SID_LO/HI, #799), publication_census.py",
                "src_stream_id_o"),
    },
    "F": {
        "aecp_cur_config_o": Port(("F_ENTITY.CUR_CONFIG",), "", _FW),
        "aecp_identify_o": Port(("F_ENTITY.IDENTIFY",), "", _FW),
        "aecp_clk_src_index_o": Port(("F_CLOCK.SOURCE_INDEX",), "", _FW),
        "aecp_pt_offset_o": Port(("F_PT_OFFSET.NS",), "source", _FW),
        "aecp_pt_offset_v_o": Port(("F_SRC_VALID.PT_OFFSET",), "source", _FW),
        "aecp_fmt_out_o": Port(("F_FMT_OUT_LO.FMT", "F_FMT_OUT_HI.FMT"), "source", _FW),
        "aecp_fmt_out_v_o": Port(("F_SRC_VALID.FMT_OUT",), "source", _FW),
        "aecp_fmt_in_o": Port(("F_FMT_IN_LO.FMT", "F_FMT_IN_HI.FMT"), "sink", _FW),
        "aecp_fmt_in_v_o": Port(("F_SNK_VALID.FMT_IN",), "sink", _FW),
        "aecp_dyn_dirty_o": Port(("F_AECP.DYN_DIRTY",), "", _FW),
        "aecp_lock_held_o": Port(("F_AECP.LOCK_HELD",), "", _FW),
        "enable_i": Port(("F_CTRL.READY",), "", "one control-ready level in place of the entity enable"),
        "restore_go_i": Port(("F_CTRL.READY",), "", "one control-ready level in place of the restore's start"),
        "restore_busy_o": Port(("F_RESTORE.BUSY",), "", _FW),
        "restore_done_o": Port(("F_RESTORE.DONE",), "", _FW),
        "restore_fail_o": Port(("F_RESTORE.FAIL",), "", _FW),
        "restore_blank_o": Port(("F_RESTORE.BLANK",), "", _FW),
        "restore_closed_o": Port(("F_RESTORE.CLOSED",), "", _FW),
        "restore_rb_o": Port(("F_RESTORE.RB",), "", _FW),
        "rs_cause_o": Port(("F_RESTORE.RS_CAUSE",), "", _FW),
        "restore_cause_o": Port(("F_RESTORE.CAUSE",), "", _FW),
        "nvm_backed_o": Port(("F_NVM.BACKED",), "", _FW),
        "nvm_alarm_o": Port(("F_NVM.ALARM",), "", _FW),
        "nvm_dirty_o": Port(("F_NVM.DIRTY",), "", _FW),
        "nvm_stale_o": Port(("F_NVM.STALE",), "", _FW),
        "nvm_pend_o": Port(("F_NVM.PEND",), "", _FW),
        "nvm_verdict_o": Port(("F_NVM.VERDICT",), "", _FW),
        "nvm_img_valid_o": Port(("F_NVM.IMG_VALID",), "", _FW),
    },
    "R": {
        "ctr_req_o": Port(("CTR_CMD.GO",), "", "GET_COUNTERS: the request"),
        "ctr_desc_type_o": Port(("CTR_REQ.TYPE",), "", "GET_COUNTERS"),
        "ctr_desc_index_o": Port(("CTR_REQ.INDEX",), "", "GET_COUNTERS"),
        "ctr_word_o": Port(("CTR_WORD.WORD",), "", "GET_COUNTERS"),
        "ctr_data_i": Port(("CTR_DATA.DATA",), "", "GET_COUNTERS: the answer"),
        "ctr_wait_i": Port(("CTR_STATUS.DONE",), "", "GET_COUNTERS: the answer's handshake"),
        "amap_req_o": Port(("AMAP_CMD.GO",), "", "GET_AUDIO_MAP: the request"),
        "amap_desc_type_o": Port(("AMAP_REQ.TYPE",), "", "GET_AUDIO_MAP"),
        "amap_desc_index_o": Port(("AMAP_REQ.INDEX",), "", "GET_AUDIO_MAP"),
        "amap_map_index_o": Port(("AMAP_PAGE.MAP_INDEX",), "", "GET_AUDIO_MAP"),
        "amap_sel_o": Port(("AMAP_PAGE.SEL",), "", "GET_AUDIO_MAP"),
        "amap_rec_o": Port(("AMAP_PAGE.REC",), "", "GET_AUDIO_MAP"),
        "amap_data_i": Port(("AMAP_DATA_LO.DATA", "AMAP_DATA_HI.DATA"), "", "GET_AUDIO_MAP: the answer"),
        "amap_wait_i": Port(("AMAP_STATUS.DONE",), "", "GET_AUDIO_MAP: the answer's handshake"),
        "amap_edit_req_o": Port(("EDIT_CMD.GO",), "", "ADD/REMOVE_AUDIO_MAPPINGS: the beat"),
        "amap_edit_phase_o": Port(("EDIT_BEAT.PHASE",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_remove_o": Port(("EDIT_BEAT.REMOVE",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_desc_type_o": Port(("EDIT_REQ.TYPE",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_desc_index_o": Port(("EDIT_REQ.INDEX",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_count_o": Port(("EDIT_BEAT.COUNT",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_rec_o": Port(("EDIT_BEAT.REC",), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_record_o": Port(("EDIT_RECORD_LO.RECORD", "EDIT_RECORD_HI.RECORD"), "",
                                   "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_value_o": Port(("EDIT_VALUE_LO.VALUE", "EDIT_VALUE_HI.VALUE"), "", "ADD/REMOVE_AUDIO_MAPPINGS"),
        "amap_edit_data_i": Port(("EDIT_DATA_LO.DATA", "EDIT_DATA_HI.DATA"), "",
                                 "ADD/REMOVE_AUDIO_MAPPINGS: the verdict"),
        "amap_edit_wait_i": Port(("EDIT_STATUS.DONE",), "", "ADD/REMOVE_AUDIO_MAPPINGS: the verdict's handshake"),
        "gsi_req_o": Port(("GSI_CMD.GO",), "", f"{_GSI}: the request"),
        "gsi_kind_o": Port(("GSI_SEL.KIND",), "", _GSI),
        "gsi_desc_type_o": Port(("GSI_REQ.TYPE",), "", _GSI),
        "gsi_desc_index_o": Port(("GSI_REQ.INDEX",), "", _GSI),
        "gsi_sel_o": Port(("GSI_SEL.SEL",), "", _GSI),
        "gsi_ord_o": Port(("GSI_SEL.ORD",), "", _GSI),
        "gsi_prop_fmt_o": Port(("GSI_PROP_LO.FMT", "GSI_PROP_HI.FMT"), "", "SET_STREAM_FORMAT's proposed format"),
        "gsi_data_i": Port(("GSI_DATA_LO.DATA", "GSI_DATA_HI.DATA"), "", f"{_GSI}: the answer"),
        "gsi_wait_i": Port(("GSI_STATUS.DONE",), "", f"{_GSI}: the answer's handshake"),
    },
    "E": {
        "ctr_change_i": Port(("COUNTERS_CHANGED",), "", "Milan v1.2 Table 5.22: a GET_COUNTERS notification"),
        "ctr_change_desc_type_i": Port(("COUNTERS_CHANGED.W1.TYPE",), "", "the changed descriptor"),
        "ctr_change_desc_index_i": Port(("COUNTERS_CHANGED.W1.INDEX",), "", "the changed descriptor"),
        "gsi_avb_chg_i": Port(("AVB_INFO_CHANGED",), "", "Milan v1.2 Table 5.22: a GET_AVB_INFO notification"),
        "gsi_asp_chg_i": Port(("AS_PATH_CHANGED",), "", "Milan v1.2 Table 5.22: a GET_AS_PATH notification"),
        "amap_live_wr_i": Port(("AMAP_LIVE_WRITE",), "", "an edit's commit beat changed the live map"),
    },
    "M": {
        "rx_tdata_i": Port(("rx_data_i",), "", "the control frames' ingress, which the switch narrows to bytes"),
        "rx_tkeep_i": Port(("rx_data_i",), "", "the final beat's bytes"),
        "rx_tvalid_i": Port(("rx_valid_i",), "", "a beat is offered"),
        "rx_tready_i": Port(("rx_valid_i",), "", "the beat is taken: a byte reaches the mailbox"),
        "rx_tlast_i": Port(("rx_last_i",), "", "the frame's last beat"),
        "m_axis_tx_tdata": Port(("tx_data_o",), "", "the control frames' egress, the switch widens the bytes"),
        "m_axis_tx_tkeep": Port(("tx_last_o",), "", "the last beat's bytes"),
        "m_axis_tx_tvalid": Port(("tx_valid_o",), "", "a beat is offered"),
        "m_axis_tx_tlast": Port(("tx_last_o",), "", "the frame's last beat"),
        "m_axis_tx_tready": Port(("tx_ready_i",), "", "the beat is taken"),
        "link_up_i": Port(("link_up_i",), "", "the LINK event"),
        "gm_change_i": Port(("gm_change_p_i",), "", "the GM event (IEEE 802.1AS-2011 clause 10)"),
        "gm_id_i": Port(("gm_id_i",), "", "the GM event's identity"),
        "gptp_domain_i": Port(("gptp_domain_i",), "", "the GM event's domain"),
    },
    "G": {
        **_rows("the wrapper's own clock and reset; axis_clk and axis_resetn keep every other consumer",
                "clk_i rst_n"),
        **_rows("tied 0: the harness lever that discards the processor's frames has no consumer in a build",
                "tx_drain_i"),
        **_rows("static identity and configuration, generated into the firmware's entity model (decision D1)",
                "entity_id_i entity_model_id_i station_mac_i talker_sources_i talker_caps_i listener_sinks_i "
                "listener_caps_i current_cfg_i identify_index_i"),
        **_rows("the firmware SRP's own source configuration and link rate, sw/firmware/ctrl/srp/srp_mbx.c "
                "(ruling 6410169666 item 3)",
                "cfg_src_en_i cfg_stream_id_i cfg_tspec_max_frame_i cfg_acc_lat_ns_i port_rate_bps_i"),
        **_rows("the descriptor image is the firmware's own (decision D1): this memory master ends at the "
                "SoC's main-memory bridge",
                "desc_mem_req_valid_o desc_mem_req_ready_i desc_mem_req_addr_o desc_mem_req_beats_o "
                "desc_mem_rsp_valid_i desc_mem_rsp_ready_o desc_mem_rsp_data_i desc_mem_rsp_last_i "
                "desc_mem_rsp_err_i"),
        **_rows("AECP responses are the firmware's own (decision D1): this memory master ends at the SoC's "
                "main-memory bridge",
                "resp_mem_req_valid_o resp_mem_req_ready_i resp_mem_req_addr_o resp_mem_req_beats_o "
                "resp_mem_rsp_valid_i resp_mem_rsp_ready_o resp_mem_rsp_data_i resp_mem_rsp_last_i "
                "resp_mem_rsp_err_i resp_mem_wr_valid_o resp_mem_wr_ready_i resp_mem_wr_addr_o resp_mem_wr_data_o "
                "resp_mem_wr_strb_o resp_mem_wr_done_i resp_mem_wr_err_i"),
        **_rows("the saved state is the firmware store's (decision D1): this memory master ends at the SoC's "
                "main-memory bridge",
                "nvm_mem_req_valid_o nvm_mem_req_ready_i nvm_mem_req_addr_o nvm_mem_req_beats_o "
                "nvm_mem_rsp_valid_i nvm_mem_rsp_ready_o nvm_mem_rsp_data_i nvm_mem_rsp_last_i nvm_mem_rsp_err_i "
                "nvm_mem_wr_valid_o nvm_mem_wr_ready_i nvm_mem_wr_addr_o nvm_mem_wr_data_o nvm_mem_wr_strb_o "
                "nvm_mem_wr_done_i nvm_mem_wr_err_i"),
        **_rows("the processor's host window (decision D1): its answer is read back at csr.i_pp_*",
                "host_req_i host_we_i host_addr_i host_wdata_i host_rdata_o host_ack_o host_err_o"),
        **_rows("the processor's saved-state control window (decision D1): its answer is read back at csr",
                "nvm_csr_sel_i nvm_csr_we_i nvm_csr_addr_i nvm_csr_wdata_i nvm_csr_rdata_o"),
        **_rows("the #637 map record face: the firmware's AECP owner applies the restore (comment 6009661573), "
                "and the map writer goes with the wrapper (ruling 6410169666 item 1, the exclusion)",
                "mrec_req_i mrec_gnt_o mrec_op_i mrec_region_i mrec_offset_i mrec_len_i mrec_wvalid_i "
                "mrec_wready_o mrec_wdata_i mrec_rvalid_o mrec_rdata_o mrec_rready_i mrec_done_o mrec_err_o "
                "mrec_abort_i amap_unflushed_i amap_alarm_i"),
        **_rows("MAAP is the firmware's (decision D1): the face ends at pp_maap_shim, the internal option at "
                "nothing",
                "maap_req_valid_o maap_req_ready_i maap_req_release_o maap_req_src_o maap_rsp_valid_i "
                "maap_rsp_ok_i maap_rsp_da_i maap_conflict_valid_i maap_conflict_src_i maap_conflict_ack_o "
                "cfg_maap_internal_i cfg_maap_count_i cfg_maap_seed_offset_i cfg_maap_seed_valid_i maap_addr_o "
                "maap_addr_valid_o maap_state_o maap_conflicts_o maap_defends_o"),
        **_rows("the processor's frame counters, superseded by the mailbox's (decision D1): read back at csr",
                "rx_frames_o tx_frames_o rx_drops_o"),
        **_rows("the processor's millisecond timebase, connected to nothing", "dbg_now_ms_o"),
        **_rows("the AECP REBOOT request (#787): the firmware's AECP owner takes REBOOT in the split, which has no "
                "carrier for it yet; the cone stops at reboot_ctrl.reboot_req_i (ruling 6554243203, the exclusion)",
                "reboot_req_o"),
    },
}

#: The class C population must be exactly publication_census.py's.
CLASS_D_NAMES = frozenset(PORTS["C"])

#: A KL_mbx port declaration: its direction and its name.
PORT_DECL = re.compile(r"^\s*(input|output)\s+(?:wire|logic)\s*(?:\[[^\]]*\])?\s*(\w+)\s*,?", re.M)


@dataclass(frozen=True)
class Carriers:
    """What a row may name: each face field's width, each event's and event field's width, KL_mbx's ports."""

    fields: dict[str, int]
    events: dict[str, int]
    mbx_ports: frozenset[str]
    sources: int
    sinks: int


@functools.lru_cache(maxsize=1)
def carriers() -> Carriers:
    """The contract's face fields and events, and the generated KL_mbx's ports."""
    c = mailbox_model.load()
    fields = {f"{r.name}.{f.name}": f.width
              for r in c.face_registers + c.face_source_registers + c.face_sink_registers for f in r.fields}
    events = {e.name: 1 for e in c.event_types}
    events |= {f"{e.name}.W{w.index}.{f.name}": f.width for e in c.event_types for w in e.words for f in w.fields}
    head = KL_MBX.read_text(encoding="utf-8").split(");", 1)[0]
    return Carriers(fields, events, frozenset(m[2] for m in PORT_DECL.finditer(head)), c.pub_sources, c.pub_sinks)


@dataclass
class PortSurvey:
    """One shape's port census: the classes' sizes, the distinct ends of the G cones by
    terminal and the removed nets they stop at, and every finding."""

    counts: dict[str, int]
    ends: dict[str, int]
    findings: list[str]


def _width(cell, port: str) -> int:
    """A port's width on the cell: the bits its connection carries, 0 when unconnected."""
    return len(cell.conns.get(port, ()))


def _shim_ok(fl, pc) -> tuple[bool, list[str]]:
    """Whether pp_maap_shim ends a G cone: each of its outputs reaches inputs of pp_shadow alone."""
    net = fl.net
    shim = net.cells.get(SHIM_CELL)
    if not live("g-shim-terminal"):
        return True, []
    if shim is None or shim.kind != SHIM:
        return False, []
    out = []
    for port, bits in sorted(shim.conns.items()):
        if shim.dirs.get(port, "inout") == "input":
            continue
        start = [b for b in bits if isinstance(b, int)]
        seen, todo, stray = set(start), deque(start), set()
        while todo:
            for e in pc.step(fl, todo.popleft()):
                if e[0] == "bit":
                    if e[1] not in seen:
                        seen.add(e[1])
                        todo.append(e[1])
                elif not (e[0] == "pin" and e[1] == WRAPPER_CELL and net.cells[WRAPPER_CELL].kind == WRAPPER):
                    stray.add(f"{e[1]}.{e[2]}" if e[0] == "pin" else
                              f"the datapath output {e[1]}" if e[0] == "out" else str(e))
        out += [f"{SHIM_CELL}'s output {port} reaches {where}, not the inputs of {WRAPPER_CELL} alone: the shim "
                f"ends no G cone" for where in sorted(stray)]
    return not out, out


def _g_end(net, e: tuple[str, ...], shim_ok: bool) -> tuple[str, str]:
    """(terminal, where) of one end of a G cone: csr, memory, shim or reboot, else the wire."""
    if e[0] == "out":
        if e[1] in G_MEMORY or not live("g-memory-terminal"):
            return "memory", e[1]
        return "wire", f"the datapath output {e[1]}"
    cell, port = e[1], e[2]
    kind = net.cells[cell].kind
    if kind == CSR and cell == CSR_CELL and (port in G_CSR or not live("g-csr-terminal")):
        return "csr", port
    if kind == SHIM and cell == SHIM_CELL and shim_ok:
        return "shim", port
    if (cell, kind, port) == REBOOT_TERMINAL:
        return "reboot", port
    if kind.startswith("$"):
        return "wire", f"{cell}.{port} ({kind}, which has no output)"
    return "wire", f"{cell}.{port}"


def _removed(name: str, excluded: tuple[str, ...]) -> bool:
    """Whether a net is one the exclusion names: a listed net, or a local sv2v made inside the block."""
    return bool(name) and (name in excluded or name.startswith(REMOVED_SCOPE))


def survey_ports(fl: Any, pc: ModuleType, table: dict[str, dict[str, Port]] | None = None,
                 excluded: tuple[str, ...] | None = None, shape: str = "recipe") -> PortSurvey:
    """Every port of the pp_shadow cell classified against table, and every G output's cone followed."""
    table = PORTS if table is None else table
    excluded = REMOVED_WITH_WRAPPER if excluded is None else excluded
    net = fl.net
    dirs = net.modules.get(WRAPPER, {})
    cell = net.cells[WRAPPER_CELL]
    out: list[str] = []
    named: dict[str, list[str]] = defaultdict(list)
    for cls in CLASSES:
        for port in table.get(cls, {}):
            named[port].append(cls)
    out += [f"unmapped port: {p} ({dirs[p]}) of {WRAPPER_CELL} is in no class; name its disposition"
            for p in sorted(dirs) if not named[p] and live("port-unmapped")]
    out += [f"port {p} is named in classes {' and '.join(sorted(named[p]))}: one port, one class"
            for p in sorted(named) if len(named[p]) > 1 and live("port-one-class")]
    out += [f"stale port row: class {cls} names {p}, which {WRAPPER} does not declare"
            for cls in CLASSES for p in sorted(table.get(cls, {})) if p not in dirs and live("port-stale")]
    have_c = set(table.get("C", {}))
    if live("port-class-d"):
        out += [f"class C names {p}, which is not the class-D census's population" for p in sorted(have_c - CLASS_D)]
        out += [f"class C lacks {p}, which the class-D census holds" for p in sorted(CLASS_D - have_c)]
    known = carriers()
    n_out, n_in = _width(cell, "acmp_declaring_o"), _width(cell, "aecp_strm_started_o")
    for cls in ("F", "R", "E", "M"):
        for port, row in sorted(table.get(cls, {}).items()):
            if port not in dirs:
                continue
            pool = known.mbx_ports if cls == "M" else known.events if cls == "E" else known.fields
            bad = [c for c in row.carrier if c not in pool]
            what = "a port of KL_mbx" if cls == "M" else "defined by contract 2.3"
            if (bad or not row.carrier) and live("port-contract"):
                out.append(f"{cls} port {port}: its carrier {', '.join(bad) or '(none)'} is not {what}")
                continue
            if cls == "M" or bad:
                continue
            n = {"source": n_out, "sink": n_in}.get(row.per, 1)
            limit = {"source": known.sources, "sink": known.sinks}.get(row.per, 1)
            want = sum(pool[c] for c in row.carrier) * n
            if (_width(cell, port) != want or n > limit) and live("port-width"):
                out.append(f"{cls} port {port} is {_width(cell, port)} bits in the shape {shape}; its carrier "
                           f"{' + '.join(row.carrier)} holds {want} for {n} {row.per or 'value'}(s), of at most "
                           f"{limit}")
    shim_ok, shim_findings = _shim_ok(fl, pc)
    out += shim_findings
    ends: set[tuple[str, str]] = set()
    reached: set[str] = set()
    for port in sorted(p for p in table.get("G", {}) if dirs.get(p) == "output"):
        start = [b for b in cell.conns.get(port, ()) if isinstance(b, int)]
        seen, todo, wires = set(start), deque(start), set()
        while todo:
            for e in pc.step(fl, todo.popleft()):
                if e[0] == "bit":
                    if e[1] in seen:
                        continue
                    seen.add(e[1])
                    name = pc.named(net, e[1])
                    if _removed(name, excluded):
                        reached.add(name)
                        continue
                    todo.append(e[1])
                    continue
                kind, where = _g_end(net, e, shim_ok)
                ends.add((kind, where))
                if kind == "wire":
                    wires.add(where)
        out += [f"G port {port} reaches the wire at {w}: a value the split placement removes still has a consumer"
                for w in sorted(wires) if live("g-on-wire")]
    out += [f"the exclusion names {n}, which no G cone of this shape reaches: drop it" for n in excluded
            if n not in reached and live("g-exclusion-stale")]
    out += [f"the exclusion names {n}, which is not a net of the map writer and restore ({REMOVED_PREFIX}*)"
            for n in excluded if not n.startswith(REMOVED_PREFIX) and live("g-exclusion-amr")]
    counts = {cls: sum(1 for p in table.get(cls, {}) if p in dirs) for cls in CLASSES}
    counts["ports"] = len(dirs)
    tally = {k: sum(1 for kind, _ in ends if kind == k) for k in ("csr", "memory", "shim", "reboot", "wire")}
    tally["removed"] = len(reached)
    return PortSurvey(counts, tally, out)


#: The class-D census's population, as publication_census.py states it; bound by that module at import.
CLASS_D: frozenset[str] = frozenset()

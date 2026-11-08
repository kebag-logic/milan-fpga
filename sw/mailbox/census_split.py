# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""census_split.py - the census's second population: the split datapath's control face, each port consumed.

THE QUESTION. In the split placement (``CTRL_SPLIT_P = 1``, #665) the datapath
builds no KL_pp_shadow. Each face the wrapper served comes from the
datapath's own ``i_ctl_*`` and ``o_ctl_*`` ports, which KL_mbx_cdc carries to
the mailbox. census_ports.py rules, port by port, which faces the mailbox
must carry. This module checks that the split datapath consumes every one of
them: each publication field (contracts 2.2 and 2.4) and each contract 2.3
field reaches the same consumers the wrapper's port fed (ruling 6715535566,
item 2).

THE NETLISTS. Each shape is elaborated twice by census_elab.py, at its own
parameters and again with ``CTRL_SPLIT_P = 1``. The all-fabric netlist is the
reference. Its pp_shadow cell names, for each wrapper port, the nets that port
drove or read. The split netlist must hold those nets, now reached from the
ports this table names.

THE POPULATION is every port of the split datapath whose name begins
``i_ctl_`` or ``o_ctl_``. ``SPLIT_PORTS`` names each under one class, the
class of the wrapper ports it stands in for:

  C  a publication field: its carrier a REGISTER.FIELD of the block
  F  a face setting or status (contract 2.3)
  R  a window's request or answer (contract 2.3)
  E  a face event (contract 2.3's event types)
  M  a frame or event path: its carrier a port of KL_mbx

Each row names what it stands for: wrapper ports of census_ports.PORTS in
its class, or a port of the frame block KL_ctrl_split.

THE RULES are census_rules.py's ``split-*`` entries, each enforced only where
``live()`` names it, each with an arm in census_selftest.py:

  split-placement    the split netlist holds no KL_pp_shadow, KL_maap or
                     KL_pp_maap_shim cell, none of the map writer's nets the
                     all-fabric exclusion names, and one KL_ctrl_split cell;
                     so the split census needs neither exclusion
  split-unmapped     every ctl port is named by a row
  split-one-class    no port is named twice
  split-stale        no row names a port the datapath does not declare
  split-contract     a row's carrier is defined; so is each ruled non-port
                     field of ``NOT_PORTS``
  split-width        a port is as wide as its carrier, CTRL_ENTRIES_P
                     entries of it where the carrier is per source or sink
  split-every-field  every publication field and every face field and event
                     of contract 2.3 is a row's carrier or ruled non-port
  split-face         each row stands for wrapper ports of its own class and
                     carrier, and every C, F, R, E or M wrapper port is stood
                     for, or ruled (``UNCARRIED``, ``TIED_C``)
  split-drives       the net a wrapper output drove is driven, in the split,
                     by exactly the ports standing for it, bit for bit where
                     one port alone drives it; a ctl output is driven by the
                     net the wrapper input it stands for read
  split-tied         a G output's net, and a class-D net the block does not
                     carry, is a constant in the split; or, as ruled, the
                     host window's acknowledgement follows its request
  split-frame-block  KL_ctrl_split takes the wrapper's frame ports and frame
                     counters net for net, and the M rows reach its ports
  split-field-reads  each field row of publication_census.CENSUS is read the
                     same way in the split, and reaches the wire
  split-consumed     every bit of an input row, for the shape's own sources
                     and sinks, reaches a cone end
  split-beyond       no bit of an entry past the shape's own is read

THE REBOOT HOLD (ruling 6715535566 item 3). The split carries no REBOOT
request: reboot_req_o's net, pp_reboot_req_w, is a constant 0 there, so
KL_reboot_ctrl's reboot_req_i never rises (split-tied holds it). The carrier
is S11's.
"""

from __future__ import annotations

import functools
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import census_ports
from census_rules import live

#: The parameter that selects the split, and the one that sizes its per-entry ports.
SPLIT_PARAM = "CTRL_SPLIT_P"
CTL = re.compile(r"^[io]_ctl_")
CTRL_SPLIT = "KL_ctrl_split"
#: The modules the split must not build.
GONE = (census_ports.WRAPPER, "KL_maap", census_ports.SHIM)
CLASSES = ("C", "F", "R", "E", "M")
#: A name sv2v makes for a temporary, which a source walk reads through.
SV2V_TMP = re.compile(r"(^|\.)sv2v_tmp_")


@dataclass(frozen=True)
class Face:
    """One ctl port: its carrier, per source or per sink, and what it stands for."""

    carrier: tuple[str, ...]
    per: str = ""                         # "source", "sink", or "" for one value
    stands: tuple[Any, ...] = ()          # wrapper ports, or (KL_ctrl_split, port) pairs
    why: str = ""


def _cs(port: str) -> tuple[str, str]:
    """A KL_ctrl_split port a row stands for."""
    return (CTRL_SPLIT, port)


#: class -> ctl port -> its row. A packed row's stands are in its carrier's
#: order, least significant first.
SPLIT_PORTS: dict[str, dict[str, Face]] = {
    "C": {
        "i_ctl_pub_da_gate": Face(("DA_GATE.OPEN",), "source", ("acmp_declaring_o",)),
        "i_ctl_pub_licence": Face(("LICENCE.ACTIVE",), "source", ("srp_active_o", "srp_sr_admitted_o")),
        "i_ctl_pub_talker_decl": Face(("TALKER_DECL.DECLARED",), "source", ("srp_tk_decl_state_o",)),
        "i_ctl_pub_src_sid": Face(("SRC_SID_LO.SID", "SRC_SID_HI.SID"), "source", ("src_stream_id_o",)),
        "i_ctl_pub_idle_slope_bps": Face(("IDLE_SLOPE.BPS",), "", ("srp_sum_slope_bps_o",)),
        "i_ctl_pub_dom_vid": Face(("SR_DOMAIN.VID",), "", ("srp_class_a_vid_o",)),
        "i_ctl_pub_dom_prio": Face(("SR_DOMAIN.PRIORITY",), "", ("srp_class_a_prio_o",)),
        "i_ctl_pub_dom_adopted": Face(("SR_DOMAIN.ADOPTED",), "", ("srp_domain_adopted_o",)),
        "i_ctl_pub_bound": Face(("BINDING.BOUND",), "sink", ("acmp_bound_o",)),
        "i_ctl_pub_sid_valid": Face(("BINDING.SID_VALID",), "sink", ("acmp_bound_sid_o",),
                                    "the stream_id is taken only while SID_VALID is set"),
        "i_ctl_pub_started": Face(("BINDING.STARTED",), "sink", ("aecp_strm_started_o",)),
        "i_ctl_pub_sid": Face(("SID_LO.SID", "SID_HI.SID"), "sink", ("acmp_bound_sid_o",)),
    },
    "F": {
        "i_ctl_cur_config": Face(("F_ENTITY.CUR_CONFIG",), "", ("aecp_cur_config_o",)),
        "i_ctl_identify": Face(("F_ENTITY.IDENTIFY",), "", ("aecp_identify_o",)),
        "i_ctl_clk_src_index": Face(("F_CLOCK.SOURCE_INDEX",), "", ("aecp_clk_src_index_o",)),
        "i_ctl_lock_held": Face(("F_AECP.LOCK_HELD",), "", ("aecp_lock_held_o",)),
        "i_ctl_dyn_dirty": Face(("F_AECP.DYN_DIRTY",), "", ("aecp_dyn_dirty_o",)),
        "i_ctl_pt_offset_ns": Face(("F_PT_OFFSET.NS",), "source", ("aecp_pt_offset_o",)),
        "i_ctl_pt_offset_v": Face(("F_SRC_VALID.PT_OFFSET",), "source", ("aecp_pt_offset_v_o",)),
        "i_ctl_fmt_out": Face(("F_FMT_OUT_LO.FMT", "F_FMT_OUT_HI.FMT"), "source", ("aecp_fmt_out_o",)),
        "i_ctl_fmt_out_v": Face(("F_SRC_VALID.FMT_OUT",), "source", ("aecp_fmt_out_v_o",)),
        "i_ctl_fmt_in": Face(("F_FMT_IN_LO.FMT", "F_FMT_IN_HI.FMT"), "sink", ("aecp_fmt_in_o",)),
        "i_ctl_fmt_in_v": Face(("F_SNK_VALID.FMT_IN",), "sink", ("aecp_fmt_in_v_o",)),
        "i_ctl_restore": Face(("F_RESTORE.BUSY", "F_RESTORE.DONE", "F_RESTORE.FAIL", "F_RESTORE.BLANK",
                               "F_RESTORE.CLOSED", "F_RESTORE.RB"), "",
                              ("restore_busy_o", "restore_done_o", "restore_fail_o", "restore_blank_o",
                               "restore_closed_o", "restore_rb_o")),
        "i_ctl_rs_cause": Face(("F_RESTORE.RS_CAUSE",), "", ("rs_cause_o",)),
        "i_ctl_restore_cause": Face(("F_RESTORE.CAUSE",), "", ("restore_cause_o",)),
        "i_ctl_nvm": Face(("F_NVM.BACKED", "F_NVM.ALARM", "F_NVM.DIRTY", "F_NVM.STALE", "F_NVM.PEND",
                           "F_NVM.IMG_VALID"), "",
                          ("nvm_backed_o", "nvm_alarm_o", "nvm_dirty_o", "nvm_stale_o", "nvm_pend_o",
                           "nvm_img_valid_o")),
        "i_ctl_nvm_verdict": Face(("F_NVM.VERDICT",), "", ("nvm_verdict_o",)),
    },
    "R": {
        "i_ctl_ctr_req": Face(("CTR_CMD.GO",), "", ("ctr_req_o",)),
        "i_ctl_ctr_type": Face(("CTR_REQ.TYPE",), "", ("ctr_desc_type_o",)),
        "i_ctl_ctr_index": Face(("CTR_REQ.INDEX",), "", ("ctr_desc_index_o",)),
        "i_ctl_ctr_word": Face(("CTR_WORD.WORD",), "", ("ctr_word_o",)),
        "o_ctl_ctr_data": Face(("CTR_DATA.DATA",), "", ("ctr_data_i",)),
        "o_ctl_ctr_wait": Face(("CTR_STATUS.DONE",), "", ("ctr_wait_i",)),
        "i_ctl_amap_req": Face(("AMAP_CMD.GO",), "", ("amap_req_o",)),
        "i_ctl_amap_type": Face(("AMAP_REQ.TYPE",), "", ("amap_desc_type_o",)),
        "i_ctl_amap_index": Face(("AMAP_REQ.INDEX",), "", ("amap_desc_index_o",)),
        "i_ctl_amap_map_index": Face(("AMAP_PAGE.MAP_INDEX",), "", ("amap_map_index_o",)),
        "i_ctl_amap_sel": Face(("AMAP_PAGE.SEL",), "", ("amap_sel_o",)),
        "i_ctl_amap_rec": Face(("AMAP_PAGE.REC",), "", ("amap_rec_o",)),
        "o_ctl_amap_data": Face(("AMAP_DATA_LO.DATA", "AMAP_DATA_HI.DATA"), "", ("amap_data_i",)),
        "o_ctl_amap_wait": Face(("AMAP_STATUS.DONE",), "", ("amap_wait_i",)),
        "i_ctl_edit_req": Face(("EDIT_CMD.GO",), "", ("amap_edit_req_o",)),
        "i_ctl_edit_phase": Face(("EDIT_BEAT.PHASE",), "", ("amap_edit_phase_o",)),
        "i_ctl_edit_remove": Face(("EDIT_BEAT.REMOVE",), "", ("amap_edit_remove_o",)),
        "i_ctl_edit_type": Face(("EDIT_REQ.TYPE",), "", ("amap_edit_desc_type_o",)),
        "i_ctl_edit_index": Face(("EDIT_REQ.INDEX",), "", ("amap_edit_desc_index_o",)),
        "i_ctl_edit_count": Face(("EDIT_BEAT.COUNT",), "", ("amap_edit_count_o",)),
        "i_ctl_edit_rec": Face(("EDIT_BEAT.REC",), "", ("amap_edit_rec_o",)),
        "i_ctl_edit_record": Face(("EDIT_RECORD_LO.RECORD", "EDIT_RECORD_HI.RECORD"), "", ("amap_edit_record_o",)),
        "i_ctl_edit_value": Face(("EDIT_VALUE_LO.VALUE", "EDIT_VALUE_HI.VALUE"), "", ("amap_edit_value_o",)),
        "o_ctl_edit_data": Face(("EDIT_DATA_LO.DATA", "EDIT_DATA_HI.DATA"), "", ("amap_edit_data_i",)),
        "o_ctl_edit_wait": Face(("EDIT_STATUS.DONE",), "", ("amap_edit_wait_i",)),
        "i_ctl_gsi_req": Face(("GSI_CMD.GO",), "", ("gsi_req_o",)),
        "i_ctl_gsi_kind": Face(("GSI_SEL.KIND",), "", ("gsi_kind_o",)),
        "i_ctl_gsi_type": Face(("GSI_REQ.TYPE",), "", ("gsi_desc_type_o",)),
        "i_ctl_gsi_index": Face(("GSI_REQ.INDEX",), "", ("gsi_desc_index_o",)),
        "i_ctl_gsi_sel": Face(("GSI_SEL.SEL",), "", ("gsi_sel_o",)),
        "i_ctl_gsi_ord": Face(("GSI_SEL.ORD",), "", ("gsi_ord_o",)),
        "i_ctl_gsi_prop": Face(("GSI_PROP_LO.FMT", "GSI_PROP_HI.FMT"), "", ("gsi_prop_fmt_o",)),
        "o_ctl_gsi_data": Face(("GSI_DATA_LO.DATA", "GSI_DATA_HI.DATA"), "", ("gsi_data_i",)),
        "o_ctl_gsi_wait": Face(("GSI_STATUS.DONE",), "", ("gsi_wait_i",)),
    },
    "E": {
        "o_ctl_ctr_chg_valid": Face(("COUNTERS_CHANGED",), "", ("ctr_change_i",)),
        "o_ctl_ctr_chg_type": Face(("COUNTERS_CHANGED.W1.TYPE",), "", ("ctr_change_desc_type_i",)),
        "o_ctl_ctr_chg_index": Face(("COUNTERS_CHANGED.W1.INDEX",), "", ("ctr_change_desc_index_i",)),
        "o_ctl_avb_chg_p": Face(("AVB_INFO_CHANGED",), "", ("gsi_avb_chg_i",)),
        "o_ctl_asp_chg_p": Face(("AS_PATH_CHANGED",), "", ("gsi_asp_chg_i",)),
        "o_ctl_amap_wr_p": Face(("AMAP_LIVE_WRITE",), "", ("amap_live_wr_i",)),
    },
    "M": {
        "o_ctl_rx_valid": Face(("rx_valid_i",), "", (_cs("rx_valid_o"),)),
        "o_ctl_rx_data": Face(("rx_data_i",), "", (_cs("rx_data_o"),)),
        "o_ctl_rx_last": Face(("rx_last_i",), "", (_cs("rx_last_o"),)),
        "i_ctl_rx_ready": Face(("rx_ready_o",), "", (_cs("rx_ready_i"),)),
        "i_ctl_tx_valid": Face(("tx_valid_o",), "", (_cs("tx_valid_i"),)),
        "i_ctl_tx_data": Face(("tx_data_o",), "", (_cs("tx_data_i"),)),
        "i_ctl_tx_last": Face(("tx_last_o",), "", (_cs("tx_last_i"),)),
        "o_ctl_tx_ready": Face(("tx_ready_i",), "", (_cs("tx_ready_o"),)),
        "o_ctl_link_up": Face(("link_up_i",), "", ("link_up_i",)),
        "o_ctl_gm_change_p": Face(("gm_change_p_i",), "", ("gm_change_i",)),
        "o_ctl_gm_id": Face(("gm_id_i",), "", ("gm_id_i",)),
        "o_ctl_gptp_domain": Face(("gptp_domain_i",), "", ("gptp_domain_i",)),
    },
}

#: The contract 2.3 fields no datapath port carries, each with its ruling.
NOT_PORTS = {
    "F_CTRL.READY": "the processor's enable and restore start, which no fabric block reads: the firmware opens "
                    "AECP on it itself",
    "F_COMMIT.GO": "the commit handshake KL_mbx_cdc's settings crossing takes, not a datapath value",
    "F_STATUS.BUSY": "the commit handshake KL_mbx_cdc's settings crossing takes, not a datapath value",
    **{f"{w}_STATUS.{f}": "the window's own state in KL_mbx (open, timed out, its tag); KL_mbx_cdc_window "
                          "carries the request and answer"
       for w in ("CTR", "AMAP", "EDIT", "GSI") for f in ("BUSY", "TIMEOUT", "TAG")},
}
#: The face events no datapath port carries: the mailbox makes them, or a datapath M row feeds them.
NOT_PORT_EVENTS = {
    "TIMER": "KL_mbx's own timers", "TICK": "KL_mbx's own tick",
    "LINK": "made by KL_mbx from its link_up_i (the M row o_ctl_link_up)",
    "GM": "made by KL_mbx from its gm_* inputs (the M rows o_ctl_gm_*)",
}

#: The wrapper ports of a carried class that no split port stands for, each ruled.
UNCARRIED = {
    "enable_i": "F_CTRL.READY, which no datapath port carries (NOT_PORTS)",
    "restore_go_i": "F_CTRL.READY, which no datapath port carries (NOT_PORTS)",
}
#: The class-D values the block does not carry: each read only by CSR status
#: or the GET_STREAM_INFO answer the firmware composes from its own state, so
#: in the split each net is a constant (publication_census.CENSUS rows).
TIED_C = ("srp_domain_change_o", "srp_lstn_reg_state_o", "srp_granted_slope_bps_o", "srp_src_fail_code_o",
          "srp_src_fail_bridge_o", "srp_over_limit_o", "srp_tk_reg_state_o", "srp_lstn_decl_state_o",
          "srp_acc_latency_o", "srp_snk_fail_code_o", "acmp_bound_eid_o", "acmp_bound_dmac_o",
          "acmp_bound_vlan_o", "adp_next_avail_index_o")
#: The G outputs whose net the split drives other than with a constant, each with its source.
G_DRIVEN = {
    "host_ack_o": ("pp_req_w", "the host window answers every access at once, refused, so the CSR is never "
                               "left busy"),
}
#: The wrapper ports KL_ctrl_split takes over, by its port of the same name.
FRAME_PORTS = ("rx_tdata_i", "rx_tkeep_i", "rx_tvalid_i", "rx_tready_i", "rx_tlast_i", "m_axis_tx_tdata",
               "m_axis_tx_tkeep", "m_axis_tx_tvalid", "m_axis_tx_tlast", "m_axis_tx_tready", "rx_frames_o",
               "rx_drops_o", "tx_frames_o")


#: The split ports no datapath block reads, in either placement: each stands for a wrapper output whose net
#: the all-fabric datapath reads nowhere either, which split-consumed proves in every shape.
UNREAD_BOTH = {
    "i_ctl_cur_config": "F_ENTITY.CUR_CONFIG: no datapath block reads the current configuration",
    "i_ctl_identify": "F_ENTITY.IDENTIFY: no root consumer drives the identify indication",
    "i_ctl_dyn_dirty": "F_AECP.DYN_DIRTY: no datapath block reads it",
    "i_ctl_edit_value": "EDIT_VALUE_LO/HI.VALUE: the map edit's datapath logic reads the record, not the value",
}


def split_shape(shape: Any) -> Any:
    """shape at CTRL_SPLIT_P = 1, named so its netlist is kept apart from the all-fabric one."""
    from census_elab import Shape
    return Shape(f"{shape.name}+split", shape.header, tuple(sorted({**dict(shape.params), SPLIT_PARAM: 1}.items())))


@dataclass
class SplitSurvey:
    """One shape's split census: each class's size, the live bits consumed, and every finding."""

    counts: dict[str, int]
    findings: list[str]


class Back:
    """Where a split bit's value comes from: through Yosys cells to the first named net, a cell or a constant."""

    def __init__(self, fl: Any, pc: ModuleType) -> None:
        self.fl, self.pc, self.net = fl, pc, fl.net
        self.ins: dict[str, list] = {}
        mem: dict[str, list] = defaultdict(list)
        for name, c in self.net.cells.items():
            bits = [b for p, bs in c.conns.items() if c.dirs.get(p, "inout") != "output" for b in bs]
            self.ins[name] = bits
            if c.memid:
                mem[c.memid] += bits
        self.mem = mem

    def sources(self, bit: Any) -> set[tuple]:
        """("net", name, index), ("cell", cell, port) or ("const",) for each source of one bit."""
        if not isinstance(bit, int):
            return {("const",)}
        out: set[tuple] = set()
        seen, todo = {bit}, deque([bit])
        while todo:
            b = todo.popleft()
            for cell, port in self.fl.drivers.get(b, ()):
                if not cell:
                    out.add(("net", port, self.net.bit_name[b][1]))
                    continue
                c = self.net.cells[cell]
                if not c.kind.startswith("$"):
                    out.add(("cell", cell, port))
                    continue
                for i in self.ins[cell] + (self.mem[c.memid] if c.memid else []):
                    if not isinstance(i, int):
                        out.add(("const",))
                    elif i not in seen:
                        seen.add(i)
                        name = self.pc.named(self.net, i)
                        if name and not SV2V_TMP.search(name):
                            out.add(("net", name, self.net.bit_name[i][1]))
                        else:
                            todo.append(i)
        return out

    def closure(self, bits: Any) -> set[str]:
        """Every datapath input and instance output a value comes from, through every cell and named net;
        empty for a constant."""
        out: set[str] = set()
        start = [b for b in bits if isinstance(b, int)]
        seen, todo = set(start), deque(start)
        while todo:
            b = todo.popleft()
            for cell, port in self.fl.drivers.get(b, ()):
                if not cell:
                    out.add(port)
                    continue
                c = self.net.cells[cell]
                if not c.kind.startswith("$"):
                    out.add(f"{cell}.{port}")
                    continue
                for i in self.ins[cell] + (self.mem[c.memid] if c.memid else []):
                    if isinstance(i, int) and i not in seen:
                        seen.add(i)
                        todo.append(i)
        return out


def _live(fl: Any, pc: ModuleType) -> set[int]:
    """Every bit of the netlist from which some cone end is reachable, walked back from the ends along each
    cell's drivers: a Yosys cell's output makes every input of it live, a memory read every write of its
    memory too, as publication_census.step() leads forward."""
    net = fl.net
    writers: dict[str, list[str]] = defaultdict(list)
    for name, c in net.cells.items():
        if c.memid and c.kind.startswith(pc.MEM_WRITES):
            writers[c.memid].append(name)
    live_bits: set[int] = set()
    for b, ends in fl.fanout.items():
        if any(e[0] in ("pin", "out") and pc.terminal(net, e) is not None for e in ends):
            live_bits.add(b)
    todo = deque(live_bits)
    done: set[str] = set()
    while todo:
        for cell, _port in fl.drivers.get(todo.popleft(), ()):
            if not cell or cell in done or not net.cells[cell].kind.startswith("$"):
                continue
            done.add(cell)
            c = net.cells[cell]
            feeding = [cell, *(writers.get(c.memid, ()) if c.memid else ())]
            for f in feeding:
                fc = net.cells[f]
                for port, bits in fc.conns.items():
                    if fc.dirs.get(port, "inout") == "output":
                        continue
                    for i in bits:
                        if isinstance(i, int) and i not in live_bits:
                            live_bits.add(i)
                            todo.append(i)
    return live_bits


def _table_findings(table: dict[str, dict[str, Face]], ports: dict, contract: Any) -> list[str]:
    """The rows against the datapath's ctl ports and the contract."""
    out: list[str] = []
    named: dict[str, list[str]] = defaultdict(list)
    for cls in CLASSES:
        for port in table.get(cls, {}):
            named[port].append(cls)
    ctl = sorted(p for p in ports if CTL.match(p))
    out += [f"unmapped split port: {p} ({ports[p][0]}) is in no class; name what it carries and stands for"
            for p in ctl if not named[p] and live("split-unmapped")]
    out += [f"split port {p} is named in classes {' and '.join(sorted(named[p]))}: one port, one class"
            for p in sorted(named) if len(named[p]) > 1 and live("split-one-class")]
    out += [f"stale split row: class {cls} names {p}, which the split datapath does not declare"
            for cls in CLASSES for p in sorted(table.get(cls, {})) if p not in ports and live("split-stale")]
    fields, events, mbx = contract.fields, contract.events, contract.mbx_ports
    pub = contract.pub
    for cls in CLASSES:
        for port, row in sorted(table.get(cls, {}).items()):
            pool = mbx if cls == "M" else events if cls == "E" else pub if cls == "C" else fields
            bad = [c for c in row.carrier if c not in pool]
            if (bad or not row.carrier) and live("split-contract"):
                what = {"M": "a port of KL_mbx", "E": "an event of contract 2.3", "C": "a field of the "
                        "publication block"}.get(cls, "a field of contract 2.3's face block")
                out.append(f"split {cls} port {port}: its carrier {', '.join(bad) or '(none)'} is not {what}")
                continue
            if cls == "M" or port not in ports:
                continue
            per_entry = any(c in contract.per_entry for c in row.carrier)
            want = sum(pool[c] for c in row.carrier) * (contract.entries if per_entry else 1)
            have = len(ports[port][1])
            if have != want and live("split-width"):
                out.append(f"split {cls} port {port} is {have} bits; its carrier {' + '.join(row.carrier)} holds "
                           f"{want}" + (f" for {contract.entries} entries" if per_entry else ""))
    out += [f"the ruled non-port field {f} is not a field of contract 2.3's face block"
            for f in sorted(NOT_PORTS) if f not in fields and live("split-contract")]
    if live("split-every-field"):
        carried = {c for cls in CLASSES for row in table.get(cls, {}).values() for c in row.carrier}
        out += [f"the publication field {f} is carried by no port of the split datapath"
                for f in sorted(pub) if f not in carried]
        out += [f"the face field {f} is carried by no port of the split datapath, and is not ruled a non-port field"
                for f in sorted(fields) if f not in carried and f not in NOT_PORTS]
        out += [f"the face event {e} is carried by no port of the split datapath"
                for e in sorted(contract.event_types) if e not in carried and e not in NOT_PORT_EVENTS]
    return out


def _face_findings(table: dict[str, dict[str, Face]]) -> list[str]:
    """Each row's stands against census_ports.PORTS, and each wrapper port stood for or ruled."""
    out: list[str] = []
    wrapper = {p: (cls, row) for cls, rows in census_ports.PORTS.items() for p, row in rows.items()}
    stood: set[str] = set()
    for cls in CLASSES:
        for port, row in sorted(table.get(cls, {}).items()):
            for s in row.stands:
                if isinstance(s, tuple):
                    if s[0] != CTRL_SPLIT or cls != "M":
                        out.append(f"split port {port} stands for {s[0]}.{s[1]}: only an M row stands for a port "
                                   f"of {CTRL_SPLIT}")
                    continue
                stood.add(s)
                if s not in wrapper:
                    out.append(f"split port {port} stands for {s}, which census_ports.PORTS does not name")
                    continue
                wcls, wrow = wrapper[s]
                if wcls != cls:
                    out.append(f"split {cls} port {port} stands for {s}, a class {wcls} port of the wrapper")
                elif cls != "C" and not set(wrow.carrier) <= set(row.carrier):
                    out.append(f"split port {port} stands for {s}, whose carrier {', '.join(wrow.carrier)} is not "
                               f"its own, {', '.join(row.carrier)}")
    for p, (cls, _row) in sorted(wrapper.items()):
        if cls in CLASSES and p not in stood and p not in UNCARRIED and p not in TIED_C and p not in FRAME_PORTS:
            out.append(f"the wrapper's class {cls} port {p} is stood for by no port of the split datapath, and is "
                       f"not ruled")
    return out if live("split-face") else []


@dataclass(frozen=True)
class AfFace:
    """What the split census reads from the all-fabric netlist of a shape, so neither worker holds both."""

    bits: dict[str, tuple]          # wrapper port -> its bits, each (net, index) or a constant
    dirs: dict[str, str]            # wrapper port -> input or output
    read: frozenset[str]            # the UNREAD_BOTH rows' wrapper ports whose net reaches a cone end
    reads: frozenset[tuple[str, str]]   # the class-D reads (wire, consumer)
    n_src: int
    n_snk: int


def af_face(af_fl: Any, pc: ModuleType, reads: list) -> AfFace | None:
    """The all-fabric face of one shape: each wrapper port's nets, and which of them the datapath reads."""
    af = af_fl.net
    cell = af.cells.get(census_ports.WRAPPER_CELL)
    if cell is None:
        return None
    bits = {p: tuple(af.bit_name[b] if isinstance(b, int) else b for b in bs) for p, bs in cell.conns.items()}
    wanted = {s for cls in CLASSES for port, row in SPLIT_PORTS.get(cls, {}).items() if port in UNREAD_BOTH
              for s in row.stands if isinstance(s, str)}
    read = frozenset(s for s in wanted if pc.cone(af_fl, {b for b in cell.conns.get(s, ()) if isinstance(b, int)}))
    return AfFace(bits, dict(af.modules.get(census_ports.WRAPPER, {})), read,
                  frozenset((r.wire, r.consumer) for r in reads), len(cell.conns.get("acmp_declaring_o", ())),
                  len(cell.conns.get("aecp_strm_started_o", ())))


def _split_bits(net: Any, named: tuple) -> list:
    """The split netlist's bits of the all-fabric (name, index) list; None where the split lacks the net."""
    out = []
    for x in named:
        if not isinstance(x, tuple):
            out.append(x)
        elif x[0] in net.names and x[1] < len(net.names[x[0]]):
            out.append(net.names[x[0]][x[1]])
        else:
            out.append(None)
    return out


@dataclass(frozen=True)
class _Ctx:
    """One shape's split census in progress: the split netlist's flow and sources, the all-fabric face, the
    rows the datapath declares, the contract and the frame block's cell."""

    fl: Any
    pc: ModuleType
    back: Back
    face: AfFace
    rows: dict[str, tuple[str, Face]]
    contract: Contract
    frames: list[str]

    @property
    def net(self) -> Any:
        """The split netlist."""
        return self.fl.net


def survey_split(fl: Any, pc: ModuleType, face: AfFace | None, shape: str,
                 table: dict[str, dict[str, Face]] | None = None) -> SplitSurvey:
    """The split census of one shape: fl is the split netlist's flow, face the all-fabric face of the shape."""
    table = SPLIT_PORTS if table is None else table
    net = fl.net
    contract = _contract()
    out: list[str] = []
    if live("split-placement"):
        out += [f"the split datapath holds {c.kind} cell {n}: the split builds no {c.kind}"
                for n, c in sorted(net.cells.items()) if c.kind in GONE]
        out += [f"the split datapath holds the map writer's local {n}: the split builds no map writer"
                for n in sorted(net.names) if n.startswith(census_ports.REMOVED_SCOPE)][:1]
    frames = sorted(n for n, c in net.cells.items() if c.kind == CTRL_SPLIT)
    if len(frames) != 1 and live("split-placement"):
        out.append(f"the split datapath holds {len(frames)} {CTRL_SPLIT} cells, not one")
    if face is None:
        out.append(f"the all-fabric netlist of the shape {shape} holds no pp_shadow cell to read the faces from")
        return SplitSurvey({}, out)
    out += _table_findings(table, net.ports, contract)
    out += _face_findings(table)
    rows = {port: (cls, row) for cls in CLASSES for port, row in table.get(cls, {}).items() if port in net.ports}
    ctx = _Ctx(fl, pc, Back(fl, pc), face, rows, contract, frames)
    if live("split-placement"):
        out += [f"the map writer's net {n}, which the all-fabric exclusion names, comes from "
                f"{', '.join(sorted(srcs))} in the split, not a constant: the split builds no map writer"
                for n in census_ports.REMOVED_WITH_WRAPPER if n in net.names
                for srcs in [ctx.back.closure(net.names[n])] if srcs]
    out += _drives(ctx) + _tied(ctx) + _frame_block(ctx) + _field_reads(ctx)
    consumed, found = _consumed(ctx)
    out += found
    counts = {cls: sum(1 for p in table.get(cls, {}) if p in net.ports) for cls in CLASSES}
    counts["ports"] = sum(1 for p in net.ports if CTL.match(p))
    counts["consumed"] = consumed
    counts["unread"] = sum(1 for p in UNREAD_BOTH if p in rows)
    return SplitSurvey(counts, out)


def _drives(ctx: _Ctx) -> list[str]:
    """split-drives: each wrapper output's net driven by the rows standing for it, each ctl output by the net
    its wrapper input read."""
    if not live("split-drives"):
        return []
    standing: dict[str, list[str]] = defaultdict(list)
    for port, (_cls, row) in ctx.rows.items():
        for s in row.stands:
            if isinstance(s, str):
                standing[s].append(port)
    out: list[str] = []
    for wport in sorted(w for w in standing if w in ctx.face.dirs):
        want = set(standing[wport])
        if ctx.face.dirs[wport] == "output":
            out += _drives_out(ctx, wport, want)
        else:
            out += _drives_in(ctx, wport, want)
    return out


def _tied(ctx: _Ctx) -> list[str]:
    """split-tied: the G outputs' nets and the class-D values the block does not carry are constants."""
    out: list[str] = []
    for wport in sorted(p for p in (*census_ports.PORTS["G"], *TIED_C) if ctx.face.dirs.get(p) == "output"):
        if wport in FRAME_PORTS or not live("split-tied"):
            continue
        named = ctx.face.bits.get(wport, ())
        bits = [b for b in _split_bits(ctx.net, named) if b is not None]
        ruled = G_DRIVEN.get(wport, ("",))[0]
        srcs: set[tuple] = set()
        for b in bits:
            srcs |= ctx.back.sources(b)
        driven = sorted({s[1] for s in srcs if s[0] == "net"} | {f"{s[1]}.{s[2]}" for s in srcs if s[0] == "cell"})
        if ruled and driven == [ruled]:
            continue
        driven = sorted(ctx.back.closure(bits))
        if driven:
            name = sorted({x[0] for x in named if isinstance(x, tuple)})
            kind = "G output" if wport in census_ports.PORTS["G"] else "class-D value the block does not carry"
            out.append(f"{', '.join(name)}, the net of the wrapper's {kind} {wport}, is driven by {', '.join(driven)} "
                       f"in the split, not a constant" + (f" or {ruled}" if ruled else ""))
    return out


def _frame_block(ctx: _Ctx) -> list[str]:
    """split-frame-block: KL_ctrl_split takes the wrapper's frame ports net for net, and the M rows its ports."""
    if not ctx.frames or not live("split-frame-block"):
        return []
    out: list[str] = []
    fcell = ctx.net.cells[ctx.frames[0]]
    for wport in FRAME_PORTS:
        named = list(ctx.face.bits.get(wport, ()))
        have = [ctx.net.bit_name[b] if isinstance(b, int) else b for b in fcell.conns.get(wport, ())]
        if have != named:
            out.append(f"{ctx.frames[0]}.{wport} carries {_names(have)}, not {_names(named)}, which the wrapper's "
                       f"{wport} carried")
    for port, (_cls, row) in sorted(ctx.rows.items()):
        for s in row.stands:
            if isinstance(s, tuple) and fcell.conns.get(s[1]) != ctx.net.ports[port][1]:
                out.append(f"{port} does not reach {ctx.frames[0]}.{s[1]}")
    return out


def _field_reads(ctx: _Ctx) -> list[str]:
    """split-field-reads: each field read of the class-D census holds in the split and reaches the wire."""
    if not live("split-field-reads"):
        return []
    out: list[str] = []
    field_rows = {k for k, r in ctx.pc.CENSUS.items() if r.kind == "field"}
    for wire, consumer in sorted(field_rows & ctx.face.reads):
        hits = ctx.pc.first_hop(ctx.fl, wire) if wire in ctx.net.names else {}
        if consumer not in hits:
            out.append(f"the field read {wire} -> {consumer} does not hold in the split datapath")
        elif not any(k == "wire" for k, _ in ctx.pc.cone(ctx.fl, hits[consumer])):
            out.append(f"the field read {wire} -> {consumer} reaches no wire in the split datapath")
    return out


def _consumed(ctx: _Ctx) -> tuple[int, list[str]]:
    """split-consumed and split-beyond: (the live bits consumed, every finding)."""
    live_bits = _live(ctx.fl, ctx.pc)
    consumed, out = 0, []
    for port, (_cls, row) in sorted(ctx.rows.items()):
        d, pbits = ctx.net.ports[port]
        if d != "input":
            continue
        n = {"source": ctx.face.n_src, "sink": ctx.face.n_snk}.get(row.per)
        keep = len(pbits) if n is None else len(pbits) // ctx.contract.entries * n
        reached = [isinstance(b, int) and b in live_bits for b in pbits[:keep]]
        consumed += sum(reached)
        what = row.carrier[0] if len(row.carrier) == 1 else " + ".join(row.carrier)
        if port in UNREAD_BOTH:
            af_read = sorted(s for s in row.stands if s in ctx.face.read)
            if any(reached) and live("split-consumed"):
                out.append(f"split port {port} is consumed in the split: drop it from UNREAD_BOTH")
            elif af_read and live("split-consumed"):
                out.append(f"split port {port} reaches no cone end, but the all-fabric datapath reads the net of "
                           f"the wrapper's {af_read[0]}: the split lost its consumer")
        elif not all(reached) and live("split-consumed"):
            out.append(f"split port {port} bit {reached.index(False)} reaches no cone end: the split datapath does "
                       f"not consume {what}")
        for k, b in enumerate(pbits[keep:], keep):
            if isinstance(b, int) and ctx.fl.fanout.get(b) and live("split-beyond"):
                out.append(f"split port {port} bit {k} is read, past the shape's {n} {row.per}(s)")
                break
    return consumed, out


def _drives_out(ctx: _Ctx, wport: str, want: set[str]) -> list[str]:
    """A wrapper output's net in the split: driven by exactly the ports standing for it, bit for bit where one
    port alone does."""
    named = ctx.face.bits.get(wport, ())
    out: list[str] = []
    got: set[str] = set()
    for k, b in enumerate(_split_bits(ctx.net, named)):
        if b is None:
            return [f"{named[k][0]}, the net of the wrapper's {wport}, is not in the split datapath"]
        srcs = ctx.back.sources(b)
        got |= {s[1] for s in srcs if s[0] == "net"} | {f"{s[1]}.{s[2]}" for s in srcs if s[0] == "cell"}
        hits = [s for s in srcs if s[0] == "net"]
        if len(want) == 1 and not out and len(hits) == 1 and hits[0][1] in want:
            port = hits[0][1]
            at = _expected(ctx.rows[port][1], wport, ctx.face, k, len(ctx.net.ports[port][1]))
            if at is not None and hits[0][2] not in at:
                out.append(f"{named[k][0]}[{named[k][1]}], the net of the wrapper's {wport}, is driven by "
                           f"{port}[{hits[0][2]}], not {port}[{at.start}]")
    if got != want:
        name = sorted({x[0] for x in named if isinstance(x, tuple)})
        out.append(f"{', '.join(name)}, the net of the wrapper's {wport}, is driven by "
                   f"{', '.join(sorted(got)) or 'a constant'} in the split, not by {', '.join(sorted(want))}")
    return out


def _drives_in(ctx: _Ctx, wport: str, want: set[str]) -> list[str]:
    """A ctl output standing for a wrapper input: driven by the net that input read, bit for bit."""
    named = ctx.face.bits.get(wport, ())
    out: list[str] = []
    want_names = {x[0] for x in named if isinstance(x, tuple)}
    for port in sorted(want):
        got: set[str] = set()
        shifted = ""
        for k, b in enumerate(ctx.net.ports[port][1]):
            hits = [s for s in ctx.back.sources(b) if s[0] == "net"]
            got |= {s[1] for s in hits}
            if (not shifted and k < len(named) and isinstance(named[k], tuple) and len(hits) == 1
                    and hits[0][1] in want_names and (hits[0][1], hits[0][2]) != named[k]):
                shifted = (f"{port}[{k}] is driven by {hits[0][1]}[{hits[0][2]}], not by {named[k][0]}[{named[k][1]}], "
                           f"which the wrapper's {wport} read")
        out += [shifted] if shifted else []
        if got != want_names:
            out.append(f"{port} is driven by {', '.join(sorted(got)) or 'a constant'} in the split, not by "
                       f"{', '.join(sorted(want_names))}, which the wrapper's {wport} read")
    return out


def _names(bits: list) -> str:
    """A short form of a list of (name, index) bits."""
    names = sorted({x[0] for x in bits if isinstance(x, tuple)})
    return ", ".join(names) if names else "constants" if bits else "nothing"


def _expected(row: Face, wport: str, face: AfFace, k: int, width: int) -> range | None:
    """The port bits bit k of wport's net may come from: the same bit of the same entry, or of the same field
    of a packed row; an entry's bits where the wrapper and the port hold an entry in different widths."""
    if not row.per:
        at = _offset(row, wport, face) + k
        return range(at, at + 1)
    n = face.n_src if row.per == "source" else face.n_snk
    entries = _contract().entries
    w_net, w_port = len(face.bits.get(wport, ())) // max(n, 1), width // entries
    if not w_net or not w_port:
        return None
    first = k // w_net * w_port
    if w_net == w_port:
        return range(first + k % w_net, first + k % w_net + 1)
    return range(first, first + w_port)


def _offset(row: Face, wport: str, face: AfFace) -> int:
    """Where wport's bits start in the row's port: in a packed row (one stand per carrier field) the widths of
    the stands before it; else 0, every stand reading the port from its first bit."""
    if len(row.stands) < 2 or len(row.stands) != len(row.carrier):
        return 0
    off = 0
    for s in row.stands:
        if s == wport:
            return off
        off += len(face.bits.get(s, ()))
    return 0


@dataclass(frozen=True)
class Contract:
    """What a split row may name, and how wide."""

    fields: dict[str, int]
    pub: dict[str, int]
    events: dict[str, int]
    event_types: frozenset[str]
    mbx_ports: frozenset[str]
    per_entry: frozenset[str]
    entries: int


@functools.lru_cache(maxsize=1)
def _contract() -> Contract:
    """The contract's publication and face fields and events, and KL_mbx's ports."""
    import mailbox_model
    c = mailbox_model.load()
    known = census_ports.carriers()
    pub = {f"{r.name}.{f.name}": f.width
           for r in c.pub_registers + c.pub_source_registers + c.pub_sink_registers for f in r.fields}
    per = {f"{r.name}.{f.name}" for r in (c.pub_source_registers + c.pub_sink_registers + c.face_source_registers
                                          + c.face_sink_registers) for f in r.fields}
    if c.pub_sources != c.pub_sinks:
        raise ValueError("the contract's sources and sinks differ in number; the split's ports carry one count")
    return Contract(known.fields, pub, known.events, frozenset(e.name for e in c.event_types), known.mbx_ports,
                    frozenset(per), c.pub_sources)

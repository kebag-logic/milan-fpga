#!/usr/bin/env python3
# Generate hdl/aecp/doc/atdecc_architecture.drawio — a block diagram of the
# Milan v1.2 ATDECC (ADP + AECP/AEM) hardware entity as implemented in hdl/aecp.
import html

cells = []
def esc(s): return html.escape(s, quote=True)
def box(i, x, y, w, h, label, fill="#dae8fc", stroke="#6c8ebf", font=12, rounded=1, dashed=0, align="center"):
    style = (f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"fontSize={font};verticalAlign=middle;align={align};spacingLeft=6;spacingRight=6;")
    if dashed: style += "dashed=1;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def grp(i, x, y, w, h, label, stroke="#999999", fill="none", font=13):
    style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};dashed=1;"
             f"verticalAlign=top;align=left;fontSize={font};fontStyle=1;spacingLeft=8;spacingTop=4;")
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def edge(i, s, t, label="", style="", dashed=0):
    st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;"
          "strokeColor=#333333;fontSize=11;" + style)
    if dashed: st += "dashed=1;strokeColor=#999999;endArrow=open;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" '
                 f'source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')

# ---- title ----
box("title", 40, 12, 1180, 30,
    "Milan v1.2 ATDECC entity (IEEE 1722.1-2021) — hardware datapath  ·  hdl/aecp",
    fill="#f5f5f5", stroke="#666666", font=15, rounded=0)

# ---- groups (drawn first, behind) ----
grp("g_net", 40, 60, 1180, 70, "MAC / wire  (AVTP ethertype 0x22F0, in milan_datapath)")
grp("g_rx",  40, 150, 300, 620, "RX path")
grp("g_core",360, 150, 470, 620, "AECP / AEM core pipeline  (hdl/aecp/KL_aecp_*)")
grp("g_tx", 850, 150, 370, 620, "TX path  (low-rate control merged into MAC TX)")
grp("g_model", 40, 800, 590, 190, "Entity model — single source of truth")
grp("g_ctrl", 650, 800, 230, 190, "milan_csr (CPU AXI-Lite)")
grp("g_ver", 900, 800, 320, 190, "Verification")

# ---- MAC / wire ----
box("mac_rx", 70, 80, 240, 40, "MAC RX  →  rx_mac_filter (TCAM)\npost-filter stream rx_axis_to_dma", fill="#d5e8d4", stroke="#82b366", font=11)
box("mac_tx", 950, 80, 240, 40, "MAC TX  (eth_mac_1g_rgmii)\ntx_axis_to_mac", fill="#d5e8d4", stroke="#82b366", font=11)
box("dma", 660, 85, 250, 30, "→ RX DMA / CPU (kl-eth)  — the tap is a copy", fill="#f8cecc", stroke="#b85450", font=10)

# ---- RX path ----
box("ingress", 60, 200, 260, 130,
    "KL_aecp_ingress\n\n• MONITOR tap on rx_axis_to_dma (reads only,\n  never backpressures the NIC)\n• filter: AECP-for-us (dst=our MAC, 0xFB)\n  and ADP ENTITY_DISCOVER\n• store-and-forward, strip Eth hdr,\n  replay BIG-lane\n• capture controller src MAC", fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")
box("adp_disc", 60, 360, 260, 40, "adp_discover_o  →  advertiser (discovery response)", fill="#ffe6cc", stroke="#d79b00", font=10)

# ---- AECP core (vertical) ----
box("val", 380, 200, 430, 46, "KL_aecp_packet_validator — drop bad message_type / CDL < 12", fill="#dae8fc", stroke="#6c8ebf", font=11, align="left")
box("par", 380, 270, 430, 56, "KL_aecp_common_parser — extract aecp_hdr_t\n(target/controller EID, seq, command_type); entity_id match", fill="#dae8fc", stroke="#6c8ebf", font=11, align="left")
box("l0",  380, 350, 245, 90, "KL_aecp_l0_state\n\n• LOCK_ENTITY (60 s timeout)\n• ACQUIRE → NOT_SUPPORTED\n• current_configuration", fill="#e1d5e7", stroke="#9673a6", font=10, align="left")
box("tim", 645, 350, 165, 90, "KL_aecp_timers\n\n1 kHz tick\n→ lock timer\n→ counter gate", fill="#e1d5e7", stroke="#9673a6", font=10, align="left")
box("bld", 380, 470, 245, 290,
    "KL_aecp_response_builder\n— the command brain\n\n• capture payload,\n  classify command\n• READ_DESCRIPTOR\n• GET/SET name · config ·\n  sampling-rate · stream-format\n• GET_STREAM_INFO · AVB_INFO ·\n  GET_COUNTERS (full-size, all\n  statuses) · MVU GET_MILAN_INFO\n• SET_* write-back\n• build response frame\n  (little-lane,\n   CDL = frame − 26)", fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")

# ---- store / overlay / accessor (right column, no overlap with builder) ----
box("acc", 645, 470, 165, 70, "KL_aecp_accessor\n\n(type, index)\n→ base, len", fill="#d5e8d4", stroke="#82b366", font=10, align="left")
box("store", 645, 560, 165, 80, "KL_aecp_aem_store\n\ndescriptor ROM\n+ SET write-back", fill="#d5e8d4", stroke="#82b366", font=10, align="left")
box("dyn", 645, 660, 165, 100, "KL_aecp_aem_dyn_mux\n\nlive-field overlay:\nentity_id, MAC, caps,\navailable_index,\ncurrent_config", fill="#d5e8d4", stroke="#82b366", font=10, align="left")

# ---- TX path ----
box("adv", 880, 200, 310, 120,
    "adp_advertiser\n\n• periodic ENTITY_AVAILABLE (valid_time)\n• answers ENTITY_DISCOVER (rcv_discover)\n• ENTITY_DEPARTING on link-down\n• available_index +1 on EVERY ADPDU sent\n  (la_avdecc/Hive strict-increment rule)", fill="#ffe6cc", stroke="#d79b00", font=10, align="left")
box("mux_lo", 880, 380, 310, 56, "adp_tx_arbiter (low-rate merge)\nADP advertise  +  AECP response", fill="#fff2cc", stroke="#d6b656", font=11, align="left")
box("mux_dp", 880, 470, 310, 56, "adp_tx_arbiter (datapath merge)\ncontrol stream inserted in inter-frame gaps", fill="#fff2cc", stroke="#d6b656", font=11, align="left")
box("txout", 880, 560, 310, 40, "→ tx_axis_to_mac", fill="#d5e8d4", stroke="#82b366", font=11)

# ---- model / generation ----
box("json", 60, 840, 180, 44, "avdecc/\nmilan-v12-entity.json\n(byte-accurate model)", fill="#f5f5f5", stroke="#666", font=10)
box("gen", 270, 840, 150, 44, "gen_aem_store.py\n(trim → 5 descriptors)", fill="#f5f5f5", stroke="#666", font=10)
box("svh", 450, 840, 160, 44, "hdl/aecp/gen/\naecp_aem_rom.svh\n(ROM+dir+overlay map)", fill="#f5f5f5", stroke="#666", font=10)
box("desc", 60, 905, 550, 70,
    "5 descriptors:  ENTITY → CONFIGURATION → { AVB_INTERFACE ×1 · AUDIO_UNIT ×1 · STREAM_OUTPUT ×1 }\n"
    "one configuration · 48/96/192 kHz · AAF talker.  Static fields in ROM; live fields overlaid at read.",
    fill="#f5f5f5", stroke="#666", font=10, align="left")

# ---- CSR ----
box("csr_id", 660, 840, 210, 60, "0x600 ADP/identity group\nentity_id · caps · station MAC ·\ngPTP GM/domain · valid_time\n(shared by ADP + AEM → can't disagree)", fill="#e1d5e7", stroke="#9673a6", font=9, align="left")
box("csr_st", 660, 910, 210, 60, "0x648 / 0x64C  AECP status (RO)\nlocked · cmd_count · resp_count ·\ncurrent_configuration", fill="#e1d5e7", stroke="#9673a6", font=9, align="left")

# ---- verification ----
box("v_cosim", 910, 840, 300, 40, "tsn-gen ↔ Verilator co-sim (Vaecp_cosim)\nreal RTL over AxiStreamBeat socket — 36/36", fill="#d5e8d4", stroke="#82b366", font=9, align="left")
box("v_la", 910, 888, 300, 40, "la_avdecc probe (Hive's library) on pw0\nfull enumeration; strict payload-size checks", fill="#d5e8d4", stroke="#82b366", font=9, align="left")
box("v_ctl", 910, 936, 300, 34, "avdecc/milan_controller.py (peer, on silicon)\n+ tb/verilator/aecp 61/61", fill="#d5e8d4", stroke="#82b366", font=9, align="left")

# ---- edges: RX/command flow ----
edge("e1", "mac_rx", "ingress", "tap (copy)")
edge("e1b", "mac_rx", "dma", "", dashed=1)
edge("e2", "ingress", "val", "big-lane AXIS")
edge("e3", "val", "par")
edge("e4", "par", "l0", "aecp_hdr_t")
edge("e5", "par", "bld", "hdr + payload")
edge("e6", "l0", "bld", "status / reject")
edge("e7", "tim", "l0", "1 kHz", dashed=1)
edge("e8", "ingress", "adp_disc", "ENTITY_DISCOVER")
edge("e9", "adp_disc", "adv", "rcv_discover")

# ---- edges: store <-> builder ----
edge("e10", "bld", "acc", "desc lookup")
edge("e11", "acc", "store", "base")
edge("e12", "store", "dyn", "ROM byte")
edge("e13", "dyn", "bld", "overlaid byte")
edge("e13b","bld", "store", "SET write-back", style="exitX=1;exitY=0.2;")

# ---- edges: TX / response flow ----
edge("e14", "bld", "mux_lo", "response AXIS")
edge("e15", "adv", "mux_lo", "advertise")
edge("e16", "mux_lo", "mux_dp")
edge("e17", "mux_dp", "txout")
edge("e18", "txout", "mac_tx")

# ---- edges: model/gen ----
edge("e19", "json", "gen")
edge("e20", "gen", "svh")
edge("e21", "svh", "store", "$include", dashed=1)
edge("e21b","svh", "acc", "", dashed=1)
edge("e21c","svh", "dyn", "", dashed=1)

# ---- edges: CSR ----
edge("e22", "csr_id", "adv", "identity", dashed=1)
edge("e23", "csr_id", "bld", "identity", dashed=1)
edge("e24", "bld", "csr_st", "cmd/resp/lock", dashed=1)

xml = ('<mxfile host="app.diagrams.net"><diagram name="atdecc-architecture">'
       '<mxGraphModel dx="1400" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" '
       'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1280" pageHeight="1040" '
       'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
       + "".join(cells) +
       '</root></mxGraphModel></diagram></mxfile>')
import sys
open(sys.argv[1], "w").write(xml)
print("wrote", sys.argv[1], len(cells), "cells")

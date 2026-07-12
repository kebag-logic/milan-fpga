#!/usr/bin/env python3
# Generate hdl/aecp/doc/atdecc_architecture.drawio — the Milan v1.2 ATDECC
# (ADP + AECP/AEM) hardware entity, as a MULTI-PAGE document:
#   page 1          : high-level block overview
#   pages 2..8      : one page per displayed block, drilling from the block's
#                     role down to byte offsets, bit fields, FSM states and
#                     address maps — every number mirrors the RTL/generated
#                     sources (aecp_pkg.sv, gen/aecp_aem_rom.svh, milan_csr.sv).
# Regenerate: python3 atdecc_architecture.gen.py atdecc_architecture.drawio
# Render:     python3 atdecc_architecture.render.py atdecc_architecture.drawio
import html, re, sys

# ----------------------------------------------------------------------- #
# tiny drawio builder
# ----------------------------------------------------------------------- #
PAGES = []          # list of (name, cells[], w, h)
cells = None
def page(name, w=1280, h=1040):
    global cells
    cells = []
    PAGES.append((name, cells, w, h))
def esc(s):
    # drawio conventions: &#10; = hard line break; runs of spaces become
    # &#160; (nbsp) so column layouts survive HTML space collapsing.
    t = html.escape(s, quote=True).replace("\n", "&#10;")
    return re.sub(r"  +", lambda m: "&#160;" * len(m.group(0)), t)
def box(i, x, y, w, h, label, fill="#dae8fc", stroke="#6c8ebf", font=12,
        rounded=1, dashed=0, align="center", mono=0):
    style = (f"rounded={rounded};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};"
             f"fontSize={font};verticalAlign=middle;align={align};spacingLeft=6;spacingRight=6;")
    if dashed: style += "dashed=1;"
    if mono:   style += "fontFamily=Courier New;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def grp(i, x, y, w, h, label, stroke="#999999", fill="none", font=13):
    style = (f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};dashed=1;"
             f"verticalAlign=top;align=left;fontSize={font};fontStyle=1;spacingLeft=8;spacingTop=4;")
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
def edge(i, s, t, label="", style="", dashed=0):
    st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;"
          "strokeColor=#333333;fontSize=11;labelBackgroundColor=#ffffff;" + style)
    if dashed: st += "dashed=1;strokeColor=#999999;endArrow=open;"
    cells.append(f'<mxCell id="{i}" value="{esc(label)}" style="{st}" edge="1" parent="1" '
                 f'source="{s}" target="{t}"><mxGeometry relative="1" as="geometry"/></mxCell>')
def note(i, x, y, w, h, label):
    box(i, x, y, w, h, label, fill="#fff9d6", stroke="#b3a100", font=10, align="left")
def table(i, x, y, w, rows, font=10, title=None, fill="#f5f5f5", stroke="#666666", rh=17):
    """rows: list of strings, one line each, rendered as a monospace box"""
    label = "\n".join(rows)
    h = rh * len(rows) + 14
    if title:
        box(i + "_t", x, y, w, 22, title, fill="#e8e8e8", stroke=stroke, font=font+1, rounded=0)
        y += 22
    box(i, x, y, w, h, label, fill=fill, stroke=stroke, font=font, rounded=0, align="left", mono=1)
    return y + h

# ======================================================================= #
# PAGE 1 — OVERVIEW
# ======================================================================= #
page("1-overview", w=1520, h=1150)
box("title", 40, 12, 1440, 30,
    "Milan v1.2 ATDECC entity (IEEE 1722.1-2021) — hardware datapath  ·  hdl/aecp   (pages 2-8: every block down to bit level)",
    fill="#f5f5f5", stroke="#666666", font=14, rounded=0)

grp("g_net", 40, 60, 1440, 70, "MAC / wire  (AVTP ethertype 0x22F0, in milan_datapath)")
grp("g_rx",  40, 150, 340, 700, "RX path   [page 2]")
grp("g_core",420, 150, 530, 700, "AECP / AEM core pipeline  (hdl/aecp/KL_aecp_*)   [pages 3-5]")
grp("g_tx", 1010, 150, 440, 700, "TX path  (low-rate control merged into MAC TX)   [pages 7-8]")
grp("g_model", 40, 880, 590, 190, "Entity model — single source of truth   [page 6]")
grp("g_ctrl", 650, 880, 240, 190, "milan_csr (CPU AXI-Lite)   [page 8]")
grp("g_ver", 910, 880, 470, 190, "Verification")

box("mac_rx", 70, 80, 240, 40, "MAC RX  →  rx_mac_filter (TCAM)\npost-filter stream rx_axis_to_dma", fill="#d5e8d4", stroke="#82b366", font=11)
box("mac_tx", 1180, 80, 240, 40, "MAC TX  (eth_mac_1g_rgmii)\ntx_axis_to_mac", fill="#d5e8d4", stroke="#82b366", font=11)
box("dma", 680, 85, 260, 30, "→ RX DMA / CPU (kl-eth)  — the tap is a copy", fill="#f8cecc", stroke="#b85450", font=10)

box("ingress", 60, 200, 280, 140,
    "KL_aecp_ingress   [p2]\n\n• MONITOR tap on rx_axis_to_dma (reads only,\n  never backpressures the NIC)\n• filter: AECP-for-us (dst=our MAC, 0xFB)\n  and ADP ENTITY_DISCOVER\n• store-and-forward (fbuf 128 B LUTRAM),\n  strip Eth hdr,\n  replay BIG-lane\n• capture controller src MAC", fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")
box("adp_disc", 60, 400, 280, 44, "adp_discover_o  →  advertiser (discovery response)", fill="#ffe6cc", stroke="#d79b00", font=10)

box("val", 440, 200, 490, 46, "KL_aecp_packet_validator   [p3] — drop bad message_type / CDL < 12", fill="#dae8fc", stroke="#6c8ebf", font=11, align="left")
box("par", 440, 290, 490, 56, "KL_aecp_common_parser   [p3] — extract aecp_hdr_t\n(target/controller EID, seq, command_type); entity_id match", fill="#dae8fc", stroke="#6c8ebf", font=11, align="left")
box("l0",  440, 400, 220, 100, "KL_aecp_l0_state   [p4]\n\n• LOCK_ENTITY (60 s timeout)\n• ACQUIRE → NOT_SUPPORTED\n• current_configuration", fill="#e1d5e7", stroke="#9673a6", font=10, align="left")
box("tim", 740, 400, 190, 56, "KL_aecp_timers   [p4]\n1 kHz tick → lock timer", fill="#e1d5e7", stroke="#9673a6", font=10, align="left")
box("bld", 440, 550, 280, 220,
    "KL_aecp_response_builder   [p5]  — the command brain\n\n• capture payload, classify command\n• READ_DESCRIPTOR · GET/SET name·config·\n  sampling-rate·stream-format · GET_STREAM_INFO·\n  AVB_INFO · GET_COUNTERS · GET_AS_PATH · MVU\n  GET_MILAN_INFO · SET_* write-back\n• build response frame (little-lane, CDL = frame − 26)", fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")

box("acc", 760, 550, 170, 56, "KL_aecp_accessor   [p6]\ndirectory 5 × 64b FF\n(type,index) → base,len", fill="#d5e8d4", stroke="#82b366", font=10)
box("store", 760, 626, 170, 56, "KL_aecp_aem_store   [p6]\nROM 808 B BRAM (byte port 8b)\n+ volatile SET write-back", fill="#d5e8d4", stroke="#82b366", font=10)
box("dyn", 760, 702, 170, 68, "KL_aecp_aem_dyn_mux   [p6]\nlive-field overlay mux\n(entity_id, MAC, caps, avail_index)", fill="#d5e8d4", stroke="#82b366", font=10)

box("adv", 1040, 200, 380, 150,
    "adp_advertiser   [p7]\n\n• periodic ENTITY_AVAILABLE (valid_time)\n• answers ENTITY_DISCOVER (rcv_discover)\n• ENTITY_DEPARTING on link-down\n• available_index +1 on EVERY ADPDU sent\n  (la_avdecc/Hive strict-increment rule)", fill="#ffe6cc", stroke="#d79b00", font=10, align="left")
box("mux_lo", 1040, 430, 380, 56, "adp_tx_arbiter (low-rate merge)   [p8]\nADP advertise  +  AECP response", fill="#fff2cc", stroke="#d6b656", font=11, align="left")
box("mux_dp", 1040, 560, 380, 56, "adp_tx_arbiter (datapath merge)   [p8]\ncontrol stream inserted in inter-frame gaps", fill="#fff2cc", stroke="#d6b656", font=11, align="left")
box("txout", 1040, 680, 380, 40, "→ tx_axis_to_mac", fill="#d5e8d4", stroke="#82b366", font=11)

box("json", 60, 920, 180, 44, "avdecc/\nmilan-v12-entity.json\n(byte-accurate model)", fill="#f5f5f5", stroke="#666", font=10)
box("gen", 270, 920, 150, 44, "gen_aem_store.py\n(trim → 5 descriptors)", fill="#f5f5f5", stroke="#666", font=10)
box("svh", 450, 920, 160, 44, "hdl/aecp/gen/\naecp_aem_rom.svh\n(ROM+dir+overlay map)", fill="#f5f5f5", stroke="#666", font=10)
box("desc", 60, 985, 550, 70,
    "5 descriptors:  ENTITY → CONFIGURATION → { AVB_INTERFACE ×1 · AUDIO_UNIT ×1 · STREAM_OUTPUT ×1 }\n"
    "one configuration · 48/96/192 kHz · AAF talker.  Static fields in ROM; live fields overlaid at read.",
    fill="#f5f5f5", stroke="#666", font=10, align="left")

box("csr_id", 665, 920, 210, 64, "0x600 ADP/identity group\nentity_id · caps · station MAC ·\ngPTP GM/domain · valid_time\n(shared by ADP + AEM → can't disagree)", fill="#e1d5e7", stroke="#9673a6", font=9, align="left")
box("csr_st", 665, 995, 210, 60, "0x648 / 0x64C  AECP status (RO)\nlocked · cmd_count · resp_count ·\ncurrent_configuration", fill="#e1d5e7", stroke="#9673a6", font=9, align="left")

box("v_cosim", 925, 920, 440, 42, "tsn-gen ↔ Verilator co-sim (Vaecp_cosim)\nreal RTL over AxiStreamBeat socket — 42/42", fill="#d5e8d4", stroke="#82b366", font=9, align="left")
box("v_la", 925, 972, 440, 42, "la_avdecc probe (Hive's library) on pw0\nfull enumeration; strict payload-size checks", fill="#d5e8d4", stroke="#82b366", font=9, align="left")
box("v_ctl", 925, 1024, 440, 36, "avdecc/milan_controller.py 31/31 on silicon · la_avdecc\nMilan=1 CLEAN · tb aecp 68/68 + acmp 41/41 · Yosys 20/20", fill="#d5e8d4", stroke="#82b366", font=9, align="left")

edge("e1", "mac_rx", "ingress", "tap (copy)")
edge("e1b", "mac_rx", "dma", "", dashed=1)
edge("e2", "ingress", "val", "big-lane AXIS")
edge("e3", "val", "par")
edge("e4", "par", "l0", "aecp_hdr_t")
edge("e5", "par", "bld", "hdr + payload")
edge("e6", "l0", "bld", "status / reject")
edge("e7", "tim", "l0", "1 kHz", dashed=1)
edge("e8", "ingress", "adp_disc", "ENTITY_DISCOVER")
edge("e9", "adp_disc", "adv")
edge("e10", "bld", "acc", "lookup")
edge("e11", "acc", "store", "base")
edge("e12", "store", "dyn", "ROM byte")
edge("e13", "dyn", "bld", "overlaid byte")
edge("e13b","bld", "store", "SET wb", style="exitX=1;exitY=0.2;")
edge("e14", "bld", "mux_lo", "response AXIS")
edge("e15", "adv", "mux_lo", "advertise")
edge("e16", "mux_lo", "mux_dp")
edge("e17", "mux_dp", "txout")
edge("e18", "txout", "mac_tx")
edge("e19", "json", "gen")
edge("e20", "gen", "svh")
edge("e21", "svh", "store", "$include", dashed=1)
edge("e21b","svh", "acc", "", dashed=1)
edge("e21c","svh", "dyn", "", dashed=1)
edge("e22", "csr_id", "adv", "identity", dashed=1)
edge("e23", "csr_id", "bld", "identity", dashed=1)
edge("e24", "bld", "csr_st", "cmd/resp/lock", dashed=1)

# ======================================================================= #
# PAGE 2 — KL_aecp_ingress
# ======================================================================= #
page("2-ingress")
box("t2", 40, 12, 1180, 30,
    "KL_aecp_ingress — RX monitor tap, frame filter, store-and-forward, big-lane replay   (hdl/aecp/KL_aecp_ingress.sv)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g2a", 40, 60, 560, 340, "role + timing isolation")
box("i2a", 60, 92, 520, 110,
    "A pure MONITOR on the post-TCAM RX stream (rx_axis_to_dma): it observes\n"
    "tvalid/tdata/tkeep/tlast and NEVER drives tready — the NIC/DMA path cannot be\n"
    "stalled by the listener. All four tap inputs are REGISTERED once on entry\n"
    "(rxv_r/rxd_r/rxk_r/rxl_r) so the AECP block adds zero combinational load on\n"
    "datapath nets (this closed the aecp1 timing failure, WNS −0.19 → +0.19).",
    fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")
table("t2fsm", 60, 215, 520, [
 "FSM (st_t, 2 bits)",
 "COLLECT_S   accepted RX bytes -> fbuf[wr_cnt]; frames > 128 B set",
 "            overflow_r, get ignored (MAX_FRAME_BYTES=128: every AECP",
 "            command fits; keeps the buffer in LUTRAM, the mux shallow)",
 "CLASSIFY_S  1 cycle after tlast: run the filter tree (right);",
 "            losers -> COLLECT_S",
 "REPLAY_S    stream fbuf[14..n-1] (Eth header stripped) to validator",
 "HOLD_S      park until the builder pops req (req_pop_i) —",
 "            exactly one command in flight",
], font=10)

grp("g2b", 620, 60, 600, 340, "accept filter — wire bytes tested (frame offsets)")
table("t2f", 640, 92, 560, [
 "byte 0-5    dst MAC     == station_mac                     [AECP arm]",
 "byte 12-13  ethertype   == 0x22F0 (AVTP)",
 "byte 14     subtype     == 0xFB (AECP)      or 0xFA (ADP)",
 "byte 15     {sv[7]=0, version[6:4]=0, message_type[3:0]}",
 "",
 "AECP arm:   message_type in {0 AEM_COMMAND, 6 VU_COMMAND}",
 "            byte 18-25 target_entity_id == entity_id (CSR)",
 "            -> capture; req_src_mac_o = bytes 6-11; replay",
 "",
 "ADP arm:    dst = 91:E0:F0:01:00:00, subtype 0xFA,",
 "            message_type == 2 (ENTITY_DISCOVER),",
 "            byte 18-25 == 0 (discover-all) or == our entity_id",
 "            -> 1-cycle adp_discover_o pulse (no replay)",
], font=10)

grp("g2c", 40, 420, 1180, 260, "byte-lane discipline — the ONE trap in this block")
box("i2lane", 60, 452, 560, 210,
    "RX tap (Forencich MAC convention, LITTLE lane):\n"
    "  tdata[7:0]   = FIRST byte on the wire\n"
    "  fbuf[wr_cnt+l] <= rxd_r[8*l +: 8] per set tkeep bit l\n\n"
    "Replay to the parser chain (BIG lane — fields MSB-first):\n"
    "  tdata[63:56] = first replayed byte (frame byte 14 = subtype)\n"
    "  w_beat[8*(7-l) +: 8] = fbuf[rp + l]\n"
    "  tkeep MSB-first: w_keep[7-l] = 1 while bytes remain\n\n"
    "The response builder emits little-lane again —\n"
    "only the parser chain is big-lane.",
    fill="#fff9d6", stroke="#b3a100", font=10, align="left", mono=1)
table("t2io", 650, 452, 550, [
 "in   rx_tvalid/tdata[63:0]/tkeep[7:0]/tlast   (tap, registered)",
 "     station_mac_i[47:0], entity_id_i[63:0]   (identity, CSR)",
 "     enable_i                                 (gate)",
 "out  m_axis_* flat AXIS (big lane, to validator)",
 "     req_src_mac_o[47:0]   requester MAC (response dst MAC)",
 "     req_valid_o / req_pop_i   one-command-in-flight handshake",
 "     adp_discover_o        1-cycle pulse -> adp_advertiser",
], font=10, title="ports")

# ======================================================================= #
# PAGE 3 — validator + parser
# ======================================================================= #
page("3-validator-parser")
box("t3", 40, 12, 1180, 30,
    "KL_aecp_packet_validator + KL_aecp_common_parser — AECPDU decode, bit-exact   (big-lane AXIS between them)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g3a", 40, 60, 560, 260, "KL_aecp_packet_validator")
box("i3v", 60, 92, 520, 90,
    "Gate in front of the parser: decodes the FIRST beat only, then forwards or\n"
    "eats the whole frame. Reads its own outputs via local mirrors (s_tready_l /\n"
    "m_tvalid_l) — modport read-back is what sv2v renders as top-absolute\n"
    "hierarchical paths (the Yosys portability-gate trap, fixed 2026-07-12).",
    fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")
table("t3v", 60, 195, 520, [
 "FIRST_BEAT_S  beat0 visible: message_type in {0,6} AND cdl >= 12 ?",
 "                yes -> PASS_S  (forward all beats, tready=downstream)",
 "                no  -> DROP_S  (tready=1, downstream tvalid never set)",
 "PASS_S/DROP_S -> FIRST_BEAT_S after tlast",
 "sideband: valid_o / drop_o / status_o[4:0] / msgtype_o[3:0]",
], font=10)

grp("g3b", 620, 60, 600, 260, "AECPDU on the parser bus — beat/byte map (big lane)")
table("t3map", 640, 92, 560, [
 "        lane7(63:56) ......................................... lane0",
 "beat0   subtype:FB | sv/mt | st/cdl | cdl | target_entity_id[63:32]",
 "beat1   target_entity_id[31:0] | controller_entity_id[63:32]",
 "beat2   controller_entity_id[31:0] | seq_id[15:0] | u/cmd[15:0]",
 "beat3+  command-specific payload ... (builder captures in parallel)",
 "",
 "byte1 = {sv[7], version[6:4], message_type[3:0]}  0=AEM_CMD 6=VU_CMD",
 "byte2 = {status[4:0], cdl[10:8]}    byte3 = cdl[7:0]  (CDL = len-26)",
 "u/cmd = {u[15], command_type[14:0]}",
 "VU: NO u/command_type — protocol_id(6B) 00:1B:C5:0A:C1:00 at 22-27",
], font=10)

grp("g3c", 40, 340, 1180, 300, "KL_aecp_common_parser")
box("i3p", 60, 372, 560, 120,
    "The first accepted beat IS beat0 — no dead IDLE hop. (The original IDLE_S\n"
    "consumed beat0 uncaptured; every field landed one beat late and target_eid\n"
    "took the controller's id. Root-caused in sim 2026-07-11.)\n\n"
    "Fields land in aecp_hdr_t as beats arrive; hdr_o.hdr_valid pulses at beat2\n"
    "when target_entity_id == entity_id_i; otherwise the frame drains silently.",
    fill="#dae8fc", stroke="#6c8ebf", font=10, align="left")
table("t3p", 60, 507, 560, [
 "BEAT0_S -> BEAT1_S -> BEAT2_S -> BEAT3_S -> PAYLOAD_S -> BEAT0_S",
 "(PAYLOAD_S drains transparently; undefined state -> BEAT0_S + $error",
 " [ifndef SYNTHESIS])",
], font=10)
table("t3hdr", 650, 372, 550, [
 "aecp_hdr_t {",
 "  message_type[3:0]        0 AEM_COMMAND / 6 VU_COMMAND",
 "  status[4:0]              command: always 0",
 "  control_data_length[10:0]",
 "  target_entity_id[63:0]       == our entity_id (gate)",
 "  controller_entity_id[63:0]   echoed into the response",
 "  sequence_id[15:0]            echoed into the response",
 "  u_flag, command_type[14:0]",
 "  hdr_valid                    1-cycle strobe at beat2",
 "}",
], font=10, title="parsed header (to l0_state + builder)")

# ======================================================================= #
# PAGE 4 — l0_state + timers
# ======================================================================= #
page("4-l0-timers")
box("t4", 40, 12, 1180, 30,
    "KL_aecp_l0_state + KL_aecp_timers — Milan lock semantics, no ACQUIRE   (hdl/aecp/KL_aecp_l0_state.sv)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g4a", 40, 60, 560, 400, "LOCK_ENTITY / ACQUIRE_ENTITY decision (Milan v1.2 §5.4.2)")
table("t4l", 60, 92, 520, [
 "state: locked_r, owner_eid_r[63:0], 60 s lock timer",
 "",
 "LOCK (flags[0]=0, lock):",
 "  !locked or owner==controller -> SUCCESS, owner=controller,",
 "                                  timer restart (60_000 x 1 kHz)",
 "  locked by other              -> ENTITY_LOCKED(3) + owner id",
 "LOCK (flags[0]=1, unlock):",
 "  owner==controller            -> SUCCESS, unlocked",
 "  locked by other              -> ENTITY_LOCKED(3)",
 "timer expiry                   -> silent unlock (auto-expiry)",
 "",
 "ACQUIRE (any flags)            -> NOT_SUPPORTED(11),",
 "                                  state NEVER changes (Milan)",
 "",
 "writes while locked-by-other   -> ENTITY_LOCKED(3), no side effect",
 "read/exempt commands bypass the lock:",
 "  ENTITY_AVAILABLE, READ_DESCRIPTOR, GET_* (config/name/rate/",
 "  format/stream-info/avb-info), GET_COUNTERS, GET_AS_PATH,",
 "  REGISTER/DEREGISTER_UNSOL, MVU GET_MILAN_INFO, LOCK itself",
], font=10)

grp("g4b", 620, 60, 600, 170, "KL_aecp_timers")
table("t4t", 640, 92, 560, [
 "CLK_FREQ_HZ_P parameter (100e6 AX7101 gateware / 50e6 Arty)",
 "divider -> tick_1khz_o (1-cycle strobe)",
 "lock timer: 60_000 ticks = 60 s, restarted on successful LOCK",
 "counter-gate / stale-tick outputs reserved for HW counters",
], font=10)

grp("g4c", 620, 250, 600, 210, "AEM status codes used (aecp_pkg.sv)")
table("t4s", 640, 282, 560, [
 " 0 SUCCESS            1 NOT_IMPLEMENTED (default echo)",
 " 2 NO_SUCH_DESCRIPTOR (bad type/index; counters/as-path miss)",
 " 3 ENTITY_LOCKED      (lock denial; write while locked-by-other)",
 " 7 BAD_ARGUMENTS      (bad SET value; ENTITY counters)",
 "11 NOT_SUPPORTED      (every ACQUIRE_ENTITY, Milan rule)",
], font=10)
note("n4", 40, 480, 1180, 60,
 "A rejected command's response keeps the ORIGINAL command's echo shape (SET_NAME error echoes 72 B; unknown commands echo their "
 "whole payload with NOT_IMPLEMENTED) — l0_reject_q selects the echo segment lengths in the builder's DECIDE_S.")

# ======================================================================= #
# PAGE 5 — response builder
# ======================================================================= #
page("5-response-builder", h=1120)
box("t5", 40, 12, 1180, 30,
    "KL_aecp_response_builder — command classify, segment engine, frame serialiser   (hdl/aecp/KL_aecp_response_builder.sv)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g5a", 40, 60, 560, 230, "FSM (state_t)")
table("t5f", 60, 92, 520, [
 "IDLE_S       wait hdr_valid from the parser",
 "CAPTURE_S    payload -> buf_r[0..63]  (u/cmd at buf[0..1],",
 "             command payload from buf[2])",
 "DECIDE_S     1 cycle: classify command_type; program <=4 segments;",
 "             set status_q + cdl_q  (tables below)",
 "WRITE_S      SET_* only: buf_r[wb_src..] -> store[wb_addr..]",
 "EMIT_ADDR_S  present store/const address (1-cycle store latency)",
 "EMIT_DATA_S  byte -> little-lane beat packer (8 B/beat, pad to 60)",
 "CONCLUDE_S   resp_count++, pop the ingress req",
], font=10)

grp("g5b", 620, 60, 600, 230, "segment engine — payload after byte 38")
table("t5seg", 640, 92, 560, [
 "4 descriptors: {kind[1:0], addr[15:0], len[15:0]}",
 "",
 "SEG_NONE   emit 0x00 x len         (zero-fill; counters block)",
 "SEG_ECHO   emit buf_r[addr..+len]  (echo command payload)",
 "SEG_STORE  emit store via dyn_mux  (descriptor/name bytes)",
 "SEG_CONST  emit const_q[addr..]    (fixed words, 64 B pool)",
 "",
 "CDL = 12 + sum(seg_len) = frame_len - 26  (IEEE 1722-2016 5.4",
 "counts octets AFTER target_entity_id; tsn-gen's frame-18",
 "CDL model is WRONG — do not use it as the CDL oracle)",
], font=10)

grp("g5c", 40, 310, 1180, 190, "response frame — byte map (little lane out: tdata[7:0] = first wire byte)")
table("t5hdr", 60, 342, 1140, [
 "byte 0-5  dst = req_src_mac (ingress capture)   byte 18-25  target_entity_id = OUR entity_id",
 "byte 6-11 src = station_mac                     byte 26-33  controller_entity_id (echo)",
 "byte 12-13 0x22F0                               byte 34-35  sequence_id (echo)",
 "byte 14   0xFB                                  byte 36-37  {u, command_type} (echo)   [AEM]",
 "byte 15   {sv=0, ver=0, msg_type = command+1}               VU: protocol_id spans 36-41",
 "byte 16   {status[4:0], cdl[10:8]}   byte 17 cdl[7:0]       byte 38+  segments",
 "runt frames zero-padded to 60 B on the wire; CDL counts the unpadded length",
], font=10)

grp("g5d", 40, 520, 1180, 440, "command programs (DECIDE_S) — segments and CDL, straight from the RTL")
table("t5cmd", 60, 552, 1140, [
 "command                    status          payload segments (after the 12 echo-header octets)      CDL",
 "ENTITY_AVAILABLE 0x0002    SUCCESS         (none)                                                   12",
 "ACQUIRE 0x0000             NOT_SUPPORTED   ECHO flags+owner_id+type+idx (16 B)                      28",
 "LOCK 0x0001                grant/LOCKED    ECHO flags(4) + CONST owner_eid(8) + ECHO type+idx(4)    28",
 "READ_DESCRIPTOR 0x0004     SUCCESS         ECHO cfg+rsvd(4) + STORE desc[base .. base+len-1]        16+len",
 "READ_DESCRIPTOR (bad idx)  NO_SUCH_DESC    ECHO cfg+rsvd+type+idx (8 B)                          20",
 "GET/SET_CONFIGURATION      SUCCESS/BAD_ARG CONST rsvd(2) + current_config(2)                        16",
 "GET/SET_NAME 0x19/0x18     SUCCESS         ECHO type+idx+nameidx+cfg(8) + STORE name[wb_addr,64]    84",
 "GET/SET_SAMPLING_RATE      SUCCESS/BAD_ARG ECHO type+idx(4) + STORE rate@534(4)                     20",
 "GET/SET_STREAM_FORMAT      SUCCESS/BAD_ARG ECHO type+idx(4) + STORE fmt@628(8)                      24",
 "GET_STREAM_INFO 0x000F     SUCCESS         ECHO(4) + CONST 52 B (flags 0xF6000000, fmt, zeros)      68",
 "                                           Milan FIXED 56-byte payload — la_avdecc rejects short",
 "GET_AVB_INFO 0x0027        SUCCESS         ECHO(4) + CONST gm+delay+domain+flags+msrp_count (16)    32",
 "GET_AS_PATH 0x0028         SUCCESS         ECHO idx(2) + CONST count=1 + clock_id EUI64 (10)        24",
 "GET_COUNTERS 0x0029        SUCCESS         ECHO(4) + CONST valid(4) + NONE 128 B zero block        148",
 "                                           valid: STREAM_OUTPUT=0x1F, AVB_INTERFACE=0x23;",
 "                                           FULL 136 B payload on error statuses too",
 "REGISTER/DEREGISTER_UNSOL  SUCCESS         (none)                                                   12",
 "MVU GET_MILAN_INFO 0x0000  SUCCESS         CONST proto+cmd+rsvd + version=1 + features + cert=0     32",
 "anything else              NOT_IMPLEMENTED ECHO the original payload                                echo",
], font=10)

# ======================================================================= #
# PAGE 6 — store / accessor / dyn_mux
# ======================================================================= #
page("6-aem-store")
box("t6", 40, 12, 1180, 30,
    "KL_aecp_accessor + KL_aecp_aem_store + KL_aecp_aem_dyn_mux — the entity model in BRAM   (gen/aecp_aem_rom.svh, generated)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g6a", 40, 60, 560, 280, "KL_aecp_accessor — descriptor directory (AEM_DIR_C)")
table("t6d", 60, 92, 520, [
 "entry[63:0] = {type[63:48], index[47:32], base[31:16], len[15:0]}",
 "",
 "type    index  base    len   descriptor",
 "0x0000  0      0x000   312   ENTITY",
 "0x0001  0      0x138    86   CONFIGURATION",
 "0x0002  0      0x18E   156   AUDIO_UNIT",
 "0x0006  0      0x22A   156   STREAM_OUTPUT",
 "0x0009  0      0x2C6    98   AVB_INTERFACE",
 "",
 "miss -> acc_found=0 -> NO_SUCH_DESCRIPTOR(2)",
 "ROM image: 808 bytes, network byte order, addr 0 = ENTITY[0]",
], font=10)

grp("g6b", 620, 60, 600, 280, "KL_aecp_aem_store — ROM + volatile SET write-back")
table("t6w", 640, 92, 560, [
 "single byte port: st_addr -> st_byte, 1-cycle latency (the",
 "builder presents the address one state early: EMIT_ADDR_S)",
 "",
 "write-back region (SET_* land here, volatile until reset):",
 "  object_name ENTITY        @  48 (64 B)   group_name @ 180",
 "  object_name CONFIGURATION @ 316",
 "  object_name AUDIO_UNIT    @ 402   sampling_rate @ 534 (4 B)",
 "  object_name STREAM_OUTPUT @ 558   stream_format @ 628 (8 B)",
 "  object_name AVB_INTERFACE @ 714",
 "",
 "validation sets: rates {0xBB80,0x17700,0x2EE00} = 48/96/192 kHz",
 "                 formats: 3 x AAF 64-bit entries (AEM_FMTS_C)",
], font=10)

grp("g6c", 40, 360, 1180, 300, "KL_aecp_aem_dyn_mux — live-field overlay (CSR truth wins over ROM)")
table("t6o", 60, 392, 1140, [
 "read addr in an overlay range -> byte substituted from the live CSR value; otherwise the ROM byte passes",
 "",
 "ENTITY desc        offset 4-11 entity_id    12-19 entity_model_id    20-23 entity_capabilities",
 "                   24-25 talker_stream_sources    26-27 talker_capabilities",
 "                   28-29 listener_stream_sinks    30-31 listener_capabilities",
 "                   32-35 controller_capabilities  36-39 available_index (ADP-coherent!)",
 "                   40-47 association_id           310-311 current_configuration",
 "AVB_INTERFACE desc 782-787 mac_address            790-797 clock_identity",
 "",
 "clock_identity = {MAC[47:24], 0xFFFE, MAC[23:0]} (EUI-64 from MAC, IEEE 1588 rule) — the SAME value",
 "GET_AS_PATH reports as path[0], so descriptor and dynamic info can never disagree.",
 "available_index overlays the advertiser's live counter: READ_DESCRIPTOR(ENTITY) matches the last ADPDU.",
], font=10)

# ======================================================================= #
# PAGE 7 — ADP advertiser
# ======================================================================= #
page("7-adp-advertiser")
box("t7", 40, 12, 1180, 30,
    "adp_advertiser — ENTITY_AVAILABLE / DEPARTING / discover response, byte-exact ADPDU   (hdl/adp/adp_advertiser.sv)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g7a", 40, 60, 620, 420, "82-byte frame — wire byte map (CDL 0x38 = 56, ADPDU = 68 B)")
table("t7f", 60, 92, 580, [
 "byte 0-5    dst = 91:E0:F0:01:00:00 (ADP multicast)",
 "byte 6-11   src = station_mac",
 "byte 12-13  0x22F0        byte 14  subtype 0xFA",
 "byte 15     {sv=0, ver=0, message_type}",
 "            0 AVAILABLE / 1 DEPARTING / 2 DISCOVER",
 "byte 16     {valid_time[4:0], cdl[10:8]}  vt in 2 s units (0x1F=62 s)",
 "byte 17     cdl[7:0] = 0x38",
 "byte 18-25  entity_id                byte 26-33  entity_model_id",
 "byte 34-37  entity_capabilities (0x00008588 = AEM|CLASS_A|gPTP)",
 "byte 38-39  talker_stream_sources    byte 40-41  talker_capabilities",
 "byte 42-43  listener_stream_sinks    byte 44-45  listener_capabilities",
 "byte 46-49  controller_capabilities",
 "byte 50-53  available_index   <-  +1 on EVERY transmitted ADPDU",
 "byte 54-61  gptp_grandmaster_id      byte 62  gptp_domain_number",
 "byte 63     reserved                 byte 64-65  current_config_index",
 "byte 66-67  identify_control_index   byte 68-69  interface_index",
 "byte 70-77  association_id           byte 78-81  reserved",
 "",
 "serialiser: 11 AXIS beats x 8 B, last beat tkeep=0x03 (2 B), little lane",
], font=10)

grp("g7b", 700, 60, 520, 420, "trigger arbitration + the available_index rule")
table("t7t", 720, 92, 480, [
 "one pending send; highest priority wins:",
 "  1. depart  (link_down / shutdown)  -> DEPARTING",
 "  2. link_up                         -> AVAILABLE",
 "  3. info_changed / gm_change (CSR)  -> AVAILABLE",
 "  4. rcv_discover (ingress pulse)    -> AVAILABLE",
 "  5. periodic timer                  -> AVAILABLE",
 "",
 "timer: re-advertise every valid_time s (validity 2x)",
 "tick_i = 1 s strobe from the datapath",
 "datapath glue: an enable-edge with link already up",
 "counts as link_up (boot-order independence)",
], font=10)
note("n7", 720, 320, 480, 150,
 "available_index increments on EVERY transmitted ADPDU —\n"
 "periodic, discover response and departing alike (tx_index_r\n"
 "latched per frame). la_avdecc/Hive treat old >= new as\n"
 "'incoherently changed' and cycle the entity offline/online;\n"
 "the pipewire module-avb reference does available_index++ on\n"
 "every send. Bump-on-change-only was silicon-diagnosed as the\n"
 "trigger and fixed 2026-07-12 (la_avdecc round 2).")

# ======================================================================= #
# PAGE 8 — TX merge + CSR
# ======================================================================= #
page("8-tx-csr")
box("t8", 40, 12, 1180, 30,
    "TX merge + milan_csr — how control frames reach the wire, and the software contract   (hdl/csr/milan_csr.sv)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)

grp("g8a", 40, 60, 560, 200, "two-stage TX merge (adp_tx_arbiter x2)")
table("t8m", 60, 92, 520, [
 "stage 1 (low-rate): ADP advertiser vs AECP responses —",
 "  frame-atomic round-robin, a started frame is never split",
 "stage 2 (datapath): control stream vs DMA TX stream —",
 "  control frames inserted in inter-frame gaps only:",
 "  data keeps line rate, no mid-frame jitter",
 "both 64-bit little-lane AXIS into eth_mac_1g_rgmii",
], font=10)

grp("g8d", 620, 60, 600, 200, "who validates what")
table("t8v", 640, 92, 560, [
 "tb/verilator/aecp       68 checks   unit/subsystem (all commands)",
 "tb/verilator/adp       121 checks   ADPDU byte-exact + index rule",
 "tb/verilator/milan_dp   17 checks   full datapath, NIC regression",
 "cosim tsn-gen <-> RTL   42 checks   independent frame builder",
 "milan_controller.py     24 checks   silicon over the AVB switch",
 "la_avdecc enum-probe    Hive's library, strict enumeration",
 "yosys 19/19 + lint 10/10            device-portability gates",
], font=10)

grp("g8b", 40, 290, 1180, 440, "CSR map — ADP/identity 0x600 + AECP status 0x648 (AXI-Lite, 32-bit)")
table("t8c", 60, 322, 1140, [
 "0x600 ADP_CTRL   [12:8] valid_time (2 s units)  [0] enable      reset 0x00001F00 (enable=0, vt=31)",
 "0x604 ADP_EIDLO  entity_id[31:0]                0x608 ADP_EIDHI  entity_id[63:32]",
 "0x60C ADP_MIDLO  entity_model_id[31:0]          0x610 ADP_MIDHI  entity_model_id[63:32]",
 "0x614 ADP_ECAPS  entity_capabilities — 0x8588; IDENTIFY_INDEX_VALID stays 0 (no CONTROL descriptor;",
 "                 advertising it is a la_avdecc compliance error, found+fixed 2026-07-11)",
 "0x618 ADP_TALK   {[31:16] talker_capabilities, [15:0] talker_stream_sources}    e.g. 0x48010008",
 "0x61C ADP_LIST   {[31:16] listener_capabilities, [15:0] listener_stream_sinks}",
 "0x620 ADP_CCAPS  controller_capabilities",
 "0x624 ADP_GMLO / 0x628 ADP_GMHI   gPTP grandmaster_id      0x62C ADP_DOMAIN [7:0] domain",
 "0x630 ADP_IDX0   {[31:16] identify_control_index, [15:0] current_configuration_index}",
 "0x634 ADP_IDX1   [15:0] interface_index",
 "0x638 ADP_ASLO / 0x63C ADP_ASHI   association_id",
 "0x640 ADP_CMD    W1S strobes, read 0:  [0] advertise-now (+bump)   [1] send DEPARTING",
 "0x644 ADP_STATUS RO: live available_index (advertiser counter)",
 "0x648 AECP_STAT0 RO: [16] locked   [15:0] cmd_count (accepted commands)",
 "0x64C AECP_STAT1 RO: [31:16] resp_count   [15:0] current_configuration",
 "",
 "identity is programmed ONCE before setting ADP_CTRL[0]; ADP and AEM read the same wires, so the",
 "advertised ADPDU and READ_DESCRIPTOR(ENTITY) can never disagree.  Setup: avdecc/aecp_csr_setup.sh.",
], font=10)


# ======================================================================= #
# PAGE 9 — HW / SW split (the softcore delimitation)
# ======================================================================= #
page("9-hw-sw-split", h=1120)
box("t9", 40, 12, 1180, 30,
    "What runs on the softcore and what does not — the delimitation   (normative text: docs/ARCHITECTURE_HW_SW_SPLIT.md)",
    fill="#f5f5f5", stroke="#666", font=14, rounded=0)
box("t9p", 40, 50, 1180, 46,
    "The fabric ANSWERS, the softcore DECIDES.  Fabric = per-frame / line-rate / liveness-with-deadlines / wire-format truth."
    "  Softcore = negotiation, policy, long-lived state, media production, once-per-boot provisioning.",
    fill="#fff9d6", stroke="#b3a100", font=11, align="left")

grp("g9h", 40, 110, 560, 620, "FPGA fabric — always on, zero-CPU  (green=silicon, orange=next)")
box("h1", 60, 142, 520, 40, "MAC 1G RGMII/GMII + TCAM dest-MAC filter", fill="#d5e8d4", stroke="#82b366", font=10)
box("h2", 60, 190, 520, 40, "802.1Q classifier + CBS shaper + queues  (never removed - user rule)", fill="#d5e8d4", stroke="#82b366", font=10)
box("h3", 60, 238, 520, 40, "PTP timestamp counter + RX/TX capture -> DMA ts window", fill="#d5e8d4", stroke="#82b366", font=10)
box("h4", 60, 286, 520, 40, "RX DMA: RSC coalescing / header-split / multi-slot  +  HW-TSO", fill="#d5e8d4", stroke="#82b366", font=10)
box("h5", 60, 334, 520, 52, "ADP advertiser — periodic/depart/discover, available_index +1 every" + "\n" + "ADPDU  (la_avdecc-clean, silicon)", fill="#d5e8d4", stroke="#82b366", font=10)
box("h6", 60, 394, 520, 52, "AECP/AEM entity — 5 descriptors, full Milan 5.4.4 command set," + "\n" + "LOCK 60 s, ROM+overlay store  (la_avdecc-clean, silicon)", fill="#d5e8d4", stroke="#82b366", font=10)
box("h7", 60, 454, 520, 52, "ACMP stateless responder — GET_TX_STATE / GET_TX_CONNECTION," + "\n" + "connection_count=0   << NEXT: the Milan=1 gate >>", fill="#ffe6cc", stroke="#d79b00", font=10)
box("h8", 60, 514, 520, 40, "low-rate TX merge arbiters (control into inter-frame gaps)", fill="#d5e8d4", stroke="#82b366", font=10)
box("h9", 60, 562, 520, 52, "future: fabric ACMP connection TABLE (SW-written via mailbox; fabric" + "\n" + "answers all state queries zero-CPU)", fill="#f5f5f5", stroke="#999", font=10)
box("h10", 60, 622, 520, 52, "optional later offload: fabric AAF framer — only if PipeWire-crafted" + "\n" + "frames cannot hold class-A cadence (NOT plan of record)", fill="#f5f5f5", stroke="#999", font=10)

grp("g9s", 660, 110, 560, 620, "VexiiRiscv softcore (Linux) — decides, provisions, produces")
box("s1", 680, 142, 520, 40, "kl-eth driver — rings, NAPI, ethtool, CSR  (silicon)", fill="#d5e8d4", stroke="#82b366", font=10)
box("s2", 680, 190, 520, 40, "identity provisioning ONCE per boot (0x600 group, caps 0x8588)", fill="#d5e8d4", stroke="#82b366", font=10)
box("s3", 680, 238, 520, 52, "kl-eth PHC /dev/ptpN + SO_TIMESTAMPING — expose the fabric clock" + "\n" + "to linuxptp   << NEXT (gPTP gate) >>", fill="#ffe6cc", stroke="#d79b00", font=10)
box("s4", 680, 298, 520, 52, "gPTP protocol: linuxptp ptp4l (BMCA, servo, pdelay) + phc2sys —" + "\n" + "in the rootfs today, unvalidated until the PHC lands", fill="#fff2cc", stroke="#d6b656", font=10)
box("s5", 680, 358, 520, 52, "gPTP->entity bridge: GM id/domain -> CSR 0x624/0x628 on change" + "\n" + "(fabric reacts: gm_change -> re-advertise + index bump + AS_PATH truth)", fill="#f5f5f5", stroke="#999", font=10)
box("s6", 680, 418, 520, 52, "ACMP connection POLICY — accept/refuse CONNECT_TX via mailbox+IRQ," + "\n" + "write the fabric connection table  (future)", fill="#f5f5f5", stroke="#999", font=10)
box("s7", 680, 478, 520, 40, "SRP/MSRP state machines (pipewire module-avb)  (future)", fill="#f5f5f5", stroke="#999", font=10)
box("s8", 680, 526, 520, 52, "AVTP media: PipeWire module-avb crafts AAF frames -> kl-eth ->" + "\n" + "fabric CBS class-A queue  (future; plan of record)", fill="#f5f5f5", stroke="#999", font=10)
box("s9", 680, 586, 520, 40, "perf lanes: AF_XDP ZC, NAPI tuning (existing campaigns)", fill="#f5f5f5", stroke="#999", font=10)

grp("g9b", 40, 750, 1180, 220, "boundary contracts — the ONLY crossings")
table("t9b", 60, 782, 1140, [
 "1. CSR 0x600 group -- identity+control, SW writes once (then only on real changes: GM change, config).",
 "   ADP and AEM read the SAME wires -> wire truth cannot diverge. RO: 0x644 avail_idx, 0x648/0x64C.",
 "2. DMA rings + ts  -- the data plane; every frame + per-frame HW timestamps in descriptors.",
 "3. PHC clock ops   -- (next) fabric counter as /dev/ptpN; ptp4l disciplines it, phc2sys mirrors REALTIME.",
 "4. mailbox + IRQ   -- (future, ACMP connections) fabric posts what it cannot answer alone; SW replies",
 "   via the connection table; fabric answers every later state query without SW.",
], font=10)

# ----------------------------------------------------------------------- #
# emit the mxfile
# ----------------------------------------------------------------------- #
out = ['<mxfile host="app.diagrams.net">']
for name, cl, w, h in PAGES:
    out.append(f'<diagram name="{name}">'
               f'<mxGraphModel dx="1400" dy="1000" grid="0" gridSize="10" guides="1" tooltips="1" '
               f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" '
               f'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
               + "".join(cl) +
               '</root></mxGraphModel></diagram>')
out.append('</mxfile>')
open(sys.argv[1], "w").write("".join(out))
print("wrote", sys.argv[1], f"({len(PAGES)} pages,", sum(len(c) for _, c, _, _ in PAGES), "cells)")

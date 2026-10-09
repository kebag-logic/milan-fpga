# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit KL_mbx.sv, the fabric skeleton of the packet mailbox.

The skeleton is the part of the fabric the contract fixes: the port list, the
register decode (a storage register for every ``rw`` register, a pulse for
every ``wo`` register, a read for every readable one), the read multiplexer
and one ring instance per direction per channel. The bound-talker registers
are the exception: the skeleton decodes them and ``KL_mbx_rx`` holds them, in
distributed RAM beside the compare that reads them. The publication block is
decoded and held here, and each of its fields leaves on a ``pub_*_o`` port
named in ``PUB_OUTPUTS``, for the datapath of the split placement. The leaves it instantiates
(``KL_mbx_ring``, ``KL_mbx_rx``, ``KL_mbx_tx``, ``KL_mbx_evt``) are written by
hand against ``KL_mbx_pkg`` and are the same for every contract.

A read-only field needs a fabric source. ``RO_SOURCES`` names the signal for
each one; a register added to the YAML with no source here is refused, so the
contract can never describe a field the skeleton silently reads as zero.
"""

from __future__ import annotations

from mailbox_emit import GENERATOR, SOURCE
from mailbox_model import Contract, ContractError, Register

#: Read-only global fields: register -> field -> SystemVerilog source.
RO_SOURCES = {
    "ID": {"MINOR": "MBX_VERSION_MINOR_C", "MAJOR": "MBX_VERSION_MAJOR_C", "MAGIC": "MBX_MAGIC_C"},
    "CAPS": {"N_CH": "MBX_N_CH_C", "N_IF": "MBX_N_IF_C", "N_TIMERS": "MBX_N_TIMERS_C",
             "EVT_WORDS_LOG2": "$clog2(MBX_EVT_WORDS_C)"},
    "IRQ_STATUS": {"RX": "rx_pending_w", "EVT": "evt_pending_w", "ERR": "err_r"},
    "NOW_MS": {"MS": "now_ms_r"},
    "LINK": {"UP": "link_up_i"},
    "EVT_HEAD": {"WORDS": "evt_head_w"},
    "BUS_ERR": {"COUNT": "bus_err_r"},
    "FILTER_MISMATCH": {"COUNT": "filter_mismatch_w"},
}

#: The interface filter registers the skeleton wires into KL_mbx_rx's own_mac_i:
#: register -> the MAC bits its one field carries, as (msb, lsb).
OWN_MAC_BITS = {"OWN_MAC_HI": (47, 32), "OWN_MAC_LO": (31, 0)}

#: The bound-talker registers KL_mbx_rx holds behind the skeleton's decode:
#: register -> the bits its one field carries, as (msb, lsb).
BOUND_BITS = {"BOUND_EID_HI": (63, 32), "BOUND_EID_LO": (31, 0), "BOUND_EN": (0, 0)}

#: The code KL_mbx_rx's bnd_reg_i gives each bound-talker register.
BOUND_CODE = {"BOUND_EID_LO": 0, "BOUND_EID_HI": 1, "BOUND_EN": 2}

#: The publication block's interface fields, each on a port of its own:
#: (register, field) -> (port, the port's bits per interface).
PUB_OUTPUTS = {
    ("DA_GATE", "OPEN"): ("pub_da_gate_o", "MBX_N_PUB_SOURCES_C"),
    ("LICENCE", "ACTIVE"): ("pub_licence_o", "MBX_N_PUB_SOURCES_C"),
    ("IDLE_SLOPE", "BPS"): ("pub_idle_slope_o", "MBX_IDLE_SLOPE_BPS_WIDTH_C"),
    ("SR_DOMAIN", "VID"): ("pub_dom_vid_o", "MBX_SR_DOMAIN_VID_WIDTH_C"),
    ("SR_DOMAIN", "PRIORITY"): ("pub_dom_prio_o", "MBX_SR_DOMAIN_PRIORITY_WIDTH_C"),
    ("SR_DOMAIN", "ADOPTED"): ("pub_dom_adopted_o", "MBX_SR_DOMAIN_ADOPTED_WIDTH_C"),
}

#: The publication block's sink fields: BINDING.BOUND on pub_bound_o, one bit a
#: sink, and the stream_id on pub_sid_o, 64 bits a sink, 0 while SID_VALID is clear.
PUB_SINK_FIELDS = {"SID_LO": ("SID",), "SID_HI": ("SID",), "BINDING": ("BOUND", "SID_VALID")}

#: Read-only interface fields; `{i}` is the interface index.
IF_SOURCES = {
    "GM_LO": {"ID": "gm_id_i[64*{i} +: 32]"},
    "GM_HI": {"ID": "gm_hi_snap_r[{i}]"},
    "DOMAIN": {"NUMBER": "domain_snap_r[{i}]"},
}

#: Read-only channel fields; `{c}` is the channel id.
CH_SOURCES = {
    "RX_HEAD": {"WORDS": "rx_head_w[16*{c} +: 16]"},
    "TX_TAIL": {"WORDS": "tx_tail_w[16*{c} +: 16]"},
    "RX_DROP": {"COUNT": "rx_drop_w[16*{c} +: 16]"},
    "RATE_DROP": {"COUNT": "rate_drop_w[16*{c} +: 16]"},
    "TX_ERR": {"COUNT": "tx_err_w[16*{c} +: 16]"},
    "RX_PASS": {"COUNT": "rx_pass_w[16*{c} +: 16]"},
}

#: The rw1c fields a write of 1 clears; every other rw1c field is a level.
STICKY = {("IRQ_STATUS", "ERR"): "err_r"}

AW = "AW2_C"   # the byte-offset width localparam inside KL_mbx


def _place(reg: str, fld: str, src: str) -> str:
    """A source placed into its field of a 32-bit register."""
    return f"mbx_place_f(32'({src}), MBX_{reg}_{fld}_LSB_C, MBX_{reg}_{fld}_WIDTH_C)"


def _mask(reg: Register) -> str:
    """The union of a register's field masks, from the constants."""
    return " | ".join(f"mbx_place_f(32'hFFFF_FFFF, MBX_{reg.name}_{f.name}_LSB_C, MBX_{reg.name}_{f.name}_WIDTH_C)"
                      for f in reg.fields)


def _bits(reg: Register) -> int:
    """The register's width up to its highest field bit: what storage of it keeps."""
    return max(f.lsb + f.width for f in reg.fields)


def _sources(reg: Register, table: dict[str, dict[str, str]], fmt: dict[str, int]) -> str:
    """The read value of a read-only register, every field from its source."""
    srcs = table.get(reg.name)
    if srcs is None or set(srcs) != {f.name for f in reg.fields}:
        raise ContractError(f"register {reg.name}: the skeleton has no fabric source for every field")
    return " | ".join(_place(reg.name, f.name, srcs[f.name].format(**fmt)) for f in reg.fields)


def _banner() -> list[str]:
    """The file banner."""
    return [
        "// SPDX-FileCopyrightText: 2026 Kebag Logic",
        "// SPDX-License-Identifier: CERN-OHL-W-2.0",
        "//",
        f"// GENERATED by {GENERATOR} from {SOURCE}; DO NOT EDIT.",
        f"// Regenerate with: python3 {GENERATOR} --write",
        "//---------------------------------------------------------------------------//",
        "//  File        : KL_mbx.sv",
        "//  Project     : Milan FPGA Platform (packet mailbox, #665 lane F0)",
        "//",
        "//  Description : The fabric skeleton of the packet mailbox: the host",
        "//                window (registers, receive rings and the event ring to read,",
        "//                transmit rings to write), the ingress filter feeding the RX",
        "//                rings, the TX merge draining the transmit rings, the fabric",
        "//                timers and the event poster, and the one interrupt.",
        "//                Reachable only behind the SoC's default-off mailbox",
        "//                switch; the default build never elaborates it.",
        "//",
        "//                The one decision that matters: the host port answers",
        "//                every request exactly one cycle later, so a bus adapter",
        "//                (KL_mbx_wb, KL_mbx_axil) holds one request in flight and",
        "//                adds nothing to the contract. A write without all four",
        "//                byte strobes is refused and counted in BUS_ERR.",
        "//---------------------------------------------------------------------------//",
        "",
        "`default_nettype none",
        "",
    ]


def _ports() -> list[str]:
    """The module header and port list."""
    return [
        "module KL_mbx",
        "  import KL_mbx_pkg::*;",
        "(",
        "  input  wire                          clk_i,          //! the mailbox clock: host port and fabric side",
        "  input  wire                          rst_n,          //! synchronous active-low reset",
        "",
        "  input  wire                          host_req_i,     //! a host access this cycle",
        "  input  wire                          host_we_i,      //! the access is a write",
        "  input  wire  [MBX_ADDR_W_C-1:0]      host_addr_i,    //! word address inside the window",
        "  input  wire  [31:0]                  host_wdata_i,   //! write data",
        "  input  wire  [3:0]                   host_be_i,      //! byte strobes; a write without all four is refused",
        "  output logic                         host_ack_o,     //! the access completes, one cycle after host_req_i",
        "  output logic [31:0]                  host_rdata_o,   //! read data, valid with host_ack_o",
        "  output logic                         irq_o,          //! the interrupt: OR of IRQ_STATUS AND IRQ_ENABLE",
        "",
        "  input  wire                          ms_tick_p_i,    //! one-cycle pulse per millisecond (NOW_MS)",
        "  input  wire  [MBX_N_IF_C-1:0]        link_up_i,      //! link level per interface",
        "  input  wire  [MBX_N_IF_C-1:0]        gm_change_p_i,  //! one-cycle pulse per interface: grandmaster change",
        "  input  wire  [MBX_N_IF_C*64-1:0]     gm_id_i,        //! gptp_grandmaster_id per interface",
        "  input  wire  [MBX_N_IF_C*8-1:0]      gptp_domain_i,  //! gptp_domain_number per interface",
        "",
        "  input  wire                          rx_valid_i,     //! ingress: a frame byte is offered",
        "  output logic                         rx_ready_o,     //! ingress: the byte is taken this cycle",
        "  input  wire  [7:0]                   rx_data_i,      //! ingress: the byte, wire order",
        "  input  wire                          rx_last_i,      //! ingress: the frame's last byte (no FCS)",
        "  input  wire  [MBX_IF_W_C-1:0]        rx_if_i,        //! ingress: interface, held for the frame",
        "",
        "  output logic                         tx_valid_o,     //! egress: a frame byte is offered",
        "  input  wire                          tx_ready_i,     //! egress: the byte is taken this cycle",
        "  output logic [7:0]                   tx_data_o,      //! egress: the byte, wire order",
        "  output logic                         tx_last_o,      //! egress: the frame's last byte",
        "  output logic [MBX_IF_W_C-1:0]        tx_if_o,        //! egress: interface, held for the frame",
        "  output logic [MBX_CH_W_C-1:0]        tx_ch_o,        //! egress: channel, held for the frame",
        "",
    ]


def _pub_ports() -> list[str]:
    """The publication block's outputs, which close the port list: interface i's
    field takes bits [width*i +: width], and sink k of interface i is entry
    N_PUB_SINKS*i + k."""
    out = ["  // the publication block, what the firmware owner publishes for the datapath"]
    for (reg, fld), (port, width) in PUB_OUTPUTS.items():
        out.append(f"  output logic [MBX_N_IF_C*{width}-1:0] {port},   //! {reg}.{fld} per interface")
    out += ["  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C-1:0] pub_bound_o,   //! BINDING.BOUND per sink",
            "  output logic [MBX_N_IF_C*MBX_N_PUB_SINKS_C*64-1:0] pub_sid_o   "
            "//! SID_HI:SID_LO per sink, 0 while BINDING.SID_VALID is clear",
            ");",
            "",
            "  localparam int unsigned AW2_C = MBX_ADDR_W_C + 2;   //! byte-offset width",
            "",
            ]
    return out


def _core() -> list[str]:
    """NOW_MS, the request decode and the signals the leaves drive."""
    return [
        "  // ---- NOW_MS --------------------------------------------------------------",
        "  logic [31:0] now_ms_r;",
        "  always_ff @(posedge clk_i) begin : now_ms",
        "    if (!rst_n) now_ms_r <= '0;",
        "    else if (ms_tick_p_i) now_ms_r <= now_ms_r + 32'd1;",
        "  end : now_ms",
        "",
        "  // ---- the request -------------------------------------------------------------",
        f"  logic [{AW}-1:0] off_w;      //! byte offset of the access",
        "  logic             wr_w;       //! an accepted write",
        "  logic             rd_w;       //! a read",
        "  logic             refused_w;  //! a write refused for a partial strobe",
        "  assign off_w     = {host_addr_i, 2'b00};",
        "  assign wr_w      = host_req_i && host_we_i && (host_be_i == 4'hF);",
        "  assign rd_w      = host_req_i && !host_we_i;",
        "  assign refused_w = host_req_i && host_we_i && (host_be_i != 4'hF);",
        "",
        "  // ---- what the leaves drive ------------------------------------------------------",
        "  logic [MBX_N_CH_C*16-1:0] rx_head_w;",
        "  logic [MBX_N_CH_C*16-1:0] rx_drop_w;",
        "  logic [MBX_N_CH_C*16-1:0] rate_drop_w;",
        "  logic [MBX_N_CH_C*16-1:0] rx_pass_w;",
        "  logic [MBX_N_CH_C*16-1:0] tx_tail_w;",
        "  logic [MBX_N_CH_C*16-1:0] tx_err_w;",
        "  logic [MBX_N_CH_C*16-1:0] rx_tail_w;",
        "  logic [MBX_N_CH_C*16-1:0] tx_head_w;",
        "  logic [15:0]              evt_head_w;",
        "  logic                     rx_err_p_w;",
        "  logic                     tx_err_p_w;",
        "  logic                     tmr_bad_p_w;",
        "  logic                     rxw_en_w;",
        "  logic [MBX_CH_W_C-1:0]    rxw_ch_w;",
        "  logic [MBX_RING_AW_C-1:0] rxw_addr_w;",
        "  logic [31:0]              rxw_data_w;",
        "  logic                     txr_en_w;",
        "  logic [MBX_CH_W_C-1:0]    txr_ch_w;",
        "  logic [MBX_RING_AW_C-1:0] txr_addr_w;",
        "  logic                     evw_en_w;",
        "  logic [$clog2(MBX_EVT_WORDS_C)-1:0] evw_addr_w;",
        "  logic [31:0]              evw_data_w;",
        "  logic [MBX_N_CH_C-1:0]    rx_pending_w;",
        "  logic                     evt_pending_w;",
        "  logic [15:0]              filter_mismatch_w;",
        "  logic [MBX_N_IF_C*48-1:0] own_mac_w;      //! OWN_MAC per interface, the filter's `own` destination",
        "  logic [31:0]              bnd_eid_w;      //! the BOUND_EID word an access names, as KL_mbx_rx stores it",
        "  logic                     bnd_eid_vld_w;  //! that word was written since the reset (else it reads 0)",
        "  logic                     bnd_en_w;       //! the BOUND_EN of the entry an access names",
        "",
    ]


def _bound_decode(contract: Contract) -> list[str]:
    """The bound-talker register an offset names: its interface, entry and
    register by the bit fields of the offset, the strides being powers of two."""
    named = " || ".join(f"in_entry == {AW}'(MBX_BND_REG_{name}_C)" for name in BOUND_CODE)
    out = ["  // ---- the bound-talker tables: decoded here, held by KL_mbx_rx -------------------",
           "  // The strides are powers of two, so an offset's interface and entry are",
           "  // its bit fields; a hole between the registers names none.",
           "  logic                  bnd_at_w;      //! the offset names a bound-talker register",
           "  logic [MBX_IF_W_C-1:0] bnd_if_w;      //! its interface",
           "  logic [4:0]            bnd_entry_w;   //! its entry (bound_talkers is at most 32)",
           "  logic [1:0]            bnd_reg_w;     //! 0 BOUND_EID_LO, 1 BOUND_EID_HI, 2 BOUND_EN",
           "  always_comb begin : bound_decode",
           f"    logic [{AW}-1:0] rel;",
           f"    logic [{AW}-1:0] in_entry;",
           f"    logic [{AW}-1:0] entry;",
           f"    rel         = off_w - {AW}'(MBX_BND_BASE_C);",
           f"    in_entry    = rel & {AW}'(MBX_BND_ENTRY_STRIDE_C - 1);",
           f"    entry       = (rel & {AW}'(MBX_BND_STRIDE_C - 1)) >> $clog2(MBX_BND_ENTRY_STRIDE_C);",
           "    bnd_if_w    = MBX_IF_W_C'(rel >> $clog2(MBX_BND_STRIDE_C));",
           "    bnd_entry_w = 5'(entry);",
           "    bnd_reg_w   = '0;"]
    for name, code in BOUND_CODE.items():
        if code:
            out.append(f"    if (in_entry == {AW}'(MBX_BND_REG_{name}_C)) bnd_reg_w = 2'd{code};")
    out += [f"    bnd_at_w    = off_w >= {AW}'(MBX_BND_BASE_C)",
            f"                  && (rel >> $clog2(MBX_BND_STRIDE_C)) < {AW}'(MBX_N_IF_C)",
            f"                  && entry < {AW}'(MBX_N_BOUND_C)",
            f"                  && ({named});",
            "  end : bound_decode",
            ""]
    return out


def _pub_decode(contract: Contract) -> list[str]:
    """The publication register an offset names: its interface, whether it is a
    sink entry's, the entry, and its offset inside the block or the entry, by
    the bit fields of the offset, the strides being powers of two."""
    regs = " || ".join(f"pub_reg_w == {AW}'(MBX_PUB_REG_{r.name}_C)" for r in contract.pub_registers)
    sinks = " || ".join(f"pub_reg_w == {AW}'(MBX_PUB_SINK_REG_{r.name}_C)" for r in contract.pub_sink_registers)
    return ["  // ---- the publication block: decoded and held here, read by the datapath -----------",
            "  // The strides are powers of two, so an offset's interface and sink entry",
            "  // are its bit fields; a hole between the registers names none.",
            "  localparam int unsigned PUB_KW_C = (MBX_N_PUB_SINKS_C > 1) ? $clog2(MBX_N_PUB_SINKS_C) : 1;"
            "   //! sink index bits",
            "  logic                  pub_at_w;     //! the offset names a publication register",
            "  logic                  pub_sink_w;   //! a sink entry's register, else an interface register",
            "  logic [MBX_IF_W_C-1:0] pub_if_w;     //! its interface",
            "  logic [PUB_KW_C-1:0]   pub_k_w;      //! its sink entry",
            f"  logic [{AW}-1:0]      pub_reg_w;    //! its offset inside the interface block or the sink entry",
            "  always_comb begin : pub_decode",
            f"    logic [{AW}-1:0] rel;",
            f"    logic [{AW}-1:0] in_if;",
            f"    logic [{AW}-1:0] in_sinks;",
            f"    logic [{AW}-1:0] entry;",
            f"    rel        = off_w - {AW}'(MBX_PUB_BASE_C);",
            f"    in_if      = rel & {AW}'(MBX_PUB_STRIDE_C - 1);",
            f"    in_sinks   = in_if - {AW}'(MBX_PUB_SINK_BASE_C);",
            "    entry      = in_sinks >> $clog2(MBX_PUB_SINK_STRIDE_C);",
            "    pub_if_w   = MBX_IF_W_C'(rel >> $clog2(MBX_PUB_STRIDE_C));",
            f"    pub_sink_w = in_if >= {AW}'(MBX_PUB_SINK_BASE_C);",
            "    pub_k_w    = PUB_KW_C'(entry);",
            f"    pub_reg_w  = pub_sink_w ? (in_sinks & {AW}'(MBX_PUB_SINK_STRIDE_C - 1)) : in_if;",
            f"    pub_at_w   = off_w >= {AW}'(MBX_PUB_BASE_C)",
            f"                 && (rel >> $clog2(MBX_PUB_STRIDE_C)) < {AW}'(MBX_N_IF_C)",
            f"                 && (pub_sink_w ? (entry < {AW}'(MBX_N_PUB_SINKS_C) && ({sinks}))",
            f"                                : ({regs}));",
            "  end : pub_decode",
            ""]


def _pub_block(contract: Contract) -> list[str]:
    """The publication registers: storage per interface and per sink, the host
    writes, and the outputs the datapath reads."""
    out = ["  // ---- the publication registers: the firmware writes them, the datapath reads them ---"]
    for r in contract.pub_registers:
        out.append(f"  logic [{_bits(r) - 1}:0] pub_{r.name.lower()}_r [MBX_N_IF_C];   //! {r.name} per interface")
    for r in contract.pub_sink_registers:
        out.append(f"  logic [{_bits(r) - 1}:0] pub_{r.name.lower()}_r [MBX_N_IF_C][MBX_N_PUB_SINKS_C];"
                   f"   //! {r.name} per sink")
    out += ["", "  always_ff @(posedge clk_i) begin : pub_write", "    if (!rst_n) begin",
            "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin"]
    out += [f"        pub_{r.name.lower()}_r[i] <= '0;" for r in contract.pub_registers]
    out.append("        for (int k = 0; k < int'(MBX_N_PUB_SINKS_C); k++) begin")
    out += [f"          pub_{r.name.lower()}_r[i][k] <= '0;" for r in contract.pub_sink_registers]
    out += ["        end", "      end", "    end else if (wr_w && pub_at_w) begin"]
    for r in contract.pub_registers:
        out.append(f"      if (!pub_sink_w && pub_reg_w == {AW}'(MBX_PUB_REG_{r.name}_C))")
        out.append(f"        pub_{r.name.lower()}_r[pub_if_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));")
    for r in contract.pub_sink_registers:
        out.append(f"      if (pub_sink_w && pub_reg_w == {AW}'(MBX_PUB_SINK_REG_{r.name}_C))")
        out.append(f"        pub_{r.name.lower()}_r[pub_if_w][pub_k_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));")
    out += ["    end", "  end : pub_write", "",
            "  always_comb begin : pub_out",
            "    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin"]
    for (reg, fld), (port, width) in PUB_OUTPUTS.items():
        field = (f"mbx_field_f(32'(pub_{reg.lower()}_r[i]), MBX_{reg}_{fld}_LSB_C, MBX_{reg}_{fld}_WIDTH_C)")
        out.append(f"      {port}[{width}*i +: {width}] = {width}'({field});")
    valid = "mbx_field_f(32'(pub_binding_r[i][k]), MBX_BINDING_SID_VALID_LSB_C, MBX_BINDING_SID_VALID_WIDTH_C)"
    bound = "mbx_field_f(32'(pub_binding_r[i][k]), MBX_BINDING_BOUND_LSB_C, MBX_BINDING_BOUND_WIDTH_C)"
    out += ["      for (int k = 0; k < int'(MBX_N_PUB_SINKS_C); k++) begin",
            f"        pub_bound_o[MBX_N_PUB_SINKS_C*i + k] = {bound} != 0;",
            f"        pub_sid_o[64*(MBX_N_PUB_SINKS_C*i + k) +: 64] = ({valid} != 0)",
            "            ? {pub_sid_hi_r[i][k], pub_sid_lo_r[i][k]} : 64'd0;",
            "      end", "    end", "  end : pub_out", ""]
    return out


def _storage(contract: Contract) -> list[str]:
    """Declarations of every register the host writes, and the sticky state."""
    out = ["  // ---- what the host writes -----------------------------------------------------"]
    for reg in contract.registers:
        if reg.access == "rw":
            out.append(f"  logic [31:0] {reg.name.lower()}_r;   //! {reg.name}")
        if reg.access == "wo":
            out.append(f"  logic        {reg.name.lower()}_p_w;   //! {reg.name} written this cycle")
    for reg in contract.ch_registers:
        if reg.access == "rw":
            out.append(f"  logic [15:0] {reg.name.lower()}_r [MBX_N_CH_C];   //! {reg.name} per channel")
    for reg in contract.iff_registers:
        if reg.access == "rw":
            out.append(f"  logic [{_bits(reg) - 1}:0] {reg.name.lower()}_r [MBX_N_IF_C];"
                       f"   //! {reg.name} per interface")
    out += [
        "  logic        err_r;                          //! IRQ_STATUS.ERR, sticky",
        "  logic [15:0] bus_err_r;                      //! BUS_ERR",
        "  logic [31:0] gm_hi_snap_r  [MBX_N_IF_C];     //! GM_HI, snapshot taken by a GM_LO read",
        "  logic [7:0]  domain_snap_r [MBX_N_IF_C];     //! DOMAIN, snapshot taken by a GM_LO read",
        "",
    ]
    for reg in contract.registers:
        if reg.access == "wo":
            out.append(f"  assign {reg.name.lower()}_p_w = wr_w && (off_w == {AW}'(MBX_REG_{reg.name}_C));")
    out.append("")
    return out


def _write_block(contract: Contract) -> list[str]:
    """The always_ff that applies host writes, the sticky error and the snapshots."""
    rw = [r for r in contract.registers if r.access == "rw"]
    ch_rw = [r for r in contract.ch_registers if r.access == "rw"]
    iff_rw = [r for r in contract.iff_registers if r.access == "rw"]
    out = ["  always_ff @(posedge clk_i) begin : host_write", "    if (!rst_n) begin"]
    out += [f"      {r.name.lower()}_r <= '0;" for r in rw]
    out += ["      err_r     <= 1'b0;", "      bus_err_r <= '0;",
            "      for (int c = 0; c < int'(MBX_N_CH_C); c++) begin"]
    out += [f"        {r.name.lower()}_r[c] <= '0;" for r in ch_rw]
    out += ["      end", "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
            "        gm_hi_snap_r[i]  <= '0;", "        domain_snap_r[i] <= '0;"]
    out += [f"        {r.name.lower()}_r[i] <= '0;" for r in iff_rw]
    out += ["      end", "    end else begin"]
    for r in rw:
        out.append(f"      if (wr_w && off_w == {AW}'(MBX_REG_{r.name}_C))"
                   f" {r.name.lower()}_r <= host_wdata_i & ({_mask(r)});")
    out.append("      for (int c = 0; c < int'(MBX_N_CH_C); c++) begin")
    for r in ch_rw:
        out.append(f"        if (wr_w && off_w == {AW}'(MBX_CH_BASE_C + c * MBX_CH_STRIDE_C + MBX_CH_REG_{r.name}_C))")
        out.append(f"          {r.name.lower()}_r[c] <= 16'(host_wdata_i & ({_mask(r)}));")
    out += ["      end",
            "      // a refusal or a drop sets ERR; a write of 1 clears it; a set wins",
            "      if (rx_err_p_w || tx_err_p_w || tmr_bad_p_w || refused_w) err_r <= 1'b1;"]
    for (reg, fld), sig in STICKY.items():
        out.append(f"      else if (wr_w && off_w == {AW}'(MBX_REG_{reg}_C)")
        out.append(f"               && mbx_field_f(host_wdata_i, MBX_{reg}_{fld}_LSB_C, MBX_{reg}_{fld}_WIDTH_C) != 0)")
        out.append(f"        {sig} <= 1'b0;")
    out += ["      if ((refused_w || tmr_bad_p_w) && bus_err_r != 16'hFFFF) bus_err_r <= bus_err_r + 16'd1;",
            "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
            f"        if (rd_w && off_w == {AW}'(MBX_IF_BASE_C + i * MBX_IF_STRIDE_C + MBX_IF_REG_GM_LO_C)) begin",
            "          gm_hi_snap_r[i]  <= gm_id_i[64*i + 32 +: 32];",
            "          domain_snap_r[i] <= gptp_domain_i[8*i +: 8];",
            "        end"]
    for r in iff_rw:
        at = f"MBX_IFF_BASE_C + i * MBX_IFF_STRIDE_C + MBX_IFF_REG_{r.name}_C"
        out.append(f"        if (wr_w && off_w == {AW}'({at}))")
        out.append(f"          {r.name.lower()}_r[i] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));")
    out += ["      end", "    end", "  end : host_write", ""]
    return out


def _read_block(contract: Contract) -> list[str]:
    """The register read value, from storage or from each field's source."""
    out = ["  logic [31:0] reg_rdata_w;   //! the register a read addresses, 0 when none",
           "  always_comb begin : reg_read", "    reg_rdata_w = '0;"]
    for reg in contract.registers:
        if reg.access == "wo":
            continue
        value = f"{reg.name.lower()}_r" if reg.access == "rw" else _sources(reg, RO_SOURCES, {})
        out.append(f"    if (off_w == {AW}'(MBX_REG_{reg.name}_C)) reg_rdata_w = {value};")
    for i in range(contract.interfaces):
        for reg in contract.if_registers:
            base = f"MBX_IF_BASE_C + {i} * MBX_IF_STRIDE_C + MBX_IF_REG_{reg.name}_C"
            out.append(f"    if (off_w == {AW}'({base})) reg_rdata_w = {_sources(reg, IF_SOURCES, {'i': i})};")
        for reg in contract.iff_registers:
            if reg.access != "rw":
                raise ContractError(f"interface filter register {reg.name}: the skeleton stores rw registers only")
            base = f"MBX_IFF_BASE_C + {i} * MBX_IFF_STRIDE_C + MBX_IFF_REG_{reg.name}_C"
            out.append(f"    if (off_w == {AW}'({base})) reg_rdata_w = 32'({reg.name.lower()}_r[{i}]);")
    for reg in contract.bnd_registers:
        if reg.access != "rw":
            raise ContractError(f"bound-talker register {reg.name}: KL_mbx_rx holds rw registers only")
    out.append(f"    if (bnd_at_w && bnd_reg_w == 2'd{BOUND_CODE['BOUND_EN']}) reg_rdata_w = "
               f"{_place('BOUND_EN', 'EN', 'bnd_en_w')};")
    out.append(f"    if (bnd_at_w && bnd_reg_w != 2'd{BOUND_CODE['BOUND_EN']} && bnd_eid_vld_w) "
               "reg_rdata_w = bnd_eid_w;")
    for reg in contract.pub_registers:
        out.append(f"    if (pub_at_w && !pub_sink_w && pub_reg_w == {AW}'(MBX_PUB_REG_{reg.name}_C)) "
                   f"reg_rdata_w = 32'(pub_{reg.name.lower()}_r[pub_if_w]);")
    for reg in contract.pub_sink_registers:
        out.append(f"    if (pub_at_w && pub_sink_w && pub_reg_w == {AW}'(MBX_PUB_SINK_REG_{reg.name}_C)) "
                   f"reg_rdata_w = 32'(pub_{reg.name.lower()}_r[pub_if_w][pub_k_w]);")
    out.append("    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin")
    for reg in contract.ch_registers:
        base = f"MBX_CH_BASE_C + c * MBX_CH_STRIDE_C + MBX_CH_REG_{reg.name}_C"
        value = (_place(reg.name, reg.fields[0].name, f"{reg.name.lower()}_r[c]") if reg.access == "rw"
                 else _sources(reg, {k: {f: s.replace("{c}", "c") for f, s in v.items()}
                                     for k, v in CH_SOURCES.items()}, {}))
        out.append(f"      if (off_w == {AW}'({base})) reg_rdata_w = {value};")
    out += ["    end", "  end : reg_read", ""]
    return out


def _ring_block(contract: Contract) -> list[str]:
    """The event ring and one RX and one transmit ring per channel, with their host windows."""
    out = ["  // ---- the rings ------------------------------------------------------------------",
           "  logic [31:0] evt_rdata_w;",
           "  logic        evt_host_w;   //! the host reads the event ring this cycle",
           f"  assign evt_host_w = rd_w && off_w >= {AW}'(MBX_EVT_BASE_C)",
           f"                      && off_w < {AW}'(MBX_EVT_BASE_C + 4 * MBX_EVT_WORDS_C);",
           "  KL_mbx_ring #(.WORDS_P(MBX_EVT_WORDS_C)) u_evt_ring (",
           "    .clk_i     (clk_i),", "    .rst_n     (rst_n),",
           "    .wr_en_i   (evw_en_w),", "    .wr_addr_i (evw_addr_w),", "    .wr_data_i (evw_data_w),",
           "    .rd_en_i   (evt_host_w),",
           f"    .rd_addr_i ($clog2(MBX_EVT_WORDS_C)'((off_w - {AW}'(MBX_EVT_BASE_C)) >> 2)),",
           "    .rd_data_o (evt_rdata_w)", "  );", ""]
    for ch in contract.channels:
        up, lo = ch.name.upper(), ch.name
        for d in ("RX", "TX"):
            words = f"MBX_CH_{up}_{d}_WORDS_C"
            base = f"MBX_CH_{up}_{d}_BASE_C"
            aw = f"$clog2({words})"
            host = f"{lo}_{d.lower()}_host_w"
            word = "receive" if d == "RX" else "transmit"
            out += [f"  // channel {lo} ({ch.ident}): {word} ring at 0x{ch.rx_base if d == 'RX' else ch.tx_base:04X}",
                    f"  logic [31:0] {lo}_{d.lower()}_rdata_w;",
                    f"  logic        {host};   //! the host {'reads' if d == 'RX' else 'writes'} this ring this cycle",
                    f"  assign {host} = {'rd_w' if d == 'RX' else 'wr_w'} && off_w >= {AW}'({base})",
                    f"                      && off_w < {AW}'({base} + 4 * {words});",
                    f"  KL_mbx_ring #(.WORDS_P({words})) u_{lo}_{d.lower()} (",
                    "    .clk_i     (clk_i),", "    .rst_n     (rst_n),"]
            if d == "RX":
                out += [f"    .wr_en_i   (rxw_en_w && rxw_ch_w == MBX_CH_W_C'(MBX_CH_{up}_C)),",
                        f"    .wr_addr_i (rxw_addr_w[{aw}-1:0]),", "    .wr_data_i (rxw_data_w),",
                        f"    .rd_en_i   ({host}),",
                        f"    .rd_addr_i ({aw}'((off_w - {AW}'({base})) >> 2)),"]
            else:
                out += [f"    .wr_en_i   ({host}),",
                        f"    .wr_addr_i ({aw}'((off_w - {AW}'({base})) >> 2)),", "    .wr_data_i (host_wdata_i),",
                        f"    .rd_en_i   (txr_en_w && txr_ch_w == MBX_CH_W_C'(MBX_CH_{up}_C)),",
                        f"    .rd_addr_i (txr_addr_w[{aw}-1:0]),"]
            out += [f"    .rd_data_o ({lo}_{d.lower()}_rdata_w)", "  );", ""]
    return out


def _mux_block(contract: Contract) -> list[str]:
    """The registered answer: register value or ring word, and the TX read return."""
    rx_sel = [f"{ch.name}_rx_host_w" for ch in contract.channels]
    out = ["  // ---- the answer, one cycle after the request ---------------------------------",
           "  logic        ack_r;", "  logic [31:0] reg_rdata_r;",
           "  logic [3:0]  rsel_r;     //! 0 a register, 1 the event ring, 2 + c channel c's receive ring",
           "  logic [MBX_CH_W_C-1:0] txr_ch_r;   //! the transmit ring the merge read last cycle",
           "  always_ff @(posedge clk_i) begin : answer",
           "    if (!rst_n) begin",
           "      ack_r       <= 1'b0;", "      reg_rdata_r <= '0;", "      rsel_r      <= '0;",
           "      txr_ch_r    <= '0;",
           "    end else begin",
           "      ack_r       <= host_req_i;", "      reg_rdata_r <= reg_rdata_w;",
           "      txr_ch_r    <= txr_ch_w;",
           "      rsel_r      <= evt_host_w ? 4'd1"]
    for k, sig in enumerate(rx_sel):
        out.append(f"                   : {sig} ? 4'd{2 + k}")
    out += ["                   : 4'd0;", "    end", "  end : answer", "",
            "  assign host_ack_o = ack_r;", "  always_comb begin : answer_mux", "    unique case (rsel_r)",
            "      4'd1:    host_rdata_o = evt_rdata_w;"]
    for k, ch in enumerate(contract.channels):
        out.append(f"      4'd{2 + k}:    host_rdata_o = {ch.name}_rx_rdata_w;")
    out += ["      default: host_rdata_o = reg_rdata_r;", "    endcase", "  end : answer_mux", "",
            "  logic [31:0] txr_data_w;   //! the transmit ring word the merge asked for last cycle",
            "  always_comb begin : tx_return", "    unique case (txr_ch_r)"]
    for ch in contract.channels:
        out.append(f"      MBX_CH_W_C'(MBX_CH_{ch.name.upper()}_C): txr_data_w = {ch.name}_tx_rdata_w;")
    out += ["      default: txr_data_w = '0;", "    endcase", "  end : tx_return", ""]
    return out


def _check_wiring(contract: Contract) -> None:
    """The register sets the skeleton wires into the leaves by name are the contract's."""
    ch_rw = {r.name for r in contract.ch_registers if r.access == "rw"}
    if ch_rw != {"RX_TAIL", "TX_HEAD"}:
        raise ContractError("the skeleton wires RX_TAIL and TX_HEAD into the leaves; the channel rw set changed")
    iff = {r.name: r for r in contract.iff_registers}
    if set(iff) != set(OWN_MAC_BITS) or any(len(r.fields) != 1 or r.fields[0].lsb != 0 or _bits(r) != hi - lo + 1
                                            for name, r in iff.items() for hi, lo in (OWN_MAC_BITS[name],)):
        raise ContractError("the skeleton wires OWN_MAC_HI (MAC[47:32]) and OWN_MAC_LO (MAC[31:0]) into the "
                            "filter; the interface filter registers changed")
    bnd = {r.name: r for r in contract.bnd_registers}
    if set(bnd) != set(BOUND_BITS) or any(len(r.fields) != 1 or r.fields[0].lsb != 0 or _bits(r) != hi - lo + 1
                                          for name, r in bnd.items() for hi, lo in (BOUND_BITS[name],)):
        raise ContractError("KL_mbx_rx holds BOUND_EID_HI (EID[63:32]), BOUND_EID_LO (EID[31:0]) and BOUND_EN "
                            "(one bit); the bound-talker registers changed")
    for name, stride in (("stride", contract.bnd_stride), ("entry_stride", contract.bnd_entry_stride)):
        if stride & (stride - 1):
            raise ContractError(f"the bound-talker {name} {stride:#x} is not a power of two: the skeleton decodes "
                                "an entry by its offset's bit fields")
    for name, stride in (("stride", contract.pub_stride), ("sink_stride", contract.pub_sink_stride)):
        if stride & (stride - 1):
            raise ContractError(f"the publication {name} {stride:#x} is not a power of two: the skeleton decodes "
                                "an interface and a sink entry by its offset's bit fields")
    if any(r.access != "rw" for r in contract.pub_registers + contract.pub_sink_registers):
        raise ContractError("the skeleton stores the publication block's registers, which are rw only")
    fields = {(r.name, f.name): f for r in contract.pub_registers for f in r.fields}
    if set(fields) != set(PUB_OUTPUTS) or {r.name: tuple(f.name for f in r.fields)
                                           for r in contract.pub_sink_registers} != PUB_SINK_FIELDS:
        raise ContractError("the skeleton wires DA_GATE.OPEN, LICENCE.ACTIVE, IDLE_SLOPE.BPS, SR_DOMAIN's VID, "
                            "PRIORITY and ADOPTED, and the sinks' SID_LO, SID_HI and BINDING's BOUND and "
                            "SID_VALID onto the pub_*_o ports; the publication registers changed")
    for name in ("DA_GATE", "LICENCE"):
        width = next(f for (reg, _), f in fields.items() if reg == name).width
        if width != contract.pub_sources:
            raise ContractError(f"{name} carries {width} sources, the contract publishes {contract.pub_sources}")
    sid = [f for r in contract.pub_sink_registers if r.name in ("SID_LO", "SID_HI") for f in r.fields]
    if any(f.lsb != 0 or f.width != 32 for f in sid):
        raise ContractError("the skeleton joins SID_HI and SID_LO, each a whole word, into the 64-bit stream_id")
    bound = {t.offset for ch in contract.channels for t in ch.terms if t.test == "eq_bound"}
    if len(bound) > 1:
        raise ContractError(f"eq_bound terms read the fields at {sorted(bound)}: KL_mbx_rx compares one "
                            "identity per frame against the bound-talker table")


def _leaves(contract: Contract) -> list[str]:
    """The pending levels, the interrupt and the three leaf instances."""
    _check_wiring(contract)
    mac = ", ".join(f"{name.lower()}_r[i]" for name in OWN_MAC_BITS)
    status = next(r for r in contract.registers if r.name == "IRQ_STATUS")
    return [
        "  always_comb begin : pending",
        "    for (int c = 0; c < int'(MBX_N_CH_C); c++) begin",
        "      rx_tail_w[16*c +: 16] = rx_tail_r[c];",
        "      tx_head_w[16*c +: 16] = tx_head_r[c];",
        "      rx_pending_w[c]       = rx_head_w[16*c +: 16] != rx_tail_r[c];",
        "    end",
        "    evt_pending_w = evt_head_w != evt_tail_r[15:0];",
        "    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
        f"      own_mac_w[48*i +: 48] = {{{mac}}};",
        "    end",
        "  end : pending",
        "",
        "  logic irq_r;",
        "  always_ff @(posedge clk_i) begin : interrupt",
        "    if (!rst_n) irq_r <= 1'b0;",
        f"    else irq_r <= |(({_sources(status, RO_SOURCES, {})}) & irq_enable_r);",
        "  end : interrupt",
        "  assign irq_o = irq_r;",
        "",
        "  KL_mbx_rx u_rx (",
        "    .clk_i           (clk_i),", "    .rst_n           (rst_n),",
        "    .ms_tick_p_i     (ms_tick_p_i),", "    .now_ms_i        (now_ms_r),",
        "    .own_eid_i       ({own_eid_hi_r, own_eid_lo_r}),",
        "    .own_mac_i       (own_mac_w),",
        "    .bnd_req_i       (host_req_i && bnd_at_w),",
        "    .bnd_we_i        (wr_w && bnd_at_w),",
        "    .bnd_if_i        (bnd_if_w),",
        "    .bnd_entry_i     (bnd_entry_w),",
        "    .bnd_reg_i       (bnd_reg_w),",
        "    .bnd_wdata_i     (host_wdata_i),",
        "    .bnd_eid_o       (bnd_eid_w),",
        "    .bnd_eid_vld_o   (bnd_eid_vld_w),",
        "    .bnd_en_o        (bnd_en_w),",
        "    .open_i          (filter_en_r[MBX_N_CH_C-1:0]),",
        "    .maap_base_i     ({maap_base_hi_r[15:0], maap_base_lo_r}),",
        "    .maap_count_i    (maap_count_r[15:0]),",
        "    .rx_valid_i      (rx_valid_i),", "    .rx_ready_o      (rx_ready_o),",
        "    .rx_data_i       (rx_data_i),", "    .rx_last_i       (rx_last_i),", "    .rx_if_i         (rx_if_i),",
        "    .wr_en_o         (rxw_en_w),", "    .wr_ch_o         (rxw_ch_w),",
        "    .wr_addr_o       (rxw_addr_w),", "    .wr_data_o       (rxw_data_w),",
        "    .rx_tail_words_i (rx_tail_w),", "    .rx_head_words_o (rx_head_w),",
        "    .rx_drop_cnt_o   (rx_drop_w),", "    .rate_drop_cnt_o (rate_drop_w),",
        "    .rx_pass_cnt_o   (rx_pass_w),", "    .mismatch_cnt_o  (filter_mismatch_w),",
        "    .err_p_o         (rx_err_p_w)",
        "  );",
        "",
        "  KL_mbx_tx u_tx (",
        "    .clk_i           (clk_i),", "    .rst_n           (rst_n),",
        "    .tx_head_words_i (tx_head_w),", "    .tx_tail_words_o (tx_tail_w),",
        "    .tx_err_cnt_o    (tx_err_w),", "    .err_p_o         (tx_err_p_w),",
        "    .rd_en_o         (txr_en_w),", "    .rd_ch_o         (txr_ch_w),",
        "    .rd_addr_o       (txr_addr_w),", "    .rd_data_i       (txr_data_w),",
        "    .tx_valid_o      (tx_valid_o),", "    .tx_ready_i      (tx_ready_i),",
        "    .tx_data_o       (tx_data_o),", "    .tx_last_o       (tx_last_o),",
        "    .tx_if_o         (tx_if_o),", "    .tx_ch_o         (tx_ch_o)",
        "  );",
        "",
        "  KL_mbx_evt u_evt (",
        "    .clk_i             (clk_i),", "    .rst_n             (rst_n),",
        "    .ms_tick_p_i       (ms_tick_p_i),",
        "    .now_ms_i          (now_ms_r),",
        "    .tick_en_i         (tick_ctl_r[MBX_TICK_CTL_EN_LSB_C]),",
        "    .tmr_cmd_p_i       (tmr_cmd_p_w),",
        "    .tmr_slot_i        (8'(mbx_field_f(host_wdata_i, MBX_TMR_CMD_SLOT_LSB_C, MBX_TMR_CMD_SLOT_WIDTH_C))),",
        "    .tmr_tag_i         (16'(mbx_field_f(host_wdata_i, MBX_TMR_CMD_TAG_LSB_C, MBX_TMR_CMD_TAG_WIDTH_C))),",
        "    .tmr_op_i          (2'(mbx_field_f(host_wdata_i, MBX_TMR_CMD_OP_LSB_C, MBX_TMR_CMD_OP_WIDTH_C))),",
        "    .tmr_deadline_ms_i (tmr_deadline_r),",
        "    .tmr_bad_p_o       (tmr_bad_p_w),",
        "    .link_up_i         (link_up_i),", "    .gm_change_p_i     (gm_change_p_i),",
        "    .gm_id_i           (gm_id_i),", "    .gptp_domain_i     (gptp_domain_i),",
        "    .evt_tail_words_i  (evt_tail_r[15:0]),", "    .evt_head_words_o  (evt_head_w),",
        "    .wr_en_o           (evw_en_w),", "    .wr_addr_o         (evw_addr_w),",
        "    .wr_data_o         (evw_data_w)",
        "  );",
        "",
        "  // the window bits a 16-bit register does not carry, the upper",
        "  // filter-enable, MAAP and TICK_CTL bits a narrower build does not use,",
        "  // and the ring index bits above the narrower rings of this contract",
        "  logic unused_w;",
        "  assign unused_w = ^{evt_tail_r[31:16], maap_base_hi_r[31:16], maap_count_r[31:16],",
        "                      filter_en_r[31:MBX_N_CH_C], tick_ctl_r[31:1], rxw_addr_w, txr_addr_w};",
        "",
        "endmodule : KL_mbx",
        "",
        "`default_nettype wire",
        "",
    ]


def emit_sv_top(contract: Contract) -> str:
    """KL_mbx.sv, the generated fabric skeleton."""
    lines = (_banner() + _ports() + _pub_ports() + _core() + _bound_decode(contract) + _pub_decode(contract)
             + _storage(contract) + _write_block(contract) + _read_block(contract) + _pub_block(contract)
             + _ring_block(contract) + _mux_block(contract) + _leaves(contract))
    return "\n".join(lines)

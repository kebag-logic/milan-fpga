# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Emit the face block of KL_mbx.sv: the settings, their commit, the windows.

The face block (contract 2.3; #665, the assignment 6409739310 and the ruling
6410169666) carries the processor wrapper's faces other than its class-D
outputs. Every setting field leaves on a port of its own, ``fw_<register>_<field>_o``
for the interface settings and the names ``FACE_SOURCE_PORTS`` and
``FACE_SINK_PORTS`` give the entries, and every window's request field on
``<window>_<field>_o`` (a ``_LO``/``_HI`` register pair joined into one
64-bit port). The ports are generated from the contract; a field the
skeleton cannot place is refused.

THE ONE DECISION THAT MATTERS: nothing leaves without its qualifier. A commit
raises ``fw_send_o`` and the settings hold until ``fw_ack_p_i``; a window's
GO raises ``<window>_req_o`` with its tag and the request fields hold until
the answer or the timeout. A write that would move a held value is refused
and counted in BUS_ERR, so the placement switch can cross every value with
cdc_handshake (its src_send and src_rcv) or toggle-plus-sync.
"""

from __future__ import annotations

from mailbox_model import FACE_COMMIT, FACE_STATUS, Contract, ContractError, Register, Window

AW = "AW2_C"

#: The source entry's ports: port -> (the registers and field it joins, high word first; bits a source).
FACE_SOURCE_PORTS = {
    "fw_pt_offset_ns_o": ((("F_PT_OFFSET", "NS"),), 32),
    "fw_pt_offset_v_o": ((("F_SRC_VALID", "PT_OFFSET"),), 1),
    "fw_fmt_out_o": ((("F_FMT_OUT_HI", "FMT"), ("F_FMT_OUT_LO", "FMT")), 64),
    "fw_fmt_out_v_o": ((("F_SRC_VALID", "FMT_OUT"),), 1),
}
#: The sink entry's ports, the same way.
FACE_SINK_PORTS = {
    "fw_fmt_in_o": ((("F_FMT_IN_HI", "FMT"), ("F_FMT_IN_LO", "FMT")), 64),
    "fw_fmt_in_v_o": ((("F_SNK_VALID", "FMT_IN"),), 1),
}


def _bits(reg: Register) -> int:
    """The register's width up to its highest field bit: what storage of it keeps."""
    return max(f.lsb + f.width for f in reg.fields)


def _mask(reg: Register) -> str:
    """The union of a register's field masks, from the constants."""
    return " | ".join(f"mbx_place_f(32'hFFFF_FFFF, MBX_{reg.name}_{f.name}_LSB_C, MBX_{reg.name}_{f.name}_WIDTH_C)"
                      for f in reg.fields)


def _field(reg: str, fld: str, src: str) -> str:
    """Field fld of register reg out of the stored word src."""
    return f"mbx_field_f(32'({src}), MBX_{reg}_{fld}_LSB_C, MBX_{reg}_{fld}_WIDTH_C)"


def _owned(contract: Contract) -> dict[str, Window]:
    """Each register a window holds, by name, and its window."""
    return {n: w for w in contract.face_windows for n in (w.go, w.status, *w.data, *w.request)}


def settings(contract: Contract) -> list[Register]:
    """The interface settings: the face block's rw registers no window holds."""
    owned = _owned(contract)
    return [r for r in contract.face_registers if r.name not in owned and r.access == "rw"]


def setting_ports(contract: Contract) -> list[tuple[str, str, str, int]]:
    """(port, register, field, bits an interface) of every setting field."""
    return [(f"fw_{r.name.removeprefix('F_').lower()}_{f.name.lower()}_o", r.name, f.name, f.width)
            for r in settings(contract) for f in r.fields]


def request_ports(w: Window, regs: dict[str, Register]) -> list[tuple[str, tuple[tuple[str, str], ...], int]]:
    """(port, the registers and fields it carries, high first; bits) of a window's request:
    a _LO/_HI pair of one whole-word field each joined, every other field on its own."""
    out, done = [], set()
    prefix = f"{w.name}_"
    for name in w.request:
        if name in done:
            continue
        reg = regs[name]
        base = name.removeprefix(prefix)
        if base.endswith(("_LO", "_HI")):
            lo, hi = f"{name[:-3]}_LO", f"{name[:-3]}_HI"
            if lo not in w.request or hi not in w.request:
                raise ContractError(f"window {w.name}: {name} has no partner of the pair {lo}, {hi}")
            fl, fh = regs[lo].fields, regs[hi].fields
            if len(fl) != 1 or len(fh) != 1 or any(f.lsb != 0 or f.width != 32 for f in fl + fh) \
                    or fl[0].name != fh[0].name:
                raise ContractError(f"window {w.name}: the pair {lo}, {hi} is not one whole-word field each")
            out.append((f"{w.name.lower()}_{base[:-3].lower()}_o", ((hi, fh[0].name), (lo, fl[0].name)), 64))
            done |= {lo, hi}
        else:
            out += [(f"{w.name.lower()}_{f.name.lower()}_o", ((name, f.name),), f.width) for f in reg.fields]
            done.add(name)
    names = [p for p, _, _ in out]
    if len(set(names)) != len(names):
        raise ContractError(f"window {w.name}: two request fields would leave on one port")
    return out


def check(contract: Contract) -> None:
    """The face block is one the skeleton can decode and wire."""
    for label, stride in (("stride", contract.face_stride), ("source_stride", contract.face_source_stride),
                          ("sink_stride", contract.face_sink_stride)):
        if stride & (stride - 1):
            raise ContractError(f"the face {label} {stride:#x} is not a power of two: the skeleton decodes an "
                                "interface and an entry by its offset's bit fields")
    for table, regs, label in ((FACE_SOURCE_PORTS, contract.face_source_registers, "source"),
                               (FACE_SINK_PORTS, contract.face_sink_registers, "sink")):
        have = {(r.name, f.name): f for r in regs for f in r.fields}
        want = {rf for parts, _ in table.values() for rf in parts}
        if set(have) != want or any(sum(have[rf].width for rf in parts) != bits for parts, bits in table.values()):
            raise ContractError(f"the skeleton wires the {label} entries' fields onto "
                                f"{', '.join(table)}; the face {label} registers changed")
    regs = {r.name: r for r in contract.face_registers}
    for w in contract.face_windows:
        request_ports(w, regs)
        if any(r.fields[0].lsb != 0 or r.fields[0].width != 32 or len(r.fields) != 1
               for r in (regs[n] for n in w.data)):
            raise ContractError(f"window {w.name}: its data registers are one whole-word field each")
    ports = [p for p, *_ in setting_ports(contract)] + [p for w in contract.face_windows
                                                         for p, *_ in request_ports(w, regs)]
    if len(set(ports)) != len(ports):
        raise ContractError("two face fields would leave on one port")


def ports(contract: Contract) -> list[str]:
    """The face block's ports: the settings and their commit, then each window."""
    regs = {r.name: r for r in contract.face_registers}
    out = ["  // the face block: the settings, held from a commit until its acknowledgement",
           "  output logic [MBX_N_IF_C-1:0] fw_send_o,   "
           "//! a commit waits for its acknowledgement: every fw_*_o holds",
           "  input  wire  [MBX_N_IF_C-1:0] fw_ack_p_i,   "
           "//! one-cycle pulse per interface: the datapath took the commit"]
    for port, reg, fld, _bits_ in setting_ports(contract):
        out.append(f"  output logic [MBX_N_IF_C*MBX_{reg}_{fld}_WIDTH_C-1:0] {port},   //! {reg}.{fld} per interface")
    for table, count, what in ((FACE_SOURCE_PORTS, "MBX_N_PUB_SOURCES_C", "source"),
                               (FACE_SINK_PORTS, "MBX_N_PUB_SINKS_C", "sink")):
        for port, (parts, bits) in table.items():
            names = ":".join(f"{r}.{f}" for r, f in parts)
            out.append(f"  output logic [MBX_N_IF_C*{count}*{bits}-1:0] {port},   //! {names} per {what}")
    for w in contract.face_windows:
        lw, tag = w.name.lower(), f"MBX_{w.status}_TAG_WIDTH_C"
        dw = 32 * len(w.data)
        out += [f"  // the {w.name} window: the request holds from its GO until its answer or {w.wait_cycles} cycles",
                f"  output logic [MBX_N_IF_C-1:0] {lw}_req_o,   //! a request is open: its fields and tag hold",
                f"  output logic [MBX_N_IF_C*{tag}-1:0] {lw}_tag_o,   //! the open request's tag"]
        for port, parts, bits in request_ports(w, regs):
            names = ":".join(f"{r}.{f}" for r, f in parts)
            out.append(f"  output logic [MBX_N_IF_C*{bits}-1:0] {port},   //! {names} per interface")
        out += [f"  input  wire  [MBX_N_IF_C-1:0] {lw}_ans_p_i,   "
                "//! one-cycle pulse: the answer, with its data and tag",
                f"  input  wire  [MBX_N_IF_C*{tag}-1:0] {lw}_ans_tag_i,   //! the tag of the request it answers",
                f"  input  wire  [MBX_N_IF_C*{dw}-1:0] {lw}_ans_data_i,   //! the answer, valid with {lw}_ans_p_i"]
    out += ["  // the face block's events, one-cycle pulses per interface with their qualifiers",
            "  input  wire  [MBX_N_IF_C-1:0] ctr_chg_p_i,   //! a served descriptor's counters moved",
            "  input  wire  [MBX_N_IF_C*16-1:0] ctr_chg_type_i,   //! its descriptor_type, valid with ctr_chg_p_i",
            "  input  wire  [MBX_N_IF_C*16-1:0] ctr_chg_index_i,   //! its descriptor_index, valid with ctr_chg_p_i",
            "  input  wire  [MBX_N_IF_C-1:0] avb_chg_p_i,   //! a served GET_AVB_INFO word changed",
            "  input  wire  [MBX_N_IF_C-1:0] asp_chg_p_i,   //! the served AS_PATH sequence changed",
            "  input  wire  [MBX_N_IF_C-1:0] amap_wr_p_i   //! an edit's commit beat changed the live map",
            ");", ""]
    return out


def decode(contract: Contract) -> list[str]:
    """The face register an offset names: interface, region (the interface's
    registers, a source entry or a sink entry), entry and offset inside it,
    by the offset's bit fields, the strides being powers of two."""
    regs = " || ".join(f"face_reg_w == {AW}'(MBX_FACE_REG_{r.name}_C)" for r in contract.face_registers)
    srcs = " || ".join(f"face_reg_w == {AW}'(MBX_FACE_SRC_REG_{r.name}_C)" for r in contract.face_source_registers)
    snks = " || ".join(f"face_reg_w == {AW}'(MBX_FACE_SNK_REG_{r.name}_C)" for r in contract.face_sink_registers)
    return ["  // ---- the face block: decoded and held here, read by the datapath -------------------",
            "  // The strides are powers of two, so an offset's interface and entry are",
            "  // its bit fields; a hole between the registers names none.",
            "  localparam int unsigned FACE_SW_C = (MBX_N_PUB_SOURCES_C > 1) ? $clog2(MBX_N_PUB_SOURCES_C) : 1;"
            "   //! source index bits",
            "  localparam int unsigned FACE_KW_C = (MBX_N_PUB_SINKS_C > 1) ? $clog2(MBX_N_PUB_SINKS_C) : 1;"
            "   //! sink index bits",
            "  logic                  face_at_w;     //! the offset names a face register",
            "  logic [1:0]            face_area_w;   //! 0 the interface's registers, 1 a source entry, 2 a sink entry",
            "  logic [MBX_IF_W_C-1:0] face_if_w;     //! its interface",
            "  logic [FACE_SW_C-1:0]  face_s_w;      //! its source entry",
            "  logic [FACE_KW_C-1:0]  face_k_w;      //! its sink entry",
            f"  logic [{AW}-1:0]      face_reg_w;    //! its offset inside the interface's registers or the entry",
            "  always_comb begin : face_decode",
            f"    logic [{AW}-1:0] rel;",
            f"    logic [{AW}-1:0] in_if;",
            f"    logic [{AW}-1:0] entry;",
            f"    rel         = off_w - {AW}'(MBX_FACE_BASE_C);",
            f"    in_if       = rel & {AW}'(MBX_FACE_STRIDE_C - 1);",
            "    face_if_w   = MBX_IF_W_C'(rel >> $clog2(MBX_FACE_STRIDE_C));",
            f"    face_area_w = (in_if >= {AW}'(MBX_FACE_SINK_BASE_C)) ? 2'd2",
            f"                : (in_if >= {AW}'(MBX_FACE_SOURCE_BASE_C)) ? 2'd1 : 2'd0;",
            f"    entry       = (face_area_w == 2'd2)",
            f"                  ? ((in_if - {AW}'(MBX_FACE_SINK_BASE_C)) >> $clog2(MBX_FACE_SINK_STRIDE_C))",
            f"                  : ((in_if - {AW}'(MBX_FACE_SOURCE_BASE_C)) >> $clog2(MBX_FACE_SOURCE_STRIDE_C));",
            "    face_s_w    = FACE_SW_C'(entry);",
            "    face_k_w    = FACE_KW_C'(entry);",
            f"    face_reg_w  = (face_area_w == 2'd2) ? ((in_if - {AW}'(MBX_FACE_SINK_BASE_C))"
            f" & {AW}'(MBX_FACE_SINK_STRIDE_C - 1))",
            f"                : (face_area_w == 2'd1) ? ((in_if - {AW}'(MBX_FACE_SOURCE_BASE_C))"
            f" & {AW}'(MBX_FACE_SOURCE_STRIDE_C - 1))",
            "                : in_if;",
            f"    face_at_w   = off_w >= {AW}'(MBX_FACE_BASE_C)",
            f"                  && (rel >> $clog2(MBX_FACE_STRIDE_C)) < {AW}'(MBX_N_IF_C)",
            "                  && ((face_area_w == 2'd0 && (" + regs + "))",
            f"                      || (face_area_w == 2'd1 && entry < {AW}'(MBX_N_PUB_SOURCES_C) && ({srcs}))",
            f"                      || (face_area_w == 2'd2 && entry < {AW}'(MBX_N_PUB_SINKS_C) && ({snks})));",
            "  end : face_decode",
            ""]


def _hit(area: int, reg: str, kind: str = "REG") -> str:
    """The decode term of one face register."""
    return f"face_at_w && face_area_w == 2'd{area} && face_reg_w == {AW}'(MBX_FACE_{kind}_{reg}_C)"


def block(contract: Contract) -> list[str]:
    """The face block's storage, its writes and their refusals, the commit, the
    windows' requests, answers and timeouts, and the outputs."""
    regs = {r.name: r for r in contract.face_registers}
    sets = settings(contract)
    out = ["  // ---- the face block's storage: the firmware writes it, the datapath reads it ---------"]
    for r in sets + [regs[n] for w in contract.face_windows for n in w.request]:
        out.append(f"  logic [{_bits(r) - 1}:0] face_{r.name.lower()}_r [MBX_N_IF_C];   //! {r.name} per interface")
    for r in contract.face_source_registers:
        out.append(f"  logic [{_bits(r) - 1}:0] face_{r.name.lower()}_r [MBX_N_IF_C][MBX_N_PUB_SOURCES_C];"
                   f"   //! {r.name} per source")
    for r in contract.face_sink_registers:
        out.append(f"  logic [{_bits(r) - 1}:0] face_{r.name.lower()}_r [MBX_N_IF_C][MBX_N_PUB_SINKS_C];"
                   f"   //! {r.name} per sink")
    out += ["  logic [MBX_N_IF_C-1:0] fw_busy_r;   //! F_STATUS.BUSY: a commit waits for its acknowledgement"]
    for w in contract.face_windows:
        lw = w.name.lower()
        out += [f"  logic [MBX_N_IF_C-1:0] {lw}_busy_r;   //! {w.status}.BUSY",
                f"  logic [MBX_N_IF_C-1:0] {lw}_done_r;   //! {w.status}.DONE",
                f"  logic [MBX_N_IF_C-1:0] {lw}_tmo_r;    //! {w.status}.TIMEOUT",
                f"  logic [MBX_{w.status}_TAG_WIDTH_C-1:0] {lw}_tag_r [MBX_N_IF_C];   //! {w.status}.TAG",
                f"  logic [15:0] {lw}_wait_r [MBX_N_IF_C];   //! cycles the open request has waited",
                f"  logic [{32 * len(w.data) - 1}:0] {lw}_data_r [MBX_N_IF_C];   //! the answer"]
    # the refusals: a write that would move a held value
    held_f = [_hit(0, r.name) for r in sets] + [_hit(0, FACE_COMMIT)]
    held_f += [_hit(1, r.name, "SRC_REG") for r in contract.face_source_registers]
    held_f += [_hit(2, r.name, "SNK_REG") for r in contract.face_sink_registers]
    out += ["", "  logic face_refused_w;   //! a write that would move a held value, refused and counted",
            "  always_comb begin : face_refusal",
            "    face_refused_w = 1'b0;",
            "    if (wr_w && fw_busy_r[face_if_w] && (" + "\n        || ".join(f"({h})" for h in held_f) + "))",
            "      face_refused_w = 1'b1;"]
    for w in contract.face_windows:
        terms = "\n        || ".join(f"({_hit(0, n)})" for n in (*w.request, w.go))
        out += [f"    if (wr_w && {w.name.lower()}_busy_r[face_if_w] && ({terms}))", "      face_refused_w = 1'b1;"]
    out += ["  end : face_refusal", ""]
    # the writes
    out += ["  always_ff @(posedge clk_i) begin : face_write", "    if (!rst_n) begin",
            "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin"]
    out += [f"        face_{r.name.lower()}_r[i] <= '0;" for r in sets]
    out += [f"        face_{regs[n].name.lower()}_r[i] <= '0;" for w in contract.face_windows for n in w.request]
    out.append("        for (int s = 0; s < int'(MBX_N_PUB_SOURCES_C); s++) begin")
    out += [f"          face_{r.name.lower()}_r[i][s] <= '0;" for r in contract.face_source_registers]
    out += ["        end", "        for (int k = 0; k < int'(MBX_N_PUB_SINKS_C); k++) begin"]
    out += [f"          face_{r.name.lower()}_r[i][k] <= '0;" for r in contract.face_sink_registers]
    out += ["        end", "      end", "    end else if (wr_w && face_at_w && !face_refused_w) begin"]
    for r in sets:
        out += [f"      if ({_hit(0, r.name)})",
                f"        face_{r.name.lower()}_r[face_if_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));"]
    for w in contract.face_windows:
        for n in w.request:
            r = regs[n]
            out += [f"      if ({_hit(0, n)})",
                    f"        face_{n.lower()}_r[face_if_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));"]
    for r in contract.face_source_registers:
        out += [f"      if ({_hit(1, r.name, 'SRC_REG')})",
                f"        face_{r.name.lower()}_r[face_if_w][face_s_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));"]
    for r in contract.face_sink_registers:
        out += [f"      if ({_hit(2, r.name, 'SNK_REG')})",
                f"        face_{r.name.lower()}_r[face_if_w][face_k_w] <= {_bits(r)}'(host_wdata_i & ({_mask(r)}));"]
    out += ["    end", "  end : face_write", ""]
    # the commit
    go = f"mbx_field_f(host_wdata_i, MBX_{FACE_COMMIT}_GO_LSB_C, MBX_{FACE_COMMIT}_GO_WIDTH_C) != 0"
    out += ["  // the commit: GO raises fw_send_o until the acknowledgement; an acknowledgement",
            "  // with no commit waiting is not one",
            "  always_ff @(posedge clk_i) begin : face_commit",
            "    if (!rst_n) fw_busy_r <= '0;",
            "    else begin",
            "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
            "        if (fw_ack_p_i[i]) fw_busy_r[i] <= 1'b0;",
            "      end",
            f"      if (wr_w && !face_refused_w && {_hit(0, FACE_COMMIT)} && {go})",
            "        fw_busy_r[face_if_w] <= 1'b1;",
            "    end",
            "  end : face_commit", ""]
    # the windows
    for w in contract.face_windows:
        lw, tag = w.name.lower(), f"MBX_{w.status}_TAG_WIDTH_C"
        dw = 32 * len(w.data)
        wgo = f"mbx_field_f(host_wdata_i, MBX_{w.go}_GO_LSB_C, MBX_{w.go}_GO_WIDTH_C) != 0"
        out += [f"  // the {w.name} window: GO opens a request under the next tag; the answer that",
                "  // carries that tag closes it, any other answer is discarded, and the timeout",
                "  // closes it unanswered",
                f"  always_ff @(posedge clk_i) begin : win_{lw}",
                "    if (!rst_n) begin",
                f"      {lw}_busy_r <= '0;", f"      {lw}_done_r <= '0;", f"      {lw}_tmo_r  <= '0;",
                "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
                f"        {lw}_tag_r[i]  <= '0;", f"        {lw}_wait_r[i] <= '0;", f"        {lw}_data_r[i] <= '0;",
                "      end",
                "    end else begin",
                "      for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
                f"        if ({lw}_busy_r[i]) begin",
                f"          if ({lw}_ans_p_i[i] && {lw}_ans_tag_i[{tag}*i +: {tag}] == {lw}_tag_r[i]) begin",
                f"            {lw}_busy_r[i] <= 1'b0;",
                f"            {lw}_done_r[i] <= 1'b1;",
                f"            {lw}_data_r[i] <= {lw}_ans_data_i[{dw}*i +: {dw}];",
                f"          end else if (32'({lw}_wait_r[i]) + 32'd1 >= MBX_WIN_{w.name}_WAIT_CYCLES_C) begin",
                f"            {lw}_busy_r[i] <= 1'b0;",
                f"            {lw}_tmo_r[i]  <= 1'b1;",
                "          end",
                f"          {lw}_wait_r[i] <= {lw}_wait_r[i] + 16'd1;",
                "        end",
                "      end",
                f"      if (wr_w && !face_refused_w && {_hit(0, w.go)} && {wgo}) begin",
                f"        {lw}_busy_r[face_if_w] <= 1'b1;",
                f"        {lw}_done_r[face_if_w] <= 1'b0;",
                f"        {lw}_tmo_r[face_if_w]  <= 1'b0;",
                f"        {lw}_tag_r[face_if_w]  <= {lw}_tag_r[face_if_w] + {tag}'(1);",
                f"        {lw}_wait_r[face_if_w] <= '0;",
                "      end",
                "    end",
                f"  end : win_{lw}", ""]
    # the outputs
    out += ["  always_comb begin : face_out", "    for (int i = 0; i < int'(MBX_N_IF_C); i++) begin",
            "      fw_send_o[i] = fw_busy_r[i];"]
    for port, reg, fld, _b in setting_ports(contract):
        width = f"MBX_{reg}_{fld}_WIDTH_C"
        out.append(f"      {port}[{width}*i +: {width}] = {width}'({_field(reg, fld, f'face_{reg.lower()}_r[i]')});")
    for table, count, idx in ((FACE_SOURCE_PORTS, "MBX_N_PUB_SOURCES_C", "s"),
                              (FACE_SINK_PORTS, "MBX_N_PUB_SINKS_C", "k")):
        out.append(f"      for (int {idx} = 0; {idx} < int'({count}); {idx}++) begin")
        for port, (parts, bits) in table.items():
            value = ", ".join(f"{32 if bits == 64 else bits}'({_field(r, f, f'face_{r.lower()}_r[i][{idx}]')})"
                              for r, f in parts)
            out.append(f"        {port}[{bits}*({count}*i + {idx}) +: {bits}] = {{{value}}};")
        out.append("      end")
    for w in contract.face_windows:
        lw, tag = w.name.lower(), f"MBX_{w.status}_TAG_WIDTH_C"
        out += [f"      {lw}_req_o[i] = {lw}_busy_r[i];", f"      {lw}_tag_o[{tag}*i +: {tag}] = {lw}_tag_r[i];"]
        for port, parts, bits in request_ports(w, regs):
            value = ", ".join(f"{32 if bits == 64 else bits}'({_field(r, f, f'face_{r.lower()}_r[i]')})"
                              for r, f in parts)
            out.append(f"      {port}[{bits}*i +: {bits}] = {{{value}}};")
    out += ["    end", "  end : face_out", ""]
    return out


def read(contract: Contract) -> list[str]:
    """The face block's read-back: the stored settings and requests, each status, each answer."""
    out = []
    for r in settings(contract):
        out.append(f"    if ({_hit(0, r.name)}) reg_rdata_w = 32'(face_{r.name.lower()}_r[face_if_w]);")
    out.append(f"    if ({_hit(0, FACE_STATUS)}) reg_rdata_w = "
               f"mbx_place_f(32'(fw_busy_r[face_if_w]), MBX_{FACE_STATUS}_BUSY_LSB_C, MBX_{FACE_STATUS}_BUSY_WIDTH_C);")
    for w in contract.face_windows:
        lw = w.name.lower()
        for n in w.request:
            out.append(f"    if ({_hit(0, n)}) reg_rdata_w = 32'(face_{n.lower()}_r[face_if_w]);")
        st = w.status
        status = " | ".join(f"mbx_place_f(32'({src}), MBX_{st}_{fld}_LSB_C, MBX_{st}_{fld}_WIDTH_C)"
                            for fld, src in (("BUSY", f"{lw}_busy_r[face_if_w]"), ("DONE", f"{lw}_done_r[face_if_w]"),
                                             ("TIMEOUT", f"{lw}_tmo_r[face_if_w]"), ("TAG", f"{lw}_tag_r[face_if_w]")))
        out.append(f"    if ({_hit(0, st)}) reg_rdata_w = {status};")
        for k, n in enumerate(w.data):
            out.append(f"    if ({_hit(0, n)}) reg_rdata_w = {lw}_data_r[face_if_w][32*{k} +: 32];")
    for r in contract.face_source_registers:
        out.append(f"    if ({_hit(1, r.name, 'SRC_REG')}) "
                   f"reg_rdata_w = 32'(face_{r.name.lower()}_r[face_if_w][face_s_w]);")
    for r in contract.face_sink_registers:
        out.append(f"    if ({_hit(2, r.name, 'SNK_REG')}) "
                   f"reg_rdata_w = 32'(face_{r.name.lower()}_r[face_if_w][face_k_w]);")
    return out


#: KL_mbx_evt's event inputs, by the KL_mbx port each comes from.
EVT_CONNECTIONS = (("ctr_chg_p_i", "ctr_chg_p_i"), ("ctr_chg_type_i", "ctr_chg_type_i"),
                   ("ctr_chg_index_i", "ctr_chg_index_i"), ("avb_chg_p_i", "avb_chg_p_i"),
                   ("asp_chg_p_i", "asp_chg_p_i"), ("amap_wr_p_i", "amap_wr_p_i"))

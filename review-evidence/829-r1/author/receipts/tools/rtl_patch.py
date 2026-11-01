#!/usr/bin/env python3
"""Apply the writable-correction RTL and builder change to the bench worktree. Fails loudly on any non-unique anchor."""
import sys
root = "$VALIDATION_STORAGE/829-a725/wt-bench/"
def patch(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old, s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)

patch("hdl/common/csr/milan_csr.sv", [
("""  parameter int unsigned MILAN_CLK_FREQ_HZ_P = 125_000_000,
""", """  parameter int unsigned MILAN_CLK_FREQ_HZ_P = 125_000_000,
  //! THE WRITABLE LATENCY CORRECTIONS (issue #829, build key
  //! gptp.latency_writable). Off, 0x540 and 0x544 stay inert scratch that
  //! resets to zero, nothing below elaborates, and the two outputs carry the
  //! elaboration constants. On, a write to either word moves the correction
  //! the plane applies and the build-time pair is only their reset value.
  parameter bit          GPTP_LAT_WRITABLE_P   = 1'b0,
  parameter int unsigned GPTP_INGRESS_LAT_NS_P = 0,
  parameter int unsigned GPTP_EGRESS_LAT_NS_P  = 0,
"""),
("""  input  wire [31:0]             i_gptp_lat_ns,
""", """  input  wire [31:0]             i_gptp_lat_ns,
  //! The corrections the plane applies, in this block's own clock domain,
  //! which is the plane's (issue #829): the constants unless
  //! GPTP_LAT_WRITABLE_P, then [15:0] of the last write to each word.
  output wire [15:0]             o_gptp_lat_ingress_ns,
  output wire [15:0]             o_gptp_lat_egress_ns,
"""),
("""  //! Register file write path: synchronous reset defaults, hardware event
""", """  //! The applied corrections (issue #829). One flop per direction, because the
  //! shadow RAM that serves the read-back has no consumer port, so one write
  //! changes one direction on one edge and a stamp reads a whole value.
  localparam logic [31:0] PTP_ILAT_RST_C =
      GPTP_LAT_WRITABLE_P ? 32'(GPTP_INGRESS_LAT_NS_P) : 32'd0;
  localparam logic [31:0] PTP_ELAT_RST_C =
      GPTP_LAT_WRITABLE_P ? 32'(GPTP_EGRESS_LAT_NS_P) : 32'd0;
  generate if (GPTP_LAT_WRITABLE_P) begin : g_lat_writable
    logic [15:0] lat_ing_r, lat_egr_r;
    always_ff @(posedge aclk) begin
      if (!aresetn) begin
        lat_ing_r <= 16'(GPTP_INGRESS_LAT_NS_P);
        lat_egr_r <= 16'(GPTP_EGRESS_LAT_NS_P);
      end else if (wr_fire) begin
        if (wr_addr == A_PTP_ILAT) lat_ing_r <= s_axi_wdata[15:0];
        if (wr_addr == A_PTP_ELAT) lat_egr_r <= s_axi_wdata[15:0];
      end
    end
    assign o_gptp_lat_ingress_ns = lat_ing_r;
    assign o_gptp_lat_egress_ns  = lat_egr_r;
  end else begin : g_lat_constant
    assign o_gptp_lat_ingress_ns = 16'(GPTP_INGRESS_LAT_NS_P);
    assign o_gptp_lat_egress_ns  = 16'(GPTP_EGRESS_LAT_NS_P);
  end endgenerate

  //! Register file write path: synchronous reset defaults, hardware event
"""),
("""      A_PTP_INCR[10:0]:   csr_default = PTP_INCR_RST_C;
""", """      A_PTP_INCR[10:0]:   csr_default = PTP_INCR_RST_C;
      A_PTP_ILAT[10:0]:   csr_default = PTP_ILAT_RST_C;
      A_PTP_ELAT[10:0]:   csr_default = PTP_ELAT_RST_C;
"""),
("""  //! remains the plane: 0x540 and 0x544 stay inert scratch. 0x005D was never
""", """  //! remains the plane: 0x540 and 0x544 stay inert scratch unless the build
  //! sets GPTP_LAT_WRITABLE_P (issue #829). 0x005D was never
"""),
("""  //! PTP_INGRESS_LAT / PTP_EGRESS_LAT (0x540/0x544) are readable, inert scratch:
  //! plain RW with no timestamp-correction consumer at VERSION 0x0002_0057.
""", """  //! PTP_INGRESS_LAT / PTP_EGRESS_LAT (0x540/0x544) are readable, inert scratch:
  //! plain RW with no timestamp-correction consumer at VERSION 0x0002_0057,
  //! unless the build sets GPTP_LAT_WRITABLE_P (issue #829).
"""),
("""  //! nanoseconds: {ingress[31:16], egress[15:0]}. Elaboration constants the
  //! builder carried from the board configuration, republished so a
""", """  //! nanoseconds: {ingress[31:16], egress[15:0]}. Elaboration constants the
  //! builder carried from the board configuration, or the written pair under
  //! GPTP_LAT_WRITABLE_P (issue #829), republished so a
"""),
("""  //! egress. This is the ONLY live latency-correction publication: 0x540
  //! and 0x544 remain inert scratch with no timestamp consumer.
""", """  //! egress. This is the ONLY live latency-correction publication: 0x540
  //! and 0x544 remain inert scratch with no timestamp consumer unless the
  //! build sets GPTP_LAT_WRITABLE_P (issue #829).
"""),
])

patch("hdl/milan/milan_datapath.sv", [
("""  //! OWNER: `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` (0x540/0x544) stay inert
  //! scratch with no timestamp consumer, so nothing can apply a correction
  //! twice. Both are published read-only at `A_GPTP_LAT` (0x7F0) so a
  //! controller host and the UART status read what is actually applied.
  //! The defaults are zero, which is the uncorrected build.
  parameter int unsigned GPTP_INGRESS_LAT_NS_P = 0,
  parameter int unsigned GPTP_EGRESS_LAT_NS_P  = 0,
""", """  //! OWNER: `PTP_INGRESS_LAT`/`PTP_EGRESS_LAT` (0x540/0x544) stay inert
  //! scratch with no timestamp consumer, so nothing can apply a correction
  //! twice. Both are published read-only at `A_GPTP_LAT` (0x7F0) so a
  //! controller host and the UART status read what is actually applied.
  //! The defaults are zero, which is the uncorrected build.
  parameter int unsigned GPTP_INGRESS_LAT_NS_P = 0,
  parameter int unsigned GPTP_EGRESS_LAT_NS_P  = 0,
  //! Build key gptp.latency_writable (issue #829): those two words move the
  //! applied corrections at runtime and the pair above is their reset value.
  //! The plane stays the only consumer, so nothing applies a correction twice.
  parameter bit GPTP_LAT_WRITABLE_P = 1'b0,
"""),
("""  //! SCRATCH. PTP_*_LAT (0x540/0x544) are readable, inert scratch: plain RW
  //! with no timestamp-correction consumer at VERSION 0x0002_0057.
""", """  //! SCRATCH. PTP_*_LAT (0x540/0x544) are readable, inert scratch: plain RW
  //! with no timestamp-correction consumer at VERSION 0x0002_0057, unless
  //! the build sets GPTP_LAT_WRITABLE_P (issue #829).
"""),
("""  //! parameters, taken from the parameters and not from the plane, because
  //! there is nothing inside the plane to read them back from and a
  //! readback port would be a second copy of a constant.
  wire [31:0] gptp_lat_ns_pub_w = (GPTP_PLANE_EN_P != 1'b0)
                             ? {16'(GPTP_INGRESS_LAT_NS_P),
                                16'(GPTP_EGRESS_LAT_NS_P)} : 32'd0;
""", """  //! parameters, taken from the parameters and not from the plane, because
  //! there is nothing inside the plane to read them back from and a
  //! readback port would be a second copy of a constant. The CSR block drives
  //! both the plane and this word (issue #829), so under GPTP_LAT_WRITABLE_P
  //! this reads what is applied after every write.
  wire [15:0] gptp_lat_ing_w, gptp_lat_egr_w;
  wire [31:0] gptp_lat_ns_pub_w = (GPTP_PLANE_EN_P != 1'b0)
                             ? {gptp_lat_ing_w, gptp_lat_egr_w} : 32'd0;
"""),
("""    .MILAN_CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ),
    //! both chmap map-RAM read ports are wired below, and the CAPTURE side
""", """    .MILAN_CLK_FREQ_HZ_P(MILAN_CLK_FREQ_HZ),
    .GPTP_LAT_WRITABLE_P(GPTP_LAT_WRITABLE_P),
    .GPTP_INGRESS_LAT_NS_P(GPTP_INGRESS_LAT_NS_P),
    .GPTP_EGRESS_LAT_NS_P(GPTP_EGRESS_LAT_NS_P),
    //! both chmap map-RAM read ports are wired below, and the CAPTURE side
"""),
("""    .i_gptp_lat_ns           (gptp_lat_ns_pub_w),
""", """    .i_gptp_lat_ns           (gptp_lat_ns_pub_w),
    .o_gptp_lat_ingress_ns   (gptp_lat_ing_w),
    .o_gptp_lat_egress_ns    (gptp_lat_egr_w),
"""),
("""        .INGRESS_LAT_NS_P(GPTP_INGRESS_LAT_NS_P),
        .EGRESS_LAT_NS_P (GPTP_EGRESS_LAT_NS_P)
    ) u_gptp_shadow (
        .clk_i           (axis_clk),
        .rst_n           (axis_resetn),
""", """        .INGRESS_LAT_NS_P(GPTP_INGRESS_LAT_NS_P),
        .EGRESS_LAT_NS_P (GPTP_EGRESS_LAT_NS_P),
        .LAT_WRITABLE_P  (GPTP_LAT_WRITABLE_P)
    ) u_gptp_shadow (
        .clk_i           (axis_clk),
        .rst_n           (axis_resetn),
        .lat_ingress_ns_i(gptp_lat_ing_w),
        .lat_egress_ns_i (gptp_lat_egr_w),
"""),
])

patch("hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv", [
("""    //! remain inert scratch with no timestamp consumer, so a correction
    //! cannot be applied twice by two owners who each think they are the
    //! only one.
""", """    //! remain inert scratch with no timestamp consumer, so a correction
    //! cannot be applied twice by two owners who each think they are the
    //! only one. LAT_WRITABLE_P below moves the source of the values and not
    //! their owner.
"""),
("""    parameter int unsigned INGRESS_LAT_NS_P = 0,
    parameter int unsigned EGRESS_LAT_NS_P  = 0
) (
    input  wire clk_i,                    //! axis_clk
    input  wire rst_n,                    //! active-low reset
""", """    parameter int unsigned INGRESS_LAT_NS_P = 0,
    parameter int unsigned EGRESS_LAT_NS_P  = 0,
    //! Issue #829: take the two corrections from the ports below at runtime,
    //! with the pair above as their reset value, rather than from the
    //! parameters. The same arithmetic at the same point, and the same sign.
    parameter bit LAT_WRITABLE_P = 1'b0
) (
    input  wire clk_i,                    //! axis_clk
    input  wire rst_n,                    //! active-low reset

    //! the runtime corrections, nanoseconds, in this clock's domain; unread
    //! unless LAT_WRITABLE_P
    input  wire [15:0] lat_ingress_ns_i,
    input  wire [15:0] lat_egress_ns_i,
"""),
("""  //! value minus that path. At the default zero this is the raw value.
  logic [63:0] ts_arr_r;
  logic [63:0] ts_arr_corr_w;
  assign ts_arr_corr_w = phc_ns_i - 64'(INGRESS_LAT_NS_P);
""", """  //! value minus that path. At the default zero this is the raw value.
  //! A write under LAT_WRITABLE_P reaches this subtractor on its own edge, so
  //! a frame's arrival stamp carries one whole value (issue #829).
  logic [63:0] ts_arr_r;
  logic [63:0] ts_arr_corr_w;
  wire  [15:0] ingress_lat_w = LAT_WRITABLE_P ? lat_ingress_ns_i
                                              : 16'(INGRESS_LAT_NS_P);
  assign ts_arr_corr_w = phc_ns_i - 64'(ingress_lat_w);
"""),
("""      .EGRESS_LAT_NS_P(EGRESS_LAT_NS_P)
""", """      .EGRESS_LAT_NS_P(EGRESS_LAT_NS_P),
      .LAT_WRITABLE_P (LAT_WRITABLE_P)
"""),
])

patch("hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv", [
("""    //! into the same single subtraction. Zero reproduces the uncorrected
    //! reconstruction bit for bit.
    parameter int unsigned EGRESS_LAT_NS_P = 0,
""", """    //! into the same single subtraction. Zero reproduces the uncorrected
    //! reconstruction bit for bit.
    parameter int unsigned EGRESS_LAT_NS_P = 0,
    //! Issue #829: take that correction from lat_egress_ns_i at runtime, with
    //! EGRESS_LAT_NS_P as its reset value.
    parameter bit LAT_WRITABLE_P = 1'b0,
"""),
("""    input  wire rst_n,                 //! synchronous active-low reset

    //! the live PHC, in this clock's domain
""", """    input  wire rst_n,                 //! synchronous active-low reset

    //! the runtime egress correction, nanoseconds, in this clock's domain;
    //! unread unless LAT_WRITABLE_P
    input  wire [15:0] lat_egress_ns_i,

    //! the live PHC, in this clock's domain
"""),
("""  localparam longint signed TXTS_NET_NS_C =
      longint'(TXTS_CORR_NS_P) - longint'(EGRESS_LAT_NS_P);
""", """  localparam longint signed TXTS_NET_NS_C =
      longint'(TXTS_CORR_NS_P) - longint'(EGRESS_LAT_NS_P);
  //! ...and what that subtraction reads. Under LAT_WRITABLE_P the net is one
  //! register fed by the corrections' one flop, so the 64-bit subtractor keeps
  //! a registered operand and a write reaches it whole on one edge (issue
  //! #829). Eighteen signed bits hold the digital term less sixteen bits.
  logic [63:0] txts_net_ns_w;
  generate if (LAT_WRITABLE_P) begin : g_net_writable
    logic signed [17:0] net_r;
    always_ff @(posedge clk_i) begin
      if (!rst_n) net_r <= 18'(TXTS_NET_NS_C);
      else        net_r <= 18'(longint'(TXTS_CORR_NS_P) -
                               longint'(lat_egress_ns_i));
    end
    assign txts_net_ns_w = 64'(longint'(net_r));
  end else begin : g_net_constant
    assign txts_net_ns_w = 64'(TXTS_NET_NS_C);
  end endgenerate
"""),
("""  assign res_ns_w = res_ok_w ? (cap_phc_r - 64'(TXTS_NET_NS_C)) : 64'd0;
""", """  assign res_ns_w = res_ok_w ? (cap_phc_r - txts_net_ns_w) : 64'd0;
"""),
])

s = open(root + "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv", encoding="utf-8").read()
i = s.index("  KL_gptp_txret #(")
j = s.index(") u_", i)
k = s.index("(\n", j) + 2
line = s[j:k]
print("txret instance head:", repr(line))
s = s[:k] + "      .lat_egress_ns_i (lat_egress_ns_i),\n" + s[k:]
open(root + "hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv", "w", encoding="utf-8").write(s)

patch("tb/verilator/gptp_shadow/gptp_shadow_wrap.sv", [
("""  ) u_shadow (
""", """  ) u_shadow (
      .lat_ingress_ns_i (16'd0),
      .lat_egress_ns_i  (16'd0),
"""),
])
patch("tb/verilator/gptp_txts/gptp_txts_wrap.sv", [
("""    parameter int unsigned ETH_CYC_PER_OCTET_P = 1,
    //! the guard's settle, scaled so a bench can afford a whole episode.
""", """    parameter int unsigned ETH_CYC_PER_OCTET_P = 1,
    //! issue #829: the corrections below reach the plane's stamps at runtime
    parameter bit          LAT_WRITABLE_P = 1'b0,
    //! the guard's settle, scaled so a bench can afford a whole episode.
"""),
("""    input  wire eth_rst_n,

    //! the plane's RX tap: peer frames enter here, through the real
""", """    input  wire eth_rst_n,

    //! the runtime corrections, nanoseconds, driven as the CSR block's flops do
    input  wire [15:0] lat_ingress_ns_i,
    input  wire [15:0] lat_egress_ns_i,

    //! the plane's RX tap: peer frames enter here, through the real
"""),
("""      .ETH_CYC_PER_OCTET_P (ETH_CYC_PER_OCTET_P)
  ) u_shadow (
      .clk_i            (dp_clk_i),
""", """      .ETH_CYC_PER_OCTET_P (ETH_CYC_PER_OCTET_P),
      .LAT_WRITABLE_P   (LAT_WRITABLE_P)
  ) u_shadow (
      .lat_ingress_ns_i (lat_ingress_ns_i),
      .lat_egress_ns_i  (lat_egress_ns_i),
      .clk_i            (dp_clk_i),
"""),
])

patch("sw/builder/endstation_builder.py", [
("""                         if k not in ("ingress_latency_ns",
                                      "egress_latency_ns")}
""", """                         if k not in ("ingress_latency_ns",
                                      "egress_latency_ns",
                                      "latency_writable")}
"""),
("""                     "ingress_latency_ns", "egress_latency_ns"}
        if not isinstance(gp_raw, dict) or set(gp_raw) - _known_gp:
""", """                     "ingress_latency_ns", "egress_latency_ns",
                     "latency_writable"}
        if not isinstance(gp_raw, dict) or set(gp_raw) - _known_gp:
"""),
("""        gptp = dict(
            port_number=gptp_engine_port_number(),
""", """        #! Off by default, and a yes/no the YAML must spell as one (#829): a
        #! board that does not state it builds exactly what it built before.
        _lat_writable = gp_raw.get("latency_writable", False)
        if not isinstance(_lat_writable, bool):
            raise ConfigError(f"gptp.latency_writable {_lat_writable!r} is "
                              f"not true or false (#829)")
        gptp = dict(
            port_number=gptp_engine_port_number(),
            latency_writable=_lat_writable,
"""),
("""            argv += [flag, str(cfg["gptp"][key])]
    return argv
""", """            argv += [flag, str(cfg["gptp"][key])]
    # issue #829: absent unless the board states it, the same discipline.
    if cfg["gptp"]["latency_writable"]:
        argv += ["--gptp-lat-writable"]
    return argv
"""),
("""            out[param] = int(cfg["gptp"][key])
    # The processor window of emit_platform_shape: the descriptor image at
""", """            out[param] = int(cfg["gptp"][key])
    if cfg["gptp"]["latency_writable"]:
        out["GPTP_LAT_WRITABLE_P"] = 1
    # The processor window of emit_platform_shape: the descriptor image at
"""),
("""                     if k not in ("ingress_latency_ns", "egress_latency_ns")}}
""", """                     if k not in ("ingress_latency_ns", "egress_latency_ns",
                                  "latency_writable")}}
"""),
])
patch("sw/litex/milan_soc.py", [
("""                 gptp_ingress_lat_ns=0, gptp_egress_lat_ns=0,
                 """ , """XX""") if False else ("""                       gptp_egress_lat_ns: int = 0,
""", """                       gptp_egress_lat_ns: int = 0,
                       gptp_lat_writable: bool = False,
"""),
("""        dp_params["p_GPTP_EGRESS_LAT_NS_P"] = int(gptp_egress_lat_ns)
""", """        dp_params["p_GPTP_EGRESS_LAT_NS_P"] = int(gptp_egress_lat_ns)
    # issue #829: the same discipline, so a board that does not ask keeps its
    # generated top .v.
    if gptp_lat_writable:
        dp_params["p_GPTP_LAT_WRITABLE_P"] = 1
"""),
("""                           gptp_egress_lat_ns=gptp_egress_lat_ns,
""", """                           gptp_egress_lat_ns=gptp_egress_lat_ns,
                           gptp_lat_writable=gptp_lat_writable,
"""),
("""                                  gptp_egress_lat_ns=int(gptp_egress_lat_ns),
""", """                                  gptp_egress_lat_ns=int(gptp_egress_lat_ns),
                                  gptp_lat_writable=bool(gptp_lat_writable),
"""),
("""                   gptp_egress_lat_ns=args.gptp_egress_lat_ns,
""", """                   gptp_egress_lat_ns=args.gptp_egress_lat_ns,
                   gptp_lat_writable=args.gptp_lat_writable,
"""),
("""                                  "top of the plane's own measured register "
                                  "stages; 0..65535")
""", """                                  "top of the plane's own measured register "
                                  "stages; 0..65535")
    gptp_group2.add_argument("--gptp-lat-writable", action="store_true",
                             help="let CSR 0x540 and 0x544 move the two "
                                  "corrections at runtime, the pair above "
                                  "being only their reset value (milan_datapath "
                                  "GPTP_LAT_WRITABLE_P, issue #829). Off, those "
                                  "words stay inert scratch")
"""),
("""    # The fabric gPTP plane is the only consumer; 0x540/0x544 stay inert.
""", """    # The fabric gPTP plane is the only consumer; 0x540/0x544 stay inert
    # unless --gptp-lat-writable.
"""),
])
s = open(root + "sw/litex/milan_soc.py", encoding="utf-8").read()
old = "gptp_ingress_lat_ns=0, gptp_egress_lat_ns=0,\n"
assert s.count(old) == 2, s.count(old)
s = s.replace(old, "gptp_ingress_lat_ns=0, gptp_egress_lat_ns=0,\n                 gptp_lat_writable=False,\n")
open(root + "sw/litex/milan_soc.py", "w", encoding="utf-8").write(s)

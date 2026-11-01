#!/usr/bin/env python3
"""Move the writable corrections' flops out of milan_csr into milan_datapath, so the CSR block's port list stays the frozen oracle's."""
root = "$VALIDATION_STORAGE/829-a725/wt-bench/"
def patch(path, pairs):
    p = root + path
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8").write(s)
patch("hdl/common/csr/milan_csr.sv", [
("""  //! THE WRITABLE LATENCY CORRECTIONS (issue #829, build key
  //! gptp.latency_writable). Off, 0x540 and 0x544 stay inert scratch that
  //! resets to zero, nothing below elaborates, and the two outputs carry the
  //! elaboration constants. On, a write to either word moves the correction
  //! the plane applies and the build-time pair is only their reset value.
""", """  //! THE WRITABLE LATENCY CORRECTIONS (issue #829, build key
  //! gptp.latency_writable). Off, 0x540 and 0x544 stay inert scratch that
  //! resets to zero. On, milan_datapath applies [15:0] of a write to either
  //! word and these two words reset to the build-time pair, so that a read
  //! returns what is applied until the first write.
"""),
("""  //! The corrections the plane applies, in this block's own clock domain,
  //! which is the plane's (issue #829): the constants unless
  //! GPTP_LAT_WRITABLE_P, then [15:0] of the last write to each word.
  output wire [15:0]             o_gptp_lat_ingress_ns,
  output wire [15:0]             o_gptp_lat_egress_ns,
""", ""),
("""  //! The applied corrections (issue #829). One flop per direction, because the
  //! shadow RAM that serves the read-back has no consumer port, so one write
  //! changes one direction on one edge and a stamp reads a whole value.
  localparam logic [31:0] PTP_ILAT_RST_C =
""", """  //! The reset image of the two correction words (issue #829).
  localparam logic [31:0] PTP_ILAT_RST_C =
"""),
("""  generate if (GPTP_LAT_WRITABLE_P) begin : g_lat_writable
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

""", """
"""),
])
patch("hdl/milan/milan_datapath.sv", [
("""  //! readback port would be a second copy of a constant. The CSR block drives
  //! both the plane and this word (issue #829), so under GPTP_LAT_WRITABLE_P
  //! this reads what is applied after every write.
  wire [15:0] gptp_lat_ing_w, gptp_lat_egr_w;
  wire [31:0] gptp_lat_ns_pub_w = (GPTP_PLANE_EN_P != 1'b0)
""", """  //! readback port would be a second copy of a constant. Under
  //! GPTP_LAT_WRITABLE_P (issue #829) the source is one flop per direction: the
  //! CSR block's shadow RAM has no consumer port, so these take the same write,
  //! on its AWREADY, which that block raises for exactly the cycle it fires.
  //! One write changes one direction on one edge and a stamp reads a whole
  //! value. Both sides are axis_clk, so no crossing lies between them, and this
  //! word reads what is applied after every write.
  wire [15:0] gptp_lat_ing_w, gptp_lat_egr_w;
  generate if (GPTP_LAT_WRITABLE_P) begin : g_gptp_lat_writable
    localparam logic [15:0] A_PTP_ILAT_C = 16'h0540;
    localparam logic [15:0] A_PTP_ELAT_C = 16'h0544;
    logic [15:0] lat_ing_r, lat_egr_r;
    always_ff @(posedge axis_clk) begin
      if (!axis_resetn) begin
        lat_ing_r <= 16'(GPTP_INGRESS_LAT_NS_P);
        lat_egr_r <= 16'(GPTP_EGRESS_LAT_NS_P);
      end else if (s_axi_awready) begin
        if (s_axi_awaddr == A_PTP_ILAT_C) lat_ing_r <= s_axi_wdata[15:0];
        if (s_axi_awaddr == A_PTP_ELAT_C) lat_egr_r <= s_axi_wdata[15:0];
      end
    end
    assign gptp_lat_ing_w = lat_ing_r;
    assign gptp_lat_egr_w = lat_egr_r;
  end else begin : g_gptp_lat_constant
    assign gptp_lat_ing_w = 16'(GPTP_INGRESS_LAT_NS_P);
    assign gptp_lat_egr_w = 16'(GPTP_EGRESS_LAT_NS_P);
  end endgenerate
  wire [31:0] gptp_lat_ns_pub_w = (GPTP_PLANE_EN_P != 1'b0)
"""),
("""    .o_gptp_lat_ingress_ns   (gptp_lat_ing_w),
    .o_gptp_lat_egress_ns    (gptp_lat_egr_w),
""", ""),
])
patch("docs/litex/CLOCK_DOMAINS.md", [
("""- That key's flops sit in `axis_clk`, the plane's own clock, so it adds no crossing.
""", """- That key's flops sit in `milan_datapath`'s `axis_clk`, the plane's own clock and the CSR block's, so it adds no crossing.
"""),
])

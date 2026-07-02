//Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
//Copyright 2022-2025 Advanced Micro Devices, Inc. All Rights Reserved.
//--------------------------------------------------------------------------------
//Tool Version: Vivado v.2025.1 (lin64) Build 6140274 Wed May 21 22:58:25 MDT 2025
//Date        : Fri Aug  8 21:51:31 2025
//Host        : oguzk-Desktop running 64-bit Ubuntu 22.04.5 LTS
//Command     : generate_target milan_dma_wrapper.bd
//Design      : milan_dma_wrapper
//Purpose     : IP block netlist
//--------------------------------------------------------------------------------
// MANUAL EXTENSION (2026-07-01, Kebag Logic): the AXI4-Lite CSR master
// (M_AXI_CSR, driven by the PS M_AXI_GP0 via axi_smc M02) and the CSR interrupt
// input (irq_csr, into ilconcat In3) were added to expose the milan_csr control
// plane to milan_top. This mirrors the edits in bd/milan-dma.tcl; regenerate
// this wrapper from that .tcl in Vivado (`generate_target`) to keep it in sync.
// The M_AXI_CSR window is 64 KB at 0x43C0_0000 (see docs/REGISTER_MAP.md).
//--------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module milan_dma_wrapper
   (m_axi_csr_awaddr,
    m_axi_csr_awprot,
    m_axi_csr_awvalid,
    m_axi_csr_awready,
    m_axi_csr_wdata,
    m_axi_csr_wstrb,
    m_axi_csr_wvalid,
    m_axi_csr_wready,
    m_axi_csr_bresp,
    m_axi_csr_bvalid,
    m_axi_csr_bready,
    m_axi_csr_araddr,
    m_axi_csr_arprot,
    m_axi_csr_arvalid,
    m_axi_csr_arready,
    m_axi_csr_rdata,
    m_axi_csr_rresp,
    m_axi_csr_rvalid,
    m_axi_csr_rready,
    irq_csr,
    DDR_addr,
    DDR_ba,
    DDR_cas_n,
    DDR_ck_n,
    DDR_ck_p,
    DDR_cke,
    DDR_cs_n,
    DDR_dm,
    DDR_dq,
    DDR_dqs_n,
    DDR_dqs_p,
    DDR_odt,
    DDR_ras_n,
    DDR_reset_n,
    DDR_we_n,
    FIXED_IO_ddr_vrn,
    FIXED_IO_ddr_vrp,
    FIXED_IO_mio,
    FIXED_IO_ps_clk,
    FIXED_IO_ps_porb,
    FIXED_IO_ps_srstb,
    MDIO_link_1_mdc,
    MDIO_link_1_mdio_io,
    axis_clk,
    axis_resetn,
    gtx90_clk,
    gtx_clk,
    gtx_reset_n,
    m_axis_tx_eth_tdata,
    m_axis_tx_eth_tkeep,
    m_axis_tx_eth_tlast,
    m_axis_tx_eth_tready,
    m_axis_tx_eth_tvalid,
    s_axis_rx_eth_tdata,
    s_axis_rx_eth_tkeep,
    s_axis_rx_eth_tlast,
    s_axis_rx_eth_tready,
    s_axis_rx_eth_tvalid,
    s_axis_ts_metadata_tdata,
    s_axis_ts_metadata_tkeep,
    s_axis_ts_metadata_tlast,
    s_axis_ts_metadata_tready,
    s_axis_ts_metadata_tvalid);
  // AXI4-Lite CSR master (from PS M_AXI_GP0 via axi_smc M02), 32b data / 32b addr
  output [31:0]m_axi_csr_awaddr;
  output [2:0]m_axi_csr_awprot;
  output m_axi_csr_awvalid;
  input m_axi_csr_awready;
  output [31:0]m_axi_csr_wdata;
  output [3:0]m_axi_csr_wstrb;
  output m_axi_csr_wvalid;
  input m_axi_csr_wready;
  input [1:0]m_axi_csr_bresp;
  input m_axi_csr_bvalid;
  output m_axi_csr_bready;
  output [31:0]m_axi_csr_araddr;
  output [2:0]m_axi_csr_arprot;
  output m_axi_csr_arvalid;
  input m_axi_csr_arready;
  input [31:0]m_axi_csr_rdata;
  input [1:0]m_axi_csr_rresp;
  input m_axi_csr_rvalid;
  output m_axi_csr_rready;
  // CSR level interrupt into PS IRQ_F2P (ilconcat In3)
  input irq_csr;
  inout [14:0]DDR_addr;
  inout [2:0]DDR_ba;
  inout DDR_cas_n;
  inout DDR_ck_n;
  inout DDR_ck_p;
  inout DDR_cke;
  inout DDR_cs_n;
  inout [3:0]DDR_dm;
  inout [31:0]DDR_dq;
  inout [3:0]DDR_dqs_n;
  inout [3:0]DDR_dqs_p;
  inout DDR_odt;
  inout DDR_ras_n;
  inout DDR_reset_n;
  inout DDR_we_n;
  inout FIXED_IO_ddr_vrn;
  inout FIXED_IO_ddr_vrp;
  inout [53:0]FIXED_IO_mio;
  inout FIXED_IO_ps_clk;
  inout FIXED_IO_ps_porb;
  inout FIXED_IO_ps_srstb;
  output MDIO_link_1_mdc;
  inout MDIO_link_1_mdio_io;
  output axis_clk;
  output [0:0]axis_resetn;
  output gtx90_clk;
  output gtx_clk;
  output [0:0]gtx_reset_n;
  output [63:0]m_axis_tx_eth_tdata;
  output [7:0]m_axis_tx_eth_tkeep;
  output m_axis_tx_eth_tlast;
  input m_axis_tx_eth_tready;
  output m_axis_tx_eth_tvalid;
  input [63:0]s_axis_rx_eth_tdata;
  input [7:0]s_axis_rx_eth_tkeep;
  input s_axis_rx_eth_tlast;
  output s_axis_rx_eth_tready;
  input s_axis_rx_eth_tvalid;
  input [63:0]s_axis_ts_metadata_tdata;
  input [7:0]s_axis_ts_metadata_tkeep;
  input s_axis_ts_metadata_tlast;
  output s_axis_ts_metadata_tready;
  input s_axis_ts_metadata_tvalid;

  wire [14:0]DDR_addr;
  wire [2:0]DDR_ba;
  wire DDR_cas_n;
  wire DDR_ck_n;
  wire DDR_ck_p;
  wire DDR_cke;
  wire DDR_cs_n;
  wire [3:0]DDR_dm;
  wire [31:0]DDR_dq;
  wire [3:0]DDR_dqs_n;
  wire [3:0]DDR_dqs_p;
  wire DDR_odt;
  wire DDR_ras_n;
  wire DDR_reset_n;
  wire DDR_we_n;
  wire FIXED_IO_ddr_vrn;
  wire FIXED_IO_ddr_vrp;
  wire [53:0]FIXED_IO_mio;
  wire FIXED_IO_ps_clk;
  wire FIXED_IO_ps_porb;
  wire FIXED_IO_ps_srstb;
  wire MDIO_link_1_mdc;
  wire MDIO_link_1_mdio_i;
  wire MDIO_link_1_mdio_io;
  wire MDIO_link_1_mdio_o;
  wire MDIO_link_1_mdio_t;
  wire axis_clk;
  wire [0:0]axis_resetn;
  wire gtx90_clk;
  wire gtx_clk;
  wire [0:0]gtx_reset_n;
  wire [63:0]m_axis_tx_eth_tdata;
  wire [7:0]m_axis_tx_eth_tkeep;
  wire m_axis_tx_eth_tlast;
  wire m_axis_tx_eth_tready;
  wire m_axis_tx_eth_tvalid;
  wire [63:0]s_axis_rx_eth_tdata;
  wire [7:0]s_axis_rx_eth_tkeep;
  wire s_axis_rx_eth_tlast;
  wire s_axis_rx_eth_tready;
  wire s_axis_rx_eth_tvalid;
  wire [63:0]s_axis_ts_metadata_tdata;
  wire [7:0]s_axis_ts_metadata_tkeep;
  wire s_axis_ts_metadata_tlast;
  wire s_axis_ts_metadata_tready;
  wire s_axis_ts_metadata_tvalid;

  // Inferred tristate MDIO pad (T2.1): portable — Vivado infers an IOBUF from this
  // on the top-level inout, other toolchains model the tristate directly. Replaces
  // the Xilinx IOBUF primitive (docs/OPEN_SOURCE_MIGRATION.md).
  assign MDIO_link_1_mdio_io = MDIO_link_1_mdio_t ? 1'bz : MDIO_link_1_mdio_o;
  assign MDIO_link_1_mdio_i  = MDIO_link_1_mdio_io;
  milan_dma milan_dma_i
       (.m_axi_csr_awaddr(m_axi_csr_awaddr),
        .m_axi_csr_awprot(m_axi_csr_awprot),
        .m_axi_csr_awvalid(m_axi_csr_awvalid),
        .m_axi_csr_awready(m_axi_csr_awready),
        .m_axi_csr_wdata(m_axi_csr_wdata),
        .m_axi_csr_wstrb(m_axi_csr_wstrb),
        .m_axi_csr_wvalid(m_axi_csr_wvalid),
        .m_axi_csr_wready(m_axi_csr_wready),
        .m_axi_csr_bresp(m_axi_csr_bresp),
        .m_axi_csr_bvalid(m_axi_csr_bvalid),
        .m_axi_csr_bready(m_axi_csr_bready),
        .m_axi_csr_araddr(m_axi_csr_araddr),
        .m_axi_csr_arprot(m_axi_csr_arprot),
        .m_axi_csr_arvalid(m_axi_csr_arvalid),
        .m_axi_csr_arready(m_axi_csr_arready),
        .m_axi_csr_rdata(m_axi_csr_rdata),
        .m_axi_csr_rresp(m_axi_csr_rresp),
        .m_axi_csr_rvalid(m_axi_csr_rvalid),
        .m_axi_csr_rready(m_axi_csr_rready),
        .irq_csr(irq_csr),
        .DDR_addr(DDR_addr),
        .DDR_ba(DDR_ba),
        .DDR_cas_n(DDR_cas_n),
        .DDR_ck_n(DDR_ck_n),
        .DDR_ck_p(DDR_ck_p),
        .DDR_cke(DDR_cke),
        .DDR_cs_n(DDR_cs_n),
        .DDR_dm(DDR_dm),
        .DDR_dq(DDR_dq),
        .DDR_dqs_n(DDR_dqs_n),
        .DDR_dqs_p(DDR_dqs_p),
        .DDR_odt(DDR_odt),
        .DDR_ras_n(DDR_ras_n),
        .DDR_reset_n(DDR_reset_n),
        .DDR_we_n(DDR_we_n),
        .FIXED_IO_ddr_vrn(FIXED_IO_ddr_vrn),
        .FIXED_IO_ddr_vrp(FIXED_IO_ddr_vrp),
        .FIXED_IO_mio(FIXED_IO_mio),
        .FIXED_IO_ps_clk(FIXED_IO_ps_clk),
        .FIXED_IO_ps_porb(FIXED_IO_ps_porb),
        .FIXED_IO_ps_srstb(FIXED_IO_ps_srstb),
        .MDIO_link_1_mdc(MDIO_link_1_mdc),
        .MDIO_link_1_mdio_i(MDIO_link_1_mdio_i),
        .MDIO_link_1_mdio_o(MDIO_link_1_mdio_o),
        .MDIO_link_1_mdio_t(MDIO_link_1_mdio_t),
        .axis_clk(axis_clk),
        .axis_resetn(axis_resetn),
        .gtx90_clk(gtx90_clk),
        .gtx_clk(gtx_clk),
        .gtx_reset_n(gtx_reset_n),
        .m_axis_tx_eth_tdata(m_axis_tx_eth_tdata),
        .m_axis_tx_eth_tkeep(m_axis_tx_eth_tkeep),
        .m_axis_tx_eth_tlast(m_axis_tx_eth_tlast),
        .m_axis_tx_eth_tready(m_axis_tx_eth_tready),
        .m_axis_tx_eth_tvalid(m_axis_tx_eth_tvalid),
        .s_axis_rx_eth_tdata(s_axis_rx_eth_tdata),
        .s_axis_rx_eth_tkeep(s_axis_rx_eth_tkeep),
        .s_axis_rx_eth_tlast(s_axis_rx_eth_tlast),
        .s_axis_rx_eth_tready(s_axis_rx_eth_tready),
        .s_axis_rx_eth_tvalid(s_axis_rx_eth_tvalid),
        .s_axis_ts_metadata_tdata(s_axis_ts_metadata_tdata),
        .s_axis_ts_metadata_tkeep(s_axis_ts_metadata_tkeep),
        .s_axis_ts_metadata_tlast(s_axis_ts_metadata_tlast),
        .s_axis_ts_metadata_tready(s_axis_ts_metadata_tready),
        .s_axis_ts_metadata_tvalid(s_axis_ts_metadata_tvalid));
endmodule

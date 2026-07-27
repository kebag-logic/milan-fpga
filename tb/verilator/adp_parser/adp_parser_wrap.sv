/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * Flat-port wrapper around KL_adp_parser (axi_stream_if slave port + a packed
 * entity_info_t output) so a Verilator harness can drive and observe it.
 *
 * WHY THIS EXISTS AT ALL: KL_adp_parser was the one ADP module with no
 * Verilator suite - its only testbench is the Vivado xsim one under
 * tb/utests/adp/kl-adp-parser/ - and that is exactly why an uncast enum
 * assignment (%Error-ENUMVALUE, KL_adp_parser.sv:81) sat in it undetected:
 * nothing in CI ever compiled the file.
 */
`default_nettype none

module adp_parser_wrap
  import adp_pkg::*;
(
  input  wire        clk,
  input  wire        rst_n,
  // AXI4-Stream slave in - the stream starts at the ETHERTYPE, which is the
  // contract the xsim TB's packet generator drives (avtp_control_subtype
  // pushes ether_type[15:8], ether_type[7:0], subtype and nothing before).
  input  wire [63:0] s_tdata,
  input  wire        s_tvalid,
  input  wire        s_tlast,
  output wire        s_tready,
  // parsed struct, flattened
  output wire        rcv_adp_discover_o,
  output wire        rcv_adp_available_o,
  output wire        rcv_adp_departing_o,
  output wire        entity_info_valid_o,
  output wire [3:0]  adp_message_type_o,   //! RAW 4-bit wire code, not clamped
  output wire [4:0]  valid_time_o,
  output wire [63:0] entity_id_o,
  output wire [63:0] entity_model_id_o,
  output wire [31:0] entity_capabilities_o,
  output wire [15:0] talker_stream_sources_o,
  output wire [15:0] talker_capabilities_o,
  output wire [15:0] listener_stream_sinks_o,
  output wire [15:0] listener_capabilities_o,
  output wire [31:0] controller_capabilities_o,
  output wire [31:0] available_index_o,
  output wire [63:0] gptp_grandmaster_id_o,
  output wire [7:0]  gptp_domain_number_o,
  output wire [15:0] current_configuration_index_o,
  output wire [15:0] identify_control_index_o,
  output wire [15:0] interface_index_o,
  output wire [63:0] association_id_o
);

  //! clk/rst_n are passed even though neither modport carries them and
  //! nothing reads them (see the PINMISSING waiver in scripts/lint_rtl.py) -
  //! tb/utests/adp/kl-adp-parser/tb_top.sv writes it the same way.
  axi_stream_if #(.TDATA_WIDTH_P(64)) s_axis(clk, rst_n);

  assign s_axis.tdata  = s_tdata;
  assign s_axis.tvalid = s_tvalid;
  assign s_axis.tlast  = s_tlast;
  assign s_axis.tkeep  = 8'hFF;
  assign s_axis.tstrb  = 8'hFF;
  assign s_axis.tid    = '0;
  assign s_axis.tdest  = '0;
  assign s_axis.tuser  = '0;
  assign s_tready      = s_axis.tready;

  entity_info_t info_w;

  KL_adp_parser dut (
    .clk_i               (clk),
    .rst_n               (rst_n),
    .s_axis              (s_axis),
    .rcv_adp_discover_o  (rcv_adp_discover_o),
    .rcv_adp_available_o (rcv_adp_available_o),
    .rcv_adp_departing_o (rcv_adp_departing_o),
    .rcv_entity_info_o   (info_w)
  );

  //! the enum member is read back as its raw 4 bits: adp05 asserts a reserved
  //! wire code survives here unmodified, which is what pins the "no clamp"
  //! decision recorded at KL_adp_parser.sv:81.
  assign adp_message_type_o            = 4'(info_w.adp_message_type);
  assign entity_info_valid_o           = info_w.entity_info_valid;
  assign valid_time_o                  = info_w.valid_time;
  assign entity_id_o                   = info_w.entity_id;
  assign entity_model_id_o             = info_w.entity_model_id;
  assign entity_capabilities_o         = info_w.entity_capabilities;
  assign talker_stream_sources_o       = info_w.talker_stream_sources;
  assign talker_capabilities_o         = info_w.talker_capabilities;
  assign listener_stream_sinks_o       = info_w.listener_stream_sinks;
  assign listener_capabilities_o       = info_w.listener_capabilities;
  assign controller_capabilities_o     = info_w.controller_capabilities;
  assign available_index_o             = info_w.available_index;
  assign gptp_grandmaster_id_o         = info_w.gptp_grandmaster_id;
  assign gptp_domain_number_o          = info_w.gptp_domain_number;
  assign current_configuration_index_o = info_w.current_configuration_index;
  assign identify_control_index_o      = info_w.identify_control_index;
  assign interface_index_o             = info_w.interface_index;
  assign association_id_o              = info_w.association_id;

endmodule

`default_nettype wire

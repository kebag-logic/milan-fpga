/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

module tb_top();

  `include "avtp_packet_gen_pkg.svh"
  `include "axi_stream_driver.svh"

  //! AVTP Packet gen related
  avtp_control_subtype avtp_control_pkt;
  subtype_t subtype;
  avtp_common_hdr_t avtp_common_hdr;
  logic [7:0] pkt[$];
  //! ADP Classes and structs
  avtp_adp_packet_gen avtp_adp_pkt_gen;
  avtp_adp_t avtp_adp_pkt;
  //! Struct for parsed ADP packet
  entity_info_t rcvd_entity_info;
   
  //! Parameters for AXI4-Stream interface and Clock
  parameter TDATA_WIDTH_P = 64;
  parameter T = 10;

  bit clk;
  bit rst_n;
  reg [63:0] total_packet_parsed = '0;

  //! Interfaces
  axi_stream_if #(.TDATA_WIDTH_P(TDATA_WIDTH_P)) s_axis_top(clk, rst_n);
  axi_stream_driver #(.CLK_PERIOD_P(T), .TDATA_WIDTH_P(TDATA_WIDTH_P)) axis_driver;

  //! DUT instantiation
  KL_adp_parser DUT
  (
    .clk_i(clk),
    .rst_n(rst_n),
    .s_axis(s_axis_top),
    .rcv_entity_info_o(rcvd_entity_info)
  );

  //! Clock generation for 5ns period (100 MHz)
  always #(T/2) clk = ~clk;

  // ------------------------------------------------------------------
  //! Task for resetting the DUT.
  task reset_dut;
    #100;
    $display("[INFO][TOP] : Reseting the DUT");
    rst_n = 1'd1;
  endtask

  // ------------------------------------------------------------------
  //! @brief Check that the parsed packet is the same as generated one.
  //! @param[in] None.
  //! @param[out] Status 
  function bit check_parsed_fields;
    bit status = 1;
    status &= (rcvd_entity_info.adp_message_type            == avtp_adp_pkt.adp_message_type);
    status &= (rcvd_entity_info.valid_time                  == avtp_adp_pkt.valid_time);
    status &= (rcvd_entity_info.entity_id                   == avtp_adp_pkt.entity_id);
    status &= (rcvd_entity_info.entity_model_id             == avtp_adp_pkt.entity_model_id);
    status &= (rcvd_entity_info.entity_capabilities         == avtp_adp_pkt.entity_capabilities);
    status &= (rcvd_entity_info.talker_stream_sources       == avtp_adp_pkt.talker_stream_sources);
    status &= (rcvd_entity_info.talker_capabilities         == avtp_adp_pkt.talker_capabilities);
    status &= (rcvd_entity_info.listener_stream_sinks       == avtp_adp_pkt.listener_stream_sinks);
    status &= (rcvd_entity_info.listener_capabilities       == avtp_adp_pkt.listener_capabilities);
    status &= (rcvd_entity_info.controller_capabilities     == avtp_adp_pkt.controller_capabilities);
    status &= (rcvd_entity_info.available_index             == avtp_adp_pkt.available_index);
    status &= (rcvd_entity_info.gptp_grandmaster_id         == avtp_adp_pkt.gptp_grandmaster_id);
    status &= (rcvd_entity_info.listener_stream_sinks       == avtp_adp_pkt.listener_stream_sinks);
    status &= (rcvd_entity_info.gptp_domain_number          == avtp_adp_pkt.gptp_domain_number);
    status &= (rcvd_entity_info.current_configuration_index == avtp_adp_pkt.current_configuration_index);
    status &= (rcvd_entity_info.identify_control_index      == avtp_adp_pkt.identify_control_index);
    status &= (rcvd_entity_info.interface_index             == avtp_adp_pkt.interface_index);
    status &= (rcvd_entity_info.association_id              == avtp_adp_pkt.association_id);
    return status;
  endfunction

  // ------------------------------------------------------------------
  //! @brief Check total packet generated is equal to the parsed packets.
  //! @param[in] None.
  //! @param[out] None. 
  task check_total_vs_parsed;
    $display("[INFO][TOP] : The Total # of ADP Packets Generated %d", avtp_control_pkt.count);
    $display("[INFO][TOP] : The Total # of ADP Packets Parsed %d", total_packet_parsed);
    if (total_packet_parsed != avtp_control_pkt.count)
      $fatal("[TOP] : # of Packet Generated is NOT equal to # of Packet Parsed");
  endtask

  //! Main TB
  initial begin
    axis_driver = new();
    axis_driver.axis_if = s_axis_top;
    reset_dut();
    $display("[TOP] : Generating ADP Packet");
    avtp_adp_pkt_gen = new();
      
    for (int i = 0; i < 100; i++) begin
      subtype = avtp_adp_pkt_gen.subtype_gen();
      avtp_common_hdr = avtp_adp_pkt_gen.subtype_header_gen();
      avtp_adp_pkt_gen.avtp_packet_gen(pkt);
      avtp_adp_pkt = avtp_adp_pkt_gen.adp_packet_gen(pkt);
      #150;
      fork
        //! AXI4-Stream drive
        begin
          axis_driver.drive_axi_stream(pkt);
        end
        //! Check the entity_info_valid
        begin
          @(posedge rcvd_entity_info.entity_info_valid);
        end
      join
      total_packet_parsed++;
      if (!check_parsed_fields())
        $fatal("[TOP] : Parsed Packet Fields are not match with generated packet");
    end

    check_total_vs_parsed();
    $display("[INFO][TOP] : UTEST for KL_ADP_PARSER IS SUCCESFULLY COMPLETED");
    $finish;
  end

endmodule
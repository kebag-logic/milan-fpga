//---------------------------------------------------------------------------//
/*
  LICENSE INFORMATION
*/
//---------------------------------------------------------------------------//

//---------------------------------------------------------------------------//
/*
Company: KebagLogics
Contributors: Cemal Dogan
Create Date: 08/06/2025 - 17:05 PM (CET+3)
Module Name: KL_discovery_top
Project Name:
Target Devices:
Tool Versions:

Description: Top module for KL_discovery_controller and KL_discovery_state.
Instantiate MAX_BOUNDED_TALKER_CNT_C KL_discovery_state module. Connect them to
the KL_discovery_controller.

Notes:

Dependencies:

Revision:
Revision 0.01 - File Created
Additional Comments:
*/
//---------------------------------------------------------------------------//


`default_nettype none

import adp_pkg::*; 

module KL_discovery_top
  (
    input wire clk_i,
    input wire rst_n,

    // From ACMP Top
    input wire [63:0] talker_entity_id_i,
    input wire talker_entity_id_valid_i,
    input wire talker_departed_i,

    // From PTP module
    input wire [63:0] gptp_grandmaster_id_i,
    input wire [7:0] gptp_domain_number_i,

    // From KL_adp_parser
    input wire rcv_adp_available_i,
    input wire rcv_adp_departing_i,
    input wire [63:0] rcv_entity_id_i,
    input wire [31:0] rcv_available_index_i,
    input wire [15:0] rcv_interface_index_i,
    input wire [63:0] rcv_gptp_grandmaster_id_i,
    input wire [7:0] rcv_gptp_domain_number_i,
    input wire [4:0] rcv_valid_time_i,

    output adp_to_acmp_event_t adp_to_acmp_event

  );



  // ---------- CONSTANT DECLARATION ---------- //

  // ---------- REG/WIRE DECLARATION ---------- //
  wire [31:0] rcv_available_index_w;
  wire [15:0] rcv_interface_index_w;
  wire [4:0] rcv_valid_time_w;
  wire [63:0] rcv_gptp_grandmaster_id_w;
  wire [7:0] rcv_gptp_domain_number_w;

  wire [MAX_BOUNDED_TALKER_CNT_C-1:0] active_talker_w;
  adp_discovery_event_t discovery_events_w;

  genvar i;
  // ---------- MODULE INSTANTIATIONS ---------- //

  KL_discovery_controller KL_DISCOVERY_CONTROLLER (
    .clk_i(clk_i),
    .rst_n(rst_n),
    .talker_entity_id_i(talker_entity_id_i),
    .talker_entity_id_valid_i(talker_entity_id_valid_i),
    .talker_departed_i(talker_departed_i),
    .rcv_adp_available_i(rcv_adp_available_i),
    .rcv_adp_departing_i(rcv_adp_departing_i),
    .rcv_entity_id_i(rcv_entity_id_i),
    .rcv_available_index_i(rcv_available_index_i),
    .rcv_interface_index_i(rcv_interface_index_i),
    .rcv_gptp_grandmaster_id_i(rcv_gptp_grandmaster_id_i),
    .rcv_gptp_domain_number_i(rcv_gptp_domain_number_i),
    .rcv_valid_time_i(rcv_valid_time_i),

    .rcv_available_index_o(rcv_available_index_w),
    .rcv_interface_index_o(rcv_interface_index_w),
    .rcv_valid_time_o(rcv_valid_time_w),
    .rcv_gptp_grandmaster_id_o(rcv_gptp_grandmaster_id_w),
    .rcv_gptp_domain_number_o(rcv_gptp_domain_number_w),
    .active_talker_o(active_talker_w),
    .discovery_events(discovery_events_w)
  );

  generate
    for(i = 0; i < MAX_BOUNDED_TALKER_CNT_C; i++) begin
      KL_discovery_state DISCOVERY_STATE (
        .clk_i(clk_i),
        .rst_n(rst_n),
        .rcv_available_index_i(rcv_available_index_w),
        .rcv_interface_index_i(rcv_interface_index_w),
        .rcv_valid_time_i(rcv_valid_time_w),
        .rcv_gptp_grandmaster_id_i(rcv_gptp_grandmaster_id_w),
        .rcv_gptp_domain_number_i(rcv_gptp_domain_number_w),
        .active_talker(active_talker_w[i]),
        .RCV_ADP_AVAILABLE(discovery_events_w.RCV_ADP_AVAILABLE[i]),
        .RCV_ADP_DEPARTING(discovery_events_w.RCV_ADP_DEPARTING[i]),
        .TMR_NO_ADP(discovery_events_w.TMR_NO_ADP[i]),
        .gptp_grandmaster_id_i(gptp_grandmaster_id_i),
        .gptp_domain_number_i(gptp_domain_number_i),
        .EVT_TK_DISCOVERED(adp_to_acmp_event.EVT_TK_DISCOVERED[i]),
        .EVT_TK_DEPARTED(adp_to_acmp_event.EVT_TK_DEPARTED[i])
      );
    end
  endgenerate

endmodule

`default_nettype wire
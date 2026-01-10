/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_adp_parser.sv
  Author      : Cemal Dogan

                cemal.dogan@kebag-logic.com

  Date        : 2025-04-21
  Description : Decapsulate the received ADP packets and save them into the
                struct called "rcv_entity_info".

                - Provide the rcv_entity_info.entity_info_valid strobe for the 
                following modules.
                - Provide the adp_message_type alongside with entity_info_valid.

  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//


`default_nettype none

import adp_pkg::*;

module KL_adp_parser
  (
    input wire clk_i, //! Global clock
    input wire rst_n, //! Active-low Reset
    axi_stream_if.slave s_axis, //! Slave AXI4-Stream interface
    output wire rcv_adp_discover_o, //! Strobe that indicates the ADP packet is DISCOVERY
    output wire rcv_adp_available_o, //! Strobe that indicates the ADP packet is AVAILABLE
    output wire rcv_adp_departing_o, //! Strobe that indicates the ADP packet is DEPARTING
    output entity_info_t rcv_entity_info_o //! Struct that holds the packet information.
  );

  //! Expected data count on ADP packet.
  localparam [3:0] MAX_DATA_CNT_C = 4'd8;

  typedef enum bit [2:0] {
    IDLE_S,
    PARSE_FIRST_S,
    PARSE_REST_S
  } state_t;

  state_t adp_state;
  //! Count the data
  reg [3:0] data_counter_r;
  //! Correct AXI4-Stream transaction from Slave side
  reg parse_flag_r;

  assign rcv_adp_discover_o = (data_counter_r == MAX_DATA_CNT_C && rcv_entity_info_o.adp_message_type == ENTITY_DISCOVER);
  assign rcv_adp_available_o = (data_counter_r == MAX_DATA_CNT_C && rcv_entity_info_o.adp_message_type == ENTITY_AVAILABLE);
  assign rcv_adp_departing_o = (data_counter_r == MAX_DATA_CNT_C && rcv_entity_info_o.adp_message_type == ENTITY_DEPARTING);
  assign rcv_entity_info_o.entity_info_valid = (data_counter_r == MAX_DATA_CNT_C);

  //! Recieve the s_axis.tvalid and start parsing
  //! the input ADP packet.
  always @(posedge clk_i) begin : parse_logic
    if (!rst_n) begin
      s_axis.tready <= 1'd0;
      adp_state <= IDLE_S;
    end
    else begin

      case (adp_state)
        IDLE_S : begin
          if (s_axis.tvalid) adp_state <= PARSE_FIRST_S;
        end

        PARSE_FIRST_S : begin
          rcv_entity_info_o.adp_message_type <= s_axis.tdata[35:32];
          rcv_entity_info_o.valid_time <= s_axis.tdata[31:27];
          rcv_entity_info_o.entity_id[63:48] <= s_axis.tdata[15:0];
          adp_state <= PARSE_REST_S;
        end

        PARSE_REST_S : begin
          s_axis.tready <= 1'd1;
          if (parse_flag_r) begin
            case (data_counter_r)
              // ------- 4th 64-bit Transaction --------- //
              1 : begin
                rcv_entity_info_o.entity_id[47:0] <= s_axis.tdata[63:16];
                rcv_entity_info_o.entity_model_id[63:48] <= s_axis.tdata[15:0];
              end
              // ------- 5th 64-bit Transaction --------- //
              2 : begin
                rcv_entity_info_o.entity_model_id[47:0] <= s_axis.tdata[63:16];
                rcv_entity_info_o.entity_capabilities[31:16] <= s_axis.tdata[15:0];
              end
              // ------- 6th 64-bit Transaction --------- //
              3 : begin
                rcv_entity_info_o.entity_capabilities[15:0] <= s_axis.tdata[63:48];
                rcv_entity_info_o.talker_stream_sources[15:0] <= s_axis.tdata[47:32];
                rcv_entity_info_o.talker_capabilities[15:0] <= s_axis.tdata[31:16];
                rcv_entity_info_o.listener_stream_sinks[15:0] <= s_axis.tdata[15:0];
              end
              // ------- 7th 64-bit Transaction --------- //
              4 : begin
                rcv_entity_info_o.listener_capabilities[15:0] <= s_axis.tdata[63:48];
                rcv_entity_info_o.controller_capabilities[31:0] <= s_axis.tdata[47:16];
                rcv_entity_info_o.available_index[31:16] <= s_axis.tdata[15:0];
              end
              // ------- 8th 64-bit Transaction --------- //
              5 : begin
                rcv_entity_info_o.available_index[15:0] <= s_axis.tdata[63:48];
                rcv_entity_info_o.gptp_grandmaster_id[63:16] <= s_axis.tdata[47:0];
              end
              // ------- 9th 64-bit Transaction --------- //
              6 : begin
                rcv_entity_info_o.gptp_grandmaster_id[15:0] <= s_axis.tdata[63:48];
                rcv_entity_info_o.gptp_domain_number[7:0] <= s_axis.tdata[47:40];
                rcv_entity_info_o.current_configuration_index[15:0] <= s_axis.tdata[31:16];
                rcv_entity_info_o.identify_control_index[15:0] <= s_axis.tdata[15:0];
              end
              // ------- 10th 64-bit Transaction --------- //
              7 : begin
                rcv_entity_info_o.interface_index[15:0] <= s_axis.tdata[63:48];
                rcv_entity_info_o.association_id[63:16] <= s_axis.tdata[47:0];
              end
              // ------- 11th 64-bit Transaction --------- //
              8 : begin
              // TLAST generated!
                rcv_entity_info_o.association_id[15:0] <= s_axis.tdata[63:48];
                s_axis.tready <= 1'd0;
                adp_state <= IDLE_S;
              end

              default : begin
                adp_state <= PARSE_REST_S;
              end
            endcase
          end
        end
      endcase
    end
  end
  
  //! Counting the correct AXI4-Stream Transactions and
  //! controlling the PARSE_S state by parse_flag_r register.
  always @(posedge clk_i) begin : control_logic
    if (!rst_n) begin
      data_counter_r <= 4'd0;
      parse_flag_r <= 1'd0;
    end
    else begin
      if (data_counter_r == MAX_DATA_CNT_C) begin
        data_counter_r <= 4'd0;
        parse_flag_r <= 1'd0;
      end
      else begin
        if (s_axis.tvalid & s_axis.tready) begin
          data_counter_r <= data_counter_r + 4'd1;
          parse_flag_r <= 1'd1;
        end
        else begin
          parse_flag_r <= 1'd0;
        end
      end
    end
  end

endmodule

`default_nettype wire

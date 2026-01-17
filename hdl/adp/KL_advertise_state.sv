//---------------------------------------------------------------------------//
/*
  LICENSE INFORMATION
*/
//---------------------------------------------------------------------------//

//---------------------------------------------------------------------------//
/*
Company: KebagLogics
Contributors: Cemal Dogan
Create Date: 21/04/2025 - 12:38 PM (CET+3)
Module Name: KL_advertise_state
Project Name:
Target Devices:
Tool Versions:

Description: Responsible for taking care of the Advertise State Machine in Milan
Specs v1.2 Clause 5.6.3.
Having three states, namely, DOWN, WAITING and DELAY


Dependencies:

Revision:
Revision 0.01 - File Created
Additional Comments:
*/
//---------------------------------------------------------------------------//


`default_nettype none

import adp_pkg::*;
// ----------- MODULE DECLARATION ----------- //
module KL_advertise_state
  (
    input wire clk_i,
    input wire rst_n,
    input entity_info mmap_entity_info_i, 
    input adp_advertise_event_t advertise_event_i,
    input wire [63:0] grandmaster_id_i,
    input wire [7:0] gptp_domain_number_i,

    output wire start_tmr_delay_o,
    output wire start_tmr_advertise_o,
    output wire stop_tmr_delay_o,
    output wire stop_tmr_advertise_o,
    axi_stream_if.master m_axis
  );

// ---------- CONSTANT DECLARATION ---------- //
  enum bit [1:0] {
    LINK_DOWN_S,
    DELAY_S,
    WAITING_S
  } state_advertise_s;

  enum bit [1:0] {
    INFO_VALID_S,
    COMMAND_S,
    ENCAPSULATE_S
  } state_encap_s;

// ---------- REG/WIRE DECLARATION ---------- //
  reg [1:0] state_advertise_r;
  reg start_tmr_delay_r;
  reg start_tmr_advertise_r;
  reg stop_tmr_delay_r;
  reg stop_tmr_advertise_r;

  reg [1:0] state_encap_r;
  reg [3:0] data_counter_r;

  reg send_available_r;
  reg send_departing_r;

// ------------ ASYNC ASSIGNMENT ------------ //
  assign start_tmr_delay_o = start_tmr_delay_r;
  assign start_tmr_advertise_o = start_tmr_advertise_r;
  assign stop_tmr_delay_o = stop_tmr_delay_r;
  assign stop_tmr_advertise_o =stop_tmr_advertise_r;

  // TODO: m_axis.tkeep & m_axis.tlast;
  assign m_axis.tlast = (data_counter_r == 4'd8) ? 1 : 0;
  assign m_axis.tkeep = (state_encap_r == INFO_VALID_S) ? 8'h00 : ((data_counter_r == 4'd8) ? 8'hFC : 8'hFF);

// --------------- MAIN LOGIC --------------- //
/*
  Process for handling the Advertise State Machine
*/
  always @(posedge clk_i) begin
    if (!rst_n) begin
      start_tmr_delay_r <= 1'd0;
      start_tmr_advertise_r <= 1'd0;
      stop_tmr_delay_r <= 1'd0;
      stop_tmr_advertise_r <= 1'd0;
      send_available_r <= 1'd0;
      send_departing_r <= 1'd0;
      state_advertise_r <= LINK_DOWN_S;
    end
    else begin
      case (state_advertise_r)
        // TBD - How to initiate the state machine in START-UP 
        LINK_DOWN_S : begin
          start_tmr_delay_r <= 1'd0;
          start_tmr_advertise_r <= 1'd0;
          stop_tmr_delay_r <= 1'd0;
          stop_tmr_advertise_r <= 1'd0;
          send_departing_r <= 1'd0;
          if (advertise_event_i.LINK_UP) begin
            start_tmr_delay_r <= 1'd1;
            state_advertise_r <= DELAY_S;
          end
        end

        DELAY_S : begin
          start_tmr_delay_r <= 1'd0;
          stop_tmr_advertise_r <= 1'd0;
          if (advertise_event_i.LINK_DOWN) begin 
            stop_tmr_delay_r <= 1'd1; 
            state_advertise_r <= LINK_DOWN_S;
          end

          if (advertise_event_i.SHUTDOWN) begin
            stop_tmr_delay_r <= 1'd1; // Stop tmr_delay timer
            // Send ENTITY_DEPARING
            send_departing_r <= 1'd1;
            state_advertise_r <= LINK_DOWN_S; // Go to Link_down
          end

          if (advertise_event_i.TMR_DELAY) begin
            // Send ENTITY_AVAILABLE
            send_available_r <= 1'd1;
            start_tmr_advertise_r <= 1'd1; // Start tmr_advertise timer
            state_advertise_r <= WAITING_S; // Go to Waiting
          end
        end

        WAITING_S : begin
          start_tmr_advertise_r <= 1'd0;
          send_available_r <= 1'd0;
          if (advertise_event_i.RCV_ADP_DISCOVER) begin
            stop_tmr_advertise_r <= 1'd1; // Stop tmr_advertise_timer,
            start_tmr_delay_r <= 1'd1; // Start tmr_delay timer,
            state_advertise_r <= DELAY_S; // Go to Delay
          end

          if (advertise_event_i.TMR_ADVERTISE) begin
            start_tmr_delay_r <= 1'd1; // Start tmr_delay timer,
            state_advertise_r <= DELAY_S; // Go to Delay
          end

          if (advertise_event_i.LINK_DOWN) begin
            stop_tmr_advertise_r <= 1'd1; // Stop tmr_advertise timer,
            state_advertise_r <= LINK_DOWN_S; // Go to Down
          end

          if (advertise_event_i.GM_CHANGE) begin
            start_tmr_delay_r <= 1'd1; // Start tmr_delay timer,
            state_advertise_r <= DELAY_S; // Go to Delay
          end

          if (advertise_event_i.SHUTDOWN) begin
            stop_tmr_advertise_r <= 1'd1; // Stop tmr_advertise timer,
            // Send ENTITY_DEPARING,
            send_departing_r <= 1'd1;
            state_advertise_r <= LINK_DOWN_S; // Go to Link_down
          end
        end

      endcase
    end
  end

  /*
    Process for ensapsulation of ENTITY_AVAILABLE/ENTITY_DEPARTING packets
  */

  always @(posedge clk_i) begin
    if (!rst_n) begin
      m_axis.tvalid <= 1'd0;
      m_axis.tdata <= '0;
      data_counter_r <= 4'd0;
      state_encap_r <= INFO_VALID_S;
    end
    else begin
      case (state_encap_r)

        INFO_VALID_S : begin
          m_axis.tvalid <= 1'd0;
          m_axis.tdata[63:40] <= {ETHERNET_TYPE_C, ADP_SUBTYPE_C};
          if (mmap_entity_info_i.entity_info_valid) 
            state_encap_r <= COMMAND_S;
        end

        COMMAND_S : begin
          if (send_available_r) begin
            m_axis.tdata[39:0] <= {SV_VER_MSG_TYPE_AVAILABLE_C, mmap_entity_info_i.valid_time, CTRL_DATA_LENGTH_C, mmap_entity_info_i.entity_id[63:48]};
            m_axis.tvalid <= 1'd1;
            state_encap_r <= ENCAPSULATE_S;
          end
          if (send_departing_r) begin
            m_axis.tdata[39:0] <= {SV_VER_MSG_TYPE_DEPARTING_C, mmap_entity_info_i.valid_time, CTRL_DATA_LENGTH_C, mmap_entity_info_i.entity_id[63:48]};
            m_axis.tvalid <= 1'd1;
            state_encap_r <= ENCAPSULATE_S;
          end
        end

        ENCAPSULATE_S : begin
          if (m_axis.tready) begin
            case (data_counter_r)

              0 : begin // 4th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.entity_id[47:0], mmap_entity_info_i.entity_model_id[63:48]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              1 : begin // 5th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.entity_model_id[47:0], mmap_entity_info_i.entity_capabilities[31:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              2 : begin // 6th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.entity_capabilities, mmap_entity_info_i.talker_stream_sources, mmap_entity_info_i.talker_capabilities, mmap_entity_info_i.listener_stream_sinks};
                data_counter_r <= data_counter_r + 4'd1;
              end

              3 : begin // 7th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.listener_capabilities, mmap_entity_info_i.controller_capabilities, mmap_entity_info_i.available_index[31:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              4 : begin // 8th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.available_index[15:0], grandmaster_id_i[63:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              5 : begin // 9th 64-bit transaction
                m_axis.tdata <= {grandmaster_id_i[15:0], gptp_domain_number_i, 8'd0, mmap_entity_info_i.current_configuration_index, mmap_entity_info_i.identify_control_index};
                data_counter_r <= data_counter_r + 4'd1;
              end

              6 : begin // 10th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.interface_index, mmap_entity_info_i.association_id[63:16]};
                data_counter_r <= data_counter_r + 4'd1;
              end

              7 : begin // 11th 64-bit transaction
                m_axis.tdata <= {mmap_entity_info_i.association_id[15:0], 48'd0};
                data_counter_r <= data_counter_r + 4'd1;
              end

              8 : begin
                data_counter_r <= 4'd0;
                m_axis.tvalid <= 1'd0;
                m_axis.tdata <= '0;
                state_encap_r <= INFO_VALID_S;
              end
            endcase
          end
        end
      endcase
    end
  end

endmodule

`default_nettype wire
//---------------------------------------------------------------------------//
/*
  LICENSE INFORMATION
*/
//---------------------------------------------------------------------------//

//---------------------------------------------------------------------------//
/*
Company: KebagLogics
Contributors: Cemal Dogan
Create Date: 12/05/2025 - 16:00 PM (CET+3)
Module Name: KL_discovery_state
Project Name:
Target Devices:
Tool Versions:
 
Description: Responsible for implementing DISCOVERY STATE MACHINE
w.r.t to 5.6.4 Milan Specification Consolidated v1.2
This module takes the active_talker input from KL_discovery_controller to 
start the state machine (Sink Connected event from 5.6.4.4) (Indication
of this talker is active and bounded).
RCV_ADP_DEPARTING and RCV_ADP_AVAILABLE events (discovery_events input) are 
generated from KL_discovery_controller. However, TMR_NO_ADP event is generated
internally.

Dependencies:

Revision:
Revision 0.01 - File Created
Additional Comments:
*/
//---------------------------------------------------------------------------//

`default_nettype none

import adp_pkg::*; 

// ----------- MODULE DECLARATION ----------- //
module KL_discovery_state
  (
    input wire clk_i,
    input wire rst_n,

    // From KL_discovery_controller
    input wire [31:0] rcv_available_index_i,
    input wire [15:0] rcv_interface_index_i,
    input wire [4:0] rcv_valid_time_i,
    input wire [63:0] rcv_gptp_grandmaster_id_i,
    input wire [7:0] rcv_gptp_domain_number_i,
    input wire active_talker, // Track the status of the talker that is bounded
    input wire RCV_ADP_AVAILABLE,
    input wire RCV_ADP_DEPARTING,
    input wire TMR_NO_ADP,

    // From PTP module
    input wire [63:0] gptp_grandmaster_id_i,
    input wire [7:0] gptp_domain_number_i,

    output wire EVT_TK_DISCOVERED, 
    output wire EVT_TK_DEPARTED
    
  );

// ---------- CONSTANT DECLARATION ---------- //
  typedef enum logic [2:0] {
    SINK_NOT_CONNECTED_S,
    TK_NOT_DISCOVERED_S,
    TK_NOT_DISCOVERED_2_S, // To prevent so many non-blocking elements on tk_not_discovered state
    TK_DISCOVERED_S,
    // Prevent nested if-else statements
    TK_DISCOVERED_AVA_S, // TK_Discovered and RCV_ADP_AVAILABLE received
    TK_DISCOVERED_AVA_2_S,
    TK_DISCOVERED_DEP_S // TK_Discovered and RCV_ADP_DEPARTING received
  } state_discovery_s;

// ---------- REG/WIRE DECLARATION ---------- //

  state_discovery_s state_discovery_r;
  // Since when RCV_ADP_AVAILABLE|DEPARTING event occurs,
  // the corresponding received inputs are given in one clock cycle.
  // Discovery state machine must save those inputs to be used for 
  // comparing.
  // Save the values in TK_NOT_DISCOVERED_S state
  reg [31:0] tk_not_available_index_r;
  reg [15:0] tk_not_interface_index_r;
  reg [4:0]  tk_not_valid_time_r;
  reg [63:0] tk_not_gptp_grandmaster_id_r;
  reg [7:0]  tk_not_gptp_domain_id_r;
  // Save the values in TK_DISCOVERED_S state
  reg [31:0] tk_available_index_r;
  reg [15:0] tk_interface_index_r;
  reg [4:0]  tk_valid_time_r;
  reg [63:0] tk_gptp_grandmaster_id_r;
  reg [7:0]  tk_gptp_domain_id_r;

  reg [63:0] gptp_grandmaster_id_r;
  reg [7:0] gptp_domain_number_r;

  reg start_tmr_no_adp_r;
  reg stop_tmr_no_adp_r;
  wire tmr_completed_w;

  reg evt_tk_discovered_r;
  reg evt_tk_departed_r;

// ------------ ASYNC ASSIGNMENT ------------ //

  assign EVT_TK_DISCOVERED = evt_tk_discovered_r;
  assign EVT_TK_DEPARTED = evt_tk_departed_r;

/* 
  Counter for TMR_NO_ADP
  valid_time field of the ENTITY_AVAILABLE packet must be 10.
  Therefore, it indicates that ENTITY_AVAILABLE packets will 
  arrive within 5 seconds
*/
  KL_counter TMR_NO_ADP_COUNTER_0 (
    .clk_i         ( clk_i ),
    .rst_n         ( rst_n ),
    .start_i       ( start_tmr_no_adp_r ),
    .stop_i        ( stop_tmr_no_adp_r ),
    .delay_value_i ( 3'd5 ),
    .completed_o   ( tmr_completed_w )
  );


// --------------- MAIN LOGIC --------------- //

  /*
    Logic for Discovery State machine;
      - Check whether the talker is active. If it is active
        go to TK_NOT_DISCOVERED state and wait for RCV_ADP_AVAILABLE,
        then do the following task 5.6.4.5.1

      - In TK_DISCOVERED state, do the following;
      5.6.4.5.2 - 5.6.4.5.3 - 5.6.4.5.4
  */
  always@(posedge clk_i) begin
    if (!rst_n) begin
      tk_not_available_index_r <= 32'd0;
      tk_not_interface_index_r <= 16'd0;
      tk_not_valid_time_r <= 5'd0;
      tk_not_gptp_grandmaster_id_r <= 64'd0;
      tk_not_gptp_domain_id_r <= 8'd0;
      tk_available_index_r <= 32'd0;
      tk_interface_index_r <= 16'd0;
      tk_valid_time_r <= 5'd0;
      tk_gptp_grandmaster_id_r <= 64'd0;
      tk_gptp_domain_id_r <= 8'd0;
      start_tmr_no_adp_r <= 1'd0;
      stop_tmr_no_adp_r <= 1'd0;
      evt_tk_discovered_r <= 1'd0;
      evt_tk_departed_r <= 1'd0;
      state_discovery_r <= SINK_NOT_CONNECTED_S;
    end
    else begin
      if (active_talker) begin // Always check whether the talker is bounded
        case (state_discovery_r)

          SINK_NOT_CONNECTED_S : begin
            state_discovery_r <= TK_NOT_DISCOVERED_S;
          end

          TK_NOT_DISCOVERED_S : begin
            evt_tk_departed_r <= 1'd0;
            stop_tmr_no_adp_r <= 1'd0;
            if (RCV_ADP_AVAILABLE) begin
              tk_not_available_index_r <= rcv_available_index_i;
              tk_not_interface_index_r <= rcv_interface_index_i;
              tk_not_valid_time_r <= rcv_valid_time_i;
              tk_not_gptp_grandmaster_id_r <= rcv_gptp_grandmaster_id_i;
              tk_not_gptp_domain_id_r <= rcv_gptp_domain_number_i;
              state_discovery_r <= TK_NOT_DISCOVERED_2_S;
            end
          end

          TK_NOT_DISCOVERED_2_S : begin
            // 5.6.4.5.1 - First item
            if ((tk_not_gptp_grandmaster_id_r == gptp_grandmaster_id_r) && (tk_not_gptp_domain_id_r && gptp_domain_number_r)) begin
              // 5.6.4.5.1 - Second item is already done in the TK_NOT_DISCOVERED_S
              start_tmr_no_adp_r <= 1'd1; // Third item
              evt_tk_discovered_r <= 1'd1; // Fourth item
              state_discovery_r <= TK_DISCOVERED_S; // Fourth item
            end
            else state_discovery_r <= SINK_NOT_CONNECTED_S;
          end

          TK_DISCOVERED_S : begin
            start_tmr_no_adp_r <= 1'd0; 
            evt_tk_discovered_r <= 1'd0;
            evt_tk_departed_r <= 1'd0;
            // Save the received fields to compare with tk_not* regs
            tk_available_index_r <= rcv_available_index_i;
            tk_interface_index_r <= rcv_interface_index_i;
            tk_valid_time_r <= rcv_valid_time_i;
            tk_gptp_grandmaster_id_r <= rcv_gptp_grandmaster_id_i;
            tk_gptp_domain_id_r <= rcv_gptp_domain_number_i;
            // Clause 5.6.4.5.2
            if (RCV_ADP_AVAILABLE) begin
              if (tk_not_interface_index_r == rcv_interface_index_i) // 5.6.4.5.2-1
                state_discovery_r <= TK_DISCOVERED_AVA_S;
              else state_discovery_r <= TK_DISCOVERED_S; // ignore the message and exit!
            end
            if (RCV_ADP_DEPARTING) begin
              if (tk_not_interface_index_r == rcv_interface_index_i) // 5.6.4.5.3-1
                state_discovery_r <= TK_DISCOVERED_DEP_S;
              else state_discovery_r <= TK_DISCOVERED_S; // ignore the message and exit!
            end
            if (tmr_completed_w) begin // 5.6.4.5.4
              evt_tk_departed_r <= 1'd1;
              state_discovery_r <= TK_NOT_DISCOVERED_S;
            end
          end

          TK_DISCOVERED_AVA_S : begin
            // available must be incremented each time when ENTITY_AVAILABLE transferred 
            // Directly go to 5.6.4.5.2-3 if rcv available index is bigger than previous one
            if (tk_available_index_r <= tk_not_available_index_r) begin // 5.6.4.5.2-2
              evt_tk_departed_r <= 1'd1; // 5.6.4.5.2-2a
              // 5.6.4.5.2-2b positive
              if ((tk_gptp_grandmaster_id_r == gptp_grandmaster_id_r) && (tk_gptp_domain_id_r == gptp_domain_number_r)) begin
                evt_tk_discovered_r <= 1'd1; // 5.6.4.5.2-2c
                stop_tmr_no_adp_r <= 1'd1; // For reseting the timer, first stopping.
                state_discovery_r <= TK_DISCOVERED_AVA_2_S;
              end
              else begin // 5.6.4.5.2-2b negative
                stop_tmr_no_adp_r <= 1'd1;
                state_discovery_r <= TK_NOT_DISCOVERED_S;
              end
            end
            else begin
              stop_tmr_no_adp_r <= 1'd1; // Stop the counter to reset
              state_discovery_r <= TK_DISCOVERED_AVA_2_S;
            end
          end

          TK_DISCOVERED_AVA_2_S : begin // For 5.6.4.5.2-3
            evt_tk_discovered_r <= 1'd0;
            evt_tk_departed_r <= 1'd0;
            stop_tmr_no_adp_r <= 1'd0;
            start_tmr_no_adp_r <= 1'd1; // Reset the timer
            tk_not_available_index_r <= tk_available_index_r; // 5.6.4.5.2-3
            state_discovery_r <= TK_DISCOVERED_S;
          end

          TK_DISCOVERED_DEP_S : begin // 5.6.4.5.3 
            stop_tmr_no_adp_r <= 1'd1; // 5.6.4.5.3-2          
            evt_tk_departed_r <= 1'd1; // 5.6.4.5.3-3
            state_discovery_r <= TK_NOT_DISCOVERED_S;
          end
        endcase
      end
      else begin
        state_discovery_r <= SINK_NOT_CONNECTED_S; // Always go to SINK_NOT_CONNECTED_S state 
        // if the active_talker input is low
      end
    end
  end

  /*
    If the talker is bounded (active), register the gptp_grandmaster_id 
    and gptp_domain_number. These registers later will be used in discovery
    state machine w.r.t the received gptp_grandmaster/domain
  */
  always @(posedge clk_i) begin
    if (!rst_n) begin
      gptp_grandmaster_id_r <= 64'd0;
      gptp_domain_number_r <= 8'd0;
    end
    else begin
      if (active_talker) begin
        gptp_grandmaster_id_r <= gptp_grandmaster_id_i; 
        gptp_domain_number_r <= gptp_domain_number_i;
      end
    end
  end


endmodule

`default_nettype wire
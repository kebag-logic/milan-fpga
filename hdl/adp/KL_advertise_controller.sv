/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
*/

/*
------------------------------------------------------------------------------
  File        : KL_advertise_controller.sv
  Author      : Cemal Dogan

                cemal.dogan@kebag-logic.com

  Date        : 2025-04-21
  Description : Providing all the necessary events for KL_advertise_state
                  - Check the rcvd_entity_info for the following fields;
                    - Entity_id matched (zero or ATDECC entity_id)
                    - Grandmaster_id
                  - Start/Stop and generate the events for TMR_DELAY and TMR_ADVERTISE
  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/

`default_nettype none
import adp_pkg::*;

module KL_advertise_controller
  (
    input wire clk_i, //! Global clock
    input wire rst_n, //! Active-low Reset 
    input wire [63:0] rcv_entity_id_i,  //! entity_info.rcv_entity_id - from KL_adp_parser
    input wire [63:0] entity_id_i,      //! entity_id of the ATDECC entity - from memory map 
    input wire [63:0] grandmaster_id_i, //! grandmaster_id - from PTP module

    input wire rcv_adp_discover_i, //! ADP Discovery packet is received and rcv_entity_id_i field is valid- from KL_adp_parser

    input link_status_t link_status_i, //! Link Status related inputs from Upper Management Module

    input tmr_events_t tmr_events_i,    //! ADP Timer events inputs

    output adp_advertise_event_t advertise_event_o //! All Advertise related evenet - to KL_advertise_state
  );

  //! GM_EVENT related registers
  reg [63:0] grandmaster_id_r;
  //! TMR_DELAY and TMR_ADVERTISE related registers.
  reg [$clog2(MAX_SECOND)-1:0] zero_four_sec_cnt_r;
  //! Register that takes the value from 0 to 4.
  reg [$clog2(MAX_SECOND)-1:0] delay_value_r;
  //! Start signal for KL_counter.
  reg start_tmr_delay_cnt_r;
  //! TMR_ADVERTISE_COUNTER finished counting.
  reg tmr_advertise_completed_r;
  //! TMR_DELAY_COUNTER finished counting.
  reg tmr_delay_completed_r;


// ------------ ASYNC ASSIGNMENT ------ ------ //
  assign advertise_event_o.LINK_DOWN = link_status_i.link_down;
  assign advertise_event_o.LINK_UP = link_status_i.link_up;
  assign advertise_event_o.SHUTDOWN = link_status_i.shutdown;
  assign advertise_event_o.GM_CHANGE = (grandmaster_id_i != grandmaster_id_r);
  assign advertise_event_o.RCV_ADP_DISCOVER = rcv_adp_discover_i && (rcv_entity_id_i == 64'd0 || rcv_entity_id_i == entity_id_i);
  assign advertise_event_o.TMR_ADVERTISE = tmr_advertise_completed_r;
  assign advertise_event_o.TMR_DELAY = tmr_delay_completed_r;

  //! Advertise counter - Static 5 sec delay
  KL_counter TMR_ADVERTISE_COUNTER (
    .clk_i         ( clk_i ),
    .rst_n         ( rst_n ),
    .start_i       ( tmr_events_i.start_tmr_advertise ),
    .stop_i        ( tmr_events_i.stop_tmr_advertise ),
    .delay_value_i ( 3'd5 ),
    .completed_o   ( tmr_advertise_completed_r )
  );

  //! Delay counter - random value between 0-4 delay
  KL_counter TMR_DELAY_COUNTER (
    .clk_i         ( clk_i ),
    .rst_n         ( rst_n ),
    .start_i       ( start_tmr_delay_cnt_r ),
    .stop_i        ( tmr_events_i.stop_tmr_delay ),
    .delay_value_i ( delay_value_r ),
    .completed_o   ( tmr_delay_completed_r )
  );
// --------------- MAIN LOGIC --------------- //

  //! Free-running counter logic - value in between 0-4
  always_ff @(posedge clk_i) begin : counter_logic
    if (!rst_n) 
      zero_four_sec_cnt_r <= 'd0;
    else begin
      if (zero_four_sec_cnt_r == 'd4)
        zero_four_sec_cnt_r <= 'd0;
      else
        zero_four_sec_cnt_r <= zero_four_sec_cnt_r + 'd1;
    end
  end

  //! Process for assigning the delay value for TMR_DELAY_COUNTER
  always_ff @(posedge clk_i) begin : tmr_delay_process
    if (!rst_n) begin
      delay_value_r <= 'd0;
      start_tmr_delay_cnt_r <= 1'd0;
    end
    else begin
      if (tmr_events_i.start_tmr_delay) begin
        delay_value_r <= zero_four_sec_cnt_r;
        start_tmr_delay_cnt_r <= 1'd1;
      end 
      else begin
        start_tmr_delay_cnt_r <= 1'd0;
      end
    end
  end

  //! Process for checking whether grandmaster_id has changed
  //! for the ATDECC Entity.
  always_ff @(posedge clk_i) begin : grandmaster_control
    if (!rst_n) grandmaster_id_r <= 64'd0;
    else grandmaster_id_r <= grandmaster_id_i;
  end

endmodule

`default_nettype wire
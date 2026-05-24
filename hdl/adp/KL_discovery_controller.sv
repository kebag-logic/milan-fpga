/*
 * SPDX-FileCopyrightText: 2025 Cemal Dogan <cemal.dogan@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_discovery_controller.sv
  Author      : Cemal Dogan

                cemal.dogan@kebag-logic.com

  Date        : 2025-05-12
  Description : Controller for KL_discovery_state
                Tasks;
                  1- Save the talker_entity_ids from ACMP - When bound happened talker_entity_id_valid_i
                  will be high
                  2- Get the rcv_adp_available, rcv_adp_departing, rcv_entity_id, rcv_available_index
                  rcv_interface_index and rcv_valid_time from KL_adp_parser. 
                  3- Loop all the possible talker_entity_ids and compare individually with rcv_entity_id
                  whenever rcv_adp_available OR rcv_adp_departing arrived.
                  4- If ids are matched -> Provide RCV_ADP_AVAILABE OR RCV_ADP_DEPARTING events to 
                  KL_discovery_state
                  5- Align events available_index_o, interface_index_o and valid_time_o

  Notes;
    1- Inputs from KL_adp_parser were generated after all packet is parsed.

  Company     : Kebag Logic
  Project     : Milan ADP

------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

//! Controller for KL_discovery_state
//! Tasks;
//!   1- Save the talker_entity_ids from ACMP - When bound happened talker_entity_id_valid_i
//!   will be high
//!   2- Get the rcv_adp_available, rcv_adp_departing, rcv_entity_id, rcv_available_index
//!   rcv_interface_index and rcv_valid_time from KL_adp_parser. 
//!   3- Loop all the possible talker_entity_ids and compare individually with rcv_entity_id
//!   whenever rcv_adp_available OR rcv_adp_departing arrived.
//!   4- If ids are matched -> Provide RCV_ADP_AVAILABE OR RCV_ADP_DEPARTING events to 
//!   KL_discovery_state
//!   5- Align events available_index_o, interface_index_o and valid_time_o

`default_nettype none

import adp_pkg::*; 

module KL_discovery_controller
  (
    input wire clk_i, //! Global clock
    input wire rst_n, //! Active-low Reset

    input wire [63:0] talker_entity_id_i, //! From ACMP Top - Talker entity Id
    input wire talker_entity_id_valid_i, //! From ACMP Top - Talker entity Id is valid
    input wire talker_departed_i, //! From ACMP Top - Talker is departed

    input wire rcv_adp_available_i, //! Received packet is Available
    input wire rcv_adp_departing_i, //! Received packet is Departing

    input entity_info_t rcv_entity_info_i, //! Received ATDECC Entity Info
    output entity_info_t rcv_entity_info_o, //! Entity Info to Discovery state module

    output wire [MAX_BOUNDED_TALKER_CNT_C -1 : 0] active_talker_o, //! Active talkers
    output adp_discovery_event_t discovery_events_o //! Discovery events to Discovery state module
  );

  //! Controller state, drive Database and index states
  typedef enum bit [1:0] {
    CTRL_IDLE_S,
    CTRL_SEARCH_S,
    CTRL_MATCHED_S
  } state_control_t;
  //! Database operations state
  typedef enum bit [2:0] {
    DB_IDLE_S,
    DB_SAVE_S,
    DB_DELETE_S,
    DB_DEL_DONE_S,
    DB_SAVE_DONE_S
  } state_database_t;
  //! Search index state
  typedef enum bit [1:0] {
    INDEX_IDLE_S,
    INDEX_SEARCH_S,
    INDEX_WAIT_S
  } state_index_t;

  //! ADP available received
  reg rcv_adp_available_r;
  //! ADP departing received
  reg rcv_adp_departing_r;
  //! Save the received entity info
  entity_info_t rcv_entity_info_r;
  //! Matched index register
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] matched_index_r;
  //! control state
  state_control_t control_state;

  //! Holds the entity_id's of bounded talkers and status field
  reg [63:0] talker_entity_id_r;
  //! Bounded talkers
  reg [MAX_BOUNDED_TALKER_CNT_C-1 : 0][63:0] bounded_talker_db_r;
  //! Current active talkers
  reg [MAX_BOUNDED_TALKER_CNT_C-1 : 0] active_talker_r;
  //! Keep track of the total number_of_talkers that are active
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] number_of_talker_r;
  int i,j;
  //! Database state
  state_database_t database_state;

  //! Index of holding the next available slot to save within bounded_talker_db_r
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] save_index_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] save_index_counter_r;
  //! Saving index found
  reg save_index_ready_r;
  //! Save index
  state_index_t save_state;

  //! Index of holding the bounded talker to be de-activate
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] delete_index_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] delete_index_counter_r;
  //! Delete index found
  reg delete_index_ready_r;
  state_index_t delete_state;

// ------------ ASYNC ASSIGNMENT ------------ //
  assign rcv_entity_info_o.available_index = (control_state == CTRL_MATCHED_S) ? rcv_entity_info_r.available_index : 0;
  assign rcv_entity_info_o.interface_index = (control_state == CTRL_MATCHED_S) ? rcv_entity_info_r.interface_index : 0;
  assign rcv_entity_info_o.gptp_grandmaster_id = (control_state == CTRL_MATCHED_S) ? rcv_entity_info_r.gptp_grandmaster_id : 0;
  assign rcv_entity_info_o.gptp_domain_number = (control_state == CTRL_MATCHED_S) ? rcv_entity_info_r.gptp_domain_number : 0;
  assign rcv_entity_info_o.valid_time = (control_state == CTRL_MATCHED_S) ? rcv_entity_info_r.valid_time : 0;
  assign rcv_entity_info_o.entity_info_valid = control_state == CTRL_MATCHED_S;

  assign active_talker_o = active_talker_r;

// --------------- MAIN LOGIC --------------- //
  /*
    Process responsible for checking whether rcv_entity_id matches with
    any entity_id in database.
    - Activate the state machine when rcv_adp_available_i or rcv_adp_departing_i
    - Search through the database and check if rcv_entity_id_r == bounded_talker_db_r
    - If matched, provide discovery_events_o.RCV_ADP_AVAILABLE || discovery_events_o.RCV_ADP_DEPARTING
    alongside with matched_index_r
  */
  always @(posedge clk_i) begin : control_fsm
    if (!rst_n) begin
      rcv_entity_info_r <= '0;
      matched_index_r <= '0;
      control_state <= CTRL_IDLE_S;
      discovery_events_o.RCV_ADP_AVAILABLE <= '0;
      discovery_events_o.RCV_ADP_DEPARTING <= '0;
      discovery_events_o.TMR_NO_ADP <= '0;
    end
    else begin
      case (control_state)

        CTRL_IDLE_S : begin
          matched_index_r <= '0;
          // Save inputs in case KL_adp_parser receives another packet
          if (rcv_adp_available_i) begin
            rcv_entity_info_r <= rcv_entity_info_i;
            rcv_adp_available_r <= 1'd1;
            control_state <= CTRL_SEARCH_S;
          end
          if (rcv_adp_departing_i) begin
            rcv_entity_info_r <= rcv_entity_info_i;
            rcv_adp_departing_r <= 1'd1;
            control_state <= CTRL_SEARCH_S;
          end
        end

        CTRL_SEARCH_S : begin
          if (matched_index_r == MAX_BOUNDED_TALKER_CNT_C - 1) begin // No Matched! 
            rcv_adp_available_r <= 1'd0;
            rcv_adp_departing_r <= 1'd0;
            control_state <= CTRL_IDLE_S;
          end
          else begin
            if ((bounded_talker_db_r[matched_index_r] == rcv_entity_info_r.entity_id) && active_talker_r[matched_index_r]) begin
              if (rcv_adp_available_r)
                discovery_events_o.RCV_ADP_AVAILABLE[matched_index_r] <= 1'd1;
              if (rcv_adp_departing_r)
                discovery_events_o.RCV_ADP_DEPARTING[matched_index_r] <= 1'd1;
              control_state <= CTRL_MATCHED_S;
            end
            else begin
              matched_index_r <= matched_index_r + 1;
            end
          end
        end

        CTRL_MATCHED_S : begin
          rcv_adp_available_r <= 1'd0;
          rcv_adp_departing_r <= 1'd0;
          discovery_events_o.RCV_ADP_AVAILABLE[matched_index_r] <= 1'd0;
          discovery_events_o.RCV_ADP_DEPARTING[matched_index_r] <= 1'd0;
          control_state <= CTRL_IDLE_S;
        end

        default : control_state <= CTRL_IDLE_S;
      endcase
    end
  end
  
  /*
    Database for holding the active bounded talker_entity_ids
    Two tasks; SAVE & DELETE

    TODO: Speed up the search algorithm.
    When we provide talker_entity_id_valid with 50ns intervals, logic fails.
    However, in real case scenario we do not expect a talker to bound within 50ns.
    Since the ACMP message transmission is not that short.! 
  */
  always @(posedge clk_i) begin : database_fsm
    if (!rst_n) begin
      talker_entity_id_r <= '0;
      number_of_talker_r <= '0;
      active_talker_r <= '0;
      for (i = 0 ; i < MAX_BOUNDED_TALKER_CNT_C; i++) begin
        bounded_talker_db_r <= '0;
      end
      database_state <= DB_IDLE_S;
    end
    else begin
      case (database_state)
        DB_IDLE_S : begin
          if (talker_entity_id_valid_i) begin
            talker_entity_id_r <= talker_entity_id_i;
            number_of_talker_r <= number_of_talker_r + 1;
            database_state <= DB_SAVE_S;
          end
          if (talker_departed_i) begin // after EVT_TK_DEPARTED provided to ACMP
          // from discovery_state module, this input is expected with correct entity_id
            talker_entity_id_r <= talker_entity_id_i;
            number_of_talker_r <= number_of_talker_r - 1;
            database_state <= DB_DELETE_S;
          end
        end

        DB_SAVE_S : begin
          if (save_index_ready_r) begin
            bounded_talker_db_r[save_index_r] <= talker_entity_id_r;
            active_talker_r[save_index_r] <= 1'd1;
            database_state <= DB_SAVE_DONE_S;
          end
        end

        DB_DELETE_S : begin
          if (delete_index_ready_r) begin
            active_talker_r[delete_index_r] <= 1'd0;
            database_state <= DB_DEL_DONE_S;
          end
        end

        DB_DEL_DONE_S : database_state <= DB_IDLE_S;
        DB_SAVE_DONE_S : database_state <= DB_IDLE_S;
        default : database_state <= DB_IDLE_S;
      endcase
    end
  end
  
  /*
    Process for handling save_index_r and save_index_ready regs.
    Loop through the bounded_talker_id to check what's the next
    available index.
    Provide the index and ready registers to database
  */
  always @(posedge clk_i) begin : index_fsm
    if (!rst_n) begin
      save_index_r <= '0;
      save_index_counter_r <= '0;
      save_index_ready_r <= 1'd0;
      save_state <= INDEX_IDLE_S;
    end
    else begin
      case (save_state)
        INDEX_IDLE_S : begin
          save_index_r <= '0;
          save_state <= INDEX_SEARCH_S;
        end

        INDEX_SEARCH_S : begin
          if (!(active_talker_r[save_index_counter_r])) begin// Empty place
            save_index_r <= save_index_counter_r;
            save_index_ready_r <= 1'd1;
            save_state <= INDEX_WAIT_S;
          end
          else begin // Place is occupied
            save_index_counter_r <= save_index_counter_r + 1;
          end
        end

        INDEX_WAIT_S : begin
          if (database_state == DB_SAVE_DONE_S) begin // talker_id saved
            save_index_ready_r <= 1'd0;
            save_state <= INDEX_IDLE_S;
          end
          // TODO: Check if any talker is departing, we can place our counter there
        end
      endcase
    end
  end

  /*
    Process for handling DELETE operations for database
      Receive the talker_entity_id who transferred departing message
      Loop through the database and find the index 
      Provide the index and ready registers to database
  */
  always @(posedge clk_i) begin : delete_fsm
    if (!rst_n) begin
      delete_index_r <= '0;
      delete_index_counter_r <= '0;
      delete_index_ready_r <= '0;
      delete_state <= INDEX_IDLE_S;
    end
    else begin
      case (delete_state)
        INDEX_IDLE_S : begin
          if (talker_departed_i) begin
            delete_state <= INDEX_SEARCH_S;
          end
        end

        INDEX_SEARCH_S : begin
          if (bounded_talker_db_r[delete_index_counter_r] == talker_entity_id_r) begin
            // talker_ids matched
            delete_index_r <= delete_index_counter_r;
            delete_index_ready_r <= 1'd1;
            delete_state <= INDEX_WAIT_S;
          end
          else begin // no match, keep searching
            delete_index_counter_r <= delete_index_counter_r + 1;
          end
        end

        INDEX_WAIT_S : begin
          if (database_state == DB_DEL_DONE_S) begin // talker_id deleted
            delete_index_counter_r <= '0;
            delete_index_ready_r <= 1'd0;
            delete_state <= INDEX_IDLE_S;
          end
        end
      endcase
    end
  end
endmodule

`default_nettype wire
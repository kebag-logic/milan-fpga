//---------------------------------------------------------------------------//
/*
  LICENSE INFORMATION
*/
//---------------------------------------------------------------------------//

//---------------------------------------------------------------------------//
/*
Company: KebagLogics
Contributors: Cemal Dogan
Create Date: 12/05/2025 - 15:38 PM (CET+3)
Module Name: KL_discovery_controller
Project Name:
Target Devices:
Tool Versions:

Description: Controller for KL_discovery_state

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


Dependencies:

Revision:
Revision 0.01 - File Created
Additional Comments:
*/
//---------------------------------------------------------------------------//


`default_nettype none

import adp_pkg::*; 
// TODO: For now module based, later will be only in KL_ADP_TOP
// TODO: Buffering logic for rcv_adp_available and rcv_adp_departing will be added.

// ----------- MODULE DECLARATION ----------- //
module KL_discovery_controller
  (
    input wire clk_i,
    input wire rst_n,

    // From ACMP Top
    input wire [63:0] talker_entity_id_i,
    input wire talker_entity_id_valid_i,
    input wire talker_departed_i,

    // From KL_adp_parser
    input wire rcv_adp_available_i,
    input wire rcv_adp_departing_i,
    input wire [63:0] rcv_entity_id_i,
    input wire [31:0] rcv_available_index_i,
    input wire [15:0] rcv_interface_index_i,
    input wire [63:0] rcv_gptp_grandmaster_id_i,
    input wire [7:0] rcv_gptp_domain_number_i,
    input wire [4:0] rcv_valid_time_i,

    // To KL_discovery_state
    output wire [31:0] rcv_available_index_o,
    output wire [15:0] rcv_interface_index_o,
    output wire [4:0] rcv_valid_time_o,
    output wire [63:0] rcv_gptp_grandmaster_id_o,
    output wire [7:0] rcv_gptp_domain_number_o,
    output wire [MAX_BOUNDED_TALKER_CNT_C -1 : 0] active_talker_o,
    output adp_discovery_event_t discovery_events
  );

// ---------- CONSTANT DECLARATION ---------- //

  typedef enum logic [1:0] {
    CTRL_IDLE_S,
    CTRL_SEARCH_S,
    CTRL_MATCHED_S
  } state_control_s;

  typedef enum logic [2:0] {
    DB_IDLE_S,
    DB_SAVE_S,
    DB_DELETE_S,
    DB_DEL_DONE_S,
    DB_SAVE_DONE_S
  } state_database_s;

  typedef enum logic [1:0] {
    INDEX_IDLE_S,
    INDEX_SEARCH_S,
    INDEX_WAIT_S
  } state_index_s;

// ---------- REG/WIRE DECLARATION ---------- //

  reg rcv_adp_available_r;
  reg rcv_adp_departing_r;
  reg [63:0] rcv_entity_id_r;
  reg [31:0] rcv_available_index_r;
  reg [15:0] rcv_interface_index_r;
  reg [63:0] rcv_gptp_grandmaster_id_r;
  reg [7:0] rcv_gptp_domain_number_r;
  reg [4:0] rcv_valid_time_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] matched_index_r;
  state_control_s control_state_r;

  // Holds the entity_id's of bounded talkers and status field
  // [63:0] talker_entity_id
  reg [63:0] talker_entity_id_r;
  reg [MAX_BOUNDED_TALKER_CNT_C-1 : 0][63:0] bounded_talker_db_r;
  reg [MAX_BOUNDED_TALKER_CNT_C-1 : 0] active_talker_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] number_of_talker_r; // Keep track of the total number_of_talkers that are active
  int i,j;
  state_database_s database_state_r;

  // Index of holding the next available slot to save within bounded_talker_db_r
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] save_index_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] save_index_counter_r;
  reg save_index_ready_r;
  state_index_s save_state_r;

  // Index of holding the bounded talker to be de-activate
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] delete_index_r;
  reg [$clog2(MAX_BOUNDED_TALKER_CNT_C)-1 : 0] delete_index_counter_r;
  reg delete_index_ready_r;
  state_index_s delete_state_r;

// ------------ ASYNC ASSIGNMENT ------------ //
  assign rcv_available_index_o = (control_state_r == CTRL_MATCHED_S) ? rcv_available_index_r : 0;
  assign rcv_interface_index_o = (control_state_r == CTRL_MATCHED_S) ? rcv_interface_index_r : 0;
  assign rcv_gptp_grandmaster_id_o = (control_state_r == CTRL_MATCHED_S) ? rcv_gptp_grandmaster_id_r : 0;
  assign rcv_gptp_domain_number_o = (control_state_r == CTRL_MATCHED_S) ? rcv_gptp_domain_number_r : 0;
  assign rcv_valid_time_o = (control_state_r == CTRL_MATCHED_S) ? rcv_valid_time_r : 0;
  assign active_talker_o = active_talker_r; 
// --------------- MAIN LOGIC --------------- //
  /*
    Process responsible for checking whether rcv_entity_id matches with
    any entity_id in database.
    - Activate the state machine when rcv_adp_available_i or rcv_adp_departing_i
    - Search through the database and check if rcv_entity_id_r == bounded_talker_db_r
    - If matched, provide discovery_events.RCV_ADP_AVAILABLE || discovery_events.RCV_ADP_DEPARTING
    alongside with matched_index_r
  */
  always @(posedge clk_i) begin
    if (!rst_n) begin
      rcv_entity_id_r <= 64'd0;
      rcv_adp_available_r <= 1'd0;
      rcv_adp_departing_r <= 1'd0;
      rcv_available_index_r <= 32'd0;
      rcv_interface_index_r <= 16'd0;
      rcv_gptp_grandmaster_id_r <= 64'd0;
      rcv_gptp_domain_number_r <= 8'd0;
      rcv_valid_time_r <= 5'd0;
      matched_index_r <= '0;
      control_state_r <= CTRL_IDLE_S;
      for (j = 0 ; j < MAX_BOUNDED_TALKER_CNT_C; j++) begin
        discovery_events.RCV_ADP_AVAILABLE[j] <= 1'd0;
        discovery_events.RCV_ADP_DEPARTING[j] <= 1'd0;
        discovery_events.TMR_NO_ADP[j] <= 1'd0;
      end
    end
    else begin
      case (control_state_r)

        CTRL_IDLE_S : begin
          matched_index_r <= '0;
          // Save inputs in case KL_adp_parser receives another packet
          rcv_entity_id_r <= rcv_entity_id_i;
          rcv_available_index_r <= rcv_available_index_i;
          rcv_interface_index_r <= rcv_interface_index_i;
          rcv_valid_time_r <= rcv_valid_time_i;
          rcv_gptp_grandmaster_id_r <= rcv_gptp_grandmaster_id_i;
          rcv_gptp_domain_number_r <= rcv_gptp_domain_number_i;
          if (rcv_adp_available_i) begin
            rcv_adp_available_r <= 1'd1;
            control_state_r <= CTRL_SEARCH_S;
          end
          if (rcv_adp_departing_i) begin
            rcv_adp_departing_r <= 1'd1;
            control_state_r <= CTRL_SEARCH_S;
          end
        end

        CTRL_SEARCH_S : begin
          if (matched_index_r == MAX_BOUNDED_TALKER_CNT_C - 1) begin // No Matched! 
            rcv_adp_available_r <= 1'd0;
            rcv_adp_departing_r <= 1'd0;
            control_state_r <= CTRL_IDLE_S;
          end
          else begin
            if ((bounded_talker_db_r[matched_index_r] == rcv_entity_id_r) && active_talker_r[matched_index_r]) begin
              if (rcv_adp_available_r)
                discovery_events.RCV_ADP_AVAILABLE[matched_index_r] <= 1'd1;
              if (rcv_adp_departing_r)
                discovery_events.RCV_ADP_DEPARTING[matched_index_r] <= 1'd1;
              control_state_r <= CTRL_MATCHED_S;
            end
            else begin
              matched_index_r <= matched_index_r + 1;
            end
          end
        end

        CTRL_MATCHED_S : begin
          rcv_adp_available_r <= 1'd0;
          rcv_adp_departing_r <= 1'd0;
          discovery_events.RCV_ADP_AVAILABLE[matched_index_r] <= 1'd0;
          discovery_events.RCV_ADP_DEPARTING[matched_index_r] <= 1'd0;
          control_state_r <= CTRL_IDLE_S;
        end
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
  always @(posedge clk_i) begin
    if (!rst_n) begin
      talker_entity_id_r <= '0;
      number_of_talker_r <= '0;
      active_talker_r <= '0;
      for (i = 0 ; i < MAX_BOUNDED_TALKER_CNT_C; i++) begin
        bounded_talker_db_r <= '0;
      end
      database_state_r <= DB_IDLE_S;
    end
    else begin
      case (database_state_r)
        DB_IDLE_S : begin
          if (talker_entity_id_valid_i) begin
            talker_entity_id_r <= talker_entity_id_i;
            number_of_talker_r <= number_of_talker_r + 1;
            database_state_r <= DB_SAVE_S;
          end
          if (talker_departed_i) begin // after EVT_TK_DEPARTED provided to ACMP
          // from discovery_state module, this input is expected with correct entity_id
            talker_entity_id_r <= talker_entity_id_i;
            number_of_talker_r <= number_of_talker_r - 1;
            database_state_r <= DB_DELETE_S;
          end
        end

        DB_SAVE_S : begin
          if (save_index_ready_r) begin
            bounded_talker_db_r[save_index_r] <= talker_entity_id_r;
            active_talker_r[save_index_r] <= 1'd1;
            database_state_r <= DB_SAVE_DONE_S;
          end
        end

        DB_DELETE_S : begin
          if (delete_index_ready_r) begin
            active_talker_r[delete_index_r] <= 1'd0;
            database_state_r <= DB_DEL_DONE_S;
          end
        end

        DB_DEL_DONE_S : database_state_r <= DB_IDLE_S;
        DB_SAVE_DONE_S : database_state_r <= DB_IDLE_S;
        
      endcase
    end
  end
  
  /*
    Process for handling save_index_r and save_index_ready regs.
    Loop through the bounded_talker_id to check what's the next
    available index.
    Provide the index and ready registers to database
  */
  always @(posedge clk_i) begin
    if (!rst_n) begin
      save_index_r <= '0;
      save_index_counter_r <= '0;
      save_index_ready_r <= 1'd0;
      save_state_r <= INDEX_IDLE_S;
    end
    else begin
      case (save_state_r)
        INDEX_IDLE_S : begin
          save_index_r <= '0;
          save_state_r <= INDEX_SEARCH_S;
        end

        INDEX_SEARCH_S : begin
          if (!(active_talker_r[save_index_counter_r])) begin// Empty place
            save_index_r <= save_index_counter_r;
            save_index_ready_r <= 1'd1;
            save_state_r <= INDEX_WAIT_S;
          end
          else begin // Place is occupied
            save_index_counter_r <= save_index_counter_r + 1;
          end
        end

        INDEX_WAIT_S : begin
          if (database_state_r == DB_SAVE_DONE_S) begin // talker_id saved
            save_index_ready_r <= 1'd0;
            save_state_r <= INDEX_IDLE_S;
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
  always @(posedge clk_i) begin
    if (!rst_n) begin
      delete_index_r <= '0;
      delete_index_counter_r <= '0;
      delete_index_ready_r <= '0;
      delete_state_r <= INDEX_IDLE_S;
    end
    else begin
      case (delete_state_r)
        INDEX_IDLE_S : begin
          if (talker_departed_i) begin
            delete_state_r <= INDEX_SEARCH_S;
          end
        end

        INDEX_SEARCH_S : begin
          if (bounded_talker_db_r[delete_index_counter_r] == talker_entity_id_r) begin
            // talker_ids matched
            delete_index_r <= delete_index_counter_r;
            delete_index_ready_r <= 1'd1;
            delete_state_r <= INDEX_WAIT_S;
          end
          else begin // no match, keep searching
            delete_index_counter_r <= delete_index_counter_r + 1;
          end
        end

        INDEX_WAIT_S : begin
          if (database_state_r == DB_DEL_DONE_S) begin // talker_id deleted
            delete_index_counter_r <= '0;
            delete_index_ready_r <= 1'd0;
            delete_state_r <= INDEX_IDLE_S;
          end
        end
      endcase
    end
  end
endmodule

`default_nettype wire
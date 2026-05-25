/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_l0_state.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP L0 (entity-level) state machine.

                Tracks the ACQUIRE_ENTITY and LOCK_ENTITY state per
                IEEE 1722.1-2021 §7.5.1 and §7.5.2:

                ACQUIRE_ENTITY
                  • flag[0]=0  → set acquired, record acquiring_controller_id
                  • flag[0]=1  → RELEASE: clear acquired
                  • Other controllers' mutating commands return
                    STATUS_ENTITY_ACQUIRED while acquired=1

                LOCK_ENTITY
                  • flag[0]=0  → set locked, reload 60 000-tick countdown
                  • flag[0]=1  → UNLOCK: clear locked
                  • Timer auto-expires after LOCK_TIMER_TICKS_C × tick_1khz_i
                  • Other controllers' mutating commands return
                    STATUS_ENTITY_LOCKED while locked=1

                status_o is driven combinationally so the response builder
                can latch it on the same cycle as hdr_i.hdr_valid.

                reject_o is asserted for one cycle when hdr_i.hdr_valid is
                high and the command is rejected due to locked/acquired state.

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §7.5.1, §7.5.2; Milan v1.2 §5.4
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_l0_state (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire [63:0]   entity_id_i,            //! EUI-64, driven from top-level MAC
  input  aecp_hdr_t    hdr_i,                  //! from common_parser
  input  wire          tick_1khz_i,            //! 1 kHz strobe from KL_aecp_timers
  input  wire          cmd_done_i,             //! response_builder signalled TX done
  output aecp_l0_state_t l0_state_o,
  output logic [4:0]   status_o,              //! for current command
  output logic         reject_o               //! this command was rejected (lock/acquire)
);

  // ------------------------------------------------------------------ //
  // State registers                                                      //
  // ------------------------------------------------------------------ //
  logic        acquired_r;
  logic [63:0] acquiring_controller_id_r;

  logic        locked_r;
  logic [63:0] locking_controller_id_r;
  logic [16:0] lock_timer_r;               //! 17-bit downcounter (ticks)

  logic [15:0] current_config_r;

  // ------------------------------------------------------------------ //
  // Wire-out the L0 state struct                                         //
  // ------------------------------------------------------------------ //
  assign l0_state_o.entity_id                = entity_id_i;
  assign l0_state_o.current_configuration_index = current_config_r;
  assign l0_state_o.locked                   = locked_r;
  assign l0_state_o.acquired                 = acquired_r;
  assign l0_state_o.acquiring_controller_id  = acquiring_controller_id_r;
  assign l0_state_o.locking_controller_id    = locking_controller_id_r;

  // ------------------------------------------------------------------ //
  // Combinational status / reject logic                                  //
  //                                                                      //
  // Rules (simplified; see spec for full controller-identity checks):    //
  //  1. If entity is acquired by another controller and the command is   //
  //     a mutating command → STATUS_ENTITY_ACQUIRED                      //
  //  2. If entity is locked by another controller → STATUS_ENTITY_LOCKED //
  //  3. ACQUIRE_ENTITY / LOCK_ENTITY themselves are always allowed (they //
  //     update the state below).                                          //
  //  4. Non-mutating read commands are always allowed.                   //
  // ------------------------------------------------------------------ //

  // Commands that are always allowed regardless of acquired/locked state
  wire w_exempt = (hdr_i.command_type == CMD_ACQUIRE_ENTITY)  ||
                  (hdr_i.command_type == CMD_LOCK_ENTITY)      ||
                  (hdr_i.command_type == CMD_ENTITY_AVAILABLE) ||
                  (hdr_i.command_type == CMD_CONTROLLER_AVAILABLE) ||
                  (hdr_i.command_type == CMD_READ_DESCRIPTOR)  ||
                  (hdr_i.command_type == CMD_GET_CONFIGURATION)||
                  (hdr_i.command_type == CMD_GET_STREAM_FORMAT)||
                  (hdr_i.command_type == CMD_GET_NAME)         ||
                  (hdr_i.command_type == CMD_GET_SAMPLING_RATE)||
                  (hdr_i.command_type == CMD_GET_CLOCK_SOURCE) ||
                  (hdr_i.command_type == CMD_GET_CONTROL)      ||
                  (hdr_i.command_type == CMD_GET_AVB_INFO)     ||
                  (hdr_i.command_type == CMD_GET_COUNTERS)     ||
                  (hdr_i.command_type == CMD_GET_AUDIO_MAP)    ||
                  (hdr_i.command_type == CMD_REGISTER_UNSOLICITED_NOTIFICATION)   ||
                  (hdr_i.command_type == CMD_DEREGISTER_UNSOLICITED_NOTIFICATION);

  wire w_from_acquiring = acquired_r &&
       (hdr_i.controller_entity_id == acquiring_controller_id_r);

  wire w_from_locking = locked_r &&
       (hdr_i.controller_entity_id == locking_controller_id_r);

  // Block if acquired and requestor is not the acquiring controller
  wire w_block_acquired = acquired_r && !w_from_acquiring && !w_exempt;

  // Block if locked and requestor is not the locking controller
  wire w_block_locked   = locked_r   && !w_from_locking   && !w_exempt;

  // SET_CONFIGURATION with out-of-range config_index → BAD_ARGUMENTS
  wire w_bad_config = (hdr_i.command_type == CMD_SET_CONFIGURATION) &&
                      (hdr_i.configuration_index >= 16'(NUM_CONFIGURATIONS_C));

  always_comb begin
    if (!hdr_i.hdr_valid) begin
      status_o = STATUS_SUCCESS;
      reject_o = 1'b0;
    end else if (w_block_acquired) begin
      status_o = STATUS_ENTITY_ACQUIRED;
      reject_o = 1'b1;
    end else if (w_block_locked) begin
      status_o = STATUS_ENTITY_LOCKED;
      reject_o = 1'b1;
    end else if (w_bad_config) begin
      status_o = STATUS_BAD_ARGUMENTS;
      reject_o = 1'b1;
    end else begin
      status_o = STATUS_SUCCESS;
      reject_o = 1'b0;
    end
  end

  // ------------------------------------------------------------------ //
  // Sequential state update                                              //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      acquired_r                 <= 1'b0;
      acquiring_controller_id_r  <= 64'd0;
      locked_r                   <= 1'b0;
      locking_controller_id_r    <= 64'd0;
      lock_timer_r               <= 17'd0;
      current_config_r           <= 16'd0;
    end else begin

      // ---------------------------------------------------------------- //
      // Lock timer countdown                                              //
      // ---------------------------------------------------------------- //
      if (locked_r && tick_1khz_i) begin
        if (lock_timer_r == 17'd0) begin
          // Timer expired — auto-unlock
          locked_r              <= 1'b0;
          locking_controller_id_r <= 64'd0;
        end else begin
          lock_timer_r <= lock_timer_r - 17'd1;
        end
      end

      // ---------------------------------------------------------------- //
      // Process incoming commands on hdr_valid strobe                    //
      // ---------------------------------------------------------------- //
      if (hdr_i.hdr_valid && !w_block_acquired && !w_block_locked) begin

        case (hdr_i.command_type)
          // ------------------------------------------------------------ //
          CMD_ACQUIRE_ENTITY: begin
            // Bit 0 of payload (flag) determines RELEASE.
            // hdr_i does not carry the acquire flags directly; the flag is
            // in the AEM payload (bytes 24+).  For this implementation the
            // u_flag field is repurposed as the RELEASE flag stub.
            // TODO: route acquire_flags[0] from cmd_specific_extract.
            if (hdr_i.u_flag) begin
              // RELEASE
              if (hdr_i.controller_entity_id == acquiring_controller_id_r) begin
                acquired_r                <= 1'b0;
                acquiring_controller_id_r <= 64'd0;
              end
              // else: ignore RELEASE from a non-owner
            end else begin
              if (!acquired_r) begin
                acquired_r                <= 1'b1;
                acquiring_controller_id_r <= hdr_i.controller_entity_id;
              end
              // else: already acquired by this or another controller
              //       (status was handled combinationally above)
            end
          end

          // ------------------------------------------------------------ //
          CMD_LOCK_ENTITY: begin
            // u_flag used as UNLOCK stub — TODO: route lock_flags[0]
            if (hdr_i.u_flag) begin
              // UNLOCK
              if (hdr_i.controller_entity_id == locking_controller_id_r) begin
                locked_r              <= 1'b0;
                locking_controller_id_r <= 64'd0;
                lock_timer_r          <= 17'd0;
              end
            end else begin
              if (!locked_r) begin
                locked_r              <= 1'b1;
                locking_controller_id_r <= hdr_i.controller_entity_id;
                lock_timer_r          <= LOCK_TIMER_TICKS_C;
              end
              // else: re-lock from same controller reloads timer
              else if (hdr_i.controller_entity_id == locking_controller_id_r) begin
                lock_timer_r <= LOCK_TIMER_TICKS_C;
              end
            end
          end

          // ------------------------------------------------------------ //
          CMD_SET_CONFIGURATION: begin
            // Out-of-range index is caught combinationally by w_bad_config
            // (status_o = STATUS_BAD_ARGUMENTS, reject_o = 1) before we get
            // here; w_block_acquired/locked gates the entire case block.
            // This guard is a defensive belt-and-suspenders redundancy.
            if (hdr_i.configuration_index < 16'(NUM_CONFIGURATIONS_C)) begin
              current_config_r <= hdr_i.configuration_index;
            end
          end

          // ------------------------------------------------------------ //
          default: begin
            // Other commands do not affect L0 state
          end
        endcase
      end // if hdr_valid

    end // else rst_n
  end

endmodule

`default_nettype wire

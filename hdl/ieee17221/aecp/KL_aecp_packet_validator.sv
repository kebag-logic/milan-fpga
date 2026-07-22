/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_packet_validator.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP packet validator — first pipeline stage.

                Inspects the first 64-bit beat of an AVTP/AECP frame and
                decides whether to pass or drop the entire packet:

                DROP conditions:
                  • message_type ∉ {MSG_AEM_COMMAND, MSG_VENDOR_UNIQUE_COMMAND}
                    → status_o = STATUS_NOT_SUPPORTED (11)
                  • control_data_length < 20 (minimum AEM header without payload)
                    → status_o = STATUS_BAD_ARGUMENTS (7)

                Valid frames are forwarded beat-by-beat from s_axis to m_axis.
                Dropped frames are consumed from s_axis without forwarding.

                Sideband outputs (registered, hold until next frame):
                  valid_o        — asserted for one cycle on last beat of good frame
                  drop_o         — asserted for one cycle on last beat of bad frame
                  status_o[4:0]  — status code for the current decision
                  message_type_o — latched message_type from beat 0

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9.1, Table 9.1
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_packet_validator (
  input  wire          clk_i,
  input  wire          rst_n,
  input  wire          s_axis_tvalid,
  output logic         s_axis_tready,
  input  wire [63:0]   s_axis_tdata,
  input  wire [7:0]    s_axis_tkeep,
  input  wire          s_axis_tlast,
  output logic         m_axis_tvalid,
  input  wire          m_axis_tready,
  output logic [63:0]  m_axis_tdata,
  output logic [7:0]   m_axis_tkeep,
  output logic         m_axis_tlast,
  output logic         valid_o,
  output logic         drop_o,
  output logic [4:0]   status_o,
  output logic [3:0]   message_type_o
);

  // ------------------------------------------------------------------ //
  // FSM                                                                  //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] {
    FIRST_BEAT_S,
    PASS_S,
    DROP_S
  } state_t;

  state_t state_r;

  // ------------------------------------------------------------------ //
  // Internal registers                                                   //
  // ------------------------------------------------------------------ //
  logic [3:0]  msg_type_r;
  logic [4:0]  status_r;
  logic        frame_valid_r;   //! set when this frame passes validation

  // ------------------------------------------------------------------ //
  // Field extraction from beat 0 (64-bit, big-endian, MSB = byte 0)     //
  //                                                                      //
  //  [63:48] EtherType  0x22F0  (already checked upstream)              //
  //  [47:40] subtype    0xFB    (already checked upstream)              //
  //  [39:36] h/version  (don't care)                                    //
  //  [35:32] message_type[3:0]                                          //
  //  [31:27] incoming status (must be 0 for commands)                   //
  //  [26:16] control_data_length[10:0]                                  //
  // ------------------------------------------------------------------ //
  // verilator lint_off SELRANGE  // tdata is 64b at runtime; default if param is 32
  wire [3:0]  w_msg_type = s_axis_tdata[35:32];
  wire [10:0] w_cdl      = s_axis_tdata[26:16];
  // verilator lint_on  SELRANGE

  // ------------------------------------------------------------------ //
  // Validation combinational                                             //
  // ------------------------------------------------------------------ //
  wire w_type_ok = (w_msg_type == MSG_AEM_COMMAND) ||
                   (w_msg_type == MSG_VENDOR_UNIQUE_COMMAND);
  //! Minimum AECPDU: controller_entity_id(8) + sequence_id(2) + u/command(2)
  //! = 12 (e.g. GET_CONFIGURATION has no payload at all).
  wire w_cdl_ok  = (w_cdl >= 11'd12);
  wire w_ok      = w_type_ok & w_cdl_ok;

  // own outputs mirrored in local nets: reading them back through the
  // modport (s_axis_tready / m_axis_tvalid) makes sv2v emit an absolute
  // hierarchical path that only resolves when KL_aecp_top is the top —
  // breaking the Yosys portability gate under milan_datapath.
  logic s_tready_l, m_tvalid_l;
  assign s_axis_tready = s_tready_l;
  assign m_axis_tvalid = m_tvalid_l;

  wire w_hs_s    = s_axis_tvalid & s_tready_l;      //! slave handshake
  wire w_hs_m    = m_tvalid_l & m_axis_tready;      //! master handshake

  // ------------------------------------------------------------------ //
  // AXI-Stream forwarding                                                //
  // In PASS_S: connect tvalid from slave to master.                     //
  // In FIRST_BEAT_S: also forward (decision taken combinationally).     //
  // In DROP_S: consume from slave, do NOT assert master tvalid.         //
  // Slave tready follows master tready when forwarding.                 //
  // ------------------------------------------------------------------ //
  always_comb begin
    m_tvalid_l    = 1'b0;
    m_axis_tdata  = s_axis_tdata;
    m_axis_tlast  = s_axis_tlast;
    m_axis_tkeep  = s_axis_tkeep;
    s_tready_l    = 1'b0;

    case (state_r)
      FIRST_BEAT_S: begin
        if (w_ok) begin
          // Forward this beat immediately — tready from master governs
          m_tvalid_l    = s_axis_tvalid;
          s_tready_l    = m_axis_tready;
        end else begin
          // Drop: accept from slave, do not forward
          s_tready_l    = 1'b1;
          m_tvalid_l    = 1'b0;
        end
      end

      PASS_S: begin
        m_tvalid_l    = s_axis_tvalid;
        s_tready_l    = m_axis_tready;
      end

      DROP_S: begin
        s_tready_l    = 1'b1;
        m_tvalid_l    = 1'b0;
      end

      default: begin
        s_tready_l    = 1'b0;
        m_tvalid_l    = 1'b0;
      end
    endcase
  end

  // ------------------------------------------------------------------ //
  // FSM — sequential                                                     //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      state_r        <= FIRST_BEAT_S;
      msg_type_r     <= 4'd0;
      status_r       <= STATUS_SUCCESS;
      frame_valid_r  <= 1'b0;
      valid_o        <= 1'b0;
      drop_o         <= 1'b0;
      status_o       <= STATUS_SUCCESS;
      message_type_o <= 4'd0;
    end else begin
      // Default: clear strobes
      valid_o <= 1'b0;
      drop_o  <= 1'b0;

      case (state_r)
        // ------------------------------------------------------------ //
        FIRST_BEAT_S: begin
          if (s_axis_tvalid) begin
            msg_type_r    <= w_msg_type;
            message_type_o <= w_msg_type;

            if (w_ok) begin
              status_r      <= STATUS_SUCCESS;
              frame_valid_r <= 1'b1;
              // Handshake completes when master accepts
              if (m_axis_tready) begin
                if (s_axis_tlast) begin
                  // Single-beat frame — done immediately
                  valid_o  <= 1'b1;
                  status_o <= STATUS_SUCCESS;
                  state_r  <= FIRST_BEAT_S;
                end else begin
                  state_r <= PASS_S;
                end
              end
            end else begin
              // Determine which error
              if (!w_type_ok) begin
                status_r  <= STATUS_NOT_SUPPORTED;
                status_o  <= STATUS_NOT_SUPPORTED;
              end else begin
                status_r  <= STATUS_BAD_ARGUMENTS;
                status_o  <= STATUS_BAD_ARGUMENTS;
              end
              frame_valid_r <= 1'b0;

              // Consume this beat (tready=1 in comb for DROP case)
              if (s_axis_tlast) begin
                // Single-beat bad frame
                drop_o  <= 1'b1;
                state_r <= FIRST_BEAT_S;
              end else begin
                state_r <= DROP_S;
              end
            end
          end
        end

        // ------------------------------------------------------------ //
        PASS_S: begin
          if (w_hs_s) begin
            if (s_axis_tlast) begin
              valid_o  <= 1'b1;
              status_o <= STATUS_SUCCESS;
              state_r  <= FIRST_BEAT_S;
            end
          end
        end

        // ------------------------------------------------------------ //
        DROP_S: begin
          if (s_axis_tvalid) begin   // tready always 1 in comb
            if (s_axis_tlast) begin
              drop_o  <= 1'b1;
              state_r <= FIRST_BEAT_S;
            end
          end
        end

        default: state_r <= FIRST_BEAT_S;
      endcase
    end
  end

endmodule

`default_nettype wire

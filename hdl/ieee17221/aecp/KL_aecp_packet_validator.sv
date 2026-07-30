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
  wire [3:0]  w_msg_type = s_axis_tdata[35:32];
  wire [10:0] w_cdl      = s_axis_tdata[26:16];

  // ------------------------------------------------------------------ //
  // Validation combinational                                             //
  // ------------------------------------------------------------------ //
  wire w_type_ok = (w_msg_type == MSG_AEM_COMMAND) ||
                   (w_msg_type == MSG_VENDOR_UNIQUE_COMMAND);
  //! Minimum AECPDU: controller_entity_id(8) + sequence_id(2) + u/command(2)
  //! = 12 (e.g. GET_CONFIGURATION has no payload at all).
  wire w_cdl_ok  = (w_cdl >= 11'd12);
  wire w_ok      = w_type_ok & w_cdl_ok;

  // ------------------------------------------------------------------ //
  // DECLARED length vs DELIVERED length (A-F14)                          //
  //                                                                      //
  // control_data_length was only ever checked for a LOWER bound. Nothing  //
  // compared it against the octets the frame actually carried, so a       //
  // SHORT frame could declare a long one and every consumer downstream    //
  // believed the header: the response builder's capture buffer is not     //
  // cleared between frames, so a 60-byte ADD_AUDIO_MAPPINGS declaring     //
  // control_data_length = 20 + 8N walked N mapping records out of the     //
  // PREVIOUS command's residue and committed them, and the echo segment   //
  // - sized from the same declared length - put up to 494 octets of       //
  // whatever the last controller sent back on the wire, to a different    //
  // controller. Two bugs, one missing compare.                            //
  //                                                                      //
  // The arithmetic, from the beat-0 map above: this stream begins at the  //
  // EtherType. control_data_length counts the control_data_payload only   //
  // (1722-2016 4.4.5.4): for an AECPDU that region begins at AECPDU octet //
  // 12 = controller_entity_id - it EXCLUDES target_entity_id, which       //
  // occupies the stream_id position at octets 4..11. This module's stream //
  // starts 2 octets earlier than the AECPDU (at the EtherType), so the    //
  // cdl region begins at STREAM byte 14 = EtherType(2) + subtype(1) +     //
  // sv/ver/msg(1) + status/cdl(2) + target_entity_id(8), and a well-formed//
  // frame carries at least 14 + control_data_length octets. Cross-checks: //
  // the module's own minimum-AECPDU comment above (controller_entity_id 8 //
  // + sequence_id 2 + u/command 2 = 12 = the cdl FLOOR), every cdl the    //
  // response builder emits (12 + payload), and 1722-2016 B.2's "cdl shall //
  // be set to 16 in all MAAP frames" against MAAP's 16 post-stream_id     //
  // octets. ORIGIN 6 (Opus verify 2026-07-30) left an 8-octet hole =      //
  // exactly one 64-bit beat = one forgeable mapping record from cbuf      //
  // residue. Padding makes frames LONGER (a 60-byte Ethernet minimum),    //
  // never shorter, so the test stays one-sided.                           //
  // ------------------------------------------------------------------ //
  localparam int unsigned CDL_ORIGIN_C = 14;  //! octets before the cdl region
  logic [12:0] blen_r;        //! octets accepted so far THIS frame
  logic [10:0] cdl_r;        //! this frame's declared control_data_length
  //! octets in the beat being handshaken (tkeep is contiguous, but count it
  //! rather than assume, so a short tail beat is measured not guessed)
  wire [3:0] w_kcnt = 4'(s_axis_tkeep[0]) + 4'(s_axis_tkeep[1])
                    + 4'(s_axis_tkeep[2]) + 4'(s_axis_tkeep[3])
                    + 4'(s_axis_tkeep[4]) + 4'(s_axis_tkeep[5])
                    + 4'(s_axis_tkeep[6]) + 4'(s_axis_tkeep[7]);
  //! running total INCLUDING the current beat; beat 0 restarts the count
  //! (blen_r still holds the previous frame's total at that point)
  wire [12:0] w_blen_now = (state_r == FIRST_BEAT_S)
                           ? {9'd0, w_kcnt} : blen_r + {9'd0, w_kcnt};
  wire [10:0] w_cdl_now  = (state_r == FIRST_BEAT_S) ? w_cdl : cdl_r;
  //! evaluated on the LAST beat, when the delivered length is finally known
  wire w_len_short = ({2'd0, w_cdl_now} + 13'(CDL_ORIGIN_C)) > w_blen_now;

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
      blen_r         <= 13'd0;
      cdl_r          <= 11'd0;
    end else begin
      // Default: clear strobes
      valid_o <= 1'b0;
      drop_o  <= 1'b0;

      //! delivered-octet accounting (A-F14): every beat this module accepts,
      //! in EITHER direction (forwarded or dropped), so the total is right
      //! whatever the verdict. Beat 0 restarts it.
      if (w_hs_s || (state_r == DROP_S && s_axis_tvalid)) begin
        blen_r <= w_blen_now;
        if (state_r == FIRST_BEAT_S) cdl_r <= w_cdl;
      end

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
                  //! Single-beat frame — the delivered length is known NOW,
                  //! so the A-F14 compare decides the verdict here.
                  if (w_len_short) begin
                    drop_o   <= 1'b1;
                    status_o <= STATUS_BAD_ARGUMENTS;
                  end else begin
                    valid_o  <= 1'b1;
                    status_o <= STATUS_SUCCESS;
                  end
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
              //! A-F14: the frame is only GOOD if it delivered at least the
              //! 6 + control_data_length octets its own header promised. The
              //! beats are already downstream by now - this strobe is what
              //! the response builder arms on, so withholding it is exactly
              //! "do not act on this frame".
              if (w_len_short) begin
                drop_o   <= 1'b1;
                status_o <= STATUS_BAD_ARGUMENTS;
              end else begin
                valid_o  <= 1'b1;
                status_o <= STATUS_SUCCESS;
              end
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

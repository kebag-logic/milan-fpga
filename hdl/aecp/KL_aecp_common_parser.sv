/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_common_parser.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP common header parser — second pipeline stage.

                Extracts the fixed AECP common control header from the AXI-
                Stream carrying an AECP frame (already validated by
                KL_aecp_packet_validator).  All beats are transparently
                forwarded to m_axis so downstream modules can also inspect
                the raw payload.

                Beat mapping (64-bit / 8-byte TDATA, big-endian):
                  Beat 0 [bytes  0– 7]: EtherType, subtype, {h,ver,msg_type},
                                        {status[4:0],cdl[10:8]}, cdl[7:0],
                                        target_eid[63:48]
                  Beat 1 [bytes  8–15]: target_eid[47:0], ctlr_eid[63:48]
                  Beat 2 [bytes 16–23]: ctlr_eid[47:0], sequence_id[15:0]
                  Beat 3 [bytes 24–31]: {u_flag,cmd_type[14:8]}, cmd_type[7:0],
                                        (cmd-specific payload starts here)

                hdr_o.hdr_valid is asserted for exactly one cycle when Beat 3
                is successfully accepted (tvalid & tready in BEAT3_S).

                mismatch_o is asserted when target_entity_id ≠ l0_state_i.entity_id
                and the frame should be silently discarded.

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9.1, §9.2
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_common_parser (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_l0_state_t l0_state_i,   //! from KL_aecp_l0_state for entity_id check
  axi_stream_if.slave  s_axis,          //! from KL_aecp_packet_validator m_axis
  axi_stream_if.master m_axis,          //! to KL_aecp_cmd_specific_extract
  output aecp_hdr_t    hdr_o,           //! parsed header (valid when hdr_o.hdr_valid)
  output logic         mismatch_o       //! entity_id mismatch (dropped silently)
);

  // ------------------------------------------------------------------ //
  // FSM                                                                  //
  // ------------------------------------------------------------------ //
  typedef enum logic [2:0] {
    IDLE_S,
    BEAT0_S,
    BEAT1_S,
    BEAT2_S,
    BEAT3_S,
    PAYLOAD_S     //! drain remaining payload beats transparently
  } state_t;

  state_t state_r;

  // ------------------------------------------------------------------ //
  // Internal header accumulator                                          //
  // ------------------------------------------------------------------ //
  aecp_hdr_t hdr_r;

  // ------------------------------------------------------------------ //
  // Transparent AXI-Stream passthrough                                   //
  // ------------------------------------------------------------------ //
  assign m_axis.tvalid = s_axis.tvalid;
  assign m_axis.tdata  = s_axis.tdata;
  assign m_axis.tlast  = s_axis.tlast;
  assign m_axis.tkeep  = s_axis.tkeep;
  assign m_axis.tstrb  = s_axis.tstrb;
  assign m_axis.tid    = s_axis.tid;
  assign m_axis.tdest  = s_axis.tdest;
  assign m_axis.tuser  = s_axis.tuser;
  assign s_axis.tready = m_axis.tready;

  wire w_hs = s_axis.tvalid & s_axis.tready;

  // ------------------------------------------------------------------ //
  // Sequential FSM + extraction                                          //
  // ------------------------------------------------------------------ //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      state_r          <= IDLE_S;
      hdr_r            <= '0;
      hdr_o            <= '0;
      mismatch_o       <= 1'b0;
    end else begin
      // Default: clear hdr_valid strobe each cycle
      hdr_o.hdr_valid  <= 1'b0;

      case (state_r)
        // ------------------------------------------------------------ //
        IDLE_S: begin
          mismatch_o <= 1'b0;   // clear on every IDLE cycle
          if (s_axis.tvalid) begin
            state_r <= BEAT0_S;
          end
        end

        // ------------------------------------------------------------ //
        // Beat 0 [bytes 0–7]:
        //   [63:48] EtherType
        //   [47:40] subtype
        //   [39:36] h/version (don't care)
        //   [35:32] message_type[3:0]
        //   [31:27] status[4:0]
        //   [26:16] control_data_length[10:0]
        //   [15: 0] target_entity_id[63:48]
        // ------------------------------------------------------------ //
        // verilator lint_off SELRANGE  // tdata is 64b at runtime; default if param is 32
        BEAT0_S: begin
          if (w_hs) begin
            hdr_r.message_type        <= s_axis.tdata[35:32];
            hdr_r.status              <= s_axis.tdata[31:27];
            hdr_r.control_data_length <= s_axis.tdata[26:16];
            hdr_r.target_entity_id[63:48] <= s_axis.tdata[15:0];
            state_r <= BEAT1_S;
          end
        end

        // ------------------------------------------------------------ //
        // Beat 1 [bytes 8–15]:
        //   [63:16] target_entity_id[47:0]
        //   [15: 0] controller_entity_id[63:48]
        // ------------------------------------------------------------ //
        BEAT1_S: begin
          if (w_hs) begin
            hdr_r.target_entity_id[47:0]       <= s_axis.tdata[63:16];
            hdr_r.controller_entity_id[63:48]  <= s_axis.tdata[15:0];
            state_r <= BEAT2_S;
          end
        end

        // ------------------------------------------------------------ //
        // Beat 2 [bytes 16–23]:
        //   [63:16] controller_entity_id[47:0]
        //   [15: 0] sequence_id[15:0]
        // ------------------------------------------------------------ //
        BEAT2_S: begin
          if (w_hs) begin
            hdr_r.controller_entity_id[47:0] <= s_axis.tdata[63:16];
            hdr_r.sequence_id                <= s_axis.tdata[15:0];
            state_r <= BEAT3_S;
          end
        end

        // ------------------------------------------------------------ //
        // Beat 3 [bytes 24–31]:
        //   [63]    u_flag
        //   [62:56] cmd_type[14:8]
        //   [55:48] cmd_type[7:0]
        //   [47: 0] command-specific payload (forwarded, not captured here)
        //
        // On handshake: assert hdr_valid, check entity_id, go back to IDLE.
        // ------------------------------------------------------------ //
        BEAT3_S: begin
          if (w_hs) begin
            hdr_r.u_flag       <= s_axis.tdata[63];
            hdr_r.command_type <= {s_axis.tdata[62:56], s_axis.tdata[55:48]};
            hdr_r.hdr_valid    <= 1'b1;

            // Publish the complete header
            hdr_o              <= hdr_r;
            hdr_o.u_flag       <= s_axis.tdata[63];
            hdr_o.command_type <= {s_axis.tdata[62:56], s_axis.tdata[55:48]};
            hdr_o.hdr_valid    <= 1'b1;

            // Entity-ID mismatch check
            if (hdr_r.target_entity_id != l0_state_i.entity_id) begin
              mismatch_o <= 1'b1;
            end

            // TODO: extract configuration_index / descriptor_type / descriptor_index
            //       from beats 4+ for descriptor commands.  For now zeroed.
            hdr_o.configuration_index <= 16'd0;
            hdr_o.descriptor_type     <= 16'd0;
            hdr_o.descriptor_index    <= 16'd0;

            if (s_axis.tlast) begin
              state_r <= IDLE_S;
            end else begin
              // Remaining payload beats (e.g. ACQUIRE/LOCK/READ_DESCRIPTOR have
              // bytes 32+) are forwarded transparently via the combinational
              // assign passthrough.  FSM drains here until tlast.
              state_r <= PAYLOAD_S;
            end
          end
        end

        // ------------------------------------------------------------ //
        // Drain payload beats transparently after header extraction     //
        // ------------------------------------------------------------ //
        // verilator lint_on  SELRANGE
        PAYLOAD_S: begin
          if (w_hs && s_axis.tlast) begin
            state_r <= IDLE_S;
          end
        end

        default: begin
          state_r <= IDLE_S;
          $error("[KL_aecp_common_parser] undefined FSM state — resetting to IDLE");
        end
      endcase
    end
  end

endmodule

`default_nettype wire

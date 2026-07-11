/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_vu_milan.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : Milan Vendor-Unique AECP handler — STUB.

                Handles MSG_VENDOR_UNIQUE_COMMAND frames whose protocol_id
                matches MILAN_PROTOCOL_ID_C (OUI 00-1B-C5-0A-C1-00).

                Supported sub-commands (Milan v1.2 §5.4):
                  VU_GET_MILAN_INFO              (0x01)
                  VU_GET_SYSTEM_UNIQUE_ID        (0x10)
                  VU_SET_SYSTEM_UNIQUE_ID        (0x11)
                  VU_GET_MEDIA_CLOCK_REFERENCE_INFO (0x20)
                  VU_SET_MEDIA_CLOCK_REFERENCE_INFO (0x21)

                Unsupported sub-commands → not_impl_o asserted, response
                carries STATUS_NOT_IMPLEMENTED.

                Ports:
                  hdr_i      — parsed common header
                  tick_1khz_i — 1 kHz strobe for timing
                  s_axis     — raw frame (to extract VU payload)
                  m_axis     — response frame output
                  not_impl_o — sub-command not recognised

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : Milan v1.2 §5.4; IEEE Std 1722.1-2021 §9.2.6
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_vu_milan (
  input  wire          clk_i,
  input  wire          rst_n,
  input  aecp_hdr_t    hdr_i,
  input  wire          tick_1khz_i,
  axi_stream_if.slave  s_axis,
  axi_stream_if.master m_axis,
  output logic         not_impl_o
);

  // TODO: implement Milan Vendor-Unique command handler FSM

  // Consume slave data, do not forward
  assign s_axis.tready = 1'b1;

  // Drive master outputs to safe defaults
  assign m_axis.tvalid = 1'b0;
  assign m_axis.tdata  = '0;
  assign m_axis.tlast  = 1'b0;
  assign m_axis.tkeep  = '0;
  assign m_axis.tstrb  = '0;
  assign m_axis.tid    = '0;
  assign m_axis.tdest  = '0;
  assign m_axis.tuser  = '0;

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      not_impl_o <= 1'b0;
    end else begin
      // TODO: implement
      not_impl_o <= hdr_i.hdr_valid &&
                    (hdr_i.message_type == MSG_VENDOR_UNIQUE_COMMAND);
    end
  end

  // verilator lint_off UNUSED
  wire unused_tick = tick_1khz_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_vu_milan not yet implemented");
  end

endmodule

`default_nettype wire

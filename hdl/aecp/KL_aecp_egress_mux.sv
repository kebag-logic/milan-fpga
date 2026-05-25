/*
 * SPDX-FileCopyrightText: 2025 Kebag Logic <contact@kebag-logic.com>
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_aecp_egress_mux.sv
  Author      : TBD
  Date        : 2025-05-25
  Description : AECP egress multiplexer — STUB.

                Arbitrates between three upstream TX sources and serialises
                them onto a single m_axis output toward the MAC TX path:

                  s_axis_aem  — AEM command responses (KL_aecp_response_builder)
                  s_axis_vu   — Milan Vendor-Unique responses (KL_aecp_vu_milan)
                  s_axis_adp  — ADP frames injected into the same TX channel

                Arbitration policy: round-robin with credit gating.
                mac_credit_i asserted means the MAC TX FIFO has space for at
                least one maximum-size Ethernet frame (1522 bytes / 190 beats
                at 64-bit width).

                Ports:
                  s_axis_aem   — AEM response slave
                  s_axis_vu    — Vendor-Unique response slave
                  s_axis_adp   — ADP frame slave
                  m_axis       — merged output master
                  mac_credit_i — MAC TX FIFO credit available

  Target      : Artix-7 XC7A100T (125 MHz AVTP clock)
  Spec refs   : IEEE Std 1722.1-2021 §9; Milan v1.2 §5
  Company     : Kebag Logic
  Project     : Milan ADP / AECP
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aecp_egress_mux (
  input  wire          clk_i,
  input  wire          rst_n,
  axi_stream_if.slave  s_axis_aem,
  axi_stream_if.slave  s_axis_vu,
  axi_stream_if.slave  s_axis_adp,
  axi_stream_if.master m_axis,
  input  wire          mac_credit_i
);

  // TODO: implement round-robin arbitration with credit gating

  // Default: back-pressure all slaves, idle master
  assign s_axis_aem.tready = 1'b0;
  assign s_axis_vu.tready  = 1'b0;
  assign s_axis_adp.tready = 1'b0;

  assign m_axis.tvalid = 1'b0;
  assign m_axis.tdata  = '0;
  assign m_axis.tlast  = 1'b0;
  assign m_axis.tkeep  = '0;
  assign m_axis.tstrb  = '0;
  assign m_axis.tid    = '0;
  assign m_axis.tdest  = '0;
  assign m_axis.tuser  = '0;

  // verilator lint_off UNUSED
  wire unused_credit = mac_credit_i;
  // verilator lint_on  UNUSED

  initial begin
    $display("[TODO] KL_aecp_egress_mux not yet implemented");
  end

endmodule

`default_nettype wire

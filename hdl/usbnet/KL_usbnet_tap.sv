/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_tap.sv
  Description : The FPGA side of the USB network path (#1011, with
                kebag-logic/usb-audio#5): the attached computer as its own
                station behind the device, control traffic only.
                  rx copy    KL_usbnet_rx_copy: the frames the device
                             receives, filtered, toward the computer.
                  tx inject  KL_usbnet_tx_inject: the computer's records,
                             its address and its checked frames.
                  tx arb     KL_usbnet_tx_arb: the computer's frames into the
                             MAC below every datapath frame.
                It sits at the MAC wrapper's system-clock side: the receive
                copy reads the stream the datapath receives, the arbiter
                sits at the MAC core's transmit input, and the two bus
                streams run on this clock (a slave-FIFO master crosses them
                to its bus clock).
                usb_ok_o, the LD1 input of #1018: the bus master reports its
                bus clock running (bus_alive_i), the computer's side has
                handed over an address, and its last host record, at most
                HOST_TIMEOUT_MS_P old, says SuperSpeed.
                MAC-SIDE PAYLOAD. The two transmit streams carry {be, data}:
                be is the MAC core's last-octet one-hot (nonzero only on a
                frame's last beat), the form its transmit input takes.
  Spec refs   : #1011, #1018; docs/design/USB_NET_PATH.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_usbnet_tap
  import KL_usbnet_pkg::*;
#(
  parameter int unsigned     CLK_HZ_P          = 80_000_000,
  parameter longint unsigned RATE_BPS_P        = 64'd10_000_000,
  parameter int unsigned     BURST_OCTETS_P    = 3200,
  parameter int unsigned     HOST_TIMEOUT_MS_P = 3000
)(
  input  wire         clk_i,   //! the system clock, the MAC wrapper's
  input  wire         rst_ni,   //! synchronous reset, active low
  //! the device's receive stream, accepted beats
  input  wire         rx_valid_i,
  input  wire [63:0]  rx_data_i,
  input  wire [7:0]   rx_keep_i,
  input  wire         rx_last_i,
  //! the datapath's transmit stream, after its store-and-forward FIFO
  input  wire         hi_valid_i,
  output logic        hi_ready_o,
  input  wire         hi_last_i,
  input  wire [63:0]  hi_data_i,
  input  wire [7:0]   hi_be_i,
  //! the MAC core's transmit input
  output logic        m_valid_o,
  input  wire         m_ready_i,
  output logic        m_last_o,
  output logic [63:0] m_data_o,
  output logic [7:0]  m_be_o,
  input  wire         inject_en_i,
  input  wire         eth_clk_i,
  input  wire         eth_rst_ni,
  input  wire         eth_end_i,
  output logic        txend_tgl_o,
  //! the bus: toward the computer
  output logic        up_valid_o,
  input  wire         up_ready_i,
  output logic [15:0] up_data_o,
  output logic        up_last_o,
  //! the bus: from the computer
  input  wire         dn_valid_i,
  output logic        dn_ready_o,
  input  wire [15:0]  dn_data_i,
  input  wire         bus_alive_i,
  //! status
  output logic        usb_ok_o,
  output logic [47:0] host_mac_o,
  output logic        host_ok_o,
  output logic [15:0] host_state_o,
  output logic        rx_verdict_valid_o,
  output rx_verdict_e rx_verdict_o,
  output logic        tx_verdict_valid_o,
  output tx_verdict_e tx_verdict_o,
  output logic [15:0] rx_copied_o,
  output logic [15:0] rx_full_o,
  output logic [15:0] tx_passed_o,
  output logic [15:0] tx_dropped_o,
  output logic [15:0] tx_skipped_o,
  output logic [15:0] tx_injected_o,
  output logic        inj_active_o     //! an injected frame owns the MAC
);
  logic        host_fresh_w;
  logic        lo_valid_w, lo_ready_w, lo_last_w;
  logic [63:0] lo_data_w;
  logic [7:0]  lo_keep_w;

  KL_usbnet_rx_copy u_rx (
    .clk_i, .rst_ni,
    .s_valid_i (rx_valid_i), .s_data_i (rx_data_i), .s_keep_i (rx_keep_i),
    .s_last_i  (rx_last_i),
    .host_mac_i (host_mac_o), .host_ok_i (host_ok_o),
    .m_valid_o (up_valid_o), .m_ready_i (up_ready_i), .m_data_o (up_data_o),
    .m_last_o  (up_last_o),
    .verdict_valid_o (rx_verdict_valid_o), .verdict_o (rx_verdict_o),
    .copied_o (rx_copied_o), .dropped_full_o (rx_full_o)
  );

  KL_usbnet_tx_inject #(
    .CLK_HZ_P (CLK_HZ_P), .RATE_BPS_P (RATE_BPS_P),
    .BURST_OCTETS_P (BURST_OCTETS_P), .HOST_TIMEOUT_MS_P (HOST_TIMEOUT_MS_P)
  ) u_tx (
    .clk_i, .rst_ni,
    .s_valid_i (dn_valid_i), .s_ready_o (dn_ready_o), .s_data_i (dn_data_i),
    .m_valid_o (lo_valid_w), .m_ready_i (lo_ready_w), .m_data_o (lo_data_w),
    .m_keep_o  (lo_keep_w),  .m_last_o  (lo_last_w),
    .host_mac_o, .host_ok_o, .host_state_o, .host_fresh_o (host_fresh_w),
    .verdict_valid_o (tx_verdict_valid_o), .verdict_o (tx_verdict_o),
    .passed_o (tx_passed_o), .dropped_o (tx_dropped_o), .skipped_o (tx_skipped_o)
  );

  //! keep mask -> the core's last-octet one-hot, on the last beat only
  wire [7:0] lo_be_w = lo_last_w ? (lo_keep_w & ~(lo_keep_w >> 1)) : 8'h00;

  KL_usbnet_tx_arb #(.PW_P (72)) u_arb (
    .clk_i, .rst_ni,
    .hi_valid_i, .hi_ready_o, .hi_last_i, .hi_data_i ({hi_be_i, hi_data_i}),
    .lo_valid_i (lo_valid_w), .lo_ready_o (lo_ready_w), .lo_last_i (lo_last_w),
    .lo_data_i  ({lo_be_w, lo_data_w}),
    .m_valid_o, .m_ready_i, .m_last_o, .m_data_o ({m_be_o, m_data_o}),
    .inject_en_i,
    .eth_clk_i, .eth_rst_ni, .eth_end_i, .txend_tgl_o,
    .lo_active_o (inj_active_o), .injected_o (tx_injected_o)
  );

  assign usb_ok_o = bus_alive_i && host_ok_o && host_fresh_w && host_state_o[0];

endmodule

`default_nettype wire

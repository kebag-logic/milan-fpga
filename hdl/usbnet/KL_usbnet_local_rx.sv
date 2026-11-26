/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_local_rx.sv
  Description : The computer's local delivery into the split control receiver.
                A passive observer copies accepted computer frames addressed
                to this device or a group. The same receive rules exclude
                stream and link-local frames. Its independent whole-frame
                buffer cannot backpressure the MAC or its network receive
                path. A full buffer drops a whole local copy and counts it.
                Records are serialized into bytes and merged at the mailbox
                input, after network timestamping and media reception. The
                network control stream wins at frame boundaries. Each grant
                stays locked through stalls and the final accepted byte.
                Control delivery may wait one local frame; the network MAC,
                gPTP and audio receiver never wait for this merger.
  Spec refs   : #1011; docs/design/USB_NET_PATH.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_usbnet_local_rx (
  input wire clk_i,                       //! the MAC wrapper's system clock
  input wire rst_ni,                      //! synchronous active-low reset
  input wire [47:0] station_mac_i,         //! device MAC, first octet in bits 47:40
  input wire s_active_i,                   //! injector owns the MAC, through PHY retirement
  input wire s_valid_i,                    //! accepted computer injection beat
  input wire [63:0] s_data_i,              //! little lane order
  input wire [7:0] s_keep_i,               //! contiguous octet mask
  input wire s_last_i,                     //! the frame's final beat
  input wire net_valid_i,                  //! buffered network control byte
  output wire net_ready_o,                //! network control byte accepted
  input wire [7:0] net_data_i,             //! wire order
  input wire net_last_i,                   //! final network control byte
  output wire m_valid_o,                  //! byte into the device's receiver
  input wire m_ready_i,                   //! receiver accepts the byte
  output wire [7:0] m_data_o,              //! wire order
  output wire m_last_o,                   //! final byte
  output wire [15:0] copied_o,             //! whole local frames copied
  output wire [15:0] full_o                //! whole local copies lost to pressure
);
  wire rec_valid_w, rec_ready_w, rec_last_w;
  wire [15:0] rec_data_w;
  //! Verdict is redundant with the copy/drop counters at this filtered seam.
  wire verdict_valid_unused_w;
  wire [2:0] verdict_unused_w;
  logic active_r;
  always_ff @(posedge clk_i) begin : observe_grant
    if (!rst_ni) active_r <= 1'b0;
    else active_r <= s_active_i;
  end : observe_grant
  //! A cancelled grant may have no last beat. Successful grants retire only
  //! after their final beat has committed, so this also safely sees retirement.
  wire discard_w = active_r && !s_active_i;
  KL_usbnet_rx_copy #(.MAX_LEN_OCTETS_P(1515)) copy (
    .clk_i, .rst_ni, .s_valid_i, .s_data_i, .s_keep_i, .s_last_i,
    .discard_i(discard_w),
    //! This is the device receiver; its identity does not depend on USB attachment.
    .host_mac_i(station_mac_i), .host_ok_i(1'b1),
    .m_valid_o(rec_valid_w), .m_ready_i(rec_ready_w),
    .m_data_o(rec_data_w), .m_last_o(rec_last_w),
    .verdict_valid_o(verdict_valid_unused_w), .verdict_o(verdict_unused_w),
    .copied_o, .dropped_full_o(full_o)
  );

  typedef enum logic [1:0] {L_LENGTH, L_KIND, L_LOW, L_HIGH} local_state_e;
  local_state_e state_r;
  logic [11:0] left_r;
  logic locked_r, local_r;
  wire local_valid_w = rec_valid_w && (state_r == L_LOW || state_r == L_HIGH);
  wire local_last_w = left_r == 12'd1;
  wire choose_local_w = locked_r ? local_r : !net_valid_i && local_valid_w;
  assign m_valid_o = choose_local_w ? local_valid_w : net_valid_i;
  assign m_data_o = choose_local_w ? ((state_r == L_HIGH) ? rec_data_w[15:8] : rec_data_w[7:0]) : net_data_i;
  assign m_last_o = choose_local_w ? local_last_w : net_last_i;
  assign net_ready_o = !choose_local_w && m_ready_i;
  wire local_take_w = choose_local_w && m_ready_i && local_valid_w;
  assign rec_ready_w = (state_r == L_LENGTH || state_r == L_KIND) ||
                       (local_take_w && (state_r == L_HIGH || local_last_w));

  always_ff @(posedge clk_i) begin : serialize
    if (!rst_ni) begin
      state_r <= L_LENGTH;
      left_r <= '0;
      locked_r <= 1'b0;
      local_r <= 1'b0;
    end else begin
      if (m_valid_o) begin
        locked_r <= !(m_ready_i && m_last_o);
        local_r <= choose_local_w;
      end
      case (state_r)
        L_LENGTH: if (rec_valid_w) begin
          left_r <= rec_data_w[11:0];
          state_r <= L_KIND;
        end
        L_KIND: if (rec_valid_w) state_r <= L_LOW;
        default: if (local_take_w) begin
          left_r <= left_r - 1'b1;
          if (local_last_w) state_r <= L_LENGTH;
          else state_r <= (state_r == L_LOW) ? L_HIGH : L_LOW;
        end
      endcase
    end
  end : serialize
  //! The length determines byte termination; this flag independently marks
  //! the corresponding final 16-bit record word and has no bus consumer here.
  wire unused_record_last_w = rec_last_w;
endmodule

`default_nettype wire

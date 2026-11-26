/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_usbnet_tx_arb.sv
  Description : The best-effort injection point of the USB network path
                (#1011), at the MAC core's transmit input, after the
                datapath's own store-and-forward FIFO.
                STRICT PRIORITY, WHOLE FRAMES. The datapath (hi) carries
                every SR class frame and every frame of the device's own
                control plane; it wins every arbitration. An injected frame
                (lo) is granted only when no datapath frame is waiting and
                none is still in the MAC between this point and the PHY. The
                datapath frame that arrives just after a grant waits for that
                one injected frame, the one lower-priority frame IEEE
                802.1Q-2018 Annex L and IEEE 802.1BA-2011 6.5 already budget
                as interference; no second injected frame can be queued ahead
                of it, because the next grant again needs the MAC empty of
                datapath frames and no datapath frame waiting.
                THE FRAME-END ACCOUNT. The MAC flips a toggle on the last
                octet of every frame it hands its PHY; the AECP REBOOT
                sequence (KL_reboot_ctrl) counts the datapath's frames out
                with it. An injected frame must not count, or a reboot could
                cut a datapath frame still in the MAC. This block therefore
                produces that toggle: it announces each grant across to the
                transmit clock (a toggle request), and the PHY-side frame end
                that answers the request is the injected frame - the only
                frame in the MAC since the grant - and is not counted. Every
                other frame end flips txend_tgl_o. The same toggle, crossed
                back, counts the datapath frames out of the MAC.
                RESETS. txend_tgl_o is reset-less, as the toggle it replaces
                (a reset that flipped it would count a frame that never
                left). While the transmit side is in reset its frames are
                gone, so an outstanding request is answered there. A reset of
                this clock's side alone leaves at most one request
                outstanding; its answer then masks one datapath frame end,
                which only lengthens the reboot wait to its bound.
  Spec refs   : #1011; IEEE 802.1Q-2018 8.6.8 (strict priority), Annex L;
                IEEE 802.1BA-2011 6.5; IEEE 1722.1-2021 7.4.43;
                docs/design/USB_NET_PATH.md, docs/design/REBOOT_RESET.md
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//
`default_nettype none

module KL_usbnet_tx_arb #(
  parameter int unsigned PW_P = 72,   //! payload bits beside valid/ready/last
  parameter int unsigned OUT_W_P = 6  //! datapath frames the MAC can hold, log2
)(
  input  wire              clk_i,   //! the system clock, the MAC wrapper's
  input  wire              rst_ni,   //! synchronous reset, active low
  //! the datapath
  input  wire              hi_valid_i,
  output logic             hi_ready_o,
  input  wire              hi_last_i,
  input  wire [PW_P-1:0]   hi_data_i,
  //! the computer's frames
  input  wire              lo_valid_i,
  output logic             lo_ready_o,
  input  wire              lo_last_i,
  input  wire [PW_P-1:0]   lo_data_i,
  //! the MAC core
  output logic             m_valid_o,
  input  wire              m_ready_i,
  output logic             m_last_o,
  output logic [PW_P-1:0]  m_data_o,
  input  wire              inject_en_i,
  //! the MAC's transmit clock: one pulse per frame end at the PHY
  input  wire              eth_clk_i,
  input  wire              eth_rst_ni,
  input  wire              eth_end_i,
  output logic             txend_tgl_o,     //! datapath frames only
  //! observation
  output logic             lo_active_o,     //! an injected frame owns the MAC
  output logic [15:0]      injected_o   //! frames injected, saturating
);
  typedef enum logic [1:0] {A_IDLE, A_HI, A_LO, A_WAIT} astate_e;
  astate_e            ast_r;
  logic               req_r;
  logic [OUT_W_P-1:0] out_r;          //! datapath frames between here and the PHY
  (* ASYNC_REG = "TRUE" *) logic [2:0] end_sync_r;
  (* ASYNC_REG = "TRUE" *) logic [1:0] ack_sync_r;
  logic               ack_r;          //! eth domain
  (* ASYNC_REG = "TRUE" *) logic [1:0] req_sync_r;  //! eth domain
  logic               tgl_r = 1'b0;   //! eth domain, reset-less

  wire hi_beat_w  = hi_valid_i && hi_ready_o;
  wire lo_beat_w  = lo_valid_i && lo_ready_o;
  wire dp_out_w   = end_sync_r[2] ^ end_sync_r[1];   //! a datapath frame left
  wire answered_w = ack_sync_r[1] == req_r;
  wire grant_lo_w = (ast_r == A_IDLE) && !hi_valid_i && lo_valid_i && inject_en_i
                 && (out_r == '0) && answered_w;

  always_comb begin : route
    hi_ready_o = 1'b0;
    lo_ready_o = 1'b0;
    m_valid_o  = 1'b0;
    m_last_o   = 1'b0;
    m_data_o   = hi_data_i;
    case (ast_r)
      A_IDLE, A_HI: begin
        //! the datapath goes straight through from idle: no added clock
        m_valid_o  = hi_valid_i;
        hi_ready_o = m_ready_i;
        m_last_o   = hi_last_i;
      end
      A_LO: begin
        m_valid_o  = lo_valid_i;
        lo_ready_o = m_ready_i;
        m_last_o   = lo_last_i;
        m_data_o   = lo_data_i;
      end
      default: ;   //! A_WAIT: the injected frame is in the MAC; hold
    endcase
  end : route

  always_ff @(posedge clk_i) begin : arb
    if (!rst_ni) begin
      ast_r       <= A_IDLE;
      req_r       <= 1'b0;
      out_r       <= '0;
      end_sync_r  <= '0;
      ack_sync_r  <= '0;
      injected_o  <= '0;
    end else begin
      end_sync_r <= {end_sync_r[1:0], tgl_r};
      ack_sync_r <= {ack_sync_r[0], ack_r};
      //! the count of datapath frames in the MAC, saturating both ways
      if (hi_beat_w && hi_last_i && !dp_out_w) begin
        if (out_r != '1) out_r <= out_r + 1'b1;
      end else if (dp_out_w && !(hi_beat_w && hi_last_i)) begin
        if (out_r != '0) out_r <= out_r - 1'b1;
      end
      case (ast_r)
        A_IDLE: begin
          if (hi_beat_w && !hi_last_i) begin
            ast_r <= A_HI;
          end else if (grant_lo_w) begin
            ast_r <= A_LO;
            req_r <= ~req_r;   //! announce: the next frame end is this one
          end
        end
        A_HI: if (hi_beat_w && hi_last_i) ast_r <= A_IDLE;
        A_LO: if (lo_beat_w && lo_last_i) begin
          ast_r <= A_WAIT;
          if (injected_o != '1) injected_o <= injected_o + 1'b1;
        end
        A_WAIT: if (answered_w) ast_r <= A_IDLE;
        default: ast_r <= A_IDLE;
      endcase
    end
  end : arb

  assign lo_active_o = (ast_r == A_LO) || (ast_r == A_WAIT);

  //! the transmit clock's side
  always_ff @(posedge eth_clk_i) begin : eth_req
    req_sync_r <= {req_sync_r[0], req_r};
  end : eth_req

  always_ff @(posedge eth_clk_i) begin : eth_side
    if (!eth_rst_ni) begin
      ack_r <= req_sync_r[1];
    end else if (eth_end_i) begin
      if (ack_r != req_sync_r[1]) ack_r <= req_sync_r[1];
      else                        tgl_r <= ~tgl_r;
    end
  end : eth_side

  assign txend_tgl_o = tgl_r;

endmodule

`default_nettype wire

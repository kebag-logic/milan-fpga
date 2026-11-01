/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_reboot_ctrl.sv
  Description : THE END-STATION RESET ON AN AECP REBOOT (issue #787). The
                protocol processor answers a controller's REBOOT of ENTITY 0
                with SUCCESS (IEEE 1722.1-2021 7.4.43), sends its
                notifications and, where advertising, ENTITY_DEPARTING
                (Milan v1.2 5.6.3.3). Once the last frame it started has
                left its own transmit face it holds reboot_req_i (processor
                #203). This block turns that level into a configuration
                reload from flash: the same configuration a power-on runs,
                so the fabric, the CPU, the MMCMs and the gPTP timestamping
                path all start as from a cold boot
                (docs/design/REBOOT_RESET.md, the (b) decision).

                FOUR PHASES, one millisecond counter.
                  DRAIN  the saved state settles. The phase ends when no
                         live writer exists (nvm_backed_i = 0) or nothing
                         accepted is outside a slot (nvm_dirty_i = 0 and
                         nvm_pend_i = 0), or after T_DRAIN_MS_P. A commit in
                         flight therefore completes, and one that does not
                         complete in time is abandoned exactly where a cold
                         cut would leave it: the A/B journal keeps the
                         previous slot (SAVED_STATE_FASTCONNECT.md 7).
                  EGRESS the frames already given to the MAC reach the PHY.
                         When the processor raises its request, its last
                         frame is still in the parent's egress path: the
                         packer's last beat, the MAC's clock crossing and
                         store-and-forward FIFO, the LiteEth core and the
                         PHY stage. A PHY reset there drops it, and with it
                         ENTITY_DEPARTING (Milan v1.2 5.6.3.5.8, 5.6.3.5.11).
                         The phase ends on a millisecond tick once no frame
                         is half taken at the MAC port and none the port
                         handed over is still in the MAC, and the path has
                         stayed that way since the previous tick: a whole
                         quiet millisecond after the last frame left the
                         MAC's PHY interface covers the PHY's own transmit
                         path. A MAC that never finishes ends it after
                         T_EGRESS_MS_C. The port is not stopped: no gate may
                         sit between the MAC-boundary arbiter and the MAC
                         handshake (the gPTP plane's direct path, #187), and
                         every frame the REBOOT owes the network was handed
                         over before the request. A frame other sources
                         start later is waited for while the path still
                         empties, and is lost with the reset after that, as
                         at a cut.
                  HOLD   phy_hold_o rises and stays up until the
                         reconfiguration takes the pins away, so the PHY is
                         held in reset and the link drops as after a cut.
                         The phase lasts T_HOLD_MS_P, at least the media's
                         worst-case sector erase, so a flash operation
                         started before it has finished before the
                         configuration logic reads the flash.
                  IPROG  eight words on the ICAPE2 X32 port, one per clock:
                         dummy, sync, NOOP, write WBSTAR, 0 (the bitstream's
                         flash offset), write CMD, IPROG, NOOP. Each word
                         leaves with the bits of every byte reversed, the
                         ICAPE2 data-bus order. The sequence repeats after
                         every further T_HOLD_MS_P for as long as the device
                         is still running.

                THE EGRESS ACCOUNT runs from reset, because a frame in the
                MAC when the request rises was handed over before it. The
                port's own handshake counts each frame in on its last beat;
                the MAC flips mac_txend_tgl_i on the last octet of every
                frame it hands its PHY (a reset-less toggle, synchronised
                here like the link guard's), which counts it out. A frame
                the MAC never sends (its internal loopback, or a reset of
                one side only) leaves the count high, and the wait then ends
                at its bound: the count can only make the wait longer, never
                shorter. While the link guard holds the MAC's whole transmit
                side in reset (mac_flush_i) every frame it held is gone, and
                the count is cleared.

                THE BOUND. From reboot_req_i to the IPROG word: at most
                T_DRAIN_MS_P + T_EGRESS_MS_C + T_HOLD_MS_P + 3 ms + 8 clocks
                (one tick of each wait is the tick phase; the sampling and
                the IPROG word's place in the sequence add the clocks).

                VENDOR-NEUTRAL. Nothing here names a primitive: the SoC
                instantiates ICAPE2 on icap_csib_o / icap_i_o with RDWRB
                tied to write, and drives the PHY reset from phy_hold_o.

  Spec refs   : IEEE 1722.1-2021 7.4.43; Milan v1.2 5.6.3.3, 5.6.3.5.8,
                5.6.3.5.11; IEEE 802.3-2022 3.2.1, 3.2.2, 4.4.2 (Table 4-2);
                docs/design/REBOOT_RESET.md;
                docs/design/SAVED_STATE_FASTCONNECT.md sections 7, 9.2 and 9.4
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_reboot_ctrl #(
  //! the longest the saved state may take to settle, in milliseconds: the
  //! producer debounce (500 ms) and the writer debounce (1,000 ms) before a
  //! commit, plus T-NVM-COMMIT-TIMEOUT (8,000 ms) for the commit itself
  //! (SAVED_STATE_FASTCONNECT.md 9.4), rounded up
  parameter int unsigned T_DRAIN_MS_P = 10_000,
  //! how long the PHY is held in reset before each IPROG, in milliseconds:
  //! the media's worst-case 64 KiB sector erase, tSE(max) 3,000 ms
  //! (SAVED_STATE_FASTCONNECT.md 9.4), plus the margin the writer's own
  //! erase wait carries; far above the PHY's minimum reset pulse
  parameter int unsigned T_HOLD_MS_P  = 3_500,
  //! the most octets of line time the MAC can still owe when the egress
  //! wait starts: every buffer from the MAC port to the PHY interface, each
  //! frame those buffers can hold with its preamble, start delimiter,
  //! padding, FCS and inter-frame gap, and one maximum frame already being
  //! sent. The SoC states it from the depths its FIFOs are built with
  //! (sw/litex/milan_soc.py, _mac_tx_egress_octets)
  parameter int unsigned MAC_TX_OCTETS_P = 32_768,
  //! the slowest line rate that MAC runs at, in Mbps
  parameter int unsigned MAC_MIN_MBPS_P  = 10
) (
  input  wire        clk_i,          //! the datapath clock (axis_clk)
  input  wire        rst_n,          //! synchronous active-low reset
  input  wire        ms_tick_i,      //! one-cycle pulse per millisecond

  //! the processor's REBOOT request: a level, held until reset (#203). Any
  //! cycle it reads 1 starts the reset; nothing later can cancel it
  input  wire        reboot_req_i,
  //! KL_nvm_backend's published status (SAVED_STATE_FASTCONNECT.md 9.1)
  input  wire        nvm_backed_i,   //! a writer answered within its deadline
  input  wire        nvm_dirty_i,    //! committable image work no slot holds
  input  wire        nvm_pend_i,     //! accepted work not yet committable

  //! the datapath's MAC port: a beat is taken
  input  wire        mac_tx_beat_i,
  input  wire        mac_tx_frame_i, //! ...and it is a frame's last
  //! ASYNCHRONOUS: the MAC flips it on the last octet of every frame it
  //! hands its PHY. Frames end at least 84 octet times apart (IEEE 802.3
  //! minFrameSize, preamble, start delimiter and gap), 672 ns at 1 Gb/s
  input  wire        mac_txend_tgl_i,
  //! the link guard holds the MAC's whole transmit side in reset
  input  wire        mac_flush_i,

  //! hold the PHY in reset: rises when the egress wait ends, held until reset
  output logic       phy_hold_o,
  //! ICAPE2 CSIB, active low: 0 for exactly the eight IPROG clocks
  output logic       icap_csib_o,
  //! ICAPE2 I[31:0]: the IPROG word of this clock, bits of each byte
  //! reversed; the dummy word whenever icap_csib_o is 1
  output logic [31:0] icap_i_o
);

  typedef enum logic [2:0] {
    S_IDLE   = 3'd0,
    S_DRAIN  = 3'd1,
    S_EGRESS = 3'd2,
    S_HOLD   = 3'd3,
    S_IPROG  = 3'd4
  } state_e;

  //! octets of line time a frame occupies beyond the bytes the MAC buffers:
  //! padding up to minFrameSize less its FCS (60), the FCS (4), preamble and
  //! start delimiter (8) and interPacketGap (12) (IEEE 802.3-2022 3.2.1,
  //! 3.2.2, Table 4-2)
  localparam int unsigned FRAME_OVERHEAD_OCTETS_C = 60 + 4 + 8 + 12;
  //! THE EGRESS BOUND, derived: the time to send MAC_TX_OCTETS_P at
  //! MAC_MIN_MBPS_P, rounded up to whole milliseconds (a Mb/s is 1,000 bits
  //! per millisecond), plus the quiet millisecond the wait ends on
  localparam int unsigned BITS_PER_MS_C  = MAC_MIN_MBPS_P * 1000;
  localparam int unsigned T_SEND_MS_C    = (MAC_TX_OCTETS_P * 8 + BITS_PER_MS_C - 1)
                                           / BITS_PER_MS_C;
  localparam int unsigned T_EGRESS_MS_C  = T_SEND_MS_C + 1;
  //! every frame occupies at least FRAME_OVERHEAD_OCTETS_C of line time, so
  //! the MAC can never owe more frames than this; the count saturates there
  localparam int unsigned FLY_MAX_C      = MAC_TX_OCTETS_P / FRAME_OVERHEAD_OCTETS_C + 1;
  localparam int unsigned FLY_W_C        = $clog2(FLY_MAX_C + 1);

  //! the millisecond counter covers the longest of the three waits
  localparam int unsigned T_DH_MS_C  = (T_DRAIN_MS_P > T_HOLD_MS_P) ? T_DRAIN_MS_P : T_HOLD_MS_P;
  localparam int unsigned T_MAX_MS_C = (T_DH_MS_C > T_EGRESS_MS_C) ? T_DH_MS_C : T_EGRESS_MS_C;
  localparam int unsigned MS_W_C     = $clog2(T_MAX_MS_C + 1);

  if (T_HOLD_MS_P < 1 || T_DRAIN_MS_P < 1) begin : g_refuse_waits
    $error("KL_reboot_ctrl: T_DRAIN_MS_P=%0d and T_HOLD_MS_P=%0d must both be at least 1 ms.",
           T_DRAIN_MS_P, T_HOLD_MS_P);
  end
  //! one maximum frame on the line is the least any MAC can owe: an
  //! envelope frame (maxEnvelopeFrameSize 2,000 octets) with its preamble,
  //! start delimiter and gap (IEEE 802.3-2022 Table 4-2)
  if (MAC_MIN_MBPS_P < 1 || MAC_TX_OCTETS_P < 2_020) begin : g_refuse_egress
    $error("KL_reboot_ctrl: MAC_MIN_MBPS_P=%0d must be at least 1 and MAC_TX_OCTETS_P=%0d at least one maximum frame on the line (2,020 octets).",
           MAC_MIN_MBPS_P, MAC_TX_OCTETS_P);
  end

  //! the IPROG sequence of the 7-series configuration interface, written as
  //! the configuration words (type-1 packet headers: write = 0x3000_0000 |
  //! register << 13 | word count; WBSTAR is register 0b10000, CMD 0b00100,
  //! IPROG is command 0b01111)
  function automatic logic [31:0] iprog_word_f(input logic [2:0] idx);
    case (idx)
      3'd0:    iprog_word_f = 32'hFFFF_FFFF;  // dummy word
      3'd1:    iprog_word_f = 32'hAA99_5566;  // sync word
      3'd2:    iprog_word_f = 32'h2000_0000;  // type-1 NOOP
      3'd3:    iprog_word_f = 32'h3002_0001;  // type-1 write, 1 word, WBSTAR
      3'd4:    iprog_word_f = 32'h0000_0000;  // WBSTAR: the bitstream at flash offset 0
      3'd5:    iprog_word_f = 32'h3000_8001;  // type-1 write, 1 word, CMD
      3'd6:    iprog_word_f = 32'h0000_000F;  // IPROG
      default: iprog_word_f = 32'h2000_0000;  // type-1 NOOP
    endcase
  endfunction

  //! ICAPE2 takes each byte with its bits reversed (D0 is the MSB of a byte)
  function automatic logic [31:0] byte_swap_bits_f(input logic [31:0] w);
    for (int b = 0; b < 4; b++)
      for (int i = 0; i < 8; i++)
        byte_swap_bits_f[8*b + i] = w[8*b + 7 - i];
  endfunction

  state_e             state_r;
  logic [MS_W_C-1:0]  ms_r;
  logic [2:0]         idx_r;
  logic               hold_r;
  logic               quiet_r;    //! the egress path has been empty since the last tick
  logic               in_frame_r; //! the port has taken a frame's first beat, not its last
  logic [FLY_W_C-1:0] fly_r;      //! frames handed to the MAC and not yet at its PHY
  logic [2:0]         txend_sync_r;
  logic               drained_w, idle_w, txend_w, took_w;
  logic               drain_exp_w, egress_exp_w, hold_exp_w;

  //! durable, or nobody left to make it durable (SAVED_STATE_FASTCONNECT.md
  //! 9.3: backed 1 with dirty 0 and pend 0 is the durable row)
  assign drained_w    = ~nvm_backed_i | (~nvm_dirty_i & ~nvm_pend_i);
  //! a frame's last octet reached the PHY: one edge of the synchronised toggle
  assign txend_w      = txend_sync_r[2] ^ txend_sync_r[1];
  //! the port handed the MAC a whole frame
  assign took_w       = mac_tx_beat_i & mac_tx_frame_i;
  //! nothing on its way to the PHY: no frame half taken, none in the MAC
  assign idle_w       = ~in_frame_r & (fly_r == '0);
  //! a wait expires on the tick past its bound, so it never ends early
  assign drain_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P));
  assign egress_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_EGRESS_MS_C));
  assign hold_exp_w   = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P));

  always_ff @(posedge clk_i) begin : egress_account
    if (!rst_n) begin
      txend_sync_r <= '0;
      in_frame_r   <= 1'b0;
      fly_r        <= '0;
    end else begin
      txend_sync_r <= {txend_sync_r[1:0], mac_txend_tgl_i};
      if (mac_tx_beat_i) in_frame_r <= ~mac_tx_frame_i;
      //! saturating both ways: a count above the truth only lengthens the
      //! wait to its bound, and an edge with nothing counted (the first
      //! clocks after a reset) must not wrap it
      if (mac_flush_i)
        fly_r <= '0;
      else if (took_w && !txend_w && fly_r != FLY_W_C'(FLY_MAX_C))
        fly_r <= fly_r + 1'b1;
      else if (txend_w && !took_w && fly_r != '0)
        fly_r <= fly_r - 1'b1;
    end
  end : egress_account

  always_ff @(posedge clk_i) begin : seq
    if (!rst_n) begin
      state_r <= S_IDLE;
      ms_r    <= '0;
      idx_r   <= '0;
      hold_r  <= 1'b0;
      quiet_r <= 1'b0;
    end else begin
      case (state_r)
        S_IDLE: begin
          ms_r <= '0;
          if (reboot_req_i) state_r <= S_DRAIN;
        end
        S_DRAIN: begin
          if (drained_w || drain_exp_w) begin
            state_r <= S_EGRESS;
            ms_r    <= '0;
            quiet_r <= 1'b0;
          end else if (ms_tick_i) begin
            ms_r <= ms_r + 1'b1;
          end
        end
        S_EGRESS: begin
          //! empty at the last tick, on every clock since, and at this one
          if ((ms_tick_i && quiet_r && idle_w) || egress_exp_w) begin
            state_r <= S_HOLD;
            ms_r    <= '0;
            hold_r  <= 1'b1;
          end else if (ms_tick_i) begin
            ms_r    <= ms_r + 1'b1;
            quiet_r <= idle_w;
          end else if (!idle_w) begin
            quiet_r <= 1'b0;
          end
        end
        S_HOLD: begin
          if (hold_exp_w) begin
            state_r <= S_IPROG;
            ms_r    <= '0;
          end else if (ms_tick_i) begin
            ms_r <= ms_r + 1'b1;
          end
        end
        S_IPROG: begin  // one word per clock, then hold again
          idx_r <= idx_r + 1'b1;
          if (idx_r == 3'd7) state_r <= S_HOLD;
        end
        //! no other encoding is reachable; the held request restarts the
        //! sequence, and hold_r stays as it is
        default: state_r <= S_IDLE;
      endcase
    end
  end : seq

  assign phy_hold_o    = hold_r;
  assign icap_csib_o   = (state_r != S_IPROG);
  //! idx_r rests at 0 outside S_IPROG, whose word is the dummy word
  assign icap_i_o      = byte_swap_bits_f(iprog_word_f(idx_r));

endmodule : KL_reboot_ctrl

`default_nettype wire

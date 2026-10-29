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
                (Milan v1.2 5.6.3.3), and then holds reboot_req_i (processor
                #203). This block turns that level into a configuration
                reload from flash: the same configuration a power-on runs,
                so the fabric, the CPU, the MMCMs and the gPTP timestamping
                path all start as from a cold boot
                (docs/design/REBOOT_RESET.md, the (b) decision).

                THREE PHASES, one millisecond counter.
                  DRAIN  the saved state settles. The phase ends when no
                         live writer exists (nvm_backed_i = 0) or nothing
                         accepted is outside a slot (nvm_dirty_i = 0 and
                         nvm_pend_i = 0), or after T_DRAIN_MS_P. A commit in
                         flight therefore completes, and one that does not
                         complete in time is abandoned exactly where a cold
                         cut would leave it: the A/B journal keeps the
                         previous slot (SAVED_STATE_FASTCONNECT.md 7).
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

                THE BOUND. From reboot_req_i to the IPROG word: at most
                T_DRAIN_MS_P + T_HOLD_MS_P + 2 ms + 8 clocks (one tick of
                each wait is the tick phase; the sampling adds a clock).

                VENDOR-NEUTRAL. Nothing here names a primitive: the SoC
                instantiates ICAPE2 on icap_csib_o / icap_i_o with RDWRB
                tied to write, and drives the PHY reset from phy_hold_o.

  Spec refs   : IEEE 1722.1-2021 7.4.43; Milan v1.2 5.6.3.3;
                docs/design/REBOOT_RESET.md; docs/design/SAVED_STATE_FASTCONNECT.md
                sections 7, 9.2 and 9.4
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
  parameter int unsigned T_HOLD_MS_P  = 3_500
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

  //! hold the PHY in reset: rises when the drain ends, held until reset
  output logic       phy_hold_o,
  //! ICAPE2 CSIB, active low: 0 for exactly the eight IPROG clocks
  output logic       icap_csib_o,
  //! ICAPE2 I[31:0]: the IPROG word of this clock, bits of each byte
  //! reversed; the dummy word whenever icap_csib_o is 1
  output logic [31:0] icap_i_o
);

  typedef enum logic [1:0] {
    S_IDLE  = 2'd0,
    S_DRAIN = 2'd1,
    S_HOLD  = 2'd2,
    S_IPROG = 2'd3
  } state_e;

  //! the millisecond counter covers the longer of the two waits
  localparam int unsigned T_MAX_MS_C = (T_DRAIN_MS_P > T_HOLD_MS_P) ? T_DRAIN_MS_P : T_HOLD_MS_P;
  localparam int unsigned MS_W_C     = $clog2(T_MAX_MS_C + 1);

  if (T_HOLD_MS_P < 1 || T_DRAIN_MS_P < 1) begin : g_refuse_waits
    $error("KL_reboot_ctrl: T_DRAIN_MS_P=%0d and T_HOLD_MS_P=%0d must both be at least 1 ms.",
           T_DRAIN_MS_P, T_HOLD_MS_P);
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

  state_e            state_r;
  logic [MS_W_C-1:0] ms_r;
  logic [2:0]        idx_r;
  logic              hold_r;
  logic              drained_w, drain_exp_w, hold_exp_w;

  //! durable, or nobody left to make it durable (SAVED_STATE_FASTCONNECT.md
  //! 9.3: backed 1 with dirty 0 and pend 0 is the durable row)
  assign drained_w   = ~nvm_backed_i | (~nvm_dirty_i & ~nvm_pend_i);
  //! a wait expires on the tick past its bound, so it never ends early
  assign drain_exp_w = ms_tick_i & (ms_r == MS_W_C'(T_DRAIN_MS_P));
  assign hold_exp_w  = ms_tick_i & (ms_r == MS_W_C'(T_HOLD_MS_P));

  always_ff @(posedge clk_i) begin : seq
    if (!rst_n) begin
      state_r <= S_IDLE;
      ms_r    <= '0;
      idx_r   <= '0;
      hold_r  <= 1'b0;
    end else begin
      case (state_r)
        S_IDLE: begin
          ms_r <= '0;
          if (reboot_req_i) state_r <= S_DRAIN;
        end
        S_DRAIN: begin
          if (drained_w || drain_exp_w) begin
            state_r <= S_HOLD;
            ms_r    <= '0;
            hold_r  <= 1'b1;
          end else if (ms_tick_i) begin
            ms_r <= ms_r + 1'b1;
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
        default: begin  // S_IPROG: one word per clock, then hold again
          idx_r <= idx_r + 1'b1;
          if (idx_r == 3'd7) state_r <= S_HOLD;
        end
      endcase
    end
  end : seq

  assign phy_hold_o  = hold_r;
  assign icap_csib_o = (state_r != S_IPROG);
  //! idx_r rests at 0 outside S_IPROG, whose word is the dummy word
  assign icap_i_o    = byte_swap_bits_f(iprog_word_f(idx_r));

endmodule : KL_reboot_ctrl

`default_nettype wire

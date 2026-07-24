/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_link_guard.sv
  Description : L1/L2 link-bounce supervisor. The eth_tx/eth_rx clock
                domains ride PHY-provided clocks (GMII: both from RXC;
                MII: TX_CLK/RX_CLK), so a link bounce stops or glitches
                them and the MAC's sys<->eth CDC halves desync - the
                silicon-proven "TX wedge until reload" (2026-07-19).
                The proven recovery is holding the MAC's sys side in
                reset (LINK_CTRL[1] -> macsys) across the outage and
                releasing it once the eth clocks are stable again; until
                now a software daemon did that in 5-20 s.

                This block does it in hardware: each eth domain exports a
                divide-by-2 toggle (plain FF, flips every cycle). The
                toggles are synchronized here and their transition rate
                is watched; no transition for DEAD_CYC_C sys cycles
                (41 us at 100 MHz - the slowest legal eth clock, MII 10M
                2.5 MHz, transitions every 800 ns) declares the clock
                dead. Any death asserts reinit_o immediately and holds
                it until BOTH clocks have run glitch-free for
                SETTLE_CYC_C (~21 ms), riding through the PHY's clock
                wobble during renegotiation. Recovery is then automatic
                and sub-50-ms with zero software involvement; the
                LINK_CTRL[1] manual strobe remains OR-ed in as the
                daemon-level fallback.

                link_est_o = "eth RX clock alive" - the first hardware
                link truth on boards whose MDIO is unusable (Arty
                MII-PMOD); it feeds eff_link (ADP/AVB_INTERFACE
                counters) as a veto on the daemon-maintained sw_link.

                eth_rst_o completes the CDC story in RTL (gaps 5: the
                sys-side reinit alone was a workaround - the ETH-side
                CDC halves kept their pointers unless software also
                strobed phy_crg_reset). It is the sequenced eth-domain
                CDC reset request: asserted with reinit_o on clock
                death, held through HOLD and the FIRST half of SETTLE
                (so both eth clocks apply it for >=SETTLE/2 clean
                cycles - the SoC turns it into a per-eth-domain
                synchronized reset), then released mid-settle while the
                sys side is STILL held. Release order is therefore
                always eth-first-then-sys: when reinit_o finally drops,
                both CDC halves have restarted from matched (zero)
                pointers and no software strobe is needed. The manual
                LINK_CTRL[1] path stays sys-only (the daemon owns
                phy_crg_reset in that flow).

                stat_o packs {bounce_cnt, flags, state} for the
                LINKG_STAT CSR; freeze_i is a CSR test hook that fakes
                clock death (full FSM drill on silicon without touching
                the cable).

  Spec refs   : docs/MILAN_COMPLIANCE_GAPS.md 5 (GMII link-bounce CDC
                desync); milan_soc.py MilanNIC reinit note (2026-07-19)
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_link_guard #(
  parameter int unsigned DEAD_CYC_C   = 4096,     //! no-transition -> dead
  parameter int unsigned SETTLE_CYC_C = 2097152   //! clean-clock hold (~21 ms)
) (
  input  wire        clk_i,          //! sys clock (always running)
  input  wire        rst_n,          //! sys reset, active low

  //! async divide-by-2 toggles from the eth clock domains (plain FFs)
  input  wire        rx_tgl_i,       //! flips every eth_rx cycle
  input  wire        tx_tgl_i,       //! flips every eth_tx cycle
  input  wire        act_tgl_i,      //! flips per received frame (activity)

  input  wire        dis_i,          //! LINK_CTRL[2]: 1 = guard disabled
  input  wire        freeze_i,       //! LINK_CTRL[3]: test - fake clock death
  input  wire        man_reinit_i,   //! LINK_CTRL[1]: manual MAC reinit

  output wire        reinit_o,       //! hold the MAC sys side in reset
  output wire        eth_rst_o,      //! sequenced eth-side CDC reset request
                                     //! (released mid-settle, before reinit_o)
  output wire        link_est_o,     //! hardware link estimate (rx alive)
  output wire [31:0] stat_o          //! LINKG_STAT readback
);

  // ------------------------------------------------------------------ //
  // Toggle synchronizers + transition detect                            //
  // ------------------------------------------------------------------ //
  logic [2:0] rx_sync_r, tx_sync_r, act_sync_r;
  logic       man_reinit_r;   //! delay FF for the manual-reinit rising edge

  always_ff @(posedge clk_i) begin : sync_ffs
    rx_sync_r    <= {rx_sync_r[1:0],  rx_tgl_i};
    tx_sync_r    <= {tx_sync_r[1:0],  tx_tgl_i};
    act_sync_r   <= {act_sync_r[1:0], act_tgl_i};
    man_reinit_r <= man_reinit_i;
  end : sync_ffs

  wire rx_trans_w  = (rx_sync_r[2]  ^ rx_sync_r[1])  && !freeze_i;
  wire tx_trans_w  = (tx_sync_r[2]  ^ tx_sync_r[1])  && !freeze_i;
  wire act_trans_w = (act_sync_r[2] ^ act_sync_r[1]);

  //! Manual reinit (LINK_CTRL[1]) rising edge -> drives the SAME sequenced
  //! eth+sys recovery as a clock-death event. Without this the manual path was
  //! sys-only (reinit_o) and could NOT clear an eth-side CDC desync that occurred
  //! while the eth clocks stayed ALIVE - a warm reconfigure, or a switch bounce
  //! whose RXC never fully dropped below the death threshold. The guard then sits
  //! in RUN_S (both clocks alive -> no auto trigger) and linkmon's reinit resets
  //! only the sys side, so the MAC wedges until a gateware reload despite repeated
  //! reinit strobes. Routing it through the FSM applies eth_rst for >=SETTLE/2
  //! clean eth cycles and releases eth-first-then-sys -> both CDC pointer sets
  //! restart matched. (The daemon no longer needs to also strobe phy_crg_reset.)
  wire man_edge_w  = man_reinit_i && !man_reinit_r;

  // ------------------------------------------------------------------ //
  // Per-clock liveness (dead = no transition for DEAD_CYC_C)            //
  // ------------------------------------------------------------------ //
  localparam int unsigned DEADW_C = $clog2(DEAD_CYC_C + 1);

  //! arm-on-first-transition: until a clock has EVER ticked it is treated
  //! as alive (matches the historical "link assumed up" boot behavior and
  //! keeps PHY-less TB/top instantiations inert with tied-off toggles)
  logic [DEADW_C-1:0] rx_dead_r, tx_dead_r;
  logic               rx_alive_r, tx_alive_r;
  logic               rx_armed_r, tx_armed_r;

  always_ff @(posedge clk_i) begin : liveness
    if (!rst_n) begin
      rx_dead_r  <= '0;
      tx_dead_r  <= '0;
      rx_alive_r <= 1'b1;
      tx_alive_r <= 1'b1;
      rx_armed_r <= 1'b0;
      tx_armed_r <= 1'b0;
    end
    else begin
      if (rx_trans_w) rx_armed_r <= 1'b1;
      if (tx_trans_w) tx_armed_r <= 1'b1;

      if (rx_trans_w)                             rx_dead_r <= '0;
      else if (rx_dead_r != DEADW_C'(DEAD_CYC_C)) rx_dead_r <= rx_dead_r + 1'b1;
      rx_alive_r <= !rx_armed_r || (rx_dead_r != DEADW_C'(DEAD_CYC_C)) || rx_trans_w;

      if (tx_trans_w)                             tx_dead_r <= '0;
      else if (tx_dead_r != DEADW_C'(DEAD_CYC_C)) tx_dead_r <= tx_dead_r + 1'b1;
      tx_alive_r <= !tx_armed_r || (tx_dead_r != DEADW_C'(DEAD_CYC_C)) || tx_trans_w;
    end
  end : liveness

  //! RX activity seen within the last ~1.3 s (status/diagnostics only)
  logic [26:0] act_age_r;
  wire         act_recent_w = (act_age_r != '1);

  always_ff @(posedge clk_i) begin : act_age
    if (!rst_n)           act_age_r <= '1;
    else if (act_trans_w) act_age_r <= '0;
    else if (!act_recent_w) ;
    else                  act_age_r <= act_age_r + 1'b1;
  end : act_age

  // ------------------------------------------------------------------ //
  // Guard FSM: RUN -> (clock death) HOLD -> (clocks back) SETTLE -> RUN //
  // ------------------------------------------------------------------ //
  typedef enum logic [1:0] {
    RUN_S,       //! clocks alive, reinit released
    HOLD_S,      //! a clock is dead: hold the MAC sys side in reset
    SETTLE_S     //! clocks back: keep holding for SETTLE_CYC_C clean cycles
  } state_t;

  localparam int unsigned SETW_C = $clog2(SETTLE_CYC_C + 1);
  //! eth-side CDC reset release point: half-way through SETTLE. Both eth
  //! clocks are alive from SETTLE entry, so the eth halves see at least
  //! SETTLE_CYC_C/2 clean clocked reset cycles before the release, and the
  //! sys side stays held for the remaining half -> release order is always
  //! eth-first-then-sys and both pointer sets restart matched.
  localparam int unsigned ETH_REL_CYC_C = SETTLE_CYC_C / 2;

  state_t             state_r;
  logic [SETW_C-1:0]  settle_r;
  logic [15:0]        bounce_cnt_r;
  logic               guard_rst_r;
  logic               eth_rst_r;
  logic               bounced_r;   //! this episode already counted a cable bounce

  wire both_alive_w = rx_alive_r && tx_alive_r;

  always_ff @(posedge clk_i) begin : guard_fsm
    if (!rst_n) begin
      state_r      <= RUN_S;
      settle_r     <= '0;
      bounce_cnt_r <= '0;
      guard_rst_r  <= 1'b0;
      eth_rst_r    <= 1'b0;
      bounced_r    <= 1'b0;
    end
    else if (dis_i) begin
      state_r     <= RUN_S;
      guard_rst_r <= 1'b0;
      eth_rst_r   <= 1'b0;
      bounced_r   <= 1'b0;
    end
    else begin
      unique case (state_r)
        RUN_S : begin
          guard_rst_r <= 1'b0;
          eth_rst_r   <= 1'b0;
          //! trigger on clock death OR a manual reinit edge - both run the full
          //! sequenced eth-then-sys CDC reset (manual reinit is no longer sys-only)
          if (!both_alive_w || man_edge_w) begin
            state_r      <= HOLD_S;
            guard_rst_r  <= 1'b1;
            eth_rst_r    <= 1'b1;
            //! count only genuine physical link bounces (clock death), not
            //! software-requested reinits, so LINKG_STAT.bounce_cnt stays a
            //! true cable-event counter
            if (!both_alive_w) begin
              bounced_r    <= 1'b1;
              bounce_cnt_r <= (&bounce_cnt_r) ? bounce_cnt_r
                                              : bounce_cnt_r + 16'd1;
            end
            else begin
              bounced_r    <= 1'b0;   //! manual-triggered episode - no bounce yet
            end
          end
        end

        HOLD_S : begin
          guard_rst_r <= 1'b1;
          eth_rst_r   <= 1'b1;
          //! a real clock death arriving during a manual-triggered hold IS a
          //! cable bounce - count it once (bounced_r guards mid-episode re-deaths)
          if (!both_alive_w && !bounced_r) begin
            bounced_r    <= 1'b1;
            bounce_cnt_r <= (&bounce_cnt_r) ? bounce_cnt_r
                                            : bounce_cnt_r + 16'd1;
          end
          if (both_alive_w) begin
            state_r  <= SETTLE_S;
            settle_r <= '0;
          end
        end

        SETTLE_S : begin
          guard_rst_r <= 1'b1;
          if (!both_alive_w) begin
            state_r   <= HOLD_S;
            eth_rst_r <= 1'b1;               //! re-death: re-arm the eth reset
          end
          else if (settle_r == SETW_C'(SETTLE_CYC_C)) begin
            state_r     <= RUN_S;
            guard_rst_r <= 1'b0;
            bounced_r   <= 1'b0;   //! episode done - re-arm bounce counting
          end
          else begin
            settle_r <= settle_r + 1'b1;
            //! sequenced release: eth side first, mid-settle
            if (settle_r == SETW_C'(ETH_REL_CYC_C)) eth_rst_r <= 1'b0;
          end
        end

        default : state_r <= RUN_S;
      endcase
    end
  end : guard_fsm

  assign reinit_o   = guard_rst_r || man_reinit_i;
  assign eth_rst_o  = eth_rst_r;
  assign link_est_o = rx_alive_r;

  assign stat_o = {bounce_cnt_r,                       // [31:16]
                   6'b0,                               // [15:10]
                   freeze_i, dis_i,                    // [9:8]
                   act_recent_w,                       // [7]
                   guard_rst_r,                        // [6]
                   2'(state_r),                        // [5:4]
                   1'b0, eth_rst_r,                    // [3:2]
                   tx_alive_r, rx_alive_r};            // [1:0]

endmodule

`default_nettype wire

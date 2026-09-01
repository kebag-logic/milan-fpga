/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_pair_blend.sv
  Author      : Kebag Logic

  Date        : 2026-07-28
  Description : Two-source capture pair-stream blend (HANDOVER 8.3b, the Arty
                audio shape): merges the stereo I2S front-end's single pair
                with a TDM master front-end's S/2 pairs into ONE
                {slot, L, R} stream on the shared packetizer contract.

                SLOT MAP - USER 2026-07-28: "channels 1/2 stay the I2S
                Pmod". The I2S pair is pair slot 0, so talker 0's first two
                channels remain the CS5343/CS4344 analog loop exercised as
                test-device channels 1/2, and the TDM pairs follow:

                    out slot 0            <- I2S pair (implicit slot 0)
                    out slot 1 + k        <- TDM pair k, k = 0..S/2-1

                Total supply = 1 + S/2 pair slots. The packetizer's prefix
                sum is unchanged - this module only widens what feeds it.

                COLLISION RULE. Both front-ends run at 48 kHz off the same
                audio MMCM but with unrelated phase, so two strobes can land
                on one clk_i cycle. The TDM strobe passes through; the I2S
                pair is held in a one-deep register and emitted on the next
                strobe-free cycle. Strobes are microseconds apart at 48 kHz
                and clk_i is tens of MHz, so the hold drains the very next
                cycle; a second I2S strobe cannot arrive while one is held
                (that would need a 1-cycle 48 kHz period). If the impossible
                happens anyway the FRESH sample wins - a stale sample is the
                only thing worth less than a dropped one.

                pairs_merged_o counts OUTPUT strobes: it is the physical
                pair supply the fabric captured (A_AAF_PAIRS 0x664), and the
                8.3b silicon acceptance number - 5 pairs x 48 kHz ~=
                240,000/s on the Arty TDM8+I2S build. Synthetic zero-fill
                pairs (KL_pair_zero_fill, downstream) are deliberately NOT
                in this count: the counter is an instrument for the physical
                front-ends, and a filled silence slot must not read as a
                captured one (methodology R5).

  Spec refs   : IEEE 1722-2016 7.3.3 (channels_per_frame the pairs feed);
                Milan v1.2 5.3.7.3 via KL_pair_zero_fill downstream
  Company     : Kebag Logic
------------------------------------------------------------------------------
*/

//! Capture pair-stream blend: I2S pair at slot 0, TDM pairs at slots 1..S/2.
//! Same {pair_valid, pair_slot, L, R} contract in, same out.

`default_nettype none

module KL_pair_blend #(
  parameter int unsigned TDM_SLOTS_P = 8  //! TDM slots of the second source
                                          //! (pairs = TDM_SLOTS_P/2)
)(
  input  wire         clk_i,              //! datapath clock
  input  wire         rst_n,              //! active-low synchronous reset

  // ---- I2S front-end pair (KL_aaf_capture_i2s: implicit slot 0) --------
  input  wire         i2s_pair_valid_i,   //! one-cycle strobe
  input  wire [23:0]  i2s_pair_l_i,
  input  wire [23:0]  i2s_pair_r_i,

  // ---- TDM master front-end pairs (KL_tdm_capture_master) --------------
  input  wire         tdm_pair_valid_i,   //! one-cycle strobe
  input  wire [3:0]   tdm_pair_slot_i,    //! pair index 0..TDM_SLOTS_P/2-1
  input  wire [23:0]  tdm_pair_l_i,
  input  wire [23:0]  tdm_pair_r_i,

  // ---- merged pair stream out ------------------------------------------
  output logic        pair_valid_o,       //! one-cycle strobe
  output logic [3:0]  pair_slot_o,        //! 0 = I2S, 1+k = TDM pair k
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  // ---- status ----------------------------------------------------------
  output logic [31:0] pairs_merged_o      //! output strobes (physical pairs)
);

  localparam int unsigned TDM_PAIRS_C = TDM_SLOTS_P / 2;

  //! The merged slot space must stay inside the 4-bit pair-slot bus the
  //! capture path carries (16 slots): 1 + S/2 <= 16. TDM32 + I2S would need
  //! 17 and is refused - the blend is the Arty TDM8 shape, and a wider one
  //! must widen the capture slot bus first, deliberately.
  if (TDM_SLOTS_P < 2 || TDM_SLOTS_P % 2 != 0 || (1 + TDM_PAIRS_C) > 16)
    $error("KL_pair_blend: TDM_SLOTS_P=%0d needs 1 + %0d merged pair slots, which does not fit the 4-bit capture pair-slot bus (16). The blend ships as I2S + TDM8; widen the pair-slot bus before asking for more.",
           TDM_SLOTS_P, TDM_SLOTS_P / 2);

  //! one-deep I2S hold for the same-cycle collision (see banner)
  logic        i2s_held_r;
  logic [23:0] i2s_hold_l_r, i2s_hold_r_r;

  //! this cycle's winner (TDM passes, held/fresh I2S fills the gaps)
  logic        emit_i2s_c;
  always_comb begin : blend_pick
    emit_i2s_c = ~tdm_pair_valid_i & (i2s_pair_valid_i | i2s_held_r);
    pair_valid_o = tdm_pair_valid_i | emit_i2s_c;
    if (tdm_pair_valid_i) begin
      pair_slot_o = 4'd1 + tdm_pair_slot_i;
      pair_l_o    = tdm_pair_l_i;
      pair_r_o    = tdm_pair_r_i;
    end else begin
      pair_slot_o = 4'd0;
      //! a fresh I2S strobe outranks the held copy (fresh sample wins)
      pair_l_o    = i2s_pair_valid_i ? i2s_pair_l_i : i2s_hold_l_r;
      pair_r_o    = i2s_pair_valid_i ? i2s_pair_r_i : i2s_hold_r_r;
    end
  end : blend_pick

  always_ff @(posedge clk_i) begin : blend_hold
    if (!rst_n) begin
      i2s_held_r   <= 1'b0;
      i2s_hold_l_r <= 24'd0;
      i2s_hold_r_r <= 24'd0;
      pairs_merged_o <= 32'd0;
    end else begin
      if (i2s_pair_valid_i & tdm_pair_valid_i) begin : g_collide
        //! collision: park the I2S pair for the next free cycle
        i2s_held_r   <= 1'b1;
        i2s_hold_l_r <= i2s_pair_l_i;
        i2s_hold_r_r <= i2s_pair_r_i;
      end else if (emit_i2s_c) begin
        i2s_held_r <= 1'b0;
      end
      if (pair_valid_o)
        pairs_merged_o <= pairs_merged_o + 32'd1;
    end
  end : blend_hold

endmodule

`default_nettype wire

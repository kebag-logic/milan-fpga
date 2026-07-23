/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_eth_tx_reset_model.sv
  Description : Clock-stop model of the GMII PHY-side eth_tx register stage,
                built to prove the AX42 reset-scope fix (extend KL_link_guard's
                sequenced eth_rst to cover the PHY TX path, not only the MAC
                CDC halves).

                Root cause it models: on GMII 1G the LiteEthPHYGMIICRG drives
                BOTH eth_rx and eth_tx BUFGs from clock_pads.rx (the PHY RXC).
                A link bounce that stops RXC therefore stops the eth_tx domain
                too, freezing (a) the reset_less pads.tx_en/tx_data launch
                registers and (b) the gtx clock-forward. On RXC return the
                framing/pointer state is stale = the silicon "TX wedge until
                reload". The daemon-only phy_crg_reset used to be the sole
                thing that re-inited that PHY-side state; eth_rst never reached
                it.

                This module carries the two register classes of that stage:
                  * tx_data_r  - a RESET_LESS data register (mirrors
                    LiteEthPHYGMIITX pads.tx_data.reset_less): no reset, holds
                    its last value while the clock is stopped, and is NOT
                    touched by the eth reset.
                  * beat_ptr_r - a RESET-COVERED framing pointer (representative
                    of the sink.valid framing the MAC drives into this stage):
                    free-runs 0..FRAME_LEN_C-1 each eth_tx clock; the reset
                    forces it back to the frame boundary (0) - the common
                    re-sync point the rest of the system (held in reinit)
                    shares. desync_err_r latches (sticky) if a true system
                    frame boundary (frame_start_i) ever lands while the pointer
                    is off-boundary = a persistent misframe / TX-wedge witness.

                The reset input models migen's AsyncResetSynchronizer exactly:
                async-ASSERT (fires even while the eth_tx clock is stopped, via
                the arst_src_w edge) and sync-RELEASE (deasserts only on the
                running clock, two stages). arst_src_w = por_rst_i | ext_rst_i
                mirrors the SoC's `reset | ext_reset` OR into the synchronizer.

                HOUSE-STYLE DEVIATION (intentional, documented): this model uses
                ASYNCHRONOUS active-high resets rather than the project's
                synchronous active-low rst_n. That is the whole subject under
                test - a synchronous reset could not assert while the clock is
                stopped, which is precisely the property the AX42 fix relies on.
                All other conventions (banner, default_nettype, //! port docs,
                _r/_w suffixes, named blocks, 2-space) are kept.

  Spec refs   : liteeth/phy/gmii.py (LiteEthPHYGMIICRG / LiteEthPHYGMIITX);
                milan_soc.py MilanNIC eth_rst wiring; hdl/common/KL_link_guard.sv
                (eth_rst_o producer); docs/findings/HANDOVER.md AX42
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_eth_tx_reset_model #(
  parameter int unsigned FRAME_LEN_C = 6   //! beats/frame = free-run framing period
) (
  input  wire       eth_tx_clk_i,   //! eth_tx clock - TB can STOP and restart it
  input  wire       por_rst_i,      //! power-on async reset (models the base PHY CRG reset)
  input  wire       ext_rst_i,      //! extended eth_rst request (async-assert / sync-release)
  input  wire       frame_start_i,  //! true system frame-boundary marker (never-stopping timeline)
  input  wire [7:0] data_i,         //! TX payload byte source

  output wire [7:0] tx_data_o,      //! reset_less TX data register (holds through a clock stop)
  output wire       tx_en_o,        //! frame active (1 = mid-frame beat)
  output wire [3:0] beat_ptr_o,     //! reset-covered framing pointer - the desync witness
  output wire       idle_o,         //! 1 = pointer at frame boundary (beat 0)
  output wire       desync_err_o    //! STICKY: a frame_start landed while off-boundary (misframe)
);

  localparam logic [3:0] LAST_BEAT_C = 4'(FRAME_LEN_C - 1);

  // ------------------------------------------------------------------ //
  // AsyncResetSynchronizer model: async-assert, sync-release            //
  // (arst_src_w = por | ext  -> two-stage synchronizer -> dom_rst_w)    //
  // ------------------------------------------------------------------ //
  wire arst_src_w = por_rst_i | ext_rst_i;   //! matches SoC `reset | ext_reset`

  // rst_sync_r is deliberately flopped BOTH async (assert path) and sync
  // (release shift) - that IS an AsyncResetSynchronizer. SYNCASYNCNET flags the
  // dual usage; here it is the intended, standard reset-synchronizer topology.
  /* verilator lint_off SYNCASYNCNET */
  logic [1:0] rst_sync_r;

  always_ff @(posedge eth_tx_clk_i or posedge arst_src_w) begin : arst_sync
    if (arst_src_w) rst_sync_r <= 2'b11;     //! async assert (no clock needed)
    else            rst_sync_r <= {rst_sync_r[0], 1'b0};   //! sync release (2 clocks)
  end : arst_sync
  /* verilator lint_on SYNCASYNCNET */

  wire dom_rst_w = rst_sync_r[1];   //! the per-eth-domain synchronized reset

  // ------------------------------------------------------------------ //
  // Reset-covered framing pointer (the CDC/framing state that desyncs)  //
  // ------------------------------------------------------------------ //
  logic [3:0] beat_ptr_r;

  always_ff @(posedge eth_tx_clk_i or posedge dom_rst_w) begin : framing
    if (dom_rst_w)                          beat_ptr_r <= 4'd0;   //! re-sync to boundary
    else if (beat_ptr_r == LAST_BEAT_C)     beat_ptr_r <= 4'd0;
    else                                    beat_ptr_r <= beat_ptr_r + 4'd1;
  end : framing

  // ------------------------------------------------------------------ //
  // Sticky misframe witness: a true boundary (frame_start_i) arriving   //
  // while the pointer is off-boundary means the eth stream is framed at //
  // the wrong phase vs the system = the persistent TX wedge. The eth    //
  // reset clears it because it re-syncs the pointer to the boundary.    //
  // ------------------------------------------------------------------ //
  logic desync_err_r;

  always_ff @(posedge eth_tx_clk_i or posedge dom_rst_w) begin : desync_latch
    if (dom_rst_w)                                       desync_err_r <= 1'b0;
    else if (frame_start_i && (beat_ptr_r != 4'd0))      desync_err_r <= 1'b1;
  end : desync_latch

  // ------------------------------------------------------------------ //
  // reset_less TX data register (mirrors pads.tx_data.reset_less): NOT  //
  // in any reset, simply holds its last clocked value across a stop and //
  // is intentionally untouched by the eth reset.                        //
  // ------------------------------------------------------------------ //
  logic [7:0] tx_data_r;

  always_ff @(posedge eth_tx_clk_i) begin : tx_data_ff
    tx_data_r <= data_i;
  end : tx_data_ff

  assign tx_data_o    = tx_data_r;
  assign tx_en_o      = (beat_ptr_r != 4'd0);
  assign beat_ptr_o   = beat_ptr_r;
  assign idle_o       = (beat_ptr_r == 4'd0);
  assign desync_err_o = desync_err_r;

endmodule

`default_nettype wire

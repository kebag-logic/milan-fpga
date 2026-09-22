/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : pp_adp_pkg.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/04, 08 §2)
//
//  Description : ADP engine constants — the F04.5 ADPDU geometry (68-byte
//                PDU behind a 14-byte Ethernet header = 82 wire bytes,
//                cdl = 56), the F04.6 entity_capabilities constant, the
//                Milan Δ5 fixed valid_time/T-ADP-ADV pair, and the two
//                DISTINCT KL_pp_prng draw kinds for T-ADP-DELAY-START vs
//                T-ADP-DELAY (review §8 item 5: a merged draw is a known
//                conformance-bug class — the kinds are separate named
//                constants so a merge is a visible diff, never a typo).
//
//                Values are stated ONCE here; KL_adp_engine derives, never
//                mirrors (F08.1 owns the timer values, F04.6 the caps mask).
//---------------------------------------------------------------------------//
`default_nettype none

package pp_adp_pkg;

  // ---- ADP message types (IEEE 1722.1-2021 Table 6-1; 04 §3) -------------
  localparam logic [3:0] ADP_MSG_AVAILABLE_C = 4'd0;
  localparam logic [3:0] ADP_MSG_DEPARTING_C = 4'd1;
  localparam logic [3:0] ADP_MSG_DISCOVER_C  = 4'd2;

  // ---- F04.5 frame geometry ----------------------------------------------
  // 14-byte Ethernet header (DA + SA + EtherType) + 68-byte ADPDU; the
  // builder emits the full wire frame, so entity_id lands at wire byte 18
  // (PDU offset 4 per F04.5), byte-exact.
  localparam int unsigned ADP_FRAME_BYTES_C = 82;
  localparam int unsigned ADP_ETH_HDR_BYTES_C = 14;
  localparam logic [10:0] ADP_CDL_C = 11'd56;

  // ---- addressing (03 §8) ------------------------------------------------
  localparam logic [47:0] ADP_MCAST_DA_C   = 48'h91E0_F001_0000;
  localparam logic [15:0] ADP_ETHERTYPE_C  = 16'h22F0;
  localparam logic [7:0]  ADP_SUBTYPE_C    = 8'hFA;

  // ---- Milan Δ5 constants (04 §3 sourcing table; F08.1) ------------------
  //! valid_time = 10 (2-s units => 20 s validity); 0 in DEPARTING/DISCOVER
  localparam logic [4:0]  ADP_VALID_TIME_C = 5'd10;
  //! T-ADP-ADV: 5 s fixed re-advertise cadence
  localparam logic [31:0] ADP_T_ADV_MS_C   = 32'd5000;

  // ---- F04.6 entity_capabilities (hex-mask column is authoritative) ------
  // AEM_SUPPORTED 0x08 | VENDOR_UNIQUE 0x80 | CLASS_A 0x100 | GPTP 0x400
  // | AEM_IDENTIFY_CONTROL_INDEX_VALID 0x4000 | AEM_INTERFACE_INDEX_VALID
  // 0x8000; every other flag 0 (incl. EFU_MODE, GAP-13).
  localparam logic [31:0] ADP_ENTITY_CAPS_C = 32'h0000_C588;

  // ---- KL_pp_prng draw kinds (08 §3; review §8 item 5: keep DISTINCT) ----
  localparam logic [2:0] ADP_DRAW_KIND_START_C = 3'd1;  //! T-ADP-DELAY-START 0..2 s
  localparam logic [2:0] ADP_DRAW_KIND_DELAY_C = 3'd2;  //! T-ADP-DELAY 0..4 s

  // ---- advertise SM (F04.2; 04 §5 sizes the arch state at 2 b) -----------
  // DELAY is split into its two real hardware phases: DRAW (waiting on the
  // PRNG rejection sampler) then DELAY (T-ADP-DELAY(-START) armed). Both
  // are the F04.2 "DELAY" state.
  typedef enum logic [1:0] {
    ADP_ADV_DOWN    = 2'd0,
    ADP_ADV_DRAW    = 2'd1,
    ADP_ADV_DELAY   = 2'd2,
    ADP_ADV_WAITING = 2'd3
  } adp_adv_st_e;

  //! received valid_time (2-s units) -> T-ADP-NOADP milliseconds (04 §6.2)
  function automatic logic [31:0] adp_vt_to_ms_f(input logic [4:0] vt);
    return 32'(vt) * 32'd2000;
  endfunction

endpackage : pp_adp_pkg
`default_nettype wire

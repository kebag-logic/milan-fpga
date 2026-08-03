/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aem_patch.sv
//  Project     : Milan saved-state fast-connect — the AEM dynamic-state
//                ingest port (E4)
//                ([`SAVED_STATE_FASTCONNECT.md`](../../../docs/design/SAVED_STATE_FASTCONNECT.md) §10c)
//
//  Description : THE MISSING HALF OF PERSISTENCE. Milan v1.2 puts eleven
//                unconditional persistence SHALLs on a PAAD-AE (§5.3.5.1,
//                5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7,
//                5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13). Every one of them can
//                be READ today. Most of them could not be PUT BACK, because
//                the state lives in KL_aecp_aem_store's RAM and that RAM's
//                write port had exactly one master: KL_aecp_response_builder's
//                SET_* write-back. No CSR reached it, and a self-addressed
//                AECP command cannot reach it either (the parser taps the RX
//                path; a frame the board sends to its own MAC is never
//                forwarded back). This module is that missing master.
//
//                DESCRIPTOR-ADDRESSED, NEVER BYTE-ADDRESSED. Software says
//                {descriptor_type, index, field}; the FABRIC resolves the byte
//                range from the SAME generated tables SET_STREAM_FORMAT uses
//                (WB_STRIN_FMT_ADDR_C / WB_STROUT_FMT_ADDR_C /
//                WB_SAMPLING_RATE_C / WB_CLOCK_SRC_IDX_C in
//                gen/aecp_aem_rom.svh). A byte address in a shell script would
//                be a second copy of a generated constant, and the AEM ROM is
//                regenerated on every config change. A consequence worth
//                stating: this port physically CANNOT write outside a field it
//                knows the name of — the address is a table lookup and the
//                length is a field constant, so no payload can reach an
//                arbitrary byte of the descriptor image.
//
//                VALIDATION IS NOT OPTIONAL AND NOT NEW. The payload runs
//                through the same acceptance the AECP path applies: the Milan
//                5.3.8.1 "shall always be using a format that is one of the
//                supported formats" family test against THIS descriptor's own
//                generated reference (AEM_STRIN_FMT_C / AEM_STROUT_FMT_C /
//                AEM_STRIN_CRF_C), the AEM_RATES_C table for a sampling rate,
//                and the 0..2 source bound for a clock source. Restoring a
//                format the entity does not declare as supported would be a
//                WORSE conformance break than the revert it fixes.
//
//                ORDERING IS STRUCTURAL, NOT CONVENTIONAL. Every CSR write is
//                REFUSED — never queued, never buffered — while the ADP
//                advertiser is enabled (0x600[0]). "Replay before the entity
//                advertises" is therefore enforced by the hardware, not by an
//                init-script convention someone has to remember. A refused
//                write changes nothing and reports VD_ADP_C, so a daemon that
//                gets the order wrong learns it from the status word instead
//                of silently half-restoring a live entity.
//
//                WHAT THIS PORT DELIBERATELY DOES NOT RESTORE. Milan 5.3.4.1
//                and 5.3.4.2 require the OPPOSITE of persistence — the locked
//                state and the registered-controller list are CLEARED by a
//                power cycle. Neither is reachable from here: there is no
//                field code for them and no address table entry, so no future
//                widening of the payload can quietly start restoring one. The
//                absence is the mechanism.
//
//                CSR GROUP (0x7C8-0x7D4, REGISTER_MAP.md; executable spec
//                tb/verilator/aempatch/aempatch_wrap.sv):
//                  0x7C8 AEMP_SEL   W  {desc_type[31:16], index[15:0]}
//                  0x7CC AEMP_FIELD W  [2:0] which field of that descriptor
//                  0x7D0 AEMP_DATA  W  payload words, MSW first
//                  0x7D4 AEMP_CTRL  W1S [0] commit, [1] abort; R: status
//
//                PAYLOAD CONVENTION. AEMP_DATA carries the field payload as a
//                LEFT-ALIGNED big-endian byte stream, exactly as those bytes
//                sit in the descriptor image — the same order the SET_*
//                write-back copies them out of the command buffer. Push
//                ceil(len/4) words, most-significant word first. The word
//                count is checked against the field (VD_LEN_C), so a daemon
//                that pushes the wrong shape is told so rather than writing a
//                truncated field.
//
//  Spec refs   : Milan v1.2 §5.3.5.1, §5.3.7.1, §5.3.8.1, §5.3.11.1 (the
//                clauses this port closes); §5.3.4.1, §5.3.4.2 (the two it
//                must never serve); IEEE Std 1722.1-2021 §7.2, §7.4.9/7.4.22
//  Company     : Kebag Logic
//---------------------------------------------------------------------------//

`default_nettype none

import aecp_pkg::*;

module KL_aem_patch (
    input  wire         clk_i,
    input  wire         rst_n,           //! sync active-low

    //! ADP advertiser enable (0x600[0]). HIGH = the entity is advertising and
    //! every CSR write below is REFUSED. This is the whole ordering contract.
    input  wire         adp_enable_i,

    // ---- host ingest (CSR 0x7C8-0x7D4, one-cycle strobes + one word) -----
    input  wire [31:0]  pat_wdata_i,     //! the word written this cycle
    input  wire         pat_sel_p_i,     //! 1-cycle: AEMP_SEL   written
    input  wire         pat_field_p_i,   //! 1-cycle: AEMP_FIELD written
    input  wire         pat_data_p_i,    //! 1-cycle: AEMP_DATA  written
    input  wire         pat_commit_p_i,  //! 1-cycle: AEMP_CTRL[0] commit
    input  wire         pat_abort_p_i,   //! 1-cycle: AEMP_CTRL[1] abort

    // ---- AEM store patch master (KL_aecp_aem_store pw_* slave) ----------
    //! held until pw_ack_i; the store refuses a cycle the SET_* write-back
    //! is using, so a byte can never be dropped on a collision
    output reg  [15:0]  pw_addr_o,
    output reg          pw_wr_o,
    output reg  [7:0]   pw_data_o,
    input  wire         pw_ack_i,

    // ---- status (CSR 0x7D4 read) ----------------------------------------
    output wire [31:0]  stat_o
);

  `include "gen/aecp_aem_rom.svh"

  // -----------------------------------------------------------------------
  // Field codes. 0/1/2 are the AEM-store-resident fields this port serves.
  // 3 and 4 are REGISTERED HERE AND REFUSED: the presentation-time offset
  // (5.3.7.6) is a KL_aecp_response_builder register array and the non-ENTITY
  // names (5.3.13) need that module's descriptor-name pointer cone, so both
  // want a builder-side slave this lane did not build. Refusing them by NAME
  // (VD_FIELD_C) is the honest answer: a daemon learns the field is not
  // served instead of watching a silent no-op and believing it restored.
  // -----------------------------------------------------------------------
  localparam logic [2:0] FLD_FORMAT_C   = 3'd0;  //! 5.3.8.1 / 5.3.7.1
  localparam logic [2:0] FLD_SAMPRATE_C = 3'd1;  //! 5.3.5.1
  localparam logic [2:0] FLD_CLKSRC_C   = 3'd2;  //! 5.3.11.1
  localparam logic [2:0] FLD_PRESOFF_C  = 3'd3;  //! 5.3.7.6  — not served here
  localparam logic [2:0] FLD_NAME_C     = 3'd4;  //! 5.3.13   — not served here

  //! FSM
  localparam logic [2:0] ST_IDLE_S  = 3'd0;
  localparam logic [2:0] ST_WRITE_S = 3'd1;
  localparam logic [2:0] ST_DONE_S  = 3'd2;

  //! verdicts (stat_o[7:4]) — ordered so the FIRST failing test names itself
  localparam logic [3:0] VD_NONE_C   = 4'd0;  //! nothing attempted since reset
  localparam logic [3:0] VD_ACCEPT_C = 4'd1;  //! validated and written
  localparam logic [3:0] VD_ADP_C    = 4'd2;  //! REFUSED: the entity is advertising
  localparam logic [3:0] VD_DESC_C   = 4'd3;  //! no such descriptor / index
  localparam logic [3:0] VD_FIELD_C  = 4'd4;  //! field not served by this port
  localparam logic [3:0] VD_LEN_C    = 4'd5;  //! wrong AEMP_DATA word count
  localparam logic [3:0] VD_VALUE_C  = 4'd6;  //! payload failed the SET_* acceptance

  // -----------------------------------------------------------------------
  // Staging
  // -----------------------------------------------------------------------
  reg  [15:0] sel_type_r;      //! AEMP_SEL[31:16] descriptor_type
  reg  [15:0] sel_idx_r;       //! AEMP_SEL[15:0]  descriptor_index
  reg  [2:0]  field_r;         //! AEMP_FIELD[2:0]
  reg  [63:0] data_r;          //! payload, left-aligned; SHIFTS OUT on write
  reg  [2:0]  nwords_r;        //! AEMP_DATA words pushed since the last commit
  reg  [2:0]  st_r;
  reg  [3:0]  verdict_r;
  reg         done_r;
  reg  [3:0]  bcnt_r;          //! bytes written in the burst
  reg  [3:0]  blen_r;          //! bytes the accepted field wants
  reg  [3:0]  bdone_r;         //! bytes written by the last ACCEPTED commit

  // -----------------------------------------------------------------------
  // Descriptor resolution — the generated tables, never a retyped address
  // -----------------------------------------------------------------------
  wire w_is_strin  = (sel_type_r == DESC_STREAM_INPUT);
  wire w_is_strout = (sel_type_r == DESC_STREAM_OUTPUT);

  //! the AUDIO_UNIT / CLOCK_DOMAIN singletons the AECP setters address
  wire w_au_ok  = (sel_type_r == DESC_AUDIO_UNIT)  && (sel_idx_r == 16'd0);
  wire w_cd_ok  = (sel_type_r == DESC_CLOCK_DOMAIN) && (sel_idx_r == 16'd0);

`ifdef AEM_PER_STREAM_FMT
  //! index clamped for the constant-array mux; range validity is a separate
  //! test below, exactly the way the response builder splits the two
  wire [3:0] w_in_fidx  = (sel_idx_r < 16'(AEM_N_STRIN_C))  ? sel_idx_r[3:0] : 4'd0;
  wire [3:0] w_out_fidx = (sel_idx_r < 16'(AEM_N_STROUT_C)) ? sel_idx_r[3:0] : 4'd0;

  wire w_strin_ok  = w_is_strin  && (sel_idx_r < 16'(AEM_N_STRIN_C));
  wire w_strout_ok = w_is_strout && (sel_idx_r < 16'(AEM_N_STROUT_C));
`else
  //! LEGACY 1-AAF-INPUT LAYOUT (no `AEM_PER_STREAM_FMT): the shape has one
  //! STREAM_OUTPUT and two STREAM_INPUTs, of which index 1 IS the CRF sink.
  //! Split exactly the way KL_aecp_response_builder splits it, so the two
  //! engines agree on which descriptors exist for every shipped config.
  wire w_strin_ok  = w_is_strin  && (sel_idx_r < 16'd2);
  wire w_strout_ok = w_is_strout && (sel_idx_r == 16'd0);
`endif

  // -----------------------------------------------------------------------
  // Acceptance — the SAME rules the SET_* arms apply, against the SAME
  // generated per-descriptor references. AEM_FMT_BASE_MASK_C lives in
  // aecp_pkg so the two readers cannot drift (a copied constant diverges in
  // silence — docs/limitations/RECURRING_DEFECT_PATTERNS.md).
  // -----------------------------------------------------------------------
  //! LEFT-ALIGN THE PAYLOAD. AEMP_DATA words shift in from the LSB end
  //! ({data_r[31:0], word}), so after two pushes the value already sits
  //! left-aligned but after ONE it sits in the low half. Normalising here —
  //! once, in front of both the acceptance test and the byte writer — is what
  //! lets the software contract stay uniform ("push the field's bytes, MSW
  //! first") instead of asking a daemon to pre-shift a 16-bit clock-source
  //! index into bit 48. The word count is validated against the field, so a
  //! payload can only be one of these two shapes by the time it is used.
  wire [63:0] w_pay        = (nwords_r == 3'd1) ? {data_r[31:0], 32'd0}
                                                : data_r;
  wire [63:0] w_fmt        = w_pay;                     //! 8 bytes, left-aligned
  wire [9:0]  w_fmt_ch     = w_fmt[31:22];
  wire [63:0] w_fmt_chm    = w_fmt & AEM_FMT_BASE_MASK_C;

`ifdef AEM_PER_STREAM_FMT
  //! ONE reference, ONE pair of comparators. The obvious spelling computes
  //! an input verdict and an output verdict side by side and picks one, which
  //! costs two 64-bit reference muxes and two 64-bit compares to use exactly
  //! half of them. Selecting the REFERENCE first and testing once measured
  //! 148 LUTs cheaper in KL_aecp_top (13 344 -> 13 196, yosys OOC on the 8x8
  //! shape), for behaviour the suite cannot tell apart — worth one extra
  //! line of explanation on a device this build is ~2 600 LUTs over.
  //! (Standalone the same change reads +50; the in-context number is the
  //! true one, per syn/yosys/ooc.sh's own note about shared decode.)
  wire [63:0] w_ref = w_is_strout ? AEM_STROUT_FMT_C[w_out_fidx]
                                  : AEM_STRIN_FMT_C[w_in_fidx];

  //! EXACT match for every Stream Output (talker wire truth — declared ==
  //! transmitted) and for a CRF sink; the Milan 6.4 channel-count family
  //! rule for an AAF sink, against THIS descriptor's own base.
  wire w_fmt_exact = w_is_strout || AEM_STRIN_CRF_C[w_in_fidx];
  wire w_fmt_ok    = w_fmt_exact
                   ? (w_fmt == w_ref)
                   : ((w_fmt_ch >= 10'd1) && (w_fmt_ch <= 10'd8) &&
                      !w_fmt[52] &&
                      (w_fmt_chm == (w_ref & AEM_FMT_BASE_MASK_C)));
`else
  //! legacy layout: the AAF family base is AEM_FMTS_C[0], the talker is
  //! hardwired stereo (declared == transmitted), and STREAM_INPUT[1] is CRF
  localparam [63:0] AAF_OUT_FMT_C =
      (AEM_FMTS_C[0] & AEM_FMT_BASE_MASK_C) | (64'd2 << 22);
  wire [63:0] w_ref      = w_is_strout ? AAF_OUT_FMT_C : AEM_CRF_FMTS_C[0];
  wire        w_fmt_exact = w_is_strout || (sel_idx_r == 16'd1);
  wire        w_fmt_ok    = w_fmt_exact
                          ? (w_fmt == w_ref)
                          : ((w_fmt_ch >= 10'd1) && (w_fmt_ch <= 10'd8) &&
                             !w_fmt[52] &&
                             (w_fmt_chm ==
                              (AEM_FMTS_C[0] & AEM_FMT_BASE_MASK_C)));
`endif

  //! sampling rate: the generated advertised list, looped to its own bound
  wire [31:0] w_rate = w_pay[63:32];
  logic       w_rate_ok;
  always_comb begin : rate_accept
    w_rate_ok = 1'b0;
    for (int unsigned ri = 0; ri < AEM_RATES_N_C; ri++)
      if (w_rate == AEM_RATES_C[ri]) w_rate_ok = 1'b1;
  end : rate_accept

  //! clock source: sources 0..2 = Internal / AAF stream / CRF stream
  wire [15:0] w_clksrc    = w_pay[63:48];
  wire        w_clksrc_ok = (w_clksrc < 16'd3);

  // -----------------------------------------------------------------------
  // Commit verdict + the resolved byte range. ONE always_comb so the order of
  // the tests IS the order an operator reads them in: descriptor before
  // field before length before value, so the status word names the first
  // thing that was wrong rather than the last.
  // -----------------------------------------------------------------------
  logic [3:0]  verdict_w;
  logic [15:0] base_w;
  logic [3:0]  len_w;
  always_comb begin : commit_calc
    verdict_w = VD_ACCEPT_C;
    base_w    = 16'd0;
    len_w     = 4'd0;
    unique case (field_r)
      FLD_FORMAT_C: begin
        len_w  = 4'd8;
`ifdef AEM_PER_STREAM_FMT
        base_w = w_is_strout ? WB_STROUT_FMT_ADDR_C[w_out_fidx]
                             : WB_STRIN_FMT_ADDR_C[w_in_fidx];
`else
        base_w = w_is_strout ? WB_STREAM_FORMAT_C
                             : (sel_idx_r == 16'd0) ? WB_STREAM_IN0_FMT_C
                                                    : WB_STREAM_IN1_FMT_C;
`endif
        if      (!(w_strin_ok || w_strout_ok)) verdict_w = VD_DESC_C;
        else if (nwords_r != 3'd2)             verdict_w = VD_LEN_C;
        else if (!w_fmt_ok)                    verdict_w = VD_VALUE_C;
      end
      FLD_SAMPRATE_C: begin
        len_w  = 4'd4;
        base_w = WB_SAMPLING_RATE_C;
        if      (!w_au_ok)         verdict_w = VD_DESC_C;
        else if (nwords_r != 3'd1) verdict_w = VD_LEN_C;
        else if (!w_rate_ok)       verdict_w = VD_VALUE_C;
      end
      FLD_CLKSRC_C: begin
        len_w  = 4'd2;
        base_w = WB_CLOCK_SRC_IDX_C;
        if      (!w_cd_ok)         verdict_w = VD_DESC_C;
        else if (nwords_r != 3'd1) verdict_w = VD_LEN_C;
        else if (!w_clksrc_ok)     verdict_w = VD_VALUE_C;
      end
      //! FLD_PRESOFF_C / FLD_NAME_C and the unassigned codes: named, refused
      default: verdict_w = VD_FIELD_C;
    endcase
  end : commit_calc

  // -----------------------------------------------------------------------
  // Sequencer
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i) begin : patch_seq
    if (!rst_n) begin
      sel_type_r <= 16'd0; sel_idx_r <= 16'd0;
      field_r    <= 3'd0;  data_r    <= 64'd0;
      nwords_r   <= 3'd0;  st_r      <= ST_IDLE_S;
      verdict_r  <= VD_NONE_C; done_r <= 1'b0;
      bcnt_r     <= 4'd0;  blen_r    <= 4'd0; bdone_r <= 4'd0;
      pw_addr_o  <= 16'd0; pw_wr_o   <= 1'b0; pw_data_o <= 8'd0;
    end else if (st_r == ST_WRITE_S) begin
      // ---- the burst is atomic once validated -------------------------
      //! It was accepted while the entity was silent, its length is a field
      //! constant (<= 8 store writes) and it is already validated; finishing
      //! it is bounded and cannot tear a descriptor field, which aborting
      //! mid-way demonstrably would.
      if (pw_ack_i) begin
        data_r <= {data_r[55:0], 8'd0};
        if (bcnt_r == blen_r - 4'd1) begin
          pw_wr_o   <= 1'b0;
          bdone_r   <= blen_r;
          verdict_r <= VD_ACCEPT_C;
          done_r    <= 1'b1;
          st_r      <= ST_DONE_S;
        end else begin
          bcnt_r    <= bcnt_r + 4'd1;
          pw_addr_o <= pw_addr_o + 16'd1;
          pw_data_o <= data_r[55:48];
        end
      end
    end else if (adp_enable_i) begin
      // ---- THE GATE: refuse, never queue ------------------------------
      //! Any of the four registers written while the advertiser is up is
      //! rejected outright: no byte reaches the store and no commit runs.
      //! The PAYLOAD is additionally DROPPED (data_r and the word count), so
      //! a transfer straddling an ADP enable cannot be completed afterwards
      //! with half its words from before the entity went live — it fails
      //! VD_LEN instead. The selection and field registers are deliberately
      //! left alone: they are inert without a payload, and clearing them
      //! would buy nothing while making the refusal harder to read back.
      if (pat_sel_p_i || pat_field_p_i || pat_data_p_i ||
          pat_commit_p_i || pat_abort_p_i) begin
        verdict_r <= VD_ADP_C;
        done_r    <= 1'b1;
        nwords_r  <= 3'd0;
        data_r    <= 64'd0;
      end
    end else if (pat_abort_p_i) begin
      nwords_r  <= 3'd0;
      data_r    <= 64'd0;
      verdict_r <= VD_NONE_C;
      done_r    <= 1'b0;
      st_r      <= ST_IDLE_S;
    end else begin
      if (pat_sel_p_i) begin
        sel_type_r <= pat_wdata_i[31:16];
        sel_idx_r  <= pat_wdata_i[15:0];
      end
      if (pat_field_p_i) field_r <= pat_wdata_i[2:0];
      if (pat_data_p_i) begin
        //! MSW first: the payload lands left-aligned, in descriptor byte order
        data_r   <= {data_r[31:0], pat_wdata_i};
        //! saturate rather than wrap — an overlong push must stay wrong
        if (nwords_r != 3'd7) nwords_r <= nwords_r + 3'd1;
      end
      if (pat_commit_p_i) begin
        verdict_r <= verdict_w;
        done_r    <= 1'b1;
        nwords_r  <= 3'd0;
        if (verdict_w == VD_ACCEPT_C) begin
          pw_wr_o   <= 1'b1;
          pw_addr_o <= base_w;
          //! the writer shifts out of data_r from the top, so it takes the
          //! NORMALISED payload — byte 0 now, the rest as each ack lands
          data_r    <= w_pay;
          pw_data_o <= w_pay[63:56];
          bcnt_r    <= 4'd0;
          blen_r    <= len_w;
          st_r      <= ST_WRITE_S;
        end else begin
          st_r <= ST_DONE_S;
        end
      end
    end
  end : patch_seq

  // -----------------------------------------------------------------------
  // Status word
  //   [2:0]   FSM state         [3]      0
  //   [7:4]   verdict (VD_*)    [11:8]   bytes written by the last ACCEPT
  //   [14:12] words staged      [15]     0
  //   [18:16] field             [19]     ADP gate (1 = writes refused)
  //   [30]    done              [31]     busy
  // -----------------------------------------------------------------------
  wire busy_w = (st_r == ST_WRITE_S);
  assign stat_o = {busy_w, done_r, 10'd0, adp_enable_i, field_r,
                   1'b0, nwords_r, bdone_r, verdict_r, 1'b0, st_r};

endmodule

`default_nettype wire

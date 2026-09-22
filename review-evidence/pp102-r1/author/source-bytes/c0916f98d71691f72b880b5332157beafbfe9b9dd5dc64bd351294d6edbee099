/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_dyn_state.sv
//  Project     : IEEE 1722.1 protocol processor
//                (Milan v1.2 §5.3.5 / §5.3.7 / §5.3.8 / §5.3.11 / §5.3.12 —
//                 the dynamic state a controller may SET and a PAAD-AE must
//                 report back; 06 §8 the µCPU state port)
//
//  Description : THE DYNAMIC-STATE STORE. Every value Milan v1.2 lets a
//                controller change at run time lives here, and nowhere else.
//
//                WHY IT EXISTS. Until VERSION 0x004B every value this entity
//                served came from one of two places: the read-only descriptor
//                image in DRAM, or a live fabric face. Neither can hold a
//                SETTING. The image is read-only at run time by construction
//                (KL_aecp_desc_store drops and counts any write outside its
//                name table) and a fabric face reports what the hardware is
//                doing, not what a controller asked for. So SET_SAMPLING_RATE,
//                SET_CLOCK_SOURCE, SET_STREAM_FORMAT, SET_STREAM_INFO,
//                SET_CONFIGURATION, SET_CONTROL and START/STOP_STREAMING had
//                nowhere to put their argument, and every one of them answered
//                the NOT_IMPLEMENTED echo. This block is the "somewhere".
//
//                THE ADDRESSING, AND WHY IT LOOKS LIKE THIS. The µISA computes
//                a state-port address as `desc_base_r + imm[19:0]`
//                (KL_aecp_ucpu.sv) and `desc_base_r` is invariantly zero in
//                this system, so THE ADDRESS IS AN IMMEDIATE AND NOTHING ELSE
//                — a µprogram cannot index by the descriptor its command
//                names. The way out is the one the gather faces already took:
//
//                  * the ADDRESS selects the FIELD (`st_addr_i[15:3]` = a
//                    SEL_*_C selector below), which a µprogram can name with a
//                    constant, and
//                  * the DESCRIPTOR INDEX arrives on `desc_index_i`, driven by
//                    KL_aecp_engine off the same registered walk field that
//                    already feeds ctr_desc_index_o / gsi_desc_index_o /
//                    amap_desc_index_o.
//
//                REGION 0x1 IS THE VALUE, REGION 0x2 IS THE VALID FLAG, and
//                the pair is what lets a GET fall back to the image: read the
//                flag, branch, take the overlay or the descriptor. The
//                alternative — seeding every row from the image at boot and
//                always reading the overlay — was rejected because it FIGHTS
//                PERSISTENCE: a saved-state restore has to write these rows,
//                and a boot seeder would have to be taught not to overwrite
//                what NVM had already put there. A valid bit composes; a seed
//                has to be sequenced.
//
//                WIDTHS ARE PER FIELD, NOT UNIFORM. A flat array of 64-bit
//                rows would be the obvious shape and it is the wrong one on
//                this die: it costs 2,304 flops at the 8x8 shape against 1,360
//                for the typed arrays below, and only two of the eight fields
//                are actually 64 bits wide. Every array here is exactly as
//                wide as the clause that owns it. The fields are ALSO read
//                continuously by the fabric (the started bits gate the
//                listener, the clock source selects the media clock, the
//                presentation offset feeds the talker), so this is state that
//                has to be flops rather than a memory whichever way it is
//                sliced — the saving is in the width, not the storage class.
//
//                WHAT THIS BLOCK DOES NOT DO. It does not check the lock
//                (CHECK_LOCK does, in the µprogram, before the write), it does
//                not validate a value against the descriptor's supported list
//                (the µprogram does), and it does not persist anything — it
//                raises `dirty_o` so the NVM manager knows a commit is owed.
//                An out-of-range descriptor index is dropped and counted
//                rather than aliased onto row zero, because silently writing
//                the wrong stream's format is worse than refusing.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_dyn_state #(
    //! the shape this processor was elaborated at; the row map below is
    //! derived from these, never hardcoded (07 §3.2's shape law)
    parameter int unsigned N_STREAM_IN_P  = 8,
    parameter int unsigned N_STREAM_OUT_P = 8,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOMAIN_P = 1,
    parameter int unsigned N_CONTROL_P    = 1
) (
    input  wire         clk_i,          //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,          //! synchronous active-low reset

    //! ---- µCPU state port, slave side (06 §8) --------------------------
    //! Same contract as KL_aecp_desc_store's: the request is held until the
    //! answer, a read answers with ONE cycle of `st_rvalid_o`, a write is
    //! taken on `st_ready_o`. The engine gates `st_req_i` by region, so this
    //! block never sees an access that is not its own.
    input  wire         st_req_i,       //! request, held until ready/rvalid
    input  wire         st_we_i,        //! 1 = write
    input  wire  [19:0] st_addr_i,      //! [19:16] region, [15:3] field sel
    input  wire  [63:0] st_wdata_i,     //! write data, right-justified
    output logic        st_ready_o,     //! write accepted this cycle
    output logic        st_rvalid_o,    //! one-cycle read answer
    output logic [63:0] st_rdata_o,     //! read data, right-justified

    //! the descriptor the command in flight names, registered by the engine
    //! one whole state earlier — see the banner
    input  wire  [15:0] desc_index_i,

    //! ---- the live face the fabric reads (07 §4) ------------------------
    output logic [15:0] cur_config_o,      //! ENTITY.current_configuration
    output logic  [7:0] identify_o,        //! the IDENTIFY CONTROL's value
    output logic [15:0] clk_src_index_o,   //! CLOCK_DOMAIN[0].clock_source_index
    //! per-row publication of the three stream-scoped settings, value beside
    //! its valid bit. The banner's design intent made literal: the
    //! presentation offset feeds the talker's per-STREAM_OUTPUT transit
    //! entries and the formats feed the RX acceptance and the served
    //! "current format", so the integrator needs every ROW, continuously -
    //! an indexed view would serve one reader per cycle and the framers are
    //! all readers at once. Values without their valid bit are meaningless:
    //! row k reads zero until a controller writes it, and a consumer that
    //! took the zero would present in the past / accept nothing.
    output logic [N_STREAM_OUT_P*32-1:0] pt_offset_o,   //! row k at [32k +: 32]
    output logic [N_STREAM_OUT_P-1:0]    pt_offset_v_o,
    output logic [N_STREAM_IN_P*64-1:0]  fmt_in_o,      //! row k at [64k +: 64]
    output logic [N_STREAM_IN_P-1:0]     fmt_in_v_o,
    output logic [N_STREAM_OUT_P*64-1:0] fmt_out_o,     //! row k at [64k +: 64]
    output logic [N_STREAM_OUT_P-1:0]    fmt_out_v_o,
    output logic        dirty_o,           //! a persisted field was written

    //! ---- observability -------------------------------------------------
    output logic [15:0] dbg_writes_o,      //! writes accepted
    output logic [15:0] dbg_oob_o          //! writes dropped, index out of range
);

  // ---- the field selectors a µprogram names (gen_ucode.py mirrors these) ---
  localparam int unsigned SEL_CFG_C    = 0;  //! current_configuration
  localparam int unsigned SEL_RATE_C   = 1;  //! current_sampling_rate
  localparam int unsigned SEL_CLKSRC_C = 2;  //! clock_source_index
  localparam int unsigned SEL_FMTIN_C  = 3;  //! current_format, Stream Inputs
  localparam int unsigned SEL_FMTOUT_C = 4;  //! current_format, Stream Outputs
  localparam int unsigned SEL_PTOFF_C  = 5;  //! presentation-time offset
  //! selector 6 was SEL_START_C, started/stopped per Stream Input. RETIRED at
  //! issue #78: Milan §5.3.8.7 makes the state a property of the BINDING ("the
  //! started/stopped state is undefined when the Stream Input is not bound"),
  //! and only the ACMP binding record has that lifecycle — it is cleared on
  //! unbind, captured by KL_acmp_nvm_shadow and restored through `pre_started_i`.
  //! A copy here had the writer and no lifecycle, so the two could disagree
  //! with nothing to say which was right. START/STOP_STREAMING now reach the
  //! record through the engine's write-only request region (0x3); nothing is
  //! stored in this block. The NUMBER is left unused rather than recycled, so a
  //! µprogram still naming selector 6 misses instead of landing on a live field.
  localparam int unsigned SEL_IDENT_C  = 7;  //! the IDENTIFY CONTROL's value

  localparam logic [3:0] RGN_DYN_C  = 4'h1;  //! region: the value
  localparam logic [3:0] RGN_DYNV_C = 4'h2;  //! region: the valid flag

  //! index widths, once. A count of 1 still needs a 1-bit index rather than a
  //! zero-width one, which is what the `> 1` guard buys.
  localparam int unsigned AUW_C = (N_AUDIO_UNIT_P > 1) ? $clog2(N_AUDIO_UNIT_P) : 1;
  localparam int unsigned CDW_C = (N_CLK_DOMAIN_P > 1) ? $clog2(N_CLK_DOMAIN_P) : 1;
  localparam int unsigned SIW_C = (N_STREAM_IN_P  > 1) ? $clog2(N_STREAM_IN_P)  : 1;
  localparam int unsigned SOW_C = (N_STREAM_OUT_P > 1) ? $clog2(N_STREAM_OUT_P) : 1;
  localparam int unsigned CTW_C = (N_CONTROL_P    > 1) ? $clog2(N_CONTROL_P)    : 1;

  //! Milan v1.2 §5.3.5.1 / §5.3.7.1 / §5.3.7.6 / §5.3.8.1 / §5.3.8.7 /
  //! §5.3.11.1 / §5.3.12 — one array per clause, each exactly as wide as its
  //! field. `_v_r` is the "a controller has set this" flag a GET branches on.
  logic [15:0] cfg_r;                      logic                      cfg_v_r;
  logic [31:0] rate_r   [N_AUDIO_UNIT_P];  logic [N_AUDIO_UNIT_P-1:0] rate_v_r;
  //! public_flat_rw: the root-integration true-ratio harness (milan-fpga
  //! tb/verilator/milan_dp sim_aclk) pokes the STORED selection directly to
  //! ask its one question - "given CRF selected, do the two grids align?" -
  //! without re-proving the command path (SET_CLOCK_SOURCE -> this row ->
  //! clk_src_index_o -> the root resolve), which the AECP-FACE arms already
  //! pin end to end. The tap is on the store, one hop upstream of that
  //! proven chain, so no unproven seam hides between poke and product.
  logic [15:0] clksrc_r [N_CLK_DOMAIN_P] /* verilator public_flat_rw */;
  logic [N_CLK_DOMAIN_P-1:0] clksrc_v_r;
  logic [63:0] fmtin_r  [N_STREAM_IN_P];   logic [N_STREAM_IN_P-1:0]  fmtin_v_r;
  logic [63:0] fmtout_r [N_STREAM_OUT_P];  logic [N_STREAM_OUT_P-1:0] fmtout_v_r;
  logic [31:0] ptoff_r  [N_STREAM_OUT_P];  logic [N_STREAM_OUT_P-1:0] ptoff_v_r;
  logic  [7:0] ident_r  [N_CONTROL_P];     logic [N_CONTROL_P-1:0]    ident_v_r;

  logic [15:0] wr_cnt_r, oob_cnt_r;

  // ---- decode -------------------------------------------------------------
  logic  [3:0] region_w;
  logic [12:0] sel_w;
  assign region_w = st_addr_i[19:16];
  assign sel_w    = st_addr_i[15:3];

  //! how many rows each selector owns, so an index past the end is REFUSED
  //! rather than aliased onto another descriptor's setting
  logic [15:0] count_w;
  always_comb begin : sel_count
    unique case (sel_w)
      13'(SEL_CFG_C):    count_w = 16'd1;
      13'(SEL_RATE_C):   count_w = 16'(N_AUDIO_UNIT_P);
      13'(SEL_CLKSRC_C): count_w = 16'(N_CLK_DOMAIN_P);
      13'(SEL_FMTIN_C):  count_w = 16'(N_STREAM_IN_P);
      13'(SEL_FMTOUT_C): count_w = 16'(N_STREAM_OUT_P);
      13'(SEL_PTOFF_C):  count_w = 16'(N_STREAM_OUT_P);
      13'(SEL_IDENT_C):  count_w = 16'(N_CONTROL_P);
      default:           count_w = 16'd0;   // an unmapped selector owns none
    endcase
  end

  logic in_range_w;
  assign in_range_w = (desc_index_i < count_w);

  //! the range-checked index, narrowed once per array. `in_range_w` gates
  //! every use, so a zero-count selector can never reach an array port.
  logic [AUW_C-1:0] au_ix_w;   assign au_ix_w = AUW_C'(desc_index_i);
  logic [CDW_C-1:0] cd_ix_w;   assign cd_ix_w = CDW_C'(desc_index_i);
  logic [SIW_C-1:0] si_ix_w;   assign si_ix_w = SIW_C'(desc_index_i);
  logic [SOW_C-1:0] so_ix_w;   assign so_ix_w = SOW_C'(desc_index_i);
  logic [CTW_C-1:0] ct_ix_w;   assign ct_ix_w = CTW_C'(desc_index_i);

  // ---- read ---------------------------------------------------------------
  logic [63:0] val_w, vld_w;
  always_comb begin : read_mux
    val_w = 64'd0;
    vld_w = 64'd0;
    if (in_range_w) begin
      unique case (sel_w)
        13'(SEL_CFG_C):    begin val_w = {48'd0, cfg_r};
                                 vld_w = {63'd0, cfg_v_r}; end
        13'(SEL_RATE_C):   begin val_w = {32'd0, rate_r[au_ix_w]};
                                 vld_w = {63'd0, rate_v_r[au_ix_w]}; end
        13'(SEL_CLKSRC_C): begin val_w = {48'd0, clksrc_r[cd_ix_w]};
                                 vld_w = {63'd0, clksrc_v_r[cd_ix_w]}; end
        13'(SEL_FMTIN_C):  begin val_w = fmtin_r[si_ix_w];
                                 vld_w = {63'd0, fmtin_v_r[si_ix_w]}; end
        13'(SEL_FMTOUT_C): begin val_w = fmtout_r[so_ix_w];
                                 vld_w = {63'd0, fmtout_v_r[so_ix_w]}; end
        13'(SEL_PTOFF_C):  begin val_w = {32'd0, ptoff_r[so_ix_w]};
                                 vld_w = {63'd0, ptoff_v_r[so_ix_w]}; end
        13'(SEL_IDENT_C):  begin val_w = {56'd0, ident_r[ct_ix_w]};
                                 vld_w = {63'd0, ident_v_r[ct_ix_w]}; end
        default: ;
      endcase
    end
  end

  //! an out-of-range read answers ZERO with the valid flag CLEAR, which sends
  //! the µprogram down its image arm — the honest answer for "this entity has
  //! no such setting", and never an alias of row zero
  logic        rd_pend_r;
  logic [63:0] rd_data_r;
  assign st_rvalid_o = rd_pend_r;
  assign st_rdata_o  = rd_data_r;
  //! a write is taken combinationally: nothing here can back-pressure
  assign st_ready_o  = st_req_i && st_we_i;

  // ---- the state ----------------------------------------------------------
  logic take_wr_w, oob_wr_w;
  assign take_wr_w = st_req_i && st_we_i && (region_w == RGN_DYN_C) && in_range_w;
  assign oob_wr_w  = st_req_i && st_we_i && (region_w == RGN_DYN_C) && !in_range_w;

  always_ff @(posedge clk_i) begin : dyn_core
    if (!rst_n) begin
      cfg_r      <= 16'd0;  cfg_v_r    <= 1'b0;
      rate_v_r   <= '0;
      clksrc_v_r <= '0;
      fmtin_v_r  <= '0;
      fmtout_v_r <= '0;
      ptoff_v_r  <= '0;
      ident_v_r  <= '0;
      rd_pend_r  <= 1'b0;
      rd_data_r  <= 64'd0;
      dirty_o    <= 1'b0;
      wr_cnt_r   <= 16'd0;
      oob_cnt_r  <= 16'd0;
      for (int unsigned i = 0; i < N_AUDIO_UNIT_P; i++) rate_r[i]   <= 32'd0;
      for (int unsigned i = 0; i < N_CLK_DOMAIN_P; i++) clksrc_r[i] <= 16'd0;
      for (int unsigned i = 0; i < N_STREAM_IN_P;  i++) fmtin_r[i]  <= 64'd0;
      for (int unsigned i = 0; i < N_STREAM_OUT_P; i++) fmtout_r[i] <= 64'd0;
      for (int unsigned i = 0; i < N_STREAM_OUT_P; i++) ptoff_r[i]  <= 32'd0;
      //! Milan §5.3.12: "0 = not identifying" IS the reset default, and the
      //! IDENTIFY value is one of the three things §5.3.4 keeps VOLATILE
      for (int unsigned i = 0; i < N_CONTROL_P;    i++) ident_r[i]  <= 8'd0;
    end else begin
      //! the read answer is one cycle behind the request, exactly like the
      //! descriptor store's, so the µCPU's `!st_rvalid_i` stall sees one flop
      rd_pend_r <= st_req_i && !st_we_i;
      rd_data_r <= (region_w == RGN_DYNV_C) ? vld_w : val_w;

      if (oob_wr_w && (oob_cnt_r != 16'hFFFF)) oob_cnt_r <= oob_cnt_r + 16'd1;

      if (take_wr_w) begin
        if (wr_cnt_r != 16'hFFFF) wr_cnt_r <= wr_cnt_r + 16'd1;
        //! §5.3.13 and friends: every field written here is one the PAAD-AE
        //! "shall save in a non-volatile memory and restore after a power
        //! cycle" EXCEPT the IDENTIFY value, so only the persisted set marks
        //! the store dirty. Raising it for IDENTIFY would commit flash on a
        //! front-panel blink.
        if (sel_w != 13'(SEL_IDENT_C)) dirty_o <= 1'b1;
        unique case (sel_w)
          13'(SEL_CFG_C):    begin cfg_r              <= st_wdata_i[15:0];
                                   cfg_v_r            <= 1'b1; end
          13'(SEL_RATE_C):   begin rate_r[au_ix_w]    <= st_wdata_i[31:0];
                                   rate_v_r[au_ix_w]  <= 1'b1; end
          13'(SEL_CLKSRC_C): begin clksrc_r[cd_ix_w]  <= st_wdata_i[15:0];
                                   clksrc_v_r[cd_ix_w]<= 1'b1; end
          13'(SEL_FMTIN_C):  begin fmtin_r[si_ix_w]   <= st_wdata_i;
                                   fmtin_v_r[si_ix_w] <= 1'b1; end
          13'(SEL_FMTOUT_C): begin fmtout_r[so_ix_w]  <= st_wdata_i;
                                   fmtout_v_r[so_ix_w]<= 1'b1; end
          13'(SEL_PTOFF_C):  begin ptoff_r[so_ix_w]   <= st_wdata_i[31:0];
                                   ptoff_v_r[so_ix_w] <= 1'b1; end
          13'(SEL_IDENT_C):  begin ident_r[ct_ix_w]   <= st_wdata_i[7:0];
                                   ident_v_r[ct_ix_w] <= 1'b1; end
          default: ;
        endcase
      end
    end
  end

  // ---- the live face ------------------------------------------------------
  assign cur_config_o    = cfg_r;
  assign identify_o      = ident_r[0];
  assign clk_src_index_o = clksrc_r[0];
  always_comb begin : live_rows
    for (int unsigned i = 0; i < N_STREAM_OUT_P; i++) begin
      pt_offset_o[32*i +: 32] = ptoff_r[i];
      fmt_out_o[64*i +: 64]   = fmtout_r[i];
    end
    for (int unsigned i = 0; i < N_STREAM_IN_P; i++)
      fmt_in_o[64*i +: 64] = fmtin_r[i];
  end
  assign pt_offset_v_o   = ptoff_v_r;
  assign fmt_in_v_o      = fmtin_v_r;
  assign fmt_out_v_o     = fmtout_v_r;
  assign dbg_writes_o    = wr_cnt_r;
  assign dbg_oob_o       = oob_cnt_r;

endmodule

`default_nettype wire

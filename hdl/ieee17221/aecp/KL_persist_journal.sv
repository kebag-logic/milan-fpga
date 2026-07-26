/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_persist_journal.sv
//  Project     : Milan saved-state fast-connect — persistence journal
//                ([`SAVED_STATE_FASTCONNECT.md`](../../../docs/design/SAVED_STATE_FASTCONNECT.md))
//
//  Description : Decoder + boot-time REPLAY MASTER for the non-volatile
//                persistence journal. Software pushes ONE journal slot image
//                (a 32-bit word stream lifted verbatim out of flash) through
//                the host ingest port; this module verifies the whole image
//                and only THEN drives the ACMP bind-restore port
//                (KL_acmp_lstn_ctx rest_*, the E1 group behind CSR
//                0x7A0-0x7B4), one transaction per journal record.
//
//                THE ATOMICITY RULE. Not one rest_req_o is ever raised from
//                an image whose magic / format / shape / length / CRC-32 did
//                not close. A torn flash slot, a truncated transfer or a
//                journal belonging to another entity is REJECTED WHOLE — it
//                can never be half-applied into the listener context table.
//                That is the property this module exists for: it does not
//                depend on a userspace daemon checking anything, and it is
//                what tb/verilator/persist proves.
//
//                WHY IN FABRIC. Software could write 0x7A0-0x7B4 directly,
//                but then "reject rather than half-apply" would be a
//                property of a daemon nobody gates. Here the verdict is
//                structural: the CRC word is the LAST word of the image, so
//                the engine physically cannot have emitted a restore before
//                it has seen and checked it.
//
//                SLOT IMAGE (32-bit LITTLE-ENDIAN words, exactly as stored):
//                  w0  MAGIC     'KLJ1' = 0x314A4C4B (byte 0 = 'K')
//                  w1  FMT_VER   {major[31:16], minor[15:0]}
//                  w2  SEQ       u32 generation counter (wrap-safe compare)
//                  w3  SHAPE     {rsvd[31:16], rec_words[15:8], n_rec[7:0]}
//                  w4  ENT_LO    owning entity_id[31:0]
//                  w5  ENT_HI    owning entity_id[63:32]
//                  then n_rec RECORDS of rec_words (= 6) words each, and
//                  finally ONE CRC-32 trailer word over every preceding
//                  word of the image (CRC-32/ISO-HDLC = `zlib.crc32`).
//
//                RECORD = the six E1 register writes, in register order, so
//                a record IS the CSR transaction it replays:
//                  r0 -> 0x7A0 talker_entity_id[31:0]
//                  r1 -> 0x7A4 talker_entity_id[63:32]
//                  r2 -> 0x7A8 {rsvd[31:28], vlan[27:16], tuid[15:0]}
//                  r3 -> 0x7AC controller_entity_id[31:0]
//                  r4 -> 0x7B0 controller_entity_id[63:32]
//                  r5 -> 0x7B4 {commit[31] added here, VALID[30],
//                               flags[23:8], sink idx[3:0]}
//                VALID[30] = 0 leaves that sink alone (a hole in the table);
//                it is the journal-side bit, never written to 0x7B4.
//
//                SLOT ARBITRATION IS SOFTWARE'S. Two flash slots exist so a
//                torn write can only ever damage the one being written;
//                software reads both, pushes the higher-SEQ one first and
//                falls back to the other if the verdict is a rejection. The
//                engine only enforces MONOTONICITY inside a boot: an image
//                whose SEQ does not beat the last ACCEPTED one is refused
//                (VD_STALE), so a stale slot can never roll a fresh bind
//                back. A rejected image never updates that watermark, so the
//                fall-back push is always allowed.
//
//  Spec refs   : Milan v1.2 §5.5.3.5.2 (saved-state entry record),
//                §5.5.2.6 step 1 (SRP params re-probed, never restored),
//                §5.4 (persistent settings); IEEE Std 1722.1-2021 §8.2.2
//  Company     : Kebag Logic
//---------------------------------------------------------------------------//

`default_nettype none

module KL_persist_journal #(
    //! journal record capacity; MUST be <= 8 (the status refusal bitmap)
    parameter int unsigned MAX_REC_P   = 8,
    //! image magic, little-endian word whose byte 0 is 'K' (hexdump "KLJ1")
    parameter logic [31:0] MAGIC_P     = 32'h314A_4C4B,
    //! accepted format major; a mismatch is rejected, never reinterpreted
    parameter logic [15:0] FMT_MAJOR_P = 16'h0001
) (
    input  wire         clk_i,
    input  wire         rst_n,           //! sync active-low

    //! this station's entity_id — a journal carrying another entity's id is
    //! refused, so a cloned rootfs cannot make board B claim board A's bind
    input  wire [63:0]  entity_id_i,

    // ---- host ingest (CSR 0x7B8/0x7BC, one word per strobe) ------------
    input  wire         jnl_start_i,     //! 1-cycle: begin a new slot image
    input  wire         jnl_wr_i,        //! 1-cycle: jnl_data_i is next word
    input  wire [31:0]  jnl_data_i,      //! flash word, little-endian as read
    input  wire         jnl_end_i,       //! 1-cycle: image complete -> verify
    input  wire         jnl_abort_i,     //! 1-cycle: drop back to idle

    // ---- ACMP bind-restore master (E1; KL_acmp_lstn_ctx rest_* slave) --
    //! req held HIGH until the engine's 1-cycle ack; status valid WITH ack
    output reg          rest_req_o,
    output reg  [3:0]   rest_idx_o,
    output reg  [63:0]  rest_talker_o,
    output reg  [15:0]  rest_tuid_o,
    output reg  [63:0]  rest_ctlr_o,
    output reg  [15:0]  rest_flags_o,
    input  wire         rest_ack_i,
    input  wire [1:0]   rest_status_i,

    // ---- status (CSR 0x7C0/0x7C4) --------------------------------------
    output wire [31:0]  stat_o,          //! see the packing below
    output wire [31:0]  seq_o            //! SEQ of the last ACCEPTED image
);

  // -----------------------------------------------------------------------
  // Shape constants
  // -----------------------------------------------------------------------
  localparam int unsigned HDR_WORDS_C = 6;                     //! w0..w5
  localparam int unsigned REC_WORDS_C = 6;                     //! 0x7A0..0x7B4
  localparam int unsigned RAM_WORDS_C = MAX_REC_P * REC_WORDS_C;
  localparam int unsigned RAM_AW_C    = (RAM_WORDS_C > 1) ? $clog2(RAM_WORDS_C) : 1;

  //! FSM
  localparam logic [2:0] ST_IDLE_S   = 3'd0;
  localparam logic [2:0] ST_LOAD_S   = 3'd1;
  localparam logic [2:0] ST_VERIFY_S = 3'd2;
  localparam logic [2:0] ST_FETCH_S  = 3'd3;
  localparam logic [2:0] ST_ARM_S    = 3'd4;
  localparam logic [2:0] ST_WAIT_S   = 3'd5;
  localparam logic [2:0] ST_DONE_S   = 3'd6;

  //! verdicts (stat_o[7:4]) — ordered so the FIRST failing structural test
  //! names itself; nothing here is acted on before VD_CRC has passed
  localparam logic [3:0] VD_NONE_C   = 4'd0;   //! no verdict since reset/start
  localparam logic [3:0] VD_ACCEPT_C = 4'd1;   //! verified and replayed
  localparam logic [3:0] VD_MAGIC_C  = 4'd2;   //! not a journal slot (or erased)
  localparam logic [3:0] VD_VER_C    = 4'd3;   //! format major this build cannot read
  localparam logic [3:0] VD_SHAPE_C  = 4'd4;   //! rec_words != 6, n_rec 0 or > MAX_REC_P
  localparam logic [3:0] VD_LEN_C    = 4'd5;   //! truncated or overlong transfer
  localparam logic [3:0] VD_CRC_C    = 4'd6;   //! TORN WRITE / bit rot
  localparam logic [3:0] VD_ENT_C    = 4'd7;   //! journal belongs to another entity
  localparam logic [3:0] VD_STALE_C  = 4'd8;   //! SEQ does not beat the accepted one

  // -----------------------------------------------------------------------
  // CRC-32/ISO-HDLC — reflected poly 0xEDB88320, init 0xFFFF_FFFF, final XOR
  // 0xFFFF_FFFF. Byte-serial steps over the LITTLE-ENDIAN word so the fabric
  // digest is bit-for-bit `zlib.crc32` over the flash byte stream: the
  // journal writer and this reader can never disagree about what was covered.
  // -----------------------------------------------------------------------
  function automatic logic [31:0] crc32_byte_f(input logic [31:0] crc_in,
                                               input logic [7:0]  d_in);
    logic [31:0] c;
    begin
      c = crc_in ^ {24'h00_0000, d_in};
      for (int unsigned b = 0; b < 8; b++) begin
        c = c[0] ? ((c >> 1) ^ 32'hEDB8_8320) : (c >> 1);
      end
      crc32_byte_f = c;
    end
  endfunction

  function automatic logic [31:0] crc32_word_f(input logic [31:0] crc_in,
                                               input logic [31:0] w_in);
    logic [31:0] c;
    begin
      c = crc32_byte_f(crc_in, w_in[7:0]);
      c = crc32_byte_f(c,      w_in[15:8]);
      c = crc32_byte_f(c,      w_in[23:16]);
      c = crc32_byte_f(c,      w_in[31:24]);
      crc32_word_f = c;
    end
  endfunction

  // -----------------------------------------------------------------------
  // Record staging RAM: sync-only write, ONE async read port (house RAM
  // rule, same shape as the ACMP context table). Only the six REPLAYED
  // words of a record are stored; everything on the wire is still folded
  // into the CRC, so a future longer record cannot be silently truncated
  // (rec_words != 6 is VD_SHAPE, never a partial parse).
  // -----------------------------------------------------------------------
  reg  [31:0]           rec_ram_r [0:RAM_WORDS_C-1];
  logic [RAM_AW_C-1:0]  rd_addr_w;
  wire  [31:0]          rd_q_w = rec_ram_r[rd_addr_w];

  // -----------------------------------------------------------------------
  // Load state
  // -----------------------------------------------------------------------
  reg  [2:0]  st_r;
  reg  [3:0]  verdict_r;
  reg  [31:0] crc_r;            //! running digest (pre final XOR)
  reg  [31:0] crc_rx_r;         //! trailer word as read from the image
  reg  [15:0] wcnt_r;           //! words consumed since jnl_start_i
  reg  [31:0] h_magic_r, h_ver_r, h_seq_r, h_ent_lo_r, h_ent_hi_r;
  reg  [7:0]  n_rec_r;          //! SHAPE[7:0]
  reg  [7:0]  rec_w_r;          //! SHAPE[15:8]
  reg         shape_bad_r;      //! latched at the SHAPE word
  reg         ovfl_r;           //! more words than the image declared
  reg         end_pend_r;       //! jnl_end_i seen, verdict next cycle

  // -----------------------------------------------------------------------
  // Replay state
  // -----------------------------------------------------------------------
  reg  [3:0]  rp_r;             //! record pointer
  reg  [2:0]  k_r;              //! word-within-record fetch counter
  reg  [31:0] cmd_r;            //! record word 5 (the 0x7B4 payload)
  reg  [31:0] meta_r;           //! record word 2 (the 0x7A8 payload)
  reg  [3:0]  n_ok_r;           //! records the engine injected (status 0)
  reg  [7:0]  refused_r;        //! bit r = record r came back status != 0
  reg  [3:0]  n_rec_acc_r;      //! record count of the ACCEPTED image
  reg  [31:0] acc_seq_r;        //! SEQ watermark of the last accepted image
  reg         acc_any_r;        //! any image accepted since reset
  reg         done_r;           //! a verdict has been produced since reset

  //! declared image length in words, header + records (CRC trailer excluded)
  wire [15:0] exp_body_w = 16'(HDR_WORDS_C) +
                           (16'(n_rec_r) * 16'(REC_WORDS_C));
  wire        is_crc_word_w = !shape_bad_r && (wcnt_r == exp_body_w);
  wire        in_rec_area_w = !shape_bad_r && (wcnt_r >= 16'(HDR_WORDS_C)) &&
                              (wcnt_r < exp_body_w);
  wire [15:0] rec_off_w     = wcnt_r - 16'(HDR_WORDS_C);

  //! wrap-safe generation compare (SEQ is a free-running u32)
  wire        seq_newer_w = ($signed(h_seq_r) - $signed(acc_seq_r)) > 0;
  wire [31:0] crc_fin_w   = crc_r ^ 32'hFFFF_FFFF;

  //! VERDICT ORDER. Structural tests first because they NAME the failure an
  //! operator will see (an erased slot is "MAGIC", not "CRC"); the CRC is
  //! the authority and gates everything that is TRUSTED FOR ACTION — the
  //! entity id, the SEQ watermark and every record word are only consulted
  //! after it has closed.
  logic [3:0] verdict_w;
  always_comb begin : verdict_calc
    if      (wcnt_r < 16'(HDR_WORDS_C))                verdict_w = VD_LEN_C;
    else if (h_magic_r != MAGIC_P)                     verdict_w = VD_MAGIC_C;
    else if (h_ver_r[31:16] != FMT_MAJOR_P)            verdict_w = VD_VER_C;
    else if (shape_bad_r)                              verdict_w = VD_SHAPE_C;
    else if (ovfl_r || (wcnt_r != (exp_body_w + 16'd1))) verdict_w = VD_LEN_C;
    else if (crc_fin_w != crc_rx_r)                    verdict_w = VD_CRC_C;
    else if ({h_ent_hi_r, h_ent_lo_r} != entity_id_i)  verdict_w = VD_ENT_C;
    else if (acc_any_r && !seq_newer_w)                verdict_w = VD_STALE_C;
    else                                               verdict_w = VD_ACCEPT_C;
  end : verdict_calc

  //! ONE staging-RAM address: the LOAD stream while words are arriving, the
  //! replay walk (record rp_r, word k_r) afterwards. They never overlap in
  //! time, so one port serves both.
  always_comb begin : rd_addr_mux
    if (st_r == ST_LOAD_S) rd_addr_w = RAM_AW_C'(rec_off_w);
    else                   rd_addr_w = RAM_AW_C'((32'(rp_r) * REC_WORDS_C) +
                                                 32'(k_r));
  end : rd_addr_mux

  // -----------------------------------------------------------------------
  // Record staging RAM write (own process, sync-only, house RAM rule)
  // -----------------------------------------------------------------------
  wire ram_we_w = (st_r == ST_LOAD_S) && jnl_wr_i && in_rec_area_w &&
                  (rec_off_w < 16'(RAM_WORDS_C));
  always_ff @(posedge clk_i) begin : rec_ram_wr
    if (ram_we_w) rec_ram_r[rd_addr_w] <= jnl_data_i;
  end : rec_ram_wr

  // -----------------------------------------------------------------------
  // Main sequencer
  // -----------------------------------------------------------------------
  always_ff @(posedge clk_i) begin : journal_seq
    if (!rst_n) begin
      st_r        <= ST_IDLE_S;
      verdict_r   <= VD_NONE_C;
      crc_r       <= 32'hFFFF_FFFF;
      crc_rx_r    <= 32'h0;
      wcnt_r      <= 16'd0;
      h_magic_r   <= 32'h0; h_ver_r <= 32'h0; h_seq_r <= 32'h0;
      h_ent_lo_r  <= 32'h0; h_ent_hi_r <= 32'h0;
      n_rec_r     <= 8'd0;  rec_w_r <= 8'd0;
      shape_bad_r <= 1'b0;  ovfl_r  <= 1'b0;  end_pend_r <= 1'b0;
      rp_r        <= 4'd0;  k_r     <= 3'd0;
      cmd_r       <= 32'h0; meta_r  <= 32'h0;
      n_ok_r      <= 4'd0;  refused_r <= 8'd0; n_rec_acc_r <= 4'd0;
      acc_seq_r   <= 32'h0; acc_any_r <= 1'b0; done_r <= 1'b0;
      rest_req_o  <= 1'b0;  rest_idx_o <= 4'd0;
      rest_talker_o <= 64'h0; rest_tuid_o <= 16'h0;
      rest_ctlr_o   <= 64'h0; rest_flags_o <= 16'h0;
    end else begin
      // ---- abort: back to idle, keep the accepted-image watermark ------
      if (jnl_abort_i) begin
        st_r       <= ST_IDLE_S;
        rest_req_o <= 1'b0;
        end_pend_r <= 1'b0;
      end
      // ---- start: only from a quiescent engine (never mid-replay) ------
      else if (jnl_start_i && ((st_r == ST_IDLE_S) || (st_r == ST_DONE_S))) begin
        st_r        <= ST_LOAD_S;
        verdict_r   <= VD_NONE_C;
        crc_r       <= 32'hFFFF_FFFF;
        crc_rx_r    <= 32'h0;
        wcnt_r      <= 16'd0;
        shape_bad_r <= 1'b0;
        ovfl_r      <= 1'b0;
        end_pend_r  <= 1'b0;
        n_rec_r     <= 8'd0;
        rec_w_r     <= 8'd0;
        h_magic_r   <= 32'h0;
        n_ok_r      <= 4'd0;
        refused_r   <= 8'd0;
        n_rec_acc_r <= 4'd0;
        rp_r        <= 4'd0;
        k_r         <= 3'd0;
      end else begin
        unique case (st_r)
          // ------------------------------------------------------------
          ST_LOAD_S: begin
            if (jnl_wr_i) begin
              wcnt_r <= wcnt_r + 16'd1;
              //! everything but the trailer is covered by the digest
              if (!is_crc_word_w) crc_r <= crc32_word_f(crc_r, jnl_data_i);
              unique casez (wcnt_r)
                16'd0: h_magic_r <= jnl_data_i;
                16'd1: h_ver_r   <= jnl_data_i;
                16'd2: h_seq_r   <= jnl_data_i;
                16'd3: begin
                  n_rec_r <= jnl_data_i[7:0];
                  rec_w_r <= jnl_data_i[15:8];
                  //! bound the parse BEFORE any record word lands, so an
                  //! absurd shape can never index past the staging RAM
                  shape_bad_r <= (jnl_data_i[15:8] != 8'(REC_WORDS_C)) ||
                                 (jnl_data_i[7:0]  == 8'd0) ||
                                 (jnl_data_i[7:0]  >  8'(MAX_REC_P));
                end
                16'd4: h_ent_lo_r <= jnl_data_i;
                16'd5: h_ent_hi_r <= jnl_data_i;
                default: begin
                  if (is_crc_word_w)      crc_rx_r <= jnl_data_i;
                  else if (!in_rec_area_w && !shape_bad_r) ovfl_r <= 1'b1;
                end
              endcase
            end
            if (jnl_end_i) end_pend_r <= 1'b1;
            if (end_pend_r && !jnl_wr_i) begin
              end_pend_r <= 1'b0;
              st_r       <= ST_VERIFY_S;
            end
          end
          // ------------------------------------------------------------
          ST_VERIFY_S: begin
            verdict_r <= verdict_w;
            done_r    <= 1'b1;
            if (verdict_w == VD_ACCEPT_C) begin
              n_rec_acc_r <= n_rec_r[3:0];
              rp_r        <= 4'd0;
              k_r         <= 3'd0;
              st_r        <= ST_FETCH_S;
            end else begin
              st_r <= ST_DONE_S;
            end
          end
          // ------------------------------------------------------------
          //! six async-read cycles lift one record out of the staging RAM
          ST_FETCH_S: begin
            unique case (k_r)
              3'd0: rest_talker_o[31:0]  <= rd_q_w;
              3'd1: rest_talker_o[63:32] <= rd_q_w;
              3'd2: begin meta_r <= rd_q_w; rest_tuid_o <= rd_q_w[15:0]; end
              3'd3: rest_ctlr_o[31:0]    <= rd_q_w;
              3'd4: rest_ctlr_o[63:32]   <= rd_q_w;
              default: begin
                cmd_r        <= rd_q_w;
                rest_flags_o <= rd_q_w[23:8];
                rest_idx_o   <= rd_q_w[3:0];
              end
            endcase
            if (k_r == 3'((REC_WORDS_C - 1))) begin
              k_r  <= 3'd0;
              st_r <= ST_ARM_S;
            end else begin
              k_r <= k_r + 3'd1;
            end
          end
          // ------------------------------------------------------------
          ST_ARM_S: begin
            //! VALID[30] clear = a hole in the journal table: that sink is
            //! deliberately left as the fabric found it
            if (cmd_r[30]) begin
              rest_req_o <= 1'b1;
              st_r       <= ST_WAIT_S;
            end else if (rp_r == (n_rec_acc_r - 4'd1)) begin
              st_r <= ST_DONE_S;
              acc_seq_r <= h_seq_r;
              acc_any_r <= 1'b1;
            end else begin
              rp_r <= rp_r + 4'd1;
              st_r <= ST_FETCH_S;
            end
          end
          // ------------------------------------------------------------
          ST_WAIT_S: begin
            //! drop req ON the ack: the engine re-arms on (req && !ack), so
            //! holding it one cycle longer would inject the record twice
            if (rest_ack_i) begin
              rest_req_o <= 1'b0;
              if (rest_status_i == 2'd0) n_ok_r <= n_ok_r + 4'd1;
              else                       refused_r[rp_r[2:0]] <= 1'b1;
              if (rp_r == (n_rec_acc_r - 4'd1)) begin
                st_r      <= ST_DONE_S;
                acc_seq_r <= h_seq_r;
                acc_any_r <= 1'b1;
              end else begin
                rp_r <= rp_r + 4'd1;
                st_r <= ST_FETCH_S;
              end
            end
          end
          // ------------------------------------------------------------
          default: begin   // ST_IDLE_S / ST_DONE_S
            rest_req_o <= 1'b0;
          end
        endcase
      end
    end
  end : journal_seq

  // -----------------------------------------------------------------------
  // Status word
  //   [2:0]   FSM state          [3]     0
  //   [7:4]   verdict (VD_*)     [11:8]  n_rec of the ACCEPTED image
  //   [15:12] records injected   [23:16] per-record refusal bitmap
  //   [30]    done               [31]    busy
  // -----------------------------------------------------------------------
  wire busy_w = (st_r != ST_IDLE_S) && (st_r != ST_DONE_S);
  assign stat_o = {busy_w, done_r, 6'd0, refused_r, n_ok_r, n_rec_acc_r,
                   verdict_r, 1'b0, st_r};
  assign seq_o  = acc_seq_r;

  // verilator lint_off UNUSED
  wire [31:0] unused_w = {meta_r[31:16], h_ver_r[15:0], rec_w_r,
                          cmd_r[31], cmd_r[29:24], cmd_r[7:4], 1'b0};
  // verilator lint_on UNUSED

endmodule

`default_nettype wire

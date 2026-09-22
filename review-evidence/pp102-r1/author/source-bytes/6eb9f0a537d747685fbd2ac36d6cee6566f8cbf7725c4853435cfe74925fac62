/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_ucpu.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/06 §8)
//
//  Description : AECP micro-coded engine SKELETON — the area experiment of
//                docs/10_RESOURCE_AND_EFFORT.md §6. Everything the ceiling
//                analysis names is real here: 4-stage F/D/E/W pipeline
//                (01 §4 Option C), 2048 × 48 µcode ROM (BRAM), 16 × 64-bit
//                operand file in DISTRIBUTED RAM (never flops — the +894-LUT
//                counter-mirror failure mode), 32-bit ALU with 64-bit move /
//                merge paths, response + iteration cursors, 5-bit status,
//                and decode for all 30 µISA operations of 06 §8. External
//                state (07 §3 image+overlay), gather sources, the response
//                buffer and the effect strobes are PORTS: this block is the
//                execute stage only, priced against the emit-engine mass it
//                would displace.
//
//                Encoding notes an implementer must keep (ucpu_pkg.sv):
//                CHECK_ARG compares fmt(rf[ra]) rel rf[rb] — rb is mandatory,
//                imm[10:0] is the fail target. DESC_ADDR never branches; it
//                sets NO_SUCH_DESCRIPTOR and the µprogram tests it with
//                BRANCH_IF_STATUS, exactly as the 06 §8 exemplar is written.
//                MOVE with ra = r0 loads zext(imm24).
//
//                RAW hazard: single pending-writeback interlock (a D-stage
//                read of a register with a write in flight bubbles one
//                cycle). Branches resolve in E and flush F/D (2-cycle
//                penalty). Multi-cycle operations (state, gather, copy,
//                header, send) hold E; F and D hold with it.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_ucpu
  import ucpu_pkg::*;
#(
    //! path of the µcode ROM image (2048 lines of 12 hex digits)
    parameter string UCODE_HEX_P = "ucode.hex"
) (
    input  wire         clk_i,
    input  wire         rst_n,

    //! dispatch: one command enters with its µPC entry + parsed operands
    input  wire         disp_valid_i,
    output logic        disp_ready_o,
    input  wire  [10:0] disp_upc_i,
    input  wire  [63:0] disp_ctlr_eid_i,   //! -> r15
    input  wire  [63:0] disp_opd0_i,       //! -> r14 (desc type|index|arg)
    input  wire  [63:0] disp_opd1_i,       //! -> r13
    //! -> r12, the SET family's ARGUMENT. The three registers above carry the
    //! locate key, the {type, index} echo and the controller id, which is
    //! everything a GET needs; a SET also has to carry the VALUE it was asked
    //! to store, and the µISA has no shift to dig it out of a packed field.
    //! Preloading it is a register write in a state that already exists, and
    //! it is what lets one µprogram serve any settable field.
    input  wire  [63:0] disp_opd2_i,       //! -> r12 (the SET argument)
    //! GET_DYNAMIC_INFO executes an ordinary getter against an aggregate
    //! response already in progress. In that mode BUILD_HEADER is suppressed
    //! and fields begin at the supplied absolute response-buffer cursor.
    input  wire         disp_batch_i,
    input  wire   [9:0] disp_resp_base_i,

    //! state port: descriptor image + overlay + names (07 §3), 1RW
    output logic        st_req_o,
    output logic        st_we_o,
    output logic        st_name_o,         //! name-region select
    output logic [19:0] st_addr_o,
    output logic [63:0] st_wdata_o,
    output logic  [7:0] st_wstrb_o,
    input  wire         st_ready_i,        //! write accepted
    input  wire         st_rvalid_i,       //! read data / locate result
    input  wire  [63:0] st_rdata_i,
    input  wire         st_err_i,          //! locate miss -> NO_SUCH_DESCRIPTOR

    //! gather port: atomic external snapshots (06 §6.2/§6.6) + map validate
    output logic        gx_req_o,
    output logic  [7:0] gx_sel_o,
    input  wire         gx_valid_i,
    input  wire  [63:0] gx_data_i,

    //! lock context (06 §6.4)
    input  wire         lock_held_i,
    input  wire  [63:0] lock_ctlr_i,

    //! response buffer: 32-bit write lane + strobes, FLOW CONTROLLED.
    //! `rb_ready_i` low HOLDS the E stage with the write still presented, so
    //! the buffer may live anywhere — including the integrator's main memory
    //! (KL_aecp_resp_buf), where a lane flush costs a memory round trip. A
    //! buffer that is always able to take a write ties it high and nothing
    //! about this pipeline changes.
    output logic        rb_we_o,
    output logic  [9:0] rb_addr_o,
    output logic [31:0] rb_wdata_o,
    output logic  [3:0] rb_wstrb_o,
    input  wire         rb_ready_i,

    //! respond / effects
    output logic        resp_send_o,
    output logic [10:0] resp_len_o,
    output logic  [4:0] resp_status_o,
    input  wire         tx_ready_i,
    output logic        eff_commit_o,
    output logic  [7:0] eff_nvm_mark_o,
    output logic        eff_nvm_stb_o,
    output logic  [3:0] eff_notify_class_o,
    output logic        eff_notify_stb_o,

    //! observability (keeps the experiment honest and the TB wrap-free)
    output logic        busy_o,
    output logic        done_o,
    output logic [10:0] dbg_upc_o,
    output logic  [4:0] dbg_status_o,
    output logic        dbg_ovf_o
);

  // ------------------------------------------------------------------ ROM
  logic [UCODE_W_C-1:0] rom_r [0:(1<<UPC_W_C)-1];
  initial $readmemh(UCODE_HEX_P, rom_r);

  logic [UCODE_W_C-1:0] rom_q_r;
  logic [UPC_W_C-1:0]   upc_r;

  // ------------------------------------------------------- register file
  // 16 x 64 distributed RAM, 1W3R (SET_MASKED reads rd as well); the three
  // async read ports replicate the LUTRAM — that replication is part of the
  // honest price of the merge path.
  (* ram_style = "distributed" *) logic [63:0] rf_r [0:15];
  logic  [3:0] rf_waddr_w;
  logic [63:0] rf_wdata_w;
  logic        rf_we_w;

  always_ff @(posedge clk_i) begin : rf_write
    if (rf_we_w) rf_r[rf_waddr_w] <= rf_wdata_w;
  end

  // ------------------------------------------------------- machine state
  typedef enum logic [2:0] {
    S_IDLE, S_PRE3, S_PRE2, S_PRE1, S_PRE0, S_RUN
  } mstate_e;
  mstate_e ms_r;

  // pipeline registers
  logic        vld_d_r;                    // instruction word in rom_q_r
  uop_t        uop_e_r;                    // E-stage op
  logic        vld_e_r;
  logic [63:0] opa_e_r, opb_e_r, opd_e_r;  // rf[ra], rf[rb], rf[rd]
  logic  [3:0] wb_rd_r;                    // W stage
  logic [63:0] wb_data_r;
  logic        wb_we_r;

  // architectural side state
  logic  [4:0] status_r;
  logic        z_r, lt_r, ovf_r;
  logic [19:0] desc_base_r;
  logic  [7:0] iter_cnt_r, iter_idx_r;
  logic  [9:0] cursor_r;
  logic [10:0] resp_len_r;
  logic        batch_r;

  // multi-cycle E sequencing
  logic  [3:0] eseq_r;                     // beat counter inside one op
  logic        copy_go_r;                  // COPY_BUFFER length loaded
  logic [15:0] copy_left_r;                // COPY_BUFFER bytes remaining
  logic [12:0] copy_idx_r;                 // 64-bit lanes already copied
  logic [63:0] copy_lane_r;                // held 64-bit lane during copy

  uop_t uop_d_w;
  assign uop_d_w = uop_t'(rom_q_r);

  // ------------------------------------------------------------- hazards
  logic raw_d_w;
  logic e_writes_w;
  always_comb begin : raw_detect
    e_writes_w = vld_e_r && (uop_e_r.op inside {OP_MOVE, OP_SET_MASKED,
                                                OP_SHIFT_R,
                                                OP_READ_ST, OP_NAME_RD,
                                                OP_GATHER_EXT});
    raw_d_w = vld_d_r &&
              ((e_writes_w && ((uop_d_w.ra == uop_e_r.rd) ||
                               (uop_d_w.rb == uop_e_r.rd) ||
                               (uop_d_w.rd == uop_e_r.rd))) ||
               (wb_we_r    && ((uop_d_w.ra == wb_rd_r) ||
                               (uop_d_w.rb == wb_rd_r) ||
                               (uop_d_w.rd == wb_rd_r))));
  end

  // ------------------------------------------------------------ E stage
  logic [63:0] a_fmt_w, b_or_imm_w;
  always_comb begin : operand_shape
    unique case (uop_e_r.fmt)
      FMT_B_C: a_fmt_w = {56'd0, opa_e_r[7:0]};
      FMT_W_C: a_fmt_w = {48'd0, opa_e_r[15:0]};
      FMT_D_C: a_fmt_w = {32'd0, opa_e_r[31:0]};
      default: a_fmt_w = opa_e_r;
    endcase
    b_or_imm_w = (uop_e_r.rb != 4'd0) ? opb_e_r : {40'd0, uop_e_r.imm};
  end

  // 32-bit ALU (compare path) + 64-bit merge
  logic [32:0] sub_w;
  logic        cmp_z_w, cmp_lt_w;
  logic [63:0] merged_w;
  always_comb begin : alu
    sub_w    = {1'b0, a_fmt_w[31:0]} - {1'b0, b_or_imm_w[31:0]};
    cmp_z_w  = (uop_e_r.fmt == FMT_Q_C) ? (opa_e_r == b_or_imm_w)
                                        : (sub_w[31:0] == 32'd0);
    cmp_lt_w = sub_w[32];
    merged_w = (opd_e_r & ~opb_e_r) | (opa_e_r & opb_e_r);
  end

  logic rel_pass_w;
  always_comb begin : relation
    unique case (uop_e_r.cnd[2:0])
      3'd0:    rel_pass_w = cmp_z_w;    // EQ
      3'd1:    rel_pass_w = !cmp_z_w;   // NE
      3'd2:    rel_pass_w = cmp_lt_w;   // LT
      3'd3:    rel_pass_w = !cmp_lt_w;  // GE
      default: rel_pass_w = cmp_z_w;
    endcase
  end

  logic brflag_w;
  always_comb begin : branch_flag
    unique case (uop_e_r.cnd)
      4'd0:    brflag_w = (status_r != ST_SUCCESS_C);
      4'd1:    brflag_w = (iter_idx_r == iter_cnt_r);
      4'd2:    brflag_w = z_r;
      4'd3:    brflag_w = lt_r;
      4'd4:    brflag_w = ovf_r;
      default: brflag_w = 1'b0;
    endcase
  end

  logic [3:0] fld_len_w;
  always_comb begin : field_len
    unique case (uop_e_r.fmt)
      FMT_B_C: fld_len_w = 4'd1;
      FMT_W_C: fld_len_w = 4'd2;
      FMT_D_C: fld_len_w = 4'd4;
      default: fld_len_w = 4'd8;
    endcase
  end

  //! COPY_BUFFER advances the cursor by the bytes it actually COPIES, not by
  //! the 8-byte lane it reads. A descriptor length is not a multiple of 8
  //! (07 §3.2: CONFIGURATION 74+4n, AVB_INTERFACE 102, CLOCK_SOURCE 86), so
  //! rounding the last lane up would put 1..7 bytes of the NEXT descriptor on
  //! the wire and lie about `control_data_length`. The final lane still writes
  //! a whole 32-bit word into the response buffer — those bytes sit past
  //! `resp_len_o` and are never emitted.
  logic [3:0] copy_adv1_w, copy_adv2_w;
  always_comb begin : copy_residual
    copy_adv1_w = (copy_left_r > 16'd4) ? 4'd4 : 4'(copy_left_r[3:0]);
    if (copy_left_r <= 16'd4)      copy_adv2_w = 4'd0;
    else if (copy_left_r > 16'd8)  copy_adv2_w = 4'd4;
    else                           copy_adv2_w = 4'(copy_left_r[3:0] - 4'd4);
  end

  logic append_skip_w;
  assign append_skip_w = (uop_e_r.op == OP_APPEND) &&
                         (({1'b0, cursor_r} + {7'd0, fld_len_w}) >
                          11'(RESP_CAP_C));

  logic is_q_field_w;
  assign is_q_field_w = (uop_e_r.op inside {OP_BUILD_FLD, OP_APPEND}) &&
                        (uop_e_r.fmt == FMT_Q_C) && !append_skip_w;

  //! the response buffer refused the write presented this cycle: hold the
  //! whole E stage — operand registers, `eseq_r`, cursor and status all keep
  //! their value and the SAME write is re-presented next cycle. This is the
  //! one back-pressure the µISA has to honour for a buffer that is not
  //! guaranteed single-cycle (06 §8 never said it was).
  logic rb_hold_w;
  assign rb_hold_w = rb_we_o && !rb_ready_i;

  // ---- E-stage control outcomes ----------------------------------------
  logic stall_e_w;
  logic br_taken_w;
  logic [UPC_W_C-1:0] br_tgt_w;
  logic end_op_w;

  always_comb begin : e_control
    stall_e_w  = 1'b0;
    br_taken_w = 1'b0;
    br_tgt_w   = uop_e_r.imm[UPC_W_C-1:0];
    end_op_w   = 1'b0;
    if (vld_e_r) begin
      unique case (uop_e_r.op)
        OP_BRANCH:     br_taken_w = 1'b1;
        OP_BR_STATUS:  br_taken_w = brflag_w;
        OP_END:        end_op_w   = 1'b1;
        OP_DESC_ADDR,
        OP_READ_ST,
        OP_NAME_RD:    stall_e_w = !st_rvalid_i;
        OP_WRITE_ST,
        OP_NAME_WR:    stall_e_w = !st_ready_i;
        OP_GATHER_EXT,
        OP_MAP_VALID:  stall_e_w = !gx_valid_i;
        OP_READ_CTRS:  stall_e_w = (eseq_r != 4'd4);
        OP_COPY_BUF:   stall_e_w = !copy_go_r || (copy_left_r != 16'd0) ||
                                   (eseq_r != 4'd0);
        OP_BUILD_HDR:  stall_e_w = (eseq_r != 4'd2);
        OP_BUILD_FLD,
        OP_APPEND:     stall_e_w = is_q_field_w && (eseq_r == 4'd0);
        OP_SEND_RESP:  stall_e_w = !tx_ready_i;
        OP_CHECK_LOCK: br_taken_w = lock_held_i && (lock_ctlr_i != opa_e_r);
        OP_CHECK_ARG:  br_taken_w = !rel_pass_w;
        default: ;
      endcase
      if ((uop_e_r.op == OP_MAP_VALID) && gx_valid_i && !gx_data_i[0])
        br_taken_w = 1'b1;
      if (rb_hold_w) stall_e_w = 1'b1;
    end
  end

  // ------------------------------------------------------- state port out
  always_comb begin : state_port
    st_req_o   = 1'b0;
    st_we_o    = 1'b0;
    st_name_o  = 1'b0;
    st_wdata_o = opa_e_r;
    st_addr_o  = desc_base_r + uop_e_r.imm[19:0];
    unique case (uop_e_r.fmt)
      FMT_B_C: st_wstrb_o = 8'h01;
      FMT_W_C: st_wstrb_o = 8'h03;
      FMT_D_C: st_wstrb_o = 8'h0F;
      default: st_wstrb_o = 8'hFF;
    endcase
    if (vld_e_r) begin
      unique case (uop_e_r.op)
        OP_DESC_ADDR: begin
          st_req_o  = 1'b1;
          // locate: {type,index} live in r14's low 32 bits, region in imm
          st_addr_o = uop_e_r.imm[19:0] ^ {4'd0, opa_e_r[15:0]};
        end
        OP_READ_ST:  st_req_o = 1'b1;
        OP_NAME_RD:  begin st_req_o = 1'b1; st_name_o = 1'b1;
                           st_addr_o = opa_e_r[19:0]
                                       + uop_e_r.imm[19:0]; end
        OP_WRITE_ST: begin st_req_o = 1'b1; st_we_o = 1'b1; end
        OP_NAME_WR:  begin st_req_o = 1'b1; st_we_o = 1'b1;
                           st_name_o = 1'b1;
                           st_addr_o = opb_e_r[19:0]
                                       + uop_e_r.imm[19:0]; end
        OP_COPY_BUF: begin
          st_req_o  = copy_go_r && (copy_left_r != 16'd0) &&
                      (eseq_r == 4'd0);
          st_addr_o = desc_base_r + uop_e_r.imm[19:0] +
                      {4'd0, copy_idx_r, 3'd0};
        end
        default: ;
      endcase
    end
  end

  // ------------------------------------------------------ gather port out
  always_comb begin : gather_port
    gx_req_o = 1'b0;
    gx_sel_o = {uop_e_r.cnd, uop_e_r.imm[3:0]};
    if (vld_e_r) begin
      unique case (uop_e_r.op)
        OP_GATHER_EXT: gx_req_o = 1'b1;
        OP_MAP_VALID:  begin gx_req_o = 1'b1;
                             gx_sel_o = {uop_e_r.cnd, 4'd0}; end
        OP_READ_CTRS:  begin gx_req_o = (eseq_r < 4'd4);
                             gx_sel_o = {uop_e_r.cnd, eseq_r}; end
        default: ;
      endcase
    end
  end

  // -------------------------------------------------- response buffer out
  logic [31:0] hdr_word_w;
  always_comb begin : header_word
    unique case (eseq_r)
      4'd0:    hdr_word_w = opa_e_r[63:32];            // target eid hi
      4'd1:    hdr_word_w = opa_e_r[31:0];             // target eid lo
      default: hdr_word_w = {opb_e_r[15:0],            // seq echo
                             3'd0, status_r, 8'd0};    // status field
    endcase
  end

  always_comb begin : resp_buffer
    rb_we_o    = 1'b0;
    rb_addr_o  = cursor_r;
    rb_wdata_o = a_fmt_w[31:0];
    rb_wstrb_o = 4'hF;
    if (vld_e_r) begin
      unique case (uop_e_r.op)
        OP_BUILD_HDR: begin
          rb_we_o    = !batch_r;
          rb_addr_o  = {4'd0, eseq_r[1:0], 4'd0} >> 2;  // 0, 4, 8
          rb_wdata_o = hdr_word_w;
        end
        OP_BUILD_FLD, OP_APPEND: begin
          rb_we_o = !append_skip_w;
          if (is_q_field_w) begin
            rb_addr_o  = cursor_r + ((eseq_r == 4'd1) ? 10'd4 : 10'd0);
            rb_wdata_o = (eseq_r == 4'd0) ? opa_e_r[63:32] : opa_e_r[31:0];
          end else begin
            unique case (uop_e_r.fmt)
              FMT_B_C: rb_wstrb_o = 4'h1;
              FMT_W_C: rb_wstrb_o = 4'h3;
              default: rb_wstrb_o = 4'hF;
            endcase
          end
        end
        OP_READ_CTRS: begin
          rb_we_o    = gx_valid_i && (eseq_r < 4'd4);
          rb_wdata_o = gx_data_i[31:0];
        end
        OP_COPY_BUF: begin
          //! A short final lane has no second word. Writing it anyway places
          //! stale bytes after the declared response and, in a batch, into
          //! the next dynamic_info header.
          rb_we_o    = ((eseq_r == 4'd1) && (copy_adv1_w != 4'd0))
                       || ((eseq_r == 4'd2) && (copy_adv2_w != 4'd0));
          rb_wdata_o = (eseq_r == 4'd1) ? copy_lane_r[63:32]
                                        : copy_lane_r[31:0];
        end
        default: ;
      endcase
    end
  end

  // ------------------------------------------------------------ effects
  logic advance_e_w;
  assign advance_e_w = vld_e_r && !stall_e_w;

  always_comb begin : effects
    eff_commit_o       = advance_e_w && (uop_e_r.op == OP_COMMIT);
    eff_nvm_stb_o      = advance_e_w && (uop_e_r.op == OP_NVM_MARK);
    eff_nvm_mark_o     = uop_e_r.imm[7:0];
    eff_notify_stb_o   = advance_e_w && (uop_e_r.op == OP_NOTIFY_ENQ);
    eff_notify_class_o = uop_e_r.imm[3:0];
    resp_send_o        = advance_e_w && (uop_e_r.op == OP_SEND_RESP);
    resp_len_o         = resp_len_r;
    resp_status_o      = status_r;
  end

  // --------------------------------------------------------- W writeback
  always_comb begin : writeback_mux
    rf_we_w    = wb_we_r;
    rf_waddr_w = wb_rd_r;
    rf_wdata_w = wb_data_r;
    unique case (ms_r)
      S_PRE3: begin rf_we_w = 1'b1; rf_waddr_w = 4'd12;
                    rf_wdata_w = disp_opd2_i; end
      S_PRE2: begin rf_we_w = 1'b1; rf_waddr_w = 4'd15;
                    rf_wdata_w = disp_ctlr_eid_i; end
      S_PRE1: begin rf_we_w = 1'b1; rf_waddr_w = 4'd14;
                    rf_wdata_w = disp_opd0_i; end
      S_PRE0: begin rf_we_w = 1'b1; rf_waddr_w = 4'd13;
                    rf_wdata_w = disp_opd1_i; end
      default: ;
    endcase
  end

  // ------------------------------------------------------- sequential core
  always_ff @(posedge clk_i) begin : core
    if (!rst_n) begin
      ms_r        <= S_IDLE;
      upc_r       <= '0;
      vld_d_r     <= 1'b0;
      vld_e_r     <= 1'b0;
      wb_we_r     <= 1'b0;
      wb_rd_r     <= '0;
      wb_data_r   <= '0;
      status_r    <= ST_SUCCESS_C;
      z_r         <= 1'b0;
      lt_r        <= 1'b0;
      ovf_r       <= 1'b0;
      desc_base_r <= '0;
      iter_cnt_r  <= '0;
      iter_idx_r  <= '0;
      cursor_r    <= '0;
      resp_len_r  <= '0;
      batch_r     <= 1'b0;
      eseq_r      <= '0;
      copy_go_r   <= 1'b0;
      copy_left_r <= '0;
      copy_idx_r  <= '0;
      copy_lane_r <= '0;
      rom_q_r     <= '0;
      uop_e_r     <= '0;
      opa_e_r     <= '0;
      opb_e_r     <= '0;
      opd_e_r     <= '0;
      done_o      <= 1'b0;
    end else begin
      done_o  <= 1'b0;
      wb_we_r <= 1'b0;

      unique case (ms_r)
        S_IDLE: begin
          vld_d_r <= 1'b0;
          vld_e_r <= 1'b0;
          if (disp_valid_i) begin
            ms_r        <= S_PRE3;
            upc_r       <= disp_upc_i;
            status_r    <= ST_SUCCESS_C;
            z_r         <= 1'b0;
            lt_r        <= 1'b0;
            ovf_r       <= 1'b0;
            batch_r     <= disp_batch_i;
            cursor_r    <= disp_batch_i ? disp_resp_base_i : 10'd12;
            resp_len_r  <= disp_batch_i ? {1'b0, disp_resp_base_i} : 11'd12;
            iter_cnt_r  <= '0;
            iter_idx_r  <= '0;
            eseq_r      <= '0;
            copy_go_r   <= 1'b0;
            copy_left_r <= '0;
          end
        end
        S_PRE3: ms_r <= S_PRE2;
        S_PRE2: ms_r <= S_PRE1;
        S_PRE1: ms_r <= S_PRE0;
        S_PRE0: ms_r <= S_RUN;

        S_RUN: begin
          // ---------------- F: µcode ROM sync read ----------------------
          if (!stall_e_w && !raw_d_w) begin
            rom_q_r <= rom_r[upc_r];
            vld_d_r <= 1'b1;
            upc_r   <= upc_r + UPC_W_C'(1);
          end

          // ---------------- D -> E latch --------------------------------
          if (!stall_e_w) begin
            if (raw_d_w) begin
              vld_e_r <= 1'b0;               // bubble
            end else begin
              vld_e_r <= vld_d_r;
              uop_e_r <= uop_d_w;
              opa_e_r <= rf_r[uop_d_w.ra];
              opb_e_r <= rf_r[uop_d_w.rb];
              opd_e_r <= rf_r[uop_d_w.rd];
            end
          end

          // ---------------- E: per-beat sequencing (runs under stall, but
          // NOT while the response buffer is refusing the write: the beat
          // counter is what selects the write, so advancing it would lose
          // the very byte the buffer just declined) --------------------
          if (vld_e_r && !rb_hold_w) begin
            unique case (uop_e_r.op)
              OP_BUILD_HDR: begin
                eseq_r <= (eseq_r == 4'd2) ? 4'd0 : eseq_r + 4'd1;
              end
              OP_BUILD_FLD, OP_APPEND: begin
                if (is_q_field_w)
                  eseq_r <= (eseq_r == 4'd1) ? 4'd0 : 4'd1;
              end
              OP_READ_CTRS: begin
                if (gx_valid_i && (eseq_r < 4'd4)) begin
                  eseq_r     <= eseq_r + 4'd1;
                  cursor_r   <= cursor_r + 10'd4;
                  resp_len_r <= resp_len_r + 11'd4;
                end else if (eseq_r == 4'd4) begin
                  eseq_r <= 4'd0;
                end
              end
              OP_COPY_BUF: begin
                if (!copy_go_r) begin
                  copy_go_r   <= 1'b1;
                  copy_left_r <= opa_e_r[15:0];
                  copy_idx_r  <= '0;
                end else if ((eseq_r == 4'd0) && st_rvalid_i &&
                             (copy_left_r != 16'd0)) begin
                  copy_lane_r <= st_rdata_i;
                  eseq_r      <= 4'd1;
                end else if (eseq_r == 4'd1) begin
                  eseq_r     <= 4'd2;
                  cursor_r   <= cursor_r + {6'd0, copy_adv1_w};
                  resp_len_r <= resp_len_r + {7'd0, copy_adv1_w};
                end else if (eseq_r == 4'd2) begin
                  eseq_r      <= 4'd0;
                  cursor_r    <= cursor_r + {6'd0, copy_adv2_w};
                  resp_len_r  <= resp_len_r + {7'd0, copy_adv2_w};
                  copy_left_r <= (copy_left_r > 16'd8)
                               ? copy_left_r - 16'd8 : 16'd0;
                  copy_idx_r  <= copy_idx_r + 13'd1;
                end
              end
              default: eseq_r <= 4'd0;
            endcase

            if (advance_e_w) begin
              copy_go_r <= 1'b0;
              // writeback staging
              unique case (uop_e_r.op)
                OP_MOVE: begin
                  wb_we_r <= 1'b1; wb_rd_r <= uop_e_r.rd;
                  wb_data_r <= (uop_e_r.ra == 4'd0)
                             ? {40'd0, uop_e_r.imm}
                             : a_fmt_w;
                end
                OP_SET_MASKED: begin
                  wb_we_r <= 1'b1; wb_rd_r <= uop_e_r.rd;
                  wb_data_r <= merged_w;
                end
                OP_SHIFT_R: begin
                  wb_we_r <= 1'b1; wb_rd_r <= uop_e_r.rd;
                  wb_data_r <= opa_e_r >> uop_e_r.imm[5:0];
                end
                OP_READ_ST, OP_NAME_RD: begin
                  wb_we_r <= 1'b1; wb_rd_r <= uop_e_r.rd;
                  wb_data_r <= st_rdata_i;
                end
                OP_GATHER_EXT: begin
                  wb_we_r <= 1'b1; wb_rd_r <= uop_e_r.rd;
                  wb_data_r <= gx_data_i;
                end
                default: ;
              endcase

              // architectural side effects at op completion
              unique case (uop_e_r.op)
                OP_COMPARE:    begin z_r <= cmp_z_w; lt_r <= cmp_lt_w; end
                OP_DESC_ADDR:  begin
                  if (st_err_i) status_r <= ST_NO_SUCH_DESC_C;
                  else          desc_base_r <= st_rdata_i[19:0];
                end
                OP_READ_ST:
                  if (st_err_i) status_r <= ST_BAD_ARGUMENTS_C;
                OP_WRITE_ST:
                  if (st_err_i) status_r <= ST_ENTITY_MISBEHAVING_C;
                OP_CHECK_LOCK:
                  if (br_taken_w) status_r <= ST_LOCKED_C;
                OP_CHECK_ARG:
                  if (br_taken_w)
                    status_r <= uop_e_r.cnd[3] ? ST_NOT_SUPPORTED_C
                                               : ST_BAD_ARGUMENTS_C;
                OP_MAP_VALID:
                  if (br_taken_w) status_r <= ST_BAD_ARGUMENTS_C;
                OP_ITER_OPEN:  begin
                  iter_cnt_r <= opa_e_r[7:0]; iter_idx_r <= '0;
                end
                OP_ITER_NEXT:  iter_idx_r <= iter_idx_r + 8'd1;
                OP_SET_STATUS: status_r   <= uop_e_r.imm[4:0];
                OP_SET_LENGTH: resp_len_r <= uop_e_r.imm[10:0];
                OP_BUILD_FLD, OP_APPEND: begin
                  if (append_skip_w) ovf_r <= 1'b1;
                  else begin
                    cursor_r   <= cursor_r + {6'd0, fld_len_w};
                    resp_len_r <= resp_len_r + {7'd0, fld_len_w};
                  end
                end
                default: ;
              endcase

              // control flow
              if (end_op_w) begin
                ms_r    <= S_IDLE;
                vld_d_r <= 1'b0;
                vld_e_r <= 1'b0;
                done_o  <= 1'b1;
              end else if (br_taken_w) begin
                upc_r   <= br_tgt_w;
                vld_d_r <= 1'b0;   // flush F/D
                vld_e_r <= 1'b0;
              end
            end
          end
        end
        default: ms_r <= S_IDLE;
      endcase
    end
  end

  assign disp_ready_o = (ms_r == S_IDLE);
  assign busy_o       = (ms_r != S_IDLE);
  assign dbg_upc_o    = upc_r;
  assign dbg_status_o = status_r;
  assign dbg_ovf_o    = ovf_r;

endmodule : KL_aecp_ucpu
`default_nettype wire

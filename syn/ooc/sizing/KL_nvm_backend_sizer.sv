/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_nvm_backend_sizer.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_FASTCONNECT.md section 8.3)
//
//  Description : AREA SIZING SKETCH. Two tops that answer one question:
//                what does replacing KL_pp_shadow's blank-flash responder
//                with the section 8 backend cost in LUT and FF?
//
//                  KL_nvm_blankflash_sizer -- the BEFORE. The responder that
//                    ships today, lifted verbatim from hdl/milan/KL_pp_shadow.sv
//                    so the two numbers are measured on the same face.
//                  KL_nvm_backend_sizer    -- the AFTER. The three pieces
//                    section 8.3 names: the region-to-offset decoder, the
//                    main-memory access path, and the control CSRs, plus the
//                    liveness and commit deadline counters of section 9.4.
//
//  THIS IS NOT SHIPPING RTL, and it is deliberately NOT under `hdl/`.
//  Nothing instantiates it, `milan_soc.py` does not register it, and
//  `scripts/lint_rtl.py` (which sweeps `hdl/`) does not see it. It exists so
//  the decision record can quote a MEASURED upper bound instead of an
//  estimate. The implementation ticket owns the shipping module, its tests
//  and the post-place delta; this file owns the number.
//
//  Measure with (see syn/yosys/README.md for the toolchain):
//    OOC_CHPARAM="N_STREAM_IN_P=1 N_STREAM_OUT_P=1 N_SPORT_IN_P=1 \
//                 N_SPORT_OUT_P=1 N_NAME_BANK_P=4  MAP_BYTES_P=136" \
//      syn/yosys/ooc.sh KL_nvm_backend_sizer KL_nvm_blankflash_sizer
//    OOC_CHPARAM="N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_SPORT_IN_P=8 \
//                 N_SPORT_OUT_P=8 N_NAME_BANK_P=30 MAP_BYTES_P=256" \
//      syn/yosys/ooc.sh KL_nvm_backend_sizer KL_nvm_blankflash_sizer
//
//  Stated simplifications, each one an UNDER-count risk named rather than
//  hidden:
//    (a) the two channel-map groups carry a per-port byte count, so their
//        record bases are not a constant stride. The sketch carries the
//        16-entry prefix table a real backend needs, loaded through the CSR
//        face, so that cost IS in the number.
//    (b) memory accesses are one byte per handshake -- a write strobe per
//        byte, and a word fetch per read byte -- rather than coalesced into
//        words. That is not a throughput loss: the port itself streams one
//        byte per handshake (KL_pp_nvm_port F02.8), so the memory side is
//        already matched to the source. A coalescing implementation would
//        add a word buffer and a lane mux, so this figure bounds the DECODE
//        and CONTROL cost rather than every possible datapath.
//    (c) the container CRC-32 of section 6 is NOT here. It is the reader's,
//        not the backend's -- the backend moves record bytes between the port
//        and the image; the acceptance order of section 6.2 runs above it.
//---------------------------------------------------------------------------//
`default_nettype none

//===========================================================================//
//  BEFORE: the blank-flash responder that ships today                       //
//  Lifted verbatim from hdl/milan/KL_pp_shadow.sv so the delta is honest.   //
//===========================================================================//
module KL_nvm_blankflash_sizer (
    input  wire        clk_i,          //! core clock
    input  wire        rst_n,          //! synchronous active-low reset

    //! ---- device face: target of KL_pp_nvm_port's initiator ----
    input  wire        dev_req_i,      //! command request
    output logic       dev_gnt_o,      //! command accepted (one cycle)
    input  wire [1:0]  dev_op_i,       //! READ / WRITE / ERASE_REGION
    input  wire [15:0] dev_len_i,      //! byte count
    input  wire        dev_wvalid_i,   //! write byte present
    output logic       dev_wready_o,   //! responder accepts the write byte
    output logic       dev_rvalid_o,   //! read byte present
    output logic [7:0] dev_rdata_o,    //! read byte -- blank flash is 0xFF
    input  wire        dev_rready_i,   //! initiator accepts the read byte
    output logic       dev_busy_o,     //! command in flight
    output logic       dev_done_o,     //! one-cycle pulse: complete
    output logic       dev_err_o,      //! one-cycle pulse: failed (never)
    output logic       nvm_backed_o    //! CONSTANT 0: no media behind the face
);

  localparam logic [1:0] NVMP_OP_READ_C  = 2'd0;
  localparam logic [1:0] NVMP_OP_WRITE_C = 2'd1;
  //! Deliberately a localparam, not a parameter: the fact is a property of
  //! the logic in this file, and a parameter would let an integrator assert
  //! persistence the fabric does not have.
  localparam logic       NVM_BACKED_C    = 1'b0;

  logic        nvm_gnt_r, nvm_done_r, nvm_rvalid_r, nvm_wready_r;
  logic [15:0] nvm_cnt_r;
  logic        nvm_busy_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      nvm_busy_r   <= 1'b0;
      nvm_gnt_r    <= 1'b0;
      nvm_done_r   <= 1'b0;
      nvm_rvalid_r <= 1'b0;
      nvm_wready_r <= 1'b0;
      nvm_cnt_r    <= 16'd0;
    end else begin
      nvm_gnt_r  <= 1'b0;
      nvm_done_r <= 1'b0;
      if (!nvm_busy_r) begin
        nvm_rvalid_r <= 1'b0;
        nvm_wready_r <= 1'b0;
        if (dev_req_i) begin
          nvm_gnt_r  <= 1'b1;
          nvm_cnt_r  <= dev_len_i;
          nvm_busy_r <= 1'b1;
          // ERASE (and any zero-length command) completes with no data phase
          if ((dev_op_i != NVMP_OP_READ_C && dev_op_i != NVMP_OP_WRITE_C)
              || (dev_len_i == 16'd0)) begin
            nvm_busy_r <= 1'b0;
            nvm_done_r <= 1'b1;
          end else begin
            nvm_rvalid_r <= (dev_op_i == NVMP_OP_READ_C);
            nvm_wready_r <= (dev_op_i == NVMP_OP_WRITE_C);
          end
        end
      end else begin
        // one byte per accepted handshake, blank flash reads as 0xFF
        if ((nvm_rvalid_r & dev_rready_i) | (nvm_wready_r & dev_wvalid_i)) begin
          if (nvm_cnt_r <= 16'd1) begin
            nvm_busy_r   <= 1'b0;
            nvm_rvalid_r <= 1'b0;
            nvm_wready_r <= 1'b0;
            nvm_done_r   <= 1'b1;
          end else begin
            nvm_cnt_r <= nvm_cnt_r - 16'd1;
          end
        end
      end
    end
  end

  assign dev_gnt_o    = nvm_gnt_r;
  assign dev_wready_o = nvm_wready_r;
  assign dev_rvalid_o = nvm_rvalid_r;
  assign dev_rdata_o  = 8'hFF;
  assign dev_busy_o   = nvm_busy_r;
  assign dev_done_o   = nvm_done_r;
  assign dev_err_o    = 1'b0;
  assign nvm_backed_o = NVM_BACKED_C;

endmodule

`default_nettype none

//===========================================================================//
//  AFTER: the section 8 backend candidate                                   //
//===========================================================================//
module KL_nvm_backend_sizer #(
    //! core clock, for the millisecond tick the deadlines count in
    parameter int unsigned CLK_HZ_P       = 125_000_000,
    //! shape: the section 4.2 allocation's per-group occupancy
    parameter int unsigned N_STREAM_IN_P  = 9,
    parameter int unsigned N_STREAM_OUT_P = 9,
    parameter int unsigned N_SPORT_IN_P   = 8,
    parameter int unsigned N_SPORT_OUT_P  = 8,
    parameter int unsigned N_AUDIO_UNIT_P = 1,
    parameter int unsigned N_CLK_DOM_P    = 1,
    parameter int unsigned N_NAME_BANK_P  = 30,
    //! nominal channel-map payload; the per-port prefix table corrects it
    parameter int unsigned MAP_BYTES_P    = 256,
    //! design page section 9.4 deadlines, in milliseconds
    parameter int unsigned T_ALIVE_MS_P   = 2000,
    parameter int unsigned T_COMMIT_MS_P  = 8000
) (
    input  wire         clk_i,          //! core clock
    input  wire         rst_n,          //! synchronous active-low reset

    //! ---- device face: target of KL_pp_nvm_port's initiator ----
    input  wire         dev_req_i,      //! command request
    output logic        dev_gnt_o,      //! command accepted (one cycle)
    input  wire  [1:0]  dev_op_i,       //! READ / WRITE / ERASE_REGION
    input  wire  [7:0]  dev_region_i,   //! region id = F07.8 record_id
    input  wire  [15:0] dev_offset_i,   //! byte offset inside the region
    input  wire  [15:0] dev_len_i,      //! byte count (ERASE: 0 = whole region)
    input  wire         dev_wvalid_i,   //! write byte present
    output logic        dev_wready_o,   //! backend accepts the write byte
    input  wire  [7:0]  dev_wdata_i,    //! write byte
    output logic        dev_rvalid_o,   //! read byte present
    output logic [7:0]  dev_rdata_o,    //! read byte
    input  wire         dev_rready_i,   //! initiator accepts the read byte
    output logic        dev_busy_o,     //! command in flight
    output logic        dev_done_o,     //! one-cycle pulse: complete
    output logic        dev_err_o,      //! one-cycle pulse: failed

    //! ---- main-memory master into the reserved ppmem window (section 8.1) --
    output logic        mem_req_o,      //! held until mem_ack_i
    output logic        mem_we_o,       //! 1 = write, 0 = read
    output logic [31:0] mem_addr_o,     //! word address, byte-aligned
    output logic [31:0] mem_wdata_o,    //! write data, byte replicated
    output logic [3:0]  mem_wstrb_o,    //! write byte enables
    input  wire         mem_ack_i,      //! one-cycle completion
    input  wire  [31:0] mem_rdata_i,    //! read data, valid with mem_ack_i

    //! ---- control CSRs (section 8.2: a control tuple, never a data window) -
    input  wire         csr_sel_i,      //! CSR access
    input  wire         csr_we_i,       //! 1 = write
    input  wire  [5:0]  csr_addr_i,     //! [4:0] register, [5] map prefix table
    input  wire  [31:0] csr_wdata_i,    //! write data
    output logic [31:0] csr_rdata_o,    //! read data

    //! ---- published status (section 9.1) ----
    output logic        nvm_backed_o,   //! live: a writer answered in time
    output logic        nvm_dirty_o,    //! committed changes no slot holds
    output logic        nvm_stale_o,    //! backed was true since reset, is not now
    output logic [3:0]  nvm_verdict_o   //! section 6.2 verdict of the last image
);

  // ---- device-face op codes (2'b11 reserved) -----------------------------
  localparam logic [1:0] OP_READ_C  = 2'd0;
  localparam logic [1:0] OP_WRITE_C = 2'd1;
  localparam logic [1:0] OP_ERASE_C = 2'd2;

  localparam int unsigned REC_HDR_C  = 8;    // F07.8 framing bytes
  localparam int unsigned NAME_BANK_C = 512; // 8 slots x 64 B, section 4.2

  // ---- the section 4.2 id blocks -----------------------------------------
  localparam int unsigned ID_CFG_C   = 'h00;
  localparam int unsigned ID_SUID_C  = 'h01;
  localparam int unsigned ID_RATE_C  = 'h02;
  localparam int unsigned ID_CLKS_C  = 'h0A;
  localparam int unsigned ID_MCR_C   = 'h12;
  localparam int unsigned ID_BIND_C  = 'h20;
  localparam int unsigned ID_FMTI_C  = 'h30;
  localparam int unsigned ID_FMTO_C  = 'h40;
  localparam int unsigned ID_PTOF_C  = 'h50;
  localparam int unsigned ID_MAPI_C  = 'h60;
  localparam int unsigned ID_MAPO_C  = 'h70;
  localparam int unsigned ID_NAME_C  = 'h80;

  // ---- per-group record size, header included ----------------------------
  localparam int unsigned SZ_CFG_C  = REC_HDR_C + 2;
  localparam int unsigned SZ_SUID_C = REC_HDR_C + 8;
  localparam int unsigned SZ_RATE_C = REC_HDR_C + 4;
  localparam int unsigned SZ_CLKS_C = REC_HDR_C + 2;
  localparam int unsigned SZ_MCR_C  = REC_HDR_C + 66;
  localparam int unsigned SZ_BIND_C = REC_HDR_C + 20;
  localparam int unsigned SZ_FMT_C  = REC_HDR_C + 8;
  localparam int unsigned SZ_PTOF_C = REC_HDR_C + 4;
  localparam int unsigned SZ_MAP_C  = REC_HDR_C + MAP_BYTES_P;
  localparam int unsigned SZ_NAME_C = REC_HDR_C + NAME_BANK_C;

  // ---- image byte bases: records are concatenated in ascending record_id --
  localparam int unsigned B_CFG_C  = 0;
  localparam int unsigned B_SUID_C = B_CFG_C  + SZ_CFG_C;
  localparam int unsigned B_RATE_C = B_SUID_C + SZ_SUID_C;
  localparam int unsigned B_CLKS_C = B_RATE_C + N_AUDIO_UNIT_P * SZ_RATE_C;
  localparam int unsigned B_MCR_C  = B_CLKS_C + N_CLK_DOM_P    * SZ_CLKS_C;
  localparam int unsigned B_BIND_C = B_MCR_C  + N_CLK_DOM_P    * SZ_MCR_C;
  localparam int unsigned B_FMTI_C = B_BIND_C + N_STREAM_IN_P  * SZ_BIND_C;
  localparam int unsigned B_FMTO_C = B_FMTI_C + N_STREAM_IN_P  * SZ_FMT_C;
  localparam int unsigned B_PTOF_C = B_FMTO_C + N_STREAM_OUT_P * SZ_FMT_C;
  localparam int unsigned B_MAPI_C = B_PTOF_C + N_STREAM_OUT_P * SZ_PTOF_C;
  localparam int unsigned B_MAPO_C = B_MAPI_C + N_SPORT_IN_P   * SZ_MAP_C;
  localparam int unsigned B_NAME_C = B_MAPO_C + N_SPORT_OUT_P  * SZ_MAP_C;

  // =======================================================================
  //  Region decode: record_id -> {image byte base, record byte length}
  // =======================================================================
  //! per-port channel-map prefix, loaded by firmware: the two map groups are
  //! the only ones whose record length varies with the port, so their base is
  //! a table lookup rather than a constant stride.
  logic [15:0] map_pref_r [0:15];
  logic [15:0] map_len_r  [0:15];

  logic [17:0] rec_base_w;
  logic [11:0] rec_len_w;
  logic        rec_hit_w;
  logic [3:0]  map_idx_w;

  assign map_idx_w = dev_region_i[3:0];

  always_comb begin
    rec_base_w = 18'd0;
    rec_len_w  = 12'd0;
    rec_hit_w  = 1'b0;
    if (dev_region_i == 8'(ID_CFG_C)) begin
      rec_base_w = 18'(B_CFG_C);
      rec_len_w  = 12'(SZ_CFG_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i == 8'(ID_SUID_C)) begin
      rec_base_w = 18'(B_SUID_C);
      rec_len_w  = 12'(SZ_SUID_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_RATE_C)
              && dev_region_i <  8'(ID_RATE_C + N_AUDIO_UNIT_P)) begin
      rec_base_w = 18'(B_RATE_C)
                 + 18'(SZ_RATE_C) * 18'(dev_region_i - 8'(ID_RATE_C));
      rec_len_w  = 12'(SZ_RATE_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_CLKS_C)
              && dev_region_i <  8'(ID_CLKS_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_CLKS_C)
                 + 18'(SZ_CLKS_C) * 18'(dev_region_i - 8'(ID_CLKS_C));
      rec_len_w  = 12'(SZ_CLKS_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_MCR_C)
              && dev_region_i <  8'(ID_MCR_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_MCR_C)
                 + 18'(SZ_MCR_C) * 18'(dev_region_i - 8'(ID_MCR_C));
      rec_len_w  = 12'(SZ_MCR_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_BIND_C)
              && dev_region_i <  8'(ID_BIND_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_BIND_C)
                 + 18'(SZ_BIND_C) * 18'(dev_region_i - 8'(ID_BIND_C));
      rec_len_w  = 12'(SZ_BIND_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_FMTI_C)
              && dev_region_i <  8'(ID_FMTI_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_FMTI_C)
                 + 18'(SZ_FMT_C) * 18'(dev_region_i - 8'(ID_FMTI_C));
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_FMTO_C)
              && dev_region_i <  8'(ID_FMTO_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_FMTO_C)
                 + 18'(SZ_FMT_C) * 18'(dev_region_i - 8'(ID_FMTO_C));
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_PTOF_C)
              && dev_region_i <  8'(ID_PTOF_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_PTOF_C)
                 + 18'(SZ_PTOF_C) * 18'(dev_region_i - 8'(ID_PTOF_C));
      rec_len_w  = 12'(SZ_PTOF_C);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_MAPI_C)
              && dev_region_i <  8'(ID_MAPI_C + N_SPORT_IN_P)) begin
      rec_base_w = 18'(B_MAPI_C) + 18'(map_pref_r[map_idx_w]);
      rec_len_w  = 12'(map_len_r[map_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_MAPO_C)
              && dev_region_i <  8'(ID_MAPO_C + N_SPORT_OUT_P)) begin
      rec_base_w = 18'(B_MAPO_C) + 18'(map_pref_r[map_idx_w]);
      rec_len_w  = 12'(map_len_r[map_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_NAME_C)
              && dev_region_i <  8'(ID_NAME_C + N_NAME_BANK_P)) begin
      rec_base_w = 18'(B_NAME_C)
                 + 18'(SZ_NAME_C) * 18'(dev_region_i - 8'(ID_NAME_C));
      rec_len_w  = 12'(SZ_NAME_C);
      rec_hit_w  = 1'b1;
    end
  end

  // =======================================================================
  //  Control CSRs
  // =======================================================================
  localparam logic [4:0] R_IMG_BASE_C = 5'd0;
  localparam logic [4:0] R_IMG_LEN_C  = 5'd1;
  localparam logic [4:0] R_SEQ_C      = 5'd2;
  localparam logic [4:0] R_STAT_C     = 5'd3;
  localparam logic [4:0] R_ACK_C      = 5'd4;

  logic [31:0] img_base_r;
  logic [31:0] img_len_r;
  logic [31:0] seq_r;
  logic [3:0]  verdict_r;
  logic        backed_r, dirty_r, stale_r, ever_backed_r;
  logic        hb_kick_w, commit_ack_w, commit_start_w, dirty_set_w;

  assign hb_kick_w      = csr_sel_i & csr_we_i & (csr_addr_i[4:0] == R_ACK_C)
                          & ~csr_addr_i[5] & csr_wdata_i[0];
  assign commit_ack_w   = csr_sel_i & csr_we_i & (csr_addr_i[4:0] == R_ACK_C)
                          & ~csr_addr_i[5] & csr_wdata_i[1];
  assign commit_start_w = csr_sel_i & csr_we_i & (csr_addr_i[4:0] == R_ACK_C)
                          & ~csr_addr_i[5] & csr_wdata_i[2];
  assign dirty_set_w    = csr_sel_i & csr_we_i & (csr_addr_i[4:0] == R_ACK_C)
                          & ~csr_addr_i[5] & csr_wdata_i[3];

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      img_base_r <= 32'd0;
      img_len_r  <= 32'd0;
      seq_r      <= 32'd0;
      verdict_r  <= 4'd0;
    end else if (csr_sel_i && csr_we_i && !csr_addr_i[5]) begin
      case (csr_addr_i[4:0])
        R_IMG_BASE_C: img_base_r <= csr_wdata_i;
        R_IMG_LEN_C:  img_len_r  <= csr_wdata_i;
        R_SEQ_C:      seq_r      <= csr_wdata_i;
        R_STAT_C:     verdict_r  <= csr_wdata_i[3:0];
        default:      ;
      endcase
    end
  end

  //! the channel-map prefix table: {length, prefix} per port, firmware-loaded
  always_ff @(posedge clk_i) begin
    if (csr_sel_i && csr_we_i && csr_addr_i[5]) begin
      map_pref_r[csr_addr_i[3:0]] <= csr_wdata_i[15:0];
      map_len_r [csr_addr_i[3:0]] <= csr_wdata_i[31:16];
    end
  end

  always_comb begin
    if (csr_addr_i[5]) begin
      csr_rdata_o = {map_len_r[csr_addr_i[3:0]], map_pref_r[csr_addr_i[3:0]]};
    end else begin
      case (csr_addr_i[4:0])
        R_IMG_BASE_C: csr_rdata_o = img_base_r;
        R_IMG_LEN_C:  csr_rdata_o = img_len_r;
        R_SEQ_C:      csr_rdata_o = seq_r;
        R_STAT_C:     csr_rdata_o = {24'd0, verdict_r, 1'b0, stale_r,
                                     dirty_r, backed_r};
        default:      csr_rdata_o = 32'd0;
      endcase
    end
  end

  // =======================================================================
  //  Deadlines (section 9.4): a millisecond tick and two down-counters
  // =======================================================================
  localparam int unsigned MS_DIV_C = CLK_HZ_P / 1000;

  logic [$clog2(MS_DIV_C)-1:0] ms_div_r;
  logic                        ms_tick_w;
  logic [15:0]                 alive_r;
  logic [15:0]                 commit_r;
  logic                        commit_busy_r;

  assign ms_tick_w = (ms_div_r == '0);

  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_div_r <= $clog2(MS_DIV_C)'(MS_DIV_C - 1);
    else        ms_div_r <= ms_tick_w ? $clog2(MS_DIV_C)'(MS_DIV_C - 1)
                                      : ms_div_r - 1'b1;
  end

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      alive_r       <= 16'd0;
      commit_r      <= 16'd0;
      commit_busy_r <= 1'b0;
      backed_r      <= 1'b0;
      dirty_r       <= 1'b0;
      stale_r       <= 1'b0;
      ever_backed_r <= 1'b0;
    end else begin
      // liveness: the heartbeat re-arms the alive deadline
      if (hb_kick_w) begin
        alive_r       <= 16'(T_ALIVE_MS_P);
        backed_r      <= 1'b1;
        ever_backed_r <= 1'b1;
      end else if (ms_tick_w && (alive_r != 16'd0)) begin
        alive_r <= alive_r - 16'd1;
        if (alive_r == 16'd1) begin
          backed_r <= 1'b0;
          if (ever_backed_r) stale_r <= 1'b1;
        end
      end

      // the commit deadline: armed at start, disarmed by the acknowledgement
      if (commit_start_w) begin
        commit_r      <= 16'(T_COMMIT_MS_P);
        commit_busy_r <= 1'b1;
      end else if (commit_ack_w) begin
        commit_busy_r <= 1'b0;
        dirty_r       <= 1'b0;
      end else if (commit_busy_r && ms_tick_w && (commit_r != 16'd0)) begin
        commit_r <= commit_r - 16'd1;
        if (commit_r == 16'd1) begin
          commit_busy_r <= 1'b0;
          backed_r      <= 1'b0;
          if (ever_backed_r) stale_r <= 1'b1;
        end
      end

      if (dirty_set_w) dirty_r <= 1'b1;
    end
  end

  assign nvm_backed_o  = backed_r;
  assign nvm_dirty_o   = dirty_r;
  //! Section 9.2's recovery rule, and what makes the (backed=1, dirty=0,
  //! stale=1) row of section 9.3 unreachable AT THE READ BOUNDARY rather than
  //! merely brief: once the writer is live again and nothing is outstanding,
  //! the loss has been made good by definition, so the published bit is
  //! masked. The latch keeps the memory; the face never shows the pair.
  assign nvm_stale_o   = stale_r & ~(backed_r & ~dirty_r);
  assign nvm_verdict_o = verdict_r;

  // =======================================================================
  //  The byte pump: device face <-> main memory
  // =======================================================================
  typedef enum logic [2:0] {
    S_IDLE, S_RDFETCH, S_RDHOLD, S_WR, S_ERASE, S_FIN, S_ERR
  } state_e;

  state_e      st_r;
  logic [31:0] addr_r;
  logic [15:0] cnt_r;
  logic [7:0]  rbyte_r;
  logic        gnt_r, done_r, err_r;
  logic [15:0] eff_len_w;

  //! ERASE with len 0 means the whole region
  assign eff_len_w = (dev_op_i == OP_ERASE_C && dev_len_i == 16'd0)
                   ? 16'(rec_len_w) : dev_len_i;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      st_r    <= S_IDLE;
      addr_r  <= 32'd0;
      cnt_r   <= 16'd0;
      rbyte_r <= 8'd0;
      gnt_r   <= 1'b0;
      done_r  <= 1'b0;
      err_r   <= 1'b0;
    end else begin
      gnt_r  <= 1'b0;
      done_r <= 1'b0;
      err_r  <= 1'b0;
      case (st_r)
        S_IDLE: begin
          if (dev_req_i) begin
            gnt_r  <= 1'b1;
            addr_r <= img_base_r + 32'(rec_base_w) + 32'(dev_offset_i);
            cnt_r  <= eff_len_w;
            // refuse an unallocated region, or a span past the record: the
            // port never range-checks record_id, so the backend must
            if (!rec_hit_w
                || ({16'd0, dev_offset_i} + {16'd0, eff_len_w}
                    > 32'(rec_len_w))) begin
              st_r <= S_ERR;
            end else if (eff_len_w == 16'd0) begin
              st_r <= S_FIN;
            end else begin
              case (dev_op_i)
                OP_READ_C:  st_r <= S_RDFETCH;
                OP_WRITE_C: st_r <= S_WR;
                default:    st_r <= S_ERASE;
              endcase
            end
          end
        end
        S_RDFETCH: begin
          if (mem_ack_i) begin
            rbyte_r <= mem_rdata_i[8*addr_r[1:0] +: 8];
            st_r    <= S_RDHOLD;
          end
        end
        S_RDHOLD: begin
          if (dev_rready_i) begin
            addr_r <= addr_r + 32'd1;
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else begin
              cnt_r <= cnt_r - 16'd1;
              st_r  <= S_RDFETCH;
            end
          end
        end
        S_WR: begin
          if (dev_wvalid_i && mem_ack_i) begin
            addr_r <= addr_r + 32'd1;
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else cnt_r <= cnt_r - 16'd1;
          end
        end
        S_ERASE: begin
          if (mem_ack_i) begin
            addr_r <= addr_r + 32'd1;
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else cnt_r <= cnt_r - 16'd1;
          end
        end
        S_FIN: begin
          done_r <= 1'b1;
          st_r   <= S_IDLE;
        end
        default: begin        // S_ERR
          err_r <= 1'b1;
          st_r  <= S_IDLE;
        end
      endcase
    end
  end

  always_comb begin
    mem_req_o   = 1'b0;
    mem_we_o    = 1'b0;
    mem_wdata_o = 32'd0;
    mem_wstrb_o = 4'd0;
    case (st_r)
      S_RDFETCH: mem_req_o = 1'b1;
      S_WR: begin
        mem_req_o   = dev_wvalid_i;
        mem_we_o    = 1'b1;
        mem_wdata_o = {4{dev_wdata_i}};
        mem_wstrb_o = 4'd1 << addr_r[1:0];
      end
      S_ERASE: begin
        mem_req_o   = 1'b1;
        mem_we_o    = 1'b1;
        mem_wdata_o = 32'hFFFF_FFFF;
        mem_wstrb_o = 4'd1 << addr_r[1:0];
      end
      default: ;
    endcase
  end

  assign mem_addr_o   = {addr_r[31:2], 2'b00};
  assign dev_gnt_o    = gnt_r;
  assign dev_wready_o = (st_r == S_WR) & mem_ack_i;
  assign dev_rvalid_o = (st_r == S_RDHOLD);
  assign dev_rdata_o  = rbyte_r;
  assign dev_busy_o   = (st_r != S_IDLE);
  assign dev_done_o   = done_r;
  assign dev_err_o    = err_r;

endmodule

`default_nettype wire

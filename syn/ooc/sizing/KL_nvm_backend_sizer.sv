/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_nvm_backend_sizer.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_FASTCONNECT.md section 8.3)
//
//  Description : AREA SIZING SKETCH, the AFTER half of a before/after pair.
//                The three pieces section 8.3 names -- the region-to-offset
//                decoder, the main-memory access path and the control CSRs --
//                plus the liveness and commit deadline counters of section
//                9.4. The BEFORE half is KL_nvm_blankflash_sizer.sv beside
//                this file (one top per file: DECLFILENAME).
//
//  THIS IS NOT SHIPPING RTL, and it is deliberately NOT under `hdl/`.
//  Nothing instantiates it, `milan_soc.py` does not register it, and
//  `scripts/lint_rtl.py` (which sweeps `hdl/`) does not see it. It exists so
//  the decision record can quote a MEASURED upper bound instead of an
//  estimate. The implementation ticket owns the shipping module, its tests
//  and the post-place delta; this file owns the number.
//
//  IT IS NOT UNCHECKED. tb/verilator/nvm_backend drives this exact source
//  against a byte-exact KLJ2 image emitted by
//  `scripts/check_nvm_record_space.py --emit-record-table`, with `-Wall` and
//  no `-Wno-fatal`, and carries three compiled-in negative controls
//  (NVM_MUT_MAP_ALIAS, NVM_MUT_NOMINAL_STRIDE, NVM_MUT_STALE_MASKONLY), each
//  of which MUST fail.
//
//  Measure with (see syn/yosys/README.md for the toolchain):
//    OOC_CHPARAM="N_STREAM_IN_P=2 N_STREAM_OUT_P=2 N_SPORT_IN_P=1 \
//                 N_SPORT_OUT_P=1 N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1 \
//                 N_NAME_P=31" syn/yosys/ooc.sh KL_nvm_backend_sizer
//    OOC_CHPARAM="N_STREAM_IN_P=9 N_STREAM_OUT_P=9 N_SPORT_IN_P=8 \
//                 N_SPORT_OUT_P=8 N_AUDIO_UNIT_P=1 N_CLK_DOM_P=1 \
//                 N_NAME_P=107" syn/yosys/ooc.sh KL_nvm_backend_sizer
//
//  THERE IS NO NOMINAL CHANNEL-MAP SIZE PARAMETER any more, and its removal
//  is the round-4 repair. A `MAP_BYTES_P` stride priced both channel-map
//  groups at one nominal length and placed the groups after it at multiples
//  of that length. KLJ2 section 6.1 concatenates records with NO padding, and
//  the generated 8x8 overlay is asymmetric -- an input port has 8 clusters
//  (64-byte payload, 72-byte framed record) and an output port has 17
//  (136-byte payload, 144-byte framed record) -- so no single nominal stride
//  can be right for both. Lengths and prefixes are now direction-distinct
//  firmware-loaded state, and every group base after them is the SUM of the
//  actual preceding lengths.
//
//  Stated simplifications, each one an UNDER-count risk named rather than
//  hidden:
//    (a) memory accesses are one byte per handshake -- a write strobe per
//        byte, and a word fetch per read byte -- rather than coalesced into
//        words. That is not a throughput loss: the port itself streams one
//        byte per handshake (KL_pp_nvm_port F02.8), so the memory side is
//        already matched to the source. A coalescing implementation would
//        add a word buffer and a lane mux, so this figure bounds the DECODE
//        and CONTROL cost rather than every possible datapath.
//    (b) the container CRC-32 of section 6 is NOT here. It is the reader's,
//        not the backend's -- the backend moves record bytes between the port
//        and the image; the acceptance order of section 6.2 runs above it.
//---------------------------------------------------------------------------//
`default_nettype none

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
    parameter int unsigned N_NAME_P       = 107,
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
    //! [5] selects the channel-map tables, [4] the DIRECTION inside them
    //! (0 = input group 0x60, 1 = output group 0x70) and [3:0] the port.
    //! With [5] clear, [4:0] is the register index.
    input  wire         csr_sel_i,      //! CSR access
    input  wire         csr_we_i,       //! 1 = write
    input  wire  [5:0]  csr_addr_i,     //! see above
    input  wire  [31:0] csr_wdata_i,    //! write data
    output logic [31:0] csr_rdata_o,    //! read data

    //! ---- published status (section 9.1) ----
    output logic        nvm_backed_o,   //! live: a writer answered in time
    output logic        nvm_dirty_o,    //! committed changes no slot holds
    output logic        nvm_stale_o,    //! a loss that has not been made good
    output logic [3:0]  nvm_verdict_o   //! section 6.2 verdict of the last image
);

  // ---- device-face op codes (2'b11 reserved) -----------------------------
  localparam logic [1:0] OP_READ_C  = 2'd0;
  localparam logic [1:0] OP_WRITE_C = 2'd1;
  localparam logic [1:0] OP_ERASE_C = 2'd2;

  localparam int unsigned REC_HDR_C  = 8;    // F07.8 framing bytes
  localparam int unsigned NAME_C = 64;       // one AEM string, section 4.2

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
  //! The two channel-map groups are absent from this list ON PURPOSE: their
  //! record length is per port, not per group, and lives in the tables below.
  localparam int unsigned SZ_CFG_C  = REC_HDR_C + 2;
  localparam int unsigned SZ_SUID_C = REC_HDR_C + 8;
  localparam int unsigned SZ_RATE_C = REC_HDR_C + 4;
  localparam int unsigned SZ_CLKS_C = REC_HDR_C + 2;
  localparam int unsigned SZ_MCR_C  = REC_HDR_C + 66;
  localparam int unsigned SZ_BIND_C = REC_HDR_C + 20;
  localparam int unsigned SZ_FMT_C  = REC_HDR_C + 8;
  localparam int unsigned SZ_PTOF_C = REC_HDR_C + 4;
  localparam int unsigned SZ_NAME_C = REC_HDR_C + NAME_C;

  // ---- image byte bases: records are concatenated in ascending record_id --
  //! Constant up to the first channel-map group, because every group before it
  //! is fixed-length. Everything after it is derived at run time from the
  //! measured lengths (b_mapo_w, b_name_w below).
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

  // =======================================================================
  //  Region decode: record_id -> {image byte base, record byte length}
  // =======================================================================
  //! Per-port channel-map prefix and length, loaded by firmware, DIRECTION
  //! DISTINCT. An input port and an output port with the same ordinal have
  //! different cluster counts on the shipped 8x8 overlay (8 against 17), so
  //! one table indexed by dev_region_i[3:0] gave both the same length and the
  //! same prefix and read the wrong span for at least one of them. The
  //! prefix is the running sum of the preceding lengths INSIDE the group.
  logic [15:0] mapi_pref_r [0:N_SPORT_IN_P-1];
  logic [15:0] mapi_len_r  [0:N_SPORT_IN_P-1];
  logic [15:0] mapo_pref_r [0:N_SPORT_OUT_P-1];
  logic [15:0] mapo_len_r  [0:N_SPORT_OUT_P-1];

  localparam int unsigned MAPI_IW_C = (N_SPORT_IN_P  > 1)
                                    ? $clog2(N_SPORT_IN_P)  : 1;
  localparam int unsigned MAPO_IW_C = (N_SPORT_OUT_P > 1)
                                    ? $clog2(N_SPORT_OUT_P) : 1;

  logic [17:0] rec_base_w;
  logic [11:0] rec_len_w;
  logic        rec_hit_w;
  logic [MAPI_IW_C-1:0] mapi_idx_w;
  logic [MAPO_IW_C-1:0] mapo_idx_w;
  logic [17:0] b_mapo_w, b_name_w;

  //! Only ever consumed inside the guarded branch that proves the id is in
  //! the group, so a truncated value outside it cannot reach an output.
  assign mapi_idx_w = MAPI_IW_C'(dev_region_i - 8'(ID_MAPI_C));
  assign mapo_idx_w = MAPO_IW_C'(dev_region_i - 8'(ID_MAPO_C));

`ifdef NVM_MUT_NOMINAL_STRIDE
  //! NEGATIVE CONTROL, never synthesised: the round-3 base arithmetic, which
  //! advanced past each channel-map group by a NOMINAL stride instead of the
  //! sum of the group's actual record lengths. KLJ2 6.1 forbids the padding
  //! that would make it right.
  localparam int unsigned MUT_MAP_NOM_C = REC_HDR_C + 256;
  assign b_mapo_w = 18'(B_MAPI_C) + 18'(N_SPORT_IN_P  * MUT_MAP_NOM_C);
  assign b_name_w = b_mapo_w      + 18'(N_SPORT_OUT_P * MUT_MAP_NOM_C);
`else
  //! A group base is the SUM of the preceding group's actual record lengths.
  //! The running prefix already carries that sum, so the span of a group is
  //! its last port's prefix plus that port's length: one adder, and it cannot
  //! disagree with the table the decode reads.
  assign b_mapo_w = 18'(B_MAPI_C)
                  + 18'(mapi_pref_r[MAPI_IW_C'(N_SPORT_IN_P  - 1)])
                  + 18'(mapi_len_r [MAPI_IW_C'(N_SPORT_IN_P  - 1)]);
  assign b_name_w = b_mapo_w
                  + 18'(mapo_pref_r[MAPO_IW_C'(N_SPORT_OUT_P - 1)])
                  + 18'(mapo_len_r [MAPO_IW_C'(N_SPORT_OUT_P - 1)]);
`endif

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
      rec_base_w = 18'(B_MAPI_C) + 18'(mapi_pref_r[mapi_idx_w]);
      rec_len_w  = 12'(mapi_len_r[mapi_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_MAPO_C)
              && dev_region_i <  8'(ID_MAPO_C + N_SPORT_OUT_P)) begin
`ifdef NVM_MUT_MAP_ALIAS
      //! NEGATIVE CONTROL, never synthesised: the round-3 decode indexed ONE
      //! {prefix,length} table with dev_region_i[3:0], so 0x60+k and 0x70+k
      //! read the same entry even though an input port is 72 framed bytes on
      //! the shipped 8x8 overlay and an output port is 144.
      rec_base_w = b_mapo_w + 18'(mapi_pref_r[MAPI_IW_C'(mapo_idx_w)]);
      rec_len_w  = 12'(mapi_len_r[MAPI_IW_C'(mapo_idx_w)]);
`else
      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]);
      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);
`endif
      rec_hit_w  = 1'b1;
    end else if (dev_region_i >= 8'(ID_NAME_C)
              && dev_region_i <  8'(ID_NAME_C + N_NAME_P)) begin
      rec_base_w = b_name_w
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

  //! The two channel-map tables: {length, prefix} per port and per direction,
  //! firmware-loaded. csr_addr_i[4] picks the direction.
  always_ff @(posedge clk_i) begin
    if (csr_sel_i && csr_we_i && csr_addr_i[5]) begin
      if (!csr_addr_i[4]) begin
        if (32'(csr_addr_i[3:0]) < 32'(N_SPORT_IN_P)) begin
          mapi_pref_r[MAPI_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
          mapi_len_r [MAPI_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
        end
      end else begin
        if (32'(csr_addr_i[3:0]) < 32'(N_SPORT_OUT_P)) begin
          mapo_pref_r[MAPO_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[15:0];
          mapo_len_r [MAPO_IW_C'(csr_addr_i[3:0])] <= csr_wdata_i[31:16];
        end
      end
    end
  end

  always_comb begin
    if (csr_addr_i[5]) begin
      if (!csr_addr_i[4]) begin
        csr_rdata_o = {mapi_len_r [MAPI_IW_C'(csr_addr_i[3:0])],
                       mapi_pref_r[MAPI_IW_C'(csr_addr_i[3:0])]};
      end else begin
        csr_rdata_o = {mapo_len_r [MAPO_IW_C'(csr_addr_i[3:0])],
                       mapo_pref_r[MAPO_IW_C'(csr_addr_i[3:0])]};
      end
    end else begin
      case (csr_addr_i[4:0])
        R_IMG_BASE_C: csr_rdata_o = img_base_r;
        R_IMG_LEN_C:  csr_rdata_o = img_len_r;
        R_SEQ_C:      csr_rdata_o = seq_r;
        R_STAT_C:     csr_rdata_o = {24'd0, verdict_r, 1'b0, nvm_stale_o,
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

  // -----------------------------------------------------------------------
  //  Section 9.2, as ONE next-state function with the priorities written out.
  //
  //  Round 3 set `stale_r` on a loss and cleared it only by reset, masking
  //  the published bit with (backed & !dirty). The mask made a clean recovery
  //  LOOK repaired while the latch still remembered the outage, so the very
  //  next ordinary controller change -- setting dirty -- lifted the mask and
  //  republished stale=1 with no new loss. A historical outage contaminated
  //  every later commit. The latch itself is now cleared by the recovery
  //  condition, which is what section 9.2 always said.
  // -----------------------------------------------------------------------
  logic alive_exp_w, commit_exp_w, loss_w;
  logic backed_n_w, dirty_n_w, stale_n_w;

  //! A deadline expires on the tick that would take it from 1 to 0. A
  //! heartbeat re-arms the liveness deadline instead of letting it expire;
  //! a start or an acknowledgement preempts the commit deadline.
  assign alive_exp_w  = ms_tick_w & (alive_r == 16'd1) & ~hb_kick_w;
  assign commit_exp_w = commit_busy_r & ms_tick_w & (commit_r == 16'd1)
                        & ~commit_start_w & ~commit_ack_w;

  //! A LOSS is either deadline expiring after a writer had once been live.
  //! A build that never had a writer is the honest (0,*,0) "never backed"
  //! state and is not stale.
  assign loss_w = (alive_exp_w | commit_exp_w) & ever_backed_r;

  //! PRIORITY, stated rather than left to statement order: a loss in the same
  //! cycle as a heartbeat wins: the heartbeat proves the writer answered at
  //! some point, not that the deadline had not already lapsed.
  assign backed_n_w = (alive_exp_w | commit_exp_w) ? 1'b0
                    : hb_kick_w                    ? 1'b1
                                                   : backed_r;

  //! PRIORITY: a change accepted in the same cycle as the acknowledgement
  //! wins, so a controller SET landing on the commit boundary is never lost.
  assign dirty_n_w  = dirty_set_w  ? 1'b1
                    : commit_ack_w ? 1'b0
                                   : dirty_r;

`ifdef NVM_MUT_STALE_MASKONLY
  //! NEGATIVE CONTROL, never synthesised: round 3's keep-the-latch machine.
  assign stale_n_w   = loss_w ? 1'b1 : stale_r;
  assign nvm_stale_o = stale_r & ~(backed_r & ~dirty_r);
`else
  //! RECOVERY, evaluated on the NEXT values so the clear is atomic with the
  //! event that earns it: the writer is live again AND nothing is
  //! outstanding. A new loss in the same cycle wins, and because a loss also
  //! forces backed_n_w to 0 the two arms can never both be taken.
  //!
  //! This makes (backed=1, dirty=0, stale=1) unreachable in the STATE rather
  //! than merely masked at the face: stale_r can only be 1 if the previous
  //! cycle took the loss arm (which drove backed_n_w to 0) or held the latch
  //! (which requires backed_n_w=0 or dirty_n_w=1). No mask is needed, and
  //! none is applied.
  assign stale_n_w   = loss_w                    ? 1'b1
                     : (backed_n_w & ~dirty_n_w) ? 1'b0
                                                 : stale_r;
  assign nvm_stale_o = stale_r;
`endif

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
        ever_backed_r <= 1'b1;
      end else if (ms_tick_w && (alive_r != 16'd0)) begin
        alive_r <= alive_r - 16'd1;
      end

      // the commit deadline: armed at start, disarmed by the acknowledgement
      if (commit_start_w) begin
        commit_r      <= 16'(T_COMMIT_MS_P);
        commit_busy_r <= 1'b1;
      end else if (commit_ack_w) begin
        commit_busy_r <= 1'b0;
      end else if (commit_busy_r && ms_tick_w && (commit_r != 16'd0)) begin
        commit_r <= commit_r - 16'd1;
        if (commit_r == 16'd1) commit_busy_r <= 1'b0;
      end

      backed_r <= backed_n_w;
      dirty_r  <= dirty_n_w;
      stale_r  <= stale_n_w;
    end
  end

  assign nvm_backed_o  = backed_r;
  assign nvm_dirty_o   = dirty_r;
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

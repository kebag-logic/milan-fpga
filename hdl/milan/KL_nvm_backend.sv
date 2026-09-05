/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_nvm_backend.sv
//  Project     : Milan FPGA -- saved state and fast connect
//                (docs/design/SAVED_STATE_FASTCONNECT.md sections 4, 8, 9)
//
//  Description : THE DEVICE BEHIND THE PROCESSOR'S NVM PORT. KL_pp_nvm_port
//                (protocol-processor) frames one F07.8 record per operation
//                and streams it one byte per handshake toward a device face;
//                this module is that device. It keeps the persisted record
//                image in the reserved main-memory window (section 8.1), so a
//                record READ fetches bytes from the image, a WRITE stores them
//                and an ERASE fills the record's span with 0xFF. Nothing here
//                touches flash: the media is owned by firmware through the
//                LiteSPI master that already exists (section 3), and what
//                crosses the CSR face is the control tuple of section 8.2 --
//                the image base and length, the sequence number, the verdict
//                of the last slot the firmware validated, the heartbeat and
//                the commit bracket -- never record data.
//
//                WHERE A RECORD IS. record_id is decoded to an image byte
//                offset by the section 4.2 allocation: fixed blocks for the
//                fixed-length groups, and for the two channel-map groups a
//                per-port, per-direction {prefix, length} table the firmware
//                loads from the same overlay the descriptor image came from
//                (an input port and an output port of one ordinal carry
//                different cluster counts on the shipped 8x8 overlay, 8 and
//                17, so the two directions never share a table). Every group
//                after the channel maps sits at the SUM of the actual
//                preceding lengths, because KLJ2 section 6.1 concatenates
//                records with no padding.
//
//                WHAT IT DOES BEFORE FIRMWARE ARRIVES. Until the firmware has
//                written a non-zero image length, this module answers exactly
//                as the blank-flash responder it replaces did: reads return
//                0xFF, writes are accepted and discarded, erase completes. So
//                a build whose firmware has no writer yet behaves as today,
//                and PP_STAT keeps telling the truth about it (nvm_backed
//                stays 0). Once configured, a READ still answers 0xFF until
//                the firmware has marked the image VALID -- the section 6.2
//                acceptance order runs in firmware over the slot it copied
//                into the window, and a record must never be restored out of
//                an image nobody validated -- while WRITE and ERASE always
//                reach the image, because the processor commits records at
//                runtime and the firmware wraps them into a container later.
//
//                WHAT IT MAY CLAIM. nvm_backed_o is fabric-derived evidence
//                and never a knob: it sets on a firmware heartbeat or a
//                completed transaction, re-arms T-NVM-WRITER-ALIVE on each,
//                and is revoked when that deadline or T-NVM-COMMIT-TIMEOUT
//                expires. nvm_dirty_o says the image holds changes no slot
//                holds; nvm_stale_o says a loss has not been made good. The
//                three follow the next-state function of section 9.2 with
//                its two priorities written out, and section 9.3's
//                (backed=1, dirty=0, stale=1) row is unreachable in the state.
//
//                THE MEMORY FACE is the same contract as the response-buffer
//                master beside it (protocol_processor_top's banner): one
//                outstanding read burst of 64-bit beats carrying their lowest
//                byte address in bits [63:56] (big-endian lanes), and one
//                outstanding single-beat write, 8-byte aligned, strobe bit n
//                enabling byte n, committed by a one-cycle wr_done pulse
//                that may follow wr_ready in the same cycle (a posted bridge)
//                or any later one (an acknowledged bridge). A read fetches
//                the word that holds the byte and keeps it until the byte
//                stream leaves the word or anything writes, so consecutive
//                bytes of one record cost one bus read per eight.
//
//  Refusals    : an unallocated record_id, a span past the record, a span
//                past the configured image and a bus error each end the
//                operation with one dev_err pulse and no further traffic.
//                The port never range-checks record_id against its region
//                (design page section 13), so this module does.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_nvm_backend #(
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
    input  wire         dev_req_i,      //! command request, held until dev_gnt_o
    output logic        dev_gnt_o,      //! command accepted (one cycle)
    input  wire  [1:0]  dev_op_i,       //! READ / WRITE / ERASE_REGION
    input  wire  [7:0]  dev_region_i,   //! region id = F07.8 record_id
    input  wire  [15:0] dev_offset_i,   //! byte offset inside the record
    input  wire  [15:0] dev_len_i,      //! byte count (ERASE: 0 = whole record)
    input  wire         dev_wvalid_i,   //! write byte present
    output logic        dev_wready_o,   //! this module accepts the write byte
    input  wire  [7:0]  dev_wdata_i,    //! write byte
    output logic        dev_rvalid_o,   //! read byte present
    output logic [7:0]  dev_rdata_o,    //! read byte
    input  wire         dev_rready_i,   //! initiator accepts the read byte
    output logic        dev_busy_o,     //! command in flight
    output logic        dev_done_o,     //! one-cycle pulse: complete
    output logic        dev_err_o,      //! one-cycle pulse: failed

    //! ---- main-memory master into the reserved ppmem window (section 8.1) --
    //! Same contract as the response-buffer master: see the banner.
    output logic        mem_req_valid_o,  //! read request, held until ready
    input  wire         mem_req_ready_i,  //! bridge accepts the request
    output logic [31:0] mem_req_addr_o,   //! byte address, 8-byte aligned
    output logic [8:0]  mem_req_beats_o,  //! 64-bit beats in the burst (1)
    input  wire         mem_rsp_valid_i,  //! response beat present
    output logic        mem_rsp_ready_o,  //! this module takes the beat
    input  wire  [63:0] mem_rsp_data_i,   //! beat data, big-endian byte lane
    input  wire         mem_rsp_last_i,   //! final beat of the burst
    input  wire         mem_rsp_err_i,    //! read failed -- abort the op
    output logic        mem_wr_valid_o,   //! write presented, held until ready
    input  wire         mem_wr_ready_i,   //! bridge accepts the write
    output logic [31:0] mem_wr_addr_o,    //! byte address, 8-byte aligned
    output logic [63:0] mem_wr_data_o,    //! lane data (byte replicated)
    output logic [7:0]  mem_wr_strb_o,    //! per-byte enable, bit n = byte n
    input  wire         mem_wr_done_i,    //! write committed (one-cycle pulse)
    input  wire         mem_wr_err_i,     //! ... and it failed

    //! ---- control CSRs (section 8.2: a control tuple, never a data window) -
    //! [5] selects the channel-map tables, [4] the DIRECTION inside them
    //! (0 = input group 0x60, 1 = output group 0x70) and [3:0] the port.
    //! With [5] clear, [4:0] is the register index (R_* below).
    input  wire         csr_sel_i,      //! CSR access
    input  wire         csr_we_i,       //! 1 = write
    input  wire  [5:0]  csr_addr_i,     //! see above
    input  wire  [31:0] csr_wdata_i,    //! write data
    output logic [31:0] csr_rdata_o,    //! read data

    //! ---- fabric evidence ----
    input  wire         change_i,       //! a persisted field moved (aecp_dyn_dirty)

    //! ---- published status (section 9.1) ----
    output logic        nvm_backed_o,   //! live: a writer answered in time
    output logic        nvm_dirty_o,    //! committed changes no slot holds
    output logic        nvm_stale_o,    //! a loss that has not been made good
    output logic [3:0]  nvm_verdict_o,  //! section 6.2 verdict of the last image
    output logic        img_valid_o     //! firmware validated the image in the window
);

  // ---- device-face op codes (2'b11 reserved) -----------------------------
  localparam logic [1:0] OP_READ_C  = 2'd0;
  localparam logic [1:0] OP_WRITE_C = 2'd1;
  localparam logic [1:0] OP_ERASE_C = 2'd2;

  localparam int unsigned REC_HDR_C = 8;     // F07.8 framing bytes
  localparam int unsigned NAME_C    = 64;    // one AEM string, section 4.2

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
  //! loaded lengths (b_mapo_w, b_name_w below).
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

  //! The id comparisons run in 9 bits: a block that ends exactly at 0x100
  //! (128 names) must not wrap to 0 and vanish, which an 8-bit sum would do.
  localparam int unsigned IDW_C = 9;

  // =======================================================================
  //  Region decode: record_id -> {image byte base, record byte length}
  // =======================================================================
  //! Per-port channel-map prefix and length, loaded by firmware, DIRECTION
  //! DISTINCT (see the banner). The prefix is the running sum of the
  //! preceding lengths INSIDE the group.
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
  logic [IDW_C-1:0] region_w;

  assign region_w = {1'b0, dev_region_i};

  //! Only ever consumed inside the guarded branch that proves the id is in
  //! the group, so a truncated value outside it cannot reach an output.
  assign mapi_idx_w = MAPI_IW_C'(dev_region_i - 8'(ID_MAPI_C));
  assign mapo_idx_w = MAPO_IW_C'(dev_region_i - 8'(ID_MAPO_C));

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

  always_comb begin
    rec_base_w = 18'd0;
    rec_len_w  = 12'd0;
    rec_hit_w  = 1'b0;
    if (region_w == IDW_C'(ID_CFG_C)) begin
      rec_base_w = 18'(B_CFG_C);
      rec_len_w  = 12'(SZ_CFG_C);
      rec_hit_w  = 1'b1;
    end else if (region_w == IDW_C'(ID_SUID_C)) begin
      rec_base_w = 18'(B_SUID_C);
      rec_len_w  = 12'(SZ_SUID_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_RATE_C)
              && region_w <  IDW_C'(ID_RATE_C + N_AUDIO_UNIT_P)) begin
      rec_base_w = 18'(B_RATE_C) + 18'(dev_region_i - 8'(ID_RATE_C)) * 18'(SZ_RATE_C);
      rec_len_w  = 12'(SZ_RATE_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_CLKS_C)
              && region_w <  IDW_C'(ID_CLKS_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_CLKS_C) + 18'(dev_region_i - 8'(ID_CLKS_C)) * 18'(SZ_CLKS_C);
      rec_len_w  = 12'(SZ_CLKS_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MCR_C)
              && region_w <  IDW_C'(ID_MCR_C + N_CLK_DOM_P)) begin
      rec_base_w = 18'(B_MCR_C) + 18'(dev_region_i - 8'(ID_MCR_C)) * 18'(SZ_MCR_C);
      rec_len_w  = 12'(SZ_MCR_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_BIND_C)
              && region_w <  IDW_C'(ID_BIND_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_BIND_C) + 18'(dev_region_i - 8'(ID_BIND_C)) * 18'(SZ_BIND_C);
      rec_len_w  = 12'(SZ_BIND_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_FMTI_C)
              && region_w <  IDW_C'(ID_FMTI_C + N_STREAM_IN_P)) begin
      rec_base_w = 18'(B_FMTI_C) + 18'(dev_region_i - 8'(ID_FMTI_C)) * 18'(SZ_FMT_C);
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_FMTO_C)
              && region_w <  IDW_C'(ID_FMTO_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_FMTO_C) + 18'(dev_region_i - 8'(ID_FMTO_C)) * 18'(SZ_FMT_C);
      rec_len_w  = 12'(SZ_FMT_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_PTOF_C)
              && region_w <  IDW_C'(ID_PTOF_C + N_STREAM_OUT_P)) begin
      rec_base_w = 18'(B_PTOF_C) + 18'(dev_region_i - 8'(ID_PTOF_C)) * 18'(SZ_PTOF_C);
      rec_len_w  = 12'(SZ_PTOF_C);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MAPI_C)
              && region_w <  IDW_C'(ID_MAPI_C + N_SPORT_IN_P)) begin
      rec_base_w = 18'(B_MAPI_C) + 18'(mapi_pref_r[mapi_idx_w]);
      rec_len_w  = 12'(mapi_len_r[mapi_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_MAPO_C)
              && region_w <  IDW_C'(ID_MAPO_C + N_SPORT_OUT_P)) begin
      rec_base_w = b_mapo_w + 18'(mapo_pref_r[mapo_idx_w]);
      rec_len_w  = 12'(mapo_len_r[mapo_idx_w]);
      rec_hit_w  = 1'b1;
    end else if (region_w >= IDW_C'(ID_NAME_C)
              && region_w <  IDW_C'(ID_NAME_C + N_NAME_P)) begin
      rec_base_w = b_name_w + 18'(dev_region_i - 8'(ID_NAME_C)) * 18'(SZ_NAME_C);
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
  logic        img_valid_r;
  logic        backed_r, dirty_r, stale_r, ever_backed_r;
  logic        reg_we_w, hb_kick_w, commit_ack_w, commit_start_w;
  logic        img_cfg_w, img_live_w, write_commit_w, dirty_set_w;

  assign reg_we_w       = csr_sel_i & csr_we_i & ~csr_addr_i[5];
  assign hb_kick_w      = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[0];
  assign commit_ack_w   = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[1];
  assign commit_start_w = reg_we_w & (csr_addr_i[4:0] == R_ACK_C) & csr_wdata_i[2];
  //! Configured: the firmware has told this module where the image is. Live:
  //! configured AND validated, the only state in which a READ may serve image
  //! bytes rather than blank flash.
  assign img_cfg_w  = (img_len_r != 32'd0);
  assign img_live_w = img_cfg_w & img_valid_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      img_base_r  <= 32'd0;
      img_len_r   <= 32'd0;
      seq_r       <= 32'd0;
      verdict_r   <= 4'd0;
      img_valid_r <= 1'b0;
    end else if (reg_we_w) begin
      case (csr_addr_i[4:0])
        //! moving the image invalidates whatever validation the old one had
        R_IMG_BASE_C: begin img_base_r <= csr_wdata_i; img_valid_r <= 1'b0; end
        R_IMG_LEN_C:  begin img_len_r  <= csr_wdata_i; img_valid_r <= 1'b0; end
        R_SEQ_C:      seq_r <= csr_wdata_i;
        //! [3:0] the section 6.2 verdict of the image the firmware last
        //! offered, [4] whether that image is the one in the window and it
        //! passed: the firmware's statement, published as evidence only
        R_STAT_C:     begin verdict_r <= csr_wdata_i[3:0]; img_valid_r <= csr_wdata_i[4]; end
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

  logic commit_busy_r;
  logic dev_busy_w;

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
        //! the status word: verdict, the commit bracket, the three section 9
        //! bits, the image's configured/valid state and the device face
        R_STAT_C:     csr_rdata_o = {16'd0, verdict_r, 1'b0, commit_busy_r,
                                     nvm_stale_o, dirty_r, img_valid_r,
                                     backed_r, img_cfg_w, dev_busy_w, 4'd0};
        default:      csr_rdata_o = 32'd0;
      endcase
    end
  end

  // =======================================================================
  //  Deadlines (section 9.4): a millisecond tick and two down-counters
  // =======================================================================
  localparam int unsigned MS_DIV_C = (CLK_HZ_P >= 1000) ? CLK_HZ_P / 1000 : 1;
  localparam int unsigned MS_W_C   = (MS_DIV_C > 1) ? $clog2(MS_DIV_C) : 1;

  logic [MS_W_C-1:0] ms_div_r;
  logic              ms_tick_w;
  logic [15:0]       alive_r;
  logic [15:0]       commit_r;

  assign ms_tick_w = (ms_div_r == '0);

  always_ff @(posedge clk_i) begin
    if (!rst_n) ms_div_r <= MS_W_C'(MS_DIV_C - 1);
    else        ms_div_r <= ms_tick_w ? MS_W_C'(MS_DIV_C - 1) : ms_div_r - 1'b1;
  end

  // -----------------------------------------------------------------------
  //  Section 9.2, as ONE next-state function with the priorities written out.
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

  //! PRIORITY: a loss in the same cycle as a heartbeat wins: the heartbeat
  //! proves the writer answered at some point, not that the deadline had not
  //! already lapsed.
  assign backed_n_w = (alive_exp_w | commit_exp_w) ? 1'b0
                    : hb_kick_w                    ? 1'b1
                                                   : backed_r;

  //! A change is ACCEPTED when the processor reports a persisted field moved
  //! or when it commits a record into the image (or into the void, before
  //! the image is configured -- accepted is accepted). PRIORITY: a change in
  //! the same cycle as the acknowledgement wins, so a controller SET landing
  //! on the commit boundary is never lost.
  assign dirty_set_w = change_i | write_commit_w;
  assign dirty_n_w   = dirty_set_w  ? 1'b1
                     : commit_ack_w ? 1'b0
                                    : dirty_r;

  //! RECOVERY, evaluated on the NEXT values so the clear is atomic with the
  //! event that earns it: the writer is live again AND nothing is
  //! outstanding. A new loss in the same cycle wins, and because a loss also
  //! forces backed_n_w to 0 the two arms can never both be taken. This makes
  //! (backed=1, dirty=0, stale=1) unreachable in the STATE rather than merely
  //! masked at the face; no mask is applied.
  assign stale_n_w = loss_w                    ? 1'b1
                   : (backed_n_w & ~dirty_n_w) ? 1'b0
                                               : stale_r;

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
  assign nvm_stale_o   = stale_r;
  assign nvm_verdict_o = verdict_r;
  assign img_valid_o   = img_valid_r;

  // =======================================================================
  //  The byte pump: device face <-> main memory
  // =======================================================================
  typedef enum logic [3:0] {
    S_IDLE,     // wait for a command
    S_RDBLANK,  // READ with no live image: stream 0xFF, no memory traffic
    S_RDFETCH,  // READ: request the word that holds the byte
    S_RDWAIT,   // READ: wait for the beat
    S_RDHOLD,   // READ: present the byte until the initiator takes it
    S_WTAKE,    // WRITE: wait for the initiator's byte
    S_WREQ,     // WRITE: present the single-beat write until accepted
    S_WDONE,    // WRITE: wait for the commit pulse
    S_WDISCARD, // WRITE with no configured image: accept and discard
    S_EREQ,     // ERASE: present one 0xFF byte write
    S_EDONE,    // ERASE: wait for its commit pulse
    S_FIN,      // pulse done
    S_ERR       // pulse err
  } state_e;

  state_e      st_r;
  logic [31:0] addr_r;
  logic [15:0] cnt_r;
  logic [7:0]  byte_r;
  logic        gnt_r, done_r, err_r, was_write_r;
  logic [15:0] eff_len_w;
  logic [31:0] span_end_w;
  logic        span_ok_w;
  //! the word cache: one fetched 64-bit beat and the address it came from
  logic        wc_valid_r;
  logic [28:0] wc_addr_r;
  logic [63:0] wc_data_r;
  logic        wc_hit_w;

  //! ERASE with len 0 means the whole record
  assign eff_len_w = (dev_op_i == OP_ERASE_C && dev_len_i == 16'd0)
                   ? 16'(rec_len_w) : dev_len_i;
  //! the span must fit the record AND the configured image
  assign span_end_w = 32'(rec_base_w) + 32'(dev_offset_i) + 32'(eff_len_w);
  assign span_ok_w  = rec_hit_w
                    && ({16'd0, dev_offset_i} + {16'd0, eff_len_w} <= 32'(rec_len_w))
                    && (span_end_w <= img_len_r);
  assign wc_hit_w   = wc_valid_r && (wc_addr_r == addr_r[31:3]);
  assign write_commit_w = done_r & was_write_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      st_r        <= S_IDLE;
      addr_r      <= 32'd0;
      cnt_r       <= 16'd0;
      byte_r      <= 8'd0;
      gnt_r       <= 1'b0;
      done_r      <= 1'b0;
      err_r       <= 1'b0;
      was_write_r <= 1'b0;
      wc_valid_r  <= 1'b0;
      wc_addr_r   <= 29'd0;
      wc_data_r   <= 64'd0;
    end else begin
      gnt_r  <= 1'b0;
      done_r <= 1'b0;
      err_r  <= 1'b0;
      //! a moved image makes every cached word a word of another image
      if (reg_we_w && (csr_addr_i[4:0] == R_IMG_BASE_C)) wc_valid_r <= 1'b0;
      case (st_r)
        S_IDLE: begin
          if (dev_req_i) begin
            gnt_r       <= 1'b1;
            addr_r      <= img_base_r + 32'(rec_base_w) + 32'(dev_offset_i);
            cnt_r       <= eff_len_w;
            was_write_r <= (dev_op_i == OP_WRITE_C);
            if (!img_cfg_w) begin
              //! no image yet: the blank-flash responder's exact behaviour
              if (dev_op_i == OP_READ_C && dev_len_i != 16'd0)       st_r <= S_RDBLANK;
              else if (dev_op_i == OP_WRITE_C && dev_len_i != 16'd0) st_r <= S_WDISCARD;
              else                                                    st_r <= S_FIN;
            end else if (!span_ok_w) begin
              //! the port never range-checks record_id; this module must
              st_r <= S_ERR;
            end else if (eff_len_w == 16'd0) begin
              st_r <= S_FIN;
            end else begin
              case (dev_op_i)
                OP_READ_C:  st_r <= img_live_w ? S_RDFETCH : S_RDBLANK;
                OP_WRITE_C: begin st_r <= S_WTAKE; wc_valid_r <= 1'b0; end
                default:    begin st_r <= S_EREQ;  wc_valid_r <= 1'b0; end
              endcase
            end
          end
        end
        S_RDBLANK: begin
          if (dev_rready_i) begin
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else                cnt_r <= cnt_r - 16'd1;
          end
        end
        S_RDFETCH: begin
          if (wc_hit_w) begin
            byte_r <= wc_data_r[63 - 8 * addr_r[2:0] -: 8];
            st_r   <= S_RDHOLD;
          end else if (mem_req_ready_i) begin
            st_r <= S_RDWAIT;
          end
        end
        S_RDWAIT: begin
          if (mem_rsp_valid_i) begin
            if (mem_rsp_err_i) begin
              wc_valid_r <= 1'b0;
              st_r       <= S_ERR;
            end else if (mem_rsp_last_i) begin
              //! the single beat of the burst: cache it and serve the byte
              wc_valid_r <= 1'b1;
              wc_addr_r  <= addr_r[31:3];
              wc_data_r  <= mem_rsp_data_i;
              byte_r     <= mem_rsp_data_i[63 - 8 * addr_r[2:0] -: 8];
              st_r       <= S_RDHOLD;
            end
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
        S_WTAKE: begin
          if (dev_wvalid_i) begin
            byte_r <= dev_wdata_i;
            st_r   <= S_WREQ;
          end
        end
        S_WREQ: begin
          if (mem_wr_ready_i) begin
            //! a posted bridge commits in the same cycle it accepts
            if (mem_wr_done_i) begin
              if (mem_wr_err_i) st_r <= S_ERR;
              else begin
                addr_r <= addr_r + 32'd1;
                if (cnt_r <= 16'd1) st_r <= S_FIN;
                else begin cnt_r <= cnt_r - 16'd1; st_r <= S_WTAKE; end
              end
            end else begin
              st_r <= S_WDONE;
            end
          end
        end
        S_WDONE: begin
          if (mem_wr_done_i) begin
            if (mem_wr_err_i) st_r <= S_ERR;
            else begin
              addr_r <= addr_r + 32'd1;
              if (cnt_r <= 16'd1) st_r <= S_FIN;
              else begin cnt_r <= cnt_r - 16'd1; st_r <= S_WTAKE; end
            end
          end
        end
        S_WDISCARD: begin
          if (dev_wvalid_i) begin
            if (cnt_r <= 16'd1) st_r <= S_FIN;
            else                cnt_r <= cnt_r - 16'd1;
          end
        end
        S_EREQ: begin
          if (mem_wr_ready_i) begin
            if (mem_wr_done_i) begin
              if (mem_wr_err_i) st_r <= S_ERR;
              else begin
                addr_r <= addr_r + 32'd1;
                if (cnt_r <= 16'd1) st_r <= S_FIN;
                else                cnt_r <= cnt_r - 16'd1;
              end
            end else begin
              st_r <= S_EDONE;
            end
          end
        end
        S_EDONE: begin
          if (mem_wr_done_i) begin
            if (mem_wr_err_i) st_r <= S_ERR;
            else begin
              addr_r <= addr_r + 32'd1;
              if (cnt_r <= 16'd1) st_r <= S_FIN;
              else begin cnt_r <= cnt_r - 16'd1; st_r <= S_EREQ; end
            end
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

  //! the memory face, driven from the state alone
  assign mem_req_valid_o = (st_r == S_RDFETCH) && !wc_hit_w;
  assign mem_req_addr_o  = {addr_r[31:3], 3'b000};
  assign mem_req_beats_o = 9'd1;
  assign mem_rsp_ready_o = (st_r == S_RDWAIT);
  assign mem_wr_valid_o  = (st_r == S_WREQ) || (st_r == S_EREQ);
  assign mem_wr_addr_o   = {addr_r[31:3], 3'b000};
  assign mem_wr_data_o   = (st_r == S_EREQ) ? {64{1'b1}} : {8{byte_r}};
  assign mem_wr_strb_o   = 8'd1 << addr_r[2:0];

  //! the device face
  assign dev_busy_w   = (st_r != S_IDLE);
  assign dev_gnt_o    = gnt_r;
  assign dev_wready_o = (st_r == S_WTAKE) || (st_r == S_WDISCARD);
  assign dev_rvalid_o = (st_r == S_RDHOLD) || (st_r == S_RDBLANK);
  assign dev_rdata_o  = (st_r == S_RDBLANK) ? 8'hFF : byte_r;
  assign dev_busy_o   = dev_busy_w;
  assign dev_done_o   = done_r;
  assign dev_err_o    = err_r;

endmodule

`default_nettype wire

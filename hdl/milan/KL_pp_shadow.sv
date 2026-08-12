/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pp_shadow.sv
  Description : Consumer-side integration wrapper for the protocol-processor
                submodule (protocol_processor_top, architecture of record
                v2.0) — the scenario-B P5 seam, in its FIRST landing shape:
                SHADOW MODE.

                WHY SHADOW AND NOT SUBSTITUTION. Scenario B's contract is
                "direct substitution at parity, old planes deleted". That is
                not reachable at this pin: the processor's AECP engine is the
                P4 micro-coded uCPU, which has NOT landed at its top — the
                AECP pop face is tied ready = 0 there and TX arbiter lanes 0
                and 1 (LANE_AECP_SOL_C / LANE_AECP_UNS_C) are, in the top's
                own words, "idle until P4". Deleting this repository's AECP
                plane against that pin would delete a shipping, live-validated
                AEM/AECP implementation and replace it with silence. So the
                first landing runs the processor ALONGSIDE the shipping
                planes and lets it drive NOTHING:

                  - it sees every control frame the shipping planes see, from
                    the same monitor tap, on real silicon and real traffic;
                  - its MAC TX byte stream is drained and COUNTED, never
                    merged into the control lane, so the wire is bit-for-bit
                    what it is today (no duplicate ADPDU, no second answer to
                    a controller — the failure mode a naive coexistence would
                    ship);
                  - its state is read out over the side port, so its ADP,
                    ACMP and SRP state machines can be compared against the
                    shipping planes' CSRs and against the wire.

                That comparison is the point. Two independent implementations
                observing one live stream is an INDEPENDENT observation in the
                sense the conformance rules demand — unlike a plane grading
                its own CSRs. When P4 lands, the substitution flips this
                wrapper's TX from the drain to the control-lane arbiter and
                deletes the old planes; nothing else here changes.

                RATE. protocol_processor_top eats a 1 byte/clk stream, which
                at 100 MHz is 100 MB/s against gigabit's 125 MB/s: a byte
                serializer fed from the raw tap CANNOT keep up with line rate,
                and would corrupt frames by lagging rather than by dropping
                them. So the tap is CLASSIFIED FIRST, at aligned beat/lane
                positions (the KL_aecp_ingress recipe), and only control
                frames enter a BRAM frame FIFO ahead of the serializer:
                EtherType 0x22F0 (any DA — the processor's own validator does
                the DA work), plus the two MRP pairs its V9 rule passes,
                DA 01-80-C2-00-00-0E + 0x22EA (MSRP) and
                DA 01-80-C2-00-00-21 + 0x88F5 (MVRP). Everything else is
                terminated into the FIFO after at most two words and reclaimed
                atomically by DROP_BAD_FRAME. Control traffic is orders of
                magnitude below the serializer's rate; a frame lost to a full
                FIFO is COUNTED (drop counter, side-port diag) and never
                silently absorbed.

                TAP DISCIPLINE. Like every other plane here this is a pure
                monitor: it drives nothing back onto rx_axis. It qualifies on
                tvalid && tready — the gh #65 handshake hazard: a stalled DMA
                parks a beat with tvalid held, and a tvalid-only tap re-eats
                it.

                NVM. The device face is answered by a BLANK-FLASH responder
                (reads 0xFF, writes accepted and discarded, erase completes).
                That is the processor's documented no-saved-binding path, and
                it is deliberately NOT persistent: shadow mode must not write
                the board's flash, and it has no business owning a region of
                it while the shipping planes own binding persistence.

  Interfaces  : monitor tap on the MAC RX AXIS stream (input only);
                a simple request/ack host bridge for the side port;
                a diagnostic bundle for the CSR.

  Parameters  : see below; N_STREAM_IN_P/N_STREAM_OUT_P size the processor's
                sink/source arrays and must not exceed what the entity model
                declares.
------------------------------------------------------------------------------
*/

`default_nettype none
//! The vendored Forencich .v sources carry a timescale; a build that mixes
//! them with timescale-less SystemVerilog is flagged (IEEE 1800-2023 3.14.2.3).
//! Simulation-only — synthesis ignores it.
`timescale 1ns/1ps

module KL_pp_shadow #(
    //! MAC RX AXIS data width (the datapath's TDATA_WIDTH). 64 only.
    parameter int unsigned TDATA_WIDTH_P  = 64,
    //! core clock, feeds the processor's timer prescaler
    parameter int unsigned CLK_HZ_P       = 100_000_000,
    //! processor sink/source array sizes (F01.5 P-N-STREAM-IN/OUT)
    parameter int unsigned N_STREAM_IN_P  = 8,
    parameter int unsigned N_STREAM_OUT_P = 8,
    //! control-frame FIFO, bytes. One 1522 B frame fits with margin for the
    //! serializer's lag; 4096 is one RAMB36 at 64 b.
    parameter int unsigned RX_FIFO_BYTES_P = 4096,
    //! Timer-prescaler pass-through (09 §3 TIM time compression). The defaults
    //! are REAL time and are what silicon builds use; a testbench overrides
    //! them so a 5 s ADP cadence is reachable in a simulation, exactly as the
    //! datapath already does for CLKV_QTICK_CYC_P / LDIAG_IVAL_CYC_P. They are
    //! DERIVED from CLK_HZ_P here, never mirrored as a second literal.
    parameter int unsigned TIM_DIV_US_P = CLK_HZ_P / 32'd1_000_000,
    parameter int unsigned TIM_DIV_MS_P = 1000,
    //! ACMP listener transition-ROM image (hdl/acmp/rom/gen_ltn_rom.py)
    parameter string       TROM_HEX_P      = "ltn_rom.hex"
) (
    input  wire        clk_i,              //! axis_clk
    input  wire        rst_n,              //! active-low reset

    //! ---- quasi-static identity (from the CSR / entity model) ----
    input  wire [63:0] entity_id_i,        //! own entity_id
    input  wire [63:0] entity_model_id_i,  //! entity_model_id
    input  wire [47:0] station_mac_i,      //! own unicast MAC, NUMERIC EUI-48
                                           //! ([47:40] = first wire byte)
    input  wire [15:0] talker_sources_i,   //! ADPDU talker_stream_sources
    input  wire [15:0] talker_caps_i,      //! ADPDU talker_capabilities
    input  wire [15:0] listener_sinks_i,   //! ADPDU listener_stream_sinks
    input  wire [15:0] listener_caps_i,    //! ADPDU listener_capabilities

    //! ---- level controls ----
    input  wire        enable_i,           //! Milan 5.6.1 boot gate (CSR bit)
    input  wire        restore_go_i,       //! start the NVM boot restore walk
    input  wire        link_up_i,          //! link status (already synced)
    input  wire        gm_change_i,        //! GM_CHANGE strobe from gptp
    input  wire [63:0] gm_id_i,            //! current gm_id
    input  wire [7:0]  gptp_domain_i,      //! current gptp domain number

    //! ---- MAC RX monitor tap (INPUT ONLY — never drives tready) ----
    input  wire [TDATA_WIDTH_P-1:0]     rx_tdata_i,  //! little lane order
    input  wire [TDATA_WIDTH_P/8-1:0]   rx_tkeep_i,  //! final-beat byte mask
    input  wire                         rx_tvalid_i, //! beat valid
    input  wire                         rx_tready_i, //! consumer accepts (gh #65)
    input  wire                         rx_tlast_i,  //! final beat of frame

    //! ---- side-port host bridge (CSR-driven, one outstanding access) ----
    input  wire        host_req_i,         //! single-cycle request strobe
    input  wire        host_we_i,          //! 1 = write
    input  wire [19:0] host_addr_i,        //! 20-bit WORD address
    input  wire [31:0] host_wdata_i,       //! write data
    output logic [31:0] host_rdata_o,      //! read data, valid with ack
    output logic       host_ack_o,         //! completion strobe
    output logic       host_err_o,         //! access refused (with ack)

    //! ---- observability ----
    output logic       restore_busy_o,     //! restore walk running
    output logic       restore_done_o,     //! restore complete
    output logic       restore_fail_o,     //! torn read-back aborted restore
    output logic       nvm_alarm_o,        //! commit retries exhausted
    output logic [15:0] rx_frames_o,       //! control frames handed to the PP
    output logic [7:0] rx_drops_o,         //! frames lost to a full FIFO
    output logic [15:0] tx_frames_o,       //! frames the PP WOULD have sent
    output logic [31:0] dbg_now_ms_o       //! the processor's ms timebase
);

  localparam int unsigned KEEP_W_C = TDATA_WIDTH_P/8;

  // V9 / EtherType constants — MUST match KL_pp_rx_validator's own
  // (DA_MSRP_C / DA_MVRP_C / ET_1722_C / ET_MSRP_C / ET_MVRP_C). A frame this
  // filter drops is a frame the processor can never see, so a divergence here
  // is silent starvation, not a wrong answer.
  localparam logic [47:0] DA_MSRP_C = 48'h01_80_C2_00_00_0E;
  localparam logic [47:0] DA_MVRP_C = 48'h01_80_C2_00_00_21;
  localparam logic [15:0] ET_1722_C = 16'h22F0;
  localparam logic [15:0] ET_MSRP_C = 16'h22EA;
  localparam logic [15:0] ET_MVRP_C = 16'h88F5;

  // ======================================================================= //
  //  RX classify + forward (aligned lanes only, no variable byte muxes)     //
  // ======================================================================= //
  //! A beat is consumed by the stream only when both sides handshake.
  logic beat_w;
  assign beat_w = rx_tvalid_i & rx_tready_i;

  //! beat 0: DA lanes 0-5. beat 1: EtherType lanes 4-5 (wire bytes 12,13).
  logic [47:0] da_num_w;
  logic [15:0] etype_w;
  assign da_num_w = {rx_tdata_i[7:0],   rx_tdata_i[15:8],
                     rx_tdata_i[23:16], rx_tdata_i[31:24],
                     rx_tdata_i[39:32], rx_tdata_i[47:40]};
  assign etype_w  = {rx_tdata_i[47:40], rx_tdata_i[55:48]};

  typedef enum logic [1:0] {FW_HEAD0, FW_HEAD1, FW_BODY, FW_SKIP} fw_state_e;
  fw_state_e fw_S;

  logic [47:0] da_r;      //! DA latched at beat 0, tested at beat 1

  logic                     fw_valid_w, fw_last_w, fw_user_w;
  logic [TDATA_WIDTH_P-1:0] fw_data_w;
  logic [KEEP_W_C-1:0]      fw_keep_w;
  logic                     fw_ready_w;

  //! accept decision, evaluated at beat 1 against the latched DA
  logic accept_w;
  assign accept_w = (etype_w == ET_1722_C)
                 || ((da_r == DA_MSRP_C) && (etype_w == ET_MSRP_C))
                 || ((da_r == DA_MVRP_C) && (etype_w == ET_MVRP_C));

  always_comb begin
    fw_valid_w = 1'b0;
    fw_data_w  = rx_tdata_i;
    fw_keep_w  = rx_tkeep_i;
    fw_last_w  = rx_tlast_i;
    fw_user_w  = 1'b0;
    unique case (fw_S)
      FW_HEAD0: begin
        // Always write beat 0 — the decision is not available until beat 1.
        // A frame ending here is a runt (< 8 B): mark it bad.
        fw_valid_w = beat_w;
        fw_user_w  = rx_tlast_i;
      end
      FW_HEAD1: begin
        fw_valid_w = beat_w;
        // Reject: terminate the frame into the FIFO NOW (2 words spent,
        // reclaimed atomically) instead of streaming the whole thing.
        if (!accept_w) begin
          fw_last_w = 1'b1;
          fw_user_w = 1'b1;
        end
      end
      FW_BODY: begin
        fw_valid_w = beat_w;
      end
      default: begin  // FW_SKIP — the rest of a rejected frame
        fw_valid_w = 1'b0;
      end
    endcase
  end

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      fw_S <= FW_HEAD0;
      da_r <= 48'd0;
    end else if (beat_w) begin
      unique case (fw_S)
        FW_HEAD0: begin
          da_r <= da_num_w;
          fw_S <= rx_tlast_i ? FW_HEAD0 : FW_HEAD1;
        end
        FW_HEAD1: fw_S <= rx_tlast_i ? FW_HEAD0
                                     : (accept_w ? FW_BODY : FW_SKIP);
        FW_BODY:  if (rx_tlast_i) fw_S <= FW_HEAD0;
        default:  if (rx_tlast_i) fw_S <= FW_HEAD0;  // FW_SKIP
      endcase
    end
  end

  //! A control frame offered while the FIFO cannot take it is LOST. The tap
  //! cannot backpressure the NIC, so this is counted, never hidden: fw_ready
  //! low during an accepted write is the only way a frame goes missing.
  logic drop_evt_w;
  assign drop_evt_w = fw_valid_w & ~fw_ready_w
                    & ((fw_S == FW_HEAD0) || (fw_S == FW_HEAD1)
                       || (fw_S == FW_BODY));

  logic [TDATA_WIDTH_P-1:0] ff_data_w;
  logic [KEEP_W_C-1:0]      ff_keep_w;
  logic                     ff_valid_w, ff_last_w, ff_ready_w;

  axis_fifo #(
    .DEPTH               (RX_FIFO_BYTES_P),
    .DATA_WIDTH          (TDATA_WIDTH_P),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (KEEP_W_C),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (1),
    .USER_WIDTH          (1),
    .FRAME_FIFO          (1),
    .USER_BAD_FRAME_VALUE(1'b1),
    .USER_BAD_FRAME_MASK (1'b1),
    .DROP_BAD_FRAME      (1),
    .DROP_OVERSIZE_FRAME (1),
    .DROP_WHEN_FULL      (1)
  ) ctl_fifo (
    .clk                (clk_i),
    .rst                (~rst_n),
    .s_axis_tdata       (fw_data_w),
    .s_axis_tkeep       (fw_keep_w),
    .s_axis_tvalid      (fw_valid_w),
    .s_axis_tready      (fw_ready_w),
    .s_axis_tlast       (fw_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       (fw_user_w),
    .m_axis_tdata       (ff_data_w),
    .m_axis_tkeep       (ff_keep_w),
    .m_axis_tvalid      (ff_valid_w),
    .m_axis_tready      (ff_ready_w),
    .m_axis_tlast       (ff_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (),
    .status_bad_frame   (),
    .status_good_frame  (),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );

  // ======================================================================= //
  //  Byte serializer — 64 b words out of the FIFO, 1 B/clk into the PP      //
  // ======================================================================= //
  logic [TDATA_WIDTH_P-1:0] ser_data_r;
  logic [KEEP_W_C-1:0]      ser_keep_r;
  logic                     ser_last_r;
  logic                     ser_busy_r;
  logic [2:0]               ser_idx_r;

  //! last valid lane of the held word (keep is contiguous from lane 0)
  logic [2:0] ser_top_w;
  always_comb begin
    ser_top_w = 3'd0;
    for (int unsigned i = 0; i < KEEP_W_C; i++) begin
      if (ser_keep_r[i]) ser_top_w = 3'(i);
    end
  end

  //! pop only when idle: one word in flight at a time
  assign ff_ready_w = ~ser_busy_r;

  logic       pp_rx_valid_w;
  logic [7:0] pp_rx_data_w;
  logic       pp_rx_last_w;

  assign pp_rx_valid_w = ser_busy_r;
  assign pp_rx_data_w  = ser_data_r[8*ser_idx_r +: 8];
  assign pp_rx_last_w  = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w);

  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      ser_busy_r <= 1'b0;
      ser_idx_r  <= 3'd0;
      ser_data_r <= '0;
      ser_keep_r <= '0;
      ser_last_r <= 1'b0;
    end else if (!ser_busy_r) begin
      if (ff_valid_w) begin
        ser_data_r <= ff_data_w;
        ser_keep_r <= ff_keep_w;
        ser_last_r <= ff_last_w;
        ser_idx_r  <= 3'd0;
        ser_busy_r <= 1'b1;
      end
    end else begin
      if (ser_idx_r == ser_top_w) ser_busy_r <= 1'b0;
      else                        ser_idx_r  <= ser_idx_r + 3'd1;
    end
  end

  // ======================================================================= //
  //  Blank-flash NVM responder (NOT persistent — see the banner)            //
  // ======================================================================= //
  localparam logic [1:0] NVMP_OP_READ_C  = 2'd0;
  localparam logic [1:0] NVMP_OP_WRITE_C = 2'd1;

  logic        nvm_req_w, nvm_wvalid_w, nvm_rready_w;
  logic [1:0]  nvm_op_w;
  logic [15:0] nvm_len_w;
  logic        nvm_gnt_r, nvm_done_r, nvm_rvalid_r, nvm_wready_r;
  logic [15:0] nvm_cnt_r;
  logic        nvm_busy_r;

  always_ff @(posedge clk_i or negedge rst_n) begin
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
        if (nvm_req_w) begin
          nvm_gnt_r  <= 1'b1;
          nvm_cnt_r  <= nvm_len_w;
          nvm_busy_r <= 1'b1;
          // ERASE (and any zero-length command) completes with no data phase
          if ((nvm_op_w != NVMP_OP_READ_C && nvm_op_w != NVMP_OP_WRITE_C)
              || (nvm_len_w == 16'd0)) begin
            nvm_busy_r <= 1'b0;
            nvm_done_r <= 1'b1;
          end else begin
            nvm_rvalid_r <= (nvm_op_w == NVMP_OP_READ_C);
            nvm_wready_r <= (nvm_op_w == NVMP_OP_WRITE_C);
          end
        end
      end else begin
        // one byte per accepted handshake, blank flash reads as 0xFF
        if ((nvm_rvalid_r & nvm_rready_w) | (nvm_wready_r & nvm_wvalid_w)) begin
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

  // ======================================================================= //
  //  The processor                                                          //
  // ======================================================================= //
  logic        pp_tx_valid_w, pp_tx_eof_w;
  logic        pp_host_rvalid_w, pp_host_err_w;
  logic [31:0] pp_host_rdata_w;

  //! one outstanding side-port access: hold the request until it completes
  logic        hb_pend_r, hb_we_r;
  logic [19:0] hb_addr_r;
  logic [31:0] hb_wdata_r;

  protocol_processor_top #(
      .N_STREAM_IN_P  (N_STREAM_IN_P),
      .N_STREAM_OUT_P (N_STREAM_OUT_P),
      .CLK_HZ_P       (CLK_HZ_P),
      .TIM_DIV_US_P   (TIM_DIV_US_P),
      .TIM_DIV_MS_P   (TIM_DIV_MS_P),
      .TROM_HEX_P     (TROM_HEX_P)
  ) u_pp (
      .clk_i               (clk_i),
      .rst_n               (rst_n),

      .entity_id_i         (entity_id_i),
      .entity_model_id_i   (entity_model_id_i),
      .own_mac_i           (station_mac_i),
      .talker_sources_i    (talker_sources_i),
      .talker_caps_i       (talker_caps_i),
      .listener_sinks_i    (listener_sinks_i),
      .listener_caps_i     (listener_caps_i),
      .current_cfg_i       (16'd0),
      .identify_index_i    (16'd0),

      .entity_enable_i     (enable_i),
      .link_up_i           (link_up_i),
      .gm_change_i         (gm_change_i),
      .gm_id_i             (gm_id_i),
      .gptp_domain_i       (gptp_domain_i),

      //! SRP quasi-static: Milan mandates point-to-point; the rest are the
      //! engine's own defaults and are inert while the service face is idle.
      .p2p_i               (1'b1),
      .cfg_rank_i          (1'b0),
      .cfg_acc_lat_ns_i    (32'd0),
      .port_rate_bps_i     (32'd1_000_000_000),
      .cfg_tspec_max_frame_i(16'd0),

      //! no talker sources are declared to the shadow: it must not attempt a
      //! reservation for a stream the shipping lwSRP plane already owns.
      .cfg_src_en_i        ('0),
      .cfg_src_iface_i     ('0),
      .cfg_stream_id_i     ('0),

      .rx_valid_i          (pp_rx_valid_w),
      .rx_data_i           (pp_rx_data_w),
      .rx_last_i           (pp_rx_last_w),

      .tx_valid_o          (pp_tx_valid_w),
      .tx_sof_o            (),
      //! the payload itself is DELIBERATELY discarded: shadow mode counts the
      //! frames the processor would have sent and keeps not one byte of them.
      //! Landing it in a wire nothing reads would be a lie about intent — and
      //! the strict build says so (UNUSEDSIGNAL on the dead net).
      .tx_data_o           (),
      .tx_eof_o            (pp_tx_eof_w),
      //! SHADOW: the drain is always ready and the bytes go nowhere. This is
      //! the one line that keeps the wire unchanged.
      .tx_ready_i          (1'b1),

      //! P4 uCPU seam — unlanded at this pin, tied per the top's contract
      .aecp_txn_valid_o    (),
      .aecp_txn_o          (),
      .aecp_txn_ready_i    (1'b0),
      .aecp_rxs_rd_slot_i  ('0),
      .aecp_rxs_rd_addr_i  ('0),
      .aecp_rxs_rd_en_i    (1'b0),
      .aecp_rxs_rd_data_o  (),
      .aecp_rxs_slot_len_o (),
      .aecp_rxs_free_i     (1'b0),
      .aecp_rxs_free_slot_i('0),

      .restore_go_i        (restore_go_i),
      .restore_busy_o      (restore_busy_o),
      .restore_done_o      (restore_done_o),
      .restore_fail_o      (restore_fail_o),
      .nvm_alarm_o         (nvm_alarm_o),

      .nvm_dev_req_o       (nvm_req_w),
      .nvm_dev_gnt_i       (nvm_gnt_r),
      .nvm_dev_op_o        (nvm_op_w),
      .nvm_dev_region_o    (),
      .nvm_dev_offset_o    (),
      .nvm_dev_len_o       (nvm_len_w),
      .nvm_dev_wvalid_o    (nvm_wvalid_w),
      .nvm_dev_wready_i    (nvm_wready_r),
      .nvm_dev_wdata_o     (),
      .nvm_dev_rvalid_i    (nvm_rvalid_r),
      .nvm_dev_rdata_i     (8'hFF),
      .nvm_dev_rready_o    (nvm_rready_w),
      .nvm_dev_busy_i      (nvm_busy_r),
      .nvm_dev_done_i      (nvm_done_r),
      .nvm_dev_err_i       (1'b0),

      .host_req_valid_i    (hb_pend_r),
      .host_we_i           (hb_we_r),
      .host_addr_i         (hb_addr_r),
      .host_wdata_i        (hb_wdata_r),
      .host_rdata_o        (pp_host_rdata_w),
      .host_rvalid_o       (pp_host_rvalid_w),
      .host_err_o          (pp_host_err_w),

      //! config-plane seam: unused in shadow mode
      .svc_valid_i         (1'b0),
      .svc_ready_o         (),
      .svc_op_i            ('0),
      .svc_index_i         ('0),
      .svc_stream_id_i     ('0),
      .svc_da_i            ('0),
      .svc_vid_i           ('0),
      .svc_max_frame_i     ('0),
      .svc_lstn_state_i    ('0),
      .svc_rsp_valid_o     (),
      .svc_rsp_status_o    (),
      .svc_rsp_data_o      (),

      .dbg_now_ms_o        (dbg_now_ms_o)
  );

  // ======================================================================= //
  //  Side-port host bridge                                                  //
  // ======================================================================= //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      hb_pend_r    <= 1'b0;
      hb_we_r      <= 1'b0;
      hb_addr_r    <= 20'd0;
      hb_wdata_r   <= 32'd0;
      host_rdata_o <= 32'd0;
      host_ack_o   <= 1'b0;
      host_err_o   <= 1'b0;
    end else begin
      host_ack_o <= 1'b0;
      if (!hb_pend_r) begin
        if (host_req_i) begin
          hb_pend_r  <= 1'b1;
          hb_we_r    <= host_we_i;
          hb_addr_r  <= host_addr_i;
          hb_wdata_r <= host_wdata_i;
        end
      end else if (pp_host_rvalid_w) begin
        hb_pend_r    <= 1'b0;
        host_rdata_o <= pp_host_rdata_w;
        host_err_o   <= pp_host_err_w;
        host_ack_o   <= 1'b1;
      end
    end
  end

  // ======================================================================= //
  //  Shadow counters — the only evidence that the processor is alive        //
  // ======================================================================= //
  always_ff @(posedge clk_i or negedge rst_n) begin
    if (!rst_n) begin
      rx_frames_o <= 16'd0;
      rx_drops_o  <= 8'd0;
      tx_frames_o <= 16'd0;
    end else begin
      if (pp_rx_valid_w & pp_rx_last_w)      rx_frames_o <= rx_frames_o + 16'd1;
      if (drop_evt_w & (rx_drops_o != 8'hFF)) rx_drops_o <= rx_drops_o + 8'd1;
      if (pp_tx_valid_w & pp_tx_eof_w)       tx_frames_o <= tx_frames_o + 16'd1;
    end
  end

endmodule

`default_nettype wire

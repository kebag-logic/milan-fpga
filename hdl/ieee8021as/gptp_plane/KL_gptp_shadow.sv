/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_gptp_shadow.sv
//  Project     : Milan AVB end-station -- the fabric gPTP plane (issue #110)
//
//  Description : The time-sync plane in the KL_pp_shadow integration shape:
//                an INPUT-ONLY tap on the MAC RX AXIS stream classifies
//                EtherType 0x88F7 into a frame FIFO, a byte serializer feeds
//                the gptp-processor submodule's KL_gptp_engine at 1 B/clk,
//                and the engine's byte TX gears back up onto one wide
//                control-lane leg. The engine's PHC face becomes the parent
//                timestamp_counter's knobs (the adjfine pulse latches to a
//                level here; adjtime passes through), and the publish bank
//                (GM identity, parent identity, asCapable/sync flags, peer
//                delay, offset) leaves as wires -- the words milan-statd
//                mirrors today.
//
//                INGRESS TIMESTAMP TRANSPORT (the part a register latch
//                gets wrong): the arrival timestamp is latched at each
//                frame's first beat and pushed into a side FIFO on the
//                frame FIFO's status_good_frame commit pulse -- exactly
//                once per frame that will actually be DELIVERED, so the
//                drop machinery (runt, reject, overflow) can never desync
//                timestamps from frames. The serializer pops one entry at
//                each frame's first byte; the engine latches at sof.
//
//                The ingress point is the tap (axis domain), not the MAC
//                SFD: the constant MAC->tap pipeline offset belongs in the
//                ingress-latency correction (REQ-PTP-06 lineage), and the
//                silicon round (#117) measures it. The EGRESS timestamp
//                comes back from KL_gptp_txstamp at the MAC boundary via
//                the txts_* face, tagged with the transmitted frame's
//                sequenceId AND messageType, because the control lane does
//                not traverse ptp_ts_top's stamper. The engine consumes
//                the sequence tag today; the type tag is carried to its
//                boundary and presented live on dbg_txts_type_o, the
//                PORT and not a register, so it is valid in the same
//                cycle the engine samples the face, until the submodule
//                matches on both (milan-fpga #214,
//                Mister-M-alt/FPGA-gPTP#28), because a sequenceId alone
//                cannot separate a Pdelay_Req from a Pdelay_Resp when the
//                two counters coincide.
//
//                A control frame offered while the FIFO cannot take it is
//                LOST and counted, never hidden (the tap cannot
//                backpressure the NIC). The same is true of the SHED RULE
//                (issue #122): the side FIFO is shallower than the frame
//                FIFO, so a frame arriving when the ring is already spoken
//                for is dropped WHOLE at its first beat rather than allowed
//                to lap a still-live stamp -- see the occupancy block below
//                for why that count has two terms and why the pointer
//                difference must be taken at pointer width.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_gptp_shadow #(
    parameter int unsigned TDATA_WIDTH_P   = 64,
    parameter int unsigned CLK_HZ_P        = 100_000_000,
    parameter string       UCODE_HEX_P     = "gptp_ucode.hex",
    parameter int unsigned RX_FIFO_BYTES_P = 2048,
    parameter int unsigned TX_FIFO_BYTES_P = 2048,
    parameter int unsigned TS_FIFO_LOG2_P  = 5
) (
    input  wire clk_i,                    //! axis_clk
    input  wire rst_n,                    //! active-low reset

    //! MAC RX tap: INPUT ONLY, a beat is real when tvalid && tready
    //! (the gh #65 hazard: a stalled DMA parks a beat with tvalid held)
    input  wire [TDATA_WIDTH_P-1:0]   rx_tdata_i,   //! little lane order
    input  wire [TDATA_WIDTH_P/8-1:0] rx_tkeep_i,
    input  wire                       rx_tvalid_i,
    input  wire                       rx_tready_i,
    input  wire                       rx_tlast_i,

    //! the live PHC value (timestamp_counter.timestamp_out)
    input  wire [63:0] phc_ns_i,

    //! PHC knobs out: adjfine as a latched LEVEL, adjtime as a pulse
    output logic signed [31:0] phc_adj_o,
    output logic               phc_step_we_o,
    output logic        [63:0] phc_step_o,

    //! TX: one wide control-lane leg (whole frames, FRAME_FIFO-held)
    output wire [TDATA_WIDTH_P-1:0]   tx_tdata_o,
    output wire [TDATA_WIDTH_P/8-1:0] tx_tkeep_o,
    output wire                       tx_tvalid_o,
    output wire                       tx_tlast_o,
    input  wire                       tx_tready_i,

    //! egress timestamp return (KL_gptp_txstamp, seq-matched)
    input  wire        txts_valid_i,
    input  wire [63:0] txts_ns_i,
    input  wire [15:0] txts_seq_i,
    input  wire [3:0]  txts_type_i,   //! messageType of the stamped frame

    //! pulses at the FIRST accepted beat of each plane frame entering the
    //! merge chain -- the boundary stamper's take decision samples at a
    //! frame's beat 0, and the gasketed merges can pass that beat through
    //! combinationally in the same cycle, so an eof-timed arm would lose
    //! the race (an sof-timed arm covers both the same-cycle and the
    //! queued case)
    output logic tx_sent_o,

    //! the publish bank -- the retired software contract
    output logic [63:0] pub_gm_id_o,
    output logic [63:0] pub_parent_id_o,
    output logic [31:0] pub_flags_o,      //! b0 present, b1 gm, b2 asCap, b3 sync
    output logic [31:0] pub_pdelay_ns_o,
    output logic [31:0] pub_offset_o,
    output logic [63:0] pub_annq_o,
    output logic        pub_commit_o,

    //! diagnostics
    output logic [15:0] dbg_tap_drop_o,   //! frames lost at the tap FIFO
    output logic [15:0] dbg_rx_drop_o,    //! frames the parser refused
    output logic [15:0] dbg_ev_drop_o,    //! events lost at the queue
    output logic        dbg_busy_o,
    output wire  [63:0] dbg_rx_ts_o,      //! the ts entry feeding the engine
    output wire         dbg_tspush_v_o,   //! bench probes: side-FIFO push
    output wire  [63:0] dbg_tspush_o,
    output wire         dbg_tspop_v_o,    //! side-FIFO pop (engine sof)
    output wire  [3:0]  dbg_txts_type_o   //! the stamp's type tag, live
);

  localparam int unsigned KEEP_W_C = TDATA_WIDTH_P / 8;
  localparam logic [15:0] ET_GPTP_C = 16'h88F7;

  // ======================================================================= //
  //  RX classify (the KL_pp_shadow idiom: aligned lanes, no byte muxes)    //
  // ======================================================================= //
  logic beat_w;
  assign beat_w = rx_tvalid_i & rx_tready_i;

  //! EtherType is wire bytes 12,13 = beat-1 LANES 4 and 5 (lane j =
  //! tdata[8j +: 8]) -- the one-lane-off failure mode is a silently deaf
  //! tap (KL_pp_shadow's banner carries the war story)
  logic [15:0] etype_w;
  assign etype_w = {rx_tdata_i[39:32], rx_tdata_i[47:40]};

  typedef enum logic [1:0] {FW_HEAD0, FW_HEAD1, FW_BODY, FW_SKIP} fw_state_e;
  fw_state_e fw_S;
  //! this frame is being SHED whole (issue #122): the ingress-ts ring was
  //! full at its sof, so no beat may enter the FIFO -- otherwise its commit
  //! would lap the ring over a still-live arrival stamp. Set at FW_HEAD0,
  //! read at FW_HEAD1 (where the EtherType verdict for the count lands).
  logic shed_r;

  logic                     fw_valid_w, fw_last_w, fw_user_w;
  logic [TDATA_WIDTH_P-1:0] fw_data_w;
  logic [KEEP_W_C-1:0]      fw_keep_w;
  logic                     fw_ready_w;

  logic accept_w;
  assign accept_w = (etype_w == ET_GPTP_C);

  //! the shed guard's verdict and the frame FIFO's bad-frame strobe are
  //! DECLARED HERE, above their first use in the always_comb below. Verilator
  //! accepts a later declaration; Vivado's front-end does not (VRFC 10-3380
  //! rejects the whole module), so a file that only ever sees Verilator can
  //! regress the xsim benches silently. Their drivers live with the ring.
  logic full_w;
  logic ff_bad_w;

  always_comb begin
    fw_valid_w = 1'b0;
    fw_data_w  = rx_tdata_i;
    fw_keep_w  = rx_tkeep_i;
    fw_last_w  = rx_tlast_i;
    fw_user_w  = 1'b0;
    unique case (fw_S)
      FW_HEAD0: begin
        // beat 0 normally enters -- the verdict needs beat 1; a frame
        // ending here is a runt, marked bad and dropped atomically. But when
        // the ingress-ts ring is FULL at sof (issue #122), the WHOLE frame is
        // shed before it enters the FIFO: suppress beat 0 too, so its commit
        // (ff_good_w) can never lap the ring over a still-live arrival stamp.
        fw_valid_w = beat_w & ~full_w;
        fw_user_w  = rx_tlast_i;
      end
      FW_HEAD1: begin
        // a shed frame keeps beat 1 out of the FIFO as well, so the shed is
        // atomic at frame granularity: nothing ever entered.
        fw_valid_w = beat_w & ~shed_r;
        if (!accept_w & ~shed_r) begin
          fw_last_w = 1'b1;
          fw_user_w = 1'b1;                  // reject: reclaimed atomically
        end
      end
      FW_BODY: fw_valid_w = beat_w;
      default: fw_valid_w = 1'b0;            // FW_SKIP
    endcase
  end

  //! the arrival stamp for the frame currently entering the tap
  logic [63:0] ts_arr_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      fw_S     <= FW_HEAD0;
      ts_arr_r <= 64'd0;
      shed_r   <= 1'b0;
    end else if (beat_w) begin
      unique case (fw_S)
        FW_HEAD0: begin
          ts_arr_r <= phc_ns_i;
          // shed the WHOLE frame when the ts ring is full at sof (issue
          // #122). A one-beat runt at full stays uncounted -- no EtherType
          // verdict lands, matching today's bad-frame reclaim.
          shed_r   <= full_w & ~rx_tlast_i;
          fw_S     <= rx_tlast_i ? FW_HEAD0 : FW_HEAD1;
        end
        // a shed frame routes to FW_SKIP regardless of EtherType (it never
        // entered the FIFO); accept_w still steers a normal frame.
        FW_HEAD1: fw_S <= rx_tlast_i ? FW_HEAD0
                                     : ((shed_r | ~accept_w) ? FW_SKIP : FW_BODY);
        FW_BODY:  if (rx_tlast_i) fw_S <= FW_HEAD0;
        default:  if (rx_tlast_i) fw_S <= FW_HEAD0;
      endcase
    end
  end

  //! counted, never hidden. DROP_WHEN_FULL keeps s_ready HIGH and drops
  //! whole frames INSIDE the FIFO, so a ready-based counter never fires:
  //! status_overflow is the real drop strobe (one per lost frame); the
  //! ready term stays as a belt-and-braces alarm for any backpressure
  //! mode change.
  logic ff_ovf_w;
  logic drop_evt_w;
  //! a SHED gPTP frame (issue #122): the ring was full at its sof, so it
  //! never entered the FIFO and ff_ovf_w never fires for it. Count it in the
  //! tap-drop diagnostic ONLY once the EtherType verdict lands (beat 1 =
  //! FW_HEAD1) and ONLY when it is 0x88F7 -- counting non-gPTP sheds would
  //! poison the diagnostic.
  logic shed_gptp_w;
  assign shed_gptp_w = beat_w & (fw_S == FW_HEAD1) & shed_r & accept_w;
  assign drop_evt_w = (fw_valid_w & ~fw_ready_w & (fw_S != FW_SKIP))
                    | ff_ovf_w | shed_gptp_w;
  logic [15:0] tap_drop_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n)           tap_drop_r <= 16'd0;
    else if (drop_evt_w)  tap_drop_r <= tap_drop_r + 16'd1;
  end
  assign dbg_tap_drop_o = tap_drop_r;

  logic [TDATA_WIDTH_P-1:0] ff_data_w;
  logic [KEEP_W_C-1:0]      ff_keep_w;
  logic                     ff_valid_w, ff_last_w, ff_ready_w;
  logic                     ff_good_w;

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
  ) rx_fifo (
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
    .m_axis_tvalid     (ff_valid_w),
    .m_axis_tready      (ff_ready_w),
    .m_axis_tlast       (ff_last_w),
    .m_axis_tid         (),
    .m_axis_tdest       (),
    .m_axis_tuser       (),
    .status_overflow    (ff_ovf_w),
    .status_bad_frame   (ff_bad_w),
    .status_good_frame  (ff_good_w),
    .status_depth       (),
    .status_depth_commit(),
    .pause_req          (1'b0),
    .pause_ack          ()
  );

  // ======================================================================= //
  //  Ingress-timestamp side FIFO: pushed per COMMITTED frame only          //
  // ======================================================================= //
  localparam int unsigned TSD_C = 1 << TS_FIFO_LOG2_P;
  logic [63:0] tsf_r [0:TSD_C-1];
  //! one extra pointer bit so (wp - rp) is a wrap-safe occupancy rather than
  //! an ambiguous full/empty compare
  logic [TS_FIFO_LOG2_P:0] tsf_wp_r, tsf_rp_r;
  logic tsf_pop_w;

  // ----------------------------------------------------------------------- //
  //  THE SHED GUARD'S OCCUPANCY (issue #122), in two terms                   //
  //                                                                          //
  //  The ring is PUSHED on ff_good_w -- the frame FIFO's commit -- which LAGS //
  //  the tap sof by the FIFO's write latency, so the ring pointers alone      //
  //  under-count: frames already taken at the tap but not yet committed are   //
  //  invisible, the guard sheds too late, and the ring still laps (measured:  //
  //  38 frames into a 32-entry ring on the burst below).                      //
  //                                                                          //
  //  Counting instead at the TAP and releasing on POP is what a first cut     //
  //  did, and it LEAKS: a frame the FIFO itself discards (oversize, or full)  //
  //  never commits, so it never pushes and never pops. One slot leaks per     //
  //  discarded frame and after TSD_C of them the guard wedges shut and the    //
  //  plane goes PERMANENTLY DEAF -- worse than the lap it was fixing, and     //
  //  invisible to the whole sweep (measured: 40 oversize frames, then         //
  //  nothing was ever accepted again).                                        //
  //                                                                          //
  //  So the second term counts frames that have ENTERED the frame FIFO and    //
  //  are not yet RESOLVED by it. A frame resolves exactly once -- good (a     //
  //  future push), bad, or overflow (no push) -- so this can neither leak nor //
  //  underflow, whatever the FIFO does with the frame. It counts non-gPTP     //
  //  frames too, which only makes the guard slightly conservative: they       //
  //  resolve within a couple of cycles and never push.                        //
  //                                                                          //
  //  sum = entries the ring holds + pushes it may still be owed, so shedding  //
  //  a new frame at TSD_C means the ring is never asked to hold a 33rd.       //
  // ----------------------------------------------------------------------- //
  logic fifo_enter_w, fifo_resolve_w;
  //! a frame's FIRST beat being written IS the frame entering the FIFO
  assign fifo_enter_w   = fw_valid_w & fw_ready_w & (fw_S == FW_HEAD0);
  assign fifo_resolve_w = ff_good_w | ff_bad_w | ff_ovf_w;
  //! BOUND: an enter is blocked once occ reaches TSD_C, and unres_r <= occ,
  //! so unres_r never exceeds TSD_C -- one bit wider than the ring index is
  //! all it needs. The saturations below are then unreachable by
  //! construction and kept only as belt-and-braces on a wedge that would
  //! cost the plane every frame.
  logic [TS_FIFO_LOG2_P:0] unres_r;
  //! THE SUBTRACTION MUST HAPPEN AT POINTER WIDTH. `N'(a - b)` sets the
  //! CONTEXT size of the whole expression, so casting the difference straight
  //! to the sum's width evaluates a - b at that width and the wrap-safe extra
  //! pointer bit is thrown away: every wrap then reads ~2^N - (rp - wp), the
  //! guard latches full and the plane sheds frames it has room for. Take the
  //! difference in its own N+1-bit net FIRST, then widen.
  logic [TS_FIFO_LOG2_P:0]   ring_occ_w;
  logic [TS_FIFO_LOG2_P+1:0] occ_w;
  assign ring_occ_w = tsf_wp_r - tsf_rp_r;
  assign occ_w  = {1'b0, ring_occ_w} + {1'b0, unres_r};
  assign full_w = (occ_w >= (TS_FIFO_LOG2_P+2)'(TSD_C));

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      tsf_wp_r <= '0;
      tsf_rp_r <= '0;
      unres_r  <= '0;
    end else begin
      if (ff_good_w) begin
        tsf_r[tsf_wp_r[TS_FIFO_LOG2_P-1:0]] <= ts_arr_r;
        tsf_wp_r                            <= tsf_wp_r + 1'b1;
      end
      //! the empty test makes a pop-without-push STRUCTURALLY unable to drive
      //! rp past wp. It cannot fire today (a pop trails its push by cycles),
      //! but with a pointer-difference compare that ordering is the only
      //! thing standing between a stray pop and a permanently shedding guard
      if (tsf_pop_w & (tsf_wp_r != tsf_rp_r)) tsf_rp_r <= tsf_rp_r + 1'b1;
      if (fifo_enter_w & ~fifo_resolve_w) begin
        if (~&unres_r) unres_r <= unres_r + 1'b1;
      end else if (~fifo_enter_w & fifo_resolve_w) begin
        if (|unres_r)  unres_r <= unres_r - 1'b1;
      end
    end
  end

  logic [63:0] rx_ts_w;
  assign rx_ts_w = tsf_r[tsf_rp_r[TS_FIFO_LOG2_P-1:0]];
  assign dbg_rx_ts_o = rx_ts_w;
  assign dbg_tspush_v_o = ff_good_w;
  assign dbg_tspush_o   = ts_arr_r;
  assign dbg_tspop_v_o  = tsf_pop_w;

  // ======================================================================= //
  //  Byte serializer: 1 B/clk into the engine, sof pops the ts entry       //
  // ======================================================================= //
  logic [TDATA_WIDTH_P-1:0] ser_data_r;
  logic [KEEP_W_C-1:0]      ser_keep_r;
  logic                     ser_last_r, ser_busy_r, ser_sof_r;
  logic [2:0]               ser_idx_r;

  logic [2:0] ser_top_w;
  always_comb begin
    ser_top_w = 3'd0;
    for (int unsigned i = 0; i < KEEP_W_C; i++) begin
      if (ser_keep_r[i]) ser_top_w = 3'(i);
    end
  end

  assign ff_ready_w = ~ser_busy_r;

  logic       eng_rx_valid_w, eng_rx_sof_w, eng_rx_eof_w;
  logic [7:0] eng_rx_data_w;
  assign eng_rx_valid_w = ser_busy_r;
  assign eng_rx_data_w  = ser_data_r[8*ser_idx_r +: 8];
  assign eng_rx_sof_w   = ser_busy_r & ser_sof_r & (ser_idx_r == 3'd0);
  assign eng_rx_eof_w   = ser_busy_r & ser_last_r & (ser_idx_r == ser_top_w);

  assign tsf_pop_w = eng_rx_valid_w & eng_rx_sof_w;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      ser_busy_r <= 1'b0;
      ser_idx_r  <= 3'd0;
      ser_data_r <= '0;
      ser_keep_r <= '0;
      ser_last_r <= 1'b0;
      ser_sof_r  <= 1'b1;
    end else if (!ser_busy_r) begin
      if (ff_valid_w) begin
        ser_data_r <= ff_data_w;
        ser_keep_r <= ff_keep_w;
        ser_last_r <= ff_last_w;
        ser_idx_r  <= 3'd0;
        ser_busy_r <= 1'b1;
      end
    end else begin
      if (ser_idx_r == ser_top_w) begin
        ser_busy_r <= 1'b0;
        ser_sof_r  <= ser_last_r;      // next word starts a frame iff eof
      end else begin
        ser_idx_r <= ser_idx_r + 3'd1;
        if (ser_idx_r == 3'd0) ser_sof_r <= 1'b0;
      end
    end
  end

  // ======================================================================= //
  //  The engine (gptp-processor submodule)                                 //
  // ======================================================================= //
  logic       eng_tx_valid_w, eng_tx_sof_w, eng_tx_eof_w, eng_tx_ready_w;
  logic [7:0] eng_tx_data_w;
  logic       adj_we_w;
  logic [31:0] adj_val_w;

  KL_gptp_engine #(
      .UCODE_HEX_P (UCODE_HEX_P),
      .CLK_HZ_P    (CLK_HZ_P)
  ) u_engine (
      .clk_i              (clk_i),
      .rst_n              (rst_n),
      .rx_valid_i         (eng_rx_valid_w),
      .rx_data_i          (eng_rx_data_w),
      .rx_sof_i           (eng_rx_sof_w),
      .rx_eof_i           (eng_rx_eof_w),
      .rx_err_i           (1'b0),
      .rx_ts_i            (rx_ts_w),
      .tx_valid_o         (eng_tx_valid_w),
      .tx_data_o          (eng_tx_data_w),
      .tx_sof_o           (eng_tx_sof_w),
      .tx_eof_o           (eng_tx_eof_w),
      .tx_ready_i         (eng_tx_ready_w),
      .txts_valid_i       (txts_valid_i),
      .txts_ns_i          (txts_ns_i),
      .txts_seq_i         (txts_seq_i),
      .phc_ns_i           (phc_ns_i),
      .phc_addend_we_o    (adj_we_w),
      .phc_addend_o       (adj_val_w),
      .phc_step_we_o      (phc_step_we_o),
      .phc_step_o         (phc_step_o),
      .pub_gm_id_o        (pub_gm_id_o),
      .pub_parent_id_o    (pub_parent_id_o),
      .pub_flags_o        (pub_flags_o),
      .pub_pdelay_ns_o    (pub_pdelay_ns_o),
      .pub_offset_o       (pub_offset_o),
      .pub_annq_o         (pub_annq_o),
      .pub_commit_o       (pub_commit_o),
      .eff_nvm_stb_o      (),
      .eff_nvm_mark_o     (),
      .eff_notify_stb_o   (),
      .eff_notify_class_o (),
      .dbg_rx_drop_o      (dbg_rx_drop_o),
      .dbg_ev_drop_o      (dbg_ev_drop_o),
      .dbg_busy_o         (dbg_busy_o),
      .dbg_status_o       ()
  );

  //! adjfine is a level at the counter: latch the engine's pulse
  always_ff @(posedge clk_i) begin : adj_latch
    if (!rst_n)        phc_adj_o <= '0;
    else if (adj_we_w) phc_adj_o <= $signed(adj_val_w);
  end

  //! The stamper's messageType tag, passed straight through. NOT
  //! registered here, deliberately: the stamper already holds
  //! {ts_ns_o, ts_seq_o, ts_type_o} in registers, and the engine samples
  //! the txts_* face COMBINATIONALLY in the cycle txts_valid_i is high
  //! (KL_gptp_engine's `if (txts_valid_i) ... txts_pend_seq_r <=
  //! txts_seq_i` latches it there; no line number, the pin moves). A
  //! register in
  //! this path would add no persistence and one cycle of lag, so at the
  //! sampling cycle it would still carry the PREVIOUS stamp's type and a
  //! consumer would credit one leg's egress time to another's claim --
  //! the mis-crediting of Mister-M-alt/FPGA-gPTP#28 over again, off by a
  //! leg instead of a sequence. When the engine matches on both tags this
  //! wire feeds its port; tb/verilator/gptp_shadow asserts the equality
  //! AT the valid cycle so the lag cannot come back.
  assign dbg_txts_type_o = txts_type_i;

  // ======================================================================= //
  //  TX gearbox: 1 B/clk up to wide beats, whole frames onto the lane      //
  // ======================================================================= //
  logic [TDATA_WIDTH_P-1:0] gb_data_r;
  logic [KEEP_W_C-1:0]      gb_keep_r;
  logic [2:0]               gb_idx_r;

  logic                     gbo_valid_w, gbo_last_w, gbo_ready_w;
  logic [TDATA_WIDTH_P-1:0] gbo_data_w;
  logic [KEEP_W_C-1:0]      gbo_keep_w;

  //! the engine byte is accepted while the beat register has room and the
  //! TX FIFO can take a completed beat; FRAME_FIFO holds the frame until
  //! its eof so a stalled lane never shows a partial frame downstream
  assign eng_tx_ready_w = gbo_ready_w | ~gbo_valid_w;

  logic beat_full_w, tx_byte_w;
  assign tx_byte_w   = eng_tx_valid_w & eng_tx_ready_w;
  assign beat_full_w = tx_byte_w & ((gb_idx_r == 3'd7) | eng_tx_eof_w);

  //! a completed beat presents combinationally from the staging register
  logic                     st_valid_r, st_last_r;
  logic [TDATA_WIDTH_P-1:0] st_data_r;
  logic [KEEP_W_C-1:0]      st_keep_r;

  assign gbo_valid_w = st_valid_r;
  assign gbo_data_w  = st_data_r;
  assign gbo_keep_w  = st_keep_r;
  assign gbo_last_w  = st_last_r;

  always_ff @(posedge clk_i) begin
    if (!rst_n) begin
      gb_data_r  <= '0;
      gb_keep_r  <= '0;
      gb_idx_r   <= 3'd0;
      st_valid_r <= 1'b0;
      st_data_r  <= '0;
      st_keep_r  <= '0;
      st_last_r  <= 1'b0;
    end else begin
      if (st_valid_r && gbo_ready_w) st_valid_r <= 1'b0;
      if (tx_byte_w) begin
        gb_data_r[8*gb_idx_r +: 8] <= eng_tx_data_w;
        gb_keep_r[gb_idx_r]        <= 1'b1;
        if ((gb_idx_r == 3'd7) || eng_tx_eof_w) begin
          st_data_r  <= gb_data_r;
          st_data_r[8*gb_idx_r +: 8] <= eng_tx_data_w;
          st_keep_r  <= gb_keep_r | (KEEP_W_C'(1) << gb_idx_r);
          st_last_r  <= eng_tx_eof_w;
          st_valid_r <= 1'b1;
          gb_idx_r   <= 3'd0;
          gb_keep_r  <= '0;
        end else begin
          gb_idx_r <= gb_idx_r + 3'd1;
        end
      end
    end
  end

  logic txf_out_last_w, txf_out_valid_w, txf_out_ready_w;

  axis_fifo #(
    .DEPTH               (TX_FIFO_BYTES_P),
    .DATA_WIDTH          (TDATA_WIDTH_P),
    .KEEP_ENABLE         (1),
    .KEEP_WIDTH          (KEEP_W_C),
    .LAST_ENABLE         (1),
    .ID_ENABLE           (0),
    .DEST_ENABLE         (0),
    .USER_ENABLE         (0),
    .FRAME_FIFO          (1),
    .DROP_BAD_FRAME      (0),
    .DROP_OVERSIZE_FRAME (0),
    .DROP_WHEN_FULL      (0)
  ) tx_fifo (
    .clk                (clk_i),
    .rst                (~rst_n),
    .s_axis_tdata       (gbo_data_w),
    .s_axis_tkeep       (gbo_keep_w),
    .s_axis_tvalid      (gbo_valid_w),
    .s_axis_tready      (gbo_ready_w),
    .s_axis_tlast       (gbo_last_w),
    .s_axis_tid         ('0),
    .s_axis_tdest       ('0),
    .s_axis_tuser       ('0),
    .m_axis_tdata       (tx_tdata_o),
    .m_axis_tkeep       (tx_tkeep_o),
    .m_axis_tvalid      (txf_out_valid_w),
    .m_axis_tready      (tx_tready_i),
    .m_axis_tlast       (txf_out_last_w),
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

  assign tx_tvalid_o = txf_out_valid_w;
  assign tx_tlast_o  = txf_out_last_w;

  //! sof tracking on the lane output: the arm fires with beat 0
  logic txo_sof_r;
  always_ff @(posedge clk_i) begin
    if (!rst_n)                              txo_sof_r <= 1'b1;
    else if (txf_out_valid_w && tx_tready_i) txo_sof_r <= txf_out_last_w;
  end
  assign tx_sent_o = txf_out_valid_w & tx_tready_i & txo_sof_r;

  logic unused_w;
  assign unused_w = eng_tx_sof_w;

endmodule : KL_gptp_shadow
`default_nettype wire

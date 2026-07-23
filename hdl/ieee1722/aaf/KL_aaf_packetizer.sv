/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : KL_aaf_packetizer.sv
  Author      : Kebag Logic

  Date        : 2026-07-22
  Description : Shared NxN AAF talker packetizer (docs/NXN_ARCHITECTURE.md
                §2.1-§2.3, phase P4): ONE framer/serializer, N talker
                contexts in a BRAM-backed context RAM (TCTX) + a double-
                banked sample staging RAM. Consumes the {slot, L, R} pair
                stream from the physical capture front-end
                (KL_aaf_capture_i2s today, item-4 TDM ser/des later) and
                emits IEEE 1722 AAF-PCM class-A frames (VLAN-tagged, 6
                samples/ch per PDU) on a 64-bit AXIS master.

                TCTX record (spec §2.2, address {t[2:0], word[3:0]}):
                  w0 CTRL   {en[0], chans[4:1], vlan_vid[16:5]}
                  w1 DMAC_LO[31:0]
                  w2 {UID[31:16], DMAC_HI[15:0]}   (stream_id = {mac, uid})
                  w3 SEQ_TS  {sequence_num[7:0]}
                  w4 TS      latched presentation time (ptp_ns + transit
                             at first-sample capture)
                  w5 FRAMES  frames_sent counter

                MULTI-CHANNEL (item-4): w0.chans = channels_per_frame,
                CONSUMED for every talker (t0 included; reset default 2 -
                never write it and the wire is byte-identical to the
                stereo shape). Supported values: even 2..8 (the pair
                stream is 2-channel-granular); 0/1 clamp to 2, odd to the
                next even, > 8 to 8. A flop mirror snoops CTRL writes so
                admission never waits on a BRAM read. The pair-slot space
                is partitioned by a prefix sum of chans/2: talker t owns
                pair slots [sum(chans/2 below t), +chans/2) - exactly the
                slot k = talker k mapping when every talker is stereo.
                Changing chans while a stream is enabled/mid-epoch is not
                supported (reconfigure disabled).

                Sample staging: double-banked RAM, 6 samples x up to 4
                pairs per bank per stream, addressed {t, bank, sample[2:0],
                chpair[1:0]} - channel alignment is slot-structural (an
                overrun drop can never skew channels). The bank swap IS
                the epoch boundary (spec §2.2). Scheduling = round-robin
                over pending banks (spec §2.3's epoch walk; pairs of all
                streams share the media clock, so pends land on the same
                6-sample cadence).

                Talker 0 aliases the legacy CSR config inputs (dest_mac /
                vlan_vid / uid 0 / chans 2) - the no-regression axiom: at
                N=1 the wire bytes equal aaf_talker_i2s's exactly (golden
                byte-compare TB). Talkers > 0 read CFG from TCTX
                (CSR-window-written, P11).

                RAM house rules: each RAM has ONE sync write process and
                ONE explicit sync read port (defect-4 lineage); the window
                port shares TCTX's ports in idle slots.

                AAF header math (IEEE 1722-2016, pdftotext-verified):
                channels_per_frame is the 10-bit field of Figure 26
                spanning fsd1 bytes {[1:0] high bits, byte 2} = frame
                bytes 35/36 here (7.3.3: "the number of audio channels
                represented in the audio sample frame"); payload =
                6 samples x C channels x 4 octets (format INT_32BIT,
                7.3.5 chronological interleave, network byte order), so
                stream_data_length (4.4.4.10) = 24*C and the frame is
                42 + 24*C bytes == 2 (mod 8): the last AXIS beat always
                keeps exactly 2 bytes and the beat count is 3*C + 6.
                C = 2 emits the historical 90-byte shape byte-identically
                (golden byte-compare gated).

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

//! Shared NxN AAF packetizer (NXN §2.1-§2.3 / P4): one framer, N talker
//! contexts (TCTX: seq/ts/frames + CFG for t>0), double-banked staging RAM,
//! round-robin epoch scheduler, t0 = legacy CSR alias (bit-exact vs
//! aaf_talker_i2s at N=1 - golden byte-compare gated).

`default_nettype none

module KL_aaf_packetizer #(
  parameter int unsigned N_TALKERS_P = 1   //! talker stream contexts
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset

  //! --- pair stream from the capture front-end (one crossing, all slots) -
  input  wire         pair_valid_i,      //! one-cycle pulse per L/R pair
  input  wire [4:0]   pair_slot_i,       //! pair slot 0..31 (talker t owns
                                         //! chans/2 consecutive slots; 32-slot
                                         //! space = 8 talkers x 4 pairs max -
                                         //! see header. Physical capture drives
                                         //! only 0..15; the chan-map mux uses
                                         //! the full width)
  input  wire [23:0]  pair_l_i,
  input  wire [23:0]  pair_r_i,

  //! --- per-talker admission gates (t0 = legacy aaf_gate) ----------------
  input  wire [N_TALKERS_P-1:0] stream_en_i,

  //! --- talker-0 legacy config aliases (no-regression axiom) -------------
  input  wire [47:0]  dest_mac_i,        //! t0 stream DMAC
  input  wire [47:0]  station_mac_i,     //! src MAC (all streams)
  input  wire [11:0]  vlan_vid_i,        //! t0 SR class VID
  input  wire [31:0]  transit_ns_i,      //! presentation offset (all streams)
  input  wire [63:0]  ptp_ns_i,          //! live PHC nanoseconds

  //! --- TCTX window port (P11 CSR window / TB; engine-arbitrated) --------
  input  wire         tctx_wr_en_i,      //! write request (poll wr_rdy)
  input  wire [6:0]   tctx_wr_addr_i,    //! {t[2:0], word[3:0]}
  input  wire [31:0]  tctx_wr_data_i,
  output logic        tctx_wr_rdy_o,     //! write accepted this cycle
  input  wire         tctx_rd_en_i,      //! read request (hold until valid)
  input  wire [6:0]   tctx_rd_addr_i,
  output logic [31:0] tctx_rd_data_o,
  output logic        tctx_rd_valid_o,

  //! --- AAF frames out (64b AXIS little lane, into the TX merge) ---------
  output logic [63:0] m_axis_tdata,
  output logic [7:0]  m_axis_tkeep,
  output logic        m_axis_tvalid,
  output logic        m_axis_tlast,
  input  wire         m_axis_tready,

  //! --- status ------------------------------------------------------------
  output logic [31:0] frames_sent_o      //! t0 frames (legacy CSR alias)
);

  localparam int unsigned SAMPLES_PER_FRAME_C = 6;
  localparam int unsigned MAX_CHANS_C = 8;             //! even 2..8 supported
  localparam int unsigned MAX_PAIRS_C = MAX_CHANS_C/2;
  //! frame sizing at the C = MAX ceiling (fb/beat mux); the live frame ends
  //! at ebeats_w = np_w + 6 beats (42 + 8*np bytes, np = 3*C pairs)
  localparam int unsigned FRAME_BYTES_C = 14 + 4 + 24 + 24*MAX_CHANS_C; //! 234
  localparam int unsigned NUM_BEATS_C   = (FRAME_BYTES_C + 7) / 8;     //! 30
  //! 42 + 24*C == 2 (mod 8) for every C: the last beat always keeps 2 bytes
  localparam int unsigned LAST_KEEP_C   = 2;
  localparam int unsigned TIDXW_C = (N_TALKERS_P <= 1) ? 1
                                                       : $clog2(N_TALKERS_P);
  localparam int unsigned TAW_C   = TIDXW_C + 4;      //! TCTX {t, word}
  //! staging {t, bank, sample[2:0], chpair[1:0]}
  localparam int unsigned SAW_C   = TIDXW_C + 1 + 3 + 2;

  //! TCTX word indices (spec §2.2)
  localparam logic [3:0] TW_CTRL_C = 4'd0, TW_DML_C = 4'd1, TW_DMH_C = 4'd2,
                         TW_SEQ_C  = 4'd3, TW_TS_C  = 4'd4, TW_FRM_C = 4'd5;

  function automatic [TAW_C-1:0] taddr(input [TIDXW_C-1:0] t, input [3:0] w);
    taddr = {t, w};
  endfunction

  // ======================================================================
  //  TCTX RAM - one sync write process, ONE explicit sync read port
  // ======================================================================
  logic [31:0]      tctx_r [(1 << TAW_C)];
  logic             tram_we_w;
  logic [TAW_C-1:0] tram_waddr_w, tram_raddr_w;
  logic [31:0]      tram_wdata_w;
  logic [31:0]      tram_q_r;

  always_ff @(posedge clk_i) begin : tctx_write_port
    if (tram_we_w) tctx_r[tram_waddr_w] <= tram_wdata_w;
  end : tctx_write_port

  always_ff @(posedge clk_i) begin : tctx_read_port
    tram_q_r <= tctx_r[tram_raddr_w];
  end : tctx_read_port

  // ======================================================================
  //  Sample staging RAM (double-banked, 6 pairs used of 8 per bank)
  // ======================================================================
  logic [47:0]      stg_r [(1 << SAW_C)];
  logic             stg_we_w;
  logic [SAW_C-1:0] stg_waddr_w, stg_raddr_w;
  logic [47:0]      stg_wdata_w;
  logic [47:0]      stg_q_r;

  always_ff @(posedge clk_i) begin : stg_write_port
    if (stg_we_w) stg_r[stg_waddr_w] <= stg_wdata_w;
  end : stg_write_port

  always_ff @(posedge clk_i) begin : stg_read_port
    stg_q_r <= stg_r[stg_raddr_w];
  end : stg_read_port

  // ======================================================================
  //  Per-stream capture state (scheduler flags stay in flops)
  // ======================================================================
  logic [2:0] nsamp_r  [N_TALKERS_P];   //! samples accumulated in wr bank
  logic       wbank_r  [N_TALKERS_P];   //! bank being filled
  logic       pend_r   [N_TALKERS_P];   //! !wbank full, awaiting emission

  //! channels_per_frame flop mirror of TCTX w0.chans (clamped even 2..8;
  //! reset 2 = the byte-identical stereo default, t0 included). Snoops the
  //! single TCTX write process so admission never reads the BRAM.
  function automatic [3:0] chn_clamp(input [3:0] c);
    chn_clamp = (c < 4'd2) ? 4'd2
              : (c >= 4'd8) ? 4'd8
              : (c[0] ? (c + 4'd1) : c);
  endfunction

  logic [3:0] chans_r [N_TALKERS_P];

  //! pair-slot partition: talker t owns pair slots [pbase_w[t], pbase_w[t+1])
  //! (prefix sum of chans/2; the identity slot k = talker k when all-stereo)
  logic [5:0] pbase_w [N_TALKERS_P+1];
  always_comb begin : pair_base
    pbase_w[0] = '0;
    for (int t = 0; t < N_TALKERS_P; t++)
      pbase_w[t+1] = pbase_w[t] + 6'(chans_r[t][3:1]);
  end : pair_base

  //! slot ownership decode (bases are disjoint: at most one talker matches)
  logic               pown_v_w;
  logic [TIDXW_C-1:0] pown_t_w;
  logic [1:0]         pown_o_w;         //! channel-pair offset in the frame
  always_comb begin : slot_own
    pown_v_w = 1'b0;
    pown_t_w = '0;
    pown_o_w = '0;
    for (int t = 0; t < N_TALKERS_P; t++)
      if ((6'(pair_slot_i) >= pbase_w[t]) &&
          (6'(pair_slot_i) <  pbase_w[t+1])) begin
        pown_v_w = 1'b1;
        pown_t_w = TIDXW_C'(t);
        pown_o_w = 2'(6'(pair_slot_i) - pbase_w[t]);
      end
  end : slot_own

  wire [1:0] own_pairs_w = 2'(chans_r[pown_t_w][3:1] - 3'd1); //! pairs-1
  wire       own_last_w  = (pown_o_w == own_pairs_w);   //! last pair of sample
  //! accept a pair: stream enabled, slot owned, and not overrunning a
  //! still-pending frame (the old MVP frame_pend drop, per bank; blocking
  //! only the bank-completing pair keeps channel alignment slot-structural)
  wire pair_ok_w = pair_valid_i && pown_v_w && stream_en_i[pown_t_w] &&
                   !(pend_r[pown_t_w] && own_last_w &&
                     (32'(nsamp_r[pown_t_w]) == SAMPLES_PER_FRAME_C - 1));

  assign stg_we_w    = pair_ok_w;
  assign stg_waddr_w = {pown_t_w, wbank_r[pown_t_w],
                        nsamp_r[pown_t_w], pown_o_w};
  assign stg_wdata_w = {pair_l_i, pair_r_i};

  //! first-pair timestamp capture -> TCTX w4 (pending reg absorbs write-
  //! port contention; value latched AT the capture cycle, like the flat
  //! talker's ts_r)
  logic        tsw_pend_r;
  logic [TIDXW_C-1:0] tsw_t_r;
  logic [31:0] tsw_val_r;

  // ======================================================================
  //  Emission engine
  // ======================================================================
  typedef enum logic [2:0] {
    E_IDLE_S,      //! round-robin pend scan
    E_CRD_S,       //! t>0: CFG reads (w0/w1/w2)
    E_DRD_S,       //! DYN + staging reads (w3, w4, 6 pairs)
    E_SEND_S,      //! 12-beat serializer
    E_WBR_S,       //! writeback: w3=seq+1 write + w5 read issue
    E_WBW_S        //! writeback: w5 = q + 1
  } estate_t;

  estate_t           est_r;
  logic [TIDXW_C-1:0] et_r;             //! stream being emitted
  logic               ebank_r;          //! bank being drained
  logic [3:0]        fph_r;             //! fetch phase (saturates at 2)
  logic [4:0]        beat_r;
  logic [TIDXW_C-1:0] rr_r;             //! round-robin pointer

  //! staging fetch walk (E_DRD_S): issues one pair read per cycle in
  //! payload order ({sample, chpair}, chpair fastest); captures lag one
  logic [4:0]        eiss_r;            //! pair reads issued
  logic [4:0]        ecap_r;            //! pairs captured into buf
  logic [2:0]        esmp_r;            //! issue sample index
  logic [1:0]        eo_r;              //! issue channel-pair index

  //! fetched context
  logic [7:0]  eseq_r;
  logic [31:0] ets_r;
  logic [47:0] edmac_r;
  logic [15:0] euid_r;
  logic [11:0] evid_r;
  logic [23:0] buf_l_r [SAMPLES_PER_FRAME_C*MAX_PAIRS_C];
  logic [23:0] buf_r_r [SAMPLES_PER_FRAME_C*MAX_PAIRS_C];

  //! per-frame shape from the chans mirror (clamped even 2..8)
  wire [3:0] echn_w   = chans_r[et_r];
  wire [2:0] epairs_w = echn_w[3:1];
  wire [4:0] np_w     = 5'(SAMPLES_PER_FRAME_C * 32'(epairs_w)); //! payload pairs
  wire [4:0] ebeats_w = np_w + 5'd6;    //! (42 + 8*np + 7) / 8

  //! round-robin grant (lowest distance from rr_r)
  logic               grant_v_w;
  logic [TIDXW_C-1:0] grant_t_w;
  always_comb begin : rr_pick
    grant_v_w = 1'b0;
    grant_t_w = '0;
    for (int k = N_TALKERS_P-1; k >= 0; k--) begin
      int t;
      t = (32'(rr_r) + k + 1) % N_TALKERS_P;
      if (pend_r[t]) begin
        grant_v_w = 1'b1;
        grant_t_w = TIDXW_C'(t);
      end
    end
  end : rr_pick

  // ----------------------------------------------------------------------
  //  Frame byte assembly (combinational over fetched/aliased fields)
  // ----------------------------------------------------------------------
  wire [47:0] eff_dmac_w = (et_r == '0) ? dest_mac_i : edmac_r;
  wire [11:0] eff_vid_w  = (et_r == '0) ? vlan_vid_i : evid_r;
  wire [15:0] eff_uid_w  = (et_r == '0) ? 16'd0      : euid_r;
  wire [63:0] stream_id_w = {station_mac_i, eff_uid_w};

  logic [7:0] fb [0:NUM_BEATS_C*8-1];
  always_comb begin : frame_bytes
    for (int k = 0; k < NUM_BEATS_C*8; k++) fb[k] = 8'h00;
    // Ethernet + 802.1Q (PCP 3, DEI 0, VID)
    {fb[0],fb[1],fb[2],fb[3],fb[4],fb[5]} = eff_dmac_w;
    {fb[6],fb[7],fb[8],fb[9],fb[10],fb[11]} = station_mac_i;
    fb[12]=8'h81; fb[13]=8'h00;
    fb[14]={3'd3, 1'b0, eff_vid_w[11:8]}; fb[15]=eff_vid_w[7:0];
    fb[16]=8'h22; fb[17]=8'hF0;
    // AAF-PCM AVTPDU (IEEE 1722-2016 clause 7)
    fb[18]=8'h02;                       // subtype AAF
    fb[19]=8'h81;                       // sv=1, ver=0, mr=0, tv=1
    fb[20]=eseq_r;                      // sequence_num
    fb[21]=8'h00;                       // reserved, tu=0
    {fb[22],fb[23],fb[24],fb[25],fb[26],fb[27],fb[28],fb[29]} = stream_id_w;
    {fb[30],fb[31],fb[32],fb[33]} = ets_r;                 // avtp_timestamp
    fb[34]=8'h02;                       // format = INT_32BIT
    // fsd1 (1722-2016 Fig 26): nsr[3:0]=5 (48 kHz, Table 11), rsv[1:0],
    // channels_per_frame[9:0] (7.3.3) split over bytes 35/36
    fb[35]={4'h5, 2'b00, 2'b00};        // cpf[9:8] = 0 (C <= 8)
    fb[36]={4'h0, echn_w};              // cpf[7:0] = C (2 = legacy shape)
    fb[37]=8'h20;                       // bit_depth = 32 (7.3.4)
    // stream_data_length (4.4.4.10) = payload octets = 6*C*4 = 8*np
    fb[38]=8'h00; fb[39]={np_w, 3'b000};
    fb[40]=8'h00;                       // sp=0 (normal), evt=0
    fb[41]=8'h00;                       // reserved
    // payload (7.3.5): 6 samples x C channels chronologically interleaved,
    // INT32 left-justified (sample << 8), network byte order. buf holds the
    // np pairs in payload order, so pair j always sits at bytes 42 + 8j.
    for (int j = 0; j < int'(SAMPLES_PER_FRAME_C*MAX_PAIRS_C); j++)
      if (32'(j) < 32'(np_w)) begin
        fb[42+j*8+0]=buf_l_r[j][23:16]; fb[42+j*8+1]=buf_l_r[j][15:8];
        fb[42+j*8+2]=buf_l_r[j][7:0];   fb[42+j*8+3]=8'h00;
        fb[42+j*8+4]=buf_r_r[j][23:16]; fb[42+j*8+5]=buf_r_r[j][15:8];
        fb[42+j*8+6]=buf_r_r[j][7:0];   fb[42+j*8+7]=8'h00;
      end
  end : frame_bytes

  logic [63:0] w_beat_w;
  always_comb
    for (int l = 0; l < 8; l++) w_beat_w[8*l +: 8] = fb[{27'd0, beat_r}*8 + l];

  assign m_axis_tdata  = w_beat_w;
  assign m_axis_tvalid = (est_r == E_SEND_S);
  assign m_axis_tlast  = (est_r == E_SEND_S) && (beat_r == ebeats_w - 5'd1);
  assign m_axis_tkeep  = (beat_r == ebeats_w - 5'd1)
                         ? 8'((1 << LAST_KEEP_C) - 1) : 8'hFF;

  // ----------------------------------------------------------------------
  //  TCTX write mux: ts capture (pend) > engine writeback > window port
  // ----------------------------------------------------------------------
  wire wb_seq_w = (est_r == E_WBR_S);
  wire wb_frm_w = (est_r == E_WBW_S);
  //! writeback stalls while a ts capture drains (single write process)
  wire wb_stall_w = tsw_pend_r;

  always_comb begin : tctx_wmux
    tram_we_w    = 1'b0;
    tram_waddr_w = '0;
    tram_wdata_w = '0;
    tctx_wr_rdy_o = 1'b0;
    if (tsw_pend_r) begin
      tram_we_w    = 1'b1;
      tram_waddr_w = taddr(tsw_t_r, TW_TS_C);
      tram_wdata_w = tsw_val_r;
    end
    else if (wb_seq_w) begin
      tram_we_w    = 1'b1;
      tram_waddr_w = taddr(et_r, TW_SEQ_C);
      tram_wdata_w = {24'd0, eseq_r + 8'd1};
    end
    else if (wb_frm_w) begin
      tram_we_w    = 1'b1;
      tram_waddr_w = taddr(et_r, TW_FRM_C);
      tram_wdata_w = tram_q_r + 32'd1;
    end
    else if (tctx_wr_en_i) begin
      tram_we_w     = 1'b1;
      tram_waddr_w  = tctx_wr_addr_i[TAW_C-1:0];
      tram_wdata_w  = tctx_wr_data_i;
      tctx_wr_rdy_o = 1'b1;
    end
  end : tctx_wmux

  //! window reads share the TCTX read port when the engine has no fetch
  //! in flight (idle-without-grant / mid-serialize slots)
  wire ext_trd_go_w = tctx_rd_en_i &&
                      ((est_r == E_IDLE_S && !grant_v_w) ||
                       (est_r == E_SEND_S));

  //! TCTX read-address mux. The grant cycle already issues the first fetch
  //! read (CTRL for t>0, SEQ for the t0 alias path).
  always_comb begin : tctx_rmux
    tram_raddr_w = taddr(et_r, TW_SEQ_C);
    unique case (est_r)
      E_CRD_S : tram_raddr_w = taddr(et_r, (fph_r == 4'd0) ? TW_DML_C
                                         : (fph_r == 4'd1) ? TW_DMH_C
                                                           : TW_SEQ_C);
      E_DRD_S : tram_raddr_w = taddr(et_r, (fph_r == 4'd0) ? TW_TS_C
                                                           : TW_SEQ_C);
      E_WBR_S : tram_raddr_w = taddr(et_r, TW_FRM_C);
      E_WBW_S : tram_raddr_w = taddr(et_r, TW_FRM_C);  //! hold across stalls
      default : tram_raddr_w = ext_trd_go_w
                  ? tctx_rd_addr_i[TAW_C-1:0]
                  : taddr(grant_t_w, (grant_t_w == '0) ? TW_SEQ_C
                                                       : TW_CTRL_C);
    endcase
  end : tctx_rmux

  //! staging read address (E_DRD_S issues pair reads on the {esmp, eo} walk)
  always_comb begin : stg_rmux
    stg_raddr_w = {et_r, ebank_r, esmp_r, eo_r};
    if (est_r != E_DRD_S) stg_raddr_w = {et_r, ebank_r, 3'd0, 2'd0};
  end : stg_rmux

  // ----------------------------------------------------------------------
  //  Sequential: capture state + emission FSM + window read turnaround
  // ----------------------------------------------------------------------
  logic ext_trd_q_r;                    //! window read issued last cycle

  always_ff @(posedge clk_i) begin : pkt_engine
    if (!rst_n) begin
      est_r   <= E_IDLE_S;
      et_r    <= '0;
      ebank_r <= 1'b0;
      fph_r   <= '0;
      beat_r  <= '0;
      rr_r    <= '0;
      eseq_r  <= '0;
      ets_r   <= '0;
      edmac_r <= '0;
      euid_r  <= '0;
      evid_r  <= '0;
      tsw_pend_r <= 1'b0;
      tsw_t_r    <= '0;
      tsw_val_r  <= '0;
      eiss_r <= '0;
      ecap_r <= '0;
      esmp_r <= '0;
      eo_r   <= '0;
      for (int i = 0; i < int'(SAMPLES_PER_FRAME_C*MAX_PAIRS_C); i++) begin
        buf_l_r[i] <= '0;
        buf_r_r[i] <= '0;
      end
      for (int t = 0; t < N_TALKERS_P; t++) begin
        nsamp_r[t] <= '0;
        wbank_r[t] <= 1'b0;
        pend_r[t]  <= 1'b0;
        chans_r[t] <= 4'd2;
      end
      frames_sent_o   <= '0;
      tctx_rd_data_o  <= '0;
      tctx_rd_valid_o <= 1'b0;
      ext_trd_q_r     <= 1'b0;
    end
    else begin
      tctx_rd_valid_o <= 1'b0;
      if (tsw_pend_r) tsw_pend_r <= 1'b0;   //! ts write wins the port now

      // ---- emission FSM --------------------------------------------------
      unique case (est_r)
        E_IDLE_S : begin
          fph_r  <= '0;
          eiss_r <= '0;
          ecap_r <= '0;
          esmp_r <= '0;
          eo_r   <= '0;
          if (grant_v_w) begin
            et_r    <= grant_t_w;
            ebank_r <= !wbank_r[grant_t_w];   //! the just-filled bank
            rr_r    <= grant_t_w;
            //! t0 uses the legacy CFG aliases: skip the CFG reads.
            //! (the CTRL read for t>0 was issued THIS cycle by tctx_rmux)
            est_r <= (grant_t_w == '0) ? E_DRD_S : E_CRD_S;
          end
        end

        E_CRD_S : begin
          //! fph0: q=CTRL, issue DML; fph1: q=DML, issue DMH; fph2: q=DMH
          unique case (fph_r)
            4'd0 : evid_r <= tram_q_r[16:5];
            4'd1 : edmac_r[31:0] <= tram_q_r;
            default : begin
              edmac_r[47:32] <= tram_q_r[15:0];
              euid_r         <= tram_q_r[31:16];
            end
          endcase
          if (fph_r == 4'd2) begin
            fph_r <= '0;
            est_r <= E_DRD_S;
          end
          else fph_r <= fph_r + 4'd1;
        end

        E_DRD_S : begin
          //! Ordering: IDLE/E_CRD tail issued the SEQ read; fph0 captures
          //! SEQ (rmux issues TS this cycle); fph1 captures TS and starts
          //! the staging walk - one pair read per cycle in payload order
          //! ({esmp, eo}, eo fastest), captures lagging one cycle
          //! (eiss > ecap <=> stg_q_r holds pair ecap). C = 2 walks the
          //! exact fph1..6-issue / fph2..7-capture cadence of the stereo
          //! shape (golden byte-compare timing preserved).
          if (fph_r == 4'd0)      eseq_r <= tram_q_r[7:0];
          else if (fph_r == 4'd1) ets_r  <= tram_q_r;
          if (fph_r != 4'd0) begin
            if (eiss_r != np_w) begin
              eiss_r <= eiss_r + 5'd1;
              if (32'(eo_r) == 32'(epairs_w) - 1) begin
                eo_r   <= '0;
                esmp_r <= esmp_r + 3'd1;
              end
              else eo_r <= eo_r + 2'd1;
            end
            if (ecap_r != eiss_r) begin
              buf_l_r[ecap_r] <= stg_q_r[47:24];
              buf_r_r[ecap_r] <= stg_q_r[23:0];
              ecap_r <= ecap_r + 5'd1;
              if (ecap_r == np_w - 5'd1) begin
                beat_r <= '0;
                est_r  <= E_SEND_S;
              end
            end
          end
          if (fph_r != 4'd2) fph_r <= fph_r + 4'd1;
        end

        E_SEND_S : begin
          if (m_axis_tready) begin
            if (beat_r == ebeats_w - 5'd1) begin
              pend_r[et_r] <= 1'b0;                  //! epoch drained
              est_r <= E_WBR_S;
            end
            else beat_r <= beat_r + 5'd1;
          end
        end

        E_WBR_S : begin
          //! w3=seq+1 write + w5 read issue (skipped a cycle if the ts
          //! capture holds the write port)
          if (!wb_stall_w) est_r <= E_WBW_S;
        end

        E_WBW_S : begin
          //! w5 = q+1 write (tram_q_r = FRAMES read issued in E_WBR_S)
          if (!wb_stall_w) begin
            if (et_r == '0) frames_sent_o <= tram_q_r + 32'd1;
            est_r <= E_IDLE_S;
          end
        end

        default : est_r <= E_IDLE_S;
      endcase

      // ---- pair capture / bank swap (after the FSM so a same-cycle
      //      new-epoch pend set wins over the drain clear) ----------------
      if (pair_ok_w) begin
        //! the sample row advances on its LAST channel pair; the bank swap
        //! on the last row's last pair (channel position is slot-addressed,
        //! so drops can only repeat a row, never skew channels)
        if (own_last_w) begin
          if (32'(nsamp_r[pown_t_w]) == SAMPLES_PER_FRAME_C - 1) begin
            nsamp_r[pown_t_w] <= '0;
            wbank_r[pown_t_w] <= !wbank_r[pown_t_w];
            pend_r[pown_t_w]  <= 1'b1;   //! bank swap = the epoch boundary
          end
          else nsamp_r[pown_t_w] <= nsamp_r[pown_t_w] + 3'd1;
        end
        if (nsamp_r[pown_t_w] == '0 && pown_o_w == '0) begin
          //! first pair of the epoch: latch the presentation time
          tsw_pend_r <= 1'b1;
          tsw_t_r    <= pown_t_w;
          tsw_val_r  <= ptp_ns_i[31:0] + transit_ns_i;
        end
      end
      // ---- chans mirror: snoop the single TCTX write process -------------
      if (tram_we_w && (tram_waddr_w[3:0] == TW_CTRL_C))
        chans_r[TIDXW_C'(tram_waddr_w >> 4)] <= chn_clamp(tram_wdata_w[4:1]);
      //! disabled stream: clear its accumulation (flat-talker semantics)
      for (int t = 0; t < N_TALKERS_P; t++) begin
        if (!stream_en_i[t]) begin
          nsamp_r[t] <= '0;
          pend_r[t]  <= 1'b0;
        end
      end

      // ---- window read turnaround ---------------------------------------
      ext_trd_q_r <= ext_trd_go_w && !ext_trd_q_r;
      if (ext_trd_q_r) begin
        tctx_rd_data_o  <= tram_q_r;
        tctx_rd_valid_o <= 1'b1;
      end
    end
  end : pkt_engine

endmodule

`default_nettype wire

module capture_leaf #(
  parameter int LEGACY_P = 0,
  parameter int INPUT_LOOPBACK_P = 0, //! synchronous input-buffer source
  parameter int unsigned N_SLOTS_P = 32,   //! TX pair slots (prefix-sum space)
  parameter int unsigned N_TDM_P   = 8,    //! TDM slots (pairs = N_TDM_P/2)
  //! TDM FRAME HANDOFF (#617): the pairs one front-end frame delivers into
  //! the TDM bucket, pair 0 first. The strobe of pair TDM_CLOSE_SLOT_P
  //! closes the frame and publishes it whole; 1..N_TDM_P/2.
  parameter int unsigned TDM_FRAME_PAIRS_P = (N_TDM_P < 2) ? 1 : N_TDM_P / 2,
  //! the pair whose strobe closes the frame: the one of the frame that
  //! arrives last. The last pair kept on a TDM bus; on the I2S blend the I2S
  //! pair at slot 0, written a whole frame after its instant, after the TDM
  //! pairs kept (#632, KL_media_if_latency_pkg close_slot())
  parameter int unsigned TDM_CLOSE_SLOT_P = TDM_FRAME_PAIRS_P - 1,
  parameter int unsigned GAP_CYC_P = 24,   //! settle cycles between slot injects
  //! LOOP bucket sizing: the RX stream-channel space kept as pair queues
  //! (N_LB_STREAMS_P * N_LB_CH_P/2 pair queues x LB_QDEPTH_C x 48 b).
  //! Elaborate it down (1 / 2) on a build that has no listener to loop back
  //! from.
  parameter int unsigned N_LB_STREAMS_P = 8, //! RX streams kept (idxh < this)
  parameter int unsigned N_LB_CH_P      = 8  //! wire channels kept per stream
)(
  input  wire         clk_i,             //! datapath clock
  input  wire         rst_n,             //! active-low synchronous reset

  //! --- map RAM write port (root-selected producer / TB) ------------------
  //! PER-CHANNEL since 0x0027 (USER 2026-08-06: "one cluster == one audio
  //! channel"): the store holds one entry PER STREAM CHANNEL, each
  //! independently selecting one MONO cluster = {source bucket, stream
  //! (idxh), pair idx, half}. No pair coupling exists anywhere in the map:
  //! the old slot-granular store forced ATDECC edits into remove-both/
  //! add-both pair dances (vendor rules 2 and 3), which is exactly what
  //! this rework retires.
  input  wire         map_wr_en_i,       //! one-cycle write strobe
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_wr_addr_i, //! CHANNEL key
  input  wire [12:0]  map_wr_data_i,     //! {en[12], half[11], src[10:8],
                                         //!  idxh[7:4], idx[3:0]}
  //! --- map RAM readback port (registered, 1-cycle latency) ---------------
  input  wire         map_rd_en_i,       //! one-cycle read request
  input  wire [$clog2(2*N_SLOTS_P)-1:0] map_rd_addr_i, //! CHANNEL key
  //! {loop_fed[14], loop_mapped[13], entry[12:0]}. entry = the addressed
  //! CHANNEL's word {en, half, src, idxh, idx}. [14:13] is the LOOP bucket's
  //! CAPABILITY MASK: a loopback channel that is mapped but has never been
  //! FED emits 24'd0, bit-for-bit what a working-but-quiet one emits -
  //! without the mask an unwired listener side reports a LYING ZERO no
  //! counter contradicts (the AX7101 routes no audio pins, so its talkers
  //! depend ENTIRELY on the loop bucket).
  //!   mapped=0            : the bucket is not in use
  //!   mapped=1, fed=0     : mapped and NEVER FED - a silent talker here is
  //!                         a BINDING or stream fault, not quiet audio
  //!   mapped=1, fed=1     : live; zeros in the payload are real silence
  output logic [14:0] map_rd_data_o,     //! (valid with rd_valid)
  output logic        map_rd_valid_o,    //! read data valid this cycle
  //! the whole store as wires (the render side's map_flat_o precedent):
  //! entry k = channel k's {en, half, src, idxh, idx}. Pure fan-out of
  //! flops that already exist - zero logic - so the fabric's GET_AUDIO_MAP
  //! answer block can walk the OUTPUT-side mappings the same way it walks
  //! the render map, without arbitrating the CSR's read port.
  output logic [2*N_SLOTS_P*13-1:0] map_flat_o,

  //! --- I2S capture pair source (single stereo pair) ----------------------
  input  wire         i2s_pair_valid_i,  //! latch pulse
  input  wire [23:0]  i2s_l_i,
  input  wire [23:0]  i2s_r_i,

  //! --- TDM capture pair sources (indexed by pair slot) -------------------
  //! public_flat_rd: milan_datapath tied this to 1'b0 until 0x0042, which
  //! collapsed every capture pair into the SINGLE-pair I2S hold and made a
  //! physical cluster past channel 1 unbackable on every shape. "Does this
  //! port ever pulse" is the tie-off detector - and it must be the PORT, not
  //! the hold register behind it: a harness that leaves the codec data pins
  //! at zero writes the hold with zeros forever, so watching the hold for a
  //! CHANGE reports a dead feed as healthy (it did, first try).
  //! The pairs of one frame arrive pair 0 first (on the blend the I2S pair
  //! at slot 0 last); the strobe of pair TDM_CLOSE_SLOT_P closes the frame
  //! (TDM FRAME HANDOFF).
  input  wire         tdm_pair_valid_i /* verilator public_flat_rd */,  //! latch pulse
  input  wire [3:0]   tdm_pair_slot_i,   //! TDM pair index (0..N_TDM_P/2-1)
  input  wire [23:0]  tdm_l_i,
  input  wire [23:0]  tdm_r_i,
  //! #632: the instant the frame closed by THIS strobe started at the media
  //! interface (KL_media_domain_event mark_ns_o), low 32 bits, which are all
  //! an avtp_timestamp carries. It is banked with the frame and loaded into
  //! the walk with it, so tdm_walk_ns_o is the instant of exactly the frame
  //! the walk reads, the coincidence law and a queued tick included (TDM
  //! FRAME HANDOFF). Defaulted: an integration with no time base reads 0.
  input  wire [31:0]  tdm_close_ns_i = 32'd0,

  //! --- tone generator sample (live; drives both L/R when TONE) -----------
  input  wire [23:0]  tone_smp_i,

  //! --- LOOP source: the depacketizer payload AXIS clone (rx -> talker) ---
  //! Never backpressured (no tready): drive lb_tvalid_i with the tapped
  //! link's ACCEPTED beats (tvalid && tready), the same clone discipline as
  //! KL_chan_map_render's tap.
  //! ALL DEFAULTED: an integration that has not wired the listener side
  //! leaves them off and gets a bucket that is permanently silent - a
  //! DEFINED state, not a dangling pin.
  input  wire [63:0]  lb_tdata_i  = 64'd0, //! 2 consecutive S32BE samples,
                                         //! wire (channel-interleaved) order
  input  wire         lb_tvalid_i = 1'b0, //! accepted-beat strobe
  input  wire         lb_tlast_i  = 1'b0, //! one AXIS frame per PDU
  input  wire [3:0]   lb_tuser_i  = 4'd0, //! RX stream index s of this PDU
  //! per-stream wire channels_per_frame (7.3.3) - RX monitors' wire_chans_o
  input  wire [N_LB_STREAMS_P*4-1:0] lb_wire_chans_i = '0, //! fields; 0 -> 2
  //! bind wipe / stream-table eviction pulse per RX stream: empties the
  //! stream's pair queues, un-primes them and zeroes its holds, so no stale
  //! samples replay on a rebind. Defaulted off: an integration without a
  //! bind plane keeps the free-running behaviour.
  input  wire [N_LB_STREAMS_P-1:0] lb_flush_i = '0,
  //! #645 settle recentre pulse per RX stream: re-centres the stream's pair
  //! queues on the LB_TARGET_C fill at its next PDU (the LOOP QUEUE banner's
  //! RECENTRE). Defaulted off: an integration without the media plane's
  //! settle keeps the queues where their priming left them.
  input  wire [N_LB_STREAMS_P-1:0] lb_recentre_i = '0,

  //! --- media sample tick (one walk of the enabled slots per pulse) -------
  output wire input_capture_o, //! claim one buffer frame per capture walk
  output wire input_read_o, //! one mono request per synchronous source read
  output wire [5:0] input_addr_o, //! buffered input destination
  input wire [23:0] input_sample_i = '0, //! one-cycle RAM return
  input  wire         tick_i,

  //! --- pair injection to the shared packetizer (its capture contract) ----
  output logic        pair_valid_o,      //! one-cycle pulse per L/R pair
  output logic [4:0]  pair_slot_o,       //! pair slot 0..31 (widened space)
  output logic [23:0] pair_l_o,
  output logic [23:0] pair_r_o,

  //! --- LOOP queue slip evidence (saturating; ZERO with locked clocks) ----
  output logic [15:0] lb_dup_cnt_o,      //! empty-at-tick repeats (fed pairs)
  output logic [15:0] lb_skip_cnt_o,     //! dropped events (full / skid ovf)

  //! --- TDM junction slip evidence (saturating; ZERO with aligned grids) --
  //! The TDM bucket is written on the fsync grid and read on the media grid,
  //! so it slips one whole frame per beat period of the two rates (the shipping
  //! divider plan: -10.64 ppm = one frame per ~1.96 s), and until 0x0057
  //! NOTHING counted it - the LOOP counters watch only the queue bucket.
  //! One event per FRAME, not per pair: every pair shares the fsync clock,
  //! so they go stale together and a per-pair count would just multiply the
  //! same slip by the pair count.
  output logic [15:0] tdm_dup_cnt_o,     //! tick with no fresh frame (grid fast)
  output logic [15:0] tdm_skip_cnt_o,    //! frame over unread frame (grid slow)
  //! #632: the instant of the frame the walk reads (tdm_close_ns_i), held
  //! for the whole walk with the walk bank
  output logic [31:0] tdm_walk_ns_o
);
KL_chan_map_capture #(
  .INPUT_LOOPBACK_P(INPUT_LOOPBACK_P),
  .N_SLOTS_P(N_SLOTS_P),
  .N_TDM_P(N_TDM_P),
  .TDM_FRAME_PAIRS_P(TDM_FRAME_PAIRS_P),
  .TDM_CLOSE_SLOT_P(TDM_CLOSE_SLOT_P),
  .GAP_CYC_P(GAP_CYC_P),
  .N_LB_STREAMS_P(N_LB_STREAMS_P),
  .N_LB_CH_P(N_LB_CH_P)
) dut (
  .clk_i(clk_i),
  .rst_n(rst_n),
  .map_wr_en_i(map_wr_en_i),
  .map_wr_addr_i(map_wr_addr_i),
  .map_wr_data_i(map_wr_data_i),
  .map_rd_en_i(map_rd_en_i),
  .map_rd_addr_i(map_rd_addr_i),
  .map_rd_data_o(map_rd_data_o),
  .map_rd_valid_o(map_rd_valid_o),
  .map_flat_o(map_flat_o),
  .i2s_pair_valid_i(i2s_pair_valid_i),
  .i2s_l_i(i2s_l_i),
  .i2s_r_i(i2s_r_i),
  .tdm_pair_valid_i(tdm_pair_valid_i),
  .tdm_pair_slot_i(tdm_pair_slot_i),
  .tdm_l_i(tdm_l_i),
  .tdm_r_i(tdm_r_i),
  .tdm_close_ns_i(tdm_close_ns_i),
  .tone_smp_i(tone_smp_i),
  .lb_tdata_i((LEGACY_P != 0) ? lb_tdata_i : '0),
  .lb_tvalid_i((LEGACY_P != 0) ? lb_tvalid_i : '0),
  .lb_tlast_i((LEGACY_P != 0) ? lb_tlast_i : '0),
  .lb_tuser_i((LEGACY_P != 0) ? lb_tuser_i : '0),
  .lb_wire_chans_i((LEGACY_P != 0) ? lb_wire_chans_i : '0),
  .lb_flush_i((LEGACY_P != 0) ? lb_flush_i : '0),
  .lb_recentre_i((LEGACY_P != 0) ? lb_recentre_i : '0),
  .input_capture_o(input_capture_o),
  .input_read_o(input_read_o),
  .input_addr_o(input_addr_o),
  .input_sample_i(input_sample_i),
  .tick_i(tick_i),
  .pair_valid_o(pair_valid_o),
  .pair_slot_o(pair_slot_o),
  .pair_l_o(pair_l_o),
  .pair_r_o(pair_r_o),
  .lb_dup_cnt_o(lb_dup_cnt_o),
  .lb_skip_cnt_o(lb_skip_cnt_o),
  .tdm_dup_cnt_o(tdm_dup_cnt_o),
  .tdm_skip_cnt_o(tdm_skip_cnt_o),
  .tdm_walk_ns_o(tdm_walk_ns_o)
);
endmodule

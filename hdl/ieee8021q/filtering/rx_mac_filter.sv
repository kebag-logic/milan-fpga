/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : rx_mac_filter.sv
//  Project     : Milan TSN NIC — RX destination-MAC filter (REQ-MAC-02)
//
//  Description : Cut-through RX AXIS filter driven by a ternary CAM (tcam.sv).
//                It extracts the destination MAC from the first beat of each
//                frame, looks it up in the software-programmed TCAM database, and
//                passes or drops the whole frame based on the match:
//                  pass = match ? ~action[0]        // matched: action[0]=drop
//                               : default_pass_i     // miss: whitelist/blacklist
//                The matched action[7:1] is exposed (frame_action_o) so downstream
//                logic can steer the frame (e.g. control queue) if desired.
//
//                Whitelist: default_pass_i=0, add accept entries (action[0]=0).
//                Blacklist: default_pass_i=1, add drop entries (action[0]=1).
//
//                REQ-MAC-02 (2026-07-26): on top of the TCAM the block now
//                implements the 802.3 §4.2.4.2.2 station address filter that
//                the CSR ABI has advertised since 2026-07-01 but nothing in
//                fabric consumed - MAC_CTRL promisc/allmulti, MAC_ADDR_HI/LO
//                exact-match unicast and the MC_HASH_HI/LO multicast bucket
//                set. Decision order for a frame's first beat:
//
//                  runt (tlast at SOF)         -> drop, always
//                  promisc_i                   -> pass (tcpdump must see all)
//                  TCAM hit                    -> action[0] decides
//                  addr_filter_en_i            -> broadcast          -> pass
//                                                 group  -> allmulti | hash bit
//                                                 unicast-> == station_mac_i
//                  otherwise                   -> default_pass_i (legacy)
//
//                addr_filter_en_i is TCAM_CTRL[1], reset 0, so a build that
//                never sets it behaves exactly as before.
//
//                Assumes the 6-byte destination MAC lies entirely in beat 0
//                (true for TDATA_WIDTH>=48, e.g. the 64-bit datapath), so the
//                accept/drop decision is available before beat 0 is forwarded —
//                no store-and-forward buffering. The TCAM write port is exported
//                so milan_csr can add/remove entries (0x700 group).
//---------------------------------------------------------------------------//

`default_nettype none

module rx_mac_filter #(
    parameter int TDATA_WIDTH  = 64,
    parameter int NUM_ENTRIES  = 16,
    parameter int ACTION_WIDTH = 8,
    parameter int IDX_WIDTH    = (NUM_ENTRIES <= 1) ? 1 : $clog2(NUM_ENTRIES)
)(
    input  wire                     clk_i,
    input  wire                     rst_n,

    // ---- 802.3 station address filter (REQ-MAC-02, milan_csr 0x100) --------
    input  wire                     addr_filter_en_i, //! TCAM_CTRL[1]: apply the address filter on a TCAM miss
    input  wire                     promisc_i,        //! MAC_CTRL[2]: accept every frame
    input  wire                     allmulti_i,       //! MAC_CTRL[3]: accept every group address
    input  wire [47:0]              station_mac_i,    //! MAC_ADDR_HI/LO, MSB-first (byte 0 in [47:40])
    input  wire [63:0]              mc_hash_i,        //! MC_HASH_HI/LO: one bit per hash bucket

    // ---- filter policy + TCAM programming (from milan_csr 0x700) -----------
    input  wire                     default_pass_i, //! accept frames that miss the TCAM
    input  wire                     tcam_wr_en_i,
    input  wire [IDX_WIDTH-1:0]     tcam_wr_index_i,
    input  wire                     tcam_wr_valid_i,
    input  wire [47:0]              tcam_wr_key_i,
    input  wire [47:0]              tcam_wr_mask_i,
    input  wire [ACTION_WIDTH-1:0]  tcam_wr_action_i,

    // ---- RX AXIS in (from MAC/PTP) ----------------------------------------
    input  wire [TDATA_WIDTH-1:0]   s_tdata,
    input  wire [TDATA_WIDTH/8-1:0] s_tkeep,
    input  wire                     s_tvalid,
    input  wire                     s_tlast,
    output wire                     s_tready,

    // ---- RX AXIS out (filtered, to DMA) -----------------------------------
    output wire [TDATA_WIDTH-1:0]   m_tdata,
    output wire [TDATA_WIDTH/8-1:0] m_tkeep,
    output wire                     m_tvalid,
    output wire                     m_tlast,
    input  wire                     m_tready,

    // ---- status (per accepted frame) --------------------------------------
    output wire [ACTION_WIDTH-1:0]  frame_action_o, //! action of the current frame's match
    output wire                     frame_match_o,  //! current frame hit a TCAM entry
    output wire                     frame_dropped_o //! current frame is being dropped
);

  // -----------------------------------------------------------------------
  //  Destination MAC = first 6 bytes on the wire (byte 0 = MAC MSB).
  //  AXIS byte lane 0 (tdata[7:0]) carries byte 0, so swap into MAC order.
  // -----------------------------------------------------------------------
  wire [47:0] dmac = { s_tdata[7:0],   s_tdata[15:8],  s_tdata[23:16],
                       s_tdata[31:24], s_tdata[39:32], s_tdata[47:40] };

  // -----------------------------------------------------------------------
  //  802.3 station address filter (REQ-MAC-02). All combinational off beat 0.
  // -----------------------------------------------------------------------
  //! I/G bit = the LEAST significant bit of the FIRST octet, i.e. dmac[40].
  wire dmac_group = dmac[40];
  //! The broadcast address is accepted by every conformant station.
  wire dmac_bcast = &dmac;
  //! Multicast hash bucket. DEFINED HERE (nothing specified one before): a
  //! 6-bit XOR fold of the 48-bit address, MSB-aligned groups of 6. Chosen
  //! over an ether_crc fold because it is a handful of XOR gates instead of a
  //! 48-bit CRC cone and the driver can reproduce it in two lines - the exact
  //! function only has to MATCH between HW and `ndo_set_rx_mode`, and the
  //! filter is approximate by construction either way (docs/reference/REGISTER_MAP.md 0x114).
  wire [5:0] mc_index = dmac[47:42] ^ dmac[41:36] ^ dmac[35:30] ^ dmac[29:24]
                      ^ dmac[23:18] ^ dmac[17:12] ^ dmac[11:6]  ^ dmac[5:0];
  wire mc_hit = mc_hash_i[mc_index];
  //! Address-filter verdict for a frame that missed the TCAM.
  wire addr_pass = dmac_bcast ? 1'b1
                 : dmac_group ? (allmulti_i | mc_hit)
                              : (dmac == station_mac_i);
  //! Miss policy: the address filter when armed, else the legacy blanket bit.
  wire miss_pass = addr_filter_en_i ? addr_pass : default_pass_i;

  wire                    match;
  wire [ACTION_WIDTH-1:0] action;

  tcam #(
    .KEY_WIDTH(48), .NUM_ENTRIES(NUM_ENTRIES), .ACTION_WIDTH(ACTION_WIDTH)
  ) mac_cam (
    .clk_i(clk_i), .rst_n(rst_n),
    .wr_en_i(tcam_wr_en_i), .wr_index_i(tcam_wr_index_i), .wr_valid_i(tcam_wr_valid_i),
    .wr_key_i(tcam_wr_key_i), .wr_mask_i(tcam_wr_mask_i), .wr_action_i(tcam_wr_action_i),
    .lookup_key_i(dmac),
    .match_o(match), .match_index_o(), .match_action_o(action), .match_vec_o()
  );

  // -----------------------------------------------------------------------
  //  Per-frame decision, latched at start-of-frame (SOF) and held to tlast.
  // -----------------------------------------------------------------------
  reg                    in_frame;   //! high after SOF, until tlast accepted
  reg                    pass_r;     //! latched pass decision for the frame
  reg [ACTION_WIDTH-1:0] action_r;   //! latched action for the frame
  reg                    match_r;    //! latched match flag for the frame

  wire sof       = s_tvalid && !in_frame;                          //! first beat of a frame
  //! runt guard: a frame whose FIRST beat carries tlast is at most 8 bytes -
  //! no legal Ethernet frame. Upstream pipeline warts can mint such ghosts
  //! at drop-frame tails (dp TB 2026-07-19); swallow them here so the host
  //! DMA never sees them, whatever their origin.
  wire runt_sof  = sof && s_tlast;
  //! SOF decision. promisc outranks an explicit TCAM drop on purpose: MAC_CTRL
  //! promiscuous means "hand me the wire", which is exactly what a capture
  //! needs; a drop entry is a filtering policy and filtering is what promisc
  //! switches off.
  wire pass_sof  = runt_sof  ? 1'b0
                 : promisc_i ? 1'b1
                 : match     ? ~action[0] : miss_pass;             //! SOF decision
  wire pass_now  = sof ? pass_sof : pass_r;                        //! decision applied this beat

  // Cut-through: forward when passing, silently consume when dropping.
  assign m_tvalid = s_tvalid & pass_now;
  assign m_tdata  = s_tdata;
  assign m_tkeep  = s_tkeep;
  assign m_tlast  = s_tlast;
  assign s_tready = pass_now ? m_tready : 1'b1;   //! drop => always ready to consume

  wire beat_acc = s_tvalid & s_tready;

  always_ff @(posedge clk_i) begin : frame_fsm
    if (!rst_n) begin
      in_frame <= 1'b0; pass_r <= 1'b0; action_r <= '0; match_r <= 1'b0;
    end else if (beat_acc) begin
      if (sof) begin
        pass_r   <= pass_sof;
        action_r <= action;
        match_r  <= match;
      end
      in_frame <= ~s_tlast;    // clear at end of frame, set within a frame
    end
  end

  assign frame_action_o  = sof ? action   : action_r;
  assign frame_match_o   = sof ? match     : match_r;
  assign frame_dropped_o = ~pass_now;

endmodule

`default_nettype wire

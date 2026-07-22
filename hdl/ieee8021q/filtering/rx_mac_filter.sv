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
  //! at drop-frame tails (dp TB 2026-07-19); swallow them here so the kernel
  //! DMA never sees them, whatever their origin.
  wire runt_sof  = sof && s_tlast;
  wire pass_sof  = runt_sof ? 1'b0
                 : match    ? ~action[0] : default_pass_i;         //! SOF decision
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

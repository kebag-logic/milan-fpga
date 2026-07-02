/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : tcam.sv
//  Project     : Milan TSN NIC — RX frame steering / filtering
//
//  Description : Small register-based **ternary CAM (TCAM)** used as a
//                destination-MAC "database": a table of {key, mask, action}
//                entries that software can add / remove / update, and against
//                which an incoming destination MAC is matched every lookup.
//
//                Ternary = each entry carries a per-bit *mask*: mask bit 1 means
//                "this key bit must match", 0 means "don't care" (wildcard). That
//                lets one entry cover a range/prefix — e.g. the reserved multicast
//                block 01-80-C2-00-00-0x (mask FF:FF:FF:FF:FF:F0) or a whole OUI —
//                which an exact-match CAM (e.g. Forencich verilog-cam, a *binary*
//                CAM) cannot express. See hdl/common/doc/tcam.md.
//
//                Register-based parallel match is the right choice for a small
//                filter table (tens of entries): every entry compares in one
//                cycle; a priority encoder returns the lowest matching index
//                (index 0 = highest priority) and its action.
//
//  Typical use : steer control frames by destination MAC (gPTP 01-80-C2-00-00-0E,
//                AVDECC/ADP 91-E0-F0-01-00-00, MAAP stream multicasts, broadcast)
//                to a control/stream queue or an accept/drop decision — the exact
//                + ternary replacement for the approximate MC_HASH filter
//                (REQ-MAC-02).
//---------------------------------------------------------------------------//

`default_nettype none

module tcam #(
    parameter int KEY_WIDTH    = 48,   //! match key width (48 = destination MAC)
    parameter int NUM_ENTRIES  = 16,   //! table depth (register-based; keep small)
    parameter int ACTION_WIDTH = 8,    //! per-entry action/tag width
    parameter int IDX_WIDTH    = (NUM_ENTRIES <= 1) ? 1 : $clog2(NUM_ENTRIES)
)(
    input  wire                    clk_i,
    input  wire                    rst_n,

    // ---- entry write port: add / update / remove one entry -----------------
    input  wire                    wr_en_i,      //! commit a write this cycle
    input  wire [IDX_WIDTH-1:0]    wr_index_i,   //! entry to write
    input  wire                    wr_valid_i,   //! 1 = add/update entry, 0 = remove (invalidate)
    input  wire [KEY_WIDTH-1:0]    wr_key_i,     //! entry match value
    input  wire [KEY_WIDTH-1:0]    wr_mask_i,    //! per-bit care mask (1 = compare, 0 = wildcard)
    input  wire [ACTION_WIDTH-1:0] wr_action_i,  //! action/tag returned on a hit

    // ---- lookup port (combinational match) ---------------------------------
    input  wire [KEY_WIDTH-1:0]    lookup_key_i,     //! key to search (e.g. dest MAC)
    output wire                    match_o,          //! 1 = at least one entry matched
    output wire [IDX_WIDTH-1:0]    match_index_o,    //! lowest matching entry index (highest priority)
    output wire [ACTION_WIDTH-1:0] match_action_o,   //! action of the winning entry
    output wire [NUM_ENTRIES-1:0]  match_vec_o       //! raw per-entry hit vector (debug / multi-hit)
);

  // -----------------------------------------------------------------------
  //  Entry storage (registers)
  // -----------------------------------------------------------------------
  reg                    ent_valid  [NUM_ENTRIES-1:0];
  reg [KEY_WIDTH-1:0]    ent_key    [NUM_ENTRIES-1:0];
  reg [KEY_WIDTH-1:0]    ent_mask   [NUM_ENTRIES-1:0];
  reg [ACTION_WIDTH-1:0] ent_action [NUM_ENTRIES-1:0];

  integer r;
  always_ff @(posedge clk_i) begin : entry_write
    if (!rst_n) begin
      for (r = 0; r < NUM_ENTRIES; r = r + 1) ent_valid[r] <= 1'b0; // invalidate all (fast clear)
    end else if (wr_en_i) begin
      ent_valid [wr_index_i] <= wr_valid_i;
      ent_key   [wr_index_i] <= wr_key_i;
      ent_mask  [wr_index_i] <= wr_mask_i;
      ent_action[wr_index_i] <= wr_action_i;
    end
  end

  // -----------------------------------------------------------------------
  //  Parallel ternary match: hit[i] = valid & ((key ^ ent_key) & mask) == 0
  // -----------------------------------------------------------------------
  reg [NUM_ENTRIES-1:0] hit;
  integer m;
  always_comb begin : match_logic
    for (m = 0; m < NUM_ENTRIES; m = m + 1)
      hit[m] = ent_valid[m] && (((lookup_key_i ^ ent_key[m]) & ent_mask[m]) == {KEY_WIDTH{1'b0}});
  end

  // -----------------------------------------------------------------------
  //  Priority encode: lowest index wins (evaluate high->low so index 0 last)
  // -----------------------------------------------------------------------
  reg                    match_any;
  reg [IDX_WIDTH-1:0]    match_idx;
  reg [ACTION_WIDTH-1:0] match_act;
  integer p;
  always_comb begin : prio_encode
    match_any = 1'b0;
    match_idx = {IDX_WIDTH{1'b0}};
    match_act = {ACTION_WIDTH{1'b0}};
    for (p = NUM_ENTRIES-1; p >= 0; p = p - 1) begin
      if (hit[p]) begin
        match_any = 1'b1;
        match_idx = p[IDX_WIDTH-1:0];
        match_act = ent_action[p];
      end
    end
  end

  assign match_vec_o    = hit;
  assign match_o        = match_any;
  assign match_index_o  = match_idx;
  assign match_action_o = match_act;

endmodule

`default_nettype wire

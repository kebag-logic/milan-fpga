/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : adp_tx_arbiter.sv
//  Project     : Milan ADP  (MAC TX integration)
//
//  Description : Two-input AXI4-Stream *packet* arbiter that merges the ADP
//                advertiser's frames (`s_adp`) with the normal shaped datapath
//                (`s_data`) into the single MAC TX stream (`m`). It grants at
//                frame boundaries and locks the granted source until its `tlast`,
//                so **a frame is never interrupted mid-packet** and ADP frames are
//                only ever inserted in inter-frame gaps of the datapath.
//
//                Arbitration is round-robin (grant alternates between the two
//                sources) so neither can be starved: the low-rate ADP stream is
//                always served in a gap, and the datapath is never blocked by ADP
//                for more than the ADP frame in flight.
//
//  Latency     : combinational grant (no start-of-frame bubble); fully
//                back-pressure safe — `m.tready` is routed only to the granted
//                source, the other source sees `tready = 0`.
//
//  Robustness  : the lock is supervised. A granted source that goes silent
//                mid-frame (no beat for 2^TO_LOG2_P cycles with `tvalid` low)
//                would otherwise hold the grant FOREVER and every source
//                behind this mux — eight of these are cascaded into the one
//                MAC TX trunk — is dead with it (the 07-29 silicon wedge
//                class: all TX stops, RX perfect, no reset reaches the lock).
//                On that timeout the arbiter closes the open frame itself
//                (one injected zero-data `tlast` beat), releases the lock and
//                pulses `abort_evt_o`. HONEST BOUND: the MAC recomputes a
//                VALID CRC over the truncated bytes (with_preamble_crc=True),
//                so the closed frame egresses as a well-formed L2 runt with a
//                zeroed tail — one malformed-content frame per abort event
//                (an AVTP listener sees a sequence step), traded against a
//                permanently dead port. The same counter expiring with
//                `tvalid` HIGH means the stall is downstream — nothing to
//                release, so it only pulses `stall_evt_o`: the two pulses
//                are the H1-vs-H2 verdict the wedge forensics lacked. A
//                flush whose injected beat is itself refused for a further
//                whole window reports `stall_evt_o` too — the block is
//                below, and the abort verdict alone would misattribute it.
//---------------------------------------------------------------------------//

`default_nettype none

module adp_tx_arbiter #(
    parameter int DATA_WIDTH = 64,
    parameter int KEEP_WIDTH = DATA_WIDTH/8,
    parameter int TO_LOG2_P  = 17          //! lock watchdog: 2^N cycles without
                                           //! an accepted beat (~2.6 ms at
                                           //! 50 MHz — legal stalls are frame
                                           //! time + the 512-cycle IFG gasket,
                                           //! orders of magnitude below)
)(
    input  wire                    clk_i,
    input  wire                    rst_n,

    // ---- slave 0: normal datapath (shaper -> MAC) ----
    input  wire [DATA_WIDTH-1:0]   s_data_tdata,
    input  wire [KEEP_WIDTH-1:0]   s_data_tkeep,
    input  wire                    s_data_tvalid,
    input  wire                    s_data_tlast,
    output wire                    s_data_tready,

    // ---- slave 1: ADP advertiser ----
    input  wire [DATA_WIDTH-1:0]   s_adp_tdata,
    input  wire [KEEP_WIDTH-1:0]   s_adp_tkeep,
    input  wire                    s_adp_tvalid,
    input  wire                    s_adp_tlast,
    output wire                    s_adp_tready,

    // ---- master: to MAC TX ----
    output wire [DATA_WIDTH-1:0]   m_tdata,
    output wire [KEEP_WIDTH-1:0]   m_tkeep,
    output wire                    m_tvalid,
    output wire                    m_tlast,
    input  wire                    m_tready,

    // ---- lock supervision (A_TXARB_DIAG 0x784) ----
    output wire                    diag_locked_o,  //! live: a grant is held
    output logic                   abort_evt_o,    //! pulse: source went silent
                                                   //! mid-frame, frame closed +
                                                   //! lock released here
    output logic                   stall_evt_o     //! pulse: downstream refused
                                                   //! a presented beat for the
                                                   //! whole window (nothing to
                                                   //! release — the block is
                                                   //! BELOW this mux)
);

  // sel: 0 = datapath, 1 = adp
  reg  locked_r;        //! a source is granted and being forwarded until tlast
  reg  sel_r;           //! the granted source while locked
  reg  last_grant_r;    //! last source granted (for round-robin fairness)
  reg  flush_r;         //! closing an abandoned frame with an injected tlast
  reg [TO_LOG2_P:0] to_cnt_r;  //! cycles the held lock has made no progress

  // Combinational grant: while locked keep sel_r; else pick a valid source,
  // preferring the one that was NOT granted last (round-robin).
  logic gsel;           //! source selected this cycle
  logic active;         //! a source is selected (locked or a fresh grant)
  always_comb begin
    gsel   = sel_r;
    active = locked_r;
    if (!locked_r) begin
      active = s_data_tvalid | s_adp_tvalid;
      if (s_data_tvalid && s_adp_tvalid) gsel = ~last_grant_r; // both -> alternate
      else if (s_adp_tvalid)             gsel = 1'b1;
      else                               gsel = 1'b0;
    end
  end

  // Output mux + per-source ready routing. While flushing, the injected beat
  // owns the bus: tvalid/tlast forced, keep forced full (the frame is already
  // lost to FCS — the beat exists only to close it), and neither source may
  // slip a beat in underneath.
  assign m_tvalid      = (active & (gsel ? s_adp_tvalid : s_data_tvalid)) | flush_r;
  assign m_tdata       = flush_r ? '0 : (gsel ? s_adp_tdata : s_data_tdata);
  assign m_tkeep       = flush_r ? {KEEP_WIDTH{1'b1}}
                                 : (gsel ? s_adp_tkeep : s_data_tkeep);
  assign m_tlast       = (gsel ? s_adp_tlast : s_data_tlast) | flush_r;
  assign s_data_tready = active & ~gsel & m_tready & ~flush_r;
  assign s_adp_tready  = active &  gsel & m_tready & ~flush_r;

  assign diag_locked_o = locked_r;

  wire beat_accepted = m_tvalid & m_tready;
  wire src_tvalid_w  = gsel ? s_adp_tvalid : s_data_tvalid;  //! the held source
  wire to_expired_w  = to_cnt_r[TO_LOG2_P];

  always_ff @(posedge clk_i) begin : lock_fsm
    if (!rst_n) begin
      locked_r <= 1'b0; sel_r <= 1'b0; last_grant_r <= 1'b0;
      flush_r  <= 1'b0; to_cnt_r <= '0;
      abort_evt_o <= 1'b0; stall_evt_o <= 1'b0;
    end else begin
      abort_evt_o <= 1'b0;
      stall_evt_o <= 1'b0;

      // lock onto the granted source at first PRESENTATION (not first
      // acceptance): locking on accept let gsel flip mid-stall when the
      // second source turned valid (round-robin re-evaluated), mutating
      // m_tdata/m_tlast under m_tvalid && !m_tready - an AXIS stability
      // violation at the MAC boundary (Opus review 2026-07-29). A source
      // that asserts tvalid must hold it to acceptance (AXIS), so locking
      // at presentation cannot deadlock.
      if (!locked_r && m_tvalid && !flush_r) begin
        locked_r <= 1'b1; sel_r <= gsel;
      end

      if (flush_r) begin
        // the injected close beat is on the bus; it leaves with m_tready
        if (m_tready) begin
          flush_r <= 1'b0; locked_r <= 1'b0; last_grant_r <= sel_r;
        end
      end
      // normal release at end-of-frame (wins a same-cycle single-beat frame)
      else if (active && beat_accepted && m_tlast) begin
        locked_r     <= 1'b0;
        last_grant_r <= gsel;
      end

      // lock watchdog: a held grant making no progress for a full window.
      // The verdict at expiry is the wedge forensics: tvalid HIGH = the
      // refusal is below this mux (report only - releasing cannot help),
      // tvalid LOW = the granted source abandoned its frame (close + free).
      // The counter keeps counting THROUGH a flush: an injected beat that is
      // itself refused for a whole further window is a downstream stall and
      // must say so - clearing on flush_r left that state permanently
      // silent behind an abort verdict (Opus verify D4).
      if (!locked_r || beat_accepted) to_cnt_r <= '0;
      else if (to_expired_w) begin
        to_cnt_r <= '0;
        if (flush_r || src_tvalid_w) stall_evt_o <= 1'b1;
        else begin
          abort_evt_o <= 1'b1;
          flush_r     <= 1'b1;
        end
      end
      else to_cnt_r <= to_cnt_r + 1'b1;
    end
  end

endmodule

`default_nettype wire

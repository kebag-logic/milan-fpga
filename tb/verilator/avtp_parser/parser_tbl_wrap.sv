/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

/*
------------------------------------------------------------------------------
  File        : parser_tbl_wrap.sv
  Author      : Kebag Logic

  Date        : 2026-07-26
  Description : Verilator harness wrapper for the RX listener VERDICT chain as
                milan_datapath wires it (docs/overview/ARCHITECTURE.md): the
                KL_stream_table authority (entry-0 ACMP alias + CSR-window
                overrides) feeding avtp_stream_parser's N-way stream_id
                compare, at a FULL-WIDTH index port so N=8 is expressible
                (tb/verilator/avtp_stream/stream_table_wrap.sv pins the index
                to [1:0] and therefore cannot carry entries 4..7).

                Everything the 0x8B4 APRB probe group reports is derivable
                from these ports WITHOUT replicating milan_datapath's latch:
                `tbl_en_o` popcount = the armed-entry count, `parse_valid_o` /
                `match_valid_o` = the parsed/matched counter increments, and
                `stream_id_o` = the stream_id as lifted off the wire. The
                harness models the probe in C++ instead of in RTL so a defect
                in the real latch can never be masked by a mirror of itself.

  Company     : Kebag Logic
  Project     : Milan AVTP
------------------------------------------------------------------------------
*/

`default_nettype none

module parser_tbl_wrap #(
  parameter int unsigned N_LISTENERS_P = 8   //! table depth = parser N_STREAMS
)(
  input  wire        clk,             //! clock
  input  wire        resetn,          //! synchronous active-low reset

  //! --- stream-0 legacy authority (ACMP listener SM bound record) ----------
  input  wire        bound0_i,        //! sink 0 bound (level)
  input  wire [63:0] sid0_i,          //! sink 0 bound stream_id

  //! --- CSR-window override/write port (P11 hook) --------------------------
  input  wire        wr_en_i,         //! one-cycle write strobe
  input  wire [3:0]  wr_idx_i,        //! entry index
  input  wire [63:0] wr_sid_i,        //! entry stream_id
  input  wire        wr_valid_i,      //! entry enable (0 = evict)

  //! --- monitored RX AXI-Stream (observed, never driven) -------------------
  input  wire [63:0] s_tdata_i,
  input  wire [7:0]  s_tkeep_i,
  input  wire        s_tvalid_i,
  input  wire        s_tready_i,
  input  wire        s_tlast_i,

  //! --- verdict + pre-match evidence (the APRB probe sources) --------------
  output wire        match_valid_o,   //! stream_id hit an ARMED entry
  output wire [(N_LISTENERS_P <= 1 ? 1 : $clog2(N_LISTENERS_P))-1:0]
                     match_index_o,   //! matched entry index
  output wire [63:0] stream_id_o,     //! stream_id AS LIFTED OFF THE WIRE
  output wire [7:0]  subtype_o,       //! that frame's AVTP subtype
  output wire        parse_valid_o,   //! parse fired (matched or not)
  output wire [31:0] avtp_frames_o,   //! APRB_PARSED source
  output wire [31:0] matched_frames_o,//! APRB_MATCHED source
  output wire [N_LISTENERS_P-1:0] bind_rise_o, //! per-entry bind edge
  output wire [N_LISTENERS_P-1:0] tbl_en_o     //! armed entries (popcount = APRB armed)
);

  wire [64*N_LISTENERS_P-1:0] tbl_sid_w;

  KL_stream_table #(.N_LISTENERS_P(N_LISTENERS_P)) u_tbl (
    .clk_i       (clk),
    .rst_n       (resetn),
    .bound0_i    (bound0_i),
    .sid0_i      (sid0_i),
    .wr_en_i     (wr_en_i),
    .wr_idx_i    (wr_idx_i),
    .wr_sid_i    (wr_sid_i),
    .wr_valid_i  (wr_valid_i),
    .tbl_sid_o   (tbl_sid_w),
    .tbl_en_o    (tbl_en_o),
    .bind_rise_o (bind_rise_o)
  );

  avtp_stream_parser #(
    .TDATA_WIDTH (64),
    .BIG_ENDIAN  (0),
    .N_STREAMS   (N_LISTENERS_P)
  ) u_par (
    .clk              (clk),
    .resetn           (resetn),
    .cfg_stream_id_i  (tbl_sid_w),
    .cfg_stream_en_i  (tbl_en_o),
    .s_tdata_i        (s_tdata_i),
    .s_tkeep_i        (s_tkeep_i),
    .s_tvalid_i       (s_tvalid_i),
    .s_tready_i       (s_tready_i),
    .s_tlast_i        (s_tlast_i),
    .match_valid_o    (match_valid_o),
    .match_index_o    (match_index_o),
    .stream_id_o      (stream_id_o),
    .avtp_ts_o        (),
    .subtype_o        (subtype_o),
    .ts_valid_o       (),
    .seq_num_o        (),
    .ts_uncertain_o   (),
    .fsh_o            (),
    .fsh2_o           (),
    .parse_valid_o    (parse_valid_o),
    .b3_o             (),
    .avtp_frames_o    (avtp_frames_o),
    .matched_frames_o (matched_frames_o)
  );

endmodule

`default_nettype wire

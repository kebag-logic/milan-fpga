/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mrp_strip.sv
//  Project     : IEEE 1722.1 protocol processor (docs/architecture/03 §3 V9,
//                10 §4 MRPDU RX queue)
//
//  Description : THE RECORDED SEAM between the RX validator and the SRP
//                engine. KL_pp_rx_validator's V9 pass-through emits the
//                whole MRP frame byte-exact from DA byte 0 with no ready;
//                KL_srp_top's decoder expects a header-stripped MRPDU
//                (ProtocolVersion first) WITH backpressure (mrp_ready may
//                drop while packed values drain). This shim:
//                  - drops wire bytes 0..13 (DA + SA + EtherType) and
//                    forwards bytes 14.. unchanged;
//                  - derives the msrp/mvrp select from the EtherType bytes
//                    it strips (0x22EA = MSRP, 0x88F5 = MVRP) — the landed
//                    validator exports no select of its own, only the
//                    byte-exact frame (V9 already guaranteed DA/EtherType
//                    pairing, so the EtherType alone is authoritative);
//                  - absorbs the rate mismatch in the 10 §4 MRPDU RX queue
//                    (P-MRPDU-QUEUE-BYTES, F01.5 default 2048), realized as
//                    one sync-read RAM of {msrp, last, data} entries with a
//                    tentative/committed write pointer: a frame that
//                    overflows the queue is rewound WHOLE and counted in
//                    drop_count_o — the decoder never sees a torn MRPDU.
//
//                The one design decision that matters: the queue commits
//                per FRAME, not per byte. The SRP decoder's malformed-PDU
//                tolerance is for wire garbage, not for queue artifacts, so
//                an overflow here must erase the whole frame instead of
//                truncating it into a plausible-but-wrong MRPDU.
//---------------------------------------------------------------------------//
`default_nettype none

module KL_mrp_strip #(
    //! P-MRPDU-QUEUE-BYTES (F01.5): MRPDU RX queue capacity in bytes
    parameter int unsigned QUEUE_BYTES_P = 2048,
    //! derived: queue address width — do not override
    localparam int unsigned AW_C = $clog2(QUEUE_BYTES_P)
) (
    input  wire         clk_i,        //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,        //! synchronous active-low reset

    //! ---- validator V9 pass-through in (no ready: never backpressured) ----
    input  wire         in_valid_i,   //! MRPDU byte strobe (frame from DA byte 0)
    input  wire  [7:0]  in_data_i,    //! byte-exact frame byte
    input  wire         in_last_i,    //! final byte of the frame

    //! ---- header-stripped MRPDU stream out (KL_srp_top mrp_* face) ----
    output logic        out_valid_o,  //! byte present (held until out_ready_i)
    output logic [7:0]  out_data_o,   //! MRPDU byte, ProtocolVersion first
    output logic        out_last_o,   //! final byte of this MRPDU
    output logic        out_msrp_o,   //! 1 = MSRP (0x22EA), 0 = MVRP (0x88F5)
    input  wire         out_ready_i,  //! consumer pop (decoder mrp_ready_o)

    //! ---- observability ----
    output logic [15:0] drop_count_o  //! whole frames erased on overflow (saturates)
);

  localparam logic [15:0] ET_MSRP_C = 16'h22EA;

  // entry = {msrp, last, data[7:0]}
  logic [9:0]      ram_r [QUEUE_BYTES_P];
  logic [9:0]      ram_q_r;

  // pointers carry one extra wrap bit; wr_cmt_r = committed, wr_tent_r =
  // in-frame tentative, rd_ptr_r = consumer side
  logic [AW_C:0]   wr_cmt_r, wr_tent_r, rd_ptr_r;

  // write-side frame walk
  logic [3:0]      hdr_idx_r;    // 0..14 saturating wire-byte index
  logic [15:0]     et_r;         // captured EtherType (bytes 12..13)
  logic            drop_r;       // overflow hit: swallow the rest of the frame
  logic            msrp_w;
  logic            body_w;       // this byte belongs to the MRPDU body
  logic            full_w;       // no room for one more tentative byte

  assign msrp_w = (et_r == ET_MSRP_C);
  assign body_w = in_valid_i && (hdr_idx_r == 4'd14);
  assign full_w = ((wr_tent_r - rd_ptr_r) == (AW_C+1)'(QUEUE_BYTES_P));

  always_ff @(posedge clk_i) begin : wr_side
    if (!rst_n) begin
      wr_cmt_r     <= '0;
      wr_tent_r    <= '0;
      hdr_idx_r    <= 4'd0;
      et_r         <= 16'd0;
      drop_r       <= 1'b0;
      drop_count_o <= 16'd0;
    end else begin
      if (in_valid_i) begin
        // wire-byte walk: capture the EtherType as it streams past
        if (hdr_idx_r == 4'd12) et_r[15:8] <= in_data_i;
        if (hdr_idx_r == 4'd13) et_r[7:0]  <= in_data_i;
        if (hdr_idx_r != 4'd14) hdr_idx_r <= hdr_idx_r + 4'd1;

        if (body_w && !drop_r) begin
          if (full_w) begin
            // overflow: rewind the WHOLE frame, count once
            wr_tent_r <= wr_cmt_r;
            drop_r    <= 1'b1;
            if (drop_count_o != 16'hFFFF) begin
              drop_count_o <= drop_count_o + 16'd1;
            end
          end else begin
            ram_r[wr_tent_r[AW_C-1:0]] <= {msrp_w, in_last_i, in_data_i};
            if (in_last_i) begin
              wr_cmt_r  <= wr_tent_r + (AW_C+1)'(1);  // commit the frame
              wr_tent_r <= wr_tent_r + (AW_C+1)'(1);
            end else begin
              wr_tent_r <= wr_tent_r + (AW_C+1)'(1);
            end
          end
        end

        if (in_last_i) begin
          // frame over: reset the walk (a runt < 15 B commits nothing)
          hdr_idx_r <= 4'd0;
          drop_r    <= 1'b0;
        end
      end
    end
  end

  // read side: first-word-fall-through with one skid entry so the stream
  // sustains one byte per cycle into the decoder
  logic       out_vld_r;
  logic [9:0] out_ent_r;
  logic       skid_vld_r;
  logic [9:0] skid_ent_r;
  logic       fetch_r;      // RAM read issued last cycle, ram_q_r valid now
  logic       avail_w;      // committed entries beyond rd_ptr_r
  logic       space_w;      // output pipeline can take the fetched entry
  logic       pop_w;

  assign avail_w = (rd_ptr_r != wr_cmt_r);
  assign pop_w   = out_vld_r && out_ready_i;
  // entries held or in flight never exceed out + skid
  assign space_w = !(out_vld_r && skid_vld_r) && !(skid_vld_r && fetch_r)
                 && !(out_vld_r && fetch_r && !out_ready_i);

  always_ff @(posedge clk_i) begin : rd_side
    if (!rst_n) begin
      rd_ptr_r   <= '0;
      out_vld_r  <= 1'b0;
      out_ent_r  <= 10'd0;
      skid_vld_r <= 1'b0;
      skid_ent_r <= 10'd0;
      fetch_r    <= 1'b0;
      ram_q_r    <= 10'd0;
    end else begin
      // stage 1: issue a sync read whenever the pipeline has room
      if (avail_w && space_w) begin
        ram_q_r  <= ram_r[rd_ptr_r[AW_C-1:0]];
        rd_ptr_r <= rd_ptr_r + (AW_C+1)'(1);
        fetch_r  <= 1'b1;
      end else begin
        fetch_r  <= 1'b0;
      end

      // stage 2: land the fetched entry in out or skid; drain skid on pop
      if (pop_w) begin
        if (skid_vld_r) begin
          out_ent_r  <= skid_ent_r;
          skid_vld_r <= 1'b0;
          if (fetch_r) begin
            skid_ent_r <= ram_q_r;
            skid_vld_r <= 1'b1;
          end
        end else if (fetch_r) begin
          out_ent_r <= ram_q_r;
        end else begin
          out_vld_r <= 1'b0;
        end
      end else begin
        if (fetch_r) begin
          if (!out_vld_r) begin
            out_ent_r <= ram_q_r;
            out_vld_r <= 1'b1;
          end else begin
            skid_ent_r <= ram_q_r;
            skid_vld_r <= 1'b1;
          end
        end
      end
    end
  end

  assign out_valid_o = out_vld_r;
  assign out_msrp_o  = out_ent_r[9];
  assign out_last_o  = out_ent_r[8];
  assign out_data_o  = out_ent_r[7:0];

endmodule : KL_mrp_strip
`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_mbx_dma.sv
//  Project     : Milan FPGA Platform (packet mailbox, #665)
//
//  Description : The split placement's record mover. It copies one record's
//                payload between a mailbox ring and the CPU's memory, so the
//                hart does not move each word over its uncached bus (#665,
//                owner decision 2026-10-29; NFR-SCOUT-03). It sits on
//                KL_mbx's host port, between KL_mbx_wb and KL_mbx, and
//                masters the CPU's coherent DMA port (AXI4, 32-bit data,
//                INCR bursts of at most sixteen beats that never cross a
//                64-byte line). A receive transfer reads a chunk of ring
//                words into a sixteen-word buffer and writes it to memory as
//                one burst; a transmit transfer reads a burst from memory
//                and writes each beat to the ring as it arrives.
//
//                The one decision that matters: the mover adds nothing to
//                the mailbox contract. It reads and writes the ring words a
//                driver's own word loop would, in ring order, with every
//                byte past the record's length zero in a transmit ring word
//                and left untouched in memory by a receive transfer (its
//                last beat's byte strobes). The record's header words, the
//                counters and the doorbells stay the driver's. While a
//                transfer runs the mover owns the host port; an access the
//                CPU makes meanwhile is held and made when the transfer
//                ends, so the window's accesses never interleave with a
//                record's words.
//
//                A start with a memory address off a word, or while a
//                transfer runs, is refused and sets the error flag; an error
//                response ends the transfer at its burst and sets it too.
//                The flag holds until the next accepted start. Responses on
//                the DMA port are the CPU's own interconnect's, which
//                answers every request, so there is no timeout here, as
//                there is none on the CPU's own bus accesses.
//---------------------------------------------------------------------------//

`default_nettype none

module KL_mbx_dma
  import KL_mbx_pkg::*;
#(
  parameter int unsigned ID_W_P = 4   //! the DMA port's AXI ID width
) (
  input  wire                      clk_i,            //! the mailbox clock, which also clocks the DMA port
  input  wire                      rst_n,            //! synchronous active-low reset

  // ---- one transfer's operands, held by the control registers -------------
  input  wire  [MBX_ADDR_W_C-1:0]  ring_base_i,      //! the ring's word 0, as a word address in the window
  input  wire  [15:0]              ring_mask_i,      //! the ring's size in words less one
  input  wire  [15:0]              ring_index_i,     //! the ring index of the transfer's first word
  input  wire  [31:0]              mem_addr_i,       //! the transfer's first memory byte, on a word
  input  wire  [11:0]              len_bytes_i,      //! the bytes to move; 0 moves nothing
  input  wire                      to_ring_i,        //! 1: memory to the ring (transmit); 0: the ring to memory (receive)
  input  wire                      start_p_i,        //! start one transfer with the operands above
  output logic                     busy_o,           //! a transfer is running and owns the host port
  output logic                     err_o,            //! the last start was refused, or its transfer saw an error response

  // ---- the CPU's host port, from KL_mbx_wb --------------------------------
  input  wire                      cpu_req_i,        //! the CPU's request this cycle
  input  wire                      cpu_we_i,         //! the request is a write
  input  wire  [MBX_ADDR_W_C-1:0]  cpu_addr_i,       //! its word address inside the window
  input  wire  [31:0]              cpu_wdata_i,      //! its write data
  input  wire  [3:0]               cpu_be_i,         //! its byte strobes
  output logic                     cpu_ack_o,        //! the CPU's request completed
  output logic [31:0]              cpu_rdata_o,      //! its read data, valid with cpu_ack_o

  // ---- KL_mbx's host port -------------------------------------------------
  output logic                     host_req_o,       //! a request this cycle
  output logic                     host_we_o,        //! the request is a write
  output logic [MBX_ADDR_W_C-1:0]  host_addr_o,      //! word address inside the window
  output logic [31:0]              host_wdata_o,     //! write data
  output logic [3:0]               host_be_o,        //! byte strobes
  input  wire                      host_ack_i,       //! the request of the cycle before completed
  input  wire  [31:0]              host_rdata_i,     //! read data, valid with host_ack_i

  // ---- the DMA port: write address ------------------------------------------
  output logic                     axi_awvalid_o,    //! AWVALID
  input  wire                      axi_awready_i,    //! AWREADY
  output logic [ID_W_P-1:0]        axi_awid_o,       //! AWID, always 0
  output logic [31:0]              axi_awaddr_o,     //! AWADDR, the burst's first byte
  output logic [7:0]               axi_awlen_o,      //! AWLEN, beats less one (at most 15)
  output logic [2:0]               axi_awsize_o,     //! AWSIZE, 2: a beat is the whole 32-bit word
  output logic [1:0]               axi_awburst_o,    //! AWBURST, INCR
  output logic                     axi_awlock_o,     //! AWLOCK, normal
  output logic [3:0]               axi_awcache_o,    //! AWCACHE, 0
  output logic [2:0]               axi_awprot_o,     //! AWPROT, 0
  output logic [3:0]               axi_awqos_o,      //! AWQOS, 0
  // ---- write data -------------------------------------------------------------
  output logic                     axi_wvalid_o,     //! WVALID
  input  wire                      axi_wready_i,     //! WREADY
  output logic [31:0]              axi_wdata_o,      //! WDATA
  output logic [3:0]               axi_wstrb_o,      //! WSTRB: every lane but on the record's last word
  output logic                     axi_wlast_o,      //! WLAST
  // ---- write response ---------------------------------------------------------
  input  wire                      axi_bvalid_i,     //! BVALID
  output logic                     axi_bready_o,     //! BREADY
  input  wire  [ID_W_P-1:0]        axi_bid_i,        //! BID, unused: one burst in flight
  input  wire  [1:0]               axi_bresp_i,      //! BRESP: SLVERR or DECERR is an error
  // ---- read address -------------------------------------------------------------
  output logic                     axi_arvalid_o,    //! ARVALID
  input  wire                      axi_arready_i,    //! ARREADY
  output logic [ID_W_P-1:0]        axi_arid_o,       //! ARID, always 0
  output logic [31:0]              axi_araddr_o,     //! ARADDR, the burst's first byte
  output logic [7:0]               axi_arlen_o,      //! ARLEN, beats less one (at most 15)
  output logic [2:0]               axi_arsize_o,     //! ARSIZE, 2: a beat is the whole 32-bit word
  output logic [1:0]               axi_arburst_o,    //! ARBURST, INCR
  output logic                     axi_arlock_o,     //! ARLOCK, normal
  output logic [3:0]               axi_arcache_o,    //! ARCACHE, 0
  output logic [2:0]               axi_arprot_o,     //! ARPROT, 0
  output logic [3:0]               axi_arqos_o,      //! ARQOS, 0
  // ---- read data ----------------------------------------------------------------
  input  wire                      axi_rvalid_i,     //! RVALID
  output logic                     axi_rready_o,     //! RREADY, always high while a read burst runs
  input  wire  [ID_W_P-1:0]        axi_rid_i,        //! RID, unused: one burst in flight
  input  wire  [31:0]              axi_rdata_i,      //! RDATA
  input  wire  [1:0]               axi_rresp_i,      //! RRESP: SLVERR or DECERR is an error
  input  wire                      axi_rlast_i       //! RLAST
);

  localparam int unsigned BEATS_C = 16;   //! a burst's most beats: one 64-byte line of 32-bit words

  typedef enum logic [2:0] {
    IDLE_S,   // no transfer; the CPU owns the host port
    FILL_S,   // receive: reading a chunk's ring words into the buffer
    AW_S,     // receive: the chunk's write burst address
    W_S,      // receive: the chunk's write beats
    B_S,      // receive: the chunk's write response
    AR_S,     // transmit: the chunk's read burst address
    R_S       // transmit: the chunk's read beats, each written to the ring as it arrives
  } state_e;

  state_e                    state_r;
  logic [MBX_ADDR_W_C-1:0]   base_r;       //! the ring's word 0
  logic [15:0]               mask_r;       //! the ring's index mask
  logic [15:0]               index_r;      //! the next ring word's index
  logic [31:2]               word_addr_r;  //! the next memory word's address
  logic [10:0]               left_r;       //! words of the transfer not yet done, its current chunk's included
  logic [3:0]                tail_be_r;    //! the byte strobes of the transfer's last word
  logic [4:0]                chunk_r;      //! the current chunk's words, 1 to 16
  logic [4:0]                count_r;      //! the chunk's ring reads answered, W beats sent or R beats taken
  logic                      err_r;        //! the error flag
  logic                      rerr_r;       //! the transmit chunk saw an error response: write no more beats
  logic                      hold_r;       //! the mover's request of last cycle is answered this cycle; its fields hold
  logic [31:0]               hold_wdata_r; //! that request's write data
  logic                      hold_last_r;  //! that request wrote its read burst's last beat
  logic [31:0]               buf_r [BEATS_C];   //! the receive chunk's words

  logic                      pend_r;       //! a CPU request held while a transfer ran
  logic                      pend_we_r;
  logic [MBX_ADDR_W_C-1:0]   pend_addr_r;
  logic [31:0]               pend_wdata_r;
  logic [3:0]                pend_be_r;
  logic                      ack_cpu_r;    //! the host port's request last cycle was the CPU's

  // ---- a transfer's shape -----------------------------------------------------------
  // A chunk is the transfer's next words up to the end of the 64-byte line
  // its first memory word is in, so a burst never crosses a line.
  function automatic logic [4:0] chunk_of(input logic [10:0] words, input logic [3:0] word_in_line);
    logic [4:0] room;
    room = 5'(BEATS_C) - {1'b0, word_in_line};
    return (words < 11'(room)) ? words[4:0] : room;
  endfunction

  logic [10:0]               start_words_w;    //! the words a start's length takes
  logic [3:0]                start_tail_be_w;  //! the strobes of its last word
  logic                      last_chunk_w;     //! the current chunk ends the transfer
  logic [10:0]               left_next_w;      //! the words left after the current chunk
  logic [31:2]               word_addr_next_w; //! the memory word after the current chunk
  assign start_words_w    = 11'((len_bytes_i + 12'd3) >> 2);
  assign start_tail_be_w  = (len_bytes_i[1:0] == 2'd0) ? 4'hF : 4'((5'd1 << len_bytes_i[1:0]) - 5'd1);
  assign last_chunk_w     = (left_r == 11'(chunk_r));
  assign left_next_w      = left_r - 11'(chunk_r);
  assign word_addr_next_w = word_addr_r + 30'(chunk_r);

  logic [MBX_ADDR_W_C-1:0]   ring_addr_w;      //! the ring word index_r names
  assign ring_addr_w     = base_r + MBX_ADDR_W_C'(index_r & mask_r);

  // ---- the ring side: one request, then its answer, as KL_mbx_wb presents them -----------
  // A request's address, direction and data hold through the cycle of its
  // answer, so an observer that reads the port's fields at the answer sees
  // the request's (index_r moves only at the answer). The cycle a CPU
  // request is answered is the CPU's too: the mover waits it out.
  logic                      fill_req_w;       //! a ring read this cycle (receive)
  logic                      beat_w;           //! a read beat is taken this cycle (transmit)
  logic                      ring_wr_w;        //! that beat is written to the ring this cycle
  logic                      last_word_w;      //! this W beat, or this read beat, is the transfer's last word
  logic [31:0]               lanes_w;          //! the transfer's last word's lanes kept, the rest zero
  logic [31:0]               beat_data_w;      //! a read beat as the ring takes it
  assign fill_req_w  = (state_r == FILL_S) && !hold_r && !ack_cpu_r && (count_r != chunk_r);
  assign beat_w      = (state_r == R_S) && !hold_r && !ack_cpu_r && axi_rvalid_i;
  assign ring_wr_w   = beat_w && !rerr_r && (axi_rresp_i[1] == 1'b0);
  assign last_word_w = last_chunk_w && (count_r + 5'd1 == chunk_r);
  assign lanes_w     = {{8{tail_be_r[3]}}, {8{tail_be_r[2]}}, {8{tail_be_r[1]}}, {8{tail_be_r[0]}}};
  assign beat_data_w = last_word_w ? (axi_rdata_i & lanes_w) : axi_rdata_i;

  // ---- the host port: the mover while it runs, else the CPU, its held request first -----
  logic                      own_w;            //! a transfer owns the host port
  logic                      mover_w;          //! the port's fields are the mover's this cycle
  logic                      cpu_issue_w;      //! the CPU's request (held or new) goes to KL_mbx this cycle
  assign own_w       = (state_r != IDLE_S);
  assign mover_w     = own_w && !ack_cpu_r;
  assign cpu_issue_w = !own_w && (pend_r || cpu_req_i);

  always_comb begin : host_mux
    host_req_o   = 1'b0;
    host_we_o    = 1'b0;
    host_addr_o  = ring_addr_w;
    host_wdata_o = '0;
    host_be_o    = 4'hF;
    if (mover_w) begin
      host_req_o   = fill_req_w || ring_wr_w;
      host_we_o    = (state_r == R_S);
      host_wdata_o = hold_r ? hold_wdata_r : beat_data_w;
    end else if (pend_r && !own_w) begin
      host_req_o   = 1'b1;
      host_we_o    = pend_we_r;
      host_addr_o  = pend_addr_r;
      host_wdata_o = pend_wdata_r;
      host_be_o    = pend_be_r;
    end else begin
      host_req_o   = cpu_req_i;
      host_we_o    = cpu_we_i;
      host_addr_o  = cpu_addr_i;
      host_wdata_o = cpu_wdata_i;
      host_be_o    = cpu_be_i;
    end
  end : host_mux

  assign cpu_ack_o   = host_ack_i && ack_cpu_r;
  assign cpu_rdata_o = host_rdata_i;
  assign busy_o      = own_w;
  assign err_o       = err_r;

  // ---- the DMA port ------------------------------------------------------------------
  assign axi_awvalid_o = (state_r == AW_S);
  assign axi_awid_o    = '0;
  assign axi_awaddr_o  = {word_addr_r, 2'b00};
  assign axi_awlen_o   = 8'(chunk_r - 5'd1);
  assign axi_awsize_o  = 3'b010;
  assign axi_awburst_o = 2'b01;
  assign axi_awlock_o  = 1'b0;
  assign axi_awcache_o = 4'b0000;
  assign axi_awprot_o  = 3'b000;
  assign axi_awqos_o   = 4'b0000;
  assign axi_wvalid_o  = (state_r == W_S);
  assign axi_wdata_o   = buf_r[count_r[3:0]];
  assign axi_wstrb_o   = last_word_w ? tail_be_r : 4'hF;
  assign axi_wlast_o   = (count_r + 5'd1 == chunk_r);
  assign axi_bready_o  = (state_r == B_S);
  assign axi_arvalid_o = (state_r == AR_S);
  assign axi_arid_o    = '0;
  assign axi_araddr_o  = {word_addr_r, 2'b00};
  assign axi_arlen_o   = 8'(chunk_r - 5'd1);
  assign axi_arsize_o  = 3'b010;
  assign axi_arburst_o = 2'b01;
  assign axi_arlock_o  = 1'b0;
  assign axi_arcache_o = 4'b0000;
  assign axi_arprot_o  = 3'b000;
  assign axi_arqos_o   = 4'b0000;
  assign axi_rready_o  = (state_r == R_S) && !hold_r && !ack_cpu_r;

  // ---- the transfer ---------------------------------------------------------------------
  // The current chunk is done: step to the next one, or end.
  logic                      chunk_end_w;      //! the chunk's last ring write is answered, or its last beat needs none
  assign chunk_end_w = (state_r == R_S)
                    && ((hold_r && hold_last_r) || (beat_w && !ring_wr_w && axi_rlast_i));

  always_ff @(posedge clk_i) begin : transfer
    if (!rst_n) begin
      state_r      <= IDLE_S;
      base_r       <= '0;
      mask_r       <= '0;
      index_r      <= '0;
      word_addr_r  <= '0;
      left_r       <= '0;
      tail_be_r    <= 4'hF;
      chunk_r      <= '0;
      count_r      <= '0;
      err_r        <= 1'b0;
      rerr_r       <= 1'b0;
      hold_r       <= 1'b0;
      hold_wdata_r <= '0;
      hold_last_r  <= 1'b0;
    end else begin
      hold_r <= fill_req_w || ring_wr_w;
      unique case (state_r)
        IDLE_S: begin
          if (start_p_i) begin
            if (mem_addr_i[1:0] != 2'b00) begin
              err_r <= 1'b1;
            end else begin
              err_r       <= 1'b0;
              rerr_r      <= 1'b0;
              base_r      <= ring_base_i;
              mask_r      <= ring_mask_i;
              index_r     <= ring_index_i;
              word_addr_r <= mem_addr_i[31:2];
              left_r      <= start_words_w;
              tail_be_r   <= start_tail_be_w;
              count_r     <= '0;
              if (len_bytes_i != 12'd0) begin
                chunk_r <= chunk_of(start_words_w, mem_addr_i[5:2]);
                state_r <= to_ring_i ? AR_S : FILL_S;
              end
            end
          end
        end
        FILL_S: begin
          // the answer to last cycle's read: the word, and the next index
          if (hold_r) begin
            index_r <= index_r + 16'd1;
            count_r <= count_r + 5'd1;
            if (count_r + 5'd1 == chunk_r) begin
              count_r <= '0;
              state_r <= AW_S;
            end
          end
        end
        AW_S: if (axi_awready_i) state_r <= W_S;
        W_S: begin
          if (axi_wready_i) begin
            count_r <= count_r + 5'd1;
            if (count_r + 5'd1 == chunk_r) state_r <= B_S;
          end
        end
        B_S: begin
          if (axi_bvalid_i) begin
            left_r      <= left_next_w;
            word_addr_r <= word_addr_next_w;
            count_r     <= '0;
            if (axi_bresp_i[1]) begin
              err_r   <= 1'b1;
              state_r <= IDLE_S;
            end else if (last_chunk_w) begin
              state_r <= IDLE_S;
            end else begin
              chunk_r <= chunk_of(left_next_w, word_addr_next_w[5:2]);
              state_r <= FILL_S;
            end
          end
        end
        AR_S: if (axi_arready_i) state_r <= R_S;
        R_S: begin
          if (beat_w) begin
            count_r <= count_r + 5'd1;
            if (axi_rresp_i[1]) begin
              err_r  <= 1'b1;
              rerr_r <= 1'b1;
            end
            if (ring_wr_w) begin
              hold_wdata_r <= beat_data_w;
              hold_last_r  <= axi_rlast_i;
            end
          end
          // the answer to last cycle's ring write: the next index
          if (hold_r) index_r <= index_r + 16'd1;
          if (chunk_end_w) begin
            left_r      <= left_next_w;
            word_addr_r <= word_addr_next_w;
            count_r     <= '0;
            if (last_chunk_w || rerr_r || (beat_w && axi_rresp_i[1])) begin
              state_r <= IDLE_S;
            end else begin
              chunk_r <= chunk_of(left_next_w, word_addr_next_w[5:2]);
              state_r <= AR_S;
            end
          end
        end
        default: state_r <= IDLE_S;
      endcase
      // a start while a transfer runs is refused; the transfer goes on
      if (start_p_i && own_w) err_r <= 1'b1;
    end
  end : transfer

  // ---- the receive chunk's buffer: each read's answer --------------------------------------
  always_ff @(posedge clk_i) begin : fill
    if (!rst_n) begin
      for (int unsigned k = 0; k < BEATS_C; k++) buf_r[k] <= '0;
    end else if ((state_r == FILL_S) && hold_r) begin
      buf_r[count_r[3:0]] <= host_rdata_i;
    end
  end : fill

  // ---- the CPU's held request and the host port's answer routing ----------------------------
  always_ff @(posedge clk_i) begin : port
    if (!rst_n) begin
      pend_r       <= 1'b0;
      pend_we_r    <= 1'b0;
      pend_addr_r  <= '0;
      pend_wdata_r <= '0;
      pend_be_r    <= '0;
      ack_cpu_r    <= 1'b0;
    end else begin
      ack_cpu_r <= cpu_issue_w;
      if (own_w && cpu_req_i) begin
        pend_r       <= 1'b1;
        pend_we_r    <= cpu_we_i;
        pend_addr_r  <= cpu_addr_i;
        pend_wdata_r <= cpu_wdata_i;
        pend_be_r    <= cpu_be_i;
      end else if (!own_w && pend_r) begin
        pend_r <= 1'b0;
      end
    end
  end : port

  // the IDs of a port with one burst in flight, and a chunk count's unused width
  logic unused_w;
  assign unused_w = ^{axi_bid_i, axi_rid_i, axi_bresp_i[0], axi_rresp_i[0]};

endmodule : KL_mbx_dma

`default_nettype wire

/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 *
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */

//---------------------------------------------------------------------------//
/*
------------------------------------------------------------------------------
  File        : KL_pcm_ring_bram.sv
  Description : On-chip dual-port BRAM PCM ring for the Milan listener media
                path — the shed-proof replacement for the LiteDRAM
                WishboneDMAWriter ring (milan_soc.py _PCMRingNxN /
                MilanDMA.pcm).

                The received-PCM datapath (KL_aaf_rx_depacketizer -> CDC
                lane -> ring) is NON-STALLABLE: a beat offered while the ring
                sink is not-ready is shed and lost on the wire contract. On
                the DRAM writer, concurrent CPU reads of the ring region
                slowed the wishbone writer below the PCM rate and the
                datapath shed ~1 beat in 24 (mf52 SHED, a 2 kHz whole-frame
                artifact; mitigated to CDC depth 128 but not killed at root),
                and DRAM write-posting/arbitration ambiguity gave a second
                1-in-24 ring artifact (I6). Both live ONLY on the arbitrated
                DRAM path.

                A BRAM ring writes in a SINGLE cycle with no arbitration and
                no write-posting, so the write side's ready is held CONSTANT
                1 — sink.ready can never drop, no beat can ever be shed, and
                I6 cannot exist. The CPU reads PCM words from the second BRAM
                port through a wishbone-classic read slave mapped into an
                uncached MMIO window; a CPU read touches a physically
                independent port and can never back-pressure or slow the
                write side.

                Layout is bit-identical to _PCMRingNxN: a beat tagged
                `wr_user_i = s` (the datapath's m_axis_pcm_tuser) lands at
                (s*stride_i + offset_r[s]) within a per-stream sub-ring of
                length_i BYTES; offset_r[s] is that stream's private write
                pointer wrapping at length_i, sub-rings stride_i bytes apart.
                enable_i=0 clears every offset and drops beats (the flat
                writer's disabled behaviour). At N_STREAMS=1 the index is
                always 0, stride engages only for s>0, and stream 0 sits at
                the window base — the flat single-ring layout bit-for-bit
                (the N=1 byte-identity axiom). base is the fixed BRAM MMIO
                window (the SoC address decoder places the whole array at
                `base`), so it is NOT part of the intra-BRAM address; the
                driver still programs the base CSR = the mmap base, keeping
                the pcm CSR ABI unchanged.

  Spec refs   : docs/NXN_ARCHITECTURE.md §1.3 P12 (per-stream ring key);
                milan_soc.py _PCMRingNxN (CSR/address ABI mirrored);
                mf52 SHED + I6 (DRAM-path silicon failures this sinks)
  Company     : Kebag Logic
  Project     : Milan AVB endstation
------------------------------------------------------------------------------
*/
//---------------------------------------------------------------------------//

`default_nettype none

module KL_pcm_ring_bram #(
  parameter int unsigned DATA_W     = 64,     //! ring word width (bus width)
  parameter int unsigned N_STREAMS  = 1,      //! per-stream sub-rings (NxN width)
  parameter int unsigned RING_BYTES = 32768   //! TOTAL BRAM bytes (power of two)
) (
  input  wire                   clk_i,        //! sys/media clock
  input  wire                   rst_n,        //! sync reset, active low

  //! --- write side (media clock, AXIS-like, NON-STALLABLE) ---------------
  input  wire  [DATA_W-1:0]     wr_data_i,    //! PCM word (wire byte order)
  input  wire  [3:0]            wr_user_i,    //! stream index s (m_axis_pcm_tuser)
  input  wire                   wr_valid_i,   //! beat offered this cycle
  output wire                   wr_ready_o,   //! HELD CONSTANT 1 (never sheds)

  //! --- control (wired to the EXISTING pcm CSR block in migen glue) ------
  input  wire  [31:0]           length_i,     //! per-stream sub-ring length (bytes)
  input  wire  [31:0]           stride_i,     //! bytes between stream sub-ring bases
  input  wire                   enable_i,     //! 0 = clear offsets + drop beats
  input  wire  [3:0]            sel_i,         //! stream index for offset readback
  output wire  [31:0]           offset_o,     //! selected stream's write pointer (bytes)

  //! --- CPU read port: wishbone-classic READ slave into BRAM port B ------
  input  wire  [31:0]           wb_adr_i,     //! word address (low bits index the ring)
  input  wire                   wb_cyc_i,     //! bus cycle
  input  wire                   wb_stb_i,     //! strobe
  output wire  [DATA_W-1:0]     wb_dat_o,     //! read data (registered)
  output wire                   wb_ack_o      //! read acknowledge
);

  // ------------------------------------------------------------------ //
  // Geometry                                                            //
  // ------------------------------------------------------------------ //
  localparam int unsigned NB    = DATA_W / 8;           //! bytes per word
  localparam int unsigned SHIFT = $clog2(NB);           //! byte->word shift (3 @ 64b)
  localparam int unsigned DEPTH = RING_BYTES / NB;      //! ring words (power of two)
  localparam int unsigned AW    = $clog2(DEPTH);        //! word-address width
  localparam int unsigned NSW   = (N_STREAMS < 1) ? 1 : N_STREAMS;   //! >=1 sub-rings

  //! the physical ring memory — one write port (A, datapath), one
  //! registered read port (B, CPU). No array reset => clean BRAM inference.
  logic [DATA_W-1:0] mem [DEPTH];

  // ------------------------------------------------------------------ //
  // Write side: single-cycle BRAM store, ready CONSTANT 1               //
  // ------------------------------------------------------------------ //
  //! clamp a stray stream index to the elaborated count (the datapath only
  //! emits tuser < N_STREAMS; this keeps a rogue tag in range) — mirrors
  //! _PCMRingNxN's Mux(user >= n_streams, 0, user)
  wire        wr_clamp_w = ({28'd0, wr_user_i} >= 32'(N_STREAMS));
  wire [3:0]  wr_s_w     = wr_clamp_w ? 4'd0 : wr_user_i;

  //! per-stream private write pointer (bytes), wraps at length_i
  logic [31:0] offset_r [NSW];

  //! address math IDENTICAL to _PCMRingNxN, minus base (applied by the SoC
  //! decoder): byte = s*stride + offset[s]; word index = byte >> SHIFT,
  //! masked to the physical ring depth so a bad CSR cannot escape the BRAM
  wire [31:0]   wr_byte_addr_w = (stride_i * {28'd0, wr_s_w}) + offset_r[wr_s_w];
  wire [AW-1:0] wr_word_addr_w = wr_byte_addr_w[SHIFT +: AW];

  //! enable gates the write only; ready is never gated (that is the whole
  //! point — the datapath can never be told to wait, so it can never shed)
  wire wr_fire_w = wr_valid_i && enable_i;

  assign wr_ready_o = 1'b1;

  always_ff @(posedge clk_i) begin : wr_port
    if (wr_fire_w) mem[wr_word_addr_w] <= wr_data_i;
  end : wr_port

  always_ff @(posedge clk_i) begin : wr_ptr
    if (!rst_n) begin
      for (int i = 0; i < int'(NSW); i++) offset_r[i] <= 32'd0;
    end
    else if (!enable_i) begin
      //! disabled: clear every offset (matches the flat writer's disable)
      for (int i = 0; i < int'(NSW); i++) offset_r[i] <= 32'd0;
    end
    else if (wr_fire_w) begin
      //! wrap when the next word would cross the sub-ring end (same predicate
      //! as _PCMRingNxN: offset + nb >= length -> back to 0)
      if (offset_r[wr_s_w] + 32'(NB) >= length_i) offset_r[wr_s_w] <= 32'd0;
      else                                        offset_r[wr_s_w] <= offset_r[wr_s_w] + 32'(NB);
    end
  end : wr_ptr

  // ------------------------------------------------------------------ //
  // Offset readback (selected stream's write pointer)                   //
  // ------------------------------------------------------------------ //
  wire       sel_clamp_w = ({28'd0, sel_i} >= 32'(N_STREAMS));
  wire [3:0] sel_s_w     = sel_clamp_w ? 4'd0 : sel_i;

  assign offset_o = offset_r[sel_s_w];

  // ------------------------------------------------------------------ //
  // Read side: wishbone-classic REGISTERED read slave (BRAM port B)     //
  // Read-only — only the datapath writes PCM. Registered for clean BRAM //
  // read-port inference (2-cycle: strobe -> next cycle data + ack).     //
  // ------------------------------------------------------------------ //
  logic [DATA_W-1:0] rd_data_r;
  logic              ack_r;

  always_ff @(posedge clk_i) begin : rd_port
    if (!rst_n) begin
      ack_r <= 1'b0;
    end
    else begin
      ack_r <= 1'b0;
      //! single-beat classic handshake: on a fresh strobe, register the BRAM
      //! word and pulse ack for exactly one cycle
      if (wb_cyc_i && wb_stb_i && !ack_r) begin
        rd_data_r <= mem[wb_adr_i[AW-1:0]];
        ack_r     <= 1'b1;
      end
    end
  end : rd_port

  assign wb_dat_o = rd_data_r;
  assign wb_ack_o = ack_r;

endmodule

`default_nettype wire

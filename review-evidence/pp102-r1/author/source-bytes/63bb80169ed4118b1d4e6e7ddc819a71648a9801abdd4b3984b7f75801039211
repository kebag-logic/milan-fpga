/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 */
//---------------------------------------------------------------------------//
//  File        : KL_aecp_desc_store.sv
//  Project     : IEEE 1722.1 protocol processor
//                (docs/architecture/07 §3.3 static image + index map,
//                 07 §3.4 name table, 06 §6.1 READ_DESCRIPTOR,
//                 06 §8 DESC_ADDR / READ_STATE / NAME_RD / COPY_BUFFER)
//
//  Description : The entity model behind the µCPU's `st_*` state port. It
//                LOCATEs a descriptor by (configuration_index,
//                descriptor_type, descriptor_index) through the 07 §3.3 index
//                map, fetches that ONE descriptor into an on-chip line buffer
//                and serves every subsequent µCPU read from there.
//
//                WHERE THE IMAGE LIVES — and why it is not a ROM. The
//                reference consumer's generated model is already 22,561 bytes
//                at the 8x8 shape (~5 RAMB36) BEFORE the 07 §3.4 overlay and
//                the 64-B-per-descriptor name table, and it grows with every
//                stream, descriptor and localized string. The reference part
//                (xc7a100t, 135 block-RAM tiles) measured 131 tiles used on a
//                recent build. So the image lives in the INTEGRATOR'S MAIN
//                MEMORY — DDR3 on the reference board — reached through the
//                vendor-neutral read-only master below. This module knows
//                nothing about what that memory is: it issues a byte address
//                plus a 64-bit beat count and consumes an in-order response
//                stream.
//
//                WHERE THE ADDRESSES COME FROM. Every address is an
//                ELABORATION PARAMETER (`DESC_BASE_P`), never a register and
//                never a CSR: the memory map is fixed when the bitstream is
//                built, so a runtime base would only buy a 32-bit port and the
//                flops behind it on a die that has none to spare. Arithmetic
//                against a constant base constant-folds away.
//
//                WHAT REPLACES "the base points at nothing". With a constant
//                base that failure is impossible — a likelier one takes its
//                place: the region exists and SOFTWARE HAS NOT LOADED THE
//                IMAGE YET, or loaded a truncated or wrong one. Uninitialised
//                DRAM is not a recognisable zero. So the image opens with a
//                magic + layout-version + checksum header
//                (hdl/aecp/desc/gen_desc_image.py) and NOTHING is served until
//                all three agree.
//
//                HEAL BEFORE ANSWER (silicon r49a/w3a evidence, 2026-08-15).
//                A locate arriving while the image is invalid used to answer
//                its miss FROM THE PARKED STATE and re-arm the header probe
//                after - so on hardware, where the loader lands the image in
//                DRAM long after the store's boot walk parked against empty
//                memory, the FIRST wire command always missed (measured: a
//                first READ_DESCRIPTOR answering BAD_ARGUMENTS, a first
//                GET_COUNTERS answering NO_SUCH_DESCRIPTOR) and only the
//                SECOND was served. The order is now walk-then-answer: an
//                invalid-image locate TRIGGERS the header probe and stalls
//                through it - the µCPU already holds `st_req` through state
//                stalls, and every walk burst is bounded by the memory
//                watchdog, so an absent bridge still degrades to the fault
//                answer in bounded time, never a hang - and the locate is
//                answered from the walk's OUTCOME: served when the freshly
//                validated image has the descriptor, the honest miss only
//                when the re-walked image genuinely lacks it or is itself
//                still invalid. The store never returns a descriptor from an
//                image whose header it has not validated — "not ready yet"
//                and "silently wrong" are different answers here.
//
//                LATENCY IS THE DESIGN PROBLEM. The reference SoC measures
//                ~1424 ns on a miss to main memory. Fetching a ~300-byte
//                descriptor one byte at a time at that latency would cost
//                ~430 µs and hold the µCPU for all of it. So: (1) the INDEX
//                MAP is walked ONCE after reset into an on-chip table — it is
//                consulted on EVERY locate, and a DRAM round trip per locate
//                is precisely the cost being avoided; at 16 B per
//                (configuration, type) it is ~128 B for the 07 §3.1 tree
//                against ~22 KB for the image, so caching the map is cheap
//                exactly where caching the image is not; (2) a located
//                descriptor is fetched ONCE, as a single burst, into
//                `LINE_BYTES_P` of line buffer, and every `READ_STATE` /
//                `COPY_BUFFER` beat after that is an on-chip read. One
//                command pays one memory latency, not one per byte.
//
//                LINE BUFFER SIZE. `LINE_BYTES_P` defaults to 576 = the
//                largest descriptor 07 §3.2 can produce, rounded up to this
//                repository's 03 §2 slot size — which is also the
//                response-buffer size, so a descriptor that fits the line
//                always fits the response. The worst case is a
//                STREAM_INPUT/OUTPUT, and the layout Milan v1.2 §5.3.3.4
//                mandates for it is IEEE 1722.1-2021 Table 7-8 (§7.2.6):
//                138 + 8·N + 2·R with N capped at 47 formats and R at 8
//                redundant streams, so 530 B. Milan v1.2 Annex C Table C.1 is
//                a permitted alternative layout (§5.3.3.4 "may", mandatory
//                only for a redundant pair) and is 2 B shorter at the same
//                caps, 528 B. 576 covers a model assembled either way. A
//                descriptor LONGER than the line cannot be served: its locate
//                answers `st_err_o` (NO_SUCH_DESCRIPTOR) rather than a
//                truncated descriptor, and the header's `desc_max_len` is
//                checked against `LINE_BYTES_P` at load time so the whole
//                image is refused up front. `gen_desc_image.py` refuses to
//                emit such an image at all; the run-time arms exist so a
//                mismatched image cannot put a lie on the wire.
//
//                THE STATE-PORT ADDRESS MAP (`st_addr_i[19:16]` = region).
//                The µISA cannot carry a 48-bit locate key on a 20-bit
//                address and 06 §8 leaves the encoding open, so:
//                  region 0x0  descriptor DATA — the located descriptor's
//                              bytes; `st_addr_i[15:3]` selects the 64-bit
//                              lane and byte n sits in bit [63-8n -: 8] (wire
//                              order, so COPY_BUFFER hands the lane straight
//                              to the response buffer unswapped). A lane past
//                              the descriptor's length reads 0.
//                  region 0xB  name-address lookup. `st_wdata_i[15:0]` is
//                              the semantic name_index. A valid lookup returns
//                              its byte address in the writable name overlay;
//                              an invalid index raises `st_err_o`.
//                  region 0xC  read: {48'd0, name_base of the located
//                              descriptor} (0xFFFF = unnamed) — where a
//                              GET_NAME/SET_NAME µprogram finds its entry.
//                  region 0xD  read: {48'd0, configurations_count} — lets a
//                              µprogram range-check configuration_index and
//                              answer BAD_ARGUMENTS (06 §6.1) instead of
//                              NO_SUCH_DESCRIPTOR.
//                  region 0xE  read: {48'd0, located descriptor length}.
//                  region 0xF  LOCATE. The key rides `st_wdata_i[47:0]` =
//                              {descriptor_index, descriptor_type,
//                              configuration_index} — the µCPU drives rf[ra]
//                              onto `st_wdata_o` on EVERY state-port cycle and
//                              it is the only 64-bit lane the face has. The
//                              answer is `st_rdata_o` = 0 (the line-buffer
//                              origin) or `st_err_o` on a miss.
//                `st_name_i` selects the 07 §3.4 name table in any region:
//                `st_addr_i[15:3]` is the 64-bit lane, so [15:6] is the
//                64-byte entry. It is the ONE writable region — names are
//                overlay, not image — and it is initialised from the image's
//                name table by the same boot walk.
//
//                Because every LOCATE answers 0, the µCPU's `desc_base_r` is
//                invariantly 0 in this system, so a µprogram addresses the
//                region pseudo-registers directly.
//
//                A write to any region other than the name table is DROPPED
//                and counted (`dbg_ro_write_o`): the static image is read-only
//                at run time (07 §2 access-rights rule).
//---------------------------------------------------------------------------//
`default_nettype none

module KL_aecp_desc_store #(
    //! Byte address of the image header in the integrator's memory map.
    //! COMPILE TIME by contract — see the banner. Must be 8-byte aligned.
    parameter logic [31:0] DESC_BASE_P       = 32'h2000_0000,
    //! On-chip line buffer for ONE located descriptor (banner: 576 = the
    //! 07 §3.2 worst case rounded to the 03 §2 slot size).
    parameter int unsigned LINE_BYTES_P      = 576,
    //! Cached 07 §3.3 index-map entries — one per (configuration, type).
    parameter int unsigned IDX_ENTRIES_P     = 32,
    //! 64-byte name-table entries held on chip (07 §3.4, writable overlay).
    parameter int unsigned NAME_ENTRIES_P    = 32,
    //! No-progress watchdog on the memory face, in clocks. An absent or wedged
    //! bridge must degrade to NO_SUCH_DESCRIPTOR, never hang the µCPU: the
    //! default 4096 is 41 µs at P-CLK-HZ = 100 MHz, far inside T-AECP-RESP.
    parameter int unsigned MEM_TIMEOUT_CYC_P = 4096,
    //! derived — do not override
    localparam int unsigned LINE_LANES_C = LINE_BYTES_P / 8,
    localparam int unsigned LINE_AW_C    = $clog2(LINE_LANES_C),
    localparam int unsigned NAME_LANES_C = NAME_ENTRIES_P * 8,
    localparam int unsigned NAME_AW_C    = $clog2(NAME_LANES_C),
    localparam int unsigned IDX_AW_C     = $clog2(IDX_ENTRIES_P),
    localparam int unsigned TMO_W_C      = $clog2(MEM_TIMEOUT_CYC_P + 1)
) (
    input  wire         clk_i,             //! core clock (P-CLK-HZ domain)
    input  wire         rst_n,             //! synchronous active-low reset

    //! ---- µCPU state port (slave side of KL_aecp_ucpu's st_*, 06 §8) ----
    input  wire         st_req_i,          //! request, held until rvalid/ready
    input  wire         st_we_i,           //! 1 = write (name region only)
    input  wire         st_name_i,         //! name-region select (07 §3.4)
    input  wire  [19:0] st_addr_i,         //! [19:16] region, [15:0] byte offset
    input  wire  [63:0] st_wdata_i,        //! write data / LOCATE key
    input  wire   [7:0] st_wstrb_i,        //! per-byte write enables
    output logic        st_ready_o,        //! write accepted this cycle
    output logic        st_rvalid_o,       //! one-cycle read / locate answer
    output logic [63:0] st_rdata_o,        //! read data (0 on a locate hit)
    output logic        st_err_o,          //! locate MISS -> NO_SUCH_DESCRIPTOR

    //! ---- read-only memory master (vendor-neutral; the integrator bridges it
    //! to whatever memory system it has — DDR3 on the reference board).
    //! ONE outstanding request; responses IN ORDER; `mem_rsp_last_i` marks the
    //! final beat; a beat carries its lowest byte address in bits [63:56].
    output logic        mem_req_valid_o,   //! request presented, held until ready
    input  wire         mem_req_ready_i,   //! bridge accepts the request
    output logic [31:0] mem_req_addr_o,    //! byte address, 8-byte aligned
    output logic  [8:0] mem_req_beats_o,   //! 64-bit beats in this burst (>= 1)
    input  wire         mem_rsp_valid_i,   //! response beat present
    output logic        mem_rsp_ready_o,   //! store consumes the beat
    input  wire  [63:0] mem_rsp_data_i,    //! beat data (big-endian byte lane)
    input  wire         mem_rsp_last_i,    //! final beat of the burst
    input  wire         mem_rsp_err_i,     //! read failed — abort the burst

    //! ---- observability (07 §2 debug window / suite taps) ----
    output logic        dbg_img_valid_o,   //! header validated, model servable
    output logic  [3:0] dbg_fault_o,       //! why not (FAULT_*_C below)
    output logic [15:0] dbg_locate_miss_o, //! locates answered with st_err_o
    output logic [15:0] dbg_fetch_cnt_o,   //! descriptor bursts issued
    output logic [15:0] dbg_ro_write_o,    //! writes dropped on a read-only region
    output logic [15:0] dbg_desc_len_o     //! length of the located descriptor
);

  // ---- image header constants (hdl/aecp/desc/gen_desc_image.py) -----------
  localparam logic [31:0] IMG_MAGIC_C   = 32'h4145_4D49;  // "AEMI"
  localparam logic [15:0] IMG_VERSION_C = 16'd1;
  localparam logic [15:0] NAME_NONE_C   = 16'hFFFF;
  localparam int unsigned HDR_BEATS_C   = 4;              // 32-byte header
  //! Keep name-table chunks aligned to whole 64-byte entries. 504 is the
  //! largest multiple of eight that fits the 9-bit burst field.
  localparam int unsigned NAME_BURST_BEATS_C = 504;

  // ---- fault codes (dbg_fault_o) -----------------------------------------
  localparam logic [3:0] FAULT_NONE_C    = 4'd0;
  localparam logic [3:0] FAULT_MAGIC_C   = 4'd1;
  localparam logic [3:0] FAULT_VERSION_C = 4'd2;
  localparam logic [3:0] FAULT_CKSUM_C   = 4'd3;
  localparam logic [3:0] FAULT_NIDX_C    = 4'd4;  // 0, or more than cached
  localparam logic [3:0] FAULT_NNAME_C   = 4'd5;  // more names than cached
  localparam logic [3:0] FAULT_DESCLEN_C = 4'd6;  // a descriptor over the line
  localparam logic [3:0] FAULT_MEMERR_C  = 4'd7;
  localparam logic [3:0] FAULT_TIMEOUT_C = 4'd8;

  // ---- state-port regions (see the banner) --------------------------------
  localparam logic [3:0] RGN_DATA_C   = 4'h0;
  localparam logic [3:0] RGN_NADDR_C  = 4'hB;
  localparam logic [3:0] RGN_NBASE_C  = 4'hC;
  localparam logic [3:0] RGN_NCFG_C   = 4'hD;
  localparam logic [3:0] RGN_LEN_C    = 4'hE;
  localparam logic [3:0] RGN_LOCATE_C = 4'hF;

  // ---- elaboration guards -------------------------------------------------
  if ((LINE_BYTES_P % 8) != 0) begin : gen_g_line_align
    $error("LINE_BYTES_P=%0d must be a multiple of 8 (64-bit lanes)",
           LINE_BYTES_P);
  end
  if ((LINE_LANES_C > 511) || ((IDX_ENTRIES_P * 2) > 511)) begin : gen_g_beats
    $error("a burst exceeds the 9-bit mem_req_beats_o field");
  end
  if ((NAME_ENTRIES_P == 0) || (NAME_ENTRIES_P > 1024)) begin : gen_g_names
    $error("NAME_ENTRIES_P=%0d must be in 1..1024", NAME_ENTRIES_P);
  end
  if (DESC_BASE_P[2:0] != 3'd0) begin : gen_g_base_align
    $error("DESC_BASE_P=%08h must be 8-byte aligned", DESC_BASE_P);
  end

  // =======================================================================
  // memories
  // =======================================================================
  //! 07 §3.3 index map, one entry per (configuration, type), walked once into
  //! this table. The 16-byte image entry lands here VERBATIM, both beats
  //! concatenated: {cfg, type, count, elem_len, elem_off, name_base, stride}.
  //! The stride is separate from the length because a descriptor length is
  //! rarely a multiple of 8 — see gen_desc_image.py.
  localparam int unsigned IDX_W_C = 128;
  logic [IDX_W_C-1:0]  idx_r [0:IDX_ENTRIES_P-1];
  logic [IDX_W_C-1:0]  idx_q_r;
  logic [IDX_AW_C-1:0] idx_waddr_w, idx_raddr_w;
  logic                idx_we_w;
  logic [IDX_W_C-1:0]  idx_wdata_w;

  always_ff @(posedge clk_i) begin : idx_ram
    if (idx_we_w) idx_r[idx_waddr_w] <= idx_wdata_w;
    idx_q_r <= idx_r[idx_raddr_w];
  end

  //! the ONE located descriptor, wire order preserved
  logic [63:0]          line_r [0:LINE_LANES_C-1];
  logic [63:0]          line_q_r;
  logic [LINE_AW_C-1:0] line_waddr_w, line_raddr_w;
  logic                 line_we_w;
  logic [63:0]          line_wdata_w;

  always_ff @(posedge clk_i) begin : line_ram
    if (line_we_w) line_r[line_waddr_w] <= line_wdata_w;
    line_q_r <= line_r[line_raddr_w];
  end

  //! 07 §3.4 name table — the writable overlay region
  logic [63:0]          name_r [0:NAME_LANES_C-1];
  logic [63:0]          name_q_r;
  logic [NAME_AW_C-1:0] name_waddr_w, name_raddr_w;
  logic                 name_we_w;
  logic [63:0]          name_wdata_w;
  logic  [7:0]          name_wstrb_w;

  always_ff @(posedge clk_i) begin : name_ram
    if (name_we_w) begin
      for (int unsigned b = 0; b < 8; b++) begin
        if (name_wstrb_w[b]) begin
          name_r[name_waddr_w][8*b +: 8] <= name_wdata_w[8*b +: 8];
        end
      end
    end
    name_q_r <= name_r[name_raddr_w];
  end

  // =======================================================================
  // header shadow, walk/serve machine
  // =======================================================================
  logic [15:0] hdr_n_config_r, hdr_n_entries_r, hdr_n_names_r, hdr_desc_max_r;
  logic [31:0] hdr_index_off_r, hdr_names_off_r;
  logic [31:0] cksum_r;
  logic [63:0] hdr_b0_r;      // header beat 0: magic | version | n_config | n_entries
  logic [63:0] idx_b0_r;      // index-entry beat 0: cfg | type | count | elem_len

  typedef enum logic [3:0] {
    S_HDR_REQ, S_HDR_RSP, S_IDX_REQ, S_IDX_RSP, S_NAM_REQ, S_NAM_RSP,
    S_READY, S_BAD, S_SCAN, S_FET_REQ, S_FET_RSP, S_PATCH_RD, S_PATCH_WR,
    S_ANSWER
  } st_e;
  st_e st_r;

  logic        img_valid_r;
  logic  [3:0] fault_r;
  logic [15:0] miss_cnt_r, fetch_cnt_r, rowr_cnt_r;

  // ---- memory sequencing --------------------------------------------------
  logic [31:0]        mreq_addr_r;
  logic  [8:0]        mreq_beats_r;
  logic               mreq_valid_r;
  logic  [8:0]        beat_ix_r;
  logic [19:0]        name_load_lane_r;
  logic [TMO_W_C-1:0] tmo_r;
  logic               mem_busy_r;

  logic [19:0] name_total_lanes_w, name_lanes_left_w;
  assign name_total_lanes_w = {4'd0, hdr_n_names_r} << 3;
  assign name_lanes_left_w  = name_total_lanes_w - name_load_lane_r;

  logic beat_w, accept_w, tmo_hit_w;
  //! a beat only COUNTS while a burst of ours is outstanding, but the store is
  //! always able to SINK one: a bridge that delivers after the watchdog
  //! abandoned a burst — or across a reset that only reached this side — must
  //! be drained, not stalled against a dead ready, or it wedges forever.
  assign beat_w    = mem_rsp_valid_i && mem_busy_r;
  assign accept_w  = mreq_valid_r && mem_req_ready_i;
  assign tmo_hit_w = (tmo_r == TMO_W_C'(MEM_TIMEOUT_CYC_P));

  assign mem_req_valid_o = mreq_valid_r;
  assign mem_req_addr_o  = mreq_addr_r;
  assign mem_req_beats_o = mreq_beats_r;
  assign mem_rsp_ready_o = 1'b1;

  // ---- the request being served ------------------------------------------
  logic [15:0] key_cfg_r, key_type_r, key_index_r;
  logic [15:0] desc_len_r, desc_nbase_r;
  logic [31:0] desc_off_r;
  logic        ans_err_r;
  logic [63:0] ans_data_r, rd_reg_r;
  logic        ans_pend_r, rd_pipe_r, req_seen_r;
  logic  [1:0] rd_kind_r;                   // 0 line, 1 name, 2 pseudo-register
  logic [IDX_AW_C-1:0] scan_rd_r;           // index-RAM read pointer
  logic [15:0]         scan_cmp_r;          // entry currently in idx_q_r
  logic                scan_rdy_r;
  //! Running first-index of the entry being compared, within its (cfg, type).
  //! One descriptor type is NOT always one index entry: a type whose members
  //! differ in length is emitted as several entries, one per run of equal
  //! length, contiguous and in ascending index order (a Milan station puts a
  //! 148-byte AAF sink and a 140-byte CRF sink both under STREAM_INPUT, and
  //! 1722.1 §7.2.6 sizes each by its own number_of_formats). Every entry stays
  //! internally uniform, so a hit is still elem_off + stride*i with no second
  //! indirection - only the `i` is now relative to where this run starts.
  //! Accumulating the counts walked past is what recovers that start, and it
  //! costs one register instead of a wider image entry. A uniform type emits
  //! one entry and this stays zero, so the uniform path is unchanged.
  logic [15:0]         scan_base_r;
  //! a read took while the image was invalid: the walk now in flight owes
  //! it an answer (the heal-before-answer order - see the banner). Kind 0 =
  //! a LOCATE (owed a scan or the honest miss); kind 1 = an RGN_NCFG read
  //! (owed configurations_count - the register E_RDESC range-checks BEFORE
  //! it ever locates, which is exactly how the w3a silicon race answered
  //! BAD_ARGUMENTS instead of serving: the parked count reads 0 and no
  //! locate ever runs to trigger the old locate-only re-arm).
  logic                heal_pend_r;
  logic                heal_kind_r;

  //! A located descriptor is refreshed from the writable name overlay before
  //! LOCATE answers, and again after a write to one of its names. The refresh
  //! is byte-serial so both memories keep one synchronous read port and the
  //! line buffer keeps one full-lane write port. At AECP rates the 128-cycle
  //! ENTITY case is negligible; duplicating either RAM port is not.
  logic        patch_answer_r;
  logic        patch_name_r;
  logic  [5:0] patch_byte_r;

  // decoded fields of the scanned entry
  logic [15:0] e_cfg_w, e_type_w, e_cnt_w, e_len_w, e_nbase_w, e_strd_w;
  logic [31:0] e_off_w;
  assign e_cfg_w   = idx_q_r[127:112];
  assign e_type_w  = idx_q_r[111:96];
  assign e_cnt_w   = idx_q_r[95:80];
  assign e_len_w   = idx_q_r[79:64];
  assign e_off_w   = idx_q_r[63:32];
  assign e_nbase_w = idx_q_r[31:16];
  assign e_strd_w  = idx_q_r[15:0];

  //! an entry is only usable if its geometry is self-consistent: a stride that
  //! is shorter than the descriptor, or not 8-aligned, would place index > 0
  //! mid-beat and byte-shift the whole line buffer. Refuse it rather than
  //! serve a shifted descriptor.
  logic e_usable_w, e_name_ok_w;
  always_comb begin : entry_name_shape
    e_name_ok_w = 1'b1;
    if (e_nbase_w != NAME_NONE_C) begin
      if (e_type_w == 16'h0000) begin
        e_name_ok_w = (e_cnt_w == 16'd1) && (e_len_w >= 16'd244)
                        && ((32'(e_nbase_w) + 32'd2)
                            <= 32'(hdr_n_names_r));
      end else begin
        e_name_ok_w = (e_len_w >= 16'd68)
                        && ((32'(e_nbase_w) + 32'(e_cnt_w))
                            <= 32'(hdr_n_names_r));
      end
    end
  end
  assign e_usable_w = (e_len_w != 16'd0) && (32'(e_len_w) <= 32'(LINE_BYTES_P))
                      && (e_strd_w >= e_len_w) && (e_strd_w[2:0] == 3'd0)
                      && e_name_ok_w;

  //! scan helpers. `rel_w` is the LOCATE key relative to the start of the run
  //! this entry describes (see scan_base_r); `last_w` marks the final table
  //! entry, which is what turns "not found yet" into a miss.
  logic type_hit_w, last_w;
  logic [15:0] rel_w;
  assign type_hit_w = (e_cfg_w == key_cfg_r) && (e_type_w == key_type_r);
  assign rel_w      = key_index_r - scan_base_r;
  assign last_w     = ((scan_cmp_r + 16'd1) >= hdr_n_entries_r);

  logic [3:0] region_w;
  assign region_w = st_addr_i[19:16];

  //! writes are accepted in one cycle, but never while the boot walk owns the
  //! name RAM (the walk is watchdog-bounded, so this can never hang)
  assign st_ready_o = (st_r == S_READY) || (st_r == S_BAD);

  //! the µCPU HOLDS st_req_o through its stall, so a read is taken once and
  //! `req_seen_r` is released by the answer — back-to-back state ops (whose
  //! st_req_o never falls between them) must each be taken
  logic take_rd_w, take_wr_w;
  assign take_rd_w = st_req_i && !st_we_i && !req_seen_r && st_ready_o;
  assign take_wr_w = st_req_i &&  st_we_i && st_ready_o;

  assign st_rvalid_o = ans_pend_r && !rd_pipe_r && (st_r == S_ANSWER);
  assign st_rdata_o  = ans_data_r;
  assign st_err_o    = ans_err_r;

  assign dbg_img_valid_o   = img_valid_r;
  assign dbg_fault_o       = fault_r;
  assign dbg_locate_miss_o = miss_cnt_r;
  assign dbg_fetch_cnt_o   = fetch_cnt_r;
  assign dbg_ro_write_o    = rowr_cnt_r;
  assign dbg_desc_len_o    = desc_len_r;

  logic [15:0] len_lanes_w;                 // ceil(desc_len/8)
  assign len_lanes_w = (desc_len_r + 16'd7) >> 3;

  logic [15:0] patch_field_off_w, patch_abs_byte_w;
  logic [15:0] patch_name_lane_w;
  logic  [2:0] patch_line_byte_w, patch_name_byte_w;
  logic  [7:0] patch_data_w;
  logic [15:0] write_name_entry_w;
  logic        write_hits_current_w;
  logic [16:0] name_lookup_entry_w;
  logic        name_lookup_valid_w;

  assign patch_field_off_w = (key_type_r == 16'h0000)
                             ? (patch_name_r ? 16'd180 : 16'd48)
                             : 16'd4;
  assign patch_abs_byte_w  = patch_field_off_w + {10'd0, patch_byte_r};
  assign patch_name_lane_w = ((desc_nbase_r + {15'd0, patch_name_r}) << 3)
                             + {13'd0, patch_byte_r[5:3]};
  assign patch_line_byte_w = patch_abs_byte_w[2:0];
  assign patch_name_byte_w = patch_byte_r[2:0];
  assign write_name_entry_w = {6'd0, st_addr_i[15:6]};
  assign write_hits_current_w = img_valid_r && (desc_nbase_r != NAME_NONE_C)
                                && ((write_name_entry_w == desc_nbase_r)
                                    || ((key_type_r == 16'h0000)
                                        && (write_name_entry_w
                                            == (desc_nbase_r + 16'd1))));
  assign name_lookup_entry_w = {1'b0, desc_nbase_r}
                               + {1'b0, st_wdata_i[15:0]};
  assign name_lookup_valid_w = img_valid_r && (desc_nbase_r != NAME_NONE_C)
                               && ((st_wdata_i[15:0] == 16'd0)
                                   || ((key_type_r == 16'h0000)
                                       && (st_wdata_i[15:0] == 16'd1)))
                               && (name_lookup_entry_w < {1'b0, hdr_n_names_r});

  always_comb begin : patch_byte_select
    patch_data_w = 8'd0;
    for (int unsigned b = 0; b < 8; b++) begin
      if (patch_name_byte_w == 3'(b))
        patch_data_w = name_q_r[63 - 8*b -: 8];
    end
  end

  // ---- RAM port muxes -----------------------------------------------------
  always_comb begin : ram_ports
    idx_we_w     = (st_r == S_IDX_RSP) && beat_w && beat_ix_r[0];
    idx_waddr_w  = IDX_AW_C'(beat_ix_r >> 1);
    // the 16-byte image entry, both beats verbatim
    idx_wdata_w  = {idx_b0_r, mem_rsp_data_i};
    idx_raddr_w  = scan_rd_r;

    line_we_w    = ((st_r == S_FET_RSP) && beat_w) || (st_r == S_PATCH_WR);
    line_waddr_w = (st_r == S_PATCH_WR)
                   ? LINE_AW_C'(patch_abs_byte_w >> 3)
                   : LINE_AW_C'(beat_ix_r);
    line_raddr_w = (st_r inside {S_PATCH_RD, S_PATCH_WR})
                   ? LINE_AW_C'(patch_abs_byte_w >> 3)
                   : LINE_AW_C'(st_addr_i[15:3]);
    line_wdata_w = mem_rsp_data_i;
    if (st_r == S_PATCH_WR) begin
      line_wdata_w = line_q_r;
      for (int unsigned b = 0; b < 8; b++) begin
        if (patch_line_byte_w == 3'(b))
          line_wdata_w[63 - 8*b -: 8] = patch_data_w;
      end
    end

    name_raddr_w = (st_r inside {S_PATCH_RD, S_PATCH_WR})
                   ? NAME_AW_C'(patch_name_lane_w)
                   : NAME_AW_C'(st_addr_i[15:3]);
    if ((st_r == S_NAM_RSP) && beat_w) begin
      name_we_w    = 1'b1;
      name_waddr_w = NAME_AW_C'(name_load_lane_r + {11'd0, beat_ix_r});
      name_wdata_w = mem_rsp_data_i;
      name_wstrb_w = 8'hFF;
    end else begin
      name_we_w    = take_wr_w && st_name_i;
      name_waddr_w = NAME_AW_C'(st_addr_i[15:3]);
      name_wdata_w = st_wdata_i;
      name_wstrb_w = st_wstrb_i;
    end
  end

  // ---- header validation of the four collected beats ----------------------
  logic       hdr_ok_w;
  logic [3:0] hdr_fault_w;
  always_comb begin : header_check
    hdr_ok_w    = 1'b0;
    hdr_fault_w = FAULT_NONE_C;
    if (hdr_b0_r[63:32] != IMG_MAGIC_C)              hdr_fault_w = FAULT_MAGIC_C;
    else if (hdr_b0_r[31:16] != IMG_VERSION_C)       hdr_fault_w = FAULT_VERSION_C;
    else if (cksum_r != 32'hFFFF_FFFF)               hdr_fault_w = FAULT_CKSUM_C;
    else if ((hdr_n_entries_r == 16'd0)
             || (hdr_n_config_r == 16'd0)
             || (32'(hdr_n_entries_r) > 32'(IDX_ENTRIES_P)))
                                                     hdr_fault_w = FAULT_NIDX_C;
    else if (32'(hdr_n_names_r) > 32'(NAME_ENTRIES_P))
                                                     hdr_fault_w = FAULT_NNAME_C;
    else if ((hdr_desc_max_r == 16'd0)
             || (32'(hdr_desc_max_r) > 32'(LINE_BYTES_P)))
                                                     hdr_fault_w = FAULT_DESCLEN_C;
    else                                             hdr_ok_w = 1'b1;
  end

  // =======================================================================
  // the machine
  // =======================================================================
  always_ff @(posedge clk_i) begin : core
    if (!rst_n) begin
      st_r            <= S_HDR_REQ;
      img_valid_r     <= 1'b0;
      fault_r         <= FAULT_NONE_C;
      miss_cnt_r      <= 16'd0;
      fetch_cnt_r     <= 16'd0;
      rowr_cnt_r      <= 16'd0;
      mreq_valid_r    <= 1'b0;
      mreq_addr_r     <= 32'd0;
      mreq_beats_r    <= 9'd0;
      mem_busy_r      <= 1'b0;
      beat_ix_r       <= 9'd0;
      tmo_r           <= '0;
      hdr_b0_r        <= 64'd0;
      idx_b0_r        <= 64'd0;
      hdr_n_config_r  <= 16'd0;
      hdr_n_entries_r <= 16'd0;
      hdr_n_names_r   <= 16'd0;
      hdr_desc_max_r  <= 16'd0;
      hdr_index_off_r <= 32'd0;
      hdr_names_off_r <= 32'd0;
      cksum_r         <= 32'd0;
      key_cfg_r       <= 16'd0;
      key_type_r      <= 16'd0;
      key_index_r     <= 16'd0;
      desc_len_r      <= 16'd0;
      desc_nbase_r    <= NAME_NONE_C;
      desc_off_r      <= 32'd0;
      ans_err_r       <= 1'b0;
      ans_data_r      <= 64'd0;
      rd_reg_r        <= 64'd0;
      ans_pend_r      <= 1'b0;
      rd_pipe_r       <= 1'b0;
      req_seen_r      <= 1'b0;
      rd_kind_r       <= 2'd0;
      scan_rd_r       <= '0;
      scan_cmp_r      <= 16'd0;
      scan_rdy_r      <= 1'b0;
      scan_base_r     <= 16'd0;
      heal_pend_r     <= 1'b0;
      heal_kind_r     <= 1'b0;
      patch_answer_r  <= 1'b0;
      patch_name_r    <= 1'b0;
      patch_byte_r    <= 6'd0;
      name_load_lane_r <= 20'd0;
    end else begin
      // a read is claimed until its answer leaves
      if (take_rd_w)   req_seen_r <= 1'b1;
      if (st_rvalid_o) req_seen_r <= 1'b0;

      // ---------------- memory request / response bookkeeping -------------
      if (accept_w) begin
        mreq_valid_r <= 1'b0;
        mem_busy_r   <= 1'b1;
        beat_ix_r    <= 9'd0;
        tmo_r        <= '0;
      end
      if (beat_w) begin
        beat_ix_r <= beat_ix_r + 9'd1;
        tmo_r     <= '0;
        if (mem_rsp_last_i || mem_rsp_err_i) mem_busy_r <= 1'b0;
      end
      //! no-progress watchdog: an absent or wedged bridge must DEGRADE to
      //! NO_SUCH_DESCRIPTOR, never hang the µCPU
      if ((mreq_valid_r || mem_busy_r) && !beat_w && !tmo_hit_w) begin
        tmo_r <= tmo_r + TMO_W_C'(1);
      end

      unique case (st_r)
        // ---------------- boot walk: header -------------------------------
        S_HDR_REQ: begin
          if (!mreq_valid_r && !mem_busy_r) begin
            mreq_valid_r <= 1'b1;
            mreq_addr_r  <= DESC_BASE_P;
            mreq_beats_r <= 9'(HDR_BEATS_C);
            cksum_r      <= 32'd0;
          end
          //! the watchdog covers the REQUEST too: a bridge that never raises
          //! ready is exactly the "no memory at all" wiring, and it must
          //! degrade to a clean fault rather than park here forever
          if (accept_w) st_r <= S_HDR_RSP;
          else if (tmo_hit_w) begin
            fault_r      <= FAULT_TIMEOUT_C;
            mreq_valid_r <= 1'b0;
            tmo_r        <= '0;
            st_r         <= S_BAD;
          end
        end
        S_HDR_RSP: begin
          if (beat_w) begin
            cksum_r <= cksum_r + mem_rsp_data_i[63:32] + mem_rsp_data_i[31:0];
            //! header bytes, big-endian, 8 per beat (gen_desc_image.py):
            //!  beat 0 @0x00 magic(4) version(2) n_config(2)
            //!  beat 1 @0x08 n_entries(2) n_names(2) index_off(4)
            //!  beat 2 @0x10 names_off(4) image_bytes(4)
            //!  beat 3 @0x18 desc_max_len(2) reserved(2) checksum(4)
            unique case (beat_ix_r[1:0])
              2'd0: begin
                hdr_b0_r       <= mem_rsp_data_i;
                hdr_n_config_r <= mem_rsp_data_i[15:0];
              end
              2'd1: begin
                hdr_n_entries_r <= mem_rsp_data_i[63:48];
                hdr_n_names_r   <= mem_rsp_data_i[47:32];
                hdr_index_off_r <= mem_rsp_data_i[31:0];
              end
              2'd2: hdr_names_off_r <= mem_rsp_data_i[63:32];
              default: hdr_desc_max_r <= mem_rsp_data_i[63:48];
            endcase
          end
          if (beat_w && mem_rsp_err_i) begin
            fault_r <= FAULT_MEMERR_C;
            st_r    <= S_BAD;
          end else if (beat_w && mem_rsp_last_i) begin
            st_r <= S_IDX_REQ;
          end else if (tmo_hit_w) begin
            fault_r    <= FAULT_TIMEOUT_C;
            mem_busy_r <= 1'b0;
            tmo_r      <= '0;
            st_r       <= S_BAD;
          end
        end
        // ---------------- boot walk: index map ----------------------------
        S_IDX_REQ: begin
          if (!hdr_ok_w) begin
            fault_r <= hdr_fault_w;
            st_r    <= S_BAD;
          end else begin
            if (!mreq_valid_r && !mem_busy_r) begin
              mreq_valid_r <= 1'b1;
              mreq_addr_r  <= DESC_BASE_P + hdr_index_off_r;
              mreq_beats_r <= 9'(hdr_n_entries_r << 1);
            end
            if (accept_w) st_r <= S_IDX_RSP;
            else if (tmo_hit_w) begin
              fault_r      <= FAULT_TIMEOUT_C;
              mreq_valid_r <= 1'b0;
              tmo_r        <= '0;
              st_r         <= S_BAD;
            end
          end
        end
        S_IDX_RSP: begin
          if (beat_w && !beat_ix_r[0]) idx_b0_r <= mem_rsp_data_i;
          if (beat_w && mem_rsp_err_i) begin
            fault_r <= FAULT_MEMERR_C;
            st_r    <= S_BAD;
          end else if (beat_w && mem_rsp_last_i) begin
            name_load_lane_r <= 20'd0;
            st_r <= S_NAM_REQ;
          end else if (tmo_hit_w) begin
            fault_r    <= FAULT_TIMEOUT_C;
            mem_busy_r <= 1'b0;
            tmo_r      <= '0;
            st_r       <= S_BAD;
          end
        end
        // ---------------- boot walk: name table (07 §3.4) ------------------
        S_NAM_REQ: begin
          if (hdr_n_names_r == 16'd0) begin
            img_valid_r <= 1'b1;
            fault_r     <= FAULT_NONE_C;
            if (heal_pend_r && !heal_kind_r) begin
              heal_pend_r <= 1'b0;
              scan_rd_r   <= '0;
              scan_cmp_r  <= 16'd0;
              scan_rdy_r  <= 1'b0;
              scan_base_r <= 16'd0;
              st_r        <= S_SCAN;
            end else if (heal_pend_r) begin
              heal_pend_r <= 1'b0;
              ans_err_r   <= 1'b0;
              ans_data_r  <= {48'd0, hdr_n_config_r};
              rd_pipe_r   <= 1'b0;
              st_r        <= S_ANSWER;
            end else st_r <= S_READY;
          end else begin
            if (!mreq_valid_r && !mem_busy_r) begin
              mreq_valid_r <= 1'b1;
              mreq_addr_r  <= DESC_BASE_P + hdr_names_off_r
                              + 32'(name_load_lane_r << 3);
              mreq_beats_r <= (name_lanes_left_w
                               > 20'(NAME_BURST_BEATS_C))
                              ? 9'(NAME_BURST_BEATS_C)
                              : 9'(name_lanes_left_w);
            end
            if (accept_w) st_r <= S_NAM_RSP;
            else if (tmo_hit_w) begin
              fault_r      <= FAULT_TIMEOUT_C;
              mreq_valid_r <= 1'b0;
              tmo_r        <= '0;
              st_r         <= S_BAD;
            end
          end
        end
        S_NAM_RSP: begin
          if (beat_w && mem_rsp_err_i) begin
            fault_r <= FAULT_MEMERR_C;
            st_r    <= S_BAD;
          end else if (beat_w && mem_rsp_last_i) begin
            if ((name_load_lane_r + {11'd0, mreq_beats_r})
                < name_total_lanes_w) begin
              name_load_lane_r <= name_load_lane_r
                                  + {11'd0, mreq_beats_r};
              st_r <= S_NAM_REQ;
            end else begin
              img_valid_r <= 1'b1;
              fault_r     <= FAULT_NONE_C;
              if (heal_pend_r && !heal_kind_r) begin
                heal_pend_r <= 1'b0;
                scan_rd_r   <= '0;
                scan_cmp_r  <= 16'd0;
                scan_rdy_r  <= 1'b0;
                scan_base_r <= 16'd0;
                st_r        <= S_SCAN;
              end else if (heal_pend_r) begin
                heal_pend_r <= 1'b0;
                ans_err_r   <= 1'b0;
                ans_data_r  <= {48'd0, hdr_n_config_r};
                rd_pipe_r   <= 1'b0;
                st_r        <= S_ANSWER;
              end else st_r <= S_READY;
            end
          end else if (tmo_hit_w) begin
            fault_r    <= FAULT_TIMEOUT_C;
            mem_busy_r <= 1'b0;
            tmo_r      <= '0;
            st_r       <= S_BAD;
          end
        end

        // ---------------- serving -----------------------------------------
        S_READY, S_BAD: begin
          //! a heal walk that ended in a fault still owes its locate the
          //! honest miss - answered HERE, from the walk's outcome, never
          //! from the parked state it started in
          if (heal_pend_r) begin
            heal_pend_r  <= 1'b0;
            ans_pend_r   <= 1'b1;
            //! a LOCATE is owed the honest miss; an RGN_NCFG read is owed a
            //! plain 0 (pseudo-register reads never err) - the walked truth
            //! either way
            ans_err_r    <= !heal_kind_r;
            ans_data_r   <= 64'd0;
            rd_pipe_r    <= 1'b0;
            if (!heal_kind_r) begin
              desc_len_r   <= 16'd0;
              desc_nbase_r <= NAME_NONE_C;
              if (miss_cnt_r != 16'hFFFF) miss_cnt_r <= miss_cnt_r + 16'd1;
            end
            st_r <= S_ANSWER;
          end
          //! the static image is read-only at run time (07 §2): only the name
          //! overlay takes a write, everything else is dropped and counted
          if (take_wr_w && !st_name_i && (rowr_cnt_r != 16'hFFFF)) begin
            rowr_cnt_r <= rowr_cnt_r + 16'd1;
          end
          if ((st_r == S_READY) && take_wr_w && st_name_i
              && write_hits_current_w) begin
            patch_answer_r <= 1'b0;
            patch_name_r   <= 1'b0;
            patch_byte_r   <= 6'd0;
            st_r           <= S_PATCH_RD;
          end
          if (take_rd_w) begin
            ans_pend_r <= 1'b1;
            ans_err_r  <= 1'b0;
            if (st_name_i) begin
              rd_pipe_r <= 1'b1;
              rd_kind_r <= 2'd1;
              st_r      <= S_ANSWER;
            end else if (region_w == RGN_LOCATE_C) begin
              key_cfg_r   <= st_wdata_i[15:0];
              key_type_r  <= st_wdata_i[31:16];
              key_index_r <= st_wdata_i[47:32];
              if (img_valid_r) begin
                scan_rd_r   <= '0;
                scan_cmp_r  <= 16'd0;
                scan_rdy_r  <= 1'b0;
                scan_base_r <= 16'd0;
                st_r       <= S_SCAN;
              end else begin
                //! not loaded, or loaded wrong: HEAL BEFORE ANSWER (banner).
                //! The key is already latched; the walk runs now and the
                //! answer comes from its outcome, so a first command after a
                //! late software load is SERVED, not sacrificed to re-arm
                //! the probe for the second.
                heal_pend_r <= 1'b1;
                heal_kind_r <= 1'b0;
                st_r        <= S_HDR_REQ;
              end
            end else if ((region_w == RGN_NCFG_C) && !img_valid_r) begin
              //! configurations_count while invalid: HEAL FIRST (see the
              //! heal_kind_r note - this is the register E_RDESC checks
              //! before it ever locates, the w3a race's actual entry). The
              //! answer comes from the walked header, or 0 only when the
              //! walk itself still fails.
              heal_pend_r <= 1'b1;
              heal_kind_r <= 1'b1;
              st_r        <= S_HDR_REQ;
            end else begin
              rd_pipe_r <= 1'b1;
              unique case (region_w)
                //! an unvalidated image reports NOTHING, not the garbage its
                //! header walk happened to read
                RGN_NADDR_C: begin
                  rd_kind_r <= 2'd2;
                  if (name_lookup_valid_w) begin
                    rd_reg_r <= {41'd0, name_lookup_entry_w, 6'd0};
                  end else begin
                    rd_reg_r  <= 64'd0;
                    ans_err_r <= 1'b1;
                  end
                end
                RGN_NBASE_C: begin rd_kind_r <= 2'd2;
                                   rd_reg_r  <= img_valid_r
                                                ? {48'd0, desc_nbase_r} : 64'd0; end
                RGN_NCFG_C:  begin rd_kind_r <= 2'd2;
                                   rd_reg_r  <= {48'd0, hdr_n_config_r}; end
                RGN_LEN_C:   begin rd_kind_r <= 2'd2;
                                   rd_reg_r  <= img_valid_r
                                                ? {48'd0, desc_len_r} : 64'd0; end
                default:     rd_kind_r <= 2'd0;             // RGN_DATA_C
              endcase
              st_r <= S_ANSWER;
            end
          end
        end

        // ---------------- locate: scan the cached index map ----------------
        S_SCAN: begin
          scan_rd_r  <= scan_rd_r + IDX_AW_C'(1);
          scan_rdy_r <= 1'b1;
          if (scan_rdy_r) begin
            scan_cmp_r <= scan_cmp_r + 16'd1;
            //! HIT. `rel_w` is the key relative to the start of this entry's
            //! run. A key below the run cannot be served here - the run that
            //! owns it came earlier and would already have hit - so the
            //! `>= scan_base_r` guard is what stops the 16-bit wrap of the
            //! subtraction from landing inside `e_cnt_w` and serving the
            //! wrong descriptor.
            if (type_hit_w && e_usable_w
                && (key_index_r >= scan_base_r) && (rel_w < e_cnt_w)) begin
              desc_len_r   <= e_len_w;
              desc_nbase_r <= (e_nbase_w == NAME_NONE_C)
                              ? NAME_NONE_C : (e_nbase_w + rel_w);
              desc_off_r   <= e_off_w + (32'(e_strd_w) * 32'(rel_w));
              st_r         <= S_FET_REQ;
            //! RIGHT TYPE, EARLIER RUN. Step the running base over this run and
            //! keep scanning: a later entry of the same type may own the key.
            //! Only the end of the table can turn this into a miss, so this
            //! arm requires there to BE a later entry.
            end else if (type_hit_w && e_usable_w && !last_w) begin
              scan_base_r <= scan_base_r + e_cnt_w;
            //! MISS. Either the table is exhausted, or this entry matched the
            //! type but its geometry is unusable. The unusable case must miss
            //! HERE rather than scan on: its count cannot be trusted, so
            //! stepping the base over it would misalign every later run of the
            //! same type and serve a plausible wrong descriptor.
            end else if (last_w || (type_hit_w && !e_usable_w)) begin
              ans_err_r    <= 1'b1;
              ans_data_r   <= 64'd0;
              rd_pipe_r    <= 1'b0;
              desc_len_r   <= 16'd0;
              desc_nbase_r <= NAME_NONE_C;
              if (miss_cnt_r != 16'hFFFF) miss_cnt_r <= miss_cnt_r + 16'd1;
              st_r <= S_ANSWER;
            end
          end
        end

        // ---------------- locate: ONE burst for the whole descriptor -------
        S_FET_REQ: begin
          if (!mreq_valid_r && !mem_busy_r) begin
            mreq_valid_r <= 1'b1;
            mreq_addr_r  <= DESC_BASE_P + {desc_off_r[31:3], 3'd0};
            mreq_beats_r <= 9'(len_lanes_w);
          end
          if (accept_w) begin
            if (fetch_cnt_r != 16'hFFFF) fetch_cnt_r <= fetch_cnt_r + 16'd1;
            st_r <= S_FET_RSP;
          end else if (tmo_hit_w) begin
            mreq_valid_r <= 1'b0;
            tmo_r        <= '0;
            ans_err_r    <= 1'b1;
            ans_data_r   <= 64'd0;
            rd_pipe_r    <= 1'b0;
            desc_len_r   <= 16'd0;
            desc_nbase_r <= NAME_NONE_C;
            if (miss_cnt_r != 16'hFFFF) miss_cnt_r <= miss_cnt_r + 16'd1;
            st_r <= S_ANSWER;
          end
        end
        S_FET_RSP: begin
          if (beat_w && mem_rsp_err_i) begin
            ans_err_r    <= 1'b1;
            ans_data_r   <= 64'd0;
            rd_pipe_r    <= 1'b0;
            desc_len_r   <= 16'd0;
            desc_nbase_r <= NAME_NONE_C;
            if (miss_cnt_r != 16'hFFFF) miss_cnt_r <= miss_cnt_r + 16'd1;
            st_r <= S_ANSWER;
          end else if (beat_w && mem_rsp_last_i) begin
            if (desc_nbase_r != NAME_NONE_C) begin
              patch_answer_r <= 1'b1;
              patch_name_r   <= 1'b0;
              patch_byte_r   <= 6'd0;
              st_r           <= S_PATCH_RD;
            end else begin
              ans_err_r  <= 1'b0;
              ans_data_r <= 64'd0;        // base = the line-buffer origin
              rd_pipe_r  <= 1'b0;
              st_r       <= S_ANSWER;
            end
          end else if (tmo_hit_w) begin
            ans_err_r    <= 1'b1;
            ans_data_r   <= 64'd0;
            rd_pipe_r    <= 1'b0;
            mem_busy_r   <= 1'b0;
            desc_len_r   <= 16'd0;
            desc_nbase_r <= NAME_NONE_C;
            if (miss_cnt_r != 16'hFFFF) miss_cnt_r <= miss_cnt_r + 16'd1;
            st_r <= S_ANSWER;
          end
        end

        // ---------------- writable-name to descriptor coherence ----------
        S_PATCH_RD: begin
          //! Both RAMs are synchronous. This state presents the byte's source
          //! and destination lanes; S_PATCH_WR consumes their registered data.
          st_r <= S_PATCH_WR;
        end
        S_PATCH_WR: begin
          if (patch_byte_r != 6'd63) begin
            patch_byte_r <= patch_byte_r + 6'd1;
            st_r         <= S_PATCH_RD;
          end else if ((key_type_r == 16'h0000) && !patch_name_r) begin
            patch_name_r <= 1'b1;
            patch_byte_r <= 6'd0;
            st_r         <= S_PATCH_RD;
          end else if (patch_answer_r) begin
            ans_err_r  <= 1'b0;
            ans_data_r <= 64'd0;
            rd_pipe_r  <= 1'b0;
            st_r       <= S_ANSWER;
          end else begin
            st_r <= S_READY;
          end
        end

        // ---------------- the one-cycle answer ------------------------------
        S_ANSWER: begin
          if (rd_pipe_r) begin
            rd_pipe_r <= 1'b0;
            unique case (rd_kind_r)
              2'd1:    ans_data_r <= name_q_r;
              2'd2:    ans_data_r <= rd_reg_r;
              default: ans_data_r <= (32'(st_addr_i[15:3]) < 32'(len_lanes_w))
                                     ? line_q_r : 64'd0;
            endcase
          end else begin
            ans_pend_r <= 1'b0;
            //! an invalid image re-probes its header after every locate
            st_r       <= img_valid_r ? S_READY : S_HDR_REQ;
          end
        end

        default: st_r <= S_BAD;
      endcase
    end
  end

endmodule : KL_aecp_desc_store
`default_nettype wire

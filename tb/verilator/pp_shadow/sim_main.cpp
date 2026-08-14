// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// milan_datapath with the protocol processor as THE control plane — the
// SUBSTITUTION harness.
//
// THE PREMISE INVERTED (2026-08-13). This file used to grade "shadow
// discipline": the processor was elaborated beside a live legacy 1722.1/SRP
// plane with tx_drain_i = 1, and the safety property was that the MAC TX port
// stayed SILENT no matter how hard the processor wanted to transmit. That
// plane is deleted. milan_datapath instantiates KL_pp_shadow unconditionally,
// ties tx_drain_i to 0 and merges the processor's packed TX with MAAP's
// through ctl_tx_mux, so the property is now the exact opposite and sections
// D and F grade it that way: the processor's frames MUST reach the MAC.
//
// What this suite proves, and why each check exists:
//
//   A. The plane is THERE and the CSR window decodes it. PP_STAT carries a
//      constant 0x5B tag, so a structural zero (the answer every undecoded
//      address gives) can never be mistaken for "present and idle".
//
//   B. The RX path works end to end: MAC AXIS beat -> aligned-lane classifier
//      -> control-frame FIFO -> byte serializer -> the processor's own
//      validator. The counter only moves when the processor ACCEPTED a whole
//      frame, so it is evidence about the processor, not about the wrapper.
//
//   C. The classifier REJECTS non-control traffic. This is the check that
//      protects the board: the serializer runs at 1 B/clk = 100 MB/s against
//      gigabit's 125 MB/s, so an unfiltered tap would lag and corrupt rather
//      than drop. A frame that should not enter must not enter.
//
//   D. SUBSTITUTION — the processor OWNS THE WIRE. It is driven until its own
//      TX frame counter moves, and frames must EGRESS at the MAC TX boundary
//      over the same window. This is the check that would catch a build that
//      left tx_drain_i asserted, or a ctl_tx_mux leg that was never connected:
//      with the legacy plane deleted, a drained processor is a device that
//      answers nothing at all.
//
//   E. The side port answers over the CSR bridge with the processor's OWN
//      magic word ("KLPP") and its shape. That word is generated inside
//      protocol_processor_top, so reading it is proof the fabric is alive and
//      clocked, not that the bridge returns a plausible constant.
//
//   F. THE ADP ADVERTISEMENT IS DECODED, NOT COUNTED. A frame census is weak
//      evidence - it cannot tell an ENTITY_AVAILABLE from a runt. The ADPDU
//      that egresses is rebuilt byte for byte from the 0x600 CSR identity
//      group (entity_id, entity_model_id, capabilities, the RO 0x618/0x61C
//      shape words, the gPTP pair) and compared against the wire, every byte
//      except the available_index, which is graded separately for strict
//      growth. That comparison is also the sharpest available corruption
//      detector for the shared control lane: one spliced MAAP beat and the
//      compare fails.
//
//   G. The CLASS-D FABRIC FACE is reachable AND LIVE. A port read once at
//      reset proves only that a wire exists; adp_next_avail_index_o is read
//      before the processor has ever advertised (must be 0) and again after
//      its compressed ADP cadence has fired (must have grown), so the check
//      is about a moving engine and not about a constant.
//
//   H. The MAAP ADAPTER REFUSES SAFELY. With no claimed block the shim must
//      still ACCEPT every request and ANSWER it — ok = 0 — because the
//      processor's allocator-busy flag is cleared only by a response: accept
//      once without answering and that source never allocates again. So the
//      graded invariant is accepted == answered, globally, plus "the DA gate
//      stayed shut" and "the plane kept serving" (side port still answers,
//      control frames still accepted). This is the regression test for the
//      one hazard this adapter can create.
//
//   I. The MAAP ADAPTER GRANTS. With KL_maap in ANNOUNCE the same request is
//      answered ok = 1 with base + source_index, and the processor's
//      per-source DA gate (acmp_declaring_o — reachable ONLY through an
//      ALLOC_DA success) goes HIGH. The granted address is checked against
//      the pool base and the offset KL_maap publishes in MAAP_STAT0, so a
//      shim that answered a plausible constant fails.
//
//   K. THE SHARED CONTROL LANE. ctl_tx_mux merges the processor's packed TX
//      with KL_maap's PROBE/ANNOUNCE PDUs. Both sources must be REPRESENTED
//      at the MAC boundary (an interleave test where only one side ever
//      transmits proves nothing), every frame must be WELL FORMED (its
//      declared control_data_length must account for its actual length, and
//      no beat before the last may carry a partial tkeep), and the TX-trunk
//      arbiters must show no abort and no stall: an abort is the watchdog
//      injecting a close beat, which IS a corrupted frame on the wire.
//      A_TXARB_DIAG's lane map is LSB-first 0 ctl_tx, 1 aaf_final, 2 crf_dp,
//      3 adp_tx, and bits 7:4 are a documented structural zero.
//
//   J. The global anti-wedge invariant: accepted == answered over every cycle.
//
// The talker source enable is NOT a -G any more: KL_pp_shadow's SRC_EN_MASK_P
// is deleted and milan_datapath drives cfg_src_en_i from the entity shape
// ({ACMP_SRC_C{1'b1}}), so every declared STREAM_OUTPUT is live on every
// build. There is no "no source enabled" arm left to select.
//
// Frames are injected LITTLE-LANE (tdata[7:0] = first wire byte). That is the
// silicon convention of the RX tap — KL_maap.sv:154 states it and tests the
// EtherType at lanes 4/5. The vlan_frame() helper in milan_dp/sim_main.cpp
// packs the OTHER way for the TX classifier path; copying it here would feed
// the processor byte-swapped frames and every accept check would read a
// silent zero.

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;

// ---- free-running observers -------------------------------------------------
// Sampled on EVERY simulated cycle (from lo(), the settled pre-edge state), so
// nothing that happens between two CSR reads can be missed. The maap face is
// two cycles wide per transaction; polling it from the check sites would grade
// whatever the sampling happened to land on.
//
// The class-D levels and the maap face are read through Verilator's flat root
// handle. They are datapath NETS marked `verilator public_flat_rd` — the same
// mechanism media_tick_p / aaf_stream_en_w already use — and NOT a CSR window:
// no software reads this state yet, and inventing a CSR for it would be a
// VERSION story for a register with no consumer.
struct MaapObs {
    long accepted   = 0;   // req_valid && req_ready — the shim took a request
    long answered   = 0;   // rsp_valid              — the shim completed one
    long granted    = 0;   // rsp_valid && rsp_ok    — with an address
    long released   = 0;   // req_valid && req_release — a RELEASE_DA offered
    uint64_t last_da = 0;  // the address of the last grant
    long declaring_cycles = 0;  // cycles acmp_declaring_o[0] was high
};
static MaapObs mo;

// ---- MAC TX frame census, whole frames, byte for byte ----------------------
// The old census kept only a destination MAC per frame, because the graded
// property was "no frame at all". Now that the processor owns the wire the
// frame CONTENT is the evidence, so every egressed frame is retained.
struct TxFrame {
    std::vector<uint8_t> bytes;
    int  beats      = 0;
    bool short_beat = false;   // a non-final beat with a partial tkeep
};
static std::vector<TxFrame> tx_frames;
static bool     tx_open = false;
static long     tx_bad_keep = 0;      // partial tkeep before tlast, any frame
static long     tx_beats_total = 0;

static const uint64_t MAAP_DST = 0x91E0F000FF00ull;  // KL_maap's own TX DA

static void observe() {
    auto* rp = dut->rootp;
    if (rp->milan_datapath__DOT__pp_maap_req_valid_w
        && rp->milan_datapath__DOT__pp_maap_req_ready_w) mo.accepted++;
    if (rp->milan_datapath__DOT__pp_maap_req_valid_w
        && rp->milan_datapath__DOT__pp_maap_req_release_w) mo.released++;
    if (rp->milan_datapath__DOT__pp_maap_rsp_valid_w) {
        mo.answered++;
        if (rp->milan_datapath__DOT__pp_maap_rsp_ok_w) {
            mo.granted++;
            mo.last_da = rp->milan_datapath__DOT__pp_maap_rsp_da_w;
        }
    }
    if (rp->milan_datapath__DOT__pp_cd_acmp_declaring_w & 1u) mo.declaring_cycles++;

    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
        if (!tx_open) { tx_frames.push_back(TxFrame()); tx_open = true; }
        TxFrame& f = tx_frames.back();
        const uint8_t keep = (uint8_t)dut->m_axis_mac_tx_tkeep;
        const uint64_t d   = dut->m_axis_mac_tx_tdata;
        for (int l = 0; l < 8; l++)
            if ((keep >> l) & 1) f.bytes.push_back((uint8_t)((d >> (8 * l)) & 0xFF));
        f.beats++;
        tx_beats_total++;
        if (!dut->m_axis_mac_tx_tlast && keep != 0xFF) {
            f.short_beat = true; tx_bad_keep++;
        }
        if (dut->m_axis_mac_tx_tlast) tx_open = false;
    }
}

// ---- frame classification, off the captured bytes --------------------------
enum FrClass { FR_SHORT, FR_ADP, FR_AECP, FR_ACMP, FR_MAAP, FR_AVTP_OTHER,
               FR_MSRP, FR_MVRP, FR_ALIEN };

static FrClass classify(const TxFrame& f) {
    if (f.bytes.size() < 15) return FR_SHORT;
    const unsigned et = ((unsigned)f.bytes[12] << 8) | f.bytes[13];
    if (et == 0x22EA) return FR_MSRP;
    if (et == 0x88F5) return FR_MVRP;
    if (et != 0x22F0) return FR_ALIEN;
    switch (f.bytes[14]) {
        case 0xFA: return FR_ADP;
        case 0xFB: return FR_AECP;
        case 0xFC: return FR_ACMP;
        case 0xFE: return FR_MAAP;
        default:   return FR_AVTP_OTHER;
    }
}

// An AVTP control PDU declares its own length: control_data_length is 11 bits
// spread over wire bytes 16[2:0] and 17, and the payload it counts starts at
// wire byte 26 (after the 12-byte AVTP control header). So the frame is
// 14 + 12 + cdl octets, padded up to the 60-octet Ethernet minimum. A frame
// whose actual length disagrees with the length it declares is corrupt -
// which is exactly what a beat spliced in from the other leg of ctl_tx_mux
// would produce.
static bool avtp_len_consistent(const TxFrame& f, size_t* want_out) {
    if (f.bytes.size() < 18) return false;
    const size_t cdl  = (((size_t)f.bytes[16] & 0x7) << 8) | f.bytes[17];
    size_t want = 14 + 12 + cdl;
    if (want < 60) want = 60;
    if (want_out) *want_out = want;
    return f.bytes.size() == want;
}

static void ck(const char* what, uint32_t got, uint32_t exp) {
    checks++;
    bool ok = (got == exp);
    if (!ok) fails++;
    printf("  [%s] %-42s got=0x%08X exp=0x%08X\n", ok ? "PASS" : "FAIL", what, got, exp);
}

static void ck_true(const char* what, bool cond, const char* detail) {
    checks++;
    if (!cond) fails++;
    printf("  [%s] %-42s %s\n", cond ? "PASS" : "FAIL", what, detail);
}

// ---- the DESCRIPTOR MEMORY the AECP store fetches from ----------------------
// milan_datapath grew nine top-level ports for it (o_desc_mem_req_valid /
// i_desc_mem_req_ready / o_desc_mem_req_addr / o_desc_mem_req_beats /
// i_desc_mem_rsp_valid / o_desc_mem_rsp_ready / i_desc_mem_rsp_data /
// i_desc_mem_rsp_last / i_desc_mem_rsp_err), because the entity model is far
// too large to spend RAMB tiles on and lives in the integrator's main memory
// at the compile-time PP_DESC_BASE_P.
//
// A HARNESS THAT LEAVES i_desc_mem_req_ready AT 0 IS NOT NEUTRAL. It is the
// documented degrade path: KL_aecp_desc_store's watchdog abandons the burst,
// the image never validates, every locate answers err and READ_DESCRIPTOR
// comes back NO_SUCH_DESCRIPTOR. That is legal behaviour and section [M]
// below drives it ON PURPOSE and says so — but it is not a test of
// READ_DESCRIPTOR, and leaving it accidental is how "the device answers AECP"
// would go ungraded while the suite exited 0.
//
// So this model serves a REAL, VALID image: one outstanding request, in-order
// beats, `last` on the final one, `rsp_ready` tied 1 by the store.
static const uint32_t DESC_BASE = 0x20000000u;

static std::vector<uint8_t> desc_img;      // the AEMI image, byte for byte
static bool     mem_answering = true;      // section [M] turns this off
static bool     mem_busy      = false;
static uint32_t mem_cur       = 0;         // byte address of the next beat
static int      mem_left      = 0;         // beats still owed
static long     mem_reqs      = 0;         // bursts accepted, for the record

static uint64_t desc_beat(uint32_t byte_addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {          // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - DESC_BASE + (uint32_t)i;
        const uint8_t  b   = (off < desc_img.size()) ? desc_img[off] : 0;
        v = (v << 8) | b;
    }
    return v;
}

// driven BEFORE eval, off state settled at the previous edge
static void mem_drive() {
    dut->i_desc_mem_req_ready = (mem_answering && !mem_busy) ? 1 : 0;
    dut->i_desc_mem_rsp_valid = mem_busy ? 1 : 0;
    dut->i_desc_mem_rsp_data  = mem_busy ? desc_beat(mem_cur) : 0;
    dut->i_desc_mem_rsp_last  = (mem_busy && mem_left == 1) ? 1 : 0;
    dut->i_desc_mem_rsp_err   = 0;
}

// sampled AFTER eval with clk still low: this is what the coming edge commits
static void mem_edge() {
    if (!mem_busy) {
        if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
            mem_cur  = dut->o_desc_mem_req_addr;
            mem_left = (int)dut->o_desc_mem_req_beats;
            mem_busy = (mem_left > 0);
            mem_reqs++;
        }
    } else if (dut->o_desc_mem_rsp_ready) {
        mem_cur += 8;
        if (--mem_left <= 0) mem_busy = false;
    }
}

// ---- the AECP RESPONSE BUFFER's memory (a SECOND, read+write master) -------
// milan_datapath grew sixteen more top-level ports (o_resp_mem_req_* /
// i_resp_mem_rsp_* / o_resp_mem_wr_* / i_resp_mem_wr_done / _wr_err) because
// the response an AECP command builds is up to 592 bytes and, held as fabric
// flops, it was 5,079 of them - the state the placer could not pack on a die
// whose block RAM was already 100% used.
//
// THE SAME "NOT NEUTRAL" RULE AS THE DESCRIPTOR FACE, and here it bites
// harder: leaving i_resp_mem_req_ready / i_resp_mem_wr_ready at 0 makes the
// buffer's watchdog void EVERY response and KL_aecp_engine answer
// ENTITY_MISBEHAVING to every command - a legal degrade that section [N]
// drives on purpose, and a silent gutting of section [L] if left accidental.
//
// This model is the bridge contract, enforced rather than assumed:
//   * ONE outstanding read burst, beats IN ORDER, `last` on the final one;
//   * rsp_ready is REAL BACKPRESSURE - the beat is HELD until it is taken;
//   * ONE outstanding single-beat write; byte `addr + n` is wr_data
//     [63-8n -: 8] and A ZERO-STROBE BYTE IS NOT MODIFIED (the model leaves
//     those bytes alone, so a bridge that clobbered them would be visible);
//   * wr_done is a ONE-CYCLE pulse issued STRICTLY AFTER the wr_ready that
//     accepted the write - the acknowledged bridge, which is what
//     sw/litex/milan_soc.py builds.
static const uint32_t RESP_BASE  = 0x20100000u;   // PP_RESP_BASE_P default
static const uint32_t RESP_BYTES = 592u;          // 16 + PP_DESC_LINE_BYTES_P

static uint8_t  rmem[RESP_BYTES];
static bool     rmem_answering = true;     // section [N] turns this off
static bool     rm_busy   = false;         // read burst in flight
static uint32_t rm_cur    = 0;
static int      rm_left   = 0;
static bool     rm_wpend  = false;         // write accepted, commits this cycle
static uint32_t rm_waddr  = 0;
static uint64_t rm_wdata  = 0;
static uint32_t rm_wstrb  = 0;
static long     rm_reqs   = 0;             // read bursts accepted
static long     rm_writes = 0;             // lane writes committed

static uint64_t rmem_beat(uint32_t byte_addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {          // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - RESP_BASE + (uint32_t)i;
        const uint8_t  b   = (off < RESP_BYTES) ? rmem[off] : 0;
        v = (v << 8) | b;
    }
    return v;
}

static void rmem_drive() {
    dut->i_resp_mem_req_ready = (rmem_answering && !rm_busy) ? 1 : 0;
    dut->i_resp_mem_rsp_valid = rm_busy ? 1 : 0;
    dut->i_resp_mem_rsp_data  = rm_busy ? rmem_beat(rm_cur) : 0;
    dut->i_resp_mem_rsp_last  = (rm_busy && rm_left == 1) ? 1 : 0;
    dut->i_resp_mem_rsp_err   = 0;
    // a write is accepted on one edge and COMMITTED on the next: wr_done can
    // never coincide with the wr_ready that took it, which is the only shape
    // KL_aecp_resp_buf's R_FLUSH arm accepts (it sets wbusy_r on the ready and
    // only THEN looks for the done)
    dut->i_resp_mem_wr_ready  = (rmem_answering && !rm_wpend) ? 1 : 0;
    dut->i_resp_mem_wr_done   = rm_wpend ? 1 : 0;
    dut->i_resp_mem_wr_err    = 0;
}

static void rmem_edge() {
    if (!rm_busy) {
        if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
            rm_cur  = dut->o_resp_mem_req_addr;
            rm_left = (int)dut->o_resp_mem_req_beats;
            rm_busy = (rm_left > 0);
            rm_reqs++;
        }
    } else if (dut->o_resp_mem_rsp_ready) {   // REAL backpressure: only then
        rm_cur += 8;
        if (--rm_left <= 0) rm_busy = false;
    }
    if (rm_wpend) {
        for (int i = 0; i < 8; i++) {
            if ((rm_wstrb >> i) & 1) {       // a 0 strobe leaves the byte alone
                const uint32_t k = rm_waddr - RESP_BASE + (uint32_t)i;
                if (k < RESP_BYTES) rmem[k] = (uint8_t)(rm_wdata >> (56 - 8 * i));
            }
        }
        rm_writes++;
        rm_wpend = false;
    } else if (dut->o_resp_mem_wr_valid && dut->i_resp_mem_wr_ready) {
        rm_waddr = dut->o_resp_mem_wr_addr;
        rm_wdata = dut->o_resp_mem_wr_data;
        rm_wstrb = dut->o_resp_mem_wr_strb;
        rm_wpend = true;
    }
}

// ---- clocking (single domain, as milan_dp drives it) ----
static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0; mem_drive(); rmem_drive(); dut->eval(); observe(); mem_edge(); rmem_edge(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->eval(); }
static void step() { lo(); hi(); }

// ---- AXI4-Lite BFM (identical protocol/timing to the milan_dp harness) ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_awready && dut->s_axi_wready; hi(); if (acc) break; }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 2048; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_arready; hi(); if (acc) break; }
    dut->s_axi_arvalid = 0;
    uint32_t d = 0;
    for (int g = 0; g < 2048; g++) { lo(); bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi(); if (rv) break; }
    dut->s_axi_rready = 0;
    return d;
}

enum {
    A_ID = 0x000, A_VERSION = 0x004,
    A_MAC_ALO = 0x108, A_MAC_AHI = 0x10C,
    A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
    A_ADP_MDLLO = 0x60C, A_ADP_MDLHI = 0x610, A_ADP_CAPS = 0x614,
    A_ADP_TALK = 0x618, A_ADP_LIST = 0x61C,
    A_ADP_GMLO = 0x624, A_ADP_GMHI = 0x628, A_ADP_GDOM = 0x62C,
    A_MAAP_CTRL = 0x6CC, A_MAAP_STAT0 = 0x6D0, A_MAAP_STAT1 = 0x6D4,
    A_TXARB_DIAG = 0x784,
    A_PP_CTRL = 0x920, A_PP_STAT = 0x924,
    A_PP_SPADDR = 0x928, A_PP_SPDATA = 0x92C, A_PP_DIAG = 0x930,
};

// The entity_id this harness provisions. NOT zero on purpose: the processor's
// talker matches a PROBE_TX on target_eid == own entity_id, and against a zero
// entity_id a frame whose bytes never arrived would match just as well.
static const uint64_t TEST_EID   = 0x001BC50CAC000001ull;
static const uint64_t TEST_MODEL = 0x001BC5441BC55569ull;

// The station MAC this harness programs, in the CSR's platform LSB-first
// packing (ALO[7:0] = the FIRST wire byte). KL_pp_shadow takes the byte
// REVERSED numeric EUI-48, so the ADPDU's source address must come out
// 02:00:00:00:00:01 on the wire — the swapped form is 01:.. = a multicast
// source address, which every bridge drops.
static const uint32_t STA_MAC_LO = 0x00000002u;   // wire bytes 0..3 = 02 00 00 00
static const uint32_t STA_MAC_HI = 0x00000100u;   // wire bytes 4..5 = 00 01
static const uint8_t  STA_MAC[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x01};

// KL_maap's pool: 91:E0:F0:00 + a 16-bit offset (KL_maap.sv POOL_BASE_HI_C).
static const uint64_t MAAP_POOL_BASE = 0x91E0F0000000ull;

// side-port windows implemented by protocol_processor_top (tb/pp_top README)
static const uint32_t SP_SNAPSHOT = 0x20000;   // word 0 = magic "KLPP"

static void do_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1; dut->m_axis_rx_tready = 1; dut->m_axis_ts_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 16; i++) step();
}

// ---- inject one little-lane frame on the MAC RX port ----
static void inject_rx(const uint8_t* f, size_t len, int tail_cycles) {
    size_t beats = (len + 7) / 8;
    std::vector<uint64_t> bw(beats, 0);
    std::vector<uint8_t>  bk(beats, 0);
    for (size_t i = 0; i < len; i++) {
        bw[i / 8] |= (uint64_t)f[i] << (8 * (i % 8));
        bk[i / 8] |= (uint8_t)(1u << (i % 8));
    }
    size_t idx = 0;
    dut->m_axis_rx_tready = 1;
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < (int)beats + tail_cycles; c++) {
        if (idx < beats) {
            dut->s_axis_mac_rx_tdata  = bw[idx];
            dut->s_axis_mac_rx_tkeep  = bk[idx];
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats - 1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
}

// run free cycles with the MAC TX sink always ready
static void run_idle(int cycles) {
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < cycles; c++) { lo(); hi(); }
}

// ---- posted side-port access over the CSR bridge ----
static uint32_t sp_read(uint32_t word_addr, bool* ok) {
    axi_write(A_PP_SPADDR, word_addr);            // arm: posts the read
    for (int g = 0; g < 4096; g++) {
        if ((axi_read(A_PP_STAT) & 1u) == 0) {    // STAT[0] = sp_busy
            if (ok) *ok = true;
            return axi_read(A_PP_SPDATA);
        }
        step();
    }
    if (ok) *ok = false;
    return 0;
}

// ---- frame builders (wire order, byte 0 = first DA octet) ----
static const uint8_t OUR_MAC[6] = {0x00, 0x1B, 0xC5, 0x0C, 0xAC, 0x00};

// ADP ENTITY_DISCOVER: DA 91:E0:F0:01:00:00, EtherType 0x22F0, subtype 0xFA,
// msg_type 2. 82 bytes on the wire (the ADPDU rule this repo enforces) = 14 B
// Ethernet + a 68 B ADPDU, i.e. control_data_length 56.
//
// CORRECTED 2026-08-12. This builder used to put the message_type in wire byte
// 16 and leave byte 15 at 0. Byte 15 is sv/version/MESSAGE_TYPE and byte 16 is
// valid_time + control_data_length[10:8], so the frame declared msg_type 0
// (ENTITY_AVAILABLE) with control_data_length 512 against a 68 B payload — the
// processor's V1 length rule threw it away, every time. Nothing caught it
// because rx_frames_o counts frames the WRAPPER handed to the processor, not
// frames the processor accepted: the count moved and the check read green
// while the engine behind it never saw a valid ADPDU. The class-D
// available_index check below is what finally made it visible — a level that
// only moves when the ADP engine actually TRANSMITS cannot be satisfied by a
// frame the ADP engine never accepted.
static size_t build_adp_discover(uint8_t* f) {
    memset(f, 0, 82);
    const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
    const uint8_t sa[6] = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
    memcpy(f, da, 6); memcpy(f + 6, sa, 6);
    f[12] = 0x22; f[13] = 0xF0;          // EtherType
    f[14] = 0xFA;                        // subtype ADP
    f[15] = 0x02;                        // sv=0, version=0, msg_type=ENTITY_DISCOVER
    f[16] = 0x00; f[17] = 56;            // valid_time 0, control_data_length 56
    // target entity_id at @4 (wire bytes 18..25) stays 0 = discover everybody
    return 82;
}

static void put64be(uint8_t* p, uint64_t v) {
    for (int i = 0; i < 8; i++) p[i] = (uint8_t)(v >> (8 * (7 - i)));
}
static void put32be(uint8_t* p, uint32_t v) {
    for (int i = 0; i < 4; i++) p[i] = (uint8_t)(v >> (8 * (3 - i)));
}
static void put16be(uint8_t* p, uint16_t v) { p[0] = (uint8_t)(v >> 8); p[1] = (uint8_t)v; }

static uint64_t get_be(const std::vector<uint8_t>& b, size_t off, size_t n) {
    uint64_t v = 0;
    for (size_t i = 0; i < n; i++) v = (v << 8) | b[off + i];
    return v;
}

// Milan PROBE_TX = IEEE 1722.1 CONNECT_TX_COMMAND (ACMP message_type 0),
// aimed at OUR OWN talker source `uid`. 70 bytes on the wire: 14 B Ethernet +
// a 56 B ACMPDU (control_data_length 44) — the length rule this repo pins
// after the 68-byte listener-deafness finding.
//
// Two offsets are load-bearing and easy to get wrong:
//   * @20 talker_entity_id (wire 34..41) is what the TALKER discriminates on.
//     protocol_processor_top's ACMP steer PREFETCHES those eight bytes out of
//     the RX slot and REWRITES txn.target_eid with them, precisely because the
//     validator's generic extraction puts the ACMPDU's @4 stream_id there.
//     Setting only @4 leaves the talker deaf with no counter moving anywhere.
//   * @36 talker_unique_id (wire 50..51) selects the source; the validator
//     takes @36 for message types 0..5 and @38 for the listener's 6..11.
static size_t build_probe_tx(uint8_t* f, uint64_t eid, uint16_t uid) {
    memset(f, 0, 70);
    const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
    const uint8_t sa[6] = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
    memcpy(f, da, 6); memcpy(f + 6, sa, 6);
    f[12] = 0x22; f[13] = 0xF0;      // EtherType 1722
    f[14] = 0xFC;                    // subtype ACMP
    f[15] = 0x00;                    // sv=0, version=0, message_type=0
    f[16] = 0x00; f[17] = 44;        // status 0, control_data_length 44
    put64be(f + 18, eid);                        // @4  stream_id
    put64be(f + 26, 0xC0FFEE00DEADBEEFull);      // @12 controller_entity_id
    put64be(f + 34, eid);                        // @20 talker_entity_id
    put64be(f + 42, 0x2222222222222222ull);      // @28 listener_entity_id
    f[50] = (uint8_t)(uid >> 8); f[51] = (uint8_t)uid;   // @36 talker_unique_id
    f[52] = 0x00; f[53] = 0x00;                          // @38 listener_unique_id
    f[62] = 0x00; f[63] = 0x01;                          // @48 sequence_id
    return 70;
}

// ---- the AEM descriptor image (hdl/aecp/desc/gen_desc_image.py layout) -----
// Built here rather than shelled out to the generator so the harness OWNS the
// bytes it will compare the wire against: an image produced by the same tool
// the DUT trusts, compared against itself, proves only that the tool is
// self-consistent. Everything is big-endian, the 1722.1 wire order.
//
//   header @0x00   32 B, four 64-bit beats; the eight u32 words must sum to
//                  0xFFFFFFFF or KL_aecp_desc_store refuses the whole image
//   index  @0x20   2 x 16 B, sorted by (config, type)
//   descs  @0x40   ENTITY[0] 40 B, then CONFIGURATION[0..1] 24 B each
//
// CONFIGURATION carries TWO descriptors on purpose: index 1 can only be
// answered correctly if the store applies elem_off + index*elem_stride, so a
// store that ignored the index would return CONFIGURATION[0]'s bytes and fail
// the byte-exact compare.
static const uint16_t DTY_ENTITY_C = 0x0000;
static const uint16_t DTY_CONFIG_C = 0x0001;
static const uint16_t DTY_ABSENT_C = 0x0002;   // AUDIO_UNIT: not in this image
static const size_t   ENT_LEN_C    = 40;
static const size_t   CFG_LEN_C    = 24;
static const uint32_t ENT_OFF_C    = 0x40;
static const uint32_t CFG_OFF_C    = 0x40 + 40;          // 0x68
static const uint32_t IMG_END_C    = CFG_OFF_C + 2 * 24; // 0x98

static void put32be_v(std::vector<uint8_t>& v, size_t off, uint32_t x) {
    for (int i = 0; i < 4; i++) v[off + i] = (uint8_t)(x >> (8 * (3 - i)));
}
static void put16be_v(std::vector<uint8_t>& v, size_t off, uint16_t x) {
    v[off] = (uint8_t)(x >> 8); v[off + 1] = (uint8_t)x;
}

// the descriptor bytes this harness expects back on the wire
static std::vector<uint8_t> desc_bytes(uint16_t type, uint16_t index) {
    const size_t n = (type == DTY_ENTITY_C) ? ENT_LEN_C : CFG_LEN_C;
    std::vector<uint8_t> d(n, 0);
    put16be_v(d, 0, type);
    put16be_v(d, 2, index);
    const uint8_t seed = (uint8_t)(0xA0 + 0x10 * type + 0x08 * index);
    for (size_t i = 4; i < n; i++) d[i] = (uint8_t)(seed + i);
    return d;
}

static void build_desc_image() {
    desc_img.assign(IMG_END_C, 0);
    // --- index map @0x20 ---------------------------------------------------
    // {cfg, type, count, elem_len, elem_off, name_base, elem_stride}
    put16be_v(desc_img, 0x20 + 0x0, 0);              // configuration_index
    put16be_v(desc_img, 0x20 + 0x2, DTY_ENTITY_C);
    put16be_v(desc_img, 0x20 + 0x4, 1);              // count
    put16be_v(desc_img, 0x20 + 0x6, (uint16_t)ENT_LEN_C);
    put32be_v(desc_img, 0x20 + 0x8, ENT_OFF_C);
    put16be_v(desc_img, 0x20 + 0xC, 0xFFFF);         // unnamed
    put16be_v(desc_img, 0x20 + 0xE, (uint16_t)ENT_LEN_C);   // stride (8-aligned)
    put16be_v(desc_img, 0x30 + 0x0, 0);
    put16be_v(desc_img, 0x30 + 0x2, DTY_CONFIG_C);
    put16be_v(desc_img, 0x30 + 0x4, 2);              // TWO of them
    put16be_v(desc_img, 0x30 + 0x6, (uint16_t)CFG_LEN_C);
    put32be_v(desc_img, 0x30 + 0x8, CFG_OFF_C);
    put16be_v(desc_img, 0x30 + 0xC, 0xFFFF);
    put16be_v(desc_img, 0x30 + 0xE, (uint16_t)CFG_LEN_C);
    // --- descriptors -------------------------------------------------------
    {
        auto e = desc_bytes(DTY_ENTITY_C, 0);
        memcpy(&desc_img[ENT_OFF_C], e.data(), e.size());
        auto c0 = desc_bytes(DTY_CONFIG_C, 0);
        memcpy(&desc_img[CFG_OFF_C], c0.data(), c0.size());
        auto c1 = desc_bytes(DTY_CONFIG_C, 1);
        memcpy(&desc_img[CFG_OFF_C + CFG_LEN_C], c1.data(), c1.size());
    }
    // --- header @0x00, checksum LAST ---------------------------------------
    put32be_v(desc_img, 0x00, 0x41454D49u);          // "AEMI"
    put16be_v(desc_img, 0x04, 1);                    // layout_version
    put16be_v(desc_img, 0x06, 1);                    // n_config
    put16be_v(desc_img, 0x08, 2);                    // n_entries
    put16be_v(desc_img, 0x0A, 0);                    // n_names
    put32be_v(desc_img, 0x0C, 0x20);                 // index_off
    put32be_v(desc_img, 0x10, IMG_END_C);            // names_off (empty)
    put32be_v(desc_img, 0x14, IMG_END_C);            // image_bytes
    put16be_v(desc_img, 0x18, (uint16_t)ENT_LEN_C);  // desc_max_len
    put16be_v(desc_img, 0x1A, 0);                    // reserved
    uint32_t sum = 0;
    for (int w = 0; w < 7; w++)
        sum += ((uint32_t)desc_img[4*w] << 24) | ((uint32_t)desc_img[4*w+1] << 16)
             | ((uint32_t)desc_img[4*w+2] << 8) |  (uint32_t)desc_img[4*w+3];
    put32be_v(desc_img, 0x1C, 0xFFFFFFFFu - sum);
}

// ---- an AECP AEM command on the wire ---------------------------------------
// IEEE 1722.1-2021 9.2.1: 14 B Ethernet + the 24 B AECPDU header + payload.
// `control_data_length` is this architecture's offset-from-@12 convention, so
// it is 12 + payload. UNICAST to the station MAC — KL_pp_shadow accepts any DA
// carrying EtherType 0x22F0 and lets the processor's own validator judge.
static const uint8_t CTLR_MAC[6] = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
static const uint64_t CTLR_EID   = 0xC0FFEE00DEADBEEFull;

static size_t build_aecp(uint8_t* f, uint8_t msg_type, uint64_t target_eid,
                         uint16_t opcode, uint16_t seq,
                         const uint8_t* pld, size_t pld_len) {
    const size_t len = 14 + 24 + pld_len;
    memset(f, 0, len);
    memcpy(f, STA_MAC, 6);                       // DA: the entity
    memcpy(f + 6, CTLR_MAC, 6);                  // SA: the controller
    f[12] = 0x22; f[13] = 0xF0;
    f[14] = 0xFB;                                // AVTP subtype AECP
    f[15] = (uint8_t)(msg_type & 0x0F);          // sv=0, version=0
    const uint16_t cdl = (uint16_t)(12 + pld_len);
    f[16] = (uint8_t)((cdl >> 8) & 0x07);        // status 0 on a command
    f[17] = (uint8_t)(cdl & 0xFF);
    put64be(f + 18, target_eid);
    put64be(f + 26, CTLR_EID);
    put16be(f + 34, seq);
    put16be(f + 36, opcode);                     // u = 0
    if (pld_len) memcpy(f + 38, pld, pld_len);
    return len;
}

// READ_DESCRIPTOR payload: configuration_index, reserved, type, index
static size_t build_read_desc(uint8_t* f, uint16_t cfg, uint16_t type,
                              uint16_t index, uint16_t seq) {
    uint8_t pl[8];
    put16be(pl + 0, cfg); put16be(pl + 2, 0);
    put16be(pl + 4, type); put16be(pl + 6, index);
    return build_aecp(f, 0 /* AEM_COMMAND */, TEST_EID, 0x0004, seq, pl, 8);
}

// A frame the classifier must REJECT: plain IPv4, EtherType 0x0800.
static size_t build_ipv4(uint8_t* f) {
    memset(f, 0, 64);
    const uint8_t da[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    memcpy(f, da, 6); memcpy(f + 6, OUR_MAC, 6);
    f[12] = 0x08; f[13] = 0x00;
    for (int i = 14; i < 64; i++) f[i] = (uint8_t)i;
    return 64;
}

// The ADPDU this build MUST emit, assembled from the CSR identity group alone
// (KL_adp_engine's frame_byte_f, F04.5). available_index (wire 50..53) is left
// zero here and excluded from the compare — it is the one field that moves.
static void expected_adpdu(uint8_t* e, uint32_t talk_w, uint32_t list_w,
                           uint32_t caps_w, uint64_t gm, uint8_t dom) {
    memset(e, 0, 82);
    const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
    memcpy(e, da, 6);
    memcpy(e + 6, STA_MAC, 6);
    e[12] = 0x22; e[13] = 0xF0;
    e[14] = 0xFA;                       // subtype ADP
    e[15] = 0x00;                       // sv=0 version=0 ENTITY_AVAILABLE
    // valid_time is ADP_VALID_TIME_C inside the engine and NOT a CSR field, so
    // it is filled in by the caller from the observed frame rather than
    // asserted here; cdl is fixed at 56.
    e[17] = 56;
    put64be(e + 18, TEST_EID);
    put64be(e + 26, TEST_MODEL);
    put32be(e + 34, caps_w);
    put16be(e + 38, (uint16_t)(talk_w & 0xFFFFu));
    put16be(e + 40, (uint16_t)(talk_w >> 16));
    put16be(e + 42, (uint16_t)(list_w & 0xFFFFu));
    put16be(e + 44, (uint16_t)(list_w >> 16));
    // 46..49 controller_capabilities = 0, 50..53 available_index (excluded)
    put64be(e + 54, gm);
    e[62] = dom;
    // 63 reserved, 64..65 current_configuration, 66..67 identify_control_index,
    // 68..69 interface_index, 70..81 association_id + reserved: all zero on
    // this build (no AECP means no SET_CONFIGURATION and no IDENTIFY).
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath + the protocol processor AS the control plane ===\n");
    //! the descriptor image must be in "memory" BEFORE the first clock: the
    //! store's boot walk (header probe -> index map) starts out of reset
    build_desc_image();
    do_reset();

    // ---- A. the plane is present and its window decodes -------------------
    printf("[A] presence + CSR window\n");
    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    uint32_t stat = axi_read(A_PP_STAT);
    ck("PP_STAT tag == 0x5B (plane present)", (stat >> 24) & 0xFF, 0x5B);
    ck("PP_DIAG clean at reset", axi_read(A_PP_DIAG), 0x00000000);
    // The TX-trunk supervisor decodes, and its four unused lanes are a
    // STRUCTURAL ZERO by construction (the cascade collapsed from 8 muxes to
    // 4 when the legacy plane's five control legs were deleted), not four
    // arbiters that happen never to have locked.
    ck("TXARB_DIAG tag == 0xA7 (window decodes)",
       axi_read(A_TXARB_DIAG) >> 24, 0xA7);
    ck("TXARB_DIAG lanes 7:4 are a structural zero",
       (axi_read(A_TXARB_DIAG) >> 4) & 0xF, 0x0);

    // Provision the identity BEFORE the plane is enabled: entity_id is the
    // discriminator the talker matches a PROBE_TX against and the field the
    // ADPDU decode below rebuilds from, and the CSR resets it to zero.
    axi_write(A_MAC_ALO, STA_MAC_LO);
    axi_write(A_MAC_AHI, STA_MAC_HI);
    axi_write(A_ADP_EIDLO, (uint32_t)(TEST_EID & 0xFFFFFFFFu));
    axi_write(A_ADP_EIDHI, (uint32_t)(TEST_EID >> 32));
    axi_write(A_ADP_MDLLO, (uint32_t)(TEST_MODEL & 0xFFFFFFFFu));
    axi_write(A_ADP_MDLHI, (uint32_t)(TEST_MODEL >> 32));
    axi_write(A_ADP_CAPS,  0x0000C588u);          // a Milan PAAD's capabilities

    // ---- P. SAVED STATE: an absent backend may not report a restore -------
    // Milan v1.2 puts unconditional SHALLs on non-volatile state: 5.3.8.2
    // "The current bound state shall be saved in a non-volatile memory and
    // restored after a power cycle", 5.3.8.3 the four binding parameters,
    // 5.3.8.7 the started/stopped state, with 5.5.2.4 fixing WHEN the
    // Listener writes them. This build cannot meet them: KL_pp_shadow answers
    // the class-F device face with a blank-flash responder (reads 0xFF,
    // discards writes), so no binding survives a power cycle.
    // WHAT IS GRADED HERE IS NOT PERSISTENCE. It is that PP_STAT never
    // reports a restore that did not happen. The failure mode being closed is
    // a checklist that reads a clean restore verdict off a device with no
    // media, passes, and then fails on a bench where the power is cycled.
    // Runs BEFORE the entity enable below, which is the boot order Milan
    // 5.5.3.5.2 requires of a real restore.
    printf("[P] saved state: an absent backend must not report a restore\n");
    axi_write(A_PP_CTRL, 0x2);                       // restore_go, pre-enable
    bool p_done = false;
    for (int i = 0; i < 200 && !p_done; i++) {
        run_idle(64);
        p_done = (axi_read(A_PP_STAT) >> 2) & 1;     // STAT[2] restore_done
    }
    const uint32_t rstat = axi_read(A_PP_STAT);
    printf("  [i]    PP_STAT 0x924 = 0x%08X (backed %u blank %u alarm %u "
           "fail %u done %u)\n", rstat, (rstat >> 6) & 1, (rstat >> 7) & 1,
           (rstat >> 4) & 1, (rstat >> 3) & 1, (rstat >> 2) & 1);
    ck_true("the restore walk terminates", p_done,
            p_done ? "restore_done set" : "restore_done never set");
    // The verdict every decoder that predates the backed/blank bits computes:
    // PP_STAT has carried {alarm, fail, done} since the group was defined, so
    // a completed walk with neither flag raised IS a successful restore to
    // anything already reading this register. That is the encoding the
    // absent-backend case has to land in, rather than a new code nothing
    // downstream understands.
    const bool legacy_success = ((rstat >> 2) & 1) && !((rstat >> 3) & 1)
                                                   && !((rstat >> 4) & 1);
    ck_true("a build with NO backend does not report a successful restore",
            !legacy_success,
            legacy_success ? "PP_STAT claims a restore that never happened"
                           : "reported not-successful");
    // ...and the two bits that keep the three outcomes apart, so "no media
    // behind the port" is never confused with "media that happened to be
    // blank" nor with "a restore that genuinely put bindings back".
    ck("PP_STAT[6] nvm_backed == 0 (no persistent media behind the device face)",
       (rstat >> 6) & 1, 0u);
    ck("PP_STAT[7] nvm_blank == 1 (the walk validated zero records)",
       (rstat >> 7) & 1, 1u);
    ck("PP_STAT[3] restore_fail == 1 (an absent backend is not a success)",
       (rstat >> 3) & 1, 1u);
    ck("PP_STAT[4] nvm_alarm == 0 (nothing was committed, so nothing retried)",
       (rstat >> 4) & 1, 0u);
    ck("the presence tag is unchanged by the verdict bits",
       (rstat >> 24) & 0xFF, 0x5Bu);

    // class-D baseline, taken before the processor has ever advertised
    uint32_t aidx0 = dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w;
    axi_write(A_PP_CTRL, 0x1);                       // entity_enable
    ck("PP_CTRL reads back", axi_read(A_PP_CTRL) & 0x3, 0x1);

    // ---- E. the side port answers with the processor's own magic ----------
    printf("[E] side-port bridge -> the processor's snapshot window\n");
    bool ok = false;
    uint32_t magic = sp_read(SP_SNAPSHOT + 0, &ok);
    ck_true("side-port access completed", ok, ok ? "ack seen" : "TIMED OUT waiting on sp_busy");
    ck("snapshot[0] magic == 'KLPP'", magic, 0x4B4C5050);
    uint32_t shape = sp_read(SP_SNAPSHOT + 1, &ok);
    ck_true("snapshot[1] shape non-zero", shape != 0, shape ? "shape word present" : "read 0");

    // ---- B. a control frame reaches the processor -------------------------
    printf("[B] RX classify -> FIFO -> serializer -> the processor's validator\n");
    uint8_t f[128];
    size_t n = build_adp_discover(f);
    uint32_t before = axi_read(A_PP_DIAG) & 0xFF;
    inject_rx(f, n, 400);                            // tail: drain the serializer
    run_idle(400);
    uint32_t after = axi_read(A_PP_DIAG) & 0xFF;
    ck("ADP DISCOVER accepted (rx_frames +1)", after - before, 1);
    ck("no frame lost to a full FIFO", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);

    // ---- C. non-control traffic is rejected by the classifier -------------
    printf("[C] the filter that keeps a 1 B/clk serializer ahead of the wire\n");
    before = axi_read(A_PP_DIAG) & 0xFF;
    for (int i = 0; i < 8; i++) { n = build_ipv4(f); inject_rx(f, n, 40); }
    run_idle(400);
    after = axi_read(A_PP_DIAG) & 0xFF;
    ck("8 IPv4 frames REJECTED (rx_frames flat)", after - before, 0);
    ck("and none of them was counted as a drop", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);

    // ---- D. SUBSTITUTION: it transmits, and the wire CARRIES it ------------
    // INVERTED 2026-08-13. This used to be "shadow discipline: the MAC TX port
    // must stay SILENT". tx_drain_i is 0 now and the processor's packed TX is
    // this device's control egress, so a silent MAC over a window in which the
    // processor completed frames is the FAILURE - it means the drain is still
    // on, or the ctl_tx_mux leg is not connected, and with the legacy plane
    // deleted this device would answer nothing at all.
    //
    // MAAP is still disabled here (MAAP_CTRL.en resets to 0), so every frame
    // in this window came from the processor. The interleave case is section K.
    printf("[D] substitution — the processor transmits AND the wire carries it\n");
    const size_t tx_frames_at_d0 = tx_frames.size();
    for (int r = 0; r < 40; r++) run_idle(2000);
    uint32_t diag = axi_read(A_PP_DIAG);
    uint32_t pp_tx = (diag >> 16) & 0xFFFF;
    ck_true("the processor SENT (tx_frames > 0)", pp_tx > 0,
            pp_tx ? "its TX lanes produced frames" : "no TX attempt seen - check the time compression");
    const size_t d_frames = tx_frames.size() - tx_frames_at_d0;
    char ddet[96];
    snprintf(ddet, sizeof ddet, "%zu frame(s) egressed at the MAC boundary", d_frames);
    ck_true("MAC TX CARRIED them (the drain is off)", d_frames > 0, ddet);
    // ...and every one of them was the processor's, because nothing else on
    // this build can reach the control lane yet.
    {
        long foreign = 0;
        for (size_t i = tx_frames_at_d0; i < tx_frames.size(); i++) {
            const FrClass c = classify(tx_frames[i]);
            if (c == FR_ALIEN || c == FR_SHORT || c == FR_MAAP) foreign++;
        }
        ck("every frame in the window was a processor control PDU",
           (uint32_t)foreign, 0u);
    }

    // ---- G. the class-D fabric face is REACHABLE and LIVE ------------------
    // A port that is only ever read at reset proves a wire exists, nothing
    // more. adp_next_avail_index_o is the class-D level with an engine behind
    // it that moves on its own: KL_adp_engine publishes the PRE-increment
    // index, so it reads 0 before the first ENTITY_AVAILABLE and counts up
    // with every advertisement the compressed cadence fires.
    //
    // The wait below is not padding. Milan 5.6.3.5.2 makes the first
    // advertisement wait T-ADP-DELAY-START, a PRNG draw of 0..2000 ms, so at
    // this suite's compressed millisecond (100 clk) the engine can legitimately
    // sit in ADP_ADV_DELAY for 200,000 cycles. Poll instead of guessing a cycle
    // count, and keep it bounded so a real stall still fails instead of hanging.
    printf("[G] class-D fabric face — reachable, and it MOVES\n");
    ck("adp_next_avail_index read 0 before any advertisement", aidx0, 0u);
    uint32_t aidx1 = dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w;
    for (int r = 0; r < 200 && aidx1 == aidx0; r++) {
        run_idle(2000);
        aidx1 = dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w;
    }
    ck_true("adp_next_avail_index CHANGED (the engine drives it)", aidx1 > aidx0,
            aidx1 > aidx0 ? "index advanced with the first ENTITY_AVAILABLE"
                          : "STILL 0 - the class-D net is not connected to the engine");

    // ---- F. the ADP advertisement, DECODED at the MAC boundary -------------
    // A frame count is weak evidence. This rebuilds the whole 82-byte ADPDU
    // from the CSR identity group and compares it against the wire byte for
    // byte, so an engine that egressed a plausible-looking runt, or a control
    // lane that spliced a MAAP beat into it, fails here.
    printf("[F] the ENTITY_AVAILABLE the processor emits, decoded byte-exact\n");
    {
        const uint32_t talk_w = axi_read(A_ADP_TALK);
        const uint32_t list_w = axi_read(A_ADP_LIST);
        const uint32_t caps_w = axi_read(A_ADP_CAPS);
        const uint64_t gm = ((uint64_t)axi_read(A_ADP_GMHI) << 32)
                          | axi_read(A_ADP_GMLO);
        const uint8_t  dom = (uint8_t)(axi_read(A_ADP_GDOM) & 0xFF);

        std::vector<size_t> adp_idx;
        for (size_t i = 0; i < tx_frames.size(); i++)
            if (classify(tx_frames[i]) == FR_ADP) adp_idx.push_back(i);

        char det[128];
        snprintf(det, sizeof det, "%zu ADPDU(s) at the MAC boundary of %zu frames",
                 adp_idx.size(), tx_frames.size());
        ck_true("an ADP frame reached the MAC TX boundary", !adp_idx.empty(), det);

        if (!adp_idx.empty()) {
            const TxFrame& a = tx_frames[adp_idx.front()];
            ck("ADPDU is 82 octets on the wire", (uint32_t)a.bytes.size(), 82u);
            ck("ADPDU DA == 91:E0:F0:01:00:00",
               (uint32_t)get_be(a.bytes, 0, 4), 0x91E0F001u);
            ck("ADPDU EtherType 0x22F0 + subtype 0xFA",
               (uint32_t)get_be(a.bytes, 12, 3), 0x22F0FAu);
            ck("ADPDU sv=0 version=0 message_type=ENTITY_AVAILABLE",
               a.bytes.size() > 15 ? a.bytes[15] : 0xFFu, 0x00u);
            ck("ADPDU control_data_length == 56",
               (uint32_t)((((unsigned)a.bytes[16] & 7) << 8) | a.bytes[17]), 56u);
            ck("ADPDU entity_id == the 0x604/0x608 pair",
               (uint32_t)get_be(a.bytes, 18, 4), (uint32_t)(TEST_EID >> 32));
            ck("ADPDU entity_id low half",
               (uint32_t)get_be(a.bytes, 22, 4), (uint32_t)(TEST_EID & 0xFFFFFFFFu));
            ck("ADPDU entity_model_id == the 0x60C/0x610 pair",
               (uint32_t)get_be(a.bytes, 26, 4), (uint32_t)(TEST_MODEL >> 32));
            // The advertised SHAPE against the same numbers milan_csr serves at
            // 0x618/0x61C over a different path. A shape that reaches one and
            // not the other is the 2026-07-27 silicon defect (a boot script
            // frozen at 1x1 while the 8x8 board advertised the wrong count).
            // This law used to be graded in milan_dp; the advertiser there is
            // the processor now and its cadence is unreachable at real-time
            // clocking, so the check lives HERE, where time is compressed.
            ck("ADPDU talker_stream_sources == 0x618",
               (uint32_t)get_be(a.bytes, 38, 2), talk_w & 0xFFFFu);
            ck("ADPDU talker_capabilities == 0x618",
               (uint32_t)get_be(a.bytes, 40, 2), talk_w >> 16);
            ck("ADPDU listener_stream_sinks == 0x61C",
               (uint32_t)get_be(a.bytes, 42, 2), list_w & 0xFFFFu);
            ck("ADPDU listener_capabilities == 0x61C",
               (uint32_t)get_be(a.bytes, 44, 2), list_w >> 16);

            // ...and now the WHOLE frame, byte for byte. valid_time (byte 16's
            // top five bits) is the engine's own constant rather than a CSR
            // field, so it is copied from the observed frame; available_index
            // (50..53) is the one moving field and is graded on its own below.
            uint8_t exp[82];
            expected_adpdu(exp, talk_w, list_w, caps_w, gm, dom);
            exp[16] = (uint8_t)((a.bytes[16] & 0xF8) | ((56 >> 8) & 0x7));
            memcpy(exp + 50, &a.bytes[50], 4);
            long diffs = 0; int firstdiff = -1;
            for (size_t i = 0; i < 82 && i < a.bytes.size(); i++)
                if (a.bytes[i] != exp[i]) { diffs++; if (firstdiff < 0) firstdiff = (int)i; }
            char bdet[128];
            snprintf(bdet, sizeof bdet,
                     "%ld differing octet(s); first at wire byte %d", diffs, firstdiff);
            ck_true("ADPDU is byte-exact against the CSR identity group",
                    diffs == 0 && a.bytes.size() == 82, bdet);

            // available_index: strictly increasing across the advertisements
            // that egressed, and the class-D face agrees with the wire.
            long nonmono = 0; uint32_t prev = 0; bool first = true;
            for (size_t k : adp_idx) {
                const uint32_t ai = (uint32_t)get_be(tx_frames[k].bytes, 50, 4);
                if (!first && ai <= prev) nonmono++;
                prev = ai; first = false;
            }
            ck("available_index strictly increases across ADPDUs",
               (uint32_t)nonmono, 0u);
            ck_true("class-D available_index >= the last one on the wire",
                    dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w >= prev,
                    "the published index tracks the wire");
        }
    }

    // ---- H. the MAAP adapter REFUSES SAFELY (no block claimed yet) ---------
    // MAAP_CTRL.en is 0 out of reset, so KL_maap holds no block and the shim
    // can grant nothing. The processor must be told so — and told PROMPTLY —
    // rather than left with a stuck allocator-busy flag.
    printf("[H] maap adapter with NO allocator: refuse, never wedge\n");
    ck("KL_maap holds no block (MAAP_STAT1.addr_valid = 0)",
       (axi_read(A_MAAP_STAT1) >> 2) & 1u, 0u);
    MaapObs h0 = mo;
    uint8_t pf[128];
    size_t pn = build_probe_tx(pf, TEST_EID, 0);
    uint32_t rxf0 = axi_read(A_PP_DIAG) & 0xFF;
    inject_rx(pf, pn, 400);
    run_idle(4000);
    uint32_t rxf1 = axi_read(A_PP_DIAG) & 0xFF;
    long h_acc = mo.accepted - h0.accepted;
    long h_ans = mo.answered - h0.answered;
    long h_gr  = mo.granted  - h0.granted;
    ck_true("the processor ASKED and the shim ACCEPTED", h_acc > 0,
            h_acc ? "ALLOC_DA taken" : "no request seen - is a source enabled?");
    ck_true("every accepted request was ANSWERED", h_acc == h_ans,
            h_acc == h_ans ? "accepted == answered"
                           : "an accepted request went unanswered - allocator-busy STICKS");
    ck("and every answer refused (ok = 0)", (uint32_t)h_gr, 0u);
    ck("the DA gate stayed SHUT (acmp_declaring = 0)",
       dut->rootp->milan_datapath__DOT__pp_cd_acmp_declaring_w & 1u, 0u);
    ck("the ACMP PROBE_TX still reached the processor", rxf1 - rxf0, 1u);
    bool okh = false;
    ck("the plane KEEPS SERVING (side port still answers 'KLPP')",
       sp_read(SP_SNAPSHOT + 0, &okh), 0x4B4C5050);
    // ...and the refusal is VISIBLE ON THE WIRE: a PROBE_TX against a source
    // that holds no destination address is answered TALKER_DEST_MAC_FAILED(3),
    // not SUCCESS. This is the honest answer, and it is the answer milan_dp
    // now records too (MAAP cannot reach ANNOUNCE at real-time clocking).
    {
        int found = -1;
        for (size_t i = tx_frames.size(); i-- > 0; )
            if (classify(tx_frames[i]) == FR_ACMP
                && tx_frames[i].bytes.size() >= 18
                && (tx_frames[i].bytes[15] & 0xF) == 1) { found = (int)i; break; }
        ck_true("a CONNECT_TX_RESPONSE came back", found >= 0,
                found >= 0 ? "response on the wire" : "no ACMP response egressed");
        if (found >= 0)
            ck("...with status TALKER_DEST_MAC_FAILED(3) — no DA to hand out",
               (tx_frames[found].bytes[16] >> 3) & 0x1F, 3u);
    }

    // ---- I. the MAAP adapter GRANTS, and the DA gate OPENS -----------------
    // Enable KL_maap and let it walk IDLE -> 3x PROBE -> ANNOUNCE. From here
    // on the FABRIC's own MAAP engine transmits too, which is what makes the
    // shared-lane section K possible at all.
    printf("[I] maap adapter with a claimed block: grant + DA gate\n");
    axi_write(A_MAAP_CTRL, 0x00000801);              // count = 8, en = 1
    bool announced = false;
    for (int r = 0; r < 200 && !announced; r++) {
        run_idle(2000);
        announced = ((axi_read(A_MAAP_STAT1) >> 2) & 1u) != 0;
    }
    ck_true("KL_maap reached ANNOUNCE (a block is claimed)", announced,
            announced ? "addr_valid asserted" : "TIMED OUT - check MAAP_CLK_HZ_P");
    uint32_t maap_off = axi_read(A_MAAP_STAT0) & 0xFFFF;

    MaapObs i0 = mo;
    pn = build_probe_tx(pf, TEST_EID, 0);
    inject_rx(pf, pn, 400);
    run_idle(8000);
    long i_acc = mo.accepted - i0.accepted;
    long i_ans = mo.answered - i0.answered;
    long i_gr  = mo.granted  - i0.granted;
    ck_true("the shim GRANTED an address", i_gr > 0,
            i_gr ? "ok = 1 returned" : "still refusing with a claimed block");
    ck_true("every accepted request was ANSWERED", i_acc == i_ans,
            i_acc == i_ans ? "accepted == answered" : "an accepted request went unanswered");
    // source 0 maps onto block offset 0 — the same base+index rule the fabric
    // already uses for its own per-stream DMACs.
    ck_true("granted DA == KL_maap base + source index",
            mo.last_da == (MAAP_POOL_BASE | (uint64_t)((maap_off + 0) & 0xFFFF)),
            mo.last_da == (MAAP_POOL_BASE | (uint64_t)((maap_off + 0) & 0xFFFF))
                ? "matches MAAP_STAT0's offset" : "address disagrees with the engine");
    ck("the per-source DA GATE is OPEN (acmp_declaring = 1)",
       dut->rootp->milan_datapath__DOT__pp_cd_acmp_declaring_w & 1u, 1u);
    ck_true("and it was held, not a one-cycle blip", mo.declaring_cycles > 100,
            mo.declaring_cycles > 100 ? "gate held" : "gate did not hold");
    // the SUCCESS half of the PROBE_TX answer, which section H could not see:
    // with a DA in hand the talker answers SUCCESS and names the stream_id
    // milan_datapath derives for source 0, {station MAC, uid}.
    //
    // THE THIRD PROBE, NOT THE SECOND. The allocation is asynchronous to the
    // answer: a probe against a source in GS_NO_DA issues the ALLOC_DA and is
    // answered TALKER_DEST_MAC_FAILED in the same walk, because the walker
    // must not park waiting for the allocator (KL_pp_maap_shim's decision 1).
    // So the probe that TRIGGERS the grant still gets a refusal, and the first
    // SUCCESS is the next one. Grading the triggering probe would have been
    // grading the race.
    {
        const size_t frames_before_p3 = tx_frames.size();
        pn = build_probe_tx(pf, TEST_EID, 0);
        inject_rx(pf, pn, 400);
        run_idle(8000);
        int found = -1;
        for (size_t i = tx_frames.size(); i-- > frames_before_p3; )
            if (classify(tx_frames[i]) == FR_ACMP
                && tx_frames[i].bytes.size() >= 62
                && (tx_frames[i].bytes[15] & 0xF) == 1) { found = (int)i; break; }
        ck_true("a CONNECT_TX_RESPONSE came back with a block claimed", found >= 0,
                found >= 0 ? "response on the wire" : "no ACMP response egressed");
        if (found >= 0) {
            const std::vector<uint8_t>& b = tx_frames[found].bytes;
            ck("PROBE_TX now answers SUCCESS", (b[16] >> 3) & 0x1F, 0u);
            ck("...naming stream_id {station MAC, uid 0} high half",
               (uint32_t)get_be(b, 18, 4), 0x02000000u);
            ck("...and its low half", (uint32_t)get_be(b, 22, 4), 0x00010000u);
            ck("...with stream_dest_mac = the granted DA (high half)",
               (uint32_t)get_be(b, 54, 4), 0x91E0F000u);
            ck("...and its low half = base offset + 0",
               (uint32_t)get_be(b, 58, 2), maap_off & 0xFFFFu);
        }
    }

    // ---- L. THE DEVICE ANSWERS AECP ---------------------------------------
    // "No AECP" was true of the first substitution build and is DEAD as a
    // premise: the processor carries a µCPU (KL_aecp_ucpu) running the
    // hdl/aecp/ucode image against KL_aecp_desc_store, and the entity model
    // it serves lives in the integrator's memory behind the nine desc_mem
    // ports this harness now backs.
    //
    // EVERY CHECK BELOW DECODES THE RESPONSE FRAME. A counter that moved
    // cannot tell a conformant AECPDU from a runt, and this is exactly the
    // place where the difference matters: a controller (Hive, la_avdecc)
    // enumerates by READ_DESCRIPTOR and gives up on the first malformed or
    // missing answer.
    //
    // The wire layout being graded (IEEE 1722.1-2021 9.2.1 + F06.14's
    // offset-from-@12 control_data_length):
    //   14        Ethernet, DA = the requester's SA, SA = the station MAC
    //   +0  0xFB  subtype AECP
    //   +1        sv/version/message_type — the COMMAND's type + 1
    //   +2..3     status[4:0] then control_data_length[10:0] = 12 + payload
    //   +4..11    target_entity_id  = ours
    //   +12..19   controller_entity_id = the command's, echoed
    //   +20..21   sequence_id, echoed
    //   +22..23   u=0 + command_type, echoed
    //   +24..     payload
    printf("[L] AECP: the device ANSWERS — decoded, not counted\n");
    {
        // helper: the newest AECP frame at the MAC boundary past `from`
        auto last_aecp = [&](size_t from) -> int {
            for (size_t i = tx_frames.size(); i-- > from; )
                if (classify(tx_frames[i]) == FR_AECP) return (int)i;
            return -1;
        };
        // helper: the fields every response shares, graded once per case
        auto grade_common = [&](const std::vector<uint8_t>& b, const char* tag,
                                uint16_t opcode, uint16_t seq, uint8_t mt) {
            char w[96];
            snprintf(w, sizeof w, "%s: message_type = command + 1", tag);
            ck(w, b[15] & 0x0F, mt);
            snprintf(w, sizeof w, "%s: sv/version nibble is zero", tag);
            ck(w, (b[15] >> 4) & 0x0F, 0u);
            snprintf(w, sizeof w, "%s: target_entity_id is OURS", tag);
            ck(w, (uint32_t)get_be(b, 18, 4), (uint32_t)(TEST_EID >> 32));
            snprintf(w, sizeof w, "%s: controller_entity_id echoed", tag);
            ck(w, (uint32_t)get_be(b, 26, 4), (uint32_t)(CTLR_EID >> 32));
            snprintf(w, sizeof w, "%s: sequence_id echoed", tag);
            ck(w, (uint32_t)get_be(b, 34, 2), seq);
            snprintf(w, sizeof w, "%s: command_type echoed, u = 0", tag);
            ck(w, (uint32_t)get_be(b, 36, 2), opcode);
            snprintf(w, sizeof w, "%s: unicast back to the requester", tag);
            ck(w, (uint32_t)get_be(b, 0, 4),
               (uint32_t)((CTLR_MAC[0] << 24) | (CTLR_MAC[1] << 16)
                          | (CTLR_MAC[2] << 8) | CTLR_MAC[3]));
            snprintf(w, sizeof w, "%s: source address is the station MAC", tag);
            ck(w, (uint32_t)get_be(b, 6, 4),
               (uint32_t)((STA_MAC[0] << 24) | (STA_MAC[1] << 16)
                          | (STA_MAC[2] << 8) | STA_MAC[3]));
        };
        // helper: cdl vs the frame's real length, the malformed-frame trap
        auto grade_len = [&](const std::vector<uint8_t>& b, const char* tag,
                             size_t pld) {
            char w[96];
            size_t want = 38 + pld; if (want < 60) want = 60;
            snprintf(w, sizeof w, "%s: control_data_length = 12 + payload", tag);
            ck(w, (uint32_t)((((unsigned)b[16] & 7) << 8) | b[17]),
               (uint32_t)(12 + pld));
            snprintf(w, sizeof w, "%s: frame length matches (60-octet min)", tag);
            ck(w, (uint32_t)b.size(), (uint32_t)want);
        };

        uint8_t cf[128];
        size_t  cn;

        // --- L1. READ_DESCRIPTOR that HITS: SUCCESS + the descriptor -------
        // The store must have validated the image out of reset (magic +
        // layout version + checksum) and walked the index map, or this comes
        // back NO_SUCH_DESCRIPTOR — which is why mem_reqs is graded too: a
        // model that never got asked is a model that proved nothing.
        ck_true("the store FETCHED from descriptor memory", mem_reqs > 0,
                mem_reqs ? "bursts served" : "no memory request ever issued");
        // ...and it ACCEPTED the image. protocol_processor_top publishes the
        // store's verdict in snapshot word 34:
        //   [0] img_valid, [4:1] fault (1 magic, 2 version, 3 checksum,
        //   4 n_entries, 5 n_names, 6 desc_max_len, 7 mem err, 8 timeout),
        //   [9:5] the last response's status, [20:10] its AECPDU length.
        // Reading it here means a rejected image is diagnosed rather than
        // showing up only as an unexplained BAD_ARGUMENTS three checks later.
        {
            bool spok = false;
            const uint32_t w34 = sp_read(SP_SNAPSHOT + 34, &spok);
            printf("  [i]    desc-store word34 = 0x%08X (%ld burst(s))\n",
                   w34, mem_reqs);
            ck("the descriptor image VALIDATED (magic+version+checksum)",
               w34 & 1u, 1u);
            ck("...with no header fault", (w34 >> 1) & 0xFu, 0u);
        }
        {
            size_t at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0101);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L1 READ_DESCRIPTOR(ENTITY,0) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE - no response frame");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_common(b, "L1", 0x0004, 0x0101, 1);
                grade_len(b, "L1", 4 + ENT_LEN_C);
                ck("L1: status SUCCESS(0)", (b[16] >> 3) & 0x1F, 0u);
                ck("L1: configuration_index @24 echoed",
                   (uint32_t)get_be(b, 38, 2), 0u);
                ck("L1: reserved @26 is zero", (uint32_t)get_be(b, 40, 2), 0u);
                // the descriptor itself, byte for byte against the image
                auto want = desc_bytes(DTY_ENTITY_C, 0);
                long bad = 0;
                for (size_t i = 0; i < want.size(); i++)
                    if (42 + i >= b.size() || b[42 + i] != want[i]) bad++;
                ck("L1: the DESCRIPTOR bytes @28 are the image's, exactly",
                   (uint32_t)bad, 0u);
            }
        }

        // --- L2. the SAME type at index 1: proves the stride arithmetic ----
        {
            size_t at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_CONFIG_C, 1, 0x0102);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L2 READ_DESCRIPTOR(CONFIGURATION,1) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_len(b, "L2", 4 + CFG_LEN_C);
                ck("L2: status SUCCESS(0)", (b[16] >> 3) & 0x1F, 0u);
                auto want = desc_bytes(DTY_CONFIG_C, 1);
                long bad = 0;
                for (size_t i = 0; i < want.size(); i++)
                    if (42 + i >= b.size() || b[42 + i] != want[i]) bad++;
                ck("L2: index 1 served at elem_off + 1*elem_stride",
                   (uint32_t)bad, 0u);
                ck("L2: ...and it is NOT index 0's descriptor",
                   (uint32_t)get_be(b, 44, 2), 1u);   // descriptor_index field
            }
        }

        // --- L3. a locate MISS: NO_SUCH_DESCRIPTOR + the §7.4.5 stub -------
        // The type AND the index are both NON-ZERO on purpose: a stub check
        // against {0, 0} would be satisfied by the zero padding of a frame
        // that never wrote a stub at all.
        {
            size_t at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_ABSENT_C, 7, 0x0103);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L3 READ_DESCRIPTOR(absent type) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_common(b, "L3", 0x0004, 0x0103, 1);
                grade_len(b, "L3", 8);          // cfg + reserved + the 4 B stub
                ck("L3: status NO_SUCH_DESCRIPTOR(2)",
                   (b[16] >> 3) & 0x1F, 2u);
                ck("L3: the IEEE 7.4.5 stub names the descriptor_type",
                   (uint32_t)get_be(b, 42, 2), DTY_ABSENT_C);
                ck("L3: ...and the descriptor_index",
                   (uint32_t)get_be(b, 44, 2), 7u);
            }
        }

        // --- L4. a bad configuration_index: BAD_ARGUMENTS, not a miss ------
        // The µprogram range-checks against configurations_count out of the
        // store's region 0xD before it ever locates, so the two failures stay
        // distinguishable — which is what a controller needs to tell "wrong
        // configuration" from "no such descriptor".
        {
            size_t at = tx_frames.size();
            // again a non-zero {type, index}, and a type that EXISTS in the
            // image: the only thing wrong with this command is the
            // configuration index, so a BAD_ARGUMENTS here cannot be a
            // mislabelled locate miss.
            cn = build_read_desc(cf, 5, DTY_CONFIG_C, 1, 0x0104);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L4 READ_DESCRIPTOR(bad config) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_len(b, "L4", 8);
                ck("L4: status BAD_ARGUMENTS(7), NOT NO_SUCH_DESCRIPTOR",
                   (b[16] >> 3) & 0x1F, 7u);
                ck("L4: the stub still names the type", (uint32_t)get_be(b, 42, 2),
                   DTY_CONFIG_C);
                ck("L4: ...and the index", (uint32_t)get_be(b, 44, 2), 1u);
                ck("L4: configuration_index @24 is the BAD one, echoed",
                   (uint32_t)get_be(b, 38, 2), 5u);
            }
        }

        // --- L5. an unimplemented opcode: a CONFORMANT NOT_IMPLEMENTED -----
        // IEEE 1722.1 9.3.5.3.3 / F06.14 "echo command": the command comes
        // back with message_type + 1, status NOT_IMPLEMENTED, its OWN payload
        // copied through and its own length declared. Never silence, never a
        // malformed frame.
        //
        // THE OPCODE IS UNASSIGNED ON PURPOSE. This arm used to send 0x0029
        // GET_COUNTERS, under a comment calling it "a Milan-mandatory opcode
        // this build does not serve". The processor now serves it for real
        // (L5b below), and these four checks went red the moment it did: an
        // exemplar chosen because a feature was MISSING expires when the
        // feature lands, and it expires as a test failure rather than as a
        // note. 0x7FFE is outside 1722.1-2021 Table 7-140's assigned range,
        // so nothing can ever implement it and this arm grades the echo law
        // itself for as long as the law stands.
        {
            uint8_t pl[8] = {0x00, 0x05, 0x00, 0x00, 0xDE, 0xAD, 0xBE, 0xEF};
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x7FFE, 0x0105, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L5 an unassigned opcode was ANSWERED, not dropped",
                    k >= 0, k >= 0 ? "an AECPDU egressed"
                                   : "SILENCE - an unimplemented opcode must ECHO");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_common(b, "L5", 0x7FFE, 0x0105, 1);
                grade_len(b, "L5", sizeof pl);
                ck("L5: status NOT_IMPLEMENTED(1)", (b[16] >> 3) & 0x1F, 1u);
                long bad = 0;
                for (size_t i = 0; i < sizeof pl; i++)
                    if (38 + i >= b.size() || b[38 + i] != pl[i]) bad++;
                ck("L5: the command's payload is ECHOED back", (uint32_t)bad, 0u);
            }
        }

        // --- L5b. GET_COUNTERS answered for real, through the wired face ---
        // IEEE 1722.1-2021 7.4.42.2 response payload: descriptor_type @0,
        // descriptor_index @2, counters_valid @4, then THIRTY-TWO quadlets of
        // counters_block @8. Payload byte 0 is frame byte 38, so the mask is
        // at 42 and the block runs 46..173.
        //
        // WHAT THIS SECTION IS FOR. The processor lays the block out; THIS
        // repository decides what the numbers mean, by driving ctr_data_i
        // from KL_avtp_rx_monitor_ctx (milan_datapath's Table 7-157 mux).
        // Those six ports were briefly left unconnected, on the reasoning
        // that an unwired face answers zero with an empty mask and is
        // therefore safe. It is not available as a choice here - this suite
        // is warnings-are-errors, so six unconnected pins are six fatal
        // PINMISSING - and the checks below exist so the WIRING is graded and
        // not just the elaboration.
        const size_t CTR_PLD_C = 2 + 2 + 4 + 128;     // 136, 7.4.42.2
        {
            // descriptor_type STREAM_INPUT (Table 7-4 0x0005), index 0: the
            // one sink this 1x1 shape elaborates.
            uint8_t pl[4] = {0x00, 0x05, 0x00, 0x00};
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x0029, 0x0130, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L5b GET_COUNTERS(STREAM_INPUT 0) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_common(b, "L5b", 0x0029, 0x0130, 1);
                grade_len(b, "L5b", CTR_PLD_C);
                ck("L5b: status SUCCESS(0), not NOT_IMPLEMENTED",
                   (b[16] >> 3) & 0x1F, 0u);
                ck("L5b: descriptor_type echoed @0", (uint32_t)get_be(b, 38, 2),
                   0x0005u);
                ck("L5b: descriptor_index echoed @2",
                   (uint32_t)get_be(b, 40, 2), 0u);
                // 0xFFF = quadlets 0..11, every counter Table 7-157 defines
                // for a STREAM_INPUT before the reserved span at offset 48.
                // Table 7-156 numbers MEDIA_LOCKED bit #31 at offset 0 and
                // TIMESTAMP_VALID bit #25 at offset 24, so the mask bit for
                // quadlet n is bit n of a conventional LSB-0 word.
                ck("L5b: counters_valid @4 is the twelve we keep (0xFFF)",
                   (uint32_t)get_be(b, 42, 4), 0x0000'0FFFu);
                // Table 7-157 reserves offsets 48..92 and gives 96.. to the
                // ENTITY_SPECIFIC set. This build claims none of them, and a
                // claimed-zero is the lie this face exists to prevent, so
                // they must be BOTH unclaimed in the mask and zero in the
                // block. The mask check above covers the first half.
                long dirty = 0;
                for (int q = 12; q < 32; q++)
                    if (get_be(b, 46 + 4 * (size_t)q, 4) != 0) dirty++;
                ck("L5b: the unclaimed quadlets 12..31 are zero",
                   (uint32_t)dirty, 0u);
                ck_true("L5b: the block is a full 32 quadlets",
                        b.size() == 46 + 128, "the frame ends at 174");
            }
        }
        {
            // THE WRONG-OBJECT GUARD. milan_datapath narrows the descriptor
            // index to the monitor's four-bit diag_idx_i, and the monitor
            // CLAMPS an out-of-range value to context 0. Driven unguarded,
            // a GET_COUNTERS for a Stream Input this shape does not have
            // would come back with SINK 0's counters under a full mask -
            // the right shape, the wrong object, and nothing on the wire to
            // say so. There is no NO_SUCH_DESCRIPTOR arm on this face, so
            // the honest answer is an EMPTY mask over a zero block.
            uint8_t pl[4] = {0x00, 0x05, 0x00, 0x09};   // STREAM_INPUT 9
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x0029, 0x0131, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L5c GET_COUNTERS(STREAM_INPUT 9) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_len(b, "L5c", CTR_PLD_C);
                ck("L5c: descriptor_index 9 echoed, not clamped to 0",
                   (uint32_t)get_be(b, 40, 2), 9u);
                ck("L5c: counters_valid is EMPTY - no such sink here",
                   (uint32_t)get_be(b, 42, 4), 0u);
                long dirty = 0;
                for (int q = 0; q < 32; q++)
                    if (get_be(b, 46 + 4 * (size_t)q, 4) != 0) dirty++;
                ck("L5c: ...and the block is all zeros, not sink 0's numbers",
                   (uint32_t)dirty, 0u);
            }
        }
        {
            // THE PADDED-COMMAND GUARD, and it is the engine's, not this
            // repository's. KL_aecp_engine walks the AECPDU into ONE pair of
            // registers for two incompatible payload shapes: 7.4.42.1 puts
            // GET_COUNTERS' {descriptor_type, descriptor_index} at @24 and
            // @26 and stops, while 7.4.5.1 puts READ_DESCRIPTOR's at @28 and
            // @30. Walk arms 6..9 therefore carry `if (!ctrs_r)`, under a
            // comment that says guarding both directions matters.
            //
            // Nothing exercised it. A GET_COUNTERS whose payload stops at
            // four octets never reaches @28, so the guard could be deleted
            // with every suite still green. This command is eight octets and
            // its tail is shaped like a READ_DESCRIPTOR for a DIFFERENT
            // object: without the guard the engine would answer about ENTITY
            // 9 while the controller asked about Stream Input 0, and the mask
            // would collapse to empty on the way past.
            uint8_t pl[8] = {0x00, 0x05,   // @24 descriptor_type STREAM_INPUT
                             0x00, 0x00,   // @26 descriptor_index 0
                             0x00, 0x00,   // @28 = READ_DESCRIPTOR's type
                             0x00, 0x09};  // @30 = READ_DESCRIPTOR's index
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x0029, 0x0133, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L5e a PADDED GET_COUNTERS was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_len(b, "L5e", CTR_PLD_C);
                ck("L5e: the type is @24's, NOT the padding at @28",
                   (uint32_t)get_be(b, 38, 2), 0x0005u);
                ck("L5e: the index is @26's, NOT the padding at @30",
                   (uint32_t)get_be(b, 40, 2), 0u);
                ck("L5e: ...so the mask is still Stream Input 0's",
                   (uint32_t)get_be(b, 42, 4), 0x0000'0FFFu);
            }
        }
        {
            // THE WRONG-TYPE GUARD, same term in the RTL. ENTITY counters are
            // Table 7-155's ENTITY_SPECIFIC_1..8; this build keeps none, so
            // the mask must be empty. A build that answered STREAM_INPUT's
            // numbers here would be claiming counters for the wrong object
            // class entirely.
            uint8_t pl[4] = {0x00, 0x00, 0x00, 0x00};   // ENTITY 0
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x0029, 0x0132, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L5d GET_COUNTERS(ENTITY) was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_len(b, "L5d", CTR_PLD_C);
                ck("L5d: descriptor_type ENTITY echoed",
                   (uint32_t)get_be(b, 38, 2), 0u);
                ck("L5d: counters_valid is EMPTY - no ENTITY counters here",
                   (uint32_t)get_be(b, 42, 4), 0u);
                long dirty = 0;
                for (int q = 0; q < 32; q++)
                    if (get_be(b, 46 + 4 * (size_t)q, 4) != 0) dirty++;
                ck("L5d: ...and the block is all zeros", (uint32_t)dirty, 0u);
            }
        }

        // --- L6. IDENTIFY_NOTIFICATION as a COMMAND: BAD_ARGUMENTS ---------
        // IEEE 1722.1 7.4.39.2 makes 0x0026 a NOTIFICATION only; sent as a
        // command it is BAD_ARGUMENTS, and that opcode-specific rule beats
        // 9.3.5.3.3's NOT_IMPLEMENTED fallback. The two statuses are the
        // whole point of the check: a build that answered NOT_IMPLEMENTED
        // here would be applying the general rule to a specified case.
        {
            uint8_t pl[4] = {0x00, 0x01, 0x00, 0x00};
            size_t at = tx_frames.size();
            cn = build_aecp(cf, 0, TEST_EID, 0x0026, 0x0106, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L6 IDENTIFY_NOTIFICATION-as-command was ANSWERED", k >= 0,
                    k >= 0 ? "an AECPDU egressed" : "SILENCE");
            if (k >= 0) {
                const std::vector<uint8_t>& b = tx_frames[k].bytes;
                grade_common(b, "L6", 0x0026, 0x0106, 1);
                grade_len(b, "L6", sizeof pl);
                ck("L6: status BAD_ARGUMENTS(7) — 7.4.39.2 beats 9.3.5.3.3",
                   (b[16] >> 3) & 0x1F, 7u);
            }
        }

        // --- L7. SILENT REFUSAL, and only where the standard allows it -----
        // Two inputs get no reply at all: a command aimed at somebody else's
        // entity_id, and an AECP RESPONSE arriving as input (answering a
        // response is how a control plane builds a storm). Both must leave
        // the plane SERVING — the follow-up command below is what separates
        // "correctly ignored" from "wedged".
        {
            size_t at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0107);
            put64be(cf + 18, TEST_EID ^ 0xFFull);        // somebody else
            inject_rx(cf, cn, 400);
            run_idle(20000);
            ck("L7a: a command for ANOTHER entity gets no reply",
               (uint32_t)(last_aecp(at) >= 0 ? 1 : 0), 0u);

            at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0108);
            cf[15] = 0x01;                               // AEM_RESPONSE as input
            inject_rx(cf, cn, 400);
            run_idle(20000);
            ck("L7b: an AECP RESPONSE arriving as input gets no reply",
               (uint32_t)(last_aecp(at) >= 0 ? 1 : 0), 0u);

            at = tx_frames.size();
            cn = build_read_desc(cf, 0, DTY_CONFIG_C, 0, 0x0109);
            inject_rx(cf, cn, 400);
            run_idle(20000);
            int k = last_aecp(at);
            ck_true("L7c: ...and the AECP plane is still SERVING after both",
                    k >= 0 && (tx_frames[k].bytes[16] >> 3) == 0,
                    k >= 0 ? "a following command answered SUCCESS"
                           : "the plane went silent - it was WEDGED, not refusing");
        }

        // KNOWN GAP, RECORDED NOT CLAIMED: Milan Δ7 wants ACQUIRE_ENTITY
        // (0x0000) answered NOT_SUPPORTED with owner_id = 0. gen_ucode.py
        // carries an E_ACQ exemplar for exactly that, but KL_aecp_engine's
        // three-arm decode does not dispatch to it, so 0x0000 currently takes
        // the generic NOT_IMPLEMENTED echo. That is a conformant answer to a
        // controller and NOT a defect in this harness; it is simply not the
        // Milan answer, and nothing here should be read as proving it.
        printf("  [GAP]  Milan D7 ACQUIRE_ENTITY (NOT_SUPPORTED, owner_id=0) is "
               "NOT distinguished from the generic NOT_IMPLEMENTED echo: "
               "KL_aecp_engine decodes 0x0004 and 0x0026 only. Ungraded here "
               "on purpose.\n");
    }

    // ---- M. NO DESCRIPTOR MEMORY: the DOCUMENTED degrade path --------------
    // An integration that offers the store nothing must not hang the µCPU.
    // KL_aecp_desc_store's watchdog abandons the burst, the image goes
    // invalid, and READ_DESCRIPTOR degrades to a well-formed
    // NO_SUCH_DESCRIPTOR. This is driven DELIBERATELY - the harness stops
    // answering - rather than being what a forgotten tie-off happens to do.
    printf("[M] descriptor memory withdrawn: degrade, never wedge\n");
    {
        mem_answering = false;
        // MEM_TIMEOUT_CYC_P defaults to 4096; the locate re-arms the header
        // probe every time, so one command pays one watchdog.
        uint8_t cf[128];
        size_t at = tx_frames.size();
        size_t cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0201);
        inject_rx(cf, cn, 400);
        for (int r = 0; r < 8; r++) run_idle(20000);
        int k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = (int)i; break; }
        ck_true("M: with no memory, READ_DESCRIPTOR still gets an ANSWER",
                k >= 0, k >= 0 ? "the watchdog degraded cleanly"
                               : "the uCPU HUNG on an absent bridge");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("M: status NO_SUCH_DESCRIPTOR(2)", (b[16] >> 3) & 0x1F, 2u);
            ck("M: control_data_length = 12 + the 8-byte stub payload",
               (uint32_t)((((unsigned)b[16] & 7) << 8) | b[17]), 20u);
            ck("M: the frame is still padded to the Ethernet minimum",
               (uint32_t)b.size(), 60u);
        }
        // ...and the store RECOVERS from the abandoned burst without a reset.
        // Note precisely what this does and does not prove: the header was
        // already validated before the memory was withdrawn, so the fetch
        // timeout marks the LOCATE as a miss and leaves img_valid standing —
        // it is the fetch path recovering, not the header probe re-arming.
        // (The re-arm arm is reachable only from a never-validated image, and
        // it answers BAD_ARGUMENTS rather than NO_SUCH_DESCRIPTOR because the
        // µprogram range-checks configurations_count — which reads 0 while the
        // image is invalid — before it ever locates.) What is graded is the
        // one thing a wedged store could not do: serve the next command.
        mem_answering = true;
        at = tx_frames.size();
        cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0202);
        inject_rx(cf, cn, 400);
        for (int r = 0; r < 4; r++) run_idle(20000);
        k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = (int)i; break; }
        ck_true("M: the image HEALS when memory returns (no reset)",
                k >= 0 && (tx_frames[k].bytes[16] >> 3) == 0,
                k >= 0 ? "SUCCESS again" : "still refusing after the load");
    }

    // ---- N. THE RESPONSE BUFFER'S MEMORY: it is USED, and it degrades -------
    // Section [L] graded byte-exact SUCCESS responses; every one of those was
    // assembled through this master, so the first two checks are what separate
    // "the buffer is in main memory" from "the harness happens to answer a
    // face nobody drives". Then the same discipline as [M]: withdraw the
    // memory ON PURPOSE and prove the documented degrade. The buffer's
    // watchdog VOIDS the response and KL_aecp_engine answers a well-formed
    // ENTITY_MISBEHAVING (1722.1 Table 7-127 status 10) instead of hanging,
    // going silent, or - the one that would actually hurt a controller -
    // putting a half-written response on the wire.
    printf("[N] response-buffer memory: exercised, then withdrawn\n");
    {
        printf("  [i]    resp-buffer traffic so far: %ld lane write(s), "
               "%ld read burst(s)\n", rm_writes, rm_reqs);
        ck_true("N: the buffer WROTE its lanes to main memory", rm_writes > 0,
                rm_writes > 0 ? "lane writes committed"
                              : "no write ever left the buffer - the response "
                                "is still fabric state");
        ck_true("N: ...and READ them back to build the frame", rm_reqs > 0,
                rm_reqs > 0 ? "read bursts served"
                            : "no read burst - the frame builder was fed from "
                              "somewhere else");

        rmem_answering = false;
        uint8_t cf[128];
        size_t at = tx_frames.size();
        size_t cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0301);
        inject_rx(cf, cn, 400);
        for (int r = 0; r < 8; r++) run_idle(20000);
        int k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = (int)i; break; }
        ck_true("N: with no memory, the command still gets an ANSWER", k >= 0,
                k >= 0 ? "the watchdog voided the response cleanly"
                       : "the uCPU HUNG on an absent bridge");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("N: status ENTITY_MISBEHAVING(10)", (b[16] >> 3) & 0x1F, 10u);
            ck("N: the response carries NO payload it could not build",
               (uint32_t)((((unsigned)b[16] & 7) << 8) | b[17]), 12u);
            ck("N: the frame is still padded to the Ethernet minimum",
               (uint32_t)b.size(), 60u);
            ck("N: ...and it is still addressed back to the requester",
               ((uint32_t)b[0] << 24) | ((uint32_t)b[1] << 16)
                   | ((uint32_t)b[2] << 8) | b[3], 0x02112233u);
        }
        // ...and it HEALS: a voided response is per-command, not sticky. The
        // buffer clears its fault on the next `open_i`, so the very next
        // command must be SUCCESS again with no reset anywhere.
        rmem_answering = true;
        at = tx_frames.size();
        cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0302);
        inject_rx(cf, cn, 400);
        for (int r = 0; r < 4; r++) run_idle(20000);
        k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = (int)i; break; }
        ck_true("N: the buffer HEALS when memory returns (no reset)",
                k >= 0 && (tx_frames[k].bytes[16] >> 3) == 0,
                k >= 0 ? "SUCCESS again"
                       : "still misbehaving after the memory came back");
    }

    // ---- K. THE SHARED CONTROL LANE (ctl_tx_mux) ---------------------------
    // Both legs must have transmitted, every frame must be well formed, and
    // the arbiters must never have fired their watchdogs. An abort is the
    // watchdog injecting a close beat into a stalled frame - a runt on the
    // wire - and a stall is the same event one level down, so a clean
    // A_TXARB_DIAG over a window in which BOTH legs transmitted is the
    // interleave evidence a frame count cannot give.
    printf("[K] ctl_tx_mux — the processor and MAAP share one lane, cleanly\n");
    run_idle(40000);
    {
        long n_adp = 0, n_acmp = 0, n_aecp = 0, n_maap = 0, n_msrp = 0, n_mvrp = 0;
        long n_alien = 0, n_short = 0, n_badlen = 0;
        for (const TxFrame& fr : tx_frames) {
            switch (classify(fr)) {
                case FR_ADP:  n_adp++;  break;
                case FR_AECP: n_aecp++; break;
                case FR_ACMP: n_acmp++; break;
                case FR_MAAP: n_maap++; break;
                case FR_MSRP: n_msrp++; break;
                case FR_MVRP: n_mvrp++; break;
                case FR_SHORT: n_short++; break;
                default: n_alien++; break;
            }
            const FrClass c = classify(fr);
            if (c == FR_ADP || c == FR_AECP || c == FR_ACMP || c == FR_MAAP
                || c == FR_AVTP_OTHER)
                if (!avtp_len_consistent(fr, nullptr)) n_badlen++;
        }
        printf("  [i]    MAC TX census: %zu frames / %ld beats — ADP %ld, AECP %ld, "
               "ACMP %ld, MAAP %ld, MSRP %ld, MVRP %ld, alien %ld, short %ld\n",
               tx_frames.size(), tx_beats_total, n_adp, n_aecp, n_acmp, n_maap,
               n_msrp, n_mvrp, n_alien, n_short);
        ck_true("the PROCESSOR leg transmitted",
                (n_adp + n_aecp + n_acmp + n_msrp + n_mvrp) > 0,
                (n_adp + n_aecp + n_acmp + n_msrp + n_mvrp) > 0
                    ? "processor PDUs on the wire" : "nothing from the processor");
        //! ...and the AECP leg specifically, which section [L] put there: the
        //! length rule below now covers AECPDUs too, so a response that was
        //! well formed in isolation but corrupted by the shared lane fails here
        ck_true("the AECP leg was represented on the shared lane", n_aecp > 0,
                n_aecp > 0 ? "AECP responses on the wire" : "no AECPDU egressed");
        ck_true("the MAAP leg transmitted", n_maap > 0,
                n_maap > 0 ? "MAAP PDUs on the wire" : "no MAAP PDU egressed");
        ck("no frame on the wire was too short to classify", (uint32_t)n_short, 0u);
        ck("no frame carried an unknown EtherType", (uint32_t)n_alien, 0u);
        ck("every AVTP PDU's length matches the length it declares",
           (uint32_t)n_badlen, 0u);
        ck("no beat before tlast carried a partial tkeep", (uint32_t)tx_bad_keep, 0u);
        // the MAAP frames really are KL_maap's, not a mislabelled fragment
        long maap_wrong_da = 0;
        for (const TxFrame& fr : tx_frames)
            if (classify(fr) == FR_MAAP && get_be(fr.bytes, 0, 6) != MAAP_DST)
                maap_wrong_da++;
        ck("every MAAP PDU carried KL_maap's own DA", (uint32_t)maap_wrong_da, 0u);

        const uint32_t d = axi_read(A_TXARB_DIAG);
        printf("  [i]    TXARB 0x784 = 0x%08X (stall %02X abort %02X locked %02X)\n",
               d, (d >> 16) & 0xFF, (d >> 8) & 0xFF, d & 0xFF);
        ck("ctl_tx_mux (lane 0) never aborted a frame", (d >> 8) & 0x1, 0u);
        ck("the MAC-boundary mux (lane 3) never aborted a frame",
           (d >> 8) & 0x8, 0u);
        ck("no TX-trunk arbiter ever stalled", (d >> 16) & 0xF, 0u);
    }

    // ---- the global anti-wedge invariant, over the WHOLE run --------------
    // The hazard the adapter can create is exactly one: take a request and
    // never answer it. Graded once, over every cycle simulated.
    printf("[J] global invariant: no accepted maap request was ever dropped\n");
    ck_true("accepted == answered across the entire run",
            mo.accepted == mo.answered,
            mo.accepted == mo.answered ? "balanced" : "UNBALANCED - a source is stranded");
    // ...and the OTHER half of the face is unreachable in this shape, on
    // purpose: milan_datapath ties cfg_src_en_i to all-ones, so no talker
    // source can ever leave the configuration and no RELEASE_DA can ever be
    // issued. That is why the owed-release law (a release booked per source
    // and retried until the face ACCEPTS it, ahead of any ALLOC_DA) is proven
    // in protocol-processor/tb/acmp_talker section L and not here. Graded
    // rather than assumed: wire cfg_src_en_i to anything live and this goes
    // red, which is the reminder to bring that path under test HERE too.
    ck("no RELEASE_DA is reachable while every source is pinned enabled",
       (uint32_t)mo.released, 0u);

    printf("----------------------------------------------------------------\n");
    printf("pp_shadow: %ld checks, %ld failures\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    delete dut;
    return fails ? 1 : 0;
}

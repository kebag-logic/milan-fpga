/*
 * SPDX-FileCopyrightText: 2026 Kebag Logic
 * SPDX-License-Identifier: CERN-OHL-W-2.0
 *
 * P12 NxN integration harness: milan_datapath at N_STREAMS=4, CSR 0x800
 * window -> REAL engines end-to-end (NXN_ARCHITECTURE.md P12 gate):
 *
 *   1. provision listener streams 1..2 THROUGH the window (SID/FMT staged,
 *      CTRL commit -> LCTX CFG words + stream-table entry + route field),
 *      readback of the CFG words through the engine-arbitrated LCTX port B
 *      (the monitor context RAM, not a CSR shadow);
 *   2. feed tagged AAF frames of both streams + an unknown sid on the MAC
 *      RX AXIS: classification tuser rides parser -> monitor -> depkt ->
 *      route; stream 1 (route=DMA flag) lands on the PCM ring output with
 *      tuser=1, stream 2 (route=NULL) is counted but not forwarded;
 *   3. read ISOLATED per-stream counters back through the window with SNAP
 *      (Table 7-157 block from the live LCTX; stream 0 legacy aliases and
 *      idx 3 stay zero); a seq-gap on stream 1 moves ONLY stream 1;
 *   4. talker side: TCTX CFG words written and read back through the live
 *      KL_aaf_packetizer window port.
 *
 * P12 follow-up gates (route flags + talker t>0 arming):
 *   5. route FLAGS {bit1 RENDER, bit0 DMA}: RENDER|DMA renders AND rings
 *      (capture-while-rendering), RENDER-only renders without a ring copy,
 *      NULL suppresses both (render truth = the datapath render-tap valid,
 *      a verilator-public probe - the flat CSRs expose no per-stream tap);
 *   6. talker t>0 arming composition (aaf_stream_en_w, verilator-public;
 *      2026-07-26 mirrored contract): t1 arms via the window TCTX CTRL[0]
 *      commit; the composition mirrors t0 TERM BY TERM - per-stream ACMP
 *      talker_active (N-context responder), cfg_aaf_bypass as the escape
 *      hatch for EVERY stream, per-stream lwSRP gate with the engine-off
 *      escape, and the engine-wide MAAP term (one claim engine, block of
 *      N addresses, stream j = base+j); window CTRL[0]=0 disarms t1.
 *      t>0 wire emission needs a sample source for its slots: the chmap
 *      capture crossbar (0x900/CMAP) feeds any of the 32 pair slots; the
 *      PHYSICAL I2S front-end alone still emits slot 0 only - frame-level
 *      TCTX-identity emission + per-slot gate drop are proven in
 *      tb/verilator/aaf sim_main_nx [I2T]/[I2T4].
 *      KL_aaf_packetizer window port;
 *   5. N-sink ACMP round: a CONNECT_RX bind of listener context 2 (a
 *      window stream's record-only explicit-sid context) reads back
 *      END-TO-END through the window's ACMP table master (SID/DMAC live,
 *      STATE via SNAP); unbound idx 3 and ctx 0 stay honest zero.
 */

#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <cstdlib>
#include <string>
#include <vector>
#include <map>
#include <unistd.h>
#include <cstdio>

// Stream count the C++ side walks. Paired with the RTL -GN_STREAMS by the
// Makefile: the default obj_nxn build is N=4; the obj_nxn8 build passes
// -GN_STREAMS=8 AND -DNSTREAMS_TB=8 so the sweep below walks idx 3..7 (the
// AX 8x8 target - the top half of the index space only exists at N=8).
#ifndef NSTREAMS_TB
#define NSTREAMS_TB 4
#endif

static Vmilan_datapath* dut;
static long checks = 0, fails = 0;
static void ck(const char* what, unsigned long got, unsigned long exp) {
    checks++;
    if (got != exp) {
        fails++;
        printf("  [FAIL] %-46s got=0x%lx exp=0x%lx\n", what, got, exp);
    } else {
        printf("  [ok]   %-46s = 0x%lx\n", what, got);
    }
}

// ---- AECP RESPONSE MEMORY model -------------------------------------------
// PORTED VERBATIM IN SHAPE from tb/verilator/pp_shadow, which is the proven
// one. Two hand-rolled attempts failed here before I copied it, and the reason
// is one line: wr_ready must go LOW while a commit is pending, so wr_done can
// never coincide with the wr_ready that accepted the write. That is the only
// shape KL_aecp_resp_buf's flush arm accepts - it sets wbusy_r on the ready and
// only THEN looks for the done. Get it wrong and the write never completes,
// the watchdog fires, and every AECP answer degrades to ENTITY_MISBEHAVING(10)
// - which looks like an RTL defect and is not.
//
// The response buffer is NOT optional the way the descriptor image is: every
// AECP answer is assembled in it. This leg's deliberate omission is the
// DESCRIPTOR image (see the [AECP] banner below); the response path is backed.
static const uint32_t RESP_BASE  = 0x20100000u;   // PP_RESP_BASE_P default
static const uint32_t RESP_BYTES = 592u;          // 16 + PP_DESC_LINE_BYTES_P

static uint8_t  rmem[RESP_BYTES];
// A memory that NEVER ACKS is a distinct failure from a memory that answers an
// error, and until 2026-08-13 nothing in this tree drove it: the SoC-side
// bridge left its bus states only on `ack`, so one unanswered access parked it
// there for good - with `cyc`/`stb` held, which the dma_bus arbiter reads as an
// outstanding transaction and stops re-arbitrating on, taking every other
// master with it. On the board that showed up as descriptor-store fault 8
// (FAULT_TIMEOUT), response-buffer fault 1 (FAULT_WTMO) and every AECP command
// answered ENTITY_MISBEHAVING. Held low, these four inputs ARE that bridge:
// section [AECP-WTMO] below drives them so the seam is graded, not assumed.
static bool     rm_answering = true;
static bool     rm_busy  = false;                 // read burst in flight
static uint32_t rm_cur   = 0;
static int      rm_left  = 0;
static bool     rm_wpend = false;                 // accepted, commits next edge
static uint32_t rm_waddr = 0;
static uint64_t rm_wdata = 0;
static uint32_t rm_wstrb = 0;

static uint64_t rmem_beat(uint32_t byte_addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {                 // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - RESP_BASE + (uint32_t)i;
        v = (v << 8) | (uint64_t)((off < RESP_BYTES) ? rmem[off] : 0);
    }
    return v;
}

static void rmem_drive() {
    if (!rm_answering) {                           // the wedged-bridge arm
        dut->i_resp_mem_req_ready = 0;
        dut->i_resp_mem_rsp_valid = 0;
        dut->i_resp_mem_rsp_data  = 0;
        dut->i_resp_mem_rsp_last  = 0;
        dut->i_resp_mem_rsp_err   = 0;
        dut->i_resp_mem_wr_ready  = 0;
        dut->i_resp_mem_wr_done   = 0;
        dut->i_resp_mem_wr_err    = 0;
        return;
    }
    dut->i_resp_mem_req_ready = rm_busy ? 0 : 1;
    dut->i_resp_mem_rsp_valid = rm_busy ? 1 : 0;
    dut->i_resp_mem_rsp_data  = rm_busy ? rmem_beat(rm_cur) : 0;
    dut->i_resp_mem_rsp_last  = (rm_busy && rm_left == 1) ? 1 : 0;
    dut->i_resp_mem_rsp_err   = 0;
    dut->i_resp_mem_wr_ready  = rm_wpend ? 0 : 1;   // low while a commit is owed
    dut->i_resp_mem_wr_done   = rm_wpend ? 1 : 0;
    dut->i_resp_mem_wr_err    = 0;
}

static void rmem_edge() {
    if (!rm_answering) return;                     // accepts nothing either
    if (!rm_busy) {
        if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
            rm_cur  = dut->o_resp_mem_req_addr;
            rm_left = (int)dut->o_resp_mem_req_beats;
            rm_busy = (rm_left > 0);
        }
    } else if (dut->o_resp_mem_rsp_ready) {         // real backpressure
        rm_cur += 8;
        if (--rm_left <= 0) rm_busy = false;
    }
    if (rm_wpend) {
        for (int i = 0; i < 8; i++) {
            if (rm_wstrb & (1u << i)) {             // zero-strobe byte untouched
                const uint32_t k = rm_waddr - RESP_BASE + (uint32_t)i;
                if (k < RESP_BYTES) rmem[k] = (uint8_t)(rm_wdata >> (56 - 8 * i));
            }
        }
        rm_wpend = false;
    } else if (dut->o_resp_mem_wr_valid && dut->i_resp_mem_wr_ready) {
        rm_waddr = dut->o_resp_mem_wr_addr;
        rm_wdata = dut->o_resp_mem_wr_data;
        rm_wstrb = dut->o_resp_mem_wr_strb;
        rm_wpend = true;
    }
}

// ---- AEM DESCRIPTOR MEMORY: THE MEMORY THAT WORKS --------------------------
// The nine desc_mem ports are the entity model's supply. Every AECP check
// written before [AECP-IMG] drove them DEAD, and that was the whole of the
// coverage: a bridge that never transacts and a harness that offers no memory
// produce the SAME waveform, so a plane that could not fetch a single beat
// passed every gate. On 2026-08-13 that is what silicon shipped - img_valid 0,
// descriptor-store fault 8 (FAULT_TIMEOUT), dbg_lane_wr parked at 2 - and no
// desk test in this tree could go red.
//
// So this model ANSWERS, and it answers the way main memory does rather than
// the way a testbench does:
//
//   * ONE outstanding burst, beats IN ORDER, `last` on the final one, and
//     o_desc_mem_rsp_ready honoured as REAL backpressure even though
//     KL_aecp_desc_store ties it 1 - a model that ignored it would hide the
//     day the store stops always sinking;
//   * the FIRST beat of every burst is DESC_MISS_CYC clocks late. A
//     zero-latency memory is the one shape that cannot exist behind a bus,
//     and it is precisely the shape that hides handshake defects: req_ready
//     and rsp_valid in the same cycle never separate "accepted" from
//     "answered";
//   * rsp_valid DROPS mid-burst. The contract orders the beats, it does not
//     promise them gapless, so a consumer that assumed gapless would only
//     ever fail against a memory that is not.
static const uint32_t DESC_BASE = 0x20000000u;   // PP_DESC_BASE_P default

// MEASURED, not invented. The reference SoC's miss to main memory is about
// 1,424 ns and milan_dp elaborates the processor at MILAN_CLK_FREQ_HZ =
// 100 MHz, so a miss is 142 clocks. The store's own no-progress watchdog is
// DESC_MEM_TMO_CYC_P = 4,096 clocks, which is the constraint that keeps this
// a realistic memory instead of a disguised timeout test.
static const int DESC_MISS_CYC  = 142;
static const int DESC_GAP_EVERY = 4;    // beats between one-clock bubbles

static std::vector<uint8_t> desc_img;   // the AEMI image, byte for byte
// what the wire MUST carry, keyed (type << 16) | index - see aemi_load()
static std::map<uint32_t, std::vector<uint8_t> > desc_want;

// Boot the processor with the image matching this elaborated entity shape.
// The descriptor store validates and caches its index at startup, just like
// the board, so replacing only the backing bytes later is not a valid image
// change and cannot prove the declared NxN descriptor set.
#if NSTREAMS_TB == 8
static const char AEMI_CFG_C[] = "endstation_ax7101_8x8";
#elif NSTREAMS_TB == 4
static const char AEMI_CFG_C[] = "endstation_arty_4x4";
#else
static const char AEMI_CFG_C[] = "endstation_ax7101_1x1_tdm8";
#endif

static bool     dm_answering = false;   // [AECP]/[AECP-WTMO] need it OFF
static bool     dm_busy   = false;      // read burst in flight
static uint32_t dm_cur    = 0;
static int      dm_left   = 0;
static int      dm_wait   = 0;          // clocks still owed before the beat
static int      dm_run    = 0;          // beats since the last bubble
static long     dm_bursts = 0, dm_beats = 0;

static uint64_t desc_beat(uint32_t byte_addr) {
    uint64_t v = 0;
    for (int i = 0; i < 8; i++) {                 // big-endian: byte n at [63-8n-:8]
        const uint32_t off = byte_addr - DESC_BASE + (uint32_t)i;
        v = (v << 8) | (uint64_t)((off < desc_img.size()) ? desc_img[off] : 0);
    }
    return v;
}

static void dmem_drive() {
    const bool beat = dm_answering && dm_busy && (dm_wait == 0);
    dut->i_desc_mem_req_ready = (dm_answering && !dm_busy) ? 1 : 0;
    dut->i_desc_mem_rsp_valid = beat ? 1 : 0;
    dut->i_desc_mem_rsp_data  = beat ? desc_beat(dm_cur) : 0;
    dut->i_desc_mem_rsp_last  = (beat && dm_left == 1) ? 1 : 0;
    dut->i_desc_mem_rsp_err   = 0;
}

static void dmem_edge() {
    if (!dm_answering) return;                    // offers nothing either
    if (!dm_busy) {
        if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
            dm_cur  = dut->o_desc_mem_req_addr;
            dm_left = (int)dut->o_desc_mem_req_beats;
            dm_busy = (dm_left > 0);
            dm_wait = DESC_MISS_CYC;              // the miss, paid per burst
            dm_run  = 0;
            dm_bursts++;
        }
    } else if (dm_wait > 0) {
        dm_wait--;
    } else if (dut->o_desc_mem_rsp_ready) {       // real backpressure
        dm_cur += 8;
        dm_beats++;
        if (--dm_left <= 0) dm_busy = false;
        else if (++dm_run == DESC_GAP_EVERY) { dm_run = 0; dm_wait = 1; }
    }
}

// THE IMAGE IS THE ONE THE BUILD SHIPS. avdecc/gen_aemi_image.py is the join
// between gen_aem_store's descriptor bytes and the submodule's image packer,
// and sw/litex writes THAT script's output at PP_DESC_BASE_P. Regenerating it
// here is what makes the byte-exact comparison below worth anything: a
// harness that packed its own image would agree with itself while the shipped
// one enumerated nothing.
//
// The --json document is the second half, and the reason no image arithmetic
// appears in this file: it carries every descriptor's bytes keyed by (type,
// index), so the expectation never restates the header walk, the index map or
// the elem_off + index*stride locate the store performs. Two independent
// paths to the same bytes; a store that located the wrong offset has nowhere
// to hide. --line-bytes MUST match PP_DESC_LINE_BYTES_P (576) or the packer
// would accept a descriptor longer than the store's line buffer.
//
// A REAL OVERLAY, BUILT HERE, and not the generator's built-in spec. The
// generator requires --overlay on purpose (07f256fc): the built-in shape names
// no board, so its ADP identity spans - entity_id, entity_model_id, the
// capability words - would go into the image UNBAKED, and an image whose
// identity is zeros enumerates as a different entity than the one the ROM
// describes. Refusing to guess is the right behaviour and this harness must
// not be the reason it is weakened.
//
// So the harness builds its own overlay first, from a TRACKED config, into its
// own temp dir. sw/builder/out/ being gitignored was the original reason to
// avoid an overlay; -o removes it. Nothing about the suite depends on WHICH
// shape: the store serves whatever main memory holds and knows nothing of the
// elaborated stream count, so the 1x1 shipping config is used for every leg
// and the expectation IS that same image. The gain over the built-in spec is
// that the bytes compared are now the bytes a board would actually be served.
//
// CWD: the harness already runs from tb/verilator/milan_dp - the processor
// $readmemh's ltn_rom.hex and ucode.hex by relative name - so the generator
// sits at a known relative depth.
static bool aemi_load(const char* cfg, std::string* why) {
    char bin[160], js[160], log[160], bld[160], ovl[224], cmd[900];
    const int pid = (int)getpid();               // parallel lanes share /tmp
    snprintf(bin, sizeof bin, "/tmp/milan_nxn_aemi_%d.bin", pid);
    snprintf(js,  sizeof js,  "/tmp/milan_nxn_aemi_%d.json", pid);
    snprintf(log, sizeof log, "/tmp/milan_nxn_aemi_%d.log", pid);
    snprintf(bld, sizeof bld, "/tmp/milan_nxn_bld_%d", pid);

    desc_img.clear();
    desc_want.clear();

    // The builder writes into <outdir>/<config-stem>/; no --write-rtl and no
    // --write-fragment, so it touches nothing tracked.
    snprintf(cmd, sizeof cmd,
             "python3 ../../../sw/builder/endstation_builder.py "
             "../../../configs/%s.yaml -o %s > %s 2>&1", cfg, bld, log);
    if (system(cmd) != 0) {
        *why = std::string("endstation_builder.py failed; its output is in ")
             + log;
        return false;
    }
    snprintf(ovl, sizeof ovl, "%s/%s/aem_overlay.json", bld, cfg);

    snprintf(cmd, sizeof cmd,
             "python3 ../../../avdecc/gen_aemi_image.py --overlay %s "
             "-o %s --json %s --line-bytes 576 > %s 2>&1", ovl, bin, js, log);
    if (system(cmd) != 0) {
        *why = std::string("gen_aemi_image.py failed; its output is in ") + log;
        return false;                            // the log is left for reading
    }

    FILE* fh = fopen(bin, "rb");
    if (!fh) { *why = "the generator wrote no image"; return false; }
    uint8_t buf[4096];
    size_t n;
    while ((n = fread(buf, 1, sizeof buf, fh)) > 0)
        desc_img.insert(desc_img.end(), buf, buf + n);
    fclose(fh);

    std::string doc;
    fh = fopen(js, "rb");
    if (!fh) { *why = "the generator wrote no document"; return false; }
    while ((n = fread(buf, 1, sizeof buf, fh)) > 0)
        doc.append((const char*)buf, n);
    fclose(fh);

    // The document is machine-written (json.dump), one object per descriptor
    // with configuration/type/index/bytes in that order, so a scan from each
    // "type" key to its object's "bytes" is unambiguous.
    size_t p = 0;
    while ((p = doc.find("\"type\":", p)) != std::string::npos) {
        const long ty = strtol(doc.c_str() + p + 7, nullptr, 10);
        const size_t pi = doc.find("\"index\":", p);
        const size_t pb = doc.find("\"bytes\":", p);
        if (pi == std::string::npos || pb == std::string::npos) break;
        const long ix = strtol(doc.c_str() + pi + 8, nullptr, 10);
        size_t q0 = doc.find('"', pb + 8);
        if (q0 == std::string::npos) break;
        const size_t q1 = doc.find('"', ++q0);
        if (q1 == std::string::npos) break;
        std::vector<uint8_t> d;
        for (size_t i = q0; i + 1 < q1; i += 2)
            d.push_back((uint8_t)strtol(doc.substr(i, 2).c_str(), nullptr, 16));
        desc_want[((uint32_t)ty << 16) | ((uint32_t)ix & 0xFFFFu)] = d;
        p = q1;
    }
    remove(bin); remove(js); remove(log);
    if (desc_img.empty() || desc_want.empty()) {
        *why = "the generator produced an empty image or document";
        return false;
    }
    return true;
}

static const std::vector<uint8_t>* desc_of(unsigned ty, unsigned ix) {
    std::map<uint32_t, std::vector<uint8_t> >::const_iterator it =
        desc_want.find(((uint32_t)ty << 16) | ix);
    return (it == desc_want.end()) ? nullptr : &it->second;
}

static void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0;
                   rmem_drive(); dmem_drive(); dut->eval();
                   rmem_edge(); dmem_edge(); }
static void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->eval(); }
static unsigned long tkd_dirty_seen = 0;
static void step() {
    lo(); hi();
    tkd_dirty_seen |= dut->rootp->milan_datapath__DOT__tkd_dirty_p_w;
}

// ---- AXI4-Lite BFM (same protocol as the milan_dp legacy harness) ----
static void axi_write(uint16_t a, uint32_t d) {
    dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = d;  dut->s_axi_wvalid = 1; dut->s_axi_wstrb = 0xF;
    dut->s_axi_bready = 1;
    for (int g = 0; g < 4096; ++g) {
        dut->eval();
        bool acc = dut->s_axi_awready && dut->s_axi_wready;
        step();
        if (acc) break;
    }
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
    for (int g = 0; g < 4096; ++g) { dut->eval(); if (dut->s_axi_bvalid) break; step(); }
    step();
    dut->s_axi_bready = 0;
}

static uint32_t axi_read(uint16_t a) {
    dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (int g = 0; g < 4096; ++g) {
        dut->eval();
        bool acc = dut->s_axi_arready;
        step();
        if (acc) break;
    }
    dut->s_axi_arvalid = 0;
    uint32_t v = 0;
    for (int g = 0; g < 4096; ++g) { dut->eval(); if (dut->s_axi_rvalid) { v = dut->s_axi_rdata; break; } step(); }
    step();
    dut->s_axi_rready = 0;
    return v;
}

enum {
    A_ID = 0x000, A_VERSION = 0x004,
    A_AAF_CTRL = 0x654, A_AAF_FRAMES = 0x660, A_LWSRP_CTRL = 0x680,
    A_CRFT_CTRL = 0x750,
    A_ADP_CTRL = 0x600, A_ADP_EIDLO = 0x604, A_ADP_EIDHI = 0x608,
    A_ADP_TALK = 0x618, A_ADP_LIST = 0x61C,
    A_AVTPRX_STAT = 0x6B8, A_AVTPRX_FRX = 0x6BC, A_PCMRX_CNT = 0x6C4,
    A_MAAP_CTRL = 0x6CC,
    A_STRM_SEL = 0x800, A_STRM_SNAP = 0x804, A_SW_CTRL = 0x810,
    A_SW_SID_LO = 0x814, A_SW_SID_HI = 0x818, A_SW_DMAC_LO = 0x81C,
    A_SW_DMAC_HI = 0x820, A_SW_FMT_LO = 0x824, A_SW_FMT_HI = 0x828,
    A_SW_STATE = 0x82C, A_SW_CNT0 = 0x830, A_SW_PDUS = 0x858,
    A_PP_STAT = 0x924, A_PP_SPADDR = 0x928, A_PP_SPDATA = 0x92C,
};

// ---- the processor's SIDE PORT, through the 0x920 CSR window --------------
// A fabric walk must never stall an AXI read, so the access is POSTED
// (milan_csr.sv g_pp_csr): a WRITE to SPADDR arms AND posts a read, PP_STAT[0]
// (sp_busy) falls when the processor acked, PP_STAT[5] is that access's error,
// and SPDATA holds the answer. Side-port window 2 is the snapshot dictionary
// (KL_pp_side_port.sv WIN_SNAP_C), whose word 0 reads "KLPP" - which is what
// separates "the store says img_valid = 0" from "this window reads zero".
static const uint32_t SP_SNAPSHOT = 0x20000;

static uint32_t sp_read(uint32_t word_addr, bool* ok) {
    axi_write(A_PP_SPADDR, word_addr);
    uint32_t st = 0;
    int g = 0;
    for (; g < 256; g++) {
        st = axi_read(A_PP_STAT);
        if ((st & 1) == 0) break;               // sp_busy fell: the walk acked
        step();
    }
    if (ok) *ok = (g < 256) && (((st >> 5) & 1) == 0);
    return axi_read(A_PP_SPDATA);
}

// route flags (KL_pcm_route / window CTRL[2:1]): bit0 = DMA, bit1 = RENDER
enum { RT_NULL = 0, RT_DMA = 1, RT_RENDER = 2, RT_RENDER_DMA = 3 };

// composed per-stream talker enables (milan_datapath aaf_stream_en_w)
static unsigned tap_stream_en() {
    return dut->rootp->milan_datapath__DOT__aaf_stream_en_w;
}

static void snap_and_wait() {
    axi_write(A_STRM_SNAP, 1);
    for (int g = 0; g < 256; ++g)
        if ((axi_read(A_STRM_SNAP) & 1) == 0) return;
}

// ---- PCM ring collection: {tuser, payload bytes} per AXIS frame ----
struct PcmFrame { int user; std::vector<uint8_t> bytes; };
static std::vector<PcmFrame> pcm_frames;
static bool pcm_open = false;
static long render_beats = 0;   // datapath render-tap beats (public probe)

static void pcm_sample() {
    if (dut->m_axis_pcm_tvalid) {
        if (!pcm_open) { pcm_frames.push_back({(int)dut->m_axis_pcm_tuser, {}}); pcm_open = true; }
        for (int l = 0; l < 8; l++)
            pcm_frames.back().bytes.push_back((dut->m_axis_pcm_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_pcm_tlast) pcm_open = false;
    }
    if (dut->rootp->milan_datapath__DOT__rend_pcm_tvalid_w) render_beats++;
}

// ---- ACMP PROBE_TX sniffer: the listener matches a PROBE_TX_RESPONSE on
// controller+talker+tuid+sequence_id (Milan 5.5.3.5.18 step 1), so answers
// must echo the probe's OWN sequence_id — harvest it off the egress while
// inject() drains. A probe launches within the bind's drain window, and the
// 100 MHz TMR_NO_RESP (20M cycles) means no second draw can occur inside a
// leg, so the per-luid latch stays valid across the follow-up CSR reads.
static std::vector<uint8_t> acmp_sniff_fr;
static uint16_t probe_seq_by_luid[16];
//! ...and a SEEN flag beside it. The sequence_id is a legitimate 0 on the
//! first draw (measured: sink 0's first PROBE_TX carries seq 0), so
//! "probe_seq != 0" is not a liveness test.
static bool     probe_seen_luid[16];
static void acmp_sniff() {
    if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
        for (int l = 0; l < 8; l++)
            if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                acmp_sniff_fr.push_back(
                    (dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
        if (dut->m_axis_mac_tx_tlast) {
            if (acmp_sniff_fr.size() >= 70 && acmp_sniff_fr[12] == 0x22 &&
                acmp_sniff_fr[13] == 0xF0 && acmp_sniff_fr[14] == 0xFC &&
                (acmp_sniff_fr[15] & 0xF) == 0x0) {   // CONNECT_TX_COMMAND
                int luid = ((acmp_sniff_fr[52] << 8) | acmp_sniff_fr[53]) & 0xF;
                probe_seq_by_luid[luid] =
                    (uint16_t)((acmp_sniff_fr[62] << 8) | acmp_sniff_fr[63]);
                probe_seen_luid[luid] = true;
            }
            acmp_sniff_fr.clear();
        }
    }
}

// ---- inject one little-lane frame on the MAC RX port ----
static void inject(const uint8_t* f, size_t len, int drain = 1200) {
    std::vector<uint64_t> beats;
    for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++)
            if (bt*8 + j < len) v |= (uint64_t)f[bt*8+j] << (8*j);
        beats.push_back(v);
    }
    size_t idx = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->m_axis_pcm_tready = 1;
    acmp_sniff_fr.clear();   // a fragment drained elsewhere is not a frame
    for (int c = 0; c < drain; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata  = beats[idx];
            dut->s_axis_mac_rx_tkeep  = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        pcm_sample();
        acmp_sniff();
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
}

// PARKED-LANE TORTURE (gh #65). rx_axis_to_dma.tready IS m_axis_rx_tready,
// so dropping the host DMA's ready parks a beat on the tapped lane with
// tvalid held — the documented starvation/flood regime. A monitor tap that
// samples tvalid alone eats every parked cycle as a NEW beat, tears the
// frame, and spends the next real PDU realigning.
static void inject_parked(const uint8_t* f, size_t len, int park_beat,
                          int park_cycles, int drain = 6000) {
    std::vector<uint64_t> beats;
    for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
        uint64_t v = 0;
        for (int j = 0; j < 8; j++)
            if (bt*8 + j < len) v |= (uint64_t)f[bt*8+j] << (8*j);
        beats.push_back(v);
    }
    size_t idx = 0;
    int parked = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->m_axis_pcm_tready = 1;
    for (int c = 0; c < drain; c++) {
        if (idx < beats.size()) {
            dut->s_axis_mac_rx_tdata  = beats[idx];
            dut->s_axis_mac_rx_tkeep  = 0xFF;
            dut->s_axis_mac_rx_tvalid = 1;
            dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
        } else {
            dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
        }
        bool want_park = ((int)idx == park_beat) && (parked < park_cycles);
        dut->m_axis_rx_tready = want_park ? 0 : 1;
        if (want_park) parked++;
        lo();
        bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
        pcm_sample();
        hi();
        if (in_acc) idx++;
    }
    dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_rx_tready = 1;
}

// ---- gh #58 D1 end-to-end: one AECP AEM transaction through the REAL RX
// path, the response fished off the MAC TX trunk (subtype 0xFB; the only
// 0xFB frames in this sim are our responses - nothing ever REGISTERs).
// dst MAC = the station MAC, which this harness leaves at its reset 0.
static std::vector<uint8_t> aecp_xact(uint16_t cmd, uint16_t sq,
                                      const std::vector<uint8_t>& pl,
                                      int cyc = 200000) {
    uint8_t f[80]; memset(f, 0, sizeof f);
    const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
    memcpy(f+6, csrc, 6);
    f[12]=0x22; f[13]=0xF0; f[14]=0xFB; f[15]=0x00;      // AECP AEM_COMMAND
    uint16_t cdl = (uint16_t)(12 + pl.size());
    f[16]=(uint8_t)((cdl >> 8) & 0x7); f[17]=(uint8_t)cdl;
    const uint8_t teid[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
    memcpy(f+18, teid, 8);                                // = A_ADP_EID
    const uint8_t ceid[8] = {0x68,0x05,0xCA,0xFF,0xFE,0x95,0xB2,0xD1};
    memcpy(f+26, ceid, 8);
    f[34]=(uint8_t)(sq >> 8); f[35]=(uint8_t)sq;
    f[36]=(uint8_t)((cmd >> 8) & 0x7F); f[37]=(uint8_t)cmd;
    for (size_t i = 0; i < pl.size() && 38 + i < sizeof f; i++) f[38+i] = pl[i];
    size_t flen = 38 + pl.size(); if (flen < 60) flen = 60;
    inject(f, flen, 40);
    std::vector<uint8_t> cur, resp;
    cur.reserve(1514);                  // one Ethernet frame off the TX trunk
    dut->m_axis_mac_tx_tready = 1;
    for (int c = 0; c < cyc && resp.empty(); c++) {
        lo();
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            for (int l = 0; l < 8; l++)
                if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                    cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
            if (dut->m_axis_mac_tx_tlast) {
                if (cur.size() > 17 && cur[12] == 0x22 && cur[13] == 0xF0 &&
                    cur[14] == 0xFB)
                    resp = std::move(cur);      // hand over, do not copy
                cur.clear();
            }
        }
        hi();
    }
    return resp;
}
static long aecp_status(const std::vector<uint8_t>& b) {
    return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
}

//! ONE served descriptor, graded end to end against the image this harness
//! generated: the answer exists, its status is SUCCESS, its declared length
//! agrees with the descriptor's real length, and the BYTES on the wire are
//! the image's. Returns that length so the caller can bound the response
//! memory's lane commits from the payload size alone.
//!
//! The wire layout (1722.1-2021 9.2.1 + 7.4.5.2), offsets from the frame:
//!   +16..17  status[4:0] then control_data_length[10:0] = 12 + payload
//!   +34..35  sequence_id, echoed
//!   +36..37  u = 0 + command_type, echoed
//!   +38..39  configuration_index      +40..41 reserved
//!   +42..    the descriptor itself
//! so the payload is 4 + descriptor_length and the frame is 42 + that length.
static size_t grade_read_desc(const char* tag, unsigned ty, unsigned ix,
                              uint16_t seq) {
    char w[112];
    const std::vector<uint8_t>* want = desc_of(ty, ix);
    snprintf(w, sizeof w, "%s: the image HAS this descriptor", tag);
    ck(w, (long)(want != nullptr), 1);
    if (!want) return 0;

    std::vector<uint8_t> pl(8, 0);              // cfg, reserved, type, index
    pl[4] = (uint8_t)(ty >> 8); pl[5] = (uint8_t)ty;
    pl[6] = (uint8_t)(ix >> 8); pl[7] = (uint8_t)ix;
    const std::vector<uint8_t> r = aecp_xact(0x0004, seq, pl);

    snprintf(w, sizeof w, "%s: READ_DESCRIPTOR was ANSWERED", tag);
    ck(w, (long)(r.size() >= 46), 1);
    if (r.size() < 46) return 0;

    snprintf(w, sizeof w, "%s: an AEM_RESPONSE (message_type 1)", tag);
    ck(w, r[15] & 0x0F, 1);
    snprintf(w, sizeof w, "%s: status SUCCESS(0)", tag);
    ck(w, aecp_status(r), 0);
    snprintf(w, sizeof w, "%s: sequence_id echoed", tag);
    ck(w, ((unsigned)r[34] << 8) | r[35], seq);
    snprintf(w, sizeof w, "%s: command_type echoed, u = 0", tag);
    ck(w, ((unsigned)r[36] << 8) | r[37], 0x0004);
    //! the LENGTH comes from the image, never from the frame being graded
    snprintf(w, sizeof w, "%s: cdl = 12 + 4 + the descriptor", tag);
    ck(w, (((unsigned)r[16] & 7) << 8) | r[17], 16 + want->size());
    size_t flen = 42 + want->size();
    if (flen < 60) flen = 60;                   // the Ethernet minimum
    snprintf(w, sizeof w, "%s: the frame is as long as it claims", tag);
    ck(w, (long)r.size(), (long)flen);
    snprintf(w, sizeof w, "%s: configuration_index @24 echoed", tag);
    ck(w, ((unsigned)r[38] << 8) | r[39], 0);
    snprintf(w, sizeof w, "%s: reserved @26 is zero", tag);
    ck(w, ((unsigned)r[40] << 8) | r[41], 0);

    long bad = 0;
    for (size_t i = 0; i < want->size(); i++)
        if (42 + i >= r.size() || r[42 + i] != (*want)[i]) bad++;
    snprintf(w, sizeof w, "%s: the bytes ARE the image's, exactly", tag);
    ck(w, bad, 0);
    //! ...and they are the descriptor that was ASKED for. The compare above
    //! already fails on a wrong index; these two say WHICH failure it was,
    //! which is the difference between "the locate is wrong" and "the image
    //! is wrong".
    snprintf(w, sizeof w, "%s: descriptor_type field @28", tag);
    ck(w, ((unsigned)r[42] << 8) | r[43], ty);
    snprintf(w, sizeof w, "%s: descriptor_index field @30", tag);
    ck(w, ((unsigned)r[44] << 8) | r[45], ix);
    return want->size();
}

// ---------------------------------------------------------------------------
// THE MODEL-DRIVEN COMMAND SWEEP
// ---------------------------------------------------------------------------
// Every expectation below is DERIVED FROM THE GENERATED ENTITY MODEL - the
// same `desc_want` map `grade_read_desc` grades against, built by running
// endstation_builder.py and gen_aemi_image.py live in this testbench. Nothing
// here is a literal, and nothing is taken from the DUT's own answer, so a
// device that is consistently wrong still fails.
//
// This is the layer that answers "do all the commands respond correctly TO
// THE ENTITY MODEL". READ_DESCRIPTOR walks every row of the model rather than
// the two descriptors it used to spot-check, and each read-side command is
// graded against the very field of the very descriptor the standard says it
// mirrors:
//   GET_CONFIGURATION  = ENTITY.current_configuration       @310 (IEEE 7.4.8.2)
//   GET_SAMPLING_RATE  = AUDIO_UNIT.current_sampling_rate   @136 (IEEE 7.4.22.2)
//   GET_CLOCK_SOURCE   = CLOCK_DOMAIN.clock_source_index     @70 (IEEE 7.4.24.2)
// GET_STREAM_FORMAT is deliberately NOT graded against the descriptor's
// current_format: IEEE 7.4.10.2 says "the current stream format", and current
// means after a SET_STREAM_FORMAT or a Milan 5.5 bind has adapted it, so the
// integrator's face - not the static image - is the authority. Its SHAPE is
// graded here and its VALUE byte-exactly in protocol-processor/tb/pp_top.
static unsigned model_be16(const std::vector<uint8_t>& d, size_t off) {
    return (off + 1 < d.size()) ? (((unsigned)d[off] << 8) | d[off + 1]) : 0u;
}
static unsigned long model_be32(const std::vector<uint8_t>& d, size_t off) {
    if (off + 3 >= d.size()) return 0ul;
    return ((unsigned long)d[off] << 24) | ((unsigned long)d[off + 1] << 16)
         | ((unsigned long)d[off + 2] << 8) | (unsigned long)d[off + 3];
}

//! shared prologue for the {type, index} read-side commands: send it, prove
//! it was answered as an AEM response with the right status, cdl and echoes.
//! Returns false when the frame is too short to grade a value out of, so a
//! caller never indexes into a truncated answer.
static bool grade_ti_head(const char* tag, const std::vector<uint8_t>& r,
                          uint16_t op, uint16_t seq, unsigned ty, unsigned ix,
                          unsigned want_cdl) {
    char w[144];
    snprintf(w, sizeof w, "%s: ANSWERED, not silence", tag);
    ck(w, (long)(r.size() >= 46), 1);
    if (r.size() < 46) return false;
    snprintf(w, sizeof w, "%s: an AEM_RESPONSE (message_type 1)", tag);
    ck(w, r[15] & 0x0F, 1);
    snprintf(w, sizeof w, "%s: status SUCCESS(0)", tag);
    ck(w, aecp_status(r), 0);
    snprintf(w, sizeof w, "%s: sequence_id echoed", tag);
    ck(w, ((unsigned)r[34] << 8) | r[35], seq);
    snprintf(w, sizeof w, "%s: command_type echoed, u = 0", tag);
    ck(w, ((unsigned)r[36] << 8) | r[37], op);
    snprintf(w, sizeof w, "%s: control_data_length is the clause's", tag);
    ck(w, (((unsigned)r[16] & 7) << 8) | r[17], (long)want_cdl);
    snprintf(w, sizeof w, "%s: descriptor_type @24 echoed", tag);
    ck(w, ((unsigned)r[38] << 8) | r[39], (long)ty);
    snprintf(w, sizeof w, "%s: descriptor_index @26 echoed", tag);
    ck(w, ((unsigned)r[40] << 8) | r[41], (long)ix);
    return true;
}

// AAF PDU: sid = 8 wire bytes, chans = wire channels_per_frame
static const uint8_t* mkaaf(const uint8_t sid[8], uint8_t seq, uint8_t chans,
                            uint8_t pay0) {
    static uint8_t f[120];
    memset(f, 0, sizeof f);
    const uint8_t dmac[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
    memcpy(f, dmac, 6);
    memcpy(f+6, sid, 6);                       // src MAC = sid MAC half
    f[12]=0x22; f[13]=0xF0;
    f[14]=0x02;                                // AAF
    f[15]=0x81;                                // sv, tv
    f[16]=seq;
    memcpy(f+18, sid, 8);
    f[26]=0x00; f[27]=0x00; f[28]=0x10; f[29]=0x00;  // avtp_ts = 0x1000 (not late/early)
    f[30]=0x02;                                // format INT32
    f[31]=(uint8_t)(0x05 << 4);                // nsr = 48 kHz
    f[32]=chans;
    f[33]=32;                                  // bit depth
    f[34]=0x00; f[35]=0x30;                    // data_len 48
    for (int i = 0; i < 48; i++) f[38+i] = (uint8_t)(pay0 + i);
    return f;
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    dut = new Vmilan_datapath;

    printf("=== milan_datapath NxN integration (N_STREAMS=%d, P12) ===\n",
           NSTREAMS_TB);
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
    dut->s_axi_bready = dut->s_axi_rready = 0;
    dut->s_axis_tx_tvalid = 0; dut->s_axis_mac_rx_tvalid = 0;
    dut->m_axis_mac_tx_tready = 1; dut->m_axis_rx_tready = 1;
    dut->m_axis_ts_tready = 1; dut->m_axis_pcm_tready = 1;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1;
    dut->i_mac_events = 0;
    for (int i = 0; i < 8; i++) step();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    for (int i = 0; i < 8; i++) step();

    ck("ID == 'MILN'", axi_read(A_ID), 0x4D494C4E);
    ck("VERSION 0x0021 (the TSpec describes the frame this build emits)",
       axi_read(A_VERSION), 0x0002004E);

    //! ENTITY IDENTITY, PROVISIONED ONCE AND EARLY (moved here 2026-08-13).
    //! These two writes used to sit inside the N-sink ACMP ctx2 section,
    //! which is deleted with the 0x800 ACMP table it graded - and every
    //! later section that talks ACMP depends on them: the processor's
    //! talker discriminates a PROBE_TX on target_eid == own entity_id, and
    //! its listener discriminates a CONNECT_RX_COMMAND on listener_entity_id.
    //! Against the CSR's zero reset value both of those match nothing, so a
    //! bench that leaves them unset gets silence and cannot tell it from a
    //! broken responder.
    axi_write(A_ADP_EIDHI, 0x020000FF);
    axi_write(A_ADP_EIDLO, 0xFE000001);      // 02:00:00:FF:FE:00:00:01
    for (int c = 0; c < 16; c++) step();

    //! [AECP] THIS LEG STARTS WITH NO DESCRIPTOR MEMORY, ON PURPOSE AND ON
    //! RECORD. milan_datapath exposes nine ports for the AEM descriptor image
    //! the AECP store fetches (o_desc_mem_req_valid / i_desc_mem_req_ready /
    //! o_desc_mem_req_addr / o_desc_mem_req_beats / i_desc_mem_rsp_valid /
    //! o_desc_mem_rsp_ready / i_desc_mem_rsp_data / i_desc_mem_rsp_last /
    //! i_desc_mem_rsp_err). Driving req_ready LOW is not neutral: it is
    //! KL_aecp_desc_store's documented degrade path - the watchdog abandons
    //! the burst, the image never validates, and READ_DESCRIPTOR comes back
    //! well formed but empty-handed. That is legal, and it is what this
    //! section grades. A zero left at a port by accident and a zero driven by
    //! a decision look identical on a waveform, so the decision is named.
    //!
    //! WHAT THIS ARM CANNOT CATCH, AND WHAT THAT COST. While it was the ONLY
    //! arm, a control plane that never transacted on those nine ports passed
    //! here - "never transacts" and "no memory offered" are the same
    //! waveform - and that is exactly what reached silicon on 2026-08-13.
    //! [AECP-IMG] below is the opposite arm: a memory that ANSWERS, the image
    //! the build ships, img_valid, and byte-exact descriptors on the wire.
    dm_answering = false;
    {
        std::vector<uint8_t> pl = {0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00};
        auto r = aecp_xact(0x0004, 0x4000, pl);   // READ_DESCRIPTOR(ENTITY,0)
        ck("[AECP] READ_DESCRIPTOR with no descriptor memory still ANSWERS",
           (long)(r.size() >= 38), 1);
        if (r.size() >= 38) {
            ck("[AECP] ...as an AEM_RESPONSE (message_type 1)",
               r[15] & 0x0F, 1);
            //! the store never validated an image, so configurations_count
            //! reads 0 and the uCPU's range check answers BAD_ARGUMENTS
            //! before it ever locates - not NO_SUCH_DESCRIPTOR
            ck("[AECP] ...with BAD_ARGUMENTS(7): configurations_count is 0",
               aecp_status(r), 7);
            ck("[AECP] ...carrying the 7.4.5 stub (cdl = 12 + 8)",
               (long)((((unsigned)r[16] & 7) << 8) | r[17]), 20);
            ck("[AECP] ...padded to the 60-octet Ethernet minimum",
               (long)r.size(), 60);
        }
    }

    //! [AECP-WTMO] THE RESPONSE MEMORY STOPS ANSWERING - AND THE STATION
    //! MUST REPORT, NOT WEDGE. The 2026-08-13 board defect was exactly this
    //! shape and nothing in this tree could have caught it: the bridge that
    //! stands where `rm_answering` stands here left its bus states only on
    //! `ack`, so ONE unanswered access parked it forever, silently. What made
    //! it lethal rather than local is the arbiter: the dma_bus re-arbitrates
    //! only when nothing is outstanding, so a master holding cyc/stb freezes
    //! every other master on that bus. The visible half of the fix is graded
    //! here - a memory that never acks must produce a well-formed
    //! ENTITY_MISBEHAVING and then HEAL, with no reset anywhere - and the
    //! bridge FSM that has to survive it is graded in
    //! sw/litex/test_pp_mem_bridge.py, which is where that FSM lives.
    //!
    //! This is the SAME degradation pp_shadow's section [N] grades on the bare
    //! processor, driven here through the whole datapath instead: real RX
    //! classify, the shared control TX lane, the real frame builder.
    {
        rm_answering = false;
        std::vector<uint8_t> pl = {0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00};
        auto r = aecp_xact(0x0004, 0x4001, pl);
        ck("[AECP-WTMO] a memory that NEVER ACKS still gets an ANSWER",
           (long)(r.size() >= 38), 1);
        if (r.size() >= 38) {
            ck("[AECP-WTMO] ...still an AEM_RESPONSE (message_type 1)",
               r[15] & 0x0F, 1);
            //! the buffer's write watchdog voided the response, so the engine
            //! answers the ONE status that says "I could not build it"
            ck("[AECP-WTMO] ...with ENTITY_MISBEHAVING(10), the documented "
               "degradation", aecp_status(r), 10);
            ck("[AECP-WTMO] ...carrying no payload it could not build "
               "(cdl = 12)",
               (long)((((unsigned)r[16] & 7) << 8) | r[17]), 12);
            ck("[AECP-WTMO] ...still padded to the 60-octet minimum",
               (long)r.size(), 60);
        }
        //! ...and the fault is PER-COMMAND, not sticky: the buffer clears on
        //! the next open, so the very next command answers as it did before
        //! the memory went away. A wedge would fail HERE even if the check
        //! above passed on a lucky first frame.
        rm_answering = true;
        auto r2 = aecp_xact(0x0004, 0x4002, pl);
        ck("[AECP-WTMO] the station HEALS when the memory returns (no reset)",
           (long)(r2.size() >= 38 && aecp_status(r2) == 7), 1);
    }

    //! [AECP-IMG] THE DESCRIPTOR MEMORY ANSWERS - AND THE ENTITY ENUMERATES.
    //!
    //! THE ARM THAT WAS MISSING, AND THE REASON THIS SECTION EXISTS. Above
    //! this line the suite proves a station that DEGRADES well: no memory
    //! gives a well-formed BAD_ARGUMENTS, a wedged memory gives a well-formed
    //! ENTITY_MISBEHAVING that heals. NEITHER can go red against a control
    //! plane that never transacts on the descriptor ports at all, because
    //! that is the stimulus both of them apply. The 2026-08-13 board shipped
    //! with exactly that: img_valid 0, descriptor-store fault 8, and the
    //! response memory's dbg_lane_wr parked at 2 where a plane that reports
    //! reaches 17 on the same traffic. Every gate was green.
    //!
    //! So this grades the SUCCESS path, which is the whole supply chain:
    //!   1. the image the BUILD SHIPS - regenerated here by the same
    //!      avdecc/gen_aemi_image.py that sw/litex loads at PP_DESC_BASE_P -
    //!      served out of a memory with real miss latency and real bubbles;
    //!   2. the store VALIDATES it: snapshot word 34 bit 0 (img_valid) with
    //!      the fault nibble [4:1] at 0, read through the 0x920 side port;
    //!   3. READ_DESCRIPTOR answers SUCCESS with the right control_data_
    //!      length, and the descriptor bytes on the wire are the image's byte
    //!      for byte - including at a NON-ZERO index, which is the only way
    //!      the locate arithmetic is exercised at all;
    //!   4. the response-memory master COMMITTED the lanes those bytes need.
    //!      A write path that silently drops still produces a plausible frame
    //!      the moment the response fits in what it did manage to write.
    {
        std::string why;
        const bool built = aemi_load(AEMI_CFG_C, &why);
        ck("[AECP-IMG] the shipped generator emitted an image",
           (long)built, 1);
        if (!built) printf("  [i]    %s\n", why.c_str());

        if (built) {
            printf("  [i]    image: %ld bytes, %ld descriptors\n",
                   (long)desc_img.size(), (long)desc_want.size());
            //! the magic is the first thing the store looks for at
            //! PP_DESC_BASE_P, so a generator that quietly emitted something
            //! else would fail every check below for the wrong reason
            uint32_t magic = 0;
            for (int i = 0; i < 4 && i < (int)desc_img.size(); i++)
                magic = (magic << 8) | desc_img[i];
            ck("[AECP-IMG] ...beginning with the AEMI magic", magic,
               0x41454D49);

            //! THE MEMORY ARRIVES, and it never leaves again: a board does
            //! not lose its DRAM halfway through a session, and every later
            //! section reads the datapath with the plane in its shipping
            //! condition.
            dm_answering = true;

            //! THE SIDE PORT FIRST, so that a zero out of word 34 later can
            //! only mean "the store rejected the image" and never "this
            //! window reads zero".
            bool spok = false;
            ck("[AECP-IMG] the snapshot window answers ('KLPP')",
               sp_read(SP_SNAPSHOT + 0, &spok), 0x4B4C5050);
            ck("[AECP-IMG] ...over a posted access that did not error",
               (long)spok, 1);

            //! ---- the descriptors on the wire -----------------------------
            //! NO RESET ANYWHERE, AND ONE COMMAND IS ALL IT TAKES. The store
            //! is parked in S_BAD with FAULT_TIMEOUT from the two sections
            //! above and it re-probes on no timer: an image that never
            //! validated re-arms its header walk after every state-port read
            //! (KL_aecp_desc_store.sv S_ANSWER, "a late software load heals
            //! with no reset"), and the µCPU STALLS on the store while that
            //! walk runs. So the very first command after the memory appears
            //! is already served, which is the healing claim in the strongest
            //! form it can be stated: a controller that retries once
            //! enumerates. MEASURED across that one command: 3 bursts and 75
            //! beats, being the 32-byte header, the 16-entry index map, and
            //! the 312-byte ENTITY line it then served.
            //!
            //! dbg_lane_wr is CUMULATIVE and [AECP-WTMO] already moved the
            //! error counter beside it, so both are graded as DELTAS across
            //! the two reads below. Word 35 is {rerr[15:0], lane_wr[15:0]}.
            const uint32_t w35_0 = sp_read(SP_SNAPSHOT + 35, &spok);
            const size_t ent_len =
                grade_read_desc("[AECP-IMG] ENTITY,0", 0x0000, 0, 0x4011);
            const uint32_t w35_1 = sp_read(SP_SNAPSHOT + 35, &spok);

            //! ...and WHY it was served, read back rather than assumed. A
            //! served descriptor with img_valid still 0 would be the store
            //! answering out of stale line-buffer contents.
            const uint32_t w34 = sp_read(SP_SNAPSHOT + 34, &spok);
            printf("  [i]    desc-store word 34 = 0x%08X after %ld burst(s), "
                   "%ld beat(s)\n", w34, dm_bursts, dm_beats);
            ck("[AECP-IMG] the store FETCHED from descriptor memory",
               (long)(dm_bursts > 0), 1);
            ck("[AECP-IMG] the image VALIDATED (word 34 bit 0)", w34 & 1u, 1);
            ck("[AECP-IMG] ...with no store fault (word 34 [4:1])",
               (w34 >> 1) & 0xFu, 0);
            //! INDEX 1, and a STREAM_INPUT on purpose. This end-station puts
            //! its media sink and its CRF sink both under STREAM_INPUT at
            //! different lengths, so the image emits them as two index runs
            //! and index 1 can only be served by subtracting the run base
            //! (KL_aecp_desc_store.sv scan_base_r). An index-0-only test
            //! never touches that arithmetic.
            const size_t si_len =
                grade_read_desc("[AECP-IMG] STREAM_INPUT,1", 0x0005, 1, 0x4012);
            const uint32_t w35_2 = sp_read(SP_SNAPSHOT + 35, &spok);

            const long lane_ent = (long)((w35_1 & 0xFFFFu) - (w35_0 & 0xFFFFu));
            const long lane_si  = (long)((w35_2 & 0xFFFFu) - (w35_1 & 0xFFFFu));
            printf("  [i]    response-memory lane writes: +%ld for ENTITY "
                   "(%ld B), +%ld for STREAM_INPUT 1 (%ld B)\n",
                   lane_ent, (long)ent_len, lane_si, (long)si_len);
            //! THE FLOOR IS THE PAYLOAD, not the DUT's accounting: 4 + the
            //! descriptor has to reach memory eight bytes at a time, so
            //! anything below (4 + len) / 8 commits means bytes never got
            //! there. The board's stuck 2 fails this by a factor of twenty.
            ck("[AECP-IMG] the response memory COMMITTED the ENTITY lanes",
               (long)(lane_ent >= (long)((4 + ent_len) / 8)), 1);
            ck("[AECP-IMG] ...and committed STREAM_INPUT 1's as well",
               (long)(lane_si >= (long)((4 + si_len) / 8)), 1);
            //! rerr counts responses the memory VOIDED. [AECP-WTMO] added one
            //! deliberately, so only the delta across a working memory is
            //! honest here.
            ck("[AECP-IMG] no response was voided by the memory",
               (long)((w35_2 >> 16) - (w35_0 >> 16)), 0);
            ck("[AECP-IMG] the response buffer reports no fault (word 36)",
               sp_read(SP_SNAPSHOT + 36, &spok) & 0x7u, 0);

            // ---- [AECP-MODEL] every command, against the whole model ----
            // The two spot-checks above proved the store serves A descriptor.
            // This proves it serves THE MODEL: every row the generator
            // emitted, then each read-side command against the field of the
            // descriptor its clause names. See the banner on grade_ti_head.
            {
                uint16_t sq = 0x4100;
                long rows = 0, worst_short = 0;
                for (std::map<uint32_t, std::vector<uint8_t> >::const_iterator
                         it = desc_want.begin(); it != desc_want.end(); ++it) {
                    const unsigned ty = (unsigned)(it->first >> 16);
                    const unsigned ix = (unsigned)(it->first & 0xFFFFu);
                    char tag[96];
                    snprintf(tag, sizeof tag,
                             "[AECP-MODEL] READ_DESCRIPTOR type %#06x index %u",
                             ty, ix);
                    if (grade_read_desc(tag, ty, ix, sq++) == 0) worst_short++;
                    rows++;
                }
                printf("  [i]    model-driven READ_DESCRIPTOR: %ld of the "
                       "generator's %ld descriptors served\n",
                       rows - worst_short, rows);
                //! a model with nothing in it would sail through the loop
                //! above having proved nothing at all - the vacuity check
                ck("[AECP-MODEL] the generated model is not empty",
                   (long)(rows >= 8), 1);

                // ---- GET_CONFIGURATION vs ENTITY.current_configuration ----
                const std::vector<uint8_t>* ent = desc_of(0x0000, 0);
                ck("[AECP-MODEL] the model HAS an ENTITY descriptor",
                   (long)(ent != nullptr), 1);
                if (ent && ent->size() >= 312) {
                    const unsigned want_cfg = model_be16(*ent, 310);
                    const std::vector<uint8_t> r =
                        aecp_xact(0x0007, sq, std::vector<uint8_t>());
                    char t[96];
                    snprintf(t, sizeof t, "[AECP-MODEL] GET_CONFIGURATION");
                    if (r.size() >= 42) {
                        char w[144];
                        snprintf(w, sizeof w, "%s: ANSWERED", t);
                        ck(w, (long)(r.size() >= 42), 1);
                        snprintf(w, sizeof w, "%s: status SUCCESS(0)", t);
                        ck(w, aecp_status(r), 0);
                        snprintf(w, sizeof w, "%s: cdl 16 (IEEE 7.4.8.2)", t);
                        ck(w, (((unsigned)r[16] & 7) << 8) | r[17], 16);
                        snprintf(w, sizeof w, "%s: reserved @24 is zero", t);
                        ck(w, ((unsigned)r[38] << 8) | r[39], 0);
                        snprintf(w, sizeof w,
                                 "%s: configuration_index IS the model's "
                                 "ENTITY.current_configuration", t);
                        ck(w, ((unsigned)r[40] << 8) | r[41], (long)want_cfg);
                    } else {
                        ck("[AECP-MODEL] GET_CONFIGURATION: ANSWERED",
                           (long)r.size(), 42);
                    }
                    sq++;
                }

                // ---- GET_SAMPLING_RATE vs AUDIO_UNIT.current_sampling_rate
                for (unsigned ix = 0; ix < 4; ix++) {
                    const std::vector<uint8_t>* au = desc_of(0x0002, ix);
                    if (!au) continue;
                    char t[96];
                    snprintf(t, sizeof t,
                             "[AECP-MODEL] GET_SAMPLING_RATE AUDIO_UNIT %u",
                             ix);
                    std::vector<uint8_t> pl(4, 0);
                    pl[0] = 0x00; pl[1] = 0x02;
                    pl[2] = (uint8_t)(ix >> 8); pl[3] = (uint8_t)ix;
                    const std::vector<uint8_t> r = aecp_xact(0x0015, sq, pl);
                    if (grade_ti_head(t, r, 0x0015, sq, 0x0002, ix, 20)
                        && r.size() >= 46) {
                        char w[144];
                        const unsigned long want_sr = model_be32(*au, 136);
                        snprintf(w, sizeof w,
                                 "%s: sampling_rate IS the model's "
                                 "current_sampling_rate (%lu)", t, want_sr);
                        ck(w, (long)model_be32(
                                  std::vector<uint8_t>(r.begin() + 42,
                                                       r.end()), 0),
                           (long)want_sr);
                        //! ...and it is a rate the model actually declares.
                        //! A device answering a plausible-but-undeclared rate
                        //! passes the compare above only if the model says so.
                        ck("[AECP-MODEL] ...and the model's rate is non-zero",
                           (long)(want_sr > 0), 1);
                    }
                    sq++;
                }

                // ---- GET_CLOCK_SOURCE vs CLOCK_DOMAIN.clock_source_index --
                for (unsigned ix = 0; ix < 4; ix++) {
                    const std::vector<uint8_t>* cd = desc_of(0x0024, ix);
                    if (!cd) continue;
                    char t[96];
                    snprintf(t, sizeof t,
                             "[AECP-MODEL] GET_CLOCK_SOURCE CLOCK_DOMAIN %u",
                             ix);
                    std::vector<uint8_t> pl(4, 0);
                    pl[0] = 0x00; pl[1] = 0x24;
                    pl[2] = (uint8_t)(ix >> 8); pl[3] = (uint8_t)ix;
                    const std::vector<uint8_t> r = aecp_xact(0x0017, sq, pl);
                    if (grade_ti_head(t, r, 0x0017, sq, 0x0024, ix, 20)
                        && r.size() >= 48) {
                        char w[144];
                        snprintf(w, sizeof w,
                                 "%s: clock_source_index IS the model's", t);
                        ck(w, ((unsigned)r[42] << 8) | r[43],
                           (long)model_be16(*cd, 70));
                        snprintf(w, sizeof w, "%s: reserved @30 is zero", t);
                        ck(w, ((unsigned)r[44] << 8) | r[45], 0);
                    }
                    sq++;
                }

                // ---- GET_STREAM_FORMAT: shape only, and why --------------
                for (unsigned ty = 0x0005; ty <= 0x0006; ty++) {
                    for (unsigned ix = 0; ix < 4; ix++) {
                        if (!desc_of(ty, ix)) continue;
                        char t[96];
                        snprintf(t, sizeof t,
                                 "[AECP-MODEL] GET_STREAM_FORMAT %#06x/%u",
                                 ty, ix);
                        std::vector<uint8_t> pl(4, 0);
                        pl[0] = (uint8_t)(ty >> 8); pl[1] = (uint8_t)ty;
                        pl[2] = (uint8_t)(ix >> 8); pl[3] = (uint8_t)ix;
                        const std::vector<uint8_t> r =
                            aecp_xact(0x0009, sq, pl);
                        grade_ti_head(t, r, 0x0009, sq, ty, ix, 24);
                        sq++;
                    }
                }

                // ---- ENTITY_AVAILABLE: the liveness probe (es-4.2) --------
                {
                    const std::vector<uint8_t> r =
                        aecp_xact(0x0002, sq, std::vector<uint8_t>());
                    ck("[AECP-MODEL] ENTITY_AVAILABLE: ANSWERED",
                       (long)(r.size() >= 58), 1);
                    if (r.size() >= 58) {
                        ck("[AECP-MODEL] ENTITY_AVAILABLE: status SUCCESS(0)",
                           aecp_status(r), 0);
                        ck("[AECP-MODEL] ENTITY_AVAILABLE: cdl 32 (7.4.3.2)",
                           (((unsigned)r[16] & 7) << 8) | r[17], 32);
                        //! Milan D7 forbids ever granting ACQUIRE, so
                        //! ENTITY_ACQUIRED and acquired_controller_id are
                        //! structurally zero on a compliant Milan device -
                        //! not merely zero because nothing acquired it yet
                        ck("[AECP-MODEL] ...ENTITY_ACQUIRED is clear (Milan D7)",
                           (long)(model_be32(std::vector<uint8_t>(
                                      r.begin() + 38, r.end()), 0) & 1ul), 0);
                        long acq = 0;
                        for (int i = 0; i < 8; i++) if (r[42 + i]) acq++;
                        ck("[AECP-MODEL] ...acquired_controller_id is zero",
                           acq, 0);
                    }
                    sq++;
                }

                // ---- THE NEGATIVE ORACLE: one past the end of the model ---
                // desc_of() returning nullptr IS the model saying "absent",
                // so the whole type space gets a miss oracle for free. A
                // device that answers SUCCESS for a descriptor its own model
                // does not declare is the failure this catches.
                {
                    const unsigned tys[] = {0x0000, 0x0002, 0x0005, 0x0006,
                                            0x0009, 0x0024};
                    long probed = 0;
                    for (unsigned k = 0; k < sizeof tys / sizeof tys[0]; k++) {
                        unsigned ix = 0;
                        while (ix < 64 && desc_of(tys[k], ix)) ix++;
                        if (ix == 0 || ix >= 64) continue;   // absent type
                        std::vector<uint8_t> pl(8, 0);
                        pl[4] = (uint8_t)(tys[k] >> 8); pl[5] = (uint8_t)tys[k];
                        pl[6] = (uint8_t)(ix >> 8);      pl[7] = (uint8_t)ix;
                        const std::vector<uint8_t> r =
                            aecp_xact(0x0004, sq++, pl);
                        char w[144];
                        snprintf(w, sizeof w,
                                 "[AECP-MODEL] type %#06x index %u is NOT in "
                                 "the model and refuses NO_SUCH_DESCRIPTOR",
                                 tys[k], ix);
                        ck(w, (long)(r.size() >= 18 ? aecp_status(r) : -1), 2);
                        probed++;
                    }
                    ck("[AECP-MODEL] the negative oracle actually probed",
                       (long)(probed >= 3), 1);
                }
            }
        }
    }

#ifdef AAF_PB_TB
    // ---- task #26 (0x002C): THE BOOT SEEDER IS GONE WITH THE AEM PLANE ----
    //      REPOINTED 2026-08-13, and this is a CAPABILITY REGRESSION, named.
    //      This check used to prove the AECP builder had walked the declared
    //      identity image into the capture map RAM during its post-reset IDLE
    //      cycles, so key 0 read the declared RING template 0x1300 with
    //      0x900[0] never written - the "in-circuit by construction" law.
    //      That builder is deleted: milan_datapath.sv now reads
    //      `assign aecp_odmap_wr_p_w = 1'b0; assign aecp_odmap_dyn_w = 1'b0;`
    //      so there is no writer AND no seeder, the RAM stays empty forever,
    //      and `cap_xbar_live_w = aecp_odmap_dyn_w | cfg_chmap_enable`
    //      collapses to CHMAP_CTRL[0] alone.
    //
    //      The RTL treats this as its documented STATIC-shape arm rather than
    //      as breakage (milan_datapath.sv:1238-1252): with the crossbar
    //      bypassed the DECLARED front-end routing stays wired straight to the
    //      packetizer, so talkers do NOT wake streaming an empty map's
    //      silence - the pb/loopback sections below frame real audio through
    //      that path. What is genuinely lost is runtime remapping without a
    //      software arm; [T66] below grades what replaced it.
    //
    //      So the two checks become the two halves of the new structural
    //      truth, and neither is vacuous: the READ mux is still live (bit 26
    //      valid) and the RAM is EMPTY. The day a seeder returns - in any
    //      form - the second one fails and this block must be restored.
    {
        axi_write(0x904, 0x100);             // capture side, key 0
        axi_write(0x910, 1);
        uint32_t sv = 0;
        for (int g = 0; g < 64; g++) {
            sv = axi_read(0x910);
            if ((sv & 1) == 0) break;
        }
        uint32_t seed0 = axi_read(0x914);
        ck("0x002C: the capture-map READ mux is still live (bit 26)",
           (seed0 >> 26) & 1, 1);
        ck("0x002C: key 0 is EMPTY - no AEM seeder writes it any more",
           seed0 & 0x1FFF, 0x0);
        ck("0x002C: ...and CHMAP_CTRL[0] is 0, so the crossbar is BYPASSED "
           "and the declared front end is the power-on path",
           axi_read(0x900) & 1, 0);
    }
#endif

    // ==================================================================
    //  DELETED 2026-08-13: the 5.5.2.7 SRP-only licence at t>0 straight from reset.
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  DELETED 2026-08-13: the Milan 4.3.3.1 declaration gate (cold boot silent, probe opens, lapse withdraws).
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ---- THE ADVERTISED SHAPE AT N > 1 (2026-07-27) --------------------
    // The CRF Media Clock Output lives at talker_unique_id = N_STREAMS and
    // the CRF sink at listener_unique_id = N_STREAMS, so the entity has
    // N+1 sources and N+1 sinks. Nothing is written here: 0x618/0x61C are
    // read-only words hardwired from milan_datapath's ACMP_SRC_C /
    // ACMP_SINKS_C. On silicon these came from a boot script frozen at the
    // 1x1 shape, so the 8x8 board advertised 1 source / 2 sinks and the CRF
    // source was OUTSIDE the advertised range - the probe test further down
    // proves uid N answers SUCCESS, and this proves a controller is ever
    // told to ask.

    // stream_id wire bytes {03:00:00:00:00:03, uid 0x0001} / {04:.., uid 2}
    const uint8_t sidB[8] = {0x03,0x00,0x00,0x00,0x00,0x03,0x00,0x01};
    const uint8_t sidC[8] = {0x04,0x00,0x00,0x00,0x00,0x04,0x00,0x02};
    const uint8_t sidX[8] = {0x05,0x00,0x00,0x00,0x00,0x05,0x00,0x09};
    // AAF format u64 for {AAF, 48k, INT32, depth 32, up to 2 ch}
    const uint32_t FMT_HI = 0x02050220, FMT_LO = 2u << 22;

    printf("-- provision listener 1 (route=DMA flag) + 2 (route=NULL) via 0x800 --\n");
    axi_write(A_STRM_SEL, 0x001);                    // dir=0 idx=1
    axi_write(A_SW_SID_LO, 0x00030001);              // sidB[63:0] LSW
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_FMT_LO, FMT_LO);
    axi_write(A_SW_FMT_HI, FMT_HI);
    axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);        // en, DMA flag only
    // CFG readback through the ENGINE-ARBITRATED LCTX port B (real RAM)
    ck("LCTX w4 CTRL readback (port B)",  axi_read(A_SW_CTRL), 0x3);
    ck("LCTX w2 FMT_LO readback (port B)", axi_read(A_SW_FMT_LO), FMT_LO);
    ck("LCTX w3 FMT_HI readback (port B)", axi_read(A_SW_FMT_HI), FMT_HI);

    axi_write(A_STRM_SEL, 0x002);                    // dir=0 idx=2
    axi_write(A_SW_SID_LO, 0x00040002);
    axi_write(A_SW_SID_HI, 0x04000000);
    axi_write(A_SW_FMT_LO, FMT_LO);
    axi_write(A_SW_FMT_HI, FMT_HI);
    axi_write(A_SW_CTRL, 0x1);                       // en, route=NULL
    ck("stream 2 CTRL readback (port B)", axi_read(A_SW_CTRL), 0x1);

    printf("-- idx-0 alias protection: route-only CTRL commit (2026-07-23) --\n");
    {
        // a CTRL commit at idx 0 with NO staged sid must not arm the
        // stream-table override: before the fix it wrote {sid=0, en=1},
        // hijacking the live ACMP alias AND matching sid-0 frames
        axi_write(A_STRM_SEL, 0x000);                // dir=0 idx=0
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);    // en + DMA, sid NOT staged
        size_t before = pcm_frames.size();
        const uint8_t sid0[8] = {0,0,0,0,0,0,0,0};
        inject(mkaaf(sid0, 5, 2, 0x10), 120);        // sid 0 must NOT match
        ck("route-only idx0 commit: sid-0 frame ignored",
           pcm_frames.size(), before);
        // ...and it is now BLOCKED, not merely mis-aimed. The pre-2026-07-26
        // guard was `(|{wing_sid_hi_r, wing_sid_lo_r})` over a staging pair
        // that is GLOBAL, not per index: it still held listener 2's sid from
        // three writes earlier, so this route-only commit wrote the stream
        // table and armed entry 0 with SOMEBODY ELSE'S stream_id (armed count
        // 3). win_commit_glue now qualifies the staging with the index it was
        // staged for (`wing_stg_hit_w`), so a commit at idx 0 with nothing
        // staged FOR IDX 0 leaves the ACMP alias alone: 2 armed, not 3.
        ck("route-only idx0 commit leaves entry 0 on the ACMP alias",
           (axi_read(0x8C4) >> 16) & 0xFF, 2);
    }

    printf("-- tagged AAF frames: 3x stream1, 2x stream2, 1x unknown --\n");
    inject(mkaaf(sidB, 10, 2, 0x30), 120);
    inject(mkaaf(sidB, 11, 2, 0x40), 120);
    inject(mkaaf(sidB, 12, 2, 0x50), 120);
    inject(mkaaf(sidC, 77, 2, 0x60), 120);
    inject(mkaaf(sidC, 78, 2, 0x70), 120);
    inject(mkaaf(sidX, 99, 2, 0x00), 120);           // no table entry: ignored

    ck("PCM ring frames = 3 (stream 1 only)", pcm_frames.size(), 3);

    // ---- RX parser probe at width N (APRB 0x8B4) ------------------------
    // The last frame injected above carries sidX, which no table entry
    // holds: the probe must report it as PARSED-but-not-MATCHED and hand
    // back the stream_id it read off the wire. That pairing is what makes
    // the group usable on a listener that accepts nothing.
    {
        enum { A_APRB_PARSED = 0x8B4, A_APRB_MATCHED = 0x8B8,
               A_APRB_SIDLO = 0x8BC, A_APRB_SIDHI = 0x8C0,
               A_APRB_INFO = 0x8C4 };
        long parsed = axi_read(A_APRB_PARSED);
        long matched = axi_read(A_APRB_MATCHED);
        long info = axi_read(A_APRB_INFO);
        ck("APRB parsed > matched (unknown sid seen)", parsed > matched ? 1 : 0, 1);
        ck("APRB last frame did NOT match", (info >> 8) & 1, 0);
        ck("APRB last subtype = AAF", info & 0xFF, 0x02);
        uint64_t wire = ((uint64_t)axi_read(A_APRB_SIDHI) << 32)
                        | (uint32_t)axi_read(A_APRB_SIDLO);
        uint64_t want = 0;
        for (int i = 0; i < 8; i++) want = (want << 8) | sidX[i];
        ck("APRB last SID == the unmatched wire sid", wire == want ? 1 : 0, 1);
        // 2 = streams 1 and 2 provisioned above. Entry 0 is NOT counted: the
        // route-only commit no longer arms it, so it stays the ACMP alias.
        // The probe counts what is ARMED, which is exactly the distinction
        // that makes "armed but matching nothing" visible on silicon.
        ck("APRB armed entries = 2 (idx0 still the ACMP alias)",
           (info >> 16) & 0xFF, 2);
    }
    bool user_ok = true, pay_ok = true;
    for (auto& fr : pcm_frames) {
        if (fr.user != 1) user_ok = false;
        if (fr.bytes.size() != 48) pay_ok = false;
    }
    if (!pcm_frames.empty() && pay_ok)
        for (int i = 0; i < 48; i++)
            if (pcm_frames[0].bytes[i] != (uint8_t)(0x30+i)) pay_ok = false;
    ck("ring tuser == 1 on every frame", user_ok, 1);
    ck("48-byte payload, frame 0 byte-exact", pay_ok, 1);

    printf("-- SNAP isolation: per-stream Table 7-157 blocks --\n");
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("s1 CNT9 FRAMES_RX = 3", axi_read(A_SW_CNT0 + 9*4), 3);
    ck("s1 CNT0 MEDIA_LOCKED = 1", axi_read(A_SW_CNT0 + 0*4), 1);
    ck("s1 CNT3 SEQ_NUM_MISMATCH = 0", axi_read(A_SW_CNT0 + 3*4), 0);
    ck("s1 CNT6 UNSUPPORTED_FORMAT = 0", axi_read(A_SW_CNT0 + 6*4), 0);
    ck("s1 PDUS = {drops 0, pdus 3}", axi_read(A_SW_PDUS), 3);
    uint32_t st1 = axi_read(A_SW_STATE);
    ck("s1 STATE media_locked", (st1 >> 10) & 1, 1);
    ck("s1 STATE wire_chans = 2", (st1 >> 11) & 0xFF, 2);

    axi_write(A_STRM_SEL, 0x002);
    snap_and_wait();
    ck("s2 CNT9 FRAMES_RX = 2", axi_read(A_SW_CNT0 + 9*4), 2);
    ck("s2 PDUS = 2 (NULL still counted)", axi_read(A_SW_PDUS), 2);
    axi_write(A_STRM_SEL, 0x003);
    snap_and_wait();
    ck("s3 (unprovisioned) CNT9 = 0", axi_read(A_SW_CNT0 + 9*4), 0);
    // stream-0 legacy flat FRAMES_RX untouched by streams 1/2 traffic;
    // 0x6C4 is the SHARED depacketizer's global {drops,pdus} (all streams:
    // 3 + 2 = 5) - per-stream pdus live in the window PDUS word
    ck("legacy 0x6BC (s0 FRAMES_RX) = 0", axi_read(A_AVTPRX_FRX), 0);
    ck("legacy 0x6C4 = shared-depkt total 5", axi_read(A_PCMRX_CNT), 5);

    printf("-- seq gap on stream 1 moves ONLY stream 1 --\n");
    // drain the 8-PDU settle window first (mismatches are suppressed while
    // settle > 0, the flat-monitor rule): 6 more in-order PDUs = 9 total
    for (uint8_t s = 13; s <= 18; s++) inject(mkaaf(sidB, s, 2, 0x30), 120);
    inject(mkaaf(sidB, 21, 2, 0x30), 120);           // expected 19: lost 2
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("s1 CNT9 FRAMES_RX = 10", axi_read(A_SW_CNT0 + 9*4), 10);
    ck("s1 CNT3 SEQ_NUM_MISMATCH = 1", axi_read(A_SW_CNT0 + 3*4), 1);
    ck("s1 CNT2 STREAM_INTERRUPTED = 1", axi_read(A_SW_CNT0 + 2*4), 1);
    axi_write(A_STRM_SEL, 0x002);
    snap_and_wait();
    ck("s2 CNT3 still 0", axi_read(A_SW_CNT0 + 3*4), 0);
    ck("s2 CNT9 still 2", axi_read(A_SW_CNT0 + 9*4), 2);

    // ======================================================================
    //  GET_COUNTERS over the wire, against the CSR window that reads the
    //  same flops (1722.1-2021 7.4.42.2, Tables 7-156 and 7-157)
    // ======================================================================
    //! WHY HERE AND NOT IN A QUIETER SECTION. Stream 1 has just been driven
    //! to a state where its counters are DISTINCT: FRAMES_RX 10,
    //! SEQ_NUM_MISMATCH 1, STREAM_INTERRUPTED 1, MEDIA_LOCKED 1, and the rest
    //! zero. Against all-zero counters a block mux that permuted its inputs
    //! would look perfect, so a section that asked for the block before any
    //! traffic could not grade the mapping at all - only its shape.
    //!
    //! TWO INDEPENDENT READERS, TWO DIFFERENT ORDERS. The CSR window at
    //! A_SW_CNT0 publishes KL_avtp_rx_monitor_ctx's OWN order (CNT9 is
    //! FRAMES_RX, CNT6 is UNSUPPORTED_FORMAT - the tv pair was appended at 10
    //! and 11 after the rest). The wire must carry Table 7-157's order, which
    //! interleaves TIMESTAMP_VALID and TIMESTAMP_NOT_VALID at offsets 24 and
    //! 28, ahead of UNSUPPORTED_FORMAT at 32. milan_datapath's mux is the
    //! only thing between them, and this table states the correspondence a
    //! second time, from the standard, so the mux cannot be graded against
    //! itself.
    {
        printf("-- GET_COUNTERS: Table 7-157 block vs the CSR window --\n");
        static const struct { int q; int csr; const char* sym; } CTRMAP[] = {
            { 0,  0, "MEDIA_LOCKED"        },   // @0
            { 1,  1, "MEDIA_UNLOCKED"      },   // @4
            { 2,  2, "STREAM_INTERRUPTED"  },   // @8
            { 3,  3, "SEQ_NUM_MISMATCH"    },   // @12
            { 4,  4, "MEDIA_RESET"         },   // @16
            { 5,  5, "TIMESTAMP_UNCERTAIN" },   // @20
            // @24 TIMESTAMP_VALID and @28 TIMESTAMP_NOT_VALID have no CSR
            // twin: that window is ten words wide (A_SW_PDUS follows at
            // A_SW_CNT0 + 40) and the tv pair is not in it. They are graded
            // by their own invariant below instead of by comparison.
            { 8,  6, "UNSUPPORTED_FORMAT"  },   // @32
            { 9,  7, "LATE_TIMESTAMP"      },   // @36
            {10,  8, "EARLY_TIMESTAMP"     },   // @40
            {11,  9, "FRAMES_RX"           },   // @44
        };
        axi_write(A_STRM_SEL, 0x001);
        snap_and_wait();
        uint32_t csr[10];
        for (int k = 0; k < 10; k++) csr[k] = axi_read(A_SW_CNT0 + (uint16_t)(k*4));

        std::vector<uint8_t> pl(4, 0);
        pl[0] = 0x00; pl[1] = 0x05;                   // STREAM_INPUT, Table 7-4
        pl[2] = 0x00; pl[3] = 0x01;                   // index 1
        const std::vector<uint8_t> r = aecp_xact(0x0029, 0x4020, pl);
        ck("[CTRS] GET_COUNTERS(STREAM_INPUT,1) was ANSWERED",
           (long)(r.size() >= 174), 1);
        if (r.size() >= 174) {
            ck("[CTRS] status SUCCESS(0), not NOT_IMPLEMENTED", aecp_status(r), 0);
            ck("[CTRS] cdl = 12 + 136", (((unsigned)r[16] & 7) << 8) | r[17], 148);
            ck("[CTRS] the frame is as long as it claims", (long)r.size(), 174);
            ck("[CTRS] descriptor_type echoed", ((unsigned)r[38] << 8) | r[39], 5);
            ck("[CTRS] descriptor_index echoed", ((unsigned)r[40] << 8) | r[41], 1);
            const uint32_t mask = ((uint32_t)r[42] << 24) | ((uint32_t)r[43] << 16)
                                | ((uint32_t)r[44] << 8)  |  (uint32_t)r[45];
            ck("[CTRS] counters_valid = 0xFFF (quadlets 0..11)",
               (long)mask, 0x0FFF);

            auto blk = [&](int q) -> uint32_t {
                const size_t o = 46 + 4 * (size_t)q;
                return ((uint32_t)r[o] << 24) | ((uint32_t)r[o+1] << 16)
                     | ((uint32_t)r[o+2] << 8) | (uint32_t)r[o+3];
            };
            char w[128];
            for (size_t i = 0; i < sizeof CTRMAP / sizeof CTRMAP[0]; i++) {
                snprintf(w, sizeof w, "[CTRS] @%d %s == CSR CNT%d",
                         CTRMAP[i].q * 4, CTRMAP[i].sym, CTRMAP[i].csr);
                ck(w, (long)blk(CTRMAP[i].q), (long)csr[CTRMAP[i].csr]);
            }
            //! ...and the values are not all the same number, or the ten
            //! checks above would pass under ANY permutation. This is the
            //! term that makes them load-bearing.
            ck("[CTRS] the graded counters are DISTINCT, not a flat block",
               (long)(blk(11) != blk(3) && blk(11) != blk(8) && blk(11) != 0), 1);

            //! THE tv PAIR, by its own invariant. 7.4.42.2: TIMESTAMP_VALID
            //! increments on a Stream data AVTPDU with tv set and
            //! TIMESTAMP_NOT_VALID on one with it cleared, so across a run of
            //! frames the two must sum to FRAMES_RX. mkaaf sets tv, so the
            //! split is all-valid, and a mux that swapped @24 with @28 would
            //! put the whole tally on the wrong side of it.
            ck("[CTRS] @24 TIMESTAMP_VALID + @28 TIMESTAMP_NOT_VALID = FRAMES_RX",
               (long)(blk(6) + blk(7)), (long)blk(11));
            ck("[CTRS] @24 TIMESTAMP_VALID carries the tally (tv was set)",
               (long)blk(6), (long)blk(11));
            ck("[CTRS] @28 TIMESTAMP_NOT_VALID is zero", (long)blk(7), 0);

            //! Table 7-157 reserves @48..@92 and gives @96.. to
            //! ENTITY_SPECIFIC_1..8. Unclaimed in the mask above AND zero
            //! here: a claimed zero is the failure this face exists to stop.
            long dirty = 0;
            for (int q = 12; q < 32; q++) if (blk(q) != 0) dirty++;
            ck("[CTRS] the unclaimed quadlets 12..31 are zero", dirty, 0);
        }

        //! ------------------------------------------------------------------
        //! [CTRS-OUT] Milan Table 5.17 is not the IEEE Stream Output layout.
        //! It compacts the five mandatory counters into quadlets 0..4 and a
        //! mask of 0x1F. Drive the real admission gate through start and stop
        //! edges, then read the bank through the full processor and response
        //! path. The standalone tkdiag suite proves interval and wrap laws;
        //! this section proves the integration and wire positions.
        {
            auto sout = [&](uint16_t seq, uint16_t index) {
                std::vector<uint8_t> p = {0x00, 0x06,
                                          (uint8_t)(index >> 8),
                                          (uint8_t)index};
                return aecp_xact(0x0029, seq, p);
            };
            auto word = [](const std::vector<uint8_t>& f, int q) -> uint32_t {
                const size_t o = (q == 32) ? 42u : 46u + 4u * (size_t)q;
                if (f.size() < o + 4) return 0xDEADBEEFu;
                return ((uint32_t)f[o] << 24) | ((uint32_t)f[o+1] << 16)
                     | ((uint32_t)f[o+2] << 8) | (uint32_t)f[o+3];
            };

            bool shape_loaded = true;
            for (int out = 0; out <= NSTREAMS_TB; out++)
                shape_loaded &= desc_want.count((0x0006u << 16) |
                                                (uint32_t)out) == 1;
            shape_loaded &= desc_want.count((0x0006u << 16) |
                                            (uint32_t)(NSTREAMS_TB + 1)) == 0;
            ck("[CTRS-OUT] descriptor image matches this entity shape",
               shape_loaded, 1);

            auto r0 = sout(0x4022, 0);
            if (const char* frame_out = getenv("MILAN_COUNTER_FRAME_OUT")) {
                FILE* dump = fopen(frame_out, "wb");
                const size_t written = dump ? fwrite(r0.data(), 1, r0.size(), dump) : 0;
                if (dump) fclose(dump);
                ck("[CTRS-OUT] optional reference frame dump is complete",
                   written, r0.size());
            }
            ck("[CTRS-OUT] Stream Output 0 answers SUCCESS",
               (long)(!r0.empty() ? aecp_status(r0) : -1), 0);
            ck("[CTRS-OUT] Table 5.17 mask is compact 0x1F",
               (long)word(r0, 32), 0x1F);
            long all_outputs_ok = 1;
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4025 + out), (uint16_t)out);
                if (rr.empty() || aecp_status(rr) != 0 || word(rr, 32) != 0x1F)
                    all_outputs_ok = 0;
            }
            ck("[CTRS-OUT] every AAF and CRF output returns mask 0x1F",
               all_outputs_ok, 1);
            const auto no_such = sout(0x4030, (uint16_t)(NSTREAMS_TB + 1));
            ck("[CTRS-OUT] first undeclared output returns NO_SUCH_DESCRIPTOR",
               (long)(!no_such.empty() ? aecp_status(no_such) : -1), 2);
            ck("[CTRS-OUT] refusal keeps the full empty body",
               (long)(word(no_such, 32) == 0 && no_such.size() == 174), 1);

            //! Exercise both real enable surfaces. AAF has one global enable,
            //! so one transition moves every declared AAF output; CRF has its
            //! own enable and must move only the final Stream Output.
            axi_write(A_AAF_CTRL, 0x00020002);       // bypass, t0 disabled
            for (int out = 1; out < NSTREAMS_TB; out++) {
                axi_write(A_STRM_SEL, 0x100u | (uint32_t)out);
                axi_write(A_SW_CTRL, 0);
            }
            axi_write(A_CRFT_CTRL, 0);
            for (int i = 0; i < 32; i++) step();

            std::vector<uint32_t> start_base(NSTREAMS_TB + 1);
            std::vector<uint32_t> stop_base(NSTREAMS_TB + 1);
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4040 + out),
                                     (uint16_t)out);
                start_base[out] = word(rr, 0);
                stop_base[out] = word(rr, 1);
            }

            tkd_dirty_seen = 0;
            axi_write(A_AAF_CTRL, 0x00020003);
            axi_write(A_AAF_CTRL, 0x00020002);
            axi_write(A_CRFT_CTRL, 1);
            axi_write(A_CRFT_CTRL, 0);
            const unsigned long all_dirty = (1ul << (NSTREAMS_TB + 1)) - 1ul;
            ck("[CTRS-OUT] every output asserted its raw dirty bit",
               tkd_dirty_seen & all_dirty, all_dirty);
            long isolated = 1;
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4060 + out),
                                     (uint16_t)out);
                if (word(rr, 0) - start_base[out] != 1 ||
                    word(rr, 1) - stop_base[out] != 1)
                    isolated = 0;
            }
            ck("[CTRS-OUT] real start/stop edges reach every index",
               isolated, 1);
            const auto rbase = sout(0x4070, 0);
            const uint32_t start0 = word(rbase, 0);
            const uint32_t stop0 = word(rbase, 1);

            tkd_dirty_seen = 0;
            axi_write(A_AAF_CTRL, 0x00020003);       // enable + bypass
            axi_write(A_CRFT_CTRL, 1);               // real CRF output enable
            for (int i = 0; i < 32; i++) step();
            ck("[CTRS-OUT] composed Stream Output gate rose",
               tap_stream_en() & 1, 1);
            ck("[CTRS-OUT] start edge raised its descriptor dirty pulse",
               tkd_dirty_seen & 1, 1);
            auto r1 = sout(0x4023, 0);
            ck("[CTRS-OUT] STREAM_START incremented through the wire bank",
               (long)word(r1, 0), (long)(start0 + 1));
            ck("[CTRS-OUT] STREAM_STOP stayed unchanged while streaming",
               (long)word(r1, 1), (long)stop0);

            //! Drive every AAF context through the real packetizer and the
            //! CRF context through the real transmitter. The clock starts
            //! uncertain, so each declared output must advance q3 and q4.
            //! This checks the event sources at every high index, not only
            //! that the processor accepts a GET_COUNTERS request for it.
            ck("[CTRS-OUT] precondition: PHC verdict is uncertain",
               dut->rootp->milan_datapath__DOT__clkv_tu_w, 1);
            std::vector<uint32_t> real_mr0(NSTREAMS_TB + 1);
            std::vector<uint32_t> real_tu0(NSTREAMS_TB + 1);
            std::vector<uint32_t> real_ftx0(NSTREAMS_TB + 1);
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4071 + out),
                                     (uint16_t)out);
                real_mr0[out]  = word(rr, 2);
                real_tu0[out]  = word(rr, 3);
                real_ftx0[out] = word(rr, 4);
            }
            //! The CRF grid is one PDU per 96 audio samples, or 49,152
            //! harness clocks. Wait past that real cadence instead of using
            //! an AAF-only delay that could never observe a CRF completion.
            constexpr int RealPduWait = 52000;
            tkd_dirty_seen = 0;
            for (int i = 0; i < RealPduWait; i++) step();
            long all_real_tu_ftx = 1;
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4080 + out),
                                     (uint16_t)out);
                if (word(rr, 3) <= real_tu0[out] ||
                    word(rr, 4) <= real_ftx0[out])
                    all_real_tu_ftx = 0;
            }
            ck("[CTRS-OUT] real q3/q4 stimuli reach every AAF and CRF index",
               all_real_tu_ftx, 1);
            ck("[CTRS-OUT] every real FRAMES_TX source raises dirty",
               tkd_dirty_seen & all_dirty, all_dirty);

            //! Inject the media-clock target change at the actual restart
            //! engine. The next packetizer and CRF PDUs carry the new mr bit,
            //! then each diagnostic context and processor row must expose it.
            dut->rootp->milan_datapath__DOT__media_clock_restart__DOT__tgt_r ^= 1;
            step();
            for (int i = 0; i < RealPduWait; i++) step();
            long all_real_mr = 1;
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x4090 + out),
                                     (uint16_t)out);
                if (word(rr, 2) <= real_mr0[out]) all_real_mr = 0;
            }
            ck("[CTRS-OUT] real q2 stimulus reaches every AAF and CRF index",
               all_real_mr, 1);

            tkd_dirty_seen = 0;
            axi_write(A_AAF_CTRL, 0x00020002);       // bypass, disabled
            axi_write(A_CRFT_CTRL, 0);
            for (int i = 0; i < 512; i++) step();
            ck("[CTRS-OUT] composed Stream Output gate fell",
               tap_stream_en() & 1, 0);
            ck("[CTRS-OUT] stop edge raised its descriptor dirty pulse",
               tkd_dirty_seen & 1, 1);
            auto r2 = sout(0x4024, 0);
            ck("[CTRS-OUT] STREAM_START survives a stop",
               (long)word(r2, 0), (long)(start0 + 1));
            ck("[CTRS-OUT] STREAM_STOP incremented through the wire bank",
               (long)word(r2, 1), (long)(stop0 + 1));
            ck("[CTRS-OUT] stopped invariant START equals STOP",
               (long)word(r2, 0), (long)word(r2, 1));

            //! A real shared enable legitimately gives the AAF contexts the
            //! same START/STOP history. Seed distinct verification signatures
            //! only after all outputs stop, then traverse the real diagnostic
            //! read mux, processor request port, response builder, and wire
            //! decoder for every index. Any clamped or aliased row now fails.
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const uint32_t tag = 0x10000u * (uint32_t)(out + 1);
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__start_r[out]
                    = tag + 0x0101u;
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__stop_r[out]
                    = tag + 0x0202u;
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__mreset_r[out]
                    = tag + 0x0303u;
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__tuiv_r[out]
                    = tag + 0x0404u;
                dut->rootp->milan_datapath__DOT__talker_diag__DOT__ftx_r[out]
                    = tag + 0x0505u;
            }
            long every_row_isolated = 1;
            std::vector<uint8_t> last_sig;
            for (int out = 0; out <= NSTREAMS_TB; out++) {
                const auto rr = sout((uint16_t)(0x40A0 + out),
                                     (uint16_t)out);
                const uint32_t tag = 0x10000u * (uint32_t)(out + 1);
                for (int q = 0; q < 5; q++)
                    if (word(rr, q) != tag + 0x0101u * (uint32_t)(q + 1))
                        every_row_isolated = 0;
                last_sig = rr;
            }
            ck("[CTRS-OUT] every NxN row preserves its unique five-word signature",
               every_row_isolated, 1);

            long reserved_dirty = 0;
            for (int q = 5; q < 32; q++)
                if (word(last_sig, q) != 0) reserved_dirty++;
            ck("[CTRS-OUT] unclaimed quadlets 5..31 are zero",
               reserved_dirty, 0);

        }

        //! ------------------------------------------------------------------
        //! [CTRS2] AVB_INTERFACE and CLOCK_DOMAIN: the other two families
        //! la_avdecc's Milan gate demands (5.3.6.3 Table 5.1, 5.3.11.2
        //! Table 5.7). Graded as DELTAS around events THIS section fires, so
        //! nothing depends on how many times earlier sections moved the
        //! levels; the link pair is graded by its INVARIANT instead, because
        //! bouncing the link mid-suite would drag the eth domains through a
        //! reset every later section would pay for.
        {
            auto ctr_of = [&](unsigned ty, unsigned ix, int q) -> uint32_t {
                std::vector<uint8_t> p(4, 0);
                p[0] = (uint8_t)(ty >> 8); p[1] = (uint8_t)ty;
                p[2] = (uint8_t)(ix >> 8); p[3] = (uint8_t)ix;
                const std::vector<uint8_t> rr = aecp_xact(0x0029, 0x4030, p);
                if (rr.size() < 174) return 0xDEADBEEFu;
                const size_t o = (q == 32) ? 42u : 46u + 4u * (size_t)q;
                return ((uint32_t)rr[o] << 24) | ((uint32_t)rr[o+1] << 16)
                     | ((uint32_t)rr[o+2] << 8) | (uint32_t)rr[o+3];
            };

            // -- the interface family ---------------------------------------
            ck("[CTRS2] AVB_INTERFACE mask = 0x23 (LINK_UP, LINK_DOWN, "
               "GPTP_GM_CHANGED)", (long)ctr_of(0x0009, 0, 32), 0x23);
            const uint32_t lu = ctr_of(0x0009, 0, 0);
            const uint32_t ld = ctr_of(0x0009, 0, 1);
            //! 5.3.6.3's own invariant, held by construction (edges of one
            //! level): the link is UP while streams flow, so up = down + 1
            ck("[CTRS2] LINK_UP = LINK_DOWN + 1 (the link is up)",
               (long)lu, (long)(ld + 1));
            ck("[CTRS2] the link has risen at least once", (long)(lu >= 1), 1);

            // -- GPTP_GM_CHANGED, by delta ----------------------------------
            //! the strobe fires only when a NONZERO grandmaster identity
            //! changes (a first publication is a discovery, not a change) -
            //! so publish A, then move to B, and expect exactly the B edge
            const uint32_t gm0 = ctr_of(0x0009, 0, 5);
            //! the GM pair is COMMIT-ON-HI (milan_csr: "LO stages, HI
            //! commits both halves in one cycle") - a LO write alone changes
            //! NOTHING, which is the atomicity a torn 64-bit id would
            //! otherwise leak through. So every change here ends with an HI
            //! write. The first commit is a DISCOVERY (0 -> A) and must NOT
            //! count; the second (A -> B) is the change.
            axi_write(0x624, 0x00C0FFEEu);           // stage LO of gm A
            axi_write(0x628, 0x001BC500u);           // COMMIT gm A (discovery)
            snap_and_wait();
            axi_write(0x624, 0x00C0FFEFu);           // stage LO of gm B
            axi_write(0x628, 0x001BC500u);           // COMMIT gm B (the change)
            snap_and_wait();
            printf("  [i]    GMLO rb 0x%08X GMHI rb 0x%08X CLKV_STAT 0x%08X\n",
                   axi_read(0x624), axi_read(0x628), axi_read(0x77C));
            printf("  [i]    gmchg flop %u strobe %u\n",
                   (unsigned)dut->rootp->milan_datapath__DOT__ctr_gmchg_r,
                   (unsigned)dut->rootp->milan_datapath__DOT__pp_gm_change_p_w);
            const uint32_t gm1 = ctr_of(0x0009, 0, 5);
            ck("[CTRS2] GPTP_GM_CHANGED counted the A-to-B move",
               (long)(gm1 - gm0 >= 1), 1);

            // -- the clock-domain family, by delta --------------------------
            //! the GM commits above are gPTP DISCONTINUITIES to the clock
            //! validity block (gm_id_i != gm_r arms HOLD_QTICK_P = 2
            //! quarter-ticks of holdover, 4096 cycles each in this leg), and
            //! tu cannot fall while holdover runs. Drain it first, or the
            //! lock edge lands after the read that grades it.
            for (int i = 0; i < 15000; i++) step();
            const uint32_t lk0 = ctr_of(0x0024, 0, 0);
            const uint32_t ul0 = ctr_of(0x0024, 0, 1);
            ck("[CTRS2] CLOCK_DOMAIN mask = 0x3 (LOCKED, UNLOCKED)",
               (long)ctr_of(0x0024, 0, 32), 0x3);
            //! lock = the CLKV lease (0x778: [0] SYNC_OK, [15:4] lease in
            //! quarter-ticks; any write reloads). tu falls -> LOCKED++
            axi_write(0x778, (0xFFFu << 4) | 1u);
            snap_and_wait();
            printf("  [i]    after lease: CLKV_STAT 0x%08X\n", axi_read(0x77C));
            const uint32_t lk1 = ctr_of(0x0024, 0, 0);
            ck("[CTRS2] the lease LOCKED the domain (+1)",
               (long)(lk1 - lk0), 1);
            //! a reported gPTP discontinuity (bit 1, W1S) drops the verdict:
            //! tu rises -> UNLOCKED++ (write keeps SYNC_OK so the NEXT lease
            //! re-locks; here we only grade the unlock edge)
            axi_write(0x778, (0xFFFu << 4) | 2u | 1u);
            for (int i = 0; i < 32; i++) step();
            const uint32_t ul1 = ctr_of(0x0024, 0, 1);
            ck("[CTRS2] the discontinuity UNLOCKED the domain (+1)",
               (long)(ul1 - ul0 >= 1), 1);
            //! 5.3.11.2's invariant across whatever the two writes left
            const uint32_t lkf = ctr_of(0x0024, 0, 0);
            const uint32_t ulf = ctr_of(0x0024, 0, 1);
            ck("[CTRS2] LOCKED - UNLOCKED is 0 or 1 (the shall-invariant)",
               (long)(lkf - ulf <= 1), 1);

            // -- the unclaimed stay unclaimed -------------------------------
            //! FRAMES_TX/RX + RX_CRC_ERROR live in mac_rmon's domain: the
            //! mask must not claim them and the quadlets must read zero -
            //! a claimed-zero is the lie this face exists to prevent
            ck("[CTRS2] AVB_INTERFACE @8 FRAMES_TX unclaimed and zero",
               (long)ctr_of(0x0009, 0, 2), 0);
            //! index 1 of either family does not exist in this image, and
            //! the counters strictness round made the store the existence
            //! authority: NO_SUCH_DESCRIPTOR with the zero-flagged fixed
            //! body, never SUCCESS over an empty mask
            {
                std::vector<uint8_t> p1 = {0x00, 0x09, 0x00, 0x01};
                auto ra = aecp_xact(0x0029, 0x402E, p1);
                ck("[CTRS2] AVB_INTERFACE index 1 refuses NO_SUCH_DESCRIPTOR",
                   (long)(!ra.empty() ? ((ra[16] >> 3) & 0x1F) : -1), 2);
                ck("[CTRS2] ...with the zero mask in the fixed body",
                   (long)(ra.size() >= 174
                          ? (long)(((unsigned)ra[42] << 8) | ra[43]) : -1), 0);
                std::vector<uint8_t> p2 = {0x00, 0x24, 0x00, 0x01};
                auto rc = aecp_xact(0x0029, 0x402F, p2);
                ck("[CTRS2] CLOCK_DOMAIN index 1 refuses NO_SUCH_DESCRIPTOR",
                   (long)(!rc.empty() ? ((rc[16] >> 3) & 0x1F) : -1), 2);
            }
        }

        //! THE WRONG-OBJECT ANSWER, upgraded by the counters strictness
        //! round: ask one past this leg's matching NxN image. The monitor
        //! could physically clamp that index, but the store must refuse it
        //! as NO_SUCH_DESCRIPTOR with the fixed body zeroed. Sink 1 answering
        //! its own numbers above still proves no index leak.
        {
            const unsigned miss = NSTREAMS_TB + 1;
            std::vector<uint8_t> p2(4, 0);
            p2[1] = 0x05;
            p2[2] = (uint8_t)(miss >> 8); p2[3] = (uint8_t)miss;
            const std::vector<uint8_t> r2 = aecp_xact(0x0029, 0x4021, p2);
            ck("[CTRS] GET_COUNTERS(first undeclared Stream Input) answered",
               (long)(r2.size() >= 174), 1);
            if (r2.size() >= 174) {
                ck("[CTRS] first undeclared input returns NO_SUCH_DESCRIPTOR",
                   (long)((r2[16] >> 3) & 0x1F), 2);
                long dirty = 0;
                for (int q = 0; q < 32; q++) {
                    const size_t o = 46 + 4 * (size_t)q;
                    if (r2[o] | r2[o+1] | r2[o+2] | r2[o+3]) dirty++;
                }
                ck("[CTRS] ...and the block is all zeros, not a neighbour's",
                   dirty, 0);
            }
        }
    }

    // ======================================================================
    //  GET_AUDIO_MAP over the wire, against the CHMAP_LOOP readback that
    //  reads the same map RAM (1722.1-2021 7.4.44, Milan v1.2 5.4.2.26,
    //  the 0x001C global-cluster index law)
    // ======================================================================
    //! TWO INDEPENDENT READERS of the render map RAM: mappings are
    //! provisioned through the 0x900 CHMAP debug window, read back through
    //! CHMAP_SNAP/CHMAP_LOOP (0x910/0x914 - the RAM's own readback port),
    //! and then fetched over the wire with GET_AUDIO_MAP, whose answer
    //! block walks a SEPARATE flat export of the same flops. The wire
    //! records below are derived FROM the CHMAP_LOOP words, so a mux that
    //! served anything but the RAM disagrees with a reader it shares
    //! nothing with.
    //!
    //! GEOMETRY ACROSS LEGS: this file elaborates under the 4x4 header
    //! (4 channels -> 4 clusters/port) and the 8x8 header (8 -> 8), while
    //! the descriptor image is always the 1x1 config's (ONE
    //! STREAM_PORT_INPUT). Both provisioned clusters sit below 4 so every
    //! leg serves them; number_of_maps is 1 in every leg (page = clusters).
    {
        printf("-- GET_AUDIO_MAP: the wire vs the CHMAP_LOOP readback --\n");
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
               A_CHMAP_WORD = 0x908, A_CHMAP_SNAP = 0x910,
               A_CHMAP_LOOP = 0x914 };
        // provision: cluster 0 <- AVB {stream 1, ch 1}, cluster 2 <- AVB
        // {stream 0, ch 3}, cluster 1 <- HOST RING ch 5 (real routing that
        // must NOT appear as a 7.4.44.2.1 record), cluster 3 left unmapped
        axi_write(A_CHMAP_CTRL, 0x1);
        axi_write(A_CHMAP_SEL, 0);  axi_write(A_CHMAP_WORD, 0x8011);
        axi_write(A_CHMAP_SEL, 2);  axi_write(A_CHMAP_WORD, 0x8003);
        axi_write(A_CHMAP_SEL, 1);  axi_write(A_CHMAP_WORD, 0x9005);
        axi_write(A_CHMAP_CTRL, 0x0);

        auto loop_rd = [&](uint32_t k) -> uint32_t {
            axi_write(A_CHMAP_SEL, k);            // side 0 = RMAP
            axi_write(A_CHMAP_SNAP, 1);           // W1S arm
            for (int g = 0; g < 256; g++)
                if ((axi_read(A_CHMAP_SNAP) & 1) == 0) break;
            return axi_read(A_CHMAP_LOOP) & 0xFFu;
        };
        const uint32_t e0 = loop_rd(0), e1 = loop_rd(1), e2 = loop_rd(2),
                       e3 = loop_rd(3);
        ck("[AMAP] LOOP reads cluster 0 = {en, avb 1.1}", (long)e0, 0x89);
        ck("[AMAP] LOOP reads cluster 1 = {en, RING 5}",  (long)e1, 0xC5);
        ck("[AMAP] LOOP reads cluster 2 = {en, avb 0.3}", (long)e2, 0x83);
        ck("[AMAP] LOOP reads cluster 3 = unmapped",      (long)e3, 0x00);

        //! the model's own record, DERIVED from the LOOP word: an AVB entry
        //! ({en, src 0}) at global cluster g means {stream idx[5:3],
        //! channel idx[2:0], cluster_offset g (base 0 on port 0),
        //! cluster_channel 0 (mono clusters)}
        auto rec_of = [](uint32_t ent, uint32_t g, uint8_t* out) {
            out[0] = 0; out[1] = (uint8_t)((ent >> 3) & 7);
            out[2] = 0; out[3] = (uint8_t)(ent & 7);
            out[4] = 0; out[5] = (uint8_t)g;
            out[6] = 0; out[7] = 0;
        };

        std::vector<uint8_t> pl(8, 0);
        pl[1] = 0x0E;                                 // STREAM_PORT_INPUT 0
        const std::vector<uint8_t> r = aecp_xact(0x002B, 0x4030, pl);
        ck("[AMAP] GET_AUDIO_MAP(SPI 0, page 0) was ANSWERED",
           (long)(r.size() >= 60), 1);
        if (r.size() >= 60) {
            ck("[AMAP] status SUCCESS(0), not NOT_IMPLEMENTED",
               aecp_status(r), 0);
            ck("[AMAP] cdl = 24 + 8*2 (two records)",
               (long)((((unsigned)r[16] & 7) << 8) | r[17]), 40);
            ck("[AMAP] the frame is as long as it claims", (long)r.size(),
               66);
            ck("[AMAP] descriptor_type echoed",
               (long)(((unsigned)r[38] << 8) | r[39]), 0x000E);
            ck("[AMAP] descriptor_index echoed",
               (long)(((unsigned)r[40] << 8) | r[41]), 0);
            ck("[AMAP] map_index echoed",
               (long)(((unsigned)r[42] << 8) | r[43]), 0);
            ck("[AMAP] number_of_maps = the ONE fixed partition",
               (long)(((unsigned)r[44] << 8) | r[45]), 1);
            ck("[AMAP] number_of_mappings = 2 (the RING entry excluded)",
               (long)(((unsigned)r[46] << 8) | r[47]), 2);
            ck("[AMAP] reserved zero",
               (long)(((unsigned)r[48] << 8) | r[49]), 0);
            uint8_t want0[8], want1[8];
            rec_of(e0, 0, want0);
            rec_of(e2, 2, want1);
            long bad = 0;
            for (int i = 0; i < 8; i++) {
                if (r[50 + i] != want0[i]) bad++;
                if (r[58 + i] != want1[i]) bad++;
            }
            ck("[AMAP] both records equal the LOOP-derived expectation",
               bad, 0);
        }

        //! the 7.4.44.1 page rule: map_index 1 of a 1-page port
        pl[5] = 0x01;
        const std::vector<uint8_t> rb = aecp_xact(0x002B, 0x4031, pl);
        ck("[AMAP] page 1 answers BAD_ARGUMENTS(7)", aecp_status(rb), 7);
        ck("[AMAP] ...with the real number_of_maps and an EMPTY page",
           (long)(rb.size() >= 50
                  ? (long)((((unsigned)rb[44] << 8) | rb[45]) << 16
                           | (((unsigned)rb[46] << 8) | rb[47]))
                  : -1), 0x00010000);

        //! the image is the existence authority: probe the first SPI index
        //! absent from this leg's matching entity model
        unsigned spi_miss = 0;
        while (spi_miss < 64 && desc_of(0x000E, spi_miss)) spi_miss++;
        pl[5] = 0x00;
        pl[2] = (uint8_t)(spi_miss >> 8); pl[3] = (uint8_t)spi_miss;
        const std::vector<uint8_t> rn = aecp_xact(0x002B, 0x4032, pl);
        ck("[AMAP] first undeclared SPI returns NO_SUCH_DESCRIPTOR(2)",
           aecp_status(rn), 2);

        //! the STREAM_PORT_OUTPUT gap is RETIRED: the capture-side map RAM
        //! answers through the same face, routed by descriptor_type. This
        //! leg's capture map is empty here, so the honest answer is SUCCESS
        //! with the D8 role-pool page count (25 clusters -> 4 pages of 8)
        //! and an EMPTY page - the full 7.4.44.2 fixed part, cdl 24.
        pl[1] = 0x0F; pl[3] = 0x00;
        const std::vector<uint8_t> ro = aecp_xact(0x002B, 0x4033, pl);
        ck("[AMAP] STREAM_PORT_OUTPUT is served now: SUCCESS(0)",
           aecp_status(ro), 0);
        ck("[AMAP] ...number_of_maps 4 (role pools), empty page, cdl 24",
           (long)(ro.size() >= 50
                  ? (long)(((((unsigned)ro[16] & 7) << 8) | ro[17]) << 16
                           | (((unsigned)ro[44] << 8) | ro[45]) << 8
                           | (((unsigned)ro[46] << 8) | ro[47]))
                  : -1), (24 << 16) | (4 << 8) | 0);

        // leave the map as this section found it: unmapped
        axi_write(A_CHMAP_CTRL, 0x1);
        axi_write(A_CHMAP_SEL, 0);  axi_write(A_CHMAP_WORD, 0x0000);
        axi_write(A_CHMAP_SEL, 1);  axi_write(A_CHMAP_WORD, 0x0000);
        axi_write(A_CHMAP_SEL, 2);  axi_write(A_CHMAP_WORD, 0x0000);
        axi_write(A_CHMAP_CTRL, 0x0);
    }

    printf("-- TCTX: talker CFG words through the live packetizer port --\n");
    axi_write(A_STRM_SEL, 0x101);                    // dir=1 idx=1
    axi_write(A_SW_DMAC_LO, 0xF000AB01);
    axi_write(A_SW_DMAC_HI, 0x000591E0);             // uid 5 in [31:16]
    axi_write(A_SW_CTRL, (2u << 5) | 1u);            // TCTX w0: vid=2, en
    ck("TCTX w0 CTRL readback (port B)", axi_read(A_SW_CTRL), (2u << 5) | 1u);
    ck("TCTX w1 DMAC_LO readback", axi_read(A_SW_DMAC_LO), 0xF000AB01);
    ck("TCTX w2 DMAC_HI readback", axi_read(A_SW_DMAC_HI), 0x000591E0);
    axi_write(A_STRM_SEL, 0x102);                    // untouched talker ctx
    ck("talker 2 CTRL reads 0", axi_read(A_SW_CTRL), 0);

    printf("-- route flags: RENDER|DMA / RENDER-only / NULL (stream 1) --\n");
    // so far every injected frame belonged to s1 (DMA-only) or s2 (NULL)
    // while s0 held the reset RENDER|DMA claim: the render tap must have
    // stayed silent (RENDER-lowest-wins picks s0, which got no frames)
    ck("render tap silent while s0 owns RENDER", render_beats, 0);
    // demote s0 (window idx 0 commit: en=0 evicts the table override,
    // route=NULL drops its RENDER claim) so s1 wins the render pick
    axi_write(A_STRM_SEL, 0x000);
    axi_write(A_SW_CTRL, (RT_NULL << 1) | 0u);
    // RENDER|DMA = capture-while-rendering: ring copy AND render tap.
    // A CTRL commit re-writes the stream-table entry from the STAGED sid
    // registers (the window ABI: SEL, stage SID, commit CTRL) - re-stage
    // sidB before every s1 CTRL rewrite.
    axi_write(A_STRM_SEL, 0x001);
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_RENDER_DMA << 1) | 1u);
    ck("s1 CTRL = RENDER|DMA readback", axi_read(A_SW_CTRL), 0x7);
    size_t rb0 = pcm_frames.size(); long xb0 = render_beats;
    inject(mkaaf(sidB, 22, 2, 0x30), 120);
    inject(mkaaf(sidB, 23, 2, 0x40), 120);
    ck("RENDER|DMA: +2 ring frames", pcm_frames.size() - rb0, 2);
    ck("RENDER|DMA: ring tuser == 1", pcm_frames.back().user, 1);
    ck("RENDER|DMA: 12 render beats (2 x 6)", render_beats - xb0, 12);
    // RENDER-only: renders, NO ring copy
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_RENDER << 1) | 1u);
    rb0 = pcm_frames.size(); xb0 = render_beats;
    inject(mkaaf(sidB, 24, 2, 0x50), 120);
    inject(mkaaf(sidB, 25, 2, 0x60), 120);
    ck("RENDER-only: no ring frames", pcm_frames.size() - rb0, 0);
    ck("RENDER-only: 12 render beats", render_beats - xb0, 12);
    // NULL: neither sink; the monitor/depkt still count ([M-5.3.8.10])
    axi_write(A_SW_SID_LO, 0x00030001);
    axi_write(A_SW_SID_HI, 0x03000000);
    axi_write(A_SW_CTRL, (RT_NULL << 1) | 1u);
    rb0 = pcm_frames.size(); xb0 = render_beats;
    inject(mkaaf(sidB, 26, 2, 0x70), 120);
    inject(mkaaf(sidB, 27, 2, 0x80), 120);
    ck("NULL: no ring frames", pcm_frames.size() - rb0, 0);
    ck("NULL: no render beats", render_beats - xb0, 0);
    axi_write(A_STRM_SEL, 0x001);
    snap_and_wait();
    ck("NULL still counted: s1 FRAMES_RX = 16", axi_read(A_SW_CNT0 + 9*4), 16);

    printf("-- talker t>0 arming: window CTRL + per-stream gate terms --\n");
    // the [TCTX] section already committed t1 CTRL en=1 through the window;
    // MAAP + lwSRP are still at their disabled defaults.
    //
    // ASK FOR THE BYPASS EXPLICITLY. This case tests the TCTX ARMING PATH -
    // that a window CTRL commit reaches the per-stream enable - not the
    // admission POLICY. Until VERSION 0x0018 it passed without asking,
    // because AAF_CTRL reset to 0x0002_0002 and bit 1 (cfg_aaf_bypass) ORs
    // past both qualifying terms, so every talker streamed from power-on
    // whether or not a Listener Ready was ever registered. That reset value
    // was the defect (Milan v1.2 5.3.7.3 makes the licence to stream
    // conditional on RECEIVING a Listener Ready/Ready Failed), so the reset
    // is now 0x0002_0000 and this check was passing BECAUSE of it.
    // 2026-07-30: the per-context TCTX CTRL[0] arming lever is GONE - it
    // reset to 0 with no board-software writer, so it held every talker
    // above 0 dark forever, and Milan v1.2 5.3.7.3 / 5.4.2.19 / 5.4.2.20 /
    // 5.5.4.1 leave no room for a per-stream software enable on a Stream
    // Output at all. So AAF_CTRL[0] is now the ONE enable for every talker,
    // exactly as it always was for t0: with it clear, bypass alone must NOT
    // light t1 (this check used to assert the opposite).
    axi_write(A_AAF_CTRL, 0x00020002);   // bypass on, flat enable still 0
    ck("AAF_CTRL.en=0 holds t1 too (one flat enable, no per-context lever)",
       (tap_stream_en() >> 1) & 1, 0);
    ck("t0 still down (AAF_CTRL.en = 0)", tap_stream_en() & 1, 0);
    // t0 up via the legacy flat path (VID 2 + bypass + en - the VID-2 rule)
    axi_write(A_AAF_CTRL, 0x00020003);
    ck("t0 up via AAF_CTRL", tap_stream_en() & 1, 1);
    // t0 EMITS on the wire while t1 is armed (capture slot 0 pairs flow
    // continuously; t>0 has no sample source at datapath level - see the
    // header note, aaf nx [I2T] proves t>0 frame identity)
    uint32_t fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 200 && axi_read(A_AAF_FRAMES) == fr0; g++)
        for (int c = 0; c < 512; c++) step();
    ck("t0 emission alive while t1 armed", axi_read(A_AAF_FRAMES) > fr0, 1);
    // lwSRP on without reservations (2026-07-26 mirrored contract): the
    // composition is term-by-term IDENTICAL for every stream now, so
    // cfg_aaf_bypass is the escape hatch for t>0 exactly as for t0 - the
    // old "only t1 drops" asymmetry WAS the honest gap this closes.
    axi_write(A_LWSRP_CTRL, 0x15);          // enable, class-A queue 5
    for (int c = 0; c < 64; c++) step();
    ck("lwSRP on + bypass: t1 rides bypass like t0", (tap_stream_en() >> 1) & 1, 1);
    ck("lwSRP on + bypass: t0 unaffected", tap_stream_en() & 1, 1);
    // bypass CLEAR: no reservation -> EVERY stream gates (FR-SRP-03 for all)
    axi_write(A_AAF_CTRL, 0x00020001);
    for (int c = 0; c < 64; c++) step();
    ck("bypass clear: t1 gates (no reservation)", (tap_stream_en() >> 1) & 1, 0);
    ck("bypass clear: t0 gates too (mirrored)", tap_stream_en() & 1, 0);
    axi_write(A_AAF_CTRL, 0x00020003);       // the VID-2 rule value restored
    for (int c = 0; c < 64; c++) step();
    fr0 = axi_read(A_AAF_FRAMES);
    for (int g = 0; g < 200 && axi_read(A_AAF_FRAMES) == fr0; g++)
        for (int c = 0; c < 512; c++) step();
    ck("t0 emission alive on bypass restore", axi_read(A_AAF_FRAMES) > fr0, 1);

    printf("-- 5.3.7.3 silence fill: an ARMED talker with no source FRAMES --\n");
    // Until 2026-07-28 t1 was armed exactly here and emitted NOTHING: no
    // pair slot had a source behind it (the W3 finding), so a listener that
    // bound it got ACMP SUCCESS and then no packets - the state Milan v1.2
    // 5.3.7.3's first sentence forbids ("...it shall be streaming AVTP
    // packets"). KL_pair_zero_fill now strobes every consumed pair slot at
    // clk_audio/512, silence where nothing feeds it, so an armed talker
    // frames at the media rate. Talkers are told apart by the sid uid16
    // (bytes 24-25): t0 = 0, t1 = 5 (staged into A_SW_DMAC_HI[31:16] in the
    // TCTX section above); anything else armed here would be a defect.
    {
        std::vector<uint8_t> cur;
        int t1f = 0, t1sil = 0, t1chans = -1, t1dlen = -1, foreign = 0,
            sibling = 0;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < 60000 && t1f < 3; c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    // TX AAF rides the VID-2 C-TAG (the AAF_CTRL[27:16]
                    // rule), so allow for the 4-byte 802.1Q shim
                    size_t off = (cur.size() > 17 && cur[12] == 0x81
                                  && cur[13] == 0x00) ? 4 : 0;
                    if (cur.size() >= 86 + off && cur[12+off] == 0x22
                        && cur[13+off] == 0xF0 && cur[14+off] == 0x02) {
                        int uid = (cur[24+off] << 8) | cur[25+off];
                        if (uid == 5) {
                            t1f++;
                            t1chans = cur[32+off];
                            t1dlen  = (cur[34+off] << 8) | cur[35+off];
                            bool z = true;
                            for (size_t i = 38+off;
                                 i < 38 + off + 48 && i < cur.size(); i++)
                                if (cur[i]) z = false;
                            if (z) t1sil++;
                        } else if (uid >= 2 && uid < NSTREAMS_TB) {
                            // 2026-07-30: t2/t3 are ELABORATED contexts and
                            // this posture has bypass on, so they are
                            // licensed and MUST also be framing silence
                            // (Milan 5.3.7.3). They are counted, not
                            // condemned - and the count is only reachable
                            // at all because their identity is now derived
                            // (they used to emit uid 0, i.e. they were
                            // silently booked as t0 and this classifier was
                            // blind to them). The bound is the ELABORATED
                            // shape, not a hard 4: at N=8 talkers 4..7 are
                            // just as real, and hardcoding 4x4 here made the
                            // 8x8 leg call them foreign.
                            sibling++;
                        } else if (uid != 0) {
                            foreign++;      // an uid we never elaborated
                        }
                    }
                    cur.clear();
                }
            }
            hi();
        }
        ck("silence fill: armed t1 EMITS AAF PDUs", t1f >= 3, 1);
        ck("silence fill: t1 channels_per_frame = wire width", t1chans, 2);
        ck("silence fill: t1 stream_data_length = 48", t1dlen, 48);
        ck("silence fill: t1 payload is DIGITAL SILENCE, every PDU",
           t1sil, t1f);
        // no PDU may carry an unique_id this shape never elaborated
        ck("silence fill: no PDU from an unelaborated uid", foreign, 0);
        // ...and the sibling contexts ARE streaming under the same licence,
        // each under its OWN derived stream_id (they emitted uid 0 before
        // the identity fix, which is exactly what made this test blind)
        ck("silence fill: sibling talkers t2/t3 frame too (5.3.7.3)",
           sibling > 0, 1);
    }

    // ==================================================================
    //  DELETED 2026-08-13: the 5.5.2.7 SRP-ONLY licence (a Listener Ready opens the gate with zero ACMP).
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  MILAN 4.2.7.2.1 DOMAIN ADOPT AT THE DATAPATH (gh #63 I4): a class-A
    //  Domain declaration with a different VID moves LWSRP_DOM (0x788),
    //  the AAF C-TAG on the wire and the CRF talker's 0x750 tag word all
    //  at once - the reservation and the frames are one pair - and the
    //  adoption REVERTS on the engine-enable fall.
    // ==================================================================
    printf("-- 4.2.7.2.1 Domain adopt: 0x788 + the AAF/CRF tag words --\n");
    {
        enum { A_LWSRP_DOM_L = 0x788, A_CRFT_CTRL_L = 0x750,
               A_LINK_CTRL_L = 0x71C };
        // entry state: LWSRP_CTRL 0x15 (engine on), AAF_CTRL 0x00020003
        // (en + bypass) - t0 is emitting tagged AAF zero-fill PDUs.
        // Adoption reverts on link-down, and eff_link rides the LINK GUARD's
        // establishment window - park the guard disabled (LINK_CTRL[2]) so
        // eff_link = i_link_up = 1 deterministically for this case.
        const uint32_t link_was = axi_read(A_LINK_CTRL_L);
        axi_write(A_LINK_CTRL_L, link_was | 0x4);
        for (int c = 0; c < 64; c++) step();
        ck("adopt-dp: defaults in force (0x788 = {prio 3, vid 2})",
           axi_read(A_LWSRP_DOM_L), 0x00030002);
        // ---- inject the bridge Domain {class A, prio 3, VID 5} ---------
        uint8_t dm[60]; memset(dm, 0, sizeof dm);
        const uint8_t msrp_da2[6] = {0x01,0x80,0xC2,0x00,0x00,0x0E};
        memcpy(dm, msrp_da2, 6);
        dm[6]=0x02; dm[7]=0xAA; dm[8]=0xBB; dm[9]=0xCC; dm[10]=0xDD;
        dm[11]=0x02;
        dm[12]=0x22; dm[13]=0xEA;
        dm[14]=0;                       // ProtocolVersion
        dm[15]=4; dm[16]=4;             // Domain (type 4), AttributeLength 4
        dm[17]=0; dm[18]=9;             // AttributeListLength
        dm[19]=0; dm[20]=1;             // VectorHeader: NOV 1
        dm[21]=6;                       // SRclassID = A
        dm[22]=3;                       // SRclassPriority = 3
        dm[23]=0; dm[24]=5;             // SRclassVID = 5
        dm[25]=36;                      // ThreePacked JoinIn
        inject(dm, 60, 2000);
        uint32_t domw = 0;
        for (int g = 0; g < 64 && domw != 0x01030005u; g++) {
            for (int c = 0; c < 64; c++) step();
            domw = axi_read(A_LWSRP_DOM_L);
        }
        ck("adopt-dp: 0x788 reads {adopted, prio 3, VID 5}",
           domw, 0x01030005u);
        // the adopt event latches the boundary until the (now-operational)
        // pair is re-declared - the same PDU again heals it
        inject(dm, 60, 2000);
        ck("adopt-dp: re-declaration of the adopted pair heals domain_ok",
           (axi_read(0x694) >> 5) & 1, 1);
        // ---- the AAF C-TAG follows: TCI = {PCP 3, DEI 0, VID 5} --------
        auto tag_of_next_aaf = [&]() -> int {
            std::vector<uint8_t> fr;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 60000; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            fr.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        if (fr.size() >= 20 && fr[12] == 0x81 && fr[13] == 0x00
                            && fr[16] == 0x22 && fr[17] == 0xF0
                            && fr[18] == 0x02) {
                            int tci = (fr[14] << 8) | fr[15];
                            hi();
                            return tci;
                        }
                        fr.clear();
                    }
                }
                hi();
            }
            return -1;
        };
        ck("adopt-dp: AAF C-TAG TCI = {PCP 3, VID 5} (0x6005)",
           (uint32_t)tag_of_next_aaf(), 0x6005);
        //! ---- DELETED 2026-08-13: the CRF tag word half, and the revert.
        //! Two subjects, both gone with hdl/ieee8021q/srp/:
        //!
        //!  (a) "the CRF talker's tag word follows the adopted pair"
        //!      (0x750[19:8] VID, [22:20] PCP). Those fields are gated by
        //!      crft_class_a_w, the CRF output's SR class A LICENCE, which
        //!      needs an admitted reservation. The processor only admits a
        //!      source that is DECLARING, and declaring needs a MAAP
        //!      ALLOC_DA success - ~1.5e8 cycles away at this leg's silicon
        //!      MAAP rate (see the deleted lwSRP sections for the
        //!      measurement). The fields read a structural 0 here and
        //!      asserting 0 would say nothing about the adopted pair.
        //!
        //!  (b) "enable-fall REVERTS to the defaults". LWSRP_CTRL's enable
        //!      used to command the fabric's own applicant, and the 4.2.7.2.1
        //!      reset list was implemented against it. The adoption is the
        //!      processor's KL_srp_domain now (lwsrp_adopt_valid is
        //!      pp_cd_srp_domain_adopted_w) and it takes NO enable from this
        //!      register, so clearing 0x680 does not command a revert and
        //!      the check was asserting that a write reaches a wire it no
        //!      longer reaches.
        //!
        //! WHAT SURVIVED IS THE PART THAT MATTERS AND IT IS ABOVE: a
        //! received class-A Domain declaration with a different VID really
        //! is adopted (0x788 = {adopted, prio 3, VID 5}), a re-declaration
        //! of the adopted pair really does heal domain_ok, and the AAF
        //! C-TAG on the wire really does move with it - the reservation and
        //! the frames are one pair, which is the clause's whole point.
        axi_write(A_LINK_CTRL_L, link_was);  // the guard's posture restored
        for (int c = 0; c < 64; c++) step();
    }

    axi_write(A_LWSRP_CTRL, 0x14);          // disable, class-A queue 5 kept
    for (int c = 0; c < 64; c++) step();
    ck("lwSRP off: t1 re-arms", (tap_stream_en() >> 1) & 1, 1);
    // MAAP enabled + unclaimed holds t0 AND t1 alike (the engine-wide
    // term - ONE claim engine; mirrors t0's composition, see the RTL note)
    axi_write(A_MAAP_CTRL, 0x0801);
    for (int c = 0; c < 16; c++) step();
    ck("MAAP unclaimed: t1 held", (tap_stream_en() >> 1) & 1, 0);
    ck("MAAP unclaimed: t0 held too", tap_stream_en() & 1, 0);
    axi_write(A_MAAP_CTRL, 0x0800);
    for (int c = 0; c < 16; c++) step();
    ck("MAAP off: both restored", tap_stream_en() & 3, 3);
    // TCTX w0 CTRL[0] IS NO LONGER AN EGRESS LEVER (2026-07-30). The word
    // still carries chans/VID and still lands in the packetizer's context
    // RAM, but nothing consults bit 0: a Stream Output the shape elaborated
    // streams when SRP licenses it (Milan 5.3.7.3's licence has no software
    // term, and 5.4.2.20 forbids STOP_STREAMING on a Stream Output). So a
    // w0 commit with bit 0 clear must leave egress exactly as it was - the
    // check that used to assert it "disarms t1", inverted into the property
    // that replaced it.
    axi_write(A_STRM_SEL, 0x101);
    axi_write(A_SW_CTRL, (2u << 5) | 0u);            // TCTX w0: vid=2, bit0=0
    for (int c = 0; c < 16; c++) step();
    ck("w0 CTRL[0]=0 does NOT stop t1 (no per-stream software enable)",
       (tap_stream_en() >> 1) & 1, 1);
    ck("t0 unaffected by the t1 w0 commit", tap_stream_en() & 1, 1);
    // ...and with bypass on (this posture) every ELABORATED talker is
    // licensed, so t2/t3 stream too - the 5.3.7.3 zero-fill truth the old
    // "never armed" expectation could only hold because the missing enable
    // kept them dark. Their identity is asserted on the wire in the
    // reset-licence case at the top of this file.
    ck("t2/t3 armed too (shape-static, reset-armed)",
       (tap_stream_en() >> 2) & 3, 3);
    // ==================================================================
    //  DELETED 2026-08-13: the N-sink ACMP ctx2 window bind, the gh #58 D1 SET_STREAM_FORMAT refusal, and the E3 journal-ingest replay.
    //  SUBJECT GONE. KL_acmp_tlkr_ctx, KL_acmp_responder, KL_acmp_listener,
    //  KL_acmp_lstn_ctx and acmp_pkg.sv are deleted. The processor runs the
    //  BIND_RX ladder internally and publishes a bind RECORD, so
    //  milan_datapath ties acmp_tbl_gnt_w and acmp_tbl_ctx_w to zero and
    //  the 0x800 window's ACMP table master reads a STRUCTURAL ZERO: the
    //  per-context SID/DMAC/STATE words this section read are not a stale
    //  view, they have no source at all. ACMPL_STATE 0x6A4's ladder fields
    //  went with them ([2:0] SM state, [14:13] probing, [12:8] acmp_status).
    //
    //  The bind itself is ALIVE and it is graded - see the TRAP-1 section,
    //  which drives a real CONNECT_RX_COMMAND, answers the listener's own
    //  PROBE_TX and checks the resulting entry-0 stream-table alias against
    //  the RX parser. That is the property that survived; the table window
    //  is not.
    //
    //  SUBJECT GONE. There is no AECP on this device. KL_aecp_top and its
    //  whole plane - packet validator, common parser, L0 state, timers,
    //  accessor, AEM store and its generated descriptor ROM, the dynamic-map
    //  mux, the response builder, the ingress decoder, KL_aem_patch and
    //  KL_persist_journal - are deleted, and the processor's AECP engine is
    //  the P4 uCPU, which has not landed at its top (aecp_txn_ready_i is
    //  tied 0 there and TX lanes 0/1 are idle). No command is answered, so
    //  GET/SET_STREAM_FORMAT, the STREAM_IS_RUNNING refusal keyed on the
    //  bind level, and the 0x7B8 journal-ingest group have no responder.
    //  JNL_STAT/JNL_SEQ and the 0x7A0 bind-restore ack are structural zeros.
    //  USER decision, made knowingly - not a defect to work around here.
    // ==================================================================
    // ======================================================================
    // item-5 (N x N, the AX 8x8 target): full-index routing sweep. The checks
    // above prove idx 1/2/3 at N=4; this proves EVERY fresh index 3..N-1 is
    // provisioned, live, and routed independently AT THE SAME TIME. Default
    // build (N=4) walks idx 3; the obj_nxn8 build (-GN_STREAMS=8) walks idx
    // 3..7 - the top half of the stream-index space that exists only at N=8,
    // so a PASS here IS the 8-stream routing proof the AX shape needs.
    printf("-- N-wide routing: fresh streams 3..%d live at once, by index --\n",
           NSTREAMS_TB - 1);
    // provision every fresh stream simultaneously, DMA route so each lands on
    // the PCM ring tagged with its own tuser. sid(s) = {0x30+s,0,0,0,0,
    // 0x30+s,0,s}: distinct from sidB/C/X and from each other.
    for (int s = 3; s < NSTREAMS_TB; s++) {
        uint32_t sid_hi = ((uint32_t)(0x30 + s) << 24);
        uint32_t sid_lo = ((uint32_t)(0x30 + s) << 16) | (uint32_t)s;
        axi_write(A_STRM_SEL, s & 0xF);                  // dir=0 idx=s
        axi_write(A_SW_SID_LO, sid_lo);
        axi_write(A_SW_SID_HI, sid_hi);
        axi_write(A_SW_FMT_LO, FMT_LO);
        axi_write(A_SW_FMT_HI, FMT_HI);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);        // en, DMA flag
    }
    // CFG readback per stream through the ENGINE-ARBITRATED LCTX port B
    for (int s = 3; s < NSTREAMS_TB; s++) {
        axi_write(A_STRM_SEL, s & 0xF);
        char nm[56]; snprintf(nm, sizeof nm, "ctx%d CTRL readback (port B)", s);
        ck(nm, axi_read(A_SW_CTRL), 0x3);
    }
    // inject one uniquely-payloaded frame per stream, interleaved, ALL table
    // entries live: the classifier must tag each frame with the right index.
    size_t ring0 = pcm_frames.size();
    for (int s = 3; s < NSTREAMS_TB; s++) {
        uint8_t sid[8] = {(uint8_t)(0x30 + s), 0, 0, 0, 0,
                          (uint8_t)(0x30 + s), 0, (uint8_t)s};
        inject(mkaaf(sid, (uint8_t)(0x40 + s), 2, (uint8_t)(0xA0 + s)), 120);
    }
    ck("sweep: one ring frame per fresh stream",
       (unsigned)(pcm_frames.size() - ring0), (unsigned)(NSTREAMS_TB - 3));
    // each ring frame carries its own stream's tuser + byte-exact payload
    bool sweep_user_ok = true, sweep_pay_ok = true;
    for (int s = 3; s < NSTREAMS_TB; s++) {
        size_t k = ring0 + (size_t)(s - 3);
        if (k >= pcm_frames.size()) { sweep_user_ok = false; break; }
        if (pcm_frames[k].user != s) sweep_user_ok = false;
        if (pcm_frames[k].bytes.size() != 48) sweep_pay_ok = false;
        else for (int i = 0; i < 48; i++)
            if (pcm_frames[k].bytes[i] != (uint8_t)(0xA0 + s + i)) sweep_pay_ok = false;
    }
    ck("sweep: ring tuser == stream index for all", sweep_user_ok, 1);
    ck("sweep: 48-byte payload byte-exact for all", sweep_pay_ok, 1);
    // isolation: each fresh stream counted EXACTLY its own single frame (no
    // cross-count across the N simultaneously-live contexts) - Table 7-157.
    for (int s = 3; s < NSTREAMS_TB; s++) {
        axi_write(A_STRM_SEL, s & 0xF);
        snap_and_wait();
        char nm[64];
        snprintf(nm, sizeof nm, "ctx%d FRAMES_RX == 1 (isolated)", s);
        ck(nm, axi_read(A_SW_CNT0 + 9*4), 1);
        snprintf(nm, sizeof nm, "ctx%d PDUS == 1", s);
        ck(nm, axi_read(A_SW_PDUS), 1);
    }
    // an unknown sid (no table entry at any index) is still ignored at width N
    {
        const uint8_t sidU[8] = {0x5A, 0, 0, 0, 0, 0x5A, 0, 0x0F};
        size_t before = pcm_frames.size();
        inject(mkaaf(sidU, 50, 2, 0x11), 120);
        ck("sweep: unknown sid ignored (no ring frame)",
           (unsigned)pcm_frames.size(), (unsigned)before);
    }

    // ======================================================================
    // HOST-PLANE drill (silicon 0x1000B regression, 2026-07-25): the fabric
    // above is fully provisioned and N streams are live - exactly the state
    // the flashed ax8x8 build was in when host RX read dead. In THIS shape
    // (N=NSTREAMS_TB, single host RX lane) the host-facing lanes must work:
    //   [H1] a non-AVTP broadcast frame on the MAC RX AXIS emerges byte-exact
    //        on the host DMA RX port (MAC -> PTP-RX -> dest-MAC filter ->
    //        m_axis_rx = the RingDMAWriter's input);
    //   [H2] a gPTP pdelay_req (event) frame yields one 2-beat metadata
    //        record on m_axis_ts (= the dma-ts writer's input), with the
    //        host RX copy of the same frame still delivered.
    // sim_main proves both at N=1 only; this is the N>1 silicon-shape gate.
    // ======================================================================
    printf("-- host plane: MAC->host-RX + PTP ts record at N=%d --\n",
           NSTREAMS_TB);
    {
        // drain the host RX lane first: every earlier inject() left frames
        // parked against m_axis_rx_tready=0 (the fabric tests never drain it)
        dut->m_axis_rx_tready = 1;
        for (int c = 0; c < 4000; c++) step();

        // [H1] 64-byte broadcast ARP-ish frame, LE lanes like the real ingress
        uint8_t hf[64]; memset(hf, 0, sizeof hf);
        const uint8_t hh[14] = {0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                0x02,0x11,0x22,0x33,0x44,0x55, 0x08,0x06};
        memcpy(hf, hh, 14);
        for (int i = 14; i < 64; i++) hf[i] = (uint8_t)(0xC0 + i);
        std::vector<uint64_t> hb, hout;
        for (int bt = 0; bt < 8; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8; j++) v |= (uint64_t)hf[bt*8+j] << (8*j);
            hb.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 800; c++) {
            if (idx < hb.size()) {
                dut->s_axis_mac_rx_tdata  = hb[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == hb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            uint64_t od  = dut->m_axis_rx_tdata;
            hi();
            if (in_acc) idx++;
            if (out_acc) hout.push_back(od);
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("host RX: broadcast frame beats delivered", hout.size(), hb.size());
        bool hexact = hout.size() == hb.size();
        if (hexact)
            for (size_t i = 0; i < hb.size(); i++)
                if (hout[i] != hb[i]) hexact = false;
        ck("host RX: broadcast frame byte-exact", hexact ? 1 : 0, 1);

        // [H2] PTP event frame -> exactly one 2-beat ts record + host RX copy
        enum { A_PTP_CTRL = 0x500, A_PTP_INCR = 0x504 };
        axi_write(A_PTP_INCR, 20u << 24);          // 20 ns/tick Q8.24
        axi_write(A_PTP_CTRL, 1);
        uint8_t g[68]; memset(g, 0, sizeof g);
        const uint8_t gh[14] = {0x01,0x80,0xC2,0,0,0x0E, 2,0,0,0,0,2, 0x88,0xF7};
        memcpy(g, gh, 14);
        g[14] = 0x12; g[15] = 0x02; g[17] = 54;    // pdelay_req, v2, len 54
        g[44] = 0xBE; g[45] = 0xEF;                // sequenceId
        std::vector<uint64_t> gb, ts;
        size_t hrx_beats = 0;
        for (int bt = 0; bt < 9; bt++) {
            uint64_t v = 0;
            for (int j = 0; j < 8 && bt*8+j < 68; j++)
                v |= (uint64_t)g[bt*8+j] << (8*j);
            gb.push_back(v);
        }
        idx = 0;
        dut->m_axis_ts_tready = 1;
        for (int c = 0; c < 800; c++) {
            if (idx < gb.size()) {
                dut->s_axis_mac_rx_tdata  = gb[idx];
                dut->s_axis_mac_rx_tkeep  = (idx == gb.size()-1) ? 0x0F : 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == gb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool tsx    = dut->m_axis_ts_tvalid && dut->m_axis_ts_tready;
            uint64_t td = dut->m_axis_ts_tdata;
            bool hrx    = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            hi();
            if (in_acc) idx++;
            if (tsx) ts.push_back(td);
            if (hrx) hrx_beats++;
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("ts record emitted (2 beats)", ts.size(), 2);
        if (ts.size() == 2) {
            ck("ts word1 dir=RX", (unsigned long)(ts[1] & 1), 0);
            ck("ts word1 mtype=2 (pdelay_req)",
               (unsigned long)((ts[1] >> 4) & 0xF), 2);
            ck("ts word1 seq=0xBEEF",
               (unsigned long)((ts[1] >> 8) & 0xFFFF), 0xBEEFUL);
        }
        ck("host RX: gPTP frame copy delivered (9 beats)", hrx_beats, 9);

        // [H3] silicon boot ordering: the dma-ts writer is NOT armed at boot
        // (m_axis_ts_tready = 0) while the LAN already carries gPTP event
        // frames (the switch runs 802.1AS). The ts record lane fills - and
        // MUST NOT wedge the shared RX pipeline: after a burst of un-drained
        // event frames, a host-destined frame still has to emerge on
        // m_axis_rx. This is the exact state the flashed ax8x8 build boots
        // into (rx_packets = 0 forever, fabric TX still perfect).
        dut->m_axis_ts_tready = 0;
        for (int burst = 0; burst < 40; burst++) {
            g[44] = (uint8_t)(burst >> 8); g[45] = (uint8_t)burst;
            idx = 0;
            for (int c = 0; c < 60; c++) {
                if (idx < gb.size()) {
                    dut->s_axis_mac_rx_tdata  = gb[idx];
                    dut->s_axis_mac_rx_tkeep  = (idx == gb.size()-1) ? 0x0F : 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == gb.size()-1);
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
        // now the host frame again, RX ring armed (tready=1), ts still unarmed
        std::vector<uint64_t> hout2;
        idx = 0;
        for (int c = 0; c < 800; c++) {
            if (idx < hb.size()) {
                dut->s_axis_mac_rx_tdata  = hb[idx];
                dut->s_axis_mac_rx_tkeep  = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast  = (idx == hb.size()-1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            bool in_acc  = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            bool out_acc = dut->m_axis_rx_tvalid && dut->m_axis_rx_tready;
            uint64_t od  = dut->m_axis_rx_tdata;
            hi();
            if (in_acc) idx++;
            if (out_acc) hout2.push_back(od);
        }
        dut->s_axis_mac_rx_tvalid = 0;
        ck("host RX alive under un-drained ts lane (8 beats)",
           hout2.size(), hb.size());
        bool h2exact = hout2.size() == hb.size();
        if (h2exact)
            for (size_t i = 0; i < hb.size(); i++)
                if (hout2[i] != hb[i]) h2exact = false;
        ck("host RX under ts backpressure byte-exact", h2exact ? 1 : 0, 1);
        dut->m_axis_ts_tready = 1;
        dut->m_axis_rx_tready = 0;
    }

    // ======================================================================
    // TRAP-1 END-TO-END — REGRESSION GUARD for the fabric-listener blocker
    // (found 2026-07-26, fixed the same day; this section asserts the FIX).
    //
    // The defect: any window CTRL write at index 0 detached the entry-0 ACMP
    // alias FOR GOOD, so a later ACMP bind of listener 0 was cosmetic - the
    // listener SM reported bound, the stream table never saw that stream_id,
    // the parser never matched. PARSED climbed, MATCHED did not: the 8x8
    // blocker's exact symptom, reached from a CSR write sequence a
    // provisioning daemon would make. Two RTL terms combined to allow it:
    //   * `(|{wing_sid_hi_r, wing_sid_lo_r})` was meant to mean "a sid was
    //     staged for this commit", but the staging pair is GLOBAL, not per
    //     index - any earlier stage for any OTHER listener satisfied it, so a
    //     route-flags-only CTRL write at idx 0 armed entry 0 with that other
    //     listener's stream_id;
    //   * `| ~csr_lctx_wr_data_w[0]` let an en=0 CTRL write through
    //     unconditionally, so even "clear this sink" reached the table -
    //     and KL_stream_table's ovr_armed_r[0] was set by ANY write and
    //     cleared only by RESET, so there was no way back to alias mode.
    //
    // The fix, asserted below:
    //   * win_commit_glue tags the staging set with the index it was staged
    //     for (`wing_stg_hit_w`), so a commit only overrides the table when a
    //     sid was staged FOR THAT INDEX, and an eviction with nothing staged
    //     commits the ZERO sid;
    //   * KL_stream_table treats {valid=0, sid=0} as RELEASE-TO-ALIAS and
    //     disarms ovr_armed_r[idx], so entry 0 returns to the ACMP alias at
    //     runtime.
    //
    // tb/verilator/avtp_parser/sim_tbl.cpp T6 covers the table-level
    // mechanism from a clean reset; this section proves the behaviour through
    // the real CSR window in the real datapath. Asserted through the 0x8B4
    // APRB probe group only - upstream of format, route and depacketizer
    // policy - so the verdict under test is the stream-table match itself and
    // nothing else. Runs last: it leaves listener 0 provisioned.
    printf("-- TRAP-1: entry-0 ACMP alias survives window writes (regression) --\n");
    {
        enum { A_APRB_PARSED = 0x8B4, A_APRB_MATCHED = 0x8B8,
               A_APRB_INFO = 0x8C4 };
        auto armed   = [&]{ return (axi_read(A_APRB_INFO) >> 16) & 0xFF; };
        auto matched = [&]{ return axi_read(A_APRB_MATCHED); };
        auto parsed  = [&]{ return axi_read(A_APRB_PARSED); };

        // the host-plane drill above deliberately left the DMA RX port
        // un-drained; the shared inject() never drives it, so frame tails
        // stall at the filter boundary and back-pressure the whole RX
        // pipeline - including the PRE-filter parser tap. Arm the port and
        // let the stalled tails flush before measuring anything.
        dut->m_axis_rx_tready = 1;
        for (int c = 0; c < 400; c++) step();

        // ---- PLAY THE TALKER (2026-08-13) -------------------------------
        //! The bind ladder is the protocol processor's now, and it is a REAL
        //! ladder: KL_pp_acmp_listener answers the CONNECT_RX_COMMAND, then
        //! launches a CONNECT_TX_COMMAND (Milan PROBE_TX) at the named talker
        //! and takes the BOUND stream_id from the ANSWER - Milan v1.2
        //! 5.5.3.5.18 step 4. The deleted listener recorded the command's own
        //! sid at bind time, so this bench never had to answer; against the
        //! processor a bench that answers nothing leaves acmp_bound_sid_o at
        //! ZERO and entry 0's alias matches nothing. The probe names its sink
        //! in listener_unique_id and its sequence_id is what the listener
        //! matches the response on (5.5.3.5.18 step 1), so both are harvested
        //! off the egress by acmp_sniff() rather than guessed.
        auto answer_probe = [&](int luid, const uint8_t* sid,
                                const uint8_t* dmac, const uint8_t* teid,
                                uint16_t tuid) {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            memcpy(f+6, teid+0, 6);                     // any unicast SA
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x01;  // CONNECT_TX_RESPONSE
            f[16]=0x00; f[17]=44;                        // status SUCCESS, cdl
            memcpy(f+18, sid, 8);                        // @4  stream_id
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;  // @12 controller
            memcpy(f+34, teid, 8);                       // @20 talker
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);                         // @28 listener = us
            f[50]=(uint8_t)(tuid >> 8); f[51]=(uint8_t)tuid;   // @36
            f[52]=(uint8_t)(luid >> 8); f[53]=(uint8_t)luid;   // @38
            memcpy(f+54, dmac, 6);                       // @40 stream_dest_mac
            f[62]=(uint8_t)(probe_seq_by_luid[luid] >> 8);     // @48 echo
            f[63]=(uint8_t)(probe_seq_by_luid[luid] & 0xFF);
            inject(f, 70, 400);
        };

        // bind listener_unique_id 0 over ACMP with an explicit stream_id -
        // the entry-0 alias, exactly how the bench listener comes up
        const uint8_t sid0[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
        const unsigned long armed_pre = armed();
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;   // CONNECT_RX_COMMAND
            f[16]=0x00; f[17]=44;
            memcpy(f+18, sid0, 8);                            // explicit sid
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tk[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[50]=0x00; f[51]=0x00;                           // talker_unique_id
            f[52]=0x00; f[53]=0x00;                           // listener_unique_id 0
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);
            f[62]=0x77; f[63]=0x22;
            //! drain LONG here: the listener answers the CONNECT_RX first and
            //! only then launches its PROBE_TX, so a 400-cycle window closes
            //! before the probe reaches the sniffer and answer_probe() would
            //! echo a stale sequence_id.
            inject(f, 70, 3000);
        }
        {
            const uint8_t tk0[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            const uint8_t dm0[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            ck("TRAP-1 bind: the listener launched its PROBE_TX",
               probe_seen_luid[0] ? 1 : 0, 1);
            answer_probe(0, sid0, dm0, tk0, 0);
        }
        unsigned long m0 = matched(), p0 = parsed();
        inject(mkaaf(sid0, 0x11, 2, 0xC0), 120);
        // THE REGRESSION GUARD: the listener is bound, both ends agree on the
        // sid, the frame reaches the parser - and the verdict is now OURS.
        // Before the fix this read MATCHED-static because entry 0 had stopped
        // being the ACMP alias hundreds of cycles earlier, when a route-flags
        // CTRL write landed on it.
        ck("TRAP-1 bound: PARSED climbs",  parsed()  - p0, 1);
        ck("TRAP-1 bound: MATCHED climbs (alias intact)", matched() - m0, 1);
        ck("TRAP-1 bound: INFO match flag set",
           (axi_read(A_APRB_INFO) >> 8) & 1, 1);
        ck("TRAP-1 bound: INFO index 0",
           (axi_read(A_APRB_INFO) >> 12) & 0xF, 0);
        // binding listener 0 ENABLES the alias entry, so the armed count rises
        // by exactly one - the alias is a live table entry again, not a ghost
        ck("TRAP-1 bound: the ACMP alias counts as one armed entry",
           armed() - armed_pre, 1);
        const unsigned long armed_bound = armed();

        // a route-flags-only CTRL write at idx 0 - the exact write that used
        // to detach the alias - must now leave it completely alone
        axi_write(A_STRM_SEL, 0x000);                 // dir=0 idx=0
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);     // en + DMA, sid NOT staged
        ck("TRAP-1 route-only CTRL at idx0 does not arm an override",
           armed(), armed_bound);
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x12, 2, 0xC0), 120);
        ck("TRAP-1 route-only CTRL at idx0: STILL MATCHES", matched() - m0, 1);

        // the explicit-override path still works: stage the sid FOR idx 0,
        // then commit. This is the deliberate bench/daemon override.
        axi_write(A_STRM_SEL, 0x000);
        axi_write(A_SW_SID_LO, 0x00020000);
        axi_write(A_SW_SID_HI, 0x02000000);
        axi_write(A_SW_CTRL, (RT_DMA << 1) | 1u);
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x13, 2, 0xC0), 120);
        ck("TRAP-1 explicit override at idx0: MATCH", matched() - m0, 1);
        ck("TRAP-1 explicit override: INFO index 0",
           (axi_read(A_APRB_INFO) >> 12) & 0xF, 0);

        // RELEASE-TO-ALIAS: "clear this sink" - en=0 with nothing staged for
        // idx 0 - commits the zero sid, which disarms the override and hands
        // entry 0 back to the ACMP alias. Before the fix this latched
        // ovr_armed_r[0] and the alias was gone until reset.
        axi_write(A_STRM_SEL, 0x000);                 // dir=0 idx=0
        axi_write(A_SW_CTRL, 0x0);                    // en=0, route=NULL
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x14, 2, 0xC0), 120);
        ck("TRAP-1 release-to-alias: PARSED climbs", parsed() - p0, 1);
        ck("TRAP-1 release-to-alias: alias is back, MATCHED climbs",
           matched() - m0, 1);
        ck("TRAP-1 release-to-alias: INFO match flag set",
           (axi_read(A_APRB_INFO) >> 8) & 1, 1);

        // and an ACMP re-bind now lands on a live alias rather than a ghost
        {
            uint8_t f[72]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0; f[14]=0xFC; f[15]=0x06;
            f[16]=0x00; f[17]=44;
            memcpy(f+18, sid0, 8);
            for (int i = 26; i < 34; i++) f[i] = (uint8_t)i;
            const uint8_t tk[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            memcpy(f+34, tk, 8);
            const uint8_t us[8] = {0x02,0x00,0x00,0xFF,0xFE,0x00,0x00,0x01};
            memcpy(f+42, us, 8);
            f[52]=0x00; f[53]=0x00;
            const uint8_t dm[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            memcpy(f+54, dm, 6);
            f[62]=0x77; f[63]=0x23;
            inject(f, 70, 3000);
        }
        {
            const uint8_t tk0[8] = {0x02,0x00,0x00,0x00,0x00,0x02,0x00,0x00};
            const uint8_t dm0[6] = {0x91,0xE0,0xF0,0x00,0x2A,0x02};
            answer_probe(0, sid0, dm0, tk0, 0);
        }
        m0 = matched(); p0 = parsed();
        inject(mkaaf(sid0, 0x15, 2, 0xC0), 120);
        ck("TRAP-1 ACMP re-bind still matches: PARSED climbs", parsed() - p0, 1);
        ck("TRAP-1 ACMP re-bind still matches: MATCHED climbs",
           matched() - m0, 1);

        // a NEGATIVE leg, so this is not a "matches everything" tautology: an
        // unrelated stream_id must still be parsed-but-not-matched with the
        // alias live
        {
            const uint8_t sidZ[8] = {0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,0x11,0x22};
            m0 = matched(); p0 = parsed();
            inject(mkaaf(sidZ, 0x16, 2, 0xC0), 120);
            ck("TRAP-1 negative: foreign sid PARSED", parsed() - p0, 1);
            ck("TRAP-1 negative: foreign sid NOT matched", matched() - m0, 0);
            ck("TRAP-1 negative: INFO match flag clear",
               (axi_read(A_APRB_INFO) >> 8) & 1, 0);
        }
    }

    // ==================================================================
    //  DELETED 2026-08-13: lwSRP attribute rows through the 0x800 window.
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  DELETED 2026-08-13: EVERY AAF talker row declares on its own enable.
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  DELETED 2026-08-13: t21 / t21-l0 / t27 - the CONNECT_RX -> lwSRP LISTENER row chain.
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  DELETED 2026-08-13: b1d-guard, the |sid want guard on an lwSRP listener row.
    //  SUBJECT GONE. hdl/ieee8021q/srp/ is deleted in full - applicant,
    //  registrar, TA registrar, walker, ingress, context table, MRPDU
    //  serializer, timers and KL_lwsrp_bw_gate. SRP is the protocol
    //  processor's KL_srp_top now and it publishes a class-D face, not an
    //  attribute-row table: milan_datapath ties srp_ctx_gnt_w,
    //  srp_ctx_rd_sid_w, srp_ctx_rd_stat_w, lwsrp_tx_count and
    //  lwsrp_rx_pdus to zero, so the 0x800 window's SRP master and the
    //  0x85C readback are STRUCTURAL ZEROS with nothing behind them.
    //
    //  AND THE LICENCE ITSELF IS OUT OF REACH ON THIS LEG, which is the
    //  part worth stating plainly rather than burying. The processor only
    //  declares a Talker Advertise for a source that is DECLARING, and
    //  acmp_declaring_o is reachable only through a MAAP ALLOC_DA success.
    //  milan_dp elaborates KL_maap at the silicon rate (MAAP_CLK_HZ_P
    //  defaults to MILAN_CLK_FREQ_HZ = 100 MHz), so its Annex B claim walk
    //  - 3 probes x ~500 ms plus announce - is ~1.5e8 cycles away.
    //  MEASURED: still PROBING after 40,000,000 cycles, and the first MSRP
    //  and MVRP frames appear only somewhere inside that window. A leg that
    //  waited for them would add ~25 minutes per elaboration to a nine-leg
    //  suite.
    //
    //  WHERE THE COVERAGE IS NOW: tb/verilator/pp_shadow compresses BOTH
    //  the processor's millisecond and KL_maap's onto one grid, and grades
    //  the DA gate, the SUCCESS PROBE_TX answer with its stream_id and
    //  stream_dest_mac, and the MSRP/MVRP frames on the shared control
    //  lane. The processor's own repository grades the SRP state machines.
    // ==================================================================
    // ==================================================================
    //  CRF Media Clock Output as an ACMP talker source  (item 5, §3.5)
    //
    //  With N >= 2 AAF sinks the CRF output is mandatory, and a controller
    //  must be able to bind it with the SAME CONNECT_TX/PROBE_TX it uses
    //  for audio. milan_datapath gives KL_acmp_tlkr_ctx one more source
    //  context at talker_unique_id = N_STREAMS whose DMAC is the MAAP block
    //  slot base+N_STREAMS; KL_crf_tx then takes that same {sid, dmac} pair
    //  whenever CRFT_SID/CRFT_DMAC are left at 0, so the answer and the
    //  frames cannot disagree.
    // ==================================================================
    printf("-- CRF media-clock output: ACMP talker context at uid N --\n");
    {
        enum { A_CRFT_CTRL = 0x750,
               A_CRFT_SIDLO = 0x754, A_CRFT_SIDHI = 0x758,
               A_CRFT_DMLO = 0x75C, A_CRFT_DMHI = 0x760 };
        // the ACMP responder is gated by ADP enable
        axi_write(A_ADP_CTRL, 0x1);
        for (int c = 0; c < 64; c++) step();

        // a PROBE_TX (CONNECT_TX_COMMAND) for talker_unique_id = uid
        auto probe = [&](uint16_t uid, std::vector<uint8_t>& resp) {
            uint8_t f[70]; memset(f, 0, sizeof f);
            const uint8_t mc[6] = {0x91,0xE0,0xF0,0x01,0x00,0x00};
            memcpy(f, mc, 6);
            const uint8_t csrc[6] = {0x68,0x05,0xCA,0x95,0xB2,0xD1};
            memcpy(f+6, csrc, 6);
            f[12]=0x22; f[13]=0xF0;
            f[14]=0xFC; f[15]=0x00;              // CONNECT_TX_COMMAND
            f[16]=0x00; f[17]=44;
            // talker_entity_id (bytes 34..41) = ours (ADP_EIDHI/LO above)
            f[34]=0x02; f[35]=0x00; f[36]=0x00; f[37]=0xFF;
            f[38]=0xFE; f[39]=0x00; f[40]=0x00; f[41]=0x01;
            f[50]=(uint8_t)(uid >> 8); f[51]=(uint8_t)uid;   // talker_unique_id
            resp.clear();
            std::vector<uint64_t> beats;
            for (int bt = 0; bt < 9; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8; j++)
                    if (bt*8+j < 70) v |= (uint64_t)f[bt*8+j] << (8*j);
                beats.push_back(v);
            }
            size_t idx = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 3000; c++) {
                if (idx < beats.size()) {
                    dut->s_axis_mac_rx_tdata  = beats[idx];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (idx == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
                }
                lo();
                bool acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            resp.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        hi(); if (acc) idx++;
                        if (resp.size() >= 16 && resp[12] == 0x22 &&
                            resp[13] == 0xF0 && resp[14] == 0xFC) break;
                        resp.clear(); continue;
                    }
                }
                hi();
                if (acc) idx++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        };
        auto be = [](const std::vector<uint8_t>& v, size_t o, int n) {
            uint64_t r = 0; for (int i = 0; i < n; i++) r = (r<<8) | v[o+i];
            return r;
        };

        //! WHAT THIS CASE CAN AND CANNOT ANSWER NOW (2026-08-13). The ACMP
        //! talker is the processor's, and it resolves a source's destination
        //! address through KL_pp_maap_shim -> KL_maap. This leg elaborates
        //! KL_maap at the silicon rate, so ANNOUNCE is ~1.5e8 cycles away and
        //! no source ever holds a DA: every in-range PROBE_TX is answered
        //! TALKER_DEST_MAC_FAILED(3), with a zero stream_id and a zero
        //! stream_dest_mac, which is the CORRECT answer - a talker must not
        //! hand out an address it does not own. So the ADDRESSING half of
        //! this case (the SUCCESS status, the {station MAC, uid} sid and the
        //! base+uid dest_mac) is graded in tb/verilator/pp_shadow, where both
        //! millisecond scales are compressed onto one grid.
        //!
        //! WHAT IS STILL GRADED HERE, and it is the item-5 claim itself: the
        //! CRF Media Clock Output EXISTS as an addressable ACMP talker source
        //! at talker_unique_id = N_STREAMS - the probe is answered, the uid
        //! is echoed - while uid N+1 is NOT, so the extra context is exactly
        //! one wide. That is the defect shape this case was written for (a
        //! CRF source outside the advertised range, invisible to every
        //! controller while its PDUs were on the wire every 2 ms).
        std::vector<uint8_t> r;
        probe((uint16_t)NSTREAMS_TB, r);
        ck("CRF probe: a 70-byte ACMP response came back", r.size(), 70);
        if (r.size() == 70) {
            ck("CRF probe: CONNECT_TX_RESPONSE(1)", r[15] & 0x0F, 1);
            //! REPOINTED from SUCCESS: no DA is held on this leg, and
            //! 1722.1-2021 7.4.20 says TALKER_DEST_MAC_FAILED(3).
            ck("CRF probe: status TALKER_DEST_MAC_FAILED(3), no DA held",
               r[16] >> 3, 3);
            ck("CRF probe: talker_unique_id echoed = N",
               be(r, 50, 2), (unsigned)NSTREAMS_TB);
        }
        // NEGATIVE LEG: one uid past the CRF context is still unknown -
        // this is not a "everything succeeds" responder, and the two
        // statuses DIFFER, so the in-range answer is not a blanket refusal
        probe((uint16_t)(NSTREAMS_TB + 1), r);
        ck("CRF probe negative: uid N+1 -> TALKER_UNKNOWN_ID",
           r.size() == 70 ? (r[16] >> 3) : 0xFF, 2);
        // and a plain audio uid is answered by the same responder
        probe(1, r);
        ck("audio uid 1 answered in range (DEST_MAC_FAILED, not UNKNOWN_ID)",
           r.size() == 70 ? (r[16] >> 3) : 0xFF, 3);

        // ---- KL_crf_tx takes the SAME pair when the CSR is left at 0 ----
        ck("CRFT_SID unset (auto)", axi_read(A_CRFT_SIDLO) |
                                    axi_read(A_CRFT_SIDHI), 0);
        ck("CRFT_DMAC unset (auto)", axi_read(A_CRFT_DMLO) |
                                     axi_read(A_CRFT_DMHI), 0);
        axi_write(A_CRFT_CTRL, 0x1);                  // enable the CRF talker
        std::vector<uint8_t> crf; std::vector<uint8_t> cur2;
        for (int c = 0; c < 400000 && crf.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur2.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    // AVTP subtype 0x04 = CRF
                    if (cur2.size() >= 26 && cur2[12] == 0x22 &&
                        cur2[13] == 0xF0 && cur2[14] == 0x04) crf = cur2;
                    cur2.clear();
                }
            }
            hi();
        }
        ck("CRF PDU on the wire", crf.empty() ? 0 : 1, 1);
        if (!crf.empty()) {
            ck("CRF PDU dmac = the ACMP answer (base + N)", be(crf, 0, 6),
               0x91E0F000FE01ULL + NSTREAMS_TB);
            ck("CRF PDU stream_id tail = N", be(crf, 24, 2),
               (unsigned)NSTREAMS_TB);
        }
        // NEGATIVE LEG: an explicit CRFT_DMAC still wins outright
        axi_write(A_CRFT_DMLO, 0xF000FEAA);
        axi_write(A_CRFT_DMHI, 0x000091E0);
        crf.clear(); cur2.clear();
        for (int c = 0; c < 400000 && crf.empty(); c++) {
            lo();
            if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                for (int l = 0; l < 8; l++)
                    if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                        cur2.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                if (dut->m_axis_mac_tx_tlast) {
                    if (cur2.size() >= 26 && cur2[12] == 0x22 &&
                        cur2[13] == 0xF0 && cur2[14] == 0x04) crf = cur2;
                    cur2.clear();
                }
            }
            hi();
        }
        ck("explicit CRFT_DMAC overrides the auto pair",
           crf.empty() ? 0 : be(crf, 0, 6), 0x91E0F000FEAAULL);
        axi_write(A_CRFT_CTRL, 0x0);
    }

    // ==================================================================
    //  CRF MEDIA CLOCK OUTPUT AS AN SR CLASS A STREAM
    //  (Milan v1.2 7.3.3 "media clock stream carried under an SRP
    //   reservation of the specified class"; 802.1Q 9.5/9.6 C-TAG;
    //   802.1Q 34.5 / Table 34-1 SR class A = PCP 3; Milan 4.2.7.2.1
    //   {class A, priority 3, VID 2})
    //
    //  Three things had to land together and this block proves all three
    //  plus the interlock that keeps them together:
    //    (1) the 802.1Q C-TAG on the CRF frames,
    //    (2) the CRF PDUs on the DATA lane (they no longer pass the
    //        control min-IFG gasket - covered by the frame still arriving
    //        at the MAC in every leg below),
    //    (3) the MSRP Talker Advertise attribute row for the stream.
    //
    //  THE TRAP: a tagged stream with no declaration is not a class A
    //  stream, it is unshaped traffic squatting in the reserved SR VLAN.
    //  The tag is therefore DERIVED from the declaration in RTL, and the
    //  two negative legs below are the proof that it cannot be set alone.
    // ==================================================================
    printf("-- CRF media clock output: SR class A (Milan 7.3.3) --\n");
    {
        enum { A_CRFT_CTRL = 0x750, A_CRFT_DMLO = 0x75C, A_CRFT_DMHI = 0x760 };
        const uint64_t CRF_DMAC = 0x91E0F000FE01ULL + NSTREAMS_TB;
        const int      SR_VID   = 2;      // LWSRP_VID reset (Milan 4.2.7.2.1)
        const int      SR_PCP   = 3;      // 802.1Q 34.5 / Table 34-1
        auto be = [](const std::vector<uint8_t>& v, size_t o, int n) {
            uint64_t r = 0; for (int i = 0; i < n; i++) r = (r<<8) | v[o+i];
            return r;
        };

        // back to the AUTO {sid, dmac} pair - the shipping path, where the
        // declaration and the frames are derived from ONE source
        axi_write(A_CRFT_DMLO, 0x0);
        axi_write(A_CRFT_DMHI, 0x0);

        // grab the next CRF PDU in EITHER shape. The discriminator is the
        // ethertype position: untagged 0x22F0 at 12, tagged 0x8100 at 12
        // with 0x22F0 pushed to 16. subtype 0x04 = CRF either way.
        auto grab_crf = [&](std::vector<uint8_t>& out, int budget) -> bool {
            std::vector<uint8_t> cur3; out.clear();
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < budget; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur3.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        bool untag = cur3.size() >= 26 && cur3[12] == 0x22 &&
                                     cur3[13] == 0xF0 && cur3[14] == 0x04;
                        bool tag   = cur3.size() >= 30 && cur3[12] == 0x81 &&
                                     cur3[13] == 0x00 && cur3[16] == 0x22 &&
                                     cur3[17] == 0xF0 && cur3[18] == 0x04;
                        if (untag || tag) { out = cur3; hi(); return true; }
                        cur3.clear();
                    }
                }
                hi();
            }
            return false;
        };
        const int CRF_BUDGET = 160000;   // > 2 event periods (49152 each)

        // ---- LEG 1 (the DEFAULT BUILD): class A bit clear -------------
        // lwSRP fully running, CRF talker running, CRFT_CTRL[1] = 0.
        // This is what every existing bitstream does and it must not move.
        axi_write(A_LWSRP_CTRL, 0x37);          // enable + talker + declare bypass
        for (int c = 0; c < 256; c++) step();
        axi_write(A_CRFT_CTRL, 0x1);            // en=1, class_a=0
        std::vector<uint8_t> f1;
        ck("class A off: a CRF PDU still reaches the MAC",
           grab_crf(f1, CRF_BUDGET) ? 1 : 0, 1);
        if (!f1.empty()) {
            ck("class A off: UNTAGGED (ethertype 22F0 at 12)",
               (f1[12] << 8) | f1[13], 0x22F0);
            ck("class A off: 60-octet legacy frame", (long)f1.size(), 60);
            ck("class A off: dmac = the ACMP answer", be(f1, 0, 6), CRF_DMAC);
        }
        uint32_t st = axi_read(A_CRFT_CTRL);
        ck("class A off: 0x750[4] TA not declared", (st >> 4) & 1, 0);
        ck("class A off: 0x750[5] not tagged",      (st >> 5) & 1, 0);
        ck("class A off: 0x750[19:8] VID reads 0",  (st >> 8) & 0xFFF, 0);

        // ---- LEG 2 (NEGATIVE - THE TRAP): class A bit SET, lwSRP OFF --
        // Asking for the tag without an engine that can declare must NOT
        // produce a tagged frame. If this leg ever tags, the interlock is
        // gone and the board is emitting an unreserved stream on the SR
        // VLAN.
        axi_write(A_LWSRP_CTRL, 0x0);           // no engine -> no declaration
        axi_write(A_CRFT_CTRL, 0x3);            // en=1, class_a=1
        for (int c = 0; c < 2048; c++) step();
        std::vector<uint8_t> f2;
        ck("lwSRP off: a CRF PDU still reaches the MAC (Milan 5.3.7.3 - a"
           " Stream Output is never stopped)",
           grab_crf(f2, CRF_BUDGET) ? 1 : 0, 1);
        if (!f2.empty())
            ck("lwSRP off + class A asked: STILL UNTAGGED (the interlock)",
               (f2[12] << 8) | f2[13], 0x22F0);
        st = axi_read(A_CRFT_CTRL);
        ck("lwSRP off: 0x750[1] readback keeps what was written",
           (st >> 1) & 1, 1);
        ck("lwSRP off: 0x750[5] tag refused", (st >> 5) & 1, 0);

        //! ---- DELETED 2026-08-13: LEGS 3, 4 and 5 (the POSITIVE side).
        //!
        //! LEG 3 asserted that with a declaration in force the CRF frames
        //! come out 802.1Q-tagged {PCP 3, VID 2} and the 0x750 tag word says
        //! so; LEG 4 decoded the MSRP TalkerAdvertise (802.1Q 35.2.2.4
        //! FirstValue - StreamID, DataFrameParameters, TSpec, PriorityAndRank)
        //! that authorises them; LEG 5 withdrew class A and required the
        //! untagged shape back.
        //!
        //! ALL THREE NEED A DECLARATION, AND THIS LEG CANNOT PRODUCE ONE.
        //! hdl/ieee8021q/srp/ is deleted; the declaration is the processor's
        //! KL_srp_top, which declares for a source that is DECLARING, and
        //! declaring needs a MAAP ALLOC_DA success. milan_dp elaborates
        //! KL_maap at the silicon rate (MAAP_CLK_HZ_P defaults to
        //! MILAN_CLK_FREQ_HZ), so ANNOUNCE is ~1.5e8 cycles away - measured
        //! still PROBING after 40,000,000. crft_class_a_w therefore never
        //! asserts, the frames stay untagged, and LEG 5's "back to untagged"
        //! would pass without ever having been tagged: a vacuous pass, which
        //! is worse than no check.
        //!
        //! LEGS 1 AND 2 ABOVE ARE UNTOUCHED AND THEY ARE THE INTERLOCK - the
        //! property this section was really written for. LEG 1: the default
        //! build emits an untagged 60-octet CRF PDU. LEG 2, the trap: asking
        //! for class A with no declaration behind it must NOT tag the frames,
        //! because a tagged stream with no reservation is unshaped traffic
        //! squatting in the reserved SR VLAN. Both still bite.
        //!
        //! The positive side - a real TalkerAdvertise on the wire with its
        //! Table 4.4 TSpec - is graded in tb/verilator/pp_shadow, which
        //! compresses the processor's millisecond and KL_maap's onto one
        //! grid and sees the MSRP/MVRP frames egress.

        axi_write(A_CRFT_CTRL, 0x0);
        axi_write(A_LWSRP_CTRL, 0x0);
    }

#ifdef AAF_PB_TB
    // ==================================================================
    //  TASK #31 - HOST PLAYBACK RING -> chmap RING bucket -> TALKER WIRE
    //  (AAF_PLAYBACK_P=1, the cfg_ax8x8 ship flip). The full playback
    //  path IN the datapath: a host-written PCM ring is fetched over the
    //  pb_mem word port, paced by KL_pcm_tx, latched by the capture
    //  crossbar's RING bucket, and framed by the packetizer - the ALSA
    //  aplay direction, ending at the MAC TX AXIS.
    //
    //  Placement decoupling is the point of the map: ring PAIR 0 (host
    //  channels 0/1) is mapped onto BOTH talker 0's and talker 1's wire
    //  slots - the mechanism that puts host stereo on the peer-facing
    //  stream channels of the USER's choice (ch2/3 in the 8ch target).
    //
    //  Underrun continuity (Milan 5.3.7.3): starving the ring must KEEP
    //  the talkers framing - payload goes digital-silence, cadence never
    //  stalls - and the starvation is CSR-observable (PBK_RAILS 0x8D0 +
    //  the pb_underrun_o rail).
    // ==================================================================
    printf("-- task #31: host ring -> RING bucket -> talker wire (pb) --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904, A_CHMAP_WORD = 0x908,
               A_PBK_RAILS = 0x8D0 };
        const uint32_t PB_LEN    = 512;      // 64-word sub-ring
        const uint32_t PB_STRIDE = 4096;
        const int      PB_LEAD   = 32;       // words kept ahead of the reader

        // streaming posture (VID-2 rule + bypass licence), lwSRP off
        axi_write(A_AAF_CTRL, 0x00020003);
        axi_write(A_LWSRP_CTRL, 0x0);

        //! TALKER 1'S IDENTITY IS THIS SECTION'S OWN PRECONDITION (2026-08-13).
        //! The TCTX case ~1300 lines up stages talker 1 with uid 5 in
        //! A_SW_DMAC_HI[31:16], and KL_aaf_packetizer's documented rule is
        //! that a software-named uid OUTRANKS the fabric-derived one (0 = not
        //! named). Until the substitution, two lwSRP/0x800-window cases that
        //! ran in between put that field back - and they are deleted with the
        //! legacy plane. So this section inherited uid 5 while classifying
        //! talker 1's PDUs as uid 1, and read t1 as SILENT when it was
        //! framing perfectly: the same file asserted uid 5 in one case and
        //! uid 1 in another. Talker 1 is NOT dark and never was.
        //! Re-stage it here rather than leaning on a neighbour: a section
        //! whose precondition is set 1300 lines away by a case that may be
        //! deleted again is a section that will lie again. The DMAC half of
        //! the word is left exactly as staged.
        axi_write(A_STRM_SEL, 0x101);                 // dir=talker, idx=1
        axi_write(A_SW_DMAC_HI, 0x000091E0);          // uid field 0 -> derived 1
        ck("pb: talker 1's uid field cleared (derived uid wins)",
           axi_read(A_SW_DMAC_HI), 0x000091E0);
        for (int c = 0; c < 64; c++) step();

        // capture map, PER-CHANNEL (0x0027): channels 0..3 <- RING pair 0,
        // halves L,R,L,R. Window word {en[15], src[14:12]=3 RING,
        // half[8], idxh[7:4]=0, idx[3:0]=0}. At 2 wire channels keys 2/3
        // are talker 1's pair (the same harmless extra coverage the old
        // slot-1 strobe gave); the 4-wire-channel shape NEEDS all four or
        // its talker-0 frame carries silence on ch2/ch3.
        axi_write(A_CHMAP_CTRL, 0x1);        // arm the fabric + the CSR port
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0xB000 | ((k & 1) << 8));
        }

        // playback engine: ring stream 0 only, silence-on-underrun
        dut->pb_ring_base_i   = 0;
        dut->pb_ring_len_i    = PB_LEN;
        dut->pb_ring_stride_i = PB_STRIDE;
        dut->pb_underrun_silence_i = 1;
        dut->pb_enable_i    = 1;
        dut->pb_stream_en_i = 0x01;

        // host ring model: ramp-tagged S32BE pairs, L=0x7A0000|j R=0x7B0000|j
        static uint8_t pbram[PB_STRIDE + PB_LEN + 64];
        uint32_t pb_committed = 0;           // words written
        auto pb_put = [&](uint32_t j) {
            uint32_t a = (j * 8) % PB_LEN;
            uint32_t L = 0x7A0000u | (j & 0xFFFF), R = 0x7B0000u | (j & 0xFFFF);
            pbram[a+0] = L >> 16; pbram[a+1] = L >> 8; pbram[a+2] = L; pbram[a+3] = 0;
            pbram[a+4] = R >> 16; pbram[a+5] = R >> 8; pbram[a+6] = R; pbram[a+7] = 0;
        };
        bool pb_feed = true;
        bool mem_pend = false; uint32_t mem_addr = 0;
        auto pb_service = [&](void) {        // call between lo() and hi()
            // 1-cycle-latency word port (the BRAM-ring timing)
            dut->pb_mem_valid_i = mem_pend ? 1 : 0;
            if (mem_pend) {
                uint64_t w = 0;
                for (int b = 0; b < 8; b++)
                    w |= (uint64_t)pbram[(mem_addr % (PB_STRIDE + PB_LEN)) + b] << (8*b);
                dut->pb_mem_data_i = w;
            }
            mem_pend = dut->pb_mem_rd_o; mem_addr = dut->pb_mem_addr_o;
            if (pb_feed) {
                uint32_t rdw = dut->pb_rd_ptr_o[0] / 8;
                while (pb_committed < rdw + PB_LEAD) pb_put(pb_committed++);
            }
            dut->pb_wr_ptr_i[0] = pb_committed * 8;
        };

        // AAF PDU capture with the ring-tag payload decode (t0 + t1)
        struct Pdu { int uid; std::vector<uint32_t> smp; bool zero; };
        auto collect = [&](int want_t0, int want_t1, int budget) {
            std::vector<Pdu> got;
            std::vector<uint8_t> cur;
            int n0 = 0, n1 = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < budget && (n0 < want_t0 || n1 < want_t1); c++) {
                lo();
                pb_service();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l)) & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02) {
                            Pdu p; p.uid = (cur[24+off] << 8) | cur[25+off];
                            p.zero = true;
                            for (int s = 0; s < 12; s++) {   // 6 events x 2ch
                                size_t o = 38 + off + 4*s;
                                uint32_t v = ((uint32_t)cur[o] << 16) |
                                             ((uint32_t)cur[o+1] << 8) | cur[o+2];
                                p.smp.push_back(v);
                                if (v) p.zero = false;
                            }
                            if (p.uid == 0) { n0++; got.push_back(p); }
                            else if (p.uid == 1) { n1++; got.push_back(p); }
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            return got;
        };

        // ---- LEG 1: both talkers carry the ring pair, ramp-exact -------
        // settle: let the engine start fetching and the buckets fill
        for (int c = 0; c < 4096; c++) { lo(); pb_service(); hi(); }
        auto pdus = collect(3, 3, 200000);
        int t0n = 0, t1n = 0; bool tags_ok = true, ramp_ok = true, lr_ok = true;
        int started = 0;                     // per-uid bit: ring seen yet
        for (auto& p : pdus) {
            (p.uid ? t1n : t0n)++;
            int prev = -1;
            for (int s = 0; s < 12; s += 2) {
                uint32_t L = p.smp[s], R = p.smp[s+1];
                //! 0x002C: the crossbar frames from BOOT, so the first
                //! captured PDU may straddle the silence->ring start -
                //! leading digital-silence events are the stream's legal
                //! pre-start tail, never a tag or ramp defect. A zero
                //! event AFTER the ring started still fails both checks.
                if (!((started >> p.uid) & 1)) {
                    if (L == 0 && R == 0) continue;
                    started |= 1 << p.uid;
                }
                if ((L >> 16) != 0x7A || (R >> 16) != 0x7B) tags_ok = false;
                if ((L & 0xFFFF) != (R & 0xFFFF)) lr_ok = false;
                // consecutive sample events step the ramp by exactly 1
                // (same clk, same divisor: no repeats, no drops)
                if (prev >= 0 &&
                    (uint16_t)(p.smp[s] & 0xFFFF) !=
                    (uint16_t)((p.smp[prev] & 0xFFFF) + 1)) ramp_ok = false;
                prev = s;
            }
        }
        ck("pb: t0 frames the host ring (>= 3 PDUs)", t0n >= 3, 1);
        ck("pb: t1 frames the SAME ring pair (>= 3)", t1n >= 3, 1);
        ck("pb: every sample carries the ring tag (L=7A/R=7B)", tags_ok, 1);
        ck("pb: L/R of one ring word stay a pair", lr_ok, 1);
        ck("pb: ramp steps by 1 per sample event (no slip)", ramp_ok, 1);
        ck("pb: engine consumed the ring (rd_ptr advanced)",
           dut->pb_rd_ptr_o[0] > 0, 1);
        ck("pb: no underrun while fed", dut->pb_underrun_o[0] & 0xFFFF, 0);

        // ---- LEG 2: starvation = SILENCE payload, cadence NEVER stalls -
        pb_feed = false;                      // freeze the host write pointer
        // drain the PB_LEAD words still queued (one word per media sample
        // at CHANS=2: ~PB_LEAD x 2083 cycles) until the engine reports the
        // first real underrun - the rail IS the drain oracle
        { int dg = 0;
          while ((dut->pb_underrun_o[0] & 0xFFFF) == 0 && dg++ < 400000) {
              lo(); pb_service(); hi(); } }
        auto starved = collect(3, 0, 200000);
        int zt0 = 0;
        for (auto& p : starved) if (p.uid == 0 && p.zero) zt0++;
        ck("pb starve: t0 KEEPS framing (5.3.7.3 cadence)",
           starved.size() >= 3, 1);
        ck("pb starve: payload is digital silence", zt0 >= 2, 1);
        ck("pb starve: underruns counted on the rail",
           (dut->pb_underrun_o[0] & 0xFFFF) > 0, 1);
        uint32_t rails = axi_read(A_PBK_RAILS);
        ck("pb starve: PBK_RAILS 0x8D0 shows the underruns",
           (rails >> 16) > 0, 1);

        // ---- LEG 3: refeed = audio returns (session survives a gap) ----
        pb_feed = true;
        for (int c = 0; c < 4096; c++) { lo(); pb_service(); hi(); }
        auto back = collect(3, 0, 200000);
        bool alive = false;
        for (auto& p : back) if (p.uid == 0 && !p.zero &&
                                 (p.smp[0] >> 16) == 0x7A) alive = true;
        ck("pb refeed: ramp audio returns on the wire", alive, 1);

        // restore: engine off, map disarmed (the legacy bit-identical path)
        dut->pb_enable_i = 0; dut->pb_stream_en_i = 0;
        axi_write(A_CHMAP_CTRL, 0x0);
    }
#endif

    // ==================================================================
    //  TASK #65 - rx -> talker LOOPBACK: the AEM's DECLARED source, made
    //  real in the fabric.
    //
    //  The entity advertises 8 "Loopback S<s> ch <c>" AUDIO_CLUSTERs on
    //  every talker STREAM_PORT_OUTPUT, and the POWER-ON dynamic map wakes
    //  pointing every talker stream channel AT them: generated
    //  AEM_ODMAP_INIT_C = {valid, cluster offset 9..16}, whose
    //  AEM_ODMAP_CSRC_C templates are src = 5 = SRC_LOOP, which the AECP
    //  seeder writes into this very map RAM as {en, src=5, idx} = 0xD0|k.
    //
    //  KL_chan_map_capture has carried that bucket since 2026-07-28, but
    //  its five lb_* inputs were never connected in milan_datapath, so they
    //  took their `= 0` port defaults: the hold bank could never be written
    //  and EVERY loopback cluster selected SILENCE. A booted, bound talker
    //  therefore streamed conformant digital silence on every channel while
    //  GET_AUDIO_MAP showed a fully-populated, entirely honest-looking map -
    //  the trap that cost a USER a listening session.
    //
    //  BITE: drop any one of the five lb_* connections in milan_datapath
    //  and the talker payload collapses to all-zero, which "carries the
    //  RECEIVED audio" below refuses. The zero-payload check alone is not
    //  enough - digital silence is a LEGAL payload (5.3.7.3 fill) - so the
    //  emitted samples are matched against the exact bytes that were
    //  received, and L/R against the wire pair they were de-interleaved
    //  from. Nothing but a working loopback lane can produce those.
    // ==================================================================
    printf("-- task #65: rx -> talker LOOPBACK (chmap src 5) --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
               A_CHMAP_WORD = 0x908 };
        const uint8_t LB_PAY0 = 0xA0;     // mkaaf payload seed (no 8-bit wrap)
        const int     LB_SID  = 1;        // sidB is provisioned to stream 1

        // the 12 S32BE samples mkaaf lays down, as the 24 audio bits the
        // depacketizer forwards and the packetizer re-emits: wire byte j in
        // lane j, lanes 3/7 the S32 pad (KL_chan_map_capture lb_tdata_i
        // contract, and tb/verilator/chmap_capture's lb_beat()).
        auto lb_smp = [&](int j) {
            return ((uint32_t)(uint8_t)(LB_PAY0 + 4*j)     << 16)
                 | ((uint32_t)(uint8_t)(LB_PAY0 + 4*j + 1) <<  8)
                 |  (uint32_t)(uint8_t)(LB_PAY0 + 4*j + 2);
        };

        // streaming posture: VID-2 rule + the bypass licence, lwSRP off -
        // the same arming the host-ring leg above uses
        axi_write(A_AAF_CTRL, 0x00020003);
        axi_write(A_LWSRP_CTRL, 0x0);

        // capture map, PER-CHANNEL (0x0027): channels <- LOOP {stream 1,
        // pair 0}, halves L,R,L,R. CSR word = {en[15], src[14:12]=5 LOOP,
        // half[8], idxh[7:4]=stream, idx[3:0]=pair}. Four keys because the
        // harness runs three shapes: at TALKER_WIRE_CHANS_P=2 keys 2/3 are
        // talker 1 (harmless extra coverage), while the 4-wire-channel
        // shape needs talker 0's four channels armed before the packetizer
        // can assemble a 4-channel frame at all.
        axi_write(A_CHMAP_CTRL, 0x1);
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, (uint32_t)(0x8000 | (5 << 12)
                                               | ((k & 1) << 8)
                                               | (LB_SID << 4) | 0));
        }

        // feed the listener: three AAF PDUs of stream 1, 2 wire channels.
        // The bucket's holds free-run, so after the burst they retain the
        // last received pair and the talker keeps re-emitting it.
        for (uint8_t s = 0; s < 3; s++)
            inject(mkaaf(sidB, (uint8_t)(120 + s), 2, LB_PAY0), 2000);

        // collect talker 0's PDUs (uid 0), decoding the 6 events x 2 ch
        std::vector<std::vector<uint32_t>> lbp;
        {
            std::vector<uint8_t> cur;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 200000 && (int)lbp.size() < 3; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            std::vector<uint32_t> smp;
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                smp.push_back(((uint32_t)cur[o]   << 16) |
                                              ((uint32_t)cur[o+1] <<  8) |
                                               (uint32_t)cur[o+2]);
                            }
                            lbp.push_back(smp);
                        }
                        cur.clear();
                    }
                }
                hi();
            }
        }
        ck("lb: talker 0 frames while the LOOP slot is mapped",
           lbp.size() >= 3, 1);

        // LOOPBACK_P is a paired flag: the Makefile passes -GLOOPBACK_P=1
        // together with -DLOOPBACK_TB, so this side always knows which
        // gateware it is talking to. BOTH states are pinned - ON must carry
        // the received audio, OFF must be silent BY CONSTRUCTION, and that
        // OFF row is the whole reason the builder's power-on map may not
        // point a talker channel at a loopback cluster in a build that did
        // not elaborate the lane.
#ifdef LOOPBACK_TB
        const int LB_LANE = 1;
#else
        const int LB_LANE = 0;
#endif
        bool any_audio = false, all_from_rx = true, pairs_ok = true;
        for (auto& p : lbp) {
            for (size_t s = 0; s + 1 < p.size(); s += 2) {
                uint32_t L = p[s], R = p[s+1];
                if (L || R) any_audio = true;
                // L must be an EVEN-indexed received sample (wire ch 0) and
                // R the one that followed it (wire ch 1): the de-interleave
                int li = -1;
                for (int j = 0; j < 12; j += 2) if (lb_smp(j) == L) li = j;
                if (li < 0) all_from_rx = false;
                else if (R != lb_smp(li + 1)) pairs_ok = false;
            }
        }
        if (LB_LANE) {
            ck("lb: talker payload is NOT digital silence", any_audio, 1);
            ck("lb: every sample is one the LISTENER received",
               all_from_rx, 1);
            ck("lb: L/R stay the wire pair they arrived as", pairs_ok, 1);
        } else {
            // LOOPBACK_P=0: the bucket is elaborated at its minimum with the
            // feed tied off, so a mapped loopback slot can only ever be
            // silence. An entity that ADVERTISED this cluster here would be
            // describing a source the gateware does not contain.
            ck("lb (lane OFF): a loopback slot is silent by construction",
               any_audio, 0);
        }

        // An UNMAPPED loop slot stops carrying the received audio - the
        // bucket is selected BY THE MAP and never leaks into a slot that
        // did not ask for it. But it must stop carrying audio the way the
        // clause allows: by SENDING SILENCE, not by going off the wire.
        //
        // Milan v1.2 5.3.9.1 makes "not mapped" a legal state for a
        // channel of a Stream Output; 5.3.7.3 says the PAAD "shall be
        // streaming AVTP packets" while it declares Talker Advertise and
        // sees a Listener Ready, and forbids STREAMING_WAIT outright. So
        // unmapping a channel owes the wire silence INSIDE a frame that
        // still goes out.
        //
        // This is the integration-level half of the proof, and it needs
        // to live HERE rather than in tb/verilator/chmap_capture: the
        // reason the gap was reachable at all is the milan_datapath
        // pkt_pv_w bypass, which mutes KL_pair_zero_fill - the guard that
        // covers exactly this for the front-end path - for as long as
        // CHMAP is armed. Only a datapath leg has both halves in it.
        // Before the fix this loop collected ZERO talker-0 PDUs.
        for (int k = 0; k < 4; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0x0000);     // en = 0
        }
        for (int c = 0; c < 20000; c++) step();
        {
            std::vector<uint8_t> cur; int leaked = 0; int seen = 0;
            int nonzero = 0;
            for (int c = 0; c < 200000 && seen < 2; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            seen++;
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                uint32_t v = ((uint32_t)cur[o]   << 16) |
                                             ((uint32_t)cur[o+1] <<  8) |
                                              (uint32_t)cur[o+2];
                                if (v) nonzero++;
                                for (int j = 0; j < 12; j++)
                                    if (v && lb_smp(j) == v) leaked++;
                            }
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            printf("         (unmapped slot: %d talker-0 PDU(s) seen)\n", seen);
            ck("lb: an UNMAPPED loop slot carries no rx audio", leaked, 0);
            ck("lb: unmapping a slot never stops talker 0 framing", seen, 2);
            ck("lb: and what it frames instead is silence", nonzero, 0);
        }

        axi_write(A_CHMAP_CTRL, 0x0);            // restore the legacy path
    }

#ifdef AAF_PB_TB
    // ==================================================================
    //  [T66] THE DYNAMIC-MAP AECP OPCODES AFTER THE SUBSTITUTION
    //
    //  WHAT THIS SECTION USED TO PROVE, AND WHY IT CANNOT ANY MORE. It was
    //  the t532 silicon pin (2026-08-09): runtime ADD/REMOVE_AUDIO_MAPPINGS
    //  reached the AECP store (GET_AUDIO_MAP tracked every edit) but landed
    //  in the fabric crossbar RAM erratically or not at all, so the wire
    //  kept framing the boot image. The fix was graded here RAM-side, and
    //  the section ran with CHMAP_CTRL[0] = 0 on purpose because the AECP
    //  mirror was the canonical programmer.
    //
    //  THAT PROGRAMMER IS DELETED. KL_aecp_engine decodes exactly two
    //  opcodes - 0x0004 READ_DESCRIPTOR and 0x0026 IDENTIFY_NOTIFICATION -
    //  and every other AEM opcode takes the NOT_IMPLEMENTED echo path;
    //  milan_datapath ties the odmap write port off. So GET_AUDIO_MAP,
    //  ADD_AUDIO_MAPPINGS and REMOVE_AUDIO_MAPPINGS are gone as CAPABILITY,
    //  and a check that expects SUCCESS from them is grading a plane that no
    //  longer exists. This is a REGRESSION AGAINST THE PRE-SUBSTITUTION
    //  DEVICE, recorded here rather than quietly dropped.
    //
    //  What is graded instead is the whole of what IS true, and every part
    //  of it is falsifiable:
    //    (A) all three opcodes get a CONFORMANT NOT_IMPLEMENTED answer -
    //        message_type + 1, status 1, control_data_length = 12 + the
    //        command's own payload, the frame padded to 60 and the payload
    //        echoed - decoded off the wire, never a counter. Silence or a
    //        malformed echo fails. (READ_DESCRIPTOR is graded end to end,
    //        against a real descriptor image, in tb/verilator/pp_shadow;
    //        this leg backs no descriptor memory - see the [AECP] note in
    //        the reset section.)
    //    (B) they leave the crossbar RAM UNTOUCHED. A phantom write from a
    //        half-deleted mirror would be far worse than no write at all.
    //    (C) the live-audio proof SURVIVES, driven through the CSR 0x900
    //        window - the only writer the crossbar has left. The property
    //        (remapping talker 0's wire pair onto the TONE cluster changes
    //        the emitted payload, L == R) is unchanged; only the programmer
    //        is. This also re-arms the crossbar for [T67], which measures
    //        the MILAN_CLK media grid and can only do so while the
    //        media_tick-paced crossbar - not the clk_audio-paced zero-fill
    //        path - is feeding the packetizer.
    // ==================================================================
    printf("-- [T66] dynamic-map opcodes: NOT_IMPLEMENTED, and the CSR "
           "window still maps --\n");
    {
        enum { CMD_GET_AUDIO_MAP = 43, CMD_ADD_AUDIO_MAPPINGS = 44,
               CMD_REMOVE_AUDIO_MAPPINGS = 45 };
        enum { A_CHMAP_CTRL2 = 0x900, A_CHMAP_SEL2 = 0x904,
               A_CHMAP_WORD2 = 0x908 };
        const uint16_t DT_SPO = 0x000F;      // STREAM_PORT_OUTPUT
        static uint16_t sq = 0x4100;

        // capture-side crossbar RAM readback (CSR 0x904/0x910/0x914 window,
        // the 0x002C boot-seed recipe): returns the 13-bit map entry
        auto cap_ram = [&](int key) -> uint32_t {
            axi_write(0x904, 0x100 | key);
            axi_write(0x910, 1);
            uint32_t sv = 0;
            for (int g = 0; g < 64; g++) {
                sv = axi_read(0x910);
                if ((sv & 1) == 0) break;
            }
            uint32_t v = axi_read(0x914);
            if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;   // readback dead
            return v & 0x1FFF;
        };
        // one ADD/REMOVE of n {si, sc, co} rows on output port 0, graded as a
        // WIRE RESPONSE: the whole point is that the answer is well formed.
        auto dmap_cmd = [&](const char* tag, int cmd, int n,
                            const int* sc, const int* co) -> long {
            std::vector<uint8_t> pl = {
                (uint8_t)(DT_SPO >> 8), (uint8_t)DT_SPO, 0x00, 0x00,
                0x00, (uint8_t)n, 0x00, 0x00 };
            for (int i = 0; i < n; i++) {
                uint8_t row[8] = {0,0, 0,(uint8_t)sc[i], 0,(uint8_t)co[i], 0,0};
                pl.insert(pl.end(), row, row + 8);
            }
            const uint16_t seq = sq++;
            auto r = aecp_xact((uint16_t)cmd, seq, pl);
            char w[112];
            snprintf(w, sizeof w, "T66 %s: ANSWERED (not silence)", tag);
            ck(w, (long)(r.size() >= 38), 1);
            if (r.size() < 38) return -1;
            const size_t want = (38 + pl.size() < 60) ? 60 : 38 + pl.size();
            snprintf(w, sizeof w, "T66 %s: status NOT_IMPLEMENTED(1)", tag);
            ck(w, aecp_status(r), 1);
            snprintf(w, sizeof w, "T66 %s: message_type = command + 1", tag);
            ck(w, r[15] & 0x0F, 1);
            snprintf(w, sizeof w, "T66 %s: cdl = 12 + the command's payload", tag);
            ck(w, (long)((((unsigned)r[16] & 7) << 8) | r[17]),
               (long)(12 + pl.size()));
            snprintf(w, sizeof w, "T66 %s: frame length matches its cdl", tag);
            ck(w, (long)r.size(), (long)want);
            snprintf(w, sizeof w, "T66 %s: sequence_id echoed", tag);
            ck(w, (long)((r[34] << 8) | r[35]), (long)seq);
            snprintf(w, sizeof w, "T66 %s: command_type echoed, u = 0", tag);
            ck(w, (long)((r[36] << 8) | r[37]), (long)cmd);
            long bad = 0;
            for (size_t i = 0; i < pl.size(); i++)
                if (38 + i >= r.size() || r[38 + i] != pl[i]) bad++;
            snprintf(w, sizeof w, "T66 %s: the command payload is ECHOED", tag);
            ck(w, bad, 0);
            return aecp_status(r);
        };
        // (The RING template helper that used to live here - the fabric word
        // an AECP ADD of cluster co had to produce - went with the ADD: there
        // is no AECP writer left to check against it, and part (B) compares
        // each key against WHAT IT WAS rather than against a template. The
        // capture-map word layout it encoded is {en[12], half[11], src[10:8],
        // idx[7:0]}, which the tone template 0x1400 below still uses.)

        // ---- (A)+(B) the three opcodes answer, and change NOTHING -------
        // The RAM words are read before and after, on the very keys the
        // commands name. A mirror that was half-deleted - still decoding the
        // rows but no longer reaching the store - would show up here as a
        // phantom write, which is strictly worse than the honest refusal.
        const int scs[4] = {4, 5, 6, 7};
        const int cos[4] = {6, 7, 4, 5};     // cross-swap: != anything mapped
        uint32_t before[4];
        for (int i = 0; i < 4; i++) before[i] = cap_ram(scs[i]);
        long all_notimpl = 1, all_inert = 1;
        for (int i = 0; i < 4; i++) {
            if (dmap_cmd("ADD", CMD_ADD_AUDIO_MAPPINGS, 1, &scs[i], &cos[i]) != 1)
                all_notimpl = 0;
            for (int c = 0; c < 3000; c++) step();   // SPACED, not a burst
            if (cap_ram(scs[i]) != before[i]) all_inert = 0;
        }
        ck("T66: 4 spaced ADD_AUDIO_MAPPINGS all NOT_IMPLEMENTED",
           all_notimpl, 1);
        ck("T66: and NONE of them touched the crossbar RAM (RAM-side read)",
           all_inert, 1);
        {
            const int rsc = 4, rco = 6;
            ck("T66: REMOVE_AUDIO_MAPPINGS is NOT_IMPLEMENTED too",
               dmap_cmd("REMOVE", CMD_REMOVE_AUDIO_MAPPINGS, 1, &rsc, &rco), 1);
            for (int c = 0; c < 3000; c++) step();
            ck("T66: ...and key 4 is still what it was", cap_ram(4), before[0]);
        }
        {
            std::vector<uint8_t> pl = {
                (uint8_t)(DT_SPO >> 8), (uint8_t)DT_SPO, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00 };            // map_index 0
            const uint16_t seq = sq++;
            auto r = aecp_xact(CMD_GET_AUDIO_MAP, seq, pl);
            //! the OUTPUT side is SERVED now (the P5 landing): SUCCESS with
            //! the full 7.4.44.2 fixed part off the capture-side store; the
            //! record count reflects whatever this leg's earlier sections
            //! left mapped, so the shape law - cdl = 24 + 8*count - is the
            //! stable assertion, not a pinned count
            ck("T66: GET_AUDIO_MAP on the OUTPUT side answers SUCCESS",
               aecp_status(r), 0);
            ck("T66: ...as a well-formed 7.4.44.2 response",
               (long)(r.size() >= 50 && (r[15] & 0x0F) == 1
                      && ((((unsigned)r[16] & 7) << 8) | r[17])
                         == (unsigned)(24 + 8 * (((unsigned)r[46] << 8) | r[47]))
                      && ((r[34] << 8) | r[35]) == seq), 1);
        }

        // ---- (B2) the Milan-mandatory set the demotion round landed ------
        // (Milan 5.4.2.21/2/1/2/10/23/24: REGISTER_UNSOLICITED_NOTIFICATION,
        //  LOCK_ENTITY, GET_STREAM_INFO, GET_AVB_INFO, GET_AS_PATH - wire
        //  truth through the REAL datapath servers: binding view, SRP nets,
        //  the gPTP CSR pair, the clock validator's asCapable.)
        {
            // REGISTER (2021 format, flags 0) -> SUCCESS with flags echoed
            std::vector<uint8_t> fl0(4, 0);
            uint16_t seq = sq++;
            auto r = aecp_xact(0x0024, seq, fl0);
            ck("B2: REGISTER_UNSOLICITED_NOTIFICATION answers SUCCESS",
               aecp_status(r), 0);
            ck("B2: ...2021 format, flags echoed (cdl 16)",
               (long)(r.size() >= 42
                      && ((((unsigned)r[16] & 7) << 8) | r[17]) == 16
                      && r[38] == 0 && r[41] == 0), 1);

            // LOCK -> SUCCESS naming the taker; foreign LOCK -> ENTITY_LOCKED
            std::vector<uint8_t> lk(16, 0);
            seq = sq++;
            r = aecp_xact(0x0001, seq, lk);
            ck("B2: LOCK_ENTITY takes (SUCCESS)", aecp_status(r), 0);
            ck("B2: ...locked_id = the taker",
               (long)(r.size() >= 50 && r[42] == r[26] && r[49] == r[33]), 1);
            // UNLOCK again so nothing later in the leg runs gated
            std::vector<uint8_t> ul(16, 0); ul[3] = 0x01;
            seq = sq++;
            r = aecp_xact(0x0001, seq, ul);
            ck("B2: UNLOCK releases (SUCCESS, locked_id 0)",
               (long)(aecp_status(r) == 0 && r.size() >= 50
                      && r[42] == 0 && r[49] == 0), 1);
            // ACQUIRE: the Milan 5.4.2.1 refusal, command echoed
            std::vector<uint8_t> aq(16, 0);
            seq = sq++;
            r = aecp_xact(0x0000, seq, aq);
            ck("B2: ACQUIRE_ENTITY refuses NOT_SUPPORTED(11)",
               aecp_status(r), 11);

            // GET_STREAM_INFO on STREAM_INPUT[0]: the Milan 80-byte body
            std::vector<uint8_t> gs = {0x00, 0x05, 0x00, 0x00};
            seq = sq++;
            r = aecp_xact(0x000F, seq, gs);
            ck("B2: GET_STREAM_INFO answers the Milan response (cdl 68)",
               (long)(aecp_status(r) == 0
                      && ((((unsigned)r[16] & 7) << 8) | r[17]) == 68), 1);
            ck("B2: ...STREAM_FORMAT_VALID with the generated AAF format",
               (long)(r.size() >= 62 && (r[42] & 0x80) != 0
                      && r[46] == 0x02 && r[47] == 0x05), 1);

            // GET_AVB_INFO: gm + domain + flags + the one class-A mapping
            std::vector<uint8_t> ga = {0x00, 0x09, 0x00, 0x00};
            seq = sq++;
            r = aecp_xact(0x0027, seq, ga);
            ck("B2: GET_AVB_INFO answers SUCCESS with one msrp mapping",
               (long)(aecp_status(r) == 0
                      && ((((unsigned)r[16] & 7) << 8) | r[17]) == 36
                      && (((unsigned)r[56] << 8) | r[57]) == 1
                      && r[58] == 0x06), 1);
            ck("B2: ...the grandmaster is the committed CSR pair",
               (long)(r.size() >= 50
                      && r[42] == 0x00 && r[43] == 0x1B && r[44] == 0xC5), 1);

            // GET_AS_PATH: count 1 = {gm} - the leaf's honest path
            std::vector<uint8_t> gp = {0x00, 0x00, 0x00, 0x00};
            seq = sq++;
            r = aecp_xact(0x0028, seq, gp);
            ck("B2: GET_AS_PATH answers count 1 with the grandmaster",
               (long)(aecp_status(r) == 0
                      && ((((unsigned)r[16] & 7) << 8) | r[17]) == 24
                      && (((unsigned)r[40] << 8) | r[41]) == 1
                      && r[42] == 0x00 && r[43] == 0x1B && r[44] == 0xC5), 1);

            // DEREGISTER: leave the registry clean for the rest of the leg
            seq = sq++;
            r = aecp_xact(0x0025, seq, {});
            ck("B2: DEREGISTER answers SUCCESS", aecp_status(r), 0);
        }

        // ---- (C) live-audio proof, through the writer that is LEFT ------
        // keys 0/1 are talker 0's two wire channels at WIRE_CHANS = 2; the
        // TONE cluster is src 4, so the CSR window word is {en[15],
        // src[14:12] = 4} = 0xC000 and the RAM word it commits is 0x1400.
        // The RAM-side readback is still the oracle - the window is a
        // request, the RAM is the truth.
        {
            axi_write(A_CHMAP_CTRL2, 0x1);   // arm the fabric + the CSR port
            for (int k = 0; k < 2; k++) {
                axi_write(A_CHMAP_SEL2, 0x100 | k);
                axi_write(A_CHMAP_WORD2, 0xC000);
            }
            for (int c = 0; c < 3000; c++) step();
            ck("T66: tone landed at key 0 (RAM-side)", cap_ram(0), 0x1400);
            ck("T66: tone landed at key 1 (RAM-side)", cap_ram(1), 0x1400);
            axi_write(0x6DC, 0x1);           // TONE_CTRL[0] = pilot on
            for (int c = 0; c < 30000; c++) step();   // let the walk emit it
            // capture one talker-0 PDU: payload nonzero, L==R per event
            std::vector<uint8_t> cur; std::vector<uint32_t> smp;
            dut->m_axis_mac_tx_tready = 1;
            for (int c = 0; c < 200000 && smp.empty(); c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0)
                            for (int s = 0; s < 12; s++) {
                                size_t o = 38 + off + 4*s;
                                smp.push_back(((uint32_t)cur[o]   << 16) |
                                              ((uint32_t)cur[o+1] <<  8) |
                                               (uint32_t)cur[o+2]);
                            }
                        cur.clear();
                    }
                }
                hi();
            }
            int nz = 0; long lr_eq = 1;
            for (size_t s = 0; s + 1 < smp.size(); s += 2) {
                if (smp[s]) nz++;
                if (smp[s] != smp[s+1]) lr_eq = 0;
            }
            // 6 sample events; the 48-entry 1 kHz table crosses zero at
            // most once in any 6-consecutive-sample window
            ck("T66: CSR-mapped tone REACHES the wire (payload live)",
               (long)(smp.size() == 12 && nz >= 4), 1);
            ck("T66: tone pair carries L == R (the TONE contract)", lr_eq, 1);
            //! LEFT ARMED ON PURPOSE for [T67] - see its banner. With
            //! aecp_odmap_dyn_w tied off, CHMAP_CTRL[0] is the ONLY thing
            //! that can put the media_tick-paced crossbar in front of the
            //! packetizer, and [T67] measures that grid.
            ck("T66: the crossbar is left ARMED for T67", axi_read(0x900) & 1, 1);
        }
    }

    // ==================================================================
    //  [T67] MEDIA-GRID CADENCE + TIMESTAMP TRACKING at the datapath
    //  level (t532 silicon 2026-08-09). The wire showed 123750 ns between
    //  6-sample PDUs - 48000 x 100/99 - where Milan 7.4 owes 125000 ns
    //  within +-50 ppm; 123750 = 6 x 2062.5 cycles x 10 ns and 2062.5 =
    //  99e6/48000, a media divider parameterized 99 MHz on a 100 MHz
    //  fabric. NOTHING at desk asserted the absolute rate (that is how it
    //  shipped), so this leg measures the SHIPPING grid end to end:
    //    * PDU-to-PDU spacing in fabric cycles over 8 epochs must equal
    //      8 x MILAN_CLK_FREQ_HZ x 6/48000 within the 50 ppm class bound
    //      (this build: 8 x 12500 exactly);
    //    * avtp_timestamp deltas must TRACK the PHC: equal to the PHC ns
    //      elapsed over those cycles at the LIVE PTP_INCR rate (read from
    //      0x504, Q8.24 - an earlier leg set 20 ns/tick), and after
    //      PTP_INCR is CSR-rewritten the deltas move with it - the
    //      integration half of the aaf [TSL] latch-not-adder pin.
    //  Runs on the [T66] tone stream: talker 0 framing continuously.
    //
    //  WHICH GRID IS UNDER TEST, AND WHY IT HAS TO BE SAID OUT LOUD NOW
    //  (2026-08-13). The packetizer drains ONE of two paths, chosen by
    //  `cap_xbar_live_w = aecp_odmap_dyn_w | cfg_chmap_enable`:
    //    * the CROSSBAR (KL_chan_map_capture), walked once per media_tick_p,
    //      i.e. MILAN_CLK_FREQ_HZ / 48000 = 2083.333 axis cycles per sample
    //      event and 12500 per 6-sample PDU - the grid this section measures;
    //    * the STATIC zero-fill path, paced by clk_audio_i / 512.
    //  Until the substitution `aecp_odmap_dyn_w` was a constant 1 on any
    //  shape that compiled the map machinery, so the crossbar was in circuit
    //  no matter what CHMAP_CTRL said and this section could not pick the
    //  wrong path. It is tied to 0 now, so CHMAP_CTRL[0] is the whole
    //  selector - and [T66] leaves it ARMED for exactly that reason.
    //  Running this section bypassed measures clk_audio/512, which every leg
    //  but obj_aclk clocks 1:1 with axis_clk: it reads 3072 cycles per PDU
    //  and looks like a 6x cadence defect that is really a harness artifact.
    //  (At the true 391/1591 divider the static path is 47,999.489 Hz,
    //  -10.6 ppm from media_tick - inside this section's 50 ppm bound - and
    //  obj_aclk is where that offset is measured directly.)
    // ==================================================================
    printf("-- [T67] media-grid cadence + avtp_timestamp PHC tracking --\n");
    {
        // collect K consecutive talker-0 PDUs: end-cycle stamps + ts
        auto collect_t0 = [&](int want) {
            std::vector<std::pair<long, uint32_t>> got;   // {cycle, ts}
            std::vector<uint8_t> cur;
            long c = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (c = 0; c < 400000 && (int)got.size() < want; c++) {
                lo();
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0) {
                            // avtp_timestamp = AVTP hdr +12: frame 26+off
                            uint32_t ts =
                                ((uint32_t)cur[26+off] << 24) |
                                ((uint32_t)cur[27+off] << 16) |
                                ((uint32_t)cur[28+off] <<  8) |
                                 (uint32_t)cur[29+off];
                            got.push_back({c, ts});
                        }
                        cur.clear();
                    }
                }
                hi();
            }
            return got;
        };

        const long EPOCH_CYC = 12500;        // MILAN_CLK 100e6 x 6/48000
        // the LIVE PHC rate (Q8.24 integer-ns; the ptp leg set 20 ns/tick)
        uint32_t incr0 = axi_read(0x504);
        long ns_cyc0 = (long)(incr0 >> 24);
        ck("T67: PTP_INCR is a whole-ns rate (Q8.24 frac 0)",
           incr0 & 0xFFFFFF, 0);
        auto p = collect_t0(9);
        ck("T67: talker 0 delivered 9 consecutive PDUs", (long)p.size(), 9);
        if (p.size() == 9) {
            long span = p[8].first - p[0].first;
            long lim  = (8 * EPOCH_CYC) / 20000 + 1;     // the 50 ppm class
            long err  = span - 8 * EPOCH_CYC;
            if (err < 0) err = -err;
            printf("         span 8 epochs = %ld cycles (nominal %ld, err %ld)\n",
                   span, 8 * EPOCH_CYC, err);
            ck("T67: PDU cadence = 48 kHz on MILAN_CLK within 50 ppm",
               err <= lim, 1);
            long d_ok = 1;
            for (int i = 1; i < 9; i++) {
                long d = (long)(uint32_t)(p[i].second - p[i-1].second);
                if (d != EPOCH_CYC * ns_cyc0) d_ok = 0;
                if (d != EPOCH_CYC * ns_cyc0)
                    printf("         ts delta %d = %ld ns (owed %ld)\n",
                           i, d, EPOCH_CYC * ns_cyc0);
            }
            ck("T67: ts deltas = PHC elapsed per epoch (12500 x INCR ns)",
               d_ok, 1);
            ck("T67: and NOT the t532 wire constant 123750",
               (long)(uint32_t)(p[1].second - p[0].second) == 123750, 0);
        } else { for (int k = 0; k < 3; k++) ck("T67 (skipped)", 0, 1); }

        // PHC warp via the ARCHITECTED CSR: PTP_INCR 0x504 moved ->
        // the deltas move with it (latched from the live PHC, never
        // synthesized; a ts += CONST adder reddens exactly this check)
        axi_write(0x504, 0x10000000);        // 16.0 ns per PHC tick
        collect_t0(3);                       // flush epochs straddling it
        auto w = collect_t0(5);
        long w_ok = (w.size() == 5) ? 1 : 0;
        for (size_t i = 1; i < w.size(); i++) {
            long d = (long)(uint32_t)(w[i].second - w[i-1].second);
            if (d != EPOCH_CYC * 16) w_ok = 0;
            if (d != EPOCH_CYC * 16)
                printf("         warp ts delta %zu = %ld ns (owed %ld)\n",
                       i, d, EPOCH_CYC * 16);
        }
        ck("T67: PTP_INCR rewrite moves the ts deltas (latch tracks PHC)",
           w_ok, 1);
        axi_write(0x504, incr0);             // restore the leg-entry PHC rate

        // [T66]/[T67] cleanup: tone off, tone mappings cleared, crossbar
        // disarmed - keys 0/1 dark and the packetizer back on the declared
        // front-end path, which is the state [T68] below expects to find.
        //
        // REPOINTED with [T66]: this used to be a REMOVE_AUDIO_MAPPINGS, and
        // that opcode is NOT_IMPLEMENTED now, so an AECP cleanup would leave
        // the tone mapped while reporting nothing wrong. The CSR 0x900 window
        // is the writer that is left, and the RAM read-back is the proof the
        // cleanup actually happened rather than the proof a command was
        // accepted.
        axi_write(0x6DC, 0x0);
        {
            enum { A_CHMAP_CTRL3 = 0x900, A_CHMAP_SEL3 = 0x904,
                   A_CHMAP_WORD3 = 0x908 };
            for (int k = 0; k < 2; k++) {
                axi_write(A_CHMAP_SEL3, 0x100 | k);
                axi_write(A_CHMAP_WORD3, 0x0000);      // en = 0
            }
            for (int c = 0; c < 3000; c++) step();
            auto cap_ram3 = [&](int key) -> uint32_t {
                axi_write(0x904, 0x100 | key);
                axi_write(0x910, 1);
                for (int g = 0; g < 64; g++) if ((axi_read(0x910) & 1) == 0) break;
                uint32_t v = axi_read(0x914);
                if (((v >> 26) & 1) == 0) return 0xFFFFFFFFu;
                return v & 0x1FFF;
            };
            ck("T67: cleanup cleared tone key 0 (RAM-side)", cap_ram3(0), 0);
            ck("T67: cleanup cleared tone key 1 (RAM-side)", cap_ram3(1), 0);
            axi_write(A_CHMAP_CTRL3, 0x0);             // back to the front end
            ck("T67: crossbar disarmed again", axi_read(0x900) & 1, 0);
        }
    }
#endif

#ifdef LOOPBACK_TB
    // ==================================================================
    //  [T68] LOOP SOURCE SEQUENCE FIDELITY - the stair-step measurement
    //  (user audio capture 2026-08-09: direct reception clean at ppm-
    //  class, loop reception 9895 glitches/s on the 6-sample PDU lattice
    //  with 8000 +/- 1000 Hz sidebands). Mechanism, in this RTL: the LOOP
    //  bucket is a LATEST-SAMPLE hold (lb_hold_r) - each received PDU
    //  bursts 6 samples per channel into it at wire speed, the media-tick
    //  walk then reads it 6 times before the next PDU, so the wire gets
    //  ~6 copies of each block's LAST sample and skips the other 5: a
    //  duplicate+skip stair on exactly the measured lattice. That WAS the
    //  documented slip policy doing what it says - correct for the
    //  once-per-sample front-end sources, WRONG for the bursty PDU
    //  source. VERSION 0x0036 landed the fix: a per-pair elastic queue
    //  (depth 8 = one PDU + margin) popped once per media tick - paced,
    //  in-order sequence replay with honest bounded slip (empty tick =
    //  repeat last + dup counted, full push = drop OLDEST + skip
    //  counted; both ZERO at lock). LB_SEQ_FIXED (the Makefile defines
    //  it for this leg) asserts that law; the pre-fix stair measured
    //  76 dup / 56 skip on this ramp.
    // ==================================================================
    printf("-- [T68] loop sequence fidelity vs a paced RAMP --\n");
    {
        enum { A_CHMAP_CTRL = 0x900, A_CHMAP_SEL = 0x904,
               A_CHMAP_WORD = 0x908 };
        const int LB_SID = 1;                // sidB is stream 1
        const int M = 10;                    // paced PDUs (60 ch0 samples)

        // talker 0's pair <- LOOP {stream 1, pair 0} via the debug window
        // (the AECP path is [T66]'s; this shape's generated LOOP templates
        // are en=0 = not-fabric-backed, so the canonical programmer rightly
        // refuses them and the bring-up window is the honest way in)
        axi_write(A_CHMAP_CTRL, 0x1);
        for (int k = 0; k < 2; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, (uint32_t)(0x8000 | (5 << 12)
                                               | ((k & 1) << 8)
                                               | (LB_SID << 4) | 0));
        }

        // paced RX: one 6-sample 2ch PDU per 12500 cycles (the media rate),
        // ch0 samples globally DISTINCT: PDU k sample s = tuple(48k + 4s)
        auto rx_pdu_beats = [&](uint8_t seq, uint8_t seed) {
            static std::vector<uint64_t> beats;
            const uint8_t* f = mkaaf(sidB, seq, 2, seed);
            beats.clear();
            for (size_t bt = 0; bt < (86 + 7) / 8; bt++) {
                uint64_t v = 0;
                for (int j = 0; j < 8; j++)
                    if (bt*8 + j < 86) v |= (uint64_t)f[bt*8+j] << (8*j);
                beats.push_back(v);
            }
            return beats;
        };

        // ACCEPTANCE WARM-UP, not graded: stream 1 has been dark since
        // task #65 (T66/T67 ran the tone), so the RX monitor's re-lock /
        // re-accept eats the first PDUs UPSTREAM of the crossbar - the
        // depacketizer forwards nothing and the queue honestly starves.
        // That behaviour belongs to the monitor's own legs and counters;
        // THIS leg grades the LOOP SOURCE's pacing, so it measures on a
        // stream the depacketizer is already forwarding. The warm-up
        // payload family is seed 0xE2 + 4j: every sample's top byte is
        // 2 mod 4, while every graded ramp value's is 0 mod 4 - residue
        // and ramp are distinguishable BY CONSTRUCTION for the stripper.
        {
            std::vector<uint64_t> beats; size_t bi = 0; int fed = 0;
            for (long c = 0; c < 6 * 12500L; c++) {
                if (c % 12500 == 0 && fed < 6) {
                    beats = rx_pdu_beats((uint8_t)(140 + fed),
                                         (uint8_t)(0xE2 + 4 * fed));
                    bi = 0; fed++;
                }
                //! WIRE-PACED beats (one 8-byte beat per 8 cycles, the GbE
                //! byte rate): the accept verdict is a multi-cycle serial
                //! walk and the depacketizer drops a frame whose verdict
                //! misses its tlast - real frames last >= 88 byte-times, a
                //! 1-beat-per-cycle firehose is 8x faster than any wire
                //! and starves the verdict window instead of the DUT
                if (bi < beats.size() && (c & 7) == 0) {
                    dut->s_axis_mac_rx_tdata  = beats[bi];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (bi == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0;
                    dut->s_axis_mac_rx_tlast  = 0;
                }
                lo();
                bool wacc = dut->s_axis_mac_rx_tvalid
                            && dut->s_axis_mac_rx_tready;
                hi();
                if (wacc) bi++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }
        // the queue's own drop-oldest evidence, graded by DELTA over the
        // paced window below (dup stays un-graded here: OTHER fed pairs
        // starve legitimately while only stream 1 is fed)
        long lbq_skip0 =
            (long)dut->rootp->milan_datapath__DOT__lb_skip_cnt_w;
        auto tuple24 = [&](int b0) -> uint32_t {
            return ((uint32_t)(uint8_t)(b0)     << 16)
                 | ((uint32_t)(uint8_t)(b0 + 1) <<  8)
                 |  (uint32_t)(uint8_t)(b0 + 2);
        };
        // expected ch0 sequence: 6 per PDU (payload samples 0,2,..,10)
        std::vector<uint32_t> expect;
        for (int k = 0; k < M; k++)
            for (int s = 0; s < 12; s += 2)
                expect.push_back(tuple24(48*k + 4*s));

        // drive M paced PDUs while capturing talker-0 ch0 output
        std::vector<uint32_t> emitted;
        {
            std::vector<uint8_t> cur;
            std::vector<uint64_t> beats; size_t bi = 0; int fed = 0;
            dut->m_axis_mac_tx_tready = 1;
            for (long c = 0; c < (long)M * 12500 + 40000; c++) {
                if (c % 12500 == 0 && fed < M) {
                    // seq continues the warm-up run (146 onward): the graded
                    // window must not open on a seq-mismatch of its own
                    beats = rx_pdu_beats((uint8_t)(146 + fed),
                                         (uint8_t)(48 * fed));
                    fed++; bi = 0;
                }
                //! wire-paced beats - same rule as the warm-up loop above
                if (bi < beats.size() && (c & 7) == 0) {
                    dut->s_axis_mac_rx_tdata  = beats[bi];
                    dut->s_axis_mac_rx_tkeep  = 0xFF;
                    dut->s_axis_mac_rx_tvalid = 1;
                    dut->s_axis_mac_rx_tlast  = (bi == beats.size()-1);
                } else {
                    dut->s_axis_mac_rx_tvalid = 0;
                    dut->s_axis_mac_rx_tlast  = 0;
                }
                lo();
                bool in_acc = dut->s_axis_mac_rx_tvalid
                              && dut->s_axis_mac_rx_tready;
                if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
                    for (int l = 0; l < 8; l++)
                        if ((dut->m_axis_mac_tx_tkeep >> l) & 1)
                            cur.push_back((dut->m_axis_mac_tx_tdata >> (8*l))
                                          & 0xFF);
                    if (dut->m_axis_mac_tx_tlast) {
                        size_t off = (cur.size() > 17 && cur[12] == 0x81
                                      && cur[13] == 0x00) ? 4 : 0;
                        if (cur.size() >= 86 + off && cur[12+off] == 0x22
                            && cur[13+off] == 0xF0 && cur[14+off] == 0x02
                            && ((cur[24+off] << 8) | cur[25+off]) == 0)
                            for (int s = 0; s < 12; s += 2) {
                                size_t o = 38 + off + 4*s;
                                emitted.push_back(
                                    ((uint32_t)cur[o]   << 16) |
                                    ((uint32_t)cur[o+1] <<  8) |
                                     (uint32_t)cur[o+2]);
                            }
                        cur.clear();
                    }
                }
                hi();
                if (in_acc) bi++;
            }
            dut->s_axis_mac_rx_tvalid = 0;
        }

        // strip the pre-ramp residue: silence fill (legal 5.3.7.3) and the
        // warm-up family (top byte 2 mod 4, disjoint from the ramp's
        // 0 mod 4). FIFO order guarantees no warm-up sample can appear
        // after the first ramp sample, so a leading strip is exact.
        while (!emitted.empty() && (emitted.front() == 0
                || ((emitted.front() >> 16) & 3) == 2))
            emitted.erase(emitted.begin());
        ck("T68: loop output collected against the paced ramp",
           emitted.size() >= 24, 1);

        // walk the expected sequence: membership, order, dups, skips. The
        // graded window ends the moment the whole ramp has been matched:
        // the feed stopped there, so everything after it is the queue law's
        // honest starved tail - it must be a pure repeat of the LAST sample
        // (the bounded-slip rule), graded separately below.
        long dups = 0, skips = 0, alien = 0, order_ok = 1;
        long tail_bad = 0; size_t matched = 0;
        {
            size_t p = 0; long last = -1;
            for (uint32_t v : emitted) {
                if (p == expect.size()) {
                    if (v != expect.back()) tail_bad++;
                    continue;
                }
                size_t q = p;
                while (q < expect.size() && expect[q] != v) q++;
                if (q == expect.size()) {
                    if (last >= 0 && v == expect[last]) { dups++; continue; }
                    // not ahead of the cursor: behind it = reordering
                    bool behind = false; size_t b = 0;
                    for (; b < p; b++) if (expect[b] == v) { behind = true; break; }
                    if (behind) order_ok = 0; else alien++;
                    continue;
                }
                skips += (long)(q - p);
                last = (long)q; p = q + 1;
            }
            matched = p;
        }
        printf("         emitted %zu ch0 samples vs %zu sent: "
               "%ld dup, %ld skipped, %ld alien, %ld bad tail\n",
               emitted.size(), expect.size(), dups, skips, alien, tail_bad);
        ck("T68: every loop sample is one the listener received", alien, 0);
        ck("T68: received order is preserved (no reordering)", order_ok, 1);
#ifdef LB_SEQ_FIXED
        // the paced-replay law (0x0036 queue rework): every received sample
        // exactly once, in order, and the post-feed tail repeats the final
        // sample only. The pre-rework latest-sample hold measured 76 dup /
        // 56 skip on this very ramp (the audible defect C stair).
        ck("T68: ZERO duplicated samples through the loop", dups, 0);
        ck("T68: ZERO skipped samples through the loop", skips, 0);
        ck("T68: the WHOLE ramp came through", (long)matched,
           (long)expect.size());
        ck("T68: post-feed tail = the final sample repeated (bounded slip)",
           tail_bad, 0);
        //! the module's own drop evidence agrees: rate-matched pacing never
        //! filled a queue, so drop-oldest never fired anywhere
        ck("T68: queue skip counter delta 0 over the paced window",
           (long)dut->rootp->milan_datapath__DOT__lb_skip_cnt_w - lbq_skip0,
           0);
#endif

        // parting state = the loop leg's: keys dark, window disarmed
        for (int k = 0; k < 2; k++) {
            axi_write(A_CHMAP_SEL, 0x100 | k);
            axi_write(A_CHMAP_WORD, 0x0000);
        }
        axi_write(A_CHMAP_CTRL, 0x0);
    }
#endif

    // ==================================================================
    //  DELETED 2026-08-13: THE SRP FABRIC LAUNCH STAGE CYCLE CONTRACT.
    //
    //  Its whole subject is gone. The block graded the launch pipeline of
    //  hdl/ieee8021q/srp/ - the fabric provisioner's requester vectors
    //  (aafsrp_req_r / lsnsrp_req_r / crf_srp_req_r), the pick/capture
    //  stages (srp_fab_pv_r / srp_fab_qv_r / srp_fab_own_r) and the
    //  KL_lwsrp_ctx attribute-row RAM (valid_r / row_fresh_w / sid_r) -
    //  plus the `qkill' fault-injection round that made a 0x800 window
    //  commit race an in-flight fabric capture for the same row.
    //
    //  hdl/ieee8021q/srp/ is DELETED in full. SRP is the protocol
    //  processor's now: it declares Talker Advertise and Listener Ready
    //  itself and publishes the result on the class-D face, and
    //  milan_datapath ties srp_ctx_gnt_w / srp_ctx_rd_* to zero. There is
    //  no attribute-row table, no provisioner, no arbiter and no
    //  fabric-vs-software row ownership to arbitrate, so there is no new
    //  witness to repoint any of these 25 checks at: the +1 landing rule,
    //  the row_fresh coherence rule, the one-write-per-retire ledger, the
    //  no-adjacent-writes serialisation rule and the qkill precedence rule
    //  are statements about logic that no longer exists.
    // ==================================================================

    // ------------------------------------------------------------------ //
    //  MEDIA GRID (VERSION 0x0041): one steerable grid, and the playback
    //  ring rides it.
    //
    //  These are WIRING claims, deliberately. tb/verilator/media_nco already
    //  grades KL_media_nco's arithmetic to 0.01 ppm against a closed form and
    //  nothing here re-proves that. What only the whole datapath can show is
    //  that media_tick_p really comes OUT of the NCO, that KL_pcm_tx really
    //  advances on it instead of on its own divider, and that
    //  clock_source = INTERNAL really pins the trim to zero - the three
    //  things a parameter typo would break silently while every ppm check
    //  in the tree stayed green.
    // ------------------------------------------------------------------ //
    {
        auto* rp = dut->rootp;

        //  6250 clocks == 3 samples EXACTLY at 100 MHz / 48 kHz (the Bresenham
        //  walks 2083, 2083, 2084), so a whole multiple of it makes the
        //  expected count exact arithmetic rather than a rounding. The window
        //  still starts at an arbitrary phase, hence the +/-1.
        const long GRID_CLK  = 625000;   // 300 samples exactly
        const long GRID_WANT = 300;

        //  the servo command the datapath hands the NCO, and the gate that
        //  decides whether the grid may follow it. The CONVERSION (sign and
        //  rescale) now lives inside KL_media_nco where tb/verilator/media_nco
        //  sweeps it; what belongs here is the WIRING - is the servo's
        //  published field really what reaches the NCO, and is the gate really
        //  the clock-source selection.
        auto servo16 = [&]() -> long {
            const unsigned long raw = rp->milan_datapath__DOT__mnco_servo_trim_w & 0xFFFFul;
            return (raw & 0x8000ul) ? (long)raw - 0x10000L : (long)raw;
        };
        auto stat16 = [&]() -> long {
            const unsigned long raw = (rp->milan_datapath__DOT__mcsrv_stat_w >> 16) & 0xFFFFul;
            return (raw & 0x8000ul) ? (long)raw - 0x10000L : (long)raw;
        };

        //  0x0042: the slot-indexed physical bucket must actually be fed.
        //  Until this round milan_datapath tied .tdm_pair_valid_i to 1'b0, so
        //  every capture pair landed in the SINGLE-pair I2S hold and a
        //  physical cluster past channel 1 could never be backed on any shape.
        //  "tdm_hold_r changed from its reset value" is the sharpest available
        //  proof that the feed exists: restore the tie-off and it stays 0.
        long tdm_written = 0;

        long ticks = 0, pcm_local = 0, mismatch = 0;
        long gate_bad = 0, cmd_bad = 0;
        for (long c = 0; c < GRID_CLK; c++) {
            step();
            if (rp->milan_datapath__DOT__chan_map_capture__DOT__tdm_pair_valid_i)
                tdm_written++;
            const bool mt = rp->milan_datapath__DOT__media_tick_p != 0;
            if (mt) ticks++;

            //  The gate must BE the clock-source selection, every cycle.
            //  That selection is a COMPILE-TIME CONSTANT now: milan_datapath
            //  declares CRF_CLK_SELECTED_C = 0 and the old aecp_clk_src net
            //  is deleted, so the gate must be 0 on every cycle - not merely
            //  equal to a net that is also 0. (Keeping both nets and tying
            //  the live one to 0 is what made every consumer compare 0 == 0
            //  and read "CRF selected"; the constant exists to end that.)
            if (rp->milan_datapath__DOT__mnco_servo_en_w != 0) gate_bad++;
            //  and the command must BE the servo's published trim field
            if (servo16() != stat16()) cmd_bad++;
#ifdef AAF_PB_TB
            //  KL_pcm_tx only exists on the playback shape (obj_nxn8); on the
            //  N=4 build the generate is not taken, so these taps do not exist
            //  and the one-grid claim is checked by the 8x8 leg alone.
            const bool pt = rp->milan_datapath__DOT__g_aaf_playback__DOT__pcm_tx__DOT__tick_w != 0;
            if (pt != mt) mismatch++;
            if (rp->milan_datapath__DOT__g_aaf_playback__DOT__pcm_tx__DOT__tick_r) pcm_local++;
#endif
        }
        printf("  [i]    media grid: %ld ticks in %ld clocks (want %ld +/-1), "
               "pcm local-divider pulses %ld, tick mismatches %ld\n",
               ticks, GRID_CLK, GRID_WANT, pcm_local, mismatch);

        //  WHAT THIS LEG CANNOT CHECK: alignment between the media grid and
        //  the TDM word clock - and the reason is blunter than the earlier
        //  version of this comment claimed.
        //
        //  CORRECTED 2026-08-10. This used to say the cause was clk_audio_i being
        //  toggled 1:1 with axis_clk, so fsync came out near 195 kHz instead
        //  of 48. That was wrong: on obj_nxn and obj_nxn8 AUDIO_IF_SLOTS_P is
        //  0, so the g_aif_i2s branch is taken and milan_datapath.sv:694 ties
        //  `tdm_fsync_o = 1'b0`. There is no fsync HERE AT ALL, at any clock
        //  rate. What runs at clk_audio/512 on these legs is i2s_lrck_o.
        //  Pointing the gap at the ratio sent the work at the wrong signal.
        //
        //  The alignment question belongs to obj_ax1x1, the leg that
        //  elaborates the shipping solo TDM8 master - and since 2026-08-10 that
        //  leg drives clk_tdm_i and checks the master is live (see
        //  sim_main.cpp). What is STILL absent there is the RATIO: both
        //  clk_audio_i and clk_tdm_i are toggled at the axis rate, so the
        //  exact 391/1591 divider plan that puts fsync at 47,999.4893 Hz
        //  against a 48,000.0000 Hz grid - -10.6393 ppm, one whole sample of
        //  slip every 1.9582 s = 195,815,385 axis cycles - is not modelled.
        //
        //  That is why the grid is brought out on AX7101 J11.9
        //  (media_lrclk_o, a 50% square at fs/2) beside tdm_fsync_o on J11.8:
        //  the requirement is that the two stay ALIGNED, and a two-channel
        //  probe is today the only instrument that can say whether they do.
        printf("  [GAP]  0x0041 grid: fsync-vs-grid ALIGNMENT is not modelled - "
               "this leg has no TDM front end at all (AUDIO_IF_SLOTS_P=0 ties "
               "tdm_fsync_o to 0); the shipping master lives in obj_ax1x1, and "
               "even there clk_tdm_i runs at the axis rate so the -10.64 ppm "
               "391/1591 ratio is absent. Measure J11.8 against J11.9.\n");

        //  vacuity guard first: a grid stuck low would make every "== 0"
        //  check below pass for the wrong reason
        ck("0x0041 grid: media_tick_p actually ticks (vacuity guard)",
           ticks > 0, 1);
        ck("0x0041 grid: rate is 48 kHz on the milan clock",
           (ticks >= GRID_WANT - 1 && ticks <= GRID_WANT + 1), 1);
#ifdef AAF_PB_TB
        ck("0x0041 grid: KL_pcm_tx's OWN divider never pulses",
           pcm_local, 0);
        ck("0x0041 grid: KL_pcm_tx advances on media_tick_p, every cycle",
           mismatch, 0);
#endif

        //  The steering WIRING. Both of these are falsifiable regardless of
        //  whether the servo ever moves, which the earlier "trim == 0 while
        //  INTERNAL" formulation was not: with clock_source = INTERNAL the
        //  servo sits at u = 0, so gated and ungated were both zero and
        //  deleting the gate left the suite green. Grading the GATE itself
        //  rather than its arithmetic consequence removes that blind spot -
        //  and the sign/rescale it used to stand in for is now swept directly
        //  by tb/verilator/media_nco (13 servo commands x 2 clock shapes).
        printf("  [i]    physical bucket: the slot-indexed feed pulsed %ld times "
               "in %ld cycles\n", tdm_written, GRID_CLK);
        ck("0x0042 phys: the slot-indexed capture bucket IS fed (was tied off)",
           tdm_written > 0, 1);

        ck("0x0041 grid: the NCO's servo gate IS the clock-source selection",
           gate_bad, 0);
        ck("0x0041 grid: INTERNAL leaves the grid free-running",
           rp->milan_datapath__DOT__mnco_servo_en_w, 0);

        //  "the command is A_MCSRV_STAT[31:16]" can only be graded while the
        //  servo status is non-zero: idle, the whole word reads 0 and every
        //  slice of it compares equal. Mutating the slice to [15:0] leaves
        //  this green - verified - so it is reported, not passed.
        if (stat16() == 0 && (rp->milan_datapath__DOT__mcsrv_stat_w & 0xFFFFu) == 0) {
            printf("  [GAP]  0x0041 grid: servo status is all-zero (idle at "
                   "clock_source=INTERNAL), so WHICH slice feeds the NCO is "
                   "unfalsifiable here. The sign and rescale it carries are "
                   "swept by tb/verilator/media_nco; only the slice is open, "
                   "and it needs a CRF stimulus at clock_source=CRF.\n");
        } else {
            ck("0x0041 grid: the NCO's servo command IS A_MCSRV_STAT[31:16]",
               cmd_bad, 0);
        }
    }

    printf("--------------------------------------------------------------\n");
    printf("checks: %ld   failures: %ld\n", checks, fails);
    printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
    dut->final();
    delete dut;
    return fails ? 1 : 0;
}

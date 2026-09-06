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
#include "../../common/verilator_harness.hpp"
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <vector>

namespace {

//! Everything the substitution harness owns: the Verilated model it
//! observes, the check tally, the free-running MAC TX census, the two
//! memory models behind the descriptor and response-buffer faces, and the
//! graded phases that used to be one 1 369-line `main` (I.2, F.3).
class PpShadowHarness {
 public:
    //! the model is owned for the whole of `run()`: the destructor runs
    //! `final()` and frees it on every path out, so there is no teardown at
    //! the bottom of this function to skip (R.11, R.20, C.149)
    int run() {
        const milan::tb::Model<Vmilan_datapath> model;
        dut = model.get();                  // the harness's observing pointer

        printf("=== milan_datapath + the protocol processor AS the control plane ===\n");
        //! the descriptor image must be in "memory" BEFORE the first clock: the
        //! store's boot walk (header probe -> index map) starts out of reset
        build_desc_image();
        do_reset();

        grade_plane_presence_and_csr_window();
        provision_the_identity_before_enable();
        grade_absent_backend_reports_no_restore();
        grade_control_face_and_liveness();
        const uint32_t aidx0 = enable_the_entity_and_read_the_class_d_baseline();
        grade_side_port_answers_with_the_processor_magic();
        grade_control_frame_reaches_the_validator();
        grade_non_control_traffic_is_rejected();
        grade_the_wire_carries_the_processor();
        grade_class_d_face_moves(aidx0);
        grade_adp_advertisement_is_byte_exact();
        grade_maap_refuses_without_wedging();
        grade_maap_grants_and_opens_the_da_gate();
        grade_the_device_answers_aecp();
        grade_descriptor_memory_withdrawn();
        grade_response_buffer_memory();
        grade_shared_control_lane();
        grade_global_anti_wedge_invariant();
        grade_heal_before_answer();

        printf("----------------------------------------------------------------\n");
        printf("pp_shadow: %ld checks, %ld failures\n", checks, fails);
        printf("RESULT: %s\n", fails ? "FAIL" : "PASS");
        return fails ? 1 : 0;
    }

 private:
    Vmilan_datapath* dut = nullptr;
    long checks = 0;
    long fails = 0;

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
    MaapObs mo;

    // ---- MAC TX frame census, whole frames, byte for byte ----------------------
    // The old census kept only a destination MAC per frame, because the graded
    // property was "no frame at all". Now that the processor owns the wire the
    // frame CONTENT is the evidence, so every egressed frame is retained.
    struct TxFrame {
        std::vector<uint8_t> bytes;
        int  beats      = 0;
        bool short_beat = false;   // a non-final beat with a partial tkeep
    };
    std::vector<TxFrame> tx_frames;
    bool     tx_open = false;
    long     tx_bad_keep = 0;      // partial tkeep before tlast, any frame
    long     tx_beats_total = 0;

    static constexpr uint64_t MAAP_DST = 0x91E0F000FF00ull;  // KL_maap's own TX DA

    void observe() {
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
            const uint8_t keep = static_cast<uint8_t>(dut->m_axis_mac_tx_tkeep);
            const uint64_t d   = dut->m_axis_mac_tx_tdata;
            for (int l = 0; l < 8; l++)
                if ((keep >> l) & 1) f.bytes.push_back(static_cast<uint8_t>((d >> (8 * l)) & 0xFF));
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

    FrClass classify(const TxFrame& f) {
        if (f.bytes.size() < 15) return FR_SHORT;
        const unsigned et = (static_cast<unsigned>(f.bytes[12]) << 8) | f.bytes[13];
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
    bool avtp_len_consistent(const TxFrame& f, size_t* want_out) {
        if (f.bytes.size() < 18) return false;
        const size_t cdl  = ((static_cast<size_t>(f.bytes[16]) & 0x7) << 8) | f.bytes[17];
        size_t want = 14 + 12 + cdl;
        if (want < 60) want = 60;
        if (want_out) *want_out = want;
        return f.bytes.size() == want;
    }

    void ck(const char* what, uint32_t got, uint32_t exp) {
        checks++;
        bool ok = (got == exp);
        if (!ok) fails++;
        printf("  [%s] %-42s got=0x%08X exp=0x%08X\n", ok ? "PASS" : "FAIL", what, got, exp);
    }

    void ck_true(const char* what, bool cond, const char* detail) {
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
    static constexpr uint32_t DESC_BASE = 0x20000000u;

    std::vector<uint8_t> desc_img;      // the AEMI image, byte for byte
    bool     mem_answering = true;      // section [M] turns this off
    bool     mem_busy      = false;
    uint32_t mem_cur       = 0;         // byte address of the next beat
    int      mem_left      = 0;         // beats still owed
    long     mem_reqs      = 0;         // bursts accepted, for the record

    uint64_t desc_beat(uint32_t byte_addr) {
        uint64_t v = 0;
        for (int i = 0; i < 8; i++) {          // big-endian: byte n at [63-8n-:8]
            const uint32_t off = byte_addr - DESC_BASE + static_cast<uint32_t>(i);
            const uint8_t  b   = (off < desc_img.size()) ? desc_img[off] : 0;
            v = (v << 8) | b;
        }
        return v;
    }

    // driven BEFORE eval, off state settled at the previous edge
    void mem_drive() {
        dut->i_desc_mem_req_ready = (mem_answering && !mem_busy) ? 1 : 0;
        dut->i_desc_mem_rsp_valid = mem_busy ? 1 : 0;
        dut->i_desc_mem_rsp_data  = mem_busy ? desc_beat(mem_cur) : 0;
        dut->i_desc_mem_rsp_last  = (mem_busy && mem_left == 1) ? 1 : 0;
        dut->i_desc_mem_rsp_err   = 0;
    }

    // sampled AFTER eval with clk still low: this is what the coming edge commits
    void mem_edge() {
        if (!mem_busy) {
            if (dut->o_desc_mem_req_valid && dut->i_desc_mem_req_ready) {
                mem_cur  = dut->o_desc_mem_req_addr;
                mem_left = static_cast<int>(dut->o_desc_mem_req_beats);
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
    static constexpr uint32_t RESP_BASE  = 0x20100000u;   // PP_RESP_BASE_P default
    static constexpr uint32_t RESP_BYTES = 592u;          // 16 + PP_DESC_LINE_BYTES_P

    uint8_t  rmem[RESP_BYTES] = {};
    bool     rmem_answering = true;     // section [N] turns this off
    bool     rm_busy   = false;         // read burst in flight
    uint32_t rm_cur    = 0;
    int      rm_left   = 0;
    bool     rm_wpend  = false;         // write accepted, commits this cycle
    uint32_t rm_waddr  = 0;
    uint64_t rm_wdata  = 0;
    uint32_t rm_wstrb  = 0;
    long     rm_reqs   = 0;             // read bursts accepted
    long     rm_writes = 0;             // lane writes committed

    uint64_t rmem_beat(uint32_t byte_addr) {
        uint64_t v = 0;
        for (int i = 0; i < 8; i++) {          // big-endian: byte n at [63-8n-:8]
            const uint32_t off = byte_addr - RESP_BASE + static_cast<uint32_t>(i);
            const uint8_t  b   = (off < RESP_BYTES) ? rmem[off] : 0;
            v = (v << 8) | b;
        }
        return v;
    }

    void rmem_drive() {
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

    void rmem_edge() {
        if (!rm_busy) {
            if (dut->o_resp_mem_req_valid && dut->i_resp_mem_req_ready) {
                rm_cur  = dut->o_resp_mem_req_addr;
                rm_left = static_cast<int>(dut->o_resp_mem_req_beats);
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
                    const uint32_t k = rm_waddr - RESP_BASE + static_cast<uint32_t>(i);
                    if (k < RESP_BYTES) rmem[k] = static_cast<uint8_t>(rm_wdata >> (56 - 8 * i));
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
    void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0; mem_drive(); rmem_drive(); dut->eval(); observe(); mem_edge(); rmem_edge(); }
    void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->eval(); }
    void step() { lo(); hi(); }

    // ---- AXI4-Lite BFM (identical protocol/timing to the milan_dp harness) ----
    //! Cycles the BFM waits for one handshake before giving up. A bounded wait, so
    //! a channel that never asserts ready fails the check that reads the result
    //! rather than hanging the suite.
    static constexpr int kAxiHandshakeGuard = 2048;

    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d;  dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiHandshakeGuard; g++) {
            lo();
            bool acc = dut->s_axi_awready && dut->s_axi_wready;   // settled, pre-edge
            hi();
            if (acc) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiHandshakeGuard; g++) {
            lo();
            bool bv = dut->s_axi_bvalid;
            hi();
            if (bv) break;
        }
        dut->s_axi_bready = 0;
    }

    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiHandshakeGuard; g++) {
            lo();
            bool acc = dut->s_axi_arready;
            hi();
            if (acc) break;
        }
        dut->s_axi_arvalid = 0;
        uint32_t d = 0;
        for (int g = 0; g < kAxiHandshakeGuard; g++) {
            lo();
            bool rv = dut->s_axi_rvalid;
            if (rv) d = dut->s_axi_rdata;
            hi();
            if (rv) break;
        }
        dut->s_axi_rready = 0;
        return d;
    }

    // The CSR window, as byte offsets. A block of `constexpr` values rather than
    // an `enum class` (Enum.5): every one of these is handed straight to
    // axi_read()/axi_write() as the plain address it is, and an enum class would
    // need a cast at each of those call sites - the construct ES.49 exists to
    // remove. `uint16_t` is the BFM's own address width, so there is no narrowing
    // left to hide either.
    static constexpr uint16_t A_ID          = 0x000;
    static constexpr uint16_t A_VERSION     = 0x004;
    static constexpr uint16_t A_MAC_ALO     = 0x108;
    static constexpr uint16_t A_MAC_AHI     = 0x10C;
    static constexpr uint16_t A_ADP_CTRL    = 0x600;
    static constexpr uint16_t A_ADP_EIDLO   = 0x604;
    static constexpr uint16_t A_ADP_EIDHI   = 0x608;
    static constexpr uint16_t A_ADP_MDLLO   = 0x60C;
    static constexpr uint16_t A_ADP_MDLHI   = 0x610;
    static constexpr uint16_t A_ADP_CAPS    = 0x614;
    static constexpr uint16_t A_ADP_TALK    = 0x618;
    static constexpr uint16_t A_ADP_LIST    = 0x61C;
    static constexpr uint16_t A_ADP_GMLO    = 0x624;
    static constexpr uint16_t A_ADP_GMHI    = 0x628;
    static constexpr uint16_t A_ADP_GDOM    = 0x62C;
    static constexpr uint16_t A_MAAP_CTRL   = 0x6CC;
    static constexpr uint16_t A_MAAP_STAT0  = 0x6D0;
    static constexpr uint16_t A_MAAP_STAT1  = 0x6D4;
    static constexpr uint16_t A_TXARB_DIAG  = 0x784;
    static constexpr uint16_t A_PP_CTRL     = 0x920;
    static constexpr uint16_t A_PP_STAT     = 0x924;
    static constexpr uint16_t A_PP_SPADDR   = 0x928;
    static constexpr uint16_t A_PP_SPDATA   = 0x92C;
    static constexpr uint16_t A_PP_DIAG     = 0x930;
    static constexpr uint16_t A_PP_NVM_SEL  = 0x934;
    static constexpr uint16_t A_PP_NVM_DATA = 0x938;
    static constexpr uint16_t A_PP_NVM_STAT = 0x93C;

    // The entity_id this harness provisions. NOT zero on purpose: the processor's
    // talker matches a PROBE_TX on target_eid == own entity_id, and against a zero
    // entity_id a frame whose bytes never arrived would match just as well.
    static constexpr uint64_t TEST_EID   = 0x001BC50CAC000001ull;
    static constexpr uint64_t TEST_MODEL = 0x001BC5441BC55569ull;

    // The station MAC this harness programs, in the CSR's platform LSB-first
    // packing (ALO[7:0] = the FIRST wire byte). KL_pp_shadow takes the byte
    // REVERSED numeric EUI-48, so the ADPDU's source address must come out
    // 02:00:00:00:00:01 on the wire — the swapped form is 01:.. = a multicast
    // source address, which every bridge drops.
    static constexpr uint32_t STA_MAC_LO = 0x00000002u;   // wire bytes 0..3 = 02 00 00 00
    static constexpr uint32_t STA_MAC_HI = 0x00000100u;   // wire bytes 4..5 = 00 01
    static constexpr uint8_t  STA_MAC[6] = {
        0x02, 0x00, 0x00, 0x00, 0x00, 0x01};

    // KL_maap's pool: 91:E0:F0:00 + a 16-bit offset (KL_maap.sv POOL_BASE_HI_C).
    static constexpr uint64_t MAAP_POOL_BASE = 0x91E0F0000000ull;

    // side-port windows implemented by protocol_processor_top (tb/pp_top README)
    static constexpr uint32_t SP_SNAPSHOT = 0x20000;   // word 0 = magic "KLPP"

    //! Cycles both resets are held asserted, and cycles the design is clocked
    //! afterwards before the first CSR access.
    static constexpr int kResetHoldCycles   = 8;
    static constexpr int kResetSettleCycles = 16;

    void do_reset() {
        dut->axis_resetn = 0; dut->gtx_resetn = 0;
        dut->s_axi_awvalid = dut->s_axi_wvalid = dut->s_axi_arvalid = 0;
        dut->s_axi_bready = dut->s_axi_rready = 0;
        dut->s_axis_mac_rx_tvalid = 0;
        dut->m_axis_mac_tx_tready = 1;
        dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1; dut->i_mac_events = 0;
        for (int i = 0; i < kResetHoldCycles; i++) step();
        dut->axis_resetn = 1; dut->gtx_resetn = 1;
        for (int i = 0; i < kResetSettleCycles; i++) step();
    }

    // ---- inject one little-lane frame on the MAC RX port ----
    void inject_rx(const uint8_t* f, size_t len, int tail_cycles) {
        size_t beats = (len + 7) / 8;
        std::vector<uint64_t> bw(beats, 0);
        std::vector<uint8_t>  bk(beats, 0);
        for (size_t i = 0; i < len; i++) {
            bw[i / 8] |= static_cast<uint64_t>(f[i]) << (8 * (i % 8));
            bk[i / 8] |= static_cast<uint8_t>(1u << (i % 8));
        }
        size_t idx = 0;
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < static_cast<int>(beats) + tail_cycles; c++) {
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
    void run_idle(int cycles) {
        dut->m_axis_mac_tx_tready = 1;
        for (int c = 0; c < cycles; c++) { lo(); hi(); }
    }

    // ---- posted side-port access over the CSR bridge ----
    //! Polls of PP_STAT[0] a posted side-port read is given before it is reported
    //! as a timeout (`*ok = false`) rather than waited on for ever.
    static constexpr int kSpBusyPollGuard = 4096;

    uint32_t sp_read(uint32_t word_addr, bool* ok) {
        axi_write(A_PP_SPADDR, word_addr);            // arm: posts the read
        for (int g = 0; g < kSpBusyPollGuard; g++) {
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
    static constexpr uint8_t OUR_MAC[6] = {
        0x00, 0x1B, 0xC5, 0x0C, 0xAC, 0x00};

    //! An ADPDU on the wire: 14 B Ethernet + a 68 B ADPDU. The length rule this
    //! repo enforces, and the one number the discover builder, the expected-frame
    //! model and the byte-exact compare below must all agree on.
    static constexpr uint32_t kAdpduWireBytes = 82;

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
    size_t build_adp_discover(uint8_t* f) {
        memset(f, 0, kAdpduWireBytes);
        const uint8_t da[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        const uint8_t sa[6] = {
            0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
        memcpy(f, da, 6); memcpy(f + 6, sa, 6);
        f[12] = 0x22; f[13] = 0xF0;          // EtherType
        f[14] = 0xFA;                        // subtype ADP
        f[15] = 0x02;                        // sv=0, version=0, msg_type=ENTITY_DISCOVER
        f[16] = 0x00; f[17] = 56;            // valid_time 0, control_data_length 56
        // target entity_id at @4 (wire bytes 18..25) stays 0 = discover everybody
        return kAdpduWireBytes;
    }

    void put64be(uint8_t* p, uint64_t v) {
        for (int i = 0; i < 8; i++) p[i] = static_cast<uint8_t>(v >> (8 * (7 - i)));
    }
    void put32be(uint8_t* p, uint32_t v) {
        for (int i = 0; i < 4; i++) p[i] = static_cast<uint8_t>(v >> (8 * (3 - i)));
    }
    void put16be(uint8_t* p, uint16_t v) {
        p[0] = static_cast<uint8_t>(v >> 8);
        p[1] = static_cast<uint8_t>(v);
    }

    uint64_t get_be(const std::vector<uint8_t>& b, size_t off, size_t n) {
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
    size_t build_probe_tx(uint8_t* f, uint64_t eid, uint16_t uid) {
        memset(f, 0, 70);
        const uint8_t da[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
        const uint8_t sa[6] = {
            0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
        memcpy(f, da, 6); memcpy(f + 6, sa, 6);
        f[12] = 0x22; f[13] = 0xF0;      // EtherType 1722
        f[14] = 0xFC;                    // subtype ACMP
        f[15] = 0x00;                    // sv=0, version=0, message_type=0
        f[16] = 0x00; f[17] = 44;        // status 0, control_data_length 44
        put64be(f + 18, eid);                        // @4  stream_id
        put64be(f + 26, 0xC0FFEE00DEADBEEFull);      // @12 controller_entity_id
        put64be(f + 34, eid);                        // @20 talker_entity_id
        put64be(f + 42, 0x2222222222222222ull);      // @28 listener_entity_id
        f[50] = static_cast<uint8_t>(uid >> 8);              // @36 talker_unique_id
        f[51] = static_cast<uint8_t>(uid);
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
    static constexpr uint16_t DTY_ENTITY_C = 0x0000;
    static constexpr uint16_t DTY_CONFIG_C = 0x0001;
    static constexpr uint16_t DTY_ABSENT_C = 0x0002;   // AUDIO_UNIT: not in this image
    //! STREAM_PORT_INPUT (Table 7-1 0x000E), ONE of them - the 1x1 shape's
    //! listener port, and the object GET_AUDIO_MAP's locate must find: the image
    //! is the EXISTENCE authority (index 1 answers NO_SUCH_DESCRIPTOR because
    //! it is absent HERE, whatever the fabric's port constants say)
    static constexpr uint16_t DTY_SPI_C    = 0x000E;
    //! STREAM_INPUT (0x0005), ONE of them - the counters strictness round made
    //! the image the EXISTENCE authority for GET_COUNTERS too, so the object
    //! whose 0xFFF mask the L5 series grades must exist here and index 9 must
    //! not
    static constexpr uint16_t DTY_STRIN_C  = 0x0005;
    static constexpr size_t   ENT_LEN_C    = 40;
    static constexpr size_t   CFG_LEN_C    = 24;
    static constexpr size_t   SPI_LEN_C    = 20;                 // Table 7-23
    static constexpr size_t   STRIN_LEN_C  = 24;                 // existence is enough
    static constexpr uint32_t ENT_OFF_C    = 0x60;               // 4 index entries now
    static constexpr uint32_t CFG_OFF_C    = ENT_OFF_C + 40;     // 0x88
    static constexpr uint32_t STRIN_OFF_C  = CFG_OFF_C + 2 * 24; // 0xB8
    static constexpr uint32_t SPI_OFF_C    = STRIN_OFF_C + 24;   // 0xD0
    static constexpr uint32_t IMG_END_C    = SPI_OFF_C + 24;     // 0xE8 (8-aligned)

    void put32be_v(std::vector<uint8_t>& v, size_t off, uint32_t x) {
        for (int i = 0; i < 4; i++) v[off + i] = static_cast<uint8_t>(x >> (8 * (3 - i)));
    }
    void put16be_v(std::vector<uint8_t>& v, size_t off, uint16_t x) {
        v[off] = static_cast<uint8_t>(x >> 8); v[off + 1] = static_cast<uint8_t>(x);
    }

    // the descriptor bytes this harness expects back on the wire
    std::vector<uint8_t> desc_bytes(uint16_t type, uint16_t index) {
        const size_t n = (type == DTY_ENTITY_C) ? ENT_LEN_C
                       : (type == DTY_SPI_C)    ? SPI_LEN_C
                       : (type == DTY_STRIN_C)  ? STRIN_LEN_C : CFG_LEN_C;
        std::vector<uint8_t> d(n, 0);
        put16be_v(d, 0, type);
        put16be_v(d, 2, index);
        if (type == DTY_SPI_C) {
            // a REAL Table 7-23 body, CONSISTENT with the elaborated shape: this
            // suite includes endstation_arty_current's generated header, whose
            // STREAM_INPUT[0] format carries channels_per_frame = 2, so the
            // fabric's audio-map geometry is 2 clusters at base 0 (one page).
            // number_of_maps 0 is the 7.2.13 dynamic-mapping declaration this
            // whole face serves.
            put16be_v(d, 12, 2);                     // number_of_clusters
            put16be_v(d, 14, 0);                     // base_cluster
            put16be_v(d, 16, 0);                     // number_of_maps: dynamic
            return d;
        }
        const uint8_t seed = static_cast<uint8_t>(0xA0 + 0x10 * type + 0x08 * index);
        for (size_t i = 4; i < n; i++) d[i] = static_cast<uint8_t>(seed + i);
        return d;
    }

    void build_desc_image() {
        desc_img.assign(IMG_END_C, 0);
        // --- index map @0x20 ---------------------------------------------------
        // {cfg, type, count, elem_len, elem_off, name_base, elem_stride}
        put16be_v(desc_img, 0x20 + 0x0, 0);              // configuration_index
        put16be_v(desc_img, 0x20 + 0x2, DTY_ENTITY_C);
        put16be_v(desc_img, 0x20 + 0x4, 1);              // count
        put16be_v(desc_img, 0x20 + 0x6, static_cast<uint16_t>(ENT_LEN_C));
        put32be_v(desc_img, 0x20 + 0x8, ENT_OFF_C);
        put16be_v(desc_img, 0x20 + 0xC, 0xFFFF);         // unnamed
        put16be_v(desc_img, 0x20 + 0xE, static_cast<uint16_t>(ENT_LEN_C));   // stride (8-aligned)
        put16be_v(desc_img, 0x30 + 0x0, 0);
        put16be_v(desc_img, 0x30 + 0x2, DTY_CONFIG_C);
        put16be_v(desc_img, 0x30 + 0x4, 2);              // TWO of them
        put16be_v(desc_img, 0x30 + 0x6, static_cast<uint16_t>(CFG_LEN_C));
        put32be_v(desc_img, 0x30 + 0x8, CFG_OFF_C);
        put16be_v(desc_img, 0x30 + 0xC, 0xFFFF);
        put16be_v(desc_img, 0x30 + 0xE, static_cast<uint16_t>(CFG_LEN_C));
        // sorted by (config, type): 0x0005 sits between CONFIG and SPI
        put16be_v(desc_img, 0x40 + 0x0, 0);
        put16be_v(desc_img, 0x40 + 0x2, DTY_STRIN_C);
        put16be_v(desc_img, 0x40 + 0x4, 1);              // STREAM_INPUT[0] only
        put16be_v(desc_img, 0x40 + 0x6, static_cast<uint16_t>(STRIN_LEN_C));
        put32be_v(desc_img, 0x40 + 0x8, STRIN_OFF_C);
        put16be_v(desc_img, 0x40 + 0xC, 0xFFFF);
        put16be_v(desc_img, 0x40 + 0xE, 24);             // stride (8-aligned)
        put16be_v(desc_img, 0x50 + 0x0, 0);
        put16be_v(desc_img, 0x50 + 0x2, DTY_SPI_C);
        put16be_v(desc_img, 0x50 + 0x4, 1);              // the 1x1 listener port
        put16be_v(desc_img, 0x50 + 0x6, static_cast<uint16_t>(SPI_LEN_C));
        put32be_v(desc_img, 0x50 + 0x8, SPI_OFF_C);
        put16be_v(desc_img, 0x50 + 0xC, 0xFFFF);
        put16be_v(desc_img, 0x50 + 0xE, 24);             // stride (8-aligned)
        // --- descriptors -------------------------------------------------------
        {
            auto e = desc_bytes(DTY_ENTITY_C, 0);
            memcpy(&desc_img[ENT_OFF_C], e.data(), e.size());
            auto c0 = desc_bytes(DTY_CONFIG_C, 0);
            memcpy(&desc_img[CFG_OFF_C], c0.data(), c0.size());
            auto c1 = desc_bytes(DTY_CONFIG_C, 1);
            memcpy(&desc_img[CFG_OFF_C + CFG_LEN_C], c1.data(), c1.size());
            auto t0 = desc_bytes(DTY_STRIN_C, 0);
            memcpy(&desc_img[STRIN_OFF_C], t0.data(), t0.size());
            auto s0 = desc_bytes(DTY_SPI_C, 0);
            memcpy(&desc_img[SPI_OFF_C], s0.data(), s0.size());
        }
        // --- header @0x00, checksum LAST ---------------------------------------
        put32be_v(desc_img, 0x00, 0x41454D49u);          // "AEMI"
        put16be_v(desc_img, 0x04, 1);                    // layout_version
        put16be_v(desc_img, 0x06, 1);                    // n_config
        put16be_v(desc_img, 0x08, 4);                    // n_entries
        put16be_v(desc_img, 0x0A, 0);                    // n_names
        put32be_v(desc_img, 0x0C, 0x20);                 // index_off
        put32be_v(desc_img, 0x10, IMG_END_C);            // names_off (empty)
        put32be_v(desc_img, 0x14, IMG_END_C);            // image_bytes
        put16be_v(desc_img, 0x18, static_cast<uint16_t>(ENT_LEN_C));  // desc_max_len
        put16be_v(desc_img, 0x1A, 0);                    // reserved
        uint32_t sum = 0;
        for (int w = 0; w < 7; w++)
            sum += (static_cast<uint32_t>(desc_img[4*w])   << 24)
                 | (static_cast<uint32_t>(desc_img[4*w+1]) << 16)
                 | (static_cast<uint32_t>(desc_img[4*w+2]) <<  8)
                 |  static_cast<uint32_t>(desc_img[4*w+3]);
        put32be_v(desc_img, 0x1C, 0xFFFFFFFFu - sum);
    }

    // ---- an AECP AEM command on the wire ---------------------------------------
    // IEEE 1722.1-2021 9.2.1: 14 B Ethernet + the 24 B AECPDU header + payload.
    // `control_data_length` is this architecture's offset-from-@12 convention, so
    // it is 12 + payload. UNICAST to the station MAC — KL_pp_shadow accepts any DA
    // carrying EtherType 0x22F0 and lets the processor's own validator judge.
    static constexpr uint8_t CTLR_MAC[6] = {
        0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
    static constexpr uint64_t CTLR_EID   = 0xC0FFEE00DEADBEEFull;

    size_t build_aecp(uint8_t* f, uint8_t msg_type, uint64_t target_eid,
                             uint16_t opcode, uint16_t seq,
                             const uint8_t* pld, size_t pld_len) {
        const size_t len = 14 + 24 + pld_len;
        memset(f, 0, len);
        memcpy(f, STA_MAC, 6);                       // DA: the entity
        memcpy(f + 6, CTLR_MAC, 6);                  // SA: the controller
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0xFB;                                // AVTP subtype AECP
        f[15] = static_cast<uint8_t>(msg_type & 0x0F);          // sv=0, version=0
        const uint16_t cdl = static_cast<uint16_t>(12 + pld_len);
        f[16] = static_cast<uint8_t>((cdl >> 8) & 0x07);        // status 0 on a command
        f[17] = static_cast<uint8_t>(cdl & 0xFF);
        put64be(f + 18, target_eid);
        put64be(f + 26, CTLR_EID);
        put16be(f + 34, seq);
        put16be(f + 36, opcode);                     // u = 0
        if (pld_len) memcpy(f + 38, pld, pld_len);
        return len;
    }

    // READ_DESCRIPTOR payload: configuration_index, reserved, type, index
    size_t build_read_desc(uint8_t* f, uint16_t cfg, uint16_t type,
                                  uint16_t index, uint16_t seq) {
        uint8_t pl[8];
        put16be(pl + 0, cfg); put16be(pl + 2, 0);
        put16be(pl + 4, type); put16be(pl + 6, index);
        return build_aecp(f, 0 /* AEM_COMMAND */, TEST_EID, 0x0004, seq, pl, 8);
    }

    // A frame the classifier must REJECT: plain IPv4, EtherType 0x0800.
    size_t build_ipv4(uint8_t* f) {
        memset(f, 0, 64);
        const uint8_t da[6] = {
            0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
        memcpy(f, da, 6); memcpy(f + 6, OUR_MAC, 6);
        f[12] = 0x08; f[13] = 0x00;
        for (int i = 14; i < 64; i++) f[i] = static_cast<uint8_t>(i);
        return 64;
    }

    // The ADPDU this build MUST emit, assembled from the CSR identity group alone
    // (KL_adp_engine's frame_byte_f, F04.5). available_index (wire 50..53) is left
    // zero here and excluded from the compare — it is the one field that moves.
    void expected_adpdu(uint8_t* e, uint32_t talk_w, uint32_t list_w,
                               uint32_t caps_w, uint64_t gm, uint8_t dom) {
        memset(e, 0, kAdpduWireBytes);
        const uint8_t da[6] = {
            0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00};
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
        put16be(e + 38, static_cast<uint16_t>(talk_w & 0xFFFFu));
        put16be(e + 40, static_cast<uint16_t>(talk_w >> 16));
        put16be(e + 42, static_cast<uint16_t>(list_w & 0xFFFFu));
        put16be(e + 44, static_cast<uint16_t>(list_w >> 16));
        // 46..49 controller_capabilities = 0, 50..53 available_index (excluded)
        put64be(e + 54, gm);
        e[62] = dom;
        // 63 reserved, 64..65 current_configuration, 66..67 identify_control_index,
        // 68..69 interface_index, 70..81 association_id + reserved: all zero in
        // this fixture before any AECP setters are issued.
    }

    // ---- A. the plane is present and its window decodes -------------------
    void grade_plane_presence_and_csr_window() {
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
    }

    // Provision the identity BEFORE the plane is enabled: entity_id is the
    // discriminator the talker matches a PROBE_TX against and the field the
    // ADPDU decode below rebuilds from, and the CSR resets it to zero.
    void provision_the_identity_before_enable() {
        axi_write(A_MAC_ALO, STA_MAC_LO);
        axi_write(A_MAC_AHI, STA_MAC_HI);
        axi_write(A_ADP_EIDLO, static_cast<uint32_t>(TEST_EID & 0xFFFFFFFFu));
        axi_write(A_ADP_EIDHI, static_cast<uint32_t>(TEST_EID >> 32));
        axi_write(A_ADP_MDLLO, static_cast<uint32_t>(TEST_MODEL & 0xFFFFFFFFu));
        axi_write(A_ADP_MDLHI, static_cast<uint32_t>(TEST_MODEL >> 32));
        axi_write(A_ADP_CAPS,  0x0000C588u);          // a Milan PAAD's capabilities
    }

    // ---- P. SAVED STATE: an unconfigured backend may not report a restore -
    // Milan v1.2 puts unconditional SHALLs on non-volatile state: 5.3.8.2
    // "The current bound state shall be saved in a non-volatile memory and
    // restored after a power cycle", 5.3.8.3 the four binding parameters,
    // 5.3.8.7 the started/stopped state, with 5.5.2.4 fixing WHEN the
    // Listener writes them. This build cannot meet them yet: KL_pp_shadow
    // answers the class-F device face with KL_nvm_backend, and until firmware
    // has configured AND validated a record image through PP_NVM_SEL/DATA
    // (nothing in this harness does) the backend answers blank flash (reads
    // 0xFF, discards writes), so no binding survives a power cycle.
    // WHAT IS GRADED HERE IS NOT PERSISTENCE. It is that PP_STAT never
    // reports a restore that did not happen. The failure mode being closed is
    // a checklist that reads a clean restore verdict off a device with no
    // media, passes, and then fails on a bench where the power is cycled.
    // Runs BEFORE the entity enable below, which is the boot order Milan
    // 5.5.3.5.2 requires of a real restore.
    void grade_absent_backend_reports_no_restore() {
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
        ck("PP_STAT[6] nvm_backed == 0 (no writer has answered behind the device face)",
           (rstat >> 6) & 1, 0u);
        ck("PP_STAT[7] nvm_blank == 1 (the walk validated zero records)",
           (rstat >> 7) & 1, 1u);
        ck("PP_STAT[3] restore_fail == 1 (an absent backend is not a success)",
           (rstat >> 3) & 1, 1u);
        ck("PP_STAT[4] nvm_alarm == 0 (nothing was committed, so nothing retried)",
           (rstat >> 4) & 1, 0u);
        ck("the presence tag is unchanged by the verdict bits",
           (rstat >> 24) & 0xFF, 0x5Bu);
        // The bits the backing store added (REGISTER_MAP PP_STAT [8]..[15:12]):
        // nothing was configured, so nothing is dirty, stale, valid or judged.
        ck("PP_STAT[8] nvm_dirty == 0 (no change was accepted)",
           (rstat >> 8) & 1, 0u);
        ck("PP_STAT[9] nvm_stale == 0 (never backed is not stale)",
           (rstat >> 9) & 1, 0u);
        ck("PP_STAT[10] nvm_img_valid == 0 (no image was validated)",
           (rstat >> 10) & 1, 0u);
        ck("PP_STAT[15:12] nvm_verdict == 0 (no image was offered)",
           (rstat >> 12) & 0xF, 0u);
    }

    // ---- P2. THE CONTROL FACE, AND THE FALSE SUCCESS ONE LEVEL UP ---------
    // PP_NVM_SEL/DATA/STAT (0x934-0x93C) reach KL_nvm_backend through
    // milan_csr and KL_pp_shadow. The sequence word is firmware's to keep and
    // inert to the fabric, so it is the one word this harness may write
    // without configuring an image: an image LENGTH would make the backend
    // wait on a memory bridge this harness does not model, and stall every
    // NVM write the processor issues afterwards.
    // Then a firmware heartbeat: it makes the writer LIVE (nvm_backed = 1)
    // and nothing else. The walk in [P] ran with no validated image behind
    // the face, and liveness arriving afterwards restores nothing, so fail
    // MUST stay raised. A verdict read off the live level instead of the
    // walk's own evidence would flip to "restored" here: that is the false
    // success issue #70 exists to remove, moved up one level.
    void grade_control_face_and_liveness() {
        printf("[P2] saved state: the control face answers, liveness heals no walk\n");
        axi_write(A_PP_NVM_SEL, 2u);
        ck("PP_NVM_SEL reads back the index", axi_read(A_PP_NVM_SEL) & 0x3Fu, 2u);
        axi_write(A_PP_NVM_DATA, 0xA5C30001u);
        ck("PP_NVM_DATA reads back the backend's word 2 (sequence)",
           axi_read(A_PP_NVM_DATA), 0xA5C30001u);
        const uint32_t nstat = axi_read(A_PP_NVM_STAT);
        ck("PP_NVM_STAT: not configured, not backed, no operation in flight",
           nstat & ((1u << 6) | (1u << 5) | (1u << 4)), 0u);

        axi_write(A_PP_NVM_STAT, 1u << 0);                // heartbeat strobe
        run_idle(8);
        const uint32_t hstat = axi_read(A_PP_STAT);
        printf("  [i]    PP_STAT 0x924 = 0x%08X after a heartbeat\n", hstat);
        ck("PP_STAT[6] nvm_backed == 1 after a firmware heartbeat (live evidence)",
           (hstat >> 6) & 1, 1u);
        ck("PP_NVM_STAT[6] agrees with PP_STAT[6]",
           (axi_read(A_PP_NVM_STAT) >> 6) & 1, 1u);
        ck("PP_STAT[3] restore_fail STAYS 1: a blind walk is not healed by liveness",
           (hstat >> 3) & 1, 1u);
        ck("PP_STAT[7] nvm_blank stays 1 (the walk still validated zero records)",
           (hstat >> 7) & 1, 1u);
        ck("PP_STAT[2] restore_done stays 1 (the walk did complete)",
           (hstat >> 2) & 1, 1u);
    }

    // class-D baseline, taken before the processor has ever advertised
    uint32_t enable_the_entity_and_read_the_class_d_baseline() {
        const uint32_t aidx0 = dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w;
        axi_write(A_PP_CTRL, 0x1);                       // entity_enable
        ck("PP_CTRL reads back", axi_read(A_PP_CTRL) & 0x3, 0x1);
        return aidx0;
    }

    // ---- E. the side port answers with the processor's own magic ----------
    void grade_side_port_answers_with_the_processor_magic() {
        printf("[E] side-port bridge -> the processor's snapshot window\n");
        bool ok = false;
        uint32_t magic = sp_read(SP_SNAPSHOT + 0, &ok);
        ck_true("side-port access completed", ok, ok ? "ack seen" : "TIMED OUT waiting on sp_busy");
        ck("snapshot[0] magic == 'KLPP'", magic, 0x4B4C5050);
        uint32_t shape = sp_read(SP_SNAPSHOT + 1, &ok);
        ck_true("snapshot[1] shape non-zero", shape != 0, shape ? "shape word present" : "read 0");
    }

    // ---- B. a control frame reaches the processor -------------------------
    void grade_control_frame_reaches_the_validator() {
        printf("[B] RX classify -> FIFO -> serializer -> the processor's validator\n");
        uint8_t f[128];
        size_t n = build_adp_discover(f);
        uint32_t before = axi_read(A_PP_DIAG) & 0xFF;
        inject_rx(f, n, 400);                            // tail: drain the serializer
        run_idle(400);
        uint32_t after = axi_read(A_PP_DIAG) & 0xFF;
        ck("ADP DISCOVER accepted (rx_frames +1)", after - before, 1);
        ck("no frame lost to a full FIFO", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);
    }

    // ---- C. non-control traffic is rejected by the classifier -------------
    void grade_non_control_traffic_is_rejected() {
        printf("[C] the filter that keeps a 1 B/clk serializer ahead of the wire\n");
        uint8_t f[128];
        size_t n = 0;
        uint32_t before = axi_read(A_PP_DIAG) & 0xFF;
        uint32_t after = 0;
        for (int i = 0; i < 8; i++) { n = build_ipv4(f); inject_rx(f, n, 40); }
        run_idle(400);
        after = axi_read(A_PP_DIAG) & 0xFF;
        ck("8 IPv4 frames REJECTED (rx_frames flat)", after - before, 0);
        ck("and none of them was counted as a drop", (axi_read(A_PP_DIAG) >> 8) & 0xFF, 0);
    }

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
    void grade_the_wire_carries_the_processor() {
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
        long foreign = 0;
        for (size_t i = tx_frames_at_d0; i < tx_frames.size(); i++) {
            const FrClass c = classify(tx_frames[i]);
            if (c == FR_ALIEN || c == FR_SHORT || c == FR_MAAP) foreign++;
        }
        ck("every frame in the window was a processor control PDU",
           static_cast<uint32_t>(foreign), 0u);
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
    void grade_class_d_face_moves(uint32_t aidx0) {
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
    }

    // ---- F. the ADP advertisement, DECODED at the MAC boundary -------------
    // A frame count is weak evidence. This rebuilds the whole 82-byte ADPDU
    // from the CSR identity group and compares it against the wire byte for
    // byte, so an engine that egressed a plausible-looking runt, or a control
    // lane that spliced a MAAP beat into it, fails here.
    void grade_adp_advertisement_is_byte_exact() {
        printf("[F] the ENTITY_AVAILABLE the processor emits, decoded byte-exact\n");
        const uint32_t talk_w = axi_read(A_ADP_TALK);
        const uint32_t list_w = axi_read(A_ADP_LIST);
        const uint32_t caps_w = axi_read(A_ADP_CAPS);
        const uint64_t gm = (static_cast<uint64_t>(axi_read(A_ADP_GMHI)) << 32)
                          | axi_read(A_ADP_GMLO);
        const uint8_t  dom = static_cast<uint8_t>(axi_read(A_ADP_GDOM) & 0xFF);

        std::vector<size_t> adp_idx;
        for (size_t i = 0; i < tx_frames.size(); i++)
            if (classify(tx_frames[i]) == FR_ADP) adp_idx.push_back(i);

        char det[128];
        snprintf(det, sizeof det, "%zu ADPDU(s) at the MAC boundary of %zu frames",
                 adp_idx.size(), tx_frames.size());
        ck_true("an ADP frame reached the MAC TX boundary", !adp_idx.empty(), det);

        if (!adp_idx.empty()) {
            const TxFrame& a = tx_frames[adp_idx.front()];
            ck("ADPDU is 82 octets on the wire", static_cast<uint32_t>(a.bytes.size()),
               kAdpduWireBytes);
            ck("ADPDU DA == 91:E0:F0:01:00:00",
               static_cast<uint32_t>(get_be(a.bytes, 0, 4)), 0x91E0F001u);
            ck("ADPDU EtherType 0x22F0 + subtype 0xFA",
               static_cast<uint32_t>(get_be(a.bytes, 12, 3)), 0x22F0FAu);
            ck("ADPDU sv=0 version=0 message_type=ENTITY_AVAILABLE",
               a.bytes.size() > 15 ? a.bytes[15] : 0xFFu, 0x00u);
            ck("ADPDU control_data_length == 56",
               static_cast<uint32_t>(((static_cast<unsigned>(a.bytes[16]) & 7) << 8) | a.bytes[17]), 56u);
            ck("ADPDU entity_id == the 0x604/0x608 pair",
               static_cast<uint32_t>(get_be(a.bytes, 18, 4)), static_cast<uint32_t>(TEST_EID >> 32));
            ck("ADPDU entity_id low half",
               static_cast<uint32_t>(get_be(a.bytes, 22, 4)), static_cast<uint32_t>(TEST_EID & 0xFFFFFFFFu));
            ck("ADPDU entity_model_id == the 0x60C/0x610 pair",
               static_cast<uint32_t>(get_be(a.bytes, 26, 4)), static_cast<uint32_t>(TEST_MODEL >> 32));
            // The advertised SHAPE against the same numbers milan_csr serves at
            // 0x618/0x61C over a different path. A shape that reaches one and
            // not the other is the 2026-07-27 silicon defect (a boot script
            // frozen at 1x1 while the 8x8 board advertised the wrong count).
            // This law used to be graded in milan_dp; the advertiser there is
            // the processor now and its cadence is unreachable at real-time
            // clocking, so the check lives HERE, where time is compressed.
            ck("ADPDU talker_stream_sources == 0x618",
               static_cast<uint32_t>(get_be(a.bytes, 38, 2)), talk_w & 0xFFFFu);
            ck("ADPDU talker_capabilities == 0x618",
               static_cast<uint32_t>(get_be(a.bytes, 40, 2)), talk_w >> 16);
            ck("ADPDU listener_stream_sinks == 0x61C",
               static_cast<uint32_t>(get_be(a.bytes, 42, 2)), list_w & 0xFFFFu);
            ck("ADPDU listener_capabilities == 0x61C",
               static_cast<uint32_t>(get_be(a.bytes, 44, 2)), list_w >> 16);

            // ...and now the WHOLE frame, byte for byte. valid_time (byte 16's
            // top five bits) is the engine's own constant rather than a CSR
            // field, so it is copied from the observed frame; available_index
            // (50..53) is the one moving field and is graded on its own below.
            uint8_t exp[kAdpduWireBytes];
            expected_adpdu(exp, talk_w, list_w, caps_w, gm, dom);
            exp[16] = static_cast<uint8_t>((a.bytes[16] & 0xF8) | ((56 >> 8) & 0x7));
            memcpy(exp + 50, &a.bytes[50], 4);
            long diffs = 0;
            int firstdiff = -1;
            for (size_t i = 0; i < kAdpduWireBytes && i < a.bytes.size(); i++)
                if (a.bytes[i] != exp[i]) {
                    diffs++;
                    if (firstdiff < 0) firstdiff = static_cast<int>(i);
                }
            char bdet[128];
            snprintf(bdet, sizeof bdet,
                     "%ld differing octet(s); first at wire byte %d", diffs, firstdiff);
            ck_true("ADPDU is byte-exact against the CSR identity group",
                    diffs == 0 && a.bytes.size() == kAdpduWireBytes, bdet);

            // available_index: strictly increasing across the advertisements
            // that egressed, and the class-D face agrees with the wire.
            long nonmono = 0;
            uint32_t prev = 0;
            bool first = true;
            for (size_t k : adp_idx) {
                const uint32_t ai = static_cast<uint32_t>(get_be(tx_frames[k].bytes, 50, 4));
                if (!first && ai <= prev) nonmono++;
                prev = ai; first = false;
            }
            ck("available_index strictly increases across ADPDUs",
               static_cast<uint32_t>(nonmono), 0u);
            ck_true("class-D available_index >= the last one on the wire",
                    dut->rootp->milan_datapath__DOT__pp_cd_adp_avail_index_w >= prev,
                    "the published index tracks the wire");
        }
    }

    // ---- H. the MAAP adapter REFUSES SAFELY (no block claimed yet) ---------
    // MAAP_CTRL.en is 0 out of reset, so KL_maap holds no block and the shim
    // can grant nothing. The processor must be told so — and told PROMPTLY —
    // rather than left with a stuck allocator-busy flag.
    void grade_maap_refuses_without_wedging() {
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
        ck("and every answer refused (ok = 0)", static_cast<uint32_t>(h_gr), 0u);
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
        int found = -1;
        for (size_t i = tx_frames.size(); i-- > 0; )
            if (classify(tx_frames[i]) == FR_ACMP
                && tx_frames[i].bytes.size() >= 18
                && (tx_frames[i].bytes[15] & 0xF) == 1) { found = static_cast<int>(i); break; }
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
    void grade_maap_grants_and_opens_the_da_gate() {
        uint8_t pf[128];
        size_t pn = 0;
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
                mo.last_da == (MAAP_POOL_BASE | static_cast<uint64_t>((maap_off + 0) & 0xFFFF)),
                mo.last_da == (MAAP_POOL_BASE | static_cast<uint64_t>((maap_off + 0) & 0xFFFF))
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
        const size_t frames_before_p3 = tx_frames.size();
        pn = build_probe_tx(pf, TEST_EID, 0);
        inject_rx(pf, pn, 400);
        run_idle(8000);
        int found = -1;
        for (size_t i = tx_frames.size(); i-- > frames_before_p3; )
            if (classify(tx_frames[i]) == FR_ACMP
                && tx_frames[i].bytes.size() >= 62
                && (tx_frames[i].bytes[15] & 0xF) == 1) { found = static_cast<int>(i); break; }
        ck_true("a CONNECT_TX_RESPONSE came back with a block claimed", found >= 0,
                found >= 0 ? "response on the wire" : "no ACMP response egressed");
        if (found >= 0) {
            const std::vector<uint8_t>& b = tx_frames[found].bytes;
            ck("PROBE_TX now answers SUCCESS", (b[16] >> 3) & 0x1F, 0u);
            ck("...naming stream_id {station MAC, uid 0} high half",
               static_cast<uint32_t>(get_be(b, 18, 4)), 0x02000000u);
            ck("...and its low half", static_cast<uint32_t>(get_be(b, 22, 4)), 0x00010000u);
            ck("...with stream_dest_mac = the granted DA (high half)",
               static_cast<uint32_t>(get_be(b, 54, 4)), 0x91E0F000u);
            ck("...and its low half = base offset + 0",
               static_cast<uint32_t>(get_be(b, 58, 2)), maap_off & 0xFFFFu);
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
    void grade_the_device_answers_aecp() {
        printf("[L] AECP: the device ANSWERS — decoded, not counted\n");
        grade_read_descriptor_hit();
        grade_read_descriptor_index_stride();
        grade_read_descriptor_locate_miss();
        grade_read_descriptor_bad_configuration();
        grade_unassigned_opcode_echoes();
        grade_get_counters_for_a_live_sink();
        grade_get_counters_for_an_absent_sink();
        grade_padded_get_counters_ignores_the_tail();
        grade_get_counters_for_an_unsupported_type();
        grade_get_audio_map_from_the_render_ram();
        grade_get_audio_map_page_rule();
        grade_get_audio_map_absent_port();
        grade_get_audio_map_output_port();
        grade_identify_notification_as_command();
        grade_silent_refusal_leaves_the_plane_serving();
        grade_acquire_entity_is_refused();
    }

    // helper: the newest AECP frame at the MAC boundary past `from`
    int last_aecp(size_t from) {
        for (size_t i = tx_frames.size(); i-- > from; )
            if (classify(tx_frames[i]) == FR_AECP) return static_cast<int>(i);
        return -1;
    }

    // helper: the fields every response shares, graded once per case
    void grade_common(const std::vector<uint8_t>& b, const char* tag,
                      uint16_t opcode, uint16_t seq, uint8_t mt) {
        char w[96];
        snprintf(w, sizeof w, "%s: message_type = command + 1", tag);
        ck(w, b[15] & 0x0F, mt);
        snprintf(w, sizeof w, "%s: sv/version nibble is zero", tag);
        ck(w, (b[15] >> 4) & 0x0F, 0u);
        snprintf(w, sizeof w, "%s: target_entity_id is OURS", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 18, 4)), static_cast<uint32_t>(TEST_EID >> 32));
        snprintf(w, sizeof w, "%s: controller_entity_id echoed", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 26, 4)), static_cast<uint32_t>(CTLR_EID >> 32));
        snprintf(w, sizeof w, "%s: sequence_id echoed", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 34, 2)), seq);
        snprintf(w, sizeof w, "%s: command_type echoed, u = 0", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 36, 2)), opcode);
        snprintf(w, sizeof w, "%s: unicast back to the requester", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 0, 4)),
           static_cast<uint32_t>((CTLR_MAC[0] << 24) | (CTLR_MAC[1] << 16)
                      | (CTLR_MAC[2] << 8) | CTLR_MAC[3]));
        snprintf(w, sizeof w, "%s: source address is the station MAC", tag);
        ck(w, static_cast<uint32_t>(get_be(b, 6, 4)),
           static_cast<uint32_t>((STA_MAC[0] << 24) | (STA_MAC[1] << 16)
                      | (STA_MAC[2] << 8) | STA_MAC[3]));
    }

    // helper: cdl vs the frame's real length, the malformed-frame trap
    void grade_len(const std::vector<uint8_t>& b, const char* tag,
                   size_t pld) {
        char w[96];
        size_t want = 38 + pld;
        if (want < 60) want = 60;
        snprintf(w, sizeof w, "%s: control_data_length = 12 + payload", tag);
        ck(w, static_cast<uint32_t>(((static_cast<unsigned>(b[16]) & 7) << 8) | b[17]),
           static_cast<uint32_t>(12 + pld));
        snprintf(w, sizeof w, "%s: frame length matches (60-octet min)", tag);
        ck(w, static_cast<uint32_t>(b.size()), static_cast<uint32_t>(want));
    }

    // --- L1. READ_DESCRIPTOR that HITS: SUCCESS + the descriptor -------
    // The store must have validated the image out of reset (magic +
    // layout version + checksum) and walked the index map, or this comes
    // back NO_SUCH_DESCRIPTOR — which is why mem_reqs is graded too: a
    // model that never got asked is a model that proved nothing.
    void grade_read_descriptor_hit() {
        uint8_t cf[128];
        size_t  cn = 0;
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
                   static_cast<uint32_t>(get_be(b, 38, 2)), 0u);
                ck("L1: reserved @26 is zero", static_cast<uint32_t>(get_be(b, 40, 2)), 0u);
                // the descriptor itself, byte for byte against the image
                auto want = desc_bytes(DTY_ENTITY_C, 0);
                long bad = 0;
                for (size_t i = 0; i < want.size(); i++)
                    if (42 + i >= b.size() || b[42 + i] != want[i]) bad++;
                ck("L1: the DESCRIPTOR bytes @28 are the image's, exactly",
                   static_cast<uint32_t>(bad), 0u);
            }
        }
    }

    // --- L2. the SAME type at index 1: proves the stride arithmetic ----
    void grade_read_descriptor_index_stride() {
        uint8_t cf[128];
        size_t  cn = 0;
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
               static_cast<uint32_t>(bad), 0u);
            ck("L2: ...and it is NOT index 0's descriptor",
               static_cast<uint32_t>(get_be(b, 44, 2)), 1u);   // descriptor_index field
        }
    }

    // --- L3. a locate MISS: NO_SUCH_DESCRIPTOR + the §7.4.5 stub -------
    // The type AND the index are both NON-ZERO on purpose: a stub check
    // against {0, 0} would be satisfied by the zero padding of a frame
    // that never wrote a stub at all.
    void grade_read_descriptor_locate_miss() {
        uint8_t cf[128];
        size_t  cn = 0;
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
               static_cast<uint32_t>(get_be(b, 42, 2)), DTY_ABSENT_C);
            ck("L3: ...and the descriptor_index",
               static_cast<uint32_t>(get_be(b, 44, 2)), 7u);
        }
    }

    // --- L4. a bad configuration_index: BAD_ARGUMENTS, not a miss ------
    // The µprogram range-checks against configurations_count out of the
    // store's region 0xD before it ever locates, so the two failures stay
    // distinguishable — which is what a controller needs to tell "wrong
    // configuration" from "no such descriptor".
    void grade_read_descriptor_bad_configuration() {
        uint8_t cf[128];
        size_t  cn = 0;
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
            ck("L4: the stub still names the type", static_cast<uint32_t>(get_be(b, 42, 2)),
               DTY_CONFIG_C);
            ck("L4: ...and the index", static_cast<uint32_t>(get_be(b, 44, 2)), 1u);
            ck("L4: configuration_index @24 is the BAD one, echoed",
               static_cast<uint32_t>(get_be(b, 38, 2)), 5u);
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
    void grade_unassigned_opcode_echoes() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x05, 0x00, 0x00, 0xDE, 0xAD, 0xBE, 0xEF};
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
            ck("L5: the command's payload is ECHOED back", static_cast<uint32_t>(bad), 0u);
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
    static constexpr size_t CTR_PLD_C = 2 + 2 + 4 + 128;     // 136, 7.4.42.2
    void grade_get_counters_for_a_live_sink() {
        uint8_t cf[128];
        size_t  cn = 0;
        // descriptor_type STREAM_INPUT (Table 7-4 0x0005), index 0: the
        // one sink this 1x1 shape elaborates.
        uint8_t pl[4] = {
            0x00, 0x05, 0x00, 0x00};
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
            ck("L5b: descriptor_type echoed @0", static_cast<uint32_t>(get_be(b, 38, 2)),
               0x0005u);
            ck("L5b: descriptor_index echoed @2",
               static_cast<uint32_t>(get_be(b, 40, 2)), 0u);
            // 0xFFF = quadlets 0..11, every counter Table 7-157 defines
            // for a STREAM_INPUT before the reserved span at offset 48.
            // Table 7-156 numbers MEDIA_LOCKED bit #31 at offset 0 and
            // TIMESTAMP_VALID bit #25 at offset 24, so the mask bit for
            // quadlet n is bit n of a conventional LSB-0 word.
            ck("L5b: counters_valid @4 is the twelve we keep (0xFFF)",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0x0000'0FFFu);
            // Table 7-157 reserves offsets 48..92 and gives 96.. to the
            // ENTITY_SPECIFIC set. This build claims none of them, and a
            // claimed-zero is the lie this face exists to prevent, so
            // they must be BOTH unclaimed in the mask and zero in the
            // block. The mask check above covers the first half.
            long dirty = 0;
            for (int q = 12; q < 32; q++)
                if (get_be(b, 46 + 4 * static_cast<size_t>(q), 4) != 0) dirty++;
            ck("L5b: the unclaimed quadlets 12..31 are zero",
               static_cast<uint32_t>(dirty), 0u);
            ck_true("L5b: the block is a full 32 quadlets",
                    b.size() == 46 + 128, "the frame ends at 174");
        }
    }

    // THE WRONG-OBJECT ANSWER, upgraded by the counters strictness
    // round: the engine's store locate now refuses an index the
    // image lacks with NO_SUCH_DESCRIPTOR (Table 7-141: "A
    // descriptor with the descriptor_type and descriptor_index
    // specified does not exist") while still carrying the fixed
    // 7.4.42.2 body, all zero. The fabric's clamp-guard on the face
    // stays as the second line of defense - a full mask over sink
    // 0's numbers remains the failure this block exists to catch.
    void grade_get_counters_for_an_absent_sink() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[4] = {
            0x00, 0x05, 0x00, 0x09};   // STREAM_INPUT 9
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
            ck("L5c: status NO_SUCH_DESCRIPTOR(2) - the image rules",
               static_cast<uint32_t>((b[16] >> 3) & 0x1F), 2u);
            ck("L5c: descriptor_index 9 echoed, not clamped to 0",
               static_cast<uint32_t>(get_be(b, 40, 2)), 9u);
            ck("L5c: counters_valid is EMPTY - no such sink here",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0u);
            long dirty = 0;
            for (int q = 0; q < 32; q++)
                if (get_be(b, 46 + 4 * static_cast<size_t>(q), 4) != 0) dirty++;
            ck("L5c: ...and the block is all zeros, not sink 0's numbers",
               static_cast<uint32_t>(dirty), 0u);
        }
    }

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
    void grade_padded_get_counters_ignores_the_tail() {
        uint8_t cf[128];
        size_t  cn = 0;
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
               static_cast<uint32_t>(get_be(b, 38, 2)), 0x0005u);
            ck("L5e: the index is @26's, NOT the padding at @30",
               static_cast<uint32_t>(get_be(b, 40, 2)), 0u);
            ck("L5e: ...so the mask is still Stream Input 0's",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0x0000'0FFFu);
        }
    }

    // THE WRONG-TYPE ANSWER, re-sized by the r49a bench round:
    // ENTITY counters are Table 7-155's ENTITY_SPECIFIC_1..8, this
    // build keeps none, and the refusal is Table 7-141's
    // NOT_SUPPORTED carried in the FULL fixed 7.4.42.2 body (zero
    // mask, zero block, cdl 148) - la_avdecc's checkResponsePayload
    // reflects ONLY NOT_IMPLEMENTED at command length and sizes
    // every other non-success answer against the response form; the
    // old 4-byte echo here was exactly its "Incorrect payload size"
    // complaint on the wire.
    void grade_get_counters_for_an_unsupported_type() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[4] = {
            0x00, 0x00, 0x00, 0x00};   // ENTITY 0
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
            ck("L5d: status NOT_SUPPORTED(11) - no ENTITY counters here",
               static_cast<uint32_t>((b[16] >> 3) & 0x1F), 11u);
            ck("L5d: descriptor_type ENTITY echoed",
               static_cast<uint32_t>(get_be(b, 38, 2)), 0u);
            ck("L5d: counters_valid ZERO in the full body",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0u);
            long dirty = 0;
            for (int q = 0; q < 32; q++)
                if (get_be(b, 46 + 4 * static_cast<size_t>(q), 4) != 0) dirty++;
            ck("L5d: ...and the block is all zeros", static_cast<uint32_t>(dirty), 0u);
        }
    }

    // --- L5e. GET_AUDIO_MAP answered for real, from the RENDER MAP RAM -
    // IEEE 1722.1-2021 7.4.44.2 response payload: descriptor_type @0,
    // descriptor_index @2, map_index @4, number_of_maps @6,
    // number_of_mappings @8, reserved @10, then 8-byte records @12.
    // Milan v1.2 5.3.3.9 makes every Stream Port Input dynamic, so this
    // command is the ONLY window a controller has onto an input's
    // mappings - a NOT_IMPLEMENTED here is "no mappings at all" to a
    // strict la_avdecc and fails its enumeration.
    //
    // WHAT THIS SECTION IS FOR: the processor lays the response out;
    // THIS repository decides what a mapping IS, by answering the
    // amap_* face from KL_chan_map_render's map RAM under the 0x001C
    // index law (global cluster index == render RAM address). The map
    // is provisioned through the CSR 0x900 debug window - the same
    // write port the AEM projector owned - and the GET must read back
    // exactly what was committed, with the reserved source encoding
    // (src = 1) EXCLUDED: it is not a STREAM_INPUT and 7.4.44.2.1 has
    // no words for it.
    //
    // THE GEOMETRY IS THE ELABORATED SHAPE'S: this suite includes the
    // endstation_arty_current header (channels_per_frame = 2), so the
    // port's window is clusters 0..1 in one page - which is exactly why
    // both provisioned slots sit inside it.

    // the 0x900 debug window's own offsets, `constexpr` for the same
    // reason the CSR block above is: they are addresses, not a closed
    // set, and each one goes straight into the BFM
    static constexpr uint16_t A_CHMAP_CTRL = 0x900;
    static constexpr uint16_t A_CHMAP_SEL  = 0x904;
    static constexpr uint16_t A_CHMAP_WORD = 0x908;
    static constexpr uint16_t A_CHMAP_SNAP = 0x910;
    static constexpr uint16_t A_CHMAP_LOOP = 0x914;

    // The section is one fixture read four ways: the map is provisioned
    // once, an independent CSR reader confirms what landed in the flops,
    // the wire answer is graded against it, and the map is then MOVED to
    // prove the answer tracks the RAM rather than a snapshot of it.
    void grade_get_audio_map_from_the_render_ram() {
        arm_the_render_map_through_the_csr_window();
        grade_the_render_ram_through_its_other_reader();
        grade_get_audio_map_page_zero();
        grade_get_audio_map_sees_the_added_mapping();
    }

    // arm the CSR write port, commit two entries, restore the arm
    // (the RAM keeps its contents; CHMAP_CTRL[0] only gates the
    // bring-up bypass and the write strobe, not the state)
    void arm_the_render_map_through_the_csr_window() {
        axi_write(A_CHMAP_CTRL, 0x1);
        // cluster 0 <- {en, src 0, stream 0, ch 1}: §5 word en[15],
        // src[12], stream[6:4], ch[2:0]
        axi_write(A_CHMAP_SEL, 0);
        axi_write(A_CHMAP_WORD, 0x8001);
        // cluster 1 <- {en, reserved src 1, index 2}: the encoding renders
        // silence and must not appear in the AEM dynamic-map response
        axi_write(A_CHMAP_SEL, 1);
        axi_write(A_CHMAP_WORD, 0x9002);
        axi_write(A_CHMAP_CTRL, 0x0);
    }

    // one cluster word, read back through the CHMAP_LOOP snapshot port
    uint32_t chmap_loop_read(uint32_t k) {
        axi_write(A_CHMAP_SEL, k);        // side 0 = RMAP
        axi_write(A_CHMAP_SNAP, 1);       // W1S arm
        for (int g = 0; g < 64; g++) {
            if ((axi_read(A_CHMAP_SNAP) & 1) == 0) break;
            run_idle(4);
        }
        return axi_read(A_CHMAP_LOOP);
    }

    // the OTHER reader first: CHMAP_LOOP 0x914 reads the render RAM
    // through its own port, so the wire answer below and this word
    // are two independent readers of the same flops - agreement of
    // the GET with a reader that shares its mux would prove nothing
    void grade_the_render_ram_through_its_other_reader() {
        ck("L5e0: CHMAP_LOOP reads cluster 0 back as {en, avb 0.1}",
           chmap_loop_read(0) & 0xFFFFu, 0x0081u);
        ck("L5e0: CHMAP_LOOP reads cluster 1 back as {en, reserved src 2}",
           chmap_loop_read(1) & 0xFFFFu, 0x00C2u);
    }

    // the wire answer for page 0, graded field by field against what the
    // CSR window committed and the loop port read back
    void grade_get_audio_map_page_zero() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x002B, 0x0140, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L5e GET_AUDIO_MAP(SPI 0, page 0) was ANSWERED", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_common(b, "L5e", 0x002B, 0x0140, 1);
            grade_len(b, "L5e", 12 + 8 * 1);
            ck("L5e: status SUCCESS(0), not NOT_IMPLEMENTED",
               (b[16] >> 3) & 0x1F, 0u);
            ck("L5e: descriptor_type echoed @0",
               static_cast<uint32_t>(get_be(b, 38, 2)), 0x000Eu);
            ck("L5e: descriptor_index echoed @2",
               static_cast<uint32_t>(get_be(b, 40, 2)), 0u);
            ck("L5e: map_index echoed @4", static_cast<uint32_t>(get_be(b, 42, 2)), 0u);
            // 2 clusters, page 2 -> ONE fixed partition (Milan 5.4.2.26)
            ck("L5e: number_of_maps @6 is the fixed partition count",
               static_cast<uint32_t>(get_be(b, 44, 2)), 1u);
            ck("L5e: number_of_mappings @8 counts the AVB entry only - "
               "the reserved-source cluster 1 is not a mapping",
               static_cast<uint32_t>(get_be(b, 46, 2)), 1u);
            ck("L5e: reserved @10 is zero", static_cast<uint32_t>(get_be(b, 48, 2)), 0u);
            // mono clusters: cluster_channel 0, and cluster_offset IS
            // the RAM address (base_cluster 0 on port 0)
            ck("L5e: record 0 = {stream 0, ch 1, cluster 0, chan 0}",
               static_cast<uint32_t>(get_be(b, 50, 4)), 0x00000001u);
            ck("L5e: record 0 offset half",
               static_cast<uint32_t>(get_be(b, 54, 4)), 0x00000000u);
        }
    }

    // ...and ADDITION is visible: the ring slot becomes an AVB
    // mapping {stream 0, ch 0} and the count moves 1 -> 2
    void grade_get_audio_map_sees_the_added_mapping() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
        axi_write(A_CHMAP_CTRL, 0x1);
        axi_write(A_CHMAP_SEL, 1);
        axi_write(A_CHMAP_WORD, 0x8000);
        axi_write(A_CHMAP_CTRL, 0x0);
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x002B, 0x0141, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L5e2 the re-read was ANSWERED", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_len(b, "L5e2", 12 + 8 * 2);
            ck("L5e2: number_of_mappings rose to 2",
               static_cast<uint32_t>(get_be(b, 46, 2)), 2u);
            ck("L5e2: record 1 is cluster 1's {stream 0, ch 0}",
               static_cast<uint32_t>(get_be(b, 58, 4)), 0x00000000u);
            ck("L5e2: record 1 offset half",
               static_cast<uint32_t>(get_be(b, 62, 4)), 0x00010000u);
        }
    }

    // --- L5f. the 7.4.44.1 page rule: map_index >= N is BAD_ARGUMENTS --
    // ...and the refusal still carries the full fixed part with the REAL
    // number_of_maps over an empty page (Milan 5.4.2.26: always N)
    void grade_get_audio_map_page_rule() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x0E, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00};
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x002B, 0x0142, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L5f GET_AUDIO_MAP(page 1 of 1) was ANSWERED", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_len(b, "L5f", 12);
            ck("L5f: status BAD_ARGUMENTS(7) - 7.4.44.1's page rule",
               (b[16] >> 3) & 0x1F, 7u);
            ck("L5f: number_of_maps still tells the real N",
               static_cast<uint32_t>(get_be(b, 44, 2)), 1u);
            ck("L5f: number_of_mappings 0 - an empty page, no records",
               static_cast<uint32_t>(get_be(b, 46, 2)), 0u);
        }
    }

    // --- L5g. an index past the image: NO_SUCH_DESCRIPTOR --------------
    // The IMAGE is the existence authority - the processor locates
    // STREAM_PORT_INPUT[1] in the same store READ_DESCRIPTOR serves and
    // misses, whatever the fabric's port constants would have said
    void grade_get_audio_map_absent_port() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x0E, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00};
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x002B, 0x0143, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L5g GET_AUDIO_MAP(SPI 1) was ANSWERED", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_len(b, "L5g", 12);
            ck("L5g: status NO_SUCH_DESCRIPTOR(2)",
               (b[16] >> 3) & 0x1F, 2u);
            ck("L5g: descriptor_index 1 echoed, not clamped",
               static_cast<uint32_t>(get_be(b, 40, 2)), 1u);
        }
    }

    // --- L5h. STREAM_PORT_OUTPUT: SERVED since the P5 landing ----------
    // Milan 5.4.2.26's second half runs through the same program with
    // the capture-side type constant, and EXISTENCE stays the image's:
    // this harness's hand image declares NO STREAM_PORT_OUTPUT, so the
    // honest answer is NO_SUCH_DESCRIPTOR carrying the full 7.4.44.2
    // fixed part (cdl 24) with the addressed type echoed - never the
    // old NOT_IMPLEMENTED echo and never an invented page
    void grade_get_audio_map_output_port() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[8] = {
            0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x002B, 0x0144, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L5h GET_AUDIO_MAP(STREAM_PORT_OUTPUT) was ANSWERED",
                k >= 0, k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_common(b, "L5h", 0x002B, 0x0144, 1);
            grade_len(b, "L5h", 12);
            ck("L5h: status NO_SUCH_DESCRIPTOR(2) - the image rules the "
               "served OUTPUT side too",
               (b[16] >> 3) & 0x1F, 2u);
            ck("L5h: the addressed type is in the fixed part",
               static_cast<uint32_t>(get_be(b, 38, 2)), 0x000Fu);
        }
    }

    // --- L6. IDENTIFY_NOTIFICATION as a COMMAND: BAD_ARGUMENTS ---------
    // IEEE 1722.1 7.4.39.2 makes 0x0026 a NOTIFICATION only; sent as a
    // command it is BAD_ARGUMENTS, and that opcode-specific rule beats
    // 9.3.5.3.3's NOT_IMPLEMENTED fallback. The two statuses are the
    // whole point of the check: a build that answered NOT_IMPLEMENTED
    // here would be applying the general rule to a specified case.
    void grade_identify_notification_as_command() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[4] = {
            0x00, 0x01, 0x00, 0x00};
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
    void grade_silent_refusal_leaves_the_plane_serving() {
        uint8_t cf[128];
        size_t  cn = 0;
        size_t at = tx_frames.size();
        cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0107);
        put64be(cf + 18, TEST_EID ^ 0xFFull);        // somebody else
        inject_rx(cf, cn, 400);
        run_idle(20000);
        ck("L7a: a command for ANOTHER entity gets no reply",
           static_cast<uint32_t>(last_aecp(at) >= 0 ? 1 : 0), 0u);

        at = tx_frames.size();
        cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0108);
        cf[15] = 0x01;                               // AEM_RESPONSE as input
        inject_rx(cf, cn, 400);
        run_idle(20000);
        ck("L7b: an AECP RESPONSE arriving as input gets no reply",
           static_cast<uint32_t>(last_aecp(at) >= 0 ? 1 : 0), 0u);

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

    // --- L8. Milan delta 7 ACQUIRE_ENTITY refusal ---------------------
    // Milan 5.4.2.1 requires NOT_SUPPORTED, never SUCCESS. The response
    // keeps the 7.4.1 body with owner_id zero. This used to be printed as
    // an unconditional gap after the processor had already landed the
    // registered ACQUIRE re-dispatch, which made a closed requirement
    // look open while leaving the real wire behavior ungraded.
    void grade_acquire_entity_is_refused() {
        uint8_t cf[128];
        size_t  cn = 0;
        uint8_t pl[16] = {};  // flags, owner_id, ENTITY type and index
        size_t at = tx_frames.size();
        cn = build_aecp(cf, 0, TEST_EID, 0x0000, 0x010A, pl, sizeof pl);
        inject_rx(cf, cn, 400);
        run_idle(20000);
        int k = last_aecp(at);
        ck_true("L8 ACQUIRE_ENTITY was ANSWERED", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            grade_common(b, "L8", 0x0000, 0x010A, 1);
            grade_len(b, "L8", sizeof pl);
            ck("L8: status NOT_SUPPORTED(11), never SUCCESS",
               (b[16] >> 3) & 0x1F, 11u);
            ck("L8: flags remain zero", static_cast<uint32_t>(get_be(b, 38, 4)), 0u);
            ck("L8: owner_id high remains zero",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0u);
            ck("L8: owner_id low remains zero",
               static_cast<uint32_t>(get_be(b, 46, 4)), 0u);
            ck("L8: ENTITY descriptor target remains zero",
               static_cast<uint32_t>(get_be(b, 50, 4)), 0u);
        }
    }

    // ---- M. NO DESCRIPTOR MEMORY: the DOCUMENTED degrade path --------------
    // An integration that offers the store nothing must not hang the µCPU.
    // KL_aecp_desc_store's watchdog abandons the burst, the image goes
    // invalid, and READ_DESCRIPTOR degrades to a well-formed
    // NO_SUCH_DESCRIPTOR. This is driven DELIBERATELY - the harness stops
    // answering - rather than being what a forgotten tie-off happens to do.
    void grade_descriptor_memory_withdrawn() {
        printf("[M] descriptor memory withdrawn: degrade, never wedge\n");
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
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
        ck_true("M: with no memory, READ_DESCRIPTOR still gets an ANSWER",
                k >= 0, k >= 0 ? "the watchdog degraded cleanly"
                               : "the uCPU HUNG on an absent bridge");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("M: status NO_SUCH_DESCRIPTOR(2)", (b[16] >> 3) & 0x1F, 2u);
            ck("M: control_data_length = 12 + the 8-byte stub payload",
               static_cast<uint32_t>(((static_cast<unsigned>(b[16]) & 7) << 8) | b[17]), 20u);
            ck("M: the frame is still padded to the Ethernet minimum",
               static_cast<uint32_t>(b.size()), 60u);
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
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
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
    void grade_response_buffer_memory() {
        printf("[N] response-buffer memory: exercised, then withdrawn\n");
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
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
        ck_true("N: with no memory, the command still gets an ANSWER", k >= 0,
                k >= 0 ? "the watchdog voided the response cleanly"
                       : "the uCPU HUNG on an absent bridge");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("N: status ENTITY_MISBEHAVING(10)", (b[16] >> 3) & 0x1F, 10u);
            ck("N: the response carries NO payload it could not build",
               static_cast<uint32_t>(((static_cast<unsigned>(b[16]) & 7) << 8) | b[17]), 12u);
            ck("N: the frame is still padded to the Ethernet minimum",
               static_cast<uint32_t>(b.size()), 60u);
            ck("N: ...and it is still addressed back to the requester",
               (static_cast<uint32_t>(b[0]) << 24) | (static_cast<uint32_t>(b[1]) << 16)
                   | (static_cast<uint32_t>(b[2]) << 8) | b[3], 0x02112233u);
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
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
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
    void grade_shared_control_lane() {
        printf("[K] ctl_tx_mux — the processor and MAAP share one lane, cleanly\n");
        run_idle(40000);
        long n_adp = 0;
        long n_acmp = 0;
        long n_aecp = 0;
        long n_maap = 0;
        long n_msrp = 0;
        long n_mvrp = 0;
        long n_alien = 0;
        long n_short = 0;
        long n_badlen = 0;
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
        ck("no frame on the wire was too short to classify", static_cast<uint32_t>(n_short), 0u);
        ck("no frame carried an unknown EtherType", static_cast<uint32_t>(n_alien), 0u);
        ck("every AVTP PDU's length matches the length it declares",
           static_cast<uint32_t>(n_badlen), 0u);
        ck("no beat before tlast carried a partial tkeep", static_cast<uint32_t>(tx_bad_keep), 0u);
        // the MAAP frames really are KL_maap's, not a mislabelled fragment
        long maap_wrong_da = 0;
        for (const TxFrame& fr : tx_frames)
            if (classify(fr) == FR_MAAP && get_be(fr.bytes, 0, 6) != MAAP_DST)
                maap_wrong_da++;
        ck("every MAAP PDU carried KL_maap's own DA", static_cast<uint32_t>(maap_wrong_da), 0u);

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
    void grade_global_anti_wedge_invariant() {
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
           static_cast<uint32_t>(mo.released), 0u);
    }

    // ---- M2. HEAL BEFORE ANSWER: the silicon arrangement, end to end ------
    // (r49a/w3a, 2026-08-15: the store parks at boot - pre-handover the DFI
    //  gate refuses the memory - and the loader lands the image AFTER. On
    //  the old order the FIRST wire command answered its miss from the
    //  parked state and only the SECOND was served: a first READ_DESCRIPTOR
    //  came back BAD_ARGUMENTS on w3a, a first GET_COUNTERS came back
    //  NO_SUCH_DESCRIPTOR on r49a. No suite ever built this arrangement -
    //  the image was always in memory before the first clock - which is why
    //  sim stayed green while silicon raced. This section IS the silicon
    //  sequence: park, hand the memory over, then demand the FIRST
    //  locate-bearing command be served.)
    void grade_heal_before_answer() {
        printf("[M2] heal-before-answer: park, hand over, first command serves\n");
        mem_answering = false;                 // pre-handover: memory refused
        do_reset();                            // the boot walk parks
        // re-provision (the reset wiped the CSR plane)
        axi_write(A_MAC_ALO, STA_MAC_LO);
        axi_write(A_MAC_AHI, STA_MAC_HI);
        axi_write(A_ADP_EIDLO, static_cast<uint32_t>(TEST_EID & 0xFFFFFFFFu));
        axi_write(A_ADP_EIDHI, static_cast<uint32_t>(TEST_EID >> 32));
        axi_write(A_ADP_MDLLO, static_cast<uint32_t>(TEST_MODEL & 0xFFFFFFFFu));
        axi_write(A_ADP_MDLHI, static_cast<uint32_t>(TEST_MODEL >> 32));
        axi_write(A_ADP_CAPS,  0x0000C588u);
        axi_write(A_PP_CTRL, 0x1);             // entity_enable
        // let the walk burn its watchdog into the parked fault
        for (int r = 0; r < 6; r++) run_idle(20000);
        mem_answering = true;                  // HANDOVER: memory + image now
        // the FIRST locate-bearing command after the handover must SERVE
        uint8_t cf[128];
        size_t at = tx_frames.size();
        size_t cn = build_read_desc(cf, 0, DTY_ENTITY_C, 0, 0x0301);
        inject_rx(cf, cn, 400);
        for (int r = 0; r < 4; r++) run_idle(20000);
        int k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
        ck_true("M2: the FIRST post-handover command was answered", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("M2: ...and SERVED, not sacrificed to the re-arm (status)",
               (b[16] >> 3) & 0x1F, 0u);
            ck("M2: the ENTITY descriptor's cdl (12 + 4 + 40)",
               static_cast<uint32_t>(((static_cast<unsigned>(b[16]) & 7) << 8) | b[17]), 56u);
            //! the hand image's ENTITY body is the seed pattern (desc_bytes:
            //! seed 0xA0, byte i = seed + i), so descriptor bytes 4..7 on
            //! the wire (frame 46..49) must read A4 A5 A6 A7 - the IMAGE'S
            //! OWN bytes, proving the walk that served this command is the
            //! one that read the freshly handed-over memory
            ck("M2: the served bytes are the image's (seed body @4..7)",
               static_cast<uint32_t>(get_be(b, 46, 4)), 0xA4A5A6A7u);
        }
        // the SECOND command serves too, and the counters path is sane
        at = tx_frames.size();
        {
            uint8_t pl[4] = {
                0x00, 0x05, 0x00, 0x00};   // STREAM_INPUT 0
            cn = build_aecp(cf, 0, TEST_EID, 0x0029, 0x0302, pl, sizeof pl);
            inject_rx(cf, cn, 400);
            for (int r = 0; r < 4; r++) run_idle(20000);
        }
        k = -1;
        for (size_t i = tx_frames.size(); i-- > at; )
            if (classify(tx_frames[i]) == FR_AECP) { k = static_cast<int>(i); break; }
        ck_true("M2: the second command (GET_COUNTERS) answered", k >= 0,
                k >= 0 ? "an AECPDU egressed" : "SILENCE");
        if (k >= 0) {
            const std::vector<uint8_t>& b = tx_frames[k].bytes;
            ck("M2: GET_COUNTERS STREAM_INPUT 0 is SUCCESS",
               (b[16] >> 3) & 0x1F, 0u);
            ck("M2: ...with the twelve-counter mask, not a raced zero",
               static_cast<uint32_t>(get_be(b, 42, 4)), 0x00000FFFu);
        }
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    PpShadowHarness harness;
    return harness.run();
}

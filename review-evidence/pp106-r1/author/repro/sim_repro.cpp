// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// SCRATCH reproduction for issue #530 (not part of the lane). milan_datapath
// at the AX7101 1x1 TDM8 shape (the flashed product shape, CRF source uid 1),
// the processor's millisecond compressed to 100 cycles and KL_maap on the
// same grid (the pp_shadow recipe). A scripted Milan listener and a scripted
// bridge port play the bench roles:
//   * the listener probes the CRF source (PROBE_TX = CONNECT_TX_COMMAND),
//     re-probes after TALKER_DEST_MAC_FAILED (4 s) and after the Talker
//     attribute disappears (0.5 s);
//   * the bridge declares Listener Ready for the CRF stream toward the DUT,
//     withdraws it 2 ms after a Talker Leave, re-declares it after a Talker
//     re-declaration, runs its own LeaveAll every BR_LA_MS with its re-join
//     in the same vector, and answers a DUT LeaveAll by re-declaring - in
//     one of two scopes selected by argv[1]:
//       app  : any MSRP LeaveAllEvent from the DUT (per-application scope)
//       type : only a LeaveAllEvent on a Listener-type message (per
//              attribute-type scope)
// Everything observed is logged with compressed-ms timestamps.
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "verilated.h"
#include <cstdio>
#include <cstdarg>
#include <algorithm>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <deque>

namespace {

constexpr int MS = 100;                 // cycles per compressed millisecond
constexpr uint64_t TEST_EID = 0x001BC50CAC000001ull;
constexpr uint32_t STA_MAC_LO = 0x00000002u;
constexpr uint32_t STA_MAC_HI = 0x00000100u;

struct Vec { int type; int la; int nov; std::vector<uint8_t> fv; std::vector<int> ev; std::vector<int> fp; };

class Repro {
 public:
    explicit Repro(bool per_type, long br_la_ms, long run_ms, bool bridge_la, bool sw_la, long sw_restart_ms)
        : per_type_(per_type), br_la_ms_(br_la_ms), run_ms_(run_ms), bridge_la_(bridge_la), sw_la_(sw_la), sw_restart_ms_(sw_restart_ms) {}
    bool sw_la_; long sw_restart_ms_;

    int run() {
        dut = new Vmilan_datapath;
        reset();
        axi_write(0x108, STA_MAC_LO); axi_write(0x10C, STA_MAC_HI);
        axi_write(0x604, uint32_t(TEST_EID)); axi_write(0x608, uint32_t(TEST_EID >> 32));
        // firmware configure_fabric() values
        axi_write(0x654, (2u << 16) | 1u);      // AAF_CTRL: VID 2, enable, no bypass
        axi_write(0x684, 2u);                   // LWSRP_VID
        axi_write(0x680, 0x10u | 3u);           // LWSRP_CTRL reset | engine | talker
        axi_write(0x6CC, (2u << 8) | 1u);       // MAAP_CTRL count N+1 = 2, en
        axi_write(0x750, 0x3u);                 // CRFT_CTRL boot: enable + class-A declare
        axi_write(0x920, 0x1u);                 // PP_CTRL entity enable
        bool ann = false;
        for (int r = 0; r < 400 && !ann; r++) { idle(2000); ann = (axi_read(0x6D4) >> 2) & 1u; }
        printf("MAAP announce: %s CRFT_CTRL=0x%08X\n", ann ? "yes" : "NO", axi_read(0x750));
        idle(300 * MS);
        t0 = cyc;
        log("start: no Listener declared, CRFT_CTRL=0x%08X", axi_read(0x750));

        // the listener's first probe
        send_probe();
        long next_retry = -1;
        while (now_ms() < run_ms_) {
            step();
            service();
            if (probe_rsp_pending_ >= 0) {
                int st = probe_rsp_pending_; probe_rsp_pending_ = -1;
                if (st == 3) { next_retry = now_ms() + 4000; }     // TMR_RETRY
            }
            if (next_retry >= 0 && now_ms() >= next_retry) { next_retry = -1; send_probe(); }
        }
        summary();
        dut->final();
        delete dut;
        return 0;
    }

 private:
    Vmilan_datapath* dut = nullptr;
    uint64_t cyc = 0, t0 = 0;
    bool per_type_;
    long br_la_ms_, run_ms_;
    bool bridge_la_;
    uint64_t crf_sid = 0x0200000000010001ull;

    // ---- observed state ----
    int lic_prev = -1, decl_prev = -1, lreg_prev = -1, act_prev = -1, adm_prev = -1;
    long crf_pdus = 0, crf_pdus_nolistener = 0;
    long lic_on_ms = -1;
    bool listener_seen_ = false;       // bridge has declared a Listener at least once
    bool bridge_declared_ = false;     // bridge currently declares the Listener
    long first_ready_ms = -1, first_crf_ms = -1;
    int probe_rsp_pending_ = -1;
    long last_probe_ok_ms = -1;
    std::vector<std::string> events;

    // scheduled bridge/listener actions (ms)
    long sched_lv = -1, sched_join = -1, sched_probe = -1, sched_redecl = -1;
    long next_br_la = -1;

    // TX capture
    std::vector<uint8_t> txb; bool txopen = false;

    long now_ms() const { return long((cyc - t0) / MS); }
    double now_msf() const { return double(cyc - t0) / MS; }

    void log(const char* fmt, ...) __attribute__((format(printf, 2, 3))) {
        char buf[512]; va_list ap; va_start(ap, fmt); vsnprintf(buf, sizeof buf, fmt, ap); va_end(ap);
        char line[600]; snprintf(line, sizeof line, "%10.2f ms  %s", now_msf(), buf);
        printf("%s\n", line); events.push_back(line);
    }

    void lo() { dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0; drive_rx(); dut->eval(); observe(); }
    void hi() { dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->eval(); cyc++; }
    void step() { lo(); hi(); }
    void idle(int n) { dut->m_axis_mac_tx_tready = 1; for (int i = 0; i < n; i++) { step(); if (t0) service(); } }

    void reset() {
        dut->axis_resetn = 0; dut->gtx_resetn = 0;
        dut->m_axis_mac_tx_tready = 1;
        dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1;
        for (int i = 0; i < 8; i++) step();
        dut->axis_resetn = 1; dut->gtx_resetn = 1;
        for (int i = 0; i < 16; i++) step();
    }

    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1; dut->s_axi_wdata = d; dut->s_axi_wstrb = 0xF;
        dut->s_axi_wvalid = 1; dut->s_axi_bready = 1;
        for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_awready && dut->s_axi_wready; hi(); if (acc) break; }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < 2048; g++) { lo(); bool bv = dut->s_axi_bvalid; hi(); if (bv) break; }
        dut->s_axi_bready = 0;
    }
    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < 2048; g++) { lo(); bool acc = dut->s_axi_arready; hi(); if (acc) break; }
        dut->s_axi_arvalid = 0; uint32_t d = 0;
        for (int g = 0; g < 2048; g++) { lo(); bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi(); if (rv) break; }
        dut->s_axi_rready = 0; return d;
    }

    // ---- RX injection queue (little-lane), one frame at a time ----
    std::deque<std::vector<uint8_t>> rxq; std::vector<uint64_t> rxw; std::vector<uint8_t> rxk; size_t rxi = 0;
    void drive_rx() {
        if (rxi >= rxw.size() && !rxq.empty()) {
            auto f = rxq.front(); rxq.pop_front();
            size_t beats = (f.size() + 7) / 8; rxw.assign(beats, 0); rxk.assign(beats, 0); rxi = 0;
            for (size_t i = 0; i < f.size(); i++) { rxw[i / 8] |= uint64_t(f[i]) << (8 * (i % 8)); rxk[i / 8] |= uint8_t(1u << (i % 8)); }
        }
        if (rxi < rxw.size()) {
            dut->s_axis_mac_rx_tdata = rxw[rxi]; dut->s_axis_mac_rx_tkeep = rxk[rxi];
            dut->s_axis_mac_rx_tvalid = 1; dut->s_axis_mac_rx_tlast = (rxi == rxw.size() - 1);
        } else { dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0; }
    }

    void observe() {
        // RX handshake bookkeeping (settled pre-edge)
        if (dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready) rxi++;
        auto* rp = dut->rootp;
        if (t0) {
            const int lic  = rp->milan_datapath__DOT__crft_emit_en_w & 1;
            const int decl = (rp->milan_datapath__DOT__pp_cd_acmp_declaring_w >> 1) & 1;
            const int lreg = (rp->milan_datapath__DOT__pp_cd_srp_lstn_reg_state_w >> 2) & 3;
            const int act  = (rp->milan_datapath__DOT__pp_cd_srp_active_w >> 1) & 1;
            const int adm  = (rp->milan_datapath__DOT__pp_cd_srp_sr_admitted_w >> 1) & 1;
            if (lic != lic_prev) { log("CRF emission licence -> %d (declaring=%d lstn_reg=%d sr_admitted=%d active=%d)", lic, decl, lreg, adm, act); lic_prev = lic; if (lic) lic_on_ms = now_ms(); }
            if (decl != decl_prev) { log("DA gate (acmp_declaring[CRF]) -> %d", decl); decl_prev = decl; }
            if (lreg != lreg_prev) { log("registered Listener on the CRF source (lstn_reg_state) -> %d", lreg); lreg_prev = lreg; }
            if (act != act_prev) { log("processor ACTIVE[CRF] -> %d", act); act_prev = act; }
            if (adm != adm_prev) { log("processor sr_admitted[CRF] -> %d", adm); adm_prev = adm; }
        }
        if (dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready) {
            if (!txopen) { txb.clear(); txopen = true; }
            const uint8_t k = uint8_t(dut->m_axis_mac_tx_tkeep); const uint64_t d = dut->m_axis_mac_tx_tdata;
            for (int l = 0; l < 8; l++) if ((k >> l) & 1) txb.push_back(uint8_t(d >> (8 * l)));
            if (dut->m_axis_mac_tx_tlast) { txopen = false; if (t0) on_tx(txb); }
        }
    }

    static uint64_t be(const std::vector<uint8_t>& b, size_t o, size_t n) { uint64_t v = 0; for (size_t i = 0; i < n && o + i < b.size(); i++) v = (v << 8) | b[o + i]; return v; }

    std::vector<Vec> parse_mrp(const std::vector<uint8_t>& b) {
        std::vector<Vec> out; size_t p = 15;
        while (p + 1 < b.size()) {
            if (b[p] == 0 && b[p + 1] == 0) break;
            if (p + 4 > b.size()) break;
            int at = b[p], al = b[p + 1]; size_t all = size_t(be(b, p + 2, 2)); p += 4; size_t end = p + all;
            while (p + 1 < end && p + 1 < b.size()) {
                int vh = int(be(b, p, 2)); p += 2; if (vh == 0) break;
                Vec v; v.type = at; v.la = (vh >> 13) & 7; v.nov = vh & 0x1FFF;
                v.fv.assign(b.begin() + long(p), b.begin() + long(std::min(b.size(), p + size_t(al)))); p += size_t(al);
                int n3 = (v.nov + 2) / 3;
                for (int i = 0; i < n3 && p < b.size(); i++, p++) { int x = b[p]; v.ev.push_back(x / 36); v.ev.push_back((x / 6) % 6); v.ev.push_back(x % 6); }
                v.ev.resize(size_t(v.nov));
                if (at == 3) { int n4 = (v.nov + 3) / 4; for (int i = 0; i < n4 && p < b.size(); i++, p++) { int x = b[p]; v.fp.push_back(x >> 6); v.fp.push_back((x >> 4) & 3); v.fp.push_back((x >> 2) & 3); v.fp.push_back(x & 3); } v.fp.resize(size_t(v.nov)); }
                out.push_back(v);
            }
            p = end;
        }
        return out;
    }

    void on_tx(const std::vector<uint8_t>& b) {
        if (b.size() < 18) return;
        size_t o = 12; if (be(b, 12, 2) == 0x8100) o = 16;
        const unsigned et = unsigned(be(b, o, 2));
        if (et == 0x22F0 && b[o + 2] == 0x04) {       // CRF AVTPDU
            crf_pdus++; if (first_crf_ms < 0) { first_crf_ms = now_ms(); log("first CRF PDU on the wire (tagged=%d)", o == 16); }
            if (!bridge_declared_) crf_pdus_nolistener++;
            return;
        }
        if (et == 0x22F0 && b[o + 2] == 0xFC && (b[15] & 0xF) == 1) {   // CONNECT_TX_RESPONSE
            const int st = (b[16] >> 3) & 0x1F;
            if (st == 0) { crf_sid = be(b, 18, 8); last_probe_ok_ms = now_ms(); }
            log("PROBE_TX response status %d (stream_id %016llx)", st, (unsigned long long)be(b, 18, 8));
            probe_rsp_pending_ = st; return;
        }
        if (et == 0x22EA) {
            auto vs = parse_mrp(b);
            std::string s; bool any_la = false, lsn_la = false, ta_lv = false, ta_join = false;
            for (auto& v : vs) {
                char t[160];
                uint64_t sid = v.fv.size() >= 8 ? be(v.fv, 0, 8) : 0;
                snprintf(t, sizeof t, " [type %d la %d n %d ev0 %d%s]", v.type, v.la, v.nov, v.ev.empty() ? -1 : v.ev[0], (v.type == 1 && sid == crf_sid) ? " CRF" : "");
                s += t;
                if (v.la) { any_la = true; if (v.type == 3) lsn_la = true; }
                if (v.type == 1 && sid == crf_sid && !v.ev.empty()) { if (v.ev[0] == 5) ta_lv = true; if (v.ev[0] <= 1) ta_join = true; }
            }
            log("DUT MSRP PDU:%s", s.c_str());
            if (ta_lv && bridge_declared_) { sched_lv = now_ms() + 2; sched_probe = now_ms() + 500; }
            if (ta_join && !bridge_declared_ && listener_seen_ && sched_join < 0) sched_join = now_ms() + 5;
            if (any_la && bridge_declared_ && (!per_type_ || lsn_la)) sched_redecl = now_ms() + 20;
            if (any_la && sw_la_ && sw_restart_ms_ > 0 && next_br_la >= 0) next_br_la = now_ms() + sw_restart_ms_;
            return;
        }
    }

    void push(const uint8_t* f, size_t n) { rxq.emplace_back(f, f + n); }

    static void put64(uint8_t* p, uint64_t v) { for (int i = 0; i < 8; i++) p[i] = uint8_t(v >> (8 * (7 - i))); }
    static void put16(uint8_t* p, uint16_t v) { p[0] = uint8_t(v >> 8); p[1] = uint8_t(v); }

    void send_probe() {
        uint8_t f[70]; memset(f, 0, sizeof f);
        const uint8_t da[6] = {0x91, 0xE0, 0xF0, 0x01, 0x00, 0x00}; const uint8_t sa[6] = {0x02, 0x11, 0x22, 0x33, 0x44, 0x55};
        memcpy(f, da, 6); memcpy(f + 6, sa, 6); f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFC; f[15] = 0x00; f[17] = 44;
        put64(f + 18, TEST_EID); put64(f + 26, 0xC0FFEE00DEADBEEFull); put64(f + 34, TEST_EID);
        put64(f + 42, 0x2222222222222222ull); f[50] = 0; f[51] = 1;   // talker_unique_id 1 = CRF
        f[62] = 0; f[63] = uint8_t(++seq_);
        push(f, 70); log("listener sends PROBE_TX to the CRF source");
    }
    int seq_ = 0;

    void send_listener(int ev, int decl, int la) {
        uint8_t f[60]; memset(f, 0, sizeof f);
        const uint8_t da[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E}; const uint8_t sa[6] = {0x02, 0x0B, 0x21, 0x00, 0x00, 0x0E};
        memcpy(f, da, 6); memcpy(f + 6, sa, 6); f[12] = 0x22; f[13] = 0xEA; f[14] = 0; f[15] = 3; f[16] = 8;
        put16(f + 17, 14); put16(f + 19, uint16_t((la << 13) | 1)); put64(f + 21, crf_sid);
        f[29] = uint8_t(ev * 36); f[30] = uint8_t(decl << 6);
        push(f, 60);
        log("bridge sends Listener %s%s for the CRF stream", ev == 5 ? "Lv" : (ev == 1 ? "JoinIn Ready" : "?"), la ? " with LeaveAll" : "");
    }

    void send_switch_la() {
        std::vector<uint8_t> f(14, 0);
        const uint8_t da[6] = {0x01, 0x80, 0xC2, 0x00, 0x00, 0x0E}; const uint8_t sa[6] = {0x02, 0x0B, 0x21, 0x00, 0x00, 0x0E};
        memcpy(f.data(), da, 6); memcpy(f.data() + 6, sa, 6); f[12] = 0x22; f[13] = 0xEA;
        f.push_back(0x00);                                               // ProtocolVersion
        const uint8_t lsn[6] = {0x03, 0x08, 0x00, 0x0E, 0x20, 0x01};    // Listener, LeaveAll, n 1
        f.insert(f.end(), lsn, lsn + 6);
        for (int i = 7; i >= 0; i--) f.push_back(uint8_t(crf_sid >> (8 * i)));
        f.push_back(0x6C); f.push_back(0x80); f.push_back(0); f.push_back(0);   // JoinMt / Ready, EndMark
        const uint8_t dom[13] = {0x04, 0x04, 0x00, 0x09, 0x20, 0x02, 0x05, 0x02, 0x00, 0x02, 0x7E, 0x00, 0x00};
        f.insert(f.end(), dom, dom + 13);                                 // Domain {5,2,2} n 2
        const uint8_t ta[6] = {0x01, 0x19, 0x00, 0x1D, 0x20, 0x00};
        f.insert(f.end(), ta, ta + 6); f.insert(f.end(), 25, 0); f.push_back(0); f.push_back(0);
        const uint8_t tf[6] = {0x02, 0x22, 0x00, 0x26, 0x20, 0x00};
        f.insert(f.end(), tf, tf + 6); f.insert(f.end(), 34, 0); f.push_back(0); f.push_back(0);
        f.push_back(0); f.push_back(0);                                   // MRPDU EndMark
        push(f.data(), f.size());
        log("bridge sends its LeaveAll MRPDU in the bench switch's layout: [Listener LA JoinMt/Ready][Domain LA n2][TA LA n0][TF LA n0]");
    }

    void service() {
        const long t = now_ms();
        if (sched_lv >= 0 && t >= sched_lv) { sched_lv = -1; send_listener(5, 2, 0); bridge_declared_ = false; }
        if (sched_probe >= 0 && t >= sched_probe) { sched_probe = -1; send_probe(); }
        if (sched_join >= 0 && t >= sched_join) { sched_join = -1; send_listener(1, 2, 0); bridge_declared_ = true; }
        if (sched_redecl >= 0 && t >= sched_redecl) { sched_redecl = -1; if (bridge_declared_) send_listener(1, 2, 0); }
        // the listener's first Ready follows its first successful probe (bench: 4.7 s)
        if (!listener_seen_ && last_probe_ok_ms >= 0 && t >= last_probe_ok_ms + 30) {
            listener_seen_ = true; bridge_declared_ = true; first_ready_ms = t; send_listener(1, 2, 0);
            next_br_la = t + br_la_ms_;
        }
        if (bridge_la_ && next_br_la >= 0 && t >= next_br_la) {
            next_br_la = t + br_la_ms_;
            if (bridge_declared_) { if (sw_la_) send_switch_la(); else send_listener(1, 2, 1); }
        }
    }

    void summary() {
        printf("---- summary (%s-scope bridge) ----\n", per_type_ ? "attribute-type" : "application");
        printf("CRF PDUs on the wire: %ld, of which with no Listener declared by the bridge: %ld\n", crf_pdus, crf_pdus_nolistener);
        printf("first CRF PDU at %ld ms, first Listener Ready at %ld ms\n", first_crf_ms, first_ready_ms);
    }
};

}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const bool sw_la = (argc > 1 && std::string(argv[1]) == "switch");
    const bool per_type = (argc > 1 && (std::string(argv[1]) == "type" || sw_la));
    const long sw_restart = (argc > 5) ? atol(argv[5]) : 9990;
    const long br_la = (argc > 2) ? atol(argv[2]) : 12500;
    const long run_ms = (argc > 3) ? atol(argv[3]) : 60000;
    const bool bridge_la = !(argc > 4 && std::string(argv[4]) == "nobla");
    Repro r(per_type, br_la, run_ms, bridge_la, sw_la, sw_restart);
    return r.run();
}

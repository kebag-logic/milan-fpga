// SPDX-License-Identifier: CERN-OHL-W-2.0
// Real AECP, receive acceptance, committed maps and transmitted loopback audio.
#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "geometry.hpp"
#include "verilated.h"
#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
extern "C" {
#include "aecp.h"
#include "aecp_image.h"
#include "aecp_entity_gen.h"
}
#include <map>
#include <vector>

namespace {
constexpr int kStreams = kCfgStreams;
constexpr int kChans = 8;
constexpr int kBusSlots = kCfgBusSlots;
constexpr int kAxiGuardCycles = 2048;
constexpr int kEvents = 6;
constexpr size_t kPayloadBytes = kChans*kEvents*4;
constexpr size_t kFrameBytes = 38+kPayloadBytes;
constexpr long kPduPeriodCycles = 12500;
constexpr double kModelNsPerAxis = 10;
constexpr long kAudNum = 391*kBusSlots/8;
constexpr long kAudDen = 1591;
constexpr int kFrameBclks = kBusSlots*32;
constexpr long kLeadFrames = 24;
constexpr uint32_t kMarker = 0x800000u;
constexpr uint32_t kEventMask = 0x1FFFFu;
constexpr int kFirst = kStreams == 1 ? 8 : 1;
constexpr int kDestinations = kStreams == 1 ? 8 : 63;
constexpr int kLead = kStreams == 1 ? 2 : 1;
constexpr uint32_t sample_word(int s,int c,long e) {
    return kMarker | (unsigned(s)<<20) | (unsigned(c)<<17) | unsigned(e);
}
class Harness {
public:
    int run();
private:
    Vmilan_datapath* dut = nullptr;
    milan::tb::Checker check{"input_loopback_dp"};
    long acc = 0;
    int aud = 0;
    long axis_cycle = 0;

    void half() {
        acc += kAudNum;
        if (acc >= kAudDen) { acc -= kAudDen; aud ^= 1; }
        dut->clk_audio_i = aud;
        dut->clk_tdm_i = aud;
    }
    void lo() {
        dut->axis_clk = 0; dut->gtx_clk = 0;
        half(); dut->eval();
        observe_audio();
    }
    void hi() {
        dut->axis_clk = 1; dut->gtx_clk = 1;
        half(); dut->eval();
        ++axis_cycle;
        observe_domain();
        drp_respond();
    }
    int drp_lat = 0;
    void drp_respond() {
        dut->i_mmcm_drp_rdy = 0;
        if (drp_lat > 0 && --drp_lat == 0) dut->i_mmcm_drp_rdy = 1;
        if (dut->o_mmcm_drp_en) drp_lat = 3;
        dut->i_mmcm_drp_do = 0;
    }

    uint64_t dom_ns_last = 0;
    const double ps_phc = 2.0 * kFrameBclks * static_cast<double>(kAudDen) /
                          static_cast<double>(kAudNum) * kModelNsPerAxis;
    std::array<bool, kStreams> anchored{};
    std::array<double, kStreams> anchor_ns{};
    std::array<long, kStreams> anchor_ord{};
    std::array<std::vector<double>, kStreams> pt_ns;

    void observe_domain() {
        dom_ns_last = dut->rootp->milan_datapath__DOT__dom_ns_w;
    }
    double stamp_the_event(int s, long ord) {
        const size_t i = static_cast<size_t>(s);
        double pt = anchor_ns[i] + static_cast<double>(ord - anchor_ord[i]) * ps_phc;
        const double floor_ns = static_cast<double>(dom_ns_last) + 0.5 * kLeadFrames * ps_phc;
        if (!anchored[i] || pt < floor_ns) {
            anchored[i] = true;
            anchor_ord[i] = ord;
            anchor_ns[i] = static_cast<double>(dom_ns_last) + kLeadFrames * ps_phc;
            pt = anchor_ns[i];
        }
        return pt;
    }
    void record_pt(int s, long ord, double pt) {
        auto& v = pt_ns[static_cast<size_t>(s)];
        if (static_cast<long>(v.size()) <= ord) v.resize(static_cast<size_t>(ord) + 1, -1.0);
        v[static_cast<size_t>(ord)] = pt;
    }
    double pt_of(int s, long ord) const {
        const auto& v = pt_ns[static_cast<size_t>(s)];
        return (ord >= 0 && ord < static_cast<long>(v.size())) ? v[static_cast<size_t>(ord)] : -1.0;
    }
    double slot0_offset() const { return ps_phc / static_cast<double>(kFrameBclks); }

    void axi_write(uint16_t a, uint32_t d) {
        dut->s_axi_awaddr = a; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = d; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool acc_w = dut->s_axi_awready && dut->s_axi_wready; hi();
            if (acc_w) break;
        }
        dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool bv = dut->s_axi_bvalid; hi(); if (bv) break;
        }
        dut->s_axi_bready = 0;
    }
    uint32_t axi_read(uint16_t a) {
        dut->s_axi_araddr = a; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool ar = dut->s_axi_arready; hi(); if (ar) break;
        }
        dut->s_axi_arvalid = 0;
        uint32_t d = 0;
        for (int g = 0; g < kAxiGuardCycles; g++) {
            lo(); const bool rv = dut->s_axi_rvalid; if (rv) d = dut->s_axi_rdata; hi();
            if (rv) break;
        }
        dut->s_axi_rready = 0;
        return d;
    }
    void inject(const uint8_t* f, size_t len) {
        std::vector<uint64_t> beats;
        for (size_t bt = 0; bt < (len + 7) / 8; bt++) {
            uint64_t v = 0;
            for (size_t j = 0; j < 8; j++)
                if (bt * 8 + j < len) v |= static_cast<uint64_t>(f[bt * 8 + j]) << (8 * j);
            beats.push_back(v);
        }
        size_t idx = 0;
        for (int c = 0; c < 1500 && idx < beats.size() + 8; c++) {
            if (idx < beats.size()) {
                dut->s_axis_mac_rx_tdata = beats[idx];
                dut->s_axis_mac_rx_tkeep = 0xFF;
                dut->s_axis_mac_rx_tvalid = 1;
                dut->s_axis_mac_rx_tlast = (idx == beats.size() - 1);
            } else {
                dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
            }
            lo();
            const bool in_acc = dut->s_axis_mac_rx_tvalid && dut->s_axis_mac_rx_tready;
            hi();
            if (in_acc || idx >= beats.size()) idx++;
        }
        dut->s_axis_mac_rx_tvalid = 0; dut->s_axis_mac_rx_tlast = 0;
    }

    static std::array<uint8_t, 8> sid_of(int s) {
        return {0x02, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, static_cast<uint8_t>(2 * s)};
    }
    static std::array<uint8_t, 6> dmac_of(int s) {
        return {0x91, 0xE0, 0xF0, 0x00, 0x2A, static_cast<uint8_t>(0x02 + 2 * s)};
    }
    unsigned feed_mask = 0;
    long next_pdu_at = 0;
    std::array<uint8_t, kStreams> wire_seq{};
    std::array<long, kStreams> injected{};

    void send_pdu(int s) {
        uint8_t f[kFrameBytes];
        memset(f, 0, sizeof f);
        const auto dmac = dmac_of(s);
        memcpy(f, dmac.data(), 6);
        const uint8_t src[6] = {0x02, 0x00, 0x00, 0x00, 0x00, 0x02};
        memcpy(f + 6, src, 6);
        f[12] = 0x22; f[13] = 0xF0;
        f[14] = 0x02;                                // AAF
        f[15] = 0x81;                                // sv, tv
        f[16] = wire_seq[static_cast<size_t>(s)]++;
        const auto sid = sid_of(s);
        memcpy(f + 18, sid.data(), 8);
        const long base = injected[static_cast<size_t>(s)];
        long carried = base;
        const double ts = stamp_the_event(s, base);
        const uint32_t ts32 = static_cast<uint32_t>(static_cast<uint64_t>(std::llround(ts)));
        f[26] = static_cast<uint8_t>(ts32 >> 24); f[27] = static_cast<uint8_t>(ts32 >> 16);
        f[28] = static_cast<uint8_t>(ts32 >> 8);  f[29] = static_cast<uint8_t>(ts32);
        for (int k = 0; k < kEvents; k++) record_pt(s, base + k, ts + k * ps_phc);
        f[30] = 0x02;                                // INT32
        f[31] = static_cast<uint8_t>(0x05 << 4);     // 48 kHz
        f[32] = static_cast<uint8_t>(kChans);
        f[33] = 32;
        f[34] = static_cast<uint8_t>(kPayloadBytes >> 8);
        f[35] = static_cast<uint8_t>(kPayloadBytes & 0xFF);
        for (int k = 0; k < kEvents; k++)
            for (int c = 0; c < kChans; c++) {
                const uint32_t v = sample_word(s, c, carried + k);
                const size_t o = 38 + 4 * (static_cast<size_t>(k) * kChans + static_cast<size_t>(c));
                f[o] = static_cast<uint8_t>(v >> 16);
                f[o + 1] = static_cast<uint8_t>(v >> 8);
                f[o + 2] = static_cast<uint8_t>(v);
                f[o + 3] = 0;
            }
        injected[static_cast<size_t>(s)] += kEvents;
        inject(f, kFrameBytes);
    }
    void step() {
        if (feed_mask != 0 && axis_cycle >= next_pdu_at) {
            for (int s = 0; s < kStreams; s++)
                if ((feed_mask >> s) & 1u) send_pdu(s);
            next_pdu_at += kPduPeriodCycles;
            return;
        }
        lo();
        hi();
    }
    void steps(long n) { while (n--) step(); }
    void run_pdus(long n) {
        const long stop = axis_cycle + n * kPduPeriodCycles;
        while (axis_cycle < stop) step();
    }
    void start_the_feeds() {
        anchored.fill(false);
        feed_mask = (1u << kStreams) - 1u;
        next_pdu_at = axis_cycle + 64;
    }

    static constexpr uint16_t kCmdGetAudioMap = 43;
    static constexpr uint16_t kCmdAddMappings = 44;
    static constexpr uint16_t kCmdRemoveMappings = 45;
    static constexpr uint16_t kDescStreamPortIn = 0x000E;
    static constexpr long kSuccess = 0;
    static constexpr long kBadArguments = 7;
    uint16_t aecp_seq = 0x5840;

    std::vector<uint8_t> aecp_request(uint16_t cmd, uint16_t sq, const std::vector<uint8_t>& pl) {
        const size_t flen = (38 + pl.size() < 60) ? 60 : 38 + pl.size();
        std::vector<uint8_t> f(flen, 0);
        const uint8_t cmac[6] = {0x68, 0x05, 0xCA, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 6, cmac, 6);
        f[12] = 0x22; f[13] = 0xF0; f[14] = 0xFB; f[15] = 0x00;
        const uint16_t cdl = static_cast<uint16_t>(12 + pl.size());
        f[16] = static_cast<uint8_t>((cdl >> 8) & 0x7);
        f[17] = static_cast<uint8_t>(cdl);
        const uint8_t teid[8] = {0x02, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x00, 0x01};
        memcpy(f.data() + 18, teid, 8);
        const uint8_t ceid[8] = {0x68, 0x05, 0xCA, 0xFF, 0xFE, 0x95, 0xB2, 0xD1};
        memcpy(f.data() + 26, ceid, 8);
        f[34] = static_cast<uint8_t>(sq >> 8); f[35] = static_cast<uint8_t>(sq);
        f[36] = static_cast<uint8_t>((cmd >> 8) & 0x7F);
        f[37] = static_cast<uint8_t>(cmd);
        for (size_t i = 0; i < pl.size(); i++) f[38 + i] = pl[i];
        return f;
    }
    std::vector<uint8_t> aecp_xact(uint16_t cmd, const std::vector<uint8_t>& pl) {
        auto f=aecp_request(cmd,aecp_seq++,pl);
        response.clear();
        aecp_rx(&core,0,f.data(),f.size());
        for(int n=0;n<200;++n) {
            bool busy=aecp_poll(&core);
            for(auto cookie:completed) aecp_tx_complete(&core,cookie,uint32_t(axis_cycle/100000));
            completed.clear();
            if(!busy) break;
        }
        return response;
    }
    static long aecp_status(const std::vector<uint8_t>& b) {
        return b.size() > 16 ? (b[16] >> 3) & 0x1F : -1;
    }
    long map_cmd(uint16_t cmd, int port, int stream, int chan, int cluster = 0) {
        std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8), static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, 0x01, 0x00, 0x00,
            0x00, static_cast<uint8_t>(stream), 0x00, static_cast<uint8_t>(chan),
            0x00, static_cast<uint8_t>(cluster), 0x00, 0x00};
        const long st = aecp_status(aecp_xact(cmd, pl));
        return st;
    }
    std::vector<std::array<int, 3>> get_audio_map(int port, long* number_of_maps, int page = 0) {
        const std::vector<uint8_t> pl = {
            static_cast<uint8_t>(kDescStreamPortIn >> 8), static_cast<uint8_t>(kDescStreamPortIn),
            static_cast<uint8_t>(port >> 8), static_cast<uint8_t>(port),
            0x00, static_cast<uint8_t>(page), 0x00, 0x00};
        const auto r = aecp_xact(kCmdGetAudioMap, pl);
        std::vector<std::array<int, 3>> rows;
        *number_of_maps = -1;
        if (aecp_status(r) != kSuccess || r.size() < 50) return rows;
        *number_of_maps = (static_cast<long>(r[44]) << 8) | r[45];
        const unsigned n = (static_cast<unsigned>(r[46]) << 8) | r[47];
        if (r.size() < 50 + 8 * static_cast<size_t>(n)) return rows;
        for (unsigned i = 0; i < n; i++) {
            const size_t o = 50 + 8 * static_cast<size_t>(i);
            rows.push_back({(r[o] << 8) | r[o + 1], (r[o + 2] << 8) | r[o + 3],
                            (r[o + 4] << 8) | r[o + 5]});
        }
        return rows;
    }

    void bring_out_of_reset();
    void boot_the_entity();
    void init_core();
    unsigned commit_records(bool remove,uint16_t type,uint16_t index,const uint8_t* rows,const uint8_t* pick,size_t count);
    bool edit_beat(unsigned phase,unsigned record,uint64_t value);
    aecp core{};
    aecp_model entity_model{};
    std::array<aecp_descriptor,AECP_ENTITY_DESCRIPTORS> descriptors{};
    std::array<uint8_t,AECP_ENTITY_VALUE_BYTES> values{};
    std::array<aecp_event,AECP_ENTITY_DESCRIPTORS> core_events{};
    std::array<uint32_t,AECP_ENTITY_OUTPUTS> latency{};
    aecp_mapping map_rows[AECP_ENTITY_MAP_ROWS]{};
    aecp_map core_maps[AECP_ENTITY_MAPS] = AECP_ENTITY_MAPS_INIT(map_rows);
    aecp_ports ports{};
    aecp_config config{};
    std::vector<uint8_t> response;
    std::vector<uint32_t> completed;
    bool align_apply = false;
    void provision_the_listener_contexts(const char* tag);
    double phc() const { return double(dut->rootp->milan_datapath__DOT__ptp_now_w); }
    using Map = std::array<int,64>;
    Map routes{};
    struct Publication { double capture_ns; Map routes; long generation; };
    std::deque<Publication> publications;
    long generation = 0;
    long event_cycle = -10000;
    double event_ns = 0;
    long copy_generation = -1;
    Map copy_routes{};
    long walk_cycle = 0;
    long walks = 0;
    long pair_count = 0;
    long max_walk_cycles = 0;
    long words = 0, nonzero = 0, silent = 0;
    long commands = 0, copy_edits = 0;
    bool grade = false;
    std::array<uint32_t,64> expected{};
    std::array<std::deque<uint32_t>,kStreams> pending_wire;
    std::vector<uint8_t> tx;
    long packets = 0;
    int pending_key = -1, pending_value = 0;
    bool pending_change = false;
    int last_commit_phase = -1;
    bool clipped = false;
    bool active_eligible = false;
    long first_eligible = 0;
    long awaiting_first = 0;

    void changed() {
        ++generation;
        publications.clear();
        expected.fill(0);
        active_eligible = false;
        awaiting_first = generation;
    }
    void factory() {
        routes.fill(-1);
        for (int d=0;d<kDestinations;++d) routes[kFirst+d] = d;
        for (int c=0;c<kFirst;++c) routes[c]=c;
    }
    void observe_audio();
    void grade_wire();
    void edit(uint16_t command,int dest,int stream,int channel,long status=0);
    void pages(bool firmware=true);
    uint64_t parent_map(int port,int page,int sel,int record=0);
    void output_buffered(bool firmware);
    void windows(int pdus) { run_pdus(pdus); }
    void clip_at_boot();
};

void Harness::bring_out_of_reset() {
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->m_axis_mac_tx_tready = 1;
    dut->i_mac_speed = 0b10; dut->i_link_up = 1; dut->i_full_duplex = 1;
    steps(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    steps(256);
    axi_write(0x108, 0x0); axi_write(0x10C, 0x0);
}

void Harness::provision_the_listener_contexts(const char* tag) {
    constexpr uint16_t kStrmSel = 0x800;
    constexpr uint16_t kSwCtrl = 0x810;
    constexpr uint16_t kSwFmtLo = 0x824;
    constexpr uint16_t kSwFmtHi = 0x828;
    const uint32_t lo_word = static_cast<uint32_t>(kCfgListenerFormat);
    const uint32_t hi_word = static_cast<uint32_t>(kCfgListenerFormat >> 32);
    long read_back = 0;
    for (int s = 1; s < kStreams; s++) {
        axi_write(kStrmSel, static_cast<uint32_t>(s));
        axi_write(kSwFmtLo, lo_word);
        axi_write(kSwFmtHi, hi_word);
        axi_write(kSwCtrl, 0x1);
        if (axi_read(kSwFmtHi) == hi_word) ++read_back;
    }
    char what[160];
    std::snprintf(what, sizeof what, "%s: streams 1-7's listener format reads back out of the LCTX", tag);
    check.dec(what, static_cast<uint64_t>(read_back), kStreams - 1);
}


void Harness::observe_audio() {
    if (!dut->axis_resetn) return;
    auto* r=dut->rootp;
    if (r->milan_datapath__DOT__dom_ev_p_w) {
        event_cycle=axis_cycle;
        event_ns=double(r->milan_datapath__DOT__dom_ns_w);
    }
    // Command intent supplies the map; the writer's commit supplies timing.
    // The queue's map and invalidate inputs are never expected values.
    if (r->milan_datapath__DOT__amap_edit_live_wr_p &&
        r->milan_datapath__DOT__amap_edit_in_change_w) {
        check.that("EDIT_INTENT_PRESENT", pending_key>=0);
        if (pending_key>=0) routes[pending_key]=pending_value;
        pending_change=true;
        last_commit_phase=int(axis_cycle-event_cycle);
        changed();
    }
    const long copy_start=event_cycle+1+4*kStreams;
    const long copy_end=copy_start+kDestinations+1;
    if (axis_cycle==copy_start) {
        copy_routes=routes;
        copy_generation=generation;
    }
    if (axis_cycle==copy_end && copy_generation==generation) {
        publications.push_back({event_ns+(kLead+1)*62500.0/3,copy_routes,generation});
        while (publications.size()>4) publications.pop_front();
    }
    if (r->milan_datapath__DOT__input_loop_capture_w) {
        expected.fill(0);
        active_eligible=false;
        const uint32_t when=r->milan_datapath__DOT__cmap_walk_ns_w;
        for (const auto& pub:publications) {
            if (pub.generation!=generation ||
                std::abs(int32_t(when-uint32_t(std::llround(pub.capture_ns))))>150) continue;
            active_eligible=true;
            for (int d=0;d<kDestinations;++d) {
                int source=pub.routes[kFirst+d];
                if (source<0) continue;
                int stream=source/8, channel=source%8;
                const double presentation=pub.capture_ns-62500.0/3;
                const long ord=std::lround((presentation-anchor_ns[stream])/ps_phc)+anchor_ord[stream];
                if (anchored[stream] && ord>=0 && ord<injected[stream] &&
                    std::abs(pt_of(stream,ord)-presentation)<ps_phc/2)
                    expected[d]=sample_word(stream,channel,ord);
            }
        }
        pair_count=0;
        walk_cycle=axis_cycle;
        ++walks;
        if (active_eligible && awaiting_first) { ++first_eligible; awaiting_first=0; }
    }
    if (grade && r->milan_datapath__DOT__cmap_pv_w) {
        int slot=r->milan_datapath__DOT__cmap_slot_w;
        check.dec("FULL_SLOT_ORDER",slot,pair_count++);
        for (int half=0;half<2;++half) {
            int channel=2*slot+half;
            uint32_t got=half ? r->milan_datapath__DOT__cmap_r_w : r->milan_datapath__DOT__cmap_l_w;
            uint32_t want=expected[channel];
            check.hex("PARENT_SAMPLE",got,want);
            pending_wire[channel/8].push_back(want);
            ++words;
            if (want) ++nonzero; else ++silent;
        }
        if (slot==4*kStreams-1) {
            long elapsed=axis_cycle-walk_cycle;
            max_walk_cycles=std::max(max_walk_cycles,elapsed);
            check.that("FULL_WALK_DEADLINE",elapsed<2083);
        }
    }
    grade_wire();
}
void Harness::grade_wire() {
    if (!grade || !dut->m_axis_mac_tx_tvalid || !dut->m_axis_mac_tx_tready) return;
    for (int b=0;b<8;++b) if ((dut->m_axis_mac_tx_tkeep>>b)&1)
        tx.push_back(uint8_t(dut->m_axis_mac_tx_tdata>>(8*b)));
    if (!dut->m_axis_mac_tx_tlast) return;
    int h=(tx.size()>16 && tx[12]==0x81) ? 18 : 14;
    if (tx.size()>size_t(h+24) && tx[h]==2) {
        int stream=tx[h+11];
        check.that("WIRE_STREAM",stream<kStreams);
        check.dec("WIRE_LENGTH",tx.size(),h+24+kPayloadBytes);
        if (stream<kStreams && tx.size()==size_t(h+24+kPayloadBytes)) {
            auto& q=pending_wire[stream];
            check.that("WIRE_CAPTURE_COVERAGE",q.size()>=48);
            if (q.size()>=48) for(int n=0;n<48;++n) {
                int o=h+24+4*n;
                uint32_t got=(uint32_t(tx[o])<<16)|(uint32_t(tx[o+1])<<8)|tx[o+2];
                check.hex("PARENT_WIRE_SAMPLE",got,q.front()); q.pop_front();
                check.dec("WIRE_PAD",tx[o+3],0);
            }
        }
        ++packets;
    }
    tx.clear();
}
void Harness::edit(uint16_t command,int dest,int stream,int channel,long status) {
    int key=kFirst+dest,port=0,cluster=key;
    for(int p=0;p<kStreams;++p)
        if(key>=kInputBase[p] && key<kInputBase[p]+kInputWidth[p]) {
            port=p; cluster=key-kInputBase[p]; break;
        }
    pending_key=key;
    pending_value=command==kCmdRemoveMappings ? -1 : 8*stream+channel;
    pending_change=false;
    long result=map_cmd(command,port,stream,channel,cluster);
    check.dec("AECP_EDIT_STATUS",result,status);
    if(result==0 && status==0 && routes[key]!=pending_value)
        check.that("ACCEPTED_EDIT_COMMITTED",false);
    if(status!=0) check.that("REJECTED_EDIT_NO_COMMIT",!pending_change);
    pending_key=-1;
    ++commands;
}
uint64_t Harness::parent_map(int port,int page,int sel,int record) {
    dut->i_ctl_amap_type=14; dut->i_ctl_amap_index=port;
    dut->i_ctl_amap_map_index=page; dut->i_ctl_amap_sel=sel;
    dut->i_ctl_amap_rec=record; dut->i_ctl_amap_req=1;
    steps(2);
    int waited=0;
    while(dut->o_ctl_amap_wait && waited++<4096) step();
    check.that("PARENT_MAP_RESPONSE",!dut->o_ctl_amap_wait);
    uint64_t result=dut->o_ctl_amap_data;
    dut->i_ctl_amap_req=0; step();
    return result;
}
void Harness::pages(bool firmware) {
    for(int port=0;port<kStreams;++port) {
        int pages=(kInputWidth[port]+7)/8;
        for(int page=0;page<pages;++page) {
            long count=-1;
            std::vector<std::array<int,3>> got;
            if(firmware) got=get_audio_map(port,&count,page);
            std::vector<std::array<int,3>> want;
            for(int c=8*page;c<std::min(kInputWidth[port],8*page+8);++c) {
                int source=routes[kInputBase[port]+c];
                if(source>=0) want.push_back({source/8,source%8,c});
            }
            std::sort(want.begin(),want.end());
            if(firmware) {
                std::sort(got.begin(),got.end());
                check.dec("GET_AUDIO_MAP_NUMBER_OF_MAPS",count,pages);
                check.that("GET_AUDIO_MAP_FIXED_PAGE_ROWS",got==want);
            }
            uint64_t metadata=parent_map(port,page,1);
            check.dec("PARENT_MAP_PAGES",metadata>>16,pages);
            check.dec("PARENT_MAP_COUNT",metadata&65535,want.size());
            std::vector<std::array<int,3>> actual;
            for(unsigned row=0;row<(metadata&65535) && row<8;++row) {
                uint64_t value=parent_map(port,page,2,row);
                actual.push_back({int(value>>48),int((value>>32)&65535),int((value>>16)&65535)});
                check.dec("PARENT_MAP_CLUSTER_CHANNEL",value&65535,0);
            }
            std::sort(actual.begin(),actual.end());
            check.that("PARENT_MAP_FIXED_PAGE_ROWS",actual==want);
        }
    }
}
void Harness::clip_at_boot() {
    // Hold the restore open while its input format clips the factory image.
    grade=false; feed_mask=0;
    dut->axis_resetn=0; dut->gtx_resetn=0; steps(32);
    dut->i_ctl_restore=1;
    dut->i_ctl_pub_bound=0; dut->i_ctl_pub_started=0; dut->i_ctl_pub_sid_valid=0;
    dut->axis_resetn=1; dut->gtx_resetn=1;
    const uint64_t format=(kCfgListenerFormat & ~(uint64_t(1023)<<22)) | (uint64_t(4)<<22);
    dut->i_ctl_fmt_in[0]=uint32_t(format); dut->i_ctl_fmt_in[1]=uint32_t(format>>32);
    dut->i_ctl_fmt_in_v=1;
    steps(200);
    factory();
    for(auto& source:routes) if(source>=4 && source<8) source=-1;
    changed(); publications.clear();
    dut->i_ctl_restore=2; steps(200);
    pages(false);
    // Formats can widen after boot; removed mappings must stay absent.
    boot_the_entity(); provision_the_listener_contexts("CLIP");
    output_buffered(false);
    for(auto& queue:pending_wire) queue.clear();
    tx.clear(); publications.clear(); expected.fill(0);
    while(!dut->rootp->milan_datapath__DOT__input_loop_capture_w) step();
    grade=true; axi_write(0x654,0x00020003);
    check.dec("AAF_ENABLED_AFTER_CLIP",axi_read(0x654)&3,3);
    long before_packets=packets;
    start_the_feeds(); windows(24);
    check.that("CLIPPED_WIRE_TRANSMITS",packets>before_packets+10*kStreams);
    pages(false);
    clipped=true;
}
void Harness::output_buffered(bool firmware) {
    if(kStreams!=1) return;
    for(int c=0;c<8;++c) for(int remove=1;remove>=0;--remove) {
        std::vector<uint8_t> pl={0,15,0,0,0,1,0,0,0,0,0,uint8_t(c),0,uint8_t(remove?c:8+c),0,0};
        unsigned status=firmware ? aecp_status(aecp_xact(remove?kCmdRemoveMappings:kCmdAddMappings,pl))
                                 : commit_records(remove,15,0,pl.data()+8,nullptr,1);
        check.dec("OUTPUT_BUFFERED_SOURCE",status,0);
    }
}

void Harness::init_core() {
    check.that("GENERATED_ENTITY_IMAGE",aecp_image_load(&entity_model,aecp_entity_image,
        sizeof aecp_entity_image,AECP_ENTITY_CRC,descriptors.data(),descriptors.size(),values.data(),values.size()));
    ports.ctx=this;
    ports.send=[](void* p,unsigned,const uint8_t* b,size_t n,uint32_t cookie) {
        auto* h=static_cast<Harness*>(p);
        h->response.assign(b,b+n); h->completed.push_back(cookie); return true;
    };
    ports.now_ms=[](void* p) { return uint32_t(static_cast<Harness*>(p)->axis_cycle/100000); };
    ports.random=[](void*) { return uint32_t(12345); };
    ports.timer=[](void*,bool,uint32_t) {};
    ports.applied=[](void*) { return true; };
    ports.changed=[](void*,aecp_change,uint16_t,uint16_t) {};
    ports.available_index=[](void*,unsigned) { return uint32_t(0); };
    ports.edit=[](void* p,bool rm,uint16_t t,uint16_t i,const uint8_t* rows,const uint8_t* pick,size_t n) {
        return static_cast<Harness*>(p)->commit_records(rm,t,i,rows,pick,n);
    };
    ports.stream=[](void*,unsigned,uint16_t,uint16_t,aecp_stream_info* info) {
        info->bound=false; info->running=false; return true;
    };
    config.entity_id=0x020000fffe000001ull;
    config.mac[0]=0; config.interfaces=1; config.model=&entity_model;
    config.maps=core_maps; config.map_count=AECP_ENTITY_MAPS;
    config.events=core_events.data(); config.latency=latency.data();
    check.that("AECP_CORE_INIT",aecp_init(&core,&config,&ports));
    aecp_open(&core);
}
bool Harness::edit_beat(unsigned phase,unsigned record,uint64_t value) {
    dut->i_ctl_edit_phase=phase; dut->i_ctl_edit_rec=record; dut->i_ctl_edit_record=value;
    lo(); hi();
    dut->i_ctl_edit_req=1;
    bool accepted=false,answered=false;
    for(int n=0;n<4096;++n) {
        lo(); bool ready=!dut->o_ctl_edit_wait; uint64_t answer=dut->o_ctl_edit_data; hi();
        if(ready) { accepted=(answer&1)!=0; answered=true; break; }
    }
    check.that("EDIT_FACE_ANSWERED",answered);
    dut->i_ctl_edit_req=0; lo(); hi();
    return accepted;
}
unsigned Harness::commit_records(bool remove,uint16_t type,uint16_t index,
                                 const uint8_t* rows,const uint8_t* pick,size_t count) {
    dut->i_ctl_edit_remove=remove; dut->i_ctl_edit_type=type;
    dut->i_ctl_edit_index=index; dut->i_ctl_edit_count=count;
    auto value=[&](size_t n) { uint64_t v=0;const uint8_t* b=rows+8*(pick?pick[n]:n);
        for(int k=0;k<8;++k) v=(v<<8)|b[k];
        return v; };
    unsigned status=edit_beat(0,0,0)?0:11;
    for(size_t n=0;!status && n<count;++n) if(!edit_beat(4,n,value(n))) status=7;
    if(!status && !edit_beat(1,0,0)) status=7;
    if(status) { edit_beat(3,0,0); return status; }
    if(align_apply) {
        while(axis_cycle-event_cycle!=4*kStreams+6) step();
        ++copy_edits; align_apply=false;
    }
    for(size_t n=0;n<count;++n) check.that("COMMIT_RESERVED",edit_beat(5,n,value(n)));
    edit_beat(2,0,0);
    return 0;
}
void Harness::boot_the_entity() {
    dut->i_ctl_restore=2;
    dut->i_ctl_clk_src_index=0;
    for(int s=0;s<kStreams;++s) {
        uint64_t sid=0; for(auto b:sid_of(s)) sid=(sid<<8)|b;
        dut->i_ctl_pub_sid[2*s]=uint32_t(sid);dut->i_ctl_pub_sid[2*s+1]=uint32_t(sid>>32);
        dut->i_ctl_pub_src_sid[2*s]=unsigned(s);dut->i_ctl_pub_src_sid[2*s+1]=0x02000001;
        dut->i_ctl_fmt_in[2*s]=uint32_t(kCfgListenerFormat);
        dut->i_ctl_fmt_in[2*s+1]=uint32_t(kCfgListenerFormat>>32);
    }
    dut->i_ctl_pub_bound=(1<<kStreams)-1; dut->i_ctl_pub_sid_valid=(1<<kStreams)-1;
    dut->i_ctl_pub_started=(1<<kStreams)-1; dut->i_ctl_fmt_in_v=(1<<kStreams)-1;
    dut->i_ctl_pub_da_gate=(1<<kStreams)-1; dut->i_ctl_pub_licence=(1<<kStreams)-1;
    steps(1000);
    axi_write(0x900,1);
    axi_write(0x108,0); axi_write(0x10c,0);
    axi_write(0x6cc,0);
}
int Harness::run() {
    const milan::tb::Model<Vmilan_datapath> model;
    dut=model.get(); factory();
    bring_out_of_reset(); boot_the_entity(); provision_the_listener_contexts("BOOT"); init_core();
    pages();
    // Select the declared buffered sources through the output-map server.
    output_buffered(true);
    start_the_feeds(); windows(12);
    // Start packet capture from a complete walk with the packetizer disabled.
    while(!dut->rootp->milan_datapath__DOT__input_loop_capture_w) step();
    grade=true;
    axi_write(0x654,0x00020003);
    windows(12);
    edit(kCmdRemoveMappings,0,0,0);
    edit(kCmdAddMappings,0,kStreams-1,7); windows(8); pages();
    edit(kCmdAddMappings,0,kStreams-1,7); // idempotent
    check.that("NOOP_NO_INVALIDATION",!pending_change); windows(4);
    edit(kCmdAddMappings,0,kStreams,0,kBadArguments); windows(4);
    edit(kCmdRemoveMappings,0,kStreams-1,7); windows(8); pages();
    align_apply=true; edit(kCmdAddMappings,0,0,6); windows(8); pages();
    // Fan-out and a nonzero page are exercised with received samples.
    edit(kCmdRemoveMappings,kDestinations-1,(kDestinations-1)/8,(kDestinations-1)%8);
    edit(kCmdAddMappings,kDestinations-1,0,6); windows(8); pages();
    windows(12);
    clip_at_boot();
    check.that("ALL_DESTINATIONS_CONCURRENT",words>8*kStreams*100 && nonzero>kDestinations*100);
    check.that("INVALIDATION_SILENCE",silent>0);
    check.that("FIRST_ELIGIBLE_SAMPLE_GRADED",first_eligible>=4);
    check.that("EDIT_DURING_COPY",copy_edits==1);
    check.that("BOOT_CLIPPING_WRITER",clipped);
    check.that("ALL_TALKERS_TRANSMIT",packets>20*kStreams);
    std::printf("parent loopback streams=%d words=%ld nonzero=%ld silence=%ld packets=%ld walks=%ld max_walk_cycles=%ld first_eligible=%ld\n",
                kStreams,words,nonzero,silent,packets,walks,max_walk_cycles,first_eligible);
    return check.report();
}
}
int main(int argc,char** argv) {
    Verilated::commandArgs(argc,argv);
    Verilated::threadContextp()->threads(1);
    Harness bench;
    return bench.run();
}

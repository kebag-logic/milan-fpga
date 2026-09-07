// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Issue #367 physical-rate integration, boundary: milan_datapath AXI-Lite
// and MAC packet interfaces. Model: 50 MHz axis/gtx aliases, 20 ns nominal
// PHC, audio/tdm = 782/1591 of axis, 200 MHz i_ps_clk. Audio edges quantize
// upward to the 10 ns half-cycle grid, phase accumulator starts at zero;
// auxiliary edges use 2.5 ns resolution. Resets assert together, clocks run
// for 64 axis cycles, and both resets release at the next axis falling edge.
// The reset arm repeats this with live traffic and discards in-flight frames.
//
// Peer: an independent 125 MHz timestamp clock, 10 us epoch offset, no
// oscillator drift. Its t2/t3 are quantized physical arrival/departure times.
// Symmetric 320 ns propagation and 20 us residence are event delays, never
// solved from a desired DUT publication. No internal DUT state is written.
// Sync is two-step at 125 ms, Announce at 1 s, Pdelay follows the DUT timer.
// RX uses an 80 ns beat period (800 Mb/s upper envelope), exact keep/last,
// reserves complete packet windows around scheduled PTP ingress, and holds
// stalled beats. TX is collected only on valid/ready, including stall arms.
//
// Audio: eight channel-distinct monotonic PCM32 ramps at 48 kHz, six samples
// per AAF PDU, through RX depacketization and all four backed loopback pairs
// to eight-channel TX. The CSR stream override, capture-map debug window and
// AAF_CTRL bypass are diagnostic provisioning, NOT licensed streaming.
// TDM master clocks and capture counts are measured; serial TDM input is
// digital silence. No physical render exists in this configuration.
//
// Omitted: LiteEth/PHY, preamble/FCS, MAC buffers and their timestamp error
// (#360), CPU/DDR, ACMP/SRP admission, NVM persistence,
// analog audio, pad delays, PLL lock/jitter/metastability, oscillator drift,
// MMCM DRP/phase actuation, CRF recovery, multiple peers/cease and compliance.
// Response memory is an ordered 592-byte store for GET_AVB_INFO/GET_AS_PATH;
// descriptor reads use the builder-generated AEM image with 12-cycle latency;
// NVM ports remain idle. MMCM is locked, acknowledgments idle,
// INTERNAL media source retained. Ethernet liveness toggles are synthetic.
// All protocol deadlines are simulated cycles. --negative-control corrupts
// peer residence timestamps and one received audio channel, off by default.

#include "../../common/verilator_harness.hpp"
#include "Vmilan_datapath.h"
#include <verilated.h>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <deque>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr uint64_t kHz = 50000000;
constexpr uint64_t kPeer = 0x0080E1FFFE112233ULL;
constexpr uint64_t kGm = 0x00AACCFFFE010203ULL;
constexpr uint64_t kSid = 0x0200000000020000ULL;
constexpr uint64_t kPropagation = 320;
constexpr uint64_t kResidence = 20000;
constexpr uint64_t kAafPeriod = 6250;
constexpr unsigned kGuard = 2048;

struct Frame {
    std::vector<uint8_t> b;
    void u8(uint8_t v) { b.push_back(v); }
    void u16(uint16_t v) { u8(v >> 8); u8(v); }
    void u32(uint32_t v) { u16(v >> 16); u16(v); }
    void u48(uint64_t v) { u16(v >> 32); u32(v); }
    void u64(uint64_t v) { u32(v >> 32); u32(v); }
    void ts(uint64_t ns) { u48(ns / 1000000000); u32(ns % 1000000000); }
};

uint64_t be(const std::vector<uint8_t>& b, size_t off, size_t n) {
    if (off + n > b.size()) return UINT64_MAX;
    uint64_t v = 0;
    for (size_t i = 0; i < n; ++i) v = (v << 8) | b[off + i];
    return v;
}

// The peer clock has its own epoch and edge quantization. It never reads PHC.
uint64_t peer_clock(uint64_t ns) { return (ns / 8) * 8 + 10000; }

Frame ptp(uint8_t type, uint16_t seq, uint16_t flags, uint16_t body) {
    Frame f;
    f.u48(0x0180C200000EULL); f.u48(0x0080E1112233ULL); f.u16(0x88F7);
    f.u8(0x10 | type); f.u8(2); f.u16(34 + body);
    f.u16(0); f.u16(flags); f.u64(0); f.u32(0);
    f.u64(kPeer); f.u16(1); f.u16(seq); f.u8(5);
    f.u8(type == 0 || type == 8 ? 0xFD : (type == 0xB ? 0 : 0x7F));
    return f;
}

Frame announce(uint16_t seq) {
    Frame f = ptp(0xB, seq, 8, 50);
    f.ts(0); f.u16(0xFFC4); f.u8(0);
    f.u8(100); f.u32(0xF8FE436A); f.u8(248); f.u64(kGm);
    f.u16(1); f.u8(0xA0); f.u16(8); f.u16(16);
    f.u64(kGm); f.u64(kPeer);
    return f;
}

Frame follow_up(uint16_t seq, uint64_t origin) {
    Frame f = ptp(8, seq, 8, 42);
    f.ts(origin); f.u16(3); f.u16(28);
    f.u48(0x0080C2000001ULL); f.u32(0); f.u16(0);
    f.u64(0); f.u32(0); f.u32(0);
    return f;
}

uint32_t sample(uint32_t index, unsigned channel) {
    // 20 bits of index fit this bounded run; channel tags occupy bits 23:20.
    return ((channel + 1) << 20) | (index & 0xFFFFF);
}

enum class TrafficControl { Normal, NoTx, StopTx };

class Harness {
 public:
    Harness(bool negative, bool extended, TrafficControl traffic_control)
        : negative_(negative), extended_(extended), traffic_control_(traffic_control) {
        check.echo_passes();
    }
    int run();

 private:
    milan::tb::Model<Vmilan_datapath> model;
    Vmilan_datapath* dut = model.get();
    milan::tb::Checker check{"ax1x1gptp physical"};
    bool negative_;
    bool extended_;
    TrafficControl traffic_control_;
    uint64_t cyc = 0;
    uint64_t audio_edges = 0;
    uint64_t ps_edges = 0;
    unsigned audio_acc = 0;
    unsigned audio_level = 0;
    unsigned fs_prev = 0;
    uint64_t fs_edges = 0;
    uint64_t first_fs = 0;
    uint64_t last_fs = 0;
    bool peer_on = false;
    bool audio_on = false;
    bool stall_on = false;
    uint64_t next_sync = 0;
    uint64_t next_announce = 0;
    uint64_t next_audio = 0;
    uint16_t sync_seq = 0;
    uint16_t announce_seq = 0;
    uint32_t audio_index = 1;
    uint8_t audio_seq = 0;
    uint64_t rx_audio = 0;
    uint64_t tx_audio = 0;
    uint64_t payload_bad = 0;
    uint64_t order_bad = 0;
    uint64_t sequence_bad = 0;
    uint64_t payload_comparisons = 0;
    uint64_t order_comparisons = 0;
    uint64_t sequence_comparisons = 0;
    uint64_t good_samples = 0;
    bool payload_started = false;
    uint32_t last_sample = 0;
    bool seq_started = false;
    uint8_t last_seq = 0;
    uint64_t audio_warm_until = 0;
    uint64_t certain_frames = 0;
    uint64_t uncertain_frames = 0;
    int require_tu = -1;
    uint64_t tu_bad = 0;
    uint64_t tu_comparisons = 0;
    uint64_t pd_requests = 0;
    uint64_t pd_answers = 0;
    uint64_t pd_first = 0;
    uint64_t pd_last = 0;
    uint64_t pd_cadence_bad = 0;
    uint64_t schedule_bad = 0;
    uint64_t stamp_origin = 0;
    int64_t oracle_delay = 0;
    std::vector<uint8_t> tx_cur;
    uint64_t tx_sof = 0;
    bool stalled = false;
    uint64_t held_data = 0;
    uint8_t held_keep = 0;
    bool held_last = false;
    uint64_t stall_beats = 0;
    uint64_t stall_bad = 0;
    uint64_t stall_until = 0;
    bool frame_stall_armed = false;
    bool frame_was_stalled = false;
    uint64_t stalled_ptp_frames = 0;
    std::array<bool, 8> completed{};
    std::deque<std::vector<uint8_t>> replies;

    struct Event {
        uint64_t at = 0;
        Frame frame;
        bool pdelay = false;
        uint64_t t1 = 0;
        uint64_t t2 = 0;
        uint64_t t3 = 0;
    };
    std::deque<Event> events;
    Event rx;
    bool rx_busy = false;
    size_t rx_off = 0;
    uint64_t rx_next = 0;
    uint64_t rx_deadline = 0;

    // Ordered response-memory face, no CPU or DDR timing claim.
    std::array<uint8_t, 592> memory{};
    bool mem_busy = false;
    uint32_t mem_addr = 0;
    unsigned mem_left = 0;
    bool mem_done = false;
    std::vector<uint8_t> descriptor;
    bool desc_busy = false;
    uint32_t desc_addr = 0;
    unsigned desc_left = 0;
    unsigned desc_wait = 0;

    struct Fires {
        bool aw = false;
        bool w = false;
        bool b = false;
        bool ar = false;
        bool r = false;
        uint32_t data = 0;
    };

    void queue(Event ev) {
        const auto pos = std::upper_bound(events.begin(), events.end(), ev.at,
            [](uint64_t at, const Event& e) { return at < e.at; });
        events.insert(pos, std::move(ev));
    }
    void run_cycles(uint64_t n) { while (n--) tick(); }
    void write(uint16_t addr, uint32_t value);
    uint32_t read(uint16_t addr);
    uint64_t read_identity(uint16_t low_addr);
    Fires tick();
    void clocks(unsigned quarter);
    void memory_drive();
    void memory_edge();
    void descriptor_drive();
    void descriptor_edge();
    void schedule();
    void receive_drive();
    void receive_edge();
    void transmit_edge();
    void complete_tx();
    void answer_pdelay(const std::vector<uint8_t>& request);
    Frame audio_frame();
    void grade_audio(const std::vector<uint8_t>& f);
    void reset();
    void configure();
    void geometry_and_clocks();
    void publication(const char* arm, bool healthy);
    std::vector<uint8_t> query(uint16_t command, uint16_t seq);
    void wire_publication();
    enum class Until { Deadline, Healthy, SyncLost, PeerLost, StalledPtp };
    void audio_window(const char* arm, uint64_t n, int tu, Until until = Until::Deadline);
    void loss_recovery();
    int report();
};

void Harness::clocks(unsigned quarter) {
    dut->i_ps_clk = quarter & 1;
    if (quarter & 1) ++ps_edges;
    if (quarter == 0 || quarter == 4) {
        audio_acc += 782;
        if (audio_acc >= 1591) {
            audio_acc -= 1591;
            audio_level ^= 1;
            if (audio_level) ++audio_edges;
        }
        dut->clk_audio_i = audio_level;
        dut->clk_tdm_i = audio_level;
        dut->axis_clk = quarter == 4;
        dut->gtx_clk = quarter == 4;
    }
    dut->eval();
    if (dut->tdm_fsync_o && !fs_prev) {
        if (!fs_edges) first_fs = cyc;
        last_fs = cyc;
        ++fs_edges;
    }
    fs_prev = dut->tdm_fsync_o;
}

void Harness::memory_drive() {
    uint64_t data = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = mem_addr - 0x20100000u + i;
        data = (data << 8) | (off < memory.size() ? memory[off] : 0);
    }
    dut->i_resp_mem_req_ready = !mem_busy;
    dut->i_resp_mem_rsp_valid = mem_busy;
    dut->i_resp_mem_rsp_data = data;
    dut->i_resp_mem_rsp_last = mem_busy && mem_left == 1;
    dut->i_resp_mem_rsp_err = 0;
    dut->i_resp_mem_wr_ready = !mem_done;
    dut->i_resp_mem_wr_done = mem_done;
    dut->i_resp_mem_wr_err = 0;
}

void Harness::memory_edge() {
    if (mem_busy && dut->o_resp_mem_rsp_ready) {
        mem_addr += 8;
        if (--mem_left == 0) mem_busy = false;
    } else if (!mem_busy && dut->o_resp_mem_req_valid) {
        mem_addr = dut->o_resp_mem_req_addr;
        mem_left = dut->o_resp_mem_req_beats;
        mem_busy = mem_left != 0;
    }
    if (mem_done) mem_done = false;
    else if (dut->o_resp_mem_wr_valid) {
        for (unsigned i = 0; i < 8; ++i) {
            const uint32_t off = dut->o_resp_mem_wr_addr - 0x20100000u + i;
            if (off < memory.size() && (dut->o_resp_mem_wr_strb & (1u << i)))
                memory[off] = dut->o_resp_mem_wr_data >> (56 - 8 * i);
        }
        mem_done = true;
    }
}

void Harness::descriptor_drive() {
    uint64_t data = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = desc_addr - 0x20000000u + i;
        data = (data << 8) | (off < descriptor.size() ? descriptor[off] : 0);
    }
    dut->i_desc_mem_req_ready = !desc_busy;
    dut->i_desc_mem_rsp_valid = desc_busy && desc_wait == 0;
    dut->i_desc_mem_rsp_data = data;
    dut->i_desc_mem_rsp_last = desc_busy && desc_left == 1;
    dut->i_desc_mem_rsp_err = 0;
}

void Harness::descriptor_edge() {
    if (!desc_busy && dut->o_desc_mem_req_valid) {
        desc_addr = dut->o_desc_mem_req_addr;
        desc_left = dut->o_desc_mem_req_beats;
        desc_busy = desc_left != 0;
        desc_wait = 12;
    } else if (desc_busy && desc_wait) --desc_wait;
    else if (desc_busy && dut->o_desc_mem_rsp_ready) {
        desc_addr += 8;
        if (--desc_left == 0) desc_busy = false;
    }
}

Harness::Fires Harness::tick() {
    if (dut->axis_resetn) schedule();
    receive_drive();
    memory_drive(); descriptor_drive();
    // Synthetic observed Ethernet clock toggles; no PHY implementation.
    dut->i_ethrx_tgl = cyc & 1;
    dut->i_ethtx_tgl = cyc & 1;
    if (stall_on && dut->m_axis_mac_tx_tvalid && !frame_stall_armed) {
        frame_stall_armed = true;
        stall_until = cyc + 64; // every frame sees 1.28 us of backpressure
    }
    dut->m_axis_mac_tx_tready = !(stall_on && cyc < stall_until);
    for (unsigned q = 0; q < 4; ++q) clocks(q);
    Fires fire;
    fire.aw = dut->s_axi_awvalid && dut->s_axi_awready;
    fire.w = dut->s_axi_wvalid && dut->s_axi_wready;
    fire.b = dut->s_axi_bready && dut->s_axi_bvalid;
    fire.ar = dut->s_axi_arvalid && dut->s_axi_arready;
    fire.r = dut->s_axi_rready && dut->s_axi_rvalid;
    fire.data = dut->s_axi_rdata;
    if (dut->axis_resetn) {
        receive_edge(); transmit_edge(); memory_edge(); descriptor_edge();
    }
    for (unsigned q = 4; q < 8; ++q) clocks(q);
    ++cyc;
    if (cyc % (kHz / 4) == 0) printf("PROGRESS simulated_seconds=%.2f rx_aaf=%llu tx_aaf=%llu\n", double(cyc) / kHz, static_cast<unsigned long long>(rx_audio), static_cast<unsigned long long>(tx_audio));
    return fire;
}

void Harness::write(uint16_t addr, uint32_t value) {
    dut->s_axi_awaddr = addr; dut->s_axi_awvalid = 1;
    dut->s_axi_wdata = value; dut->s_axi_wstrb = 15; dut->s_axi_wvalid = 1;
    dut->s_axi_bready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        const Fires f = tick();
        if (f.aw) dut->s_axi_awvalid = 0;
        if (f.w) dut->s_axi_wvalid = 0;
        if (f.b) { dut->s_axi_bready = 0; return; }
    }
    throw std::runtime_error("AXI write response timeout");
}

uint32_t Harness::read(uint16_t addr) {
    dut->s_axi_araddr = addr; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        const Fires f = tick();
        if (f.ar) dut->s_axi_arvalid = 0;
        if (f.r) { dut->s_axi_rready = 0; return f.data; }
    }
    throw std::runtime_error("AXI read response timeout");
}

uint64_t Harness::read_identity(uint16_t low_addr) {
    // REGISTER_MAP: the first half opens a snapshot until its complement.
    // Consume both halves even when checking reset, without a pending read
    // that could join a later live low word to an earlier snapshot high word.
    const uint32_t low = read(low_addr);
    const uint32_t high = read(low_addr + 4);
    return (uint64_t(high) << 32) | low;
}

Frame Harness::audio_frame() {
    Frame f;
    f.u48(0x91E0F0002A02ULL); f.u48(0x020000000002ULL); f.u16(0x22F0);
    f.u8(2); f.u8(0x81); f.u8(audio_seq++); f.u8(0); f.u64(kSid);
    f.u32(peer_clock(cyc * 20) + 2000000); // 2 ms presentation offset
    f.u8(2); f.u8(0x50); f.u8(8); f.u8(32); f.u16(192); f.u16(0);
    for (unsigned s = 0; s < 6; ++s) {
        for (unsigned ch = 0; ch < 8; ++ch)
            f.u32(sample(audio_index, negative_ && ch == 3 ? 2 : ch) << 8);
        ++audio_index;
    }
    return f;
}

void Harness::schedule() {
    if (peer_on && cyc >= next_announce) {
        queue({cyc + 500, announce(announce_seq++)});
        next_announce = cyc + kHz;
    }
    if (peer_on && cyc >= next_sync) {
        const uint64_t depart = (cyc + 1000) * 20 + 10 - kPropagation;
        Frame f = ptp(0, sync_seq, 0x0208, 10); f.ts(0);
        queue({cyc + 1000, f});
        queue({cyc + 1500, follow_up(sync_seq++, peer_clock(depart))});
        next_sync = cyc + kHz / 8;
    }
    if (!rx_busy && !events.empty() && events.front().at <= cyc) {
        rx = std::move(events.front()); events.pop_front();
        rx_busy = true; rx_off = 0; rx_next = cyc; rx_deadline = cyc + kGuard;
    }
    // Leave 200 cycles for a complete AAF PDU before each PTP reservation.
    if (!rx_busy && audio_on && cyc >= next_audio
            && (events.empty() || events.front().at > cyc + 200)) {
        rx = {cyc, audio_frame()}; rx_busy = true; rx_off = 0;
        rx_next = cyc; rx_deadline = cyc + kGuard;
        next_audio += kAafPeriod;
    }
}

void Harness::receive_drive() {
    dut->s_axis_mac_rx_tvalid = rx_busy && cyc >= rx_next;
    dut->s_axis_mac_rx_tlast = rx_busy && rx_off + 8 >= rx.frame.b.size();
    uint64_t data = 0;
    uint8_t keep = 0;
    if (rx_busy) for (size_t i = 0; i < 8 && rx_off + i < rx.frame.b.size(); ++i) {
        data |= static_cast<uint64_t>(rx.frame.b[rx_off + i]) << (i * 8);
        keep |= 1u << i;
    }
    dut->s_axis_mac_rx_tdata = data; dut->s_axis_mac_rx_tkeep = keep;
}

void Harness::receive_edge() {
    if (!rx_busy) return;
    if (cyc > rx_deadline) throw std::runtime_error("MAC RX beat timeout");
    if (!dut->s_axis_mac_rx_tvalid || !dut->s_axis_mac_rx_tready) return;
    if (rx_off == 0 && rx.pdelay) {
        const uint64_t t4 = cyc * 20 + 10;
        // Only event times enter this oracle; publication is read afterwards.
        oracle_delay = (static_cast<int64_t>(t4 - rx.t1)
                         - static_cast<int64_t>(rx.t3 - rx.t2)) / 2;
        if (cyc != rx.at) ++schedule_bad;
        ++pd_answers;
        printf("Pdelay event seq=%llu t1=%llu t2=%llu t3=%llu t4=%llu oracle=%lld ns\n",
               static_cast<unsigned long long>(be(rx.frame.b, 44, 2)),
               static_cast<unsigned long long>(rx.t1),
               static_cast<unsigned long long>(rx.t2),
               static_cast<unsigned long long>(rx.t3),
               static_cast<unsigned long long>(t4), static_cast<long long>(oracle_delay));
    }
    rx_off += 8; rx_next = cyc + 4;
    if (rx_off >= rx.frame.b.size()) {
        if (be(rx.frame.b, 12, 2) == 0x22F0 && rx.frame.b[14] == 2) ++rx_audio;
        rx_busy = false;
    }
}

void Harness::answer_pdelay(const std::vector<uint8_t>& request) {
    if (!pd_requests) pd_first = tx_sof;
    if (pd_requests && (tx_sof - pd_last < 999900000
                       || tx_sof - pd_last > 1000100000)) ++pd_cadence_bad;
    pd_last = tx_sof; ++pd_requests;
    if (!peer_on) return;
    const uint64_t arrival = tx_sof + kPropagation;
    const uint64_t depart = arrival + kResidence;
    const uint64_t t2 = peer_clock(arrival);
    const uint64_t t3 = peer_clock(depart);
    const uint16_t seq = be(request, 44, 2);
    Frame resp = ptp(3, seq, 0x0200, 20); resp.ts(t2);
    Frame fu = ptp(0xA, seq, 0, 20); fu.ts(t3 + (negative_ ? 2000 : 0));
    for (size_t i = 34; i < 44; ++i) { resp.u8(request[i]); fu.u8(request[i]); }
    const uint64_t at = (depart + kPropagation - 10) / 20;
    queue({at, resp, true, tx_sof, t2, t3});
    queue({at + 200, fu});
}

void Harness::transmit_edge() {
    if (stalled && (!dut->m_axis_mac_tx_tvalid || held_data != dut->m_axis_mac_tx_tdata
            || held_keep != dut->m_axis_mac_tx_tkeep || held_last != bool(dut->m_axis_mac_tx_tlast)))
        ++stall_bad;
    stalled = dut->m_axis_mac_tx_tvalid && !dut->m_axis_mac_tx_tready;
    if (stalled) {
        ++stall_beats; frame_was_stalled = true; held_data = dut->m_axis_mac_tx_tdata;
        held_keep = dut->m_axis_mac_tx_tkeep; held_last = dut->m_axis_mac_tx_tlast;
    }
    if (!dut->m_axis_mac_tx_tvalid || !dut->m_axis_mac_tx_tready) return;
    if (tx_cur.empty()) tx_sof = cyc * 20 + 10;
    for (unsigned i = 0; i < 8; ++i)
        if (dut->m_axis_mac_tx_tkeep & (1u << i))
            tx_cur.push_back(dut->m_axis_mac_tx_tdata >> (8 * i));
    if (dut->m_axis_mac_tx_tlast) {
        complete_tx(); tx_cur.clear(); frame_stall_armed = false;
        frame_was_stalled = false;
    }
    if (tx_cur.size() > 2048) throw std::runtime_error("MAC TX missing tlast");
}

void Harness::complete_tx() {
    const auto& f = tx_cur;
    if (frame_was_stalled && be(f, 12, 2) == 0x88F7) ++stalled_ptp_frames;
    if (f.size() >= 68 && be(f, 12, 2) == 0x88F7 && (f[14] & 15) == 2)
        answer_pdelay(f);
    const size_t v = be(f, 12, 2) == 0x8100 ? 4 : 0;
    if (f.size() > 38 + v && be(f, 12 + v, 2) == 0x22F0 && f[14 + v] == 2)
        grade_audio(f);
    if (f.size() > 38 && be(f, 12, 2) == 0x22F0 && f[14] == 0xFB)
        replies.push_back(f);
}

void Harness::grade_audio(const std::vector<uint8_t>& f) {
    const size_t v = be(f, 12, 2) == 0x8100 ? 4 : 0;
    ++tx_audio;
    const bool tu = f[17 + v] & 1;
    if (tu) ++uncertain_frames; else ++certain_frames;
    if (require_tu >= 0) {
        ++tu_comparisons;
        if (tu != bool(require_tu)) ++tu_bad;
    }
    if (seq_started) {
        ++sequence_comparisons;
        if (f[16 + v] != uint8_t(last_seq + 1)) ++sequence_bad;
    }
    seq_started = true; last_seq = f[16 + v];
    if (f.size() != 230 + v || f[32 + v] != 8 || be(f, 34 + v, 2) != 192) {
        ++payload_comparisons; ++payload_bad; return;
    }
    if (cyc < audio_warm_until) return;
    for (unsigned s = 0; s < 6; ++s) {
        const size_t off = 38 + v + 32 * s;
        const uint32_t index = (be(f, off, 4) >> 8) & 0xFFFFF;
        bool channels_ok = true;
        for (unsigned ch = 0; ch < 8; ++ch) {
            ++payload_comparisons;
            if (be(f, off + 4 * ch, 4) != (uint64_t(sample(index, ch)) << 8))
                channels_ok = false;
        }
        if (!channels_ok) ++payload_bad;
        if (payload_started) {
            ++order_comparisons;
            if (index != last_sample + 1) ++order_bad;
        }
        payload_started = true; last_sample = index;
        if (channels_ok) ++good_samples;
    }
}

void Harness::reset() {
    peer_on = false; audio_on = false; stall_on = false; require_tu = -1;
    events.clear(); rx_busy = false; tx_cur.clear(); replies.clear(); stalled = false;
    frame_stall_armed = false; frame_was_stalled = false; stall_until = 0;
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0; dut->s_axi_arvalid = 0;
    dut->s_axi_bready = 0; dut->s_axi_rready = 0;
    dut->i_mac_speed = 2; dut->i_link_up = 1; dut->i_full_duplex = 1;
    dut->i_mmcm_locked = 1;
    dut->i_mmcm_ps_done = 0; dut->i_mmcm_drp_rdy = 0; dut->i_mmcm_drp_do = 0;
    dut->i2s_sdout_i = 0; dut->tdm_data_i = 0;
    dut->tdm_bclk_i = 0; dut->tdm_fsync_i = 0;
    mem_busy = false; mem_done = false; desc_busy = false; desc_wait = 0;
    run_cycles(64);
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    stamp_origin = cyc * 20;
    pd_requests = 0; pd_answers = 0;
    seq_started = false; payload_started = false;
    audio_seq = 0; audio_index = 1;
    run_cycles(512);
}

void Harness::configure() {
    write(0x108, 0x00000002); write(0x10C, 0x00000100);
    write(0x608, 0x020000FF); write(0x604, 0xFE000001);
    check.hex("PHC reset increment is 20 ns", read(0x504), 0x14000000);
    check.hex("advertised talker geometry AAF plus CRF", read(0x618), 0x48010002);
    check.hex("advertised listener geometry AAF plus CRF", read(0x61C), 0x48010002);
    write(0x778, 0x85); write(0x6E4, 777); // inert legacy health writes
    check.hex("software cannot manufacture gPTP health", read(0x77C) & 0x10003, 1);
    check.hex("software cannot manufacture peer delay", read(0x6E4), 0);
    write(0x654, 0x00020001);
    check.hex("unlicensed talker gate closed", read(0x66C) & 8, 0);
    write(0x800, 0); write(0x814, uint32_t(kSid)); write(0x818, kSid >> 32);
    write(0x824, 0x02006000); write(0x828, 0x02050220); write(0x810, 1);
    check.hex("listener override eight-channel format", read(0x824), 0x02006000);
    write(0x900, 1);
    for (unsigned ch = 0; ch < 8; ++ch) {
        write(0x904, 0x100 | ch);
        write(0x908, 0xD000 | ((ch & 1) << 8) | (ch / 2));
    }
    write(0x654, traffic_control_ == TrafficControl::NoTx ? 0x00020001 : 0x00020003);
    check.hex("diagnostic talker bypass opens gate", read(0x66C) & 8, 8);
    printf("TRAFFIC: diagnostic AAF_CTRL bypass and CSR listener/map overrides; licensed streaming NOT RUN\n");
    audio_on = true; next_audio = cyc;
    audio_warm_until = cyc + kHz / 100; // 10 ms settling, excluded from payload score
    peer_on = true; next_sync = cyc; next_announce = cyc + kHz / 4;
}

void Harness::geometry_and_clocks() {
    const uint32_t pairs0 = read(0x664);
    const uint64_t a0 = audio_edges;
    const uint64_t p0 = ps_edges;
    const uint64_t f0 = fs_edges;
    const uint64_t start = cyc;
    run_cycles(159100);
    const uint64_t delta = cyc - start;
    const int64_t audio_error = static_cast<int64_t>((audio_edges - a0) * 1591)
        - static_cast<int64_t>(delta * 782);
    check.that("audio ratio 782/1591 within one quantized edge", std::abs(audio_error) <= 1591);
    check.that("200 MHz auxiliary clock has four rising edges per Milan cycle",
               ps_edges - p0 == delta * 4);
    const uint32_t pairs = read(0x664) - pairs0;
    check.that("TDM8 master captures four pairs per frame", pairs > 500
        && std::abs(int64_t(pairs) - int64_t(4 * (fs_edges - f0))) <= 4);
    check.that("TDM8 FSYNC period follows audio divided by 512", fs_edges > 100
        && std::abs(double(last_fs - first_fs) / double(fs_edges - 1) - 512.0 * 1591 / 782) < 2);
    write(0x520, 4); run_cycles(32);
    const uint64_t phc0 = (uint64_t(read(0x534)) << 32) | read(0x530);
    const uint64_t c0 = cyc;
    run_cycles(10000); write(0x520, 4); run_cycles(32);
    const uint64_t phc1 = (uint64_t(read(0x534)) << 32) | read(0x530);
    check.dec("PHC advances 20 ns per modeled cycle before Sync selection", phc1 - phc0, (cyc - c0) * 20);
}

void Harness::publication(const char* arm, bool healthy) {
    const uint32_t gen0 = read(0x7E4);
    const uint64_t gm = read_identity(0x624);
    const uint64_t parent = read_identity(0x730);
    const uint32_t delay = read(0x6E4);
    const uint32_t stat = read(0x77C);
    const uint32_t gen1 = read(0x7E4);
    printf("PUBLIC %s at %.6f s: GM=%016llx parent=%016llx delay=%u oracle=%lld CLKV=%08x generation=%x/%x\n",
           arm, double(cyc) / kHz, static_cast<unsigned long long>(gm),
           static_cast<unsigned long long>(parent), delay, static_cast<long long>(oracle_delay), stat, gen0, gen1);
    check.hex("CSR snapshot publication generation stable", gen0, gen1);
    if (healthy) {
        check.hex("selected GM matches independent Announce", gm, kGm);
        check.hex("selected parent matches peer identity", parent, kPeer);
        check.hex("PathTrace has GM and parent", gen1 & 15, 2);
        check.hex("asCapable and Sync healthy, uncertainty cleared", stat & 0x10003, 0x10002);
        // Bound: 20 ns ingress phase plus 8 ns peer quantization. No PHY allowance.
        check.that("peer delay equals independent event oracle within 28 ns",
                   std::abs(int64_t(delay) - oracle_delay) <= 28);
    } else {
        check.hex("loss clears asCapable", stat & 0x10000, 0);
        check.hex("loss clears Sync and asserts uncertainty", stat & 3, 1);
    }
}

std::vector<uint8_t> Harness::query(uint16_t command, uint16_t seq) {
    Frame f;
    f.u48(0x020000000001ULL); f.u48(0x0080E1112233ULL); f.u16(0x22F0);
    f.u8(0xFB); f.u8(0); f.u16(16); f.u64(0x020000FFFE000001ULL);
    f.u64(kPeer); f.u16(seq); f.u16(command);
    f.u16(command == 0x27 ? 9 : 0); f.u16(0);
    while (f.b.size() < 60) f.u8(0);
    queue({cyc + 2000, f});
    const uint64_t end = cyc + 200000;
    while (cyc < end) {
        tick();
        while (!replies.empty()) {
            auto reply = std::move(replies.front()); replies.pop_front();
            if (be(reply, 34, 2) == seq && be(reply, 36, 2) == command) return reply;
        }
    }
    return {};
}

void Harness::wire_publication() {
    const uint32_t delay = read(0x6E4);
    const auto avb = query(0x27, 0x7001);
    check.dec("GET_AVB_INFO length", avb.size(), 62);
    check.dec("GET_AVB_INFO status SUCCESS", avb.size() > 16 ? avb[16] >> 3 : 255, 0);
    check.hex("GET_AVB_INFO coherent GM", be(avb, 42, 8), kGm);
    check.dec("GET_AVB_INFO delay equals CSR bank", be(avb, 50, 4), delay);
    check.that("GET_AVB_INFO asCapable agrees with CSR", avb.size() > 55 && (avb[55] & 1));
    const auto path = query(0x28, 0x7002);
    check.dec("GET_AS_PATH Ethernet minimum length", path.size(), 60);
    check.dec("GET_AS_PATH status SUCCESS", path.size() > 16 ? path[16] >> 3 : 255, 0);
    check.dec("GET_AS_PATH control data length excludes padding", be(path, 16, 2) & 0x7FF, 32);
    check.dec("GET_AS_PATH padding bytes are zero", be(path, 58, 2), 0);
    check.dec("GET_AS_PATH two ordered identities", be(path, 38, 4), 2);
    check.hex("GET_AS_PATH GM", be(path, 42, 8), kGm);
    check.hex("GET_AS_PATH parent", be(path, 50, 8), kPeer);
}

void Harness::audio_window(const char* arm, uint64_t n, int tu, Until until) {
    printf("AUDIO arm=%s deadline=%.6f s\n", arm, double(n) / kHz);
    const uint64_t start = cyc;
    const uint64_t rx0 = rx_audio;
    const uint64_t tx0 = tx_audio;
    const uint64_t bad0 = payload_bad;
    const uint64_t order0 = order_bad;
    const uint64_t seq0 = sequence_bad;
    const uint64_t good0 = good_samples;
    const uint64_t tu0 = tu_bad;
    const uint64_t order_comparisons0 = order_comparisons;
    const uint64_t sequence_comparisons0 = sequence_comparisons;
    const uint64_t tu_comparisons0 = tu_comparisons;
    require_tu = tu;
    if (extended_ || until == Until::Deadline) run_cycles(n);
    else {
        // Observe only public state, at 1 ms intervals. The deadline remains
        // the original bound; a missing transition still fails the assertions
        // below and at the caller. Ten milliseconds exceeds the unchanged
        // >50 packet / >300 sample requirements. No DUT timer is modified.
        const uint64_t end = cyc + n;
        while (cyc < end) {
            run_cycles(std::min(kHz / 1000, end - cyc));
            if (cyc - start < kHz / 100) continue;
            const uint32_t stat = read(0x77C);
            const bool reached =
                (until == Until::Healthy && (stat & 0x10003) == 0x10002
                    && pd_answers >= 2)
                || (until == Until::SyncLost && (stat & 3) == 1)
                || (until == Until::PeerLost && (stat & 0x10003) == 1
                    && pd_requests >= pd_answers + 5)
                || (until == Until::StalledPtp && stalled_ptp_frames > 0);
            if (reached) {
                // Drain the in-flight Pdelay pair and publication crossing.
                run_cycles(kHz / 1000);
                break;
            }
        }
    }
    require_tu = -1;
    printf("AUDIO elapsed=%.6f s\n", double(cyc - start) / kHz);
    printf("AUDIO result rx=%llu tx=%llu samples=%llu bad_payload=%llu bad_order=%llu\n",
        static_cast<unsigned long long>(rx_audio - rx0), static_cast<unsigned long long>(tx_audio - tx0),
        static_cast<unsigned long long>(good_samples - good0), static_cast<unsigned long long>(payload_bad - bad0),
        static_cast<unsigned long long>(order_bad - order0));
    check.that("both eight-channel packet directions active", rx_audio - rx0 > 50 && tx_audio - tx0 > 50);
    check.that("all eight channel payloads match the supplied ramp", payload_bad == bad0 && good_samples - good0 > 300);
    const auto compared = [this](const char* label, uint64_t comparisons, uint64_t errors) {
        if (comparisons) check.dec(label, errors, 0);
        else printf("NOT RUN: %s (no comparisons in this window; uncounted)\n", label);
    };
    compared("audio sample order, no duplicates or gaps", order_comparisons - order_comparisons0,
             order_bad - order0);
    compared("AAF packet sequence order", sequence_comparisons - sequence_comparisons0, sequence_bad - seq0);
    if (tu >= 0) compared("AAF uncertainty matches public stable state", tu_comparisons - tu_comparisons0,
                          tu_bad - tu0);
    else printf("NOT RUN: stable-tu comparison during transition window\n");
}

void Harness::loss_recovery() {
    peer_on = false; events.clear();
    const uint64_t loss = cyc;
    audio_window("Sync loss transition", kHz * 45 / 100, -1, Until::SyncLost);
    check.hex("375 ms Sync timeout clears sync and asserts tu", read(0x77C) & 3, 1);
    // Keep the original total loss deadline (450 ms + 4.6 s). Ending the
    // Sync arm early must not shorten the fourth missed-response interval.
    audio_window("peer loss, real fourth missed Pdelay",
                 extended_ ? kHz * 46 / 10 : loss + kHz * 505 / 100 - cyc,
                 1, Until::PeerLost);
    publication("lost", false);
    // A request is judged at the next request interval. Four unanswered
    // intervals therefore finish when the fifth unanswered request starts.
    check.that("four unanswered Pdelay intervals elapsed", pd_requests >= pd_answers + 5);
    printf("LOSS elapsed %.6f s, no timer compression\n", double(cyc - loss) / kHz);
    peer_on = true; next_sync = cyc; next_announce = cyc + kHz / 4;
    audio_window("recovery transition", kHz * 3, -1, Until::Healthy);
    publication("recovered", true);
    audio_window("recovered stable", kHz / 50, 0);
}

int Harness::report() {
    const auto cumulative = [this](const char* label, uint64_t comparisons, uint64_t errors) {
        if (comparisons) check.dec(label, errors, 0);
        else printf("NOT RUN: %s (no comparisons; uncounted)\n", label);
    };
    cumulative("all monitored audio payload errors, excluding declared warm-up", payload_comparisons, payload_bad);
    cumulative("all monitored audio sample ordering errors", order_comparisons, order_bad);
    cumulative("all monitored AAF packet sequence errors", sequence_comparisons, sequence_bad);
    printf("AUDIO comparisons payload=%llu sample_order=%llu packet_sequence=%llu\n",
           static_cast<unsigned long long>(payload_comparisons),
           static_cast<unsigned long long>(order_comparisons),
           static_cast<unsigned long long>(sequence_comparisons));
    constexpr std::array<const char*, 8> phases = {
        "geometry and clocks", "initial audio payload", "first Pdelay exchange",
        "acquisition and public coherence", "healthy audio", "backpressure",
        "loss and recovery", "reset and reacquisition"};
    for (size_t i = 0; i < phases.size(); ++i)
        if (!completed[i]) printf("NOT RUN TO COMPLETION: %s\n", phases[i]);
    printf("simulated_duration_seconds=%.9f cycles=%llu\n", double(cyc) / kHz,
           static_cast<unsigned long long>(cyc));
    printf("clock_audio_hz=%.6f clock_axis_hz=50000000 clock_ps_hz=200000000 PHC_increment_ns=20\n", double(kHz) * 782 / 1591);
    printf("NOT RUN: licensed ACMP/SRP streaming; physical TDM render; CRF recovery; multiple-responder cease; PHY/MAC calibration; CPU/DDR; physical compliance\n");
    printf("NOT RUN: warm-up payload comparisons during first 10 ms of each reset epoch\n");
    printf("exit_status=%d negative_control=%d\n", check.passed() ? 0 : 1, negative_);
    return check.report();
}

int Harness::run() {
    printf("ax1x1gptp PHYSICAL: 50 MHz, 782/1591 audio, 200 MHz auxiliary; negative_control=%d extended=%d\n", negative_, extended_);
    try {
        std::ifstream image("obj_ax1x1gptp/aemi.bin", std::ios::binary);
        if (!image) throw std::runtime_error("generated AEM image missing");
        descriptor.assign(std::istreambuf_iterator<char>(image), std::istreambuf_iterator<char>());
        if (descriptor.empty()) throw std::runtime_error("generated AEM image empty");
        reset(); configure(); geometry_and_clocks(); completed[0] = true;
        run_cycles(kHz / 100);
        audio_window("initial payload", kHz / 50, 1);
        completed[1] = true;
        if (traffic_control_ == TrafficControl::NoTx) return report();
        if (traffic_control_ == TrafficControl::StopTx) {
            // Preserve the initial comparisons, then drain admitted traffic.
            // This proves a later empty window cannot borrow earlier evidence.
            write(0x654, 0x00020001);
            run_cycles(kHz / 100);
            audio_window("admission withheld after traffic", kHz / 50, 1);
            return report();
        }
        const auto initial_avb = query(0x27, 0x7010);
        check.dec("pre-acquisition GET_AVB_INFO length", initial_avb.size(), 62);
        check.dec("pre-acquisition GET_AVB_INFO SUCCESS", initial_avb.size() > 16 ? initial_avb[16] >> 3 : 255, 0);
        check.hex("pre-acquisition GET_AVB_INFO has no selected GM", be(initial_avb, 42, 8), 0);
        run_cycles(kHz * 12 / 10);
        check.dec("first Pdelay response completed", pd_answers, 1);
        check.hex("one response cannot assert asCapable", read(0x77C) & 0x10000, 0);
        const uint32_t first_delay = read(0x6E4);
        printf("FIRST PDELAY published=%u oracle=%lld ns\n", first_delay, static_cast<long long>(oracle_delay));
        check.that("first peer delay matches independent event oracle within 28 ns",
                   std::abs(int64_t(first_delay) - oracle_delay) <= 28);
        completed[2] = true;
        if (negative_) return report();
        audio_window("acquisition", kHz * 18 / 10, -1, Until::Healthy);
        check.that("boot Pdelay occurs at 1.2 s", pd_requests >= 2
            && pd_first - stamp_origin >= 1200000000 && pd_first - stamp_origin < 1200100000);
        check.dec("Pdelay retains one-second cadence", pd_cadence_bad, 0);
        check.dec("scheduled peer ingress met its event times", schedule_bad, 0);
        publication("acquired", true);
        wire_publication(); completed[3] = true;
        if (!negative_) {
            audio_window("healthy stable", kHz / 50, 0); completed[4] = true;
            stall_on = true;
            // The next one-second DUT request is the backpressured PTP
            // witness. Acquisition now finishes before 2.3 s, so allow it
            // to reach that request at 3.2 s without changing the cadence.
            audio_window("TX backpressure", extended_ ? kHz * 3 / 10 : kHz, 0, Until::StalledPtp);
            stall_on = false;
            check.that("backpressure actually stalled valid beats", stall_beats > 0);
            check.dec("TX held data keep last and valid under stalls", stall_bad, 0);
            check.that("gPTP packets traversed actual backpressure", stalled_ptp_frames > 0);
            publication("after backpressure", true); completed[5] = true;
            loss_recovery(); completed[6] = true;
            printf("RESET: assert with audio and peer active, flush model in-flight packets\n");
            reset(); configure();
            check.hex("reset clears complete public GM", read_identity(0x624), 0);
            check.hex("reset clears complete public parent", read_identity(0x730), 0);
            audio_window("reset reacquisition", kHz * 3, -1, Until::Healthy);
            publication("reset recovered", true);
            audio_window("reset stable", kHz / 50, 0); completed[7] = true;
            check.dec("all scheduled Pdelay ingress events met deadlines", schedule_bad, 0);
            check.that("all epochs retain real Pdelay cadence",
                       pd_requests >= 2 && pd_cadence_bad == 0);
        } else printf("NOT RUN: long loss/backpressure/reset arms in negative-control mode\n");
    } catch (const std::exception& e) {
        check.fail(e.what());
        printf("NOT RUN: remaining arms after bounded transport failure\n");
    }
    return report();
}
}  // namespace

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, nullptr, _IOLBF, 0);
    bool negative = false;
    bool extended = false;
    TrafficControl traffic_control = TrafficControl::Normal;
    if (argc == 2 && std::string(argv[1]) == "--negative-control") negative = true;
    else if (argc == 2 && std::string(argv[1]) == "--extended") extended = true;
    else if (argc == 2 && std::string(argv[1]) == "--no-tx-control") traffic_control = TrafficControl::NoTx;
    else if (argc == 2 && std::string(argv[1]) == "--stop-tx-control") traffic_control = TrafficControl::StopTx;
    else if (argc != 1) {
        fprintf(stderr, "usage: %s [--negative-control|--extended|--no-tx-control|--stop-tx-control]\n", argv[0]);
        return 2;
    }
    Harness harness(negative, extended, traffic_control);
    return harness.run();
}

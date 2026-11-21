// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// twin_split.cpp - the two-placement simulation's split half (#665).
//
// tb_split_top: KL_mbx on the mailbox clock, KL_mbx_cdc and the two byte
// crossings, and milan_datapath at CTRL_SPLIT_P = 1, the shipping shape. The
// control firmware is the split image's own platform (sw/firmware/ctrl/plat,
// ctrl_plat.c's boot and composition), built for the host by twin_fw.py, as
// tb/verilator/mbx's co-simulation runs the firmware on the RTL mailbox:
//   - mbx_hal.h is KL_mbx's host port, one request a mailbox clock;
//   - ctrl_plat_io.h's CSR window is the datapath's AXI4-Lite port, its UART a
//     sink that is always empty and never full;
//   - F1's flash is the store's host flash model, blank, as test_plat_boot.cpp
//     gives it.
// The modeled millisecond is one KL_mbx millisecond tick: the bench pulses
// ms_tick_p_i, lets the mailbox and the datapath run, and services the loop
// until it reports nothing owed, so the firmware is never late against its
// own clock. MAAP's first range is pinned at twin::kMaapPreferred, compiled
// in by twin_fw.py (CTRL_PLAT_MAAP_PREFERRED, simulation only).
//
// Every control frame the datapath's MAC sends is captured with the
// millisecond it left at into the capture file twin_compare.py reads. With
// --plant NAME the capture is planted before it is written, so the comparison
// must refuse it (twin_compare.py names each plant's words):
//   byte-flip            one byte of the second ADPDU's payload inverted
//   srp-plus-k           the first MSRP Talker vector's FirstValue one higher
//   missing-notification the first unsolicited AECP response after the
//                        STOP_STREAMING response dropped
//
//   Vmilan_dp_twin_sp <capture.json> [--plant NAME]
//
// With --srptx SCENARIO it runs the split build's SRP transmit path instead
// (#867, srptx.hpp) and writes what srptx_grade.py grades:
//   Vmilan_dp_twin_sp --srptx wire|hold|licence <capture.json> [--ms N]
//                     [--peer-leave-all-ms N]   (licence only)
//
// With --maps it runs the platform's audio maps on the render store instead
// (#923, maps_main): each check prints PASS or FAIL with its label and words;
// --plant no-edit cuts the core's edit port after the boot.
//   Vmilan_dp_twin_sp --maps [--plant no-edit]
//
// With --fanout, built at the 8x8 shape with one interface (#948,
// fanout_main), a controller binds two and then three of the entity's Stream
// Inputs to one peer talker's stream over ACMP, the talker answering each
// probe, and unbinds one: each bound input counts and receives every PDU of
// the stream, the unbound one nothing. Each check prints PASS or FAIL with its
// label and words.
//   Vmilan_dp_twin8_sp --fanout

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <memory>
#include <stdexcept>
#include <string>
#include <vector>

#include "Vtb_split_top.h"
#include "Vtb_split_top___024root.h"
#include "verilated.h"

#include "srp_entity_gen.h"
#include "ctrl_plat.h"
#include "ctrl_plat_policy_gen.h"
#include "mbx_hal.h"
extern "C" {
#include "nvm_fmodel.h"
}
// the store's headers carry no extern "C", and its shape header asserts in C11's spelling
#define _Static_assert static_assert
extern "C" {
#include "nvm_store.h"
}
#undef _Static_assert
#include "twin.hpp"
#include "srptx.hpp"

namespace {

constexpr std::uintptr_t kCsr = 0x90000000u;
constexpr std::uintptr_t kUart = 0xf0001000u;
constexpr ctrl_plat_uart kUartRegs = {kUart + 0x0u, kUart + 0x4u, kUart + 0x8u, kUart + 0x10u};
constexpr unsigned kGuard = 4096;
//! Mailbox clocks the bench runs after each tick before it services the loop,
//! and the most service passes one millisecond takes.
constexpr unsigned kSettle = 64;
constexpr unsigned kPasses = 400;
//! --srptx (#867): after a millisecond's service the RTL runs until neither the
//! MAC nor the bench's receive side has moved a beat for kDrainIdle datapath
//! cycles since the last TX commit, past ctl_tx_mux's 512-cycle gap and the
//! path's latency, then the loop is serviced again and drained again. So a
//! committed frame leaves at its RTL time inside the millisecond, and a
//! received one is taken, answered and sent inside it; at most kDrainMax.
constexpr std::uint64_t kDrainIdle = 2048;
constexpr std::uint64_t kDrainMax = 50000;

//! --fanout (#948): the peer talker's stream, as its PROBE_TX_RESPONSE gives it, and whether the talker answers.
constexpr std::uint64_t kFanStream = 0x0202DEADBEEF0005ull;
constexpr std::uint64_t kFanDest = 0x91E0F0005B0Aull;
bool& twin_talker_answers() {
    static bool on = false;
    return on;
}

//! The peer talker's PROBE_TX_RESPONSE to the entity's PROBE_TX_COMMAND (IEEE 1722.1-2021 8.2.1.5, Milan v1.2
//! 5.5.3.5.18): the command echoed, message_type 1, status SUCCESS, and the stream's stream_id, destination and
//! VLAN 2. False for any other frame.
bool probe_tx_answer(const twin::Frame& sent, twin::Frame* answer) {
    std::uint16_t t = 0;
    std::size_t at = 0;
    if (!twin::ethertype(sent, &t, &at) || t != twin::kEtherAvtp || at != 14 || sent.size() < 70) return false;
    if (sent[14] != twin::kSubAcmp || (sent[15] & 0xFu) != 0u) return false;
    std::uint64_t talker = 0;
    for (unsigned k = 0; k < 8; ++k) talker = talker << 8 | sent[34 + k];
    if (talker != twin::kPeerTalker) return false;
    *answer = sent;
    twin::put_be(*answer, 6, twin::kPeerMac, 6);
    (*answer)[15] = static_cast<std::uint8_t>((sent[15] & 0xF0u) | 1u);
    (*answer)[16] = static_cast<std::uint8_t>(sent[16] & 0x07u);
    twin::put_be(*answer, 18, kFanStream, 8);
    twin::put_be(*answer, 54, kFanDest, 6);
    twin::put_be(*answer, 60, 1, 2);
    twin::put_be(*answer, 66, 2, 2);
    return true;
}

class SplitHalf {
 public:
    explicit SplitHalf(Vtb_split_top* d) : d_(d) {}

    void reset();
    std::uint32_t host(std::uint32_t byte_off, bool we, std::uint32_t v);
    void axi_write(std::uint16_t addr, std::uint32_t value);
    std::uint32_t axi_read(std::uint16_t addr);
    void sys(std::uint64_t n);
    void tick_ms();
    void mac_rx(const twin::Frame& f) { rx_q_.push_back(f); }
    bool quiet() const { return rx_q_.empty() && tx_cur_.empty(); }
    std::uint32_t ms() const { return ms_; }
    //! The modeled time in us: the tick's millisecond, then 2.5 ns a bench unit since it (srptx.hpp)
    double now_us() const { return ms_ * 1000.0 + static_cast<double>(u_ - u_tick_) * 0.0025; }
    const Vtb_split_top* dut() const { return d_; }
    void tx_committed() { tx_active_dp_ = dp_; }
    void drain();
    void capture(twin::Capture* cap) { cap_ = cap; }
    unsigned host_timeouts() const { return host_timeouts_; }
    std::string& console() { return console_; }

 private:
    struct Fires {
        bool aw = false;
        bool w = false;
        bool b = false;
        bool ar = false;
        bool r = false;
        std::uint32_t data = 0;
    };

    void unit();
    void dp_edge();
    void dp_cycles(unsigned n);
    void rx_drive();
    void tx_take();

    Vtb_split_top* d_;
    std::uint64_t u_ = 0;
    std::uint64_t u_tick_ = 0;
    double first_us_ = 0;
    std::uint64_t dp_ = 0;
    std::uint64_t tx_active_dp_ = 0;
    std::uint64_t rx_active_dp_ = 0;
    std::uint32_t ms_ = 0;
    Fires fires_{};
    bool rx_fire_ = false;
    std::deque<twin::Frame> rx_q_;
    std::size_t rx_off_ = 0;
    twin::Frame tx_cur_;
    twin::Capture* cap_ = nullptr;
    unsigned host_timeouts_ = 0;
    std::string console_;
};

//! One time unit: the mailbox clock toggles every second unit (period 4),
//! the datapath's every fourth, offset by one (period 8), as sim_split.cpp.
void SplitHalf::unit() {
    ++u_;
    if (u_ % 2 == 0) {
        const bool rising = !d_->sys_clk;
        d_->sys_clk = rising;
        d_->eval();
        if (rising) d_->ms_tick_p_i = 0;
    } else if (u_ % 4 == 1) {
        const bool rising = !d_->dp_clk;
        if (rising) dp_edge();
        d_->dp_clk = rising;
        d_->eval();
        if (rising) {
            ++dp_;
            if (rx_fire_) {
                rx_off_ += 8;
                if (rx_off_ >= rx_q_.front().size()) {
                    rx_q_.pop_front();
                    rx_off_ = 0;
                }
            }
            rx_drive();
            d_->eval();
        }
    }
}

//! What the datapath clock's rising edge takes: every handshake as it stands before it.
void SplitHalf::dp_edge() {
    rx_fire_ = d_->rx_tvalid && d_->rx_tready;
    fires_.aw = d_->s_axi_awvalid && d_->s_axi_awready;
    fires_.w = d_->s_axi_wvalid && d_->s_axi_wready;
    fires_.b = d_->s_axi_bvalid && d_->s_axi_bready;
    fires_.ar = d_->s_axi_arvalid && d_->s_axi_arready;
    fires_.r = d_->s_axi_rvalid && d_->s_axi_rready;
    fires_.data = d_->s_axi_rdata;
    tx_take();
}

void SplitHalf::rx_drive() {
    const bool busy = !rx_q_.empty();
    if (busy) rx_active_dp_ = dp_;
    const twin::Frame* f = busy ? &rx_q_.front() : nullptr;
    std::uint64_t data = 0;
    std::uint32_t keep = 0;
    for (std::size_t i = 0; busy && i < 8 && rx_off_ + i < f->size(); ++i) {
        data |= static_cast<std::uint64_t>((*f)[rx_off_ + i]) << (8 * i);
        keep |= 1u << i;
    }
    d_->rx_tvalid = busy;
    d_->rx_tlast = busy && rx_off_ + 8 >= f->size();
    d_->rx_tdata = data;
    d_->rx_tkeep = keep;
}

void SplitHalf::tx_take() {
    if (d_->tx_tvalid) tx_active_dp_ = dp_;
    if (!d_->tx_tvalid || !d_->tx_tready) return;
    if (tx_cur_.empty()) first_us_ = now_us();
    for (unsigned i = 0; i < 8; ++i)
        if (d_->tx_tkeep & (1u << i)) tx_cur_.push_back(static_cast<std::uint8_t>(d_->tx_tdata >> (8 * i)));
    if (!d_->tx_tlast) return;
    twin::Frame answer;
    const char* who = nullptr;
    if (twin_talker_answers() && probe_tx_answer(tx_cur_, &answer)) rx_q_.push_back(answer);
    if (cap_ != nullptr && twin::is_control(tx_cur_)) {
        cap_->frames.push_back({ms_, tx_cur_});
        if (twin::controller_available_answer(tx_cur_, &answer, &who)) {
            rx_q_.push_back(answer);
            cap_->applied.push_back({ms_, who, answer});
        }
    } else if (cap_ != nullptr) {
        cap_->stream_frame(ms_);
    }
    if (cap_ != nullptr && srptx::mac_frame(tx_cur_, first_us_, &answer)) {
        rx_q_.push_back(answer);
        cap_->applied.push_back({ms_, "MSRP Listener Ready JoinIn for source 0, the peer answering a LeaveAll", answer});
    }
    tx_cur_.clear();
}

void SplitHalf::drain() {
    const std::uint64_t until = dp_ + kDrainMax;
    while (dp_ < until && (d_->tx_tvalid || !tx_cur_.empty() || !rx_q_.empty() || dp_ - tx_active_dp_ < kDrainIdle ||
                           dp_ - rx_active_dp_ < kDrainIdle))
        dp_cycles(64);
}

void SplitHalf::dp_cycles(unsigned n) {
    const std::uint64_t until = dp_ + n;
    while (dp_ < until) unit();
}

void SplitHalf::sys(std::uint64_t n) {
    // a mailbox clock is two units, so n of them are 4n units
    for (std::uint64_t k = 0; k < 4 * n; ++k) unit();
}

void SplitHalf::reset() {
    d_->sys_rst_n = 0;
    d_->dp_rst_n = 0;
    d_->host_req_i = 0;
    d_->rx_tvalid = 0;
    d_->tx_tready = 1;
    d_->link_up = 1;
    d_->s_axi_awvalid = 0;
    d_->s_axi_wvalid = 0;
    d_->s_axi_arvalid = 0;
    d_->s_axi_bready = 0;
    d_->s_axi_rready = 0;
    // tb_split_top's second KL_ctrl_split, the split leg's tap, idle here
    d_->tap_tvalid = 0;
    d_->tap_ready = 1;
    sys(20);
    d_->sys_rst_n = 1;
    d_->dp_rst_n = 1;
    sys(20);
}

//! One KL_mbx host access: the request for one mailbox clock, then the clock its ack arrives.
std::uint32_t SplitHalf::host(std::uint32_t byte_off, bool we, std::uint32_t v) {
    d_->host_req_i = 1;
    d_->host_we_i = we;
    d_->host_addr_i = byte_off / 4u;
    d_->host_wdata_i = v;
    d_->host_be_i = 0xF;
    sys(1);
    d_->host_req_i = 0;
    d_->host_we_i = 0;
    for (int i = 0; i < 8; ++i) {
        if (d_->host_ack_o) {
            const std::uint32_t r = d_->host_rdata_o;
            sys(1);
            return r;
        }
        sys(1);
    }
    ++host_timeouts_;
    return 0;
}

void SplitHalf::axi_write(std::uint16_t addr, std::uint32_t value) {
    d_->s_axi_awaddr = addr;
    d_->s_axi_awvalid = 1;
    d_->s_axi_wdata = value;
    d_->s_axi_wstrb = 0xF;
    d_->s_axi_wvalid = 1;
    d_->s_axi_bready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        dp_cycles(1);
        if (fires_.aw) d_->s_axi_awvalid = 0;
        if (fires_.w) d_->s_axi_wvalid = 0;
        if (fires_.b) {
            d_->s_axi_bready = 0;
            return;
        }
    }
    throw std::runtime_error("AXI write response timeout");
}

std::uint32_t SplitHalf::axi_read(std::uint16_t addr) {
    d_->s_axi_araddr = addr;
    d_->s_axi_arvalid = 1;
    d_->s_axi_rready = 1;
    for (unsigned g = 0; g < kGuard; ++g) {
        dp_cycles(1);
        if (fires_.ar) d_->s_axi_arvalid = 0;
        if (fires_.r) {
            d_->s_axi_rready = 0;
            return fires_.data;
        }
    }
    throw std::runtime_error("AXI read response timeout");
}

//! The tick: the millisecond that ends is checked against 1 ms of RTL time
//! (srptx.hpp), and the MAC refuses every beat while a hold is in force.
void SplitHalf::tick_ms() {
    if (ms_ > 0)
        srptx::rec().intra_ms_max_us = std::max(srptx::rec().intra_ms_max_us, now_us() - ms_ * 1000.0);
    u_tick_ = u_;
    d_->ms_tick_p_i = 1;
    sys(1);
    ++ms_;
    d_->tx_tready = srptx::held(ms_) ? 0 : 1;
    nvm_fmodel_advance_us(1000);
}

//! The half the HAL calls reach: the one instance main() makes.
SplitHalf*& current() {
    static SplitHalf* half = nullptr;
    return half;
}

//! The platform's environment, as test_plat_boot.cpp's SetUp() builds it.
struct Env {
    ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
    ctrl_plat_stream streams[CTRL_SRP_SOURCES] = CTRL_PLAT_STREAMS_INIT;
    nvm_flash flash{};
    ctrl_plat_env env{};

    Env() {
        nvm_fmodel_blank();
        nvm_fmodel_power_on();
        nvm_fmodel_window(NVM_SLOT_A, NVM_SLOT_B + NVM_SLOT_BYTES);
        nvm_fmodel_times(1000, 100);
        flash = nvm_fmodel_port;
        env.flash = &flash;
        env.csr = kCsr;
        env.uart = kUartRegs;
        env.policy = &policy;
        env.streams = streams;
        env.aaf_outputs = CTRL_PLAT_AAF_OUTPUTS;
        env.crf_output = CTRL_PLAT_CRF_OUTPUT;
        env.link_rate_bps = CTRL_PLAT_LINK_BPS;
        ctrl_plat_generated_image(&env);
    }
};

//! One modeled millisecond: the stimulus due, the tick, the settle, then the
//! loop serviced until nothing is owed and the MAC has gone quiet.
void millisecond(SplitHalf& half, const std::vector<twin::Stimulus>& stim, std::size_t* next,
                 twin::Capture* cap) {
    while (*next < stim.size() && stim[*next].ms <= half.ms()) {
        half.mac_rx(stim[*next].frame);
        cap->applied.push_back({half.ms(), stim[*next].what, stim[*next].frame});
        srptx::applied(stim[*next].what);
        ++*next;
    }
    half.tick_ms();
    half.sys(kSettle);
    const unsigned rounds = srptx::rec().on && !srptx::held(half.ms()) ? 2 : 1;
    for (unsigned round = 0; round < rounds; ++round) {
        for (unsigned pass = 0; pass < kPasses; ++pass) {
            const unsigned owed = ctrl_loop_service(&ctrl_plat.app.loop);
            if (owed == 0 && half.quiet()) break;
            half.sys(kSettle);
        }
        if (rounds == 2) half.drain();
    }
    srptx::sample(half.dut());
}

//! The first Talker message's first vector (IEEE 802.1Q-2018 10.8.1.2: each
//! MSRP message is AttributeType, AttributeLength, AttributeListLength, then
//! its vectors; a vector's two-byte header precedes FirstValue, whose
//! stream_id is its first eight bytes, Table 35-2): its stream_id's last byte
//! one higher, so every FirstValue + k it declares is off by one.
bool bump_talker(twin::Frame* f, std::size_t at) {
    std::size_t m = at + 1;
    while (m + 4 + 2 + 8 <= f->size() && !((*f)[m] == 0 && (*f)[m + 1] == 0)) {
        const std::uint8_t kind = (*f)[m];
        if (kind == 1 || kind == 2) {
            ++(*f)[m + 4 + 2 + 7];
            return true;
        }
        m += 4 + static_cast<std::size_t>((*f)[m + 2] << 8 | (*f)[m + 3]);
    }
    return false;
}

//! The planted difference --plant names, applied to the capture.
bool plant(const std::string& name, twin::Capture* cap) {
    unsigned adp = 0;
    bool stopped = false;
    for (auto it = cap->frames.begin(); it != cap->frames.end(); ++it) {
        twin::Frame& f = it->bytes;
        std::uint16_t t = 0;
        std::size_t at = 0;
        if (!twin::ethertype(f, &t, &at)) continue;
        const bool avtp = t == twin::kEtherAvtp && at + 24 < f.size();
        if (name == "byte-flip" && avtp && f[at] == twin::kSubAdp && ++adp == 2) {
            f[at + 20] = static_cast<std::uint8_t>(~f[at + 20]);
            return true;
        }
        // the STOP_STREAMING response (command_type 0x0023), then the first
        // unsolicited response after it (IEEE 1722.1-2021 7.5.2)
        const bool aem = avtp && f[at] == twin::kSubAecp;
        stopped = stopped || (aem && f[at + 22] == 0x00 && f[at + 23] == 0x23);
        if (name == "missing-notification" && stopped && aem && (f[at + 22] & 0x80u)) {
            cap->frames.erase(it);
            return true;
        }
        if (name == "srp-plus-k" && t == twin::kEtherMsrp && bump_talker(&f, at)) return true;
    }
    return false;
}

}  // namespace

// mbx_hal.h on KL_mbx's host port
extern "C" std::uint32_t mbx_hal_read32(std::uint32_t byte_offset) {
    const std::uint32_t v = current()->host(byte_offset, false, 0);
    srptx::hal_read(byte_offset, v);
    return v;
}

extern "C" void mbx_hal_write32(std::uint32_t byte_offset, std::uint32_t value) {
    srptx::hal_write(byte_offset, value);
    (void)current()->host(byte_offset, true, value);
    if (srptx::rec().on && srptx::tx_head(byte_offset)) current()->tx_committed();
}

extern "C" void mbx_hal_wait(void) {}

// ctrl_plat_io.h: the datapath's CSR window, and a UART that never holds a byte
extern "C" std::uint32_t ctrl_plat_io_read32(std::uintptr_t address) {
    if (address >= kCsr && address < kCsr + 0x10000u) {
        return current()->axi_read(static_cast<std::uint16_t>(address - kCsr));
    }
    return address == kUartRegs.rxempty ? 1u : 0u;
}

extern "C" void ctrl_plat_io_write32(std::uintptr_t address, std::uint32_t value) {
    if (address >= kCsr && address < kCsr + 0x10000u) {
        current()->axi_write(static_cast<std::uint16_t>(address - kCsr), value);
    } else if (address == kUartRegs.rxtx) {
        current()->console().push_back(static_cast<char>(value));
    }
}

//! The --srptx run (srptx.hpp): the scenario's stimulus on the split half
//! from reset, recorded at lwSRP's boundary, its timers, the mailbox and the MAC.
int srptx_main(const std::string& name, const char* path, std::uint32_t run_ms) {
    if (name != "wire" && name != "hold" && name != "licence") {
        std::fprintf(stderr, "FAIL --srptx takes wire, hold or licence, not %s\n", name.c_str());
        return 2;
    }
    if (name != "licence" && srptx::rec().peer_leave_all_ms != srptx::kPeerLeaveAllMs) {
        std::fprintf(stderr, "FAIL --peer-leave-all-ms moves the licence scenario's peer LeaveAll, not %s's\n",
                     name.c_str());
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    SplitHalf half(dut.get());
    current() = &half;
    srptx::Recorder& r = srptx::rec();
    r.ms = [] { return current()->ms(); };
    r.us = [] { return current()->now_us(); };
    static Env env;
    r.talker_sid = twin::kEntityMac << 16 | env.streams[0].unique_id;
    const std::vector<twin::Stimulus> stim = srptx::scenario(name);
    if (run_ms) r.run_ms = run_ms;
    twin::Capture cap;
    r.on = true;
    half.reset();
    half.capture(&cap);
    const ctrl_plat_stage stage = ctrl_plat_boot(&env.env);
    if (stage != CTRL_PLAT_READY) {
        std::fprintf(stderr, "FAIL the platform stopped its boot at stage %d: %s\n", static_cast<int>(stage),
                     half.console().c_str());
        return 2;
    }
    std::size_t next = 0;
    while (half.ms() < r.run_ms) millisecond(half, stim, &next, &cap);
    half.drain();
    r.on = false;
    dut->final();
    if (!srptx::write(path, cap.applied)) {
        std::fprintf(stderr, "FAIL the capture %s was not written\n", path);
        return 2;
    }
    std::printf("srptx %s: %zu control frames, %zu MRPDUs from lwSRP, %u sent by the adapter, %u host timeouts, %u ms\n",
                name.c_str(), r.mac.size(), r.lib.size(), ctrl_plat.srp.transmitted, half.host_timeouts(), r.run_ms);
    return half.host_timeouts() == 0 && r.layout_error.empty() ? 0 : 1;
}

//! ---- --maps (#923): the platform firmware's audio maps on the split datapath's render store ----

//! The render map store's byte for input key k (milan_datapath.sv amap_in_store_r: {valid, 0, stream[2:0],
//! channel[2:0]} a key, the input port's key its cluster), whatever width Verilator gives the store.
template <class T> unsigned store_byte(const T& v, unsigned k) {
    return static_cast<unsigned>((static_cast<std::uint64_t>(v) >> (8u * k)) & 0xFFu);
}
template <std::size_t W> unsigned store_byte(const VlWide<W>& v, unsigned k) {
    return (v[k / 4u] >> (8u * (k % 4u))) & 0xFFu;
}

class Maps {
 public:
    Maps(SplitHalf& half, twin::Capture& cap) : half_(half), cap_(cap) {}

    //! One check: PASS or FAIL with its label and its words, one line each.
    void check(bool ok, const char* label, const std::string& words) {
        std::printf("%s [%s] %s\n", ok ? "PASS" : "FAIL", label, words.c_str());
        failed_ += ok ? 0u : 1u;
    }
    unsigned failed() const { return failed_; }

    //! An AEM command and its response's status, or -1 with none within 60 ms; then THE PACE's 10 ms.
    int ask(std::uint16_t command_type, const std::vector<std::uint8_t>& payload, twin::Frame* out = nullptr) {
        const std::uint16_t seq = seq_++;
        const std::size_t from = cap_.frames.size();
        half_.mac_rx(twin::aem(command_type, payload, seq));
        const std::vector<twin::Stimulus> none;
        std::size_t next = 0;
        int status = -1;
        for (unsigned ms = 0; ms < 60 && status < 0; ++ms) {
            millisecond(half_, none, &next, &cap_);
            for (std::size_t k = from; k < cap_.frames.size() && status < 0; ++k) {
                const twin::Frame& f = cap_.frames[k].bytes;
                std::uint16_t t = 0;
                std::size_t at = 0;
                if (twin::ethertype(f, &t, &at) && t == twin::kEtherAvtp && at + 24 <= f.size() &&
                    f[at] == twin::kSubAecp && (f[at + 1] & 0xFu) == 1u && (f[at + 20] << 8 | f[at + 21]) == seq &&
                    (f[at + 22] << 8 | f[at + 23]) == command_type) {
                    status = f[at + 2] >> 3;
                    if (out != nullptr) out->assign(f.begin() + static_cast<std::ptrdiff_t>(at), f.end());
                }
            }
        }
        for (unsigned ms = 0; ms < 10; ++ms) millisecond(half_, none, &next, &cap_);
        return status;
    }

    //! GET_AUDIO_MAP of STREAM_PORT_INPUT 0, page 0: its mappings, each {stream, channel, cluster, cluster_channel}.
    std::vector<std::array<unsigned, 4>> get_map() {
        std::vector<std::uint8_t> p = twin::descriptor(14, 0);
        p.resize(8, 0);
        twin::Frame r;
        std::vector<std::array<unsigned, 4>> rows;
        if (ask(0x002B, p, &r) != 0 || r.size() < 36) return {{9999, 0, 0, 0}};
        const unsigned count = static_cast<unsigned>(r[32] << 8 | r[33]);
        for (unsigned k = 0; k < count && 36 + 8 * k + 8 <= r.size(); ++k) {
            const std::uint8_t* m = r.data() + 36 + 8 * k;
            rows.push_back({static_cast<unsigned>(m[0] << 8 | m[1]), static_cast<unsigned>(m[2] << 8 | m[3]),
                            static_cast<unsigned>(m[4] << 8 | m[5]), static_cast<unsigned>(m[6] << 8 | m[7])});
        }
        return rows;
    }

    //! The render store's mappings of STREAM_PORT_INPUT 0's clusters, as GET_AUDIO_MAP reports them, in cluster order.
    std::vector<std::array<unsigned, 4>> store() const {
        std::vector<std::array<unsigned, 4>> rows;
        for (unsigned k = 0; k < kClusters; ++k) {
            const unsigned b = store_byte(half_.dut()->rootp->tb_split_top__DOT__u_dp__DOT__amap_in_store_r, k);
            if (b & 0x80u) rows.push_back({(b >> 3) & 7u, b & 7u, k, 0});
        }
        return rows;
    }

    //! GET_AUDIO_MAP's mappings and the store's, the same set.
    void agree(const char* label, const std::string& after) {
        auto got = get_map();
        auto held = store();
        std::sort(got.begin(), got.end(), [](auto& x, auto& y) { return x[2] < y[2]; });
        check(got == held, label, "GET_AUDIO_MAP and the render store agree " + after);
    }

    //! SET_STREAM_FORMAT of STREAM_INPUT 0 to its declared format at `channels` channels.
    int set_channels(unsigned channels) {
        const std::uint64_t format = (kInFormat & ~(std::uint64_t(1023) << 22)) | (std::uint64_t(channels) << 22);
        std::vector<std::uint8_t> p = twin::descriptor(5, 0);
        for (unsigned k = 0; k < 8; ++k) p.push_back(static_cast<std::uint8_t>(format >> (56 - 8 * k)));
        return ask(0x0008, p);
    }

    //! ADD (0x002C) or REMOVE (0x002D) of `rows` at STREAM_PORT_INPUT 0.
    int edit(std::uint16_t command_type, const std::vector<std::array<unsigned, 4>>& rows) {
        std::vector<std::uint8_t> p = twin::descriptor(14, 0);
        p.push_back(static_cast<std::uint8_t>(rows.size() >> 8));
        p.push_back(static_cast<std::uint8_t>(rows.size()));
        p.push_back(0);
        p.push_back(0);
        for (auto& r : rows)
            for (unsigned v : r) {
                p.push_back(static_cast<std::uint8_t>(v >> 8));
                p.push_back(static_cast<std::uint8_t>(v));
            }
        return ask(command_type, p);
    }

    //! STREAM_INPUT 0's declared format and STREAM_PORT_INPUT 0's clusters at the twin's shape.
    static constexpr std::uint64_t kInFormat = TWIN_IN0_FMT;
    static constexpr unsigned kClusters = 8;

 private:
    SplitHalf& half_;
    twin::Capture& cap_;
    std::uint16_t seq_ = 0x9230;
    unsigned failed_ = 0;
};

//! The --maps run: the platform's boot on the split half, then each map check, the saved map at the next boot.
//! With --plant no-edit the core's edit port is cut after the boot, the defect #923 found, and every check that reads
//! the store must fail.
int maps_main(const std::string& plant) {
    if (!plant.empty() && plant != "no-edit") {
        std::fprintf(stderr, "FAIL --maps plants no-edit alone, not %s\n", plant.c_str());
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    SplitHalf half(dut.get());
    current() = &half;
    twin::Capture cap;
    half.reset();
    half.capture(&cap);
    static Env env;
    if (ctrl_plat_boot(&env.env) != CTRL_PLAT_READY) {
        std::fprintf(stderr, "FAIL the platform stopped its boot: %s\n", half.console().c_str());
        return 2;
    }
    if (plant == "no-edit") ctrl_plat.aecp.ports.edit = nullptr;
    Maps m(half, cap);
    using Rows = std::vector<std::array<unsigned, 4>>;
    Rows identity;
    for (unsigned c = 0; c < Maps::kClusters; ++c) identity.push_back({0, c, c, 0});
    m.check(m.store() == identity, "MAPS-BOOT", "the render store holds the boot map, eight identity mappings");
    m.agree("MAPS-BOOT", "at boot");
    m.check(m.set_channels(4) == 7, "MAPS-REFUSED",
            "with the mappings in place, a narrowing SET_STREAM_FORMAT answers BAD_ARGUMENTS");
    m.check(m.edit(0x002D, identity) == 0, "MAPS-REMOVE", "REMOVE_AUDIO_MAPPINGS of all eight answers SUCCESS");
    m.check(m.store().empty(), "MAPS-STORE", "the removal reached the render store");
    m.agree("MAPS-STORE", "after the removal");
    for (unsigned channels : {1u, 2u, 4u, 6u}) {
        m.check(m.set_channels(channels) == 0, "MAPS-FORMAT",
                "once the mappings are removed, a narrowing SET_STREAM_FORMAT to " + std::to_string(channels) +
                    (channels == 1 ? " channel" : " channels") + " answers SUCCESS");
    }
    m.check(m.set_channels(7) == 7, "MAPS-FORMAT", "7 channels, a format the input does not support, is refused");
    m.check(m.set_channels(8) == 0, "MAPS-FORMAT", "the declared 8 channels answer SUCCESS");
    const Rows edited{{0, 1, 0, 0}, {0, 0, 1, 0}, {0, 2, 2, 0}};
    m.check(m.edit(0x002C, edited) == 0, "MAPS-ADD", "ADD_AUDIO_MAPPINGS of an edited map answers SUCCESS");
    m.check(m.store() == edited, "MAPS-EDIT", "an edited map reached the render store");
    m.agree("MAPS-EDIT", "after the addition");
    m.check(m.set_channels(2) == 7, "MAPS-REFUSED",
            "with a mapping of channel 2 in place, a SET_STREAM_FORMAT to 2 channels answers BAD_ARGUMENTS");
    // the saved map: once its save is durable, a power cycle and the next boot restore it to the store
    const unsigned saved = nvm_store_status()->commits_ok;
    const std::vector<twin::Stimulus> none;
    std::size_t next = 0;
    for (unsigned ms = 0; ms < 20000 && nvm_store_status()->commits_ok == saved; ++ms) millisecond(half, none, &next, &cap);
    m.check(nvm_store_status()->commits_ok != saved, "MAPS-SAVED", "the edited map's save is durable");
    // the power cycle: SRP's participants released as the image's end releases them, the RTL reset, the flash
    // powered on again with what it holds, and the platform's boot from the start
    srp_mbx_destroy(&ctrl_plat.srp);
    half.reset();
    nvm_fmodel_power_on();
    const ctrl_plat_stage again = ctrl_plat_boot(&env.env);
    m.check(again == CTRL_PLAT_READY, "MAPS-SAVED",
            "the platform boots again from the saved state (stage " + std::to_string(static_cast<int>(again)) + ")");
    if (again != CTRL_PLAT_READY) std::printf("console: %s\n", half.console().c_str());
    m.check(m.store() == edited, "MAPS-SAVED", "the saved map, restored at boot, reached the render store");
    m.agree("MAPS-SAVED", "after the restore");
    dut->final();
    std::printf("maps%s: %u failed, %u host timeouts, %u ms, %u EDIT and GSI beats with no answer since the boot\n",
                plant.empty() ? "" : (" planted " + plant).c_str(), m.failed(), half.host_timeouts(), half.ms(),
                ctrl_plat.face.unanswered);
    return m.failed() == 0 && half.host_timeouts() == 0 ? 0 : 1;
}


//! ---- --fanout (#948): one peer talker's stream bound to several Stream Inputs, the 8x8 shape ----

class Fan {
 public:
    Fan(SplitHalf& half, twin::Capture& cap) : half_(half), cap_(cap) {}

    void check(bool ok, const char* label, const std::string& words) {
        std::printf("%s [%s] %s\n", ok ? "PASS" : "FAIL", label, words.c_str());
        failed_ += ok ? 0u : 1u;
    }
    unsigned failed() const { return failed_; }

    void run_ms(unsigned n) {
        const std::vector<twin::Stimulus> none;
        std::size_t next = 0;
        for (unsigned ms = 0; ms < n; ++ms) millisecond(half_, none, &next, &cap_);
    }

    //! BIND_RX (CONNECT_RX_COMMAND) or UNBIND_RX (DISCONNECT_RX_COMMAND) of STREAM_INPUT `s` to the peer talker's
    //! unique_id 0, then 100 ms: the bind's probe is answered by the talker, and the listener settles
    void acmp(bool bind, unsigned s) {
        twin::Frame f = twin::acmp(bind ? 6 : 8, twin::kPeerTalker, twin::kEntityId, seq_++);
        twin::put_be(f, 52, s, 2);
        half_.mac_rx(f);
        run_ms(100);
    }

    //! An AEM command and its response from the AVTP header on, or empty with none within 60 ms.
    twin::Frame ask(std::uint16_t command_type, const std::vector<std::uint8_t>& payload) {
        const std::uint16_t seq = seq_++;
        const std::size_t from = cap_.frames.size();
        half_.mac_rx(twin::aem(command_type, payload, seq));
        const std::vector<twin::Stimulus> none;
        std::size_t next = 0;
        twin::Frame out;
        for (unsigned ms = 0; ms < 60 && out.empty(); ++ms) {
            millisecond(half_, none, &next, &cap_);
            for (std::size_t k = from; k < cap_.frames.size() && out.empty(); ++k) {
                const twin::Frame& r = cap_.frames[k].bytes;
                std::uint16_t t = 0;
                std::size_t at = 0;
                if (twin::ethertype(r, &t, &at) && t == twin::kEtherAvtp && at + 24 <= r.size() &&
                    r[at] == twin::kSubAecp && (r[at + 1] & 0xFu) == 1u && (r[at + 20] << 8 | r[at + 21]) == seq &&
                    (r[at + 22] << 8 | r[at + 23]) == command_type)
                    out.assign(r.begin() + static_cast<std::ptrdiff_t>(at), r.end());
            }
        }
        return out;
    }

    //! STREAM_INPUT s's TIMESTAMP_VALID as GET_COUNTERS answers it (IEEE 1722.1-2021 Table 7-157 @24: a received
    //! PDU with tv set, counted on receipt), or -1 with no SUCCESS answer
    long counted(unsigned s) {
        const twin::Frame r = ask(0x0029, twin::descriptor(5, static_cast<std::uint16_t>(s)));
        if (r.size() < 32 + 4 * 12 || (r[2] >> 3) != 0) return -1;
        const std::size_t o = 32 + 4 * 6;
        return static_cast<long>(static_cast<std::uint32_t>(r[o]) << 24 | static_cast<std::uint32_t>(r[o + 1]) << 16 |
                                 static_cast<std::uint32_t>(r[o + 2]) << 8 | r[o + 3]);
    }

    //! The 0x800 window's PDUS word of index s, read between milliseconds, when the firmware is not running. For
    //! an input above 0 it is the input's DEPKT tally, its PDUs out of the depacketizer, the render path's input;
    //! index 0's is the flat alias of the depacketizer's shared total (milan_csr's index-0 snapshot, PCMRX_CNT),
    //! every PDU it emits for any input.
    long pdus_word(unsigned s) {
        half_.axi_write(0x800, s);
        half_.axi_write(0x804, 1);
        for (int g = 0; g < 256; ++g)
            if ((half_.axi_read(0x804) & 1u) == 0) break;
        return static_cast<long>(half_.axi_read(0x858) & 0xFFFFu);
    }

    //! `n` PDUs of the stream, one a millisecond, each 8 channels of six 48 kHz samples (the inputs' format)
    void send(unsigned n) {
        for (unsigned k = 0; k < n; ++k) {
            twin::Frame f = twin::eth(kFanDest, twin::kPeerMac, twin::kEtherAvtp, 14 + 24 + 192);
            f[14] = 0x02;                       // AAF
            f[15] = 0x81;                       // sv, tv
            f[16] = avtp_seq_++;
            twin::put_be(f, 18, kFanStream, 8);
            twin::put_be(f, 26, 0x1000, 4);
            f[30] = 0x02;                       // INT32
            f[31] = 0x05 << 4;                  // 48 kHz
            f[32] = 8;
            f[33] = 32;
            twin::put_be(f, 34, 192, 2);
            for (unsigned i = 0; i < 192; ++i) f[38 + i] = static_cast<std::uint8_t>(k * 13u + i);
            half_.mac_rx(f);
            run_ms(1);
        }
        run_ms(5);
    }

    //! A round of `n` PDUs: every input in `on` counts each in GET_COUNTERS and receives each, every input in
    //! `off` neither. An input above 0 is graded by its own DEPKT tally; the depacketizer's shared total grows by
    //! one PDU per receiving input, so with the others' tallies it grades input 0's share.
    void round(const char* label, unsigned n, std::initializer_list<unsigned> on, std::initializer_list<unsigned> off) {
        std::array<long, 8> c0{}, r0{};
        for (unsigned s : on) { c0[s] = counted(s); r0[s] = pdus_word(s); }
        for (unsigned s : off) { c0[s] = counted(s); r0[s] = pdus_word(s); }
        const long total0 = pdus_word(0);
        send(n);
        for (unsigned s : on) {
            const long c = counted(s);
            check(c0[s] >= 0 && c - c0[s] == static_cast<long>(n), label,
                  "STREAM_INPUT " + std::to_string(s) + " counts every PDU in GET_COUNTERS (" +
                      std::to_string(c - c0[s]) + " of " + std::to_string(n) + ")");
            if (s == 0) continue;
            const long r = pdus_word(s);
            check(r - r0[s] == static_cast<long>(n), label,
                  "STREAM_INPUT " + std::to_string(s) + " receives every PDU (" + std::to_string(r - r0[s]) +
                      " of " + std::to_string(n) + ")");
        }
        for (unsigned s : off) {
            const long c = counted(s);
            const long r = s == 0 ? r0[s] : pdus_word(s);
            check(c0[s] >= 0 && c == c0[s] && r == r0[s], label,
                  "STREAM_INPUT " + std::to_string(s) + " counts and receives nothing");
        }
        const long total = pdus_word(0) - total0;
        check(total == static_cast<long>(n * on.size()), label,
              "the depacketizer emits one PDU per receiving input (" + std::to_string(total) + " of " +
                  std::to_string(n * on.size()) + ")");
    }

 private:
    SplitHalf& half_;
    twin::Capture& cap_;
    std::uint16_t seq_ = 0x9480;
    std::uint8_t avtp_seq_ = 0;
    unsigned failed_ = 0;
};

//! The --fanout run: the platform's boot on the split half at 8x8/1if, then the binds, the PDUs and the checks.
int fanout_main() {
    // three AAF Stream Inputs and the CRF input: the 8x8 shape (the twin's own shape, 1x1, has one AAF input)
    if (CTRL_AEM_STREAM_INPUTS < 4) {
        std::fprintf(stderr, "FAIL --fanout runs at a shape with three AAF Stream Inputs; this one has %u inputs\n",
                     static_cast<unsigned>(CTRL_AEM_STREAM_INPUTS));
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    SplitHalf half(dut.get());
    current() = &half;
    twin::Capture cap;
    half.reset();
    half.capture(&cap);
    static Env env;
    if (ctrl_plat_boot(&env.env) != CTRL_PLAT_READY) {
        std::fprintf(stderr, "FAIL the platform stopped its boot: %s\n", half.console().c_str());
        return 2;
    }
    twin_talker_answers() = true;
    Fan f(half, cap);
    f.run_ms(200);
    f.acmp(true, 0);
    f.acmp(true, 1);
    f.round("FAN-TWO", 4, {0, 1}, {2});
    f.acmp(true, 2);
    f.round("FAN-THREE", 4, {0, 1, 2}, {});
    f.acmp(false, 1);
    f.round("FAN-UNBIND", 4, {0, 2}, {1});
    dut->final();
    std::printf("fanout: %u failed, %u host timeouts, %u ms\n", f.failed(), half.host_timeouts(), half.ms());
    return f.failed() == 0 && half.host_timeouts() == 0 ? 0 : 1;
}

//! --srptx SCENARIO CAPTURE, then each option with its value: --ms N, --peer-leave-all-ms N.
bool srptx_args(int argc, char** argv, std::uint32_t* run_ms) {
    if (argc < 4 || argc % 2 != 0 || std::strcmp(argv[1], "--srptx") != 0) return false;
    for (int k = 4; k < argc; k += 2) {
        const bool ms = std::strcmp(argv[k], "--ms") == 0;
        if (!ms && std::strcmp(argv[k], "--peer-leave-all-ms") != 0) return false;
        const auto value = static_cast<std::uint32_t>(std::stoul(argv[k + 1]));
        if (ms) {
            *run_ms = value;
        } else {
            srptx::rec().peer_leave_all_ms = value;
        }
    }
    return true;
}

int main(int argc, char** argv) {
    std::uint32_t run_ms = 0;
    if (srptx_args(argc, argv, &run_ms)) return srptx_main(argv[2], argv[3], run_ms);
    if (argc == 2 && std::strcmp(argv[1], "--fanout") == 0) return fanout_main();
    if (argc >= 2 && std::strcmp(argv[1], "--maps") == 0) {
        if (argc != 2 && !(argc == 4 && std::strcmp(argv[2], "--plant") == 0)) {
            std::fprintf(stderr, "usage: %s --maps [--plant no-edit]\n", argv[0]);
            return 2;
        }
        return maps_main(argc == 4 ? argv[3] : "");
    }
    const std::string planted = argc == 4 && std::strcmp(argv[2], "--plant") == 0 ? argv[3] : "";
    if (argc != 2 && planted.empty()) {
        std::fprintf(stderr, "usage: %s <capture.json> [--plant NAME]\n", argv[0]);
        return 2;
    }
    auto ctx = std::make_unique<VerilatedContext>();
    const auto dut = std::make_unique<Vtb_split_top>(ctx.get());
    SplitHalf half(dut.get());
    current() = &half;
    twin::Capture cap;
    cap.placement = "split";
    cap.ms_unit = "KL_mbx millisecond tick";
    half.reset();
    half.capture(&cap);
    static Env env;
    const ctrl_plat_stage stage = ctrl_plat_boot(&env.env);
    cap.notes.push_back({"boot_stage", std::to_string(static_cast<int>(stage))});
    cap.notes.push_back({"boot_ms", std::to_string(half.ms())});
    if (stage != CTRL_PLAT_READY) {
        std::fprintf(stderr, "FAIL the platform stopped its boot at stage %d: %s\n", static_cast<int>(stage),
                     half.console().c_str());
        return 2;
    }
    const std::vector<twin::Stimulus> stim = twin::scenario();
    std::size_t next = 0;
    while (half.ms() < twin::kRunMs) millisecond(half, stim, &next, &cap);
    half.capture(nullptr);
    if (!planted.empty() && !plant(planted, &cap)) {
        std::fprintf(stderr, "FAIL the plant %s found nothing to plant\n", planted.c_str());
        return 2;
    }
    if (!planted.empty()) cap.notes.push_back({"plant", planted});
    dut->final();
    if (!cap.write(argv[1])) {
        std::fprintf(stderr, "FAIL the capture %s was not written\n", argv[1]);
        return 2;
    }
    std::printf("split half: %zu control frames, %llu stream frames, %u host timeouts, %u ms%s%s\n",
                cap.frames.size(), static_cast<unsigned long long>(cap.stream_frames), half.host_timeouts(),
                twin::kRunMs, planted.empty() ? "" : ", planted ", planted.c_str());
    return half.host_timeouts() == 0 ? 0 : 1;
}

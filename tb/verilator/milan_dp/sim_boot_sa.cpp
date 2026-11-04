// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// Issue #839: from reset, through the firmware's own boot order, every frame
// that leaves the MAC boundary carries the station MAC as its source
// address (IEEE 802.1AC-2016 11.1 and IEEE 802.1Q-2022 6.8.1: source_address
// is the individual address of the source MSAP). The defect this leg
// reproduces: the processor's SRP engine runs from reset, the firmware
// writes the station MAC only in configure_fabric(), and the first MSRP PDU
// of every boot left with 00:00:00:00:00:00.
//
// Boot: reset, then a BIOS window with no CSR access (the engines are live,
// the firmware has not run), then milan_init()'s four stages in the order
// gen_boot_fw.py read out of milan_init() itself:
//   configure_fabric()  the firmware's own code (boot_fw.c, copied out of
//                       milan_baremetal.c), every CSR load and store through
//                       this harness's AXI4-Lite master, its words the
//                       generated constants of the shipping 1x1 config
//   load_aem_image()    no CSR access; the builder's AEM image for the same
//                       config is served on the descriptor face from reset
//   nvm_boot()          stood in for by the step it ends with on blank
//                       media, PP_CTRL[1] starting the restore walk, which
//                       proves the image and ends COMPLETE. Its saved-state
//                       CSR traffic is not modelled (NVM faces idle)
//   entity_advertise(1) the firmware's own code
// Then the run continues past the first ENTITY_AVAILABLE to its re-advertise,
// and a controller asks one AECP and one ACMP question and opens the AAF
// talker through the documented AAF_CTRL[1] diagnostic bypass, so the
// processor's AECP and ACMP answers and an AAF stream are on the wire too.
//
// Then the pair's sequencing, in an order the firmware does not use: two
// further resets, each writing one half of the station MAC alone and then,
// 300 processor ms later, the other. One half alone must open no
// CSR-addressed transmitter, whichever half it is, and the second half must
// release the frame the processor built meanwhile with the whole address.
//
// Elaboration: the gptp leg's (shipping 1x1 entity, fabric gPTP on, 2 MHz
// fabric clock, one processor millisecond = 100 cycles), with this leg's
// gPTP program generated for the same station MAC. The MAC accepts every
// beat (tready 1), the link is up, the peer answers nothing but the two
// controller questions. Every frame is collected on valid/ready at
// m_axis_mac_tx and graded; nothing about the DUT is written but its CSRs.
//
// Usage: Vmilan_dp_bootsa [aem image]. The image defaults to aemi.bin beside
// the executable, where the Makefile writes it. Exit 0 only when every check
// passes.

#include "../../common/verilator_harness.hpp"
#include "../../common/gptp_launch_observer.hpp"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include "boot_fw.h"
#include <verilated.h>

#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <deque>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <vector>

#ifndef PP_MS_CYC_TB
#error "Makefile must couple PP_MS_CYC_TB to GPP_TIM_DIV_MS_P"
#endif

extern "C" {
uint32_t boot_fw_csr_read(unsigned int offset);
void boot_fw_csr_write(unsigned int offset, uint32_t value);
void boot_fw_configure_fabric(void);
void boot_fw_entity_advertise(int verified);
}

namespace {

constexpr uint64_t kMsCyc = PP_MS_CYC_TB;   //! one processor millisecond
constexpr unsigned kPhcTickNs = 8;
//! The BIOS window: reset release to milan_init(). Long enough for the SRP
//! engine to offer its first MRPDU (its join timer is 200 ms, Milan v1.2
//! Table 4.3), which is the frame the defect sent with a zero address; the
//! check below that the processor offered a frame inside it keeps this leg
//! from passing on a boot that never reached the defect.
constexpr uint64_t kBiosMs = 400;
//! ENTITY_AVAILABLE waits T-ADP-DELAY-START, up to 2000 ms (Milan v1.2
//! 5.6.3.5.2); the bound adds the restore walk and slack
constexpr uint64_t kAdvertiseBoundMs = 3000;
//! The run past the first ENTITY_AVAILABLE ends once the entity has
//! re-advertised (every 5000 processor ms, the processor's ADP_T_ADV_MS_C),
//! the gPTP plane has sent and the AAF talker has streamed. gPTP and MAAP
//! keep the fabric clock's own time (2 MHz here), so this bound is in
//! cycles: 2.5 s of their time, past MAAP's probe retransmits (IEEE
//! 1722-2016 Table B.8) and the 1 s Pdelay interval.
constexpr uint64_t kPastBoundCyc = 5000000;
constexpr uint64_t kControllerMac = 0x0080E1112233ULL;
constexpr uint64_t kControllerId = 0x0080E1FFFE112233ULL;
constexpr uint64_t kAcmpDa = 0x91E0F0010000ULL;

uint64_t be(const std::vector<uint8_t>& b, size_t off, size_t n) {
    if (off + n > b.size()) return UINT64_MAX;
    uint64_t v = 0;
    for (size_t i = 0; i < n; ++i) v = (v << 8) | b[off + i];
    return v;
}

struct Frame {
    std::vector<uint8_t> b;
    void u8(uint8_t v) { b.push_back(v); }
    void u16(uint16_t v) { u8(static_cast<uint8_t>(v >> 8)); u8(static_cast<uint8_t>(v)); }
    void u32(uint32_t v) { u16(static_cast<uint16_t>(v >> 16)); u16(static_cast<uint16_t>(v)); }
    void u48(uint64_t v) { u16(static_cast<uint16_t>(v >> 32)); u32(static_cast<uint32_t>(v)); }
    void u64(uint64_t v) { u32(static_cast<uint32_t>(v >> 32)); u32(static_cast<uint32_t>(v)); }
};

//! The transmitter a frame came from, read off its EtherType and subtype.
enum class Kind { Msrp, Mvrp, Gptp, Adp, Aecp, Acmp, Maap, Aaf, Crf, Other };
constexpr std::array<const char*, 10> kKindName = {
    "MSRP", "MVRP", "gPTP", "ADP", "AECP", "ACMP", "MAAP", "AAF", "CRF", "other"};

Kind classify(const std::vector<uint8_t>& f) {
    size_t et = 12;
    if (be(f, et, 2) == 0x8100) et += 4;
    switch (be(f, et, 2)) {
    case 0x22EA: return Kind::Msrp;
    case 0x88F5: return Kind::Mvrp;
    case 0x88F7: return Kind::Gptp;
    case 0x22F0:
        switch (f.size() > et + 2 ? f[et + 2] : 0xFF) {
        case 0xFA: return Kind::Adp;
        case 0xFB: return Kind::Aecp;
        case 0xFC: return Kind::Acmp;
        case 0xFE: return Kind::Maap;
        case 0x02: return Kind::Aaf;
        case 0x04: return Kind::Crf;
        default: return Kind::Other;
        }
    default: return Kind::Other;
    }
}

//! The destination address a frame of `kind` must carry, or 0 where it is
//! the stream's own: the stamp rewrites octets 6 to 11 and no other, so the
//! octets before them must still be the protocol's (IEEE 802.1Q-2022 Table
//! 10-1 for MRP, IEEE 802.1AS-2011 10.4.3 for gPTP, IEEE 1722.1-2021
//! Annex B for ADP and ACMP, IEEE 1722-2016 Table B.10 for MAAP).
uint64_t protocol_da(Kind kind) {
    switch (kind) {
    case Kind::Msrp: return 0x0180C200000EULL;
    case Kind::Mvrp: return 0x0180C2000021ULL;
    case Kind::Gptp: return 0x0180C200000EULL;
    case Kind::Adp:
    case Kind::Acmp: return 0x91E0F0010000ULL;
    case Kind::Maap: return 0x91E0F000FF00ULL;
    default: return 0;
    }
}

//! One frame the DUT sent, where and when.
struct Sent {
    uint64_t cyc = 0;
    Kind kind = Kind::Other;
    uint64_t da = 0;
    uint64_t sa = 0;
    bool before_mac = false;     //! left before configure_fabric() wrote the MAC
    uint8_t adp_msg = 0xFF;      //! ADP message_type, for ADPDUs
};

class BootSaHarness {
 public:
    explicit BootSaHarness(std::vector<uint8_t> image) : descriptor_(std::move(image)) {
        check_.echo_passes();
    }
    int run();
    uint32_t csr_read(unsigned int offset) { return read(static_cast<uint16_t>(offset)); }
    void csr_write(unsigned int offset, uint32_t value) {
        write(static_cast<uint16_t>(offset), value);
        const bool before = wrote_lo_ && wrote_hi_;
        if (offset == 0x108) wrote_lo_ = true;
        if (offset == 0x10C) wrote_hi_ = true;
        if (!before && wrote_lo_ && wrote_hi_)
            printf("[BOOTSA] configure_fabric() completed the station MAC at cycle %llu\n",
                   static_cast<unsigned long long>(cyc_));
    }

 private:
    milan::tb::Model<Vmilan_datapath> model_;
    Vmilan_datapath* dut_ = model_.get();
    milan::tb::Checker check_{"bootsa"};
    std::vector<uint8_t> descriptor_;
    milan::tb::GptpLaunchObserver observer_{kPhcTickNs};
    uint64_t cyc_ = 0;
    bool wrote_lo_ = false;
    bool wrote_hi_ = false;
    bool pp_offered_early_ = false;      //! the processor offered a frame in the BIOS window
    struct { bool aw, w, b, ar, r; uint32_t data; } fires_{};

    std::vector<uint8_t> tx_cur_;
    std::vector<Sent> sent_;
    std::vector<std::vector<uint8_t>> frames_;
    std::deque<std::vector<uint8_t>> rx_queue_;
    std::vector<uint8_t> rx_;
    size_t rx_off_ = 0;
    bool rx_busy_ = false;

    std::array<uint8_t, 592> rmem_{};
    bool rm_busy_ = false, rm_done_ = false;
    uint32_t rm_addr_ = 0;
    unsigned rm_left_ = 0;
    bool dm_busy_ = false;
    uint32_t dm_addr_ = 0;
    unsigned dm_left_ = 0, dm_wait_ = 0, drp_lat_ = 0;

    uint64_t phc_ns() const {
        const auto& acc = dut_->rootp->milan_datapath__DOT__ts_counter__DOT__acc;
        return (static_cast<uint64_t>(acc[2]) << 40) | (static_cast<uint64_t>(acc[1]) << 8)
             | (acc[0] >> 24);
    }
    void tick();
    void run_cycles(uint64_t n) { while (n--) tick(); }
    void memory_drive();
    void memory_edge();
    void rx_drive();
    void tx_edge();
    void write(uint16_t addr, uint32_t value);
    uint32_t read(uint16_t addr);
    void reset();
    void pair_order(uint16_t first, uint16_t second, const char* tag);
    void bios_window();
    void run_stage(const std::string& stage);
    size_t first_entity_available(size_t from) const;
    std::vector<uint8_t> await(Kind kind, size_t from, uint64_t bound_cyc,
                               uint8_t message_type);
    void controller();
    void grade();
};

BootSaHarness* g_harness = nullptr;

void BootSaHarness::tick() {
    rx_drive();
    dut_->axis_clk = 0; dut_->gtx_clk = 0;
    memory_drive();
    dut_->eval();
    const bool rx_fire = dut_->s_axis_mac_rx_tvalid && dut_->s_axis_mac_rx_tready;
    fires_.aw = dut_->s_axi_awvalid && dut_->s_axi_awready;
    fires_.w = dut_->s_axi_wvalid && dut_->s_axi_wready;
    fires_.b = dut_->s_axi_bvalid && dut_->s_axi_bready;
    fires_.ar = dut_->s_axi_arvalid && dut_->s_axi_arready;
    fires_.r = dut_->s_axi_rvalid && dut_->s_axi_rready;
    fires_.data = dut_->s_axi_rdata;
    if (!(wrote_lo_ && wrote_hi_) && dut_->rootp->milan_datapath__DOT__pp_shadow__DOT__txp_valid_r)
        pp_offered_early_ = true;
    tx_edge();
    observer_.edge(dut_, cyc_, phc_ns());
    dut_->i_mmcm_drp_rdy = 0;
    if (drp_lat_ && --drp_lat_ == 0) dut_->i_mmcm_drp_rdy = 1;
    if (dut_->o_mmcm_drp_en) drp_lat_ = 3;
    memory_edge();
    dut_->axis_clk = 1; dut_->gtx_clk = 1;
    dut_->eval();
    if (rx_fire) {
        rx_off_ += 8;
        if (rx_off_ >= rx_.size()) rx_busy_ = false;
    }
    ++cyc_;
}

void BootSaHarness::memory_drive() {
    uint64_t data = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = rm_addr_ - 0x20100000u + i;
        data = (data << 8) | (off < rmem_.size() ? rmem_[off] : 0);
    }
    dut_->i_resp_mem_req_ready = !rm_busy_;
    dut_->i_resp_mem_rsp_valid = rm_busy_;
    dut_->i_resp_mem_rsp_data = data;
    dut_->i_resp_mem_rsp_last = rm_busy_ && rm_left_ == 1;
    dut_->i_resp_mem_rsp_err = 0;
    dut_->i_resp_mem_wr_ready = !rm_done_;
    dut_->i_resp_mem_wr_done = rm_done_;
    dut_->i_resp_mem_wr_err = 0;
    uint64_t desc = 0;
    for (unsigned i = 0; i < 8; ++i) {
        const uint32_t off = dm_addr_ - 0x20000000u + i;
        desc = (desc << 8) | (off < descriptor_.size() ? descriptor_[off] : 0);
    }
    dut_->i_desc_mem_req_ready = !dm_busy_;
    dut_->i_desc_mem_rsp_valid = dm_busy_ && dm_wait_ == 0;
    dut_->i_desc_mem_rsp_data = desc;
    dut_->i_desc_mem_rsp_last = dm_busy_ && dm_left_ == 1;
    dut_->i_desc_mem_rsp_err = 0;
}

void BootSaHarness::memory_edge() {
    if (rm_busy_ && dut_->o_resp_mem_rsp_ready) {
        rm_addr_ += 8;
        if (--rm_left_ == 0) rm_busy_ = false;
    } else if (!rm_busy_ && dut_->o_resp_mem_req_valid) {
        rm_addr_ = dut_->o_resp_mem_req_addr;
        rm_left_ = dut_->o_resp_mem_req_beats;
        rm_busy_ = rm_left_ != 0;
    }
    if (rm_done_) rm_done_ = false;
    else if (dut_->o_resp_mem_wr_valid) {
        for (unsigned i = 0; i < 8; ++i) {
            const uint32_t off = dut_->o_resp_mem_wr_addr - 0x20100000u + i;
            if (off < rmem_.size() && (dut_->o_resp_mem_wr_strb & (1u << i)))
                rmem_[off] = static_cast<uint8_t>(dut_->o_resp_mem_wr_data >> (56 - 8 * i));
        }
        rm_done_ = true;
    }
    if (!dm_busy_ && dut_->o_desc_mem_req_valid) {
        dm_addr_ = dut_->o_desc_mem_req_addr;
        dm_left_ = dut_->o_desc_mem_req_beats;
        dm_busy_ = dm_left_ != 0;
        dm_wait_ = 12;
    } else if (dm_busy_ && dm_wait_) {
        --dm_wait_;
    } else if (dm_busy_ && dut_->o_desc_mem_rsp_ready) {
        dm_addr_ += 8;
        if (--dm_left_ == 0) dm_busy_ = false;
    }
}

void BootSaHarness::rx_drive() {
    if (!rx_busy_ && !rx_queue_.empty()) {
        rx_ = std::move(rx_queue_.front());
        rx_queue_.pop_front();
        rx_off_ = 0;
        rx_busy_ = true;
    }
    dut_->s_axis_mac_rx_tvalid = rx_busy_;
    dut_->s_axis_mac_rx_tlast = rx_busy_ && rx_off_ + 8 >= rx_.size();
    uint64_t data = 0;
    uint8_t keep = 0;
    for (size_t i = 0; rx_busy_ && i < 8 && rx_off_ + i < rx_.size(); ++i) {
        data |= static_cast<uint64_t>(rx_[rx_off_ + i]) << (8 * i);
        keep = static_cast<uint8_t>(keep | (1u << i));
    }
    dut_->s_axis_mac_rx_tdata = data;
    dut_->s_axis_mac_rx_tkeep = keep;
}

//! The MAC accepts every beat; a frame is its accepted beats' kept octets.
void BootSaHarness::tx_edge() {
    if (!(dut_->m_axis_mac_tx_tvalid && dut_->m_axis_mac_tx_tready)) return;
    for (unsigned i = 0; i < 8; ++i)
        if (dut_->m_axis_mac_tx_tkeep & (1u << i))
            tx_cur_.push_back(static_cast<uint8_t>(dut_->m_axis_mac_tx_tdata >> (8 * i)));
    if (!dut_->m_axis_mac_tx_tlast) return;
    observer_.offer(tx_cur_, cyc_);
    Sent s;
    s.cyc = cyc_;
    s.kind = classify(tx_cur_);
    s.da = be(tx_cur_, 0, 6);
    s.sa = be(tx_cur_, 6, 6);
    s.before_mac = !(wrote_lo_ && wrote_hi_);
    if (s.kind == Kind::Adp && tx_cur_.size() > 15) s.adp_msg = tx_cur_[15] & 0xF;
    sent_.push_back(s);
    frames_.push_back(tx_cur_);
    tx_cur_.clear();
}

void BootSaHarness::write(uint16_t addr, uint32_t value) {
    dut_->s_axi_awaddr = addr; dut_->s_axi_awvalid = 1;
    dut_->s_axi_wdata = value; dut_->s_axi_wstrb = 0xF; dut_->s_axi_wvalid = 1;
    dut_->s_axi_bready = 1;
    for (unsigned g = 0; g < 2048; ++g) {
        tick();
        if (fires_.aw) dut_->s_axi_awvalid = 0;
        if (fires_.w) dut_->s_axi_wvalid = 0;
        if (fires_.b) { dut_->s_axi_bready = 0; return; }
    }
    throw std::runtime_error("AXI write response timeout");
}

uint32_t BootSaHarness::read(uint16_t addr) {
    dut_->s_axi_araddr = addr; dut_->s_axi_arvalid = 1; dut_->s_axi_rready = 1;
    for (unsigned g = 0; g < 2048; ++g) {
        tick();
        if (fires_.ar) dut_->s_axi_arvalid = 0;
        if (fires_.r) { dut_->s_axi_rready = 0; return fires_.data; }
    }
    throw std::runtime_error("AXI read response timeout");
}

void BootSaHarness::reset() {
    dut_->axis_resetn = 0; dut_->gtx_resetn = 0;
    dut_->s_axi_awvalid = 0; dut_->s_axi_wvalid = 0; dut_->s_axi_arvalid = 0;
    dut_->s_axi_bready = 0; dut_->s_axi_rready = 0;
    dut_->m_axis_mac_tx_tready = 1;
    dut_->i_mac_speed = 2; dut_->i_link_up = 1; dut_->i_full_duplex = 1;
    dut_->i_mac_events = 0;
    dut_->i_mmcm_locked = 1;
    dut_->i_mmcm_ps_done = 0; dut_->i_mmcm_drp_rdy = 0; dut_->i_mmcm_drp_do = 0;
    dut_->i2s_sdout_i = 0; dut_->tdm_data_i = 0;
    dut_->tdm_bclk_i = 0; dut_->tdm_fsync_i = 0;
    dut_->clk_audio_i = 0; dut_->clk_tdm_i = 0;
    milan::tb::GptpLaunchObserver::tie_off(dut_);
    observer_.reset();
    rx_queue_.clear();
    rx_busy_ = false;
    rm_busy_ = rm_done_ = dm_busy_ = false;
    rm_left_ = dm_left_ = dm_wait_ = drp_lat_ = 0;
    wrote_lo_ = wrote_hi_ = false;
    run_cycles(64);
    dut_->axis_resetn = 1; dut_->gtx_resetn = 1;
}

//! One reset, then `first` alone, then `second`: the pair must be complete
//! before any CSR-addressed transmitter starts, in either order.
void BootSaHarness::pair_order(uint16_t first, uint16_t second, const char* tag) {
    reset();
    const size_t from = sent_.size();
    run_cycles(300 * kMsCyc);
    write(first, first == 0x108 ? kStationMacLo : kStationMacHi);
    run_cycles(300 * kMsCyc);
    auto csr_addressed = [this](size_t at) {
        size_t n = 0;
        for (size_t i = at; i < sent_.size(); ++i) n += sent_[i].kind != Kind::Gptp;
        return n;
    };
    std::string what = std::string("[BOOTSA] pair: ") + tag + " alone opens no CSR-addressed transmitter";
    check_.dec(what.c_str(), csr_addressed(from), 0);
    const size_t released = sent_.size();
    write(second, second == 0x108 ? kStationMacLo : kStationMacHi);
    const uint64_t end = cyc_ + 100 * kMsCyc;
    while (cyc_ < end && csr_addressed(released) == 0) tick();
    what = std::string("[BOOTSA] pair: the second half after ") + tag + " releases the processor's frame";
    check_.that(what.c_str(), csr_addressed(released) > 0);
    uint64_t wrong = 0;
    for (size_t i = from; i < sent_.size(); ++i) wrong += sent_[i].sa != kStationMac;
    what = std::string("[BOOTSA] pair: every frame of the ") + tag + " boot carries the station MAC";
    check_.dec(what.c_str(), wrong, 0);
}

//! Reset release to milan_init(): the engines run, nothing touches a CSR.
void BootSaHarness::bios_window() {
    printf("[BOOTSA] BIOS window: %llu processor ms with no CSR access\n",
           static_cast<unsigned long long>(kBiosMs));
    run_cycles(kBiosMs * kMsCyc);
}

void BootSaHarness::run_stage(const std::string& stage) {
    printf("[BOOTSA] milan_init(): %s()\n", stage.c_str());
    if (stage == "configure_fabric") {
        boot_fw_configure_fabric();
    } else if (stage == "load_aem_image") {
        // no CSR access: the image is on the descriptor face from reset
    } else if (stage == "nvm_boot") {
        constexpr uint16_t kPpCtrl = 0x920;
        constexpr uint16_t kPpStat = 0x924;
        constexpr uint32_t kDone = 1u << 2;
        constexpr uint32_t kClosed = 1u << 16;
        write(kPpCtrl, read(kPpCtrl) | 0x2u);
        uint32_t stat = 0;
        for (unsigned r = 0; r < 400 && !(stat & (kDone | kClosed)); ++r) {
            run_cycles(64);
            stat = read(kPpStat);
        }
        check_.hex("[BOOTSA] nvm_boot(): the restore walk ends COMPLETE (done 1, CLOSED 0)",
                   stat & (kDone | kClosed), kDone);
    } else if (stage == "entity_advertise") {
        boot_fw_entity_advertise(1);
    } else {
        throw std::runtime_error("milan_init() calls a stage this leg cannot run: " + stage);
    }
}

size_t BootSaHarness::first_entity_available(size_t from) const {
    for (size_t i = from; i < sent_.size(); ++i)
        if (sent_[i].kind == Kind::Adp && sent_[i].adp_msg == 0) return i;
    return SIZE_MAX;
}

//! The first frame of `kind` (and, for AECP and ACMP, of `message_type`)
//! from frames_[from] on, or empty when none leaves within `bound_cyc`.
std::vector<uint8_t> BootSaHarness::await(Kind kind, size_t from, uint64_t bound_cyc,
                                          uint8_t message_type) {
    const uint64_t end = cyc_ + bound_cyc;
    while (cyc_ < end) {
        tick();
        for (size_t i = from; i < sent_.size(); ++i)
            if (sent_[i].kind == kind && frames_[i].size() > 15
                    && (frames_[i][15] & 0xF) == message_type)
                return frames_[i];
    }
    return {};
}

//! Past the first ENTITY_AVAILABLE: one AECP command (READ_DESCRIPTOR of
//! the ENTITY, IEEE 1722.1-2021 7.4.5), one ACMP command
//! (GET_TX_STATE_COMMAND, IEEE 1722.1-2021 8.2.1.5) and the AAF talker
//! opened by the AAF_CTRL[1] bypass, so those three transmitters send too.
void BootSaHarness::controller() {
    Frame a;
    a.u48(kStationMac); a.u48(kControllerMac); a.u16(0x22F0);
    a.u8(0xFB); a.u8(0x00); a.u16(20);
    a.u64(kEntityId); a.u64(kControllerId);
    a.u16(0x4001); a.u16(0x0004);
    a.u16(0); a.u16(0); a.u16(0); a.u16(0);   // configuration 0, ENTITY 0
    while (a.b.size() < 60) a.u8(0);
    size_t from = sent_.size();
    rx_queue_.push_back(a.b);
    const auto aecp = await(Kind::Aecp, from, 400 * kMsCyc, 1);
    check_.that("[BOOTSA] the processor answers READ_DESCRIPTOR (an AECP frame leaves)",
                !aecp.empty());

    Frame c;
    c.u48(kAcmpDa); c.u48(kControllerMac); c.u16(0x22F0);
    c.u8(0xFC); c.u8(0x04); c.u16(44);
    c.u64(0);                                   // stream_id
    c.u64(kControllerId); c.u64(kEntityId); c.u64(0);
    c.u16(0); c.u16(0);                         // talker / listener unique id
    c.u48(0); c.u16(0); c.u16(0x5001); c.u16(0); c.u16(0); c.u16(0);
    while (c.b.size() < 60) c.u8(0);
    from = sent_.size();
    rx_queue_.push_back(c.b);
    const auto acmp = await(Kind::Acmp, from, 400 * kMsCyc, 5);
    check_.that("[BOOTSA] the processor answers GET_TX_STATE_COMMAND (an ACMP frame leaves)",
                !acmp.empty());

    write(0x654, read(0x654) | 0x2u);
}

void BootSaHarness::grade() {
    std::array<uint64_t, kKindName.size()> seen{}, wrong{}, wrong_da{};
    uint64_t zero = 0, early_csr = 0;
    size_t first_bad = SIZE_MAX;
    for (size_t i = 0; i < sent_.size(); ++i) {
        const Sent& s = sent_[i];
        const auto k = static_cast<size_t>(s.kind);
        ++seen[k];
        if (s.sa == 0) ++zero;
        if (s.sa != kStationMac) {
            ++wrong[k];
            if (first_bad == SIZE_MAX) first_bad = i;
        }
        if (s.before_mac && s.kind != Kind::Gptp) ++early_csr;
        const uint64_t da = s.kind == Kind::Aecp ? kControllerMac : protocol_da(s.kind);
        if (da != 0 && s.da != da) ++wrong_da[k];
    }
    printf("[BOOTSA] %zu frames:", sent_.size());
    for (size_t k = 0; k < kKindName.size(); ++k)
        if (seen[k]) printf(" %s %llu", kKindName[k], static_cast<unsigned long long>(seen[k]));
    printf("\n");
    std::array<unsigned, kKindName.size()> shown{};
    for (size_t i = 0; i < sent_.size(); ++i) {
        const Sent& s = sent_[i];
        if (shown[static_cast<size_t>(s.kind)]++ >= 2) continue;
        printf("[BOOTSA]   #%zu %-5s cycle %8llu source %012llx%s\n", i,
               kKindName[static_cast<size_t>(s.kind)], static_cast<unsigned long long>(s.cyc),
               static_cast<unsigned long long>(s.sa), s.before_mac ? " (before the MAC write)" : "");
    }
    if (first_bad != SIZE_MAX) {
        const Sent& s = sent_[first_bad];
        printf("[BOOTSA] first frame not from the station MAC: #%zu %s at cycle %llu, "
               "source %012llx, %s the station MAC was written\n", first_bad,
               kKindName[static_cast<size_t>(s.kind)], static_cast<unsigned long long>(s.cyc),
               static_cast<unsigned long long>(s.sa), s.before_mac ? "before" : "after");
    }
    check_.that("[BOOTSA] the processor offered a frame before the station MAC was written",
                pp_offered_early_);
    check_.dec("[BOOTSA] no frame carries the all-zero source address", zero, 0);
    check_.dec("[BOOTSA] no CSR-addressed transmitter starts a frame before the station MAC is written",
               early_csr, 0);
    for (const Kind k : {Kind::Msrp, Kind::Mvrp, Kind::Gptp, Kind::Adp, Kind::Aecp,
                         Kind::Acmp, Kind::Maap, Kind::Aaf, Kind::Crf, Kind::Other}) {
        const auto i = static_cast<size_t>(k);
        const std::string what = std::string("[BOOTSA] every ") + kKindName[i]
            + " frame's source address is the station MAC";
        check_.dec(what.c_str(), wrong[i], 0);
    }
    for (const Kind k : {Kind::Msrp, Kind::Mvrp, Kind::Gptp, Kind::Adp, Kind::Aecp,
                         Kind::Acmp, Kind::Maap}) {
        const auto i = static_cast<size_t>(k);
        const std::string what = std::string("[BOOTSA] every ") + kKindName[i]
            + " frame's destination address is its protocol's (octets 0 to 5 untouched)";
        check_.dec(what.c_str(), wrong_da[i], 0);
    }
    check_.dec("[BOOTSA] every frame is a known protocol's (octets 12 and 13 untouched)",
               seen[static_cast<size_t>(Kind::Other)], 0);
    for (const Kind k : {Kind::Msrp, Kind::Gptp, Kind::Adp, Kind::Aecp, Kind::Acmp,
                         Kind::Maap, Kind::Aaf}) {
        const auto i = static_cast<size_t>(k);
        const std::string what = std::string("[BOOTSA] ") + kKindName[i]
            + " frames were sent and graded";
        check_.that(what.c_str(), seen[i] > 0);
    }
    const uint32_t diag = read(0x784);
    check_.hex("[BOOTSA] A_TXARB_DIAG: no arbiter stall or abort since reset",
               (diag >> 8) & 0xFFFF, 0);
}

int BootSaHarness::run() {
    printf("bootsa: 2 MHz fabric, one processor ms = %llu cycles, station MAC %012llx\n",
           static_cast<unsigned long long>(kMsCyc), static_cast<unsigned long long>(kStationMac));
    try {
        reset();
        bios_window();
        for (const char* stage : kBootStages) run_stage(stage);
        const size_t advertise_from = sent_.size();
        const uint64_t end = cyc_ + kAdvertiseBoundMs * kMsCyc;
        while (cyc_ < end && first_entity_available(advertise_from) == SIZE_MAX) tick();
        const size_t first = first_entity_available(advertise_from);
        check_.that("[BOOTSA] the first ENTITY_AVAILABLE leaves after entity_advertise()",
                    first != SIZE_MAX);
        if (first != SIZE_MAX)
            printf("[BOOTSA] first ENTITY_AVAILABLE at cycle %llu, frame #%zu\n",
                   static_cast<unsigned long long>(sent_[first].cyc), first);
        controller();
        const uint64_t past = cyc_ + kPastBoundCyc;
        auto sent = [this](Kind k) {
            for (const Sent& s : sent_) if (s.kind == k) return true;
            return false;
        };
        while (cyc_ < past && !(sent(Kind::Gptp) && sent(Kind::Aaf)
                                && first != SIZE_MAX
                                && first_entity_available(first + 1) != SIZE_MAX))
            tick();
        check_.that("[BOOTSA] the entity re-advertises past the first ENTITY_AVAILABLE",
                    first != SIZE_MAX && first_entity_available(first + 1) != SIZE_MAX);
        grade();
        pair_order(0x108, 0x10C, "MAC_ADDR_LO");
        pair_order(0x10C, 0x108, "MAC_ADDR_HI");
    } catch (const std::exception& e) {
        check_.fail(e.what());
    }
    printf("simulated_cycles=%llu\n", static_cast<unsigned long long>(cyc_));
    return check_.report();
}

}  // namespace

extern "C" uint32_t boot_fw_csr_read(unsigned int offset) {
    return g_harness->csr_read(offset);
}

extern "C" void boot_fw_csr_write(unsigned int offset, uint32_t value) {
    g_harness->csr_write(offset, value);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    setvbuf(stdout, nullptr, _IOLBF, 0);
    if (argc > 2) {
        fprintf(stderr, "usage: %s [aem image]\n", argv[0]);
        return 2;
    }
    std::string path = argc == 2 ? std::string(argv[1]) : std::string(argv[0]);
    if (argc < 2) {
        const size_t slash = path.rfind('/');
        path = (slash == std::string::npos ? std::string(".") : path.substr(0, slash))
             + "/aemi.bin";
    }
    std::ifstream file(path, std::ios::binary);
    std::vector<uint8_t> image{std::istreambuf_iterator<char>(file),
                               std::istreambuf_iterator<char>()};
    if (image.empty()) {
        fprintf(stderr, "bootsa: the AEM image %s is missing or empty\n", path.c_str());
        return 2;
    }
    BootSaHarness harness(std::move(image));
    g_harness = &harness;
    return harness.run();
}

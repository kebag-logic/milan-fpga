// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// sim_link_reset.cpp - #972: from reset, the split datapath transmits nothing
// until the firmware publishes the PHY's verified link, at the shipping shape
// it is elaborated for (1x1/1if or 8x8/1if), with the PHY's link retained.
//
// Boundary: milan_datapath at CTRL_SPLIT_P = 1, the gPTP plane at its product
// default (on), the MAC's transmit stream taken every cycle. Its i_link_up and
// i_full_duplex are the SoC's link-status word, milan_mac_link_status, as
// milan_soc.py's MilanMAC builds it: a sys register at the reset --word-reset
// names (the Makefile reads it from sw/litex/mac_link_status.py, the split's
// with an MDIO pair), its link and duplex bits crossed into the datapath clock
// by two flops each (MultiReg, its flops at 0 from configuration). One clock
// stands in for sys and the datapath's.
//
// The firmware's boot before its PHY poll arms is its own code: ctrl_plat.c's
// identity check and CSR policy (ctrl_plat_csr.c, built for the host with the
// shape's generated policy), each access an AXI4-Lite transaction on the
// datapath's CSR window, at --boot-ms. They program the station address and
// the fabric's media policy, as the firmware does before its PHY poll arms.
// The firmware's publication is a write of the word, link up at 1000 Mb/s full
// duplex as the PHY poll publishes the shipping PHY's, at --publish-ms.
//
// The PHY's link is retained: its receive and transmit clock toggles run from
// the first cycle, as after a reload that kept the link, so the link guard's
// estimate qualifies and LINK_CTRL[0] keeps its reset, 1. Each run is a fresh
// model, a configuration reload:
//   --publish-ms T  the firmware publishes at T: no frame crosses the MAC
//                   boundary before the publication has crossed, and the gPTP
//                   plane's frames follow it within the window, so transmit
//                   admission is observed, not assumed
//   --publish-ms 0  nothing ever publishes and no policy is written, as on a
//                   boot refused at the CSR identity check, before the PHY poll
//                   arms: no frame in the window
// Probes, read only (linkreset_probes.vlt): eff_link_w, which the gPTP plane's
// port enable and o_ctl_link_up (the mailbox's LINK level, which the split's
// firmware MAAP, ADP and SRP follow) both are, the split building no KL_maap;
// cfg_sw_link (LINK_CTRL[0]) and linkg_est_w (the guard's estimate).
// The MAC behind the boundary is the shared launch observer
// (gptp_launch_observer.hpp), the SoC's KL_gptp_gmii_launch interface, without
// which the plane never unseals. The gPTP plane's timebase is compressed as
// the gptp leg's is (MILAN_CLK_FREQ_HZ in the Makefile, the PHC at 8 ns a
// cycle, written to PTP_INCR at reset in every run).
// Omitted: LiteEth, the PHY, the CPU and the rest of its firmware, the mailbox.

#include "../../common/verilator_harness.hpp"
#include "../../common/gptp_launch_observer.hpp"
#include "ctrl_plat_csr.h"
#include "ctrl_plat_io.h"
#include "ctrl_plat_policy_gen.h"
#include "Vmilan_datapath.h"
#include "Vmilan_datapath___024root.h"
#include <verilated.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#ifndef LINKRESET_POINT
#error "LINKRESET_POINT: the shape this model is elaborated at, 1 (1x1/1if) or 8 (8x8/1if), from the Makefile"
#endif
#define LINKRESET_SHAPE (LINKRESET_POINT == 8 ? "8x8/1if" : "1x1/1if")
#ifndef LINKRESET_CLK_HZ
#error "LINKRESET_CLK_HZ: the model's MILAN_CLK_FREQ_HZ (the Makefile's)"
#endif

namespace {

constexpr std::uint32_t kLinkUp = 1u, kFullDuplex = 1u << 3;
constexpr std::uint32_t kPublished = 13u;   // link up, 1000 Mb/s, full duplex: the poll's word for the shipping PHY
constexpr std::uint64_t kCyclesPerMs = LINKRESET_CLK_HZ / 1000u;
constexpr unsigned kPhcTickNs = 8;   // the PHC's advance a cycle, GPTP_PHC_TICK_NS_P in the Makefile

struct Frame {
    std::uint64_t cycle;
    std::uint16_t ethertype;
    std::size_t bytes;
};

struct Bench {
    milan::tb::Model<Vmilan_datapath> model;
    Vmilan_datapath* dut = model.get();
    std::uint64_t cyc = 0;
    bool phy_clocks = true;
    // the SoC's word in sys, and its two-flop crossings (MultiReg) into the datapath clock
    std::uint32_t word = 0;
    unsigned link_s1 = 0, link_s2 = 0, fd_s1 = 0, fd_s2 = 0;
    std::vector<Frame> frames;
    std::vector<std::uint8_t> cur;
    milan::tb::GptpLaunchObserver observer{kPhcTickNs};
    std::uint64_t phc_ns() const {
        const auto& acc = dut->rootp->milan_datapath__DOT__ts_counter__DOT__acc;
        return (static_cast<std::uint64_t>(acc[2]) << 40) | (static_cast<std::uint64_t>(acc[1]) << 8) | (acc[0] >> 24);
    }
    std::uint64_t eff_first_up = 0, sw_down = 0, est_down = 0, ctl_up_before = 0;
    bool eff_seen_up = false;

    void edge() {
        // the PHY's clocks: alive from the first cycle (the link retained)
        dut->i_ethrx_tgl = phy_clocks ? (cyc >> 1) & 1u : 0u;
        dut->i_ethtx_tgl = phy_clocks ? (cyc >> 1) & 1u : 0u;
        dut->i_ethact_tgl = 0;
        dut->i_link_up = link_s2;
        dut->i_full_duplex = fd_s2;
        dut->m_axis_mac_tx_tready = 1;
        dut->axis_clk = 0; dut->gtx_clk = 0; dut->clk_audio_i = 0; dut->clk_tdm_i = 0; dut->i_ps_clk = 0;
        dut->eval();
        // the transmit beat taken at this rising edge
        const bool take = dut->m_axis_mac_tx_tvalid && dut->m_axis_mac_tx_tready;
        const std::uint64_t data = dut->m_axis_mac_tx_tdata;
        const unsigned keep = dut->m_axis_mac_tx_tkeep;
        const bool last = dut->m_axis_mac_tx_tlast;
        dut->axis_clk = 1; dut->gtx_clk = 1; dut->clk_audio_i = 1; dut->clk_tdm_i = 1; dut->i_ps_clk = 1;
        dut->eval();
        if (take) {
            for (unsigned k = 0; k < 8; ++k) {
                if (keep & (1u << k)) cur.push_back(static_cast<std::uint8_t>(data >> (8 * k)));
            }
            if (last) {
                const std::uint16_t type = cur.size() >= 14 ? static_cast<std::uint16_t>(cur[12] << 8 | cur[13]) : 0;
                frames.push_back({cyc, type, cur.size()});
                observer.offer(cur, cyc);
                cur.clear();
            }
        }
        observer.edge(dut, cyc, phc_ns());
        // the crossings' flops on the same edge (MultiReg's two stages)
        link_s2 = link_s1; link_s1 = word & kLinkUp;
        fd_s2 = fd_s1; fd_s1 = (word & kFullDuplex) != 0u;
        ++cyc;
        observe();
    }

    //! One AXI4-Lite write of the CSR window, address and data offered together, as ctrl_plat_io.h makes it.
    void axi_write(std::uint16_t addr, std::uint32_t value) {
        dut->s_axi_awaddr = addr; dut->s_axi_awvalid = 1;
        dut->s_axi_wdata = value; dut->s_axi_wstrb = 0xF; dut->s_axi_wvalid = 1;
        dut->s_axi_bready = 1;
        bool aw = false, w = false, b = false;
        // the bound covers the CSR defaults sweep after reset, during which the window takes no access
        for (int k = 0; k < 4000 && !b; ++k) {
            dut->eval();
            const bool aw_take = dut->s_axi_awvalid && dut->s_axi_awready;
            const bool w_take = dut->s_axi_wvalid && dut->s_axi_wready;
            const bool b_take = dut->s_axi_bvalid && dut->s_axi_bready;
            edge();
            if (aw_take) { aw = true; dut->s_axi_awvalid = 0; }
            if (w_take) { w = true; dut->s_axi_wvalid = 0; }
            b = b_take;
        }
        if (!(aw && w && b)) { std::printf("FAIL CSR write at 0x%x never answered\n", addr); ++faults; }
    }
    //! One AXI4-Lite read of the CSR window.
    std::uint32_t axi_read(std::uint16_t addr) {
        dut->s_axi_araddr = addr; dut->s_axi_arvalid = 1; dut->s_axi_rready = 1;
        for (int k = 0; k < 4000; ++k) {
            dut->eval();
            const bool ar_take = dut->s_axi_arvalid && dut->s_axi_arready;
            const bool r_take = dut->s_axi_rvalid && dut->s_axi_rready;
            const std::uint32_t data = dut->s_axi_rdata;
            edge();
            if (ar_take) dut->s_axi_arvalid = 0;
            if (r_take) return data;
        }
        std::printf("FAIL CSR read at 0x%x never answered\n", addr);
        ++faults;
        return 0;
    }
    unsigned faults = 0;

    std::uint64_t published_at = 0;   // the publication's cycle, 0 for none
    void observe() {
        const auto* r = dut->rootp;
        const bool eff = r->milan_datapath__DOT__eff_link_w;
        if (eff && !eff_seen_up) { eff_seen_up = true; eff_first_up = cyc; }
        if (!r->milan_datapath__DOT__cfg_sw_link && !sw_down) sw_down = cyc ? cyc : 1;
        if (!r->milan_datapath__DOT__linkg_est_w && !est_down && dut->axis_resetn) est_down = cyc;
        if (dut->o_ctl_link_up && (published_at == 0 || cyc < published_at) && !ctl_up_before) ctl_up_before = cyc;
    }
};

std::uint64_t arg(int argc, char** argv, const char* name, std::uint64_t fallback) {
    for (int k = 1; k + 1 < argc; ++k) {
        if (std::strcmp(argv[k], name) == 0) return std::strtoull(argv[k + 1], nullptr, 0);
    }
    return fallback;
}

Bench* current = nullptr;
//! The CSR window's base in ctrl_plat_io.h's addresses: the window at 0, as the bench passes it.
constexpr std::uintptr_t kCsr = 0;

}  // namespace

// ctrl_plat_io.h: the datapath's CSR window; nothing else is addressed before the PHY poll arms
extern "C" std::uint32_t ctrl_plat_io_read32(std::uintptr_t address) {
    return current->axi_read(static_cast<std::uint16_t>(address - kCsr));
}

extern "C" void ctrl_plat_io_write32(std::uintptr_t address, std::uint32_t value) {
    current->axi_write(static_cast<std::uint16_t>(address - kCsr), value);
}

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);
    const std::uint32_t reset_word = static_cast<std::uint32_t>(arg(argc, argv, "--word-reset", 0x100));
    const std::uint64_t publish_ms = arg(argc, argv, "--publish-ms", 1500);
    const std::uint64_t boot_ms = arg(argc, argv, "--boot-ms", 3);
    const std::uint64_t window_ms = arg(argc, argv, "--window-ms", 1600);
    std::string label = std::string("linkreset ") + LINKRESET_SHAPE + (publish_ms ? " published" : " refused");
    milan::tb::Checker check{label.c_str()};
    if (reset_word > 15u) {
        std::printf("FAIL --word-reset: the word's reset (mac_link_status.py) is required\n");
        return 2;
    }
    Bench b;
    current = &b;
    b.phy_clocks = arg(argc, argv, "--phy-clocks", 1) != 0;
    Vmilan_datapath* dut = b.dut;
    // configuration: every register at its initial value, the word at its reset, the crossings' flops at 0
    b.word = reset_word;
    dut->axis_resetn = 0; dut->gtx_resetn = 0;
    dut->i_mac_speed = 2; dut->i_mmcm_locked = 1;
    dut->s_axi_awvalid = 0; dut->s_axi_wvalid = 0; dut->s_axi_arvalid = 0; dut->s_axi_bready = 1; dut->s_axi_rready = 1;
    dut->s_axis_mac_rx_tvalid = 0;
    milan::tb::GptpLaunchObserver::tie_off(dut);
    const std::uint64_t published_at = publish_ms * kCyclesPerMs;
    b.published_at = published_at;
    for (int k = 0; k < 64; ++k) b.edge();
    dut->axis_resetn = 1; dut->gtx_resetn = 1;
    // the compressed timebase: the PHC at kPhcTickNs a cycle (PTP_INCR, ns in [31:24]), as the gptp leg sets it
    b.axi_write(0x504, kPhcTickNs << 24);
    const std::uint64_t end = window_ms * kCyclesPerMs;
    const std::uint64_t boot_at = boot_ms * kCyclesPerMs;
    bool booted = false, identity = false;
    std::uint64_t policy_done = 0;
    while (b.cyc < end) {
        if (publish_ms != 0 && b.cyc >= published_at && b.word != kPublished) b.word = kPublished;
        if (publish_ms != 0 && !booted && b.cyc >= boot_at) {
            // ctrl_plat_boot's steps before the PHY poll arms: the identity check, then the policy
            booted = true;
            std::uint32_t version = 0;
            identity = ctrl_plat_csr_identity(kCsr, &version);
            const struct ctrl_plat_policy policy = CTRL_PLAT_POLICY_INIT;
            if (identity) ctrl_plat_csr_policy(kCsr, &policy);
            policy_done = b.cyc;
            std::printf("BOOT identity %s VERSION 0x%08x, policy written by %.3f ms\n", identity ? "ok" : "refused",
                        version, static_cast<double>(policy_done) / kCyclesPerMs);
            continue;
        }
        b.edge();
    }
    // the publication's crossing: two flops, then the datapath's own registering of its effective link
    const std::uint64_t crossed = published_at + 2u;
    std::size_t before = 0, after = 0;
    for (const Frame& f : b.frames) (publish_ms == 0 || f.cycle < crossed ? before : after) += 1u;
    std::printf("SHAPE %s word reset %u publish %llu ms window %llu ms (%llu cycles/ms)\n", LINKRESET_SHAPE,
                reset_word, static_cast<unsigned long long>(publish_ms), static_cast<unsigned long long>(window_ms),
                static_cast<unsigned long long>(kCyclesPerMs));
    for (std::size_t k = 0; k < b.frames.size() && k < 6; ++k) {
        std::printf("FRAME %zu at %.3f ms ethertype 0x%04x %zu bytes\n", k,
                    static_cast<double>(b.frames[k].cycle) / kCyclesPerMs, b.frames[k].ethertype, b.frames[k].bytes);
    }
    {
        std::vector<std::pair<std::uint16_t, unsigned>> types;
        for (const Frame& f : b.frames) {
            bool found = false;
            for (auto& t : types) {
                if (t.first == f.ethertype) { ++t.second; found = true; }
            }
            if (!found) types.push_back({f.ethertype, 1u});
        }
        for (const auto& t : types) std::printf("ETHERTYPE 0x%04x %u frames\n", t.first, t.second);
    }
    std::printf("EFF first up at %s ms; LINK_CTRL[0] %s; guard estimate %s\n",
                b.eff_seen_up ? std::to_string(static_cast<double>(b.eff_first_up) / kCyclesPerMs).c_str() : "never",
                b.sw_down ? "fell" : "1 throughout", b.est_down ? "fell" : "1 throughout");
    std::printf("FRAMES before the publication %zu, after %zu\n", before, after);
    check.dec("every CSR access of the boot answered", b.faults, 0);
    if (publish_ms != 0) {
        check.that("the boot's identity check passes on the split datapath", identity);
        check.that("the policy is written before the publication", booted && policy_done < published_at);
    }
    // the other two factors of the effective link qualify throughout: only the word holds it down
    check.that("LINK_CTRL[0] qualifies the link throughout (its reset, 1)", b.sw_down == 0);
    check.that("the link guard's estimate qualifies the link throughout (the PHY's clocks retained)", b.est_down == 0);
    check.dec("no frame crosses the MAC boundary before the firmware's publication", before, 0);
    check.that("the effective link (the gPTP port enable, the mailbox LINK) stays down before the publication",
               publish_ms == 0 ? !b.eff_seen_up : (!b.eff_seen_up || b.eff_first_up >= crossed));
    check.dec("o_ctl_link_up, the mailbox's LINK level, stays down before the publication", b.ctl_up_before, 0);
    if (publish_ms != 0) {
        check.that("the effective link rises with the publication", b.eff_seen_up && b.eff_first_up <= crossed + 4u);
        check.that("frames follow the publication within the window (transmit admitted)", after > 0);
    }
    return check.report();
}

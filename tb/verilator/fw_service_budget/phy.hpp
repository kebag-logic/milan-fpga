// SPDX-License-Identifier: (GPL-2.0 OR MIT)
#pragma once
#include <array>
#include <cstdint>
#include <cstdio>
#include <stdexcept>

// IEEE 802.3 22.3.4 peer; firmware supplies every clock and publication.
class PhyPeer {
public:
    void tick_entry(std::uint64_t cycle) { entry_ = cycle; }
    void sample(Vsim& dut, std::uint64_t cycle) {
        const unsigned pins = dut.phy_pins;
        if ((pins & 1u) && !(previous_ & 1u)) {
            if (bit_ == 0) { start_ = cycle; command_ = 0; }
            if (bit_ < 46) {
                if (!(pins & 2u)) throw std::runtime_error("MDIO command not driven");
                if (bit_ < 32) {
                    if (!(pins & 4u)) throw std::runtime_error("MDIO preamble not one");
                } else command_ = (command_ << 1) | ((pins >> 2) & 1u);
                reply_ = 1;
            } else {
                if (pins & 2u) throw std::runtime_error("MDIO read bus contention");
                if ((command_ >> 10) != 6u) throw std::runtime_error("MDIO not Clause-22 read");
                if (bit_ == 46) value_ = reg(command_ & 31u, cycle);
                // Edge k launches bit k+1: TA zero at 46, D15 at 47.
                reply_ = bit_ == 46 ? 0u : bit_ == 63 ? 1u : ((value_ >> (62u - bit_)) & 1u);
                if (((command_ >> 5) & 31u) != 0) reply_ = 1;
            }
            ++bit_;
        }
        if (!(pins & 1u) && bit_ == 64) {
            bit_ = 0;
            ++transactions_;
            const auto elapsed = cycle - start_;
            if (elapsed > longest_) longest_ = elapsed;
        }
        previous_ = pins;
        if (dut.phy_publish) {
            ++publications_;
            const auto elapsed = cycle - entry_;
            if (elapsed > longest_poll_) longest_poll_ = elapsed;
            read_due_ = cycle + 100;
        }
        if (read_due_ && cycle >= read_due_) reading_ = true;
        if (reading_ && dut.phy_ack) {
            if (dut.phy_error || dut.phy_data != dut.phy_status)
                throw std::runtime_error("MAC_STATUS disagrees with PHY publication");
            const auto& fabric = *dut.rootp->sim;
            const auto up = fabric.__PVT__milan_datapath__DOT__ctr_linkup_r;
            const auto down = fabric.__PVT__milan_datapath__DOT__ctr_linkdn_r;
            if (reads_) {
                const bool edge = (last_status_ ^ dut.phy_data) & 1u;
                if (up - last_up_ != unsigned(edge && (dut.phy_data & 1u))
                    || down - last_down_ != unsigned(edge && !(dut.phy_data & 1u)))
                    throw std::runtime_error("fabric link counter did not advance exactly once");
                if (edge && !(dut.phy_data & 1u)) ++down_edges_;
                if (edge && (dut.phy_data & 1u)) ++up_edges_;
            }
            std::printf("\nEVENT cycle=%llu kind=phy_read status=%u up=%u down=%u\n",
                        static_cast<unsigned long long>(cycle), unsigned(dut.phy_data), up, down);
            last_status_ = dut.phy_data;
            last_up_ = up;
            last_down_ = down;
            ++reads_;
            reading_ = false;
            read_due_ = 0;
        }
    }
    void drive(Vsim& dut) const {
        dut.phy_reply = reply_;
        dut.phy_read = reading_;
    }
    void report() const {
        if (!transactions_ || !publications_ || !reads_) throw std::runtime_error("missing MDIO/publication evidence");
        std::printf("\nPHY_TIMING transactions=%u publications=%u max_transaction_cycles=%llu max_poll_cycles=%llu down_edges=%u up_edges=%u\n",
                    transactions_, publications_, static_cast<unsigned long long>(longest_),
                    static_cast<unsigned long long>(longest_poll_), down_edges_, up_edges_);
    }
private:
    unsigned reg(unsigned address, std::uint64_t cycle) const {
        // The finite link-loss interval exercises recovery during long duties.
        const bool link = cycle < 150000000ULL || cycle >= 180000000ULL;
        switch (address) {
        case 0: return 0x1000;
        case 1: return link ? 0x0124 : 0x0120;
        case 2: return 0x001c;
        case 4: return 0x01e1;
        case 5: return cycle < 240000000ULL ? 0x01e1 : 0x0101;
        case 9: return 0x0300;
        case 10: return cycle < 240000000ULL ? 0x0c00 : 0;
        case 15: return 0x3000;
        default: return 0;
        }
    }
    unsigned previous_ = 0;
    unsigned bit_ = 0;
    unsigned command_ = 0;
    unsigned reply_ = 1;
    unsigned value_ = 0;
    unsigned transactions_ = 0;
    unsigned publications_ = 0;
    unsigned last_status_ = 13;
    unsigned last_up_ = 0;
    unsigned last_down_ = 0;
    unsigned reads_ = 0;
    unsigned down_edges_ = 0;
    unsigned up_edges_ = 0;
    std::uint64_t start_ = 0;
    std::uint64_t entry_ = 0;
    std::uint64_t longest_ = 0;
    std::uint64_t longest_poll_ = 0;
    std::uint64_t read_due_ = 0;
    bool reading_ = false;
};

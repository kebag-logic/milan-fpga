// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// phy_peer.hpp - a pin-level Clause-22 PHY behind the host bus's MDIO pair and
// the link-status word it publishes to (#919; plat/ctrl_plat_phy.h), as
// sw/firmware/nvm_hosttest/phy_peer.h answers the release's poll.
//
// It follows the pins the firmware writes, edge by edge: the 32 preamble ones
// and the 14 command bits driven, the turnaround and data released, each
// command a Clause-22 read (ST 01, OP 10). The PHY launches bit k + 1 on MDC's
// rising edge k (IEEE 802.3 22.3.4), so an STA that samples before the next
// rising edge reads the turnaround's zero, then D15 to D0. A PHY at another
// address, one told not to acknowledge, and a register on its NAK list leave
// the line high. BMSR's link status latches low (22.2.4.2.13): a loss the test
// latches reads as link down once, at the PHY's own address. Every frame and
// every publication is recorded with the bus access it ended at, and the first
// violation of the frame is kept as a finding instead of aborting the test.

#ifndef PHY_PEER_HPP
#define PHY_PEER_HPP

#include <array>
#include <cstddef>
#include <cstdint>
#include <string>
#include <vector>

namespace phy_peer {

struct Frame {
    unsigned address;
    unsigned reg;
    std::size_t at;   // the bus access that ended it
};

struct Publication {
    std::uint32_t word;
    std::size_t at;
};

struct Peer {
    std::uintptr_t w = 0, r = 0, status = 0;   // the addresses it answers (0: none)
    std::array<std::uint16_t, 32> regs{};
    unsigned address = 0;
    bool latched_down = false;
    bool acknowledge = true;
    unsigned nak = 32;
    std::uint32_t word = 13u;                  // link_status's value: the reset value, 1000 Mb/s full duplex, up
    std::vector<Frame> frames;
    std::vector<Publication> published;
    std::string fault;
    unsigned edge = 0, previous = 0, command = 0, reply = 1, input = 0;

    bool owns(std::uintptr_t a) const { return a != 0u && (a == w || a == r || a == status); }
    void violate(const char* what) {
        if (fault.empty()) fault = what;
    }
    // 1000BASE-T full duplex, negotiated, at `at`: the release's host test's register file.
    void gigabit(unsigned at) {
        address = at;
        regs = {};
        regs[0] = 0x1000u;
        regs[1] = 0x0124u;
        regs[2] = 0x001cu;
        regs[4] = 0x01e1u;
        regs[5] = 0x01e1u;
        regs[9] = 0x0300u;
        regs[10] = 0x0c00u;
        regs[15] = 0x3000u;
    }
    void link(bool up) {
        if (up) {
            regs[1] |= 0x4u;
        } else {
            regs[1] &= ~0x4u;
        }
    }
    void write(std::uintptr_t a, std::uint32_t v, std::size_t at) {
        if (a == status) {
            word = v;
            published.push_back({v, at});
            return;
        }
        if (a != w) return;
        if ((v & 1u) != 0u && (previous & 1u) == 0u) rise(v);
        if ((v & 1u) == 0u && edge == 64u) {
            frames.push_back({(command >> 5) & 31u, command & 31u, at});
            edge = 0;
            command = 0;
            reply = 1;
        }
        previous = v;
    }
    std::uint32_t read(std::uintptr_t a) const { return a == r ? reply : a == status ? word : 0u; }

private:
    void rise(std::uint32_t v) {
        if (edge >= 64u) {
            violate("a frame longer than 64 bit periods");
            return;
        }
        if (edge < 46u) {
            if ((v & 2u) == 0u) violate("the preamble or command not driven");
            if (edge < 32u && (v & 4u) == 0u) violate("a preamble bit not one");
            if (edge >= 32u) command = command << 1 | ((v >> 2) & 1u);
            reply = 1;
        } else {
            const bool addressed = ((command >> 5) & 31u) == address;
            if ((v & 2u) != 0u) violate("the turnaround or data driven by the STA");
            if ((command >> 10) != 6u) violate("not a Clause-22 read");
            if (edge == 46u) {
                const unsigned reg = command & 31u;
                input = regs[reg];
                if (reg == 1u && latched_down && addressed) {
                    input &= ~4u;
                    latched_down = false;
                }
            }
            reply = edge == 46u ? 0u : edge == 63u ? 1u : (input >> (62u - edge)) & 1u;
            if (!addressed || !acknowledge || (command & 31u) == nak) reply = 1;
        }
        ++edge;
    }
};

}  // namespace phy_peer

#endif  // PHY_PEER_HPP

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// phy_peer.hpp - a pin-level Clause-22 PHY behind the host bus's MDIO pair and
// the link-status word it publishes to (#919; plat/ctrl_plat_phy.h), as
// sw/firmware/nvm_hosttest/phy_peer.h answers the release's poll.
//
// It follows the pins the firmware writes, edge by edge: the 32 preamble ones
// and the 14 command bits driven, then a Clause-22 read (ST 01, OP 10) releases
// the turnaround and data, and a write (ST 01, OP 01, #840) drives its
// turnaround 10 and its 16 data bits too. The PHY launches bit k + 1 on MDC's
// rising edge k (IEEE 802.3 22.3.4), so an STA that samples before the next
// rising edge reads the turnaround's zero, then D15 to D0. A PHY at another
// address, one told not to acknowledge, and a register on its NAK list leave
// the line high. A write at the PHY's address sets the register, unless it is
// on the `ignored` list; register 0's restart (22.2.4.1.7) and reset bits
// clear themselves, a restart is counted, and where `restart_drops` it
// latches a loss, as a real PHY's renegotiation does. Where `negotiates`, a
// restart latches registers 4 and 9 as the abilities in force (28.2.4.1.3),
// apart from the registers a later write changes, and the link is the highest
// mode they share with the partner's (registers 5 and 10): `active_speed`,
// 0 when none, its link status following, negotiation complete. The next
// `drop_restarts` writes that restart negotiation are lost whole, as a write
// lost on the wire: register 0, the restart count, the abilities in force and
// the link stay the last negotiation's (22.2.4.1.7: the restart bit clears
// itself, so no read-back tells the two apart). BMSR's link status
// latches low (22.2.4.2.13): a loss the test latches reads as link down once,
// at the PHY's own address. Every frame and every publication is recorded with
// the bus access it ended at, and the first violation of the frame is kept as
// a finding instead of aborting the test.

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
    std::size_t at;        // the bus access that ended it
    bool write = false;    // a Clause-22 write, its value below
    std::uint16_t value = 0;
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
    unsigned ignored = 32;                     // a register whose writes it drops (32: none)
    unsigned drop_restarts = 0;                // the restart writes it loses next, whole
    bool restart_drops = false;
    unsigned restarts = 0;
    bool negotiates = false;                   // a restart latches the abilities in force and sets the link
    std::uint16_t active_anar = 0, active_gctrl = 0;
    unsigned active_speed = 0;                 // Mb/s of the link negotiated on them, 0: none
    std::uint32_t word = 13u;                  // link_status's value; a suite sets the reset it models
    std::vector<Frame> frames;
    std::vector<Publication> published;
    std::string fault;
    unsigned edge = 0, previous = 0, command = 0, reply = 1, input = 0, data = 0;

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
            const bool write = (command >> 10) == 5u;
            frames.push_back({(command >> 5) & 31u, command & 31u, at, write, static_cast<std::uint16_t>(data)});
            if (write) written();
            edge = 0;
            command = 0;
            data = 0;
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
        } else if ((command >> 10) == 5u) {
            if ((v & 2u) == 0u) violate("a write's turnaround or data not driven");
            data = (data << 1 | ((v >> 2) & 1u)) & 0x3ffffu;
            reply = 1;
        } else {
            const bool addressed = ((command >> 5) & 31u) == address;
            if ((v & 2u) != 0u) violate("the turnaround or data driven by the STA");
            if ((command >> 10) != 6u) violate("not a Clause-22 read or write");
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
    // A whole write: its turnaround 10 (22.2.4.5), then the register set at the PHY's own address.
    void written() {
        if ((data >> 16) != 2u) violate("a write's turnaround not 10");
        const unsigned reg = command & 31u;
        if (((command >> 5) & 31u) != address || reg == ignored) return;
        std::uint16_t value = static_cast<std::uint16_t>(data);
        if (reg == 0u && (value & 0x0200u) != 0u && drop_restarts != 0u) {
            --drop_restarts;
            return;
        }
        if (reg == 0u) regs[0] = static_cast<std::uint16_t>(value & ~0x8200u);
        else regs[reg] = value;
        if (reg == 0u && (value & 0x0200u) != 0u) {
            ++restarts;
            if (restart_drops) latched_down = true;
            if (negotiates) negotiate();
        }
    }

public:
    // A negotiation on the registers as they are now: registers 4 and 9 latched as the abilities in force, the link
    // the highest mode they share with the partner's, or none, and BMSR's autonegotiation complete.
    void negotiate() {
        active_anar = regs[4];
        active_gctrl = regs[9];
        const unsigned gig = (static_cast<unsigned>(active_gctrl) << 2) & regs[10] & 0x0c00u;
        const unsigned common = active_anar & regs[5] & 0x03e0u;
        active_speed = gig != 0u ? 1000u : (common & 0x0380u) != 0u ? 100u : common != 0u ? 10u : 0u;
        link(active_speed != 0u);
        regs[1] |= 0x0020u;
    }
};

}  // namespace phy_peer

#endif  // PHY_PEER_HPP

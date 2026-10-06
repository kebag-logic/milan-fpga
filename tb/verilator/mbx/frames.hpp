// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// frames.hpp - wire frames for the mailbox suite, written from the clauses
// (IEEE 1722.1-2021 Figures 6-1, 8-1 and 9-1; IEEE 1722-2016 Figure B.4;
// IEEE 802.1Q-2018 10.8), never from the RTL or the contract's filter table.
// The filter's byte offsets are then checked against these frames, so a
// contract offset that disagrees with the clause fails here.

#ifndef MBX_FRAMES_HPP
#define MBX_FRAMES_HPP

#include <cstdint>
#include <vector>

namespace mbx_tb {

//! One frame the TX merge sent: its bytes, interface and channel.
struct TxFrame {
    std::vector<std::uint8_t> bytes;
    unsigned iface = 0;
    unsigned channel = 0;
};

constexpr std::uint16_t kEtherAvtp = 0x22F0;   // IEEE 1722-2016 Table 5
constexpr std::uint16_t kEtherMsrp = 0x22EA;   // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherMvrp = 0x88F5;   // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherVlan = 0x8100;   // IEEE 802.1Q-2018 Table 9-1
constexpr std::uint8_t kSubAdp = 0xFA;          // IEEE 1722.1-2021 6.2.2.1
constexpr std::uint8_t kSubAecp = 0xFB;         // IEEE 1722.1-2021 9.2.2.1.1
constexpr std::uint8_t kSubAcmp = 0xFC;         // IEEE 1722.1-2021 8.2.2.1
constexpr std::uint8_t kSubMaap = 0xFE;         // IEEE 1722-2016 B.2.1
constexpr std::uint64_t kSrcMac = 0x0011223344A5ull;

inline void put_be(std::vector<std::uint8_t>& f, std::size_t at, std::uint64_t v, unsigned n) {
    for (unsigned i = 0; i < n; ++i) {
        f[at + i] = static_cast<std::uint8_t>(v >> (8u * (n - 1u - i)));
    }
}

//! An untagged Ethernet header with `len` frame bytes in all.
inline std::vector<std::uint8_t> eth(std::uint64_t dst, std::uint16_t ethertype, std::size_t len) {
    std::vector<std::uint8_t> f(len, 0);
    put_be(f, 0, dst, 6);
    put_be(f, 6, kSrcMac, 6);
    put_be(f, 12, ethertype, 2);
    return f;
}

//! An ADPDU (Figure 6-1): entity_id at wire byte 18, control_data_length 56.
//! `len` other than 82 truncates or zero-pads the 82-byte frame.
inline std::vector<std::uint8_t> adpdu(std::uint8_t message_type, std::uint64_t entity_id,
                                       std::size_t len = 82) {
    auto f = eth(0x91E0F0010000ull, kEtherAvtp, 82);
    f[14] = kSubAdp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 56, 2);
    put_be(f, 18, entity_id, 8);
    f.resize(len, 0);
    return f;
}

//! An ACMPDU (Figure 8-1): talker_entity_id at 34, listener_entity_id at 42.
inline std::vector<std::uint8_t> acmpdu(std::uint8_t message_type, std::uint64_t talker,
                                        std::uint64_t listener) {
    auto f = eth(0x91E0F0010000ull, kEtherAvtp, 70);
    f[14] = kSubAcmp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 44, 2);
    put_be(f, 34, talker, 8);
    put_be(f, 42, listener, 8);
    return f;
}

//! An AECPDU (Figure 9-1): target_entity_id at 18.
inline std::vector<std::uint8_t> aecpdu(std::uint64_t target, std::size_t len = 64) {
    auto f = eth(0x001B92000001ull, kEtherAvtp, len);
    f[14] = kSubAecp;
    put_be(f, 18, target, 8);
    return f;
}

//! A MAAP PDU (Figure B.4): requested_start_address at 26, requested_count at 32.
inline std::vector<std::uint8_t> maap(std::uint8_t message_type, std::uint64_t start, std::uint16_t count) {
    auto f = eth(0x91E0F000FF00ull, kEtherAvtp, 42);
    f[14] = kSubMaap;
    f[15] = message_type & 0x0Fu;
    put_be(f, 26, start, 6);
    put_be(f, 32, count, 2);
    return f;
}

//! An MRPDU frame: ProtocolVersion 0 at byte 14, then `body` (802.1Q 10.8).
inline std::vector<std::uint8_t> mrp(std::uint16_t ethertype, const std::vector<std::uint8_t>& body) {
    auto f = eth(ethertype == kEtherMsrp ? 0x0180C200000Eull : 0x0180C2000021ull, ethertype, 15 + body.size());
    for (std::size_t i = 0; i < body.size(); ++i) {
        f[15 + i] = body[i];
    }
    return f;
}

}  // namespace mbx_tb

#endif  // MBX_FRAMES_HPP

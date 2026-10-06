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
constexpr std::uint16_t kEtherPtp = 0x88F7;    // IEEE 802.1AS-2020 11.3.4: not a control EtherType here
constexpr std::uint8_t kSubAaf = 0x02;          // IEEE 1722-2016 Table 6
constexpr std::uint8_t kSubCrf = 0x04;          // IEEE 1722-2016 Table 6
constexpr std::uint8_t kSubAdp = 0xFA;          // IEEE 1722.1-2021 6.2.2.1
constexpr std::uint8_t kSubAecp = 0xFB;         // IEEE 1722.1-2021 9.2.2.1.1
constexpr std::uint8_t kSubAcmp = 0xFC;         // IEEE 1722.1-2021 8.2.2.1
constexpr std::uint8_t kSubReserved = 0xFD;     // IEEE 1722-2016 Table 6: reserved, no format assigned
constexpr std::uint8_t kSubMaap = 0xFE;         // IEEE 1722-2016 B.2.1
constexpr std::uint64_t kSrcMac = 0x0011223344A5ull;
constexpr std::uint64_t kAdpAcmpMac = 0x91E0F0010000ull;   // IEEE 1722.1-2021 Table B.1: ADP and ACMP
constexpr std::uint64_t kIdentifyMac = 0x91E0F0010001ull;  // IEEE 1722.1-2021 Table B.1: identification
constexpr std::uint64_t kMaapMac = 0x91E0F000FF00ull;      // IEEE 1722-2016 Table B.10
constexpr std::uint64_t kMsrpMac = 0x0180C200000Eull;      // IEEE 802.1Q-2018 35.2.2.1 (Table 8-1)
constexpr std::uint64_t kMvrpMac = 0x0180C2000021ull;      // IEEE 802.1Q-2018 Table 10-1
constexpr std::uint64_t kStreamMac = 0x91E0F000FE01ull;    // IEEE 1722-2016 Table B.9: a static stream address
//! The unicast MAC the suite gives interface 0 (OWN_MAC); interface i takes
//! kOwnMac + i, so each interface's is its own.
constexpr std::uint64_t kOwnMac = 0x001B92000001ull;
//! A unicast MAC no interface owns: traffic a switch floods.
constexpr std::uint64_t kForeignMac = 0x001B92000099ull;

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

//! An AECPDU (Figure 9-1): target_entity_id at 18, an AEM_COMMAND unicast
//! to interface 0's own MAC.
inline std::vector<std::uint8_t> aecpdu(std::uint64_t target, std::size_t len = 64) {
    auto f = eth(kOwnMac, kEtherAvtp, len);
    f[14] = kSubAecp;
    put_be(f, 18, target, 8);
    return f;
}

//! An AECPDU of any message_type (Table 9-1), both identities and its
//! destination: target_entity_id at 18, controller_entity_id at 26,
//! sequence_id at 34, and for an AEM PDU the command_type at 36 (7.4).
inline std::vector<std::uint8_t> aecp(std::uint8_t message_type, std::uint64_t target, std::uint64_t controller,
                                      std::uint64_t dst = kOwnMac, std::uint16_t command_type = 0) {
    auto f = eth(dst, kEtherAvtp, 64);
    f[14] = kSubAecp;
    f[15] = message_type & 0x0Fu;
    put_be(f, 16, 12, 2);
    put_be(f, 18, target, 8);
    put_be(f, 26, controller, 8);
    put_be(f, 34, 0x0102, 2);
    put_be(f, 36, command_type, 2);
    return f;
}

//! The CONTROLLER_AVAILABLE command type (IEEE 1722.1-2021 7.4.4, Table
//! 7-140; Milan v1.2 5.4.5.3 sends it to a registered controller as a
//! liveness probe).
constexpr std::uint16_t kControllerAvailable = 0x0003;

//! The frame with an 802.1Q C-tag (TPID 0x8100, then PCP 3 and VID 2, the SR
//! class A tag) inserted after the source address (802.1Q-2018 9.3).
inline std::vector<std::uint8_t> tagged(const std::vector<std::uint8_t>& untagged) {
    std::vector<std::uint8_t> f(untagged.begin(), untagged.begin() + 12);
    const std::uint8_t tag[] = {0x81, 0x00, 0x60, 0x02};
    f.insert(f.end(), tag, tag + 4);
    f.insert(f.end(), untagged.begin() + 12, untagged.end());
    return f;
}

//! The frame with its destination MAC replaced.
inline std::vector<std::uint8_t> to(std::vector<std::uint8_t> f, std::uint64_t dst) {
    put_be(f, 0, dst, 6);
    return f;
}

//! The frame with its EtherType replaced.
inline std::vector<std::uint8_t> with_ethertype(std::vector<std::uint8_t> f, std::uint16_t ethertype) {
    put_be(f, 12, ethertype, 2);
    return f;
}

//! The frame with byte 14 (the AVTP subtype; ProtocolVersion in an MRPDU) replaced.
inline std::vector<std::uint8_t> with_subtype(std::vector<std::uint8_t> f, std::uint8_t subtype) {
    f[14] = subtype;
    return f;
}

//! An AVTP stream data PDU (AAF or CRF) of `len` bytes to a stream address.
inline std::vector<std::uint8_t> stream_pdu(std::uint8_t subtype, std::uint64_t dst = kStreamMac,
                                            std::size_t len = 80) {
    auto f = eth(dst, kEtherAvtp, len);
    f[14] = subtype;
    f[15] = 0x81;   // sv set, version 0, mr 0, tv 1
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

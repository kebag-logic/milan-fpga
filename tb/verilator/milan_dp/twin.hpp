// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// twin.hpp - what both halves of the two-placement simulation share (#665;
// twin_fabric.cpp, twin_split.cpp, twin_compare.py): the one stimulus, the
// control frames each half captures at its MAC, and the capture file.
//
// THE STIMULUS IS ONE LIST. Each half applies it at the same modeled
// millisecond of its own clock: the all-fabric half's millisecond is the
// processor's compressed one (PP_TIM_DIV_MS_P datapath cycles), the split
// half's is one KL_mbx millisecond tick. The two clocks are never compared:
// twin_compare.py compares each protocol's frames as an ordered sequence, and
// grades a time a standard leaves random or bounded against that bound in
// each half on its own (#665 issuecomment-6716584453, item 1).
//
// A controller (kController, at kControllerMac) enumerates and drives the
// entity over AECP and ACMP, a peer talker's stream is bound and probed, and a
// peer probes the MAAP range both halves hold, which they defend (IEEE
// 1722-2016 B.3). Every frame is written from the clauses cited beside it.

#ifndef TWIN_HPP
#define TWIN_HPP

#include <cstdint>
#include <cstdio>
#include <string>
#include <vector>

namespace twin {

using Frame = std::vector<std::uint8_t>;

constexpr std::uint16_t kEtherAvtp = 0x22F0;      // IEEE 1722-2016 Table 5
constexpr std::uint16_t kEtherMsrp = 0x22EA;      // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherMvrp = 0x88F5;      // IEEE 802.1Q-2018 Table 10-2
constexpr std::uint16_t kEtherVlan = 0x8100;      // IEEE 802.1Q-2018 9.3
constexpr std::uint8_t kSubAdp = 0xFA;            // IEEE 1722.1-2021 6.2.2.1
constexpr std::uint8_t kSubAecp = 0xFB;           // IEEE 1722.1-2021 9.2.2.1.1
constexpr std::uint8_t kSubAcmp = 0xFC;           // IEEE 1722.1-2021 8.2.2.1
constexpr std::uint8_t kSubMaap = 0xFE;           // IEEE 1722-2016 B.2.1
constexpr std::uint64_t kAdpMulticast = 0x91E0F0010000ull;   // IEEE 1722.1-2021 Table B.1
constexpr std::uint64_t kMaapMulticast = 0x91E0F000FF00ull;  // IEEE 1722-2016 Table B.9

//! The entity under test, from the shipping shape's generated identity
//! (configs/endstation_ax7101_1x1_tdm8.yaml; adp_entity_gen.h).
constexpr std::uint64_t kEntityId = 0x020000FFFE000001ull;
constexpr std::uint64_t kEntityMac = 0x020000000001ull;
//! The controller, a peer talker and a peer listener.
constexpr std::uint64_t kController = 0x1111222233334444ull;
constexpr std::uint64_t kControllerMac = 0x001B92000099ull;
constexpr std::uint64_t kPeerTalker = 0x0202DEADBEEF0001ull;
constexpr std::uint64_t kPeerListener = 0x0303CAFEF00D0001ull;
constexpr std::uint64_t kPeerMac = 0x001B920000AAull;

//! MAAP's pinned first range, the simulation-only setting both halves take
//! (#665 issuecomment-6716584453, item 1): offset 0x0100 of the IEEE 1722-2016
//! B.4 pool, two addresses, one per talker source.
constexpr std::uint64_t kMaapPoolBase = 0x91E0F0000000ull;
constexpr std::uint16_t kMaapOffset = 0x0100;
constexpr std::uint64_t kMaapPreferred = kMaapPoolBase + kMaapOffset;
#ifndef TWIN_FW_MAAP_PREFERRED
#error "TWIN_FW_MAAP_PREFERRED, the pin twin_fw.py compiled into the firmware, comes from its cflags"
#endif
static_assert(TWIN_FW_MAAP_PREFERRED == kMaapPreferred, "both halves pin MAAP at one range");

//! How long both halves run, in modeled milliseconds.
constexpr std::uint32_t kRunMs = 36000;

inline void put_be(Frame& f, std::size_t at, std::uint64_t v, unsigned n) {
    for (unsigned i = 0; i < n; ++i) {
        f[at + i] = static_cast<std::uint8_t>(v >> (8u * (n - 1u - i)));
    }
}

//! An untagged frame from `src` to `dst`, padded to the 60-byte minimum.
inline Frame eth(std::uint64_t dst, std::uint64_t src, std::uint16_t ethertype, std::size_t len) {
    Frame f(len < 60 ? 60 : len, 0);
    put_be(f, 0, dst, 6);
    put_be(f, 6, src, 6);
    put_be(f, 12, ethertype, 2);
    return f;
}

//! ENTITY_DISCOVER for every entity (IEEE 1722.1-2021 6.2.1.5, entity_id 0).
inline Frame discover() {
    Frame f = eth(kAdpMulticast, kControllerMac, kEtherAvtp, 82);
    f[14] = kSubAdp;
    f[15] = 2;
    put_be(f, 16, 56, 2);
    return f;
}

//! An ACMPDU (IEEE 1722.1-2021 Figure 8-1), to the ACMP multicast address.
inline Frame acmp(std::uint8_t message_type, std::uint64_t talker, std::uint64_t listener, std::uint16_t seq) {
    Frame f = eth(kAdpMulticast, kControllerMac, kEtherAvtp, 70);
    f[14] = kSubAcmp;
    f[15] = message_type;
    put_be(f, 16, 44, 2);
    put_be(f, 26, kController, 8);
    put_be(f, 34, talker, 8);
    put_be(f, 42, listener, 8);
    put_be(f, 62, seq, 2);
    return f;
}

//! An AEM_COMMAND (IEEE 1722.1-2021 Figure 9-1, 9.2.1.2) from the controller
//! to the entity's MAC; control_data_length counts from controller_entity_id.
inline Frame aem(std::uint16_t command_type, const std::vector<std::uint8_t>& payload, std::uint16_t seq) {
    Frame f = eth(kEntityMac, kControllerMac, kEtherAvtp, 38 + payload.size());
    f[14] = kSubAecp;
    f[15] = 0;
    put_be(f, 16, 12 + payload.size(), 2);
    put_be(f, 18, kEntityId, 8);
    put_be(f, 26, kController, 8);
    put_be(f, 34, seq, 2);
    put_be(f, 36, command_type, 2);
    for (std::size_t k = 0; k < payload.size(); ++k) {
        f[38 + k] = payload[k];
    }
    return f;
}

//! A descriptor_type and descriptor_index pair, the head of most AEM payloads.
inline std::vector<std::uint8_t> descriptor(std::uint16_t type, std::uint16_t index) {
    return {static_cast<std::uint8_t>(type >> 8), static_cast<std::uint8_t>(type),
            static_cast<std::uint8_t>(index >> 8), static_cast<std::uint8_t>(index)};
}

//! READ_DESCRIPTOR (IEEE 1722.1-2021 7.4.5.1): the configuration, then the pair.
inline Frame read_descriptor(std::uint16_t type, std::uint16_t index, std::uint16_t seq, std::uint8_t config = 0) {
    std::vector<std::uint8_t> p{0, config, 0, 0};
    const std::vector<std::uint8_t> d = descriptor(type, index);
    p.insert(p.end(), d.begin(), d.end());
    return aem(0x0004, p, seq);
}

//! A MAAP PROBE from the peer for `count` addresses at `start` (IEEE 1722-2016 B.2).
inline Frame maap_probe(std::uint64_t start, std::uint16_t count) {
    Frame f = eth(kMaapMulticast, kPeerMac, kEtherAvtp, 42);
    f[14] = kSubMaap;
    f[15] = 1;                       // MAAP_PROBE (Table B.1), version 0
    put_be(f, 16, 16, 2);            // control_data_length
    put_be(f, 26, start, 6);         // requested_start_address
    put_be(f, 32, count, 2);         // requested_count
    return f;
}

//! SET_STREAM_FORMAT (IEEE 1722.1-2021 7.4.9.1) of one descriptor to `format`.
inline Frame set_stream_format(std::uint16_t type, std::uint16_t index, std::uint64_t format, std::uint16_t seq) {
    std::vector<std::uint8_t> p = descriptor(type, index);
    for (unsigned k = 0; k < 8; ++k) p.push_back(static_cast<std::uint8_t>(format >> (56 - 8 * k)));
    return aem(0x0008, p, seq);
}

//! SET_STREAM_INFO (IEEE 1722.1-2021 7.4.15.1) with no sub-command: flags 0
//! and every field 0, the 2021 payload's 84 bytes (aecp_commands.c's bound).
inline Frame set_stream_info(std::uint16_t type, std::uint16_t index, std::uint16_t seq) {
    std::vector<std::uint8_t> p = descriptor(type, index);
    p.resize(84, 0);
    return aem(0x000E, p, seq);
}

//! An AECPDU of a non-AEM message_type (IEEE 1722.1-2021 Table 9-1) with
//! `data` after the sequence_id: here a reserved type.
inline Frame aecp_other(std::uint8_t message_type, const std::vector<std::uint8_t>& data, std::uint16_t seq) {
    Frame f = aem(0, data, seq);
    f.erase(f.begin() + 36, f.begin() + 38);   // no command_type: the data follows the sequence_id
    f.resize(f.size() < 60 ? 60 : f.size(), 0);
    f[15] = message_type;
    put_be(f, 16, 10 + data.size(), 2);
    return f;
}

//! The shipping shape's STREAM_INPUT 0 format, its default (ADP_STRIN0_FMT_C,
//! the Makefile's TWIN_IN0_FMT out of the shape header both halves build).
#ifndef TWIN_IN0_FMT
#error "TWIN_IN0_FMT, STREAM_INPUT 0's declared format, comes from the Makefile"
#endif
constexpr std::uint64_t kIn0Format = TWIN_IN0_FMT;

//! One stimulus frame and the modeled millisecond both halves receive it at.
struct Stimulus {
    std::uint32_t ms;
    const char* what;
    Frame frame;
};

//! The scenario's stimulus, in time order (the plan's S6: ADP, ACMP, MAAP,
//! AECP; SRP declares on its own).
inline std::vector<Stimulus> scenario() {
    const std::uint16_t sin = 0x0005;   // STREAM_INPUT
    const std::uint16_t sout = 0x0006;  // STREAM_OUTPUT
    return {
        {2500, "ADP ENTITY_DISCOVER", discover()},
        {3000, "AECP REGISTER_UNSOLICITED_NOTIFICATION", aem(0x0024, {0, 0, 0, 0}, 1)},
        {3100, "AECP READ_DESCRIPTOR ENTITY 0", read_descriptor(0x0000, 0, 2)},
        {3200, "AECP READ_DESCRIPTOR CONFIGURATION 0", read_descriptor(0x0001, 0, 3)},
        {3300, "AECP READ_DESCRIPTOR STREAM_INPUT 0", read_descriptor(sin, 0, 4)},
        {3400, "AECP READ_DESCRIPTOR STREAM_OUTPUT 0", read_descriptor(sout, 0, 5)},
        {3500, "AECP READ_DESCRIPTOR AVB_INTERFACE 0", read_descriptor(0x0009, 0, 6)},
        {3600, "AECP GET_STREAM_FORMAT STREAM_INPUT 0", aem(0x0009, descriptor(sin, 0), 7)},
        {3800, "AECP GET_COUNTERS STREAM_INPUT 0", aem(0x0029, descriptor(sin, 0), 8)},
        {4000, "ACMP BIND_RX sink 0", acmp(6, kPeerTalker, kEntityId, 0x0101)},
        {4500, "ACMP GET_RX_STATE sink 0", acmp(10, kPeerTalker, kEntityId, 0x0102)},
        {5000, "ACMP PROBE_TX source 0", acmp(0, kEntityId, kPeerListener, 0x0103)},
        {5500, "ACMP GET_TX_STATE source 0", acmp(4, kEntityId, kPeerListener, 0x0104)},
        {6000, "AECP START_STREAMING STREAM_INPUT 0", aem(0x0022, descriptor(sin, 0), 9)},
        {6200, "AECP STOP_STREAMING STREAM_INPUT 0", aem(0x0023, descriptor(sin, 0), 10)},
        {7000, "ACMP UNBIND_RX sink 0", acmp(8, kPeerTalker, kEntityId, 0x0105)},
        {8000, "MAAP PROBE of the held range", maap_probe(kMaapPreferred, 2)},
        // the F5 difference ledger's rows (sw/firmware/ctrl/aecp/README.md)
        {9000, "AECP READ_DESCRIPTOR ENTITY 0 at configuration 1", read_descriptor(0x0000, 0, 11, 1)},
        {9200, "AECP SET_STREAM_INFO STREAM_INPUT 0, no sub-command", set_stream_info(sin, 0, 12)},
        {9400, "AECP SET_STREAM_FORMAT STREAM_INPUT 0 to its default", set_stream_format(sin, 0, kIn0Format, 13)},
        {9600, "AECP reserved message_type 10", aecp_other(10, {0, 0, 0, 0}, 14)},
    };
}

//! The EtherType after an optional C-tag, and the payload's offset.
inline bool ethertype(const Frame& f, std::uint16_t* type, std::size_t* at) {
    if (f.size() < 15) return false;
    std::size_t k = 12;
    std::uint16_t t = static_cast<std::uint16_t>(f[k] << 8 | f[k + 1]);
    if (t == kEtherVlan && f.size() >= 19) {
        k += 4;
        t = static_cast<std::uint16_t>(f[k] << 8 | f[k + 1]);
    }
    *type = t;
    *at = k + 2;
    return true;
}

//! A control frame the comparison reads: ADP, AECP, ACMP or MAAP under the
//! AVTP EtherType, or an MSRP or MVRP MRPDU. Stream data is counted, not kept.
inline bool is_control(const Frame& f) {
    std::uint16_t t = 0;
    std::size_t at = 0;
    if (!ethertype(f, &t, &at)) return false;
    if (t == kEtherMsrp || t == kEtherMvrp) return true;
    if (t != kEtherAvtp || at >= f.size()) return false;
    const std::uint8_t sub = f[at];
    return sub == kSubAdp || sub == kSubAecp || sub == kSubAcmp || sub == kSubMaap;
}

//! One frame a half's MAC sent, and the modeled millisecond it left at.
struct Sent {
    std::uint32_t ms;
    Frame bytes;
};

inline std::string hex(const Frame& f) {
    std::string s;
    char b[3];
    for (const std::uint8_t c : f) {
        std::snprintf(b, sizeof b, "%02x", c);
        s += b;
    }
    return s;
}

//! The capture twin_compare.py reads: the half's name, its millisecond, every
//! control frame in the order its MAC sent it, the stimulus as applied, and
//! the count of stream frames the capture left out.
struct Capture {
    std::string placement;
    std::string ms_unit;
    std::vector<Sent> frames;
    std::vector<std::pair<std::uint32_t, std::string>> applied;
    std::uint64_t stream_frames = 0;
    std::vector<std::pair<std::string, std::string>> notes;

    bool write(const char* path) const {
        std::FILE* fh = std::fopen(path, "w");
        if (fh == nullptr) return false;
        std::fprintf(fh, "{\"placement\": \"%s\", \"ms_unit\": \"%s\", \"run_ms\": %u, \"stream_frames\": %llu,\n",
                     placement.c_str(), ms_unit.c_str(), kRunMs, static_cast<unsigned long long>(stream_frames));
        std::fprintf(fh, " \"notes\": {");
        for (std::size_t k = 0; k < notes.size(); ++k) {
            std::fprintf(fh, "%s\"%s\": \"%s\"", k ? ", " : "", notes[k].first.c_str(), notes[k].second.c_str());
        }
        std::fprintf(fh, "},\n \"applied\": [");
        for (std::size_t k = 0; k < applied.size(); ++k) {
            std::fprintf(fh, "%s\n  {\"ms\": %u, \"what\": \"%s\"}", k ? "," : "", applied[k].first,
                         applied[k].second.c_str());
        }
        std::fprintf(fh, "],\n \"frames\": [");
        for (std::size_t k = 0; k < frames.size(); ++k) {
            std::fprintf(fh, "%s\n  {\"ms\": %u, \"hex\": \"%s\"}", k ? "," : "", frames[k].ms,
                         hex(frames[k].bytes).c_str());
        }
        std::fprintf(fh, "]}\n");
        return std::fclose(fh) == 0;
    }
};

}  // namespace twin

#endif  // TWIN_HPP

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
// 1722-2016 B.3). A second controller (kController2, at its own MAC) registers
// for unsolicited notifications, so the commands of the first are notified to
// it (IEEE 1722.1-2021 7.5.2), and the F5 difference ledger's remaining rows
// are reached: LOCK_ENTITY and its release, the Milan vendor-unique commands
// (Milan v1.2 5.4.3, 5.4.4) and one HDCP_APM PDU (#665 issuecomment-6717765106,
// item 6). A second read of ENTITY follows two ENTITY_AVAILABLE, so its
// available_index is not the first ADPDU's 0 (issuecomment-6722002738, item 6).
// Both controllers answer the entity's CONTROLLER_AVAILABLE as a live
// controller does (controller_available_answer), so each stays registered to
// the run's end, past the 60 s lock expiry. Every frame is written from the
// clauses cited beside it.

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
//! The controller, a second controller, a peer talker and a peer listener.
constexpr std::uint64_t kController = 0x1111222233334444ull;
constexpr std::uint64_t kControllerMac = 0x001B92000099ull;
constexpr std::uint64_t kController2 = 0x2222333344445555ull;
constexpr std::uint64_t kController2Mac = 0x001B9200009Bull;
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

//! How long both halves run, in modeled milliseconds: past the expiry of the
//! lock taken at 11400 ms and never released (Milan v1.2 5.4.2.2, 60 s).
constexpr std::uint32_t kRunMs = 75000;

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

//! A controller: its entity ID and the MAC its frames come from.
struct Controller {
    std::uint64_t id;
    std::uint64_t mac;
};
constexpr Controller kFirst{kController, kControllerMac};
constexpr Controller kSecond{kController2, kController2Mac};

//! An AEM_COMMAND (IEEE 1722.1-2021 Figure 9-1, 9.2.1.2) from a controller
//! to the entity's MAC; control_data_length counts from controller_entity_id.
inline Frame aem(std::uint16_t command_type, const std::vector<std::uint8_t>& payload, std::uint16_t seq,
                 Controller from = kFirst) {
    Frame f = eth(kEntityMac, from.mac, kEtherAvtp, 38 + payload.size());
    f[14] = kSubAecp;
    f[15] = 0;
    put_be(f, 16, 12 + payload.size(), 2);
    put_be(f, 18, kEntityId, 8);
    put_be(f, 26, from.id, 8);
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
inline Frame read_descriptor(std::uint16_t type, std::uint16_t index, std::uint16_t seq, std::uint8_t config = 0,
                             Controller from = kFirst) {
    std::vector<std::uint8_t> p{0, config, 0, 0};
    const std::vector<std::uint8_t> d = descriptor(type, index);
    p.insert(p.end(), d.begin(), d.end());
    return aem(0x0004, p, seq, from);
}

//! LOCK_ENTITY (IEEE 1722.1-2021 7.4.2.1) of the ENTITY descriptor: flags
//! (UNLOCK is bit 0), locked_id 0, descriptor_type and descriptor_index 0.
inline Frame lock_entity(bool unlock, std::uint16_t seq) {
    std::vector<std::uint8_t> p(16, 0);
    p[3] = unlock ? 1 : 0;
    return aem(0x0001, p, seq);
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

//! A Milan vendor-unique command (Milan v1.2 5.4.3.2, Table 5.18): the MVU
//! protocol_id 00-1B-C5-0A-C1-00, r 0 and command_type, the halfword at @30,
//! then the command's octets from @32, in the figure its clause gives.
inline Frame mvu(std::uint16_t command_type, std::uint16_t at30, const std::vector<std::uint8_t>& octets,
                 std::uint16_t seq) {
    std::vector<std::uint8_t> d{0x00, 0x1B, 0xC5, 0x0A, 0xC1, 0x00,
                                static_cast<std::uint8_t>(command_type >> 8), static_cast<std::uint8_t>(command_type),
                                static_cast<std::uint8_t>(at30 >> 8), static_cast<std::uint8_t>(at30)};
    d.insert(d.end(), octets.begin(), octets.end());
    return aecp_other(6, d, seq);
}

//! SET_SYSTEM_UNIQUE_ID's system_unique_id (Milan v1.2 5.4.4.2, Figure 5.5;
//! 0 is the default it forbids).
constexpr std::uint64_t kSystemUniqueId = 0x0102030405060708ull;

//! SET_MEDIA_CLOCK_REFERENCE_INFO's octets from @32 (Milan v1.2 5.4.4.4,
//! Figure 5.6, clock domain 0 at @30), the command the processor's model
//! sends (tests/steps/aecp_engine_model.py): flags 0x03, both Table 5.21
//! flags; octets 0, 0 and 0x80; four reserved octets; the domain named
//! "DEFAULT", zero padded to 64 octets.
inline std::vector<std::uint8_t> mcr_info() {
    std::vector<std::uint8_t> o{0x03, 0x00, 0x00, 0x80, 0, 0, 0, 0, 'D', 'E', 'F', 'A', 'U', 'L', 'T'};
    o.resize(8 + 64, 0);
    return o;
}

//! An HDCP_APM_COMMAND (IEEE 1722.1-2021 9.7): its fixed header after the
//! sequence_id (two HDCP data octets, flags 0, fragment offset 0), then the
//! two data octets.
inline Frame hdcp_apm(std::uint16_t seq) {
    return aecp_other(8, {0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0xDE, 0xAD}, seq);
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
        {3050, "AECP REGISTER_UNSOLICITED_NOTIFICATION, the second controller",
         aem(0x0024, {0, 0, 0, 0}, 0x0201, kSecond)},
        {3060, "AECP READ_DESCRIPTOR ENTITY 0, the second controller", read_descriptor(0x0000, 0, 0x0202, 0, kSecond)},
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
        {6500, "AECP START_STREAMING STREAM_INPUT 0, once stopped", aem(0x0022, descriptor(sin, 0), 23)},
        {7000, "ACMP UNBIND_RX sink 0", acmp(8, kPeerTalker, kEntityId, 0x0105)},
        // after each half's second ENTITY_AVAILABLE (available_index 1) and before its third, so ENTITY's
        // available_index shows (IEEE 1722.1-2021 Table 7-2; #665 issuecomment-6722002738, item 6)
        {7500, "AECP READ_DESCRIPTOR ENTITY 0, after two ENTITY_AVAILABLE", read_descriptor(0x0000, 0, 25)},
        {8000, "MAAP PROBE of the held range", maap_probe(kMaapPreferred, 2)},
        // the F5 difference ledger's rows (sw/firmware/ctrl/aecp/README.md)
        {9000, "AECP READ_DESCRIPTOR ENTITY 0 at configuration 1", read_descriptor(0x0000, 0, 11, 1)},
        {9200, "AECP SET_STREAM_INFO STREAM_INPUT 0, no sub-command", set_stream_info(sin, 0, 12)},
        {9400, "AECP SET_STREAM_FORMAT STREAM_INPUT 0 to its default", set_stream_format(sin, 0, kIn0Format, 13)},
        {9600, "AECP reserved message_type 10", aecp_other(10, {0, 0, 0, 0}, 14)},
        {9800, "AECP LOCK_ENTITY ENTITY 0", lock_entity(false, 15)},
        {10000, "AECP LOCK_ENTITY ENTITY 0, UNLOCK", lock_entity(true, 16)},
        {10200, "AECP MVU GET_MILAN_INFO", mvu(0x0000, 0, {}, 17)},
        {10400, "AECP MVU SET_SYSTEM_UNIQUE_ID",
         mvu(0x0001, 0, {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08}, 18)},
        {10600, "AECP MVU GET_SYSTEM_UNIQUE_ID", mvu(0x0002, 0, {}, 19)},
        {10800, "AECP MVU SET_MEDIA_CLOCK_REFERENCE_INFO clock domain 0", mvu(0x0003, 0, mcr_info(), 20)},
        {11000, "AECP MVU GET_MEDIA_CLOCK_REFERENCE_INFO clock domain 0", mvu(0x0004, 0, {}, 21)},
        {11200, "AECP HDCP_APM_COMMAND", hdcp_apm(22)},
        {11400, "AECP LOCK_ENTITY ENTITY 0, left to expire", lock_entity(false, 24)},
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

//! A live controller's answer to the entity's CONTROLLER_AVAILABLE (Milan
//! v1.2 5.4.5.3; IEEE 1722.1-2021 7.4.4): when `sent` is that AEM_COMMAND
//! addressed to one of the two controllers, its AEM_RESPONSE SUCCESS from that
//! controller's MAC, with the command's sequence_id, so both stay registered
//! and see every notice to the run's end. `who` names the controller.
inline bool controller_available_answer(const Frame& sent, Frame* answer, const char** who) {
    std::uint16_t t = 0;
    std::size_t at = 0;
    if (!ethertype(sent, &t, &at) || t != kEtherAvtp || at + 24 > sent.size() || sent[at] != kSubAecp ||
        (sent[at + 1] & 0x0F) != 0 || sent[at + 22] != 0x00 || sent[at + 23] != 0x03) {
        return false;
    }
    std::uint64_t target = 0;
    for (unsigned k = 0; k < 8; ++k) target = target << 8 | sent[at + 4 + k];
    const Controller* from = target == kController ? &kFirst : target == kController2 ? &kSecond : nullptr;
    if (from == nullptr) return false;
    *answer = eth(kEntityMac, from->mac, kEtherAvtp, 38);
    Frame& f = *answer;
    f[14] = kSubAecp;
    f[15] = 1;                                   // AEM_RESPONSE, status SUCCESS
    put_be(f, 16, 12, 2);
    put_be(f, 18, from->id, 8);                  // target_entity_id: the controller answering
    for (unsigned k = 0; k < 8; ++k) f[26 + k] = sent[at + 12 + k];   // controller_entity_id: the entity
    f[34] = sent[at + 20];                       // the command's sequence_id
    f[35] = sent[at + 21];
    put_be(f, 36, 0x0003, 2);
    *who = from == &kFirst ? "AECP CONTROLLER_AVAILABLE response, the first controller"
                           : "AECP CONTROLLER_AVAILABLE response, the second controller";
    return true;
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
    //! each stimulus frame as applied: its millisecond, its name and its bytes
    struct Applied {
        std::uint32_t ms;
        std::string what;
        Frame frame;
    };
    std::vector<Applied> applied;
    std::uint64_t stream_frames = 0;
    //! the millisecond the first stream frame left at, or -1: MVRP is graded against it (Milan v1.2 4.3.2)
    std::int64_t first_stream_ms = -1;
    std::vector<std::pair<std::string, std::string>> notes;

    //! Count one stream frame, and note the first one's millisecond.
    void stream_frame(std::uint32_t ms) {
        if (stream_frames++ == 0) first_stream_ms = ms;
    }

    bool write(const char* path) const {
        std::FILE* fh = std::fopen(path, "w");
        if (fh == nullptr) return false;
        std::fprintf(fh,
                     "{\"placement\": \"%s\", \"ms_unit\": \"%s\", \"run_ms\": %u, \"stream_frames\": %llu, "
                     "\"first_stream_ms\": %lld,\n",
                     placement.c_str(), ms_unit.c_str(), kRunMs, static_cast<unsigned long long>(stream_frames),
                     static_cast<long long>(first_stream_ms));
        std::fprintf(fh, " \"notes\": {");
        for (std::size_t k = 0; k < notes.size(); ++k) {
            std::fprintf(fh, "%s\"%s\": \"%s\"", k ? ", " : "", notes[k].first.c_str(), notes[k].second.c_str());
        }
        std::fprintf(fh, "},\n \"applied\": [");
        for (std::size_t k = 0; k < applied.size(); ++k) {
            std::fprintf(fh, "%s\n  {\"ms\": %u, \"what\": \"%s\", \"hex\": \"%s\"}", k ? "," : "", applied[k].ms,
                         applied[k].what.c_str(), hex(applied[k].frame).c_str());
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

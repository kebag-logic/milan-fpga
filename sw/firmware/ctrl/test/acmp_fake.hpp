// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// acmp_fake.hpp - the ACMP core's ports as a test's fakes, the frames a test
// sends it and the fields it reads back (#665 lane F3).
//
// Every port call is logged in order (Call), so a test can say what came
// before what: a response before its notification (#653), a persist before
// nothing in particular, a timer arm after the frame it times. A test can
// also make one port call back into the core (Fake::hook), which is what the
// no-callback rule (#678) forbids and the core's guard must refuse.

#ifndef ACMP_FAKE_HPP
#define ACMP_FAKE_HPP

#include <array>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <functional>
#include <vector>

#include "acmp.h"
#include "wire.h"

namespace acmp_test {

constexpr std::uint64_t kOwn = 0x0A0B0C0D0E0F1011ull;          // this entity
constexpr std::uint64_t kMac0 = 0x001B92000A01ull;
constexpr std::uint64_t kMac1 = 0x001B92000A02ull;
constexpr std::uint64_t kCtl1 = 0x0011223344556677ull;         // controllers
constexpr std::uint64_t kCtl2 = 0x0099AABBCCDDEEFFull;
constexpr std::uint64_t kTkA = 0x00221100AABBCCDDull;          // talkers
constexpr std::uint64_t kTkB = 0x00221100AABBCC55ull;
constexpr std::uint64_t kGm0 = 0xA1A2A3A4A5A6A7A8ull;
constexpr std::uint64_t kSid = 0x5544332211002233ull;
constexpr std::uint64_t kDa = 0x91E0F0004455ull;

// One port call.
struct Call {
    enum Kind { SEND, TIMER, GPTP, NOW, SEED, LOCKED, SOURCE, SRP, PERSIST, CHANGED } kind;
    unsigned index;             // the interface, sink or source
    bool flag;                  // TIMER: armed; SRP: a stream (not NULL); SEND: taken
    std::uint32_t value;        // TIMER: the deadline
    acmp_stream stream;         // SRP
};

struct Sent {
    unsigned interface;
    std::array<std::uint8_t, ACMP_FRAME_BYTES> bytes;
};

struct Fake {
    bool room = true;
    std::uint32_t now = 50000;
    std::uint64_t gm[ACMP_MAX_INTERFACES] = {kGm0, kGm0, kGm0, kGm0};
    std::uint8_t domain[ACMP_MAX_INTERFACES] = {};
    std::uint32_t seed = 0x5EEDu;
    bool locked = false;
    std::uint64_t holder = 0;
    acmp_source_state source[ACMP_MAX_SOURCES] = {};
    std::vector<Sent> sent;
    std::vector<Call> calls;
    bool armed[ACMP_MAX_INTERFACES] = {};
    std::uint32_t at[ACMP_MAX_INTERFACES] = {};
    // one call back into the core, made from inside the port named by
    // hook_kind, then cleared
    Call::Kind hook_kind = Call::SEND;
    std::function<void()> hook;

    void reenter(Call::Kind kind) {
        if (hook && hook_kind == kind) {
            auto h = hook;
            hook = nullptr;
            h();
        }
    }
    unsigned count(Call::Kind kind) const {
        unsigned n = 0;
        for (const Call& c : calls) {
            n += c.kind == kind ? 1u : 0u;
        }
        return n;
    }
    // The position in the log of the n-th call of a kind (from 0), or -1.
    int position(Call::Kind kind, unsigned n = 0) const {
        for (std::size_t i = 0; i < calls.size(); ++i) {
            if (calls[i].kind == kind && n-- == 0u) {
                return static_cast<int>(i);
            }
        }
        return -1;
    }
    void clear() {
        sent.clear();
        calls.clear();
    }
};

inline Fake fk;

inline bool f_send(void*, unsigned interface, const std::uint8_t* frame, std::size_t len) {
    fk.calls.push_back({Call::SEND, interface, fk.room, 0u, {}});
    fk.reenter(Call::SEND);
    if (!fk.room || len != ACMP_FRAME_BYTES) {
        return false;
    }
    Sent s{interface, {}};
    std::memcpy(s.bytes.data(), frame, len);
    fk.sent.push_back(s);
    return true;
}

inline std::uint32_t f_now(void*) {
    fk.calls.push_back({Call::NOW, 0u, false, fk.now, {}});
    fk.reenter(Call::NOW);
    return fk.now;
}

inline void f_timer(void*, unsigned interface, bool armed, std::uint32_t deadline) {
    fk.calls.push_back({Call::TIMER, interface, armed, deadline, {}});
    fk.armed[interface] = armed;
    fk.at[interface] = deadline;
    fk.reenter(Call::TIMER);
}

inline void f_gptp(void*, unsigned interface, std::uint64_t* gm, std::uint8_t* domain) {
    fk.calls.push_back({Call::GPTP, interface, false, 0u, {}});
    *gm = fk.gm[interface];
    *domain = fk.domain[interface];
    fk.reenter(Call::GPTP);
}

inline std::uint32_t f_seed(void*) {
    fk.calls.push_back({Call::SEED, 0u, false, 0u, {}});
    fk.reenter(Call::SEED);
    return fk.seed;
}

inline bool f_locked(void*, std::uint64_t* holder) {
    fk.calls.push_back({Call::LOCKED, 0u, fk.locked, 0u, {}});
    *holder = fk.holder;
    fk.reenter(Call::LOCKED);
    return fk.locked;
}

inline void f_source(void*, unsigned index, acmp_source_state* out) {
    fk.calls.push_back({Call::SOURCE, index, false, 0u, {}});
    *out = fk.source[index];
    fk.reenter(Call::SOURCE);
}

inline void f_srp(void*, unsigned sink, const acmp_stream* stream) {
    fk.calls.push_back({Call::SRP, sink, stream != nullptr, 0u, stream != nullptr ? *stream : acmp_stream{}});
    fk.reenter(Call::SRP);
}

inline void f_persist(void*, unsigned sink) {
    fk.calls.push_back({Call::PERSIST, sink, false, 0u, {}});
    fk.reenter(Call::PERSIST);
}

inline void f_changed(void*, unsigned sink) {
    fk.calls.push_back({Call::CHANGED, sink, false, 0u, {}});
    fk.reenter(Call::CHANGED);
}

inline const acmp_ports kPorts = {nullptr, f_send, f_now, f_timer, f_gptp, f_seed};
inline const acmp_env kEnv = {nullptr, f_locked, f_source, f_srp, f_persist, f_changed};

// ---- frames -------------------------------------------------------------------------

struct Pdu {
    std::uint8_t msg = 0;
    std::uint8_t status = 0;
    std::uint64_t stream_id = 0;
    std::uint64_t controller = 0;
    std::uint64_t talker = 0;
    std::uint64_t listener = 0;
    std::uint16_t talker_uid = 0;
    std::uint16_t listener_uid = 0;
    std::uint64_t dest_mac = 0;
    std::uint16_t count = 0;
    std::uint16_t seq = 0;
    std::uint16_t flags = 0;
    std::uint16_t vlan = 0;
};

// An ACMP frame (IEEE 1722.1-2021 Figure 8-1) as a controller or a talker sends it.
inline std::array<std::uint8_t, ACMP_FRAME_BYTES> acmpdu(const Pdu& p, std::uint64_t src = 0x0202DEADBEEFull) {
    std::array<std::uint8_t, ACMP_FRAME_BYTES> f{};
    std::uint8_t* b = f.data();
    wire_put_be(b, ACMP_MULTICAST_MAC, 6);
    wire_put_be(b + 6, src, 6);
    wire_put_be(b + 12, ACMP_ETHERTYPE, 2);
    b[14] = ACMP_SUBTYPE;
    b[15] = p.msg & 0x0Fu;
    wire_put_be(b + 16, (static_cast<std::uint32_t>(p.status) << 11) | ACMP_CONTROL_DATA_LENGTH, 2);
    wire_put_be(b + 18, p.stream_id, 8);
    wire_put_be(b + 26, p.controller, 8);
    wire_put_be(b + 34, p.talker, 8);
    wire_put_be(b + 42, p.listener, 8);
    wire_put_be(b + 50, p.talker_uid, 2);
    wire_put_be(b + 52, p.listener_uid, 2);
    wire_put_be(b + 54, p.dest_mac, 6);
    wire_put_be(b + 60, p.count, 2);
    wire_put_be(b + 62, p.seq, 2);
    wire_put_be(b + 64, p.flags, 2);
    wire_put_be(b + 66, p.vlan, 2);
    return f;
}

// A frame's ACMPDU, read back.
inline Pdu read(const std::uint8_t* b) {
    Pdu p;
    p.msg = b[15] & 0x0Fu;
    p.status = static_cast<std::uint8_t>(b[16] >> 3);
    p.stream_id = wire_be64(b + 18);
    p.controller = wire_be64(b + 26);
    p.talker = wire_be64(b + 34);
    p.listener = wire_be64(b + 42);
    p.talker_uid = wire_be16(b + 50);
    p.listener_uid = wire_be16(b + 52);
    p.dest_mac = (static_cast<std::uint64_t>(wire_be16(b + 54)) << 32) | wire_be32(b + 56);
    p.count = wire_be16(b + 60);
    p.seq = wire_be16(b + 62);
    p.flags = wire_be16(b + 64);
    p.vlan = wire_be16(b + 66);
    return p;
}

inline bool same(const Pdu& x, const Pdu& y) {
    return x.msg == y.msg && x.status == y.status && x.stream_id == y.stream_id && x.controller == y.controller &&
           x.talker == y.talker && x.listener == y.listener && x.talker_uid == y.talker_uid &&
           x.listener_uid == y.listener_uid && x.dest_mac == y.dest_mac && x.count == y.count && x.seq == y.seq &&
           x.flags == y.flags && x.vlan == y.vlan;
}

// An ADP frame (IEEE 1722.1-2021 Figure 6-1) from a talker.
struct Adp {
    std::uint8_t msg = ACMP_ADP_MSG_ENTITY_AVAILABLE;
    std::uint64_t entity = kTkA;
    std::uint8_t valid_time = 10;
    std::uint32_t index = 1;
    std::uint64_t gm = kGm0;
    std::uint8_t domain = 0;
    std::uint16_t interface_index = 0;
};

inline std::array<std::uint8_t, ACMP_ADP_FRAME_BYTES> adpdu(const Adp& a) {
    std::array<std::uint8_t, ACMP_ADP_FRAME_BYTES> f{};
    std::uint8_t* b = f.data();
    wire_put_be(b, ACMP_MULTICAST_MAC, 6);
    wire_put_be(b + 6, 0x0202DEADBEEFull, 6);
    wire_put_be(b + 12, ACMP_ETHERTYPE, 2);
    b[14] = ACMP_ADP_SUBTYPE;
    b[15] = a.msg & 0x0Fu;
    wire_put_be(b + 16, (static_cast<std::uint32_t>(a.valid_time) << 11) | 56u, 2);
    wire_put_be(b + 18, a.entity, 8);
    wire_put_be(b + 50, a.index, 4);
    wire_put_be(b + 54, a.gm, 8);
    b[62] = a.domain;
    wire_put_be(b + 68, a.interface_index, 2);
    return f;
}

}  // namespace acmp_test

#endif  // ACMP_FAKE_HPP

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: MIT
// Milan v1.2 5.5.3
// Milan v1.2 5.6.4

#include <gtest/gtest.h>

#include <array>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "wire.h"

using namespace acmp_test;
extern "C" {
bool old_acmp_init(struct acmp *a, const struct acmp_config *cfg, const struct acmp_ports *ports,
	       const struct acmp_env *env);
bool old_acmp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len);
bool old_acmp_rx_ready(const struct acmp *a);
void old_acmp_adp_rx(struct acmp *a, unsigned interface, const uint8_t *frame, size_t len);
void old_acmp_timer_expired(struct acmp *a, unsigned interface);
void old_acmp_tk_registered(struct acmp *a, unsigned sink, bool failed);
void old_acmp_tk_unregistered(struct acmp *a, unsigned sink);
void old_acmp_tk_kind_changed(struct acmp *a, unsigned sink, bool failed);
bool old_acmp_set_started(struct acmp *a, unsigned sink, bool started);
bool old_acmp_poll(struct acmp *a);
bool old_acmp_listener_registered(struct acmp *a, unsigned interface, unsigned source, bool registered);
bool old_acmp_declaring(struct acmp *a, unsigned source);
enum acmp_restore old_acmp_restore_binding(struct acmp *a, unsigned sink, const uint8_t *payload, unsigned len);
void old_acmp_restore_rollback(struct acmp *a);
void old_acmp_open(struct acmp *a);
bool old_acmp_binding_latch(const struct acmp *a, unsigned sink, uint8_t payload[ACMP_BINDING_BYTES]);
bool old_acmp_view(const struct acmp *a, unsigned sink, struct acmp_sink_view *view);
bool old_acmp_change_pending(const struct acmp *a, unsigned sink);
}
#define CALL(fn) (s.old ? old_##fn : fn)

static_assert(ACMP_MAX_INTERFACES <= sizeof(acmp::dirty_if) * 8u, "the interface mark holds a bit for every interface");

extern "C" void ctrl_reentry_assert(const char* module) {
    static_cast<void>(module);
}

namespace {

enum Kind : std::uint64_t { SEND, NOW, TIMER, GPTP, SEED, ADMIT, PUBLISH, LOCKED, SOURCE, SRP, PERSIST, CHANGED };

struct Side {
    acmp a{};
    bool room = true;
    std::uint32_t now = 50000;
    std::uint64_t gm[ACMP_MAX_INTERFACES] = {kGm0, kGm0, kGm0, kGm0};
    bool locked = false;
    std::uint64_t holder = 0;
    acmp_source_state source[ACMP_MAX_SOURCES] = {};
    std::vector<std::vector<std::uint64_t>> trace;
    bool old = false;
};

Side& side(void* ctx) {
    return *static_cast<Side*>(ctx);
}

bool w_send(void* ctx, unsigned interface, const std::uint8_t* frame, std::size_t len) {
    std::vector<std::uint64_t> call = {SEND, interface, len};
    for (std::size_t i = 0; i < len; ++i) {
        call.push_back(frame[i]);
    }
    side(ctx).trace.push_back(call);
    return side(ctx).room;
}

std::uint32_t w_now(void* ctx) {
    side(ctx).trace.push_back({NOW, side(ctx).now});
    return side(ctx).now;
}

void w_timer(void* ctx, unsigned interface, bool armed, std::uint32_t deadline) {
    side(ctx).trace.push_back({TIMER, interface, armed, deadline});
}

void w_gptp(void* ctx, unsigned interface, std::uint64_t* gm, std::uint8_t* domain) {
    side(ctx).trace.push_back({GPTP, interface});
    *gm = side(ctx).gm[interface];
    *domain = 0u;
}

std::uint32_t w_seed(void* ctx) {
    side(ctx).trace.push_back({SEED});
    return 0x5EEDu;
}

void w_admit(void* ctx, unsigned interface, unsigned sink, bool bound, std::uint64_t talker) {
    side(ctx).trace.push_back({ADMIT, interface, sink, bound, talker});
}

void w_publish(void* ctx, unsigned interface, unsigned sink, bool bound, bool started, std::uint64_t stream,
               bool moved) {
    side(ctx).trace.push_back({PUBLISH, interface, sink, bound, started, stream, moved});
}

bool w_locked(void* ctx, std::uint64_t* holder) {
    side(ctx).trace.push_back({LOCKED});
    *holder = side(ctx).holder;
    return side(ctx).locked;
}

void w_source(void* ctx, unsigned index, acmp_source_state* out) {
    side(ctx).trace.push_back({SOURCE, index});
    *out = side(ctx).source[index];
}

void w_srp(void* ctx, unsigned sink, const acmp_stream* stream) {
    if (stream == nullptr) {
        side(ctx).trace.push_back({SRP, sink, 0u});
        return;
    }
    side(ctx).trace.push_back({SRP, sink, 1u, stream->stream_id, stream->dest_mac, stream->vlan_id});
}

void w_persist(void* ctx, unsigned sink) {
    side(ctx).trace.push_back({PERSIST, sink});
}

void w_changed(void* ctx, unsigned sink) {
    side(ctx).trace.push_back({CHANGED, sink});
}


bool same_view(const acmp_sink_view& u, const acmp_sink_view& v) {
    return u.state == v.state && u.bound == v.bound && u.binding.talker_entity_id == v.binding.talker_entity_id &&
           u.binding.controller_entity_id == v.binding.controller_entity_id &&
           u.binding.talker_unique_id == v.binding.talker_unique_id && u.binding.streaming_wait == v.binding.streaming_wait &&
           u.started == v.started && u.probing_status == v.probing_status && u.acmp_status == v.acmp_status &&
           u.settled == v.settled && u.stream.stream_id == v.stream.stream_id && u.stream.dest_mac == v.stream.dest_mac &&
           u.stream.vlan_id == v.stream.vlan_id && u.talker_registered == v.talker_registered &&
           u.registering_failed == v.registering_failed && u.talker_discovered == v.talker_discovered;
}

struct Rng {
    std::uint32_t x;
    std::uint32_t next() {
        x ^= x << 13;
        x ^= x >> 17;
        x ^= x << 5;
        return x;
    }
    unsigned below(unsigned n) {
        return next() % n;
    }
};

class AcmpWalk : public ::testing::Test {
 protected:
    Side walked;
    Side full;
    acmp_ports ports[2] = {};
    acmp_env env[2] = {};
    acmp_config cfg = {};
    Rng rng{0x9E3779B9u};
    std::uint32_t seed = 0x9E3779B9u;
    bool wide = false;

    void start(unsigned sinks) {
        wide = sinks > 32u;
        cfg.entity_id = kOwn;
        cfg.n_interfaces = wide ? 3u : 2u;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.mac[2] = kMac1 + 1u;
        cfg.n_sinks = sinks;
        for (unsigned k = 0; k < sinks; ++k) {
            cfg.sink_interface[k] = static_cast<std::uint8_t>(k < 32u ? (k * 7u + k / 3u) % 2u : 2u);
        }
        cfg.n_sources = 2;
        cfg.source_interface[0] = 0;
        cfg.source_interface[1] = 1;
        Side* sides[2] = {&walked, &full};
        for (unsigned n = 0; n < 2u; ++n) {
            for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) {
                sides[n]->source[i] = acmp_source_state{i % 3u != 2u, {kSid + i, kDa + i, 2u}, i % 2u == 1u};
            }
            ports[n] = acmp_ports{sides[n], w_send, w_now, w_timer, w_gptp, w_seed, w_admit, w_publish};
            env[n] = acmp_env{sides[n], w_locked, w_source, w_srp, w_persist, w_changed};
            sides[n]->old = n == 1u;
            ASSERT_TRUE((n ? old_acmp_init : acmp_init)(&sides[n]->a, &cfg, &ports[n], &env[n])) << "both walk cores take the shape";
        }
    }

    void every_sink_marked() {
        for (std::uint32_t& word : full.a.dirty) {
            word = ~0u;
        }
        full.a.dirty_if = ~0u;
    }

    template <typename F>
    void both(F entry) {
        entry(walked);
        entry(full);
    }

    unsigned sink() {
        return rng.below(cfg.n_sinks);
    }

    unsigned sink_in(acmp_sink_state a, acmp_sink_state b, bool sent = false) {
        unsigned k = sink();
        for (unsigned n = 0; n < cfg.n_sinks; ++n) {
            unsigned j = (k + n) % cfg.n_sinks;
            const acmp_sink& s = walked.a.sinks[j];
            if ((s.state == a || s.state == b) && !(sent && s.timer_held)) {
                return j;
            }
        }
        return k;
    }

    unsigned commanded_sink() {
        return wide && rng.below(4u) == 0u ? cfg.n_sinks - 1u : sink();
    }

    void rx(const Pdu& p, unsigned interface) {
        auto f = acmpdu(p);
        both([&](Side& s) { CALL(acmp_rx)(&s.a, interface, f.data(), f.size()); });
    }

    void listener(std::uint8_t msg) {
        unsigned k = commanded_sink();
        Pdu p;
        p.msg = msg;
        p.controller = rng.below(4u) == 0u ? kCtl2 : kCtl1;
        p.talker = rng.below(3u) == 0u ? kTkB : kTkA;
        p.listener = kOwn;
        p.talker_uid = static_cast<std::uint16_t>(1u + rng.below(2u));
        p.listener_uid = static_cast<std::uint16_t>(k);
        p.flags = rng.below(4u) == 0u ? spec::FLAG_STREAMING_WAIT : 0u;
        p.seq = static_cast<std::uint16_t>(rng.next());
        rx(p, cfg.sink_interface[k]);
    }

    void probe_answer() {
        unsigned k = rng.below(5u) == 0u ? sink() : sink_in(ACMP_PRB_W_RESP, ACMP_PRB_W_RESP2, true);
        const acmp_sink& s = walked.a.sinks[k];
        Pdu p;
        p.msg = spec::MSG_PROBE_TX_RESPONSE;
        p.status = rng.below(4u) == 0u ? spec::STATUS_TALKER_DEST_MAC_FAIL : spec::STATUS_SUCCESS;
        p.controller = s.probe_controller;
        p.talker = s.probe_talker;
        p.listener = kOwn;
        p.talker_uid = s.probe_talker_uid;
        p.listener_uid = static_cast<std::uint16_t>(k);
        p.seq = rng.below(6u) == 0u ? static_cast<std::uint16_t>(s.probe_seq + 1u) : s.probe_seq;
        p.stream_id = kSid + rng.below(3u);
        p.dest_mac = kDa + rng.below(3u);
        p.vlan = static_cast<std::uint16_t>(2u + rng.below(2u));
        rx(p, s.interface);
    }

    void talker() {
        Pdu p;
        const std::uint8_t msgs[4] = {spec::MSG_PROBE_TX_COMMAND, spec::MSG_DISCONNECT_TX_COMMAND,
                                      spec::MSG_GET_TX_STATE_COMMAND, spec::MSG_GET_TX_CONNECTION_COMMAND};
        p.msg = msgs[rng.below(4u)];
        p.controller = kCtl1;
        p.talker = kOwn;
        p.listener = kTkA;
        p.talker_uid = static_cast<std::uint16_t>(rng.below(3u));
        p.seq = static_cast<std::uint16_t>(rng.next());
        rx(p, rng.below(cfg.n_interfaces));
    }

    void adp() {
        Adp d;
        d.msg = rng.below(5u) == 0u ? spec::ADPDU_ENTITY_DEPARTING : spec::ADPDU_ENTITY_AVAILABLE;
        d.entity = rng.below(3u) == 0u ? kTkB : kTkA;
        d.valid_time = static_cast<std::uint8_t>(1u + rng.below(4u));
        d.index = 1u + rng.below(6u);
        d.gm = rng.below(8u) == 0u ? kGm0 + 1u : kGm0;
        d.interface_index = static_cast<std::uint16_t>(rng.below(2u));
        auto f = adpdu(d);
        unsigned interface = rng.below(cfg.n_interfaces);
        both([&](Side& s) { CALL(acmp_adp_rx)(&s.a, interface, f.data(), f.size()); });
    }

    void restore() {
        unsigned k = wide && rng.below(2u) == 0u ? cfg.n_sinks - 1u : sink();
        std::array<std::uint8_t, spec::BINDING_BYTES> payload{};
        if (rng.below(3u) != 0u) {
            payload[0] = static_cast<std::uint8_t>(1u | (rng.below(2u) << 1));
            wire_put_be(payload.data() + 2, 1u + rng.below(2u), 2);
            wire_put_be(payload.data() + 4, rng.below(3u) == 0u ? kTkB : kTkA, 8);
            wire_put_be(payload.data() + 12, kCtl1, 8);
        }
        both([&](Side& s) { (void)CALL(acmp_restore_binding)(&s.a, k, payload.data(), spec::BINDING_BYTES); });
        both([&](Side& s) { CALL(acmp_open)(&s.a); });
    }

    void step() {
        if (wide && walked.a.owed_count != 0u && walked.room && rng.below(2u) == 0u) {
            both([&](Side& s) { (void)CALL(acmp_poll)(&s.a); });
            return;
        }
        unsigned r = rng.below(100u);
        if (r < 14u) {
            listener(spec::MSG_BIND_RX_COMMAND);
        } else if (r < 20u) {
            listener(spec::MSG_UNBIND_RX_COMMAND);
        } else if (r < 23u) {
            listener(spec::MSG_GET_RX_STATE_COMMAND);
        } else if (r < 33u) {
            probe_answer();
        } else if (r < 37u) {
            talker();
        } else if (r < 47u) {
            adp();
        } else if (r < 62u) {
            std::uint32_t ms = rng.below(5u) == 0u ? 4000u + rng.below(8000u) : rng.below(400u);
            unsigned interface = rng.below(cfg.n_interfaces);
            walked.now += ms;
            full.now += ms;
            both([&](Side& s) { CALL(acmp_timer_expired)(&s.a, interface); });
        } else if (r < 66u) {
            unsigned k = sink_in(ACMP_SETTLED_NO_RSV, ACMP_SETTLED_NO_RSV);
            bool failed = rng.below(2u) == 0u;
            both([&](Side& s) { CALL(acmp_tk_registered)(&s.a, k, failed); });
        } else if (r < 69u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            bool failed = rng.below(2u) == 0u;
            both([&](Side& s) { CALL(acmp_tk_kind_changed)(&s.a, k, failed); });
        } else if (r < 72u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            both([&](Side& s) { CALL(acmp_tk_unregistered)(&s.a, k); });
        } else if (r < 77u) {
            unsigned k = sink();
            bool started = rng.below(2u) == 0u;
            both([&](Side& s) { (void)CALL(acmp_set_started)(&s.a, k, started); });
        } else if (r < 87u) {
            both([&](Side& s) { (void)CALL(acmp_poll)(&s.a); });
        } else if (r < 92u) {
            bool room = rng.below(3u) != 0u;
            walked.room = room;
            full.room = room;
        } else if (r < 95u) {
            bool locked = rng.below(4u) == 0u;
            walked.locked = locked;
            full.locked = locked;
            walked.holder = kCtl2;
            full.holder = kCtl2;
        } else if (r < 98u) {
            restore();
        } else {
            both([&](Side& s) { CALL(acmp_restore_rollback)(&s.a); });
            both([&](Side& s) { CALL(acmp_open)(&s.a); });
        }
    }

    void walk(unsigned sinks, unsigned steps) {
        start(sinks);
        rng.x = seed;
        unsigned first = wide ? sinks - 1u : 0u;
        unsigned reached = 0;
        unsigned answers = 0;
        unsigned probes = 0;
        for (unsigned n = 0; n < steps; ++n) {
            unsigned head = walked.a.owed_head;
            unsigned of = walked.a.owed_count != 0u ? walked.a.owed[head].probe_of : 0u;
            bool held = of > first && walked.a.sinks[of - 1u].timer_held;
            step();
            ASSERT_TRUE(walked.trace == full.trace)
                << "the changed-sink walk makes the full walk's calls, in order, at step " << n << " of "
                << sinks << " sinks";
            for (std::uint32_t word : walked.a.dirty) {
                ASSERT_EQ(word, 0u) << "a completed entry leaves no sink marked, at step " << n << " of " << sinks
                                    << " sinks";
            }
            ASSERT_EQ(walked.a.dirty_if, 0u)
                << "a completed entry leaves no interface marked, at step " << n << " of " << sinks << " sinks";

            for (unsigned k = 0; k < sinks; ++k) {
                const acmp_sink& x = walked.a.sinks[k];
                const acmp_sink& y = full.a.sinks[k];
                ASSERT_EQ(std::memcmp(x.saved, y.saved, sizeof x.saved), 0) << "saved record, sink " << k << " step " << n;
                const acmp_sink_view& u = x.reported;
                const acmp_sink_view& v = y.reported;
                ASSERT_TRUE(same_view(u, v)) << "reported view, sink " << k << " step " << n;
                acmp_sink_view p{}, q{};
                ASSERT_TRUE(acmp_view(&walked.a, k, &p) && old_acmp_view(&full.a, k, &q));
                ASSERT_TRUE(same_view(p, q)) << "acmp_view, sink " << k << " step " << n;
                std::uint8_t r1[ACMP_BINDING_BYTES], r2[ACMP_BINDING_BYTES];
                ASSERT_TRUE(acmp_binding_latch(&walked.a, k, r1) && old_acmp_binding_latch(&full.a, k, r2));
                ASSERT_EQ(std::memcmp(r1, r2, sizeof r1), 0) << "binding latch, sink " << k << " step " << n;
                ASSERT_EQ(x.change_owed, y.change_owed) << "change owed, sink " << k << " step " << n;
            }
            walked.trace.clear();
            full.trace.clear();
            probes += held && walked.a.owed_head != head && !walked.a.sinks[of - 1u].timer_held ? 1u : 0u;
            for (unsigned k = first; k < sinks; ++k) {
                reached += walked.a.sinks[k].state == ACMP_SETTLED_RSV_OK ? 1u : 0u;
                answers += walked.a.sinks[k].change_owed != 0u ? 1u : 0u;
            }
        }
        EXPECT_NE(reached, 0u) << "the random entries reach a reservation, on the second mark word at 33 sinks";
        EXPECT_NE(answers, 0u) << "the random entries owe a sink's response, on the second mark word at 33 sinks";
        if (wide) {
            EXPECT_NE(probes, 0u) << "at 33 sinks the second mark word's sink sends an owed probe its timer waits for";
        }
    }
};

TEST_F(AcmpWalk, BaseAndHeadAgreeAt1Sinks) {
    if (1u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(1u, 4000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt2Sinks) {
    if (2u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(2u, 6000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt8Sinks) {
    if (8u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(8u, 8000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt9Sinks) {
    if (9u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(9u, 8000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt16Sinks) {
    if (16u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(16u, 8000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt32Sinks) {
    if (32u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(32u, 8000u);
        if (HasFatalFailure()) return;
    }
}
TEST_F(AcmpWalk, BaseAndHeadAgreeAt33Sinks) {
    if (33u > ACMP_MAX_SINKS) GTEST_SKIP();
    for (std::uint32_t s = 1; s <= 12u; ++s) {
        seed = 0x9E3779B9u * s + 7u;
        walk(33u, 10000u);
        if (HasFatalFailure()) return;
    }
}
}

// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: MIT
// Milan v1.2 5.5.3
// Milan v1.2 5.6.4

#include <gtest/gtest.h>

#include <array>
#include <cstdio>
#include <cstdint>
#include <cstring>
#include <string>
#include <vector>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "wire.h"

using namespace acmp_test;

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
    bool wide = false;
    unsigned ev_left = 0, ev_head = 0, ev_bind = 0, ev_unbind = 0, ev_kind = 0;

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
            ASSERT_TRUE(acmp_init(&sides[n]->a, &cfg, &ports[n], &env[n])) << "both walk cores take the shape";
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
        every_sink_marked();
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
        return wide && BIAS != 0u && rng.below(BIAS) == 0u ? cfg.n_sinks - 1u : sink();
    }

    void rx(const Pdu& p, unsigned interface) {
        auto f = acmpdu(p);
        both([&](Side& s) { acmp_rx(&s.a, interface, f.data(), f.size()); });
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
        both([&](Side& s) { acmp_adp_rx(&s.a, interface, f.data(), f.size()); });
    }

    void restore() {
        unsigned k = wide && RB && rng.below(2u) == 0u ? cfg.n_sinks - 1u : sink();
        std::array<std::uint8_t, spec::BINDING_BYTES> payload{};
        if (rng.below(3u) != 0u) {
            payload[0] = static_cast<std::uint8_t>(1u | (rng.below(2u) << 1));
            wire_put_be(payload.data() + 2, 1u + rng.below(2u), 2);
            wire_put_be(payload.data() + 4, rng.below(3u) == 0u ? kTkB : kTkA, 8);
            wire_put_be(payload.data() + 12, kCtl1, 8);
        }
        both([&](Side& s) { (void)acmp_restore_binding(&s.a, k, payload.data(), spec::BINDING_BYTES); });
        both([&](Side& s) { acmp_open(&s.a); });
    }

    void step() {
        if (wide && POLLB != 0u && walked.a.owed_count != 0u && walked.room && rng.below(POLLB) == 0u) {
            bool held = walked.a.sinks[32].timer_held;
            unsigned head = walked.a.owed_head;
            bool head32 = walked.a.owed[head].probe_of == 33u;
            both([&](Side& s) { (void)acmp_poll(&s.a); });
            if (head32 && held && !walked.a.sinks[32].timer_held) { ++ev_left; }
            if (head32) { ++ev_head; }
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
            both([&](Side& s) { acmp_timer_expired(&s.a, interface); });
        } else if (r < 66u) {
            unsigned k = sink_in(ACMP_SETTLED_NO_RSV, ACMP_SETTLED_NO_RSV);
            bool failed = rng.below(2u) == 0u;
            both([&](Side& s) { acmp_tk_registered(&s.a, k, failed); });
        } else if (r < 69u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            bool failed = rng.below(2u) == 0u;
            if (walked.a.sinks[k].state == ACMP_SETTLED_RSV_OK && walked.a.sinks[k].tk_failed != failed) { ++ev_kind; }
            both([&](Side& s) { acmp_tk_kind_changed(&s.a, k, failed); });
        } else if (r < 72u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            both([&](Side& s) { acmp_tk_unregistered(&s.a, k); });
        } else if (r < 77u) {
            unsigned k = sink();
            bool started = rng.below(2u) == 0u;
            both([&](Side& s) { (void)acmp_set_started(&s.a, k, started); });
        } else if (r < 87u) {
            bool held = wide && walked.a.sinks[32].timer_held;
            unsigned head = walked.a.owed_head;
            bool head32 = wide && walked.a.owed_count != 0u && walked.a.owed[head].probe_of == 33u;
            both([&](Side& s) { (void)acmp_poll(&s.a); });
            if (head32 && held && !walked.a.sinks[32].timer_held) { ++ev_left; }
            if (head32) { ++ev_head; if (0) printf("poll head32 room=%d held=%d seqmatch=%d after_held=%d state=%d count=%u\n", walked.room, held, (unsigned)((walked.a.owed[head].frame[14+48]<<8)|walked.a.owed[head].frame[14+49]) == walked.a.sinks[32].probe_seq, walked.a.sinks[32].timer_held, walked.a.sinks[32].state, walked.a.owed_count); }
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
            both([&](Side& s) { acmp_restore_rollback(&s.a); });
            both([&](Side& s) { acmp_open(&s.a); });
        }
    }

    void walk(unsigned sinks, unsigned steps) {
        start(sinks);
        unsigned reached = 0;
        unsigned answers = 0;
        unsigned probes = 0;
        for (unsigned n = 0; n < steps; ++n) {
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
            walked.trace.clear();
            full.trace.clear();
            for (unsigned k = wide ? sinks - 1u : 0u; k < sinks; ++k) {
                reached += walked.a.sinks[k].state == ACMP_SETTLED_RSV_OK ? 1u : 0u;
                answers += walked.a.sinks[k].change_owed != 0u ? 1u : 0u;
                probes += walked.a.sinks[k].timer_held ? 1u : 0u;
            }
        }
        printf("sinks=%u left=%u head=%u answers=%u probes=%u reached=%u kind=%u\n", sinks, ev_left, ev_head, answers, probes, reached, ev_kind);
        EXPECT_NE(reached, 0u) << "the random entries reach a reservation, on the second mark word at 33 sinks";
        EXPECT_NE(answers, 0u) << "the random entries owe a sink's response, on the second mark word at 33 sinks";
        EXPECT_NE(probes, 0u) << "the random entries owe a sink's probe, on the second mark word at 33 sinks";
    }
};

// REQ: ACMP-13, ACMP-10, ACMP-09, ACMP-05
TEST_F(AcmpWalk, OneSinkMatchesTheFullWalk) {
    walk(1u, 4000u);
}

// REQ: ACMP-13, ACMP-10, ACMP-09, ACMP-05
TEST_F(AcmpWalk, EightSinksMatchTheFullWalk) {
    walk(8u, 6000u);
}

// REQ: ACMP-13, ACMP-10, ACMP-09, ACMP-05
TEST_F(AcmpWalk, ThirtyTwoSinksMatchTheFullWalk) {
    walk(32u, 8000u);
}

// REQ: ACMP-13, ACMP-10, ACMP-05
TEST_F(AcmpWalk, ThirtyThreeSinksMatchTheFullWalk) {
    ASSERT_EQ(ACMP_MAX_SINKS, 33u) << "the walk test's core holds a second mark word";
    walk(33u, STEPS);
}

}

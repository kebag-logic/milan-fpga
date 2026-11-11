// SPDX-License-Identifier: MIT
// Reviewer probe for tsn-c-stack #32: one ACMP core driven by the random entry sequence of
// tests/test_acmp_walk.cpp, every port and environment call recorded. Linked once against the
// head's src/acmp.c and once against main's, the two outputs must be byte-identical.
// Usage: trace_walk SINKS STEPS SEED LIFT
//   LIFT 0: the head test's entry mix (at 33 sinks no command to sink 32 and no room withdrawn).
//   LIFT 1: commands reach every sink, room is withdrawn at every size, a restore is not always
//           followed at once by acmp_open, and restores may come twice before the open.
// Output: one line per step, "step calls fnv64", then a line with the totals.
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

#include "acmp.h"
#include "acmp_fake.hpp"
#include "wire.h"

using namespace acmp_test;

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
    unsigned long counts[12] = {};
};

Side& side(void* ctx) { return *static_cast<Side*>(ctx); }
void rec(void* ctx, std::vector<std::uint64_t> c) { side(ctx).counts[c[0]]++; side(ctx).trace.push_back(std::move(c)); }

bool w_send(void* ctx, unsigned interface, const std::uint8_t* frame, std::size_t len) {
    std::vector<std::uint64_t> call = {SEND, interface, len};
    for (std::size_t i = 0; i < len; ++i) call.push_back(frame[i]);
    rec(ctx, call);
    return side(ctx).room;
}
std::uint32_t w_now(void* ctx) { rec(ctx, {NOW, side(ctx).now}); return side(ctx).now; }
void w_timer(void* ctx, unsigned i, bool armed, std::uint32_t d) { rec(ctx, {TIMER, i, armed, d}); }
void w_gptp(void* ctx, unsigned i, std::uint64_t* gm, std::uint8_t* domain) { rec(ctx, {GPTP, i}); *gm = side(ctx).gm[i]; *domain = 0u; }
std::uint32_t w_seed(void* ctx) { rec(ctx, {SEED}); return 0x5EEDu; }
void w_admit(void* ctx, unsigned i, unsigned k, bool b, std::uint64_t t) { rec(ctx, {ADMIT, i, k, b, t}); }
void w_publish(void* ctx, unsigned i, unsigned k, bool b, bool s, std::uint64_t st, bool m) { rec(ctx, {PUBLISH, i, k, b, s, st, m}); }
bool w_locked(void* ctx, std::uint64_t* h) { rec(ctx, {LOCKED}); *h = side(ctx).holder; return side(ctx).locked; }
void w_source(void* ctx, unsigned i, acmp_source_state* out) { rec(ctx, {SOURCE, i}); *out = side(ctx).source[i]; }
void w_srp(void* ctx, unsigned k, const acmp_stream* s) {
    if (s == nullptr) { rec(ctx, {SRP, k, 0u}); return; }
    rec(ctx, {SRP, k, 1u, s->stream_id, s->dest_mac, s->vlan_id});
}
void w_persist(void* ctx, unsigned k) { rec(ctx, {PERSIST, k}); }
void w_changed(void* ctx, unsigned k) { rec(ctx, {CHANGED, k}); }

struct Rng {
    std::uint32_t x;
    std::uint32_t next() { x ^= x << 13; x ^= x >> 17; x ^= x << 5; return x; }
    unsigned below(unsigned n) { return next() % n; }
};

struct Walk {
    Side w;
    acmp_ports ports{};
    acmp_env env{};
    acmp_config cfg{};
    Rng rng{0x9E3779B9u};
    bool wide = false;
    bool lift = false;
    bool open_owed = false;

    void start(unsigned sinks) {
        wide = sinks > 32u;
        cfg.entity_id = kOwn;
        cfg.n_interfaces = 2;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.n_sinks = sinks;
        for (unsigned k = 0; k < sinks; ++k) cfg.sink_interface[k] = static_cast<std::uint8_t>((k * 7u + k / 3u) % 2u);
        cfg.n_sources = 2;
        cfg.source_interface[0] = 0;
        cfg.source_interface[1] = 1;
        for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i) w.source[i] = acmp_source_state{i % 3u != 2u, {kSid + i, kDa + i, 2u}, i % 2u == 1u};
        ports = acmp_ports{&w, w_send, w_now, w_timer, w_gptp, w_seed, w_admit, w_publish};
        env = acmp_env{&w, w_locked, w_source, w_srp, w_persist, w_changed};
        if (!acmp_init(&w.a, &cfg, &ports, &env)) { std::puts("init refused"); std::exit(3); }
    }
    unsigned sink() { return rng.below(cfg.n_sinks); }
    unsigned sink_in(acmp_sink_state a, acmp_sink_state b, bool sent = false) {
        unsigned k = sink();
        for (unsigned n = 0; n < cfg.n_sinks; ++n) {
            unsigned j = (k + n) % cfg.n_sinks;
            const acmp_sink& s = w.a.sinks[j];
            if ((s.state == a || s.state == b) && !(sent && s.timer_held)) return j;
        }
        return k;
    }
    unsigned commanded_sink() {
        unsigned k = sink();
        return wide && !lift && k >= 32u ? k - 32u : k;
    }
    void rx(const Pdu& p, unsigned interface) { auto f = acmpdu(p); acmp_rx(&w.a, interface, f.data(), f.size()); }
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
        const acmp_sink& s = w.a.sinks[k];
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
        rx(p, rng.below(2u));
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
        unsigned interface = rng.below(2u);
        acmp_adp_rx(&w.a, interface, f.data(), f.size());
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
        (void)acmp_restore_binding(&w.a, k, payload.data(), spec::BINDING_BYTES);
        if (lift && rng.below(2u) == 0u) { open_owed = true; return; }   // the open comes after later entries
        acmp_open(&w.a);
        open_owed = false;
    }
    void step() {
        unsigned r = rng.below(100u);
        if (r < 14u) listener(spec::MSG_BIND_RX_COMMAND);
        else if (r < 20u) listener(spec::MSG_UNBIND_RX_COMMAND);
        else if (r < 23u) listener(spec::MSG_GET_RX_STATE_COMMAND);
        else if (r < 33u) probe_answer();
        else if (r < 37u) talker();
        else if (r < 47u) adp();
        else if (r < 62u) {
            std::uint32_t ms = rng.below(5u) == 0u ? 4000u + rng.below(8000u) : rng.below(400u);
            unsigned interface = rng.below(2u);
            w.now += ms;
            acmp_timer_expired(&w.a, interface);
        } else if (r < 66u) {
            unsigned k = sink_in(ACMP_SETTLED_NO_RSV, ACMP_SETTLED_NO_RSV);
            acmp_tk_registered(&w.a, k, rng.below(2u) == 0u);
        } else if (r < 69u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            acmp_tk_kind_changed(&w.a, k, rng.below(2u) == 0u);
        } else if (r < 72u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            acmp_tk_unregistered(&w.a, k);
        } else if (r < 77u) {
            unsigned k = sink();
            bool started = rng.below(2u) == 0u;
            (void)acmp_set_started(&w.a, k, started);
        } else if (r < 87u) {
            (void)acmp_poll(&w.a);
        } else if (r < 92u) {
            w.room = (wide && !lift) || rng.below(3u) != 0u;
        } else if (r < 95u) {
            w.locked = rng.below(4u) == 0u;
            w.holder = kCtl2;
        } else if (r < 98u) {
            restore();
        } else {
            acmp_restore_rollback(&w.a);
            if (lift && rng.below(2u) == 0u) { open_owed = true; return; }
            acmp_open(&w.a);
            open_owed = false;
        }
        if (lift && open_owed && rng.below(4u) == 0u) { acmp_open(&w.a); open_owed = false; }
    }
};

std::uint64_t fnv(const std::vector<std::vector<std::uint64_t>>& t) {
    std::uint64_t h = 0xcbf29ce484222325ull;
    for (const auto& c : t) {
        for (std::uint64_t v : c) { h ^= v; h *= 0x100000001b3ull; }
        h ^= 0xFFFFull; h *= 0x100000001b3ull;
    }
    return h;
}

}

int main(int argc, char** argv) {
    if (argc != 5) { std::fputs("usage: trace_walk SINKS STEPS SEED LIFT\n", stderr); return 2; }
    unsigned sinks = static_cast<unsigned>(std::strtoul(argv[1], nullptr, 0));
    unsigned steps = static_cast<unsigned>(std::strtoul(argv[2], nullptr, 0));
    Walk walk;
    walk.rng.x = static_cast<std::uint32_t>(std::strtoul(argv[3], nullptr, 0));
    walk.lift = std::strtoul(argv[4], nullptr, 0) != 0;
    walk.start(sinks);
    unsigned long reached_last = 0, owed_max = 0, changed_hi = 0, unbound_hi = 0;
    for (unsigned n = 0; n < steps; ++n) {
        walk.step();
        std::printf("%u %zu %016llx\n", n, walk.w.trace.size(), static_cast<unsigned long long>(fnv(walk.w.trace)));
        for (const auto& c : walk.w.trace) {
            if (c[0] == CHANGED && c[1] >= 32u) changed_hi++;
            if (c[0] == PUBLISH && c[2] >= 32u && c[3] == 0u) unbound_hi++;
        }
        walk.w.trace.clear();
        if (walk.w.a.sinks[sinks - 1u].state == ACMP_SETTLED_RSV_OK) reached_last++;
        if (walk.w.a.owed_count > owed_max) owed_max = walk.w.a.owed_count;
    }
    std::printf("totals sends %lu changed %lu persist %lu publish %lu admit %lu timer %lu now %lu | last-sink-registered-steps %lu owed-max %lu changed-sink>=32 %lu unbound-publish-sink>=32 %lu\n",
                walk.w.counts[SEND], walk.w.counts[CHANGED], walk.w.counts[PERSIST], walk.w.counts[PUBLISH], walk.w.counts[ADMIT],
                walk.w.counts[TIMER], walk.w.counts[NOW], reached_last, owed_max, changed_hi, unbound_hi);
    return 0;
}

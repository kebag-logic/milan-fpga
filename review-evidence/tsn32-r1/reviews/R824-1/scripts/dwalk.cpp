// SPDX-License-Identifier: MIT
// Reviewer probe (issue 32): drive the head ACMP core (changed-sink walk) and main's ACMP core (old_ prefix, built
// from main's src/acmp.c with its own header) with the same random entries, and require after every entry the same
// port and environment calls in the same order, the same return values, and the same public view, binding latch and
// change-pending state of every sink.
// Environment knobs: SINKS, STEPS, SEED, LIFT (1: BIND/UNBIND reach sinks >= 32 and transmit room may be withdrawn at
// any sink count), REENTER (1: callbacks try to re-enter both cores), NOOPEN (1: restore is not followed by open;
// open is its own random entry).
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

extern "C" {
void ctrl_reentry_assert(const char*) {}
bool old_acmp_init(acmp*, const acmp_config*, const acmp_ports*, const acmp_env*);
bool old_acmp_rx(acmp*, unsigned, const std::uint8_t*, std::size_t);
void old_acmp_adp_rx(acmp*, unsigned, const std::uint8_t*, std::size_t);
void old_acmp_timer_expired(acmp*, unsigned);
void old_acmp_tk_registered(acmp*, unsigned, bool);
void old_acmp_tk_kind_changed(acmp*, unsigned, bool);
void old_acmp_tk_unregistered(acmp*, unsigned);
bool old_acmp_set_started(acmp*, unsigned, bool);
bool old_acmp_poll(acmp*);
bool old_acmp_listener_registered(acmp*, unsigned, unsigned, bool);
bool old_acmp_declaring(acmp*, unsigned);
acmp_restore old_acmp_restore_binding(acmp*, unsigned, const std::uint8_t*, unsigned);
void old_acmp_restore_rollback(acmp*);
void old_acmp_open(acmp*);
bool old_acmp_binding_latch(const acmp*, unsigned, std::uint8_t*);
bool old_acmp_view(const acmp*, unsigned, acmp_sink_view*);
bool old_acmp_change_pending(const acmp*, unsigned);
bool old_acmp_rx_ready(const acmp*);
}

namespace {

struct Api {
    decltype(&acmp_init) init;
    decltype(&acmp_rx) rx;
    decltype(&acmp_adp_rx) adp_rx;
    decltype(&acmp_timer_expired) expired;
    decltype(&acmp_tk_registered) registered;
    decltype(&acmp_tk_kind_changed) kind;
    decltype(&acmp_tk_unregistered) unregistered;
    decltype(&acmp_set_started) started;
    decltype(&acmp_poll) poll;
    decltype(&acmp_listener_registered) lreg;
    decltype(&acmp_declaring) declaring;
    decltype(&acmp_restore_binding) restore;
    decltype(&acmp_restore_rollback) rollback;
    decltype(&acmp_open) open;
    bool (*latch)(const acmp*, unsigned, std::uint8_t*);
    decltype(&acmp_view) view;
    decltype(&acmp_change_pending) pending;
    decltype(&acmp_rx_ready) ready;
};
const Api kNew = {acmp_init, acmp_rx, acmp_adp_rx, acmp_timer_expired, acmp_tk_registered, acmp_tk_kind_changed,
                  acmp_tk_unregistered, acmp_set_started, acmp_poll, acmp_listener_registered, acmp_declaring,
                  acmp_restore_binding, acmp_restore_rollback, acmp_open, acmp_binding_latch, acmp_view,
                  acmp_change_pending, acmp_rx_ready};
const Api kOld = {old_acmp_init, old_acmp_rx, old_acmp_adp_rx, old_acmp_timer_expired, old_acmp_tk_registered,
                  old_acmp_tk_kind_changed, old_acmp_tk_unregistered, old_acmp_set_started, old_acmp_poll,
                  old_acmp_listener_registered, old_acmp_declaring, old_acmp_restore_binding,
                  old_acmp_restore_rollback, old_acmp_open, old_acmp_binding_latch, old_acmp_view,
                  old_acmp_change_pending, old_acmp_rx_ready};

enum Kind : std::uint64_t { SEND, NOW, TIMER, GPTP, SEED, ADMIT, PUBLISH, LOCKED, SOURCE, SRP, PERSIST, CHANGED, RET,
                            REENTRY };

struct Side {
    acmp a{};  // the old core uses a prefix of this storage: main's struct acmp lacks the two mark fields
    const Api* api = nullptr;
    bool room = true;
    std::uint32_t now = 50000;
    std::uint64_t gm[ACMP_MAX_INTERFACES] = {kGm0, kGm0, kGm0, kGm0};
    bool locked = false;
    std::uint64_t holder = 0;
    acmp_source_state source[ACMP_MAX_SOURCES] = {};
    unsigned reenter = 0;  // nonzero: the next callback tries to re-enter with this selector
    std::vector<std::vector<std::uint64_t>> trace;
};
Side& side(void* ctx) { return *static_cast<Side*>(ctx); }

void try_reenter(Side& s) {
    if (s.reenter == 0u) {
        return;
    }
    unsigned r = s.reenter;
    s.reenter = 0u;
    std::uint64_t got = 0;
    if (r % 4u == 0u) {
        got = s.api->started(&s.a, 0u, true);
    } else if (r % 4u == 1u) {
        got = s.api->poll(&s.a);
    } else if (r % 4u == 2u) {
        Pdu p;
        p.msg = spec::MSG_UNBIND_RX_COMMAND;
        p.controller = kCtl1;
        p.listener = kOwn;
        p.listener_uid = 0u;
        auto f = acmpdu(p);
        got = s.api->rx(&s.a, 0u, f.data(), f.size());
    } else {
        s.api->rollback(&s.a);
    }
    s.trace.push_back({REENTRY, r, got});
}

bool w_send(void* ctx, unsigned interface, const std::uint8_t* frame, std::size_t len) {
    std::vector<std::uint64_t> call = {SEND, interface, len};
    for (std::size_t i = 0; i < len; ++i) call.push_back(frame[i]);
    side(ctx).trace.push_back(call);
    try_reenter(side(ctx));
    return side(ctx).room;
}
std::uint32_t w_now(void* ctx) { side(ctx).trace.push_back({NOW, side(ctx).now}); return side(ctx).now; }
void w_timer(void* ctx, unsigned i, bool armed, std::uint32_t d) { side(ctx).trace.push_back({TIMER, i, armed, d}); try_reenter(side(ctx)); }
void w_gptp(void* ctx, unsigned i, std::uint64_t* gm, std::uint8_t* domain) {
    side(ctx).trace.push_back({GPTP, i}); *gm = side(ctx).gm[i]; *domain = 0u;
}
std::uint32_t w_seed(void* ctx) { side(ctx).trace.push_back({SEED}); return 0x5EEDu; }
void w_admit(void* ctx, unsigned i, unsigned k, bool b, std::uint64_t t) { side(ctx).trace.push_back({ADMIT, i, k, b, t}); try_reenter(side(ctx)); }
void w_publish(void* ctx, unsigned i, unsigned k, bool b, bool st, std::uint64_t x, bool m) {
    side(ctx).trace.push_back({PUBLISH, i, k, b, st, x, m}); try_reenter(side(ctx));
}
bool w_locked(void* ctx, std::uint64_t* h) { side(ctx).trace.push_back({LOCKED}); *h = side(ctx).holder; return side(ctx).locked; }
void w_source(void* ctx, unsigned i, acmp_source_state* out) { side(ctx).trace.push_back({SOURCE, i}); *out = side(ctx).source[i]; }
void w_srp(void* ctx, unsigned k, const acmp_stream* x) {
    if (x == nullptr) { side(ctx).trace.push_back({SRP, k, 0u}); return; }
    side(ctx).trace.push_back({SRP, k, 1u, x->stream_id, x->dest_mac, x->vlan_id});
}
void w_persist(void* ctx, unsigned k) { side(ctx).trace.push_back({PERSIST, k}); try_reenter(side(ctx)); }
void w_changed(void* ctx, unsigned k) { side(ctx).trace.push_back({CHANGED, k}); try_reenter(side(ctx)); }

struct Rng {
    std::uint32_t x;
    std::uint32_t next() { x ^= x << 13; x ^= x >> 17; x ^= x << 5; return x; }
    unsigned below(unsigned n) { return next() % n; }
};

unsigned env(const char* name, unsigned dflt) {
    const char* v = std::getenv(name);
    return v ? static_cast<unsigned>(std::strtoul(v, nullptr, 0)) : dflt;
}

struct Probe {
    Side walked, old;
    acmp_ports ports[2] = {};
    acmp_env envs[2] = {};
    acmp_config cfg = {};
    Rng rng{0x9E3779B9u};
    unsigned sinks = 8, lift = 0, reenter = 0, noopen = 0;
    bool restricted = false;

    template <typename F> void both(F f) { f(walked); f(old); }
    void ret(std::uint64_t a, std::uint64_t b) { walked.trace.push_back({RET, a}); old.trace.push_back({RET, b}); }
    unsigned sink() { return rng.below(cfg.n_sinks); }
    unsigned sink_in(acmp_sink_state a, acmp_sink_state b, bool sent = false) {
        unsigned k = sink();
        for (unsigned n = 0; n < cfg.n_sinks; ++n) {
            unsigned j = (k + n) % cfg.n_sinks;
            const acmp_sink& s = walked.a.sinks[j];
            if ((s.state == a || s.state == b) && !(sent && s.timer_held)) return j;
        }
        return k;
    }
    unsigned commanded_sink() { unsigned k = sink(); return restricted && k >= 32u ? k - 32u : k; }
    void arm_reentry() {
        if (reenter && rng.below(6u) == 0u) {
            unsigned r = 1u + rng.below(400u);
            walked.reenter = r;
            old.reenter = r;
        }
    }
    void rx(const Pdu& p, unsigned interface) {
        auto f = acmpdu(p);
        arm_reentry();
        bool x = walked.api->rx(&walked.a, interface, f.data(), f.size());
        bool y = old.api->rx(&old.a, interface, f.data(), f.size());
        ret(x, y);
    }
    void listener(std::uint8_t msg) {
        unsigned k = commanded_sink();
        Pdu p;
        p.msg = msg;
        p.controller = rng.below(4u) == 0u ? kCtl2 : kCtl1;
        p.talker = rng.below(3u) == 0u ? kTkB : kTkA;
        p.listener = rng.below(40u) == 0u ? kTkB : kOwn;
        p.talker_uid = static_cast<std::uint16_t>(1u + rng.below(2u));
        p.listener_uid = static_cast<std::uint16_t>(rng.below(50u) == 0u ? cfg.n_sinks + rng.below(3u) : k);
        p.flags = rng.below(4u) == 0u ? spec::FLAG_STREAMING_WAIT : 0u;
        p.seq = static_cast<std::uint16_t>(rng.next());
        rx(p, k < cfg.n_sinks ? cfg.sink_interface[k] : 0u);
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
        arm_reentry();
        both([&](Side& s) { s.api->adp_rx(&s.a, interface, f.data(), f.size()); });
    }
    void restore() {
        unsigned k = cfg.n_sinks > 32u && rng.below(2u) == 0u ? 32u + rng.below(cfg.n_sinks - 32u) : sink();
        std::array<std::uint8_t, spec::BINDING_BYTES> payload{};
        if (rng.below(3u) != 0u) {
            payload[0] = static_cast<std::uint8_t>(1u | (rng.below(2u) << 1) | (rng.below(4u) == 0u ? 4u : 0u));
            wire_put_be(payload.data() + 2, 1u + rng.below(2u), 2);
            wire_put_be(payload.data() + 4, rng.below(3u) == 0u ? kTkB : kTkA, 8);
            wire_put_be(payload.data() + 12, kCtl1, 8);
        }
        ret(walked.api->restore(&walked.a, k, payload.data(), spec::BINDING_BYTES),
            old.api->restore(&old.a, k, payload.data(), spec::BINDING_BYTES));
        if (!noopen) both([&](Side& s) { s.api->open(&s.a); });
    }
    void step() {
        unsigned r = rng.below(102u);
        if (r < 14u) listener(spec::MSG_BIND_RX_COMMAND);
        else if (r < 20u) listener(spec::MSG_UNBIND_RX_COMMAND);
        else if (r < 23u) listener(spec::MSG_GET_RX_STATE_COMMAND);
        else if (r < 33u) probe_answer();
        else if (r < 37u) talker();
        else if (r < 47u) adp();
        else if (r < 62u) {
            std::uint32_t ms = rng.below(5u) == 0u ? 4000u + rng.below(8000u) : rng.below(400u);
            unsigned interface = rng.below(2u);
            walked.now += ms;
            old.now += ms;
            arm_reentry();
            both([&](Side& s) { s.api->expired(&s.a, interface); });
        } else if (r < 66u) {
            unsigned k = sink_in(ACMP_SETTLED_NO_RSV, ACMP_SETTLED_NO_RSV);
            bool failed = rng.below(2u) == 0u;
            arm_reentry();
            both([&](Side& s) { s.api->registered(&s.a, k, failed); });
        } else if (r < 69u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            bool failed = rng.below(2u) == 0u;
            both([&](Side& s) { s.api->kind(&s.a, k, failed); });
        } else if (r < 72u) {
            unsigned k = sink_in(ACMP_SETTLED_RSV_OK, ACMP_SETTLED_RSV_OK);
            both([&](Side& s) { s.api->unregistered(&s.a, k); });
        } else if (r < 77u) {
            unsigned k = sink();
            bool started = rng.below(2u) == 0u;
            arm_reentry();
            ret(walked.api->started(&walked.a, k, started), old.api->started(&old.a, k, started));
        } else if (r < 87u) {
            arm_reentry();
            ret(walked.api->poll(&walked.a), old.api->poll(&old.a));
        } else if (r < 92u) {
            bool room = (restricted && !lift) || rng.below(3u) != 0u;
            walked.room = room;
            old.room = room;
        } else if (r < 95u) {
            bool locked = rng.below(4u) == 0u;
            walked.locked = old.locked = locked;
            walked.holder = old.holder = kCtl2;
        } else if (r < 98u) {
            restore();
        } else if (r < 99u) {
            both([&](Side& s) { s.api->rollback(&s.a); });
            if (!noopen) both([&](Side& s) { s.api->open(&s.a); });
        } else if (r < 100u) {
            both([&](Side& s) { s.api->open(&s.a); });
        } else if (r < 101u) {
            unsigned src = rng.below(2u);
            ret(walked.api->declaring(&walked.a, src), old.api->declaring(&old.a, src));
        } else {
            unsigned src = rng.below(2u);
            bool reg = rng.below(2u) == 0u;
            ret(walked.api->lreg(&walked.a, src, src, reg), old.api->lreg(&old.a, src, src, reg));
        }
    }
    bool same_state(unsigned n) {
        for (unsigned k = 0; k < cfg.n_sinks; ++k) {
            acmp_sink_view x{}, y{};
            walked.api->view(&walked.a, k, &x);
            old.api->view(&old.a, k, &y);
            std::uint8_t lx[ACMP_BINDING_BYTES], ly[ACMP_BINDING_BYTES];
            walked.api->latch(&walked.a, k, lx);
            old.api->latch(&old.a, k, ly);
            if (std::memcmp(&x, &y, sizeof x) != 0 || std::memcmp(lx, ly, sizeof lx) != 0 ||
                walked.api->pending(&walked.a, k) != old.api->pending(&old.a, k)) {
                std::printf("STATE DIFFERS at step %u sink %u\n", n, k);
                return false;
            }
        }
        if (walked.api->ready(&walked.a) != old.api->ready(&old.a)) {
            std::printf("READY DIFFERS at step %u\n", n);
            return false;
        }
        return true;
    }
    int run() {
        sinks = env("SINKS", 8);
        unsigned steps = env("STEPS", 20000);
        rng.x = env("SEED", 0x9E3779B9u) | 1u;
        lift = env("LIFT", 0);
        reenter = env("REENTER", 0);
        noopen = env("NOOPEN", 0);
        restricted = sinks > 32u;
        cfg.entity_id = kOwn;
        cfg.n_interfaces = 2;
        cfg.mac[0] = kMac0;
        cfg.mac[1] = kMac1;
        cfg.n_sinks = sinks;
        for (unsigned k = 0; k < sinks; ++k) cfg.sink_interface[k] = static_cast<std::uint8_t>((k * 7u + k / 3u) % 2u);
        cfg.n_sources = 2;
        cfg.source_interface[0] = 0;
        cfg.source_interface[1] = 1;
        walked.api = &kNew;
        old.api = &kOld;
        Side* sides[2] = {&walked, &old};
        for (unsigned n = 0; n < 2u; ++n) {
            for (unsigned i = 0; i < ACMP_MAX_SOURCES; ++i)
                sides[n]->source[i] = acmp_source_state{i % 3u != 2u, {kSid + i, kDa + i, 2u}, i % 2u == 1u};
            ports[n] = acmp_ports{sides[n], w_send, w_now, w_timer, w_gptp, w_seed, w_admit, w_publish};
            envs[n] = acmp_env{sides[n], w_locked, w_source, w_srp, w_persist, w_changed};
            if (!sides[n]->api->init(&sides[n]->a, &cfg, &ports[n], &envs[n])) {
                std::printf("init refused\n");
                return 2;
            }
        }
        if (lift) restricted = false;
        unsigned long calls = 0, owed_steps = 0, settled_hi = 0, reentries = 0, rsv = 0;
        for (unsigned n = 0; n < steps; ++n) {
            step();
            if (walked.trace != old.trace) {
                std::printf("TRACE DIFFERS at step %u (%zu vs %zu calls)\n", n, walked.trace.size(), old.trace.size());
                return 1;
            }
            if (!same_state(n)) return 1;
            calls += walked.trace.size();
            for (auto& c : walked.trace) reentries += c[0] == REENTRY;
            walked.trace.clear();
            old.trace.clear();
            owed_steps += walked.a.owed_count != 0u;
            for (unsigned k = 0; k < sinks; ++k) {
                rsv += walked.a.sinks[k].state == ACMP_SETTLED_RSV_OK;
                if (k >= 32u) settled_hi += walked.a.sinks[k].state == ACMP_SETTLED_RSV_OK;
            }
        }
        std::printf("PASS max_sinks %u sinks %u steps %u seed 0x%08x lift %u reenter %u noopen %u: calls %lu, steps with "
                    "owed frames %lu, reentry attempts %lu, settled-rsv sink-steps %lu (sinks>=32: %lu), deferred %u\n",
                    static_cast<unsigned>(ACMP_MAX_SINKS), sinks, steps, env("SEED", 0x9E3779B9u) | 1u, lift, reenter,
                    noopen, calls, owed_steps, reentries, rsv, settled_hi, walked.a.deferred_sends);
        return 0;
    }
};

}  // namespace

int main() {
    static Probe p;
    return p.run();
}

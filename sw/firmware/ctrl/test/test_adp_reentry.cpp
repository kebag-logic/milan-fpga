// SPDX-License-Identifier: CERN-OHL-W-2.0
// Host-only violating ports: debug assertions and release refusal on the same calls.

#include <gtest/gtest.h>

#include <array>
#include <csignal>
#include <cstdint>
#include <cstdlib>
#include <cstring>
#include <tuple>

#include "fw_gtest.hpp"
extern "C" {
#include "adp.h"
#ifdef ADP_TEST_COVERAGE
void __gcov_dump(void);
#endif
}

namespace fw_test {
const char* tally_label() {
#ifdef ADP_TEST_RELEASE
    return "ADP release re-entry";
#else
    return "ADP debug re-entry";
#endif
}
}

namespace {
enum class Port { Send, Start, Stop, Gptp, Link, Seed };
enum class Entry { Init, Enable, Configuration, Rx, Timer, Link, Gm, Poll, Build, Count };

#ifndef ADP_TEST_RELEASE
// Preserve the assertion's real stderr diagnostic and terminate the child.
// gcov normally loses an aborting child's counters; flush them for coverage.
void assertion_exit(int) {
#ifdef ADP_TEST_COVERAGE
    __gcov_dump();
#endif
    std::_Exit(86);
}
#endif

struct Rig {
    adp a{};
    adp other{};
    adp_entity entity{};
    adp_ports ports{};
    Port selected = Port::Start;
    Entry entry = Entry::Timer;
    bool inject = false;
    bool cross_instance = false;
    bool running = false;
    std::uint32_t delay = 0;
    unsigned callbacks = 0;

    Rig() {
        ports = {this, send, start, stop, gptp, link, seed};
        adp_init(&a, &entity, &ports, 0, 0);
        adp_init(&other, &entity, &ports, 1, 0);
    }

    void callback(Port port) {
        if (!inject || port != selected) {
            return;
        }
        inject = false;  // a missing guard must not recurse indefinitely
        ++callbacks;
        adp* target = cross_instance ? &other : &a;
        std::array<unsigned char, sizeof(adp)> before{};
        std::memcpy(before.data(), target, sizeof(adp));
        std::array<std::uint8_t, ADP_FRAME_BYTES> frame{};
        frame.fill(0xA5);
        switch (entry) {
        case Entry::Init: adp_init(target, &entity, &ports, 7, 9); break;
        case Entry::Enable: adp_set_enable(target, !target->enabled); break;
        case Entry::Configuration: adp_set_current_configuration(target, 7); break;
        case Entry::Rx: adp_rx(target, nullptr, 0); break;
        case Entry::Timer: adp_timer_expired(target); break;
        case Entry::Link: adp_link_change(target, !target->link_up); break;
        case Entry::Gm: adp_gm_change(target); break;
        case Entry::Poll: EXPECT_FALSE(adp_poll(target)); break;
        case Entry::Build: adp_build(target, ADP_MSG_ENTITY_AVAILABLE, 1, frame.data()); break;
        case Entry::Count: static_cast<void>(adp_reentry_count()); break;
        }
        EXPECT_EQ(std::memcmp(before.data(), target, sizeof(adp)), 0) << "callback leaves core state unchanged";
        for (const auto byte : frame) {
            EXPECT_EQ(byte, 0xA5) << "callback leaves output unchanged";
        }
    }

    static bool send(void* ctx, unsigned, const std::uint8_t*, std::size_t) {
        static_cast<Rig*>(ctx)->callback(Port::Send);
        return true;
    }
    static void start(void* ctx, unsigned, std::uint32_t ms) {
        auto& r = *static_cast<Rig*>(ctx);
        r.running = true;
        r.delay = ms;
        r.callback(Port::Start);
    }
    static void stop(void* ctx, unsigned) {
        auto& r = *static_cast<Rig*>(ctx);
        r.running = false;
        r.callback(Port::Stop);
    }
    static void gptp(void* ctx, unsigned, std::uint64_t* gm, std::uint8_t* domain) {
        static_cast<Rig*>(ctx)->callback(Port::Gptp);
        *gm = 1;
        *domain = 0;
    }
    static bool link(void* ctx, unsigned) {
        static_cast<Rig*>(ctx)->callback(Port::Link);
        return true;
    }
    static std::uint32_t seed(void* ctx) {
        auto& r = *static_cast<Rig*>(ctx);
        r.callback(Port::Seed);
        // Force the next xorshift state to 1: its upper sixteen bits are 4,
        // which draws exactly zero milliseconds for the startup timer.
        return r.a.rng ^ 1u;
    }
    void expire() {
        running = false;
        adp_timer_expired(&a);
    }
    void trigger() {
        switch (selected) {
        case Port::Send: expire(); break;
        case Port::Start: adp_gm_change(&a); break;
        case Port::Stop: adp_set_enable(&a, false); break;
        case Port::Gptp: {
            std::array<std::uint8_t, ADP_FRAME_BYTES> frame{};
            adp_build(&a, ADP_MSG_ENTITY_AVAILABLE, 0, frame.data());
            break;
        }
        case Port::Link:
        case Port::Seed: adp_set_enable(&a, true); break;
        }
    }
};

// Both original inline-expiry probes also prove the corresponding valid,
// deferred expiry still advances the machine after the violating call.
TEST(AdpReentry, AdvertiseInlineExpiry) {
    Rig r;
    adp_set_enable(&r.a, true);
    ASSERT_EQ(r.delay, 0u);
    ASSERT_TRUE(r.running);
    r.inject = true;
#ifdef ADP_TEST_RELEASE
    const auto before = adp_reentry_count();
    r.expire();
    EXPECT_EQ(adp_reentry_count(), before + 1u) << "inline ADVERTISE expiry is counted";
#else
    EXPECT_EXIT({ std::signal(SIGABRT, assertion_exit); r.expire(); },
                ::testing::ExitedWithCode(86), "!port_active") << "inline ADVERTISE expiry asserts";
    r.inject = false;
    r.expire();
#endif
    EXPECT_EQ(r.a.state, ADP_STATE_WAITING);
    EXPECT_EQ(r.a.timer, ADP_TIMER_ADVERTISE);
    EXPECT_TRUE(r.running) << "ADVERTISE remains running";
    EXPECT_EQ(r.delay, ADP_ADVERTISE_MS);
    EXPECT_EQ(r.a.stray_expiries, 0u);
    r.expire();
    EXPECT_EQ(r.a.state, ADP_STATE_DELAY);
    EXPECT_EQ(r.a.timer, ADP_TIMER_DELAY);
    EXPECT_TRUE(r.running);
}

TEST(AdpReentry, DelayInlineExpiryOnGmChange) {
    Rig r;
    adp_set_enable(&r.a, true);
    r.expire();
    r.inject = true;
#ifdef ADP_TEST_RELEASE
    const auto before = adp_reentry_count();
    adp_gm_change(&r.a);
    EXPECT_EQ(adp_reentry_count(), before + 1u) << "inline DELAY expiry is counted";
#else
    EXPECT_EXIT({ std::signal(SIGABRT, assertion_exit); adp_gm_change(&r.a); },
                ::testing::ExitedWithCode(86), "!port_active") << "inline DELAY expiry asserts";
    r.inject = false;
    adp_gm_change(&r.a);
#endif
    EXPECT_EQ(r.a.state, ADP_STATE_DELAY);
    EXPECT_EQ(r.a.timer, ADP_TIMER_DELAY);
    EXPECT_TRUE(r.running) << "DELAY remains running";
    EXPECT_EQ(r.a.stray_expiries, 0u);
    r.expire();
    EXPECT_EQ(r.a.state, ADP_STATE_WAITING);
    EXPECT_EQ(r.a.timer, ADP_TIMER_ADVERTISE);
    EXPECT_TRUE(r.running);
}

class AdpPortEntry : public ::testing::TestWithParam<std::tuple<Port, Entry, bool>> {};

TEST_P(AdpPortEntry, RefusesBeforeTouchingState) {
    Rig r;
    std::tie(r.selected, r.entry, r.cross_instance) = GetParam();
    if (r.selected != Port::Link && r.selected != Port::Seed) {
        adp_set_enable(&r.a, true);
        if (r.selected == Port::Start) {
            r.expire();
        }
    }
    r.inject = true;
#ifdef ADP_TEST_RELEASE
    const auto before = adp_reentry_count();
    r.trigger();
    EXPECT_EQ(r.callbacks, 1u);
    EXPECT_EQ(adp_reentry_count(), before + 1u) << "each port callback is counted";
#else
    EXPECT_EXIT({ std::signal(SIGABRT, assertion_exit); r.trigger(); },
                ::testing::ExitedWithCode(86), "!port_active") << "each port callback asserts";
#endif
    // All entry points must work again once the outer port returns.
    r.inject = false;
    const auto after = adp_reentry_count();
    adp_init(&r.a, &r.entity, &r.ports, 0, 0);
    adp_set_current_configuration(&r.a, 2);
    adp_set_enable(&r.a, true);
    EXPECT_EQ(r.a.current_configuration_index, 2u);
    EXPECT_EQ(r.a.timer, ADP_TIMER_DELAY);
    EXPECT_TRUE(r.running);
    EXPECT_EQ(adp_reentry_count(), after);
}

INSTANTIATE_TEST_SUITE_P(AllPorts, AdpPortEntry,
    ::testing::Combine(::testing::Values(Port::Send, Port::Start, Port::Stop, Port::Gptp, Port::Link, Port::Seed),
                       ::testing::Values(Entry::Init, Entry::Enable, Entry::Configuration, Entry::Rx,
                                         Entry::Timer, Entry::Link, Entry::Gm, Entry::Poll, Entry::Build, Entry::Count),
                       ::testing::Bool()));
}  // namespace

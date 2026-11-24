// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
#include <array>
#include <cstdint>
#include <cstdio>

// Each call is measured from its committed entry to the committed return instruction, as hart 0's SPAN.
// Both cores use 32-bit instructions. Recursion/re-entry is reported as unfinished, never silently overwritten.
// Inclusive maxima can overlap; their sum is not elapsed CPU time. An unfinished call contributes no cost.
struct HartsCost {
    struct Item {
        bool active = false;
        std::uint32_t ret = 0;
        std::uint64_t start = 0, count = 0, sum = 0, max = 0, reentered = 0;
    };
    std::array<Item, h1_cost_count> items{};
    void sample(std::uint32_t pc, std::uint32_t previous, std::uint64_t cycle) {
        for (unsigned i = 0; i < h1_cost_count; ++i) {
            auto& s = items[i];
            if (s.active && pc == s.ret) {
                auto cost = cycle - s.start;
                ++s.count; s.sum += cost;
                if (cost > s.max) s.max = cost;
                s.active = false;
            }
            if (pc == h1_cost_pc[i]) {
                if (s.active) ++s.reentered;
                s.active = true; s.ret = previous + 4u; s.start = cycle;
            }
        }
    }
    void report() const {
        for (unsigned i = 0; i < h1_cost_count; ++i) {
            const auto& s = items[i];
            std::printf("H1COST %llu %llu %llu %llu %s\n",
                        static_cast<unsigned long long>(s.count), static_cast<unsigned long long>(s.sum),
                        static_cast<unsigned long long>(s.max),
                        static_cast<unsigned long long>(s.reentered + s.active), h1_cost_name[i]);
        }
    }
};

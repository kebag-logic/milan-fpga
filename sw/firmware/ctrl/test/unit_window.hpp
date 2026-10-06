// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// unit_window.hpp - the contract's identity words and a mailbox window a
// unit test writes word by word, behind MockMbxHal (#665 lane FT).
//
// The window is no model: nothing happens in it but what the test writes
// there and what the firmware writes back, so a test can lay out a record or
// an event no fabric would post (a length past the ring, an interface with
// no instance, a type the contract does not define) and read what the driver
// did with it.

#ifndef UNIT_WINDOW_HPP
#define UNIT_WINDOW_HPP

#include <gmock/gmock.h>

#include <cstdint>
#include <map>
#include <utility>
#include <vector>

#include "mbx_contract.h"
#include "mbx_wire.h"
#include "mock_mbx_hal.hpp"

namespace unit {

constexpr std::uint32_t log2_of(std::uint32_t v) {
    std::uint32_t k = 0;
    while ((1u << k) < v) {
        ++k;
    }
    return k;
}

//! The ID word of the contract this firmware was built against.
inline std::uint32_t contract_id() {
    return mbx_place(MBX_MAGIC, MBX_ID_MAGIC_LSB, MBX_ID_MAGIC_WIDTH) |
           mbx_place(MBX_VERSION_MAJOR, MBX_ID_MAJOR_LSB, MBX_ID_MAJOR_WIDTH);
}

//! The CAPS word of that contract.
inline std::uint32_t contract_caps() {
    return mbx_place(MBX_N_CH, MBX_CAPS_N_CH_LSB, MBX_CAPS_N_CH_WIDTH) |
           mbx_place(MBX_N_IF, MBX_CAPS_N_IF_LSB, MBX_CAPS_N_IF_WIDTH) |
           mbx_place(MBX_N_TIMERS, MBX_CAPS_N_TIMERS_LSB, MBX_CAPS_N_TIMERS_WIDTH) |
           mbx_place(log2_of(MBX_EVT_WORDS), MBX_CAPS_EVT_WORDS_LOG2_LSB, MBX_CAPS_EVT_WORDS_LOG2_WIDTH);
}

inline std::uint32_t ch_reg(unsigned ch, std::uint32_t reg) { return MBX_CH_BASE + MBX_CH_STRIDE * ch + reg; }

//! Every read answers from `words` (0 where nothing was written), every
//! write lands there and is logged in order.
class Window {
 public:
    explicit Window(::testing::NiceMock<MockMbxHal>& hal) {
        ON_CALL(hal, read32(::testing::_)).WillByDefault([this](std::uint32_t off) { return at(off); });
        ON_CALL(hal, write32(::testing::_, ::testing::_)).WillByDefault([this](std::uint32_t off, std::uint32_t v) {
            words[off] = v;
            writes.emplace_back(off, v);
        });
        words[MBX_REG_ID] = contract_id();
        words[MBX_REG_CAPS] = contract_caps();
    }

    std::uint32_t at(std::uint32_t off) const {
        const auto it = words.find(off);
        return it == words.end() ? 0u : it->second;
    }

    //! Word `index` of channel ch's receive ring.
    std::uint32_t& rx(unsigned ch, std::uint32_t index) {
        static const std::uint32_t base[MBX_N_CH] = MBX_CH_RX_BASE_TBL;
        static const std::uint32_t size[MBX_N_CH] = MBX_CH_RX_WORDS_TBL;
        return words[base[ch] + 4u * (index & (size[ch] - 1u))];
    }

    //! Word `index` of the event ring.
    std::uint32_t& evt(std::uint32_t index) { return words[MBX_EVT_BASE + 4u * (index & (MBX_EVT_WORDS - 1u))]; }

    //! The last value written to `off`, or none.
    bool wrote(std::uint32_t off, std::uint32_t* value) const {
        for (auto it = writes.rbegin(); it != writes.rend(); ++it) {
            if (it->first == off) {
                *value = it->second;
                return true;
            }
        }
        return false;
    }

    std::map<std::uint32_t, std::uint32_t> words;
    std::vector<std::pair<std::uint32_t, std::uint32_t>> writes;
};

}  // namespace unit

#endif  // UNIT_WINDOW_HPP

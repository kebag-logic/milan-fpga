// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once

#include <array>
#include <cstdint>
#include <cstdio>
#include <vector>

namespace milan::tb {

//! Independent wire literals: Milan v1.2 4.2.6 selects IEEE 802.1AS-2011
//! with Cor1/Cor2, 11.4.1 through 11.4.2.3 and Table 11-4. These five
//! Ethernet TX words replace the common flag table. Announce is separate.
//! Nothing here constrains RX, which ignores reserved bits and twoStepFlag.
class GptpTxFlags {
 public:
  void observe(const std::vector<uint8_t>& frame) {
    if (frame.size() < 15 || frame[12] != 0x88 || frame[13] != 0xF7) return;
    for (auto& rule : rules_) {
      if ((frame[14] & 0xF) != rule.type) continue;
      ++rule.seen;
      // A truncated flags field cannot look like a conforming zero word.
      const uint32_t got = frame.size() >= 22
          ? (uint32_t(frame[20]) << 8) | frame[21] : 0x10000;
      if (got != rule.flags && rule.wrong++ == 0) rule.first_wrong = got;
    }
  }

  //! One non-vacuity check per required type, then one aggregate check of
  //! EVERY observed word per type. Extra observed types are graded too.
  template <typename Expect>
  void report(Expect expect, uint16_t required_types) const {
    for (const auto& rule : rules_) {
      char label[128];
      if (required_types & (1u << rule.type)) {
        std::snprintf(label, sizeof label, "%s TX flags: frames observed", rule.name);
        expect(label, rule.seen != 0, 1);
      }
      if (!rule.seen) continue;
      std::snprintf(label, sizeof label, "%s TX flags: every wire word (Table 11-4)", rule.name);
      expect(label, rule.wrong ? rule.first_wrong : rule.flags, rule.flags);
      std::printf("TX flags %s: %llu frames, %llu wrong, expected 0x%04x\n",
                  rule.name, static_cast<unsigned long long>(rule.seen),
                  static_cast<unsigned long long>(rule.wrong), rule.flags);
    }
  }

  static constexpr uint16_t all_types = (1u << 0) | (1u << 2) | (1u << 3)
                                      | (1u << 8) | (1u << 10);

 private:
  struct Rule {
    const char* name;
    uint8_t type;
    uint16_t flags;
    uint64_t seen = 0;
    uint64_t wrong = 0;
    uint32_t first_wrong = 0;
  };
  std::array<Rule, 5> rules_{{
      {"Sync", 0x0, 0x0200},
      {"Follow_Up", 0x8, 0x0000},
      {"Pdelay_Req", 0x2, 0x0000},
      {"Pdelay_Resp", 0x3, 0x0200},
      {"Pdelay_Resp_Follow_Up", 0xA, 0x0000},
  }};
};

}  // namespace milan::tb

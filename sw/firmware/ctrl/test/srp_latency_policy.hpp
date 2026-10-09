// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
#include <cstdint>
// FR_NFR 3.4.1: one service budget across the original event and every retry.
inline constexpr uint64_t srp_service_limit_ns=10000000;

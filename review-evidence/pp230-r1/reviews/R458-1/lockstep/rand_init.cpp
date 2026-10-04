// SPDX-License-Identifier: CERN-OHL-W-2.0
// R458-1 probe: randomise every unreset variable (both models differently)
// without touching the bench's argv; LS_SEED selects the seed.
#include <cstdlib>
#include "verilated.h"
namespace {
struct RandInit {
  RandInit() {
    Verilated::randReset(2);
    const char* s = std::getenv("LS_SEED");
    Verilated::randSeed(s ? std::atoi(s) : 1);
  }
} rand_init;
}  // namespace

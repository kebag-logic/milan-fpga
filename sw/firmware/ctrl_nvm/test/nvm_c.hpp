// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// nvm_c.hpp - the saved-state store's C11 headers and its host models,
// included from the C++ tests (#665 lane FT).
//
// The store's headers carry no extern "C" of their own and assert the
// shape's sizes with C11's _Static_assert, which C++ spells static_assert.
// Both are supplied here, for these includes only, so the firmware is
// compiled and read exactly as it ships. The include path is the tree being
// built (nvm_bench.includes), so a planted copy's headers are the ones read.

#ifndef NVM_C_HPP
#define NVM_C_HPP

#define _Static_assert static_assert

extern "C" {
#include <generated/soc.h>

#include "litespi_model.h"
#include "nvm_fmodel.h"
#include "nvm_flash_litespi.h"
#include "nvm_klj2.h"
#include "nvm_smodel.h"
#include "nvm_store.h"
}

#undef _Static_assert

#endif  // NVM_C_HPP

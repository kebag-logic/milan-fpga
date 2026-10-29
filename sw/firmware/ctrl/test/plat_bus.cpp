// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// plat_bus.cpp - ctrl_plat_io.h on the host bus of plat_bus.hpp (#665 S3).

#include "plat_bus.hpp"

namespace plat_bus {

Bus& bus() {
    static Bus instance;
    return instance;
}

}  // namespace plat_bus

extern "C" std::uint32_t ctrl_plat_io_read32(std::uintptr_t address) { return plat_bus::bus().read(address); }

extern "C" void ctrl_plat_io_write32(std::uintptr_t address, std::uint32_t value) {
    plat_bus::bus().write(address, value);
}

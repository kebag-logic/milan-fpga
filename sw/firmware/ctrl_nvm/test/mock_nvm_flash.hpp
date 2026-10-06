// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// mock_nvm_flash.hpp - the store's flash port (nvm_flash.h) as a GoogleMock
// object (#665 lane FT).
//
// struct nvm_flash is the store's whole media port: five calls and a context
// pointer. port() returns one whose calls forward to this mock, so a test
// hands the store a medium that answers each read with bytes the test
// chooses, read by read, which no model of a device produces on demand.

#ifndef MOCK_NVM_FLASH_HPP
#define MOCK_NVM_FLASH_HPP

#include <gmock/gmock.h>

#include <cstdint>

#include "nvm_c.hpp"

class MockNvmFlash {
 public:
    MockNvmFlash() = default;
    MockNvmFlash(const MockNvmFlash&) = delete;
    MockNvmFlash& operator=(const MockNvmFlash&) = delete;

    MOCK_METHOD(int, read, (std::uint32_t addr, std::uint8_t* dst, std::uint32_t len));
    MOCK_METHOD(int, program, (std::uint32_t addr, const std::uint8_t* src, std::uint32_t len));
    MOCK_METHOD(int, erase, (std::uint32_t addr));
    MOCK_METHOD(int, busy, ());
    MOCK_METHOD(std::uint64_t, now_us, ());

    //! The port the store is handed: every call reaches this mock.
    const nvm_flash* port() const { return &port_; }

 private:
    static MockNvmFlash* self(void* ctx) { return static_cast<MockNvmFlash*>(ctx); }
    static int read_(void* ctx, std::uint32_t addr, std::uint8_t* dst, std::uint32_t len) {
        return self(ctx)->read(addr, dst, len);
    }
    static int program_(void* ctx, std::uint32_t addr, const std::uint8_t* src, std::uint32_t len) {
        return self(ctx)->program(addr, src, len);
    }
    static int erase_(void* ctx, std::uint32_t addr) { return self(ctx)->erase(addr); }
    static int busy_(void* ctx) { return self(ctx)->busy(); }
    static std::uint64_t now_us_(void* ctx) { return self(ctx)->now_us(); }

    const nvm_flash port_{read_, program_, erase_, busy_, now_us_, this};
};

#endif  // MOCK_NVM_FLASH_HPP

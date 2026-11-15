// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
//
// test_ctrl_mem.cpp - plat/ctrl_mem.c, the control core's memcpy, memmove,
// memset and memcmp (#665), built on the host under the names ctrl_mem_* so
// the host's own C library is untouched:
//
//   W1  memcpy writes exactly src[0..n) into dst[0..n), for every alignment
//       of each pointer and every length up to several words, and leaves
//       src and every byte outside dst[0..n) unchanged;
//   W2  memmove gives the copy a temporary buffer would, for every
//       overlap: the destination below, equal to and above the source;
//   W3  memset writes the low byte of c into dst[0..n) only;
//   W4  none of them reads or writes across the ends of [dst, dst + n) or
//       [src, src + n): each runs at the very edge of a page whose
//       neighbour is inaccessible, so an access crossing into it faults;
//   W5  each copy and fill returns dst;
//   W6  memcmp returns the difference of the first differing bytes, as
//       unsigned chars, or 0, for every alignment, length and position.

#include <gtest/gtest.h>
#include <sys/mman.h>
#include <unistd.h>

#include <cstddef>
#include <cstdint>
#include <cstring>
#include <vector>

#include "fw_gtest.hpp"

FW_TALLY_LABEL("ctrl memory primitives (host)");

extern "C" {
void *ctrl_mem_memcpy(void *dst, const void *src, std::size_t n);
void *ctrl_mem_memmove(void *dst, const void *src, std::size_t n);
void *ctrl_mem_memset(void *dst, int c, std::size_t n);
int ctrl_mem_memcmp(const void *a, const void *b, std::size_t n);
}

namespace {

constexpr std::size_t kMaxLength = 80;      // twenty words and change: every turn count of every loop
constexpr std::size_t kSlack = 16;          // guard bytes either side of a destination
constexpr unsigned char kGuard = 0xEE;

// A byte pattern no two nearby positions share.
unsigned char pattern(std::size_t i) { return static_cast<unsigned char>(0x11u + 37u * i); }

// A 16-aligned buffer, so every offset below is that misalignment exactly.
struct Aligned {
    alignas(16) unsigned char bytes[kSlack + 8 + kMaxLength + 600 + kSlack];
};

TEST(CtrlMem, W1MemcpyEveryAlignmentAndLength) {
    std::vector<std::size_t> lengths;
    for (std::size_t n = 0; n <= kMaxLength; ++n) lengths.push_back(n);
    lengths.push_back(312);   // READ_DESCRIPTOR's ENTITY body
    lengths.push_back(452);
    for (unsigned d_off = 0; d_off < 8; ++d_off) {
        for (unsigned s_off = 0; s_off < 8; ++s_off) {
            for (std::size_t n : lengths) {
                Aligned src{}, dst{};
                for (std::size_t i = 0; i < sizeof src.bytes; ++i) src.bytes[i] = pattern(i);
                std::memset(dst.bytes, kGuard, sizeof dst.bytes);
                unsigned char *d = dst.bytes + kSlack + d_off;
                const unsigned char *s = src.bytes + kSlack + s_off;
                void *r = ctrl_mem_memcpy(d, s, n);
                EXPECT_EQ(r, d) << "W5 memcpy returns dst";
                for (std::size_t i = 0; i < sizeof dst.bytes; ++i) {
                    const unsigned char *p = dst.bytes + i;
                    const unsigned char want = (p >= d && p < d + n) ? s[p - d] : kGuard;
                    ASSERT_EQ(*p, want) << "W1 memcpy byte " << i << " dst+" << d_off << " src+" << s_off
                                        << " n " << n;
                }
                for (std::size_t i = 0; i < sizeof src.bytes; ++i) {
                    ASSERT_EQ(src.bytes[i], pattern(i)) << "W1 memcpy leaves the source unchanged";
                }
            }
        }
    }
}

TEST(CtrlMem, W2MemmoveEveryOverlap) {
    for (unsigned s_off = 0; s_off < 40; ++s_off) {
        for (unsigned d_off = 0; d_off < 40; ++d_off) {
            for (std::size_t n = 0; n <= 48; ++n) {
                Aligned buf{};
                for (std::size_t i = 0; i < sizeof buf.bytes; ++i) buf.bytes[i] = pattern(i);
                std::vector<unsigned char> want(buf.bytes, buf.bytes + sizeof buf.bytes);
                std::vector<unsigned char> temp(want.begin() + kSlack + s_off, want.begin() + kSlack + s_off + n);
                std::copy(temp.begin(), temp.end(), want.begin() + kSlack + d_off);
                unsigned char *d = buf.bytes + kSlack + d_off;
                void *r = ctrl_mem_memmove(d, buf.bytes + kSlack + s_off, n);
                EXPECT_EQ(r, d) << "W5 memmove returns dst";
                for (std::size_t i = 0; i < sizeof buf.bytes; ++i) {
                    ASSERT_EQ(buf.bytes[i], want[i]) << "W2 memmove byte " << i << " src+" << s_off << " dst+"
                                                     << d_off << " n " << n;
                }
            }
        }
    }
}

TEST(CtrlMem, W3MemsetEveryAlignmentLengthAndValue) {
    for (int c : {0, 0xA5, 0x1FF, -1, 0x80}) {
        for (unsigned d_off = 0; d_off < 8; ++d_off) {
            for (std::size_t n = 0; n <= kMaxLength + 600; n += (n < kMaxLength ? 1 : 151)) {
                Aligned dst{};
                std::memset(dst.bytes, kGuard, sizeof dst.bytes);
                unsigned char *d = dst.bytes + kSlack + d_off;
                void *r = ctrl_mem_memset(d, c, n);
                EXPECT_EQ(r, d) << "W5 memset returns dst";
                for (std::size_t i = 0; i < sizeof dst.bytes; ++i) {
                    const unsigned char *p = dst.bytes + i;
                    const unsigned char want = (p >= d && p < d + n) ? static_cast<unsigned char>(c) : kGuard;
                    ASSERT_EQ(*p, want) << "W3 memset byte " << i << " dst+" << d_off << " n " << n << " c " << c;
                }
            }
        }
    }
}

// The first differing bytes' difference, or 0: the runtime's byte loop.
int reference_cmp(const unsigned char *a, const unsigned char *b, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) {
        if (a[i] != b[i]) return a[i] - b[i];
    }
    return 0;
}

TEST(CtrlMem, W6MemcmpEveryAlignmentLengthAndPosition) {
    for (unsigned a_off = 0; a_off < 8; ++a_off) {
        for (unsigned b_off = 0; b_off < 8; ++b_off) {
            for (std::size_t n = 0; n <= 40; ++n) {
                // equal, then one byte above and one below at every position
                for (std::size_t at = 0; at <= n; ++at) {
                    for (int delta : {0, 1, -1, 0x80}) {
                        if (at == n && delta != 0) continue;
                        Aligned x{}, y{};
                        for (std::size_t i = 0; i < sizeof x.bytes; ++i) x.bytes[i] = y.bytes[i] = pattern(i / 3);
                        unsigned char *p = x.bytes + kSlack + a_off;
                        unsigned char *q = y.bytes + kSlack + b_off;
                        std::memcpy(q, p, n);
                        if (delta != 0) q[at] = static_cast<unsigned char>(q[at] + delta);
                        ASSERT_EQ(ctrl_mem_memcmp(p, q, n), reference_cmp(p, q, n))
                            << "W6 memcmp a+" << a_off << " b+" << b_off << " n " << n << " at " << at << " delta " << delta;
                    }
                }
            }
        }
    }
}

// Two adjacent pages, one of them inaccessible: [first, first + page) is
// usable when the guard follows, [second, second + page) when it precedes.
struct Fence {
    std::size_t page = static_cast<std::size_t>(sysconf(_SC_PAGESIZE));
    unsigned char *base = nullptr;
    explicit Fence(bool guard_after) {
        void *m = mmap(nullptr, 2 * page, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
        if (m == MAP_FAILED) return;
        base = static_cast<unsigned char *>(m);
        if (mprotect(guard_after ? base + page : base, page, PROT_NONE) != 0) {
            munmap(base, 2 * page);
            base = nullptr;
        }
    }
    ~Fence() {
        if (base != nullptr) munmap(base, 2 * page);
    }
    Fence(const Fence &) = delete;
    Fence &operator=(const Fence &) = delete;
    // The last n bytes before the guard, or the first n after it.
    unsigned char *end(std::size_t n) const { return base + page - n; }
    unsigned char *start() const { return base + page; }
};

TEST(CtrlMem, W4NoAccessOutsideEitherRange) {
    Fence src_hi(true), dst_hi(true), src_lo(false), dst_lo(false);
    ASSERT_NE(src_hi.base, nullptr);
    ASSERT_NE(dst_hi.base, nullptr);
    ASSERT_NE(src_lo.base, nullptr);
    ASSERT_NE(dst_lo.base, nullptr);
    for (std::size_t n = 0; n <= 40; ++n) {
        for (unsigned shift = 0; shift < 4; ++shift) {
            // The source ends at the guard; the destination is misaligned against it.
            unsigned char *s = src_hi.end(n);
            for (std::size_t i = 0; i < n; ++i) s[i] = pattern(i);
            unsigned char *d = dst_hi.end(n + shift);
            ctrl_mem_memcpy(d, s, n);
            ASSERT_EQ(std::memcmp(d, s, n), 0) << "W4 memcpy up to a guard, n " << n << " shift " << shift;
            ctrl_mem_memmove(d, s, n);
            ASSERT_EQ(std::memcmp(d, s, n), 0) << "W4 memmove up to a guard, n " << n << " shift " << shift;
            ASSERT_EQ(ctrl_mem_memcmp(d, s, n), 0) << "W4 memcmp up to a guard, n " << n << " shift " << shift;
            ctrl_mem_memset(dst_hi.end(n), 0x5A, n);
            // The source starts at the guard; the destination is misaligned against it.
            unsigned char *s2 = src_lo.start();
            for (std::size_t i = 0; i < n; ++i) s2[i] = pattern(i + 3);
            unsigned char *d2 = dst_lo.start() + shift;
            ctrl_mem_memcpy(d2, s2, n);
            ASSERT_EQ(std::memcmp(d2, s2, n), 0) << "W4 memcpy from a guard, n " << n << " shift " << shift;
            ctrl_mem_memmove(d2, s2, n);
            ASSERT_EQ(std::memcmp(d2, s2, n), 0) << "W4 memmove from a guard, n " << n << " shift " << shift;
            ASSERT_EQ(ctrl_mem_memcmp(d2, s2, n), 0) << "W4 memcmp from a guard, n " << n << " shift " << shift;
            ctrl_mem_memset(dst_lo.start(), 0x5A, n);
            // An overlapping move downwards, ending at the guard.
            unsigned char *o = dst_hi.end(n + shift);
            for (std::size_t i = 0; i < n + shift; ++i) o[i] = pattern(i);
            ctrl_mem_memmove(o + shift, o, n);
            for (std::size_t i = 0; i < n; ++i) {
                ASSERT_EQ(o[shift + i], pattern(i)) << "W4 memmove downwards to a guard, n " << n << " shift " << shift;
            }
            // An overlapping move downwards, starting at the guard: the merge from the top reads down to it.
            unsigned char *u = src_lo.start();
            for (std::size_t i = 0; i < n + shift; ++i) u[i] = pattern(i);
            ctrl_mem_memmove(u + shift, u, n);
            for (std::size_t i = 0; i < n; ++i) {
                ASSERT_EQ(u[shift + i], pattern(i)) << "W4 memmove downwards from a guard, n " << n << " shift " << shift;
            }
        }
    }
}

}  // namespace

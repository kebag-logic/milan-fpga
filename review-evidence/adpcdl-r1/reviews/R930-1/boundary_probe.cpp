// SPDX-License-Identifier: MIT
#include "test_adp.cpp"
#include <sys/mman.h>
#include <unistd.h>

TEST(IndependentBoundary, PhysicalEndOfBuffer) {
    const size_t page = static_cast<size_t>(sysconf(_SC_PAGESIZE));
    void* pages = mmap(nullptr, 2 * page, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    ASSERT_NE(pages, MAP_FAILED);
    auto* base = static_cast<uint8_t*>(pages);
    ASSERT_EQ(mprotect(base + page, page, PROT_NONE), 0);
    auto* frame = base + page - 82;
    unsigned checked = 0;
    for (unsigned state = 0; state < 5; ++state) {
        for (uint64_t target : {UINT64_C(0), entity.entity_id, entity.entity_id ^ UINT64_C(1)}) {
            for (unsigned valid_time : {0u, 31u}) {
                for (unsigned length = 0; length < 2048; ++length) {
                    discover(frame, 2u, target);
                    wire_put_be(frame + 16, (valid_time << 11) | length, 2);
                    if (length < 56 || target == (entity.entity_id ^ UINT64_C(1))) {
                        adp a;
                        discovery_state(&a, state);
                        refused_discovery(&a, frame, 82);
                    } else {
                        accepted_discovery(state, frame, 82);
                    }
                    if (HasFailure()) return;
                    ++checked;
                }
            }
        }
    }
    EXPECT_EQ(checked, 61440u);
    EXPECT_EQ(munmap(pages, 2 * page), 0);
}

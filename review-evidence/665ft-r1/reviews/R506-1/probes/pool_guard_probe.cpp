// Probe (R506-1): is ctrl_pool_alloc's `bin->free_head != NULL` arc reachable?
// A client that writes into a block after freeing it (a use-after-free, the
// corruption ctrl_pool.c line 114 says the guard exists for) leaves a class
// whose free_count is non-zero and whose free list is empty.
#include <gtest/gtest.h>
#include <cstring>
extern "C" {
#include "ctrl_pool.h"
}
TEST(PoolProbe, FreeListDisagreeingWithItsCountIsExhausted) {
    static const struct ctrl_pool_class classes[] = {{32u, 2u}};
    alignas(16) static unsigned char arena[512];
    struct ctrl_pool pool;
    ASSERT_TRUE(ctrl_pool_init(&pool, arena, sizeof arena, classes, 1));
    void* a = ctrl_pool_alloc(&pool, 24u);
    void* b = ctrl_pool_alloc(&pool, 24u);
    ASSERT_NE(a, nullptr);
    ASSERT_NE(b, nullptr);
    ctrl_pool_free(&pool, a);
    ctrl_pool_free(&pool, b);           // list: b -> a, count 2
    std::memset(b, 0, sizeof(void*));   // the client writes into b after freeing it
    void* c = ctrl_pool_alloc(&pool, 24u);
    EXPECT_EQ(c, b);                    // b handed out, head now NULL, count 1
    EXPECT_EQ(pool.bins[0].free_count, 1u);
    EXPECT_EQ(pool.bins[0].free_head, nullptr);
    unsigned long refused = pool.refused;
    EXPECT_EQ(ctrl_pool_alloc(&pool, 24u), nullptr) << "the guarded arc: count 1, empty list, refused";
    EXPECT_EQ(pool.refused, refused + 1u);
}

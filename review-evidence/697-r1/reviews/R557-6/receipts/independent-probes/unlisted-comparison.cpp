// SPDX-License-Identifier: MIT
#include <gtest/gtest.h>
// REQ: PORT-01
TEST(Review, Control) { GTEST_ASSERT_LT(2, 1) << "review diagnostic"; }

#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <cstdlib>
struct Mock { MOCK_METHOD(void, call, ()); };
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_EQ) { SCOPED_TRACE("template trace"); int left = 1, right = 2; ASSERT_EQ(left, right)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_FALSE) { SCOPED_TRACE("template trace"); ASSERT_FALSE(true)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_GE) { SCOPED_TRACE("template trace"); ASSERT_GE(1, 2)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_LE) { SCOPED_TRACE("template trace"); ASSERT_LE(2, 1)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_NE) { SCOPED_TRACE("template trace"); ASSERT_NE(1, 1)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, ASSERT_TRUE) { SCOPED_TRACE("template trace"); ASSERT_TRUE(false)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_CALL) { SCOPED_TRACE("template trace"); Mock mock; EXPECT_CALL(mock, call()).Times(1); }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_EQ) { SCOPED_TRACE("template trace"); int left = 1, right = 2; EXPECT_EQ(left, right)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_EXIT) { SCOPED_TRACE("template trace"); EXPECT_EXIT(std::_Exit(1), ::testing::ExitedWithCode(0), "")  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_FALSE) { SCOPED_TRACE("template trace"); EXPECT_FALSE(true)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_GE) { SCOPED_TRACE("template trace"); EXPECT_GE(1, 2)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_LE) { SCOPED_TRACE("template trace"); EXPECT_LE(2, 1)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_NE) { SCOPED_TRACE("template trace"); EXPECT_NE(1, 1)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }
#line 1 "assertion-forms.cpp"
TEST(Forms, EXPECT_TRUE) { SCOPED_TRACE("template trace"); EXPECT_TRUE(false)  << "\nTSN_TEMPLATE_BEGIN\n" << "discarded stream" << "\nTSN_TEMPLATE_END\n" ; }


namespace {
TEST_F(AcmpCore, IndependentTalkerTopOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA ^ 0x0200000000000000ull);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "talker-only top octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[4], 2u) << "saved talker top octet must follow the new binding";
}
TEST_F(AcmpCore, IndependentControllerTopOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA, 1u, kCtl1 ^ 0x0200000000000000ull);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "controller-only top octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[12], 2u) << "saved controller top octet must follow the new binding";
}
TEST_F(AcmpCore, IndependentUniqueHighOctetPersistence) {
    bind(0); fk.clear();
    bind(0, kTkA, 0x0101u);
    EXPECT_EQ(fk.count(Call::PERSIST), 1u) << "unique-id-only high octet change requires persistence";
    EXPECT_EQ(a.sinks[0].saved[2], 1u) << "saved unique-id high octet must follow the new binding";
}
}

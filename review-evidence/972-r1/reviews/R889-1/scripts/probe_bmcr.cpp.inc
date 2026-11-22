
// Reviewer probe (not part of the tree): registers 4 and 9 hold the advertisement at boot, but register 0 does not
// hold autonegotiation as THE ADVERTISEMENT's write sets it (enable set, isolate clear).
TEST_F(PlatPhy, X1ForcedModeWithTheAdvertisementHeld) {
    peer.gigabit(7u);
    peer.regs[4] = 0x0001u;
    peer.regs[9] = 0x0200u;
    peer.regs[0] = 0x2100u;   // autonegotiation off, forced 100 Mb/s full duplex (22.2.4.1)
    arm_again();
    (void)poll(now);
    next();
    next();
    std::printf("X1 word=%u restarts=%u bmcr=0x%04x\n", peer.word, peer.restarts, peer.regs[0]);
    EXPECT_NE(peer.word, kFull100) << "X1 a 100 Mb/s forced link is published up after the boot";
    EXPECT_NE(peer.regs[0] & 0x1000u, 0u) << "X1 autonegotiation is left disabled after the boot";
}

TEST_F(PlatPhy, X2IsolatedWithTheAdvertisementHeld) {
    peer.gigabit(7u);
    peer.regs[4] = 0x0001u;
    peer.regs[9] = 0x0200u;
    peer.regs[0] = 0x1400u;   // autonegotiation on, isolate set (22.2.4.1.6)
    arm_again();
    (void)poll(now);
    next();
    next();
    std::printf("X2 word=%u restarts=%u bmcr=0x%04x\n", peer.word, peer.restarts, peer.regs[0]);
    EXPECT_EQ(peer.regs[0] & 0x0400u, 0u) << "X2 isolate is left set after the boot";
}

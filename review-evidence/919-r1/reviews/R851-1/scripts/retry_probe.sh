#!/usr/bin/env bash
# retry_probe.sh: the head's ctrl_plat_phy.c on a copy of phy_peer.hpp that records register 4 at each restart,
# with test_plat_phy.cpp's 16 tests and one added test: the boot's register-4 write dropped once (a transient
# management fault), every later access answered. Exit 1 with the added test failing reproduces the recovery
# defect (the only restart ran on 100BASE-TX advertised, and the repaired register 4 then counts as verified).
# Copies only, under the packet's scratch; needs the unit gate's generated headers (scratch/fw-unit).
set -u
P=${PACKET:?export PACKET, this packet directory}
R=${CLONE:?export CLONE, the review clone at the exact head}
T=$R/sw/firmware/ctrl/test
G=$P/scratch/fw-unit/checkout/acmpnvm/gen
O=$P/scratch/probe/retry
rm -rf "$O"; mkdir -p "$O/inc"
cp "$T/phy_peer.hpp" "$T/plat_bus.hpp" "$T/plat_bus.cpp" "$O/inc/"
cp "$T/test_plat_phy.cpp" "$O/inc/t.cpp"
mk() { python3 -I "$P/scripts/mkmut.py" "$1" "$1.new" "$2" "$3" && mv "$1.new" "$1"; }
mk "$O/inc/phy_peer.hpp" '            ++restarts;\n' '            ++restarts;\n            adv_at_restart = regs[4];\n'
mk "$O/inc/phy_peer.hpp" '    unsigned restarts = 0;\n' '    unsigned restarts = 0;\n    std::uint16_t adv_at_restart = 0;\n'
mk "$O/inc/t.cpp" '}  // namespace\n' 'TEST_F(PlatPhy, R851DroppedBootWriteThenRepaired) {
    peer.ignored = 4u;
    arm_again();
    (void)poll(now);
    ASSERT_EQ(peer.restarts, 1u);
    EXPECT_EQ(peer.adv_at_restart, 0x01e1u) << "R851 the only restart so far ran on the PHY defaults (100BASE-TX)";
    peer.ignored = 32u;
    for (int k = 0; k < 10; ++k) next();
    std::printf("R851-PROBE register4=%04x advertised-at-last-restart=%04x restarts=%u adv-owed=%u published=%u\\n",
                peer.regs[4], peer.adv_at_restart, peer.restarts, phy.adv, peer.word);
    EXPECT_EQ(peer.regs[4], 0x0001u) << "R851 register 4 repaired and read back";
    EXPECT_EQ(phy.adv, 0u) << "R851 the advertisement counts as verified";
    EXPECT_EQ(peer.adv_at_restart & 0x0180u, 0u) << "R851 the last negotiation ran without 100BASE-TX advertised";
}

}  // namespace\n'
printf '#include "nvm_store.h"\nstatic struct nvm_status st;\nconst struct nvm_status *nvm_store_status(void) { return &st; }\nbool nvm_store_step(void *c, uint32_t d) { (void)c; (void)d; return false; }\nuint32_t nvm_store_clock(void *c) { (void)c; return 0u; }\n' > "$O/stubs.c"
printf '#include "fw_gtest.hpp"\nFW_TALLY_LABEL("probe")\n' > "$O/label.cpp"
INC="-I$O/inc -I$R/sw/firmware/ctrl/plat -I$T -I$R/sw/firmware/gtest -I$R/sw/firmware/ctrl_nvm -I$G"
cd "$O" || exit 3
gcc -std=c11 -O1 $INC -c "$R/sw/firmware/ctrl/plat/ctrl_plat_phy.c" -o phy.o && gcc -std=c11 -O1 $INC -c stubs.c -o stubs.o &&
g++ -std=c++20 -O1 $INC -include cstdio -c inc/t.cpp -o t.o && g++ -std=c++20 -O1 $INC -c inc/plat_bus.cpp -o bus.o &&
g++ -std=c++20 $INC -c label.cpp -o label.o && g++ ./*.o -lgtest_main -lgtest -pthread -o t || exit 3
diff -u "$T/phy_peer.hpp" inc/phy_peer.hpp
diff -u "$T/test_plat_phy.cpp" inc/t.cpp
./t --gtest_brief=1

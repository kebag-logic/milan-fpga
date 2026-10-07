// SPDX-License-Identifier: CERN-OHL-W-2.0
// Reviewer probe (R532-6): Round 5 control: one valid MSRP PDU whose Class A Domain values need
// more attribute storage than the static pool can ever provide. Does the
// retained record block later SRP reception indefinitely?
#include "srp_fixture.hpp"
namespace fw_test { const char *tally_label() { return "R532-6 head-of-line probe"; } }
namespace {
class R532Hol : public Srp {
protected:
    // N Domain vectors (class 6, priority 3, VID first..first+N-1), one JoinIn each.
    std::vector<uint8_t> domains(unsigned n, unsigned first) {
        std::vector<uint8_t> f(14);
        wire_put_be(f.data(),0x0180c200000eull,6);
        wire_put_be(f.data()+6,0x020304010203ull,6);
        wire_put_be(f.data()+12,0x22ea,2);
        f.push_back(0); f.push_back(4); f.push_back(4);
        const unsigned list=n*7+2;
        f.push_back(list>>8); f.push_back(list&255);
        for(unsigned k=0;k<n;++k) {
            const unsigned vid=first+k;
            f.insert(f.end(),{0,1,6,3,uint8_t(vid>>8),uint8_t(vid&255),36});
        }
        f.insert(f.end(),{0,0,0,0});
        return f;
    }
    void serve_ms(unsigned ms) {
        for(unsigned k=0;k<ms;++k) {
            mbx_model_advance_ms(&model,1);
            for(unsigned n=0;n<50;++n) if(ctrl_loop_service(&loop)==0 && !mbx_model_irq(&model)) break;
        }
    }
    void run(unsigned n) {
        settle(); serve_ms(400);
        const unsigned i=MBX_N_IF-1;
        EXPECT_CALL(licence,Change(i,0,true)).Times(::testing::AtMost(1));
        offer(frame(3,identity(i),0,2),i);
        auto big=domains(n,100);
        ASSERT_LE(big.size(),(size_t)MBX_FRAME_BYTES_MAX);
        ASSERT_TRUE(mbx_model_rx(&model,big.data(),big.size(),0));
        serve_ms(5);
        std::cout << "N=" << n << " bytes=" << big.size()
                  << " refused=" << adapter.refused << " received=" << adapter.received
                  << " malformed=" << adapter.malformed << " pool_in_use=" << ctrl_pool_in_use(&pool) << std::endl;
        // A later, ordinary Listener withdrawal on the last interface.
        auto leave=frame(3,identity(i),5,2);
        ASSERT_TRUE(mbx_model_rx(&model,leave.data(),leave.size(),i));
        const unsigned before=adapter.received;
        EXPECT_CALL(licence,Change(i,0,false)).Times(::testing::AtMost(1));
        for(unsigned s=0;s<6;++s) {
            serve_ms(5000);
            std::cout << "  t+" << (s+1)*5 << "s refused=" << adapter.refused
                      << " received=" << adapter.received << " active=" << adapter.ifs[i].active[0]
                      << " pool_in_use=" << ctrl_pool_in_use(&pool) << std::endl;
        }
        EXPECT_GT(adapter.received,before) << "later SRP input never received";
    }
};
TEST_F(R532Hol, ControlTwoDomainValues) { run(2); }
TEST_F(R532Hol, ManyDomainValuesInOneValidPdu) { run(150); }
TEST_F(R532Hol, TwelveDomainValues) { run(12); }
TEST_F(R532Hol, TwentyDomainValues) { run(20); }
TEST_F(R532Hol, ThirtyDomainValues) { run(30); }
}

// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "srp_fixture.hpp"
#include <csignal>
FW_TALLY_LABEL("ctrl SRP debug guard");
namespace {
TEST_F(Srp, SynchronousBindingFromOutputAsserts) {
    settle();
    EXPECT_DEATH({
        std::signal(SIGABRT,SIG_DFL);
        EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
            srp_mbx_bind(&adapter,0,0,nullptr,nullptr,0);
        });
        offer(frame(3,identity(),0,2));
    },"!m->busy");
}
TEST_F(Srp, SynchronousReceiveFromOutputAsserts) {
    settle();
    EXPECT_DEATH({
        std::signal(SIGABRT,SIG_DFL);
        EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
            mbx_frame received{}; received.len=17;
            loop.rx[MBX_CH_SRP].fn(&adapter,&received);
        });
        offer(frame(3,identity(),0,2));
    },"!m->busy");
}
TEST_F(Srp, SynchronousTickFromOutputAsserts) {
    settle();
    EXPECT_DEATH({
        std::signal(SIGABRT,SIG_DFL);
        EXPECT_CALL(licence,Change(0,0,true)).WillOnce([&](unsigned,unsigned,bool) {
            loop.ticks[loop.n_ticks-1]();
        });
        offer(frame(3,identity(),0,2));
    },"!m->busy");
}

}

// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "fw_gtest.hpp"
#include "aecp.h"
#include "aecp_callback_inputs.hpp"
#include <gtest/gtest.h>
#include <cstdio>
#include <cstdlib>

FW_TALLY_LABEL("AECP debug callback contract");

extern "C" void ctrl_reentry_assert(const char *)
{
    std::fputs("protocol callback reentry\n",stderr);
    std::_Exit(86);
}

TEST(AecpDebug, EveryInputRejectsSynchronousPortDelivery)
{
    for(unsigned entry=0;entry<15;++entry){
        EXPECT_EXIT(([&]{
            uint8_t bytes[312]={};
            aecp_descriptor d{0,0,0,312,bytes,bytes};
            aecp_model model{&d,1,1};aecp_event events[1]{};
            aecp_config cfg{1,{1,2},1,&model,nullptr,0,events,nullptr};
            aecp a{},other{};
            aecp_ports quiet{};quiet.now_ms=[](void*){return 0u;};
            quiet.timer=[](void*,bool,uint32_t){};
            (void)aecp_init(&other,&cfg,&quiet);
            struct Context {unsigned entry;aecp *other;aecp_config *cfg;aecp_ports *ports;};
            Context ctx{entry,&other,&cfg,&quiet};auto ports=quiet;ports.ctx=&ctx;
            ports.now_ms=[](void*p){auto &c=*static_cast<Context*>(p);
                callback_input(c.entry,*c.other,*c.cfg,*c.ports);return 0u;};
            (void)aecp_init(&a,&cfg,&ports);aecp_open(&a);
            std::_Exit(0);
        }()),testing::ExitedWithCode(86),"protocol callback reentry")<<"input "<<entry;
    }
}

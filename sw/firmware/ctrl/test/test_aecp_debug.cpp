// SPDX-License-Identifier: CERN-OHL-W-2.0
#include "fw_gtest.hpp"
#include "aecp.h"
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
    for(unsigned entry=0;entry<6;++entry){
        EXPECT_EXIT({
            aecp a{};a.in_port=true;
            switch(entry){
            case 0:aecp_open(&a);break;
            case 1:aecp_rx(&a,0,nullptr,0);break;
            case 2:(void)aecp_poll(&a);break;
            case 3:aecp_start_done(&a,true,true);break;
            case 4:aecp_changed(&a,5,0,8);break;
            case 5:aecp_tx_complete(&a,0,0);break;
            }
            std::_Exit(0);
        },testing::ExitedWithCode(86),"protocol callback reentry")<<"input "<<entry;
    }
}

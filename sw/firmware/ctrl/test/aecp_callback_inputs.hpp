// SPDX-License-Identifier: CERN-OHL-W-2.0
#pragma once
extern "C" {
#include "aecp.h"
#include "aecp_state.h"
}

// #678: enumerate the public protocol and boot inputs from a real port call.
static void callback_input(unsigned entry, aecp &a, const aecp_config &cfg,
                           const aecp_ports &ports)
{
    uint64_t owner=0;
    uint8_t value[8]={};
    aecp_value field{AECP_CHANGE_FORMAT,5,0,0};
    aecp_map map{};
    switch(entry){
    case 0:(void)aecp_init(&a,&cfg,&ports);break;
    case 1:aecp_open(&a);break;
    case 2:(void)aecp_ready(&a);break;
    case 3:(void)aecp_locked(&a,&owner);break;
    case 4:aecp_rx(&a,0,nullptr,0);break;
    case 5:(void)aecp_poll(&a);break;
    case 6:aecp_start_done(&a,true,true);break;
    case 7:aecp_changed(&a,5,0,8);break;
    case 8:aecp_tx_complete(&a,0,0);break;
    case 9:(void)aecp_value_restore(&a,field,value,sizeof value);break;
    case 10:(void)aecp_value_latch(&a,field,value,sizeof value);break;
    case 11:(void)aecp_restore_defaults(&a);break;
    case 12:(void)aecp_map_restore(&a,&map,nullptr,0);break;
    case 13:aecp_map_refused(&a,&map);break;
    case 14:(void)aecp_restore_settle(&a);break;
    }
}

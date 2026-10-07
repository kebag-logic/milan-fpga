// SPDX-License-Identifier: CERN-OHL-W-2.0
// Add SRP to the opt-in ADP/ACMP/MAAP composition before entering the loop.
#include "ctrl_app.h"
#include "srp_mbx.h"
#include "mbx_wire.h"

bool ctrl_app_attach_srp(struct ctrl_app *app, struct srp_mbx *srp)
{
    if (!app->loop.rx[MBX_CH_ADP].fn || !app->loop.rx[MBX_CH_MAAP].fn ||
        !srp_mbx_attach(srp,&app->loop)) {
        return false;
    }
    uint32_t channels = (1u << MBX_CH_ADP) | (1u << MBX_CH_MAAP) | (1u << MBX_CH_SRP);
    if (app->loop.rx[MBX_CH_ACMP].fn) {
        channels |= 1u << MBX_CH_ACMP;
    }
    mbx_irq_enable(mbx_place(channels,MBX_IRQ_ENABLE_RX_LSB,MBX_IRQ_ENABLE_RX_WIDTH) |
                   mbx_place(1u,MBX_IRQ_ENABLE_EVT_LSB,MBX_IRQ_ENABLE_EVT_WIDTH));
    mbx_tick_enable(true);
    mbx_filter_open(channels);
    return true;
}

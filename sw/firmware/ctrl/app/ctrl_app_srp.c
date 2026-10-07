// SPDX-License-Identifier: CERN-OHL-W-2.0
// Add SRP to the opt-in ADP/ACMP/MAAP composition before entering the loop.
#include "ctrl_app.h"
#include "srp_mbx.h"
#include "mbx_wire.h"
#include "wire.h"
#include <string.h>

// Forward the entity's existing ports with their original context. SRP's
// callback copies intent only; the loop delivers it after SRP's poll returns.
static bool locked(void *ctx, uint64_t *owner)
{
    struct ctrl_app *app = ctx;
    return app->acmp_owner->locked(app->acmp_owner->ctx,owner);
}

static void source(void *ctx, unsigned n, struct acmp_source_state *value)
{
    struct ctrl_app *app = ctx;
    app->acmp_owner->source(app->acmp_owner->ctx,n,value);
}

static void persist(void *ctx, unsigned n)
{
    struct ctrl_app *app = ctx;
    app->acmp_owner->persist(app->acmp_owner->ctx,n);
}

static void changed(void *ctx, unsigned n)
{
    struct ctrl_app *app = ctx;
    app->acmp_owner->changed(app->acmp_owner->ctx,n);
}

static bool deliver(void *ctx);

static void request(void *ctx, unsigned sink, const struct acmp_stream *stream)
{
    struct ctrl_app *app = ctx;
    struct ctrl_app_srp_request *r = &app->srp_requests[sink];
    r->bound = stream != NULL;
    if (stream) {
        r->stream = *stream;
    }
    r->pending = true;
    app->acmp_owner->srp(app->acmp_owner->ctx,sink,stream);
}

static bool deliver(void *ctx)
{
    struct ctrl_app *app = ctx;
    // Destroy detaches SRP. The caller stops service before releasing storage.
    if (app->srp->loop != &app->loop) {
        return false;
    }
    bool pending = false;
    for (unsigned sink = 0; sink < app->acmp.acmp.cfg.n_sinks; ++sink) {
        struct ctrl_app_srp_request *r = &app->srp_requests[sink];
        if (!r->pending) {
            continue;
        }
        struct msrp_stream_id id;
        uint8_t mac[6];
        wire_put_be(id.bytes,r->stream.stream_id,8);
        wire_put_be(mac,r->stream.dest_mac,6);
        unsigned interface = app->acmp.acmp.cfg.sink_interface[sink];
        if (srp_mbx_bind(app->srp,interface,sink,r->bound ? &id : NULL,mac,r->stream.vlan_id)) {
            r->pending = false;
        }
        pending = r->pending || pending;
    }
    return pending;
}

bool ctrl_app_attach_srp(struct ctrl_app *app, struct srp_mbx *srp)
{
    bool acmp = app->loop.rx[MBX_CH_ACMP].fn != NULL;
    if (acmp && (app->acmp.acmp.env == &app->acmp_delivery ||
                 app->acmp.acmp.cfg.n_sinks > CTRL_SRP_SINKS ||
                 app->loop.n_polls + 2u > CTRL_LOOP_MAX_POLLS)) {
        return false;
    }
    if (!app->loop.rx[MBX_CH_ADP].fn || !app->loop.rx[MBX_CH_MAAP].fn ||
        !srp_mbx_attach(srp,&app->loop)) {
        return false;
    }
    uint32_t channels = (1u << MBX_CH_ADP) | (1u << MBX_CH_MAAP) | (1u << MBX_CH_SRP);
    if (app->loop.rx[MBX_CH_ACMP].fn) {
        channels |= 1u << MBX_CH_ACMP;
        app->srp = srp;
        memset(app->srp_requests,0,sizeof(app->srp_requests));
        app->acmp_owner = app->acmp.acmp.env;
        app->acmp_delivery = (struct acmp_env){app,locked,source,request,persist,changed};
        app->acmp.acmp.env = &app->acmp_delivery;
        (void)ctrl_loop_add_poll(&app->loop,deliver,app);
    }
    mbx_irq_enable(mbx_place(channels,MBX_IRQ_ENABLE_RX_LSB,MBX_IRQ_ENABLE_RX_WIDTH) |
                   mbx_place(1u,MBX_IRQ_ENABLE_EVT_LSB,MBX_IRQ_ENABLE_EVT_WIDTH));
    mbx_tick_enable(true);
    mbx_filter_open(channels);
    return true;
}

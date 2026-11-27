// SPDX-License-Identifier: CERN-OHL-W-2.0
// Add SRP to the opt-in ADP/ACMP/MAAP composition before entering the loop.
#include "ctrl_app.h"
#include "srp_mbx.h"
#include "mbx_wire.h"
#include "wire.h"
#include <string.h>

// Forward the entity's existing ports with their original context. SRP's
// binding callback copies intent only; the loop delivers it after SRP's poll returns.
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
    r->parked = r->bound && (r->stream.vlan_id == 0 || r->stream.vlan_id >= 4095);
    r->pending = true;
    app->acmp_owner->srp(app->acmp_owner->ctx,sink,stream);
}

// A binding SRP's registrations reach ACMP at: delivered and bound. SRP retained the event prefix before returning
// from its poll, and an old binding's registration is never fed to a replacement awaiting delivery.
static bool delivered(const struct ctrl_app_srp_request *r)
{
    return !r->parked && !r->pending && r->bound;
}

// ACMP's completion of SRP's registrations at a binding delivered (srp_requests), the sink on its interface, from the
// kind it holds now: a kind registered the sink awaits or a changed kind, then a loss the binding latched (srp_mbx.c,
// capture), only where `lose` lets it: a loss left latched is owed to a later delivery.
static void complete(struct ctrl_app *app, unsigned sink, unsigned interface, bool lose)
{
    struct srp_sink *s = &app->srp->ifs[interface].sinks[sink];
    uint8_t registered = s->feedback_kind;
    enum acmp_sink_state state = app->acmp.acmp.sinks[sink].state;
    if (registered && state == ACMP_SETTLED_NO_RSV) {
        acmp_tk_registered(&app->acmp.acmp,sink,registered == 1u);
    } else if (registered &&
               app->acmp.acmp.sinks[sink].tk_failed != (registered == 1u)) {
        // Accepted intent is settled; every settled exit requests stop.
        // Thus a registered sink outside NO_RSV is already RSV_OK.
        acmp_tk_kind_changed(&app->acmp.acmp,sink,registered == 1u);
    }
    if (s->withdrawn && lose) {
        // The retained kind has been delivered above, before its loss.
        s->withdrawn = false;
        acmp_tk_unregistered(&app->acmp.acmp,sink);
    }
}

// THE SETTLE's client (ctrl_loop.h): the completion a record's pass owed, as the next ordinary pass starts, at every
// binding delivered and from its latest kind; true when one was owed. Only an ordinary pass's polls owe it, after
// this delivery's bindings, and none runs between them and this call, so it completes what that delivery would have.
static bool settle(void *ctx)
{
    struct ctrl_app *app = ctx;
    if (!app->srp_settle_owed) {
        return false;
    }
    app->srp_settle_owed = false;
    if (app->srp->loop != &app->loop) {
        return true;
    }
    for (unsigned sink = 0; sink < app->acmp.acmp.cfg.n_sinks; ++sink) {
        if (delivered(&app->srp_requests[sink])) {
            complete(app,sink,app->acmp.acmp.cfg.sink_interface[sink],true);
        }
    }
    return true;
}

static bool deliver(void *ctx)
{
    struct ctrl_app *app = ctx;
    for (unsigned source = 0; source < app->acmp.acmp.cfg.n_sources; ++source) {
        unsigned interface = app->acmp.acmp.cfg.source_interface[source];
        bool present = app->srp->loop == &app->loop && source < CTRL_SRP_SOURCES &&
                       app->srp->ifs[interface].listener_present[source];
        // ACMP is told a Listener's presence where its flag differs: the call sets that flag and nothing else, so a
        // pass that changes no source's paid it for every source each pass (#665)
        if (app->acmp.acmp.sources[source].listener_registered != present) {
            (void)acmp_listener_registered(&app->acmp.acmp,interface,source,present);
        }
    }
    // Destroy detaches SRP. The caller stops service before releasing storage.
    if (app->srp->loop != &app->loop) {
        return false;
    }
    // The sources whose Talker declaration SRP changed since this delivery last ran, each its STREAM_OUTPUT's
    // GET_STREAM_INFO notice, which the AECP bridge raises in the next pass: so a pass that takes one owes output and
    // is not the loop's idle pass (#936; ctrl_loop.h, the polls; Milan v1.2 5.4.5.2, Table 5.22)
    bool noticed = false;
    for (unsigned interface = 0; interface < MBX_N_IF; ++interface) {
        noticed = noticed || app->srp->ifs[interface].noticed != 0u;
        app->srp_noticed |= app->srp->ifs[interface].noticed;
        app->srp->ifs[interface].noticed = 0u;
    }
    // A Talker is declared while its destination is valid (#895; Milan v1.2 4.3.3.1, 5.3.7.4): the MAAP adapter's DA
    // gate, refreshed by MAAP's poll before this one, with the range MAAP holds on the interface
    for (unsigned interface = 0; interface < MBX_N_IF; ++interface) {
        (void)srp_mbx_gate(app->srp,interface,app->maap.published_gate[interface],app->maap.ifs[interface].core.base);
    }
    bool pending = noticed;
    // A pass whose drain took a record carries the record alone where CTRL_LOOP_SETTLE_ALONE is set: ACMP's completion
    // is owed to THE SETTLE, the next ordinary pass's first work, and the loop passes on to it (#977, its ruling of
    // 2026-11-23, item 3)
    const bool settles = CTRL_LOOP_SETTLE_ALONE && app->loop.drain_taken != 0u;
    // a delivery that owes no settle completes every binding itself, below, so it leaves none owed
    app->srp_settle_owed = settles;
    pending = pending || settles;
    // One delivery makes at most one binding change and, outside THE SETTLE, at most one loss completion, each the
    // first owed from its turn, the sink after the last it made: so each owed waits at most n_sinks deliveries and the
    // rest stay pending, delivered in turn. THE TRANSMIT waits on none of them, and a withdrawal a later delivery makes
    // rides the next MRPDU (#977, its ruling on round 9's STOP, item 2; IEEE 802.1Q-2018 10.7.4.1)
    const unsigned n = app->acmp.acmp.cfg.n_sinks;
    unsigned bind = n;
    unsigned lose = n;
    for (unsigned step = 0; step < n && bind == n; ++step) {
        const unsigned k = (app->srp_bind_turn + step) % n;
        const struct ctrl_app_srp_request *r = &app->srp_requests[k];
        if (r->parked ? app->srp->ifs[app->acmp.acmp.cfg.sink_interface[k]].sinks[k].bound : r->pending) {
            bind = k;
        }
    }
    for (unsigned step = 0; step < n && lose == n && !settles; ++step) {
        const unsigned k = (app->srp_loss_turn + step) % n;
        if (k != bind && delivered(&app->srp_requests[k]) &&
            app->srp->ifs[app->acmp.acmp.cfg.sink_interface[k]].sinks[k].withdrawn) {
            lose = k;
        }
    }
    for (unsigned sink = 0; sink < n; ++sink) {
        struct ctrl_app_srp_request *r = &app->srp_requests[sink];
        unsigned interface = app->acmp.acmp.cfg.sink_interface[sink];
        struct srp_sink *s = &app->srp->ifs[interface].sinks[sink];
        if (r->parked) {
            // A replacement can overtake the old unbind in the request slot.
            // Retire that accepted binding, then leave the invalid request idle.
            r->pending = s->bound && (sink != bind || !srp_mbx_bind(app->srp,interface,sink,NULL,NULL,0));
            pending = pending || r->pending;
            continue;
        }
        if (r->pending && sink == bind) {
            struct msrp_stream_id id;
            uint8_t mac[6];
            wire_put_be(id.bytes,r->stream.stream_id,8);
            wire_put_be(mac,r->stream.dest_mac,6);
            if (srp_mbx_bind(app->srp,interface,sink,r->bound ? &id : NULL,mac,r->stream.vlan_id)) {
                r->pending = false;
                // A new ACMP epoch supersedes even identical SRP identities.
                s->feedback_kind = s->desired;
                s->withdrawn = false;
            }
        }
        if (delivered(r) && !settles) {
            complete(app,sink,interface,sink == lose);
        }
        pending = r->pending || (delivered(r) && s->withdrawn) || pending;
    }
    if (bind < n) {
        app->srp_bind_turn = (uint8_t)((bind + 1u) % n);
    }
    if (lose < n) {
        app->srp_loss_turn = (uint8_t)((lose + 1u) % n);
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
        // a recomposed application keeps no record of the SRP instance it attached before (#936)
        app->srp_noticed = 0u;
        app->acmp_owner = app->acmp.acmp.env;
        app->acmp_delivery = (struct acmp_env){app,locked,source,request,persist,changed};
        app->acmp.acmp.env = &app->acmp_delivery;
        (void)ctrl_loop_add_poll(&app->loop,deliver,app);
        // bound at every shape; only where CTRL_LOOP_SETTLE_ALONE is set does a delivery owe it work
        app->srp_settle_owed = false;
        app->srp_bind_turn = 0u;
        app->srp_loss_turn = 0u;
        (void)ctrl_loop_set_settle(&app->loop,settle,app);
    }
    mbx_irq_enable(mbx_place(channels,MBX_IRQ_ENABLE_RX_LSB,MBX_IRQ_ENABLE_RX_WIDTH) |
                   mbx_place(1u,MBX_IRQ_ENABLE_EVT_LSB,MBX_IRQ_ENABLE_EVT_WIDTH));
    mbx_tick_enable(true);
    mbx_filter_open(channels);
    return true;
}

// SPDX-License-Identifier: CERN-OHL-W-2.0
// The adapter owns no heap or protocol tables; lwSRP owns its MRP machines.
#include "srp_mbx.h"
#include <string.h>
#include "srp_bounds.h"
#ifndef NDEBUG
#include <assert.h>
#endif
#include "shlan_port.h"
#include "wire.h"
#include "ports/timer.h"
#include "shish_lan/error.h"
#include "shish_lan/mrp_pdu.h"

const struct ctrl_pool_class srp_pool_classes[SRP_POOL_N_CLASSES] = {
    {64u, SRP_POOL_SMALL_BLOCKS}, {256u, SRP_POOL_MEDIUM_BLOCKS}, {512u, SRP_POOL_LARGE_BLOCKS}
};

// Stop retrying allocation refusal after one periodic interval from arrival.
// This recovery limit does not extend the service bound (FR_NFR.md 3.4.1).
#define SRP_RX_RETRY_MS 1000u

// Every source has its bit of the publication block's LICENCE and TALKER_DECL.
_Static_assert(CTRL_SRP_SOURCES <= MBX_N_PUB_SOURCES, "every source needs a LICENCE and a TALKER_DECL bit");

// The JoinTime every participant is configured with, in centiseconds (create_participants).
#define SRP_JOIN_CS 20u
// THE TRANSMIT (ctrl_loop.h, #665): two aged builds stand further apart than the 18 ms of SRP's records (THE
// SHARE, nine passes), so at most one stands among the passes a record waits; and every participant's owed MRPDU,
// one a build, is sent within the JoinTime (IEEE 802.1Q Table 10-7).
_Static_assert(CTRL_LOOP_TX_AGE * MBX_TICK_MS * 1000u >= 9u * CTRL_LOOP_SHARE_US,
               "two aged builds stand further apart than SRP's bound");
_Static_assert(2u * MBX_N_IF * CTRL_LOOP_TX_MS <= SRP_JOIN_CS * MBX_TICK_MS,
               "every participant's owed MRPDU is sent within the JoinTime");

static struct srp_mbx *timer_owner;
static void tick(void);
static bool poll(void *ctx);
static bool transmit(void *ctx);
static bool transmit_aged(void *ctx);
static void receive(void *ctx, const struct mbx_frame *frame);
static void on_event(void *ctx, const struct mbx_event *event);
static void snapshot(struct srp_interface *i);
static void capture(struct srp_sink *s, uint8_t previous);

static bool enter(struct srp_mbx *m)
{
    if (m->busy) {
        ++m->reentries;
#ifndef NDEBUG
        assert(!m->busy);
#endif
        return false;
    }
    m->busy = true;
    return true;
}

static void tick(void)
{
    struct srp_mbx *m = timer_owner;
    if (!enter(m)) {
        return;
    }
    shlan_timer_tick();
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        if (m->ifs[n].msrp) {
            snapshot(&m->ifs[n]);
        }
    }
    // A centisecond's timers can make an MRPDU owed: the build is held for THE TRANSMIT, and its age counts the
    // centiseconds dispatched while it is held (ctrl_loop.h).
    m->tx_age += m->tx_held ? 1u : 0u;
    m->tx_held = true;
    m->busy = false;
}

// The interface's licences as the fabric datapath reads them (the publication
// block's LICENCE, bit s source s), written before any licence change is
// reported, so the stream gate never trails the notification it causes.
static void publish_licence(const struct srp_interface *i)
{
    uint32_t active = 0;
    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
        active |= (i->active[k] ? 1u : 0u) << k;
    }
    (void)mbx_pub_licence(i->index,active);
}

// The interface's Talker declarations as the fabric datapath reads them (the
// publication block's TALKER_DECL, bit s source s): set by declare_sources
// before the declarations it describes are sent, and cleared here before the
// participants holding them are destroyed, so the datapath tags a stream's
// frames only while its Talker attribute is declared (802.1Q 35.1.2: a bridge
// prunes a tagged stream with none). A creation that fails declared nothing
// the block shows: declare_sources publishes only once every source joined.
static void withdraw_declared(unsigned index)
{
    (void)mbx_pub_talker_decl(index,0u);
}

static struct srp_interface *from_ctx(struct msrp_ctx *ctx)
{
    return (struct srp_interface *)((uint8_t *)ctx - offsetof(struct srp_interface, msrp_ctx));
}

static void listener(struct msrp_ctx *ctx, uint8_t port,
                      const struct msrp_stream_id *identity, enum msrp_listener_decl declaration, bool is_new)
{
    (void)port; (void)is_new;
    struct srp_interface *i = from_ctx(ctx);
    i->stale = true; // what an indication writes, snapshot copies (#665)
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        if (memcmp(i->sources[n].value.stream_id.bytes,identity->bytes,8) == 0) {
            i->registered[n] = declaration == MSRP_LISTENER_DECL_READY ||
                               declaration == MSRP_LISTENER_DECL_READY_FAILED;
            if (!i->registered[n] && i->active[n]) {
                i->stop_owed[n] = true;
            }
        }
    }
}

// Indications copy registration changes only. The filter below closes the
// preceding complete wire event, after both halves of an atomic replacement.
static void talker_changed(struct srp_interface *i, const struct msrp_talker_adv *v,
                           uint8_t kind, bool registered)
{
    i->stale = true; // what an indication writes, snapshot copies (#665)
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        struct srp_sink *s = &i->sinks[k];
        if (s->bound && memcmp(s->stream_id.bytes,v->stream_id.bytes,8) == 0) {
            s->registered_kinds &= (uint8_t)~kind;
            if (registered && memcmp(s->dest_mac,v->dest_mac,6) == 0 && s->vid == v->vlan_id) {
                s->registered_kinds |= kind;
            }
        }
    }
}

static void advertised(struct msrp_ctx *ctx, uint8_t port,
                       const struct msrp_talker_adv *value, bool is_new)
{
    (void)port; (void)is_new;
    talker_changed(from_ctx(ctx),value,2u,true);
}

static void failed(struct msrp_ctx *ctx, uint8_t port,
                   const struct msrp_talker_failed *value, bool is_new)
{
    (void)port; (void)is_new;
    talker_changed(from_ctx(ctx),&value->talker,1u,true);
}

static void left(struct msrp_ctx *ctx, uint8_t port, uint8_t type, const void *value)
{
    if (type == MSRP_ATTR_TYPE_LISTENER) {
        listener(ctx,port,value,MSRP_LISTENER_DECL_IGNORE,false);
    } else if (type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) {
        talker_changed(from_ctx(ctx),value,type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u,false);
    }
}

static void domain(struct msrp_ctx *ctx, uint8_t port, const struct msrp_domain *value, bool is_new)
{
    (void)port; (void)is_new;
    struct srp_interface *i = from_ctx(ctx);
    // The receive-interest filter has already checked the class and VID.
    if (memcmp(&i->domain,value,sizeof(*value)) != 0) {
        i->next_domain = *value;
        i->domain_owed = true;
        i->owner->tx_held = true;
    }
}

static bool declare_sources(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    uint64_t used = 0;
    uint32_t declared = 0;
    // A join rewrites the value of the attribute a registration shares (#665).
    i->stale = true;
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        struct msrp_talker_failed value = {.talker=i->sources[n].value};
        value.talker.vlan_id = i->domain.vid;
        value.talker.priority_and_rank = (uint8_t)((value.talker.priority_and_rank & 0x10u) | (i->domain.priority << 5));
        uint64_t size = (uint64_t)value.talker.max_frame_size + 22u;
        if (size < 68u) {
            size = 68u;
        }
        uint64_t slope = (size + 20u) * value.talker.max_interval_frames * 64000u;
        bool admitted = i->sources[n].allocated && value.talker.max_interval_frames > 0 &&
                        used + slope <= (uint64_t)m->config.link_rate_bps * 3u / 4u;
        i->admitted[n] = admitted;
        if (admitted) {
            used += slope;
        } else {
            wire_put_be(value.failure_info + 2,i->mac,6);
            value.failure_info[8] = i->sources[n].allocated ? 1 : 2;
        }
        if (mrp_mad_join(i->msrp,0,admitted ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,
                         &value,true) != 0) {
            return false;
        }
        declared |= 1u << n;
    }
    // The admitted bandwidth (IDLE_SLOPE) and the declared sources
    // (TALKER_DECL), before these declarations are sent. used is at most
    // three quarters of a 32-bit link rate.
    (void)mbx_pub_idle_slope(i->index,(uint32_t)used);
    (void)mbx_pub_talker_decl(i->index,declared);
    return true;
}

static bool interested_msrp(void *ctx, uint8_t port, uint8_t type, const void *value)
{
    (void)port;
    struct srp_interface *i = ctx;
    // lwSRP doc/integrator.md:321-323 and mrp.h:288-290 forbid reentry.
    // Observe the previous complete event from copied indication data only.
    // Atomic replacement stays continuous; Lv then New remains two events.
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        struct srp_sink *s = &i->sinks[k];
        uint8_t previous = s->desired;
        s->desired = (s->registered_kinds & 1u) ? 1u : (s->registered_kinds & 2u);
        capture(s,previous);
    }
    if (type == MSRP_ATTR_TYPE_DOMAIN) {
        const struct msrp_domain *d = value;
        return d->class_id == 6 && d->vid > 0 && d->vid < 4095;
    }
    if (type == MSRP_ATTR_TYPE_LISTENER) {
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
            if (memcmp(i->sources[n].value.stream_id.bytes,value,8) == 0) {
                return true;
            }
        }
    } else {
        for (unsigned n = 0; n < CTRL_SRP_SINKS; ++n) {
            if (i->sinks[n].bound && memcmp(i->sinks[n].stream_id.bytes,value,8) == 0) {
                return true;
            }
        }
    }
    return false;
}

static bool interested_mvrp(void *ctx, uint8_t port, uint8_t type, const void *value)
{
    (void)port; (void)type;
    const struct srp_interface *i = ctx;
    const uint16_t vid = wire_be16(value);
    if (vid == i->domain.vid) {
        return true;
    }
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        if (i->sinks[k].bound && i->sinks[k].vid == vid) {
            return true;
        }
    }
    return false;
}

// lwSRP reports every Applicant or Registrar state change of a participant
// here. A Registrar change is a change of what snapshot copies; any change
// can leave an attribute mrp_reclaim frees (#665).
static void msrp_moved(void *ctx, const struct mrp_transition *t)
{
    struct srp_interface *i = ctx;
    i->reclaim = true;
    if (t->reg_from != t->reg_to) {
        i->stale = true;
    }
}

static void mvrp_moved(void *ctx, const struct mrp_transition *t)
{
    (void)t;
    struct srp_interface *i = ctx;
    i->reclaim = true;
}

static bool create_participants(struct srp_interface *i)
{
    i->msrp_ctx = (struct msrp_ctx){.on_domain=domain,.on_listener=listener,.on_leave=left,
                                    .on_talker_advertise=advertised,.on_talker_failed=failed};
    i->msrp = msrp_app_create(1,&i->msrp_ctx);
    i->mvrp = mvrp_app_create(1,&i->mvrp_ctx);
    if (!i->msrp || !i->mvrp) {
        return false;
    }
    mrp_set_observer(i->msrp,msrp_moved,i);
    mrp_set_observer(i->mvrp,mvrp_moved,i);
    i->stale = true;
    i->reclaim = true;
    // These valid constants are installed before creating any attribute.
    (void)mrp_port_configure(i->msrp,0,SRP_JOIN_CS,500,1000,(uint32_t)i->mac,true);
    (void)mrp_port_configure(i->mvrp,0,SRP_JOIN_CS,500,1000,(uint32_t)i->mac ^ 0x91u,true);
    mrp_set_rx_filter(i->msrp,interested_msrp,i);
    mrp_set_rx_filter(i->mvrp,interested_mvrp,i);
    i->vlan_sent = false;
    i->domain = (struct msrp_domain){6,3,2};
    // The default Domain, not adopted, before it is declared (SR_DOMAIN).
    (void)mbx_pub_domain(i->index,false,i->domain.priority,i->domain.vid);
    if (mrp_mad_join(i->msrp,0,MSRP_ATTR_TYPE_DOMAIN,&i->domain,true) != 0 ||
        mvrp_declare(i->mvrp,0,2) != 0) {
        return false;
    }
    return declare_sources(i);
}

static bool open_interface(struct srp_interface *i)
{
    if (create_participants(i)) {
        // its declarations are owed: THE TRANSMIT builds them
        i->owner->tx_held = true;
        return true;
    }
    msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);
    i->msrp = NULL; i->mvrp = NULL;
    return false;
}

bool srp_mbx_init(struct srp_mbx *m, const struct srp_mbx_config *config)
{
    if (timer_owner == m) {
        if (!enter(m)) {
            return false;
        }
        m->busy = false;
        return false;
    }
    memset(m,0,sizeof(*m));
    m->config = *config;
    if (!config->licence || !shlan_port_pool()) {
        return false;
    }
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        struct srp_interface *i = &m->ifs[n];
        i->owner = m; i->index = n; i->mac = config->mac[n];
        if (!config->sources[n]) {
            srp_mbx_destroy(m);
            return false;
        }
        memcpy(i->sources,config->sources[n],sizeof(i->sources));
        if (!open_interface(i)) {
            ++m->refused;
            srp_mbx_destroy(m);
            return false;
        }
    }
    m->initialized = true;
    return true;
}

void srp_mbx_destroy(struct srp_mbx *m)
{
    if (!enter(m)) {
        return;
    }
    if (m->loop) {
        struct ctrl_loop *l = m->loop;
        l->rx[MBX_CH_SRP] = (struct ctrl_loop_rx){0};
        for (unsigned n = 0; n < l->n_ticks; ++n) {
            if (l->ticks[n] == tick) {
                --l->n_ticks;
                memmove(l->ticks + n,l->ticks + n + 1,(l->n_ticks - n) * sizeof(*l->ticks));
                break;
            }
        }
        for (unsigned n = 0; n < l->n_polls; ++n) {
            if (l->polls[n].ctx == m) {
                --l->n_polls;
                memmove(l->polls + n,l->polls + n + 1,(l->n_polls - n) * sizeof(*l->polls));
                break;
            }
        }
        for (unsigned n = 0; n < l->n_sinks; ++n) {
            if (l->sinks[n].ctx == m) {
                --l->n_sinks;
                memmove(l->sinks + n,l->sinks + n + 1,(l->n_sinks - n) * sizeof(*l->sinks));
                break;
            }
        }
        if (l->transmit_ctx == m) {
            l->transmit = NULL;
            l->transmit_aged = NULL;
            l->transmit_ctx = NULL;
        }
        m->loop = NULL;
    }
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        struct srp_interface *i = &m->ifs[n];
        // Every licence closes on the datapath before any revocation is
        // reported. An init refusal reaches here before i->index is set.
        bool revoked[CTRL_SRP_SOURCES];
        for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
            revoked[k] = i->active[k];
            i->active[k] = false;
            i->listener_present[k] = false;
        }
        (void)mbx_pub_licence(n,0u);
        for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
            if (revoked[k]) {
                m->config.licence(m->config.ctx,n,k,false);
            }
        }
        withdraw_declared(n);
        msrp_app_destroy(i->msrp); i->msrp = NULL;
        mvrp_app_destroy(i->mvrp); i->mvrp = NULL;
    }
    if (timer_owner == m) {
        timer_owner = NULL;
    }
    m->owed_len = 0;
    m->pending_rx.len = 0;
    m->initialized = false;
    m->busy = false;
}

static bool has_sink(const struct srp_interface *i,
                         const struct srp_sink *old, bool same_stream)
{
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        const struct srp_sink *s = &i->sinks[k];
        if (s->bound &&
            (same_stream ? memcmp(s->stream_id.bytes,old->stream_id.bytes,8) == 0 : s->vid == old->vid)) {
            return true;
        }
    }
    return false;
}

bool srp_mbx_bind(struct srp_mbx *m, unsigned interface, unsigned sink,
                  const struct msrp_stream_id *identity, const uint8_t dest_mac[6], uint16_t vid)
{
    if (!enter(m)) {
        return false;
    }
    if (interface >= MBX_N_IF || sink >= CTRL_SRP_SINKS ||
        (identity && (!dest_mac || vid == 0 || vid >= 4095)) || m->owed_len || m->pending_rx.len) {
        m->busy = false;
        return false;
    }
    struct srp_interface *i = &m->ifs[interface];
    struct srp_sink *s = &i->sinks[sink];
    if (!i->msrp) {
        m->busy = false;
        return false;
    }
    if (s->bound && identity && memcmp(&s->stream_id,identity,8) == 0 &&
        memcmp(s->dest_mac,dest_mac,6) == 0 && s->vid == vid) {
        m->busy = false;
        return true;
    }
    struct srp_sink replacement = {0};
    if (identity) {
        replacement.stream_id = *identity;
        memcpy(replacement.dest_mac,dest_mac,6);
        replacement.vid = vid;
        replacement.bound = true;
        // Carry the shared Applicant and committed VID across replacements,
        // including several accepted binds before the next service pass.
        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
            const struct srp_sink *r = &i->sinks[k];
            if (!r->bound) {
                continue;
            }
            if (memcmp(r->stream_id.bytes,identity->bytes,8) == 0) {
                replacement.declared |= r->declared;
            }
            if (r->vid == vid) {
                replacement.vlan_requested |= r->vlan_requested;
                replacement.vlan_sent |= r->vlan_sent;
            }
        }
    }
    const struct srp_sink old = *s;
    *s = replacement;
    i->stale = true; // snapshot matches registrations against the bindings (#665)
    if (old.bound) {
        // Judge the complete new binding set, including the replacement.
        // a declaration withdrawn here is sent by THE TRANSMIT's call
        if (!has_sink(i,&old,true)) {
            (void)msrp_withdraw_listener(i->msrp,0,&old.stream_id);
            m->tx_held = m->tx_held || old.declared != 0u;
        }
        if (old.vid != i->domain.vid && !has_sink(i,&old,false)) {
            (void)mvrp_withdraw(i->mvrp,0,old.vid);
            m->tx_held = m->tx_held || old.vlan_requested;
        }
    }
    m->busy = false;
    return true;
}

static bool rx_order_ready(struct srp_mbx *m)
{
    return m->owed_len == 0 && m->loop->ticks_owed == 0 &&
           !(mbx_irq_status() & (1u << MBX_IRQ_STATUS_EVT_LSB));
}

static bool rx_ready(void *ctx)
{
    struct srp_mbx *m = ctx;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        if (m->ifs[n].reopening) {
            return false;
        }
    }
    return m->pending_rx.len == 0 && rx_order_ready(m);
}

// Return false only for local storage refusal. Earlier events
// may already have applied; lwSRP requires replay of the identical payload.
static bool apply_receive(struct srp_mbx *m, const struct mbx_frame *frame)
{
    struct srp_interface *i = &m->ifs[frame->interface];
    uint16_t type = wire_be16(frame->bytes + 12);
    uint64_t da = ((uint64_t)wire_be32(frame->bytes) << 16) | wire_be16(frame->bytes + 4);
    struct mrp_app *app;
    if (type == MRP_ETHERTYPE_MSRP && da == 0x0180c200000eull) {
        app = i->msrp;
    } else if (type == MRP_ETHERTYPE_MVRP && da == 0x0180c2000021ull) {
        app = i->mvrp;
    } else {
        ++m->malformed;
        return true;
    }
    if (i->msrp) {
        // Seed copied kinds from the registrar before entering any callback.
        snapshot(i);
    }
    int result = app ? mrp_rx(app,0,frame->bytes + 14,frame->len - 14u) : -SHLAN_ERROR_NO_MEMORY;
    // A received attribute can be created with no state change (#665).
    i->reclaim = true;
    if (i->msrp) {
        // Include the last event, also when an earlier event applied before
        // allocation refusal. Identical receive retries remain idempotent.
        snapshot(i);
    }
    if (result == -SHLAN_ERROR_NO_MEMORY) {
        ++m->refused;
        return false;
    }
    if (result != 0) {
        ++m->malformed;
    } else {
        ++m->received;
    }
    return true;
}

static void expire_receive(struct srp_mbx *m)
{
    if (m->pending_rx.len &&
        (uint32_t)(mbx_now_ms() - m->pending_rx.arrival_ms) >= SRP_RX_RETRY_MS) {
        m->pending_rx.len = 0;
        ++m->rx_discarded;
    }
}

static void receive(void *ctx, const struct mbx_frame *frame)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return;
    }
    if (frame->interface >= MBX_N_IF || frame->len < 17u) {
        ++m->malformed;
        m->busy = false;
        return;
    }
    struct srp_interface *i = &m->ifs[frame->interface];
    if (!i->link || (i->discard_prefix && mbx_rx_before(MBX_CH_SRP,i->rx_mark))) {
        m->busy = false;
        return;
    }
    if (!apply_receive(m,frame)) {
        m->pending_rx = *frame;
        expire_receive(m);
    }
    // a received record can make an MRPDU owed: THE TRANSMIT builds it once the pass's input is taken
    m->tx_held = true;
    m->busy = false;
}

struct send_context {
    struct srp_interface *interface;
    struct mrp_app *app;
};

static void vlan_committed(void *ctx, uint8_t type, enum mrp_attr_event event, const void *value)
{
    (void)type;
    struct srp_interface *i = ctx;
    // mvrp_declare requests Join, never New. Mt/Lv carry no membership.
    if (event != MRP_ATTR_EVENT_JOININ && event != MRP_ATTR_EVENT_JOINMT) {
        return;
    }
    if (wire_be16(value) == i->domain.vid) {
        i->vlan_sent = true;
    }
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        struct srp_sink *s = &i->sinks[k];
        if (s->bound && s->vid == wire_be16(value)) {
            s->vlan_sent = true;
        }
    }
}

static int send_pdu(void *ctx, uint8_t port, const uint8_t *pdu, size_t len)
{
    (void)port;
    struct send_context *s = ctx;
    struct srp_mbx *m = s->interface->owner;
    // pdu is owed_frame + 14: lwSRP sends the buffer poll gave it, and while a
    // frame is owed only its participant runs, so nothing rebuilds over it.
    if (!m->owed_len) {
        memcpy(m->owed_frame,s->app->ops->group_addr,6);
        wire_put_be(m->owed_frame + 6,s->interface->mac,6);
        wire_put_be(m->owed_frame + 12,s->app->ops->ethertype,2);
        m->owed_len = (uint16_t)(len + 14u);
        m->owed_if = s->interface->index;
        m->owed_ethertype = s->app->ops->ethertype;
    }
    if (mbx_tx_send(MBX_CH_SRP,m->owed_if,m->owed_frame,m->owed_len) != MBX_STATUS_OK) {
        return -SHLAN_ERROR_NO_BUFFER;
    }
    if (s->app->ops->ethertype == MRP_ETHERTYPE_MVRP) {
        // Only the accepted record licenses this VID (Milan 4.3.2).
        (void)mrpdu_parse(pdu,len,s->app->ops,vlan_committed,NULL,s->interface);
    }
    m->owed_len = 0;
    ++m->transmitted;
    return 0;
}

static void registrations(void *ctx, const struct mrp_attr_status *status)
{
    struct srp_interface *i = ctx;
    if (status->reg == MRP_REG_STATE_MT) {
        return;
    }
    if (status->attr_type == MSRP_ATTR_TYPE_LISTENER) {
        const uint8_t *v = status->attr_val;
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
            if (memcmp(i->sources[n].value.stream_id.bytes,v,8) == 0) {
                // One value per StreamID; Ignore occupies no registrar (35.2.2.7.2).
                i->listener_present[n] = true;
                i->registered[n] = v[8] == 2 || v[8] == 3;
            }
        }
    } else if (status->attr_type == MSRP_ATTR_TYPE_TALKER_ADV ||
               status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED) {
        const struct msrp_talker_adv *v = status->attr_val;
        for (unsigned n = 0; n < CTRL_SRP_SINKS; ++n) {
            struct srp_sink *sink = &i->sinks[n];
            if (sink->bound && memcmp(sink->stream_id.bytes,v->stream_id.bytes,8) == 0 &&
                memcmp(sink->dest_mac,v->dest_mac,6) == 0 && sink->vid == v->vlan_id) {
                if (status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED) {
                    sink->desired = 1;
                    sink->registered_kinds |= 1u;
                } else {
                    sink->registered_kinds |= 2u;
                    if (sink->desired != 1) {
                        sink->desired = 2;
                    }
                }
            }
        }
    }
}

static void capture(struct srp_sink *s, uint8_t previous)
{
    if (previous && !s->desired) {
        s->withdrawn = true;
    }
    if (!s->withdrawn && s->desired) {
        s->feedback_kind = s->desired;
    }
}

static void snapshot(struct srp_interface *i)
{
    uint8_t previous[CTRL_SRP_SINKS];
    if (!i->stale) {
        // Nothing the walk reads changed since it last ran, so it would copy
        // the values held: only each sink's capture runs (#665).
        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
            capture(&i->sinks[k],i->sinks[k].desired);
        }
        return;
    }
    i->stale = false;
    ++i->owner->walks;
    memset(i->registered,0,sizeof(i->registered));
    memset(i->listener_present,0,sizeof(i->listener_present));
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        previous[k] = i->sinks[k].desired;
        i->sinks[k].desired = 0;
        i->sinks[k].registered_kinds = 0;
    }
    (void)mrp_attr_visit(i->msrp,0,registrations,i);
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        capture(&i->sinks[k],previous[k]);
        // a binding's declaration changed: THE TRANSMIT's call declares and sends it
        i->owner->tx_held = i->owner->tx_held || i->sinks[k].desired != previous[k];
    }
}

static bool change_domain(struct srp_interface *i)
{
    if (!i->domain_owed) {
        return true;
    }
    // Reserve the only new local storage before withdrawing either old
    // declaration. The received Domain and startup Talkers already exist.
    if (mvrp_declare(i->mvrp,0,i->next_domain.vid) != 0) {
        return false;
    }
    (void)mrp_mad_leave(i->msrp,0,MSRP_ATTR_TYPE_DOMAIN,&i->domain);
    const struct srp_sink old_vlan = {.vid=i->domain.vid};
    if (i->domain.vid != i->next_domain.vid && !has_sink(i,&old_vlan,false)) {
        (void)mvrp_withdraw(i->mvrp,0,i->domain.vid);
    }
    if (i->domain.vid != i->next_domain.vid) {
        i->vlan_sent = false;
    }
    i->domain = i->next_domain;
    // The adopted Domain, before the declarations that carry it (SR_DOMAIN).
    (void)mbx_pub_domain(i->index,true,i->domain.priority,i->domain.vid);
    (void)mrp_mad_join(i->msrp,0,MSRP_ATTR_TYPE_DOMAIN,&i->domain,true);
    (void)declare_sources(i);
    i->domain_owed = false;
    return true;
}

static bool prepare_declarations(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    bool owed = false;
    if (!change_domain(i)) {
        ++m->refused; owed = true;
    }
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        struct srp_sink *s = &i->sinks[k];
        if (s->desired == 2 && !s->vlan_requested) {
            if (mvrp_declare(i->mvrp,0,s->vid) != 0) {
                ++m->refused; owed = true;
                continue;
            }
            s->vlan_requested = true;
            s->vlan_sent = i->vlan_sent && s->vid == i->domain.vid;
            for (unsigned other = 0; other < CTRL_SRP_SINKS; ++other) {
                if (i->sinks[other].bound && i->sinks[other].vlan_sent && i->sinks[other].vid == s->vid) {
                    s->vlan_sent = true;
                }
            }
        }
    }
    // One Applicant owns a StreamID, even when several bindings request it.
    // Resolve every eligible sink before changing that shared declaration.
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        struct srp_sink *s = &i->sinks[k];
        if (!s->bound) {
            continue;
        }
        uint8_t desired = 0;
        bool handled = false;
        for (unsigned other = 0; other < CTRL_SRP_SINKS; ++other) {
            const struct srp_sink *r = &i->sinks[other];
            if (r->bound && memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {
                handled = handled || other < k;
                if (r->desired != 2 || r->vlan_sent) {
                    desired |= r->desired;
                }
            }
        }
        if (handled) {
            continue;
        }
        if (desired != s->declared) {
            // A declaration rewrites the value of the attribute a registration shares (#665).
            i->stale = true;
        }
        int result = desired == s->declared ? 0 : desired ? msrp_declare_listener(i->msrp,0,&s->stream_id,desired) :
                               msrp_withdraw_listener(i->msrp,0,&s->stream_id);
        if (result == 0) {
            for (unsigned other = k; other < CTRL_SRP_SINKS; ++other) {
                struct srp_sink *r = &i->sinks[other];
                if (r->bound && memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {
                    r->declared = desired;
                }
            }
        } else {
            ++m->refused; owed = true;
        }
    }
    return owed;
}

static void reset_interface(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    if (m->owed_len && m->owed_if == i->index) {
        m->owed_len = 0;
    }
    if (m->pending_rx.len && m->pending_rx.interface == i->index) {
        m->pending_rx.len = 0;
    }
    i->rx_mark = mbx_rx_mark(MBX_CH_SRP);
    i->discard_prefix = true;
    // Every licence closes on the datapath before any revocation is reported.
    bool revoked[CTRL_SRP_SOURCES];
    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
        revoked[k] = i->active[k];
        i->active[k] = false;
        i->stop_owed[k] = false;
        // the registrar it was walked from is destroyed below (#665)
        i->listener_present[k] = false;
    }
    publish_licence(i);
    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
        if (revoked[k]) {
            ++m->stops;
            m->config.licence(m->config.ctx,i->index,k,false);
        }
    }
    withdraw_declared(i->index);
    msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);
    i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        uint8_t previous = i->sinks[k].desired;
        i->sinks[k].desired = 0; i->sinks[k].declared = 0;
        i->sinks[k].registered_kinds = 0;
        capture(&i->sinks[k],previous);
        i->sinks[k].vlan_requested = false; i->sinks[k].vlan_sent = false;
    }
    // The next pass's poll builds the new participants: both halves in one
    // pass are over the per-pass share at 8x8 (#665, srp_bounds.h).
    i->reopen_polls = 1u;
    i->reopening = true;
}

static void on_event(void *ctx, const struct mbx_event *event)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return;
    }
    if (event->type == MBX_EV_TYPE_LINK && event->interface < MBX_N_IF) {
        struct srp_interface *i = &m->ifs[event->interface];
        // A repeated UP can represent coalesced down/up edges. Only the
        // initial UP uses the already clean startup participants.
        if (i->link_seen || !event->link_up) {
            reset_interface(i);
        }
        i->link_seen = true;
        i->link = event->link_up;
    }
    m->busy = false;
}

// Whether the interface whose turn it is builds in this poll, read from its
// state as the poll starts, before any interface is visited: it has no
// participants, is not withdrawing and its link level held. Read during the
// visits, a turn interface visited first would already have spent its
// withdrawal, and the rule would hold in one orientation only (#665).
static bool turn_builds(const struct srp_mbx *m, const bool link[MBX_N_IF])
{
    unsigned t = m->build_turn % MBX_N_IF;
    const struct srp_interface *turn = &m->ifs[t];
    return !turn->msrp && !turn->reopen_polls && turn->link == link[t];
}

// A participant may hold an attribute mrp_reclaim frees (#665). lwSRP reclaims
// nothing on a participant holding a prepared PDU: while a frame is owed, its
// interface's reclaim is owed after it.
static void reclaim(struct srp_interface *i)
{
    if (i->reclaim) {
        (void)mrp_reclaim(i->msrp,0);
        (void)mrp_reclaim(i->mvrp,0);
        i->reclaim = i->owner->owed_len != 0u;
    }
}

static bool poll(void *ctx)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return false;
    }
    bool links[MBX_N_IF];
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        links[n] = mbx_link_up(n);
    }
    // Interface n builds before the one whose turn it is only when that one does not build in this poll.
    const unsigned turn = m->build_turn % MBX_N_IF;
    const bool turn_due = turn_builds(m, links);
    bool owed = false;
    bool built = false;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        struct srp_interface *i = &m->ifs[n];
        bool link = links[n];
        if (i->link != link) {
            reset_interface(i);
            i->link = link;
            i->link_seen = true;
        }
        if (i->discard_prefix && !mbx_rx_before(MBX_CH_SRP,i->rx_mark)) {
            i->discard_prefix = false;
        }
        if (i->reopen_polls) {
            --i->reopen_polls;
            owed = true;
            continue;
        }
        if (!i->msrp && (built || (n != turn && turn_due))) {
            // One interface is built a pass: both at 8x8/2if took a pass to
            // 2.08 ms of the 2.0 ms share (#665, srp_bounds.h). This one is
            // built first on the next pass, and its receive waits until then.
            owed = true;
            continue;
        }
        i->reopening = false;
        if (!i->msrp) {
            built = true;
            m->build_turn = (n + 1u) % MBX_N_IF;
            // A failed recreate is counted and retried without dereferencing it.
            msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);
            i->msrp = NULL; i->mvrp = NULL;
            if (!open_interface(i)) {
                ++m->refused; owed = true;
                if (m->pending_rx.interface == n) {
                    expire_receive(m);
                }
                continue;
            }
        }
        // Retry only after lifecycle reconciliation and older output/events.
        // One attempt per poll; the fabric tick also wakes an idle loop.
        if (m->pending_rx.len && m->pending_rx.interface == n && rx_order_ready(m)) {
            if (apply_receive(m,&m->pending_rx)) {
                m->pending_rx.len = 0;
                m->tx_held = true;
            } else {
                expire_receive(m);
            }
        }
        snapshot(i);
        for (unsigned s = 0; s < CTRL_SRP_SOURCES; ++s) {
            if (i->stop_owed[s]) {
                i->stop_owed[s] = false;
                i->active[s] = false;
                ++m->stops;
                publish_licence(i);
                m->config.licence(m->config.ctx,n,s,false);
            }
            bool active = i->link && i->vlan_sent && i->admitted[s] && i->registered[s];
            if (active != i->active[s]) {
                if (!active) {
                    ++m->stops;
                }
                i->active[s] = active;
                publish_licence(i);
                m->config.licence(m->config.ctx,n,s,active);
            }
        }
    }
    // In a pass whose build follows (tx_pass), the build's call reclaims after
    // its declarations, as this poll did before the build moved out of it; in
    // any other pass the poll does, so a record the next pass takes finds the
    // room (#665).
    if (!m->loop->tx_pass) {
        for (unsigned n = 0; n < MBX_N_IF; ++n) {
            if (m->ifs[n].msrp) {
                reclaim(&m->ifs[n]);
            }
        }
    }
    // The poll declares nothing and builds no MRPDU: THE TRANSMIT does both,
    // once a pass's input is taken (ctrl_loop.h). It sends only the frame a
    // build left owed, one a pass and oldest first (A3), and while it holds a
    // build it reports it owed, so the loop passes on to the pass that takes it.
    if (m->owed_len) {
        struct srp_interface *i = &m->ifs[m->owed_if];
        struct mrp_app *app = m->owed_ethertype == MRP_ETHERTYPE_MVRP ? i->mvrp : i->msrp;
        struct send_context send = {i,app};
        if (i->msrp && i->link &&
            mrp_transmit(app,0,m->owed_frame + 14u,sizeof(m->owed_frame) - 14u,send_pdu,&send) != 0) {
            owed = true;
        }
        if (!m->owed_len) {
            // the frame this pass carries (SRP_MBX_POLL_FRAMES): THE TRANSMIT builds none beside it
            m->resent_pass = m->loop->stats.passes;
        }
    }
    owed = owed || m->tx_held;
    m->busy = false;
    return owed;
}

// THE TRANSMIT's client (ctrl_loop.h, #665): the declarations, then at most
// SRP_MBX_POLL_FRAMES MRPDUs a call (srp_bounds.h), in the order the poll took
// them before the build moved out of it. A Domain adopted here is sent in this
// call, so no poll sees its VID unlicensed between them (Milan 4.3.2), and a
// reclaim comes after the declarations, so a refused declaration does not take
// the room a retained receive waits for. A call that visits every participant
// and sends nothing holds no build until a centisecond, a record or a
// declaration may owe one.
static bool transmit(void *ctx)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return false;
    }
    bool reclaims = false;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        reclaims = reclaims || (m->ifs[n].msrp && m->ifs[n].reclaim);
    }
    if (m->resent_pass == m->loop->stats.passes || (!m->tx_held && !m->owed_len && !reclaims)) {
        // the pass's frame is the owed one the poll sent, or nothing is held and nothing waits to be reclaimed
        m->busy = false;
        return m->tx_held;
    }
    m->tx_age = 0;
    bool owed = false;
    if (!m->owed_len) {
        for (unsigned n = 0; n < MBX_N_IF; ++n) {
            if (m->ifs[n].msrp) {
                owed = prepare_declarations(&m->ifs[n]) || owed;
            }
        }
    }
    // A participant that sent ends the call's transmissions, and the cursor
    // resumes at the next participant on the next call, which the owed result
    // runs at once.
    unsigned sent = 0;
    for (unsigned attempt = 0; attempt < 2u * MBX_N_IF && sent < SRP_MBX_POLL_FRAMES; ++attempt) {
        unsigned slot = m->owed_len ? 2u * m->owed_if + (m->owed_ethertype == MRP_ETHERTYPE_MVRP) : m->cursor;
        struct srp_interface *i = &m->ifs[slot / 2u];
        struct mrp_app *app = slot % 2u ? i->mvrp : i->msrp;
        struct send_context send = {i,app};
        if (!i->msrp) {
            m->cursor = (slot + 1u) % (2u * MBX_N_IF);
            continue;
        }
        reclaim(i);
        if (i->link) {
            int result = mrp_transmit(app,0,m->owed_frame + 14u,sizeof(m->owed_frame) - 14u,send_pdu,&send);
            if (result != 0) {
                owed = true;
            }
            sent += result > 0 ? 1u : 0u;
        }
        if (!m->owed_len) {
            m->cursor = (slot + 1u) % (2u * MBX_N_IF);
        }
        if (m->owed_len) {
            break;
        }
    }
    m->tx_held = owed;
    m->busy = false;
    return owed;
}

// THE TRANSMIT's age: a held build past CTRL_LOOP_TX_AGE centiseconds, with
// no frame owed ahead of it, takes a pass of its own (ctrl_loop.h).
static bool transmit_aged(void *ctx)
{
    const struct srp_mbx *m = ctx;
    return m->tx_held && !m->owed_len && m->tx_age > CTRL_LOOP_TX_AGE;
}

bool srp_mbx_attach(struct srp_mbx *m, struct ctrl_loop *loop)
{
    if (!enter(m)) {
        return false;
    }
    bool ok = m->initialized && !m->loop && !timer_owner && loop->n_ticks < CTRL_LOOP_MAX_TICKS &&
              loop->n_polls < CTRL_LOOP_MAX_POLLS && loop->n_sinks < CTRL_LOOP_MAX_SINKS && !loop->rx[MBX_CH_SRP].fn &&
              !loop->transmit;
    if (ok) {
        for (unsigned n = 0; n < MBX_N_IF; ++n) {
            m->ifs[n].link = mbx_link_up(n);
        }
        m->loop = loop;
        m->resent_pass = loop->stats.passes - 1u;
        timer_owner = m;
        (void)ctrl_loop_bind_rx(loop,MBX_CH_SRP,receive,m);
        (void)ctrl_loop_add_sink(loop,on_event,m);
        (void)ctrl_loop_add_tick(loop,tick);
        (void)ctrl_loop_add_poll(loop,poll,m);
        (void)ctrl_loop_set_transmit(loop,transmit,transmit_aged,m);
        ctrl_loop_set_rx_ready(loop,MBX_CH_SRP,rx_ready);
    }
    m->busy = false;
    return ok;
}

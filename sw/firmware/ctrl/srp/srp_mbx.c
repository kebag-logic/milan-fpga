// SPDX-License-Identifier: CERN-OHL-W-2.0
// The adapter owns no heap or protocol tables; lwSRP owns its MRP machines.
#include "srp_mbx.h"
#include <string.h>
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
// This recovery limit does not extend the 10 ms service budget.
#define SRP_RX_RETRY_MS 1000u

static struct srp_mbx *timer_owner;
static void tick(void);
static bool poll(void *ctx);
static void receive(void *ctx, const struct mbx_frame *frame);
static void on_event(void *ctx, const struct mbx_event *event);
static void snapshot(struct srp_interface *i);

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
    m->busy = false;
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

static void left(struct msrp_ctx *ctx, uint8_t port, uint8_t type, const void *value)
{
    if (type == MSRP_ATTR_TYPE_LISTENER) {
        listener(ctx,port,value,MSRP_LISTENER_DECL_IGNORE,false);
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
    }
}

static bool declare_sources(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    uint64_t used = 0;
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
    }
    return true;
}

static bool interested_msrp(void *ctx, uint8_t port, uint8_t type, const void *value)
{
    (void)port;
    struct srp_interface *i = ctx;
    // Observe the previous complete wire AttributeEvent. A kind replacement
    // is atomic inside one event; a following Lv/New pair is two events.
    // The visitor is read-only: no protocol entry or delivery occurs here.
    snapshot(i);
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

static bool create_participants(struct srp_interface *i)
{
    i->msrp_ctx = (struct msrp_ctx){.on_domain=domain,.on_listener=listener,.on_leave=left};
    i->msrp = msrp_app_create(1,&i->msrp_ctx);
    i->mvrp = mvrp_app_create(1,&i->mvrp_ctx);
    if (!i->msrp || !i->mvrp) {
        return false;
    }
    // These valid constants are installed before creating any attribute.
    (void)mrp_port_configure(i->msrp,0,20,500,1000,(uint32_t)i->mac,true);
    (void)mrp_port_configure(i->mvrp,0,20,500,1000,(uint32_t)i->mac ^ 0x91u,true);
    mrp_set_rx_filter(i->msrp,interested_msrp,i);
    mrp_set_rx_filter(i->mvrp,interested_mvrp,i);
    i->vlan_sent = false;
    i->domain = (struct msrp_domain){6,3,2};
    if (mrp_mad_join(i->msrp,0,MSRP_ATTR_TYPE_DOMAIN,&i->domain,true) != 0 ||
        mvrp_declare(i->mvrp,0,2) != 0) {
        return false;
    }
    return declare_sources(i);
}

static bool open_interface(struct srp_interface *i)
{
    if (create_participants(i)) {
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
        m->loop = NULL;
    }
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        struct srp_interface *i = &m->ifs[n];
        for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
            if (i->active[k]) {
                i->active[k] = false;
                m->config.licence(m->config.ctx,n,k,false);
            }
        }
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
    if (old.bound) {
        // Judge the complete new binding set, including the replacement.
        if (!has_sink(i,&old,true)) {
            (void)msrp_withdraw_listener(i->msrp,0,&old.stream_id);
        }
        if (old.vid != i->domain.vid && !has_sink(i,&old,false)) {
            (void)mvrp_withdraw(i->mvrp,0,old.vid);
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
    int result = app ? mrp_rx(app,0,frame->bytes + 14,frame->len - 14u) : -SHLAN_ERROR_NO_MEMORY;
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
    if (!m->owed_len) {
        memcpy(m->owed_frame,s->app->ops->group_addr,6);
        wire_put_be(m->owed_frame + 6,s->interface->mac,6);
        wire_put_be(m->owed_frame + 12,s->app->ops->ethertype,2);
        memcpy(m->owed_frame + 14,pdu,len);
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
                } else if (sink->desired != 1) {
                    sink->desired = 2;
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
    memset(i->registered,0,sizeof(i->registered));
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        previous[k] = i->sinks[k].desired;
        i->sinks[k].desired = 0;
    }
    (void)mrp_attr_visit(i->msrp,0,registrations,i);
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        capture(&i->sinks[k],previous[k]);
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
    for (unsigned k = 0; k < CTRL_SRP_SOURCES; ++k) {
        if (i->active[k]) {
            i->active[k] = false;
            ++m->stops;
            m->config.licence(m->config.ctx,i->index,k,false);
        }
        i->stop_owed[k] = false;
    }
    msrp_app_destroy(i->msrp); mvrp_app_destroy(i->mvrp);
    i->msrp = NULL; i->mvrp = NULL; i->domain_owed = false;
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        uint8_t previous = i->sinks[k].desired;
        i->sinks[k].desired = 0; i->sinks[k].declared = 0;
        capture(&i->sinks[k],previous);
        i->sinks[k].vlan_requested = false; i->sinks[k].vlan_sent = false;
    }
    if (!open_interface(i)) {
        ++m->refused;
    }
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

static bool poll(void *ctx)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return false;
    }
    bool owed = false;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        struct srp_interface *i = &m->ifs[n];
        bool link = mbx_link_up(n);
        if (i->link != link) {
            reset_interface(i);
            i->link = link;
            i->link_seen = true;
        }
        if (i->discard_prefix && !mbx_rx_before(MBX_CH_SRP,i->rx_mark)) {
            i->discard_prefix = false;
        }
        if (!i->msrp) {
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
                m->config.licence(m->config.ctx,n,s,false);
            }
            bool active = i->link && i->vlan_sent && i->admitted[s] && i->registered[s];
            if (active != i->active[s]) {
                if (!active) {
                    ++m->stops;
                }
                i->active[s] = active;
                m->config.licence(m->config.ctx,n,s,active);
            }
        }
    }
    if (!m->owed_len) {
        for (unsigned n = 0; n < MBX_N_IF; ++n) {
            if (m->ifs[n].msrp) {
                owed = prepare_declarations(&m->ifs[n]) || owed;
            }
        }
    }
    for (unsigned attempt = 0; attempt < 2u * MBX_N_IF; ++attempt) {
        unsigned slot = m->owed_len ? 2u * m->owed_if + (m->owed_ethertype == MRP_ETHERTYPE_MVRP) : m->cursor;
        struct srp_interface *i = &m->ifs[slot / 2u];
        struct mrp_app *app = slot % 2u ? i->mvrp : i->msrp;
        struct send_context send = {i,app};
        if (!i->msrp) {
            m->cursor = (slot + 1u) % (2u * MBX_N_IF);
            continue;
        }
        (void)mrp_reclaim(i->msrp,0);
        (void)mrp_reclaim(i->mvrp,0);
        if (i->link) {
            int result = mrp_transmit(app,0,m->frame,sizeof(m->frame) - 14u,send_pdu,&send);
            if (result != 0) {
                owed = true;
            }
        }
        if (!m->owed_len) {
            m->cursor = (slot + 1u) % (2u * MBX_N_IF);
        }
        if (m->owed_len) {
            break;
        }
    }
    m->busy = false;
    return owed;
}

bool srp_mbx_attach(struct srp_mbx *m, struct ctrl_loop *loop)
{
    if (!enter(m)) {
        return false;
    }
    bool ok = m->initialized && !m->loop && !timer_owner && loop->n_ticks < CTRL_LOOP_MAX_TICKS &&
              loop->n_polls < CTRL_LOOP_MAX_POLLS && loop->n_sinks < CTRL_LOOP_MAX_SINKS && !loop->rx[MBX_CH_SRP].fn;
    if (ok) {
        for (unsigned n = 0; n < MBX_N_IF; ++n) {
            m->ifs[n].link = mbx_link_up(n);
        }
        m->loop = loop;
        timer_owner = m;
        (void)ctrl_loop_bind_rx(loop,MBX_CH_SRP,receive,m);
        (void)ctrl_loop_add_sink(loop,on_event,m);
        (void)ctrl_loop_add_tick(loop,tick);
        (void)ctrl_loop_add_poll(loop,poll,m);
        ctrl_loop_set_rx_ready(loop,MBX_CH_SRP,rx_ready);
    }
    m->busy = false;
    return ok;
}

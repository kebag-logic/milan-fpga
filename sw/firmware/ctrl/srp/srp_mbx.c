// SPDX-License-Identifier: CERN-OHL-W-2.0
// The adapter owns no heap or protocol tables; lwSRP owns its MRP machines.
#include "srp_mbx.h"
#include <string.h>
#include "srp_bounds.h"
#include "../plat/ctrl_cc.h"
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
// held_count counts the StreamIDs held (#925, srp_held).
_Static_assert(SRP_HELD_STREAMS <= 255u, "held_count counts every StreamID held");
// The pool's fixed blocks fund the kept Talkers beside the Domain's and the default VID's (#969, srp_mbx.h).
_Static_assert(SRP_KEPT_TALKERS + SRP_POOL_DOMAIN_BLOCKS <= SRP_POOL_FIXED_BLOCKS, "the fixed blocks fund the kept");
_Static_assert(SRP_RECORD_VALUES >= CTRL_SRP_SINKS && SRP_RECORD_VALUES <= CTRL_SRP_SINKS + SRP_KEPT_TALKERS,
               "V holds every bound sink and no more than the bound and the kept (#977)");
// kept_count counts an interface's kept Talker attributes, each a block of the pool (#969, srp_mbx.h).
_Static_assert(SRP_POOL_MEDIUM_BLOCKS + SRP_POOL_LARGE_BLOCKS <= 255u, "kept_count counts every kept attribute");
// What owes an interface's next receive a count of its kept Talkers (#969, srp_mbx.h kept_due; count_kept): a binding
// changed, which moves what is kept; or one counted or kept since may end with its block freed after the count (one
// kept may never register, or a registration end), which a block returned shows.
#define SRP_KEPT_BOUND 1u
#define SRP_KEPT_PENDING 2u

// The JoinTime every participant is configured with, in centiseconds (create_participants): the loop's, whose
// THE TRANSMIT bound is derived from it (ctrl_loop.h, CTRL_LOOP_JOIN_CS).
#define SRP_JOIN_CS CTRL_LOOP_JOIN_CS
// The LeaveAllTime every participant is configured with, in centiseconds (create_participants): 10 s (IEEE 802.1Q-2018
// Table 10-7; Milan v1.2 Table 4.3).
#define SRP_LEAVEALL_CS 1000u
// The nominal longest LeaveAll period, in centiseconds: IEEE 802.1Q-2018 10.7.4.3 draws each leavealltimer, a peer's
// too, below 1.5 x LeaveAllTime; Milan v1.2 Table 4.3's tolerance, to 15.5 s, is not covered (#951).
#define SRP_LEAVEALL_LONGEST_CS (SRP_LEAVEALL_CS + SRP_LEAVEALL_CS / 2u)
// A withdrawn Talker's hold-off, in centiseconds, before its StreamID declares another FirstValue (#895). MSRP does not
// support a changed FirstValue on a StreamID: at least two LeaveAllTime periods pass between the Leave and the new
// declaration (IEEE 802.1Q-2018 35.2.2.8). The new declaration reaches the wire within two nominal longest periods,
// 30 s, of the Leave's request, where the count starts (#951); two at Milan's tolerance edge reach 31 s. The count's
// end leaves at most a JoinTime and THE TRANSMIT's MRPDU by every source before the declaration is on the wire (hold,
// CTRL_LOOP_TX_MS, the built design's, held at or over its tx row at every shape by flip_grade.py --check:
// rows_tiers.tx_statements, and tx_held at 8x8/1if), so both are counted inside the two periods: the declaration
// comes no sooner than two longest periods less both terms and no later than 30 s (#956, the owner's decision of
// 2026-11-21).
#define SRP_REDECLARE_CS (2u * SRP_LEAVEALL_LONGEST_CS - SRP_JOIN_CS - (CTRL_LOOP_TX_MS + 9u) / 10u)
// Each source's count (srp_mbx.h, held_cs) holds the whole hold-off.
_Static_assert(SRP_REDECLARE_CS < 1ul << 8u * sizeof ((struct srp_mbx *)0)->held_cs[0], "held_cs holds the hold-off");
// A participant's slot: MSRP then MVRP of each interface.
#define SRP_SLOTS (2u * MBX_N_IF)

static struct srp_mbx *timer_owner;
static void tick(void);
static bool poll(void *ctx);
static void transmit(void *ctx, unsigned most);
static bool transmit_aged(void *ctx);
static void receive(void *ctx, const struct mbx_frame *frame);
static void on_event(void *ctx, const struct mbx_event *event);
static void snapshot(struct srp_interface *i);
static void capture(struct srp_sink *s, uint8_t previous);
static void count_held(struct srp_mbx *m);

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

// Whether the n bytes at a and at b are the same (#665): a record's StreamID
// and MAC comparisons, in the receive filter, the indications and the
// registrar walk, are equality tests, a source or a sink each, and through
// memcmp each paid its alignment checks and its ordering's byte loop, about
// 170 cycles. This one stops at the first byte that differs, from the last:
// one talker's StreamIDs differ in their unique ID, the last two bytes (IEEE
// 802.1Q-2018 35.2.2.8.2), and one talker's MACs in their last bytes.
static CTRL_CC_NOINLINE bool same(const uint8_t *a, const uint8_t *b, unsigned n)
{
    while (n != 0u) {
        --n;
        if (a[n] != b[n]) {
            return false;
        }
    }
    return true;
}

// A set of octets, bit b of word b / 32 for an octet b (#977): the last octets of the StreamIDs a list holds, which
// its search reads first, so a StreamID ending in an octet none of them ends in costs that one test, not the list's
// scan (srp_mbx.h kept_octets, held_octets). A bit set for an octet no entry ends in costs only the scan.
static CTRL_CC_INLINE bool octet_in(const uint32_t *set, uint8_t octet)
{
    return (set[octet >> 5] >> (octet & 31u) & 1u) != 0u;
}

static CTRL_CC_INLINE void octet_add(uint32_t *set, uint8_t octet)
{
    set[octet >> 5] |= 1u << (octet & 31u);
}

// A StreamID's eight octets copied one at a time (#977): a call of memcpy costs the control CPU about 400 cycles for
// them, which a Talker kept for a StreamID no binding holds paid twice, its kept list's copy and its held entry's.
static CTRL_CC_INLINE void copy_id(uint8_t *to, const uint8_t *from)
{
    to[0] = from[0];
    to[1] = from[1];
    to[2] = from[2];
    to[3] = from[3];
    to[4] = from[4];
    to[5] = from[5];
    to[6] = from[6];
    to[7] = from[7];
}

// The sources whose StreamID is the Listener's at id, bit n source n (#665's ruling of 2026-11-20, item 3): the receive
// filter, a Listener's indication, its Registrar change and the walk each look a Listener up here, once, where each
// had matched it against every source with a call of same. same is entered only where the last bytes agree: one
// talker's StreamIDs differ in their unique ID, so every other source of the shape is told apart by that one compare.
static CTRL_CC_NOINLINE uint32_t sources_of(const struct srp_interface *i, const uint8_t *id)
{
    uint32_t of = 0u;
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        const uint8_t *s = i->sources[n].value.stream_id.bytes;
        if (s[7] == id[7] && same(s,id,8)) {
            of |= 1u << n;
        }
    }
    return of;
}

// A slot's participant: each interface's MSRP, then its MVRP.
static struct mrp_app *participant(const struct srp_interface *i, unsigned slot)
{
    return slot % 2u ? i->mvrp : i->msrp;
}

static void tick(void)
{
    struct srp_mbx *m = timer_owner;
    if (!enter(m)) {
        return;
    }
    shlan_timer_tick();
    m->retry_spent = false;
    // lwSRP arms a participant's join timer as it sends and reports no expiry: join_left keeps the same count, so
    // the centisecond that ends it is the one an MRPDU waiting on it became owed in, as a LeaveAll Active state owes
    // its LeaveAll once no join timer holds it, IEEE 802.1Q 10.7.4.1 and Table 10-5 (THE TRANSMIT in ctrl_loop.h).
    for (unsigned slot = 0; slot < SRP_SLOTS; ++slot) {
        struct srp_interface *i = &m->ifs[slot / 2u];
        enum mrp_la_state la = MRP_LA_STATE_PASSIVE;
        if (i->msrp) {
            (void)mrp_port_status(participant(i,slot),0,&la,NULL);
        }
        if (m->join_left[slot] != 0u ? --m->join_left[slot] == 0u : la == MRP_LA_STATE_ACTIVE) {
            m->tx_due |= (uint8_t)(1u << (slot / 2u));
        }
    }
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        if (m->ifs[n].msrp) {
            snapshot(&m->ifs[n]);
        }
    }
    count_held(m);
    m->busy = false;
}

// A declaration the interface's participants must send, owed a pass given whole. While notices are queued it waits for
// the join timer, which holds the frame back anyway and whose end owes the pass that declares and sends: what a peer's
// records make owed then comes at the JoinTime's rate, whatever their rate, and THE RETRY's bound can count it.
static void hold(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    if (m->join_left[2u * i->index] == 0u || !m->loop->retry_queued) {
        m->tx_due |= (uint8_t)(1u << i->index);
    }
}

// Each withdrawn source's hold-off, a centisecond at a time (tick): at its end
// a valid source whose destination changed may declare it, which THE TRANSMIT
// does (#895, declare_sources).
static void count_held(struct srp_mbx *m)
{
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        if (m->held_cs[n] != 0u && --m->held_cs[n] == 0u) {
            for (unsigned k = 0; k < MBX_N_IF; ++k) {
                struct srp_interface *i = &m->ifs[k];
                if (((i->gate & i->readdressed) >> n & 1u) != 0u) {
                    i->sources_owed = true;
                    hold(i);
                }
            }
        }
    }
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

// A Listener's indication copies its declaration where it is reported, so it owes no registrar walk (#930): lwSRP
// indicates a Listener whose stored declaration changed while it registers, and every Registrar change that starts or
// ends a registration, which the observer copies too (listener_moved). So the declaration it indicates, Ignore at a
// registration's end (left), is what a source's STREAM_OUTPUT shows of the Listener registered for its stream (#943's
// REGISTERING and REGISTERING_FAILED) while the source's DA gate is open on the interface: the gate is what the
// datapath's face reports as the output declaring, and MAAP opens it on the source's own interface only (maap_mbx.c).
// Each change of it there is noticed for the output's GET_STREAM_INFO notice (#957; Milan v1.2 5.4.5.2, Table 5.22;
// IEEE 1722.1-2021 7.5.2), as the release processor notices a Listener registration change (its LISTENER_REG_CHANGE).
// A Listener declared again unchanged shows the same, one registered again after a LeaveAll is not indicated, and
// behind a closed gate the face shows neither flag.
static void listener(struct msrp_ctx *ctx, uint8_t port,
                      const struct msrp_stream_id *identity, enum msrp_listener_decl declaration, bool is_new)
{
    (void)port; (void)is_new;
    struct srp_interface *i = from_ctx(ctx);
    const uint32_t of = sources_of(i,identity->bytes);
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        if ((of >> n & 1u) != 0u) {
            i->registered[n] = declaration == MSRP_LISTENER_DECL_READY ||
                               declaration == MSRP_LISTENER_DECL_READY_FAILED;
            if (!i->registered[n] && i->active[n]) {
                i->stop_owed[n] = true;
            }
            i->noticed |= (uint32_t)(i->declaration[n] != declaration) << n & i->gate;
            i->declaration[n] = (uint8_t)declaration;
        }
    }
}

// The Listener declaration a binding's registered Talkers ask for: Ready (2) for an Advertise, AskingFailed (1) for a
// Failed (IEEE 802.1Q-2018 35.2.2.7.2), each the bit of its kind. A talker declares one of the two for a stream and
// moves directly between them (35.1.2.1). A received JoinIn or JoinMt of one kind replaces a registered other
// (35.2.6), as lwSRP does, but lwSRP registers a New beside it. 35.2.6's informative NOTE gives Failed precedence while
// both are registered. Milan v1.2 5.3.8.5 has a Listener Ready declared while a matching Advertise is received, and
// the ruling on #925 follows it: the kind registered latest, the talker's current state, decides, and the other once
// the latest leaves. Every binding of the StreamID records the latest (talker_changed), and a StreamID none binds
// holds it while both stay registered (srp_mbx_bind), so a binding made at any time takes it. Both registered with no
// latest known is reached only past the held table's bound, and takes Failed.
static uint8_t listener_kind(const struct srp_sink *s)
{
    const uint8_t kinds = (s->registered_kinds & s->latest_kind) != 0u ? s->latest_kind : s->registered_kinds;
    return (kinds & 1u) != 0u ? 1u : kinds;
}

// The held table's scan for an interface's StreamID (held_stream): same is entered only where the last bytes agree, as
// in sources_of: one talker's StreamIDs differ in their unique ID (#977).
static CTRL_CC_NOINLINE struct srp_held *held_scan(struct srp_mbx *m, unsigned interface, const uint8_t *stream_id)
{
    for (unsigned n = 0; n < m->held_count; ++n) {
        const uint8_t *held = m->held[n].stream_id.bytes;
        if (held[7] == stream_id[7] && m->held[n].interface == interface && same(held,stream_id,8)) {
            return &m->held[n];
        }
    }
    return NULL;
}

// The held entry of an interface's StreamID, or NULL (#925, srp_held), scanned for only where a StreamID held ends in
// the same octet, a test made where it is asked, so a StreamID no entry ends like calls nothing (#977).
static CTRL_CC_INLINE struct srp_held *held_stream(struct srp_mbx *m, unsigned interface, const uint8_t *stream_id)
{
    return octet_in(m->held_octets,stream_id[7]) ? held_scan(m,interface,stream_id) : NULL;
}

// A held entry ends: the last one takes its place (#925, srp_held).
static void release_held(struct srp_mbx *m, struct srp_held *h)
{
    *h = m->held[--m->held_count];
    // another entry may end in the octet this one did, so the octets are kept until none is held (#977)
    if (m->held_count == 0u) {
        memset(m->held_octets,0,sizeof(m->held_octets));
    }
}

_Static_assert(CTRL_SRP_SINKS <= 32u, "an interface's touched sinks hold a bit for each sink");
_Static_assert(CTRL_SRP_SINKS < 255u, "a sink index holds each sink plus one in an octet");

// The interface's sink index (srp_mbx.h, lane_first): every bound sink in the lane of its StreamID's last byte, each
// lane ascending, so a visit of a lane finds what the loop over every sink found, in its order. Only srp_mbx_bind
// writes a binding, and it rebuilds the index; srp_mbx_init's zeroing leaves every lane empty, as every sink unbound
// (#977, its ruling of 2026-11-23, item 5).
static void index_sinks(struct srp_interface *i)
{
    memset(i->lane_first,0,sizeof(i->lane_first));
    i->bound_sinks = 0u;
    for (unsigned k = CTRL_SRP_SINKS; k-- != 0u;) {
        i->lane_next[k] = 0u;
        if (i->sinks[k].bound) {
            ++i->bound_sinks;
            uint8_t *first = &i->lane_first[i->sinks[k].stream_id.bytes[7] % SRP_SINK_LANES];
            i->lane_next[k] = *first;
            *first = (uint8_t)(k + 1u);
        }
    }
}

// Indications copy registration changes only. The filter below closes the
// preceding complete wire event, after both halves of an atomic replacement.
static void talker_changed(struct srp_interface *i, const struct msrp_talker_adv *v,
                           uint8_t kind, bool registered)
{
    bool bound = false;
    const uint8_t last = v->stream_id.bytes[7];
    // the bound sinks of the StreamID's lane (index_sinks), the last byte first, as sources_of: one talker's
    // StreamIDs differ in their unique ID (#977)
    for (unsigned n = i->lane_first[last % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {
        const unsigned k = n - 1u;
        struct srp_sink *s = &i->sinks[k];
        if (s->stream_id.bytes[7] == last && same(s->stream_id.bytes,v->stream_id.bytes,8)) {
            bound = true;
            // what listener_kind reads of this sink changed: the receive filter takes it again (#977)
            i->touched |= 1u << k;
            s->registered_kinds &= (uint8_t)~kind;
            // every binding of the StreamID holds its latest registration, whatever its destination and VID, so a
            // binding made later can take it from any of them (#925, srp_mbx_bind)
            s->latest_kind = registered ? kind : s->latest_kind;
            if (registered && same(s->dest_mac,v->dest_mac,6) && s->vid == v->vlan_id) {
                s->registered_kinds |= kind;
            }
        }
    }
    // What an indication of a bound StreamID writes, snapshot copies (#665). One of a StreamID none binds changes no
    // binding, and the walk copies nothing of its kept attribute (#969, count_kept).
    i->stale = i->stale || bound;
    // A StreamID none binds is held while both its kinds stay registered, or from a registration it was kept for: a
    // leave of either ends that, and the registration latest decides while it holds, as it does for a bound StreamID
    // (#969; #925, srp_held). lwSRP reports every registration's end, its leave timer's too, whatever the receive
    // filter answers. Past the table's bound nothing more is held; a binding of both kinds with no latest takes Failed.
    struct srp_mbx *m = i->owner;
    // a registration of a StreamID none binds that ends may be a kept one, whose block mrp_reclaim frees later: the
    // count after that return owes it no more (#969, count_kept)
    if (!bound && !registered) {
        m->kept_due[i->index] |= SRP_KEPT_PENDING;
    }
    struct srp_held *h = bound ? NULL : held_stream(m,i->index,v->stream_id.bytes);
    if (registered && !bound && h == NULL && m->held_count < SRP_HELD_STREAMS) {
        h = &m->held[m->held_count++];
        copy_id(h->stream_id.bytes,v->stream_id.bytes);
        h->interface = (uint8_t)i->index;
        octet_add(m->held_octets,v->stream_id.bytes[7]);
    }
    if (h != NULL && registered) {
        h->latest_kind = kind;
    } else if (h != NULL) {
        release_held(m,h);
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
        hold(i);
    }
}

// What declare_sources joins (#895): the valid sources not declared and those
// whose type changes, every valid one again (an adopted Domain's VID), or
// every valid one of new participants, which publish nothing if one is refused
// (withdraw_declared).
#define SRP_DECLARE_CHANGED 0u
#define SRP_DECLARE_EVERY 1u
#define SRP_DECLARE_NEW 2u

// The interface's Talker declarations (#895). A source declares only while its SRP parameters are valid (gate,
// Milan v1.2 4.3.3.1 and 5.3.7.4), at once: Talker Advertise once it is allocated and its bandwidth fits three
// quarters of the link after the sources before it, else Talker Failed with the interface's MAC as system identifier,
// code 1 if it is allocated and 2 if not (IEEE 802.1Q-2018 35.2.2.8.7, Table 35-6). A declared source withdraws when
// its parameters lapse or its destination changes. MSRP does not support a changed FirstValue on a StreamID
// (35.2.2.8): a changed destination waits SRP_REDECLARE_CS after the Leave, an unchanged one may be declared again at
// once, and a type its admission changes swaps in place, the new one joined before the old leaves. talkers holds what
// the participants declared, and at a creation after a reset what the destroyed ones did, whose declarations left
// with no Leave: the rules hold across a reset too.
static bool declare_sources(struct srp_interface *i, unsigned how)
{
    struct srp_mbx *m = i->owner;
    uint32_t advertise = 0;
    uint64_t used = 0;
    bool done = true;
    // A join rewrites the value of the attribute a registration shares (#665).
    i->stale = true;
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        const uint32_t bit = 1u << n;
        // admitted[n] is the declared type: Advertise when set
        const bool was = i->admitted[n];
        const bool valid = (i->gate & bit) != 0u;
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
        if ((i->talkers & bit) != 0u && (!valid || (i->readdressed & bit) != 0u)) {
            // the licence closes before TALKER_DECL drops the source, so the stream gate never trails it
            if (i->active[n]) {
                i->active[n] = false;
                ++m->stops;
                publish_licence(i);
                m->config.licence(m->config.ctx,i->index,n,false);
            }
            // lwSRP finds a Talker by its type and StreamID, and refuses a Leave while the participant holds an MRPDU
            // the ring refused (mrp_mad.c), which the declarations after THE TRANSMIT's build may meet. The source
            // then stays declared, in TALKER_DECL too, and its withdrawal is owed with THE TRANSMIT's next
            // declarations, whose first pass meets no frame owed (transmit_aged): lwSRP takes it there, and the
            // hold-off starts at the Leave it took (#895)
            if (mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,&value) != 0) {
                done = false;
            } else {
                i->talkers &= ~bit;
                m->held_cs[n] = SRP_REDECLARE_CS;
            }
        }
        if (!admitted) {
            wire_put_be(value.failure_info + 2,i->mac,6);
            value.failure_info[8] = i->sources[n].allocated ? 1 : 2;
        }
        const bool waits = (i->readdressed & bit) != 0u && m->held_cs[n] != 0u;
        // the type declared after this call: the old one unless a join succeeds
        bool advertised = was;
        if (valid && !waits && (how != SRP_DECLARE_CHANGED || (i->talkers & bit) == 0u || admitted != was)) {
            if (mrp_mad_join(i->msrp,0,admitted ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,
                             &value,true) != 0) {
                if (how == SRP_DECLARE_NEW) {
                    return false;
                }
                done = false;
            } else {
                if ((i->talkers & bit) != 0u && admitted != was) {
                    (void)mrp_mad_leave(i->msrp,0,was ? MSRP_ATTR_TYPE_TALKER_ADV : MSRP_ATTR_TYPE_TALKER_FAILED,
                                        &value);
                }
                i->talkers |= bit;
                i->readdressed &= ~bit;
                advertised = admitted;
            }
        }
        i->admitted[n] = advertised && (i->talkers & bit) != 0u;
        if (i->admitted[n]) {
            used += slope;
            advertise |= bit;
        }
    }
    // The admitted bandwidth (IDLE_SLOPE) and the declared sources
    // (TALKER_DECL), after the requests and before the build that sends them:
    // a withdrawn source's bit is clear before its Leave leaves. used is at
    // most three quarters of a 32-bit link rate.
    (void)mbx_pub_idle_slope(i->index,(uint32_t)used);
    (void)mbx_pub_talker_decl(i->index,i->talkers);
    // a refused join or withdrawal is tried again with THE TRANSMIT's next declarations
    i->sources_owed = !done;
    // Each source whose declaration changed against what its STREAM_OUTPUT last showed is noticed (#936; Milan v1.2
    // 5.4.5.2, Table 5.22; IEEE 1722.1-2021 7.5.2): declared or withdrawn, or still declared with its type swapped or
    // on another VID (an adopted Domain's). A failed creation returns before this, so what it joined is noticed once
    // it succeeds. A Talker Failed's code follows the source's allocation, which only a withdrawal changes
    // (srp_mbx_gate).
    const uint32_t kept = i->talkers & i->shown;
    uint32_t moved = (i->talkers ^ i->shown) | ((advertise ^ i->shown_advertise) & kept);
    if (i->domain.vid != i->shown_vid) {
        moved |= kept;
    }
    i->noticed |= moved;
    i->shown = i->talkers;
    i->shown_advertise = advertise;
    i->shown_vid = i->domain.vid;
    return done;
}

// The kind of a Talker attribute type: 1 Failed, 2 Advertise (srp_sink.registered_kinds' bits).
static uint8_t talker_kind(uint8_t type)
{
    return type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;
}

// A Talker attribute of a StreamID none of the interface's bindings holds, kept so a binding made later takes its
// registration in the walk it owes (#969): ACMP initiates the reservation only once the talker answers its probe
// (Milan v1.2 5.5.3.5.18 step 4), and a talker declares once, then stays quiet until a LeaveAll (IEEE 802.1Q-2018
// Table 10-3), so one refused here is not seen again before then. Kept already, or while the interface keeps fewer
// than SRP_KEPT_TALKERS, which the pool's fixed blocks fund (srp_mbx.h): kept_count, counted before the receive
// (count_kept), and each one kept since adds one. One kept now may end with no registration (a Leave lwSRP creates
// it for, or an allocation refused), so the count is pending until a count sees it. Past the bound the receive
// ignores it, as for every StreamID before #969. The filter reads no walk's result, so the walk's schedule moves no
// answer of it (#930). The list is scanned only where a StreamID it lists ends in the same octet, and same is entered
// only where the last bytes agree, as in sources_of (#977). The kept a record can register are at most V less the
// bound sinks (SRP_RECORD_VALUES; #977, its ruling of 2026-11-27 on the population bound, item 2): the filter takes
// only the first that many listed, and keeps a new one only below it, so the bound and the kept a record registers
// are never more than V.
static bool keep_talker(struct srp_interface *i, uint8_t type, const uint8_t *stream_id)
{
    struct srp_mbx *m = i->owner;
    struct srp_kept *kept = m->kept[i->index];
    const uint8_t kind = talker_kind(type);
    uint8_t *count = &m->kept_count[i->index];
    const unsigned room = SRP_RECORD_VALUES - i->bound_sinks;
    const unsigned bound = room < SRP_KEPT_TALKERS ? room : SRP_KEPT_TALKERS;
    const unsigned listed = *count < bound ? *count : bound;
    for (unsigned n = octet_in(m->kept_octets[i->index],stream_id[7]) ? 0u : listed; n < listed; ++n) {
        if (kept[n].kind == kind && kept[n].stream_id.bytes[7] == stream_id[7] &&
            same(kept[n].stream_id.bytes,stream_id,8)) {
            return true;
        }
    }
    if (*count >= bound) {
        return false;
    }
    copy_id(kept[*count].stream_id.bytes,stream_id);
    octet_add(m->kept_octets[i->index],stream_id[7]);
    kept[(*count)++].kind = kind;
    m->kept_due[i->index] |= SRP_KEPT_PENDING;
    return true;
}

static bool interested_msrp(void *ctx, uint8_t port, uint8_t type, const void *value)
{
    (void)port;
    struct srp_interface *i = ctx;
    // lwSRP doc/integrator.md:321-323 and mrp.h:288-290 forbid reentry.
    // Observe the previous complete event from copied indication data only.
    // Atomic replacement stays continuous; Lv then New remains two events.
    // Only a bound Talker's indication changes what listener_kind reads, and it marks the interface stale
    // (talker_changed), which only the walk clears. apply_receive's snapshot leaves every sink at listener_kind with
    // its capture made, so while the interface is not stale the previous event changed no sink and this pass would
    // change nothing: it runs from the first Talker indication of the receive (#665's ruling of 2026-11-20, item 3),
    // for the sinks an indication touched since it last ran (talker_changed): listener_kind reads nothing else a
    // receive changes, and capture of a sink whose declaration did not change repeats what it did, so it leaves every
    // other sink (#977).
    const uint32_t touched = i->touched;
    i->touched = 0u;
    for (unsigned k = 0; (touched >> k) != 0u; ++k) {
        if ((touched >> k & 1u) == 0u) {
            continue;
        }
        struct srp_sink *s = &i->sinks[k];
        uint8_t previous = s->desired;
        s->desired = listener_kind(s);
        capture(s,previous);
        // A declaration changed: THE TRANSMIT's call declares and sends it. The walk after the receive compares with
        // this value, so it owes nothing for this change, whatever follows in the MRPDU (#925).
        if (s->desired != previous) {
            hold(i);
        }
    }
    if (type == MSRP_ATTR_TYPE_DOMAIN) {
        const struct msrp_domain *d = value;
        return d->class_id == 6 && d->vid > 0 && d->vid < 4095;
    }
    if (type == MSRP_ATTR_TYPE_LISTENER) {
        return sources_of(i,value) != 0u;
    } else {
        // the bound sinks of the StreamID's lane alone (index_sinks; #977)
        const uint8_t *id = value;
        for (unsigned n = i->lane_first[id[7] % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {
            if (i->sinks[n - 1u].stream_id.bytes[7] == id[7] && same(i->sinks[n - 1u].stream_id.bytes,id,8)) {
                return true;
            }
        }
    }
    // the Domain's and the Listener's above, lwSRP delivers MSRP's Talker types alone here (mrp_pdu.c skips a type its
    // application does not know)
    return keep_talker(i,type,value);
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

// One Listener's Registrar change, copied as the walk copies that Listener's presence (registrations): present while
// it registers (#930). Whether what it registers is Ready is its indication's (listener).
static void listener_moved(struct srp_interface *i, const struct mrp_transition *t)
{
    const uint32_t of = sources_of(i,t->attr_val);
    for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
        if ((of >> n & 1u) != 0u) {
            i->listener_present[n] = t->reg_to != MRP_REG_STATE_MT;
        }
    }
}

// lwSRP reports every Applicant or Registrar state change of a participant
// here.
// The walk copies whether each MSRP Talker and Listener registers and what it registers. Each change of that comes
// with an indication: every Registrar change into or out of MT (IEEE 802.1Q-2018 Table 10-4) and, in lwSRP, a value
// changed while it registers. A Talker's indication marks the walk owed (talker_changed) and a Listener's copies its
// declaration (listener), so a Registrar change owes no walk; a Listener's is copied here for its presence (#930).
// mrp_reclaim frees an attribute whose Registrar is MT and whose Applicant observes or has left (VO, AO, QO), and lwSRP
// reports every change of either state here, the one exception an attribute's creation, at VO and MT (mrp_mad.c,
// get_or_create_attr): a change into such a state owes the reclaim, and one out of creation's is counted, so a receive
// tells the attributes it created and left there (apply_receive). Any other change leaves nothing mrp_reclaim frees, and
// owes no walk of the participant's attributes (#665's ruling of 2026-11-20, item 3).
// An Applicant that moves may request a transmit (Table 10-3 note 6), owed now when its participant's join timer is
// idle: a build arms that timer, so this owes a participant one pass a JoinTime, and one that moves in the build that
// sent it owes nothing past that pass, whose end clears its interface. A function of its own, both participants'
// observers calling it, as the split link script's hot list places it (plat/ctrl_split_hot.txt).
// The Applicant states mrp_reclaim frees an attribute in, a bit each: it observes or has left, declaring nothing.
#define SRP_FREED_APPL ((1u << MRP_APPL_STATE_VO) | (1u << MRP_APPL_STATE_AO) | (1u << MRP_APPL_STATE_QO))
_Static_assert(MRP_APPL_STATE_COUNT <= 32u, "SRP_FREED_APPL holds a bit for each Applicant state");
static CTRL_CC_NOINLINE void moved(struct srp_interface *i, unsigned slot, const struct mrp_transition *t)
{
    struct srp_mbx *m = i->owner;
    if (t->reg_to == MRP_REG_STATE_MT && (SRP_FREED_APPL >> t->appl_to & 1u) != 0u) {
        i->reclaim = true;
    }
    if (t->appl_from == MRP_APPL_STATE_VO && t->reg_from == MRP_REG_STATE_MT) {
        ++i->fresh;
    }
    i->moved = true;
    if (slot == 0u && t->attr_type == MSRP_ATTR_TYPE_LISTENER && t->reg_from != t->reg_to) {
        listener_moved(i,t);
    }
    if (t->appl_from != t->appl_to && m->join_left[2u * i->index + slot] == 0u) {
        m->tx_due |= (uint8_t)(1u << i->index);
    }
}

static void moved_msrp(void *ctx, const struct mrp_transition *t)
{
    moved(ctx, 0u, t);
}

static void moved_mvrp(void *ctx, const struct mrp_transition *t)
{
    moved(ctx, 1u, t);
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
    mrp_set_observer(i->msrp,moved_msrp,i);
    mrp_set_observer(i->mvrp,moved_mvrp,i);
    i->stale = true;
    i->reclaim = true;
    // These valid constants are installed before creating any attribute.
    (void)mrp_port_configure(i->msrp,0,SRP_JOIN_CS,500,SRP_LEAVEALL_CS,(uint32_t)i->mac,true);
    (void)mrp_port_configure(i->mvrp,0,SRP_JOIN_CS,500,SRP_LEAVEALL_CS,(uint32_t)i->mac ^ 0x91u,true);
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
    return declare_sources(i,SRP_DECLARE_NEW);
}

static bool open_interface(struct srp_interface *i)
{
    if (create_participants(i)) {
        // its declarations are owed: THE TRANSMIT builds them
        hold(i);
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
        // a composition with no MAAP DA gate declares every source from creation (#895, srp_mbx_gate)
        i->gate = config->sources_valid ? (1u << CTRL_SRP_SOURCES) - 1u : 0u;
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
        l->drain_charge = NULL;
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
                // the StreamID's latest Talker registration, which every binding of it holds (#925, talker_changed)
                replacement.latest_kind = r->latest_kind;
                replacement.stream_kinds = r->stream_kinds;
            }
            if (r->vid == vid) {
                replacement.vlan_requested |= r->vlan_requested;
                replacement.vlan_sent |= r->vlan_sent;
            }
        }
        // A StreamID none binds, held: the binding takes its latest (#925, #969), and the walk it owes its kinds
        struct srp_held *h = held_stream(m,interface,identity->bytes);
        if (h != NULL) {
            replacement.latest_kind = h->latest_kind;
            replacement.stream_kinds = 3u;
            release_held(m,h);
        }
    }
    const struct srp_sink old = *s;
    *s = replacement;
    i->stale = true; // snapshot matches registrations against the bindings (#665)
    index_sinks(i); // the lookups' index of the bindings, this one among them (#977)
    // and the next receive counts the kept Talkers again: a binding made now takes its StreamID's, an unbinding keeps
    // them (#969, count_kept)
    m->kept_due[interface] |= SRP_KEPT_BOUND;
    if (old.bound) {
        // Judge the complete new binding set, including the replacement.
        // a declaration withdrawn here is sent by THE TRANSMIT's call
        if (!has_sink(i,&old,true)) {
            (void)msrp_withdraw_listener(i->msrp,0,&old.stream_id);
            if (old.declared != 0u) {
                hold(i);
            }
            // The last binding of a StreamID whose kinds are both registered: the StreamID holds its latest until
            // either leaves, so a later binding takes it (#925). The pool bounds the StreamIDs held (srp_held), so the
            // table does not fill.
            if (old.stream_kinds == 3u && m->held_count < SRP_HELD_STREAMS) {
                m->held[m->held_count++] = (struct srp_held){old.stream_id,(uint8_t)interface,old.latest_kind};
                octet_add(m->held_octets,old.stream_id.bytes[7]);
            }
        }
        if (old.vid != i->domain.vid && !has_sink(i,&old,false)) {
            (void)mvrp_withdraw(i->mvrp,0,old.vid);
            if (old.vlan_requested) {
                hold(i);
            }
        }
    }
    m->busy = false;
    return true;
}

bool srp_mbx_gate(struct srp_mbx *m, unsigned interface, uint32_t valid, uint64_t base)
{
    if (!enter(m)) {
        return false;
    }
    const bool ok = m->loop != NULL && interface < MBX_N_IF;
    if (ok) {
        struct srp_interface *i = &m->ifs[interface];
        // CTRL_SRP_SOURCES is at most MBX_N_PUB_SOURCES, under 32: a bit past the sources is no source
        valid &= (1u << CTRL_SRP_SOURCES) - 1u;
        // the gate and base of its last call: each valid source already holds base + n, so nothing changes (#895)
        if (i->gate_seen && valid == i->gate && base == i->gate_base) {
            m->busy = false;
            return true;
        }
        i->gate_seen = true;
        i->gate_base = base;
        bool changed = valid != i->gate;
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
            if ((valid >> n & 1u) == 0u) {
                continue;
            }
            // a valid source's destination, base + n: one that differs from the last declared changes the FirstValue
            struct srp_source *s = &i->sources[n];
            uint64_t dest = base + n;
            bool moved = !s->allocated;
            for (unsigned b = 6u; b-- != 0u; dest >>= 8) {
                moved = moved || s->value.dest_mac[b] != (uint8_t)dest;
                s->value.dest_mac[b] = (uint8_t)dest;
            }
            if (moved) {
                s->allocated = true;
                i->readdressed |= 1u << n;
                changed = true;
            }
        }
        if (changed) {
            i->gate = valid;
            i->sources_owed = true;
            hold(i);
        }
    }
    m->busy = false;
    return ok;
}

// Older output, and the events posted before the record: THE DRAIN's order (ctrl_loop.h) keeps the ring's
// position against the events a pass took, so an event posted after a record holds it back no more. And a build whose
// declarations were made in a slice of their own (transmit, CTRL_LOOP_DECLARE_ALONE): no record comes between them and
// their MRPDU, as none comes between them in one pass given whole (#977).
static bool rx_order_ready(struct srp_mbx *m)
{
    return m->owed_len == 0 && m->loop->ticks_owed == 0 && !m->declared_alone;
}

// THE DRAIN's charge of the record at the head of SRP's ring (ctrl_loop.h, THE TIERS; #977, its ruling of 2026-11-23,
// item 4): the unit, and a Talker registration's stated cost for each Talker value it can carry that can register, a
// bound read from the record before lwSRP parses it and never under that count. Only an MSRP record carries a Talker.
// Its Messages are read by their headers (IEEE 802.1Q-2018 10.8.1.2, 35.2.2.4: AttributeType, AttributeLength and
// AttributeListLength, which bounds each, as lwSRP's parser takes it), each Talker Message's vectors by their
// VectorHeader's NumberOfValues, and every other Message is skipped by its length. Only a VectorHeader of 0 ends a
// Message's vectors (10.8.1.2): a vector of no values, a LeaveAll's, skips its header and its FirstValue and the walk
// goes on (10.8.2.8), as lwSRP's parser does. The receive filter takes a Talker value only for a bound sink's StreamID
// or a kept one, at most V of them (interested_msrp, keep_talker, SRP_RECORD_VALUES), and a vector's values are
// distinct StreamIDs (35.2.2.8.4, an overflowing increment refused), so a vector registers at most V. A PDU lwSRP
// refuses registers none. Past SRP_CHARGE_MESSAGES Messages the rest of the record is charged by its length, V for
// each SRP_TALKER_VECTOR_MIN octets, the least a vector that holds a Talker value takes, so the read is bounded and
// the count is never under (#977, its ruling of 2026-11-27 on the population bound, items 2 and 4). A shape whose
// registration cost is 0 charges the unit.
#define SRP_RECORD_HEAD (14u + 1u) // the Ethernet header and the ProtocolVersion: the first Message's offset
#define SRP_TALKER_VECTOR_MIN (2u + 25u + 1u) // a VectorHeader, a Talker Advertise's FirstValue, one ThreeEvents
#define SRP_CHARGE_MESSAGES 8u // a Message a type and some repeated before the rest is charged by its length
static CTRL_CC_INLINE unsigned peek16(unsigned at)
{
    return (unsigned)mbx_rx_next_byte(MBX_CH_SRP,at) << 8 | mbx_rx_next_byte(MBX_CH_SRP,at + 1u);
}

static unsigned rx_charge(void *ctx)
{
    (void)ctx;
    const unsigned len = mbx_rx_next_len(MBX_CH_SRP);
    unsigned values = 0u;
    if (len > SRP_RECORD_HEAD && peek16(12u) == MRP_ETHERTYPE_MSRP) {
        unsigned at = SRP_RECORD_HEAD;
        for (unsigned messages = 0u; at + 4u <= len; ++messages) {
            if (messages == SRP_CHARGE_MESSAGES) {
                values += SRP_RECORD_VALUES * ((len - at) / SRP_TALKER_VECTOR_MIN);
                break;
            }
            const unsigned type = mbx_rx_next_byte(MBX_CH_SRP,at);
            const unsigned alen = mbx_rx_next_byte(MBX_CH_SRP,at + 1u);
            if ((type | alen) == 0u) {
                break; // the PDU's EndMark: lwSRP parses nothing past it (10.8.1.2)
            }
            const unsigned list = peek16(at + 2u);
            at += 4u;
            const unsigned end = list > len - at ? len : at + list;
            while ((type == MSRP_ATTR_TYPE_TALKER_ADV || type == MSRP_ATTR_TYPE_TALKER_FAILED) && at + 2u <= end) {
                const unsigned header = peek16(at);
                if (header == 0u) {
                    break; // the Message's EndMark
                }
                const unsigned count = mrp_vh_nv((uint16_t)header);
                values += count < SRP_RECORD_VALUES ? count : SRP_RECORD_VALUES;
                at += 2u + alen + (count + 2u) / 3u;
            }
            at = end;
        }
    }
    return CTRL_LOOP_SRP_UNIT_US + CTRL_LOOP_SRP_REG_US * values;
}

static bool rx_ready(void *ctx)
{
    struct srp_mbx *m = ctx;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        if (m->ifs[n].reopening) {
            return false;
        }
    }
    return m->pending_rx.len == 0 && rx_order_ready(m) && mbx_rx_waiting(MBX_CH_SRP,m->loop->rx_order);
}

// The blocks the pool can still give an attribute: lwSRP's attribute is over the small class's 64 bytes, so it takes a
// medium or a large block, the pool's second and third classes, carved from srp_pool_classes smallest first
// (ctrl_pool_init) (#665's ruling of 2026-11-20, item 3).
static CTRL_CC_INLINE unsigned attribute_room(const struct ctrl_pool *pool)
{
    return (unsigned)pool->bins[1].free_count + pool->bins[2].free_count;
}

// The Applicant states of an attribute the participant does not declare (IEEE 802.1Q-2018 Table 10-3): it observes
// (VO, AO, QO) or answers a Leave or LeaveAll with what its Registrar holds (LO), a bit each.
#define SRP_UNDECLARED_APPL (SRP_FREED_APPL | (1u << MRP_APPL_STATE_LO))

// Whether a binding of the interface holds the StreamID at id.
static bool bound_stream(const struct srp_interface *i, const uint8_t *id)
{
    // the bound sinks of the StreamID's lane alone (index_sinks; #977)
    for (unsigned n = i->lane_first[id[7] % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {
        if (same(i->sinks[n - 1u].stream_id.bytes,id,8)) {
            return true;
        }
    }
    return false;
}

// One attribute of the count (#969, count_kept): a Talker the participant does not declare, whose StreamID none of
// the interface's bindings holds, registered or left with its block not yet freed (mrp_reclaim frees it), is kept. One
// left (its Registrar MT) leaves the count pending until a count after its block's return.
static void kept_visited(void *ctx, const struct mrp_attr_status *status)
{
    struct srp_interface *i = ctx;
    struct srp_mbx *m = i->owner;
    const uint8_t *id = ((const struct msrp_talker_adv *)status->attr_val)->stream_id.bytes;
    if ((status->attr_type == MSRP_ATTR_TYPE_TALKER_ADV || status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED) &&
        (SRP_UNDECLARED_APPL >> status->appl & 1u) != 0u && !bound_stream(i,id)) {
        uint8_t *count = &m->kept_count[i->index];
        if (*count < SRP_KEPT_TALKERS) {
            struct srp_kept *kept = &m->kept[i->index][*count];
            copy_id(kept->stream_id.bytes,id);
            octet_add(m->kept_octets[i->index],id[7]);
            kept->kind = talker_kind(status->attr_type);
        }
        ++*count;
        if (status->reg == MRP_REG_STATE_MT) {
            m->kept_due[i->index] |= SRP_KEPT_PENDING;
        }
    }
}

// The interface's kept Talker attributes counted and listed again from its participant, before a receive and outside
// lwSRP's callbacks (#969, keep_talker), whenever the count may hold one no longer kept: a binding changed
// (srp_mbx_bind), or one counted or kept since may have ended and a block was returned since the count. A kept
// attribute ends only when mrp_reclaim frees it, a return, after its Registrar left IN, an indication
// (talker_changed), or after a creation with no registration (keep_talker); and when a reset destroys the
// participants, which zeroes the count with them (reset_interface). So the count a receive starts from is exactly the
// kept attributes its participant holds, and a receive refuses a Talker only at that occupancy, past which the fixed
// blocks fund no more (srp_mbx.h). While nothing is pending a block returned owes no count, so the kept at their bound
// cost a receive nothing more.
static void count_kept(struct srp_interface *i)
{
    struct srp_mbx *m = i->owner;
    const unsigned n = i->index;
    const unsigned due = m->kept_due[n];
    if ((due & SRP_KEPT_BOUND) != 0u || ((due & SRP_KEPT_PENDING) != 0u && m->kept_returned[n] != ctrl_pool_returned)) {
        m->kept_due[n] = 0u;
        m->kept_returned[n] = ctrl_pool_returned;
        m->kept_count[n] = 0u;
        memset(m->kept_octets[n],0,sizeof(m->kept_octets[n]));
        (void)mrp_attr_visit(i->msrp,0,kept_visited,i);
    }
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
        count_kept(i);
    }
    // A received attribute can be created with no state change (#665), at VO and MT, which mrp_reclaim frees: the
    // receive owes the reclaim when it created more attributes than left that state (moved). lwSRP takes a medium or a
    // large block for each attribute it creates, and a small one for each map work, a larger one only once the small
    // class is spent; it frees an attribute only in mrp_reclaim and destroy, and a map work in the event that took it,
    // an end station's map_join and map_leave propagating to no port (mrp_mad.c: map_reserve, map_publish). So the
    // room for attributes mrp_rx takes is the attributes it created, and a map work in a larger block owes a reclaim
    // it need not (#665's ruling of 2026-11-20, item 3).
    const struct ctrl_pool *pool = shlan_port_pool();
    const unsigned room = attribute_room(pool);
    i->fresh = 0u;
    int result = app ? mrp_rx(app,0,frame->bytes + 14,frame->len - 14u) : -SHLAN_ERROR_NO_MEMORY;
    if (room > attribute_room(pool) + i->fresh) {
        i->reclaim = true;
    }
    if (i->msrp) {
        // Include the last event, also when an earlier event applied before
        // allocation refusal. Identical receive retries remain idempotent.
        snapshot(i);
    }
    if (result == -SHLAN_ERROR_NO_MEMORY) {
        ++m->refused;
        // What the refusal saw, after every change of its own (poll).
        i->moved = false;
        m->pending_freed = ctrl_pool_returned;
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
        const uint32_t of = sources_of(i,v);
        for (unsigned n = 0; n < CTRL_SRP_SOURCES; ++n) {
            if ((of >> n & 1u) != 0u) {
                // One value per StreamID; Ignore occupies no registrar (35.2.2.7.2).
                i->listener_present[n] = true;
                i->registered[n] = v[8] == 2 || v[8] == 3;
            }
        }
    } else if (status->attr_type == MSRP_ATTR_TYPE_TALKER_ADV ||
               status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED) {
        const struct msrp_talker_adv *v = status->attr_val;
        const uint8_t last = v->stream_id.bytes[7];
        // the bound sinks of the StreamID's lane alone (index_sinks; #977)
        for (unsigned n = i->lane_first[last % SRP_SINK_LANES]; n != 0u; n = i->lane_next[n - 1u]) {
            struct srp_sink *sink = &i->sinks[n - 1u];
            if (sink->stream_id.bytes[7] == last && same(sink->stream_id.bytes,v->stream_id.bytes,8)) {
                // the StreamID's, whatever their destination and VID: a final unbinding with both holds the latest
                // (#925, srp_mbx_bind)
                sink->stream_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;
                if (same(sink->dest_mac,v->dest_mac,6) && sink->vid == v->vlan_id) {
                    // the declaration follows from both kinds once the walk ends (snapshot, listener_kind)
                    sink->registered_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;
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
        // the values held: only each sink's capture runs (#665), with its
        // declaration unchanged, so only its copy of a continuing kind
        // (capture, with previous the declaration; #665's ruling of
        // 2026-11-20, item 3).
        for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
            if (!i->sinks[k].withdrawn && i->sinks[k].desired) {
                i->sinks[k].feedback_kind = i->sinks[k].desired;
            }
        }
        return;
    }
    i->stale = false;
    i->touched = 0u; // the walk below takes every sink again
    ++i->owner->walks;
    memset(i->registered,0,sizeof(i->registered));
    memset(i->listener_present,0,sizeof(i->listener_present));
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        previous[k] = i->sinks[k].desired;
        i->sinks[k].registered_kinds = 0;
        i->sinks[k].stream_kinds = 0;
    }
    (void)mrp_attr_visit(i->msrp,0,registrations,i);
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        i->sinks[k].desired = listener_kind(&i->sinks[k]);
        capture(&i->sinks[k],previous[k]);
        // a binding's declaration changed: THE TRANSMIT's call declares and sends it
        if (i->sinks[k].desired != previous[k]) {
            hold(i);
        }
    }
}

static bool change_domain(struct srp_interface *i)
{
    if (!i->domain_owed) {
        // what a validity change or a hold-off's end owes (#895: srp_mbx_gate, count_held)
        return !i->sources_owed || declare_sources(i,SRP_DECLARE_CHANGED);
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
    (void)declare_sources(i,SRP_DECLARE_EVERY);
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
            ++m->declarations;
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
        // the last byte first, as sources_of: one talker's StreamIDs differ in their unique ID, so a call of memcmp
        // for every pair made the declarations' pass quadratic in the sinks (#977, its ruling of 2026-11-23, item 5)
        for (unsigned other = 0; other < CTRL_SRP_SINKS; ++other) {
            const struct srp_sink *r = &i->sinks[other];
            if (r->bound && r->stream_id.bytes[7] == s->stream_id.bytes[7] &&
                memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {
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
            // A declaration rewrites the value of the attribute a registration shares (#665), which the walk copies
            // only for a source of its StreamID (registrations, sources_of): one of a StreamID no source talks
            // changes nothing the walk copies and owes it none (#977, its ruling of 2026-11-23, item 5).
            i->stale = i->stale || sources_of(i,s->stream_id.bytes) != 0u;
        }
        int result = desired == s->declared ? 0 : desired ? msrp_declare_listener(i->msrp,0,&s->stream_id,desired) :
                               msrp_withdraw_listener(i->msrp,0,&s->stream_id);
        if (result == 0) {
            m->declarations += desired != s->declared;
            for (unsigned other = k; other < CTRL_SRP_SINKS; ++other) {
                struct srp_sink *r = &i->sinks[other];
                if (r->bound && r->stream_id.bytes[7] == s->stream_id.bytes[7] &&
                    memcmp(r->stream_id.bytes,s->stream_id.bytes,8) == 0) {
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
        // the registrar it was walked from, and the Listener it registers, are destroyed below (#665): a registration
        // after the reset is a change of the Listener the source's STREAM_OUTPUT shows, whatever it declares (#957)
        i->declaration[k] = 0u;
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
    m->join_left[2u * i->index] = 0u;
    m->join_left[2u * i->index + 1u] = 0u;
    m->tx_due &= (uint8_t)~(1u << i->index);
    // a build owed after declarations of their own ends with the participants that made them: the new ones declare
    // again, and records are taken again (#977, transmit)
    m->declared_alone = false;
    // a build resuming at one of its participants ends with them: the new ones build whole (THE TIERS)
    m->tx_resume = (m->tx_resume - 1u) / 2u == i->index ? 0u : m->tx_resume;
    for (unsigned k = 0; k < CTRL_SRP_SINKS; ++k) {
        uint8_t previous = i->sinks[k].desired;
        i->sinks[k].desired = 0; i->sinks[k].declared = 0;
        i->sinks[k].registered_kinds = 0;
        i->sinks[k].stream_kinds = 0;
        capture(&i->sinks[k],previous);
        i->sinks[k].vlan_requested = false; i->sinks[k].vlan_sent = false;
    }
    // the registrations a StreamID was held for are destroyed with the participants (#925, srp_held); a later entry
    // moved into the place of one ending has been seen already; and so are the kept Talkers (#969, count_kept)
    for (unsigned n = m->held_count; n-- != 0u;) {
        if (m->held[n].interface == i->index) {
            release_held(m,&m->held[n]);
        }
    }
    m->kept_count[i->index] = 0u;
    memset(m->kept_octets[i->index],0,sizeof(m->kept_octets[i->index]));
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
        } else {
            hold(i);
        }
        i->link_seen = true;
        i->link = event->link_up;
        i->link_carried = event->link_up;
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
static CTRL_CC_NOINLINE void reclaim(struct srp_interface *i)
{
    if (i->reclaim) {
        (void)mrp_reclaim(i->msrp,0);
        (void)mrp_reclaim(i->mvrp,0);
        i->reclaim = i->owner->owed_len != 0u;
    }
}

// One participant's MRPDU: lwSRP's result, with its join timer's shadow (tick) restarted by what it sent.
static CTRL_CC_NOINLINE int build_mrpdu(struct srp_mbx *m, struct srp_interface *i, unsigned slot)
{
    struct send_context send = {i,participant(i,slot)};
    int result = mrp_transmit(send.app,0,m->owed_frame + 14u,sizeof(m->owed_frame) - 14u,send_pdu,&send);
    if (result > 0) {
        m->join_left[slot] = SRP_JOIN_CS;
    }
    return result;
}

// Whether the level `up` the LINK register reads is a carried UP (#973): by the last LINK the loop dispatched (bit 0
// of link_carried), or by none owed. A poll that reads an uncarried UP marks it (bit 1), and a later poll takes it if
// no LINK has come by then and the loop's take in that poll's pass ended on an empty ring (events_left); a LINK's
// level replaces both bits, and a poll that reads a DOWN clears the mark (the mask). Only the loop takes events, and
// the fabric posts a LINK first of its sources once the ring has room (KL_mbx_evt.sv). So a LINK owed at the marking
// poll was posted then, if the ring had room, or else as the next take made room, a take that stops at
// CTRL_LOOP_EVENTS_PER_PASS of the full ring's MBX_EVT_WORDS / MBX_EV_WORDS records; either way a later take that
// empties the ring takes it. A DOWN can elide that UP's record, and the UP after it is owed a LINK of its own, posted
// after takes the mark rests on: so the mark holds only while each poll reads the link up. A DOWN that no poll reads
// ends between two of SRP's polls, and a link the PHY dropped renegotiates for longer (IEEE 802.3-2022 28.3.2,
// break_link_timer). So a re-attach that read a DOWN whose record the fabric then elided, its level back before the
// record posted, follows the link that is up, and an UP after a DOWN is taken from its own LINK.
_Static_assert(CTRL_LOOP_EVENTS_PER_PASS < MBX_EVT_WORDS / MBX_EV_WORDS, "a full event ring outlasts one take");
static bool carried_up(const struct srp_mbx *m, struct srp_interface *i, bool up)
{
    unsigned c = i->link_carried;
    if ((c & 1u) == 0u) {
        c = ((c >> 1 & (m->loop->events_left ? 0u : 1u)) | 2u) & -(unsigned)up;
        i->link_carried = (uint8_t)c;
    }
    return c & up;
}

static bool poll(void *ctx)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return false;
    }
    // Each interface's level in this poll (#973): a DOWN as the LINK register reads it, so a link lost while a full
    // ring holds its LINK record back fails closed at once; an UP only while it is carried (carried_up). The register
    // can rise after the loop took this pass's events, and a reset on that level would make the LINK the next pass
    // dispatches a repeated UP, which resets the interface again (on_event): a first UP would lose the clean startup
    // participants it keeps, and a later one would reset the interface twice.
    bool links[MBX_N_IF];
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        links[n] = carried_up(m, &m->ifs[n], mbx_link_up(n));
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
        // Retry only after lifecycle reconciliation and older output/events, and only once what the refusal depends on
        // changed since it: a block a pool returned (ctrl_pool_returned) or an Applicant or Registrar change of the
        // interface's participants (moved). lwSRP refuses a receive only where an allocation fails (mrp_mad.c:
        // get_or_create_attr and map_reserve under rx_on_attr), and which allocations a replay asks for follows from the
        // filter's answers (interested_msrp, interested_mvrp) and the attributes' existence, values and states. While a
        // receive waits the filter's inputs hold, since no binding changes (srp_mbx_bind) and no declaration or Domain
        // is made (transmit), and the kept Talkers change only with the filter's own answers, which a replay repeats,
        // or with a count, which a block returned owes (#969, count_kept); an attribute
        // is freed only by a block returned and created only by one taken, which leaves
        // no more room; its value changes only by a receive or a declaration, and no other SRP record is taken meanwhile
        // (rx_ready). So a retry with neither changed meets the same refusal: it is not made, and the deadline is checked
        // as that refusal would check it. Even then at most one retry a centisecond (tick), so the retries come at THE
        // TICK's rate, not the passes' (#665).
        if (m->pending_rx.len && m->pending_rx.interface == n && rx_order_ready(m) && !m->loop->events_left) {
            if (!i->moved && ctrl_pool_returned == m->pending_freed) {
                expire_receive(m);
            } else if (!m->retry_spent) {
                m->retry_spent = true;
                if (apply_receive(m,&m->pending_rx)) {
                    m->pending_rx.len = 0;
                } else {
                    expire_receive(m);
                }
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
    // The poll reclaims, so a record the next pass takes finds the room (#665). A rebuild comes no sooner than the
    // poll after a reset's, so this holds that pass's records to their cap (ctrl_loop.h, THE DRAIN).
    bool rebuilds = false;
    for (unsigned n = 0; n < MBX_N_IF; ++n) {
        if (m->ifs[n].msrp) {
            reclaim(&m->ifs[n]);
        } else {
            rebuilds = true;
        }
    }
    m->loop->rx_held = rebuilds;
    // The poll declares nothing and builds no MRPDU: THE TRANSMIT does both, in a
    // pass of its own (ctrl_loop.h). It sends only the frame a build left owed,
    // one a pass and oldest first (A3), and reports what the build owes, so the
    // loop passes on to that pass.
    if (m->owed_len) {
        struct srp_interface *i = &m->ifs[m->owed_if];
        unsigned mvrp = m->owed_ethertype == MRP_ETHERTYPE_MVRP;
        if (i->msrp && i->link && build_mrpdu(m,i,2u * m->owed_if + mvrp) != 0) {
            owed = true;
        }
    }
    owed = owed || m->tx_owed != 0u;
    m->busy = false;
    return owed;
}

// THE TRANSMIT's client (ctrl_loop.h, #665), called in a pass given whole to what an interface owes, a slice of tier 2
// (THE TIERS): every interface's declarations, then both participants' MRPDUs of the first interface that owes one, and
// the next such pass takes the rest; then that interface's declarations again, for what a first VLAN send licensed. A
// slice that cannot hold both MRPDUs makes `most` of them (CTRL_LOOP_BUILD_MOST) and the next slice resumes at the next
// participant, its declarations already made, then makes that interface's declarations: the frames of the build made
// whole, with a slice between two (#894; #665, the decision of 2026-11-09, item 2). The pause takes the interface's due
// and the build stays owed (tx_owed), so what comes due between the two slices, a join timer's end among the
// centiseconds dispatched there, is owed again once the build ends, as after a build made whole (#956). Where a slice
// holds both MRPDUs (CTRL_LOOP_BUILD_MOST 2) a Domain adopted here is sent in this call, so no poll sees its VID
// unlicensed between them. Where it holds one (both points' slices, #894's slice ruling of 2026-11-13) the MVRP MRPDU
// follows in the next slice and polls may run between the two, and the Talker's licence still waits for the MVRP commit
// (vlan_sent; Milan v1.2 4.3.2). No declaration is made while a retained receive waits, so none takes the room it waits
// for. A refused or waiting declaration is tried again when the join count ends, at the JoinTime's rate and not every
// pass given whole, so the passes this client takes stay what THE RETRY's bound counts. A frame the ring refuses stays
// the poll's (A3) and the interface stays due.
static void transmit(void *ctx, unsigned most)
{
    struct srp_mbx *m = ctx;
    if (!enter(m)) {
        return;
    }
    const unsigned resume = m->tx_resume;
    // what came due since the slice the build resumes from, whose pause took its interface's due
    const unsigned again = resume != 0u ? m->tx_due : 0u;
    // the interface the build is of: one interface's always, or the one it resumes, or the first due
    const unsigned first = MBX_N_IF == 1u ? 0u : resume != 0u ? (resume - 1u) / 2u : (m->tx_due & 1u) != 0u ? 0u : 1u;
    const bool declared_alone = m->declared_alone;
    m->declared_alone = false;
    m->declarations = 0u;
    for (unsigned k = resume != 0u ? MBX_N_IF : 0u; k <= MBX_N_IF; ++k) {
        const unsigned n = k < MBX_N_IF ? k : first;
        struct srp_interface *i = &m->ifs[n];
        // Where the slice holds a build and no more (CTRL_LOOP_DECLARE_ALONE), declarations that re-declared a Listener
        // or joined a VLAN took this slice: the MRPDU is built in the next pass given whole, the interface still due,
        // and no record is taken between (rx_order_ready). Once a call: the next builds whatever it declares (#977, its
        // ruling of 2026-11-23, item 3).
        if (k == MBX_N_IF && CTRL_LOOP_DECLARE_ALONE && !declared_alone && m->declarations != 0u) {
            m->declared_alone = true;
            break;
        }
        if (k == MBX_N_IF) {
            m->tx_resume = 0u;
            unsigned built = 0u;
            for (unsigned slot = resume != 0u ? resume - 1u : 2u * n; i->msrp && slot < 2u * n + 2u && !m->owed_len;
                 ++slot) {
                if (built++ == most) {
                    // the reclaim the next participant's build would make, so a record taken between the two slices
                    // finds the room the build whole leaves it (#665, THE TRANSMIT's declarations)
                    reclaim(i);
                    m->tx_resume = (uint8_t)(slot + 1u);
                    break;
                }
                reclaim(i);
                if (i->link) {
                    (void)build_mrpdu(m,i,slot);
                }
            }
            // a frame the ring refused stays the poll's and its interface stays due (A3), the pause's due taken or not
            const unsigned bit = 1u << n;
            m->tx_due = (uint8_t)((m->tx_due & ~bit) | (m->owed_len != 0u ? bit : again));
            if (m->tx_resume != 0u) {
                break;
            }
        }
        if (i->msrp && (m->pending_rx.len != 0u || prepare_declarations(i)) && m->join_left[2u * n] == 0u) {
            m->join_left[2u * n] = SRP_JOIN_CS;
        }
    }
    m->busy = false;
}

// THE TRANSMIT's due: an owed MRPDU, or a build waiting for its next slice, with no frame owed ahead of it, takes a
// pass of its own (ctrl_loop.h).
static bool transmit_aged(void *ctx)
{
    const struct srp_mbx *m = ctx;
    // A tick posted during the preceding ordinary pass must age the old
    // timers before a build arms a new join timer. GM changes may keep the
    // event ring nonempty, so only pending ticks defer this build.
    return m->tx_owed != 0u && !m->owed_len && !m->loop->ticks_owed && !mbx_tick_pending();
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
            m->ifs[n].link_carried = m->ifs[n].link;
        }
        m->loop = loop;
        timer_owner = m;
        (void)ctrl_loop_bind_rx(loop,MBX_CH_SRP,receive,m);
        (void)ctrl_loop_add_sink(loop,on_event,m);
        (void)ctrl_loop_add_tick(loop,tick);
        (void)ctrl_loop_add_poll(loop,poll,m);
        (void)ctrl_loop_set_transmit(loop,transmit,transmit_aged,m);
        ctrl_loop_set_rx_ready(loop,MBX_CH_SRP,rx_ready);
        loop->drain_ch = MBX_CH_SRP + 1u;
        loop->drain_charge = rx_charge;
    }
    m->busy = false;
    return ok;
}

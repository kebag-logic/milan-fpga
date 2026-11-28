// SPDX-License-Identifier: CERN-OHL-W-2.0
// SRP's Listener copies (#930): a Listener's indication copies its declaration and lwSRP's transition observer its
// presence, where lwSRP reports them, and a Registrar change owes no registrar walk. The reference is the walk's
// schedule as #665 left srp_mbx.c: every Listener indication and every Registrar change of either participant owed
// the walk, so the snapshot after it walked the registrar. srp_mbx.c is built for this suite with lwSRP's
// msrp_app_create and mrp_set_observer renamed to the seams below (srp_arms.py), which restore that schedule in the
// reference run and only pass each call on in the copied run. Random record sequences run through both from the same
// seed: every mailbox write and every licence call, in order, and the state the loop, ACMP and THE TRANSMIT read must
// be the same after every step, and each settled step of the copied run holds what a walk of the registrar copies,
// each sink's declaration by the latest Talker registration while both kinds are registered (#925).
// The SRP cut (#665's ruling of 2026-11-20, item 3) has a reference of its own, the adapter as it stood before it:
// every Applicant or Registrar change and every receive owed lwSRP's reclaim, and the receive filter recomputed every
// sink's declaration at every attribute. srp_mbx.c's calls of mrp_rx, mrp_reclaim and mrp_set_rx_filter are renamed
// to seams below as well, which restore that schedule in the reference run. The same random records run through both:
// the same calls, writes and state, the reclaim's flag apart, and after every step each participant's attributes, in
// order, with their states and values, so every reclaim the reference ran that freed an attribute the cut ran too,
// at the same step; and the cut walks the attributes fewer times.
// Run at 1x1/1if and 8x8/1if (test_ctrl_firmware.py).
#include "srp_fixture.hpp"
#include <array>
#include <cstddef>
#include <list>
#include <string>
FW_TALLY_LABEL("ctrl SRP Listener copies");
namespace {
// The run whose Listener indications and Registrar changes owe the walk (the reference).
bool reference_walk = false;
// The run whose every change and receive owe the reclaim and whose filter recomputes every sink (the cut's
// reference), the adapter it runs, and every reclaim walk the firmware made and what each freed.
bool reference_reclaim = false;
srp_mbx *reclaiming = nullptr;
unsigned reclaim_walks = 0;
unsigned reclaim_frees = 0;

srp_interface *owner_of(msrp_ctx *ctx) {
    return reinterpret_cast<srp_interface *>(reinterpret_cast<uint8_t *>(ctx) - offsetof(srp_interface,msrp_ctx));
}
decltype(msrp_ctx::on_listener) adapter_listener;
decltype(msrp_ctx::on_leave) adapter_leave;
void listened(msrp_ctx *ctx, uint8_t port, const msrp_stream_id *id, msrp_listener_decl decl, bool is_new) {
    adapter_listener(ctx,port,id,decl,is_new);
    if(reference_walk) owner_of(ctx)->stale=true;
}
void departed(msrp_ctx *ctx, uint8_t port, uint8_t type, const void *value) {
    adapter_leave(ctx,port,type,value);
    if(reference_walk && type==MSRP_ATTR_TYPE_LISTENER) owner_of(ctx)->stale=true;
}
struct Observer {
    void (*fn)(void *, const mrp_transition *);
    void *ctx;
};
std::list<Observer> observers;
void observed(void *ctx, const mrp_transition *t) {
    const auto *o=static_cast<const Observer *>(ctx);
    o->fn(o->ctx,t);
    if(reference_walk && t->reg_from!=t->reg_to) static_cast<srp_interface *>(o->ctx)->stale=true;
    if(reference_reclaim) static_cast<srp_interface *>(o->ctx)->reclaim=true;
}
struct Filter {
    mrp_rx_filter_fn fn;
    void *ctx;
};
std::list<Filter> filters;
// The reference's filter recomputes every sink, as a stale interface's did before the filter took only the sinks an
// indication touched (#977), and leaves the walk's mark as it found it.
bool filtered(void *ctx, uint8_t port, uint8_t type, const void *value) {
    const auto *f=static_cast<const Filter *>(ctx);
    auto *i=static_cast<srp_interface *>(f->ctx);
    const bool stale=i->stale;
    if(reference_reclaim) {
        i->stale=true;
        i->touched=(1u<<CTRL_SRP_SINKS)-1u;
    }
    const bool interested=f->fn(f->ctx,port,type,value);
    i->stale=stale;
    return interested;
}
} // namespace

// srp_mbx.c's calls of lwSRP's msrp_app_create and mrp_set_observer, renamed to these for this suite (srp_arms.py).
extern "C" mrp_app *srp_test_msrp_app_create(uint8_t n_ports, msrp_ctx *ctx) {
    adapter_listener=ctx->on_listener; ctx->on_listener=listened;
    adapter_leave=ctx->on_leave; ctx->on_leave=departed;
    return msrp_app_create(n_ports,ctx);
}
extern "C" void srp_test_set_observer(mrp_app *app, void (*fn)(void *, const mrp_transition *), void *ctx) {
    observers.push_back({fn,ctx});
    mrp_set_observer(app,observed,&observers.back());
}
// srp_mbx.c's calls of mrp_rx, mrp_reclaim and mrp_set_rx_filter, renamed to these for this suite (srp_arms.py).
extern "C" int srp_test_mrp_rx(mrp_app *app, uint8_t port, const uint8_t *pdu, size_t len) {
    const int result=mrp_rx(app,port,pdu,len);
    if(reference_reclaim && reclaiming) {
        for(auto &i:reclaiming->ifs) if(i.msrp==app || i.mvrp==app) i.reclaim=true;
    }
    return result;
}
extern "C" unsigned srp_test_mrp_reclaim(mrp_app *app, uint8_t port) {
    const unsigned freed=mrp_reclaim(app,port);
    ++reclaim_walks;
    reclaim_frees+=freed;
    return freed;
}
extern "C" void srp_test_set_rx_filter(mrp_app *app, mrp_rx_filter_fn fn, void *ctx) {
    filters.push_back({fn,ctx});
    mrp_set_rx_filter(app,filtered,&filters.back());
}

namespace {
using Step = std::vector<uint64_t>;
enum Kind : uint64_t { WRITE, LICENCE, RECORD, FRAME, STATE };

// What a walk of the registrar copies (registrations()'s rules), against what the interface holds.
bool holds_walk(const srp_interface &i) {
    struct Walked {
        const srp_interface *i;
        bool present[CTRL_SRP_SOURCES];
        bool registered[CTRL_SRP_SOURCES];
        uint8_t kinds[CTRL_SRP_SINKS];
    } w{&i,{},{},{}};
    mrp_attr_visit(i.msrp,0,[](void *p,const mrp_attr_status *s) {
        auto &c=*static_cast<Walked *>(p);
        const auto *v=static_cast<const uint8_t *>(s->attr_val);
        if(s->reg==MRP_REG_STATE_MT) return;
        if(s->attr_type==MSRP_ATTR_TYPE_LISTENER) {
            for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) if(!std::memcmp(c.i->sources[n].value.stream_id.bytes,v,8)) {
                c.present[n]=true; c.registered[n]=v[8]==2 || v[8]==3;
            }
        } else if(s->attr_type==MSRP_ATTR_TYPE_TALKER_ADV || s->attr_type==MSRP_ATTR_TYPE_TALKER_FAILED) {
            const auto *t=static_cast<const msrp_talker_adv *>(s->attr_val);
            for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
                const auto &sink=c.i->sinks[k];
                if(sink.bound && !std::memcmp(sink.stream_id.bytes,t->stream_id.bytes,8) &&
                   !std::memcmp(sink.dest_mac,t->dest_mac,6) && sink.vid==t->vlan_id)
                    c.kinds[k]|=s->attr_type==MSRP_ATTR_TYPE_TALKER_FAILED ? 1 : 2;
            }
        }
    },&w);
    for(unsigned n=0;n<CTRL_SRP_SOURCES;++n)
        if(w.present[n]!=i.listener_present[n] || w.registered[n]!=i.registered[n]) return false;
    for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
        if(w.kinds[k]!=i.sinks[k].registered_kinds) return false;
        // the declaration the walked kinds ask for, the latest registered deciding while both are (#925)
        const uint8_t latest=i.sinks[k].latest_kind, kinds=(w.kinds[k]&latest) ? latest : w.kinds[k];
        if(i.sinks[k].desired!=((kinds&1) ? 1 : kinds)) return false;
    }
    return true;
}

// Where two steps first differ: the entry's index, kind and both values.
std::string first_difference(const Step &a, const Step &b) {
    size_t k=0;
    while(k<a.size() && k<b.size() && a[k]==b[k]) ++k;
    const auto at=[](const Step &s,size_t k) { return k<s.size() ? std::to_string(s[k]) : std::string("end"); };
    return "entry "+std::to_string(k)+" of "+std::to_string(a.size())+" and "+std::to_string(b.size())+
           ": reference "+at(a,k)+", copied "+at(b,k)+" (the two before: "+(k>1 ? at(a,k-2) : "")+" "+
           (k>0 ? at(a,k-1) : "")+")";
}

class Listeners : public Srp {
protected:
    std::vector<Step> steps;      // a run's steps, each its mailbox writes and licence calls, then its state
    std::vector<std::string> said; // what each step did
    uint32_t x=0;
    uint32_t framed=0;
    unsigned licensed=0;
    unsigned present=0;
    unsigned walks=0;
    // The differential against the cut's reference: its state holds the participants' attributes, not the flag.
    bool reclaim_mode=false;
    unsigned walked=0;
    unsigned freed=0;

    // Each participant's attributes, newest first, with their states and whole stored values (mrp_attr_visit; lwSRP
    // stores each in 48 bytes, cleared at its creation).
    static void attributes(Step &s, const mrp_app *app) {
        s.push_back(mrp_attr_visit(app,0,[](void *p,const mrp_attr_status *a) {
            auto &into=*static_cast<Step *>(p);
            const auto *v=static_cast<const uint8_t *>(a->attr_val);
            into.insert(into.end(),{a->attr_type,uint64_t(a->appl),uint64_t(a->reg)});
            into.insert(into.end(),v,v+48);
        },&s));
    }

    // Every write but those of the SRP transmit ring, whose records carry the driver's commit count since its start
    // (mbx_contract.h, TX record word 1), which the second run starts later: the frames are the model's (state).
    static void written(void *ctx, bool write, uint32_t off, uint32_t value) {
        if(write && (off<MBX_CH_SRP_TX_BASE || off>=MBX_CH_SRP_TX_BASE+4u*MBX_CH_SRP_TX_WORDS))
            static_cast<Listeners *>(ctx)->steps.back().insert(
                static_cast<Listeners *>(ctx)->steps.back().end(),{WRITE,off,value});
    }
    static void licence_call(void *ctx, unsigned interface, unsigned source, bool active) {
        static_cast<Listeners *>(ctx)->steps.back().insert(
            static_cast<Listeners *>(ctx)->steps.back().end(),{LICENCE,interface,source,active});
    }
    // Most sources admitted, every third declared Talker Failed: several licences can open at once.
    void SetUp() override {
        reclaiming=&adapter;
        Srp::SetUp();
        srp_mbx_destroy(&adapter);
        for(unsigned i=0;i<MBX_N_IF;++i) for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) sources[i][n].allocated=n%3u!=2u;
        config.licence=licence_call; config.ctx=this;
        ASSERT_TRUE(srp_mbx_init(&adapter,&config));
        ASSERT_TRUE(srp_mbx_attach(&adapter,&loop));
        steps.assign(1,Step{});
        mbx_host_trace(written,this);
    }
    void TearDown() override {
        mbx_host_trace(nullptr,nullptr);
        Srp::TearDown();
        reclaiming=nullptr;
    }
    // A second run on a fresh adapter, model, loop and pool.
    void again() {
        TearDown();
        model=mbx_model{}; loop=ctrl_loop{}; pool=ctrl_pool{}; adapter=srp_mbx{};
        SetUp();
    }
    uint32_t next() { x^=x<<13; x^=x>>17; x^=x<<5; return x; }
    unsigned below(unsigned n) { return next()%n; }

    // A Listener Message of `count` values from the StreamID of source `first` on, a source past the last one's
    // StreamID being no source's (35.2.2.8.2: the FirstValue's unique ID incremented), each its own event and
    // declaration, after a LeaveAll when `la`.
    std::vector<uint8_t> listeners(unsigned first, unsigned count, const unsigned *events, const unsigned *subtypes,
                                   bool la) {
        auto sid=identity(0,0);
        wire_put_be(sid.data()+6,wire_be16(sid.data()+6)+first,2);
        auto f=frame(3,sid,events[0],subtypes[0],la);
        if(count==1) return f;
        auto *p=f.data()+14;
        const unsigned list=2+8+1+1+2;
        wire_put_be(p+3,list,2); wire_put_be(p+5,(la ? 0x2000 : 0)+count,2);
        p[15]=uint8_t(events[0]*36+events[1]*6); p[16]=uint8_t(subtypes[0]<<6 | subtypes[1]<<4);
        return f;
    }
    std::vector<uint8_t> talker(unsigned which, unsigned event, bool failed, bool other_dest, bool la) {
        msrp_stream_id sid{{2,1,2,3,4,5,6,uint8_t(7+which)}};
        if(which==2) std::copy_n(sources[0][0].value.stream_id.bytes,8,sid.bytes);
        std::vector<uint8_t> v(25);
        std::copy_n(sid.bytes,8,v.begin());
        const std::array<uint8_t,6> da{0x91,0xe0,0xf0,0,0,uint8_t(other_dest ? 10 : 9)};
        std::copy_n(which==2 ? sources[0][0].value.dest_mac : da.data(),6,v.begin()+8);
        wire_put_be(v.data()+14,2,2); wire_put_be(v.data()+16,224,2); wire_put_be(v.data()+18,1,2); v[20]=0x60;
        if(failed) { v.resize(34); v[33]=1; }
        return frame(failed ? 2 : 1,v,event,0,la);
    }
    std::vector<uint8_t> vlan(uint16_t vid, unsigned event, bool la) {
        std::vector<uint8_t> f(26);
        wire_put_be(f.data(),0x0180c2000021ull,6); wire_put_be(f.data()+6,0x020304000009ull,6);
        wire_put_be(f.data()+12,0x88f5,2);
        const uint8_t pdu[]={0,1,2,uint8_t(la ? 0x20 : 0),1,uint8_t(vid>>8),uint8_t(vid),uint8_t(event*36),0,0,0,0};
        std::copy(pdu,pdu+12,f.begin()+14);
        return f;
    }
    // A record the fabric's limiter may drop (mailbox.yaml `rate`), taken with no poll after it or settled.
    void record(const std::vector<uint8_t> &f, bool unpolled) {
        steps.back().insert(steps.back().end(),{RECORD,mbx_model_rx(&model,f.data(),f.size(),0)});
        if(unpolled) {
            const unsigned polls=loop.n_polls;
            loop.n_polls=0; ctrl_loop_service(&loop); loop.n_polls=polls;
        } else {
            settle();
        }
    }
    void record(const std::vector<uint8_t> &f) {
        record(f,below(3)==0);
    }
    // One random step: a record of each kind the adapter takes, a binding, time, a link change or a refusal.
    void step() {
        const unsigned r=below(100);
        const bool la=below(10)==0;
        if(r<36) {
            const unsigned first=below(CTRL_SRP_SOURCES+1u);   // CTRL_SRP_SOURCES: a StreamID no source has
            const unsigned count=first+1u<CTRL_SRP_SOURCES && below(3)==0 ? 2u : 1u;
            const unsigned events[2]={below(6),below(6)};
            const unsigned subtypes[2]={below(4),below(4)};
            said.back()="Listener "+std::to_string(first)+" x"+std::to_string(count)+" event "+
                        std::to_string(events[0])+" declaration "+std::to_string(subtypes[0])+(la ? " LeaveAll" : "");
            record(listeners(first,count,events,subtypes,la));
        } else if(r<50) {
            const unsigned which=below(3);
            const unsigned event=below(6);
            const bool failed=below(3)==0;
            const bool other=below(4)==0;
            said.back()="Talker "+std::to_string(which)+(failed ? " Failed" : " Advertise")+" event "+
                        std::to_string(event)+(other ? " other destination" : "")+(la ? " LeaveAll" : "");
            record(talker(which,event,failed,other,la));
        } else if(r<55) {
            const unsigned event=below(6);
            const uint8_t vid=below(4)==0 ? 5 : 2;
            said.back()="Domain VID "+std::to_string(vid)+" event "+std::to_string(event);
            record(frame(4,{6,3,0,vid},event,0,la));
        } else if(r<60) {
            const unsigned event=below(6);
            const uint16_t vid=below(2) ? 2 : 9;
            said.back()="MVRP VID "+std::to_string(vid)+" event "+std::to_string(event);
            record(vlan(vid,event,la));
        } else if(r<68) {
            const unsigned k=below(CTRL_SRP_SINKS);
            const unsigned which=below(4);
            said.back()="bind sink "+std::to_string(k)+" to "+std::to_string(which);
            msrp_stream_id sid{{2,1,2,3,4,5,6,uint8_t(7+which)}};
            const std::array<uint8_t,6> da{0x91,0xe0,0xf0,0,0,9};
            if(which==2) std::copy_n(sources[0][0].value.stream_id.bytes,8,sid.bytes);
            const uint8_t *dest=which==2 ? sources[0][0].value.dest_mac : da.data();
            (void)srp_mbx_bind(&adapter,0,k,which==3 ? nullptr : &sid,which==3 ? nullptr : dest,which==3 ? 0 : 2);
            settle();
        } else if(r<88) {
            const unsigned u=below(50);
            const unsigned ms=u<40 ? 1+below(40) : u<46 ? 210 : u<49 ? 1000 : 5100;
            said.back()="advance "+std::to_string(ms)+" ms";
            advance(ms);
        } else if(r<91) {
            said.back()="link down and up";
            mbx_model_set_link(&model,0,false); settle();
            if(below(2)) advance(1+below(30));
            mbx_model_set_link(&model,0,true); settle();
        } else if(r<96) {
            const int left=int(below(3));
            const unsigned first=below(CTRL_SRP_SOURCES);
            const unsigned events[2]={1,1};
            const unsigned subtypes[2]={2,1};
            said.back()="refusal after "+std::to_string(left)+" blocks, Listener "+std::to_string(first);
            calloc_before_failure=left;
            record(listeners(first,1,events,subtypes,false),true);
            calloc_before_failure=-1;
            settle();
        } else {
            said.back()="settle";
            settle();
        }
    }
    // The state the loop, ACMP's delivery and THE TRANSMIT read, appended to the step's calls.
    void state() {
        auto &s=steps.back();
        for(;framed<model.tx_sent;++framed) {
            const auto *f=mbx_model_tx_frame(&model,framed);
            s.insert(s.end(),{FRAME,framed,f!=nullptr});
            if(f) {
                s.insert(s.end(),{f->len,f->interface,f->channel,f->now_ms});
                s.insert(s.end(),f->bytes,f->bytes+f->len);
            }
        }
        s.push_back(STATE);
        for(unsigned i=0;i<MBX_N_IF;++i) {
            const auto &f=adapter.ifs[i];
            for(unsigned n=0;n<CTRL_SRP_SOURCES;++n) {
                s.insert(s.end(),{f.registered[n],f.listener_present[n],f.active[n],f.stop_owed[n],f.admitted[n]});
                licensed+=f.active[n]; present+=f.listener_present[n];
            }
            for(unsigned k=0;k<CTRL_SRP_SINKS;++k) {
                const auto &q=f.sinks[k];
                s.insert(s.end(),{q.bound,q.desired,q.declared,q.registered_kinds,q.feedback_kind,q.withdrawn,
                                  q.vlan_requested,q.vlan_sent});
            }
            // against the cut's reference the reclaim's flag differs by design: what it frees is compared instead
            s.insert(s.end(),{f.link,f.vlan_sent,f.domain.vid,f.talkers,reclaim_mode ? 0u : f.reclaim,f.moved,
                              f.msrp!=nullptr});
            if(reclaim_mode && f.msrp) {
                attributes(s,f.msrp);
                attributes(s,f.mvrp);
            }
        }
        s.insert(s.end(),{adapter.tx_due,adapter.refused,adapter.malformed,adapter.received,adapter.transmitted,
                          adapter.stops,adapter.rx_discarded,adapter.pending_rx.len,adapter.owed_len,
                          ctrl_pool_in_use(&pool),model.tx_sent,model.now_ms});
    }
    // One run of `count` steps from `seed`; the copied run's settled steps also hold what a walk copies.
    std::vector<Step> run(bool reference, uint32_t seed, unsigned count) {
        reference_walk=reference && !reclaim_mode;
        reference_reclaim=reference && reclaim_mode;
        reclaim_walks=0; reclaim_frees=0;
        x=seed; framed=0; licensed=0; present=0;
        said.assign(1,"start");
        settle(); advance(400); state();
        for(unsigned n=0;n<count;++n) {
            steps.emplace_back(); said.emplace_back();
            step(); state();
            for(unsigned i=0;i<MBX_N_IF;++i) if(!reference && adapter.ifs[i].msrp && !adapter.ifs[i].stale) {
                EXPECT_TRUE(holds_walk(adapter.ifs[i]))<<"the copied run holds what a walk of the registrar copies, "
                                                         "after step "<<n<<": "<<said.back();
            }
        }
        walks=adapter.walks;
        walked=reclaim_walks; freed=reclaim_frees;
        reference_walk=false;
        reference_reclaim=false;
        auto made=steps;
        steps.assign(1,Step{});
        return made;
    }
    void differential(uint32_t seed, unsigned count) {
        const auto full=run(true,seed,count);
        const unsigned full_walks=walks, full_walked=walked, full_freed=freed, full_licensed=licensed,
                       full_present=present;
        const auto full_said=said;
        again();
        const auto copied=run(false,seed,count);
        ASSERT_EQ(copied.size(),full.size());
        for(size_t n=0;n<full.size();++n) {
            ASSERT_TRUE(copied[n]==full[n])<<"the copied run makes the reference run's mailbox writes and licence "
                                             "calls, in order, and holds its state, at step "<<n<<" of "<<count<<": "<<
                                             full_said[n]<<"; "<<first_difference(full[n],copied[n]);
        }
        EXPECT_EQ(said,full_said);
        if(reclaim_mode) {
            EXPECT_EQ(freed,full_freed)<<"the cut's reclaims free what the reference's freed";
            EXPECT_NE(full_freed,0u)<<"the random records leave attributes the reclaim frees";
            EXPECT_LT(walked,full_walked)<<"the cut walks the attributes only where one may be freed";
        } else {
            EXPECT_LT(walks,full_walks)<<"a Listener's change walks no registrar";
        }
        EXPECT_NE(full_licensed,0u)<<"the random records license a source";
        EXPECT_NE(full_present,0u)<<"the random records register a Listener";
    }
    // A Listener record of one value, source `n`'s StreamID, its event (802.1Q-2018 10.8.2.6: 0 New, 1 JoinIn,
    // 3 JoinMt, 4 Mt, 5 Lv) and declaration (2 Ready), settled.
    void listener(unsigned n, unsigned event, unsigned declaration=2) {
        const unsigned events[2]={event,0}, subtypes[2]={declaration,0};
        record(listeners(n,1,events,subtypes,false),false);
    }
};

TEST_F(Listeners, RandomRecordsMatchTheReferenceWalk) {
    differential(0x9E3779B9u,3000);
}

TEST_F(Listeners, ASecondSequenceMatchesTheReferenceWalk) {
    differential(0x2545F491u,3000);
}

// The SRP cut (#665's ruling of 2026-11-20, item 3) against the adapter before it, on the same records.
TEST_F(Listeners, RandomRecordsMatchTheReferenceReclaim) {
    reclaim_mode=true;
    differential(0x9E3779B9u,3000);
}

TEST_F(Listeners, ASecondSequenceMatchesTheReferenceReclaim) {
    reclaim_mode=true;
    differential(0x2545F491u,3000);
}

// A registered Listener's JoinIn changes no state, and THE TRANSMIT's builds, a LeaveAll's among them, move Applicants
// and Registrars but leave nothing mrp_reclaim frees, while the Listener stays declared: none owes the reclaim's walk of
// the participants' attributes, which the adapter before the cut made after every receive and every change.
TEST_F(Listeners, SteadyListenerRecordsAndBuildsWalkNoAttributes) {
    settle(); advance(400);
    listener(0,1); advance(300);
    const unsigned walked=reclaim_walks, held=ctrl_pool_in_use(&pool), sent=model.tx_sent;
    for(unsigned k=0;k<120;++k) {
        listener(0,1); advance(150);
    }
    EXPECT_GT(model.tx_sent,sent)<<"THE TRANSMIT built and sent MRPDUs meanwhile";
    EXPECT_EQ(ctrl_pool_in_use(&pool),held);
    EXPECT_EQ(reclaim_walks,walked)<<"a registered Listener's JoinIn and THE TRANSMIT's builds walk no attributes";
}

// An Mt of a Listener never registered: lwSRP creates its attribute at VO and MT and changes no state, so only the
// receive's own count owes the reclaim, which frees it by the next poll.
TEST_F(Listeners, AListenerLeftAsCreatedIsReclaimed) {
    settle(); advance(400);
    const unsigned held=ctrl_pool_in_use(&pool), walked=reclaim_walks;
    listener(1,4);
    EXPECT_GT(reclaim_walks,walked);
    EXPECT_EQ(ctrl_pool_in_use(&pool),held)<<"an attribute a receive created and left as created is reclaimed";
}

// The same in an MRPDU that also changes an attribute it did not create: its LeaveAll takes a registered Listener's
// Registrar from IN to LV, its Applicant from VO to LO, and that Listener's JoinIn its Registrar back (IEEE 802.1Q-2018
// Tables 10-3 and 10-4), changes out of no creation, which count for none. The Mt rides a second vector, after the
// LeaveAll's, so the LeaveAll leaves the attribute it creates as created.
TEST_F(Listeners, AListenerLeftAsCreatedBesideAnotherChangeIsReclaimed) {
    settle(); advance(400);
    listener(0,1); advance(300);
    const unsigned held=ctrl_pool_in_use(&pool);
    const unsigned joined[2]={1,0}, ready[2]={2,0}, mt[2]={4,0};
    auto f=listeners(0,1,joined,ready,true);
    const auto second=listeners(1,1,mt,ready,false);
    // the second's vector (header, FirstValue, its two packed events) before the first's EndMarks
    const size_t vector=2+8+1+1;
    f.insert(f.end()-4,second.begin()+14+5,second.begin()+14+5+vector);
    wire_put_be(f.data()+14+3,wire_be16(f.data()+14+3)+vector,2);
    record(f,false);
    EXPECT_EQ(ctrl_pool_in_use(&pool),held)<<"an attribute a receive created and left as created beside another "
                                              "change is reclaimed";
}

// A Listener's leave takes its Registrar to MT (Milan v1.2 4.2.7.2.2) with its Applicant observing: the change into
// that state owes the reclaim, which frees the attribute.
TEST_F(Listeners, ALeavingListenerIsReclaimed) {
    settle(); advance(400);
    const unsigned held=ctrl_pool_in_use(&pool);
    listener(1,1); advance(300);
    ASSERT_EQ(ctrl_pool_in_use(&pool),held+1u);
    listener(1,5); advance(1000);
    EXPECT_EQ(ctrl_pool_in_use(&pool),held)<<"an attribute changed into a state mrp_reclaim frees is reclaimed";
}
} // namespace
